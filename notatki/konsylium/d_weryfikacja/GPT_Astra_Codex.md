# GPT Astra (Codex) — gpt-6-astra (Codex, wysiłek high)

**Rdzeń analizy się broni. Główna odpowiedź — więcej nowych pacjentów, ale gorsza obserwowana retencja — jest zgodna z załącznikami. Nie wysyłałbym jednak tej wersji bez poprawek.** Najważniejsze dotyczą progu decyzji dla Meta, pewności rekomendacji dotyczącej TikToka oraz zdań, które przedstawiają hipotezę jako ustaloną przyczynę.

Sprawdzałem załączniki, nie bazę, kod ani działanie strony. Poniżej rozróżniam błędy, niejasności i brakujące potwierdzenia. Różnic wynikających wyłącznie z zaokrąglenia nie traktuję jako dowodu błędu rachunkowego.

**1. Lista poprawek od najważniejszej**

1. **Krytyczna przed wysłaniem — nie ma jeszcze wymaganego linku do narzędzia.**
   
   **Miejsce:** B, początek README; A, wymagania dotyczące oddania.
   
   **Problem:** to brak formalny, nie zarzut do analizy. README zawiera adres zastępczy: `https://<organizacja>.github.io/<repozytorium>/`. Z załączników wynika, że publikacja świadomie czeka.
   
   **Dowód:** zadanie wymaga działającej strony dostępnej bez konta i instalacji.
   
   **Poprawka:** przed wysłaniem uzupełnić rzeczywisty adres narzędzia i repozytorium. Sprawdzić je bez zalogowania, w tym ładowanie danych, filtry i odnośniki między zakładkami. Na podstawie tekstowego eksportu nie mogę potwierdzić działania narzędzia.

2. **Ważna — próg decyzji dla Meta przeczy deklarowanej kolejności działań.**
   
   **Miejsce:** C, „Priorytety”, zasady listy, pozycje 5 i 9; „Czego nie wiemy”, pozycja 1.
   
   **Problem:** lista deklaruje wycenę każdej pozycji po wykonaniu wcześniejszych. Tymczasem próg około 85% dla Meta pochodzi z wyniku **przed naprawą zwrotów**, choć naprawa jest pozycją 5.
   
   **Dowód:** przy wydatkach 163,3 tys. zł i wyniku +27,8 tys. zł marża przed reklamą wynosi 191,1 tys. zł. Próg to:
   
   `163,3 / (163,3 + 27,8) = 85,45%`.
   
   Po naprawie zwrotów w wariancie A wynik wynosi +70,1 tys. zł. Próg zmienia się na:
   
   `163,3 / (163,3 + 70,1) = 69,97%`.
   
   W horyzoncie 180 dni analogicznie wychodzi około **69,4% zamiast 84,5%**.
   
   **Poprawka:** podać osobne progi przed zmianą reklamy i po niej. Docelowy próg wyznaczyć z marży zmierzonej przy rzeczywiście wdrożonej wersji kampanii. Nie stosować mechanicznie 85% po wcześniejszej poprawie ekonomii.

3. **Ważna — rekomendacja pauzy TikToka jest rozsądna, ale deklarowana pewność jest za duża.**
   
   **Miejsce:** C, „Priorytety”, pozycja 3.
   
   **Problem:** zdanie „pewny jest tylko brak korzyści” nie wynika z przedstawionego przedziału. Brak wykazanej korzyści nie oznacza wykazanego braku korzyści.
   
   **Dowód:** wynik po 180 dniach wynosi −1,1 zł na pacjenta, ale przedział warunkowy obejmuje **od −5,3 do +3,0 zł**, przy 299 pacjentach. Dodatkowo nie obejmuje niepewności atrybucji ani wartości po 180 dniach.
   
   **Poprawka:** napisać: „Obie reguły dają ujemne oszacowania punktowe. Dane uzasadniają odwracalną pauzę, ale nie dowodzą, że kampania nie może przynosić korzyści”. „Wysoka pewność co do znaku” zastąpić oceną pewności oszacowania, a nie samej zgodności dwóch rachunków.

