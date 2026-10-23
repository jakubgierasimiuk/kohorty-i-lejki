"""Kontrola opublikowanej strony pod prawdziwym adresem (GitHub Pages); jedyny skrypt, który otwiera adres spoza 127.0.0.1.

Sprawdza: 9 zakładek przy 1366 px (komputer) i 375 px (telefon, emulacja dotyku), błędy w konsoli i strony,
przewijanie w bok, wczytanie wszystkich plików danych (status 200), żądania do innych adresów,
dwa odnośniki z filtrami (lejek i nowa tabela zdarzeń w „Kohortach”) wprost i po odświeżeniu,
znacznik noindex w HTML i nagłówki odpowiedzi. Zrzuty pierwszej zakładki do katalogu wyjściowego.

Użycie (z głównego folderu repozytorium, po każdym pushu, za zgodą Kuby na publikację):
    python -I analiza/f_strona_publiczna.py https://jakubgierasimiuk.github.io/kohorty-i-lejki/ <katalog wyjściowy poza repozytorium>
Wynik: <katalog>/wynik.json i zrzuty pierwszej zakładki; na ekranie podsumowanie i lista problemów.
"""
import json
import os
import sys
import urllib.request
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ADRES, WYJ = sys.argv[1].rstrip("/") + "/", sys.argv[2]
sys.path.insert(0, os.path.join(os.getcwd(), "analiza"))
import e_przegladarka as ep  # noqa: E402  (tylko stałe: lista zakładek i znaczniki gotowości)

HOST = urlparse(ADRES).netloc
LEJEK = ("#lejek?typ=zwykla&pac=nie_kupowal&podz=urzadzenie&krok=k5s&wygl=7&a=2024-10-01_2025-09-30"
         "&b=2025-10-01_2026-09-30&w=mobile%2Cdesktop%2Ctablet&lw=mobile")

STAN_JS = """() => {
  const sek = [...document.querySelectorAll('section')].find(s => !s.hidden && s.offsetParent !== null);
  const pola = sek ? [...sek.querySelectorAll('select, input')].map(e =>
      (e.id || e.name || e.className) + '=' + (e.type === 'checkbox' || e.type === 'radio' ? e.checked : e.value)) : [];
  const tyt = sek ? [...sek.querySelectorAll('h2, h3, .wykres-tytul, figcaption')].slice(0, 12).map(e => e.textContent.trim().slice(0, 80)) : [];
  return {hash: location.hash, sekcja: sek ? sek.id : null, pola, tyt, y: Math.round(scrollY)};
}"""


