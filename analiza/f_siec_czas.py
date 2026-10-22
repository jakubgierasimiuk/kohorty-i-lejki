"""F — żądania sieciowe i czas ładowania strony (ostatnia kontrola przed publikacją, część 2: technika).

1. Żądania sieciowe: otwiera stronę z folderu narzedzie/ w Microsoft Edge bez okna (Playwright, 127.0.0.1) w trybie jasnym
   i ciemnym, przy 1366 px i 375 px, przechodzi przez 9 zakładek i zmienia filtry. Zapisuje każde żądanie (adres, rodzaj,
   status). Każde ma iść do 127.0.0.1 na port lokalnego serwera.
2. Przeszukuje pliki w narzedzie/ pod kątem adresów http(s), fontów, CDN, skryptów analityki i wywołań sieci
   (fetch, XMLHttpRequest, sendBeacon, WebSocket, import, @import, preconnect).
3. Czas ładowania: czas do gotowości pierwszej zakładki i każdej kolejnej (pierwsze otwarcie) oraz bajty przesłane
   przez sieć, w trzech wariantach: komputer bez ograniczeń; telefon (375 px) z wolnym 4G i czterokrotnie wolniejszym
   procesorem (CDP), pliki skompresowane gzip jak na GitHub Pages; to samo bez kompresji (najgorszy przypadek).
   Lokalny serwer w wariantach „gzip” kompresuje odpowiedzi tak jak GitHub Pages (Content-Encoding: gzip).
4. Rozmiar plików strony: razem, osobno dane_strony/, oraz po kompresji gzip.
Wynik: analiza/wyniki/f_siec_czas.txt

Uruchomienie z głównego folderu (kilka minut):
    python -I analiza/f_siec_czas.py
"""
import datetime as dt
import functools
import gzip
import http.server
import io
import os
import re
import subprocess
import sys
import threading
import time
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARZEDZIE = os.path.join(KATALOG, "narzedzie")
RAPORT = os.path.join(KATALOG, "analiza", "wyniki", "f_siec_czas.txt")
ZAKLADKI = ["wzrost", "kohorty", "lejek", "po-zakupie", "zdarzenia", "wynik", "jakosc", "priorytety", "niewiadome"]
NAZWY = {"wzrost": "Czy to wzrost", "kohorty": "Kohorty", "lejek": "Lejek", "po-zakupie": "Po zakupie", "zdarzenia": "Zdarzenia",
         "wynik": "Wynik biznesu", "jakosc": "Jakość danych", "priorytety": "Priorytety", "niewiadome": "Czego nie wiemy"}
# gotowość zakładki: jej najpóźniej rysowany element
GOTOWE = {
    "wzrost": "#wz-nowy .slupki-grup .sg-wiersz", "kohorty": "#ko-macierz tbody tr", "lejek": "#lj-udzial .kl-grupa",
    "po-zakupie": "#pz-karta-godziny .kolumny .kl-grupa", "zdarzenia": "#zd-lista article", "wynik": "#ek-wykres .wk-wiersz",
    "jakosc": "#jk-testy-kw .slupek-wiersz", "priorytety": "#pr-1 .hantle .wk-wiersz", "niewiadome": "#nw-tabela tbody tr",
}
# zmiany filtrów na zakładkach (selektor pola, wartość) — do kontroli żądań przy klikaniu
FILTRY = {
    "kohorty": [("#ko-podz", "kanal"), ("#ko-okno", "30"), ("#ko-miara", "marza"), ("#ko-regula", "Z2"), ("#ko-f-urzadzenie", "mobile"), ("#ko-f-urzadzenie", "")],
    "lejek": [("#f-podz", "kanal"), ("#f-podz", "kampania"), ("#f-podz", "strona_wejscia"), ("#f-podz", "system_przegladarka"),
              ("#f-podz", "urzadzenie_przegladarka"), ("#f-podz", "urzadzenie"), ("#f-podz", "calosc"), ("#f-pac", "wszyscy"), ("#f-krok", "k3")],
    "po-zakupie": [("#pz-spec", "pediatra"), ("#pz-prog", "p30"), ("#zw-grupa", "nowe"), ("#oc-spec", "psychiatra"), ("#pz-ruch-grupa", "pozostale")],
    "wynik": [("#wy-krok", "tydz"), ("#ek-poziom", "kampania"), ("#ek-okres", "1")],
    "niewiadome": [("#nw-filtr-pozycja", "1")],
}
SZUKAJ = [r"https?://[^\s\"'<>)]+", r"fonts\.googleapis|fonts\.gstatic|@font-face", r"\bcdn\b|cdnjs|jsdelivr|unpkg",
          r"google-analytics|googletagmanager|gtag\(|\bga\(|plausible|matomo|hotjar|clarity\.ms|segment\.io|mixpanel",
          r"\bfetch\(|XMLHttpRequest|sendBeacon|new WebSocket|EventSource|\bimport\(|@import|rel=\"?preconnect|rel=\"?dns-prefetch"]


