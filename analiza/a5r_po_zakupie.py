"""A5 retencja, krok 4b — to, co dzieje się po zakupie, i komunikacja po zakupie a powroty (2026-10-19).

  1. Czas od zapłaty do terminu wizyty (czekanie) i długość wizyty.
  2. Statusy: anulowane, nieodebrane, zwrócone po wizycie — w czasie, według kampanii, usługi i opóźnienia.
  3. Oceny wizyt.
  4. Czy przebieg pierwszej wizyty (opóźnienie, czekanie, status, ocena) tłumaczy spadek powrotu w kampaniach
     obecnych w obu okresach (rozkład jak w a5r_struktura.py).
  5. Newsletter i SMS a powroty na poziomie pacjenta: kontakt z CRM w dniach 1–90, powrót w 24 godziny od
     wejścia z CRM (ZALOZENIA.md 26, przypisanie do ostatniego wejścia), zgoda marketingowa, wolumen wejść w czasie.

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/a5r_po_zakupie.py
Wynik: analiza/wyniki/a5r_po_zakupie.txt
"""

import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
from a5r_punktualnosc import NOWE, zbuduj_wizyty  # noqa: E402
from a5r_struktura import proba, rozklad, tabela_segmentow, zbuduj_atr  # noqa: E402

WYNIK = os.path.join(D.KATALOG, "analiza", "wyniki", "a5r_po_zakupie.txt")
KONIEC = D.KONIEC
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)

