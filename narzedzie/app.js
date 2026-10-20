/* Narzędzie B2C: nawigacja, lejek, oś zdarzeń, jakość danych (pozostałe zakładki: widoki.js i widoki_c.js).
   Wszystkie liczby pochodzą z plików w dane_strony/ (tworzy je analiza/b_eksport.py). Ten plik ich nie wpisuje, tylko liczy
   z nich odsetki i sumy dla wybranych filtrów oraz je formatuje. */
(function () {
  "use strict";

  var P = window.D.P, ZD = window.D.zdarzenia, JK = window.D.jakosc;
  var ET = P.etykiety;
  var DZIEN = 86400000;
  var START = Date.parse(P.meta.start + "T00:00:00Z");
  var NDNI = Math.round((Date.parse(P.meta.koniec + "T00:00:00Z") - START) / DZIEN) + 1;
  var MIES = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"];
  var RZYM = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];

  // ------------------------------------------------------------ formatowanie (jak w b_eksport.py)
  function liczba(x, m) {
    if (x === null || x === undefined || !isFinite(x)) return "—";
    m = m || 0;
    var s = Math.abs(x).toFixed(m), cz = s.split(".");
    var c = cz[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    return (x < 0 && Number(s) !== 0 ? "−" : "") + c + (cz[1] ? "," + cz[1] : "");
  }
  function proc(x, m) { return x === null || !isFinite(x) ? "—" : liczba(x, m === undefined ? 1 : m) + "%"; }
  function znak(x, m) { return (x > 0 ? "+" : "") + liczba(x, m); }
  function dataIdx(i) { return new Date(START + i * DZIEN); }
  function dataPL(i) { var d = dataIdx(i); return d.getUTCDate() + "." + ("0" + (d.getUTCMonth() + 1)).slice(-2) + "." + d.getUTCFullYear(); }
  function isoIdx(i) { return dataIdx(i).toISOString().slice(0, 10); }
  function idxIso(s) { return Math.round((Date.parse(s + "T00:00:00Z") - START) / DZIEN); }
  function ogranicz(i) { return Math.max(0, Math.min(NDNI - 1, i)); }
  function kwartal(iso) { var r = +iso.slice(0, 4), m = +iso.slice(5, 7); return RZYM[Math.floor((m - 1) / 3)] + " kw. " + r; }

  function el(tag, attrs, dzieci) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === "text") e.textContent = attrs[k];
      else if (k === "class") e.className = attrs[k];
      else if (k === "style") e.setAttribute("style", attrs[k]);
      else e.setAttribute(k, attrs[k]);
    }
    (dzieci || []).forEach(function (d) { if (d !== null && d !== undefined) e.appendChild(typeof d === "string" ? document.createTextNode(d) : d); });
    return e;
  }
  function wyczysc(e) { while (e.firstChild) e.removeChild(e.firstChild); return e; }
  function $(id) { return document.getElementById(id); }
  function css(nazwa) { return getComputedStyle(document.documentElement).getPropertyValue(nazwa).trim(); }
  function akapity(cel, zdania) { wyczysc(cel); zdania.forEach(function (z) { cel.appendChild(el("p", { text: z })); }); }

  function etykieta(podz, w) {
    if (w === "__razem") return "Razem";
    if (podz === "calosc") return "Całość";
    var m = ET[podz];
    return (m && m[w]) || w;
  }

  // ------------------------------------------------------------ wspólne: mostek dashboardu
  function mostek(tabela) {
    var M = JK.mostek.kroki, miary = [["nowi", "Nowi pacjenci"], ["zamowienia", "Zamówienia"],
      ["przychod", "Przychód z konsultacji"], ["go", "TelemediGO"]];
    var o1 = P.meta.okresy[0].nazwa, o2 = P.meta.okresy[1].nazwa;
    wyczysc(tabela);
    tabela.appendChild(el("caption", { class: "przypis", style: "text-align:left;caption-side:top;padding-bottom:6px",
      text: "Wzrost: okres " + o2 + " wobec okresu " + o1 + ". Pod wzrostem: wartości w obu okresach." }));
    var tr = el("tr", null, [el("th", { text: "Krok" })]);
    miary.forEach(function (m) { tr.appendChild(el("th", { text: m[1] })); });
    tabela.appendChild(el("thead", null, [tr]));
    var tb = el("tbody");
    M.forEach(function (k, i) {
      var r = el("tr", i === 0 ? { class: "podsuma" } : null, [el("td", { text: k.opis })]);
      miary.forEach(function (m) {
        var v = k.miary[m[0]], poprz = i > 0 ? M[i - 1].miary[m[0]] : null;
        if (poprz && poprz.p1 === v.p1 && poprz.p2 === v.p2) { r.appendChild(el("td", { text: "bez zmian" })); return; }
        var wart = m[0] === "przychod"
          ? liczba(v.p1 / 1e6, 3) + " → " + liczba(v.p2 / 1e6, 3) + " mln zł"
          : liczba(v.p1) + " → " + liczba(v.p2);
        r.appendChild(el("td", null, [el("strong", { text: znak(v.wzrost, 1) + "%" }), el("br"),
          el("span", { class: "przypis", text: wart })]));
      });
      tb.appendChild(r);
    });
    tabela.appendChild(tb);
  }

  // ------------------------------------------------------------ lejek
  var KROKI = [
    { id: "k1", nazwa: "Wybór usługi", krotko: "usługa / sesje", licz: "k1", mian: "s" },
    { id: "k2", nazwa: "Wybór terminu", krotko: "termin / usługa", licz: "k2", mian: "k1" },
    { id: "k3", nazwa: "Logowanie albo konto", krotko: "konto / termin", licz: "k3", mian: "k2" },
    { id: "k4", nazwa: "Wejście na płatność", krotko: "płatność / konto", licz: "k4", mian: "k3" },
    { id: "k5", nazwa: "Płatność przyjęta", krotko: "przyjęta / wejście", licz: "k5", mian: "k4" },
    { id: "k5s", nazwa: "Sesja do płatności", krotko: "płatność / sesje", licz: "k5", mian: "s" }
  ];
  var MIARY_WYKRESU = KROKI.concat([
    { id: "sesje", nazwa: "Sesje dziennie" },
    { id: "udzial", nazwa: "Udział w sesjach" }
  ]);
  var POLA = ["s", "k1", "k2", "k3", "k4", "k5"];
  var O = P.meta.okresy;
  var S = {
    typ: "zwykla", pac: "wszyscy", podz: "przegladarka", krok: "k5s", wygl: 7,
    a: [idxIso(O[0].od), idxIso(O[0].do)], b: [idxIso(O[1].od), idxIso(O[1].do)],
    preset: "rok", wybrane: null, kolory: {}
  };
  var ladowane = {}, cache = {}, wykresLejka = null;

  function wczytajPodzial(podz) {
    if (window.D.lejek && window.D.lejek[podz]) return Promise.resolve(window.D.lejek[podz]);
    if (ladowane[podz]) return ladowane[podz];
    ladowane[podz] = new Promise(function (ok, blad) {
      var s = document.createElement("script");
      s.src = "dane_strony/lejek_" + podz + ".js";
      s.onload = function () { ok(window.D.lejek[podz]); };
      s.onerror = function () { delete ladowane[podz]; blad(new Error("Nie udało się wczytać danych: " + podz)); };
      document.body.appendChild(s);
    });
    return ladowane[podz];
  }

  function pasuje(s) { return s.typ === S.typ && (S.typ !== "zwykla" || S.pac === "wszyscy" || s.pacjent === S.pac); }

  function seria(dane, w) {
    var klucz = S.podz + "|" + S.typ + "|" + S.pac + "|" + w;
    if (cache[klucz]) return cache[klucz];
    var out = {};
    POLA.forEach(function (k) { out[k] = new Float64Array(NDNI); });
    dane.serie.forEach(function (s) {
      if (!pasuje(s)) return;
      if (w !== "__razem" && s.w !== w) return;
      POLA.forEach(function (k) { var a = s[k]; if (a) for (var i = 0; i < NDNI; i++) out[k][i] += a[i]; });
    });
    cache[klucz] = out;
    return out;
  }
  function suma(arr, z) { var t = 0; for (var i = z[0]; i <= z[1]; i++) t += arr[i]; return t; }
  function wartosci(dane) {
    var zb = {};
    dane.serie.forEach(function (s) {
      if (pasuje(s)) zb[s.w] = true;
    });
    return Object.keys(zb);
  }

  function ustawPreset(p) {
    S.preset = p;
    if (p === "rok") { S.a = [idxIso(O[0].od), idxIso(O[0].do)]; S.b = [idxIso(O[1].od), idxIso(O[1].do)]; }
    else if (p === "90") { S.b = [NDNI - 90, NDNI - 1]; S.a = [NDNI - 180, NDNI - 91]; }
    else if (p === "30rr") { S.b = [NDNI - 30, NDNI - 1]; S.a = [NDNI - 395, NDNI - 366]; }
    else if (p.indexOf("zd:") === 0) {
      var z = ZD.lista.filter(function (x) { return x.id === p.slice(3); })[0];
      if (z) { var d = idxIso(z.od); S.a = [ogranicz(d - 60), ogranicz(d - 1)]; S.b = [ogranicz(d), ogranicz(d + 59)]; }
    }
  }

  function zapiszAdres() {
    var q = new URLSearchParams();
    q.set("typ", S.typ); q.set("pac", S.pac); q.set("podz", S.podz); q.set("krok", S.krok); q.set("wygl", S.wygl);
    q.set("a", isoIdx(S.a[0]) + "_" + isoIdx(S.a[1])); q.set("b", isoIdx(S.b[0]) + "_" + isoIdx(S.b[1]));
    if (S.wybrane) q.set("w", S.wybrane.join(","));
    history.replaceState(null, "", "#lejek?" + q.toString());
  }

  function czytajAdres(q) {
    if (!q || !Array.from(q.keys()).length) return;
    // ustawienia, których nie ma w adresie, wracają do domyślnych (a nie zostają z poprzedniego widoku)
    S.typ = "zwykla"; S.pac = "wszyscy"; S.podz = "przegladarka"; S.krok = "k5s"; S.wygl = 7; ustawPreset("rok");
    if (q.get("typ")) S.typ = q.get("typ");
    if (q.get("pac")) S.pac = q.get("pac");
    if (q.get("podz")) S.podz = q.get("podz");
    if (q.get("krok")) S.krok = q.get("krok");
    if (q.get("wygl")) S.wygl = +q.get("wygl");
    ["a", "b"].forEach(function (k) {
      var v = q.get(k);
      if (v && v.indexOf("_") > 0) { var c = v.split("_"); S[k] = [ogranicz(idxIso(c[0])), ogranicz(idxIso(c[1]))]; S.preset = "wlasne"; }
    });
    if (S.preset === "wlasne" && S.a[0] === idxIso(O[0].od) && S.a[1] === idxIso(O[0].do) &&
        S.b[0] === idxIso(O[1].od) && S.b[1] === idxIso(O[1].do)) S.preset = "rok";
    S.wybrane = q.get("w") ? q.get("w").split(",").filter(Boolean) : null;
    S.kolory = {};
  }

  function przydzielKolory() {
    var zajete = {};
    Object.keys(S.kolory).forEach(function (w) {
      if (S.wybrane.indexOf(w) < 0) delete S.kolory[w]; else zajete[S.kolory[w]] = true;
    });
    S.wybrane.forEach(function (w) {
      if (S.kolory[w]) return;
      for (var i = 1; i <= 8; i++) if (!zajete[i]) { S.kolory[w] = i; zajete[i] = true; return; }
    });
  }

  function rysujNaglowekLejka() {
    var N = P.lejek_naglowek;
    akapity($("lj-zdania"), N.zdania);
    var n = wyczysc($("lj-naprawy"));
    N.naprawy.forEach(function (x) {
      n.appendChild(el("div", { class: "naprawa" }, [el("h4", { text: x.tytul }), el("p", { text: x.tekst }),
        el("a", { href: x.link, text: "Pokaż w lejku" })]));
    });
    akapity($("lj-osobne"), N.osobne);
  }

  function przygotujFiltry() {
    var fp = $("f-podz");
    ["calosc", "urzadzenie", "przegladarka", "system_przegladarka", "urzadzenie_przegladarka", "kanal", "kampania",
      "strona_wejscia"].forEach(function (p) { fp.appendChild(el("option", { value: p, text: ET.podzial[p] })); });
    var pr = $("f-preset");
    pr.appendChild(el("option", { value: "rok", text: "Okres 2 wobec okresu 1 (rok do roku)" }));
    pr.appendChild(el("option", { value: "90", text: "Ostatnie 90 dni wobec poprzednich 90" }));
    pr.appendChild(el("option", { value: "30rr", text: "Ostatnie 30 dni wobec tych samych dni rok wcześniej" }));
    ZD.lista.forEach(function (z) {
      pr.appendChild(el("option", { value: "zd:" + z.id, text: "60 dni przed i po: " + z.tytul + " (" + dataPL(idxIso(z.od)) + ")" }));
    });
    pr.appendChild(el("option", { value: "wlasne", text: "Własne daty" }));
    var fk = $("f-krok");
    MIARY_WYKRESU.forEach(function (m) {
      fk.appendChild(el("option", { value: m.id, text: m.nazwa + (m.krotko ? " (" + m.krotko + ")" : "") }));
    });
    ["a-od", "a-do", "b-od", "b-do"].forEach(function (k) {
      var i = $("f-" + k); i.min = P.meta.start; i.max = P.meta.koniec;
    });

    $("f-typ").onchange = function () { S.typ = this.value; S.wybrane = null; S.kolory = {}; odswiezLejek(); };
    $("f-pac").onchange = function () { S.pac = this.value; odswiezLejek(); };
    $("f-podz").onchange = function () { S.podz = this.value; S.wybrane = null; S.kolory = {}; odswiezLejek(); };
    $("f-preset").onchange = function () { if (this.value !== "wlasne") ustawPreset(this.value); else S.preset = "wlasne"; odswiezLejek(); };
    $("f-krok").onchange = function () { S.krok = this.value; odswiezLejek(true); };
    $("f-wygl").onchange = function () { S.wygl = +this.value; odswiezLejek(true); };
    ["a", "b"].forEach(function (k) {
      ["od", "do"].forEach(function (g, j) {
        $("f-" + k + "-" + g).onchange = function () {
          if (!this.value) return;
          S[k][j] = ogranicz(idxIso(this.value));
          if (S[k][0] > S[k][1]) S[k] = [S[k][1], S[k][0]];
          S.preset = "wlasne"; odswiezLejek();
        };
      });
    });
  }

  function ustawKontrolki() {
    $("f-typ").value = S.typ; $("f-pac").value = S.pac; $("f-podz").value = S.podz; $("f-krok").value = S.krok;
    $("f-wygl").value = String(S.wygl); $("f-preset").value = S.preset;
    $("f-a-od").value = isoIdx(S.a[0]); $("f-a-do").value = isoIdx(S.a[1]);
    $("f-b-od").value = isoIdx(S.b[0]); $("f-b-do").value = isoIdx(S.b[1]);
    $("f-pac").disabled = S.typ !== "zwykla";
  }

  function opisOkresow() {
    return "Okres A: " + dataPL(S.a[0]) + "–" + dataPL(S.a[1]) + " (" + (S.a[1] - S.a[0] + 1) + " dni). " +
      "Okres B: " + dataPL(S.b[0]) + "–" + dataPL(S.b[1]) + " (" + (S.b[1] - S.b[0] + 1) + " dni).";
  }

  function komorkaKroku(sr, k) {
    var lA = suma(sr[k.licz], S.a), mA = suma(sr[k.mian], S.a), lB = suma(sr[k.licz], S.b), mB = suma(sr[k.mian], S.b);
    var pA = mA > 0 ? 100 * lA / mA : null, pB = mB > 0 ? 100 * lB / mB : null;
    var td = el("td", { title: k.nazwa + " (" + k.krotko + "). Okres B: " + liczba(lB) + " z " + liczba(mB) +
      ". Okres A: " + liczba(lA) + " z " + liczba(mA) + "." });
    td.appendChild(el("span", { class: "b", text: proc(pB) }));
    td.appendChild(el("span", { class: "n", text: " z " + liczba(mB) }));
    var a = el("span", { class: "a", text: "A: " + proc(pA) + " z " + liczba(mA) + " " });
    if (pA !== null && pB !== null) {
      var d = pB - pA, zero = Math.abs(d) < 0.05;
      a.appendChild(el("span", { class: "delta " + (zero ? "zero" : d > 0 ? "plus" : "minus"),
        text: (zero ? "= " : d > 0 ? "▲" : "▼") + liczba(Math.abs(d), 1) }));
    }
    td.appendChild(a);
    return td;
  }

  function rysujTabeleLejka(dane) {
    var t = wyczysc($("lj-tabela"));
    var razem = seria(dane, "__razem");
    var sA = suma(razem.s, S.a), sB = suma(razem.s, S.b);
    var hr = el("tr", null, [el("th", { text: ET.podzial[S.podz] }), el("th", { text: "Sesje B (A)" }),
      el("th", { text: "Udział w sesjach B (A)" })]);
    KROKI.forEach(function (k) { hr.appendChild(el("th", { class: "th-krok", text: k.nazwa, title: k.krotko })); });
    t.appendChild(el("thead", null, [hr]));
    var tb = el("tbody");
    var lista = wartosci(dane).map(function (w) { var sr = seria(dane, w); return { w: w, sr: sr, sB: suma(sr.s, S.b), sA: suma(sr.s, S.a) }; })
      .filter(function (x) { return x.sA + x.sB > 0; })
      .sort(function (x, y) { return y.sB - x.sB || y.sA - x.sA; });
    if (!S.wybrane) S.wybrane = S.podz === "calosc" ? ["__razem"] : lista.slice(0, 5).map(function (x) { return x.w; });
    if (S.podz === "calosc") S.wybrane = S.wybrane.map(function (w) { return w === "calosc" ? "__razem" : w; });
    S.wybrane = S.wybrane.filter(function (w) { return w === "__razem" || lista.some(function (x) { return x.w === w; }); });
    przydzielKolory();

    function wiersz(w, sr, wA, wB, klasa) {
      var wybrany = S.wybrane.indexOf(w) >= 0;
      var chk = el("input", { type: "checkbox", "aria-label": "Pokaż na wykresie: " + etykieta(S.podz, w) });
      chk.checked = wybrany;
      chk.onchange = function () {
        if (this.checked) {
          if (S.wybrane.length >= 8) { this.checked = false; alert("Na wykresie mieści się najwyżej osiem serii."); return; }
          S.wybrane.push(w);
        } else S.wybrane = S.wybrane.filter(function (x) { return x !== w; });
        odswiezLejek(true, true);
      };
      var kol = wybrany && S.kolory[w] ? css("--series-" + S.kolory[w]) : "transparent";
      var tr = el("tr", { class: (klasa || "") + (wybrany ? " zaznaczony" : ""), style: "--kolor:" + kol });
      tr.appendChild(el("td", null, [el("label", { class: "wiersz-wybor" }, [chk,
        el("span", { class: "kropka", style: "background:" + kol }), el("span", { text: etykieta(S.podz, w) })])]));
      tr.appendChild(el("td", null, [el("span", { class: "b", text: liczba(wB) }), el("span", { class: "a", text: "A: " + liczba(wA) })]));
      tr.appendChild(el("td", null, [el("span", { class: "b", text: proc(sB ? 100 * wB / sB : null) }),
        el("span", { class: "a", text: "A: " + proc(sA ? 100 * wA / sA : null) })]));
      KROKI.forEach(function (k) { tr.appendChild(komorkaKroku(sr, k)); });
      return tr;
    }
    tb.appendChild(wiersz("__razem", razem, sA, sB, "podsuma"));
    if (S.podz !== "calosc") lista.forEach(function (x) { tb.appendChild(wiersz(x.w, x.sr, x.sA, x.sB)); });
    t.appendChild(tb);
    $("lj-okresy-opis").textContent = opisOkresow() + " Typ: " + ET.typ[S.typ] + ". " +
      (S.typ === "zwykla" ? "Kto: " + (S.pac === "wszyscy" ? "wszyscy" : ET.pacjent[S.pac].toLowerCase()) + "." : "Wszyscy w tym typie kupowali wcześniej.");
  }

  function krocz(arr, w) {
    var out = new Float64Array(arr.length), acc = 0;
    for (var i = 0; i < arr.length; i++) { acc += arr[i]; if (i >= w) acc -= arr[i - w]; out[i] = acc; }
    return out;
  }

  function osieWykresu(etykietaY, formatY) {
    var m = css("--muted"), g = css("--grid");
    return [
      { stroke: m, grid: { stroke: g, width: 1 }, ticks: { stroke: g, width: 1, size: 4 }, font: "12px system-ui",
        values: function (u, splits, ai, space, incr) {
          return splits.map(function (ts) {
            var d = new Date(ts * 1000);
            return incr >= 28 * 86400 ? MIES[d.getUTCMonth()] + " " + d.getUTCFullYear() : d.getUTCDate() + " " + MIES[d.getUTCMonth()];
          });
        } },
      { stroke: m, grid: { stroke: g, width: 1 }, ticks: { stroke: g, width: 1, size: 4 }, font: "12px system-ui",
        label: etykietaY, labelFont: "12px system-ui", size: 56,
        values: function (u, splits) { return splits.map(formatY); } }
    ];
  }

  function rysujZdarzeniaNaWykresie(u, zdarzenia) {
    var ctx = u.ctx, top = u.bbox.top, h = u.bbox.height, dpr = window.devicePixelRatio || 1;
    ctx.save();
    ctx.strokeStyle = css("--ink-2"); ctx.fillStyle = css("--ink-2"); ctx.lineWidth = 1 * dpr;
    ctx.font = (11 * dpr) + "px system-ui"; ctx.textAlign = "center";
    zdarzenia.forEach(function (z) {
      var x = u.valToPos((START + idxIso(z.od) * DZIEN) / 1000, "x", true);
      if (x < u.bbox.left || x > u.bbox.left + u.bbox.width) return;
      ctx.beginPath(); ctx.moveTo(Math.round(x) + 0.5, top + 14 * dpr); ctx.lineTo(Math.round(x) + 0.5, top + h); ctx.stroke();
      ctx.fillText(String(z.nr), x, top + 11 * dpr);
    });
    ctx.restore();
  }

  function rysujOkresy(u) {
    var ctx = u.ctx, top = u.bbox.top, h = u.bbox.height;
    [["A", S.a, css("--okres-a")], ["B", S.b, css("--okres-b")]].forEach(function (o) {
      var x0 = u.valToPos((START + o[1][0] * DZIEN) / 1000, "x", true);
      var x1 = u.valToPos((START + (o[1][1] + 1) * DZIEN) / 1000, "x", true);
      x0 = Math.max(x0, u.bbox.left); x1 = Math.min(x1, u.bbox.left + u.bbox.width);
      if (x1 <= x0) return;
      ctx.save(); ctx.fillStyle = o[2]; ctx.fillRect(x0, top, x1 - x0, h); ctx.restore();
    });
  }

  function zdarzeniaNumerowane() {
    return ZD.lista.map(function (z, i) { var k = Object.assign({}, z); k.nr = i + 1; return k; });
  }

  function rysujWykresLejka(dane) {
    var miara = MIARY_WYKRESU.filter(function (m) { return m.id === S.krok; })[0] || KROKI[5];
    var w = S.wygl;
    $("lj-wykres-tytul").textContent = miara.nazwa + (miara.krotko ? " (" + miara.krotko + ")" : "") +
      ", " + (w === 1 ? "dzień po dniu" : "suma z " + w + " dni kończących się danego dnia");
    var x = new Float64Array(NDNI);
    for (var i = 0; i < NDNI; i++) x[i] = (START + i * DZIEN) / 1000;
    var data = [x], series = [{ label: "Dzień", value: function (u, ts) { return ts == null ? "—" : dataPL(Math.round((ts * 1000 - START) / DZIEN)); } }];
    var razem = seria(dane, "__razem"), sRazem = krocz(razem.s, w);
    S.wybrane.forEach(function (wart) {
      var sr = seria(dane, wart), y = new Array(NDNI), mian;
      if (miara.id === "sesje") {
        var l = krocz(sr.s, w);
        for (i = 0; i < NDNI; i++) y[i] = i >= w - 1 ? l[i] / w : null;
        mian = null;
      } else if (miara.id === "udzial") {
        var l2 = krocz(sr.s, w); mian = sRazem;
        for (i = 0; i < NDNI; i++) y[i] = i >= w - 1 && mian[i] > 0 ? 100 * l2[i] / mian[i] : null;
      } else {
        var ln = krocz(sr[miara.licz], w); mian = krocz(sr[miara.mian], w);
        for (i = 0; i < NDNI; i++) y[i] = i >= w - 1 && mian[i] > 0 ? 100 * ln[i] / mian[i] : null;
      }
      data.push(y);
      (function (mian) {
        series.push({
          label: etykieta(S.podz, wart), stroke: css("--series-" + S.kolory[wart]), width: 2, spanGaps: false,
          points: { show: false },
          value: function (u, v, si, di) {
            if (v == null) return "—";
            if (miara.id === "sesje") return liczba(v, 1) + " sesji dziennie";
            return proc(v) + (mian && di != null ? " z " + liczba(mian[di]) + (miara.id === "udzial" ? " sesji razem" : "") : "");
          }
        });
      })(mian);
    });
    var cel = wyczysc($("lj-wykres"));
    var zd = zdarzeniaNumerowane();
    var procentowa = miara.id !== "sesje";
    var opts = {
      width: Math.max(320, cel.clientWidth), height: 340,
      scales: { x: { time: true }, y: { range: function (u, mn, mx) { return [0, procentowa ? Math.min(100, Math.max(5, mx * 1.08)) : Math.max(1, mx * 1.08)]; } } },
      axes: osieWykresu(procentowa ? "%" : "sesje dziennie", function (v) { return liczba(v, 0) + (procentowa ? "%" : ""); }),
      series: series,
      cursor: { drag: { x: true, y: false }, points: { size: 8 } },
      legend: { live: true },
      tzDate: function (ts) { return uPlot.tzDate(new Date(ts * 1000), "Etc/UTC"); },
      hooks: { drawClear: [rysujOkresy], draw: [function (u) { rysujZdarzeniaNaWykresie(u, zd); }] }
    };
    if (wykresLejka) wykresLejka.destroy();
    wykresLejka = new uPlot(opts, data, cel);
    var leg = wyczysc($("lj-zdarzenia-legenda"));
    zd.forEach(function (z) {
      leg.appendChild(el("li", null, [el("a", { href: "#zdarzenia?z=" + z.id, text: dataPL(idxIso(z.od)) + ": " + z.tytul })]));
    });
  }

  function odswiezLejek(tylkoWykres, tabelaTez) {
    ustawKontrolki();
    var cel = $("lj-wykres");
    cel.style.opacity = "0.5";
    wczytajPodzial(S.podz).then(function (dane) {
      if (!tylkoWykres || tabelaTez) rysujTabeleLejka(dane);
      rysujWykresLejka(dane);
      cel.style.opacity = "1";
      zapiszAdres();
    }).catch(function (e) {
      wyczysc(cel).appendChild(el("p", { class: "przypis", text: e.message + ". Odśwież stronę." }));
      cel.style.opacity = "1";
    });
  }

  // ------------------------------------------------------------ zdarzenia
  var obszaryWidoczne = { lejek: true, retencja: true, obsluga: true, jakosc: true };

  function rysujFiltryZdarzen() {
    var f = wyczysc($("zd-filtry"));
    ZD.obszary.forEach(function (o) {
      var chk = el("input", { type: "checkbox" });
      chk.checked = obszaryWidoczne[o.id];
      chk.onchange = function () { obszaryWidoczne[o.id] = this.checked; rysujOs(); rysujListeZdarzen(); };
      var n = ZD.lista.filter(function (z) { return z.obszar === o.id; }).length;
      f.appendChild(el("label", { class: "chip" }, [chk, ET.obszary[o.id] + " (" + n + ")"]));
    });
  }

  function rysujOs() {
    var kont = wyczysc($("zd-os"));
    var szer = Math.max(560, kont.clientWidth || 900), lewy = 130, prawy = 16, gora = 34, tor = 40;
    var obszary = ZD.obszary.filter(function (o) { return obszaryWidoczne[o.id]; });
    var wys = gora + obszary.length * tor + 8;
    var NS = "http://www.w3.org/2000/svg";
    function s(tag, a, txt) { var e = document.createElementNS(NS, tag); for (var k in a) e.setAttribute(k, a[k]); if (txt) e.textContent = txt; return e; }
    var svg = s("svg", { viewBox: "0 0 " + szer + " " + wys, role: "img", "aria-label": "Oś czasu zdarzeń w podziale na obszary" });
    function xp(i) { return lewy + (szer - lewy - prawy) * i / (NDNI - 1); }
    // podziałka: początek każdego kwartału
    for (var i = 0; i < NDNI; i++) {
      var d = dataIdx(i);
      if (d.getUTCDate() === 1 && d.getUTCMonth() % 3 === 0) {
        svg.appendChild(s("line", { x1: xp(i), x2: xp(i), y1: gora - 8, y2: wys - 4, class: "siatka" }));
        svg.appendChild(s("text", { x: xp(i) + 3, y: gora - 14 }, RZYM[d.getUTCMonth()] + " " + d.getUTCFullYear()));
      }
    }
    var zd = zdarzeniaNumerowane();
    obszary.forEach(function (o, j) {
      var y = gora + j * tor;
      svg.appendChild(s("rect", { x: lewy, y: y + 4, width: szer - lewy - prawy, height: tor - 8, rx: 6, class: "tor-tlo" }));
      svg.appendChild(s("text", { x: 0, y: y + tor / 2 + 4, class: "tor-nazwa" }, ET.obszary[o.id]));
      var tu = zd.filter(function (z) { return z.obszar === o.id; });
      if (!tu.length && o.puste) svg.appendChild(s("text", { x: lewy + 10, y: y + tor / 2 + 4, class: "puste" }, o.puste));
      var ostatniX = -99;
      tu.forEach(function (z) {
        var i0 = idxIso(z.od), i1 = z.do ? idxIso(z.do) : null, g;
        var xl = xp(i0) - ostatniX < 14 ? ostatniX + 14 : xp(i0);   // numery bliskich zdarzeń nie nachodzą na siebie
        ostatniX = xl;
        if (i1 !== null && i1 > i0) {
          g = s("rect", { x: xp(i0), y: y + tor / 2 - 6, width: Math.max(6, xp(i1) - xp(i0)), height: 12, rx: 4, class: "znacznik-zakres", tabindex: 0 });
        } else {
          g = s("circle", { cx: xp(i0), cy: y + tor / 2, r: 6, class: "znacznik", tabindex: 0 });
        }
        g.appendChild(s("title", {}, z.nr + ". " + dataPL(i0) + (i1 ? "–" + dataPL(i1) : "") + ": " + z.tytul));
        g.addEventListener("click", function () { pokazZdarzenie(z.id); });
        g.addEventListener("keydown", function (e) { if (e.key === "Enter") pokazZdarzenie(z.id); });
        svg.appendChild(g);
        svg.appendChild(s("text", { x: xl, y: y + tor / 2 - 9, "text-anchor": "middle" }, String(z.nr)));
      });
    });
    kont.appendChild(svg);
  }

  function rysujListeZdarzen() {
    var l = wyczysc($("zd-lista"));
    zdarzeniaNumerowane().forEach(function (z) {
      if (!obszaryWidoczne[z.obszar]) return;
      var dl = el("dl", null, [el("dt", { text: "Co się zmieniło" }), el("dd", { text: z.co })]);
      if (z.ile) { dl.appendChild(el("dt", { text: "O ile" })); dl.appendChild(el("dd", { text: z.ile })); }
      dl.appendChild(el("dt", { text: "Skąd wiemy" })); dl.appendChild(el("dd", { text: z.skad }));
      var link = z.link && z.link.indexOf("#lejek") === 0 ? el("a", { href: z.link, text: "Pokaż w lejku" })
        : z.link ? el("a", { href: z.link, text: "Zobacz w jakości danych" }) : null;
      l.appendChild(el("article", { class: "karta zdarzenie", id: "zd-" + z.id }, [
        el("div", { class: "meta" }, [el("span", { class: "data", text: z.nr + ". " + dataPL(idxIso(z.od)) + (z.do ? "–" + dataPL(idxIso(z.do)) : "") }),
          el("span", { class: "obszar", text: ET.obszary[z.obszar] }), el("span", { text: z.rodzaj })]),
        el("h3", { text: z.tytul }), dl, link ? el("p", null, [link]) : null]));
    });
  }

  function pokazZdarzenie(id) {
    var e = $("zd-" + id);
    if (!e) return;
    Array.prototype.forEach.call(document.querySelectorAll(".zdarzenie.podswietlone"), function (x) { x.classList.remove("podswietlone"); });
    e.classList.add("podswietlone");
    e.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  var KROK_Z_PRZEJSCIA = { usluga: "k1", termin: "k2", logowanie: "k3", sesja_do_platn: "k5s", sesje_dziennie: "sesje" };
  var NAZWA_PRZEJSCIA = { usluga: "Wybór usługi / sesje", termin: "Wybór terminu / usługa", logowanie: "Konto / termin",
    sesja_do_platn: "Sesja do płatności", sesje_dziennie: "Sesje dziennie" };

  function rysujWykryte() {
    var W = ZD.wykryte, ix = {};
    W.kolumny.forEach(function (k, i) { ix[k] = i; });
    var sel = $("zd-wykryte-podz");
    if (!sel.options.length) {
      sel.appendChild(el("option", { value: "", text: "Wszystkie (" + W.wiersze.length + ")" }));
      var pd = {};
      W.wiersze.forEach(function (r) { pd[r[ix.podzial]] = (pd[r[ix.podzial]] || 0) + 1; });
      Object.keys(pd).forEach(function (p) { sel.appendChild(el("option", { value: p, text: (ET.podzial[p] || p) + " (" + pd[p] + ")" })); });
      sel.onchange = rysujWykryte;
    }
    var t = wyczysc($("zd-wykryte"));
    var hr = el("tr");
    ["Data", "Podział", "Wartość", "Miara", "Przed", "Po", "Zmiana", "Dni przed / po", "Zamówienia na 30 dni", ""].forEach(function (h) { hr.appendChild(el("th", { text: h })); });
    t.appendChild(el("thead", null, [hr]));
    var tb = el("tbody");
    W.wiersze.filter(function (r) { return !sel.value || r[ix.podzial] === sel.value; })
      .sort(function (a, b) { return a[ix.data] < b[ix.data] ? -1 : a[ix.data] > b[ix.data] ? 1 : 0; })
      .forEach(function (r) {
        var ruch = r[ix.rodzaj] === "ruch", f = function (v) { return ruch ? liczba(v, 1) : proc(v); };
        var d = idxIso(r[ix.data]);
        var q = new URLSearchParams({ typ: "zwykla", pac: "nie_kupowal", podz: r[ix.podzial], krok: KROK_Z_PRZEJSCIA[r[ix.przejscie]] || "k5s",
          wygl: "7", a: isoIdx(ogranicz(d - r[ix.dni_przed])) + "_" + isoIdx(ogranicz(d - 1)),
          b: isoIdx(ogranicz(d)) + "_" + isoIdx(ogranicz(d + r[ix.dni_po] - 1)), w: r[ix.wartosc] });
        tb.appendChild(el("tr", null, [
          el("td", { text: dataPL(d) }), el("td", { text: ET.podzial[r[ix.podzial]] || r[ix.podzial] }),
          el("td", { text: etykieta(r[ix.podzial], r[ix.wartosc]) }), el("td", { text: NAZWA_PRZEJSCIA[r[ix.przejscie]] || r[ix.przejscie] }),
          el("td", { text: f(r[ix.przed]) }), el("td", { text: f(r[ix.po]) }),
          el("td", { class: "delta " + (r[ix.zmiana] >= 0 ? "plus" : "minus"), text: znak(r[ix.zmiana], 1) + (ruch ? "" : " pkt proc.") }),
          el("td", { text: r[ix.dni_przed] + " / " + r[ix.dni_po] }),
          el("td", { text: r[ix.zamowienia_na_30_dni] === null ? "—" : znak(r[ix.zamowienia_na_30_dni], 1) }),
          el("td", null, [el("a", { href: "#lejek?" + q.toString(), text: "w lejku" })])]));
      });
    t.appendChild(tb);
  }

  // ------------------------------------------------------------ jakość danych
  var wykresDup = null;
  function rysujJakosc() {
    mostek($("jk-mostek"));
    akapity($("jk-dup-zdania"), JK.duplikaty.zdania);
    akapity($("jk-testy-zdania"), JK.testy.zdania);
    var kw = wyczysc($("jk-testy-kw")), mx = Math.max.apply(null, JK.testy.kwartaly.map(function (k) { return k.n; }));
    kw.appendChild(el("span", { class: "przypis", text: "Kwartał" }));
    kw.appendChild(el("span", { class: "przypis", text: "Zamówienia testowe" }));
    JK.testy.kwartaly.forEach(function (k) {
      kw.appendChild(el("span", { text: kwartal(k.kw) }));
      kw.appendChild(el("div", { class: "slupek-wiersz" }, [el("div", { class: "slupek", style: "width:" + (70 * k.n / mx) + "%" }),
        el("span", { text: liczba(k.n) })]));
    });
    $("jk-godzina").textContent = JK.godzina.zdanie;
    var dr = wyczysc($("jk-drobne")); JK.drobne.forEach(function (z) { dr.appendChild(el("li", { text: z })); });
    var cz = wyczysc($("jk-czyste")); JK.czyste.forEach(function (z) { cz.appendChild(el("li", { text: z })); });
    rysujWykresDup();
  }

  function rysujWykresDup() {
    var cel = wyczysc($("jk-dup-wykres"));
    var x = new Float64Array(NDNI);
    for (var i = 0; i < NDNI; i++) x[i] = (START + i * DZIEN) / 1000;
    var od = idxIso(JK.duplikaty.od), dok = idxIso(JK.duplikaty.do);
    var opts = {
      width: Math.max(320, cel.clientWidth), height: 260,
      scales: { x: { time: true, min: x[ogranicz(od - 21)], max: x[ogranicz(dok + 21)] }, y: { range: function (u, mn, mx) { return [0, mx * 1.1]; } } },
      axes: osieWykresu("zamówienia dziennie", function (v) { return liczba(v, 0); }),
      series: [
        { label: "Dzień", value: function (u, ts) { return ts == null ? "—" : dataPL(Math.round((ts * 1000 - START) / DZIEN)); } },
        { label: "Zamówienia bez kopii", stroke: css("--series-1"), width: 2, points: { show: false },
          value: function (u, v) { return v == null ? "—" : liczba(v); } },
        { label: "Kopie (duplikaty)", stroke: css("--series-2"), fill: css("--series-2"), width: 0,
          paths: uPlot.paths.bars({ size: [0.6, 24] }), points: { show: false },
          value: function (u, v) { return v == null ? "—" : liczba(v); } }
      ],
      cursor: { drag: { x: true, y: false } },
      tzDate: function (ts) { return uPlot.tzDate(new Date(ts * 1000), "Etc/UTC"); }
    };
    if (wykresDup) wykresDup.destroy();
    wykresDup = new uPlot(opts, [x, JK.duplikaty.zamowienia_d, JK.duplikaty.kopie_d], cel);
  }

  // ------------------------------------------------------------ nawigacja
  var WIDOKI = Array.prototype.map.call(document.querySelectorAll(".zakladki a"), function (a) { return a.dataset.widok; });
  var narysowane = {}, biezacy = null;

  function trasa() {
    var cz = location.hash.slice(1).split("?"), nazwa = decodeURIComponent(cz[0]);
    var widok = WIDOKI.indexOf(nazwa) >= 0 ? nazwa : "wzrost";
    var q = new URLSearchParams(cz[1] || "");
    WIDOKI.forEach(function (v) { $("v-" + v).hidden = v !== widok; });
    Array.prototype.forEach.call(document.querySelectorAll(".zakladki a"), function (a) {
      if (a.dataset.widok === widok) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    if (biezacy !== widok) window.scrollTo(0, 0);
    biezacy = widok;
    if (widok === "lejek") {
      if (!narysowane.lejek) { rysujNaglowekLejka(); przygotujFiltry(); narysowane.lejek = true; }
      czytajAdres(q);
      odswiezLejek();
    }
    if (widok === "zdarzenia") {
      if (!narysowane.zdarzenia) { rysujFiltryZdarzen(); rysujListeZdarzen(); rysujWykryte(); narysowane.zdarzenia = true; }
      rysujOs();
      if (q.get("z")) setTimeout(function () { pokazZdarzenie(q.get("z")); }, 50);
    }
    if (widok === "jakosc") { if (!narysowane.jakosc) { rysujJakosc(); narysowane.jakosc = true; } else rysujWykresDup(); }
    if (window.BW && window.BW[widok]) window.BW[widok].pokaz(q);
  }

  function przerysujWykresy() {
    if (biezacy === "lejek" && narysowane.lejek) odswiezLejek(true, true);
    if (biezacy === "jakosc" && narysowane.jakosc) rysujWykresDup();
    if (biezacy === "zdarzenia" && narysowane.zdarzenia) rysujOs();
    if (window.BW && window.BW[biezacy] && window.BW[biezacy].przerysuj) window.BW[biezacy].przerysuj();
  }

  // pomocnicze funkcje dla widoków z plików widoki.js (kohorty, po zakupie, wynik biznesu)
  // i widoki_c.js (czy to wzrost, priorytety, czego nie wiemy)
  var wczytywane = {};
  function wczytaj(plik, klucz) {
    if (window.D[klucz]) return Promise.resolve(window.D[klucz]);
    if (!wczytywane[plik]) wczytywane[plik] = new Promise(function (ok, blad) {
      var sk = document.createElement("script");
      sk.src = "dane_strony/" + plik + ".js";
      sk.onload = function () { ok(window.D[klucz]); };
      sk.onerror = function () { delete wczytywane[plik]; blad(new Error("Nie udało się wczytać danych: " + plik)); };
      document.body.appendChild(sk);
    });
    return wczytywane[plik];
  }
  window.B = { P: P, ZD: ZD, ET: ET, O: O, NDNI: NDNI, START: START, DZIEN: DZIEN, MIES: MIES, RZYM: RZYM,
    liczba: liczba, proc: proc, znak: znak, dataPL: dataPL, isoIdx: isoIdx, idxIso: idxIso, ogranicz: ogranicz,
    el: el, wyczysc: wyczysc, $: $, css: css, akapity: akapity, osieWykresu: osieWykresu, krocz: krocz,
    zdarzeniaNumerowane: zdarzeniaNumerowane, rysujZdarzeniaNaWykresie: rysujZdarzeniaNaWykresie, wczytaj: wczytaj,
    mostek: mostek };

  var czasResize = null;
  window.addEventListener("resize", function () { clearTimeout(czasResize); czasResize = setTimeout(przerysujWykresy, 200); });
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq.addEventListener) mq.addEventListener("change", przerysujWykresy);
  }
  window.addEventListener("hashchange", trasa);

  $("stopka-meta").textContent = "Dane od " + dataPL(0) + " do " + dataPL(NDNI - 1) + ". Liczby przeliczone " +
    P.meta.wygenerowano + " skryptami analiza/b_eksport.py i analiza/b2_eksport_c.py" + (P.meta.commit ? " (stan repozytorium " + P.meta.commit + ")" : "") +
    ". Strona nie pobiera niczego z internetu.";
  trasa();
})();
