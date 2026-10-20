# C — szkic na poranny przegląd Kuby (sesja prowadząca, 2026-10-20)

**Status:** szkic. Nic tu nie jest wnioskiem, dopóki Kuba go nie przyjmie. Zakres: `DECYZJE.md`, wpis z 2026-10-20 o nowej sesji prowadzącej.

**Pliki:**

| Plik | Co zawiera |
|---|---|
| `analiza/c_telemedigo.py` → `analiza/wyniki/c_telemedigo.txt` | TelemediGO: skąd wzrost sprzedaży, opłaty wobec zniżek, zniżki wobec kosztu lekarza, powroty z kontrolami samoselekcji i projektem testu. Zestawienia miesięczne dla narzędzia: `c_telemedigo_miesiace.csv` i `c_telemedigo_miesiace_znizki.csv`. |
| `analiza/c_priorytety.py` → `analiza/wyniki/c_priorytety.txt` | W1–W3: liczby do odpowiedzi „czy to wzrost” (nowi pacjenci, powroty, marża na pacjenta, wynik biznesu). P1–P10: wartość pozycji listy priorytetów. Liczby przepisane z wcześniejszych raportów skrypt sprawdza w tych raportach (funkcja `z_raportu`). |
| `notatki/recenzje/c_codex_*.md` | Recenzja Codeksa (model Sol): polecenie, odpowiedź, podsumowanie. |
| `notatki/konsylium/c_priorytety/brief.md` | Brief dla konsylium, bez naszej opinii. **Nie wysłany** — czeka na decyzję Kuby. |

Oba skrypty uruchamia się z głównego folderu przez `python -I`, każdy w kilka sekund. Tylko czytają bazę.

Okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026. „Przyjęta reguła” = źródło według pierwszego wejścia, kod kampanii rozstrzyga (`ZALOZENIA.md` 22). „Sesja płatności” = reguła porównawcza (punkt 23). „Nowe kampanie” = `meta_prosp_l4_szybko` (Meta, od 3.11.2025) i `tt_prosp_l4_15min` (TikTok, od 9.02.2026), obie na zwolnienie lekarskie (L4).

---

## 1. Propozycja odpowiedzi „czy to wzrost” (do akceptacji Kuby)

**Propozycja w dwóch zdaniach:** w rozumieniu Telemedi to nie jest wzrost, bo z dwóch warunków spełniony jest tylko pierwszy: pacjentów z pierwszym zakupem jest o 52,1% więcej (24 687 wobec 16 231), ale retencja jest gorsza (powrót w 90 dniach 17,4% wobec 23,9% na tych samych dniach kalendarzowych, a marża na pacjenta w 90 dniach 58,3 zł wobec 66,6 zł). Większość spadku retencji to pacjenci dwóch nowych kampanii na L4, ale bez nich retencja też spada (do 22,0% według przyjętej reguły albo 20,4% według sesji płatności), a nowych pacjentów spoza tych kampanii przybyło tylko o 7,3–20,1%.

### 1a. Więcej pacjentów: tak

- Nowych pacjentów jest 24 687 w okresie 2 wobec 16 231 w okresie 1, czyli +52,1% (`c_priorytety.txt`, W1).
- Bez pacjentów dwóch nowych kampanii na L4 jest ich 17 419 według przyjętej reguły (+7,3%) albo 19 500 według sesji płatności (+20,1%).
- Z kanałów bezpłatnych (wejścia bezpośrednie, bezpłatne wyszukiwanie, program poleceń) przybyło 12,1%: z 7 069 do 7 924.
- Nie wiemy, ilu pacjentów nowych kampanii przyszłoby i bez nich (dodatkowość, sekcja 4, punkt 1).

### 1b. Lepsza retencja: nie

- Powrót, czyli kolejne nieanulowane zamówienie, liczony na tych samych dniach kalendarzowych (`c_priorytety.txt`, W2):
  - w 30 dniach 7,8% (22 646 pacjentów) wobec 11,0% (14 984);
  - w 60 dniach 13,7% (20 823) wobec 19,1% (13 941);
  - w 90 dniach 17,4% (18 924) wobec 23,9% (12 867);
  - w 180 dniach 22,2% (12 591) wobec 27,5% (9 125) (`a5r_kohorty.txt`).
- Marża na pacjenta w 90 dniach przed kosztem pozyskania: 58,3 zł wobec 66,6 zł, czyli −8,3 zł.
- **Bez pacjentów nowych kampanii retencja też spada.** Powrót w 90 dniach wynosi 22,0% według przyjętej reguły (14 031 pacjentów) i 20,4% według sesji płatności (15 414), wobec 23,9%. Marża na pacjenta w 90 dniach 66,0 zł i 63,3 zł, wobec 66,6 zł.
- Pacjenci nowych kampanii wracają w 90 dniach w 4,1% (4 893 pacjentów).
- W obrębie tej samej usługi spadku nie widać: pacjenci z pierwszym L4 z pozostałych kanałów wracają w 13,9% wobec 14,8%, bez istotnej zmiany (`a5_retencja.md`, krok 3).

### 1c. Najważniejsze zastrzeżenia

1. **Dashboard liczy dane na surowo.** Zawiera 604 zdublowane zamówienia z czerwca 2026, 2 071 zamówień kont testowych i przychód przed zwrotami. Po oczyszczeniu zamówienia rosną o 55,7% zamiast 61%, a przychód z konsultacji po zwrotach o 44,8% zamiast 50% (`ZNALEZISKA.md`, A3). Nowi pacjenci (+52%) i TelemediGO (+40%) się nie zmieniają.
2. **Start od zera.** W okresie 1 nie było bazy pacjentów z poprzedniego roku. W okresie 2 pacjenci pozyskani w okresie 1 złożyli 5 289 zamówień powtórnych, które dały 153 tys. zł marży konsultacji (`c_priorytety.txt`, W3). Sumy roczne z definicji faworyzują więc drugi rok.
3. **Wynik biznesu rośnie wolniej niż sprzedaż.** Marża po koszcie lekarza, kampaniach i prowizji wynosi 828 tys. zł w okresie 1 i 1 048 tys. zł w okresie 2, czyli +26,6%. Po odjęciu marży powtórnych konsultacji pacjentów pozyskanych w okresie 1 to +8,1%, a po odjęciu także ich opłat za TelemediGO (41,5 tys. zł) +3,1%. To rozbicie księgowe, a nie wynik biznesu, który startuje od zera: nie modeluje zmian wydatków ani zachowania pacjentów. Wydatki na kampanie rosną o 77% (z 368 do 650 tys. zł).
4. **Struktura pacjentów się zmieniła.** Pacjenci nowych kampanii to 29% nowych pacjentów okresu 2 według przyjętej reguły (7 268 z 24 687). Zostawiają 36,3 zł marży w 90 dniach wobec 66,0 zł pozostałych.
5. **Obie reguły źródła.** Podział spadku powrotu (z 23,9% do 17,4%) na nowe i stare kampanie zależy od reguły. Według przyjętej reguły to 4,6 punktu procentowego nowych kampanii i 2,0 punktu starych. Według sesji płatności to 3,0 i 3,5 punktu (`ZNALEZISKA.md`, A5 retencja). Kierunek jest ten sam w obu.
6. **To opis, nie przyczyna.** Widzimy spadek obserwowanej retencji, także po wyłączeniu pacjentów nowych kampanii. Nie dowodzi to, że identyczni pacjenci zachowują się gorzej. Rozkład na strukturę i zachowanie nie mówi też, co by się stało bez nowych kampanii. Spadek w starych kampaniach zbiega się z porannymi opóźnieniami u internistów, ale ich nie dowodzi (sekcja 4, punkt 4).

