"""G — pierwsza zakładka od nowa: liczby do werdyktu „czy to wzrost” (wątek Kuby z 2026-10-23, po publikacji).

Kuba zatrzymał się na zdaniu, że marża po wszystkich kosztach wzrosła o 27%, i zapytał, dlaczego w takim razie werdykt
brzmi „Nie”. Jego hipoteza: prawie cały przyrost pacjentów dały dwie nowe kampanie na L4, na ich pacjencie po koszcie
pozyskania prawie nic nie zostaje (od wiosny dokładamy), a marża rośnie głównie dzięki powrotom pacjentów z pierwszego
roku. Ten skrypt sprawdza ją kodem, zanim cokolwiek trafi na stronę:

  G1. jaką część przyrostu nowych pacjentów dały dwie nowe kampanie na L4 (obie reguły źródła);
  G2. ile zostaje z jednego nowego pacjenta: marża w 180 dniach minus koszt jego pozyskania, rok do roku, płatne
      z płatnymi (nowe kampanie na L4 wobec pozostałych kampanii płatnych), obok przybliżenie dla całego rocznika;
  G3. to samo dla nowych kampanii na L4 miesiąc po miesiącu: od którego miesiąca koszt pozyskania przekracza wszystko,
      co pacjent zostawia (marża w 180 dniach; dla młodszych kohort przybliżenie);
  G4. rozbicie przyrostu marży po wszystkich kosztach (828 → 1 048 tys. zł) na pacjentów pozyskanych rok wcześniej
      i na wynik pacjentów pozyskanych w danym roku po kosztach kampanii, z tym samym rachunkiem rok wcześniej.

Definicje bez zmian (analiza/definicje.py, ZALOZENIA.md 16–43), ekonomia kampanii jak w analiza/a5e_ekonomia.py
(koszt pozyskania = wydatki i prowizja z tych samych dni co kohorty / nowi pacjenci; marża przed kosztem pozyskania =
przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza). Liczby przepisane z wcześniejszych raportów skrypt
sprawdza w tych raportach (z_raportu), więc żadna nie przechodzi „z pamięci”.

Przybliżenie marży w 180 dniach dla kohort bez pełnego okna (G2b, G3): marża w najdłuższym pełnym oknie pacjenta
(90, 30 albo 0 dni) + średni przyrost marży od tego okna do 180 dni, zmierzony na kohortach tej samej grupy z pełnym
oknem 180 dni (1.10.2025–3.04.2026). Założenie: młodsze kohorty dorabiają po pierwszym zamówieniu tyle samo co starsze
(ten sam sposób co d_kampanie.py, 2b). Przedział 95% jest warunkowy: rozrzut marży i przyrostu, przy stałym koszcie
pozyskania i wybranej regule źródła.

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/g_werdykt.py
Wynik: analiza/wyniki/g_werdykt.txt i analiza/wyniki/g_werdykt.json
"""

import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
import a5e_ekonomia as E  # noqa: E402

WYNIKI = os.path.join(D.KATALOG, "analiza", "wyniki")
WYNIK = os.path.join(WYNIKI, "g_werdykt.txt")
WYNIK_JSON = os.path.join(WYNIKI, "g_werdykt.json")
NOWE = E.NOWE
PROWIZJA = E.PROWIZJA
GRUPY = {"1_nowe_kampanie_L4": "nowe kampanie na L4", "2_pozostale_platne": "pozostałe kampanie płatne",
         "3_afiliacja_ranking": "ranking lekarzy (afiliacja)", "4_bezplatne": "kanały bezpłatne"}
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)


def z_raportu(plik, tekst, wartosc):
    """Liczba przepisana z raportu: sprawdza, że `tekst` stoi w pliku `plik` (analiza/wyniki), i zwraca `wartosc`."""
    with open(os.path.join(WYNIKI, plik), encoding="utf-8") as f:
        if tekst not in f.read():
            raise ValueError(f"W raporcie {plik} nie ma tekstu {tekst!r} — liczba nieaktualna")
    return wartosc


