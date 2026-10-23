"""F — liczby na wykresach wobec tekstu i tabel tej samej karty (ostatnia kontrola przed publikacją, część 2: technika).

Otwiera stronę z folderu narzedzie/ w Microsoft Edge bez okna (Playwright, lokalny serwer 127.0.0.1 z losowym portem)
przy szerokości 1366 px (komputer) i 375 px (telefon). Liczby czyta z wyrenderowanej strony (DOM): podpisy wykresów,
podpowiedzi (atrybut title), teksty kart i tabele, także te w zwijanych sekcjach. Nie czyta kodu, który rysuje wykresy.

Porównuje każdą liczbę wypisaną na wykresie z tą samą liczbą w tekście albo w tabeli tej samej karty (ta sama jednostka
i ten sam okres; wiersz tabeli dobrany po etykiecie, kolumna po nagłówku). Gdy karta danej liczby nie podaje, porównuje
z niezależnym źródłem i zaznacza to w kolumnie „odniesienie”: z tabelą tej samej zakładki liczoną w przeglądarce z danych
pacjent po pacjencie, z rachunkiem w Pythonie na plikach danych strony albo z raportem w analiza/wyniki/. Sprawdza też
stany zdania nad mapą kohort (widoczne tylko przy mapie miesięcznej bez zawężeń).

Wykresy dzienne (uPlot, rysowane na płótnie) nie mają liczb w DOM; ich numery zdarzeń sprawdzamy przez listę zdarzeń pod
wykresem. Takie wykresy są wypisane w raporcie jako „nie dało się porównać” z powodem.

Uruchomienie z głównego folderu:
    python -I analiza/f_wykresy_tekst.py [--silnik msedge|webkit|firefox]
Wynik: analiza/wyniki/f_wykresy_tekst.txt (Edge); przy innym silniku f_wykresy_tekst_<silnik>.txt. WebKit to silnik Safari,
a WebKit i Firefox to przeglądarki z pakietu Playwright (bez instalowania). Firefox nie emuluje telefonu (is_mobile),
więc przy 375 px ma tylko wąskie okno.
"""
import argparse
import datetime as dt
import functools
import http.server
import json
import os
import re
import subprocess
import sys
import threading
from decimal import ROUND_HALF_UP, Decimal

from playwright.sync_api import sync_playwright

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARZEDZIE = os.path.join(KATALOG, "narzedzie")
WYNIKI = os.path.join(KATALOG, "analiza", "wyniki")
RAPORT = os.path.join(WYNIKI, "f_wykresy_tekst.txt")
SZEROKOSCI = [(1366, 900, False), (375, 812, True)]
ZAKLADKI = ["wzrost", "kohorty", "lejek", "po-zakupie", "zdarzenia", "wynik", "jakosc", "priorytety", "niewiadome"]
NAZWY = {"wzrost": "Czy to wzrost", "kohorty": "Kohorty", "lejek": "Lejek", "po-zakupie": "Po zakupie",
         "zdarzenia": "Zdarzenia", "wynik": "Wynik biznesu", "jakosc": "Jakość danych", "priorytety": "Priorytety",
         "niewiadome": "Czego nie wiemy"}
# znaki gotowości: wszystkie wykresy zakładki narysowane (część wczytuje dane później, np. kwartały i udział nowych kampanii)
GOTOWE = {
    "wzrost": ["#wz-nowy .slupki-skum .wk-wiersz", "#wz-nowy .hantle .wk-wiersz", "#wz-nowy .slupki-parami .wk-wiersz",
               "#wz-nowy .slupki-grup .sg-wiersz", "#wz-nowy .schodki .wk-wiersz"],
    "kohorty": ["#ko-naglowek .hantle .wk-wiersz", "#ko-tabela tbody tr", "#ko-macierz tbody tr"],
    "lejek": ["#lj-naprawy .hantle .wk-wiersz", "#lj-kroki .lk-krok", "#lj-udzial .kl-grupa", "#lj-tabela tbody tr"],
    "po-zakupie": ["#pz-karta-godziny .kolumny .kl-grupa", "#pz-ruch-hantle .wk-wiersz", "#pz-godziny tbody tr"],
    "zdarzenia": ["#zd-tabela tbody tr", "#zd-lista .zdarzenie", "#zd-os svg .os-nr, #zd-os .os-pionowa li"],
    "wynik": ["#ek-wykres .wk-wiersz", "#wy-kwartaly-wykres .sg-wiersz", "#wy-kwartaly tbody tr", "#wy-tabela tbody tr"],
    "jakosc": ["#jk-karta-mostek .schodki .wk-wiersz", "#jk-testy-kw .slupek-wiersz"],
    "priorytety": ["#pr-karty article", "#pr-1 .hantle .wk-wiersz", "#pr-przeglad tbody tr"],
    "niewiadome": ["#nw-tabela tbody tr"],
}

# Odczyt wyrenderowanej zakładki: widoczne karty (article) z tekstem bez wykresów i tabel, tabele (także w zwijanych
# sekcjach), wykresy w kartach (figure.wk), kafelki, kroki lejka, słupki zamówień testowych, oś zdarzeń, listy zdarzeń
# pod wykresami dziennymi, pasek pozycji priorytetu i zdanie nad mapą kohort.
ZBIERZ = r"""
(z) => {
  const v = document.getElementById('v-' + z);
  const T = e => e ? (e.textContent || '').replace(/[\s   ]+/g, ' ').trim() : '';
  const wlasne = (a, sel) => [...a.querySelectorAll(sel)].filter(x => x.closest('article') === a);
  const zm = e => { const s = e && e.querySelector('.zm > span'); return s ? T(s) : ''; };
  const atr = (e, n) => (e && e.getAttribute(n)) || '';
  const tabela = t => ({ id: t.id || '', wDetails: !!t.closest('details'), podpis: T(t.querySelector('caption')),
    naglowki: [...t.querySelectorAll('thead tr')].map(r => [...r.children].map(T)),
    wiersze: [...t.querySelectorAll('tbody tr')].map(r => ({ klasa: r.className, id: r.id || '',
      komorki: [...r.children].map(c => ({ t: T(c), b: T(c.querySelector('.b')), n: T(c.querySelector('.n')), a: T(c.querySelector('.a')),
        strong: T(c.querySelector('strong')), zm: zm(c), przypis: T(c.querySelector('.przypis')), pod: T(c.querySelector('.pod')),
        kwota: T(c.querySelector('.kwota')), kdop: T(c.querySelector('.kwota-dopisek')), znacznik: T(c.querySelector('.znacznik')),
        pdop: T(c.querySelector('.pewnosc-dopisek')), link: T(c.querySelector('a')), href: atr(c.querySelector('a'), 'href'),
        linki: [...c.querySelectorAll('a')].map(x => ({ t: T(x), href: atr(x, 'href') })), tytul: atr(c, 'title') })) })) });
  const wykres = f => ({ klasa: f.className, opis: atr(f, 'aria-label'), przypis: T(f.querySelector('figcaption')),
    tytul: T(f.querySelector('.kl-tytul')), legenda: [...f.querySelectorAll('.wk-legenda .wk-lg')].map(T),
    os: [...f.querySelectorAll('.wk-os-skala span, .kl-os-y span')].map(T),
    wiersze: [...f.querySelectorAll('.wk-wiersz:not(.wk-os), .wk-podtytul, .wk-grupa-tytul, .kl-grupa')].map(w => ({
      klasa: w.className, tekst: T(w), etykieta: T(w.querySelector('.wk-etykieta')),
      a: T(w.querySelector('.wk-a')), b: T(w.querySelector('.wk-ab strong')), zm: zm(w),
      slupki: [...w.querySelectorAll('.wk-slupek-tekst')].map(T),
      segmenty: [...w.querySelectorAll('.wk-segment')].map(s => ({ klasa: s.className, t: T(s) })),
      suma: T(w.querySelector('.wk-wart > strong')), sg: [...w.querySelectorAll('.sg-tekst')].map(T),
      v: [...w.querySelectorAll('.wk-v')].map(T), uwaga: T(w.querySelector('.znacznik')), bez: !!w.querySelector('.wk-bez'),
      podpisy: [...w.querySelectorAll('.kl-wart')].map(T), tytul: atr(w, 'title'), aria: atr(w, 'aria-label') })) });
  const karty = [...v.querySelectorAll('article, details.zdarzenie')].filter(a => !a.closest('[hidden]')).map(a => {
    const k = a.cloneNode(true);
    k.querySelectorAll('article, figure.wk, .wk-dwa, table, .lejek-kroki, .os-zdarzen, .slupki-poziome, .kafelki, .pasek-priorytetu')
      .forEach(x => x.remove());
    const wm = a.querySelector('#ko-macierz-wniosek');
    return {
      id: a.id || '', klasa: a.className, tytul: T(a.querySelector('h2, h3')), tekst: T(k),
      tabele: wlasne(a, 'table').map(tabela), wykresy: wlasne(a, 'figure.wk').map(wykres),
      kafelki: wlasne(a, '.kafelek').map(x => ({ liczba: T(x.querySelector('.kafelek-liczba')), zm: zm(x),
        podpis: T(x.querySelector('.kafelek-podpis')), dopisek: T(x.querySelector('.kafelek-dopisek')) })),
      werdyktDopisek: T(a.querySelector('.werdykt-dopisek')),
      kroki: wlasne(a, '.lk-krok, .lk-przejscie').map(x => ({ klasa: x.className, nazwa: T(x.querySelector('.lk-nazwa')),
        n: T(x.querySelector('.lk-n')), b: T(x.querySelector('.lk-b')), a: T(x.querySelector('.lk-a')),
        dalej: T(x.querySelector('.lk-dalej strong')), dalejA: T(x.querySelector('.lk-dalej .przypis')), zm: zm(x),
        tytul: atr(x.querySelector('.lk-tor'), 'title') })),
      testy: wlasne(a, '.slupki-poziome').map(x => [...x.children].map(T)),
      os: wlasne(a, '.os-zdarzen svg').map(s => ({ szer: s.viewBox.baseVal.width,
        nr: [...s.querySelectorAll('text.os-nr')].map(t => ({ t: T(t), x: +t.getAttribute('x') })),
        znaczniki: [...s.querySelectorAll('[tabindex]')].map(m => ({ aria: atr(m, 'aria-label'), tag: m.tagName, klasa: atr(m, 'class'),
          x: m.tagName === 'circle' ? +m.getAttribute('cx') : m.tagName === 'rect' ? +m.getAttribute('x') + (m.classList.contains('znacznik-zakres') ? 0 : 5.5)
            : +((atr(m, 'd').match(/^M([\d.]+)/) || [0, 0])[1]) })) })),
      osPion: wlasne(a, '.os-pionowa li').map(li => ({ data: T(li.querySelector('.os-data strong')), obszar: T(li.querySelector('.obszar')),
        link: T(li.querySelector('a')), href: atr(li.querySelector('a'), 'href') })),
      listyZd: wlasne(a, '.lista-zdarzen-wykres').map(ol => [...ol.querySelectorAll('li')].map(li => ({ nr: li.value, t: T(li),
        href: atr(li.querySelector('a'), 'href') }))),
      meta: T(a.querySelector('.meta .data')), obszar: T(a.querySelector('.meta .obszar')),
      pasek: wlasne(a, '.pasek-priorytetu').map(p => ({ kwota: T(p.querySelector('.kwota')), dopisek: T(p.querySelector('.kwota-dopisek')),
        pewnosc: T(p.querySelector('.znacznik')), pdop: T(p.querySelector('.pewnosc-dopisek')), wdrozenie: T(p.querySelector('.pasek-wartosc')) })),
      wniosekMapy: wm ? { t: T(wm), widoczne: !wm.hidden && !wm.closest('[hidden]') } : null,
      pigulki: wlasne(a, '#pr-pigulki a').map(x => ({ t: T(x), href: atr(x, 'href'), tytul: atr(x, 'title') })),
      chipy: wlasne(a, '#zd-filtry label').map(T),
    };
  });
  const nw = document.getElementById('nw-tabela');
  return { zakladka: z, karty, niewiadome: z === 'niewiadome' && nw ? tabela(nw) : null };
}
"""


# ------------------------------------------------------------------ pomocnicze: liczby w polskim zapisie
def norm(s):
    return re.sub(r"[\s   ]+", " ", str(s or "")).replace("−", "-").replace("–", "–").strip()


LICZBA = re.compile(r"[+-]?\d{1,3}(?: \d{3})+(?:,\d+)?(?!\d)|[+-]?\d+(?:,\d+)?")
PROC = re.compile(r"[+-]?\d{1,3}(?: \d{3})*(?:,\d+)?%")


def liczby(s):
    return [float(x.replace(" ", "").replace(",", ".")) for x in LICZBA.findall(norm(s))]


def l1(s):
    x = liczby(s)
    return x[0] if x else None


def proc_z(s):
    m = PROC.search(norm(s))
    return m.group(0) if m else None


def zaokr(x, m=0):
    q = Decimal(1).scaleb(-m)
    return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))


def pl(x, m=0):
    """Liczba w zapisie strony: spacja tysięcy, przecinek, minus jako „-” (po norm)."""
    s = f"{abs(zaokr(x, m)):,.{m}f}".replace(",", " ").replace(".", ",")
    return ("-" if x < 0 and zaokr(x, m) != 0 else "") + s


def jest(tekst, token):
    """Czy liczba (z jednostką) stoi w tekście jako osobny zapis; zwraca zdanie, w którym stoi, albo None."""
    t, tok = norm(tekst), norm(token)
    m = re.search(r"(?<![\d,])[+]?" + re.escape(tok.lstrip("+")) + r"(?![\d]|,\d)", t)
    if not m:
        return None
    pocz = max(t.rfind(". ", 0, m.start()) + 2, m.start() - 90)
    kon = t.find(". ", m.end())
    kon = len(t) if kon < 0 or kon - m.end() > 90 else kon + 1
    return t[pocz:kon]


def data_pl(s):
    """„17.03.2026” → date."""
    d, m, r = s.split(".")
    return dt.date(int(r), int(m), int(d))


RZYM = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


def miesiac(et):
    """„XI 2025” → (2025, 11)."""
    a, b = norm(et).split(" ")[:2]
    return int(b), RZYM.index(a) + 1