4. **Ważna — czas i reguła rozstrzygnięcia testu Meta są niedopracowane.**
   
   **Miejsce:** C, „Priorytety”, pozycja 9.
   
   **Problem:** nie pokazano, czy test wojewódzki rozróżni dodatkowość poniżej i powyżej progu. Nie ma wariantu „wynik nierozstrzygający”. Pomiar przez 4–6 tygodni nie daje bezpośrednio pełnej marży nowych pacjentów po 90 lub 180 dniach.
   
   **Dowód:** decyzja ma zależeć od przekroczenia około 85%, ale brakuje minimalnego wykrywanego efektu, zmienności wyników województw i oczekiwanego przedziału wyniku. Przy połowie wydatków koszt 4–6 tygodni, liczony z rocznej utraconej marży 30,6–32,9 tys. zł, wynosi około **1,2–1,9 tys. zł**, a nie jednolicie 1,6–1,8 tys. zł.
   
   **Poprawka:** dodać ocenę wykonalności na danych sprzed testu, regułę dla wyniku nierozstrzygającego i harmonogram dojrzewania marży. Ustalić również, jak test współistnieje ze zmianą kreacji i obsady lekarzy. Wspólna obsada może sprawić, że ograniczenie reklamy w części kraju poprawi obsługę także w regionach kontrolnych.

5. **Ważna — dla testu TelemediGO nie da się sprawdzić liczebności ani kosztu z udostępnionych załączników.**
   
   **Miejsce:** C, „Priorytety”, pozycja 12; E7, brak pełnej sekcji 4.
   
   **Problem:** podano 487–1 823 pacjentów na grupę, koszt 3,3–12,2 tys. zł i ponad cztery lata dla testu oferty płatnej. Brakuje parametrów pozwalających odtworzyć te rachunki. Sam tekst przyznaje, że próba została wyznaczona dla powrotu, choć główną miarą ma być marża.
   
   **Dowód:** nie podano zakładanej zmiany retencji, mocy testu, wariancji marży ani dokładnego momentu przyznania bezpłatnej zniżki.
   
   **Poprawka:** dopisać te założenia. Wyjaśnić, czy zniżka obejmuje pierwszą konsultację, jak traktowani są pacjenci, którzy kupiliby członkostwo za 89 zł, oraz czy koszt obejmuje utracone opłaty. Obecne liczebności oznaczyć jako wstępne, dopóki nie zostaną dobrane do marży.

6. **Ważna — wyceny całej listy nie są konsekwentnie liczone po wcześniejszych działaniach.**
   
   **Miejsce:** C, „Priorytety”, zasady listy oraz pozycje 4, 7, 10 i 11.
   
   **Problem:** poza Meta są dalsze zależności. Wycena komunikacji korzysta z pełnych 24 687 nowych pacjentów. Cennik korzysta z historycznych 7 363 wizyt. Wycena brakujących sesji nadal obejmuje TikToka, mimo wcześniejszego wstrzymania kampanii.
   
   **Dowód:** pozycja 11 sama dopowiada „po wstrzymaniu TikToka mniej”, lecz pozostawia 52 tys. zł w przeglądzie.
   
   **Poprawka:** najprościej zmienić zasadę na: „To osobne scenariusze względem historycznej bazy; zależności wskazujemy przy pozycjach”. Alternatywą jest rzeczywiste przeliczenie wspólnego scenariusza po kolejnych działaniach. Samo „kwot nie sumujemy” nie usuwa sprzeczności.

7. **Ważna — niższa konwersja przeglądarek w aplikacjach nie dowodzi usterki tych przeglądarek.**
   
   **Miejsce:** C, „Lejek”, fragment „Dwie rzeczy trzeba naprawić na stronie”; D, znaleziska dotyczące pozyskania.
   
   **Problem:** opis miesza obserwację gorszego lejka z diagnozą techniczną.
   
   **Dowód:** D, ekonomia kampanii, mówi, że **w nowych kampaniach** surowa konwersja przeglądarek w aplikacjach nie jest niższa niż zwykłych. C, końcówka priorytetów, wycenia tę poprawę na 0 zł w przyjętym rachunku.
   
   **Poprawka:** rozdzielić: „Safari — silny sygnał problemu konkretnego kroku” oraz „przeglądarki w aplikacjach — niższa konwersja zagregowana, wymagająca diagnozy”. Porównywać je w tej samej kampanii, okresie, urządzeniu i grupie pacjentów. Nie obiecywać naprawy bez wykazania problemu.