def zl(x):
    return f"{x:,.0f}".replace(",", " ")


def okna_pelne():
    """Ostatni dzień kohorty z pełnym oknem 180, 90, 30 i 0 dni (czas polski, koniec danych 30.09.2026)."""
    return {w: pd.Timestamp(D.granice_por(w)[1]) if w else pd.Timestamp(D.KONIEC) for w in (180, 90, 30, 0)}


def marza_180_przybl(pe, maska_grupy, kol_marzy=("marza_0", "marza_30", "marza_90", "marza_180")):
    """Dla pacjentów okresu 2 z maski: marża w najdłuższym pełnym oknie i przybliżenie marży w 180 dniach.
    Zwraca (ramka z kolumnami okno, m_obs, m180_przybl; słownik przyrostów i ich wariancji)."""
    gr = okna_pelne()
    p = pe[maska_grupy & (pe.okres == 2)].copy()
    p["okno"] = np.select([p.d0 <= gr[180], p.d0 <= gr[90], p.d0 <= gr[30]], [180, 90, 30], 0)
    wczesne = p[p.okno == 180]
    przyrost, war = {180: 0.0}, {180: 0.0}
    for w in (90, 30, 0):
        roz = wczesne["marza_180"] - wczesne[f"marza_{w}"]
        przyrost[w] = float(roz.mean()) if len(roz) else np.nan
        war[w] = float(roz.var(ddof=1) / len(roz)) if len(roz) > 1 else np.nan
    p["m_obs"] = np.select([p.okno == 180, p.okno == 90, p.okno == 30], [p.marza_180, p.marza_90, p.marza_30], p.marza_0)
    p["m180_przybl"] = p.m_obs + p.okno.map(przyrost)
    return p, przyrost, war, len(wczesne)


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=True)
    pe = E.zbuduj_pe(con)
    wyd = E.zbuduj_wyd(con)
    linie, J = [], {}

    def r(tekst=""):
        linie.append(tekst)

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    def naglowek(t):
        r("\n" + "=" * 110)
        r(t)
        r("=" * 110)

    r(f"G — LICZBY DO WERDYKTU „CZY TO WZROST” ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026. Z1K = przyjęta reguła źródła (pierwsze wejście, kod kampanii")
    r("rozstrzyga), Z2 = sesja płatności. Nowe kampanie na L4 = meta_prosp_l4_szybko (od 3.11.2025) i tt_prosp_l4_15min")
    r("(od 9.02.2026). Pozostałe kampanie płatne = Google Ads, Meta lekarz online, remarketing Meta (płatne za klik, z")
    r("marketing_spend). Ranking lekarzy (afiliacja, prowizja 25 zł za pacjenta) osobno, obok jako wariant „płatne z afiliacją”.")

    # ======================= G1 =======================
    naglowek("G1. PRZYROST NOWYCH PACJENTÓW I UDZIAŁ DWÓCH NOWYCH KAMPANII NA L4")
    g1 = []
    for reg in ("Z1K", "Z2"):
        kol = f"grupa_{reg}"
        t = pe.groupby(["okres", kol]).size().unstack(0).fillna(0).astype(int)
        t.columns = ["okres_1", "okres_2"]
        t["przyrost"] = t.okres_2 - t.okres_1
        razem = t.sum()
        t["udzial_w_przyroscie_proc"] = (100 * t.przyrost / razem.przyrost).round(1)
        t = t.reset_index().rename(columns={kol: "grupa"})
        t.insert(0, "regula", reg)
        g1.append(t)
        r(f"\n   reguła {reg}:")
        pokaz(t)
        r(f"     razem: okres 1 {razem.okres_1}, okres 2 {razem.okres_2}, przyrost {razem.przyrost}")
    g1 = pd.concat(g1)
    n1, n2 = int((pe.okres == 1).sum()), int((pe.okres == 2).sum())
    przyrost = n2 - n1
    z_raportu("c_priorytety.txt", "     zmiana %: nowi: +52.1%", None)
    nk = {reg: int(g1[(g1.regula == reg) & (g1.grupa == "1_nowe_kampanie_L4")].okres_2.iloc[0]) for reg in ("Z1K", "Z2")}
    meta = int(((pe.okres == 2) & (pe.kampania == "meta_prosp_l4_szybko")).sum())
    tt = int(((pe.okres == 2) & (pe.kampania == "tt_prosp_l4_15min")).sum())
    r(f"\n   Przyrost nowych pacjentów: {n1} → {n2}, +{przyrost} (+{100 * (n2 / n1 - 1):.1f}%).")
    for reg in ("Z1K", "Z2"):
        r(f"   {reg}: nowe kampanie na L4 {nk[reg]} pacjentów = {100 * nk[reg] / przyrost:.1f}% przyrostu; "
          f"bez nich przyrost {przyrost - nk[reg]} (+{100 * ((n2 - nk[reg]) / n1 - 1):.1f}%).")
    r(f"   Z1K według kampanii: Meta na L4 {meta}, TikTok na L4 {tt}.")
    J["g1"] = {"nowi_o1": n1, "nowi_o2": n2, "przyrost": przyrost, "przyrost_proc": 100 * (n2 / n1 - 1),
               "nowe_z1k": nk["Z1K"], "nowe_z2": nk["Z2"], "nowe_meta_z1k": meta, "nowe_tiktok_z1k": tt,
               "udzial_nowych_w_przyroscie_z1k": 100 * nk["Z1K"] / przyrost,
               "udzial_nowych_w_przyroscie_z2": 100 * nk["Z2"] / przyrost,
               "grupy": g1.to_dict(orient="records")}

    # ======================= G2 =======================
    naglowek("G2. ILE ZOSTAJE Z JEDNEGO NOWEGO PACJENTA: MARŻA W 180 DNIACH MINUS KOSZT POZYSKANIA, PŁATNE Z PŁATNYMI")
    r("   Okno 180 dni: kohorty 1.10–3.04 w obu okresach (te same dni kalendarzowe). Koszt pozyskania = wydatki kampanii")
    r("   z tych samych dni (+ prowizja 25 zł za pacjenta rankingu) / nowi pacjenci. Przedział 95% warunkowy (rozrzut marży).")

    def zestaw(grupy, regula, okno, okres):
        """Wynik dla zbioru grup: pacjenci, wydatki tych grup z dni kohort okna, prowizja, marża, wynik."""
        od, do = E.granice(okno)[okres]
        kg = f"grupa_{regula}"
        kk = "kanal" if regula == "Z1K" else "kanal_z2"
        p = pe[(pe.okres == okres) & (pe.d0 >= od) & (pe.d0 <= do) & pe[kg].isin(grupy)]
        wy = float(wyd[(wyd.d >= od) & (wyd.d <= do) & wyd.grupa.isin(grupy)].wydatki.sum())
        prow = PROWIZJA * float((p[kk] == "afiliacja_ranking").sum())
        n = len(p)
        if n == 0:
            return None
        m = p[f"marza_{okno}"]
        koszt = (wy + prow) / n
        se = m.std(ddof=1) / np.sqrt(n)
        return {"regula": regula, "okno": okno, "okres": okres, "grupy": "+".join(g[0] for g in grupy), "nowi": n,
                "wydatki_zl": round(wy), "prowizja_zl": round(prow), "koszt_pozysk": koszt, "marza": float(m.mean()),
                "wynik": float(m.mean() - koszt), "wynik_od": float(m.mean() - koszt - 1.96 * se),
                "wynik_do": float(m.mean() - koszt + 1.96 * se), "wynik_razem_zl": float((m.mean() - koszt) * n)}

    ZESTAWY = [("1",), ("2",), ("3",), ("1", "2"), ("1", "2", "3")]
    pelne = {k: v for k, v in zip("1234", GRUPY)}
    g2 = []
    for okno in (180, 90):
        for reg in ("Z1K", "Z2"):
            for z in ZESTAWY:
                for o in (1, 2):
                    w = zestaw([pelne[x] for x in z], reg, okno, o)
                    if w:
                        g2.append(w)
    g2 = pd.DataFrame(g2)
    for okno in (180, 90):
        r(f"\n2{'a' if okno == 180 else 'c'}. Okno {okno} dni (grupy: 1 = nowe kampanie na L4, 2 = pozostałe kampanie płatne, "
          "3 = ranking lekarzy; 1+2 = wszystkie kampanie płatne za klik; 1+2+3 = z afiliacją)")
        pokaz(g2[g2.okno == okno].drop(columns="okno").round(1))
    # kontrola zgodności z a5e_ekonomia.txt (1b)
    k = g2[(g2.okno == 180) & (g2.regula == "Z1K") & (g2.grupy == "1") & (g2.okres == 2)].iloc[0]
    z_raportu("a5e_ekonomia.txt", "      1_nowe_kampanie_L4    Z1K      2  2352       71325            0                 30.3          37.3           7.0",
              None)
    assert (k.nowi, round(k.koszt_pozysk, 1), round(k.marza, 1), round(k.wynik, 1)) == (2352, 30.3, 37.3, 7.0), k
    k = g2[(g2.okno == 180) & (g2.regula == "Z1K") & (g2.grupy == "2")]
    z_raportu("a5e_ekonomia.txt", "      2_pozostale_platne    Z1K      1  4717      193425            0                 41.0          72.8          31.8", None)
    assert [round(x, 1) for x in k.wynik] == [31.8, 29.7], k
    r("   Kontrola: nowe kampanie (Z1K, 180 dni) i pozostałe płatne (Z1K, 180 dni) zgodne z a5e_ekonomia.txt, 1b.")

    # 2b: cały rocznik — okres 1 ma pełne 180 dni dla wszystkich kohort, okres 2 przybliżenie
    r("\n2b. Cały rocznik (wszystkie kohorty okresu, koszt pozyskania z wydatków i prowizji całego okresu). Okres 1: marża w")
    r("    180 dniach zmierzona dla wszystkich kohort (ostatnia 30.09.2025, pełne okno). Okres 2: przybliżenie (opis na górze")
    r("    skryptu); okno_* = ilu pacjentów ma marżę z pełnego okna 180, 90, 30 i 0 dni.")
    rocz = []
    for reg in ("Z1K", "Z2"):
        kg = f"grupa_{reg}"
        kk = "kanal" if reg == "Z1K" else "kanal_z2"
        for z in ZESTAWY:
            grupy = [pelne[x] for x in z]
            for o in (1, 2):
                od, do = E.granice(None)[o]
                maska = pe[kg].isin(grupy)
                wy = float(wyd[(wyd.d >= od) & (wyd.d <= do) & wyd.grupa.isin(grupy)].wydatki.sum())
                if o == 1:
                    p = pe[maska & (pe.okres == 1)]
                    if not len(p):
                        continue
                    m = p.marza_180
                    se = m.std(ddof=1) / np.sqrt(len(p))
                    okna = {180: len(p), 90: 0, 30: 0, 0: 0}
                else:
                    p, prz, war, n180 = marza_180_przybl(pe, maska)
                    if not len(p):
                        continue
                    m = p.m180_przybl
                    se2 = p.m_obs.var(ddof=1) / len(p) + sum(war[w] * (p.okno == w).mean() ** 2 for w in (90, 30, 0))
                    se = np.sqrt(se2)
                    okna = {w: int((p.okno == w).sum()) for w in (180, 90, 30, 0)}
                prow = PROWIZJA * float((p[kk] == "afiliacja_ranking").sum())
                koszt = (wy + prow) / len(p)
                rocz.append({"regula": reg, "grupy": "+".join(z), "okres": o, "nowi": len(p), "wydatki_zl": round(wy),
                             "prowizja_zl": round(prow), "koszt_pozysk": koszt, "marza180": float(m.mean()),
                             "wynik": float(m.mean() - koszt), "wynik_od": float(m.mean() - koszt - 1.96 * se),
                             "wynik_do": float(m.mean() - koszt + 1.96 * se), "wynik_razem_zl": float((m.mean() - koszt) * len(p)),
                             **{f"okno_{w}": v for w, v in okna.items()}})
    rocz = pd.DataFrame(rocz)
    pokaz(rocz.round(1))
    J["g2"] = {"okno": g2.to_dict(orient="records"), "rocznik": rocz.to_dict(orient="records")}

    # ======================= G3 =======================
    naglowek("G3. NOWE KAMPANIE NA L4 MIESIĄC PO MIESIĄCU: KOSZT POZYSKANIA A WSZYSTKO, CO PACJENT ZOSTAWIA (180 DNI)")
    r("   miesiąc = miesiąc pierwszego zakupu (kohorta); wydatki = wydatki kampanii w tym miesiącu; koszt = wydatki / nowi.")
    r("   marza180 = zmierzona, gdy cała kohorta ma pełne 180 dni (do 3.04.2026); dla młodszych przybliżenie: marża w najdłuższym")
    r("   pełnym oknie pacjenta + przyrost do 180 dni zmierzony na kohortach 1.10.2025–3.04.2026 tej samej grupy i reguły.")
    r("   okno = najkrótsze pełne okno w miesiącu (180, 90, 30, 0). wynik = marza180 − koszt; przedział 95% warunkowy.")
    g3, prz_all = [], {}
    for nazwa, kampanie in (("razem", NOWE), ("meta", ("meta_prosp_l4_szybko",)), ("tiktok", ("tt_prosp_l4_15min",))):
        for reg in ("Z1K", "Z2"):
            kc = "kampania" if reg == "Z1K" else "kampania_z2"
            p, prz, war, n180 = marza_180_przybl(pe, pe[kc].isin(kampanie))
            prz_all[f"{nazwa}_{reg}"] = {"przyrost_do_180": {str(k): v for k, v in prz.items()}, "pacjenci_z_pelnym_180": n180}
            p["miesiac"] = p.d0.dt.to_period("M")
            p["kwartal"] = p.d0.dt.to_period("Q")
            w = wyd[wyd.kampania.isin(kampanie) & (wyd.d >= "2025-10-01")].copy()
            w["miesiac"] = w.d.dt.to_period("M")
            w["kwartal"] = w.d.dt.to_period("Q")
            for poziom in ("miesiac", "kwartal"):
                wk = w.groupby(poziom).wydatki.sum()
                for okres_, g in p.groupby(poziom):
                    n = len(g)
                    koszt = float(wk.get(okres_, 0.0)) / n
                    se2 = g.m_obs.var(ddof=1) / n + sum(war[x] * (g.okno == x).mean() ** 2 for x in (90, 30, 0))
                    m = float(g.m180_przybl.mean())
                    g3.append({"kampanie": nazwa, "regula": reg, "poziom": poziom, "okres": str(okres_), "nowi": n,
                               "wydatki_zl": round(float(wk.get(okres_, 0.0))), "koszt_pozysk": koszt,
                               "okno": int(g.okno.min()), "marza180": m, "wynik": m - koszt,
                               "wynik_od": m - koszt - 1.96 * np.sqrt(se2), "wynik_do": m - koszt + 1.96 * np.sqrt(se2),
                               "wynik_razem_zl": (m - koszt) * n,
                               "powrot90_proc": float(100 * (g[g.okno >= 90].dni_R2.fillna(10 ** 6) <= 90).mean())
                               if (g.okno >= 90).any() else np.nan})
    g3 = pd.DataFrame(g3)
    for nazwa in ("razem", "meta", "tiktok"):
        for reg in ("Z1K", "Z2"):
            r(f"\n   {nazwa}, {reg}: przyrost marży do 180 dni zmierzony na {prz_all[f'{nazwa}_{reg}']['pacjenci_z_pelnym_180']} "
              f"pacjentach: od 90 dni {prz_all[f'{nazwa}_{reg}']['przyrost_do_180']['90']:.2f} zł, od 30 dni "
              f"{prz_all[f'{nazwa}_{reg}']['przyrost_do_180']['30']:.2f} zł, od dnia 0 {prz_all[f'{nazwa}_{reg}']['przyrost_do_180']['0']:.2f} zł")
            for poziom in ("miesiac", "kwartal"):
                t = g3[(g3.kampanie == nazwa) & (g3.regula == reg) & (g3.poziom == poziom)].drop(columns=["kampanie", "regula", "poziom"])
                pokaz(t.round(1))
    # pierwszy miesiąc z wynikiem ujemnym
    pierwszy = {}
    for nazwa in ("razem", "meta", "tiktok"):
        for reg in ("Z1K", "Z2"):
            t = g3[(g3.kampanie == nazwa) & (g3.regula == reg) & (g3.poziom == "miesiac")].sort_values("okres")
            uj = t[t.wynik < 0]
            uj_pewne = t[t.wynik_do < 0]
            # od którego miesiąca wynik jest ujemny w każdym kolejnym miesiącu
            od_kiedy = None
            for i in range(len(t)):
                if (t.wynik.iloc[i:] < 0).all():
                    od_kiedy = t.okres.iloc[i]
                    break
            pierwszy[f"{nazwa}_{reg}"] = {"pierwszy_ujemny": uj.okres.iloc[0] if len(uj) else None,
                                         "pierwszy_ujemny_z_przedzialem_ponizej_zera": uj_pewne.okres.iloc[0] if len(uj_pewne) else None,
                                         "ujemny_w_kazdym_miesiacu_od": od_kiedy,
                                         "miesiace_ujemne": list(uj.okres), "miesiace_ujemne_pewne": list(uj_pewne.okres)}
    r("\n   Pierwszy miesiąc z wynikiem ujemnym (wynik < 0), z przedziałem w całości poniżej zera, i miesiąc, od którego wynik")
    r("   jest ujemny w każdym kolejnym miesiącu:")
    for k_, v in pierwszy.items():
        r(f"     {k_}: {v}")
    J["g3"] = {"tabela": g3.to_dict(orient="records"), "przyrosty": prz_all, "pierwszy_ujemny": pierwszy}

    # ======================= G4 =======================
    naglowek("G4. PRZYROST MARŻY PO WSZYSTKICH KOSZTACH (828 → 1 048 TYS. ZŁ): PACJENCI Z PIERWSZEGO ROKU A NOWI PACJENCI ROKU")
    r("   Marża przed kampaniami = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza, w roku kalendarzowym")
    r("   okresu (zamówienia według dnia płatności, TelemediGO według dnia zakupu), podzielona według roku pozyskania pacjenta.")
    r("   Wynik pacjentów pozyskanych w danym roku = ich marża w tym samym roku − wydatki na kampanie − prowizja tego roku.")
    ek = con.sql("""SELECT e.user_id, e.okres okres_kohorty, CASE WHEN e.t < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres,
                           e.marza, e.pierwsze, e.zamowienie
                    FROM ek e""").df()
    zr = pe[["user_id", "grupa_Z1K", "grupa_Z2"]]
    ek = ek.merge(zr, on="user_id", how="left")
    wyd_o = {o: float(wyd[(wyd.d < "2025-10-01") if o == 1 else (wyd.d >= "2025-10-01")].wydatki.sum()) for o in (1, 2)}
    wyd_nowe = float(wyd[wyd.kampania.isin(NOWE)].wydatki.sum())
    prow_o = {o: PROWIZJA * float(((pe.okres == o) & (pe.kanal == "afiliacja_ranking")).sum()) for o in (1, 2)}
    prow_o_z2 = {o: PROWIZJA * float(((pe.okres == o) & (pe.kanal_z2 == "afiliacja_ranking")).sum()) for o in (1, 2)}
    mk = ek.groupby(["okres", "okres_kohorty"]).marza.sum()
    przed = {o: float(ek[ek.okres == o].marza.sum()) for o in (1, 2)}
    marza = {o: przed[o] - wyd_o[o] - prow_o[o] for o in (1, 2)}
    baza2 = float(mk.get((2, 1), 0.0))
    wlasni = {1: float(mk[(1, 1)]) - wyd_o[1] - prow_o[1], 2: float(mk[(2, 2)]) - wyd_o[2] - prow_o[2]}
    z_raportu("c_priorytety.txt", "                     marza  828085.0 1048069.0  219984.0         27.0", None)
    assert (round(marza[1]), round(marza[2])) == (828085, 1048069), marza
    z_raportu("c_priorytety.txt", "853 635 zł (+3.1%)", None)
    assert round(wlasni[2]) == 853635, wlasni
    zm = marza[2] - marza[1]
    r(f"   Marża po wszystkich kosztach: okres 1 {zl(marza[1])} zł, okres 2 {zl(marza[2])} zł, przyrost {zl(zm)} zł "
      f"(+{100 * zm / marza[1]:.1f}%). Kontrola z c_priorytety.txt (W3): zgodna.")
    r(f"   a) pacjenci pozyskani w okresie 1, ich marża w okresie 2 (powtórne zamówienia i TelemediGO): {zl(baza2)} zł "
      f"= {100 * baza2 / zm:.1f}% przyrostu; w okresie 1 takiej bazy z poprzedniego roku nie było (dane zaczynają się 1.10.2024).")
    r(f"   b) pacjenci pozyskani w danym roku, po kosztach kampanii i prowizji: okres 1 {zl(wlasni[1])} zł, okres 2 "
      f"{zl(wlasni[2])} zł, zmiana {zl(wlasni[2] - wlasni[1])} zł ({100 * (wlasni[2] / wlasni[1] - 1):+.1f}%) "
      f"= {100 * (wlasni[2] - wlasni[1]) / zm:.1f}% przyrostu.")
    r(f"      na nowego pacjenta: okres 1 {wlasni[1] / n1:.2f} zł ({n1} pacjentów), okres 2 {wlasni[2] / n2:.2f} zł ({n2}).")
    r(f"      marża przed kampaniami pacjentów roku: {zl(mk[(1, 1)])} → {zl(mk[(2, 2)])} zł "
      f"({100 * (mk[(2, 2)] / mk[(1, 1)] - 1):+.1f}%); wydatki {zl(wyd_o[1])} → {zl(wyd_o[2])} zł ({100 * (wyd_o[2] / wyd_o[1] - 1):+.1f}%), "
      f"prowizja {zl(prow_o[1])} → {zl(prow_o[2])} zł.")
    # rozbicie b) w okresie 2 na nowe kampanie i resztę, obie reguły; okres 1 według tej samej reguły
    g4 = []
    for reg, kol, prow in (("Z1K", "grupa_Z1K", prow_o), ("Z2", "grupa_Z2", prow_o_z2)):
        for o in (1, 2):
            e = ek[(ek.okres == o) & (ek.okres_kohorty == o)]
            nowe_m = float(e[e[kol] == "1_nowe_kampanie_L4"].marza.sum())
            reszta_m = float(e[e[kol] != "1_nowe_kampanie_L4"].marza.sum())
            wy_nowe = wyd_nowe if o == 2 else 0.0
            n_nowe = int(((pe.okres == o) & (pe[kol] == "1_nowe_kampanie_L4")).sum())
            n_reszta = int(((pe.okres == o) & (pe[kol] != "1_nowe_kampanie_L4")).sum())
            g4.append({"regula": reg, "okres": o, "nowe_pacjenci": n_nowe, "nowe_marza_przed": nowe_m, "nowe_wydatki": wy_nowe,
                       "nowe_wynik": nowe_m - wy_nowe, "reszta_pacjenci": n_reszta, "reszta_marza_przed": reszta_m,
                       "reszta_wydatki": wyd_o[o] - wy_nowe, "reszta_prowizja": prow[o],
                       "reszta_wynik": reszta_m - (wyd_o[o] - wy_nowe) - prow[o]})
    g4 = pd.DataFrame(g4)
    r("\n   Wynik pacjentów pozyskanych w danym roku: nowe kampanie na L4 a reszta (marża w roku pozyskania − ich wydatki;")
    r("   reszcie przypisane wydatki pozostałych kampanii i prowizja; prowizja według tej samej reguły co źródło):")
    pokaz(g4.round(0))
    for reg in ("Z1K", "Z2"):
        a = g4[(g4.regula == reg) & (g4.okres == 1)].iloc[0]
        b = g4[(g4.regula == reg) & (g4.okres == 2)].iloc[0]
        r(f"   {reg}: nowe kampanie {zl(b.nowe_wynik)} zł ({b.nowe_wynik / b.nowe_pacjenci:.2f} zł na pacjenta); reszta "
          f"{zl(a.reszta_wynik)} → {zl(b.reszta_wynik)} zł ({100 * (b.reszta_wynik / a.reszta_wynik - 1):+.1f}%; na pacjenta "
          f"{a.reszta_wynik / a.reszta_pacjenci:.2f} → {b.reszta_wynik / b.reszta_pacjenci:.2f} zł).")
    r("   To rozbicie księgowe (przypisanie marży i kosztów grupom), a nie zmierzony wpływ: nie mówi, ilu pacjentów nowych")
    r("   kampanii przyszłoby bez nich ani co by się stało z resztą biznesu bez tych kampanii.")
    J["g4"] = {"marza_o1": marza[1], "marza_o2": marza[2], "przyrost": zm, "przyrost_proc": 100 * zm / marza[1],
               "baza_o1_w_o2": baza2, "baza_udzial_w_przyroscie_proc": 100 * baza2 / zm,
               "wlasni_o1": wlasni[1], "wlasni_o2": wlasni[2], "wlasni_zmiana": wlasni[2] - wlasni[1],
               "wlasni_zmiana_proc": 100 * (wlasni[2] / wlasni[1] - 1),
               "wlasni_udzial_w_przyroscie_proc": 100 * (wlasni[2] - wlasni[1]) / zm,
               "wlasni_na_pacjenta_o1": wlasni[1] / n1, "wlasni_na_pacjenta_o2": wlasni[2] / n2,
               "przed_kampaniami_wlasni_o1": float(mk[(1, 1)]), "przed_kampaniami_wlasni_o2": float(mk[(2, 2)]),
               "wydatki_o1": wyd_o[1], "wydatki_o2": wyd_o[2], "wydatki_nowe": wyd_nowe, "prowizja_o1": prow_o[1],
               "prowizja_o2": prow_o[2], "podzial": g4.to_dict(orient="records")}

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")

    def czysc(x):
        if isinstance(x, dict):
            return {str(k): czysc(v) for k, v in x.items()}
        if isinstance(x, list):
            return [czysc(v) for v in x]
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, (np.floating, float)):
            return None if np.isnan(x) else float(x)
        if isinstance(x, pd.Period):
            return str(x)
        return x

    with open(WYNIK_JSON, "w", encoding="utf-8") as f:
        json.dump(czysc(J), f, ensure_ascii=False, indent=1)
    print(f"Zapisano {WYNIK} i {WYNIK_JSON}")


if __name__ == "__main__":
    main()