# ------------------------------------------------------------------ zapis porównań
class Wynik:
    def __init__(self):
        self.wiersze, self.nie = [], []
        self.szer = None

    def por(self, zakl, karta, wykres, co, na_wykresie, odniesienie, ok, zrodlo="tekst karty"):
        self.wiersze.append({"szer": self.szer, "zakl": zakl, "karta": karta, "wykres": wykres, "co": co,
                             "w": str(na_wykresie), "o": str(odniesienie), "zrodlo": zrodlo, "ok": bool(ok)})
        return ok

    def rowne(self, zakl, karta, wykres, co, a, b, zrodlo="tabela karty"):
        return self.por(zakl, karta, wykres, co, a, b, norm(a) == norm(b), zrodlo)

    def w_tekscie(self, zakl, karta, wykres, co, token, tekst, zrodlo="tekst karty"):
        zd = jest(tekst, token)
        return self.por(zakl, karta, wykres, co, token, ("„" + zd + "”") if zd else "BRAK w tekście", zd is not None, zrodlo)

    def niedasie(self, zakl, wykres, powod):
        if (zakl, wykres, powod) not in [(x[0], x[1], x[2]) for x in self.nie]:
            self.nie.append((zakl, wykres, powod, self.szer))


def karta(karty, id=None, wykres=None, tabela=None, tytul=None):
    for k in karty:
        if id and k["id"] == id:
            return k
        if wykres and any(wykres in f["klasa"].split() for f in k["wykresy"]) and not (wykres == "hantle" and any("hantle-grupy" in f["klasa"] for f in k["wykresy"])):
            return k
        if tabela and any(t["id"] == tabela for t in k["tabele"]):
            return k
        if tytul and tytul in k["tytul"]:
            return k
    return None


def wyk(k, klasa):
    for f in k["wykresy"]:
        if klasa in f["klasa"].split():
            return f
    return None


def tab(k, naglowek=None, id=None):
    for t in k["tabele"]:
        if id and t["id"] == id:
            return t
        if naglowek and t["naglowki"] and any(naglowek in h for r in t["naglowki"] for h in r):
            return t
    return None


def kolumna(t, nazwa, wiersz_nagl=-1):
    nag = t["naglowki"][wiersz_nagl]
    for i, h in enumerate(nag):
        if norm(h) == norm(nazwa) or norm(h).startswith(norm(nazwa)):
            return i
    raise KeyError(f"brak kolumny {nazwa!r} w {nag}")


def wiersz_tab(t, etykieta, przez=lambda s: s):
    for w in t["wiersze"]:
        if w["komorki"] and przez(norm(w["komorki"][0]["t"])) == przez(norm(etykieta)):
            return w
    return None


# ------------------------------------------------------------------ zakładka „Czy to wzrost”
def kontrola_wzrost(W, karty):
    """Pierwsza zakładka od rundy G (2026-10-23): werdykt z trzema linijkami i kafelkami, osiem kroków z identyfikatorami
    wz-<krok> i karta TelemediGO. Wykresy porównywane z tabelą i tekstem tej samej karty, kafelki i werdykt z wykresami."""
    Z = NAZWY["wzrost"]
    kw = karta(karty, id="wz-werdykt")
    kp, kr, kg = karta(karty, id="wz-pacjenci"), karta(karty, id="wz-retencja"), karta(karty, id="wz-telemedigo")
    kk, km, kn, kmz = karta(karty, id="wz-wynik"), karta(karty, id="wz-dashboard"), karta(karty, id="wz-na-pacjencie"), karta(karty, id="wz-marza")
    # 1. słupki nowych pacjentów (krok 2)
    f, K = wyk(kp, "slupki-skum"), "Skąd są nowi pacjenci"
    sumy = {}
    for w in f["wiersze"]:
        m = re.match(r"(.*?): pozostałe kampanie i kanały ([\d ]+), nowe kampanie na L4 ([\d ]+), razem ([\d ]+)$", norm(w["tytul"]))
        okres, poz, now, raz = m.group(1), l1(m.group(2)), l1(m.group(3)), l1(m.group(4))
        sumy[okres] = (poz, now, raz)
        W.rowne(Z, K, "słupki pacjentów", f"{okres}: liczba na końcu słupka = razem w podpowiedzi", w["suma"], pl(raz), "podpowiedź wykresu")
        W.por(Z, K, "słupki pacjentów", f"{okres}: części sumują się do razem", f"{pl(poz)} + {pl(now)}", pl(raz), poz + now == raz, "rachunek")
        for s, v in zip(w["segmenty"], [x for x in (poz, now) if x > 0]):
            if s["t"]:
                W.rowne(Z, K, "słupki pacjentów", f"{okres}: podpis części słupka", s["t"], pl(v), "podpowiedź wykresu")
    raz1, raz2 = sumy["rok wcześniej"][2], sumy["ostatnie 12 miesięcy"][2]
    poz2, now2 = sumy["ostatnie 12 miesięcy"][0], sumy["ostatnie 12 miesięcy"][1]
    udz = 100 * now2 / (raz2 - raz1)
    for tok in (pl(raz2 - raz1), pl(now2), f"{pl(udz)}% przyrostu", f"tylko o {pl(100 * (poz2 / raz1 - 1))}%"):
        W.w_tekscie(Z, K, "słupki pacjentów", "przyrost, pacjenci nowych kampanii i ich udział w przyroście w tekście karty", tok, kp["tekst"])
    # 2. hantle powrotu (krok 3) wobec tabeli karty
    f, t, K = wyk(kr, "hantle"), tab(kr, "Powrót w ciągu"), "Czy wracają"
    hantle_powrotu(W, Z, K, f, t)
    h90 = [w for w in f["wiersze"] if "90 dni" in w["etykieta"]][0]
    for v in (f"{pl(zaokr(l1(h90['b'])))}%", f"{pl(zaokr(l1(h90['a'])))}%"):
        W.w_tekscie(Z, K, "hantle powrotu", "zaokrąglony powrót w 90 dniach (hantel 90 dni) w tekście", v, kr["tekst"])
    # 3. TelemediGO: słupki parami wobec tabeli karty
    f, t, K = wyk(kg, "slupki-parami"), tab(kg, "Typ zakupu"), "TelemediGO"
    ia, ib, iz = kolumna(t, "Rok wcześniej"), kolumna(t, "Ostatnie 12 miesięcy"), kolumna(t, "Zmiana")
    for w in f["wiersze"]:
        r = next((x for x in t["wiersze"] if norm(x["komorki"][0]["t"]).startswith(norm(w["etykieta"]))), None)
        if r is None:
            W.por(Z, K, "słupki TelemediGO", f"{w['etykieta']}: wiersz tabeli", w["etykieta"], "BRAK wiersza", False)
            continue
        if norm(r["komorki"][0]["t"]) != norm(w["etykieta"]):
            W.niedasie(Z, "słupki TelemediGO", f"podpis wiersza na wykresie („{w['etykieta']}”) krótszy niż w tabeli („{r['komorki'][0]['t']}”); liczby porównane")
        W.rowne(Z, K, "słupki TelemediGO", f"{w['etykieta']}: rok wcześniej", w["slupki"][0], r["komorki"][ia]["t"])
        W.rowne(Z, K, "słupki TelemediGO", f"{w['etykieta']}: ostatnie 12 miesięcy", w["slupki"][1], r["komorki"][ib]["t"])
        W.rowne(Z, K, "słupki TelemediGO", f"{w['etykieta']}: zmiana", w["zm"], r["komorki"][iz]["t"])
    # 4. kwartały (krok 6): słupki grupowane wobec tabeli karty (zmiana rok do roku i poziom w tys. zł)
    f, t, K = wyk(kk, "slupki-grup"), tab(kk, "Marża przed kosztem kampanii"), "W którą stronę to idzie"
    im, ik = kolumna(t, "Marża przed kosztem kampanii"), kolumna(t, "Wydatki na kampanie")
    kw3 = None
    for w in f["wiersze"]:
        r = wiersz_tab(t, w["etykieta"], lambda s: s.replace("kw. ", ""))
        mt = re.search(r"marża przed kosztem kampanii ([\d ]+) zł wobec ([\d ]+) zł, wydatki na kampanie ([\d ]+) zł wobec ([\d ]+) zł", norm(w["tytul"]))
        W.rowne(Z, K, "kwartały", f"{w['etykieta']}: zmiana marży przed kosztem kampanii", w["sg"][0], r["komorki"][im]["zm"])
        W.rowne(Z, K, "kwartały", f"{w['etykieta']}: zmiana wydatków na kampanie", w["sg"][1], r["komorki"][ik]["zm"])
        W.rowne(Z, K, "kwartały", f"{w['etykieta']}: marża przed kosztem kampanii (podpowiedź, tys. zł)", pl(l1(mt.group(1)) / 1000, 1) + " tys. zł", r["komorki"][im]["pod"])
        W.rowne(Z, K, "kwartały", f"{w['etykieta']}: wydatki na kampanie (podpowiedź, tys. zł)", pl(l1(mt.group(3)) / 1000, 1) + " tys. zł", r["komorki"][ik]["pod"])
        if w["etykieta"] == "III kw. 2026":
            kw3 = (l1(w["sg"][0]), l1(w["sg"][1]))
    W.w_tekscie(Z, K, "kwartały", "III kw. 2026: zmiana marży przed kosztem kampanii w tekście (zaokrąglona)", f"{pl(kw3[0])}%", kk["tekst"])
    W.por(Z, K, "kwartały", "III kw. 2026: „wydatki ponad dwa razy wyższe” = zmiana wydatków ponad +100%", f"+{pl(kw3[1], 1)}%", "ponad dwa razy",
          kw3[1] > 100 and "ponad dwa razy wyższe" in kk["tekst"], "tekst karty")
    # 5. schodki mostka (krok 1) wobec tabeli mostka
    schodki_mostka(W, Z, "Ile z liczb z dashboardu jest prawdą", wyk(km, "schodki"), tab(km, "Krok"), km["tekst"])
    # 6. zostaje na pacjencie miesiąc po miesiącu (krok 4): punkty wobec tabeli w szczegółach i zdań karty
    f, t, K = wyk(kn, "punkty-zero"), tab(kn, "Miesiąc pierwszego zakupu"), "Ile zarabiamy na nowym pacjencie"
    i1, i2 = kolumna(t, "Zostaje na pacjencie"), kolumna(t, "Zostaje na pacjencie według sesji z płatnością")
    od_kwietnia = []
    for w in f["wiersze"]:
        et = norm(w["etykieta"]).replace(" *", "")
        r = wiersz_tab(t, et)
        if r is None:
            W.por(Z, K, "punkty wyniku", f"{et}: wiersz tabeli", et, "BRAK", False)
            continue
        W.rowne(Z, K, "punkty wyniku", f"{et}: zostaje na pacjencie według pierwszego wejścia", w["v"][0], r["komorki"][i1]["zm"] or r["komorki"][i1]["t"])
        W.rowne(Z, K, "punkty wyniku", f"{et}: zostaje na pacjencie według sesji z płatnością", w["v"][1], r["komorki"][i2]["zm"] or r["komorki"][i2]["t"])
        rok, mies = miesiac(et)
        W.por(Z, K, "punkty wyniku", f"{et}: gwiazdka (przybliżenie) tylko od kwietnia 2026", "*" if "*" in w["etykieta"] else "—",
              "*" if (rok, mies) >= (2026, 4) else "—", ("*" in w["etykieta"]) == ((rok, mies) >= (2026, 4)), "tytuł tabeli")
        if (rok, mies) >= (2026, 4):
            od_kwietnia.append((l1(w["v"][0]), l1(w["v"][1])))
    W.w_tekscie(Z, K, "punkty wyniku", "od kwietnia: najniższa wartość według pierwszego wejścia (zaokrąglona) w tekście",
                f"od {pl(min(a for a, _ in od_kwietnia))}", kn["tekst"])
    W.w_tekscie(Z, K, "punkty wyniku", "od kwietnia: najwyższa wartość według pierwszego wejścia (zaokrąglona) w tekście",
                f"do +{pl(max(a for a, _ in od_kwietnia))} zł", kn["tekst"])
    W.w_tekscie(Z, K, "punkty wyniku", "od kwietnia według sesji z płatnością: zakres strat (zaokrąglony) w tekście",
                f"{pl(-max(b for _, b in od_kwietnia))}–{pl(-min(b for _, b in od_kwietnia))} zł", kn["tekst"])
    W.por(Z, K, "punkty wyniku", "od kwietnia według sesji z płatnością każdy miesiąc pod kreską („tracą”)",
          ", ".join(pl(b, 1) for _, b in od_kwietnia), "wszystkie < 0", all(b < 0 for _, b in od_kwietnia), "rachunek")
    # 7. marża po wszystkich kosztach w obu latach (krok 5): segmenty, suma i tekst
    f, K = wyk(kmz, "slupki-skum"), "Skąd w takim razie +27% marży"
    sm = {}
    for w in f["wiersze"]:
        seg = [l1(s["t"]) for s in w["segmenty"] if s["t"]]
        sm[w["etykieta"]] = (seg, l1(w["suma"]))
        W.por(Z, K, "słupki marży", f"{w['etykieta']}: części sumują się do sumy (±1 tys. zł z zaokrągleń)", " + ".join(pl(x) for x in seg),
              w["suma"], abs(sum(seg) - l1(w["suma"])) <= 1, "rachunek")
        for x in seg + [l1(w["suma"])]:
            W.w_tekscie(Z, K, "słupki marży", f"{w['etykieta']}: kwota z wykresu w tekście karty albo werdyktu", f"{pl(x)} tys. zł",
                        kmz["tekst"] + " " + kw["tekst"])
    m1, m2 = sm["rok wcześniej"][1], sm["ostatnie 12 miesięcy"][1]
    baza = sm["ostatnie 12 miesięcy"][0][1]
    W.w_tekscie(Z, K, "słupki marży", "przyrost marży (suma ostatnich 12 miesięcy − rok wcześniej) w tekście", f"{pl(m2 - m1)} tys. zł", kmz["tekst"])
    W.w_tekscie(Z, K, "słupki marży", "udział pacjentów z pierwszego roku w przyroście (z wykresu, zaokrąglony) w tekście",
                f"{pl(100 * baza / (m2 - m1))}% przyrostu", kmz["tekst"])
    W.w_tekscie(Z, "werdykt", "linijka „Więcej zarabiamy”", "marża z wykresu kroku 5 w werdykcie", f"z {pl(m1)} do {pl(m2)} tys. zł", kw["tekst"])
    # 8. kafelki i zdanie werdyktu wobec wykresów i kart kroków
    K = "werdykt (kafelki)"
    for kf in kw["kafelki"]:
        p = norm(kf["podpis"])
        if "przyrostu nowych pacjentów" in p:
            W.por(Z, K, "kafelek pacjentów", "udział nowych kampanii w przyroście = słupki pacjentów", kf["liczba"], f"{pl(udz)}%",
                  norm(kf["liczba"]) == f"{pl(udz)}%", "wykres kroku 2")
            W.w_tekscie(Z, K, "kafelek pacjentów", "udział według sesji z płatnością w tekście kroku 2", l1(kf["dopisek"]) and f"{pl(l1(kf['dopisek']))}% przyrostu",
                        kp["tekst"])
        elif "zostaje w ciągu 180 dni" in p:
            W.w_tekscie(Z, K, "kafelek na pacjencie", "kwota na pacjencie nowych kampanii w odpowiedzi kroku 4", f"180 dni {norm(kf['liczba'])}", kn["tekst"])
            W.w_tekscie(Z, K, "kafelek na pacjencie", "kwota pozostałych kampanii płatnych w odpowiedzi kroku 4", f"płatnych {pl(l1(kf['dopisek']))} zł", kn["tekst"])
        elif "wraca w ciągu 90 dni" in p:
            W.por(Z, K, "kafelek powrotu", "powrót 90 dni (ostatnie 12 miesięcy) = hantel 90 dni", kf["liczba"], h90["b"], zaokr(l1(h90["b"])) == l1(kf["liczba"]), "hantle kroku 3")
            W.por(Z, K, "kafelek powrotu", "powrót 90 dni (rok wcześniej) = hantel 90 dni", kf["dopisek"], h90["a"], zaokr(l1(h90["a"])) == l1(kf["dopisek"]), "hantle kroku 3")
        elif "przyrostu marży to zakupy" in p:
            W.por(Z, K, "kafelek marży", "udział pacjentów z pierwszego roku = słupki marży (zaokrąglony)", kf["liczba"], f"{pl(100 * baza / (m2 - m1))}%",
                  norm(kf["liczba"]) == f"{pl(100 * baza / (m2 - m1))}%", "wykres kroku 5")
            W.w_tekscie(Z, K, "kafelek marży", "zmiana wyniku pacjentów pozyskanych w danym roku w werdykcie", f"tylko o {pl(abs(l1(kf['dopisek'])))}%", kw["tekst"])
        else:
            W.niedasie(Z, "kafelki werdyktu", f"nierozpoznany kafelek „{kf['liczba']} {kf['podpis']}”")
    K = "werdykt (zdanie główne)"
    W.w_tekscie(Z, K, "zdanie główne", "udział nowych kampanii w przyroście pacjentów = słupki kroku 2", f"({pl(udz)}%)", kw["tekst"])
    W.w_tekscie(Z, K, "zdanie główne", "wzrost nowych pacjentów = słupki kroku 2", f"o {pl(100 * (raz2 / raz1 - 1))}% więcej", kw["tekst"])
    W.w_tekscie(Z, K, "zdanie główne", "wzrost bez nowych kampanii = słupki kroku 2", f"tylko o {pl(100 * (poz2 / raz1 - 1))}%", kw["tekst"])
    W.w_tekscie(Z, K, "zdanie główne", "przyrost marży w procentach = wykres kroku 5 (zaokrąglony)", f"o {pl(100 * (m2 / m1 - 1))}%", kw["tekst"])
    W.w_tekscie(Z, K, "zdanie główne", "przyrost marży w tytule kroku 5", f"+{pl(100 * (m2 / m1 - 1))}%", kmz["tytul"], "tytuł kroku 5")


