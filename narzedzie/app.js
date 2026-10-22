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
  var BK = window.BK;
  // karta z danych (nowy kształt), a gdy jej nie ma: dotychczasowe zdania
  // (elementy z klasą „zastap” to statyczne przypisy, które karta z danych zastępuje)
  function zdaniaAlboKarta(art, miejsce, karta, zdania, wstawki) {
    if (BK.czyKarta(karta)) {
      BK.kartaW(art, miejsce, karta, { wstawki: wstawki });
      Array.prototype.forEach.call(art.querySelectorAll(".zastap"), function (x) { x.hidden = true; });
      return true;
    }
    if (zdania) akapity(miejsce, zdania);
    return false;
  }
  // karta wstępu zakładki (np. jakość danych, zdarzenia): staje pod nagłówkiem zamiast akapitu wstępu
  function wstepKarta(sekcja, karta) {
    var s = $(sekcja);
    if (!BK.czyKarta(karta) || s.querySelector(".karta-wstep")) return;
    var w = s.querySelector(".wstep"), k = BK.karta(karta, { klasa: "karta-wstep" });
    if (w) { w.hidden = true; w.parentNode.insertBefore(k, w.nextSibling); }
    else s.insertBefore(k, s.querySelector("h2").nextSibling);
  }
  // zmiana w punktach procentowych jako etykieta ze strzałką; wyżej = lepiej, chyba że odwrotnie.
  // o.neutralnie: bez oceny (szara etykieta, np. przy małych grupach, których nie interpretujemy); o.wobec: z czym porównujemy
  function zmianaPkt(d, miejsca, odwrotnie, o) {
    o = o || {};
    var m = miejsca === undefined ? 1 : miejsca, zero = Math.abs(d) < Math.pow(10, -m) / 2;
    var lepiej = odwrotnie ? d < 0 : d > 0, wobec = o.wobec || "wobec okresu A";
    return BK.zmiana(zero ? liczba(0, m) : znak(d, m), zero ? "bez" : BK.kierunekZnaku(d),
      zero || o.neutralnie ? "neutralnie" : lepiej ? "dobrze" : "zle",
      zero ? "Bez zmiany " + wobec : (d > 0 ? "Wzrost" : "Spadek") + " o " + liczba(Math.abs(d), m) + " " + wobec);
  }
  // ikony i znaczniki zapisane w index.html jako miejsca do wypełnienia
  function ikonyStatyczne() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-ikona]"), function (e) { e.parentNode.replaceChild(BK.ikona(e.dataset.ikona), e); });
    Array.prototype.forEach.call(document.querySelectorAll("[data-znacznik]"), function (e) {
      e.parentNode.replaceChild(BK.znacznik({ tekst: e.textContent, stan: e.dataset.znacznik }), e);
    });
  }

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
    tabela.appendChild(el("caption", { class: "przypis",
      text: "Zmiana: ostatnie 12 miesięcy (" + o2 + ") wobec roku wcześniej (" + o1 + "). Pod zmianą: wartość rok wcześniej → wartość w ostatnich 12 miesiącach." }));
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
  // domyślnie osoby, które jeszcze nie kupowały (dla pozyskania liczą się one, a nie pacjenci powracający)
  var S = {
    typ: "zwykla", pac: "nie_kupowal", podz: "przegladarka", krok: "k5s", wygl: 7,
    a: [idxIso(O[0].od), idxIso(O[0].do)], b: [idxIso(O[1].od), idxIso(O[1].do)],
    preset: "rok", wybrane: null, kolory: {}, lw: "__razem"
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
    if (S.lw && S.lw !== "__razem") q.set("lw", S.lw);
    history.replaceState(null, "", "#lejek?" + q.toString());
  }

  function czytajAdres(q) {
    if (!q || !Array.from(q.keys()).length) return;
    // ustawienia, których nie ma w adresie, wracają do domyślnych (a nie zostają z poprzedniego widoku)
    S.typ = "zwykla"; S.pac = "nie_kupowal"; S.podz = "przegladarka"; S.krok = "k5s"; S.wygl = 7; ustawPreset("rok");
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
    // wykres kroków: wartość z adresu, a gdy odnośnik wskazuje jedną wartość podziału — ta wartość
    S.lw = q.get("lw") || (S.wybrane && S.wybrane.length === 1 ? S.wybrane[0] : "__razem");
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
    zdaniaAlboKarta($("lj-naglowek"), $("lj-zdania"), N.karta, N.zdania);
    var n = wyczysc($("lj-naprawy"));
    if (N.naprawy_karty && N.naprawy_karty.length) {
      N.naprawy_karty.forEach(function (k) { n.appendChild(BK.karta(k, { prefiks: "lj-" })); });
    } else {
      // dotychczasowy kształt: karty napraw w karcie nagłówka
      $("lj-zdania").appendChild(el("div", { class: "naprawy" }, N.naprawy.map(function (x) {
        return el("div", { class: "naprawa" }, [el("h4", { text: x.tytul }), el("p", { text: x.tekst }),
          el("a", { href: x.link, text: "Pokaż w lejku" })]);
      })));
    }
    if (BK.czyKarta(N.osobne_karta)) {
      // tytuł karty (wniosek) staje się napisem zwijanej sekcji, reszta karty jej treścią
      var ko = Object.assign({}, N.osobne_karta);
      if (ko.tytul) $("lj-naglowek").querySelector("details.osobne > summary").textContent = ko.tytul;
      delete ko.tytul;
      var o = wyczysc($("lj-osobne")), c = BK.karta(ko);
      while (c.firstChild) o.appendChild(c.firstChild);
    } else akapity($("lj-osobne"), N.osobne);
    $("lj-granica").textContent = N.granica || "";
  }

  function przygotujFiltry() {
    var fp = $("f-podz");
    ["calosc", "urzadzenie", "przegladarka", "system_przegladarka", "urzadzenie_przegladarka", "kanal", "kampania",
      "strona_wejscia"].forEach(function (p) { fp.appendChild(el("option", { value: p, text: ET.podzial[p] })); });
    var pr = $("f-preset");
    pr.appendChild(el("option", { value: "rok", text: "Ostatnie 12 miesięcy wobec roku wcześniej" }));
    pr.appendChild(el("option", { value: "90", text: "Ostatnie 90 dni wobec poprzednich 90" }));
    pr.appendChild(el("option", { value: "30rr", text: "Ostatnie 30 dni wobec tych samych dni rok wcześniej" }));
    ZD.lista.forEach(function (z) {
      pr.appendChild(el("option", { value: "zd:" + z.id, text: "60 dni przed i po: " + (z.krotko || z.tytul) + " (" + dataPL(idxIso(z.od)) + ")" }));
    });
    pr.appendChild(el("option", { value: "wlasne", text: "Własne daty" }));
    var fk = $("f-krok");
    MIARY_WYKRESU.forEach(function (m) {
      fk.appendChild(el("option", { value: m.id, text: m.nazwa + (m.krotko ? " (" + m.krotko + ")" : "") }));
    });
    ["a-od", "a-do", "b-od", "b-do"].forEach(function (k) {
      var i = $("f-" + k); i.min = P.meta.start; i.max = P.meta.koniec;
    });

    $("f-typ").onchange = function () { S.typ = this.value; S.wybrane = null; S.kolory = {}; S.lw = "__razem"; odswiezLejek(); };
    $("f-pac").onchange = function () { S.pac = this.value; odswiezLejek(); };
    $("f-podz").onchange = function () { S.podz = this.value; S.wybrane = null; S.kolory = {}; S.lw = "__razem"; odswiezLejek(); };
    $("f-lw").onchange = function () {
      S.lw = this.value;
      wczytajPodzial(S.podz).then(function (dane) { rysujKrokiLejka(dane); zapiszAdres(); });
    };
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
    var a = el("span", { class: "a", text: "A: " + proc(pA) + " z " + liczba(mA) });
    if (pA !== null && pB !== null) a.appendChild(zmianaPkt(pB - pA, 1));
    td.appendChild(a);
    return td;
  }

  // ------------------------------------------------------------ wykres kroków lejka (liczony z tych samych danych co tabela)
  var KROKI_LEJKA = [
    { pole: "s", nazwa: "Wejście na stronę" }, { pole: "k1", nazwa: ET.kroki.k1 }, { pole: "k2", nazwa: ET.kroki.k2 },
    { pole: "k3", nazwa: ET.kroki.k3 }, { pole: "k4", nazwa: ET.kroki.k4 }, { pole: "k5", nazwa: ET.kroki.k5 }
  ];
  // nazwy okresów porównania; aD to forma po „wobec”
  function nazwyOkresow() {
    if (S.preset === "rok") return { b: "Ostatnie 12 miesięcy", a: "rok wcześniej", aD: "roku wcześniej" };
    if (S.preset === "30rr") return { b: "Ostatnie 30 dni", a: "te same dni rok wcześniej", aD: "tych samych dni rok wcześniej" };
    if (S.preset === "90") return { b: "Ostatnie 90 dni", a: "poprzednie 90 dni", aD: "poprzednich 90 dni" };
    if (S.preset.indexOf("zd:") === 0) return { b: "Po zdarzeniu", a: "przed zdarzeniem", aD: "okresu przed zdarzeniem" };
    return { b: "Okres B", a: "okres A", aD: "okresu A" };
  }
  function rysujKrokiLejka(dane) {
    var lista = wartosci(dane).map(function (w) { return { w: w, n: suma(seria(dane, w).s, S.b) + suma(seria(dane, w).s, S.a) }; })
      .filter(function (x) { return x.n > 0; }).sort(function (x, y) { return y.n - x.n; });
    var sel = wyczysc($("f-lw"));
    sel.appendChild(el("option", { value: "__razem", text: S.podz === "calosc" ? "Całość" : "Razem (wszystkie wartości)" }));
    if (S.podz !== "calosc") lista.forEach(function (x) { sel.appendChild(el("option", { value: x.w, text: etykieta(S.podz, x.w) })); });
    if (S.lw !== "__razem" && !lista.some(function (x) { return x.w === S.lw; })) S.lw = "__razem";
    sel.value = S.lw;
    sel.closest("label").hidden = S.podz === "calosc";

    var sr = seria(dane, S.lw), nz = nazwyOkresow();
    var kroki = [];
    KROKI_LEJKA.forEach(function (k) {
      var nB = suma(sr[k.pole], S.b), nA = suma(sr[k.pole], S.a);
      if (k.pole !== "s" && nB + nA === 0) return;   // krok, którego ten typ sesji nie ma (np. zakup samego TelemediGO)
      kroki.push({ k: k, nB: nB, nA: nA });
    });
    var s0 = kroki[0];
    kroki.forEach(function (x, i) {
      x.pB = s0.nB > 0 ? 100 * x.nB / s0.nB : null;
      x.pA = s0.nA > 0 ? 100 * x.nA / s0.nA : null;
      if (i > 0) {
        var p = kroki[i - 1];
        x.tB = p.nB > 0 ? 100 * x.nB / p.nB : null;
        x.tA = p.nA > 0 ? 100 * x.nA / p.nA : null;
        x.iloraz = x.tB !== null && x.tA ? x.tB / x.tA : null;
      }
    });
    // najbardziej pogorszone przejście: największy względny spadek (ono najbardziej obniża odsetek sesji z płatnością)
    var najgorsze = null;
    kroki.forEach(function (x, i) {
      if (i > 0 && x.iloraz !== null && x.tB < x.tA - 0.05 && (!najgorsze || x.iloraz < najgorsze.iloraz)) najgorsze = x;
    });

    var nazwaW = S.lw === "__razem" ? (S.podz === "calosc" ? "" : "razem") : etykieta(S.podz, S.lw);
    $("lj-kroki-tytul").textContent = "Kroki lejka: " + nz.b.charAt(0).toLowerCase() + nz.b.slice(1) + " wobec " + nz.aD + (nazwaW ? ", " + nazwaW : "");
    $("lj-kroki-opis").textContent = (S.typ === "zwykla" ? "Kto: " + (S.pac === "wszyscy" ? "wszyscy" : ET.pacjent[S.pac].toLowerCase()) + ". " : ET.typ[S.typ] + ". ") +
      opisOkresow();
    var cel = wyczysc($("lj-kroki"));
    if (!s0.nB || !s0.nA) {
      cel.appendChild(el("p", { class: "lejek-pusty", text: "W wybranych okresach nie ma sesji dla tego wyboru. Zmień filtry albo daty." }));
    }
    kroki.forEach(function (x, i) {
      if (!s0.nB && !s0.nA) return;
      if (i > 0) {
        var gorsze = x === najgorsze;
        var dalej = el("div", { class: "lk-dalej" }, [
          el("span", null, ["Przechodzi dalej: ", el("strong", { text: proc(x.tB) })]),
          el("span", { class: "przypis", text: nz.a + ": " + proc(x.tA) }),
          x.tB !== null && x.tA !== null ? zmianaPkt(x.tB - x.tA, 1) : null,
          gorsze ? BK.znacznik({ tekst: "Największy spadek", stan: "zle" }) : null]);
        cel.appendChild(el("div", { class: "lk-przejscie" + (gorsze ? " lk-najgorsze" : ""), role: "listitem" }, [
          el("div", { class: "lk-strzalka" }, [BK.ikona("spadek")]), dalej]));
      }
      var tor = el("div", { class: "lk-tor", title: x.k.nazwa + ": " + proc(x.pB) + " sesji (" + liczba(x.nB) + " z " + liczba(s0.nB) + "), " +
        nz.a + " " + proc(x.pA) + " (" + liczba(x.nA) + " z " + liczba(s0.nA) + ")" }, [
        el("div", { class: "lk-pasek", style: "width:" + Math.max(0, Math.min(100, x.pB || 0)) + "%" }),
        x.pA !== null ? el("div", { class: "lk-kreska", style: "left:" + Math.max(0, Math.min(100, x.pA)) + "%" }) : null]);
      cel.appendChild(el("div", { class: "lk-krok", role: "listitem" }, [
        el("div", { class: "lk-nazwa" }, [x.k.nazwa, el("span", { class: "lk-n", text: liczba(x.nB) + " sesji" })]),
        tor,
        el("div", { class: "lk-wart" }, [el("span", { class: "lk-b", text: proc(x.pB) }),
          el("span", { class: "lk-a", text: nz.a + ": " + proc(x.pA) })])]));
    });
    var lg = wyczysc($("lj-kroki-legenda"));
    lg.appendChild(el("span", { class: "lg" }, [el("span", { class: "lg-pasek" }), nz.b + ": odsetek sesji, które doszły do kroku"]));
    lg.appendChild(el("span", { class: "lg" }, [el("span", { class: "lg-kreska" }), "Ten sam odsetek: " + nz.a]));
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
    ctx.strokeStyle = css("--muted"); ctx.fillStyle = css("--ink-2"); ctx.lineWidth = 1 * dpr;
    ctx.globalAlpha = 0.7; ctx.setLineDash([3 * dpr, 3 * dpr]);
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
      leg.appendChild(el("li", null, [el("a", { href: "#zdarzenia?z=" + z.id, text: dataPL(idxIso(z.od)) + ": " + (z.krotko || z.tytul) })]));
    });
  }

  function odswiezLejek(tylkoWykres, tabelaTez) {
    ustawKontrolki();
    var cel = $("lj-wykres");
    cel.style.opacity = "0.5";
    wczytajPodzial(S.podz).then(function (dane) {
      if (!tylkoWykres || tabelaTez) { rysujTabeleLejka(dane); rysujKrokiLejka(dane); }
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
      var link = z.link ? el("a", { href: z.link, text: napisOdnosnika(z.link) }) : null;
      l.appendChild(el("article", { class: "karta zdarzenie", id: "zd-" + z.id }, [
        el("div", { class: "meta" }, [el("span", { class: "data", text: z.nr + ". " + dataPL(idxIso(z.od)) + (z.do ? "–" + dataPL(idxIso(z.do)) : "") }),
          el("span", { class: "obszar", text: ET.obszary[z.obszar] }), el("span", { text: z.rodzaj })]),
        el("h3", { text: z.tytul }), dl, link ? el("p", null, [link]) : null]));
    });
  }

  // napis odnośnika według zakładki, do której prowadzi
  var NAPISY_ODNOSNIKOW = { lejek: "Pokaż w lejku", kohorty: "Pokaż w kohortach", "po-zakupie": "Pokaż w zakładce „Po zakupie”",
    wynik: "Pokaż w wyniku biznesu", jakosc: "Zobacz w jakości danych", zdarzenia: "Pokaż na osi zdarzeń", priorytety: "Pokaż w priorytetach" };
  function napisOdnosnika(href) {
    var cel = href.slice(1).split("?")[0];
    return NAPISY_ODNOSNIKOW[cel] || "Pokaż";
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
          el("td", null, [BK.zmiana(znak(r[ix.zmiana], 1) + (ruch ? "" : " pkt proc."), BK.kierunekZnaku(r[ix.zmiana]),
            ruch ? "neutralnie" : r[ix.zmiana] >= 0 ? "dobrze" : "zle")]),
          el("td", { text: r[ix.dni_przed] + " / " + r[ix.dni_po] }),
          el("td", { text: r[ix.zamowienia_na_30_dni] === null ? "—" : znak(r[ix.zamowienia_na_30_dni], 1) }),
          el("td", null, [el("a", { href: "#lejek?" + q.toString(), text: "w lejku" })])]));
      });
    t.appendChild(tb);
  }

  // ------------------------------------------------------------ jakość danych
  var wykresDup = null;
  function rysujJakosc() {
    // karty z danych: D.jakosc.karty.* (kontrakt, notatki/e_runda.md 3.5), a gdy ich nie ma — dotychczasowe zdania
    var KJ = JK.karty || {};
    wstepKarta("v-jakosc", JK.karta);
    mostek($("jk-mostek"));
    zdaniaAlboKarta($("jk-karta-mostek"), $("jk-mostek-zdania"), KJ.mostek, null,
      { mostek: function () { return $("jk-mostek").closest(".tabela-ramka"); } });
    zdaniaAlboKarta($("jk-karta-dup"), $("jk-dup-zdania"), KJ.duplikaty || JK.duplikaty.karta, JK.duplikaty.zdania);
    zdaniaAlboKarta($("jk-karta-testy"), $("jk-testy-zdania"), KJ.testy || JK.testy.karta, JK.testy.zdania);
    var kw = wyczysc($("jk-testy-kw")), mx = Math.max.apply(null, JK.testy.kwartaly.map(function (k) { return k.n; }));
    kw.appendChild(el("span", { class: "przypis", text: "Kwartał" }));
    kw.appendChild(el("span", { class: "przypis", text: "Zamówienia testowe" }));
    JK.testy.kwartaly.forEach(function (k) {
      kw.appendChild(el("span", { text: kwartal(k.kw) }));
      kw.appendChild(el("div", { class: "slupek-wiersz" }, [el("div", { class: "slupek", style: "width:" + (70 * k.n / mx) + "%" }),
        el("span", { text: liczba(k.n) })]));
    });
    zdaniaAlboKarta($("jk-karta-godzina"), $("jk-godzina"), KJ.godzina || JK.godzina.karta, [JK.godzina.zdanie]);
    [["drobne", KJ.drobne || JK.karta_drobne, JK.drobne], ["czyste", KJ.czyste || JK.karta_czyste, JK.czyste]].forEach(function (x) {
      if (BK.czyKarta(x[1])) { BK.kartaW($("jk-karta-" + x[0]), $("jk-" + x[0]), x[1]); return; }
      var ul = el("ul", { class: "punkty" });
      x[2].forEach(function (z) { ul.appendChild(el("li", { text: z })); });
      wyczysc($("jk-" + x[0])).appendChild(ul);
    });
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
      if (q && Array.from(q.keys()).length) setTimeout(function () {
        $("lj-tabela").closest(".karta").scrollIntoView({ behavior: "smooth", block: "start" });
      }, 60);
    }
    if (widok === "zdarzenia") {
      if (!narysowane.zdarzenia) { wstepKarta("v-zdarzenia", ZD.karta); rysujFiltryZdarzen(); rysujListeZdarzen(); rysujWykryte(); narysowane.zdarzenia = true; }
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
    mostek: mostek, BK: BK, zdaniaAlboKarta: zdaniaAlboKarta, zmianaPkt: zmianaPkt, wstepKarta: wstepKarta };
  ikonyStatyczne();

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
