"""E — kontrola strony narzędzia w przeglądarce bez okna (runda E, część 3: wygląd).

Otwiera stronę z folderu narzedzie/ w Microsoft Edge bez okna (Playwright), na lokalnym serwerze 127.0.0.1 z losowym
portem, i sprawdza:
  1. wszystkie 9 zakładek przy szerokości 1366 px (komputer) i 375 px (telefon): czy się rysują, czy w konsoli nie ma
     błędów i czy strona nie przewija się w bok; zapisuje zrzut każdej zakładki;
  2. wszystkie odnośniki między zakładkami (#...): czy otwierają właściwą zakładkę, a odnośniki do pozycji priorytetów
     i zdarzeń podświetlają właściwą kartę;
  3. lejek: domyślnie „Jeszcze nie kupowali”, wykres kroków reaguje na filtry, wyróżnione jest jedno przejście.

Tryb --przyklad sprawdza nowy kształt danych z kontraktu (notatki/e_runda.md, punkt 3), zanim eksport zacznie go
dawać: przeglądarka dostaje dotychczasowe pliki dane_strony/*.js z dopisanym na końcu przekształceniem do nowego
kształtu (stare pola są usuwane, żeby strona nie mogła z nich skorzystać). Pliki na dysku się nie zmieniają, a teksty
w przykładzie to dotychczasowe teksty z danych przełożone mechanicznie (tytuły kart i znaczniki są przykładowe).

Uruchomienie z głównego folderu:
    python -I analiza/e_przegladarka.py --wyjscie <katalog na zrzuty i raport> [--przyklad]
Wynik: <katalog>/raport.txt i zrzuty <katalog>/<szerokość>_<zakładka>.png
"""
import argparse
import functools
import http.server
import os
import subprocess
import sys
import threading

from playwright.sync_api import sync_playwright

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARZEDZIE = os.path.join(KATALOG, "narzedzie")
ZAKLADKI = ["wzrost", "kohorty", "lejek", "po-zakupie", "zdarzenia", "wynik", "jakosc", "priorytety", "niewiadome"]
GOTOWE = {
    "wzrost": "#wz-nowy .karta, #wz-puenta p", "kohorty": "#ko-tabela tbody tr", "lejek": "#lj-tabela tbody tr",
    "po-zakupie": "#pz-tabela tbody tr", "zdarzenia": "#zd-lista article", "wynik": "#ek-tabela tbody tr",
    "jakosc": "#jk-mostek tbody tr", "priorytety": "#pr-karty article", "niewiadome": "#nw-tabela tbody tr",
}
SZEROKOSCI = [(1366, 900), (375, 812)]

