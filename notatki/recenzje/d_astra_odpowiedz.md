**Werdykt: główne liczby potwierdzają odpowiedź „więcej pacjentów, ale gorsza retencja”; przed wysłaniem analizy trzeba jednak poprawić kilka zbyt stanowczych wniosków i niespójności w wycenach priorytetów.**

Nie znalazłem błędu krytycznego zmieniającego tę odpowiedź. Obliczenia wykonałem własnym kodem, bez importowania skryptów projektu, z bazą otwartą przez `read_only=True`. Korzystałem ze schematu `czyste`; dane surowe były potrzebne wyłącznie do odtworzenia dashboardu i sprawdzenia usuniętych wizyt testowych. Niczego nie zapisywałem.

1. **Ważna — dwa zdania o retencji są szersze niż dowody.**

   W [szkicu, wiersz 22](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:22>) stwierdzenie „większość spadku retencji to pacjenci dwóch nowych kampanii” jest prawdziwe tylko według przyjętej reguły źródła. Moje przeliczenie daje udział **70,7% spadku** według tej reguły, ale **46,4% według sesji płatności**. To rozkład opisowy, nie zmierzony wpływ kampanii.

   Z kolei [wiersz 45](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:45>) uogólnia porównanie pacjentów z pierwszym L4 na „tę samą usługę”. Po wyłączeniu nowych kampanii powrót pacjentów z pierwszą e-receptą spada z **33,44% do 29,92%**, a innych specjalistów z **25,16% do 20,64%**. Podane 14,8% i 13,9% są poprawne dla konkretnej grupy L4.

   **Poprawka:** „Obecność pacjentów nowych kampanii odpowiada opisowo za około 46–71% spadku, zależnie od reguły źródła”. Drugie zdanie ograniczyć do L4: „W tej konkretnej grupie nie wykazaliśmy istotnej zmiany”.

2. **Ważna — metoda Safari jest poprawnym scenariuszem, ale nie uzasadnia pewnego wyniku kwartału „bez awarii”.**

   Niezależnie odtworzyłem [obliczenie z sekcji 5f](<C:/Users/K/Desktop/Zadanie - TM/analiza/a5p_zdarzenia.py:221>):

   - skuteczność kroku konta spada z **2 813 / 4 254 = 66,126%** do **2 132 / 4 678 = 45,575%**;
   - dalsza konwersja wynosi **1 541 / 2 132 = 72,280%**;
   - przemnożenie różnicy przez 4 678 sesji i dalszą konwersję daje **694,877 zamówienia**;
   - po odjęciu równoległego spadku w innych przeglądarkach otrzymuję **628,397 zamówienia**.

   Dodatkowa kontrola liczona osobno dla kampanii daje **624 zamówienia po korekcie**, czyli podobny wynik. Metoda jest rozsądna jako przybliżenie przy przyjętych założeniach. Przedział 628–695 **nie jest jednak przedziałem ufności ani udowodnioną liczbą utraconych pacjentów**.

   Kwota kwartalna w [szkicu, wiersz 26](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:26>) powstaje przez przemnożenie średniej straty z 198 dni przez 92 dni. Tymczasem zastosowanie tej samej metody bezpośrednio do sesji III kwartału daje **258–289 zamówień**, zamiast **292–323**. Rachunek kwartalny pomija też powroty pacjentów, których pierwsze zakupy mogły zostać utracone przed lipcem.

   **Poprawka:** pozostawić 75–83 tys. zł jako scenariusz rocznej wartości odzyskanych pacjentów. Zdanie o kwartale zmienić na: „Szacowana skala problemu Safari jest porównywalna ze spadkiem marży III kwartału, ale nie ustaliliśmy wyniku kwartału bez tego problemu”.

