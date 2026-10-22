**Liczby z punktów 1–9 są zgodne. Poprawiłbym kilka zdań, głównie opis trendu kwartalnego, interpretację testu Mety i przedstawienie scenariusza TikToka jako pewnego wyniku.** Niczego nie zmieniałem.

Punkty 1–2 przeliczyłem własnym kodem, bez uruchamiania `e_poprawki.py`. Bazę otworzyłem z `read_only=True`.

| Nr | Nasza wartość | Twoja wartość | Zgodne/różnica/nie sprawdzono | Uwaga |
|---|---|---|---|---|
| 1 | IV–IX 2026: 146 402 sesje, 12 315 płatności, 8,41%; rok wcześniej: 65 262, 7 257, 11,12% | Dokładnie te same liczebności; 8,41177% i 11,11979% | **Zgodne** | Potwierdzam zakresy miesięczne 8,11–8,87% i 10,76–11,50%, III kwartały 8,31% i 11,12% oraz całe okresy 9,31% i 11,21%. |
| 2 | 1 044 zwroty; L4 1 024 z 5 895 wizyt; pozostałe cele 10/10/0 | 1 044; L4 1 024/5 895, e-recepta 10/420, konsultacja 10/783, skierowanie 0/35 | **Zgodne** | Własne przypisanie pacjentów według pierwszego wejścia z rozstrzygającym kodem odtwarza wszystkie liczby. |
| 3 | TikTok: −6 118 / −27 825 / −7 658 / −29 365 zł; Meta: +44 331 / −18 990 / +46 368 / −17 729 zł | Te same osiem kwot | **Zgodne** | Raport potwierdza wariant B; kwoty dotyczą dni działania kampanii, a 90 i 180 dni oznaczają horyzont marży pacjenta. |
| 4 | Dziś 85,4%/84,5%; kreacja 78,7%/77,9%; zasady zwrotów 70,0%/69,4% | Te same sześć progów | **Zgodne** | Skrót 85% → 79% → 70% odpowiada horyzontowi 90 dni. |
| 5 | 15,7%; 29,7%; 42,6%; następnie 47,3–52,7%; wcześniej 4,7–6,9% | Te same wartości po zaokrągleniu | **Zgodne** | Własne zapytanie potwierdza serię pacjentów spoza nowych kampanii według miesiąca terminu. |
| 6 | 66,1% → 45,6%, po zmianie 4 678 sesji; okna 60 dni: 66,2% → 45,1%, 1 763/1 553 sesje | 66,126% → 45,575%; 66,194% → 45,138%; liczebności identyczne | **Zgodne** | Skrót 66% → 46% jest właściwy dla dłuższych okien, ale dla okien 60 dni byłoby 66% → 45%. |
| 7 | −12,2 / −5,1 / −4,4 punktu procentowego | −12,20 / −5,11 / −4,44 punktu procentowego | **Zgodne** | „Około 4–12 punktów procentowych” poprawnie streszcza porównanie w tych samych kampaniach. |
| 8 | Internista poza blokiem: 2,7%/14 898 wobec 2,8%/9 563; inni rano: 3,0%/2 757 wobec 2,8%/1 949 | 2,6715% wobec 2,7711%; 3,0468% wobec 2,7707%; liczebności identyczne | **Zgodne** | „Około 3% w obu latach” jest poprawnym przybliżeniem. |
| 9 | Wymienione zaokrąglenia i „ponad co piąte konto” | Te same wartości docelowe | **Zgodne** | Szczególnie 41% jest prawidłowe, bo wartość źródłowa wynosi 41,4536%; 41,5% to już wcześniejsze zaokrąglenie. |

**Ocena zdań a–h**

- **a — zgodne po doprecyzowaniu okresu.** Proponuję: „Od kwietnia do września 2026 płatnością kończyło się około 8% sesji osób, które jeszcze nie kupowały. W tych samych miesiącach rok wcześniej było to około 11%”.

- **b — zasadniczo zgodne, ale „zaczęła spadać” jest zbyt kategoryczne.** Już w grudniu 2025 było 10,39% wobec 11,14% rok wcześniej. Lepiej: „Od lutego 2026 różnica względem roku wcześniejszego wyraźnie się powiększa, a od kwietnia pogłębia”. Nowe kampanie stanowią od kwietnia 42,1–47,1% sesji, więc „prawie połowa” jest akceptowalne. Konwersja 5,49% wobec 11,42% oznacza około **52% niższą konwersję**, więc drugie zdanie jest zgodne. Zbieżność ze startem TikToka nie dowodzi przyczynowości.

