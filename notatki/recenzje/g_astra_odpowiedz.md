Największy problem tego narzędzia to **kolejność dostępu do informacji**. Czytelnik często najpierw dostaje rozbudowane uzasadnienie, potem ustawienia, a dopiero po kilku ekranach właściwy widok danych. Drugi problem to brak wyraźnej granicy między stałym komentarzem autora a wynikiem zależnym od ustawień.

Recenzja obejmuje zrzuty, pełne teksty i szkielet HTML. Nie oceniam zakładki „Czy to wzrost”. Uwagi dotyczące telefonu i zachowania odnośników są wymaganiami do sprawdzenia, ponieważ materiały nie pokazują tych interakcji.

Szacunki dotyczą pracy nad interfejsem: **mała — do godziny, średnia — kilka godzin, duża — przebudowa kilku powiązanych elementów**.

**1. Ogólne zasady wynikające z uwag Kuby**

1. **Obietnica zakładki:** pierwszy ekran powinien pokazywać narzędzie odpowiadające nazwie zakładki oraz krótki wniosek potrzebny do jego odczytania.
2. **Odległe sterowanie:** ustawienia powinny znajdować się przy elementach, którymi sterują, a wspólne ustawienia mieć jedno widoczne miejsce.
3. **Pomieszany zakres:** stałe podsumowania muszą być oddzielone od wyników zmieniających się po użyciu filtrów.
4. **Odwrócona hierarchia:** szczegóły dowodowe i metodyczne powinny rozwijać odpowiedź, zamiast opóźniać dotarcie do niej.
5. **Rozproszone informacje:** pełne wyjaśnienie powinno mieć jedno miejsce, a pozostałe zakładki prowadzić do niego krótkim, opisowym odnośnikiem.
6. **Przeciążona tabela:** domyślny widok powinien służyć jednemu porównaniu, z jednostkami i czytelnymi okresami, bez ukrywania kluczowej kolumny poza ekranem.
7. **Pozorna pewność:** kolor i słowa „lepiej” lub „gorzej” nie mogą sugerować potwierdzonej zmiany, jeśli pokazujemy tylko różnicę liczbową.
8. **Niewidoczny stan:** czytelnik powinien zawsze wiedzieć, jakie dane ogląda i jak wrócić do ustawień początkowych.
9. **Nawigacja wymagająca pamięci:** nazwy odnośników powinny opisywać cel, zamiast wymagać zapamiętywania numerów zdarzeń, priorytetów i niewiadomych.

**2. Lejek**

Czytelnik szuka odpowiedzi: **na którym kroku, w jakiej grupie i od kiedy tracimy kupujących**. Na pierwszym ekranie widzi interpretację, ale właściwy lejek dopiero na `lejek_03`.

**Układ od góry — średnia.** Zostawić dwuzdaniowy wniosek. Następnie umieścić pasek „Sesje w analizie”, kroki lejka oraz kartę „Konwersja dzień po dniu” z tabelą grup. Dopiero niżej dać rozpoznane problemy: Safari i przeglądarki w aplikacjach. Długie wyjaśnienie struktury ruchu z `lejek_01` zwinąć. Wykres udziału nowych kampanii z `lejek_03–04` przenieść do tego wyjaśnienia: obecnie przecina ciąg elementów zależnych od filtrów, choć sam tych filtrów nie uwzględnia.

**Sterowanie — średnia.** „Sesje w analizie” powinno zawierać grupę osób, typ sesji i porównanie okresów. Podział musi być wspólny dla wykresu dziennego i tabeli. „Pokaż dla” przy krokach przemianować na „Grupa pokazana w lejku”; to inne działanie niż zaznaczanie kilku serii na wykresie. Przy każdej karcie wskazać zależności jednym zdaniem. Dodać uzgodnione już przywracanie ustawień domyślnych.

**Tabela — duża.** Na `lejek_05` najważniejsza końcowa kolumna „Sesja do płatności” wypada poza widoczny obszar. Domyślnie pokazać grupę, liczebność, wynik wybranej miary w obu okresach i zmianę. Pełny zestaw kroków pozostawić jako drugi widok. Nazwy okresów zastąpią „A” i „B”, a każda zmiana otrzyma jednostkę.