---

## 2. TelemediGO — cztery pytania Kuby

Raport: `analiza/wyniki/c_telemedigo.txt`. Każde członkostwo kosztuje 89 zł i trwa 365 dni, bez wyjątków. Każde z 9 738 zamówień ze zniżką TelemediGO przypada w czasie ważności członkostwa.

### 2.1 Skąd wzrost sprzedaży o 40%

**W skrócie:** wzrost o 709 zakupów (z 1 759 do 2 468, +40,3%) wynika z tego, że jest więcej zamówień, i z pełnego roku sprzedaży w newsletterze. Odsetek pacjentów, którzy kupują TelemediGO, nie rośnie.

- **Typ zakupu** (sekcja 1a):

  ```
  typ zakupu                                   okres 1   okres 2   zmiana   udział we wzroście
  przy kasie z pierwszym zamówieniem pacjenta      905      1 089     +184         26%
  przy kasie z kolejnym zamówieniem                629        918     +289         41%
  osobno, z newslettera crm_go_upsell              225        461     +236         33%
  razem                                          1 759      2 468     +709        100%
  ```

- **Sprzedaż osobna w newsletterze** ruszyła 8.09.2025. W okresie 1 działała więc tylko 23 dni, a sprzedała w nich 225 członkostw. W okresie 2 sprzedaje średnio 38 miesięcznie (sekcja 1b). Możliwe odczytanie: start kampanii zebrał od razu pacjentów, którzy czekali na ofertę. Wysyłek w danych nie ma, więc nie wiemy, ile wiadomości poszło w kolejnych miesiącach.
- **Przy kasie: więcej zamówień, a nie wyższy odsetek kupujących** (sekcja 1e). Liczymy zamówienia pacjentów bez ważnego członkostwa:
  - przy pierwszym zamówieniu odsetek kupujących spada z 5,58% do 4,41%. Więcej zamówień dodaje 471 zakupów, a niższy odsetek odejmuje 287;
  - przy kolejnych zamówieniach odsetek rośnie lekko, z 9,27% do 9,86%. Więcej zamówień dodaje 234 zakupy, a wyższy odsetek 55. Zamówień powtórnych jest więcej głównie przez start od zera.
- **Spadek odsetka przy pierwszym zamówieniu to w całości pacjenci nowych kampanii na L4** (sekcja 1f). Kupuje u nich 1,5% (Meta na L4 1,48%, TikTok 1,49%). Bez nich odsetek stoi: 5,58% wobec 5,63%. W rozkładzie zmiany −1,16 punktu procentowego, a z tego −1,22 przypada na nowe segmenty.
- **Kupujący** (sekcja 1c): nowi pacjenci przy pierwszym zamówieniu +184, pacjenci, którzy już kupowali, ale pierwszy raz biorą TelemediGO, +440, a drugie członkostwo po wygaśnięciu pierwszego +85.
- **Ponowne zakupy są rzadkie** (sekcja 1d). W 90 dniach po wygaśnięciu odnawia 5,4% członków (62 z 1 140), a w 180 dniach 6,3%. Tylko 8,8% byłych członków składa w 90 dniach po wygaśnięciu jakiekolwiek zamówienie. Większość członków nie jest więc aktywna, gdy członkostwo wygasa. W okresie 2 wygasa 1 759 członkostw. W danych nie widać przypomnienia o wygaśnięciu.
- **Kanały** (sekcja 1g): przybyło głównie u pacjentów z wejść bezpośrednich (+212), z bezpłatnego wyszukiwania (+141) i z Google Ads ogólnych (+123).

### 2.2 Ile dają opłaty wobec zniżek udzielonych na wizytach

**W skrócie:** opłata 89 zł nie pokrywa średniej zniżki. Przy założeniu, że te same wizyty zostałyby kupione po cenie katalogowej i bez TelemediGO, opłaty są niższe od zniżek o 11–16 zł na członkostwo. To nie jest strata programu, bo nie wiemy, ile wizyt członkostwo dokłada. Pacjenci, którzy kupują przy kolejnym zamówieniu, dostają zniżek dużo więcej niż płacą.

- **Zniżka efektywna** liczy tylko wizyty, za które zapłata zostaje (odbyte i nieodebrane). Przy anulowanej i zwróconej wizycie pacjent dostaje całą zapłatę z powrotem, więc zniżka nie zmienia przychodu.
- **Członkostwa z okresu 1** mają pełne 365 dni w danych (sekcja 2a):
  - 1 759 członkostw, 156 551 zł opłat;
  - 183 939 zł zniżki efektywnej na 4 902 zamówieniach, czyli 104,57 zł na członkostwo;
  - opłaty minus zniżki: −27 388 zł, czyli −15,57 zł na członkostwo, przy założeniu, że te same wizyty zostałyby kupione bez TelemediGO.
- **Według typu zakupu** (okres 1, zniżka efektywna na członkostwo):
  - przy kasie z pierwszym zamówieniem: 88,94 zł, czyli prawie tyle, ile opłata;
  - przy kasie z kolejnym zamówieniem: 136,36 zł, czyli 47,4 zł więcej niż opłata;
  - osobno z newslettera: 78,56 zł, czyli 10,4 zł mniej niż opłata. Ale 41,8% tych członków nie wykorzystuje zniżki ani razu.
- 38% członkostw dostaje więcej zniżki niż 89 zł. Mediana wynosi 66,3 zł.
- **Członkostwa z okresu 2** idą tym samym torem (sekcja 2b): w pierwszych 180 dniach 77,91 zł zniżki wobec 81,68 zł w okresie 1. Przy tej samej proporcji na resztę roku wyszłoby około 99,7 zł, czyli −10,7 zł na członkostwo. To przybliżenie, nie wynik.
- **Widok kasowy, rok do roku** (sekcja 2c): w okresie 1 opłaty przewyższyły zniżki o 35,8 tys. zł, a w okresie 2 zniżki przewyższyły opłaty o 24,9 tys. zł. W okresie 2 zniżki dostają też członkowie z okresu 1.
- **Zastrzeżenie:** zniżka jest kosztem tylko wtedy, gdy wizyta odbyłaby się i bez TelemediGO. Jeśli członkostwo przyciąga dodatkowe wizyty, każda dodatkowa wizyta u internisty daje marżę (punkt 2.3), a u większości specjalistów stratę.

