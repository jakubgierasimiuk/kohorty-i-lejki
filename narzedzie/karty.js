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

  // ------------------------------------------------------------ istotność zmian w tabelach grup (runda G, uwaga Kuby)
  // „Wyraźna zmiana” = 95% przedział różnicy nie obejmuje zera (przybliżenie normalne, jak w notatkach, założenie 56).
  // Reszta to „bez wyraźnej zmiany”: szara etykieta, bez koloru oceny. Mała grupa: poniżej MALA_GRUPA w którymś okresie.
  // Ten sam rachunek w Pythonie: analiza/g_istotnosc.py (kontrola strony porównuje oba wyniki).
  var Z95 = 1.959963984540054, MALA_GRUPA = 100;
  function przedzial(d, se) { return { d: d, od: d - Z95 * se, do: d + Z95 * se, wyrazna: d - Z95 * se > 0 || d + Z95 * se < 0 }; }
  // dwa odsetki (liczniki i mianowniki); wynik w punktach procentowych
  function roznicaOdsetkow(lA, mA, lB, mB) {
    if (!mA || !mB) return null;
    var pA = lA / mA, pB = lB / mB;
    return przedzial(100 * (pB - pA), 100 * Math.sqrt(pA * (1 - pA) / mA + pB * (1 - pB) / mB));
  }
  // dwie średnie z sum i sum kwadratów wartości na pacjenta (marża na pacjenta); wynik w jednostce wartości
  function roznicaSrednich(sA, kA, nA, sB, kB, nB) {
    if (nA < 2 || nB < 2) return null;
    var mA = sA / nA, mB = sB / nB;
    var vA = Math.max(0, (kA - nA * mA * mA) / (nA - 1)), vB = Math.max(0, (kB - nB * mB * mB) / (nB - 1));
    return przedzial(mB - mA, Math.sqrt(vA / nA + vB / nB));
  }
  // liczby zdarzeń w okresach różnej długości (np. nowi pacjenci dziennie): różnica tempa na dzień
  function roznicaTempa(nA, dA, nB, dB) {
    if (!dA || !dB) return null;
    return przedzial(nB / dB - nA / dA, Math.sqrt(nA / (dA * dA) + nB / (dB * dB)));
  }

  // etykieta zmiany w tabeli grup: kolor tylko przy wyraźnej zmianie (z.stan: dobrze | zle | wyrazna, ta ostatnia bez oceny
  // kierunku, np. udział albo liczba pacjentów); bez wyraźnej zmiany szara, z dopiskiem (krotko: bez dopisku, w podpowiedzi)
  function etykietaIstotnosci(z, krotko) {
    var s = z.wyrazna ? (z.stan === "wyrazna" ? "neutralnie" : z.stan) : "neutralnie";
    var e = zmiana(z.tekst, z.kierunek, s, null, { slowo: false });
    if (z.wyrazna && z.stan === "wyrazna") e.classList.add("zm-wyrazna");
    if (!z.wyrazna) e.classList.add("zm-szara");
    return el("span", { class: "tg-etykieta" }, [e, !z.wyrazna && !krotko ? el("span", { class: "tg-bez", text: "bez wyraźnej zmiany" }) : null]);
  }
  // objaśnienie pod tabelą grup; o.ocena: czy kolory oceniają kierunek (lepiej / gorzej), o.jednostka: „pacjentów” / „sesji”
  function legendaIstotnosci(cel, o) {
    if (!cel) return;
    o = o || {};
    while (cel.firstChild) cel.removeChild(cel.firstChild);
    cel.appendChild(el("span", { text: "Kolor tylko przy zmianie większej niż przypadek (95% przedział zmiany nie obejmuje zera):" }));
    (o.ocena ? [["wzrost", "dobrze", "lepiej"], ["spadek", "zle", "gorzej"]] : [["wzrost", "wyrazna", "wyraźna zmiana"]]).forEach(function (x) {
      var z = el("span", { class: "zm zm-" + (x[1] === "wyrazna" ? "neutralnie zm-wyrazna" : x[1]) }, [ikona(x[0]), el("span", { text: x[2] })]);
      cel.appendChild(z);
    });
    cel.appendChild(el("span", { class: "zm zm-neutralnie zm-szara" }, [ikona("bez"), el("span", { text: "bez wyraźnej zmiany" })]));
    if (!o.bezMalych) {
      cel.appendChild(el("span", { class: "tg-mala", text: "mała grupa" }));
      cel.appendChild(el("span", { text: "poniżej " + MALA_GRUPA + " " + (o.jednostka || "pacjentów") + " w którymś okresie." }));
    }
    cel.appendChild(el("span", { text: "Przedział zmiany widać po najechaniu na etykietę." }));
  }
  // Tabela grup (kohorty, lejek). Tryb „miara”: jedna miara, kolumny: grupa, liczebność (raz na wiersz), wartość w obu
  // okresach i zmiana. Tryb „wszystkie”: w komórce tylko zmiana dla każdego okna albo kroku, wartości w podpowiedzi.
  // cfg: {podzial, nazwaN, nazwaA, nazwaB, tryb, kolumny (tryb „wszystkie”), wiersze: [{nazwa, podsuma, mala, n, nTytul,
  //   wybor: {zaznaczony, kolor, zmien(czy)}, wA, wB, zm: {tekst, kierunek, stan, wyrazna, tytul}, komorki: [{zm, tytul}]}]}
  function tabelaGrup(t, cfg) {
    while (t.firstChild) t.removeChild(t.firstChild);
    var wsz = cfg.tryb === "wszystkie";
    t.className = "tabela tabela-grup" + (wsz ? " tg-wszystkie" : "");
    var hr = el("tr", null, [el("th", { scope: "col", text: cfg.podzial }), el("th", { scope: "col", class: "tg-n", text: cfg.nazwaN })]);
    (wsz ? cfg.kolumny : [cfg.nazwaA, cfg.nazwaB, "Zmiana"]).forEach(function (k, i) {
      hr.appendChild(el("th", { scope: "col", class: wsz || i === 2 ? "tg-zm" : "tg-w", text: k }));
    });
    t.appendChild(el("thead", null, [hr]));
    var tb = el("tbody");
    cfg.wiersze.forEach(function (w) {
      var nazwa = el("span", { class: "tg-nazwa" }, [el("span", { text: w.nazwa }),
        w.mala ? el("span", { class: "tg-mala", title: "Mała grupa: poniżej " + MALA_GRUPA + " " + (cfg.jednostka || "pacjentów") + " w którymś okresie", text: "mała grupa" }) : null,
        el("span", { class: "tg-n-tel", text: cfg.nazwaN + ": " + w.n })]);
      var pierwsza = nazwa;
      if (w.wybor) {
        var chk = el("input", { type: "checkbox", "aria-label": "Pokaż na wykresie: " + w.nazwa });
        chk.checked = !!w.wybor.zaznaczony;
        chk.onchange = function () { w.wybor.zmien(this.checked, this); };
        pierwsza = el("label", { class: "wiersz-wybor" }, [chk,
          el("span", { class: "kropka", style: "background:" + (w.wybor.zaznaczony && w.wybor.kolor ? w.wybor.kolor : "transparent") }), nazwa]);
      }
      var tr = el("tr", { class: ((w.podsuma ? "podsuma" : "") + (w.wybor && w.wybor.zaznaczony ? " zaznaczony" : "")).trim() || null },
        [el("td", null, [pierwsza]), el("td", { class: "tg-n", text: w.n, title: w.nTytul })]);
      if (wsz) (w.komorki || []).forEach(function (k) {
        tr.appendChild(el("td", { class: "tg-zm", title: k && k.tytul }, [k && k.zm ? etykietaIstotnosci(k.zm, true) : "—"]));
      });
      else {
        tr.appendChild(el("td", { class: "tg-w", text: w.wA }));
        tr.appendChild(el("td", { class: "tg-w tg-b", text: w.wB }));
        tr.appendChild(el("td", { class: "tg-zm", title: w.zm && w.zm.tytul }, [w.zm ? etykietaIstotnosci(w.zm) : "—"]));
      }
      tb.appendChild(tr);
    });
    t.appendChild(tb);
    return t;
  }


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
  // „Ładna” podziałka osi: krok 1, 2, 2,5 albo 5 razy potęga dziesięciu, najwyżej n kroków; zero zawsze na podziałce.
  // Zwraca {min, max, krok, wartosci: [liczby podziałki]}.
  function podzialka(mn, mx, n) {
    mn = Math.min(0, mn); mx = Math.max(0, mx); n = n || 6;
    if (mx === mn) mx = mn + 1;
    var surowy = (mx - mn) / n, pot = Math.pow(10, Math.floor(Math.log(surowy) / Math.LN10)), krok = pot * 10;
    [1, 2, 2.5, 5, 10].some(function (m) { if (m * pot >= surowy) { krok = m * pot; return true; } return false; });
    var a = Math.floor(mn / krok + 1e-9) * krok, b = Math.ceil(mx / krok - 1e-9) * krok, w = [];
    for (var v = a; v <= b + krok / 1000; v += krok) w.push(Math.round(v * 1e6) / 1e6);
    return { min: a, max: b, krok: krok, wartosci: w };
  }

  // Schodki poziomów (mostek „dashboard → dane oczyszczone”): dla każdej miary słupek poziomu po każdym kroku, wspólna oś
  // od zera. To poziomy, a nie odejmowanie jak w wodospadzie: każdy słupek zaczyna się od zera. Pierwszy krok (dane surowe)
  // szary, kolejne niebieskie; kreska na kolejnych słupkach pokazuje poziom pierwszego kroku.
  // cfg: {legenda: [{klasa, nazwa}], miary: [{nazwa, kroki: [{etykieta, v, tekst, bezZmian, tytul}]}], max, os: [teksty], opis, przypis}
  function schodki(cfg) {
    var f = el("figure", { class: "wk schodki", role: "group", "aria-label": cfg.opis || null });
    f.appendChild(el("div", { class: "wk-legenda" }, (cfg.legenda || []).map(function (x) {
      return el("span", { class: "wk-lg" }, [el("span", { class: x.klasa }), el("span", { text: x.nazwa })]);
    })));
    cfg.miary.forEach(function (m) {
      f.appendChild(el("div", { class: "wk-grupa-tytul", text: m.nazwa }));
      var x0 = m.kroki.length ? pozycja(m.kroki[0].v, 0, cfg.max) : null;
      m.kroki.forEach(function (k, i) {
        var x = pozycja(k.v, 0, cfg.max), opis = m.nazwa + ", " + k.etykieta + ": " + k.tekst + (k.bezZmian ? " (bez zmian)" : "");
        f.appendChild(el("div", { class: "wk-wiersz", tabindex: "0", title: k.tytul || opis, "aria-label": opis }, [
          el("span", { class: "wk-etykieta", text: k.etykieta }),
          el("div", { class: "wk-tor sch-tor" }, [el("span", { class: "sch-pasek " + (i === 0 ? "sl-a" : "sl-b"), style: "width:" + x + "%" }),
            i > 0 && x0 !== null ? el("span", { class: "sch-kreska", style: "left:" + x0 + "%" }) : null]),
          el("span", { class: "wk-wart" }, [el("strong", { text: k.tekst }), k.bezZmian ? el("span", { class: "wk-bez", text: "bez zmian" }) : null])]));
      });
    });
    if (cfg.os) f.appendChild(osWartosci(cfg.os));
    if (cfg.przypis) f.appendChild(el("figcaption", { class: "wk-przypis", text: cfg.przypis }));
    return f;
  }

  // Słupki grupowane: w każdym wierszu po jednym poziomym słupku na serię, od zera (także w lewo, dla wartości ujemnych),
  // z podpisem przy słupku. cfg: {serie: [{nazwa, klasa}], wiersze: [{etykieta, wartosci: [liczby], teksty: [napisy], tytul}],
  //   min, max, os: [teksty podziałki od min do max], opis, przypis}
  function slupkiGrupowane(cfg) {
    var min = Math.min(0, cfg.min || 0), max = cfg.max, x0 = pozycja(0, min, max);
    var f = el("figure", { class: "wk slupki-grup", role: "group", "aria-label": cfg.opis || null });
    f.appendChild(el("div", { class: "wk-legenda" }, cfg.serie.map(function (s) {
      return el("span", { class: "wk-lg" }, [el("span", { class: "pkt kw " + s.klasa }), el("span", { text: s.nazwa })]);
    })));
    cfg.wiersze.forEach(function (w) {
      var opis = w.etykieta + ": " + cfg.serie.map(function (s, i) { return s.nazwa + " " + w.teksty[i]; }).join(", ");
      f.appendChild(el("div", { class: "wk-wiersz sg-wiersz", tabindex: "0", title: w.tytul || opis, "aria-label": opis }, [
        el("span", { class: "wk-etykieta", text: w.etykieta }),
        el("div", { class: "sg-linie" }, cfg.serie.map(function (s, i) {
          var v = w.wartosci[i], ok = v !== null && v !== undefined && isFinite(v), x = ok ? pozycja(v, min, max) : x0;
          return el("div", { class: "sg-linia" }, [
            el("div", { class: "sg-tor" }, [el("span", { class: "sg-zero", style: "left:" + x0 + "%" }),
              ok ? el("span", { class: "sg-pasek " + s.klasa, style: "left:" + Math.min(x, x0) + "%;width:" + Math.abs(x - x0) + "%" }) : null]),
            el("span", { class: "sg-tekst" + (ok && v < 0 ? " ujemne" : "") }, [w.teksty[i]])]);
        }))]));
    });
    if (cfg.os) f.appendChild(el("div", { class: "wk-wiersz wk-os sg-os", "aria-hidden": "true" }, [el("span"),
      el("div", { class: "sg-os-siatka" }, [el("div", { class: "wk-os-skala" }, cfg.os.map(function (t) { return el("span", { text: t }); })), el("span")])]));
    if (cfg.przypis) f.appendChild(el("figcaption", { class: "wk-przypis", text: cfg.przypis }));
    return f;
  }

  // Pionowe kolumny (np. miesiące albo godziny), oś od zera; w grupie jedna albo kilka wąskich kolumn (jedna na serię).
  // cfg: {tytul (napis nad wykresem), serie: [{nazwa, klasa}] (legenda, opcjonalnie), grupy: [{os: [linie podpisu osi] albo null,
  //   wartosci: [liczby], podpisy: [napisy nad kolumnami] (opcjonalnie), tytul (podpowiedź), opis (dla czytników), tlo: bool}],
  //   max, os: [{v, tekst}] (podziałka osi pionowej), tloNazwa (podpis podcieniowanych grup), wys (px), opis, przypis}
  function kolumny(cfg) {
    var max = cfg.max || 1, n = cfg.grupy.length, wys = cfg.wys || 180;
    var f = el("figure", { class: "wk kolumny", role: "group", "aria-label": cfg.opis || null });
    if (cfg.tytul) f.appendChild(el("div", { class: "kl-tytul", text: cfg.tytul }));
    if (cfg.serie && cfg.serie.length) f.appendChild(el("div", { class: "wk-legenda" }, cfg.serie.map(function (s) {
      return el("span", { class: "wk-lg" }, [el("span", { class: "pkt kw " + s.klasa }), el("span", { text: s.nazwa })]);
    }).concat(cfg.tloNazwa && cfg.grupy.some(function (g) { return g.tlo; }) ?
      [el("span", { class: "wk-lg" }, [el("span", { class: "kl-tlo-wzor" }), el("span", { text: cfg.tloNazwa })])] : [])));
    var osY = el("div", { class: "kl-os-y", style: "height:" + wys + "px", "aria-hidden": "true" });
    var obszar = el("div", { class: "kl-obszar", style: "height:" + wys + "px" });
    (cfg.os || []).forEach(function (t) {
      var b = pozycja(t.v, 0, max);
      osY.appendChild(el("span", { style: "bottom:" + b + "%", text: t.tekst }));
      if (t.v > 0) obszar.appendChild(el("span", { class: "kl-siatka", style: "bottom:" + b + "%" }));
    });
    // podpis podcieniowanych grup nad ciągłym odcinkiem (np. „blok poranny”)
    for (var i = 0; i < n; i++) {
      if (!cfg.grupy[i].tlo || (i > 0 && cfg.grupy[i - 1].tlo)) continue;
      var j = i; while (j + 1 < n && cfg.grupy[j + 1].tlo) j++;
      if (cfg.tloNazwa) obszar.appendChild(el("span", { class: "kl-tlo-nazwa", style: "left:" + (100 * i / n) + "%;width:" + (100 * (j - i + 1) / n) + "%",
        text: cfg.tloNazwa, "aria-hidden": "true" }));
    }
    var rzad = el("div", { class: "kl-grupy" });
    cfg.grupy.forEach(function (g) {
      rzad.appendChild(el("div", { class: "kl-grupa" + (g.tlo ? " kl-tlo" : ""), tabindex: "0", title: g.tytul || null, "aria-label": g.opis || g.tytul || null },
        g.wartosci.map(function (v, k) {
          var ok = v !== null && v !== undefined && isFinite(v);
          return el("span", { class: "kl-kol " + ((cfg.serie && cfg.serie[k] && cfg.serie[k].klasa) || "sl-b") + (ok ? "" : " kl-brak"),
            style: "height:" + (ok ? pozycja(v, 0, max) : 0) + "%" }, [g.podpisy && g.podpisy[k] ? el("span", { class: "kl-wart", text: g.podpisy[k] }) : null]);
        })));
    });
    obszar.appendChild(rzad);
    var osX = el("div", { class: "kl-os-x", "aria-hidden": "true" }, cfg.grupy.map(function (g) {
      return el("span", null, g.os ? [el("span", null, g.os.map(function (t, k) { return el("span", { class: k ? "kl-os-2" : null, text: t }); }))] : null);
    }));
    // miejsce nad obszarem na podpisy kolumn albo podpis podcieniowanych grup
    var gora = cfg.grupy.some(function (g) { return g.podpisy; }) || (cfg.tloNazwa && cfg.grupy.some(function (g) { return g.tlo; }));
    f.appendChild(el("div", { class: "kl-ramka" + (gora ? " kl-z-gora" : "") }, [osY, obszar, el("span"), osX]));
    if (cfg.przypis) f.appendChild(el("figcaption", { class: "wk-przypis", text: cfg.przypis }));
    return f;
  }

  // wstawia wykres do karty pod wnioskiem; tabelę z liczbami, którą wykres zastępuje, chowa do zwijanej sekcji
  function wstawWykres(art, wykres, schowajTabele, napis) {
    if (!art || !wykres) return;
    var w = art.querySelector(".znaczy") || art.querySelector(".wniosek"), tr = art.querySelector(".tresc");
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
    // same źródła bez treści: sekcja nazywa się „Skąd liczby” (runda G: „Szczegóły” bez szczegółów zniechęcają do klikania)
    var tylkoZrodlo = (!lista || !lista.length) && zrodlo;
    var d = el("details", { class: "szczegoly" }, [el("summary", { text: tytul || (tylkoZrodlo ? "Skąd liczby" : "Szczegóły") })]);
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
    // runda G: krok pierwszej zakładki mówi pod odpowiedzią, co ona znaczy dla biznesu
    if (k.znaczy) gora.appendChild(el("p", { class: "znaczy" }, [el("strong", { text: "Co to znaczy dla biznesu: " }), k.znaczy]));
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
    zmiana: zmiana, legendaZmian: legendaZmian, kierunekZnaku: kierunekZnaku, bloki: bloki,
    roznicaOdsetkow: roznicaOdsetkow, roznicaSrednich: roznicaSrednich, roznicaTempa: roznicaTempa, MALA_GRUPA: MALA_GRUPA,
    etykietaIstotnosci: etykietaIstotnosci, legendaIstotnosci: legendaIstotnosci, tabelaGrup: tabelaGrup, tabela: tabela, kafelek: kafelek, kafelki: kafelki,
    linki: linki, szczegoly: szczegoly, zastrzezenie: zastrzezenie, karta: karta, kartaW: kartaW, czyKarta: czyKarta,
    tekstKomorki: tekstKomorki, komorkaDzieci: komorkaDzieci, POZIOMY: POZIOMY,
    hantle: hantle, slupkiParami: slupkiParami, slupkiSkumulowane: slupkiSkumulowane, punktyZero: punktyZero, wstawWykres: wstawWykres,
    schodki: schodki, slupkiGrupowane: slupkiGrupowane, kolumny: kolumny, podzialka: podzialka };
})();