3. **Ważna — „pewna strata”, „zawsze” i przypisanie straty wyłącznie cennikowi przekraczają zakres obliczeń.**

   [Wiersz 237](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:237>) mówi, że każdy tydzień działania TikToka to „pewna strata”. Tymczasem dla dojrzałej próby 180-dniowej według przyjętej reguły wynik wynosi **−1,14 zł na pacjenta**, z warunkowym przedziałem 95% od **−5,30 do +3,02 zł**. Potwierdza to również [raport ekonomii, wiersz 213](<C:/Users/K/Desktop/Zadanie - TM/analiza/wyniki/a5e_ekonomia.txt:213>).

   Wynik prognozy całego rocznika pozostaje ujemny, ale korzyść z wyłączenia zależy od założeń dotyczących dodatkowości, marży utraconych pacjentów i pozostałych kanałów. Sam wzrost marży przez cztery tygodnie po pauzie również nie będzie dowodem jej skuteczności — może wynikać z sezonu lub innych zmian.

   Podobnie [wiersz 243](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:243>) nie dowodzi, że cennik jest jedyną przyczyną straty kampanii na specjalistów. Wynik zależy także od kosztu pozyskania, struktury usług i powrotów.

   **Poprawka:** „W przyjętych scenariuszach wyłączenie poprawia wynik; rekomendujemy odwracalną pauzę”. Cennik nazwać „jednym z głównych ograniczeń marży”. Zmianę po pauzie porównywać z ustalonym punktem odniesienia.

4. **Ważna — podsumowanie rocznych wycen kampanii pomija horyzont 180 dni.**

   [Tabela priorytetów, wiersze 196 i 202](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:196>) podaje przedziały wynikające z 90 dni, choć zasada listy wymaga obu horyzontów.

   | Miejsce | W szkicu | Wynik uwzględniający również 180 dni |
   |---|---|---|
   | TikTok, pozycja 3 | +18,6–48,0 tys. zł rocznie przy 100% dodatkowych pacjentów | Dla 180 dni: **+21,0–50,4 tys. zł**. Łączny zakres obu horyzontów: **+18,6–50,4 tys. zł**. |
   | Meta, pozycja 9 i niewiadoma 1 | Od −30,6 do +179,6 tys. zł rocznie | Dla 180 dni dolny scenariusz wynosi **−32,9 tys. zł**. Łączny zakres: **−32,9 do +179,6 tys. zł**. |

   Podstawą są kwoty z [raportu scenariuszy, wiersze 274–277](<C:/Users/K/Desktop/Zadanie - TM/analiza/wyniki/a5e_scenariusze.txt:274>) oraz mnożniki 365/234 i 365/332.

   **Poprawka:** pokazać oba horyzonty osobno albo wyraźnie podpisać obecne przedziały „90 dni”. To samo doprecyzować przy progu decyzji Meta wynoszącym 85%.

5. **Ważna — 31,4 tys. zł korzyści ze zmiany TelemediGO ponownie nazwano „sufitem”, mimo że raport wyraźnie temu przeczy.**

   W [wierszu 315](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:315>) stoi „sufit 31,4 tys. zł”. Tymczasem [raport TelemediGO, sekcja 3c](<C:/Users/K/Desktop/Zadanie - TM/analiza/wyniki/c_telemedigo.txt:230>) podaje:

   - **31 405 zł**, jeśli wszystkie wizyty zostają po cenie katalogowej;
   - **35 191 zł** w korzystniejszym scenariuszu, w którym poszczególne zamówienia mogą zniknąć albo pozostać.

   Pierwsza kwota jest scenariuszem, nie górną granicą. Oba rachunki pomijają zmianę sprzedaży członkostw. Stwierdzenie o „około połowie” efektu w pierwszym roku również nie ma przedstawionego obliczenia uwzględniającego daty wygasania i wykorzystania członkostw.

   **Poprawka:** zastąpić „sufit” słowem „scenariusz”. Połowę efektu w pierwszym roku oznaczyć jako dodatkowe założenie planistyczne.

6. **Ważna — newsletter i SMS nie są głównym obserwowanym kanałem powrotów, a spadek kontaktów na całą bazę wymaga kontekstu.**

   [Niewiadoma 9, wiersz 357](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:357>) nazywa komunikację z pacjentami głównym kanałem powrotów. Według [raportu, sekcja 5c](<C:/Users/K/Desktop/Zadanie - TM/analiza/wyniki/a5r_po_zakupie.txt:229>) w okresie 2 powrót po takim wejściu dotyczy **3,16% pacjentów**, wobec **18,84% wracających bez niego**, wśród pacjentów spoza nowych kampanii. To około **14% obserwowanych pierwszych powrotów**.

   Co więcej, w porównywalnym oknie pierwszych 90 dni udział pacjentów spoza nowych kampanii z wejściem z newslettera lub SMS-a **rośnie z 17,5% do 17,9%**. Spadek wejść na 1 000 osób w całej narastającej bazie może częściowo odzwierciedlać starzenie się tej bazy.

   **Poprawka:** „Newsletter i SMS są kanałem, którego dodatkowy wpływ warto przetestować”. Przy spadku 56–108 do 24–52 wejść dopisać, że mianownikiem jest cała dotychczasowa baza pacjentów.

