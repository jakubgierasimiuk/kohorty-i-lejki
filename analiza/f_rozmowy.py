"""F: oczyszczony zapis rozmów z Claude Code (`rozmowy/`) i lekcje z pamięci projektu (`notatki/lekcje.md`).

Źródło: pliki rozmów tego projektu, które Claude Code zapisuje lokalnie (jeden plik JSONL na sesję; folder domyślnie
wyliczany z położenia repozytorium). Podfolderów (rozmowy agentów pomocniczych, wyniki narzędzi) skrypt nie czyta.
Pamięć projektu: podfolder `memory` tego samego folderu.

Lista dozwolona — z rozmów bierzemy wyłącznie:
1. wiadomości wpisane przez Kubę (wpisy `user` od człowieka, bloki tekstu, bez `isMeta`, bez bloków <system-reminder>);
2. tekstowe odpowiedzi Claude (wpisy `assistant`, bloki `text`);
3. treść poleceń i wiadomości wysłanych innym sesjom i agentom (tylko pola z treścią w wywołaniach, które je
   uruchamiają albo wysyłają im wiadomości).
Nie bierzemy niczego innego: wpisów `attachment` (instrukcje, pamięć, lista usług i umiejętności, środowisko),
pozostałych wywołań narzędzi i ich wyników, powiadomień automatycznych, raportów agentów i sesji potomnych.

Z zachowanego tekstu usuwamy, zostawiając oznaczenie: adresy stron, adresy e-mail, ścieżki spoza folderu projektu,
nazwy innych projektów (lista spoza repozytorium, `--nazwy`), ciągi wyglądające na klucze oraz fragmenty, które
pokrywają się z tekstem zadania na 8 słów z rzędu albo więcej (tekst zadania spoza repozytorium, `--zadanie`).
Potem skrypt skanuje cały wynik (rozmowy, lekcje, README repozytorium). Raport z kontekstem trafień zapisuje poza
repozytorium (`--raport`), a na ekran wypisuje tylko liczby.

Użycie (z głównego folderu repozytorium):
    python -I analiza/f_rozmowy.py --zadanie <plik> --nazwy <plik> --raport <plik>
Pliki z argumentów muszą leżeć poza repozytorium.
"""
import argparse
import collections
import datetime as dt
import json
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

KORZEN = Path(__file__).resolve().parent.parent
STREFA = ZoneInfo("Europe/Warsaw")
WYJ_ROZMOWY = KORZEN / "rozmowy"
WYJ_LEKCJE = KORZEN / "notatki" / "lekcje.md"
N_SLOW = 8  # tyle słów z rzędu wspólnych z tekstem zadania wystarcza do usunięcia fragmentu
DLUGA_WIADOMOSC = 3000

OZN = {
    "url": "[adres strony usunięty]",
    "email": "[adres e-mail usunięty]",
    "sciezka": "[ścieżka spoza projektu usunięta]",
    "projekt": "[nazwa innego projektu usunięta]",
    "usluga": "[nazwa rozszerzenia spoza projektu usunięta]",
    "klucz": "[ciąg wyglądający na klucz usunięty]",
    "zadanie": "[fragment tekstu zadania usunięty]",
}
OPIS_OZN = {
    "url": "adresy stron, w tym link do strony z zadaniem i do paczki danych",
    "email": "adresy e-mail",
    "sciezka": "ścieżki do plików i folderów poza folderem projektu",
    "projekt": "nazwy innych projektów Kuby",
    "usluga": "nazwy rozszerzeń aplikacji używanych poza tym projektem",
    "klucz": "ciągi wyglądające na klucz albo hasło",
    "zadanie": f"{N_SLOW} i więcej słów z rzędu wspólnych z tekstem zadania",
}
KATEGORIE = ("url", "email", "sciezka", "projekt", "usluga", "zadanie", "klucz")
# Zostają celowo: nazwy usług claude.ai i Booking.com (nazwy łączników, wymienione też w CLAUDE.md, bez adresu strony)
# i lokalne adresy podglądu strony (127.0.0.1, localhost), które nie prowadzą do żadnej strony w internecie.
DOZWOLONE_DOMENY = {"claude.ai", "booking.com"}
RE_LOKALNY = re.compile(r"(?i)https?://(?:127\.0\.0\.1|localhost)(?::\d+)?(?:/[^\s<>\"'`]*)?")

LIT = "0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźżÀ-ÖØ-öø-ÿ"
RE_SR = re.compile(r"<system-reminder>.*?(?:</system-reminder>|\Z)", re.S)
RE_WKLEJKA = re.compile(r'<pasted_content id="[^"]*">\n?(.*?)(?:\n?</pasted_content id="[^"]*">|\Z)', re.S)
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}\b")
RE_URL = re.compile(r"(?i)\b(?:https?|ftp|file)://[^\s<>\"'`]+|\bwww\.[^\s<>\"'`]+")
RE_DOMENA = re.compile(
    rf"(?i)(?<![{LIT}@./\\_-])(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
    r"(?:com\.pl|co\.uk|com|pl|ai|io|org|net|dev|eu|info|gov|edu|xyz)"
    rf"(?![{LIT}_-])(?:/[^\s<>\"'`]*)?"
)
RE_KLUCZ = re.compile(
    r"sk-or-v1-[A-Za-z0-9]{16,}|sk-ant-[A-Za-z0-9_-]{16,}|sk-(?:proj-)?[A-Za-z0-9_-]{32,}"
    r"|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}"
    r"|xox[abprs]-[A-Za-z0-9-]{10,}|eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|(?i:(?:api[_-]?key|secret|password|passwd|hasło|haslo|token)\s*[:=]\s*[\"']?[A-Za-z0-9_\-./+]{12,})"
)
RE_SCIEZKA_START = re.compile(
    rf"(?<![{LIT}_\\/.~%$:-])"
    r"(?:[A-Za-z]:(?:\\\\|\\|/)"
    r"|/[A-Za-z]/(?=Users|users|Program|Windows|ProgramData|tmp)"
    r"|/(?:tmp|home|Users|usr|etc|var|opt|private|Library)/"
    r"|~[\\/]"
    r"|%[A-Za-z_]+%"
    r"|\$(?:HOME|env:[A-Za-z_]+)"
    r"|(?:AppData|Downloads|Desktop|Documents|OneDrive)[\\/])"
)
ZNAK_SCIEZKI = r"[^\s\"'`<>|*?\])„”]"
RE_SCIEZKA_DALEJ = re.compile(ZNAK_SCIEZKI + "*")
RE_SCIEZKA_SPACJA = re.compile(r"(?: [^\s\"'`<>|*?\])„”\\/]+){1,2}[\\/]" + ZNAK_SCIEZKI + "*")
RE_SLOWO = re.compile(r"[^\W_]+")

# Miejsca do przejrzenia przez Kubę: czy wiadomość nie dotyczy samej rekrutacji (osoby, adresy, warunki).
REKRUTACJA = [
    ("rekrutacja (poza „zadanie rekrutacyjne”)", r"rekrut(?!acyjn)\w*"),
    ("osoba rekrutująca", r"rekrutując\w*|rekruter\w*"),
    ("osoba (Pan, Pani)", r"\b(?:Pan|Pani|Panem|Panią|Pana|Panu)\s+[A-ZŁŚŻŹĆŃÓ][a-ząćęłńóśźż]+"),
    ("mail i wysyłka", r"\bmail\w*|\bwysyłk\w*|\bwysła\w*\s+(?:mail|odpowied|rozwiąz|link)"),
    ("warunki zatrudnienia", r"wynagrodz\w*|pensj\w*|zarob\w*|umow[aęy]\b|\betat\w*|\bB2B\b|ofert\w*\s+prac\w*"),
    ("rozmowa kwalifikacyjna", r"rozmow\w*\s+(?:kwalifikac|rekrutac|o\s+prac|z\s+Telemedi)\w*"),
    ("kontakt", r"\bHR\b|\bCV\b|linkedin\w*|numer\w*\s+telefon\w*|\btel\.\s?\d|\+48\s?\d|\b\d{3}[ -]\d{3}[ -]\d{3}\b"),
    ("Telemedi jako adresat", r"(?:do|od|z|w)\s+Telemedi\b(?!GO)"),
]

