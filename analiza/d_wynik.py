"""D — liczby do poprawek po konsylium (notatki/d_poprawki.md, punkty 4, 7 i pozycja 6 listy; 2026-10-21).

Cztery części:
  1. Rozkład spadku marży III kwartału 2026 wobec III kwartału 2025, od nowa: składniki, pacjenci nowych kampanii
     a reszta (obie reguły źródła), pierwsze zamówienia a powtórne, rocznik pacjenta, miesiące VII–IX; sprawdzenie
     rozbicia z syntezy recenzentów; skąd się bierze szacunek Safari na iOS „14–21 tys. zł w III kwartale”
     (c_priorytety.py, P1) i jaka jego część byłaby marżą zaksięgowaną w samym kwartale.
  2. Udział marży z zamówień pacjentów pozyskanych w poprzednich kwartałach („baza powracających”) w marży
     każdego kwartału obu lat.
  3. Test Meta na L4 (meta_prosp_l4_szybko) w parach województw: szum estymatora udziału pacjentów dodatkowych
     w testach pozornych na danych okresu 2, najmniejszy wykrywalny efekt, próg decyzji dziś i po naprawie zwrotów,
     koszt testu 4 i 6 tygodni.
  4. Pozycja 6 (poranna obsada internistów): skąd zakres 0–65,2 tys. zł (c_priorytety.py, P8) i warianty.

Definicje: analiza/definicje.py (ZALOZENIA.md 16–54). Marża biznesu jak w c_priorytety.py, W4: przychód
z konsultacji po zwrotach + TelemediGO − koszt lekarza (także za wizyty zwrócone) − wydatki na kampanie − prowizja
afiliacyjna (przyjęta reguła, w dniu pierwszego zamówienia). Dni księgowania: ZALOZENIA.md 46.

Tylko czyta schemat `czyste` (baza otwarta tylko do odczytu, tabele tymczasowe). Uruchomienie z głównego folderu:
    python -I analiza/d_wynik.py
Wynik: analiza/wyniki/d_wynik.txt (raport), analiza/wyniki/d_wynik.json (najważniejsze liczby, płaski słownik).
"""

import sys

sys.dont_write_bytecode = True  # nie zapisujemy plików .pyc (w folderze pracują inne sesje)

import datetime as dt  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
import a5e_ekonomia as E  # noqa: E402
from a5e_scenariusze import spadki_retencji  # noqa: E402
from a5r_struktura import PELNE, proba, zbuduj_atr  # noqa: E402
from a5r_punktualnosc import rozklad_zagniezdzony, zbuduj_wizyty  # noqa: E402

WYNIKI = os.path.join(D.KATALOG, "analiza", "wyniki")
WYNIK = os.path.join(WYNIKI, "d_wynik.txt")
WYNIK_JSON = os.path.join(WYNIKI, "d_wynik.json")
KONIEC = D.KONIEC
NOWE = ("meta_prosp_l4_szybko", "tt_prosp_l4_15min")
META = "meta_prosp_l4_szybko"
Q3_25, Q3_26 = "2025-07-01", "2026-07-01"
Z_MOC = 1.959964 + 0.841621   # alfa 5% dwustronnie + moc 80%
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)


def zl(x):
    return f"{x:,.0f} zł".replace(",", " ")


def tys(x):
    return f"{x / 1000:,.1f}".replace(",", " ").replace(".", ",") + " tys. zł"


def proc(x, n=1):
    return f"{100 * x:.{n}f}%".replace(".", ",")


def z_raportu(plik, tekst):
    """Sprawdza, że `tekst` stoi w raporcie analiza/wyniki/`plik` (liczba nie przechodzi „z pamięci”)."""
    with open(os.path.join(WYNIKI, plik), encoding="utf-8") as f:
        if tekst not in f.read():
            raise SystemExit(f"W raporcie {plik} nie ma tekstu {tekst!r} — liczba nieaktualna")


def zgodne(a, b, opis, tol=0.5):
    if abs(a - b) > tol:
        raise SystemExit(f"Niezgodność: {opis}: {a} wobec {b}")


def skladniki(df):
    return pd.Series({"zamowienia": float(df.zamowienie.sum()), "przychod": df.przychod.sum(), "telemedigo": df.go.sum(),
                      "koszt_lekarza": df.koszt_lekarza.sum(),
                      "przed_kampaniami": (df.przychod + df.go - df.koszt_lekarza).sum(),
                      "wydatki": df.wydatki.sum(), "prowizja": df.prowizja.sum(), "marza": df.marza.sum()})


def dobierz_pary(cechy):
    """Pary o najmniejszej sumie kwadratów odległości (dokładnie, programowanie dynamiczne po podzbiorach)."""
    n = len(cechy)
    odl = ((cechy[:, None, :] - cechy[None, :, :]) ** 2).sum(-1)
    pelna = (1 << n) - 1
    pamiec = {}

    def f(maska):
        if maska == pelna:
            return 0.0, ()
        if maska in pamiec:
            return pamiec[maska]
        i = next(k for k in range(n) if not maska & (1 << k))
        najl = None
        for j in range(i + 1, n):
            if not maska & (1 << j):
                c, p = f(maska | (1 << i) | (1 << j))
                c += odl[i, j]
                if najl is None or c < najl[0]:
                    najl = (c, ((i, j),) + p)
        pamiec[maska] = najl
        return najl
    return list(f(0)[1])


