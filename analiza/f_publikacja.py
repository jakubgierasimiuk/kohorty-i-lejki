"""F — gotowość do publikacji: podścieżka jak na GitHub Pages, szerokości pośrednie, silniki Safari (WebKit) i Firefox.

1. Podścieżka: lokalny serwer 127.0.0.1 podaje folder narzedzie/ pod adresem /b2c-narzedzie/ (tak jak GitHub Pages podaje
   repozytorium pod https://<organizacja>.github.io/<repozytorium>/), a pod / zwraca 404. Edge przechodzi 9 zakładek
   i kilka odnośników z parametrami; każde żądanie musi trafić pod podścieżkę i dostać 200.
2. Szerokości 768 px (tablet) i 1920 px (duży monitor) w Edge: 9 zakładek, błędy w konsoli, przewijanie w bok,
   wykresy szersze niż karta; zrzuty dwóch zakładek.
3. Silniki WebKit (silnik Safari) i Firefox z pakietu Playwright, przy 1366 px i 375 px: 9 zakładek, błędy strony
   i konsoli, przewijanie w bok, przycisk „Zakładki” na telefonie; zrzuty trzech zakładek przy 375 px.
Wynik: analiza/wyniki/f_publikacja.txt, zrzuty do katalogu podanego w --zrzuty (poza repozytorium).

Uruchomienie z głównego folderu:
    python -I analiza/f_publikacja.py --zrzuty <katalog>
"""
import argparse
import datetime as dt
import functools
import http.server
import os
import subprocess
import sys
import threading
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARZEDZIE = os.path.join(KATALOG, "narzedzie")
RAPORT = os.path.join(KATALOG, "analiza", "wyniki", "f_publikacja.txt")
PREFIKS = "/b2c-narzedzie/"
ZAKLADKI = ["wzrost", "kohorty", "lejek", "po-zakupie", "zdarzenia", "wynik", "jakosc", "priorytety", "niewiadome"]
GOTOWE = {
    "wzrost": "#wz-nowy .slupki-grup .sg-wiersz", "kohorty": "#ko-macierz tbody tr", "lejek": "#lj-udzial .kl-grupa",
    "po-zakupie": "#pz-karta-godziny .kolumny .kl-grupa", "zdarzenia": "#zd-lista article", "wynik": "#ek-wykres .wk-wiersz",
    "jakosc": "#jk-testy-kw .slupek-wiersz", "priorytety": "#pr-1 .hantle .wk-wiersz", "niewiadome": "#nw-tabela tbody tr",
}
POMIAR = """() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth,
  szersze: [...document.querySelectorAll('main *')].filter(e => { const r = e.getBoundingClientRect();
    return r.width > 0 && r.right > window.innerWidth + 1 && !e.closest('.tabela-ramka, .zakladki, .macierz-ramka'); })
    .slice(0, 5).map(e => e.tagName + (e.id ? '#' + e.id : '') + '.' + (typeof e.className === 'string' ? e.className : '')),
  wykresy: [...document.querySelectorAll('section:not([hidden]) .wykres')].filter(e => e.offsetParent && e.scrollWidth > e.clientWidth + 1)
    .map(e => e.id + ' ' + e.scrollWidth + '/' + e.clientWidth),
  karty: document.querySelectorAll('section:not([hidden]) article').length })"""


class Handler(http.server.SimpleHTTPRequestHandler):
    prefiks = None

    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def translate_path(self, path):
        if self.prefiks:
            if not path.startswith(self.prefiks):
                return os.path.join(NARZEDZIE, "__brak__")
            path = "/" + path[len(self.prefiks):]
        return super().translate_path(path)


