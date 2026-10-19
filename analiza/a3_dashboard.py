"""A3 — odtworzenie dashboardu: które definicje dają dokładnie jego cztery liczby.

Dashboard (z treści zadania), ostatnie 12 miesięcy (X 2025 – IX 2026) wobec poprzednich 12 (X 2024 – IX 2025):
  +52% pacjentów z pierwszym zakupem, +61% zamówień, +50% przychodu z konsultacji, +40% sprzedanych TelemediGO.

Liczymy na danych surowych (schemat `surowe`) każdą miarę w siatce wariantów:
  wspólne dla wszystkich miar:
    duplikaty   z | bez
    testy       z | bez kodu TEST-QA | bez kont testowych (wszystkie 2 071 zamówień)
    statusy     wszystkie | bez anulowanych | odbyte (completed + refunded) | tylko completed
    granice     czas polski | UTC (dashboard liczony w strefie UTC przesuwa granice o 1–2 godziny)
  osobno dla miar:
    przychód          zapłata | zapłata minus zwroty | cena katalogowa; z TelemediGO albo bez
    nowy pacjent      pierwsze zamówienie | pierwsza płatność łącznie z samym TelemediGO
                      | dla kontroli: kupujący w okresie (nie pierwszy zakup)
    TelemediGO        wszystkie zakupy (duplikatów i testów brak, sekcje 1–2 raportu A2)

Procenty na dashboardzie są zaokrąglone do całości: wariant „pasuje”, gdy wzrost zaokrąglony do całości
równa się liczbie z dashboardu. Kombinacja pasuje, gdy pasują naraz wszystkie cztery miary.
Na końcu: te same miary w kombinacji dashboardu, ale po oczyszczeniu (bez duplikatów i bez kont testowych).

Uruchomienie z głównego folderu projektu:
    python -I analiza/a3_dashboard.py
Wynik: ekran + analiza/wyniki/a3_dashboard.txt (+ pełna siatka: analiza/wyniki/a3_siatka.csv)
"""

import datetime as dt
import itertools
import math
import os
import sys

import duckdb
import pandas as pd

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAZA = os.path.join(KATALOG, "analiza", "telemedi.duckdb")
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "a3_dashboard.txt")
SIATKA = os.path.join(KATALOG, "analiza", "wyniki", "a3_siatka.csv")
pd.set_option("display.width", 220)

CEL = {"nowi": 52, "zamowienia": 61, "przychod": 50, "go": 40}
NAZWY = {"nowi": "pacjenci z pierwszym zakupem", "zamowienia": "zamówienia",
         "przychod": "przychód z konsultacji", "go": "sprzedane TelemediGO"}

DUPLIKATY = ("z", "bez")
TESTY = ("z", "bez_kodu", "bez_kont")
STATUSY = {"wszystkie": ("completed", "cancelled", "no_show", "refunded"),
           "bez_anulowanych": ("completed", "no_show", "refunded"),
           "odbyte": ("completed", "refunded"),
           "completed": ("completed",)}
GRANICE = ("pl", "utc")
PRZYCHOD = ("zaplata", "netto", "katalog")
Z_GO = ("bez_go", "z_go")
NOWY = ("pierwsze_zamowienie", "pierwsza_platnosc", "kupujacy_w_okresie")


def okres(seria_czasu):
    """1 = X 2024 – IX 2025, 2 = X 2025 – IX 2026 (granica 1.10.2025 00:00 w danej strefie)."""
    return (seria_czasu >= pd.Timestamp("2025-10-01")).astype(int) + 1