8. **Ważna — opis opóźnień zawiera zarówno błąd, jak i zbyt mocny wniosek.**
   
   **Miejsce:** C, „Po zakupie”, punktualność; C, zdarzenie 7; D, wnioski o przepustowości.
   
   **Problem i dowód:**
   
   - „Opóźnienia rosną tylko u internisty rano” przeczy tabeli. W południe rosną z **3,0% do 8,9%**, a w nocy z **1,9% do 5,7%**. Rano wzrost jest zdecydowanie największy.
   - Więcej opóźnień przy podobnej dziennej liczbie wizyt nie dowodzi samo w sobie spadku przepustowości. Nie znamy obsady ani rozkładu wizyt wewnątrz poranka. Ta sama suma dzienna może oznaczać inne spiętrzenie terminów.
   
   **Poprawka:** „Największe pogorszenie dotyczy poranków u internisty. Wzrostu nie wyjaśnia sama dzienna liczba wizyt. Wynik jest zgodny z problemem dostępnej obsady lub organizacji terminów; mechanizmu nie ustaliliśmy”.

9. **Ważna — opis Safari jest miejscami mocniejszy niż dowody i niespójny co do zakresu.**
   
   **Miejsce:** C, „Lejek”, zdarzenie 12, priorytet 1; D, znaleziska.
   
   **Problem:** „przestaje działać zakładanie konta” sugeruje całkowitą awarię. Konta nadal powstają. Zdarzenie mówi o spadku „w każdym kanale”, a priorytet 1 wyłącza TikToka z oceny z powodu małej próby.
   
   **Dowód:** 668 nowych kont po zmianie; skuteczność kroku konta około 45–46%. Priorytet 1: „TikTok ma za małą próbę do oceny”.
   
   **Poprawka:** „Od 17 marca gwałtownie spada skuteczność rejestracji w Safari na iOS”. Zakres: „w głównych kanałach z dostateczną próbą”. Kryterium naprawy oprzeć na konwersji i płatnościach, nie na powrocie do bezwzględnych 1 080 kont w 60 dni — liczba kont zależy także od ruchu.

10. **Ważna — dwa uogólnienia o retencji wymagają zawężenia.**
    
    **Miejsce:** C, „Kohorty”, wprowadzenie; C, „Czy to wzrost”, fragment o pierwszej usłudze; D, podsumowania.
    
    **Problem i dowód:**
    
    - „Większość spadku” dotyczy przyjętej reguły źródła. Według sesji płatności udział nowych kampanii wynosi około **46%**, czyli mniej niż połowę.
    - „W jednej grupie spadku nie wykazaliśmy” pomija pediatrię i psychiatrię. E1 pokazuje odpowiednio **22,3% → 26,3%** oraz **22,5% → 24,6%**. Nie twierdzę, że wzrosty są istotne, ale nie są wykazanymi spadkami.
    
    **Poprawka:** „Nowe kampanie odpowiadają opisowo za 46–71% spadku”. Przy usługach podać pełny obraz, bez sugerowania, że L4 jest jedynym wyjątkiem.

11. **Ważna — fragment o L4 ma inne liczby niż raport i nie ujawnia dodatkowego filtra.**
    
    **Miejsce:** C, „Czy to wzrost”, „W jednej grupie…”; E1, W2, pierwsza usługa `internista_l4`.
    
    **Rozbieżność:**
    
    - C: **14,8% → 13,9%**, liczebności **2 639 → 2 797**.
    - E1: **14,6% → 13,8%**, liczebności **2 795 → 2 969**.
    
    **Ocena:** nie przesądzam błędu obliczeń. Odsyłacz do analizy „L4 z L4” sugeruje dodatkowe ograniczenie grupy, którego tekst nie wyjaśnia.
    
    **Poprawka:** nazwać dokładnie dodatkowy filtr albo użyć liczb z E1 dla wszystkich pacjentów z pierwszą usługą „internista: L4”, po wyłączeniu nowych kampanii.

