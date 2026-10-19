# A5 — retencja (sesja „A5: retencja”, 2026-10-19)

Notatka robocza sesji retencji. Sesja prowadząca scali stąd wpisy do wspólnych notatek (`ZALOZENIA.md`, `ZNALEZISKA.md`, `DECYZJE.md`, `PLAN.md`, `PRZEKAZANIE.md`, `analiza/README.md`). Tych plików ta sesja nie edytuje.

## Stan

| Krok | Co | Stan |
|---|---|---|
| 1 | Wspólny moduł definicji `analiza/definicje.py` | zrobione (`c5b17ea`), odtwarza sekcję 6 raportu A4 co do znaku |
| 2 | Kohorty dzienne, powroty 30/60/90, zamówienia i marża na pacjenta | zrobione (`e858e69`, uzupełnione przy kroku 3) |
| 3 | Struktura pacjentów a ich zachowanie, Meta po kampaniach — STOP 1 | przyjęte przez Kubę z dopiskami (niżej); recenzja Codeksa (Sol) uwzględniona (`notatki/recenzje/a5r_codex.md`) |
| 4 | Po zakupie (najpierw punktualność i obciążenie internistów), newsletter i SMS a powroty | zrobione |
| 5 | Zdarzenia w seriach — STOP 2 | do zrobienia |

## Krok 1 — wspólny moduł definicji

- `analiza/definicje.py`: przyjęte definicje z A4 jako funkcje, które tworzą tabele tymczasowe na połączeniu tylko do odczytu. `D.polacz()`, potem `D.zbuduj(con)` albo po kolei `zbuduj_podstawy`, `zbuduj_kohorty`, `zbuduj_zrodla`, `zbuduj_crm`, `zbuduj_ekonomie`.
- Tabele: `zam`, `ses`, `przeg`, `ses_pac`, `koh` (nowy pacjent N1), `powr` (kolumna `dni_R2`), `sp`, `reg`, `zr` (reguły Z1, Z2, Z1K w długim formacie), `zrodlo` (Z1K i Z2 w jednym wierszu na pacjenta), `logow`, `kontakt`, `po_kontakcie_wszystkie`, `po_kontakcie`, `crm_rozl` (rozłączne przypisanie zamówienia do ostatniego wejścia z CRM), `ek` (zdarzenia pieniężne pacjenta z dniem od wejścia do kohorty: przychód po zwrotach, TelemediGO, koszt lekarza, marża). Funkcje SQL: `stopy()` i `stopy_por()` (porównanie na tych samych dniach kalendarzowych, z liczbą pacjentów), `granice_por(n)`.
- Różnice wobec `a4_definicje.py`: tylko przyjęte warianty (bez N2–N4, R1, R3, R4, Z1b, Z3), więc `koh` i `powr` nie mają kolumny `war`. Parametr `dni_obserwacji` w `zbuduj_crm` (domyślnie 61 jak w A4; do samego okna 24 godzin wystarczy 1).
- Kontrola: `python -I analiza/a5r_kontrola_definicji.py` liczy podpunkty 6a–6e na tabelach modułu i porównuje z `analiza/wyniki/a4_definicje.txt`. Wynik: 53 wiersze, 0 różnic (`analiza/wyniki/a5r_kontrola_definicji.txt`), także po dopisaniu ekonomii.
- Import w skrypcie uruchamianym przez `python -I`: `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`, potem `import definicje as D` (tryb `-I` nie dodaje folderu skryptu do ścieżki).

## Krok 2 — kohorty, powroty, marża na pacjenta (`analiza/a5r_kohorty.py`, raport `analiza/wyniki/a5r_kohorty.txt`, kohorty dzienne `analiza/wyniki/a5r_kohorty_dzienne.csv`)

Wszystko na tych samych dniach kalendarzowych (ZALOZENIA.md 27), tylko kohorty z pełnym oknem.

