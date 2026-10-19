"""A5 retencja, krok 4a — punktualność wizyt i obciążenie internistów a powroty (2026-10-19).

Dopisek Kuby po STOP 1: czy spadek powrotu w kampaniach działających w obu latach siedzi w pierwszych wizytach,
które zaczęły się z opóźnieniem (według godziny i specjalizacji, zwłaszcza internista rano), i czy opóźnienia
rosną od startu kampanii Meta na L4 (3.11.2025), przy skokach jej ruchu (17.11, 8.12.2025, 2.01, 19.01.2026)
i od startu TikToka (9.02.2026). Hipoteza Kuby do sprawdzenia: nowe kampanie przeciążyły internistów w godzinach,
w których przychodzą też pozostali pacjenci.

Opóźnienie = faktyczny start wizyty − umówiony termin, w minutach (tylko wizyty, które się odbyły: completed,
refunded). Pora = godzina umówionego terminu (czas polski). Obciążenie = liczba nieanulowanych wizyt u internisty
umówionych na tę samą godzinę zegarową tego samego dnia. „Nowe kampanie” = pacjenci przypisani do
meta_prosp_l4_szybko albo tt_prosp_l4_15min (reguła Z1K; obok Z2 tam, gdzie to zmienia podział).

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/a5r_punktualnosc.py
Wynik: analiza/wyniki/a5r_punktualnosc.txt, analiza/wyniki/a5r_punktualnosc_tygodnie.csv
"""

import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
from a5r_struktura import proba, rozklad, tabela_segmentow, zbuduj_atr  # noqa: E402

WYNIK = os.path.join(D.KATALOG, "analiza", "wyniki", "a5r_punktualnosc.txt")
WYNIK_TYG = os.path.join(D.KATALOG, "analiza", "wyniki", "a5r_punktualnosc_tygodnie.csv")
NOWE = ("meta_prosp_l4_szybko", "tt_prosp_l4_15min")
DATY = {"2025-11-03": "start Meta L4", "2025-11-17": "skok Meta L4", "2025-12-08": "skok Meta L4",
        "2026-01-02": "skok Meta L4", "2026-01-19": "skok Meta L4", "2026-02-09": "start TikTok L4"}
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)

KOSZYK = """CASE WHEN started_at IS NULL THEN 'brak_wizyty'
                 WHEN op <= 5 THEN 'a_do_5_min' WHEN op <= 15 THEN 'b_6_15_min'
                 WHEN op <= 30 THEN 'c_16_30_min' ELSE 'd_ponad_30_min' END"""
PORA = """CASE WHEN h BETWEEN 6 AND 11 THEN 'a_rano_6_11' WHEN h BETWEEN 12 AND 15 THEN 'b_poludnie_12_15'
               WHEN h BETWEEN 16 AND 23 THEN 'c_wieczor_16_23' ELSE 'd_noc_0_5' END"""


