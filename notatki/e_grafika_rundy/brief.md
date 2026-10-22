# Brief: jak przedstawić graficznie narzędzie analityczne (runda 1, niezależna propozycja)

Jesteś jednym z trzech niezależnych recenzentów-projektantów. Każdy dostaje ten sam brief i pisze własną propozycję, bez wiedzy o pozostałych. Potem z trzech propozycji powstanie jedna wspólna wersja, którą każdy z was jeszcze oceni. Pisz po polsku, konkretnie, bez ogólników. Nie zmieniaj żadnych plików — tylko czytasz i piszesz odpowiedź.

## 1. Zlecenie właściciela projektu (słowa Kuby)

> Ustalcie wspólną wersję, jak przedstawić graficznie cały projekt (deliverables), aby był:
> 1. zgodny ze sztuką,
> 2. maksymalnie czytelny,
> 3. dodajcie, gdzie się da, graficzną reprezentację danych,
> 4. przeanalizujcie, w jaki sposób (wykresy, wykresy kołowe, infografiki) wspomóc odbiór danych i poprawić czytelność analizy.
>
> UI i kolorystyka, układ oddawanego produktu: wykorzystaj impeccable (zasady projektowania interfejsów), by poprawić warstwę wizualną.

## 2. Co to za produkt i kto go ogląda

- To rozwiązanie zadania rekrutacyjnego na stanowisko Head of B2C w firmie telemedycznej (pacjent płaci sam za konsultacje online i za program zniżkowy „TelemediGO”). Dane są syntetyczne, za dwa lata (X 2024 – IX 2026).
- Pytanie z zadania: czy to, co widać na dashboardzie (+52% nowych pacjentów, +61% zamówień, +50% przychodu, +40% TelemediGO), jest wzrostem, rozumianym jako jednocześnie więcej pacjentów i lepsza retencja. Najważniejsza część zadania: analiza kohortowa w rozdzielczości dziennej i znalezienie w danych zdarzeń, które zmieniły zachowanie pacjentów. Druga obowiązkowa część: lejek od wejścia na stronę do płatności, „gdzie i od kiedy tracimy pacjentów”.
- Zasady firmy z zadania: „Nie rób slajdów. Pokaż to, na czym faktycznie pracujesz.” Narzędzie ma być takie, „na którym samemu prowadziłoby się ten biznes na co dzień”, i otwierać się z linku.
- **Oddajemy:** (a) link do narzędzia — statyczna strona z 9 zakładkami: Czy to wzrost, Kohorty, Lejek, Po zakupie, Zdarzenia, Wynik biznesu, Jakość danych, Priorytety, Czego nie wiemy; (b) lista priorytetów (jest w narzędziu); (c) repozytorium z kodem, historią i notatkami, z plikiem README.md na GitHubie (odpowiedź w skrócie + jak czytać narzędzie).
- **Kto ogląda:** osoby z firmy (rekrutujący, przełożony stanowiska, ktoś z zarządu lub od danych). Otwierają link raz, w pierwszych minutach decydują, czy wnioski są mocne, a narzędzie dobre. Część obejrzy to na telefonie. Druga perspektywa: osoba, która codziennie prowadzi na tym biznes (patrzy na kohorty i lejek).

## 3. Co już jest (stan obecny)

