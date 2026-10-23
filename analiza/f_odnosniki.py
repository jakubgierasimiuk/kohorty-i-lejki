"""F — odnośniki z parametrami w adresie po otwarciu wprost i po odświeżeniu (ostatnia kontrola przed publikacją, część 2).

Otwiera stronę z folderu narzedzie/ w Microsoft Edge bez okna (Playwright, 127.0.0.1) przy szerokości 1366 px i:
  1. zbiera z wyrenderowanych zakładek wszystkie odnośniki z parametrami w adresie (#kohorty?…, #lejek?…,
     #priorytety?p=…, #niewiadome?n=…, #zdarzenia?z=… i pozostałe), także te w zwiniętych sekcjach i w tabelach;
  2. każdy otwiera wprost w nowej karcie, zapisuje stan (zakładka, adres po wczytaniu, wartości wszystkich pól filtrów
     zakładki, podświetlona karta i jej położenie na ekranie), odświeża stronę i porównuje stan; sprawdza też, czy stan
     zgadza się z parametrami odnośnika (filtry z adresu w polach i w adresie, podświetlona właściwa karta, karta na ekranie);
  3. zmienia filtry w interfejsie na każdej zakładce i sprawdza, czy adres się zmienia i czy stan wraca po odświeżeniu
     (strona zapisuje w adresie tylko filtry kohort i lejka; pozostałe opisujemy jako stan rzeczy);
  4. sprawdza przyciski wstecz i dalej: między zakładkami, po odnośniku z filtrami i po zmianie filtra.
Wynik: analiza/wyniki/f_odnosniki.txt

Uruchomienie z głównego folderu (kilka minut):
    python -I analiza/f_odnosniki.py
"""
import datetime as dt
import functools
import http.server
import os
import subprocess
import sys
import threading
from urllib.parse import parse_qsl

from playwright.sync_api import sync_playwright

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARZEDZIE = os.path.join(KATALOG, "narzedzie")
RAPORT = os.path.join(KATALOG, "analiza", "wyniki", "f_odnosniki.txt")
ZAKLADKI = ["wzrost", "kohorty", "lejek", "po-zakupie", "zdarzenia", "wynik", "jakosc", "priorytety", "niewiadome"]
GOTOWE = {
    "wzrost": "#wz-nowy .schodki .wk-wiersz", "kohorty": "#ko-macierz tbody tr", "lejek": "#lj-kroki .lk-krok",
    "po-zakupie": "#pz-karta-godziny .kolumny .kl-grupa", "zdarzenia": "#zd-lista .zdarzenie", "wynik": "#ek-wykres .wk-wiersz, #ek-wykres .lejek-pusty",
    "jakosc": "#jk-testy-kw .slupek-wiersz", "priorytety": "#pr-karty article", "niewiadome": "#nw-tabela tbody tr",
}
# klucz parametru w adresie → pole filtra na stronie
POLA = {
    "lejek": {"typ": "f-typ", "pac": "f-pac", "podz": "f-podz", "krok": "f-krok", "wygl": "f-wygl", "lw": "f-lw"},
    "kohorty": {"regula": "ko-regula", "podz": "ko-podz", "okno": "ko-okno", "miara": "ko-miara", "wygl": "ko-wygl"},
}
CEL = {"p": "pr-", "z": "zd-", "n": "nw-"}