12. **Ważna — porównanie marży po 90 i 180 dniach łatwo odczytać jako dojrzewanie tych samych pacjentów.**
    
    **Miejsce:** C, „Wynik biznesu”, tabela ekonomii kampanii; C, priorytety 3–4; D, założenie 40.
    
    **Problem:** są to różne roczniki pacjentów i różne koszty pozyskania. Notatki to wyjaśniają, ale tabela nie pokazuje osobnego kosztu dla 180 dni.
    
    **Dowód:** nowe kampanie według przyjętej reguły:
    
    - 90 dni: marża 36,3 zł, koszt pozyskania 32,7 zł, wynik +3,6 zł;
    - 180 dni: marża 37,3 zł, koszt pozyskania **30,3 zł**, wynik +7,0 zł.
    
    Widoczny w tabeli koszt 32,7 zł nie pozwala odtworzyć wyniku po 180 dniach. TikTok ma natomiast marżę 31,9 zł po 90 dniach i 31,2 zł po 180 dniach — także dlatego, że to różne kohorty.
    
    **Poprawka:** pokazać koszt pozyskania dla obu okien i dopisać „różne kohorty”. Jeśli celem jest ocena przyrostu wartości między 90. a 180. dniem, policzyć oba okna na tej samej grupie.

13. **Ważna — roczne scenariusze są rachunkowo poprawne, ale ich podstawa prognostyczna wymaga wyraźniejszego oznaczenia.**
    
    **Miejsce:** C, „Priorytety”, wyceny kampanii; D, założenia 40 i 53.
    
    **Problem:** nakładają się dwa założenia: marża dojrzałych kohort reprezentuje również młodsze kohorty, a tempo z części roku reprezentuje pełny rok. To istotne przy kampaniach, których ruch rósł skokami.
    
    **Dowód:** dla TikToka wynik po 180 dniach pochodzi z 299 pacjentów, podczas gdy w pełnym okresie przypisano mu 2 209 nowych pacjentów.
    
    **Poprawka:** nazywać kwoty „rocznym scenariuszem przy historycznym tempie i marży dojrzałych kohort”. Pokazać wrażliwość na inną marżę i tempo. W pozycji 7 dopisać też, że 95,6 zł wyceniające dodatkowy powrót jest obserwacyjną różnicą marży z **dni 1–180**, choć sam powrót mierzymy do 90. dnia.

14. **Ważna — krzywa powrotu nie przedstawia jednej stałej populacji.**
    
    **Miejsce:** C, „Kohorty”, „Krzywa powrotu według dnia”.
    
    **Problem:** mianownik zmienia się wraz z dniem obserwacji. Konstrukcja jest jawna, ale odbiorca może odczytać ją jako przebieg zachowania tej samej grupy.
    
    **Dowód:** E2: okres 2 ma 22 646 pacjentów dla 30 dni, 18 924 dla 90 dni i 12 591 dla 180 dni.
    
    **Poprawka:** dodać widoczne ostrzeżenie, że różnica między punktami nie jest przyrostem powrotów tej samej populacji. Przydatny byłby dodatkowy wariant ze stałą grupą pacjentów mających pełne wybrane okno. Nie zarzucam obecnej metodzie błędu porównania rok do roku.

15. **Ważna — trzeba sprawdzić, dlaczego pełna kohorta bez zakupów dostaje brak marży zamiast zera.**
    
    **Miejsce:** E2, sekcja 3, miesiąc 12, okres 2.
    
    **Problem:** raport podaje 186 pacjentów z pełnym oknem i 0,000 kolejnych zamówień na pacjenta, ale przychód, koszt i marża mają `NaN`.
    
    **Dowód:** brak aktywności w pełni obserwowanym okresie nie jest tym samym co brak obserwacji.
    
    **Poprawka:** sprawdzić agregację miesięcy bez transakcji. Jeżeli nie było również wpływów z TelemediGO, wynik powinien wynosić 0 zł. Nie mogę z załączników ustalić, czy ten problem dotyczy tylko wydruku, czy innych agregacji.

16. **Ważna — walidacja źródła kodami jest opisana w sposób mogący wyglądać na sprawdzanie reguły nią samą.**
    
    **Miejsce:** D, `ZALOZENIA.md`, punkt 22; `DECYZJE.md`, definicje.
    
    **Problem:** reguła, w której kod rozstrzyga źródło, powinna być zgodna z mapowaniem tego kodu w 100% przypadków objętych regułą. Tymczasem uzasadnienie mówi o 96,6–97,0%.
    
    **Dowód:** opis jednocześnie ustanawia kod rozstrzygającym i używa zgodności z nim jako argumentu za wyborem.
    
    **Poprawka:** wyraźnie napisać, że zgodność 96,6–97,0% dotyczy **pierwszego wejścia przed nadpisaniem źródła kodem**, jeżeli tak faktycznie liczono. Zachować zastrzeżenie, że kody nie stanowią dowodu przyrostowego wpływu reklam.