# Przekształcenie dotychczasowych danych do nowego kształtu (tylko w przeglądarce, w trybie --przyklad).
# Dopisywane na końcu pliku danych; każde wywołanie usuwa stare pola, które nowy kształt zastępuje.
PRZYKLAD = {
    "c.js": r"""
(function () {
  var C = D.C, W = C.wzrost, P = C.priorytety;
  function ak(t) { return { typ: "akapit", tekst: t }; }
  function pk(l) { return { typ: "punkty", punkty: l }; }
  var liczbaZ = function (t) { var m = String(t).match(/[+−-]?\d[\d  ]*(,\d+)?\s?(%|tys\. zł|zł)?/); return m ? m[0].trim() : "—"; };
  var nowyW = {
    tytul: "Czy to, co widać na dashboardzie, jest wzrostem?",
    wstep: "Przykład nowego kształtu danych (test sesji wyglądu).",
    werdykt: { znacznik: { tekst: "Nie", stan: "zle" }, tekst: W.skrot.odpowiedz },
    kafelki: W.skrot.liczby.map(function (t, i) {
      return { liczba: liczbaZ(t), podpis: t.length > 70 ? t.slice(0, 70) + "…" : t, zmiana: i === 1 ? "spadek" : "wzrost", stan: i === 0 ? "dobrze" : "zle" };
    }),
    decyzje: { tytul: "Decyzje na pierwszy tydzień", punkty: W.skrot.decyzje.map(function (d, i) {
      var m = d.href.match(/p=(\d+)/); return { nr: i + 1, tekst: d.tekst.replace(/\s*\(pozycja \d+\);?\.?$/, ""), href: d.href, dopisek: m ? "pozycja " + m[1] : "" }; }) },
    karty: [
      { id: "pacjenci", tytul: "Więcej pacjentów", znacznik: { tekst: "Tak", stan: "dobrze" }, wniosek: W.pacjenci.punkty[0],
        tresc: [{ typ: "liczba", liczba: W.pacjenci.liczba, podpis: W.pacjenci.podpis, zmiana: "wzrost", stan: "dobrze" }],
        zastrzezenie: W.pacjenci.punkty[1], szczegoly: [pk(W.pacjenci.punkty.slice(2))], zrodlo: "przykład" },
      { id: "retencja", tytul: "Lepsza retencja", znacznik: { tekst: "Nie", stan: "zle" }, wniosek: W.retencja.punkty[0],
        tresc: [{ typ: "tabela", kolumny: ["Powrót w ciągu", "Rok wcześniej", "Ostatnie 12 miesięcy", "Zmiana"],
          wiersze: W.retencja.okna.map(function (o) { return { opis: o.dni + " dni", komorki: [{ tekst: o.tekst1.replace(/ \(.*/, ""), pod: o.tekst1.replace(/^.*\(|\)$/g, "") },
            o.tekst2, { tekst: o.zmiana, zmiana: o.p2 >= o.p1 ? "wzrost" : "spadek", stan: o.p2 >= o.p1 ? "dobrze" : "zle" }] }; }) }],
        szczegoly: [ak(W.retencja.punkty[1]), pk(W.retencja.punkty.slice(2))], linki: W.linki.slice(0, 2), zrodlo: W.zrodlo },
      { id: "telemedigo", tytul: W.telemedigo.tytul, znacznik: { tekst: "Uwaga", stan: "uwaga" }, wniosek: W.telemedigo.puenta,
        tresc: [{ typ: "tabela", tytul: "Typy zakupu", kolumny: W.telemedigo.tabela.kolumny,
          wiersze: W.telemedigo.tabela.wiersze.map(function (r, i, a) { return { opis: r.opis, komorki: r.komorki, podsuma: i === a.length - 1 }; }) }],
        szczegoly: [pk(W.telemedigo.punkty)], linki: W.telemedigo.linki, zrodlo: W.telemedigo.zrodlo },
      { id: "wynik", tytul: W.kwartaly.naglowek, wniosek: W.zamkniecie,
        tresc: [ak(W.safari), { typ: "podtytul", tekst: W.kwartaly.rozklad_tytul }, ak(W.kwartaly.rozklad_wstep), pk(W.kwartaly.rozklad_punkty)],
        zastrzezenie: W.kwartaly.luka, szczegoly: [ak(W.kwartaly.baza)], zrodlo: "przykład" },
      { id: "zastrzezenia", tytul: "Najważniejsze zastrzeżenia", tresc: [{ typ: "numerowane", punkty: W.zastrzezenia.map(function (x) { return x.tytul + " " + x.tekst; }) }] },
      { id: "mostek", tytul: "Dashboard a dane oczyszczone", wniosek: D.P.wzrost.dashboard.zdanie, wstaw: "mostek" }
    ],
    zrodlo: W.zrodlo
  };
  C.wzrost = nowyW;
  var poziom = function (s) { var m = String(s).match(/^(wysoka|średnia|niska)/i); return m ? (m[1].toLowerCase() === "średnia" ? "srednia" : m[1].toLowerCase()) : (/test/.test(s) ? "test" : "srednia"); };
  var POZ = { wysoka: "Wysoka", srednia: "Średnia", niska: "Niska", test: "Test" };
  P.przeglad = P.przeglad.map(function (r) {
    var p = poziom(r.pewnosc), m = r.ile.match(/^[^(;,]*/);
    return { nr: r.nr, co: r.co, ile: (m ? m[0] : r.ile).trim(), ile_dopisek: r.ile.slice(m ? m[0].length : 0).replace(/^[\s;,]+/, ""),
      pewnosc: { poziom: p, tekst: POZ[p], dopisek: r.pewnosc.replace(/^(wysoka|średnia|niska)[:,]?\s*/i, "") }, wdrozenie: r.wdrozenie };
  });
  var przeg = {}; P.przeglad.forEach(function (r) { przeg[r.nr] = r; });
  P.karty = P.karty.map(function (k) {
    var r = przeg[k.nr];
    return { nr: k.nr, tytul: k.tytul, wniosek: k.sekcje[0].punkty[0],
      pasek: { ile: r.ile, ile_dopisek: r.ile_dopisek, pewnosc: r.pewnosc, wdrozenie: r.wdrozenie },
      sekcje: k.sekcje.slice(1), tabela: k.tabela, szczegoly: [pk(k.sekcje[0].punkty.slice(1))], linki: k.linki, zrodlo: k.zrodlo };
  });
  P.zasady = { tytul: "Zasady listy", wniosek: P.zasady[0], tresc: [pk(P.zasady.slice(1, 4))], szczegoly: [pk(P.zasady.slice(4)), ak(P.definicje)] };
  delete P.definicje;
  P.nie_robimy = { tytul: "Czego proponujemy teraz nie robić", tresc: [pk(P.nie_robimy)] };
})();
""",
    "podsumowanie.js": r"""
(function () {
  var N = D.P.lejek_naglowek;
  N.karta = { tytul: "Przykład: nagłówek lejka jako karta", wniosek: N.zdania[0], tresc: N.zdania.slice(1, 2).map(function (t) { return { typ: "akapit", tekst: t }; }),
    zastrzezenie: N.zdania[2] || null, szczegoly: N.zdania.slice(3).map(function (t) { return { typ: "akapit", tekst: t }; }), zrodlo: "przykład" };
  N.naprawy_karty = N.naprawy.map(function (x) { return { tytul: x.tytul, znacznik: { tekst: "Do naprawy", stan: "zle" }, wniosek: x.tekst,
    linki: [{ tekst: "Pokaż w lejku", href: x.link }] }; });
  N.osobne_karta = { tresc: [{ typ: "punkty", punkty: N.osobne }] };
  delete N.zdania; delete N.naprawy; delete N.osobne;
})();
""",
    "kohorty.js": r"""
(function () {
  var K = D.kohorty;
  K.karta = { tytul: "Przykład: nagłówek kohort jako karta", znacznik: { tekst: "Gorzej", stan: "zle" }, wniosek: K.zdania[0],
    tresc: K.zdania.slice(1, 2).map(function (t) { return { typ: "akapit", tekst: t }; }),
    szczegoly: K.zdania.slice(2).map(function (t) { return { typ: "akapit", tekst: t }; }), zrodlo: "przykład" };
  delete K.zdania;
})();
""",
    "po_zakupie.js": r"""
(function () {
  var Z = D.po_zakupie;
  ["punktualnosc", "ruch", "zwroty", "oceny"].forEach(function (k) {
    var z = Z["zdania_" + k];
    Z.karty = Z.karty || {};
    Z.karty[k] = { tytul: "Przykład: " + k, wniosek: z[0], tresc: z.slice(1, 2).map(function (t) { return { typ: "akapit", tekst: t }; }),
      szczegoly: z.slice(2).map(function (t) { return { typ: "akapit", tekst: t }; }), zrodlo: "przykład" };
    delete Z["zdania_" + k];
  });
})();
""",
    "wynik.js": r"""
(function () {
  var Y = D.wynik;
  Y.karta = { tytul: "Przykład: wynik biznesu", wniosek: Y.zdania[0], szczegoly: Y.zdania.slice(1).map(function (t) { return { typ: "akapit", tekst: t }; }) };
  Y.ekonomia.karta = { tytul: "Przykład: ekonomia kampanii", wniosek: Y.ekonomia.zdania[0],
    zastrzezenie: Y.ekonomia.zdania[1] || null, szczegoly: Y.ekonomia.zdania.slice(2).map(function (t) { return { typ: "akapit", tekst: t }; }) };
  delete Y.zdania; delete Y.ekonomia.zdania;
})();
""",
    "jakosc.js": r"""
(function () {
  var J = D.jakosc;
  J.karty = { mostek: { tytul: "Przykład: mostek", wniosek: "Przykład wniosku nad tabelą mostka.", wstaw: "mostek" } };
  J.karta = { tytul: "Przykład: wstęp zakładki jakości", wniosek: "Przykład wniosku wstępu." };
  J.karty.duplikaty = { tytul: "Przykład: duplikaty", wniosek: J.duplikaty.zdania[0], szczegoly: J.duplikaty.zdania.slice(1).map(function (t) { return { typ: "akapit", tekst: t }; }) };
  J.karty.testy = { tytul: "Przykład: zamówienia testowe", wniosek: J.testy.zdania[0], szczegoly: J.testy.zdania.slice(1).map(function (t) { return { typ: "akapit", tekst: t }; }) };
  J.karty.godzina = { tytul: "Przykład: godzina bez danych", wniosek: J.godzina.zdanie };
  J.karty.drobne = { tytul: "Przykład: drobne niespójności", tresc: [{ typ: "punkty", punkty: J.drobne }] };
  J.karty.czyste = { tytul: "Przykład: sprawdzone i czyste", tresc: [{ typ: "punkty", punkty: J.czyste }] };
  delete J.duplikaty.zdania; delete J.testy.zdania; delete J.godzina.zdanie; delete J.drobne; delete J.czyste;
})();
""",
}

