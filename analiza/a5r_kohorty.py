"""A5 retencja, krok 2 — kohorty dzienne, powroty, zamówienia i marża na pacjenta (2026-10-19).

Definicje z analiza/definicje.py (notatki/ZALOZENIA.md 16–27): nowy pacjent N1, powrót R2 (kolejne zamówienie
nieanulowane), okna 30/60/90 dni, tylko kohorty z pełnym oknem, porównanie okresów na tych samych dniach
kalendarzowych, przy każdym wyniku liczba pacjentów.

Marża na pacjenta = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza (także za wizyty zwrócone),
przed kosztem pozyskania (kampanie, prowizja afiliacyjna). Liczona narastająco od dnia wejścia do kohorty
(dzień 0, z pierwszym zamówieniem) do N-tego dnia; tylko kohorty, które miały pełne N dni.

  1. Porównanie okresów na tych samych dniach kalendarzowych: powrót, kolejne zamówienia, marża na pacjenta.
  2. Krzywa „dzień od pierwszego zakupu”: odsetek pacjentów z powrotem do dnia d.
  3. Marża na pacjenta w kolejnych 30-dniowych miesiącach od pierwszego zakupu.
  4. Kohorty miesięczne (z kohort dziennych) i te same miesiące rok do roku.
  5. Start od zera: zamówienia i przychód nowych i powracających pacjentów.
  6. Kohorty tygodniowe (szereg do szukania zdarzeń; pełny szereg dzienny w CSV).

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/a5r_kohorty.py
Wynik: analiza/wyniki/a5r_kohorty.txt, analiza/wyniki/a5r_kohorty_dzienne.csv
"""

import datetime as dt
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402

WYNIK = os.path.join(D.KATALOG, "analiza", "wyniki", "a5r_kohorty.txt")
WYNIK_DZIENNE = os.path.join(D.KATALOG, "analiza", "wyniki", "a5r_kohorty_dzienne.csv")
KONIEC = D.KONIEC
OKNA_EK = (30, 60, 90, 180, 365)       # okna dla zamówień i marży na pacjenta
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 200)