7. **Ważna — plan testu TelemediGO ma niespójny czas rekrutacji i nie wykazuje mocy dla głównego wskaźnika finansowego.**

   [Wiersz 334](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:334>) przewiduje 2–6 tygodni na przydzielenie 487–1 823 pacjentów na grupę. Dla większej próby potrzeba 3 646 pacjentów. Przy około 2 057 nowych pacjentach miesięcznie oznacza to **1,77 miesiąca, czyli około 7,7 tygodnia**, zgodnie z [raportem, wiersz 338](<C:/Users/K/Desktop/Zadanie - TM/analiza/wyniki/c_telemedigo.txt:338>).

   Liczebność została wyznaczona dla różnicy odsetków powrotu. W szkicu wskaźnikiem głównym jest jednak marża. Nie przedstawiono obliczenia liczebności potrzebnej do wykrycia określonej zmiany marży.

   **Poprawka:** podać około 2–8 tygodni rekrutacji, następnie 90 dni obserwacji. Przed uruchomieniem ustalić minimalny istotny biznesowo efekt marży i sprawdzić wymaganą próbę.

Pozostałe uwagi mają **wagę drobną**. Nie zmieniają głównego werdyktu, ale warto je usunąć z wersji dla firmy.

| Miejsce | Co jest nie tak i dowód | Propozycja poprawki |
|---|---|---|
| [Safari, w. 209](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:209>) | „Spadek jest w każdym kanale”. W raporcie `a5p_zdarzenia.txt`, sekcja 5b, TikTok rośnie z **33,3% do 38,5%**, przy bardzo małych próbach: 9 i 26 sesji z terminem. Rejestracja również nie przestaje działać całkowicie: po zmianie nadal powstaje 668 kont w 60 dni. | „Skuteczność rejestracji gwałtownie spada w głównych kanałach; TikTok ma zbyt małą próbę do oceny”. |
| [Kampania na specjalistów, w. 245](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:245>) | Szczegółowe kwoty raportu P7 wykorzystują marżę pacjenta zaokrągloną do 0,1 zł. Bez pośredniego zaokrąglania wyniki wynoszą **−23 242 / −31 518 zł po 90 dniach** oraz **−19 387 / −30 170 zł po 180 dniach**. | Zaokrąglać dopiero końcowy wynik. Różnice są niewielkie; pełne porównanie jest w tabeli końcowej. |
| [Cennik, w. 316](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:316>) | **73 630 zł** zakłada dodatkowe 10 zł zapłaty na każdej z 7 363 wizyt. Przy utrzymaniu zniżki TelemediGO 20% na 1 425 takich wizytach podwyżka ceny katalogowej o 10 zł daje **70 780 zł**. | Zostawić 73,6 tys. zł jako granicę, ale podać 70,8 tys. zł przy obecnych zniżkach i niezmienionej liczbie wizyt. |
| [TelemediGO, w. 138](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:138>) | Zmiana kosztu pediatry na 25 zł nie czyni „obu usług” dochodowymi. Psycholog nadal ma cenę katalogową 99 zł i koszt 100 zł; jego łączna marża w okresie 2 wynosi **−1 429,80 zł**. | Napisać, że zmiana założenia poprawia wynik pediatrii. |
| [Zakupy osobne, w. 85](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:85>) wobec raportu | Szkic poprawnie podaje **225 / 461** zakupów osobnych. Zdanie pod tabelą w [raporcie TelemediGO, w. 27](<C:/Users/K/Desktop/Zadanie - TM/analiza/wyniki/c_telemedigo.txt:27>) błędnie podaje **1 984 / 2 929**. Kod dolicza wiersz sumy. | Poprawić raport, pozostawić liczby w szkicu. |
| [Poranna obsada, w. 270](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:270>) | „Jedyna dźwignia na retencję” nie wynika z danych. Sama lista zawiera też komunikację po wizycie i test zniżek. | „Jedna z konkretnych hipotez poprawy retencji, z tanim pierwszym krokiem diagnostycznym”. |
| [Niewiadoma 16, w. 364](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:364>) | Nie jest prawdą, że cała marża po 180 dniach pozostaje nieobserwowalna do 2027 roku. **5 137 pacjentów okresu 2 ma już pełne 270 dni obserwacji**; raport kohort pokazuje również marżę w miesiącach 7–9. | „Nie znamy pełnej długoterminowej marży całego rocznika; starsze kohorty pozwalają już częściowo ją ocenić”. |
| [Niewiadoma 14, w. 362](<C:/Users/K/Desktop/Zadanie - TM/notatki/c_szkic.md:362>) | **51 775 zł** kosztu wizyt testowych dotyczy obu lat, a wycena priorytetu **37 950 zł** dotyczy okresu 2. Brakuje ram czasowych. | Dopisać „łącznie w obu okresach”. |

