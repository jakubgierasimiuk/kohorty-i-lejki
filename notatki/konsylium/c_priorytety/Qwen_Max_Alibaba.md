# Qwen Max (Alibaba) — qwen/qwen3.8-max-0902

# Ocena konsylium: kolejność działań

## Kryterium rankingu

Stosuję formułę: **(oczekiwana wartość × pewność kierunku) ÷ wysiłek wdrożenia**, z dodatkowym filtrem: działania blokujące inne decyzje dostają premię za efekt dźwigni. Pewność kierunku oceniam subiektywnie (0–1) na podstawie tego, ile niewiadomych stoi za szacunkiem.

---

## Ranking

| # | Pozycja | Szacowana wartość roczna | Pewność | Wysiłek | Uzasadnienie miejsca |
|---|---------|--------------------------|---------|---------|----------------------|
| 1 | **E** – Safari iPhone | 75–95 tys. zł | bardzo wysoka | dni | Jedyny punkt z twardym dowodem: spadek konwersji 66→46% tylko w jednej przeglądarce, od konkretnej daty, we wszystkich kanałach. Nawet przy 50% haircut (część pacjentów wróciłaby innym urządzeniem) to ~40–50 tys. zł przy zerowym ryzyku. |
| 2 | **K** – Pomiar | 0–38 tys. zł bezpośrednio; pośrednio: warunek poprawności wszystkich pozostałych decyzji | bardzo wysoka (problem istnieje na pewno) | 1–2 tyg. | Codzienny raport zawyża przychód o ~600 duplikatów i 2 071 zamówień testowych. Bez tego nie wiemy, czy kampanie realmente rosną, czy tylko raport kłamie. To nie jest „nice to have" – to fundament. |
| 3 | **A** – Zniżka u specjalistów | 14,7–31,4 tys. zł | bardzo wysoka (matematyka: cena < koszt) | 1–2 tyg. + 12 mies. pełnego efektu | Każda wizyta ze zniżką 20% u specjalisty (poza psychiatrą) generuje stratę. To nie jest hipoteza – to arytmetyka. Wdrożenie trywialne. |
| 4 | **B** – Wstrzymanie TikTok L4 | +11,9 do +30,8 tys. zł (minimum) | wysoka (ujemny wynik w obu regułach i obu horyzontach) | 1 dzień | Najtańszy eksperyment w całej liście: wyłączasz, mierzysz 4–6 tygodni, jeśli liczba pacjentów nie spada – zostawiasz wyłączone. Odwracalne w 1 dzień. |
| 5 | **C** – Wstrzymanie Google Ads na specjalistów | +19,4 do +31,5 tys. zł (minimum) | wysoka (ujemny w obu regułach) | 1 tydzień | CPA 57–81 zł przy marży pacjenta 32–37 zł. Żadna optymalizacja nie da 40–60% obniżki CPA w rozsądnym czasie. Wyłączyć, ewentualnie restartować z nową strukturą. |
| 6 | **D** – Zwroty po L4 | +12,7 do +57,1 tys. zł (reguła 1) | średnia (nie znamy powodu zwrotów) | 1–2 tyg. | Wartość realna, ale nakłada się z B (ci sami pacjenci TikToka). Jeśli B wyłączone, D dotyczy głównie pacjentów Meta. Wymaga diagnozy przyczyny – bez tego zmiana treści reklamy to strzał w ciemno. |
| 7 | **H** – Sesje zalogowane | 0 lub 36–89 tys. zł | niska–średnia | 1 dzień testu | Test ręczny kosztuje dzień. Jeśli to zepsuta ścieżka – wartość ogromna. Jeśli to „sprawdzam konto" – zero. Stosunek wartości do wysiłku uzasadnia szybki test. |
| 8 | **I** – Luka klik→sesja | 0 lub do 52 tys. zł | niska | 1–2 dni | Prawdopodobnie artefakt pomiarowy (Meta liczy kliknięcia inaczej niż Google). Sprawdzenie w panelach reklamowych rozstrzygnie w 1–2 dni. Jeśli to artefakt – zamykamy temat. |
| 9 | **F** – Meta L4 (test geo) | −27,8 do +163,3 tys. zł | bardzo niska (znak zależy od reguły) | 4–6 tyg. testu | Jedyna kampania, gdzie nie wiemy nawet, czy jest na plusie. Test geo jest poprawnym podejściem, ale wymaga czasu i dyscypliny w analizie. Nie podejmować decyzji bez testu. |
| 10 | **J** – Program zniżkowy a powroty | nieznana (test) | niska | 90 dni + koszt 3,3–12,2 tys. zł | Pytanie strategiczne: czy program dokłada wizyt, czy tylko subsydiuje pacjentów, którzy i tak wrócą. Odpowiedź zmienia model biznesowy, ale nie daje szybkiej marży. |
| 11 | **G** – Opóźnienia poranne | 0–65 tys. zł | bardzo niska | nieznany (brak danych o grafikach) | Bez danych o grafikach lekarzy i bez możliwości zmiany obsady nie da się nic zrobić. Najpierw trzeba zebrać dane – to nie jest akcja, to temat do zbadania. |