class Handler(http.server.SimpleHTTPRequestHandler):
    gzip_on = False
    pamiec = {}

    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if not self.gzip_on or "gzip" not in (self.headers.get("Accept-Encoding") or ""):
            return super().do_GET()
        sciezka = self.translate_path(self.path)
        if os.path.isdir(sciezka):
            sciezka = os.path.join(sciezka, "index.html")
        if not os.path.isfile(sciezka):
            return super().do_GET()
        if sciezka not in self.pamiec:
            with open(sciezka, "rb") as f:
                surowe = f.read()
            bufor = io.BytesIO()
            with gzip.GzipFile(fileobj=bufor, mode="wb", compresslevel=6, mtime=0) as g:
                g.write(surowe)
            self.pamiec[sciezka] = bufor.getvalue()
        dane = self.pamiec[sciezka]
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(sciezka))
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(dane)))
        self.end_headers()
        self.wfile.write(dane)


def serwer(gz):
    klasa = type("H", (Handler,), {"gzip_on": gz, "pamiec": {}})
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(klasa, directory=NARZEDZIE))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def zadania(p):
    """Część 1: wszystkie żądania w 4 wariantach (tryb × szerokość), z przejściem przez zakładki i zmianą filtrów."""
    s = serwer(False)
    port = s.server_address[1]
    adres = f"http://127.0.0.1:{port}/"
    wyniki = []
    b = p.chromium.launch(channel="msedge", headless=True)
    for tryb in ("jasny", "ciemny"):
        for szer, wys in ((1366, 900), (375, 812)):
            ctx = b.new_context(viewport={"width": szer, "height": wys}, color_scheme="dark" if tryb == "ciemny" else "light",
                                is_mobile=szer < 760, has_touch=szer < 760)
            log = []
            ctx.on("request", lambda r: log.append((r.url, r.resource_type)))
            nieudane = []
            ctx.on("requestfailed", lambda r: nieudane.append(r.url))
            statusy = []
            ctx.on("response", lambda r: statusy.append((r.url, r.status)))
            pg = ctx.new_page()
            pg.goto(adres + "#wzrost")
            pg.wait_for_selector(GOTOWE["wzrost"], timeout=60000, state="attached")
            for z in ZAKLADKI:
                pg.evaluate(f"location.hash = '{z}'")
                pg.wait_for_selector(GOTOWE[z], timeout=60000, state="attached")
                pg.wait_for_timeout(500)
                for sel, wart in FILTRY.get(z, []):
                    pg.evaluate("([s, v]) => { const e = document.querySelector(s); if (e) { e.value = v; e.dispatchEvent(new Event('change', { bubbles: true })); } }", [sel, wart])
                    pg.wait_for_timeout(700)
                if z == "kohorty":
                    for t in ("tygodniowe", "dzienne", "miesięczne"):
                        pg.click(f"#ko-macierz-filtry button:has-text('{t}')")
                        pg.wait_for_timeout(600)
                if z == "wynik":
                    pg.click("#ek-karta .przelacznik button:has-text('180 dni')")
                    pg.wait_for_timeout(400)
                if z == "zdarzenia":
                    pg.click("#zd-filtry label:first-child input")
                    pg.wait_for_timeout(400)
            pg.wait_for_timeout(1000)
            ctx.close()
            obce = [u for u, _ in log if urlparse(u).hostname != "127.0.0.1" or (urlparse(u).port not in (port, None) and not u.startswith("data:"))]
            obce = [u for u in obce if not u.startswith("data:")]
            bledne = [(u, st) for u, st in statusy if st >= 400]
            wyniki.append({"tryb": tryb, "szer": szer, "n": len(log), "pliki": sorted({urlparse(u).path for u, _ in log}), "obce": obce,
                           "nieudane": nieudane, "bledne": bledne, "rodzaje": sorted({r for _, r in log})})
    b.close()
    s.shutdown()
    return wyniki


