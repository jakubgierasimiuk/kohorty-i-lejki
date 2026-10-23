"""G — szybka kontrola „Czego nie wiemy” i „Priorytetów” po grupowaniu pytań i karcie zakresu listy (2026-10-23).

Edge bez okna, strona z folderu narzedzie/ na 127.0.0.1 (losowy port). Sprawdza: sześć nagłówków grup i 21 pytań, każde raz;
odnośniki #niewiadome?n=<nr> z pierwszej zakładki i kart priorytetów (podświetlony wiersz na ekranie, także po filtrze,
który go ukrywał); filtr pozycji chowa puste grupy; karta zakresu listy z „Nie robimy teraz” nad przeglądem priorytetów
i brak osobnej karty „Nie robimy teraz”; odnośnik #priorytety?p=9; błędy w konsoli; przy 1366 i 375 px.

Uruchomienie z głównego folderu: python -I analiza/g_kontrola_niewiadomych.py
Wynik na ekranie i w analiza/wyniki/g_kontrola_niewiadomych.txt."""
import functools
import http.server
import os
import sys
import threading

from playwright.sync_api import sync_playwright

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Cichy(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    sys.stdout.reconfigure(errors="replace")
    serw = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Cichy, directory=os.path.join(KATALOG, "narzedzie")))
    threading.Thread(target=serw.serve_forever, daemon=True).start()
    adres = f"http://127.0.0.1:{serw.server_address[1]}/"
    wyn = []

    def ok(war, opis):
        wyn.append(("OK   " if war else "BŁĄD ") + opis)

    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", headless=True)
        for szer, wys, tel in ((1366, 900, False), (375, 812, True)):
            ctx = b.new_context(viewport={"width": szer, "height": wys}, is_mobile=tel, has_touch=tel, locale="pl-PL")
            pg = ctx.new_page()
            bledy = []
            pg.on("pageerror", lambda e: bledy.append(str(e)))
            pg.on("console", lambda m: bledy.append(m.text) if m.type == "error" else None)
            pg.goto(adres + "#niewiadome")
            pg.wait_for_selector("#nw-tabela tbody tr")
            gr = pg.evaluate("[...document.querySelectorAll('#nw-tabela tr.oddzielnik')].map(x => x.textContent)")
            nry = pg.evaluate("[...document.querySelectorAll('#nw-tabela tbody tr:not(.oddzielnik)')].map(x => +x.id.slice(3))")
            ok(len(gr) == 6, f"{szer} px: 6 nagłówków grup ({len(gr)}: {' | '.join(gr)})")
            ok(sorted(nry) == list(range(1, 22)), f"{szer} px: 21 pytań, każde raz ({len(nry)})")
            for n in (1, 4, 8, 19):
                pg.goto(adres + "#niewiadome?n=" + str(n))
                pg.wait_for_timeout(900)
                s = pg.evaluate(f"(() => {{ const e = document.getElementById('nw-{n}'); const r = e.getBoundingClientRect();"
                                f" return [e.classList.contains('podswietlone'), Math.round(r.top), innerHeight, e.hidden]; }})()")
                ok(s[0] and not s[3] and -5 <= s[1] < s[2] * 0.7, f"{szer} px: #niewiadome?n={n} podświetla wiersz na ekranie ({s})")
            pg.goto(adres + "#niewiadome")
            pg.wait_for_timeout(500)
            pg.select_option("#nw-filtr-pozycja", "1")
            pg.wait_for_timeout(300)
            widoczne = pg.evaluate("[...document.querySelectorAll('#nw-tabela tbody tr')].filter(x => !x.hidden).map(x => x.className + ':' + (x.id || x.textContent.slice(0, 20)))")
            ok(widoczne and all(("oddzielnik" in w) or w.endswith(("nw-6", "nw-7")) for w in widoczne) and sum("oddzielnik" in w for w in widoczne) == 1,
               f"{szer} px: filtr pozycji 1 zostawia pytania 6 i 7 i jeden nagłówek grupy ({widoczne})")
            pg.select_option("#nw-filtr-pozycja", "")
            pg.goto(adres + "#priorytety")
            pg.wait_for_selector("#pr-karty article")
            st = pg.evaluate("""(() => { const k = document.getElementById('pr-zasady-karta'), p = document.getElementById('pr-przeglad-karta');
              return [!!k && k.tagName, !!k && !!k.querySelector('h3') && k.querySelector('h3').textContent, !!k && k.querySelectorAll('ul.punkty li').length,
                !!k && !!k.querySelector('details.zasady-zwiniete'), !!k && !!p && (k.compareDocumentPosition(p) & 4) > 0,
                document.getElementById('pr-nie-robimy-miejsce').hidden]; })()""")
            ok(st[0] == "ARTICLE" and st[1] and st[2] >= 1 and st[3] and st[4] and st[5],
               f"{szer} px: karta zakresu listy nad przeglądem, „Nie robimy teraz” w niej, zasady zwinięte, bez osobnej karty na dole ({st})")
            pg.goto(adres + "#priorytety?p=9")
            pg.wait_for_timeout(3000)   # płynne przewinięcie na długiej stronie (karta 9 jest kilka ekranów niżej)
            s = pg.evaluate("(() => { const e = document.getElementById('pr-9'); const r = e.getBoundingClientRect(); return [e.classList.contains('podswietlone'), Math.round(r.top), innerHeight]; })()")
            ok(s[0] and -5 <= s[1] < s[2] * 0.7, f"{szer} px: #priorytety?p=9 podświetla kartę pozycji 9 na ekranie ({s})")
            sw = pg.evaluate("[document.documentElement.scrollWidth, innerWidth]")
            ok(sw[0] <= sw[1], f"{szer} px: bez przewijania w bok ({sw})")
            ok(not bledy, f"{szer} px: błędy w konsoli: {bledy[:3]}")
            ctx.close()
        b.close()
    serw.shutdown()
    zle = [w for w in wyn if w.startswith("BŁĄD")]
    linie = wyn + ["", f"problemów: {len(zle)}"]
    with open(os.path.join(KATALOG, "analiza", "wyniki", "g_kontrola_niewiadomych.txt"), "w", encoding="utf-8") as f:
        f.write("G — „Czego nie wiemy” (grupy) i „Priorytety” (karta zakresu listy)\n\n" + "\n".join(linie) + "\n")
    for x in linie:
        print(x)


if __name__ == "__main__":
    main()