LINKI = r"""
(z) => [...document.querySelectorAll('#v-' + z + ' a[href^="#"]')].map(a => ({ href: a.getAttribute('href'),
  gdzie: ((a.closest('article') && (a.closest('article').querySelector('h3, h2') || {}).textContent) || '').trim().slice(0, 60),
  tekst: (a.textContent || '').trim().slice(0, 60) })).filter(x => x.href.includes('?'))
"""
STAN = r"""
() => {
  const s = [...document.querySelectorAll('section.widok')].find(x => !x.hidden);
  const kontrolki = {};
  if (s) s.querySelectorAll('select, input').forEach(e => { if (e.id) kontrolki[e.id] = e.type === 'checkbox' ? e.checked : e.value; });
  const pod = [...document.querySelectorAll('.podswietlone')].filter(e => !e.closest('[hidden]') && !e.hidden).map(e => {
    const r = e.getBoundingClientRect(); return { id: e.id, top: Math.round(r.top), dol: Math.round(r.bottom) }; });
  const kroki = document.getElementById('lj-kroki-karta'), dzienny = document.getElementById('ko-wykres-karta');
  const pr = document.getElementById('ko-preset');
  return { hash: decodeURIComponent(location.hash), widok: s ? s.id.slice(2) : null, kontrolki, pod, scrollY: Math.round(scrollY), ih: innerHeight,
    krokiTop: kroki && s && s.id === 'v-lejek' ? Math.round(kroki.getBoundingClientRect().top) : null,
    krokiTytul: (document.getElementById('lj-kroki-tytul') || {}).textContent || null,
    dziennyTop: dzienny && s && s.id === 'v-kohorty' ? Math.round(dzienny.getBoundingClientRect().top) : null,
    presetOpcja: pr && pr.selectedOptions && pr.selectedOptions[0] ? pr.selectedOptions[0].textContent : null };
}
"""


class CichyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def nazwa_z(href):
    return href[1:].split("?")[0] or "wzrost"


def czekaj(pg, z):
    pg.wait_for_selector(GOTOWE.get(z, "body"), timeout=30000, state="attached")
    pg.wait_for_timeout(1200)     # przewinięcie do karty (scrollIntoView z animacją) i dorysowanie wykresów


# runda G: adres zapisuje tylko ustawienia inne niż startowe (założenie 90), więc parametr równy wartości startowej może
# zniknąć z adresu; pole filtra dalej musi mieć wartość z odnośnika
DOMYSLNE = {"kohorty": {"regula": "Z1K", "podz": "grupa", "okno": "90", "miara": "powrot", "wygl": "7",
                        "a": "2024-10-01_2025-09-30", "b": "2025-10-01_2026-09-30"},
            "lejek": {"typ": "zwykla", "pac": "nie_kupowal", "podz": "przegladarka", "krok": "k5s", "wygl": "7",
                      "a": "2024-10-01_2025-09-30", "b": "2025-10-01_2026-09-30", "w": "calosc"}}


def oczekiwania(href, s):
    """Lista (opis, ok) — czy stan po wczytaniu zgadza się z parametrami odnośnika."""
    z = nazwa_z(href)
    q = dict(parse_qsl(href.split("?", 1)[1], keep_blank_values=True))
    wyn = [("zakładka z odnośnika", s["widok"] == z)]
    adres = dict(parse_qsl(s["hash"].split("?", 1)[1], keep_blank_values=True)) if "?" in s["hash"] else {}
    if z in POLA:
        for k, v in q.items():
            if k in ("a", "b", "w") or k.startswith("f_") or k in POLA[z]:
                if DOMYSLNE.get(z, {}).get(k) == v and k not in adres:
                    wyn.append((f"parametr {k}={v} (wartość startowa) może zniknąć z adresu", True))
                else:
                    wyn.append((f"parametr {k}={v} zostaje w adresie", adres.get(k) == v))
            if k in POLA[z]:
                wyn.append((f"pole {POLA[z][k]} = {v}", str(s["kontrolki"].get(POLA[z][k])) == v))
            if k.startswith("f_"):
                wyn.append((f"zawężenie ko-f-{k[2:]} = {v}", str(s["kontrolki"].get("ko-f-" + k[2:])) == v))
        if z == "lejek":
            wyn.append(("wykres kroków na ekranie (przewinięcie)", s["krokiTop"] is not None and -5 <= s["krokiTop"] < s["ih"] * 0.6))
        if z == "kohorty":
            # runda F: odnośnik z filtrami przewija do wykresu dzień po dniu (pod tabelą zdarzeń na górze zakładki)
            wyn.append(("wykres dzień po dniu na ekranie (przewinięcie)", s["dziennyTop"] is not None and -5 <= s["dziennyTop"] < s["ih"] * 0.6))
            if "a" in q and "b" in q:
                a0, a1 = (dt.date.fromisoformat(x) for x in q["a"].split("_"))
                b0, b1 = (dt.date.fromisoformat(x) for x in q["b"].split("_"))
                if (a1 - a0).days == 59 and (b0 - a1).days == 1 and (b1 - b0).days == 59:
                    # okna „60 dni przed i po” dniu b0: na liście porównań pozycja tego zdarzenia, a nie „własne daty”
                    wyn.append((f"porównanie „60 dni przed i po” zdarzeniu z {b0:%d.%m.%Y}", str(s["kontrolki"].get("ko-preset", "")).startswith("zd:")
                                and (s["presetOpcja"] or "").endswith(f"({b0.day}.{b0:%m.%Y})")))
    for k, pref in CEL.items():
        if k in q:
            cel = pref + q[k]
            p = [x for x in s["pod"] if x["id"] == cel]
            wyn.append((f"podświetlona karta {cel}", bool(p)))
            wyn.append((f"karta {cel} na ekranie (przewinięcie)", bool(p) and p[0]["top"] < s["ih"] * 0.6 and p[0]["dol"] > 0))
    return wyn


