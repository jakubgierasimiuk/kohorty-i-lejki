/* Rysowanie kart tekstowych w ogólnym kształcie z kontraktu danych (notatki/e_runda.md, punkt 3), ikony SVG,
   znaczniki stanu i pewności oraz etykiety zmiany rok do roku. Ten plik nie wpisuje żadnych liczb ani wniosków:
   wszystkie teksty przychodzą z danych (dane_strony/*.js), a stąd idą na stronę jako zwykły tekst (bez HTML).
   Udostępnia window.BK; korzystają z niego app.js, widoki.js i widoki_c.js. */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";

  function el(tag, attrs, dzieci) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (attrs[k] === null || attrs[k] === undefined) continue;
      if (k === "text") e.textContent = attrs[k];
      else if (k === "class") e.className = attrs[k];
      else e.setAttribute(k, attrs[k]);
    }
    (dzieci || []).forEach(function (d) { if (d !== null && d !== undefined && d !== false) e.appendChild(typeof d === "string" ? document.createTextNode(d) : d); });
    return e;
  }

  // ------------------------------------------------------------ ikony (linie 2 px na siatce 24 × 24)
  var IKONY = {
    dobrze: [["circle", { cx: 12, cy: 12, r: 9 }], ["path", { d: "M8 12.4l2.7 2.7L16.2 9.4" }]],
    zle: [["circle", { cx: 12, cy: 12, r: 9 }], ["path", { d: "M9.2 9.2l5.6 5.6M14.8 9.2l-5.6 5.6" }]],
    uwaga: [["path", { d: "M12 3.8l9 15.6H3z", "stroke-linejoin": "round" }], ["path", { d: "M12 10v4.2M12 16.9v.1" }]],
    neutralnie: [["circle", { cx: 12, cy: 12, r: 9 }], ["path", { d: "M8 12h8" }]],
    wysoka: [["circle", { cx: 12, cy: 12, r: 9 }], ["path", { d: "M8 12.4l2.7 2.7L16.2 9.4" }]],
    srednia: [["circle", { cx: 12, cy: 12, r: 9 }], ["path", { d: "M12 3v18a9 9 0 0 0 0-18z", fill: "currentColor", stroke: "none" }]],
    niska: [["circle", { cx: 12, cy: 12, r: 9 }], ["path", { d: "M12 7.6v5.4M12 16.2v.1" }]],
    test: [["path", { d: "M9 3.5h6M10 3.5v5.8L4.9 18.2a1.6 1.6 0 0 0 1.4 2.3h11.4a1.6 1.6 0 0 0 1.4-2.3L14 9.3V3.5", "stroke-linejoin": "round" }],
      ["path", { d: "M7.3 14.5h9.4" }]],
    info: [["circle", { cx: 12, cy: 12, r: 9 }], ["path", { d: "M12 11v5.4M12 7.8v.1" }]],
    wzrost: [["path", { d: "M12 19V5.5M6.5 11L12 5.5 17.5 11" }]],
    spadek: [["path", { d: "M12 5v13.5M6.5 13L12 18.5 17.5 13" }]],
    bez: [["path", { d: "M5 12h13.5M13 6.5l5.5 5.5-5.5 5.5" }]],
    lista: [["path", { d: "M4 6.5h16M4 12h16M4 17.5h16" }]]
  };
  function ikona(nazwa, etykieta) {
    var svg = document.createElementNS(NS, "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("class", "ikona");
    svg.setAttribute("fill", "none");
    svg.setAttribute("stroke", "currentColor");
    svg.setAttribute("stroke-width", "2");
    svg.setAttribute("stroke-linecap", "round");
    if (etykieta) { svg.setAttribute("role", "img"); svg.setAttribute("aria-label", etykieta); }
    else svg.setAttribute("aria-hidden", "true");
    (IKONY[nazwa] || IKONY.neutralnie).forEach(function (cz) {
      var e = document.createElementNS(NS, cz[0]);
      for (var k in cz[1]) e.setAttribute(k, cz[1][k]);
      svg.appendChild(e);
    });
    return svg;
  }

  var STANY = { dobrze: 1, zle: 1, uwaga: 1, neutralnie: 1 };
  function stan(s) { return STANY[s] ? s : "neutralnie"; }

  // znacznik stanu: {tekst, stan} → kolor zawsze z ikoną i słowem
  function znacznik(z, duzy) {
    if (!z || !z.tekst) return null;
    var s = stan(z.stan);
    return el("span", { class: "znacznik st-" + s + (duzy ? " znacznik-duzy" : "") }, [ikona(s), el("span", { text: z.tekst })]);
  }

  // pewność w priorytetach: {poziom: wysoka|srednia|niska|test, tekst, dopisek}
  var POZIOMY = { wysoka: "Wysoka", srednia: "Średnia", niska: "Niska", test: "Test" };
  function pewnosc(p) {
    if (!p) return null;
    var poz = POZIOMY[p.poziom] ? p.poziom : null;
    var z = el("span", { class: "znacznik " + (poz ? "pw-" + poz : "st-neutralnie") }, [ikona(poz || "neutralnie"),
      el("span", { text: p.tekst || (poz ? POZIOMY[poz] : "") })]);
    return z;
  }
  // dotychczasowy kształt pewności to jeden napis, np. „wysoka: awaria widoczna w danych” albo „— (to jest test)”
  function pewnoscZNapisu(t) {
    if (!t) return null;
    if (typeof t === "object") return t;
    var s = String(t).trim(), m = s.match(/^(wysoka|średnia|niska)\b[:,]?\s*(.*)$/i);
    if (m) {
      var poz = m[1].toLowerCase() === "wysoka" ? "wysoka" : m[1].toLowerCase() === "niska" ? "niska" : "srednia";
      return { poziom: poz, tekst: POZIOMY[poz], dopisek: m[2] };
    }
    if (/test/i.test(s)) return { poziom: "test", tekst: "Test", dopisek: s.replace(/^[—–-]\s*/, "").replace(/^\((.*)\)$/, "$1") };
    return { poziom: null, tekst: s };
  }

  // etykieta zmiany rok do roku: strzałka według kierunku, kolor i słowo według stanu (kolor stanu nigdy bez słowa).
  // Słowo jest widoczne; tylko w dużych tabelach podziałów (kohorty, lejek, wykryte zmiany) opcje.slowo = false:
  // wtedy słowo jest w podpowiedzi i dla czytników ekranu, a pod tabelą stoi objaśnienie kolorów (legendaZmian).
  var SLOWO = { dobrze: "lepiej", zle: "gorzej", uwaga: "uwaga", neutralnie: "" };
  function zmiana(tekst, kierunek, s, tytul, opcje) {
    s = stan(s);
    var kier = kierunek === "wzrost" || kierunek === "spadek" ? kierunek : "bez";
    var slowo = SLOWO[s] && tekst !== SLOWO[s] ? SLOWO[s] : "", widoczne = !opcje || opcje.slowo !== false;
    var t = tytul ? tytul + (slowo ? ": " + slowo : "") : (slowo && !widoczne ? slowo : null);
    return el("span", { class: "zm zm-" + s, title: t }, [ikona(kier), el("span", { text: tekst }),
      slowo ? el("span", { class: widoczne ? "zm-slowo" : "sr", text: widoczne ? slowo : " (" + slowo + ")" }) : null]);
  }
  // objaśnienie kolorów etykiet zmiany pod dużymi tabelami podziałów
  function legendaZmian(cel, wobec) {
    if (!cel) return;
    while (cel.firstChild) cel.removeChild(cel.firstChild);
    cel.appendChild(el("span", { text: "Etykiety zmiany " + (wobec || "wobec okresu porównania") + ":" }));
    [["wzrost", "dobrze", "lepiej"], ["spadek", "zle", "gorzej"], ["bez", "neutralnie", "bez oceny"]].forEach(function (x) {
      cel.appendChild(el("span", { class: "zm zm-" + x[1] }, [ikona(x[0]), el("span", { text: x[2] })]));
    });
    cel.appendChild(el("span", { text: "Strzałka pokazuje kierunek, kolor ocenę; słowo także po najechaniu na etykietę." }));
  }
  function kierunekZnaku(d) { return d > 0 ? "wzrost" : d < 0 ? "spadek" : "bez"; }


  // ------------------------------------------------------------ wykresy w kartach (HTML i CSS, bez biblioteki)
  // Liczby do podpisów przychodzą z wywołującego już sformatowane (tak jak w tekstach), tu tylko pozycje na osi.
  function pozycja(v, min, max) { return Math.max(0, Math.min(100, 100 * (v - min) / ((max - min) || 1))); }
  function legendaPunktow(lista) {
    return el("div", { class: "wk-legenda" }, lista.map(function (x) {
      return el("span", { class: "wk-lg" }, [el("span", { class: "pkt " + x.klasa }), el("span", { text: x.nazwa })]);
    }));
  }
  function osWartosci(teksty) {
    return el("div", { class: "wk-wiersz wk-os", "aria-hidden": "true" }, [el("span"),
      el("div", { class: "wk-os-skala" }, teksty.map(function (t) { return el("span", { text: t }); })), el("span")]);
  }
  // Wykres hantlowy. cfg: {nazwy: {a, b}, wiersze: [{etykieta, a, b, tekstA, tekstB, zmiana: {tekst, kierunek, stan, tytul},
  //   tytul, podtytul}], min, max, os: [teksty podziałki], kodowanie: "okresy" (szary → niebieski) | "grupy", opis, przypis}
  function hantle(cfg) {
    var min = cfg.min || 0, max = cfg.max;
    var f = el("figure", { class: "wk hantle" + (cfg.kodowanie === "grupy" ? " hantle-grupy" : ""), role: "group", "aria-label": cfg.opis || null });
    f.appendChild(legendaPunktow([{ klasa: "pkt-a", nazwa: cfg.nazwy.a }, { klasa: "pkt-b", nazwa: cfg.nazwy.b }]));
    cfg.wiersze.forEach(function (w) {
      if (w.podtytul) { f.appendChild(el("div", { class: "wk-podtytul", text: w.etykieta })); return; }
      var xa = pozycja(w.a, min, max), xb = pozycja(w.b, min, max), lo = Math.min(xa, xb), hi = Math.max(xa, xb);
      var opis = w.etykieta + ": " + cfg.nazwy.a + " " + w.tekstA + ", " + cfg.nazwy.b + " " + w.tekstB;
      f.appendChild(el("div", { class: "wk-wiersz", tabindex: "0", title: w.tytul || opis, "aria-label": opis }, [
        el("span", { class: "wk-etykieta", text: w.etykieta }),
        el("div", { class: "wk-tor" }, [el("span", { class: "hantle-odcinek", style: "left:" + lo + "%;width:" + (hi - lo) + "%" }),
          el("span", { class: "pkt pkt-a", style: "left:" + xa + "%" }), el("span", { class: "pkt pkt-b", style: "left:" + xb + "%" })]),
        el("span", { class: "wk-wart" }, [el("span", { class: "wk-ab" }, [el("span", { class: "wk-a", text: w.tekstA }), " → ",
          el("strong", { text: w.tekstB })]), w.zmiana ? zmiana(w.zmiana.tekst, w.zmiana.kierunek, w.zmiana.stan, w.zmiana.tytul) : null])]));
    });
    if (cfg.os) f.appendChild(osWartosci(cfg.os));
    if (cfg.przypis) f.appendChild(el("figcaption", { class: "wk-przypis", text: cfg.przypis }));
    return f;
  }
  // Słupki parami (wartość wcześniejsza szara, późniejsza niebieska, wspólny początek osi).
  // cfg: {nazwy: {a, b}, wiersze: [{etykieta, a, b, tekstA, tekstB, zmiana}], max, opis, przypis}
  function slupkiParami(cfg) {
    var f = el("figure", { class: "wk slupki-parami", role: "group", "aria-label": cfg.opis || null });
    f.appendChild(legendaPunktow([{ klasa: "pkt-a kw", nazwa: cfg.nazwy.a }, { klasa: "pkt-b kw", nazwa: cfg.nazwy.b }]));
    cfg.wiersze.forEach(function (w) {
      var opis = w.etykieta + ": " + cfg.nazwy.a + " " + w.tekstA + ", " + cfg.nazwy.b + " " + w.tekstB;
      f.appendChild(el("div", { class: "wk-wiersz", tabindex: "0", title: w.tytul || opis, "aria-label": opis }, [
        el("span", { class: "wk-etykieta", text: w.etykieta }),
        el("div", { class: "wk-para" }, [
          el("div", { class: "wk-slupek-wiersz" }, [el("span", { class: "wk-slupek sl-a", style: "width:" + pozycja(w.a, 0, cfg.max) + "%" }),
            el("span", { class: "wk-slupek-tekst", text: w.tekstA })]),
          el("div", { class: "wk-slupek-wiersz" }, [el("span", { class: "wk-slupek sl-b", style: "width:" + pozycja(w.b, 0, cfg.max) + "%" }),
            el("span", { class: "wk-slupek-tekst mocny", text: w.tekstB })])]),
        el("span", { class: "wk-wart" }, [w.zmiana ? zmiana(w.zmiana.tekst, w.zmiana.kierunek, w.zmiana.stan, w.zmiana.tytul) : null])]));
    });
    if (cfg.przypis) f.appendChild(el("figcaption", { class: "wk-przypis", text: cfg.przypis }));
    return f;
  }
  // Słupki skumulowane w skali liczebności (długość = liczba, nie 100%).
  // cfg: {czesci: [{nazwa, klasa}], wiersze: [{etykieta, wartosci: [liczby], teksty: [napisy], suma: napis}], max, opis}
  function slupkiSkumulowane(cfg) {
    var f = el("figure", { class: "wk slupki-skum", role: "group", "aria-label": cfg.opis || null });
    f.appendChild(el("div", { class: "wk-legenda" }, cfg.czesci.map(function (c) {
      return el("span", { class: "wk-lg" }, [el("span", { class: "pkt kw " + c.klasa }), el("span", { text: c.nazwa })]);
    })));
    cfg.wiersze.forEach(function (w) {
      var opis = w.etykieta + ": " + cfg.czesci.map(function (c, i) { return c.nazwa + " " + w.teksty[i]; }).join(", ") + ", razem " + w.suma;
      f.appendChild(el("div", { class: "wk-wiersz", tabindex: "0", title: opis, "aria-label": opis }, [
        el("span", { class: "wk-etykieta", text: w.etykieta }),
        el("div", { class: "wk-skum" }, cfg.czesci.map(function (c, i) {
          var v = w.wartosci[i], sz = pozycja(v, 0, cfg.max);
          return v > 0 ? el("span", { class: "wk-segment " + c.klasa, style: "width:" + sz + "%" }, [sz > 14 ? el("span", { text: w.teksty[i] }) : null]) : null;
        })),
        el("span", { class: "wk-wart" }, [el("strong", { text: w.suma })])]));
    });
    if (cfg.przypis) f.appendChild(el("figcaption", { class: "wk-przypis", text: cfg.przypis }));
    return f;
  }
  // Punkty względem zera (np. wynik na pacjenta po koszcie pozyskania według dwóch reguł przypisania).
  // cfg: {legenda: [{klasa, nazwa}], wiersze: [{etykieta, punkty: [{v, klasa}], teksty: [napisy], ujemne: [bool], uwaga: element}],
  //   min, max, os: [teksty], opis, przypis}
  function punktyZero(cfg) {
    var f = el("figure", { class: "wk punkty-zero", role: "group", "aria-label": cfg.opis || null });
    f.appendChild(legendaPunktow(cfg.legenda));
    var x0 = pozycja(0, cfg.min, cfg.max);
    cfg.wiersze.forEach(function (w) {
      var opis = w.etykieta + ": " + cfg.legenda.map(function (l, i) { return l.nazwa + " " + w.teksty[i]; }).join(", ");
      f.appendChild(el("div", { class: "wk-wiersz", tabindex: "0", title: opis, "aria-label": opis }, [
        el("span", { class: "wk-etykieta", text: w.etykieta }),
        el("div", { class: "wk-tor" }, [el("span", { class: "wk-zero", style: "left:" + x0 + "%" })].concat(w.punkty.map(function (p) {
          return p.v === null || p.v === undefined ? null : el("span", { class: "pkt " + p.klasa, style: "left:" + pozycja(p.v, cfg.min, cfg.max) + "%" });
        }))),
        el("span", { class: "wk-wart" }, w.teksty.map(function (t, i) {
          return el("span", { class: "wk-v" + (w.ujemne && w.ujemne[i] ? " ujemne" : "") }, [el("span", { class: "pkt mini " + cfg.legenda[i].klasa }), t]);
        }).concat([w.uwaga || null]))]));
    });
    if (cfg.os) f.appendChild(osWartosci(cfg.os));
    if (cfg.przypis) f.appendChild(el("figcaption", { class: "wk-przypis", text: cfg.przypis }));
    return f;
  }
  // wstawia wykres do karty pod wnioskiem; tabelę z liczbami, którą wykres zastępuje, chowa do zwijanej sekcji
  function wstawWykres(art, wykres, schowajTabele, napis) {
    if (!art || !wykres) return;
    var w = art.querySelector(".wniosek"), tr = art.querySelector(".tresc");
    if (w) w.parentNode.insertBefore(wykres, w.nextSibling);
    else if (tr) tr.parentNode.insertBefore(wykres, tr);
    else art.appendChild(wykres);
    if (!schowajTabele) return;
    var t = art.querySelector(".tresc .tabela-ramka") || art.querySelector(".tabela-ramka");
    if (!t || t.closest("details")) return;
    var d = el("details", { class: "szczegoly tabela-zwinieta" }, [el("summary", { text: napis || "Tabela z liczbami" })]);
    t.parentNode.insertBefore(d, t);
    d.appendChild(t);
  }

  // ------------------------------------------------------------ bloki treści
  function tekstKomorki(k) {
    if (k === null || k === undefined) return "—";
    if (typeof k !== "object") return String(k);
    return k.tekst;
  }
  function komorkaDzieci(k) {
    if (k === null || k === undefined || typeof k !== "object") return [k === null || k === undefined ? "—" : String(k)];
    var out = [];
    if (k.zmiana) out.push(zmiana(k.tekst, k.zmiana, k.stan));
    else if (k.stan && k.stan !== "neutralnie") out.push(znacznik({ tekst: k.tekst, stan: k.stan }));
    else out.push(String(k.tekst));
    if (k.pod) out.push(el("span", { class: "pod", text: k.pod }));
    return out;
  }
  function komorka(k, tag) { return el(tag || "td", null, komorkaDzieci(k)); }
  function tabela(b) {
    var t = el("table", { class: "tabela" });
    if (b.tytul) t.appendChild(el("caption", { text: b.tytul }));
    if (b.kolumny && b.kolumny.length) {
      var hr = el("tr");
      b.kolumny.forEach(function (k) { hr.appendChild(el("th", { text: k })); });
      t.appendChild(el("thead", null, [hr]));
    }
    var tb = el("tbody");
    (b.wiersze || []).forEach(function (w) {
      var tr = el("tr", w.podsuma ? { class: "podsuma" } : null);
      if (w.opis !== undefined) tr.appendChild(el("td", { text: w.opis }));
      (w.komorki || []).forEach(function (k) { tr.appendChild(komorka(k)); });
      tb.appendChild(tr);
    });
    t.appendChild(tb);
    return el("div", { class: "tabela-ramka" }, [t]);
  }
  function kafelek(b) {
    return el("div", { class: "kafelek" }, [
      el("div", { class: "kafelek-gora" }, [el("span", { class: "kafelek-liczba", text: b.liczba }),
        b.zmiana || (b.stan && b.stan !== "neutralnie") ? zmiana(SLOWO[stan(b.stan)] || (b.zmiana === "wzrost" ? "wzrost" : b.zmiana === "spadek" ? "spadek" : "bez zmian"), b.zmiana || "bez", b.stan) : null]),
      b.podpis ? el("span", { class: "kafelek-podpis", text: b.podpis }) : null,
      b.dopisek ? el("span", { class: "kafelek-dopisek", text: b.dopisek }) : null]);
  }
  function kafelki(lista) { return el("div", { class: "kafelki" }, lista.map(kafelek)); }

  function blok(b) {
    if (!b) return null;
    if (typeof b === "string") return el("p", { text: b });
    switch (b.typ) {
      case "akapit": return el("p", { text: b.tekst });
      case "punkty": return el("ul", { class: "punkty" }, (b.punkty || []).map(function (p) { return el("li", { text: p }); }));
      case "numerowane": return el("ol", { class: "punkty" }, (b.punkty || []).map(function (p) { return el("li", { text: p }); }));
      case "podtytul": return el("h4", { class: "podtytul-karty", text: b.tekst });
      case "liczba": return kafelki([b]);
      case "tabela": return tabela(b);
      default: return b.tekst ? el("p", { text: b.tekst }) : null;
    }
  }
  // lista bloków; kolejne bloki „liczba” stają w jednym rzędzie kafelków
  function bloki(lista, cel) {
    cel = cel || document.createDocumentFragment();
    var rzad = null;
    (lista || []).forEach(function (b) {
      if (b && b.typ === "liczba") {
        if (!rzad) { rzad = []; }
        rzad.push(b);
        return;
      }
      if (rzad) { cel.appendChild(kafelki(rzad)); rzad = null; }
      var e = blok(b);
      if (e) cel.appendChild(e);
    });
    if (rzad) cel.appendChild(kafelki(rzad));
    return cel;
  }

  function linki(lista, etykieta) {
    if (!lista || !lista.length) return null;
    var ul = el("ul", { class: "linki" }, [el("li", { class: "linki-etykieta", text: etykieta || "Zobacz w danych:" })]);
    lista.forEach(function (l) { ul.appendChild(el("li", null, [el("a", { href: l.href, text: l.tekst })])); });
    return ul;
  }
  function szczegoly(lista, zrodlo, tytul) {
    if ((!lista || !lista.length) && !zrodlo) return null;
    var d = el("details", { class: "szczegoly" }, [el("summary", { text: tytul || "Szczegóły" })]);
    var w = el("div", { class: "szczegoly-tresc" });
    bloki(lista, w);
    if (zrodlo) w.appendChild(el("p", { class: "zrodlo", text: "Skąd liczby: " + zrodlo }));
    d.appendChild(w);
    return d;
  }
  function zastrzezenie(t) {
    if (!t) return null;
    // etykieta w osobnym wierszu, bez dwukropka (tekst zastrzeżenia często sam ma dwukropek)
    return el("p", { class: "zastrzezenie" }, [ikona("info"), el("span", null, [el("strong", { class: "zastrzezenie-etykieta", text: "Zastrzeżenie" }),
      el("span", { class: "zastrzezenie-tekst", text: t })])]);
  }

  // części karty: nagłówek (tytuł i znacznik), góra (wniosek, treść, wstawka, zastrzeżenie, odnośniki), dół (szczegóły)
  function czesci(k, wstawki) {
    var gora = document.createDocumentFragment();
    if (k.wniosek) gora.appendChild(el("p", { class: "wniosek", text: k.wniosek }));
    if (k.tresc && k.tresc.length) gora.appendChild(bloki(k.tresc, el("div", { class: "tresc" })));
    if (k.wstaw && wstawki && wstawki[k.wstaw]) { var w = wstawki[k.wstaw](); if (w) gora.appendChild(w); }
    var z = zastrzezenie(k.zastrzezenie);
    if (z) gora.appendChild(z);
    var l = linki(k.linki);
    if (l) gora.appendChild(l);
    return { gora: gora, dol: szczegoly(k.szczegoly, k.zrodlo) };
  }
  // nagłówek: tytuł-wniosek ze znacznikiem; gdy karta ma krótką etykietę (np. „Więcej pacjentów”), etykieta i znacznik
  // stoją w wierszu nad tytułem
  function naglowek(k, tag) {
    if (k.etykieta) return el("div", { class: "karta-tytul karta-tytul-etykieta" }, [
      el("div", { class: "karta-etykieta" }, [el("span", { text: k.etykieta }), znacznik(k.znacznik)]),
      el(tag || "h3", { text: k.tytul })]);
    return el("div", { class: "karta-tytul" }, [el(tag || "h3", { text: k.tytul }), znacznik(k.znacznik)]);
  }
  // cała karta jako nowy element
  function karta(k, opcje) {
    opcje = opcje || {};
    var a = el("article", { class: "karta" + (opcje.klasa ? " " + opcje.klasa : ""), id: k.id ? (opcje.prefiks || "k-") + k.id : null });
    if (k.tytul) a.appendChild(naglowek(k));
    var c = czesci(k, opcje.wstawki);
    a.appendChild(c.gora);
    if (c.dol) a.appendChild(c.dol);
    return a;
  }
  // karta wpisana w istniejącą kartę strony (z filtrami, wykresem albo tabelą): tytuł zastępuje dotychczasowy nagłówek,
  // wniosek i treść idą w miejsce dotychczasowych zdań, a „Szczegóły” na koniec karty
  function kartaW(art, miejsce, k, opcje) {
    opcje = opcje || {};
    if (!art || !k) return false;
    if (k.tytul) {
      var h = art.querySelector(".karta-tytul") || art.querySelector("h3");
      var n = naglowek(k);
      if (h) h.parentNode.replaceChild(n, h); else art.insertBefore(n, art.firstChild);
    }
    Array.prototype.forEach.call(art.querySelectorAll(":scope > .karta-dol"), function (x) { x.parentNode.removeChild(x); });
    var c = czesci(k, opcje.wstawki);
    while (miejsce.firstChild) miejsce.removeChild(miejsce.firstChild);
    miejsce.appendChild(c.gora);
    if (c.dol) { c.dol.classList.add("karta-dol"); art.appendChild(c.dol); }
    return true;
  }
  function czyKarta(k) { return !!(k && typeof k === "object" && !Array.isArray(k) && (k.tytul || k.wniosek || k.tresc)); }

  window.BK = { el: el, ikona: ikona, znacznik: znacznik, pewnosc: pewnosc, pewnoscZNapisu: pewnoscZNapisu,
    zmiana: zmiana, legendaZmian: legendaZmian, kierunekZnaku: kierunekZnaku, bloki: bloki, tabela: tabela, kafelek: kafelek, kafelki: kafelki,
    linki: linki, szczegoly: szczegoly, zastrzezenie: zastrzezenie, karta: karta, kartaW: kartaW, czyKarta: czyKarta,
    tekstKomorki: tekstKomorki, komorkaDzieci: komorkaDzieci, POZIOMY: POZIOMY,
    hantle: hantle, slupkiParami: slupkiParami, slupkiSkumulowane: slupkiSkumulowane, punktyZero: punktyZero, wstawWykres: wstawWykres };
})();
