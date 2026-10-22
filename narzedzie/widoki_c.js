/* Widoki z wynikiem punktu C: „Czy to wzrost”, „Priorytety”, „Czego nie wiemy”.
   Dane z dane_strony/c.js (tworzy je analiza/b2_eksport_c.py, uruchamiany też przez analiza/b_eksport.py).
   Ten plik nie wpisuje żadnych liczb: wszystkie zdania i wartości w tabelach przychodzą gotowe z eksportu.
   Rysuje nowy kształt danych z kontraktu (notatki/e_runda.md, punkt 3), a gdy go nie ma — dotychczasowy.
   Pomocnicze funkcje (el, $, mostek) udostępnia app.js jako window.B, karty i znaczniki karty.js jako window.BK. */
(function () {
  "use strict";
  var BW = window.BW = window.BW || {};
  var C = window.D.C;
  var b = function () { return window.B; };
  var BK = window.BK;

  function lista(cel, punkty) {
    var B = b();
    B.wyczysc(cel);
    punkty.forEach(function (p) { cel.appendChild(B.el("li", { text: p })); });
    return cel;
  }
  function linkiDanych(cel, linki) {
    var B = b();
    B.wyczysc(cel);
    var l = BK.linki(linki);
    if (l) cel.appendChild(l);
    return cel;
  }
  function wiersz(komorki, naglowek) {
    var B = b(), tr = B.el("tr");
    komorki.forEach(function (k) {
      var td = B.el(naglowek ? "th" : "td", typeof k === "string" ? { text: k } : k.attrs, typeof k === "string" ? null : k.dzieci);
      tr.appendChild(td);
    });
    return tr;
  }
  function podswietl(id) {
    var e = document.getElementById(id);
    if (!e) return;
    Array.prototype.forEach.call(document.querySelectorAll(".priorytet.podswietlone"), function (x) { x.classList.remove("podswietlone"); });
    e.classList.add("podswietlone");
    setTimeout(function () { e.scrollIntoView({ behavior: "smooth", block: "start" }); }, 30);
  }
  function wstawki() {
    var B = b();
    return { mostek: function () { var t = B.el("table", { class: "tabela" }); B.mostek(t); return B.el("div", { class: "tabela-ramka" }, [t]); } };
  }

  // ------------------------------------------------------------ CZY TO WZROST
  var gotoweWz = false;
  function nowyKsztaltWzrostu(W) { return W && W.werdykt && typeof W.werdykt === "object" && Array.isArray(W.karty); }

  function rysujWzrostNowy(W) {
    var B = b(), el = B.el, $ = B.$;
    $("wz-stary").hidden = true;
    var n = B.wyczysc($("wz-nowy"));
    n.hidden = false;
    if (W.tytul) $("wz-tytul").textContent = W.tytul;
    if (W.wstep) $("wz-wstep").textContent = W.wstep;

    var art = el("article", { class: "karta werdykt", id: "wz-werdykt" }, [
      el("div", { class: "werdykt-gora" }, [BK.znacznik(W.werdykt.znacznik, true), el("div", null, [
        el("p", { class: "werdykt-tekst", text: W.werdykt.tekst }),
        W.werdykt.dopisek ? el("p", { class: "werdykt-dopisek", text: W.werdykt.dopisek }) : null])])]);
    if (W.kafelki && W.kafelki.length) art.appendChild(BK.kafelki(W.kafelki));
    if (W.decyzje && W.decyzje.punkty && W.decyzje.punkty.length) {
      art.appendChild(el("h3", { class: "decyzje-tytul", text: W.decyzje.tytul || "" }));
      art.appendChild(el("ol", { class: "decyzje" }, W.decyzje.punkty.map(function (d, i) {
        var nr = String(d.nr || i + 1);
        return el("li", null, [
          d.href ? el("a", { class: "nr", href: d.href, text: nr, "aria-hidden": "true", tabindex: "-1" }) : el("span", { class: "nr", text: nr }),
          el("span", { class: "decyzja-tekst" }, [d.href ? el("a", { href: d.href, text: d.tekst }) : d.tekst,
            d.dopisek ? el("span", { class: "dopisek", text: d.dopisek }) : null])]);
      })));
    }
    n.appendChild(art);

    var karty = W.karty || [], ws = wstawki();
    var elKarty = karty.map(function (k) { return BK.karta(k, { prefiks: "wz-", wstawki: ws }); });
    if (elKarty.length >= 2) n.appendChild(el("div", { class: "karty-dwie" }, elKarty.slice(0, 2)));
    elKarty.slice(elKarty.length >= 2 ? 2 : 0).forEach(function (a) { n.appendChild(a); });
    // wykresy w kartach: „Więcej pacjentów” (słupki), „Lepsza retencja” (hantle), TelemediGO (słupki parami)
    if (karty[0] && karty[0].etykieta) BK.wstawWykres(elKarty[0], slupkiPacjentow());
    if (karty[1] && karty[1].etykieta) BK.wstawWykres(elKarty[1], hantleRetencji(), true);
    karty.forEach(function (k, i) { if (k.wykres && k.wykres.wiersze && i >= 2) BK.wstawWykres(elKarty[i], slupkiTelemedigo(k.wykres), true); });
    $("wz-zrodlo").textContent = W.zrodlo || "";
  }

  // powrót nowych pacjentów w 30/60/90/180 dniach: rok wcześniej → ostatnie 12 miesięcy (hantle); dane z podsumowanie.js
  function hantleRetencji() {
    var B = b(), R = B.P.wzrost && B.P.wzrost.retencja;
    if (!R || !R.okna || !R.okna.length) return null;
    return BK.hantle({ nazwy: { a: "rok wcześniej", b: "ostatnie 12 miesięcy" }, kodowanie: "okresy", min: 0, max: 30, os: ["0%", "10%", "20%", "30%"],
      opis: "Powrót nowych pacjentów w ciągu 30, 60, 90 i 180 dni: rok wcześniej i ostatnie 12 miesięcy",
      wiersze: R.okna.map(function (o) {
        var d = o.p2 - o.p1;
        return { etykieta: "w ciągu " + o.dni + " dni", a: o.p1, b: o.p2, tekstA: B.proc(o.p1), tekstB: B.proc(o.p2),
          tytul: "Powrót w ciągu " + o.dni + " dni: rok wcześniej " + B.proc(o.p1) + " z " + B.liczba(o.n1) + " pacjentów, ostatnie 12 miesięcy " +
            B.proc(o.p2) + " z " + B.liczba(o.n2) + " pacjentów (kohorty z pełnym oknem)",
          zmiana: { tekst: B.znak(d, 1) + " pkt proc.", kierunek: BK.kierunekZnaku(d), stan: d < 0 ? "zle" : d > 0 ? "dobrze" : "neutralnie" } };
      }) });
  }
  // nowi pacjenci w obu latach: nowe kampanie na L4 i pozostali (długość = liczba pacjentów); dane z podsumowanie.js
  function slupkiPacjentow() {
    var B = b(), G = B.P.wzrost && B.P.wzrost.pacjenci && B.P.wzrost.pacjenci.grupy;
    if (!G) return null;
    var poz = G.filter(function (g) { return g.grupa === "pozostale"; })[0], now = G.filter(function (g) { return g.grupa === "nowe_kampanie"; })[0];
    if (!poz || !now) return null;
    var r1 = poz.n1 + now.n1, r2 = poz.n2 + now.n2;
    return BK.slupkiSkumulowane({ czesci: [{ nazwa: "pozostałe kampanie i kanały", klasa: "seg-pozostale" }, { nazwa: "nowe kampanie na L4", klasa: "seg-nowe" }],
      max: Math.max(r1, r2) * 1.02, opis: "Nowi pacjenci rok wcześniej i w ostatnich 12 miesiącach, w podziale na nowe kampanie na L4 i pozostałe",
      wiersze: [{ etykieta: "rok wcześniej", wartosci: [poz.n1, now.n1], teksty: [B.liczba(poz.n1), B.liczba(now.n1)], suma: B.liczba(r1) },
        { etykieta: "ostatnie 12 miesięcy", wartosci: [poz.n2, now.n2], teksty: [B.liczba(poz.n2), B.liczba(now.n2)], suma: B.liczba(r2) }],
      przypis: "Nowi pacjenci według pierwszego wejścia; długość słupka to liczba pacjentów." });
  }
  // TelemediGO: trzy sposoby zakupu, rok wcześniej i ostatnie 12 miesięcy (słupki parami); dane z pola wykres karty
  function slupkiTelemedigo(Wk) {
    var B = b(), mx = Math.max.apply(null, Wk.wiersze.map(function (r) { return Math.max(r.p1, r.p2); }));
    return BK.slupkiParami({ nazwy: { a: "rok wcześniej", b: "ostatnie 12 miesięcy" }, max: mx * 1.05,
      opis: "Sprzedaż TelemediGO według sposobu zakupu: rok wcześniej i ostatnie 12 miesięcy",
      wiersze: Wk.wiersze.map(function (r) {
        var d = r.p2 - r.p1;
        return { etykieta: r.opis, a: r.p1, b: r.p2, tekstA: B.liczba(r.p1), tekstB: B.liczba(r.p2),
          zmiana: { tekst: B.znak(d, 0), kierunek: BK.kierunekZnaku(d), stan: "neutralnie", tytul: "Zmiana liczby zakupów rok do roku" } };
      }), przypis: "Liczba zakupów TelemediGO." });
  }
  BW.hantleRetencji = hantleRetencji;

  function rysujWzrostStary(W) {
    var B = b(), el = B.el, $ = B.$, O = B.O;
    var S = W.skrot;
    $("wz-skrot-odpowiedz").textContent = S.odpowiedz;
    lista($("wz-skrot-liczby"), S.liczby);
    var dz = B.wyczysc($("wz-skrot-decyzje"));
    S.decyzje.forEach(function (d) { dz.appendChild(el("li", null, [el("a", { href: d.href, text: d.tekst })])); });
    $("wz-skrot-kwota").textContent = S.kwota;
    B.akapity($("wz-puenta"), W.puenta);

    $("wz-pacjenci-liczba").textContent = W.pacjenci.liczba;
    $("wz-pacjenci-podpis").textContent = W.pacjenci.podpis;
    lista($("wz-pacjenci-punkty"), W.pacjenci.punkty);

    $("wz-retencja-liczba").textContent = W.retencja.liczba;
    $("wz-retencja-podpis").textContent = W.retencja.podpis;
    var t = B.wyczysc($("wz-retencja-tabela"));
    t.appendChild(el("thead", null, [wiersz(["Powrót w ciągu", "Rok wcześniej (" + O[0].nazwa + ")", "Ostatnie 12 miesięcy (" + O[1].nazwa + ")", "Zmiana"], true)]));
    var tb = el("tbody");
    W.retencja.okna.forEach(function (o) {
      var lepiej = o.p2 >= o.p1;
      tb.appendChild(wiersz([o.dni + " dni", o.tekst1, o.tekst2,
        { attrs: null, dzieci: [BK.zmiana(o.zmiana, BK.kierunekZnaku(o.p2 - o.p1), lepiej ? "dobrze" : "zle")] }]));
    });
    t.appendChild(tb);
    lista($("wz-retencja-punkty"), W.retencja.punkty);

    var G = W.telemedigo;
    $("wz-go-tytul").textContent = G.tytul;
    $("wz-go-puenta").textContent = G.puenta;
    var g = B.wyczysc($("wz-go-tabela"));
    g.appendChild(el("thead", null, [wiersz(G.tabela.kolumny, true)]));
    var gb = el("tbody");
    G.tabela.wiersze.forEach(function (r, i) {
      var tr = wiersz([r.opis].concat(r.komorki));
      if (i === G.tabela.wiersze.length - 1) tr.className = "podsuma";
      gb.appendChild(tr);
    });
    g.appendChild(gb);
    lista($("wz-go-punkty"), G.punkty);
    linkiDanych($("wz-go-linki"), G.linki);
    $("wz-go-zrodlo").textContent = G.zrodlo;

    $("wz-zamkniecie").textContent = W.zamkniecie;
    $("wz-safari").textContent = W.safari;
    $("wz-kwartaly-naglowek").textContent = W.kwartaly.naglowek;
    var k = B.wyczysc($("wz-kwartaly"));
    k.appendChild(el("thead", null, [wiersz(["Kwartał", "Marża", "Rok wcześniej", "Zmiana marży", "Wydatki na kampanie",
      "Rok wcześniej", "Wydatki: ile razy więcej"], true)]));
    var kb = el("tbody");
    W.kwartaly.wiersze.forEach(function (r) {
      kb.appendChild(wiersz([r.kw, r.m2, r.m1, { attrs: null, dzieci: [BK.zmiana(r.zm, r.minus ? "spadek" : "wzrost", r.minus ? "zle" : "dobrze")] },
        r.w2, r.w1, r.il]));
    });
    k.appendChild(kb);
    lista($("wz-kwartaly-punkty"), W.kwartaly.punkty);
    $("wz-rozklad-tytul").textContent = W.kwartaly.rozklad_tytul;
    $("wz-rozklad-wstep").textContent = W.kwartaly.rozklad_wstep;
    lista($("wz-rozklad-punkty"), W.kwartaly.rozklad_punkty);
    $("wz-rozklad-luka").textContent = W.kwartaly.luka;
    $("wz-baza").textContent = W.kwartaly.baza;

    var z = B.wyczysc($("wz-zastrzezenia"));
    W.zastrzezenia.forEach(function (x) { z.appendChild(el("li", null, [el("strong", { text: x.tytul }), " " + x.tekst])); });

    $("wz-dashboard-zdanie").textContent = B.P.wzrost.dashboard.zdanie;
    B.mostek($("wz-mostek"));
    linkiDanych($("wz-linki"), W.linki);
    $("wz-zrodlo").textContent = W.zrodlo;
  }
  function rysujWzrost() {
    var W = C.wzrost;
    if (nowyKsztaltWzrostu(W)) rysujWzrostNowy(W); else rysujWzrostStary(W);
  }
  BW.wzrost = { pokaz: function () { if (!gotoweWz) { rysujWzrost(); gotoweWz = true; } } };

  // ------------------------------------------------------------ PRIORYTETY
  var gotowePr = false;
  // kwota: w nowym kształcie krótka kwota i dopisek osobno, w dotychczasowym jeden napis
  function kwota(ile, dopisek) {
    var B = b();
    return [B.el("span", { class: "kwota", text: ile }), dopisek ? B.el("span", { class: "kwota-dopisek", text: dopisek }) : null];
  }
  function pewnoscKom(p) {
    var B = b(), x = BK.pewnoscZNapisu(p);
    if (!x) return ["—"];
    return [BK.pewnosc(x), x.dopisek ? B.el("span", { class: "pewnosc-dopisek", text: x.dopisek }) : null];
  }
  function pasek(p) {
    var B = b(), el = B.el;
    return el("div", { class: "pasek-priorytetu" }, [
      el("div", null, [el("span", { class: "pasek-etykieta", text: "Ile warte rocznie (marża)" })].concat(kwota(p.ile, p.ile_dopisek))),
      el("div", null, [el("span", { class: "pasek-etykieta", text: "Pewność" })].concat(pewnoscKom(p.pewnosc))),
      el("div", null, [el("span", { class: "pasek-etykieta", text: "Wdrożenie" }), el("span", { class: "pasek-wartosc", text: p.wdrozenie })])]);
  }
  function rysujPriorytety() {
    var B = b(), el = B.el, $ = B.$, P = C.priorytety;
    if (P.tytul) $("pr-tytul").textContent = P.tytul;
    $("pr-wstep").textContent = P.wstep;
    if (BK.czyKarta(P.zasady)) {
      B.wyczysc($("pr-zasady-miejsce")).appendChild(BK.karta(P.zasady, { prefiks: "pr-" }));
    } else {
      lista($("pr-zasady"), P.zasady);
      $("pr-definicje").textContent = P.definicje || "";
    }

    var t = B.wyczysc($("pr-przeglad"));
    var etyk = ["Nr", "Co robimy", "Ile warte rocznie (marża)", "Pewność", "Wdrożenie"];
    t.appendChild(el("thead", null, [wiersz(etyk, true)]));
    var tb = el("tbody");
    P.przeglad.forEach(function (r) {
      var href = "#priorytety?p=" + r.nr;
      tb.appendChild(wiersz([
        { attrs: { class: "nr-kom", "data-etykieta": etyk[0] }, dzieci: [el("a", { href: href, class: "nr", text: String(r.nr), "aria-label": "Pozycja " + r.nr }) ] },
        { attrs: { "data-etykieta": etyk[1] }, dzieci: [el("a", { href: href, text: r.co })] },
        { attrs: { "data-etykieta": etyk[2] }, dzieci: kwota(r.ile, r.ile_dopisek) },
        { attrs: { "data-etykieta": etyk[3] }, dzieci: pewnoscKom(r.pewnosc) },
        { attrs: { "data-etykieta": etyk[4], text: r.wdrozenie } }]));
    });
    t.appendChild(tb);

    var przeg = {};
    P.przeglad.forEach(function (r) { przeg[r.nr] = r; });
    var kont = B.wyczysc($("pr-karty"));
    P.karty.forEach(function (k) {
      var r = przeg[k.nr] || {};
      var p = k.pasek || { ile: r.ile, ile_dopisek: r.ile_dopisek, pewnosc: r.pewnosc, wdrozenie: r.wdrozenie };
      var art = el("article", { class: "karta priorytet", id: "pr-" + k.nr }, [
        el("div", { class: "priorytet-naglowek" }, [el("span", { class: "nr", text: String(k.nr) }), el("h3", { text: k.tytul })]),
        k.wniosek ? el("p", { class: "wniosek", text: k.wniosek }) : null,
        pasek(p)
      ]);
      // pozycja 1 (Safari): ten sam wykres co w karcie naprawy w lejku
      if (k.nr === 1 && B.hantleSafari) { var hs = B.hantleSafari(); if (hs) art.appendChild(hs); }
      if (k.sekcje && k.sekcje.length) {
        var dl = el("dl", { class: "sekcje" });
        k.sekcje.forEach(function (s) {
          dl.appendChild(el("dt", { text: s.tytul }));
          var dd = el("dd");
          if (s.punkty.length === 1) dd.appendChild(el("p", { text: s.punkty[0] }));
          else dd.appendChild(lista(el("ul"), s.punkty));
          dl.appendChild(dd);
        });
        art.appendChild(dl);
      }
      if (k.tabela) art.appendChild(tabelaKarty(k.tabela));
      if (k.tresc && k.tresc.length) art.appendChild(BK.bloki(k.tresc, el("div", { class: "tresc" })));
      if (k.zastrzezenie) art.appendChild(BK.zastrzezenie(k.zastrzezenie));
      var l = BK.linki(k.linki);
      if (l) art.appendChild(l);
      if (k.szczegoly && k.szczegoly.length) art.appendChild(BK.szczegoly(k.szczegoly, k.zrodlo));
      else if (k.zrodlo) art.appendChild(el("p", { class: "zrodlo", text: "Skąd liczby: " + k.zrodlo }));
      art.appendChild(el("p", { class: "wroc" }, [el("a", { href: "#priorytety", text: "Wróć do przeglądu" })]));
      kont.appendChild(art);
    });
    if (BK.czyKarta(P.nie_robimy)) {
      B.wyczysc($("pr-nie-robimy-miejsce")).appendChild(BK.karta(P.nie_robimy, { prefiks: "pr-", klasa: "karta-cicha" }));
    } else lista($("pr-nie-robimy"), P.nie_robimy);
    $("pr-zrodlo").textContent = P.zrodlo;
  }
  function tabelaKarty(T) {
    var B = b(), el = B.el;
    var t = el("table", { class: "tabela tabela-lejek tabela-kampanii" });
    t.appendChild(el("caption", { text: T.tytul }));
    t.appendChild(el("thead", null, [wiersz([""].concat(T.kolumny), true)]));
    var tb = el("tbody");
    T.wiersze.forEach(function (w) {
      var kom = [w.opis];
      w.komorki.forEach(function (c) {
        // komórka w kształcie z kontraktu (tekst albo {tekst, zmiana, stan, pod}) albo dotychczasowa {w, rok, minus}
        if (typeof c !== "object" || c === null || c.tekst !== undefined) { kom.push({ attrs: null, dzieci: BK.komorkaDzieci(c) }); return; }
        var dz = [el("span", { class: "b" + (c.minus ? " ujemne" : ""), text: c.w })];
        if (c.rok) dz.push(el("span", { class: "a", text: "pełny rok: " + c.rok }));
        kom.push({ attrs: null, dzieci: dz });
      });
      tb.appendChild(wiersz(kom));
    });
    t.appendChild(tb);
    return el("div", { class: "tabela-ramka" }, [t]);
  }
  BW.priorytety = {
    pokaz: function (q) {
      if (!gotowePr) { rysujPriorytety(); gotowePr = true; }
      if (q && q.get("p")) podswietl("pr-" + q.get("p"));
    }
  };

  // ------------------------------------------------------------ CZEGO NIE WIEMY
  var gotoweNw = false;
  function rysujNiewiadome() {
    var B = b(), el = B.el, $ = B.$, N = C.niewiadome;
    if (N.tytul) $("nw-tytul").textContent = N.tytul;
    $("nw-wstep").textContent = N.wstep;
    var t = B.wyczysc($("nw-tabela"));
    var etyk = ["Nr", "Czego nie wiemy", "Dlaczego to ważne", "Test albo brakujące dane", "Pozycja listy priorytetów"];
    t.appendChild(el("thead", null, [wiersz(etyk, true)]));
    var tb = el("tbody");
    N.wiersze.forEach(function (w) {
      tb.appendChild(wiersz([
        { attrs: { class: "nr-kom", "data-etykieta": etyk[0] }, dzieci: [el("span", { class: "nr", text: String(w.nr) })] },
        { attrs: { "data-etykieta": etyk[1] }, dzieci: [el("strong", { text: w.co })] },
        { attrs: { "data-etykieta": etyk[2], text: w.dlaczego } },
        { attrs: { "data-etykieta": etyk[3], text: w.test } },
        { attrs: { "data-etykieta": etyk[4] }, dzieci: [w.pozycja ? el("a", { href: "#priorytety?p=" + w.pozycja, text: "pozycja " + w.pozycja }) : "—"] }]));
    });
    t.appendChild(tb);
    $("nw-zrodlo").textContent = N.zrodlo;
  }
  BW.niewiadome = { pokaz: function () { if (!gotoweNw) { rysujNiewiadome(); gotoweNw = true; } } };
})();
