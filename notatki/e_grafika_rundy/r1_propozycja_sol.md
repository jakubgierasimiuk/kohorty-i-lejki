## A. Werdykt ogólny

**Produkt ma mocne wnioski, ale warstwa dowodowa wymaga większej czytelności.** Działają: werdykt na wejściu, trzy zamówione kafelki, odnośniki do danych oraz wykres kroków lejka z porównaniem do roku wcześniej. Najbardziej przeszkadzają: jednakowo opakowane sekcje, rozbudowane filtry przed wykresami i tabele, których najważniejsze kolumny znikają na telefonie. W kodzie są też dwa problemy interpretacyjne: kolory serii zależą od kolejności wyboru, a mapa kohort skaluje każdą kolumnę osobno, więc identyczny odcień oznacza różne odsetki powrotu. Rekomenduję dopracowanie obecnego narzędzia według zasad impeccable z briefu, z pierwszeństwem dla kohort, lejka i telefonu.

## B. System wizualny

**Kolory**

Zostawić obecną bazę:

| Rola | Wartość / zasada |
|---|---|
| Pasek nagłówka | `#13213A` |
| Tło strony / powierzchnia | `#EEF1F5` / `#FFFFFF` |
| Tekst główny / pomocniczy | `#172133` / `#435067` |
| Akcja i wybór | `#1F5FCC` |
| Linie podziału | `#DCE1E9`; siatka wykresów jaśniejsza |
| Dobrze / źle / uwaga | Obecne tokeny; zawsze ikona SVG i widoczne słowo |

Paletę wykresów oddzielić od stanów. Proponuję niebieski `#2A78D6`, fiolet `#7663B0`, turkus `#167D8D`, róż `#B85C8A`, brąz `#8B6B43` i szaroniebieski `#69788C`. Maksymalnie cztery serie domyślnie; pozostałe dostępne przez wybór. Kolor przypisywać do klucza kategorii, niezależnie od sortowania i zaznaczenia.

W widokach skupionych na jednej diagnozie wyróżnić jedną serię, a pozostałe pokazać szaro. W porównaniu lat: wcześniejszy okres jako pusty znacznik lub linia przerywana, późniejszy jako pełny znacznik lub linia ciągła.

Tła okresów A i B zmienić na dwa neutralne poziomy szarości, np. 4% i 8% krycia. Dodać ich nazwy przy wykresie. Obecne niebieskie tło okresu B konkuruje z niebieską serią.

Tryb ciemny już istnieje. Zachować go, dodać wybór „System / Jasny / Ciemny” i sprawdzić kontrast wykresów, mapy kohort oraz etykiet. To kontrola istniejącego rozwiązania, bez nowego projektu kolorystycznego.

**Typografia**

- Jedna rodzina systemowa, obecny zestaw zastępczy.
- Tytuł zakładki: 26/32 px na komputerze, 22/28 px na telefonie.
- Nagłówek sekcji: 18/24 px, grubość 650.
- Wniosek: 16/24 px, grubość 500–600.
- Tekst: 15/23 px. Tabela: 13/19 px na komputerze, 14/20 px w uproszczonym widoku telefonu.
- Przypisy i osie: minimum 12 px. Nie zmniejszać całego SVG, żeby „zmieścić” wykres.
- Wszystkie dane: cyfry tabelaryczne. Wartość główna mocniejsza, liczebność spokojniejsza.
- Akapity ograniczyć do około `72ch`, zamiast obecnych szerokości dochodzących do 900 px.

**Układ**

Zostawić maksymalną szerokość 1320 px oraz marginesy 24 px na komputerze i 16 px na telefonie. Wprowadzić rytm odstępów 4–8–12–16–24–32 px.

Kartą pozostaje samodzielna jednostka pracy: werdykt, analiza z wykresem, priorytet. Filtry, legenda, zastrzeżenie i „Szczegóły” są częściami tej jednostki, bez dodatkowego cienia i obramowanego pudełka. Trzy zamówione kafelki pozostają wyjątkiem.

Usunąć wymuszanie jednakowej wysokości sąsiednich kart tekstowych. Na zrzutach „Czy to wzrost” i „Lejek” powoduje ono duże puste obszary. W obrębie analizy kolejność powinna być stała: **wniosek → wykres → zastrzeżenie → odnośniki → szczegóły**.

**Komponenty**

