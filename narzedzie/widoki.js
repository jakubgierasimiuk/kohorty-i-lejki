/* Widoki: Kohorty, Po zakupie, Wynik biznesu. Dane z dane_strony/ (tworzy je analiza/b_eksport.py).
   Ten plik nie wpisuje żadnych wyników: liczy sumy i odsetki dla wybranych filtrów i je formatuje.
   Pomocnicze funkcje (formatowanie, wykresy) udostępnia app.js jako window.B. */
(function () {
  "use strict";
  var BW = window.BW = {};
  var ZN = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var b = function () { return window.B; };

  // ------------------------------------------------------------ wspólne
  function okresyPreset(p, S) {
    var B = b(), O = B.O, N = B.NDNI;
    S.preset = p;
    if (p === "rok") { S.a = [B.idxIso(O[0].od), B.idxIso(O[0].do)]; S.b = [B.idxIso(O[1].od), B.idxIso(O[1].do)]; }
    else if (p === "90") { S.b = [N - 90, N - 1]; S.a = [N - 180, N - 91]; }
    else if (p === "30rr") { S.b = [N - 30, N - 1]; S.a = [N - 395, N - 366]; }
    else if (p.indexOf("zd:") === 0) {
      var z = B.ZD.lista.filter(function (x) { return x.id === p.slice(3); })[0];
      if (z) { var d = B.idxIso(z.od); S.a = [B.ogranicz(d - 60), B.ogranicz(d - 1)]; S.b = [B.ogranicz(d), B.ogranicz(d + 59)]; }
    }
  }
  function opcjePresetow(sel) {
    var B = b();
    [["rok", "Ostatnie 12 miesięcy wobec roku wcześniej"], ["90", "Ostatnie 90 dni wobec poprzednich 90"],
      ["30rr", "Ostatnie 30 dni wobec tych samych dni rok wcześniej"]].forEach(function (o) {
      sel.appendChild(B.el("option", { value: o[0], text: o[1] }));
    });
    // tylko zdarzenia, które mogły zmienić kohorty: bez godziny bez danych i duplikatów w eksporcie (obszar „jakość danych”)
    B.ZD.lista.forEach(function (z) {
      if (z.obszar === "jakosc") return;
      sel.appendChild(B.el("option", { value: "zd:" + z.id, text: "60 dni przed i po: " + (z.krotko || z.tytul) + " (" + B.dataPL(B.idxIso(z.od)) + ")" }));
    });
    sel.appendChild(B.el("option", { value: "wlasne", text: "Własne daty" }));
  }
  function wybor(id, etyk, opcje, wartosc, zmiana) {
    var B = b(), s = B.el("select", { id: id });
    opcje.forEach(function (o) { s.appendChild(B.el("option", { value: o[0], text: o[1] })); });
    s.value = wartosc;
    s.onchange = function () { zmiana(this.value); };
    return B.el("label", null, [etyk, s]);
  }
  function cieniuj(u, a, bb, nazwy) { b().polaOkresow(u, a, bb, nazwy); }
  /* serie: [{label, kolor (numer serii albo kolor css), y, opis(di, v)}],
     o: {jednostka, procent, a, b, nazwy: {a, b} (podpisy pól okresów), zdarzenia, x, min, max} */
  // wykres dzienny (uPlot) z własną legendą: o.id, o.obszary (zdarzenia tylko z tych obszarów), o.odswiez, o.wybor, o.koncowe;
  // seria: {label, kolor, y, opis(di, v), w (klucz do wyboru), szer (grubość linii)}
  function wykres(cel, serie, o) {
    var B = b();
    B.wyczysc(cel);
    var x = o.x;
    if (!x) { x = new Float64Array(B.NDNI); for (var i = 0; i < B.NDNI; i++) x[i] = (B.START + i * B.DZIEN) / 1000; }
    var etX = o.etykietaX || function (u, ts) { return ts == null ? "—" : B.dataPL(Math.round((ts * 1000 - B.START) / B.DZIEN)); };
    var dane = [x], ser = [{ label: "Dzień" }], opisy = [];
    serie.forEach(function (s) {
      dane.push(s.y);
      var kol = typeof s.kolor === "number" ? B.css("--series-" + s.kolor) : s.kolor;
      ser.push({ label: s.label, stroke: kol, width: s.szer || 2, points: { show: !!o.punkty, size: 6 } });
      opisy.push({ label: s.label, kolor: kol, w: s.w, gruba: (s.szer || 2) > 2,
        wart: function (v, di) { return s.opis ? s.opis(di, v) : B.liczba(v, 1); } });
    });
    var zd = o.listaZd || (o.zdarzenia ? B.zdarzeniaWykresu(o.id || "", o.obszary || null) : []);
    var lista = o.listaZd ? (o.listaPod ? zd : null) : (o.zdarzenia ? zd : null);
    var opts = {
      width: cel.clientWidth || 300, height: o.wys || 320,
      scales: { x: { time: true, min: o.min, max: o.max },
        y: { range: function (u, mn, mx) { return [Math.min(0, mn), o.procent ? Math.min(100, Math.max(5, mx * 1.08)) : (mx > 0 ? mx * 1.08 : 1)]; } } },
      axes: B.osieWykresu("", o.formatY || function (v) { return B.liczba(v, 0) + (o.procent ? "%" : ""); }),
      series: ser, cursor: { drag: { x: true, y: false } },
      tzDate: function (ts) { return uPlot.tzDate(new Date(ts * 1000), "Etc/UTC"); },
      hooks: { drawClear: [function (u) { cieniuj(u, o.a, o.b, o.nazwy); }], draw: [function (u) { if (zd.length) B.rysujZdarzeniaNaWykresie(u, zd); }] }
    };
    if (o.osX) opts.axes[0].values = o.osX;
    var dorysuj = B.legendaUplot(opts, cel, { id: o.id || "", serie: opisy, koncowe: o.koncowe !== false,
      etykietaX: function (ts) { return etX(null, ts); }, obszary: o.zdarzenia && !o.listaZd ? (o.obszary || null) : null,
      zdarzenia: lista, odswiez: o.odswiez, wybor: o.wybor });
    var u = new uPlot(opts, dane, cel);
    dorysuj();
    return u;
  }
  function krocz(arr, w) { return b().krocz(arr, w); }
  function suma(arr, z) { var t = 0; if (!z) return 0; for (var i = z[0]; i <= z[1]; i++) t += arr[i]; return t; }
  // o (opcjonalnie): {pref: napis przed wartością porównania, wobec: podpowiedź etykiety, neutralnie: etykieta bez oceny}
  function komorka(pB, nB, pA, nA, jedn, miejsca, odwrotnie, o) {
    o = o || {};
    var B = b(), td = B.el("td"), j = jedn === undefined ? "%" : jedn, m = miejsca === undefined ? 1 : miejsca;
    var f = function (v) { return v === null || !isFinite(v) ? "—" : B.liczba(v, m) + (j === "%" ? "%" : j ? " " + j : ""); };
    td.appendChild(B.el("span", { class: "b", text: f(pB) }));
    // „z” i liczba sklejone twardą spacją, żeby na wąskim ekranie nie rozdzielał ich koniec wiersza
    td.appendChild(B.el("span", { class: "n", text: nB !== null ? " z " + B.liczba(nB) : "" }));
    var a = B.el("span", { class: "a", text: (o.pref || "A: ") + f(pA) + (nA !== null ? " z " + B.liczba(nA) : "") });
    if (pA !== null && pB !== null && isFinite(pA) && isFinite(pB)) {
      // runda G: kolor tylko przy wyraźnej zmianie (95% przedział różnicy odsetków bez zera); średnie bez przedziału
      // (np. średnia ocena) to zmiana opisowa, bez oceny
      var ist = j === "%" && nA && nB ? B.BK.roznicaOdsetkow(pA * nA / 100, nA, pB * nB / 100, nB) : null;
      var szara = !ist || !ist.wyrazna, oo = Object.assign({}, o, szara ? { neutralnie: true } : {});
      var tag = B.zmianaPkt(pB - pA, m, odwrotnie, oo);
      if (szara) {
        tag.classList.add("zm-szara");
        tag.title = ist ? "Bez wyraźnej zmiany. 95% przedział zmiany: od " + B.znak(ist.od, 1) + " do " + B.znak(ist.do, 1) + " pkt proc." :
          "Zmiana opisowa, bez oceny istotności";
      } else tag.title = (tag.title ? tag.title + ". " : "") + "95% przedział zmiany: od " + B.znak(ist.od, 1) + " do " + B.znak(ist.do, 1) + " pkt proc.";
      a.appendChild(tag);
    }
    td.appendChild(a);
    return td;
  }
  function legendaPod(t, o) {
    var B = b(), r = t.closest(".tabela-ramka"), n = r.nextElementSibling;
    if (!n || !n.classList.contains("legenda-zmian")) { n = B.el("p", { class: "legenda-zmian" }); r.parentNode.insertBefore(n, r.nextSibling); }
    B.BK.legendaIstotnosci(n, o);
  }
  function opisOkresow(S) {
    var B = b();
    return "Okres A: " + B.dataPL(S.a[0]) + "–" + B.dataPL(S.a[1]) + ". Okres B: " + B.dataPL(S.b[0]) + "–" + B.dataPL(S.b[1]) + ".";
  }
  function datyAB(pref, S, odswiez) {
    var B = b(), f = B.el("div", { class: "filtry-daty" });
    ["a", "b"].forEach(function (k) {
      var nazwa = k === "a" ? "Wcześniejszy okres" : "Późniejszy okres";
      var fs = B.el("fieldset", { class: "okresy" }, [B.el("legend", { text: nazwa })]);
      ["od", "do"].forEach(function (g, j) {
        var i = B.el("input", { type: "date", id: pref + "-" + k + "-" + g, min: B.P.meta.start, max: B.P.meta.koniec,
          "aria-label": nazwa + " " + g });
        i.value = B.isoIdx(S[k][j]);
        i.onchange = function () {
          if (!this.value) return;
          S[k][j] = B.ogranicz(B.idxIso(this.value));
          if (S[k][0] > S[k][1]) S[k] = [S[k][1], S[k][0]];
          S.preset = "wlasne"; odswiez();
        };
        fs.appendChild(i);
        if (j === 0) fs.appendChild(document.createTextNode(" – "));
      });
      f.appendChild(fs);
    });
    return f;
  }

  // ------------------------------------------------------------ KOHORTY
  // Układ od góry (uwagi Kuby z 2026-10-23): wniosek niezależny od ustawień; pasek „Pacjenci w analizie” (przypisanie
  // źródła, zawężenia jako etykiety, „Przywróć domyślne”), przyklejony przy przewijaniu i działający na wszystko pod nim;
  // mapa kohort; karta „dzień po dniu” z całym sterowaniem w nagłówku, zdarzeniami jako przyciskami porównania 60 dni
  // przed i po i tabelą grup; krzywa powrotu na końcu.
  var WYMIARY = [
    { id: "kanal", nazwa: "Źródło (kanał)", reg: true }, { id: "kampania", nazwa: "Kampania", reg: true },
    { id: "grupa", nazwa: "Nowe kampanie na L4" }, { id: "urzadzenie", nazwa: "Urządzenie" },
    { id: "przegladarka", nazwa: "Przeglądarka" }, { id: "usluga", nazwa: "Pierwsza usługa" },
    { id: "znizka", nazwa: "Zniżka" }, { id: "go0", nazwa: "TelemediGO przy pierwszym zakupie" },
    { id: "status1", nazwa: "Status pierwszego zamówienia" }, { id: "koszyk", nazwa: "Opóźnienie pierwszej wizyty" },
    { id: "pora", nazwa: "Pora pierwszej wizyty" }
  ];
  var zawezOtwarte = false;
  var MIARY_K = [["powrot", "Powrót w oknie"], ["marza", "Marża na pacjenta w oknie"], ["nowi", "Nowi pacjenci dziennie"],
    ["udzial", "Udział w nowych pacjentach"]];
  var K = null, KOD = {}, KS = null, wykresK = null, gotoweK = false;
  // Zdarzenia, które mogły zmienić kohorty: wszystkie poza jakością danych (godzina bez danych, duplikaty w eksporcie).
  // Na wykresie domyślnie przyczyny (obszary lejek i obsługa pacjenta: kampanie, awarie, zwroty, opóźnienia); zmiany
  // wykryte w samych kohortach (obszar retencja, czyli skutki) po zaznaczeniu przełącznika pod wykresem.
  var OBSZARY_PRZYCZYN = ["lejek", "obsluga"];
  function zdarzeniaKohort() { return b().zdarzeniaNumerowane().filter(function (z) { return z.obszar !== "jakosc"; }); }
  function zdarzeniaWykresuK() {
    return zdarzeniaKohort().filter(function (z) { return KS.skutki || OBSZARY_PRZYCZYN.indexOf(z.obszar) >= 0; });
  }

  function domyslneK() {
    var s = { regula: "Z1K", f: {}, podz: "grupa", okno: 90, miara: "powrot", wygl: 7, preset: "rok", wybrane: null, kolory: {},
      tryb: "miara", skutki: false, gran: "mies" };
    okresyPreset("rok", s);
    return s;
  }
  function wielka(t) { return t ? t.charAt(0).toUpperCase() + t.slice(1) : t; }
  // porównywane okresy słowami, bez „A” i „B”: a, b (nagłówki i zdania), aD (po „wobec”), z (po „poziomu”)
  function nazwyK() {
    var B = b(), p = KS.preset;
    if (p === "wlasne") {
      var a = B.dataPL(KS.a[0]) + "–" + B.dataPL(KS.a[1]), bb = B.dataPL(KS.b[0]) + "–" + B.dataPL(KS.b[1]);
      return { a: a, b: bb, aD: a, z: "z okresu " + a };
    }
    if (p.indexOf("zd:") === 0) return { a: "60 dni przed", b: "60 dni po", aD: "60 dni przed zdarzeniem", z: "sprzed zdarzenia" };
    var n = B.nazwyPresetu(p);
    return { a: n.a, b: n.b.charAt(0).toLowerCase() + n.b.slice(1), aD: n.aD, z: "z " + n.aD };
  }
  function kluczWym(id) {
    var w = WYMIARY.filter(function (x) { return x.id === id; })[0];
    return w && w.reg && KS.regula === "Z2" ? id + "_z2" : id;
  }
  function etykietaWart(id, v) {
    var B = b(), ET = B.ET;
    if (v === "__razem") return "Wszyscy wybrani pacjenci";
    if (id === "grupa") return v === "nowe" ? "Nowe kampanie na L4" : "Pozostałe kampanie i kanały";
    if (id === "znizka" && !(ET.znizka && ET.znizka[v])) return "Kod " + v;
    var m = ET[id];
    return (m && m[v]) || v;
  }
  function wartosciWym(id) {
    if (id === "grupa") return ["nowe", "pozostale"];
    return K.wart[kluczWym(id)];
  }
  function kodyWym(id) {
    if (id === "grupa") {
      var kk = kluczWym("kampania"), nowe = b().ET.nowe_kampanie, kody = KOD[kk], w = K.wart[kk];
      var czyNowa = w.map(function (x) { return nowe.indexOf(x) >= 0 ? 0 : 1; });
      var out = new Uint8Array(K.n);
      for (var i = 0; i < K.n; i++) out[i] = czyNowa[kody[i]];
      return out;
    }
    return KOD[kluczWym(id)];
  }
  function przygotujK() {
    Object.keys(K.kat).forEach(function (k) {
      var s = K.kat[k], a = new Uint8Array(K.n);
      for (var i = 0; i < K.n; i++) a[i] = ZN.indexOf(s.charAt(i));
      KOD[k] = a;
    });
  }
  function zakresyOkna(n) {
    var N = b().NDNI, ost = N - 1 - n, bk = Math.min(KS.b[1], ost);
    if (bk < KS.b[0]) return null;
    var dl = bk - KS.b[0], ak = Math.min(KS.a[1], KS.a[0] + dl, ost);
    if (ak < KS.a[0]) return null;
    return { a: [KS.a[0], ak], b: [KS.b[0], bk] };
  }
  function filtryAktywne() {
    return Object.keys(KS.f).filter(function (id) { return KS.f[id] !== ""; }).map(function (id) {
      return { kody: kodyWym(id), idx: wartosciWym(id).indexOf(KS.f[id]) };
    });
  }
  function pacjenciFiltru() {
    var f = filtryAktywne(), out = [];
    for (var i = 0; i < K.n; i++) {
      var ok = true;
      for (var j = 0; j < f.length; j++) if (f[j].kody[i] !== f[j].idx) { ok = false; break; }
      if (ok) out.push(i);
    }
    return out;
  }

  // ---------- adres i „Przywróć domyślne”: w adresie tylko ustawienia inne niż startowe
  function adresK() {
    var q = new URLSearchParams(), B = b(), D = domyslneK();
    if (KS.regula !== D.regula) q.set("regula", KS.regula);
    if (KS.podz !== D.podz) q.set("podz", KS.podz);
    if (KS.okno !== D.okno) q.set("okno", KS.okno);
    if (KS.miara !== D.miara) q.set("miara", KS.miara);
    if (KS.wygl !== D.wygl) q.set("wygl", KS.wygl);
    if (KS.a.join() !== D.a.join() || KS.b.join() !== D.b.join()) {
      q.set("a", B.isoIdx(KS.a[0]) + "_" + B.isoIdx(KS.a[1])); q.set("b", B.isoIdx(KS.b[0]) + "_" + B.isoIdx(KS.b[1]));
    }
    WYMIARY.forEach(function (w) { if (KS.f[w.id]) q.set("f_" + w.id, KS.f[w.id]); });
    if (KS.wybrane && KS.wybraneDomyslne && KS.wybrane.join() !== KS.wybraneDomyslne.join()) q.set("w", KS.wybrane.join(","));
    if (KS.tryb !== D.tryb) q.set("tabela", KS.tryb);
    if (KS.skutki) q.set("skutki", "1");
    if (KS.gran !== D.gran) q.set("mapa", KS.gran);
    return q.toString();
  }
  function zapiszAdresK() {
    var s = adresK();
    history.replaceState(null, "", "#kohorty" + (s ? "?" + s : ""));
    var r = b().$("ko-reset");
    if (r) { r.disabled = !s; r.title = s ? "Wraca do ustawień startowych zakładki i czyści adres" : "Ustawienia są startowe"; }
  }
  function czytajAdresK(q) {
    if (!q || !Array.from(q.keys()).length) { if (!KS) KS = domyslneK(); return; }
    var B = b();
    KS = domyslneK();
    if (q.get("regula")) KS.regula = q.get("regula");
    if (q.has("podz")) KS.podz = q.get("podz");
    if (q.get("okno")) KS.okno = +q.get("okno");
    if (q.get("miara")) KS.miara = q.get("miara");
    if (q.get("wygl")) KS.wygl = +q.get("wygl");
    if (q.get("tabela") === "wszystkie") KS.tryb = "wszystkie";
    if (q.get("skutki") === "1") KS.skutki = true;
    if (["mies", "tydz", "dzien"].indexOf(q.get("mapa")) >= 0) KS.gran = q.get("mapa");
    ["a", "b"].forEach(function (k) {
      var v = q.get(k);
      if (v && v.indexOf("_") > 0) { var c = v.split("_"); KS[k] = [B.ogranicz(B.idxIso(c[0])), B.ogranicz(B.idxIso(c[1]))]; KS.preset = "wlasne"; }
    });
    var r = domyslneK();
    if (KS.preset === "wlasne" && KS.a.join() === r.a.join() && KS.b.join() === r.b.join()) KS.preset = "rok";
    // daty „60 dni przed i po” zdarzeniu (np. z tabeli zdarzeń): na liście porównań ta pozycja, a nie „własne daty”
    if (KS.preset === "wlasne") B.ZD.lista.some(function (z) {
      if (z.obszar === "jakosc") return false;   // tych zdarzeń nie ma na liście porównań
      var t = {};
      okresyPreset("zd:" + z.id, t);
      if (t.a && t.a.join() === KS.a.join() && t.b.join() === KS.b.join()) { KS.preset = "zd:" + z.id; return true; }
      return false;
    });
    WYMIARY.forEach(function (w) { if (q.get("f_" + w.id)) KS.f[w.id] = q.get("f_" + w.id); });
    KS.wybrane = q.get("w") ? q.get("w").split(",").filter(Boolean) : null;
  }
  function przywrocK() {
    KS = domyslneK();
    zawezOtwarte = false;
    history.replaceState(null, "", "#kohorty");
    sterowanieK(); filtryMacierzy(); rysujK();
  }
  // przyklejony pasek: pod przyklejonym nagłówkiem strony (komputer), na górze ekranu (telefon, nagłówek nie jest przyklejony)
  function przyklej() { if (b().przyklejPaski) b().przyklejPaski(); }

  // ---------- pasek „Pacjenci w analizie”
  function pasekK() {
    var B = b(), box = B.wyczysc(B.$("ko-pasek"));
    WYMIARY.forEach(function (w) { if (KS.f[w.id] && wartosciWym(w.id).indexOf(KS.f[w.id]) < 0) KS.f[w.id] = ""; });
    var n = pacjenciFiltru().length, akt = WYMIARY.filter(function (w) { return KS.f[w.id]; });
    var w = B.el("div", { class: "pa-wnetrze" });
    w.appendChild(B.el("div", { class: "pa-tytul" }, [B.el("strong", { text: "Pacjenci w analizie" }),
      B.el("span", { class: "pa-liczba", text: B.liczba(n) + " " + (n === 1 ? "nowy pacjent" : "nowych pacjentów") +
        (akt.length ? " po zawężeniu" : ", wszyscy") })]));
    w.appendChild(wybor("ko-regula", "Przypisanie źródła", [["Z1K", "według pierwszego wejścia"], ["Z2", "według sesji z płatnością"]],
      KS.regula, function (v) { KS.regula = v; KS.wybrane = null; KS.kolory = {}; rysujK(); }));
    var chipy = B.el("div", { class: "pa-chipy" }, [B.el("span", { class: "pa-etykieta", text: "Zawężenia" })]);
    akt.forEach(function (x) {
      var c = B.el("button", { type: "button", class: "chip chip-usun", "aria-label": "Usuń zawężenie: " + x.nazwa },
        [x.nazwa + ": " + etykietaWart(x.id, KS.f[x.id]), B.el("span", { "aria-hidden": "true", text: "×" })]);
      c.onclick = function () { KS.f[x.id] = ""; rysujK(); };
      chipy.appendChild(c);
    });
    var d = B.el("details", { class: "pa-zawez" }, [B.el("summary", { text: akt.length ? "Zmień" : "Dodaj zawężenie" })]);
    var siatka = B.el("div", { class: "pa-panel" });
    WYMIARY.forEach(function (x) {
      var opcje = [["", "wszystkie"]].concat(wartosciWym(x.id).map(function (v) { return [v, etykietaWart(x.id, v)]; }));
      siatka.appendChild(wybor("ko-f-" + x.id, x.nazwa, opcje, KS.f[x.id] || "", function (v) { KS.f[x.id] = v; rysujK(); }));
    });
    var zamknij = B.el("button", { type: "button", class: "przycisk-maly", text: "Zamknij" });
    zamknij.onclick = function () { d.open = false; };
    siatka.appendChild(zamknij);
    d.appendChild(siatka);
    d.open = zawezOtwarte;
    d.addEventListener("toggle", function () { zawezOtwarte = d.open; });
    chipy.appendChild(d);
    w.appendChild(chipy);
    var reset = B.el("button", { type: "button", class: "przycisk-maly pa-reset", id: "ko-reset", text: "Przywróć domyślne" });
    reset.onclick = przywrocK;
    w.appendChild(reset);
    box.appendChild(w);
    przyklej();
  }
  // jedna krótka linijka przy każdej karcie zależnej od ustawień: od których
  function zalezyK() {
    var B = b(), nz = nazwyK();
    B.$("ko-macierz-zalezy").textContent = "Zależy od paska „Pacjenci w analizie”.";
    B.$("ko-wykres-zalezy").textContent = "Zależy od paska „Pacjenci w analizie” i od ustawień tej karty; tabela grup niżej używa tych samych.";
    B.$("ko-krzywa-zalezy").textContent = "Zależy od paska „Pacjenci w analizie” i od porównania wybranego w karcie „Dzień po dniu” (teraz: " +
      nz.a + " i " + nz.b + ").";
  }

  // ---------- mapa kohort (domyślnie miesięczna, decyzja Kuby): dzienne kohorty po ok. 40 pacjentów skaczą z dnia na dzień,
  // a rozdzielczość dzienną pokazuje wykres dzień po dniu pod mapą; tygodniowe i dzienne są o jedno kliknięcie
  var OKNA_MACIERZY = [7, 14, 30, 60, 90, 180], wykresKrz = null;
  // jedna skala koloru dla całej macierzy: ten sam kolor = ten sam przedział odsetka w każdym oknie i po każdym filtrze
  // (progi dobrane tak, żeby w każdym oknie były co najmniej dwa odcienie); kolory z tokenów --heat-0…7 w styl.css
  var PROGI_MACIERZY = [5, 10, 15, 20, 25, 30, 35];
  function klasaMacierzy(v) { var k = 0; while (k < PROGI_MACIERZY.length && v >= PROGI_MACIERZY[k]) k++; return k; }
  function skalaMacierzy() {
    var B = b(), cel = B.$("ko-macierz-skala");
    if (!cel || cel.firstChild) return;
    var ol = B.el("ol", { "aria-label": "Skala koloru: powrót w oknie" });
    for (var k = 0; k <= PROGI_MACIERZY.length; k++) {
      var t = k === 0 ? "poniżej " + PROGI_MACIERZY[0] + "%" : k === PROGI_MACIERZY.length ? PROGI_MACIERZY[k - 1] + "% i więcej" :
        PROGI_MACIERZY[k - 1] + "–" + PROGI_MACIERZY[k] + "%";
      ol.appendChild(B.el("li", null, [B.el("span", { class: "pole hm" + k }), B.el("span", { text: t })]));
    }
    cel.appendChild(B.el("span", { text: "Powrót w oknie:" }));
    cel.appendChild(ol);
    cel.appendChild(B.el("span", null, [B.el("span", { class: "pusta" }), "brak pełnego okna"]));
  }
  function grupyKohort(gran) {
    var B = b(), N = B.NDNI, gr = [], cur = null;
    for (var i = 0; i < N; i++) {
      var d = new Date(B.START + i * B.DZIEN);
      var kl = gran === "dzien" ? i : gran === "tydz" ? i - ((d.getUTCDay() + 6) % 7) : d.getUTCFullYear() * 100 + d.getUTCMonth();
      if (!cur || cur.kl !== kl) { cur = { kl: kl, od: i, do: i }; gr.push(cur); } else cur.do = i;
    }
    return gr;
  }
  function rysujMacierz() {
    var B = b(), N = B.NDNI, idx = pacjenciFiltru(), gr = grupyKohort(KS.gran), przyp = new Int32Array(N);
    gr.forEach(function (g, j) { for (var i = g.od; i <= g.do; i++) przyp[i] = j; });
    var st = gr.map(function () { return { n: 0, r: OKNA_MACIERZY.map(function () { return 0; }) }; });
    idx.forEach(function (i) {
      var s_ = st[przyp[K.d[i]]], r = K.r[i];
      s_.n++;
      if (r >= 0) OKNA_MACIERZY.forEach(function (w, k) { if (r <= w) s_.r[k]++; });
    });
    var zd = zdarzeniaKohort();
    var wiersze = gr.map(function (g, j) {
      var x = st[j];
      return { g: g, n: x.n, p: OKNA_MACIERZY.map(function (w, k) { return g.do <= N - 1 - w && x.n > 0 ? 100 * x.r[k] / x.n : null; }),
        zd: zd.filter(function (z) { var di = B.idxIso(z.od); return di >= g.od && di <= g.do; }) };
    });
    skalaMacierzy();
    wniosekMacierzy();
    // miesięczna mapa (24 wiersze) stoi cała, bez przewijania w ramce; tygodniowa i dzienna przewijają się w ramce
    B.$("ko-macierz").closest(".macierz-ramka").classList.toggle("przewijana", KS.gran !== "mies");
    var t = B.wyczysc(B.$("ko-macierz"));
    var hr = B.el("tr", null, [B.el("th", { text: KS.gran === "dzien" ? "Kohorta (dzień)" : KS.gran === "tydz" ? "Kohorta (tydzień od)" : "Kohorta (miesiąc)" }),
      B.el("th", { text: "Nowi pacjenci" })]);
    OKNA_MACIERZY.forEach(function (w) { hr.appendChild(B.el("th", { text: w + " dni" })); });
    hr.appendChild(B.el("th", { class: "macierz-zd", text: "Zdarzenia w tej kohorcie" }));
    t.appendChild(B.el("thead", null, [hr]));
    var tb = B.el("tbody");
    wiersze.forEach(function (r) {
      var d = new Date(B.START + r.g.od * B.DZIEN);
      var naz = KS.gran !== "mies" ? B.dataPL(r.g.od) : B.RZYM[d.getUTCMonth()] + " " + d.getUTCFullYear();
      var tr = B.el("tr", null, [B.el("td", { text: naz }), B.el("td", { text: B.liczba(r.n) })]);
      r.p.forEach(function (v, k) {
        if (v === null) { tr.appendChild(B.el("td", { class: "macierz-pusta", text: "·", title: "Kohorta nie ma jeszcze pełnego okna " + OKNA_MACIERZY[k] + " dni" })); return; }
        tr.appendChild(B.el("td", { class: "macierz-kom hm" + klasaMacierzy(v),
          text: B.liczba(v, 1), title: naz + ": powrót w " + OKNA_MACIERZY[k] + " dniach " + B.proc(v) + " z " + B.liczba(r.n) + " pacjentów" }));
      });
      // krótkie nazwy zdarzeń zamiast numerów (uwaga Kuby); pełny tytuł i data w podpowiedzi
      tr.appendChild(B.el("td", { class: "macierz-zd" }, r.zd.map(function (z) {
        return B.el("span", { class: "mz-zd", title: B.dataPL(B.idxIso(z.od)) + ": " + z.tytul, text: z.krotko || z.tytul });
      })));
      tb.appendChild(tr);
    });
    t.appendChild(tb);
  }
  // przełącznik rozdzielczości mapy jako widoczne przyciski
  function filtryMacierzy() {
    var B = b(), f = B.wyczysc(B.$("ko-macierz-filtry"));
    var g = B.el("div", { class: "przelacznik", role: "group", "aria-label": "Kohorty w mapie" });
    [["mies", "miesięczne"], ["tydz", "tygodniowe"], ["dzien", "dzienne"]].forEach(function (o) {
      var p = B.el("button", { type: "button", "aria-pressed": String(KS.gran === o[0]), text: o[1] });
      p.onclick = function () {
        KS.gran = o[0];
        Array.prototype.forEach.call(g.querySelectorAll("button"), function (x) { x.setAttribute("aria-pressed", String(x === p)); });
        rysujMacierz(); zapiszAdresK();
      };
      g.appendChild(p);
    });
    f.appendChild(B.el("span", { class: "przelacznik-etykieta", text: "Kohorty:" }));
    f.appendChild(g);
    wniosekMacierzy();
  }
  // zdanie z wnioskiem nad mapą: z danych (kohorty.js, klucz macierz), gdy eksport je podaje. Opisuje tylko mapę domyślną
  // (wszyscy nowi pacjenci, bez zawężeń, kohorty miesięczne), więc przy zawężeniu albo innej rozdzielczości jest ukryte.
  function wniosekMacierzy() {
    var B = b(), M = K && K.macierz, w = B.$("ko-macierz-wniosek");
    if (!w) return;
    var domyslna = KS && KS.gran === "mies" && !Object.keys(KS.f).some(function (id) { return KS.f[id]; }) && KS.regula === "Z1K";
    w.textContent = M && M.wniosek ? M.wniosek : "";
    w.hidden = !(M && M.wniosek && domyslna);
  }

  // ---------- krzywa powrotu (okresy nazwane słowami)
  function rysujKrzywa() {
    var B = b(), idx = pacjenciFiltru(), D = 180, xs = [], yA = [], yB = [], nA = [], nB = [], nz = nazwyK();
    for (var d = 1; d <= D; d++) {
      var z = zakresyOkna(d), eA = 0, rA = 0, eB = 0, rB = 0;
      xs.push(d);
      if (!z) { yA.push(null); yB.push(null); nA.push(0); nB.push(0); continue; }
      for (var j = 0; j < idx.length; j++) {
        var i = idx[j], x = K.d[i], ok = K.r[i] >= 0 && K.r[i] <= d;
        if (x >= z.a[0] && x <= z.a[1]) { eA++; if (ok) rA++; }
        if (x >= z.b[0] && x <= z.b[1]) { eB++; if (ok) rB++; }
      }
      yA.push(eA ? 100 * rA / eA : null); yB.push(eB ? 100 * rB / eB : null); nA.push(eA); nB.push(eB);
    }
    var cel = B.wyczysc(B.$("ko-krzywa")), m = B.css("--muted"), g = B.css("--grid");
    var mx = Math.max.apply(null, yA.concat(yB).filter(function (v) { return v !== null; }).concat([1]));
    var dW = 30, dP = 0;
    for (var q = D; q >= 1; q--) if (nB[q - 1] > 0) { dP = q; break; }
    B.$("ko-krzywa-opis").textContent = dP && nB[dW - 1] ? "Każdy punkt krzywej liczymy z innych pacjentów: dzień N bierze tylko kohorty, " +
      "które ten dzień już osiągnęły. W okresie „" + nz.b + "” dzień " + dW + " to " + B.liczba(nB[dW - 1]) + " pacjentów, a dzień " + dP + " już tylko " +
      B.liczba(nB[dP - 1]) + ", z najstarszych kohort. Wyższe wartości późnych dni nie znaczą więc, że młodsze kohorty nadrabiają." : "";
    if (wykresKrz) wykresKrz.destroy();
    var daty = KS.preset === "wlasne" ? null : [" (" + B.dataPL(KS.a[0]) + "–" + B.dataPL(KS.a[1]) + ")", " (" + B.dataPL(KS.b[0]) + "–" + B.dataPL(KS.b[1]) + ")"];
    var naA = wielka(nz.a) + (daty ? daty[0] : ""), naB = wielka(nz.b) + (daty ? daty[1] : "");
    var wartB = function (v, di) { return B.proc(v) + " z " + B.liczba(nB[di]) + (yA[di] ? ", " + B.liczba(100 * v / yA[di], 0) + "% poziomu " + nz.z : ""); };
    var optsK = {
      width: cel.clientWidth || 300, height: 300,
      scales: { x: { time: false }, y: { range: [0, mx * 1.1] } },
      axes: [{ stroke: m, grid: { stroke: g, width: 1 }, ticks: { stroke: g, width: 1, size: 4 }, font: "12px system-ui",
        label: "dni od pierwszego zakupu", labelFont: "12px system-ui", values: function (u, sp) { return sp.map(function (v) { return v; }); } },
      { stroke: m, grid: { stroke: g, width: 1 }, ticks: { stroke: g, width: 1, size: 4 }, font: "12px system-ui", size: 56,
        values: function (u, sp) { return sp.map(function (v) { return B.liczba(v, 0) + "%"; }); } }],
      series: [{ label: "Dzień", value: function (u, v) { return v == null ? "—" : v + ". dzień"; } },
        { label: naA, stroke: B.css("--seria-a"), width: 2,
          value: function (u, v, si, di) { return v == null ? "—" : B.proc(v) + " z " + B.liczba(nA[di]); } },
        { label: naB, stroke: B.css("--seria-b"), width: 2.5, value: function (u, v, si, di) { return v == null ? "—" : wartB(v, di); } }],
      cursor: { drag: { x: true, y: false } }
    };
    var dorysuj = B.legendaUplot(optsK, cel, { id: "krzywa", koncowe: true, etykietaX: function (v) { return v + ". dzień od pierwszego zakupu"; },
      serie: [{ label: wielka(nz.a), kolor: B.css("--seria-a"), wart: function (v, di) { return B.proc(v) + " z " + B.liczba(nA[di]); } },
        { label: wielka(nz.b), kolor: B.css("--seria-b"), gruba: true, wart: wartB }] });
    wykresKrz = new uPlot(optsK, [xs, yA, yB], cel);
    dorysuj();
  }

  // ---------- liczenie grup: na dzień pierwszego zakupu, z sumą kwadratów marży (przedział zmiany średniej)
  function agregujK() {
    var N = b().NDNI, okna = K.okna, ile = okna.length, filtry = filtryAktywne();
    var podz = KS.podz ? kodyWym(KS.podz) : null, wartP = KS.podz ? wartosciWym(KS.podz) : [];
    var grupy = {}, razem = nowaGrupa();
    function nowaGrupa() {
      var g = { cnt: new Float64Array(N), ret: [], mar: [], mar2: [] };
      for (var k = 0; k < ile; k++) { g.ret.push(new Float64Array(N)); g.mar.push(new Float64Array(N)); g.mar2.push(new Float64Array(N)); }
      return g;
    }
    var marze = okna.map(function (n) { return K["m" + n]; });
    for (var i = 0; i < K.n; i++) {
      var ok = true;
      for (var f = 0; f < filtry.length; f++) if (filtry[f].kody[i] !== filtry[f].idx) { ok = false; break; }
      if (!ok) continue;
      var d = K.d[i], r = K.r[i], cele = [razem];
      if (podz) { var w = wartP[podz[i]]; if (!grupy[w]) grupy[w] = nowaGrupa(); cele.push(grupy[w]); }
      for (var c = 0; c < cele.length; c++) {
        var g = cele[c];
        g.cnt[d] += 1;
        for (var k = 0; k < ile; k++) {
          if (r >= 0 && r <= okna[k]) g.ret[k][d] += 1;
          var mm = marze[k][i] / 10;
          g.mar[k][d] += mm; g.mar2[k][d] += mm * mm;
        }
      }
    }
    grupy.__razem = razem;
    return grupy;
  }
  function statyK(g, wszyscy) {
    var BK = b().BK, s = { nA: suma(g.cnt, KS.a), nB: suma(g.cnt, KS.b), wA: suma(wszyscy.cnt, KS.a), wB: suma(wszyscy.cnt, KS.b),
      dA: KS.a[1] - KS.a[0] + 1, dB: KS.b[1] - KS.b[0] + 1, okna: [] };
    K.okna.forEach(function (n, k) {
      var z = zakresyOkna(n);
      if (!z) { s.okna.push(null); return; }
      var eA = suma(g.cnt, z.a), eB = suma(g.cnt, z.b), rA = suma(g.ret[k], z.a), rB = suma(g.ret[k], z.b);
      var sA = suma(g.mar[k], z.a), sB = suma(g.mar[k], z.b), qA = suma(g.mar2[k], z.a), qB = suma(g.mar2[k], z.b);
      s.okna.push({ n: n, z: z, eA: eA, eB: eB, pA: eA ? 100 * rA / eA : null, pB: eB ? 100 * rB / eB : null,
        mA: eA ? sA / eA : null, mB: eB ? sB / eB : null,
        ist: BK.roznicaOdsetkow(rA, eA, rB, eB), istM: BK.roznicaSrednich(sA, qA, eA, sB, qB, eB) });
    });
    s.istN = BK.roznicaTempa(s.nA, s.dA, s.nB, s.dB);
    s.istU = BK.roznicaOdsetkow(s.nA, s.wA, s.nB, s.wB);
    return s;
  }
  // wartość miary w obu okresach i zmiana z przedziałem (tabela grup, zdanie o zdarzeniu); n = okno w dniach
  function miaraK(s, miara, n) {
    var B = b();
    if (miara === "powrot" || miara === "marza") {
      var o = s.okna[K.okna.indexOf(n)];
      if (!o || (!o.eA && !o.eB)) return null;
      // grupa, której w jednym okresie nie było (np. nowe kampanie rok wcześniej): wartość tylko tam, gdzie są pacjenci
      var pr = miara === "powrot", A = pr ? o.pA : o.mA, Bv = pr ? o.pB : o.mB, oba = !!(o.eA && o.eB);
      var f = function (v) { return v === null ? "—" : pr ? B.proc(v) : B.liczba(v, 1) + " zł"; };
      var fz = function (v) { return B.znak(v, 1) + (pr ? " pkt proc." : " zł"); };
      return { tA: f(A), tB: f(Bv), nA: o.eA, nB: o.eB, r: oba ? (pr ? o.ist : o.istM) : null, d: oba ? Bv - A : null, ocena: true,
        tekst: oba ? fz(Bv - A) : "—", fz: fz, z: o.z };
    }
    if (miara === "nowi") {
      var tA = s.nA / s.dA, tB = s.nB / s.dB;
      return { tA: B.liczba(tA, 1), tB: B.liczba(tB, 1), nA: s.nA, nB: s.nB, r: s.istN, d: tB - tA, ocena: false,
        tekst: tA ? B.znak(100 * (tB / tA - 1), 0) + "%" : "—",
        fz: function (v) { return B.znak(v, 1) + " pacjenta dziennie"; } };
    }
    if (!s.wA || !s.wB) return null;
    var uA = 100 * s.nA / s.wA, uB = 100 * s.nB / s.wB;
    return { tA: B.proc(uA), tB: B.proc(uB), nA: s.nA, nB: s.nB, r: s.istU, d: uB - uA, ocena: false,
      tekst: B.znak(uB - uA, 1) + " pkt proc.", fz: function (v) { return B.znak(v, 1) + " pkt proc."; } };
  }
  function etykietaK(m) {
    if (!m || !m.r) return null;
    return { tekst: m.tekst, kierunek: b().BK.kierunekZnaku(m.d), wyrazna: m.r.wyrazna, stan: !m.ocena ? "wyrazna" : m.d > 0 ? "dobrze" : "zle",
      tytul: (m.r.wyrazna ? "Zmiana większa niż przypadek" : "Bez wyraźnej zmiany") + ". 95% przedział zmiany: od " + m.fz(m.r.od) +
        " do " + m.fz(m.r.do) + "." };
  }
  function opisMiaryK(n) {
    return KS.miara === "powrot" ? "powrót w " + n + " dniach" : KS.miara === "marza" ? "marża na pacjenta w " + n + " dniach" :
      KS.miara === "nowi" ? "nowi pacjenci dziennie" : "udział w nowych pacjentach";
  }
  function oknaDotycza() { return KS.miara === "powrot" || KS.miara === "marza"; }

  // ---------- rysowanie całości
  function listaGrupK(grupy) {
    var wszyscy = grupy.__razem;
    return Object.keys(grupy).filter(function (w) { return w !== "__razem"; }).map(function (w) {
      return { w: w, g: grupy[w], s: statyK(grupy[w], wszyscy) };
    }).filter(function (x) { return x.s.nA + x.s.nB > 0; }).sort(function (x, y) { return y.s.nB - x.s.nB || y.s.nA - x.s.nA; });
  }
  // co (bez argumentów): wszystko; „wykres”: wykres i zdarzenia; „karta”: wykres, zdarzenia i tabela grup
  function rysujK(co) {
    var grupy = agregujK(), lista = listaGrupK(grupy);
    KS.wybraneDomyslne = ["__razem"].concat(lista.slice(0, KS.podz ? 4 : 0).map(function (x) { return x.w; }));
    if (!KS.wybrane) KS.wybrane = KS.wybraneDomyslne.slice();
    KS.wybrane = KS.wybrane.filter(function (w) { return w === "__razem" || grupy[w]; });
    przydziel(KS);
    if (co !== "wykres") tabelaK(lista, grupy);
    wykresKoh(grupy);
    panelZdarzenK(grupy);
    if (!co) { pasekK(); rysujMacierz(); rysujKrzywa(); }
    zalezyK();
    zapiszAdresK();
  }

  // ---------- karta „dzień po dniu”: sterowanie w nagłówku
  function sterowanieK() {
    var B = b(), box = B.wyczysc(B.$("ko-sterowanie"));
    box.appendChild(wybor("ko-miara", "Miara", MIARY_K, KS.miara, function (v) { KS.miara = v; sterowanieK(); rysujK("karta"); }));
    if (oknaDotycza()) box.appendChild(wybor("ko-okno", "Okno", K.okna.map(function (n) { return [String(n), n + " dni od pierwszego zakupu"]; }),
      String(KS.okno), function (v) { KS.okno = +v; rysujK("karta"); }));
    box.appendChild(wybor("ko-wygl", "Wygładzenie", [["1", "bez wygładzenia (dzień)"], ["7", "suma z 7 dni"], ["28", "suma z 28 dni"]],
      String(KS.wygl), function (v) { KS.wygl = +v; rysujK("wykres"); }));
    box.appendChild(wybor("ko-podz", "Podział na grupy", [["", "bez podziału"]].concat(WYMIARY.map(function (w) { return [w.id, w.nazwa]; })),
      KS.podz, function (v) { KS.podz = v; KS.wybrane = null; KS.kolory = {}; rysujK("karta"); }));
    var pr = B.el("select", { id: "ko-preset" });
    opcjePresetow(pr);
    pr.value = KS.preset;
    pr.onchange = function () { if (this.value !== "wlasne") okresyPreset(this.value, KS); else KS.preset = "wlasne"; sterowanieK(); rysujK(); };
    box.appendChild(B.el("label", null, ["Porównanie", pr]));
    if (KS.preset === "wlasne") box.appendChild(datyAB("ko", KS, function () { sterowanieK(); rysujK(); }));
  }
  // kolor idzie za grupą, nie za kolejnością zaznaczenia: miejsce w palecie według stałej kolejności wartości wymiaru;
  // „Wszyscy wybrani pacjenci” to seria odniesienia w kolorze tuszu; nowe kampanie na L4 zawsze pomarańczowe, pozostałe niebieskie
  var KOLOR_GRUPY = { nowe: "--series-2", pozostale: "--series-1" };
  function przydziel(S) {
    var wart = S.podz ? wartosciWym(S.podz) : [], zajete = {};
    S.kolory = {};
    S.wybrane.slice().sort(function (a, c) { return wart.indexOf(a) - wart.indexOf(c); }).forEach(function (w) {
      if (w === "__razem") { S.kolory[w] = "--seria-ref"; return; }
      if (S.podz === "grupa" && KOLOR_GRUPY[w]) { S.kolory[w] = KOLOR_GRUPY[w]; return; }
      var start = Math.max(0, wart.indexOf(w)) % 8;
      for (var k = 0; k < 8; k++) { var i = (start + k) % 8 + 1; if (!zajete[i]) { S.kolory[w] = "--series-" + i; zajete[i] = true; return; } }
      S.kolory[w] = "--seria-ref";
    });
  }
  function wykresKoh(grupy) {
    var B = b(), w = KS.wygl, N = B.NDNI, k = K.okna.indexOf(KS.okno), n = KS.okno, ost = N - 1 - n, nz = nazwyK();
    var naz = MIARY_K.filter(function (m) { return m[0] === KS.miara; })[0][1];
    B.$("ko-wykres-tytul").textContent = "Dzień po dniu: " + naz.charAt(0).toLowerCase() + naz.slice(1) + (oknaDotycza() ? " (" + n + " dni)" : "") +
      " według dnia pierwszego zakupu, " + (w === 1 ? "bez wygładzenia" : "suma z " + w + " dni");
    var cWsz = krocz(grupy.__razem.cnt, w);
    var serie = KS.wybrane.map(function (wart) {
      var g = grupy[wart], y = new Array(N), c = krocz(g.cnt, w), mian = c, i;
      if (oknaDotycza()) {
        var l = krocz(KS.miara === "powrot" ? g.ret[k] : g.mar[k], w);
        for (i = 0; i < N; i++) y[i] = i >= w - 1 && i <= ost && c[i] > 0 ? (KS.miara === "powrot" ? 100 : 1) * l[i] / c[i] : null;
      } else if (KS.miara === "nowi") {
        for (i = 0; i < N; i++) y[i] = i >= w - 1 ? c[i] / w : null;
        mian = null;
      } else {
        for (i = 0; i < N; i++) y[i] = i >= w - 1 && cWsz[i] > 0 ? 100 * c[i] / cWsz[i] : null;
        mian = cWsz;
      }
      return { label: etykietaWart(KS.podz, wart), kolor: B.css(KS.kolory[wart] || "--seria-ref"), y: y, w: wart, szer: wart === "__razem" ? 2.5 : 1.75,
        opis: function (di, v) {
          if (KS.miara === "nowi") return B.liczba(v, 1) + " dziennie";
          if (KS.miara === "marza") return B.liczba(v, 1) + " zł na pacjenta z " + B.liczba(mian[di]);
          return B.proc(v) + " z " + B.liczba(mian[di]) + (KS.miara === "udzial" ? " wybranych" : "");
        } };
    });
    // seria odniesienia rysowana na końcu, żeby nie chowała się pod seriami podziału
    serie.sort(function (p, q) { return (p.w === "__razem") - (q.w === "__razem"); });
    if (wykresK) wykresK.destroy();
    var proc = KS.miara === "powrot" || KS.miara === "udzial";
    var dost = Object.keys(grupy).filter(function (v) { return v !== "__razem"; }).map(function (v) {
      var t = 0, c_ = grupy[v].cnt; for (var j = 0; j < c_.length; j++) t += c_[j]; return { w: v, n: t };
    }).sort(function (p, q) { return q.n - p.n; }).map(function (p) { return [p.w, etykietaWart(KS.podz, p.w)]; });
    wykresK = wykres(B.$("ko-wykres"), serie, { procent: proc, jednostka: proc ? "%" : KS.miara === "marza" ? "zł" : "pacjenci",
      formatY: function (v) { return B.liczba(v, 0) + (proc ? "%" : ""); }, a: KS.a, b: KS.b, nazwy: { a: nz.a, b: nz.b },
      listaZd: zdarzeniaWykresuK(), id: "kohorty", odswiez: function () { rysujK("wykres"); },
      wybor: { dostepne: [["__razem", "Wszyscy wybrani pacjenci"]].concat(dost), wybrane: KS.wybrane, max: 8,
        dodaj: function (v) { KS.wybrane.push(v); rysujK("karta"); },
        usun: function (v) { KS.wybrane = KS.wybrane.filter(function (q) { return q !== v; }); rysujK("karta"); } } });
  }

  // ---------- zdarzenia pod wykresem: przyciski ustawiają porównanie 60 dni przed i po, zdanie mówi, co się zmieniło
  function zdanieZdarzenia(z, grupy, lista) {
    var B = b(), BK = B.BK, naz = "„" + (z.krotko || z.tytul) + "” (" + B.dataPL(B.idxIso(z.od)) + ")";
    var s = statyK(grupy.__razem, grupy.__razem), m = miaraK(s, KS.miara, KS.okno), co = opisMiaryK(KS.okno);
    if (KS.miara === "udzial") {
      if (!KS.podz) return naz + ": udział w nowych pacjentach ma sens z podziałem na grupy; wybierz podział w nagłówku karty.";
      var naj = null;
      lista.forEach(function (x) {
        var mm = miaraK(x.s, "udzial", KS.okno);
        if (mm && mm.r && (!naj || Math.abs(mm.d) > Math.abs(naj.m.d))) naj = { x: x, m: mm };
      });
      if (!naj) return "";
      return naz + ": najbardziej zmienił się udział grupy „" + etykietaWart(KS.podz, naj.x.w) + "”, z " + naj.m.tA + " w 60 dniach przed do " +
        naj.m.tB + " w 60 dniach po, czyli " + naj.m.tekst + ", " + (naj.m.r.wyrazna ? "więcej niż przypadek." : "bez wyraźnej zmiany.");
    }
    if (!m || !m.r) return naz + ": po tym zdarzeniu żadna kohorta nie ma jeszcze pełnego okna " + KS.okno + " dni; wybierz krótsze okno.";
    var dl = m.z ? m.z.b[1] - m.z.b[0] + 1 : 60, okr = dl < 60 ? dl + " dniach" : "60 dniach";
    var t = naz + ": " + co + " wszystkich wybranych pacjentów to " + m.tA + " w " + okr + " przed i " + m.tB + " w " + okr + " po (" +
      B.liczba(m.nA) + " i " + B.liczba(m.nB) + " pacjentów), czyli " + m.tekst + ", " + (m.r && m.r.wyrazna ? "więcej niż przypadek" : "bez wyraźnej zmiany");
    if (dl < 60) t += "; po zdarzeniu tylko " + dl + " dni kohort ma już pełne okno";
    if (KS.podz && lista.length) {
      var wyr = lista.filter(function (x) { var mm = miaraK(x.s, KS.miara, KS.okno); return mm && mm.r && mm.r.wyrazna; }).length;
      t += "; wyraźna zmiana w " + wyr + " z " + lista.length + " grup w tabeli niżej";
    }
    return t + ".";
  }
  function panelZdarzenK(grupy) {
    var B = b(), cel = B.wyczysc(B.$("ko-zd")), lista = zdarzeniaWykresuK();
    cel.appendChild(B.el("p", { class: "zd-panel-tytul", text: "Co zmieniło się po zdarzeniu: przycisk ustawia porównanie 60 dni przed i 60 dni po" }));
    var box = B.el("div", { class: "zd-przyciski", role: "group", "aria-label": "Zdarzenia: porównanie 60 dni przed i po" });
    lista.forEach(function (z) {
      var akt = KS.preset === "zd:" + z.id;
      var p = B.el("button", { type: "button", class: "zd-przycisk", "aria-pressed": String(akt), title: z.tytul }, [
        B.el("span", { class: "zd-nr", text: String(z.nr) }), B.el("span", { class: "zd-data", text: B.dataPL(B.idxIso(z.od)) }),
        B.el("span", { class: "zd-naz", text: z.krotko || z.tytul })]);
      p.onclick = function () { okresyPreset(akt ? "rok" : "zd:" + z.id, KS); sterowanieK(); rysujK(); };
      box.appendChild(p);
    });
    cel.appendChild(box);
    var nSk = zdarzeniaKohort().filter(function (z) { return OBSZARY_PRZYCZYN.indexOf(z.obszar) < 0; }).length;
    var chk = B.el("input", { type: "checkbox" });
    chk.checked = !!KS.skutki;
    chk.onchange = function () { KS.skutki = this.checked; rysujK("wykres"); };
    cel.appendChild(B.el("label", { class: "chip zd-skutki" }, [chk, "Pokaż też zmiany wykryte w samych kohortach (" + nSk + ")"]));
    var zd = KS.preset.indexOf("zd:") === 0 ? zdarzeniaKohort().filter(function (z) { return "zd:" + z.id === KS.preset; })[0] : null;
    if (zd) {
      var zdanie = zdanieZdarzenia(zd, grupy, listaGrupK(grupy));
      cel.appendChild(B.el("p", { class: "zd-wynik", "aria-live": "polite" }, [zdanie + " ",
        B.el("a", { href: "#zdarzenia?z=" + zd.id, text: "Opis zdarzenia" })]));
    }
    cel.appendChild(B.el("p", { class: "przypis" }, ["Skutek każdego zdarzenia w złotych, pewność i co robimy: ",
      B.el("a", { href: "#zdarzenia", text: "tabela „Co zmieniło kohorty i wynik” w zakładce „Zdarzenia”" }), "."]));
  }

  // ---------- tabela grup: jedna miara naraz (ta sama co na wykresie) albo wszystkie okna; kolor tylko przy wyraźnej zmianie
  function tabelaK(lista, grupy) {
    var B = b(), BK = B.BK, nz = nazwyK(), wsz = KS.tryb === "wszystkie" && oknaDotycza();
    var podzNaz = KS.podz ? WYMIARY.filter(function (w) { return w.id === KS.podz; })[0].nazwa : "Pacjenci";
    function wiersz(w, g) {
      var s = statyK(g, grupy.__razem), wybrany = KS.wybrane.indexOf(w) >= 0;
      var r = { nazwa: etykietaWart(KS.podz, w), podsuma: w === "__razem",
        wybor: { zaznaczony: wybrany, kolor: wybrany && KS.kolory[w] ? B.css(KS.kolory[w]) : null, zmien: function (czy, chk) {
          if (czy) { if (KS.wybrane.length >= 8) { chk.checked = false; return; } KS.wybrane.push(w); }
          else KS.wybrane = KS.wybrane.filter(function (x) { return x !== w; });
          rysujK("karta");
        } } };
      if (wsz) {
        r.n = B.liczba(s.nA) + " → " + B.liczba(s.nB);
        r.nTytul = "Nowi pacjenci w całych okresach: " + nz.a + " " + B.liczba(s.nA) + ", " + nz.b + " " + B.liczba(s.nB) + ".";
        r.mala = Math.min(s.nA, s.nB) > 0 && Math.min(s.nA, s.nB) < BK.MALA_GRUPA;
        r.komorki = K.okna.map(function (n) {
          var m = miaraK(s, KS.miara, n), e = etykietaK(m);
          if (!e) return null;
          return { zm: e, tytul: wielka(nz.a) + ": " + m.tA + " z " + B.liczba(m.nA) + " pacjentów. " + wielka(nz.b) + ": " + m.tB + " z " +
            B.liczba(m.nB) + " pacjentów. " + e.tytul };
        });
      } else {
        var m = miaraK(s, KS.miara, KS.okno);
        r.n = m ? B.liczba(m.nA) + " → " + B.liczba(m.nB) : "—";
        r.mala = !!m && Math.min(m.nA, m.nB) > 0 && Math.min(m.nA, m.nB) < BK.MALA_GRUPA;
        r.wA = m ? m.tA : "—"; r.wB = m ? m.tB : "—"; r.zm = etykietaK(m);
      }
      return r;
    }
    var wiersze = [wiersz("__razem", grupy.__razem)].concat(KS.podz ? lista.map(function (x) { return wiersz(x.w, x.g); }) : []);
    BK.tabelaGrup(B.$("ko-tabela"), { podzial: podzNaz, nazwaN: "Pacjenci: " + nz.a + " → " + nz.b, nazwaA: wielka(nz.a),
      nazwaB: wielka(nz.b), tryb: wsz ? "wszystkie" : "miara", jednostka: "pacjentów",
      kolumny: K.okna.map(function (n) { return n + " dni"; }), wiersze: wiersze });
    // tytuł, przełącznik trybu i opis okresów
    var naz = opisMiaryK(KS.okno);
    B.$("ko-tabela-tytul").textContent = "Grupy: " + (wsz ? (KS.miara === "powrot" ? "powrót" : "marża na pacjenta") + " we wszystkich oknach" : naz) +
      (KS.podz ? ", podział: " + podzNaz.charAt(0).toLowerCase() + podzNaz.slice(1) : "");
    var pf = B.wyczysc(B.$("ko-tabela-tryb"));
    if (oknaDotycza()) {
      var g = B.el("div", { class: "przelacznik", role: "group", "aria-label": "Tabela grup" });
      [["miara", "okno " + KS.okno + " dni"], ["wszystkie", "wszystkie okna"]].forEach(function (o) {
        var p = B.el("button", { type: "button", "aria-pressed": String((wsz ? "wszystkie" : "miara") === o[0]), text: o[1] });
        p.onclick = function () { KS.tryb = o[0]; rysujK("karta"); };
        g.appendChild(p);
      });
      pf.appendChild(B.el("span", { class: "przelacznik-etykieta", text: "Tabela:" }));
      pf.appendChild(g);
    }
    var opis;
    if (wsz) opis = "W komórce zmiana; wartości i liczba pacjentów po najechaniu. Każde okno bierze tylko kohorty z pełnym oknem, więc dłuższe okna mają mniej kohort.";
    else if (oknaDotycza()) {
      var z = zakresyOkna(KS.okno);
      // przy własnych datach nazwy okresów to same daty, więc w opisie słowa „wcześniejszy” i „późniejszy”
      var na = KS.preset === "wlasne" ? "wcześniejszy okres" : nz.a, nb = KS.preset === "wlasne" ? "późniejszy okres" : nz.b;
      opis = z ? "Kohorty z pełnym oknem " + KS.okno + " dni: " + na + " " + B.dataPL(z.a[0]) + "–" + B.dataPL(z.a[1]) + ", " + nb + " " +
        B.dataPL(z.b[0]) + "–" + B.dataPL(z.b[1]) + "." : "W wybranym okresie żadna kohorta nie ma jeszcze pełnego okna " + KS.okno + " dni.";
    } else opis = (KS.preset === "wlasne" ? "Wcześniejszy okres" : wielka(nz.a)) + ": " + B.dataPL(KS.a[0]) + "–" + B.dataPL(KS.a[1]) + " (" +
      (KS.a[1] - KS.a[0] + 1) + " dni), " + (KS.preset === "wlasne" ? "późniejszy okres" : nz.b) + ": " +
      B.dataPL(KS.b[0]) + "–" + B.dataPL(KS.b[1]) + " (" + (KS.b[1] - KS.b[0] + 1) + " dni)." +
      (KS.miara === "nowi" ? " Zmiana w procentach liczby nowych pacjentów dziennie." : "");
    B.$("ko-okresy-opis").textContent = opis + " Zaznaczone wiersze są na wykresie wyżej.";
    BK.legendaIstotnosci(B.$("ko-legenda-zmian"), { ocena: oknaDotycza(), jednostka: "pacjentów" });
  }

  BW.kohorty = {
    pokaz: function (q) {
      var B = b();
      if (!gotoweK) B.akapity(B.$("ko-zdania"), ["Wczytywanie danych kohort…"]);
      B.wczytaj("kohorty", "kohorty").then(function (dane) {
        if (!K) { K = dane; przygotujK(); }
        if (!gotoweK) {
          B.zdaniaAlboKarta(B.$("ko-naglowek"), B.$("ko-zdania"), K.karta, K.zdania);
          // obraz liczby z wniosku: powrót w czterech oknach, rok wcześniej → ostatnie 12 miesięcy
          if (BW.hantleRetencji) B.BK.wstawWykres(B.$("ko-naglowek"), BW.hantleRetencji());
          gotoweK = true;
        }
        czytajAdresK(q);
        sterowanieK();
        filtryMacierzy();
        rysujK();
        // odnośnik z ustawieniami (np. z tabeli zdarzeń) przewija do wykresu dzień po dniu; sama zakładka otwiera się na górze
        if (q && Array.from(q.keys()).length) setTimeout(function () {
          B.$("ko-wykres-karta").scrollIntoView({ behavior: "smooth", block: "start" });
        }, 60);
      }).catch(function (e) { B.akapity(B.$("ko-zdania"), [e.message + ". Odśwież stronę."]); });
    },
    przerysuj: function () { if (K && KS) { rysujK("wykres"); rysujKrzywa(); przyklej(); } }
  };

  // ------------------------------------------------------------ PO ZAKUPIE
  var PZ = null, PS = { spec: "internista", grupa: "pozostale", prog: "p15", wygl: 28,
    zwGrupa: "wszyscy", zwZam: "wszystkie", zwWygl: 28, ocSpec: "internista", ocGrupa: "pozostale",
    opWizyta: "internista_rano", opGrupa: "pozostale", wyrozPora: "a_rano_6_11", wyrozCel: "l4" };
  var wykresP = null, wykresZ = null, gotoweP = false;
  // w „Po zakupie” i „Wyniku biznesu” nie wybiera się dat, więc porównanie nazywamy słowami, a nie literami A i B
  var RR = { pref: "rok wcześniej: ", wobec: "wobec roku wcześniej" };
  var PORY = ["a_rano_6_11", "b_poludnie_12_15", "c_wieczor_16_23", "d_noc_0_5"];
  var CELE = ["l4", "e_recepta", "konsultacja", "skierowanie"];
  var KOSZYKI = ["a_do_5_min", "b_5_15_min", "c_15_30_min", "d_ponad_30_min", "brak_wizyty"];

  function zdarzeniaPZ() {
    return b().zdarzeniaNumerowane().filter(function (z) { return z.obszar === "obsluga" || /^start/.test(String(z.rodzaj)); });
  }
  function zsumuj(lista, warunek, pola) {
    var N = b().NDNI, out = {};
    pola.forEach(function (p) { out[p] = new Float64Array(N); });
    lista.forEach(function (s) {
      if (!warunek(s)) return;
      pola.forEach(function (p) { var a = s[p]; if (a) for (var i = 0; i < N; i++) out[p][i] += a[i]; });
    });
    return out;
  }
  function grupaOk(g, nowa) { return g === "wszyscy" || (g === "nowe" ? nowa : !nowa); }
  function zakresOkresu(o) { var B = b(), O = B.O[o - 1]; return [B.idxIso(O.od), B.idxIso(O.do)]; }

  function rysujPunktualnosc() {
    var B = b(), ET = B.ET, w = PS.wygl;
    var serie = PORY.map(function (pora, i) {
      var s = zsumuj(PZ.punktualnosc, function (x) { return x.pora === pora && (PS.spec === "wszyscy" || x.spec === PS.spec) && grupaOk(PS.grupa, x.nowa); }, ["n", PS.prog]);
      var m = krocz(s.n, w), l = krocz(s[PS.prog], w), y = new Array(B.NDNI);
      for (var d = 0; d < B.NDNI; d++) y[d] = d >= w - 1 && m[d] > 0 ? 100 * l[d] / m[d] : null;
      var wyr = pora === PS.wyrozPora;
      return { label: ET.pora[pora], kolor: B.css(wyr ? "--series-1" : "--seria-a"), szer: wyr ? 2.5 : 1.25, y: y,
        opis: function (di, v) { return B.proc(v) + " z " + B.liczba(m[di]) + " wizyt"; } };
    });
    if (wykresP) wykresP.destroy();
    wykresP = wykres(B.$("pz-wykres"), serie, { procent: true, jednostka: "%", listaZd: zdarzeniaPZ(), listaPod: true, a: zakresOkresu(1), b: zakresOkresu(2), nazwy: B.nazwyPresetu("rok"),
      id: "punktualnosc", odswiez: rysujPunktualnosc });
    // tabela: specjalizacja × pora, okres 1 wobec okresu 2
    var t = B.wyczysc(B.$("pz-tabela")), o1 = zakresOkresu(1), o2 = zakresOkresu(2);
    t.appendChild(B.el("thead", null, [B.el("tr", null, [B.el("th", { text: "Specjalizacja" }), B.el("th", { text: "Pora terminu" }),
      B.el("th", { text: "Spóźnione " + (PS.prog === "p15" ? "ponad 15" : "ponad 30") + " minut: ostatnie 12 miesięcy (" + B.O[1].nazwa + "), pod spodem rok wcześniej" })])]));
    var tb = B.el("tbody");
    var specy = ["internista", "pediatra", "psychiatra", "inny"].filter(function (sp) { return PS.wszystkieSpec || PS.spec === "wszyscy" || sp === PS.spec; });
    specy.forEach(function (sp) {
      PORY.forEach(function (pora) {
        var s = zsumuj(PZ.punktualnosc, function (x) { return x.pora === pora && x.spec === sp && grupaOk(PS.grupa, x.nowa); }, ["n", PS.prog]);
        var nA = suma(s.n, o1), nB = suma(s.n, o2);
        if (nA + nB === 0) return;
        tb.appendChild(B.el("tr", sp === PS.spec && specy.length > 1 ? { class: "zaznaczony", style: "--kolor:" + B.css("--accent") } : null,
          [B.el("td", { text: ET.spec[sp] }), B.el("td", { text: ET.pora[pora] }),
            komorka(nB ? 100 * suma(s[PS.prog], o2) / nB : null, nB, nA ? 100 * suma(s[PS.prog], o1) / nA : null, nA, "%", 1, true, RR)]));
      });
    });
    t.appendChild(tb);
    legendaPod(t, { ocena: true, jednostka: "wizyt", bezMalych: true });
    // przycisk: wszystkie specjalizacje albo tylko wybrana (domyślnie tabela idzie za wyborem specjalizacji, jak wykres)
    var r = t.closest(".tabela-ramka"), p = r.previousElementSibling;
    if (!p || !p.classList.contains("pz-spec-przycisk")) { p = B.el("p", { class: "pz-spec-przycisk" }); r.parentNode.insertBefore(p, r); }
    B.wyczysc(p);
    if (PS.spec !== "wszyscy") {
      var btn = B.el("button", { type: "button", class: "przycisk-maly", text: PS.wszystkieSpec ? "Pokaż tylko wybraną specjalizację" : "Pokaż wszystkie specjalizacje (16 wierszy)" });
      btn.onclick = function () { PS.wszystkieSpec = !PS.wszystkieSpec; rysujPunktualnosc(); };
      p.appendChild(btn);
    }
  }

  var RUCH_GRUPA = "wszyscy";
  // forma „wizyta / wizyty / wizyt” po przedziale ruchu: idzie za ostatnią liczbą („21–24 wizyty”, „25–28 wizyt”);
  // po „do 8” i „41 i więcej” zawsze „wizyt”
  function wizytPrzedzialu(pz) {
    var m = /(\d+)$/.exec(pz), n = m ? +m[1] : 0;
    if (!m || /^do /.test(pz)) return "wizyt";
    return n === 1 ? "wizyta" : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14) ? "wizyty" : "wizyt";
  }
  function rysujRuch() {
    var B = b(), t = B.wyczysc(B.$("pz-ruch")), stare = RUCH_GRUPA === "pozostale", hw = [];
    var przedz = [];
    PZ.ruch.forEach(function (r) { if (przedz.indexOf(r.przedzial) < 0) przedz.push(r.przedzial); });
    t.appendChild(B.el("thead", null, [B.el("tr", null, [B.el("th", { text: "Poranne wizyty u internisty w dniu" }),
      B.el("th", { text: "Spóźnione ponad 15 minut: ostatnie 12 miesięcy (" + B.O[1].nazwa + "), pod spodem rok wcześniej" }),
      B.el("th", { text: "Dni z takim ruchem" })])]));
    var tb = B.el("tbody");
    przedz.forEach(function (pz) {
      var o = {};
      PZ.ruch.forEach(function (r) { if (r.przedzial === pz) o[r.okres] = r; });
      var f = function (r) { if (!r) return [null, null]; var od = stare ? r.odbyte_stare : r.odbyte, sp = stare ? r.spoznione_stare : r.spoznione; return [od ? 100 * sp / od : null, od]; };
      var a = f(o[1]), bb = f(o[2]);
      if (a[0] !== null && bb[0] !== null) {
        var d = bb[0] - a[0];
        hw.push({ etykieta: pz + " " + wizytPrzedzialu(pz), a: a[0], b: bb[0], tekstA: B.proc(a[0]), tekstB: B.proc(bb[0]),
          tytul: "Poranne wizyty u internisty w dniach z ruchem " + pz + ": spóźnione ponad 15 minut rok wcześniej " + B.proc(a[0]) + " z " + B.liczba(a[1]) +
            ", ostatnie 12 miesięcy " + B.proc(bb[0]) + " z " + B.liczba(bb[1]),
          zmiana: { tekst: B.znak(d, 1) + " pkt proc.", kierunek: B.BK.kierunekZnaku(d), stan: Math.abs(d) < 0.05 ? "neutralnie" : d > 0 ? "zle" : "dobrze" } });
      }
      tb.appendChild(B.el("tr", null, [B.el("td", { text: pz }), komorka(bb[0], bb[1], a[0], a[1], "%", 1, true, RR),
        B.el("td", null, [B.el("span", { class: "b", text: o[2] ? B.liczba(o[2].dni) : "—" }), B.el("span", { class: "a", text: "rok wcześniej: " + (o[1] ? B.liczba(o[1].dni) : "—") })])]));
    });
    t.appendChild(tb);
    var mx = Math.max.apply(null, hw.map(function (w) { return Math.max(w.a, w.b); }).concat([10]));
    mx = Math.ceil(mx / 10) * 10;
    var hc = B.wyczysc(B.$("pz-ruch-hantle"));
    hc.appendChild(B.BK.hantle({ nazwy: { a: "rok wcześniej", b: "ostatnie 12 miesięcy" }, kodowanie: "okresy", min: 0, max: mx,
      os: [0, mx / 2, mx].map(function (v) { return B.liczba(v, 0) + "%"; }), wiersze: hw,
      opis: "Odsetek porannych wizyt u internisty spóźnionych ponad 15 minut według ruchu porannego w dniu: rok wcześniej i ostatnie 12 miesięcy",
      przypis: "Odsetek porannych wizyt u internisty (6:00–11:59) spóźnionych ponad 15 minut, w dniach z takim samym ruchem porannym." }));
  }

  function rysujPowrotOpoznienie() {
    var B = b(), t = B.wyczysc(B.$("pz-powrot"));
    if (!K) { t.appendChild(B.el("caption", { class: "przypis", text: "Wczytywanie danych kohort…" })); return; }
    var kU = KOD.usluga, kP = KOD.pora, kK = KOD.koszyk, kKamp = KOD.kampania, wU = K.wart.usluga, wP = K.wart.pora,
      wK = K.wart.koszyk, wKamp = K.wart.kampania, nowe = B.ET.nowe_kampanie;
    var n = 90, B1 = B.O[1], ost = B.NDNI - 1 - n;
    var b0 = B.idxIso(B1.od), bk = Math.min(B.idxIso(B1.do), ost), a0 = B.idxIso(B.O[0].od), ak = a0 + (bk - b0);
    var st = {};
    KOSZYKI.forEach(function (k) { st[k] = { eA: 0, rA: 0, eB: 0, rB: 0 }; });
    for (var i = 0; i < K.n; i++) {
      var usl = wU[kU[i]];
      if (PS.opWizyta !== "wszystkie" && usl.indexOf("internista") !== 0) continue;
      if (PS.opWizyta === "internista_rano" && wP[kP[i]] !== "a_rano_6_11") continue;
      var nowa = nowe.indexOf(wKamp[kKamp[i]]) >= 0;
      if (!grupaOk(PS.opGrupa, nowa)) continue;
      var d = K.d[i], wr = K.r[i] >= 0 && K.r[i] <= n, s = st[wK[kK[i]]];
      if (d >= a0 && d <= ak) { s.eA++; if (wr) s.rA++; }
      if (d >= b0 && d <= bk) { s.eB++; if (wr) s.rB++; }
    }
    t.appendChild(B.el("thead", null, [B.el("tr", null, [B.el("th", { text: "Opóźnienie pierwszej wizyty" }),
      B.el("th", { text: "Powrót w 90 dniach: kohorty " + B.dataPL(b0) + "–" + B.dataPL(bk) + ", pod spodem te same dni rok wcześniej (" + B.dataPL(a0) + "–" + B.dataPL(ak) + ")" })])]));
    var tb = B.el("tbody");
    KOSZYKI.forEach(function (k) {
      var s = st[k];
      tb.appendChild(B.el("tr", null, [B.el("td", { text: B.ET.koszyk[k] }),
        komorka(s.eB ? 100 * s.rB / s.eB : null, s.eB, s.eA ? 100 * s.rA / s.eA : null, s.eA, "%", 1, false,
          { pref: RR.pref, wobec: RR.wobec, neutralnie: true })]));
    });
    t.appendChild(tb);
  }

  function rysujZwroty() {
    var B = b(), ET = B.ET, w = PS.zwWygl;
    var warunek = function (cel) {
      return function (x) {
        return (!cel || x.cel === cel) && grupaOk(PS.zwGrupa, x.nowa) &&
          (PS.zwZam === "wszystkie" || (PS.zwZam === "pierwsze" ? x.pierwsze : !x.pierwsze));
      };
    };
    var serie = CELE.map(function (cel, i) {
      var s = zsumuj(PZ.zwroty, warunek(cel), ["odbyte", "zwrocone"]);
      var m = krocz(s.odbyte, w), l = krocz(s.zwrocone, w), y = new Array(B.NDNI);
      for (var d = 0; d < B.NDNI; d++) y[d] = d >= w - 1 && m[d] > 0 ? 100 * l[d] / m[d] : null;
      var wyr = cel === PS.wyrozCel;
      return { label: ET.cel[cel], kolor: B.css(wyr ? "--series-1" : "--seria-a"), szer: wyr ? 2.5 : 1.25, y: y,
        opis: function (di, v) { return B.proc(v) + " z " + B.liczba(m[di]) + " odbytych"; } };
    });
    if (wykresZ) wykresZ.destroy();
    wykresZ = wykres(B.$("zw-wykres"), serie, { procent: true, jednostka: "%", listaZd: zdarzeniaPZ(), listaPod: true, a: zakresOkresu(1), b: zakresOkresu(2), nazwy: B.nazwyPresetu("rok"),
      id: "zwroty", odswiez: rysujZwroty });
    var t = B.wyczysc(B.$("zw-tabela")), o1 = zakresOkresu(1), o2 = zakresOkresu(2);
    t.appendChild(B.el("thead", null, [B.el("tr", null, ["Cel wizyty", "Zwrot po odbytej wizycie", "Anulowane przed wizytą",
      "Pacjent nie odebrał"].map(function (h) { return B.el("th", { text: h }); }))]));
    var tb = B.el("tbody");
    // kwoty w drugiej tabeli w zwiniętej sekcji pod główną
    var r = t.closest(".tabela-ramka"), d = B.$("zw-kwoty");
    if (!d) {
      d = B.el("details", { class: "szczegoly tabela-zwinieta", id: "zw-kwoty" }, [B.el("summary", { text: "Tabela: zwrócone zapłaty i koszt lekarza za zwrócone wizyty" }),
        B.el("div", { class: "tabela-ramka" }, [B.el("table", { class: "tabela tabela-lejek", id: "zw-kwoty-tabela" })])]);
      r.parentNode.insertBefore(d, r.nextSibling);
    }
    var t2 = B.wyczysc(B.$("zw-kwoty-tabela"));
    t2.appendChild(B.el("thead", null, [B.el("tr", null, ["Cel wizyty", "Zwrócone zapłaty", "Koszt lekarza za zwrócone wizyty"].map(function (h) { return B.el("th", { text: h }); }))]));
    var tb2 = B.el("tbody");
    CELE.concat([null]).forEach(function (cel) {
      var s = zsumuj(PZ.zwroty, warunek(cel), ["wszystkie", "anul", "nieodebr", "odbyte", "zwrocone", "zw_zl", "kl_zw"]);
      var f = function (licz, mian) { var a = suma(s[mian], o1), bb = suma(s[mian], o2); return komorka(bb ? 100 * suma(s[licz], o2) / bb : null, bb, a ? 100 * suma(s[licz], o1) / a : null, a, "%", 1, true, RR); };
      var zl = function (p) { return B.el("td", null, [B.el("span", { class: "b", text: B.liczba(suma(s[p], o2)) + " zł" }), B.el("span", { class: "a", text: "rok wcześniej: " + B.liczba(suma(s[p], o1)) + " zł" })]); };
      tb.appendChild(B.el("tr", cel ? null : { class: "podsuma" }, [B.el("td", { text: cel ? ET.cel[cel] : "Razem" }),
        f("zwrocone", "odbyte"), f("anul", "wszystkie"), f("nieodebr", "wszystkie")]));
      tb2.appendChild(B.el("tr", cel ? null : { class: "podsuma" }, [B.el("td", { text: cel ? ET.cel[cel] : "Razem" }), zl("zw_zl"), zl("kl_zw")]));
    });
    t.appendChild(tb);
    t2.appendChild(tb2);
    legendaPod(t, { ocena: true, jednostka: "wizyt", bezMalych: true });
  }

  function rysujOceny() {
    var B = b(), t = B.wyczysc(B.$("oc-tabela"));
    var st = {};
    KOSZYKI.slice(0, 4).forEach(function (k) { st[k] = { 1: { o: 0, oc: 0, s: 0, ni: 0 }, 2: { o: 0, oc: 0, s: 0, ni: 0 } }; });
    PZ.oceny.forEach(function (r) {
      if (!st[r.koszyk] || (PS.ocSpec !== "wszyscy" && r.spec !== PS.ocSpec) || !grupaOk(PS.ocGrupa, r.nowa)) return;
      var x = st[r.koszyk][r.okres];
      x.o += r.odbyte; x.oc += r.ocenione; x.s += r.suma; x.ni += r.niskie;
    });
    t.appendChild(B.el("thead", null, [B.el("tr", null, ["Opóźnienie wizyty", "Odsetek ocenionych", "Średnia ocena (1–5)", "Oceny 1–2"]
      .map(function (h) { return B.el("th", { text: h }); }))]));
    var tb = B.el("tbody");
    Object.keys(st).forEach(function (k) {
      var a = st[k][1], bb = st[k][2];
      tb.appendChild(B.el("tr", null, [B.el("td", { text: B.ET.koszyk[k] }),
        komorka(bb.o ? 100 * bb.oc / bb.o : null, bb.o, a.o ? 100 * a.oc / a.o : null, a.o, "%", 1, false, RR),
        komorka(bb.oc ? bb.s / bb.oc : null, bb.oc, a.oc ? a.s / a.oc : null, a.oc, "", 2, false, RR),
        komorka(bb.oc ? 100 * bb.ni / bb.oc : null, bb.oc, a.oc ? 100 * a.ni / a.oc : null, a.oc, "%", 1, true, RR)]));
    });
    t.appendChild(tb);
  }

  function filtryP() {
    var B = b(), grupy = [["pozostale", "Spoza nowych kampanii"], ["nowe", "Nowe kampanie na L4"], ["wszyscy", "Wszyscy"]];
    var specy = [["internista", "Internista"], ["pediatra", "Pediatra"], ["psychiatra", "Psychiatra"], ["inny", "Inni specjaliści"], ["wszyscy", "Wszyscy"]];
    var f = B.wyczysc(B.$("pz-filtry"));
    f.appendChild(wybor("pz-spec", "Specjalizacja", specy, PS.spec, function (v) { PS.spec = v; rysujPunktualnosc(); }));
    f.appendChild(wybor("pz-grupa", "Pacjenci", grupy, PS.grupa, function (v) { PS.grupa = v; rysujPunktualnosc(); }));
    f.appendChild(wybor("pz-prog", "Opóźnienie", [["p15", "ponad 15 minut"], ["p30", "ponad 30 minut"]], PS.prog, function (v) { PS.prog = v; rysujPunktualnosc(); }));
    f.appendChild(wybor("pz-wygl", "Wygładzenie", [["1", "dzień"], ["7", "suma z 7 dni"], ["28", "suma z 28 dni"]], String(PS.wygl), function (v) { PS.wygl = +v; rysujPunktualnosc(); }));
    f.appendChild(wybor("pz-wyroz", "Wyróżnij porę", PORY.map(function (p) { return [p, B.ET.pora[p]]; }), PS.wyrozPora, function (v) { PS.wyrozPora = v; rysujPunktualnosc(); }));
    var fo = B.wyczysc(B.$("pz-powrot-filtry"));
    fo.appendChild(wybor("pz-op-wizyta", "Pierwsza wizyta", [["internista_rano", "Internista rano (6–11)"], ["internista", "Internista, każda pora"], ["wszystkie", "Wszystkie"]],
      PS.opWizyta, function (v) { PS.opWizyta = v; rysujPowrotOpoznienie(); }));
    fo.appendChild(wybor("pz-op-grupa", "Pacjenci (według pierwszego wejścia)", grupy, PS.opGrupa, function (v) { PS.opGrupa = v; rysujPowrotOpoznienie(); }));
    var fz = B.wyczysc(B.$("zw-filtry"));
    fz.appendChild(wybor("zw-grupa", "Pacjenci", [["wszyscy", "Wszyscy"], ["nowe", "Nowe kampanie na L4"], ["pozostale", "Spoza nowych kampanii"]],
      PS.zwGrupa, function (v) { PS.zwGrupa = v; rysujZwroty(); }));
    fz.appendChild(wybor("zw-zam", "Zamówienia", [["wszystkie", "Wszystkie"], ["pierwsze", "Pierwsze"], ["kolejne", "Kolejne"]],
      PS.zwZam, function (v) { PS.zwZam = v; rysujZwroty(); }));
    fz.appendChild(wybor("zw-wygl", "Wygładzenie", [["1", "dzień"], ["7", "suma z 7 dni"], ["28", "suma z 28 dni"]], String(PS.zwWygl), function (v) { PS.zwWygl = +v; rysujZwroty(); }));
    fz.appendChild(wybor("zw-wyroz", "Wyróżnij cel", CELE.map(function (c) { return [c, B.ET.cel[c]]; }), PS.wyrozCel, function (v) { PS.wyrozCel = v; rysujZwroty(); }));
    var fc = B.wyczysc(B.$("oc-filtry"));
    fc.appendChild(wybor("oc-spec", "Specjalizacja", specy, PS.ocSpec, function (v) { PS.ocSpec = v; rysujOceny(); }));
    fc.appendChild(wybor("oc-grupa", "Pacjenci", grupy, PS.ocGrupa, function (v) { PS.ocGrupa = v; rysujOceny(); }));
  }

  // opóźnienia według godziny terminu: gotowa tabela z eksportu (analiza/b2_eksport_c.py, teksty_d)
  function rysujGodziny() {
    var B = b(), G = PZ.godziny, t = B.wyczysc(B.$("pz-godziny"));
    B.$("pz-godziny-tytul").textContent = G.tytul;
    B.$("pz-godziny-przypis").textContent = G.przypis;
    B.zdaniaAlboKarta(B.$("pz-karta-godziny"), B.$("pz-godziny-zdania"), (PZ.karty || {}).godziny, null);
    var tr = B.el("tr");
    G.kolumny.forEach(function (k) { tr.appendChild(B.el("th", { text: k })); });
    t.appendChild(B.el("thead", null, [tr]));
    var tb = B.el("tbody");
    G.wiersze.forEach(function (w) {
      var r = B.el("tr", w.blok ? { class: "wiersz-blok" } : null, [B.el("td", { text: w.opis })]);
      w.komorki.forEach(function (k) { r.appendChild(B.el("td", { text: k })); });
      tb.appendChild(r);
    });
    t.appendChild(tb);
    // wykres: dwa małe wykresy (internista, pozostali lekarze), tabela i jej tytuł w zwijanej sekcji
    var wk = wykresGodzin(G), art = B.$("pz-karta-godziny");
    if (wk) {
      B.BK.wstawWykres(art, wk, true);
      var d = art.querySelector("details.tabela-zwinieta"), ty = B.$("pz-godziny-tytul");
      if (d && ty) d.insertBefore(ty, d.querySelector(".tabela-ramka"));
    }
  }
  // Opóźnienia według godziny terminu: odsetek wizyt odbytych, które zaczęły się ponad 15 minut po terminie
  // (spóźnione / odbyte z pola liczby), dla każdej godziny dwie wąskie kolumny: rok wcześniej (szara) i ostatnie
  // 12 miesięcy (niebieska); ta sama skala w obu wykresach; godziny bloku porannego (pole blok) podcieniowane
  function wykresGodzin(G) {
    var B = b(), BK = B.BK;
    if (!G || !G.wiersze || !G.wiersze.length || !G.wiersze[0].liczby) return null;
    var GR = [["internista", "Internista"], ["pozostali", "Pozostali lekarze"]], mx = 0;
    var p = function (x) { return x && x.odbyte ? 100 * x.spoznione / x.odbyte : null; };
    G.wiersze.forEach(function (w) { GR.forEach(function (g) { var l = w.liczby[g[0]] || {}; mx = Math.max(mx, p(l["1"]) || 0, p(l["2"]) || 0); }); });
    var sk = BK.podzialka(0, mx, 5);
    var t = function (x) { var v = p(x); return v === null ? "—" : B.proc(v) + " (" + B.liczba(x.spoznione) + " z " + B.liczba(x.odbyte) + " wizyt)"; };
    var wykresy = GR.map(function (g) {
      return BK.kolumny({ tytul: g[1], max: sk.max, wys: 150, tloNazwa: "blok poranny",
        os: sk.wartosci.map(function (v) { return { v: v, tekst: B.liczba(v, 0) + "%" }; }),
        grupy: G.wiersze.map(function (w, i) {
          var l = w.liczby[g[0]] || {}, opis = w.opis + ", " + g[1].toLowerCase() + ": rok wcześniej " + t(l["1"]) + ", ostatnie 12 miesięcy " + t(l["2"]) +
            (w.blok ? "; blok poranny" : "");
          return { os: i % 3 === 0 ? [String(w.opis).split("–")[0]] : null, wartosci: [p(l["1"]), p(l["2"])], tlo: !!w.blok, tytul: opis, opis: opis };
        }),
        serie: [{ nazwa: "rok wcześniej", klasa: "sl-a" }, { nazwa: "ostatnie 12 miesięcy", klasa: "sl-b" }],
        opis: g[1] + ": odsetek wizyt spóźnionych ponad 15 minut według godziny terminu, rok wcześniej i ostatnie 12 miesięcy" });
    });
    // legenda tylko nad pierwszym wykresem; drugi ma ją identyczną
    var leg = wykresy[1].querySelector(".wk-legenda");
    if (leg) leg.classList.add("kl-legenda-druga");
    return B.el("div", { class: "wk-dwa" }, wykresy.concat([B.el("p", { class: "wk-przypis wk-dwa-przypis",
      text: "Odsetek wizyt odbytych, które zaczęły się ponad 15 minut po terminie, według godziny terminu. Ta sama skala w obu wykresach." })]));
  }

  BW["po-zakupie"] = {
    pokaz: function () {
      var B = b();
      B.wczytaj("po_zakupie", "po_zakupie").then(function (dane) {
        PZ = dane;
        if (!gotoweP) {
          // karty z danych: D.po_zakupie.karty.* (kontrakt, notatki/e_runda.md 3.5), a gdy ich nie ma — dotychczasowe zdania
          var KP = PZ.karty || {};
          if (PZ.karty) B.$("pz-jak-liczymy").hidden = true;   // definicje i źródła są wtedy w szczegółach kart z danych
          B.zdaniaAlboKarta(B.$("pz-karta-punktualnosc"), B.$("pz-zdania"), KP.punktualnosc || PZ.karta_punktualnosc, PZ.zdania_punktualnosc);
          B.zdaniaAlboKarta(B.$("pz-karta-ruch"), B.$("pz-ruch-zdania"), KP.ruch || PZ.karta_ruch, PZ.zdania_ruch);
          B.zdaniaAlboKarta(B.$("pz-karta-powrot"), B.$("pz-powrot-zdania"), KP.powrot, null);
          rysujGodziny();
          var fr = B.wyczysc(B.$("pz-ruch-filtry"));
          fr.appendChild(wybor("pz-ruch-grupa", "Pacjenci", [["wszyscy", "Wszyscy"], ["pozostale", "Spoza nowych kampanii"]], RUCH_GRUPA,
            function (v) { RUCH_GRUPA = v; rysujRuch(); }));
          B.zdaniaAlboKarta(B.$("pz-karta-zwroty"), B.$("zw-zdania"), KP.zwroty || PZ.karta_zwroty, PZ.zdania_zwroty);
          B.zdaniaAlboKarta(B.$("pz-karta-oceny"), B.$("oc-zdania"), KP.oceny || PZ.karta_oceny, PZ.zdania_oceny);
          filtryP(); gotoweP = true;
        }
        rysujPunktualnosc(); rysujRuch(); rysujZwroty(); rysujOceny(); rysujPowrotOpoznienie();
        // legenda koloru zmian pod pozostałymi tabelami (kolor tylko przy wyraźnej zmianie)
        ["pz-ruch", "pz-powrot", "oc-tabela"].forEach(function (id) { if (B.$(id)) legendaPod(B.$(id), { ocena: true, jednostka: "wizyt", bezMalych: true }); });
        return B.wczytaj("kohorty", "kohorty");
      }).then(function (dane) {
        if (!K) { K = dane; przygotujK(); }
        rysujPowrotOpoznienie();
      }).catch(function (e) { B.akapity(B.$("pz-zdania"), [e.message + ". Odśwież stronę."]); });
    },
    przerysuj: function () { if (PZ) { rysujPunktualnosc(); rysujZwroty(); } }
  };

  // ------------------------------------------------------------ WYNIK BIZNESU
  var WY = null, WS = { krok: "mies", poziom: "grupa", okres: 2, okno: 90 }, wykresW = null, wykresW2 = null, gotoweW = false;

  function okresy(krok) {
    var B = b(), N = B.NDNI, gr = [], cur = null;
    for (var i = 0; i < N; i++) {
      var d = new Date(B.START + i * B.DZIEN), kl;
      if (krok === "mies") kl = d.getUTCFullYear() * 100 + d.getUTCMonth();
      else if (krok === "tydz") kl = i - ((d.getUTCDay() + 6) % 7);      // tydzień od poniedziałku
      else kl = i;
      if (!cur || cur.kl !== kl) { cur = { kl: kl, od: i, do: i }; gr.push(cur); } else cur.do = i;
    }
    return gr;
  }
  function sumaOkresu(arr, g) { var t = 0; for (var i = g.od; i <= g.do; i++) t += arr[i]; return t; }
  function skladowe(g, serie) {
    var S = serie || WY.serie;
    var prz = sumaOkresu(S.przychod_pierwsze, g) + sumaOkresu(S.przychod_powtorne, g), go = sumaOkresu(S.go, g),
      kl = sumaOkresu(S.koszt_lekarza, g), kamp = sumaOkresu(S.wydatki_google, g) + sumaOkresu(S.wydatki_meta, g) + sumaOkresu(S.wydatki_tiktok, g),
      pr = sumaOkresu(S.prowizja, g);
    return { prz: prz, prz1: sumaOkresu(S.przychod_pierwsze, g), prz2: sumaOkresu(S.przychod_powtorne, g), go: go, kl: kl, kamp: kamp, pr: pr,
      marza: prz + go - kl - kamp - pr, zam: sumaOkresu(S.zamowienia, g), nowi: sumaOkresu(S.nowi, g) };
  }
  function rysujWynik() {
    var B = b(), gr = okresy(WS.krok);
    // marża przed kosztem kampanii = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza
    // (= marża + wydatki na kampanie + prowizja, ta sama definicja co w eksporcie); wydatki na kampanie bez prowizji
    var x = new Float64Array(gr.length), cz = { przed: [], kamp: [], marza: [] };
    gr.forEach(function (g, i) {
      x[i] = (B.START + g.od * B.DZIEN) / 1000;
      var s = skladowe(g);
      cz.przed.push(s.prz + s.go - s.kl); cz.kamp.push(s.kamp); cz.marza.push(s.marza);
    });
    var f = function (v) { return B.liczba(v) + " zł"; };
    var serie = [
      { label: "Marża przed kosztem kampanii", kolor: B.css("--series-1"), y: cz.przed, opis: function (di, v) { return f(v); } },
      { label: "Wydatki na kampanie", kolor: B.css("--series-7"), y: cz.kamp, opis: function (di, v) { return f(v); } }
    ];
    if (wykresW) wykresW.destroy();
    if (wykresW2) wykresW2.destroy();
    var et = function (u, ts) {
      if (ts == null) return "—";
      var i = Math.round((ts * 1000 - B.START) / B.DZIEN), g = gr.filter(function (q) { return q.od === i; })[0];
      return g ? B.dataPL(g.od) + (g.do > g.od ? "–" + B.dataPL(g.do) : "") : B.dataPL(i);
    };
    var fY = function (v) { return Math.abs(v) >= 1000 ? B.liczba(v / 1000, 0) + " tys." : B.liczba(v, 0); };
    // tylko zdarzenia, które mogły zmienić wynik: starty kampanii, awaria, zmiana poziomu konwersji (bez jakości danych
    // i bez zmian wykrytych w samych kohortach); jedna lista pod drugim wykresem
    var zdW = B.zdarzeniaNumerowane().filter(function (z) { return z.obszar !== "jakosc" && /^(start|awaria|zmiana poziomu)/.test(String(z.rodzaj)); });
    wykresW = wykres(B.$("wy-wykres"), serie, { x: x, procent: false, jednostka: "zł", punkty: WS.krok === "mies", etykietaX: et, listaZd: zdW, formatY: fY, id: "wynik1" });
    wykresW2 = wykres(B.$("wy-wykres2"), [{ label: "Marża po koszcie lekarza, kampaniach i prowizji", kolor: B.css("--series-3"), y: cz.marza,
      opis: function (di, v) { return f(v); } }], { x: x, procent: false, jednostka: "zł", punkty: WS.krok === "mies", etykietaX: et, listaZd: zdW, listaPod: true, formatY: fY, wys: 240, id: "wynik2" });
    // tabela miesięczna z sumami okresów
    var t = B.wyczysc(B.$("wy-tabela"));
    var kol = [["Okres", null], ["Zamówienia", "zam"], ["Nowi pacjenci", "nowi"], ["Przychód: pierwsze zamówienia", "prz1"],
      ["Przychód: kolejne zamówienia", "prz2"], ["TelemediGO", "go"], ["Koszt lekarza", "kl"], ["Kampanie", "kamp"],
      ["Prowizja afiliacyjna", "pr"], ["Marża", "marza"]];
    t.appendChild(B.el("thead", null, [B.el("tr", null, kol.map(function (k) { return B.el("th", { text: k[0] + (k[1] && k[1] !== "zam" && k[1] !== "nowi" ? " (zł)" : "") }); }))]));
    var tb = B.el("tbody");
    var O = B.O, okr = [{ nazwa: "Rok wcześniej (" + O[0].nazwa + ")", od: B.idxIso(O[0].od), do: B.idxIso(O[0].do) },
      { nazwa: "Ostatnie 12 miesięcy (" + O[1].nazwa + ")", od: B.idxIso(O[1].od), do: B.idxIso(O[1].do) }];
    var s1 = skladowe(okr[0]), s2 = skladowe(okr[1]);
    okr.forEach(function (o, j) {
      var s = j ? s2 : s1;
      tb.appendChild(B.el("tr", { class: "podsuma" }, kol.map(function (k) { return B.el("td", { text: k[1] ? B.liczba(s[k[1]]) : o.nazwa }); })));
    });
    tb.appendChild(B.el("tr", { class: "podsuma" }, kol.map(function (k) {
      return B.el("td", { text: k[1] ? (s1[k[1]] ? B.znak(100 * (s2[k[1]] / s1[k[1]] - 1), 1) + "%" : "—") : "Zmiana rok do roku" });
    })));
    rysujKwartaly();
    okresy("mies").forEach(function (g) {
      var s = skladowe(g), d = new Date(B.START + g.od * B.DZIEN);
      tb.appendChild(B.el("tr", null, kol.map(function (k) {
        return B.el("td", { text: k[1] ? B.liczba(s[k[1]]) : B.RZYM[d.getUTCMonth()] + " " + d.getUTCFullYear() });
      })));
    });
    t.appendChild(tb);
  }

  // kwartały ostatnich 12 miesięcy i te same kwartały rok wcześniej: [{kw: „IV kw. 2025”, kwA: „IV kw. 2024”, sA, sB}]
  function kwartalyRr(serie) {
    var B = b(), N = B.NDNI, i = B.idxIso(B.O[1].od), out = [];
    while (i < N) {
      var d = new Date(B.START + i * B.DZIEN), m = d.getUTCMonth(), y = d.getUTCFullYear();
      var dk = new Date(Date.UTC(y, m + 3, 1)), k = Math.min(N - 1, Math.round((dk.getTime() - B.START) / B.DZIEN) - 1);
      var dp = new Date(Date.UTC(y - 1, m, 1)), dpk = new Date(Date.UTC(y - 1, m + 3, 1));
      var ip = Math.round((dp.getTime() - B.START) / B.DZIEN), kp = Math.round((dpk.getTime() - B.START) / B.DZIEN) - 1;
      var sB = skladowe({ od: i, do: k }, serie), sA = skladowe({ od: ip, do: kp }, serie);
      sB.przgo = sB.prz + sB.go; sA.przgo = sA.prz + sA.go;
      // marża przed kosztem kampanii = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza (jak na wykresie wyżej)
      sB.przed = sB.prz + sB.go - sB.kl; sA.przed = sA.prz + sA.go - sA.kl;
      var q = B.RZYM[Math.floor(m / 3)] + " kw. ";
      out.push({ kw: q + y, kwA: q + (y - 1), sA: sA, sB: sB });
      i = k + 1;
    }
    return out;
  }
  // Słupki grupowane kwartałów: zmiana rok do roku marży przed kosztem kampanii obok zmiany wydatków na kampanie
  // (wydatki bez prowizji, kolor jak na wykresie „Wyniku biznesu”). Dane: wynik.js (serie dzienne).
  function wykresKwartalow(dane) {
    var B = b(), lista = kwartalyRr(dane ? dane.serie : null), wsz = [];
    var zm = function (a, v) { return a ? 100 * (v / a - 1) : null; };
    var zl = function (v) { return B.liczba(v) + " zł"; };
    var wiersze = lista.map(function (q) {
      var p = zm(q.sA.przed, q.sB.przed), k = zm(q.sA.kamp, q.sB.kamp);
      wsz.push(p, k);
      return { etykieta: q.kw, wartosci: [p, k], teksty: [p === null ? "—" : B.znak(p, 1) + "%", k === null ? "—" : B.znak(k, 1) + "%"],
        tytul: q.kw + " wobec " + q.kwA + ": marża przed kosztem kampanii " + zl(q.sB.przed) + " wobec " + zl(q.sA.przed) +
          ", wydatki na kampanie " + zl(q.sB.kamp) + " wobec " + zl(q.sA.kamp) };
    });
    var ok = wsz.filter(function (v) { return v !== null && isFinite(v); });
    var sk = B.BK.podzialka(Math.min.apply(null, ok.concat([0])), Math.max.apply(null, ok.concat([0])), 6);
    return B.BK.slupkiGrupowane({ min: sk.min, max: sk.max, wiersze: wiersze,
      os: sk.wartosci.map(function (v) { return (v > 0 ? "+" : "") + B.liczba(v, 0) + "%"; }),
      serie: [{ nazwa: "marża przed kosztem kampanii", klasa: "sg-marza" }, { nazwa: "wydatki na kampanie", klasa: "sg-kampanie" }],
      opis: "Zmiana rok do roku w każdym kwartale: marża przed kosztem kampanii i wydatki na kampanie",
      przypis: "Zmiana wobec tego samego kwartału rok wcześniej. Marża przed kosztem kampanii to przychód z konsultacji po zwrotach i z TelemediGO minus koszt lekarza; wydatki na kampanie bez prowizji afiliacyjnej." });
  }
  BW.wykresKwartalow = wykresKwartalow;

  function rysujKwartaly() {
    var B = b(), t = B.wyczysc(B.$("wy-kwartaly"));
    var kol = [["Marża po wszystkich kosztach", "marza"], ["Wydatki na kampanie", "kamp"], ["Przychód: konsultacje po zwrotach i TelemediGO", "przgo"],
      ["Koszt lekarza", "kl"], ["Nowi pacjenci", "nowi"]];
    var w = B.$("wy-kwartaly-wykres");
    if (w) B.wyczysc(w).appendChild(wykresKwartalow(WY));
    t.appendChild(B.el("thead", null, [B.el("tr", null, [B.el("th", { text: "Kwartał" })]
      .concat(kol.map(function (k) { return B.el("th", { text: k[0] }); })))]));
    var tb = B.el("tbody");
    kwartalyRr().forEach(function (q) {
      var sA = q.sA, sB = q.sB;
      var tr = B.el("tr", null, [B.el("td", { text: q.kw, title: q.kw + " wobec " + q.kwA })]);
      kol.forEach(function (kk) {
        var a = sA[kk[1]], bb = sB[kk[1]], zm = a ? 100 * (bb / a - 1) : null, zl = kk[1] !== "nowi";
        // wydatki na kampanie: wzrost to „uwaga” (jak kafelek wydatków w „Czy to wzrost”); koszt lekarza rośnie z liczbą wizyt, bez oceny
        var stanZm = kk[1] === "kamp" ? (zm > 0 ? "uwaga" : "neutralnie") : kk[1] === "kl" ? "neutralnie" : (zm > 0 ? "dobrze" : "zle");
        tr.appendChild(B.el("td", null, [B.el("span", { class: "b", text: B.liczba(bb) + (zl ? " zł" : "") }),
          B.el("span", { class: "a", text: "rok wcześniej: " + B.liczba(a) + (zl ? " zł" : "") }, [
            B.BK.zmiana(B.znak(zm, 1) + "%", B.BK.kierunekZnaku(zm), stanZm,
              (zm >= 0 ? "Wzrost" : "Spadek") + " o " + B.liczba(Math.abs(zm), 1) + "% rok do roku")])]));
      });
      tb.appendChild(tr);
    });
    t.appendChild(tb);
  }

  function rysujEkonomie() {
    var B = b(), ET = B.ET, w = WY.ekonomia.wiersze.filter(function (r) { return r.poziom === WS.poziom && r.okres === WS.okres; });
    var klucze = [];
    w.forEach(function (r) { if (klucze.indexOf(r.klucz) < 0) klucze.push(r.klucz); });
    var znajdz = function (k, reg, okno) { return w.filter(function (r) { return r.klucz === k && r.regula === reg && r.okno === okno; })[0]; };
    var t = B.wyczysc(B.$("ek-tabela"));
    var h1 = B.el("tr", null, [B.el("th", { text: WS.poziom === "grupa" ? "Grupa" : WS.poziom === "kanal" ? "Kanał" : "Kampania" }),
      B.el("th", { text: "Według pierwszego wejścia", colspan: 2, style: "text-align:center" }),
      B.el("th", { text: "Według sesji z płatnością", colspan: 2, style: "text-align:center" }), B.el("th", { text: "" })]);
    var h2 = B.el("tr", null, [B.el("th", { text: "" })]);
    [0, 1].forEach(function () {
      ["Koszt pozyskania", "Wynik na pacjenta w " + WS.okno + " dniach"].forEach(function (x) { h2.appendChild(B.el("th", { text: x })); });
    });
    var tt = B.$("ek-tabela-tytul");
    if (tt) tt.textContent = "Tabela: koszt pozyskania i wynik na pacjenta w " + WS.okno + " dniach, obie reguły przypisania";
    h2.appendChild(B.el("th", { text: "Ocena" }));
    t.appendChild(B.el("thead", null, [h1, h2]));
    var tb = B.el("tbody");
    var et = function (k) { return WS.poziom === "grupa" ? (ET.grupa_ek[k] || k) : WS.poziom === "kanal" ? (ET.kanal[k] || k) : (ET.kampania[k] || k); };
    var zl = function (v) { return (v > 0 ? "+" : "") + B.liczba(v, 1) + " zł"; };
    klucze.forEach(function (k) {
      var tr = B.el("tr", null, [B.el("td", { text: et(k) })]), znaki = {};
      ["Z1K", "Z2"].forEach(function (reg) {
        [znajdz(k, reg, WS.okno)].forEach(function (r, j) {
          if (!r) { tr.appendChild(B.el("td", { text: "—" })); tr.appendChild(B.el("td", { text: "—" })); return; }
          znaki[reg + j] = r.wynik >= 0;
          tr.appendChild(B.el("td", null, [B.el("span", { class: "b", text: B.liczba(r.cac, 1) + " zł" }),
            B.el("span", { class: "a", text: B.liczba(r.nowi) + " pac." })]));
          tr.appendChild(B.el("td", { title: "Przedział warunkowy " + B.liczba(r.od, 1) + "–" + B.liczba(r.do, 1) + " zł. Powrót: " + B.liczba(r.powrot, 1) + "%." },
            [B.el("span", { class: "b" + (r.wynik < 0 ? " ujemne" : ""), text: zl(r.wynik) }),
              B.el("span", { class: "a", text: "marża " + B.liczba(r.marza, 1) + " zł − koszt " + B.liczba(r.cac, 1) + " zł" })]));
        });
      });
      var niepewne = znaki.Z1K0 !== undefined && znaki.Z20 !== undefined && znaki.Z1K0 !== znaki.Z20;
      tr.appendChild(B.el("td", null, [niepewne ? B.BK.znacznik({ tekst: "Niepewny: znak zależy od przypisania źródła", stan: "uwaga" }) : null]));
      tb.appendChild(tr);
    });
    t.appendChild(tb);
    rysujEkonomieWykres(w, klucze, et, znajdz);
  }
  function rysujEkonomieWykres(w, klucze, et, znajdz) {
    var B = b(), BK = B.BK, okno = WS.okno, zl = function (v) { return (v > 0 ? "+" : "") + B.liczba(v, 1) + " zł"; };
    var wiersze = klucze.map(function (k) {
      var r1 = znajdz(k, "Z1K", okno), r2 = znajdz(k, "Z2", okno), v1 = r1 ? r1.wynik : null, v2 = r2 ? r2.wynik : null;
      var rozne = v1 !== null && v2 !== null && (v1 >= 0) !== (v2 >= 0);
      return { etykieta: et(k), punkty: [{ v: v1, klasa: "pkt-r1" }, { v: v2, klasa: "pkt-r2" }],
        teksty: [v1 === null ? "—" : zl(v1), v2 === null ? "—" : zl(v2)], ujemne: [v1 < 0, v2 < 0],
        uwaga: rozne ? BK.znacznik({ tekst: "Znak zależy od przypisania", stan: "uwaga" }) : null };
    }).filter(function (r) { return r.punkty[0].v !== null || r.punkty[1].v !== null; });
    var wsz = []; wiersze.forEach(function (r) { r.punkty.forEach(function (p) { if (p.v !== null) wsz.push(p.v); }); });
    var krok = 20, mn = Math.min(0, Math.floor(Math.min.apply(null, wsz.concat([0])) / krok) * krok),
      mx = Math.max(0, Math.ceil(Math.max.apply(null, wsz.concat([0])) / krok) * krok);
    if (mx === mn) mx = mn + krok;
    if ((mx - mn) / krok > 6) {   // szeroki zakres: podziałka co 40 zł, oś znowu od wielokrotności kroku, żeby zero było na podziałce
      krok = 40;
      mn = Math.min(0, Math.floor(Math.min.apply(null, wsz.concat([0])) / krok) * krok);
      mx = Math.max(0, Math.ceil(Math.max.apply(null, wsz.concat([0])) / krok) * krok);
    }
    var os = []; for (var v = mn; v <= mx + 0.001; v += krok) os.push((v > 0 ? "+" : "") + B.liczba(v, 0) + " zł");
    var c = B.wyczysc(B.$("ek-wykres"));
    if (!wiersze.length) {
      c.appendChild(B.el("p", { class: "lejek-pusty", text: "Na tym poziomie dane nie mają wyniku w oknie " + okno + " dni. Wybierz okno 90 dni albo inny poziom." }));
      return;
    }
    c.appendChild(BK.punktyZero({ legenda: [{ klasa: "pkt-r1", nazwa: "według pierwszego wejścia" }, { klasa: "pkt-r2", nazwa: "według sesji z płatnością" }],
      min: mn, max: mx, os: os, wiersze: wiersze,
      opis: "Wynik na pacjenta po koszcie pozyskania w " + okno + " dniach według dwóch reguł przypisania źródła",
      przypis: "Wynik na pacjenta w " + okno + " dniach: marża na pacjenta minus koszt pozyskania. Pionowa linia to zero: na lewo od niej kampania traci na każdym pacjencie." }));
  }

  BW.wynik = {
    pokaz: function () {
      var B = b();
      B.wczytaj("wynik", "wynik").then(function (dane) {
        WY = dane;
        if (!gotoweW) {
          B.zdaniaAlboKarta(B.$("wy-karta"), B.$("wy-zdania"), WY.karta, WY.zdania);
          B.$("wy-granica").textContent = WY.granica || "";
          B.zdaniaAlboKarta(B.$("ek-karta"), B.$("ek-zdania"), WY.ekonomia.karta, WY.ekonomia.zdania);
          var f = B.wyczysc(B.$("wy-filtry"));
          f.appendChild(wybor("wy-krok", "Grupowanie", [["mies", "miesiące"], ["tydz", "tygodnie"], ["dzien", "dni"]], WS.krok,
            function (v) { WS.krok = v; rysujWynik(); }));
          var fe = B.wyczysc(B.$("ek-filtry"));
          fe.appendChild(wybor("ek-poziom", "Poziom", [["grupa", "Grupy kampanii"], ["kampania", "Kampanie"], ["kanal", "Kanały"]], WS.poziom,
            function (v) { WS.poziom = v; rysujEkonomie(); }));
          fe.appendChild(wybor("ek-okres", "Okres", [["2", "Ostatnie 12 miesięcy (" + B.O[1].nazwa + ")"], ["1", "Rok wcześniej (" + B.O[0].nazwa + ")"]], String(WS.okres),
            function (v) { WS.okres = +v; rysujEkonomie(); }));
          // okno wykresu wyniku: przełącznik 90 / 180 dni (tabela w szczegółach pokazuje oba)
          var g = B.el("div", { class: "przelacznik", role: "group", "aria-label": "Okno wyniku na pacjenta" });
          [90, 180].forEach(function (n) {
            var p = B.el("button", { type: "button", "aria-pressed": String(WS.okno === n), text: n + " dni" });
            p.onclick = function () { WS.okno = n; Array.prototype.forEach.call(g.querySelectorAll("button"), function (x) { x.setAttribute("aria-pressed", String(x === p)); }); rysujEkonomie(); };
            g.appendChild(p);
          });
          fe.appendChild(B.el("label", { class: "filtr-przelacznik" }, ["Okno wyniku", g]));
          gotoweW = true;
        }
        rysujWynik(); rysujEkonomie();
      }).catch(function (e) { B.akapity(B.$("wy-zdania"), [e.message + ". Odśwież stronę."]); });
    },
    przerysuj: function () { if (WY) rysujWynik(); }
  };
})();
