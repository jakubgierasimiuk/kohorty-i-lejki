# D — nowe brzmienia na stronie, etap 2 (sesja prowadząca dla sesji narzędzia, 2026-10-21)

**Po co ten plik:** teksty zakładek „Czy to wzrost”, „Priorytety” i „Czego nie wiemy” idą jak dotąd za `notatki/c_szkic.md` (sekcje 1, 3 i 4). Tu są nowe brzmienia dla pozostałych zakładek (eksport `analiza/b_eksport.py`). Każda liczba ma źródło w raporcie; na stronie liczby odczytuje eksport, nie wpisujemy ich ręcznie. Numery w nawiasach kwadratowych to punkty listy Kuby (`notatki/d_poprawki.md`) i syntezy konsylium (`notatki/konsylium/d_weryfikacja/synteza.md`).

Raporty z nowymi liczbami: `analiza/wyniki/d_retencja.txt`, `d_kampanie.txt`, `d_wynik.txt`, a te same liczby w postaci klucz → wartość w `d_retencja.json`, `d_kampanie.json`, `d_wynik.json`.

## Lejek

### Rozkład zmiany konwersji [synteza 16]

Obecne zdanie „Rachunkowo prawie cały spadek to zmiana ruchu…” zostaje, ale dochodzi zdanie o tym, że wynik zależy od podziału, i dlaczego przyjmujemy podział według przeglądarki i kampanii. Liczby: `analiza/wyniki/a5p_lejek.txt`, sekcja 4.

> Wynik rozkładu zależy od podziału. Według przeglądarki zmiana struktury ruchu daje −3,00 punktu procentowego, a zmiana konwersji w obrębie grup +0,67 punktu. Według kampanii to −2,44 i +0,11 punktu. Według strony wejścia (−0,45 i −1,87 punktu) i według tego, czy osoba już kupowała (−0,44 i −1,89 punktu), większość spadku wychodzi jako zmiana konwersji w obrębie grup. Przyjmujemy podział według przeglądarki i kampanii, bo ruch zmienił się właśnie w tym wymiarze: przybyło sesji nowych kampanii w przeglądarkach w aplikacjach, których w okresie 1 nie było. Na tej samej stronie wejścia albo w tej samej grupie pacjentów nowy ruch miesza się ze starym, więc jego niższa konwersja wygląda jak spadek w obrębie grupy.

### Przeglądarki wbudowane w aplikacje [Kuba 2, synteza 10]

Zdanie „To jednak nie jest tylko »inny ruch«. Dwie rzeczy trzeba naprawić na stronie:” i karta „Przeglądarki wbudowane w aplikacje tracą pacjentów na każdym kroku” są za mocne. Liczby: `d_kampanie.txt`, punkt 1 (1a — odtworzenie, 1e — zbiorczo w tej samej kampanii i przy tym samym typie odwiedzającego).

Zdanie wprowadzające:

> To nie zwalnia z naprawy. Jedną rzecz trzeba naprawić na stronie na pewno (Safari na iOS), a drugą sprawdzić (przeglądarki wbudowane w aplikacje w ruchu osób, które znają już stronę).

Karta (zamiast obecnej):

> **Przeglądarki wbudowane w aplikacje: w reklamach do nowych odbiorców nie płacą rzadziej niż zwykłe, w ruchu powracających płacą rzadziej.** W kampaniach do nowych odbiorców nie wykryliśmy niższej konwersji przeglądarki w aplikacji niż zwykłej w tej samej kampanii (Meta na L4 5,99% z 46 091 sesji wobec 5,58% z 14 901, TikTok 4,80% z 28 160 wobec 4,56% z 5 310; Meta „lekarz online” różnica −0,15 punktu procentowego, od −0,51 do +0,21, 29 330 sesji w przeglądarkach wbudowanych w dwóch latach). Niska konwersja tych kampanii nie wynika więc wyraźnie z przeglądarki; naprawą, którą da się wycenić, jest obietnica reklamy i strona wejścia (Priorytety, pozycja 5). W ruchu osób, które znają już stronę, jest inaczej: w okresie 2 sesje w przeglądarkach w aplikacjach płacą rzadziej niż zwykłe w tej samej kampanii — w remarketingu Meta o 12,2 punktu (1 772 sesje w przeglądarkach wbudowanych), w Google Ads na markę o 5,1 punktu (2 357), w wejściach bezpośrednich o 4,4 punktu (4 261). Luka jest na wyborze usługi i na kroku konta. Porównanie jest obserwacyjne: nie rozdziela wpływu przeglądarki od cech użytkowników (Czego nie wiemy, punkt 19).

Liczby z obecnej karty (płacą w 5–7% sesji, Chrome i Safari w 16–18%, kroki lejka) mogą zostać jako opis, ale bez tytułu „tracą pacjentów”.

### Konta bez zakupu [Kuba 10, synteza 20]

Jedno zdanie w „Lejku” (liczby: `d_retencja.txt`, punkt 6):

