/* Widoki z wynikiem punktu C: „Czy to wzrost”, „Priorytety”, „Czego nie wiemy”.
   Dane z dane_strony/c.js (tworzy je analiza/b2_eksport_c.py, uruchamiany też przez analiza/b_eksport.py).
   Ten plik nie wpisuje żadnych liczb: wszystkie zdania i wartości w tabelach przychodzą gotowe z eksportu.
   Pomocnicze funkcje (el, $, mostek) udostępnia app.js jako window.B. */
(function () {
  "use strict";
  var BW = window.BW = window.BW || {};
  var C = window.D.C;
  var b = function () { return window.B; };

  function lista(cel, punkty) {
    var B = b();
    B.wyczysc(cel);
    punkty.forEach(function (p) { cel.appendChild(B.el("li", { text: p })); });
    return cel;
  }
  function linkiDanych(cel, linki) {
    var B = b();
    B.wyczysc(cel);
    cel.appendChild(B.el("span", { class: "linki-etykieta", text: "Zobacz w danych: " }));
    linki.forEach(function (l, i) {
      if (i) cel.appendChild(document.createTextNode(" · "));
      cel.appendChild(B.el("a", { href: l.href, text: l.tekst }));
    });
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

  // ------------------------------------------------------------ CZY TO WZROST
  var gotoweWz = false;
  function rysujWzrost() {
    var B = b(), el = B.el, $ = B.$, W = C.wzrost, O = B.O;
    $("wz-werdykt").textContent = W.werdykt;
    B.akapity($("wz-puenta"), W.puenta);

    $("wz-pacjenci-liczba").textContent = W.pacjenci.liczba;
    $("wz-pacjenci-podpis").textContent = W.pacjenci.podpis;
    lista($("wz-pacjenci-punkty"), W.pacjenci.punkty);

    $("wz-retencja-liczba").textContent = W.retencja.liczba;
    $("wz-retencja-podpis").textContent = W.retencja.podpis;
    var t = B.wyczysc($("wz-retencja-tabela"));
    t.appendChild(el("thead", null, [wiersz(["Powrót w ciągu", "Okres 1 (" + O[0].nazwa + ")", "Okres 2 (" + O[1].nazwa + ")", "Zmiana"], true)]));
    var tb = el("tbody");
    W.retencja.okna.forEach(function (o) {
      tb.appendChild(wiersz([o.dni + " dni", o.tekst1, o.tekst2,
        { attrs: { class: "delta " + (o.p2 >= o.p1 ? "plus" : "minus"), text: o.zmiana } }]));
    });
    t.appendChild(tb);
    lista($("wz-retencja-punkty"), W.retencja.punkty);

    $("wz-zamkniecie").textContent = W.zamkniecie;
    $("wz-safari").textContent = W.safari;
    $("wz-kwartaly-naglowek").textContent = W.kwartaly.naglowek;
    var k = B.wyczysc($("wz-kwartaly"));
    k.appendChild(el("thead", null, [wiersz(["Kwartał", "Marża", "Rok wcześniej", "Zmiana marży", "Wydatki na kampanie",
      "Rok wcześniej", "Wydatki: ile razy więcej"], true)]));
    var kb = el("tbody");
    W.kwartaly.wiersze.forEach(function (r) {
      kb.appendChild(wiersz([r.kw, r.m2, r.m1, { attrs: { class: "delta " + (r.minus ? "minus" : "plus"), text: r.zm } },
        r.w2, r.w1, r.il]));
    });
    k.appendChild(kb);
    lista($("wz-kwartaly-punkty"), W.kwartaly.punkty);

    var z = B.wyczysc($("wz-zastrzezenia"));
    W.zastrzezenia.forEach(function (x) { z.appendChild(el("li", null, [el("strong", { text: x.tytul }), " " + x.tekst])); });

    $("wz-dashboard-zdanie").textContent = B.P.wzrost.dashboard.zdanie;
    B.mostek($("wz-mostek"));
    linkiDanych($("wz-linki"), W.linki);
    $("wz-zrodlo").textContent = W.zrodlo;
  }
  BW.wzrost = { pokaz: function () { if (!gotoweWz) { rysujWzrost(); gotoweWz = true; } } };

  // ------------------------------------------------------------ PRIORYTETY
  var gotowePr = false;
  function rysujPriorytety() {
    var B = b(), el = B.el, $ = B.$, P = C.priorytety;
    $("pr-wstep").textContent = P.wstep;
    lista($("pr-zasady"), P.zasady);
    $("pr-definicje").textContent = P.definicje;

    var t = B.wyczysc($("pr-przeglad"));
    var etyk = ["Nr", "Co robimy", "Ile warte rocznie (marża)", "Pewność", "Wdrożenie"];
    t.appendChild(el("thead", null, [wiersz(etyk, true)]));
    var tb = el("tbody");
    P.przeglad.forEach(function (r) {
      var href = "#priorytety?p=" + r.nr;
      tb.appendChild(wiersz([
        { attrs: { class: "nr-kom", "data-etykieta": etyk[0] }, dzieci: [el("a", { href: href, class: "nr", text: String(r.nr) })] },
        { attrs: { "data-etykieta": etyk[1] }, dzieci: [el("a", { href: href, text: r.co })] },
        { attrs: { "data-etykieta": etyk[2], text: r.ile } }, { attrs: { "data-etykieta": etyk[3], text: r.pewnosc } },
        { attrs: { "data-etykieta": etyk[4], text: r.wdrozenie } }]));
    });
    t.appendChild(tb);

    var przeg = {};
    P.przeglad.forEach(function (r) { przeg[r.nr] = r; });
    var kont = B.wyczysc($("pr-karty"));
    P.karty.forEach(function (k) {
      var r = przeg[k.nr];
      var art = el("article", { class: "karta priorytet", id: "pr-" + k.nr }, [
        el("div", { class: "priorytet-naglowek" }, [el("span", { class: "nr", text: String(k.nr) }), el("h3", { text: k.tytul })]),
        el("p", { class: "priorytet-meta" }, [
          el("span", null, [el("span", { class: "przypis", text: "Ile warte rocznie: " }), r.ile]),
          el("span", null, [el("span", { class: "przypis", text: "Pewność: " }), r.pewnosc]),
          el("span", null, [el("span", { class: "przypis", text: "Wdrożenie: " }), r.wdrozenie])])
      ]);
      var dl = el("dl", { class: "sekcje" });
      k.sekcje.forEach(function (s) {
        dl.appendChild(el("dt", { text: s.tytul }));
        var dd = el("dd");
        if (s.punkty.length === 1) dd.appendChild(el("p", { text: s.punkty[0] }));
        else dd.appendChild(lista(el("ul"), s.punkty));
        dl.appendChild(dd);
      });
      art.appendChild(dl);
      if (k.tabela) art.appendChild(tabelaKarty(k.tabela));
      art.appendChild(linkiDanych(el("p", { class: "linki-danych" }), k.linki));
      art.appendChild(el("p", { class: "przypis", text: "Skąd liczby: " + k.zrodlo }));
      art.appendChild(el("p", { class: "przypis" }, [el("a", { href: "#priorytety", text: "↑ Wróć do przeglądu" })]));
      kont.appendChild(art);
    });
    lista($("pr-nie-robimy"), P.nie_robimy);
    $("pr-zrodlo").textContent = P.zrodlo;
  }
  function tabelaKarty(T) {
    var B = b(), el = B.el;
    var t = el("table", { class: "tabela tabela-lejek tabela-kampanii" });
    t.appendChild(el("caption", { class: "przypis", text: T.tytul }));
    t.appendChild(el("thead", null, [wiersz([""].concat(T.kolumny), true)]));
    var tb = el("tbody");
    T.wiersze.forEach(function (w) {
      var kom = [w.opis];
      w.komorki.forEach(function (c) {
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
