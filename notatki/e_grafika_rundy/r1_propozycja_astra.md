## A. Werdykt ogólny

**Zachowałbym obecną identyfikację, a przebudował hierarchię informacji i sposób czytania danych.** Granatowy nagłówek, jednoznaczny werdykt, decyzje prowadzące do priorytetów i wykres kroków lejka już dobrze służą zadaniu. Najbardziej przeszkadzają rozbudowane wstępy przed częścią roboczą, szerokie tabele z drobnym tekstem oraz pomniejszanie wykresów na telefonie. Najważniejsza poprawka merytoryczno-wizualna dotyczy mapy kohort: kod skaluje kolory osobno dla każdej kolumny, więc identyczny odcień oznacza różne wartości powrotu. Propozycja wynika z przeglądu zrzutów, kodu, danych i notatek; nie zmieniałem plików ani nie testowałem interakcji w przeglądarce.

## B. System wizualny

Stosuję zasady impeccable podane w briefie. Nie znalazłem osobnej dostępnej umiejętności impeccable.

**Kolory — S; uporządkowanie przypisania serii — M.**

- Zostają: `--bar: #13213a`, `--plane: #eef1f5`, `--surface: #ffffff`, `--accent: #1f5fcc`, `--ink: #172133`.
- Zostają obecne tokeny stanów. Zieleń, czerwień i bursztyn nie powinny jednocześnie identyfikować zwykłych kategorii.
- Paleta kategorii: niebieski `#2463C5`, fioletowy `#7652A3`, turkusowy `#087E8B`, grafitowy `#526176`. Domyślnie najwyżej cztery serie; więcej przez świadomy wybór albo osobne wykresy.
- Kolor przypisujemy do klucza kategorii, nie kolejności zaznaczania. Dziś funkcje przydzielania kolorów zwalniają kolor po odznaczeniu serii.
- Okres A: `#F5F6F8`; okres B: `#EDF3FC`. Nad obszarem nazwa i daty. Barwa tła nie zastępuje podpisu.
- Tryb ciemny już istnieje. Zachować, rozjaśnić serie i sprawdzić także mapę kohort, której paleta jest obecnie wpisana osobno w JavaScript. Nie projektować drugiego układu.

**Typografia — S.**

Jedna rodzina systemowa pozostaje. Tytuł zakładki: 26/32 px, na telefonie 22/28 px. Nagłówek sekcji: 18/24 px, grubość 650. Tekst: 15/23 px, na telefonie 16/24 px. Tabele: 14/20 px; przypisy: 13/18 px. Liczby główne: 32/36 px. Cyfry tabelaryczne we wszystkich danych, datach, legendach i podpowiedziach. Akapity ograniczyć do `72ch`, zamiast obecnych szerokości dochodzących do 900 px.

**Układ — M.**

Zostawić kontener 1320 px i marginesy 24 px na komputerze, 16 px na telefonie. Rytm odstępów: 8, 12, 16, 24 i 32 px. Karta oznacza samodzielne zadanie: werdykt, analizę z wykresem albo konkretny priorytet. Tabela, legenda, filtry lokalne i zastrzeżenie są częściami tego zadania, bez kolejnych zaokrąglonych pudełek.

Zastrzeżenie: ikona, pogrubiona etykieta i tekst na wspólnym tle karty. Pasek priorytetu: trzy pola rozdzielone liniami. Trzy zamówione kafelki pozostają wyjątkiem. Dwie sąsiednie karty nie muszą mieć jednakowej wysokości — obecnie powstają duże puste przestrzenie.

**Komponenty — S–M każdy.**