### 2.3 Czy wizyty ze zniżką pokrywają koszt lekarza

**W skrócie:** u internisty po zniżce 50% tak, u psychiatry po zniżce 20% ledwo, u pozostałych specjalistów nie. W okresie 2 wizyty ze zniżką u specjalistów poza psychiatrą przyniosły 14,7 tys. zł straty.

- **Cennik** (sekcja 3a; ceny z danych, koszt lekarza za wizytę odbytą):

  ```
  specjalizacja                          cena   po zniżce   koszt lekarza   marża bez zniżki   marża ze zniżką
  internista (zniżka 50%)                 89,0      44,5          25              64,0             +19,5
  psychiatra                             269,0     215,2         200              69,0             +15,2
  endokrynolog, ginekolog                119,0      95,2         100              19,0              −4,8
  dermatolog, kardiolog, neurolog, urolog 109,0     87,2         100               9,0             −12,8
  psycholog                               99,0      79,2         100              −1,0             −20,8
  pediatra                                95,0      76,0         100              −5,0             −24,0
  ```

- **Rzeczywiste zamówienia z obu lat, z anulacjami, nieodebranymi i zwrotami** (sekcja 3b, marża na zamówienie):
  - internista: 18,6 zł ze zniżką wobec 59,4 zł bez zniżki;
  - psychiatra: 17,0 zł wobec 65,4 zł;
  - pediatra: −21,8 zł wobec −3,6 zł;
  - pozostali specjaliści ze zniżką od −2,6 zł (ginekolog) do −19,4 zł (psycholog).
- **Razem** (sekcja 3c): u specjalistów poza internistą i psychiatrą marża zamówień ze zniżką wynosi −7 845 zł w okresie 1 (753 zamówienia) i −14 682 zł w okresie 2 (1 512 zamówień). Zniżka efektywna na tych zamówieniach to 15 539 zł i 31 405 zł.
- **Znalezisko poboczne (zależy od założenia 33):** wizyta u pediatry przynosi stratę także bez zniżki (cena 95 zł przy koszcie lekarza 100 zł), a u psychologa wychodzi prawie na zero. Przy koszcie pediatry 25 zł (wariant z założenia 33) obie usługi są dochodowe. Prawdziwej stawki pediatry nie znamy (sekcja 4).

### 2.4 Czy TelemediGO zmienia powroty

**W skrócie:** kupujący TelemediGO wracają dużo częściej niż podobni pacjenci, ale dane nie mówią, ile z tego to wpływ zniżki, a ile to, że kupują ci, którzy i tak planują wracać. Obie kontrole dają wyniki zgodne z kilkoma wyjaśnieniami i żadna tego nie rozstrzyga. Rozstrzygnie test.

- **Porównanie z podobnymi pacjentami** (sekcja 4a). Nowi pacjenci, którzy kupili TelemediGO przy pierwszym zamówieniu, wobec pacjentów bez niego z tego samego okresu, kanału pozyskania, pierwszej usługi i miesiąca kohorty:
  - powrót w 90 dniach: okres 1 — 34,3% wobec 24,2% (905 kupujących), czyli +10,1 punktu procentowego (od +6,9 do +13,4); okres 2 — 34,7% wobec 20,0% (858), czyli +14,6 punktu (od +11,4 do +17,8);
  - kolejne zamówienia w 365 dniach (okres 1): 1,31 wobec 0,74 na pacjenta;
  - marża w dniach 1–365 jest u kupujących niższa o 21,9 zł, bo płacą mniej za każdą wizytę;
  - **z opłatą 89 zł i zniżką na pierwszym zamówieniu** (dni 0–365) kupujący zostawiają o 31,6 zł więcej marży niż podobni pacjenci (117,3 zł wobec 85,7 zł);
  - dodanie statusu pierwszego zamówienia do warstw prawie nic nie zmienia.
- **Kontrola 1: przebieg zamówień przed wygaśnięciem członkostwa i po nim, wśród kupujących bez kolejnego zakupu członkostwa** (sekcja 4b, okres 1, 683 kupujących). Gdyby przewagę dawała tylko niższa cena, po wygaśnięciu powinna zniknąć:
  - dni 1–90: zamawia 34,7% kupujących wobec 19,1% podobnych, iloraz 1,82;
  - dni 276–365 (ostatni kwartał ważności): 8,5% wobec 2,3%, iloraz 3,77. Możliwe odczytanie: pacjenci wykorzystują zniżkę przed końcem ważności;
  - dni 366–455 (po wygaśnięciu): 2,9% wobec 1,7%, iloraz 1,77, różnica +1,3 punktu (od −0,2 do +2,7).
  - wśród wszystkich pierwotnych kupujących (707, także odnawiający) po wygaśnięciu zamawia 6,2% wobec 1,6%, ale tu część zamówień jest już na nowym członkostwie;
  - **Odczytanie:** w punktach przewaga maleje, ale w proporcji zostaje prawie taka sama jak na początku. Wynik jest zgodny z kilkoma wyjaśnieniami (samoselekcja, nawyk, zniżka) i nie rozstrzyga między nimi. Liczby po wygaśnięciu są małe, a wyłączenie odnawiających zależy od zachowania po zakupie i zabiera z grupy najaktywniejszych (recenzja Codeksa).
- **Kontrola 2: pacjenci, którzy weszli z newslettera sprzedającego TelemediGO** (sekcja 4c). Kupujący osobno wobec pacjentów bez zakupu przy wejściu i przez następne 30 dni. Obie grupy zainteresowały się ofertą:
  - w 180 dniach przed zakupem (albo przed wejściem bez zakupu) mieli prawie tyle samo zamówień: 2,93 kupujący (450 pacjentów) i 3,04 pozostali (189);
  - w 180 dniach po: 1,51 wobec 1,22;
  - różnica różnic: +0,40 zamówienia na pacjenta w 180 dniach. 15 ze 189 pacjentów grupy porównawczej kupuje członkostwo później; bez nich różnica wynosi +0,49;
  - **Odczytanie:** przy podobnej historii kupujący zamawiają potem więcej. To statystyka opisowa, która zakłada równoległe trendy obu grup. Dopuszcza wpływ zniżki, ale decyzja o zakupie może też wynikać z wizyty, którą pacjent już planował. Grupa porównawcza jest mała. Lepsze porównanie na tych danych to dopasowanie przy wejściu według miesiąca, stażu, czasu od ostatniej konsultacji i wcześniejszych zamówień (recenzja Codeksa; do zrobienia, jeśli Kuba uzna to za potrzebne).
