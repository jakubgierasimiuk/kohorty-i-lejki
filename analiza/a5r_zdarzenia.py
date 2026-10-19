"""A5 retencja, krok 5 — zdarzenia w seriach retencji i po zakupie (2026-10-19).

Szukamy dni, od których zmienia się poziom serii dziennej. Metoda: podział binarny na danych jednostkowych
(pacjent albo wizyta z dniem): w odcinku szukamy dnia podziału z największą statystyką z różnicy średnich
(lewa i prawa część, przybliżenie normalne), przyjmujemy podział, gdy |z| >= 4 i obie części mają co najmniej
28 dni, i powtarzamy w każdej części (najwyżej 4 podziały na serię). To przybliżenie, nie dowód przyczyny.

Serie:
  - powrót w 30 dniach, kohorty dzienne: wszyscy, kampanie obecne w obu okresach, nowe kampanie;
  - powrót w 90 dniach, kampanie obecne w obu okresach;
  - udział nowych kampanii w nowych pacjentach;
  - wizyty u internisty rano (6–11) spóźnione ponad 15 minut (dzień terminu), pacjenci spoza nowych kampanii;
  - pierwsze zamówienie zwrócone po wizycie;
  - marża na pacjenta w 30 dniach;
  - powrót w 30 dniach pacjentów, których pierwsza płatność była w Safari na iOS (zdarzenie z sesji pozyskania:
    od 17.03.2026 w Safari na iOS przestaje działać zakładanie konta).
Potem: miesiące spadku w kampaniach obecnych w obu okresach zestawione z datami kampanii na L4 i z opóźnieniami
(dopisek Kuby nr 3) i przybliżony wpływ zdarzeń na marżę.

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/a5r_zdarzenia.py
Wynik: analiza/wyniki/a5r_zdarzenia.txt, analiza/wyniki/a5r_zdarzenia.csv
"""

import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
from a5r_punktualnosc import DATY, NOWE, zbuduj_wizyty  # noqa: E402
from a5r_struktura import zbuduj_atr  # noqa: E402

WYNIK = os.path.join(D.KATALOG, "analiza", "wyniki", "a5r_zdarzenia.txt")
WYNIK_CSV = os.path.join(D.KATALOG, "analiza", "wyniki", "a5r_zdarzenia.csv")
KONIEC = pd.Timestamp(D.KONIEC)
MIN_DNI, PROG_Z, MAX_PODZ = 28, 4.0, 4
DATY_ALL = {**DATY, "2026-03-17": "Safari iOS: zakładanie konta (sesja pozyskania)"}
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)


def podzialy(dni, y, prog=None):
    """Podział binarny serii jednostkowej (dzień, wartość). Zwraca listę (dzień_podziału, z)."""
    prog = PROG_Z if prog is None else prog
    d = pd.DataFrame({"d": dni, "y": y}).dropna()
    g = d.groupby("d").y.agg(["count", "sum"]).join(d.assign(y2=d.y ** 2).groupby("d").y2.sum())
    g = g.reindex(pd.date_range(g.index.min(), g.index.max()), fill_value=0)
    wyniki = []

    def szukaj(lo, hi, glebia):
        if glebia >= MAX_PODZ or hi - lo < 2 * MIN_DNI:
            return
        c = g.iloc[lo:hi]
        n, s, s2 = c["count"].cumsum().values, c["sum"].cumsum().values, c["y2"].cumsum().values
        N, S, S2 = n[-1], s[-1], s2[-1]
        najl, kz = None, 0.0
        for k in range(MIN_DNI - 1, len(c) - MIN_DNI):
            n1, n2 = n[k], N - n[k]
            if n1 < 30 or n2 < 30:
                continue
            m1, m2 = s[k] / n1, (S - s[k]) / n2
            v1 = max(s2[k] / n1 - m1 ** 2, 1e-12)
            v2 = max((S2 - s2[k]) / n2 - m2 ** 2, 1e-12)
            z = (m2 - m1) / np.sqrt(v1 / n1 + v2 / n2)
            if abs(z) > abs(kz):
                najl, kz = k, z
        if najl is None or abs(kz) < prog:
            return
        wyniki.append((c.index[najl + 1], kz))
        szukaj(lo, lo + najl + 1, glebia + 1)
        szukaj(lo + najl + 1, hi, glebia + 1)

    szukaj(0, len(g), 0)
    return sorted(wyniki), g


