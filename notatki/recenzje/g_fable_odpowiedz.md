# Przejrzystość narzędzia: przegląd zakładek 3–9 oczami czytelnika z Telemedi

Materiał: 59 zrzutów przy 1366 px, teksty zakładek, `index.html`. Dodatkowo sprawdziłem działającą stronę (Edge bez okna, 1366×900 i 390×844): szerokość tabel, przyciski powrotu, przyklejenie filtrów, działanie odnośników. Takie ustalenia oznaczam „(sprawdzone na żywo)”.

## 1. Zasady ogólne wyciągnięte z uwag Kuby

1. **Pierwszy ekran o czymś innym.** Zakładka otwiera się tym, co obiecuje jej nazwa; wniosek i tabela zdarzeń nie mogą zasłaniać kohort, lejka ani marży na dwa ekrany.
2. **Wniosek wciśnięty między filtrowane karty.** Treść niezależna od ustawień stoi nad paskiem ustawień, wszystko zależne stoi pod nim, bez wyjątków.
3. **Filtr-sierota.** Sterowanie stoi w nagłówku karty, którą zmienia, albo w jednym przyklejonym pasku, który widać przy przewijaniu; filtr dwa ekrany nad tabelą nie istnieje dla czytelnika.
4. **Niemy związek.** Każda karta zależna od ustawień ma jedną linijkę: od których.
5. **Rozdzielone bliźniaki.** Wykres i tabela, które dzielą podział, porównanie i zaznaczone serie, są jedną kartą.
6. **Skutek jako wyjaśnienie.** Na wykresach i osi domyślnie widać przyczyny (starty kampanii, decyzje, awarie), a zmiany wykryte w tej samej mierze, którą pokazuje wykres, to skutki i idą pod przełącznik.
7. **Tabela dla autora, nie dla czytelnika.** Jedna miara naraz, liczebność raz na wiersz, okresy słowami, zmiana z jednostką, nagłówek pierwszej kolumny jako nazwa podziału, bez „A:”, „B” i numerów.
8. **Kolorowy szum.** Czerwień i zieleń tylko, gdy różnica przekracza rozrzut losowy; reszta szara „bez wyraźnej zmiany”, małe grupy oznaczone.
9. **Tabela ucięta z prawej.** Każda tabela mieści się w 1366 px bez przewijania w bok; co się nie mieści, idzie na przełącznik albo pod kursor.
10. **Bez drogi powrotnej.** Jeden przycisk przywraca ustawienia startowe, czyści adres i jest aktywny tylko po zmianie.

## 2. Przegląd zakładek

### Lejek

**Czego szuka czytelnik:** gdzie i od kiedy tracimy pacjentów, czyli kroki lejka z największym ubytkiem. **Na pierwszym ekranie tego nie widzi**: `lejek_01` to wniosek z czterema punktami, zastrzeżeniem i dwoma zwiniętymi wierszami; `lejek_02` to dwie karty z hantlami i pasek filtrów; lejek pojawia się dopiero na `lejek_03`.

