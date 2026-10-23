# Znaleziska — rzeczy podejrzane w danych

Zasada Telemedi: „jeśli coś w danych wygląda podejrzanie, powiedz o tym — to też jest odpowiedź”. Tu trafia każda niespójność, luka, duplikat, wartość nierealna i każdy tekst w danych, który wygląda na skierowany do AI (nie wykonujemy go — tylko opisujemy).

## 2026-10-19 — kontrola bezpieczeństwa paczki

**Wynik: w paczce nie znaleźliśmy tekstu skierowanego do AI ani niczego, co wygląda na ukryte polecenie.**

- Paczka `telemedi-b2c-dane.zip`, SHA-256 `aad606afa8517eb9b773c951a01262a0115cb19632ab7f650f86d3ee89ed12bd`. 18 plików, dokładnie lista z zadania. Program antywirusowy Windows (Microsoft Defender) nie znalazł zagrożeń. Raporty: `bezpieczenstwo/raport_20261019_115329.txt` (bez rozpakowania), `bezpieczenstwo/raport_20261019_115443.txt` (po rozpakowaniu).
- Nagłówki 17 plików CSV zgodne ze słownikiem z zadania. Liczby wierszy zgodne co do wiersza (razem 1 082 369). Żaden wiersz nie ma innej liczby pól niż nagłówek.
- `dane/README.md` (110 linii) przeczytany jako dane: to wyłącznie słownik danych i zasady biznesowe. Nie zwraca się do AI i niczego nie każe robić.
- **Fałszywy alarm skanu:** wszystkie 9 761 oznaczeń „słowa kierowane do AI” to dwie wartości ze słowem „polecenie”: `utm_source = 'polecenie'` (4 741 sesji) i `landing_page = '/polecenie'` (5 020 sesji). To program poleceń — README w sekcji o kosztach marketingu wymienia go wprost („program poleceń: bez kosztu w danych”). Skrypt reaguje na to słowo, bo po polsku może znaczyć „rozkaz”.
- **Do sprawdzenia w analizie (nie bezpieczeństwo):** liczba sesji z wejściem na `/polecenie` (5 020) i liczba sesji ze źródłem `polecenie` (4 741) różnią się o 279. Strona poleceń i oznaczenie źródła nie zawsze idą w parze — ważne przy przypisywaniu źródła pozyskania.
- **Ograniczenie tej kontroli:** skan treści szukał listy znanych słów i wzorców. Nie wyklucza tekstu sformułowanego innymi słowami. Dlatego zrobiliśmy drugą kontrolę od odwrotnej strony (niżej).

### Profil wszystkich kolumn (`bezpieczenstwo/profil_kolumn.py`, raport `bezpieczenstwo/profil_kolumn_20261019_120448.txt`)

**Wynik: w danych nie ma miejsca na ukryte polecenie. Pytanie o prompt injection uważamy za zamknięte.**

- Każda kolumna z określonym formatem (identyfikatory, daty i czasy, liczby, wartości ze słownika — 42 z 53 kolumn) ma zero wartości spoza formatu.
- Kolumny swobodne mają od 2 do 21 unikalnych wartości. Wszystkie wypisane w raporcie i przejrzane: regiony, źródła i kanały wejścia, 14 nazw kampanii, systemy, przeglądarki, 21 stron wejścia, 6 kodów rabatowych. Same zwykłe wartości marketingowe i adresy podstron.
- Najdłuższa komórka w całym zbiorze ma 38 znaków (`/blog/teleporada-jak-sie-przygotowac` i podobne). Nie ma ani jednego znaku spoza zwykłego zestawu (litery, cyfry, polskie znaki, podstawowa interpunkcja).
- Spacje występują tylko między datą a godziną i w nazwie przeglądarki `Samsung Internet`.

### Do analizy — pierwsze podejrzane rzeczy zauważone przy profilu

- **Kod rabatowy `TEST-QA` w 1 810 zamówieniach.** Wygląda na zamówienia testowe zespołu jakości w danych produkcyjnych. Do sprawdzenia: kiedy występują, jakie mają kwoty i statusy, czy trzeba je wyłączyć z przychodu i z kohort. → **Sprawdzone w A2** (niżej): 22 konta testowe, 2 071 zamówień, część bez kodu.
- **Źródło `bing` (3 944 sesje) nie ma kosztów w `marketing_spend.csv`.** Do sprawdzenia, czy to ruch bezpłatny (`organic`), czy brakujący koszt kampanii. → **Wyjaśnione w A2:** Bing ma w sesjach `utm_medium = organic`, czyli bezpłatne wyniki wyszukiwania. Brak kosztu jest zgodny z oznaczeniem.
- **Dwie kampanie mają koszty tylko przez część okresu:** `meta_prosp_l4_szybko` przez 332 dni i `tt_prosp_l4_15min` przez 234 dni, wobec 730 dni pozostałych. To kandydaci na zdarzenia (start kampanii) do odczytania z danych. → **A2:** to starty kampanii, nie luki. Sesje i koszty zaczynają się tego samego dnia (szczegóły niżej).

## 2026-10-19 — jakość danych (punkt A2)

Pełny raport: `analiza/wyniki/a2_jakosc.txt`, kod: `analiza/a2_jakosc.py`. Na razie nic nie jest usunięte ani poprawione. Propozycje czyszczenia czekają na wspólny przegląd.

**W skrócie: dane są czyste poza dwiema dużymi sprawami — duplikatami zamówień w czerwcu 2026 i zamówieniami testowymi. Obie zawyżają drugi rok wobec pierwszego.**

### Duże

1. **Duplikaty zamówień: 604 zamówienia zapisane dwa razy, wszystkie od 10.06.2026 00:07 do 24.06.2026 23:59.**
   - W pliku `orders.csv` jest 65 882 wierszy, a unikalnych zamówień 65 278. Każde zdublowane zamówienie ma dokładnie dwie identyczne kopie w dwóch sąsiednich liniach.
   - W tych 15 dniach zdublowanych jest od 28% do 42% zamówień dziennie. Dzień przed oknem i dzień po nim nie ma ani jednego duplikatu.
   - Udział zdublowanych jest podobny bez względu na metodę płatności, status i zniżkę (od 33% do 39%). To wygląda na błąd eksportu, a nie na prawdziwe podwójne płatności. W analityce każde z tych zamówień ma tylko jeden krok płatności.
   - Wszystkie duplikaty są w drugim roku dashboardu (X 2025 – IX 2026). Dodają mu 604 zamówienia i 51 293 zł zapłat, czyli 45 805 zł po odjęciu zwrotów.
   - W pozostałych tabelach nie ma ani jednego duplikatu, także na stykach plików kwartalnych i półrocznych.

2. **Zamówienia testowe: 22 konta, 2 071 zamówień, z czego 290 bez kodu TEST-QA.**
   - 1 781 zamówień ma kod TEST-QA. Wiersze z tym kodem to 1 810, z czego 29 to duplikaty z punktu 1. Każde jest zapłacone 1 zł zamiast 89 zł i ma status „odbyta”.
   - Te same 22 konta mają jeszcze 290 zamówień bez kodu. Każde jest zapłacone pełne 89 zł, zwrócone w całości i ma status „zwrócona”. Wyglądają na testy procesu zwrotu. Filtr po samym kodzie by ich nie złapał.
   - Wszystkie 2 071 to czat z internistą trwający dokładnie 1 minutę. Taki czas trwania nie występuje u żadnego innego pacjenta (najkrótsza prawdziwa wizyta trwa 3 minuty). Dwa niezależne podpisy (kod na koncie i czas 1 minuty) dają ten sam zbiór.
   - Składane tylko od poniedziałku do piątku, między 9:00 a 17:59. Wszystkie konta to województwo mazowieckie, miasto powyżej 200 tys. mieszkańców, bez zgody marketingowej, roczniki 1986–1997. Wszystkie wchodzą bezpośrednio, z komputera, w przeglądarce Chrome, na stronę `/konto`.
   - Liczba testów rośnie z 35 w czwartym kwartale 2024 do 370–410 na kwartał w 2026. W pierwszym roku dashboardu jest ich 553, w drugim 1 518. Zawyżają więc wzrost zamówień.
   - W analityce mają 2 093 sesje z kompletem kroków lejka (2 071 z zamówieniem i 22 sesje założenia konta). Zawyżają też lejek.
   - Pieniądze: 27 591 zł zapłat i 25 810 zł zwrotów, czyli 1 781 zł przychodu. Według zasady z zadania (25 zł za każdą odbytą wizytę u internisty, także zwróconą) dałoby to 51 775 zł kosztu lekarza. Czy lekarz naprawdę dostał wynagrodzenie za jednominutowy test, z danych nie wiemy.
   - **Przegląd w punkcie D (2026-10-21, `analiza/d_testy.py` → `analiza/wyniki/d_testy.txt`): nic się nie zmienia.** Liczby z A2 odtwarzają się co do sztuki (22 konta, 553 i 1 518 zamówień, 290 bez kodu, 2 093 sesje, 51 775 zł). Reguła jest kompletna: poza 22 kontami nie ma ani jednej wizyty trwającej 1 albo 2 minuty, kodu z „TEST” albo „QA” ani zapłaty 0 zł; konto z największą liczbą zamówień poza testami ma ich 18, a konto testowe średnio 94,1. Wyłączenie nie zabiera prawdziwych danych: wszystkie zamówienia kont testowych to jednominutowy czat z internistą, a 22 przeglądarki testowe nie były używane przez żadne inne konto. Wszystkie sesje testowe to wejścia bezpośrednie, więc nie zawyżały sesji kampanii płatnych. W schemacie `czyste` nie ma żadnego zamówienia, konta, sesji ani zakupu TelemediGO kont testowych.

