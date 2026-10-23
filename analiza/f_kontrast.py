"""F — czytelność w trybie jasnym i ciemnym oraz układ na telefonie (ostatnia kontrola przed publikacją, część 2).

Otwiera stronę z folderu narzedzie/ w Microsoft Edge bez okna (Playwright, 127.0.0.1) w czterech wariantach: tryb jasny
i ciemny, szerokość 1366 px i 375 px. Na każdej z 9 zakładek rozwija wszystkie zwijane sekcje i mierzy:
  1. kontrast każdego widocznego tekstu z tłem pod nim (WCAG 2: 4,5:1 dla zwykłego tekstu, 3:1 dla dużego);
  2. kontrast elementów wykresów z tłem karty (punkty i odcinki hantli, słupki, kolumny, znaczniki osi zdarzeń, linie zera;
     WCAG 1.4.11: 3:1 dla elementów graficznych potrzebnych do odczytu);
  3. teksty ucięte (element z ukrytym nadmiarem, którego treść jest szersza niż pole) i tabele szersze niż ramka bez
     możliwości przewinięcia;
  4. przewijanie strony w bok.
Wynik: analiza/wyniki/f_kontrast.txt. Wykresy na płótnie (uPlot) nie mają elementów w DOM; sprawdzamy je na zrzutach.

Uruchomienie z głównego folderu:
    python -I analiza/f_kontrast.py
"""
import datetime as dt
import functools
import http.server
import os
import subprocess
import sys
import threading

from playwright.sync_api import sync_playwright

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARZEDZIE = os.path.join(KATALOG, "narzedzie")
RAPORT = os.path.join(KATALOG, "analiza", "wyniki", "f_kontrast.txt")
ZAKLADKI = ["wzrost", "kohorty", "lejek", "po-zakupie", "zdarzenia", "wynik", "jakosc", "priorytety", "niewiadome"]
GOTOWE = {
    "wzrost": "#wz-nowy .slupki-grup .sg-wiersz", "kohorty": "#ko-macierz tbody tr", "lejek": "#lj-udzial .kl-grupa",
    "po-zakupie": "#pz-karta-godziny .kolumny .kl-grupa", "zdarzenia": "#zd-lista .zdarzenie", "wynik": "#ek-wykres .wk-wiersz",
    "jakosc": "#jk-testy-kw .slupek-wiersz", "priorytety": "#pr-1 .hantle .wk-wiersz", "niewiadome": "#nw-tabela tbody tr",
}
WARIANTY = [("jasny", 1366, 900), ("ciemny", 1366, 900), ("jasny", 375, 812), ("ciemny", 375, 812)]

