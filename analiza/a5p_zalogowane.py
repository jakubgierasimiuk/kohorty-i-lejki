"""A5 (pozyskanie) — pogłębienie sesji zalogowanych od wejścia (2026-10-19).

Sesja zalogowana od wejścia (ZALOZENIA.md 10): konto w sesji, bez kroku 3 (logowanie albo konto), poza zakupem
samego TelemediGO. W danych żadna z nich nie kończy się zakupem konsultacji. Dwa odczytania (DECYZJE.md):
(a) to wizyty „sprawdzam konto”, a do zakupu pacjent i tak przechodzi przez logowanie; (b) ścieżka zakupu dla
zalogowanych jest zepsuta albo inaczej mierzona (krok 3 zapisywany każdemu przy kasie).

Sekcje:
  1. skala i trend;  2. na którym kroku odpadają;  3. z jakich stron i kampanii przychodzą (z CRM);
  4. co pacjent robi po takiej sesji (zakup w innej sesji w ciągu godziny, doby, tygodnia);
  5. czy kupują potem rzadziej niż podobni pacjenci bez takich sesji (punkt kontrolny 30 dni po pierwszym zakupie);
  6. czas między wyborem terminu a krokiem 3 w zakupach pierwszych i powtórnych;
  7. dane wejściowe do wariantu pesymistycznego (lista niewiadomych).
Definicje pacjenta, kohorty, powrotu, źródła i kosztu lekarza: wspólny moduł analiza/definicje.py (tylko import).

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/a5p_zalogowane.py
Wynik: analiza/wyniki/a5p_zalogowane.txt
"""