### Do wspólnej dyskusji

3. **Sesje zalogowane od wejścia nigdy nie kończą się zakupem konsultacji.**
   - Słownik danych mówi, że pacjent zalogowany na wejściu ma `user_id` w sesji, ale nie ma kroku `account_completed`.
   - Takich sesji (bez zakupu samego TelemediGO) jest 22 068. Wszystkie należą do pacjentów, którzy już wcześniej kupowali. Wchodzą głównie na `/konto` oraz z newslettera i SMS-ów.
   - 4 574 z nich wybiera usługę. Tylko 112 wybiera termin, a do płatności nie dochodzi żadna. Wśród sesji niezalogowanych termin wybiera 42% tych, które wybrały usługę.
   - Z drugiej strony każda z 65 278 sesji z zamówieniem ma krok logowania, także każda z 24 338 sesji zakupów powtórnych. Wyjątek ze słownika w sesjach płacących w ogóle nie występuje.
   - Obraz jest taki sam w każdym kwartale, więc to nie jest zdarzenie z konkretnego dnia.
   - Dwa możliwe odczytania: (a) wejścia zalogowane to wizyty „sprawdzam konto”, a do zakupu pacjent i tak przechodzi przez logowanie; (b) ścieżka zakupu dla zalogowanych jest zepsuta albo inaczej mierzona. Ma to znaczenie dla lejka i dla oceny kampanii CRM.

4. **START10 nie jest kodem z okresu startu.** Plan zakładał, że okres rozruchu wyznaczy kod startowy START10. Tymczasem START10 jest używany przez całe dwa lata, na 9,0–9,5% pierwszych zamówień w każdym kwartale do grudnia 2025 i na 6,8–7,8% od stycznia 2026. Okres rozruchu trzeba wyznaczyć inaczej.

5. **Kody rabatowe obniżają cenę o stałą kwotę w złotych, a nie o procent.** START10 i RANKING10 to 10 zł, WRACAM15 15 zł, L4SZYBKO20 20 zł, TIKTOK25 25 zł, TEST-QA 88 zł. Kody L4SZYBKO20, START10, TIKTOK25 i RANKING10 występują wyłącznie na pierwszym zamówieniu pacjenta. WRACAM15 występuje wyłącznie na kolejnych zamówieniach.

6. **Starty kampanii widoczne w danych (kandydaci na zdarzenia do punktu A5, nie problemy jakości):**
   - `meta_prosp_l4_szybko` (Meta): sesje i koszty od 3.11.2025, kod L4SZYBKO20 od 4.11.2025;
   - `tt_prosp_l4_15min` (TikTok): sesje i koszty od 9.02.2026, kod TIKTOK25 od 10.02.2026;
   - `crm_go_upsell` (newsletter, sprzedaż TelemediGO): sesje od 8.09.2025.

### Drobne

7. **Luka w danych 17.05.2025 od 13:00 do 14:00.** W tej godzinie jest 1 sesja zamiast typowych 21 i nie ma żadnego zamówienia. Dwie inne godziny (11.10.2024 16:00 i 14.12.2024 13:00) mają sesje bez zdarzeń lejka, ale to może być przypadek. Wpływ pomijalny.
8. **24 zamówienia „psycholog + e-recepta”.** Psycholog nie jest lekarzem i w Polsce nie wystawia recept. Wartość nierealna.
9. **Jedno zamówienie pacjenta z aktywnym TelemediGO jest zapłacone bez zniżki.**
10. **Program poleceń:** 330 sesji wchodzi na `/polecenie` z innym źródłem (bezpośrednio, z Google albo z Meta). Kolejne 51 sesji ma źródło `polecenie`, ale inną stronę wejścia. Ważne przy przypisywaniu źródła.

### Sprawdzone i czyste

- Czas: moment płatności w każdym z 65 278 zamówień i w każdym z 4 227 zakupów TelemediGO jest co do sekundy równy krokowi `payment_succeeded` w analityce po przeliczeniu na czas polski. System transakcyjny zapisuje czas polski i poprawnie obsługuje zmianę czasu. Pliki kwartalne i półroczne są pocięte według północy czasu polskiego, bez dziur i bez nakładek.
- Kliknięcia wobec sesji są stabilne w każdym kwartale: około 0,92 sesji na kliknięcie w Google, od 0,79 do 0,82 w Meta i 0,72 w TikToku. Nie ma dni z kosztem bez sesji ani sesji z kampanii płatnej bez kosztu. Największe odchylenie dnia od średniej kampanii mieści się w szumie losowym.
- Powiązania: każde zamówienie i każdy zakup TelemediGO ma sesję tego samego konta. Każda płatność w analityce ma zamówienie albo zakup TelemediGO. Nic nie dzieje się przed założeniem konta.
- Statusy wobec zwrotów są zgodne z opisem w README. Nie ma zwrotów większych niż zapłata ani zwrotów częściowych. Ceny katalogowe są stałe przez dwa lata. Zniżki TelemediGO (50% i 20%) i kody rabatowe zgadzają się co do złotówki. TelemediGO kosztuje zawsze 89 zł, jest ważne 365 dni, a członkostwa jednego pacjenta się nie nakładają.
- Kroki lejka idą zawsze w kolejności. Nie ma kroku bez poprzedniego.
- Tożsamość: żadna przeglądarka nie jest dzielona przez dwa konta. 3 835 kont (7,3%) używa więcej niż jednej przeglądarki, najwięcej ośmiu.
- Wartości realne: wiek pacjentów od 18 do 84 lat, wizyty trwają od 3 do 36 minut, termin wypada od 9 minut do 71 godzin po zapłacie.

## 2026-10-19 — odtworzenie dashboardu (punkt A3)

Pełny raport: `analiza/wyniki/a3_dashboard.txt`, kod: `analiza/a3_dashboard.py`, cała siatka wariantów: `analiza/wyniki/a3_siatka.csv`.

**W skrócie: dashboard liczy dane na surowo — z duplikatami zamówień, z zamówieniami testowymi i z przychodem przed zwrotami. Po oczyszczeniu wzrost zamówień spada z +61% do +56%, a przychodu z +50% do +48%. Liczba nowych pacjentów i sprzedaż TelemediGO się nie zmieniają.**

1. **Jak liczony jest dashboard.** W siatce 864 kombinacji definicji wszystkie cztery liczby naraz daje 14 kombinacji. Każda z nich liczy zamówienia razem z duplikatami i razem z testami, a przychód jako sumę zapłat przed zwrotami. Żadna kombinacja bez duplikatów albo bez testów nie pasuje.
   - Pasujące kombinacje różnią się tylko drobiazgami: czy liczą zamówienia anulowane, czy granice okresów są w czasie polskim czy w UTC, czy przychód obejmuje TelemediGO, czy nowym pacjentem jest też ktoś, kto kupił samo TelemediGO. Różnice między nimi wynoszą najwyżej 0,64 punktu procentowego w każdej miarze.
   - Najprostsza pasująca kombinacja: każdy wiersz pliku zamówień to zamówienie, przychód to suma zapłat bez TelemediGO i bez odejmowania zwrotów, nowy pacjent to konto z pierwszym zamówieniem, czas polski. Daje +51,9% pacjentów, +60,7% zamówień, +50,3% przychodu i +40,3% TelemediGO.
   - Kontrola: gdyby dashboard obcinał procenty zamiast je zaokrąglać, nie pasowałaby żadna kombinacja.

