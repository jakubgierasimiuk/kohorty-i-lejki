# Qwen Max (Alibaba) — qwen/qwen3.8-max-0902

# Weryfikacja rozwiązania zadania rekrutacyjnego Telemedi B2C

## 1. Lista poprawek od najważniejszej

### 1.1. Rozbieżność liczb L4 „z pozostałych kanałów" między zakładką „Czy to wzrost" a raportem

- **Waga:** ważna
- **Miejsce:** zakładka „Czy to wzrost", sekcja „Lepsza retencja: nie", zdanie o L4; raport `a5r_kohorty.txt` → E1 (W2), wiersz `internista_l4`
- **Co jest nie tak:** Zakładka podaje: „pacjenci z pierwszym L4 z pozostałych kanałów wracają w 13,9% (2 797 pacjentów) wobec 14,8% (2 639)". Raport E1 (W2) dla `internista_l4` bez nowych kampanii: okres 1 = 14,6% (2 795), okres 2 = 13,8% (2 969). Różnice: 14,8 vs 14,6; 2 639 vs 2 795; 13,9 vs 13,8; 2 797 vs 2 969.
- **Dowód:** E1 W2: `internista_l4 14.6 13.8 2795 2969`. Zakładka: „13,9% (2 797) wobec 14,8% (2 639)".
- **Propozycja:** Sprawdzić, czy zakładka nie stosuje dodatkowego filtra (np. wyklucza jeszcze jeden kanał). Jeśli tak — nazwać go w tekście. Jeśli nie — poprawić liczby na zgodne z raportem.

### 1.2. Różnica w liczbach porannych opóźnień między „Po zakupie" a „Priorytetami"

- **Waga:** ważna
- **Miejsce:** zakładka „Po zakupie", nagłówek sekcji „Punktualność"; zakładka „Priorytety", pozycja 6, akapit „Z danych"
- **Co jest nie tak:** „Po zakupie" (filtr: spoza nowych kampanii): „15,7% w XI 2025 (521 wizyt), 29,7% w XII, 42,6% w I 2026 i 47,3–52,7% od II do IX 2026". „Priorytety" poz. 6: „15,6% w listopadzie 2025 (572 wizyty), 29,7% w grudniu i 41,8% w styczniu 2026, a od lutego do września 2026 około połowy (48,4–52,6%)". Różnice: 15,7 vs 15,6%; 521 vs 572 wizyt; 42,6 vs 41,8%; 47,3–52,7 vs 48,4–52,6%.
- **Dowód:** Cytaty powyżej. „Po zakupie" deklaruje filtr „Spoza nowych kampanii"; „Priorytety" nie podaje wprost filtra dla tych liczb (dla okresu bazowego pisze „wszyscy pacjenci").
- **Propozycja:** Ujednolicić: albo obie zakładki pokazują „spoza nowych kampanii", albo „Priorytety" podają, że liczby dotyczą wszystkich pacjentów. Najprawdopodobniej 572 vs 521 to różnica między „wszyscy" a „spoza nowych kampanii" — wtedy dodać etykietę.

### 1.3. Dwa okna pomiaru awarii Safari — różne liczby w różnych zakładkach

- **Waga:** drobna
- **Miejsce:** zakładka „Lejek" i „Zdarzenia" (60 dni przed/po: 66,2% → 45,1%, 1 763 i 1 553 sesje) vs zakładka „Priorytety" poz. 1 (pełny okres: 66,1% → 45,6%, 4 678 sesji po)
- **Co jest nie tak:** Czytelnik, który nie zauważy różnicy okien, może uznać to za błąd. Obie wartości są poprawne, ale różnica nie jest wyjaśniona w jednym miejscu.
- **Dowód:** „Lejek": „66,2% (1 763 sesje, 16.01–16.03.2026) do 45,1% (1 553 sesje, 17.03–15.05.2026)". „Priorytety": „66,1% do 45,6% (od 1.10.2025 do 16.03.2026 wobec 17.03–30.09.2026; po awarii 4 678 sesji)".
- **Propozycja:** W zakładce „Priorytety" dodać jedno zdanie: „Okno 60 dni (lejek, zdarzenia): 66,2% → 45,1%; pełny okres (tu): 66,1% → 45,6%". Albo w „Zdarzeniach" dopisać pełny okres obok 60-dniowego.

### 1.4. Zaokrąglenia w raportach vs zakładkach

- **Waga:** drobna
- **Miejsce:** raport E1 (W3): `zmiana_proc` = 45.0, 48.0, 27.0, 77.0, 0.0; zakładki: 44,8%, 47,6%, 26,6%, 76,7%, 0,2%
- **Co jest nie tak:** Raport zaokrągla do pełnych procentów, zakładki do jednego miejsca po przecinku. Ktoś porównujący raport z zakładką może pomyśleć, że to błąd.
- **Dowód:** 998 076 / 2 230 266 = 44,75% → zakładki: 44,8%; raport: 45.0. Analogicznie dla pozostałych.
- **Propozycja:** Albo zmienić format raportu na jedno miejsce po przecinku, albo dodać w README uwagę: „Raporty zaokrąglają do pełnych procentów; zakładki do 0,1 pp".

