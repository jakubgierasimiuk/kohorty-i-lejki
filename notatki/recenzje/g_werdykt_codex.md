1. **Liczby są zgodne. Werdykt „Nie” jest uzasadniony przy przyjętej definicji wzrostu, ale część jego uzasadnienia mówi więcej, niż pokazują dane.**

Obliczenia wykonałem własnym kodem na bazie otwartej przez `read_only=True`. Z `definicje.py` wykorzystałem definicje kohort i źródeł. Marżę policzyłem niezależnie z zamówień, zwrotów, kosztów lekarzy i opłat TelemediGO. Nie zmieniałem plików.

**a) Udział kampanii w przyroście pacjentów — zgodny:**

- Nowi pacjenci: **16 231 → 24 687**, czyli przyrost o **8 456 osób**.
- Według pierwszego wejścia: **7 268 / 8 456 = 85,9508%**, po zaokrągleniu **86,0% — zgodna**.
- Według sesji z płatnością: **5 187 / 8 456 = 61,3411%**, czyli **61,3% — zgodna**.

To udział pacjentów **przypisanych** kampaniom w przyroście. Nie jest to zmierzony wpływ reklam.

**b) Wynik po 180 dniach — wszystkie wartości zgodne.**

Sumowałem marżę pacjenta od dnia pierwszego zakupu do dnia 180 włącznie. Następnie odejmowałem wydatki właściwych kampanii z okresu 1.10–3.04 podzielone przez liczbę nowych pacjentów.

- Według pierwszego wejścia: nowe kampanie **6,9806 zł, 2 352 pacjentów**; pozostałe płatne **29,6582 zł, 5 130 pacjentów**; rok wcześniej **31,7610 zł, 4 717 pacjentów**. Zatem **7,0 / 29,7 / 31,8 zł — zgodne**, liczebności również.
- Według sesji z płatnością: **−5,1838 / 27,5231 / 29,9911 zł**, czyli **−5,2 / 27,5 / 30,0 zł — zgodne**.

**c) Wyniki miesięczne — wszystkie zgodne.**

Koszt pozyskania to miesięczne wydatki obu kampanii podzielone przez przypisanych pacjentów. Młodszym pacjentom uzupełniłem marżę z najdłuższego pełnego okna średnim przyrostem do 180 dni, zmierzonym na dojrzałych kohortach tej samej grupy.

Kwoty poniżej są w złotych na pacjenta. Pierwsze trzy kolumny liczb dotyczą pierwszego wejścia.

| Miesiąc | Koszt pozyskania | Marża 180 dni | Wynik | Wynik według sesji z płatnością | Ocena wszystkich wartości |
|---|---:|---:|---:|---:|---|
| XI 2025 | 27,3 | 34,3 | +7,0 | +0,4 | zgodne |
| XII 2025 | 27,7 | 37,4 | +9,6 | −8,7 | zgodne |
| I 2026 | 30,1 | 40,4 | +10,3 | −0,3 | zgodne |
| II 2026 | 29,6 | 39,7 | +10,1 | −1,4 | zgodne |
| III 2026 | 31,7 | 35,5 | +3,8 | −7,9 | zgodne |
| IV 2026* | 36,0 | 35,0 | −1,0 | −15,9 | zgodne |
| V 2026* | 33,1 | 36,1 | +3,0 | −11,6 | zgodne |
| VI 2026* | 35,9 | 35,6 | −0,3 | −12,9 | zgodne |
| VII 2026* | 37,3 | 37,0 | −0,3 | −14,5 | zgodne |
| VIII 2026* | 36,4 | 36,5 | +0,1 | −14,0 | zgodne |
| IX 2026* | 34,8 | 36,1 | +1,3 | −15,5 | zgodne |

\* Częściowo lub całkowicie przybliżona marża.

Wyniki kwartalne liczyłem z łącznej marży i wydatków, z uwzględnieniem liczebności pacjentów:

- II kwartał 2026: **+0,676 zł → +0,7 zł — zgodna**.
- III kwartał 2026: **+0,385 zł → +0,4 zł — zgodna**.
- Według sesji z płatnością od kwietnia: **od −11,647 do −15,887 zł**, czyli wskazany zakres **od −11,6 do −15,9 zł — zgodny**.

**d) Rozbicie marży — wszystkie wartości zgodne.**

