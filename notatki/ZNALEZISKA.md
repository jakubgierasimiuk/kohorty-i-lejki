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

- **Kod rabatowy `TEST-QA` w 1 810 zamówieniach.** Wygląda na zamówienia testowe zespołu jakości w danych produkcyjnych. Do sprawdzenia: kiedy występują, jakie mają kwoty i statusy, czy trzeba je wyłączyć z przychodu i z kohort.
- **Źródło `bing` (3 944 sesje) nie ma kosztów w `marketing_spend.csv`.** Do sprawdzenia, czy to ruch bezpłatny (`organic`), czy brakujący koszt kampanii.
- **Dwie kampanie mają koszty tylko przez część okresu:** `meta_prosp_l4_szybko` przez 332 dni i `tt_prosp_l4_15min` przez 234 dni, wobec 730 dni pozostałych. To kandydaci na zdarzenia (start kampanii) do odczytania z danych.