- **Test, który to rozstrzygnie** (sekcja 4d; koszt: `c_priorytety.txt`, P10):
  - **losowe członkostwo próbne:** połowa nowych pacjentów dostaje bezpłatny dostęp do zniżek TelemediGO na 90 dni, od dnia po pierwszym zamówieniu. Druga połowa nie dostaje. Porównujemy powrót w 90 dniach i marżę. Tu nie ma samoselekcji, bo o członkostwie decyduje losowanie. Test mierzy wpływ niższej ceny, ale sam nie rozstrzyga, czy płatny program za 89 zł się opłaca;
  - różnice z porównania służą tylko jako scenariusze efektu. Jeśli wpływ zniżki to jedna czwarta obecnej różnicy (3,7 punktu procentowego), potrzeba 1 823 pacjentów na grupę, czyli około 1,8 miesiąca pozyskania plus 90 dni obserwacji. Dodatkowy koszt to około 12,2 tys. zł zniżek przy obecnym zachowaniu pacjentów. Jeśli wpływ to połowa różnicy, wystarczy 487 pacjentów na grupę i około 3,3 tys. zł;
  - losowe pokazywanie samej oferty przy kasie nie wystarczy, bo kupuje tylko 4,5% pacjentów i efekt ginie w grupie (potrzeba ponad 4 lat pozyskania).

### 2.5 Co z tego wynika dla listy priorytetów (propozycja)

- Warunki TelemediGO u specjalistów to pozycja 7 listy.
- **Nie promujemy mocniej sprzedaży ani odnowień TelemediGO przed testem.** Jeśli wizyty odbyłyby się i bez członkostwa, opłaty są niższe od zniżek o około 11–16 zł na członkostwo. Program opłaca się tylko wtedy, gdy przyciąga dodatkowe wizyty, zwłaszcza u internisty. Test to pozycja 10 listy.

---

## 3. Lista priorytetów (propozycja, od najważniejszego)

**Zasady listy:**
- Wartość to zmiana marży na rok. Rokiem bazowym jest okres 2. Marża = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza − wydatki na kampanie − prowizja.
- Przy kampaniach podajemy wynik po 90 i po 180 dniach od pozyskania (dopisek Kuby) oraz obie reguły źródła.
- **Kwot nie sumujemy.** Mają różne horyzonty i częściowo się nakładają. Na przykład wstrzymanie TikToka (pozycja 3) zabiera tę część naprawy zwrotów L4 (pozycja 2), która dotyczy TikToka: 14,9 tys. z 57,1 tys. zł w wariancie A.
- Czas wdrożenia to nasz szacunek, a nie liczba z danych. Telemedi zna swój zespół i system lepiej.
- Kolejność: najpierw rzeczy pewne w danych i szybkie, potem decyzje, które wymagają testu.

**Przegląd:**

| # | Co robimy | Ile warte rocznie (marża) | Pewność | Wdrożenie |
|---|---|---|---|---|
| 1 | Naprawić zakładanie konta w Safari na iOS | 75–83 tys. zł (90 dni), 86–95 tys. zł (180 dni) | wysoka: awaria widoczna w danych | dni |
| 2 | Uczciwa obietnica w reklamach L4: mniej zwrotów po wizycie | 22–57 tys. zł (przyjęta reguła), 13–32 tys. zł (sesja płatności) | średnia: nie znamy powodu zwrotów | 1–2 tygodnie |
| 3 | Wstrzymać TikToka na L4 (naprawa nie wystarcza) | +12–31 tys. zł przy 100% pacjentów dodatkowych, do +82 tys. zł | średnia: znak ten sam w obu regułach i oknach | 1 dzień |
| 4 | Sprawdzić ręcznie zakup dla zalogowanych pacjentów | 0 albo 36–40 tys. zł (wysoki scenariusz 89 tys. zł) | niska: dane wskazują raczej na 0 zł | 1 dzień |
| 5 | Test dodatkowości Meta na L4 w połowie województw | decyzja warta od −28 do +163 tys. zł | — (to jest test) | 1 tydzień + 4–6 tygodni |
| 6 | Poranna obsada internistów: dane o grafikach i test | scenariusz od 0 do 65 tys. zł, koszt obsady nieznany | niska | 2–6 tygodni |
| 7 | TelemediGO: bez zniżki u specjalistów z ceną po zniżce poniżej kosztu lekarza | scenariusze 15–31 tys. zł | wysoka co do kierunku | 1–2 tygodnie, pełny efekt po 12 miesiącach |
| 8 | `gs_generic_specjalisci`: obniżyć koszt pozyskania albo wyłączyć | +19–32 tys. zł przy 100% pacjentów dodatkowych, do +53 tys. zł | średnia: strata w obu regułach i oknach | 1 tydzień + 4–8 tygodni |
| 9 | Sprawdzić stratę między kliknięciem a sesją w Meta i TikToku | 0 albo do 52 tys. zł (górna granica) | niska | 1–2 dni |
| 10 | Test TelemediGO z losowym członkostwem próbnym | decyduje o roli programu; koszt testu 3–12 tys. zł | — (to jest test) | 2–6 tygodni + 90 dni |

### Pozycja 1. Naprawić zakładanie konta w Safari na iOS

- **Z danych:** od 17.03.2026 w Safari na iPhone'ach i iPadach przestaje działać zakładanie nowego konta. Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spada z 66,1% do 45,6% i nie wraca. Logowanie do istniejących kont działa. Inne przeglądarki tego nie mają, a spadek jest w każdym kanale (`a5_pozyskanie.md`, sekcja 2).
- **Ile warta:** w 198 dniach od 17.03 do 30.09.2026 to 628–695 utraconych pierwszych zamówień, czyli 1 158–1 281 rocznie. Nowy pacjent z pierwszą płatnością w Safari na iOS zostawia w okresie 2 średnio 64,6 zł marży w 90 dniach i 74,3 zł w 180 dniach. Daje to **75–83 tys. zł marży rocznie w horyzoncie 90 dni i 86–95 tys. zł w horyzoncie 180 dni** (`c_priorytety.txt`, P1).
- **Założenia:** utracone pierwsze zamówienie to utracony nowy pacjent (odpadnięci nie kupują później częściej w tej samej przeglądarce, ale innych urządzeń nie widzimy); nie doliczamy kosztu pozyskania, bo wejście już zostało opłacone; skala problemu z 17.03–30.09.2026 utrzymywałaby się przez rok. Kwoty to marża rocznika odzyskanych pacjentów w 90 albo 180 dniach od pozyskania, a nie wpływy w całości w tym samym roku.
- **Po czym poznamy, że zadziałała:** krok konta po wyborze terminu w Safari na iOS u osób, które jeszcze nie kupowały, wraca z około 46% do około 66%, a zakładanie kont w Safari na iOS wraca do poziomu sprzed 17.03 (około 1 080 w 60 dniach). Widać to w lejku dzień po dniu po 1–2 tygodniach.
- **Wdrożenie:** powtórzenie rejestracji na iPhonie, logi błędów i lista zmian z 16–17.03.2026 to 1–2 dni. Sama poprawka to zwykle dni.

