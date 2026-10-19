"""A4 — warianty definicji przed kohortami (2026-10-19).

  1. Nowy pacjent: cztery warianty i łączenie kont po przeglądarce.
  2. Anulacje i zwroty: pierwsze zamówienia według statusu, anulowane powroty, przychód netto.
  3. Powrót: cztery warianty, okna 30, 60 i 90 dni.
  4. Źródło pozyskania: reguły przypisania, kontrola kodami kampanii, prowizja afiliacyjna.
  5. Okno powrotu po wejściu z newslettera albo SMS-a.

Przy każdym wariancie: ile zmienia w liczbie nowych pacjentów, w powrotach i w strukturze źródeł.
Warianty zmieniamy po jednym; pozostałe definicje stoją wtedy na wariancie odniesienia
(nowy pacjent = pierwsze opłacone zamówienie, powrót = kolejne opłacone zamówienie,
źródło = sesja płatności).

Tylko czyta schemat `czyste` (analiza/a2_czyste.py). Uruchomienie z głównego folderu projektu:
    python -I analiza/a4_definicje.py
Wynik: analiza/wyniki/a4_definicje.txt, analiza/wyniki/a4_zrodla_kampanie.csv
"""

import datetime as dt
import os
import sys

import duckdb
import pandas as pd

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAZA = os.path.join(KATALOG, "analiza", "telemedi.duckdb")
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "a4_definicje.txt")
WYNIK_KAMPANIE = os.path.join(KATALOG, "analiza", "wyniki", "a4_zrodla_kampanie.csv")
WYNIK_PRZYKLADY = os.path.join(KATALOG, "analiza", "wyniki", "a4_przyklady.txt")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)

KONIEC = "2026-09-30"   # ostatni dzień danych
OKRES2 = "2025-10-01"   # początek drugiego roku dashboardu (czas polski)
OKNA = (30, 60, 90)

KANAL = """
  CASE WHEN utm_source IS NULL THEN 'bezposrednie'
       WHEN utm_campaign = 'gs_brand' THEN 'google_ads_marka'
       WHEN utm_campaign LIKE 'gs_generic%' THEN 'google_ads_ogolne'
       WHEN utm_medium = 'organic' THEN 'wyszukiwarka_bezplatna'
       WHEN utm_campaign LIKE 'meta_prosp%' THEN 'meta_pozyskanie'
       WHEN utm_campaign = 'meta_rmkt_koszyk' THEN 'meta_remarketing'
       WHEN utm_source = 'tiktok' THEN 'tiktok'
       WHEN utm_medium = 'affiliate' THEN 'afiliacja_ranking'
       WHEN utm_medium = 'referral' THEN 'program_polecen'
       WHEN utm_medium IN ('email', 'sms') THEN 'crm'
       ELSE 'inne' END"""

# kod kampanii na pierwszym zamówieniu -> kanał i kampania, które kod wskazuje
KODY = {"L4SZYBKO20": ("meta_pozyskanie", "meta_prosp_l4_szybko"),
        "TIKTOK25": ("tiktok", "tt_prosp_l4_15min"),
        "RANKING10": ("afiliacja_ranking", "rankinglekarzy_affiliate")}

NOWY = {"N1": "pierwsze opłacone zamówienie konsultacji (dowolny status) — jak dashboard",
        "N2": "pierwsza jakakolwiek płatność (zamówienie albo samo TelemediGO)",
        "N3": "pierwsze zamówienie nieanulowane (odbyte, zwrócone po wizycie albo nieodebrane)",
        "N4": "pierwsza wizyta, która się odbyła (odbyta albo zwrócona po wizycie)"}
POWROT = {"R1": "kolejne opłacone zamówienie (dowolny status)",
          "R2": "kolejne zamówienie nieanulowane",
          "R3": "kolejna wizyta, która się odbyła",
          "R4": "R1 albo osobny zakup TelemediGO"}
POWROT_SQL = {"R1": "z.rodzaj = 'zam'",
              "R2": "z.rodzaj = 'zam' AND z.status <> 'cancelled'",
              "R3": "z.rodzaj = 'zam' AND z.status IN ('completed', 'refunded')",
              "R4": "TRUE"}


