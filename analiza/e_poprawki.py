"""E2 — liczby do drugiej listy poprawek Kuby (runda E, 2026-10-22): tylko te, których nie ma w żadnym raporcie.

1. Lejek osób, które jeszcze nie kupowały: ile płaci „dziś”. Konwersja sesji do płatności w miesiącach IV–IX 2026
   (poziom po pogłębieniu spadku, notatki/e_runda.md, punkt 4.4) wobec tych samych miesięcy rok wcześniej (IV–IX 2025)
   i, dla porównania, w III kwartale 2026 wobec III kwartału 2025. Sprawdzenie: suma miesięcy = miesiące z
   analiza/wyniki/e_merytoryka.json (lj_miesiace).
2. Zwroty po wizycie u pacjentów nowych kampanii w ostatnich 12 miesiącach: wszystkie cele wizyty a same wizyty L4
   (dlaczego „Po zakupie” pokazuje 1 044 zwroty, a pozycja 5 listy priorytetów 1 024). Liczone niezależnie na bazie,
   według dnia płatności, jak w analiza/a5r_po_zakupie.py (2b).

Czyta bazę analiza/telemedi.duckdb tylko do odczytu (schemat `czyste`, definicje z analiza/definicje.py) i plik
analiza/wyniki/a5p_lejek_dzienny.csv.gz (lejek dzienny, z którego liczy też e_merytoryka.py). Raport:
analiza/wyniki/e_poprawki.txt, liczby dla strony: analiza/wyniki/e_poprawki.json.
Uruchomienie z głównego folderu: python -I analiza/e_poprawki.py
"""

import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
from a5r_punktualnosc import zbuduj_wizyty  # noqa: E402

WYNIKI = os.path.join(D.KATALOG, "analiza", "wyniki")
DZIS = ("2026-04", "2026-09")          # miesiące „dziś”: od pogłębienia spadku (kwiecień 2026) do końca danych
ROK_WCZESNIEJ = ("2025-04", "2025-09")
Q3 = (("2026-07", "2026-09"), ("2025-07", "2025-09"))