Nie wolno jednak mechanicznie zastosować zasady „jedna liczebność na wiersz” do wszystkich kroków: przejście do płatności ma inną podstawę niż wybór terminu. W widoku jednej miary pokazać jej podstawę; w pełnej tabeli udostępnić podstawę każdej komórki po kliknięciu.

**Oznaczenia — mała.** „Najbardziej obniża płatności” na `lejek_03` zastąpić dokładniejszym „Największe względne pogorszenie przejścia”. Obecna etykieta brzmi jak wyjaśnienie przyczynowe. Drobne zmiany z `lejek_05–06` pozbawić ocen kolorystycznych, jeśli nie mają odpowiedniego potwierdzenia.

**3. Po zakupie**

Czytelnik szuka odpowiedzi: **czy wizyty przebiegają dobrze i jak opóźnienia oraz zwroty wiążą się z dalszym zachowaniem pacjentów**. Pierwszy ekran pokazuje problem punktualności, lecz zwroty pojawiają się dopiero na `po-zakupie_06`.

**Układ od góry — średnia.** Zacząć krótkim podsumowaniem dwóch problemów: opóźnień internistów i zwrotów po wizytach dotyczących zwolnień lekarskich. Następnie pokazać punktualność w czasie, zwroty, powroty po spóźnionej pierwszej wizycie i oceny. Na końcu umieścić „Diagnozę porannych opóźnień”, łącząc rozkład godzinowy z porównaniem przy podobnym ruchu. Zachować zastrzeżenie, że obserwowany związek opóźnień z powrotami nie dowodzi przyczyny.

**Pierwsza karta — średnia.** Skrócić wstęp z `po-zakupie_01`, aby więcej wykresu mieściło się na pierwszym ekranie. Pod wykresem domyślnie pokazywać tylko wiersze wybranej specjalizacji. Pełna tabela wszystkich specjalizacji z `po-zakupie_02–03` powinna być rozwijana. Obecnie jej długość odsuwa kolejne problemy, a wybór „Internista” nie ogranicza widocznej tabeli.

**Sterowanie — średnia.** Zachować lokalne filtry, ponieważ karty analizują różne populacje. Przy punktualności napisać wprost, które ustawienia dotyczą wykresu, a które również tabeli. Przy pozostałych kartach umieścić etykiety aktualnej grupy oraz lokalne przywracanie ustawień. Szczególnie ważne jest rozróżnienie „Wszyscy” przy porównaniu ruchu i „Spoza nowych kampanii” przy powrotach. Stałe wnioski powinny być oznaczone jako podsumowanie ustawień domyślnych.

**Tabele — średnia.** Tabelę zwrotów z `po-zakupie_07` rozdzielić na „Odsetki i liczby wizyt” oraz „Zwrócone zapłaty i koszt lekarza”; obecnie prawa część jest ucięta. W tabeli ocen z `po-zakupie_08` oddzielić liczbę wizyt od liczby ocen, zamiast powtarzać tę drugą przy dwóch miarach. Zmiany średniej oceny opisywać jako punkty skali 1–5, a zmiany odsetków jako punkty procentowe. Usunąć czerwone „gorzej” przy zmianie średniej o 0,03, skoro tekst sam mówi, że porównania z niewielką grupą wcześniejszych ocen nie interpretujemy.

**4. Zdarzenia**

Czytelnik szuka odpowiedzi: **co wydarzyło się kiedy i gdzie może obejrzeć zmianę w danych**. Na `zdarzenia_01` oś jest widoczna, ale jej numery wymagają dalszego szukania opisów.

**Układ od góry — średnia.** Zgodnie z decyzją Kuby pierwszą kartą powinien zostać przegląd przeniesiony z „Kohort”. Potem oś czasu, a pod nią opisy zdarzeń. Dotychczasową dużą kartę wprowadzającą skrócić do zdania pod tytułem. Surowe wyniki automatycznego wykrywania zmian pozostawić zwinięte na końcu.

