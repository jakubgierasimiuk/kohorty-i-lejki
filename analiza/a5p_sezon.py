"""A5 (pozyskanie) — sezon a wydatki na kampanie (2026-10-19).

Pytanie z PLAN.md (A5, pułapki): czy wzrost liczby nowych pacjentów od października 2024 do stycznia 2025
(i później) idzie za wydatkami na kampanie, czy za sezonem. Wydatki też mają kształt zimowy, więc oba wpływy
nakładają się w czasie. Rozdzielamy je pośrednio:
  1. nowi pacjenci miesiąc po miesiącu w kanałach płatnych i bezpłatnych (źródło Z1K, ZALOZENIA.md 22);
     kanały bezpłatne nie mają wydatków, więc ich ruch pokazuje popyt bez reklamy (z zastrzeżeniem, że reklama
     może podnosić wejścia bezpośrednie i wyszukiwanie marki);
  2. koszt pozyskania i wydajność każdej kampanii płatnej w miesiącach (zł na nowego pacjenta, nowi na 1 000 kliknięć);
  3. wyświetlenia, kliknięcia i koszt kliknięcia w Google Ads jako przybliżenie popytu w wyszukiwarce;
  4. cel pierwszej wizyty nowych pacjentów (L4, e-recepta, konsultacja, skierowanie) w miesiącach;
  5. te same miesiące rok do roku.
Dwa lata danych to jedna obserwacja każdego sezonu na rok, więc sezonu nie oddzielimy w pełni od trendu.

Definicje: wspólny moduł analiza/definicje.py (tylko import). Tylko czyta schemat `czyste`. Uruchomienie:
    python -I analiza/a5p_sezon.py
Wynik: analiza/wyniki/a5p_sezon.txt, analiza/wyniki/a5p_sezon_miesiace.csv
"""

import datetime as dt
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "a5p_sezon.txt")
WYNIK_CSV = os.path.join(KATALOG, "analiza", "wyniki", "a5p_sezon_miesiace.csv")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_rows", 500)