2. **Mostek od dashboardu do danych oczyszczonych** (najprostsza kombinacja, okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026):

   ```
   krok                                nowi pacjenci   zamówienia   przychód z konsultacji   TelemediGO
   dashboard (dane surowe)                 +51,9%        +60,7%            +50,3%              +40,3%
   bez duplikatów                          +51,9%        +58,3%            +48,1%              +40,3%
   bez duplikatów i kont testowych         +52,1%        +55,7%            +47,7%              +40,3%
   + przychód po odjęciu zwrotów              —             —              +44,8%                 —
   ```

   - Duplikaty z czerwca 2026 dodają drugiemu rokowi 604 zamówienia, czyli 2,4 punktu procentowego wzrostu zamówień.
   - Testy dodają kolejne 2,6 punktu procentowego, bo w drugim roku jest ich prawie trzy razy więcej niż w pierwszym (1 518 wobec 553).
   - Nowi pacjenci prawie się nie zmieniają (+51,9% wobec +52,1%), bo testy to tylko 22 konta.
   - Po oczyszczeniu: 16 231 nowych pacjentów w okresie 1 i 24 687 w okresie 2; 24 716 i 38 491 zamówień; 2,375 i 3,508 mln zł zapłat przed zwrotami; 1 759 i 2 468 zakupów TelemediGO.

3. **Trop do A5: zwroty rosną prawie dwa razy szybciej niż sprzedaż.** Na danych oczyszczonych zwroty wynoszą 144 461 zł w okresie 1 i 279 855 zł w okresie 2, czyli +93,7%. Udział zwrotów w zapłatach rośnie z 6,1% do 8,0%. Najszybciej rosną zwroty po odbytej wizycie (status „refunded”): z 492 do 1 626 zamówień, czyli ponad trzykrotnie przy wzroście wszystkich zamówień o 56%. Za takie wizyty lekarz dostaje wynagrodzenie, więc to uderza w marżę podwójnie. Kiedy i gdzie to się zaczęło — w A5.

4. **Czego mostek jeszcze nie pokazuje:** start od zera. W pierwszym roku nie było bazy powracających pacjentów, więc część wzrostu zamówień i przychodu to naturalne dorastanie bazy, a nie lepsza retencja. To rozdzielamy w A5 (nowi wobec powracających, kohorty w tym samym wieku).

## 2026-10-19 — przy ustalaniu definicji (punkt A4)

Pełny raport: `analiza/wyniki/a4_definicje.txt`, kod: `analiza/a4_definicje.py`. Poniższe to obserwacje do sprawdzenia w A5, a nie wnioski. Przyczyn nie przesądzamy.

1. **Powrót w 90 dniach jest niższy w okresie 2 przy każdej definicji.** Przy przyjętych definicjach wynosi 23,6% w okresie 1 i 17,4% w okresie 2. Przy porównaniu na tych samych dniach kalendarzowych (punkt 27 założeń) jest to 23,9% (12 867 pacjentów) wobec 17,4% (18 924 pacjentów). We wszystkich wariantach nowego pacjenta i powrotu wynik mieści się między 23,0% a 25,2% w okresie 1 i między 16,9% a 18,5% w okresie 2. Kierunek jest więc ten sam.
2. **Zmienia się struktura źródeł.** Według przyjętej reguły źródła Meta (pozyskanie) to 6,3% nowych pacjentów w okresie 1 i 24,9% w okresie 2. TikTok rośnie z 0% do 8,9%. To kanały z najniższym powrotem w okresie 2: 6,7% (Meta pozyskanie) i 3,2% (TikTok) w 90 dniach. W pozostałych kanałach powrót w okresie 2 wynosi od 16,8% do 26,1%. Zmiana struktury może tłumaczyć część spadku powrotów, ale nie całość: powrót pacjentów z Meta (pozyskanie) spada też w obrębie samego kanału, z 20,7% do 6,7%. Rozdzielamy to w A5.
3. **Zwroty po odbytej wizycie przy pierwszym zamówieniu.** Takich pierwszych zamówień było 341 w okresie 1 i 1 394 w okresie 2. Ci pacjenci wracają w 90 dniach w 5,0% (okres 1) i 3,3% (okres 2), wobec 24,5% i 18,6% po wizycie odbytej bez zwrotu. Najczęściej zdarza się to w Meta (11,0% pierwszych zamówień według sesji płatności) i w TikToku (13,3%), wobec 1,7–3,6% w pozostałych kanałach. Możliwe wyjaśnienia to obietnica reklamy, decyzje lekarzy albo inna przyczyna. Rozstrzygamy w A5.
4. **Wejścia z newslettera i SMS-ów to w dwóch trzecich sesje zalogowane od wejścia, bez żadnego zakupu w sesji.** Takich wejść jest 10 330 z 15 239 (wejścia z pełnymi 61 dniami obserwacji, bez kampanii sprzedającej TelemediGO). W kolejnych dniach widać tylko małą nadwyżkę zamówień: 6 na 1 000 wejść w 7 dni i 13 na 1 000 w 30 dni. Pozostałe 4 909 wejść daje 557 zamówień nieanulowanych na 1 000 wejść w tej samej sesji. CRM to główny kanał powrotów, więc dołączamy to do sprawy sesji zalogowanych w A5 (dopisek Kuby).
5. **Kampania sprzedająca TelemediGO (`crm_go_upsell`)** daje 696 zakupów TelemediGO na 1 000 wejść w tej samej sesji. Każdy osobny zakup TelemediGO przypada po co najmniej drugim zamówieniu pacjenta.
6. **Pacjenci z kodem kampanii płacą często w innej sesji niż ta z kampanii.** 1 711 pacjentów z kodem L4SZYBKO20, TIKTOK25 albo RANKING10 płaci w sesji bezpośredniej, z wyszukiwania marki, z bezpłatnego Google albo z remarketingu Meta. Według pierwszego wejścia 97% z nich trafia do kampanii kodu. Dla tych trzech kampanii sesja płatności przypisuje więc część pacjentów pozyskanych przez kampanię do wejść bezpośrednich, wyszukiwania marki i remarketingu.

## 2026-10-19 — lejek i zdarzenia w lejku (punkt A5, część pozyskania)

Szczegóły, liczby i metoda: `notatki/a5_pozyskanie.md`. Raporty: `analiza/wyniki/a5p_*.txt`. Liczby potwierdził Codex (model Sol) własnym kodem. Jeden błąd mianownika w `a5p_zalogowane.py` został poprawiony (`notatki/recenzje/a5p_codex.md`).

**W skrócie: tracimy pacjentów w dwóch miejscach, które trzeba naprawić na stronie: w przeglądarkach wbudowanych w aplikacje i w zakładaniu konta w Safari na iOS od 17.03.2026.** *(Zawężone 2026-10-21 po konsylium i dopisku Kuby: pewna naprawa na stronie to Safari na iOS. W kampaniach do nowych odbiorców nie wykryliśmy niższej konwersji przeglądarki w aplikacji niż zwykłej w tej samej kampanii (porównanie obserwacyjne); rzadziej płaci tylko w ruchu osób, które znają już stronę, i nie wiemy, czy przez przeglądarkę — sekcja z 2026-10-21 niżej.)* ** Rachunkowo prawie cały spadek konwersji lejka to zmiana struktury ruchu. Ten ruch traci jednak na każdym kroku, więc to nie jest tylko „inny ruch” (dopisek Kuby).**