def hantle_powrotu(W, Z, K, f, t):
    """Hantle powrotu w 30/60/90/180 dniach wobec tabeli karty (kolumny dobrane po nagłówkach)."""
    ia, ib, iz = kolumna(t, "Rok wcześniej"), kolumna(t, "Ostatnie 12 miesięcy"), kolumna(t, "Zmiana")
    for w in f["wiersze"]:
        dni = re.search(r"(\d+) dni", w["etykieta"]).group(1)
        r = wiersz_tab(t, f"{dni} dni")
        n = re.search(r"rok wcześniej ([\d,]+%) z ([\d ]+) pacjentów, ostatnie 12 miesięcy ([\d,]+%) z ([\d ]+) pacjentów", norm(w["tytul"]))
        W.rowne(Z, K, "hantle powrotu", f"{dni} dni: rok wcześniej", w["a"], proc_z(r["komorki"][ia]["t"]))
        W.rowne(Z, K, "hantle powrotu", f"{dni} dni: ostatnie 12 miesięcy", w["b"], proc_z(r["komorki"][ib]["t"]))
        W.rowne(Z, K, "hantle powrotu", f"{dni} dni: zmiana", w["zm"], r["komorki"][iz]["zm"] or r["komorki"][iz]["t"])
        W.por(Z, K, "hantle powrotu", f"{dni} dni: liczba pacjentów w podpowiedzi (rok wcześniej, ostatnie 12 miesięcy)",
              f"{n.group(2)}, {n.group(4)}", f"{pl(liczby(r['komorki'][ia]['t'])[1])}, {pl(liczby(r['komorki'][ib]['t'])[1])}",
              (l1(n.group(2)), l1(n.group(4))) == (liczby(r["komorki"][ia]["t"])[1], liczby(r["komorki"][ib]["t"])[1]))


def schodki_mostka(W, Z, K, f, t, tekst):
    """Schodki mostka wobec tabeli mostka: wartość po każdym kroku, „bez zmian”, para wartości w podpowiedzi."""
    miara, ostatnie = None, {}
    for w in f["wiersze"]:
        if "wk-grupa-tytul" in w["klasa"]:
            miara = w["tekst"]
            ic = kolumna(t, miara)
            continue
        r = wiersz_tab(t, w["etykieta"])
        kom = r["komorki"][ic]
        wart = norm(w["tekst"]).replace(norm(w["etykieta"]), "").replace("bez zmian", "").strip()
        para = re.search(r"\(([^()]*)\)$", norm(w["tytul"])).group(1)
        if norm(kom["t"]) == "bez zmian":
            W.por(Z, K, "schodki mostka", f"{miara}, {w['etykieta']}: „bez zmian” na wykresie i w tabeli", "bez zmian" if w["bez"] else "BRAK „bez zmian”",
                  "bez zmian", w["bez"], "tabela karty")
            W.rowne(Z, K, "schodki mostka", f"{miara}, {w['etykieta']}: poziom = poprzedni krok w tabeli", wart, ostatnie[miara][0])
            W.rowne(Z, K, "schodki mostka", f"{miara}, {w['etykieta']}: wartości w podpowiedzi = poprzedni krok w tabeli", para, ostatnie[miara][1])
        else:
            W.por(Z, K, "schodki mostka", f"{miara}, {w['etykieta']}: bez napisu „bez zmian”", "bez zmian" if w["bez"] else "—", "—", not w["bez"], "tabela karty")
            W.rowne(Z, K, "schodki mostka", f"{miara}, {w['etykieta']}: wzrost rok do roku", wart, kom["strong"])
            W.rowne(Z, K, "schodki mostka", f"{miara}, {w['etykieta']}: wartości w podpowiedzi", para, kom["przypis"])
            ostatnie[miara] = (kom["strong"], kom["przypis"])
    # zaokrąglone liczby z tekstu karty: zamówienia i przychód po oczyszczeniu wobec dashboardu
    pierwszy = {m: None for m in ostatnie}
    for w in f["wiersze"]:
        if "wk-grupa-tytul" in w["klasa"]:
            miara = w["tekst"]
        elif pierwszy.get(miara) is None:
            pierwszy[miara] = l1(norm(w["tekst"]).replace(norm(w["etykieta"]), ""))
    for m_, (ost, _) in ostatnie.items():
        for v in (pierwszy[m_], l1(ost)):
            W.w_tekscie(Z, K, "schodki mostka", f"{m_}: zaokrąglony wzrost w tekście karty", f"{pl(v)}%", tekst)


# ------------------------------------------------------------------ zakładka „Kohorty”
def kontrola_kohorty(W, karty, stany_mapy, zdarzenia, tabela_okien=None):
    Z = NAZWY["kohorty"]
    kn = karta(karty, id="ko-naglowek")
    f = wyk(kn, "hantle")
    hantle_powrotu(W, Z, "nagłówek kohort", f, tab(kn, "Powrót w ciągu"))
    for v in ("17%", "24%", "22%"):
        W.w_tekscie(Z, "nagłówek kohort", "hantle powrotu", "zaokrąglony powrót w 90 dniach w tekście karty", v, kn["tekst"])
    # hantle wobec wiersza „Wszyscy wybrani pacjenci” tabeli grup (liczonej w przeglądarce z danych pacjent po pacjencie):
    # tabela w trybie „wszystkie okna”, wartości i liczebności w podpowiedzi komórki, zmiana w etykiecie (runda G)
    t = tabela_okien
    if not t or not t["wiersze"]:
        W.por(Z, "nagłówek kohort", "hantle powrotu", "tabela grup w trybie „wszystkie okna”", "BRAK", "tabela", False)
    else:
        r = t["wiersze"][0]
        for w in f["wiersze"]:
            dni = re.search(r"(\d+) dni", w["etykieta"]).group(1)
            kom = r["komorki"][kolumna(t, f"{dni} dni")]
            m = re.search(r"Rok wcześniej: ([\d,]+%) z ([\d ]+) pacjentów\. Ostatnie 12 miesięcy: ([\d,]+%) z ([\d ]+) pacjentów", norm(kom["tytul"]))
            n = re.search(r"rok wcześniej ([\d,]+%) z ([\d ]+) pacjentów, ostatnie 12 miesięcy ([\d,]+%) z ([\d ]+) pacjentów", norm(w["tytul"]))
            zr = "tabela grup w karcie „Dzień po dniu”, tryb „wszystkie okna” (wiersz „Wszyscy wybrani pacjenci”, liczona w przeglądarce)"
            if not m:
                W.por(Z, "nagłówek kohort", "hantle powrotu", f"{dni} dni: podpowiedź komórki tabeli", norm(kom["tytul"])[:60] or "BRAK", "wartości", False, zr)
                continue
            W.rowne(Z, "nagłówek kohort", "hantle powrotu", f"{dni} dni: rok wcześniej (procent i pacjenci)", f"{w['a']} z {n.group(2)}", f"{m.group(1)} z {m.group(2)}", zr)
            W.rowne(Z, "nagłówek kohort", "hantle powrotu", f"{dni} dni: ostatnie 12 miesięcy (procent i pacjenci)", f"{w['b']} z {n.group(4)}", f"{m.group(3)} z {m.group(4)}", zr)
            W.rowne(Z, "nagłówek kohort", "hantle powrotu", f"{dni} dni: zmiana w punktach procentowych", norm(w["zm"]).replace(" pkt proc.", ""),
                    norm(kom["zm"]).replace(" pkt proc.", ""), zr)
    # zdanie nad mapą wobec mapy miesięcznej
    km = karta(karty, tabela="ko-macierz")
    t = tab(km, id="ko-macierz")
    zd = km["wniosekMapy"]["t"]
    i90, inn = kolumna(t, "90 dni"), kolumna(t, "Nowi pacjenci")
    wiersze = [(miesiac(x["komorki"][0]["t"]), l1(x["komorki"][inn]["t"]), l1(x["komorki"][i90]["t"]) if l1(x["komorki"][i90]["t"]) is not None else None)
               for x in t["wiersze"]]
    m = re.search(r"wraca około (\d+)% nowych pacjentów, wobec około (\d+)% w kohortach do (\w+) (\d{4})", norm(zd))
    MIES = {"stycznia": 1, "lutego": 2, "marca": 3, "kwietnia": 4, "maja": 5, "czerwca": 6, "lipca": 7, "sierpnia": 8, "września": 9,
            "października": 10, "listopada": 11, "grudnia": 12}
    do = (int(m.group(4)), MIES[m.group(3)])
    wcz = [x for x in wiersze if x[0] <= do and x[2] is not None]
    pozn = [x for x in wiersze if x[0] >= (2026, 3) and x[2] is not None]
    sr = lambda xs: sum(n * p for _, n, p in xs) / sum(n for _, n, _ in xs)
    zr = "mapa kohort (kolumna 90 dni, średnia ważona liczbą pacjentów z wartości w komórkach)"
    W.por(Z, "mapa kohort", "zdanie nad mapą", f"powrót w 90 dniach w kohortach do {m.group(3)} {m.group(4)} ({len(wcz)} miesięcy, {pl(sum(n for _, n, _ in wcz))} pacjentów)",
          f"około {m.group(2)}%", f"{pl(sr(wcz), 1)}%", zaokr(sr(wcz)) == int(m.group(2)), zr)
    W.por(Z, "mapa kohort", "zdanie nad mapą", f"powrót w 90 dniach od marca 2026 ({len(pozn)} miesiące z pełnym oknem, {pl(sum(n for _, n, _ in pozn))} pacjentów)",
          f"około {m.group(1)}%", f"{pl(sr(pozn), 1)}%", zaokr(sr(pozn)) == int(m.group(1)), zr)
    xi = [p for d, _, p in wiersze if d == (2025, 11)][0]
    W.por(Z, "mapa kohort", "zdanie nad mapą", "„od listopada 2025 kohorty wracają rzadziej”: XI 2025 poniżej każdego miesiąca do X 2025",
          f"XI 2025: {pl(xi, 1)}%", f"najniżej do X 2025: {pl(min(p for _, _, p in wcz), 1)}%", xi < min(p for _, _, p in wcz), zr)
    mid = [p for d, _, p in wiersze if (2025, 11) <= d <= (2026, 2)]
    iii = [p for d, _, p in wiersze if d == (2026, 3)][0]
    W.por(Z, "mapa kohort", "zdanie nad mapą", "„od marca 2026 spadek się pogłębia”: III 2026 poniżej każdego miesiąca XI 2025 – II 2026",
          f"III 2026: {pl(iii, 1)}%", f"najniżej XI 2025 – II 2026: {pl(min(mid), 1)}%", iii < min(mid), zr)
    for opis, widoczne, oczek in stany_mapy:
        W.por(Z, "mapa kohort", "zdanie nad mapą", f"stan zdania: {opis}", "widoczne" if widoczne else "ukryte", "widoczne" if oczek else "ukryte",
              widoczne == oczek, "zasada strony: zdanie opisuje tylko mapę miesięczną bez zawężeń")
    # kolumna „Zdarzenia w tej kohorcie”: krótka nazwa zdarzenia w wierszu miesiąca jego daty; zdarzeń jakości danych
    # (godzina bez danych, duplikaty) w mapie nie ma (runda G, uwaga Kuby: nie zmieniły kohort)
    iz = kolumna(t, "Zdarzenia w tej kohorcie")
    lista = {x["id"]: x for x in dane_strony("zdarzenia.js")["D.zdarzenia"]["lista"]}
    for nr, z in sorted(zdarzenia.items()):
        oczek = (z["od"].year, z["od"].month)
        zl = lista.get(z["id"], {})
        naz = norm(zl.get("krotko") or zl.get("tytul") or "")
        gdzie = [miesiac(x["komorki"][0]["t"]) for x in t["wiersze"] if naz and naz in norm(x["komorki"][iz]["t"])]
        if zl.get("obszar") == "jakosc":
            W.por(Z, "mapa kohort", "kolumna „Zdarzenia”", f"zdarzenie {nr} ({z['od']:%d.%m.%Y}, jakość danych) nie stoi w mapie",
                  "BRAK w mapie" if not gdzie else ", ".join(f"{RZYM[m - 1]} {r}" for r, m in gdzie), "BRAK w mapie", not gdzie, "zasada strony (runda G)")
            continue
        W.por(Z, "mapa kohort", "kolumna „Zdarzenia”", f"zdarzenie {nr} ({z['od']:%d.%m.%Y}) „{naz}” w wierszu miesiąca",
              ", ".join(f"{RZYM[m - 1]} {r}" for r, m in gdzie) or "BRAK w mapie", f"{RZYM[oczek[1] - 1]} {oczek[0]}",
              gdzie == [oczek], "karty zdarzeń w zakładce „Zdarzenia”, nazwy z zdarzenia.js")