### Pozycja 2. Uczciwa obietnica w reklamach L4 i na stronie wejścia: mniej zwrotów po wizycie

- **Z danych:** 17,4% odbytych wizyt L4 pacjentów nowych kampanii kończy się zwrotem po wizycie (1 024 z 5 895), wobec 5,3% L4 pozostałych pacjentów. Kod rabatowy ani opóźnienie wizyty nie zmieniają tego odsetka. Za zwróconą wizytę lekarz dostaje wynagrodzenie (`a5_ekonomia.md`, sekcja 4b).
- **Ile warta:** gdyby odsetek spadł do poziomu pozostałych pacjentów, **od 22,3 tys. zł (wariant B) do 57,1 tys. zł (wariant A) marży rocznie według przyjętej reguły i od 12,7 do 31,8 tys. zł według sesji płatności.** Wynik po 180 dniach jest taki sam, bo ci pacjenci prawie nie wracają (`c_priorytety.txt`, P2).
- **Założenia:** wariant A — wizyta daje pacjentowi to, czego oczekiwał, i zapłata zostaje. Wariant B — uczciwa obietnica odstrasza pacjentów, którzy nie dostaliby L4, i ci nie kupują; oszczędzamy koszt lekarza. Prawda leży zwykle pomiędzy.
- **Po czym poznamy:** odsetek zwróconych wizyt L4 z tych kampanii tydzień po tygodniu spada z 17,4% w stronę 5–6%. Obok śledzimy liczbę pierwszych zamówień z kampanii i koszt pozyskania, bo wariant B zmniejsza liczbę zamówień.
- **Wdrożenie:** zmiana treści reklam i strony `/zwolnienie-l4-online` to 1–2 tygodnie. Pytanie przed płatnością („lekarz wystawia L4 tylko przy wskazaniach medycznych”) to 2–4 tygodnie. Pomiar to 4–6 tygodni.
- **Czego nie wiemy:** powodu zwrotów nie ma w danych (sekcja 4, punkt 3).

### Pozycja 3. Wstrzymać kampanię TikTok na L4 — naprawa nie wystarcza

- **Z danych:** wynik na pacjenta jest ujemny w obu regułach i w obu oknach: −4,6 i −17,8 zł po 90 dniach, −1,1 i −11,0 zł po 180 dniach. Pacjenci wracają w 90 dniach w 3,2% (`a5_ekonomia.md`, sekcje 1–2).
- **Naprawić albo wyłączyć — obie drogi w marży na rok** (`c_priorytety.txt`, P3):
  - **dziś:** −11,9 tys. zł (przyjęta reguła) i −30,8 tys. zł (sesja płatności) po 90 dniach; −13,5 i −32,3 tys. zł po 180 dniach;
  - **naprawić zwroty** (wariant A, najlepszy): wynik +3,0 tys. zł albo −23,2 tys. zł po 90 dniach; +1,4 i −24,7 tys. zł po 180 dniach. Przeglądarki wbudowane w aplikacje nie dają w tym rachunku nic (w TikToku konwersja nie jest w nich niższa);
  - **wyłączyć:** przy 100% pacjentów dodatkowych +11,9 albo +30,8 tys. zł po 90 dniach i +13,5 albo +32,3 tys. zł po 180 dniach; przy 50% +47,2 albo +56,6 tys. zł; przy 0% +82,5 tys. zł (oszczędzone wydatki).
- **Propozycja:** wstrzymać. Wyłączenie nie pogarsza marży w żadnej regule, żadnym oknie i żadnym wariancie dodatkowości. Naprawa w najlepszym razie doprowadza wynik do zera. Do kampanii można wrócić po naprawie obietnicy (pozycja 2), na małym budżecie i z grupą kontrolną.
- **Dodatkowa korzyść, jeśli hipoteza porannych opóźnień jest prawdziwa:** mniej porannych wizyt u internisty (pozycja 6).
- **Po czym poznamy:** łączna marża rośnie co najmniej o 11,9 tys. zł rocznie, czyli tyle, ile w wariancie, w którym wszyscy pacjenci TikToka byli dodatkowi. Jeśli po wstrzymaniu w pozostałych kanałach przybywa nowych pacjentów L4, część pacjentów TikToka przyszłaby i bez niego, a zysk jest większy.
- **Wdrożenie:** 1 dzień. Pomiar 4–6 tygodni.

### Pozycja 4. Sprawdzić ręcznie zakup dla pacjentów zalogowanych od wejścia

- **Z danych:** 22 068 sesji zalogowanych od wejścia nigdy nie kończy się zakupem konsultacji. Każdy z 22 289 zakupów powtórnych ma krok logowania, choć według słownika danych zalogowany pacjent nie powinien go mieć. Dane nie rozstrzygają między odczytaniami: (A) to wizyty „sprawdzam konto” albo (B) ścieżka zakupu dla zalogowanych jest zepsuta. Kilka faktów przemawia za A (`a5_pozyskanie.md`, sekcja 3).
- **Ile warta** (`c_priorytety.txt`, P5): w odczytaniu A 0 zł. W odczytaniu B to scenariusze: 2 906 sesji z wyborem usługi w okresie 2 × 40,9% do płatności × 33,99 zł marży zamówienia powtórnego = **około 40 tys. zł rocznie**, a licząc pacjentów zamiast sesji (2 557, bo kilka sesji to często ten sam zamiar zakupu) około 36 tys. zł. Wysoki scenariusz (× 90,5%) daje około 89 tys. zł, ale to przelicznik z późniejszego kroku, a nie górna granica. Zakładamy, że odzyskane płatności to odrębne zamówienia. Część tych zakupów i tak dzieje się później.
- **Po czym poznamy:** test daje odpowiedź od razu. Jeśli ścieżka jest zepsuta, po naprawie sesje zalogowane od wejścia zaczynają kończyć się płatnością.
- **Wdrożenie:** ręczny test w 1 dzień: zalogować się, zamknąć kartę, wrócić zalogowanym z linku w newsletterze i z `/konto`, wybrać usługę i termin, zapłacić, sprawdzić zapisane kroki. Do tego prośba o logi błędów dla sesji zalogowanych od wejścia.
- **Dlaczego tak wysoko mimo niskiej pewności:** to najtańsza pozycja z wartością rzędu kilkudziesięciu tysięcy złotych, a CRM to główny kanał powrotów.

### Pozycja 5. Meta na L4: test dodatkowości przed decyzją