CZEK = """CASE WHEN czekanie <= 30 THEN 'a_do_30_min' WHEN czekanie <= 120 THEN 'b_31_120_min'
               WHEN czekanie <= 720 THEN 'c_2_12_godz' ELSE 'd_ponad_12_godz' END"""


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=True, dni_obserwacji=1)
    zbuduj_atr(con)
    zbuduj_wizyty(con)
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def df(sql):
        return con.sql(sql).df()

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    r(f"A5 RETENCJA — PO ZAKUPIE I KOMUNIKACJA PO ZAKUPIE ({dt.datetime.now():%Y-%m-%d %H:%M})")
    r("Definicje z analiza/definicje.py. Nowe kampanie = meta_prosp_l4_szybko i tt_prosp_l4_15min (Z1K).")
    r("Czekanie = umówiony termin − moment zapłaty (minuty). Opóźnienie = start − termin (a5r_punktualnosc.py).")

    # ============ 1. CZEKANIE I DŁUGOŚĆ WIZYTY ============
    r("\n" + "=" * 120)
    r("1. CZEKANIE NA WIZYTĘ I DŁUGOŚĆ WIZYTY")
    r("=" * 120)
    r("1a. Czekanie od zapłaty do terminu, wszystkie zamówienia u internisty, według okresu i pory terminu (minuty)")
    pokaz(df("""
      SELECT okres, pora, count(*) n, round(quantile_cont(czekanie, 0.5)) mediana, round(quantile_cont(czekanie, 0.9)) p90,
             round(100.0 * avg((czekanie > 120)::INT), 1) ponad_2_godz
      FROM wiz WHERE specialization = 'internista' GROUP BY 1, 2 ORDER BY 2, 1"""))
    r("\n1b. Miesięcznie: mediana czekania i odsetek czekających ponad 2 godziny (internista, pacjenci spoza nowych kampanii)")
    pokaz(df("""
      SELECT strftime(created_at, '%Y-%m') miesiac, count(*) n, round(quantile_cont(czekanie, 0.5)) mediana_min,
             round(100.0 * avg((czekanie > 120)::INT), 1) ponad_2_godz,
             round(100.0 * avg((czekanie > 120)::INT) FILTER (WHERE pora = 'a_rano_6_11'), 1) ponad_2_godz_rano
      FROM wiz WHERE specialization = 'internista' AND NOT nowa_z1k GROUP BY 1 ORDER BY 1"""))
    r("\n1c. Długość odbytej wizyty u internisty (minuty) według celu wizyty i grupy pacjenta, okres 2")
    pokaz(df("""
      SELECT visit_purpose, CASE WHEN nowa_z1k THEN 'nowe_kampanie' ELSE 'pozostali' END grupa, count(*) n,
             round(avg(duration_min), 1) sr_dlugosc, round(avg(op), 1) sr_opozn
      FROM wiz
      WHERE specialization = 'internista' AND okres = 2 AND started_at IS NOT NULL GROUP BY 1, 2 ORDER BY 1, 2"""))
    r("     Ten sam cel wizyty w okresie 1 (bez nowych kampanii):")
    pokaz(df("""
      SELECT visit_purpose, count(*) n, round(avg(duration_min), 1) sr_dlugosc, round(avg(op), 1) sr_opozn
      FROM wiz
      WHERE specialization = 'internista' AND okres = 1 AND started_at IS NOT NULL GROUP BY 1 ORDER BY 1"""))
    r("\n1d. Pora terminu wizyt u internisty: udział rano (6–11) według grupy pacjenta i celu, okres 2")
    pokaz(df("""
      SELECT CASE WHEN nowa_z1k THEN 'nowe_kampanie' ELSE 'pozostali' END grupa, visit_purpose, count(*) n,
             round(100.0 * avg((pora = 'a_rano_6_11')::INT), 1) proc_rano
      FROM wiz WHERE specialization = 'internista' AND okres = 2 AND status <> 'cancelled' GROUP BY 1, 2 ORDER BY 1, 2"""))

    # ============ 2. STATUSY ============
    r("\n" + "=" * 120)
    r("2. ANULOWANE, NIEODEBRANE I ZWRÓCONE PO WIZYCIE")
    r("=" * 120)
    r("2a. Miesięcznie, wszystkie zamówienia: odsetek według statusu, osobno pacjenci nowych kampanii i pozostali")
    pokaz(df("""
      SELECT strftime(created_at, '%Y-%m') miesiac,
             count(*) FILTER (WHERE NOT nowa_z1k) n_pozostali,
             round(100.0 * avg((status = 'cancelled')::INT) FILTER (WHERE NOT nowa_z1k), 1) anul_pozost,
             round(100.0 * avg((status = 'no_show')::INT) FILTER (WHERE NOT nowa_z1k), 1) nieodeb_pozost,
             round(100.0 * avg((status = 'refunded')::INT) FILTER (WHERE NOT nowa_z1k), 1) zwrot_po_pozost,
             count(*) FILTER (WHERE nowa_z1k) n_nowe,
             round(100.0 * avg((status = 'cancelled')::INT) FILTER (WHERE nowa_z1k), 1) anul_nowe,
             round(100.0 * avg((status = 'refunded')::INT) FILTER (WHERE nowa_z1k), 1) zwrot_po_nowe
      FROM wiz GROUP BY 1 ORDER BY 1"""))
    r("\n2b. Zwrot po odbytej wizycie: odsetek wizyt odbytych (completed + refunded), według celu, grupy i okresu")
    pokaz(df("""
      SELECT visit_purpose, okres, CASE WHEN nowa_z1k THEN 'nowe_kampanie' ELSE 'pozostali' END grupa,
             count(*) wizyty_odbyte, round(100.0 * avg((status = 'refunded')::INT), 1) proc_zwrot_po_wizycie
      FROM wiz WHERE status IN ('completed', 'refunded') GROUP BY 1, 2, 3 ORDER BY 1, 2, 3"""))
    r("\n2c. Zwrot po wizycie a opóźnienie (wizyty odbyte u internisty, pacjenci spoza nowych kampanii)")
    pokaz(df("""
      SELECT koszyk, okres, count(*) n, round(100.0 * avg((status = 'refunded')::INT), 1) proc_zwrot_po_wizycie,
             round(avg(duration_min), 1) sr_dlugosc
      FROM wiz
      WHERE specialization = 'internista' AND started_at IS NOT NULL AND NOT nowa_z1k GROUP BY 1, 2 ORDER BY 1, 2"""))
    r("\n2d. Pierwsze zamówienie pacjentów nowych kampanii: zwrot po wizycie według celu i kodu rabatowego")
    pokaz(df("""
      SELECT r.kampania, w.visit_purpose, coalesce(z.promo_code, 'brak') kod, count(*) n,
             round(100.0 * avg((w.status = 'refunded')::INT), 1) proc_zwrot_po_wizycie,
             round(100.0 * avg((w.status = 'cancelled')::INT), 1) proc_anulowane
      FROM wiz w JOIN zrodlo r USING (user_id) JOIN zam z USING (order_id)
      WHERE w.nr = 1 AND w.nowa_z1k GROUP BY 1, 2, 3 HAVING count(*) >= 30 ORDER BY 1, 4 DESC"""))

    # ============ 3. OCENY ============
    r("\n" + "=" * 120)
    r("3. OCENY WIZYT (1–5; większość pacjentów nie ocenia)")
    r("=" * 120)
    r("3a. Wizyty odbyte: odsetek ocenionych i średnia ocena według okresu, grupy i opóźnienia (internista)")
    pokaz(df("""
      SELECT okres, CASE WHEN nowa_z1k THEN 'nowe_kampanie' ELSE 'pozostali' END grupa, koszyk, count(*) n,
             round(100.0 * avg((rating IS NOT NULL)::INT), 1) proc_ocenionych, round(avg(rating), 2) sr_ocena,
             round(100.0 * avg((rating <= 2)::INT) FILTER (WHERE rating IS NOT NULL), 1) proc_ocen_1_2
      FROM wiz
      WHERE specialization = 'internista' AND started_at IS NOT NULL GROUP BY 1, 2, 3 ORDER BY 1, 2, 3"""))
    r("\n3b. Wizyty odbyte według statusu: oceny")
    pokaz(df("""
      SELECT status, okres, count(*) n, round(100.0 * avg((rating IS NOT NULL)::INT), 1) proc_ocenionych, round(avg(rating), 2) sr_ocena
      FROM wiz WHERE started_at IS NOT NULL GROUP BY 1, 2 ORDER BY 1, 2"""))

    # ============ 4. ROZKŁAD Z PRZEBIEGIEM PIERWSZEJ WIZYTY ============
    atr = con.sql(f"""
      SELECT a.*, w.koszyk, w.pora, w.op, {CZEK} czek, w.specialization spec,
             CASE WHEN o.rating IS NULL THEN 'bez_oceny' WHEN o.rating <= 2 THEN 'ocena_1_2' WHEN o.rating = 3 THEN 'ocena_3'
                  ELSE 'ocena_4_5' END ocena, u.marketing_consent zgoda
      FROM atr a JOIN wiz w ON w.user_id = a.user_id AND w.nr = 1 JOIN czyste.orders o ON o.order_id = w.order_id
      JOIN czyste.users u ON u.user_id = a.user_id""").df()
    atr["d0"] = pd.to_datetime(atr.d0)
    atr["dni_R2"] = atr.dni_R2.astype(float)
    a90 = proba(atr, 90)
    stare = a90[~a90.kampania.isin(NOWE)]
    r("\n" + "=" * 120)
    r("4. CZY PRZEBIEG PIERWSZEJ WIZYTY TŁUMACZY SPADEK POWROTU W KAMPANIACH OBECNYCH W OBU OKRESACH (90 dni)")
    r("=" * 120)
    for w in ("czek", "ocena", "zgoda"):
        r(f"\n4.{w}")
        pokaz(tabela_segmentow(stare, w))
    r("\n4b. Rozkład zmiany (punkty procentowe), kampanie obecne w obu okresach, Z1K")
    poz = [["kampania", "usluga"], ["kampania", "usluga", "koszyk"], ["kampania", "usluga", "czek"],
           ["kampania", "usluga", "ocena"], ["kampania", "usluga", "zgoda"],
           ["kampania", "usluga", "koszyk", "status1"], ["kampania", "usluga", "koszyk", "czek", "status1"]]
    pokaz(pd.DataFrame([rozklad(stare, p) for p in poz]))
    r("     Ocena jest wystawiana po wizycie, często po decyzji o powrocie; traktujemy ją jako opis, nie przyczynę.")

    # ============ 5. NEWSLETTER I SMS ============
    r("\n" + "=" * 120)
    r("5. NEWSLETTER I SMS A POWROTY NA POZIOMIE PACJENTA")
    r("=" * 120)
    r("   Wejście z CRM = sesja z utm_medium email albo sms przypisana do pacjenta (konto albo jego przeglądarka),")
    r("   po pierwszym zakupie. Powrót „po CRM” = pierwsze nieanulowane zamówienie po pierwszym zakupie, przypisane do")
    r("   ostatniego wejścia z CRM w 24 godzinach przed płatnością (ZALOZENIA.md 26). Widać kliknięcia, nie wysyłki.")
    con.execute("""
      CREATE TEMP TABLE pierwszy_powrot AS
      SELECT k.user_id, arg_min(z.order_id, z.created_at) order_id
      FROM koh k JOIN zam z ON z.user_id = k.user_id AND z.created_at > k.t0 AND z.status <> 'cancelled' GROUP BY 1""")
    crm = con.sql("""
      SELECT k.user_id,
             count(c.session_id) FILTER (WHERE date_diff('day', k.d0, c.ts::DATE) BETWEEN 1 AND 90) wejscia_crm_90,
             count(c.session_id) FILTER (WHERE date_diff('day', k.d0, c.ts::DATE) BETWEEN 1 AND 90
                                         AND c.kampania <> 'crm_go_upsell') wejscia_crm_90_bez_go,
             any_value(rz.kampania) kampania_crm_powrotu
      FROM koh k LEFT JOIN kontakt c ON c.pacjent = k.user_id AND c.kanal = 'crm' AND c.byl_pacjentem
      LEFT JOIN pierwszy_powrot pp ON pp.user_id = k.user_id LEFT JOIN crm_rozl rz ON rz.order_id = pp.order_id
      GROUP BY 1""").df()
    a = a90.merge(crm, on="user_id", how="left")
    a["grupa2"] = np.where(a.kampania.isin(NOWE), "nowe_kampanie", "pozostale")
    a["kontakt"] = (a.wejscia_crm_90 > 0).astype(float)
    a["powrot_crm"] = ((a.y == 1) & a.kampania_crm_powrotu.notna()).astype(float)
    a["powrot_bez_crm"] = ((a.y == 1) & a.kampania_crm_powrotu.isna()).astype(float)
    r("\n5a. Kohorty z pełnym oknem 90 dni (te same dni): kontakt z CRM w dniach 1–90 i źródło powrotu (%)")
    g = a.groupby(["grupa2", "okres"]).agg(n=("user_id", "size"), zgoda=("zgoda", "mean"), kontakt_crm=("kontakt", "mean"),
                                           wejscia_na_pac=("wejscia_crm_90", "mean"), powrot90=("y", "mean"),
                                           powrot_po_crm=("powrot_crm", "mean"), powrot_bez_crm=("powrot_bez_crm", "mean")).reset_index()
    for c in ("zgoda", "kontakt_crm", "powrot90", "powrot_po_crm", "powrot_bez_crm"):
        g[c] = (100 * g[c]).round(1)
    g["wejscia_na_pac"] = g.wejscia_na_pac.round(3)
    pokaz(g)
    r("     zgoda = odsetek z zgodą marketingową; kontakt_crm = co najmniej jedno wejście z CRM w dniach 1–90.")
    r("\n5b. Powrót w 90 dniach według zgody marketingowej i kontaktu z CRM, kampanie obecne w obu okresach")
    st = a[a.grupa2 == "pozostale"]
    g = st.groupby(["zgoda", "kontakt", "okres"]).agg(n=("user_id", "size"), powrot90=("y", "mean")).reset_index()
    g["powrot90"] = (100 * g.powrot90).round(1)
    pokaz(g)
    r("     Pacjent z kontaktem z CRM to pacjent, który kliknął; to samo w sobie zależy od zamiaru zakupu (nie przyczyna).")
    r("\n5c. Rozkład spadku powrotu (kampanie obecne w obu okresach) na powroty po CRM i pozostałe, punkty procentowe")
    for etyk, kol in (("po CRM", "powrot_crm"), ("bez CRM", "powrot_bez_crm")):
        p1, p2 = st[st.okres == 1][kol].mean(), st[st.okres == 2][kol].mean()
        r(f"     {etyk}: {100 * p1:.2f}% wobec {100 * p2:.2f}% ({100 * (p2 - p1):+.2f} punktu)")
    r("\n5d. Kampania CRM, do której trafił pierwszy powrót (kampanie obecne w obu okresach), % pacjentów kohorty")
    g = st.groupby(["okres"]).kampania_crm_powrotu.value_counts().unstack(0).fillna(0)
    g = (100 * g / st.groupby("okres").size()).round(2).reset_index()
    pokaz(g)

    r("\n5e. Wejścia z CRM w czasie: liczba wejść pacjentów po pierwszym zakupie na miesiąc i na 1000 pacjentów,")
    r("    którzy do początku miesiąca kupili co najmniej raz")
    pokaz(df("""
      WITH m AS (SELECT DISTINCT date_trunc('month', ts)::DATE miesiac FROM kontakt WHERE kanal = 'crm'),
           baza AS (SELECT m.miesiac, (SELECT count(*) FROM koh WHERE t0 < m.miesiac) pacjenci FROM m),
           w AS (SELECT date_trunc('month', ts)::DATE miesiac, kampania, count(*) n FROM kontakt
                 WHERE kanal = 'crm' AND byl_pacjentem GROUP BY 1, 2)
      SELECT strftime(b.miesiac, '%Y-%m') miesiac, b.pacjenci,
             sum(n) FILTER (WHERE kampania = 'crm_reactivation') reaktywacja,
             sum(n) FILTER (WHERE kampania = 'crm_recepta_przypomnienie') recepta,
             sum(n) FILTER (WHERE kampania = 'crm_sms_przypomnienie') sms,
             sum(n) FILTER (WHERE kampania = 'crm_go_upsell') go_upsell,
             round(1000.0 * sum(n) / nullif(b.pacjenci, 0), 1) wejscia_na_1000_pacjentow
      FROM baza b LEFT JOIN w USING (miesiac) GROUP BY b.miesiac, b.pacjenci ORDER BY 1"""))
    r("\n5f. Zamówienia nieanulowane do 24 godzin od wejścia z CRM na 1000 wejść (przypisanie do ostatniego wejścia),")
    r("    miesięcznie, bez crm_go_upsell")
    pokaz(df("""
      WITH w AS (SELECT date_trunc('month', ts)::DATE miesiac, count(*) wejscia FROM kontakt
                 WHERE kanal = 'crm' AND byl_pacjentem AND kampania <> 'crm_go_upsell' GROUP BY 1),
           z AS (SELECT date_trunc('month', k.ts)::DATE miesiac, count(*) zam FROM crm_rozl c JOIN kontakt k ON k.session_id = c.wejscie
                 WHERE c.kampania <> 'crm_go_upsell' GROUP BY 1)
      SELECT strftime(miesiac, '%Y-%m') miesiac, wejscia, zam, round(1000.0 * zam / wejscia, 1) zam_na_1000
      FROM w LEFT JOIN z USING (miesiac) ORDER BY 1"""))

    con.close()
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Raport: {os.path.relpath(WYNIK, D.KATALOG)} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
