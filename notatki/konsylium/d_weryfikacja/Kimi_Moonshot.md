# Kimi (Moonshot) — moonshotai/kimi-k3

# Weryfikacja rozwiązania — opinia konsylium

## 1. Lista poprawek (od najważniejszej)

### Poprawka 1 — ważna — niespójność zmiany powrotu w 180 dniach między zakładkami
- **Miejsce:** zakładka „Kohory" (C, tabela „Kohorty w podziale", wiersz „Wszyscy w filtrze", kolumna „Powrót w 180 dniach") wobec zakładki „Czy to wzrost" (tabela retencji).
- **Co jest nie tak:** w „Kohortach" stoi „22,2% z 12 591 / A: 27,5% z 9 125 **▼5,2**", a w „Czy to wzrost" ta sama para to „**−5,3 pkt proc.**".
- **Dowód:** 27,5 − 22,2 = **5,3**. Załącznik E2 (sekcja 1b) potwierdza: „powrot_zmiana_pkt -5.3" dla okna 180.
- **Poprawka:** zmienić ▼5,2 na ▼5,3 na stronie i sprawdzić, czemu skrypt eksportu nie złapał różnicy (README twierdzi, że `b_eksport.py` „sprawdza liczby na stronie z raportami").

### Poprawka 2 — ważna — dwie różne liczby dla awarii Safari bez wyjaśnienia różnicy
- **Miejsce:** zakładka „Lejek" i zdarzenie 12 (66,2% → 45,1%, okna 60 dni: 1 763 i 1 553 sesje) wobec karty priorytetu 1 (66,1% → 45,6%, okres 1.10.2025–16.03.2026, 4 678 sesji).
- **Co jest nie tak:** czytelnik widzi dla „tego samego" kroku dwie pary liczb (66,2/45,1 i 66,1/45,6) w dwóch miejscach narzędzia. Priorytet 1 nie pisze, że używa dłuższego okna bazowego.
- **Dowód:** C, zakładka Lejek: „spadł z 66,2% … do 45,1%"; C, priorytet 1: „spada z 66,1% do 45,6%". E4 sekcja 5f potwierdza wariant 66,1/45,6 (okres 1.10–16.03).
- **Poprawka:** w priorytecie 1 dopisać jedno zdanie: „liczone na dłuższym oknie bazowym niż w zakładce Lejek, stąd 66,1/45,6 zamiast 66,2/45,1; wniosek identyczny".

### Poprawka 3 — ważna — data „2026-10-21" w raporcie z 2026-10-20
- **Miejsce:** E1, nagłówek W4: „(dopisek kandydata **2026-10-21**; zł)" — raport `c_priorytety.txt` ma datę generacji 2026-10-20 14:32, a DECYZJE.md datuje dopisek o marży kwartalnej na 2026-10-20.
- **Co jest nie tak:** data w przyszłości w śladzie pracy; wygląda jak literówka, ale w repozytorium oddawanym firmie osłabia wiarygodność metki czasowej.
- **Poprawka:** poprawić datę na 2026-10-20 i przeliczyć nagłówek.

### Poprawka 4 — ważna — rozbieżność liczb opóźnień w XI 2025 między zakładką a priorytetem
- **Miejsce:** zakładka „Po zakupie": „15,7% w XI 2025 (**521 wizyt**)" wobec priorytetu 6: „15,6% w listopadzie 2025 (**572 wizyty**)".
- **Co jest nie tak:** różne liczebności (521 vs 572) i odsetki (15,7 vs 15,6) dla pozornie tej samej statystyki. Priorytet ma dopisek „(wszyscy pacjenci)", „Po zakupie" filtr „Spoza nowych kampanii" — ale w tekście „Po zakupie" zdanie brzmi „u pacjentów spoza nowych kampanii", a w priorytecie „wszyscy pacjenci", więc to zapewne dwie różne grupy. Bez nazwania tego czytelnik odbiera to jako błąd.
- **Dowód:** cytaty powyżej (C). E5 pokazuje trzecią serię (24.11–25.12: 615 wizyt, 27,8%) — trzy różne liczby dla „listopadowych opóźnień" w trzech miejscach.
- **Poprawka:** ujednolicić okna i filtry albo explicite podpisać każdą wersję (grupa pacjentów × definicja miesiąca). To akurat obszar, który firma będzie drążyć, bo z niego wynika priorytet 6.

### Poprawka 5 — ważna — liczby priorytetu 4 nie do sprawdzenia z raportów w załącznikach
- **Miejsce:** karta priorytetu 4: „Rocznie **923** nowych pacjentów według przyjętej reguły, **657** według sesji płatności, wydatki **53,2 tys. zł**".
- **Co jest nie tak:** E6 pokazuje dla `gs_generic_specjalisci` w oknie 90 dni 719/519 pacjentów i wydatki 40 319 zł; liczb rocznych (923/657) nie ma w żadnym załączonym raporcie. Nie da się zweryfikować przeliczenia na pełny rok ani wariantów wyłączenia (+19,4 do +53,2 tys.).
- **Poprawka:** dopisać w raporcie `c_priorytety.txt` (P7) jawne przeliczenie rocznika tej kampanii. Zaznaczam: nie twierdzę, że liczby są błędne — twierdzę, że nie da się ich sprawdzić z załączników.

### Poprawka 6 — drobna — zaokrąglenia w E1 zacierają dokładność
- **Miejsce:** E1 W3: kolumna „zmiana_proc" pokazuje 45.0, 48.0, 27.0, 77.0, podczas gdy wszędzie indziej (strona, README, D) są 44,8%, 47,6%, 26,6%, 76,7%.
- **Poprawka:** jedno miejsce po przecinku w raporcie; teraz raport wygląda na niespójny z resztą, choć jest tylko mniej precyzyjny.

### Poprawka 7 — drobna — założenie 19 nieaktualne po rozszerzeniu okien
- **Miejsce:** D, ZALOZENIA.md pkt 19: powrót liczony „w oknach 30, 60 i 90 dni" — tymczasem analiza i strona liczą też 180 dni (i wspominają 270).
- **Poprawka:** dopisać okno 180 do założenia 19 (kwestia porządkowa w śladzie pracy).

### Poprawka 8 — drobna — „każdy pacjent kupuje w ciągu 30 dni" bez pokrycia
- **Miejsce:** D, założenie 22: „75,1% tego samego dnia, 24,6% w ciągu 1–7 dni" = 99,7% — pozostałe 0,3% kupuje w 8–30 dni, ale zdanie „Każdy pacjent kupuje w ciągu 30 dni od pierwszego wejścia" jest mocniejsze niż pokazane liczby.
- **Poprawka:** dopisać rozkład do 30 dni albo złagodzić zdanie.

## 2. Co się potwierdziło (przeliczone z załączników)

- **Wzrost nowych pacjentów:** 24 687/16 231 = **+52,1%** ✓; bez nowych kampanii: 17 419/16 231 = +7,3% i 19 500/16 231 = +20,1% ✓; kanały bezpłatne 7 924/7 069 = +12,1% ✓.
- **Marża okresów (W3):** 2 230 266 + 156 551 − 1 175 700 − 367 632 − 15 400 = **828 085 zł** ✓; okres 2: 3 228 342 + 219 652 − 1 734 825 − 649 675 − 15 425 = **1 048 069 zł** ✓ (+26,6% ✓). Korekty startu od zera: 1 048 069 − 152 960 = 895 109 (+8,1% ✓), −41 474 = 853 635 (+3,1% ✓).
- **Mostek dashboardu:** 40 613 − 604 = 40 009; −1 518 = 38 491; 25 269 − 553 = 24 716; 38 491/24 716 = **+55,7%** ✓. Duplikaty i testy spójne w B, C, D, E.
- **Przychód po zwrotach:** 3 228 342/2 230 266 = +44,8% ✓; przed zwrotami 3,508/2,375 = +47,7% ✓.
- **Rozkład spadku lejka:** −3,00 (struktura) + 0,67 (konwersja) = −2,33 pkt ✓ zgodne z E3 sekcją 4.
- **Rozkład procentowy spadku powrotu:** 4,6/6,5 = 70,8% i 3,0/6,5 = 46% — zakres „46–71%" w zakładce „Czy to wzrost" ✓.
- **Próg decyzji priorytetu 9:** interpolacja liniowa między −30,6 (100% dodatkowych) a +179,6 tys. zł (0%) daje próg 30,6/210,2 → **85,4%** — dokładnie jak na stronie ✓.
- **Priorytet 7:** 24 687 × 1% × 95,6 zł = 23 600 ≈ 23,6 tys. zł ✓.
- **Priorytet 1:** 1 158–1 281 pacjentów × 64,6 zł = 74,8–82,7 tys. zł ≈ podane 75–83 tys. ✓.
- **TelemediGO:** 905/16 231 = 5,58% i 1 089/24 687 = 4,41% ✓; udział nowych kampanii 7 268/24 687 = 29,4% ✓; spadek III kw.: 222 824 − 207 713 = 15 111 zł ✓; ×1,56 przeliczenia TikToka (−11,9 → −18,6) ✓.
- **Definicje:** nowy pacjent, powrót (nieanulowane), koszt lekarza za wizyty zwrócone (zgodnie z zadaniem), prowizja 25 zł bez względu na status, czas polski z obsługą zmiany czasu (sprawdzone 65 278/65 278 co do sekundy) — wszystkie zgodne z treścią zadania i nazwane jako założenia.

## 3. Ocena z perspektywy zlecającego

**Trzy najmocniejsze strony:**
1. **To jest narzędzie do prowadzenia biznesu, nie raport.** Kohorty dzienne z pełnym oknem, 12 filtrów, dwie reguły atrybucji obok siebie, macierz z oznaczeniem niedojrzałych kohort, lejek z rozbiciem struktury na konwersję — dokładnie to, o co prosił punkt 3 zadania.
2. **Dyscyplina „wniosek nie mówi więcej niż dane".** Wszędzie, gdzie znak zależy od reguły, wynik jest nazwany niepewnym; scenariusze są nazwane scenariuszami z wariantem 0 zł; „wyłączyć albo naprawić" ma rachunek w obie strony. Lista 18 niewiadomych z testem przy każdej to najlepszy fragment pracy wobec punktu 5 zadania.
3. **Odtworzenie dashboardu i mostek do danych czystych.** Kandydat nie tylko odpowiedział „nie, to nie wzrost", ale pokazał, skąd biorą się liczby z dashboardu (duplikaty, testy, zwroty, start od zera) i udowodnił to siatką 864 kombinacji definicji.

**Trzy najsłabsze strony:**
1. **Gęstość i objętość.** Dziewięć zakładek z tysiącami liczb; odpowiedź „nie" jest właściwa, ale pierwszy czytelnik potrzebuje 15 minut, żeby ją znaleźć w szczegółach. Brak jednego ekranu „5 liczb, które musisz zapamiętać".
2. **Drobne niespójności liczbowe właśnie tam, gdzie kandydat deklaruje automatyczną kontrolę spójności** (▼5,2 vs −5,3; trzy wersje opóźnień listopadowych; dwie wersje Safari). Pojedynczo drobne, razem podważają hasło „każda liczba sprawdzona skryptem".
3. **Macierz kohort domyślnie tygodniowa**, choć zadanie wymaga rozdzielczości dziennej jako serca pracy. Wykres dzienny jest, ale macierz — najbardziej „kohortowy" element — startuje w tygodniach.

**Czego brakuje wobec zadania:** jawnego, krótkiego powiązania każdego priorytetu z konkretnym zdarzeniem z osi (jest pośrednio, ale firma prosiła „które zdarzenie zmieniło zachowanie i wynik"); analizy wrażliwości decyzji o koszcie pediatry (jest wariant 25 zł w założeniach, ale nie w narzędziu); wyraźnego zaznaczenia, że 29% wzrostu pacjentów to jedna decyzja marketingowa (dwie kampanie), co jest najważniejszym strategicznym faktem z danych.

**Decyzja: zatrudniłbym / zaprosiłbym do ostatniego etapu.** Na plus przesądza: poprawna odpowiedź na główne pytanie z pełnym rachunkiem, jakość definicji i obsługa niepewności na poziomie, jakiego rzadko się widuje, oraz ślad pracy, w którym widać korekty po recenzjach (m.in. wycofanie zbyt mocnego zdania o sezonie). Na minus: drobne niespójności prezentacji w miejscach, gdzie kandydat sam zadeklarował automatyczną kontrolę, oraz próg wejścia w materiał. To są wady redakcyjne, nie analityczne — a rola jest analityczno-operacyjna.

## Czego nie dało się sprawdzić z załączników

Poprawności kodu i odwzorowania liczb z bazy (to sprawdzają dwaj członkowie zespołu z dostępem do plików), wyglądu i działania wykresów, treści skróconych tabel, liczb rocznika kampanii `gs_generic_specjalisci` (poprawka 5) oraz tego, czy narzędzie faktycznie otwiera się z linku (link w README jest jeszcze placeholderem — **to trzeba domknąć przed wysyłką, inaczej praca nie spełnia twardego wymagania z tabeli „Co oddajemy"**).