> 11 482 z 52 400 kont (21,9%) nie ma żadnego zakupu, a odsetek jest podobny w obu okresach (21,3% kont założonych w okresie 1 i 22,3% w okresie 2). Każde z tych kont wybrało usługę i przeszło krok konta, a 37,1% z nich zaczęło płatność. 58,1% z 11 482 ma zgodę marketingową (stan na 30.09.2026), ale w danych nie ma ani jednego ich wejścia z newslettera albo SMS-a (widać kliknięcia, nie wysyłki). Test: Czego nie wiemy, punkt 20.

## Kohorty

### Wiek, płeć i województwo [Kuba 10, synteza 18]

Zdanie pod nagłówkiem albo przy filtrach (filtra wieku i województwa nie dodajemy; liczby: `d_retencja.txt`, punkt 5; przyjęta reguła źródła, w nawiasach sesja płatności tam, gdzie się różni):

> Wiek, płeć, wielkość miejscowości i województwo nie zmieniają wniosku. Pacjenci nowych kampanii są młodsi (średnio 27,6 roku, 7 268 pacjentów, wobec 38,0 roku pozostałych w obu okresach), ale pierwsze L4 z nowych kampanii wraca w 90 dniach rzadko w każdej grupie wieku: 3,5% do 29 lat (2 532 pacjentów), 4,7% w wieku 30–44 lat (1 505) i 5,1% od 45 lat (39), wobec 13,3–15,3% u pozostałych pacjentów z pierwszym L4 (668–1 507 pacjentów w grupie wieku; okres 2, kohorty do 2.07.2026). Po przeważeniu okresu 2 strukturą wieku i płci okresu 1 spadek powrotu w 90 dniach bez nowych kampanii zostaje ten sam: −1,9 punktu procentowego według przyjętej reguły i −3,3 zamiast −3,5 punktu według sesji płatności. Udział nowych kampanii w nowych pacjentach okresu 2 jest podobny we wszystkich województwach (26,2–31,5%). Jeden trop regionalny: w dolnośląskim powrót poza nowymi kampaniami spada z 27,6% (1 024 pacjentów) do 19,7% (1 001), ale test wszystkich województw razem nie odrzuca, że zmiana jest wszędzie podobna, a dolnośląskie miało najwyższy powrót w okresie 1.

## Po zakupie

### Opóźnienia po godzinach i w ciągu poranka [Kuba 2 i 9, synteza 4 i 12]

Zdanie „Opóźnienia rosną tylko u internisty rano.” przeczy tabeli pod spodem. Zamiast niego (liczby: `d_retencja.txt`, punkt 1, internista, wszyscy pacjenci, okres według dnia terminu):

> Opóźnienia u internisty rosną najbardziej w jednym porannym bloku od 5:00 do 12:59, a mniej o 13:00. Odsetek wizyt spóźnionych ponad 15 minut: o 5:00 15,3% (459 wizyt) wobec 1,5% (267) rok wcześniej, o 6:00–10:00 od 40,4% do 47,0% (865–1 858 wizyt w godzinie) wobec 5,7–7,5%, o 12:00 22,3% (1 303) wobec 3,4% (774), o 13:00 5,6% (1 207) wobec 2,5% (719). Poza 5:00–13:59 odsetek jest prawie taki sam: 2,7% z 14 898 wizyt wobec 2,8% z 9 563. Wzrost w porach „południe” i „noc” to głównie brzegi porannego bloku: bez godziny 12:00 południe rośnie tylko z 2,9% do 3,9%, a noc bez 5:00 z 2,0% do 3,1%. U pozostałych lekarzy rano bez istotnej zmiany: 3,0% z 2 757 wizyt wobec 2,8% z 1 949.

Zdanie o miesiącach (6:00–11:59, pacjenci spoza nowych kampanii) zostaje. Odczytanie „spadła poranna przepustowość” zawężamy (liczby: `d_retencja.txt`, punkt 2, okres 2, wszyscy pacjenci):

> Już wizyty z najwcześniejszym porannym terminem w danym dniu są często spóźnione, a w danych zagregowanych nie widać narastania opóźnień w ciągu poranka: wizyty z najwcześniejszym porannym terminem dnia są spóźnione ponad 15 minut w 41,9% (391 wizyt), kolejne w 43,3% (8 760), średnio 18,7 wobec 20,2 minuty. W tym samym miesiącu (II–IX 2026) godziny z 8 i więcej wizytami mają o 4,2 punktu procentowego więcej spóźnionych niż godziny z 1–3 wizytami. Odczytanie, nie pomiar: to bardziej pasuje do stałego przesunięcia od początku dnia (późniejszy start względem grafiku, inna organizacja zapisów albo kolejki) niż do kolejki, która narasta, bo pacjentów jest więcej, niż lekarze zdążą przyjąć. Najwcześniejszy termin liczymy dla całej sieci, a nie dla pojedynczego lekarza; bez identyfikatorów lekarzy i grafików mechanizmu nie rozstrzygamy (Czego nie wiemy, punkt 4).

Wykres albo tabela według godziny terminu (0–23, okres A i B) byłyby tu najczytelniejsze; dane: `d_retencja.json`, klucze z sekcji 1 (internista, wszyscy).

## Wynik biznesu

