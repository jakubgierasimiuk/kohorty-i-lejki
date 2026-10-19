"""A5 (pozyskanie) — zdarzenia w lejku: dni, od których zmienia się konwersja kroku (2026-10-19).

Wejście: analiza/wyniki/a5p_lejek_dzienny.csv.gz (z analiza/a5p_lejek.py), sesje zwykłe osób, które jeszcze
nie kupowały. Sesje pacjentów powracających płacą w około 90% przypadków, a ich liczba rośnie od zera przez
pierwszy rok; w całości ruchu daje to pozorny stopniowy wzrost konwersji (a5p_lejek.txt, sekcja 3, pacjent).

Metoda (dla każdej serii dziennej: podział × wartość × przejście między krokami):
  1. Seria: x_t = sesje z krokiem, n_t = sesje z krokiem poprzednim, dzień po dniu (czas polski),
     od pierwszego do ostatniego dnia, w którym grupa ma ruch.
  2. Rozrzut ponad losowość (dzień tygodnia, szum): φ = średni kwadrat reszt Pearsona wobec średniej
     kroczącej z 29 dni; co najmniej 1. Statystyki dzielimy przez φ (quasi-wiarygodność).
  3. Podział binarny: w odcinku szukamy dnia, który najbardziej poprawia wiarygodność dwumianową
     przy podziale na dwa poziomy. Przyjmujemy go, jeśli 2·zysk/φ > KARA i oba odcinki mają co najmniej
     MIN_DNI dni; potem powtarzamy w każdym kawałku (najwyżej MAX_ZMIAN zmian na serię).
  4. Zmiana trafia do listy, jeśli poziom różni się co najmniej o MIN_PP punktu procentowego
     i o MIN_WZGL procent względnie.
  5. Wpływ na zamówienia: (poziom po − poziom przed) × sesje wchodzące na krok w odcinku po zmianie
     × dalsza konwersja do płatności w tym odcinku. Liczone w zamówieniach na 30 dni i razem do końca odcinka.
     To przybliżenie „co by było, gdyby poziom się nie zmienił”, nie dowód przyczyny.
To samo robimy dla liczby sesji dziennie (rozkład Poissona), żeby znaleźć starty i końce ruchu.

Sekcja 5 sprawdza wybrane zdarzenia wprost na bazie (tylko odczyt): czy zmiana jest w każdym kanale,
czy to zmiana struktury ruchu, co dokładnie się psuje i ile zamówień to kosztuje.

Uruchomienie z głównego folderu projektu (po analiza/a5p_lejek.py):
    python -I analiza/a5p_zdarzenia.py
Wynik: analiza/wyniki/a5p_zdarzenia.txt, analiza/wyniki/a5p_zdarzenia.csv
"""

import datetime as dt
import os
import sys

import duckdb
import numpy as np
import pandas as pd

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAZA = os.path.join(KATALOG, "analiza", "telemedi.duckdb")
WEJSCIE = os.path.join(KATALOG, "analiza", "wyniki", "a5p_lejek_dzienny.csv.gz")
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "a5p_zdarzenia.txt")
WYNIK_CSV = os.path.join(KATALOG, "analiza", "wyniki", "a5p_zdarzenia.csv")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_rows", 500)

PRZEJSCIA = [("k1", "sesje", "usluga"), ("k2", "k1", "termin"), ("k3", "k2", "logowanie"),
             ("k4", "k3", "wejscie_platn"), ("k5", "k4", "platnosc"), ("k5", "sesje", "sesja_do_platn")]
PODZIALY = ["calosc", "urzadzenie", "przegladarka", "urzadzenie_przegladarka", "system_przegladarka", "kanal", "kampania",
            "strona_wejscia"]
MIN_DNI = 14        # najkrótszy odcinek
MAX_ZMIAN = 6       # najwięcej zmian na serię
KARA = 25.0         # próg 2·zysk/φ (chi-kwadrat z 1 stopniem swobody: p około 6e-7)
MIN_PP = 1.0        # najmniejsza zmiana poziomu konwersji, punkty procentowe
MIN_WZGL = 5.0      # najmniejsza zmiana względna, %
MIN_MIANOWNIK = 3000  # najmniej sesji wchodzących na krok w całej serii
MIN_WZGL_RUCH = 25.0  # najmniejsza zmiana względna liczby sesji dziennie, %


