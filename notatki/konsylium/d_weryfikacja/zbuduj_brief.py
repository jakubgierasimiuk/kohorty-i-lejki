"""Składa brief końcowej rundy konsylium (punkt D) z nagłówka i załączników A–E.

Uruchomienie z głównego folderu projektu:
    python -I notatki/konsylium/d_weryfikacja/zbuduj_brief.py
Wynik: notatki/konsylium/d_weryfikacja/brief.md

Załączniki: A — treść zadania (CLAUDE.md, punkty 2–6), B — README.md, C — teksty zakładek narzędzia
(analiza/wyniki/b_teksty_strony.md), D — ZALOZENIA, ZNALEZISKA, DECYZJE, E — wybrane fragmenty raportów.
Imię prowadzącego pracę zamieniamy na „kandydat” (zasady konsylium: bez danych osobowych); dane są syntetyczne.
"""

import os
import re
import sys

KAT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TU = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(KAT, "analiza", "wyniki")


def czytaj(*p):
    with open(os.path.join(KAT, *p), encoding="utf-8") as f:
        return f.read().replace("\r\n", "\n")


def linie(tekst, od, do=None):
    """Fragment od pierwszej linii zaczynającej się od `od` do linii przed pierwszą zaczynającą się od `do`."""
    ll = tekst.split("\n")
    i = next(k for k, l in enumerate(ll) if l.startswith(od))
    j = next((k for k, l in enumerate(ll) if k > i and do and l.startswith(do)), len(ll))
    return "\n".join(ll[i:j]).rstrip()


ZAMIANY = [(r"\bJakub(a)? Gierasimiuk\w*", "kandydat"), (r"\bKuby\b", "kandydata"), (r"\bKubie\b", "kandydatowi"),
           (r"\bKubę\b", "kandydata"), (r"\bKubą\b", "kandydatem"), (r"\bKuba\b", "kandydat"),
           (r"[\w.]+@telemedi\.com", "[adres e-mail usunięty]")]


def anonimizuj(t):
    for a, b in ZAMIANY:
        t = re.sub(a, b, t)
    return t


def main():
    sys.stdout.reconfigure(errors="replace")
    czesci = [czytaj("notatki", "konsylium", "d_weryfikacja", "naglowek.md")]

    claude = czytaj("CLAUDE.md")
    czesci.append("# Załącznik A — treść zadania (streszczenie i cytaty z zadania)\n\n" + linie(claude, "## 2.", "## 7."))
    czesci.append("# Załącznik B — README repozytorium\n\n" + czytaj("README.md"))
    czesci.append("# Załącznik C — pełne teksty zakładek narzędzia\n\n" + czytaj("analiza", "wyniki", "b_teksty_strony.md"))
    for plik in ("ZALOZENIA.md", "ZNALEZISKA.md", "DECYZJE.md"):
        czesci.append(f"# Załącznik D — notatki/{plik}\n\n" + czytaj("notatki", plik))

    e = ["# Załącznik E — najważniejsze zestawienia liczb (fragmenty raportów z `analiza/wyniki/`)"]
    t = czytaj("analiza", "wyniki", "c_priorytety.txt")
    e.append("## E1. Odpowiedź „czy to wzrost”: nowi pacjenci, powroty, marża, wynik biznesu, kwartały (c_priorytety.txt, W1–W4)\n\n```\n"
             + linie(t, "C — LICZBY", "P1. SAFARI") + "\n```")
    t = czytaj("analiza", "wyniki", "a5r_kohorty.txt")
    e.append("## E2. Kohorty: powroty, krzywa, marża w miesiącach, kohorty miesięczne, start od zera (a5r_kohorty.txt, sekcje 1–5)\n\n```\n"
             + linie(t, "1. OKRES 1", "6. KOHORTY TYGODNIOWE") + "\n```")
    t = czytaj("analiza", "wyniki", "a5p_lejek.txt")
    e.append("## E3. Lejek: typy sesji, kwartały, podziały, rozkład zmiany konwersji (a5p_lejek.txt, sekcje 1–4)\n\n```\n"
             + linie(t, "1. TYPY SESJI", "2b. To samo") + "\n\n" + linie(t, "3. PODZIAŁY", "3. kampania") + "\n\n"
             + linie(t, "4. ZMIANA KONWERSJI", "5. CZAS MIĘDZY") + "\n```")
    t = czytaj("analiza", "wyniki", "a5p_zdarzenia.txt")
    e.append("## E4. Zdarzenia: lejek i Safari na iOS (a5p_zdarzenia.txt, sekcje 1, 5f, 6)\n\n```\n" + linie(t, "1. ZMIANY", "2. ZMIANY")
             + "\n\n" + linie(t, "5f.", "5g.") + "\n\n" + linie(t, "6. STARTY") + "\n```")
    e.append("## E5. Zdarzenia: retencja i obsługa pacjenta (a5r_zdarzenia.csv)\n\n```\n" + czytaj("analiza", "wyniki", "a5r_zdarzenia.csv") + "\n```")
    t = czytaj("analiza", "wyniki", "a5e_ekonomia.txt")
    e.append("## E6. Ekonomia kampanii: obie reguły źródła, 90 i 180 dni (a5e_ekonomia.txt, sekcje 1–2b)\n\n```\n"
             + linie(t, "1. NAGŁÓWEK", "2c. Pełne okresy").replace("=" * 110 + "\n", "") + "\n```")
    t = czytaj("analiza", "wyniki", "c_telemedigo.txt")
    e.append("## E7. TelemediGO (c_telemedigo.txt, sekcje 0–3; sekcja 4 w skrócie w zakładce „Czy to wzrost”)\n\n```\n"
             + linie(t, "C — TELEMEDIGO", "4. CZY TELEMEDIGO") + "\n```")
    czesci.append("\n\n".join(e))

    brief = anonimizuj("\n\n".join(czesci)) + "\n"
    with open(os.path.join(TU, "brief.md"), "w", encoding="utf-8", newline="\r\n") as f:
        f.write(brief)
    print(f"brief.md: {len(brief.encode('utf-8')):,} bajtów, {len(brief):,} znaków; pozostałe „Kub”: {len(re.findall('Kub[aiyęą]', brief))}")


if __name__ == "__main__":
    main()