# ------------------------------------------------------------------ zakładka „Lejek”
def raport_d_kampanie():
    """Wiersze „okres 2” z tabeli V1 punktu 1 raportu d_kampanie.txt: {grupa: (proc_wbud, proc_oczekiwany, roznica_pkt, sesje)}."""
    out, w_v1 = {}, False
    with open(os.path.join(WYNIKI, "d_kampanie.txt"), encoding="utf-8") as f:
        for linia in f:
            if re.match(r"\s*V1:", linia):
                w_v1 = True
                continue
            if w_v1 and re.match(r"\s*V\d:", linia):
                break
            if w_v1:
                m = re.match(r"\s*(.+?)\s+2\s+(\d+)\s+\d+\s+[\d.]+\s+[\d.]+\s+([\d.]+)\s+([\d.]+)\s+(-?[\d.]+)", linia)
                if m:
                    out[m.group(1).strip()] = (float(m.group(3)), float(m.group(4)), float(m.group(5)), int(m.group(2)))
    return out


def dane_strony(nazwa):
    out = {}
    with open(os.path.join(NARZEDZIE, "dane_strony", nazwa), encoding="utf-8") as f:
        for linia in f:
            poz = linia.find("={")
            if poz >= 0:
                out[linia[:poz].split(";")[-1]] = json.loads(linia[poz + 1:].rstrip().rstrip(";"))
    return out


def kontrola_lejek(W, karty, kroki_stany):
    Z = NAZWY["lejek"]
    # 1. Safari: hantle wobec tekstu karty (wartości i okresy)
    ks = karta(karty, wykres="hantle")
    f, K = wyk(ks, "hantle"), "Safari (karta naprawy)"
    tekst, prz = norm(ks["tekst"]), norm(f["przypis"])
    # runda F, poprawka 5: oba wiersze na tych samych oknach (60 dni przed awarią i po niej); przypis podaje też poziom
    # Safari do końca danych
    m_ok = re.search(r"Przed awarią: (\S+)–(\S+)\. Po awarii: (\S+)–(\S+)\.", prz)
    okresy = m_ok.groups() + m_ok.groups()[2:] if m_ok else ("?",) * 6
    m_kon = re.search(r"Do końca danych krok w Safari nie wraca: ([\d,]+)% od (\S+) do (\S+)\.", prz)
    m60 = re.search(r"W 60 dniach przed awarią i po niej: ([\d,]+)% \((\S+)–(\S+), [\d ]+ sesj\w*\) i ([\d,]+)% \((\S+)–(\S+), [\d ]+ sesj\w*\); "
                    r"pozostałe przeglądarki w tych samych dniach ([\d,]+)% i ([\d,]+)%", tekst)
    mcal = re.search(r"([\d,]+)% od (\S+) do (\S+) i ([\d,]+)% od (\S+) do (\S+?) \(", tekst)
    wart = {}   # (grupa, od, do) -> wartość z tekstu
    if m60:
        g = m60.groups()
        wart[("Safari", g[1], g[2])], wart[("Safari", g[4], g[5])] = l1(g[0]), l1(g[3])
        wart[("Pozostałe", g[1], g[2])], wart[("Pozostałe", g[4], g[5])] = l1(g[6]), l1(g[7])
    if mcal:
        g = mcal.groups()
        rok = g[5][-4:]
        wart[("Safari", g[1] if g[1].count(".") == 2 else g[1] + "." + rok, g[2])] = l1(g[0])
        wart[("Safari", g[4] if g[4].count(".") == 2 else g[4] + "." + rok, g[5])] = l1(g[3])
    wsk = {"Safari na iPhone'ach": [("Safari", okresy[0], okresy[1]), ("Safari", okresy[2], okresy[3])],
           "Pozostałe przeglądarki": [("Pozostałe", okresy[0], okresy[1]), ("Pozostałe", okresy[4], okresy[5])]}
    for w in f["wiersze"]:
        for strona, (klucz, napis) in zip(("przed awarią", "po awarii"), zip(wsk[w["etykieta"]], (w["a"], w["b"]))):
            v = wart.get(klucz)
            W.por(Z, K, "hantle Safari", f"{w['etykieta']}, {strona} ({klucz[1]}–{klucz[2]}, okres z przypisu wykresu)", napis,
                  f"{pl(v, 1)}%" if v is not None else "BRAK wartości dla tego okresu w tekście", v is not None and f"{pl(v)}%" == norm(napis),
                  "tekst karty (Szczegóły), ten sam okres")
        W.por(Z, K, "hantle Safari", f"{w['etykieta']}: zmiana = różnica podpisanych wartości", w["zm"], f"{pl(l1(w['b']) - l1(w['a']))} pkt proc.",
              l1(w["zm"]) == l1(w["b"]) - l1(w["a"]), "rachunek")
    sa = f["wiersze"][0]
    W.w_tekscie(Z, K, "hantle Safari", "Safari przed awarią w zdaniu głównym karty", sa["a"], ks["tekst"])
    W.w_tekscie(Z, K, "hantle Safari", "Safari po awarii w zdaniu głównym karty", sa["b"], ks["tekst"])
    W.por(Z, K, "hantle Safari", "oba wiersze na tych samych oknach (przypis wykresu)", f"{okresy[0]}–{okresy[1]} i {okresy[2]}–{okresy[3]}",
          "60 dni przed awarią i 60 dni po niej, jak w tekście karty", bool(m_ok and m60) and
          (okresy[0], okresy[1], okresy[2], okresy[3]) == (m60.group(2), m60.group(3), m60.group(5), m60.group(6)), "tekst karty (Szczegóły)")
    kl = ("Safari", m_kon.group(2), m_kon.group(3)) if m_kon else None
    W.por(Z, K, "hantle Safari", "przypis: Safari do końca danych = tekst karty, ten sam okres", m_kon.group(1) + "%" if m_kon else "BRAK",
          f"{pl(wart[kl], 1)}%" if kl in wart else "BRAK wartości dla tego okresu w tekście",
          bool(m_kon) and kl in wart and l1(m_kon.group(1)) == wart[kl], "tekst karty (Szczegóły)")
    # 2. przeglądarki w aplikacjach: hantle wobec tekstu karty i raportu d_kampanie.txt
    kb = next(k for k in karty if any("hantle-grupy" in x["klasa"] for x in k["wykresy"]))
    f, K = next(x for x in kb["wykresy"] if "hantle-grupy" in x["klasa"]), "przeglądarki w aplikacjach"
    rd = raport_d_kampanie()
    MAPA = {"Remarketing Meta": "remarketing Meta (meta_rmkt_koszyk)", "Google Ads na markę": "Google Ads marka (gs_brand)",
            "Wejścia bezpośrednie": "wejścia bezpośrednie", "Kampania Meta na L4": "nowe: Meta na L4", "Kampania TikTok na L4": "nowe: TikTok na L4"}
    tekst = norm(kb["tekst"])
    for w in f["wiersze"]:
        if "wk-podtytul" in w["klasa"]:
            continue
        r = rd.get(MAPA.get(w["etykieta"], ""))
        zr = "analiza/wyniki/d_kampanie.txt, punkt 1, V1, okres 2"
        n = re.search(r"w aplikacji ([\d,]+%) z ([\d ]+) sesji, zwykłe przeglądarki w tych samych warunkach ([\d,]+%); różnica ([+-]?[\d,]+) pkt proc\.", norm(w["tytul"]))
        if r is None:
            W.por(Z, K, "hantle przeglądarek", f"{w['etykieta']}: wiersz raportu", w["etykieta"], "BRAK", False, zr)
            continue
        W.rowne(Z, K, "hantle przeglądarek", f"{w['etykieta']}: zwykłe przeglądarki w tych samych warunkach", w["a"], f"{pl(r[1], 1)}%", zr)
        W.rowne(Z, K, "hantle przeglądarek", f"{w['etykieta']}: przeglądarka w aplikacji", w["b"], f"{pl(r[0], 1)}%", zr)
        W.rowne(Z, K, "hantle przeglądarek", f"{w['etykieta']}: różnica", norm(w["zm"]).replace(" pkt proc.", ""), ("+" if r[2] > 0 else "") + pl(r[2], 1), zr)
        W.rowne(Z, K, "hantle przeglądarek", f"{w['etykieta']}: sesje w aplikacji (podpowiedź)", n.group(2), pl(r[3]), zr)
        if w["etykieta"] in ("Remarketing Meta", "Google Ads na markę", "Wejścia bezpośrednie"):
            W.w_tekscie(Z, K, "hantle przeglądarek", f"{w['etykieta']}: różnica w tekście karty", pl(abs(l1(w["zm"])), 1) + " punktu", tekst)
            W.w_tekscie(Z, K, "hantle przeglądarek", f"{w['etykieta']}: sesje w aplikacji w tekście karty", n.group(2), tekst)
        else:
            nazwa = "Meta na L4" if "Meta" in w["etykieta"] else "TikTok"
            mt = re.search(re.escape(nazwa) + r" ([\d,]+)% z ([\d ]+)(?: sesji)? wobec ([\d,]+)% z ([\d ]+)", tekst)
            if mt:
                W.por(Z, K, "hantle przeglądarek", f"{w['etykieta']}: w aplikacji = tekst karty po zaokrągleniu", w["b"], mt.group(1) + "%",
                      f"{pl(l1(mt.group(1)), 1)}%" == norm(w["b"]), "tekst karty (Szczegóły)")
                W.por(Z, K, "hantle przeglądarek", f"{w['etykieta']}: zwykłe przeglądarki = tekst karty po zaokrągleniu", w["a"], mt.group(3) + "%",
                      f"{pl(l1(mt.group(3)), 1)}%" == norm(w["a"]), "tekst karty (Szczegóły)")
                W.rowne(Z, K, "hantle przeglądarek", f"{w['etykieta']}: sesje w aplikacji", n.group(2), mt.group(2), "tekst karty (Szczegóły)")
            else:
                W.por(Z, K, "hantle przeglądarek", f"{w['etykieta']}: liczby w tekście karty", w["b"], "BRAK", False)
    zakres = re.search(r"różnica wynosi (\d+)–(\d+) punktów", tekst)
    rz = [abs(l1(w["zm"])) for w in f["wiersze"] if w["etykieta"] in ("Remarketing Meta", "Google Ads na markę", "Wejścia bezpośrednie")]
    W.por(Z, K, "hantle przeglądarek", "zakres różnic w zdaniu głównym = zaokrąglone skrajne różnice z wykresu", f"{pl(min(rz), 1)}–{pl(max(rz), 1)}",
          zakres.group(0) if zakres else "BRAK", bool(zakres) and (zaokr(min(rz)), zaokr(max(rz))) == (int(zakres.group(1)), int(zakres.group(2))))
    # 3. udział nowych kampanii: kolumny wobec tabeli w karcie nagłówka i niezależnego rachunku na pliku danych
    ku = karta(karty, id="lj-udzial-karta")
    f, K = wyk(ku, "kolumny"), "udział nowych kampanii"
    kn = karta(karty, id="lj-naglowek")
    t = tab(kn, "Udział sesji nowych kampanii")
    iu = kolumna(t, "Udział sesji nowych kampanii")
    P = dane_strony("podsumowanie.js")["D.P"]
    L = dane_strony("lejek_kampania.js")['D.lejek["kampania"]']
    nowe = set(P["etykiety"]["nowe_kampanie"])
    start = dt.date.fromisoformat(L["start"])
    mies = {}
    for s in L["serie"]:
        if s.get("typ") != "zwykla" or s.get("pacjent") != "nie_kupowal" or not s.get("s"):
            continue
        for i, v in enumerate(s["s"]):
            if v:
                d = start + dt.timedelta(days=i)
                x = mies.setdefault((d.year, d.month), [0, 0])
                x[1] += v
                if s["w"] in nowe:
                    x[0] += v
    udzial = {}
    for w in f["wiersze"]:
        m = re.match(r"(\S+ \d{4}): ([\d,]+)% \(([\d ]+) z ([\d ]+) sesji\)", norm(w["tytul"]))
        d = miesiac(m.group(1))
        udzial[d] = l1(m.group(2))
        nowe_n, wsz = mies.get(d, (0, 0))
        zr = "rachunek w Pythonie na narzedzie/dane_strony/lejek_kampania.js (sesje zwykłe, jeszcze nie kupowali)"
        W.por(Z, K, "kolumny udziału", f"{m.group(1)}: sesje nowych kampanii i wszystkie (podpowiedź)", f"{m.group(3)} z {m.group(4)}",
              f"{pl(nowe_n)} z {pl(wsz)}", (l1(m.group(3)), l1(m.group(4))) == (nowe_n, wsz), zr)
        if w["podpisy"] and w["podpisy"][0]:
            W.rowne(Z, K, "kolumny udziału", f"{m.group(1)}: podpis kolumny = podpowiedź", w["podpisy"][0], m.group(2) + "%", "podpowiedź wykresu")
        r = wiersz_tab(t, m.group(1))
        if r is not None:
            kom = norm(r["komorki"][iu]["t"])
            ok = kom == norm(m.group(2) + "%") or (kom == "—" and l1(m.group(2)) == 0)
            W.por(Z, K, "kolumny udziału", f"{m.group(1)}: udział = tabela miesięcy w karcie nagłówka lejka", m.group(2) + "%", kom, ok,
                  "tabela w karcie nagłówka lejka (Szczegóły)")
    tn = norm(kn["tekst"])
    m = re.search(r"przekroczyły 30% ruchu nowych osób w lutym 2026 \(([\d,]+)%\), a od kwietnia to (\d+)–(\d+)%", tn)
    if m:
        W.por(Z, K, "kolumny udziału", "luty 2026 w tekście nagłówka = kolumna II 2026", m.group(1) + "%", f"{pl(udzial[(2026, 2)], 1)}%",
              l1(m.group(1)) == udzial[(2026, 2)] and udzial[(2026, 1)] < 30 < udzial[(2026, 2)], "kolumny wykresu")
        od_kw = [v for d, v in udzial.items() if d >= (2026, 4)]
        W.por(Z, K, "kolumny udziału", "„od kwietnia 42–47%” = zaokrąglone skrajne kolumny IV–IX 2026", f"{m.group(2)}–{m.group(3)}%",
              f"{pl(min(od_kw), 1)}–{pl(max(od_kw), 1)}%", (zaokr(min(od_kw)), zaokr(max(od_kw))) == (int(m.group(2)), int(m.group(3))), "kolumny wykresu")
    else:
        W.niedasie(Z, "kolumny udziału", "zdanie o progu 30% i zakresie od kwietnia nie znalezione w tekście nagłówka lejka")
    # 4. kroki lejka wobec tabeli „Kroki lejka w podziale” (ten sam wiersz)
    for opis, kroki, tl in kroki_stany:
        kroki_lejka(W, Z, opis, kroki, tl)