- **Stan i zmiana:** ikona SVG, wartość oraz widoczne słowo. Dziś „lepiej/gorzej” w etykietach tabel jest ukryte dla wzroku. Jednostkę zmiany podać w nagłówku kolumny, np. „Zmiana w punktach procentowych”.
- **Legenda:** nazwa, próbka linii i aktualna wartość. Bez kursora pokazuje nazwy; nie zajmuje miejsca rzędami pustych kresek.
- **Podpowiedź:** data, seria, wartość i liczebność. Otwierana najechaniem, dotknięciem oraz klawiaturą; na telefonie jako panel pod wykresem.
- **Filtry:** stale widoczne podstawowe ustawienia; pozostałe w rozwijanej części tego samego panelu. Aktywne filtry zawsze widoczne, nawet po zwinięciu. Osobno zaznaczyć, że wnioski wprowadzające dotyczą analizy bazowej.
- **Tabela:** liczby do prawej, nazwy do lewej. Wybrany wiersz sygnalizuje checkbox i delikatne tło. Na telefonie domyślnie wybrana miara z obiema wartościami okresów; pełna tabela dostępna osobno.
- **Odnośniki i szczegóły:** zachować konkretne nazwy „Zobacz w danych”. Cel otwiera właściwe filtry i wyróżnia wskazaną sekcję. Natywne sekcje zwijane pozostają; obszar dotknięcia minimum 44 px.

**Nawigacja — M.**

Na komputerze zachować dziewięć zakładek i aktywne podkreślenie. Na telefonie zastąpić trzy rzędy pigułek przyciskiem z nazwą bieżącej zakładki, rozwijającym pełną listę. Informacja o danych syntetycznych pozostaje widoczna. Po przewinięciu wystarczy niewysoki pasek nawigacyjny; nie przyklejać całego nagłówka.

## C. Zakładka po zakładce

S = około godziny, M = pół dnia, L = dzień lub więcej. Szacunki obejmują dopracowanie telefonu. „W przeglądarce” oznacza brak zmiany eksportu; obejmuje także samą prezentację HTML/CSS.

### 1. Czy to wzrost

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Werdykt i decyzje | Dobra hierarchia, ale duża wysokość na telefonie | Zachować trzy kafelki; skrócić odstępy, spłaszczyć ich wnętrza. Decyzje bez dodatkowych ramek | `c.js`: `D.C.wzrost.werdykt`, `kafelki`, `decyzje`; **w przeglądarce** | Szybsze dojście od odpowiedzi do działania | S |
| Retencja | Tabela czterech okien | Cztery poziome hantle: rok wcześniej i ostatni rok, wspólna oś procentowa. Tabela pod przełącznikiem | `kohorty.js`: `d`, `r`; okresy z `podsumowanie.js`; **w przeglądarce**, z obecną regułą dojrzałości kohort | Widać spadek w każdym oknie | M |
| Sprzedaż TelemediGO | Tabela trzech sposobów zakupu | Trzy pary poziomych słupków: liczba zakupów w obu latach | `c.js`: tabela w `wzrost.karty[].tresc`; wartości są tekstem — **wymaga eksportu** pól liczbowych | Widać, które sposoby zakupu zwiększyły sprzedaż | M |

### 2. Kohorty

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Kolejność i filtry | Rozbudowany panel, potem szeroka tabela | Podstawowe filtry, wykres dzienny, tabela przekrojów, macierz. Pozostałe filtry rozwijane; dzienna rozdzielczość pozostaje domyślna | `kohorty.js`: `kat`, `wart`, `d`, `r`, `m30…m180`; **w przeglądarce** | Obowiązkowa analiza dzienna pojawia się wcześniej | M |
| Mapa kohort | Kolor zależy od kwantyli osobnej kolumny; początek od października 2024 | Wspólna, niezmienna skala z legendą. Przycisk przejścia do ostatniej dojrzałej kohorty i wybranego zdarzenia. Brak pełnego okna odróżniony od zera | `kohorty.js`: `d`, `r`; `zdarzenia.js`: `lista`; **w przeglądarce** | Kolor staje się porównywalny, a istotne daty dostępne | M |
| Trend i skład pacjentów | Trzy linie oraz liczne znaczniki zdarzeń | Pod trendem opcjonalny miesięczny wykres udziałów: nowe kampanie i pozostali. Wspólna oś czasu, osobne osie pionowe | `d`, `kat.kampania`, `wart.kampania`; `D.P.etykiety.nowe_kampanie`; **w przeglądarce** | Pozwala zestawić zmianę struktury ze zmianą retencji bez sugerowania przyczyny | M |

