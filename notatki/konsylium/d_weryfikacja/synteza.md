# Konsylium — końcowa weryfikacja całego rozwiązania: wynik (2026-10-20)

Runda na briefie `brief.md` (zlecenie Kuby „konsylium z Fable”). Brief zawierał treść zadania, README, pełne teksty 9 zakładek (`analiza/wyniki/b_teksty_strony.md`, commit `06ba9b8`), założenia, znaleziska, decyzje i zestawienia z raportów. Dwaj członkowie zespołu dostali dostęp do repozytorium i przeliczyli liczby z bazy, tylko do odczytu.

## Puenta

**Błędu krytycznego nie ma. Odpowiedź „to nie jest wzrost w rozumieniu Telemedi” i wszystkie główne liczby się potwierdziły.** Przed wysłaniem trzeba:
- poprawić kilka błędów i sprzeczności, które czytelnik zobaczy na stronie;
- złagodzić kilka zdań, które mówią więcej, niż pokazują dane;
- dopisać jedną brakującą warstwę: krótkie streszczenie decyzji i podziały demograficzne w kohortach.

## Co się potwierdziło

Przeliczone niezależnie z bazy i z załączników, bez rozbieżności:
- nowi pacjenci 16 231 → 24 687 (+52,1%), bez nowych kampanii +7,3% albo +20,1%;
- zamówienia +55,7%, przychód z konsultacji po zwrotach +44,8%, mostek od dashboardu (604 duplikaty, 553 i 1 518 zamówień testowych);
- powrót w 30, 60, 90 i 180 dniach, 23,9% → 17,4% w 90 dniach, 3 076 → 3 289 powracających osób;
- marża na pacjenta w 90 dniach 66,6 → 58,3 zł;
- marża biznesu 828 085 → 1 048 069 zł, III kwartał −6,8% przy wydatkach ×2,08, lipiec lepszy niż rok wcześniej;
- TelemediGO 1 759 → 2 468, opłaty wobec zniżek −27 388 zł;
- Safari na iOS: 628–695 utraconych pierwszych zamówień, 1 158–1 281 rocznie, wartości 74,8–82,8 i 86,0–95,2 tys. zł;
- próg decyzji Meta 85,4% jako rachunek, cennik specjalistów (73 630 i 70 780 zł), przeliczenia na pełny rok ×1,56 i ×1,10;
- definicje: nowy pacjent, powrót, przychód po zwrotach, koszt lekarza także za wizyty zwrócone, dwie reguły źródła, porównanie na tych samych dniach kalendarzowych;
- jakość danych: duplikaty, konta testowe, czas polski, 65 882 − 604 − 2 071 = 63 207 zamówień.

## Lista poprawek od najważniejszej

Oznaczenia: **[strona]** — zmienia sesja narzędzia; **[notatki]** — sesja prowadząca (notatki, README, raporty). Liczby oznaczone „do potwierdzenia” pochodzą z przeliczeń członków zespołu i przed wpisaniem policzymy je naszym kodem.

### Warunek wysyłki (to nie błąd, ale bez tego zadanie nie jest spełnione)

0. **Prawdziwy link do narzędzia.** README ma jeszcze adres zastępczy, a zadanie wymaga strony, która „otwiera się z linku”. Wpisać adres, upublicznić repozytorium, włączyć Pages i sprawdzić oba linki w oknie prywatnym i na telefonie. Przy okazji usunąć z bieżącej wersji `CLAUDE.md` adres e-mail osoby rekrutującej, zanim repozytorium stanie się publiczne (historia zostaje, decyzja Kuby). [notatki + krok publikacji]

### Ważne — błędy i sprzeczności, które czytelnik zobaczy

1. **Średnia ocena wyświetla się jako procent** („4,45% z 3 446”, skala 1–5) w „Po zakupie”. Przyczyna: `widoki.js`, funkcja `komorka`, `j = jedn || "%"`. [strona]
2. **Zła etykieta przy sześciu zdarzeniach** (3, 5, 6, 7, 10, 11): napis „Zobacz w jakości danych”, a odnośnik prowadzi do „Kohort” albo „Po zakupie” (`app.js`, linie 502–503). To najważniejsza część zadania. [strona]
3. **Trzy zdania sprzed poprawek po weryfikacji Astrą:**
   - nagłówek „Kohort”: „większość spadku” zamiast „około 46–71%, zależnie od reguły”;
   - karta w „Lejku” i zdarzenie 12: „nie działa” albo „przestaje działać zakładanie konta” zamiast „gwałtownie spada skuteczność”.
   [strona; notatki: `ZNALEZISKA.md`, A5 pozyskanie]