- **Stan i zmiana:** zachować ikony. W etykiecie zmiany pokazać słowo także wzrokowo; dziś „lepiej/gorzej” bywa dostępne wyłącznie czytnikom ekranu. Jednostkę zmiany podać w nagłówku kolumny.
- **Legenda:** zawsze widoczne nazwy i próbki linii. Po wskazaniu punktu dopisywać wartości, bez zmiany wysokości komponentu.
- **Podpowiedź:** data lub kohorta, seria, wartość, licznik i mianownik. Obsługa najechania, dotknięcia i klawiatury; tabela jako alternatywa.
- **Filtry:** jeden panel nad wynikami. Widoczne podstawowe ustawienia, reszta w rozwinięciu; aktywne ograniczenia pokazane także po zwinięciu. Pełna nazwa wybranej opcji musi być odczytywalna.
- **Tabela:** przyklejony pierwszy identyfikator i nagłówki. Na telefonie podstawowy widok ma pokazywać nazwę grupy i wybraną miarę, a pełna tabela pozostaje dostępna w osobnym obszarze przewijania.
- **„Zobacz w danych”:** przy wykresie, którego dotyczy, ze stanem filtrów w adresie.
- **Sekcje zwijane:** cały wiersz jako obszar dotykowy wysokości minimum 44 px; widoczny stan rozwinięcia.

**Nawigacja**

Na komputerze zachować dziewięć zakładek i aktywne podkreślenie. Na telefonie zastąpić wielorzędowe pigułki przyciskiem z nazwą bieżącej zakładki, rozwijającym pełną listę dziewięciu pozycji. Zachować nazwę produktu i uwagę o danych syntetycznych. Obecny nagłówek zajmuje około jednej czwartej pierwszego mobilnego ekranu.

## C. Zakładka po zakładce

W tabelach ścieżki danych są względne wobec `narzedzie/dane_strony/`. **S** oznacza około godziny, **M** pół dnia, **L** dzień lub więcej. Wysiłki dotyczą pojedynczych zmian; wspólne komponenty można wykorzystać wielokrotnie.

### 1. Czy to wzrost

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Powrót pacjentów | Tabela czterech okien | Cztery poziome hantle: rok wcześniej i ostatnie 12 miesięcy; liczebności w podpowiedzi, tabela poniżej | `kohorty.js`: `d`, `r`, `okna`; **w przeglądarce**, z obecnymi regułami pełnych okien | Kierunek i wielkość pogorszenia widać jednocześnie | M |
| Źródło nowych pacjentów | Liczby w punktach | Dwa poziome słupki liczebności: wcześniejszy rok i ostatni rok; drugi podzielony na nowe kampanie i resztę | `kohorty.js`: `d`, `kat`, `wart`; `podsumowanie.js`: `etykiety.nowe_kampanie`; **w przeglądarce** | Pokazuje zarówno przyrost, jak i zmianę składu | M |
| Marża a wydatki | Tabela kwartalna | Dwie małe plansze ze zmianą rok do roku: marża przed kampaniami i wydatki kampanii, wspólna skala procentowa | `wynik.js`: `serie`; **w przeglądarce** | Rozchodzenie się tempa wzrostu jest głównym obrazem | M |

Werdykt, trzy kafelki i cztery decyzje zostają. Nie dodawać czwartego kafelka.

### 2. Kohorty

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Kolejność i filtry | Duży panel, szeroka tabela, dopiero potem trend | Wniosek → podstawowe filtry → trend → porównanie grup → macierz → krzywa. Dodatkowe filtry rozwijane | Obecny stan filtrów w `widoki.js`; **w przeglądarce** | Obowiązkowa analiza dzienna pojawia się wcześniej | M |
| Mapa kohort | Osobna skala kwantylowa każdej kolumny; brak legendy | Stała skala 0–100% wspólna dla wszystkich okien, widoczna legenda; brak pełnego okna jako odrębny wzór. Na telefonie jedna wybrana kolumna i możliwość przełączenia okna | `kohorty.js`: `d`, `r`; **w przeglądarce** | Ten sam kolor zawsze oznacza ten sam odsetek | M |
| Porównanie grup | Wielopoziomowe komórki i obcięte kolumny | Widok wybranej miary, np. powrotu w 90 dniach: nazwa, wartość obu lat, zmiana, liczebność. Pełna tabela nadal dostępna | `kohorty.js`: `d`, `r`, `m90`, kategorie; **w przeglądarce** | Najważniejszą miarę można porównać bez przesuwania tabeli | M |

