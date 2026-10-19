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

**W skrócie: tracimy pacjentów w dwóch miejscach, które trzeba naprawić na stronie: w przeglądarkach wbudowanych w aplikacje i w zakładaniu konta w Safari na iOS od 17.03.2026. Rachunkowo prawie cały spadek konwersji lejka to zmiana struktury ruchu. Ten ruch traci jednak na każdym kroku, więc to nie jest tylko „inny ruch” (dopisek Kuby).**

1. **Konwersja sesji do płatności spadła z 16,0% w okresie 1 do 13,7% w okresie 2.** Rachunkowo prawie cały spadek to większy udział przeglądarek wbudowanych w aplikacje Instagram, Facebook i TikTok: z 10,7% do 35,6% sesji, głównie z reklam Meta i TikToka. Te przeglądarki płacą w 5–7% sesji, a Chrome i Safari w 16–18%. Tracą na każdym kroku lejka, także na zakładaniu konta.
2. **Zdarzenie 17.03.2026: w Safari na iPhone'ach i iPadach przestaje działać zakładanie konta.** Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spada z 66,2% do 45,1% i zostaje na tym poziomie do końca danych. Inne przeglądarki tego nie mają. Spadek jest w każdym kanale, więc to nie zmiana struktury. Psuje się zakładanie nowego konta, a logowanie do istniejącego działa. Szacunek: około 95–105 utraconych pierwszych zamówień na 30 dni, razem 628–695 od 17.03 do 30.09.2026. Przyczyny w danych nie widać.
3. **Starty kampanii jako zdarzenia:** Meta na L4 od 3.11.2025 (płaci w lejku lepiej niż starsza kampania Meta, ale 2–3 razy rzadziej niż wyszukiwarka; strona `/zwolnienie-l4-online` traci na konwersji tylko przez ten ruch), TikTok od 9.02.2026, sprzedaż TelemediGO w newsletterze od 8.09.2025 (686 zakupów samego TelemediGO).
4. **Remarketing Meta słabnie od początku 2026 przez zmianę puli odbiorców.** Płatność spada z 28,2% sesji w IV kwartale 2025 do około 19% w II i III kwartale 2026. W obrębie źródła, z którego osoba trafiła na stronę pierwszy raz, konwersja stoi.
5. **Sesje zalogowane od wejścia: dane nie rozstrzygają między odczytaniami.** Przeciw „zepsutej ścieżce, która odbiera nam zakupy” przemawiają trzy rzeczy: pacjenci odpadają przed krokiem konta, a nie na nim; pacjenci z takimi sesjami wracają częściej niż podobni bez nich; krok konta w zakupach powtórnych trwa kilkadziesiąt sekund, a nie 1–2 sekundy. Zostaje mocna niespójność ze słownikiem danych: według niego zalogowany pacjent nie ma kroku konta, a w danych ma go każdy zakup. Po pierwszym zakupie pacjent nie ma ani jednej anonimowej sesji, a rozkład odstępów między krokami w zakupach powtórnych jest jednakowy. To wygląda na cechę generatora danych.
6. **Sezon a wydatki: przyczyny wzrostu nowych pacjentów od X 2024 do I 2025 nie da się rozdzielić.** W kanałach opartych na wyszukiwaniu (bezpłatnym i płatnym) widać wyraźny sezon: zimą więcej nowych pacjentów niż latem. Wydatki rosły jednak w tych samych miesiącach. Kampania Meta z prawie stałym budżetem ma co najwyżej słaby sezon (+8% pacjentów zimą przy +5% wydatków).
7. **Strata między kliknięciem reklamy a sesją w Meta i TikToku** (dopisek Kuby). Na kliknięcie przypada 0,92–0,93 sesji w Google Ads, 0,79–0,82 w Meta i 0,72 w TikToku, stale w każdym kwartale. Trzy odczytania: porzucenie przed załadowaniem strony, luka w śledzeniu w przeglądarkach wbudowanych albo inne liczenie kliknięć przez platformy. W remarketingu Meta przeglądarek wbudowanych jest mało, a stosunek jest ten sam, co bardziej pasuje do liczenia kliknięć. Górna granica w okresie 2: 23 776 sesji, do 1 434 zamówień i 50 494 zł wydatków.
8. **Co nie jest zdarzeniem:** wzrost konwersji w pierwszym roku (dorastanie bazy powracających), spadki kroku konta z 5–12.02.2026 (ten sam problem Safari na iOS plus zmiana struktury) i spadek wyboru usługi wiosną 2026 (zmiana struktury). Kroki płatności są stabilne w każdym podziale.