def przeszukaj():
    """Część 2: adresy i wywołania sieci w plikach strony."""
    out = []
    for kat, _, pliki in os.walk(NARZEDZIE):
        for n in sorted(pliki):
            sc = os.path.join(kat, n)
            wzgl = os.path.relpath(sc, NARZEDZIE).replace("\\", "/")
            try:
                with open(sc, encoding="utf-8") as f:
                    t = f.read()
            except UnicodeDecodeError:
                continue
            for wz in SZUKAJ:
                for m in re.finditer(wz, t, flags=re.I):
                    kontekst = t[max(0, m.start() - 50): m.end() + 30].replace("\n", " ")
                    out.append((wzgl, m.group(0)[:80], kontekst))
    return out


def czasy(p, wariant, telefon, gz, siec, cpu):
    """Część 3: czas do gotowości zakładek i bajty przez sieć (CDP: Network.loadingFinished.encodedDataLength)."""
    s = serwer(gz)
    adres = f"http://127.0.0.1:{s.server_address[1]}/"
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 375 if telefon else 1366, "height": 812 if telefon else 900}, is_mobile=telefon, has_touch=telefon)
    pg = ctx.new_page()
    cdp = ctx.new_cdp_session(pg)
    cdp.send("Network.enable")
    cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    if siec:
        cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": siec[0], "downloadThroughput": siec[1] * 1024 * 1024 / 8,
                                                       "uploadThroughput": siec[2] * 1024 / 8})
    if cpu:
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": cpu})
    bajty = {"razem": 0}
    adresy = {}
    cdp.on("Network.requestWillBeSent", lambda e: adresy.__setitem__(e["requestId"], e["request"]["url"]))
    cdp.on("Network.loadingFinished", lambda e: bajty.__setitem__("razem", bajty["razem"] + e["encodedDataLength"]))
    wyn = []
    t0 = time.perf_counter()
    pg.goto(adres + "#wzrost", wait_until="commit", timeout=180000)
    pg.wait_for_selector("#wz-nowy .karta", timeout=180000, state="attached")
    t_pierwsza_karta = time.perf_counter() - t0
    pg.wait_for_selector(GOTOWE["wzrost"], timeout=180000, state="attached")
    t1 = time.perf_counter() - t0
    nav = pg.evaluate("() => { const n = performance.getEntriesByType('navigation')[0]; return { dcl: Math.round(n.domContentLoadedEventEnd), load: Math.round(n.loadEventEnd) }; }")
    wyn.append(("wzrost", t1, bajty["razem"], f"pierwsza karta widoczna po {t_pierwsza_karta:.1f} s; DOMContentLoaded {nav['dcl'] / 1000:.1f} s, load {nav['load'] / 1000:.1f} s"))
    for z in ZAKLADKI[1:]:
        przed = bajty["razem"]
        t = time.perf_counter()
        pg.evaluate(f"location.hash = '{z}'")
        pg.wait_for_selector(GOTOWE[z], timeout=180000, state="attached")
        wyn.append((z, time.perf_counter() - t, bajty["razem"] - przed, ""))
    # ponowne wejście na zakładkę (dane już w pamięci strony)
    t = time.perf_counter()
    pg.evaluate("location.hash = 'kohorty'")
    pg.wait_for_selector(GOTOWE["kohorty"], timeout=180000, state="attached")
    pg.wait_for_timeout(50)
    powrot = time.perf_counter() - t
    ctx.close()
    b.close()
    s.shutdown()
    return {"wariant": wariant, "zakladki": wyn, "razem": bajty["razem"], "powrot_kohorty": powrot}