4. **„Opóźnienia rosną tylko u internisty rano” przeczy tabeli pod spodem.** U internisty w południe opóźnień przybyło z 3,0% do 8,9%, w nocy z 1,9% do 5,7%, a sama godzina 12:00 jest jeszcze w problemie. Nowe brzmienie: „najsilniej rano; w południe i w nocy też rosną, z niskiego poziomu”. [strona, notatki]
5. **Ta sama miara „L4 z pozostałych kanałów” ma dwie wartości:** 13,9% (2 797) wobec 14,8% (2 639) w „Czy to wzrost”, a 13,8% (2 969) wobec 14,6% (2 795) w raporcie i w „Kohortach” po ustawieniu filtrów. Użyć drugiej pary, którą da się odtworzyć na stronie. [strona, notatki]
6. **Zmiana powrotu w 180 dniach:** −5,3 w „Czy to wzrost” wobec ▼5,2 w „Kohortach”. Poprawna jest 5,2 (27,47% − 22,24%); 5,3 wynika z odejmowania zaokrągleń. [strona, notatki]
7. **„Wynik biznesu”: przy wyniku po 180 dniach stoi koszt pozyskania z 90 dni** (32,7 zł zamiast 30,3 zł), więc 37,3 − 32,7 nie daje pokazanego +7,0 zł. Osobna kolumna kosztu dla 180 dni. [strona]
8. **Pozycja 6: liczebność przy średnich ocenach** to 469 i 3 446 ocen, a nie 1 550 i 11 007 wizyt. [strona, notatki]
9. **Daty z jutra w raporcie:** nagłówki W4 i P1b w `c_priorytety.txt` mają „2026-10-21”. [notatki]

### Ważne — zdania mocniejsze niż dane

10. **„Przeglądarki wbudowane w aplikacje tracą pacjentów — naprawić na stronie” kłóci się z naszym własnym rachunkiem.** W obrębie tej samej kampanii przeglądarka w aplikacji konwertuje tak samo jak zwykła (Meta na L4 5,99% wobec 5,58%, TikTok 4,80% wobec 4,56%). Niska konwersja to cecha ruchu z reklam, a nie przeglądarki, a pozycja na liście wycenia ją na 0 zł. Nowe brzmienie karty w „Lejku”: „ruch z reklam Meta i TikToka płaci 3–4 razy rzadziej niż wyszukiwarka, niezależnie od przeglądarki”. „Dwie rzeczy do naprawy na stronie” → jedna (Safari na iOS). [strona, notatki: `ZNALEZISKA.md`]
11. **Pozycja 3 (TikTok): „wysoka pewność co do znaku”.** Karta sama podaje po 180 dniach −1,1 zł na pacjenta z przedziałem od −5,3 do +3,0 zł. Nowe brzmienie w przeglądzie: „wysoka co do braku korzyści; znak po 180 dniach niepewny”. Propozycja odwracalnej pauzy zostaje. [strona, notatki]
12. **„Spadła poranna przepustowość” to odczytanie, nie pomiar.** Do dopisania obserwacja z bazy (do potwierdzenia): w okresie 2 opóźnienie jest prawie takie samo o każdej godzinie poranka (6:00 — 45,4%, 8:00 — 47,0%, 10:00 — 40,4% wizyt spóźnionych ponad 15 minut). Nie narasta więc w ciągu poranka. To bardziej pasuje do stałej przyczyny (późniejszy start, inna kolejka, system zapisów) niż do kolejki przerastającej przepustowość. Zawęża to diagnozę w pozycji 6. [strona, notatki]
13. **Spadek marży w III kwartale nie jest rozłożony.** Rozłożony (do potwierdzenia naszym kodem):
    - pacjenci nowych kampanii zostawili w kwartale 89,0 tys. zł marży przy 87,9 tys. zł wydatków, czyli wyszli na zero;
    - reszta biznesu: 206,6 tys. zł po wydatkach wobec 222,8 tys. zł rok wcześniej. Z tej różnicy około 11,2 tys. zł to niższe opłaty TelemediGO wobec września 2025, a skala awarii Safari mieści się w pozostałej luce.
    Do tego jedno zdanie, że wcześniejsze kwartały okresu 1 nie miały jeszcze bazy powracających, więc ich wzrost rok do roku (+71%, +43%) jest zawyżony startem od zera. Miarodajny jest III kwartał. Przy Safari pokazać, z czego bierze się 14–21 tys. zł, i nie zestawiać marży rocznika z marżą zaksięgowaną w kwartale bez tego zastrzeżenia. [strona, notatki]
