# Kimi (Moonshot) — moonshotai/kimi-k3

# Ocena i ranking działań

## Kryterium

Stosuję: **wartość oczekiwana (środek scenariuszy × prawdopodobieństwo, że efekt jest realny) ÷ czas wdrożenia**, z premią dla działań, które usuwają ryzyko błędnych decyzji w przyszłości. Przy remisach wygrywa pewność, nie maksymalny scenariusz.

## Ranking

**1. E — Safari/iPhone (75–95 tys. zł/rok, wdrożenie dni)**
Najpewniejsza pozycja na liście. Sygnał jest bardzo czysty: jedna przeglądarka, ostra data graniczna (17.03.2026), spadek 66%→46% w *każdym* kanale jednocześnie, logowanie działa — to praktycznie wyklucza zmianę ruchu i wskazuje na regresję techniczną (data zbiega się pewnie z wdrożeniem lub aktualizacją iOS). Kwoty są najwyższe spośród pozycji o wysokiej pewności. Jedno zastrzeżenie do wyceny: założenie „utracony pierwszy zakup = utracony pacjent" zawyża wartość, bo część tych osób wróciłaby później innym urządzeniem. Realnie oceniłbym na 50–75 tys. zł — i tak lider.

**2. K — naprawa raportowania (0–37,95 tys. zł bezpośrednio, 1–2 tygodnie)**
Stawiam drugie mimo skromnej wyceny, bo to warunek wiarygodności wszystkich pozostałych pozycji: zarząd widzi +61% zamówień, gdy realnie jest +56%, a przychód jest liczony przed zwrotami — przy kampaniach o wysokim poziomie zwrotów (D) to systematycznie zawyża ich wynik. Dodatkowo: 2 071 zamówień testowych z wizytami trwającymi 1 minutę zaniża średnie oceny, czas wizyty i prawdopodobnie wskaźniki opóźnień — może to zniekształcać pozycję G. Bezpośrednia wycena 37,95 tys. zł zakłada, że lekarze są opłacani za wizyty testowe — do sprawdzenia w 1 dzień przez księgowość, zanim ktokolwiek uzna to za oszczędność.