def kroki_lejka(W, Z, opis, kroki, t):
    """Wykres kroków lejka wobec wiersza tej samej wartości w tabeli grup w trybie „wszystkie kroki” (runda G): w komórce
    zmiana, w podpowiedzi odsetek i mianownik w obu okresach. Kroki dopasowane po kolejności (kolumny od drugiej po
    liczebności do „Sesja do płatności”), bo nazwy kroków na wykresie i w tabeli mogą się różnić."""
    K = "kroki lejka"
    wartosc = "Wszystkie wybrane sesje" if opis.startswith("Razem") else opis
    # pierwsza komórka: nazwa, czasem „mała grupa” i liczebność na telefon („Sesje…: …”), sklejone bez spacji
    r = wiersz_tab(t, wartosc, przez=lambda s: re.split(r"Sesje( na kroku „[^”]*”)?:", norm(s))[0].replace("mała grupa", "").strip())
    zr = f"tabela „Kroki lejka w podziale”, wiersz „{wartosc}”"
    if r is None:
        W.por(Z, K, "wykres kroków", f"{opis}: wiersz tabeli", wartosc, "BRAK", False, zr)
        return
    nag = [norm(h) for h in t["naglowki"][-1]]
    isp = nag.index("Sesja do płatności")
    kol = list(range(2, isp))
    etapy = [x for x in kroki if "lk-krok" in x["klasa"]]
    przejscia = [x for x in kroki if "lk-przejscie" in x["klasa"]]
    nazwa = lambda x: norm(x["nazwa"]).replace(norm(x["n"]), "").strip()

    def wart(kom):   # (odsetek B, mianownik B, odsetek A) z podpowiedzi komórki
        m = re.search(r"Rok wcześniej: ([\d,]+%|—) z ([\d ]+) sesji\. Ostatnie 12 miesięcy: ([\d,]+%) z ([\d ]+) sesji", norm(kom["tytul"]))
        return (m.group(3), l1(m.group(4)), m.group(1)) if m else (None, None, None)
    W.por(Z, K, "wykres kroków", f"{opis}: liczba kroków = wejście + kolumny kroków w tabeli", len(etapy), len(kol) + 1, len(etapy) == len(kol) + 1, zr)
    W.rowne(Z, K, "wykres kroków", f"{opis}: sesje w późniejszym okresie (pierwszy krok)", pl(l1(etapy[0]["n"])),
            pl(l1(norm(r["komorki"][1]["t"]).split("→")[-1])), zr)
    for i, (x, ic) in enumerate(zip(przejscia, kol)):
        nw, nt = nazwa(etapy[i + 1]), nag[ic]
        if nw != nt:
            W.niedasie(Z, "wykres kroków", f"ten sam krok ma dwie nazwy: na wykresie kroków „{nw}”, w tabeli i w polu „Miara” „{nt}” (dopasowane po kolejności)")
        kom = r["komorki"][ic]
        pB, mB, pA = wart(kom)
        W.rowne(Z, K, "wykres kroków", f"{opis}: {nt}: przechodzi dalej (ostatnie 12 miesięcy)", x["dalej"], pB, zr)
        W.rowne(Z, K, "wykres kroków", f"{opis}: {nt}: przechodzi dalej (rok wcześniej)", proc_z(x["dalejA"]), proc_z(pA), zr)
        W.rowne(Z, K, "wykres kroków", f"{opis}: {nt}: zmiana w punktach procentowych", norm(x["zm"]).replace(" pkt proc.", ""),
                norm(kom["zm"]).replace(" pkt proc.", ""), zr)
        n = l1(etapy[i + 1]["n"])
        if i + 1 < len(kol):
            _, mn, _ = wart(r["komorki"][kol[i + 1]])
            W.por(Z, K, "wykres kroków", f"{opis}: {nt}: sesje w kroku (ostatnie 12 miesięcy) = mianownik kolumny „{nag[kol[i + 1]]}”", pl(n), pl(mn),
                  n == mn, zr)
        else:
            p, mian = l1(pB), mB
            tol = mian * 0.0005 + 0.5
            W.por(Z, K, "wykres kroków", f"{opis}: {nt}: sesje w kroku (ostatnie 12 miesięcy) = odsetek × mianownik z tabeli (tabela nie podaje licznika)",
                  pl(n), f"{pl(p * mian / 100)} ± {pl(tol)}", abs(n - p * mian / 100) <= tol, zr + ", w granicach zaokrąglenia odsetka")
    pB, _, pA = wart(r["komorki"][isp])
    W.rowne(Z, K, "wykres kroków", f"{opis}: ostatni krok jako odsetek sesji (ostatnie 12 miesięcy) = „Sesja do płatności”", etapy[-1]["b"], pB, zr)
    W.rowne(Z, K, "wykres kroków", f"{opis}: ostatni krok jako odsetek sesji (rok wcześniej) = „Sesja do płatności”", proc_z(etapy[-1]["a"]), proc_z(pA), zr)


# ------------------------------------------------------------------ zakładka „Po zakupie”
def kontrola_po_zakupie(W, karty, ruch_stany):
    Z = NAZWY["po-zakupie"]
    kg = karta(karty, id="pz-karta-godziny")
    t = tab(kg, id="pz-godziny")
    K = "opóźnienia według godziny"
    kol = {norm(h): i for i, h in enumerate(t["naglowki"][-1])}
    godz = {}
    for f in kg["wykresy"]:
        grupa = "Internista" if "Internista" in f["opis"] else "Pozostali lekarze"
        for w in f["wiersze"]:
            m = re.match(r"(\d+:\d+–\d+:\d+), [^:]+: rok wcześniej ([\d,]+%) \((\d+) z ([\d ]+) wizyt\), ostatnie 12 miesięcy ([\d,]+%) \((\d+) z ([\d ]+) wizyt\)(; blok poranny)?$",
                         norm(w["tytul"]))
            if not m:
                W.por(Z, K, f"kolumny: {grupa}", "podpowiedź kolumny w oczekiwanym kształcie", w["tytul"], "„rok wcześniej X% (k z n wizyt), …”", False)
                continue
            h = m.group(1)
            godz[(grupa, h)] = {"A": (l1(m.group(2)), l1(m.group(3)), l1(m.group(4))), "B": (l1(m.group(5)), l1(m.group(6)), l1(m.group(7)))}
            r = wiersz_tab(t, h)
            for okr, iA, nazwa in (("A", 2, "rok wcześniej"), ("B", 5, "ostatnie 12 miesięcy")):
                kom = r["komorki"][kol[f"{grupa}, {nazwa}"]]["t"]
                na_w = f"{m.group(iA)} ({m.group(iA + 2)})"
                W.rowne(Z, K, f"kolumny: {grupa}", f"{h}, {nazwa}: odsetek spóźnionych i liczba wizyt", na_w, kom)
            W.por(Z, K, f"kolumny: {grupa}", f"{h}: podcieniowany blok poranny = wiersz bloku w tabeli", "blok" if m.group(8) else "—",
                  "blok" if "wiersz-blok" in r["klasa"] else "—", bool(m.group(8)) == ("wiersz-blok" in r["klasa"]))
            if grupa == "Internista":
                zm = l1(r["komorki"][kol["Internista: zmiana (punkty procentowe)"]]["t"])
                d = 100 * (l1(m.group(6)) / l1(m.group(7)) - l1(m.group(3)) / l1(m.group(4)))
                W.por(Z, K, "kolumny: Internista", f"{h}: zmiana w tabeli = różnica odsetków z liczb w podpowiedzi", pl(d, 1), pl(zm, 1),
                      pl(d, 1) == pl(zm, 1), "tabela karty (rachunek z liczników w podpowiedzi)")
    tekst = norm(kg["tekst"])
    # zdania tekstu o pojedynczych godzinach i o bloku 6:00–10:59
    for m in re.finditer(r"o (\d+):00: ([\d,]+)% z ([\d ]+) wizyt, rok wcześniej ([\d,]+)% z ([\d ]+)", tekst):
        x = godz.get(("Internista", f"{m.group(1)}:00–{m.group(1)}:59"))
        W.por(Z, K, "kolumny: Internista", f"godzina {m.group(1)}:00 w tekście karty = kolumna", f"{pl(x['B'][0], 1)}% z {pl(x['B'][2])}, rok wcześniej {pl(x['A'][0], 1)}% z {pl(x['A'][2])}",
              f"{m.group(2)}% z {m.group(3)}, rok wcześniej {m.group(4)}% z {m.group(5)}",
              (x["B"][0], x["B"][2], x["A"][0], x["A"][2]) == (l1(m.group(2)), l1(m.group(3)), l1(m.group(4)), l1(m.group(5))), "tekst karty (Szczegóły)")
    blok = [godz[("Internista", f"{h}:00–{h}:59")] for h in range(6, 11)]
    m = re.search(r"od 6:00 do 10:59: od ([\d,]+)% do ([\d,]+)% \(([\d ]+)–([\d ]+) wizyt w godzinie\), rok wcześniej ([\d,]+)–([\d,]+)%", tekst)
    oczek = (min(x["B"][0] for x in blok), max(x["B"][0] for x in blok), min(x["B"][2] for x in blok), max(x["B"][2] for x in blok),
             min(x["A"][0] for x in blok), max(x["A"][0] for x in blok))
    W.por(Z, K, "kolumny: Internista", "6:00–10:59 w tekście karty = skrajne kolumny tych godzin", " ".join(pl(v, 1) for v in oczek),
          " ".join(m.groups()) if m else "BRAK", bool(m) and tuple(l1(g) for g in m.groups()) == oczek, "tekst karty (Szczegóły)")
    mz = re.search(r"Od 6:00 do 10:59 ponad 15 minut po terminie zaczyna się (\d+)–(\d+)% wizyt", tekst)
    W.por(Z, K, "kolumny: Internista", "6:00–10:59 w zdaniu głównym (zaokrąglone)", f"{pl(oczek[0])}–{pl(oczek[1])}%", mz.group(0) if mz else "BRAK",
          bool(mz) and (zaokr(oczek[0]), zaokr(oczek[1])) == (int(mz.group(1)), int(mz.group(2))))
    m = re.search(r"poza 5:00–13:59: ([\d,]+)% z ([\d ]+) wizyt, rok wcześniej ([\d,]+)% z ([\d ]+)", tekst)
    poza = [godz[("Internista", f"{h}:00–{h}:59")] for h in list(range(0, 5)) + list(range(14, 24))]
    sB, nB = sum(x["B"][1] for x in poza), sum(x["B"][2] for x in poza)
    sA, nA = sum(x["A"][1] for x in poza), sum(x["A"][2] for x in poza)
    W.por(Z, K, "kolumny: Internista", "poza 5:00–13:59 w tekście = suma liczników z podpowiedzi kolumn", f"{pl(100 * sB / nB, 1)}% z {pl(nB)}, rok wcześniej {pl(100 * sA / nA, 1)}% z {pl(nA)}",
          (f"{m.group(1)}% z {m.group(2)}, rok wcześniej {m.group(3)}% z {m.group(4)}") if m else "BRAK",
          bool(m) and (pl(100 * sB / nB, 1), nB, pl(100 * sA / nA, 1), nA) == (m.group(1), l1(m.group(2)), m.group(3), l1(m.group(4))), "tekst karty (Szczegóły)")
    # poranny ruch: hantle wobec tabeli karty, w obu stanach przełącznika „Pacjenci”
    for opis, k in ruch_stany:
        f, t = wyk(k, "hantle"), tab(k, id="pz-ruch")
        K = f"poranny ruch ({opis})"
        for w in f["wiersze"]:
            et = re.sub(r" wizyt[ay]?$", "", norm(w["etykieta"]))   # „21–24 wizyty”, „25–28 wizyt” (runda F, P10)
            r = wiersz_tab(t, et)
            kom = r["komorki"][1]
            n = re.search(r"rok wcześniej ([\d,]+%) z ([\d ]+), ostatnie 12 miesięcy ([\d,]+%) z ([\d ]+)$", norm(w["tytul"]))
            ma = re.search(r"([\d,]+%) z ([\d ]+)", norm(kom["a"]))
            W.rowne(Z, K, "hantle ruchu", f"{et}: rok wcześniej (odsetek z liczbą wizyt)", f"{w['a']} z {n.group(2)}", f"{ma.group(1)} z {pl(l1(ma.group(2)))}" if ma else kom["a"])
            W.rowne(Z, K, "hantle ruchu", f"{et}: ostatnie 12 miesięcy (odsetek z liczbą wizyt)", f"{w['b']} z {n.group(4)}", f"{kom['b']} {kom['n']}")
            W.rowne(Z, K, "hantle ruchu", f"{et}: zmiana w punktach procentowych", norm(w["zm"]).replace(" pkt proc.", ""), kom["zm"])
        if opis == "wszyscy pacjenci":
            m = re.search(r"w dni z (\d+–\d+) porannymi wizytami spóźnionych było ([\d,]+)% wizyt rok wcześniej \((\d+) dni\) i ([\d,]+)% w ostatnich 12 miesiącach \((\d+) dni\)",
                          norm(k["tekst"]))
            if m:
                w = next(x for x in f["wiersze"] if norm(x["etykieta"]).startswith(m.group(1)))
                r = wiersz_tab(t, m.group(1))
                W.por(Z, K, "hantle ruchu", f"przykład {m.group(1)} w tekście karty = hantel i tabela (dni z takim ruchem)",
                      f"{w['a']} → {w['b']}; dni {r['komorki'][2]['a'].replace('rok wcześniej: ', '')} i {r['komorki'][2]['b']}",
                      f"{m.group(2)}% → {m.group(4)}%; dni {m.group(3)} i {m.group(5)}",
                      (norm(w["a"]), norm(w["b"]), l1(r["komorki"][2]["a"]), l1(r["komorki"][2]["b"])) == (m.group(2) + "%", m.group(4) + "%", l1(m.group(3)), l1(m.group(5))),
                      "tekst karty (Szczegóły)")