def rozmiary():
    out, dane, razem, gz_razem, gz_dane = [], 0, 0, 0, 0
    for kat, _, pliki in os.walk(NARZEDZIE):
        for n in pliki:
            sc = os.path.join(kat, n)
            r = os.path.getsize(sc)
            with open(sc, "rb") as f:
                g = len(gzip.compress(f.read(), compresslevel=6))
            wzgl = os.path.relpath(sc, NARZEDZIE).replace("\\", "/")
            out.append((wzgl, r, g))
            razem += r
            gz_razem += g
            if wzgl.startswith("dane_strony/"):
                dane += r
                gz_dane += g
    return sorted(out, key=lambda x: -x[1]), razem, dane, gz_razem, gz_dane


def kb(x):
    return f"{x / 1024:,.0f} KB".replace(",", " ")


def main():
    sys.stdout.reconfigure(errors="replace")
    L = []
    with sync_playwright() as p:
        Z = zadania(p)
        WARIANTY = [("komputer 1366 px, bez ograniczeń, bez kompresji (lokalnie)", False, False, None, None),
                    ("komputer 1366 px, bez ograniczeń, gzip jak GitHub Pages", False, True, None, None),
                    ("telefon 375 px, wolne 4G (150 ms, 1,6 Mb/s) i procesor 4× wolniej, gzip jak GitHub Pages", True, True, (150, 1.6, 750), 4),
                    ("telefon 375 px, wolne 4G i procesor 4× wolniej, bez kompresji (najgorszy przypadek)", True, False, (150, 1.6, 750), 4)]
        C = [czasy(p, *w) for w in WARIANTY]
    S = przeszukaj()
    pliki, razem, dane, gz_razem, gz_dane = rozmiary()
    rev = subprocess.run(["git", "-C", KATALOG, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    L.append(f"F — ŻĄDANIA SIECIOWE I CZAS ŁADOWANIA ({dt.datetime.now():%Y-%m-%d %H:%M}, commit {rev}, pliki strony z dysku)")
    L += ["", "1. Żądania sieciowe (9 zakładek, zmiany filtrów na zakładkach kohort, lejka, po zakupie, wyniku, zdarzeń i niewiadomych)"]
    for z in Z:
        L.append(f"   {z['tryb']:6} {z['szer']:5} px: {z['n']} żądań, różnych plików {len(z['pliki'])}, poza 127.0.0.1: {len(z['obce'])}, "
                 f"nieudanych {len(z['nieudane'])}, ze statusem 4xx/5xx {len(z['bledne'])}; rodzaje: {', '.join(z['rodzaje'])}")
        for u in z["obce"][:10] + z["nieudane"][:10]:
            L.append(f"      {u}")
        for u, st in z["bledne"][:10]:
            L.append(f"      {st} {u}")
    L.append(f"   Pliki pobrane (wariant jasny, 1366 px): {', '.join(Z[0]['pliki'])}")
    L += ["", "2. Adresy i wywołania sieci w plikach narzedzie/ (każde trafienie z kontekstem)"]
    L += [f"   {plik}: {traf!r} … {kont[:150]!r}" for plik, traf, kont in S] or ["   brak"]
    L += ["", "3. Czas ładowania (sekundy do narysowania ostatniego elementu zakładki; pierwsze otwarcie każdej zakładki po kolei; bajty przez sieć)"]
    for c in C:
        L.append(f"   == {c['wariant']}: razem przez sieć {kb(c['razem'])}")
        for z, t, b_, uw in c["zakladki"]:
            L.append(f"      {NAZWY[z]:16} {t:6.1f} s  {kb(b_):>9}  {uw}")
        L.append(f"      ponowne wejście na „Kohorty” (dane w pamięci): {c['powrot_kohorty']:.1f} s")
    L += ["", f"4. Rozmiar plików strony: razem {kb(razem)} ({len(pliki)} plików), w tym dane_strony/ {kb(dane)}; po kompresji gzip razem {kb(gz_razem)}, dane_strony/ {kb(gz_dane)}",
          "   największe pliki (bajty, po gzip):"]
    L += [f"      {n:42} {kb(r):>9} {kb(g):>9}" for n, r, g in pliki[:20]]
    tekst = "\n".join(L) + "\n"
    with open(RAPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write(tekst)
    print(tekst)


if __name__ == "__main__":
    main()
