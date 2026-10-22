**Liczby 1–9 są zgodne. Korekty wymagają głównie interpretacje i zakresy porównań.** Punkty 1–8 przeliczyłem własnym kodem przez `python -I`, na DuckDB otwartej z `read_only=True`. Nie uruchamiałem `e_poprawki.py` i nie zmieniałem plików.

W tabeli zapis „sesje / płatności” oznacza liczby sesji i sesji ze zdarzeniem `payment_succeeded`.

| Nr | Nasza wartość | Twoja wartość | Zgodne/różnica/nie sprawdzono | Uwaga |
|---|---|---|---|---|
| 1 | Okres 1: 144 813 / 16 232; okres 2: 265 264 / 24 686 | Identyczne liczby | **Zgodne** | Łączenie przeglądarek z kontami nie powiela sesji w tych danych. |
| 2 | Według sesji: 11,21% → 11,42%; IV–IX: 11,12% → 11,02% | Okres 1: 144 813 sesji, 11,2089%; okres 2: 170 802, 11,4161%; IV–IX 2025: 65 262, 11,1198%; IV–IX 2026: 79 677, 11,0182% | **Zgodne** | Półroczna zmiana wynosi −0,10 punktu procentowego. |
| 3 | Według pierwszego wejścia: okres 2 159 225 / 17 418; IV–IX 2026 71 441 / 7 328; zmiana −0,86 | Odpowiednio 10,9392% i 10,2574%; IV–IX 2025: 65 262 / 7 257, czyli 11,1198%; zmiana −0,8624 punktu procentowego, przedział [−1,1905; −0,5342] | **Zgodne** | Przedział odtwarza podane przybliżenie normalne. |
| 4 | 11 577 / 2 081, 17,98%; przeciwny przypadek: 0 | 11 577 / 2 081, 17,9753%; 2 081 pacjentów przypisanych nowym kampaniom według pierwszego wejścia, a innym według sesji płatności; przeciwny przypadek: 0 | **Zgodne** | To wartości całego okresu 2. |
| 5 | Safari: IV–IX 8,27% wobec 11,99%; krok konta 45,7% wobec 67,0%; przed awarią 12,07% wobec 12,15% | IV–IX 2026: 14 323 / 1 184, 8,2664%, konto 1 628 / 3 561 = 45,7175%; IV–IX 2025: 12 887 / 1 545, 11,9888%, konto 2 086 / 3 112 = 67,0308%; przed awarią: 12,0674% z 14 477 sesji wobec 12,1534% z 12 803 | **Zgodne** | Filtr obejmuje również iPady. |
| 6 | Pozostałe: 10,76% wobec 10,91%; konto 65,4% wobec 66,4%; zmiana −0,15 | IV–IX 2026: 57 118 / 6 144, 10,7567%, konto 65,4274%; IV–IX 2025: 52 375 / 5 712, 10,9060%, konto 66,4483%; zmiana −0,1493 punktu procentowego, przedział [−0,5178; +0,2193] | **Zgodne** | Przedział obejmuje zero, ale nie dowodzi identycznej konwersji. |
| 7 | Bez nowych kampanii: −0,86 = Safari −0,74 + pozostałe −0,12 + struktura około 0; wszyscy: −2,71 | Bez nowych kampanii: Safari −0,74067, pozostałe −0,11958, struktura +0,03060 −0,03273; wszyscy: struktura −2,06939, Safari −0,54961, pozostałe −0,08903 punktu procentowego | **Zgodne** | Safari stanowi 85,9% spadku poza osobami nowych kampanii; rozkład jest opisowy. |
| 8 | Iloraz 0,690 = 1,030 × 0,682 × 0,982; podane miesiące | Ilorazy: 0,689511 = 1,029557 × 0,682037 × 0,981936; Safari IV: 7,4519% z 2 912 sesji wobec 11,1327%, konto 43,0% wobec 65,1591%; IX: 8,9255% z 2 364 wobec 12,3527%; pozostałe IV: 10,7206% z 11 324 wobec 11,0971%; IX: 10,4712% z 9 359 wobec 11,2983% | **Zgodne** | Zaokrąglenia wszystkich podanych wartości są poprawne. |
| 9 | +29,6%, +66,4%, +104,0%, +107,7%; 113,1, 170,6, 184,4, 181,6 tys. zł | Z raportu: +29,6116%, +66,3580%, +104,0263%, +107,6541%; wydatki 113 089,43; 170 625,40; 184 405,30; 181 554,93 zł | **Zgodne** | `e_merytoryka.json` potwierdza cztery kwartały, a `d_wynik.txt` dodatkowo potwierdza III kwartał 2026. |

