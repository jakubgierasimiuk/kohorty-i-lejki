"""A5 — ekonomia kampanii, część 2: koszty nowych kampanii na L4, scenariusze, dodatkowość, naprawić albo wyłączyć
(sesja „a5-ekonomia”, 2026-10-19).

Nowe kampanie na L4 = meta_prosp_l4_szybko (od 3.11.2025) i tt_prosp_l4_15min (od 9.02.2026). Liczy:
  A. skład marży na pacjenta w 90 dniach (pierwsze zamówienie, zniżka, zwrot, koszt lekarza, TelemediGO, dni 1–90)
     i wynik po koszcie pozyskania, nowe kampanie wobec pozostałych, obie reguły źródła;
  B. koszty widoczne tylko w nowych kampaniach: zwroty po wizycie i koszt lekarza za te wizyty, niska zgoda
     marketingowa (z powrotem i powrotem przypisanym do newslettera i SMS-a według zgody);
  C. scenariusz hipotezy Kuby (poranne godziny internistów) z wartością powrotu z ZALOZENIA.md 38 — scenariusz,
     nie wynik; liczby spadku powrotu czyta z raportu części retencji (analiza/wyniki/a5r_zdarzenia.txt);
  D. czy pacjenci nowych kampanii są dodatkowi: pozyskanie w pozostałych kanałach po startach kampanii, rok do roku;
  E. naprawić albo wyłączyć (CLAUDE.md, punkt 9): każda droga z rachunkiem w marży i z założeniami.

Importuje analiza/definicje.py i analiza/a5e_ekonomia.py. Tylko czyta schemat `czyste`. Uruchomienie:
    python -I analiza/a5e_scenariusze.py
Wynik: analiza/wyniki/a5e_scenariusze.txt
"""

import datetime as dt
import math
import os
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
import a5e_ekonomia as E  # noqa: E402

WYNIK = os.path.join(D.KATALOG, "analiza", "wyniki", "a5e_scenariusze.txt")
ZRODLO_RETENCJI = os.path.join(D.KATALOG, "analiza", "wyniki", "a5r_zdarzenia.txt")
NOWE = E.NOWE
zl = E.zl
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)


def koszt_lekarza(spec, status):
    if status not in ("completed", "refunded"):
        return 0.0
    return 25.0 if spec == "internista" else 200.0 if spec == "psychiatra" else 100.0