---

## Błędy i słabe założenia w wycenach

### E – Safari
Założenie „utracony pierwszy zakup = utracony pacjent" jest **zbyt pesymistyczne w jedną stronę i zbyt optymistyczne w drugą**:
- Część pacjentów mogła wrócić innym urządzeniem lub przeglądarką (zawyżenie straty).
- Ale jeśli pacjent nie mógł założyć konta, to nie zostawił danych → nie dostanie przypomnienia → prawdopodobieństwo powrotu bliskie zeru (zaniżenie straty w długim terminie).

Netto: szacunek 75–95 tys. jest rozsądny jako rząd wielkości, ale precyzja ±30%.

### A – Zniżka u specjalistów
Scenariusz „+31,4 tys. zł (wszystkie zostają po cenie katalogowej)" jest **nierealistyczny**. Pacjent, który kupił program za 89 zł po to, żeby płacić 87 zł zamiast 109 zł, nie zapłaci 109 zł – po prostu nie przyjdzie. Realistyczny scenariusz to +14,7 do +22 tys. zł.

### B – TikTok
Widełki „+11,9 do +82,5 tys. zł" są **myląco szerokie**. Górna granica (+82,5 tys.) zakłada, że żaden pacjent TikToka nie przyszedłby organicznie – to skrajnie nieprawdopodobne przy kampanii na tak generyczne zapytanie jak L4. Realistyczny szacunek: +15–40 tys. zł.

### D – Zwroty po L4
Brak powodu zwrotu to **krytyczna luka**. Jeśli powodem jest np. „pacjent dostał L4, ale chciał tylko receptę" – zmiana treści reklamy nie pomoże. Jeśli powodem jest „lekarz odmówił L4, ale system naliczył opłatę" – to bug produktowy. Bez tej wiedzy wycena jest spekulatywna.

### K – Pomiar
Wycena 37,95 tys. zł zakłada, że lekarze dostają 25 zł za wizytę testową. **To trzeba zweryfikować w ciągu 1 dnia** (zapytać księgowość lub sprawdzić przelewy). Jeśli nie dostają – bezpośrednia wartość wynosi 0, ale wartość pośrednia (poprawność decyzji) pozostaje.

### F – Meta L4
Widełki −27,8 do +163,3 tys. zł są **bezużyteczne decyzyjnie**. Rozpiętość 191 tys. zł przy braku jakiejkolwiek informacji o inkrementalności oznacza, że nie wiemy nic. Test geo jest jedyną drogą.

---

## Naprawiać czy wyłączać?

| Kampania | Rekomendacja | Uzasadnienie |
|----------|-------------|--------------|
| **TikTok L4** | **Wyłączyć natychmiast**, potem ewentualnie naprawiać i restartować | Ujemna w obu regułach, obu horyzontach. Nawet po naprawie zwrotów wynik to +3 tys. (reguła 1) lub −23 tys. (reguła 2). Nie ma scenariusza, w którym naprawa daje pewny zysk. Koszt Opportunity: każdy dzień działania to strata. |
| **Google Ads specjaliści** | **Wyłączyć**, nie naprawiać | Wymagana obniżka CPA o 40–60% jest nierealistyczna bez fundamentalnej zmiany strategii (nowe słowa kluczowe, nowy landing, inna oferta). To nie jest „naprawa" – to budowa od nowa. |
| **Meta L4** | **Nie wyłączać, testować** | Wynik dodatni w regule 1 (zgodnej z kodami rabatowymi w 97%). Wyłączenie bez testu ryzykuje utratę +27,8 tys. zł. Test geo jest tani i rozstrzygający. |