17. **Ważna — brakuje domknięcia kilku sygnałów dostępnych w samych raportach.**
    
    **Miejsce:** C, „Zdarzenia”, surowe wyniki; E6, ekonomia kampanii; E2, kolejne zamówienia.
    
    **Problem:** nie potrzeba kolejnych rozbudowanych priorytetów, ale czytelnik powinien wiedzieć, czy poniższe sygnały wyjaśniono:
    
    - Google Ads na markę: kandydat zmiany 22.05.2026, konwersja **21,2% → 17,8%**, oszacowanie −39,6 zamówienia na 30 dni.
    - Google Ads na e-receptę: koszt pozyskania **48,8 → 59,8 zł**, czyli +22,5%; wynik po 90 dniach **28,6 → 15,7 zł**, czyli −45,1%, według przyjętej reguły.
    - Kolejne zamówienia na pacjenta w 90 dniach: **0,334 → 0,234**, czyli −29,9%. Narzędzie eksponuje głównie wystąpienie choć jednego powrotu.
    
    **Poprawka:** dodać krótkie rozstrzygnięcie „wyjaśnione przez… / do monitorowania / niewyjaśnione”. Częstotliwość kolejnych zakupów dołączyć jako miarę retencji. Nie uznaję tych sygnałów automatycznie za niezależne zdarzenia.

18. **Ważna — wynik testu darmowego TelemediGO nie wystarczy do decyzji o promocji płatnego programu.**
    
    **Miejsce:** C, priorytet 12, „Ile warta” oraz „Zastrzeżenie”; E7, opłaty wobec zniżek.
    
    **Problem:** zastrzeżenie słusznie mówi, że darmowy dostęp bada zniżkę, ale opis wartości testu nadal sugeruje rozstrzygnięcie, czy promować program za 89 zł.
    
    **Dowód:** ekonomia grup jest różna. W okresie 1 efektywna zniżka na członkostwo wynosi:
    
    - 88,94 zł przy pierwszej konsultacji;
    - 136,36 zł przy kolejnej;
    - 78,56 zł przy osobnym zakupie.
    
    **Poprawka:** opisać test jako pierwszy etap: czy dostęp do zniżek zwiększa marżę. Osobno pozostawić wybór ceny i sposobu sprzedaży. Zastąpić także „opłaca się, gdy dokłada wizyt” przez „opłaca się, gdy dodatkowa marża pokrywa koszt zniżek” — dodatkowa wizyta u części specjalistów może przecież zwiększać stratę.

19. **Drobna — wyjaśnienie wzrostu sprzedaży TelemediGO pomija dodatni efekt odsetka przy kolejnych zamówieniach.**
    
    **Miejsce:** C, „Czy to wzrost”, karta TelemediGO; E7, sekcja 1e.
    
    **Problem:** „Przy kasie przybywa zakupów (…) nie wyższy odsetek kupujących” jest za szerokie.
    
    **Dowód:** przy kolejnych zamówieniach wzrost z 9,27% do 9,86% dodaje **55 zakupów**. Pełne rozbicie wzrostu o 709 zakupów to około:
    
    `705 z większej liczby zamówień − 232 z łącznej zmiany odsetków + 236 zakupów osobnych`.
    
    **Poprawka:** „Wzrost napędza większa liczba zamówień i sprzedaż osobna. Łączny wpływ zmian odsetka kupujących jest ujemny, choć przy kolejnych zamówieniach odsetek nieznacznie wzrósł”.

20. **Drobna — opis udziału newslettera i SMS-ów można odczytać z niewłaściwym mianownikiem.**
    
    **Miejsce:** C, priorytet 7.
    
    **Problem:** „Po wejściu (…) wraca 3,16%, a bez takiego wejścia 18,84%” brzmi jak porównanie skuteczności dwóch grup.
    
    **Dowód:** te wartości sumują się do 22,0% i mają wspólny mianownik 14 031 pacjentów. Udział powrotów poprzedzonych wejściem z wiadomości to `3,16 / 22,0 = 14,4%`.
    
    **Poprawka:** „Spośród wszystkich pacjentów 3,16% wróciło po takim wejściu, a 18,84% bez takiego wejścia”. Nie są to odsetki powrotu wśród klikających i nieklikających.