def spadki_retencji():
    """Spadek powrotu w 90 dniach w starych kampaniach (punkty procentowe) i liczba ich pacjentów w okresie 2,
    z raportu części retencji (a5r_zdarzenia.txt, scenariusze wpływu na marżę)."""
    tekst = open(ZRODLO_RETENCJI, encoding="utf-8").read()
    wzory = {"caly_Z1K": r"spadek powrotu w starych kampaniach, cały \(Z1K\)\s+([\d.]+)\s+(\d+)",
             "caly_Z2": r"spadek powrotu w starych kampaniach, cały \(sesja płatności\)\s+([\d.]+)\s+(\d+)",
             "opoznienia_Z1K": r"zmiana rozkładu opóźnień przy stałych kampaniach i usługach \(Z1K[^)]*\)\s+([\d.]+)\s+(\d+)",
             "opoznienia_Z2": r"zmiana rozkładu opóźnień przy stałych kampaniach i usługach \(sesja płatności[^)]*\)\s+([\d.]+)\s+(\d+)"}
    wynik = {}
    for k, w in wzory.items():
        m = re.search(w, tekst)
        if not m:
            raise SystemExit(f"Nie znalazłem w {ZRODLO_RETENCJI} wiersza: {k}")
        wynik[k] = (float(m.group(1)), int(m.group(2)))
    return wynik


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=True, dni_obserwacji=1, ekonomia=True)
    pe = E.zbuduj_pe(con)
    wyd = E.zbuduj_wyd(con)
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

    r(f"A5 EKONOMIA KAMPANII, CZĘŚĆ 2 — KOSZTY NOWYCH KAMPANII NA L4, SCENARIUSZE, DODATKOWOŚĆ, NAPRAWIĆ ALBO WYŁĄCZYĆ")
    r(f"({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`. Nowe kampanie na L4 = meta_prosp_l4_szybko (od 3.11.2025) i")
    r("tt_prosp_l4_15min (od 9.02.2026). Reguły źródła: Z1K (przyjęta) i Z2 (sesja płatności). Definicje jak w")
    r("analiza/a5e_ekonomia.py. Kwoty w zł. Scenariusze opisują, ile byłoby warte coś, czego dane nie dowodzą.")

    # wspólne: segment pacjenta według reguły
    def segment(kampania):
        return {"meta_prosp_l4_szybko": "1_meta_L4", "tt_prosp_l4_15min": "2_tiktok_L4"}.get(kampania, "3_pozostali")
    pe["seg_Z1K"] = pe.kampania.map(segment)
    pe["seg_Z2"] = pe.kampania_z2.map(segment)
    pe["nowa_Z1K"] = pe.kampania.isin(NOWE)
    pe["nowa_Z2"] = pe.kampania_z2.isin(NOWE)
    pe["lek1"] = [koszt_lekarza(a, b) for a, b in zip(pe.spec1, pe.status1)]
    pe["go0"] = pe.marza_0 - (pe.zaplata1 - pe.zwrot1 - pe.lek1)
    pe["znizka1"] = pe.cena1 - pe.zaplata1
    pe["marza_1_90"] = pe.marza_90 - pe.marza_0
    pe["powrot90"] = (pe.dni_R2.fillna(10 ** 6) <= 90).astype(float)
    g90 = E.granice(90)
    w90 = pe[(pe.okres == 2) & (pe.d0 >= g90[2][0]) & (pe.d0 <= g90[2][1])]
    w90_1 = pe[(pe.okres == 1) & (pe.d0 >= g90[1][0]) & (pe.d0 <= g90[1][1])]
    wyd2 = wyd[(wyd.d >= g90[2][0]) & (wyd.d <= g90[2][1])]

    # ---------- A. skład marży ----------
    naglowek("A. SKŁAD MARŻY NA PACJENTA W 90 DNIACH I WYNIK PO KOSZCIE POZYSKANIA (okres 2, kohorty 1.10.2025–2.07.2026)")
    r("   cena = cena katalogowa pierwszego zamówienia, znizka = cena − zapłata, zwrot = zwrot na pierwszym zamówieniu,")
    r("   lekarz = koszt lekarza za pierwsze zamówienie, go = TelemediGO kupione przy kasie, dni_1_90 = marża kolejnych")
    r("   zamówień i TelemediGO w dniach 1–90. marza = zaplata − zwrot − lekarz + go + dni_1_90. Koszt pozyskania jak w")
    r("   a5e_ekonomia.py (wydatki z dni kohort / nowi z tych dni). Pozostali = wszyscy pozostali pacjenci (płatni i bezpłatni);")
    r("   pozostali płatni = tylko kampanie płatne bez nowych.")
    wiersze = []
    for reg in ("Z1K", "Z2"):
        kamp = "kampania" if reg == "Z1K" else "kampania_z2"
        kan = "kanal" if reg == "Z1K" else "kanal_z2"
        segmenty = {"1_meta_L4": w90[kamp] == "meta_prosp_l4_szybko", "2_tiktok_L4": w90[kamp] == "tt_prosp_l4_15min",
                    "nowe_razem": w90[kamp].isin(NOWE),
                    "pozostali_platni": (~w90[kamp].isin(NOWE)) & w90[kan].isin(E.PLATNE),
                    "pozostali_wszyscy": ~w90[kamp].isin(NOWE)}
        for nazwa, maska in segmenty.items():
            g = w90[maska]
            if nazwa in ("1_meta_L4", "2_tiktok_L4", "nowe_razem"):
                kampanie = {"1_meta_L4": ["meta_prosp_l4_szybko"], "2_tiktok_L4": ["tt_prosp_l4_15min"], "nowe_razem": list(NOWE)}[nazwa]
                koszt = wyd2[wyd2.kampania.isin(kampanie)].wydatki.sum()
            elif nazwa == "pozostali_platni":
                koszt = wyd2[~wyd2.kampania.isin(NOWE)].wydatki.sum()
            else:
                koszt = wyd2[~wyd2.kampania.isin(NOWE)].wydatki.sum() + E.PROWIZJA * (g[kan] == "afiliacja_ranking").sum()
            wiersze.append({"regula": reg, "segment": nazwa, "nowi": len(g), "cena": g.cena1.mean(), "znizka": g.znizka1.mean(),
                            "zaplata": g.zaplata1.mean(), "zwrot": g.zwrot1.mean(), "lekarz": g.lek1.mean(), "go": g.go0.mean(),
                            "dni_1_90": g.marza_1_90.mean(), "marza": g.marza_90.mean(), "koszt_pozysk": koszt / len(g),
                            "wynik": g.marza_90.mean() - koszt / len(g), "powrot90_proc": 100 * g.powrot90.mean(),
                            "L4_proc": 100 * (g.cel1 == "l4").mean(), "zwrot_po_wizycie_proc": 100 * (g.status1 == "refunded").mean()})
    A = pd.DataFrame(wiersze).round(1)
    pokaz(A)
    r("   Uwaga: pozostali_wszyscy liczą koszt pozyskania jako wszystkie wydatki poza nowymi kampaniami + prowizja, podzielone")
    r("   przez wszystkich pozostałych pacjentów (też bezpłatnych), czyli średni koszt pacjenta w reszcie biznesu.")

    # ---------- B. koszty widoczne tylko w nowych kampaniach ----------
    naglowek("B. KOSZTY WIDOCZNE TYLKO W NOWYCH KAMPANIACH NA L4 (okres 2, wszystkie zamówienia pacjentów)")
    zam2 = con.sql("""
      SELECT z.order_id, z.user_id, z.created_at, z.specialization, z.visit_purpose, z.status, z.amount_paid::DOUBLE zaplata,
             z.refund_amount::DOUBLE zwrot, r.kampania, r.kampania_z2
      FROM zam z JOIN zrodlo r USING (user_id) WHERE z.created_at >= TIMESTAMP '2025-10-01'""").df()
    zam2["lekarz"] = [koszt_lekarza(a, b) for a, b in zip(zam2.specialization, zam2.status)]
    r("B1. Zwroty po odbytej wizycie (status refunded): lekarz dostaje wynagrodzenie, pacjent dostaje zwrot.")
    r("    Wizyty L4 = cel wizyty L4 u każdego lekarza, odbyte (completed albo refunded), jak w części retencji.")
    wiersze = []
    segm_b = {"meta_prosp_l4_szybko": ["meta_prosp_l4_szybko"], "tt_prosp_l4_15min": ["tt_prosp_l4_15min"],
              "nowe kampanie": list(NOWE)}
    for reg, kol in (("Z1K", "kampania"), ("Z2", "kampania_z2")):
        maski = {k: zam2[kol].isin(v) for k, v in segm_b.items()}
        maski["pozostali"] = ~zam2[kol].isin(NOWE)
        for nazwa, maska in maski.items():
            lista = segm_b.get(nazwa)
            npac = int((pe[(pe.okres == 2)][kol].isin(lista) if lista else ~pe[(pe.okres == 2)][kol].isin(NOWE)).sum())
            z = zam2[maska]
            ref = z[z.status == "refunded"]
            l4 = z[(z.visit_purpose == "l4") & z.status.isin(["completed", "refunded"])]
            wiersze.append({"regula": reg, "pacjenci": nazwa, "pacjentow_okres2": npac,
                            "wizyty_zwrocone": len(ref), "zwrocone_zl": round(ref.zwrot.sum()), "lekarz_za_zwrocone_zl": round(ref.lekarz.sum()),
                            "zwrot_na_pac": round(ref.zwrot.sum() / npac, 1), "lekarz_na_pac": round(ref.lekarz.sum() / npac, 1),
                            "wizyty_L4_odbyte": len(l4), "L4_zwrocone": int((l4.status == "refunded").sum()),
                            "L4_zwrot_proc": round(100 * (l4.status == "refunded").mean(), 1),
                            "sredni_zwrot_L4_zl": round(l4[l4.status == "refunded"].zwrot.mean(), 1)})
    B1 = pd.DataFrame(wiersze)
    pokaz(B1)
    l4_1 = con.sql("""SELECT count(*) n, count(*) FILTER (WHERE status = 'refunded') z FROM zam
                      WHERE created_at < TIMESTAMP '2025-10-01' AND visit_purpose = 'l4'
                        AND status IN ('completed', 'refunded')""").fetchone()
    r(f"   Dla porównania okres 1: odbyte wizyty L4 {l4_1[0]}, zwrócone po wizycie {l4_1[1]} "
      f"({100 * l4_1[1] / l4_1[0]:.1f}%).")

    r("\nB2. Zgoda marketingowa i powrót w 90 dniach według zgody (kohorty okresu 2 do 2.07.2026).")
    r("    powrot_crm = powrót w dniach 1–90 zamówieniem przypisanym do wejścia z newslettera albo SMS-a w ciągu 24 godzin")
    r("    (ZALOZENIA.md 26, rozłącznie: ostatnie wejście przed płatnością). To dolna granica wpływu kontaktu.")
    crm = con.sql("""
      SELECT z.user_id, min(date_diff('day', k.d0, z.created_at::DATE)) dni_crm
      FROM crm_rozl c JOIN zam z USING (order_id) JOIN koh k ON k.user_id = z.user_id
      WHERE z.nr > 1 GROUP BY 1""").df()
    pe2 = pe.merge(crm, on="user_id", how="left")
    pe2["powrot_crm90"] = ((pe2.dni_crm.fillna(10 ** 6) >= 1) & (pe2.dni_crm.fillna(10 ** 6) <= 90)).astype(float)
    pe2["powrot_bez_crm90"] = pe2.powrot90 - pe2.powrot_crm90.where(pe2.powrot90 == 1, 0)
    w2 = pe2[(pe2.okres == 2) & (pe2.d0 >= g90[2][0]) & (pe2.d0 <= g90[2][1])]
    wiersze = []
    for reg in ("Z1K", "Z2"):
        for nowa in (True, False):
            g = w2[w2[f"nowa_{reg}"] == nowa]
            for zg in (1, 0):
                h = g[g.zgoda == zg]
                wiersze.append({"regula": reg, "pacjenci": "nowe kampanie" if nowa else "pozostali", "zgoda": zg,
                                "n": len(h), "udzial_proc": round(100 * len(h) / len(g), 1),
                                "powrot90_proc": round(100 * h.powrot90.mean(), 1),
                                "powrot_crm90_proc": round(100 * h.powrot_crm90.mean(), 2),
                                "marza90": round(h.marza_90.mean(), 1)})
    B2 = pd.DataFrame(wiersze)
    pokaz(B2)

    # ---------- C. wartość powrotu i scenariusz poranka ----------
    naglowek("C. WARTOŚĆ POWROTU (ZALOZENIA.md 38) I SCENARIUSZ HIPOTEZY KUBY: PORANNE GODZINY INTERNISTÓW")
    o1 = pe[pe.okres == 1].assign(m1_180=lambda x: x.marza_180 - x.marza_0)
    wr, nwr = o1[o1.powrot90 == 1].m1_180.mean(), o1[o1.powrot90 == 0].m1_180.mean()
    WARTOSC = round(wr - nwr, 1)
    r(f"   Kontrola wartości powrotu: okres 1, marża dni 1–180: wrócił w 90 dniach {wr:.1f} zł ({int((o1.powrot90 == 1).sum())} "
      f"pacjentów), nie wrócił {nwr:.1f} zł ({int((o1.powrot90 == 0).sum())}); różnica {WARTOSC:.1f} zł (założenie 38: 95,6 zł).")
    sp = spadki_retencji()
    n_old = {"Z1K": int((pe[(pe.okres == 2)].nowa_Z1K == False).sum()), "Z2": int((pe[(pe.okres == 2)].nowa_Z2 == False).sum())}  # noqa: E712
    n_new = {"Z1K": int(pe[(pe.okres == 2)].nowa_Z1K.sum()), "Z2": int(pe[(pe.okres == 2)].nowa_Z2.sum())}
    r(f"   Pacjenci okresu 2: stare kampanie {n_old['Z1K']} (Z1K) i {n_old['Z2']} (Z2); nowe kampanie {n_new['Z1K']} i {n_new['Z2']}.")
    r("   Spadek powrotu w 90 dniach w starych kampaniach (punkty procentowe) z analiza/wyniki/a5r_zdarzenia.txt:")
    wiersze = []
    for k, (pp, n) in sp.items():
        reg = k.split("_")[-1]
        if n != n_old[reg]:
            raise SystemExit(f"Liczba pacjentów w raporcie retencji ({n}) różni się od policzonej ({n_old[reg]}) dla {k}")
        powr = pp / 100 * n
        wiersze.append({"scenariusz": {"caly": "cały spadek w starych kampaniach (górna granica)",
                                       "opoznienia": "tylko zmiana rozkładu opóźnień pierwszej wizyty"}[k.split("_")[0]],
                        "regula": reg, "spadek_pkt": pp, "pacjenci_starych": n, "powrotow_mniej": round(powr),
                        "marza_180_zl": round(powr * WARTOSC), "na_pacjenta_nowych_kampanii_zl": round(powr * WARTOSC / n_new[reg], 1)})
    C = pd.DataFrame(wiersze)
    pokaz(C)
    r("   To scenariusz, nie wynik: zakłada, że spadek przypisany opóźnieniom (albo cały spadek) to skutek nowych kampanii")
    r("   i że każdy utracony powrót jest wart 95,6 zł marży w 180 dniach. Część retencji pokazała, że przy tym samym")
    r("   ruchu porannym opóźnień jest dużo więcej niż rok wcześniej (spadła przepustowość), więc kampanie mogą nie być")
    r("   przyczyną. Kwotę dzielimy na pacjentów obu nowych kampanii tylko po to, żeby pokazać rząd wielkości obok wyniku.")

    # ---------- D. dodatkowość ----------
    naglowek("D. CZY PACJENCI NOWYCH KAMPANII SĄ DODATKOWI: POZYSKANIE W POZOSTAŁYCH KANAŁACH, ROK DO ROKU (reguła Z1K)")
    r("   Gdyby nowe kampanie przejmowały pacjentów, którzy i tak by przyszli, po ich startach powinno spaść pozyskanie")
    r("   w pozostałych kanałach wobec tego samego okresu rok wcześniej, najmocniej przy L4. Reguła Z1K, bo sesja płatności")
    r("   z definicji przenosi część pacjentów nowych kampanii do wejść bezpośrednich i wyszukiwania marki.")
    pe["m"] = pe.d0.dt.to_period("M")
    pe["L4"] = pe.cel1 == "l4"
    grupy = {"nowe kampanie L4": pe.nowa_Z1K, "bezplatne": pe.grupa_Z1K == "4_bezplatne",
             "platne bez nowych": pe.grupa_Z1K == "2_pozostale_platne", "wszyscy bez nowych": ~pe.nowa_Z1K,
             "L4 bez nowych": (~pe.nowa_Z1K) & pe.L4, "gs_generic_l4": pe.kampania == "gs_generic_l4",
             "bez nowych, nie L4": (~pe.nowa_Z1K) & (~pe.L4)}
    mies = pd.DataFrame({k: pe[v].groupby("m").size() for k, v in grupy.items()}).fillna(0).astype(int)
    rr = []
    for m in mies.index[mies.index >= pd.Period("2025-10", "M")]:
        p = m - 12
        w = {"miesiac": str(m)}
        for k in grupy:
            w[k] = mies.at[m, k]
            if k != "nowe kampanie L4":
                w[k + " r/r"] = round(mies.at[m, k] / mies.at[p, k], 2) if mies.at[p, k] else np.nan
        rr.append(w)
    pokaz(pd.DataFrame(rr))
    r("   r/r = miesiąc okresu 2 / ten sam miesiąc okresu 1. Październik 2025 to jedyny miesiąc okresu 2 przed startem")
    r("   kampanii Meta na L4 (3.11.2025).")

    r("\nD2. 28 dni przed startem i 28 dni od startu, wobec tych samych dni rok wcześniej (różnica różnic, iloraz).")
    r("    iloraz = (po/przed w roku startu) / (po/przed rok wcześniej); 1,00 = bez zmiany; przedział 95% z rozkładu Poissona.")
    pe["d"] = pe.d0
    wiersze = []
    for start in (pd.Timestamp("2025-11-03"), pd.Timestamp("2026-02-09")):
        for k, v in grupy.items():
            if k == "nowe kampanie L4":
                continue
            s = pe[v]

            def licz(od, do):
                return int(((s.d >= od) & (s.d < do)).sum())
            st0 = start - pd.DateOffset(years=1)
            a2, b2 = licz(start, start + pd.Timedelta(days=28)), licz(start - pd.Timedelta(days=28), start)
            a1, b1 = licz(st0, st0 + pd.Timedelta(days=28)), licz(st0 - pd.Timedelta(days=28), st0)
            il = (a2 / b2) / (a1 / b1)
            se = math.sqrt(1 / a2 + 1 / b2 + 1 / a1 + 1 / b1)
            wiersze.append({"start": start.date(), "grupa": k, "przed_rok_wczesniej": b1, "po_rok_wczesniej": a1,
                            "przed": b2, "po": a2, "iloraz": round(il, 2), "od": round(il * math.exp(-1.96 * se), 2),
                            "do": round(il * math.exp(1.96 * se), 2)})
    pokaz(pd.DataFrame(wiersze))
    r("    Start 3.11.2025: 28 dni przed = 6.10–2.11, po = 3.11–30.11 (rok wcześniej te same daty 2024).")
    r("    Start 9.02.2026: przed = 12.01–8.02, po = 9.02–8.03 (rok wcześniej te same daty 2025). Rok wcześniej")
    r("    w lutym–marcu 2025 nie było nowych kampanii; 28 dni przed 9.02.2026 kampania Meta na L4 już działała.")

    r("\nD3. Pacjenci nowych kampanii, którzy przed pierwszym wejściem z kampanii mieli wejście z innego kanału")
    d3 = con.sql("""
      SELECT r.kampania, count(*) pacjenci,
             count(*) FILTER (WHERE g.Z1_kampania NOT IN ('meta_prosp_l4_szybko', 'tt_prosp_l4_15min')) pierwsze_wejscie_inne,
             count(*) FILTER (WHERE g.Z2_kampania NOT IN ('meta_prosp_l4_szybko', 'tt_prosp_l4_15min')) platnosc_w_innej_sesji,
             round(avg(g.sesje_do_zakupu), 2) sesje_do_zakupu
      FROM zrodlo r JOIN reg g USING (user_id)
      WHERE r.kampania IN ('meta_prosp_l4_szybko', 'tt_prosp_l4_15min') GROUP BY 1""").df()
    pokaz(d3)
    r("    pierwsze_wejscie_inne = kod kampanii przypisał pacjenta do kampanii, choć pierwsze widoczne wejście było z innego")
    r("    kanału; platnosc_w_innej_sesji = zapłacił w sesji z innego źródła (stąd mniej pacjentów według sesji płatności).")

    r("\nD4. Ilu pacjentów L4 mogło przejść z pozostałych kanałów do nowych kampanii (przybliżenie)")
    r("    Założenie: bez nowych kampanii stosunek pacjentów z pierwszym L4 do pacjentów z inną pierwszą usługą w pozostałych")
    r("    kanałach byłby taki jak w tym samym miesiącu okresu 1. Brakujący = oczekiwani − faktyczni pacjenci L4 w pozostałych")
    r("    kanałach, miesiące XI 2025 – IX 2026. Październik 2025 (przed startem) pokazuje, jak bardzo to założenie się myli")
    r("    bez żadnej kampanii.")
    wiersze = []
    for m in mies.index[mies.index >= pd.Period("2025-10", "M")]:
        p = m - 12
        ocz = mies.at[m, "bez nowych, nie L4"] * mies.at[p, "L4 bez nowych"] / mies.at[p, "bez nowych, nie L4"]
        wiersze.append({"miesiac": str(m), "L4_faktyczni": mies.at[m, "L4 bez nowych"], "L4_oczekiwani": round(ocz),
                        "brakujacy": round(ocz - mies.at[m, "L4 bez nowych"]), "nowe_kampanie": mies.at[m, "nowe kampanie L4"]})
    d4 = pd.DataFrame(wiersze)
    pokaz(d4)
    po = d4[d4.miesiac >= "2025-11"]
    r(f"    Razem XI 2025 – IX 2026: brakujących {po.brakujacy.sum()} pacjentów L4 wobec {po.nowe_kampanie.sum()} pacjentów "
      f"nowych kampanii ({100 * po.brakujacy.sum() / po.nowe_kampanie.sum():.1f}%). W październiku 2025 (bez kampanii) "
      f"wynik to {d4.brakujacy.iloc[0]} (ujemny = więcej L4, niż zakłada wzór).")

    # ---------- E. naprawić albo wyłączyć ----------
    naglowek("E. NAPRAWIĆ ALBO WYŁĄCZYĆ — RACHUNEK W MARŻY NA ROK (okres 2: X 2025 – IX 2026)")
    r("   Podstawa roczna: wydatki i nowi pacjenci z całego okresu 2, marża na pacjenta w 90 dniach z kohort z pełnym")
    r("   oknem (1.10.2025–2.07.2026), obok marża w 180 dniach (kohorty do 3.04.2026; TikTok ma w niej tylko 299 pacjentów).")
    rok = pe[pe.okres == 2]
    w180 = pe[(pe.okres == 2) & (pe.d0 >= E.granice(180)[2][0]) & (pe.d0 <= E.granice(180)[2][1])]
    wyd_rok = wyd[wyd.d >= pd.Timestamp("2025-10-01")].groupby("kampania").wydatki.sum()
    kampanie = {"meta_prosp_l4_szybko": ["meta_prosp_l4_szybko"], "tt_prosp_l4_15min": ["tt_prosp_l4_15min"], "obie": list(NOWE)}
    podst = []
    for nazwa, lista in kampanie.items():
        for reg, kol in (("Z1K", "kampania"), ("Z2", "kampania_z2")):
            n = int(rok[kol].isin(lista).sum())
            m90 = w90[w90[kol].isin(lista)].marza_90.mean()
            m180 = w180[w180[kol].isin(lista)].marza_180.mean()
            wy = float(wyd_rok.reindex(lista).sum())
            podst.append({"kampania": nazwa, "regula": reg, "nowi_rok": n, "wydatki_rok": round(wy), "koszt_pozysk": round(wy / n, 1),
                          "marza90": round(m90, 1), "marza180": round(m180, 1), "wynik90_na_pac": round(m90 - wy / n, 1),
                          "wynik90_rok": round(n * m90 - wy), "wynik180_rok": round(n * m180 - wy)})
    P = pd.DataFrame(podst)
    r("\nE0. Podstawa")
    pokaz(P)

    r("\nE1. WYŁĄCZYĆ (ograniczenie budżetu do zera). Zysk = oszczędzone wydatki − utracona marża pacjentów, którzy bez")
    r("    kampanii by nie przyszli. Dodatkowość nieznana (sekcja D), więc trzy warianty: 100%, 50% i 0% pacjentów dodatkowych.")
    r("    Scenariusz poranka (sekcja C) to możliwy dodatkowy zysk z wyłączenia, tylko jeśli hipoteza Kuby jest prawdziwa.")
    wiersze = []
    for _, p in P.iterrows():
        for f in (1.0, 0.5, 0.0):
            wiersze.append({"kampania": p.kampania, "regula": p.regula, "dodatkowi_proc": int(100 * f),
                            "oszczednosc_wydatkow": p.wydatki_rok, "utracona_marza90": round(f * p.nowi_rok * p.marza90),
                            "zmiana_marzy90": round(p.wydatki_rok - f * p.nowi_rok * p.marza90),
                            "zmiana_marzy180": round(p.wydatki_rok - f * p.nowi_rok * p.marza180)})
    pokaz(pd.DataFrame(wiersze))
    sc = C.set_index(["scenariusz", "regula"]).marza_180_zl
    r(f"    Scenariusz poranka przy wyłączeniu obu kampanii: od {zl(sc.min())} do {zl(sc.max())} zł marży w 180 dniach rocznie")
    r("    (tylko zmiana rozkładu opóźnień albo cały spadek w starych kampaniach, obie reguły; sekcja C).")
    r("    Uwaga: część retencji pokazała, że wyłączenie kampanii nie musi podnieść powrotu, bo nie wiemy, gdzie ci pacjenci")
    r("    kupiliby bez kampanii (recenzja Codeksa w kroku 3).")

    r("\nE2. NAPRAWIĆ. Każda droga osobno, kwoty roczne dla obu nowych kampanii (okres 2), przyjęta reguła i sesja płatności.")
    # E2a: zwroty L4
    r("\n  E2a. Obietnica reklamy i strona wejścia: odsetek zwrotów po wizytach L4 spada do poziomu L4 pozostałych pacjentów.")
    r("       Wariant A: wizyty, które dziś kończą się zwrotem, zostają opłacone (pacjent dostaje to, co obiecano), zysk = zwrot.")
    r("       Wariant B: uczciwa obietnica odstrasza pacjentów, którzy nie dostaliby L4, i nie kupują; zysk = 25 zł kosztu")
    r("       lekarza za wizytę, a przy tych samych wydatkach jest tyle samo mniej zamówień (koszt pozyskania rośnie).")
    wiersze = []
    for reg in ("Z1K", "Z2"):
        b_old = B1[(B1.regula == reg) & (B1.pacjenci == "pozostali")].iloc[0]
        for kamp in ("meta_prosp_l4_szybko", "tt_prosp_l4_15min", "nowe kampanie"):
            b = B1[(B1.regula == reg) & (B1.pacjenci == kamp)].iloc[0]
            unik = b.wizyty_L4_odbyte * max(b.L4_zwrot_proc - b_old.L4_zwrot_proc, 0) / 100
            wiersze.append({"kampania": kamp, "regula": reg, "wizyty_L4": b.wizyty_L4_odbyte, "L4_zwrot_proc": b.L4_zwrot_proc,
                            "pozostali_proc": b_old.L4_zwrot_proc, "zwrotow_mniej": round(unik),
                            "wariant_A_zl": round(unik * b.sredni_zwrot_L4_zl), "wariant_B_zl": round(unik * 25)})
    E2a = pd.DataFrame(wiersze)
    pokaz(E2a, "       ")
    for reg in ("Z1K", "Z2"):
        g = w90[w90[f"nowa_{reg}"] & (w90.cel1 == "l4")]
        pr_ok, pr_ref = g[g.status1 == "completed"].powrot90.mean(), g[g.status1 == "refunded"].powrot90.mean()
        unik = E2a[(E2a.regula == reg) & (E2a.kampania == "nowe kampanie")].zwrotow_mniej.iloc[0]
        r(f"       Dopisek do wariantu A ({reg}, scenariusz): pacjenci nowych kampanii z pierwszym L4 wracają w 90 dniach w "
          f"{100 * pr_ok:.1f}% po wizycie bez zwrotu i w {100 * pr_ref:.1f}% po zwrocie; różnica × {unik} × {WARTOSC} zł = "
          f"{zl(unik * (pr_ok - pr_ref) * WARTOSC)} zł rocznie.")

    # E2b: zgoda marketingowa
    r("\n  E2b. Zgoda marketingowa: udział zgód pacjentów nowych kampanii rośnie do poziomu pozostałych pacjentów.")
    r("       Dwa odczytania wartości jednej dodatkowej zgody: (1) powrót przypisany do newslettera i SMS-a u pacjentów ze")
    r("       zgodą (pacjenci bez zgody nie mają takich powrotów wcale); (2) cała różnica powrotu w 90 dniach między pacjentami")
    r("       ze zgodą i bez niej. Jeśli (2) jest mniejsze od (1), pacjenci ze zgodą wracają przez newsletter i SMS, ale bez")
    r("       zgody wracają prawie tak samo często inną drogą.")
    wiersze = []
    for reg in ("Z1K", "Z2"):
        kol = "kampania" if reg == "Z1K" else "kampania_z2"
        poz = w2[~w2[kol].isin(NOWE)]
        u_old = 100 * (poz.zgoda == 1).mean()
        for kamp, lista in (("meta_prosp_l4_szybko", ["meta_prosp_l4_szybko"]), ("tt_prosp_l4_15min", ["tt_prosp_l4_15min"]),
                            ("nowe kampanie", list(NOWE))):
            g = w2[w2[kol].isin(lista)]
            n_rok = int(pe[(pe.okres == 2)][kol].isin(lista).sum())
            u_new = 100 * (g.zgoda == 1).mean()
            dod = n_rok * max(u_old - u_new, 0) / 100
            crm_r = g[g.zgoda == 1].powrot_crm90.mean() - g[g.zgoda == 0].powrot_crm90.mean()
            cal_r = g[g.zgoda == 1].powrot90.mean() - g[g.zgoda == 0].powrot90.mean()
            wiersze.append({"kampania": kamp, "regula": reg, "nowi_rok": n_rok, "zgoda_proc": round(u_new, 1),
                            "pozostali_proc": round(u_old, 1), "dodatkowe_zgody": round(dod),
                            "roznica_powrotu_crm_pkt": round(100 * crm_r, 2), "roznica_powrotu_cala_pkt": round(100 * cal_r, 2),
                            "wartosc_1_zl": round(dod * crm_r * WARTOSC), "wartosc_2_zl": round(dod * cal_r * WARTOSC)})
    E2b = pd.DataFrame(wiersze)
    pokaz(E2b, "       ")

    # E2c: przeglądarki wbudowane
    r("\n  E2c. Strona wejścia w przeglądarkach wbudowanych w aplikacje (Instagram, Facebook, TikTok): konwersja sesji nowych")
    r("       kampanii do pierwszego zamówienia w tej samej sesji, okres 2, cały i przed awarią Safari na iOS (do 16.03.2026).")
    konw = con.sql("""
      WITH s AS (SELECT s.session_id, s.utm_campaign kampania, s.started_at_pl < TIMESTAMP '2026-03-17' przed_awaria,
                        CASE WHEN s.browser IN ('Instagram', 'Facebook', 'TikTok') THEN 'wbudowana' ELSE 'zwykla' END typ
                 FROM czyste.sessions s
                 WHERE s.utm_campaign IN ('meta_prosp_l4_szybko', 'tt_prosp_l4_15min') AND s.started_at_pl >= TIMESTAMP '2025-10-01')
      SELECT kampania, typ, count(*) sesje, count(z.order_id) pierwsze_zamowienia,
             round(100.0 * count(z.order_id) / count(*), 2) konwersja_proc,
             count(*) FILTER (WHERE przed_awaria) sesje_przed_awaria,
             round(100.0 * count(z.order_id) FILTER (WHERE przed_awaria) / nullif(count(*) FILTER (WHERE przed_awaria), 0), 2)
               konwersja_przed_awaria_proc
      FROM s LEFT JOIN zam z ON z.session_id = s.session_id AND z.nr = 1 GROUP BY 1, 2 ORDER BY 1, 2""").df()
    pokaz(konw, "       ")
    E2c = {}
    for kamp in NOWE:
        k = konw[konw.kampania == kamp].set_index("typ")
        luka = (k.at["zwykla", "konwersja_proc"] - k.at["wbudowana", "konwersja_proc"]) / 100
        E2c[kamp] = 0.0
        if luka > 0:
            dod = k.at["wbudowana", "sesje"] * luka * 0.5
            m90 = P[(P.kampania == kamp) & (P.regula == "Z1K")].marza90.iloc[0]
            E2c[kamp] = dod * m90
            r(f"       {kamp}: połowa luki domknięta → {dod:.0f} pierwszych zamówień więcej, {zl(dod * m90)} zł marży w 90 dniach.")
        else:
            r(f"       {kamp}: przeglądarki wbudowane konwertują nie gorzej niż zwykłe w tej samej kampanii "
              f"({k.at['wbudowana', 'konwersja_proc']}% wobec {k.at['zwykla', 'konwersja_proc']}%), więc ta droga nie poprawia")
            r("         wyniku tej kampanii w tym rachunku. Niska konwersja to cecha ruchu z kampanii, nie samej przeglądarki.")
    E2c["nowe kampanie"] = sum(E2c.values())

    # E2d: poranek
    r("\n  E2d. Przepustowość poranka (obsada internistów 6:00–11:59): wartość jak w sekcji C, od "
      f"{zl(sc.min())} do {zl(sc.max())} zł rocznie, tylko jeśli opóźnienia obniżają powroty. Kosztu dodatkowej obsady")
    r("       nie ma w danych (koszt lekarza w zadaniu to stawka za wizytę, nie za dyżur), więc tej drogi nie da się")
    r("       wycenić netto.")

    # E3: zestawienie
    naglowek("E3. ZESTAWIENIE NA ROK: OBECNY WYNIK, NAPRAWIĆ, WYŁĄCZYĆ (zmiana marży w 90 dniach od pozyskania, zł)")
    r("   obecny_wynik = nowi × marża w 90 dniach − wydatki. Naprawić: A albo B ze zwrotów L4 (E2a), plus większa z dwóch")
    r("   wartości zgody (E2b), plus przeglądarki (E2c). Wyłączyć: zmiana marży = wydatki − dodatkowi × marża (E1); przy 100%")
    r("   dodatkowych to dokładnie −obecny_wynik. Scenariusz poranka osobno (sekcja C), bo zależy od niepotwierdzonej hipotezy.")
    wiersze = []
    for kamp in ("meta_prosp_l4_szybko", "tt_prosp_l4_15min", "nowe kampanie"):
        kp = "obie" if kamp == "nowe kampanie" else kamp
        for reg in ("Z1K", "Z2"):
            p = P[(P.kampania == kp) & (P.regula == reg)].iloc[0]
            a = E2a[(E2a.kampania == kamp) & (E2a.regula == reg)].iloc[0]
            b = E2b[(E2b.kampania == kamp) & (E2b.regula == reg)].iloc[0]
            zg = max(b.wartosc_1_zl, b.wartosc_2_zl, 0)
            pr = round(E2c[kamp]) if reg == "Z1K" else 0
            wiersze.append({"kampania": kamp, "regula": reg, "obecny_wynik": p.wynik90_rok,
                            "napraw_zwroty_A": a.wariant_A_zl, "napraw_zwroty_B": a.wariant_B_zl, "napraw_zgoda": zg,
                            "napraw_przegladarki": pr,
                            "po_naprawie_A": p.wynik90_rok + a.wariant_A_zl + zg + pr,
                            "po_naprawie_B": p.wynik90_rok + a.wariant_B_zl + zg + pr,
                            "wylacz_100proc_dodatkowi": round(p.wydatki_rok - p.nowi_rok * p.marza90),
                            "wylacz_50proc": round(p.wydatki_rok - 0.5 * p.nowi_rok * p.marza90),
                            "wylacz_0proc": p.wydatki_rok})
    pokaz(pd.DataFrame(wiersze))
    r("   Kolumny napraw_* i wylacz_* to zmiana marży wobec dziś. po_naprawie = wynik kampanii po naprawie. Przy wyłączeniu")
    r("   tracimy też ewentualne przyszłe naprawy. Oba warianty zakładają, że reszta biznesu się nie zmienia.")

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"zapisano {WYNIK} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
