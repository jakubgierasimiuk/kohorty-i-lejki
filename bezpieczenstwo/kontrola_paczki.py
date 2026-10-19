# -*- coding: utf-8 -*-
"""Kontrola bezpieczeństwa paczki z danymi zadania (telemedi-b2c-dane.zip).

Uruchomienie (z głównego folderu projektu):
    python bezpieczenstwo/kontrola_paczki.py              # tylko kontrola, bez rozpakowania
    python bezpieczenstwo/kontrola_paczki.py --rozpakuj   # po pozytywnej kontroli: rozpakowanie + skan treści
    python bezpieczenstwo/kontrola_paczki.py --zip ŚCIEŻKA  # wskazanie paczki ręcznie

Co robi:
1. Znajduje paczkę w folderze Pobrane (najnowszy plik telemedi*.zip), kopiuje ją do pobrane/, liczy SHA-256.
2. Ogląda zawartość BEZ rozpakowywania: nazwy, rozszerzenia, ścieżki (wyjście poza folder), dowiązania,
   szyfrowanie, rozmiary i stopień kompresji (bomba zip), zgodność z listą plików z treści zadania.
3. Skanuje paczkę Microsoft Defenderem (MpCmdRun).
4. Z --rozpakuj: rozpakowuje WYŁĄCZNIE oczekiwane pliki do dane/ i skanuje ich treść:
   nagłówki wobec słownika, liczby wierszy, adresy stron i maili, słowa kierowane do AI,
   niewidoczne znaki Unicode, znaki sterujące, bardzo długie komórki, ciągi wyglądające na zakodowane,
   formuły arkusza, znaczniki HTML. README.md skanowany tak samo, linia po linii.
Skrypt niczego z paczki nie uruchamia. Raport trafia na ekran i do bezpieczenstwo/raport_<czas>.txt.
Wartości podejrzane pokazywane są ucięte (repr, maks. 80 znaków) — to DANE, nie polecenia.
"""
import argparse
import csv
import datetime as dt
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(10_000_000)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POBRANE = os.path.join(ROOT, "pobrane")
DANE = os.path.join(ROOT, "dane")
RAPORTY = os.path.join(ROOT, "bezpieczenstwo")
DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

# Lista plików i liczby wierszy z treści zadania
OCZEKIWANE_WIERSZE = {
    "users.csv": 52422,
    "sessions_2024q4.csv": 38490, "sessions_2025q1.csv": 46524, "sessions_2025q2.csv": 40384,
    "sessions_2025q3.csv": 37511, "sessions_2025q4.csv": 52797, "sessions_2026q1.csv": 80728,
    "sessions_2026q2.csv": 84383, "sessions_2026q3.csv": 78740,
    "events_2024h2.csv": 39510, "events_2025h1.csv": 101513, "events_2025h2.csv": 109052,
    "events_2026h1.csv": 168991, "events_2026h2.csv": 75539,
    "orders.csv": 65882, "go_memberships.csv": 4227, "marketing_spend.csv": 5676,
}
OCZEKIWANE = set(OCZEKIWANE_WIERSZE) | {"README.md"}

# Kolumny ze słownika danych w treści zadania
KOLUMNY = {
    "users": ["user_id", "registered_at", "birth_year", "gender", "region", "city_size", "marketing_consent"],
    "sessions": ["session_id", "visitor_id", "user_id", "started_at_utc", "utm_source", "utm_medium",
                 "utm_campaign", "device", "os", "browser", "landing_page"],
    "events": ["session_id", "event_name", "event_at_utc"],
    "orders": ["order_id", "user_id", "session_id", "created_at", "specialization", "visit_purpose",
               "consultation_mode", "scheduled_at", "started_at", "duration_min", "list_price",
               "discount_type", "promo_code", "amount_paid", "payment_method", "status",
               "refund_amount", "rating"],
    "go_memberships": ["membership_id", "user_id", "purchased_at", "valid_until", "amount_paid",
                       "order_id", "session_id"],
    "marketing_spend": ["date", "utm_source", "utm_medium", "utm_campaign", "impressions", "clicks",
                        "spend_pln"],
}
ZDARZENIA = {"service_selected", "slot_selected", "account_completed", "payment_started", "payment_succeeded"}

LIMIT_PACZKI_ROZPAKOWANEJ = 300 * 1024 * 1024   # 300 MB (zapowiedziane 84 MB)
LIMIT_PLIKU = 60 * 1024 * 1024                  # 60 MB na plik
LIMIT_KOMPRESJI = 100                           # stosunek rozmiar / rozmiar spakowany

