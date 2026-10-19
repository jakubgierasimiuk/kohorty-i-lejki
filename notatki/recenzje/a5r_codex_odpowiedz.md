**Potwierdzam poprawność głównych liczb i rozkładu, ale interpretacja wymaga korekty: wynik opisuje zmianę składu pacjentów, a kontrola przypisania źródła przecenia odporność podziału na nowe i dotychczasowe kampanie.**

Nie znalazłem błędu krytycznego. Wszystkie przeliczenia wykonałem własnym kodem w pamięci, na bazie otwartej z `read_only=True`, bez uruchamiania Waszych skryptów raportowych i bez zapisywania plików.

1. **Ważna — kontrola według sesji płatności myli nowe kampanie z nowymi komórkami.**

   W [notatce, linia 49](</C:/Users/K/Desktop/Zadanie - TM/notatki/a5_retencja.md:49>) kontrolę według sesji płatności opisano jako „−4,3 nowe kampanie, −2,2 zachowanie”. Jednak przy podziale kampania × usługa × zniżka × status nowe komórki mogą powstać również w dotychczasowych kampaniach.

   Moje przeliczenie według sesji płatności daje:

   - **Na poziomie kampanii:** nowe kampanie −3,030 punktu procentowego, struktura +0,041, zachowanie −3,537.
   - **Na poziomie czterech cech:** nowe komórki −4,277 punktu procentowego, zniknięte +0,110, struktura −0,144, zachowanie −2,215.

   Około **1,25 punktu procentowego** różnicy między tymi składnikami „nowości” wynika więc z drobniejszych komórek, a nie z dwóch nowych kampanii. Według sesji płatności do tych kampanii należy 3 510 pacjentów, wobec 4 893 według przyjętej reguły pierwszego wejścia z pierwszeństwem kodu kampanii.

   **Poprawka:** dodać kontrolę według sesji płatności na samym poziomie kampanii. Napisać, że kierunek wyniku jest odporny, ale przypisanie spadku między nowe i dotychczasowe kampanie zależy istotnie od reguły źródła. Przyjętej definicji źródła nie trzeba zmieniać.

2. **Ważna — 4,6 punktu procentowego to poprawny rozkład opisowy, ale nie efekt przyczynowy kampanii.**

   Na poziomie kampanii niezależnie otrzymałem:

   \[
   -6{,}5261 =
   -4{,}6141 + 0 + 0{,}0772 - 1{,}9892
   \quad\text{punktu procentowego}.
   \]

   Składniki oznaczają kolejno nowe kampanie, zniknięte kampanie, strukturę i zachowanie. Liczby potwierdzają [opis w notatce, linie 39–43](</C:/Users/K/Desktop/Zadanie - TM/notatki/a5_retencja.md:39>).

   **−4,6141 punktu procentowego jest różnicą między wynikiem wszystkich pacjentów okresu 2 a wynikiem tego samego okresu po wyłączeniu dwóch kampanii.** Nie wiadomo, gdzie ci pacjenci kupiliby bez tych kampanii ani czy kupiliby w ogóle. Przesunięcie pacjentów między kampaniami może również zmienić skład dotychczasowych kampanii.

   Nie wolno z tego wyciągać wniosku, że wyłączenie kampanii podniosłoby retencję o 4,6 punktu procentowego. Nie można też ocenić ich opłacalności bez kosztu pozyskania i dodatkowej sprzedaży.

   **Poprawka:** użyć sformułowania: „W przyjętym rozkładzie opisowym obecność pacjentów przypisanych do dwóch nowych kampanii odpowiada za 4,61 z 6,53 punktu procentowego różnicy”.

3. **Ważna — wykluczenie sezonowości jest zbyt stanowcze, choć dodatkowa kontrola wzmacnia Wasz wniosek.**

   [Notatka, linia 45](</C:/Users/K/Desktop/Zadanie - TM/notatki/a5_retencja.md:45>) stwierdza, że niski powrót nowych kampanii nie wynika z pory roku. Pierwotne porównanie nie wystarcza do takiego wykluczenia: nowe kampanie działały przez krótsze części okresu, a wspólne granice kalendarzowe nie wyrównują udziałów poszczególnych miesięcy.

   Dodatkowo przeliczyłem pacjentów z pierwszym L4 u internisty **od 9 lutego do 2 lipca 2026 r.**, we wszystkich grupach na tych samych datach:

   - nowa kampania Meta na szybkie L4: **4,09%**, 90 powrotów na 2 200 pacjentów;
   - kampania TikToka: **2,83%**, 30 na 1 060;
   - pozostałe kanały, bez obu kampanii Meta pozyskania i TikToka: **14,44%**, 197 na 1 364.

   Różnica pozostaje duża. Ponadto po wyłączeniu nowych kampanii rozkład według miesiąca daje składnik struktury miesięcy **+0,043 punktu procentowego**, a spadek wewnątrz miesięcy **−1,955 punktu procentowego**. Zmiana udziałów miesięcy nie wyjaśnia więc pozostałego spadku.

   **Poprawka:** zastąpić wykluczenie sezonu zdaniem: „Różnica utrzymuje się dla tej samej usługi i wspólnych dat pozyskania; prosta zmiana struktury miesięcy jej nie wyjaśnia”.