# ------------------------------------------------------------------ zakładka „Zdarzenia” i listy zdarzeń pod wykresami
def zdarzenia_z_kart(karty):
    out = {}
    for k in karty:
        m = re.match(r"(\d+)\. (\d+\.\d+\.\d{4})(?:–(\d+\.\d+\.\d{4}))?$", norm(k["meta"]))
        if k["id"].startswith("zd-") and m:
            out[int(m.group(1))] = {"id": k["id"][3:], "od": data_pl(m.group(2)), "do": data_pl(m.group(3)) if m.group(3) else None,
                                    "obszar": k["obszar"], "tytul": k["tytul"], "napis": norm(k["meta"])[len(m.group(1)) + 2:]}
    return out


def kontrola_zdarzenia(W, karty, zd, start, ndni):
    Z = NAZWY["zdarzenia"]
    po_dacie = sorted(zd.items(), key=lambda x: (x[1]["od"], x[0]))
    W.por(Z, "lista zdarzeń", "numeracja", "numery kart rosną z datą (1, 2, 3, …)", ", ".join(str(n) for n, _ in po_dacie),
          ", ".join(str(i + 1) for i in range(len(po_dacie))), [n for n, _ in po_dacie] == list(range(1, len(po_dacie) + 1)), "daty na kartach zdarzeń")
    ko = karta(karty, id="zd-os-karta")
    for c in ko["chipy"]:
        m = re.match(r"(.+) \((\d+)\)$", norm(c))
        n = sum(1 for z in zd.values() if norm(z["obszar"]) == m.group(1))
        W.por(Z, "oś zdarzeń", "chipy obszarów", f"liczba przy chipie „{m.group(1)}” = karty tego obszaru", m.group(2), n, int(m.group(2)) == n, "karty zdarzeń")
    if ko["os"]:
        s = ko["os"][0]
        szer, lewy, prawy = s["szer"], 130, 16
        nr_x = {}
        for t in s["nr"]:
            nr_x.setdefault(round(t["x"], 1), []).append(t["t"])
        for mk in s["znaczniki"]:
            m = re.match(r"(\d+)\. (\d+\.\d+\.\d{4})(?:–(\d+\.\d+\.\d{4}))?, ([^:]+): (.*)$", norm(mk["aria"]))
            nr = int(m.group(1))
            z = zd.get(nr)
            W.por(Z, "oś zdarzeń", "znacznik", f"zdarzenie {nr}: data i tytuł znacznika = karta", f"{m.group(2)}{'–' + m.group(3) if m.group(3) else ''}: {m.group(5)[:60]}",
                  f"{z['napis']}: {z['tytul'][:60]}" if z else "BRAK karty",
                  bool(z) and m.group(2) == z["napis"].split("–")[0] and norm(m.group(5)) == norm(z["tytul"]), "karty zdarzeń")
            i = (data_pl(m.group(2)) - start).days
            x_oczek = lewy + (szer - lewy - prawy) * i / (ndni - 1)
            W.por(Z, "oś zdarzeń", "znacznik", f"zdarzenie {nr}: położenie na osi = dzień {m.group(2)}", f"x = {mk['x']:.1f}", f"x = {x_oczek:.1f}",
                  abs(mk["x"] - x_oczek) < 0.6, "skala osi (dni od 1.10.2024)")
            W.por(Z, "oś zdarzeń", "numer nad znacznikiem", f"zdarzenie {nr}: numer nad znacznikiem", ", ".join(nr_x.get(round(mk["x"], 1), ["BRAK"])), str(nr),
                  str(nr) in nr_x.get(round(mk["x"], 1), []), "znacznik osi")
    for li in ko["osPion"]:
        m = re.match(r"(\d+)\. (\d+\.\d+\.\d{4}(?:–\d+\.\d+\.\d{4})?)$", norm(li["data"]))
        nr = int(m.group(1))
        z = zd.get(nr)
        W.por(Z, "oś zdarzeń (telefon)", "lista pionowa", f"zdarzenie {nr}: data, obszar i odnośnik = karta",
              f"{m.group(2)}, {li['obszar']}, {li['href']}", f"{z['napis']}, {z['obszar']}, #zdarzenia?z={z['id']}" if z else "BRAK",
              bool(z) and (m.group(2), norm(li["obszar"]), li["href"]) == (z["napis"], norm(z["obszar"]), f"#zdarzenia?z={z['id']}"), "karty zdarzeń")


def kontrola_listy_zdarzen(W, zakl, karty, zd):
    for k in karty:
        for lista in k["listyZd"]:
            for li in lista:
                z = zd.get(li["nr"])
                m = re.match(r"(\d+\.\d+\.\d{4}): (.*)$", norm(li["t"]))
                W.por(NAZWY[zakl], k["tytul"][:50] or k["id"], "lista zdarzeń pod wykresem dziennym", f"zdarzenie {li['nr']}: data i odnośnik = karta zdarzenia",
                      f"{m.group(1)}, {li['href']}", f"{z['napis'].split('–')[0]}, #zdarzenia?z={z['id']}" if z else "BRAK karty",
                      bool(z) and (m.group(1), li["href"]) == (z["napis"].split("–")[0], f"#zdarzenia?z={z['id']}"), "karty zdarzeń")


# ------------------------------------------------------------------ zakładka „Wynik biznesu”
def kontrola_wynik(W, karty, ek_stany):
    Z = NAZWY["wynik"]
    kw = karta(karty, id="wy-karta")
    kq, kc = karta(karty, id="wy-kw-karta"), karta(karty, id="wy-czas-karta")
    f = wyk(kq, "slupki-grup")
    t = tab(kq, id="wy-kwartaly")
    td = tab(kw, "Marża przed kosztem kampanii")
    K = "kwartały"
    kol = {norm(h): i for i, h in enumerate(t["naglowki"][-1])}
    ip, ik, im = kolumna(td, "Marża przed kosztem kampanii"), kolumna(td, "Wydatki na kampanie"), kolumna(td, "Marża po kosztach kampanii")
    for w in f["wiersze"]:
        r = next(x for x in t["wiersze"] if norm(x["komorki"][0]["t"]) == norm(w["etykieta"]))
        c = lambda nazwa: r["komorki"][kol[nazwa]]
        przB = l1(c("Przychód: konsultacje po zwrotach i TelemediGO")["b"]) - l1(c("Koszt lekarza")["b"])
        przA = l1(c("Przychód: konsultacje po zwrotach i TelemediGO")["a"]) - l1(c("Koszt lekarza")["a"])
        mt = re.search(r"marża przed kosztem kampanii ([\d ]+) zł wobec ([\d ]+) zł, wydatki na kampanie ([\d ]+) zł wobec ([\d ]+) zł", norm(w["tytul"]))
        zr = "tabela „Kwartały rok do roku” (przychód minus koszt lekarza)"
        W.por(Z, K, "kwartały", f"{w['etykieta']}: marża przed kosztem kampanii w podpowiedzi = przychód − koszt lekarza z tabeli (oba lata)",
              f"{mt.group(1)} i {mt.group(2)} zł", f"{pl(przB)} i {pl(przA)} zł", abs(l1(mt.group(1)) - przB) <= 1 and abs(l1(mt.group(2)) - przA) <= 1, zr)
        W.por(Z, K, "kwartały", f"{w['etykieta']}: wydatki na kampanie w podpowiedzi = tabela (oba lata)", f"{mt.group(3)} i {mt.group(4)} zł",
              f"{c('Wydatki na kampanie')['b']} i {norm(c('Wydatki na kampanie')['a']).replace('rok wcześniej: ', '')}",
              (l1(mt.group(3)), l1(mt.group(4))) == (l1(c("Wydatki na kampanie")["b"]), l1(c("Wydatki na kampanie")["a"])), "tabela „Kwartały rok do roku”")
        W.por(Z, K, "kwartały", f"{w['etykieta']}: zmiana marży przed kosztem kampanii = rachunek z tabeli", w["sg"][0], f"+{pl(100 * (przB / przA - 1), 1)}%",
              l1(w["sg"][0]) == zaokr(100 * (przB / przA - 1), 1), zr)
        W.rowne(Z, K, "kwartały", f"{w['etykieta']}: zmiana wydatków na kampanie = tabela", w["sg"][1], c("Wydatki na kampanie")["zm"], "tabela „Kwartały rok do roku”")
        rd = wiersz_tab(td, w["etykieta"])
        W.rowne(Z, K, "kwartały", f"{w['etykieta']}: zmiana marży przed kosztem kampanii = tabela z liczbami w karcie", w["sg"][0], rd["komorki"][ip]["zm"])
        W.rowne(Z, K, "kwartały", f"{w['etykieta']}: zmiana wydatków = tabela z liczbami w karcie", w["sg"][1], rd["komorki"][ik]["zm"])
        W.rowne(Z, K, "kwartały", f"{w['etykieta']}: zmiana marży po kosztach kampanii (tabela z liczbami) = tabela kwartałów", rd["komorki"][im]["zm"], c("Marża po wszystkich kosztach")["zm"],
                "tabela „Kwartały rok do roku”")
    # zdania karty wobec tabeli „Miesiące i sumy obu lat”
    ty = tab(kc, id="wy-tabela")
    kol = {norm(h): i for i, h in enumerate(ty["naglowki"][-1])}
    r1, r2 = ty["wiersze"][0]["komorki"], ty["wiersze"][1]["komorki"]
    v = lambda r, n: l1(r[kol[n]]["t"])
    przed = [v(r, "Przychód: pierwsze zamówienia (zł)") + v(r, "Przychód: kolejne zamówienia (zł)") + v(r, "TelemediGO (zł)") - v(r, "Koszt lekarza (zł)") for r in (r1, r2)]
    tekst = norm(kw["tekst"])
    for opis, wart in (("marża przed kosztem kampanii za rok", 100 * (przed[1] / przed[0] - 1)),
                       ("wydatki na kampanie za rok", 100 * (v(r2, "Kampanie (zł)") / v(r1, "Kampanie (zł)") - 1)),
                       ("marża po koszcie lekarza, kampaniach i prowizji za rok", 100 * (v(r2, "Marża (zł)") / v(r1, "Marża (zł)") - 1))):
        W.w_tekscie(Z, "wynik biznesu", "tekst nad wykresami", f"{opis}: zaokrąglona zmiana z tabeli „Miesiące i sumy obu lat” w tekście", f"{pl(wart)}%", tekst,
                    "tekst karty wobec tabeli")
    # ekonomia kampanii: punkty wobec tabeli, we wszystkich stanach przełączników
    tekst_ek = None
    pkt = {}
    for opis, poziom, okres, okno, k in ek_stany:
        tekst_ek = tekst_ek or norm(k["tekst"])
        f, t = wyk(k, "punkty-zero"), tab(k, id="ek-tabela")
        K = f"ekonomia kampanii ({opis})"
        if f is None:
            W.por(Z, K, "punkty wyniku", "brak wykresu: informacja zamiast pustej osi", "informacja" if "dane nie mają wyniku w oknie" in norm(k["tekst"]) else "BRAK",
                  "informacja", "dane nie mają wyniku w oknie" in norm(k["tekst"]), "zasada strony")
            continue
        grupa = 1     # runda G: tabela tylko dla wybranego okna, w grupie reguły kolumny „koszt”, „wynik”
        for w in f["wiersze"]:
            r = wiersz_tab(t, w["etykieta"])
            if r is None:
                W.por(Z, K, "punkty wyniku", f"{w['etykieta']}: wiersz tabeli", w["etykieta"], "BRAK", False)
                continue
            for j, regula in enumerate(("według pierwszego wejścia", "według sesji z płatnością")):
                kom = r["komorki"][1 + 2 * j + grupa]
                W.rowne(Z, K, "punkty wyniku", f"{w['etykieta']}: wynik na pacjenta {regula}, {okno} dni", w["v"][j], kom["b"] or kom["t"])
                pkt[(poziom, okres, okno, w["etykieta"], j)] = l1(w["v"][j])
            znaki = [l1(x) for x in w["v"]]
            rozne = None not in znaki and (znaki[0] >= 0) != (znaki[1] >= 0)
            W.por(Z, K, "punkty wyniku", f"{w['etykieta']}: znacznik „Znak zależy od przypisania” tylko przy różnych znakach",
                  w["uwaga"] or "—", "znacznik" if rozne else "—", bool(w["uwaga"]) == rozne, "rachunek")
            if w["uwaga"]:
                W.por(Z, K, "punkty wyniku", f"{w['etykieta']}: znacznik na wykresie ma ocenę „Niepewny” w tabeli", w["uwaga"], r["komorki"][-1]["t"] or "—",
                      "Niepewny" in r["komorki"][-1]["t"])
    # zdania karty ekonomii
    K = "ekonomia kampanii (tekst karty)"
    for opis, klucz, tok in (("TikTok na L4, pierwsze wejście, 90 dni", ("kampania", 2, 90, "TikTok: L4 w 15 minut", 0), "około {} zł"),
                             ("TikTok na L4, sesja z płatnością, 90 dni", ("kampania", 2, 90, "TikTok: L4 w 15 minut", 1), "około {} zł"),
                             ("obie nowe kampanie, pierwsze wejście, 90 dni", ("grupa", 2, 90, "Nowe kampanie na L4 (Meta i TikTok)", 0), "około {} zł"),
                             ("obie nowe kampanie, sesja z płatnością, 90 dni", ("grupa", 2, 90, "Nowe kampanie na L4 (Meta i TikTok)", 1), "około {} zł")):
        v = pkt.get(klucz)
        if v is None:
            W.niedasie(Z, "ekonomia kampanii", f"brak punktu dla zdania „{opis}” (sprawdź nazwę kampanii)")
            continue
        napis = pl(abs(v)) if "TikTok" in opis else ("+" if v > 0 else "-") + pl(abs(v))
        W.w_tekscie(Z, K, "punkty wyniku", f"{opis}: zaokrąglony punkt w zdaniu głównym", tok.format(napis), tekst_ek)
        W.w_tekscie(Z, K, "punkty wyniku", f"{opis}: dokładny punkt w Szczegółach", ("+" if v > 0 else "") + pl(v, 1) + " zł", tekst_ek)
    for j in (0, 1):
        v = pkt.get(("grupa", 2, 180, "Nowe kampanie na L4 (Meta i TikTok)", j))
        if v is not None:
            W.w_tekscie(Z, K, "punkty wyniku", f"obie nowe kampanie, 180 dni, {'pierwsze wejście' if j == 0 else 'sesja z płatnością'}: punkt w Szczegółach",
                        ("+" if v > 0 else "") + pl(v, 1) + " zł", tekst_ek)