**Przenoszona tabela — średnia.** Nie kopiować jej obecnej szerokości i gęstości z `kohorty_01–02`. Domyślnie zostawić datę, nazwę zdarzenia, grupę, krótkie porównanie oraz działanie. Rozwinięcie wiersza pokaże pełne liczebności, warunki wyceny i ograniczenia. Kwoty opisać jako „Skala problemu lub wartość działania”, ponieważ obecna kolumna miesza historyczne zwroty, jednorazowy wzrost marży i roczne scenariusze napraw.

**Opisy zdarzeń — średnia.** Na `zdarzenia_02–07` każde zdarzenie dostaje rozbudowaną kartę, często powtarzającą inne zakładki. Zastąpić je zwartymi rozwijanymi pozycjami: data, nazwa i jedno zdanie o zmianie pozostają widoczne. Szczegółowa diagnoza Safari mieszka w „Lejku”, opóźnienia w „Po zakupie”, a duplikaty w „Jakości danych”. Tutaj pozostają chronologia, dowód datowania i odnośnik.

**Sterowanie i nazwy — średnia.** Filtry obszarów powinny obejmować przegląd, oś i listę opisów, z widoczną liczbą wyników oraz przyciskiem „Pokaż wszystkie”. Kliknięcie zdarzenia na osi powinno otwierać jego opis. „Kandydat poniżej progu” z `zdarzenia_05` przemianować na „Spadek bez potwierdzonej daty przełomu”. Start kampanii i późniejszą zmianę zachowania nadal pokazywać osobno; bliskość dat nie powinna sugerować udowodnionej przyczyny.

**5. Wynik biznesu**

Czytelnik szuka odpowiedzi: **ile zostaje po uwzględnionych kosztach i które kampanie pokrywają koszt pozyskania pacjenta**. Pierwszy ekran podaje wnioski, lecz wykres zaczyna się przy dolnej krawędzi, a ekonomia kampanii dopiero na `wynik_05`.

**Układ od góry — średnia.** Zostawić krótki wniosek roczny i krótkie zastrzeżenie dotyczące III kwartału. Następnie pokazać wykres marży po koszcie lekarza, kampaniach i prowizji, ekonomię kampanii, porównanie marży przed kampaniami z wydatkami, a potem kwartały. Szczegółowe zestawienie miesięcy przenieść na koniec i zwinąć. Pełny opis jednorazowego startu sprzedaży TelemediGO powinien być tutaj, przy porównaniu kwartałów; „Zdarzenia” wystarczą jako skrót chronologiczny.

**Ekonomia kampanii — średnia.** Nagłówek na `wynik_05` mówi o TikToku, lecz domyślny wykres pokazuje połączone kampanie Meta i TikTok. Ustawić początkowo poziom pojedynczych kampanii, aby można było zobaczyć dowód dla wniosku. Zachować obie reguły przypisania obok siebie. Na `wynik_06` znacznik zera pierwszego wiersza nie jest wyrównany z pozostałymi; wszystkie wiersze powinny korzystać z tej samej osi i skali.

**Tabele — średnia.** „Marża” w tabeli kwartalnej z `wynik_03` wymaga pełniejszego nagłówka, ponieważ wykres bezpośrednio nad nią pokazuje inną marżę. W zestawieniu miesięcy z `wynik_04` potrzebny jest przypięty nagłówek. Domyślna tabela ekonomii powinna przedstawiać jedno wybrane okno: 90 albo 180 dni. Liczebności zachować osobno dla obu reguł przypisania, bo grupy nie są identyczne; szczegółowe rozpisanie „marża minus koszt” można rozwinąć.

**Sterowanie i oznaczenia — średnia.** Grupowanie na dni, tygodnie lub miesiące umieścić przy wykresach czasowych i wyraźnie wyłączyć z jego zakresu stałe porównania kwartalne. Filtry ekonomii pozostawić lokalne. Usunąć podwójne listy czternastu zdarzeń z `wynik_02`, zostawiając jeden wybór zdarzeń i odnośnik do osi. W tabelach finansowych kolor powinien oznaczać kierunek biznesowy, bez udawania testu statystycznego zmian księgowych.

**6. Jakość danych**

Czytelnik szuka odpowiedzi: **czy można ufać wynikom i co zmieniło oczyszczenie danych**. Odpowiedź jest już na `jakosc_01`, ale pierwsza karta odsuwa najbardziej użyteczne porównanie.