- **Z danych:** wynik kampanii zależy od reguły źródła: +27,8 tys. zł rocznie według przyjętej reguły i −28,7 tys. zł według sesji płatności po 90 dniach; +29,9 i −27,5 tys. zł po 180 dniach. Dane nie rozstrzygają, ilu jej pacjentów przyszłoby i bez niej. Jest słaby sygnał przejmowania pacjentów L4 z pozostałych kanałów po jej starcie (`a5_ekonomia.md`, sekcje 6–7).
- **Naprawić albo wyłączyć** (`c_priorytety.txt`, P4):
  - **naprawić zwroty** (wariant A): wynik +70,1 tys. zł (przyjęta reguła) albo −4,5 tys. zł (sesja płatności);
  - **wyłączyć:** od −27,8 tys. zł (przyjęta reguła, wszyscy pacjenci dodatkowi) do +163,3 tys. zł (żaden pacjent nie jest dodatkowy).
  - **Tyle jest wart test:** decyzja waha się od −27,8 do +163,3 tys. zł rocznie.
- **Propozycja:** do czasu wyniku testu kampania działa z poprawioną obietnicą (pozycja 2).
- **Test:** na 4–6 tygodni wyłączyć albo mocno obniżyć budżet w losowo wybranej połowie województw. Porównać nowych pacjentów ze wszystkich kanałów, osobno L4, i powroty pozostałych pacjentów w województwach z kampanią i bez niej. Ten sam test sprawdza hipotezę porannych opóźnień, jeśli zmierzymy przy okazji opóźnienia porannych wizyt.
- **Po czym poznamy:** różnica w liczbie nowych pacjentów między połówkami kraju wobec różnicy w wydatkach. To daje koszt pozyskania pacjenta dodatkowego.
- **Wdrożenie:** tydzień przygotowania i 4–6 tygodni testu.

### Pozycja 6. Poranna obsada internistów: dane o grafikach i test

- **Z danych:** od listopada 2025 około połowa porannych wizyt u internisty (6:00–11:59) zaczyna się ponad 15 minut po terminie, wobec 5–7% rok wcześniej. Przy tym samym porannym ruchu opóźnień jest o 26,4 punktu procentowego więcej, więc spadła przepustowość poranka, a nie tylko przybyło pacjentów. Wizyty spóźnione ponad 30 minut mają średnią ocenę 2,9 wobec 4,5 przy punktualnych. Rano spada powrót po wizytach spóźnionych (`a5_retencja.md`, krok 4).
- **Ile warta:** to tylko scenariusz: od 0 zł (opóźnienia nie zmieniają powrotów) przez 11,9–12,7 tys. zł (wariant wąski) do 31,8–65,2 tys. zł (wariant szeroki) marży rocznie w horyzoncie 180 dni (`c_priorytety.txt`, P8). Kosztu dodatkowej obsady nie ma w danych, więc wartości netto nie da się policzyć.
- **Po czym poznamy:** odsetek porannych wizyt u internisty spóźnionych ponad 15 minut spada z około 50% w stronę 5–7%, oceny porannych wizyt rosną, a powrót w 90 dniach pacjentów z pierwszą wizytą rano wraca w stronę 23–24%.
- **Wdrożenie:** dane o obsadzie i grafikach to kilka dni. Test (więcej internistów rano w losowo wybrane dni albo mniej porannych terminów z kampanii na L4) to 2–4 tygodnie. Efekt w powrotach widać po 90 dniach.

### Pozycja 7. TelemediGO: bez zniżki u specjalistów, u których cena po zniżce jest niższa niż koszt lekarza

- **Z danych:** po zniżce 20% cena jest niższa niż koszt lekarza u wszystkich specjalistów poza psychiatrą: od −4,8 zł (endokrynolog, ginekolog) do −24 zł (pediatra) na wizycie. W okresie 2 te wizyty przyniosły 14,7 tys. zł straty na 1 512 zamówieniach (punkt 2.3).
- **Ile warta** (scenariusze, nie granice; `c_priorytety.txt`, P6): **14,7 tys. zł rocznie**, jeśli wszystkie te zamówienia znikną; 18,9 tys. zł, jeśli znikną tylko te, które dziś przynoszą stratę; **31,4 tys. zł**, jeśli wszystkie zostaną po cenie katalogowej. Gdy każdy pacjent reaguje inaczej, wynik mieści się między 10,9 a 35,2 tys. zł. Ryzyko: część pacjentów może rzadziej kupować TelemediGO. Jeśli wizyty odbyłyby się i bez programu, opłaty są dziś niższe od zniżek (punkt 2.2), więc mniejsza sprzedaż nie obniżałaby marży.
- **Warianty:** zniżka 0% u tych specjalistów; zniżka najwyżej 8% u specjalistów z ceną 109–119 zł (cena po zniżce zostaje powyżej 100 zł kosztu lekarza) i bez zniżki u pediatry i psychologa, których cena katalogowa już jest poniżej kosztu lekarza; albo zniżka tylko u internisty i psychiatry.
- **Po czym poznamy:** marża wizyt członków u specjalistów przechodzi z −14,7 tys. zł na zero albo powyżej. Obok śledzimy sprzedaż TelemediGO i powroty członków.
- **Wdrożenie:** zmiana regulaminu i kasy to 1–2 tygodnie. Obecni członkowie mają stare warunki do końca ważności, więc pełny efekt jest po 12 miesiącach.

### Pozycja 8. `gs_generic_specjalisci` (Google Ads ogólne na specjalistów): obniżyć koszt pozyskania albo wyłączyć

- **Z danych:** wynik na pacjenta jest ujemny w obu regułach i obu oknach: −23,7 i −44,7 zł po 90 dniach, −14,3 i −36,6 zł po 180 dniach. Marża pacjenta jest niska, bo wizyta u specjalisty po cenie katalogowej zostawia tylko 9–19 zł ponad koszt lekarza (`a5_ekonomia.md`, sekcja 2; punkt 2.3).
- **Naprawić albo wyłączyć** (`c_priorytety.txt`, P7; 923 nowych pacjentów rocznie według przyjętej reguły, 657 według sesji płatności, wydatki 53,2 tys. zł):
  - **dziś:** −23,3 tys. zł (przyjęta reguła) i −31,5 tys. zł (sesja płatności) po 90 dniach; −19,4 i −30,2 tys. zł po 180 dniach;
  - **naprawić:** koszt pozyskania musiałby spaść z 57,6 zł (przyjęta reguła) albo 80,9 zł (sesja płatności) do 32–37 zł, czyli o 40–60% (stawki, słowa kluczowe, strona wejścia). Druga droga to wyższa marża wizyt u specjalistów (ceny). Wartość naprawy: do 19–32 tys. zł, czyli do zera straty;
  - **wyłączyć:** +19,4 do +31,5 tys. zł przy 100% pacjentów dodatkowych, +36,3 do +42,4 tys. zł przy 50%, +53,2 tys. zł przy 0%.
- **Propozycja:** najpierw obniżyć stawki i sprawdzić koszt pozyskania przez 4–8 tygodni. Jeśli nie spadnie w stronę 35 zł, wyłączyć.
- **Po czym poznamy:** koszt pozyskania i marża na pacjenta w 90 dniach z tej kampanii, miesiąc po miesiącu.
- **Wdrożenie:** tydzień zmian w kampanii i 4–8 tygodni pomiaru.

