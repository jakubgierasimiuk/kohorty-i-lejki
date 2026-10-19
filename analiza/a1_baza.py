"""A1 — baza DuckDB z danymi z zadania.

Ładuje wszystkie 17 plików CSV z dane/ do analiza/telemedi.duckdb, schemat `surowe`:
- każda kolumna ma jawnie podany typ (nic nie jest zgadywane z treści), puste pole = NULL,
- żadnego czyszczenia ani deduplikacji — eksport jest surowy i tak go zostawiamy (jakość danych to punkt A2),
- przy każdym wierszu: plik źródłowy i numer linii w pliku (do szukania duplikatów na stykach plików w A2),
- sesje i zdarzenia: obok czasu UTC czas polski (Europe/Warsaw, ze zmianą czasu) i dzień polski.
  Tabele z systemu transakcyjnego (users, orders, go_memberships, marketing_spend) są już w czasie polskim.

Kontrole na końcu: kolejność kolumn wobec słownika, liczby wierszy wobec zadania, przeliczenie czasu
porównane wiersz po wierszu z niezależnym przeliczeniem w Pythonie (zoneinfo), dni zmiany czasu.
Wynik: ekran + analiza/wyniki/a1_baza.txt.

Uruchomienie z głównego folderu projektu:
    python -I analiza/a1_baza.py
Skrypt tylko czyta dane/ i za każdym razem buduje bazę od nowa.
"""

import datetime as dt
import hashlib
import os
import zoneinfo

import duckdb
import pyarrow as pa
import pyarrow.csv as pacsv

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DANE = os.path.join(KATALOG, "dane")
BAZA = os.path.join(KATALOG, "analiza", "telemedi.duckdb")
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "a1_baza.txt")
STREFA = "Europe/Warsaw"

ID, TXT, TS, DATA, INT, ZL = "BIGINT", "VARCHAR", "TIMESTAMP", "DATE", "INTEGER", "DECIMAL(10,2)"

# tabela -> (pliki, kolumny w kolejności z nagłówka CSV z typem)
TABELE = {
    "users": (["users.csv"], {
        "user_id": ID, "registered_at": TS, "birth_year": INT, "gender": TXT, "region": TXT,
        "city_size": TXT, "marketing_consent": INT}),
    "sessions": ([f"sessions_{k}.csv" for k in
                  ("2024q4", "2025q1", "2025q2", "2025q3", "2025q4", "2026q1", "2026q2", "2026q3")], {
        "session_id": ID, "visitor_id": TXT, "user_id": ID, "started_at_utc": TS, "utm_source": TXT,
        "utm_medium": TXT, "utm_campaign": TXT, "device": TXT, "os": TXT, "browser": TXT,
        "landing_page": TXT}),
    "events": ([f"events_{k}.csv" for k in ("2024h2", "2025h1", "2025h2", "2026h1", "2026h2")], {
        "session_id": ID, "event_name": TXT, "event_at_utc": TS}),
    "orders": (["orders.csv"], {
        "order_id": ID, "user_id": ID, "session_id": ID, "created_at": TS, "specialization": TXT,
        "visit_purpose": TXT, "consultation_mode": TXT, "scheduled_at": TS, "started_at": TS,
        "duration_min": INT, "list_price": ZL, "discount_type": TXT, "promo_code": TXT,
        "amount_paid": ZL, "payment_method": TXT, "status": TXT, "refund_amount": ZL, "rating": INT}),
    "go_memberships": (["go_memberships.csv"], {
        "membership_id": ID, "user_id": ID, "purchased_at": TS, "valid_until": DATA, "amount_paid": ZL,
        "order_id": ID, "session_id": ID}),
    "marketing_spend": (["marketing_spend.csv"], {
        "date": DATA, "utm_source": TXT, "utm_medium": TXT, "utm_campaign": TXT, "impressions": INT,
        "clicks": INT, "spend_pln": "DECIMAL(12,2)"}),
}

# liczby wierszy z treści zadania (CLAUDE.md, punkt 6)
OCZEKIWANE = {"users": 52_422, "sessions": 459_557, "events": 494_605, "orders": 65_882,
              "go_memberships": 4_227, "marketing_spend": 5_676}

# kolumny czasu UTC z analityki -> nazwa kolumny w czasie polskim i dnia polskiego
CZAS_UTC = {"sessions": ("started_at_utc", "started_at_pl", "dzien_pl"),
            "events": ("event_at_utc", "event_at_pl", "dzien_pl")}


def sha256(sciezka):
    h = hashlib.sha256()
    with open(sciezka, "rb") as f:
        for kawalek in iter(lambda: f.read(1 << 20), b""):
            h.update(kawalek)
    return h.hexdigest()