21. **Drobna — opis przesunięcia dni między UTC a czasem polskim jest błędny.**
    
    **Miejsce:** D, `ZALOZENIA.md`, punkt 3.
    
    **Problem:** chodzi o pierwsze godziny dnia w Polsce, nie wejścia po 22:00 lub 23:00 czasu polskiego.
    
    **Dowód:** przykładowo 22:30 UTC latem to 00:30 następnego dnia w Polsce.
    
    **Poprawka:** „Zdarzenia po 22:00 UTC latem lub 23:00 UTC zimą przypadają już na kolejny dzień w Polsce”. To błąd opisu; załączniki nie wskazują błędu samego przeliczenia.

22. **Drobne — pozostałe rozbieżności i usterki prezentacji do uporządkowania.**

    | Miejsce | Co się nie zgadza lub wymaga dopisku | Proponowana poprawka |
    |---|---|---|
    | C, „Po zakupie”, średnia ocena | Tabela pokazuje **4,45%**, **2,92%** itd., choć skala to 1–5 | Usunąć `%`. To jednoznaczny błąd jednostki |
    | C, priorytet 6, oceny | Podano 1 550 i 11 007 wizyt przy porównaniu średnich ocen; ocen jest odpowiednio **469 i 3 446** | Podać liczbę ocen, ewentualnie obie liczebności z nazwami |
    | C, „Kohorty”, 180 dni | Tabela: spadek **5,2 punktu procentowego**; C „Czy to wzrost” i E2: **5,3** | Ujednolicić wynik na podstawie niezaokrąglonych wartości |
    | C, zdarzenie 10 | Spadek datowany **10.02.2026**, opisany jako występujący „w dniu startu” TikToka; start to **9.02.2026** | „Dzień po starcie kampanii”; nadal jako zbieżność |
    | C, „Czy to wzrost”; D, odtworzenie dashboardu | „Nowi pacjenci się nie zmieniają”, choć **16 251 → 16 231** i **24 689 → 24 687** | „Zaokrąglona dynamika pozostaje około +52%; liczby spadają o konta testowe” |
    | D, przychód; C, „Wynik biznesu”; E1–E2 | Przychód okresu 1: **2 230 267** albo **2 230 266 zł**; kolejne zamówienia okresu 1: **739 284** albo **739 283 zł**. Składniki przychodu okresu 2 w C sumują się do **3 228 343 zł**, suma wynosi **3 228 342 zł** | Najpewniej niezależne zaokrąglenia. Ujednolicić prezentację lub dopisać, że zaokrąglone składniki mogą nie sumować się do sumy |
    | C i E3, lejek, wobec C i E1, zamówienia | Lejek: **24 717 / 38 490**; zamówienia: **24 716 / 38 491** | To pasuje do różnych dni przypisania: rozpoczęcia sesji i płatności. Dopisać wyjaśnienie oraz potwierdzić przesunięcie jednej sesji przez granicę roku |
    | D, opis krzywej; E2, sekcja 2 | D mówi o **72–75%** poziomu okresu 1 od 7. do 90. dnia; E2 ma **71%** w dniach 30 i 45 | Zmienić zakres na około 71–75% |
    | E4, start newslettera | Kolumna `dni`: **326**; od 8.09.2025 do 30.09.2026 są **388 dni kalendarzowych** | Jeżeli chodzi o dni z ruchem, tak nazwać kolumnę. Bez danych nie rozstrzygam, czym jest 326 |
    | E1, nagłówek W4 | „Dopisek kandydata **2026-10-21**” w raporcie z **2026-10-20** | Poprawić datę |
    | B, odtworzenie strony; C, stopka; D, trzecia wersja | README wskazuje `b_eksport.py`, a końcowe treści powstają również przez `b2_eksport_c.py` | Jawnie wymienić oba kroki i ich kolejność |

**2. Co się potwierdziło**