1. **Konwersja sesji do płatności spadła z 16,0% w okresie 1 do 13,7% w okresie 2.** Rachunkowo prawie cały spadek to większy udział przeglądarek wbudowanych w aplikacje Instagram, Facebook i TikTok: z 10,7% do 35,6% sesji, głównie z reklam Meta i TikToka. Te przeglądarki płacą w 5–7% sesji, a Chrome i Safari w 16–18%. Tracą na każdym kroku lejka, także na zakładaniu konta.
2. **Zdarzenie 17.03.2026: w Safari na iPhone'ach i iPadach gwałtownie spada skuteczność zakładania nowego konta** (konta dalej powstają, ale rzadziej: 668 zamiast 1 082 w 60 dniach). Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spada z 66,2% (60 dni przed, 16.01–16.03.2026) do 45,1% (60 dni po, 17.03–15.05.2026) i zostaje na tym poziomie do końca danych (45,6% w całym okresie 17.03–30.09.2026 wobec 66,1% w okresie 1.10.2025–16.03.2026). *(Brzmienie poprawione 2026-10-21 po konsylium: wcześniej „przestaje działać”.)* Inne przeglądarki tego nie mają. Spadek jest w każdym kanale, więc to nie zmiana struktury. Psuje się zakładanie nowego konta, a logowanie do istniejącego działa. Szacunek: około 95–105 utraconych pierwszych zamówień na 30 dni, razem 628–695 od 17.03 do 30.09.2026. Przyczyny w danych nie widać.
3. **Starty kampanii jako zdarzenia:** Meta na L4 od 3.11.2025 (płaci w lejku lepiej niż starsza kampania Meta, ale 2–3 razy rzadziej niż wyszukiwarka; strona `/zwolnienie-l4-online` traci na konwersji tylko przez ten ruch), TikTok od 9.02.2026, sprzedaż TelemediGO w newsletterze od 8.09.2025 (686 zakupów samego TelemediGO).
4. **Remarketing Meta słabnie od początku 2026 przez zmianę puli odbiorców.** Płatność spada z 28,2% sesji w IV kwartale 2025 do około 19% w II i III kwartale 2026. W obrębie źródła, z którego osoba trafiła na stronę pierwszy raz, konwersja stoi.
5. **Sesje zalogowane od wejścia: dane nie rozstrzygają między odczytaniami.** Przeciw „zepsutej ścieżce, która odbiera nam zakupy” przemawiają trzy rzeczy: pacjenci odpadają przed krokiem konta, a nie na nim; pacjenci z takimi sesjami wracają częściej niż podobni bez nich; krok konta w zakupach powtórnych trwa kilkadziesiąt sekund, a nie 1–2 sekundy. Zostaje mocna niespójność ze słownikiem danych: według niego zalogowany pacjent nie ma kroku konta, a w danych ma go każdy zakup. Po pierwszym zakupie pacjent nie ma ani jednej anonimowej sesji, a rozkład odstępów między krokami w zakupach powtórnych jest jednakowy. To wygląda na cechę generatora danych.
6. **Sezon a wydatki: przyczyny wzrostu nowych pacjentów od X 2024 do I 2025 nie da się rozdzielić.** W kanałach opartych na wyszukiwaniu (bezpłatnym i płatnym) widać wyraźny sezon: zimą więcej nowych pacjentów niż latem. Wydatki rosły jednak w tych samych miesiącach. Kampania Meta z prawie stałym budżetem ma co najwyżej słaby sezon (+8% pacjentów zimą przy +5% wydatków).
7. **Strata między kliknięciem reklamy a sesją w Meta i TikToku** (dopisek Kuby). Na kliknięcie przypada 0,92–0,93 sesji w Google Ads, 0,79–0,82 w Meta i 0,72 w TikToku, stale w każdym kwartale. Trzy odczytania: porzucenie przed załadowaniem strony, luka w śledzeniu w przeglądarkach wbudowanych albo inne liczenie kliknięć przez platformy. W remarketingu Meta przeglądarek wbudowanych jest mało, a stosunek jest ten sam, co bardziej pasuje do liczenia kliknięć. Górna granica w okresie 2: 23 776 sesji, do 1 434 zamówień i 50 494 zł wydatków.
8. **Co nie jest zdarzeniem:** wzrost konwersji w pierwszym roku (dorastanie bazy powracających), spadki kroku konta z 5–12.02.2026 (ten sam problem Safari na iOS plus zmiana struktury) i spadek wyboru usługi wiosną 2026 (zmiana struktury). Kroki płatności są stabilne w każdym podziale.

## 2026-10-19 — kohorty, struktura pacjentów i przebieg wizyty (punkt A5, część retencji)

Szczegóły, liczby i metoda: `notatki/a5_retencja.md`. Raporty: `analiza/wyniki/a5r_*.txt`. Dwie recenzje Codeksa (model Sol) uwzględnione: `notatki/recenzje/a5r_codex.md` i `a5r_codex2.md`.

**Kohorty, powroty i marża na pacjenta (krok 2; porównanie na tych samych dniach kalendarzowych, tylko kohorty z pełnym oknem):**

- **Powrót spada w każdym oknie.** W 30 dniach 11,0% (14 984 pacjentów) wobec 7,8% (22 646). W 60 dniach 19,1% (13 941) wobec 13,7% (20 823). W 90 dniach 23,9% (12 867) wobec 17,4% (18 924). W 180 dniach 27,5% (9 125) wobec 22,2% (12 591).
- **Krzywa „dzień od pierwszego zakupu”:** okres 2 ma od 7. do 90. dnia stale około 72–75% powrotu okresu 1. Dłuższe okna (180 i 270 dni) wyglądają lepiej (0,81 i 0,89), ale obejmują tylko najstarsze kohorty okresu 2 (X 2025 – III 2026), więc nie świadczą o nadrabianiu.
- **Marża na pacjenta przed kosztem pozyskania** (przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza): w 90 dniach 66,6 zł wobec 58,3 zł (−8,3 zł, −12,5%); w 30 dniach 55,9 zł wobec 49,9 zł; w 180 dniach 75,5 zł wobec 67,7 zł. Kolejne zamówienia na pacjenta w 90 dniach: 0,334 wobec 0,234.
- **Kohorty miesięczne:** w okresie 1 powrót w 90 dniach mieści się między 21,3% a 26,3%. Październik 2025 jest jeszcze na tym poziomie (23,5%). Od listopada 2025 spada do 18,9–20,0%, a od marca 2026 do 13,7–15,6%. Kohorty tygodniowe pokazują te same dwa progi: tydzień od 3.11.2025 i tydzień od 2.03.2026.
- **Start od zera:** w okresie 2 jest 38 491 zamówień: 24 687 pierwszych, 5 289 powtórnych od pacjentów z kohort okresu 1 i 8 515 powtórnych od pacjentów z kohort okresu 2. W okresie 1 było 24 716 zamówień: 16 231 pierwszych i 8 485 powtórnych. Powtórne zamówienia rosną więc o 62,7%, ale 5 289 z nich to baza z okresu 1, której w okresie 1 z definicji nie było.
- **Koszt pediatry (wrażliwość):** wariant 25 zł zamiast 100 zł podnosi marżę na pacjenta w 90 dniach o 4,8 zł w okresie 1 i o 3,7 zł w okresie 2 (różnica kosztu: 84 300 zł i 110 700 zł). Kierunek zmiany się nie zmienia.

**Struktura a zachowanie oraz przebieg wizyty (kroki 3–5, w brzmieniu przyjętym przez Kubę):**