- **Powrót spada w każdym oknie.** W 30 dniach 11,0% (14 984 pacjentów) wobec 7,8% (22 646). W 60 dniach 19,1% (13 941) wobec 13,7% (20 823). W 90 dniach 23,9% (12 867) wobec 17,4% (18 924). W 180 dniach 27,5% (9 125) wobec 22,2% (12 591).
- **Krzywa „dzień od pierwszego zakupu”:** okres 2 ma od 7. do 90. dnia stale około 72–75% powrotu okresu 1. Dłuższe okna (180 i 270 dni) wyglądają lepiej (0,81 i 0,89), ale obejmują tylko najstarsze kohorty okresu 2 (X 2025 – III 2026), więc nie świadczą o nadrabianiu.
- **Marża na pacjenta przed kosztem pozyskania** (przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza): w 90 dniach 66,6 zł wobec 58,3 zł (−8,3 zł, −12,5%); w 30 dniach 55,9 zł wobec 49,9 zł; w 180 dniach 75,5 zł wobec 67,7 zł. Kolejne zamówienia na pacjenta w 90 dniach: 0,334 wobec 0,234.
- **Kohorty miesięczne:** w okresie 1 powrót w 90 dniach mieści się między 21,3% a 26,3%. Październik 2025 jest jeszcze na tym poziomie (23,5%). Od listopada 2025 spada do 18,9–20,0%, a od marca 2026 do 13,7–15,6%. Kohorty tygodniowe pokazują te same dwa progi: tydzień od 3.11.2025 i tydzień od 2.03.2026.
- **Start od zera:** w okresie 2 jest 38 491 zamówień: 24 687 pierwszych, 5 289 powtórnych od pacjentów z kohort okresu 1 i 8 515 powtórnych od pacjentów z kohort okresu 2. W okresie 1 było 24 716 zamówień: 16 231 pierwszych i 8 485 powtórnych. Powtórne zamówienia rosną więc o 62,7%, ale 5 289 z nich to baza z okresu 1, której w okresie 1 z definicji nie było.
- **Koszt pediatry (wrażliwość):** wariant 25 zł zamiast 100 zł podnosi marżę na pacjenta w 90 dniach o 4,8 zł w okresie 1 i o 3,7 zł w okresie 2 (różnica kosztu: 84 300 zł i 110 700 zł). Kierunek zmiany się nie zmienia.

## Krok 3 — struktura pacjentów a ich zachowanie (`analiza/a5r_struktura.py`, raport `analiza/wyniki/a5r_struktura.txt`)

Metoda: rozkład zmiany powrotu na nowe segmenty (komórki bez pacjentów w okresie 1), strukturę i zachowanie w komórkach obecnych w obu okresach (rozkład symetryczny), na coraz drobniejszych podziałach: kampania, pierwsza usługa, zniżka pierwszego zamówienia, status pierwszego zamówienia, przeglądarka. Okno 90 dni, te same dni kalendarzowe. Wynik nie jest dowodem przyczyny.

- **Liczby Codeksa powtórzone naszym kodem:** 23,60% (okres 1 w całości, 16 231 pacjentów), 17,38% (okres 2 do 2.07.2026, 18 924), 21,29% przy strukturze kanałów okresu 1, 23,72% w okresie 1 bez kohort z października 2024 (14 946 pacjentów). Zgodne co do setnej części procenta.
- **Rozkład spadku z 23,9% do 17,4% (−6,5 punktu procentowego):**
  - na poziomie kanału (jak Codex): struktura −1,7, TikTok jako nowy kanał −1,0, zachowanie w kanałach −3,8;
  - na poziomie kampanii (wynik główny): w rozkładzie opisowym **obecność pacjentów przypisanych do dwóch nowych kampanii na L4 odpowiada za 4,61 z 6,53 punktu**, struktura pozostałych kampanii +0,08, a reszta (−1,99) to spadek w kampaniach obecnych w obu okresach. To nie jest efekt przyczynowy: nie wiemy, gdzie ci pacjenci kupiliby bez tych kampanii ani czy kupiliby w ogóle, więc nie wynika z tego, że wyłączenie kampanii podniosłoby retencję (recenzja Codeksa);
  - drobniejsze podziały (usługa, zniżka, status pierwszej wizyty, przeglądarka) nie zmieniają obrazu: zachowanie w komórkach wspólnych −2,0 do −2,1 punktu.