def main():
    sys.stdout.reconfigure(errors="replace")
    os.makedirs(WYJ, exist_ok=True)
    wynik = {"adres": ADRES, "problemy": []}
    # noindex i nagłówki
    with urllib.request.urlopen(ADRES, timeout=30) as r:
        html = r.read().decode("utf-8", errors="replace")
        wynik["status_html"] = r.status
        wynik["naglowki"] = {k: v for k, v in r.headers.items() if k.lower() in ("content-type", "x-robots-tag", "server", "cache-control")}
    wynik["noindex"] = 'name="robots" content="noindex' in html
    if not wynik["noindex"]:
        wynik["problemy"].append("brak noindex w HTML")
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", headless=True)
        for szer, wys, tel in ((1366, 900, False), (375, 812, True)):
            k = b.new_context(viewport={"width": szer, "height": wys}, is_mobile=tel, has_touch=tel)
            s = k.new_page()
            bledy, obce, dane = [], set(), {}
            s.on("pageerror", lambda e: bledy.append("pageerror: " + str(e)[:150]))
            s.on("console", lambda m: bledy.append("console: " + m.text[:150]) if m.type == "error" else None)

            def odp(r):
                u = urlparse(r.url)
                if u.netloc != HOST:
                    obce.add(u.netloc)
                if "/dane_strony/" in u.path:
                    dane[u.path.rsplit("/", 1)[-1]] = r.status
            s.on("response", odp)
            s.on("requestfailed", lambda rq: bledy.append("requestfailed: " + rq.url[:120]))
            s.goto(ADRES + "#wzrost", wait_until="load", timeout=60000)
            zak = []
            for z in ep.ZAKLADKI:
                s.goto(ADRES + "#" + z, timeout=60000)
                try:
                    s.wait_for_selector(ep.GOTOWE[z], timeout=30000)
                    gotowa = True
                except Exception:  # noqa: BLE001
                    gotowa = False
                s.wait_for_timeout(500)
                szer_dok = s.evaluate("[document.documentElement.scrollWidth, innerWidth]")
                zak.append({"zakladka": z, "gotowa": gotowa, "szerokosc": szer_dok})
                if not gotowa:
                    wynik["problemy"].append(f"{szer} px: zakładka {z} się nie narysowała")
                if szer_dok[0] > szer_dok[1] + 1:
                    wynik["problemy"].append(f"{szer} px: zakładka {z} przewija się w bok {szer_dok}")
            if szer == 1366:
                s.goto(ADRES + "#wzrost")
                s.wait_for_timeout(1500)
            s.goto(ADRES + "#wzrost")
            s.wait_for_selector(ep.GOTOWE["wzrost"], timeout=30000)
            s.wait_for_timeout(800)
            s.screenshot(path=os.path.join(WYJ, f"wzrost_{szer}.png"))
            # odnośniki z filtrami: lejek i pierwszy odnośnik „Pokaż na kohortach dziennych”
            s.goto(ADRES + "#kohorty")
            s.wait_for_selector(ep.GOTOWE["kohorty"], timeout=30000)
            href_koh = s.evaluate("""() => { const a = [...document.querySelectorAll('a')].find(a => a.textContent.includes('Pokaż na kohortach dziennych'));
                                       return a ? a.getAttribute('href') : null; }""")
            odn = []
            for h in (LEJEK, href_koh):
                if not h:
                    wynik["problemy"].append(f"{szer} px: nie znaleziono odnośnika z tabeli zdarzeń")
                    continue
                s.goto(ADRES + (h if h.startswith("#") else "#" + h.split("#", 1)[-1]))
                s.wait_for_timeout(2500)
                przed = s.evaluate(STAN_JS)
                s.reload(wait_until="load")
                s.wait_for_timeout(2500)
                po = s.evaluate(STAN_JS)
                ten_sam = przed["hash"] == po["hash"] and przed["pola"] == po["pola"] and przed["tyt"] == po["tyt"]
                odn.append({"odnosnik": h[:120], "ten_sam_stan_po_odswiezeniu": ten_sam, "sekcja": po["sekcja"],
                            "przewiniecie_przed_po": [przed["y"], po["y"]], "pola": len(po["pola"])})
                if not ten_sam:
                    wynik["problemy"].append(f"{szer} px: inny stan po odświeżeniu: {h[:60]}")
            brak_200 = {n: st for n, st in dane.items() if st != 200}
            if brak_200:
                wynik["problemy"].append(f"{szer} px: pliki danych bez statusu 200: {brak_200}")
            if obce:
                wynik["problemy"].append(f"{szer} px: żądania do innych adresów: {sorted(obce)}")
            if bledy:
                wynik["problemy"].append(f"{szer} px: błędy: {bledy[:5]}")
            wynik[f"{szer}px"] = {"zakladki": zak, "pliki_danych": dict(sorted(dane.items())), "liczba_plikow_danych": len(dane),
                                   "obce_adresy": sorted(obce), "bledy": bledy, "odnosniki": odn}
            k.close()
        b.close()
    with open(os.path.join(WYJ, "wynik.json"), "w", encoding="utf-8") as f:
        json.dump(wynik, f, ensure_ascii=False, indent=1)
    print("HTML:", wynik["status_html"], "| noindex:", wynik["noindex"], "| nagłówki:", wynik["naglowki"])
    for szer in ("1366px", "375px"):
        w = wynik[szer]
        print(f"{szer}: zakładki narysowane {sum(z['gotowa'] for z in w['zakladki'])}/9, pliki danych {w['liczba_plikow_danych']} "
              f"(wszystkie 200: {all(v == 200 for v in w['pliki_danych'].values())}), obce adresy {w['obce_adresy']}, błędy {len(w['bledy'])}")
        for o in w["odnosniki"]:
            print(f"   odnośnik {o['odnosnik'][:70]}… → ten sam stan po odświeżeniu: {o['ten_sam_stan_po_odswiezeniu']}, "
                  f"sekcja {o['sekcja']}, przewinięcie {o['przewiniecie_przed_po']}")
    print("PROBLEMY:", wynik["problemy"] or "brak")


if __name__ == "__main__":
    main()