- **Główne dynamiki.** Z podanych liczb:
  - nowi pacjenci: `24 687 / 16 231 − 1 = 52,10%`;
  - zamówienia: `38 491 / 24 716 − 1 = 55,73%`;
  - przychód z konsultacji po zwrotach: `3 228 342 / 2 230 266 − 1 = 44,75%`;
  - marża: `1 048 069 / 828 085 − 1 = 26,57%`.

- **Retencja i liczba powracających nie są ze sobą sprzeczne.**  
  `3 076 / 12 867 = 23,91%`, a `3 289 / 18 924 = 17,38%`. Liczba powracających rośnie o 6,92%, mimo spadku odsetka.

- **Porównywalne granice okien są poprawne.** Przy końcu obserwacji 30.09.2026 pełne okna kończą się na kohortach z 31 sierpnia, 1 sierpnia, 2 lipca i 3 kwietnia dla odpowiednio 30, 60, 90 i 180 dni. Wartości 23,6% i 23,9% dla okresu 1 opisują różne zakresy kohort; nie stanowią błędu, jeśli zakres jest podany.

- **Czyszczenie danych uzgadnia się liczbowo.**  
  `65 882 − 604 − 2 071 = 63 207` zamówień, czyli `24 716 + 38 491`.  
  `459 557 − 2 093 = 457 464` sesje, czyli `434 710 + 22 068 + 686`.  
  Różnica między 1 810 wierszami z TEST-QA a 1 781 unikalnymi zamówieniami wynika z 29 duplikatów.

- **Definicje są zasadniczo obronione i jawne.** Nowy pacjent jako pierwsze opłacone zamówienie odpowiada pytaniu dashboardu. Powrót jako kolejne nieanulowane zamówienie jest dopuszczalnym wyborem, choć trzeba pamiętać, że obejmuje także wizyty nieodebrane i zwrócone po odbyciu. Koszt lekarza za wizyty odbyte i zwrócone jest zgodny z zadaniem. Przyjęcie 100 zł dla pediatry i psychologa odpowiada literalnej regule „pozostali”.

- **Roczne sumy marży odtwarzają się.**  
  Okres 1: `2 230 266 + 156 551 − 1 175 700 − 367 632 − 15 400 = 828 085 zł`.  
  Okres 2: `3 228 342 + 219 652 − 1 734 825 − 649 675 − 15 425 = 1 048 069 zł`.

- **Wniosek o III kwartale jest poprawny.** Marża spada o 6,78%, a wydatki rosną do 2,077-krotności poziomu sprzed roku. Lipiec nadal jest lepszy; słabszy jest kwartał jako całość. Rozbicie zmiany na marżę przed kampaniami, wydatki i prowizję jest spójne z dokładnością zaokrągleń.

- **Rozbicie wpływu bazy z pierwszego roku jest poprawne jako rachunek, nie kontrfaktyczny scenariusz.**  
  Po odjęciu 152 960 zł marży konsultacji wzrost wynosi 8,09%. Po dodatkowym odjęciu 41 474 zł opłat TelemediGO wynosi 3,09%. Zastrzeżenie o braku modelowania zmian zachowania i wydatków jest potrzebne i już obecne.

- **Przeliczenie Safari na pełny rok jest poprawne warunkowo.**  
  `628–695 × 365 / 198 = 1 158–1 281` pacjentów.  
  Przy marży 64,6 zł daje około 74,8–82,8 tys. zł; przy 74,3 zł około 86,0–95,2 tys. zł. Nie jest to przedział ufności ani dowód, że każdy brakujący zakup oznacza utraconego pacjenta.

- **Liczby dotyczące TelemediGO są zasadniczo zgodne.** Sprzedaż rośnie o 709 zakupów, czyli 40,31%. Opłaty: `1 759 × 89 = 156 551 zł` i `2 468 × 89 = 219 652 zł`. Różnica opłat i zniżek dla członkostw okresu 1 wynosi −27 388,20 zł. Odnowienia `62 / 1 140 = 5,44%` dotyczą prawidłowo ograniczonej grupy z pełnym okresem obserwacji.

- **Wyceny prostych scenariuszy są poprawne.**  
  Koszt lekarzy za testy okresu 2: `1 518 × 25 = 37 950 zł`.  
  Jeden punkt procentowy dodatkowych powrotów: `24 687 × 1% × 95,6 = 23 600,77 zł`.  
  Podwyżka o 10 zł: `7 363 × 10 = 73 630 zł`; przy zachowaniu 20% zniżki dla 1 425 wizyt: 70 780 zł.

