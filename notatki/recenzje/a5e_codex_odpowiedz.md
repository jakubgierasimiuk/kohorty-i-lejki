Liczby z punktu 1 są poprawne, ale scenariusze „naprawić” wymagają korekt rachunkowych, a decyzji o wyłączeniu kampanii nie da się uzasadnić samą atrybucją ani obecnym testem dodatkowości.

Przeliczenia wykonałem własnym kodem, bez importowania skryptów projektu. Bazę otworzyłem z `read_only=True`. Niczego nie zapisałem.

1. **Ważna — końcowe zestawienie „naprawić” miesza horyzonty i podstawy obliczeń.**

   **Problem.** Sekcja E3 opisuje wynik w 90 dniach, ale dodaje do niego wartość zgód marketingowych wycenioną przy użyciu marży z dni 1–180. Korzyść ze zmniejszenia zwrotów pochodzi natomiast ze wszystkich wizyt w okresie 2. Nie jest to spójny wynik tych samych kohort w jednym horyzoncie.

   **Dowód.** W [a5e_scenariusze.py:395](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a5e_scenariusze.py:395) wartość zgód jest mnożona przez 95,6 zł. Następnie [wiersz 453](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a5e_scenariusze.py:453) dodaje tę kwotę do wyniku opisanego jako 90-dniowy.

   Dodatkowo roczna prognoza obu kampanii nie sumuje się z prognozami kampanii liczonych osobno. Według Z1K suma wyników Meta i TikToka wynosi **15 917 zł**, natomiast wiersz „obie” pokazuje **17 849 zł**. Przyczyną jest zastosowanie jednej średniej marży z dojrzałych kohort do rocznika o innym udziale obu kampanii — [wiersze 320–326](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a5e_scenariusze.py:320).

   **Poprawka.** Ujednolicić kohorty i horyzont każdej kolumny. Prognozę roczną liczyć osobno dla każdej kampanii, a potem sumować. Nazwać ją prognozą marży rocznika pozyskanych pacjentów, ponieważ obejmuje również przyszłe przychody po końcu okresu 2.

2. **Ważna — wariant B zmniejszenia zwrotów wymaga innego mianownika i rzeczywistych kosztów lekarza.**

   **Problem.** Wariant A zachowuje liczbę wizyt. Wariant B usuwa wizyty, więc zmniejsza zarówno liczbę zwrotów, jak i liczbę wszystkich odbytych wizyt. Oba warianty nie mogą używać tej samej liczby unikniętych zwrotów. Ponadto nie każda wizyta L4 kosztuje 25 zł.

   **Dowód.** [a5e_scenariusze.py:359](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a5e_scenariusze.py:359) stosuje w obu wariantach różnicę odsetków pomnożoną przez dotychczasową liczbę wizyt.

   Dla Z1K mamy 1 024 zwroty na 5 895 wizyt. Docelowy odsetek pozostałych pacjentów wynosi dokładnie 270/5 080:

   - Wariant A wymaga utrzymania płatności za **710,68 wizyty**. Przy obecnej średniej kwocie zwrotu daje to **57 112 zł**, zamiast raportowanych 57 349 zł. Różnica wynika z przedwczesnego zaokrąglenia odsetków.
   - Wariant B wymaga rozwiązania równania `(1024 − x)/(5895 − x) = 270/5080`. Wynik to **750,58 usuniętej wizyty**, zamiast około 713.
   - Wśród 1 024 zwróconych wizyt L4 nowych kampanii **983 były u internisty, a 41 u psychiatry**. Średni koszt lekarza wynosił więc około **32,01 zł**, zamiast 25 zł.

   Przy reprezentatywnym usuwaniu tych wizyt oszczędność kosztu lekarza wyniosłaby około **24 024 zł**, zamiast raportowanych 17 832 zł. To nadal korzyść przed utratą ewentualnego TelemediGO i późniejszej marży tych pacjentów.

   **Poprawka.** Rozdzielić wzory obu wariantów. Używać dokładnych odsetków i kosztów poszczególnych specjalizacji. W wariancie B osobno uwzględnić utraconą marżę pacjentów oraz rozróżnić usunięte wizyty od utraconych nowych pacjentów.

3. **Ważna — rachunek „wyłączyć” jest poprawny warunkowo, ale średnia marża przypisanych pacjentów nie musi być marżą pacjentów dodatkowych.**

   **Problem.** Wzór „oszczędzone wydatki minus dodatkowi pacjenci razy marża” jest właściwy. Wymaga jednak założenia, że pacjenci dodatkowi mają taką samą średnią marżę jak wszyscy pacjenci przypisani kampanii. Przy dodatkowości 50% to nie wynika z danych.

   **Dowód.** [a5e_scenariusze.py:338](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a5e_scenariusze.py:338) skaluje jedną średnią przez 100%, 50% i 0%. Przykładowo dokładny wynik wyłączenia TikToka według Z1K wynosi odpowiednio **+11 928 zł, +47 196 zł i +82 464 zł** przy zachowaniu tych założeń.

   **TelemediGO i koszt lekarza są już uwzględnione w marży.** Dla dojrzałych pacjentów obu nowych kampanii według Z1K przychód z TelemediGO w dniach 0–90 wynosi **6 408 zł**. Nie należy ponownie dodawać oszczędności kosztu lekarza do wyniku wyłączenia.

   Brakuje natomiast marży po przyjętym horyzoncie. Wariant 180-dniowy częściowo to pokazuje, ale porównuje inne kohorty. Niższa średnia TikToka w 180 niż w 90 dniach nie dowodzi spadku wartości pacjenta wraz z wiekiem.

   **Poprawka.** Pokazać osobno wrażliwość na udział pacjentów dodatkowych i ich marżę. Dopisać założenie o niezmienionych kosztach pozostałych kanałów oraz zachowaniu pacjentów, którzy przyszliby bez kampanii. Przyszłą marżę oceniać na tych samych kohortach.

