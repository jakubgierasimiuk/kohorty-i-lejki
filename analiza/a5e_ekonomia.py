"""A5 — ekonomia kampanii: koszt pozyskania i wynik na pacjenta (sesja „a5-ekonomia”, 2026-10-19).

Pytanie z PLAN.md (A5, dopiski po A4): ile kosztuje pozyskanie pacjenta w każdej kampanii i kanale i ile
pacjent zostawia marży po odjęciu tego kosztu. Według przyjętej reguły źródła (Z1K, ZALOZENIA.md 22) i obok
według sesji płatności (Z2, punkt 23). Kampania, której wynik zmienia znak zależnie od reguły, jest niepewna.

Definicje (moduł analiza/definicje.py, tylko import):
  - nowy pacjent N1, dzień kohorty d0 = dzień płatności pierwszego zamówienia (ZALOZENIA.md 16);
  - marża na pacjenta przed kosztem pozyskania = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza
    (za wizyty odbyte i zwrócone), narastająco od dnia 0 do dnia N, tylko kohorty z pełnym oknem N (punkt 34);
  - okresy na tych samych dniach kalendarzowych (punkt 27): dla okna N kohorty okresu 1 od 1.10.2024 do
    granice_por(N)[0], okresu 2 od 1.10.2025 do granice_por(N)[1];
  - prowizja afiliacyjna 25 zł za pierwsze opłacone zamówienie pacjenta przypisanego do rankingu lekarzy tą samą
    regułą co źródło, bez względu na status (punkt 25); obok jedna liczba według kodu RANKING10.

Założenia tej sesji (propozycje do ZALOZENIA.md, notatki/a5_ekonomia.md):
  - wydatki kampanii łączymy z kohortami po dniu kalendarzowym: wydatki z dni kohort okna (np. 1.10.2025 –
    2.07.2026) dzielimy przez nowych pacjentów z tych samych dni. Pacjent kupuje zwykle tego samego dnia co
    pierwsze wejście (75,1%) albo w ciągu 7 dni (24,6%), więc przesunięcie na brzegach okna jest małe;
  - koszt pozyskania = (wydatki + prowizja) / nowi pacjenci kampanii; kanały bez wydatków mają koszt 0 zł
    (program poleceń nie ma kosztu w danych — README);
  - wynik na pacjenta = marża na pacjenta w N dniach − koszt pozyskania; przedział 95% tylko z rozrzutu marży
    (błąd standardowy średniej), koszt pozyskania traktujemy jako stały.

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/a5e_ekonomia.py
Wynik: analiza/wyniki/a5e_ekonomia.txt, analiza/wyniki/a5e_kampanie.csv (zestawienie bez wierszy pacjentów).
"""

import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402

WYNIK = os.path.join(D.KATALOG, "analiza", "wyniki", "a5e_ekonomia.txt")
WYNIK_CSV = os.path.join(D.KATALOG, "analiza", "wyniki", "a5e_kampanie.csv")
PROWIZJA = 25.0
NOWE = ("meta_prosp_l4_szybko", "tt_prosp_l4_15min")
OKNA_W = (90, 180)
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)

PLATNE = ("google_ads_marka", "google_ads_ogolne", "meta_pozyskanie", "meta_remarketing", "tiktok")


def zl(x):
    """Kwota w złotych bez groszy, ze spacją co trzy cyfry."""
    return f"{x:,.0f}".replace(",", " ")


def grupa(kanal, kampania):
    """Grupa do zestawień nagłówkowych."""
    if kampania in NOWE:
        return "1_nowe_kampanie_L4"
    if kanal in PLATNE:
        return "2_pozostale_platne"
    if kanal == "afiliacja_ranking":
        return "3_afiliacja_ranking"
    return "4_bezplatne"