**Co przeszkadza:**
- Karta „Udział sesji nowych kampanii na L4 … miesiąc po miesiącu” (`lejek_03`–`lejek_04`) stoi między krokami lejka a wykresem dzień po dniu, choć sam przypis mówi, że nie zależy od filtrów (zasada 2). To dowód do zdania z wniosku „od kwietnia to prawie połowa”, więc jego miejsce jest przy wniosku.
- Pasek filtrów (`lejek_02`) ma dobry tytuł „Filtry: kroki lejka, tabela i wykres dzień po dniu”, ale nie jest przyklejony, tabela, którą steruje, jest dwa ekrany niżej, a przycisku „Przywróć domyślne” nie ma (sprawdzone na żywo: nie ma go nigdzie na stronie, żaden pasek filtrów nie jest przyklejony). Boli to szczególnie tu, bo odnośniki z innych zakładek ustawiają naraz typ sesji, podział, okresy i serie.
- „Okres A” i „Okres B” w polach dat i w opisie pod tytułem kroków (`lejek_03`).
- Tabela „Kroki lejka w podziale” (`lejek_05`): 1391 px przy 1230 px dostępnych (sprawdzone na żywo), więc ostatnia i najważniejsza kolumna „Sesja do płatności” jest ucięta. W każdej komórce cztery liczby i etykieta koloru: Opera „−5,0 gorzej” z 622 sesji i „+6,7 lepiej” z 392 sesji to szum (zasada 8).
- Legenda przy prawej krawędzi wykresu ucina nazwy serii („Instagram (w aplikacj…”, `lejek_04`), a tytuł wykresu to nazwa miary plus wygładzenie, czyli opis techniczny w miejscu tytułu.

**Proponowany układ od góry:**
1. Wniosek skrócony do dwóch zdań i trzech punktów; w pustej prawej połowie karty mały wykres udziału sesji nowych kampanii (dziś osobna karta), reszta w zwiniętych „Szczegółach” razem z tabelami miesięcznymi, które już tam są.
2. Pasek „Sesje w analizie”: Kto, Typ sesji, Porównanie z okresami słowami, zawężenia jako etykiety, „Przywróć domyślne”; przyklejony.
3. Karta „Kroki lejka” jak dziś, z „Pokaż dla” w nagłówku.
4. Dwie karty „Do naprawy” (Safari) i „Do sprawdzenia” (przeglądarki w aplikacjach), bo wynikają z kroków i prowadzą do priorytetów.
5. Jedna karta „Dzień po dniu i podział”: w nagłówku miara, wygładzenie, podział; pod wykresem zdarzenia jako przyciski „60 dni przed i po” (jak w Kohortach); tabela podziału w tej samej karcie, z tą samą miarą co wykres, a „wszystkie kroki” jako opcja z samą zmianą w komórce.
6. „Sesje poza lejkiem głównym” (zalogowane od wejścia, samo TelemediGO) jako ostatnia, zwinięta karta.
7. „Jak liczymy w tej zakładce”.

**Tabele:** jedna miara naraz, liczebność raz na wiersz, „rok wcześniej / ostatnie 12 miesięcy” zamiast „A:”, zmiana „−3,0 pkt proc.”, kolor tylko przy istotnej różnicy (Safari −10,1 punktu z 10 205 sesji zostaje czerwone, Opera szarzeje), wiersz sumy „Wszystkie wybrane sesje”.

**Sterowanie:** filtry daleko od tabeli, brak przycisku powrotu, brak linijki „zależy od” przy wykresie. Odnośniki działają dobrze: „Pokaż w lejku” z karty zdarzenia ustawia filtry i przewija do kroków (sprawdzone na żywo).

**Pracochłonność:** przeniesienie wykresu udziału i skrócenie wniosku: mała; pasek przyklejony z przyciskiem: średnia; wykres z tabelą w jednej karcie: średnia; przebudowa tabeli: duża, ale wspólny kod z tabelą grup w Kohortach.

### Po zakupie

**Czego szuka czytelnik:** co dzieje się z pacjentem po zapłacie (punktualność, zwroty, oceny) i czy to zmienia powrót. **Widzi na pierwszym ekranie** (`po-zakupie_01`): wniosek, filtry w karcie, wykres. To dobry pierwszy ekran.

**Co przeszkadza:**
- Sześć kart, 6 334 px (siedem ekranów), w dwóch wątkach: cztery o opóźnieniach, jedna o zwrotach, jedna o ocenach. Karta „Zwroty” (`po-zakupie_06`) przerywa wątek opóźnień między „Powrót po spóźnionej wizycie” a „Oceny według opóźnienia” (`po-zakupie_08`).
- Tabela punktualności (`po-zakupie_02`–`po-zakupie_03`): 16 wierszy specjalizacja × pora, kolor w każdym wierszu, także „+0,7 gorzej” przy 104 wobec 82 wizyt (pediatra w nocy). Jedna kolumna liczbowa przy prawej krawędzi, środek pusty.
- Tabela zwrotów (`po-zakupie_07`): 1300 px, kolumny kwot ucięte (sprawdzone na żywo); kolor przy „+0,1 gorzej” (2,6% wobec 2,5%).
- Tabela ocen (`po-zakupie_08`): „−0,02 gorzej” przy średniej 4,45 wobec 4,47, „+0,01 lepiej”, rok wcześniej z 44 ocenami w kolorze. Najczystszy kolorowy szum w narzędziu.
- Tabela powrotu po opóźnieniu (`po-zakupie_05`): tekst mówi „tych porównań nie oceniamy”, a tabela pokazuje rok wcześniej z 35 i 135 pacjentami.
- Filtr „Pacjenci” ma różne wartości domyślne: „Spoza nowych kampanii” (karty 1, 4, 6), „Wszyscy” (karty 3, 5); czytelnik porównuje liczby między kartami i nie wie, dlaczego się różnią. „Specjalizacja (wykres)” sugeruje, że tabela nie zależy od specjalizacji, a od czego zależy, nie wiadomo (zasada 4).
- Pod wykresami zdarzenia 6 i 7 to skutki; przyczyny (starty Meta i TikToka) są pod „wszystkie obszary” (zasada 6).

**Proponowany układ od góry:** 1. „Punktualność” = karta 1 z tabelą 4×4, 2. „Skąd opóźnienia: godziny i ruch” = dzisiejsze karty 2 i 3 obok siebie, 3. „Powrót po spóźnionej wizycie”, 4. „Oceny” zaraz po powrocie, 5. „Zwroty, anulacje, nieodebrane” na końcu, 6. „Jak liczymy”.

**Tabele:** punktualność jako wiersze = specjalizacja, kolumny = pora, liczebność raz w nagłówku wiersza, kolor tylko internista rano i południe. Zwroty: kolumny kwot do zwiniętej „Tabeli z liczbami” (84 tys. zł i 34 tys. zł są już w zdaniu nad tabelą). Oceny i powrót: rok wcześniej szary i tylko po najechaniu, gdy grupa ma mniej niż około 150 obserwacji.

**Sterowanie:** filtry stoją przy kartach (dobrze); ujednolicić domyślne „Pacjenci” albo wyjaśnić jedną linijką; linijka „zależy od” przy każdej tabeli.

**Pracochłonność:** kolejność kart: mała; tabela 4×4: średnia; kolor z istotnością: średnia (wspólna reguła); tabela zwrotów: mała; domyślne wartości: mała.

### Zdarzenia

**Czego szuka czytelnik:** co się stało, kiedy i ile kosztowało. **Widzi na pierwszym ekranie** wniosek i oś z czterema torami (`zdarzenia_01`). Oś jest klikalna i przewija do karty (sprawdzone na żywo).

**Co przeszkadza:**
- Czternaście kart chronologicznie, pięć ekranów (`zdarzenia_02`–`zdarzenia_07`); pierwszą kartą jest „Godzina bez danych”, najmniej istotne zdarzenie, a wszystkie karty mają ten sam ciężar: nie widać na nich ani kwoty, ani decyzji. Tabela zdarzeń z Kohort, która według listy Kuby trafia tu na górę, załatwia połowę; druga połowa to kolejność kart.
- Pary przyczyna–skutek stoją jako osobne karty o tej samej dacie: start Meta (karta 4) i udział nowych kampanii (karta 5), oba 3.11.2025; start TikToka 9.02 (karta 9) i spadek powrotu w 30 dniach 10.02 (karta 10).
- Karty 1 i 14 (godzina bez danych, duplikaty) powtarzają w całości treść zakładki „Jakość danych”.
- Na osi znaczniki mają tylko numery; przy pięciu znacznikach w listopadzie 2025 czytelnik liczy numery.
- Cztery brzmienia tego samego odnośnika: „Pokaż w lejku”, „Pokaż w kohortach”, „Zobacz w jakości danych”, „Pokaż w zakładce „Po zakupie””; dwa ostatnie prowadzą na początek zakładki, nie do karty (sprawdzone na żywo).
- Tekst wniosku w wąskiej kolumnie z pustą prawą połową karty (`zdarzenia_01`).

**Proponowany układ od góry:**
1. Wniosek (dwa zdania, szczegóły zwinięte).
2. Tabela zdarzeń i decyzji (przeniesiona z Kohort), z odnośnikami „Opis zdarzenia” do kart niżej.
3. Oś czasu z krótką etykietą słowną przy przyczynach (starty kampanii, newsletter, awaria), numery przy skutkach.
4. Karty: najpierw przyczyny z ich skutkami jako podsekcją tej samej karty (Meta + udział nowych kampanii; TikTok + powrót w 30 dniach), potem zmiany bez znanej przyczyny, na końcu jakość danych skrócona do jednego akapitu „O ile” i odnośnika do pełnego opisu.
5. „Wszystkie zmiany wykryte automatycznie” zwinięte, jak dziś.

**Tabele:** surowy wynik metody jest w porządku. **Sterowanie:** chipy obszarów przy osi są dobre; brakuje linijki, czy filtrują też listę kart.

**Pracochłonność:** kolejność i pary: mała, łączenie kart: średnia; etykiety na osi: średnia; jedno brzmienie odnośników i kotwice: mała; skrócenie kart jakości danych: mała.

### Wynik biznesu

**Czego szuka czytelnik:** ile zarabiamy, czy marża rośnie i czy kampanie się zwracają; jedna liczba za rok, kwartały, potem szczegóły. **Na pierwszym ekranie** (`wynik_01`) widzi cztery akapity, zastrzeżenie i skrawek wykresu. Liczba „+27% po wszystkich kosztach” jest w drugim akapicie zwykłą czcionką, a kwoty marży (828 tys. zł → 1 048 tys. zł) dopiero w tabeli na `wynik_04`, cztery ekrany niżej.

**Co przeszkadza:**
- Jedna karta `wy-karta` obejmuje wniosek, filtr, dwa wykresy liniowe, wykres kwartalny, tabelę kwartalną, tabelę miesięczną i szczegóły: cztery ekrany bez granic (`wynik_01`–`wynik_05`).
- Na obu wykresach liniowych wszystkie 14 zdarzeń jako pionowe linie, w listopadzie 2025 pięć linii obok siebie (`wynik_01`, `wynik_02`), a lista 14 odnośników powtórzona pod każdym wykresem (sprawdzone na żywo). Przyczyny wystarczą, to pięć linii (zasada 6).
- Filtr „Grupowanie” stoi nad wykresami, ale nie mówi, że nie dotyczy kwartałów i tabeli miesięcznej. Legendy przy prawej krawędzi ucięte („Marża przed kosztem k…”).
- Tabela kwartalna (`wynik_03`): nagłówek „Kwartał wobec tego samego kwartału rok wcześniej” i wiersze „IV kw. 2025 wobec IV kw. 2024” mówią to samo dwa razy. Etykieta „uwaga” przy wydatkach i brak oceny przy koszcie lekarza są dobre.
- Tabela miesięczna (`wynik_04`): 27 wierszy, mieści się, ale na start wystarczą wiersze roczne i zmiana; miesiące mogą być zwinięte.
- „Szczegóły” pierwszej karty to sześć osobnych wątków (III kwartał bez newslettera, marża na powtórne zamówienie, rozkład księgowy, awaria Safari w kwartale, baza powracających, przychód i koszty). To najciekawsza część zakładki, bo tłumaczy zastrzeżenie „−7% albo +1%”, a jest schowana pod jednym słowem.
- Tabela ekonomii kampanii (zwinięta): 1369 px, przewija się w bok (sprawdzone na żywo); osiem kolumn liczbowych, choć nad wykresem jest już przełącznik „Okno wyniku 90 / 180 dni”.

**Proponowany układ od góry:** 1. „Rok do roku”: wniosek w dwóch zdaniach i trzy liczby z tabeli jako kafelki (marża po wszystkich kosztach 1 048 tys. zł, +26,6%; marża przed kampaniami +41,5%; wydatki na kampanie +76,7%), zastrzeżenie, szczegóły zwinięte. 2. „Kwartały rok do roku”: słupki i tabela, z linijką „nie zależy od grupowania”. 3. „Miesiąc po miesiącu”: grupowanie w nagłówku karty, dwa wykresy, domyślnie tylko przyczyny jako linie, jedna lista zdarzeń pod kartą. 4. „Dlaczego III kwartał 2026 jest słabszy”: dzisiejsze szczegóły jako zwinięte podsekcje z nagłówkami. 5. Tabela miesięczna, zwinięta. 6. „Ekonomia kampanii” jak dziś, a tabela pokazuje tylko okno wybrane przełącznikiem (cztery kolumny).

**Tabele:** jak wyżej; w tabeli kwartalnej pierwsza kolumna „IV kw. 2025” wystarczy. **Sterowanie:** „Grupowanie” do nagłówka karty wykresów; ekonomia kampanii jest w porządku.

**Pracochłonność:** podział karty: średnia; przyczyny zamiast 14 linii i jedna lista: mała; kafelki: mała; zwinięcie miesięcy: mała; tabela ekonomii według okna: średnia.

### Jakość danych

**Czego szuka czytelnik:** czy może ufać liczbom i jak dashboard ma się do danych oczyszczonych. **Widzi na pierwszym ekranie** wniosek i mostek dashboard → dane czyste (`jakosc_01`). Dobrze.

**Co przeszkadza:**
- Karta 1 („Dane wymagały dwóch poprawek”) i karta 2 („Dashboard zawyża…”) mówią to samo; „Szczegóły” karty 1 to tylko linijka o źródle (125 znaków; sprawdzone na żywo), tak samo w „Drobnych niespójnościach” (74 znaki) i „Pozostałych sprawdzeniach” (100 znaków). Klik bez nagrody uczy, żeby nie klikać.
- „Godzina bez danych” (1 sesja zamiast 21) ma własną kartę, zastrzeżenie i szczegóły, choć tekst sam mówi, że wpływ jest pomijalny (`jakosc_04`).
- Akapity w wąskiej kolumnie, listy na pełną szerokość w tej samej karcie (`jakosc_04`, `jakosc_05`).

**Proponowany układ od góry:** 1. „Od dashboardu do danych oczyszczonych” = karty 1 i 2 razem, 2. „Duplikaty”, 3. „Zamówienia testowe”, 4. „Drobne sprawy” = godzina bez danych i drobne niespójności, 5. „Sprawdzone i czyste”, 6. „Skąd liczby w tej zakładce” jako jedyne miejsce ze źródłami. Tabele i sterowanie w porządku. **Pracochłonność:** wszystko małe.

### Priorytety

**Czego szuka czytelnik:** listę od najważniejszego z kwotą, miarą sukcesu i czasem. **Widzi na pierwszym ekranie** tabelę przeglądu z grupami i pigułkami (`priorytety_01`). To najlepszy pierwszy ekran w narzędziu.

**Co przeszkadza:**
- 10 809 px, dwanaście ekranów (sprawdzone na żywo); na telefonie 23 740 px. Między przeglądem a pozycją 1 stoi cały ekran zasad listy (`priorytety_02`–`priorytety_03`).
- Tabele scenariuszy w kartach 3, 4 i 9 (`priorytety_05`, `priorytety_06`, `priorytety_09`): sześć wierszy, cztery kolumny, w komórce dwie liczby („−11,9 tys. zł / pełny rok: −18,6 tys. zł”). Wiersze 1–3 mówią, ile kampania zarabia dziś i po naprawie, wiersze 4–6, ile da wyłączenie przy trzech założeniach; granicy między nimi nie ma. Karta mówi o kwocie rocznej, a główna liczba w komórce to kwota z 234 dni.
- Chipy „Czego nie wiemy: punkt 6, punkt 7” to numery bez nazw. Sekcje kart są niespójne: „Dlaczego” (1–4, 6, 7), „Dwie różne decyzje” (5), brak (8), „Dlaczego dopiero 9. miejsce” (9), „Co pokaże” (12).
- Stopka (`priorytety_13`) podaje ścieżki z notatek: `notatki/c_szkic.md`, `notatki/konsylium/…`, `notatki/recenzje/c_codex.md`. Dla czytelnika z Telemedi to nazwy wewnętrzne.
- Nagłówki grup („Pewne straty”, „Pauzy, które da się cofnąć”) są w tabeli, ale nie między kartami.

**Proponowany układ od góry:** 1. Wstęp jednym zdaniem, 2. Przegląd (tabela, pigułki), 3. Zasady zwinięte do zdania „Kolejność oznacza wagę decyzji; kwot nie sumujemy” plus „Szczegóły”, 4. Karty 1–12 z nagłówkami grup między nimi, 5. „Nie robimy teraz”, 6. Źródła bez ścieżek do notatek.

**Tabele:** scenariusze w dwóch grupach wierszy „Naprawić” i „Wyłączyć”; główna liczba to pełny rok, kwota z okresu działania pod spodem; domyślnie okno 90 dni, 180 w szczegółach. Tabela cennika (`priorytety_10`) jest dobra. **Sterowanie:** pigułki i „Wróć do przeglądu” wystarczają; `#priorytety?p=9` podświetla kartę (sprawdzone na żywo).

**Pracochłonność:** zasady, nazwy przy punktach, nagłówki grup, stopka, ujednolicenie sekcji: małe; tabele scenariuszy: średnia.

### Czego nie wiemy

**Czego szuka czytelnik:** co dane nie rozstrzygają i jaki test to domknie. **Widzi na pierwszym ekranie** tabelę (`niewiadome_01`). Dobrze.

**Co przeszkadza:**
- 21 wierszy w kolejności numerów, bez grup i bez wagi: wiersz 1 (decyzja warta od −31 do +180 tys. zł) i wiersz 14 (umowa z rankingiem) wyglądają tak samo.
- Kolumna „Dlaczego to ważne” miesza kwotę z uzasadnieniem w akapitach po 5–9 linijek (wiersze 1, 9, 21); czytelnik szuka kwoty. Kolumna „Pozycja listy priorytetów” to pełne tytuły w trzech linijkach i „—” w siedmiu wierszach.
- Stopka z „Notatka: notatki/c_szkic.md, sekcja 4” i listą plików wyników (`niewiadome_04`).

**Proponowany układ:** te same wiersze w grupach z nagłówkami, numery bez zmian (odnośnik `#niewiadome?n=4` podświetla wiersz; sprawdzone na żywo): „Kampanie i pozyskanie” (1, 2, 10, 11, 12, 20, 21), „Strona i ścieżka zakupu” (5, 6, 7, 18, 19), „Obsługa pacjenta” (3, 4, 17), „TelemediGO i cennik” (8, 16), „Komunikacja z pacjentem” (9), „Dane i rozliczenia” (13, 14, 15). Kolumny: Nr, Czego nie wiemy, Co od tego zależy (kwota wytłuszczona na początku komórki), Jak domknąć, Pozycja (numer i dwa słowa). Filtr „wszystkie (21)” pełni rolę powrotu.

**Pracochłonność:** grupy i krótka kolumna pozycji: małe; kwota na początek komórki: średnia.

### Kohorty: trzy uwagi spoza listy Kuby

1. Pod tytułem „Kohorty w podziale” stoi dwuwierszowy ciąg dat dla czterech okien naraz („Kohorty z pełnym oknem: 30 dni: A …; 60 dni: …”, `kohorty_05`). Pokazać tylko okno wybrane do tabeli, resztę w „Jak liczymy”.
2. Przypis pod krzywą powrotu („Każdy punkt krzywej liczymy z innych pacjentów…”, `kohorty_07`) to ostrzeżenie przed błędnym odczytem całego wykresu, a stoi pod nim drobnym drukiem. Jedno zdanie nad wykresem zwykłą czcionką.
3. Legenda przy prawej krawędzi wykresu dzień po dniu ucina nazwy serii („Pozostałe kampanie i …”, `kohorty_03`), tak samo w Lejku i Wyniku; nazwy są już pod wykresem, więc etykiety przy liniach mogą być krótkie albo w dymku.

## 3. Sprawy wspólne

**Nawigacja.** Nagłówek z zakładkami jest przyklejony, na dole każdej zakładki jest „Dalej: …”, a odnośniki między zakładkami ustawiają filtry i podświetlają kartę lub wiersz (sprawdzone na żywo dla `#lejek?…`, `#zdarzenia?z=…`, `#priorytety?p=…`, `#niewiadome?n=…`). Brakuje spisu kart w długich zakładkach: Priorytety 12 ekranów, Po zakupie 7, Kohorty 6, Zdarzenia 6, Wynik 5. Pigułki z Priorytetów są gotowym wzorem: rząd krótkich odnośników do kart pod tytułem zakładki.

**Powtórzenia: gdzie co mieszka.** Awaria Safari ma pełny opis w Lejku, Zdarzeniach (karta 12) i Priorytetach (karta 1, ten sam wykres hantli). Propozycja: pełny opis i wykres w Lejku, w Zdarzeniach „O ile” i odnośnik, w Priorytetach wykres zostaje, bo karta decyzji ma być samodzielna. Duplikaty i godzina bez danych: pełny opis w Jakości danych, w Zdarzeniach akapit. Lista 14 zdarzeń pod wykresami: jedna lista na kartę, tylko zdarzenia z linii na wykresie. Reguły przypisania źródła są tłumaczone w trzech miejscach (Kohorty, Wynik, Priorytety); jedno miejsce i odnośnik.

**Nazewnictwo okresów i grup.** Okresy mają trzy konwencje: „Okres A / Okres B” (Lejek, Kohorty), „rok wcześniej / ostatnie 12 miesięcy” (Po zakupie, Wynik, Jakość), „X 2025 – IX 2026”. Jedna: „rok wcześniej (X 2024 – IX 2025)” i „ostatnie 12 miesięcy (X 2025 – IX 2026)”, a pola dat w filtrach „Porównujemy … z …”. Grupy: „Pozostałe kampanie i kanały”, „spoza nowych kampanii”, „kampanie działające w obu latach” to nazwy tej samej albo prawie tej samej grupy; „Google Ads na markę”, „Google Ads: marka”, „Google Ads: hasło marki” to jedna kampania w trzech brzmieniach.

**Legenda kolorów.** Etykiety „lepiej / gorzej / bez oceny” są spójne, ale obok nich działają cztery inne systemy: „uwaga” (Wynik), „Znak zależy od przypisania” (ekonomia), „Do naprawy / Do sprawdzenia” (Lejek), „Pewność: Wysoka / Średnia / Niska / Test”. To znośne, jeśli każda tabela ma własną legendę, ale reguła istotności z punktu 4 Kuby musi objąć wszystkie tabele ze zmianą: Lejek, trzy tabele w Po zakupie, Kohorty. W tabelach kwartalnych Wyniku kolor jest uzasadniony.

**Odnośniki.** Cztery brzmienia; odnośniki do Po zakupie, Jakości danych i Wyniku lądują na początku zakładki. Potrzebne kotwice kart i jedno brzmienie „Pokaż w: Po zakupie, zwroty”; chipy „punkt 6” potrzebują nazwy.

**Puste prawe połowy kart.** Tekst wniosków ma około 610 px szerokości w karcie 1230 px (`po-zakupie_01`, `wynik_01`, `zdarzenia_01`, `jakosc_03`): pół ekranu bieli na każdym pierwszym ekranie. To miejsce na dowód wniosku: wykres udziału sesji nowych kampanii w Lejku, kafelki liczb w Wyniku. Nagłówki kart łamią się w wąskiej kolumnie, choć karta jest szeroka.

**Telefon (390 px).** Strona nie wychodzi poza ekran, tabele zamieniają się w listy etykieta–wartość, tabela lejka pokazuje tylko „Sesje” i „Sesja do płatności”, jest pływający przycisk „Zakładki” (sprawdzone na żywo). Do poprawy: nagłówek z notą o danych syntetycznych i trzema rzędami zakładek zajmuje 420 z 844 px pierwszego ekranu (nota do jednej linijki, zakładki tylko pod przyciskiem); tabele kwartalna, miesięczna, ekonomii i surowego wyniku metody przewijają się w bok bez wskazówki „przewiń w bok”.

## 4. Dziesięć zmian o największym zysku w stosunku do pracy

1. **Przyklejony pasek filtrów z przyciskiem „Przywróć domyślne” w Lejku i Kohortach** (średnia): odnośniki z innych zakładek ustawiają naraz pięć filtrów, a czytelnik nie ma dziś jak wrócić do stanu wyjściowego.
2. **Tabele mieszczą się w 1366 px: lejek w podziale, zwroty, ekonomia kampanii, kohorty w podziale** (duża, jeden kod dla wszystkich): dziś ucięta jest najważniejsza kolumna lejka, „Sesja do płatności”.
3. **Kolor tylko przy istotnej różnicy w każdej tabeli ze zmianą** (średnia): „−0,02 gorzej” przy ocenie i „+0,7 gorzej” przy 82 wizytach uczą czytelnika ignorować kolor także tam, gdzie ma znaczenie.
4. **Wynik biznesu: jedna karta na cztery, pięć przyczyn zamiast 14 linii, jedna lista zdarzeń** (średnia): dziś wykres marży jest nieczytelny w listopadzie 2025, a czytelnik przewija cztery ekrany jednej karty.
5. **Lejek: wykres udziału sesji nowych kampanii do karty wniosku, kroki lejka na drugi ekran** (mała): zakładka „Lejek” zaczyna pokazywać lejek bez przewijania przez dwa ekrany tekstu.
6. **Zdarzenia: tabela zdarzeń na górze, karty w parach przyczyna–skutek, jakość danych skrócona do akapitu** (mała do średniej): dziś pierwszą kartą jest najmniej istotne zdarzenie, a przyczyna i skutek stoją jako dwie równorzędne karty.
7. **Po zakupie: tabela punktualności 4×4, oceny zaraz po powrocie, zwroty na koniec** (średnia): 16-wierszowa tabela z kolorem w każdym wierszu i przerwany wątek opóźnień.
8. **Jedno brzmienie odnośników i kotwice do kart** (mała): część odnośników ląduje na początku zakładki zamiast przy karcie, o którą chodzi.
9. **Słowa zamiast kodów i numerów: okresy, grupy, punkty „Czego nie wiemy”, etykiety przyczyn na osi** (mała do średniej): „Okres A”, „punkt 6” i „5” na osi wymagają legendy, której czytelnik nie ma w głowie.
10. **Sprzątanie: puste „Szczegóły” w Jakości danych, zasady priorytetów zwinięte do zdania, stopki bez ścieżek do notatek, grupy w „Czego nie wiemy”** (mała): klik bez nagrody i nazwy plików z notatek osłabiają zaufanie do strony, która poza tym jest bardzo staranna.

## 5. Czego nie ruszać

- Karta „Kroki lejka” (`lejek_03`): paski z kreską roku wcześniej, „Przechodzi dalej”, etykieta „Najbardziej obniża płatności”, „Pokaż dla” w nagłówku. Wzór dla reszty narzędzia.
- Wykresy hantli: „Do naprawy” i „Do sprawdzenia”, „Przy tym samym porannym ruchu”, powroty w oknach, ekonomia kampanii z dwiema regułami, linią zera i etykietą „Znak zależy od przypisania”.
- Priorytety: tabela przeglądu z grupami i pigułkami, pasek „Ile warte / Pewność / Wdrożenie”, sekcje „Dlaczego / Co robimy / Po czym poznamy”, chipy „Zobacz w danych”, karta „Nie robimy teraz”, tabela cennika.
- Odnośniki, które ustawiają filtry i podświetlają kartę albo wiersz; przyklejony nagłówek; „Dalej: …”.
- Jakość danych: słupki mostka z kreską poziomu dashboardu i podpisem „bez zmian”, wykres duplikatów z zaznaczonym oknem, kolejność od dużego do małego.
- Oś zdarzeń z torami, kształtami i chipami obszarów; schemat karty „Co się zmieniło / O ile / Skąd wiemy (zwinięte)”.
- Wykresy godzinowe opóźnień ze wspólną skalą i blokiem porannym; „uwaga” przy wydatkach i brak oceny przy koszcie lekarza w tabeli kwartalnej.
- Blok „Zastrzeżenie” pod każdym wnioskiem i nagłówki kart pisane jako zdania z liczbą.
- Widok na telefonie: tabele w listy, przycisk „Zakładki”, brak przewijania strony w bok.