- Kod strony: `narzedzie/index.html`, `narzedzie/styl.css`, `narzedzie/app.js` (lejek, nawigacja, wspólne funkcje), `narzedzie/widoki.js` (kohorty, po zakupie, zdarzenia, wynik, jakość), `narzedzie/widoki_c.js` (czy to wzrost, priorytety, czego nie wiemy), `narzedzie/karty.js` (rysowanie kart tekstowych, znaczników stanu, etykiet zmiany). Dane: `narzedzie/dane_strony/*.js` (przeliczone wcześniej; kształt danych w załączniku A na końcu briefu).
- Pełne teksty wszystkich zakładek, tak jak je widać na stronie: `analiza/wyniki/b_teksty_strony.md` (długi plik; przejrzyj, nie musisz czytać całości).
- Decyzje poprzedniej sesji wyglądu: `notatki/e_wyglad.md`.
- **Zrzuty ekranu** obecnej strony (komputer 1366 px i telefon 375 px), pocięte na ekrany: dołączone do tej wiadomości albo w katalogu podanym w poleceniu. Nazwa pliku: `<szerokość>_<zakładka>_<numer ekranu>.png`.
- Poprzednie wytyczne Kuby do wyglądu (część 3 rundy E, już wdrożone):
  - u góry ciemnogranatowy pasek z nazwą i zakładkami, białe karty z delikatnym cieniem na jasnoszarym tle, jeden kolor do odnośników i wyborów;
  - kolory stanu (dobrze, źle, uwaga) zawsze razem z ikoną SVG i słowem, nigdy sam kolor; bez znaków typu ▲;
  - bez kolorowych pasków po lewej stronie kart;
  - „Czy to wzrost”: werdykt ze znacznikiem „Nie”, trzy kafelki z dużą liczbą i jedną linijką podpisu, ponumerowane decyzje na pierwszy tydzień prowadzące do priorytetów; karty „Więcej pacjentów” i „Lepsza retencja” ze znacznikami „Tak” i „Nie”;
  - lejek: wykres kroków od wejścia do płatności (pasek z odsetkiem sesji, znacznik roku wcześniej, przejścia między krokami, wyróżnione przejście, które najbardziej się pogorszyło), domyślnie osoby, które jeszcze nie kupowały, reaguje na filtry;
  - priorytety: pewność jako kolorowe znaczniki (Wysoka, Średnia, Niska, Test), kwota wyróżniona, w karcie pasek „Ile warte · Pewność · Wdrożenie”;
  - zmiany rok do roku jako małe zielone albo czerwone etykiety ze strzałką;
  - filtry w jednym panelu nad treścią; telefon ma działać tak samo dobrze.
- Automatyczny detektor impeccable (statyczny przegląd kodu HTML/CSS/JS) nie zgłosił żadnych uchybień. Ocena projektowa (hierarchia, czytelność, dobór wykresów) jest więc po waszej stronie.

## 4. Twarde ograniczenia (nie do zmiany)

1. **Strona statyczna**, ścieżki względne (będzie pod podścieżką GitHub Pages), działa bez instalacji i bez konta, ma znacznik `noindex`.
2. **Nic z sieci:** żadnych bibliotek, czcionek ani obrazów pobieranych z internetu. Dostępna lokalnie jest tylko biblioteka wykresów **uPlot** (`narzedzie/lib/`). Inne wykresy rysujemy sami w SVG/HTML/CSS (tak powstał wykres kroków lejka). Czcionki: tylko systemowe (dziś Segoe UI Variable na Windowsie, systemowe na innych). Nowej biblioteki nie dodajemy, chyba że da się ją uzasadnić i dołączyć lokalnie — wtedy napisz to wprost jako osobną decyzję.
3. **Liczby i wnioski pochodzą wyłącznie z danych.** Każde zdanie z liczbą na stronie powstaje w eksporcie i przechodzi kontrolę zgodności z notatkami. Warstwa graficzna nie dopisuje nowych liczb w tekstach. Wykres liczony w przeglądarce z istniejących danych jest dopuszczalny (np. wykres kroków lejka), ale nie może tworzyć nowego twierdzenia w tekście. Jeśli propozycja wymaga nowego agregatu albo nowego tekstu, oznacz ją „wymaga eksportu” (robi to inna sesja).
4. **Kolory stanu** (dobrze, źle, uwaga) tylko razem z ikoną SVG i słowem. **Bez kolorowych pasków po lewej stronie kart.**
5. **Telefon (375 px) ma działać tak samo dobrze** jak komputer: bez przewijania strony w bok.
6. Strona jest po polsku; teksty są już przepisane (nagłówek karty = wniosek, jedno zdanie z wnioskiem pod nim, szczegóły w zwijanych sekcjach „Szczegóły”). Nie przepisujemy treści — projektujemy jej prezentację.
7. Czas: to ostatnia faza przed wysłaniem. Każdą propozycję oceń wysiłkiem S (godzina), M (pół dnia), L (dzień i więcej).

## 5. Zasady, na których opieramy ocenę