### 1.5. „Wzrost o 7–20%" w README — brak precyzji

- **Waga:** drobna
- **Miejsce:** README, sekcja „Więcej pacjentów: tak"
- **Co jest nie tak:** „Poza tymi kampaniami nowych pacjentów przybyło o 7–20%, zależnie od reguły przypisania źródła." Zakładka „Czy to wzrost" podaje dokładne wartości: +7,3% (Z1K) i +20,1% (Z2). README zaokrągla do „7–20%", co jest poprawne, ale mniej precyzyjne.
- **Dowód:** E1 W1: bez_nowych_z1k +7.3%, bez_nowych_z2 +20.1%.
- **Propozycja:** Zostawić jak jest (README to podsumowanie) albo podać dokładne wartości. Nie jest to błąd.

---

## 2. Co się potwierdziło

### Liczby zgodne we wszystkich miejscach (zakładki, README, notatki, raporty):

| Miara | Wartość | Źródła |
|---|---|---|
| Nowi pacjenci okres 1 / okres 2 | 16 231 / 24 687 (+52,1%) | B, C (3 zakładki), D, E1 |
| Powrót w 90 dniach (te same dni) | 23,9% (12 867) → 17,4% (18 924) | B, C, D, E1, E2 |
| Marża na pacjenta w 90 dniach | 66,6 → 58,3 zł | B, C, D, E1, E2 |
| Zamówienia oczyszczone | 24 716 → 38 491 (+55,7%) | B, C (4 zakładki), D, E2 |
| Przychód po zwrotach | 2 230 266 → 3 228 342 (+44,8%) | B, C, D, E1 |
| Marża całkowita | 828 085 → 1 048 069 (+26,6%) | B, C, D, E1 |
| TelemediGO | 1 759 → 2 468 (+40,3%) | B, C, D, E7 |
| Marża Q3 2026 vs Q3 2025 | 207 713 vs 222 824 (−6,8%) | B, C, D, E1 |
| Wydatki Q3: iloraz | 2,08× | B, C, E1 |
| Duplikaty zamówień | 604, okno 10–24.06.2026 | B, C, D, E4 |
| Konta testowe | 22 konta, 2 071 zamówień | B, C, D |
| Utracone zamówienia Safari | 628–695 w 198 dni | C (3 zakładki), E4 |
| Zwroty L4 nowe kampanie | 17,4% (1 024 z 5 895) vs 5,3% (270 z 5 080) | C, D |
| Koszt pozyskania nowe kampanie (Z1K) | 32,7 zł | C, E6 |
| Wynik nowe kampanie Z1K 90d | +3,6 zł/pac | C, E6 |
| Wynik TikTok Z1K/Z2 90d | −4,6 / −17,8 zł/pac | C, E6 |
| gs_generic_specjalisci Z1K/Z2 90d | −23,7 / −44,7 zł/pac | C, E6 |
| TelemediGO: opłata vs zniżka (okres 1) | −27 388 zł (−15,57 zł/członkostwo) | C, E7 |
| Prowizja afiliacyjna | 15 400 → 15 425 zł | C, E1 |
| Liczba powracających w 90 dniach | 3 076 → 3 289 (+6,9%) | B, C, E1 |
| Mostek dashboard → oczyszczone | wszystkie 4 kroki | C (2 zakładki), D |

### Definicje poprawne i spójne:

- **Nowy pacjent:** pierwsze opłacone zamówienie, dowolny status — spójne z definicją dashboardu i słownikiem danych. Warianty odrzucone policzone i pokazane. ✓
- **Powrót:** kolejne nieanulowane zamówienie — logiczne (anulacja = pełny zwrot przed wizytą). ✓
- **Źródło pozyskania (przyjęta reguła):** pierwsze wejście + kod kampanii rozstrzyga — zgodność z kodami 96,6–97,0%, najwyższa spośród wariantów. ✓
- **Przychód po zwrotach:** `amount_paid − refund_amount`, zwrot w dniu płatności (brak daty zwrotu w danych) — założenie nazwane. ✓
- **Marża na pacjenta:** przychód po zwrotach + GO − koszt lekarza, przed kosztem pozyskania — spójna we wszystkich zakładkach. ✓
- **Koszt lekarza:** 25 zł internista, 200 zł psychiatra, 100 zł pozostali (w tym pediatra) — zgodne z zadaniem; założenie o pediatrze nazwane i policzone w wariancie alternatywnym. ✓
- **Porównanie na tych samych dniach kalendarzowych:** okres 1 obcinany do tej samej długości co dojrzała część okresu 2 — poprawne i jasno opisane. ✓
- **Przeliczenie na pełny rok:** TikTok × 1,56 (234 dni), Meta × 1,10 (332 dni) — 365/234 = 1,560 ✓; 365/332 = 1,099 ✓.

### Wnioski, które nie przekraczają danych:

- „To nie jest wzrost" — poparte spadkiem retencji w każdym oknie. ✓
- „Spadła poranna przepustowość" — nazwane „odczytaniem", bez przesądzania przyczyny, z listą alternatyw. ✓
- „Lekarz nie wystawia L4, którego pacjent oczekuje" — nazwane „możliwym odczytaniem". ✓
- Rozkład spadku na nowe/stare kampanie — nazwany „opisowym, nie zmierzonym wpływem". ✓
- Wartości priorytetów jako scenariusze i zakresy, nie punktowe prognozy. ✓

---

## 3. Ocena z perspektywy zlecającego

### Trzy najmocniejsze strony

1. **Jednoznaczna, odważna odpowiedź na pytanie zadania.** „Nie, to nie jest wzrost" — z pełnym rozbiciem na oba warunki, z zastrzeżeniami i z mostkiem od dashboardu do danych oczyszczonych. Kandydat nie unika konkluzji, ale też nie przesądza przyczyn. To dokładnie to, czego oczekuje firma, która pyta „czy to, co widać na dashboardzie, jest wzrostem".

2. **Zdarzenia znalezione w danych bez podanej listy.** 13 zdarzeń na osi czasu, każde z datą, wielkością zmiany i metodą wykrycia. Wymaganie zadania („listy zmian nie dostajecie — zdarzenia trzeba znaleźć w danych") jest spełnione w pełni, z nadwyżką: kandydat pokazuje też surowy wynik metody (245 kandydatów) i wyjaśnia, które odrzucił i dlaczego.

3. **Lista priorytetów z wartością w marży, sposobem pomiaru i czasem wdrożenia.** 12 pozycji, każda z kwotą (lub scenariuszem), miarą sukcesu i szacunkiem czasu. Przy kampaniach — obie drogi (naprawić albo wyłączyć) z wariantami dodatkowości. Zasada budżetu („nie przesuwamy automatycznie") pokazuje dojrzałość biznesową.

### Trzy najsłabsze strony

1. **Objętość i próg wejścia.** Dziewięć zakładek, 12 priorytetów, 18 niewiadomych, dziesiątki tabel i wykresów. Osoba czytająca to pierwszy raz potrzebuje dużo czasu, żeby znaleźć odpowiedź na konkretne pytanie. README pomaga, ale samo narzędzie nie ma „ścieżki szybkiego czytania" (np. 3-minutowego podsumowania na pierwszej zakładce).

2. **Dwie reguły źródła jako stały motyw.** Niemal każda liczba kampanii jest podana w dwóch wariantach (Z1K i Z2). To uczciwe, ale dla czytelnika, który chce jednej odpowiedzi, jest frustrujące. Przydałoby się jedno zdanie na początku: „Gdybyśmy musieli wybrać jedną regułę, wybralibyśmy Z1K, bo zgadza się z kodami w 97% przypadków" — takie zdanie pada w założeniach, ale nie w samym narzędziu.

3. **Brak wizualnego „dashboardu wykonawczego".** Zadanie mówi „narzędzie, na którym da się prowadzić biznes na co dzień". Obecne narzędzie jest analityczne (kohorty, lejki, zdarzenia), ale nie ma widoku „dziś rano patrzę na te 5 liczb i wiem, czy jest dobrze". To drobnostka, bo zadanie nie wymaga dashboardu operacyjnego, ale osoba prowadząca biznes chciałaby taki widok.

### Czego brakuje wobec zadania

| Wymaganie | Status |
|---|---|
| Kohorty dzienne, pocięte tak, żeby było widać co się wydarzyło | ✓ (wykres dzienny z wygładzeniem, macierz kohort, krzywa powrotu, filtry, podział na serie) |
| Zdarzenia znalezione w danych | ✓ (13 zdarzeń + surowa lista 245 kandydatów) |
| Lejki: gdzie i od kiedy tracimy pacjentów | ✓ (lejek z podziałami, wykres czasowy, sesje zalogowane i GO osobno) |
| Narzędzie działające z linku, bez instalacji | ✓ (GitHub Pages, statyczne pliki, bez konta) |
| Priorytety z wartością, pomiarem, czasem | ✓ (12 pozycji, każda z trzema elementami) |
| Czego nie da się rozstrzygnąć | ✓ (18 pozycji z testem przy każdej) |
| Ślad pracy | ✓ (repozytorium z historią, notatki, recenzje, konsylium) |

Braków względem wymagań nie widzę. Jedyna rzecz, której nie da się ocenić z załączników, to czy narzędzie faktycznie działa i czy wykresy są czytelne — tego tekst nie pokaże.

### Decyzja

**Przyjąłbym kandydata.**

**Na plus przesądza:**
- Odpowiedź na pytanie zadania jest jasna, odważna i dobrze udokumentowana.
- Poziom rygoru analitycznego (dwie reguły, scenariusze, zastrzeżenia, testy) jest wyższy niż typowy dla kandydatów na stanowisko Head of Sales. To osoba, która nie podejmie decyzji na złych danych.
- Znalezienie błędów w danych (duplikaty, testy, awaria Safari) i pokazanie ich wpływu na dashboard to dokładnie to, czego firma potrzebuje od osoby prowadzącej biznes na kohortach.
- Proces pracy (defin