### 3. Lejek

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Kroki | Czytelne paski i znacznik poprzedniego roku | Zachować. Oddzielić wizualnie „od wszystkich sesji” od „przechodzi dalej”; pokazać jednostkę zmiany | `lejek_<podział>.js`: `s`, `k1…k5`; **w przeglądarce**. Sprawdzone: zwykłe sesje mają pełne kroki | Chroni przed mieszaniem mianowników | S |
| Awaria Safari | Wniosek tekstowy nad częścią roboczą | Dwie hantle: Safari na iOS oraz pozostałe przeglądarki, te same okresy przed i po | `podsumowanie.js`: `lejek_naglowek.safari.przed_proc`, `po60_proc`, `reszta_przed_proc`, `reszta_po60_proc`, daty; **w przeglądarce** | Pokazuje skalę i lokalność pogorszenia | M |
| Tabela przeglądarek | Wiele kolumn i domyślnie pięć linii | Wybór jednego przejścia: nazwa, oba okresy, zmiana i liczebność. Pełna tabela jako drugi widok | `lejek_przegladarka.js`: `serie`; **w przeglądarce** | W telefonie można porównywać wyniki bez szukania kolumn | M |

### 4. Po zakupie

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Punktualność | Cztery równorzędne kolorowe linie | Rano wyróżnione, pozostałe serie neutralne z różnymi kreskowaniami; wybrana seria może przejąć wyróżnienie | `po_zakupie.js`: `punktualnosc[].n`, `p15`, `p30`, `pora`, `spec`; **w przeglądarce** | Wzrok trafia na główną zmianę | S |
| Godziny wizyt | Tabela 24 godzin | Dwa wykresy pod sobą: internista i pozostali; godziny na osi poziomej, dwie linie okresów, wspólna skala | `godziny.wiersze[].komorki` zawierają tekst; **wymaga eksportu** liczników i mianowników | Ujawnia blok opóźnień i porównanie z pozostałymi lekarzami | M |
| Zwroty i oceny | Kolejne obszerne tabele | Zwroty: hantle odsetka zwróconych wizyt. Oceny: punkty średniej na skali ocen, obok liczba ocen i udział ocenionych wizyt | `zwroty`: `zwrocone`, `odbyte`; `oceny`: `suma`, `ocenione`, `odbyte`; **w przeglądarce** | Pokazuje różnice i wielkość podstawy porównania | M |

### 5. Zdarzenia

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Oś czasu | Na komputerze użyteczna; na telefonie pomniejszona do miniatury | Komputer: zachować tory. Telefon: lista miesięcy z datą, nazwą i obszarem, prowadząca do opisu | `zdarzenia.js`: `lista`, `obszary`; **w przeglądarce** | Nazwy pozostają czytelne i dotykalne | M |
| Znaczniki na innych wykresach | Numery nachodzą na siebie | Domyślnie zdarzenia związanego obszaru; bliskie znaczniki grupowane. Dotknięcie rozwija nazwy i daty | `lista[].obszar`, `od`, `krotko`, `link`; **w przeglądarce** | Usuwa konieczność pamiętania numerów | M |

### 6. Wynik biznesu

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Przychód, koszty, marża | Cztery linie, największa dominuje | Trzy wykresy miesięczne: przychód; koszty lekarzy i pozyskania; marża. Wspólny czas, jawne skale w złotych | `wynik.js`: `serie`; istniejące obliczenia `skladowe()`; **w przeglądarce** | Trend marży nie ginie pod przychodem | M |
| Ekonomia kampanii | Szeroka tabela | Poziome słupki rozbieżne wyniku na pacjenta; obok siebie dwie reguły przypisania. Jeden wybrany horyzont | `ekonomia.wiersze`: `wynik`, `regula`, `okno`, `okres`, `klucz`; **w przeglądarce** | Widać straty oraz zależność wyniku od przypisania | M |