Zachować dzienną rozdzielczość. Wygładzenie zmienia sposób czytania trendu, a nie definicję kohorty.

### 3. Lejek

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Wykres kroków | Dobre paski i znaczniki wcześniejszego roku | Zachować. Kliknięcie przejścia ustawia tę miarę na wykresie dziennym i przenosi do niego | `lejek_*.js`: `s`, dostępne `k1…k5`; **w przeglądarce** | Łączy „gdzie tracimy” z „od kiedy” | M |
| Awaria Safari | Karta tekstowa, dalej ogólny wykres | Bezpośredni widok kroku konto/termin dla Safari na iOS, z porównaniem i oznaczeniem daty awarii | `lejek_system_przegladarka.js`; `podsumowanie.js`: `lejek_naglowek.safari`; **w przeglądarce** | Pokazuje diagnozę bez samodzielnego ustawiania filtrów | M |
| Trend według przeglądarki | Wiele linii i wszystkie zdarzenia | Wybrana przeglądarka wyróżniona; pozostałe neutralne. Zdarzenia lejka domyślnie, pozostałe na żądanie | `lejek_*.js`, `zdarzenia.js`: `lista`; **w przeglądarce** | Awaria nie ginie w ruchu z innych źródeł | M |

Kod zawiera `k1–k3`, choć skrócony załącznik nie wymienia ich przy wszystkich plikach. Wykres musi sprawdzać dostępność kroku; brak danych nie oznacza zera.

### 4. Po zakupie

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Punktualność w czasie | Cztery równorzędne kolorowe linie | Rano wyróżnione niebieskim, pozostałe pory szare i odróżnione linią; możliwość wyboru innej pory | `po_zakupie.js`: `punktualnosc.n`, `p15`, `p30`; **w przeglądarce** | Wzrok trafia w problem porannych wizyt | S |
| Opóźnienie według godziny | Tabela 24 wierszy | Hantle dla każdej godziny, osobno internista i pozostali lekarze, wspólna skala | `po_zakupie.js`: `godziny` ma tekstowe komórki; **wymaga eksportu** liczb | Blok godzin problemowych widać bez czytania 24 wierszy | M |
| Zwroty i oceny | Linie oraz tabele | Zwroty: porównanie odsetków dla L4 z nowych kampanii i pozostałych. Oceny: punkty średniej według opóźnienia, obok udział ocenionych | `po_zakupie.js`: `zwroty`, `oceny`; **w przeglądarce** | Oddziela problem zwrotów od selekcji osób wystawiających oceny | M |

### 5. Zdarzenia

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Oś zdarzeń | Cztery tory; na telefonie cały rysunek miniaturyzowany | Komputer: zachować tory. Telefon: pionowa chronologia z datą, obszarem i krótką nazwą | `zdarzenia.js`: `lista`; **w przeglądarce** | Daty i punkty pozostają czytelne i dotykalne | M |
| Szczegóły zdarzeń | Długa seria podobnych kart | Zwarta lista z rozwijanym opisem; zdarzenie wskazane z wykresu automatycznie otwarte | `lista`: `co`, `ile`, `skad`, `link`; **w przeglądarce** | Szybsze znalezienie konkretnego zdarzenia | M |

### 6. Wynik biznesu

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Przychód, koszty, marża | Cztery linie na wspólnej osi | Marża jako główny trend; przychód i koszty w oddzielnym panelu. Wspólny zakres czasu, jednostka i synchronizacja wskazania | `wynik.js`: `serie`; **w przeglądarce** | Marża nie jest przyciśnięta skalą przychodu | M |
| Ekonomia kampanii | Bardzo szeroka tabela | Poziomy wykres punktowy wyniku na pacjenta, oś z zerem; dwa symbole reguł przypisania. Przełącznik 90/180 dni | `wynik.js`: `ekonomia.wiersze`, `wynik`, `regula`, `okno`, `klucz`; **w przeglądarce** | Widać kampanie tracące oraz zależność oceny od przypisania | M |
| Rachunek marży | Składniki rozproszone w tabeli | Wodospad wybranego okresu: przychód konsultacji + TelemediGO − lekarze − kampanie − prowizja = marża | `wynik.js`: `serie`; **w przeglądarce** | Ujawnia równanie wyniku, bez nowej interpretacji przyczynowej | M |