def zbuduj_wizyty(con):
    """`wiz`: każde zamówienie z opóźnieniem, porą, obciążeniem godziny u internisty i grupą pacjenta."""
    con.execute(f"""
      CREATE TEMP TABLE wiz0 AS
      SELECT z.order_id, z.user_id, z.nr, z.created_at, z.scheduled_at, z.started_at, z.status, z.specialization,
             z.visit_purpose, z.duration_min, z.rating, date_diff('minute', z.scheduled_at, z.started_at) op,
             date_diff('minute', z.created_at, z.scheduled_at) czekanie, hour(z.scheduled_at) h,
             date_trunc('hour', z.scheduled_at) slot,
             CASE WHEN z.created_at < TIMESTAMP '{D.OKRES2}' THEN 1 ELSE 2 END okres,
             r.kampania IN {NOWE} nowa_z1k, r.kampania_z2 IN {NOWE} nowa_z2
      FROM zam z JOIN zrodlo r USING (user_id)""")
    con.execute("""
      CREATE TEMP TABLE slot_int AS
      SELECT slot, count(*) obciazenie, count(*) FILTER (WHERE nowa_z1k) obc_nowe
      FROM wiz0 WHERE specialization = 'internista' AND status <> 'cancelled' GROUP BY 1""")
    con.execute(f"""
      CREATE TEMP TABLE wiz AS
      SELECT w.*, {KOSZYK} koszyk, {PORA} pora, coalesce(s.obciazenie, 0) obciazenie, coalesce(s.obc_nowe, 0) obc_nowe
      FROM wiz0 w LEFT JOIN slot_int s ON s.slot = w.slot AND w.specialization = 'internista'""")


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False)
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

    r(f"A5 RETENCJA — PUNKTUALNOŚĆ WIZYT I OBCIĄŻENIE INTERNISTÓW ({dt.datetime.now():%Y-%m-%d %H:%M})")
    r("Opóźnienie = start wizyty − umówiony termin (minuty), tylko wizyty odbyte. Pora = godzina terminu.")
    r("Obciążenie = nieanulowane wizyty u internisty umówione na tę samą godzinę tego samego dnia.")
    r("Nowe kampanie = meta_prosp_l4_szybko i tt_prosp_l4_15min (reguła Z1K). Okres = data płatności zamówienia.")

    # ---------- pierwsza wizyta pacjenta: cechy do kohort ----------
    atr = con.sql("""
      SELECT a.*, w.koszyk, w.pora, w.op, w.obciazenie, w.obc_nowe, w.specialization spec, w.czekanie
      FROM atr a JOIN wiz w ON w.user_id = a.user_id AND w.nr = 1""").df()
    atr["d0"] = pd.to_datetime(atr.d0)
    atr["dni_R2"] = atr.dni_R2.astype(float)
    a90 = proba(atr, 90)
    stare = a90[~a90.kampania.isin(NOWE)]
    stare_z2 = a90[~a90.kampania_z2.isin(NOWE)]

    # ============ 1. CZY SPADEK W STARYCH KAMPANIACH SIEDZI W SPÓŹNIONYCH PIERWSZYCH WIZYTACH ============
    r("\n" + "=" * 120)
    r("1. PIERWSZA WIZYTA: OPÓŹNIENIE A POWRÓT W 90 DNIACH (kampanie obecne w obu okresach; te same dni kalendarzowe)")
    r("=" * 120)
    r("1a. Udział pierwszych wizyt według opóźnienia i powrót w 90 dniach w każdym koszyku (%)")
    pokaz(tabela_segmentow(stare, "koszyk"))
    r("\n1b. To samo tylko dla pierwszej wizyty u internisty")
    pokaz(tabela_segmentow(stare[stare.spec == "internista"], "koszyk"))
    r("\n1c. Pierwsza wizyta u internisty według pory terminu: udział i powrót")
    pokaz(tabela_segmentow(stare[stare.spec == "internista"], "pora"))
    r("\n1d. Odsetek pierwszych wizyt u internisty z opóźnieniem ponad 15 i ponad 30 minut, według pory i okresu")
    x = stare[(stare.spec == "internista") & stare.op.notna()].copy()
    x["p15"], x["p30"] = (x.op > 15).astype(float), (x.op > 30).astype(float)
    g = x.groupby(["pora", "okres"]).agg(n=("op", "size"), sr_opozn=("op", "mean"), ponad15=("p15", "mean"),
                                          ponad30=("p30", "mean")).reset_index()
    g[["sr_opozn"]] = g[["sr_opozn"]].round(1)
    g["ponad15"], g["ponad30"] = (100 * g.ponad15).round(1), (100 * g.ponad30).round(1)
    pokaz(g)

    r("\n1f. Pierwsza wizyta u internisty: powrót w 90 dniach według pory i opóźnienia (czy rano spada też na czas)")
    x = stare[stare.spec == "internista"].copy()
    x["pora_koszyk"] = x.pora.str[:7] + " " + x.koszyk
    pokaz(tabela_segmentow(x, "pora_koszyk").sort_values("pora_koszyk"))

    r("\n1e. Rozkład zmiany powrotu w kampaniach obecnych w obu okresach z opóźnieniem pierwszej wizyty jako podziałem")
    r("    (struktura = część różnicy, którą tłumaczy zmiana udziału spóźnionych pierwszych wizyt)")
    poz = [["koszyk"], ["kampania"], ["kampania", "usluga"], ["kampania", "usluga", "koszyk"],
           ["kampania", "usluga", "pora", "koszyk"], ["kampania", "usluga", "znizka", "status1", "koszyk"]]
    pokaz(pd.DataFrame([rozklad(stare, p) for p in poz]))
    r("     To samo przy źródle według sesji płatności (Z2):")
    s2 = stare_z2.assign(kampania=stare_z2.kampania_z2)
    pokaz(pd.DataFrame([rozklad(s2, p) for p in (["koszyk"], ["kampania", "usluga"], ["kampania", "usluga", "koszyk"],
                                                  ["kampania", "usluga", "pora", "koszyk"])]))

    # ============ 2. OPÓŹNIENIA W CZASIE ============
    r("\n" + "=" * 120)
    r("2. OPÓŹNIENIA WIZYT U INTERNISTY W CZASIE (wszystkie wizyty odbyte, według tygodnia terminu)")
    r("=" * 120)
    tyg = df(f"""
      SELECT date_trunc('week', scheduled_at)::DATE tydzien,
             count(*) FILTER (WHERE status <> 'cancelled') wizyty_nieanul,
             count(*) FILTER (WHERE status <> 'cancelled' AND nowa_z1k) wizyty_nowe_kampanie,
             count(*) FILTER (WHERE status <> 'cancelled' AND pora = 'a_rano_6_11') wizyty_rano,
             round(avg(op), 1) sr_opozn,
             round(avg(op) FILTER (WHERE pora = 'a_rano_6_11'), 1) sr_opozn_rano,
             round(100.0 * avg((op > 15)::INT) FILTER (WHERE pora = 'a_rano_6_11'), 1) rano_ponad15,
             round(100.0 * avg((op > 30)::INT) FILTER (WHERE pora = 'a_rano_6_11'), 1) rano_ponad30,
             round(100.0 * avg((op > 15)::INT) FILTER (WHERE pora = 'a_rano_6_11' AND NOT nowa_z1k), 1) rano_ponad15_stare,
             round(100.0 * avg((op > 15)::INT) FILTER (WHERE pora <> 'a_rano_6_11'), 1) pozostale_pory_ponad15,
             round(avg(obciazenie) FILTER (WHERE pora = 'a_rano_6_11' AND status <> 'cancelled'), 2) sr_obciazenie_rano
      FROM wiz WHERE specialization = 'internista' GROUP BY 1 ORDER BY 1""")
    tyg = tyg[tyg.tydzien <= pd.Timestamp("2026-09-28")]
    tyg["zdarzenie"] = tyg.tydzien.map(lambda t: " ".join(v for k, v in DATY.items()
                                                         if pd.Timestamp(k) - pd.Timedelta(days=6) <= t <= pd.Timestamp(k)))
    tyg.to_csv(WYNIK_TYG, index=False, encoding="utf-8")
    pokaz(tyg)

    r("\n2b. Miesięcznie: wizyty u internisty rano, odsetek ponad 15 minut rano i poza rankiem, specjaliści dla porównania")
    t = df("""
      SELECT strftime(scheduled_at, '%Y-%m') miesiac,
             count(*) FILTER (WHERE specialization = 'internista' AND status <> 'cancelled' AND pora = 'a_rano_6_11') int_rano,
             round(100.0 * avg((op > 15)::INT) FILTER (WHERE specialization = 'internista' AND pora = 'a_rano_6_11'), 1) int_rano_ponad15,
             round(100.0 * avg((op > 15)::INT) FILTER (WHERE specialization = 'internista' AND pora <> 'a_rano_6_11'), 1) int_inne_ponad15,
             round(100.0 * avg((op > 15)::INT) FILTER (WHERE specialization <> 'internista'), 1) specjalisci_ponad15,
             round(100.0 * count(*) FILTER (WHERE specialization = 'internista' AND status <> 'cancelled' AND pora = 'a_rano_6_11' AND nowa_z1k)
                   / nullif(count(*) FILTER (WHERE specialization = 'internista' AND status <> 'cancelled' AND pora = 'a_rano_6_11'), 0), 1) rano_udzial_nowych
      FROM wiz WHERE scheduled_at < TIMESTAMP '2026-10-01' GROUP BY 1 ORDER BY 1""")
    pokaz(t)

    # ============ 3. OBCIĄŻENIE A OPÓŹNIENIE ============
    r("\n" + "=" * 120)
    r("3. OBCIĄŻENIE GODZINY A OPÓŹNIENIE (wizyty odbyte u internisty)")
    r("=" * 120)
    r("3a. Średnie opóźnienie i odsetek ponad 15 minut według obciążenia godziny, osobno w okresach")
    t = df("""
      SELECT CASE WHEN obciazenie <= 2 THEN 'a_1_2' WHEN obciazenie <= 4 THEN 'b_3_4' WHEN obciazenie <= 6 THEN 'c_5_6'
                  WHEN obciazenie <= 9 THEN 'd_7_9' WHEN obciazenie <= 14 THEN 'e_10_14' ELSE 'f_15_plus' END obciazenie_godziny,
             okres, count(*) wizyty, round(avg(op), 1) sr_opozn, round(100.0 * avg((op > 15)::INT), 1) ponad15,
             round(100.0 * avg((op > 30)::INT), 1) ponad30
      FROM wiz WHERE specialization = 'internista' AND op IS NOT NULL GROUP BY 1, 2 ORDER BY 1, 2""")
    pokaz(t)
    r("\n3b. To samo według pory terminu (czy rano jest gorzej przy tym samym obciążeniu)")
    t = df("""
      SELECT pora, CASE WHEN obciazenie <= 4 THEN 'a_do_4' WHEN obciazenie <= 9 THEN 'b_5_9' ELSE 'c_10_plus' END obciazenie_godziny,
             count(*) wizyty, round(avg(op), 1) sr_opozn, round(100.0 * avg((op > 15)::INT), 1) ponad15
      FROM wiz WHERE specialization = 'internista' AND op IS NOT NULL GROUP BY 1, 2 ORDER BY 1, 2""")
    pokaz(t)
    r("\n3c. Wizyty pacjentów spoza nowych kampanii: opóźnienie według obciążenia godziny i liczby wizyt z nowych")
    r("    kampanii w tej samej godzinie (okres 2, rano 6–11)")
    t = df("""
      SELECT CASE WHEN obciazenie <= 4 THEN 'a_do_4' WHEN obciazenie <= 9 THEN 'b_5_9' ELSE 'c_10_plus' END obciazenie_godziny,
             CASE WHEN obc_nowe = 0 THEN '0' WHEN obc_nowe <= 2 THEN '1_2' ELSE '3_plus' END wizyty_nowych_w_godzinie,
             count(*) wizyty, round(avg(op), 1) sr_opozn, round(100.0 * avg((op > 15)::INT), 1) ponad15
      FROM wiz WHERE specialization = 'internista' AND op IS NOT NULL AND NOT nowa_z1k AND okres = 2 AND pora = 'a_rano_6_11'
      GROUP BY 1, 2 ORDER BY 1, 2""")
    pokaz(t)
    r("\n3d. Rozkład obciążenia godzin rano u internisty: średnio wizyt na godzinę z terminami, według okresu")
    t = df("""
      SELECT CASE WHEN slot < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres, count(*) godziny_z_wizytami,
             round(avg(obciazenie), 2) sr_obciazenie, round(avg(obc_nowe), 2) sr_z_nowych_kampanii,
             round(quantile_cont(obciazenie, 0.9), 1) obciazenie_p90
      FROM slot_int WHERE hour(slot) BETWEEN 6 AND 11 AND slot < TIMESTAMP '2026-10-01' GROUP BY 1 ORDER BY 1""")
    pokaz(t)

    # ============ 4. MIESIĄCE KOHORT ============
    r("\n" + "=" * 120)
    r("4. KOHORTY MIESIĘCZNE KAMPANII OBECNYCH W OBU OKRESACH: OPÓŹNIENIE PIERWSZEJ WIZYTY I POWRÓT")
    r("=" * 120)
    st = atr[~atr.kampania.isin(NOWE)].copy()
    st["mies"] = st.d0.dt.strftime("%Y-%m")
    st["p15"] = np.where(st.op.notna(), (st.op > 15).astype(float), np.nan)
    st["y90"] = np.where(st.d0 <= pd.Timestamp(D.granice_por(90)[1]), (st.dni_R2 <= 90).astype(float), np.nan)
    st["y30"] = np.where(st.d0 <= pd.Timestamp(D.granice_por(30)[1]), (st.dni_R2 <= 30).astype(float), np.nan)
    m = st.groupby("mies").agg(n=("user_id", "size"), pierwsza_ponad15=("p15", "mean"), powrot30=("y30", "mean"),
                               powrot90=("y90", "mean")).reset_index()
    for c in ("pierwsza_ponad15", "powrot30", "powrot90"):
        m[c] = (100 * m[c]).round(1)
    pokaz(m)
    r("     Powrót tylko dla dojrzałych kohort; miesiąc na granicy dojrzałości liczony z dojrzałych dni.")

    r("\n4b. Kampanie obecne w obu okresach, te same miesiące rok do roku: powrót w 90 dniach w każdym koszyku opóźnienia")
    s = stare.assign(mm=stare.d0.dt.month)
    for etyk, maska in (("listopad–styczeń", s.mm.isin([11, 12, 1])), ("marzec–maj", s.mm.isin([3, 4, 5])),
                        ("październik i luty", s.mm.isin([10, 2])), ("czerwiec", s.mm == 6)):
        r(f"   {etyk}:")
        pokaz(tabela_segmentow(s[maska], "koszyk"))
        d = rozklad(s[maska], ["kampania", "usluga", "koszyk"])
        r(f"     rozkład (kampania x usługa x opóźnienie): zmiana {d['zmiana']}, struktura {d['struktura']}, "
          f"zachowanie {d['zachowanie']} punktu procentowego")

    con.close()
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Raport: {os.path.relpath(WYNIK, D.KATALOG)} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