- **Bez pacjentów dwóch nowych kampanii** (`meta_prosp_l4_szybko`, `tt_prosp_l4_15min`): 23,9% (12 867) wobec 22,0% (14 031), czyli −1,9 punktu procentowego (95% przedział od −2,9 do −0,9). Uwzględnione cechy (usługa, zniżka, status pierwszej wizyty, przeglądarka, miesiąc kohorty) nie wyjaśniają tej różnicy; „zachowanie” to reszta, nie rozpoznana przyczyna. W najdrobniejszym podziale 261 z 409 komórek wspólnych ma mniej niż 10 pacjentów w którymś okresie (7,6% pacjentów), więc drobne podziały traktujemy jako kontrolę.
- **Meta po kampaniach (hipoteza Kuby):** spadek w kanale z 21,2% do 6,7% (−14,6 punktu) w dwóch trzecich wynika ze składu: nowa kampania na L4 ma 3 628 pacjentów (81% pacjentów Meta pozyskania w okresie 2) i powrót 4,5% (−9,5 punktu). Stara kampania `meta_prosp_lekarz_online` też spada: z 21,2% (786 pacjentów) do 16,2% (835), czyli −5,1 punktu (przedział od −8,9 do −1,3). Jej struktura usług, zniżek i statusów się nie zmienia (struktura +0,0 do +0,5 punktu).
- **L4 z L4 (sezon i usługa):** pacjenci z pierwszym L4 u internisty z pozostałych kanałów wracają w 14,8% (2 639) wobec 13,9% (2 797), bez istotnej zmiany (przedział od −2,7 do +1,0). Pacjenci L4 z nowej kampanii Meta wracają w 4,3% (3 016), z TikToka w 2,8% (1 060). Na wspólnych datach pozyskania (kohorty 9.02–2.07.2026) jest tak samo: kampania Meta na L4 4,1% (2 200), TikTok 2,8% (1 060), pozostałe kanały 14,4% (1 364). Różnica utrzymuje się dla tej samej usługi i wspólnych dat pozyskania; zmiana struktury miesięcy jej nie wyjaśnia (bez nowych kampanii: struktura miesięcy +0,04, spadek w miesiącach −1,96 punktu).
- **Kod rabatowy nie różnicuje:** w kampanii Meta na L4 pacjenci z kodem L4SZYBKO20 wracają w 4,0%, bez kodu w 4,8%.
- **TikTok osobno:** powrót 2,1% w 30 dniach (1 874 pacjentów), 2,9% w 60 (1 562) i 3,2% w 90 (1 265), wobec 7,6%, 13,4% i 16,7% w pozostałych kanałach w tych samych dniach od 9.02.2026. Bez TikToka okres 2 ma 18,4% zamiast 17,4%.
- **Marża na pacjenta w 90 dniach:** 66,6 zł wobec 58,3 zł. Na poziomie kampanii −7,7 z −8,3 zł przypada na nowe kampanie. Bez nich 66,6 zł wobec 66,0 zł: marża pierwszego zamówienia bez zmian (50,0 i 50,4 zł), marża dni 1–90 spada z 16,6 do 15,6 zł. Pacjenci nowych kampanii: 36,3 zł (34,0 zł z pierwszego zamówienia, 2,2 zł z dni 1–90).
- **Kontrole:** ten sam obraz w oknach 30 i 60 dni, bez kohort z października w obu okresach (−7,2 punktu, z tego −5,0 nowe kampanie i −2,6 zachowanie), przy okresie 1 w całości. **Źródło według sesji płatności zmienia podział spadku między nowe i stare kampanie:** na poziomie kampanii nowe kampanie −3,03, struktura +0,04, zachowanie −3,54 punktu (wobec −4,61 / +0,08 / −1,99 według przyjętej reguły). Według sesji płatności do nowych kampanii trafia 3 510 pacjentów zamiast 4 893. Kierunek jest odporny, podział zależy od reguły źródła. Możliwy powód, do oceny: pacjenci z kodem nowych kampanii często płacą w sesji bezpośredniej, z wyszukiwania marki albo z remarketingu (`ZNALEZISKA.md`, A4, punkt 6), więc sesja płatności przenosi ich do starych kampanii.
- **Pozostałe kampanie rok do roku** (bez dwóch nowych, powrót w 90 dniach): spadek w listopadzie–styczniu (−2,8 do −4,2 punktu) i w marcu–maju (−2,3 do −3,1), bez spadku w październiku (+1,3) i lutym (+1,2). Najbardziej spadają `gs_generic_erecepta` (32,4% → 27,8%) i `meta_prosp_lekarz_online`. Przyczyna otwarta (krok 4: przebieg wizyty, CRM).
- **Do sprawdzenia w kroku 5:** powrót w 30 dniach pozostałych kanałów w lipcu i sierpniu 2026 jest wyższy niż rok wcześniej (11,9% wobec 9,0% i 11,1% wobec 10,0%).