import datetime as dt
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "a5p_zalogowane.txt")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_rows", 500)


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

    def tab(sql):
        pokaz(df(sql))

    r(f"A5 POZYSKANIE — SESJE ZALOGOWANE OD WEJŚCIA ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Kroki: k1 wybór usługi, k2 wybór terminu, k3 logowanie albo konto, k4 wejście na płatność, k5 płatność przyjęta.")
    r("Zamówienie liczone jak powrót (ZALOZENIA.md 19): nieanulowane, chyba że opis mówi inaczej. Odstępy w UTC.")

    con.execute("""
      CREATE TEMP TABLE ev AS
      SELECT session_id,
             max((event_name = 'service_selected')::INT) k1, max((event_name = 'slot_selected')::INT) k2,
             max((event_name = 'account_completed')::INT) k3, max((event_name = 'payment_succeeded')::INT) k5,
             min(event_at_utc) FILTER (WHERE event_name = 'service_selected') t1,
             min(event_at_utc) FILTER (WHERE event_name = 'slot_selected') t2,
             min(event_at_utc) FILTER (WHERE event_name = 'account_completed') t3
      FROM czyste.events GROUP BY 1""")
    # wszystkie sesje z kontem: zalogowane od wejścia, sesje z krokiem 3 i zakup samego TelemediGO
    con.execute("""
      CREATE TEMP TABLE sk AS
      SELECT s.session_id, s.user_id, s.visitor_id, s.started_at_pl, s.started_at_utc, s.dzien_pl,
             s.device, s.browser, s.os, s.landing_page, ses.kanal, ses.kampania, s.utm_medium,
             CASE WHEN s.dzien_pl < DATE '2025-10-01' THEN 1 ELSE 2 END okres,
             coalesce(e.k1, 0) k1, coalesce(e.k2, 0) k2, coalesce(e.k3, 0) k3, coalesce(e.k5, 0) k5, e.t1, e.t2, e.t3,
             CASE WHEN g.session_id IS NOT NULL THEN 'samo_telemedigo'
                  WHEN coalesce(e.k3, 0) = 0 THEN 'zalogowana_od_wejscia' ELSE 'z_krokiem_3' END typ,
             (SELECT count(*) FROM zam z WHERE z.user_id = s.user_id AND z.created_at < s.started_at_pl) zam_wczesniej,
             o.order_id, o.nr nr_zamowienia
      FROM czyste.sessions s
      JOIN ses USING (session_id)
      LEFT JOIN ev e USING (session_id)
      LEFT JOIN (SELECT DISTINCT session_id FROM czyste.go_memberships WHERE order_id IS NULL) g USING (session_id)
      LEFT JOIN zam o ON o.session_id = s.session_id
      WHERE s.user_id IS NOT NULL""")
    con.execute("CREATE TEMP TABLE zl AS SELECT * FROM sk WHERE typ = 'zalogowana_od_wejscia'")
    # następne zamówienie pacjenta po sesji (w innej sesji), nieanulowane i dowolne
    con.execute("""
      -- brak późniejszego zamówienia = NULL; przy odsetkach zamieniamy go na „nigdy” (coalesce), żeby został w mianowniku
      CREATE TEMP TABLE zl_po AS
      SELECT zl.session_id,
             min(epoch(timezone('Europe/Warsaw', z.created_at)) - epoch(timezone('UTC', zl.started_at_utc)))
               FILTER (WHERE z.status <> 'cancelled') sek_do_zamowienia,
             min(epoch(timezone('Europe/Warsaw', z.created_at)) - epoch(timezone('UTC', zl.started_at_utc))) sek_do_dowolnego
      FROM zl LEFT JOIN zam z ON z.user_id = zl.user_id AND z.created_at > zl.started_at_pl
      GROUP BY 1""")

    # ---------- 1. skala ----------
    r("\n" + "=" * 100)
    r("1. SKALA: SESJE Z KONTEM WEDŁUG TYPU, W KWARTAŁACH")
    r("=" * 100)
    tab("""
      SELECT strftime(date_trunc('quarter', dzien_pl), '%Y-%m') kwartal_od,
             count(*) FILTER (WHERE typ = 'zalogowana_od_wejscia') zalogowane_od_wejscia,
             count(DISTINCT user_id) FILTER (WHERE typ = 'zalogowana_od_wejscia') ich_pacjenci,
             count(*) FILTER (WHERE typ = 'z_krokiem_3' AND zam_wczesniej > 0) z_krokiem_3_pacjenci_powracajacy,
             count(*) FILTER (WHERE typ = 'z_krokiem_3' AND zam_wczesniej > 0 AND k5 = 1) w_tym_z_platnoscia,
             count(*) FILTER (WHERE typ = 'zalogowana_od_wejscia' AND zam_wczesniej = 0) zalogowane_bez_wczesniejszego_zamowienia
      FROM sk GROUP BY 1 ORDER BY 1""")
    tab("""
      SELECT count(*) sesje, count(DISTINCT user_id) pacjenci,
             (SELECT count(DISTINCT user_id) FROM zam WHERE nr = 2) pacjenci_z_co_najmniej_2_zamowieniami,
             round(count(*) / count(DISTINCT user_id), 2) sesji_na_pacjenta
      FROM zl""")
    r("   Sesje pacjentów, którzy już kupowali: albo zalogowana od wejścia (bez kroku 3), albo z krokiem 3.")
    r("   Sesji pacjentów powracających bez konta w danych nie widać (przeglądarka znana z logowania zawsze ma konto).")
    tab("""
      SELECT count(*) FILTER (WHERE s.user_id IS NULL) anonimowe_sesje_w_znanej_przegladarce_po_pierwszym_zakupie,
             count(*) FILTER (WHERE s.user_id IS NOT NULL) sesje_z_kontem_po_pierwszym_zakupie
      FROM ses_pac s JOIN koh k ON k.user_id = s.pacjent AND s.started_at_pl > k.t0""")

    # ---------- 2. kroki ----------
    r("\n" + "=" * 100)
    r("2. NA KTÓRYM KROKU ODPADAJĄ (sesje zalogowane od wejścia wobec sesji z krokiem 3 pacjentów powracających)")
    r("=" * 100)
    tab("""
      SELECT CASE WHEN typ = 'zalogowana_od_wejscia' THEN 'zalogowana od wejscia' ELSE 'z krokiem 3, pacjent powracajacy' END sesja,
             okres, count(*) sesje, sum(k1) k1, sum(k2) k2, sum(k3) k3, sum(k5) k5,
             round(100 * avg(k1), 1) proc_usluga, round(100 * sum(k2) / nullif(sum(k1), 0), 1) proc_termin_z_uslugi,
             round(100 * sum(k5) / count(*), 1) proc_platnosc
      FROM sk WHERE typ = 'zalogowana_od_wejscia' OR (typ = 'z_krokiem_3' AND zam_wczesniej > 0)
      GROUP BY 1, 2 ORDER BY 1, 2""")
    r("   Dla porównania: wszystkie sesje zwykłe osób, które jeszcze nie kupowały — termin wybiera około 70% tych,")
    r("   które wybrały usługę (analiza/wyniki/a5p_lejek.txt, sekcja 2).")
    r("\n2b. Czas od wejścia do wyboru usługi i od usługi do terminu (sekundy, mediana)")
    tab("""
      SELECT typ, count(*) FILTER (WHERE k1 = 1) z_usluga,
             median(epoch(t1) - epoch(started_at_utc)) med_wejscie_usluga,
             median(epoch(t2) - epoch(t1)) med_usluga_termin
      FROM sk WHERE typ IN ('zalogowana_od_wejscia', 'z_krokiem_3') GROUP BY 1 ORDER BY 1""")

    # ---------- 3. strony i kampanie ----------
    r("\n" + "=" * 100)
    r("3. Z JAKICH STRON I KAMPANII PRZYCHODZĄ")
    r("=" * 100)
    r("3a. Strona wejścia: sesje zalogowane od wejścia wobec sesji z krokiem 3 pacjentów powracających (oba okresy)")
    tab("""
      SELECT landing_page strona_wejscia,
             count(*) FILTER (WHERE typ = 'zalogowana_od_wejscia') zalogowane,
             round(100 * count(*) FILTER (WHERE typ = 'zalogowana_od_wejscia')
                   / sum(count(*) FILTER (WHERE typ = 'zalogowana_od_wejscia')) OVER (), 1) proc_zalogowanych,
             round(100 * avg(k1) FILTER (WHERE typ = 'zalogowana_od_wejscia'), 1) proc_z_usluga,
             count(*) FILTER (WHERE typ = 'z_krokiem_3' AND zam_wczesniej > 0) z_krokiem_3_powracajacy,
             round(100 * count(*) FILTER (WHERE typ = 'z_krokiem_3' AND zam_wczesniej > 0)
                   / sum(count(*) FILTER (WHERE typ = 'z_krokiem_3' AND zam_wczesniej > 0)) OVER (), 1) proc_z_krokiem_3
      FROM sk GROUP BY 1 ORDER BY 2 DESC""")
    r("\n3b. Kampania (UTM sesji)")
    tab("""
      SELECT kampania,
             count(*) FILTER (WHERE typ = 'zalogowana_od_wejscia') zalogowane,
             round(100 * count(*) FILTER (WHERE typ = 'zalogowana_od_wejscia')
                   / sum(count(*) FILTER (WHERE typ = 'zalogowana_od_wejscia')) OVER (), 1) proc_zalogowanych,
             round(100 * avg(k1) FILTER (WHERE typ = 'zalogowana_od_wejscia'), 1) proc_z_usluga,
             count(*) FILTER (WHERE typ = 'z_krokiem_3' AND zam_wczesniej > 0) z_krokiem_3_powracajacy,
             round(100 * count(*) FILTER (WHERE typ = 'z_krokiem_3' AND zam_wczesniej > 0)
                   / sum(count(*) FILTER (WHERE typ = 'z_krokiem_3' AND zam_wczesniej > 0)) OVER (), 1) proc_z_krokiem_3
      FROM sk GROUP BY 1 ORDER BY 2 DESC""")
    r("\n3c. Wejścia z newslettera i SMS-ów (kampanie CRM) według typu sesji: wszystkie sesje z tych kampanii,")
    r("    także bez konta. Zakup w ciągu 24 godzin = zamówienie nieanulowane pacjenta w dowolnej sesji (ZALOZENIA.md 26).")
    tab("""
      WITH c AS (SELECT s.session_id, ses.kampania, s.user_id, s.started_at_utc, s.started_at_pl,
                        CASE WHEN g.session_id IS NOT NULL THEN 'samo_telemedigo'
                             WHEN s.user_id IS NULL THEN 'bez_konta'
                             WHEN coalesce(e.k3, 0) = 0 THEN 'zalogowana_od_wejscia' ELSE 'z_krokiem_3' END typ
                 FROM czyste.sessions s JOIN ses USING (session_id) LEFT JOIN ev e USING (session_id)
                 LEFT JOIN (SELECT DISTINCT session_id FROM czyste.go_memberships WHERE order_id IS NULL) g USING (session_id)
                 WHERE s.utm_medium IN ('email', 'sms'))
      SELECT kampania, count(*) wejscia,
             count(*) FILTER (WHERE typ = 'zalogowana_od_wejscia') zalogowane_od_wejscia,
             count(*) FILTER (WHERE typ = 'z_krokiem_3') z_krokiem_3,
             count(*) FILTER (WHERE typ = 'samo_telemedigo') samo_telemedigo,
             count(*) FILTER (WHERE typ = 'bez_konta') bez_konta,
             round(100 * count(*) FILTER (WHERE typ = 'zalogowana_od_wejscia') / count(*), 1) proc_zalogowanych
      FROM c GROUP BY 1 ORDER BY 2 DESC""")
    r("\n3d. Przypomnienie o recepcie (crm_recepta_przypomnienie) i strona /recepta-online: co robią zalogowani od wejścia")
    tab("""
      SELECT CASE WHEN kampania = 'crm_recepta_przypomnienie' THEN 'przypomnienie o recepcie'
                  WHEN landing_page = '/recepta-online' THEN 'strona /recepta-online (inne zrodla)' END grupa,
             count(*) sesje, round(100 * avg(k1), 1) proc_z_usluga, sum(k2) z_terminem,
             round(100 * avg((coalesce(p.sek_do_zamowienia, 1e12) <= 3600)::INT), 1) proc_zamowienie_w_1_godz,
             round(100 * avg((coalesce(p.sek_do_zamowienia, 1e12) <= 86400)::INT), 1) proc_zamowienie_w_24_godz,
             round(100 * avg((coalesce(p.sek_do_zamowienia, 1e12) <= 7 * 86400)::INT), 1) proc_zamowienie_w_7_dni
      FROM zl JOIN zl_po p USING (session_id)
      WHERE kampania = 'crm_recepta_przypomnienie' OR landing_page = '/recepta-online' GROUP BY 1 ORDER BY 1""")

    # ---------- 4. co potem ----------
    r("\n" + "=" * 100)
    r("4. CO PACJENT ROBI PO SESJI ZALOGOWANEJ OD WEJŚCIA: ZAMÓWIENIE W INNEJ SESJI")
    r("=" * 100)
    r("   Odsetek sesji, po których pacjent złożył zamówienie nieanulowane w ciągu 1 godziny, 24 godzin i 7 dni od wejścia.")
    r("   Tylko sesje z pełnymi 7 dniami obserwacji (do 23.09.2026). Według najdalszego kroku w sesji i grupy kampanii.")
    tab("""
      SELECT CASE WHEN k2 = 1 THEN '3: wybrał termin' WHEN k1 = 1 THEN '2: wybrał usługę' ELSE '1: bez kroków' END najdalszy_krok,
             CASE WHEN utm_medium IN ('email', 'sms') THEN 'crm' ELSE 'inne' END zrodlo,
             count(*) sesje,
             round(100 * avg((coalesce(p.sek_do_zamowienia, 1e12) <= 3600)::INT), 1) proc_1_godz,
             round(100 * avg((coalesce(p.sek_do_zamowienia, 1e12) <= 86400)::INT), 1) proc_24_godz,
             round(100 * avg((coalesce(p.sek_do_zamowienia, 1e12) <= 7 * 86400)::INT), 1) proc_7_dni
      FROM zl JOIN zl_po p USING (session_id)
      WHERE dzien_pl <= DATE '2026-09-23' GROUP BY 1, 2 ORDER BY 1, 2""")
    r("\n4b. Po ilu minutach od wejścia pada zamówienie, jeśli pada w ciągu 24 godzin (sesje z wyborem usługi)")
    tab("""
      SELECT CASE WHEN sek_do_zamowienia <= 600 THEN '1: do 10 min' WHEN sek_do_zamowienia <= 3600 THEN '2: 10-60 min'
                  WHEN sek_do_zamowienia <= 6 * 3600 THEN '3: 1-6 godz' ELSE '4: 6-24 godz' END po_ilu,
             count(*) sesje
      FROM zl JOIN zl_po p USING (session_id)
      WHERE k1 = 1 AND sek_do_zamowienia <= 86400 GROUP BY 1 ORDER BY 1""")
    r("\n4b2. Dzień następnego zamówienia nieanulowanego po sesji zalogowanej od wejścia (pełne doby od wejścia, UTC);")
    r("     sesje z pełnymi 14 dniami obserwacji (do 16.09.2026). Odsetek wszystkich takich sesji.")
    tab("""
      SELECT floor(sek_do_zamowienia / 86400)::INT doba_po_wejsciu, count(*) sesje,
             round(100 * count(*) / (SELECT count(*) FROM zl WHERE dzien_pl <= DATE '2026-09-16'), 2) proc_sesji
      FROM zl JOIN zl_po p USING (session_id)
      WHERE dzien_pl <= DATE '2026-09-16' AND sek_do_zamowienia < 14 * 86400 GROUP BY 1 ORDER BY 1""")
    r("\n4b3. Odwrotnie: ile zamówień powtórnych poprzedza sesja zalogowana od wejścia tego pacjenta")
    tab("""
      SELECT count(*) zamowienia_powtorne,
             round(100 * avg((EXISTS (SELECT 1 FROM zl WHERE zl.user_id = z.user_id AND zl.started_at_pl < z.created_at
                                      AND zl.started_at_pl >= z.created_at - INTERVAL 1 DAY))::INT), 1) proc_z_sesja_w_1_dzien_przed,
             round(100 * avg((EXISTS (SELECT 1 FROM zl WHERE zl.user_id = z.user_id AND zl.started_at_pl < z.created_at
                                      AND zl.started_at_pl >= z.created_at - INTERVAL 7 DAY))::INT), 1) proc_z_sesja_w_7_dni_przed,
             round(100 * avg((EXISTS (SELECT 1 FROM zl WHERE zl.user_id = z.user_id AND zl.started_at_pl < z.created_at
                                      AND zl.started_at_pl >= z.created_at - INTERVAL 30 DAY))::INT), 1) proc_z_sesja_w_30_dni_przed
      FROM zam z WHERE z.nr > 1 AND z.status <> 'cancelled' AND z.created_at >= TIMESTAMP '2024-11-01'""")
    r("\n4c. Tło: jak często ci sami pacjenci składają zamówienie w dowolnych 24 godzinach. Liczone jako zamówienia")
    r("    powtórne nieanulowane na pacjento-dzień, wszystkie dni od pierwszego zakupu do 30.09.2026 (także dni z sesją")
    r("    zalogowaną od wejścia; Codex policzył dla dni bez takich sesji 0,364 zamiast 0,375 — różnica pomijalna).")
    tab("""
      WITH p AS (SELECT DISTINCT user_id FROM zl),
           dni AS (SELECT k.user_id, date_diff('day', k.d0, DATE '2026-09-30') dni FROM koh k JOIN p USING (user_id)),
           zz AS (SELECT z.user_id, count(*) n FROM zam z JOIN p USING (user_id) WHERE z.nr > 1 AND z.status <> 'cancelled' GROUP BY 1)
      SELECT sum(dni) pacjento_dni, sum(coalesce(n, 0)) zamowienia_powtorne,
             round(100 * sum(coalesce(n, 0)) / sum(dni), 2) proc_szansa_zamowienia_na_dzien
      FROM dni LEFT JOIN zz USING (user_id)""")

    # ---------- 5. czy kupują rzadziej ----------
    r("\n" + "=" * 100)
    r("5. CZY PACJENCI Z TAKIMI SESJAMI KUPUJĄ POTEM RZADZIEJ NIŻ PODOBNI PACJENCI BEZ NICH")
    r("=" * 100)
    r("   Punkt kontrolny: 30 dni po pierwszym zakupie (dzień kohorty d0, ZALOZENIA.md 16). Pacjenci, którzy w dniach 1–30")
    r("   nie złożyli żadnego zamówienia. Grupa „z sesją”: co najmniej jedna sesja zalogowana od wejścia w dniach 1–30.")
    r("   Wynik: powrót (zamówienie nieanulowane) w dniach 31–90. Tylko kohorty do 2.07.2026 (pełne 90 dni).")
    r("   Podobni = te same warstwy: okres, zgoda marketingowa, cel i status pierwszego zamówienia, kanał pozyskania (Z1K).")
    r("   stand_bez_sesji = wynik grupy bez sesji przeliczony na strukturę warstw grupy z sesją (standaryzacja bezpośrednia).")
    r("   Uwaga: odwiedzenie strony samo w sobie świadczy o zainteresowaniu; przy innych równych warunkach grupa z sesją")
    r("   powinna kupować częściej. Porównanie nie rozstrzyga przyczyny.")

    def punkt_kontrolny(L, koniec_wyniku, ostatnia_kohorta):
        con.execute(f"""
          CREATE OR REPLACE TEMP TABLE pk AS
          WITH pierwsze AS (SELECT z.user_id, z.visit_purpose cel, z.status status_pierwszego FROM zam z WHERE nr = 1),
               baza AS (SELECT k.user_id, k.d0, k.okres, u.marketing_consent zgoda, p.cel, p.status_pierwszego,
                               coalesce(zr.kanal, 'brak') kanal
                        FROM koh k JOIN czyste.users u USING (user_id) JOIN pierwsze p USING (user_id)
                        LEFT JOIN zrodlo zr USING (user_id)
                        WHERE k.d0 <= DATE '{ostatnia_kohorta}'
                          AND NOT EXISTS (SELECT 1 FROM zam z WHERE z.user_id = k.user_id AND z.nr > 1
                                          AND date_diff('day', k.d0, z.created_at::DATE) BETWEEN 1 AND {L})),
               ekspo AS (SELECT b.user_id, count(zl.session_id) sesje
                         FROM baza b LEFT JOIN zl ON zl.user_id = b.user_id
                           AND date_diff('day', b.d0, zl.dzien_pl) BETWEEN 1 AND {L}
                         GROUP BY 1),
               wyn AS (SELECT b.user_id, max((z.status <> 'cancelled'
                                              AND date_diff('day', b.d0, z.created_at::DATE) BETWEEN {L + 1} AND {koniec_wyniku})::INT) powrot
                       FROM baza b LEFT JOIN zam z ON z.user_id = b.user_id AND z.nr > 1 GROUP BY 1)
          SELECT b.*, e.sesje > 0 z_sesja, coalesce(w.powrot, 0) powrot
          FROM baza b JOIN ekspo e USING (user_id) JOIN wyn w USING (user_id)""")
        w = df("""
          SELECT okres, zgoda, cel, status_pierwszego, kanal, z_sesja, count(*) n, sum(powrot) powroty
          FROM pk GROUP BY ALL""")
        wyniki = []
        for nazwa, filtr in (("oba okresy", w["okres"] > 0), ("okres 1", w["okres"] == 1), ("okres 2", w["okres"] == 2)):
            x = w[filtr]
            warstwy = ["okres", "zgoda", "cel", "status_pierwszego", "kanal"]
            e = x[x["z_sesja"]].groupby(warstwy)[["n", "powroty"]].sum()
            c = x[~x["z_sesja"]].groupby(warstwy)[["n", "powroty"]].sum()
            wsp = e.join(c, lsuffix="_e", rsuffix="_c", how="inner")
            wsp = wsp[wsp["n_c"] >= 5]
            stand = (wsp["n_e"] * wsp["powroty_c"] / wsp["n_c"]).sum() / wsp["n_e"].sum()
            wyniki.append({"grupa": nazwa, "pacjenci_z_sesja": int(e["n"].sum()), "pacjenci_bez_sesji": int(c["n"].sum()),
                           "powrot_z_sesja_proc": round(100 * e["powroty"].sum() / e["n"].sum(), 1),
                           "powrot_bez_sesji_proc": round(100 * c["powroty"].sum() / c["n"].sum(), 1),
                           "z_sesja_w_warstwach_wspolnych_proc": round(100 * wsp["powroty_e"].sum() / wsp["n_e"].sum(), 1),
                           "stand_bez_sesji_proc": round(100 * stand, 1),
                           "pacjenci_z_sesja_w_warstwach_wspolnych": int(wsp["n_e"].sum())})
        return pd.DataFrame(wyniki)

    r("\n5a. Punkt kontrolny 30 dni, wynik w dniach 31–90")
    pokaz(punkt_kontrolny(30, 90, "2026-07-02"))
    r("\n5b. Sprawdzenie wrażliwości: punkt kontrolny 60 dni, wynik w dniach 61–120 (kohorty do 2.06.2026)")
    pokaz(punkt_kontrolny(60, 120, "2026-06-02"))
    r("\n5c. Według liczby sesji zalogowanych od wejścia w dniach 1–30 i według tego, czy w sesji wybrano usługę")
    punkt_kontrolny(30, 90, "2026-07-02")
    tab("""
      WITH u AS (SELECT pk.user_id, max(zl.k1) wybral_usluge
                 FROM pk JOIN zl ON zl.user_id = pk.user_id AND date_diff('day', pk.d0, zl.dzien_pl) BETWEEN 1 AND 30 GROUP BY 1),
           s AS (SELECT pk.user_id, count(zl.session_id) n FROM pk LEFT JOIN zl ON zl.user_id = pk.user_id
                   AND date_diff('day', pk.d0, zl.dzien_pl) BETWEEN 1 AND 30 GROUP BY 1)
      SELECT CASE WHEN s.n = 0 THEN '0 sesji' WHEN s.n = 1 THEN '1 sesja' ELSE '2 i więcej' END sesje_w_dniach_1_30,
             coalesce(u.wybral_usluge, 0) wybral_usluge, count(*) pacjenci, round(100 * avg(pk.powrot), 1) powrot_31_90_proc
      FROM pk JOIN s USING (user_id) LEFT JOIN u USING (user_id) GROUP BY 1, 2 ORDER BY 1, 2""")

    # ---------- 6. czas wybór terminu -> krok 3 ----------
    r("\n" + "=" * 100)
    r("6. CZAS MIĘDZY WYBOREM TERMINU A KROKIEM 3 (sekundy, UTC): ZAKUPY PIERWSZE WOBEC POWTÓRNYCH")
    r("=" * 100)
    r("   Kilkadziesiąt sekund wskazuje na prawdziwe logowanie; 1–2 sekundy raczej na automatyczny zapis kroku.")
    tab("""
      SELECT CASE WHEN nr_zamowienia = 1 THEN '1: pierwsze zamowienie' WHEN nr_zamowienia > 1 THEN '2: zamowienie powtorne'
                  ELSE '3: bez zamowienia' END rodzaj,
             count(*) sesje, min(epoch(t3) - epoch(t2)) min_s,
             quantile_cont(epoch(t3) - epoch(t2), 0.01) p1_s, quantile_cont(epoch(t3) - epoch(t2), 0.1) p10_s,
             median(epoch(t3) - epoch(t2)) mediana_s, quantile_cont(epoch(t3) - epoch(t2), 0.9) p90_s,
             round(100 * avg((epoch(t3) - epoch(t2) <= 2)::INT), 2) proc_do_2_s,
             round(100 * avg((epoch(t3) - epoch(t2) <= 10)::INT), 2) proc_do_10_s
      FROM sk WHERE typ = 'z_krokiem_3' AND k2 = 1 GROUP BY 1 ORDER BY 1""")
    r("\n6b. Rozkład w przedziałach (procent sesji z zamówieniem)")
    tab("""
      SELECT CASE WHEN epoch(t3) - epoch(t2) <= 2 THEN '1: 0-2 s' WHEN epoch(t3) - epoch(t2) <= 10 THEN '2: 3-10 s'
                  WHEN epoch(t3) - epoch(t2) <= 30 THEN '3: 11-30 s' WHEN epoch(t3) - epoch(t2) <= 60 THEN '4: 31-60 s'
                  WHEN epoch(t3) - epoch(t2) <= 120 THEN '5: 61-120 s' WHEN epoch(t3) - epoch(t2) <= 300 THEN '6: 121-300 s'
                  ELSE '7: ponad 300 s' END przedzial,
             round(100 * count(*) FILTER (WHERE nr_zamowienia = 1) / sum(count(*) FILTER (WHERE nr_zamowienia = 1)) OVER (), 1) pierwsze,
             round(100 * count(*) FILTER (WHERE nr_zamowienia > 1) / sum(count(*) FILTER (WHERE nr_zamowienia > 1)) OVER (), 1) powtorne
      FROM sk WHERE typ = 'z_krokiem_3' AND order_id IS NOT NULL GROUP BY 1 ORDER BY 1""")
    r("\n6c. Czy w zakupie powtórnym krok 3 to założenie nowego konta (rejestracja w tej sesji)?")
    tab("""
      SELECT count(*) zakupy_powtorne,
             count(*) FILTER (WHERE u.registered_at >= sk.started_at_pl - INTERVAL 1 MINUTE) konto_zalozone_w_tej_sesji
      FROM sk JOIN czyste.users u USING (user_id) WHERE sk.nr_zamowienia > 1""")
    r("\n6d. Odstępy między kolejnymi krokami w zakupach powtórnych i pierwszych (mediana i rozstęp p10–p90, sekundy)")
    tab("""
      SELECT CASE WHEN nr_zamowienia = 1 THEN 'pierwsze' ELSE 'powtorne' END rodzaj,
             median(epoch(t2) - epoch(t1)) med_k1_k2, quantile_cont(epoch(t2) - epoch(t1), 0.1) p10_k1_k2,
             quantile_cont(epoch(t2) - epoch(t1), 0.9) p90_k1_k2,
             median(epoch(t3) - epoch(t2)) med_k2_k3, quantile_cont(epoch(t3) - epoch(t2), 0.1) p10_k2_k3,
             quantile_cont(epoch(t3) - epoch(t2), 0.9) p90_k2_k3
      FROM sk WHERE order_id IS NOT NULL GROUP BY 1 ORDER BY 1""")

    # ---------- 7. dane do wariantu pesymistycznego ----------
    r("\n" + "=" * 100)
    r("7. DANE WEJŚCIOWE DO WARIANTU PESYMISTYCZNEGO (lista niewiadomych; wartość w marży policzymy później)")
    r("=" * 100)
    r("   Wariant pesymistyczny: ścieżka zakupu dla zalogowanych jest zepsuta i część tych sesji to utracone zamówienia.")
    r("   W grze: sesje zalogowane od wejścia, w których pacjent wybrał usługę, a nie złożył zamówienia nieanulowanego")
    r("   w ciągu 24 godzin w innej sesji (te, po których zamówienie padło, uznajemy za uratowane).")
    tab("""
      SELECT okres, count(*) sesje_zalogowane, count(DISTINCT user_id) pacjenci,
             count(*) FILTER (WHERE k1 = 1) z_wyborem_uslugi, count(DISTINCT user_id) FILTER (WHERE k1 = 1) pacjenci_z_wyborem_uslugi,
             count(*) FILTER (WHERE k1 = 1 AND coalesce(p.sek_do_zamowienia, 1e12) > 86400) z_usluga_bez_zamowienia_24h,
             count(DISTINCT user_id) FILTER (WHERE k1 = 1 AND coalesce(p.sek_do_zamowienia, 1e12) > 86400) ich_pacjenci,
             count(*) FILTER (WHERE k2 = 1) z_wyborem_terminu,
             count(*) FILTER (WHERE k2 = 1 AND coalesce(p.sek_do_zamowienia, 1e12) > 86400) z_terminem_bez_zamowienia_24h
      FROM zl JOIN zl_po p USING (session_id) GROUP BY ROLLUP (okres) ORDER BY okres NULLS LAST""")
    r("\n7b. Wskaźniki do przeliczenia sesji na zamówienia (sesje zwykłe, dwa lata; analiza/wyniki/a5p_lejek.txt):")
    tab("""
      WITH s AS (SELECT * FROM sk WHERE typ = 'z_krokiem_3' AND zam_wczesniej > 0)
      SELECT round(100 * sum(k5) / count(*), 1) powracajacy_k5_na_sesje_z_krokiem_3,
             (SELECT round(100 * sum(e.k5) / sum(e.k1), 1) FROM ev e JOIN czyste.sessions s2 USING (session_id)
              WHERE s2.user_id IS NULL OR e.k3 = 1) wszyscy_k5_na_wybor_uslugi,
             (SELECT round(100 * sum(e.k5) / sum(e.k2), 1) FROM ev e JOIN czyste.sessions s2 USING (session_id)
              WHERE s2.user_id IS NULL OR e.k3 = 1) wszyscy_k5_na_wybor_terminu
      FROM s""")
    r("\n7c. Średnie zamówienie powtórne (nieanulowane i wszystkie), zł: przychód po zwrotach i koszt lekarza (bez TelemediGO)")
    tab(f"""
      SELECT CASE WHEN created_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres, count(*) zamowienia_powtorne,
             round(avg(amount_paid - refund_amount), 2) sredni_przychod_po_zwrotach_zl,
             round(avg({D.KOSZT_LEKARZA}), 2) sredni_koszt_lekarza_zl,
             round(avg(amount_paid - refund_amount - ({D.KOSZT_LEKARZA})), 2) srednia_marza_zl,
             round(avg(amount_paid - refund_amount - ({D.KOSZT_LEKARZA})) FILTER (WHERE status <> 'cancelled'), 2) srednia_marza_nieanulowane_zl
      FROM zam WHERE nr > 1 GROUP BY 1 ORDER BY 1""")

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Zapisano {WYNIK} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