- Krok 3 w brzmieniu przyjętym przez Kubę (dopisek nr 1; liczbowo, po weryfikacji Astrą: około 46–71% spadku, zależnie od reguły źródła): większość spadku powrotów wiąże się z pacjentami dwóch nowych kampanii na L4, ale w kampaniach działających w obu latach też jest spadek, którego sprawdzone cechy nie tłumaczą. Obie wersje według reguły źródła: przyjęta reguła 4,6 i 2,0 punktu, sesja płatności 3,0 i 3,5 punktu (spadek z 23,9% do 17,4% w 90 dniach).
- Krok 4 i 5, przyjęte przez Kubę (STOP 2):
  - **Opóźnienia porannych wizyt u internisty od listopada 2025** (kandydat zmiany 24.11.2025): wizyty z terminem 6:00–11:59 spóźnione ponad 15 minut, pacjenci spoza nowych kampanii, 4,7–6,9% miesięcznie do X 2025, 15,7% w XI 2025, 29,7% w XII, 42,6% w I 2026, 47–53% od II 2026. U internisty w innych porach i u specjalistów bez dużej zmiany. **Przy tym samym porannym ruchu w dniu opóźnień jest o 26,4 punktu procentowego więcej niż rok wcześniej**, a w obrębie miesiąca opóźnienia prawie nie zależą od ruchu. Odczytanie bez przesądzania przyczyny: spadła poranna przepustowość (obsada, organizacja zapisów albo lekarze zajęci pacjentami spoza B2C), a nie tylko przybyło pacjentów.
  - **Rano spada powrót po wizytach spóźnionych, nie po punktualnych.** Pacjenci starych kampanii z pierwszą wizytą u internisty rano: powrót w 90 dniach 23,6% wobec 19,0%; wieczorem 23,5% i 23,5%. Sama zmiana rozkładu opóźnień przy stałych kampaniach i usługach odpowiada za −0,76 z −1,91 punktu spadku w starych kampaniach (przyjęta reguła źródła) i −0,64 z −3,50 (sesja płatności).
  - **Zwroty po wizytach L4 w nowych kampaniach (ważne dla listy priorytetów):** 17,4% odbytych wizyt L4 pacjentów kampanii `meta_prosp_l4_szybko` i `tt_prosp_l4_15min` kończy się zwrotem po wizycie (1 024 z 5 895 w okresie 2), wobec 5,3% L4 pozostałych pacjentów (270 z 5 080) i 6,0% w okresie 1. Kod rabatowy i opóźnienie nie zmieniają odsetka. W okresie 2 wszystkie zwroty po wizycie pacjentów nowych kampanii to 1 044 wizyty, 84 112 zł zwróconych zapłat i 33 975 zł kosztu lekarza za te wizyty. Powodu zwrotu w danych nie ma (możliwe odczytanie: lekarz nie wystawia L4, którego pacjent oczekuje po obietnicy reklamy).
  - **Niska zgoda marketingowa pacjentów nowych kampanii (ważne dla listy priorytetów):** 37,8% wobec 63,8–64,4% pacjentów starych kampanii; wejście z newslettera albo SMS-a w dniach 1–90 ma 8,2% z nich wobec 17,5–17,9%. Newsletter i SMS-y do tych pacjentów prawie nie docierają.
  - **Brak wyraźnego zdarzenia w powrocie starych kampanii:** najsilniejszy kandydat 2.03.2026 (z = −3,943, poniżej progu 4): 23,3% przed, 20,9% po. Luty 2026 bez spadku mimo opóźnień — trop eksploracyjny.

## 2026-10-20 — ekonomia kampanii (punkt A5)

Szczegóły, liczby i metoda: `notatki/a5_ekonomia.md`. Raporty: `analiza/wyniki/a5e_*.txt`, zestawienie `analiza/wyniki/a5e_kampanie.csv`. Recenzja Codeksa (model Sol) uwzględniona. Wynik po 180 dniach stoi zawsze obok wyniku po 90 dniach (dopisek Kuby).

**W skrócie:**

1. **Nowe kampanie na L4 pozyskują pacjenta taniej niż reszta kampanii płatnych, ale ten pacjent zostawia prawie o połowę mniej marży.** Według przyjętej reguły źródła wynik na pacjenta to +3,6 zł po 90 dniach i +7,0 zł po 180 dniach. Według sesji płatności to −9,4 zł i −5,2 zł. Znak zależy od reguły atrybucji, więc to wynik **niepewny**. Pozostałe kampanie płatne mają +20,0 zł po 90 dniach i +29,7 zł po 180 dniach.
2. **Kampania na TikToku ma wynik ujemny w obu regułach i w obu oknach:** −4,6 i −17,8 zł na pacjenta po 90 dniach oraz −1,1 i −11,0 zł po 180 dniach, przy małej próbie. Kampania Meta na L4 jest niepewna: +6,5 i −6,5 zł po 90 dniach oraz +8,2 i −4,3 zł po 180 dniach.
3. **Niska marża tych pacjentów to kody rabatowe, zwroty po wizycie L4 i prawie zerowe powroty.** Tańszy lekarz (internista) częściowo to równoważy.
4. **Zgoda marketingowa i przeglądarki wbudowane w aplikacje nie dają w tym rachunku wyraźnej wartości.** U pacjentów nowych kampanii zgoda prawie nie zmienia powrotu. Surowa konwersja w przeglądarkach wbudowanych nie jest w tych kampaniach niższa niż w zwykłych.
5. **Największa dźwignia naprawy to zwroty po wizytach L4.** Gdyby spadły do poziomu pozostałych pacjentów, dawałoby to od 22 do 57 tys. zł marży rocznie według przyjętej reguły.
6. **Dane nie rozstrzygają, czy pacjenci tych kampanii są dodatkowi.** Łączne pozyskanie w pozostałych kanałach po startach kampanii nie spadło wyraźnie. Widać jednak sygnał względnego osłabienia L4 w pozostałych kanałach po starcie kampanii Meta.
7. **Hipoteza porannych opóźnień to tylko scenariusz: od 0 do 65 tys. zł marży rocznie.** W wariancie wąskim wychodzi około 12 tys. zł. Na pacjenta nowych kampanii to od 0 do 12,6 zł. Szeroki wariant zjada cały ich wynik według przyjętej reguły.

**Szczegóły:**

- Nowe kampanie na L4 według przyjętej reguły: koszt pozyskania 32,7 zł, marża 36,3 zł, wynik +3,6 zł na pacjenta w 90 dniach. Według sesji płatności: 45,6 zł, 36,1 zł i −9,4 zł. Pozostałe kampanie płatne: +20,0 zł i +18,7 zł. Wynik nowych kampanii zależy od reguły atrybucji (niepewny). TikTok ma wynik ujemny w obu regułach (−4,6 i −17,8 zł), a Meta na L4 jest niepewna (+6,5 i −6,5 zł).
- Według sesji płatności prawie wszystkie kampanie pozyskujące mają wynik ujemny w 90 dniach, a według przyjętej reguły dodatni. To własność reguły, nie błąd kodu (punkt 2, potwierdził Codex).
- Marża pacjentów nowych kampanii jest niższa o 27,9 zł na pacjenta. Odpowiadają za to kody rabatowe (−12,8 zł), zwroty (−8,7 zł), brak powrotów (−12,1 zł), niższa cena (−6,7 zł) i rzadsze TelemediGO (−3,8 zł). Tańszy lekarz równoważy +16,2 zł.
- Zgoda marketingowa u pacjentów nowych kampanii prawie nie zmienia ich powrotu (4,2% wobec 4,1%).
- W nowych kampaniach surowa konwersja sesji do pierwszego zamówienia w przeglądarkach wbudowanych w aplikacje nie jest niższa niż w zwykłych (bez rozdzielenia urządzenia, daty i pacjenta).
- `gs_generic_specjalisci` ma wynik ujemny w obu regułach i oknach. `gs_generic_erecepta` drożeje: koszt pozyskania rośnie z 48,8 do 59,8 zł.
- Dodatkowość: nie widać dużego spadku łącznego pozyskania w pozostałych kanałach po startach kampanii. Widać jednak sygnał względnego osłabienia L4 po starcie Meta: L4 wobec innych usług w pozostałych kanałach 0,73 (od 0,56 do 0,95), kampania Google Ads na L4 0,67 (od 0,45 do 0,98). Na fikcyjnych datach startu w okresie 1 tak niski iloraz wychodzi w 4 z 44 tygodni. Dane nie rozstrzygają dodatkowości.
- Ranking lekarzy daje w obu okresach prawie tę samą liczbę pacjentów (616 i 617). Możliwa cecha generatora, bez wpływu na wnioski.

**Co zmienia okno 180 dni:**

- `gs_generic_lekarz_online` i `gs_generic_erecepta` przestają zależeć od reguły atrybucji: po 180 dniach są dodatnie w obu regułach;
- zależne od reguły zostają `meta_prosp_l4_szybko`, `gs_generic_l4` i `meta_prosp_lekarz_online`;
- TikTok i `gs_generic_specjalisci` są ujemne w obu regułach w obu oknach.

## 2026-10-20 — wynik biznesu po kwartałach (punkt B i dopisek Kuby do punktu C)

Raporty: `analiza/wyniki/b_eksport.txt` i `analiza/wyniki/c_priorytety.txt` (W4, P1). Obie sesje liczyły to niezależnie i dostały te same liczby.