### Otwarte po kroku 3 (nie wnioski)
- Czy pacjenci nowych kampanii to pacjenci dodatkowi, czy przejęci z innych kanałów. Liczba nowych pacjentów z pozostałych kanałów rośnie (12 081 → 13 196 w próbie 90 dni), ale to sprawa pozyskania.
- Co obniża powrót w kampaniach obecnych w obu okresach (−1,9 punktu) i w starej kampanii Meta (−5,1 punktu). Kandydaci do kroku 4: przebieg wizyty, zwroty, komunikacja po zakupie.
- Dlaczego pacjenci kampanii na L4 nie wracają (obietnica „szybkie L4”, jednorazowa potrzeba, zwroty po wizycie 14,1% pierwszych zamówień w kampanii Meta na L4). To pytanie do kroku 4 i do listy niewiadomych.

## Krok 4 — po zakupie (`analiza/a5r_punktualnosc.py` → `wyniki/a5r_punktualnosc.txt` i `a5r_punktualnosc_tygodnie.csv`; `analiza/a5r_po_zakupie.py` → `wyniki/a5r_po_zakupie.txt`)

Kolejność według dopisku Kuby: najpierw punktualność pierwszej wizyty i obciążenie internistów. Opóźnienie = faktyczny start − umówiony termin (minuty, tylko wizyty odbyte). Obciążenie = nieanulowane wizyty u internisty umówione na tę samą godzinę zegarową. Kampanie „stare” = obecne w obu okresach (bez `meta_prosp_l4_szybko` i `tt_prosp_l4_15min`). Okno 90 dni, te same dni kalendarzowe. Obserwacje, nie wnioski.