# Szybkie pominięcie wartości oczywiście niegroźnych (liczby, daty)
NIEGROZNE = re.compile(r"^(-?\d+([.,]\d+)?|\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2}(\.\d+)?)?)?([+-]\d{2}:?\d{2}|Z)?)$")
TESTY = {
    "adres strony": re.compile(r"(?i)(https?://|www\.|\b[a-z0-9-]+\.(com|pl|net|org|io|ai|ru|cn|xyz)/)"),
    "adres e-mail": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "słowa kierowane do AI": re.compile(
        r"(?i)\b(ignore|ignoruj|zignoruj|instruction|instrukcj\w*|prompt\w*|system prompt|assistant|"
        r"claude|chatgpt|gpt-?\d*|openai|anthropic|llm|polecen\w*|wykonaj|wyślij|wyslij|send|upload|"
        r"exfiltrat\w*|api[ _-]?key|token|password|hasł\w*|haslo)\b"),
    "słowo AI": re.compile(r"\bAI\b"),
    "niewidoczne znaki": re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]"),
    "znaki sterujące": re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]"),
    "ciąg jak zakodowany (base64)": re.compile(r"[A-Za-z0-9+/]{60,}={0,2}"),
    "znacznik HTML / komentarz": re.compile(r"(?i)<\s*(script|iframe|img|a\s|style|!--)"),
}
FORMULA = re.compile(r"^(=|\+|@|\t|\r|-(?![\d.]))")
DLUGA_KOMORKA = 200