def zbuduj_pe(con):
    """`pe` (DataFrame): jeden wiersz na nowego pacjenta: d0, okres, powrót, źródło według obu reguł, cechy
    pierwszego zamówienia, zgoda marketingowa, marża w oknach 0/30/90/180 dni i składniki pierwszego zamówienia."""
    kol = ", ".join(f"coalesce(sum(e.marza) FILTER (WHERE e.dni <= {w}), 0) marza_{w}" for w in (0, 30, 90, 180))
    pe = con.sql(f"""
      SELECT p.user_id, p.d0, p.okres, p.dni_R2, r.kod, r.kanal, r.kampania, r.kanal_z2, r.kampania_z2,
             z.visit_purpose cel1, z.specialization spec1, z.status status1, z.list_price::DOUBLE cena1,
             z.amount_paid::DOUBLE zaplata1, z.refund_amount::DOUBLE zwrot1, u.marketing_consent zgoda,
             {kol}
      FROM powr p JOIN zrodlo r USING (user_id) JOIN zam z ON z.user_id = p.user_id AND z.nr = 1
      JOIN czyste.users u ON u.user_id = p.user_id
      LEFT JOIN ek e ON e.user_id = p.user_id
      GROUP BY ALL""").df()
    pe["d0"] = pd.to_datetime(pe["d0"])
    for r_, kk, kc in (("Z1K", "kanal", "kampania"), ("Z2", "kanal_z2", "kampania_z2")):
        pe[f"grupa_{r_}"] = [grupa(a, b) for a, b in zip(pe[kk], pe[kc])]
    return pe


def zbuduj_wyd(con):
    """`wyd` (DataFrame): wydatki dzień × kampania, z kanałem tej samej klasyfikacji co sesje."""
    w = con.sql(f"""
      SELECT date d, utm_campaign kampania, {D.KANAL} kanal, spend_pln::DOUBLE wydatki, clicks klikniecia
      FROM czyste.marketing_spend""").df()
    w["d"] = pd.to_datetime(w["d"])
    w["grupa"] = [grupa(a, b) for a, b in zip(w["kanal"], w["kampania"])]
    return w


def granice(okno):
    """Daty kohort (od, do) w okresie 1 i 2 dla okna; okno None = pełne okresy."""
    if okno is None:
        return {1: (pd.Timestamp("2024-10-01"), pd.Timestamp("2025-09-30")),
                2: (pd.Timestamp("2025-10-01"), pd.Timestamp(D.KONIEC))}
    g1, g2 = D.granice_por(okno)
    return {1: (pd.Timestamp("2024-10-01"), pd.Timestamp(g1)), 2: (pd.Timestamp("2025-10-01"), pd.Timestamp(g2))}