def porownaj(s1, s2):
    """Różnice stanu po otwarciu wprost i po odświeżeniu (bez położenia w pikselach, które sprawdza oczekiwania)."""
    roz = []
    for k in ("hash", "widok", "krokiTytul"):
        if s1[k] != s2[k]:
            roz.append(f"{k}: {s1[k]} → {s2[k]}")
    for k in sorted(set(s1["kontrolki"]) | set(s2["kontrolki"])):
        if s1["kontrolki"].get(k) != s2["kontrolki"].get(k):
            roz.append(f"pole {k}: {s1['kontrolki'].get(k)} → {s2['kontrolki'].get(k)}")
    if [x["id"] for x in s1["pod"]] != [x["id"] for x in s2["pod"]]:
        roz.append(f"podświetlenie: {[x['id'] for x in s1['pod']]} → {[x['id'] for x in s2['pod']]}")
    return roz


def zmien(pg, sel, wartosc=None, etykieta=None):
    if wartosc is not None:
        pg.evaluate("([s, v]) => { const e = document.querySelector(s); e.value = v; e.dispatchEvent(new Event('change', { bubbles: true })); }", [sel, wartosc])
    else:
        pg.click(sel)
    pg.wait_for_timeout(1500)


def main():
    sys.stdout.reconfigure(errors="replace")
    serw = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(CichyHandler, directory=NARZEDZIE))
    threading.Thread(target=serw.serve_forever, daemon=True).start()
    adres = f"http://127.0.0.1:{serw.server_address[1]}/"
    L, problemy, bledy = [], [], []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", headless=True)
        ctx = b.new_context(viewport={"width": 1366, "height": 900})
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: bledy.append(str(e)))
        # 1. zbieranie odnośników
        pg.goto(adres + "#wzrost")
        linki = {}
        for z in ZAKLADKI:
            pg.evaluate(f"location.hash = '{z}'")
            czekaj(pg, z)
            for x in pg.evaluate(LINKI, z):
                linki.setdefault(x["href"], []).append((z, x["gdzie"], x["tekst"]))
        pg.close()
        rodzaje = {}
        for h in linki:
            k = nazwa_z(h) + "?" + "&".join(sorted({kv.split("=")[0] for kv in h.split("?", 1)[1].split("&")}))
            rodzaje[k] = rodzaje.get(k, 0) + 1
        L.append(f"1. Odnośniki z parametrami: {len(linki)} różnych adresów (z {sum(len(v) for v in linki.values())} miejsc na stronie).")
        for k, n in sorted(rodzaje.items(), key=lambda x: -x[1]):
            L.append(f"   {n:4} × {k}")
        # 2. każdy odnośnik: otwarcie wprost i odświeżenie
        n_ok = n_spr = 0
        wiersze = []
        for i, (h, skad) in enumerate(sorted(linki.items())):
            z = nazwa_z(h)
            t = ctx.new_page()
            t.on("pageerror", lambda e: bledy.append(str(e)))
            t.goto(adres + h)
            czekaj(t, z)
            s1 = t.evaluate(STAN)
            t.reload()
            czekaj(t, z)
            s2 = t.evaluate(STAN)
            t.close()
            roz = porownaj(s1, s2)
            ocz1, ocz2 = oczekiwania(h, s1), oczekiwania(h, s2)
            zle = [f"po otwarciu: {o}" for o, ok in ocz1 if not ok] + [f"po odświeżeniu: {o}" for o, ok in ocz2 if not ok] + [f"stan się zmienił: {r}" for r in roz]
            n_spr += len(ocz1) + len(ocz2) + 1
            n_ok += sum(ok for _, ok in ocz1) + sum(ok for _, ok in ocz2) + (not roz)
            wiersze.append(f"   {'OK ' if not zle else 'ŹLE'} {h[:150]}  [z: {skad[0][0]} / {skad[0][1][:40]}{' i ' + str(len(skad) - 1) + ' innych' if len(skad) > 1 else ''}]")
            for x in zle:
                wiersze.append(f"        {x}")
                problemy.append(f"{h[:100]}: {x}")
        L += ["", f"2. Otwarcie wprost i odświeżenie: {len(linki)} odnośników, {n_spr} sprawdzeń, niezgodnych {n_spr - n_ok}.",
              "   (sprawdzenia: zakładka, każdy parametr w adresie i w polu filtra, podświetlona karta i jej położenie na ekranie — po otwarciu i po odświeżeniu; oraz brak zmiany stanu po odświeżeniu)"]
        L += wiersze
        # 3. zmiana filtra w interfejsie, adres i odświeżenie
        L += ["", "3. Zmiana filtra w interfejsie i odświeżenie (czy adres zapisuje stan i czy stan wraca)"]
        PROBY = [
            ("kohorty", "Podział na serie = kanał", lambda q: zmien(q, "#ko-podz", "kanal"), "ko-podz", "kanal"),
            ("kohorty", "Okno = 30 dni", lambda q: zmien(q, "#ko-okno", "30"), "ko-okno", "30"),
            ("kohorty", "Zawężenie: urządzenie = desktop", lambda q: zmien(q, "#ko-f-urzadzenie", "desktop"), "ko-f-urzadzenie", "desktop"),
            ("kohorty", "Mapa kohort: tygodniowe", lambda q: zmien(q, "#ko-macierz-filtry button:has-text('tygodniowe')"), None, None),
            ("lejek", "Podział = urządzenie, Pokaż dla = telefon", lambda q: (zmien(q, "#f-podz", "urzadzenie"), zmien(q, "#f-lw", "mobile")), "f-lw", "mobile"),
            ("lejek", "Kto = wszyscy", lambda q: zmien(q, "#f-pac", "wszyscy"), "f-pac", "wszyscy"),
            ("po-zakupie", "Specjalizacja (wykres) = pediatra", lambda q: zmien(q, "#pz-spec", "pediatra"), "pz-spec", "pediatra"),
            ("po-zakupie", "Poranny ruch: pacjenci spoza nowych kampanii", lambda q: zmien(q, "#pz-ruch-grupa", "pozostale"), "pz-ruch-grupa", "pozostale"),
            ("wynik", "Ekonomia: poziom = kampanie", lambda q: zmien(q, "#ek-poziom", "kampania"), "ek-poziom", "kampania"),
            ("wynik", "Grupowanie = tygodnie", lambda q: zmien(q, "#wy-krok", "tydz"), "wy-krok", "tydz"),
            ("zdarzenia", "Odznaczenie chipu „Lejek”", lambda q: zmien(q, "#zd-filtry label:first-child input"), None, None),
            ("niewiadome", "Filtr pozycji = 1", lambda q: zmien(q, "#nw-filtr-pozycja", "1"), "nw-filtr-pozycja", "1"),
        ]
        for z, opis, akcja, pole, wart in PROBY:
            t = ctx.new_page()
            t.goto(adres + "#" + z)
            czekaj(t, z)
            h0 = t.evaluate("decodeURIComponent(location.hash)")
            try:
                akcja(t)
            except Exception as e:  # noqa: BLE001
                L.append(f"   {z}: {opis}: nie udało się zmienić filtra ({e.__class__.__name__}: {str(e)[:120]})")
                t.close()
                continue
            s1 = t.evaluate(STAN)
            t.reload()
            czekaj(t, z)
            s2 = t.evaluate(STAN)
            t.close()
            zmiana_adresu = s1["hash"] != h0
            zostaje = (s2["kontrolki"].get(pole) == wart) if pole else (s1["hash"] == s2["hash"] and zmiana_adresu)
            L.append(f"   {z}: {opis}: adres po zmianie {'ZMIENIA SIĘ' if zmiana_adresu else 'bez zmian'}; po odświeżeniu filtr "
                     f"{'ZOSTAJE' if zostaje else 'wraca do domyślnego'}" + (f" (pole {pole}: {s2['kontrolki'].get(pole)})" if pole else ""))
            if z in POLA and pole and not zostaje:
                problemy.append(f"{z}: {opis}: filtr zapisywany w adresie nie wraca po odświeżeniu")
        # 4. wstecz i dalej
        L += ["", "4. Przyciski wstecz i dalej"]
        t = ctx.new_page()
        t.goto(adres + "#wzrost")
        czekaj(t, "wzrost")
        kroki = []
        t.click("nav.zakladki a[data-widok='kohorty']")
        czekaj(t, "kohorty")
        kroki.append(("klik zakładki „Kohorty”", t.evaluate(STAN)))
        t.click("nav.zakladki a[data-widok='lejek']")
        czekaj(t, "lejek")
        kroki.append(("klik zakładki „Lejek”", t.evaluate(STAN)))
        zmien(t, "#f-pac", "wszyscy")
        kroki.append(("zmiana filtra „Kto = wszyscy”", t.evaluate(STAN)))
        t.go_back()
        czekaj(t, nazwa_z(t.evaluate("location.hash") or "#wzrost"))
        kroki.append(("wstecz", t.evaluate(STAN)))
        t.go_forward()
        czekaj(t, nazwa_z(t.evaluate("location.hash") or "#wzrost"))
        kroki.append(("dalej", t.evaluate(STAN)))
        # odnośnik z filtrami z karty „Czy to wzrost” i powrót
        t.goto(adres + "#wzrost")
        czekaj(t, "wzrost")
        pierwszy = t.evaluate("() => { const a = [...document.querySelectorAll('#v-wzrost a[href^=\"#kohorty?\"]')][0]; a.scrollIntoView({block: 'center'}); return [a.getAttribute('href'), Math.round(scrollY)]; }")
        t.wait_for_timeout(300)
        y_przed = t.evaluate("Math.round(scrollY)")
        t.click(f"#v-wzrost a[href='{pierwszy[0]}']")
        czekaj(t, "kohorty")
        kroki.append((f"klik odnośnika {pierwszy[0][:60]}… z karty (przewinięcie strony {y_przed} px)", t.evaluate(STAN)))
        t.go_back()
        czekaj(t, "wzrost")
        st = t.evaluate(STAN)
        kroki.append((f"wstecz (przewinięcie strony {st['scrollY']} px; przed kliknięciem {y_przed} px)", st))
        t.go_forward()
        czekaj(t, "kohorty")
        kroki.append(("dalej", t.evaluate(STAN)))
        t.close()
        for opis, s in kroki:
            L.append(f"   {opis}: zakładka {s['widok']}, adres {s['hash'][:110]}")
        ctx.close()
        b.close()
    serw.shutdown()
    rev = subprocess.run(["git", "-C", KATALOG, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    naglowek = [f"F — ODNOŚNIKI Z PARAMETRAMI, ODŚWIEŻENIE, WSTECZ I DALEJ ({dt.datetime.now():%Y-%m-%d %H:%M}, commit {rev}, pliki strony z dysku)",
                "Edge bez okna, 127.0.0.1, 1366 × 900 px. Każdy odnośnik otwarty w nowej karcie wprost z adresu, potem odświeżony.", "",
                f"Problemy: {len(problemy)}; błędy strony w czasie kontroli: {len(bledy)}"]
    naglowek += [f"   {x}" for x in problemy[:40]] + [f"   błąd strony: {x[:200]}" for x in bledy[:10]] + [""]
    tekst = "\n".join(naglowek + L) + "\n"
    with open(RAPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write(tekst)
    print("\n".join(naglowek))
    print("\n".join(x for x in L if not x.startswith("   OK ")))


if __name__ == "__main__":
    main()
