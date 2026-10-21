"""E — teksty strony w nowym kształcie karty (notatki/e_runda.md, punkt 3), runda „merytoryka, język, wygląd”.

Ten moduł ma dwie części:
  1. wspólne narzędzia dla nowych tekstów (używa ich też analiza/e_teksty_zakladki.py): budowa kart i bloków, słownik
     (okres 1 → rok wcześniej itd.), nowe numery niewiadomych po usunięciu dawnej pozycji 13, kontrola liczb;
  2. teksty zakładek „Czy to wzrost”, „Priorytety”, „Czego nie wiemy” i nagłówka lejka (sesja prowadząca).

Zasada liczb bez zmian: żadnej liczby wpisanej ręcznie. Liczby przychodzą z raportów (przez b2_eksport_c.wartosci, V)
i z analiza/wyniki/e_merytoryka.json (E). Kontrola: każda liczba w tekstach karty musi stać we fragmencie notatki
z tekstami (notatki/e_teksty.md albo notatki/e_teksty_zakladki.md, sekcja „### <klucz>”) albo w fragmencie dawnej
notatki (c_szkic.md, d_teksty_strony.md), z której pochodzi przeniesione zdanie.
"""
import json
import os
import re

import b2_eksport_c as B2

KATALOG = B2.KATALOG
WYNIKI = B2.WYNIKI
E_TEKSTY = os.path.join(KATALOG, "notatki", "e_teksty.md")
E_TEKSTY_ZAKLADKI = os.path.join(KATALOG, "notatki", "e_teksty_zakladki.md")

liczba, proc, zn, zl, tz, tzn, t1, ile, zakres = B2.liczba, B2.proc, B2.zn, B2.zl, B2.tz, B2.tzn, B2.t1, B2.ile, B2.zakres