def ll_dwumian(x, n):
    """Log-wiarygodność dwumianowa odcinków przy jednym poziomie (bez stałej); x, n mogą być tablicami."""
    x, n = np.asarray(x, float), np.asarray(n, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        p = np.where(n > 0, x / np.where(n > 0, n, 1), 0.0)
        a = np.where(x > 0, x * np.log(np.where(p > 0, p, 1)), 0.0)
        b = np.where(n - x > 0, (n - x) * np.log(np.where(p < 1, 1 - p, 1)), 0.0)
    return a + b


def ll_poisson(x, n):
    """Log-wiarygodność Poissona odcinków: x zdarzeń w n dniach, jeden poziom (bez stałej)."""
    x, n = np.asarray(x, float), np.asarray(n, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(x > 0, x * np.log(np.where(x > 0, x / n, 1)) - x, 0.0)


def segmentuj(x, n, ll, phi):
    """Podział binarny. x, n: tablice dzienne. Zwraca posortowaną listę indeksów początku nowych odcinków."""
    cx, cn = np.concatenate([[0], np.cumsum(x)]), np.concatenate([[0], np.cumsum(n)])
    zmiany = []
    kolejka = [(0, len(x))]
    while kolejka and len(zmiany) < MAX_ZMIAN:
        najlepszy = None
        for a, b in kolejka:
            if b - a < 2 * MIN_DNI:
                continue
            t = np.arange(a + MIN_DNI, b - MIN_DNI + 1)
            zysk = (ll(cx[t] - cx[a], cn[t] - cn[a]) + ll(cx[b] - cx[t], cn[b] - cn[t])
                    - ll(cx[b] - cx[a], cn[b] - cn[a]))
            i = int(np.argmax(zysk))
            stat = 2 * float(zysk[i]) / phi
            if najlepszy is None or stat > najlepszy[0]:
                najlepszy = (stat, int(t[i]), a, b)
        if najlepszy is None or najlepszy[0] < KARA:
            break
        stat, t, a, b = najlepszy
        zmiany.append(t)
        kolejka.remove((a, b))
        kolejka += [(a, t), (t, b)]
    return sorted(zmiany)


def rozrzut(x, n, dwumian=True):
    """φ: średni kwadrat reszt Pearsona wobec średniej kroczącej z 29 dni (co najmniej 1)."""
    sx = pd.Series(x).rolling(29, center=True, min_periods=8).sum().to_numpy()
    sn = pd.Series(n).rolling(29, center=True, min_periods=8).sum().to_numpy()
    if dwumian:
        p = sx / np.where(sn > 0, sn, np.nan)
        war = n * p * (1 - p)
        ok = (n > 0) & (war > 0)
        res = (x[ok] - n[ok] * p[ok]) ** 2 / war[ok]
    else:
        m = sx / np.where(sn > 0, sn, np.nan)
        ok = m > 0
        res = (x[ok] - m[ok]) ** 2 / m[ok]
    return max(1.0, float(np.nanmean(res))) if len(res) else 1.0


def weryfikacja(r, pokaz):
    """Sekcja 5: sprawdzenie wybranych zdarzeń wprost na bazie."""
    con = duckdb.connect(BAZA, read_only=True)

    def df(sql):
        return con.sql(sql).df()

    con.execute("""
      CREATE TEMP TABLE ev AS
      SELECT session_id,
             max((event_name = 'service_selected')::INT) k1, max((event_name = 'slot_selected')::INT) k2,
             max((event_name = 'account_completed')::INT) k3, max((event_name = 'payment_started')::INT) k4,
             max((event_name = 'payment_succeeded')::INT) k5,
             min(event_at_utc) FILTER (WHERE event_name = 'slot_selected') t2,
             min(event_at_utc) FILTER (WHERE event_name = 'account_completed') t3
      FROM czyste.events GROUP BY 1""")
    con.execute("CREATE TEMP TABLE przeg AS SELECT DISTINCT visitor_id, user_id FROM czyste.sessions WHERE user_id IS NOT NULL")
    con.execute("CREATE TEMP TABLE pierwszy AS SELECT user_id, min(created_at) t FROM czyste.orders GROUP BY 1")
    # sesje zwykłe (bez zalogowanych od wejścia i bez zakupu samego TelemediGO), z oznaczeniem nowego odwiedzającego
    con.execute("""
      CREATE TEMP TABLE sz AS
      SELECT s.*, coalesce(e.k1, 0) k1, coalesce(e.k2, 0) k2, coalesce(e.k3, 0) k3, coalesce(e.k4, 0) k4,
             coalesce(e.k5, 0) k5, e.t2, e.t3,
             CASE WHEN s.utm_source IS NULL THEN 'bezposrednie' WHEN s.utm_campaign = 'gs_brand' THEN 'google_ads_marka'
                  WHEN s.utm_campaign LIKE 'gs_generic%' THEN 'google_ads_ogolne'
                  WHEN s.utm_medium = 'organic' THEN 'wyszukiwarka_bezplatna'
                  WHEN s.utm_campaign LIKE 'meta_prosp%' THEN 'meta_pozyskanie'
                  WHEN s.utm_campaign = 'meta_rmkt_koszyk' THEN 'meta_remarketing'
                  WHEN s.utm_source = 'tiktok' THEN 'tiktok' ELSE 'pozostale' END kanal,
             CASE WHEN s.os = 'iOS' AND s.browser = 'Safari' THEN 'iOS Safari'
                  WHEN s.os = 'iOS' THEN 'iOS inne przegladarki'
                  WHEN s.os = 'macOS' AND s.browser = 'Safari' THEN 'macOS Safari' ELSE 'pozostale' END grupa,
             coalesce(pz.t < s.started_at_pl, FALSE) kupowal_wczesniej,
             u.registered_at
      FROM czyste.sessions s
      LEFT JOIN ev e USING (session_id)
      LEFT JOIN przeg p ON p.visitor_id = s.visitor_id AND s.user_id IS NULL
      LEFT JOIN pierwszy pz ON pz.user_id = coalesce(s.user_id, p.user_id)
      LEFT JOIN czyste.users u ON u.user_id = s.user_id
      WHERE NOT (s.user_id IS NOT NULL AND coalesce(e.k3, 0) = 0)
        AND s.session_id NOT IN (SELECT session_id FROM czyste.go_memberships WHERE order_id IS NULL)""")

    r("\n" + "=" * 100)
    r("5. SPRAWDZENIE WYBRANYCH ZDARZEŃ NA BAZIE")
    r("=" * 100)
    przed, po60, po = ("'2026-01-16' AND '2026-03-16'", "'2026-03-17' AND '2026-05-15'", "'2026-03-17' AND '2026-09-30'")

    def stopa(licz, mian, okno, warunek="TRUE"):
        return (f"round(100 * sum({licz}) FILTER (WHERE dzien_pl BETWEEN {okno} AND {warunek})"
                f" / sum({mian}) FILTER (WHERE dzien_pl BETWEEN {okno} AND {warunek}), 1)")

    r("\n5a. Logowanie albo założenie konta (k3 / k2) w Safari na iOS wobec innych przeglądarek, osoby, które jeszcze")
    r("    nie kupowały. Okna: 60 dni przed 17.03.2026 (16.01–16.03), 60 dni po (17.03–15.05) i całe po (17.03–30.09).")
    pokaz(df(f"""
      SELECT grupa, sum(k2) FILTER (WHERE dzien_pl BETWEEN {przed}) z_terminem_przed,
             {stopa('k3', 'k2', przed)} przed, {stopa('k3', 'k2', po60)} po_60_dni, {stopa('k3', 'k2', po)} po_do_30_09
      FROM sz WHERE NOT kupowal_wczesniej GROUP BY 1 ORDER BY 1"""))
    r("\n5b. To samo w Safari na iOS według kanału (czy spadek jest w każdym kanale, czy to zmiana struktury ruchu)")
    pokaz(df(f"""
      SELECT kanal, sum(k2) FILTER (WHERE dzien_pl BETWEEN {przed}) z_terminem_przed, {stopa('k3', 'k2', przed)} przed,
             sum(k2) FILTER (WHERE dzien_pl BETWEEN {po60}) z_terminem_po_60_dni, {stopa('k3', 'k2', po60)} po_60_dni
      FROM sz WHERE NOT kupowal_wczesniej AND grupa = 'iOS Safari' GROUP BY 1 ORDER BY 2 DESC"""))
    r("\n5c. Dzień po dniu wokół 17.03.2026: k3 / k2 w Safari na iOS i w pozostałych (osoby, które jeszcze nie kupowały)")
    pokaz(df("""
      SELECT dzien_pl, dayname(dzien_pl) dzien_tyg, sum(k2) FILTER (WHERE grupa = 'iOS Safari') z_terminem_ios_safari,
             round(100 * sum(k3) FILTER (WHERE grupa = 'iOS Safari') / sum(k2) FILTER (WHERE grupa = 'iOS Safari'), 1) ios_safari,
             round(100 * sum(k3) FILTER (WHERE grupa <> 'iOS Safari') / sum(k2) FILTER (WHERE grupa <> 'iOS Safari'), 1) pozostale
      FROM sz WHERE NOT kupowal_wczesniej AND dzien_pl BETWEEN '2026-03-10' AND '2026-03-24' GROUP BY 1, 2 ORDER BY 1"""))
    r("\n5d. Co się psuje: założenie nowego konta czy logowanie do istniejącego. Krok 3 w sesjach zwykłych (także")
    r("    pacjentów powracających); założenie konta w sesji = rejestracja konta między początkiem sesji a krokiem 3")
    r("    (z zapasem 1 minuty). Okna jak w 5a.")
    pokaz(df(f"""
      WITH k AS (SELECT *, registered_at BETWEEN started_at_pl - INTERVAL 1 MINUTE
                                         AND timezone('Europe/Warsaw', timezone('UTC', t3)) + INTERVAL 1 MINUTE rejestracja
                 FROM sz WHERE k3 = 1)
      SELECT grupa = 'iOS Safari' ios_safari,
             count(*) FILTER (WHERE rejestracja AND dzien_pl BETWEEN {przed}) zalozenia_konta_przed,
             count(*) FILTER (WHERE rejestracja AND dzien_pl BETWEEN {po60}) zalozenia_konta_po_60_dni,
             count(*) FILTER (WHERE NOT rejestracja AND dzien_pl BETWEEN {przed}) logowania_przed,
             count(*) FILTER (WHERE NOT rejestracja AND dzien_pl BETWEEN {po60}) logowania_po_60_dni,
             count(*) FILTER (WHERE kupowal_wczesniej AND dzien_pl BETWEEN {przed}) w_tym_powracajacy_przed,
             count(*) FILTER (WHERE kupowal_wczesniej AND dzien_pl BETWEEN {po60}) w_tym_powracajacy_po_60_dni
      FROM k GROUP BY 1 ORDER BY 1"""))
    r("\n5e. Czy odpadnięci na kroku 3 kupują później w tej samej przeglądarce (ten sam visitor_id), w ciągu 30 dni.")
    r("    Sesje osób, które jeszcze nie kupowały, z wyborem terminu i bez kroku 3. Po = 17.03–31.08.2026 (pełne 30 dni).")
    pokaz(df(f"""
      WITH o AS (SELECT sz.grupa, sz.dzien_pl,
                        EXISTS (SELECT 1 FROM czyste.sessions s2 JOIN czyste.orders z ON z.session_id = s2.session_id
                                WHERE s2.visitor_id = sz.visitor_id AND z.created_at > sz.started_at_pl
                                  AND z.created_at <= sz.started_at_pl + INTERVAL 30 DAY) kupil_pozniej
                 FROM sz WHERE NOT kupowal_wczesniej AND k2 = 1 AND k3 = 0 AND grupa IN ('iOS Safari', 'pozostale'))
      SELECT grupa, count(*) FILTER (WHERE dzien_pl BETWEEN {przed}) odpadli_przed,
             round(100 * avg(kupil_pozniej::INT) FILTER (WHERE dzien_pl BETWEEN {przed}), 1) proc_kupilo_pozniej_przed,
             count(*) FILTER (WHERE dzien_pl BETWEEN '2026-03-17' AND '2026-08-31') odpadli_po,
             round(100 * avg(kupil_pozniej::INT) FILTER (WHERE dzien_pl BETWEEN '2026-03-17' AND '2026-08-31'), 1) proc_kupilo_pozniej_po
      FROM o GROUP BY 1 ORDER BY 1"""))
    r("\n5f. Ile zamówień kosztuje zdarzenie w Safari na iOS: (k3/k2 przed − k3/k2 po) × sesje z wyborem terminu po")
    r("    × dalsza konwersja do płatności po (k5/k3). Przed = 1.10.2025–16.03.2026, po = 17.03–30.09.2026 (198 dni).")
    r("    Osobno osoby, które jeszcze nie kupowały (pierwsze zamówienia), i pacjenci powracający. Zakłada, że bez")
    r("    zdarzenia Safari na iOS trzymałoby poziom sprzed 17.03; nie odejmuje zakupów odłożonych na później (5e).")
    pokaz(df("""
      WITH a AS (SELECT CASE WHEN kupowal_wczesniej THEN 'powracajacy' ELSE 'nowi' END kto,
                        sum(k3) FILTER (WHERE dzien_pl BETWEEN '2025-10-01' AND '2026-03-16')
                          / sum(k2) FILTER (WHERE dzien_pl BETWEEN '2025-10-01' AND '2026-03-16') p0,
                        sum(k3) FILTER (WHERE dzien_pl >= '2026-03-17') / sum(k2) FILTER (WHERE dzien_pl >= '2026-03-17') p1,
                        sum(k2) FILTER (WHERE dzien_pl >= '2026-03-17') k2_po,
                        sum(k5) FILTER (WHERE dzien_pl >= '2026-03-17') / sum(k3) FILTER (WHERE dzien_pl >= '2026-03-17') dalej
                 FROM sz WHERE grupa = 'iOS Safari' GROUP BY 1)
      SELECT kto, round(100 * p0, 1) przed, round(100 * p1, 1) po, k2_po z_terminem_po, round(100 * dalej, 1) k5_do_k3_po,
             round((p0 - p1) * k2_po * dalej) utracone_zamowienia_198_dni,
             round((p0 - p1) * k2_po * dalej / 198 * 30, 1) na_30_dni
      FROM a ORDER BY 1"""))

    r("\n5g. Start kampanii Meta na L4 (meta_prosp_l4_szybko, od 3.11.2025): lejek dwóch kampanii Meta od tego dnia")
    r("    i lejek strony /zwolnienie-l4-online z ruchem z Meta i TikToka i bez niego (osoby, które jeszcze nie kupowały).")
    pokaz(df("""
      SELECT utm_campaign kampania, count(*) sesje, round(100 * avg(k1), 1) usluga, round(100 * sum(k2) / sum(k1), 1) termin,
             round(100 * sum(k3) / sum(k2), 1) logowanie, round(100 * sum(k5) / sum(k3), 1) k5_do_k3,
             round(100 * avg(k5), 2) sesja_do_platn
      FROM sz WHERE NOT kupowal_wczesniej AND utm_campaign LIKE 'meta_prosp%' AND dzien_pl >= '2025-11-03'
      GROUP BY 1 ORDER BY 1"""))
    pokaz(df("""
      SELECT CASE WHEN dzien_pl < '2025-11-03' THEN '1: 1.05-2.11.2025' WHEN dzien_pl < '2026-02-09' THEN '2: 3.11.2025-8.02.2026'
                  ELSE '3: od 9.02.2026' END okres,
             kanal IN ('meta_pozyskanie', 'tiktok') z_meta_lub_tiktok, count(*) sesje,
             round(100 * avg(k1), 1) usluga, round(100 * sum(k2) / sum(k1), 1) termin, round(100 * sum(k3) / sum(k2), 1) logowanie,
             round(100 * avg(k5), 2) sesja_do_platn
      FROM sz WHERE NOT kupowal_wczesniej AND landing_page = '/zwolnienie-l4-online' AND dzien_pl >= '2025-05-01'
      GROUP BY 1, 2 ORDER BY 1, 2"""))

    r("\n5h. Remarketing Meta (meta_rmkt_koszyk) w kwartałach, z Safari na iOS i bez (osoby, które jeszcze nie kupowały)")
    pokaz(df("""
      SELECT strftime(date_trunc('quarter', dzien_pl), '%Y-%m') kwartal_od, count(*) sesje,
             round(100 * avg(k1), 1) usluga, round(100 * sum(k3) / sum(k2), 1) logowanie, round(100 * avg(k5), 1) sesja_do_platn,
             round(100 * avg(k1) FILTER (WHERE grupa <> 'iOS Safari'), 1) usluga_bez_ios_safari,
             round(100 * sum(k3) FILTER (WHERE grupa <> 'iOS Safari') / sum(k2) FILTER (WHERE grupa <> 'iOS Safari'), 1)
               logowanie_bez_ios_safari,
             round(100 * avg(k5) FILTER (WHERE grupa <> 'iOS Safari'), 1) sesja_do_platn_bez_ios_safari,
             round(100 * avg((browser IN ('Instagram', 'Facebook'))::INT), 1) proc_w_aplikacji
      FROM sz WHERE NOT kupowal_wczesniej AND utm_campaign = 'meta_rmkt_koszyk' GROUP BY 1 ORDER BY 1"""))
    r("\n5i. Remarketing Meta według źródła pierwszej sesji tej samej przeglądarki (skąd pochodzą osoby, do których")
    r("    remarketing wraca). Pierwsza sesja = najwcześniejsza sesja tego samego visitor_id; jeśli to sama sesja")
    r("    remarketingu (nowe ciasteczko), źródło = remarketing. Osoby, które jeszcze nie kupowały.")
    pokaz(df("""
      WITH pierw AS (SELECT visitor_id, arg_min(CASE WHEN utm_source IS NULL THEN 'bezposrednie'
                                                     WHEN utm_campaign LIKE 'meta_prosp%' THEN 'meta_pozyskanie'
                                                     WHEN utm_campaign = 'meta_rmkt_koszyk' THEN 'remarketing'
                                                     WHEN utm_source = 'tiktok' THEN 'tiktok'
                                                     WHEN utm_source IN ('google', 'bing') THEN 'google_bing' ELSE 'pozostale' END,
                                                (started_at_utc, session_id)) zrodlo
                     FROM czyste.sessions GROUP BY 1)
      SELECT CASE WHEN dzien_pl < '2025-10-01' THEN '1: okres 1' WHEN dzien_pl < '2026-01-01' THEN '2: X-XII 2025'
                  ELSE '3: I-IX 2026' END okres,
             p.zrodlo, count(*) sesje, round(100 * avg(k1), 1) usluga, round(100 * avg(k5), 1) sesja_do_platn
      FROM sz JOIN pierw p USING (visitor_id)
      WHERE NOT kupowal_wczesniej AND utm_campaign = 'meta_rmkt_koszyk' GROUP BY 1, 2 ORDER BY 1, 3 DESC"""))
    con.close()


def main():
    sys.stdout.reconfigure(errors="replace")
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    dz = pd.read_csv(WEJSCIE, parse_dates=["dzien"])
    # sesje zwykłe osób, które jeszcze nie kupowały: lejek pozyskania bez efektu dorastania bazy powracających
    dz = dz[(dz["typ"] == "zwykla") & (dz["pacjent"] == "nie_kupowal")]
    dz = dz.groupby(["dzien", "podzial", "wartosc"], as_index=False)[["sesje", "k1", "k2", "k3", "k4", "k5"]].sum()
    dni = pd.date_range("2024-10-01", "2026-09-30", freq="D")

    wyniki = []
    for podzial in PODZIALY:
        czesc = dz[dz["podzial"] == podzial]
        for wartosc, g in czesc.groupby("wartosc"):
            g = g.set_index("dzien").reindex(dni, fill_value=0)
            aktywne = np.flatnonzero(g["sesje"].to_numpy() > 0)
            if len(aktywne) < 2 * MIN_DNI:
                continue
            g = g.iloc[aktywne[0]:aktywne[-1] + 1]
            daty = g.index
            # liczba sesji dziennie (Poisson): starty, końce i zmiany poziomu ruchu
            if podzial != "calosc":
                x = g["sesje"].to_numpy(float)
                n = np.ones(len(x))
                phi = rozrzut(x, n, dwumian=False)
                zm = segmentuj(x, n, ll_poisson, phi)
                granice = [0] + zm + [len(x)]
                for i, t in enumerate(zm):
                    przed = x[granice[i]:t].mean()
                    po = x[t:granice[i + 2]].mean()
                    wzgl = 100 * (po - przed) / przed if przed > 0 else np.inf
                    if abs(wzgl) >= MIN_WZGL_RUCH:
                        wyniki.append({"rodzaj": "ruch", "podzial": podzial, "wartosc": wartosc, "przejscie": "sesje_dziennie",
                                       "data": daty[t].date(), "przed": round(przed, 1), "po": round(po, 1),
                                       "zmiana": round(po - przed, 1), "zmiana_wzgl_proc": round(wzgl, 1),
                                       "dni_przed": t - granice[i], "dni_po": granice[i + 2] - t, "phi": round(phi, 2)})
            # konwersje kroków (dwumian)
            for licz, mian, nazwa in PRZEJSCIA:
                x, n = g[licz].to_numpy(float), g[mian].to_numpy(float)
                if n.sum() < MIN_MIANOWNIK:
                    continue
                phi = rozrzut(x, n)
                zm = segmentuj(x, n, ll_dwumian, phi)
                granice = [0] + zm + [len(x)]
                for i, t in enumerate(zm):
                    a, b = granice[i], granice[i + 2]
                    p0 = x[a:t].sum() / n[a:t].sum()
                    p1 = x[t:b].sum() / n[t:b].sum()
                    dpp = 100 * (p1 - p0)
                    wzgl = 100 * (p1 - p0) / p0 if p0 > 0 else np.inf
                    if abs(dpp) < MIN_PP or abs(wzgl) < MIN_WZGL:
                        continue
                    # wpływ na zamówienia w odcinku po zmianie
                    wej = n[t:b].sum()
                    dalej = (g["k5"].to_numpy(float)[t:b].sum() / x[t:b].sum()) if licz != "k5" and x[t:b].sum() > 0 else 1.0
                    wplyw = (p1 - p0) * wej * dalej
                    wyniki.append({"rodzaj": "konwersja", "podzial": podzial, "wartosc": wartosc, "przejscie": nazwa,
                                   "data": daty[t].date(), "przed": round(100 * p0, 1), "po": round(100 * p1, 1),
                                   "zmiana": round(dpp, 1), "zmiana_wzgl_proc": round(wzgl, 1),
                                   "dni_przed": t - a, "dni_po": b - t, "phi": round(phi, 2),
                                   "wejscia_po": int(wej), "zamowienia_razem": round(wplyw),
                                   "zamowienia_na_30_dni": round(wplyw / (b - t) * 30, 1)})
    wy = pd.DataFrame(wyniki)
    wy.to_csv(WYNIK_CSV, index=False, encoding="utf-8")

    r(f"A5 POZYSKANIE — ZDARZENIA W LEJKU ({dt.datetime.now():%Y-%m-%d %H:%M}), sesje zwykłe osób, które jeszcze nie kupowały")
    r(f"Metoda: podział binarny serii dziennych, kara {KARA}, odcinek co najmniej {MIN_DNI} dni, najwyżej {MAX_ZMIAN} zmian na serię;")
    r(f"konwersja: zmiana co najmniej {MIN_PP} punktu procentowego i {MIN_WZGL}% względnie; ruch: co najmniej {MIN_WZGL_RUCH}% względnie.")
    r("przed / po = poziom w sąsiednich odcinkach (konwersja w %, ruch w sesjach dziennie). Data = pierwszy dzień nowego poziomu.")
    r("Wpływ = (po − przed) × sesje wchodzące na krok po zmianie × dalsza konwersja do płatności; to przybliżenie, nie przyczyna.")
    r(f"Pełna lista: {os.path.relpath(WYNIK_CSV, KATALOG)} ({len(wy)} wierszy).")

    k = wy[wy["rodzaj"] == "konwersja"].copy()
    r("\n" + "=" * 100)
    r("1. ZMIANY KONWERSJI W CAŁYM LEJKU GŁÓWNYM")
    r("=" * 100)
    pokaz(k[k["podzial"] == "calosc"].sort_values(["przejscie", "data"]).drop(columns=["rodzaj", "podzial", "wartosc"]))

    r("\n" + "=" * 100)
    r("2. ZMIANY KONWERSJI W PODZIAŁACH (bez sesja_do_platn), według wielkości wpływu")
    r("=" * 100)
    kk = k[(k["podzial"] != "calosc") & (k["przejscie"] != "sesja_do_platn")].copy()
    kk["abs"] = kk["zamowienia_razem"].abs()
    pokaz(kk.sort_values("abs", ascending=False).drop(columns=["rodzaj", "abs"]).head(80))

    r("\n" + "=" * 100)
    r("3. ZMIANY KONWERSJI SESJA DO PŁATNOŚCI W PODZIAŁACH")
    r("=" * 100)
    ks = k[(k["podzial"] != "calosc") & (k["przejscie"] == "sesja_do_platn")]
    pokaz(ks.sort_values(["podzial", "data"]).drop(columns=["rodzaj", "przejscie"]))

    r("\n" + "=" * 100)
    r("4. ZMIANY RUCHU (sesje dziennie): starty, końce i zmiany poziomu")
    r("=" * 100)
    rr = wy[(wy["rodzaj"] == "ruch") & wy["podzial"].isin(["kanal", "kampania", "strona_wejscia", "przegladarka", "urzadzenie"])]
    pokaz(rr.sort_values(["data", "podzial"]).drop(columns=["rodzaj", "przejscie", "wejscia_po", "zamowienia_razem",
                                                            "zamowienia_na_30_dni"], errors="ignore"))

    weryfikacja(r, pokaz)

    r("\n" + "=" * 100)
    r("6. STARTY KAMPANII WIDOCZNE W RUCHU: ILE SESJI I ZAMÓWIEŃ W SESJI KAMPANII (wszystkie sesje zwykłe)")
    r("=" * 100)
    r("   Zamówienia według sesji płatności (pierwsze zamówienia osobno); źródło pozyskania według reguły Z1K")
    r("   jest w analiza/wyniki/a5p_sezon.txt, sekcja 2. Kampania sprzedaży TelemediGO: zakupy samego TelemediGO.")
    wsz = pd.read_csv(WEJSCIE, parse_dates=["dzien"])
    kam = wsz[(wsz["podzial"] == "kampania") & (wsz["wartosc"].isin(["meta_prosp_l4_szybko", "tt_prosp_l4_15min", "crm_go_upsell"]))]
    st = kam.groupby("wartosc").agg(pierwszy_dzien=("dzien", "min"), dni=("dzien", "nunique"), sesje=("sesje", "sum"),
                                    platnosci=("k5", "sum"), zamowienia=("zamowienia", "sum"),
                                    pierwsze_zamowienia=("pierwsze_zamowienia", "sum")).reset_index()
    st["pierwszy_dzien"] = st["pierwszy_dzien"].dt.date
    st["sesje_dziennie"] = (st["sesje"] / st["dni"]).round(1)
    st["zamowienia_dziennie"] = (st["zamowienia"] / st["dni"]).round(1)
    st["proc_sesja_do_platn"] = (100 * st["platnosci"] / st["sesje"]).round(2)
    pokaz(st)

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Zapisano {WYNIK} ({len(linie)} linii), {len(wy)} zmian")


if __name__ == "__main__":
    main()