def zbuduj_pac(con):
    """`pac`: jeden wiersz na nowego pacjenta, z dniem do powrotu i sumami w oknach OKNA_EK."""
    kol = []
    for w in OKNA_EK:
        kol += [f"count(*) FILTER (WHERE e.zamowienie AND e.nieanul AND NOT e.pierwsze AND e.dni <= {w}) kol_zam_{w}",
                f"coalesce(sum(e.przychod) FILTER (WHERE e.dni <= {w}), 0) przychod_{w}",
                f"coalesce(sum(e.go) FILTER (WHERE e.dni <= {w}), 0) go_{w}",
                f"coalesce(sum(e.koszt_lekarza) FILTER (WHERE e.dni <= {w}), 0) koszt_{w}",
                f"coalesce(sum(e.marza) FILTER (WHERE e.dni <= {w}), 0) marza_{w}"]
    con.execute(f"""
      CREATE TEMP TABLE pac AS
      SELECT p.user_id, p.d0, p.okres, p.dni_R2, {', '.join(kol)}
      FROM powr p LEFT JOIN ek e USING (user_id)
      GROUP BY ALL""")


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False)
    zbuduj_pac(con)
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def df(sql):
        return con.sql(sql).df()

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    r(f"A5 RETENCJA — KOHORTY DZIENNE, POWROTY, ZAMÓWIENIA I MARŻA NA PACJENTA ({dt.datetime.now():%Y-%m-%d %H:%M})")
    r("Schemat `czyste`, definicje z analiza/definicje.py (ZALOZENIA.md 16–27). Okres 1 = kohorty X 2024 – IX 2025,")
    r("okres 2 = kohorty X 2025 – IX 2026. Powrót = kolejne zamówienie nieanulowane najpóźniej N-tego dnia po dniu kohorty.")
    r("Marża = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza (25 zł internista, 200 zł psychiatra,")
    r("100 zł pozostali, także pediatra; za wizyty odbyte i zwrócone), narastająco od dnia 0 do dnia N, przed kosztem")
    r("pozyskania. Tylko kohorty z pełnym oknem. Porównanie okresów: okres 1 obcięty do tego samego dnia roku, co")
    r("ostatnia dojrzała kohorta okresu 2 (ZALOZENIA.md 27). n = liczba pacjentów.")

    # ============ 1. PORÓWNANIE OKRESÓW ============
    r("\n" + "=" * 110)
    r("1. OKRES 1 WOBEC OKRESU 2 NA TYCH SAMYCH DNIACH KALENDARZOWYCH")
    r("=" * 110)
    wiersze = []
    for w in OKNA_EK:
        g1, g2 = D.granice_por(w)
        if g2 < dt.date.fromisoformat(D.OKRES2):      # okres 2 bez dojrzałych kohort: okres 1 w całości
            g1 = g2
        for o, g in ((1, g1), (2, g2)):
            x = df(f"""
              SELECT {w} okno_dni, {o} okres, DATE '{g}' kohorty_do, count(*) n,
                     round(100.0 * count(*) FILTER (WHERE dni_R2 <= {w}) / nullif(count(*), 0), 1) powrot_proc,
                     round(avg(kol_zam_{w}), 3) kolejne_zam_na_pac,
                     round(avg(przychod_{w}), 1) przychod_na_pac, round(avg(go_{w}), 1) go_na_pac,
                     round(avg(koszt_{w}), 1) koszt_lek_na_pac, round(avg(marza_{w}), 1) marza_na_pac
              FROM pac WHERE okres = {o} AND d0 <= DATE '{g}'""")
            wiersze.append(x)
    t1 = pd.concat(wiersze)
    pokaz(t1)
    r("     Okno 365 dni: okres 2 nie ma jeszcze kohort z pełnym rokiem (n = 0), więc liczba dotyczy tylko okresu 1.")
    r("\n1b. Zmiana okresu 2 wobec okresu 1 (te same dni kalendarzowe)")
    p = t1.pivot(index="okno_dni", columns="okres")
    zm = pd.DataFrame({
        "okno_dni": p.index,
        "n_o1": p[("n", 1)].values, "n_o2": p[("n", 2)].values,
        "powrot_o1": p[("powrot_proc", 1)].values, "powrot_o2": p[("powrot_proc", 2)].values,
        "powrot_zmiana_pkt": (p[("powrot_proc", 2)] - p[("powrot_proc", 1)]).round(1).values,
        "marza_o1": p[("marza_na_pac", 1)].values, "marza_o2": p[("marza_na_pac", 2)].values,
        "marza_zmiana_zl": (p[("marza_na_pac", 2)] - p[("marza_na_pac", 1)]).round(1).values,
        "marza_zmiana_proc": (100 * p[("marza_na_pac", 2)] / p[("marza_na_pac", 1)] - 100).round(1).values})
    pokaz(zm[zm.n_o2 > 0])

    # ============ 2. KRZYWA DZIEŃ OD PIERWSZEGO ZAKUPU ============
    r("\n" + "=" * 110)
    r("2. ODSETEK PACJENTÓW Z POWROTEM DO DNIA d OD PIERWSZEGO ZAKUPU (każdy punkt na tych samych dniach kalendarzowych)")
    r("=" * 110)
    kr = []
    for d in (1, 3, 7, 14, 21, 30, 45, 60, 90, 120, 150, 180, 270, 365):
        g1, g2 = D.granice_por(d)
        kr.append(df(f"""
          SELECT {d} dzien,
                 count(*) FILTER (WHERE okres = 1 AND d0 <= DATE '{g1}') n_o1,
                 round(100.0 * count(*) FILTER (WHERE okres = 1 AND d0 <= DATE '{g1}' AND dni_R2 <= {d})
                       / nullif(count(*) FILTER (WHERE okres = 1 AND d0 <= DATE '{g1}'), 0), 1) proc_o1,
                 count(*) FILTER (WHERE okres = 2 AND d0 <= DATE '{g2}') n_o2,
                 round(100.0 * count(*) FILTER (WHERE okres = 2 AND d0 <= DATE '{g2}' AND dni_R2 <= {d})
                       / nullif(count(*) FILTER (WHERE okres = 2 AND d0 <= DATE '{g2}'), 0), 1) proc_o2
          FROM pac"""))
    k = pd.concat(kr)
    k["o2_do_o1"] = (k.proc_o2 / k.proc_o1).round(2)
    pokaz(k)
    r("     o2_do_o1 = powrót okresu 2 jako ułamek powrotu okresu 1 (1,00 = bez zmiany).")

    # ============ 3. MARŻA W KOLEJNYCH MIESIĄCACH ============
    r("\n" + "=" * 110)
    r("3. MARŻA I ZAMÓWIENIA NA PACJENTA W KOLEJNYCH 30-DNIOWYCH MIESIĄCACH OD PIERWSZEGO ZAKUPU")
    r("=" * 110)
    r("   Miesiąc 1 = dni 0–30 (z pierwszym zamówieniem), miesiąc m = dni 30(m−1)+1 … 30m. Każdy miesiąc na tych samych")
    r("   dniach kalendarzowych: kohorty, które miały pełne 30m dni. Zamówienia = nieanulowane, w miesiącu 1 bez pierwszego.")
    mies = []
    for m in range(1, 13):
        lo, hi = (0 if m == 1 else 30 * (m - 1) + 1), 30 * m
        g1, g2 = D.granice_por(hi)
        for o, g in ((1, g1), (2, g2)):
            mies.append(df(f"""
              WITH k AS (SELECT user_id FROM pac WHERE okres = {o} AND d0 <= DATE '{g}'),
                   e AS (SELECT * FROM ek WHERE user_id IN (SELECT user_id FROM k) AND dni BETWEEN {lo} AND {hi})
              SELECT {m} miesiac, {o} okres, (SELECT count(*) FROM k) n,
                     round(1.0 * count(*) FILTER (WHERE zamowienie AND nieanul AND NOT pierwsze) / nullif((SELECT count(*) FROM k), 0), 3) zam_na_pac,
                     round(sum(przychod) / nullif((SELECT count(*) FROM k), 0), 1) przychod_na_pac,
                     round(sum(go) / nullif((SELECT count(*) FROM k), 0), 1) go_na_pac,
                     round(sum(koszt_lekarza) / nullif((SELECT count(*) FROM k), 0), 1) koszt_lek_na_pac,
                     round(sum(marza) / nullif((SELECT count(*) FROM k), 0), 1) marza_na_pac
              FROM e"""))
    t3 = pd.concat(mies)
    p3 = t3.pivot(index="miesiac", columns="okres")
    t3w = pd.DataFrame({"miesiac": p3.index, "n_o1": p3[("n", 1)].values, "n_o2": p3[("n", 2)].values,
                        "zam_na_pac_o1": p3[("zam_na_pac", 1)].values, "zam_na_pac_o2": p3[("zam_na_pac", 2)].values,
                        "marza_na_pac_o1": p3[("marza_na_pac", 1)].values, "marza_na_pac_o2": p3[("marza_na_pac", 2)].values})
    pokaz(t3w)
    r("     Szczegóły (przychód po zwrotach, TelemediGO, koszt lekarza na pacjenta):")
    pokaz(t3)

    # ============ 4. KOHORTY MIESIĘCZNE ============
    r("\n" + "=" * 110)
    r("4. KOHORTY MIESIĘCZNE (miesiąc pierwszego zakupu); puste = miesiąc bez pełnego okna dla wszystkich swoich dni")
    r("=" * 110)
    kol = []
    for w in (30, 60, 90, 180, 365):
        pelny = f"last_day(min(d0)) <= DATE '{KONIEC}' - {w}"
        kol.append(f"CASE WHEN {pelny} THEN round(100.0 * count(*) FILTER (WHERE dni_R2 <= {w}) / count(*), 1) END powrot{w}"
                   if w <= 90 else "NULL::DOUBLE x" + str(w))
        kol.append(f"CASE WHEN {pelny} THEN round(avg(marza_{w}), 1) END marza{w}")
    kol.append(f"CASE WHEN last_day(min(d0)) <= DATE '{KONIEC}' - 90 THEN round(avg(kol_zam_90), 3) END kol_zam90")
    t4 = df(f"""
      SELECT strftime(date_trunc('month', d0), '%Y-%m') miesiac, any_value(okres) okres, count(*) n, {', '.join(kol)}
      FROM pac GROUP BY 1 ORDER BY 1""")
    t4 = t4.drop(columns=[c for c in t4.columns if c.startswith("x")])
    pokaz(t4)

    r("\n4b. Te same miesiące rok do roku (miesiąc okresu 2 wobec tego samego miesiąca okresu 1)")
    t4["mm"] = t4.miesiac.str[5:]
    a, b = t4[t4.okres == 1].set_index("mm"), t4[t4.okres == 2].set_index("mm")
    yoy = pd.DataFrame({"miesiac_o1": a.miesiac, "miesiac_o2": b.miesiac.reindex(a.index), "n_o1": a.n, "n_o2": b.n.reindex(a.index),
                        "n_zmiana_proc": (100 * b.n.reindex(a.index) / a.n - 100).round(1),
                        "powrot90_o1": a.powrot90, "powrot90_o2": b.powrot90.reindex(a.index),
                        "powrot90_zmiana_pkt": (b.powrot90.reindex(a.index) - a.powrot90).round(1),
                        "marza90_o1": a.marza90, "marza90_o2": b.marza90.reindex(a.index),
                        "marza90_zmiana_zl": (b.marza90.reindex(a.index) - a.marza90).round(1)})
    pokaz(yoy.reset_index(drop=True))

    # ============ 5. START OD ZERA ============
    r("\n" + "=" * 110)
    r("5. START OD ZERA: ZAMÓWIENIA I PRZYCHÓD W OKRESIE WEDŁUG TEGO, KIEDY PACJENT PRZYSZEDŁ")
    r("=" * 110)
    r("   Okres zamówienia (data płatności) × rodzaj: pierwsze zamówienie (nowy pacjent), powtórne pacjentów z kohort")
    r("   okresu 1, powtórne pacjentów z kohort okresu 2. Wszystkie zamówienia (także anulowane); przychód po zwrotach,")
    r("   TelemediGO osobno, marża przed kosztem pozyskania.")
    t5 = df(f"""
      SELECT CASE WHEN t < TIMESTAMP '{D.OKRES2}' THEN 1 ELSE 2 END okres_zdarzenia,
             CASE WHEN zamowienie AND pierwsze THEN 'a_pierwsze' WHEN NOT zamowienie THEN 'd_telemedigo'
                  WHEN okres = 1 THEN 'b_powtorne_kohorty_o1' ELSE 'c_powtorne_kohorty_o2' END rodzaj,
             count(*) FILTER (WHERE zamowienie) zamowienia, count(*) FILTER (WHERE zamowienie AND nieanul) nieanulowane,
             count(*) FILTER (WHERE NOT zamowienie) telemedigo,
             round(sum(przychod)) przychod_zl, round(sum(go)) go_zl, round(sum(koszt_lekarza)) koszt_lek_zl, round(sum(marza)) marza_zl
      FROM ek GROUP BY ALL ORDER BY 1, 2""")
    pokaz(t5)
    s5 = t5.groupby("okres_zdarzenia")[["zamowienia", "przychod_zl", "marza_zl"]].sum()
    r(f"     Razem zamówienia: okres 1 {int(s5.zamowienia[1])}, okres 2 {int(s5.zamowienia[2])} "
      f"({100 * s5.zamowienia[2] / s5.zamowienia[1] - 100:+.1f}%).")

    # ============ 6. KOHORTY TYGODNIOWE ============
    r("\n" + "=" * 110)
    r("6. KOHORTY TYGODNIOWE (tydzień od poniedziałku; powrót tylko przy pełnym oknie dla każdego dnia tygodnia)")
    r("=" * 110)
    kol = []
    for w in (30, 60, 90):
        pelny = f"max(d0) <= DATE '{KONIEC}' - {w}"
        kol.append(f"CASE WHEN {pelny} THEN round(100.0 * count(*) FILTER (WHERE dni_R2 <= {w}) / count(*), 1) END powrot{w}")
    kol.append(f"CASE WHEN max(d0) <= DATE '{KONIEC}' - 90 THEN round(avg(marza_90), 1) END marza90")
    t6 = df(f"""
      SELECT date_trunc('week', d0)::DATE tydzien, count(*) n, count(DISTINCT d0) dni, {', '.join(kol)}
      FROM pac GROUP BY 1 ORDER BY 1""")
    pokaz(t6)

    # ============ CSV: kohorty dzienne ============
    kol = []
    for w in (30, 60, 90):
        kol.append(f"CASE WHEN d0 <= DATE '{KONIEC}' - {w} THEN count(*) FILTER (WHERE dni_R2 <= {w}) END powroty{w}")
    for w in OKNA_EK:
        kol += [f"CASE WHEN d0 <= DATE '{KONIEC}' - {w} THEN sum(kol_zam_{w}) END kolejne_zam{w}",
                f"CASE WHEN d0 <= DATE '{KONIEC}' - {w} THEN round(sum(marza_{w}), 2) END marza{w}_zl"]
    dz = df(f"""
      SELECT d0 dzien, okres, isodow(d0) dzien_tygodnia, count(*) nowi, {', '.join(kol)}
      FROM pac GROUP BY d0, okres ORDER BY d0""")
    dz.to_csv(WYNIK_DZIENNE, index=False, encoding="utf-8")
    r(f"\nKohorty dzienne ({len(dz)} dni): {os.path.relpath(WYNIK_DZIENNE, D.KATALOG)}")
    r("Kolumny: nowi, powroty30/60/90 (liczba pacjentów z powrotem; puste = brak pełnego okna), kolejne_zamN, marzaN_zl (sumy).")

    con.close()
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Raport: {os.path.relpath(WYNIK, D.KATALOG)} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