### Rozkład spadku marży w III kwartale 2026 [Kuba 7, synteza 13]

Przy marży po kwartałach rok do roku (liczby: `d_wynik.txt`, punkty 1b, 1c, 1e, 1f i 2; to samo w `c_szkic.md`, sekcja 1c, punkt 6). Jeśli strona ma dziś zdanie, że skala problemu Safari jest „porównywalna ze spadkiem” albo kwotę „14–21 tys. zł”, zastąpić je drugim akapitem niżej.

> **Rozkład spadku III kwartału (opis księgowy, nie zmierzony wpływ).** Marża spadła o 15,1 tys. zł. Według przyjętej reguły pacjenci nowych kampanii zostawili 89,0 tys. zł marży przed kampaniami przy 87,9 tys. zł wydatków, czyli wyszli prawie na zero (+1,1 tys. zł). Reszta biznesu straciła 16,2 tys. zł: opłaty TelemediGO −11,2 tys. zł (w tym sprzedaż osobna w newsletterze −10,5 tys. zł: 225 zakupów we wrześniu 2025 wobec 107 w całym III kwartale 2026), wyższe wydatki kampanii działających w obu latach −6,2 tys. zł, marża konsultacji +1,2 tys. zł (więcej powtórnych zamówień, ale każde zostawia mniej marży: 32,81 zł wobec 35,86 zł). Księgowo lukę, która zostaje po odjęciu TelemediGO (5,0 tys. zł), wyjaśnia wzrost wydatków kampanii działających w obu latach, częściowo skompensowany wzrostem marży konsultacji. Rozkład księgowy nie rozdziela wpływu Safari od innych zmian przychodu. Według sesji płatności podział się odwraca: nowe kampanie −25,2 tys. zł, reszta +10,1 tys. zł; suma jest ta sama. Cały spadek przypada na wrzesień (−20,8 tys. zł); lipiec +6,6 tys. zł, sierpień −0,9 tys. zł.

> **Safari na iOS nie mieści się w tej luce.** Szacowana marża utracona przez awarię w samym III kwartale to 14,6–18,3 tys. zł (258–323 utracone pierwsze zamówienia z ich powrotami w tym samym kwartale, zależnie od odjęcia tła i założonego tempa strat), a osobny scenariusz powrotów pacjentów utraconych od 17.03 do 30.06 daje 4,1–4,5 tys. zł. To kwota tego samego rzędu co cały spadek kwartału (15,1 tys. zł) i większa niż luka 5,0 tys. zł. Wyniku kwartału bez awarii nie mierzymy: to rachunek przy założeniach pozycji 1 listy priorytetów.

> **Wcześniejsze kwartały okresu 1 nie miały jeszcze bazy powracających.** Marża z pacjentów pozyskanych w poprzednich kwartałach to 0% marży IV kwartału 2024, 23,4% I kwartału 2025 i 51,7% III kwartału 2025. Bez tej bazy marża rośnie rok do roku o 8,5% zamiast 71,4% w IV kwartale 2025 i o 26,1% zamiast 43,0% w I kwartale 2026. Miarodajne jest więc porównanie III kwartałów (baza to 51,7% i 51,1% marży).

## Zdarzenia

### Google Ads na markę od 22.05.2026 [synteza 22]

Nowe zdarzenie na osi (obszar: lejek), liczby: `d_kampanie.txt`, punkt 5 (5a, 5b, 5c, 5d, 5g):

> **22.05.2026: spada konwersja Google Ads na markę.** Sesja do płatności u osób, które jeszcze nie kupowały, spada z 21,2% (21 186 sesji, 1.10.2024–21.05.2026) do 17,8% (5 152 sesje, 22.05–30.09.2026), czyli o około 28,5–39,6 zamówienia na 30 dni zależnie od okna porównania. Bez Safari na iOS spadek jest prawie taki sam (−2,2 punktu procentowego wobec 17.03–21.05.2026), zmiana struktury ruchu (urządzenie, przeglądarka, strona wejścia) daje około zera, a inne kanały w tych dniach się nie zmieniają. Rok wcześniej w tym samym sezonie spadek był mniejszy (−1,3 punktu) i nieistotny, więc część może być sezonowa. W tym samym czasie rośnie koszt kliknięcia tej kampanii (z 1,01 zł w okresie 1 do 1,19 zł w okresie 2). Przyczyny w danych nie widać (Czego nie wiemy, punkt 22).

## Jak liczymy

### Kampania `crm_go_upsell`: 326 dni wobec 388 dni kalendarzowych [synteza, drobne]

Tam, gdzie strona pokazuje liczbę dni kampanii sprzedaży TelemediGO w newsletterze: 326 to liczba dni, w których była co najmniej jedna sesja z tej kampanii. Od pierwszego dnia (8.09.2025) do końca danych (30.09.2026) mija 388 dni kalendarzowych. Kampanie płatne mają sesje każdego dnia, więc u nich obie liczby są równe (Meta na L4: 332 dni). Źródło: `analiza/a5p_zdarzenia.py`, sekcja 6 (kolumna `dni` = liczba różnych dni z sesjami).