**Układ od góry — mała.** Połączyć wstęp z porównaniem dashboardu i oczyszczonych danych. Najpierw pokazać zmianę wzrostu zamówień z 60,7% do 55,7% oraz przychodu z 50,3% do 44,8%, z nazwanym okresem porównania. Następnie dwie poprawki: duplikaty i zamówienia testowe. Na końcu jedna sekcja „Pozostałe sprawdzenia”, zawierająca lukę godzinową, drobne niespójności i kontrole bez wykrytych problemów.

**Treść — mała.** W karcie testów z `jakosc_03` zostawić liczbę zamówień, liczbę kont i zasadę wyłączenia. Rozbudowane rozpoznawanie testów przenieść do „Jak rozpoznaliśmy zamówienia testowe”. Nie chować informacji o niepewnym koszcie lekarzy. „Pozostałe sprawdzenia wyszły czysto” zastąpić „W pozostałych sprawdzeniach nie wykryliśmy niespójności”; zakres twierdzenia będzie zgodny z zakresem kontroli.

**Wykresy i tabela — mała.** Z wykresu liczby zamówień usunąć powtórzony słupek „po odjęciu zwrotów”, który pozostaje bez zmian. Zachować ten etap przy przychodzie i w pełnej tabeli. Nagłówek „TelemediGO” doprecyzować jako liczbę zakupów programu, ponieważ obok występuje przychód w złotych. Przy 604 duplikatach i 2071 zamówieniach testowych jawnie podać zakres czasu.

**Sterowanie — mała.** Ta zakładka nie potrzebuje filtrów. Potrzebuje krótkiego oznaczenia, że pokazuje stałe porównanie obu lat, oraz opisowych rozwinięć zamiast kilku jednakowych „Szczegółów”. Pełne uzasadnienie oczyszczania pozostaje właśnie tutaj.

**7. Priorytety**

Czytelnik szuka odpowiedzi: **co zrobić najpierw, ile to może dać i po czym rozpoznać efekt**. Pierwszy ekran spełnia tę obietnicę lepiej niż większość zakładek, lecz pełna lista i dwanaście rozbudowanych kart wymagają bardzo długiego przewijania.

**Układ od góry — średnia.** Nad przegląd przenieść dwa zdania z `priorytety_02`: kolejność oznacza wagę decyzji, a kwot nie sumujemy. Dalej pozostawić listę w obecnej kolejności, następnie rozwijane karty działań i na końcu „Czego teraz nie robimy”. Usunąć osobny rząd przycisków 1–12 z `priorytety_01`; nazwy działań w przeglądzie powinny być odnośnikami.

**Karty działań — średnia.** W rozwiniętej karcie na początku pokazać działanie, wartość z warunkiem, czas wdrożenia i sposób pomiaru. „Dlaczego” skrócić, a pełne uzasadnienie skierować do właściwej zakładki. Powtórzone hantle Safari z `priorytety_03` można usunąć, zostawiając jedno porównanie tekstowe i odnośnik do lejka. Tabele scenariuszy z `priorytety_05`, `06` i `10` zwinąć pod „Założenia i warianty wyceny”.

**Jednostki i pewność — mała.** Nagłówek „Ile warte rocznie” nie pasuje do kosztu testu ani do wartości jednego punktu procentowego poprawy powrotów. Zastąpić go „Wartość lub koszt”, zachowując bezpośrednio przy kwocie właściwy horyzont i warunek. Nie zmieniać wycen. Rozdzielić też „rocznie” od okna, w którym liczymy wartość pacjenta: 90 lub 180 dni.

„Test” nie jest poziomem pewności, a „Wysoka” przy Safari dotyczy obserwowanego problemu, nie pewności odzyskania całej kwoty. Zamiast jednej wspólnej etykiety zastosować krótkie opisy, np. „Problem potwierdzony; wycena scenariuszowa” i „Decyzja wymaga testu”.

**Sterowanie — średnia.** Odnośnik powinien otwierać właściwą kartę, a „Wróć do przeglądu” wracać do odpowiedniego wiersza. Można dodać filtr istniejących grup działań, bez zmiany rankingu. Domyślnie pokazywać wszystkie. W tabelach scenariuszy przełącznik okna 90/180 dni ograniczy szerokość; obie reguły przypisania powinny pozostać widoczne jednocześnie.