def opis(nazwa, dni, y, skala=100):
    """Odcinki między podziałami: poziom, liczba jednostek, zmiana wobec poprzedniego odcinka."""
    pk, g = podzialy(dni, y)
    granice = [g.index.min()] + [p for p, _ in pk] + [g.index.max() + pd.Timedelta(days=1)]
    wiersze = []
    for i in range(len(granice) - 1):
        c = g[(g.index >= granice[i]) & (g.index < granice[i + 1])]
        wiersze.append({"seria": nazwa, "od": granice[i].date(), "do": (granice[i + 1] - pd.Timedelta(days=1)).date(),
                        "n": int(c["count"].sum()), "poziom": round(skala * c["sum"].sum() / c["count"].sum(), 2)})
    t = pd.DataFrame(wiersze)
    t["zmiana"] = t.poziom.diff().round(2)
    zs = {p.date(): round(z, 1) for p, z in pk}
    t["z"] = t.od.map(zs)
    t["zbieg_z_data"] = t.od.map(lambda d: "; ".join(f"{v} ({k})" for k, v in DATY_ALL.items()
                                                    if abs((pd.Timestamp(d) - pd.Timestamp(k)).days) <= 7))
    if not pk:   # bez podziału: najlepszy kandydat poniżej progu, do informacji
        kand, _ = podzialy(dni, y, prog=0.0)
        if kand:
            dzien, z = max(kand, key=lambda k: abs(k[1]))
            l, p_ = g[g.index < dzien], g[g.index >= dzien]
            t.attrs["kandydat"] = (f"brak podziału z |z| >= {PROG_Z}; najsilniejszy kandydat {dzien.date()} (z = {z:.1f}): "
                                   f"{skala * l['sum'].sum() / l['count'].sum():.2f} przed, {skala * p_['sum'].sum() / p_['count'].sum():.2f} po")
    return t


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False)
    zbuduj_atr(con)
    zbuduj_wizyty(con)
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    r(f"A5 RETENCJA — ZDARZENIA W SERIACH ({dt.datetime.now():%Y-%m-%d %H:%M})")
    r(f"Podział binarny na danych jednostkowych: |z| >= {PROG_Z}, odcinki co najmniej {MIN_DNI} dni, najwyżej {MAX_PODZ} podziały.")
    r("Poziom w procentach (powroty, udziały) albo w zł (marża). zbieg_z_data = znana data w odległości do 7 dni.")
    r("Znane daty: " + "; ".join(f"{k} {v}" for k, v in DATY_ALL.items()))

    atr = con.sql("""
      SELECT a.*, s.os, s.browser, w.koszyk, w.op, w.specialization spec
      FROM atr a JOIN zam z ON z.user_id = a.user_id AND z.nr = 1 JOIN czyste.sessions s ON s.session_id = z.session_id
      JOIN wiz w ON w.order_id = z.order_id""").df()
    atr["d0"] = pd.to_datetime(atr.d0)
    atr["dni_R2"] = atr.dni_R2.astype(float)
    atr["nowa"] = atr.kampania.isin(NOWE)
    g30, g90 = pd.Timestamp(D.granice_por(30)[1]), pd.Timestamp(D.granice_por(90)[1])
    a30 = atr[atr.d0 <= g30].assign(y=lambda x: (x.dni_R2 <= 30).astype(float))
    a90 = atr[atr.d0 <= g90].assign(y=lambda x: (x.dni_R2 <= 90).astype(float))
    wiz = con.sql("""SELECT scheduled_at::DATE dzien, op FROM wiz
                     WHERE specialization = 'internista' AND pora = 'a_rano_6_11' AND op IS NOT NULL AND NOT nowa_z1k
                       AND scheduled_at < TIMESTAMP '2026-10-01'""").df()
    wiz["dzien"] = pd.to_datetime(wiz.dzien)
    ek30 = con.sql("""SELECT k.d0, coalesce(sum(e.marza) FILTER (WHERE e.dni <= 30), 0) m
                      FROM koh k LEFT JOIN ek e USING (user_id) GROUP BY k.user_id, k.d0""").df()
    ek30["d0"] = pd.to_datetime(ek30.d0)
    ek30 = ek30[ek30.d0 <= g30]
    safari = a30[(a30.browser == "Safari") & (a30.os == "iOS") & ~a30.nowa]

    serie = [
        opis("powrot30_wszyscy", a30.d0, a30.y),
        opis("powrot30_stare_kampanie", a30[~a30.nowa].d0, a30[~a30.nowa].y),
        opis("powrot30_nowe_kampanie", a30[a30.nowa].d0, a30[a30.nowa].y),
        opis("powrot90_stare_kampanie", a90[~a90.nowa].d0, a90[~a90.nowa].y),
        opis("udzial_nowych_kampanii", atr.d0, atr.nowa.astype(float)),
        opis("rano_internista_ponad15_stare", wiz.dzien, (wiz.op > 15).astype(float)),
        opis("pierwsze_zwrot_po_wizycie", atr.d0, (atr.status1 == "refunded").astype(float)),
        opis("marza30_na_pacjenta_zl", ek30.d0, ek30.m, skala=1),
        opis("powrot30_safari_ios_stare", safari.d0, safari.y),
    ]
    zd = pd.concat(serie)
    zd.to_csv(WYNIK_CSV, index=False, encoding="utf-8")
    r("\n" + "=" * 120)
    r("1. ODCINKI SERII DZIENNYCH (każdy wiersz = okres o stałym poziomie; zmiana = wobec poprzedniego odcinka)")
    r("=" * 120)
    for s in serie:
        pokaz(s)
        if "kandydat" in s.attrs:
            r("     " + s.attrs["kandydat"])
        r("")

    # ============ 2. MIESIĄCE (dopisek Kuby nr 3) ============
    r("=" * 120)
    r("2. MIESIĄCE KOHORT: KAMPANIE OBECNE W OBU OKRESACH ROK DO ROKU, Z DATAMI KAMPANII NA L4 I OPÓŹNIENIAMI")
    r("=" * 120)
    st = a90[~a90.nowa].copy()
    st["mm"] = st.d0.dt.month
    rows = []
    nowi = atr.assign(mies=atr.d0.dt.to_period("M"))
    for mm in (10, 11, 12, 1, 2, 3, 4, 5, 6):
        x1, x2 = st[(st.okres == 1) & (st.mm == mm)], st[(st.okres == 2) & (st.mm == mm)]
        p1, p2 = x1.y.mean(), x2.y.mean()
        se = np.sqrt(p1 * (1 - p1) / len(x1) + p2 * (1 - p2) / len(x2))
        m2 = x2.d0.dt.to_period("M").iloc[0]
        nm = nowi[nowi.mies == m2]
        w = wiz[wiz.dzien.dt.to_period("M") == m2]
        rows.append({"miesiac_o2": str(m2), "n_o1": len(x1), "n_o2": len(x2), "powrot90_o1": round(100 * p1, 1),
                     "powrot90_o2": round(100 * p2, 1), "zmiana_pkt": round(100 * (p2 - p1), 1),
                     "od": round(100 * (p2 - p1 - 1.96 * se), 1), "do": round(100 * (p2 - p1 + 1.96 * se), 1),
                     "pierwsza_ponad15_o2": round(100 * (x2.op > 15).mean(), 1),
                     "pierwsza_ponad15_o1": round(100 * (x1.op > 15).mean(), 1),
                     "rano_int_ponad15_wszystkie": round(100 * (w.op > 15).mean(), 1),
                     "nowi_meta_l4": int((nm.kampania == "meta_prosp_l4_szybko").sum()),
                     "nowi_tiktok": int((nm.kampania == "tt_prosp_l4_15min").sum()),
                     "daty": "; ".join(v for k, v in DATY_ALL.items() if pd.Timestamp(k).to_period("M") == m2)})
    t = pd.DataFrame(rows)
    pokaz(t)
    r("     od/do = 95% przedział zmiany (przybliżenie normalne). Przy około 1 300–2 000 pacjentów na miesiąc przedział ma")
    r("     szerokość około ±3 punktów procentowych, więc pojedyncze miesiące (październik, luty) mieszczą się w szumie.")
    for etyk, mies in (("listopad–styczeń", [11, 12, 1]), ("marzec–maj", [3, 4, 5]), ("październik i luty", [10, 2]),
                       ("październik", [10]), ("luty", [2])):
        x1, x2 = st[(st.okres == 1) & st.mm.isin(mies)], st[(st.okres == 2) & st.mm.isin(mies)]
        p1, p2 = x1.y.mean(), x2.y.mean()
        se = np.sqrt(p1 * (1 - p1) / len(x1) + p2 * (1 - p2) / len(x2))
        r(f"     {etyk}: {100 * p1:.1f}% (n = {len(x1)}) wobec {100 * p2:.1f}% (n = {len(x2)}), zmiana "
          f"{100 * (p2 - p1):+.1f} punktu (od {100 * (p2 - p1 - 1.96 * se):+.1f} do {100 * (p2 - p1 + 1.96 * se):+.1f})")

    # ============ 3. SAFARI NA iOS ============
    r("\n" + "=" * 120)
    r("3. SAFARI NA iOS (17.03.2026): POWROTY PACJENTÓW, KTÓRZY PIERWSZY RAZ ZAPŁACILI W SAFARI NA iOS")
    r("=" * 120)
    r("   Czy zdarzenie z lejka (nie działa zakładanie konta) widać też w powrotach pacjentów, którzy już mają konto.")
    zam = con.sql("""
      SELECT z.created_at::DATE dzien, s.os = 'iOS' AND s.browser = 'Safari' safari_ios, z.nr > 1 powtorne
      FROM zam z JOIN czyste.sessions s USING (session_id) WHERE z.status <> 'cancelled'""").df()
    zam["dzien"] = pd.to_datetime(zam.dzien)
    zam["okno"] = np.select([zam.dzien < "2026-02-15", zam.dzien < "2026-03-17", zam.dzien < "2026-04-16"],
                            ["a_przed_15.02", "b_15.02_16.03", "c_17.03_15.04"], "d_po_15.04")
    t = zam[zam.dzien >= "2025-10-01"].groupby(["okno", "powtorne"]).safari_ios.agg(["count", "mean"]).reset_index()
    t["mean"] = (100 * t["mean"]).round(1)
    pokaz(t.rename(columns={"count": "zamowienia_nieanul", "mean": "proc_w_safari_ios"}))
    r("     Udział Safari na iOS w zamówieniach powtórnych i pierwszych przed i po 17.03.2026 (okres 2).")

    # ============ 4. WARTOŚĆ POWROTU I PRZYBLIŻONY WPŁYW NA MARŻĘ ============
    r("\n" + "=" * 120)
    r("4. PRZYBLIŻONY WPŁYW NA MARŻĘ (przed kosztem pozyskania)")
    r("=" * 120)
    v = con.sql(f"""
      WITH p AS (SELECT user_id, d0, okres, dni_R2 FROM powr WHERE okres = 1 AND d0 <= DATE '{D.KONIEC}' - 180)
      SELECT coalesce(p.dni_R2 <= 90, FALSE) wrocil_90, count(DISTINCT p.user_id) n,
             round(sum(e.marza) FILTER (WHERE e.dni BETWEEN 1 AND 180) / count(DISTINCT p.user_id), 1) marza_dni_1_180
      FROM p LEFT JOIN ek e ON e.user_id = p.user_id GROUP BY 1 ORDER BY 1""").df()
    pokaz(v)
    wart = float(v.marza_dni_1_180.iloc[1] - v.marza_dni_1_180.iloc[0])
    r(f"     Wartość powrotu (założenie): różnica marży z dni 1–180 między pacjentem, który wrócił w 90 dniach, a tym,")
    r(f"     który nie wrócił, kohorty okresu 1 z pełnymi 180 dniami: {wart:.1f} zł. To korelacja, nie skutek; nie obejmuje")
    r("     marży po 180 dniach. Bezpośrednio obserwowana zmiana: marża dni 1–90 na pacjenta starych kampanii 16,6 zł wobec")
    r("     15,6 zł (a5r_struktura.txt, 6b), czyli około 1,0 zł mniej na każdego nowego pacjenta w pierwszych 90 dniach.")
    n_stare_o2 = int(((atr.okres == 2) & ~atr.nowa).sum())
    n_nowe_o2 = int(((atr.okres == 2) & atr.nowa).sum())
    r(f"     Nowi pacjenci okresu 2: kampanie obecne w obu okresach {n_stare_o2}, nowe kampanie {n_nowe_o2}.")
    rows = []
    for etyk, dp in (("spadek powrotu w starych kampaniach, cały (Z1K)", 1.91),
                     ("spadek powrotu w starych kampaniach, cały (sesja płatności)", 3.50),
                     ("część przypisana opóźnieniu pierwszej wizyty (Z1K, kampania x usługa x opóźnienie)", 0.58),
                     ("część przypisana opóźnieniu pierwszej wizyty (sesja płatności)", 1.28)):
        rows.append({"skladnik": etyk, "punkty_proc": dp, "pacjenci_o2": n_stare_o2,
                     "powrotow_mniej": round(dp / 100 * n_stare_o2), "marza_zl_rocznie": round(-dp / 100 * n_stare_o2 * wart)})
    pokaz(pd.DataFrame(rows))
    r("     Liczba punktów z a5r_struktura.txt (5) i a5r_punktualnosc.txt (1e). Marża = powrotów mniej × wartość powrotu.")
    m = con.sql(f"""
      SELECT r.kampania IN {NOWE} nowa, count(*) wizyty_zwrocone, round(sum(z.amount_paid)) zwrocone_zl,
             round(sum(CASE z.specialization WHEN 'internista' THEN 25 WHEN 'psychiatra' THEN 200 ELSE 100 END)) koszt_lekarza_zl
      FROM zam z JOIN zrodlo r USING (user_id) WHERE z.status = 'refunded' AND z.created_at >= TIMESTAMP '{D.OKRES2}'
      GROUP BY 1 ORDER BY 1""").df()
    r("\n     Zwroty po odbytej wizycie w okresie 2 (wszystkie zamówienia): zwrócone zapłaty i koszt lekarza za te wizyty")
    pokaz(m)

    con.close()
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Raport: {os.path.relpath(WYNIK, D.KATALOG)} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