**3. D — zwroty po wizytach L4 (12,7–57,1 tys. zł, 1–2 tygodnie)**
Stawiam przed decyzjami o wyłączeniu kampanii B i F, z jednego powodu: **nie znamy przyczyny zwrotu**. Jeśli zwroty wynikają z tego, że reklama obiecuje coś, czego produkt nie daje (np. sugeruje „L4 online", a lekarz odmawia), to TikTok/Meta wcale nie są złymi kanałami — zły jest komunikat, a wyłączenie kampanii polegałoby na karaniu kanału za wadę komunikatu, którą przeniesiemy do następnego kanału. Ponieważ nie wiadomo też, ilu pacjentów kampanii przyszłoby bez niej, a „naprawa" D ma nakładający się efekt z „wyłączeniem" B, **najpierw naprawiać, potem wyłączać** — jeśli po naprawie kampania nadal jest ujemna. Wyjątek od tej reguły niżej, przy C.

**4. F — test geo dla Meta (decyzja warta −27,8 do +163,3 tys. zł)**
Sama kampania nie „daje" marży — daje ją test. Meta to największa z kampanii L4 i jedyna, gdzie znak wyniku zależy od reguły przypisania. Rozstrzygnięcie, ilu pacjentów jest dodatkowych, odpowiada na główne „czego nie wiemy" z briefu i dotyczy też interpretacji B. Test geograficzny 4–6 tygodni jest dobrze zaprojektowany; zastrzeżenie: województwa różnią się strukturą, więc potrzebna losowa alokacja i kontrola sezonowości (4–6 tygodni zimą vs latem da inne wyniki — mamy tylko jedną zimę i jedno lato danych). Wartość poznawcza: wysoka, koszt: utrata części wolumenu na czas testu.

**5. B — TikTok na L4**
Ujemny w obu regułach i obu horyzontach — to mocniejszy sygnał niż Meta. Ale: najlepszy wariant naprawy daje +3,0 tys. zł, czyli okolice zera, więc nawet po naprawie kampania ledwie się spina. Decyzja: wdrożyć D na tej kampanii najpierw (tanio, 1–2 tygodnie), i jeśli wynik nie wyjdzie stabilnie powyżej zera — wyłączyć. Uwaga na wycenę „do +82,5 tys. zł, jeśli żaden pacjent nie był dodatkowy" — to nie jest wycena wyłączenia, tylko ilustracja, że kampania mogła kanibalizować darmowy ruch; nikt nie wie, ile z tego jest prawdy, więc tego scenariusza nie wolno pokazywać zarządowi jako „zysk z wyłączenia".

**6. C — Google Ads na specjalistów**
Tu wybieram **wyłączenie bez próby naprawy** — i tu łamię własną regułę z punktu 3. Powody: (a) ujemny we wszystkich czterech konfiguracjach reguła×horyzont, (b) problem jest strukturalny, nie komunikacyjny — koszt pozyskania 57,6–80,9 zł przy marży 32–37 zł oznacza, że do rentowności trzeba obniżyć CAC o 40–60%, co w aukcji Google na frazach medycznych jest mało realne w perspektywie miesięcy, (c) kwota na szali to 19–32 tys. zł/rok — za mało, żeby poświęcać 4–8 tygodni pomiaru naprawy o niskim prawdopodobieństwie. Naprawia się kampanie, których problem jest naprawialny (komunikat, strona, zwroty); nie naprawia się kampanii, których problem to cena aukcji.

**7. G — opóźnienia poranne (0–65 tys. zł, koszt obsady nieznany)**
Ważne, bo to może być przyczyna systemowego spadku powrotów z 23,9% do 17,4% — a to jest największy problem biznesowy w danych. Ale pozycja jest niedoprecyzowana: „przy tym samym ruchu więcej opóźnień, więc spadła przepustowość" — alternatywne wyjaśnienia to wydłużenie wizyt (też realny problem) albo mniej lekarzy w grafiku, a bez danych o grafikach nie wiadomo, które. Koszt naprawy (dodatkowa obsada) może zjeść całą marżę. Kolejność działań: najpierw dostać grafiki i sprawdzić długość wizyt (dni), potem wycenić. Do tego: sprawdzić, czy 1-minutowe wizyty testowe z K nie zawyżają/zaniżają tych statystyk.

**8. A — program zniżkowy u specjalistów (14,7–31,4 tys. zł, pełny efekt po 12 mies.)**
Wycena jest poprawna rachunkowo (87,2 zł < 100 zł kosztu to jasne), ale ma słabe założenie behawioralne: scenariusz „znikają tylko wizyty ze stratą" (+18,9 tys.) zakłada, że pacjenci pogodzą się ze zmianą warunków bez reakcji. Program zniżkowy to produkt retencyjny (J), więc pogorszenie warunków może obniżyć odnawialność i powroty — efekt drugiego rzędu, którego wycena nie uwzględnia. Dodatkowo pełny efekt po 12 miesiącach oznacza, że w horyzoncie roku pozyskamy ułamek kwoty. Robić, ale jako decyzję produktową po analizie J, nie jako szybką oszczędność.

**9. J — test programu zniżkowego**
To nie działanie marżowe, tylko badawcze — i słusznie. Ale stawiam nisko w kolejności wykonania, bo: test 90 dni + analiza oznacza decyzję za ~4 miesiące, a koszt badania (do 12,2 tys. zł zniżek + koszt utraconych opłat, jeśli test okaże się pozytywny dla darmowego dostępu) rośnie wraz z rozmiarem próby. Zastrzeżenie do faktu „przewaga członków zostaje po wygaśnięciu" — to silna wskazówka, że program **selekcjonuje** lojalnych pacjentów, zamiast ich tworzyć (samoselekcja: program kupują ci, którzy i tak planują wracać). Przy 5% odnawialności program prawdopodobnie nie jest motorem retencji. Test potwierdzi, ale nie traktowałbym go jako priorytetu sprzedażowego.

**10. I — strata kliknięcie→sesja (0–52 tys. zł, 1–2 dni sprawdzenia)**
Stosunek 0,72–0,82 vs 0,92 w Google jest niestety często wyjaśniany różnicą definicji kliknięcia między platformami (Meta i TikTok liczą kliknięcia inaczej niż Google liczy kliknięcia prowadzące do sesji) — stąd scenariusz 0 zł jest moim scenariuszem bazowym. Ale sprawdzenie w panelach to 1–2 dni, więc **zrobić od razu jako zadanie diagnostyczne**, nie jako projekt. Jeśli okaże się, że to porzucenia przy ładowaniu — skacze wysoko w rankingu (52 tys. zł przy koszcie optymalizacji strony).

**11. H — sesje zalogowanych (0–40 tys. zł)**
22 tys. sesji bez jednego zakupu przy każdym zakupie powracającym z krokiem logowania — fakt, że „kilka faktów wskazuje" na wizyty typu „sprawdzam konto", czyni scenariusz 0 zł bardziej prawdopodobnym. Test ręczny w 1 dzień: ktoś z zespołu loguje się i przechodzi ścieżkę zakupu. Zrobić natychmiast jako test, ale nie budować na tym planu. Jeśli test pokaże zepsutą ścieżkę — awansuje do top 3.

## Odpowiedź na pytanie: naprawiać czy wyłączać?

Reguła: **naprawiać, gdy diagnoza wskazuje na naprawialną przyczynę w naszej kontroli (komunikat, strona, obsługa zwrotów) i gdy kanał ma fundament w postaci wolumenu; wyłączać, gdy problem to ekonomia aukcji albo gdy nawet najlepszy wariant naprawy daje wynik około zera.** Stąd: D przed decyzją o B; C wyłączyć; F rozstrzygnąć testem, bo tam problemem jest nieznajomość, nie wynik.

## Brakujące działania

1. **Program retencji pierwszych 90 dni** — spadek powrotu 23,9%→17,4% przy wzroście nowych pacjentów o 52% to największa strata wartości w całym biznesie (przywrócenie dawnego poziomu przy obecnej bazie nowych pacjentów byłoby warte orientacyjnie kilkaset tysięcy zł rocznie — nie policzę dokładnie bez rozkładu wartości wizyt, ale to rząd wielkości więcej niż jakikolwiek kandydat). Nikt nie wnioskuje o działanie: sekwencja kontaktu po pierwszej wizycie, przypomnienia, follow-up lekarza. To brak numer jeden.
2. **Diagnoza, skąd bierze się pogorszenie jakości kohort** — nowi pacjenci 2025/26 wracają gorzej i dają mniejszą marżę. Czy to tylko kampanie L4 (29% nowych), czy pozostałe kanały też pogorszyły kohorty? Jeśli tylko L4, problem się rozwiąże przez B/D/F; jeśli szerzej — mamy systemowy problem z jakością pozyskania, którego żaden kandydat nie adresuje.
3. **Zatrzymanie łączonego wzrostu wydatków przy spadającej efektywności** — wydatki 2,08× r/r w III kw. 2026 przy marży −6,8% r/r. Potrzebna zasada budżetowa (np. próg marży na pacjenta w 90 dniach na poziomie kampanii), nie tylko decyzje o pojedynczych kampaniach.
4. **Decyzja o kampaniach L4 jako produkcie** — pacjenci z L4: 4% powrotu, 36 zł marży. Nawet po naprawie zwrotów to może być produkt strukturalnie nierentowny w modelu subskrypcyjnym marży. Ktoś powinien odpowiedzieć, czy L4 ma być produktem pozyskującym (wtedy akceptujemy niską marżę i inwestujemy w konwersję na kolejne wizyty), czy nie.
5. **Analiza, czy wzrost wydatków w IV kw. 2025 (+71% marży r/r przy 1,30× wydatków) pokazuje działający kanał do skalowania** — lista kandydatów jest cała o gaszeniu pożarów; brakuje pozycji „skalować to, co zadziałało jesienią 2025".

## Czego nie wiem / zastrzeżenia

- Nie wiem, jaka jest pojemność zespołu — ranking zakłada wykonanie równoległe pozycji tanich (K, I, H) z testami (F).
- Kwot B, D i F nie da się sumować — to różne scenariusze na tej samej populacji.
- Nie potrafię rozstrzygnąć, która reguła przypisania jest bliższa prawdy — reguła 1 zawyża wynik kampanii z kodami, reguła 2 przypisuje kampanii pacjentów, których mogła nie pozyskać; test geo (F) jest jedyną drogą.
- Nie wiem, czy spadek w Safari na pewno jest błędem po stronie firmy (możliwe, że zmiana iOS) — ale to nie zmienia decyzji: diagnoza kosztuje 1–2 dni.