GRUPY_LEKCJI = [
    ("Współpraca z Kubą", ["analiza-wspolnie-z-kuba", "definicje-podstawa-w-zadaniu",
                           "watpliwosc-kuby-najpierw-policz", "polecenia-kuby-jako-wklejka"]),
    ("Wnioski: co wolno napisać", ["kontrola-ma-rozrozniac-hipotezy", "streszczenie-nie-wzmacnia-wnioskow",
                                   "zdanie-wyjasnia-wymaga-rachunku", "struktura-nie-chowa-naprawy"]),
    ("Pułapki w kodzie analizy", ["odsetki-puste-wypadaja-z-mianownika", "date-diff-liczy-granice",
                                  "kolejnosc-przed-rankingiem"]),
    ("Teksty strony i kontrola liczb", ["narzedzie-liczby-z-danych", "wzorzec-kontroli-nie-z-kodu",
                                        "strona-bez-wewnetrznych-pojec", "odmiana-liczebnikow-w-tekstach",
                                        "zamiana-slowa-kolizja-znaczen"]),
    ("Drugi model i konsylium", ["recenzja-codeksa-przed-zamknieciem", "konsylium-duzy-brief-puste-odpowiedzi"]),
    ("Praca w kilku sesjach naraz", ["sesje-w-glownym-folderze", "numery-wpisow-przy-rownoleglych-sesjach",
                                     "scalanie-propozycji-skryptem", "wlasny-identyfikator-sesji",
                                     "zlecenie-zmienia-sie-w-trakcie"]),
    ("Narzędzia i środowisko pracy", ["heredoc-polskie-cudzyslowy", "konce-wierszy-sprawdzaj-pythonem",
                                      "zrzuty-strony-playwright-edge", "laczniki-wylaczanie"]),
]

# Wpis o wyłączaniu łączników przycięty do ogólnej lekcji: bez nazw usług i rozszerzeń spoza projektu.
PRZYCIETE = {
    "laczniki-wylaczanie": (
        "Łączniki claude.ai wyłącza się narzędziem `set_session_connector_enabled` (enabled=false), po sprawdzeniu "
        "`session_connectors_status` (tylko wiersze kind „connector”). Na tym projekcie 2026-10-19 wyszły trzy pułapki:\n"
        "- Wyłączenie zapisuje się też jako ustawienie domyślne dla nowych sesji. W innych projektach Kuba musi włączyć "
        "łączniki z powrotem (menu „+” w polu wiadomości → Connectors).\n"
        "- Cztery łączniki po wyłączeniu dalej miały status „connected”. Drugie wywołanie odpowiadało „already disabled; "
        "nothing changed”. Ich narzędzia zniknęły z sesji dopiero następnego dnia.\n"
        "- Serwerów spoza claude.ai (rozszerzeń aplikacji i serwerów dopisanych w konfiguracji) z sesji wyłączyć się "
        "nie da — można ich tylko nie używać.\n\n"
        "**Why:** CLAUDE.md wymaga odcięcia od usług na starcie każdej sesji. Bez sprawdzenia statusu po wyłączeniu "
        "sesja raportuje Kubie „wyłączone”, choć narzędzia dalej są dostępne.\n\n"
        "**How to apply:** po wyłączeniu sprawdź status jeszcze raz. Jeśli coś dalej jest „connected”, napisz Kubie "
        "jednym zdaniem, żeby wyłączył to ręcznie, i nie używaj tych narzędzi. Przy pierwszym wyłączeniu uprzedź Kubę "
        "o skutku dla nowych sesji."
    ),
}

# Historie z sekcji README „Jak pracowaliśmy z AI”: gdzie w zapisie rozmów się dzieją.
# Każde miejsce: (fragment tytułu rozmowy, autor, fraza z tekstu wiadomości, opis miejsca). Numer wiadomości
# skrypt znajduje sam, więc odnośniki zostają poprawne po ponownym uruchomieniu.
HISTORIE = [
    ("1. Pierwszy plan pracy", [
        ("Pierwsza sesja projektu", "Claude", "Odtwarzam cztery liczby z dashboardu", "pierwszy plan Claude"),
        ("Pierwsza sesja projektu", "Kuba", "Nie zatwierdzam jeszcze", "Kuba odrzuca plan i mówi, jak ma wyglądać praca"),
    ]),
    ("2. Zdania mocniejsze niż dane", [
        ("prowadzenie planu analizy", "Claude", "To pasuje do sezonu infekcji", "Claude: wzrost „pasuje do sezonu infekcji”"),
        ("prowadzenie planu analizy", "Kuba", "to sezon infekcji", "poprawka Kuby: w tych samych miesiącach rosną wydatki"),
        ("prowadzenie planu analizy", "Kuba", "to na razie hipoteza, nie wniosek", "druga poprawka Kuby: spadek powrotu w Mecie"),
    ]),
    ("3. Kontrola Codeksa a hipoteza Kuby", [
        ("A5: retencja", "Claude", "Wycofuję zdanie", "Claude wycofuje powiązanie po kontroli Codeksa"),
        ("A5: retencja", "Kuba", "lekarza nie obchodzi", "Kuba odczytuje kontrolę inaczej"),
        ("A5: retencja", "Claude", "26,4 punktu procentowego więcej", "wynik porównania, które rozdziela oba odczytania"),
    ]),
    ("4. Błędy w kodzie, które złapał drugi model", [
        ("A5: pozyskanie", "Claude", "14,3% zamiast 2,6%", "zawyżony odsetek zamówień po wejściach z newslettera i SMS-ów"),
        ("A5: retencja", "Claude", "przesunęła się z 17.11 na 24.11.2025", "opóźnienia wizyt po poprawce liczenia czasu"),
    ]),
    ("5. Safari: awaria schowana pod „zmianą ruchu”", [
        ("A5: pozyskanie", "Claude", "bo zmienił się ruch, a nie dlatego", "pierwszy nagłówek części o lejku"),
        ("A5: pozyskanie", "Kuba", "żeby nie gubił dwóch rzeczy", "Kuba odrzuca nagłówek"),
        ("E: nowy wygląd", "Kuba", "gryzie się z Safari", "trzecia lista Kuby"),
        ("E: nowy wygląd", "Claude", "Safari na iPhone'ach płaci w 8,3% sesji", "wynik przeliczenia według pierwszego wejścia"),
    ]),
    ("6. Spadek marży w III kwartale, który zależał od jednego zdarzenia", [
        ("Sesja prowadząca: punkt C", "Kuba", "w VII–IX 2026 marża jest niższa", "Kuba: marża w III kwartale ma zamknąć odpowiedź"),
        ("Merytoryka narzędzia", "Kuba", "budzi moją wątpliwość", "Kuba podważa to zdanie"),
        ("Merytoryka narzędzia", "Claude", "Spadek marży o 6,8% nie jest pewny", "wynik rachunku"),
    ]),
    ("7. Kwota awarii Safari a spadek marży: zdania bez rachunku", [
        ("Sesja prowadząca: punkt C", "Kuba", "więc Safari się w niej nie mieści", "Kuba odejmuje liczby z syntezy konsylium"),
        ("D: poprawki po konsylium", "Claude", "Safari się w luce nie mieści", "rozkład spadku policzony kodem"),
        ("D: poprawki po konsylium", "Kuba", "o jaką lukę chodzi", "Kuba: czytelnik z Telemedi nie wie, o jaką lukę chodzi"),
        ("D: poprawki po konsylium", "Kuba", "też to przeredaguj", "to samo w „Wyniku biznesu”"),
    ]),
    ("8. Recenzja Codeksa po konsylium: błąd jednostki i reguła bez uzasadnienia", [
        ("D: poprawki po konsylium", "Claude", "większej oczekiwanej marży", "pierwotne uzasadnienie reguły testu Mety"),
        ("D: poprawki po konsylium", "Claude", "Uwzględniłem recenzję Codeksa", "wynik recenzji: 34 z 35 liczb zgodnych"),
    ]),
    ("9. „Najpierw napraw, potem wyłączaj” a wstrzymanie dwóch kampanii", [
        ("Pierwsza sesja projektu", "Claude", "nową stałą zasadę", "zasada zapisana w CLAUDE.md"),
        ("Sesja prowadząca: punkt C", "Claude", "Naprawa zwrotów doprowadza wynik tej kampanii najwyżej do", "TikTok: policzone obie drogi"),
        ("Sesja prowadząca: punkt C", "Claude", "odwracalna pauza", "pauza zamiast „pewnej straty”"),
        ("Sesja prowadząca: punkt C", "Kuba", "potem pauzy, które da się cofnąć", "kolejność listy według Kuby"),
    ]),
    ("10. Kontrole, które same się myliły", [
        ("Merytoryka narzędzia", "Claude", "niczego nie sprawdzała", "szkic do kontroli liczb generowany ze strony"),
        ("E: nowy wygląd", "Claude", "Liczby wpisane ręcznie w kodzie tekstów", "liczby wpisane ręcznie w kod i w szkic naraz"),
        ("Ostatnia kontrola", "Claude →", "wadliwe od wysokości strony 16 384", "zrzut ekranu, który się urywał"),
    ]),
]


# ---------------------------------------------------------------- wczytanie