**8. Czego nie wiemy**

Czytelnik szuka odpowiedzi: **co blokuje konkretną decyzję i jakie sprawdzenie usunie tę niewiadomą**. Pierwszy ekran pokazuje właściwą treść, ale tabela wymaga czytania długich akapitów w kilku wąskich kolumnach.

**Układ od góry — średnia.** Zostawić krótki wstęp, potem filtr decyzji, filtr obszaru i wyszukiwanie tekstowe. Niżej pokazać zwarty rejestr pytań z rozwijanymi szczegółami. Nie zmieniać numerów, bo prowadzą do nich istniejące odnośniki. Pełne opisy testów powinny pozostać w kartach priorytetów; tutaj wystarczy rodzaj testu, potrzebne dane oraz ograniczenie, które test rozstrzyga.

**Tabela — średnia.** Na `niewiadome_01` pierwszy wiersz zajmuje dużą część ekranu przez szczegółowy opis testu regionalnego. W widoku podstawowym wystarczą trzy kolumny: „Pytanie”, „Co trzeba sprawdzić” i „Decyzja, która od tego zależy”. Numer można umieścić przy pytaniu. Kwoty i uzasadnienia zostawić w rozwinięciu. Długie pytanie o przeglądarki z `niewiadome_03` skrócić do „Czy niższa konwersja wynika z przeglądarki, czy z grupy użytkowników?”.

**Oznaczenia — mała.** Myślnik w kolumnie priorytetu zastąpić „Bez osobnego działania na liście”. Nie wygląda wtedy jak brak danych. Zmienić „wszystkie (21)” na „Wszystkie pytania — 21”, bo obecny podpis może sugerować 21 priorytetów. Kwoty zachowują walutę i horyzont, a procenty pozostają przy nazwanej grupie. Kolorowanie nie jest tutaj potrzebne.

**Sterowanie — średnia.** Po filtrowaniu wyświetlać aktywny wybór, liczbę wyników i „Pokaż wszystkie”. Odnośnik z innej zakładki powinien odsłonić właściwe pytanie nawet wtedy, gdy wcześniejszy filtr by je ukrywał. Techniczne ścieżki plików z `niewiadome_04` przenieść do rozwijanych źródeł.

**9. Jedna dodatkowa uwaga do Kohort**

**Liczebność musi odpowiadać wybranej mierze — mała.** Przy wdrażaniu „liczby pacjentów raz na wiersz” nie zastępować liczby pacjentów z pełnym oknem ogólną liczebnością grupy. Dla powrotu w 90 dni potrzebna jest liczebność osób obserwowanych przez 90 dni, a dla 180 dni będzie ona inna. W opcjonalnym widoku wszystkich okien podstawy muszą pozostać dostępne przy poszczególnych wynikach.

**10. Sprawy wspólne**

**Nawigacja — średnia.** Zachować górne zakładki, ale po przewinięciu zmniejszać część z tytułem i opisem zadania. Przypięte nagłówki tabel powinny znajdować się pod nawigacją. Odnośniki do kart muszą uwzględniać jej wysokość. Powrót przeglądarką powinien odtwarzać poprzedni widok, ustawienia i pozycję.

**Miejsce pełnych wyjaśnień — średnia.** Datowanie zmian i chronologia mieszkają w „Zdarzeniach”; diagnoza konwersji w „Lejku”; obsługa wizyt i zwroty w „Po zakupie”; ekonomia w „Wyniku biznesu”; czyszczenie w „Jakości danych”; działania i scenariusze w „Priorytetach”; braki dowodowe w „Czego nie wiemy”. Krótki wniosek może się powtarzać, pełna argumentacja nie powinna.

**Okresy i grupy — mała.** Stosować „Rok wcześniej: październik 2024–wrzesień 2025” oraz „Ostatnie 12 miesięcy danych: październik 2025–wrzesień 2026”. Przy własnych zakresach używać „Okres porównania” i „Okres analizowany”. Rozróżniać pacjentów pozyskanych przez kampanię od sesji pochodzących z kampanii. „Nowe kampanie na L4” przy pierwszym użyciu rozwinąć jako kampanie Meta i TikTok promujące konsultacje dotyczące zwolnień lekarskich.

