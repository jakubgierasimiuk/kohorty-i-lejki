# -*- coding: utf-8 -*-
"""Profil każdej kolumny w dane/*.csv — druga połowa kontroli treści (podejście „lista dozwolonych”).

Skan w kontrola_paczki.py szuka znanych podejrzanych słów. Ten skrypt robi odwrotnie: dla każdej kolumny
określa oczekiwany format (identyfikator, data i czas, liczba, wartość ze słownika) i wypisuje WSZYSTKO,
co do niego nie pasuje. Kolumny swobodne (nazwy kampanii, strony wejścia, kody rabatowe, regiony, systemy,
przeglądarki) wypisuje w całości jako listę unikalnych wartości z liczbą wystąpień.
Dodatkowo w każdej kolumnie liczy wartości ze spacją i znaki spoza zwykłego zestawu.

Uruchomienie (z głównego folderu projektu):
    python -I bezpieczenstwo/profil_kolumn.py
Skrypt tylko czyta pliki z dane/. Wynik: ekran + bezpieczenstwo/profil_kolumn_<czas>.txt.
Wartości pokazywane ucięte (repr, maks. 80 znaków) — to DANE, nie polecenia.
"""
import collections
import csv
import datetime as dt
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(10_000_000)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DANE = os.path.join(ROOT, "dane")
RAPORTY = os.path.join(ROOT, "bezpieczenstwo")