- **Suma roczna ukrywa przebieg w kwartałach.** Marża (przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza − kampanie − prowizja) rośnie rok do roku o 71,4% w IV kwartale 2025, o 43,0% w I kwartale 2026, o 13,0% w II kwartale i spada o 6,8% w III kwartale 2026 (207 713 zł wobec 222 824 zł). Wydatki na kampanie są w tych kwartałach 1,30, 1,66, 2,04 i 2,08 raza wyższe niż rok wcześniej. Za cały rok marża rośnie o 26,6%.
- **Spadek w III kwartale to wydatki rosnące szybciej niż marża przed kampaniami:** marża przed kampaniami +78 963 zł, wydatki +94 123 zł.
- **Niższy jest kwartał, a nie każdy miesiąc.** Lipiec 2026: 73 384 zł wobec 66 832 zł; sierpień: 66 315 wobec 67 190 zł; wrzesień: 68 014 wobec 88 802 zł.
- **Wrzesień 2025 zawyża bazę porównania** przez start sprzedaży TelemediGO w newsletterze (225 zakupów w 23 dni). Bez opłat za TelemediGO III kwartał 2026 też jest niższy: −4,9%.
- **Szacowana skala problemu Safari na iOS w III kwartale 2026 (około 14–21 tys. zł marży) jest porównywalna ze spadkiem marży tego kwartału** (15,1 tys. zł; `c_priorytety.txt`, P1), ale wyniku kwartału bez tego problemu nie ustaliliśmy (weryfikacja Astrą, `notatki/recenzje/d_astra.md`). *(Poprawione 2026-10-21: „14–21 tys. zł” mieszało marżę z dnia zakupu z marżą rocznika. Strata zaksięgowana w samym kwartale to 14,6–18,3 tys. zł i 4,1–4,5 tys. zł powrotów pacjentów utraconych wcześniej, założenie 58. Rozkład spadku kwartału: sekcja z 2026-10-21 niżej.)*

## 2026-10-20 — TelemediGO i lista priorytetów (punkt C, przyjęte przez Kubę)

Szczegóły i liczby: `notatki/c_szkic.md` (sekcje 1–4), raporty `analiza/wyniki/c_telemedigo.txt` i `c_priorytety.txt`. Liczby główne potwierdził Codex (Sol) własnym kodem. Listę priorytetów oceniło konsylium (9 z 9): `notatki/konsylium/c_priorytety/synteza.md`.

**TelemediGO:**
- Wzrost sprzedaży TelemediGO o 40,3% to więcej zamówień i pełny rok sprzedaży w newsletterze (w okresie 1 23 dni). Odsetek nowych pacjentów, którzy kupują przy pierwszym zamówieniu, spada z 5,58% do 4,41%, w całości przez pacjentów nowych kampanii na L4 (1,5%).
- Członkostwa z okresu 1 dostały 104,57 zł zniżki efektywnej przy opłacie 89 zł. Kupujący przy kolejnym zamówieniu dostają 136,36 zł.
- Po zniżce 20% cena wizyty jest niższa niż koszt lekarza u wszystkich specjalistów poza psychiatrą. W okresie 2 to −14,7 tys. zł marży na 1 512 zamówieniach.
- Przy koszcie pediatry 100 zł (założenie 33) wizyta u pediatry przynosi stratę także bez zniżki (cena 95 zł).
- Odnawia około 5% członków. W danych nie widać przypomnienia o wygaśnięciu.
- Kupujący TelemediGO wracają częściej niż podobni pacjenci (+10,1 i +14,6 punktu procentowego w 90 dniach), ale po wygaśnięciu przewaga w proporcji zostaje (iloraz 1,77). Dane nie rozdzielają wpływu zniżki od samoselekcji.
- Wizyta u specjalisty po cenie katalogowej zostawia ponad koszt lekarza tylko 9–19 zł (cena 109–119 zł); pediatra (95 zł) i psycholog (99 zł) mają cenę poniżej kosztu lekarza przy założeniu 33 (`c_priorytety.txt`, P14).

**Odpowiedź „czy to wzrost” (przyjęta przez Kubę):** pacjentów z pierwszym zakupem jest o 52,1% więcej, ale retencja jest gorsza: powrót w 90 dniach 17,4% wobec 23,9% na tych samych dniach kalendarzowych, a bez pacjentów nowych kampanii 22,0% (przyjęta reguła) albo 20,4% (sesja płatności). W III kwartale 2026 marża była o 6,8% niższa niż rok wcześniej przy wydatkach na kampanie 2,08 raza wyższych; szacowana strata z Safari zaksięgowana w kwartale jest tego samego rzędu co ten spadek (sekcja z 2026-10-21 niżej). Liczba osób, które wróciły w 90 dniach, rośnie (3 076 → 3 289, +6,9%), spada odsetek.

**Lista priorytetów (przyjęta przez Kubę, 12 pozycji):** Safari na iOS; pomiar; wstrzymać TikToka na L4; wstrzymać Google Ads na specjalistów do zmiany cennika; uczciwa obietnica L4 w Meta; poranna obsada internistów; komunikacja po wizycie z grupą kontrolną; test zalogowanych; test dodatkowości Meta; cennik i warunki TelemediGO u specjalistów; strata kliknięć; test TelemediGO. Wartości, sposób pomiaru i wdrożenie: `c_szkic.md`, sekcja 3.

## 2026-10-21 — poprawki po konsylium końcowej weryfikacji (punkt D)

Lista Kuby: `notatki/d_poprawki.md`. Raporty: `analiza/wyniki/d_retencja.txt`, `d_kampanie.txt`, `d_wynik.txt`. Recenzja Codeksa (Sol): `notatki/recenzje/d2_codex.md`. Każdą wątpliwość Kuby najpierw policzyliśmy, potem zmieniliśmy zdanie.

**Wątpliwości Kuby — co pokazały dane:**
- **Opóźnienia po godzinach: Kuba ma rację.** U internisty największy wzrost to jeden blok od 5:00 do 12:59 (o 5:00 z 1,5% do 15,3% wizyt spóźnionych ponad 15 minut, o 12:00 z 3,4% do 22,3%), a mniejszy zostaje o 13:00 (z 2,5% do 5,6%). Poza 5:00–13:59 odsetek jest prawie taki sam (2,8% z 9 563 wizyt wobec 2,7% z 14 898). Wzrost „w południe” i „w nocy” to głównie brzegi porannego bloku. U pozostałych lekarzy rano bez istotnej zmiany (2,8% z 1 949 wobec 3,0% z 2 757).
- **Poranek: już wizyty z najwcześniejszym porannym terminem dnia są często spóźnione, a narastania nie widać.** Spóźnione ponad 15 minut: 41,9% (391 wizyt, okres 2) wobec 43,3% kolejnych (8 760). W tym samym miesiącu godziny z 8 i więcej wizytami mają tylko o 4,2 punktu więcej spóźnionych niż godziny z 1–3 wizytami. Odczytanie: stałe przesunięcie od początku dnia, a nie kolejka ponad przepustowość. Najwcześniejszy termin liczymy dla całej sieci, nie dla lekarza; mechanizmu bez danych o lekarzach i grafikach nie rozstrzygamy.
- **Przeglądarki w aplikacjach: nie uogólniamy.** W kampaniach do nowych odbiorców nie wykryliśmy niższej konwersji niż w zwykłych przeglądarkach w tej samej kampanii (także Meta „lekarz online”: −0,15 punktu, 29 330 sesji w przeglądarkach wbudowanych); porównanie jest obserwacyjne. W ruchu osób, które znają już stronę, płacą rzadziej: remarketing Meta −12,2 punktu (1 772 sesje), Google Ads na markę −5,1 (2 357), wejścia bezpośrednie −4,4 (4 261). Nie wiemy, czy winna jest przeglądarka, czy to, kto z niej korzysta.
- **TikTok po 180 dniach: pewność co do znaku zostaje.** Wynik −1,1 zł to tylko wczesne kohorty 10.02–3.04.2026 (299 pacjentów) z tańszym pozyskaniem (32,4 zł wobec 37,3 zł całego rocznika), które w dniach 91–180 nie dorobiły marży. Przybliżenie dla całego rocznika: −5,4 zł według przyjętej reguły i −19,3 zł według sesji płatności.
- **Pediatra i psychiatra: bez istotnej zmiany** (22,3% → 26,3% i 22,5% → 24,6%, przedziały obejmują zero). Pierwsze L4 z pozostałych kanałów jest bez zmiany tylko według przyjętej reguły (14,6% → 13,8%); według sesji płatności spada do 11,0%.
- **Spadek marży w III kwartale 2026 (−15,1 tys. zł):** według przyjętej reguły pacjenci nowych kampanii wychodzą prawie na zero (+1,1 tys. zł), a reszta traci 16,2 tys. zł: TelemediGO −11,2 tys. zł (sprzedaż osobna w newsletterze we wrześniu 2025), wyższe wydatki kampanii działających w obu latach −6,2 tys. zł, marża konsultacji +1,2 tys. zł. **Księgowo lukę po odjęciu TelemediGO (5,0 tys. zł) wyjaśniają wyższe wydatki starych kampanii, częściowo skompensowane wzrostem marży konsultacji. Szacunek Safari (14,6–18,3 tys. zł w kwartale) jest większy niż ta luka, więc się w niej nie mieści; rozkład księgowy nie rozdziela jednak wpływu Safari od innych zmian przychodu.** Według sesji płatności podział się odwraca. Cały spadek przypada na wrzesień.
- **Test Mety w 4–6 tygodni nie odróżni wyniku od progu.** Błąd udziału dodatkowych 24,4 punktu po 4 tygodniach i 20,1 po 6 (testy pozorne, ocena orientacyjna); dłuższy test wymaga osobnego przeliczenia. Rozrzut jest prawie czysto losowy, więc sam dobór par prawdopodobnie nie wystarczy. Próg po naprawie zwrotów: 70,0% (90 dni). W liczbie pacjentów próg prawie nie zależy od reguły: około 4 320 pacjentów w 332 dniach działania kampanii.