### 7. Jakość danych

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Korekty dashboardu | Tabela czterech miar i czterech kroków | Dwa wykresy kolejnych poziomów wzrostu: zamówienia i przychód; pacjenci i TelemediGO jako spokojne wartości kontrolne | `jakosc.js`: `mostek.kroki[].miary`, `p1`, `p2`, `wzrost`; **w przeglądarce** | Eksponuje korekty, które faktycznie zmieniają ocenę | M |
| Duplikaty i testy | Linia ze słupkami oraz słupki kwartalne | Zachować formy; oznaczyć zakres duplikacji bezpośrednio na wykresie i zapewnić mobilne wskazywanie wartości | `jakosc.js`: `duplikaty`, `testy.kwartaly`; **w przeglądarce** | Obecne formy już odpowiadają zadaniu danych | S |

### 8. Priorytety

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Przegląd | Tabela; telefon rozwija wszystkie pola każdej pozycji | Zachować kolejność. Mobilnie pokazać numer, działanie, kwotę i pewność; dopiski i wdrożenie dostępne po rozwinięciu | `c.js`: `priorytety.przeglad`; **w przeglądarce** | Krótsza droga do dalszych pozycji bez ukrywania decyzji | M |
| Karta działania | Kwota, pewność, wdrożenie w szarym panelu | Płaski pas trzech pól, dalej stała struktura „Dlaczego / Co robimy / Po czym poznamy”; powrót do właściwego wiersza przeglądu | `c.js`: `priorytety.karty`; **w przeglądarce** | Ułatwia porównywanie działań i powrót do listy | S |

### 9. Czego nie wiemy

| Element | Jak jest dziś | Propozycja | Z jakich danych | Dlaczego czytelniej | Wysiłek |
|---|---|---|---|---|---|
| Lista 21 pytań | Rozbudowana tabela | Komputer: tabela z wyraźnymi kolumnami pytania, konsekwencji i testu. Telefon: pytanie oraz powiązany priorytet, rozwijana konsekwencja i test | `c.js`: `niewiadome.wiersze`; **w przeglądarce** | Zachowuje związek pytania z decyzją |
M |
| Powiązania | Odnośnik do priorytetu | Filtr według pozycji priorytetów i odnośnik powrotny z jej karty do powiązanych pytań | `wiersze[].pozycja`; **w przeglądarce** | Nie trzeba pamiętać numerów między zakładkami | M |

## D. Wykresy kołowe, infografiki i inne formy

**Nie proponuję żadnego koła ani pierścienia.** Udział nowych kampanii i pozostałych to dwie części, które szybciej odczytuje się z paska. Pełny podział źródeł ma za dużo kategorii; lepsze są uporządkowane poziome słupki.

- **Mostek jakości:** do porównania zmian procentowych użyć kolejnych punktów lub poziomów. Prawdziwy wodospad stosować do liczebności albo złotych, osobno dla każdego roku. Odejmowanie testów zmienia obie bazy porównania.
- **Rozkład spadku powrotu:** nie rysować przyczynowego podziału „kampanie kontra reszta”. Wykres dekompozycji wymaga eksportu dokładnych składników i opisu metody. Pokazuje zmianę składu, nie efekt reklamy.
- **Hantle:** właściwe dla powrotu w kolejnych oknach i opóźnień według godziny. Dwie reguły przypisania kampanii pokazywać różnymi symbolami, bez sugerowania kolejności czasowej.
- **Małe wielokrotności:** dobre dla marży i wydatków oraz porównań specjalizacji. Porównywane panele muszą mieć zgodne skale.
- **Mapa kohort:** główna forma analityczna, z liczebnością i pełnością okna. Dzienna rozdzielczość zostaje.
- **Udziały w czasie:** skumulowany wykres 100% można policzyć z kategorii kohort. Warstwy muszą być rozłączne; „Wszyscy” nie może być dodatkową warstwą. Ze względu na czas zostawiłbym go jako opcję późniejszą.
- **Oś zdarzeń:** właściwa infografika projektu; wskazuje współwystępowanie, nie udowadnia przyczyny.
- **Sankey lejka:** odrzucić. Obecne dane opisują liczebności kroków, a nie komplet indywidualnych ścieżek. Paski lepiej pokazują straty między etapami.

Nowa biblioteka nie jest potrzebna. Wystarczą uPlot i lokalne SVG/HTML/CSS.

