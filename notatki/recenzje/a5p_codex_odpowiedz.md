**Główne liczby się potwierdzają, ale kilka wniosków wymaga zawężenia.** Najważniejsze korekty dotyczą miesięcznej konwersji nowych odwiedzających, grupy porównawczej dla Safari oraz stwierdzenia o stałym budżecie kampanii Meta.

Wszystkie poniższe wyliczenia wykonałem własnym kodem na schemacie `czyste`, z bazą otwartą tylko do odczytu. Nie uruchamiałem Waszych skryptów i nie zapisywałem plików.

1. **Lejek i rozkład zmiany — zgadza się.**

   W okresie 1 płatnością kończy się **24 717 ze 154 085 sesji zwykłych, czyli 16,041%**. W okresie 2 jest to **38 490 z 280 625 sesji, czyli 13,716%**. Spadek wynosi **2,325 punktu procentowego**.

   Podział według przeglądarki daje efekt struktury **−2,996 punktu procentowego** i efekt konwersji wewnątrz grup **+0,671 punktu procentowego**.

   Wzory są poprawną tożsamością rachunkową. Przyjęcie dla nowej grupy konwersji z okresu 2 jako zastępczej konwersji okresu 1 rzeczywiście przypisuje jej wkład w całości do struktury. To jawna konwencja, ponieważ historycznej konwersji tej grupy nie znamy.

   Rozkład zależy jednak od wyboru wag. Przy rozkładzie symetrycznym otrzymuję odpowiednio **−2,883 i +0,558 punktu procentowego**. Kierunek pozostaje ten sam. Wyniku +0,67 nie należy interpretować jako dowodu poprawy produktu: wewnątrz przeglądarek zmieniają się także kanały i udział pacjentów powracających.

2. **Pierwszy rok — zgadza się kierunek; nie zgadza się dokładny zakres miesięczny.**

   Konwersja osób bez wcześniejszego zakupu wynosi miesięcznie **10,755–11,564%**, czyli po zaokrągleniu **10,8–11,6%**. Wyjątkiem wobec podanego zakresu jest sierpień 2025: **1 074 płatności z 9 986 sesji, czyli 10,8%**.

   W kwartałach wynik jest jeszcze stabilniejszy: **11,28%, 11,28%, 11,12% i 11,12%**, kolejno od czwartego kwartału 2024 do trzeciego kwartału 2025. Wzrost zagregowanej konwersji wynika więc z rosnącego udziału sesji pacjentów powracających.

   Rozpoznawanie wcześniejszego zakupu jest poprawne względem przyjętej definicji. Sprawdziłem, że żadna przeglądarka nie jest przypisana do więcej niż jednego konta. Porównanie momentów po prawidłowym przeliczeniu na czas UTC nie zmienia klasyfikacji ani jednej sesji.

   Ograniczenie pozostaje: pacjenta używającego nowej przeglądarki, w której nigdy się nie zaloguje, nie da się rozpoznać jako powracającego.