# Sprawdzenie odnośników: po zmianie adresu — czy widać właściwą zakładkę i czy cel jest podświetlony.
SPRAWDZ_ODNOSNIK = r"""
(h) => {
  const nazwa = h.slice(1).split('?')[0] || 'wzrost';
  const v = document.getElementById('v-' + nazwa);
  const q = new URLSearchParams(h.split('?')[1] || '');
  const out = { widok: !!v && !v.hidden };
  if (q.get('p')) { const e = document.getElementById('pr-' + q.get('p')); out.cel = !!e && e.classList.contains('podswietlone'); }
  if (q.get('z')) { const e = document.getElementById('zd-' + q.get('z')); out.cel = !!e && e.classList.contains('podswietlone'); }
  if (nazwa === 'lejek' && [...q.keys()].length) out.cel = document.querySelectorAll('#lj-tabela tbody tr').length > 0 && document.querySelectorAll('#lj-kroki .lk-krok').length > 0;
  return out;
}
"""


class CichyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def serwer():
    obsluga = functools.partial(CichyHandler, directory=NARZEDZIE)
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), obsluga)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def z_gita(rewizja, nazwa):
    """Plik danych strony w wersji z podanego commitu (np. HEAD), bez zmiany plików na dysku."""
    wynik = subprocess.run(["git", "-C", KATALOG, "show", f"{rewizja}:narzedzie/dane_strony/{nazwa}"],
                           capture_output=True, timeout=60)
    if wynik.returncode:
        raise RuntimeError(wynik.stderr.decode("utf-8", "replace"))
    return wynik.stdout.decode("utf-8")