Przypisałem zdarzenia pieniężne do roku zakupu i roku pozyskania pacjenta. Wydatki kampanii oraz prowizje odjąłem od wyniku pacjentów pozyskanych w danym roku.

- Łączna marża: **828 085,25 → 1 048 069,34 zł — zgodna**. Przyrost wynosi **219 984,09 zł, czyli 26,6%**.
- Pacjenci pierwszego roku, zakupy w drugim roku: **194 434,50 zł**, czyli **88,3857% przyrostu — zgodna**.
- Pacjenci pozyskani w danym roku po kampaniach i prowizji: **828 085,25 → 853 634,84 zł**, czyli **+3,0854% — zgodna**.
- Na nowego pacjenta: **51,0187 → 34,5783 zł**, czyli **51,02 → 34,58 zł — zgodna**.

2. **Metoda nie podważa spadku retencji. Ogranicza jednak interpretację rentowności i przyczyn wzrostu marży.**

- **Przybliżenie młodszych kohort:** poprawnie odtwarza zadeklarowaną metodę. Zakłada jednak niezmienny dalszy przebieg marży mimo zmian kampanii i struktury pacjentów. Dopłaty według pierwszego wejścia wynoszą tylko **0,35–2,87 zł na pacjenta**, ale wynik bliski zeru jest wrażliwy nawet na małe odchylenia. Bezpieczny wniosek: „szacunkowo blisko zera”.
- **Łączenie wydatków po dniu kalendarzowym:** rozsądne uproszczenie, ale opóźnienie zakupu przesuwa pacjentów między miesiącami. W pomocniczym przeliczeniu mianownika według dnia pierwszego wejścia wrześniowy koszt wyniósł **35,95 zamiast 34,76 zł na pacjenta**. Nie jest to alternatywny pełny rachunek, ale pokazuje skalę wrażliwości wyniku bliskiego zeru.
- **Porównanie roczników:** obie strony mają takie same granice kalendarzowe, lecz **inny rozkład czasu obserwacji**. Średnio od pierwszego zakupu do końca własnego roku było **191,0 dni wcześniej i 177,8 dni później**. Spadku z 51 do 35 zł nie można w całości przypisać pogorszeniu ekonomii pacjenta. Do tego służy porównanie w stałym oknie 180 dni.
- **Start od zera:** 88,4% jest poprawnym rozbiciem księgowym. Pierwszy rok nie miał analogicznego składnika marży od wcześniejszej bazy. Ten udział sam w sobie nie dowodzi słabości wzrostu ani poprawy retencji.

Niezależnie potwierdziłem powrót w 90 dni: **3 076 / 12 867 = 23,9%** wcześniej oraz **3 289 / 18 924 = 17,4%** później. To wystarcza do „Nie” przy wymaganiu jednocześnie większej liczby pacjentów i lepszej retencji.

3. **Ocena brzmienia:**

- **Cały główny werdykt — za mocny.** „Dały” sugeruje wpływ przyczynowy. „Prawie nic” jest oceną bez ustalonego progu. Wyniki 7 zł i „od wiosny zero” dotyczą różnych kohort. Przede wszystkim akapit nie podaje najważniejszego powodu „Nie”: spadku retencji. Propozycja całego akapitu:

  > Nie według przyjętej definicji: nowych pacjentów jest o 52% więcej, ale w ciągu 90 dni wraca 17% wobec 24% rok wcześniej. Marża po uwzględnionych kosztach wzrosła o 27%. W rozbiciu księgowym 88% jej przyrostu przypada na zakupy pacjentów pozyskanych rok wcześniej. Dwóm nowym kampaniom na L4 przypisujemy 86% przyrostu pacjentów. Na ich wczesnych kohortach zostaje po pozyskaniu 7 zł w 180 dni wobec 30 zł w pozostałych kampaniach płatnych. Dla kohort od kwietnia szacowany wynik jest bliski zeru według pierwszego wejścia, a ujemny według sesji z płatnością.