4. **Ważna — „zachowanie” jest resztą po uwzględnieniu obserwowanych cech, a nie rozpoznaną przyczyną.**

   Wynik rzeczywiście utrzymuje się po coraz drobniejszych podziałach: składnik zachowania wynosi **−1,989 punktu procentowego** dla kampanii i **−2,113 punktu procentowego** dla kampanii × usługi × zniżki × statusu.

   Jednak **261 z 409 wspólnych komórek** ma mniej niż 10 pacjentów przynajmniej w jednym okresie. Obejmują one około 7,6% pacjentów wspólnej części każdej próby. Drobny podział jest zatem obciążony szumem. Status pierwszej wizyty może też sam zależeć od kampanii — słusznie zaznaczacie to w [skrypcie, linie 168–169](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_struktura.py:168>).

   Nie wykluczono różnic w potrzebie pacjenta, cechach demograficznych, komunikacji po zakupie czy jakości wizyty niewidocznej w samym statusie. Brak istotnej zmiany L4 w pozostałych kanałach również nie oznacza równoważności: niezależny 95-procentowy przedział różnicy wynosi **od −2,70 do +1,03 punktu procentowego**.

   **Poprawka:** napisać, że „uwzględnione cechy nie wyjaśniają pozostałej różnicy”. Jako główny wynik zachować podział według kampanii lub kampanii i usługi. Drobniejsze podziały traktować jako kontrolę i uzupełnić przedziałami niepewności składników rozkładu.

5. **Drobna — zaokrąglone składniki nie zawsze sumują się dokładnie do zaokrąglonej zmiany.**

   W [funkcji `rozklad()`, linie 97–100](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_struktura.py:97>) każdy składnik jest zaokrąglany osobno. Na przykład dla kampanii pokazane −4,61 + 0,08 −1,99 daje −6,52, podczas gdy pokazana całkowita zmiana wynosi −6,53 punktu procentowego.

   **Poprawka:** dodać adnotację o zaokrągleniach. Warto też sprawdzać sumę przed zaokrągleniem. W moich przeliczeniach tożsamość zachodziła z błędem numerycznym poniżej \(10^{-12}\).

Sam kod głównych obliczeń oceniam pozytywnie:

- **Rozkład jest poprawny.** Wspólne komórki mają udziały normalizowane osobno w obu okresach. Symetryczne składniki struktury i zachowania sumują się do zmiany we wspólnej części. Dodanie różnic między całą próbą a częścią wspólną daje pełną zmianę.
- **Próba jest poprawna.** `proba()`, `granice_por()` i `stopy_por()` stosują pełne okna oraz właściwe granice kalendarzowe. Dla 90 dni są to 2 lipca 2025 r. i 2 lipca 2026 r.
- **Brak powrotu pozostaje w mianowniku.** Konwersja na zwykły typ zmiennoprzecinkowy w [linii 125](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_struktura.py:125>) sprawia, że porównanie `NaN <= okno` daje `False`. W badanej próbie nie znalazłem braków cech używanych w podstawowych podziałach ani utraty pacjentów przez dołączenie sesji.
- **Ekonomia odpowiada definicji.** Przychód uwzględnia zwroty, TelemediGO jest doliczane osobno, a koszt lekarza obejmuje wizyty odbyte i zwrócone. W danych nie ma zdarzeń ekonomicznych przed dniem kohorty, więc brak jawnej dolnej granicy `dni >= 0` nie zmienia tych wyników.

**Koszt pediatry: przyjęcie 100 zł jest rozsądne i zgodne z literalną zasadą zadania.** [Słownik danych, linia 108](</C:/Users/K/Desktop/Zadanie - TM/dane/README.md:108>) wyróżnia tylko internistę i psychiatrę, a pozostałym specjalistom przypisuje 100 zł. Zniżka TelemediGO jest dodatkową przesłanką klasyfikacji, ale sama nie dowodzi wysokości wynagrodzenia lekarza.

Wariant 25 zł daje marżę na pacjenta w 90 dniach:

- **wszyscy:** 71,41 zł wobec 62,02 zł, czyli spadek o 9,39 zł;
- **bez nowych kampanii:** 71,41 zł wobec 70,59 zł, czyli spadek o 0,82 zł.

Kierunek wniosków pozostaje ten sam. Retencja w ogóle nie zależy od tego założenia. Proponuję jedynie oprzeć uzasadnienie 100 zł przede wszystkim na treści zasady kosztowej.

Poniżej porównanie wszystkich wskazanych liczb. Pary oznaczają okres 1 → okres 2; stopy dotyczą powrotu w 90 dniach, a marże obejmują dni 0–90 przed kosztem pozyskania.

| Miara | Wasz wynik | Mój wynik |
|---|---|---|
| Wszyscy pacjenci | 23,91% (12 867) → 17,38% (18 924) | **23,9061%** (3 076 / 12 867) → **17,3800%** (3 289 / 18 924) |
| Nowa kampania Meta na szybkie L4 — `meta_prosp_l4_szybko`, okres 2 | 4,5%; 3 628 pacjentów | **4,4928%**; 163 / **3 628** |
| Kampania TikToka na L4 — `tt_prosp_l4_15min`, okres 2 | 3,2%; 1 265 pacjentów | **3,1621%**; 40 / **1 265** |
| Bez dwóch nowych kampanii | 23,91% → 21,99% (14 031) | **23,9061%** (3 076 / 12 867) → **21,9942%** (3 086 / 14 031) |
| Dotychczasowa kampania Meta „lekarz online” — `meta_prosp_lekarz_online` | 21,2% (786) → 16,2% (835) | **21,2468%** (167 / 786) → **16,1677%** (135 / 835) |
| Pierwsze L4 u internisty, pozostałe kanały | 14,8% (2 639) → 13,9% (2 797) | **14,7783%** (390 / 2 639) → **13,9435%** (390 / 2 797) |
| Marża na pacjenta, wszyscy | 66,6 zł → 58,3 zł | **66,5952 zł → 58,2953 zł** |
| Marża na pacjenta, bez dwóch nowych kampanii | 66,6 zł → 66,0 zł | **66,5952 zł → 65,9749 zł** |