def obsluga_danych(rewizja, przyklad):
    """Podstawia pliki dane_strony/*.js: z commitu (--dane-z-gita) i/lub z dopisanym przekształceniem (--przyklad)."""
    def podstaw(route):
        nazwa = route.request.url.rsplit("/", 1)[-1].split("?")[0]
        if rewizja:
            tresc = z_gita(rewizja, nazwa)
        else:
            tresc = route.fetch().text()
        if przyklad and nazwa in PRZYKLAD:
            tresc += "\n" + PRZYKLAD[nazwa]
        route.fulfill(status=200, body=tresc, headers={"content-type": "text/javascript; charset=utf-8", "cache-control": "no-store"})
    return podstaw


def main():
    sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--wyjscie", required=True, help="katalog na zrzuty i raport (poza repozytorium)")
    ap.add_argument("--przyklad", action="store_true", help="nowy kształt danych z kontraktu, podstawiony w przeglądarce")
    ap.add_argument("--dane-z-gita", metavar="REWIZJA", help="pliki dane_strony/ z tego commitu (np. HEAD), zamiast z dysku")
    ap.add_argument("--bez-zrzutow", action="store_true")
    arg = ap.parse_args()
    os.makedirs(arg.wyjscie, exist_ok=True)
    s = serwer()
    adres = f"http://127.0.0.1:{s.server_address[1]}/"
    raport, problemy = [], []
    tryb = ("dane z commitu " + arg.dane_z_gita if arg.dane_z_gita else "dane z dane_strony/ na dysku") + \
        (", przekształcone do nowego kształtu (przykład podstawiony w przeglądarce)" if arg.przyklad else "")
    raport.append(f"Kontrola strony w Edge bez okna, {adres}, tryb: {tryb}")

    with sync_playwright() as p:
        przegl = p.chromium.launch(channel="msedge", headless=True)
        for szer, wys in SZEROKOSCI:
            kontekst = przegl.new_context(viewport={"width": szer, "height": wys})
            if arg.przyklad or arg.dane_z_gita:
                kontekst.route("**/dane_strony/*.js*", obsluga_danych(arg.dane_z_gita, arg.przyklad))
            strona = kontekst.new_page()
            bledy = []
            strona.on("pageerror", lambda e: bledy.append("błąd strony: " + str(e)))
            strona.on("console", lambda m: bledy.append("konsola: " + m.text) if m.type == "error" else None)
            strona.goto(adres + "#wzrost")
            raport.append(f"\n== Szerokość {szer} px ==")
            hrefy = set()
            for z in ZAKLADKI:
                strona.evaluate(f"location.hash = '{z}'")
                try:
                    strona.wait_for_selector(GOTOWE[z], timeout=30000)
                except Exception as e:  # noqa: BLE001
                    problemy.append(f"{szer} px, {z}: zakładka się nie narysowała ({e.__class__.__name__})")
                    continue
                strona.wait_for_timeout(700)
                m = strona.evaluate("""() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth,
                    h: document.documentElement.scrollHeight,
                    szersze: [...document.querySelectorAll('main *')].filter(e => { const r = e.getBoundingClientRect();
                      return r.width > 0 && r.right > window.innerWidth + 1 && !e.closest('.tabela-ramka, .zakladki, .macierz-ramka'); })
                      .slice(0, 5).map(e => e.tagName + (e.id ? '#' + e.id : '') + '.' + e.className)})""")
                bok = m["sw"] > m["iw"] + 1
                raport.append(f"{z:12s} wysokość {m['h']:6d} px, szerokość dokumentu {m['sw']} / okno {m['iw']}"
                              + (" — PRZEWIJA SIĘ W BOK" if bok else ""))
                if bok or m["szersze"]:
                    problemy.append(f"{szer} px, {z}: wychodzi poza ekran: {m['szersze']}")
                hrefy |= set(strona.evaluate(f"""() => [...document.querySelectorAll('#v-{z} a[href^="#"]')].map(a => a.getAttribute('href'))"""))
                if not arg.bez_zrzutow:
                    strona.screenshot(path=os.path.join(arg.wyjscie, f"{szer}_{z}.png"), full_page=True)
            # lejek: domyślne „Kto” i wykres kroków
            strona.evaluate("location.hash = 'lejek'")
            strona.wait_for_selector("#lj-kroki .lk-krok")
            strona.wait_for_timeout(300)
            lj = strona.evaluate("""() => ({kto: document.getElementById('f-pac').value,
                kroki: document.querySelectorAll('#lj-kroki .lk-krok').length,
                najgorsze: document.querySelectorAll('#lj-kroki .lk-najgorsze').length,
                tytul: document.getElementById('lj-kroki-tytul').innerText})""")
            raport.append(f"lejek: Kto = {lj['kto']}, kroków {lj['kroki']}, wyróżnionych przejść {lj['najgorsze']}, tytuł: {lj['tytul']}")
            if lj["kto"] != "nie_kupowal" or lj["kroki"] < 2 or lj["najgorsze"] > 1:
                problemy.append(f"{szer} px, lejek: {lj}")
            strona.select_option("#f-podz", "urzadzenie")
            strona.wait_for_timeout(800)
            strona.select_option("#f-lw", "mobile")
            strona.wait_for_timeout(300)
            lj2 = strona.evaluate("() => document.getElementById('lj-kroki-tytul').innerText + ' | ' + location.hash")
            raport.append(f"lejek po filtrze (urządzenie = telefon): {lj2}")
            if "Telefon" not in lj2:
                problemy.append(f"{szer} px, lejek nie reaguje na filtr: {lj2}")
            if not arg.bez_zrzutow:
                strona.locator("#lj-kroki-karta").screenshot(path=os.path.join(arg.wyjscie, f"{szer}_lejek_kroki_telefon.png"))
            # odnośniki między zakładkami (raz, na pierwszej szerokości; zakładki są te same)
            zle = []
            for h in (sorted(hrefy) if szer == SZEROKOSCI[0][0] else []):
                if h in ("#", ""):
                    continue
                strona.evaluate("h => { location.hash = h.slice(1); }", h)
                strona.wait_for_timeout(700 if h.startswith("#lejek") else 250)
                w = strona.evaluate(SPRAWDZ_ODNOSNIK, h)
                if not w["widok"] or w.get("cel") is False:
                    zle.append(f"{h} → {w}")
            if szer == SZEROKOSCI[0][0]:
                raport.append(f"odnośniki między zakładkami: {len(hrefy)} sprawdzonych, niedziałających {len(zle)}")
            problemy += [f"{szer} px, odnośnik: {x}" for x in zle]
            raport.append(f"błędy w konsoli: {len(bledy)}")
            problemy += [f"{szer} px, {b}" for b in bledy[:20]]
            kontekst.close()
        przegl.close()
    s.shutdown()
    raport.append("\n== Problemy ==")
    raport += problemy or ["brak"]
    tekst = "\n".join(raport) + "\n"
    with open(os.path.join(arg.wyjscie, "raport.txt"), "w", encoding="utf-8") as f:
        f.write(tekst)
    print(tekst)


if __name__ == "__main__":
    main()