### Pozycja 9. Sprawdzić stratę między kliknięciem reklamy a sesją w Meta i TikToku

- **Z danych:** na kliknięcie przypada 0,92–0,93 sesji w Google Ads, 0,79–0,82 w Meta i 0,72 w TikToku, stale w każdym kwartale (`a5_pozyskanie.md`, sekcja 5).
- **Ile warta:** 0 zł, jeśli to sposób liczenia kliknięć przez platformy. Jeśli ludzie porzucają stronę, zanim się załaduje, i da się to odzyskać: do 1 434 zamówień × 36,3 zł marży = do 52 tys. zł rocznie (górna granica, `c_priorytety.txt`, P9).
- **Po czym poznamy:** porównanie kliknięć w link i wyświetleń strony docelowej w panelach Meta i TikToka z sesjami w analityce, dzień po dniu, oraz czas ładowania w przeglądarkach wbudowanych.
- **Wdrożenie:** 1–2 dni na sprawdzenie. Naprawa, jeśli potrzebna, zależy od przyczyny.

### Pozycja 10. Test TelemediGO z losowym członkostwem próbnym

- **Z danych:** punkt 2.4. Nie wiemy, czy TelemediGO podnosi powroty, czy tylko przyciąga pacjentów, którzy i tak wracają.
- **Ile warta:** decyduje, czy program promować (sprzedaż, przypomnienie o odnowieniu; dziś odnawia około 5%), czy ograniczyć. Dodatkowy koszt testu to około 3,3–12,2 tys. zł zniżek (`c_priorytety.txt`, P10). Test mierzy wpływ zniżki; o opłacalności płatnego programu za 89 zł decydujemy na jego podstawie razem z rachunkiem z punktu 2.2.
- **Po czym poznamy:** różnica powrotu w 90 dniach i marży między grupą z członkostwem próbnym a grupą bez niego.
- **Wdrożenie:** 2–6 tygodni na losowe przydzielenie (487–1 823 pacjentów na grupę), potem 90 dni obserwacji.

### Czego proponujemy teraz nie robić (z danych)

- **Zgoda marketingowa pacjentów nowych kampanii:** w najlepszym odczytaniu 1,9 tys. zł rocznie (`a5_ekonomia.md`, sekcja 7).
- **Przeglądarki wbudowane w aplikacje w nowych kampaniach:** w tym rachunku 0 zł, bo konwersja nie jest tam niższa. W pozostałych kampaniach sprawa jest otwarta.
- **Mocniejsza sprzedaż i odnowienia TelemediGO:** dopiero po teście z pozycji 10.

---

## 4. Czego nie da się rozstrzygnąć (z testem albo brakującymi danymi)

| # | Czego nie wiemy | Dlaczego to ważne | Test albo brakujące dane |
|---|---|---|---|
| 1 | Czy pacjenci nowych kampanii na L4 są dodatkowi | od tego zależy decyzja o Meta na L4: od −27,8 do +163,3 tys. zł rocznie | wyłączenie kampanii w losowej połowie województw na 4–6 tygodni; badanie przyrostu w panelach Meta i TikToka |
| 2 | Która reguła źródła jest bliższa prawdy dla kampanii bez kodu (Google Ads ogólne, Meta lekarz online) | znak wyniku tych kampanii zależy od reguły | ten sam test z grupą kontrolną bez reklamy |
| 3 | Powód zwrotów po wizycie L4 w nowych kampaniach (17,4% wobec 5,3%) | od niego zależy, czy naprawa jest bliżej 57 tys. zł (wariant A), czy 22 tys. zł (wariant B) | powód zwrotu, decyzja lekarza (czy L4 wystawiono), treść reklam |
| 4 | Dlaczego spadła poranna przepustowość internistów i czy opóźnienia obniżają powroty | scenariusz od 0 do 65 tys. zł rocznie; luty 2026 nie pasuje do prostej hipotezy | grafiki i obsada poranna przed i po 3.11.2025, obciążenie lekarzy pacjentami spoza B2C, koszt obsady; test z dodatkową poranną obsadą w losowe dni |
| 5 | Sesje zalogowane od wejścia: wizyty „sprawdzam konto” czy zepsuta ścieżka | 0 albo około 36–40 tys. zł rocznie (wysoki scenariusz 89 tys. zł) | ręczny test zakupu po zalogowaniu; logi błędów; znacznik „zalogowany na wejściu” w analityce |
| 6 | Przyczyna awarii zakładania konta w Safari na iOS od 17.03.2026 | potrzebna do naprawy (pozycja 1) | lista zmian w produkcie z 16–17.03.2026, logi rejestracji według przeglądarki, powtórzenie na iPhonie |
| 7 | Czy utraceni w Safari na iOS kupili na innym urządzeniu | zmienia wartość pozycji 1 | powiązanie urządzeń po adresie e-mail albo numerze telefonu przy próbie rejestracji |
| 8 | Czy TelemediGO podnosi powroty, czy tylko przyciąga pacjentów, którzy i tak wracają | decyduje o tym, czy program promować | losowe członkostwo próbne (pozycja 10) |
| 9 | Czy newsletter i SMS wywołują zakup | CRM to główny kanał powrotów; widać kliknięcia, nie wysyłki; wejść z CRM na 1 000 pacjentów jest coraz mniej (z 56–108 do 24–52 miesięcznie) | liczba wysyłek; losowa grupa kontrolna bez wysyłki |
| 10 | Wartość remarketingu porzuconego koszyka | przyjęta reguła z definicji przypisuje mu mało pacjentów | grupa kontrolna, której remarketing się nie wyświetla |
| 11 | Sezon a wydatki na kampanie | wzrostu od X 2024 do I 2025 nie da się rozdzielić; dwa lata to jedna zima i jedno lato w roku | zmiana budżetu w części kraju (grupa kontrolna według województw) |
| 12 | Strata między kliknięciem reklamy a sesją w Meta i TikToku | od 0 do 52 tys. zł rocznie | panele reklamowe, logi serwera, czas ładowania strony w przeglądarkach wbudowanych |
| 13 | Prawdziwa stawka lekarza u pediatry (przyjęte 100 zł) | przy 100 zł pediatra przynosi stratę nawet bez zniżki; przy 25 zł marża na pacjenta w 90 dniach rośnie o 3,7–4,8 zł | stawka z umów z lekarzami |
| 14 | Koszt lekarza za wizyty testowe (51 775 zł według zasady z zadania) | wynik biznesu | informacja, czy lekarze dostali wynagrodzenie za testy; przegląd testów w punkcie D |
| 15 | Warunki umowy z rankingiem lekarzy | prowizja 30,8 tys. zł według naszej reguły albo 14,9 tys. zł według kodu | umowa z rankingiem |
| 16 | Marża po 180 dniach | rachunek kampanii jej nie obejmuje; zaniża wartość kampanii z powracającymi pacjentami | czas: kohorty okresu 2 dojrzeją dopiero w 2027 |