**Kolory — średnia.** Oddzielić barwy serii, zaznaczenie wiersza i ocenę zmiany. Dla dostępnych wyników potwierdzających brak wyraźnej różnicy używać szarej etykiety. Gdy oceny statystycznej w ogóle nie ma, napisać „Zmiana opisowa — bez oceny”, zamiast twierdzić, że różnicy nie wykryto. Nie wprowadzać nowego arbitralnego progu liczebności ani nowych obliczeń.

**Odnośniki i stan — średnia.** Zamiast „punkt 7” stosować „Czy pacjenci z Safari kupili na innym urządzeniu?”. Przycisk ustawiający porównanie powinien mówić, co ustawi. Przywracanie ustawień czyści parametry danej analizy, ale pozostawia użytkownika w jej zakładce.

**Telefon — duża.** Tabele tekstowe zamieniać w rozwijane wiersze z podpisanymi polami. W tabelach analitycznych pokazywać jedną miarę i przypiętą nazwę grupy. Dane dostępne po najechaniu udostępnić również po dotknięciu. Ograniczyć wysokość przypiętego nagłówka i filtrów. Sprawdzić także pełne legendy: już przy 1366 pikselach część nazw serii jest skracana.

**11. Dziesięć zmian o największym zysku względem pracy**

1. **Przenieść kroki lejka bezpośrednio pod krótki wniosek — średnia.** Czytelnik od razu dostanie widok, po który otworzył zakładkę.
2. **Zwinąć tabelę wszystkich miesięcy w „Wyniku biznesu” — mała.** Ekonomia kampanii przestanie być ukryta za kilkudziesięcioma wierszami.
3. **Przenieść zwroty tuż pod punktualność — mała.** Drugi ważny problem obsługi pacjentów przestanie wyglądać na późniejszy dodatek.
4. **Dopisać zakres działania filtrów przy kartach — mała.** Czytelnik przestanie przypisywać zmianom ustawień wpływ na elementy, których one nie sterują.
5. **Przenieść zastrzeżenie o niesumowaniu kwot nad priorytety — mała.** Zapobiegnie to błędnej interpretacji, zanim czytelnik zacznie porównywać wyceny.
6. **Ujednolicić jednostki, okresy i nazwy grup — mała.** Zniknie konieczność rozszyfrowywania „A”, „B” i nieopisanych zmian liczbowych.
7. **Pokazać pojedyncze kampanie i wyrównać ich skalę — średnia.** Wykres ekonomii zacznie bezpośrednio uzasadniać wniosek o TikToku.
8. **Usunąć nieuzasadnione czerwone i zielone oceny — średnia.** Interfejs przestanie nadawać drobnym różnicom rangę potwierdzonego problemu.
9. **Zastąpić numery opisowymi odnośnikami — mała.** Nawigacja przestanie wymagać pamiętania struktury całego dokumentu.
10. **Ujednolicić przywracanie ustawień domyślnych — średnia.** Eksperymentowanie z narzędziem stanie się odwracalne i łatwiejsze do zrozumienia.

**12. Czego nie ruszać**

Zachować nagłówki zaczynające się od wniosku, porównania przed i po oraz hantle pokazujące dwie wartości. To skutecznie skraca drogę od danych do znaczenia.

Zachować rozdzielenie obserwacji od hipotezy, zwłaszcza przy opóźnieniach, zwrotach i przeglądarkach w aplikacjach. Zastrzeżenie zmieniające interpretację powinno pozostać widoczne obok wyniku.

Zachować obie reguły przypisania źródła w ekonomii kampanii, pełne okna obserwacji kohort oraz oznaczenie brakującego okna. Uproszczenie prezentacji nie może usuwać tych różnic.

Zachować kolejność priorytetów i pola „Co robimy”, „Po czym poznamy” oraz czas wdrożenia. Problemem jest długość prezentacji, nie sam schemat decyzji.

Zachować informację o syntetycznych danych, zakres dat i możliwość dotarcia do metod oraz źródeł. Techniczne nazwy plików można schować, ale możliwość sprawdzenia pochodzenia liczby powinna zostać.