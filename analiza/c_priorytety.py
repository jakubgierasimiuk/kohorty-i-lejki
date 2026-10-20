"""C — liczby do odpowiedzi „czy to wzrost” i do listy priorytetów (2026-10-20).

Część W (wzrost): nowi pacjenci, powroty i marża na pacjenta według obu reguł źródła, z pacjentami dwóch nowych
kampanii na L4 i bez nich; wynik biznesu w obu okresach (marża po koszcie lekarza, kampaniach i prowizji) z rozbiciem
marży konsultacji na pierwsze zamówienia i zamówienia powtórne (start od zera).

Część P (priorytety): wartość każdej pozycji listy w marży na rok. Liczby z wcześniejszych raportów są wpisane jako
stałe z odnośnikiem; funkcja `z_raportu` sprawdza, że każda z nich naprawdę stoi w podanym raporcie (żeby żadna liczba
nie przeszła „z pamięci”). Nowe liczby (marża pacjentów z Safari na iOS, sesje zalogowane od wejścia, warunki
TelemediGO u specjalistów, gs_generic_specjalisci, koszt testu TelemediGO) liczy ten skrypt.

Definicje: analiza/definicje.py (ZALOZENIA.md 16–43). Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu:
    python -I analiza/c_priorytety.py
Wynik: analiza/wyniki/c_priorytety.txt
"""

import datetime as dt
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402

WYNIKI = os.path.join(D.KATALOG, "analiza", "wyniki")
WYNIK = os.path.join(WYNIKI, "c_priorytety.txt")
KONIEC = D.KONIEC
NOWE = ("meta_prosp_l4_szybko", "tt_prosp_l4_15min")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)


def z_raportu(plik, tekst, wartosc):
    """Liczba przepisana z raportu: sprawdza, że `tekst` stoi w pliku `plik` (analiza/wyniki), i zwraca `wartosc`."""
    with open(os.path.join(WYNIKI, plik), encoding="utf-8") as f:
        if tekst not in f.read():
            raise ValueError(f"W raporcie {plik} nie ma tekstu {tekst!r} — liczba nieaktualna")
    return wartosc