**Nowe obserwacje przy okazji:**
- **Tempo ostatniego półrocza:** wydatki nowych kampanii dziennie wyższe o 14,9% (Meta) i 14,3% (TikTok), nowi pacjenci tylko o 9,2% i 12,5%, więc wynik kampanii w tym tempie jest gorszy (Meta +23,1 zamiast +30,6 tys. zł rocznie, przyjęta reguła).
- **Koszt kliknięcia Google Ads na markę rośnie:** z 1,01 do 1,19 zł (+17,9%), co kwartał wyżej; koszt pierwszego zamówienia z 7,53 do 11,33 zł. Całe Google Ads tanieje o 3,5%.
- **Od 22.05.2026 spada konwersja Google Ads na markę:** sesja do płatności 21,2% → 17,8%, około 28,5–39,6 zamówienia mniej na 30 dni. To nie Safari ani zmiana struktury ruchu. Przyczyny w danych nie widać (niewiadoma 22).
- **Kod rabatowy Mety na L4 (L4SZYBKO20, 20 zł)** jest na 3 511 z 5 059 pierwszych zamówień kampanii, to 62,8 tys. zł zniżki efektywnej rocznie. Zwroty z kodem i bez są takie same (14,5% i 14,3%).
- **Konta bez zakupu:** 11 482 z 52 400 kont (21,9%), każde wybrało usługę i przeszło krok konta, 37,1% zaczęło płatność. 58,1% ma zgodę marketingową, ale nie ma ani jednego ich wejścia z newslettera albo SMS-a.
- **Baza powracających w kwartałach:** w III kwartale 2026 baza 35 032 pacjentów dała mniej marży niż rok wcześniej baza 12 794 pacjentów (106,2 wobec 115,2 tys. zł). Wzrost rok do roku IV kwartału 2025 i I kwartału 2026 jest zawyżony startem od zera; bez bazy +8,5% i +26,1% zamiast +71,4% i +43,0%.
- **Demografia nie zmienia wniosku** (założenie 55); dolnośląskie to trop do sprawdzenia.

## 2026-10-21 wieczorem — ostatnia runda przed publikacją: wątpliwości Kuby (punkt E, część 1)

Zlecenie: `notatki/e_runda.md`. Skrypt: `analiza/e_merytoryka.py` → `analiza/wyniki/e_merytoryka.txt` i `.json`. Każdą wątpliwość najpierw policzyliśmy.

- **Reguły źródła w retencji: cała różnica to jedna grupa pacjentów (Kuba ma rację).** 1 383 pacjentów z pełnym oknem 90 dni (2 081 w całych ostatnich 12 miesiącach) przyjęta reguła przypisuje nowym kampaniom na L4, a sesja płatności starym kanałom. 92% z nich weszło pierwszy raz z reklamy nowej kampanii, 73% zapłaciło z jej kodem, 83% zaczęło od L4; zapłacili po wejściu bezpośrednim (42%), z bezpłatnej wyszukiwarki (24%), z Google Ads na markę (22%) albo z remarketingu Meta (13%). Wracają w 4,3%, jak pozostali pacjenci nowych kampanii. Grupy odwrotnej nie ma. Bez tej grupy sesja płatności daje dokładnie to samo co reguła przyjęta (powrót 22,0%, marża 66,0 zł, pacjentów +7,3%, udział nowych kampanii w spadku powrotu 71%). To samo tłumaczy „L4 z pozostałych kanałów” według sesji płatności (11,0%): do 2 969 pacjentów reguły przyjętej dochodzi 1 145 pacjentów nowych kampanii z pierwszym L4. Recenzja Codeksa (Sol) doprecyzowała: z 2 081 pacjentów 1 918 weszło pierwszy raz z reklamy nowej kampanii i zapłaciło w innej sesji, a 163 weszło z innego kanału i zapłaciło z kodem nowej kampanii w tej samej sesji. Obie reguły dają bez tej grupy te same liczby zbiorcze (powrót, marża, przyrost pacjentów), choć dla 4 190 innych pacjentów (6 271 razem z tą grupą; e_merytoryka.txt, punkt 1) wskazują różne kampanie.
- **Spadek marży III kwartału 2026 (−6,8%) nie jest odporny.** Rok wcześniej sprzedaż osobna TelemediGO w newsletterze ruszyła 8.09.2025 i w 23 dni sprzedała 225 członkostw wobec zwykłego tempa 29 (461 w ostatnich 12 miesiącach). Nadwyżka 196 zakupów to 17,4 tys. zł. Bez niej marża III kwartału 2026 jest o 1,1% wyższa niż rok wcześniej; bez całej sprzedaży w newsletterze w obu latach o 2,3% niższa; bez wszystkich opłat TelemediGO o 4,9% niższa. Odporne: marża przed kosztem kampanii +25,2% (bez nadwyżki +32,6%) przy wydatkach 2,08 raza wyższych; za cały rok marża +26,6%, przed kampaniami +41,5%, wydatki +76,7%.
- **Baza powracających w III kwartale:** bez nadwyżki startu (jej części przypadającej na bazę: 210 z 225 zakupów; poprawka po recenzji Codeksa, wcześniej cała nadwyżka i +8,6%) dała w 2026 o 7,3% więcej marży niż rok wcześniej (bez całej sprzedaży w newsletterze +1,0%). Wszystkich pacjentów pozyskanych w poprzednich kwartałach jest prawie trzy razy więcej (35 032 wobec 12 794), ale tych, którzy w kwartale coś kupili, o 15% więcej (1 735 wobec 1 503). Dawne zdanie „baza dała mniej marży niż rok wcześniej” wynikało z jednorazowego startu sprzedaży w newsletterze.
- **Marża na powtórne zamówienie (35,86 → 32,81 zł, pacjenci spoza nowych kampanii, III kwartał) spada w 89% przez rosnący udział wizyt ze zniżką TelemediGO** (z 34,3% do 41,6% powtórnych zamówień). Wizyta ze zniżką zostawia 11,01 zł, bez zniżki 48,78 zł; u specjalisty ze zniżką −5,59 zł. W obrębie rodzaju zniżki marża prawie stoi (−0,35 zł). Spina się z tym, że opłata 89 zł nie pokrywa zniżek.
- **Lejek osób, które jeszcze nie kupowały: 11,2% → 9,3% sesji z płatnością.** Do stycznia 2026 różnica rok do roku wynosi 0,2–0,8 punktu, w lutym i marcu 2026 1,5–1,6 punktu, od kwietnia 2,3–3,1 punktu. Spadek zbiega się z rosnącym udziałem sesji nowych kampanii (luty 31,8%, od kwietnia 42–47%), które płacą w 5,5%. Bez nich konwersja nowych osób nie spada (11,2% → 11,4%). Krok konta po wyborze terminu spada od kwietnia (Safari na iOS).
- **Błąd w zdaniu o przeglądarkach w aplikacjach:** „4,8–7,2% wobec 16,1–18,1%” dotyczyło wszystkich sesji, a zdanie mówiło o osobach, które jeszcze nie kupowały. U nich: 3,8–6,6% wobec 9,9–12,2%. Poprawione na stronie.
- **Pozycja 7:** 3,16% i 18,84% to podział tej samej grupy (powrót 22,0%) według drogi powrotu, a nie porównanie dwóch grup; 14% powrotów zaczyna się od wejścia z newslettera albo SMS-a. 23,6 tys. zł za punkt procentowy to marża do 180. dnia.
- **Kampanie na markę i remarketing:** 37,1% i 24,1% zamówień w ich sesjach to zamówienia powtórne, których rachunek kosztu pozyskania nie uwzględnia, więc wynik tych kampanii na nowego pacjenta jest ostrożny.
- **Godzina bez danych (17.05.2025, 13:00–14:00):** zamówień w tej godzinie jest zwykle około 2 (mediana z 15 dni), więc ich brak niewiele mówi. Nie wiemy, czy to przerwa w działaniu strony, czy w zbieraniu danych.
- **Słownik danych o sesjach zalogowanych od wejścia** mówi tylko, że taka sesja nie ma kroku logowania; nie mówi, że powinna kończyć się zakupem. Zdanie w README poprawione.
- **Pozycja 4 (Google Ads na specjalistów):** pauza się opłaca, dopóki nowych pacjentów u specjalistów ze wszystkich kanałów ubywa mniej niż około 31 tygodniowo (wydatki 53,2 tys. zł / marża 32,4 zł na pacjenta w 90 dniach, bez zaokrąglenia: 1 640 rocznie); kampania przypisuje sobie 13–18 tygodniowo, a wszystkich nowych pacjentów u specjalistów jest około 66 tygodniowo.