def wczytaj(plik, kolumny):
    """Plik CSV jako tekst (bez zgadywania typów) + plik źródłowy i numer linii w pliku."""
    tabela = pacsv.read_csv(
        os.path.join(DANE, plik),
        convert_options=pacsv.ConvertOptions(column_types={k: pa.string() for k in kolumny},
                                             strings_can_be_null=False))
    if tabela.column_names != list(kolumny):
        raise SystemExit(f"{plik}: nagłówek {tabela.column_names} różni się od słownika {list(kolumny)}")
    n = tabela.num_rows
    tabela = tabela.append_column("plik", pa.array([plik] * n, pa.string()))
    # linia 1 to nagłówek; pola nie zawierają znaków nowej linii (profil kolumn), więc wiersz = linia
    return tabela.append_column("wiersz_w_pliku", pa.array(range(2, n + 2), pa.int64()))


def main():
    os.makedirs(os.path.dirname(WYNIK), exist_ok=True)
    if os.path.exists(BAZA):
        os.remove(BAZA)
    con = duckdb.connect(BAZA)
    con.execute("CREATE SCHEMA surowe")
    linie = []

    def r(t=""):
        print(t)
        linie.append(t)

    r(f"A1 — BAZA DANYCH ({dt.datetime.now():%Y-%m-%d %H:%M})")
    r(f"Baza: analiza/telemedi.duckdb, schemat `surowe`. DuckDB {duckdb.__version__}.")

    # --- ładowanie ---
    pliki_meta = []
    for nazwa, (pliki, kolumny) in TABELE.items():
        czesci = []
        for plik in pliki:
            t = wczytaj(plik, kolumny)
            czesci.append(t)
            sciezka = os.path.join(DANE, plik)
            pliki_meta.append((plik, nazwa, t.num_rows, os.path.getsize(sciezka), sha256(sciezka)))
        etap = pa.concat_tables(czesci)
        con.register("etap", etap)
        rzut = ", ".join(
            f'NULLIF("{k}", \'\') AS "{k}"' if typ == TXT else f'CAST(NULLIF("{k}", \'\') AS {typ}) AS "{k}"'
            for k, typ in kolumny.items())
        if nazwa in CZAS_UTC:
            utc, pl, dzien = CZAS_UTC[nazwa]
            # timezone('UTC', t) czyta t jako UTC; timezone(strefa, ...) zwraca czas lokalny w tej strefie
            dodatkowe = (f", timezone('{STREFA}', timezone('UTC', \"{utc}\")) AS {pl}"
                         f", CAST(timezone('{STREFA}', timezone('UTC', \"{utc}\")) AS DATE) AS {dzien}")
        else:
            dodatkowe = ""
        con.execute(f"CREATE TABLE surowe.{nazwa} AS "
                    f"SELECT *{dodatkowe} FROM (SELECT {rzut}, plik, wiersz_w_pliku FROM etap)")
        con.unregister("etap")

    con.execute("CREATE TABLE surowe.pliki (plik VARCHAR, tabela VARCHAR, wiersze BIGINT, "
                "bajty BIGINT, sha256 VARCHAR)")
    con.executemany("INSERT INTO surowe.pliki VALUES (?, ?, ?, ?, ?)", pliki_meta)

    # --- kontrola 1: liczby wierszy ---
    r("\n1. Liczby wierszy w bazie wobec treści zadania")
    razem_baza = razem_zadanie = 0
    zgodne = True
    for nazwa in TABELE:
        n = con.execute(f"SELECT count(*) FROM surowe.{nazwa}").fetchone()[0]
        nplikow = len(TABELE[nazwa][0])
        ok = n == OCZEKIWANE[nazwa]
        zgodne &= ok
        razem_baza += n
        razem_zadanie += OCZEKIWANE[nazwa]
        r(f"   {nazwa:16} {n:>9,} wierszy z {nplikow} pl.  zadanie: {OCZEKIWANE[nazwa]:>9,}  "
          f"{'zgodne' if ok else 'RÓŻNICA'}")
    r(f"   {'RAZEM':16} {razem_baza:>9,}                zadanie: {razem_zadanie:>9,}  "
      f"{'zgodne' if razem_baza == razem_zadanie else 'RÓŻNICA'}")
    r("   Wiersze w poszczególnych plikach:")
    for plik, nazwa, n, bajty, _ in pliki_meta:
        r(f"     {plik:24} {n:>8,}  ({bajty / 1e6:.1f} MB)")

    # --- kontrola 2: przeliczenie czasu wobec niezależnego przeliczenia w Pythonie ---
    r(f"\n2. Czas polski w sesjach i zdarzeniach (DuckDB) wobec niezależnego przeliczenia "
      f"w Pythonie (zoneinfo, baza stref tzdata)")
    tz = zoneinfo.ZoneInfo(STREFA)
    for nazwa, (utc, pl, dzien) in CZAS_UTC.items():
        df = con.execute(f"SELECT {utc}, {pl} FROM surowe.{nazwa}").df()
        oczek = df[utc].dt.tz_localize("UTC").dt.tz_convert(tz).dt.tz_localize(None)
        rozne = int((oczek != df[pl]).sum())
        r(f"   {nazwa:9} {len(df):>9,} wierszy, niezgodnych: {rozne}")

    # --- kontrola 3: przesunięcie wobec UTC i dni zmiany czasu ---
    r("\n3. Przesunięcie czasu polskiego wobec UTC")
    for nazwa, (utc, pl, dzien) in CZAS_UTC.items():
        wiersze = con.execute(f"""
            SELECT date_diff('hour', {utc}, {pl}) AS h, count(*), min({utc}), max({utc})
            FROM surowe.{nazwa} GROUP BY 1 ORDER BY 1""").fetchall()
        for h, n, od, do in wiersze:
            r(f"   {nazwa:9} UTC+{h}: {n:>9,} wierszy")
    r("   Dni (czas polski), w których przesunięcie się zmienia — powinny to być tylko dni zmiany czasu:")
    dni = con.execute(f"""
        SELECT dzien_pl,
               max(started_at_utc) FILTER (WHERE date_diff('hour', started_at_utc, started_at_pl) = 2) AS ost_2,
               min(started_at_utc) FILTER (WHERE date_diff('hour', started_at_utc, started_at_pl) = 1) AS pierw_1,
               max(started_at_utc) FILTER (WHERE date_diff('hour', started_at_utc, started_at_pl) = 1) AS ost_1,
               min(started_at_utc) FILTER (WHERE date_diff('hour', started_at_utc, started_at_pl) = 2) AS pierw_2
        FROM surowe.sessions GROUP BY 1
        HAVING count(DISTINCT date_diff('hour', started_at_utc, started_at_pl)) > 1 ORDER BY 1""").fetchall()
    for dzien, ost_2, pierw_1, ost_1, pierw_2 in dni:
        if ost_2 and pierw_1 and ost_2 < pierw_1:
            r(f"     {dzien}: koniec czasu letniego — ostatnia sesja UTC+2 o {ost_2:%H:%M} UTC, "
              f"pierwsza UTC+1 o {pierw_1:%H:%M} UTC")
        else:
            r(f"     {dzien}: początek czasu letniego — ostatnia sesja UTC+1 o {ost_1:%H:%M} UTC, "
              f"pierwsza UTC+2 o {pierw_2:%H:%M} UTC")

    # --- kontrola 4: zakres dat i skala przesunięcia dni ---
    r("\n4. Zakres dat i to, ile zmienia przeliczenie strefy")
    for nazwa, (utc, pl, dzien) in CZAS_UTC.items():
        od_pl, do_pl, od_utc, do_utc, inny_dzien, n = con.execute(f"""
            SELECT min({pl}), max({pl}), min({utc}), max({utc}),
                   count(*) FILTER (WHERE {dzien} <> CAST({utc} AS DATE)), count(*)
            FROM surowe.{nazwa}""").fetchone()
        r(f"   {nazwa:9} czas polski {od_pl} – {do_pl}  (UTC {od_utc} – {do_utc})")
        r(f"   {'':9} w innym dniu niż według UTC: {inny_dzien:,} wierszy, czyli {inny_dzien / n:.1%}")
    for nazwa, kol, opis in (("users", "registered_at", "czas polski z systemu transakcyjnego"),
                             ("orders", "created_at", "czas polski z systemu transakcyjnego"),
                             ("go_memberships", "purchased_at", "czas polski z systemu transakcyjnego"),
                             ("marketing_spend", "date", "dzień według czasu polskiego")):
        od, do = con.execute(f"SELECT min({kol}), max({kol}) FROM surowe.{nazwa}").fetchone()
        r(f"   {nazwa:16} {kol}: {od} – {do}  ({opis})")

    con.close()
    r(f"\nBaza zapisana: analiza/telemedi.duckdb ({os.path.getsize(BAZA) / 1e6:.0f} MB, poza repozytorium).")
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Raport zapisany: {os.path.relpath(WYNIK, KATALOG)}")
    if not zgodne:
        raise SystemExit("Liczby wierszy niezgodne z zadaniem — sprawdź raport.")


if __name__ == "__main__":
    main()
