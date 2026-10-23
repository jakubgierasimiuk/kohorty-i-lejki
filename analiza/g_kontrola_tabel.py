"""G — kontrola zachowania nowych „Kohort” i „Lejka” (runda przejrzystości, 2026-10-23) w Edge bez okna.

Otwiera stronę z folderu narzedzie/ na lokalnym serwerze 127.0.0.1 (losowy port) i sprawdza: czysty adres na starcie,
„Przywróć domyślne” (nieaktywny bez zmian, po zmianie aktywny, wraca do startu i czyści adres), przyciski zdarzeń
(porównanie 60 dni przed i po, zdanie o zmianie), okresy słowami w tabeli, nazwy zdarzeń w mapie, przyklejony pasek pod
nagłówkiem, szerokość tabel grup przy 1366 px oraz kolor i zmianę każdej komórki tabel grup wobec rachunku w Pythonie
(analiza/wyniki/g_istotnosc.json; najpierw uruchomić analiza/g_istotnosc.py).

Uruchomienie z głównego folderu: python -I analiza/g_kontrola_tabel.py
Wynik na ekranie i w analiza/wyniki/g_kontrola_tabel.txt (OK albo BŁĄD przy każdym sprawdzeniu)."""
import functools
import http.server
import json
import os
import re
import sys
import threading

from playwright.sync_api import sync_playwright

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = json.load(open(os.path.join(KATALOG, "analiza", "wyniki", "g_istotnosc.json"), encoding="utf-8"))


class Cichy(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


SERW = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Cichy, directory=os.path.join(KATALOG, "narzedzie")))
threading.Thread(target=SERW.serve_forever, daemon=True).start()
ADRES = f"http://127.0.0.1:{SERW.server_address[1]}/"
problemy, uwagi = [], []


def ok(war, opis):
    (uwagi if war else problemy).append(("OK  " if war else "BŁĄD ") + opis)


def tabela(pg, sel):
    return pg.evaluate("""(sel) => Array.from(document.querySelectorAll(sel + ' tbody tr')).map(tr => {
        const c = Array.from(tr.cells);
        return { nazwa: c[0].querySelector('.tg-nazwa > span') ? c[0].querySelector('.tg-nazwa > span').textContent : c[0].textContent,
          kom: c.slice(2).map(td => { const z = td.querySelector('.zm'); return z ? { t: z.textContent, kl: z.className, tytul: td.title } : { t: td.textContent }; }) };
    })""", sel)


def liczba(t):
    m = re.search(r"([+−-]?\d+(?:,\d+)?)", t)
    return float(m.group(1).replace("−", "-").replace(",", ".")) if m else None


def porownaj(wiersze_js, scen, miary, okna_kolumn, opis):
    """miary: nazwy miar g_istotnosc w kolejności kolumn tabeli (tryb „wszystkie”)."""
    py = {w["grupa"]: {k["miara"]: k for k in w["komorki"]} for w in scen["tabela"]["wiersze"]}
    zg = rz = 0
    for w in wiersze_js:
        naz = w["nazwa"].replace("mała grupa", "").strip()
        naz = "Wszyscy wybrani pacjenci" if naz.startswith("Wszyscy wybrani") else naz
        naz = "Razem" if naz.startswith("Wszystkie wybrane sesje") else naz
        if naz not in py:
            problemy.append(f"BŁĄD {opis}: wiersz „{naz}” nie ma odpowiednika w g_istotnosc.json")
            continue
        for k, m in zip(w["kom"], miary):
            if m is None or "kl" not in k or m not in py[naz]:
                continue
            p = py[naz][m]
            kol = "zm-szara" not in k["kl"]
            d = liczba(k["t"])
            if kol == p["istotna"] and d is not None and abs(d - round(p["zmiana"], 1)) < 0.051:
                zg += 1
            else:
                rz += 1
                problemy.append(f"BŁĄD {opis}: {naz} / {m}: strona {k['t']} kolor={kol}, Python {p['zmiana']:+.2f} istotna={p['istotna']}")
    ok(rz == 0, f"{opis}: {zg} komórek zgodnych z g_istotnosc.json, {rz} niezgodnych")
    return zg


