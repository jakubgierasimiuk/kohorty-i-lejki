"""F — powtarzalność eksportu: pliki danych strony na dysku wobec wersji z commitu (ostatnia kontrola, część 2).

Po ponownym uruchomieniu eksportu (analiza/e_poprawki.py, analiza/e_wykresy.py, analiza/b_eksport.py) porównuje każdy
plik narzedzie/dane_strony/*.js z wersją z podanego commitu (domyślnie HEAD), wartość po wartości (JSON po znaku „=”).
Różnice dzieli na trzy rodzaje:
  - metadane: pola „wygenerowano” i „commit” (data przeliczenia i skrót commitu w stopce strony);
  - szum zmiennoprzecinkowy: liczby różne o mniej niż 1e-9 względnie (kolejność sumowania w bazie);
  - różnice w treści: wszystko inne (to byłby sygnał, że strona po eksporcie pokazuje coś innego niż w commicie).
Pliki tylko czyta; nic nie zapisuje poza raportem.

Uruchomienie z głównego folderu:
    python -I analiza/f_eksport_powtarzalnosc.py [--rewizja HEAD]
Wynik: analiza/wyniki/f_eksport_powtarzalnosc.txt
"""
import argparse
import glob
import json
import os
import subprocess
import sys

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DANE = os.path.join(KATALOG, "narzedzie", "dane_strony")
RAPORT = os.path.join(KATALOG, "analiza", "wyniki", "f_eksport_powtarzalnosc.txt")
METADANE = {"wygenerowano", "commit"}


def ladunki(tekst):
    """Wszystkie przypisania „X=…;” z pliku danych strony jako słownik {cel: obiekt JSON}."""
    wynik = {}
    for linia in tekst.splitlines():
        # pierwsze „={” otwiera dane (np. D.C={…}; albo D.lejek=D.lejek||{};D.lejek["kanal"]={…};)
        poz = linia.find("={")
        if poz < 0:
            continue
        cel = linia[:poz].split(";")[-1]
        cialo = linia[poz + 1:].rstrip().rstrip(";")
        wynik[cel] = json.loads(cialo)
    return wynik


def porownaj(a, b, sciezka, wynik):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                wynik["tresc"].append(f"{sciezka}.{k}: klucz tylko w {'commicie' if k in a else 'pliku na dysku'}")
            else:
                porownaj(a[k], b[k], f"{sciezka}.{k}", wynik)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            wynik["tresc"].append(f"{sciezka}: długość listy {len(a)} → {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            porownaj(x, y, f"{sciezka}[{i}]", wynik)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if a != b:
            wzgl = abs(a - b) / max(abs(a), abs(b), 1e-300)
            (wynik["szum"] if wzgl < 1e-9 else wynik["tresc"]).append(f"{sciezka}: {a!r} → {b!r}")
    elif a != b:
        klucz = sciezka.rsplit(".", 1)[-1]
        (wynik["meta"] if klucz in METADANE else wynik["tresc"]).append(f"{sciezka}: {str(a)[:80]!r} → {str(b)[:80]!r}")


def main():
    sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--rewizja", default="HEAD")
    arg = ap.parse_args()
    linie = [f"F — POWTARZALNOŚĆ EKSPORTU: narzedzie/dane_strony/*.js na dysku wobec commitu {arg.rewizja}", ""]
    suma = {"meta": 0, "szum": 0, "tresc": 0}
    for sciezka in sorted(glob.glob(os.path.join(DANE, "*.js"))):
        nazwa = os.path.basename(sciezka)
        z_gita = subprocess.run(["git", "-C", KATALOG, "show", f"{arg.rewizja}:narzedzie/dane_strony/{nazwa}"],
                                capture_output=True, timeout=60)
        if z_gita.returncode:
            linie.append(f"{nazwa:36} BRAK W COMMICIE")
            suma["tresc"] += 1
            continue
        tekst_git = z_gita.stdout.decode("utf-8")
        with open(sciezka, encoding="utf-8", newline="") as f:
            tekst_dysk = f.read()
        if tekst_git == tekst_dysk:
            linie.append(f"{nazwa:36} identyczny co do bajtu")
            continue
        a, b = ladunki(tekst_git), ladunki(tekst_dysk)
        wynik = {"meta": [], "szum": [], "tresc": []}
        porownaj(a, b, nazwa, wynik)
        for k in suma:
            suma[k] += len(wynik[k])
        linie.append(f"{nazwa:36} metadane {len(wynik['meta'])}, szum zmiennoprzecinkowy {len(wynik['szum'])}, "
                     f"różnice w treści {len(wynik['tresc'])}")
        for rodzaj, opis in (("meta", "metadane"), ("szum", "szum"), ("tresc", "TREŚĆ")):
            for x in wynik[rodzaj][:20]:
                linie.append(f"      {opis}: {x}")
    linie += ["", f"Razem: metadane {suma['meta']}, szum zmiennoprzecinkowy {suma['szum']}, różnice w treści {suma['tresc']}."]
    tekst = "\n".join(linie) + "\n"
    os.makedirs(os.path.dirname(RAPORT), exist_ok=True)
    with open(RAPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write(tekst)
    print(tekst)


if __name__ == "__main__":
    main()