def argumenty():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    domyslne = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(KORZEN))
    p.add_argument("--zrodlo", type=Path, default=domyslne, help="folder z plikami rozmów (*.jsonl)")
    p.add_argument("--pamiec", type=Path, default=None, help="folder pamięci projektu (domyślnie <zrodlo>/memory)")
    p.add_argument("--zadanie", type=Path, required=True, help="tekst zadania, tylko do porównania (poza repozytorium)")
    p.add_argument("--nazwy", type=Path, required=True, help="lista nazw spoza projektu (poza repozytorium)")
    p.add_argument("--raport", type=Path, required=True, help="raport z kontekstem trafień (poza repozytorium)")
    a = p.parse_args()
    for nazwa in ("zadanie", "nazwy", "raport"):
        sciezka = getattr(a, nazwa).resolve()
        if sciezka == KORZEN or KORZEN in sciezka.parents:
            sys.exit(f"Plik --{nazwa} musi leżeć poza repozytorium: {sciezka}")
    if a.pamiec is None:
        a.pamiec = a.zrodlo / "memory"
    return a


def wczytaj_nazwy(p):
    listy = {"usun": [], "usluga": [], "sprawdz": []}
    for linia in p.read_text(encoding="utf-8").splitlines():
        linia = linia.strip()
        if not linia or linia.startswith("#"):
            continue
        rodzaj, _, wzor = linia.partition(":")
        if rodzaj.strip() in listy:
            listy[rodzaj.strip()].append(wzor.strip())

    def kompiluj(lista):
        return [(w, re.compile(rf"(?i)(?<![{LIT}_])(?:{w})(?![{LIT}_])")) for w in lista]
    return kompiluj(listy["usun"]), kompiluj(listy["usluga"]), kompiluj(listy["sprawdz"])


def slowa(t):
    return [(m.group(0).lower(), m.start(), m.end()) for m in RE_SLOWO.finditer(t)]


def ngramy_zadania(p):
    s = [w for w, _, _ in slowa(p.read_text(encoding="utf-8"))]
    return {tuple(s[i:i + N_SLOW]) for i in range(len(s) - N_SLOW + 1)}


def wczytaj_jsonl(p):
    wpisy = []
    with open(p, encoding="utf-8", errors="replace") as f:
        for i, linia in enumerate(f):
            try:
                w = json.loads(linia)
            except json.JSONDecodeError:
                continue
            if isinstance(w, dict):
                w["_plik"], w["_linia"] = p.stem, i
                wpisy.append(w)
    return wpisy


def czas_pl(znacznik):
    return dt.datetime.fromisoformat(znacznik.replace("Z", "+00:00")).astimezone(STREFA)


def norm(t):
    t = re.sub(r"[„”“\"'’‘`]", "", t or "")
    return re.sub(r"\s+", " ", t).strip().lower()


# ---------------------------------------------------------------- czyszczenie tekstu

def dozwolony(kat, fragment):
    if kat != "url":
        return False
    szablon = "<" in fragment or "&lt;" in fragment  # np. https://<organizacja>.github.io/<repozytorium>/
    return szablon or bool(RE_LOKALNY.fullmatch(fragment)) or fragment.lower() in DOZWOLONE_DOMENY


class Czyszczenie:
    def __init__(self, ngramy, usun, uslugi, korzen):
        self.ngramy = ngramy
        self.usun = usun
        self.uslugi = uslugi
        self.korzenie = self._warianty_korzenia(korzen)
        self.usuniete = []  # (kategoria, oryginał, kontekst, miejsce)
        self.zostawione = collections.Counter()  # celowo zostawione nazwy usług i lokalne adresy

    @staticmethod
    def _warianty_korzenia(k):
        s = str(k)
        w = {s, s.replace("\\", "/"), s.replace("\\", "\\\\")}
        m = re.match(r"([A-Za-z]):\\(.*)", s)
        if m:
            reszta = m.group(2).replace("\\", "/")
            w |= {f"/{m.group(1).lower()}/{reszta}", f"/{m.group(1).upper()}/{reszta}"}
        try:
            wzgl = str(k.relative_to(Path.home()))
            w |= {wzgl, wzgl.replace("\\", "/")}
        except ValueError:
            pass
        return sorted({x.lower() for x in w}, key=len, reverse=True)

    def _zapisz(self, kat, tekst, a, b, miejsce):
        self.usuniete.append((kat, tekst[a:b], tekst[max(0, a - 70):a] + "⟦" + tekst[a:b] + "⟧" + tekst[b:b + 70], miejsce))

    def _zamien_wzorcem(self, tekst, wzor, kat, miejsce):
        wyj, poz = [], 0
        for m in wzor.finditer(tekst):
            a, b = m.start(), m.end()
            if kat == "url":
                while b > a and tekst[b - 1] in ".,;:!?)]}”’\"'*_":
                    b -= 1
            if dozwolony(kat, tekst[a:b]):
                self.zostawione[tekst[a:b].lower()] += 1
                continue
            self._zapisz(kat, tekst, a, b, miejsce)
            wyj.append(tekst[poz:a])
            wyj.append(OZN[kat])
            poz = b
        wyj.append(tekst[poz:])
        return "".join(wyj)

    def sciezki(self, tekst, miejsce=None, tylko_znajdz=False):
        wyj, poz, i, traf = [], 0, 0, []
        while True:
            m = RE_SCIEZKA_START.search(tekst, i)
            if not m:
                break
            a = m.start()
            dalej = tekst[a:].lower()
            korzen = next((k for k in self.korzenie if dalej.startswith(k)), None)
            if korzen:
                i = a + len(korzen)
                continue
            b = RE_SCIEZKA_DALEJ.match(tekst, m.end()).end()
            while True:
                s = RE_SCIEZKA_SPACJA.match(tekst, b)
                if not s:
                    break
                b = s.end()
            while b > a and tekst[b - 1] in ".,;:!?)]}":
                b -= 1
            if b - a < 3:
                i = m.end()
                continue
            traf.append((a, b))
            if not tylko_znajdz:
                self._zapisz("sciezka", tekst, a, b, miejsce)
                wyj.append(tekst[poz:a])
                wyj.append(OZN["sciezka"])
                poz = b
            i = b
        if tylko_znajdz:
            return traf
        wyj.append(tekst[poz:])
        return "".join(wyj)

    def zadanie(self, tekst, miejsce=None, tylko_znajdz=False):
        s = slowa(tekst)
        pokryte = [False] * len(s)
        for i in range(len(s) - N_SLOW + 1):
            if tuple(w for w, _, _ in s[i:i + N_SLOW]) in self.ngramy:
                for j in range(i, i + N_SLOW):
                    pokryte[j] = True
        odcinki, i = [], 0
        while i < len(s):
            if pokryte[i]:
                j = i
                while j + 1 < len(s) and pokryte[j + 1]:
                    j += 1
                odcinki.append((s[i][1], s[j][2]))
                i = j + 1
            else:
                i += 1
        if tylko_znajdz:
            return odcinki
        wyj, poz = [], 0
        for a, b in odcinki:
            self._zapisz("zadanie", tekst, a, b, miejsce)
            wyj.append(tekst[poz:a])
            wyj.append(OZN["zadanie"])
            poz = b
        wyj.append(tekst[poz:])
        return "".join(wyj)

    def __call__(self, tekst, miejsce):
        tekst = self._zamien_wzorcem(tekst, RE_KLUCZ, "klucz", miejsce)
        tekst = self._zamien_wzorcem(tekst, RE_URL, "url", miejsce)
        tekst = self._zamien_wzorcem(tekst, RE_EMAIL, "email", miejsce)
        tekst = self._zamien_wzorcem(tekst, RE_DOMENA, "url", miejsce)
        tekst = self.sciezki(tekst, miejsce)
        for _, wzor in self.usun:
            tekst = self._zamien_wzorcem(tekst, wzor, "projekt", miejsce)
        for _, wzor in self.uslugi:
            tekst = self._zamien_wzorcem(tekst, wzor, "usluga", miejsce)
        tekst = self.zadanie(tekst, miejsce)
        return tekst


# ---------------------------------------------------------------- Markdown

MAPA_SESJI = {}  # identyfikator sesji w aplikacji -> plik rozmowy (do odnośników „#local_…” w tekstach)
RE_LINK = re.compile(r"\]\((<[^>\n]+>|[^)\s]+)\)")