def serwer(prefiks=None):
    klasa = type("H", (Handler,), {"prefiks": prefiks})
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(klasa, directory=NARZEDZIE))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def przejdz(pg, adres, bledy, zrzuty=None, pref="", lista=None):
    """Otwiera 9 zakładek po kolei; zwraca wiersze raportu i problemy."""
    wiersze, problemy = [], []
    pg.goto(adres + "#wzrost")
    for z in lista or ZAKLADKI:
        pg.evaluate(f"location.hash = '{z}'")
        try:
            pg.wait_for_selector(GOTOWE[z], timeout=60000, state="attached")
        except Exception as e:  # noqa: BLE001
            problemy.append(f"{z}: zakładka się nie narysowała ({e.__class__.__name__})")
            continue
        pg.wait_for_timeout(800)
        m = pg.evaluate(POMIAR)
        bok = m["sw"] > m["iw"] + 1
        wiersze.append(f"{z:11} kart {m['karty']:3}, szerokość dokumentu {m['sw']} / okno {m['iw']}" + (" — PRZEWIJA SIĘ W BOK" if bok else ""))
        if bok or m["szersze"]:
            problemy.append(f"{z}: wychodzi poza ekran {m['szersze']}")
        if m["wykresy"]:
            problemy.append(f"{z}: wykres szerszy niż karta {m['wykresy']}")
        if zrzuty and z in zrzuty[1]:
            pg.screenshot(path=os.path.join(zrzuty[0], f"{pref}{z}.png"), full_page=True)
    return wiersze, problemy