4. **Ważna — niektóre opisy sugerują przyczynowość, której dane nie potwierdzają.**

   **Problem i dowód.**

   - [a5e_scenariusze.py:177](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a5e_scenariusze.py:177) nazywa powrót przypisany newsletterowi lub SMS-owi „dolną granicą wpływu kontaktu”. To nie jest dolna granica wpływu. Pacjent mógłby kupić również bez wiadomości.
   - Rachunki zgód odtworzyłem: dla obu nowych kampanii Z1K daje **1 900 zł** według powrotów przypisanych wiadomościom, ale tylko **53 zł** według całej obserwowanej różnicy powrotów. Wybranie większej wartości w [wierszu 448](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a5e_scenariusze.py:448) tworzy optymistyczny wariant, nie centralne oszacowanie korzyści.
   - [Wiersz 427](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a5e_scenariusze.py:427) stwierdza, że niska konwersja jest cechą ruchu, a nie przeglądarki. Dane pokazują jedynie brak niższej **surowej konwersji w tej samej sesji**. Nie rozdzielają wpływu urządzenia, daty, pacjenta i powrotu w innej sesji.

   Wartość powrotu **95,6 zł** odtworzyłem: dokładna różnica to **95,581 zł**. Po podstawieniu współczynników z raportu retencji rachunki poranka również są poprawne: **31 806 zł, 65 247 zł, 12 656 zł i 11 931 zł**. Zastrzeżenia przyczynowe w sekcji C są zasadne. Jednak zakres **11 931–65 247 zł** jest zakresem wybranych scenariuszy, a nie przedziałem możliwego efektu. Efekt może wynosić zero. „Cały spadek” nie stanowi formalnej górnej granicy.

   **Poprawka.** Usunąć określenia „dolna granica wpływu” oraz rozstrzygnięcie o przyczynie niskiej konwersji. Warianty zgód pokazywać osobno, z ich założeniami. Scenariusz poranka uzupełnić o brak efektu.

5. **Ważna — wniosek o dodatkowości wymaga zawężenia do pozyskania łącznego.**

   **Problem.** Brak spadku liczby pacjentów rok do roku nie wyklucza przejmowania pacjentów. Pozostałe kanały mogłyby bez kampanii rosnąć szybciej.

   **Dowód.** Odtworzyłem porównania 28-dniowe z [a5e_scenariusze.py:267](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a5e_scenariusze.py:267):

   - Po starcie Meta iloraz zmian dla wszystkich pozostałych kanałów wynosi **1,043**, z przedziałem 95% **0,936–1,163**.
   - Dla L4 w pozostałych kanałach wynosi **0,815**, z przedziałem **0,644–1,030**.
   - Dla kampanii Google Ads `gs_generic_l4` wynosi **0,668**, z przedziałem **0,455–0,981**.

   Wykonałem dodatkowe porównanie: zmianę pozyskania L4 względem innych usług w pozostałych kanałach, skorygowaną o analogiczną zmianę rok wcześniej. Po starcie Meta iloraz wynosi **0,730**, z orientacyjnym przedziałem 95% **0,560–0,951**. Po starcie TikToka wynosi **0,900**, z przedziałem **0,714–1,136**.

   Jest więc sygnał względnego osłabienia L4 po starcie Meta. Nie jest to dowód przejmowania pacjentów: porównanie nadal wymaga założenia wspólnego trendu, a przedziały zakładają niezależne zliczenia.

   Przybliżenie z sekcji D4 odtworzyłem. Suma przed zaokrągleniem wynosi **226,00 pacjentów**; raportowane **227** powstaje przez sumowanie zaokrąglonych miesięcy. To około 3,1% z 7 268 pacjentów kampanii, ale nie oszacowanie udziału niedodatkowych pacjentów.

   **Poprawka.** Napisać: „Nie widać dużego spadku łącznego pozyskania w pozostałych kanałach. Widać jednak sygnał względnego osłabienia L4 po starcie Meta. Dane nie rozstrzygają dodatkowości”. Rozwinąć analizę tygodniową o trendy przed startem, fikcyjne daty startu, wydatki pozostałych kampanii i niepewność uwzględniającą zależności między dniami.