3. **Safari na iOS — zgadzają się data, skala głównego spadku i rachunek 695; nie zgadzają się dwa uogólnienia.**

   Dla osób bez wcześniejszego zakupu:

   - przed zmianą: **1 167 przejść do kroku 3 na 1 763 wybory terminu, czyli 66,194%**;
   - po zmianie, w porównywalnym oknie 60 dni: **701 na 1 553, czyli 45,138%**.

   **17 marca 2026 jest najlepiej dopasowaną datą zmiany** w moim niezależnym przeszukaniu dat. Własna segmentacja wskazuje tylko tę datę przy karach 15, 25, 50 i 100. Ten konkretny sygnał jest mocny.

   Natomiast:
   
   - **Wszystkie pozostałe przeglądarki razem mają 64,828% → 63,380%.** Wartości 64,8% → 63,8% dotyczą węższej grupy raportu, która wyłącza również inne przeglądarki na iOS i Safari na macOS.
   - **Spadek nie występuje dosłownie w każdym kanale.** W TikToku jest 3/9 → 10/26, czyli **33,3% → 38,5%**. Próba jest bardzo mała. W pozostałych kanałach Safari na iOS spadek się potwierdza.

   Liczby zakończonych rejestracji **1 082 → 668** oraz logowań do istniejącego konta **659 → 619** potwierdzam. Są zgodne z problemem dotyczącym zakładania konta. Same liczby sukcesów nie dowodzą jednak przyczyny technicznej, ponieważ nie znamy zamiaru osób odpadających przed krokiem 3.

   Rachunek utraconych zamówień od 17 marca do 30 września odtwarza się:

   \[
   (2813/4254-2132/4678)\times4678\times1541/2132
   =694{,}88.
   \]

   **695 jest poprawnym szacunkiem przy przyjętym scenariuszu.** Po uwzględnieniu równoległego pogorszenia tego kroku we wszystkich pozostałych przeglądarkach otrzymuję około **628 zamówień**. To sprawdzenie wrażliwości, nie rozstrzygnięcie przyczynowe.

   Spośród sesji odpadających przed krokiem 3 późniejszy zakup w tej samej przeglądarce następuje w ciągu 30 dni po **6,7% sesji przed zmianą i 6,4% po zmianie**. Nie widać wzrostu odrabiania strat, ale szacunek 695 nadal nie jest liczbą bezpowrotnie utraconych unikalnych pacjentów.

4. **Sesje zalogowane od wejścia — zgadza się, z ograniczeniem interpretacji.**

   Potwierdzam **22 068 sesji i 12 461 pacjentów**. Usługę wybiera **4 574 sesji, czyli 20,727%**. Termin wybierają **112 sesji, czyli 2,449% sesji z wyborem usługi**. Żadna nie kończy się płatnością.

   Potwierdzam też **zero anonimowych sesji po pierwszym zakupie w przeglądarkach znanych z logowania**.

   Porównanie po punkcie kontrolnym jest policzone poprawnie. We wspólnych warstwach obejmuje **1 125 pacjentów z taką sesją**. Ich powrót w dniach 31–90 wynosi **16,0%**, wobec **13,210%** w grupie bez sesji po standaryzacji. Cała grupa z sesją liczy 1 142 pacjentów i ma surowy wynik 15,9%.

   Projekt poprawnie oddziela okres wyznaczania grup od okresu mierzenia wyniku. Nie znalazłem odwrócenia kierunku w sprawdzonych wariantach:

   - po dodatkowym uwzględnieniu miesiąca kohorty: **16,5% wobec 13,7%**;
   - po wyrównaniu dat końcowych kohort między latami: **15,9% wobec 13,2%**.

   Wynik dotyczy jednak wyłącznie osób bez kolejnego zamówienia w pierwszych 30 dniach. Nie rozstrzyga, czy sesja zalogowana pomaga albo przeszkadza w zakupie. Przy punkcie kontrolnym po 60 dniach w okresie 2 różnica praktycznie znika: **7,20% wobec 7,16%**.

   W zakupach powtórnych oba odstępy mają takie same sprawdzone kwantyle: **28 sekund, 83 sekundy i 137 sekund** dla percentyla 10., mediany i percentyla 90. Rozkłady empiryczne są bardzo podobne, ale nie identyczne. Czasów tych nie traktowałbym jako dowodu rzeczywistego ponownego logowania.

5. **Sezon a wydatki — zgadzają się mnożniki; nie zgadza się dosłownie „stały budżet, brak sezonu”.**

   Oba porównywane okna pierwszego roku mają po 123 dni.

   | Miara | X 2024–I 2025 | V–VIII 2025 | Zima / lato |
   |---|---:|---:|---:|
   | Nowi pacjenci z kanałów bezpłatnych | 2 606 | 1 906 | 1,367 |
   | Nowi pacjenci z kanałów płatnych | 2 985 | 2 494 | 1,197 |
   | Wydatki na kampanie | 121 658,69 zł | 114 552,95 zł | 1,062 |
   | Nowi pacjenci z Google Ads | 2 596 | 2 138 | 1,214 |
   | Wydatki Google Ads | 100 410,33 zł | 94 489,77 zł | 1,063 |

   Kampania Meta `meta_prosp_lekarz_online`, czyli pozyskanie na ogólną ofertę lekarza online, daje **351 nowych pacjentów zimą wobec 324 latem**. Jej wydatki wynoszą **19 329,42 zł wobec 18 359,88 zł**. Oznacza to zimą **8,3% więcej pacjentów przy wydatkach większych o 5,3%**. Liczba nowych pacjentów na złotówkę jest większa o **2,9%**.

   Uczciwy wniosek: **ta kampania nie pokazuje silnej sezonowości porównywalnej z kanałami bezpłatnymi**. Braku sezonowości nie da się dowieść tym porównaniem.