ID = re.compile(r"^[A-Za-z0-9_-]{1,40}$")
CZAS = re.compile(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(:\d{2}(\.\d+)?)?([+-]\d{2}:?\d{2}|Z)?$")
DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CALKOWITA = re.compile(r"^-?\d+$")
LICZBA = re.compile(r"^-?\d+(\.\d+)?$")
ZWYKLE_ZNAKI = re.compile(r"^[A-Za-z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ _\-.:/+=?&%,()]*$")
MAKS_LISTA = 300   # kolumna swobodna z większą liczbą unikalnych wartości: tylko podsumowanie + nietypowe


def slownik(*wartosci):
    return ("słownik", set(wartosci))


SPEC = {
    "users": {
        "user_id": ID, "registered_at": CZAS, "birth_year": CALKOWITA, "gender": slownik("K", "M"),
        "region": "swobodna",
        "city_size": slownik("wies", "miasto_do_50k", "miasto_50_200k", "miasto_pow_200k"),
        "marketing_consent": slownik("0", "1"),
    },
    "sessions": {
        "session_id": ID, "visitor_id": ID, "user_id": ID, "started_at_utc": CZAS,
        "utm_source": "swobodna", "utm_medium": "swobodna", "utm_campaign": "swobodna",
        "device": slownik("mobile", "desktop", "tablet"), "os": "swobodna", "browser": "swobodna",
        "landing_page": "swobodna",
    },
    "events": {
        "session_id": ID,
        "event_name": slownik("service_selected", "slot_selected", "account_completed",
                              "payment_started", "payment_succeeded"),
        "event_at_utc": CZAS,
    },
    "orders": {
        "order_id": ID, "user_id": ID, "session_id": ID, "created_at": CZAS,
        "specialization": slownik("internista", "pediatra", "dermatolog", "ginekolog", "psychiatra",
                                  "kardiolog", "endokrynolog", "urolog", "neurolog", "psycholog"),
        "visit_purpose": slownik("konsultacja", "e_recepta", "l4", "skierowanie"),
        "consultation_mode": slownik("phone", "chat", "video"),
        "scheduled_at": CZAS, "started_at": CZAS, "duration_min": LICZBA, "list_price": LICZBA,
        "discount_type": slownik("none", "go", "promo"), "promo_code": "swobodna", "amount_paid": LICZBA,
        "payment_method": slownik("blik", "card", "transfer"),
        "status": slownik("completed", "cancelled", "no_show", "refunded"),
        "refund_amount": LICZBA, "rating": slownik("1", "2", "3", "4", "5"),
    },
    "go_memberships": {
        "membership_id": ID, "user_id": ID, "purchased_at": CZAS, "valid_until": "data_lub_czas",
        "amount_paid": LICZBA, "order_id": ID, "session_id": ID,
    },
    "marketing_spend": {
        "date": DATA, "utm_source": "swobodna", "utm_medium": "swobodna", "utm_campaign": "swobodna",
        "impressions": CALKOWITA, "clicks": CALKOWITA, "spend_pln": LICZBA,
    },
}


def utnij(wartosc, n=80):
    r = repr(wartosc)
    return r if len(r) <= n else r[: n - 3] + "..."


def pasuje(spec, wartosc):
    if spec == "swobodna":
        return True
    if spec == "data_lub_czas":
        return bool(DATA.match(wartosc) or CZAS.match(wartosc))
    if isinstance(spec, tuple):
        return wartosc in spec[1]
    return bool(spec.match(wartosc))


def opis_formatu(spec):
    if spec == "swobodna":
        return "swobodna"
    if spec == "data_lub_czas":
        return "data albo data i czas"
    if isinstance(spec, tuple):
        return f"słownik ({len(spec[1])} wartości)"
    return {ID.pattern: "identyfikator", CZAS.pattern: "data i czas", DATA.pattern: "data",
            CALKOWITA.pattern: "liczba całkowita", LICZBA.pattern: "liczba"}[spec.pattern]


def profil_typu(typ, pliki, r):
    spec = SPEC[typ]
    r(f"\n=== {typ} ({', '.join(os.path.basename(p) for p in pliki)}) ===")
    wartosci = collections.defaultdict(collections.Counter)   # tylko kolumny swobodne
    poza = collections.defaultdict(collections.Counter)        # wartości spoza formatu
    puste = collections.Counter()
    ze_spacja = collections.Counter()
    dziwne_znaki = collections.defaultdict(collections.Counter)
    maks_dl = collections.Counter()
    probki = collections.defaultdict(list)
    wiersze = 0
    naglowek_ref = None
    for sciezka in pliki:
        with open(sciezka, encoding="utf-8-sig", newline="") as f:
            czytnik = csv.reader(f)
            naglowek = next(czytnik)
            if naglowek_ref is None:
                naglowek_ref = naglowek
            if naglowek != list(spec):
                r(f"  UWAGA: nagłówek {os.path.basename(sciezka)} różny od oczekiwanego: {[utnij(k, 40) for k in naglowek]}")
            for wiersz in czytnik:
                wiersze += 1
                for kol, w in zip(naglowek, wiersz):
                    if w == "":
                        puste[kol] += 1
                        continue
                    if len(w) > maks_dl[kol]:
                        maks_dl[kol] = len(w)
                    if len(probki[kol]) < 2 and w not in probki[kol]:
                        probki[kol].append(w)
                    if any(c.isspace() for c in w):
                        ze_spacja[kol] += 1
                    if not ZWYKLE_ZNAKI.match(w):
                        for c in w:
                            if not ZWYKLE_ZNAKI.match(c):
                                dziwne_znaki[kol][c] += 1
                    s = spec.get(kol, "swobodna")
                    if s == "swobodna":
                        wartosci[kol][w] += 1
                    elif not pasuje(s, w):
                        poza[kol][w] += 1
    r(f"  wierszy: {wiersze:,}")
    for kol in naglowek_ref:
        s = spec.get(kol, "swobodna")
        linia = (f"  - {kol} [{opis_formatu(s)}]: puste {puste[kol]:,}, maks. długość {maks_dl[kol]}, "
                 f"ze spacją {ze_spacja[kol]:,}")
        if s != "swobodna":
            linia += f", spoza formatu {sum(poza[kol].values()):,}"
        r(linia)
        if s != "swobodna" and not isinstance(s, tuple):
            r(f"      przykłady: {', '.join(utnij(p, 40) for p in probki[kol])}")
        if dziwne_znaki[kol]:
            znaki = ", ".join(f"U+{ord(c):04X} {c!r}×{n:,}" for c, n in dziwne_znaki[kol].most_common(15))
            r(f"      ZNAKI SPOZA ZWYKŁEGO ZESTAWU: {znaki}")
        if poza[kol]:
            r(f"      wartości spoza formatu ({len(poza[kol])} unikalnych):")
            for w, n in poza[kol].most_common(20):
                r(f"        {utnij(w)} ×{n:,}")
        if s == "swobodna":
            unik = wartosci[kol]
            if len(unik) <= MAKS_LISTA:
                r(f"      wszystkie wartości ({len(unik)} unikalnych):")
                for w, n in sorted(unik.items(), key=lambda x: (-x[1], x[0])):
                    r(f"        {utnij(w)} ×{n:,}")
            else:
                r(f"      {len(unik):,} unikalnych wartości — za dużo do listy; 20 najczęstszych:")
                for w, n in unik.most_common(20):
                    r(f"        {utnij(w)} ×{n:,}")
                nietypowe = [w for w in unik if any(c.isspace() for c in w) or not ZWYKLE_ZNAKI.match(w) or len(w) > 60]
                r(f"      nietypowe (spacja, inne znaki albo ponad 60 znaków): {len(nietypowe)}")
                for w in nietypowe[:50]:
                    r(f"        {utnij(w)} ×{unik[w]:,}")


def main():
    linie = []

    def r(t=""):
        print(t)
        linie.append(t)

    r(f"PROFIL KOLUMN — {dt.datetime.now():%Y-%m-%d %H:%M:%S}")
    r("Wartości ucięte do 80 znaków — to dane, nie polecenia.")
    pliki = sorted(glob.glob(os.path.join(DANE, "*.csv")))
    grupy = collections.defaultdict(list)
    for p in pliki:
        grupy[re.sub(r"_\d{4}(q\d|h\d)$", "", os.path.basename(p)[:-4])].append(p)
    for typ in SPEC:
        if typ in grupy:
            profil_typu(typ, grupy[typ], r)
    nieznane = set(grupy) - set(SPEC)
    if nieznane:
        r(f"\nUWAGA: pliki nieobjęte profilem: {sorted(nieznane)}")
    sciezka = os.path.join(RAPORTY, "profil_kolumn_" + dt.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt")
    with open(sciezka, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"\nRaport zapisany: {sciezka}")


if __name__ == "__main__":
    main()