**impeccable (zasady projektowania interfejsów):**
- Tryb strony: przede wszystkim **„Operate”** (narzędzie do pracy: skanowalność, spójność, przewidywalna struktura, gęstość tam, gdzie użytkownik jej potrzebuje, „narzędzie znika w zadaniu”), z elementami **„Read”** (tekst analizy: miara wiersza 65–75 znaków, struktura dla zrozumienia).
- Kolor w trybie Operate: powściągliwy. Akcent tylko dla akcji, wyboru i stanu, nie do dekoracji. Spójny słownik stanów. Druga warstwa neutralna dla paneli.
- Typografia: jedna dobrze ustawiona rodzina, stała skala ról (stosunek 1,125–1,2), cyfry tabelaryczne w danych.
- Układ: test zmrużonych oczu (czy po rozmyciu widać element główny, drugorzędny i grupy w kolejności), grupowanie bliskością zamiast kolejnych pudełek, rytm ciasnych i hojnych odstępów, gęstość dopasowana do częstości użycia.
- Odrzucane domyślne wzorce: identyczne karty jako cała struktura strony; **karty zagnieżdżone w kartach**; szablon „duża liczba + mały podpis + dodatkowe statystyki” (wyjątek: Kuba wprost zamówił trzy kafelki z dużą liczbą — brief wygrywa); etykieta-kicker nad nagłówkiem; numery sekcji, chyba że kolejność niesie informację; gradientowy tekst; dekoracyjne szkło i rozmycia; kolorowa ramka po lewej; mini-wykresy (sparkline) i pierścienie postępu udające treść; znaki Unicode zamiast ikon.
- Ocena heurystykami Nielsena (widoczność stanu, zgodność z językiem użytkownika, spójność, rozpoznawanie zamiast pamiętania, estetyka i minimalizm, pomoc) oraz obciążeniem poznawczym (ściana opcji, „most pamięci” — trzeba pamiętać coś z innego miejsca, żargon, szum wizualny, niespójne wzorce, przełączanie kontekstu).

**Wykresy (zasady dataviz):**
- Najpierw forma według zadania danych, kolor na końcu. Czasem właściwa forma to nie wykres (kafelek z liczbą, tabela).
- Zadanie → forma: porównanie wielkości → słupki (siatka → mapa ciepła); trend → linia; jedna seria jest sednem → **wyróżnienie** (jedna w kolorze, reszta szara); odchylenie od bazy → słupki rozbieżne albo linia wobec bazy; część całości → słupek skumulowany (≤ 6 części, poziomy przy długich nazwach); przed → po na element → **wykres hantlowy (dumbbell)**.
- **Wykres kołowy / pierścieniowy:** tylko część całości na pierwszy rzut oka, najwyżej 6 części, nigdy do porównywania bliskich wartości; 2 części → kafelek albo pasek-licznik, nie koło.
- Nigdy dwóch osi Y. Kolory kategorii w stałej kolejności, kolor idzie za bytem, nie za pozycją. Kolory stanu zarezerwowane. Legenda przy ≥ 2 seriach, podpisy bezpośrednie wybiórczo (koniec linii, skrajność), nie liczba przy każdym punkcie. Cienkie znaki, siatka i osie jako ciche, ciągłe linie. Podpowiedź po najechaniu na każdym wykresie. Widok tabelaryczny jako zapas dostępności.

## 6. Twoje zadanie

Obejrzyj zrzuty i kod. Zaproponuj, jak przedstawić graficznie cały produkt. Odpowiedz dokładnie w tej strukturze (razem najwyżej ok. 3 000 słów):

**A. Werdykt ogólny** (3–5 zdań): co dziś działa, co najbardziej szkodzi czytelności i zgodności ze sztuką.

**B. System wizualny.** Konkretnie, z wartościami tam, gdzie to ma sens:
- kolory (tokeny: co zostaje, co zmienić i dlaczego; paleta serii wykresów; tła okresów porównania; tryb ciemny);
- typografia (role, rozmiary, grubości, cyfry);
- układ i siatka (szerokości, odstępy, rytm, karty — co zostaje kartą, co nie; jak uniknąć kart w kartach);
- komponenty (znacznik stanu, etykieta zmiany, kafelek, legenda, podpowiedź na wykresie, panel filtrów, tabela, odnośniki „Zobacz w danych”, sekcje zwijane);
- nawigacja między zakładkami (komputer i telefon).

**C. Zakładka po zakładce** (wszystkie 9). Dla każdej tabela:
`element | jak jest dziś | propozycja (forma graficzna, konkretnie) | z jakich danych (plik/klucz z załącznika A; „w przeglądarce” albo „wymaga eksportu”) | dlaczego czytelniej | wysiłek S/M/L`.
Szukaj miejsc, gdzie tekst albo tabela niesie liczby, które czyta się szybciej z obrazu. Dla każdej propozycji sprawdź, czy da się ją policzyć z danych, które strona już ma.

**D. Wykresy kołowe, infografiki i inne formy.** Gdzie ich użyć, a gdzie nie, z uzasadnieniem odnoszącym się do konkretnych danych tego projektu (np. mix źródeł pozyskania, udział nowych kampanii, mostek od dashboardu do danych oczyszczonych, rozkład spadku powrotu, lista priorytetów, oś zdarzeń). Rozważ też: wykres wodospadowy (mostek), hantle (rok do roku), małe wielokrotności (small multiples), mapę ciepła kohort, wykres skumulowany udziałów w czasie, oś czasu zdarzeń, diagram przepływu (Sankey) lejka.