---

## 5. Konsylium

Brief do oceny listy priorytetów leży w `notatki/konsylium/c_priorytety/brief.md`. Jest napisany bez naszej opinii. **Nic nie zostało wysłane.** Decyzja należy do Kuby (rano). Limit rundy to 3 USD.

## 6. Recenzja Codeksa (model Sol)

Wynik i nasze decyzje: sekcja 8.

## 7. Propozycje wpisów do wspólnych notatek (scalę po przeglądzie Kuby)

### Do `ZALOZENIA.md` (nowe punkty od 44, sekcja „TelemediGO i priorytety, punkt C”)

44. **Zniżka TelemediGO w złotych** = cena katalogowa − zapłata na zamówieniu ze zniżką TelemediGO. **Zniżka efektywna** liczy tylko wizyty odbyte i nieodebrane, bo przy anulowanej i zwróconej wizycie pacjent dostaje całą zapłatę z powrotem. Zniżkę przypisujemy członkostwu, w którego ważności (od chwili zakupu do `valid_until` włącznie) padło zamówienie.
45. **Typ zakupu TelemediGO:** przy kasie z pierwszym zamówieniem pacjenta, przy kasie z kolejnym zamówieniem, osobno (sesja z kampanii `crm_go_upsell`). Okres zakupu = dzień zakupu członkostwa. **Odsetek kupujących przy kasie** liczymy na zamówieniach pacjentów, którzy w chwili zamówienia nie mieli ważnego członkostwa.
46. **Opłata wobec zniżek** to rachunek przy założeniu, że wizyty ze zniżką odbyłyby się i bez TelemediGO. Nie jest to wynik programu, bo nie wiemy, ile wizyt członkostwo dokłada.
47. **Kupujący TelemediGO a podobni pacjenci:** dokładne dopasowanie w warstwach (okres, kanał pozyskania według przyjętej reguły, pierwsza usługa, miesiąc kohorty), wynik ważony liczbą kupujących. Różnica to suma wpływu zniżki i samoselekcji, nie efekt programu.
48. **Wartość pozycji listy priorytetów** = zmiana marży na rok, z okresem 2 jako rokiem bazowym, przy kampaniach w horyzoncie 90 i 180 dni od pozyskania i według obu reguł źródła. Kwot z różnych pozycji nie sumujemy (różne horyzonty, nakładanie się). Czas wdrożenia to nasz szacunek.
49. **Utracony pierwszy zakup w Safari na iOS = utracony nowy pacjent** z marżą nowych pacjentów z pierwszą płatnością w Safari na iOS w okresie 2, bez kosztu pozyskania (wejście już opłacone).

### Do `ZNALEZISKA.md` (sekcja „C — TelemediGO”)

- Wzrost sprzedaży TelemediGO o 40,3% to więcej zamówień i pełny rok sprzedaży w newsletterze (w okresie 1 23 dni). Odsetek nowych pacjentów, którzy kupują przy pierwszym zamówieniu, spada z 5,58% do 4,41%, w całości przez pacjentów nowych kampanii na L4 (1,5%).
- Członkostwa z okresu 1 dostały 104,57 zł zniżki efektywnej przy opłacie 89 zł. Kupujący przy kolejnym zamówieniu dostają 136,36 zł.
- Po zniżce 20% cena wizyty jest niższa niż koszt lekarza u wszystkich specjalistów poza psychiatrą. W okresie 2 to −14,7 tys. zł marży na 1 512 zamówieniach.
- Przy koszcie pediatry 100 zł (założenie 33) wizyta u pediatry przynosi stratę także bez zniżki (cena 95 zł).
- Odnawia około 5% członków. W danych nie widać przypomnienia o wygaśnięciu.
- Kupujący TelemediGO wracają częściej niż podobni pacjenci (+10,1 i +14,6 punktu procentowego w 90 dniach), ale po wygaśnięciu przewaga w proporcji zostaje (iloraz 1,77). Dane nie rozdzielają wpływu zniżki od samoselekcji.

### Do `PLAN.md`, `PRZEKAZANIE.md`, `analiza/README.md`

- Status C, nowe skrypty i wyniki — wpisane od razu (fakty o plikach, nie wnioski).
- Do narzędzia (punkt B): sekcja „czy to wzrost” z dwiema odpowiedziami i zastrzeżeniami; lista priorytetów z tabelą przeglądu i kartami pozycji; lista niewiadomych; TelemediGO z zestawień `c_telemedigo_miesiace*.csv` — po przyjęciu przez Kubę.

## 8. Recenzja Codeksa (model Sol) — wynik

Pełne podsumowanie: `notatki/recenzje/c_codex.md`. Polecenie i odpowiedź: `c_codex_prompt.md`, `c_codex_odpowiedz.md`.

- **Wszystkie liczby główne Codex przeliczył niezależnie, własnym kodem, i zgadzają się co do sztuki i co do złotówki:** zakupy TelemediGO według typu, odsetki kupujących, zniżki członkostw z okresu 1, marża wizyt ze zniżką u specjalistów, wynik biznesu, powroty z nowymi kampaniami i bez nich, wartości P1 i P7. Uwag krytycznych nie ma.
- **Osiem uwag, wszystkie przyjęte i wprowadzone:**
  - liczebność próby testu była zaniżona (wzór ze wspólną wariancją); teraz 136, 487 i 1 823 pacjentów na grupę zamiast 105, 422 i 1 687;
  - „+8,1%” to tylko odjęcie marży powtórnych konsultacji poprzedniego rocznika; po odjęciu także jego opłat za TelemediGO wychodzi +3,1%; oba nazwane jako rozbicie księgowe;
  - grupa porównawcza w kontroli 2 obejmuje 15 późniejszych kupujących; nowa nazwa i wariant bez nich (+0,49 zamiast +0,40);
  - kontrola 1 nie rozdziela wpływu ceny od samoselekcji; nowe brzmienie „zgodny z kilkoma wyjaśnieniami” i wariant ze wszystkimi kupującymi;
  - wartości warunków TelemediGO to scenariusze, nie granice; dodane 18,9 tys. zł i zakres 10,9–35,2 tys. zł;
  - porównanie opłat ze zniżkami wymaga jawnego założenia o tych samych wizytach; dopisane w raporcie i w szkicu;
  - koszt testu: dodatkowy, a nie nominalny (6,71 zł zamiast 6,76 zł na pacjenta);
  - sesje zalogowane: scenariusze, wariant na pacjentach (35,5 tys. zł), 90,5% to nie górna granica.
- **Co się zmieniło w liczbach szkicu:** koszt testu 3,3–12,2 tys. zł zamiast 2,9–11,4 tys. zł; liczebność 487–1 823 zamiast 422–1 687; wynik bez poprzedniego rocznika +3,1% obok +8,1%. Kierunek żadnego wniosku się nie zmienił.

## 9. Dopiski i decyzje Kuby

(po porannym przeglądzie)