def pun_wiersze(a, komorka, podzial="koszyk", miara="y"):
    """To samo co a5r_punktualnosc.rozklad_zagniezdzony, ale składnik „punktualność” w podziale na wiersze
    (komórka × koszyk), żeby wybrać tylko poranne wizyty u internisty. Kod przepisany 1:1, suma sprawdzana."""
    g = a.groupby(komorka + [podzial, "okres"])[miara].agg(["count", "mean"]).unstack("okres").reindex(columns=PELNE)
    n1, n2 = g[("count", 1)].fillna(0), g[("count", 2)].fillna(0)
    r1, r2 = g[("mean", 1)], g[("mean", 2)]
    r1, r2 = r1.fillna(r2), r2.fillna(r1)
    kl = g.index.droplevel(podzial)
    c1, c2 = n1.groupby(kl).sum(), n2.groupby(kl).sum()
    wsp = set(c1[(c1 > 0) & (c2 > 0)].index)
    m = kl.isin(list(wsp))
    n1, n2, r1, r2 = n1[m], n2[m], r1[m], r2[m]
    kl = kl[m]
    C1, C2 = n1.groupby(kl).sum(), n2.groupby(kl).sum()
    S1, S2 = C1 / C1.sum(), C2 / C2.sum()
    q1 = n1.values / C1.reindex(kl).values
    q2 = n2.values / C2.reindex(kl).values
    sr_s = ((S1 + S2) / 2).reindex(kl).values
    pun = sr_s * (q2 - q1) * (r1.values + r2.values) / 2
    w = n1.index.to_frame(index=False)
    w["pun"] = pun
    w["n_o1"], w["n_o2"] = n1.values, n2.values
    return w


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=True)
    q = lambda s: con.sql(s).df()  # noqa: E731
    linie = []
    J = {}

    def r(tekst=""):
        linie.append(tekst)

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    def naglowek(t):
        r("\n" + "=" * 118)
        r(t)
        r("=" * 118)

    r(f"D — WYNIK BIZNESU, BAZA POWRACAJĄCYCH, TEST META NA L4, PORANNA OBSADA ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Okres 1 = 1.10.2024–30.09.2025, okres 2 = 1.10.2025–30.09.2026, czas polski. Z1K = przyjęta reguła źródła (pierwsze")
    r("wejście, kod kampanii rozstrzyga), Z2 = sesja płatności. „Nowe kampanie” = meta_prosp_l4_szybko i tt_prosp_l4_15min.")
    r("Marża biznesu = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza − wydatki na kampanie − prowizja")
    r("(jak c_priorytety.py, W4). „Przed kampaniami” = przed wydatkami i prowizją. Kwoty w zł. Rozkład księgowy opisuje, z czego")
    r("składa się zmiana; nie jest zmierzonym wpływem żadnej decyzji.")

    # =====================================================================================================
    # 1. ROZKŁAD SPADKU MARŻY III KWARTAŁU
    # =====================================================================================================
    con.execute(f"""
      CREATE TEMP TABLE d_pac AS
      SELECT k.user_id, k.t0, k.okres okres_koh, date_trunc('quarter', k.t0)::DATE kw_koh, k.order_id pierwsze_id,
             coalesce(r.kampania IN {NOWE}, FALSE) nowa_z1k, coalesce(r.kampania_z2 IN {NOWE}, FALSE) nowa_z2, r.kanal
      FROM koh k LEFT JOIN zrodlo r USING (user_id)""")
    con.execute(f"""
      CREATE TEMP TABLE d_zd AS
      WITH e AS (
        SELECT z.created_at ts, 'konsultacja' typ, CASE WHEN z.nr = 1 THEN 'pierwsze' ELSE 'powtorne' END rodzaj,
               CAST(NULL AS VARCHAR) typ_go, z.user_id, CAST(NULL AS VARCHAR) kampania_wyd,
               (z.amount_paid - z.refund_amount)::DOUBLE przychod, 0.0::DOUBLE go, ({D.KOSZT_LEKARZA})::DOUBLE koszt_lekarza,
               0.0::DOUBLE wydatki, 0.0::DOUBLE prowizja, 1 zamowienie
        FROM zam z
        UNION ALL
        SELECT g.purchased_at, 'telemedigo', CASE WHEN g.order_id = p.pierwsze_id THEN 'pierwsze' ELSE 'powtorne' END,
               CASE WHEN g.order_id IS NULL THEN 'osobno' WHEN g.order_id = p.pierwsze_id THEN 'kasa_pierwsze'
                    ELSE 'kasa_kolejne' END,
               g.user_id, NULL, 0.0, g.amount_paid::DOUBLE, 0.0, 0.0, 0.0, 0
        FROM czyste.go_memberships g LEFT JOIN d_pac p USING (user_id)
        UNION ALL
        SELECT m.date::TIMESTAMP, 'wydatki', 'pozyskanie', NULL, NULL, m.utm_campaign, 0.0, 0.0, 0.0, m.spend_pln::DOUBLE, 0.0, 0
        FROM czyste.marketing_spend m
        UNION ALL
        SELECT p.t0, 'prowizja', 'pozyskanie', NULL, p.user_id, NULL, 0.0, 0.0, 0.0, 0.0, 25.0, 0
        FROM d_pac p WHERE p.kanal = 'afiliacja_ranking')
      SELECT e.*, strftime(date_trunc('quarter', e.ts), '%Y-%m-%d') kw, strftime(date_trunc('month', e.ts), '%Y-%m') mies,
             p.okres_koh, strftime(p.kw_koh, '%Y-%m-%d') kw_koh,
             CASE WHEN e.typ = 'wydatki' THEN e.kampania_wyd IN {NOWE} ELSE p.nowa_z1k END nowa_z1k,
             CASE WHEN e.typ = 'wydatki' THEN e.kampania_wyd IN {NOWE} ELSE p.nowa_z2 END nowa_z2,
             e.przychod + e.go - e.koszt_lekarza - e.wydatki - e.prowizja marza
      FROM e LEFT JOIN d_pac p USING (user_id)""")
    zd = q("SELECT * FROM d_zd")
    brak = int(((zd.typ != "wydatki") & zd.okres_koh.isna()).sum())
    if brak:
        raise SystemExit(f"{brak} zdarzeń pieniężnych bez pacjenta w kohortach")

    # kontrola: ten sam SQL co c_priorytety.py, W4 (marża po kwartałach)
    kw4 = q(f"""
      WITH zz AS (
        SELECT date_trunc('quarter', z.created_at)::DATE kw, sum(z.amount_paid - z.refund_amount)::DOUBLE przychod,
               sum({D.KOSZT_LEKARZA})::DOUBLE koszt_lekarza, count(*) zamowienia
        FROM zam z GROUP BY 1),
      gg AS (SELECT date_trunc('quarter', purchased_at)::DATE kw, sum(amount_paid)::DOUBLE telemedigo FROM czyste.go_memberships GROUP BY 1),
      ww AS (SELECT date_trunc('quarter', date)::DATE kw, sum(spend_pln)::DOUBLE wydatki FROM czyste.marketing_spend GROUP BY 1),
      pp AS (SELECT date_trunc('quarter', k.t0)::DATE kw, 25.0 * count(*) prowizja FROM koh k JOIN zrodlo r USING (user_id)
             WHERE r.kanal = 'afiliacja_ranking' GROUP BY 1)
      SELECT strftime(zz.kw, '%Y-%m-%d') kw, zamowienia, przychod, telemedigo, koszt_lekarza, coalesce(wydatki, 0) wydatki,
             coalesce(prowizja, 0) prowizja,
             przychod + telemedigo - koszt_lekarza - coalesce(wydatki, 0) - coalesce(prowizja, 0) marza
      FROM zz LEFT JOIN gg USING (kw) LEFT JOIN ww USING (kw) LEFT JOIN pp USING (kw) ORDER BY 1""").set_index("kw")
    moje = zd.groupby("kw").apply(skladniki, include_groups=False)
    for kw_ in kw4.index:
        for kol in ("przychod", "telemedigo", "koszt_lekarza", "wydatki", "prowizja", "marza", "zamowienia"):
            zgodne(moje.at[kw_, kol], kw4.at[kw_, kol], f"W4 {kw_} {kol}", tol=0.005)
    z_raportu("c_priorytety.txt", "2026-Q3        9181  747306.0     49662.0       404475.0          392493.0 181555.0    3225.0 207713.0")
    z_raportu("c_priorytety.txt", "2025-Q3        6316  558212.0     56693.0       301375.0          313530.0  87431.0    3275.0 222824.0")

    a, b = zd[zd.kw == Q3_25], zd[zd.kw == Q3_26]
    A_, B_ = skladniki(a), skladniki(b)
    dm = B_.marza - A_.marza
    J.update({"q3_2025_marza": A_.marza, "q3_2026_marza": B_.marza, "q3_zmiana_marzy": dm,
              "q3_2025_wydatki": A_.wydatki, "q3_2026_wydatki": B_.wydatki})

    naglowek("1. SPADEK MARŻY III KWARTAŁU 2026 (VII–IX) WOBEC III KWARTAŁU 2025 — ROZKŁAD OD NOWA")
    r("   Kontrola: sumy po kwartałach zgadzają się co do grosza z SQL c_priorytety.py (W4) dla wszystkich 8 kwartałów.")
    r(f"   III kwartał 2025: marża {zl(A_.marza)}; III kwartał 2026: {zl(B_.marza)}; zmiana {zl(dm)} ({proc(dm / A_.marza)}).")

    r("\n1a. Składniki (cały biznes). wkład = wpływ zmiany składnika na zmianę marży (koszty ze znakiem minus).")
    znak = {"zamowienia": np.nan, "przychod": 1, "telemedigo": 1, "koszt_lekarza": -1, "przed_kampaniami": 1, "wydatki": -1,
            "prowizja": -1, "marza": 1}
    t = pd.DataFrame({"pozycja": A_.index, "III_kw_2025": A_.values, "III_kw_2026": B_.values})
    t["zmiana"] = t.III_kw_2026 - t.III_kw_2025
    t["wklad_w_zmiane_marzy"] = [z * d for z, d in zip(t.pozycja.map(znak), t.zmiana)]
    pokaz(t.round(0))
    w = zd[(zd.typ == "wydatki") & zd.kw.isin([Q3_25, Q3_26])].pivot_table(index="kampania_wyd", columns="kw", values="wydatki",
                                                                         aggfunc="sum", fill_value=0.0)
    w = w.reindex(columns=[Q3_25, Q3_26], fill_value=0.0)
    w.columns = ["III_kw_2025", "III_kw_2026"]
    w["wklad_w_zmiane_marzy"] = -(w.III_kw_2026 - w.III_kw_2025)
    w["nowa_kampania"] = w.index.isin(NOWE)
    r("   Wydatki według kampanii (wkład = −zmiana wydatków):")
    pokaz(w.sort_values("wklad_w_zmiane_marzy").reset_index().rename(columns={"kampania_wyd": "kampania"}).round(0))
    wyd_stare = w[~w.nowa_kampania]
    J["q3_wydatki_stare_kampanie_2025"] = wyd_stare.III_kw_2025.sum()
    J["q3_wydatki_stare_kampanie_2026"] = wyd_stare.III_kw_2026.sum()
    r(f"   Wydatki kampanii działających w obu latach: {zl(wyd_stare.III_kw_2025.sum())} wobec {zl(wyd_stare.III_kw_2026.sum())}"
      f" ({zl(wyd_stare.III_kw_2026.sum() - wyd_stare.III_kw_2025.sum())}); nowe kampanie: 0 zł wobec "
      f"{zl(w[w.nowa_kampania].III_kw_2026.sum())}.")

    # --- 1b. nowe kampanie a reszta ---
    r("\n1b. Pacjenci nowych kampanii a reszta biznesu. Pacjentom przypisane są ich zamówienia, opłaty TelemediGO, koszt lekarza")
    r("    i prowizja; grupie „nowe” wydatki dwóch nowych kampanii, reszcie wydatki pozostałych kampanii. pacjenci = osoby")
    r("    z co najmniej jednym zamówieniem w kwartale.")
    wiersze = []
    for reg, kol in (("Z1K", "nowa_z1k"), ("Z2", "nowa_z2")):
        for nowa in (True, False):
            for kw_, df in ((Q3_25, a), (Q3_26, b)):
                s = skladniki(df[df[kol] == nowa])
                pac = df[(df[kol] == nowa) & (df.typ == "konsultacja")].user_id.nunique()
                wiersze.append({"regula": reg, "grupa": "nowe kampanie" if nowa else "reszta", "kwartal": kw_[:4] + "-Q3",
                                "pacjenci": pac, **s.to_dict()})
    G = pd.DataFrame(wiersze)
    pokaz(G.round(0))
    gz = G.set_index(["regula", "grupa", "kwartal"])
    for reg in ("Z1K", "Z2"):
        nowe26 = gz.loc[(reg, "nowe kampanie", "2026-Q3")]
        res25, res26 = gz.loc[(reg, "reszta", "2025-Q3")], gz.loc[(reg, "reszta", "2026-Q3")]
        luka = (res26.marza - res25.marza) - (res26.telemedigo - res25.telemedigo)
        k = reg.lower()
        J.update({f"q3_nowe_{k}_przed_kampaniami_2026": nowe26.przed_kampaniami, f"q3_nowe_{k}_wydatki_2026": nowe26.wydatki,
                  f"q3_nowe_{k}_marza_2026": nowe26.marza, f"q3_nowe_{k}_zamowienia_2026": nowe26.zamowienia,
                  f"q3_reszta_{k}_marza_2025": res25.marza, f"q3_reszta_{k}_marza_2026": res26.marza,
                  f"q3_reszta_{k}_zmiana": res26.marza - res25.marza,
                  f"q3_reszta_{k}_telemedigo_zmiana": res26.telemedigo - res25.telemedigo,
                  f"q3_reszta_{k}_luka_bez_telemedigo": luka})
        r(f"   {reg}: nowe kampanie {zl(nowe26.przed_kampaniami)} marży przed kampaniami ({int(nowe26.zamowienia)} zamówień, "
          f"{int(nowe26.pacjenci)} pacjentów) przy {zl(nowe26.wydatki)} wydatków, czyli {zl(nowe26.marza)} po wydatkach;")
        r(f"        reszta {zl(res26.marza)} po wydatkach wobec {zl(res25.marza)} ({zl(res26.marza - res25.marza)}); w tym opłaty "
          f"TelemediGO {zl(res25.telemedigo)} → {zl(res26.telemedigo)} ({zl(res26.telemedigo - res25.telemedigo)});")
        r(f"        po odjęciu zmiany TelemediGO zostaje {zl(luka)}.")
    r("   Sprawdzenie twierdzenia z syntezy recenzentów (Z1K): „89,0 tys. zł marży przy 87,9 tys. zł wydatków; reszta 206,6 wobec")
    r("   222,8 tys. zł; około 11,2 tys. zł to niższe opłaty TelemediGO; zostaje około 5 tys. zł” — porównanie z liczbami powyżej")
    r(f"   (Z1K): {tys(J['q3_nowe_z1k_przed_kampaniami_2026'])}, {tys(J['q3_nowe_z1k_wydatki_2026'])}, "
      f"{tys(J['q3_reszta_z1k_marza_2026'])} wobec {tys(J['q3_reszta_z1k_marza_2025'])}, "
      f"{tys(J['q3_reszta_z1k_telemedigo_zmiana'])}, {tys(J['q3_reszta_z1k_luka_bez_telemedigo'])}.")

    # --- 1c. reszta: szczegółowy rozkład luki ---
    r("\n1c. Reszta biznesu: z czego składa się zmiana (te same pozycje w obu kwartałach; suma = zmiana marży reszty).")
    r("    konsultacje = przychód po zwrotach − koszt lekarza; rocznik = okres pierwszego zamówienia pacjenta.")

    def pozycje(df):
        out = {}
        kons = df[df.typ == "konsultacja"]
        for nazwa, m in (("konsultacje: pierwsze zamówienia", kons.rodzaj == "pierwsze"),
                         ("konsultacje: powtórne, rocznik okresu 1", (kons.rodzaj == "powtorne") & (kons.okres_koh == 1)),
                         ("konsultacje: powtórne, rocznik okresu 2", (kons.rodzaj == "powtorne") & (kons.okres_koh == 2))):
            x = kons[m]
            out[nazwa] = (len(x), x.przychod.sum(), x.koszt_lekarza.sum(), (x.przychod - x.koszt_lekarza).sum())
        g = df[df.typ == "telemedigo"]
        for tg, nazwa in (("kasa_pierwsze", "TelemediGO przy kasie z pierwszym zamówieniem"),
                          ("kasa_kolejne", "TelemediGO przy kasie z kolejnym zamówieniem"),
                          ("osobno", "TelemediGO kupione osobno (crm_go_upsell)")):
            x = g[g.typ_go == tg]
            out[nazwa] = (len(x), x.go.sum(), 0.0, x.go.sum())
        x = df[df.typ == "wydatki"]
        out["wydatki na kampanie"] = (np.nan, np.nan, np.nan, -x.wydatki.sum())
        x = df[df.typ == "prowizja"]
        out["prowizja afiliacyjna"] = (len(x), np.nan, np.nan, -x.prowizja.sum())
        return out

    for reg, kol in (("Z1K", "nowa_z1k"), ("Z2", "nowa_z2")):
        p25, p26 = pozycje(a[~a[kol]]), pozycje(b[~b[kol]])
        t = pd.DataFrame([{"pozycja": k, "liczba_2025": p25[k][0], "liczba_2026": p26[k][0], "przychod_2025": p25[k][1],
                           "przychod_2026": p26[k][1], "koszt_lek_2025": p25[k][2], "koszt_lek_2026": p26[k][2],
                           "marza_2025": p25[k][3], "marza_2026": p26[k][3], "zmiana": p26[k][3] - p25[k][3]} for k in p25])
        r(f"   Reszta biznesu według {reg}:")
        pokaz(t.round(0))
        zgodne(t.zmiana.sum(), J[f"q3_reszta_{reg.lower()}_zmiana"], f"suma pozycji reszty {reg}", tol=0.01)
        k = reg.lower()
        kp = t.set_index("pozycja")
        # rozbicie pierwszych zamówień na liczbę i marżę na zamówienie
        n1_, n2_ = kp.at["konsultacje: pierwsze zamówienia", "liczba_2025"], kp.at["konsultacje: pierwsze zamówienia", "liczba_2026"]
        m1_ = kp.at["konsultacje: pierwsze zamówienia", "marza_2025"] / n1_
        m2_ = kp.at["konsultacje: pierwsze zamówienia", "marza_2026"] / n2_
        r(f"   {reg}, pierwsze zamówienia reszty: {int(n1_)} → {int(n2_)} zamówień, marża na zamówienie {m1_:.2f} → {m2_:.2f} zł;"
          f" efekt liczby {zl((n2_ - n1_) * m1_)}, efekt marży na zamówienie {zl(n2_ * (m2_ - m1_))}.")
        pw = t[t.pozycja.str.startswith("konsultacje: powtórne")]
        n1p, n2p = pw.liczba_2025.sum(), pw.liczba_2026.sum()
        m1p, m2p = pw.marza_2025.sum() / n1p, pw.marza_2026.sum() / n2p
        r(f"   {reg}, powtórne zamówienia reszty: {int(n1p)} → {int(n2p)} zamówień, marża na zamówienie {m1p:.2f} → {m2p:.2f} zł;"
          f" efekt liczby {zl((n2p - n1p) * m1p)}, efekt marży na zamówienie {zl(n2p * (m2p - m1p))}.")
        J.update({f"q3_reszta_{k}_pierwsze_zamowienia_2025": n1_, f"q3_reszta_{k}_pierwsze_zamowienia_2026": n2_,
                  f"q3_reszta_{k}_pierwsze_marza_zmiana": kp.at["konsultacje: pierwsze zamówienia", "zmiana"],
                  f"q3_reszta_{k}_powtorne_marza_zmiana": pw.zmiana.sum(),
                  f"q3_reszta_{k}_wydatki_wklad": kp.at["wydatki na kampanie", "zmiana"],
                  f"q3_reszta_{k}_prowizja_wklad": kp.at["prowizja afiliacyjna", "zmiana"],
                  f"q3_reszta_{k}_konsultacje_marza_zmiana": t[t.pozycja.str.startswith("konsultacje")].zmiana.sum()})

    # --- 1d. pierwsze a powtórne, rocznik (cały biznes) ---
    r("\n1d. Cały biznes: pierwsze zamówienia a powtórne i rocznik pacjenta (marża przed kampaniami; pozyskanie = wydatki")
    r("    i prowizja). Pierwsze = pierwsze zamówienie i TelemediGO kupione z nim; powtórne = kolejne zamówienia i pozostałe")
    r("    TelemediGO. W III kwartale 2025 wszyscy pacjenci są z rocznika okresu 1.")
    wiersze = []
    for kw_, df in ((Q3_25, a), (Q3_26, b)):
        for nazwa, m in (("pierwsze, rocznik 2", (df.rodzaj == "pierwsze") & (df.okres_koh == 2)),
                         ("pierwsze, rocznik 1", (df.rodzaj == "pierwsze") & (df.okres_koh == 1)),
                         ("powtórne, rocznik 1", (df.rodzaj == "powtorne") & (df.okres_koh == 1)),
                         ("powtórne, rocznik 2", (df.rodzaj == "powtorne") & (df.okres_koh == 2)),
                         ("pozyskanie (wydatki i prowizja)", df.rodzaj == "pozyskanie")):
            s = skladniki(df[m])
            wiersze.append({"kwartal": kw_[:4] + "-Q3", "pozycja": nazwa, "zamowienia": s.zamowienia,
                            "przed_kampaniami": s.przed_kampaniami, "marza": s.marza})
    t = pd.DataFrame(wiersze).pivot_table(index="pozycja", columns="kwartal", values=["zamowienia", "marza"], aggfunc="sum")
    t.columns = [f"{x}_{y}" for x, y in t.columns]
    t["zmiana_marzy"] = t["marza_2026-Q3"] - t["marza_2025-Q3"]
    pokaz(t.reset_index().round(0))
    zgodne(t.zmiana_marzy.sum(), dm, "suma 1d", tol=0.01)
    tt = t["zmiana_marzy"]
    J.update({"q3_pierwsze_marza_zmiana": tt["pierwsze, rocznik 2"] + tt["pierwsze, rocznik 1"],
              "q3_powtorne_rocznik1_marza_zmiana": tt["powtórne, rocznik 1"], "q3_powtorne_rocznik2_marza_2026": tt["powtórne, rocznik 2"],
              "q3_pozyskanie_zmiana": tt["pozyskanie (wydatki i prowizja)"]})
    r("   Zmiana marży = pierwsze zamówienia " + zl(J["q3_pierwsze_marza_zmiana"]) + " + powtórne rocznika okresu 1 "
      + zl(J["q3_powtorne_rocznik1_marza_zmiana"]) + " + powtórne rocznika okresu 2 " + zl(J["q3_powtorne_rocznik2_marza_2026"])
      + " + pozyskanie " + zl(J["q3_pozyskanie_zmiana"]) + ".")
    r("   W III kwartale 2026 powtórne zamówienia składają się z dwóch roczników; rok wcześniej był tylko rocznik okresu 1.")

    # --- 1e. miesiące ---
    r("\n1e. Osobno lipiec, sierpień, wrzesień (Z1K; reszta = bez pacjentów i wydatków nowych kampanii)")
    wiersze = []
    for mm in ("07", "08", "09"):
        x25, x26 = zd[zd.mies == f"2025-{mm}"], zd[zd.mies == f"2026-{mm}"]
        s25, s26 = skladniki(x25), skladniki(x26)
        r25, r26 = skladniki(x25[~x25.nowa_z1k]), skladniki(x26[~x26.nowa_z1k])
        n26 = skladniki(x26[x26.nowa_z1k])
        go_os25 = x25[(x25.typ_go == "osobno") & ~x25.nowa_z1k].go.sum()
        go_os26 = x26[(x26.typ_go == "osobno") & ~x26.nowa_z1k].go.sum()
        wiersze.append({"miesiac": mm, "marza_2025": s25.marza, "marza_2026": s26.marza, "zmiana": s26.marza - s25.marza,
                        "nowe_przed_kampaniami_2026": n26.przed_kampaniami, "nowe_wydatki_2026": n26.wydatki,
                        "reszta_2025": r25.marza, "reszta_2026": r26.marza, "reszta_zmiana": r26.marza - r25.marza,
                        "reszta_telemedigo_zmiana": r26.telemedigo - r25.telemedigo,
                        "w_tym_go_osobno_2025": go_os25, "w_tym_go_osobno_2026": go_os26,
                        "reszta_wydatki_zmiana": r26.wydatki - r25.wydatki,
                        "reszta_konsultacje_zmiana": (r26.przychod - r26.koszt_lekarza) - (r25.przychod - r25.koszt_lekarza),
                        "reszta_luka_bez_telemedigo": (r26.marza - r25.marza) - (r26.telemedigo - r25.telemedigo)})
    M_ = pd.DataFrame(wiersze)
    pokaz(M_.round(0))
    for _, w_ in M_.iterrows():
        J[f"q3_miesiac_{w_.miesiac}_zmiana_marzy"] = w_.zmiana
        J[f"q3_miesiac_{w_.miesiac}_reszta_luka_bez_telemedigo"] = w_.reszta_luka_bez_telemedigo
    r("   reszta_konsultacje_zmiana = zmiana (przychód po zwrotach − koszt lekarza) reszty; reszta_wydatki_zmiana = zmiana wydatków")
    r("   pozostałych kampanii (wzrost obniża marżę). w_tym_go_osobno = TelemediGO kupione osobno (sesje crm_go_upsell).")
    go_typ = zd[(zd.typ == "telemedigo") & zd.mies.isin([f"{y}-{m}" for y in (2025, 2026) for m in ("07", "08", "09")])]
    go_typ = go_typ.pivot_table(index="mies", columns="typ_go", values="go", aggfunc=["count", "sum"], fill_value=0)
    go_typ.columns = [f"{'liczba' if x == 'count' else 'zl'}_{y}" for x, y in go_typ.columns]
    r("   TelemediGO według typu zakupu i miesiąca (wszyscy pacjenci):")
    pokaz(go_typ.reset_index())
    r("\n1g. Podsumowanie części 1 (opis księgowy, nie zmierzony wpływ):")
    r(f"   - Cała zmiana marży III kwartału: {zl(dm)}. Według miesięcy: lipiec {zl(J['q3_miesiac_07_zmiana_marzy'])}, sierpień "
      f"{zl(J['q3_miesiac_08_zmiana_marzy'])}, wrzesień {zl(J['q3_miesiac_09_zmiana_marzy'])}.")
    r(f"   - Według przyjętej reguły (Z1K): pacjenci nowych kampanii {zl(J['q3_nowe_z1k_marza_2026'])} po wydatkach; reszta biznesu "
      f"{zl(J['q3_reszta_z1k_zmiana'])}, z czego TelemediGO {zl(J['q3_reszta_z1k_telemedigo_zmiana'])}, wydatki pozostałych kampanii "
      f"{zl(J['q3_reszta_z1k_wydatki_wklad'])}, marża konsultacji {zl(J['q3_reszta_z1k_konsultacje_marza_zmiana'])} (pierwsze "
      f"{zl(J['q3_reszta_z1k_pierwsze_marza_zmiana'])}, powtórne {zl(J['q3_reszta_z1k_powtorne_marza_zmiana'])}), prowizja "
      f"{zl(J['q3_reszta_z1k_prowizja_wklad'])}.")
    r(f"   - Według sesji płatności (Z2): pacjenci nowych kampanii {zl(J['q3_nowe_z2_marza_2026'])} po wydatkach; reszta "
      f"{zl(J['q3_reszta_z2_zmiana'])} (po odjęciu TelemediGO {zl(J['q3_reszta_z2_luka_bez_telemedigo'])}). Podział między nowe")
    r("     kampanie a resztę zależy więc od reguły źródła; suma jest ta sama.")

    # --- 1f. Safari na iOS: rachunek 14–21 tys. zł i część zaksięgowana w kwartale ---
    naglowek("1f. SAFARI NA iOS: SKĄD „14–21 TYS. ZŁ W III KWARTALE” (c_priorytety.py, P1) I CO Z TEGO TRAFIA DO SAMEGO KWARTAŁU")
    con.execute("""
      CREATE TEMP TABLE saf_ev AS
      SELECT session_id,
             max((event_name = 'service_selected')::INT) k1, max((event_name = 'slot_selected')::INT) k2,
             max((event_name = 'account_completed')::INT) k3, max((event_name = 'payment_started')::INT) k4,
             max((event_name = 'payment_succeeded')::INT) k5
      FROM czyste.events GROUP BY 1""")
    con.execute("CREATE TEMP TABLE saf_pierwszy AS SELECT user_id, min(created_at) t FROM czyste.orders GROUP BY 1")
    con.execute("""
      CREATE TEMP TABLE saf_sz AS
      SELECT s.dzien_pl, coalesce(e.k2, 0) k2, coalesce(e.k3, 0) k3, coalesce(e.k5, 0) k5,
             coalesce(s.os = 'iOS' AND s.browser = 'Safari', FALSE) ios, coalesce(pz.t < s.started_at_pl, FALSE) kupowal_wczesniej
      FROM czyste.sessions s
      LEFT JOIN saf_ev e USING (session_id)
      LEFT JOIN przeg p ON p.visitor_id = s.visitor_id AND s.user_id IS NULL
      LEFT JOIN saf_pierwszy pz ON pz.user_id = coalesce(s.user_id, p.user_id)
      WHERE NOT (s.user_id IS NOT NULL AND coalesce(e.k3, 0) = 0)
        AND s.session_id NOT IN (SELECT session_id FROM czyste.go_memberships WHERE order_id IS NULL)""")

    def utracone(od, do=None):
        war = f"dzien_pl >= '{od}'" + (f" AND dzien_pl <= '{do}'" if do else "")
        x = q(f"""
          WITH a AS (SELECT ios,
                            sum(k3) FILTER (WHERE dzien_pl BETWEEN '2025-10-01' AND '2026-03-16')
                              / sum(k2) FILTER (WHERE dzien_pl BETWEEN '2025-10-01' AND '2026-03-16') p0,
                            sum(k3) FILTER (WHERE {war}) / sum(k2) FILTER (WHERE {war}) p1,
                            sum(k2) FILTER (WHERE {war}) k2_po, sum(k5) FILTER (WHERE {war}) / sum(k3) FILTER (WHERE {war}) dalej
                     FROM saf_sz WHERE NOT kupowal_wczesniej GROUP BY 1)
          SELECT s.k2_po, s.p0, s.p1, s.dalej, (s.p0 - s.p1) * s.k2_po * s.dalej bez_tla,
                 ((s.p0 - s.p1) - (r_.p0 - r_.p1)) * s.k2_po * s.dalej po_odjeciu_tla
          FROM a s, a r_ WHERE s.ios AND NOT r_.ios""").iloc[0]
        return x
    cale = utracone("2026-03-17")
    zgodne(round(cale.bez_tla), 695, "Safari bez odjęcia tła (a5p 5f)")
    zgodne(round(cale.po_odjeciu_tla), 628, "Safari po odjęciu tła (a5p 5f)")
    z_raportu("a5p_zdarzenia.txt", "695.0      105.3")
    z_raportu("a5p_zdarzenia.txt", "628.0       95.2")
    kw3 = utracone("2026-07-01")
    r("   Utracone pierwsze zamówienia = (k3/k2 przed − k3/k2 po) × sesje z wyborem terminu po × k5/k3 po; przed = 1.10.2025–16.03.2026;")
    r("   osoby, które jeszcze nie kupowały; „po odjęciu tła” odejmuje równoległą zmianę w pozostałych przeglądarkach (a5p 5f).")
    r(f"   17.03–30.09.2026 (198 dni): {cale.bez_tla:.1f} bez odjęcia tła, {cale.po_odjeciu_tla:.1f} po odjęciu (odtworzone 695 i 628).")
    r(f"   Sam III kwartał (1.07–30.09.2026, 92 dni), ten sam wzór: {kw3.bez_tla:.1f} bez odjęcia tła, {kw3.po_odjeciu_tla:.1f} po odjęciu"
      f" (k3/k2 {proc(kw3.p1)} wobec {proc(kw3.p0)} przed; {int(kw3.k2_po)} sesji z wyborem terminu).")

    # marża narastająco pacjentów z pierwszą płatnością w Safari na iOS, okres 2
    sf = q("""
      SELECT k.user_id, k.d0, e.dni, e.marza
      FROM koh k JOIN czyste.sessions s ON s.session_id = k.session_id
      LEFT JOIN ek e ON e.user_id = k.user_id AND e.dni <= 200
      WHERE k.okres = 2 AND s.os = 'iOS' AND s.browser = 'Safari'""")
    sf["d0"] = pd.to_datetime(sf.d0)

    def krzywa(granica_dni, kmax):
        g = sf[sf.d0 <= pd.Timestamp(KONIEC) - pd.Timedelta(days=granica_dni)]
        n = g.user_id.nunique()
        dz = g.dropna(subset=["dni"]).groupby("dni").marza.sum().reindex(range(kmax + 1), fill_value=0.0)
        return dz.cumsum().values / n, n
    M91, n91 = krzywa(91, 91)
    m0 = q(f"""SELECT avg(coalesce(m0, 0)) m0, avg(coalesce(m91, 0)) m91, count(*) n
               FROM koh k JOIN czyste.sessions s ON s.session_id = k.session_id
               LEFT JOIN (SELECT user_id, sum(marza) FILTER (WHERE dni = 0) m0, sum(marza) FILTER (WHERE dni <= 91) m91
                          FROM ek GROUP BY 1) e ON e.user_id = k.user_id
               WHERE k.okres = 2 AND s.os = 'iOS' AND s.browser = 'Safari' AND k.d0 <= DATE '{KONIEC}' - 91""").iloc[0]
    zgodne(M91[0], m0.m0, "marża dnia 0 Safari (P1)", tol=1e-9)
    zgodne(M91[91], m0.m91, "marża do 91 dni Safari (P1)", tol=1e-9)
    r(f"   Marża pacjenta z pierwszą płatnością w Safari na iOS (okres 2, {n91} pacjentów z kohort do {pd.Timestamp(KONIEC) - pd.Timedelta(days=91):%d.%m.%Y}):"
      f" dzień 0 {M91[0]:.2f} zł, do 91. dnia {M91[91]:.2f} zł (przed kosztem pozyskania).")
    r("   Rachunek c_priorytety.py, P1: utracone w 198 dniach / 198 × 92 dni × marża; dolny koniec = po odjęciu tła × marża dnia 0,")
    r("   górny = bez odjęcia tła × marża do 91. dnia:")
    wiersze = []
    for nazwa, utr in (("po odjęciu tła", cale.po_odjeciu_tla), ("bez odjęcia tła", cale.bez_tla)):
        tempo = round(utr) / 198
        zaks = tempo * M91[:92].sum()
        wiersze.append({"wariant": nazwa, "utracone_w_kwartale": tempo * 92, "marza_dnia_0": tempo * 92 * M91[0],
                        "marza_do_91_dni_rocznik": tempo * 92 * M91[91], "zaksiegowane_w_kwartale": zaks,
                        "w_tym_powroty_w_kwartale": zaks - tempo * 92 * M91[0]})
    for nazwa, utr in (("III kwartał, po odjęciu tła", kw3.po_odjeciu_tla), ("III kwartał, bez odjęcia tła", kw3.bez_tla)):
        tempo = utr / 92
        zaks = tempo * M91[:92].sum()
        wiersze.append({"wariant": nazwa, "utracone_w_kwartale": utr, "marza_dnia_0": utr * M91[0],
                        "marza_do_91_dni_rocznik": utr * M91[91], "zaksiegowane_w_kwartale": zaks,
                        "w_tym_powroty_w_kwartale": zaks - utr * M91[0]})
    S_ = pd.DataFrame(wiersze)
    pokaz(S_.round(1))
    z_raportu("c_priorytety.txt", "marża z dnia pierwszego zamówienia 14 141 zł")
    z_raportu("c_priorytety.txt", "najwyżej 20 869 zł")
    zgodne(S_.marza_dnia_0[0], 14141, "Safari P1 dolny koniec", tol=1)
    zgodne(S_.marza_do_91_dni_rocznik[1], 20869, "Safari P1 górny koniec", tol=1)
    # powtórne zamówienia w III kwartale pacjentów utraconych 17.03–30.06 (106 dni)
    M197, n197 = krzywa(197, 197)
    przen = []
    for nazwa, utr in (("po odjęciu tła", cale.po_odjeciu_tla), ("bez odjęcia tła", cale.bez_tla)):
        tempo = round(utr) / 198
        przen.append(tempo * sum(M197[k + 92] - M197[k] for k in range(106)))
    r("   utracone_w_kwartale × marza_dnia_0 i × marza_do_91_dni_rocznik to dwa końce zakresu z P1 (14 141 i 20 869 zł).")
    r("   zaksiegowane_w_kwartale = pierwsze zamówienia utracone w dniach 1.07–30.09 (równe tempo) × marża narastająco do 30.09:")
    r("   pacjent utracony 25.09 ma w kwartale tylko 5 dni na powrót, więc dostaje M(5), a nie M(91). Suma = tempo × Σ M(k), k = 0..91.")
    r(f"   Obok (nie w zakresie P1): powtórne zamówienia w III kwartale pacjentów utraconych 17.03–30.06: {zl(przen[0])}–{zl(przen[1])}")
    r(f"   (marża narastająco z {n197} pacjentów z kohort do {pd.Timestamp(KONIEC) - pd.Timedelta(days=197):%d.%m.%Y}, dni 0–197).")
    J.update({"safari_utracone_198_dni_po_odjeciu_tla": cale.po_odjeciu_tla, "safari_utracone_198_dni_bez_odjecia_tla": cale.bez_tla,
              "safari_utracone_q3_po_odjeciu_tla": kw3.po_odjeciu_tla, "safari_utracone_q3_bez_odjecia_tla": kw3.bez_tla,
              "safari_marza_dnia_0": M91[0], "safari_marza_do_91_dni": M91[91],
              "safari_p1_dolny_koniec": S_.marza_dnia_0[0], "safari_p1_gorny_koniec": S_.marza_do_91_dni_rocznik[1],
              "safari_zaksiegowane_q3_po_odjeciu_tla": S_.zaksiegowane_w_kwartale[0],
              "safari_zaksiegowane_q3_bez_odjecia_tla": S_.zaksiegowane_w_kwartale[1],
              "safari_zaksiegowane_q3_tempo_q3_po_odjeciu_tla": S_.zaksiegowane_w_kwartale[2],
              "safari_zaksiegowane_q3_tempo_q3_bez_odjecia_tla": S_.zaksiegowane_w_kwartale[3],
              "safari_powroty_q3_utraconych_przed_q3_od": przen[0], "safari_powroty_q3_utraconych_przed_q3_do": przen[1]})

    # =====================================================================================================
    # 2. BAZA POWRACAJĄCYCH W MARŻY KWARTAŁÓW
    # =====================================================================================================
    naglowek("2. UDZIAŁ MARŻY Z ZAMÓWIEŃ PACJENTÓW POZYSKANYCH W POPRZEDNICH KWARTAŁACH („BAZA”) W KAŻDYM KWARTALE")
    r("   pierwsze = pierwsze zamówienia i TelemediGO kupione z nimi; ten_sam_kw = kolejne zamówienia i TelemediGO pacjentów")
    r("   pozyskanych w tym samym kwartale; baza = zamówienia i TelemediGO pacjentów pozyskanych w poprzednich kwartałach;")
    r("   pozyskanie = wydatki i prowizja. Kwoty to marża przed kampaniami (pozyskanie ze znakiem minus). Dane zaczynają się")
    r("   1.10.2024, więc w IV kwartale 2024 bazy nie ma z definicji.")
    zd["kat"] = np.select([zd.rodzaj == "pozyskanie", zd.rodzaj == "pierwsze", zd.kw_koh == zd.kw],
                          ["pozyskanie", "pierwsze", "ten_sam_kw"], "baza")
    zd["przed"] = zd.przychod + zd.go - zd.koszt_lekarza
    kk = zd.pivot_table(index="kw", columns="kat", values="marza", aggfunc="sum", fill_value=0.0)
    kk["marza"] = kk.sum(1)
    kk["przed_kampaniami"] = kk.marza - kk.pozyskanie
    kk["zamowienia_bazy"] = zd[(zd.kat == "baza") & (zd.typ == "konsultacja")].groupby("kw").size().reindex(kk.index, fill_value=0)
    kk["pacjenci_w_bazie"] = [int((zd.loc[zd.typ == "konsultacja"].query("rodzaj == 'pierwsze'").kw < k_).sum()) for k_ in kk.index]
    kk["udzial_bazy_w_przed_proc"] = 100 * kk.baza / kk.przed_kampaniami
    kk["udzial_bazy_w_marzy_proc"] = 100 * kk.baza / kk.marza
    kk = kk.reset_index()
    kk["kwartal"] = pd.to_datetime(kk.kw).dt.year.astype(str) + "-Q" + pd.to_datetime(kk.kw).dt.quarter.astype(str)
    pokaz(kk[["kwartal", "pierwsze", "ten_sam_kw", "baza", "pozyskanie", "przed_kampaniami", "marza", "zamowienia_bazy",
              "pacjenci_w_bazie", "udzial_bazy_w_przed_proc", "udzial_bazy_w_marzy_proc"]].round(1))
    for i in range(8):
        zgodne(kk.marza[i], kw4.marza.iloc[i], "marża kwartału w części 2", tol=0.01)
    rr = []
    for i in range(4, 8):
        p_, c_ = kk.iloc[i - 4], kk.iloc[i]
        rr.append({"kwartal": c_.kwartal, "marza_zmiana_proc": 100 * (c_.marza / p_.marza - 1),
                   "baza_rok_wczesniej": p_.baza, "baza": c_.baza, "przyrost_bazy": c_.baza - p_.baza,
                   "przyrost_bazy_w_zmianie_marzy_proc": 100 * (c_.baza - p_.baza) / (c_.marza - p_.marza),
                   "marza_bez_bazy_rok_wczesniej": p_.marza - p_.baza, "marza_bez_bazy": c_.marza - c_.baza,
                   "marza_bez_bazy_zmiana_proc": 100 * ((c_.marza - c_.baza) / (p_.marza - p_.baza) - 1)})
        kp_, kc_ = p_.kwartal.replace("-Q", "_q"), c_.kwartal.replace("-Q", "_q")
        J[f"baza_udzial_w_marzy_proc_{kp_}"] = p_.udzial_bazy_w_marzy_proc
        J[f"baza_udzial_w_marzy_proc_{kc_}"] = c_.udzial_bazy_w_marzy_proc
        J[f"baza_marza_{kp_}"] = p_.baza
        J[f"baza_marza_{kc_}"] = c_.baza
        J[f"marza_zmiana_proc_{kc_}"] = 100 * (c_.marza / p_.marza - 1)
        J[f"marza_bez_bazy_zmiana_proc_{kc_}"] = 100 * ((c_.marza - c_.baza) / (p_.marza - p_.baza) - 1)
        J[f"przyrost_bazy_w_zmianie_marzy_proc_{kc_}"] = 100 * (c_.baza - p_.baza) / (c_.marza - p_.marza)
    RR = pd.DataFrame(rr)
    r("   Rok do roku: przyrost_bazy = o ile więcej marży dała baza niż rok wcześniej; marza_bez_bazy = marża bez bazy (pierwsze")
    r("   zamówienia, powroty z tego samego kwartału, minus pozyskanie).")
    pokaz(RR.round(1))
    r("   Odczyt: w IV kwartale 2024 i I kwartale 2025 baza była mała (start danych od zera), więc wzrost rok do roku w IV kwartale")
    r("   2025 i I kwartale 2026 zawiera przyrost samej bazy. W III kwartale 2025 baza była już duża, więc porównanie III kwartałów")
    r("   jest najmniej zniekształcone startem od zera (zostaje różnica w wieku bazy: rocznik okresu 1 starzeje się).")

    # =====================================================================================================
    # 3. TEST META NA L4 W PARACH WOJEWÓDZTW
    # =====================================================================================================
    naglowek("3. TEST META NA L4 W PARACH WOJEWÓDZTW: CZY 4–6 TYGODNI ODRÓŻNI WYNIK OD PROGU 85%")
    # --- 3a. próg decyzji dziś i po naprawie zwrotów ---
    pe = E.zbuduj_pe(con)
    pe["lek1"] = np.where(pe.status1.isin(["completed", "refunded"]),
                          np.where(pe.spec1 == "internista", 25.0, np.where(pe.spec1 == "psychiatra", 200.0, 100.0)), 0.0)
    g90, g180 = E.granice(90), E.granice(180)
    w90 = pe[(pe.okres == 2) & (pe.d0 >= g90[2][0]) & (pe.d0 <= g90[2][1])]
    w180 = pe[(pe.okres == 2) & (pe.d0 >= g180[2][0]) & (pe.d0 <= g180[2][1])]
    rok2 = pe[pe.okres == 2]
    wyd_meta = float(q(f"SELECT sum(spend_pln)::DOUBLE w FROM czyste.marketing_spend WHERE utm_campaign = '{META}' AND date >= DATE '{D.OKRES2}'").w[0])
    zam2 = q(f"""SELECT z.visit_purpose, z.status, z.specialization, z.refund_amount::DOUBLE zwrot, r.kampania, r.kampania_z2
                 FROM zam z JOIN zrodlo r USING (user_id) WHERE z.created_at >= TIMESTAMP '{D.OKRES2}'""")
    zam2["lekarz"] = np.where(zam2.status.isin(["completed", "refunded"]),
                              np.where(zam2.specialization == "internista", 25.0,
                                       np.where(zam2.specialization == "psychiatra", 200.0, 100.0)), 0.0)
    progi = []
    podst = {}
    for reg, kol in (("Z1K", "kampania"), ("Z2", "kampania_z2")):
        n = int((rok2[kol] == META).sum())
        m90 = w90[w90[kol] == META].marza_90.mean()
        m180 = w180[w180[kol] == META].marza_180.mean()
        l4 = zam2[(zam2.visit_purpose == "l4") & zam2.status.isin(["completed", "refunded"])]
        poz = l4[~l4[kol].isin(NOWE)]
        cel = (poz.status == "refunded").sum() / len(poz)
        mt = l4[l4[kol] == META]
        zw = mt[mt.status == "refunded"]
        x_a = max(len(zw) - len(mt) * cel, 0)
        nap_a = x_a * zw.zwrot.sum() / len(zw)
        x_b = max((len(zw) - cel * len(mt)) / (1 - cel), 0)
        wn = w90[w90[kol].isin(NOWE) & (w90.cel1 == "l4") & (w90.status1 == "refunded")]
        dalsza = (wn.marza_90 - (wn.zaplata1 - wn.zwrot1 - wn.lek1)).mean()
        nap_b = x_b * (round(zw.lekarz.mean(), 2) - dalsza)   # zaokrąglenie jak w a5e_scenariusze.py (B1)
        podst[reg] = {"n": n, "m90": m90, "m180": m180, "nap_a": nap_a, "nap_b": nap_b}
        for okno, m in ((90, m90), (180, m180)):
            for wariant, nap in (("dziś", 0.0), ("po naprawie zwrotów A", nap_a), ("po naprawie zwrotów B", nap_b)):
                marza_rok = n * m + nap
                progi.append({"regula": reg, "horyzont_dni": okno, "wariant": wariant, "nowi_rok": n, "marza_rocznika": marza_rok,
                              "wydatki": wyd_meta, "wynik": marza_rok - wyd_meta, "prog_proc": 100 * wyd_meta / marza_rok,
                              "prog_pacjentow": wyd_meta / (marza_rok / n)})
    P_ = pd.DataFrame(progi)
    zgodne(round(podst["Z1K"]["nap_a"]), 42262, "naprawa A Meta Z1K (a5e E2a)", tol=0)
    zgodne(round(podst["Z1K"]["nap_b"]), 16486, "naprawa B Meta Z1K (a5e E2a)", tol=0)
    zgodne(round(podst["Z2"]["nap_a"]), 24273, "naprawa A Meta Z2 (a5e E2a)", tol=0)
    zgodne(round(podst["Z2"]["nap_b"]), 9745, "naprawa B Meta Z2 (a5e E2a)", tol=0)
    zgodne(P_[(P_.regula == "Z1K") & (P_.horyzont_dni == 90) & (P_.wariant == "dziś")].wynik.iloc[0], 27845, "wynik Meta Z1K 90 dni", tol=1)
    r("3a. Próg decyzji = udział pacjentów dodatkowych, przy którym wyłączenie przestaje się opłacać = wydatki / marża rocznika")
    r("    przypisanych pacjentów (przed kosztem pozyskania). Wydatki i pacjenci z dni działania kampanii w okresie 2 (332 dni).")
    r("    Naprawa zwrotów A i B jak w a5e_scenariusze.py, E2a (odtworzone: 42 262 / 16 486 zł Z1K, 24 273 / 9 745 zł Z2).")
    r("    prog_pacjentow = ilu pacjentów musiałoby zniknąć po wyłączeniu, żeby utracona marża zrównała się z oszczędnością.")
    pokaz(P_.round(1))
    r("    Próg powyżej 100% (sesja płatności) znaczy, że wyłączenie opłaca się nawet wtedy, gdy wszyscy przypisani są dodatkowi.")
    r("    Próg w liczbie pacjentów prawie nie zależy od reguły; reguła zmienia tylko mianownik udziału.")
    for _, w_ in P_.iterrows():
        kl = {"dziś": "dzis", "po naprawie zwrotów A": "po_naprawie_a", "po naprawie zwrotów B": "po_naprawie_b"}[w_.wariant]
        J[f"meta_prog_proc_{w_.regula.lower()}_{w_.horyzont_dni}_dni_{kl}"] = w_.prog_proc

    # --- 3b. dane: nowi pacjenci według województwa ---
    nw = q(f"""
      SELECT k.d0, u.region, r.kampania = '{META}' meta_z1k, coalesce(r.kampania_z2 = '{META}', FALSE) meta_z2,
             f.visit_purpose = 'l4' l4
      FROM koh k JOIN czyste.users u USING (user_id) JOIN zrodlo r USING (user_id)
      JOIN zam f ON f.user_id = k.user_id AND f.nr = 1
      WHERE k.okres = 2""")
    if nw.region.isna().any():
        raise SystemExit("Pacjenci bez województwa")
    nw["d0"] = pd.to_datetime(nw.d0)
    dni = pd.date_range(D.OKRES2, KONIEC)
    woj = sorted(nw.region.unique())
    if len(woj) != 16:
        raise SystemExit(f"Oczekiwano 16 województw, jest {len(woj)}")

    def macierz(maska):
        x = nw[maska].groupby(["region", "d0"]).size().unstack("d0").reindex(index=woj, columns=dni, fill_value=0)
        return x.fillna(0).values.astype(float)
    Y = {"wszyscy": macierz(nw.d0.notna()), "L4": macierz(nw.l4)}
    Mz = {"Z1K": macierz(nw.meta_z1k), "Z2": macierz(nw.meta_z2)}
    pol = len(dni) // 2
    roz = np.log(Y["wszyscy"].sum(1))
    trend = np.log(Y["wszyscy"][:, pol:].sum(1) / Y["wszyscy"][:, :pol].sum(1))
    cechy = np.column_stack([(roz - roz.mean()) / roz.std(), (trend - trend.mean()) / trend.std()])
    pary = dobierz_pary(cechy)
    # tygodnie pełne (poniedziałek–niedziela) do opisu rozproszenia
    tyg_od = next(i for i, d in enumerate(dni) if d.weekday() == 0)
    ntyg = (len(dni) - tyg_od) // 7

    def tygodnie(Mx):
        return Mx[:, tyg_od:tyg_od + 7 * ntyg].reshape(len(woj), ntyg, 7).sum(2)
    Yt = tygodnie(Y["wszyscy"])
    ocz = Yt.sum(1, keepdims=True) / Yt.sum() * Yt.sum(0, keepdims=True)
    rozpr = ((Yt - ocz) ** 2 / ocz).sum(1) / (ntyg - 1)
    opis = pd.DataFrame({"wojewodztwo": woj, "nowi_okres2": Y["wszyscy"].sum(1).astype(int),
                         "tygodniowo": Yt.mean(1), "meta_z1k_tygodniowo": tygodnie(Mz["Z1K"]).mean(1),
                         "meta_z2_tygodniowo": tygodnie(Mz["Z2"]).mean(1),
                         "udzial_meta_z1k_proc": 100 * Mz["Z1K"].sum(1) / Y["wszyscy"].sum(1),
                         "trend_II_do_I_polrocza": np.exp(trend), "rozproszenie_tygodniowe": rozpr})
    para_nr = {}
    for i, (x, y) in enumerate(pary):
        para_nr[x] = para_nr[y] = i + 1
    opis["para"] = [para_nr[i] for i in range(len(woj))]
    r("\n3b. Nowi pacjenci okresu 2 według województwa (czyste.users.region) i pary dobrane wielkością i trendem")
    r(f"    (najmniejsza suma kwadratów odległości po standaryzacji: log liczby nowych pacjentów i log ilorazu II/I półrocza).")
    r(f"    Tygodnie pełne: {ntyg} tygodni od {dni[tyg_od]:%d.%m.%Y}. rozproszenie_tygodniowe = wariancja reszt wobec udziału")
    r("    województwa × tygodnia w kraju, podzielona przez oczekiwaną (1 = szum jak w rozkładzie Poissona).")
    pokaz(opis.sort_values(["para", "nowi_okres2"], ascending=[True, False]).round(2))
    J["test_nowi_tygodniowo_kraj"] = float(Yt.sum(0).mean())
    J["test_meta_z1k_tygodniowo_kraj"] = float(tygodnie(Mz["Z1K"]).sum(0).mean())
    J["test_meta_z2_tygodniowo_kraj"] = float(tygodnie(Mz["Z2"]).sum(0).mean())

    # --- 3c. testy pozorne ---
    q3m = q(f"""SELECT count(*) FILTER (WHERE r.kampania = '{META}') n_z1k, count(*) FILTER (WHERE r.kampania_z2 = '{META}') n_z2
                FROM koh k JOIN zrodlo r USING (user_id) WHERE k.d0 BETWEEN DATE '2026-07-01' AND DATE '{KONIEC}'""").iloc[0]
    wyd_q3 = float(q(f"""SELECT sum(spend_pln)::DOUBLE w FROM czyste.marketing_spend WHERE utm_campaign = '{META}'
                          AND date BETWEEN DATE '2026-07-01' AND DATE '{KONIEC}'""").w[0])
    tempo = {"Z1K": float(q3m.n_z1k) / 92, "Z2": float(q3m.n_z2) / 92}   # pacjenci przypisani dziennie w kraju, III kw. 2026
    I = np.array([p[0] for p in pary])
    Jx = np.array([p[1] for p in pary])
    PRZ = np.array(list(itertools.product([0, 1], repeat=len(pary))))
    T_idx = np.where(PRZ == 0, I, Jx)
    C_idx = np.where(PRZ == 0, Jx, I)
    OD_MARCA = (pd.Timestamp("2026-03-01") - pd.Timestamp(D.OKRES2)).days

    def placebo(miara, W, P, krok=7):
        Ym = Y[miara]
        wyn = {k: [] for k in ("par", "zb", "A1", "A2", "Vp", "start")}
        for s in range(P, Ym.shape[1] - W + 1, krok):
            yP, yW = Ym[:, s - P:s].sum(1), Ym[:, s:s + W].sum(1)
            a1, a2 = Mz["Z1K"][:, s:s + W].sum(1), Mz["Z2"][:, s:s + W].sum(1)
            yTP, yCP, yTW, yCW = yP[T_idx], yP[C_idx], yW[T_idx], yW[C_idx]
            wyn["par"].append((yCW * yTP / yCP - yTW).sum(1))
            sTP, sCP, sTW, sCW = yTP.sum(1), yCP.sum(1), yTW.sum(1), yCW.sum(1)
            wyn["zb"].append(sCW * sTP / sCP - sTW)
            # wariancja estymatora zbiorczego przy samym szumie Poissona (metoda delta)
            wyn["Vp"].append(sTW + (sTP / sCP) ** 2 * sCW + (sCW / sCP) ** 2 * sTP + (sCW * sTP / sCP ** 2) ** 2 * sCP)
            wyn["A1"].append(a1[T_idx].sum(1))
            wyn["A2"].append(a2[T_idx].sum(1))
            wyn["start"].append(np.full(len(PRZ), s))
        return {k: np.concatenate(v) for k, v in wyn.items()}, len(wyn["par"])

    PROG = 0.854
    r("\n3c. Testy pozorne (bez interwencji) na danych okresu 2. Pary stałe; w każdej parze jedno województwo „wyłączone”, we")
    r(f"    wszystkich {len(PRZ)} możliwych przypisaniach; okno testu przesuwane co 7 dni; okres odniesienia = 8 tygodni tuż przed")
    r("    oknem (wiersz z 16 tygodniami to sprawdzenie wrażliwości). Spadek D = oczekiwani w województwach wyłączonych − faktyczni;")
    r("    oczekiwani = kontrole w oknie × iloraz wyłączonych do kontroli z okresu odniesienia; estymator „par” liczy iloraz w każdej")
    r("    parze osobno, „zb” na sumach 8 województw. Bez interwencji D powinno wynosić 0, a jego rozrzut to szum testu.")
    r("    Udział dodatkowych = D / A_teraz, A_teraz = pacjenci, których kampania przypisałaby województwom wyłączonym w oknie")
    r(f"    w tempie III kwartału 2026 (połowa kraju: {tempo['Z1K'] * 3.5:.1f} pacjentów tygodniowo według Z1K, {tempo['Z2'] * 3.5:.1f}"
      " według Z2).")
    r("    blad = odchylenie standardowe D / A_teraz (wszystkie okna); blad_od_marca = tylko okna od 1.03.2026 (obie kampanie")
    r("    w pełnej skali); blad_D_przez_A_okna = rozrzut D / A z faktycznym A w oknie (okna od 1.03.2026).")
    r("    mde = najmniejszy wykrywalny efekt (moc 80%, alfa 5%, dwustronnie) = 2,80 × blad. P_ponizej_progu_gdy_100 = szansa, że")
    r("    test pokaże udział poniżej progu 85,4%, gdy naprawdę wszyscy są dodatkowi; P_powyzej_progu_gdy_70 = odwrotnie przy 70%.")
    wyniki_t = []
    for miara in ("wszyscy", "L4"):
        for W, P in ((28, 56), (42, 56), (56, 56), (84, 56), (42, 112)):
            res, nokien = placebo(miara, W, P)
            pozn = res["start"] >= OD_MARCA
            for est in ("par", "zb"):
                D_ = res[est]
                for reg, A_k in (("Z1K", "A1"), ("Z2", "A2")):
                    A_now = 0.5 * tempo[reg] * W
                    se = D_.std(ddof=1) / A_now
                    wyniki_t.append({"miara": miara, "tygodnie": W // 7, "odniesienie_tyg": P // 7, "estymator": est,
                                     "regula": reg, "okna": nokien, "okna_od_marca": int(pozn.sum() / len(PRZ)),
                                     "A_teraz": A_now, "srednie_D": D_.mean(), "D_sd": D_.std(ddof=1),
                                     "D_sd_od_marca": D_[pozn].std(ddof=1), "D_sd_poisson": np.sqrt(res["Vp"]).mean(),
                                     "blad_proc": 100 * se, "blad_od_marca_proc": 100 * D_[pozn].std(ddof=1) / A_now,
                                     "blad_D_przez_A_okna_proc": 100 * (D_ / res[A_k])[pozn].std(ddof=1),
                                     "mde_proc": 100 * Z_MOC * se,
                                     "P_ponizej_progu_gdy_100": 100 * 0.5 * math.erfc((1 - PROG) / se / math.sqrt(2)),
                                     "P_powyzej_progu_gdy_70": 100 * 0.5 * math.erfc((PROG - 0.70) / se / math.sqrt(2))})
    TT = pd.DataFrame(wyniki_t)
    pokaz(TT.round(1))
    r("    D_sd_poisson = średni błąd estymatora „zb” przy samym szumie Poissona (dolna granica); D_sd = zmierzony w testach pozornych.")
    glowne = TT[(TT.miara == "wszyscy") & (TT.odniesienie_tyg == 8) & (TT.regula == "Z1K")]
    najl = glowne.groupby("tygodnie").blad_proc.min()
    najl_m = glowne.groupby("tygodnie").blad_od_marca_proc.min()
    for tyg in (4, 6, 8, 12):
        x = glowne[glowne.tygodnie == tyg].sort_values("blad_proc").iloc[0]
        J[f"test_blad_udzialu_proc_{tyg}_tyg_z1k"] = x.blad_proc
        J[f"test_blad_udzialu_od_marca_proc_{tyg}_tyg_z1k"] = najl_m[tyg]
        J[f"test_mde_proc_{tyg}_tyg_z1k"] = x.mde_proc
        J[f"test_A_teraz_pacjentow_{tyg}_tyg_z1k"] = x.A_teraz
        J[f"test_P_ponizej_progu_gdy_100_proc_{tyg}_tyg"] = x.P_ponizej_progu_gdy_100
        J[f"test_P_powyzej_progu_gdy_70_proc_{tyg}_tyg"] = x.P_powyzej_progu_gdy_70
        J[f"test_blad_udzialu_proc_{tyg}_tyg_z2"] = TT[(TT.miara == "wszyscy") & (TT.odniesienie_tyg == 8) & (TT.regula == "Z2")
                                                        & (TT.tygodnie == tyg)].blad_proc.min()
        J[f"test_blad_udzialu_proc_{tyg}_tyg_z1k_miara_L4"] = TT[(TT.miara == "L4") & (TT.odniesienie_tyg == 8)
                                                                  & (TT.regula == "Z1K") & (TT.tygodnie == tyg)].blad_proc.min()
    se6 = najl[6] / 100
    tyg_potrz = 6 * (Z_MOC * se6 / 0.146) ** 2
    J["test_tygodnie_potrzebne_mde_14_6_proc"] = tyg_potrz
    J["test_tempo_q3_meta_z1k_dziennie"] = tempo["Z1K"]
    J["test_tempo_q3_meta_z2_dziennie"] = tempo["Z2"]
    r(f"    Lepszy z dwóch estymatorów, wszyscy nowi pacjenci, Z1K: błąd udziału {najl[4]:.1f} punktu procentowego przy 4 tygodniach,"
      f" {najl[6]:.1f} przy 6, {najl[8]:.1f} przy 8 i {najl[12]:.1f} przy 12 (okna od marca: {najl_m[4]:.1f}, {najl_m[6]:.1f},"
      f" {najl_m[8]:.1f}, {najl_m[12]:.1f}).")
    r(f"    Najmniejszy wykrywalny efekt: {Z_MOC * najl[4]:.0f} punktów przy 4 tygodniach i {Z_MOC * najl[6]:.0f} przy 6. Odróżnienie 100% od"
      " 85,4% (14,6 punktu) albo 85,4% od 70% (15,4 punktu)")
    r(f"    wymaga błędu około {str(round(100 * 0.146 / Z_MOC, 1)).replace('.', ',')} punktu. Przy spadku błędu jak 1/√tygodni to około {tyg_potrz:.0f} tygodni testu"
      " w tym układzie (ekstrapolacja z 6 tygodni; dłuższe okna pozorne pokazują, czy błąd naprawdę tak spada).")
    for tyg in (4, 6):
        mde = Z_MOC * najl[tyg]
        r(f"    {tyg} tygodni: najmniejszy wykrywalny efekt {mde:.0f} punktów; odróżni 100% od 85,4%: {'tak' if mde <= 14.6 else 'nie'};"
          f" odróżni 85,4% od 70%: {'tak' if mde <= 15.4 else 'nie'}; przy 100% dodatkowych wynik poniżej progu w "
          f"{J[f'test_P_ponizej_progu_gdy_100_proc_{tyg}_tyg']:.0f}% testów, przy 70% powyżej progu w "
          f"{J[f'test_P_powyzej_progu_gdy_70_proc_{tyg}_tyg']:.0f}%.")
    r(f"    Sama miara „nowi pacjenci z pierwszym L4” (zakłada, że kampania nie zmienia liczby pacjentów z innymi usługami) daje błąd"
      f" {J['test_blad_udzialu_proc_6_tyg_z1k_miara_L4']:.1f} punktu przy 6 tygodniach, nadal za dużo. Szum jest prawie czysto")
    r("    poissonowski (D_sd ≈ D_sd_poisson), więc lepszy dobór par go nie usunie; pomaga tylko więcej pacjentów w teście.")

    # --- 3d. koszt testu ---
    koszt = []
    for reg in ("Z1K", "Z2"):
        p = podst[reg]
        wyn_rok = p["n"] * p["m90"] - wyd_meta
        n_q3 = float(q3m.n_z1k if reg == "Z1K" else q3m.n_z2)
        for tyg in (4, 6):
            koszt.append({"regula": reg, "tygodnie": tyg,
                          "jak_c_priorytety_dni_dzialania": wyn_rok * tyg / 52 * 0.5,
                          "jak_c_priorytety_pelny_rok": wyn_rok * 365 / 332 * tyg / 52 * 0.5,
                          "tempo_III_kw_2026": (n_q3 * p["m90"] - wyd_q3) / 92 * 7 * tyg * 0.5,
                          "tempo_III_kw_po_naprawie_A": (n_q3 * (p["m90"] + p["nap_a"] / p["n"]) - wyd_q3) / 92 * 7 * tyg * 0.5})
    K_ = pd.DataFrame(koszt)
    r("\n3d. Koszt testu = utracona marża − oszczędzone wydatki w województwach wyłączonych (połowa ruchu), gdy wszyscy przypisani")
    r("    są dodatkowi (najgorszy przypadek; przy udziale równym progowi koszt = 0, poniżej progu test daje zysk). Ujemna kwota =")
    r("    zysk. Marża na pacjenta w 90 dniach z kohort 1.10.2025–2.07.2026 (Z1K 37,8 zł, Z2 37,4 zł), także dla pacjentów III kwartału.")
    r(f"    Tempo III kwartału 2026 (92 dni): {int(q3m.n_z1k)} pacjentów (Z1K), {int(q3m.n_z2)} (Z2), wydatki {zl(wyd_q3)}.")
    pokaz(K_.round(0))
    z_raportu("c_priorytety.txt", "1 606 zł w dniach działania, 1 766 zł na pełny rok")
    for _, w_ in K_.iterrows():
        J[f"test_koszt_{w_.tygodnie}_tyg_{w_.regula.lower()}_tempo_q3"] = w_.tempo_III_kw_2026
        J[f"test_koszt_{w_.tygodnie}_tyg_{w_.regula.lower()}_pelny_rok"] = w_.jak_c_priorytety_pelny_rok
        J[f"test_koszt_{w_.tygodnie}_tyg_{w_.regula.lower()}_tempo_q3_po_naprawie_a"] = w_.tempo_III_kw_po_naprawie_A

    wyn_z1k = P_[(P_.regula == "Z1K") & (P_.horyzont_dni == 90) & (P_.wariant == "dziś")].wynik.iloc[0]
    r("\n3e. Reguła na wynik niejednoznaczny (do ustalenia z góry przez właściciela; warianty, bez rozstrzygnięcia):")
    r("    A. Status quo: jeśli 95% przedział udziału obejmuje próg, kampania zostaje bez zmian. Chroni przed utratą pacjentów,")
    r(f"       ale utrzymuje wydatek, który może być stratą (przy 0% dodatkowych {zl(wyd_meta)} w dniach działania).")
    r("    B. Domyślnie wyłączamy (decyzja odwracalna): przy wyniku niejednoznacznym kampania zostaje wyłączona i wraca, jeśli")
    r(f"       pozyskanie spadnie. Najgorszy koszt błędu (100% dodatkowych, Z1K, 90 dni) to {zl(wyn_z1k)} w dniach działania;")
    r("       według sesji płatności wyłączenie opłaca się w każdym wariancie.")
    r("    C. Przedłużenie ustalone z góry: punkty kontrolne co 2 tygodnie, decyzja, gdy przedział wykluczy próg, najdłużej N tygodni")
    r(f"       (według 3c około {tyg_potrz:.0f} tygodni, żeby odróżnić 100% od 85%); po N tygodniach wariant A albo B.")
    r("    D. Mniejszy budżet zamiast zero-jedynkowo: przy wyniku niejednoznacznym połowa budżetu i dalszy pomiar.")
    r("    E. Decyzja na wartości oczekiwanej: działanie z większą oczekiwaną marżą przy rozkładzie udziału z testu; uwzględnia")
    r(f"       asymetrię strat (wyłączenie przy 100% dodatkowych traci {zl(wyn_z1k)}, utrzymanie przy 0% traci {zl(wyd_meta)}).")
    r("    Ryzyka projektu: (1) wspólna, ogólnopolska obsada lekarzy — wyłączenie zmniejsza obciążenie internistów, więc w")
    r("    województwach kontrolnych może przybyć wolnych terminów, zakupów i powrotów; to zawyża spadek D (więcej „dodatkowych”),")
    r("    a wynik w retencji przenosi się na kontrole; (2) województwo konta (users.region) to nie miejsce wyświetlenia reklamy,")
    r("    więc część reklam „przecieka” między województwami i zaniża D; (3) wydatków nie ma w podziale na województwa, więc")
    r("    oszczędność w województwach wyłączonych trzeba wziąć z panelu Mety; (4) zakup bywa do 7 dni po wejściu, więc brzegi")
    r("    okna przesuwają kilka procent pacjentów.")

    # =====================================================================================================
    # 4. PORANNA OBSADA
    # =====================================================================================================
    naglowek("4. POZYCJA 6 (PORANNA OBSADA INTERNISTÓW): SKĄD ZAKRES 0–65,2 TYS. ZŁ I JAKIE SĄ WARIANTY")
    o1 = pe[pe.okres == 1].assign(m1_180=lambda x: x.marza_180 - x.marza_0, pow90=lambda x: x.dni_R2.fillna(10 ** 6) <= 90)
    wr, nwr = o1[o1.pow90].m1_180.mean(), o1[~o1.pow90].m1_180.mean()
    WART = round(wr - nwr, 1)
    zgodne(WART, 95.6, "wartość powrotu (ZALOZENIA.md 38)", tol=0.01)
    sp = spadki_retencji()
    r(f"   Wartość powrotu = marża dni 1–180 pacjenta, który wrócił w 90 dniach ({wr:.1f} zł, {int(o1.pow90.sum())} pacjentów okresu 1),")
    r(f"   minus marża tego, który nie wrócił ({nwr:.1f} zł, {int((~o1.pow90).sum())}) = {WART} zł (różnica obserwacyjna, ZALOZENIA.md 38).")
    r("   Scenariusz = spadek powrotu w 90 dniach (punkty procentowe) × pacjenci okresu 2 starych kampanii × 95,6 zł, marża w 180 dniach")
    r("   na rok. Spadki z a5r_zdarzenia.txt (a5r_struktura sekcja 5 i a5r_punktualnosc 1g).")

    # najwęższy wariant: tylko poranne wizyty u internisty (rozkład 1g z porą terminu w komórce)
    zbuduj_atr(con)
    zbuduj_wizyty(con)
    atr = q("""SELECT a.*, w.koszyk, w.pora, w.op, w.specialization spec
               FROM atr a JOIN wiz w ON w.user_id = a.user_id AND w.nr = 1""")
    atr["d0"] = pd.to_datetime(atr.d0)
    atr["dni_R2"] = atr.dni_R2.astype(float)
    a90 = proba(atr, 90)
    stare = a90[~a90.kampania.isin(NOWE)]
    s2 = a90[~a90.kampania_z2.isin(NOWE)]
    s2 = s2.assign(kampania=s2.kampania_z2)
    wariant = []
    for reg, dane, n_old in (("Z1K", stare, sp["caly_Z1K"][1]), ("Z2", s2, sp["caly_Z2"][1])):
        ref = rozklad_zagniezdzony(dane, ["kampania", "usluga"])
        ref_p = rozklad_zagniezdzony(dane, ["kampania", "usluga", "pora"])
        zgodne(ref["punktualnosc_wizyty_odbyte"], sp[f"opoznienia_{reg}"][0] * -1, f"punktualność 1g {reg}", tol=0.006)
        pw = pun_wiersze(dane, ["kampania", "usluga", "pora"])
        odb = pw[pw.koszyk != "brak_wizyty"]
        zgodne(round(100 * odb.pun.sum(), 2), ref_p["punktualnosc_wizyty_odbyte"], f"suma wierszy punktualności {reg}", tol=0.006)
        rano_int = odb[(odb.pora == "a_rano_6_11") & odb.usluga.str.startswith("internista")].pun.sum()
        rano = odb[odb.pora == "a_rano_6_11"].pun.sum()
        sp_caly, sp_waski = sp[f"caly_{reg}"][0], sp[f"opoznienia_{reg}"][0]
        for nazwa, pkt in (("brak efektu", 0.0),
                           ("najwęższy: punktualność tylko porannych pierwszych wizyt u internisty (komórka z porą)", -100 * rano_int),
                           ("pomocniczo: punktualność porannych pierwszych wizyt u wszystkich lekarzy", -100 * rano),
                           ("wąski: zmiana rozkładu opóźnień pierwszej wizyty, wszystkie pory i lekarze (1g)", sp_waski),
                           ("szeroki: cały spadek powrotu w starych kampaniach", sp_caly)):
            wariant.append({"regula": reg, "wariant": nazwa, "spadek_pkt": pkt, "pacjenci_starych": n_old,
                            "powrotow_mniej": pkt / 100 * n_old, "marza_180_dni_rocznie": pkt / 100 * n_old * WART})
    V_ = pd.DataFrame(wariant)
    pokaz(V_.round(2))
    for t_ in ("0.76             17419             132         12656", "0.64             19500             125         11931",
               "1.91             17419             333         31806", "3.50             19500             683         65247"):
        z_raportu("a5e_scenariusze.txt", t_)
    r("   Wąski i szeroki odtwarzają a5e_scenariusze.txt, C (11 931–12 656 i 31 806–65 247 zł). Zakres „0–65,2 tys. zł” w P8 to")
    r("   od wariantu „brak efektu” do szerokiego wariantu według sesji płatności. Szeroki przypisuje opóźnieniom cały spadek powrotu")
    r("   w starych kampaniach (także części niezwiązane z wizytą), więc nie jest górną granicą skutku obsady. Wąski obejmuje")
    r("   opóźnienia o każdej porze i u każdego lekarza; obsada poranna mogłaby zmienić tylko część poranną (wariant najwęższy).")
    r("   Wszystkie warianty zakładają, że opóźnienie obniża powrót (zależność obserwacyjna) i że powrót jest wart 95,6 zł.")
    r("   Koszt dodatkowej obsady nie jest w danych, więc wartości netto nie da się policzyć.")
    for _, w_ in V_.iterrows():
        kl = w_.wariant.split(":")[0].replace(" ", "_").translate(str.maketrans("ąęłńóśżź", "aelnoszz"))
        J[f"poranek_{kl}_{w_.regula.lower()}_zl"] = w_.marza_180_dni_rocznie
        J[f"poranek_{kl}_{w_.regula.lower()}_pkt"] = w_.spadek_pkt

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    J = {k: (round(float(v), 4) if v is not None and not (isinstance(v, float) and math.isnan(v)) else None) for k, v in J.items()}
    with open(WYNIK_JSON, "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1)
    print(f"Zapisano {WYNIK} ({len(linie)} linii) i {WYNIK_JSON} ({len(J)} liczb)")


if __name__ == "__main__":
    main()
