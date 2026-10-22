"""E — liczby dla nowych wykresów strony (etap 5 dopracowania grafiki, polecenie Kuby 2026-10-22).

Strona rysuje z nich wykresy, a teksty zostają bez zmian. Ten skrypt liczy tylko to, czego nie ma w raportach jako
liczników: opóźnienia według godziny terminu jako liczby wizyt odbytych i spóźnionych ponad 15 minut (internista
i pozostali lekarze, wszyscy pacjenci, okres według dnia terminu — ta sama definicja co analiza/d_retencja.py, punkt 1).
Kontrola: odsetki z tych liczników muszą się zgadzać z d_retencja.json (internista) i z tabelą w d_retencja.txt
(pozostali lekarze, przez b2_eksport_c.wartosci).

Uruchomienie z głównego folderu: python -I analiza/e_wykresy.py → analiza/wyniki/e_wykresy.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
import a5r_punktualnosc as RP  # noqa: E402

WYNIKI = os.path.join(D.KATALOG, "analiza", "wyniki")


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=False)
    RP.zbuduj_wizyty(con)
    t = con.sql(f"""
      WITH wt AS (
        SELECT *, CASE WHEN scheduled_at < TIMESTAMP '{D.OKRES2}' THEN 1
                       WHEN scheduled_at < TIMESTAMP '2026-10-01' THEN 2 END okres_t
        FROM wiz)
      SELECT CASE WHEN specialization = 'internista' THEN 'internista' ELSE 'pozostali' END grupa, h, okres_t okres,
             count(*) odbyte, count(*) FILTER (WHERE op > 15) spoznione
      FROM wt WHERE op IS NOT NULL AND okres_t IS NOT NULL GROUP BY ALL ORDER BY 1, 2, 3""").df()
    with open(os.path.join(WYNIKI, "d_retencja.json"), encoding="utf-8") as f:
        dr = json.load(f)
    import b2_eksport_c as B2
    pg = B2.wartosci(B2.Zrodla())["pozostali_godz"]
    G = {}
    bledy = 0
    for _, w in t.iterrows():
        h, o = int(w.h), int(w.okres)
        G.setdefault(w.grupa, {}).setdefault(str(h), {})[str(o)] = {"odbyte": int(w.odbyte), "spoznione": int(w.spoznione)}
        p = 100 * w.spoznione / w.odbyte
        if w.grupa == "internista":
            wz_p = dr[f"op_internista_wszyscy_godz{h:02d}_ponad15_proc_okres{o}"]
            wz_n = dr[f"op_internista_wszyscy_godz{h:02d}_wizyty_okres{o}"]
            ok = abs(p - wz_p) < 1e-3 and int(wz_n) == int(w.odbyte)
        else:
            wz_n, wz_p = pg[h][o - 1], pg[h][o + 1]
            ok = int(wz_n) == int(w.odbyte) and abs(round(p, 1) - wz_p) < 1e-9
        bledy += not ok
        if not ok:
            print(f"RÓŻNICA: {w.grupa} {h}:00 okres {o}: {w.odbyte} / {p:.4f}% wobec {wz_n} / {wz_p}")
    if bledy:
        raise SystemExit(f"{bledy} różnic wobec d_retencja")
    with open(os.path.join(WYNIKI, "e_wykresy.json"), "w", encoding="utf-8") as f:
        json.dump({"godziny": G}, f, ensure_ascii=False, indent=1)
    print(f"Zapisano analiza/wyniki/e_wykresy.json ({len(t)} wierszy, 0 różnic wobec d_retencja)")


if __name__ == "__main__":
    main()