def main():
    sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--zrzuty", required=True)
    arg = ap.parse_args()
    os.makedirs(arg.zrzuty, exist_ok=True)
    L, P = [], []
    with sync_playwright() as p:
        # 1. podścieżka
        s = serwer(PREFIKS)
        baza = f"http://127.0.0.1:{s.server_address[1]}"
        b = p.chromium.launch(channel="msedge", headless=True)
        ctx = b.new_context(viewport={"width": 1366, "height": 900})
        zad, odp, bledy = [], [], []
        ctx.on("request", lambda r: zad.append(r.url))
        ctx.on("response", lambda r: odp.append((r.url, r.status)))
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: bledy.append("błąd strony: " + str(e)))
        pg.on("console", lambda m: bledy.append("konsola: " + m.text) if m.type == "error" else None)
        w, pr = przejdz(pg, baza + PREFIKS, bledy)
        for h in ("#kohorty?regula=Z1K&podz=kanal&okno=90&miara=powrot&wygl=7&f_grupa=pozostale", "#lejek?podz=urzadzenie&w=mobile", "#priorytety?p=3",
                  "#niewiadome?n=4", "#zdarzenia?z=safari_ios"):
            pg.goto(baza + PREFIKS + h)
            pg.wait_for_timeout(2500)
            widok = pg.evaluate("() => { const s = [...document.querySelectorAll('section.widok')].find(x => !x.hidden); return s ? s.id : null; }")
            ok = widok == "v-" + h[1:].split("?")[0]
            w.append(f"odnośnik {h}: zakładka {widok}{'' if ok else ' — ŹLE'}")
            if not ok:
                pr.append(f"odnośnik {h} pod podścieżką otwiera {widok}")
        poza = [u for u in zad if not u.startswith("data:") and not urlparse(u).path.startswith(PREFIKS)]
        zle = [(u, st) for u, st in odp if st >= 400]
        ctx.close()
        b.close()
        L += ["1. Podścieżka jak na GitHub Pages (" + PREFIKS + "): " + f"{len(zad)} żądań, poza podścieżką {len(poza)}, ze statusem 4xx/5xx {len(zle)}, "
              f"błędów w konsoli {len(bledy)}"]
        L += [f"   {x}" for x in w]
        L += [f"   poza podścieżką: {u}" for u in poza[:10]] + [f"   {st}: {u}" for u, st in zle[:10]] + [f"   {x}" for x in bledy[:10]]
        P += [f"podścieżka: {x}" for x in pr] + [f"podścieżka: żądanie poza {PREFIKS}: {u}" for u in poza[:5]] + [f"podścieżka: {st} {u}" for u, st in zle[:5]] + \
             [f"podścieżka: {x}" for x in bledy[:5]]
        s.shutdown()
        # 2. szerokości pośrednie (Edge) i 3. silniki WebKit i Firefox
        s = serwer()
        adres = f"http://127.0.0.1:{s.server_address[1]}/"
        PROBY = [("Edge", "chromium", {"channel": "msedge"}, 768, 1024, False, ["kohorty", "lejek"]),
                 ("Edge", "chromium", {"channel": "msedge"}, 1920, 1080, False, ["wzrost", "lejek"]),
                 ("WebKit (Safari)", "webkit", {}, 1366, 900, False, []),
                 ("WebKit (Safari)", "webkit", {}, 375, 812, True, ["wzrost", "kohorty", "lejek"]),
                 ("Firefox", "firefox", {}, 1366, 900, False, []),
                 ("Firefox", "firefox", {}, 375, 812, False, ["lejek"])]
        for nazwa, silnik, opcje, szer, wys, telefon, zrz in PROBY:
            b = getattr(p, silnik).launch(headless=True, **opcje)
            kw = {"viewport": {"width": szer, "height": wys}}
            if silnik == "firefox":
                # Firefox z Playwrighta bez języka zwraca navigator.language = "undefined" i uPlot się nie wczytuje (artefakt testu)
                kw["locale"] = "pl-PL"
            if telefon:
                kw.update(is_mobile=True, has_touch=True)
            ctx = b.new_context(**kw)
            pg = ctx.new_page()
            bledy = []
            pg.on("pageerror", lambda e: bledy.append("błąd strony: " + str(e)))
            pg.on("console", lambda m: bledy.append("konsola: " + m.text) if m.type == "error" else None)
            pref = f"{silnik}_{szer}_"
            w, pr = przejdz(pg, adres, bledy, (arg.zrzuty, zrz), pref)
            if szer < 760:
                pg.evaluate("location.hash = 'priorytety'")
                pg.wait_for_timeout(800)
                pg.evaluate("window.scrollTo(0, 2500)")
                pg.wait_for_timeout(600)
                widac = pg.evaluate("() => !document.getElementById('szybkie-zakladki').hidden")
                if widac:
                    pg.click("#szybkie-przycisk")
                    pg.wait_for_timeout(300)
                n = pg.evaluate("() => { const l = document.getElementById('szybkie-lista'); return l.hidden ? 0 : l.querySelectorAll('a').length; }")
                w.append(f"przycisk „Zakładki” po przewinięciu: {'widoczny' if widac else 'NIEWIDOCZNY'}, zakładek na liście {n}")
                if not widac or n != 9:
                    pr.append(f"przycisk „Zakładki”: widoczny={widac}, zakładek={n}")
            wersja = b.version
            ctx.close()
            b.close()
            L += ["", f"{'2' if nazwa == 'Edge' else '3'}. {nazwa} {wersja}, {szer} × {wys} px{' (telefon)' if telefon else ''}: problemów {len(pr)}, błędów w konsoli {len(bledy)}"]
            L += [f"   {x}" for x in w] + [f"   PROBLEM: {x}" for x in pr] + [f"   {x}" for x in bledy[:15]]
            P += [f"{nazwa} {szer} px: {x}" for x in pr] + [f"{nazwa} {szer} px: {x}" for x in bledy[:5]]
        s.shutdown()
    rev = subprocess.run(["git", "-C", KATALOG, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    nag = [f"F — GOTOWOŚĆ DO PUBLIKACJI: PODŚCIEŻKA, SZEROKOŚCI POŚREDNIE, SAFARI (WEBKIT) I FIREFOX ({dt.datetime.now():%Y-%m-%d %H:%M}, commit {rev})",
           f"Problemy razem: {len(P)}"] + [f"   {x}" for x in P] + [""]
    tekst = "\n".join(nag + L) + "\n"
    with open(RAPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write(tekst)
    print(tekst)


if __name__ == "__main__":
    main()