PLATNE = ("google_ads_marka", "google_ads_ogolne", "meta_pozyskanie", "meta_remarketing", "tiktok")
GRUPA = f"""CASE WHEN kanal IN {PLATNE} THEN 'platne'
                 WHEN kanal = 'afiliacja_ranking' THEN 'afiliacja'
                 ELSE 'bezplatne' END"""


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=False)
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def df(sql):
        return con.sql(sql).df()

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    r(f"A5 POZYSKANIE — SEZON A WYDATKI NA KAMPANIE ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Nowy pacjent = N1 (ZALOZENIA.md 16), miesiąc = miesiąc pierwszego zakupu (czas polski). Źródło = Z1K (punkt 22).")
    r("Kanały płatne: Google Ads (marka i ogólne), Meta (pozyskanie i remarketing), TikTok. Afiliacja (ranking lekarzy)")
    r("osobno, bo płacimy prowizję za pacjenta, a nie za kliknięcie. Bezpłatne: wejścia bezpośrednie, bezpłatne")
    r("wyszukiwanie (Google i Bing), program poleceń, newsletter i SMS. Wydatki netto z marketing_spend.csv (czas polski).")

    con.execute(f"""
      CREATE TEMP TABLE np AS
      SELECT k.user_id, k.d0, strftime(date_trunc('month', k.d0), '%Y-%m') m, z.kanal, z.kampania, {GRUPA} grupa,
             o.visit_purpose cel
      FROM koh k JOIN zrodlo z USING (user_id) JOIN zam o ON o.order_id = k.order_id""")
    con.execute("""
      CREATE TEMP TABLE wyd AS
      SELECT strftime(date_trunc('month', date), '%Y-%m') m, utm_campaign kampania,
             sum(spend_pln)::DOUBLE wydatki, sum(clicks) klikniecia, sum(impressions) wyswietlenia
      FROM czyste.marketing_spend GROUP BY 1, 2""")

    # ---------- 1. miesiące ----------
    r("\n" + "=" * 100)
    r("1. NOWI PACJENCI W KANAŁACH PŁATNYCH I BEZPŁATNYCH, WYDATKI NA KAMPANIE, MIESIĄC PO MIESIĄCU")
    r("=" * 100)
    m = df("""
      WITH n AS (SELECT m, count(*) nowi, count(*) FILTER (WHERE grupa = 'platne') nowi_platne,
                        count(*) FILTER (WHERE grupa = 'bezplatne') nowi_bezplatne,
                        count(*) FILTER (WHERE grupa = 'afiliacja') nowi_afiliacja,
                        count(*) FILTER (WHERE kanal IN ('meta_pozyskanie', 'tiktok')) nowi_meta_tiktok,
                        count(*) FILTER (WHERE kanal IN ('google_ads_marka', 'google_ads_ogolne')) nowi_google_ads,
                        count(*) FILTER (WHERE kanal = 'wyszukiwarka_bezplatna') nowi_wyszukiwarka_bezpl,
                        count(*) FILTER (WHERE kanal = 'bezposrednie') nowi_bezposrednie
                 FROM np GROUP BY 1),
           w AS (SELECT m, sum(wydatki) wydatki, sum(klikniecia) klikniecia FROM wyd GROUP BY 1),
           d AS (SELECT strftime(date_trunc('month', d), '%Y-%m') m, count(*) dni
                 FROM range(DATE '2024-10-01', DATE '2026-10-01', INTERVAL 1 DAY) t(d) GROUP BY 1)
      SELECT n.*, round(w.wydatki) wydatki_zl, w.klikniecia, d.dni,
             round(n.nowi_platne / (w.wydatki / 1000), 2) nowi_platne_na_1000_zl,
             round(w.wydatki / n.nowi_platne) zl_na_nowego_platnego
      FROM n JOIN w USING (m) JOIN d USING (m) ORDER BY m""")
    m.to_csv(WYNIK_CSV, index=False, encoding="utf-8")
    pokaz(m)
    r(f"   Ta sama tabela w pliku {os.path.relpath(WYNIK_CSV, KATALOG)}.")

    r("\n1b. Na dzień (żeby miesiące różnej długości się nie myliły) i jako indeks: październik 2024 = 100")
    x = m.copy()
    for k in ("nowi_platne", "nowi_bezplatne", "nowi_google_ads", "nowi_wyszukiwarka_bezpl", "nowi_bezposrednie", "wydatki_zl"):
        x[k + "_dz"] = x[k] / x["dni"]
    idx = pd.DataFrame({"miesiac": x["m"]})
    for k, nazwa in (("wydatki_zl", "wydatki"), ("nowi_platne", "nowi_platne"), ("nowi_google_ads", "nowi_google_ads"),
                     ("nowi_bezplatne", "nowi_bezplatne"), ("nowi_wyszukiwarka_bezpl", "nowi_wyszuk_bezpl"),
                     ("nowi_bezposrednie", "nowi_bezposr")):
        idx[nazwa] = (100 * x[k + "_dz"] / x[k + "_dz"].iloc[0]).round(0).astype(int)
    pokaz(idx)

    # ---------- 2. kampanie płatne ----------
    r("\n" + "=" * 100)
    r("2. KAMPANIE PŁATNE: WYDATKI, KLIKNIĘCIA I NOWI PACJENCI (Z1K) W MIESIĄCACH")
    r("=" * 100)
    r("   zl_na_nowego = wydatki / nowi pacjenci kampanii; nowi_na_1000_klik = nowi / kliknięcia × 1000.")
    k = df("""
      WITH n AS (SELECT m, kampania, count(*) nowi FROM np WHERE grupa = 'platne' GROUP BY 1, 2)
      SELECT w.m, w.kampania, round(w.wydatki) wydatki_zl, w.klikniecia, coalesce(n.nowi, 0) nowi,
             round(w.wydatki / nullif(n.nowi, 0)) zl_na_nowego, round(1000 * n.nowi / w.klikniecia, 1) nowi_na_1000_klik,
             round(w.wydatki / w.klikniecia, 2) zl_na_klik
      FROM wyd w LEFT JOIN n USING (m, kampania) ORDER BY w.kampania, w.m""")
    for nazwa, w in k.groupby("kampania", sort=False):
        r(f"\n2. {nazwa}")
        pokaz(w.drop(columns=["kampania"]))

    # ---------- 3. popyt w wyszukiwarce ----------
    r("\n" + "=" * 100)
    r("3. GOOGLE ADS: WYŚWIETLENIA, KLIKNIĘCIA I KOSZT KLIKNIĘCIA (przybliżenie popytu w wyszukiwarce)")
    r("=" * 100)
    r("   Wyświetlenia kampanii w wyszukiwarce zależą od liczby wyszukiwań i od budżetu. Koszt kliknięcia rośnie,")
    r("   gdy rośnie konkurencja o te same hasła. Kampania na hasło „Telemedi” (gs_brand) najlepiej oddaje")
    r("   zainteresowanie samą marką. Obok sesje z bezpłatnego wyszukiwania (Google i Bing) na dzień.")
    pokaz(df("""
      WITH g AS (SELECT m, sum(wyswietlenia) FILTER (WHERE kampania = 'gs_brand') wysw_marka,
                        sum(wyswietlenia) FILTER (WHERE kampania LIKE 'gs_generic%') wysw_ogolne,
                        round(sum(wydatki) FILTER (WHERE kampania LIKE 'gs_generic%')
                              / sum(klikniecia) FILTER (WHERE kampania LIKE 'gs_generic%'), 2) zl_na_klik_ogolne,
                        round(100.0 * sum(klikniecia) FILTER (WHERE kampania LIKE 'gs_generic%')
                              / sum(wyswietlenia) FILTER (WHERE kampania LIKE 'gs_generic%'), 2) proc_klikniec_ogolne,
                        round(sum(wydatki) FILTER (WHERE kampania LIKE 'gs_generic%')) wydatki_ogolne_zl
                 FROM wyd GROUP BY 1),
           s AS (SELECT strftime(date_trunc('month', dzien_pl), '%Y-%m') m,
                        count(*) FILTER (WHERE utm_medium = 'organic') / count(DISTINCT dzien_pl) sesje_bezpl_wyszuk_dziennie,
                        count(*) FILTER (WHERE utm_source IS NULL) / count(DISTINCT dzien_pl) sesje_bezposr_dziennie
                 FROM czyste.sessions GROUP BY 1)
      SELECT g.*, round(s.sesje_bezpl_wyszuk_dziennie, 1) sesje_bezpl_wyszuk_dziennie,
             round(s.sesje_bezposr_dziennie, 1) sesje_bezposr_dziennie
      FROM g JOIN s USING (m) ORDER BY m"""))
    r("\n3b. Bezpłatne wyszukiwanie i wejścia bezpośrednie: sesje osób, które jeszcze nie kupowały, na dzień")
    r("    (bez sesji z kontem i bez anonimowych sesji przeglądarek pacjentów po pierwszym zakupie)")
    pokaz(df("""
      WITH p AS (SELECT s.session_id, s.dzien_pl, s.utm_medium, s.utm_source,
                        coalesce(k.t0 < s.started_at_pl, FALSE) po_zakupie
                 FROM czyste.sessions s LEFT JOIN przeg pr ON pr.visitor_id = s.visitor_id
                 LEFT JOIN koh k ON k.user_id = coalesce(s.user_id, pr.user_id))
      SELECT strftime(date_trunc('month', dzien_pl), '%Y-%m') m,
             round(count(*) FILTER (WHERE utm_medium = 'organic' AND NOT po_zakupie) / count(DISTINCT dzien_pl), 1) bezpl_wyszuk_nowi,
             round(count(*) FILTER (WHERE utm_source IS NULL AND NOT po_zakupie) / count(DISTINCT dzien_pl), 1) bezposr_nowi
      FROM p GROUP BY 1 ORDER BY 1"""))

    # ---------- 4. cel pierwszej wizyty ----------
    r("\n" + "=" * 100)
    r("4. CEL PIERWSZEJ WIZYTY NOWYCH PACJENTÓW W MIESIĄCACH (procent nowych pacjentów w grupie kanałów)")
    r("=" * 100)
    for g in ("bezplatne", "platne"):
        r(f"\n4. {g}")
        pokaz(df(f"""
          SELECT m, count(*) nowi,
                 round(100 * avg((cel = 'l4')::INT), 1) l4, round(100 * avg((cel = 'e_recepta')::INT), 1) e_recepta,
                 round(100 * avg((cel = 'konsultacja')::INT), 1) konsultacja, round(100 * avg((cel = 'skierowanie')::INT), 1) skierowanie
          FROM np WHERE grupa = '{g}' GROUP BY 1 ORDER BY 1"""))
    r("\n4b. Nowi pacjenci z kanałów bezpłatnych na dzień według celu pierwszej wizyty")
    pokaz(df("""
      SELECT m, round(count(*) FILTER (WHERE cel = 'l4') / max(day(last_day(d0))), 1) l4_dziennie,
             round(count(*) FILTER (WHERE cel = 'e_recepta') / max(day(last_day(d0))), 1) e_recepta_dziennie,
             round(count(*) FILTER (WHERE cel = 'konsultacja') / max(day(last_day(d0))), 1) konsultacja_dziennie,
             round(count(*) FILTER (WHERE cel = 'skierowanie') / max(day(last_day(d0))), 1) skierowanie_dziennie
      FROM np WHERE grupa = 'bezplatne' GROUP BY 1 ORDER BY 1"""))

    # ---------- 5. rok do roku ----------
    r("\n" + "=" * 100)
    r("5. TE SAME MIESIĄCE ROK DO ROKU: X–I (zima) i V–VIII (lato), nowi pacjenci i wydatki")
    r("=" * 100)
    pokaz(df("""
      WITH n AS (SELECT CASE WHEN m BETWEEN '2024-10' AND '2025-01' THEN 'X 2024 - I 2025'
                             WHEN m BETWEEN '2025-10' AND '2026-01' THEN 'X 2025 - I 2026'
                             WHEN m BETWEEN '2025-05' AND '2025-08' THEN 'V - VIII 2025'
                             WHEN m BETWEEN '2026-05' AND '2026-08' THEN 'V - VIII 2026' END okres,
                        grupa, count(*) nowi FROM np GROUP BY 1, 2),
           w AS (SELECT CASE WHEN m BETWEEN '2024-10' AND '2025-01' THEN 'X 2024 - I 2025'
                             WHEN m BETWEEN '2025-10' AND '2026-01' THEN 'X 2025 - I 2026'
                             WHEN m BETWEEN '2025-05' AND '2025-08' THEN 'V - VIII 2025'
                             WHEN m BETWEEN '2026-05' AND '2026-08' THEN 'V - VIII 2026' END okres,
                        round(sum(wydatki)) wydatki_zl FROM wyd GROUP BY 1)
      SELECT okres, sum(nowi) FILTER (WHERE grupa = 'bezplatne') nowi_bezplatne,
             sum(nowi) FILTER (WHERE grupa = 'platne') nowi_platne, sum(nowi) FILTER (WHERE grupa = 'afiliacja') nowi_afiliacja,
             any_value(w.wydatki_zl) wydatki_zl
      FROM n JOIN w USING (okres) WHERE okres IS NOT NULL GROUP BY 1 ORDER BY 1"""))
    r("\n5b. Zima wobec lata w tym samym roku: ile razy więcej nowych pacjentów na dzień zimą (X–I) niż latem (V–VIII)")
    r("    w kanałach bezpłatnych i w kanałach płatnych, obok tego samego stosunku dla wydatków.")
    pokaz(df("""
      WITH n AS (SELECT CASE WHEN m BETWEEN '2024-10' AND '2025-01' THEN 'zima1' WHEN m BETWEEN '2025-05' AND '2025-08' THEN 'lato1'
                             WHEN m BETWEEN '2025-10' AND '2026-01' THEN 'zima2' WHEN m BETWEEN '2026-05' AND '2026-08' THEN 'lato2' END p,
                        grupa, kanal FROM np),
           w AS (SELECT CASE WHEN m BETWEEN '2024-10' AND '2025-01' THEN 'zima1' WHEN m BETWEEN '2025-05' AND '2025-08' THEN 'lato1'
                             WHEN m BETWEEN '2025-10' AND '2026-01' THEN 'zima2' WHEN m BETWEEN '2026-05' AND '2026-08' THEN 'lato2' END p,
                        kampania, wydatki FROM wyd)
      SELECT 'rok 1: X 2024 - I 2025 wobec V - VIII 2025' porownanie,
             round((count(*) FILTER (WHERE p = 'zima1' AND grupa = 'bezplatne') / 123.0)
                   / (count(*) FILTER (WHERE p = 'lato1' AND grupa = 'bezplatne') / 123.0), 2) bezplatne,
             round((count(*) FILTER (WHERE p = 'zima1' AND grupa = 'platne') / 123.0)
                   / (count(*) FILTER (WHERE p = 'lato1' AND grupa = 'platne') / 123.0), 2) platne,
             (SELECT round(sum(wydatki) FILTER (WHERE p = 'zima1') / sum(wydatki) FILTER (WHERE p = 'lato1'), 2) FROM w) wydatki,
             (SELECT round(sum(wydatki) FILTER (WHERE p = 'zima1' AND kampania LIKE 'gs%')
                           / sum(wydatki) FILTER (WHERE p = 'lato1' AND kampania LIKE 'gs%'), 2) FROM w) wydatki_google,
             round((count(*) FILTER (WHERE p = 'zima1' AND kanal IN ('google_ads_marka', 'google_ads_ogolne')))
                   / (count(*) FILTER (WHERE p = 'lato1' AND kanal IN ('google_ads_marka', 'google_ads_ogolne'))), 2) nowi_google_ads
      FROM n
      UNION ALL
      SELECT 'rok 2: X 2025 - I 2026 wobec V - VIII 2026',
             round(count(*) FILTER (WHERE p = 'zima2' AND grupa = 'bezplatne') / count(*) FILTER (WHERE p = 'lato2' AND grupa = 'bezplatne'), 2),
             round(count(*) FILTER (WHERE p = 'zima2' AND grupa = 'platne') / count(*) FILTER (WHERE p = 'lato2' AND grupa = 'platne'), 2),
             (SELECT round(sum(wydatki) FILTER (WHERE p = 'zima2') / sum(wydatki) FILTER (WHERE p = 'lato2'), 2) FROM w),
             (SELECT round(sum(wydatki) FILTER (WHERE p = 'zima2' AND kampania LIKE 'gs%')
                           / sum(wydatki) FILTER (WHERE p = 'lato2' AND kampania LIKE 'gs%'), 2) FROM w),
             round((count(*) FILTER (WHERE p = 'zima2' AND kanal IN ('google_ads_marka', 'google_ads_ogolne')))
                   / (count(*) FILTER (WHERE p = 'lato2' AND kanal IN ('google_ads_marka', 'google_ads_ogolne'))), 2)
      FROM n"""))
    r("   Oba okresy porównania mają po 123 dni (X–I i V–VIII), więc stosunek liczb jest stosunkiem średnich dziennych.")

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Zapisano {WYNIK} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