# ------------------------------------------------------------------ zakładka „Jakość danych”
def kontrola_jakosc(W, karty):
    Z = NAZWY["jakosc"]
    km = karta(karty, id="jk-karta-mostek")
    schodki_mostka(W, Z, "mostek dashboardu", wyk(km, "schodki"), tab(km, id="jk-mostek"), km["tekst"])
    kt = karta(karty, id="jk-karta-testy")
    pola = kt["testy"][0][2:]
    kw = [(pola[i], l1(pola[i + 1])) for i in range(0, len(pola), 2)]
    rok = lambda et: (int(et[-4:]), RZYM.index(et.split(" ")[0]) * 3 + 1)
    y1 = sum(n for e, n in kw if (2024, 10) <= rok(e) <= (2025, 7))
    y2 = sum(n for e, n in kw if (2025, 10) <= rok(e) <= (2026, 7))
    tekst = norm(kt["tekst"])
    m = re.search(r"([\d ]+) zamówienia rok wcześniej i ([\d ]+) zamówień w ostatnich 12 miesiącach", tekst)
    W.por(Z, "zamówienia testowe", "słupki kwartałów", "suma kwartałów IV 2024 – III 2025 i IV 2025 – III 2026 = tekst karty", f"{pl(y1)} i {pl(y2)}",
          f"{m.group(1)} i {m.group(2)}" if m else "BRAK", bool(m) and (y1, y2) == (l1(m.group(1)), l1(m.group(2))))
    W.w_tekscie(Z, "zamówienia testowe", "słupki kwartałów", "suma wszystkich kwartałów = liczba zamówień testowych w tekście", f"{pl(sum(n for _, n in kw))} zamówień", tekst)


# ------------------------------------------------------------------ zakładki „Priorytety” i „Czego nie wiemy”
def kontrola_priorytety(W, karty, safari_lejek):
    Z = NAZWY["priorytety"]
    k1 = karta(karty, id="pr-1")
    f = wyk(k1, "hantle")
    for w, s in zip(f["wiersze"], safari_lejek["wiersze"]):
        W.rowne(Z, "pozycja 1", "hantle Safari", f"{w['etykieta']}: przed, po i zmiana = wykres w karcie Safari w lejku", f"{w['a']} → {w['b']}, {w['zm']}",
                f"{s['a']} → {s['b']}, {s['zm']}", "karta Safari w zakładce „Lejek” (tekst tej karty: kontrola w lejku)")
    kp = karta(karty, id="pr-przeglad-karta")
    t = tab(kp, id="pr-przeglad")
    przeg = {}
    for r in t["wiersze"]:
        if "oddzielnik" in r["klasa"]:
            continue
        c = r["komorki"]
        przeg[int(c[0]["t"])] = {"co": c[1]["t"], "ile": c[2]["kwota"], "dop": c[2]["kdop"], "pew": c[3]["znacznik"], "pdop": c[3]["pdop"], "wdr": c[4]["t"]}
    for nr in sorted(przeg):
        k = karta(karty, id=f"pr-{nr}")
        p = k["pasek"][0] if k and k["pasek"] else None
        if p is None:
            W.por(Z, f"pozycja {nr}", "pasek karty", "karta pozycji z paskiem", "—", "BRAK karty", False, "tabela „Przegląd”")
            continue
        W.rowne(Z, f"pozycja {nr}", "pasek karty", "ile warte (kwota i dopisek) = przegląd", f"{p['kwota']} | {p['dopisek']}", f"{przeg[nr]['ile']} | {przeg[nr]['dop']}", "tabela „Przegląd”")
        W.rowne(Z, f"pozycja {nr}", "pasek karty", "pewność = przegląd", f"{p['pewnosc']} | {p['pdop']}", f"{przeg[nr]['pew']} | {przeg[nr]['pdop']}", "tabela „Przegląd”")
        W.rowne(Z, f"pozycja {nr}", "pasek karty", "wdrożenie = przegląd", p["wdrozenie"], przeg[nr]["wdr"], "tabela „Przegląd”")
    for pg in kp["pigulki"]:
        nr = int(pg["t"])
        W.por(Z, "przegląd", "pigułki", f"pigułka {nr}: odnośnik i nazwa = pozycja listy", f"{pg['href']} | {pg['tytul']}", f"#priorytety?p={nr} | {przeg.get(nr, {}).get('co')}",
              pg["href"] == f"#priorytety?p={nr}" and norm(pg["tytul"]) == norm(przeg.get(nr, {}).get("co", "")), "tabela „Przegląd”")
    return przeg


def kontrola_niewiadome(W, t, przeg):
    Z = NAZWY["niewiadome"]
    ip = kolumna(t, "Pozycja listy priorytetów")
    # runda G: nagłówki grup tematycznych to wiersze „oddzielnik” z jedną komórką; każdy numer pytania raz
    nry = [norm(r["komorki"][0]["t"]) for r in t["wiersze"] if "oddzielnik" not in r["klasa"]]
    W.por(Z, "tabela", "grupy tematyczne", "każde pytanie raz, numery 1…N", ", ".join(sorted(nry, key=int)),
          ", ".join(str(i) for i in range(1, len(nry) + 1)), sorted(int(x) for x in nry) == list(range(1, len(nry) + 1)), "dane c.js")
    for r in t["wiersze"]:
        if "oddzielnik" in r["klasa"]:
            continue
        kom = r["komorki"][ip]
        if not kom["href"]:
            continue
        nr = int(kom["href"].split("=")[1])
        W.rowne(Z, f"punkt {r['komorki'][0]['t']}", "kolumna pozycji", "numer i nazwa pozycji = przegląd priorytetów", kom["link"], f"{nr}. {przeg[nr]['co']}",
                "tabela „Przegląd” w zakładce „Priorytety”")


# ------------------------------------------------------------------ „Kohorty”: tabela „co zmieniło kohorty i wynik” (runda F, poprawka 1)
# zapisy liczb w komórce: daty, godziny, odsetki, kwoty, zakresy i liczby (bez cyfr w nazwach typu „L4”); długość okna
# („w 90 dniach”, „ostatnich 12 miesięcy”) to część nazwy miary i też musi stać w karcie źródłowej
ZAPISY = [re.compile(r"\d{1,2}\.\d{2}\.\d{4}"), re.compile(r"\d{1,2}:\d{2}"),
          re.compile(r"[+-]?\d{1,3}(?: \d{3})*(?:,\d+)?(?:–\d{1,3}(?: \d{3})*(?:,\d+)?)?(?: tys\.)? zł"),
          re.compile(r"[+-]?\d+(?:,\d+)?(?:–\d+(?:,\d+)?)?%"), re.compile(r"(?<![\w,.])\d{1,3}(?: \d{3})+(?![\d,])"),
          re.compile(r"(?<![\w,.:–+-])\d+(?:,\d+)?–\d+(?:,\d+)?(?![\d%])"), re.compile(r"(?<![\w,.:–])[+-]?\d+(?:,\d+)?(?![\w%.:–]|,\d)")]


def zapisy_liczb(s):
    t, out = norm(s), []
    for wz in ZAPISY:
        for m in wz.finditer(t):
            out.append(m.group(0).lstrip("+"))
        t = wz.sub(lambda m: "#" * len(m.group(0)), t)
    return out


# źródła liczb dla wierszy tabeli: karty zdarzeń (id), karty innych zakładek (zakładka, tytuł karty albo id), pozycje
# listy priorytetów, pozycja, z której jest skutek w złotych (kwota i dopisek), i pozycja, z której jest pewność
ZRODLA_TABELI = {
    "start_go_upsell": (["start_go_upsell"], [("wynik", "id", "wy-karta")], [], None, None),
    "start_meta_l4": (["start_meta_l4", "udzial_nowych", "start_tiktok", "marza30_spada"], [("kohorty", "id", "ko-naglowek")], [9, 5], 9, 9),
    "zwroty_pierwsze": (["zwroty_pierwsze"], [("po-zakupie", "tytul", "Zwroty po wizycie")], [5], None, 5),
    "opoznienia_rano": (["opoznienia_rano"], [], [6], 6, 6),
    "start_tiktok": (["start_tiktok", "powrot30_spada"], [("wynik", "id", "ek-karta")], [3], 3, 3),
    "powrot90_stare": (["powrot90_stare"], [], [], None, None),
    "safari_ios": (["safari_ios"], [("lejek", "wykres", "hantle")], [1], 1, 1),
    "marka_konwersja": (["marka_konwersja"], [], [], None, None),
}


def kontrola_tabeli_zdarzen(W, D, zd, przeg, nw):
    Z, K = NAZWY["zdarzenia"], "co zmieniło kohorty i wynik"
    kz = karta(D["zdarzenia"]["karty"], id="zd-tabela-karta")
    t = tab(kz, id="zd-tabela") if kz else None
    if not t:
        W.por(Z, K, "tabela zdarzeń", "tabela na górze zakładki", "BRAK", "8 wierszy", False, "dane zdarzenia.js")
        return
    po_id = {z["id"]: z for z in zd.values()}
    karty_zd = {k["id"][3:]: k for k in D["zdarzenia"]["karty"] if k["id"].startswith("zd-") and k["meta"]}
    W.rowne(Z, K, "tabela zdarzeń", "liczba wierszy (8 zdarzeń i decyzji z osi)", str(len(t["wiersze"])), "8", "decyzja Kuby, poprawka 1")
    for r in t["wiersze"]:
        id_ = r["id"][len("zt-"):]
        c = r["komorki"]
        z = po_id.get(id_)
        zr_id, inne, pozycje, nr_skutek, nr_pewnosc = ZRODLA_TABELI.get(id_, ([id_], [], [], None, None))
        zrodla, opis_zr = [], []
        for x in zr_id:
            if x in karty_zd:
                zrodla.append(karty_zd[x]["tekst"])
                opis_zr.append(f"karta zdarzenia {x}")
        for zakl, jak, co in inne:
            k = karta(D[zakl]["karty"], **({"tytul": co} if jak == "tytul" else {"id": co} if jak == "id" else {"wykres": co}))
            if k:
                zrodla.append(k["tekst"])
                opis_zr.append(f"karta „{k['tytul'][:40]}” ({NAZWY[zakl]})")
        for nr in pozycje:
            p = przeg.get(nr, {})
            zrodla.append(" ".join([p.get("co", ""), p.get("ile", ""), p.get("dop", ""), p.get("pew", ""), p.get("pdop", "")]))
            opis_zr.append(f"pozycja {nr} w przeglądzie listy priorytetów")
        zr_tekst, zr_opis = " | ".join(zrodla), "; ".join(opis_zr)
        # data wiersza = data karty zdarzenia
        W.por(Z, K, "tabela zdarzeń", f"{id_}: data w kolumnie „Kiedy” = karta zdarzenia", c[0]["strong"],
              f"{z['od']:%d.%m.%Y}".lstrip("0") if z else "BRAK karty", bool(z) and data_pl(c[0]["strong"]) == z["od"], "karty zdarzeń w zakładce „Zdarzenia”")
        # każda liczba w komórkach 1–6 stoi w karcie źródłowej
        for i, nazwa in ((0, "Kiedy"), (2, "Kogo dotyczy"), (3, "Co zmieniło się po nim"), (4, "Skutek w złotych"), (5, "Pewność")):
            for tok in zapisy_liczb(c[i]["t"]):
                if i == 0 and tok == c[0]["strong"]:
                    continue
                W.w_tekscie(Z, K, "tabela zdarzeń", f"{id_}, kolumna „{nazwa}”: {tok}", tok, zr_tekst, zr_opis)
        # kwota, dopisek i pewność pozycji listy priorytetów: dokładnie jak w przeglądzie
        if nr_skutek:
            p = przeg.get(nr_skutek, {})
            W.rowne(Z, K, "tabela zdarzeń", f"{id_}: skutek = pozycja {nr_skutek} (kwota i dopisek)", f"{c[4]['kwota']} | {c[4]['kdop']}",
                    f"{p.get('ile')} | {p.get('dop')}", "tabela „Przegląd” w zakładce „Priorytety”")
        if nr_pewnosc:
            p = przeg.get(nr_pewnosc, {})
            W.rowne(Z, K, "tabela zdarzeń", f"{id_}: pewność = pozycja {nr_pewnosc}", f"{c[5]['znacznik']} | {c[5]['pdop']}",
                    f"{p.get('pew')} | {p.get('pdop')}", "tabela „Przegląd” w zakładce „Priorytety”")
        # odnośniki: co robimy, kohorty dzienne (60 dni przed i po dacie zdarzenia), opis zdarzenia
        for l in c[6]["linki"]:
            h = l["href"]
            if h.startswith("#priorytety?p="):
                nr = int(h.split("=")[1])
                W.rowne(Z, K, "tabela zdarzeń", f"{id_}: odnośnik do pozycji {nr} (nazwa = przegląd)", l["t"], f"Pozycja {nr}: {przeg.get(nr, {}).get('co')}",
                        "tabela „Przegląd” w zakładce „Priorytety”")
            elif h.startswith("#niewiadome?n="):
                nr = h.split("=")[1]
                W.por(Z, K, "tabela zdarzeń", f"{id_}: odnośnik do „Czego nie wiemy”, punkt {nr}", l["t"], f"punkt {nr}: {nw.get(nr, 'BRAK')[:60]}",
                      nr in nw and l["t"].startswith(f"Czego nie wiemy, punkt {nr}"), "tabela „Czego nie wiemy”")
            elif h.startswith("#kohorty?"):
                q = dict(x.split("=", 1) for x in h.split("?", 1)[1].split("&"))
                if z:
                    d = z["od"]
                    a = (max(dt.date(2024, 10, 1), d - dt.timedelta(days=60)), d - dt.timedelta(days=1))
                    b = (d, min(dt.date(2026, 9, 30), d + dt.timedelta(days=59)))
                    oczek = f"a={a[0]}_{a[1]}, b={b[0]}_{b[1]}"
                else:
                    oczek = "BRAK karty"
                W.rowne(Z, K, "tabela zdarzeń", f"{id_}: „Pokaż na kohortach dziennych” = 60 dni przed i po dacie zdarzenia",
                        f"a={q.get('a')}, b={q.get('b')}", oczek, "data karty zdarzenia")
            elif h.startswith("#zdarzenia?z="):
                W.por(Z, K, "tabela zdarzeń", f"{id_}: „Opis zdarzenia” prowadzi do karty tego zdarzenia", h, f"#zdarzenia?z={id_}",
                      h == f"#zdarzenia?z={id_}" and id_ in karty_zd, "karty zdarzeń w zakładce „Zdarzenia”")
        W.por(Z, K, "tabela zdarzeń", f"{id_}: dwa odnośniki wiersza („Pokaż na kohortach dziennych”, „Opis zdarzenia”)",
              ", ".join(l["t"] for l in c[6]["linki"][-2:]), "Pokaż na kohortach dziennych, Opis zdarzenia",
              [l["t"] for l in c[6]["linki"][-2:]] == ["Pokaż na kohortach dziennych", "Opis zdarzenia"], "decyzja Kuby, poprawka 1")