POMIAR = r"""
(z) => {
  const v = document.getElementById('v-' + z);
  v.querySelectorAll('details').forEach(d => { d.open = true; });
  const rgba = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);
    return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const nad = (g, t) => [0, 1, 2].map(i => g[i] * g[3] + t[i] * (1 - g[3])).concat([1]);
  const lum = c => { const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const kontrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  // tło pod elementem: kolejne tła przodków złożone od dołu (body ma tło jawne)
  // (tło przodka liczy się tylko wtedy, gdy środek elementu leży w jego obrysie: podpis nad słupkiem stoi na tle karty, nie słupka)
  const tlo = (e, wzgl) => { const r = (wzgl || e).getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, warstwy = [];
    for (let x = e; x; x = x.parentElement) { const c = rgba(getComputedStyle(x).backgroundColor), q = x.getBoundingClientRect();
      const wObrysie = x === document.documentElement || x === document.body || (cx >= q.left && cx <= q.right && cy >= q.top && cy <= q.bottom);
      if (c && c[3] > 0 && wObrysie) { warstwy.push(c); if (c[3] >= 1) break; } }
    let t = [255, 255, 255, 1]; for (let i = warstwy.length - 1; i >= 0; i--) t = nad(warstwy[i], t); return t; };
  const przezr = e => { let o = 1; for (let x = e; x; x = x.parentElement) o *= +getComputedStyle(x).opacity; return o; };
  const widoczny = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && !e.closest('[hidden]'); };
  const sciezka = e => { const p = []; for (let x = e; x && x !== v && p.length < 4; x = x.parentElement)
      p.unshift(x.tagName.toLowerCase() + (x.id ? '#' + x.id : '') + (typeof x.className === 'string' && x.className ? '.' + x.className.split(' ').filter(Boolean).slice(0, 2).join('.') : ''));
    return p.join(' > '); };
  const teksty = [], grafika = [], uciete = [];
  let nT = 0, nG = 0;
  const wszystkie = [...v.querySelectorAll('*')];
  for (const e of wszystkie) {
    if (!widoczny(e)) continue;
    const s = getComputedStyle(e);
    const wlasny = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    const svgTekst = e instanceof SVGElement && (e.tagName === 'text' || e.tagName === 'tspan');
    if (wlasny && !(e instanceof SVGElement) || svgTekst) {
      let c = rgba(svgTekst ? s.fill : s.color); if (!c) continue;
      const t = svgTekst ? tlo(e.closest('svg').parentElement, e) : tlo(e);
      c = [c[0], c[1], c[2], c[3] * przezr(e)];
      const k = kontrast(nad(c, t), t), px = parseFloat(s.fontSize), gr = +s.fontWeight >= 700;
      const prog = px >= 24 || (gr && px >= 18.66) ? 3 : 4.5;
      nT++;
      if (k < prog) teksty.push({ k: +k.toFixed(2), prog, px, tekst: (e.textContent || '').trim().slice(0, 50), gdzie: sciezka(e),
        kolor: s.color || s.fill, tlo: 'rgb(' + t.slice(0, 3).map(Math.round).join(',') + ')' });
    }
    // elementy wykresów: punkty, odcinki, słupki, kolumny, linie zera, znaczniki osi
    if (e.matches('.pkt, .hantle-odcinek, .wk-slupek, .wk-segment, .sg-pasek, .kl-kol, .sch-pasek, .sch-kreska, .wk-zero, .sg-zero, .lk-pasek, .lk-kreska, .znacznik, .znacznik-zakres, .slupek')
        || (e instanceof SVGElement && e.matches('line.siatka, rect.tor-tlo'))) {
      if (e.closest('.wk-legenda') || e.classList.contains('mini')) continue;
      const svg = e instanceof SVGElement;
      let c = rgba(svg ? (s.fill !== 'none' && rgba(s.fill) && rgba(s.fill)[3] > 0 ? s.fill : s.stroke) : (rgba(s.backgroundColor) && rgba(s.backgroundColor)[3] > 0 ? s.backgroundColor : s.borderTopColor));
      if (!c) continue;
      const t = svg ? tlo(e.closest('svg').parentElement, e) : tlo(e.parentElement || e, e);
      // znaki puste (pierścień, pusty romb, puste koło na osi): kolor niesie obwódka albo kontur, a nie wypełnienie
      if (kontrast(nad(c, t), t) < 1.5) {
        const cien = !svg && /inset/.test(s.boxShadow) ? s.boxShadow.split(/,(?![^(]*\))/).find(x => /inset/.test(x)) : null;
        const o = svg ? rgba(s.stroke) : cien ? rgba(cien) : (parseFloat(s.borderTopWidth) > 0 ? rgba(s.borderTopColor) : null);
        if (o && o[3] > 0) c = o;
      }
      const rodzaj = e.matches('.hantle-odcinek, .sch-kreska, .wk-zero, .sg-zero, .lk-kreska, line.siatka, rect.tor-tlo') ? 'pomocniczy'
        : (!svg && e.matches('.znacznik')) ? 'tło znacznika stanu' : 'znak danych';
      c = [c[0], c[1], c[2], c[3] * przezr(e)];
      const k = kontrast(nad(c, t), t);
      nG++;
      if (k < 3) grafika.push({ rodzaj, k: +k.toFixed(2), klasa: (svg ? e.getAttribute('class') : e.className) || e.tagName, gdzie: sciezka(e),
        kolor: 'rgb(' + nad(c, t).slice(0, 3).map(Math.round).join(',') + ')', tlo: 'rgb(' + t.slice(0, 3).map(Math.round).join(',') + ')' });
    }
    if ((s.overflow === 'hidden' || s.overflowX === 'hidden' || s.textOverflow === 'ellipsis') && e.scrollWidth > e.clientWidth + 2 && e.clientWidth > 0
        && !e.closest('.tabela-ramka') && !e.matches('.uplot, .uplot *, canvas, .wykres, .wykres *')) {
      uciete.push({ gdzie: sciezka(e), szer: e.clientWidth, tresc: e.scrollWidth, tekst: (e.textContent || '').trim().slice(0, 60) });
    }
  }
  // tabele szersze niż ramka: ramka musi dać się przewinąć w bok
  const tabele = [...v.querySelectorAll('.tabela-ramka')].filter(widoczny).map(r => ({ gdzie: sciezka(r), szer: r.clientWidth, tresc: r.scrollWidth,
    przewijana: ['auto', 'scroll'].includes(getComputedStyle(r).overflowX) })).filter(x => x.tresc > x.szer + 2);
  return { nT, nG, teksty, grafika, uciete, tabele, sw: document.documentElement.scrollWidth, iw: window.innerWidth };
}
"""


class CichyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    sys.stdout.reconfigure(errors="replace")
    serw = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(CichyHandler, directory=NARZEDZIE))
    threading.Thread(target=serw.serve_forever, daemon=True).start()
    adres = f"http://127.0.0.1:{serw.server_address[1]}/"
    wyniki = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", headless=True)
        for tryb, szer, wys in WARIANTY:
            ctx = b.new_context(viewport={"width": szer, "height": wys}, color_scheme="dark" if tryb == "ciemny" else "light",
                                is_mobile=szer < 760, has_touch=szer < 760)
            pg = ctx.new_page()
            pg.goto(adres + "#wzrost")
            for z in ZAKLADKI:
                pg.evaluate(f"location.hash = '{z}'")
                pg.wait_for_selector(GOTOWE[z], timeout=30000, state="attached")
                pg.wait_for_timeout(800)
                wyniki.append((tryb, szer, z, pg.evaluate(POMIAR, z)))
            ctx.close()
        b.close()
    serw.shutdown()
    rev = subprocess.run(["git", "-C", KATALOG, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    L = [f"F — CZYTELNOŚĆ W TRYBIE JASNYM I CIEMNYM, UKŁAD NA TELEFONIE ({dt.datetime.now():%Y-%m-%d %H:%M}, commit {rev}, pliki strony z dysku)",
         "Edge bez okna, 127.0.0.1, wszystkie zwijane sekcje rozwinięte. Progi: tekst 4,5:1 (duży 3:1), elementy wykresów 3:1 (WCAG 2.1).", "",
         "1. Podsumowanie (tryb, szerokość: teksty sprawdzone / poniżej progu; elementy wykresów sprawdzone / poniżej progu; ucięte; tabele bez przewijania; przewijanie w bok)"]
    for tryb, szer, _ in WARIANTY:
        x = [w for t_, s_, _, w in wyniki if (t_, s_) == (tryb, szer)]
        gr = [g for w in x for g in w['grafika']]
        L.append(f"   {tryb:6} {szer:5} px: teksty {sum(w['nT'] for w in x):6} / {sum(len(w['teksty']) for w in x):4}; "
                 f"wykresy {sum(w['nG'] for w in x):5} / {len(gr):4} (znaki danych {sum(g['rodzaj'] == 'znak danych' for g in gr)}, "
                 f"pomocnicze {sum(g['rodzaj'] == 'pomocniczy' for g in gr)}, tło znaczników stanu {sum(g['rodzaj'] == 'tło znacznika stanu' for g in gr)}); "
                 f"ucięte {sum(len(w['uciete']) for w in x)}; "
                 f"tabele bez przewijania {sum(1 for w in x for t in w['tabele'] if not t['przewijana'])}; "
                 f"w bok {sum(1 for w in x if w['sw'] > w['iw'] + 1)}")
    L += ["", "2. Szczegóły według zakładek (najsłabsze przykłady, najwyżej 12 na zakładkę i rodzaj)"]
    for tryb, szer, z, w in wyniki:
        if not (w["teksty"] or w["grafika"] or w["uciete"] or any(not t["przewijana"] for t in w["tabele"]) or w["sw"] > w["iw"] + 1):
            continue
        L.append(f"   == {tryb}, {szer} px, {z}: teksty poniżej progu {len(w['teksty'])} z {w['nT']}, elementy wykresów {len(w['grafika'])} z {w['nG']}")
        for t in sorted(w["teksty"], key=lambda t: t["k"])[:12]:
            L.append(f"      tekst {t['k']:5.2f}:1 (próg {t['prog']}, {t['px']:.0f} px) „{t['tekst']}” kolor {t['kolor']} na {t['tlo']} | {t['gdzie']}")
        for g in sorted(w["grafika"], key=lambda g: (g["rodzaj"] != "znak danych", g["k"]))[:12]:
            L.append(f"      wykres ({g['rodzaj']}) {g['k']:5.2f}:1 {g['klasa']} kolor {g['kolor']} na {g['tlo']} | {g['gdzie']}")
        for u in w["uciete"][:12]:
            L.append(f"      ucięte: pole {u['szer']} px, treść {u['tresc']} px „{u['tekst']}” | {u['gdzie']}")
        for t in w["tabele"]:
            if not t["przewijana"]:
                L.append(f"      tabela szersza niż ramka i bez przewijania: {t['szer']} / {t['tresc']} px | {t['gdzie']}")
        if w["sw"] > w["iw"] + 1:
            L.append(f"      strona przewija się w bok: {w['sw']} / {w['iw']} px")
    tekst = "\n".join(L) + "\n"
    with open(RAPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write(tekst)
    print(tekst[:6000])


if __name__ == "__main__":
    main()
