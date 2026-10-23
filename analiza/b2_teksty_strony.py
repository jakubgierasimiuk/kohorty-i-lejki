"""B2 — pełne teksty wszystkich zakładek narzędzia w jednym pliku markdown, tak jak widzi je czytelnik.

Skrypt otwiera prawdziwą stronę (narzedzie/) w przeglądarce bez okna (Microsoft Edge przez Playwright), na lokalnym
serwerze 127.0.0.1 z losowym portem, i po kolei wchodzi na 9 zakładek z domyślnymi ustawieniami. Z widocznej treści
każdej zakładki składa markdown: nagłówki, zdania, listy, filtry z wybraną opcją, podpisy wykresów (nazwy serii)
i tabele jako tabele markdown. Tabele dłuższe niż 40 wierszy są skrócone do 15 pierwszych i 5 ostatnich wierszy
z dopiskiem, ile ich jest. Rozwijane sekcje są rozwinięte. Liczb nie liczy: bierze to, co narysowała strona.

Przeznaczenie: materiał do rundy konsylium (zlecenie Kuby przez sesję prowadzącą, 2026-10-20) i do przeglądu
tekstów bez otwierania strony.

Uruchomienie z głównego folderu (po analiza/b_eksport.py, około pół minuty):
    python -I analiza/b2_teksty_strony.py
Wynik: analiza/wyniki/b_teksty_strony.md
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
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "b_teksty_strony.md")
SZEROKOSC, WYSOKOSC = 1366, 900

# zakładka → element, który musi mieć treść, zanim zaczniemy czytać (dane wczytują się po wejściu na zakładkę)
GOTOWE = {
    "wzrost": "#wz-nowy .karta, #wz-puenta p", "kohorty": "#ko-tabela tbody tr", "lejek": "#lj-tabela tbody tr",
    "po-zakupie": "#pz-tabela tbody tr", "zdarzenia": "#zd-lista .zdarzenie", "wynik": "#ek-tabela tbody tr",
    "jakosc": "#jk-mostek tbody tr", "priorytety": "#pr-karty article", "niewiadome": "#nw-tabela tbody tr",
}
# tabele, które są w zwijanych sekcjach (wykres nad nimi), są w DOM, ale niewidoczne: czekamy na ich obecność
STAN = {
    "wynik": "attached", "jakosc": "attached",
}

# Czytanie widocznej treści jednej zakładki i zamiana na markdown (w przeglądarce, na narysowanym DOM).
CZYTNIK = r"""
(sel) => {
  const root = document.querySelector(sel);
  root.querySelectorAll('details').forEach(d => { d.open = true; });
  const out = [];
  const T = s => (s || '').replace(/\s+/g, ' ').trim();
  const widoczny = e => { const cs = getComputedStyle(e); return cs.display !== 'none' && cs.visibility !== 'hidden'; };
  const komorka = c => c.innerText.split('\n').map(x => x.trim()).filter(Boolean).join('<br>').replace(/\|/g, '\\|');
  const akapit = t => { if (t) out.push(t, ''); };

  function tabela(t) {
    const cap = t.querySelector('caption');
    if (cap && T(cap.innerText)) akapit('*' + T(cap.innerText) + '*');
    const siatka = [];
    [...t.querySelectorAll('thead tr')].forEach((r, i) => {
      siatka[i] = siatka[i] || [];
      let k = 0;
      [...r.children].forEach(c => {
        while (siatka[i][k] !== undefined) k++;
        const cs = +(c.getAttribute('colspan') || 1), rs = +(c.getAttribute('rowspan') || 1), tx = komorka(c);
        for (let a = 0; a < rs; a++) for (let b = 0; b < cs; b++) {
          siatka[i + a] = siatka[i + a] || [];
          siatka[i + a][k + b] = (a === 0 ? tx : '');
        }
        k += cs;
      });
    });
    let head = [];
    if (siatka.length) {
      const nk = Math.max(...siatka.map(r => r.length));
      const h = [];
      for (let k = 0; k < nk; k++) {
        const czesci = [];
        siatka.forEach(r => { const v = r[k]; if (v && czesci[czesci.length - 1] !== v) czesci.push(v); });
        h.push(czesci.join(' — '));
      }
      head = [h];
    }
    let rows = [...t.querySelectorAll('tbody tr')].map(r => [...r.children].map(komorka));
    if (!head.length && rows.length) { head = [rows[0]]; rows = rows.slice(1); }
    if (!head.length) return;
    const n = Math.max(head[0].length, ...rows.map(r => r.length));
    const wiersz = r => { r = r.slice(); while (r.length < n) r.push(''); return '| ' + r.join(' | ') + ' |'; };
    out.push(wiersz(head[0]), '|' + ' --- |'.repeat(n));
    const razem = rows.length;
    if (razem > 40) rows = rows.slice(0, 15).concat([null], rows.slice(-5));
    rows.forEach(r => out.push(r ? wiersz(r) : wiersz(['… pominięto ' + (razem - 20) + ' wierszy, tabela ma ich ' + razem + ' …'])));
    out.push('');
  }
  function nazwa(el) {
    const l = el.closest('label');
    if (l) {
      const t = T([...l.childNodes].filter(x => x.nodeType === 3 || (x.nodeType === 1 && !['SELECT', 'INPUT'].includes(x.tagName)
        && !x.querySelector('select, input'))).map(x => x.textContent).join(' '));
      if (t) return t;
    }
    return T(el.getAttribute('aria-label') || '');
  }
  function opcje(s) {
    const o = [...s.options].map(x => T(x.text));
    const wyb = s.selectedIndex >= 0 ? T(s.options[s.selectedIndex].text) : '';
    const lista = o.length <= 8 ? o.join(' / ') : o.slice(0, 6).join(' / ') + ' / … (razem ' + o.length + ' opcji)';
    return wyb + ' (do wyboru: ' + lista + ')';
  }
  function filtry(f) {
    const poz = [];
    f.querySelectorAll('select, input, fieldset').forEach(x => {
      if (x.tagName === 'SELECT') poz.push('- ' + nazwa(x) + ': ' + opcje(x) + (x.disabled ? ' — nieaktywne' : ''));
      else if (x.tagName === 'INPUT' && x.type === 'checkbox') poz.push('- ' + (x.checked ? '☑ ' : '☐ ') + nazwa(x));
      else if (x.tagName === 'INPUT' && x.type === 'date' && !x.closest('fieldset')) poz.push('- ' + nazwa(x) + ': ' + x.value);
      else if (x.tagName === 'FIELDSET') {
        const d = [...x.querySelectorAll('input[type=date]')].map(i => i.value);
        const leg = x.querySelector('legend');
        if (d.length) poz.push('- ' + (leg ? T(leg.innerText) : 'Okres') + ': ' + d.join(' – '));
      }
    });
    if (poz.length) { out.push('*Filtry (ustawienia domyślne):*'); poz.forEach(p => out.push(p)); out.push(''); }
  }
  function lista(e) {
    [...e.children].forEach((li, i) => { const t = T(li.innerText); if (t) out.push((e.tagName === 'OL' ? (i + 1) + '. ' : '- ') + t); });
    out.push('');
  }
  function wykres(e) {
    // nazwy serii z legendy strony (.lw-nazwa; od etapu 3 grafiki zamiast domyślnej legendy uPlot)
    const s = [...e.querySelectorAll('.lw-nazwa, .u-legend .u-series:not(:first-child) .u-label')].map(x => T(x.innerText)).filter(Boolean);
    akapit('*[Wykres] serie: ' + (s.length ? s.join('; ') : 'brak') + '*');
  }
  function os(svg) {
    const tory = [...svg.querySelectorAll('.tor-nazwa')].map(x => T(x.textContent));
    const zn = svg.querySelectorAll('.znacznik, .znacznik-zakres').length;
    const puste = [...svg.querySelectorAll('.puste')].map(x => T(x.textContent));
    akapit('*[Oś czasu, rysunek] tory: ' + tory.join(', ') + '; znaczników zdarzeń: ' + zn + (puste.length ? '; ' + puste.join(' ') : '') + '*');
  }
  function przejdz(e) {
    if (e.nodeType === 3) { akapit(T(e.textContent)); return; }
    if (e.nodeType !== 1 || !widoczny(e)) return;
    const tag = e.tagName;
    if (['SCRIPT', 'STYLE', 'CANVAS', 'CAPTION'].includes(tag)) return;
    if (e.classList.contains('uplot')) { wykres(e); return; }
    // rysunek osi zdarzeń; pozostałe SVG to ikony (np. w etykietach zmiany) i nie mają treści
    if (tag === 'svg') { if (e.classList.contains('os-rys')) os(e); return; }
    // wykresy w kartach (hantle, słupki, schodki, kolumny): opis wykresu i opis każdego wiersza albo kolumny
    if (tag === 'FIGURE' && e.classList.contains('wk')) {
      const t = e.querySelector('.kl-tytul');
      akapit('*[Wykres' + (t ? ': ' + T(t.innerText) : '') + '] ' + T(e.getAttribute('aria-label') || '') + '*');
      [...e.querySelectorAll('.wk-grupa-tytul, .wk-podtytul, [tabindex][aria-label]')].forEach(w => {
        if (!w.hasAttribute('tabindex')) { out.push('', '**' + T(w.innerText) + '**'); return; }
        const zm = w.querySelector('.zm');
        out.push('- ' + T(w.getAttribute('aria-label')) + (zm ? ' [' + T(zm.innerText) + ']' : ''));
      });
      out.push('');
      const p = e.querySelector('figcaption');
      if (p) akapit('*' + T(p.innerText) + '*');
      return;
    }
    if (e.classList.contains('priorytet-naglowek')) {
      akapit('### ' + T(e.querySelector('.nr').innerText) + '. ' + T(e.querySelector('h3').innerText)); return;
    }
    if (e.classList.contains('priorytet-meta') || (e.classList.contains('meta') && e.closest('.zdarzenie'))) {
      akapit('*' + [...e.children].map(x => T(x.innerText)).filter(Boolean).join(' · ') + '*'); return;
    }
    // runda E: nagłówek karty ze znacznikiem (i etykietą), werdykt, kafelki, decyzje, pasek priorytetu, kroki lejka
    if (e.classList.contains('karta-tytul')) {
      const et = e.querySelector('.karta-etykieta > span:first-child'), zn = e.querySelector('.znacznik'), h = e.querySelector('h3, h4');
      akapit('### ' + (et ? T(et.innerText) + ': ' : '') + T(h ? h.innerText : '') + (zn ? ' — znacznik „' + T(zn.innerText) + '”' : '')); return;
    }
    if (e.classList.contains('werdykt-gora')) {
      const zn = e.querySelector('.znacznik');
      akapit('**Werdykt' + (zn ? ' (znacznik „' + T(zn.innerText) + '”)' : '') + ':** ' + T(e.querySelector('.werdykt-tekst').innerText));
      const d = e.querySelector('.werdykt-dopisek'); if (d) akapit(T(d.innerText));
      return;
    }
    if (e.classList.contains('kafelki')) {
      [...e.querySelectorAll('.kafelek')].forEach(k => {
        const q = c => { const x = k.querySelector(c); return x ? T(x.innerText) : ''; };
        out.push('- **' + q('.kafelek-liczba') + '**' + (q('.zm') ? ' [' + q('.zm') + ']' : '') + ' ' + q('.kafelek-podpis') + (q('.kafelek-dopisek') ? ' — ' + q('.kafelek-dopisek') : ''));
      });
      out.push(''); return;
    }
    if (tag === 'OL' && e.classList.contains('decyzje')) {
      [...e.children].forEach((li, i) => {
        const t = li.querySelector('.decyzja-tekst'), d = li.querySelector('.dopisek');
        const a = t.querySelector('a');
        out.push((i + 1) + '. ' + T(a ? a.innerText : t.firstChild.textContent) + (d ? ' (' + T(d.innerText) + ')' : ''));
      });
      out.push(''); return;
    }
    if (tag === 'UL' && e.classList.contains('linki')) {
      const li = [...e.children];
      akapit(T(li[0].innerText) + ' ' + li.slice(1).map(x => T(x.innerText)).join('; ') + ' *(odnośniki)*'); return;
    }
    if (e.classList.contains('pasek-priorytetu')) {
      akapit('*' + [...e.children].map(x => { const c = [...x.children].map(y => T(y.innerText)).filter(Boolean);
        return c[0] + ': ' + c.slice(1).join(' — '); }).join(' · ') + '*');
      return;
    }
    if (e.classList.contains('lejek-kroki')) {
      out.push('| Krok | Sesje (B) | Odsetek sesji (B) | Porównanie | Przejście do kroku |', '| --- | --- | --- | --- | --- |');
      let przejscie = '';
      [...e.children].forEach(c => {
        if (c.classList.contains('lk-przejscie')) { przejscie = T(c.innerText); return; }
        if (!c.classList.contains('lk-krok')) { akapit(T(c.innerText)); return; }
        const nazwa = T(c.querySelector('.lk-nazwa').firstChild.textContent), q = x => T(c.querySelector(x).innerText);
        out.push('| ' + [nazwa, q('.lk-n'), q('.lk-b'), q('.lk-a'), przejscie].join(' | ') + ' |');
        przejscie = '';
      });
      out.push(''); return;
    }
    if (e.classList.contains('slupki-poziome')) {
      const ch = [...e.children].map(x => T(x.innerText));
      out.push('| ' + ch[0] + ' | ' + ch[1] + ' |', '| --- | --- |');
      for (let i = 2; i + 1 < ch.length; i += 2) out.push('| ' + ch[i] + ' | ' + ch[i + 1] + ' |');
      out.push('');
      return;
    }
    if (tag === 'A' && !e.closest('p, li, td')) { akapit('→ ' + T(e.innerText) + ' *(odnośnik)*'); return; }
    if (/^H[1-4]$/.test(tag)) { const t = T(e.innerText); if (t) akapit('#'.repeat(+tag[1]) + ' ' + t); return; }
    if (tag === 'P' && e.classList.contains('zastrzezenie') && e.querySelector('.zastrzezenie-tekst')) {
      akapit('**Zastrzeżenie.** ' + T(e.querySelector('.zastrzezenie-tekst').innerText)); return;
    }
    if (tag === 'P') { const t = T(e.innerText); if (t) akapit(e.classList.contains('przypis') ? '*' + t + '*' : t); return; }
    if (tag === 'UL' || tag === 'OL') { lista(e); return; }
    if (tag === 'TABLE') { tabela(e); return; }
    if (tag === 'DL') {
      [...e.children].forEach(x => {
        if (x.tagName === 'DT') out.push('**' + T(x.innerText) + ':**');
        else if (x.tagName === 'DD') {
          if (x.querySelector('ul, ol, p, table')) [...x.childNodes].forEach(przejdz); else akapit(T(x.innerText));
        }
      });
      out.push('');
      return;
    }
    if (tag === 'FORM' || e.classList.contains('filtry') || e.classList.contains('filtry-wykresu')
        || (tag === 'LABEL' && e.querySelector('select'))) { filtry(e); return; }
    if (tag === 'SUMMARY') { akapit('**' + T(e.innerText) + '** *(sekcja rozwijana, tu rozwinięta)*'); return; }
    if (!e.children.length) { akapit(T(e.innerText)); return; }
    [...e.childNodes].forEach(przejdz);
  }
  przejdz(root);
  return out.join('\n').replace(/\n{3,}/g, '\n\n');
}
"""


class CichyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serwer():
    obsluga = functools.partial(CichyHandler, directory=NARZEDZIE)
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), obsluga)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def main():
    sys.stdout.reconfigure(errors="replace")
    global WYNIK
    if "--wyjscie" in sys.argv:   # np. do kontroli w katalogu tymczasowym, bez nadpisywania wyniku w analiza/wyniki/
        WYNIK = sys.argv[sys.argv.index("--wyjscie") + 1]
    try:
        commit = subprocess.run(["git", "-C", KATALOG, "rev-parse", "--short", "HEAD"], capture_output=True,
                                text=True, timeout=10).stdout.strip()
    except Exception:  # noqa: BLE001
        commit = ""
    s = serwer()
    adres = f"http://127.0.0.1:{s.server_address[1]}/"
    bledy = []
    czesci = []
    with sync_playwright() as p:
        przegl = p.chromium.launch(channel="msedge", headless=True)
        strona = przegl.new_page(viewport={"width": SZEROKOSC, "height": WYSOKOSC})
        strona.on("pageerror", lambda e: bledy.append(str(e)))
        strona.on("console", lambda m: bledy.append(m.text) if m.type == "error" else None)
        strona.goto(adres + "#wzrost")
        strona.wait_for_selector(GOTOWE["wzrost"])
        naglowek = strona.evaluate("""() => ({
            tytul: document.querySelector('.naglowek h1').innerText.trim(),
            podtytul: document.querySelector('.podtytul').innerText.trim(),
            uwaga: document.querySelector('.syntetyczne').innerText.trim(),
            zakladki: [...document.querySelectorAll('.zakladki a')].map(a => [a.dataset.widok, a.innerText.trim()])})""")
        for i, (widok, nazwa) in enumerate(naglowek["zakladki"], 1):
            strona.evaluate(f"location.hash = '{widok}'")
            strona.wait_for_selector(GOTOWE[widok], timeout=30000, state=STAN.get(widok, "visible"))
            strona.wait_for_timeout(800)   # wykresy i tabele rysują się chwilę po danych
            md = strona.evaluate(CZYTNIK, f"#v-{widok}")
            czesci.append(f"# Zakładka {i}: {nazwa} (`#{widok}`)\n\n{md.strip()}\n")
        stopka = strona.evaluate("() => document.getElementById('stopka-meta').innerText.trim()")
        przegl.close()
    s.shutdown()

    teraz = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    wstep = [
        "# Teksty strony narzędzia — wszystkie zakładki, tak jak widzi je czytelnik", "",
        f"Wygenerowane {teraz} skryptem `analiza/b2_teksty_strony.py` ze strony w `narzedzie/` (stan repozytorium "
        f"{commit}), otwartej w przeglądarce bez okna (Microsoft Edge), szerokość {SZEROKOSC} px. Każda zakładka "
        f"przy ustawieniach domyślnych, bez klikania. Tabele dłuższe niż 40 wierszy są skrócone do 15 pierwszych "
        f"i 5 ostatnich wierszy. Rozwijane sekcje są rozwinięte. Wykresy opisane nazwami serii. W komórkach tabel "
        f"`<br>` oddziela linie, które strona pokazuje jedna pod drugą (zwykle: wartość w okresie B, pod spodem "
        f"okres A i zmiana). Odnośniki do innych zakładek są oznaczone strzałką albo wypisane po „Zobacz w danych”.", "",
        f"**Nagłówek strony:** {naglowek['tytul']} — {naglowek['podtytul']}", "",
        f"**Uwaga na każdej stronie:** {naglowek['uwaga']}", "",
        "**Zakładki:** " + ", ".join(f"{n} (`#{w}`)" for w, n in naglowek["zakladki"]), "",
    ]
    tekst = "\n".join(wstep) + "\n" + "\n".join(czesci) + f"\n---\n\n**Stopka strony:** {stopka}\n"
    with open(WYNIK, "w", encoding="utf-8", newline="\n") as f:
        f.write(tekst)
    print(f"Zapisano {WYNIK}: {len(tekst):,} znaków, {tekst.count(chr(10)):,} linii, zakładek: {len(czesci)}")
    print(f"Błędy w konsoli strony: {len(bledy)}" + ("".join(f"\n   {b}" for b in bledy[:10]) if bledy else ""))


if __name__ == "__main__":
    main()