Podane przedziały traktują sesje jako niezależne. Powtarzające się sesje tych samych osób ograniczają ich interpretację.

**Zdania a–g**

- **a. Za mocne przyczynowo.** Rozkład średniej nie dowodzi dwóch wyłącznych przyczyn. Proponuję: **„Spadek konwersji nowych osób wiąże się głównie z większym udziałem ruchu nowych kampanii na L4 i pogorszeniem kroku konta w Safari”.**

- **b. Liczby poprawne, „tylko” i „nie zmieniła się” za mocne.** Proponuję: **„Od kwietnia do września 2026, poza osobami nowych kampanii, wyraźny spadek widać w Safari na iPhone’ach i iPadach: płaci 8,27% sesji wobec 11,99% rok wcześniej. Pogorszenie skupia się na kroku konta; raport zdarzeń wskazuje zmianę od 17 marca 2026. W pozostałych przeglądarkach nie wykryto istotnej statystycznie zmiany konwersji”.**

- **c. Zasadniczo uzasadnione, lecz miesza okresy.** Sesje reklam nowych kampanii stanowią od kwietnia około **42–47%** sesji nowych osób. W IV–IX 2026 płaci w nich **5,30%**, wobec **10,26%** poza osobami nowych kampanii. Lepiej użyć tych wartości zamiast rocznych 5,49% i 10,94%. Trzeba też zachować nazwę „sesje z reklam”, ponieważ wszystkie sesje osób nowych kampanii stanowią w tym półroczu **51,2%** ruchu.

- **d. Mechanizm potwierdzony, zakres wymaga doprecyzowania.** Proponuję: **„Według sesji roczna konwersja rośnie z 11,21% do 11,42%. W IV–IX pozostaje zbliżona: 11,02% wobec 11,12% rok wcześniej. W całym okresie 2 ten podział zachowuje dodatkowe 11 577 sesji osób nowych kampanii, z konwersją 17,98%. W samym IV–IX jest to 8 236 sesji z konwersją 17,62%. Ich uwzględnienie podnosi średnią i maskuje spadek widoczny po wyłączeniu wszystkich sesji tych osób”.**

- **e. Uzasadnione opisowo.** Precyzyjniej: **„Spadek konwersji w Safari odpowiada za około 86% spadku średniej poza osobami nowych kampanii na L4 w IV–IX 2026 wobec tych samych miesięcy 2025”.** To udział w rozkładzie, nie zmierzony wpływ awarii.

- **f. Ta sama korekta co w b.** Proponuję: **„Poza osobami nowych kampanii, według pierwszego wejścia, w IV–IX 2026 wyraźny spadek występuje w Safari na iPhone’ach i iPadach: płaci 8,27% sesji wobec 11,99% rok wcześniej. W pozostałych przeglądarkach nie wykryto istotnej statystycznie zmiany”.**

- **g. Reguła jest rozsądnym przybliżeniem dla dostępnych identyfikatorów.** Nie rozpoznaje tej samej niezalogowanej osoby w różnych przeglądarkach. Dodatkowo przypisanie kodem z przyszłego zamówienia zależy od tego, czy osoba ostatecznie kupiła. Nie zmienia to poprawności przeliczenia według przyjętej definicji. **Nie można jednak zagwarantować, że błędy identyfikacji nie zmienią wyników 5–7** — szczególnie udziału przypisanego Safari. Nie ma też dowodu, że faktycznie odwracają wniosek. Dodatkowej kontroli wrażliwości nie ukończyłem.

**Inne zauważone błędy**

1. W [e_teksty.py](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/e_teksty.py:1209) zdanie **„Cały spadek przypada na krok konta”** jest zbyt kategoryczne. Konwersja po kroku konta również maleje, o około 1,8% względnie. Poprawnie: „Pogorszenie skupia się na kroku konta”.
2. Odwołanie źródłowe karty w [e_teksty.py](C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/e_teksty.py:1248) wskazuje wyłącznie punkt 1 raportu `e_poprawki.txt`. Nowe wyliczenia według pierwszego wejścia i rozkład Safari znajdują się w **punkcie 3**; ten punkt należy dopisać również do źródła karty Safari.