def main():
    sys.stdout.reconfigure(errors="replace")
    con = duckdb.connect(BAZA, read_only=True)
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def df(sql):
        return con.sql(sql).df()

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    def tab(sql, wciecie="     "):
        pokaz(df(sql), wciecie)

    r(f"A4 — WARIANTY DEFINICJI ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r(f"Okres 1 = 1.10.2024 – 30.09.2025, okres 2 = 1.10.2025 – 30.09.2026 (data pierwszego zakupu, czas polski).")
    r("Powrót w N dniach = zdarzenie powrotu najpóźniej N-tego dnia kalendarzowego po dniu wejścia do kohorty.")
    r("Liczony tylko dla kohort z pełnym oknem (dzień kohorty <= 30.09.2026 minus N dni): 30 dni do 31.08.2026,")
    r("60 dni do 1.08.2026, 90 dni do 2.07.2026. Okres 1 ma pełne okna w całości.")

    # ---------- tabele pomocnicze ----------
    con.execute("""
      CREATE TEMP TABLE zam AS
      SELECT o.*, row_number() OVER (PARTITION BY user_id ORDER BY created_at, order_id) nr
      FROM czyste.orders o""")
    con.execute(f"""
      CREATE TEMP TABLE ses AS
      SELECT session_id, visitor_id, user_id, started_at_pl, started_at_utc, utm_source, utm_medium, utm_campaign, landing_page,
             {KANAL} kanal,
             coalesce(utm_campaign, utm_source || '_' || utm_medium, 'bezposrednie') kampania
      FROM czyste.sessions""")
    con.execute("CREATE TEMP TABLE przeg AS SELECT DISTINCT visitor_id, user_id FROM czyste.sessions WHERE user_id IS NOT NULL")
    con.execute("""
      CREATE TEMP TABLE ses_pac AS
      SELECT coalesce(s.user_id, p.user_id) pacjent, s.*, s.user_id IS NULL anonimowa
      FROM ses s LEFT JOIN przeg p ON p.visitor_id = s.visitor_id
      WHERE coalesce(s.user_id, p.user_id) IS NOT NULL""")
    # kohorty w czterech wariantach nowego pacjenta
    con.execute("""
      CREATE TEMP TABLE koh AS
      WITH n1 AS (SELECT 'N1' war, user_id, created_at t0, session_id, order_id FROM zam WHERE nr = 1),
           n2 AS (SELECT 'N2' war, user_id, t0, session_id, order_id FROM (
                    SELECT *, row_number() OVER (PARTITION BY user_id ORDER BY t0, rodzaj) k FROM (
                      SELECT user_id, created_at t0, session_id, order_id, 1 rodzaj FROM zam
                      UNION ALL
                      SELECT user_id, purchased_at, session_id, NULL, 0 FROM czyste.go_memberships WHERE order_id IS NULL))
                  WHERE k = 1),
           n3 AS (SELECT 'N3' war, user_id, created_at t0, session_id, order_id FROM (
                    SELECT *, row_number() OVER (PARTITION BY user_id ORDER BY created_at, order_id) k
                    FROM zam WHERE status <> 'cancelled') WHERE k = 1),
           n4 AS (SELECT 'N4' war, user_id, created_at t0, session_id, order_id FROM (
                    SELECT *, row_number() OVER (PARTITION BY user_id ORDER BY created_at, order_id) k
                    FROM zam WHERE status IN ('completed', 'refunded')) WHERE k = 1)
      SELECT *, t0::DATE d0, CASE WHEN t0 < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres
      FROM (SELECT * FROM n1 UNION ALL SELECT * FROM n2 UNION ALL SELECT * FROM n3 UNION ALL SELECT * FROM n4)""")
    # zdarzenia, które mogą być powrotem
    con.execute("""
      CREATE TEMP TABLE zd AS
      SELECT user_id, created_at t, 'zam' rodzaj, status FROM zam
      UNION ALL
      SELECT user_id, purchased_at, 'go', NULL FROM czyste.go_memberships WHERE order_id IS NULL""")
    wyr = ",\n".join(
        f"min(date_diff('day', k.d0, z.t::DATE)) FILTER (WHERE {w}) dni_{n}" for n, w in POWROT_SQL.items())
    con.execute(f"""
      CREATE TEMP TABLE powr AS
      SELECT k.war, k.user_id, k.d0, k.okres, k.session_id, {wyr}
      FROM koh k LEFT JOIN zd z ON z.user_id = k.user_id AND z.t > k.t0
      GROUP BY ALL""")

    def stopy(war="N1", powrot="R1", grupa=None, warunek="TRUE"):
        """Odsetek kohorty z powrotem w 30/60/90 dniach, osobno dla okresu 1 i 2 (tylko pełne okna)."""
        g = f"{grupa}, " if grupa else ""
        kol = []
        for n in OKNA:
            for o in (1, 2):
                kol.append(f"""round(100.0 * count(*) FILTER (WHERE okres = {o} AND d0 <= DATE '{KONIEC}' - {n}
                                 AND dni_{powrot} <= {n})
                            / nullif(count(*) FILTER (WHERE okres = {o} AND d0 <= DATE '{KONIEC}' - {n}), 0), 1) p{n}_o{o}""")
        return f"SELECT {g}{', '.join(kol)} FROM powr WHERE war = '{war}' AND {warunek} {'GROUP BY ' + grupa if grupa else ''}"

    def stopy_por(war="N1", powrot="R2"):
        """Jak stopy(), ale okres 1 obcięty do tych samych dni kalendarzowych, co dojrzała część okresu 2."""
        koniec = dt.date.fromisoformat(KONIEC)
        kol = []
        for n in OKNA:
            g2 = koniec - dt.timedelta(days=n)
            g1 = g2.replace(year=g2.year - 1)
            w1 = f"okres = 1 AND d0 <= DATE '{g1}'"
            w2 = f"okres = 2 AND d0 <= DATE '{g2}'"
            kol += [f"round(100.0 * count(*) FILTER (WHERE {w1} AND dni_{powrot} <= {n}) / count(*) FILTER (WHERE {w1}), 1) p{n}_o1",
                    f"round(100.0 * count(*) FILTER (WHERE {w2} AND dni_{powrot} <= {n}) / count(*) FILTER (WHERE {w2}), 1) p{n}_o2",
                    f"count(*) FILTER (WHERE {w1}) n{n}_o1", f"count(*) FILTER (WHERE {w2}) n{n}_o2"]
        return f"SELECT {', '.join(kol)} FROM powr WHERE war = '{war}'"

    # ============ 1. NOWY PACJENT ============
    r("\n" + "=" * 100)
    r("1. NOWY PACJENT")
    r("=" * 100)
    for k, v in NOWY.items():
        r(f"   {k}: {v}")

    r("\n1a. Liczba nowych pacjentów i zmiana wobec N1")
    tab("""
      WITH a AS (SELECT * FROM koh), b AS (SELECT * FROM koh WHERE war = 'N1')
      SELECT a.war wariant,
             count(*) FILTER (WHERE a.okres = 1) nowi_okres1,
             count(*) FILTER (WHERE a.okres = 2) nowi_okres2,
             round(100.0 * count(*) FILTER (WHERE a.okres = 2) / count(*) FILTER (WHERE a.okres = 1) - 100, 1) wzrost_proc,
             count(*) nowi_razem,
             (SELECT count(*) FROM b) - count(*) wypada_wobec_N1,
             count(*) FILTER (WHERE a.d0 <> b.d0) zmienia_dzien_kohorty,
             count(*) FILTER (WHERE a.okres <> b.okres) zmienia_okres
      FROM a JOIN b USING (user_id) GROUP BY 1 ORDER BY 1""")
    tab("""
      SELECT count(*) FILTER (WHERE purchased_at < (SELECT min(created_at) FROM zam z WHERE z.user_id = g.user_id))
               go_osobno_przed_pierwszym_zamowieniem,
             count(*) FILTER (WHERE user_id NOT IN (SELECT user_id FROM zam)) go_bez_zadnego_zamowienia
      FROM czyste.go_memberships g WHERE order_id IS NULL""")

    r("\n1b. Powrót (R1: kolejne opłacone zamówienie) w 30/60/90 dniach, % kohorty, okres 1 wobec okresu 2")
    pokaz(pd.concat([df(stopy(w)).assign(wariant=w) for w in NOWY]).set_index("wariant").reset_index())

    r("\n1c. Struktura źródeł nowych pacjentów (kanał sesji zdarzenia, które robi z pacjenta nowego), % pacjentów, dwa lata")
    s = df("""
      SELECT k.war, s.kanal, count(*) n FROM koh k JOIN ses s USING (session_id) GROUP BY ALL""")
    s["proc"] = (100 * s.n / s.groupby("war").n.transform("sum")).round(1)
    piv = s.pivot(index="kanal", columns="war", values="proc").fillna(0)
    for w in ("N2", "N3", "N4"):
        piv[f"{w}-N1_pkt"] = (piv[w] - piv["N1"]).round(1)
    pokaz(piv.sort_values("N1", ascending=False).reset_index())

    r("\n1d. Pierwsze zamówienie według statusu w każdym kanale (sesja płatności), % pierwszych zamówień")
    tab("""
      SELECT s.kanal, count(*) pierwsze_zamowienia,
             round(100.0 * count(*) FILTER (WHERE z.status = 'cancelled') / count(*), 1) proc_anulowane,
             round(100.0 * count(*) FILTER (WHERE z.status = 'no_show') / count(*), 1) proc_nieodebrane,
             round(100.0 * count(*) FILTER (WHERE z.status = 'refunded') / count(*), 1) proc_zwrot_po_wizycie
      FROM zam z JOIN ses s USING (session_id) WHERE z.nr = 1 GROUP BY 1 ORDER BY 2 DESC""")

    r("\n1e. Łączenie kont po przeglądarce")
    tab("""
      SELECT count(*) przegladarki_z_kontem,
             count(*) FILTER (WHERE n > 1) przegladarki_z_wiecej_niz_jednym_kontem
      FROM (SELECT visitor_id, count(DISTINCT user_id) n FROM przeg GROUP BY 1)""")
    tab("""
      SELECT count(*) konta, count(*) FILTER (WHERE n > 1) konta_z_wiecej_niz_jedna_przegladarka
      FROM (SELECT user_id, count(DISTINCT visitor_id) n FROM przeg GROUP BY 1)""")
    r("     Żadna przeglądarka nie należy do dwóch kont, więc łączenie kont po przeglądarce nie zmienia liczby pacjentów.")
    r("     Przeglądarka łączy tylko anonimowe sesje z kontem (to wykorzystuje reguła źródła w punkcie 4).")

    # ============ 2. ANULACJE I ZWROTY ============
    r("\n" + "=" * 100)
    r("2. ANULACJE I ZWROTY")
    r("=" * 100)
    r("   Statusy: completed = wizyta odbyta; cancelled = anulowana przed wizytą, pełny zwrot; no_show = pacjent nie")
    r("   odebrał, bez zwrotu; refunded = wizyta odbyta, zwrot po wizycie. Koszt lekarza: completed i refunded.")

    r("\n2a. Pierwsze zamówienie pacjenta według statusu i powrót (R1) w 30/60/90 dniach")
    tab(f"""
      SELECT z.status, count(*) pacjenci, round(100.0 * count(*) / sum(count(*)) OVER (), 1) proc_pacjentow,
             count(*) FILTER (WHERE p.okres = 1) okres1, count(*) FILTER (WHERE p.okres = 2) okres2,
             {', '.join(f"round(100.0 * count(*) FILTER (WHERE p.d0 <= DATE '{KONIEC}' - {n} AND p.dni_R1 <= {n}) / count(*) FILTER (WHERE p.d0 <= DATE '{KONIEC}' - {n}), 1) powrot{n}_proc" for n in OKNA)}
      FROM powr p JOIN zam z ON z.user_id = p.user_id AND z.nr = 1
      WHERE p.war = 'N1' GROUP BY 1 ORDER BY 2 DESC""")
    r("     Pacjenci z anulowanym pierwszym zamówieniem: czy i kiedy składają nieanulowane zamówienie")
    tab("""
      SELECT count(*) pacjenci_anulowane_pierwsze,
             count(n3.user_id) maja_pozniej_nieanulowane,
             count(*) FILTER (WHERE date_diff('day', n1.d0, n3.d0) <= 7) w_ciagu_7_dni,
             count(*) FILTER (WHERE date_diff('day', n1.d0, n3.d0) <= 30) w_ciagu_30_dni,
             count(*) - count(n3.user_id) nigdy
      FROM koh n1 JOIN zam z ON z.user_id = n1.user_id AND z.nr = 1 AND z.status = 'cancelled'
      LEFT JOIN koh n3 ON n3.user_id = n1.user_id AND n3.war = 'N3'
      WHERE n1.war = 'N1'""")

    r("\n2b. Kolejne zamówienia (od drugiego) według statusu — czy anulowany powrót jest powrotem")
    tab("""
      SELECT status, count(*) zamowienia_powtorne, round(100.0 * count(*) / sum(count(*)) OVER (), 1) proc
      FROM zam WHERE nr > 1 GROUP BY 1 ORDER BY 2 DESC""")
    tab(f"""
      SELECT count(*) pacjenci_z_powrotem_R1_90d,
             count(*) FILTER (WHERE dni_R2 IS NULL OR dni_R2 > 90) z_tego_w_90d_tylko_anulowane
      FROM powr WHERE war = 'N1' AND d0 <= DATE '{KONIEC}' - 90 AND dni_R1 <= 90""")

    r("\n2c. Przychód z konsultacji: zapłaty przed zwrotami, zwroty i przychód po zwrotach, zł")
    r("     Zwrot przypisujemy do dnia płatności zamówienia (w danych nie ma daty zwrotu).")
    tab("""
      SELECT CASE WHEN created_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres, status,
             count(*) zamowienia, round(sum(amount_paid)) zaplaty_zl, round(sum(refund_amount)) zwroty_zl,
             round(sum(amount_paid - refund_amount)) po_zwrotach_zl
      FROM zam GROUP BY ALL ORDER BY 1, 3 DESC""")
    tab("""
      WITH a AS (SELECT CASE WHEN created_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres,
                        sum(amount_paid) zapl, sum(refund_amount) zwr FROM zam GROUP BY 1),
           g AS (SELECT CASE WHEN purchased_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres,
                        sum(amount_paid) go FROM czyste.go_memberships GROUP BY 1),
           w AS (SELECT okres, zapl, zapl - zwr netto, zapl - zwr + go netto_z_go FROM a JOIN g USING (okres))
      SELECT 'A: zaplaty przed zwrotami (dashboard)' wariant,
             round(max(zapl) FILTER (WHERE okres = 1)) okres1_zl, round(max(zapl) FILTER (WHERE okres = 2)) okres2_zl,
             round(100 * max(zapl) FILTER (WHERE okres = 2) / max(zapl) FILTER (WHERE okres = 1) - 100, 1) wzrost_proc FROM w
      UNION ALL
      SELECT 'B: po zwrotach', round(max(netto) FILTER (WHERE okres = 1)), round(max(netto) FILTER (WHERE okres = 2)),
             round(100 * max(netto) FILTER (WHERE okres = 2) / max(netto) FILTER (WHERE okres = 1) - 100, 1) FROM w
      UNION ALL
      SELECT 'C: po zwrotach + TelemediGO', round(max(netto_z_go) FILTER (WHERE okres = 1)),
             round(max(netto_z_go) FILTER (WHERE okres = 2)),
             round(100 * max(netto_z_go) FILTER (WHERE okres = 2) / max(netto_z_go) FILTER (WHERE okres = 1) - 100, 1) FROM w""")

    # ============ 3. POWRÓT ============
    r("\n" + "=" * 100)
    r("3. POWRÓT (nowy pacjent = N1)")
    r("=" * 100)
    for k, v in POWROT.items():
        r(f"   {k}: {v}")
    r("\n3a. Odsetek kohorty z powrotem w 30/60/90 dniach, okres 1 wobec okresu 2")
    pokaz(pd.concat([df(stopy("N1", p)).assign(wariant=p) for p in POWROT]).set_index("wariant").reset_index())
    r("     Liczba kohort dziennych i pacjentów z pełnym oknem:")
    tab(f"""
      SELECT {', '.join(f"count(DISTINCT d0) FILTER (WHERE d0 <= DATE '{KONIEC}' - {n}) dni_{n}, count(*) FILTER (WHERE d0 <= DATE '{KONIEC}' - {n}) pacjenci_{n}" for n in OKNA)}
      FROM powr WHERE war = 'N1'""")

    r("\n3b. Ile dni mija od pierwszego do drugiego zamówienia (wszyscy pacjenci z drugim zamówieniem)")
    tab("""
      WITH d AS (SELECT date_diff('day', a.created_at::DATE, b.created_at::DATE) dni
                 FROM zam a JOIN zam b ON a.user_id = b.user_id AND a.nr = 1 AND b.nr = 2)
      SELECT CASE WHEN dni = 0 THEN '0 (ten sam dzien)' WHEN dni <= 7 THEN '1-7' WHEN dni <= 14 THEN '8-14'
                  WHEN dni <= 30 THEN '15-30' WHEN dni <= 60 THEN '31-60' WHEN dni <= 90 THEN '61-90'
                  WHEN dni <= 180 THEN '91-180' ELSE 'ponad 180' END przedzial_dni,
             count(*) pacjenci, round(100.0 * count(*) / sum(count(*)) OVER (), 1) proc, min(dni) min_dni
      FROM d GROUP BY 1 ORDER BY min(dni)""")
    tab("""
      SELECT min(date_diff('minute', a.created_at, b.created_at)) najkrotsza_przerwa_min_miedzy_kolejnymi_zamowieniami,
             count(*) FILTER (WHERE a.created_at::DATE = b.created_at::DATE) kolejne_zamowienia_tego_samego_dnia
      FROM zam a JOIN zam b ON a.user_id = b.user_id AND b.nr = a.nr + 1""")

    r("\n3c. Osobny zakup TelemediGO jako powrót: ile razy w 90 dniach to jedyny powrót")
    tab(f"""
      SELECT count(*) FILTER (WHERE dni_R4 <= 90) z_powrotem_R4,
             count(*) FILTER (WHERE dni_R1 <= 90) z_powrotem_R1,
             count(*) FILTER (WHERE dni_R4 <= 90 AND (dni_R1 IS NULL OR dni_R1 > 90)) tylko_go
      FROM powr WHERE war = 'N1' AND d0 <= DATE '{KONIEC}' - 90""")

    r("     Kontrola: osobne zakupy TelemediGO według dni od pierwszego zamówienia i zamówienia w tym samym oknie")
    tab("""
      WITH g AS (SELECT g.user_id, date_diff('day', k.d0, g.purchased_at::DATE) dni,
                        (SELECT count(*) FROM zam z WHERE z.user_id = g.user_id AND z.created_at > k.t0
                           AND z.created_at <= g.purchased_at) zamowien_wczesniej
                 FROM czyste.go_memberships g JOIN koh k ON k.user_id = g.user_id AND k.war = 'N1'
                 WHERE g.order_id IS NULL)
      SELECT CASE WHEN dni <= 90 THEN 'do 90 dni' ELSE 'po 90 dniach' END kiedy, count(*) zakupy_go_osobno,
             count(*) FILTER (WHERE zamowien_wczesniej = 0) przed_drugim_zamowieniem
      FROM g GROUP BY 1 ORDER BY 1""")

    r("\n3d. Powrót w 90 dniach według kanału (sesja płatności pierwszego zamówienia), cztery warianty powrotu, %")
    r("     (warianty powrotu nie zmieniają, kto jest nowym pacjentem ani z jakiego źródła przyszedł)")
    rama = None
    for p in POWROT:
        x = df(f"""
          SELECT s.kanal, count(*) FILTER (WHERE d0 <= DATE '{KONIEC}' - 90) kohorta_90d,
                 round(100.0 * count(*) FILTER (WHERE d0 <= DATE '{KONIEC}' - 90 AND dni_{p} <= 90)
                       / count(*) FILTER (WHERE d0 <= DATE '{KONIEC}' - 90), 1) {p}
          FROM powr JOIN ses s USING (session_id) WHERE war = 'N1' GROUP BY 1""")
        rama = x if rama is None else rama.merge(x[["kanal", p]], on="kanal")
    pokaz(rama.sort_values("kohorta_90d", ascending=False))

    # ============ 4. ŹRÓDŁO POZYSKANIA ============
    r("\n" + "=" * 100)
    r("4. ŹRÓDŁO POZYSKANIA (nowy pacjent = N1, czyli pierwsze opłacone zamówienie)")
    r("=" * 100)
    r("   Z1: pierwsze wejście pacjenta (sesje konta + anonimowe sesje jego przeglądarek, do momentu zakupu)")
    r("   Z1b: pierwsze wejście bez łączenia przez przeglądarkę (tylko sesje z kontem)")
    r("   Z2: sesja, w której zapłacił")
    r("   Z3: ostatnie wejście z oznaczonego źródła (nie bezpośrednie) w 30 dniach przed zakupem; brak = bezpośrednie")
    r("   Z3_7, Z3_90: to samo z oknem 7 i 90 dni (wrażliwość okna)")
    r("   Z1K, Z2K, Z3K: kod kampanii na pierwszym zamówieniu wskazuje źródło, w pozostałych reguła bez zmian")
    con.execute("""
      CREATE TEMP TABLE sp AS
      SELECT k.user_id, k.t0, k.okres, k.session_id sesja_platnosci, s.session_id, s.started_at_pl,
             s.kanal, s.kampania, s.anonimowa, s.landing_page
      FROM koh k JOIN ses_pac s ON s.pacjent = k.user_id AND s.started_at_pl <= k.t0
      WHERE k.war = 'N1'""")

    def ostatnie_oznaczone(dni):
        w = f"kanal <> 'bezposrednie' AND started_at_pl >= t0 - INTERVAL {dni} DAY"
        return (f"coalesce(arg_max(kanal, started_at_pl) FILTER (WHERE {w}), 'bezposrednie') Z3_{dni}_kanal, "
                f"coalesce(arg_max(kampania, started_at_pl) FILTER (WHERE {w}), 'bezposrednie') Z3_{dni}_kampania")

    con.execute(f"""
      CREATE TEMP TABLE reg AS
      SELECT user_id, okres, any_value(z.promo_code) kod,
             arg_min(kanal, (started_at_pl, session_id)) Z1_kanal, arg_min(kampania, (started_at_pl, session_id)) Z1_kampania,
             arg_min(kanal, (started_at_pl, session_id)) FILTER (WHERE NOT anonimowa) Z1b_kanal,
             arg_min(kampania, (started_at_pl, session_id)) FILTER (WHERE NOT anonimowa) Z1b_kampania,
             any_value(kanal) FILTER (WHERE session_id = sesja_platnosci) Z2_kanal,
             any_value(kampania) FILTER (WHERE session_id = sesja_platnosci) Z2_kampania,
             {ostatnie_oznaczone(30)}, {ostatnie_oznaczone(7)}, {ostatnie_oznaczone(90)},
             count(*) sesje_do_zakupu, count(*) FILTER (WHERE anonimowa) sesje_anonimowe,
             max((landing_page = '/polecenie')::INT) bylo_wejscie_polecenie
      FROM sp JOIN (SELECT user_id u, promo_code FROM zam WHERE nr = 1) z ON z.u = sp.user_id
      GROUP BY 1, 2""")
    # długi format: pacjent x reguła -> kanał, kampania
    reguly = {"Z1": "Z1", "Z1b": "Z1b", "Z2": "Z2", "Z3": "Z3_30", "Z3_7": "Z3_7", "Z3_90": "Z3_90"}
    czesci = [f"SELECT user_id, okres, kod, '{n}' regula, {c}_kanal kanal, {c}_kampania kampania FROM reg"
              for n, c in reguly.items()]
    przyp_k = " ".join(f"WHEN '{k}' THEN '{v[0]}'" for k, v in KODY.items())
    przyp_c = " ".join(f"WHEN '{k}' THEN '{v[1]}'" for k, v in KODY.items())
    for n in ("Z1", "Z2", "Z3"):
        c = reguly[n]
        czesci.append(f"""SELECT user_id, okres, kod, '{n}K' regula,
                          coalesce(CASE kod {przyp_k} END, {c}_kanal) kanal,
                          coalesce(CASE kod {przyp_c} END, {c}_kampania) kampania FROM reg""")
    con.execute("CREATE TEMP TABLE zr AS " + " UNION ALL ".join(czesci))
    kolejnosc = ["Z1", "Z1b", "Z2", "Z3", "Z3_7", "Z3_90", "Z1K", "Z2K", "Z3K"]

    r("\n4a. Łączenie anonimowych sesji z kontem przez przeglądarkę")
    tab("""
      SELECT count(*) nowi_pacjenci,
             (SELECT count(*) FROM koh WHERE war = 'N1') - count(*) bez_sesji_przed_zakupem,
             count(*) FILTER (WHERE sesje_anonimowe > 0) z_anonimowa_sesja_przed_zakupem,
             round(avg(sesje_do_zakupu), 2) srednio_sesji_do_zakupu,
             count(*) FILTER (WHERE sesje_do_zakupu = 1) tylko_sesja_platnosci,
             count(*) FILTER (WHERE Z1b_kanal IS NULL) bez_sesji_z_kontem
      FROM reg""")
    r("     Dni od pierwszego wejścia (Z1) do pierwszego zamówienia:")
    tab("""
      WITH d AS (SELECT user_id, date_diff('day', min(started_at_pl)::DATE, any_value(t0)::DATE) dni FROM sp GROUP BY 1)
      SELECT CASE WHEN dni = 0 THEN '0 (ten sam dzien)' WHEN dni <= 7 THEN '1-7' WHEN dni <= 30 THEN '8-30'
                  WHEN dni <= 90 THEN '31-90' ELSE 'ponad 90' END przedzial_dni,
             count(*) pacjenci, round(100.0 * count(*) / sum(count(*)) OVER (), 1) proc
      FROM d GROUP BY 1 ORDER BY min(dni)""")

    r("\n4b. Struktura źródeł nowych pacjentów według reguły, % pacjentów, dwa lata")
    s = df("SELECT regula, kanal, count(*) n FROM zr GROUP BY ALL")
    s["proc"] = (100 * s.n / s.groupby("regula").n.transform("sum")).round(1)
    piv = s.pivot(index="kanal", columns="regula", values="proc").fillna(0)[kolejnosc]
    pokaz(piv.sort_values("Z2", ascending=False).reset_index())
    r("     Liczba pacjentów:")
    piv_n = s.pivot(index="kanal", columns="regula", values="n").fillna(0).astype(int)[kolejnosc]
    pokaz(piv_n.sort_values("Z2", ascending=False).reset_index())

    r("\n4c. Ilu pacjentów zmienia kanał wobec Z2 (sesja płatności)")
    tab(f"""
      SELECT a.regula, count(*) FILTER (WHERE a.kanal <> b.kanal) zmienia_kanal,
             round(100.0 * count(*) FILTER (WHERE a.kanal <> b.kanal) / count(*), 1) proc,
             count(*) FILTER (WHERE a.kampania <> b.kampania) zmienia_kampanie
      FROM zr a JOIN zr b ON a.user_id = b.user_id AND b.regula = 'Z2'
      GROUP BY 1 ORDER BY list_position({kolejnosc}, a.regula)""")
    r("     Wariant z kodem wobec tej samej reguły bez kodu:")
    tab("""
      SELECT a.regula, count(*) FILTER (WHERE a.kanal <> b.kanal) zmienia_kanal_wobec_reguly_bez_kodu
      FROM zr a JOIN zr b ON a.user_id = b.user_id AND b.regula = replace(a.regula, 'K', '')
      WHERE a.regula IN ('Z1K', 'Z2K', 'Z3K') GROUP BY 1 ORDER BY 1""")

    r("\n4d. Kontrola kodami kampanii: % pacjentów z kodem, których reguła przypisuje do kampanii kodu")
    kontrola = []
    for kod, (kanal, kampania) in KODY.items():
        x = df(f"""
          SELECT regula, count(*) n, round(100.0 * count(*) FILTER (WHERE kampania = '{kampania}') / count(*), 1) proc
          FROM zr WHERE kod = '{kod}' GROUP BY 1""")
        x["kod"] = f"{kod} ({x.n.iloc[0]} pacjentów)"
        kontrola.append(x)
    k = pd.concat(kontrola).pivot(index="kod", columns="regula", values="proc")[kolejnosc]
    pokaz(k.reset_index())
    r("     Gdzie trafiają pacjenci z kodem, których reguła NIE przypisuje do kampanii kodu (wszystkie trzy kody razem):")
    przyp_kamp = " ".join(f"WHEN '{k}' THEN '{v[1]}'" for k, v in KODY.items())
    tab(f"""
      SELECT regula, kanal, count(*) pacjenci
      FROM zr WHERE kod IN ({', '.join(f"'{k}'" for k in KODY)}) AND kampania <> CASE kod {przyp_kamp} END
        AND regula IN ('Z1', 'Z2', 'Z3')
      GROUP BY regula, kanal QUALIFY row_number() OVER (PARTITION BY regula ORDER BY count(*) DESC) <= 4
      ORDER BY regula, pacjenci DESC""")

    r("\n4e. Prowizja afiliacyjna (25 zł za pierwsze opłacone zamówienie pacjenta przypisanego do rankingu)")
    r("     README: prowizja należy się także wtedy, gdy pierwsze zamówienie zostało potem anulowane albo zwrócone.")
    tab(f"""
      SELECT regula, count(*) FILTER (WHERE okres = 1) pacjenci_okres1, count(*) FILTER (WHERE okres = 2) pacjenci_okres2,
             count(*) pacjenci_razem, 25 * count(*) prowizja_zl
      FROM zr WHERE kanal = 'afiliacja_ranking' GROUP BY 1 ORDER BY list_position({kolejnosc}, regula)""")
    tab("""
      SELECT 'kod RANKING10' wariant, count(*) FILTER (WHERE okres = 1) pacjenci_okres1,
             count(*) FILTER (WHERE okres = 2) pacjenci_okres2, count(*) pacjenci_razem, 25 * count(*) prowizja_zl
      FROM reg WHERE kod = 'RANKING10'
      UNION ALL
      SELECT 'kod RANKING10 albo sesja platnosci z rankingu', count(*) FILTER (WHERE okres = 1),
             count(*) FILTER (WHERE okres = 2), count(*), 25 * count(*)
      FROM reg WHERE kod = 'RANKING10' OR Z2_kanal = 'afiliacja_ranking'
      UNION ALL
      SELECT 'jakiekolwiek wejscie z rankingu przed zakupem', count(*) FILTER (WHERE okres = 1),
             count(*) FILTER (WHERE okres = 2), count(*), 25 * count(*)
      FROM reg WHERE user_id IN (SELECT user_id FROM sp WHERE kanal = 'afiliacja_ranking')""")
    tab("""
      WITH a AS (SELECT 25 * count(*) FILTER (WHERE regula = 'Z1K' AND kanal = 'afiliacja_ranking') z1k,
                        25 * count(*) FILTER (WHERE regula = 'Z1' AND kanal = 'afiliacja_ranking') z1,
                        25 * count(*) FILTER (WHERE regula = 'Z2' AND kanal = 'afiliacja_ranking') z2,
                        25 * count(*) FILTER (WHERE regula = 'Z1' AND kod = 'RANKING10') ranking10 FROM zr),
           p AS (SELECT sum(amount_paid - refund_amount) netto FROM zam)
      SELECT z1k - ranking10 roznica_Z1K_minus_RANKING10_zl, z1 - ranking10 roznica_Z1_minus_RANKING10_zl,
             z2 - ranking10 roznica_Z2_minus_RANKING10_zl,
             round(100 * (z1k - ranking10) / netto, 2) roznica_Z1K_proc_przychodu_po_zwrotach_dwa_lata
      FROM a, p""")

    r("\n4f. Program poleceń: pacjenci z wejściem na /polecenie przed zakupem i ilu z nich reguła przypisuje do poleceń")
    tab(f"""
      SELECT z.regula, count(*) pacjenci_z_wejsciem_na_polecenie,
             count(*) FILTER (WHERE z.kanal = 'program_polecen') przypisani_do_polecen
      FROM zr z JOIN reg r USING (user_id) WHERE r.bylo_wejscie_polecenie = 1 AND z.regula IN ('Z1', 'Z2', 'Z3')
      GROUP BY 1 ORDER BY 1""")

    r("\n4g. Powrót (R1) w 90 dniach według kanału, zależnie od reguły źródła, % kohort z pełnym oknem")
    s = df(f"""
      SELECT z.regula, z.kanal, round(100.0 * count(*) FILTER (WHERE p.dni_R1 <= 90) / count(*), 1) powrot90
      FROM zr z JOIN powr p ON p.user_id = z.user_id AND p.war = 'N1'
      WHERE p.d0 <= DATE '{KONIEC}' - 90 GROUP BY ALL""")
    pokaz(s.pivot(index="kanal", columns="regula", values="powrot90")[kolejnosc].reset_index())

    r("\n4h. Struktura źródeł w okresie 1 i okresie 2 dla trzech reguł podstawowych, % pacjentów okresu")
    s = df("SELECT regula, okres, kanal, count(*) n FROM zr WHERE regula IN ('Z1', 'Z2', 'Z3') GROUP BY ALL")
    s["proc"] = (100 * s.n / s.groupby(["regula", "okres"]).n.transform("sum")).round(1)
    s["kol"] = s.regula + "_o" + s.okres.astype(str)
    pokaz(s.pivot(index="kanal", columns="kol", values="proc").fillna(0).sort_values("Z2_o2", ascending=False).reset_index())

    kamp = df("SELECT regula, kampania, okres, count(*) pacjenci FROM zr GROUP BY ALL ORDER BY 1, 2, 3")
    kamp.to_csv(WYNIK_KAMPANIE, index=False, encoding="utf-8")

    # ============ 5. OKNO PO NEWSLETTERZE I SMS-IE ============
    r("\n" + "=" * 100)
    r("5. OKNO POWROTU PO WEJŚCIU Z NEWSLETTERA ALBO SMS-A")
    r("=" * 100)
    r("   Kontakt = sesja z kampanii CRM, przypisana do pacjenta (konto albo jego przeglądarka). Wysyłek bez")
    r("   kliknięcia w danych nie widać. Zamówienia liczymy na pacjenta, w dowolnej sesji, od chwili wejścia;")
    r("   tylko zamówienia nieanulowane, jak przy powrocie (ZALOZENIA.md punkt 19), chyba że opis mówi inaczej.")
    r("   Dzień 0 = pierwsze 24 godziny od wejścia; odstępy liczone w UTC (zmiana czasu nie przesuwa doby).")
    r("   Tylko wejścia z pełnymi 61 dniami obserwacji (wejście + 61 dni <= koniec danych, czyli do 31.07.2026).")
    con.execute("""
      CREATE TEMP TABLE logow AS SELECT DISTINCT session_id FROM czyste.events WHERE event_name = 'account_completed'""")
    # zalogowana od wejścia: z wyjątkiem zakupu samego TelemediGO (ZALOZENIA.md punkt 10)
    con.execute("""
      CREATE TEMP TABLE kontakt AS
      SELECT s.pacjent, s.session_id, s.started_at_pl ts, timezone('UTC', s.started_at_utc) ts_utc, s.kampania, s.kanal,
             EXISTS (SELECT 1 FROM zam z WHERE z.user_id = s.pacjent AND z.created_at < s.started_at_pl) byl_pacjentem,
             s.user_id IS NOT NULL AND s.session_id NOT IN (SELECT session_id FROM logow)
               AND s.session_id NOT IN (SELECT session_id FROM czyste.go_memberships WHERE order_id IS NULL) zalogowana
      FROM ses_pac s
      WHERE timezone('UTC', s.started_at_utc) + INTERVAL 61 DAY <= timezone('Europe/Warsaw', TIMESTAMP '2026-10-01 00:00:00')""")
    con.execute("""
      CREATE TEMP TABLE po_kontakcie_wszystkie AS
      SELECT k.session_id, k.kampania, k.kanal, k.byl_pacjentem, k.zalogowana, k.ts_utc, o.order_id, o.status,
             o.session_id = k.session_id w_sesji,
             floor((epoch(timezone('Europe/Warsaw', o.created_at)) - epoch(k.ts_utc)) / 86400)::INT dzien
      FROM kontakt k JOIN zam o ON o.user_id = k.pacjent AND timezone('Europe/Warsaw', o.created_at) >= k.ts_utc
                                AND timezone('Europe/Warsaw', o.created_at) < k.ts_utc + INTERVAL 61 DAY""")
    con.execute("CREATE TEMP TABLE po_kontakcie AS SELECT * FROM po_kontakcie_wszystkie WHERE status <> 'cancelled'")
    r("\n5a. Wejścia z CRM według kampanii")
    tab("""
      SELECT kampania, count(*) wejscia, count(*) FILTER (WHERE byl_pacjentem) wejscia_pacjentow_po_zakupie,
             count(*) FILTER (WHERE NOT byl_pacjentem) wejscia_przed_pierwszym_zakupem
      FROM kontakt WHERE kanal = 'crm' GROUP BY 1 ORDER BY 2 DESC""")

    def profil(warunek_k, etykieta):
        return f"""
          WITH k AS (SELECT * FROM kontakt WHERE {warunek_k}),
               p AS (SELECT * FROM po_kontakcie WHERE {warunek_k}),
               n AS (SELECT count(*) n FROM k)
          SELECT '{etykieta}' grupa, (SELECT n FROM n) wejscia,
                 round(1000.0 * count(*) FILTER (WHERE w_sesji) / (SELECT n FROM n), 1) w_tej_sesji,
                 round(1000.0 * count(*) FILTER (WHERE dzien = 0 AND NOT w_sesji) / (SELECT n FROM n), 1) d0_poza_sesja,
                 round(1000.0 * count(*) FILTER (WHERE dzien = 1) / (SELECT n FROM n), 1) d1,
                 round(1000.0 * count(*) FILTER (WHERE dzien = 2) / (SELECT n FROM n), 1) d2,
                 round(1000.0 * count(*) FILTER (WHERE dzien = 3) / (SELECT n FROM n), 1) d3,
                 round(1000.0 * count(*) FILTER (WHERE dzien BETWEEN 4 AND 7) / 4 / (SELECT n FROM n), 1) d4_7,
                 round(1000.0 * count(*) FILTER (WHERE dzien BETWEEN 8 AND 14) / 7 / (SELECT n FROM n), 1) d8_14,
                 round(1000.0 * count(*) FILTER (WHERE dzien BETWEEN 15 AND 30) / 16 / (SELECT n FROM n), 1) d15_30,
                 round(1000.0 * count(*) FILTER (WHERE dzien BETWEEN 31 AND 60) / 30 / (SELECT n FROM n), 1) d31_60_tlo
          FROM p"""

    r("\n5b. Zamówienia na 1000 wejść na dzień, według dnia od wejścia (pacjenci po pierwszym zakupie)")
    r("     d4_7, d8_14, d15_30 i d31_60_tlo to średnia na jeden dzień w przedziale; d31_60 traktujemy jako tło.")
    czesci = [profil(f"kanal = 'crm' AND byl_pacjentem AND kampania = '{c}'", c)
              for c in ("crm_reactivation", "crm_recepta_przypomnienie", "crm_sms_przypomnienie", "crm_go_upsell")]
    czesci.append(profil("kanal = 'crm' AND byl_pacjentem", "CRM razem"))
    bez_go = "kanal = 'crm' AND byl_pacjentem AND kampania <> 'crm_go_upsell'"
    czesci.append(profil(f"{bez_go} AND zalogowana", "CRM bez go_upsell: zalogowana od wejscia"))
    czesci.append(profil(f"{bez_go} AND NOT zalogowana", "CRM bez go_upsell: pozostale"))
    czesci.append(profil("kanal <> 'crm' AND byl_pacjentem", "porownanie: inne wejscia pacjentow"))
    tab(" UNION ALL ".join(f"SELECT * FROM ({c})" for c in czesci))

    r("\n5c. Odsetek wejść z CRM (pacjenci po pierwszym zakupie), po których pacjent zamawia w ciągu N dni")
    tab("""
      WITH k AS (SELECT * FROM kontakt WHERE kanal = 'crm' AND byl_pacjentem),
           p AS (SELECT session_id, min(dzien) pierwszy FROM po_kontakcie WHERE kanal = 'crm' AND byl_pacjentem GROUP BY 1)
      SELECT k.kampania, count(*) wejscia,
             round(100.0 * count(*) FILTER (WHERE pierwszy = 0) / count(*), 1) do_1_dnia,
             round(100.0 * count(*) FILTER (WHERE pierwszy <= 2) / count(*), 1) do_3_dni,
             round(100.0 * count(*) FILTER (WHERE pierwszy <= 6) / count(*), 1) do_7_dni,
             round(100.0 * count(*) FILTER (WHERE pierwszy <= 13) / count(*), 1) do_14_dni,
             round(100.0 * count(*) FILTER (WHERE pierwszy <= 29) / count(*), 1) do_30_dni
      FROM k LEFT JOIN p USING (session_id) GROUP BY 1 ORDER BY 2 DESC""")

    r("\n5e. Okno przypisania zamówienia do wejścia z CRM: zamówienia na 1000 wejść i nadwyżka nad tłem")
    r("     (kampanie CRM bez crm_go_upsell, pacjenci po pierwszym zakupie; tło = średnia dzienna z dni 31-60")
    r("     po wejściu razy liczba dni okna; w tej samej sesji tła nie odejmujemy)")
    r("     Zalogowana od wejścia = konto w sesji i brak kroku logowania (ZALOZENIA.md, punkt 10).")
    rama = []
    for grupa, war_g in (("CRM bez go_upsell", "TRUE"), ("zalogowana od wejscia", "zalogowana"),
                         ("pozostale", "NOT zalogowana")):
        czesci = []
        for etykieta, dni in (("tylko ta sama sesja", None), ("do 24 godzin", 1), ("do 3 dni", 3),
                              ("do 7 dni", 7), ("do 14 dni", 14), ("do 30 dni", 30)):
            if dni is None:
                war, tlo = "w_sesji", "0"
            else:
                war, tlo = f"(w_sesji OR dzien < {dni})", f"{dni} * (SELECT tlo FROM t)"
            czesci.append(f"""
              SELECT '{grupa}' grupa, '{etykieta}' okno,
                     round(1000.0 * count(*) FILTER (WHERE {war}) / (SELECT n FROM n), 1) zamowienia_na_1000,
                     round({tlo}, 1) tlo_na_1000,
                     round(1000.0 * count(*) FILTER (WHERE {war}) / (SELECT n FROM n) - {tlo}, 1) nadwyzka_na_1000
              FROM p""")
        rama.append(df(f"""
          WITH k AS (SELECT * FROM kontakt WHERE {bez_go} AND {war_g}),
               p AS (SELECT * FROM po_kontakcie WHERE {bez_go} AND {war_g}),
               n AS (SELECT count(*) n FROM k),
               t AS (SELECT 1000.0 * count(*) FILTER (WHERE dzien BETWEEN 31 AND 60) / 30 / (SELECT n FROM n) tlo FROM p)
          {" UNION ALL ".join(czesci)}"""))
    pokaz(pd.concat(rama))

    r("\n5d. crm_go_upsell: zakupy TelemediGO na 1000 wejść, według dnia od wejścia")
    tab(f"""
      WITH k AS (SELECT * FROM kontakt WHERE kampania = 'crm_go_upsell'),
           g AS (SELECT floor((epoch(timezone('Europe/Warsaw', g.purchased_at)) - epoch(k.ts_utc)) / 86400)::INT dzien,
                        g.session_id = k.session_id w_sesji
                 FROM k JOIN czyste.go_memberships g ON g.user_id = k.pacjent
                   AND timezone('Europe/Warsaw', g.purchased_at) >= k.ts_utc
                   AND timezone('Europe/Warsaw', g.purchased_at) < k.ts_utc + INTERVAL 61 DAY)
      SELECT (SELECT count(*) FROM k) wejscia,
             round(1000.0 * count(*) FILTER (WHERE w_sesji) / (SELECT count(*) FROM k), 1) w_tej_sesji,
             round(1000.0 * count(*) FILTER (WHERE dzien = 0 AND NOT w_sesji) / (SELECT count(*) FROM k), 1) d0_poza_sesja,
             round(1000.0 * count(*) FILTER (WHERE dzien BETWEEN 1 AND 3) / 3 / (SELECT count(*) FROM k), 1) d1_3,
             round(1000.0 * count(*) FILTER (WHERE dzien BETWEEN 4 AND 7) / 4 / (SELECT count(*) FROM k), 1) d4_7,
             round(1000.0 * count(*) FILTER (WHERE dzien BETWEEN 8 AND 30) / 23 / (SELECT count(*) FROM k), 1) d8_30,
             round(1000.0 * count(*) FILTER (WHERE dzien BETWEEN 31 AND 60) / 30 / (SELECT count(*) FROM k), 1) d31_60_tlo
      FROM g""")

    # ============ 6. PRZYJĘTE DEFINICJE ============
    r("\n" + "=" * 100)
    r("6. PRZYJĘTE DEFINICJE (Kuba, 2026-10-19) — LICZBY ODNIESIENIA DLA A5")
    r("=" * 100)
    r("   Nowy pacjent = N1 (status pierwszego zamówienia jako podział). Powrót = R2 w oknach 30/60/90 dni.")
    r("   TelemediGO mierzone osobno, nie jako powrót. Przychód z konsultacji po zwrotach, TelemediGO osobno.")
    r("   Źródło = Z1K (pierwsze wejście z anonimowymi sesjami przeglądarek pacjenta; kod kampanii rozstrzyga).")
    r("   Prowizja afiliacyjna = reguła Z1K. Okno CRM = 24 godziny od wejścia, na pacjenta, w dowolnej sesji,")
    r("   tylko zamówienia nieanulowane; przy przypisaniu sprzedaży zamówienie idzie do ostatniego wejścia z CRM.")
    r("   Okresy porównujemy na tych samych dniach kalendarzowych (punkt 27). Zmiany po recenzji Codeksa (Sol).")
    r("\n6a. Nowi pacjenci według statusu pierwszego zamówienia i powrót R2 w 90 dniach (okres 2: kohorty do 2.07.2026)")
    tab(f"""
      SELECT z.status status_pierwszego, count(*) FILTER (WHERE p.okres = 1) nowi_o1, count(*) FILTER (WHERE p.okres = 2) nowi_o2,
             round(100.0 * count(*) FILTER (WHERE p.okres = 1 AND p.dni_R2 <= 90) / count(*) FILTER (WHERE p.okres = 1), 1) powrot90_o1,
             round(100.0 * count(*) FILTER (WHERE p.okres = 2 AND p.d0 <= DATE '{KONIEC}' - 90 AND p.dni_R2 <= 90)
                   / count(*) FILTER (WHERE p.okres = 2 AND p.d0 <= DATE '{KONIEC}' - 90), 1) powrot90_o2
      FROM powr p JOIN zam z ON z.user_id = p.user_id AND z.nr = 1 WHERE p.war = 'N1'
      GROUP BY 1 ORDER BY 2 DESC""")
    r("\n6b. Powrót R2 w 30/60/90 dniach, wszyscy nowi pacjenci, % kohorty")
    tab(stopy("N1", "R2"))
    r("     Porównywalne dni kalendarzowe (recenzja Codeksa): w okresie 1 tylko kohorty do tego samego dnia roku,")
    r("     co ostatnia dojrzała kohorta okresu 2 (30 dni: 31.08, 60 dni: 1.08, 90 dni: 2.07); n = liczba pacjentów")
    tab(stopy_por("N1", "R2"))
    for regula, opis in (("Z1K", "reguła przyjęta"), ("Z2", "sesja płatności, pokazywana obok przy ekonomii kampanii")):
        r(f"\n6c. Nowi pacjenci według kanału ({regula}: {opis}) i powrót R2 w 90 dniach")
        tab(f"""
          SELECT z.kanal, count(*) FILTER (WHERE z.okres = 1) nowi_o1, count(*) FILTER (WHERE z.okres = 2) nowi_o2,
                 round(100.0 * count(*) FILTER (WHERE z.okres = 1) / sum(count(*) FILTER (WHERE z.okres = 1)) OVER (), 1) udzial_o1,
                 round(100.0 * count(*) FILTER (WHERE z.okres = 2) / sum(count(*) FILTER (WHERE z.okres = 2)) OVER (), 1) udzial_o2,
                 round(100.0 * count(*) FILTER (WHERE p.okres = 1 AND p.dni_R2 <= 90) / count(*) FILTER (WHERE p.okres = 1), 1) powrot90_o1,
                 round(100.0 * count(*) FILTER (WHERE p.okres = 2 AND p.d0 <= DATE '{KONIEC}' - 90 AND p.dni_R2 <= 90)
                       / nullif(count(*) FILTER (WHERE p.okres = 2 AND p.d0 <= DATE '{KONIEC}' - 90), 0), 1) powrot90_o2
          FROM zr z JOIN powr p ON p.user_id = z.user_id AND p.war = 'N1' WHERE z.regula = '{regula}'
          GROUP BY 1 ORDER BY 3 DESC""")
    r("\n6d. Prowizja afiliacyjna według reguły Z1K i według kodu RANKING10, zł")
    tab("""
      SELECT 'Z1K' wariant, 25 * count(*) FILTER (WHERE okres = 1) okres1_zl, 25 * count(*) FILTER (WHERE okres = 2) okres2_zl,
             25 * count(*) razem_zl FROM zr WHERE regula = 'Z1K' AND kanal = 'afiliacja_ranking'
      UNION ALL
      SELECT 'kod RANKING10', 25 * count(*) FILTER (WHERE okres = 1), 25 * count(*) FILTER (WHERE okres = 2), 25 * count(*)
      FROM reg WHERE kod = 'RANKING10'""")
    r("\n6e. Wejścia z CRM: zamówienia (i zakupy TelemediGO) pacjenta do 24 godzin od wejścia, na 1000 wejść")
    r("     (wejścia z pełnymi 61 dniami obserwacji, pacjenci po pierwszym zakupie)")
    r("     zamowienia_24h = nieanulowane, każde wejście osobno; z_anulowanymi = wszystkie płatności;")
    r("     rozlacznie = każde nieanulowane zamówienie przypisane tylko do ostatniego wejścia z CRM przed płatnością")
    tab("""
      WITH rozl AS (SELECT kampania, count(*) n FROM (
                      SELECT order_id, arg_max(kampania, ts_utc) kampania FROM po_kontakcie
                      WHERE kanal = 'crm' AND byl_pacjentem AND dzien = 0 GROUP BY 1) GROUP BY 1)
      SELECT k.kampania, count(DISTINCT k.session_id) wejscia,
             round(1000.0 * (SELECT count(*) FROM po_kontakcie p WHERE p.kampania = k.kampania AND p.byl_pacjentem AND p.dzien = 0)
                   / count(DISTINCT k.session_id), 1) zamowienia_24h_na_1000,
             round(1000.0 * (SELECT count(*) FROM po_kontakcie_wszystkie p WHERE p.kampania = k.kampania AND p.byl_pacjentem
                               AND p.dzien = 0) / count(DISTINCT k.session_id), 1) z_anulowanymi_na_1000,
             any_value(r.n) zamowienia_rozlacznie,
             round(1000.0 * any_value(r.n) / count(DISTINCT k.session_id), 1) rozlacznie_na_1000,
             round(1000.0 * (SELECT count(*) FROM kontakt k2 JOIN czyste.go_memberships g ON g.user_id = k2.pacjent
                               AND timezone('Europe/Warsaw', g.purchased_at) >= k2.ts_utc
                               AND timezone('Europe/Warsaw', g.purchased_at) < k2.ts_utc + INTERVAL 1 DAY
                             WHERE k2.kampania = k.kampania AND k2.byl_pacjentem) / count(DISTINCT k.session_id), 1) go_24h_na_1000
      FROM kontakt k LEFT JOIN rozl r USING (kampania) WHERE k.kanal = 'crm' AND k.byl_pacjentem
      GROUP BY 1 ORDER BY 2 DESC""")

    # ============ 7. PRZYKŁADY PACJENTÓW (do recenzji kodu) ============
    przyklady(con)

    con.close()
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Raport zapisany: {os.path.relpath(WYNIK, KATALOG)} ({len(linie)} linii)")
    print(f"Kampanie: {os.path.relpath(WYNIK_KAMPANIE, KATALOG)}")
    print(f"Przykłady: {os.path.relpath(WYNIK_PRZYKLADY, KATALOG)}")


KRYTERIA = {
    "pierwsze zamówienie anulowane, później nieanulowane (N1 i N3 różnią się dniem)":
        "SELECT a.user_id FROM koh a JOIN koh b ON a.user_id = b.user_id AND b.war = 'N3' WHERE a.war = 'N1' AND a.d0 <> b.d0",
    "pierwsze zamówienie zwrócone po wizycie":
        "SELECT user_id FROM zam WHERE nr = 1 AND status = 'refunded'",
    "anonimowa sesja przed zakupem, pierwsze wejście inne niż sesja płatności":
        "SELECT user_id FROM reg WHERE sesje_anonimowe > 0 AND Z1_kanal <> Z2_kanal",
    "kod L4SZYBKO20, pierwsze wejście nie z kampanii kodu (kod rozstrzyga)":
        "SELECT user_id FROM reg WHERE kod = 'L4SZYBKO20' AND Z1_kampania <> 'meta_prosp_l4_szybko'",
    "drugie zamówienie anulowane, powrót R2 później niż R1":
        "SELECT user_id FROM powr WHERE war = 'N1' AND dni_R2 > dni_R1",
    "wejście z CRM i zamówienie do 24 godzin w innej sesji":
        "SELECT k.pacjent FROM kontakt k JOIN po_kontakcie p USING (session_id) WHERE k.kanal = 'crm' AND p.dzien = 0 AND NOT p.w_sesji",
    "kilka przeglądarek, pierwsze wejście z anonimowej sesji":
        """SELECT r.user_id FROM reg r WHERE r.sesje_anonimowe > 0
             AND r.user_id IN (SELECT user_id FROM przeg GROUP BY 1 HAVING count(*) > 1)""",
    "ranking lekarzy jako pierwsze wejście, płatność w innej sesji (prowizja wg Z1K)":
        "SELECT user_id FROM reg WHERE Z1_kanal = 'afiliacja_ranking' AND Z2_kanal <> 'afiliacja_ranking'",
}


def przyklady(con):
    """Po jednym pacjencie (najmniejszy identyfikator) na kryterium: surowe wiersze i to, co policzył kod."""
    linie = [f"A4 — PRZYKŁADY PACJENTÓW DO RĘCZNEJ KONTROLI KODU ({dt.datetime.now():%Y-%m-%d %H:%M})",
             "Surowe wiersze ze schematu `czyste` i wartości wyliczone przez analiza/a4_definicje.py.",
             "Sesje: wszystkie sesje pacjenta (konto albo jego przeglądarka) do dnia ostatniego zamówienia + 1."]

    def pokaz(tytul, sql):
        linie.append(f"\n  {tytul}")
        d = con.sql(sql).df()
        linie.extend("    " + l for l in (d.to_string(index=False) if len(d) else "(brak)").splitlines())

    for opis, sql in KRYTERIA.items():
        uid = con.sql(f"SELECT min(user_id) FROM ({sql}) t(user_id)").fetchone()[0]
        linie.append("\n" + "=" * 100)
        linie.append(f"KRYTERIUM: {opis}")
        linie.append(f"PACJENT user_id = {uid}")
        if uid is None:
            continue
        pokaz("konto", f"SELECT * FROM czyste.users WHERE user_id = {uid}")
        pokaz("zamówienia", f"""SELECT nr, order_id, created_at, status, promo_code, session_id, list_price, amount_paid,
                                       refund_amount, specialization, visit_purpose FROM zam WHERE user_id = {uid} ORDER BY nr""")
        pokaz("TelemediGO", f"SELECT * FROM czyste.go_memberships WHERE user_id = {uid} ORDER BY purchased_at")
        pokaz("sesje", f"""
          SELECT s.session_id, s.started_at_pl, s.visitor_id, s.user_id konto_w_sesji, s.utm_source, s.utm_medium,
                 s.utm_campaign, s.landing_page, s.kanal,
                 (SELECT string_agg(event_name, ',' ORDER BY event_at_utc) FROM czyste.events e WHERE e.session_id = s.session_id) kroki
          FROM ses_pac s WHERE s.pacjent = {uid}
            AND s.started_at_pl <= (SELECT max(created_at) FROM zam WHERE user_id = {uid}) + INTERVAL 1 DAY
          ORDER BY s.started_at_pl""")
        pokaz("wyliczone: wejście do kohorty w wariantach N1-N4", f"SELECT war, t0, d0, okres, session_id FROM koh WHERE user_id = {uid} ORDER BY war")
        pokaz("wyliczone: dni do powrotu (N1) w wariantach R1-R4", f"SELECT dni_R1, dni_R2, dni_R3, dni_R4 FROM powr WHERE war = 'N1' AND user_id = {uid}")
        pokaz("wyliczone: źródło według reguł", f"""
          SELECT regula, kanal, kampania FROM zr WHERE user_id = {uid}
          ORDER BY list_position(['Z1', 'Z1b', 'Z2', 'Z3', 'Z3_7', 'Z3_90', 'Z1K', 'Z2K', 'Z3K'], regula)""")
        pokaz("wyliczone: wejścia z CRM i zamówienia do 24 godzin", f"""
          SELECT k.session_id, k.ts, k.kampania, k.zalogowana, k.byl_pacjentem,
                 count(p.dzien) FILTER (WHERE p.dzien = 0) zamowienia_24h,
                 count(p.dzien) FILTER (WHERE p.dzien = 0 AND p.w_sesji) w_tej_sesji
          FROM kontakt k LEFT JOIN po_kontakcie p USING (session_id)
          WHERE k.pacjent = {uid} AND k.kanal = 'crm' GROUP BY ALL ORDER BY k.ts""")

    with open(WYNIK_PRZYKLADY, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")


if __name__ == "__main__":
    main()
