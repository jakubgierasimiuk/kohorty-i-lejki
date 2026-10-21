"""D — retencja i obsługa pacjenta: sześć sprawdzeń do poprawek po konsylium końcowej weryfikacji (2026-10-21).

Lista Kuby (notatki/d_poprawki.md, punkty 2, 6, 9 i 10) i przeliczenia członków zespołu do potwierdzenia naszym kodem:
  1. opóźnienia wizyt według godziny terminu: czy południe i noc łapią tylko brzegi porannego bloku;
  2. poranek: według godziny, pierwsza wizyta dnia wobec kolejnych, kolejność w porannym bloku, obciążenie godziny;
  3. powrót w 90 dniach według pierwszej usługi (pediatra, psychiatra, L4, e-recepta, inni specjaliści) z 95% przedziałem;
  4. kolejne zamówienia na pacjenta w 90 dniach od pierwszego;
  5. demografia (wiek, płeć, wielkość miejscowości, województwo) a wniosek o retencji, ze standaryzacją;
  6. konta bez żadnego zakupu.

Definicje: analiza/definicje.py (ZALOZENIA.md 16–27). Opóźnienie, pora i obciążenie z analiza/a5r_punktualnosc.py
(ZALOZENIA.md 37): opóźnienie = faktyczny start − umówiony termin w minutach co do sekundy, tylko wizyty odbyte
(completed, refunded); obciążenie = nieanulowane wizyty u internisty z terminem w tej samej godzinie zegarowej tego dnia.
Okres wizyty w punktach 1–2 = dzień umówionego terminu (tak liczy tabela punktualności na stronie, analiza/b_eksport.py);
okres pacjenta w punktach 3–5 = dzień pierwszej płatności (kohorta). „Nowe kampanie” = meta_prosp_l4_szybko
i tt_prosp_l4_15min, według przyjętej reguły źródła (Z1K) i według sesji płatności (Z2). Powroty i kolejne zamówienia
porównujemy na tych samych dniach kalendarzowych (okres 1: kohorty 1.10.2024–2.07.2025, okres 2: 1.10.2025–2.07.2026,
ZALOZENIA.md 27). Przedział 95% różnicy dwóch odsetków: przybliżenie normalne.

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/d_retencja.py
Wynik: analiza/wyniki/d_retencja.txt (raport) i analiza/wyniki/d_retencja.json (najważniejsze liczby, płaski słownik).
"""

import datetime as dt
import json
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
import a5r_punktualnosc as RP  # noqa: E402  (zbuduj_wizyty, PORA, NOWE — ZALOZENIA.md 37)
from a5r_struktura import GRUPA, USLUGA  # noqa: E402

WYNIK = os.path.join(D.KATALOG, "analiza", "wyniki", "d_retencja.txt")
WYNIK_JSON = os.path.join(D.KATALOG, "analiza", "wyniki", "d_retencja.json")
NOWE = RP.NOWE
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

POP = {"wszyscy": "TRUE", "spoza_nowych_z1k": "NOT nowa_z1k", "spoza_nowych_z2": "NOT nowa_z2"}
SPEC = {"internista": "specialization = 'internista'", "pozostali_lekarze": "specialization <> 'internista'"}
SEGMENTY = {"rano_6_11": range(6, 12), "poludnie_12_15": range(12, 16), "wieczor_16_23": range(16, 24),
            "noc_0_5": range(0, 6), "godz_12": [12], "poludnie_bez_12_czyli_13_15": [13, 14, 15],
            "poludnie_14_15": [14, 15], "godz_5": [5], "noc_bez_5_czyli_0_4": [0, 1, 2, 3, 4], "noc_0_3": [0, 1, 2, 3],
            "godz_13": [13], "poza_5_13_czyli_0_4_i_14_23": [0, 1, 2, 3, 4] + list(range(14, 24))}
ZAKRESY = [("okres_1", "okres_t = 1"), ("okres_2", "okres_t = 2"),
           ("II_IX_2025", "scheduled_at >= TIMESTAMP '2025-02-01' AND scheduled_at < TIMESTAMP '2025-10-01'"),
           ("II_IX_2026", "scheduled_at >= TIMESTAMP '2026-02-01' AND scheduled_at < TIMESTAMP '2026-10-01'")]
USLUGI = ["pediatra", "psychiatra", "internista_l4", "internista_e_recepta", "inny_specjalista",
          "internista_konsultacja", "internista_skierowanie"]

J = {}


def zapisz(klucz, wartosc):
    """Liczba do pliku JSON: całkowite bez zmian, ułamki z 4 miejscami; brak wartości (NaN) pomijamy."""
    klucz = klucz.lower()
    if wartosc is None:
        return
    if isinstance(wartosc, (bool, np.bool_)):
        wartosc = int(wartosc)
    if isinstance(wartosc, (int, np.integer)):
        J[klucz] = int(wartosc)
        return
    w = float(wartosc)
    if math.isnan(w):
        return
    J[klucz] = int(w) if w.is_integer() else round(w, 4)


def por2(n1, k1, n2, k2):
    """Dwa odsetki: wartości w %, różnica w punktach procentowych, 95% przedział (przybliżenie normalne), z."""
    n1, k1, n2, k2 = int(n1), int(k1), int(n2), int(k2)
    if n1 == 0 or n2 == 0:
        return {"n_o1": n1, "p_o1": np.nan, "n_o2": n2, "p_o2": np.nan, "zmiana_pkt": np.nan, "od": np.nan,
                "do": np.nan, "z": np.nan}
    p1, p2 = k1 / n1, k2 / n2
    d = p2 - p1
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return {"n_o1": n1, "p_o1": 100 * p1, "n_o2": n2, "p_o2": 100 * p2, "zmiana_pkt": 100 * d,
            "od": 100 * (d - 1.96 * se), "do": 100 * (d + 1.96 * se), "z": d / se if se > 0 else np.nan}


def werdykt(od, do):
    if od > 0:
        return "rosnie"
    if do < 0:
        return "spada"
    return "bez istotnej zmiany"


