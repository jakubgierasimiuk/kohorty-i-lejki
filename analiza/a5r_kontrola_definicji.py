"""A5 retencja — kontrola wspólnego modułu definicji (2026-10-19).

Liczy sekcję 6 raportu A4 (liczby według przyjętych definicji, podpunkty 6a–6e) na tabelach z
analiza/definicje.py i porównuje wynik wiersz po wierszu z zapisanym raportem analiza/wyniki/a4_definicje.txt.
Zgodność co do znaku oznacza, że moduł odtwarza definicje z A4 co do sztuki.

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/a5r_kontrola_definicji.py
Wynik: analiza/wyniki/a5r_kontrola_definicji.txt
"""

import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402

RAPORT_A4 = os.path.join(D.KATALOG, "analiza", "wyniki", "a4_definicje.txt")
WYNIK = os.path.join(D.KATALOG, "analiza", "wyniki", "a5r_kontrola_definicji.txt")
KONIEC = D.KONIEC


def sekcja6(con):
    """Te same zapytania co sekcja 6 w a4_definicje.py, na tabelach modułu (bez kolumny `war`)."""
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def tab(sql, wciecie="     "):
        for linia in con.sql(sql).df().to_string(index=False).splitlines():
            r(wciecie + linia)

    r("6a. Nowi pacjenci według statusu pierwszego zamówienia i powrót R2 w 90 dniach (okres 2: kohorty do 2.07.2026)")
    tab(f"""
      SELECT z.status status_pierwszego, count(*) FILTER (WHERE p.okres = 1) nowi_o1, count(*) FILTER (WHERE p.okres = 2) nowi_o2,
             round(100.0 * count(*) FILTER (WHERE p.okres = 1 AND p.dni_R2 <= 90) / count(*) FILTER (WHERE p.okres = 1), 1) powrot90_o1,
             round(100.0 * count(*) FILTER (WHERE p.okres = 2 AND p.d0 <= DATE '{KONIEC}' - 90 AND p.dni_R2 <= 90)
                   / count(*) FILTER (WHERE p.okres = 2 AND p.d0 <= DATE '{KONIEC}' - 90), 1) powrot90_o2
      FROM powr p JOIN zam z ON z.user_id = p.user_id AND z.nr = 1
      GROUP BY 1 ORDER BY 2 DESC""")
    r("\n6b. Powrót R2 w 30/60/90 dniach, wszyscy nowi pacjenci, % kohorty")
    tab(D.stopy())
    r("     Porównywalne dni kalendarzowe (recenzja Codeksa): w okresie 1 tylko kohorty do tego samego dnia roku,")
    r("     co ostatnia dojrzała kohorta okresu 2 (30 dni: 31.08, 60 dni: 1.08, 90 dni: 2.07); n = liczba pacjentów")
    tab(D.stopy_por())
    for regula, opis in (("Z1K", "reguła przyjęta"), ("Z2", "sesja płatności, pokazywana obok przy ekonomii kampanii")):
        r(f"\n6c. Nowi pacjenci według kanału ({regula}: {opis}) i powrót R2 w 90 dniach")
        tab(f"""
          SELECT z.kanal, count(*) FILTER (WHERE z.okres = 1) nowi_o1, count(*) FILTER (WHERE z.okres = 2) nowi_o2,
                 round(100.0 * count(*) FILTER (WHERE z.okres = 1) / sum(count(*) FILTER (WHERE z.okres = 1)) OVER (), 1) udzial_o1,
                 round(100.0 * count(*) FILTER (WHERE z.okres = 2) / sum(count(*) FILTER (WHERE z.okres = 2)) OVER (), 1) udzial_o2,
                 round(100.0 * count(*) FILTER (WHERE p.okres = 1 AND p.dni_R2 <= 90) / count(*) FILTER (WHERE p.okres = 1), 1) powrot90_o1,
                 round(100.0 * count(*) FILTER (WHERE p.okres = 2 AND p.d0 <= DATE '{KONIEC}' - 90 AND p.dni_R2 <= 90)
                       / nullif(count(*) FILTER (WHERE p.okres = 2 AND p.d0 <= DATE '{KONIEC}' - 90), 0), 1) powrot90_o2
          FROM zr z JOIN powr p ON p.user_id = z.user_id WHERE z.regula = '{regula}'
          GROUP BY 1 ORDER BY 3 DESC""")
    r("\n6d. Prowizja afiliacyjna według reguły Z1K i według kodu RANKING10, zł")
    tab("""
      SELECT 'Z1K' wariant, 25 * count(*) FILTER (WHERE okres = 1) okres1_zl, 25 * count(*) FILTER (WHERE okres = 2) okres2_zl,
             25 * count(*) razem_zl FROM zr WHERE regula = 'Z1K' AND kanal = 'afiliacja_ranking'
      UNION ALL
      SELECT 'kod RANKING10', 25 * count(*) FILTER (WHERE okres = 1), 25 * count(*) FILTER (WHERE okres = 2), 25 * count(*)
      FROM reg WHERE kod = 'RANKING10'""")
    r("\n6e. Wejścia z CRM: zamówienia (i zakupy TelemediGO) pacjenta do 24 godzin od wejścia, na 1000 wejść")
    r("     (wejścia z pełnymi 61 dniami obserwacji, pacjenci po pierwszym zakupie)")
    r("     zamowienia_24h = nieanulowane, każde wejście osobno; z_anulowanymi = wszystkie płatności;")
    r("     rozlacznie = każde nieanulowane zamówienie przypisane tylko do ostatniego wejścia z CRM przed płatnością")
    tab("""
      WITH rozl AS (SELECT kampania, count(*) n FROM crm_rozl GROUP BY 1)
      SELECT k.kampania, count(DISTINCT k.session_id) wejscia,
             round(1000.0 * (SELECT count(*) FROM po_kontakcie p WHERE p.kampania = k.kampania AND p.byl_pacjentem AND p.dzien = 0)
                   / count(DISTINCT k.session_id), 1) zamowienia_24h_na_1000,
             round(1000.0 * (SELECT count(*) FROM po_kontakcie_wszystkie p WHERE p.kampania = k.kampania AND p.byl_pacjentem
                               AND p.dzien = 0) / count(DISTINCT k.session_id), 1) z_anulowanymi_na_1000,
             any_value(r.n) zamowienia_rozlacznie,
             round(1000.0 * any_value(r.n) / count(DISTINCT k.session_id), 1) rozlacznie_na_1000,
             round(1000.0 * (SELECT count(*) FROM kontakt k2 JOIN czyste.go_memberships g ON g.user_id = k2.pacjent
                               AND timezone('Europe/Warsaw', g.purchased_at) >= k2.ts_utc
                               AND timezone('Europe/Warsaw', g.purchased_at) < k2.ts_utc + INTERVAL 1 DAY
                             WHERE k2.kampania = k.kampania AND k2.byl_pacjentem) / count(DISTINCT k.session_id), 1) go_24h_na_1000
      FROM kontakt k LEFT JOIN rozl r USING (kampania) WHERE k.kanal = 'crm' AND k.byl_pacjentem
      GROUP BY 1 ORDER BY 2 DESC""")
    return linie


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con)
    nowe = "\n".join(sekcja6(con)).splitlines()   # nagłówki "\n6b." to dwa wiersze, jak w zapisanym pliku
    con.close()

    with open(RAPORT_A4, encoding="utf-8") as f:
        a4 = f.read().splitlines()
    start = next(i for i, l in enumerate(a4) if l.startswith("6a. "))
    stare = a4[start:]
    while stare and not stare[-1].strip():
        stare.pop()

    rozne = [(i, s, n) for i, (s, n) in enumerate(zip(stare, nowe)) if s != n]
    zgodne = not rozne and len(stare) == len(nowe)

    out = [f"A5 RETENCJA — KONTROLA MODUŁU analiza/definicje.py ({dt.datetime.now():%Y-%m-%d %H:%M})",
           "Sekcja 6 raportu A4 (6a–6e) policzona na tabelach modułu i porównana z analiza/wyniki/a4_definicje.txt.",
           f"Wierszy w raporcie A4: {len(stare)}, w wyniku modułu: {len(nowe)}, wierszy różnych: {len(rozne)}.",
           "WYNIK: " + ("ZGODNE CO DO ZNAKU" if zgodne else "RÓŻNICE — moduł nie odtwarza A4"), ""]
    for i, s, n in rozne[:40]:
        out += [f"  wiersz {i}:", f"    A4:    {s}", f"    moduł: {n}"]
    out += ["", "Wynik modułu:", ""] + nowe
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out[:4]))
    print(f"Raport: {os.path.relpath(WYNIK, D.KATALOG)}")


if __name__ == "__main__":
    main()