def popraw_cel(cel):
    """Odnośnik z tekstu rozmowy tak, żeby działał z folderu rozmowy/: pliki projektu względem głównego folderu,
    numery linii jako #L, sesje aplikacji jako pliki rozmów. Odnośników, których nie rozpoznajemy, nie zmieniamy."""
    nawias = cel.startswith("<") and cel.endswith(">")
    c = cel[1:-1] if nawias else cel
    m = re.fullmatch(r"#(local_[0-9a-f-]{36})", c)
    if m:
        return MAPA_SESJI.get(m.group(1), cel)
    if c.startswith(("#", "../", "[")) or (re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", c) and not re.match(r"[A-Za-z]:[\\/]", c)):
        return cel
    sciezka = c.replace("\\", "/")
    korzen = str(KORZEN).replace("\\", "/")
    warianty = [korzen, "/" + korzen]
    if re.match(r"[A-Za-z]:/", korzen):
        warianty.append(f"/{korzen[0].lower()}{korzen[2:]}")
    for k in warianty:
        if sciezka.lower().startswith(k.lower() + "/"):
            sciezka = sciezka[len(k) + 1:]
            break
    sciezka, _, kotwica = sciezka.partition("#")
    kotwica = "#" + kotwica if kotwica else ""
    m = re.fullmatch(r"(.+?):(\d+)(?:-(\d+))?", sciezka)
    if m and not (KORZEN / sciezka).exists():
        sciezka = m.group(1)
        kotwica = f"#L{m.group(2)}" + (f"-L{m.group(3)}" if m.group(3) else "")
    if not sciezka or not (KORZEN / sciezka).exists():
        return cel
    wynik = sciezka[len("rozmowy/"):] if sciezka.startswith("rozmowy/") else "../" + sciezka
    wynik += kotwica
    return f"<{wynik}>" if " " in wynik else wynik


def popraw_linki(tekst):
    return RE_LINK.sub(lambda m: "](" + popraw_cel(m.group(1)) + ")", tekst)


def formatuj(tekst):
    """Nagłówki w treści o trzy poziomy niżej (nagłówkami są numery wiadomości), znaczniki HTML jako zwykły tekst,
    odnośniki poprawione tak, żeby działały z folderu rozmowy/, domknięcie niedomkniętego bloku kodu.
    Słowa się nie zmieniają."""
    wyj, kod = [], None
    for linia in tekst.split("\n"):
        s = linia.lstrip()
        p = re.match(r"(`{3,}|~{3,})", s)
        if kod is None:
            if p:
                kod = p.group(1)
                wyj.append(linia)
                continue
            linia = re.sub(r"^(\s{0,3})(#{1,6})(?=\s)", lambda m: m.group(1) + "#" * min(6, len(m.group(2)) + 3), linia)
            czesci = re.split(r"(`+[^`]*`+)", linia)
            linia = "".join(c if c.startswith("`") else re.sub(r"(?<!\]\()<(?=[A-Za-z/!?])", "&lt;", popraw_linki(c))
                            for c in czesci)
            wyj.append(linia)
        else:
            wyj.append(linia)
            if p and p.group(1)[0] == kod[0] and len(p.group(1)) >= len(kod) and not s[len(p.group(1)):].strip():
                kod = None
    if kod is not None:
        wyj.append(kod)
    return "\n".join(wyj)


def cytat(tekst):
    return "\n".join("> " + l if l.strip() else ">" for l in tekst.split("\n"))


def wiadomosc_kuby(tekst):
    """Wklejone bloki jako cytat z podpisem; reszta bez zmian."""
    czesci, poz = [], 0
    for m in RE_WKLEJKA.finditer(tekst):
        przed = tekst[poz:m.start()].strip()
        if przed:
            czesci.append(formatuj(przed))
        czesci.append("*Wklejony tekst:*\n\n" + cytat(formatuj(m.group(1).strip())))
        poz = m.end()
    reszta = tekst[poz:].strip()
    if reszta:
        czesci.append(formatuj(reszta))
    return "\n\n".join(czesci)


def nazwa_pliku(data, tytul):
    t = tytul.translate(str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ"))
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()[:60].strip("-")
    return f"{data}_{t}.md"


# ---------------------------------------------------------------- rozmowy

def rodziny_plikow(dane):
    """Pliki, które dzielą wpisy o tych samych identyfikatorach, to jedna rozmowa zapisana kilka razy
    (wznowienie albo rozwidlenie). Wspólną część pokazujemy raz."""
    rodzic = {s: s for s in dane}

    def znajdz(x):
        while rodzic[x] != x:
            rodzic[x] = rodzic[rodzic[x]]
            x = rodzic[x]
        return x

    pierwszy = {}
    for s, wpisy in dane.items():
        for w in wpisy:
            u = w.get("uuid")
            if not u:
                continue
            if u in pierwszy:
                rodzic[znajdz(s)] = znajdz(pierwszy[u])
            else:
                pierwszy[u] = s
    grupy = collections.defaultdict(list)
    for s in dane:
        grupy[znajdz(s)].append(s)
    return list(grupy.values())


def teksty_bloku(tresc):
    if isinstance(tresc, str):
        return [tresc]
    return [b.get("text", "") for b in (tresc or []) if isinstance(b, dict) and b.get("type") == "text"]


def tekst_wyniku(b):
    c = b.get("content")
    if isinstance(c, str):
        return c
    return " ".join(x.get("text", "") for x in (c or []) if isinstance(x, dict))


RE_START = re.compile(r'Started session "(.+?)" \(session_id: (local_[0-9a-f-]{36})')
RE_PROPOZYCJA = re.compile(r'(?:Proposed|opening for) "(.+?)" \(task_id: (task_\w+)\)')
RE_OD_SESJI = re.compile(r'<cross-session-message from="(local_[0-9a-f-]{36})" name="([^"]*)">\n?(.*?)(?:</cross-session-message>|\Z)', re.S)


def metadane(dane):
    """Tytuły sesji po identyfikatorach aplikacji (z wyników uruchomienia sesji i z opakowań wiadomości).
    Wyników narzędzi nie przepisujemy — służą tylko do podpisów i odnośników."""
    tytul_id, tytul_propozycji = {}, {}
    wywolania = {}
    for wpisy in dane.values():
        for w in wpisy:
            if w.get("type") == "assistant":
                for b in (w.get("message") or {}).get("content") or []:
                    if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "mcp__ccd_session__start_session":
                        wywolania[b.get("id")] = b.get("input") or {}
            elif w.get("type") == "user":
                tresc = (w.get("message") or {}).get("content")
                for b in tresc if isinstance(tresc, list) else []:
                    if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") in wywolania:
                        t = tekst_wyniku(b)
                        for tyt, lid in RE_START.findall(t):
                            tytul_id[lid] = tyt
                        for tyt, tid in RE_PROPOZYCJA.findall(t):
                            tytul_propozycji[tid] = tyt
                for tx in teksty_bloku(tresc):
                    for lid, nazwa, _ in RE_OD_SESJI.findall(tx):
                        tytul_id.setdefault(lid, nazwa)
    return tytul_id, tytul_propozycji


def tytul_pliku(wpisy):
    t = [w.get("customTitle") for w in wpisy if w.get("type") == "custom-title" and w.get("customTitle")]
    return t[-1] if t else None


def zbierz_rozmowy(dane, czysc):
    tytul_id, tytul_propozycji = metadane(dane)
    rodziny = rodziny_plikow(dane)
    pominiete = collections.Counter()
    rozmowy = []
    for rodzina in rodziny:
        wpisy, widziane = [], set()
        kolejnosc = sorted(rodzina, key=lambda s: min((w["timestamp"] for w in dane[s] if w.get("timestamp")), default=""))
        for s in kolejnosc:
            for w in dane[s]:
                u = w.get("uuid")
                if u:
                    if u in widziane:
                        continue
                    widziane.add(u)
                wpisy.append(w)
        wpisy = [w for w in wpisy if w.get("timestamp") and w.get("type") in ("user", "assistant")]
        wpisy.sort(key=lambda w: (w["timestamp"], kolejnosc.index(w["_plik"]), w["_linia"]))
        tytuly = [tytul_pliku(dane[s]) for s in kolejnosc]
        tytul = collections.Counter(t for t in tytuly if t).most_common(1)
        tytul = tytul[0][0] if tytul else kolejnosc[0]
        r = {"pliki": kolejnosc, "tytul": tytul, "wiadomosci": [], "pierwsza_od_sesji": False}
        teksty_asystenta = set()
        pierwszy_user = True
        for w in wpisy:
            czas = czas_pl(w["timestamp"])
            if w["type"] == "user":
                tresc = (w.get("message") or {}).get("content")
                if w.get("toolUseResult") is not None or (isinstance(tresc, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in tresc)):
                    pominiete["wyniki narzędzi"] += 1
                    continue
                if w.get("isCompactSummary"):
                    r["wiadomosci"].append({"rodzaj": "znacznik", "czas": czas, "znacznik": "skrocenie"})
                    pominiete["streszczenie po automatycznym skróceniu rozmowy"] += 1
                    continue
                origin = (w.get("origin") or {}).get("kind")
                if origin == "peer":
                    if str((w.get("origin") or {}).get("from", "")).startswith("local_"):
                        for tx in teksty_bloku(tresc):
                            for lid, nazwa, wnetrze in RE_OD_SESJI.findall(tx):
                                r["wiadomosci"].append({"rodzaj": "znacznik", "czas": czas, "znacznik": "od_sesji",
                                                        "od": lid, "nazwa": nazwa, "tresc_norm": norm(wnetrze)})
                    else:
                        pominiete["raporty agentów pomocniczych"] += 1
                    pierwszy_user = False
                    continue
                if w.get("isMeta"):
                    pominiete["wpisy meta (np. treść umiejętności)"] += 1
                    continue
                teksty = [RE_SR.sub("", t).strip() for t in teksty_bloku(tresc)]
                teksty = [t for t in teksty if t]
                obrazy = sum(1 for b in tresc if isinstance(b, dict) and b.get("type") == "image") if isinstance(tresc, list) else 0
                if origin == "human":
                    if not teksty and not obrazy:
                        pominiete["wiadomość Kuby bez tekstu"] += 1
                        continue
                    tekst = "\n\n".join(teksty)
                    if obrazy:
                        tekst += "\n\n" + "[obraz pominięty]" * obrazy
                    r["wiadomosci"].append({"rodzaj": "kuba", "czas": czas, "autor": "Kuba", "surowy": tekst})
                    pierwszy_user = False
                    continue
                for tx in teksty:
                    if tx.startswith(("Background (from the session that started this one)", "Task (from the session that started this one)")) and pierwszy_user:
                        r["wiadomosci"].append({"rodzaj": "znacznik", "czas": czas, "znacznik": "start", "tresc_norm": norm(tx)})
                        r["pierwsza_od_sesji"] = True
                    elif tx.startswith("[Request interrupted by user"):
                        r["wiadomosci"].append({"rodzaj": "znacznik", "czas": czas, "znacznik": "przerwanie"})
                    elif tx.startswith("<cross-session-message"):
                        for lid, nazwa, wnetrze in RE_OD_SESJI.findall(tx):
                            r["wiadomosci"].append({"rodzaj": "znacznik", "czas": czas, "znacznik": "od_sesji",
                                                    "od": lid, "nazwa": nazwa, "tresc_norm": norm(wnetrze)})
                    elif tx.startswith("<task-notification"):
                        pominiete["powiadomienia o zadaniach w tle"] += 1
                    elif tx.startswith("<side-sessions-event"):
                        pominiete["powiadomienia o sesjach potomnych"] += 1
                    else:
                        pominiete["inne wpisy aplikacji (do przejrzenia)"] += 1
                pierwszy_user = False
            else:
                if w.get("isApiErrorMessage"):
                    pominiete["komunikaty o błędach"] += 1
                    continue
                mid = (w.get("message") or {}).get("id")
                for b in (w.get("message") or {}).get("content") or []:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") == "text" and (b.get("text") or "").strip():
                        klucz = (mid, b["text"])
                        if klucz in teksty_asystenta:
                            continue
                        teksty_asystenta.add(klucz)
                        r["wiadomosci"].append({"rodzaj": "claude", "czas": czas, "autor": "Claude", "surowy": b["text"].strip()})
                    elif b.get("type") == "tool_use":
                        nazwa, wej = b.get("name"), b.get("input") or {}
                        if nazwa == "Agent" and wej.get("prompt"):
                            opis = wej.get("description") or "agent"
                            model = wej.get("model") or wej.get("subagent_type")
                            r["wiadomosci"].append({"rodzaj": "polecenie", "czas": czas, "cel": "agent", "opis": opis,
                                                    "model": model, "surowy": wej["prompt"].strip()})
                        elif nazwa == "mcp__ccd_session__start_session":
                            tresc = "\n\n".join(x.strip() for x in (wej.get("background"), wej.get("prompt")) if x and x.strip())
                            if not tresc:
                                pominiete["propozycje sesji bez treści (sam tytuł)"] += 1
                                continue
                            tyt = wej.get("title") or tytul_propozycji.get(wej.get("proposal_id")) or "nowa sesja"
                            r["wiadomosci"].append({"rodzaj": "polecenie", "czas": czas, "cel": "nowa_sesja", "opis": tyt,
                                                    "inicjatywa": wej.get("initiation"), "surowy": tresc,
                                                    "prompt_norm": norm(wej.get("prompt"))})
                        elif nazwa == "mcp__ccd_session__hand_off_to_session" and wej.get("remaining_plan"):
                            r["wiadomosci"].append({"rodzaj": "polecenie", "czas": czas, "cel": "nowa_sesja",
                                                    "opis": wej.get("title") or "nowa sesja", "inicjatywa": "hand_off",
                                                    "surowy": wej["remaining_plan"].strip(), "prompt_norm": ""})
                        elif nazwa in ("SendMessage", "mcp__ccd_session_mgmt__send_message") and (wej.get("message") or "").strip():
                            do = wej.get("to") or wej.get("recipient") or wej.get("session_id") or ""
                            rodz = wej.get("recipient_kind") or ("session" if str(do).startswith("local_") else "agent")
                            r["wiadomosci"].append({"rodzaj": "polecenie", "czas": czas,
                                                    "cel": "sesja" if rodz == "session" else "agent_dalej",
                                                    "do": do, "opis": tytul_id.get(do), "surowy": wej["message"].strip(),
                                                    "tresc_norm": norm(wej["message"])})
                        else:
                            pominiete["pozostałe wywołania narzędzi"] += 1
        rozmowy.append(r)
    rozmowy.sort(key=lambda r: r["wiadomosci"][0]["czas"] if r["wiadomosci"] else dt.datetime.max.replace(tzinfo=STREFA))
    for r in rozmowy:
        poczatek = r["wiadomosci"][0]["czas"] if r["wiadomosci"] else None
        r["plik"] = nazwa_pliku(poczatek.strftime("%Y-%m-%d") if poczatek else "0000-00-00", r["tytul"])
    nazwy_plikow = collections.Counter(r["plik"] for r in rozmowy)
    for r in rozmowy:
        if nazwy_plikow[r["plik"]] > 1:
            r["plik"] = r["plik"][:-3] + "-" + r["pliki"][0][:8] + ".md"
    for r in rozmowy:
        nr = 0
        for m in r["wiadomosci"]:
            if m["rodzaj"] != "znacznik":
                nr += 1
                m["nr"] = nr
                m["tekst"] = czysc(m["surowy"], (r["plik"], nr, m.get("autor") or "Claude →"))
                if m.get("opis"):
                    m["opis"] = czysc(m["opis"], (r["plik"], nr, "tytuł polecenia"))
    return rozmowy, tytul_id, pominiete


def powiaz(rozmowy, tytul_id):
    """Odnośniki: polecenie startowe sesji potomnej, wiadomości od innych sesji, tytuły odbiorców."""
    po_tytule = {norm(r["tytul"]): r for r in rozmowy}
    starty, wyslane = [], {}
    for r in rozmowy:
        for m in r["wiadomosci"]:
            if m.get("rodzaj") == "polecenie" and m["cel"] == "nowa_sesja" and m.get("prompt_norm"):
                starty.append((m["prompt_norm"][:300], r, m))
            if m.get("rodzaj") == "polecenie" and m["cel"] == "sesja":
                wyslane.setdefault(m["tresc_norm"][:300], (r, m))
                cel = po_tytule.get(norm(m.get("opis") or tytul_id.get(m.get("do"), "")))
                m["cel_rozmowa"] = cel
            if m.get("rodzaj") == "polecenie" and m["cel"] == "nowa_sesja":
                m["cel_rozmowa"] = po_tytule.get(norm(m["opis"]))
    for r in rozmowy:
        for m in r["wiadomosci"]:
            if m.get("znacznik") == "start":
                for pref, rr, mm in starty:
                    if pref and pref in m["tresc_norm"]:
                        m["ref"] = (rr, mm)
                        r["rodzic"] = rr
                        break
            elif m.get("znacznik") == "od_sesji":
                m["ref"] = wyslane.get(m["tresc_norm"][:300])
                m["nadawca"] = po_tytule.get(norm(m["nazwa"])) or (m["ref"][0] if m.get("ref") else None)


# ---------------------------------------------------------------- zapis

def fmt_czas(c):
    return c.strftime("%d.%m.%Y, %H:%M")


def link_rozmowy(r, nr=None, od=""):
    return f"{od}{r['plik']}" + (f"#w{nr}" if nr else "")


def naglowek_polecenia(m):
    if m["cel"] == "agent":
        model = f" (model {m['model']})" if m.get("model") else ""
        return f"Claude → agent „{m['opis']}”{model}"
    if m["cel"] == "agent_dalej":
        return "Claude → agent (dalszy ciąg rozmowy z agentem)"
    cel = m.get("cel_rozmowa")
    if m["cel"] == "nowa_sesja":
        rodz = {"own_initiative": "propozycja nowej sesji", "offer": "propozycja nowej sesji do decyzji Kuby",
                "hand_off": "przekazanie pracy nowej sesji"}.get(m.get("inicjatywa"), "nowa sesja")
        nazwa = f"[„{m['opis']}”]({link_rozmowy(cel)})" if cel else f"„{m['opis']}”"
        return f"Claude → {rodz} {nazwa}"
    nazwa = f"[„{cel['tytul']}”]({link_rozmowy(cel)})" if cel else (f"„{m['opis']}”" if m.get("opis") else "inna sesja")
    return f"Claude → sesja {nazwa}"


def tekst_znacznika(m):
    z = m["znacznik"]
    if z == "przerwanie":
        return "*Kuba przerwał odpowiedź.*"
    if z == "skrocenie":
        return "*Rozmowa skrócona automatycznie, bo skończyło się miejsce w kontekście; streszczenie pominięte.*"
    if z == "start":
        if m.get("ref"):
            rr, mm = m["ref"]
            return (f"*Tę sesję uruchomiła sesja „{rr['tytul']}”. Polecenie startowe: "
                    f"[{rr['plik']}, wiadomość {mm['nr']}]({link_rozmowy(rr, mm['nr'])}).*")
        return "*Tę sesję uruchomiła inna sesja; polecenia startowego nie znaleziono w zapisie.*"
    if z == "od_sesji":
        nad = m.get("nadawca")
        nazwa = nad["tytul"] if nad else m["nazwa"]
        if m.get("ref"):
            rr, mm = m["ref"]
            return f"*Wiadomość od sesji „{nazwa}”: [{rr['plik']}, wiadomość {mm['nr']}]({link_rozmowy(rr, mm['nr'])}).*"
        return f"*Wiadomość od sesji „{nazwa}” (treść pominięta).*"
    return ""


def policz(r):
    c = collections.Counter(m["rodzaj"] for m in r["wiadomosci"])
    return c["kuba"], c["claude"], c["polecenie"]


def zapisz_rozmowe(r):
    w = [m for m in r["wiadomosci"]]
    kuba, claude, pol = policz(r)
    od, do = w[0]["czas"], w[-1]["czas"]
    linie = [f"# {r['tytul']}", ""]
    linie.append(f"Rozmowa z Claude Code w projekcie zadania Telemedi, od {fmt_czas(od)} do {fmt_czas(do)} (czas polski). "
                 f"Wiadomości Kuby: {kuba}. Odpowiedzi Claude: {claude}. Polecenia i wiadomości do innych sesji i agentów: {pol}.")
    linie.append("")
    if r.get("rodzic"):
        start = next(m for m in w if m.get("znacznik") == "start")
        rr, mm = start["ref"]
        linie.append(f"Sesję uruchomiła sesja [„{rr['tytul']}”]({link_rozmowy(rr)}), poleceniem z "
                     f"[wiadomości {mm['nr']}]({link_rozmowy(rr, mm['nr'])}).")
    elif r.get("pierwsza_od_sesji"):
        linie.append("Sesję uruchomiła inna sesja.")
    else:
        linie.append("Sesję otworzył Kuba.")
    if len(r["pliki"]) > 1:
        linie.append("")
        linie.append(f"Rozmowa była wznawiana i zapisała się w {len(r['pliki'])} plikach z tą samą początkową częścią. "
                     "Tę część pokazujemy raz, a dalsze wiadomości z każdego pliku po kolei, według czasu.")
    linie += ["", "Co jest w zapisie, czego w nim nie ma i jakie są oznaczenia: [README](README.md).", ""]
    for m in w:
        if m["rodzaj"] == "znacznik":
            if m["znacznik"] == "start" and r.get("rodzic"):
                continue  # to samo stoi już na górze pliku
            t = tekst_znacznika(m)
            if t:
                linie += [t, ""]
            continue
        if m["rodzaj"] == "kuba":
            autor, tresc = "Kuba", wiadomosc_kuby(m["tekst"])
        elif m["rodzaj"] == "claude":
            autor, tresc = "Claude", formatuj(m["tekst"])
        else:
            autor, tresc = naglowek_polecenia(m), cytat(formatuj(m["tekst"]))
        linie += [f'### <a id="w{m["nr"]}"></a>{m["nr"]}. {autor} · {fmt_czas(m["czas"])}', "", tresc, ""]
    return "\n".join(linie).rstrip() + "\n"


def zapisz_readme(rozmowy, liczniki, historie):
    linie = [
        "# Zapis rozmów z Claude Code",
        "",
        f"Tu jest oczyszczony zapis wszystkich rozmów z Claude Code, w których powstało to rozwiązanie ({len(rozmowy)} rozmów, "
        f"od {fmt_czas(rozmowy[0]['wiadomosci'][0]['czas'])} do {fmt_czas(max(r['wiadomosci'][-1]['czas'] for r in rozmowy))}). "
        "Claude Code to główne narzędzie tej pracy: liczył kodem, pisał notatki i zbudował narzędzie. "
        "Polecenia dla drugiego modelu (Codex) i briefy konsylium są osobno, w `notatki/recenzje/` i `notatki/konsylium/`, "
        "a lekcje zapisane po drodze przez Claude w `notatki/lekcje.md`.",
        "",
        "## Co jest w środku",
        "",
        "Każdy plik to jedna rozmowa. Wiadomości idą po kolei, a przy każdej stoi numer, autor, data i godzina (czas polski). Autorzy:",
        "- **Kuba** — wiadomości wpisane przez Kubę, słowo w słowo, także wklejone bloki tekstu (oznaczone „Wklejony tekst”);",
        "- **Claude** — tekstowe odpowiedzi Claude w rozmowie;",
        "- **Claude → nowa sesja, sesja albo agent** — sama treść poleceń i wiadomości, które Claude wysłał innym sesjom "
        "Claude Code i agentom pomocniczym.",
        "",
        "Pracowaliśmy w wielu sesjach naraz. Sesja prowadząca uruchamiała sesje do kolejnych punktów planu, a te zgłaszały "
        "się z powrotem. Dlatego część rozmów zaczyna się od polecenia innej sesji (odnośnik na górze pliku), a w środku stoją "
        "odnośniki do wiadomości od innych sesji.",
        "",
        "## Czego tu nie ma i dlaczego",
        "",
        "- **Tekstu zadania.** Taka jest decyzja Kuby: zadanie nie trafia do repozytorium. Każdy fragment, który pokrywa się "
        f"z tekstem zadania na {N_SLOW} słów z rzędu albo więcej, jest zastąpiony oznaczeniem.",
        "- **Tego, co aplikacja dokleja do rozmowy:** globalnych instrukcji Kuby dla wszystkich jego projektów, pamięci, listy "
        "podłączonych usług i umiejętności, informacji o środowisku. Dotyczą też innych spraw Kuby, a nie tego zadania. Zasady "
        "pracy z AI w tym projekcie są w `CLAUDE.md`, a lekcje z pamięci projektu w `notatki/lekcje.md`.",
        "- **Wywołań narzędzi i ich wyników** (czytanie i edycja plików, polecenia w terminalu, wydruki danych). Kod i wyniki "
        "są w repozytorium (`analiza/`, `analiza/wyniki/`, `narzedzie/`), a zmiany w historii commitów.",
        "- **Rozmów agentów pomocniczych, automatycznych powiadomień** (o zadaniach w tle, raportów agentów i sesji potomnych) "
        "**i komunikatów aplikacji.** Z komunikatów zostały tylko dwa oznaczenia: „Kuba przerwał odpowiedź” i „rozmowa "
        "skrócona automatycznie”.",
        "- **Rozumowania modelu przed odpowiedzią** — lista dozwolona obejmuje tylko tekst odpowiedzi.",
        "",
        "## Co usunęliśmy z zachowanego tekstu",
        "",
        "W miejscu usuniętego fragmentu stoi oznaczenie w nawiasie kwadratowym.",
        "",
        "| Oznaczenie | Co zastępuje | Ile razy |",
        "|---|---|---:|",
    ]
    for kat in KATEGORIE:
        linie.append(f"| `{OZN[kat]}` | {OPIS_OZN[kat]} | {liczniki.get(kat, 0)} |")
    linie += [
        "",
        "Zostały bez zmian lokalne adresy podglądu strony (127.0.0.1), bo nie prowadzą do żadnej strony w internecie, "
        "oraz nazwy usług „claude.ai” i „Booking.com” jako nazwy łączników, bez adresu strony, tak jak w `CLAUDE.md`. "
        "Odnośniki do plików projektu i do innych sesji są poprawione tak, żeby działały z tego folderu.",
        "",
        "## Jak to powstało",
        "",
        "Skrypt `analiza/f_rozmowy.py` czyta pliki rozmów, które Claude Code zapisuje lokalnie, i przepuszcza tylko tekst "
        "z listy dozwolonej (wyżej). Listę nazw innych projektów i tekst zadania dostaje z plików spoza repozytorium, bo same "
        "nie mogą tu trafić. Na końcu skanuje wynik: adresy, e-maile, ścieżki, nazwy, wzorce kluczy i tekst zadania. Raport "
        "z kontekstem trafień zapisuje poza repozytorium. Zapis trafia do repozytorium dopiero po przejrzeniu wyniku i raportu "
        "przez Kubę.",
        "",
        "Dwie rozmowy były wznawiane i zapisały się w kilku plikach z tą samą początkową częścią. Tę część pokazujemy raz.",
        "",
        "## Rozmowy",
        "",
        "| Od | Do | Rozmowa | Kto ją otworzył | Kuba | Claude | Do innych sesji i agentów |",
        "|---|---|---|---|---:|---:|---:|",
    ]
    for r in rozmowy:
        kuba, claude, pol = policz(r)
        kto = f"sesja „{r['rodzic']['tytul']}”" if r.get("rodzic") else ("inna sesja" if r.get("pierwsza_od_sesji") else "Kuba")
        linie.append(f"| {fmt_czas(r['wiadomosci'][0]['czas'])} | {fmt_czas(r['wiadomosci'][-1]['czas'])} | "
                     f"[{r['tytul']}]({r['plik']}) | {kto} | {kuba} | {claude} | {pol} |")
    if historie:
        linie += ["", "## Gdzie w rozmowach dzieją się historie z README", "",
                  "Sekcja „Jak pracowaliśmy z AI” w głównym README opisuje ślepe uliczki i poprawki. Tu są miejsca w rozmowach, "
                  "w których się wydarzyły.", ""]
        for tytul, miejsca in historie:
            linie.append(f"**{tytul}**")
            for opis, r, nr in miejsca:
                linie.append(f"- {opis}: [{r['plik']}, wiadomość {nr}]({link_rozmowy(r, nr)})")
            linie.append("")
    return "\n".join(linie).rstrip() + "\n"


def znajdz_historie(rozmowy):
    wynik, braki = [], []
    for tytul, miejsca in HISTORIE:
        znalezione = []
        for frag_tytulu, autor, fraza, opis in miejsca:
            traf = None
            for r in rozmowy:
                if norm(frag_tytulu) not in norm(r["tytul"]):
                    continue
                for m in r["wiadomosci"]:
                    if m["rodzaj"] == "znacznik" or (autor and m.get("autor", "Claude →") != autor):
                        continue
                    if norm(fraza) in norm(m["tekst"]):
                        traf = (opis, r, m["nr"])
                        break
                if traf:
                    break
            if traf:
                znalezione.append(traf)
            else:
                braki.append((tytul, frag_tytulu, fraza))
        wynik.append((tytul, znalezione))
    return wynik, braki


# ---------------------------------------------------------------- lekcje

def lekcje(folder, czysc, rozmowy):
    indeks = {}
    for linia in (folder / "MEMORY.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"- \[(.+?)\]\((.+?)\.md\)", linia.strip())
        if m:
            indeks[m.group(2)] = m.group(1)
    wpisy = {}
    for p in sorted(folder.glob("*.md")):
        if p.name == "MEMORY.md":
            continue
        t = p.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n(.*)", t.replace("\r\n", "\n"), re.S)
        glowa, tresc = (m.group(1), m.group(2)) if m else ("", t)
        sesja = re.search(r"originSessionId:\s*(\S+)", glowa)
        wpisy[p.stem] = {"tytul": indeks.get(p.stem, p.stem), "tresc": PRZYCIETE.get(p.stem, tresc.strip()),
                         "sesja": sesja.group(1) if sesja else None, "przyciete": p.stem in PRZYCIETE}
    rozmowa_pliku = {s: r for r in rozmowy for s in r["pliki"]}
    znane = [s for _, lista in GRUPY_LEKCJI for s in lista]
    grupy = [(g, [s for s in lista if s in wpisy]) for g, lista in GRUPY_LEKCJI]
    inne = [s for s in sorted(wpisy) if s not in znane]
    if inne:
        grupy.append(("Inne", inne))
    linie = [
        "# Lekcje z pracy z AI (pamięć projektu)",
        "",
        "Claude Code zapisuje w trakcie pracy krótkie notatki dla kolejnych sesji: co poszło źle, dlaczego i jak tego unikać. "
        f"Ten plik zbiera wszystkie takie notatki z tego projektu ({len(wpisy)}), pogrupowane według tematu. Każda to ślepa "
        "uliczka, pułapka albo poprawka Kuby, z uzasadnieniem i sposobem stosowania.",
        "",
        "Treść wpisów jest taka jak w pamięci, z pięcioma wyjątkami: pominięte pola techniczne (nazwa pliku, opis do "
        "wyszukiwania, typ, identyfikator sesji, data zmiany); etykiety „Why” i „How to apply” zamienione na „Dlaczego” "
        "i „Jak stosować”; odnośniki między wpisami zamienione na linki w tym pliku; ścieżki spoza folderu projektu zastąpione "
        "oznaczeniem; wpis o wyłączaniu łączników przycięty do ogólnej lekcji, bez nazw usług i rozszerzeń spoza projektu. "
        "Pod każdym wpisem jest rozmowa, w której powstał (`rozmowy/`). Plik tworzy skrypt `analiza/f_rozmowy.py`.",
        "",
    ]
    for g, lista in grupy:
        if not lista:
            continue
        linie += [f"## {g}", ""]
        for s in lista:
            wp = wpisy[s]
            tresc = wp["tresc"].replace("**Why:**", "**Dlaczego:**").replace("**How to apply:**", "**Jak stosować:**")
            tresc = re.sub(r"\[\[([^\]]+)\]\]", lambda m: f"[{wpisy[m.group(1)]['tytul']}](#{m.group(1)})" if m.group(1) in wpisy else m.group(1), tresc)
            tresc = czysc(tresc, ("notatki/lekcje.md", s, "lekcja"))
            linie += [f'### <a id="{s}"></a>{wp["tytul"]}', "", formatuj_lekcje(tresc), ""]
            r = rozmowa_pliku.get(wp["sesja"])
            zrodlo = f"Zapisane w rozmowie [„{r['tytul']}”](../rozmowy/{r['plik']})." if r else "Rozmowa, w której powstał wpis, nie jest w zapisie."
            if wp["przyciete"]:
                zrodlo += " Wpis przycięty do ogólnej lekcji."
            linie += [f"*{zrodlo}*", ""]
    return "\n".join(linie).rstrip() + "\n", len(wpisy)


def formatuj_lekcje(t):
    return re.sub(r"^(\s{0,3})(#{1,6})(?=\s)", lambda m: m.group(1) + "#" * min(6, len(m.group(2)) + 3), t, flags=re.M)


# ---------------------------------------------------------------- skan wyniku

def skanuj(pliki, czysc, sprawdz):
    """Skan gotowych plików: to, co powinno już zniknąć (oczekiwane 0), i miejsca do przejrzenia."""
    traf = collections.defaultdict(list)

    def dodaj(kat, sciezka, tekst, a, b):
        nr_linii = tekst.count("\n", 0, a) + 1
        kontekst = tekst[max(0, a - 80):a] + "⟦" + tekst[a:b] + "⟧" + tekst[b:b + 80]
        traf[kat].append((sciezka, nr_linii, kontekst.replace("\n", " ⏎ ")))

    ozn = set(OZN.values())
    for sciezka in pliki:
        tekst = sciezka.read_text(encoding="utf-8")
        wzgl = sciezka.relative_to(KORZEN).as_posix()
        bez_ozn = tekst
        for o in ozn:
            bez_ozn = bez_ozn.replace(o, " " * len(o))
        for kat, wzor in (("adres e-mail", RE_EMAIL), ("adres strony", RE_URL), ("adres strony (sama domena)", RE_DOMENA),
                          ("wzorzec klucza", RE_KLUCZ)):
            for m in wzor.finditer(bez_ozn):
                b = m.end()
                while kat.startswith("adres strony") and b > m.start() and bez_ozn[b - 1] in ".,;:!?)]}”’\"'*_":
                    b -= 1
                if kat.startswith("adres strony") and dozwolony("url", bez_ozn[m.start():b]):
                    dodaj("zostawione celowo: lokalny adres podglądu albo nazwa usługi", wzgl, tekst, m.start(), b)
                else:
                    dodaj(kat, wzgl, tekst, m.start(), b)
        for a, b in czysc.sciezki(bez_ozn, tylko_znajdz=True):
            dodaj("ścieżka spoza projektu", wzgl, tekst, a, b)
        for _, wzor in czysc.usun:
            for m in wzor.finditer(bez_ozn):
                dodaj("nazwa innego projektu", wzgl, tekst, m.start(), m.end())
        for _, wzor in czysc.uslugi:
            for m in wzor.finditer(bez_ozn):
                dodaj("nazwa rozszerzenia spoza projektu", wzgl, tekst, m.start(), m.end())
        for a, b in czysc.zadanie(bez_ozn, tylko_znajdz=True):
            dodaj("tekst zadania (8+ słów)", wzgl, tekst, a, b)
        for w, wzor in sprawdz:
            for m in wzor.finditer(bez_ozn):
                dodaj(f"do przejrzenia: {w}", wzgl, tekst, m.start(), m.end())
        for opis, w in REKRUTACJA:
            for m in re.finditer(w, bez_ozn, flags=re.I if "Pan" not in w else 0):
                dodaj(f"rekrutacja: {opis}", wzgl, tekst, m.start(), m.end())
    return traf


def raport(sciezka, podsumowanie, czysc, traf, dlugie, pominiete):
    L = ["# Raport skanu zapisu rozmów (poza repozytorium)", "", "## Podsumowanie", ""]
    L += [f"- {k}: {v}" for k, v in podsumowanie]
    L += ["", "## Pominięte wpisy (liczby)", ""] + [f"- {k}: {v}" for k, v in sorted(pominiete.items())]
    L += ["", "## Usunięte fragmenty (oryginał w ⟦ ⟧, z kontekstem przed usunięciem)", ""]
    po_kat = collections.defaultdict(list)
    for kat, oryg, kontekst, miejsce in czysc.usuniete:
        po_kat[kat].append((oryg, kontekst, miejsce))
    L += ["Zostawione celowo (bez zmiany): " + ", ".join(f"`{k}` × {v}" for k, v in sorted(czysc.zostawione.items())), ""]
    for kat in ("klucz", "email", "url", "sciezka", "projekt", "usluga", "zadanie"):
        lista = po_kat.get(kat, [])
        L += [f"### {OPIS_OZN[kat]}: {len(lista)}", ""]
        if kat in ("url", "email", "sciezka", "projekt", "usluga"):
            ile = collections.Counter(o for o, _, _ in lista)
            L += ["Różne wartości (liczba wystąpień):", ""] + [f"- `{o}` × {n}" for o, n in ile.most_common()] + [""]
        for oryg, kontekst, miejsce in lista:
            L.append(f"- {miejsce[0]} · {miejsce[1]} · {miejsce[2]}: {kontekst.replace(chr(10), ' ⏎ ')}")
        L.append("")
    L += ["## Skan gotowych plików", ""]
    for kat in sorted(traf):
        L += [f"### {kat}: {len(traf[kat])}", ""]
        L += [f"- {p}:{n}: {k}" for p, n, k in traf[kat]] + [""]
    L += [f"## Wiadomości Kuby dłuższe niż {DLUGA_WIADOMOSC} znaków: {len(dlugie)}", ""]
    L += [f"- {p} · wiadomość {nr} · {n} znaków: {pocz}" for p, nr, n, pocz in dlugie] + [""]
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    sciezka.write_text("\n".join(L), encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- główna

def main():
    sys.stdout.reconfigure(errors="replace")
    a = argumenty()
    usun, uslugi, sprawdz = wczytaj_nazwy(a.nazwy)
    czysc = Czyszczenie(ngramy_zadania(a.zadanie), usun, uslugi, KORZEN)
    pliki = sorted(a.zrodlo.glob("*.jsonl"))
    if not pliki:
        sys.exit(f"Brak plików rozmów w {a.zrodlo}")
    dane = {p.stem: wczytaj_jsonl(p) for p in pliki}
    rozmowy, tytul_id, pominiete = zbierz_rozmowy(dane, czysc)
    rozmowy = [r for r in rozmowy if r["wiadomosci"]]
    powiaz(rozmowy, tytul_id)
    po_tytule = {norm(r["tytul"]): r for r in rozmowy}
    for lid, tyt in tytul_id.items():
        if norm(tyt) in po_tytule:
            MAPA_SESJI[lid] = po_tytule[norm(tyt)]["plik"]

    WYJ_ROZMOWY.mkdir(exist_ok=True)
    for stary in WYJ_ROZMOWY.glob("*.md"):
        if stary.name == "README.md" or re.match(r"\d{4}-\d{2}-\d{2}_", stary.name):
            stary.unlink()
    for r in rozmowy:
        (WYJ_ROZMOWY / r["plik"]).write_text(zapisz_rozmowe(r), encoding="utf-8", newline="\n")
    tekst_lekcji, n_lekcji = lekcje(a.pamiec, czysc, rozmowy)
    WYJ_LEKCJE.write_text(tekst_lekcji, encoding="utf-8", newline="\n")
    liczniki = collections.Counter(k for k, _, _, _ in czysc.usuniete)
    historie, braki = znajdz_historie(rozmowy)
    (WYJ_ROZMOWY / "README.md").write_text(zapisz_readme(rozmowy, liczniki, historie), encoding="utf-8", newline="\n")

    wszystkie = [m for r in rozmowy for m in r["wiadomosci"] if m["rodzaj"] != "znacznik"]
    po_rodz = collections.defaultdict(lambda: [0, 0])
    for m in wszystkie:
        po_rodz[m["rodzaj"]][0] += 1
        po_rodz[m["rodzaj"]][1] += len(m["tekst"])
    dlugie = [(r["plik"], m["nr"], len(m["tekst"]), m["tekst"][:160].replace("\n", " ⏎ "))
              for r in rozmowy for m in r["wiadomosci"] if m["rodzaj"] == "kuba" and len(m["tekst"]) > DLUGA_WIADOMOSC]
    znaczniki = collections.Counter(m["znacznik"] for r in rozmowy for m in r["wiadomosci"] if m["rodzaj"] == "znacznik")
    do_skanu = sorted(WYJ_ROZMOWY.glob("*.md")) + [WYJ_LEKCJE, KORZEN / "README.md"]
    traf = skanuj(do_skanu, czysc, sprawdz)
    znaki_plikow = sum(len(p.read_text(encoding="utf-8")) for p in sorted(WYJ_ROZMOWY.glob("*.md")))

    podsumowanie = [
        ("pliki sesji (JSONL)", len(pliki)),
        ("rozmowy (pliki w rozmowy/, bez README)", len(rozmowy)),
        ("rozmowy zapisane w kilku plikach", sum(1 for r in rozmowy if len(r["pliki"]) > 1)),
        ("wiadomości Kuby", po_rodz["kuba"][0]), ("znaki wiadomości Kuby", po_rodz["kuba"][1]),
        ("odpowiedzi Claude", po_rodz["claude"][0]), ("znaki odpowiedzi Claude", po_rodz["claude"][1]),
        ("polecenia i wiadomości do innych sesji i agentów", po_rodz["polecenie"][0]),
        ("znaki poleceń", po_rodz["polecenie"][1]),
        ("znaki wszystkich plików rozmowy/", znaki_plikow),
        ("oznaczenia: polecenie startowe od innej sesji", znaczniki["start"]),
        ("oznaczenia: wiadomość od innej sesji", znaczniki["od_sesji"]),
        ("oznaczenia: Kuba przerwał odpowiedź", znaczniki["przerwanie"]),
        ("oznaczenia: rozmowa skrócona automatycznie", znaczniki["skrocenie"]),
        ("lekcje w notatki/lekcje.md", n_lekcji),
    ]
    podsumowanie += [(f"usunięte: {OPIS_OZN[k]}", liczniki.get(k, 0)) for k in KATEGORIE]
    podsumowanie += [("zostawione celowo: lokalne adresy podglądu i nazwy usług claude.ai, Booking.com",
                      sum(czysc.zostawione.values()))]
    podsumowanie += [(f"wiadomości Kuby dłuższe niż {DLUGA_WIADOMOSC} znaków", len(dlugie))]
    podsumowanie += [(f"skan wyniku: {k}", len(v)) for k, v in sorted(traf.items())]
    podsumowanie += [("historie z README bez znalezionego miejsca", len(braki))]
    raport(a.raport, podsumowanie, czysc, traf, dlugie, pominiete)
    for k, v in podsumowanie:
        if not k.startswith("skan wyniku: do przejrzenia: "):
            print(f"{k}: {v}")
    print("skan wyniku, listy do przejrzenia (liczba trafień):",
          sum(len(v) for k, v in traf.items() if k.startswith("do przejrzenia: ")))
    print("pominięte wpisy:", dict(sorted(pominiete.items())))
    for tytul, frag, fraza in braki:
        print(f"UWAGA: nie znaleziono miejsca historii „{tytul}” ({frag}): {fraza}")
    if liczniki.get("klucz"):
        print("UWAGA: w zapisie były ciągi wyglądające na klucz — zatrzymaj się i pokaż raport sesji prowadzącej.")


if __name__ == "__main__":
    main()