def zaokr(ramka, miejsca=1):
    r = ramka.copy()
    for c in r.columns:
        if pd.api.types.is_float_dtype(r[c]):
            r[c] = r[c].round(miejsca)
    return r


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=False)
    RP.zbuduj_wizyty(con)
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def q(sql):
        return con.sql(sql).df()

    def pokaz(ramka, wciecie="     ", miejsca=1):
        for linia in zaokr(ramka, miejsca).to_string(index=False).splitlines():
            r(wciecie + linia)

    def naglowek(t):
        r("\n" + "=" * 120)
        r(t)
        r("=" * 120)

    r(f"D — RETENCJA I OBSŁUGA PACJENTA: SZEŚĆ SPRAWDZEŃ PO KONSYLIUM ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Okres 1 = 1.10.2024–30.09.2025, okres 2 = 1.10.2025–30.09.2026 (czas polski). Wizyty (punkty 1–2): okres według dnia")
    r("terminu; opóźnienie = start − termin w minutach, tylko wizyty odbyte. Pacjenci (punkty 3–5): okres według dnia pierwszej")
    r("płatności, powrót = kolejne zamówienie nieanulowane, okresy na tych samych dniach kalendarzowych (kohorty do 2.07).")
    r("„Nowe kampanie” = meta_prosp_l4_szybko i tt_prosp_l4_15min; Z1K = przyjęta reguła źródła, Z2 = sesja płatności.")
    r("Odsetki w %, zmiany w punktach procentowych (pkt), od/do = 95% przedział różnicy (przybliżenie normalne).")

    con.execute(f"""
      CREATE TEMP TABLE wt AS
      SELECT *, CASE WHEN scheduled_at < TIMESTAMP '{D.OKRES2}' THEN 1
                     WHEN scheduled_at < TIMESTAMP '2026-10-01' THEN 2 END okres_t,
             minute(scheduled_at) mi, scheduled_at::DATE dzien
      FROM wiz""")

    # =====================================================================================================
    # 1. OPÓŹNIENIA WEDŁUG GODZINY TERMINU
    # =====================================================================================================
    naglowek("1. OPÓŹNIENIA WIZYT WEDŁUG GODZINY TERMINU (0–23), OKRES 1 WOBEC OKRESU 2")
    r("n = wizyty odbyte; p15/p30 = % spóźnionych ponad 15/30 minut; sr/med = średnie i mediana opóźnienia w minutach.")
    r(f"Poza okresami: {int(q('SELECT count(*) FROM wt WHERE okres_t IS NULL AND op IS NOT NULL').iloc[0, 0])} wizyt odbytych"
      " z terminem od 1.10.2026 (pominięte).")

    def godziny(spec_w, pop_w):
        return q(f"""
          SELECT h, okres_t okres, count(*) n, count(*) FILTER (WHERE op > 15) k15, count(*) FILTER (WHERE op > 30) k30,
                 sum(op) s_op, median(op) med
          FROM wt WHERE op IS NOT NULL AND okres_t IS NOT NULL AND {spec_w} AND {pop_w} GROUP BY ALL ORDER BY 1, 2""")

    def tabela_godzin(t):
        t = t.assign(p15=100 * t.k15 / t.n, p30=100 * t.k30 / t.n, sr=t.s_op / t.n)
        pv = t.pivot(index="h", columns="okres", values=["n", "p15", "p30", "sr", "med"])
        pv.columns = [f"{a}_o{b}" for a, b in pv.columns]
        pv = pv.reindex(columns=[f"{a}_o{o}" for a in ("n", "p15", "p30", "sr", "med") for o in (1, 2)]).reset_index()
        pv["n_o1"], pv["n_o2"] = pv.n_o1.fillna(0).astype(int), pv.n_o2.fillna(0).astype(int)
        pv["zmiana_p15"] = pv.p15_o2 - pv.p15_o1
        return pv

    def segmenty(t):
        wiersze = []
        for nazwa, godz in SEGMENTY.items():
            x = t[t.h.isin(list(godz))].groupby("okres")[["n", "k15", "k30", "s_op"]].sum()
            if 1 not in x.index or 2 not in x.index:
                continue
            c = por2(x.loc[1, "n"], x.loc[1, "k15"], x.loc[2, "n"], x.loc[2, "k15"])
            wiersze.append({"segment": nazwa, "n_o1": c["n_o1"], "p15_o1": c["p_o1"], "n_o2": c["n_o2"], "p15_o2": c["p_o2"],
                            "zmiana_pkt": c["zmiana_pkt"], "od": c["od"], "do": c["do"],
                            "p30_o1": 100 * x.loc[1, "k30"] / x.loc[1, "n"], "p30_o2": 100 * x.loc[2, "k30"] / x.loc[2, "n"],
                            "sr_o1": x.loc[1, "s_op"] / x.loc[1, "n"], "sr_o2": x.loc[2, "s_op"] / x.loc[2, "n"]})
        return pd.DataFrame(wiersze)

    seg_wyn = {}
    for spec, spec_w in SPEC.items():
        for pop, pop_w in POP.items():
            t = godziny(spec_w, pop_w)
            r(f"\n1.{spec} — {pop}: według godziny terminu")
            tg = tabela_godzin(t)
            pokaz(tg)
            s = segmenty(t)
            seg_wyn[(spec, pop)] = s
            r(f"   {spec} — {pop}: pory dnia i pory bez godzin przylegających do poranka (12:00 i 5:00)")
            pokaz(s)
            for _, w in s.iterrows():
                for o in (1, 2):
                    zapisz(f"op_{spec}_{pop}_{w.segment}_ponad15_proc_okres{o}", w[f"p15_o{o}"])
                    zapisz(f"op_{spec}_{pop}_{w.segment}_wizyty_okres{o}", w[f"n_o{o}"])
                    zapisz(f"op_{spec}_{pop}_{w.segment}_srednie_min_okres{o}", w[f"sr_o{o}"])
                zapisz(f"op_{spec}_{pop}_{w.segment}_ponad15_zmiana_pkt", w.zmiana_pkt)
                zapisz(f"op_{spec}_{pop}_{w.segment}_ponad15_zmiana_od", w.od)
                zapisz(f"op_{spec}_{pop}_{w.segment}_ponad15_zmiana_do", w["do"])
            if spec == "internista" and pop in ("wszyscy", "spoza_nowych_z1k"):
                for _, w in tg.iterrows():
                    for o in (1, 2):
                        zapisz(f"op_internista_{pop}_godz{int(w.h):02d}_ponad15_proc_okres{o}", w[f"p15_o{o}"])
                        zapisz(f"op_internista_{pop}_godz{int(w.h):02d}_wizyty_okres{o}", w[f"n_o{o}"])
                        zapisz(f"op_internista_{pop}_godz{int(w.h):02d}_mediana_min_okres{o}", w[f"med_o{o}"])

    s = seg_wyn[("internista", "spoza_nowych_z1k")].set_index("segment")
    r("\n1k. Kontrola zgodności z tekstem strony (internista, pacjenci spoza nowych kampanii Z1K, okres według dnia terminu):")
    r(f"     południe {s.loc['poludnie_12_15', 'p15_o1']:.1f}% z {s.loc['poludnie_12_15', 'n_o1']} → "
      f"{s.loc['poludnie_12_15', 'p15_o2']:.1f}% z {s.loc['poludnie_12_15', 'n_o2']}   [tekst: 3,0% z 2 974 → 8,9% z 3 748]")
    r(f"     noc {s.loc['noc_0_5', 'p15_o1']:.1f}% z {s.loc['noc_0_5', 'n_o1']} → "
      f"{s.loc['noc_0_5', 'p15_o2']:.1f}% z {s.loc['noc_0_5', 'n_o2']}   [tekst: 1,9% z 1 322 → 5,7% z 1 418]")

    r("\n1m. Internista: godziny przy granicach porannego bloku według kwadransa terminu (minuty 0–14, 15–29, 30–44, 45–59),")
    r("    % wizyt spóźnionych ponad 15 minut. Czy opóźnienia o 12:xx i 5:xx skupiają się przy samym poranku.")
    for pop in ("wszyscy", "spoza_nowych_z1k"):
        t = q(f"""
          SELECT h, (mi // 15) * 15 kwadrans, okres_t okres, count(*) n, 100.0 * avg((op > 15)::INT) p15
          FROM wt WHERE op IS NOT NULL AND okres_t IS NOT NULL AND specialization = 'internista' AND {POP[pop]}
                AND h IN (4, 5, 6, 11, 12, 13) GROUP BY ALL""")
        pv = t.pivot(index=["h", "kwadrans"], columns="okres", values=["n", "p15"])
        pv.columns = [f"{a}_o{b}" for a, b in pv.columns]
        pv = pv[["n_o1", "p15_o1", "n_o2", "p15_o2"]].reset_index()
        pv["n_o1"], pv["n_o2"] = pv.n_o1.astype(int), pv.n_o2.astype(int)
        r(f"   {pop}:")
        pokaz(pv)
        for _, w in pv.iterrows():
            if int(w.h) in (5, 12):
                for o in (1, 2):
                    zapisz(f"op_internista_{pop}_godz{int(w.h):02d}_min{int(w.kwadrans):02d}_ponad15_proc_okres{o}", w[f"p15_o{o}"])
                    zapisz(f"op_internista_{pop}_godz{int(w.h):02d}_min{int(w.kwadrans):02d}_wizyty_okres{o}", w[f"n_o{o}"])

    # =====================================================================================================
    # 2. PORANEK
    # =====================================================================================================
    naglowek("2. PORANEK U INTERNISTY (termin 6:00–11:59): GODZINA, PIERWSZA WIZYTA DNIA, KOLEJNOŚĆ, OBCIĄŻENIE")
    r("Zakresy: okres_1 = terminy X 2024 – IX 2025, okres_2 = X 2025 – IX 2026, II_IX_2025 i II_IX_2026 = luty–wrzesień")
    r("(w II–IX 2026 odsetek porannych opóźnień jest około 50%). Wizyty wszystkich pacjentów, o ile nie zaznaczono inaczej.")

    def stat_zakresy(tabela, grupa_sql, warunek="TRUE"):
        out = []
        for nazwa, w in ZAKRESY:
            t = q(f"""
              SELECT {grupa_sql} grupa, count(*) n, count(*) FILTER (WHERE op > 15) k15, 100.0 * avg((op > 15)::INT) p15,
                     100.0 * avg((op > 30)::INT) p30, avg(op) sr, median(op) med
              FROM {tabela} WHERE op IS NOT NULL AND {w} AND {warunek} GROUP BY 1 ORDER BY 1""")
            t.insert(0, "zakres", nazwa)
            out.append(t)
        return pd.concat(out, ignore_index=True)

    r("\n2a. Według godziny terminu 6–11")
    for pop in ("wszyscy", "spoza_nowych_z1k"):
        t = stat_zakresy("wt", "h", f"specialization = 'internista' AND h BETWEEN 6 AND 11 AND {POP[pop]}")
        pv = t.pivot(index="grupa", columns="zakres", values=["n", "p15", "sr", "med"])
        pv.columns = [f"{a}_{b}" for a, b in pv.columns]
        kol = [f"{a}_{z}" for z, _ in ZAKRESY for a in ("n", "p15", "sr", "med")]
        pv = pv[kol].reset_index().rename(columns={"grupa": "godzina"})
        r(f"   {pop}:")
        pokaz(pv)
        for _, w in t.iterrows():
            zapisz(f"ranek_{pop}_godz{int(w.grupa):02d}_{w.zakres}_ponad15_proc", w.p15)
            zapisz(f"ranek_{pop}_godz{int(w.grupa):02d}_{w.zakres}_wizyty", w.n)
            zapisz(f"ranek_{pop}_godz{int(w.grupa):02d}_{w.zakres}_srednie_min", w.sr)
            zapisz(f"ranek_{pop}_godz{int(w.grupa):02d}_{w.zakres}_mediana_min", w.med)
    t2 = stat_zakresy("wt", "h", "specialization = 'internista' AND h BETWEEN 6 AND 11").set_index(["zakres", "grupa"])
    r("     Twierdzenie członka zespołu (okres 2, internista): 6:00 45,4%, 8:00 47,0%, 10:00 40,4%. Nasze (wszyscy, okres 2): "
      + ", ".join(f"{h}:00 {t2.loc[('okres_2', h), 'p15']:.1f}%" for h in (6, 7, 8, 9, 10, 11))
      + "; w II–IX 2026: " + ", ".join(f"{h}:00 {t2.loc[('II_IX_2026', h), 'p15']:.1f}%" for h in (6, 7, 8, 9, 10, 11)) + ".")

    con.execute("""
      CREATE TEMP TABLE ranek AS
      SELECT w.*, row_number() OVER (PARTITION BY dzien ORDER BY scheduled_at, order_id) kol,
             scheduled_at = min(scheduled_at) OVER (PARTITION BY dzien) pierwszy_termin,
             count(*) OVER (PARTITION BY dzien) ruch_dnia,
             date_diff('minute', date_trunc('day', scheduled_at) + INTERVAL 6 HOUR, scheduled_at) termin_min_od_6
      FROM wt w
      WHERE specialization = 'internista' AND pora = 'a_rano_6_11' AND status <> 'cancelled' AND okres_t IS NOT NULL""")
    con.execute("""
      CREATE TEMP TABLE ranek_odb AS
      SELECT r.*, row_number() OVER (PARTITION BY dzien ORDER BY scheduled_at, order_id) kol_odb,
             avg(CASE WHEN pierwszy_termin THEN op END) OVER (PARTITION BY dzien) op_pierwszej
      FROM ranek r WHERE op IS NOT NULL""")
    r("\n2b. Kolejność w porannym bloku dnia: wizyty nieanulowane u internisty z terminem 6:00–11:59 tego dnia, ułożone według")
    r("    terminu (remis rozstrzyga numer zamówienia). Pierwsza wizyta dnia = wszystkie wizyty z najwcześniejszym porannym")
    r("    terminem tego dnia. Opóźnienie liczone tylko dla wizyt odbytych.")
    rem = q("""SELECT count(DISTINCT dzien) dni, count(DISTINCT dzien) FILTER (WHERE pierwszy_termin AND kol = 2) dni_z_remisem_na_pierwszym_terminie
               FROM ranek""")
    pokaz(rem)
    t = q("""
      SELECT CASE WHEN okres_t = 1 THEN 'okres_1' ELSE 'okres_2' END zakres, count(*) dni,
             avg(termin_min_od_6) termin_pierwszej_min_po_6, 100.0 * avg((termin_min_od_6 = 0)::INT) proc_dni_z_pierwsza_o_6_00,
             avg(termin_min_od_6 + op) start_pierwszej_min_po_6, avg(ruch_dnia) sr_ruch_poranny
      FROM ranek WHERE kol = 1 GROUP BY 1 ORDER BY 1""")
    r("     Pierwsza poranna wizyta dnia: termin i faktyczny start (minuty po 6:00; start tylko gdy wizyta odbyta)")
    pokaz(t)
    for _, w in t.iterrows():
        zapisz(f"ranek_pierwsza_wizyta_termin_min_po_6_{w.zakres}", w.termin_pierwszej_min_po_6)
        zapisz(f"ranek_pierwsza_wizyta_start_min_po_6_{w.zakres}", w.start_pierwszej_min_po_6)
        zapisz(f"ranek_dni_{w.zakres}", w.dni)

    r("\n2c. Pierwsza poranna wizyta dnia wobec kolejnych (wszyscy pacjenci)")
    t = stat_zakresy("ranek", "CASE WHEN pierwszy_termin THEN 'a_pierwsza' ELSE 'b_kolejne' END")
    pokaz(t.drop(columns="k15"))
    for _, w in t.iterrows():
        zapisz(f"ranek_{w.grupa[2:]}_{w.zakres}_ponad15_proc", w.p15)
        zapisz(f"ranek_{w.grupa[2:]}_{w.zakres}_wizyty", w.n)
        zapisz(f"ranek_{w.grupa[2:]}_{w.zakres}_srednie_min", w.sr)
        zapisz(f"ranek_{w.grupa[2:]}_{w.zakres}_mediana_min", w.med)
    r("     Kontrola: pierwsza odbyta wizyta dnia (kolejność tylko wśród wizyt odbytych) wobec kolejnych odbytych")
    t = stat_zakresy("ranek_odb", "CASE WHEN kol_odb = 1 THEN 'a_pierwsza_odbyta' ELSE 'b_kolejne' END")
    pokaz(t.drop(columns="k15"))
    for _, w in t[t.grupa == "a_pierwsza_odbyta"].iterrows():
        zapisz(f"ranek_pierwsza_odbyta_{w.zakres}_ponad15_proc", w.p15)
        zapisz(f"ranek_pierwsza_odbyta_{w.zakres}_wizyty", w.n)

    r("     Pierwsza poranna wizyta dnia według jej terminu (gdyby lekarz zaczynał o stałej porze, pierwsza wizyta z terminem")
    r("     o 6:00 byłaby bardziej spóźniona niż pierwsza wizyta z późniejszym terminem):")
    t = stat_zakresy("ranek", """CASE WHEN termin_min_od_6 < 15 THEN 'a_6_00_6_14' WHEN termin_min_od_6 < 30 THEN 'b_6_15_6_29'
                                      WHEN termin_min_od_6 < 60 THEN 'c_6_30_6_59' ELSE 'd_od_7_00' END""", "pierwszy_termin")
    pokaz(t.drop(columns="k15"))
    for _, w in t.iterrows():
        zapisz(f"ranek_pierwsza_termin_{w.grupa[2:]}_{w.zakres}_ponad15_proc", w.p15)
        zapisz(f"ranek_pierwsza_termin_{w.grupa[2:]}_{w.zakres}_wizyty", w.n)
        zapisz(f"ranek_pierwsza_termin_{w.grupa[2:]}_{w.zakres}_srednie_min", w.sr)

    r("\n2d. Według kolejności wizyty w porannym bloku dnia (1., 2.–5., 6.–10., 11. i dalsze)")
    kol_sql = "CASE WHEN kol = 1 THEN 'a_1' WHEN kol <= 5 THEN 'b_2_5' WHEN kol <= 10 THEN 'c_6_10' ELSE 'd_11_plus' END"
    for pop in ("wszyscy", "spoza_nowych_z1k"):
        t = stat_zakresy("ranek", kol_sql, POP[pop])
        r(f"   {pop} (kolejność liczona wśród wszystkich nieanulowanych wizyt, statystyki dla wizyt tej grupy):")
        pokaz(t.drop(columns="k15"))
        for _, w in t.iterrows():
            zapisz(f"ranek_{pop}_kolejnosc_{w.grupa[2:]}_{w.zakres}_ponad15_proc", w.p15)
            zapisz(f"ranek_{pop}_kolejnosc_{w.grupa[2:]}_{w.zakres}_wizyty", w.n)
            zapisz(f"ranek_{pop}_kolejnosc_{w.grupa[2:]}_{w.zakres}_srednie_min", w.sr)
    r("\n2e. Przyrost opóźnienia względem pierwszej wizyty tego samego dnia: średnio (opóźnienie wizyty − średnie opóźnienie")
    r("    odbytych wizyt z pierwszym porannym terminem dnia), minuty; dni, w których pierwsza wizyta się odbyła")
    out = []
    for nazwa, w in ZAKRESY:
        t = q(f"""
          SELECT {kol_sql} grupa, count(*) n, avg(op - op_pierwszej) przyrost_min, avg(op_pierwszej) sr_pierwszej_min,
                 avg(op) sr_min, 100.0 * avg((op - op_pierwszej > 10)::INT) proc_o_ponad_10_min_pozniej
          FROM ranek_odb WHERE NOT pierwszy_termin AND op_pierwszej IS NOT NULL AND {w} GROUP BY 1 ORDER BY 1""")
        t.insert(0, "zakres", nazwa)
        out.append(t)
    t = pd.concat(out, ignore_index=True)
    pokaz(t)
    for _, w in t.iterrows():
        zapisz(f"ranek_przyrost_wzgledem_pierwszej_{w.grupa[2:]}_{w.zakres}_min", w.przyrost_min)
        zapisz(f"ranek_przyrost_wzgledem_pierwszej_{w.grupa[2:]}_{w.zakres}_wizyty", w.n)

    r("\n2f. Według obciążenia godziny (nieanulowane wizyty u internisty z terminem w tej samej godzinie tego dnia; 11 = 11")
    r("    i więcej), wizyty odbyte rano, okres 1 wobec okresu 2 i II–IX 2025 wobec II–IX 2026, wszyscy pacjenci")
    pary = (("okres_1_wobec_2", "okres_t", "TRUE"),
            ("II_IX_2025_wobec_2026", "year(scheduled_at) - 2024",
             "month(scheduled_at) BETWEEN 2 AND 9 AND year(scheduled_at) IN (2025, 2026)"))
    for nazwa, okres_sql, war in pary:
        t = q(f"""
          SELECT least(obciazenie, 11) obciazenie, {okres_sql} o, count(*) n, count(*) FILTER (WHERE op > 15) k15, avg(op) sr
          FROM wt WHERE specialization = 'internista' AND pora = 'a_rano_6_11' AND op IS NOT NULL AND okres_t IS NOT NULL
                AND {war} GROUP BY ALL""")
        pv = t.pivot(index="obciazenie", columns="o", values=["n", "k15", "sr"]).fillna(0)
        pv.columns = [f"{a}_o{b}" for a, b in pv.columns]
        pv["p15_o1"] = 100 * pv.k15_o1 / pv.n_o1.replace(0, np.nan)
        pv["p15_o2"] = 100 * pv.k15_o2 / pv.n_o2.replace(0, np.nan)
        pv["zmiana_pkt"] = pv.p15_o2 - pv.p15_o1
        for c in ("n_o1", "n_o2"):
            pv[c] = pv[c].astype(int)
        r(f"   {nazwa}:")
        pokaz(pv[["n_o1", "p15_o1", "sr_o1", "n_o2", "p15_o2", "sr_o2", "zmiana_pkt"]].reset_index())
        wsp = pv[(pv.n_o1 >= 20) & (pv.n_o2 >= 20)]
        w = wsp.n_o1 + wsp.n_o2
        roz = (wsp.zmiana_pkt * w).sum() / w.sum()
        surowa = 100 * (pv.k15_o2.sum() / pv.n_o2.sum() - pv.k15_o1.sum() / pv.n_o1.sum())
        r(f"     Bez wyrównania różnica {surowa:.1f} pkt; przy tym samym obciążeniu (przedziały z co najmniej 20 wizytami w obu")
        r(f"     okresach, średnia ważona liczbą wizyt): {roz:.1f} pkt ({len(wsp)} przedziałów, {int(w.sum())} wizyt).")
        zapisz(f"ranek_obciazenie_{nazwa}_roznica_surowa_pkt", surowa)
        zapisz(f"ranek_obciazenie_{nazwa}_roznica_przy_tym_samym_obciazeniu_pkt", roz)
        zapisz(f"ranek_obciazenie_{nazwa}_wizyty_w_porownaniu", int(w.sum()))
    r("\n2g. II–IX 2026: obciążenie godziny w obrębie tego samego miesiąca (czy gradient z 2f nie jest różnicą między miesiącami).")
    r("    Obciążenie: niskie 1–3, średnie 4–7, wysokie 8+ wizyt w godzinie; różnica wysokie − niskie liczona w każdym")
    r("    miesiącu i uśredniona z wagą liczby wizyt w obu grupach.")
    t = q("""
      SELECT strftime(scheduled_at, '%Y-%m') miesiac,
             CASE WHEN obciazenie <= 3 THEN 'a_1_3' WHEN obciazenie <= 7 THEN 'b_4_7' ELSE 'c_8_plus' END obc,
             count(*) n, 100.0 * avg((op > 15)::INT) p15
      FROM wt WHERE specialization = 'internista' AND pora = 'a_rano_6_11' AND op IS NOT NULL
            AND scheduled_at >= TIMESTAMP '2026-02-01' AND scheduled_at < TIMESTAMP '2026-10-01' GROUP BY ALL""")
    pv = t.pivot(index="miesiac", columns="obc", values=["n", "p15"])
    pv.columns = [f"{a}_{b}" for a, b in pv.columns]
    pv = pv.reset_index()
    pokaz(pv)
    ok = pv.dropna()
    w = ok["n_a_1_3"] + ok["n_c_8_plus"]
    roz = ((ok["p15_c_8_plus"] - ok["p15_a_1_3"]) * w).sum() / w.sum()
    r(f"     W tym samym miesiącu godziny z 8+ wizytami mają średnio o {roz:.1f} pkt więcej wizyt spóźnionych ponad 15 minut niż")
    r(f"     godziny z 1–3 wizytami ({len(ok)} miesięcy, {int(w.sum())} wizyt).")
    zapisz("ranek_II_IX_2026_w_miesiacu_wysokie_minus_niskie_obciazenie_pkt", roz)
    zapisz("ranek_II_IX_2026_w_miesiacu_wysokie_minus_niskie_obciazenie_wizyty", int(w.sum()))

    # =====================================================================================================
    # 3–5. PACJENCI: DANE WSPÓLNE
    # =====================================================================================================
    con.execute(f"""
      CREATE TEMP TABLE kz AS
      SELECT p.user_id, p.d0, p.okres, p.dni_R2, r.kanal, r.kampania, r.kanal_z2, r.kampania_z2,
             r.kampania IN {NOWE} nowa_z1k, coalesce(r.kampania_z2 IN {NOWE}, FALSE) nowa_z2,
             {USLUGA} usluga, {GRUPA} grupa,
             coalesce(r.kampania_z2 IN ('meta_prosp_lekarz_online', 'meta_prosp_l4_szybko') OR r.kanal_z2 = 'tiktok', FALSE)
               grupa_meta_tiktok_z2
      FROM powr p JOIN zrodlo r USING (user_id, okres) JOIN zam z ON z.user_id = p.user_id AND z.nr = 1""")
    con.execute("""
      CREATE TEMP TABLE kol90 AS
      SELECT k.user_id,
             count(z.order_id) FILTER (WHERE z.status <> 'cancelled' AND date_diff('day', k.d0, z.created_at::DATE) <= 90) kolejne90
      FROM koh k LEFT JOIN zam z ON z.user_id = k.user_id AND z.created_at > k.t0 GROUP BY 1""")
    pac = q("""
      SELECT kz.*, kol90.kolejne90, u.birth_year, u.gender, u.region, u.city_size, u.marketing_consent,
             year(kz.d0) - u.birth_year wiek
      FROM kz JOIN kol90 USING (user_id) JOIN czyste.users u USING (user_id)""")
    n_koh = int(q("SELECT count(*) FROM koh").iloc[0, 0])
    pac["d0"] = pd.to_datetime(pac.d0)
    pac["dni_R2"] = pac.dni_R2.astype(float)
    pac["nowa_z1k"], pac["nowa_z2"] = pac.nowa_z1k.astype(bool), pac.nowa_z2.astype(bool)
    g1, g2 = D.granice_por(90)
    dojr = ((pac.okres == 1) & (pac.d0 <= pd.Timestamp(g1))) | ((pac.okres == 2) & (pac.d0 <= pd.Timestamp(g2)))
    a = pac[dojr].copy()
    a["y"] = (a.dni_R2 <= 90).astype(float)

    def por_y(x, maska):
        x1, x2 = x[maska & (x.okres == 1)], x[maska & (x.okres == 2)]
        return por2(len(x1), x1.y.sum(), len(x2), x2.y.sum())

    # =====================================================================================================
    # 3. POWRÓT WEDŁUG PIERWSZEJ USŁUGI
    # =====================================================================================================
    naglowek("3. POWRÓT W 90 DNIACH WEDŁUG PIERWSZEJ USŁUGI, OKRES 1 WOBEC OKRESU 2 (te same dni kalendarzowe)")
    r(f"Pacjenci: {len(pac)} nowych pacjentów z tabeli kohort ({n_koh} w `koh`); z pełnym oknem 90 dni: okres 1 "
      f"{int((a.okres == 1).sum())}, okres 2 {int((a.okres == 2).sum())}.")
    c = por_y(a, a.okres > 0)
    r(f"Kontrola: wszyscy {c['p_o1']:.1f}% z {c['n_o1']} → {c['p_o2']:.1f}% z {c['n_o2']}   [c_priorytety.txt W2: 23,9% z 12 867 → 17,4% z 18 924]")
    pops3 = (("wszyscy", lambda x: x.okres > 0), ("bez_nowych_z1k", lambda x: ~x.nowa_z1k), ("bez_nowych_z2", lambda x: ~x.nowa_z2))
    wiersze = []
    for u in USLUGI:
        for pop, f in pops3:
            c = por_y(a, (a.usluga == u) & f(a))
            wiersze.append({"usluga": u, "pacjenci": pop, **c, "werdykt": werdykt(c["od"], c["do"])})
    for pop, maska in (("pozostale_kanaly_z1k (bez Meta i TikToka, jak a5r_struktura)", a.grupa == "4_pozostale_kanaly"),
                       ("pozostale_kanaly_z2 (bez Meta i TikToka według sesji płatności)", ~a.grupa_meta_tiktok_z2)):
        c = por_y(a, (a.usluga == "internista_l4") & maska)
        wiersze.append({"usluga": "internista_l4", "pacjenci": pop, **c, "werdykt": werdykt(c["od"], c["do"])})
    t3 = pd.DataFrame(wiersze)
    pokaz(t3, miejsca=2)
    r(f"     Przy 7 usługach porównywanych naraz próg z po poprawce Bonferroniego (5% łącznie) wynosi "
      f"{stats.norm.ppf(1 - 0.05 / 14):.2f}; |z| poniżej tej wartości nie odróżnia się od przypadku przy wielu porównaniach.")
    for _, w in t3.iterrows():
        pk = "pozostale_kanaly_z1k" if w.pacjenci.startswith("pozostale_kanaly_z1k") else (
            "pozostale_kanaly_z2" if w.pacjenci.startswith("pozostale_kanaly_z2") else w.pacjenci)
        k = f"powrot90_{w.usluga}_{pk}"
        for o in (1, 2):
            zapisz(f"{k}_proc_okres{o}", w[f"p_o{o}"])
            zapisz(f"{k}_pacjenci_okres{o}", w[f"n_o{o}"])
        zapisz(f"{k}_zmiana_pkt", w.zmiana_pkt)
        zapisz(f"{k}_zmiana_od", w.od)
        zapisz(f"{k}_zmiana_do", w["do"])
        zapisz(f"{k}_z", w.z)
    r("     Kontrola z modułem definicji (D.stopy_por na tej samej tabeli, bez nowych kampanii Z1K):")
    pokaz(q(D.stopy_por(grupa="usluga", warunek="NOT nowa_z1k", tabela="kz", okna=(90,))))

    # =====================================================================================================
    # 4. KOLEJNE ZAMÓWIENIA W 90 DNIACH
    # =====================================================================================================
    naglowek("4. KOLEJNE ZAMÓWIENIA NA PACJENTA W 90 DNIACH OD PIERWSZEGO (nieanulowane, te same dni kalendarzowe)")
    r("Kolejne zamówienie = zamówienie po pierwszym, nieanulowane, najpóźniej 90. dnia kalendarzowego po dniu kohorty (jak powrót).")
    pops4 = pops3 + (("tylko_nowe_z1k", lambda x: x.nowa_z1k), ("tylko_nowe_z2", lambda x: x.nowa_z2))
    wiersze = []
    for pop, f in pops4:
        m = f(a)
        for o in (1, 2):
            x = a[m & (a.okres == o)]
            if len(x) == 0:
                continue
            wiersze.append({"pacjenci": pop, "okres": o, "n": len(x), "kolejne_na_pacjenta": x.kolejne90.mean(),
                            "proc_co_najmniej_1": 100 * (x.kolejne90 >= 1).mean(),
                            "proc_co_najmniej_2": 100 * (x.kolejne90 >= 2).mean(),
                            "kolejne_na_powracajacego": x.kolejne90[x.kolejne90 >= 1].mean(),
                            "kolejne_razem": int(x.kolejne90.sum())})
    t4 = pd.DataFrame(wiersze)
    pokaz(t4, miejsca=3)
    r("   Zmiana okres 2 − okres 1 (średnia na pacjenta z 95% przedziałem; odsetki w pkt z 95% przedziałem):")
    wiersze = []
    for pop, f in pops3:
        m = f(a)
        x1, x2 = a[m & (a.okres == 1)].kolejne90, a[m & (a.okres == 2)].kolejne90
        d = x2.mean() - x1.mean()
        se = math.sqrt(x1.var() / len(x1) + x2.var() / len(x2))
        c1 = por2(len(x1), (x1 >= 1).sum(), len(x2), (x2 >= 1).sum())
        c2 = por2(len(x1), (x1 >= 2).sum(), len(x2), (x2 >= 2).sum())
        wiersze.append({"pacjenci": pop, "srednia_o1": x1.mean(), "srednia_o2": x2.mean(), "zmiana_sredniej": d,
                        "od": d - 1.96 * se, "do": d + 1.96 * se, "zmiana_proc_wzgl": 100 * (x2.mean() / x1.mean() - 1),
                        "co_najmniej_1_zmiana_pkt": c1["zmiana_pkt"], "co_najmniej_2_zmiana_pkt": c2["zmiana_pkt"],
                        "co_najmniej_2_od": c2["od"], "co_najmniej_2_do": c2["do"]})
        zapisz(f"kolejne90_{pop}_zmiana_sredniej", d)
        zapisz(f"kolejne90_{pop}_zmiana_sredniej_od", d - 1.96 * se)
        zapisz(f"kolejne90_{pop}_zmiana_sredniej_do", d + 1.96 * se)
    pokaz(pd.DataFrame(wiersze), miejsca=3)
    for _, w in t4.iterrows():
        k = f"kolejne90_{w.pacjenci}_okres{w.okres}"
        zapisz(f"{k}_pacjenci", w.n)
        zapisz(f"{k}_srednia_na_pacjenta", w.kolejne_na_pacjenta)
        zapisz(f"{k}_co_najmniej_1_proc", w.proc_co_najmniej_1)
        zapisz(f"{k}_co_najmniej_2_proc", w.proc_co_najmniej_2)
        zapisz(f"{k}_na_powracajacego", w.kolejne_na_powracajacego)
        zapisz(f"{k}_zamowienia_razem", w.kolejne_razem)

    # =====================================================================================================
    # 5. DEMOGRAFIA
    # =====================================================================================================
    naglowek("5. DEMOGRAFIA A WNIOSEK O RETENCJI (wiek, płeć, wielkość miejscowości, województwo)")
    r("Wiek przy pierwszym zamówieniu = rok dnia kohorty − rok urodzenia (w danych jest tylko rok, więc wiek ±1 rok).")
    r("Dane konta opisują właściciela konta; przy wizytach u pediatry to zwykle rodzic, nie dziecko.")
    pac["wiek_gr"] = pd.cut(pac.wiek, [-1, 24, 34, 44, 54, 200], labels=["a_do_24", "b_25_34", "c_35_44", "d_45_54", "e_55_plus"])
    pac["wiek_rec"] = pd.cut(pac.wiek, [-1, 29, 44, 59, 200], labels=["a_do_29", "b_30_44", "c_45_59", "d_60_plus"])
    pac["wiek_rec_l4"] = pd.cut(pac.wiek, [-1, 29, 44, 200], labels=["a_do_29", "b_30_44", "c_45_plus"])
    for c_ in ("wiek_gr", "wiek_rec", "wiek_rec_l4"):
        a[c_] = pac.loc[a.index, c_]
    r(f"Wiek: od {int(pac.wiek.min())} do {int(pac.wiek.max())} lat, braki: {int(pac.wiek.isna().sum())}.")

    r("\n5a. Wiek i cechy nowych pacjentów (wszyscy nowi pacjenci okresu, nie tylko z pełnym oknem)")
    wiersze = []
    for regula in ("z1k", "z2"):
        for o in (1, 2):
            for nowa in (False, True):
                for l4 in (False, True):
                    x = pac[(pac.okres == o) & (pac[f"nowa_{regula}"] == nowa)]
                    if l4:
                        x = x[x.usluga == "internista_l4"]
                    if len(x) == 0:
                        continue
                    wiersze.append({"regula": regula, "okres": o, "grupa": ("nowe_kampanie" if nowa else "reszta"),
                                    "pierwsza_usluga": "tylko_L4" if l4 else "wszystkie", "n": len(x),
                                    "sr_wiek": x.wiek.mean(), "mediana_wieku": x.wiek.median(),
                                    "proc_kobiet": 100 * (x.gender == "K").mean(), "proc_wies": 100 * (x.city_size == "wies").mean(),
                                    "proc_zgoda": 100 * x.marketing_consent.mean()})
    t5a = pd.DataFrame(wiersze)
    pokaz(t5a)
    for _, w in t5a.iterrows():
        k = f"demo_{w.regula}_okres{w.okres}_{w.grupa}_{w.pierwsza_usluga.lower()}"
        zapisz(f"{k}_pacjenci", w.n)
        zapisz(f"{k}_sredni_wiek", w.sr_wiek)
        zapisz(f"{k}_proc_kobiet", w.proc_kobiet)
        zapisz(f"{k}_proc_zgoda_marketingowa", w.proc_zgoda)

    def tabela_demo(x, kol, regula):
        wiersze = []
        for g, xx in x.groupby(kol, observed=True):
            rs = xx[~xx[f"nowa_{regula}"]]
            nw = xx[xx[f"nowa_{regula}"] & (xx.okres == 2)]
            c = por_y(rs, rs.okres > 0)
            wiersze.append({kol: g, "reszta_n_o1": c["n_o1"], "reszta_p_o1": c["p_o1"], "reszta_n_o2": c["n_o2"],
                            "reszta_p_o2": c["p_o2"], "zmiana_pkt": c["zmiana_pkt"], "od": c["od"], "do": c["do"],
                            "nowe_n_o2": len(nw), "nowe_p_o2": 100 * nw.y.mean() if len(nw) else np.nan,
                            "nowe_udzial_o2": 100 * len(nw) / max(len(xx[xx.okres == 2]), 1)})
        return pd.DataFrame(wiersze)

    r("\n5b. Powrót w 90 dniach według grupy (te same dni kalendarzowe): reszta = pacjenci spoza nowych kampanii,")
    r("    okres 1 wobec okresu 2; nowe = pacjenci nowych kampanii (tylko okres 2); nowe_udzial_o2 = ich udział w grupie")
    for kol, opis in (("wiek_gr", "grupa wieku"), ("gender", "płeć"), ("city_size", "wielkość miejscowości"),
                      ("wiek_rec", "grupy wieku członka zespołu")):
        for regula in ("z1k", "z2"):
            t = tabela_demo(a, kol, regula)
            r(f"   {opis}, reguła {regula.upper()}:")
            pokaz(t)
            for _, w in t.iterrows():
                k = f"demo_powrot90_{kol}_{ {'K': 'kobiety', 'M': 'mezczyzni'}.get(w[kol], w[kol])}_{regula}"
                zapisz(f"{k}_reszta_proc_okres1", w.reszta_p_o1)
                zapisz(f"{k}_reszta_pacjenci_okres1", w.reszta_n_o1)
                zapisz(f"{k}_reszta_proc_okres2", w.reszta_p_o2)
                zapisz(f"{k}_reszta_pacjenci_okres2", w.reszta_n_o2)
                zapisz(f"{k}_reszta_zmiana_pkt", w.zmiana_pkt)
                zapisz(f"{k}_reszta_zmiana_od", w.od)
                zapisz(f"{k}_reszta_zmiana_do", w["do"])
                zapisz(f"{k}_nowe_proc_okres2", w.nowe_p_o2)
                zapisz(f"{k}_nowe_pacjenci_okres2", w.nowe_n_o2)

    r("\n5c. Tylko pierwsze L4 u internisty: powrót w 90 dniach według grupy wieku, nowe kampanie wobec reszty (okres 2)")
    a_l4 = a[a.usluga == "internista_l4"]
    for kol in ("wiek_rec_l4", "wiek_gr"):
        for regula in ("z1k", "z2"):
            t = tabela_demo(a_l4, kol, regula)
            r(f"   {kol}, reguła {regula.upper()}:")
            pokaz(t)
            for _, w in t.iterrows():
                k = f"demo_l4_powrot90_{kol}_{w[kol]}_{regula}"
                zapisz(f"{k}_nowe_proc_okres2", w.nowe_p_o2)
                zapisz(f"{k}_nowe_pacjenci_okres2", w.nowe_n_o2)
                zapisz(f"{k}_reszta_proc_okres2", w.reszta_p_o2)
                zapisz(f"{k}_reszta_pacjenci_okres2", w.reszta_n_o2)
                zapisz(f"{k}_reszta_proc_okres1", w.reszta_p_o1)
                zapisz(f"{k}_reszta_pacjenci_okres1", w.reszta_n_o1)

    r("\n5d. Województwa: udział nowych kampanii w nowych pacjentach okresu 2 (wszyscy nowi pacjenci okresu 2) i powrót")
    r("    w 90 dniach pacjentów spoza nowych kampanii, okres 1 wobec okresu 2 (te same dni). z_vs_reszta = różnica zmiany")
    r("    w województwie i zmiany w pozostałych województwach, podzielona przez jej błąd standardowy.")
    r("    z_poziom_o1 / z_poziom_o2 = poziom powrotu w województwie wobec reszty kraju w tym samym okresie (z).")
    p2 = pac[pac.okres == 2]

    def z_poziomu(x, reszta_kraju, o):
        x1, x2 = x[x.okres == o].y, reszta_kraju[reszta_kraju.okres == o].y
        c = por2(len(x2), x2.sum(), len(x1), x1.sum())
        return c["z"]

    for regula in ("z1k", "z2"):
        wiersze = []
        for reg, xx in a.groupby("region"):
            rs = xx[~xx[f"nowa_{regula}"]]
            reszta_kraju = a[(a.region != reg) & ~a[f"nowa_{regula}"]]
            c = por_y(rs, rs.okres > 0)
            cr = por_y(reszta_kraju, reszta_kraju.okres > 0)
            se_r = (c["do"] - c["od"]) / (2 * 1.96)
            se_k = (cr["do"] - cr["od"]) / (2 * 1.96)
            nowi2 = p2[p2.region == reg]
            wiersze.append({"wojewodztwo": reg, "nowi_o2": len(nowi2), "udzial_nowych_kampanii_o2": 100 * nowi2[f"nowa_{regula}"].mean(),
                            "reszta_n_o1": c["n_o1"], "reszta_p_o1": c["p_o1"], "reszta_n_o2": c["n_o2"], "reszta_p_o2": c["p_o2"],
                            "zmiana_pkt": c["zmiana_pkt"], "od": c["od"], "do": c["do"],
                            "z_vs_reszta": (c["zmiana_pkt"] - cr["zmiana_pkt"]) / math.sqrt(se_r ** 2 + se_k ** 2),
                            "z_poziom_o1": z_poziomu(rs, reszta_kraju, 1), "z_poziom_o2": z_poziomu(rs, reszta_kraju, 2)})
        t = pd.DataFrame(wiersze).sort_values("zmiana_pkt")
        r(f"   reguła {regula.upper()}:")
        pokaz(t, miejsca=2)
        tab = pd.crosstab(p2.region, p2[f"nowa_{regula}"])
        chi, pval, dof, _ = stats.chi2_contingency(tab)
        se = (t["do"] - t["od"]) / (2 * 1.96)
        wagi = 1 / se ** 2
        sr = (wagi * t.zmiana_pkt).sum() / wagi.sum()
        Q = (wagi * (t.zmiana_pkt - sr) ** 2).sum()
        pQ = stats.chi2.sf(Q, len(t) - 1)
        prog = stats.norm.ppf(1 - 0.05 / (2 * len(t)))
        r(f"     Udział nowych kampanii: od {t.udzial_nowych_kampanii_o2.min():.1f}% do {t.udzial_nowych_kampanii_o2.max():.1f}%;"
          f" test jednorodności udziałów między województwami: chi2 = {chi:.1f}, df = {dof}, p = {pval:.3f}.")
        r(f"     Zmiana powrotu poza nowymi kampaniami: od {t.zmiana_pkt.min():.1f} do {t.zmiana_pkt.max():.1f} pkt; test jednorodności"
          f" zmian (Q Cochrana) = {Q:.1f}, df = {len(t) - 1}, p = {pQ:.3f}. Próg |z| po poprawce Bonferroniego na {len(t)}"
          f" województw: {prog:.2f}.")
        dln = t.set_index("wojewodztwo").loc["dolnoslaskie"] if "dolnoslaskie" in set(t.wojewodztwo) else None
        if dln is not None:
            r(f"     Dolnośląskie: {dln.reszta_p_o1:.1f}% z {int(dln.reszta_n_o1)} → {dln.reszta_p_o2:.1f}% z {int(dln.reszta_n_o2)},"
              f" zmiana {dln.zmiana_pkt:.1f} pkt (od {dln.od:.1f} do {dln['do']:.1f}), z wobec reszty kraju {dln.z_vs_reszta:.2f};"
              f" udział nowych kampanii {dln.udzial_nowych_kampanii_o2:.1f}% z {int(dln.nowi_o2)}.")
        zapisz(f"demo_wojewodztwa_{regula}_udzial_nowych_min_proc", t.udzial_nowych_kampanii_o2.min())
        zapisz(f"demo_wojewodztwa_{regula}_udzial_nowych_max_proc", t.udzial_nowych_kampanii_o2.max())
        zapisz(f"demo_wojewodztwa_{regula}_udzial_nowych_chi2_p", pval)
        zapisz(f"demo_wojewodztwa_{regula}_zmiana_powrotu_Q", Q)
        zapisz(f"demo_wojewodztwa_{regula}_zmiana_powrotu_Q_p", pQ)
        zapisz(f"demo_wojewodztwa_{regula}_prog_z_bonferroni", prog)
        for _, w in t.iterrows():
            k = f"demo_woj_{w.wojewodztwo.replace('-', '_')}_{regula}"
            zapisz(f"{k}_nowi_pacjenci_okres2", w.nowi_o2)
            zapisz(f"{k}_udzial_nowych_kampanii_proc_okres2", w.udzial_nowych_kampanii_o2)
            zapisz(f"{k}_reszta_powrot90_proc_okres1", w.reszta_p_o1)
            zapisz(f"{k}_reszta_pacjenci_okres1", w.reszta_n_o1)
            zapisz(f"{k}_reszta_powrot90_proc_okres2", w.reszta_p_o2)
            zapisz(f"{k}_reszta_pacjenci_okres2", w.reszta_n_o2)
            zapisz(f"{k}_reszta_zmiana_pkt", w.zmiana_pkt)
            zapisz(f"{k}_z_wobec_reszty_kraju", w.z_vs_reszta)
            zapisz(f"{k}_z_poziomu_okres1_wobec_reszty_kraju", w.z_poziom_o1)
            zapisz(f"{k}_z_poziomu_okres2_wobec_reszty_kraju", w.z_poziom_o2)

    r("\n5e. Standaryzacja: powrót okresu 2 bez nowych kampanii przy strukturze okresu 1 (komórki: grupa wieku × płeć;")
    r("    wariant: grupa wieku × płeć × wielkość miejscowości). Waga komórki = jej udział w okresie 1 (te same dni).")
    wiersze = []
    for regula in ("z1k", "z2"):
        rs = a[~a[f"nowa_{regula}"]]
        for nazwa, komorki in (("wiek_x_plec", ["wiek_gr", "gender"]), ("wiek_x_plec_x_miejscowosc", ["wiek_gr", "gender", "city_size"])):
            g = rs.groupby(komorki + ["okres"], observed=True).y.agg(["count", "mean"]).unstack("okres")
            g = g.dropna()
            w1 = g[("count", 1)] / g[("count", 1)].sum()
            std = 100 * (w1 * g[("mean", 2)]).sum()
            p1 = 100 * rs[rs.okres == 1].y.mean()
            p2_ = 100 * rs[rs.okres == 2].y.mean()
            wiersze.append({"regula": regula, "komorki": nazwa, "liczba_komorek": len(g), "n_o1": int((rs.okres == 1).sum()),
                            "n_o2": int((rs.okres == 2).sum()), "p_o1": p1, "p_o2_surowy": p2_, "p_o2_przy_strukturze_o1": std,
                            "spadek_surowy_pkt": p2_ - p1, "spadek_po_standaryzacji_pkt": std - p1})
            k = f"demo_standaryzacja_{nazwa}_{regula}"
            zapisz(f"{k}_powrot90_okres1_proc", p1)
            zapisz(f"{k}_pacjenci_okres1", int((rs.okres == 1).sum()))
            zapisz(f"{k}_powrot90_okres2_surowy_proc", p2_)
            zapisz(f"{k}_pacjenci_okres2", int((rs.okres == 2).sum()))
            zapisz(f"{k}_powrot90_okres2_przy_strukturze_okresu1_proc", std)
    pokaz(pd.DataFrame(wiersze), miejsca=2)

    # =====================================================================================================
    # 6. KONTA BEZ ŻADNEGO ZAKUPU
    # =====================================================================================================
    naglowek("6. KONTA BEZ ŻADNEGO ZAKUPU (żadnego zamówienia w żadnym statusie)")
    con.execute("""
      CREATE TEMP TABLE konta AS
      SELECT u.user_id, u.registered_at, u.marketing_consent, coalesce(o.n, 0) zamowienia, coalesce(g.n, 0) telemedigo,
             o.pierwsze, coalesce(o.n, 0) = 0 bez_zakupu,
             CASE WHEN u.registered_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres_rej
      FROM czyste.users u
      LEFT JOIN (SELECT user_id, count(*) n, min(created_at) pierwsze FROM czyste.orders GROUP BY 1) o USING (user_id)
      LEFT JOIN (SELECT user_id, count(*) n FROM czyste.go_memberships GROUP BY 1) g USING (user_id)""")
    con.execute("""
      CREATE TEMP TABLE ev_ses AS
      SELECT session_id, bool_or(event_name = 'service_selected') wybor, bool_or(event_name = 'account_completed') konto,
             bool_or(event_name = 'payment_started') platnosc
      FROM czyste.events GROUP BY 1""")
    con.execute("""
      CREATE TEMP TABLE ses_konta AS
      SELECT k.user_id, count(s.session_id) sesje, count(s.session_id) FILTER (WHERE NOT s.anonimowa) sesje_zalogowane,
             count(s.session_id) FILTER (WHERE e.wybor) sesje_wybor_uslugi,
             count(s.session_id) FILTER (WHERE e.konto) sesje_krok_konta,
             count(s.session_id) FILTER (WHERE e.platnosc) sesje_start_platnosci,
             count(s.session_id) FILTER (WHERE s.kanal = 'crm') sesje_crm,
             count(s.session_id) FILTER (WHERE s.kanal = 'crm' AND s.utm_medium = 'email') sesje_newsletter,
             count(s.session_id) FILTER (WHERE s.kanal = 'crm' AND s.utm_medium = 'sms') sesje_sms,
             count(s.session_id) FILTER (WHERE s.kanal = 'crm' AND k.pierwsze IS NOT NULL AND s.started_at_pl < k.pierwsze) sesje_crm_przed_pierwszym_zakupem,
             count(s.session_id) FILTER (WHERE k.pierwsze IS NOT NULL AND s.started_at_pl < k.pierwsze) sesje_przed_pierwszym_zakupem
      FROM konta k LEFT JOIN ses_pac s ON s.pacjent = k.user_id LEFT JOIN ev_ses e ON e.session_id = s.session_id
      GROUP BY 1""")
    t = q("""
      SELECT CASE WHEN bez_zakupu THEN 'a_bez_zakupu' ELSE 'b_z_zakupem' END grupa, count(*) konta,
             100.0 * count(*) / sum(count(*)) OVER () proc_kont,
             sum(telemedigo) telemedigo,
             100.0 * avg(marketing_consent) proc_zgoda,
             100.0 * avg((sesje > 0)::INT) proc_z_sesja,
             100.0 * avg((sesje_zalogowane > 0)::INT) proc_z_sesja_zalogowana,
             100.0 * avg((sesje_wybor_uslugi > 0)::INT) proc_z_wyborem_uslugi,
             100.0 * avg((sesje_krok_konta > 0)::INT) proc_z_krokiem_konta,
             100.0 * avg((sesje_start_platnosci > 0)::INT) proc_ze_startem_platnosci,
             100.0 * avg((sesje_crm > 0)::INT) proc_z_wejsciem_crm,
             100.0 * avg((sesje_newsletter > 0)::INT) proc_z_newsletterem,
             100.0 * avg((sesje_sms > 0)::INT) proc_z_sms,
             100.0 * avg((sesje_crm_przed_pierwszym_zakupem > 0)::INT) proc_z_crm_przed_pierwszym_zakupem,
             sum(sesje_crm) wejscia_crm, avg(sesje) sr_sesji
      FROM konta JOIN ses_konta USING (user_id) GROUP BY 1 ORDER BY 1""")
    pokaz(zaokr(t, 2).set_index("grupa").T.reset_index().rename(columns={"index": "miara"}), miejsca=2)
    for _, w in t.iterrows():
        g = w.grupa[2:]
        for c_ in t.columns[1:]:
            zapisz(f"konta_{g}_{c_}", w[c_])
    zapisz("konta_wszystkie", int(t.konta.sum()))
    bz = q("""SELECT count(*) n, count(*) FILTER (WHERE marketing_consent = 1) zgoda,
                     count(*) FILTER (WHERE marketing_consent = 1 AND sesje_crm = 0) zgoda_bez_crm
              FROM konta JOIN ses_konta USING (user_id) WHERE bez_zakupu""").iloc[0]
    r(f"     Konta bez zakupu ze zgodą marketingową i bez żadnego wejścia z newslettera ani SMS-a: {int(bz.zgoda_bez_crm)} z "
      f"{int(bz.zgoda)}. W danych widać tylko kliknięcia, nie wysyłki: brak wejścia nie dowodzi, że wiadomości nie wysłano.")
    zapisz("konta_bez_zakupu_ze_zgoda_bez_wejscia_crm", int(bz.zgoda_bez_crm))
    zapisz("konta_bez_zakupu_ze_zgoda", int(bz.zgoda))

    r("\n6b. Kiedy założone: okres i kwartał rejestracji (konta, bez zakupu, %)")
    t = q("""
      SELECT okres_rej okres, strftime(date_trunc('quarter', registered_at), '%Y-%m') kwartal_od, count(*) konta,
             count(*) FILTER (WHERE bez_zakupu) bez_zakupu, 100.0 * avg(bez_zakupu::INT) proc_bez_zakupu,
             100.0 * avg(marketing_consent) FILTER (WHERE bez_zakupu) proc_zgoda_bez_zakupu
      FROM konta GROUP BY 1, 2 ORDER BY 2""")
    pokaz(t, miejsca=2)
    t = q("""
      SELECT okres_rej okres, count(*) konta, count(*) FILTER (WHERE bez_zakupu) bez_zakupu, 100.0 * avg(bez_zakupu::INT) proc_bez_zakupu
      FROM konta GROUP BY 1 ORDER BY 1""")
    pokaz(t, miejsca=2)
    for _, w in t.iterrows():
        zapisz(f"konta_rejestracja_okres{w.okres}_konta", w.konta)
        zapisz(f"konta_rejestracja_okres{w.okres}_bez_zakupu", w.bez_zakupu)
        zapisz(f"konta_rejestracja_okres{w.okres}_bez_zakupu_proc", w.proc_bez_zakupu)
    r("\n6c. Miesiące rejestracji")
    t = q("""
      SELECT strftime(registered_at, '%Y-%m') miesiac, count(*) konta, count(*) FILTER (WHERE bez_zakupu) bez_zakupu,
             100.0 * avg(bez_zakupu::INT) proc_bez_zakupu
      FROM konta GROUP BY 1 ORDER BY 1""")
    pokaz(t, miejsca=1)
    for _, w in t.iterrows():
        zapisz(f"konta_rejestracja_{w.miesiac.replace('-', '_')}_bez_zakupu", w.bez_zakupu)
        zapisz(f"konta_rejestracja_{w.miesiac.replace('-', '_')}_konta", w.konta)
    r("\n6d. Kupujący: czas od rejestracji do pierwszego zamówienia (czy ostatnie miesiące rejestracji są niedojrzałe)")
    t = q("""
      SELECT CASE WHEN d < 0 THEN 'a_przed_rejestracja' WHEN d = 0 THEN 'b_ten_sam_dzien' WHEN d <= 7 THEN 'c_1_7_dni'
                  WHEN d <= 30 THEN 'd_8_30_dni' ELSE 'e_ponad_30_dni' END odstep, count(*) konta,
             100.0 * count(*) / sum(count(*)) OVER () proc
      FROM (SELECT date_diff('day', registered_at::DATE, pierwsze::DATE) d FROM konta WHERE NOT bez_zakupu) GROUP BY 1 ORDER BY 1""")
    pokaz(t, miejsca=2)
    for _, w in t.iterrows():
        zapisz(f"konta_kupujacy_odstep_{w.odstep[2:]}_proc", w.proc)
        zapisz(f"konta_kupujacy_odstep_{w.odstep[2:]}_konta", w.konta)

    con.close()
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    with open(WYNIK_JSON, "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1)
    print(f"Raport: {os.path.relpath(WYNIK, D.KATALOG)} ({len(linie)} linii); liczby: {os.path.relpath(WYNIK_JSON, D.KATALOG)} "
          f"({len(J)} kluczy)")


if __name__ == "__main__":
    main()