6. **Ważna — przedział 95% można obronić wyłącznie jako warunkowy przedział średniej marży.**

   **Problem.** Obecny przedział nie obejmuje zmienności liczby pozyskanych pacjentów, kosztu pozyskania, atrybucji ani dodatkowości.

   **Dowód.** [a5e_ekonomia.py:125](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a5e_ekonomia.py:125) wykorzystuje wyłącznie błąd standardowy marży. Dla obu nowych kampanii odtworzyłem przedziały wyniku **+2,51 do +4,68 zł według Z1K** oraz **−10,71 do −8,14 zł według Z2**. Żaden nie obejmuje zera, mimo przeciwnego znaku wyników.

   **Poprawka.** Nazwać je „przedziałami warunkowymi przy stałym koszcie pozyskania i wybranej regule źródła”. Do prognozowania przyszłej ekonomii rozważyć wspólne losowanie bloków tygodniowych wydatków, liczby pacjentów i marży. Nadal osobno pokazywać wrażliwość na atrybucję.

7. **Drobna — rozliczanie wydatków według dni płatności jest rozsądnym przybliżeniem w tym przekroju.**

   **Problem.** Na granicy okna część wydatków dotyczy pacjentów kupujących później. Początek kampanii w środku okresu sam w sobie nie unieważnia rachunku, ponieważ wcześniejsze dni mają zerowe wydatki tej kampanii.

   **Dowód.** Według Z1K w oknie płatności mamy **4 893 pacjentów** obu kampanii. Przy wyznaczeniu tego samego okna według pierwszego widocznego wejścia byłoby **4 912**, czyli o **0,39% więcej**. Koszt pozyskania zmieniłby się z **32,68 zł do 32,55 zł**.

   **Poprawka.** Zachować metodę i dopisać tę kontrolę brzegową. Nie przenosić automatycznie jej dokładności na krótkie okresy tuż po starcie kampanii.

8. **Drobna — oznaczenie „niepewne” jest poprawne, ale powinno wskazywać niepewność atrybucji.**

   **Dowód.** Spośród 4 893 pacjentów nowych kampanii według Z1K, **1 383** zapłaciło w sesjach innych źródeł: 575 bezpośrednich, 325 bezpłatnego wyszukiwania Google, 299 wyszukiwania marki i 184 remarketingu Meta. Pozostaje dokładnie **3 510 pacjentów według Z2**.

   Zmiana znaku jest więc własnością reguły przypisywania pacjentów i kosztów. Nie znalazłem tu błędu kodu. Zgodnie z raportem część kampanii Google Ads i Meta zmienia znak. Google Ads na specjalistów pozostaje ujemne w obu regułach, a remarketing zmienia znak w przeciwnym kierunku.

   **Poprawka.** Używać określenia „wynik zależny od reguły atrybucji”. Dodać, że dodatni wynik w obu regułach również nie dowodzi opłacalności dodatkowego budżetu.

Poniżej porównanie liczb z punktu 1. W każdej komórce podaję **raport / moje przeliczenie**. Koszt pozyskania, marża i wynik dotyczą jednego pacjenta. Okno marży obejmuje dni 0–90, a kohorty okres 1.10.2025–2.07.2026.

| Grupa i reguła | Nowi pacjenci | Wydatki, zł | Koszt pozyskania, zł | Marża, zł | Wynik, zł |
|---|---:|---:|---:|---:|---:|
| Obie nowe kampanie, Z1K | 4 893 / 4 893 | 159 897 / 159 897 | 32,7 / 32,7 | 36,3 / 36,3 | +3,6 / +3,6 |
| Obie nowe kampanie, Z2 | 3 510 / 3 510 | 159 897 / 159 897 | 45,6 / 45,6 | 36,1 / 36,1 | −9,4 / −9,4 |
| Pozostałe kampanie płatne, Z1K | 7 076 / 7 076 | 312 427 / 312 427 | 44,2 / 44,2 | 64,2 / 64,2 | +20,0 / +20,0 |
| TikTok, Z1K | 1 265 / 1 265 | 46 220 / 46 220 | 36,5 / 36,5 | 31,9 / 31,9 | −4,6 / −4,6 |
| TikTok, Z2 | 921 / 921 | 46 220 / 46 220 | 50,2 / 50,2 | 32,4 / 32,4 | −17,8 / −17,8 |

Pozostałe liczby dotyczą całego okresu 2, czyli 1.10.2025–30.09.2026. Zwroty liczone są na wizytach, nie na unikalnych pacjentach.

| Miara | Raport | Moje przeliczenie |
|---|---:|---:|
| Afiliacja według Z1K | 617 pacjentów; 15 425 zł | 617 pacjentów; 15 425 zł |
| Afiliacja według Z2 | 405 pacjentów; 10 125 zł | 405 pacjentów; 10 125 zł |
| Afiliacja według kodu RANKING10 | 295 pacjentów; 7 375 zł | 295 pacjentów; 7 375 zł |
| Zwroty po odbytych wizytach L4, nowe kampanie Z1K | 1 024 / 5 895; 17,4% | 1 024 / 5 895; 17,4% |
| Zwroty po odbytych wizytach L4, pozostali pacjenci | 270 / 5 080; 5,3% | 270 / 5 080; 5,3% |