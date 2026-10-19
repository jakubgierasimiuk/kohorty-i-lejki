"""A5 (pozyskanie) — lejek od sesji do płatności, dzień po dniu, w podziałach (2026-10-19).

Kroki lejka (README): 1 wybór usługi, 2 wybór terminu, 3 logowanie albo konto, 4 wejście na płatność,
5 płatność przyjęta. Każdy krok występuje w sesji najwyżej raz, a kroki idą zawsze w kolejności (A2).

Typy sesji (ZALOZENIA.md 10):
  zwykla                 — sesja bez konta albo z kontem, które pojawia się dopiero na kroku 3;
  zalogowana_od_wejscia  — konto w sesji, bez kroku 3, poza zakupem samego TelemediGO (osobny wiersz);
  samo_telemedigo        — zakup samego TelemediGO (README: ma tylko dwa ostatnie kroki).
Główny lejek i jego podziały liczymy na sesjach zwykłych.

Dzień = dzień rozpoczęcia sesji w czasie polskim (dzien_pl). Odstępy między krokami liczymy w UTC.
Podziały: urządzenie, przeglądarka (Instagram, Facebook i TikTok to przeglądarki wbudowane w aplikacje),
kanał i kampania z UTM sesji (te same grupy co w A4), strona wejścia, oraz to, czy odwiedzający kupował
już wcześniej (przez konto albo przeglądarkę, w której kiedyś był zalogowany).

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/a5p_lejek.py
Wynik: analiza/wyniki/a5p_lejek.txt, analiza/wyniki/a5p_lejek_dzienny.csv.gz (serie dzienne dla narzędzia
i dla wykrywania zdarzeń w analiza/a5p_zdarzenia.py)
"""

import datetime as dt
import os
import sys

import duckdb
import pandas as pd

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAZA = os.path.join(KATALOG, "analiza", "telemedi.duckdb")
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "a5p_lejek.txt")
WYNIK_DZIENNY = os.path.join(KATALOG, "analiza", "wyniki", "a5p_lejek_dzienny.csv.gz")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_rows", 500)

# te same grupy kampanii co w analiza/a4_definicje.py (ZALOZENIA.md 22)
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
KAMPANIA = "coalesce(utm_campaign, utm_source || '_' || utm_medium, 'bezposrednie')"

PODZIALY = {"urzadzenie": "device", "przegladarka": "browser", "urzadzenie_przegladarka": "device || ' ' || browser",
            "system_przegladarka": "os || ' ' || browser",
            "kanal": "kanal", "kampania": "kampania", "strona_wejscia": "landing_page", "pacjent": "pacjent"}

KROKI = ["sesje", "k1", "k2", "k3", "k4", "k5"]
PRZEJSCIA = [("k1", "sesje", "usluga"), ("k2", "k1", "termin"), ("k3", "k2", "logowanie"),
             ("k4", "k3", "wejscie_platn"), ("k5", "k4", "platnosc"), ("k5", "sesje", "sesja_do_platn")]