### 4a. Punktualność i obciążenie (hipoteza Kuby o przeciążeniu internistów)
- **Opóźnienia rosną tylko u internisty rano i od startu kampanii Meta na L4.** Wizyty u internisty z terminem 6:00–11:59, które zaczęły się ponad 15 minut po terminie: 4,1–6,4% w każdym miesiącu od X 2024 do X 2025, potem 14,3% w listopadzie 2025, 27,4% w grudniu, 39,9% w styczniu 2026, 46,6% w lutym i 46–51% do września 2026. U internisty w innych porach 1–3% przed i 4–6% po. U specjalistów bez zmian (1–4%).
- **Tydzień po tygodniu przebieg idzie za ruchem kampanii:** u pacjentów spoza nowych kampanii odsetek porannych wizyt spóźnionych ponad 15 minut to 3,5–7,4% w październiku 2025, 6,2% w tygodniu startu (3.11), 12,4% tydzień później, 16,7% w tygodniu skoku z 17.11, 22–31% w grudniu (skok 8.12), 36–43% w styczniu (skoki 2.01 i 19.01) i 45–50% od lutego (start TikToka 9.02).
- **Obciążenie:** rano u internisty średnio 2,73 wizyty na godzinę z terminami w okresie 1 i 4,43 w okresie 2, z czego 1,27 to pacjenci nowych kampanii. Ich udział w porannych wizytach u internisty rośnie z 6,8% (XI 2025) do około 40% (od VI 2026). W okresie 1 opóźnienie prawie nie zależy od obciążenia godziny (3,5–5,0 minuty średnio), w okresie 2 rośnie z nim (6,3 minuty przy 1–2 wizytach, 15,4 przy 10–14).
- **Przy tym samym obciążeniu godziny** wizyty pacjentów spoza nowych kampanii (okres 2, rano) są częściej spóźnione, gdy w tej godzinie są też wizyty z nowych kampanii: przy obciążeniu do 4 wizyt 27,9% ponad 15 minut bez wizyt z nowych kampanii wobec 45,6% przy 1–2 takich wizytach.
- **Czego to nie jest:** długość wizyty się nie zmienia (średnio 8,5 minuty u internisty w obu okresach, wizyty L4 z nowych kampanii też 8,5). Czas od zapłaty do terminu też nie (mediana 37–41 minut, ponad 2 godziny czeka 23–26% w każdym miesiącu). W danych nie ma grafików lekarzy, więc nie widać, czy rano ubyło lekarzy, czy przybyło pacjentów na tylu samych lekarzy. Dane pasują do hipotezy Kuby, ale jej nie dowodzą.
- **Pierwsza wizyta pacjentów starych kampanii u internisty rano:** ponad 15 minut opóźnienia 5,5% (2 656 wizyt) w okresie 1 wobec 36,1% (2 893) w okresie 2; ponad 30 minut 1,2% wobec 17,7%. Powrót w 90 dniach tych pacjentów: 23,6% (2 844) wobec 19,0% (3 117), czyli −4,6 punktu procentowego. Wieczorem 23,5% wobec 23,5%.
- **Rano spada powrót po wizytach spóźnionych, nie po punktualnych:** zaczęte do 5 minut po terminie 24,9% wobec 26,5%; 6–15 minut 23,0% wobec 19,2%; 16–30 minut 20,4% wobec 16,1%; ponad 30 minut 15,2% wobec 9,8%.
- **Powrót a opóźnienie pierwszej wizyty (stare kampanie, wszystkie pory i specjalizacje):** do 5 minut 25,1% i 24,1%; ponad 30 minut 7,4% i 9,8%. Udział pierwszych wizyt spóźnionych ponad 15 minut rośnie z 2,9% do 10,0%.
- **Ile spadku w starych kampaniach przypada na zmianę punktualności pierwszej wizyty (rozkład opisowy):** z −1,91 punktu procentowego według przyjętej reguły źródła 0,83 punktu na samym podziale według opóźnienia, 0,58 przy kampanii × usłudze × opóźnieniu, 0,42 z porą terminu. Według sesji płatności z −3,50 punktu: 0,86, 1,28 i 1,09. Około połowa spadku w starych kampaniach (−4,6 punktu na 3 117 pacjentach, czyli około 1,0 z 1,9 punktu) to pacjenci z pierwszą wizytą u internisty rano.
- **Miesiące (dopisek Kuby nr 3):** w listopadzie–styczniu spadek w starych kampaniach to −3,3 punktu, z czego 0,5 przypada na opóźnienie; w marcu–maju −2,8, z czego 0,7. W październiku i lutym spadku nie ma (+1,3), choć w lutym 13,8% pierwszych wizyt starych kampanii jest spóźnionych ponad 15 minut. Opóźnienie nie tłumaczy więc całego wzoru miesięcy. Sprawdzamy w kroku 5.
- **Oceny:** wizyty spóźnione ponad 30 minut mają średnią ocenę 2,9 (32% ocen 1–2) wobec 4,5 przy wizytach na czas (1% ocen 1–2), w obu okresach tak samo. Ocenę wystawia około 30% pacjentów.

### 4b. Pozostały przebieg wizyty
- **Zwroty po odbytej wizycie skupiają się w L4 z nowych kampanii:** 17,4% odbytych wizyt L4 pacjentów nowych kampanii (5 895 wizyt) wobec 5,3% L4 pozostałych pacjentów w okresie 2 i 6,0% w okresie 1. W e-recepcie, konsultacji i skierowaniu 0,8–2,4%. Kod rabatowy nie zmienia odsetka (L4SZYBKO20 16,5%, bez kodu 16,5%; TIKTOK25 15,6%, bez kodu 15,7%). Zwrot nie zależy od opóźnienia (1,6–2,6% w każdym koszyku). Możliwe odczytania (do oceny Kuby): lekarz nie wystawia L4, którego pacjent oczekuje po obietnicy reklamy („szybkie L4”, „L4 w 15 minut”), albo inna przyczyna. W danych nie ma powodu zwrotu.
- **Anulowane i nieodebrane** u pacjentów spoza nowych kampanii bez zmian w czasie (anulowane 3,3–5,1%, nieodebrane 1,8–3,0% miesięcznie).
- **Czekanie, ocena i zgoda marketingowa nie tłumaczą spadku w starych kampaniach** (struktura od −0,0 do +0,2 punktu w rozkładzie).

