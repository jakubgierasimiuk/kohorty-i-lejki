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