- **„Od wiosny wychodzimy na zero” — w porządku jako przybliżenie**, pod warunkiem wskazania kampanii, reguły i szacunku. Lepiej: „Dla pacjentów tych kampanii pozyskanych od kwietnia szacujemy wynik bliski zeru według pierwszego wejścia”.
- **„Marża (…) wzrosła (…) prawie wyłącznie dzięki pacjentom z pierwszego roku” — za mocne przyczynowo.** Lepiej: „W rozbiciu księgowym zakupy pacjentów z pierwszego roku stanowią 88% przyrostu marży”.
- **„88% (…) to kolejne zakupy (…), a nie lepszy wynik na nowych pacjentach” — pierwsza część w porządku, końcówka za mocna.** Wynik nowych roczników obejmuje liczbę pacjentów, koszty i czas obserwacji. Lepiej: „Pozostałe 12% przyrostu to wzrost łącznego wyniku pacjentów pozyskanych w danym roku, po kampaniach i prowizji”.
- **„Wzrost (…) zależy od dwóch kampanii, a nie od szerszego popytu” — za mocne.** Źródło pozyskania nie rozstrzyga o popycie ani dodatkowości reklamy. Lepiej: „86% przyrostu pacjentów przypisujemy dwóm kampaniom; poza nimi liczba nowych pacjentów wzrosła o 7%”.
- **„Nowe kampanie kupują liczbę pacjentów (…) koszt pozyskania zjada całą marżę” — za mocne.** Nie zmierzono dodatkowości, a wynik nie jest wszędzie zerowy. Lepiej: „Przypisani tym kampaniom pacjenci dają znacznie niższy wynik po pozyskaniu. Dla kohort od kwietnia szacujemy wynik bliski zeru według pierwszego wejścia”.
- **„Sam przyrost liczby pacjentów prawie nie podniósł zysku” — za mocne.** Nie wyodrębniono wpływu samej liczby pacjentów. Lepiej: „Łączny wynik pacjentów pozyskanych w danym roku wzrósł o 3%, przy wzroście ich liczby o 52%”.
- **„Marża po kosztach kampanii już nie rośnie (…) była na poziomie roku wcześniej” — za mocne.** Faktycznie spadła o **6,8%**; wzrost o około **1%** jest wariantem po szacowanej korekcie. Lepiej: „W III kwartale 2026 marża po kampaniach i prowizji spadła o 6,8% rok do roku. Po korekcie o szacowaną nadwyżkę startu TelemediGO byłaby wyższa o około 1%”.

4. **Czytelnik zrozumie rozbicie +27%, ale może nadal błędnie odczytać powód „Nie”.**

Obecny początek sugeruje, że wzrost marży został unieważniony przez słabą ekonomikę reklam. Tymczasem odpowiedź wynika z przyjętej definicji: liczba pacjentów wzrosła, retencja spadła. To powinno być pierwszym zdaniem.

Trzeba też wyraźniej rozdzielić **wynik w 180 dni** od **wyniku do końca roku pozyskania**. Określenie „marża po wszystkich kosztach” warto zastąpić przez „marża po kosztach lekarzy, kampanii i prowizji”. Słowo „zysk” sugeruje szerszy rachunek kosztów.

Dodatkowy błąd językowy: „tracą na każdym pacjencie” oznacza stratę na każdej osobie. Obliczenia pokazują **średnią stratę na pacjenta**.

| Zgłoszenie | Waga | Propozycja |
|---|---|---|
| Główny werdykt pomija bezpośredni powód „Nie” | drobne | Zacząć od wzrostu liczby pacjentów i spadku retencji |
| „Dały”, „zależy”, „kupują” sugerują zmierzony wpływ reklam | za mocne | Pisać „przypisujemy kampaniom” |
| „Nie od szerszego popytu” | za mocne | Usunąć; dane nie rozstrzygają o popycie |
| „Sam przyrost liczby (…) podniósł zysk” | za mocne | Opisać zmianę łącznego wyniku roczników |
| Roczniki mają różny czas obserwacji | drobne | Dopisać ograniczenie przy porównaniu 51 → 35 zł |
| „Od wiosny zero”, „cała marża” | za mocne | „Szacowany wynik bliski zeru według pierwszego wejścia” |
| „Już nie rośnie” miesza wynik rzeczywisty z korektą | za mocne | Oddzielić spadek o 6,8% od wariantu po korekcie |
| „Tracą na każdym pacjencie” | błąd | „Przynoszą średnią stratę na pacjenta” |
| „Zysk”, „po wszystkich kosztach” | za mocne | Nazwać marżę i uwzględnione koszty |