**E. Pozostałe elementy oddawane:** README na GitHubie (co da się tam pokazać graficznie bez psucia zasad — np. diagram Mermaid, zrzut?), lista priorytetów, „Czego nie wiemy”.

**F. Czego nie robić** — ryzyka: przeładowanie, efekt „dashboardu dla ozdoby”, wykresy, które sugerują więcej, niż dane mówią, kolizje z zasadami z punktu 4.

**G. Dziesięć najważniejszych zmian** w kolejności „wartość dla czytelnika ÷ wysiłek”, każda w jednym, dwóch zdaniach, z oznaczeniem S/M/L i „w przeglądarce” / „wymaga eksportu”.

---

## Załącznik A. Kształt danych strony (`narzedzie/dane_strony/*.js`, klucze i typy, bez wartości)

Uwaga: `kohorty.js` ma dane na poziomie pacjenta (40 918 nowych pacjentów: dzień pierwszego zakupu `d`, dzień powrotu `r`, marża w oknach `m30…m180`, 12 wymiarów kategorii) — przeglądarka może z nich policzyć dowolny przekrój kohort. Pliki `lejek_<podział>.js` mają dzienne serie sesji i kroków lejka (`s`, `k1…k5`) dla każdej wartości podziału, typu sesji i rodzaju pacjenta. `wynik.js` ma dzienne serie przychodu i kosztów. `zdarzenia.js` ma listę wykrytych zdarzeń (data, obszar, tytuł, krótka nazwa, co się zmieniło, o ile, skąd wiemy).