## E. Pozostałe elementy oddawane

**README:** na początku rzeczywisty, klikalny adres narzędzia, krótka odpowiedź i jeden aktualny zrzut komputerowego widoku startowego. Zrzut umieścić w repozytorium, z tekstem alternatywnym i odnośnikiem do narzędzia. Zachować tekstową odpowiedź, ponieważ obrazu nie da się wygodnie czytać na każdym urządzeniu.

Mermaid wykorzystać najwyżej do pokazania drogi „dane → oczyszczenie → analiza → eksport → narzędzie”. Bez nowych liczb i bez powielania wykresów biznesowych. Schemat jest opcjonalny; większą wartość ma aktualny zrzut i instrukcja czytania.

**Lista priorytetów:** narzędzie pozostaje jedynym pełnym źródłem. README pokazuje pierwsze decyzje i prowadzi do kart. Nie tworzyć osobnej prezentacji ani drugiego rankingu.

**„Czego nie wiemy”:** pokazywać jako rejestr decyzji wymagających dowodu. Powiązania z priorytetami są ważniejsze od dekoracyjnych ikon i wykresów liczby niewiadomych.

## F. Czego nie robić

- Nie dodawać wykresu do każdej karty. Krótka odpowiedź albo pojedyncza kwota często wystarcza.
- Nie skalować całego wykresu do telefonu. Obecna mobilna oś zdarzeń pokazuje skutek takiego podejścia.
- Nie wyświetlać wszystkich czternastu zdarzeń na każdym trendzie. Powstaje szum i konieczność pamiętania numerów.
- Nie zamieniać brakującego pełnego okna kohorty na zero.
- Nie kolorować wzrostu kosztu automatycznie jako pogorszenia bez kontekstu ekonomicznego.
- Nie traktować przedziałów warunkowych ekonomii kampanii jako statystycznych przedziałów ufności.
- Nie sumować wartości priorytetów. Pozycje mogą się nakładać i opisują różne scenariusze.
- Nie wydobywać liczb z akapitów ani napisów takich jak „0 albo 38 tys. zł”. Do wykresu potrzebny jest jawny kontrakt liczbowy.
- Nie ukrywać zastrzeżenia o przyczynowości w odległych szczegółach.
- Nie dokładać dekoracyjnych animacji, nowych fontów, bibliotek z sieci ani kolejnych poziomów kart.

## G. Dziesięć najważniejszych zmian

1. **Stałe kolory kategorii — S, w przeglądarce.** Zastąpić przydział według kolejności wyboru mapą klucz → kolor. Ta sama grupa pozostaje rozpoznawalna po zmianie filtrów.

2. **Jednoznaczna skala mapy kohort — M, w przeglądarce.** Wprowadzić wspólną skalę procentową, legendę i odrębne oznaczenie niepełnego okna.

3. **Wykresy dopasowane do telefonu — M, w przeglądarce.** Usunąć minimalną szerokość 320 px tam, gdzie wnętrze karty jest węższe. Dopasować osie i zapewnić dotykowy odczyt wartości.

4. **Mniej znaczników zdarzeń na trendach — M, w przeglądarce.** Domyślnie pokazywać zdarzenia właściwego obszaru; wybrane zdarzenie wyróżniać i opisywać bezpośrednio.

5. **Krótsze filtry kohort — M, w przeglądarce.** Zostawić widoczne podstawowe ustawienia, pozostałe rozwijać. Trend przenieść przed szeroką tabelę.

6. **Mobilny widok jednej miary tabeli — M, w przeglądarce.** Pokazać nazwę grupy, porównanie lat i liczebność; pełną tabelę pozostawić dostępną.

7. **Hantle retencji na stronie startowej — M, w przeglądarce.** Cztery okna powrotu tworzą najkrótszy graficzny dowód głównego werdyktu.

8. **Wyróżnienie porannych opóźnień — S, w przeglądarce.** Jedna mocna seria i neutralne porównania poprawią obecny wykres bez zmiany jego konstrukcji.

9. **Czytelna mobilna chronologia — M, w przeglądarce.** Zastąpić miniaturę osi pionową listą zdarzeń z pełnymi datami i odnośnikami.

10. **Wykres wyniku kampanii względem zera — M, w przeglądarce.** Dwa symbole reguł przypisania pokażą, które decyzje są odporne na zmianę sposobu przypisania źródła.