## 2026-10-22 — trzecia lista Kuby: lejek bez nowych kampanii według pierwszego wejścia (punkt E)

Skrypt: `analiza/e_poprawki.py`, punkt 3 (kwiecień–wrzesień 2026 wobec tych samych miesięcy 2025, sesje osób, które jeszcze nie kupowały). Recenzja Codeksa (Sol): 9 z 9 liczb zgodnych (`notatki/recenzje/e3_codex*.md`).

- **Hipoteza Kuby się potwierdziła: płaska średnia „bez nowych kampanii” przykrywała Safari.** Według sesji konwersja bez nowych kampanii stoi (11,12% → 11,02%), ale według pierwszego wejścia osoby spada: 11,12% → 10,26% (65 262 i 71 441 sesji), −0,86 punktu procentowego, przedział 95% od −1,19 do −0,53. Różnica reguł to 8 236 sesji powrotnych osób z reklam L4 (wejście bezpośrednie, wyszukiwarka, inna reklama), które płacą w 17,6%; liczone według sesji zawyżały ruch spoza kampanii.
- **Prawie cały ten spadek to Safari na iPhone'ach:** 11,99% → 8,27% (12 887 i 14 323 sesje), krok konta po wyborze terminu 67,0% → 45,7%; przed awarią (X 2025 – II 2026) bez zmiany (12,15% i 12,07%). Pozostałe przeglądarki: 10,91% → 10,76%, bez istotnej zmiany (przedział od −0,52 do +0,22 punktu). Rozkład opisowy spadku −0,86 punktu: Safari −0,74 (około 86%), reszta −0,12.
- **Cecha danych:** sesje z reklam nowych kampanii mają tylko osoby, których pierwsze wejście to nowa kampania (0 sesji u pozostałych osób). Prawdopodobnie cecha generatora danych; w prawdziwych danych byłoby to nietypowe.

## 2026-10-23 — wątek Kuby po publikacji: dlaczego „Nie”, skoro marża rośnie o 27% (runda G)

Skrypt: `analiza/g_werdykt.py` → `analiza/wyniki/g_werdykt.txt` i `.json`. Codex (Sol) przeliczył wszystkie liczby własnym kodem: zgodne (`notatki/recenzje/g_werdykt_codex.md`).

- **Skąd przyrost pacjentów:** z 8 456 nowych pacjentów więcej (16 231 → 24 687) 7 268, czyli 86,0%, to pacjenci dwóch nowych kampanii na L4 według pierwszego wejścia (Meta 5 059, TikTok 2 209); według sesji z płatnością 5 187, czyli 61,3%.
- **Ile zostaje na pacjencie** (marża w 180 dniach minus koszt pozyskania, pierwsze zakupy 1.10–3.04): nowe kampanie 7,0 zł (2 352 pacjentów, przedział 95% od 5,4 do 8,6 zł), pozostałe kampanie płatne 29,7 zł wobec 31,8 zł rok wcześniej; według sesji z płatnością −5,2 zł, 27,5 i 30,0 zł. Cały rocznik z przybliżeniem: 2,8 zł wobec 26,7 i 30,8 zł.
- **Miesiąc po miesiącu** (nowe kampanie razem, według pierwszego wejścia): koszt pozyskania rośnie z 27–30 zł (XI 2025 – II 2026) do 33–37 zł (IV–IX 2026), marża w 180 dniach 34–40 zł, wynik od kwietnia od −1,0 do +3,0 zł; II i III kwartał 2026 0,7 i 0,4 zł. **Hipoteza Kuby „od wiosny dokładamy” nie potwierdziła się według pierwszego wejścia** (wychodzimy na zero); Meta na L4 jest na plusie w każdym miesiącu, TikTok na L4 pod kreską od marca 2026 (II kwartał −6,4 zł). Według sesji z płatnością obie kampanie razem tracą od grudnia 2025, od kwietnia od 11,6 do 15,9 zł na pacjencie.
- **Skąd +27% marży:** 828 085 → 1 048 069 zł (+219 984 zł). 194 434 zł (88,4% przyrostu) to zakupy w drugim roku pacjentów pozyskanych w pierwszym (152 960 zł marży konsultacji, 41 474 zł TelemediGO). Pacjenci pozyskani w danym roku, po kosztach kampanii i prowizji: 828 085 → 853 635 zł (+3,1%), na nowego pacjenta 51,02 → 34,58 zł. Nowe kampanie na L4 w roku pozyskania: +17,3 tys. zł według pierwszego wejścia, −58,3 tys. zł według sesji z płatnością.

## 2026-10-23 — runda G (przejrzystość): kolor zmian w tabelach grup był w większości szumem

Wątpliwość Kuby: przy porównaniu „60 dni przed i po godzinie bez danych” w podziale na pierwszą usługę prawie każda komórka tabeli kohort jest czerwona albo zielona, a grupy mają po 100–500 pacjentów i różnice rzędu 1–3 punktów procentowych. Policzone kodem (`analiza/g_istotnosc.py` → `analiza/wyniki/g_istotnosc.txt`). Wątpliwość się potwierdziła.

- **Przypadek Kuby (kohorty, 60 dni przed i po 17.05.2025, pierwsza usługa):** 48 komórek ze zmianą (powrót w 30, 60, 90 i 180 dniach, marża na pacjenta w 90 i 180 dniach, 8 wierszy). Strona kolorowała 46 z nich. Istotna nie jest żadna. 6 komórek dotyczy małych grup, poniżej 100 pacjentów w którymś okresie.
- **Kohorty, ustawienia domyślne (ostatnie 12 miesięcy wobec roku wcześniej, nowe kampanie na L4):** 12 komórek, kolorowe 12, istotnych 10. Przy dużych grupach i długich okresach kolor był zwykle uzasadniony.
- **Kohorty, rok do roku, pierwsza usługa:** 48 komórek, kolorowe 48, istotnych 30.
- **Kohorty, 60 dni przed i po starcie Meta na L4, kanał:** 54 komórki, kolorowe 53, istotnych 14 (18 w małych grupach).
- **Lejek, ustawienia domyślne (osoby, które jeszcze nie kupowały, przeglądarka, rok do roku):** 54 komórki, kolorowe 51, istotnych 21.
- **Lejek, 60 dni przed i po godzinie bez danych, przeglądarka:** 54 komórki, kolorowe 53, istotne 2.
- **Lejek, 60 dni przed i po awarii Safari, system i przeglądarka:** 138 komórek, kolorowe 136, istotnych 10 (36 w małych grupach).

Wniosek dla strony: kolor oznaczał tylko kierunek różnicy po zaokrągleniu, nie jej pewność. Przy porównaniach 60 dni przed i po i przy drobnych podziałach większość kolorów była szumem. Od rundy G kolor oznacza zmianę większą niż przypadek (założenia 87–88), a strona i Python dają ten sam wynik w każdej sprawdzonej komórce (`notatki/g_przejrzystosc.md`, punkt 5). Pozostałe zmiany są szare, z dopiskiem „bez wyraźnej zmiany”.