### 7. Jakość danych

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Dashboard a dane oczyszczone | Cztery miary i cztery etapy w tabeli | Cztery hantle wzrostu: surowe–oczyszczone. Szczegóły korekt pozostają w tabeli | `jakosc.js`: `mostek.kroki[].miary.*.wzrost`; **w przeglądarce** | Natychmiast pokazuje wielkość korekty każdej miary | M |
| Duplikaty i testy | Linia z pomarańczowymi słupkami; poprawne słupki kwartalne | Zachować formy. Zaznaczyć przedział duplikatów, zastąpić pomarańcz kategorią neutralną | `duplikaty.od`, `do`, `zamowienia_d`, `kopie_d`; `testy.kwartaly`; **w przeglądarce** | Poprawia odczyt bez dokładania wykresów | S |

### 8. Priorytety

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Przegląd mobilny | Każda pozycja rozpisana w długi blok | Numer i działanie, niżej kwota z niezbędnym zastrzeżeniem, następnie pewność i czas. Dodatkowe objaśnienia rozwijane | `c.js`: `priorytety.przeglad`; **w przeglądarce** | Pozwala objąć wzrokiem więcej decyzji | M |
| Karta działania | Dobry pasek trzech parametrów, wiele pudełek | Zachować parametry jako płaski wiersz; dodać powiązane niewiadome pod odnośnikami do danych | `priorytety.karty`; `niewiadome.wiersze[].pozycja`; **w przeglądarce** | Łączy decyzję z warunkami jej oceny | S |

### 9. Czego nie wiemy

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Lista pytań | Długa tabela tekstowa | Filtr według powiązanego priorytetu. Widoczne pytanie i proponowany test; uzasadnienie rozwijane | `c.js`: `niewiadome.wiersze`; **w przeglądarce** | Czytelnik znajduje niewiadome dotyczące konkretnej decyzji | M |
| Powiązania | Odnośnik „pozycja 9” | Numer wraz z nazwą działania pobraną z przeglądu priorytetów | `wiersze[].pozycja`, `priorytety.przeglad[].co`; **w przeglądarce** | Nie wymaga pamiętania numeracji | S |

## D. Wykresy kołowe, infografiki i inne formy

**Nie proponuję wykresu kołowego w podstawowej wersji.** Udział nowych kampanii w pacjentach ma dwie części — lepszy będzie poziomy pasek udziałów. Kanałów pozyskania jest więcej niż sześć; poziome słupki pozwolą porównać je bez sztucznego grupowania.

- **Wodospad:** dobry do korekty liczby zamówień albo przychodu. Liczyć różnice kolejnych `p1` lub `p2` z `jakosc.mostek`, osobno dla każdego okresu. Nie odejmować liczby testów z dwóch lat od zamówień jednego roku. To opcja **M, w przeglądarce**, po prostszych hantlach wzrostu.
- **Rozkład spadku powrotu:** nie rysować koła „przyczyn”. Ewentualny mostek jest opisową dekompozycją, z widocznym zastrzeżeniem. Proponuję **wymaga eksportu**, aby zatwierdzony rozkład i jego nazwy miały jedno źródło.
- **Hantle:** najlepsze dla retencji, Safari i zwrotów. Punkty oznaczają dwa okresy, nie przedział niepewności.
- **Małe wielokrotności:** przydatne dla wyniku biznesu i porównania punktualności. Muszą mieć czytelne osie; nie mogą stać się miniaturami.
- **Mapa kohort:** zachować. Stałe przedziały kolorów, np. granice 0, 5, 10, 15, 20, 30, 50 i 100%, wspólne dla kolumn i filtrów. Legenda pokazuje nierówne przedziały.
- **Udziały w czasie:** stosować do składu nowych pacjentów; liczebność w podpowiedzi. Nie zastępuje wykresu liczby pacjentów.
- **Sankey:** odrzucić. Obecny lejek jest liniowy, a agregaty nie opisują kompletnych indywidualnych ścieżek.
- **Infografika:** tylko jako prosty przewodnik po narzędziu. Bez dekoracyjnych ikon medycznych i strzałek sugerujących dowiedzioną przyczynowość.