def konwersje(ramka):
    """Dokleja konwersje kroków w procentach (krok wobec poprzedniego) i sesja do płatności."""
    for licz, mian, nazwa in PRZEJSCIA:
        ramka[nazwa] = (100 * ramka[licz] / ramka[mian].where(ramka[mian] > 0)).round(1)
    return ramka


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

    r(f"A5 POZYSKANIE — LEJEK OD SESJI DO PŁATNOŚCI ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Kroki: k1 wybór usługi, k2 wybór terminu, k3 logowanie albo konto, k4 wejście na płatność, k5 płatność przyjęta.")
    r("Konwersja kroku = sesje z krokiem / sesje z krokiem poprzednim, w procentach. sesja_do_platn = k5 / sesje.")
    r("Okres 1 = sesje od 1.10.2024 do 30.09.2025, okres 2 = od 1.10.2025 do 30.09.2026 (dzień sesji, czas polski).")

    # ---------- tabela sesji ----------
    con.execute("""
      CREATE TEMP TABLE ev AS
      SELECT session_id,
             min(event_at_utc) FILTER (WHERE event_name = 'service_selected') t1,
             min(event_at_utc) FILTER (WHERE event_name = 'slot_selected') t2,
             min(event_at_utc) FILTER (WHERE event_name = 'account_completed') t3,
             min(event_at_utc) FILTER (WHERE event_name = 'payment_started') t4,
             min(event_at_utc) FILTER (WHERE event_name = 'payment_succeeded') t5
      FROM czyste.events GROUP BY 1""")
    con.execute("""
      CREATE TEMP TABLE zam AS
      SELECT o.*, row_number() OVER (PARTITION BY user_id ORDER BY created_at, order_id) nr FROM czyste.orders o""")
    con.execute("CREATE TEMP TABLE przeg AS SELECT DISTINCT visitor_id, user_id FROM czyste.sessions WHERE user_id IS NOT NULL")
    con.execute("CREATE TEMP TABLE pierwszy AS SELECT user_id, min(created_at) t FROM czyste.orders GROUP BY 1")
    con.execute(f"""
      CREATE TEMP TABLE sl AS
      SELECT s.session_id, s.dzien_pl dzien, s.started_at_utc, s.device, s.browser, s.os, s.landing_page, s.user_id,
             coalesce(s.user_id, p.user_id) pacjent_id,
             {KANAL} kanal, {KAMPANIA} kampania,
             CASE WHEN s.dzien_pl < DATE '2025-10-01' THEN 1 ELSE 2 END okres,
             CASE WHEN g.session_id IS NOT NULL THEN 'samo_telemedigo'
                  WHEN s.user_id IS NOT NULL AND e.t3 IS NULL THEN 'zalogowana_od_wejscia'
                  ELSE 'zwykla' END typ,
             CASE WHEN pz.t < s.started_at_pl THEN 'kupowal_wczesniej' ELSE 'nie_kupowal' END pacjent,
             (e.t1 IS NOT NULL)::INT k1, (e.t2 IS NOT NULL)::INT k2, (e.t3 IS NOT NULL)::INT k3,
             (e.t4 IS NOT NULL)::INT k4, (e.t5 IS NOT NULL)::INT k5,
             e.t1, e.t2, e.t3, e.t4, e.t5,
             (o.order_id IS NOT NULL)::INT zamowienie, coalesce(o.nr = 1, FALSE)::INT pierwsze_zamowienie,
             o.order_id
      FROM czyste.sessions s
      LEFT JOIN ev e USING (session_id)
      LEFT JOIN (SELECT DISTINCT session_id FROM czyste.go_memberships WHERE order_id IS NULL) g USING (session_id)
      LEFT JOIN przeg p ON p.visitor_id = s.visitor_id AND s.user_id IS NULL
      LEFT JOIN pierwszy pz ON pz.user_id = coalesce(s.user_id, p.user_id)
      LEFT JOIN zam o ON o.session_id = s.session_id""")
    kontrola = df("SELECT count(*) sesje, count(DISTINCT session_id) unikalne, sum(zamowienie) zamowienia, sum(k5) platnosci FROM sl")
    r("\nKontrola: " + ", ".join(f"{k} = {int(v):,}".replace(",", " ") for k, v in kontrola.iloc[0].items()))

    kroki_sql = "count(*) sesje, sum(k1) k1, sum(k2) k2, sum(k3) k3, sum(k4) k4, sum(k5) k5, sum(zamowienie) zamowienia"

    # ---------- 1. typy sesji ----------
    r("\n" + "=" * 100)
    r("1. TYPY SESJI I ICH KROKI (oba okresy razem i osobno)")
    r("=" * 100)
    pokaz(konwersje(df(f"SELECT typ, 'razem' okres, {kroki_sql} FROM sl GROUP BY 1 UNION ALL "
                       f"SELECT typ, okres::VARCHAR, {kroki_sql} FROM sl GROUP BY 1, 2 ORDER BY 1, 2")))
    r("   Sesje zalogowane od wejścia nie mają kroku 3 z definicji; zakup samego TelemediGO ma tylko kroki 4 i 5.")

    # ---------- 2. lejek główny w kwartałach ----------
    r("\n" + "=" * 100)
    r("2. LEJEK GŁÓWNY (sesje zwykłe) W KWARTAŁACH")
    r("=" * 100)
    pokaz(konwersje(df(f"""
      SELECT strftime(date_trunc('quarter', dzien), '%Y-%m') kwartal_od, {kroki_sql},
             sum(pierwsze_zamowienie) pierwsze_zam
      FROM sl WHERE typ = 'zwykla' GROUP BY 1 ORDER BY 1""")))
    r("\n2b. To samo w miesiącach (tylko konwersje kroków)")
    m = konwersje(df(f"""
      SELECT strftime(date_trunc('month', dzien), '%Y-%m') miesiac, {kroki_sql}
      FROM sl WHERE typ = 'zwykla' GROUP BY 1 ORDER BY 1"""))
    pokaz(m[["miesiac", "sesje", "k5"] + [p[2] for p in PRZEJSCIA]])
    r("\n2c. Sesja do płatności w miesiącach: osoby, które jeszcze nie kupowały, i pacjenci, którzy już kupowali")
    r("    (konto sesji albo konto przeglądarki, w której pacjent kiedyś był zalogowany; pierwszy zakup przed sesją)")
    pokaz(df("""
      SELECT strftime(date_trunc('month', dzien), '%Y-%m') miesiac,
             count(*) FILTER (WHERE pacjent = 'nie_kupowal') sesje_nowych,
             round(100 * avg(k5) FILTER (WHERE pacjent = 'nie_kupowal'), 1) sesja_do_platn_nowych,
             count(*) FILTER (WHERE pacjent = 'kupowal_wczesniej') sesje_powracajacych,
             round(100 * avg(k5) FILTER (WHERE pacjent = 'kupowal_wczesniej'), 1) sesja_do_platn_powracajacych,
             round(100 * avg(k5), 1) sesja_do_platn_wszystkich
      FROM sl WHERE typ = 'zwykla' GROUP BY 1 ORDER BY 1"""))

    # ---------- 3. podziały w okresach ----------
    r("\n" + "=" * 100)
    r("3. PODZIAŁY LEJKA GŁÓWNEGO: OKRES 1 WOBEC OKRESU 2")
    r("=" * 100)
    r("   udzial_ses = udział w sesjach zwykłych okresu w %. Kolumny konwersji jak wyżej, dla okresu 1 i 2;")
    r("   zm_* = zmiana w punktach procentowych (okres 2 minus okres 1).")
    for nazwa, wyr in PODZIALY.items():
        if nazwa in ("urzadzenie_przegladarka", "system_przegladarka"):
            continue
        t = konwersje(df(f"""
          SELECT {wyr} wartosc, okres, {kroki_sql} FROM sl WHERE typ = 'zwykla' GROUP BY 1, 2"""))
        t["udzial_ses"] = (100 * t["sesje"] / t.groupby("okres")["sesje"].transform("sum")).round(1)
        kol = ["sesje", "udzial_ses"] + [p[2] for p in PRZEJSCIA]
        w = t.pivot(index="wartosc", columns="okres", values=kol)
        out = pd.DataFrame({"wartosc": w.index})
        for k in kol:
            for o in (1, 2):
                out[f"{k}_{o}"] = w[(k, o)].values if (k, o) in w.columns else None
        for k in ("usluga", "termin", "logowanie", "wejscie_platn", "platnosc", "sesja_do_platn"):
            out[f"zm_{k}"] = (out[f"{k}_2"] - out[f"{k}_1"]).round(1)
        out = out.sort_values("sesje_2", ascending=False, na_position="last")
        r(f"\n3. {nazwa}")
        pokaz(out[["wartosc", "sesje_1", "sesje_2", "udzial_ses_1", "udzial_ses_2",
                   "usluga_1", "usluga_2", "termin_1", "termin_2", "logowanie_1", "logowanie_2",
                   "wejscie_platn_1", "wejscie_platn_2", "platnosc_1", "platnosc_2",
                   "sesja_do_platn_1", "sesja_do_platn_2"]].fillna("-"))

    # ---------- 4. struktura a konwersja ----------
    r("\n" + "=" * 100)
    r("4. ZMIANA KONWERSJI SESJA DO PŁATNOŚCI: STRUKTURA RUCHU A KONWERSJA W OBRĘBIE GRUP")
    r("=" * 100)
    r("   Rozkład zmiany (okres 2 minus okres 1, punkty procentowe) na dwie części, w każdym podziale osobno:")
    r("   efekt_struktury = suma po grupach (udział_2 − udział_1) × konwersja_1;")
    r("   efekt_konwersji = suma po grupach udział_2 × (konwersja_2 − konwersja_1).")
    r("   Grupy, których nie było w okresie 1 (nowe kampanie), wchodzą w całości do efektu struktury:")
    r("   ich konwersja_1 przyjmujemy równą konwersji_2. Rozkład opisuje, nie wskazuje przyczyny.")
    calosc = df("SELECT okres, sum(k5) / count(*) k FROM sl WHERE typ = 'zwykla' GROUP BY 1").set_index("okres")["k"]
    wiersze = []
    for nazwa, wyr in PODZIALY.items():
        t = df(f"SELECT {wyr} g, okres, count(*) n, sum(k5) k5 FROM sl WHERE typ = 'zwykla' GROUP BY 1, 2")
        w = t.pivot(index="g", columns="okres", values=["n", "k5"]).fillna(0)
        u1, u2 = w[("n", 1)] / w[("n", 1)].sum(), w[("n", 2)] / w[("n", 2)].sum()
        c2 = (w[("k5", 2)] / w[("n", 2)]).where(w[("n", 2)] > 0, 0)
        c1 = (w[("k5", 1)] / w[("n", 1)]).where(w[("n", 1)] > 0, c2)
        struktura = ((u2 - u1) * c1).sum()
        konw = (u2 * (c2 - c1)).sum()
        wiersze.append({"podzial": nazwa, "konwersja_1": round(100 * calosc[1], 2), "konwersja_2": round(100 * calosc[2], 2),
                        "zmiana_pp": round(100 * (calosc[2] - calosc[1]), 2),
                        "efekt_struktury_pp": round(100 * struktura, 2), "efekt_konwersji_pp": round(100 * konw, 2)})
    pokaz(pd.DataFrame(wiersze))

    # ---------- 5. czasy między krokami ----------
    r("\n" + "=" * 100)
    r("5. CZAS MIĘDZY KROKAMI (sekundy, UTC), sesje zwykłe")
    r("=" * 100)
    pokaz(df("""
      SELECT CASE WHEN zamowienie = 1 AND pierwsze_zamowienie = 1 THEN 'pierwsze zamowienie'
                  WHEN zamowienie = 1 THEN 'zamowienie powtorne' ELSE 'bez zamowienia' END rodzaj, okres,
             count(*) FILTER (WHERE k2 = 1) z_terminem,
             median(epoch(t2) - epoch(t1)) FILTER (WHERE k2 = 1) med_usluga_termin,
             median(epoch(t3) - epoch(t2)) FILTER (WHERE k3 = 1) med_termin_logowanie,
             quantile_cont(epoch(t3) - epoch(t2), 0.1) FILTER (WHERE k3 = 1) p10_termin_logowanie,
             median(epoch(t4) - epoch(t3)) FILTER (WHERE k4 = 1) med_logowanie_platn,
             median(epoch(t5) - epoch(t4)) FILTER (WHERE k5 = 1) med_platn_sukces
      FROM sl WHERE typ = 'zwykla' GROUP BY 1, 2 ORDER BY 1, 2"""))

    # ---------- 6. samo TelemediGO ----------
    r("\n" + "=" * 100)
    r("6. ZAKUP SAMEGO TELEMEDIGO (tylko kroki 4 i 5)")
    r("=" * 100)
    pokaz(df("""
      SELECT strftime(date_trunc('quarter', dzien), '%Y-%m') kwartal_od, count(*) sesje, sum(k4) k4, sum(k5) k5,
             count(*) FILTER (WHERE kampania = 'crm_go_upsell') z_crm_go_upsell,
             count(*) FILTER (WHERE landing_page = '/telemedigo') wejscie_telemedigo,
             count(*) FILTER (WHERE landing_page = '/konto') wejscie_konto
      FROM sl WHERE typ = 'samo_telemedigo' GROUP BY 1 ORDER BY 1"""))
    r("   Sesje, które weszły na /telemedigo albo z kampanii crm_go_upsell, a nie kupiły samego TelemediGO:")
    pokaz(df("""
      SELECT typ, count(*) sesje, sum(k1) k1, sum(k4) k4, sum(zamowienie) zamowienia
      FROM sl WHERE (landing_page = '/telemedigo' OR kampania = 'crm_go_upsell') GROUP BY 1 ORDER BY 2 DESC"""))

    # ---------- 6b. od kliknięcia reklamy do sesji ----------
    r("\n" + "=" * 100)
    r("6b. OD KLIKNIĘCIA REKLAMY DO SESJI (krok przed lejkiem; dopisek Kuby po przeglądzie, 2026-10-19)")
    r("=" * 100)
    r("   Kliknięcia z marketing_spend.csv wobec sesji z tym samym utm_campaign (wszystkie typy sesji), w okresach.")
    r("   W grze = kliknięcia × (sesje na kliknięcie w ogólnych kampaniach Google Ads w tym samym okresie) − sesje,")
    r("   czyli ile sesji więcej byłoby przy stosunku z Google. Zamówienia w grze = to × konwersja sesji kampanii")
    r("   do płatności (sesje zwykłe). Górna granica: zakłada, że brakujące osoby zachowałyby się jak te, które")
    r("   dotarły. Z danych nie wiemy, czy to porzucenie przed załadowaniem strony, czy luka w śledzeniu.")
    kl = df("""
      WITH k AS (SELECT utm_campaign kampania, CASE WHEN date < DATE '2025-10-01' THEN 1 ELSE 2 END okres,
                        sum(clicks) klikniecia, sum(spend_pln)::DOUBLE wydatki
                 FROM czyste.marketing_spend GROUP BY 1, 2),
           s AS (SELECT kampania, okres, count(*) sesje,
                        sum(k5) FILTER (WHERE typ = 'zwykla') / count(*) FILTER (WHERE typ = 'zwykla') konw,
                        avg((browser IN ('Instagram', 'Facebook', 'TikTok'))::INT) w_aplikacji
                 FROM sl GROUP BY 1, 2),
           g AS (SELECT okres, sum(s.sesje) / sum(k.klikniecia) wsk
                 FROM k JOIN s USING (kampania, okres) WHERE kampania LIKE 'gs_generic%' GROUP BY 1)
      SELECT k.kampania, k.okres, k.klikniecia, s.sesje, round(s.sesje / k.klikniecia, 3) sesje_na_klik,
             round(100 * s.w_aplikacji, 1) proc_sesji_w_aplikacji, round(100 * s.konw, 2) proc_sesja_do_platn,
             round(greatest(k.klikniecia * g.wsk - s.sesje, 0)) sesje_w_grze,
             round(greatest(k.klikniecia * g.wsk - s.sesje, 0) * s.konw) zamowienia_w_grze,
             round(k.wydatki * greatest(1 - s.sesje / (k.klikniecia * g.wsk), 0)) wydatki_bez_sesji_zl
      FROM k JOIN s USING (kampania, okres) JOIN g USING (okres) ORDER BY k.kampania, k.okres""")
    pokaz(kl)
    r("   wydatki_bez_sesji_zl = część wydatków przypadająca na brakujące sesje przy tym samym stosunku co Google.")
    r("   Razem w okresie 2 dla kampanii Meta i TikToka:")
    pokaz(kl[(kl["okres"] == 2) & kl["kampania"].str.match(r"^(meta|tt)_")][["sesje_w_grze", "zamowienia_w_grze",
                                                                            "wydatki_bez_sesji_zl"]].sum().to_frame().T)

    # ---------- 7. serie dzienne do pliku ----------
    czesci = []
    for nazwa, wyr in {"calosc": "'calosc'", **PODZIALY}.items():
        czesci.append(f"""
          SELECT dzien, typ, pacjent, '{nazwa}' podzial, {wyr} wartosc, {kroki_sql},
                 sum(pierwsze_zamowienie) pierwsze_zamowienia
          FROM sl GROUP BY ALL""")
    dz = df(" UNION ALL ".join(czesci) + " ORDER BY podzial, wartosc, typ, pacjent, dzien")
    dz.to_csv(WYNIK_DZIENNY, index=False, encoding="utf-8", compression="gzip")
    r("\n" + "=" * 100)
    r(f"7. SERIE DZIENNE: {os.path.relpath(WYNIK_DZIENNY, KATALOG)} — {len(dz):,} wierszy".replace(",", " "))
    r("   Kolumny: dzien, typ sesji, pacjent (kupowal_wczesniej / nie_kupowal), podzial, wartosc, sesje, k1..k5,")
    r("   zamowienia, pierwsze_zamowienia.")
    r("   Dni bez sesji w danej grupie nie mają wiersza (zero sesji).")

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Zapisano {WYNIK} ({len(linie)} linii) i {WYNIK_DZIENNY}")


if __name__ == "__main__":
    main()