```
## c.js: D.C
wygenerowano: tekst
wzrost: obiekt (7 kluczy)
  tytul: tekst
  wstep: tekst
  werdykt: obiekt (3 kluczy)
    znacznik: obiekt (2 kluczy)
      tekst: tekst
      stan: tekst
    tekst: tekst
    dopisek: tekst
  kafelki: lista[3] z dict
      liczba: tekst
      podpis: tekst
      dopisek: tekst
      zmiana: tekst
      stan: tekst
  decyzje: obiekt (2 kluczy)
    tytul: tekst
    punkty: lista[4] z dict
        {nr, tekst, href, dopisek}
  karty: lista[6] z dict
      tytul: tekst
      znacznik: obiekt (2 kluczy)
        {tekst, stan}
      wniosek: tekst
      tresc: lista[1] z dict
          {typ, punkty}
      zastrzezenie: tekst
      szczegoly: lista[1] z dict
          {typ, punkty}
      linki: lista[1] z dict
          {tekst, href}
      zrodlo: tekst
      etykieta: tekst
  zrodlo: tekst
priorytety: obiekt (7 kluczy)
  tytul: tekst
  wstep: tekst
  przeglad: lista[12] z dict
      nr: int
      co: tekst
      ile: tekst
      ile_dopisek: tekst
      pewnosc: obiekt (3 kluczy)
        {poziom, tekst, dopisek}
      wdrozenie: tekst
  zasady: obiekt (4 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[1] z dict
        {typ, punkty}
    szczegoly: lista[2] z dict
        {typ, punkty}
  karty: lista[12] z dict
      nr: int
      tytul: tekst
      wniosek: tekst
      pasek: obiekt (4 kluczy)
        {ile, ile_dopisek, pewnosc, wdrozenie}
      sekcje: lista[3] z dict
          {tytul, punkty}
      szczegoly: lista[6] z dict
          {typ, tekst}
      zrodlo: tekst
      linki: lista[2] z dict
          {tekst, href}
  nie_robimy: obiekt (3 kluczy)
    tytul: tekst
    tresc: lista[1] z dict
        {typ, punkty}
    szczegoly: lista[1] z dict
        {typ, punkty}
  zrodlo: tekst
niewiadome: obiekt (4 kluczy)
  tytul: tekst
  wstep: tekst
  wiersze: lista[21] z dict
      nr: int
      co: tekst
      dlaczego: tekst
      test: tekst
      pozycja: int
  zrodlo: tekst

## jakosc.js: D.jakosc
mostek: obiekt (1 kluczy)
  kroki: lista[4] z dict
      opis: tekst
      miary: obiekt (4 kluczy)
        {nowi, zamowienia, przychod, go}
duplikaty: obiekt (6 kluczy)
  od: tekst
  do: tekst
  kopie: int
  zamowienia_d: lista[730] z int
  kopie_d: lista[730] z int
  zdania: lista[2] z str
testy: obiekt (2 kluczy)
  kwartaly: lista[8] z dict
      kw: tekst
      n: int
  zdania: lista[4] z str
godzina: obiekt (3 kluczy)
  od: tekst
  do: tekst
  zdanie: tekst
drobne: lista[3] z str
czyste: lista[6] z str
start: tekst
dni: int
karta: obiekt (4 kluczy)
  tytul: tekst
  wniosek: tekst
  tresc: lista[1] z dict
      typ: tekst
      tekst: tekst
  zrodlo: tekst
karty: obiekt (6 kluczy)
  mostek: obiekt (6 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[1] z dict
        {typ, tekst}
    szczegoly: lista[2] z dict
        {typ, tekst}
    zrodlo: tekst
    wstaw: tekst
  duplikaty: obiekt (5 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[2] z dict
        {typ, tekst}
    szczegoly: lista[1] z dict
        {typ, tekst}
    zrodlo: tekst
  testy: obiekt (6 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[3] z dict
        {typ, tekst}
    zastrzezenie: tekst
    szczegoly: lista[2] z dict
        {typ, tekst}
    zrodlo: tekst
  godzina: obiekt (6 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[1] z dict
        {typ, tekst}
    zastrzezenie: tekst
    szczegoly: lista[1] z dict
        {typ, tekst}
    zrodlo: tekst
  drobne: obiekt (4 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[1] z dict
        {typ, punkty}
    zrodlo: tekst
  czyste: obiekt (4 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[1] z dict
        {typ, punkty}
    zrodlo: tekst

## kohorty.js: D.kohorty
n: int
d: lista[40918] z int
r: lista[40918] z int
okna: lista[4] z int
kat: obiekt (12 kluczy)
  kanal: tekst
  kampania: tekst
  kanal_z2: tekst
  kampania_z2: tekst
  urzadzenie: tekst
  przegladarka: tekst
  usluga: tekst
  znizka: tekst
  go0: tekst
  status1: tekst
  koszyk: tekst
  pora: tekst
wart: obiekt (12 kluczy)
  kanal: lista[9] z str
  kampania: lista[14] z str
  kanal_z2: lista[9] z str
  kampania_z2: lista[14] z str
  urzadzenie: lista[3] z str
  przegladarka: lista[9] z str
  usluga: lista[7] z str
  znizka: lista[6] z str
  go0: lista[2] z str
  status1: lista[4] z str
  koszyk: lista[5] z str
  pora: lista[4] z str
m30: lista[40918] z int
m60: lista[40918] z int
m90: lista[40918] z int
m180: lista[40918] z int
zdania: lista[4] z str
karta: obiekt (6 kluczy)
  tytul: tekst
  wniosek: tekst
  tresc: lista[3] z dict
      typ: tekst
      tekst: tekst
  zastrzezenie: tekst
  szczegoly: lista[8] z dict
      typ: tekst
      kolumny: lista[4] z str
      wiersze: lista[4] z dict
          {opis, komorki}
      tytul: tekst
  zrodlo: tekst

## lejek_calosc.js: D.lejek["calosc"]
start: tekst
dni: int
serie: lista[4] z dict
    typ: tekst
    pacjent: tekst
    w: tekst
    s: lista[730] z int
    k4: lista[730] z int
    k5: lista[730] z int

## lejek_kampania.js: D.lejek["kampania"]
start: tekst
dni: int
serie: lista[30] z dict
    {typ, pacjent, w, s, k4, k5}

## lejek_kanal.js: D.lejek["kanal"]
start: tekst
dni: int
serie: lista[20] z dict
    {typ, pacjent, w, s, k4, k5}

## lejek_przegladarka.js: D.lejek["przegladarka"]
start: tekst
dni: int
serie: lista[35] z dict
    {typ, pacjent, w, s, k4, k5}

## lejek_strona_wejscia.js: D.lejek["strona_wejscia"]
start: tekst
dni: int
serie: lista[30] z dict
    {typ, pacjent, w, s, k4, k5}

## lejek_system_przegladarka.js: D.lejek["system_przegladarka"]
start: tekst
dni: int
serie: lista[86] z dict
    {typ, pacjent, w, s, k4, k5}

## lejek_urzadzenie.js: D.lejek["urzadzenie"]
start: tekst
dni: int
serie: lista[12] z dict
    {typ, pacjent, w, s, k4, k5}

## lejek_urzadzenie_przegladarka.js: D.lejek["urzadzenie_przegladarka"]
start: tekst
dni: int
serie: lista[77] z dict
    {typ, pacjent, w, s, k4, k5}

## po_zakupie.js: D.po_zakupie
godziny: obiekt (4 kluczy)
  tytul: tekst
  kolumny: lista[6] z str
  wiersze: lista[24] z dict
      opis: tekst
      komorki: lista[5] z str
      blok: bool
  przypis: tekst
punktualnosc: lista[32] z dict
    spec: tekst
    pora: tekst
    nowa: bool
    n: lista[730] z int
    p15: lista[730] z int
    p30: lista[730] z int
zwroty: lista[15] z dict
    cel: tekst
    nowa: bool
    pierwsze: bool
    wszystkie: lista[730] z int
    anul: lista[730] z int
    nieodebr: lista[730] z int
    odbyte: lista[730] z int
    zwrocone: lista[730] z int
    zw_zl: lista[730] z int
    kl_zw: lista[730] z int
oceny: lista[47] z dict
    okres: int
    spec: tekst
    nowa: bool
    koszyk: tekst
    odbyte: int
    ocenione: int
    suma: float
    niskie: int
ruch: lista[14] z dict
    przedzial: tekst
    okres: int
    dni: int
    odbyte: int
    spoznione: int
    odbyte_stare: int
    spoznione_stare: int
zdania_ruch: lista[3] z str
zdania_punktualnosc: lista[4] z str
zdania_zwroty: lista[2] z str
zdania_oceny: lista[1] z str
start: tekst
dni: int
karty: obiekt (6 kluczy)
  punktualnosc: obiekt (6 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[2] z dict
        {typ, tekst}
    zastrzezenie: tekst
    szczegoly: lista[5] z dict
        {typ, tekst}
    zrodlo: tekst
  godziny: obiekt (5 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[2] z dict
        {typ, tekst}
    szczegoly: lista[3] z dict
        {typ, punkty}
    zrodlo: tekst
  ruch: obiekt (6 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[2] z dict
        {typ, tekst}
    zastrzezenie: tekst
    szczegoly: lista[4] z dict
        {typ, tekst}
    zrodlo: tekst
  powrot: obiekt (6 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[2] z dict
        {typ, tekst}
    zastrzezenie: tekst
    szczegoly: lista[3] z dict
        {typ, punkty}
    zrodlo: tekst
  zwroty: obiekt (6 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[2] z dict
        {typ, tekst}
    zastrzezenie: tekst
    szczegoly: lista[3] z dict
        {typ, tekst}
    zrodlo: tekst
  oceny: obiekt (6 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[1] z dict
        {typ, tekst}
    zastrzezenie: tekst
    szczegoly: lista[2] z dict
        {typ, tekst}
    zrodlo: tekst

## podsumowanie.js: D.P
meta: obiekt (5 kluczy)
  wygenerowano: tekst
  commit: tekst
  start: tekst
  koniec: tekst
  okresy: lista[2] z dict
      od: tekst
      do: tekst
      nazwa: tekst
etykiety: obiekt (24 kluczy)
  typ: obiekt (3 kluczy)
    zwykla: tekst
    zalogowana_od_wejscia: tekst
    samo_telemedigo: tekst
  pacjent: obiekt (2 kluczy)
    nie_kupowal: tekst
    kupowal_wczesniej: tekst
  kroki: obiekt (5 kluczy)
    k1: tekst
    k2: tekst
    k3: tekst
    k4: tekst
    k5: tekst
  podzial: obiekt (8 kluczy)
    calosc: tekst
    urzadzenie: tekst
    przegladarka: tekst
    system_przegladarka: tekst
    urzadzenie_przegladarka: tekst
    kanal: tekst
    kampania: tekst
    strona_wejscia: tekst
  urzadzenie: obiekt (3 kluczy)
    desktop: tekst
    mobile: tekst
    tablet: tekst
  kanal: obiekt (10 kluczy)
    afiliacja_ranking: tekst
    bezposrednie: tekst
    crm: tekst
    google_ads_marka: tekst
    google_ads_ogolne: tekst
    meta_pozyskanie: tekst
    meta_remarketing: tekst
    program_polecen: tekst
    tiktok: tekst
    wyszukiwarka_bezplatna: tekst
  kampania: obiekt (18 kluczy)
    bezposrednie: tekst
    bing_organic: tekst
    crm_go_upsell: tekst
    crm_reactivation: tekst
    crm_recepta_przypomnienie: tekst
    crm_sms_przypomnienie: tekst
    google_organic: tekst
    gs_brand: tekst
    gs_generic_erecepta: tekst
    gs_generic_l4: tekst
    gs_generic_lekarz_online: tekst
    gs_generic_specjalisci: tekst
    meta_prosp_l4_szybko: tekst
    meta_prosp_lekarz_online: tekst
    meta_rmkt_koszyk: tekst
    program_polecen: tekst
    rankinglekarzy_affiliate: tekst
    tt_prosp_l4_15min: tekst
  przegladarka: obiekt (3 kluczy)
    Instagram: tekst
    Facebook: tekst
    TikTok: tekst
  w_aplikacji: lista[3] z str
  obszary: obiekt (4 kluczy)
    lejek: tekst
    retencja: tekst
    obsluga: tekst
    jakosc: tekst
  usluga: obiekt (7 kluczy)
    internista_l4: tekst
    internista_e_recepta: tekst
    internista_konsultacja: tekst
    internista_skierowanie: tekst
    pediatra: tekst
    psychiatra: tekst
    inny_specjalista: tekst
  znizka: obiekt (2 kluczy)
    brak: tekst
    TelemediGO: tekst
  go0: obiekt (2 kluczy)
    tak: tekst
    nie: tekst
  status1: obiekt (4 kluczy)
    completed: tekst
    refunded: tekst
    cancelled: tekst
    no_show: tekst
  koszyk: obiekt (5 kluczy)
    a_do_5_min: tekst
    b_5_15_min: tekst
    c_15_30_min: tekst
    d_ponad_30_min: tekst
    brak_wizyty: tekst
  pora: obiekt (4 kluczy)
    a_rano_6_11: tekst
    b_poludnie_12_15: tekst
    c_wieczor_16_23: tekst
    d_noc_0_5: tekst
  spec: obiekt (4 kluczy)
    internista: tekst
    pediatra: tekst
    psychiatra: tekst
    inny: tekst
  cel: obiekt (4 kluczy)
    l4: tekst
    e_recepta: tekst
    konsultacja: tekst
    skierowanie: tekst
  grupa_ek: obiekt (4 kluczy)
    1_nowe_kampanie_L4: tekst
    2_pozostale_platne: tekst
    3_afiliacja_ranking: tekst
    4_bezplatne: tekst
  nowe_kampanie: lista[2] z str
  kanal_z2: obiekt (10 kluczy)
    afiliacja_ranking: tekst
    bezposrednie: tekst
    crm: tekst
    google_ads_marka: tekst
    google_ads_ogolne: tekst
    meta_pozyskanie: tekst
    meta_remarketing: tekst
    program_polecen: tekst
    tiktok: tekst
    wyszukiwarka_bezplatna: tekst
  kampania_z2: obiekt (18 kluczy)
    bezposrednie: tekst
    bing_organic: tekst
    crm_go_upsell: tekst
    crm_reactivation: tekst
    crm_recepta_przypomnienie: tekst
    crm_sms_przypomnienie: tekst
    google_organic: tekst
    gs_brand: tekst
    gs_generic_erecepta: tekst
    gs_generic_l4: tekst
    gs_generic_lekarz_online: tekst
    gs_generic_specjalisci: tekst
    meta_prosp_l4_szybko: tekst
    meta_prosp_lekarz_online: tekst
    meta_rmkt_koszyk: tekst
    program_polecen: tekst
    rankinglekarzy_affiliate: tekst
    tt_prosp_l4_15min: tekst
  system_przegladarka: obiekt (22 kluczy)
    Android Chrome: tekst
    Android Facebook: tekst
    Android Firefox: tekst
    Android Instagram: tekst
    Android Opera: tekst
    Android Samsung Internet: tekst
    Android TikTok: tekst
    Linux Chrome: tekst
    Linux Firefox: tekst
    Windows Chrome: tekst
    Windows Edge: tekst
    Windows Firefox: tekst
    Windows Opera: tekst
    iOS Chrome: tekst
    iOS Facebook: tekst
    iOS Firefox: tekst
    iOS Instagram: tekst
    iOS Safari: tekst
    iOS TikTok: tekst
    macOS Chrome: tekst
    macOS Firefox: tekst
    macOS Safari: tekst
  urzadzenie_przegladarka: obiekt (21 kluczy)
    desktop Chrome: tekst
    desktop Edge: tekst
    desktop Firefox: tekst
    desktop Opera: tekst
    desktop Safari: tekst
    mobile Chrome: tekst
    mobile Facebook: tekst
    mobile Firefox: tekst
    mobile Instagram: tekst
    mobile Opera: tekst
    mobile Safari: tekst
    mobile Samsung Internet: tekst
    mobile TikTok: tekst
    tablet Chrome: tekst
    tablet Facebook: tekst
    tablet Firefox: tekst
    tablet Instagram: tekst
    tablet Opera: tekst
    tablet Safari: tekst
    tablet Samsung Internet: tekst
    tablet TikTok: tekst
wzrost: obiekt (3 kluczy)
  pacjenci: obiekt (4 kluczy)
    n1: int
    n2: int
    wzrost: float
    zdanie: tekst
  retencja: obiekt (2 kluczy)
    okna: lista[3] z dict
        {dni, p1, p2, n1, n2, do1, do2}
    zdanie: tekst
  dashboard: obiekt (1 kluczy)
    zdanie: tekst
lejek_naglowek: obiekt (11 kluczy)
  zdania: lista[4] z str
  naprawy: lista[2] z dict
      tytul: tekst
      tekst: tekst
      link: tekst
  osobne: lista[3] z str
  safari: obiekt (19 kluczy)
    data: tekst
    przed: lista[2] z str
    po60: lista[2] z str
    przed_proc: float
    po60_proc: float
    po_proc: float
    przed_k2: int
    po60_k2: int
    przed_od: tekst
    przed_do: tekst
    po60_od: tekst
    po60_do: tekst
    reszta_przed_proc: float
    reszta_po60_proc: float
    utracone_od: int
    utracone_do: int
    dni_po: int
    na30_od: float
    na30_do: float
  konw: lista[2] z float
  sesje: lista[2] z int
  platnosci: lista[2] z int
  granica: tekst
  karta: obiekt (7 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[1] z dict
        {typ, punkty}
    zastrzezenie: tekst
    szczegoly: lista[3] z dict
        {typ, punkty}
    linki: lista[1] z dict
        {tekst, href}
    zrodlo: tekst
  naprawy_karty: lista[2] z dict
      tytul: tekst
      znacznik: obiekt (2 kluczy)
        {tekst, stan}
      wniosek: tekst
      tresc: lista[1] z dict
          {typ, punkty}
      szczegoly: lista[1] z dict
          {typ, tekst}
      linki: lista[1] z dict
          {tekst, href}
      zrodlo: tekst
  osobne_karta: obiekt (2 kluczy)
    tytul: tekst
    tresc: lista[3] z dict
        {typ, tekst}

## wynik.js: D.wynik
dni: int
start: tekst
serie: obiekt (13 kluczy)
  przychod_pierwsze: lista[730] z int
  przychod_powtorne: lista[730] z int
  zaplaty: lista[730] z int
  zwroty: lista[730] z int
  koszt_lekarza: lista[730] z int
  zamowienia: lista[730] z int
  nowi: lista[730] z int
  go: lista[730] z int
  go_n: lista[730] z int
  wydatki_google: lista[730] z float
  wydatki_meta: lista[730] z float
  wydatki_tiktok: lista[730] z int
  prowizja: lista[730] z int
zdania: lista[7] z str
ekonomia: obiekt (3 kluczy)
  wiersze: lista[166] z dict
      okres: int
      regula: tekst
      okno: int
      poziom: tekst
      klucz: tekst
      nowi: int
      wydatki: float
      prowizja: float
      cac: float
      marza: float
      wynik: float
      od: float
      do: float
      razem: float
      powrot: float
  zdania: lista[3] z str
  karta: obiekt (6 kluczy)
    tytul: tekst
    wniosek: tekst
    tresc: lista[2] z dict
        {typ, tekst}
    zastrzezenie: tekst
    szczegoly: lista[5] z dict
        {typ, tekst}
    zrodlo: tekst
granica: tekst
karta: obiekt (6 kluczy)
  tytul: tekst
  wniosek: tekst
  tresc: lista[3] z dict
      typ: tekst
      tekst: tekst
  zastrzezenie: tekst
  szczegoly: lista[20] z dict
      typ: tekst
      kolumny: lista[4] z str
      wiersze: lista[4] z dict
          {opis, komorki}
      tytul: tekst
  zrodlo: tekst

## zdarzenia.js: D.zdarzenia
lista: lista[14] z dict
    id: tekst
    obszar: tekst
    od: tekst
    rodzaj: tekst
    tytul: tekst
    co: tekst
    ile: tekst
    skad: tekst
    link: tekst
    krotko: tekst
wykryte: obiekt (2 kluczy)
  kolumny: lista[11] z str
  wiersze: lista[245] z list
obszary: lista[4] z dict
    id: tekst
    puste: tekst
karta: obiekt (5 kluczy)
  tytul: tekst
  wniosek: tekst
  tresc: lista[1] z dict
      typ: tekst
      tekst: tekst
  zastrzezenie: tekst
  szczegoly: lista[1] z dict
      typ: tekst
      tekst: tekst
```