## E. Pozostałe elementy oddawane

**README — S.** Na górze rzeczywisty link do narzędzia; obecnie jest placeholder. Pod krótką odpowiedzią jeden lokalny zrzut obejmujący werdykt i decyzje, z opisem alternatywnym. Zrzut jest ilustracją, nie jedynym nośnikiem odpowiedzi. Krótki diagram Mermaid może pokazać ścieżkę czytania: „Werdykt → Kohorty i lejek → Priorytety → Niewiadome”. Nie powielać dziewięciu zakładek jako galerii.

**Lista priorytetów — S.** Zachować jedną wersję w narzędziu, a z README prowadzić odnośnikiem. Nie budować wykresu sumującego potencjały: kwoty mają różne warunki, horyzonty i mogą się nakładać.

**Niewiadome — S.** Traktować jako zaplecze decyzji, dostępne także z konkretnego priorytetu. Nie nadawać automatycznie statusów „rozwiązane” lub „pilne”, których dane nie zawierają.

## F. Czego nie robić

- Nie dodawać wykresu obok każdej tabeli. Domyślnie jedna reprezentacja, druga pod przełącznikiem.
- Nie parsować zdań i sformatowanych komórek jako źródła liczb do nowych wykresów.
- Nie przedstawiać przedziałów scenariuszy jako przedziałów ufności.
- Nie utożsamiać udziału nowych kampanii ze zmierzonym wpływem reklam.
- Nie zmieniać dziennych kohort na miesięczne tylko dlatego, że łatwiej je narysować.
- Nie usuwać liczebności, informacji o dojrzałości kohort ani zastrzeżeń potrzebnych do interpretacji.
- Nie uznawać braku przewijania całej strony w bok za dowód dobrej wersji mobilnej.
- Nie rozciągać słupków od arbitralnego minimum; nie używać dwóch osi pionowych.
- Nie dodawać nowej biblioteki, zewnętrznych zasobów, dekoracyjnych animacji ani kolejnych kafelków.

## G. Dziesięć najważniejszych zmian

1. **Ujednolicić skalę mapy kohort — M, w przeglądarce.** Ten sam kolor musi oznaczać ten sam zakres odsetka, niezależnie od kolumny i filtrów.

2. **Naprawić etykiety zmian — S, w przeglądarce.** Pokazać słowo oceny obok ikony oraz jasno nazwać jednostkę zmiany.

3. **Zwiększyć czytelność tabel i skrócić szerokość akapitów — S, w przeglądarce.** Większe dane, mniej drobnych dopisków i tekst do `72ch` poprawią wszystkie zakładki.

4. **Zastąpić miniaturową oś zdarzeń listą mobilną — M, w przeglądarce.** Daty i nazwy staną się czytelne bez powiększania ekranu.

5. **Ograniczyć i grupować znaczniki zdarzeń na wykresach — M, w przeglądarce.** Nazwy zdarzeń powinny być dostępne bez przechodzenia do innej zakładki.

6. **Przenieść dzienny wykres kohort przed tabelę — M, w przeglądarce.** Najważniejsza część zadania przestanie być ukryta pod formularzem i zestawieniem.

7. **Dodać mobilny wybór miary w tabelach kohort i lejka — M, w przeglądarce.** Zachować oba okresy, zmianę i liczebność na jednym ekranie.

8. **Dodać wspólną obsługę podpowiedzi dotykiem i klawiaturą — L, w przeglądarce.** Uzupełnić ją widokiem tabelarycznym wartości wykresu.

9. **Pokazać Safari na dwóch hantlach — M, w przeglądarce.** To niewielki wykres wzmacniający najważniejszy priorytet naprawczy.

10. **Dodać hantle retencji na stronie wejściowej — M, w przeglądarce.** Wykres pokaże podstawę werdyktu „Nie” szybciej niż obecna tabela.