Do odpowiedzi „czy to wzrost” dopisałbym jeszcze jedno rozróżnienie: **liczba pacjentów wracających w 90 dni wzrosła z 3 076 do 3 289, czyli o 6,9%, mimo spadku odsetka powracających**. Nie zmienia to odpowiedzi według definicji firmy. Zapobiega jednak odczytaniu „gorszej retencji” jako spadku bezwzględnej liczby powracających. Warto również podać wprost, że porównanie 90-dniowe obejmuje pierwsze zakupy do **2 lipca każdego roku**, a nie pełne roczniki.

Poniżej wszystkie liczby wskazane do niezależnego przeliczenia. Pary oznaczają **okres 1 / okres 2**, chyba że opis mówi inaczej. Przy dwóch regułach podaję kolejno **przyjętą regułę źródła / sesję płatności**. Kwoty Safari odtwarzające raport wykorzystują jego zaokrąglone 628 i 695 zamówień; zachowanie pełnej precyzji do końca nie zmienia przedziałów prezentowanych w tysiącach złotych.

| Miara | Wasz wynik | Moje przeliczenie |
|---|---|---|
| Nowi pacjenci | 16 231 / 24 687; +52,1% | **16 231 / 24 687; +52,098%** |
| Nowi bez dwóch kampanii, przyjęta reguła, okres 2 | 17 419; +7,3% | **17 419; +7,319%** |
| Nowi bez dwóch kampanii, sesja płatności, okres 2 | 19 500; +20,1% | **19 500; +20,140%** |
| Powrót w 30 dni | 11,0% z 14 984 / 7,8% z 22 646 | **11,018% z 14 984 / 7,842% z 22 646** |
| Powrót w 60 dni | 19,1% z 13 941 / 13,7% z 20 823 | **19,088% z 13 941 / 13,735% z 20 823** |
| Powrót w 90 dni | 23,9% z 12 867 / 17,4% z 18 924 | **23,906% z 12 867 / 17,380% z 18 924** |
| Powrót w 90 dni bez nowych kampanii, przyjęta reguła, okres 2 | 22,0% z 14 031 | **21,994% z 14 031** |
| Powrót w 90 dni bez nowych kampanii, sesja płatności, okres 2 | 20,4% z 15 414 | **20,410% z 15 414** |
| Marża pacjenta w 90 dni, przed pozyskaniem | 66,6 / 58,3 zł | **66,595 / 58,295 zł** |
| Ta marża bez nowych kampanii, przyjęta reguła, okres 2 | 66,0 zł | **65,975 zł** |
| Ta marża bez nowych kampanii, sesja płatności, okres 2 | 63,3 zł | **63,342 zł** |
| Marża biznesu | 828 085 / 1 048 069 zł | **828 085,25 / 1 048 069,34 zł** |
| Zmiana marży IV kwartału 2025 rok do roku | +71,4% | **+71,385%** |
| Zmiana marży I kwartału 2026 rok do roku | +43,0% | **+42,995%** |
| Zmiana marży II kwartału 2026 rok do roku | +13,0% | **+12,999%** |
| Marża III kwartału 2026 wobec III kwartału 2025 | 207 713 wobec 222 824 zł; −6,8% | **207 712,87 wobec 222 823,66 zł; −6,782%** |
| Iloraz wydatków kwartalnych, kolejno IV 2025–III 2026 | 1,30 / 1,66 / 2,04 / 2,08 | **1,2961 / 1,6636 / 2,0403 / 2,0765** |
| Wzrost zamówień surowych | +60,7% | **25 269 → 40 613; +60,723%** |
| Wzrost zamówień oczyszczonych | +55,7% | **24 716 → 38 491; +55,733%** |
| Wzrost surowego przychodu przed zwrotami | +50,3% | **2 381 880,60 → 3 579 928,60 zł; +50,298%** |
| Wzrost oczyszczonego przychodu po zwrotach | +44,8% | **2 230 266,50 → 3 228 342,40 zł; +44,751%** |
| Safari: utracone pierwsze zamówienia, 17.03–30.09.2026 | 628–695 w 198 dniach | **628,397–694,877 w 198 dniach**, według przyjętej metody |
| Safari: marża pacjenta w 90 dni, okres 2 | 64,6 zł | **64,600 zł; 2 990 pacjentów** |
| Safari: marża pacjenta w 180 dni, okres 2 | 74,3 zł | **74,324 zł; 2 278 pacjentów** |
| Safari: roczna wartość, horyzont 90 dni | 75–83 tys. zł | **74 786–82 765 zł**, przy 628–695 zamówieniach |
| Safari: roczna wartość, horyzont 180 dni | 86–95 tys. zł | **86 043–95 222 zł**, przy 628–695 zamówieniach |
| Safari: wartość w III kwartale 2026 | Około 14–21 tys. zł | **14 141–20 869 zł według uproszczenia raportu**; zastrzeżenia w uwadze 2 |
| Wizyty testowe, okres 2 | 1 518, wszystkie u internisty | **1 518 po deduplikacji; wszystkie u internisty, odbyte i jednominutowe** |
| Koszt tych wizyt przy 25 zł za wizytę | 37 950 zł | **37 950 zł** |
| TikTok: prognoza wyniku w 90 dni, przyjęta reguła | −11 928 zł | **−11 928,22 zł** |
| TikTok: prognoza wyniku w 90 dni, sesja płatności | −30 801 zł | **−30 800,77 zł** |
| TikTok: dni działania i mnożnik roczny | 234 dni; ×1,56 | **234 dni; ×1,559829** |
| TikTok: wynik 90-dniowy przeliczony na pełny rok | −18,6 / −48,0 tys. zł | **−18 605,99 / −48 043,93 zł** |
| Google Ads na specjalistów: wynik 90-dniowy, obie reguły | −23 253 / −31 543 zł | **−23 241,80 / −31 518,04 zł**; różnica przez pośrednie zaokrąglenia |
| Google Ads na specjalistów: wynik 180-dniowy, obie reguły | −19 376 / −30 163 zł | **−19 386,57 / −30 169,52 zł**; różnica przez pośrednie zaokrąglenia |
| Marża odbytej wizyty po cenie katalogowej u wskazanych sześciu specjalistów | 9–19 zł | **9 lub 19 zł**; pediatra −5 zł, psycholog −1 zł |
| Wizyty specjalistyczne z zapłatą, która zostaje, okres 2 | 7 363 | **7 363** |
| Zakupy TelemediGO ogółem | 1 759 / 2 468 | **1 759 / 2 468** |
| TelemediGO przy pierwszym zamówieniu | 905 / 1 089 | **905 / 1 089** |
| TelemediGO przy kolejnym zamówieniu | 629 / 918 | **629 / 918** |
| TelemediGO osobno z newslettera | 225 / 461 | **225 / 461** |
| Efektywna zniżka członkostw z okresu 1 | 104,57 zł na członkostwo | **183 939,20 / 1 759 = 104,5703 zł** |
| Marża wizyt ze zniżką u specjalistów poza internistą i psychiatrą, okres 2 | −14 682 zł | **−14 681,60 zł na 1 512 zamówieniach** |
| TelemediGO przy pierwszym zakupie: różnica powrotu w 90 dni, okres 1 | +10,1 punktu procentowego | **34,292% wobec 24,174%; +10,118 punktu procentowego** |
| TelemediGO przy pierwszym zakupie: różnica powrotu w 90 dni, okres 2 | +14,6 punktu procentowego | **34,660% wobec 20,036%; +14,624 punktu procentowego** |