def main():
    sys.stdout.reconfigure(errors="replace")  # konsola Windows (cp1250) nie ma znaku minus i strzałek
    con = duckdb.connect(BAZA, read_only=True)
    # zamówienia: każdy wiersz surowy z oznaczeniem kopii i testów; czas UTC wyliczony z czasu polskiego
    zam = con.execute("""
      SELECT order_id, user_id, status, list_price::DOUBLE list_price, amount_paid::DOUBLE amount_paid,
             refund_amount::DOUBLE refund_amount, created_at AS t_pl,
             timezone('UTC', timezone('Europe/Warsaw', created_at)) AS t_utc,
             row_number() OVER (PARTITION BY order_id ORDER BY wiersz_w_pliku) > 1 AS kopia,
             coalesce(promo_code = 'TEST-QA', FALSE) AS kod_testowy,
             user_id IN (SELECT user_id FROM surowe.orders WHERE promo_code = 'TEST-QA') AS konto_testowe
      FROM surowe.orders""").df()
    go = con.execute("""
      SELECT membership_id, user_id, (order_id IS NULL) osobno, purchased_at AS t_pl,
             timezone('UTC', timezone('Europe/Warsaw', purchased_at)) AS t_utc
      FROM surowe.go_memberships""").df()
    con.close()
    for t in (zam, go):
        t["okres_pl"], t["okres_utc"] = okres(t["t_pl"]), okres(t["t_utc"])
    # w wariancie UTC zamówienia sprzed 1.10.2024 00:00 UTC (czyli przed 2:00 czasu polskiego) są poza okresem 1
    for t in (zam, go):
        t.loc[t["t_utc"] < pd.Timestamp("2024-10-01"), "okres_utc"] = 0

    linie = []

    def r(tekst=""):
        print(tekst)
        linie.append(tekst)

    def wzrost(p1, p2):
        return 100.0 * (p2 / p1 - 1) if p1 else float("nan")

    def filtr(dup, test, stat):
        m = zam["status"].isin(STATUSY[stat])
        if dup == "bez":
            m &= ~zam["kopia"]
        if test == "bez_kodu":
            m &= ~zam["kod_testowy"]
        elif test == "bez_kont":
            m &= ~zam["konto_testowe"]
        return zam[m]

    # --- każda miara w każdym wariancie ---
    wiersze = []
    for dup, test, stat, gr in itertools.product(DUPLIKATY, TESTY, STATUSY, GRANICE):
        z = filtr(dup, test, stat)
        ok = f"okres_{gr}"
        wsp = dict(duplikaty=dup, testy=test, statusy=stat, granice=gr)
        # zamówienia
        n = z.groupby(ok).size()
        wiersze.append({**wsp, "miara": "zamowienia", "wariant": "-", "p1": n.get(1, 0), "p2": n.get(2, 0)})
        # przychód
        for prz, zgo in itertools.product(PRZYCHOD, Z_GO):
            kol = {"zaplata": z["amount_paid"], "netto": z["amount_paid"] - z["refund_amount"],
                   "katalog": z["list_price"]}[prz]
            s = kol.groupby(z[ok]).sum()
            p1, p2 = s.get(1, 0.0), s.get(2, 0.0)
            if zgo == "z_go":
                g = go.groupby(ok).size() * 89.0
                p1, p2 = p1 + g.get(1, 0.0), p2 + g.get(2, 0.0)
            wiersze.append({**wsp, "miara": "przychod", "wariant": f"{prz}/{zgo}", "p1": p1, "p2": p2})
        # nowi pacjenci
        for nowy in NOWY:
            if nowy == "kupujacy_w_okresie":
                u = z.groupby(ok)["user_id"].nunique()
                p1, p2 = u.get(1, 0), u.get(2, 0)
            else:
                zakupy = z[["user_id", "t_pl", ok]].rename(columns={ok: "okres"})
                if nowy == "pierwsza_platnosc":
                    zakupy = pd.concat([zakupy, go[["user_id", "t_pl", ok]].rename(columns={ok: "okres"})])
                pierwsze = zakupy.sort_values("t_pl").drop_duplicates("user_id")
                c = pierwsze.groupby("okres").size()
                p1, p2 = c.get(1, 0), c.get(2, 0)
            wiersze.append({**wsp, "miara": "nowi", "wariant": nowy, "p1": p1, "p2": p2})
        # TelemediGO (nie zależy od duplikatów, testów ani statusów zamówień — tych w tabeli GO nie ma)
        g = go.groupby(ok).size()
        wiersze.append({**wsp, "miara": "go", "wariant": "wszystkie", "p1": g.get(1, 0), "p2": g.get(2, 0)})

    siatka = pd.DataFrame(wiersze)
    siatka["wzrost_proc"] = [wzrost(a, b) for a, b in zip(siatka["p1"], siatka["p2"])]
    siatka["zaokr"] = siatka["wzrost_proc"].round().astype(int)
    siatka["cel"] = siatka["miara"].map(CEL)
    siatka["pasuje"] = siatka["zaokr"] == siatka["cel"]
    os.makedirs(os.path.dirname(WYNIK), exist_ok=True)
    siatka.to_csv(SIATKA, index=False, float_format="%.4f")

    r(f"A3 — ODTWORZENIE DASHBOARDU ({dt.datetime.now():%Y-%m-%d %H:%M}), dane surowe")
    r("Okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026. Wzrost = okres 2 / okres 1 − 1.")
    r(f"Siatka: {len(siatka):,} wierszy (miara × wariant). Pełna siatka: analiza/wyniki/a3_siatka.csv")

    # --- 1. każda miara osobno: ile wariantów pasuje ---
    r("\n1. Każda miara osobno: zakres wzrostu w siatce i liczba wariantów zgodnych z dashboardem")
    for m in CEL:
        s = siatka[siatka["miara"] == m]
        r(f"   {NAZWY[m]:30} dashboard +{CEL[m]}%  w siatce od {s['wzrost_proc'].min():+.1f}% do "
          f"{s['wzrost_proc'].max():+.1f}%, pasuje {int(s['pasuje'].sum())} z {len(s)} wariantów")

    # --- 2. wpływ każdego wymiaru na każdą miarę (pozostałe wymiary w wersji „surowej”) ---
    r("\n2. Wpływ pojedynczych wymiarów (pozostałe ustawione na: z duplikatami, z testami, wszystkie statusy,")
    r("   czas polski, przychód = zapłata bez TelemediGO, nowy pacjent = pierwsze zamówienie)")
    baza = dict(duplikaty="z", testy="z", statusy="wszystkie", granice="pl")
    wariant_bazowy = {"zamowienia": "-", "przychod": "zaplata/bez_go", "nowi": "pierwsze_zamowienie", "go": "wszystkie"}

    def wybierz(miara, wariant=None, **wymiary):
        w = {**baza, **wymiary}
        s = siatka[(siatka["miara"] == miara) & (siatka["wariant"] == (wariant or wariant_bazowy[miara]))]
        for k, v in w.items():
            s = s[s[k] == v]
        return s.iloc[0]

    def wiersz_wplywu(opis, w_nowi=None, w_przychod=None, **wymiary):
        nadpisane = {"nowi": w_nowi, "przychod": w_przychod}
        komorki = [f"{wybierz(m, nadpisane.get(m), **wymiary)['wzrost_proc']:+6.2f}%" for m in CEL]
        r(f"   {opis:44} " + "  ".join(f"{k:>10}" for k in komorki))

    r(f"   {'':44} " + "  ".join(f"{m:>10}" for m in ("nowi", "zamówienia", "przychód", "GO")))
    r(f"   {'DASHBOARD':44} " + "  ".join(f"{'+' + str(CEL[m]) + '%':>10}" for m in CEL))
    wiersz_wplywu("wszystko surowo")
    wiersz_wplywu("bez duplikatów", duplikaty="bez")
    wiersz_wplywu("bez kodu TEST-QA", testy="bez_kodu")
    wiersz_wplywu("bez kont testowych", testy="bez_kont")
    for stat in ("bez_anulowanych", "odbyte", "completed"):
        wiersz_wplywu(f"statusy: {stat}", statusy=stat)
    wiersz_wplywu("granice okresów w UTC", granice="utc")
    for prz, zgo in (("netto", "bez_go"), ("katalog", "bez_go"), ("zaplata", "z_go")):
        wiersz_wplywu(f"przychód: {prz}, {zgo}", w_przychod=f"{prz}/{zgo}")
    wiersz_wplywu("nowy pacjent: pierwsza płatność (z samym GO)", w_nowi="pierwsza_platnosc")
    wiersz_wplywu("nowy pacjent: kupujący w okresie", w_nowi="kupujacy_w_okresie")

    # --- 3. kombinacje, w których pasują naraz wszystkie cztery ---
    def pasujace(zaokraglenie):
        """Kombinacje (wymiary wspólne + wariant przychodu + wariant nowego pacjenta) zgodne z czterema liczbami."""
        t = siatka.assign(ok=zaokraglenie(siatka["wzrost_proc"]).astype(int) == siatka["cel"])
        wynik = []
        for (dup, test, stat, gr), s in t.groupby(["duplikaty", "testy", "statusy", "granice"]):
            if not (s[s["miara"] == "go"]["ok"].all() and s[s["miara"] == "zamowienia"]["ok"].all()):
                continue
            for _, p in s[(s["miara"] == "przychod") & s["ok"]].iterrows():
                for _, n in s[(s["miara"] == "nowi") & s["ok"]].iterrows():
                    wynik.append(dict(duplikaty=dup, testy=test, statusy=stat, granice=gr,
                                      przychod=p["wariant"], nowy_pacjent=n["wariant"],
                                      nowi=n["wzrost_proc"],
                                      zamowienia=s[s["miara"] == "zamowienia"]["wzrost_proc"].iloc[0],
                                      przychod_proc=p["wzrost_proc"],
                                      go=s[s["miara"] == "go"]["wzrost_proc"].iloc[0]))
        return pd.DataFrame(wynik)

    def pokaz(df):
        df = df.copy()
        for k in ("nowi", "zamowienia", "przychod_proc", "go"):
            df[k] = df[k].map(lambda x: f"{x:+.2f}%")
        for linia in df.to_string(index=False).splitlines():
            r("     " + linia)

    wszystkich = len(DUPLIKATY) * len(TESTY) * len(STATUSY) * len(GRANICE) * len(PRZYCHOD) * len(Z_GO) * len(NOWY)
    komb = pasujace(lambda x: x.round())
    r("\n3. Kombinacje, w których naraz pasują wszystkie cztery liczby dashboardu (zaokrąglenie do całości)")
    r(f"   Wszystkich kombinacji w siatce: {wszystkich}. Pasujących: {len(komb)}.")
    if len(komb):
        pokaz(komb)
        r("   Wartości wymiarów występujące w pasujących kombinacjach:")
        for k in ("duplikaty", "testy", "statusy", "granice", "przychod", "nowy_pacjent"):
            r(f"     {k:14} {', '.join(sorted(komb[k].unique()))}")

    # --- 4. najprostsza pasująca kombinacja i mostek do danych oczyszczonych ---
    GLOWNA = dict(duplikaty="z", testy="z", statusy="wszystkie", granice="pl",
                  przychod="zaplata/bez_go", nowy_pacjent="pierwsze_zamowienie")
    r("\n4. Najprostsza pasująca kombinacja: każdy wiersz pliku orders liczony jako zamówienie, przychód = suma")
    r("   zapłat bez odejmowania zwrotów i bez TelemediGO, nowy pacjent = konto z pierwszym zamówieniem, czas polski.")
    maska = (komb[list(GLOWNA)] == pd.Series(GLOWNA)).all(axis=1) if len(komb) else pd.Series(dtype=bool)
    r(f"   Ta kombinacja jest wśród pasujących: {'tak' if maska.any() else 'NIE'}.")
    if maska.any():
        g = komb[maska].iloc[0]
        rozrzut = {k: abs(komb[k] - g[k]).max() for k in ("nowi", "zamowienia", "przychod_proc", "go")}
        r("   Pozostałe pasujące kombinacje różnią się od niej najwyżej o (punkty procentowe): "
          + ", ".join(f"{NAZWY[m]} {rozrzut[k]:.2f}" for m, k in
                      (("nowi", "nowi"), ("zamowienia", "zamowienia"), ("przychod", "przychod_proc"), ("go", "go"))) + ".")

    kroki = [("dashboard (dane surowe)", dict(duplikaty="z", testy="z"), "zaplata/bez_go"),
             ("bez duplikatów", dict(duplikaty="bez", testy="z"), "zaplata/bez_go"),
             ("bez duplikatów i kont testowych", dict(duplikaty="bez", testy="bez_kont"), "zaplata/bez_go"),
             ("+ przychód po odjęciu zwrotów", dict(duplikaty="bez", testy="bez_kont"), "netto/bez_go")]
    r("\n   Mostek: od liczb dashboardu do danych oczyszczonych, krok po kroku (te same pozostałe definicje)")
    r(f"   {'krok':34} " + "  ".join(f"{NAZWY[m][:26]:>26}" for m in CEL))
    for opis, wym, prz in kroki:
        komorki = []
        for m in CEL:
            w = wybierz(m, prz if m == "przychod" else None, statusy="wszystkie", granice="pl", **wym)
            if m == "przychod":
                komorki.append(f"{w['p1'] / 1e6:.3f} > {w['p2'] / 1e6:.3f} mln {w['wzrost_proc']:+.1f}%")
            else:
                komorki.append(f"{w['p1']:,.0f} > {w['p2']:,.0f} {w['wzrost_proc']:+.1f}%")
        r(f"   {opis:34} " + "  ".join(f"{k:>26}" for k in komorki))
    r("   Ostatni krok (przychód po zwrotach) to już zmiana definicji, a nie czyszczenie. Pokazany, bo dashboard")
    r("   liczy przychód przed zwrotami, a w marży liczymy po zwrotach.")
    czyste = dict(duplikaty="bez", testy="bez_kont", statusy="wszystkie", granice="pl")
    brutto, netto = wybierz("przychod", "zaplata/bez_go", **czyste), wybierz("przychod", "netto/bez_go", **czyste)
    zw1, zw2 = brutto["p1"] - netto["p1"], brutto["p2"] - netto["p2"]
    r(f"   Trop do A5: zwroty (dane oczyszczone) {zw1:,.0f} zł w okresie 1 i {zw2:,.0f} zł w okresie 2, czyli {wzrost(zw1, zw2):+.1f}%.")
    r(f"   Udział zwrotów w zapłatach: {100 * zw1 / brutto['p1']:.1f}% w okresie 1 i {100 * zw2 / brutto['p2']:.1f}% w okresie 2.")

    # --- 5. odporność: obcinanie zamiast zaokrąglania ---
    komb_obc = pasujace(lambda x: x.apply(math.floor))
    r("\n5. Odporność: gdyby dashboard obcinał procenty (np. 60,7% pokazane jako 60%) zamiast zaokrąglać")
    r(f"   Pasujących kombinacji: {len(komb_obc)}.")
    if len(komb_obc):
        pokaz(komb_obc)
        r("   Wartości wymiarów występujące w pasujących kombinacjach:")
        for k in ("duplikaty", "testy", "statusy", "granice", "przychod", "nowy_pacjent"):
            r(f"     {k:14} {', '.join(sorted(komb_obc[k].unique()))}")

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"\nRaport zapisany: {os.path.relpath(WYNIK, KATALOG)}")


if __name__ == "__main__":
    main()