**Zasada ogólna:** jeśli kampania jest ujemna w *obu* regułach przypisania – wyłączamy. Jeśli jest ujemna tylko w jednej – testujemy.

---

## Brakujące działania

### 1. Rozstrzygnięcie reguły przypisania (blokuje B, D, F)
To nie jest osobna pozycja na liście, a powinno być. Bez decyzji, która reguła jest bliższa prawdy, trzy pozycje (B, D, F) mają nierozstrzygalny znak. Proponowany test: porównać kohorty pacjentów z kodem rabatowym (97% zgodności z regułą 1) z kohortami bez kodu – jeśli ich zachowanie jest podobne, reguła 1 jest lepszym proxy. Czas: 1–2 dni analizy.

### 2. Spadek powrotów z 23,9% do 17,4% – diagnoza
Brief mówi, że powrót spadł, ale nie ma żadnej pozycji, która bada *dlaczego*. Kampanie L4 tłumaczą część (ich pacjenci wracają w 4%), ale nawet po ich wyłączeniu powrót „organicznych" pacjentów mógł spaść. Warto rozbić kohorty na: (a) pacjenci z kampanii L4, (b) pacjenci z pozostałych kampanii, (c) pacjenci organiczni – i sprawdzić, czy spadek dotyczy wszystkich, czy tylko (a). Czas: 1–2 dni.

### 3. Renewal programu zniżkowego (5%)
Tylko 5% członków odnawia. Brief nie zawiera pozycji, która bada, dlaczego. Jeśli program jest rentowny (a pozycja J ma to zbadać), to wzrost renewal z 5% do 15% przy ~4 000 członków rocznie to dodatkowe ~900 × 89 zł = ~80 tys. zł przychodu (nie marży – trzeba odjąć koszt zniżek). Brak tej pozycji na liście to luka.

### 4. Komunikacja po wizycie (retencja)
Brak danych o newsletterach i SMS-ach, ale sam fakt, że ich nie mierzymy, jest problemem. Jeśli firma nie wysyła żadnej komunikacji po wizycie (np. „jak się czujesz?", „przypomnienie o kontroli"), to jest to najtańszy możliwy eksperyment retencyjny. Koszt: ~0 zł (e-mail), czas: 1 tydzień.

### 5. Analiza sezonowości
III kwartał 2026 to −6,8% rdr. Ale III kwartał to lato – sezonowo niski popyt na konsultacje. Czy spadek jest sezonowy, czy strukturalny? Bez danych za III kwartał 2024 (których brief nie podaje wprost, ale można wyliczyć z danych rocznych) nie da się tego rozstrzygnąć. To wpływa na interpretację wszystkich trendów.

---

## Czego nie wiem na pewno

1. **Czy lekarze dostają wynagrodzenie za wizyty testowe** – to zmienia wartość pozycji K z 0 na 38 tys. zł.
2. **Jaka jest cena katalogowa wizyt u specjalistów** – brief podaje przykład 87,2 zł po zniżce, ale nie podaje pełnego cennika. Bez tego nie mogę zweryfikować, czy scenariusz A jest poprawnie policzony.
3. **Czy spadek powrotów z 23,9% do 17,4% jest w całości wyjaźniony przez kampanie L4** – jeśli kampanie dają 29% nowych pacjentów z powrotem 4%, to „organiczny" powrót powinien wynosić ~22,8% (ważony). Skoro ogólny to 17,4%, to albo organiczni też spadli, albo proporcje są inne niż zakładam.
4. **Jaki jest zespół techniczny firmy** – „wdrożenie: dni" dla Safari zakłada, że ktoś potrafi zdiagnozować i naprawić bug w przeglądarce. Jeśli firma nie ma developera front-end, czas rośnie do tygodni.
5. **Czy istnieje jakakolwiek komunikacja retencyjna** (e-mail, SMS, push) – brief mówi, że nie ma danych o wysyłkach, ale nie mówi, czy one w ogóle istnieją.

---

## Podsumowanie w jednym zdaniu

**Zacznij od E (Safari) i K (pomiar) w tym samym tygodniu, potem A i wyłączenie B/C w drugim tygodniu – to daje łącznie 110–160 tys. zł rocznej marży przy pewności >80% i wysiłku <3 tygodni; reszta wymaga testów i danych, których jeszcze nie mamy.**