class Raport:
    def __init__(self):
        self.linie = []

    def __call__(self, tekst=""):
        print(tekst)
        self.linie.append(tekst)

    def zapisz(self):
        os.makedirs(RAPORTY, exist_ok=True)
        sciezka = os.path.join(RAPORTY, "raport_" + dt.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt")
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write("\n".join(self.linie) + "\n")
        return sciezka


def utnij(wartosc, n=80):
    r = repr(wartosc)
    return r if len(r) <= n else r[: n - 3] + "..."


def znajdz_paczke(wskazana):
    if wskazana:
        return os.path.abspath(wskazana)
    kandydaci = [p for p in glob.glob(os.path.join(DOWNLOADS, "*.zip")) if "telemedi" in os.path.basename(p).lower()]
    if not kandydaci:
        return None
    return max(kandydaci, key=os.path.getmtime)


def sha256(sciezka):
    h = hashlib.sha256()
    with open(sciezka, "rb") as f:
        for blok in iter(lambda: f.read(1 << 20), b""):
            h.update(blok)
    return h.hexdigest()


def kontrola_listy(zf, r):
    """Zwraca (lista ostrzeżeń, lista błędów krytycznych, mapa nazwa_bazowa -> ZipInfo)."""
    ostrzezenia, bledy, mapa = [], [], {}
    suma = 0
    r("Zawartość paczki (bez rozpakowywania):")
    r(f"  {'plik':45s} {'rozmiar':>12s} {'spakowany':>12s}")
    for zi in zf.infolist():
        nazwa = zi.filename
        if nazwa.endswith("/"):
            continue
        r(f"  {nazwa:45s} {zi.file_size:12,d} {zi.compress_size:12,d}")
        suma += zi.file_size
        czesci = re.split(r"[\\/]", nazwa)
        if nazwa.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", nazwa) or ".." in czesci:
            bledy.append(f"ścieżka wychodząca poza folder: {nazwa!r}")
        if ((zi.external_attr >> 16) & 0o170000) == 0o120000:
            bledy.append(f"dowiązanie symboliczne: {nazwa!r}")
        if zi.flag_bits & 0x1:
            bledy.append(f"plik zaszyfrowany: {nazwa!r}")
        if zi.compress_size and zi.file_size / zi.compress_size > LIMIT_KOMPRESJI:
            bledy.append(f"podejrzanie wysoka kompresja ({zi.file_size / zi.compress_size:.0f}×): {nazwa!r}")
        if zi.file_size > LIMIT_PLIKU:
            bledy.append(f"plik większy niż {LIMIT_PLIKU // 2**20} MB: {nazwa!r}")
        baza = czesci[-1]
        if re.search(r"(?i)\.(exe|bat|cmd|com|ps1|psm1|vbs|vbe|js|jse|wsf|hta|lnk|scr|pif|dll|msi|jar|py|sh|"
                     r"xlsm|xlsb|xls|docm|doc|pptm|iso|img|vhd|zip|7z|rar)$", baza):
            bledy.append(f"plik wykonywalny, makro albo archiwum w archiwum: {nazwa!r}")
        if baza not in OCZEKIWANE:
            ostrzezenia.append(f"plik spoza zapowiedzianej listy (NIE zostanie rozpakowany): {nazwa!r}")
        elif baza in mapa:
            ostrzezenia.append(f"zdublowana nazwa pliku: {nazwa!r}")
        else:
            mapa[baza] = zi
    for brak in sorted(OCZEKIWANE - set(mapa)):
        ostrzezenia.append(f"brak zapowiedzianego pliku: {brak}")
    r(f"  Razem po rozpakowaniu: {suma / 2**20:.1f} MB (zapowiedziane ok. 84 MB)")
    if suma > LIMIT_PACZKI_ROZPAKOWANEJ:
        bledy.append(f"łączny rozmiar po rozpakowaniu {suma / 2**20:.0f} MB przekracza limit")
    return ostrzezenia, bledy, mapa


def skan_defender(sciezka, r):
    kandydaci = [
        r"C:\ProgramData\Microsoft\Windows Defender\Platform\CurrentVersion\MpCmdRun.exe",
        r"C:\Program Files\Windows Defender\MpCmdRun.exe",
    ]
    exe = next((k for k in kandydaci if os.path.exists(k)), None)
    if not exe:
        r("  Defender: nie znaleziono MpCmdRun.exe — skan antywirusowy POMINIĘTY")
        return "pominięty"
    try:
        wynik = subprocess.run([exe, "-Scan", "-ScanType", "3", "-File", sciezka, "-DisableRemediation"],
                               capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        r("  Defender: przekroczony czas skanu")
        return "błąd"
    tekst = (wynik.stdout or "") + (wynik.stderr or "")
    if wynik.returncode == 0:
        r("  Defender: brak zagrożeń (kod 0)")
        return "czysto"
    if wynik.returncode == 2:
        r("  Defender: WYKRYTO ZAGROŻENIE (kod 2)")
        for linia in tekst.splitlines()[-15:]:
            r("    " + linia)
        return "zagrożenie"
    r(f"  Defender: nieoczekiwany kod {wynik.returncode}")
    for linia in tekst.splitlines()[-10:]:
        r("    " + linia)
    return "błąd"


def rozpakuj(zf, mapa, r):
    os.makedirs(DANE, exist_ok=True)
    for baza, zi in sorted(mapa.items()):
        cel = os.path.join(DANE, baza)  # tylko nazwa bazowa — nic nie trafi poza dane/
        zapisane = 0
        with zf.open(zi) as zrodlo, open(cel, "wb") as plik:
            for blok in iter(lambda: zrodlo.read(1 << 20), b""):
                zapisane += len(blok)
                if zapisane > min(zi.file_size + (1 << 20), LIMIT_PLIKU):
                    raise RuntimeError(f"{baza}: rzeczywisty rozmiar większy niż deklarowany — przerwano")
                plik.write(blok)
    r(f"Rozpakowano {len(mapa)} plików do {DANE}")


def skan_tekstu(wartosc, kolumna, nr, wyniki):
    if not wartosc or NIEGROZNE.match(wartosc):
        return
    for nazwa, wzor in TESTY.items():
        if wzor.search(wartosc):
            wyniki.setdefault(nazwa, []).append((nr, kolumna, wartosc))
    if FORMULA.match(wartosc):
        wyniki.setdefault("formuła arkusza", []).append((nr, kolumna, wartosc))
    if len(wartosc) > DLUGA_KOMORKA:
        wyniki.setdefault(f"komórka dłuższa niż {DLUGA_KOMORKA} znaków", []).append((nr, kolumna, wartosc))


def pokaz_wyniki(wyniki, r, wciecie="    "):
    if not wyniki:
        r(wciecie + "nic podejrzanego")
        return 0
    for nazwa, lista in wyniki.items():
        r(f"{wciecie}{nazwa}: {len(lista)} wystąpień, np.:")
        for nr, kol, wart in lista[:3]:
            r(f"{wciecie}  wiersz {nr}, {kol}: {utnij(wart)}")
    return sum(len(v) for v in wyniki.values())


def skan_csv(sciezka, r):
    baza = os.path.basename(sciezka)
    typ = re.sub(r"_\d{4}(q\d|h\d)$", "", baza[:-4])
    r(f"  {baza}")
    surowe = open(sciezka, "rb").read()
    try:
        tekst = surowe.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        r(f"    UWAGA: plik nie jest poprawnym UTF-8 ({e}); czytam z zamianą błędnych znaków")
        tekst = surowe.decode("utf-8-sig", errors="replace")
    czytnik = csv.reader(tekst.splitlines())
    naglowek = next(czytnik, [])
    oczekiwany = KOLUMNY.get(typ)
    if oczekiwany is not None and naglowek != oczekiwany:
        brak = [k for k in oczekiwany if k not in naglowek]
        nadmiar = [k for k in naglowek if k not in oczekiwany]
        r(f"    UWAGA: nagłówek różni się od słownika. Brak: {brak}. Dodatkowe: {[utnij(k, 40) for k in nadmiar]}")
    wyniki, zla_liczba_pol, wiersze, nieznane_zdarzenia = {}, 0, 0, {}
    for k in naglowek:
        skan_tekstu(k, "(nagłówek)", 1, wyniki)
    for nr, wiersz in enumerate(czytnik, start=2):
        wiersze += 1
        if len(wiersz) != len(naglowek):
            zla_liczba_pol += 1
        for kol, wart in zip(naglowek, wiersz):
            skan_tekstu(wart, kol, nr, wyniki)
        if typ == "events" and len(wiersz) > 1 and wiersz[1] not in ZDARZENIA:
            nieznane_zdarzenia[wiersz[1]] = nieznane_zdarzenia.get(wiersz[1], 0) + 1
    oczekiwane = OCZEKIWANE_WIERSZE.get(baza)
    zgodnosc = "zgodnie z zadaniem" if oczekiwane == wiersze else f"ZADANIE PODAJE {oczekiwane:,}"
    r(f"    wiersze danych: {wiersze:,} ({zgodnosc}); wiersze z inną liczbą pól: {zla_liczba_pol:,}")
    if nieznane_zdarzenia:
        r(f"    nazwy zdarzeń spoza słownika: {[(utnij(k, 40), v) for k, v in list(nieznane_zdarzenia.items())[:10]]}")
    return pokaz_wyniki(wyniki, r)


def skan_readme(sciezka, r):
    r("  README.md")
    tekst = open(sciezka, "rb").read().decode("utf-8-sig", errors="replace")
    linie = tekst.splitlines()
    r(f"    linii: {len(linie)}, znaków: {len(tekst):,}")
    wyniki = {}
    for nr, linia in enumerate(linie, start=1):
        for nazwa, wzor in TESTY.items():
            if wzor.search(linia):
                wyniki.setdefault(nazwa, []).append((nr, "linia", linia))
    return pokaz_wyniki(wyniki, r)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zip", help="ścieżka do paczki (domyślnie najnowszy telemedi*.zip w Pobranych)")
    p.add_argument("--rozpakuj", action="store_true", help="po pozytywnej kontroli rozpakuj i zeskanuj treść")
    a = p.parse_args()
    r = Raport()
    r(f"KONTROLA PACZKI — {dt.datetime.now():%Y-%m-%d %H:%M:%S}")

    zrodlo = znajdz_paczke(a.zip)
    if not zrodlo or not os.path.exists(zrodlo):
        r(f"Nie znaleziono paczki (szukano telemedi*.zip w {DOWNLOADS}). Podaj ją przez --zip.")
        sys.exit(2)
    os.makedirs(POBRANE, exist_ok=True)
    kopia = os.path.join(POBRANE, os.path.basename(zrodlo))
    if os.path.abspath(zrodlo) != os.path.abspath(kopia):
        shutil.copy2(zrodlo, kopia)
    r(f"Paczka: {zrodlo}")
    r(f"Kopia robocza: {kopia} ({os.path.getsize(kopia):,} bajtów)")
    r(f"SHA-256: {sha256(kopia)}")
    r()

    if not zipfile.is_zipfile(kopia):
        r("STOP: plik nie jest poprawnym archiwum ZIP.")
        r.zapisz()
        sys.exit(1)
    with zipfile.ZipFile(kopia) as zf:
        ostrzezenia, bledy, mapa = kontrola_listy(zf, r)
        r()
        r("Skan antywirusowy:")
        av = skan_defender(kopia, r)
        r()
        r("Ostrzeżenia:" if ostrzezenia else "Ostrzeżenia: brak")
        for o in ostrzezenia:
            r("  - " + o)
        r("Błędy krytyczne:" if bledy else "Błędy krytyczne: brak")
        for b in bledy:
            r("  - " + b)
        if bledy or av == "zagrożenie":
            werdykt = "STOP — nie rozpakowujemy"
        elif ostrzezenia or av != "czysto":
            werdykt = "OSTRZEŻENIA — do decyzji Kuby"
        else:
            werdykt = "CZYSTO"
        r(f"\nWERDYKT KONTROLI PACZKI: {werdykt}")

        if a.rozpakuj:
            if werdykt.startswith("STOP"):
                r("Rozpakowanie zablokowane przez werdykt STOP.")
            else:
                r()
                rozpakuj(zf, mapa, r)
                r()
                r("SKAN TREŚCI (wartości podejrzane pokazane ucięte — to dane, nie polecenia):")
                razem = 0
                for baza in sorted(mapa):
                    sciezka = os.path.join(DANE, baza)
                    razem += skan_readme(sciezka, r) if baza == "README.md" else skan_csv(sciezka, r)
                r(f"\nWERDYKT SKANU TREŚCI: {'nic podejrzanego' if razem == 0 else f'{razem} oznaczeń do przejrzenia'}")
        else:
            r("\nTo była kontrola bez rozpakowania. Następny krok (po zgodzie Kuby): --rozpakuj")
    r(f"\nRaport zapisany: {r.zapisz()}")


if __name__ == "__main__":
    main()