def zl(x):
    return f"{x:,.0f} zł".replace(",", " ")


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=True)
    q = lambda s: con.sql(s).df()  # noqa: E731
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    def naglowek(t):
        r("\n" + "=" * 110)
        r(t)
        r("=" * 110)

    r(f"C — LICZBY DO ODPOWIEDZI „CZY TO WZROST” I DO LISTY PRIORYTETÓW ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026. Z1K = przyjęta reguła źródła (pierwsze wejście, kod kampanii")
    r("rozstrzyga), Z2 = sesja płatności. „Nowe kampanie” = meta_prosp_l4_szybko i tt_prosp_l4_15min (oba na L4, od 3.11.2025")
    r("i 9.02.2026).")

    # ======================= W. CZY TO WZROST =======================
    naglowek("W1. WIĘCEJ PACJENTÓW: nowi pacjenci w okresach, z nowymi kampaniami i bez nich, obie reguły")
    con.execute(f"""
      CREATE TEMP TABLE kz AS
      SELECT p.*, z.kanal, z.kampania, z.kanal_z2, z.kampania_z2,
             z.kampania IN {NOWE} nowa_z1k, coalesce(z.kampania_z2 IN {NOWE}, FALSE) nowa_z2
      FROM powr p JOIN zrodlo z USING (user_id, okres)""")
    w1 = q("""SELECT okres, count(*) nowi,
                     count(*) FILTER (WHERE NOT nowa_z1k) bez_nowych_z1k,
                     count(*) FILTER (WHERE NOT nowa_z2) bez_nowych_z2,
                     count(*) FILTER (WHERE kanal IN ('bezposrednie', 'wyszukiwarka_bezplatna', 'program_polecen', 'crm')) bezplatne_z1k
              FROM kz GROUP BY 1 ORDER BY 1""")
    pokaz(w1)
    zm = (w1.iloc[1, 1:] / w1.iloc[0, 1:] - 1) * 100
    r("     zmiana %: " + ", ".join(f"{k}: {v:+.1f}%" for k, v in zm.items()))

    naglowek("W2. LEPSZA RETENCJA: powrót w 30/60/90 dniach na tych samych dniach kalendarzowych (ZALOZENIA.md 27)")
    for nazwa, war in (("wszyscy", "TRUE"), ("bez nowych kampanii (Z1K)", "NOT nowa_z1k"), ("bez nowych kampanii (Z2)", "NOT nowa_z2"),
                       ("tylko nowe kampanie (Z1K)", "nowa_z1k")):
        t = q(D.stopy_por(warunek=war, tabela="kz"))
        r(f"   {nazwa}:")
        pokaz(t)
    r("   Marża na pacjenta w 90 dniach (przed kosztem pozyskania, ZALOZENIA.md 34), te same dni kalendarzowe:")
    g1, g2 = D.granice_por(90)
    con.execute("CREATE TEMP TABLE m90 AS SELECT user_id, sum(marza) FILTER (WHERE dni <= 90) m FROM ek GROUP BY 1")
    w3 = q(f"""SELECT okres, count(*) pacjenci, avg(coalesce(m, 0)) marza_wszyscy,
                      avg(coalesce(m, 0)) FILTER (WHERE NOT nowa_z1k) marza_bez_nowych_z1k,
                      avg(coalesce(m, 0)) FILTER (WHERE NOT nowa_z2) marza_bez_nowych_z2
               FROM kz LEFT JOIN m90 USING (user_id)
               WHERE (okres = 1 AND d0 <= DATE '{g1}') OR (okres = 2 AND d0 <= DATE '{g2}') GROUP BY 1 ORDER BY 1""")
    pokaz(w3.round(1))

    naglowek("W3. WYNIK BIZNESU W OKRESACH KALENDARZOWYCH (zł)")
    r("   Marża = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza − wydatki na kampanie − prowizja afiliacyjna")
    r("   (prowizja według przyjętej reguły, ZALOZENIA.md 25). Zamówienia według dnia płatności, zwrot w dniu płatności.")
    w4 = q(f"""
      WITH zam_ok AS (
        SELECT CASE WHEN z.created_at < TIMESTAMP '{D.OKRES2}' THEN 1 ELSE 2 END okres, z.nr, k.okres okres_kohorty,
               (z.amount_paid - z.refund_amount)::DOUBLE przychod, ({D.KOSZT_LEKARZA})::DOUBLE koszt_lekarza
        FROM zam z JOIN koh k USING (user_id)),
      kons AS (SELECT okres, sum(przychod) przychod_konsultacji, sum(koszt_lekarza) koszt_lekarza,
                      sum(przychod - koszt_lekarza) FILTER (WHERE nr = 1) marza_pierwszych,
                      sum(przychod - koszt_lekarza) FILTER (WHERE nr > 1 AND okres_kohorty = 1) marza_powt_kohorty_o1,
                      sum(przychod - koszt_lekarza) FILTER (WHERE nr > 1 AND okres_kohorty = 2) marza_powt_kohorty_o2,
                      count(*) FILTER (WHERE nr = 1) zam_pierwsze, count(*) FILTER (WHERE nr > 1 AND okres_kohorty = 1) zam_powt_o1,
                      count(*) FILTER (WHERE nr > 1 AND okres_kohorty = 2) zam_powt_o2
               FROM zam_ok GROUP BY 1),
      go AS (SELECT CASE WHEN g.purchased_at < TIMESTAMP '{D.OKRES2}' THEN 1 ELSE 2 END okres, sum(g.amount_paid)::DOUBLE telemedigo,
                    sum(g.amount_paid) FILTER (WHERE k.okres = 1)::DOUBLE telemedigo_kohorty_o1
             FROM czyste.go_memberships g JOIN koh k USING (user_id) GROUP BY 1),
      wyd AS (SELECT CASE WHEN date < DATE '{D.OKRES2}' THEN 1 ELSE 2 END okres, sum(spend_pln)::DOUBLE wydatki_kampanie
              FROM czyste.marketing_spend GROUP BY 1),
      prow AS (SELECT okres, 25.0 * count(*) prowizja FROM zrodlo WHERE kanal = 'afiliacja_ranking' GROUP BY 1)
      SELECT * FROM kons JOIN go USING (okres) JOIN wyd USING (okres) JOIN prow USING (okres) ORDER BY okres""")
    w4["marza"] = w4.przychod_konsultacji + w4.telemedigo - w4.koszt_lekarza - w4.wydatki_kampanie - w4.prowizja
    t = w4.set_index("okres").T
    t["zmiana"] = t[2] - t[1]
    t["zmiana_proc"] = (100 * (t[2] / t[1] - 1)).round(1)
    pokaz(t.round(0).reset_index().rename(columns={"index": "pozycja", 1: "okres_1", 2: "okres_2"}))
    r("   marza_powt_kohorty_o1 w okresie 2 = marża z zamówień powtórnych pacjentów pozyskanych w okresie 1 (start od zera:")
    r("   w okresie 1 takiej bazy z poprzedniego roku nie było).")
    m1, m2 = w4.marza[0], w4.marza[1]
    baza = w4.marza_powt_kohorty_o1[1]
    go_baza = w4.telemedigo_kohorty_o1[1]
    r(f"   Po odjęciu marży powtórnych konsultacji pacjentów pozyskanych w okresie 1: okres 2 {zl(m2 - baza)} "
      f"({100 * ((m2 - baza) / m1 - 1):+.1f}% wobec okresu 1; bez odjęcia {100 * (m2 / m1 - 1):+.1f}%).")
    r(f"   Po odjęciu także ich opłat za TelemediGO w okresie 2 ({zl(go_baza)}): {zl(m2 - baza - go_baza)} "
      f"({100 * ((m2 - baza - go_baza) / m1 - 1):+.1f}%).")
    r("   To rozbicie księgowe, a nie wynik biznesu, który startuje od zera: nie modeluje zmian wydatków ani zachowania")
    r("   pacjentów (recenzja Codeksa).")

    # ======================= P. PRIORYTETY =======================
    naglowek("P1. SAFARI NA iOS: ZAKŁADANIE KONTA OD 17.03.2026 (a5p_zdarzenia.txt, 5f)")
    utr_hi = z_raportu("a5p_zdarzenia.txt", "695.0      105.3", 695.0)
    utr_lo = z_raportu("a5p_zdarzenia.txt", "628.0       95.2", 628.0)
    dni = 198
    m = q(f"""SELECT count(*) FILTER (WHERE k.d0 <= DATE '{KONIEC}' - 90) n90,
                     avg(coalesce(m90, 0)) FILTER (WHERE k.d0 <= DATE '{KONIEC}' - 90) marza90,
                     count(*) FILTER (WHERE k.d0 <= DATE '{KONIEC}' - 180) n180,
                     avg(coalesce(m180, 0)) FILTER (WHERE k.d0 <= DATE '{KONIEC}' - 180) marza180
              FROM koh k JOIN czyste.sessions s ON s.session_id = k.session_id
              LEFT JOIN (SELECT user_id, sum(marza) FILTER (WHERE dni <= 90) m90, sum(marza) FILTER (WHERE dni <= 180) m180
                         FROM ek GROUP BY 1) e ON e.user_id = k.user_id
              WHERE k.okres = 2 AND s.os = 'iOS' AND s.browser = 'Safari'""")
    pokaz(m.round(1))
    for nazwa, utr in (("po odjęciu tła", utr_lo), ("bez odjęcia tła", utr_hi)):
        rok = utr / dni * 365
        r(f"   {nazwa}: {utr:.0f} pierwszych zamówień w {dni} dniach, czyli {rok:.0f} rocznie; marża w 90 dniach "
          f"{zl(rok * m.marza90[0])}, w 180 dniach {zl(rok * m.marza180[0])} rocznie")
    r("   Założenia: utracone pierwsze zamówienie = utracony nowy pacjent (odpadnięci nie kupują później częściej w tej samej")
    r("   przeglądarce, a5p 5e; inne urządzenia nieznane); marża jak u nowych pacjentów z pierwszą płatnością w Safari na iOS")
    r("   w okresie 2; bez kosztu pozyskania, bo wejście już zostało opłacone; skala problemu z 17.03–30.09.2026 utrzymuje się")
    r("   przez rok. Kwoty to marża rocznika odzyskanych pacjentów w 90 albo 180 dniach od pozyskania, a nie wpływy w całości")
    r("   w tym samym roku kalendarzowym (recenzja Codeksa).")

    naglowek("P2. ZWROTY PO WIZYTACH L4 W NOWYCH KAMPANIACH — OBIETNICA REKLAMY (a5e_scenariusze.txt, E2a, E3, E3b)")
    a_z1k = z_raportu("a5e_scenariusze.txt", "710.7         57112", 57112)
    b_z1k = z_raportu("a5e_scenariusze.txt", "750.6             32.01          2.32         22283", 22283)
    a_z2 = z_raportu("a5e_scenariusze.txt", "399.2         31795", 31795)
    b_z2 = z_raportu("a5e_scenariusze.txt", "434.6             31.59          2.41         12680", 12680)
    r(f"   90 dni: przyjęta reguła od {zl(b_z1k)} (wariant B) do {zl(a_z1k)} (wariant A); sesja płatności od {zl(b_z2)} do {zl(a_z2)} rocznie.")
    a180 = z_raportu("a5e_scenariusze.txt", "nowe kampanie    Z1K            15917             16414              73526              38697", (73526 - 16414, 38697 - 16414))
    a180z2 = z_raportu("a5e_scenariusze.txt", "nowe kampanie     Z2           -59536            -59815             -28020             -47135", (-28020 + 59815, -47135 + 59815))
    r(f"   180 dni (zmiana wobec dziś): przyjęta reguła {zl(a180[1])} do {zl(a180[0])}; sesja płatności {zl(a180z2[1])} do {zl(a180z2[0])}.")

    naglowek("P3. TIKTOK NA L4 (tt_prosp_l4_15min): WYŁĄCZYĆ ALBO NAPRAWIĆ (a5e_scenariusze.txt, E3, E3b)")
    tt = z_raportu("a5e_scenariusze.txt", "tt_prosp_l4_15min    Z1K        -11928            14891             5810           2963          -6118           11928          47196         82464", None)
    tt2 = z_raportu("a5e_scenariusze.txt", "tt_prosp_l4_15min     Z2        -30801             7605             2976         -23196         -27825           30801          56633         82464", None)
    tt180 = z_raportu("a5e_scenariusze.txt", "tt_prosp_l4_15min    Z1K           -11928            -13468               1423              -7658               13468              47966", None)
    tt180b = z_raportu("a5e_scenariusze.txt", "tt_prosp_l4_15min     Z2           -30801            -32341             -24736             -29365               32341              57402", None)
    del tt, tt2, tt180, tt180b
    r("   Dziś (90 dni): −11 928 zł (Z1K), −30 801 zł (Z2). 180 dni: −13 468 zł i −32 341 zł.")
    r("   Wyłączyć (zmiana marży): przy 100% pacjentów dodatkowych +11 928 / +30 801 zł (90 dni), +13 468 / +32 341 zł (180 dni);")
    r("   przy 50%: +47 196 / +56 633 zł; przy 0%: +82 464 zł (oszczędzone wydatki).")
    r("   Naprawić zwroty: wynik po naprawie (wariant A) +2 963 zł (Z1K) i −23 196 zł (Z2) w 90 dniach; +1 423 i −24 736 zł w 180 dniach.")

    naglowek("P4. META NA L4 (meta_prosp_l4_szybko): DECYZJA PO TEŚCIE DODATKOWOŚCI (a5e_scenariusze.txt, E3, E3b)")
    z_raportu("a5e_scenariusze.txt", "meta_prosp_l4_szybko    Z1K         27845            42262            16486          70107          44331          -27845          67739        163322", None)
    z_raportu("a5e_scenariusze.txt", "meta_prosp_l4_szybko     Z2        -28735            24273             9745          -4462         -18990           28735          96029        163322", None)
    r("   Dziś (90 dni): +27 845 zł (Z1K), −28 735 zł (Z2); 180 dni: +29 882 zł i −27 474 zł.")
    r("   Wyłączyć: od −27 845 zł (Z1K, 100% dodatkowych) do +163 322 zł (0% dodatkowych). Naprawić zwroty (A): wynik +70 107 zł")
    r("   (Z1K) albo −4 462 zł (Z2). Rozpiętość decyzji: od −27,8 do +163,3 tys. zł rocznie — tyle jest wart test.")

    naglowek("P5. SESJE ZALOGOWANE OD WEJŚCIA BEZ ZAKUPU — WARIANT PESYMISTYCZNY (a5p_zalogowane.txt, sekcja 7)")
    s2 = z_raportu("a5p_zalogowane.txt", "2906", 2906)
    p_usl = z_raportu("a5p_zalogowane.txt", "40.9", 0.409)
    p_gora = z_raportu("a5p_zalogowane.txt", "90.5", 0.905)
    marza_powt = z_raportu("a5p_zalogowane.txt", "33.99", 33.99)
    pac2 = z_raportu("a5p_zalogowane.txt", "2906          2557", 2557)
    r(f"   Okres 2: {s2} sesji z wyborem usługi bez zamówienia w 24 godziny ({pac2} pacjentów). Scenariusze, gdyby ścieżka była")
    r("   zepsuta (odczytanie B), przy założeniu, że odzyskane płatności to odrębne, dodatkowe zamówienia:")
    r(f"   - sesje × {100 * p_usl:.1f}% (z wyboru usługi do płatności) × {marza_powt:.2f} zł marży zamówienia powtórnego = {zl(s2 * p_usl * marza_powt)} rocznie;")
    r(f"   - pacjenci zamiast sesji (kilka sesji jednego pacjenta to często ten sam zamiar zakupu): {zl(pac2 * p_usl * marza_powt)} rocznie;")
    r(f"   - wysoki scenariusz × {100 * p_gora:.1f}% (przelicznik z późniejszego kroku, nie formalna górna granica): {zl(s2 * p_gora * marza_powt)} rocznie.")
    r("   Odczytanie A (wizyty „sprawdzam konto”): 0 zł. Część tych zakupów i tak się odbywa później (pacjenci z takimi sesjami")
    r("   wracają częściej niż podobni).")

    naglowek("P6. TELEMEDIGO: ZNIŻKA 20% U SPECJALISTÓW Z CENĄ PO ZNIŻCE PONIŻEJ KOSZTU LEKARZA (c_telemedigo.txt, 3c)")
    t = q(f"""SELECT CASE WHEN created_at < TIMESTAMP '{D.OKRES2}' THEN 1 ELSE 2 END okres, count(*) zamowienia,
                     sum(amount_paid - refund_amount - ({D.KOSZT_LEKARZA}))::DOUBLE marza,
                     sum(CASE WHEN status IN ('completed', 'no_show') THEN list_price - amount_paid ELSE 0 END)::DOUBLE znizka_efektywna
              FROM czyste.orders WHERE discount_type = 'go' AND specialization NOT IN ('internista', 'psychiatra') GROUP BY 1 ORDER BY 1""")
    pokaz(t.round(0))
    ze_strata = q(f"""SELECT sum(-(amount_paid - refund_amount - ({D.KOSZT_LEKARZA})))::DOUBLE z FROM czyste.orders
                       WHERE discount_type = 'go' AND specialization NOT IN ('internista', 'psychiatra')
                         AND created_at >= TIMESTAMP '{D.OKRES2}' AND amount_paid - refund_amount - ({D.KOSZT_LEKARZA}) < 0""").z[0]
    r("   Zmiana warunków (bez zniżki u tych specjalistów), okres 2, scenariusze (nie granice; recenzja Codeksa):")
    r(f"   - znikają wszystkie te zamówienia: {zl(-t.marza[1])} rocznie;")
    r(f"   - znikają tylko zamówienia, które dziś przynoszą stratę: {zl(ze_strata)} rocznie;")
    r(f"   - wszystkie zostają po cenie katalogowej: {zl(t.znizka_efektywna[1])} rocznie;")
    r("   - przy osobnej reakcji przy każdym zamówieniu: od 10 896 do 35 191 zł (c_telemedigo.txt, 3c).")
    z_raportu("c_telemedigo.txt", "10896.0                     35191.0", None)
    r("   Wszystkie bez wpływu na sprzedaż członkostw (część pacjentów może rzadziej kupować TelemediGO).")

    naglowek("P7. gs_generic_specjalisci: WYNIK UJEMNY W OBU REGUŁACH I OBU OKNACH (a5e_kampanie.csv)")
    k = pd.read_csv(os.path.join(WYNIKI, "a5e_kampanie.csv"))
    k = k[(k.kampania == "gs_generic_specjalisci") & (k.okres == 2)]
    rok = k[k.okno_dni == "pelny_rok"].set_index("regula")
    for reg in ("Z1K", "Z2"):
        nowi, wyd = rok.loc[reg, "nowi"], rok.loc[reg, "wydatki_zl"]
        for okno in ("90", "180"):
            w = k[(k.okno_dni == okno) & (k.regula == reg)].iloc[0]
            dz = nowi * w.marza_na_pac - wyd
            r(f"   {reg}, {okno} dni: nowi rocznie {nowi}, wydatki {zl(wyd)}, koszt pozyskania {wyd / nowi:.1f} zł, marża na pacjenta "
              f"{w.marza_na_pac} zł, wynik {zl(dz)}; wyłączyć przy 100% / 50% / 0% dodatkowych: "
              f"{zl(-dz)} / {zl(wyd - 0.5 * nowi * w.marza_na_pac)} / {zl(wyd)}; koszt pozyskania na zero wyniku: {w.marza_na_pac} zł")
    r("   Założenia rachunku „wyłączyć”: ZALOZENIA.md 42 (pacjenci dodatkowi mają średnią marżę przypisanych, pozostali")
    r("   zachowują się jak dziś, koszty pozostałych kanałów bez zmian).")
    r("   Naprawić = obniżyć koszt pozyskania do poziomu marży pacjenta (stawki, słowa kluczowe, strona wejścia) albo podnieść")
    r("   marżę wizyt u specjalistów (cena katalogowa 109–119 zł przy koszcie lekarza 100 zł, c_telemedigo.txt 3a).")

    naglowek("P8. PORANNA PRZEPUSTOWOŚĆ INTERNISTÓW — SCENARIUSZ (a5e_scenariusze.txt, C)")
    for tekst in ("0.76             17419             132         12656", "0.64             19500             125         11931",
                  "1.91             17419             333         31806", "3.50             19500             683         65247"):
        z_raportu("a5e_scenariusze.txt", tekst, None)
    r("   Brak efektu 0 zł; wąski 11 931–12 656 zł; szeroki 31 806–65 247 zł marży w 180 dniach rocznie. Koszt dodatkowej obsady")
    r("   nieznany (koszt lekarza w zadaniu to stawka za wizytę), więc wartości netto nie da się policzyć.")

    naglowek("P9. STRATA MIĘDZY KLIKNIĘCIEM REKLAMY A SESJĄ W META I TIKTOKU (a5p_lejek.txt, 6b)")
    z_raportu("a5p_lejek.txt", "23776.0             1434.0               50494.0", None)
    marza_nowe = z_raportu("a5e_ekonomia.txt", "36.3", 36.3)
    r(f"   Górna granica okresu 2: 23 776 sesji, do 1 434 zamówień, 50 494 zł wydatków. Jeśli to porzucenie ładowania strony i da się")
    r(f"   je odzyskać: do 1 434 × {marza_nowe} zł (marża w 90 dniach pacjenta nowych kampanii) = {zl(1434 * marza_nowe)} rocznie.")
    r("   Jeśli to sposób liczenia kliknięć przez platformy: 0 zł (sprawa pomiaru).")

    naglowek("P10. TELEMEDIGO: KOSZT TESTU Z LOSOWYM CZŁONKOSTWEM PRÓBNYM (c_telemedigo.txt, 4d, projekt B)")
    t = q(f"""SELECT count(DISTINCT k.user_id) pacjenci,
                     sum(CASE WHEN z.status IN ('completed', 'no_show')
                              THEN z.list_price * CASE WHEN z.specialization = 'internista' THEN 0.5 ELSE 0.2 END ELSE 0 END)::DOUBLE
                       / count(DISTINCT k.user_id) znizka_na_pacjenta_dni_1_90,
                     sum(CASE WHEN z.status IN ('completed', 'no_show')
                              THEN greatest(z.amount_paid - z.list_price * CASE WHEN z.specialization = 'internista' THEN 0.5 ELSE 0.8 END, 0)
                              ELSE 0 END)::DOUBLE
                       / count(DISTINCT k.user_id) dodatkowy_koszt_na_pacjenta
              FROM koh k LEFT JOIN zam z ON z.user_id = k.user_id AND z.nr > 1
                                         AND date_diff('day', k.d0, z.created_at::DATE) BETWEEN 1 AND 90
              WHERE k.okres = 2 AND k.d0 <= DATE '{KONIEC}' - 90
                AND NOT EXISTS (SELECT 1 FROM czyste.go_memberships g WHERE g.user_id = k.user_id
                                AND date_diff('day', k.d0, g.purchased_at::DATE) BETWEEN 0 AND 90)""")
    pokaz(t.round(2))
    r("   znizka_na_pacjenta = nominalna zniżka TelemediGO od ceny katalogowej; dodatkowy_koszt = różnica wobec dzisiejszej")
    r("   zapłaty (część wizyt ma już inne kody rabatowe, recenzja Codeksa). Koszt lekarza się nie zmienia.")
    for n, tekst in ((487, "potrzeba 487 pacjentów"), (1823, "potrzeba 1 823 pacjentów")):
        z_raportu("c_telemedigo.txt", tekst, None)
        r(f"   {n} pacjentów w grupie próbnej (c_telemedigo.txt, 4d): około {zl(n * t.dodatkowy_koszt_na_pacjenta[0])} dodatkowego kosztu"
          f" (nominalnie {zl(n * t.znizka_na_pacjenta_dni_1_90[0])}) przy obecnym zachowaniu; więcej, jeśli członkostwo wywołuje dodatkowe wizyty.")
    r("   Członkostwo próbne zaczyna się dzień po pierwszym zamówieniu, więc pierwsze zamówienie jest bez zniżki z członkostwa")
    r("   próbnego (inne kody rabatowe nadal obowiązują).")

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Zapisano {WYNIK} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