**Błędy w kodzie zmieniające wynik**

- Przy pierwszym odczycie [a5p_zalogowane.py](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5p_zalogowane.py:190>) średnie pomijały sesje bez jakiegokolwiek późniejszego zamówienia, ponieważ ich czas oczekiwania miał wartość `NULL`. Zawyżało to wyniki sekcji 3d i 4. Przykładowo raport pokazywał **14,3% zamiast 2,6%** zakupów w ciągu 7 dni po sesjach z newslettera lub SMS-a bez kroków lejka. **Podczas recenzji kod i raport zostały poprawione przez inną sesję. Przy ostatnim odczycie poprawka już była obecna.**
- W [sekcji 4c](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5p_zalogowane.py:235>) opis mówi o dniach bez sesji zalogowanej, lecz kod uwzględnia wszystkie dni. Faktyczny wynik dla dni bez takich sesji to **0,364 zamówienia na 100 pacjento-dni**, wobec raportowanych **0,375**. Różnica jest mała, ale opis i obliczenie powinny być zgodne.
- Nie znalazłem błędu rachunkowego w kodzie zmieniającego pięć głównych zestawów liczb poza opisanymi korektami interpretacji i zakresów.

**Słabości metody**

- Segmentacja pomija epizody krótsze niż 14 dni i grupy z mianownikiem poniżej 3 000. Limit sześciu zmian oraz zachłanny podział mogą przeoczyć bardziej złożony przebieg. Trend lub sezon mogą też zostać przedstawione jako skoki.
- Kara 25 nie daje deklarowanego poziomu istotności dla całego poszukiwania. Algorytm wybiera najlepszą datę spośród wielu dat i sprawdza wiele nakładających się serii. Dla Safari wynik jest odporny na sprawdzone zmiany kary.
- Porównanie po punkcie kontrolnym nadal różni grupy pod względem zainteresowania zakupem. Wykluczenie wczesnych zakupów dodatkowo zawęża populację. Standaryzacja nie usuwa tych różnic.
- Wyświetlenia Google Ads zależą również od budżetu i ustawień kampanii. Kanały bezpłatne mogą reagować na reklamę. Dlatego sezon nie został przyczynowo oddzielony od wydatków.

**Inne odczytania danych**

- Zimą Google Ads dostarcza **16,0% więcej kliknięć**, mimo wydatków większych tylko o 6,3%. Średni koszt kliknięcia jest niższy o **8,4%**. Część przewagi pozyskania wynika więc z tańszego ruchu; liczba nowych pacjentów na kliknięcie rośnie o dalsze **4,7%**.
- Wysoka konwersja powracających w „sesjach zwykłych” jest częściowo związana z definicją grupy. Sesje z kontem bez kroku 3 są odkładane do osobnej kategorii, a zwykłe sesje powracających wszystkie dochodzą do kroku 3. Nie należy przenosić ich konwersji na wszystkie wejścia obecnych pacjentów.
- Brak płatności w sesjach zalogowanych oraz podobne czasy kolejnych kroków pasują także do sposobu wygenerowania lub rejestrowania danych. Nie rozstrzygają samodzielnie o awarii ścieżki zakupowej.

Nie przeprowadziłem pełnej kalibracji fałszywych alarmów segmentacji, niezależnego audytu czyszczenia danych ani testu przyczynowego sezonowości.