def wczytaj_e():
    with open(os.path.join(WYNIKI, "e_merytoryka.json"), encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- karty i bloki (kontrakt: notatki/e_runda.md, punkt 3)

def karta(tytul, wniosek=None, znacznik=None, tresc=None, zastrzezenie=None, szczegoly=None, linki=None, zrodlo=None,
          **inne):
    k = {"tytul": tytul}
    if znacznik:
        k["znacznik"] = znacznik
    if wniosek:
        k["wniosek"] = wniosek
    if tresc:
        k["tresc"] = tresc
    if zastrzezenie:
        k["zastrzezenie"] = zastrzezenie
    if szczegoly:
        k["szczegoly"] = szczegoly
    if linki:
        k["linki"] = linki
    if zrodlo:
        k["zrodlo"] = zrodlo
    k.update(inne)
    return k


def znacznik(tekst, stan):
    return {"tekst": tekst, "stan": stan}


def akapit(t):
    return {"typ": "akapit", "tekst": t}


def punkty(lista):
    return {"typ": "punkty", "punkty": list(lista)}


def numerowane(lista):
    return {"typ": "numerowane", "punkty": list(lista)}


def podtytul(t):
    return {"typ": "podtytul", "tekst": t}


def tabela(kolumny, wiersze, tytul=None):
    t = {"typ": "tabela", "kolumny": kolumny, "wiersze": wiersze}
    if tytul:
        t["tytul"] = tytul
    return t


def wiersz(opis, komorki, podsuma=False):
    w = {"opis": opis, "komorki": komorki}
    if podsuma:
        w["podsuma"] = True
    return w


def zmiana(tekst, wartosc, lepiej_gdy_rosnie=True, pod=None):
    """Komórka ze zmianą rok do roku: strzałka według znaku, kolor i słowo według tego, czy zmiana jest dobra."""
    kier = "bez" if round(wartosc, 6) == 0 else ("wzrost" if wartosc > 0 else "spadek")
    if kier == "bez":
        stan = "neutralnie"
    else:
        stan = "dobrze" if (wartosc > 0) == lepiej_gdy_rosnie else "zle"
    k = {"tekst": tekst, "zmiana": kier, "stan": stan}
    if pod:
        k["pod"] = pod
    return k


def link(tekst, href):
    return {"tekst": tekst, "href": href}


# ---------------------------------------------------------------- słownik i numery niewiadomych

# Dawna niewiadoma 13 (stawka pediatry) wypada z listy: to założenie z zadania (punkt 10 listy Kuby). Pozycje 14–22
# dostają numery 13–21. Odwołania w tekstach przenumerowuje funkcja przenumeruj().
NIEWIADOMA = {n: (n if n < 13 else n - 1) for n in range(1, 23) if n != 13}


def przenumeruj(t):
    """Odwołania do niewiadomych w przeniesionych zdaniach: „Czego nie wiemy, punkt 19” → „punkt 18”, „niewiadoma 21” → „20”."""
    def zamien(m):
        n = int(m.group(2))
        return m.group(1) + str(NIEWIADOMA.get(n, n))
    t = re.sub(r"(Czego nie wiemy, punkt )(\d+)", zamien, t)
    t = re.sub(r"(niewiadom[aąeiy] )(\d+)", zamien, t)
    return t


# Zamiany słownika (część 2 listy Kuby): „okres 1/2” → „rok wcześniej / ostatnie 12 miesięcy”. Kolejność ma znaczenie.
SLOWNIK = [
    (r"\bw okresie X 2024 – IX 2025\b", "rok wcześniej (X 2024 – IX 2025)"),
    (r"\bw okresie X 2025 – IX 2026\b", "w ostatnich 12 miesiącach (X 2025 – IX 2026)"),
    (r"\bOkres X 2024 – IX 2025\b", "Rok wcześniej (X 2024 – IX 2025)"),
    (r"\bOkres X 2025 – IX 2026\b", "Ostatnie 12 miesięcy (X 2025 – IX 2026)"),
    (r"\bw okresie 1\b", "rok wcześniej"),
    (r"\bw okresie 2\b", "w ostatnich 12 miesiącach"),
    (r"\bz okresu 1\b", "sprzed roku"),
    (r"\bz okresu 2\b", "z ostatnich 12 miesięcy"),
    (r"\bokresu 1\b", "roku wcześniej"),
    (r"\bokresu 2\b", "ostatnich 12 miesięcy"),
    (r"\bOkres 1\b", "Rok wcześniej"),
    (r"\bOkres 2\b", "Ostatnie 12 miesięcy"),
    (r"\bokres 1\b", "rok wcześniej"),
    (r"\bokres 2\b", "ostatnie 12 miesięcy"),
]


def slownik(t):
    for a, b in SLOWNIK:
        t = re.sub(a, b, t)
    return przenumeruj(t)


def popraw(obj):
    """Słownik i numery niewiadomych we wszystkich napisach struktury (bez odnośników i pól technicznych)."""
    if isinstance(obj, str):
        return slownik(obj)
    if isinstance(obj, list):
        return [popraw(x) for x in obj]
    if isinstance(obj, dict):
        return {k: (v if k in ("href", "zrodlo", "id", "poziom", "stan", "zmiana", "typ") else popraw(v)) for k, v in obj.items()}
    return obj


# ---------------------------------------------------------------- kontrola liczb

POMIJANE = ("linki", "zrodlo", "href", "_dodane", "_fragmenty", "nr", "id", "poziom", "stan", "zmiana", "typ", "wstaw")


def napisy(obj):
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        out = []
        for k, v in obj.items():
            if k in POMIJANE:
                continue
            out += napisy(v)
        return out
    if isinstance(obj, list):
        out = []
        for v in obj:
            out += napisy(v)
        return out
    return []


def fragmenty_notatki(sciezka):
    if not os.path.exists(sciezka):
        return {}
    with open(sciezka, encoding="utf-8") as f:
        s = f.read().replace("\r\n", "\n")
    return {m.group(1).strip(): m.group(0) for m in re.finditer(r"^### (.+?)$.*?(?=^### |^## |\Z)", s, re.M | re.S)}


def _stare():
    out = {f"c:{k}": v for k, v in B2.szkic_fragmenty().items()}
    with open(B2.D_TEKSTY, encoding="utf-8") as f:
        s = f.read().replace("\r\n", "\n")
    for m in re.finditer(r"^### (.+?)$.*?(?=^### |^## |\Z)", s, re.M | re.S):
        out["d:" + m.group(1).strip()] = m.group(0)
    return out


def kontrola(bloki, notatka=E_TEKSTY, prefiks="e"):
    """bloki: lista (nazwa, obiekt, [dodatkowe fragmenty, np. 'c:pozycja:3' albo 'd:<nagłówek>'], [liczby dodane]).
    Fragment własny to sekcja „### nazwa” w notatce. Zwraca listę (nazwa, liczb, bez pokrycia, użyte dodane)."""
    fr = fragmenty_notatki(notatka)
    stare = _stare()
    wynik = []
    for nazwa, obj, dodatkowe, dodane in bloki:
        wzor = fr.get(nazwa, "")
        for d in dodatkowe:
            if d.startswith("d:"):
                klucz = next((h for h in stare if h.startswith(d)), None)
                wzor += stare.get(klucz, "") if klucz else ""
            else:
                wzor += stare.get(d, "")
        if not wzor:
            wynik.append((f"{prefiks}:{nazwa[:22]}", 0, ["brak fragmentu w notatce"], []))
            continue
        w, dod = set(B2.tokeny(wzor)), set(B2.tokeny(" | ".join(dodane)))
        tk = [x for t in napisy(obj) for x in B2.tokeny(t)]
        wynik.append((f"{prefiks}:{nazwa[:22]}", len(tk), sorted({x for x in tk if x not in w and x not in dod}),
                      sorted({x for x in tk if x not in w and x in dod})))
    return wynik


# ---------------------------------------------------------------- teksty sesji prowadzącej (wypełniane w części 2)

def teksty_c(V, E, C):
    """Nowe „Czy to wzrost”, „Priorytety” i „Czego nie wiemy”. C = dane w dotychczasowym kształcie (z b2_eksport_c).
    Zwraca (C w nowym kształcie, bloki do kontroli)."""
    return C, []


def karty_lejka(nag, V, E):
    """Karty nagłówka lejka (D.P.lejek_naglowek.karta, .naprawy_karty, .osobne_karta). Zwraca bloki do kontroli."""
    return []