### 4c. Newsletter i SMS a powroty (na poziomie pacjenta, okno 24 godzin)
- **Pacjenci nowych kampanii są dla CRM prawie niedostępni:** zgodę marketingową ma 37,8% z nich wobec 63,8–64,4% pacjentów starych kampanii. Wejście z CRM w dniach 1–90 ma 8,2% wobec 17,5–17,9%.
- **W starych kampaniach kontakt z CRM się nie zmienia** (17,5% i 17,9% pacjentów, 0,21 i 0,22 wejścia na pacjenta w 90 dniach). Powrót przypisany do wejścia z CRM: 3,48% wobec 3,16% kohorty (−0,32 punktu); powrót bez CRM: 20,42% wobec 18,84% (−1,59 punktu). Spadek jest więc głównie poza CRM.
- **Skuteczność wejścia z CRM spada lekko:** zamówienia nieanulowane w 24 godziny na 1 000 wejść (bez `crm_go_upsell`) 158–275 w okresie 1 i 145–199 w okresie 2; najniżej od lipca 2026 (145–158).
- **Liczba wejść z CRM nie rośnie z bazą pacjentów:** na 1 000 pacjentów po pierwszym zakupie 56–108 wejść miesięcznie w okresie 1 i spadek do 24–52 w okresie 2. Widać tylko kliknięcia, nie wysyłki, więc nie wiemy, czy wysyłek jest mniej, czy mniej osób klika.
- Pacjenci, którzy klikają CRM, wracają w 41–42% w obu okresach; to pacjenci z zamiarem zakupu, więc nie jest to miara skutku wiadomości (test z grupą kontrolną: lista niewiadomych).

## Propozycje wpisów do wspólnych notatek (do scalenia przez sesję prowadzącą)

### `ZALOZENIA.md` (nowe punkty od 28)
28. **Koszt lekarza u pediatry = 100 zł**, jak u „każdego innego specjalisty”. Podstawa: zasada z zadania wymienia osobno tylko internistę (25 zł) i psychiatrę (200 zł), a wszystkim pozostałym przypisuje 100 zł. Dodatkowa przesłanka: TelemediGO traktuje pediatrę jak specjalistów (zniżka 20%, nie 50%). Codex (Sol) uznał to za rozsądne. Wariant 25 zł: koszt niższy o 84 300 zł w okresie 1 i 110 700 zł w okresie 2; marża na pacjenta w 90 dniach wyższa o 4,8 i 3,7 zł. Kierunek wniosków bez zmian. Psycholog też liczy się jako inny specjalista (100 zł).
29. **Marża na pacjenta (przed kosztem pozyskania)** = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza (za wizyty odbyte i zwrócone), narastająco od dnia wejścia do kohorty (dzień 0, z pierwszym zamówieniem i TelemediGO kupionym przy kasie) do dnia N, tylko kohorty z pełnym oknem N dni. „Miesiąc” od pierwszego zakupu = kolejne 30-dniowe bloki (miesiąc 1 = dni 0–30). Koszt pozyskania (kampanie, prowizja) odejmuje sesja prowadząca przy ekonomii kampanii.
30. **Cechy pierwszego zakupu w podziałach kohort:** pierwsza usługa = internista według celu wizyty (L4, e-recepta, konsultacja, skierowanie), pediatra, psychiatra, inny specjalista; zniżka = brak, TelemediGO albo kod rabatowy; przeglądarka = wbudowana w aplikację (Instagram, Facebook, TikTok) albo zwykła, z sesji płatności; urządzenie z sesji płatności.
31. **Struktura a zachowanie:** rozkład zmiany na nowe segmenty (komórki bez pacjentów w okresie 1), zniknięte segmenty, strukturę i zachowanie w komórkach wspólnych (rozkład symetryczny), na podziałach od kanału do kampania × usługa × zniżka × status pierwszego zamówienia × przeglądarka. Status pierwszej wizyty może sam zależeć od kampanii, więc pokazujemy rozkład z nim i bez niego. Wynik nie jest dowodem przyczyny.

