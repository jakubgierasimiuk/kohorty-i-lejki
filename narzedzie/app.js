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
      zero ? "Bez zmiany " + wobec : (d > 0 ? "Wzrost" : "Spadek") + " o " + liczba(Math.abs(d), m) + " " + wobec,
      { slowo: !o.bezSlowa });
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
  var MIARY_MOSTKA = [["nowi", "Nowi pacjenci"], ["zamowienia", "Zamówienia"], ["przychod", "Przychód z konsultacji"], ["go", "TelemediGO"]];
  // „wartość rok wcześniej → wartość w ostatnich 12 miesiącach”, jak pod zmianą w tabeli mostka
  function wartMostka(miara, v) {
    return miara === "przychod" ? liczba(v.p1 / 1e6, 3) + " → " + liczba(v.p2 / 1e6, 3) + " mln zł" : liczba(v.p1) + " → " + liczba(v.p2);
  }
  function mostek(tabela) {
    var M = JK.mostek.kroki, miary = MIARY_MOSTKA;
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
        r.appendChild(el("td", null, [el("strong", { text: znak(v.wzrost, 1) + "%" }), el("br"),
          el("span", { class: "przypis", text: wartMostka(m[0], v) })]));
      });
      tb.appendChild(r);
    });
    tabela.appendChild(tb);
  }
  // Schodki mostka: wzrost rok do roku zamówień i przychodu z konsultacji po każdym kroku (te same liczby i ten sam zapis
  // co w tabeli mostka). Nowi pacjenci i TelemediGO zostają w tabeli: w mostku prawie się nie zmieniają.
  function schodkiMostka() {
    var M = JK.mostek && JK.mostek.kroki;
    if (!M || !M.length) return null;
    var miary = MIARY_MOSTKA.filter(function (m) { return m[0] === "zamowienia" || m[0] === "przychod"; }), mx = 0;
    var dane = miary.map(function (m) {
      return { nazwa: m[1], kroki: M.map(function (k, i) {
        var v = k.miary[m[0]], poprz = i > 0 ? M[i - 1].miary[m[0]] : null;
        mx = Math.max(mx, v.wzrost);
        return { etykieta: k.opis, v: v.wzrost, tekst: znak(v.wzrost, 1) + "%", bezZmian: !!(poprz && poprz.p1 === v.p1 && poprz.p2 === v.p2),
          tytul: m[1] + ", " + k.opis + ": " + znak(v.wzrost, 1) + "% rok do roku (" + wartMostka(m[0], v) + ")" };
      }) };
    });
    var s = BK.podzialka(0, mx, 7);
    return BK.schodki({ miary: dane, max: s.max, os: s.wartosci.map(function (v) { return liczba(v, 0) + "%"; }),
      legenda: [{ klasa: "pkt kw pkt-a", nazwa: M[0].opis }, { klasa: "pkt kw pkt-b", nazwa: "po kolejnych krokach oczyszczenia" },
        { klasa: "sch-kreska-wzor", nazwa: "poziom z dashboardu" }],
      opis: "Wzrost zamówień i przychodu z konsultacji rok do roku po każdym kroku od dashboardu do danych oczyszczonych",
      przypis: "Wzrost: ostatnie 12 miesięcy (" + P.meta.okresy[1].nazwa + ") wobec roku wcześniej (" + P.meta.okresy[0].nazwa +
        "). Każdy słupek to poziom po danym kroku, liczony od zera, a nie różnica między krokami." });
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

  // kolor idzie za grupą, nie za kolejnością zaznaczenia: każda wartość ma stałe miejsce w palecie (ranking po liczbie
  // wszystkich sesji w pliku podziału, niezależny od filtrów i okresów); „Razem” to seria odniesienia w kolorze tuszu
  var rankingi = {};
  function rankingWartosci(dane) {
    if (rankingi[S.podz]) return rankingi[S.podz];
    var suma_ = {};
    dane.serie.forEach(function (s) { var t = 0; for (var i = 0; i < s.s.length; i++) t += s.s[i]; suma_[s.w] = (suma_[s.w] || 0) + t; });
    var r = {};
    Object.keys(suma_).sort(function (a, c) { return suma_[c] - suma_[a] || (a < c ? -1 : 1); }).forEach(function (w, i) { r[w] = i; });
    return (rankingi[S.podz] = r);
  }
  function przydzielKolory(dane) {
    var rank = rankingWartosci(dane), zajete = {};
    S.kolory = {};
    S.wybrane.slice().sort(function (a, c) { return (rank[a] === undefined ? 99 : rank[a]) - (rank[c] === undefined ? 99 : rank[c]); })
      .forEach(function (w) {
        if (w === "__razem") { S.kolory[w] = "--seria-ref"; return; }
        var start = (rank[w] || 0) % 8;
        for (var k = 0; k < 8; k++) { var i = (start + k) % 8 + 1; if (!zajete[i]) { S.kolory[w] = "--series-" + i; zajete[i] = true; return; } }
        S.kolory[w] = "--seria-ref";
      });
  }

  // Safari na iPhone'ach: krok konta po wyborze terminu przed awarią i po niej, obok pozostałe przeglądarki (hantle);
  // oba wiersze na tych samych oknach: 60 dni przed awarią i 60 dni po niej (runda F, poprawka 5)
  function hantleSafari() {
    var s = P.lejek_naglowek && P.lejek_naglowek.safari;
    if (!s || s.przed_proc === undefined || s.po60_proc === undefined) return null;
    var po = s.po60_proc;
    function wiersz(et, a, b, zla) {
      var d = Math.round(b) - Math.round(a);   // różnica liczb pokazanych (całe procenty, jak w tekście karty)
      return { etykieta: et, a: a, b: b, tekstA: proc(a, 0), tekstB: proc(b, 0),
        zmiana: { tekst: znak(d, 0) + " pkt proc.", kierunek: BK.kierunekZnaku(d), stan: zla ? "zle" : "neutralnie",
          tytul: (d < 0 ? "Spadek" : "Wzrost") + " o " + liczba(Math.abs(d), 1) + " pkt proc." } };
    }
    return BK.hantle({ nazwy: { a: "przed awarią", b: "po awarii" }, kodowanie: "okresy", min: 0, max: 80, os: ["0%", "20%", "40%", "60%", "80%"],
      opis: "Krok konta po wyborze terminu, osoby, które jeszcze nie kupowały: Safari na iPhone'ach i pozostałe przeglądarki przed awarią i po niej",
      wiersze: [wiersz("Safari na iPhone'ach", s.przed_proc, po, true), wiersz("Pozostałe przeglądarki", s.reszta_przed_proc, s.reszta_po60_proc, false)],
      przypis: "Odsetek sesji po wyborze terminu, które przechodzą przez krok konta, w obu wierszach w tych samych dniach. Przed awarią: " +
        dataPL(idxIso(s.przed[0])) + "–" + dataPL(idxIso(s.przed[1])) + ". Po awarii: " + dataPL(idxIso(s.po60[0])) + "–" + dataPL(idxIso(s.po60[1])) + "." +
        (s.po_proc !== undefined ? " Do końca danych krok w Safari nie wraca: " + proc(s.po_proc, 1) + " od " + dataPL(idxIso(s.data)) + " do " + dataPL(NDNI - 1) + "." : "") });
  }
  // przeglądarki w aplikacjach wobec zwykłych przeglądarek w tych samych warunkach (ta sama kampania i grupa osób)
  function hantlePrzegladarek(W) {
    if (!W || !W.wiersze || !W.wiersze.length) return null;
    var wiersze = [], byloL4 = false;
    W.wiersze.forEach(function (r) {
      if (r.rodzaj === "nowe_osoby" && !byloL4) { wiersze.push({ podtytul: true, etykieta: "Dla porównania: kampanie na L4, które trafiają do nowych osób" }); byloL4 = true; }
      var a = r.zwykla_w_tych_samych_warunkach.proc, b = r.w_aplikacji.proc, d = r.roznica_pkt;
      wiersze.push({ etykieta: r.kampania, a: a, b: b, tekstA: proc(a, 1), tekstB: proc(b, 1),
        tytul: r.kampania + ": w aplikacji " + proc(b, 1) + " z " + liczba(r.w_aplikacji.sesje) + " sesji, zwykłe przeglądarki w tych samych warunkach " + proc(a, 1) +
          (r.od_pkt !== undefined ? "; różnica " + znak(d, 1) + " pkt proc. (przedział " + znak(r.od_pkt, 1) + " do " + znak(r.do_pkt, 1) + ")" : ""),
        zmiana: { tekst: znak(d, 1) + " pkt proc.", kierunek: BK.kierunekZnaku(d), stan: "neutralnie" } });
    });
    return BK.hantle({ nazwy: { a: "zwykłe przeglądarki w tych samych warunkach", b: "przeglądarka w aplikacji" }, kodowanie: "grupy",
      min: 0, max: 30, os: ["0%", "10%", "20%", "30%"], wiersze: wiersze,
      opis: "Odsetek sesji zakończonych płatnością w przeglądarkach w aplikacjach i w zwykłych przeglądarkach w tych samych warunkach",
      przypis: "Odsetek sesji zakończonych płatnością, " + (W.okres || "ostatnie 12 miesięcy") + ". Zwykłe przeglądarki „w tych samych warunkach”: odsetek, jaki miałyby te same sesje przy konwersji zwykłych przeglądarek w tej samej kampanii i tej samej grupie osób." });
  }

  function rysujNaglowekLejka() {
    var N = P.lejek_naglowek;
    zdaniaAlboKarta($("lj-naglowek"), $("lj-zdania"), N.karta, N.zdania);
    var n = wyczysc($("lj-naprawy"));
    if (N.naprawy_karty && N.naprawy_karty.length) {
      N.naprawy_karty.forEach(function (k, i) {
        var a = BK.karta(k, { prefiks: "lj-" });
        n.appendChild(a);
        // wykresy w kartach napraw: Safari (pierwsza karta) i przeglądarki w aplikacjach (karta z polem wykres)
        if (k.wykres) BK.wstawWykres(a, hantlePrzegladarek(k.wykres));
        else if (i === 0) BK.wstawWykres(a, hantleSafari());
      });
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
      wczytajPodzial(S.podz).then(function (dane) { rysujKrokiLejka(dane); rysujWykresLejka(dane); zapiszAdres(); });
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
    // „z” i liczba sklejone twardą spacją, żeby na wąskim ekranie nie rozdzielał ich koniec wiersza
    td.appendChild(el("span", { class: "n", text: " z " + liczba(mB) }));
    var a = el("span", { class: "a", text: "A: " + proc(pA) + " z " + liczba(mA) });
    if (pA !== null && pB !== null) a.appendChild(zmianaPkt(pB - pA, 1, false, { bezSlowa: true }));
    td.appendChild(a);
    return td;
  }

  // tabela podziałów na telefonie: widoczne kolumny stałe i jedna wybrana miara; całą tabelę pokazuje przycisk
  var KOLUMNA_TEL = {};
  function tabelaTelefon(t, id, stale, domyslna) {
    var ramka = t.closest(".tabela-ramka"), th = t.querySelectorAll("thead tr:last-child th"), miary = [];
    Array.prototype.forEach.call(th, function (h, i) { if (stale.indexOf(i) < 0) miary.push([i, h.textContent]); });
    var wyb = KOLUMNA_TEL[id] !== undefined ? KOLUMNA_TEL[id] : domyslna;
    function ustaw() {
      Array.prototype.forEach.call(t.rows, function (r) {
        Array.prototype.forEach.call(r.cells, function (c, i) { c.classList.toggle("kol-tel-ukryta", stale.indexOf(i) < 0 && i !== wyb); });
      });
    }
    ustaw();
    var stary = ramka.previousElementSibling;
    if (stary && stary.classList.contains("tabela-tel")) stary.parentNode.removeChild(stary);
    var sel = el("select", { "aria-label": "Miara w tabeli" }, miary.map(function (m) { return el("option", { value: String(m[0]), text: m[1] }); }));
    sel.value = String(wyb);
    sel.onchange = function () { wyb = KOLUMNA_TEL[id] = +this.value; ustaw(); };
    var btn = el("button", { type: "button", class: "przycisk-maly", text: t.classList.contains("cala-tabela") ? "Pokaż jedną miarę" : "Pokaż całą tabelę" });
    btn.onclick = function () { var c = t.classList.toggle("cala-tabela"); btn.textContent = c ? "Pokaż jedną miarę" : "Pokaż całą tabelę"; };
    ramka.parentNode.insertBefore(el("div", { class: "tabela-tel" }, [el("label", null, ["Miara w tabeli", sel]), btn]), ramka);
  }

  // ------------------------------------------------------------ wykres kroków lejka (liczony z tych samych danych co tabela)
  var KROKI_LEJKA = [
    { pole: "s", nazwa: "Wejście na stronę" }, { pole: "k1", nazwa: ET.kroki.k1 }, { pole: "k2", nazwa: ET.kroki.k2 },
    { pole: "k3", nazwa: ET.kroki.k3 }, { pole: "k4", nazwa: ET.kroki.k4 }, { pole: "k5", nazwa: ET.kroki.k5 }
  ];
  // nazwy okresów porównania; aD to forma po „wobec”
  function nazwyPresetu(p) {
    if (p === "rok") return { b: "Ostatnie 12 miesięcy", a: "rok wcześniej", aD: "roku wcześniej" };
    if (p === "30rr") return { b: "Ostatnie 30 dni", a: "te same dni rok wcześniej", aD: "tych samych dni rok wcześniej" };
    if (p === "90") return { b: "Ostatnie 90 dni", a: "poprzednie 90 dni", aD: "poprzednich 90 dni" };
    if (p && p.indexOf("zd:") === 0) return { b: "Po zdarzeniu", a: "przed zdarzeniem", aD: "okresu przed zdarzeniem" };
    return { b: "Okres B", a: "okres A", aD: "okresu A" };
  }
  function nazwyOkresow() { return nazwyPresetu(S.preset); }
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
          gorsze ? BK.znacznik({ tekst: "Najbardziej obniża płatności", stan: "zle" }) : null]);
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
    if (!S.wybrane) S.wybrane = S.podz === "calosc" ? ["__razem"] : lista.slice(0, 4).map(function (x) { return x.w; });
    if (S.podz === "calosc") S.wybrane = S.wybrane.map(function (w) { return w === "calosc" ? "__razem" : w; });
    S.wybrane = S.wybrane.filter(function (w) { return w === "__razem" || lista.some(function (x) { return x.w === w; }); });
    przydzielKolory(dane);

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
      var kol = wybrany && S.kolory[w] ? css(S.kolory[w]) : "transparent";
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
    BK.legendaZmian($("lj-legenda-zmian"), "wobec okresu A, w punktach procentowych");
    tabelaTelefon(t, "lejek", [0, 1], 8);
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

  // pionowe linie zdarzeń z numerami jak na osi zdarzeń; bliskie numery schodzą do drugiego i trzeciego rzędu,
  // na wąskim wykresie (telefon) same linie bez numerów (nazwy są w liście pod wykresem)
  function rysujZdarzeniaNaWykresie(u, zdarzenia) {
    var ctx = u.ctx, top = u.bbox.top, h = u.bbox.height, dpr = window.devicePixelRatio || 1, waskie = u.bbox.width < 500 * dpr;
    var rzedy = [-1e9, -1e9, -1e9];
    ctx.save();
    ctx.lineWidth = 1 * dpr; ctx.font = (11 * dpr) + "px system-ui"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    zdarzenia.map(function (z) { return { z: z, x: u.valToPos((START + idxIso(z.od) * DZIEN) / 1000, "x", true) }; })
      .filter(function (p) { return p.x >= u.bbox.left && p.x <= u.bbox.left + u.bbox.width; })
      .sort(function (a, c) { return a.x - c.x; })
      .forEach(function (p) {
        var r = 0;
        while (r < rzedy.length - 1 && p.x - rzedy[r] < 16 * dpr) r++;
        rzedy[r] = p.x;
        ctx.globalAlpha = 0.5; ctx.strokeStyle = css("--muted");
        ctx.beginPath(); ctx.moveTo(Math.round(p.x) + 0.5, top + (waskie ? 0 : 8 * dpr)); ctx.lineTo(Math.round(p.x) + 0.5, top + h); ctx.stroke();
        ctx.globalAlpha = 1;
        if (waskie) return;
        var t = String(p.z.nr), y = top + (8 + r * 14) * dpr, sz = ctx.measureText(t).width + 6 * dpr;
        ctx.fillStyle = css("--surface"); ctx.fillRect(p.x - sz / 2, y - 6.5 * dpr, sz, 13 * dpr);
        ctx.fillStyle = css("--ink-2"); ctx.fillText(t, p.x, y);
      });
    ctx.restore();
  }

  // ------------------------------------------------------------ legenda wykresów dziennych (zamiast domyślnej legendy uPlot)
  // Zdarzenia na wykresie: domyślnie tylko z obszaru wykresu (np. „Lejek”), przełącznik pokazuje wszystkie.
  var ZD_WSZYSTKIE = {};
  function zdarzeniaWykresu(id, obszary) {
    var zd = zdarzeniaNumerowane();
    if (!obszary || ZD_WSZYSTKIE[id]) return zd;
    return zd.filter(function (z) { return obszary.indexOf(z.obszar) >= 0; });
  }
  // Dopisuje do opcji uPlot własną legendę i podpisy końców linii; zwraca funkcję, która po utworzeniu wykresu rysuje legendę.
  // o: {id, serie: [{label, kolor, w, gruba, wart(v, i)}], etykietaX(x), obszary, zdarzenia, koncowe, odswiez(),
  //     wybor: {dostepne: [[w, nazwa]], wybrane: [w], max, dodaj(w), usun(w)}}
  function legendaUplot(opts, cel, o) {
    var waskie = (cel.clientWidth || 300) < 600, wart = [], data = null;
    var PUSTE = waskie ? "Dotknij wykresu, żeby zobaczyć wartości." : "Najedź na wykres, żeby zobaczyć wartości.";
    opts.legend = { show: false };
    opts.hooks = opts.hooks || {};
    (opts.hooks.setCursor = opts.hooks.setCursor || []).push(function (u) {
      if (!data) return;
      var i = u.cursor.idx;
      if (i === null || i === undefined) { data.textContent = PUSTE; wart.forEach(function (w) { w.textContent = ""; }); return; }
      data.textContent = o.etykietaX(u.data[0][i]);
      o.serie.forEach(function (s, k) { var v = u.data[k + 1][i]; wart[k].textContent = v === null || v === undefined ? "—" : s.wart(v, i); });
    });
    if (o.koncowe && !waskie && o.serie.length <= 4) {
      opts.padding = [8, 160, 0, 0];
      (opts.hooks.draw = opts.hooks.draw || []).push(function (u) { podpisyKoncowe(u, o.serie); });
    }
    return function () {
      var box = el("div", { class: "lw" });
      data = el("div", { class: "lw-data", text: PUSTE });
      box.appendChild(data);
      var lista = el("div", { class: "lw-serie" });
      o.serie.forEach(function (s, k) {
        wart[k] = el("span", { class: "lw-wart" });
        var usun = null;
        if (o.wybor && o.wybor.wybrane.length > 1 && s.w !== undefined) {
          usun = el("button", { type: "button", class: "lw-usun", "aria-label": "Usuń z wykresu: " + s.label, title: "Usuń z wykresu" }, ["×"]);
          usun.onclick = function () { o.wybor.usun(s.w); };
        }
        lista.appendChild(el("span", { class: "lw-seria" }, [el("span", { class: "lw-kreska" + (s.gruba ? " gruba" : ""), style: "background:" + s.kolor }),
          el("span", { class: "lw-nazwa", text: s.label }), wart[k], usun]));
      });
      if (o.wybor) {
        var reszta = o.wybor.dostepne.filter(function (x) { return o.wybor.wybrane.indexOf(x[0]) < 0; });
        if (reszta.length && o.wybor.wybrane.length < (o.wybor.max || 8)) {
          var sel = el("select", { class: "lw-dodaj", "aria-label": "Dodaj serię do wykresu" }, [el("option", { value: "", text: "+ Dodaj serię" })].concat(
            reszta.map(function (x) { return el("option", { value: x[0], text: x[1] }); })));
          sel.onchange = function () { if (this.value) o.wybor.dodaj(this.value); };
          lista.appendChild(sel);
        }
      }
      box.appendChild(lista);
      if (o.zdarzenia) {
        var stopka = el("div", { class: "lw-zdarzenia" });
        if (o.zdarzenia.length) stopka.appendChild(el("ol", { class: "lista-zdarzen-wykres" }, o.zdarzenia.map(function (z) {
          return el("li", { value: String(z.nr) }, [el("a", { href: "#zdarzenia?z=" + z.id, text: dataPL(idxIso(z.od)) + ": " + (z.krotko || z.tytul) })]);
        })));
        if (o.obszary) {
          var chk = el("input", { type: "checkbox" });
          chk.checked = !!ZD_WSZYSTKIE[o.id];
          chk.onchange = function () { ZD_WSZYSTKIE[o.id] = this.checked; o.odswiez(); };
          stopka.appendChild(el("label", { class: "chip lw-wszystkie" }, [chk, "Zdarzenia ze wszystkich obszarów (" + zdarzeniaNumerowane().length + ")"]));
        }
        box.appendChild(stopka);
      }
      cel.appendChild(box);
    };
  }
  // podpisy na końcach linii (do czterech serii, nie na telefonie): kreska w kolorze serii i nazwa w kolorze tekstu
  function podpisyKoncowe(u, serie) {
    var ctx = u.ctx, dpr = window.devicePixelRatio || 1, xmax = u.scales.x.max, pozy = [];
    serie.forEach(function (s, k) {
      var d = u.data[k + 1], x = u.data[0];
      for (var i = d.length - 1; i >= 0; i--) if (d[i] !== null && d[i] !== undefined && x[i] <= xmax) { pozy.push({ y: u.valToPos(d[i], "y", true), s: s }); return; }
    });
    pozy.sort(function (a, c) { return a.y - c.y; });
    for (var j = 1; j < pozy.length; j++) if (pozy[j].y - pozy[j - 1].y < 15 * dpr) pozy[j].y = pozy[j - 1].y + 15 * dpr;
    var x0 = u.bbox.left + u.bbox.width + 8 * dpr;
    ctx.save();
    ctx.font = (12 * dpr) + "px system-ui"; ctx.textBaseline = "middle"; ctx.textAlign = "left";
    pozy.forEach(function (p) {
      ctx.fillStyle = p.s.kolor; ctx.fillRect(x0, p.y - 1.5 * dpr, 10 * dpr, 3 * dpr);
      ctx.fillStyle = css("--ink-2");
      ctx.fillText(p.s.label.length > 22 ? p.s.label.slice(0, 21) + "…" : p.s.label, x0 + 14 * dpr, p.y);
    });
    ctx.restore();
  }

  // szare pola okresów porównania z nazwą przy dolnej krawędzi (nazwy idą za wyborem porównania)
  function polaOkresow(u, a, b, nazwy) {
    var ctx = u.ctx, top = u.bbox.top, h = u.bbox.height, dpr = window.devicePixelRatio || 1;
    [[a, css("--okres-a"), nazwy && nazwy.a], [b, css("--okres-b"), nazwy && nazwy.b]].forEach(function (o) {
      if (!o[0]) return;
      var x0 = u.valToPos((START + o[0][0] * DZIEN) / 1000, "x", true);
      var x1 = u.valToPos((START + (o[0][1] + 1) * DZIEN) / 1000, "x", true);
      x0 = Math.max(x0, u.bbox.left); x1 = Math.min(x1, u.bbox.left + u.bbox.width);
      if (x1 <= x0) return;
      ctx.save(); ctx.fillStyle = o[1]; ctx.fillRect(x0, top, x1 - x0, h);
      if (o[2]) {
        ctx.font = (11 * dpr) + "px system-ui"; ctx.textBaseline = "bottom";
        var t = o[2].charAt(0).toUpperCase() + o[2].slice(1);
        var sz = ctx.measureText(t).width;
        if (sz + 12 * dpr < x1 - x0) {
          // tło pod nazwą, żeby linie danych jej nie przecinały
          ctx.fillStyle = css("--surface"); ctx.globalAlpha = 0.88;
          ctx.fillRect(x0 + 3 * dpr, top + h - 18 * dpr, sz + 6 * dpr, 15 * dpr);
          ctx.globalAlpha = 1; ctx.fillStyle = css("--ink-2"); ctx.fillText(t, x0 + 6 * dpr, top + h - 5 * dpr);
        }
      }
      ctx.restore();
    });
  }
  function rysujOkresy(u) { var n = nazwyOkresow(); polaOkresow(u, S.a, S.b, n); }

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
    var data = [x], series = [{ label: "Dzień" }], opisy = [];
    var razem = seria(dane, "__razem"), sRazem = krocz(razem.s, w);
    // wartość wybrana w „Pokaż dla” jest wyróżniona, pozostałe szare (gdy jest na wykresie)
    var wyroz = S.lw !== "__razem" && S.wybrane.indexOf(S.lw) >= 0 ? S.lw : null;
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
      var kol = wyroz && wart !== wyroz ? css("--seria-a") : css(S.kolory[wart] || "--seria-ref");
      var gruba = wyroz ? wart === wyroz : wart === "__razem";
      series.push({ label: etykieta(S.podz, wart), stroke: kol, width: wyroz && !gruba ? 1.25 : gruba ? 2.5 : 2, spanGaps: false, points: { show: false } });
      opisy.push({ label: etykieta(S.podz, wart), kolor: kol, w: wart, gruba: gruba, wart: (function (mian) {
        return function (v, di) {
          if (miara.id === "sesje") return liczba(v, 1) + " sesji dziennie";
          return proc(v) + (mian && di != null ? " z " + liczba(mian[di]) + (miara.id === "udzial" ? " sesji razem" : "") : "");
        };
      })(mian) });
    });
    var cel = wyczysc($("lj-wykres"));
    var zd = zdarzeniaWykresu("lejek", ["lejek"]);
    var procentowa = miara.id !== "sesje";
    var opts = {
      width: cel.clientWidth || 300, height: 340,
      scales: { x: { time: true }, y: { range: function (u, mn, mx) { return [0, procentowa ? Math.min(100, Math.max(5, mx * 1.08)) : Math.max(1, mx * 1.08)]; } } },
      axes: osieWykresu("", function (v) { return liczba(v, 0) + (procentowa ? "%" : ""); }),
      series: series,
      cursor: { drag: { x: true, y: false }, points: { size: 8 } },
      tzDate: function (ts) { return uPlot.tzDate(new Date(ts * 1000), "Etc/UTC"); },
      hooks: { drawClear: [rysujOkresy], draw: [function (u) { rysujZdarzeniaNaWykresie(u, zd); }] }
    };
    var dostepne = (S.podz === "calosc" ? [] : wartosci(dane).map(function (v) { return { w: v, n: suma(seria(dane, v).s, S.b) }; })
      .sort(function (p, q) { return q.n - p.n; }).map(function (p) { return [p.w, etykieta(S.podz, p.w)]; }));
    var dorysuj = legendaUplot(opts, cel, { id: "lejek", serie: opisy, obszary: ["lejek"], zdarzenia: zd, koncowe: true,
      etykietaX: function (ts) { return dataPL(Math.round((ts * 1000 - START) / DZIEN)); },
      odswiez: function () { odswiezLejek(true); },
      wybor: { dostepne: [["__razem", "Razem"]].concat(dostepne), wybrane: S.wybrane, max: 8,
        dodaj: function (v) { S.wybrane.push(v); odswiezLejek(true, true); },
        usun: function (v) { S.wybrane = S.wybrane.filter(function (q) { return q !== v; }); odswiezLejek(true, true); } } });
    if (wykresLejka) wykresLejka.destroy();
    wykresLejka = new uPlot(opts, data, cel);
    dorysuj();
  }

  // Udział sesji nowych kampanii na L4 w sesjach osób, które jeszcze nie kupowały, miesiąc po miesiącu. Liczony z pliku
  // podziału według kampanii, zawsze dla sesji zwykłych osób, które jeszcze nie kupowały: nie zależy od podziału,
  // „Kto” ani okresów wybranych w filtrach lejka.
  var udzialNarysowany = false;
  function rysujUdzialNowych() {
    var cel = $("lj-udzial");
    if (!cel || udzialNarysowany) return;
    udzialNarysowany = true;
    wczytajPodzial("kampania").then(function (dane) {
      var nowe = ET.nowe_kampanie || [], mies = [], kl = {}, przyp = new Int32Array(NDNI), i;
      for (i = 0; i < NDNI; i++) {   // miesiące kalendarzowe według dnia sesji (dni w danych są w czasie polskim)
        var d = dataIdx(i), k = d.getUTCFullYear() * 12 + d.getUTCMonth();
        if (kl[k] === undefined) { kl[k] = mies.length; mies.push({ r: d.getUTCFullYear(), m: d.getUTCMonth(), nowe: 0, wsz: 0 }); }
        przyp[i] = kl[k];
      }
      dane.serie.forEach(function (s) {
        if (s.typ !== "zwykla" || s.pacjent !== "nie_kupowal" || !s.s) return;
        var czyNowa = nowe.indexOf(s.w) >= 0;
        for (var j = 0; j < NDNI; j++) { var v = s.s[j]; if (!v) continue; var x = mies[przyp[j]]; x.wsz += v; if (czyNowa) x.nowe += v; }
      });
      mies.forEach(function (x) { x.p = x.wsz > 0 ? 100 * x.nowe / x.wsz : null; });
      var mx = Math.max.apply(null, mies.map(function (x) { return x.p || 0; }).concat([1])), sk = BK.podzialka(0, mx, 5);
      wyczysc(cel).appendChild(BK.kolumny({ max: sk.max, wys: 190,
        os: sk.wartosci.map(function (v) { return { v: v, tekst: liczba(v, 0) + "%" }; }),
        serie: [{ nazwa: "nowe kampanie na L4", klasa: "seg-nowe" }],
        grupy: mies.map(function (x, j) {
          var naz = RZYM[x.m] + " " + x.r, t = naz + ": " + proc(x.p) + " (" + liczba(x.nowe) + " z " + liczba(x.wsz) + " sesji)";
          return { os: j % 3 === 0 ? (j === 0 || x.m === 0 ? [RZYM[x.m], String(x.r)] : [RZYM[x.m]]) : null,
            wartosci: [x.p], podpisy: [x.p ? proc(x.p) : ""], tytul: t, opis: t };
        }),
        opis: "Udział sesji nowych kampanii na L4 w sesjach osób, które jeszcze nie kupowały, w każdym miesiącu",
        przypis: "Udział sesji z dwóch nowych kampanii na L4 (Meta i TikTok) w zwykłych sesjach osób, które jeszcze nie " +
          "kupowały, w każdym miesiącu kalendarzowym. Wykres nie zależy od filtrów „Podział” i „Kto” ani od okresów wybranych wyżej." }));
    }).catch(function (e) { udzialNarysowany = false; wyczysc(cel).appendChild(el("p", { class: "przypis", text: e.message + ". Odśwież stronę." })); });
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

  // chipy obszarów w nagłówku karty z osią
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

  // kształt znacznika według rodzaju zdarzenia (pole rodzaj): koło = start kampanii; kwadrat = awaria, błąd albo luka
  // w danych; romb = zmiana (poziomu, stopniowa, struktury pacjentów, wyniku i zachowania kohort, obsługi pacjenta);
  // puste koło = kandydat poniżej progu; zdarzenie z datą końca to pasek od początku do końca
  var KSZTALTY = [["kolo", "start kampanii"], ["kwadrat", "awaria, błąd albo luka w danych"], ["romb", "zmiana"],
    ["puste", "kandydat poniżej progu"], ["pasek", "zdarzenie z datą początku i końca"]];
  function ksztalt(z) {
    if (z.do && z.do !== z.od) return "pasek";
    var r = String(z.rodzaj || "").toLowerCase();
    if (r.indexOf("start") === 0) return "kolo";
    if (r.indexOf("kandydat") === 0) return "puste";
    if (r === "awaria" || r.indexOf("błąd") === 0 || r.indexOf("luka") === 0) return "kwadrat";
    if (r.indexOf("zmiana") === 0) return "romb";
    return "kolo";
  }
  function znakKsztaltu(k) { return el("span", { class: "ks ks-" + k, "aria-hidden": "true" }); }
  function rysujLegendeOsi() {
    var c = $("zd-os-legenda");
    if (!c || c.firstChild) return;
    var obecne = {};
    ZD.lista.forEach(function (z) { obecne[ksztalt(z)] = true; });
    KSZTALTY.forEach(function (k) {
      if (obecne[k[0]]) c.appendChild(el("span", { class: "wk-lg" }, [znakKsztaltu(k[0]), el("span", { text: k[1] })]));
    });
  }

  function rysujOsPionowa(kont) {
    var ol = el("ol", { class: "os-pionowa", "aria-label": "Zdarzenia w kolejności dat" });
    zdarzeniaNumerowane().forEach(function (z) {
      if (!obszaryWidoczne[z.obszar]) return;
      var i0 = idxIso(z.od);
      ol.appendChild(el("li", { class: "zk-" + ksztalt(z) }, [
        el("div", { class: "os-data" }, [el("strong", { text: z.nr + ". " + dataPL(i0) + (z.do ? "–" + dataPL(idxIso(z.do)) : "") }),
          el("span", { class: "obszar", text: ET.obszary[z.obszar] })]),
        el("a", { href: "#zdarzenia?z=" + z.id, text: z.krotko || z.tytul })]));
    });
    kont.appendChild(ol);
  }
  function rysujOs() {
    var kont = wyczysc($("zd-os"));
    rysujLegendeOsi();
    if ((kont.clientWidth || 900) < 600) { rysujOsPionowa(kont); return; }
    var szer = Math.max(560, kont.clientWidth || 900), lewy = 130, prawy = 16, gora = 34, ODSTEP = 18, RZAD = 13;
    var obszary = ZD.obszary.filter(function (o) { return obszaryWidoczne[o.id]; });
    var NS = "http://www.w3.org/2000/svg";
    function s(tag, a, txt) { var e = document.createElementNS(NS, tag); for (var k in a) e.setAttribute(k, a[k]); if (txt) e.textContent = txt; return e; }
    function xp(i) { return lewy + (szer - lewy - prawy) * i / (NDNI - 1); }
    // numery bez nachodzenia: bliskie zdarzenia dostają numer w wyższym rzędzie nad znacznikiem; tor jest tak wysoki,
    // ile rzędów potrzeba
    var zd = zdarzeniaNumerowane(), tory = [], y = gora;
    obszary.forEach(function (o) {
      var tu = zd.filter(function (z) { return z.obszar === o.id; }).map(function (z) { return { z: z, x: xp(idxIso(z.od)) }; })
        .sort(function (a, c) { return a.x - c.x; });
      var rzedy = [];
      tu.forEach(function (p) {
        var r = 0;
        while (rzedy[r] !== undefined && p.x - rzedy[r] < ODSTEP) r++;
        rzedy[r] = p.x; p.r = r;
      });
      var wys = 30 + RZAD * Math.max(1, rzedy.length);
      tory.push({ o: o, tu: tu, y: y, wys: wys });
      y += wys;
    });
    var wys = y + 8;
    var svg = s("svg", { viewBox: "0 0 " + szer + " " + wys, class: "os-rys", role: "img", "aria-label": "Oś czasu zdarzeń w podziale na obszary; kształt znacznika według rodzaju zdarzenia" });
    // podziałka: początek każdego kwartału
    for (var i = 0; i < NDNI; i++) {
      var d = dataIdx(i);
      if (d.getUTCDate() === 1 && d.getUTCMonth() % 3 === 0) {
        svg.appendChild(s("line", { x1: xp(i), x2: xp(i), y1: gora - 8, y2: wys - 4, class: "siatka" }));
        svg.appendChild(s("text", { x: xp(i) + 3, y: gora - 14 }, RZYM[d.getUTCMonth()] + " " + d.getUTCFullYear()));
      }
    }
    tory.forEach(function (t) {
      var cy = t.y + t.wys - 15;
      svg.appendChild(s("rect", { x: lewy, y: t.y + 3, width: szer - lewy - prawy, height: t.wys - 6, rx: 6, class: "tor-tlo" }));
      svg.appendChild(s("text", { x: 0, y: cy + 4, class: "tor-nazwa" }, ET.obszary[t.o.id]));
      if (!t.tu.length && t.o.puste) svg.appendChild(s("text", { x: lewy + 10, y: cy + 4, class: "puste" }, t.o.puste));
      t.tu.forEach(function (p) {
        var z = p.z, i0 = idxIso(z.od), i1 = z.do ? idxIso(z.do) : null, k = ksztalt(z), x = p.x, g;
        if (k === "pasek") g = s("rect", { x: x, y: cy - 6, width: Math.max(6, xp(i1) - x), height: 12, rx: 4, class: "znacznik-zakres" });
        else if (k === "kwadrat") g = s("rect", { x: x - 5.5, y: cy - 5.5, width: 11, height: 11, rx: 1.5, class: "znacznik zk-kwadrat" });
        else if (k === "romb") g = s("path", { d: "M" + x + " " + (cy - 7.5) + "L" + (x + 7.5) + " " + cy + "L" + x + " " + (cy + 7.5) + "L" + (x - 7.5) + " " + cy + "Z", class: "znacznik zk-romb" });
        else if (k === "puste") g = s("circle", { cx: x, cy: cy, r: 5.5, class: "znacznik zk-puste" });
        else g = s("circle", { cx: x, cy: cy, r: 6, class: "znacznik zk-kolo" });
        g.setAttribute("tabindex", "0");
        g.setAttribute("aria-label", z.nr + ". " + dataPL(i0) + (i1 ? "–" + dataPL(i1) : "") + ", " + z.rodzaj + ": " + z.tytul);
        g.appendChild(s("title", {}, z.nr + ". " + dataPL(i0) + (i1 ? "–" + dataPL(i1) : "") + " (" + z.rodzaj + "): " + z.tytul));
        g.addEventListener("click", function () { pokazZdarzenie(z.id); });
        g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pokazZdarzenie(z.id); } });
        svg.appendChild(g);
        svg.appendChild(s("text", { x: x, y: cy - 11 - p.r * RZAD, "text-anchor": "middle", class: "os-nr" }, String(z.nr)));
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
      // „Skąd wiemy” w zwijanej sekcji na końcu karty
      var skad = z.skad ? el("details", { class: "szczegoly" }, [el("summary", { text: "Skąd wiemy" }),
        el("div", { class: "szczegoly-tresc" }, [el("p", { text: z.skad })])]) : null;
      var link = z.link ? el("a", { href: z.link, text: napisOdnosnika(z.link) }) : null;
      l.appendChild(el("article", { class: "karta zdarzenie", id: "zd-" + z.id }, [
        el("div", { class: "meta" }, [el("span", { class: "data", text: z.nr + ". " + dataPL(idxIso(z.od)) + (z.do ? "–" + dataPL(idxIso(z.do)) : "") }),
          el("span", { class: "obszar", text: ET.obszary[z.obszar] }), el("span", { class: "rodzaj" }, [znakKsztaltu(ksztalt(z)), z.rodzaj])]),
        el("h3", { text: z.tytul }), dl, link ? el("p", { class: "zd-link" }, [link]) : null, skad]));
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
            ruch ? "neutralnie" : r[ix.zmiana] >= 0 ? "dobrze" : "zle", null, { slowo: false })]),
          el("td", { text: r[ix.dni_przed] + " / " + r[ix.dni_po] }),
          el("td", { text: r[ix.zamowienia_na_30_dni] === null ? "—" : znak(r[ix.zamowienia_na_30_dni], 1) }),
          el("td", null, [el("a", { href: "#lejek?" + q.toString(), text: "w lejku" })])]));
      });
    t.appendChild(tb);
    BK.legendaZmian($("zd-wykryte-legenda"), "(poziom po wykrytej zmianie wobec poziomu przed nią)");
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
    // schodki mostka pod wnioskiem, tabela mostka w zwijanej sekcji
    BK.wstawWykres($("jk-karta-mostek"), schodkiMostka(), true);
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
      width: cel.clientWidth || 300, height: 260,
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
      tzDate: function (ts) { return uPlot.tzDate(new Date(ts * 1000), "Etc/UTC"); },
      hooks: { drawClear: [function (u) { oknoDuplikatow(u, od, dok); }], draw: [function (u) { oknoDuplikatow(u, od, dok, true); }] }
    };
    var dorysuj = legendaUplot(opts, cel, { id: "duplikaty", koncowe: false,
      etykietaX: function (ts) { return dataPL(Math.round((ts * 1000 - START) / DZIEN)); },
      serie: [{ label: "Zamówienia bez kopii", kolor: css("--series-1"), wart: function (v) { return liczba(v); } },
        { label: "Kopie (duplikaty)", kolor: css("--series-2"), wart: function (v) { return liczba(v); } }] });
    if (wykresDup) wykresDup.destroy();
    wykresDup = new uPlot(opts, [x, JK.duplikaty.zamowienia_d, JK.duplikaty.kopie_d], cel);
    dorysuj();
  }

  // okno duplikatów (JK.duplikaty.od–do) podcieniowane na szaro, z podpisem przy górnej krawędzi; gdy podpis jest szerszy
  // niż pole (telefon), wychodzi w prawo na tle karty
  function oknoDuplikatow(u, od, dok, podpis) {
    var ctx = u.ctx, top = u.bbox.top, h = u.bbox.height, dpr = window.devicePixelRatio || 1;
    var x0 = Math.max(u.valToPos((START + od * DZIEN) / 1000, "x", true), u.bbox.left);
    var x1 = Math.min(u.valToPos((START + (dok + 1) * DZIEN) / 1000, "x", true), u.bbox.left + u.bbox.width);
    if (x1 <= x0) return;
    ctx.save();
    if (!podpis) { ctx.fillStyle = css("--okres-b"); ctx.fillRect(x0, top, x1 - x0, h); ctx.restore(); return; }
    // podpis rysowany po seriach, żeby linia go nie przecinała
    ctx.font = (11 * dpr) + "px system-ui"; ctx.textBaseline = "top"; ctx.textAlign = "left";
    var t = "Okno duplikatów", sz = ctx.measureText(t).width;
    var xt = Math.min(x0 + 4 * dpr, u.bbox.left + u.bbox.width - sz - 6 * dpr);
    ctx.fillStyle = css("--surface"); ctx.globalAlpha = 0.88; ctx.fillRect(xt - 3 * dpr, top + 3 * dpr, sz + 6 * dpr, 15 * dpr);
    ctx.globalAlpha = 1; ctx.fillStyle = css("--ink-2"); ctx.fillText(t, xt, top + 5 * dpr);
    ctx.restore();
  }

  // ------------------------------------------------------------ nawigacja
  var WIDOKI =Array.prototype.map.call(document.querySelectorAll(".zakladki a"), function (a) { return a.dataset.widok; });
  var narysowane = {}, biezacy = null;

  function trasa() {
    var cz = location.hash.slice(1).split("?"), nazwa = decodeURIComponent(cz[0]);
    var widok = WIDOKI.indexOf(nazwa) >= 0 ? nazwa : "wzrost";
    var q = new URLSearchParams(cz[1] || "");
    WIDOKI.forEach(function (v) { $("v-" + v).hidden = v !== widok; });
    Array.prototype.forEach.call(document.querySelectorAll(".zakladki a, .szybkie-lista a"), function (a) {
      if (a.dataset.widok === widok) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    zamknijSzybkie();
    if (biezacy !== widok) window.scrollTo(0, 0);
    biezacy = widok;
    if (widok === "lejek") {
      if (!narysowane.lejek) { rysujNaglowekLejka(); przygotujFiltry(); narysowane.lejek = true; }
      czytajAdres(q);
      odswiezLejek();
      rysujUdzialNowych();
      if (q && Array.from(q.keys()).length) setTimeout(function () {
        $("lj-kroki-karta").scrollIntoView({ behavior: "smooth", block: "start" });
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

  // ------------------------------------------------------------ przycisk „Zakładki” na telefonie
  // Na telefonie pasek z zakładkami nie jest przyklejony. Gdy zniknie z ekranu, w prawym dolnym rogu pojawia się przycisk,
  // który rozwija listę wszystkich zakładek.
  function zamknijSzybkie() {
    var l = $("szybkie-lista"), p = $("szybkie-przycisk");
    if (l && !l.hidden) { l.hidden = true; p.setAttribute("aria-expanded", "false"); }
  }
  function przygotujSzybkie() {
    var box = $("szybkie-zakladki"), l = $("szybkie-lista"), p = $("szybkie-przycisk");
    if (!box) return;
    Array.prototype.forEach.call(document.querySelectorAll(".zakladki a"), function (a) {
      l.appendChild(el("li", null, [el("a", { href: a.getAttribute("href"), "data-widok": a.dataset.widok, text: a.textContent })]));
    });
    p.insertBefore(BK.ikona("lista"), p.firstChild);
    p.onclick = function (e) {
      e.stopPropagation();
      l.hidden = !l.hidden; p.setAttribute("aria-expanded", String(!l.hidden));
      if (!l.hidden) { var akt = l.querySelector("a[aria-current]") || l.querySelector("a"); if (akt) akt.focus(); }
    };
    l.addEventListener("click", function (e) { if (e.target.closest("a")) zamknijSzybkie(); });
    document.addEventListener("click", function (e) { if (!box.contains(e.target)) zamknijSzybkie(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { zamknijSzybkie(); } });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (wpisy) {
        box.hidden = wpisy[0].isIntersecting;
        if (box.hidden) zamknijSzybkie();
      }).observe(document.querySelector(".zakladki"));
    }
  }

  // na dole każdej zakładki odnośnik do następnej (ostatnia wraca do początku)
  function odnosnikiDalej() {
    var linki = Array.prototype.slice.call(document.querySelectorAll(".zakladki a"));
    linki.forEach(function (a, i) {
      var s = $("v-" + a.dataset.widok), nast = linki[i + 1];
      if (!s || s.querySelector(":scope > .dalej")) return;
      s.appendChild(el("p", { class: "dalej" }, [el("a", { href: (nast || linki[0]).getAttribute("href"),
        text: nast ? "Dalej: " + nast.textContent : "Wróć do początku: " + linki[0].textContent })]));
    });
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
    mostek: mostek, BK: BK, zdaniaAlboKarta: zdaniaAlboKarta, zmianaPkt: zmianaPkt, wstepKarta: wstepKarta,
    nazwyPresetu: nazwyPresetu, polaOkresow: polaOkresow, hantleSafari: hantleSafari,
    legendaUplot: legendaUplot, zdarzeniaWykresu: zdarzeniaWykresu, tabelaTelefon: tabelaTelefon, schodkiMostka: schodkiMostka };
  ikonyStatyczne();
  przygotujSzybkie();
  odnosnikiDalej();

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