- **c — próg zgodny, opis pomiaru wymaga uściślenia.** Sam ubytek pacjentów w województwach bez reklamy nie wystarcza. Proponuję: „Wyłączamy kampanię, jeśli oszacowany w teście ubytek wszystkich nowych pacjentów względem sytuacji bez wyłączenia reklamy jest mniejszy niż około 85% liczby pacjentów przypisywanych kampanii w tych województwach i tym samym czasie”. Dopisałbym: „Próg dotyczy marży w 90 dniach; w scenariuszu nowej kreacji wynosi około 79%, a zmiany zasad zwrotów około 70%”.

- **d — liczby zgodne, pewność za duża.** Początek powinien brzmieć: „W scenariuszu, w którym nowa kreacja zniechęca osoby, które dostałyby zwrot…”. Zakończenie: „…kampania nadal wykazuje stratę według obu reguł przypisania”. Warto dopisać, że kwoty dotyczą **234 dni działania**, aby nie pomylić ich z wynikiem rocznym.

- **e — mylące.** Zdanie sugeruje porównanie kolejnych kwartałów, podczas gdy tabela pokazuje tempo **rok do roku**. Poprawnie: „W kolejnych kwartałach roczne tempo wzrostu wydatków na kampanie rośnie, a roczne tempo wzrostu marży przed ich kosztem maleje”. Wydatki rosną rok do roku o 29,6%, 66,4%, 104,0% i 107,7%; marża przed kampaniami o 55,2%, 49,7%, 38,4% i 25,2%.

- **f — zasadniczo zgodne z tabelą, lecz „bez wyceny” jest nieprecyzyjne.** Pozycja 11 ma wycenioną górną granicę, a pozycja 12 koszt. Lepiej: „Na końcu dwie pozycje bez oszacowanego efektu finansowego: pozycja 11 ma tylko górną granicę możliwej korzyści, a pozycja 12 tylko koszt testu”. Meta ma największą stawkę, ale pozycja 7 podaje wartość za punkt procentowy poprawy, więc kwoty nie są w pełni porównywalne.

- **g — zgodne po złagodzeniu języka.** „Tyle samo” zastąpiłbym przez „niemal tyle samo”. Całość: „Wzrost opóźnień skupia się w bloku 5:00–13:59, najmocniej między 6:00 a 11:59. Poza blokiem odsetek wynosi 2,7% wobec 2,8% rok wcześniej”. Godzinę 13:00 można zaliczyć do brzegu bloku, ale wzrost z 2,5% do 5,6% nie jest zerowy.

- **h — zgodne.** Różnica 20 zwrotów to dokładnie 10 e-recept i 10 konsultacji.

**Inne zauważone błędy**

1. [e_teksty.py:894](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/e_teksty.py:894): polecenie podjęcia decyzji także przy niejednoznacznym wyniku testu jest zbyt stanowcze. Niepewny szacunek może znajdować się po dowolnej stronie progu wskutek szumu.

2. [e_teksty.py:815](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/e_teksty.py:815): „od listopada 2025 […] rosną z miesiąca na miesiąc” nie opisuje całej serii. Od lutego występują wahania. Lepiej: „Rosły od listopada do lutego, a następnie utrzymywały się na poziomie około połowy wizyt”.

3. [e_teksty.py:735](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/e_teksty.py:735): wariant A nie doprowadza TikToka najwyżej „do zera”. Według pierwszego wejścia daje **+2 963 zł w horyzoncie 90 dni i +1 423 zł w horyzoncie 180 dni**. Lepiej: „Daje niewielki dodatni wynik według pierwszego wejścia, ale pozostawia stratę według sesji płatności”.

4. [e_teksty_zakladki.py:265](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/e_teksty_zakladki.py:265): „poza tym blokiem” następuje bezpośrednio po godzinach 6:00–10:59, choć porównanie dotyczy obszaru poza **5:00–13:59**. Trzeba wpisać ten zakres wprost.

W `e_poprawki.py` nie znalazłem błędu obliczeniowego dotyczącego punktów 1–2.