14. **Progi i przeliczenia przy kampaniach:**
    - próg decyzji Meta (85%) jest liczony sprzed naprawy zwrotów; po naprawie (wariant A) wynosi około 70%. Podać oba;
    - mnożnik „na pełny rok” liczy średnią z okresu rozruchu kampanii; w tempie ostatnich 6 miesięcy kwoty są o około 13–15% wyższe (do potwierdzenia). Znak żadnej decyzji się nie zmienia, ale trzeba to dopisać;
    - wyceny są osobnymi scenariuszami względem historycznej bazy, a nie liczone „po kolei” po wcześniejszych pozycjach; nazwać to wprost.
    [strona, notatki]
15. **Pozycja 6 pokazuje tylko szeroki zakres (0–65 tys. zł).** Podać wariant bazowy: około 12 tys. zł w wariancie wąskim, do 65 tys. zł w szerokim, koszt obsady nieznany. [strona, notatki]
16. **Pozostałe uogólnienia do zawężenia:**
    - „W jednej grupie spadku nie wykazaliśmy” — u pediatry (22,3% → 26,3%) i psychiatry (22,5% → 24,6%) powrót rośnie, a nie spada;
    - „odsetek kupujących TelemediGO nie rośnie” — przy kolejnych zamówieniach rośnie (9,27% → 9,86%);
    - „rachunkowo prawie cały spadek konwersji to zmiana ruchu” — zależy od podziału (według strony wejścia albo typu pacjenta wychodzi odwrotnie); jedno zdanie, dlaczego właściwy jest podział według przeglądarki i kampanii;
    - założenie 22: 96,6–97,0% zgodności to pierwsze wejście przed nadpisaniem kodem kampanii.
    [strona, notatki]

### Ważne — pominięcia

17. **Krótka pierwsza warstwa dla czytającego pierwszy raz:** jedna karta na górze „Czy to wzrost” (odpowiedź, pięć liczb, trzy decyzje na poniedziałek, jedna kwota). Bez niej przekaz jest gęsty: zdania mają po 3–6 liczb i zastrzeżenie. [strona]
18. **Podziały demograficzne w kohortach (wiek, płeć, województwo, wielkość miejscowości) nie są użyte nigdzie,** choć są w danych. Z przeliczeń zespołu (do potwierdzenia):
    - pacjenci nowych kampanii mają średnio 27,6 roku wobec 38,3;
    - wiek nie tłumaczy braku powrotów (w każdej grupie wieku L4 z nowych kampanii wraca 3,5–4,8% wobec 13,4–15,0%) ani spadku w starych kampaniach (−1 do −2 punktów w każdej grupie wieku);
    - udział nowych kampanii jest podobny w województwach (26–31%), co wspiera test w parach województw;
    - jeden trop regionalny do sprawdzenia: województwo dolnośląskie.
    Propozycja: filtr wieku i województwa w „Kohortach” albo co najmniej zdanie i założenie „sprawdziliśmy, że wiek nie zmienia wniosku”. [strona, notatki]
19. **Rozdzielczość dzienna kohort powinna być widoczna od razu.** Domyślnie widać macierz tygodniową i wygładzenie 7-dniowe, choć wykres schodzi do dnia. Do tego zastrzeżenie przy krzywej powrotu: każdy punkt ma innych pacjentów (punkt w dniu 270 to 5 137 osób), więc wyższe wartości późnych dni nie są nadrabianiem. [strona]
20. **Konta bez zakupu (do potwierdzenia):** 11 482 z 52 400 kont (21,9%) nie ma żadnego zamówienia, a newsletter ani SMS do nich nie trafiają, choć 58,1% ma zgodę marketingową. Zdanie w „Lejku” i nowa niewiadoma z testem (sekwencja do kont bez zakupu, z grupą kontrolną), bez wyceny. [strona, notatki]
21. **Test Meta (pozycja 9) do domknięcia:**
    - moc i najmniejszy wykrywalny efekt;
    - reguła na wynik nierozstrzygający;
    - pary województw;
    - ryzyko, że wspólna obsada lekarzy przeniesie efekt na województwa kontrolne;
    - koszt testu także dla 4 tygodni.
    [strona, notatki]
22. **Zdarzenie bez rozliczenia:** spadek konwersji kampanii Google Ads na hasło „Telemedi” od 22.05.2026 (21,2% → 17,8%, około 40 zamówień mniej na 30 dni) jest w surowych wynikach, a nie ma go na osi ani w niewiadomych. [strona, notatki]

### Drobne

- README:
  - „Prawie jedna trzecia (29%)” — dopisać, że według przyjętej reguły (według sesji płatności 21%);
  - zdanie „nowi pacjenci się nie zmieniają” po oczyszczeniu — w rzeczywistości +51,9% → +52,1%;
  - wskazać też `b2_eksport_c.py`.