- **Kierunek strat wizyt ze zniżką u części specjalistów jest poprawny.** Przykładowo `109 × 80% − 100 = −12,80 zł`, a u pediatry `95 × 80% − 100 = −24 zł`. To nie jest jednak samo w sobie pełny wynik członkostwa ani pacjenta.

**Nie potwierdzam niezależnie** parametrów detekcji zdarzeń, kwoty 65,2 tys. zł dla poranków, scenariuszy 36–40/89 tys. zł dla zalogowanych, 52 tys. zł dla brakujących sesji ani liczebności i kosztów testów. Załączniki nie zawierają wszystkich składników tych rachunków. Wcześniejsze recenzje modeli są śladem procesu, a nie zastępstwem tej weryfikacji.

**3. Ocena z perspektywy zlecającego**

| Wymaganie zadania | Ocena na podstawie załączników |
|---|---|
| Kohorty dzienne i znalezienie zdarzeń | **Spełnione merytorycznie.** Są dzienne serie, segmenty, pełne okna i kandydaci zmian. Tygodniowa macierz nie jest naruszeniem wymagania, skoro wykres pozwala zejść do pojedynczego dnia |
| Lejki: gdzie i od kiedy tracimy pacjentów | **Spełnione.** Szczególnie mocny jest sygnał Safari. Słabsza jest interpretacja przeglądarek w aplikacjach jako usterki |
| Działające narzędzie z linku | **Niepotwierdzone i jeszcze niedostarczone w README.** Tekst opisuje narzędzie, ale nie pozwala sprawdzić interakcji |
| Priorytety z wartością, pomiarem i czasem | **Formalnie spełnione.** Wyceny wymagają spójnej bazy, a projekty testów — reguł rozstrzygnięcia i realnego harmonogramu pomiaru |
| Lista niewiadomych i sposobów rozstrzygnięcia | **Mocno spełnione.** Brakuje wyraźniejszego oznaczenia nierozstrzygających testów oraz ograniczeń bieżącego pomiaru przy braku dat zwrotów |
| Repozytorium ze śladem pracy | **Dobrze opisane, ale niezweryfikowane.** Nie oglądałem kodu, historii ani dostępności repozytorium |

**Trzy najmocniejsze strony:**

1. **Dyscyplina analityczna.** Kandydat rozróżnia wzrost skali, retencję, zmianę struktury pacjentów i wynik finansowy. Kontroluje dojrzewanie kohort i sezon porównania.
2. **Przełożenie danych na decyzje.** Safari, zwroty L4 i ekonomia specjalistów prowadzą do konkretnych działań z rachunkiem wartości.
3. **Jawne założenia i niewiadome.** Dwie reguły źródła, osobne potraktowanie remarketingu, zastrzeżenia dotyczące TelemediGO i brak automatycznego przesuwania budżetu są przekonujące.

**Trzy najsłabsze strony:**

1. **Nierówna ostrożność wnioskowania.** Notatki często zawierają właściwe zastrzeżenie, ale nagłówek zamienia je w pewnik.
2. **Plan eksperymentów jest mniej dopracowany niż analiza historyczna.** Brakuje mocy testów, decyzji przy niepewnym wyniku i spójności między interwencjami.
3. **Czytelnik musi sam uzgadniać zakresy liczb.** Dotyczy to zwłaszcza marży po 90 i 180 dniach, dat sesji i płatności oraz podgrup L4. Duża liczba powtórzeń zwiększa ryzyko rozbieżności.

**Moja decyzja: kandydat przechodzi do końcowej rozmowy.** To mocne rozwiązanie pokazujące umiejętności potrzebne do prowadzenia biznesu na kohortach. Nie odrzuciłbym go z powodu wskazanych usterek.

Na rozmowie poprosiłbym jednak o obronę trzech decyzji: dlaczego wstrzymać TikToka mimo przedziału obejmującego zysk, jak zmieni się próg Meta po naprawie zwrotów oraz kiedy test jest zbyt mały, żeby uzasadnić decyzję. Odpowiedzi pokażą, czy kandydat sam kontroluje rozumowanie stojące za narzędziem.