def ekonomia(pe, wyd, poziom, regula, okno):
    """Zestawienie: poziom ∈ {kampania, kanal, grupa}; regula ∈ {Z1K, Z2}; okno ∈ {90, 180, None}."""
    kol = {("kampania", "Z1K"): "kampania", ("kampania", "Z2"): "kampania_z2", ("kanal", "Z1K"): "kanal",
           ("kanal", "Z2"): "kanal_z2", ("grupa", "Z1K"): "grupa_Z1K", ("grupa", "Z2"): "grupa_Z2"}[(poziom, regula)]
    kanal_kol = "kanal" if regula == "Z1K" else "kanal_z2"
    wiersze = []
    for o, (od, do) in granice(okno).items():
        p = pe[(pe.okres == o) & (pe.d0 >= od) & (pe.d0 <= do)]
        w = wyd[(wyd.d >= od) & (wyd.d <= do)]
        wg = w.groupby({"kampania": "kampania", "kanal": "kanal", "grupa": "grupa"}[poziom])["wydatki"].sum()
        for klucz, g in p.groupby(kol):
            n = len(g)
            prow = PROWIZJA * (g[kanal_kol] == "afiliacja_ranking").sum()
            wy = float(wg.get(klucz, 0.0))
            r = {"okres": o, "regula": regula, "okno_dni": okno if okno else "pelny_rok", poziom: klucz,
                 "nowi": n, "wydatki_zl": round(wy), "prowizja_zl": round(prow),
                 "koszt_pozysk_na_pac": round((wy + prow) / n, 1)}
            if okno:
                m = g[f"marza_{okno}"]
                se = m.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
                wyn = m.mean() - (wy + prow) / n
                r.update({"marza_na_pac": round(m.mean(), 1), "wynik_na_pac": round(wyn, 1),
                          "wynik_od": round(wyn - 1.96 * se, 1), "wynik_do": round(wyn + 1.96 * se, 1),
                          "wynik_razem_zl": round(wyn * n),
                          "powrot_proc": round(100 * (g.dni_R2.fillna(10 ** 6) <= 90).mean(), 1)})
            wiersze.append(r)
        # kampanie z wydatkami bez żadnego pacjenta w tej regule
        for klucz in set(wg.index) - set(p[kol].unique()):
            wiersze.append({"okres": o, "regula": regula, "okno_dni": okno if okno else "pelny_rok", poziom: klucz,
                            "nowi": 0, "wydatki_zl": round(float(wg[klucz])), "prowizja_zl": 0})
    return pd.DataFrame(wiersze)


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=True)
    pe = zbuduj_pe(con)
    wyd = zbuduj_wyd(con)
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    r(f"A5 EKONOMIA KAMPANII — KOSZT POZYSKANIA I WYNIK NA PACJENTA ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Okres 1 = kohorty X 2024 – IX 2025, okres 2 = X 2025 – IX 2026. Źródło: Z1K = pierwsze wejście z anonimowymi")
    r("sesjami przeglądarek pacjenta, kod kampanii rozstrzyga (ZALOZENIA.md 22); Z2 = sesja płatności (punkt 23).")
    r("Marża na pacjenta = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza, dni 0..N, przed kosztem")
    r("pozyskania (punkt 34). Koszt pozyskania = (wydatki + prowizja 25 zł za pacjenta rankingu) / nowi pacjenci z tych")
    r("samych dni. Wynik na pacjenta = marża − koszt pozyskania. Okno 90 dni: kohorty 1.10–2.07 w obu okresach,")
    r("okno 180 dni: 1.10–3.04 (te same dni kalendarzowe, punkt 27). Przedział 95% wyniku tylko z rozrzutu marży.")

    # ---------- 0. kontrola ----------
    r("\n" + "=" * 110)
    r("0. KONTROLA: liczby odniesienia z części retencji (a5r_kohorty.txt, sekcja 1)")
    r("=" * 110)
    for okno, oczek in ((90, "12867 / 18924, 66.6 / 58.3 zł"), (180, "9125 / 12591, 75.5 / 67.7 zł")):
        gr = granice(okno)
        t = [pe[(pe.okres == o) & (pe.d0 >= gr[o][0]) & (pe.d0 <= gr[o][1])] for o in (1, 2)]
        r(f"   okno {okno}: pacjenci {len(t[0])} / {len(t[1])}, marża na pacjenta {t[0][f'marza_{okno}'].mean():.1f} / "
          f"{t[1][f'marza_{okno}'].mean():.1f} zł   (oczekiwane: {oczek})")
    r(f"   wydatki razem: {zl(wyd.wydatki.sum())} zł (okres 1: {zl(wyd[wyd.d < '2025-10-01'].wydatki.sum())} zł, "
      f"okres 2: {zl(wyd[wyd.d >= '2025-10-01'].wydatki.sum())} zł)")

    # ---------- 1. grupy ----------
    r("\n" + "=" * 110)
    r("1. NAGŁÓWEK: NOWE KAMPANIE NA L4 (meta_prosp_l4_szybko + tt_prosp_l4_15min) WOBEC POZOSTAŁYCH, OBIE REGUŁY")
    r("=" * 110)
    r("   Grupy: 1 = dwie nowe kampanie na L4; 2 = pozostałe kampanie płatne (Google Ads, Meta lekarz online,")
    r("   remarketing Meta); 3 = ranking lekarzy (prowizja); 4 = kanały bezpłatne (bezpośrednie, wyszukiwarka,")
    r("   program poleceń, newsletter i SMS). Kolumny: koszt_pozysk_na_pac i wynik_na_pac w zł na pacjenta.")
    wszystkie = []
    for okno in OKNA_W:
        for reg in ("Z1K", "Z2"):
            t = ekonomia(pe, wyd, "grupa", reg, okno)
            wszystkie.append(t.assign(poziom="grupa"))
    g = pd.concat(wszystkie)
    for okno in OKNA_W:
        r(f"\n1{'a' if okno == 90 else 'b'}. Okno {okno} dni")
        x = g[g.okno_dni == okno].sort_values(["grupa", "regula", "okres"])
        pokaz(x[["grupa", "regula", "okres", "nowi", "wydatki_zl", "prowizja_zl", "koszt_pozysk_na_pac", "marza_na_pac",
                 "wynik_na_pac", "wynik_od", "wynik_do", "wynik_razem_zl", "powrot_proc"]])
    r("   powrot_proc = powrót w 90 dniach (w oknie 180 też 90 dni, dla porównania z częścią retencji).")

    # pełny rok: koszt pozyskania bez marży
    r("\n1c. Pełne okresy (12 miesięcy): nowi pacjenci, wydatki, prowizja i koszt pozyskania (bez marży, bo młode")
    r("    kohorty nie mają pełnego okna)")
    gp = pd.concat([ekonomia(pe, wyd, "grupa", reg, None) for reg in ("Z1K", "Z2")])
    pokaz(gp.sort_values(["grupa", "regula", "okres"])[["grupa", "regula", "okres", "nowi", "wydatki_zl", "prowizja_zl",
                                                         "koszt_pozysk_na_pac"]])

    # ---------- 2. kampanie ----------
    r("\n" + "=" * 110)
    r("2. KAMPANIE I KANAŁY BEZPŁATNE: OKRES 1 I OKRES 2, OBIE REGUŁY ŹRÓDŁA")
    r("=" * 110)
    tabele = []
    for okno in OKNA_W + (None,):
        for reg in ("Z1K", "Z2"):
            tabele.append(ekonomia(pe, wyd, "kampania", reg, okno).assign(poziom="kampania"))
    k = pd.concat(tabele)
    for okno in OKNA_W:
        r(f"\n2{'a' if okno == 90 else 'b'}. Okno {okno} dni (kampanie bez pacjentów w danej regule: nowi = 0)")
        x = k[k.okno_dni == okno]
        szer = x.pivot_table(index="kampania", columns=["regula", "okres"],
                             values=["nowi", "koszt_pozysk_na_pac", "marza_na_pac", "wynik_na_pac"], aggfunc="first")
        szer.columns = [f"{a}_{b}_o{c}" for a, b, c in szer.columns]
        kolejnosc = [f"{m}_{reg}_o{o}" for reg in ("Z1K", "Z2") for o in (1, 2)
                     for m in ("nowi", "koszt_pozysk_na_pac", "marza_na_pac", "wynik_na_pac")]
        szer = szer.reindex(columns=[c for c in kolejnosc if c in szer.columns])
        wydk = x[x.regula == "Z1K"].groupby(["kampania", "okres"]).wydatki_zl.first().unstack()
        szer.insert(0, "wydatki_o2", wydk.get(2))
        szer.insert(0, "wydatki_o1", wydk.get(1))
        szer = szer.sort_values("wydatki_o2", ascending=False).reset_index()
        for reg in ("Z1K", "Z2"):
            r(f"\n   reguła {reg}")
            kol = ["kampania", "wydatki_o1", "wydatki_o2"] + [c for c in szer.columns if f"_{reg}_" in c]
            pokaz(szer[kol])

    r("\n2c. Pełne okresy: koszt pozyskania (wydatki i prowizja z całych 12 miesięcy / nowi z całych 12 miesięcy)")
    x = k[k.okno_dni == "pelny_rok"]
    szer = x.pivot_table(index="kampania", columns=["regula", "okres"], values=["nowi", "koszt_pozysk_na_pac"], aggfunc="first")
    szer.columns = [f"{a}_{b}_o{c}" for a, b, c in szer.columns]
    wydk = x[x.regula == "Z1K"].groupby(["kampania", "okres"]).wydatki_zl.first().unstack()
    szer.insert(0, "wydatki_o2", wydk.get(2))
    szer.insert(0, "wydatki_o1", wydk.get(1))
    pokaz(szer.sort_values("wydatki_o2", ascending=False).reset_index())

    # ---------- 3. zmiana znaku ----------
    r("\n" + "=" * 110)
    r("3. NIEPEWNE: KAMPANIE, KTÓRYCH WYNIK NA PACJENTA ZMIENIA ZNAK ZALEŻNIE OD REGUŁY ŹRÓDŁA")
    r("=" * 110)
    r("   Tylko kampanie płatne i afiliacja (kanały bezpłatne mają koszt 0 zł, więc ich wynik = marża). Dodatkowo:")
    r("   czy przedział 95% wyniku obejmuje zero w którejkolwiek regule.")
    pl = k[(k.okno_dni.isin(OKNA_W)) & (k.wydatki_zl.fillna(0) + k.prowizja_zl.fillna(0) > 0)]
    s = pl.pivot_table(index=["kampania", "okno_dni", "okres"], columns="regula",
                       values=["nowi", "wynik_na_pac", "wynik_od", "wynik_do"], aggfunc="first")
    s.columns = [f"{a}_{b}" for a, b in s.columns]
    s = s.reset_index()
    s["znak_zalezy_od_reguly"] = np.sign(s.wynik_na_pac_Z1K) != np.sign(s.wynik_na_pac_Z2)
    s["przedzial_obejmuje_zero"] = ((s.wynik_od_Z1K <= 0) & (s.wynik_do_Z1K >= 0)) | ((s.wynik_od_Z2 <= 0) & (s.wynik_do_Z2 >= 0))
    pokaz(s[["kampania", "okno_dni", "okres", "nowi_Z1K", "wynik_na_pac_Z1K", "wynik_od_Z1K", "wynik_do_Z1K",
             "nowi_Z2", "wynik_na_pac_Z2", "wynik_od_Z2", "wynik_do_Z2", "znak_zalezy_od_reguly", "przedzial_obejmuje_zero"]])
    r("\n   Kampanie ze zmianą znaku w którymkolwiek oknie i okresie:")
    zm = s[s.znak_zalezy_od_reguly]
    r("     " + (", ".join(sorted(set(zm.kampania))) if len(zm) else "brak"))

    # ---------- 4. prowizja ----------
    r("\n" + "=" * 110)
    r("4. PROWIZJA AFILIACYJNA (25 zł za pierwsze opłacone zamówienie, bez względu na status)")
    r("=" * 110)
    for o, (od, do) in granice(None).items():
        p = pe[(pe.okres == o)]
        a, b, c = (p.kanal == "afiliacja_ranking").sum(), (p.kanal_z2 == "afiliacja_ranking").sum(), (p.kod == "RANKING10").sum()
        r(f"   okres {o}: według przyjętej reguły {a} pacjentów = {zl(PROWIZJA * a)} zł; według sesji płatności {b} = "
          f"{zl(PROWIZJA * b)} zł; według kodu RANKING10 {c} = {zl(PROWIZJA * c)} zł")
    a, b, c = (pe.kanal == "afiliacja_ranking").sum(), (pe.kanal_z2 == "afiliacja_ranking").sum(), (pe.kod == "RANKING10").sum()
    r(f"   dwa lata: {zl(PROWIZJA * a)} zł (przyjęta reguła), {zl(PROWIZJA * b)} zł (sesja płatności), "
      f"{zl(PROWIZJA * c)} zł (kod RANKING10)")
    r("   Wariant RANKING10 przy ekonomii rankingu: ta sama marża pacjentów rankingu (przyjęta reguła), a prowizja tylko")
    r("   za pacjentów z kodem, rozłożona na wszystkich pacjentów rankingu:")
    for okno in OKNA_W:
        for o in (1, 2):
            gr = granice(okno)[o]
            w_oknie = pe[(pe.okres == o) & (pe.d0 >= gr[0]) & (pe.d0 <= gr[1])]
            p = w_oknie[w_oknie.kanal == "afiliacja_ranking"]
            n10 = (w_oknie.kod == "RANKING10").sum()
            m = p[f"marza_{okno}"].mean()
            r(f"   okno {okno}, okres {o}: {len(p)} pacjentów rankingu, marża {m:.1f} zł, prowizja 25,0 zł na pacjenta, "
              f"wynik {m - PROWIZJA:.1f} zł; wariant RANKING10: {n10} kodów, prowizja {zl(PROWIZJA * n10)} zł, "
              f"{PROWIZJA * n10 / len(p):.1f} zł na pacjenta, wynik {m - PROWIZJA * n10 / len(p):.1f} zł")
    r("   Kontrola zbieżności sum (w oknie 90 dni oba okresy mają tyle samo pacjentów rankingu): pacjenci rankingu")
    r("   według przyjętej reguły w miesiącach kohorty, okres 1 i okres 2:")
    mies = pe[pe.kanal == "afiliacja_ranking"].assign(m=lambda x: x.d0.dt.month).groupby(["okres", "m"]).size().unstack("m")
    pokaz(mies.reset_index())

    # ---------- 5. kanały ----------
    r("\n" + "=" * 110)
    r("5. KANAŁY (grupy kampanii), okno 90 dni, obie reguły")
    r("=" * 110)
    kn = pd.concat([ekonomia(pe, wyd, "kanal", reg, 90) for reg in ("Z1K", "Z2")])
    pokaz(kn.sort_values(["kanal", "regula", "okres"])[["kanal", "regula", "okres", "nowi", "wydatki_zl", "prowizja_zl",
                                                         "koszt_pozysk_na_pac", "marza_na_pac", "wynik_na_pac",
                                                         "wynik_od", "wynik_do", "wynik_razem_zl", "powrot_proc"]])

    out = pd.concat([g, gp.assign(poziom="grupa"), k, kn.assign(poziom="kanal")], ignore_index=True)
    out.to_csv(WYNIK_CSV, index=False, encoding="utf-8")
    r(f"\nZestawienie (grupy, kampanie, kanały, obie reguły, okna 90, 180 i pełny rok): {os.path.relpath(WYNIK_CSV, D.KATALOG)}")

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print("\n".join(linie[:40]))
    print(f"... zapisano {WYNIK}")


if __name__ == "__main__":
    main()