def main():
    sys.stdout.reconfigure(errors="replace")
    linie, J = [], {}

    def r(t=""):
        linie.append(t)

    r(f"E2 — LICZBY DO DRUGIEJ LISTY POPRAWEK ({dt.datetime.now():%Y-%m-%d %H:%M})")
    r("Okres 1 = rok wcześniej (1.10.2024–30.09.2025), okres 2 = ostatnie 12 miesięcy (1.10.2025–30.09.2026), czas polski.")

    # ------------------------------------------------------------------------------------------------ 1. lejek „dziś”
    r("\n1. LEJEK OSÓB, KTÓRE JESZCZE NIE KUPOWAŁY: SESJA DO PŁATNOŚCI „DZIŚ” (sesje zwykłe, dzień sesji w czasie polskim)")
    L = pd.read_csv(os.path.join(WYNIKI, "a5p_lejek_dzienny.csv.gz"))
    L["dzien"] = pd.to_datetime(L.dzien)
    z = L[(L.typ == "zwykla") & (L.podzial == "calosc") & (L.pacjent == "nie_kupowal")].copy()
    z["mies"] = z.dzien.dt.strftime("%Y-%m")
    m = z.groupby("mies")[["sesje", "k5"]].sum()

    def okno(od, do, nazwa):
        x = m.loc[od:do]
        s, p = int(x.sesje.sum()), int(x.k5.sum())
        k = 100 * p / s
        mies = 100 * x.k5 / x.sesje
        r(f"   {nazwa:28} {od}–{do}: {s:>7} sesji, {p:>6} płatności, konwersja {k:.2f}% "
          f"(miesiące od {mies.min():.2f}% do {mies.max():.2f}%)")
        return s, p, k, float(mies.min()), float(mies.max())

    d = okno(*DZIS, "dziś (IV–IX 2026)")
    w = okno(*ROK_WCZESNIEJ, "rok wcześniej (IV–IX 2025)")
    q2 = okno(*Q3[0], "III kwartał 2026")
    q1 = okno(*Q3[1], "III kwartał 2025")
    r(f"   Zmiana IV–IX rok do roku: {d[2] - w[2]:+.2f} punktu procentowego; III kwartał: {q2[2] - q1[2]:+.2f} punktu.")
    for k, v in (("dzis", d), ("rok_wczesniej", w), ("q3_2026", q2), ("q3_2025", q1)):
        J[f"lj_nk_{k}_sesje"], J[f"lj_nk_{k}_platnosci"], J[f"lj_nk_{k}_konw"] = v[0], v[1], v[2]
        J[f"lj_nk_{k}_mies_min"], J[f"lj_nk_{k}_mies_max"] = v[3], v[4]
    J["lj_nk_dzis_od"], J["lj_nk_dzis_do"] = DZIS
    # sprawdzenie: te same miesiące w e_merytoryka.json
    with open(os.path.join(WYNIKI, "e_merytoryka.json"), encoding="utf-8") as f:
        E = json.load(f)
    em = {x["mies"]: x for x in E["lj_miesiace"]}
    for od, do, v in ((*DZIS, d), (*ROK_WCZESNIEJ, w)):
        ms = [x for x in em if od <= x <= do]
        s_e, p_e = sum(em[x]["sesje"] for x in ms), sum(em[x]["k5"] for x in ms)
        zgodne = (s_e, int(p_e)) == (v[0], v[1])
        r(f"   Sprawdzenie z e_merytoryka.json ({od}–{do}): {s_e} sesji, {int(p_e)} płatności — "
          f"{'zgodne' if zgodne else 'RÓŻNICA'}")
        assert zgodne

    # ------------------------------------------------------------------------------- 2. zwroty po wizycie, dwa zbiory
    r("\n2. ZWROTY PO ODBYTEJ WIZYCIE U PACJENTÓW NOWYCH KAMPANII (według pierwszego wejścia), OSTATNIE 12 MIESIĘCY")
    r("   Według dnia płatności; wizyta odbyta = completed albo refunded; zwrot po wizycie = refunded.")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=False)
    zbuduj_wizyty(con)
    t = con.sql("""
      SELECT visit_purpose, count(*) odbyte, count(*) FILTER (WHERE status = 'refunded') zwroty
      FROM wiz WHERE okres = 2 AND nowa_z1k AND status IN ('completed', 'refunded')
      GROUP BY 1 ORDER BY 1""").df()
    con.close()
    for _, x in t.iterrows():
        r(f"   {x.visit_purpose:12} wizyty odbyte {int(x.odbyte):>6}, zwroty po wizycie {int(x.zwroty):>5} "
          f"({100 * x.zwroty / x.odbyte:.1f}%)")
    wsz, l4 = int(t.zwroty.sum()), int(t.loc[t.visit_purpose == "l4", "zwroty"].iloc[0])
    l4_odb = int(t.loc[t.visit_purpose == "l4", "odbyte"].iloc[0])
    r(f"   Razem: {wsz} zwrotów po wizycie (wszystkie cele), z tego {l4} przy wizytach L4 (z {l4_odb} wizyt L4) i "
      f"{wsz - l4} przy innych celach wizyty.")
    J.update({"zw_nowe_wszystkie": wsz, "zw_nowe_l4": l4, "zw_nowe_l4_odbyte": l4_odb, "zw_nowe_inne_cele": wsz - l4})

    with open(os.path.join(WYNIKI, "e_poprawki.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linie) + "\n")
    with open(os.path.join(WYNIKI, "e_poprawki.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(J, f, ensure_ascii=False, indent=1, default=lambda v: v.item() if hasattr(v, "item") else str(v))
    print("\n".join(linie))
    print("Zapisano analiza/wyniki/e_poprawki.txt i e_poprawki.json")


if __name__ == "__main__":
    main()