# ------------------------------------------------------------------ przeglądarka
class CichyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def czekaj(strona, z):
    for sel in GOTOWE[z]:
        strona.wait_for_selector(sel, timeout=30000, state="attached")
    strona.wait_for_timeout(600)


def pokaz(strona, z):
    strona.evaluate(f"location.hash = '{z}'")
    czekaj(strona, z)
    return strona.evaluate(ZBIERZ, z)


def zbierz_szerokosc(strona, adres):
    D, bledy = {}, []
    strona.on("pageerror", lambda e: bledy.append("błąd strony: " + str(e)))
    strona.on("console", lambda m: bledy.append("konsola: " + m.text) if m.type == "error" else None)
    strona.goto(adres + "#wzrost")
    for z in ZAKLADKI:
        D[z] = pokaz(strona, z)
    S = {}
    # kohorty: stany zdania nad mapą
    pokaz(strona, "kohorty")
    stan = lambda: strona.evaluate("() => { const w = document.getElementById('ko-macierz-wniosek'); return !!w && !w.hidden && !!w.textContent.trim(); }")
    stany = [("mapa miesięczna, bez zawężeń (domyślnie)", stan(), True)]
    strona.click("#ko-macierz-filtry button:has-text('tygodniowe')")
    strona.wait_for_timeout(500)
    stany.append(("po przełączeniu na kohorty tygodniowe", stan(), False))
    strona.click("#ko-macierz-filtry button:has-text('dzienne')")
    strona.wait_for_timeout(800)
    stany.append(("po przełączeniu na kohorty dzienne", stan(), False))
    strona.click("#ko-macierz-filtry button:has-text('miesięczne')")
    strona.wait_for_timeout(500)
    stany.append(("po powrocie do kohort miesięcznych", stan(), True))
    wart = strona.evaluate("() => [...document.querySelectorAll('#ko-f-urzadzenie option')].map(o => o.value).filter(Boolean)[0]")
    strona.evaluate("v => { const s = document.getElementById('ko-f-urzadzenie'); s.value = v; s.dispatchEvent(new Event('change')); }", wart)
    strona.wait_for_timeout(1500)
    stany.append((f"z zawężeniem pacjentów (urządzenie = {wart})", stan(), False))
    strona.evaluate("() => { const s = document.getElementById('ko-f-urzadzenie'); s.value = ''; s.dispatchEvent(new Event('change')); }")
    strona.wait_for_timeout(1500)
    stany.append(("po usunięciu zawężenia", stan(), True))
    S["mapa"] = stany
    # kohorty: tabela grup w trybie „wszystkie okna” (wartości w podpowiedziach) do porównania z hantlami wniosku
    strona.click("#ko-tabela-tryb button:has-text('wszystkie okna')")
    strona.wait_for_timeout(800)
    dk = strona.evaluate(ZBIERZ, "kohorty")
    S["kohorty_okna"] = tab(karta(dk["karty"], tabela="ko-tabela"), id="ko-tabela")
    strona.click("#ko-reset")
    strona.wait_for_timeout(800)
    # lejek: kroki dla „Wszystkie wybrane sesje” i dla „Safari”, tabela grup w trybie „wszystkie kroki”
    pokaz(strona, "lejek")
    strona.click("#lj-tabela-tryb button:has-text('wszystkie kroki')")
    strona.wait_for_timeout(1000)
    dl = strona.evaluate(ZBIERZ, "lejek")
    kroki = [("Razem (domyślnie)", karta(dl["karty"], id="lj-kroki-karta")["kroki"], tab(karta(dl["karty"], tabela="lj-tabela"), id="lj-tabela"))]
    strona.select_option("#f-lw", label="Safari")
    strona.wait_for_timeout(1000)
    dl2 = strona.evaluate(ZBIERZ, "lejek")
    kroki.append(("Safari", karta(dl2["karty"], id="lj-kroki-karta")["kroki"], tab(karta(dl2["karty"], tabela="lj-tabela"), id="lj-tabela")))
    strona.click("#lj-reset")
    strona.wait_for_timeout(800)
    S["kroki"] = kroki
    # po zakupie: poranny ruch w obu stanach przełącznika „Pacjenci”
    dp = pokaz(strona, "po-zakupie")
    ruch = [("wszyscy pacjenci", karta(dp["karty"], id="pz-karta-ruch"))]
    strona.select_option("#pz-ruch-grupa", "pozostale")
    strona.wait_for_timeout(600)
    dp2 = strona.evaluate(ZBIERZ, "po-zakupie")
    ruch.append(("pacjenci spoza nowych kampanii", karta(dp2["karty"], id="pz-karta-ruch")))
    strona.select_option("#pz-ruch-grupa", "wszyscy")
    S["ruch"] = ruch
    # wynik biznesu: ekonomia kampanii we wszystkich stanach
    pokaz(strona, "wynik")
    ek = []
    for poziom in ("grupa", "kampania", "kanal"):
        strona.select_option("#ek-poziom", poziom)
        for okres in ("2", "1"):
            strona.select_option("#ek-okres", okres)
            for okno in (90, 180):
                strona.click(f"#ek-karta .przelacznik button:has-text('{okno} dni')")
                strona.wait_for_timeout(400)
                dw = strona.evaluate(ZBIERZ, "wynik")
                ek.append((f"poziom {poziom}, okres {okres}, okno {okno} dni", poziom, int(okres), okno, karta(dw["karty"], id="ek-karta")))
    strona.select_option("#ek-poziom", "grupa")
    strona.select_option("#ek-okres", "2")
    strona.click("#ek-karta .przelacznik button:has-text('90 dni')")
    S["ekonomia"] = ek
    return D, S, bledy


def main():
    sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--silnik", default="msedge", choices=["msedge", "webkit", "firefox"])
    arg = ap.parse_args()
    raport = RAPORT if arg.silnik == "msedge" else RAPORT.replace(".txt", f"_{arg.silnik}.txt")
    obsluga = functools.partial(CichyHandler, directory=NARZEDZIE)
    serw = http.server.ThreadingHTTPServer(("127.0.0.1", 0), obsluga)
    threading.Thread(target=serw.serve_forever, daemon=True).start()
    adres = f"http://127.0.0.1:{serw.server_address[1]}/"
    P = dane_strony("podsumowanie.js")["D.P"]
    start = dt.date.fromisoformat(P["meta"]["start"])
    ndni = (dt.date.fromisoformat(P["meta"]["koniec"]) - start).days + 1
    W = Wynik()
    bledy_razem = {}
    with sync_playwright() as p:
        przegl = p.chromium.launch(channel="msedge", headless=True) if arg.silnik == "msedge" else getattr(p, arg.silnik).launch(headless=True)
        nazwa_silnika = f"{'Edge' if arg.silnik == 'msedge' else 'WebKit (silnik Safari)' if arg.silnik == 'webkit' else 'Firefox'} {przegl.version}"
        for szer, wys, telefon in SZEROKOSCI:
            telefon = telefon and arg.silnik != "firefox"
            # Firefox z Playwrighta bez ustawionego języka zwraca navigator.language = "undefined" i biblioteka wykresów (uPlot)
            # nie wczytuje się; prawdziwy Firefox zawsze ma język, więc ustawiamy polski
            jezyk = {"locale": "pl-PL"} if arg.silnik == "firefox" else {}
            kontekst = przegl.new_context(viewport={"width": szer, "height": wys}, is_mobile=telefon, has_touch=telefon, **jezyk)
            strona = kontekst.new_page()
            D, S, bledy = zbierz_szerokosc(strona, adres)
            bledy_razem[szer] = bledy
            kontekst.close()
            W.szer = szer
            zd = zdarzenia_z_kart(D["zdarzenia"]["karty"])
            kontrola_wzrost(W, D["wzrost"]["karty"])
            kontrola_kohorty(W, D["kohorty"]["karty"], S["mapa"], zd, S.get("kohorty_okna"))
            kontrola_lejek(W, D["lejek"]["karty"], S["kroki"])
            kontrola_po_zakupie(W, D["po-zakupie"]["karty"], S["ruch"])
            kontrola_zdarzenia(W, D["zdarzenia"]["karty"], zd, start, ndni)
            for z in ZAKLADKI:
                kontrola_listy_zdarzen(W, z, D[z]["karty"], zd)
            kontrola_wynik(W, D["wynik"]["karty"], S["ekonomia"])
            kontrola_jakosc(W, D["jakosc"]["karty"])
            przeg = kontrola_priorytety(W, D["priorytety"]["karty"], wyk(karta(D["lejek"]["karty"], wykres="hantle"), "hantle"))
            kontrola_niewiadome(W, D["niewiadome"]["niewiadome"], przeg)
            # tabela „co zmieniło kohorty i wynik” (od rundy G w „Zdarzeniach”) wobec kart zdarzeń, priorytetów i ekonomii kampanii
            nw = {norm(r["komorki"][0]["t"]): norm(r["komorki"][1]["t"]) for r in D["niewiadome"]["niewiadome"]["wiersze"]
                  if "oddzielnik" not in r["klasa"]}
            kontrola_tabeli_zdarzen(W, D, zd, przeg, nw)
            # wykresy bez liczb w DOM
            W.niedasie(NAZWY["kohorty"], "wykres dzień po dniu i krzywa powrotu (uPlot)", "rysowane na płótnie; liczby tylko pod kursorem; numery zdarzeń sprawdzone przez listę pod wykresem")
            W.niedasie(NAZWY["lejek"], "wykres dzień po dniu (uPlot)", "rysowany na płótnie; liczby tylko pod kursorem; numery zdarzeń sprawdzone przez listę pod wykresem")
            W.niedasie(NAZWY["po-zakupie"], "punktualność i zwroty dzień po dniu (uPlot)", "rysowane na płótnie; liczby tylko pod kursorem; numery zdarzeń sprawdzone przez listę pod wykresem")
            W.niedasie(NAZWY["wynik"], "dwa wykresy marży i wydatków (uPlot)", "rysowane na płótnie; liczby tylko pod kursorem; sumy roczne sprawdzone przez tekst karty i tabelę miesięcy")
            W.niedasie(NAZWY["jakosc"], "duplikaty dzień po dniu (uPlot)", "rysowany na płótnie; liczby (604 kopie, 28–42% dziennie) tylko w tekście karty")
        przegl.close()
    serw.shutdown()
    rev = subprocess.run(["git", "-C", KATALOG, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    linie = [f"F — LICZBY NA WYKRESACH A TEKST I TABELE TEJ SAMEJ KARTY ({dt.datetime.now():%Y-%m-%d %H:%M}, commit {rev}, pliki strony z dysku)",
             f"Liczby czytane z wyrenderowanej strony ({nazwa_silnika}, bez okna, 127.0.0.1). Szerokości: 1366 px (komputer) i 375 px (telefon).", "",
             "1. Podsumowanie"]
    for szer, _, _ in SZEROKOSCI:
        x = [w for w in W.wiersze if w["szer"] == szer]
        linie.append(f"   {szer} px: {len(x)} porównań, niezgodnych {sum(not w['ok'] for w in x)}; błędy w konsoli w czasie kontroli: {len(bledy_razem[szer])}")
        for b in bledy_razem[szer][:10]:
            linie.append(f"      {b}")
    linie.append(f"   Razem: {len(W.wiersze)} porównań, niezgodnych {sum(not w['ok'] for w in W.wiersze)}.")
    linie.append("   Według zakładek (obie szerokości razem):")
    for z in ZAKLADKI:
        x = [w for w in W.wiersze if w["zakl"] == NAZWY[z]]
        linie.append(f"      {NAZWY[z]:18} {len(x):5} porównań, niezgodnych {sum(not w['ok'] for w in x)}")
    linie += ["", "2. Niezgodności"]
    zle = [w for w in W.wiersze if not w["ok"]]
    linie += [f"   {w['szer']} px | {w['zakl']} | {w['karta']} | {w['wykres']} | {w['co']}: na wykresie {w['w']} | odniesienie {w['o']} ({w['zrodlo']})" for w in zle] or ["   brak"]
    linie += ["", "3. Wykresy i liczby, których nie dało się porównać (albo uwagi do porównania)"]
    linie += [f"   {z} | {wk}: {pw}" for z, wk, pw, _ in W.nie] or ["   brak"]
    linie += ["", "4. Wszystkie porównania (szerokość | zakładka | karta | wykres | co: na wykresie || odniesienie (źródło) | wynik)"]
    for w in W.wiersze:
        linie.append(f"   {w['szer']} | {w['zakl']} | {w['karta']} | {w['wykres']} | {w['co']}: {w['w']} || {w['o']} ({w['zrodlo']}) | {'zgodne' if w['ok'] else 'NIEZGODNE'}")
    tekst = "\n".join(linie) + "\n"
    os.makedirs(WYNIKI, exist_ok=True)
    with open(raport, "w", encoding="utf-8", newline="\n") as f:
        f.write(tekst)
    print("\n".join(linie[:20 + len(zle) + len(W.nie)]))


if __name__ == "__main__":
    main()
