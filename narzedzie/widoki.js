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
    [["rok", "Okres 2 wobec okresu 1 (rok do roku)"], ["90", "Ostatnie 90 dni wobec poprzednich 90"],
      ["30rr", "Ostatnie 30 dni wobec tych samych dni rok wcześniej"]].forEach(function (o) {
      sel.appendChild(B.el("option", { value: o[0], text: o[1] }));
    });
    B.ZD.lista.forEach(function (z) {
      sel.appendChild(B.el("option", { value: "zd:" + z.id, text: "60 dni przed i po: " + z.tytul + " (" + B.dataPL(B.idxIso(z.od)) + ")" }));
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
  function cieniuj(u, a, bb) {
    var B = b(), ctx = u.ctx, top = u.bbox.top, h = u.bbox.height;
    [[a, B.css("--okres-a")], [bb, B.css("--okres-b")]].forEach(function (o) {
      if (!o[0]) return;
      var x0 = u.valToPos((B.START + o[0][0] * B.DZIEN) / 1000, "x", true);
      var x1 = u.valToPos((B.START + (o[0][1] + 1) * B.DZIEN) / 1000, "x", true);
      x0 = Math.max(x0, u.bbox.left); x1 = Math.min(x1, u.bbox.left + u.bbox.width);
      if (x1 > x0) { ctx.save(); ctx.fillStyle = o[1]; ctx.fillRect(x0, top, x1 - x0, h); ctx.restore(); }
    });
  }
  /* serie: [{label, kolor (numer serii albo kolor css), y, opis(di, v)}], o: {jednostka, procent, a, b, zdarzenia, x, min, max} */
  function wykres(cel, serie, o) {
    var B = b();
    B.wyczysc(cel);
    var x = o.x;
    if (!x) { x = new Float64Array(B.NDNI); for (var i = 0; i < B.NDNI; i++) x[i] = (B.START + i * B.DZIEN) / 1000; }
    var dane = [x], ser = [{ label: "Dzień", value: o.etykietaX || function (u, ts) { return ts == null ? "—" : B.dataPL(Math.round((ts * 1000 - B.START) / B.DZIEN)); } }];
    serie.forEach(function (s) {
      dane.push(s.y);
      ser.push({ label: s.label, stroke: typeof s.kolor === "number" ? B.css("--series-" + s.kolor) : s.kolor, width: 2,
        points: { show: !!o.punkty, size: 6 },
        value: function (u, v, si, di) { return v == null ? "—" : s.opis ? s.opis(di, v) : B.liczba(v, 1); } });
    });
    var zd = o.zdarzenia ? B.zdarzeniaNumerowane() : [];
    var opts = {
      width: Math.max(320, cel.clientWidth), height: o.wys || 320,
      scales: { x: { time: true, min: o.min, max: o.max },
        y: { range: function (u, mn, mx) { return [Math.min(0, mn), o.procent ? Math.min(100, Math.max(5, mx * 1.08)) : (mx > 0 ? mx * 1.08 : 1)]; } } },
      axes: B.osieWykresu(o.jednostka || "", o.formatY || function (v) { return B.liczba(v, 0) + (o.procent ? "%" : ""); }),
      series: ser, cursor: { drag: { x: true, y: false } }, legend: { live: true },
      tzDate: function (ts) { return uPlot.tzDate(new Date(ts * 1000), "Etc/UTC"); },
      hooks: { drawClear: [function (u) { cieniuj(u, o.a, o.b); }], draw: [function (u) { if (zd.length) B.rysujZdarzeniaNaWykresie(u, zd); }] }
    };
    if (o.osX) opts.axes[0].values = o.osX;
    return new uPlot(opts, dane, cel);
  }
  function krocz(arr, w) { return b().krocz(arr, w); }
  function suma(arr, z) { var t = 0; if (!z) return 0; for (var i = z[0]; i <= z[1]; i++) t += arr[i]; return t; }
  function komorka(pB, nB, pA, nA, jedn, miejsca, odwrotnie) {
    var B = b(), td = B.el("td"), j = jedn || "%", m = miejsca === undefined ? 1 : miejsca;
    var f = function (v) { return v === null || !isFinite(v) ? "—" : B.liczba(v, m) + (j === "%" ? "%" : " " + j); };
    td.appendChild(B.el("span", { class: "b", text: f(pB) }));
    td.appendChild(B.el("span", { class: "n", text: nB !== null ? " z " + B.liczba(nB) : "" }));
    var a = B.el("span", { class: "a", text: "A: " + f(pA) + (nA !== null ? " z " + B.liczba(nA) : "") + " " });
    if (pA !== null && pB !== null && isFinite(pA) && isFinite(pB)) {
      var d = pB - pA, zero = Math.abs(d) < Math.pow(10, -m) / 2, lepiej = odwrotnie ? d < 0 : d > 0;
      a.appendChild(B.el("span", { class: "delta " + (zero ? "zero" : lepiej ? "plus" : "minus"),
        text: (zero ? "= " : d > 0 ? "▲" : "▼") + B.liczba(Math.abs(d), m) }));
    }
    td.appendChild(a);
    return td;
  }
  function opisOkresow(S) {
    var B = b();
    return "Okres A: " + B.dataPL(S.a[0]) + "–" + B.dataPL(S.a[1]) + ". Okres B: " + B.dataPL(S.b[0]) + "–" + B.dataPL(S.b[1]) + ".";
  }
  function datyAB(pref, S, odswiez) {
    var B = b(), f = B.el("div", { class: "filtry-daty" });
    ["a", "b"].forEach(function (k) {
      var fs = B.el("fieldset", { class: "okresy" }, [B.el("legend", { text: "Okres " + k.toUpperCase() })]);
      ["od", "do"].forEach(function (g, j) {
        var i = B.el("input", { type: "date", id: pref + "-" + k + "-" + g, min: B.P.meta.start, max: B.P.meta.koniec,
          "aria-label": "Okres " + k.toUpperCase() + " " + g });
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
  var WYMIARY = [
    { id: "kanal", nazwa: "Źródło (kanał)", reg: true }, { id: "kampania", nazwa: "Kampania", reg: true },
    { id: "grupa", nazwa: "Nowe kampanie na L4" }, { id: "urzadzenie", nazwa: "Urządzenie" },
    { id: "przegladarka", nazwa: "Przeglądarka" }, { id: "usluga", nazwa: "Pierwsza usługa" },
    { id: "znizka", nazwa: "Zniżka" }, { id: "go0", nazwa: "TelemediGO przy pierwszym zakupie" },
    { id: "status1", nazwa: "Status pierwszego zamówienia" }, { id: "koszyk", nazwa: "Opóźnienie pierwszej wizyty" },
    { id: "pora", nazwa: "Pora pierwszej wizyty" }
  ];
  var MIARY_K = [["powrot", "Powrót w oknie"], ["marza", "Marża na pacjenta w oknie"], ["nowi", "Nowi pacjenci dziennie"],
    ["udzial", "Udział w nowych pacjentach"]];
  var K = null, KOD = {}, KS = null, wykresK = null, gotoweK = false;

  function domyslneK() {
    var s = { regula: "Z1K", f: {}, podz: "grupa", okno: 90, miara: "powrot", wygl: 7, preset: "rok", wybrane: null, kolory: {} };
    okresyPreset("rok", s);
    return s;
  }
  function kluczWym(id) {
    var w = WYMIARY.filter(function (x) { return x.id === id; })[0];
    return w && w.reg && KS.regula === "Z2" ? id + "_z2" : id;
  }
  function etykietaWart(id, v) {
    var B = b(), ET = B.ET;
    if (v === "__razem") return "Wszyscy w filtrze";
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

  var OKNA_MACIERZY = [7, 14, 30, 60, 90, 180], KS_GRAN = "tydz", wykresKrz = null;
  var RAMPA = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281"];

  function grupyKohort(gran) {
    var B = b(), N = B.NDNI, gr = [], cur = null;
    for (var i = 0; i < N; i++) {
      var d = new Date(B.START + i * B.DZIEN);
      var kl = gran === "tydz" ? i - ((d.getUTCDay() + 6) % 7) : d.getUTCFullYear() * 100 + d.getUTCMonth();
      if (!cur || cur.kl !== kl) { cur = { kl: kl, od: i, do: i }; gr.push(cur); } else cur.do = i;
    }
    return gr;
  }

  function rysujMacierz() {
    var B = b(), N = B.NDNI, idx = pacjenciFiltru(), gr = grupyKohort(KS_GRAN), przyp = new Int32Array(N);
    gr.forEach(function (g, j) { for (var i = g.od; i <= g.do; i++) przyp[i] = j; });
    var st = gr.map(function () { return { n: 0, r: OKNA_MACIERZY.map(function () { return 0; }) }; });
    idx.forEach(function (i) {
      var s_ = st[przyp[K.d[i]]], r = K.r[i];
      s_.n++;
      if (r >= 0) OKNA_MACIERZY.forEach(function (w, k) { if (r <= w) s_.r[k]++; });
    });
    var zd = B.zdarzeniaNumerowane();
    var wiersze = gr.map(function (g, j) {
      var x = st[j];
      return { g: g, n: x.n, p: OKNA_MACIERZY.map(function (w, k) { return g.do <= N - 1 - w && x.n > 0 ? 100 * x.r[k] / x.n : null; }),
        zd: zd.filter(function (z) { var di = B.idxIso(z.od); return di >= g.od && di <= g.do; }) };
    });
    var mn = OKNA_MACIERZY.map(function (w, k) {
      var v = wiersze.map(function (r) { return r.p[k]; }).filter(function (x) { return x !== null; });
      return v.length ? [Math.min.apply(null, v), Math.max.apply(null, v)] : [0, 1];
    });
    var t = B.wyczysc(B.$("ko-macierz"));
    var hr = B.el("tr", null, [B.el("th", { text: KS_GRAN === "tydz" ? "Kohorta (tydzień od)" : "Kohorta (miesiąc)" }),
      B.el("th", { text: "Nowi pacjenci" }), B.el("th", { text: "Zdarzenia" })]);
    OKNA_MACIERZY.forEach(function (w) { hr.appendChild(B.el("th", { text: w + " dni" })); });
    t.appendChild(B.el("thead", null, [hr]));
    var tb = B.el("tbody");
    wiersze.forEach(function (r) {
      var d = new Date(B.START + r.g.od * B.DZIEN);
      var naz = KS_GRAN === "tydz" ? B.dataPL(r.g.od) : B.RZYM[d.getUTCMonth()] + " " + d.getUTCFullYear();
      var tr = B.el("tr", null, [B.el("td", { text: naz }), B.el("td", { text: B.liczba(r.n) }),
        B.el("td", { class: "macierz-zd", text: r.zd.map(function (z) { return z.nr; }).join(", "),
          title: r.zd.map(function (z) { return z.nr + ". " + z.tytul; }).join("\n") })]);
      r.p.forEach(function (v, k) {
        if (v === null) { tr.appendChild(B.el("td", { class: "macierz-pusta", text: "·", title: "Kohorta nie ma jeszcze pełnego okna " + OKNA_MACIERZY[k] + " dni" })); return; }
        var z = mn[k], u = z[1] > z[0] ? (v - z[0]) / (z[1] - z[0]) : 0.5, st_ = Math.min(RAMPA.length - 1, Math.floor(u * RAMPA.length));
        tr.appendChild(B.el("td", { class: "macierz-kom", style: "background:" + RAMPA[st_] + ";color:" + (st_ >= 7 ? "#fff" : "#0b0b0b"),
          text: B.liczba(v, 1), title: naz + ": powrót w " + OKNA_MACIERZY[k] + " dniach " + B.proc(v) + " z " + B.liczba(r.n) + " pacjentów" }));
      });
      tb.appendChild(tr);
    });
    t.appendChild(tb);
  }

  function rysujKrzywa() {
    var B = b(), idx = pacjenciFiltru(), D = 180, xs = [], yA = [], yB = [], nA = [], nB = [];
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
    if (wykresKrz) wykresKrz.destroy();
    wykresKrz = new uPlot({
      width: Math.max(320, cel.clientWidth), height: 300,
      scales: { x: { time: false }, y: { range: [0, mx * 1.1] } },
      axes: [{ stroke: m, grid: { stroke: g, width: 1 }, ticks: { stroke: g, width: 1, size: 4 }, font: "12px system-ui",
        label: "dni od pierwszego zakupu", labelFont: "12px system-ui", values: function (u, sp) { return sp.map(function (v) { return v; }); } },
      { stroke: m, grid: { stroke: g, width: 1 }, ticks: { stroke: g, width: 1, size: 4 }, font: "12px system-ui", size: 56,
        values: function (u, sp) { return sp.map(function (v) { return B.liczba(v, 0) + "%"; }); } }],
      series: [{ label: "Dzień", value: function (u, v) { return v == null ? "—" : v + ". dzień"; } },
        { label: "Okres A (" + B.dataPL(KS.a[0]) + "–" + B.dataPL(KS.a[1]) + ")", stroke: B.css("--ink-2"), width: 2,
          value: function (u, v, si, di) { return v == null ? "—" : B.proc(v) + " z " + B.liczba(nA[di]); } },
        { label: "Okres B (" + B.dataPL(KS.b[0]) + "–" + B.dataPL(KS.b[1]) + ")", stroke: B.css("--series-1"), width: 2,
          value: function (u, v, si, di) { return v == null ? "—" : B.proc(v) + " z " + B.liczba(nB[di]) + (yA[di] ? ", " + B.liczba(100 * v / yA[di], 0) + "% poziomu A" : ""); } }],
      legend: { live: true }, cursor: { drag: { x: true, y: false } }
    }, [xs, yA, yB], cel);
  }

  function agregujK() {
    var N = b().NDNI, okna = K.okna, ile = okna.length;
    var filtry = Object.keys(KS.f).filter(function (id) { return KS.f[id] !== ""; }).map(function (id) {
      var kody = kodyWym(id), wart = wartosciWym(id), idx = wart.indexOf(KS.f[id]);
      return { kody: kody, idx: idx };
    });
    var podz = KS.podz ? kodyWym(KS.podz) : null, wartP = KS.podz ? wartosciWym(KS.podz) : [];
    var grupy = {}, razem = nowaGrupa();
    function nowaGrupa() {
      var g = { cnt: new Float64Array(N), ret: [], mar: [] };
      for (var k = 0; k < ile; k++) { g.ret.push(new Float64Array(N)); g.mar.push(new Float64Array(N)); }
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
          g.mar[k][d] += marze[k][i] / 10;
        }
      }
    }
    grupy.__razem = razem;
    return grupy;
  }
  function statyK(g, wszyscy) {
    var okna = K.okna, s = { nA: suma(g.cnt, KS.a), nB: suma(g.cnt, KS.b), okna: [] };
    s.uA = suma(wszyscy.cnt, KS.a) ? 100 * s.nA / suma(wszyscy.cnt, KS.a) : null;
    s.uB = suma(wszyscy.cnt, KS.b) ? 100 * s.nB / suma(wszyscy.cnt, KS.b) : null;
    okna.forEach(function (n, k) {
      var z = zakresyOkna(n);
      if (!z) { s.okna.push(null); return; }
      var eA = suma(g.cnt, z.a), eB = suma(g.cnt, z.b);
      s.okna.push({ eA: eA, eB: eB, pA: eA ? 100 * suma(g.ret[k], z.a) / eA : null, pB: eB ? 100 * suma(g.ret[k], z.b) / eB : null,
        mA: eA ? suma(g.mar[k], z.a) / eA : null, mB: eB ? suma(g.mar[k], z.b) / eB : null, z: z });
    });
    return s;
  }
  function przydziel(S) {
    var zajete = {};
    Object.keys(S.kolory).forEach(function (w) { if (S.wybrane.indexOf(w) < 0) delete S.kolory[w]; else zajete[S.kolory[w]] = true; });
    S.wybrane.forEach(function (w) {
      if (S.kolory[w]) return;
      for (var i = 1; i <= 8; i++) if (!zajete[i]) { S.kolory[w] = i; zajete[i] = true; return; }
    });
  }
  function zapiszAdresK() {
    var q = new URLSearchParams(), B = b();
    q.set("regula", KS.regula); q.set("podz", KS.podz); q.set("okno", KS.okno); q.set("miara", KS.miara); q.set("wygl", KS.wygl);
    q.set("a", B.isoIdx(KS.a[0]) + "_" + B.isoIdx(KS.a[1])); q.set("b", B.isoIdx(KS.b[0]) + "_" + B.isoIdx(KS.b[1]));
    Object.keys(KS.f).forEach(function (id) { if (KS.f[id] !== "") q.set("f_" + id, KS.f[id]); });
    if (KS.wybrane) q.set("w", KS.wybrane.join(","));
    history.replaceState(null, "", "#kohorty?" + q.toString());
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
    ["a", "b"].forEach(function (k) {
      var v = q.get(k);
      if (v && v.indexOf("_") > 0) { var c = v.split("_"); KS[k] = [B.ogranicz(B.idxIso(c[0])), B.ogranicz(B.idxIso(c[1]))]; KS.preset = "wlasne"; }
    });
    var r = domyslneK();
    if (KS.preset === "wlasne" && KS.a.join() === r.a.join() && KS.b.join() === r.b.join()) KS.preset = "rok";
    WYMIARY.forEach(function (w) { if (q.get("f_" + w.id)) KS.f[w.id] = q.get("f_" + w.id); });
    KS.wybrane = q.get("w") ? q.get("w").split(",").filter(Boolean) : null;
  }

  function filtryK() {
    var B = b(), box = B.wyczysc(B.$("ko-filtry"));
    var odswiez = function () { rysujK(); };
    box.appendChild(wybor("ko-regula", "Reguła źródła", [["Z1K", "Przyjęta: pierwsze wejście, kod kampanii rozstrzyga"],
      ["Z2", "Sesja płatności"]], KS.regula, function (v) {
      KS.regula = v; KS.wybrane = null; KS.kolory = {}; filtryK(); odswiez();
    }));
    WYMIARY.forEach(function (w) {
      var opcje = [["", "wszystkie"]].concat(wartosciWym(w.id).map(function (v) { return [v, etykietaWart(w.id, v)]; }));
      if (KS.f[w.id] && wartosciWym(w.id).indexOf(KS.f[w.id]) < 0) KS.f[w.id] = "";
      box.appendChild(wybor("ko-f-" + w.id, w.nazwa, opcje, KS.f[w.id] || "", function (v) { KS.f[w.id] = v; odswiez(); }));
    });
    box.appendChild(wybor("ko-podz", "Podział na serie", [["", "bez podziału"]].concat(WYMIARY.map(function (w) { return [w.id, w.nazwa]; })),
      KS.podz, function (v) { KS.podz = v; KS.wybrane = null; KS.kolory = {}; odswiez(); }));
    var pr = B.el("select", { id: "ko-preset" });
    opcjePresetow(pr);
    pr.value = KS.preset;
    pr.onchange = function () { if (this.value !== "wlasne") okresyPreset(this.value, KS); else KS.preset = "wlasne"; filtryK(); odswiez(); };
    box.appendChild(B.el("label", null, ["Porównanie", pr]));
    box.appendChild(datyAB("ko", KS, function () { filtryK(); odswiez(); }));
    var fw = B.wyczysc(B.$("ko-filtry-wykresu"));
    fw.appendChild(wybor("ko-miara", "Miara", MIARY_K, KS.miara, function (v) { KS.miara = v; rysujK(true); }));
    fw.appendChild(wybor("ko-okno", "Okno", K.okna.map(function (n) { return [String(n), n + " dni od pierwszego zakupu"]; }),
      String(KS.okno), function (v) { KS.okno = +v; rysujK(true); }));
    fw.appendChild(wybor("ko-wygl", "Wygładzenie", [["1", "bez wygładzenia (dzień)"], ["7", "suma z 7 dni"], ["28", "suma z 28 dni"]],
      String(KS.wygl), function (v) { KS.wygl = +v; rysujK(true); }));
  }

  function rysujK(tylkoWykres) {
    var B = b(), grupy = agregujK(), wszyscy = grupy.__razem;
    var lista = Object.keys(grupy).filter(function (w) { return w !== "__razem"; }).map(function (w) {
      return { w: w, g: grupy[w], s: statyK(grupy[w], wszyscy) };
    }).filter(function (x) { return x.s.nA + x.s.nB > 0; }).sort(function (x, y) { return y.s.nB - x.s.nB || y.s.nA - x.s.nA; });
    if (!KS.wybrane) KS.wybrane = ["__razem"].concat(lista.slice(0, KS.podz ? 4 : 0).map(function (x) { return x.w; }));
    KS.wybrane = KS.wybrane.filter(function (w) { return w === "__razem" || grupy[w]; });
    przydziel(KS);
    if (!tylkoWykres) tabelaK(lista, grupy);
    wykresKoh(grupy);
    if (!tylkoWykres) { rysujMacierz(); rysujKrzywa(); }
    zapiszAdresK();
  }

  function tabelaK(lista, grupy) {
    var B = b(), t = B.wyczysc(B.$("ko-tabela")), okna = K.okna;
    var hr = B.el("tr", null, [B.el("th", { text: KS.podz ? WYMIARY.filter(function (w) { return w.id === KS.podz; })[0].nazwa : "Grupa" }),
      B.el("th", { text: "Nowi pacjenci B (A)" }), B.el("th", { text: "Udział B (A)" })]);
    okna.forEach(function (n) { hr.appendChild(B.el("th", { class: "th-krok", text: "Powrót w " + n + " dniach" })); });
    [90, 180].forEach(function (n) { hr.appendChild(B.el("th", { class: "th-krok", text: "Marża na pacjenta, " + n + " dni" })); });
    t.appendChild(B.el("thead", null, [hr]));
    var tb = B.el("tbody");
    function wiersz(w, g, klasa) {
      var s = statyK(g, grupy.__razem), wybrany = KS.wybrane.indexOf(w) >= 0;
      var kol = wybrany && KS.kolory[w] ? B.css("--series-" + KS.kolory[w]) : "transparent";
      var chk = B.el("input", { type: "checkbox", "aria-label": "Pokaż na wykresie: " + etykietaWart(KS.podz, w) });
      chk.checked = wybrany;
      chk.onchange = function () {
        if (this.checked) { if (KS.wybrane.length >= 8) { this.checked = false; return; } KS.wybrane.push(w); }
        else KS.wybrane = KS.wybrane.filter(function (x) { return x !== w; });
        rysujK();
      };
      var tr = B.el("tr", { class: (klasa || "") + (wybrany ? " zaznaczony" : ""), style: "--kolor:" + kol });
      tr.appendChild(B.el("td", null, [B.el("label", { class: "wiersz-wybor" }, [chk, B.el("span", { class: "kropka", style: "background:" + kol }),
        B.el("span", { text: etykietaWart(KS.podz, w) })])]));
      tr.appendChild(B.el("td", null, [B.el("span", { class: "b", text: B.liczba(s.nB) }), B.el("span", { class: "a", text: "A: " + B.liczba(s.nA) })]));
      tr.appendChild(B.el("td", null, [B.el("span", { class: "b", text: B.proc(s.uB) }), B.el("span", { class: "a", text: "A: " + B.proc(s.uA) })]));
      s.okna.forEach(function (o) { tr.appendChild(o ? komorka(o.pB, o.eB, o.pA, o.eA) : B.el("td", { text: "—" })); });
      [90, 180].forEach(function (n) {
        var o = s.okna[okna.indexOf(n)];
        tr.appendChild(o ? komorka(o.mB, o.eB, o.mA, o.eA, "zł", 1) : B.el("td", { text: "—" }));
      });
      return tr;
    }
    tb.appendChild(wiersz("__razem", grupy.__razem, "podsuma"));
    lista.forEach(function (x) { tb.appendChild(wiersz(x.w, x.g)); });
    t.appendChild(tb);
    var opis = [];
    okna.forEach(function (n) {
      var z = zakresyOkna(n);
      opis.push(n + " dni: " + (z ? "A " + B.dataPL(z.a[0]) + "–" + B.dataPL(z.a[1]) + ", B " + B.dataPL(z.b[0]) + "–" + B.dataPL(z.b[1]) : "brak kohort z pełnym oknem w okresie B"));
    });
    B.$("ko-okresy-opis").textContent = opisOkresow(KS) + " Kohorty z pełnym oknem: " + opis.join("; ") + ".";
  }

  function wykresKoh(grupy) {
    var B = b(), w = KS.wygl, N = B.NDNI, k = K.okna.indexOf(KS.okno), n = KS.okno, ost = N - 1 - n;
    var naz = MIARY_K.filter(function (m) { return m[0] === KS.miara; })[0][1];
    B.$("ko-wykres-tytul").textContent = naz + (KS.miara === "powrot" || KS.miara === "marza" ? " (" + n + " dni)" : "") +
      " według dnia pierwszego zakupu, " + (w === 1 ? "dzień po dniu" : "suma z " + w + " dni kończących się danego dnia");
    var cWsz = krocz(grupy.__razem.cnt, w);
    var serie = KS.wybrane.map(function (wart) {
      var g = grupy[wart], y = new Array(N), c = krocz(g.cnt, w), mian = c, i;
      if (KS.miara === "powrot" || KS.miara === "marza") {
        var l = krocz(KS.miara === "powrot" ? g.ret[k] : g.mar[k], w);
        for (i = 0; i < N; i++) y[i] = i >= w - 1 && i <= ost && c[i] > 0 ? (KS.miara === "powrot" ? 100 : 1) * l[i] / c[i] : null;
      } else if (KS.miara === "nowi") {
        for (i = 0; i < N; i++) y[i] = i >= w - 1 ? c[i] / w : null;
        mian = null;
      } else {
        for (i = 0; i < N; i++) y[i] = i >= w - 1 && cWsz[i] > 0 ? 100 * c[i] / cWsz[i] : null;
        mian = cWsz;
      }
      return { label: etykietaWart(KS.podz, wart), kolor: KS.kolory[wart], y: y,
        opis: function (di, v) {
          if (KS.miara === "nowi") return B.liczba(v, 1) + " dziennie";
          if (KS.miara === "marza") return B.liczba(v, 1) + " zł na pacjenta z " + B.liczba(mian[di]);
          return B.proc(v) + " z " + B.liczba(mian[di]) + (KS.miara === "udzial" ? " w filtrze" : "");
        } };
    });
    if (wykresK) wykresK.destroy();
    var proc = KS.miara === "powrot" || KS.miara === "udzial";
    wykresK = wykres(B.$("ko-wykres"), serie, { procent: proc, jednostka: proc ? "%" : KS.miara === "marza" ? "zł" : "pacjenci",
      formatY: function (v) { return B.liczba(v, 0) + (proc ? "%" : ""); }, a: KS.a, b: KS.b, zdarzenia: true });
  }

  function filtryMacierzy() {
    var B = b(), f = B.wyczysc(B.$("ko-macierz-filtry"));
    f.appendChild(wybor("ko-gran", "Kohorty", [["tydz", "tygodniowe"], ["mies", "miesięczne"]], KS_GRAN,
      function (v) { KS_GRAN = v; rysujMacierz(); }));
  }

  BW.kohorty = {
    pokaz: function (q) {
      var B = b(), cel = B.$("ko-wykres");
      if (!gotoweK) {
        B.akapity(B.$("ko-zdania"), ["Wczytywanie danych kohort…"]);
      }
      B.wczytaj("kohorty", "kohorty").then(function (dane) {
        if (!K) { K = dane; przygotujK(); }
        if (!gotoweK) { B.akapity(B.$("ko-zdania"), K.zdania); gotoweK = true; }
        czytajAdresK(q);
        filtryK();
        filtryMacierzy();
        rysujK();
      }).catch(function (e) { B.akapity(B.$("ko-zdania"), [e.message + ". Odśwież stronę."]); });
    },
    przerysuj: function () { if (K && KS) { rysujK(true); rysujKrzywa(); } }
  };

  // ------------------------------------------------------------ PO ZAKUPIE
  var PZ = null, PS = { spec: "internista", grupa: "pozostale", prog: "p15", wygl: 28,
    zwGrupa: "wszyscy", zwZam: "wszystkie", zwWygl: 28, ocSpec: "internista", ocGrupa: "pozostale",
    opWizyta: "internista_rano", opGrupa: "pozostale" };
  var wykresP = null, wykresZ = null, gotoweP = false;
  var PORY = ["a_rano_6_11", "b_poludnie_12_15", "c_wieczor_16_23", "d_noc_0_5"];
  var CELE = ["l4", "e_recepta", "konsultacja", "skierowanie"];
  var KOSZYKI = ["a_do_5_min", "b_5_15_min", "c_15_30_min", "d_ponad_30_min", "brak_wizyty"];

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
      return { label: ET.pora[pora], kolor: i + 1, y: y, opis: function (di, v) { return B.proc(v) + " z " + B.liczba(m[di]) + " wizyt"; } };
    });
    if (wykresP) wykresP.destroy();
    wykresP = wykres(B.$("pz-wykres"), serie, { procent: true, jednostka: "%", zdarzenia: true, a: zakresOkresu(1), b: zakresOkresu(2) });
    // tabela: specjalizacja × pora, okres 1 wobec okresu 2
    var t = B.wyczysc(B.$("pz-tabela")), o1 = zakresOkresu(1), o2 = zakresOkresu(2);
    t.appendChild(B.el("thead", null, [B.el("tr", null, [B.el("th", { text: "Specjalizacja" }), B.el("th", { text: "Pora terminu" }),
      B.el("th", { text: "Spóźnione " + (PS.prog === "p15" ? "ponad 15" : "ponad 30") + " minut: okres B = " + B.O[1].nazwa + " (A = " + B.O[0].nazwa + ")" })])]));
    var tb = B.el("tbody");
    ["internista", "pediatra", "psychiatra", "inny"].forEach(function (sp) {
      PORY.forEach(function (pora) {
        var s = zsumuj(PZ.punktualnosc, function (x) { return x.pora === pora && x.spec === sp && grupaOk(PS.grupa, x.nowa); }, ["n", PS.prog]);
        var nA = suma(s.n, o1), nB = suma(s.n, o2);
        if (nA + nB === 0) return;
        tb.appendChild(B.el("tr", sp === PS.spec ? { class: "zaznaczony", style: "--kolor:" + B.css("--accent") } : null,
          [B.el("td", { text: ET.spec[sp] }), B.el("td", { text: ET.pora[pora] }),
            komorka(nB ? 100 * suma(s[PS.prog], o2) / nB : null, nB, nA ? 100 * suma(s[PS.prog], o1) / nA : null, nA, "%", 1, true)]));
      });
    });
    t.appendChild(tb);
  }

  var RUCH_GRUPA = "wszyscy";
  function rysujRuch() {
    var B = b(), t = B.wyczysc(B.$("pz-ruch")), stare = RUCH_GRUPA === "pozostale";
    var przedz = [];
    PZ.ruch.forEach(function (r) { if (przedz.indexOf(r.przedzial) < 0) przedz.push(r.przedzial); });
    t.appendChild(B.el("thead", null, [B.el("tr", null, [B.el("th", { text: "Poranne wizyty u internisty w dniu" }),
      B.el("th", { text: "Spóźnione ponad 15 minut: B = " + B.O[1].nazwa + " (A = " + B.O[0].nazwa + ")" }),
      B.el("th", { text: "Dni B (A)" })])]));
    var tb = B.el("tbody");
    przedz.forEach(function (pz) {
      var o = {};
      PZ.ruch.forEach(function (r) { if (r.przedzial === pz) o[r.okres] = r; });
      var f = function (r) { if (!r) return [null, null]; var od = stare ? r.odbyte_stare : r.odbyte, sp = stare ? r.spoznione_stare : r.spoznione; return [od ? 100 * sp / od : null, od]; };
      var a = f(o[1]), bb = f(o[2]);
      tb.appendChild(B.el("tr", null, [B.el("td", { text: pz }), komorka(bb[0], bb[1], a[0], a[1], "%", 1, true),
        B.el("td", null, [B.el("span", { class: "b", text: o[2] ? B.liczba(o[2].dni) : "—" }), B.el("span", { class: "a", text: "A: " + (o[1] ? B.liczba(o[1].dni) : "—") })])]));
    });
    t.appendChild(tb);
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
      B.el("th", { text: "Powrót w 90 dniach: B = kohorty " + B.dataPL(b0) + "–" + B.dataPL(bk) + " (A = " + B.dataPL(a0) + "–" + B.dataPL(ak) + ")" })])]));
    var tb = B.el("tbody");
    KOSZYKI.forEach(function (k) {
      var s = st[k];
      tb.appendChild(B.el("tr", null, [B.el("td", { text: B.ET.koszyk[k] }),
        komorka(s.eB ? 100 * s.rB / s.eB : null, s.eB, s.eA ? 100 * s.rA / s.eA : null, s.eA)]));
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
      return { label: ET.cel[cel], kolor: i + 1, y: y, opis: function (di, v) { return B.proc(v) + " z " + B.liczba(m[di]) + " odbytych"; } };
    });
    if (wykresZ) wykresZ.destroy();
    wykresZ = wykres(B.$("zw-wykres"), serie, { procent: true, jednostka: "%", zdarzenia: true, a: zakresOkresu(1), b: zakresOkresu(2) });
    var t = B.wyczysc(B.$("zw-tabela")), o1 = zakresOkresu(1), o2 = zakresOkresu(2);
    t.appendChild(B.el("thead", null, [B.el("tr", null, ["Cel wizyty", "Zwrot po odbytej wizycie", "Anulowane przed wizytą",
      "Pacjent nie odebrał", "Zwrócone zapłaty B (A)", "Koszt lekarza za zwrócone B (A)"].map(function (h) { return B.el("th", { text: h }); }))]));
    var tb = B.el("tbody");
    CELE.concat([null]).forEach(function (cel) {
      var s = zsumuj(PZ.zwroty, warunek(cel), ["wszystkie", "anul", "nieodebr", "odbyte", "zwrocone", "zw_zl", "kl_zw"]);
      var f = function (licz, mian) { var a = suma(s[mian], o1), bb = suma(s[mian], o2); return komorka(bb ? 100 * suma(s[licz], o2) / bb : null, bb, a ? 100 * suma(s[licz], o1) / a : null, a, "%", 1, true); };
      var zl = function (p) { return B.el("td", null, [B.el("span", { class: "b", text: B.liczba(suma(s[p], o2)) + " zł" }), B.el("span", { class: "a", text: "A: " + B.liczba(suma(s[p], o1)) + " zł" })]); };
      tb.appendChild(B.el("tr", cel ? null : { class: "podsuma" }, [B.el("td", { text: cel ? ET.cel[cel] : "Razem" }),
        f("zwrocone", "odbyte"), f("anul", "wszystkie"), f("nieodebr", "wszystkie"), zl("zw_zl"), zl("kl_zw")]));
    });
    t.appendChild(tb);
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
        komorka(bb.o ? 100 * bb.oc / bb.o : null, bb.o, a.o ? 100 * a.oc / a.o : null, a.o),
        komorka(bb.oc ? bb.s / bb.oc : null, bb.oc, a.oc ? a.s / a.oc : null, a.oc, "", 2),
        komorka(bb.oc ? 100 * bb.ni / bb.oc : null, bb.oc, a.oc ? 100 * a.ni / a.oc : null, a.oc, "%", 1, true)]));
    });
    t.appendChild(tb);
  }

  function filtryP() {
    var B = b(), grupy = [["pozostale", "Spoza nowych kampanii"], ["nowe", "Nowe kampanie na L4"], ["wszyscy", "Wszyscy"]];
    var specy = [["internista", "Internista"], ["pediatra", "Pediatra"], ["psychiatra", "Psychiatra"], ["inny", "Inni specjaliści"], ["wszyscy", "Wszyscy"]];
    var f = B.wyczysc(B.$("pz-filtry"));
    f.appendChild(wybor("pz-spec", "Specjalizacja (wykres)", specy, PS.spec, function (v) { PS.spec = v; rysujPunktualnosc(); }));
    f.appendChild(wybor("pz-grupa", "Pacjenci", grupy, PS.grupa, function (v) { PS.grupa = v; rysujPunktualnosc(); }));
    f.appendChild(wybor("pz-prog", "Opóźnienie", [["p15", "ponad 15 minut"], ["p30", "ponad 30 minut"]], PS.prog, function (v) { PS.prog = v; rysujPunktualnosc(); }));
    f.appendChild(wybor("pz-wygl", "Wygładzenie", [["1", "dzień"], ["7", "suma z 7 dni"], ["28", "suma z 28 dni"]], String(PS.wygl), function (v) { PS.wygl = +v; rysujPunktualnosc(); }));
    var fo = B.wyczysc(B.$("pz-powrot-filtry"));
    fo.appendChild(wybor("pz-op-wizyta", "Pierwsza wizyta", [["internista_rano", "Internista rano (6–11)"], ["internista", "Internista, każda pora"], ["wszystkie", "Wszystkie"]],
      PS.opWizyta, function (v) { PS.opWizyta = v; rysujPowrotOpoznienie(); }));
    fo.appendChild(wybor("pz-op-grupa", "Pacjenci (reguła przyjęta)", grupy, PS.opGrupa, function (v) { PS.opGrupa = v; rysujPowrotOpoznienie(); }));
    var fz = B.wyczysc(B.$("zw-filtry"));
    fz.appendChild(wybor("zw-grupa", "Pacjenci", [["wszyscy", "Wszyscy"], ["nowe", "Nowe kampanie na L4"], ["pozostale", "Spoza nowych kampanii"]],
      PS.zwGrupa, function (v) { PS.zwGrupa = v; rysujZwroty(); }));
    fz.appendChild(wybor("zw-zam", "Zamówienia", [["wszystkie", "Wszystkie"], ["pierwsze", "Pierwsze"], ["kolejne", "Kolejne"]],
      PS.zwZam, function (v) { PS.zwZam = v; rysujZwroty(); }));
    fz.appendChild(wybor("zw-wygl", "Wygładzenie", [["1", "dzień"], ["7", "suma z 7 dni"], ["28", "suma z 28 dni"]], String(PS.zwWygl), function (v) { PS.zwWygl = +v; rysujZwroty(); }));
    var fc = B.wyczysc(B.$("oc-filtry"));
    fc.appendChild(wybor("oc-spec", "Specjalizacja", specy, PS.ocSpec, function (v) { PS.ocSpec = v; rysujOceny(); }));
    fc.appendChild(wybor("oc-grupa", "Pacjenci", grupy, PS.ocGrupa, function (v) { PS.ocGrupa = v; rysujOceny(); }));
  }

  BW["po-zakupie"] = {
    pokaz: function () {
      var B = b();
      B.wczytaj("po_zakupie", "po_zakupie").then(function (dane) {
        PZ = dane;
        if (!gotoweP) {
          B.akapity(B.$("pz-zdania"), PZ.zdania_punktualnosc);
          B.akapity(B.$("pz-ruch-zdania"), PZ.zdania_ruch);
          var fr = B.wyczysc(B.$("pz-ruch-filtry"));
          fr.appendChild(wybor("pz-ruch-grupa", "Pacjenci", [["wszyscy", "Wszyscy"], ["pozostale", "Spoza nowych kampanii"]], RUCH_GRUPA,
            function (v) { RUCH_GRUPA = v; rysujRuch(); }));
          B.akapity(B.$("zw-zdania"), PZ.zdania_zwroty);
          B.akapity(B.$("oc-zdania"), PZ.zdania_oceny);
          filtryP(); gotoweP = true;
        }
        rysujPunktualnosc(); rysujRuch(); rysujZwroty(); rysujOceny(); rysujPowrotOpoznienie();
        return B.wczytaj("kohorty", "kohorty");
      }).then(function (dane) {
        if (!K) { K = dane; przygotujK(); }
        rysujPowrotOpoznienie();
      }).catch(function (e) { B.akapity(B.$("pz-zdania"), [e.message + ". Odśwież stronę."]); });
    },
    przerysuj: function () { if (PZ) { rysujPunktualnosc(); rysujZwroty(); } }
  };

  // ------------------------------------------------------------ WYNIK BIZNESU
  var WY = null, WS = { krok: "mies", poziom: "grupa", okres: 2 }, wykresW = null, gotoweW = false;

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
  function skladowe(g) {
    var S = WY.serie;
    var prz = sumaOkresu(S.przychod_pierwsze, g) + sumaOkresu(S.przychod_powtorne, g), go = sumaOkresu(S.go, g),
      kl = sumaOkresu(S.koszt_lekarza, g), kamp = sumaOkresu(S.wydatki_google, g) + sumaOkresu(S.wydatki_meta, g) + sumaOkresu(S.wydatki_tiktok, g),
      pr = sumaOkresu(S.prowizja, g);
    return { prz: prz, prz1: sumaOkresu(S.przychod_pierwsze, g), prz2: sumaOkresu(S.przychod_powtorne, g), go: go, kl: kl, kamp: kamp, pr: pr,
      marza: prz + go - kl - kamp - pr, zam: sumaOkresu(S.zamowienia, g), nowi: sumaOkresu(S.nowi, g) };
  }
  function rysujWynik() {
    var B = b(), gr = okresy(WS.krok);
    var x = new Float64Array(gr.length), cz = { prz: [], kl: [], kamp: [], marza: [] };
    gr.forEach(function (g, i) {
      x[i] = (B.START + g.od * B.DZIEN) / 1000;
      var s = skladowe(g);
      cz.prz.push(s.prz + s.go); cz.kl.push(s.kl); cz.kamp.push(s.kamp + s.pr); cz.marza.push(s.marza);
    });
    var f = function (v) { return B.liczba(v) + " zł"; };
    var serie = [
      { label: "Przychód (konsultacje po zwrotach i TelemediGO)", kolor: 1, y: cz.prz, opis: function (di, v) { return f(v); } },
      { label: "Koszt lekarza", kolor: 2, y: cz.kl, opis: function (di, v) { return f(v); } },
      { label: "Kampanie i prowizja afiliacyjna", kolor: 4, y: cz.kamp, opis: function (di, v) { return f(v); } },
      { label: "Marża", kolor: 3, y: cz.marza, opis: function (di, v) { return f(v); } }
    ];
    if (wykresW) wykresW.destroy();
    var et = function (u, ts) {
      if (ts == null) return "—";
      var i = Math.round((ts * 1000 - B.START) / B.DZIEN), g = gr.filter(function (q) { return q.od === i; })[0];
      return g ? B.dataPL(g.od) + (g.do > g.od ? "–" + B.dataPL(g.do) : "") : B.dataPL(i);
    };
    wykresW = wykres(B.$("wy-wykres"), serie, { x: x, procent: false, jednostka: "zł", punkty: WS.krok === "mies", etykietaX: et, zdarzenia: true,
      formatY: function (v) { return Math.abs(v) >= 1000 ? B.liczba(v / 1000, 0) + " tys." : B.liczba(v, 0); } });
    // tabela miesięczna z sumami okresów
    var t = B.wyczysc(B.$("wy-tabela"));
    var kol = [["Okres", null], ["Zamówienia", "zam"], ["Nowi pacjenci", "nowi"], ["Przychód: pierwsze zamówienia", "prz1"],
      ["Przychód: kolejne zamówienia", "prz2"], ["TelemediGO", "go"], ["Koszt lekarza", "kl"], ["Kampanie", "kamp"],
      ["Prowizja afiliacyjna", "pr"], ["Marża", "marza"]];
    t.appendChild(B.el("thead", null, [B.el("tr", null, kol.map(function (k) { return B.el("th", { text: k[0] + (k[1] && k[1] !== "zam" && k[1] !== "nowi" ? " (zł)" : "") }); }))]));
    var tb = B.el("tbody");
    var O = B.O, okr = [{ nazwa: "Okres " + O[0].nazwa, od: B.idxIso(O[0].od), do: B.idxIso(O[0].do) },
      { nazwa: "Okres " + O[1].nazwa, od: B.idxIso(O[1].od), do: B.idxIso(O[1].do) }];
    var s1 = skladowe(okr[0]), s2 = skladowe(okr[1]);
    okr.forEach(function (o, j) {
      var s = j ? s2 : s1;
      tb.appendChild(B.el("tr", { class: "podsuma" }, kol.map(function (k) { return B.el("td", { text: k[1] ? B.liczba(s[k[1]]) : o.nazwa }); })));
    });
    tb.appendChild(B.el("tr", { class: "podsuma" }, kol.map(function (k) {
      return B.el("td", { text: k[1] ? (s1[k[1]] ? B.znak(100 * (s2[k[1]] / s1[k[1]] - 1), 1) + "%" : "—") : "Zmiana okres 2 wobec 1" });
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

  function rysujKwartaly() {
    var B = b(), t = B.wyczysc(B.$("wy-kwartaly")), O = B.O, i2 = B.idxIso(O[1].od), N = B.NDNI;
    var kol = [["Marża", "marza"], ["Wydatki na kampanie", "kamp"], ["Przychód: konsultacje po zwrotach i TelemediGO", "przgo"],
      ["Koszt lekarza", "kl"], ["Nowi pacjenci", "nowi"]];
    t.appendChild(B.el("thead", null, [B.el("tr", null, [B.el("th", { text: "Kwartał (B) wobec tego samego kwartału rok wcześniej (A)" })]
      .concat(kol.map(function (k) { return B.el("th", { text: k[0] }); })))]));
    var tb = B.el("tbody");
    var i = i2;
    while (i < N) {
      var d = new Date(B.START + i * B.DZIEN), m = d.getUTCMonth(), y = d.getUTCFullYear();
      var dk = new Date(Date.UTC(y, m + 3, 1)), k = Math.min(N - 1, Math.round((dk.getTime() - B.START) / B.DZIEN) - 1);
      var dp = new Date(Date.UTC(y - 1, m, 1)), dpk = new Date(Date.UTC(y - 1, m + 3, 1));
      var ip = Math.round((dp.getTime() - B.START) / B.DZIEN), kp = Math.round((dpk.getTime() - B.START) / B.DZIEN) - 1;
      var sB = skladowe({ od: i, do: k }), sA = skladowe({ od: ip, do: kp });
      sB.przgo = sB.prz + sB.go; sA.przgo = sA.prz + sA.go; sB.kamp += 0; sA.kamp += 0;
      var tr = B.el("tr", null, [B.el("td", { text: B.RZYM[Math.floor(m / 3)] + " kw. " + y + " wobec " + B.RZYM[Math.floor(m / 3)] + " kw. " + (y - 1) })]);
      kol.forEach(function (kk) {
        var a = sA[kk[1]], bb = sB[kk[1]], zm = a ? 100 * (bb / a - 1) : null, zl = kk[1] !== "nowi";
        var lepiej = kk[1] === "kamp" || kk[1] === "kl" ? zm < 0 : zm > 0;
        tr.appendChild(B.el("td", null, [B.el("span", { class: "b", text: B.liczba(bb) + (zl ? " zł" : "") }),
          B.el("span", { class: "a", text: "A: " + B.liczba(a) + (zl ? " zł" : "") + " " }, [B.el("span", {
            class: "delta " + (lepiej ? "plus" : "minus"), text: (zm >= 0 ? "▲" : "▼") + B.liczba(Math.abs(zm), 1) + "%" })])]));
      });
      tb.appendChild(tr);
      i = k + 1;
    }
    t.appendChild(tb);
  }

  function rysujEkonomie() {
    var B = b(), ET = B.ET, w = WY.ekonomia.wiersze.filter(function (r) { return r.poziom === WS.poziom && r.okres === WS.okres; });
    var klucze = [];
    w.forEach(function (r) { if (klucze.indexOf(r.klucz) < 0) klucze.push(r.klucz); });
    var znajdz = function (k, reg, okno) { return w.filter(function (r) { return r.klucz === k && r.regula === reg && r.okno === okno; })[0]; };
    var t = B.wyczysc(B.$("ek-tabela"));
    var h1 = B.el("tr", null, [B.el("th", { text: WS.poziom === "grupa" ? "Grupa" : WS.poziom === "kanal" ? "Kanał" : "Kampania" }),
      B.el("th", { text: "Przyjęta reguła źródła", colspan: 4, style: "text-align:center" }),
      B.el("th", { text: "Sesja płatności", colspan: 4, style: "text-align:center" }), B.el("th", { text: "" })]);
    var h2 = B.el("tr", null, [B.el("th", { text: "" })]);
    [0, 1].forEach(function () {
      ["Nowi pacjenci", "Koszt pozyskania na pacjenta", "Wynik na pacjenta, 90 dni", "Wynik na pacjenta, 180 dni"].forEach(function (x) { h2.appendChild(B.el("th", { text: x })); });
    });
    h2.appendChild(B.el("th", { text: "Ocena" }));
    t.appendChild(B.el("thead", null, [h1, h2]));
    var tb = B.el("tbody");
    var et = function (k) { return WS.poziom === "grupa" ? (ET.grupa_ek[k] || k) : WS.poziom === "kanal" ? (ET.kanal[k] || k) : (ET.kampania[k] || k); };
    var zl = function (v) { return (v > 0 ? "+" : "") + B.liczba(v, 1) + " zł"; };
    klucze.forEach(function (k) {
      var tr = B.el("tr", null, [B.el("td", { text: et(k) })]), znaki = {};
      ["Z1K", "Z2"].forEach(function (reg) {
        var r90 = znajdz(k, reg, 90), r180 = znajdz(k, reg, 180);
        tr.appendChild(B.el("td", { text: r90 ? B.liczba(r90.nowi) : "—" }));
        tr.appendChild(B.el("td", { text: r90 ? B.liczba(r90.cac, 1) + " zł" : "—" }));
        [r90, r180].forEach(function (r, j) {
          if (!r) { tr.appendChild(B.el("td", { text: "—" })); return; }
          znaki[reg + j] = r.wynik >= 0;
          tr.appendChild(B.el("td", { class: "", title: "Przedział warunkowy " + B.liczba(r.od, 1) + "–" + B.liczba(r.do, 1) + " zł. Powrót: " + B.liczba(r.powrot, 1) + "%." },
            [B.el("span", { class: "b delta " + (r.wynik >= 0 ? "plus" : "minus"), text: zl(r.wynik) }),
              B.el("span", { class: "a", text: "marża " + B.liczba(r.marza, 1) + " zł, " + B.liczba(r.nowi) + " pac." })]));
        });
      });
      var niepewne = (znaki.Z1K0 !== undefined && znaki.Z20 !== undefined && znaki.Z1K0 !== znaki.Z20) ||
        (znaki.Z1K1 !== undefined && znaki.Z21 !== undefined && znaki.Z1K1 !== znaki.Z21);
      tr.appendChild(B.el("td", { text: niepewne ? "niepewny: znak zależy od reguły" : "" }));
      tb.appendChild(tr);
    });
    t.appendChild(tb);
  }

  BW.wynik = {
    pokaz: function () {
      var B = b();
      B.wczytaj("wynik", "wynik").then(function (dane) {
        WY = dane;
        if (!gotoweW) {
          B.akapity(B.$("wy-zdania"), WY.zdania);
          B.akapity(B.$("ek-zdania"), WY.ekonomia.zdania);
          var f = B.wyczysc(B.$("wy-filtry"));
          f.appendChild(wybor("wy-krok", "Grupowanie", [["mies", "miesiące"], ["tydz", "tygodnie"], ["dzien", "dni"]], WS.krok,
            function (v) { WS.krok = v; rysujWynik(); }));
          var fe = B.wyczysc(B.$("ek-filtry"));
          fe.appendChild(wybor("ek-poziom", "Poziom", [["grupa", "Grupy kampanii"], ["kampania", "Kampanie"], ["kanal", "Kanały"]], WS.poziom,
            function (v) { WS.poziom = v; rysujEkonomie(); }));
          fe.appendChild(wybor("ek-okres", "Okres", [["2", "Okres " + B.O[1].nazwa], ["1", "Okres " + B.O[0].nazwa]], String(WS.okres),
            function (v) { WS.okres = +v; rysujEkonomie(); }));
          gotoweW = true;
        }
        rysujWynik(); rysujEkonomie();
      }).catch(function (e) { B.akapity(B.$("wy-zdania"), [e.message + ". Odśwież stronę."]); });
    },
    przerysuj: function () { if (WY) rysujWynik(); }
  };
})();