def main():
    sys.stdout.reconfigure(errors="replace")
    sc = {s["nazwa"].split(":")[0] + ":" + s["nazwa"].split(":")[1][:30]: s for s in G}
    S_KUBA = G[0]; S_DOM_K = G[1]; S_USL_ROK = G[2]; S_LJ_DOM = G[4]; S_LJ_LUKA = G[5]
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", headless=True)
        ctx = b.new_context(viewport={"width": 1366, "height": 900}, locale="pl-PL")
        pg = ctx.new_page()
        bledy = []
        pg.on("pageerror", lambda e: bledy.append(str(e)))
        pg.on("console", lambda m: bledy.append(m.text) if m.type == "error" else None)

        # --- Kohorty: domyślne
        pg.goto(ADRES + "#kohorty"); pg.wait_for_timeout(2500)
        ok(pg.evaluate("location.hash") == "#kohorty", f"Kohorty: adres startowy czysty ({pg.evaluate('location.hash')})")
        ok(pg.evaluate("document.getElementById('ko-reset').disabled"), "Kohorty: „Przywróć domyślne” nieaktywny na starcie")
        w = tabela(pg, "#ko-tabela")
        # tryb „miara”: kolumny [A, B, Zmiana] → porównanie tylko kolumny zmiany
        porownaj([{"nazwa": x["nazwa"], "kom": x["kom"][2:]} for x in w], S_DOM_K, ["powrót w 90 dniach"], None, "Kohorty domyślne, powrót 90 dni")
        # zmiana ustawienia → przycisk aktywny, adres z parametrem
        pg.select_option("#ko-miara", "marza"); pg.wait_for_timeout(800)
        ok("miara=marza" in pg.evaluate("location.hash") and not pg.evaluate("document.getElementById('ko-reset').disabled"),
           "Kohorty: po zmianie miary adres ma miara=marza, przycisk aktywny")
        w = tabela(pg, "#ko-tabela")
        porownaj([{"nazwa": x["nazwa"], "kom": x["kom"][2:]} for x in w], S_DOM_K, ["marża na pacjenta w 90 dniach (zł)"], None, "Kohorty domyślne, marża 90 dni")
        pg.click("#ko-reset"); pg.wait_for_timeout(800)
        ok(pg.evaluate("location.hash") == "#kohorty" and pg.evaluate("document.getElementById('ko-miara').value") == "powrot"
           and pg.evaluate("document.getElementById('ko-reset').disabled"), "Kohorty: „Przywróć domyślne” wraca do startu i czyści adres")

        # --- Kohorty: przypadek Kuby (60 dni przed i po godzinie bez danych, pierwsza usługa) — z adresu
        pg.goto(ADRES + "#kohorty?podz=usluga&a=2025-03-18_2025-05-16&b=2025-05-17_2025-07-15&tabela=wszystkie"); pg.wait_for_timeout(2500)
        w = tabela(pg, "#ko-tabela")
        n = porownaj(w, S_KUBA, ["powrót w 30 dniach", "powrót w 60 dniach", "powrót w 90 dniach", "powrót w 180 dniach"], None,
                     "Kohorty, przypadek Kuby, powrót we wszystkich oknach")
        kolorowe = sum(1 for x in w for k in x["kom"] if "kl" in k and "zm-szara" not in k["kl"])
        ok(kolorowe == 0, f"Kohorty, przypadek Kuby: kolorowych komórek {kolorowe} (Python: 0 istotnych)")
        pg.select_option("#ko-miara", "marza"); pg.wait_for_timeout(800)
        w = tabela(pg, "#ko-tabela")
        porownaj(w, S_KUBA, [None, None, "marża na pacjenta w 90 dniach (zł)", "marża na pacjenta w 180 dniach (zł)"], None,
                 "Kohorty, przypadek Kuby, marża 90 i 180 dni")
        # lista porównań bez zdarzeń jakości danych
        opcje = pg.evaluate("Array.from(document.querySelectorAll('#ko-preset option')).map(o => o.textContent)")
        ok(not any("Godzina bez danych" in o or "Duplikaty" in o for o in opcje), f"Kohorty: lista porównań bez jakości danych ({len(opcje)} pozycji)")

        # --- Kohorty: przycisk zdarzenia ustawia porównanie i pokazuje zdanie
        pg.goto(ADRES + "#kohorty"); pg.wait_for_timeout(2000)
        if not pg.evaluate("document.getElementById('ko-reset').disabled"): pg.click("#ko-reset"); pg.wait_for_timeout(800)
        pg.click("#ko-zd .zd-przycisk >> text=Start kampanii Meta na L4"); pg.wait_for_timeout(900)
        h = pg.evaluate("location.hash")
        zd = pg.evaluate("(document.querySelector('#ko-zd .zd-wynik')||{}).textContent || ''")
        ok("a=2025-09-04_2025-11-02" in h and "b=2025-11-03_2026-01-01" in h, f"Kohorty: przycisk Meta ustawia 60 dni przed i po ({h})")
        ok(zd.startswith("„Start kampanii Meta na L4” (3.11.2025)"), "Kohorty: zdanie o zdarzeniu: " + zd[:160])
        naglowki = pg.evaluate("Array.from(document.querySelectorAll('#ko-tabela thead th')).map(x => x.textContent)")
        ok("60 dni przed" in naglowki and "60 dni po" in naglowki, f"Kohorty: okresy słowami w tabeli {naglowki}")
        ok(pg.evaluate("document.querySelectorAll('#ko-zd .zd-przycisk').length") == 8, "Kohorty: 8 przycisków przyczyn domyślnie")
        linie = pg.evaluate("document.querySelectorAll('#ko-macierz .mz-zd').length")
        ok(linie >= 10, f"Kohorty: nazwy zdarzeń w mapie ({linie})")
        # przyklejony pasek
        pg.evaluate("window.scrollTo(0, 2500)"); pg.wait_for_timeout(300)
        top = pg.evaluate("document.getElementById('ko-pasek').getBoundingClientRect().top")
        hn = pg.evaluate("document.querySelector('.naglowek').offsetHeight")
        ok(abs(top - hn) < 2, f"Kohorty: pasek przyklejony pod nagłówkiem (top {top}, nagłówek {hn})")
        # szerokość tabeli przy 1366
        pg.select_option("#ko-podz", "kanal"); pg.wait_for_timeout(800)
        sz = pg.evaluate("[document.querySelector('#ko-tabela').scrollWidth, document.querySelector('#ko-tabela').closest('.tabela-ramka').clientWidth]")
        ok(sz[0] <= sz[1], f"Kohorty: tabela grup mieści się bez przewijania w bok przy 1366 ({sz})")

        # --- Lejek
        pg.goto(ADRES + "#lejek"); pg.wait_for_timeout(2500)
        ok(pg.evaluate("location.hash") == "#lejek", f"Lejek: adres startowy czysty ({pg.evaluate('location.hash')})")
        ok(pg.evaluate("document.getElementById('lj-reset').disabled"), "Lejek: „Przywróć domyślne” nieaktywny na starcie")
        pg.click("#lj-tabela-tryb button >> text=wszystkie kroki"); pg.wait_for_timeout(900)
        w = tabela(pg, "#lj-tabela")
        porownaj(w, S_LJ_DOM, ["Wybór usługi", "Wybór terminu", "Logowanie albo konto", "Wejście na płatność", "Płatność przyjęta", "Sesja do płatności"],
                 None, "Lejek domyślny, wszystkie kroki")
        sz = pg.evaluate("[document.querySelector('#lj-tabela').scrollWidth, document.querySelector('#lj-tabela').closest('.tabela-ramka').clientWidth]")
        ok(sz[0] <= sz[1], f"Lejek: tabela wszystkich kroków mieści się przy 1366 ({sz})")
        ok("tabela=wszystkie" in pg.evaluate("location.hash") and not pg.evaluate("document.getElementById('lj-reset').disabled"),
           "Lejek: zmiana trybu tabeli w adresie, przycisk aktywny")
        pg.click("#lj-reset"); pg.wait_for_timeout(900)
        ok(pg.evaluate("location.hash") == "#lejek" and pg.evaluate("document.getElementById('lj-reset').disabled"),
           "Lejek: „Przywróć domyślne” czyści adres")
        pg.goto(ADRES + "#lejek?a=2025-03-18_2025-05-16&b=2025-05-17_2025-07-15&tabela=wszystkie"); pg.wait_for_timeout(2500)
        w = tabela(pg, "#lj-tabela")
        porownaj(w, S_LJ_LUKA, ["Wybór usługi", "Wybór terminu", "Logowanie albo konto", "Wejście na płatność", "Płatność przyjęta", "Sesja do płatności"],
                 None, "Lejek, 60 dni przed i po godzinie bez danych")
        pg.goto(ADRES + "#lejek"); pg.wait_for_timeout(2000)
        pg.click("#lj-zd .zd-przycisk >> text=Awaria zakładania konta"); pg.wait_for_timeout(1200)
        zd = pg.evaluate("(document.querySelector('#lj-zd .zd-wynik')||{}).textContent || ''")
        ok(zd.startswith("„Awaria zakładania konta"), "Lejek: zdanie o zdarzeniu: " + zd[:200])
        ok(pg.evaluate("document.getElementById('lj-daty').hidden"), "Lejek: pola dat ukryte przy porównaniu z listy")
        pg.select_option("#f-preset", "wlasne"); pg.wait_for_timeout(600)
        ok(not pg.evaluate("document.getElementById('lj-daty').hidden"), "Lejek: pola dat widoczne przy „Własne daty”")
        # Lejek otwarty wprost: pasek przyklejony pod nagłówkiem, karta kroków nie chowa się pod paskiem po odnośniku
        p2 = ctx.new_page(); p2.goto(ADRES + "#lejek?pac=wszyscy"); p2.wait_for_timeout(2500)
        p2.evaluate("window.scrollTo(0, 1500)"); p2.wait_for_timeout(300)
        top = p2.evaluate("document.getElementById('lj-filtry').getBoundingClientRect().top")
        hn = p2.evaluate("document.querySelector('.naglowek').offsetHeight")
        ok(abs(top - hn) < 2, f"Lejek otwarty wprost: pasek przyklejony pod nagłówkiem (top {top}, nagłówek {hn})")
        p2.close()
        ok(not bledy, f"błędy w konsoli: {bledy[:3]}")
        b.close()
    linie = problemy + uwagi + ["", f"problemów: {len(problemy)}"]
    with open(os.path.join(KATALOG, "analiza", "wyniki", "g_kontrola_tabel.txt"), "w", encoding="utf-8") as f:
        f.write("G — zachowanie „Kohort” i „Lejka” i kolory tabel grup wobec g_istotnosc.json\n\n" + "\n".join(linie) + "\n")
    for x in linie:
        print(x)
    SERW.shutdown()


if __name__ == "__main__":
    main()