- Zdarzenie 10: start TikToka to 9.02.2026, a nie 10.02. Zdarzenie 8: „w 2026” to okres niezdefiniowany na stronie.
- Safari: dwie pary liczb dla tego samego zjawiska (66,2% → 45,1% w oknach 60-dniowych, 66,1% → 45,6% w pozycji 1). Nazwać okno w obu miejscach.
- Płatności w lejku a zamówienia różnią się o 1 na granicy okresów (sesja liczy się do dnia rozpoczęcia, zamówienie do dnia płatności); przychód okresu 1: 2 230 266 albo 2 230 267 zł (zaokrąglenie). Jedno zdanie w „Jak liczymy”.
- Założenie 3: kierunek przesunięcia czasu UTC wobec polskiego opisany odwrotnie.
- Raport kohort, sekcja 3, miesiąc 12 w okresie 2: `NaN` zamiast 0.
- Kampania `crm_go_upsell`: 326 dni w raporcie wobec 388 dni kalendarzowych — wyjaśnić.
- Odnośniki „Pokaż w lejku” zmieniają filtry, ale nie przewijają do tabeli.
- `robots.txt` pod podścieżką nic nie daje; blokadę indeksowania i tak zapewnia `noindex`.

## Rozwidlenie decyzji

1. **Miejsce testu Meta na liście.** Część zespołu widzi go wyżej (4.–5. miejsce), bo to największa stawka na liście (od −31 do +180 tys. zł), a test kosztuje najwyżej około 2 tys. zł. Twoja decyzja z przeglądu stawia przed nim poranną obsadę, bo to dźwignia na retencję z tanim pierwszym krokiem. **Rekomendacja:** zostawić kolejność. Do karty dopisać, że test Meta rusza w drugim tygodniu, równolegle z diagnozą poranka, bo oba testy da się zrobić w tych samych województwach.
2. **Ile z pominięć robimy przed wysyłką** (termin: jutro).
   - **Rekomendacja na dziś:** punkty 1–16 (poprawki tekstów i dwa błędy wyświetlania, kilka godzin), karta streszczenia (17), zdanie i założenie o demografii zamiast pełnego filtra (18), zastrzeżenie przy krzywej (19).
   - **Jeśli starczy czasu:** filtr wieku i województwa, konta bez zakupu (20).
   - **Do niewiadomych zamiast do narzędzia:** szczegóły testu Meta (21) i zdarzenie z Google Ads na markę (22).

## Perspektywa zlecającego

- **Decyzja:** wszyscy, którzy odpowiedzieli, zaprosiliby kandydata dalej albo przyjęli rozwiązanie. Część pod warunkiem poprawek przed wysyłką.
- **Najmocniejsze strony:**
  - rzetelność danych: dokładne odtworzenie dashboardu, duplikaty i testy złapane dwoma niezależnymi podpisami;
  - jednoznaczna odpowiedź z nazwaną niepewnością, dwie reguły źródła i opis odróżniony od przyczyny;
  - zdarzenia znalezione w danych z datami i połączone z pieniędzmi;
  - priorytety w złotych z drogą „naprawić albo wyłączyć”;
  - niewiadome z testem przy każdej pozycji;
  - sprawdzalny ślad pracy.
- **Najsłabsze strony:**
  - przekaz przeciążony liczbami i zastrzeżeniami, bez krótkiej warstwy decyzji;
  - narzędzie bardziej przypomina raport w zakładkach niż codzienny pulpit: nie ma widoku „wczoraj i ostatnie 7 dni” z alarmami;
  - plan testów mniej dopracowany niż analiza;
  - drobne niespójności mimo deklarowanej kontroli liczb skryptem.
- **Pytania, które warto przygotować na rozmowę:**
  - co robimy z Meta na L4 w pierwszym tygodniu, skoro według jednej reguły wyłączenie zyskuje zawsze;
  - jak skrócić to do decyzji dla zarządu;
  - czy narzędzie jest pulpitem codziennej pracy, czy prezentacją wyników.

## Pewność

- **Wysoka**, że liczby i główna odpowiedź są poprawne: przeliczone niezależnie z bazy przez dwóch członków i z załączników przez pozostałych.
- **Wysoka**, że poprawki 1–11 są potrzebne: błędy i sprzeczności widoczne na stronie.
- **Średnia** co do wagi pominięć 17–22: to kwestia oczekiwań zlecającego.

Konsylium: 8 z 10 członków odpowiedziało (Gemini i GLM zużyły cały limit odpowiedzi na rozumowanie, zastępstwo też odpadło; jedna odpowiedź urywa się na samym końcu), koszt 2,17 USD (około 8,70 zł). Kto co mówił — na życzenie.