### `ZNALEZISKA.md` (sekcja „A5 retencja”) — po przeglądzie Kuby
- Treść z kroku 3 powyżej, po decyzji Kuby, które zdania są wnioskami.

### `analiza/README.md`
- `python -I analiza/a5r_kontrola_definicji.py` — kontrola wspólnego modułu `analiza/definicje.py` wobec sekcji 6 raportu A4. Wynik: `wyniki/a5r_kontrola_definicji.txt`.
- `python -I analiza/a5r_kohorty.py` — kohorty dzienne, powroty w 30/60/90 dniach, zamówienia i marża na pacjenta, kohorty miesięczne i tygodniowe, start od zera, wrażliwość na koszt pediatry. Wynik: `wyniki/a5r_kohorty.txt`, `wyniki/a5r_kohorty_dzienne.csv`.
- `python -I analiza/a5r_punktualnosc.py` — opóźnienie wizyt, pora, obciążenie godzin u internisty, powrót według opóźnienia pierwszej wizyty, opóźnienia w czasie. Wynik: `wyniki/a5r_punktualnosc.txt`, `wyniki/a5r_punktualnosc_tygodnie.csv`.
- `python -I analiza/a5r_po_zakupie.py` — czekanie, długość wizyty, statusy i zwroty, oceny, rozkład z przebiegiem pierwszej wizyty, newsletter i SMS a powroty. Wynik: `wyniki/a5r_po_zakupie.txt`.
- `python -I analiza/a5r_struktura.py` — rozdzielenie zmiany struktury pacjentów od zmiany zachowania (kanał, kampania, usługa, zniżka, przebieg pierwszej wizyty, przeglądarka), Meta po kampaniach, L4 z L4, TikTok osobno, kontrole wrażliwości, niepewność. Wynik: `wyniki/a5r_struktura.txt`.

## Dopiski Kuby

### 2026-10-19, przegląd STOP 1 (krok 3 przyjęty z poprawkami po Codeksie)
1. **Zapis na teraz:** większość spadku powrotów wiąże się z pacjentami dwóch nowych kampanii na L4, ale w kampaniach działających w obu latach też jest spadek, którego sprawdzone cechy nie tłumaczą. Podział zależy od reguły źródła, więc w notatkach i w narzędziu podajemy obie wersje (pierwsze wejście z kodem kampanii: 4,6 i 2,0 punktu; sesja płatności: 3,0 i 3,5 punktu).
2. **„Przebieg pierwszej wizyty” w kroku 3 to był tylko status, bez punktualności.** W kroku 4 najpierw: czy spadek w starych kampaniach siedzi w pierwszych wizytach, które zaczęły się z opóźnieniem, według godziny i specjalizacji, zwłaszcza u internisty rano. Czy opóźnienia rosną od startu kampanii na L4 (3.11.2025) i przy kolejnych skokach jej ruchu (17.11, 8.12.2025, 2.01, 19.01.2026 — notatka sesji pozyskania) oraz od startu TikToka (9.02.2026). **Hipoteza Kuby do sprawdzenia, nie do założenia:** nowe kampanie przeciążyły internistów w godzinach, w których przychodzą też pozostali pacjenci. Jeśli tak, koszt tych kampanii obejmuje też gorszą retencję pozostałych pacjentów.
3. **Spadek w starych kampaniach jest w listopadzie–styczniu i w marcu–maju, nie w październiku i lutym.** Przy zdarzeniach w kroku 5 zestawiamy te miesiące z datami startu i skoków kampanii na L4 oraz z opóźnieniami wizyt.

Propozycja wpisu do `DECYZJE.md` (sesja prowadząca): „2026-10-19 — wynik kroku 3 retencji A5 przyjęty przez Kubę z poprawkami po recenzji Codeksa (Sol), z trzema dopiskami” + treść punktów 1–3.
