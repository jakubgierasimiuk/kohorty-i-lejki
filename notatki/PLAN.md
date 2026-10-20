# Plan pracy — zatwierdzony przez Kubę 2026-10-19 (wersja 2)

Kolejność: **wstępna analiza → narzędzie → uzupełnienie analizy → weryfikacja.** Bez dat — robimy, kiedy zrobimy.

## Zasady współpracy

- **Przed rozpoczęciem każdego punktu pytamy Kubę, czy idziemy dalej.** Żaden punkt nie startuje bez jego „tak”.
- Claude liczy i pokazuje wyniki. Wnioski wyciągamy razem. Po każdym większym kroku jest przegląd z Kubą — nic nie jest wnioskiem, dopóki go razem nie przyjmiemy. Wnioski weryfikujemy konsylium.
- Skrypty, które tylko czytają dane, Claude uruchamia bez pytania (bezpieczeństwo paczki zamknięte — punkt 0). Pyta przed: instalacją pakietów, rundą konsylium, publikacją, mailem.
- Stała zasada z CLAUDE.md, punkt 9: **najpierw napraw, potem wyłączaj.**
- Po każdym punkcie: aktualizacja tabeli statusu niżej, notatki (`ZALOZENIA.md`, `ZNALEZISKA.md`, `DECYZJE.md`) i commit po polsku.

## Status

| Punkt | Co | Status |
|---|---|---|
| 0 | Kontrola bezpieczeństwa paczki | zrobione (commit `e5897ac`, wynik w `ZNALEZISKA.md`) |
| A1 | Baza danych | zrobione (commit `025d6f0`, `analiza/a1_baza.py`, wynik w `analiza/wyniki/a1_baza.txt`) |
| A2 | Jakość danych | zrobione: raport (commit `b7466aa`), czyszczenie przyjęte przez Kubę, warstwa `czyste` (`analiza/a2_czyste.py`). Zamówienia testowe do ponownego przeglądu w punkcie D |
| A3 | Odtworzenie dashboardu | zrobione, przyjęte przez Kubę (commit `b91975a`, `analiza/a3_dashboard.py`, `analiza/wyniki/a3_dashboard.txt`) |
| A4 | Definicje (razem) | zrobione: definicje przyjęte przez Kubę (`ZALOZENIA.md` 16–27, `analiza/a4_definicje.py`, `analiza/wyniki/a4_definicje.txt`), recenzja Codeksa (Sol) uwzględniona (`notatki/recenzje/a4_codex.md`) |
| A5 | Pierwsze kohorty, lejek, po zakupie, zdarzenia | zrobione w całości: pozyskanie (`f240505`), retencja (`c5b17ea` … `f8fda6d`) i ekonomia kampanii (`d6f63e4` … `24ac35d`), wszystko przyjęte przez Kubę i scalone |
| B | Narzędzie | startuje przed końcem A5 (decyzja Kuby 2026-10-19): szkielet, czyli układ, lejek, oś zdarzeń i jakość danych; kohorty po drugim zatrzymaniu sesji retencji |
| C | Uzupełnienie analizy, priorytety, niewiadome | szkic przejrzany przez Kubę 2026-10-20 (kierunek przyjęty, cztery dopiski wprowadzone), konsylium zrobione (9 z 9, `notatki/konsylium/c_priorytety/synteza.md`); **ostateczna lista 12 priorytetów czeka na akceptację Kuby**: `notatki/c_szkic.md` — analiza TelemediGO (`analiza/c_telemedigo.py`), propozycja odpowiedzi „czy to wzrost”, lista 10 priorytetów z wartością w marży, lista 16 niewiadomych (`analiza/c_priorytety.py`); recenzja Codeksa (Sol) w `notatki/recenzje/c_codex.md`; brief konsylium przygotowany, niewysłany (decyzja Kuby rano) |
| D | Weryfikacja, publikacja, mail | do zrobienia |

---

## A. Wstępna analiza

### A1. Baza
- Sprawdzić, czy są zainstalowane DuckDB i pandas. Jeśli nie — zapytać Kubę o instalację z oficjalnego repozytorium pakietów Pythona (PyPI).
- Załadować wszystkie CSV do DuckDB (plik bazy w `analiza/`, poza repozytorium).
- Czas sesji i zdarzeń przeliczyć z UTC na czas polski (Europe/Warsaw, ze zmianą czasu).

### A2. Jakość danych — każda tabela osobno
- **Duplikaty w każdej tabeli osobno:** wiersze identyczne w całości, ten sam identyfikator z różną treścią. **Kiedy występują:** dni, godziny, styki plików kwartalnych i półrocznych.
- **TEST-QA (1 810 zamówień):** kto je składa (ile kont, czy te same, jak wyglądają te konta), kiedy (rozkład w czasie i porach dnia), czy wizyty się odbyły (status, faktyczny start, czas trwania, kwota, zwrot), czy mają sesje i zdarzenia w analityce, czy powstał koszt lekarza.
- **Kliknięcia z `marketing_spend.csv` wobec sesji z tych samych kampanii, dzień po dniu:** stosunek sesji do kliknięć, dni z kosztem bez sesji, sesje bez kosztu (Bing).
- **Czas zamówienia (system transakcyjny) wobec czasu płatności w analityce po przeliczeniu strefy:** różnica o godzinę albo dwie = źle przeliczona strefa; różnica zmienna przy zmianie czasu = źle obsłużony czas letni.
- **Pozostałe:** zamówienia bez sesji albo bez zdarzenia płatności, zwroty większe niż zapłata, cena niezgodna ze zniżką, luki w zbieraniu danych, kolejność kroków lejka, TelemediGO wobec zamówień, zamówienia sprzed założenia konta.

**Stop — przegląd z Kubą:** raport jakości danych.

### A3. Dashboard odtworzony dokładnie
- Siatka wariantów definicji: z duplikatami i bez, z TEST-QA i bez, przychód przed i po zwrotach, które statusy się liczą, granice okresów w UTC albo w czasie polskim, czy pierwszym zakupem może być sam TelemediGO.
- Szukamy kombinacji, która daje **dokładnie wszystkie cztery liczby naraz:** +52% pacjentów z pierwszym zakupem, +61% zamówień, +50% przychodu z konsultacji, +40% sprzedanych TelemediGO. Procenty na dashboardzie są zaokrąglone do całości, więc może pasować kilka kombinacji — wtedy pokazujemy wszystkie pasujące i razem wybieramy najbardziej prawdopodobną.
- Wynik: jak liczony jest dashboard + zestawienie obok siebie: miary dashboardu i te same miary po oczyszczeniu.

**Stop — przegląd z Kubą.**

### A4. Definicje — ustalamy razem, zanim policzymy kohorty
Przy każdej: warianty i to, ile każdy zmienia w liczbie nowych pacjentów, w powrotach i w strukturze źródeł.
- **Nowy pacjent:** pierwsze opłacone zamówienie konsultacji / pierwsza jakakolwiek płatność, łącznie z samym TelemediGO / pierwsza wizyta, która się odbyła. Czy łączymy konta, które dzielą tę samą przeglądarkę.
- **Powrót:** kolejne opłacone zamówienie / kolejna wizyta, która się odbyła / czy zakup TelemediGO liczy się jako powrót. Okna 30, 60, 90 dni.
- **Źródło pozyskania:** pierwsze wejście pacjenta / sesja, w której zapłacił / ostatnie wejście z oznaczonego źródła (nie bezpośrednie) w oknie przed zakupem. Łączenie anonimowych sesji z kontem przez identyfikator przeglądarki. *(dopisane 2026-10-19 po A2)* Kody kampanii na pierwszym zamówieniu (L4SZYBKO20 — Meta, TIKTOK25 — TikTok, RANKING10 — ranking lekarzy) służą jako kontrola każdej reguły; obok pokazujemy wariant, w którym kod wskazuje źródło. Prowizję afiliacyjną liczymy tą samą regułą, którą wybierzemy dla źródła; drugi wariant (po kodzie RANKING10) jedną liczbą obok. Jeśli różnica jest mała, nie poświęcamy temu więcej czasu.
- **Anulacje i zwroty:** czy pacjent z anulowanym pierwszym zamówieniem jest nowym pacjentem, czy anulowany powrót jest powrotem, jak liczymy przychód netto.

- *(dopisane 2026-10-19, decyzja Kuby)* Przed zamknięciem A4 recenzja definicji przez Codeksa (model Sol, profil `review`): czy definicje odpowiadają pytaniu zadania, czy czegoś nie brakuje w wariantach i pułapkach, czy kod liczy to, co mówią definicje, na kilku konkretnych pacjentach. Przeniesione z punktu D.

**Stop — przyjmujemy definicje razem.** Zapis w `notatki/ZALOZENIA.md`.

### A5. Pierwsze kohorty dzienne, lejek, to, co dzieje się po zakupie, zdarzenia
- **Kohorty:** powrót w 30/60/90 dniach, zamówienia na pacjenta, marża na pacjenta w kolejnych miesiącach. Podziały: źródło i kampania, urządzenie i przeglądarka, pierwsza usługa, zniżka i TelemediGO.
- **Lejek:** od sesji do płatności, dzień po dniu, w tych samych podziałach. Uwzględnić wyjątki z README: pacjent zalogowany na wejściu nie ma kroku logowania; zakup samego TelemediGO ma tylko dwa ostatnie kroki.
- **Sesje zalogowane od wejścia** *(dopisane 2026-10-19 po A2, decyzja Kuby)*: w lejku osobny wiersz. Pogłębienie: na którym kroku odpadają; z jakich stron i kampanii przychodzą (np. przypomnienie o recepcie — pacjenci, którzy chcą ją przedłużyć); czy kupują potem rzadziej niż podobni pacjenci bez takich sesji; czas między wyborem terminu a krokiem logowania w zakupach powtórnych (kilkadziesiąt sekund = prawdziwe logowanie, 1–2 sekundy = raczej automatyczny zapis dla zalogowanych).
- **Po zakupie, w czasie:** czy wizyta się odbyła, czy zaczęła się na czas (faktyczny start wobec umówionego terminu), ile pacjent czekał od zapłaty do terminu, zwroty, nieodebrane wizyty, oceny. Czy pacjent ze spóźnioną, nieodbytą albo zwróconą wizytą wraca rzadziej. Kampanie komunikacji po zakupie widoczne w sesjach (`crm_reactivation`, `crm_recepta_przypomnienie`, `crm_sms_przypomnienie`, `crm_go_upsell`): od kiedy działają i czy zmieniają powroty. Newsletter i SMS oceniamy na poziomie pacjenta (powrót w ciągu kilku dni od kontaktu), nie konwersją sesji — wejścia z nich są często zalogowane, a zakup dzieje się w innej sesji.
- **Wykrywanie zdarzeń:** w każdej serii dziennej szukamy dni, od których zmienia się poziom. Każde zdarzenie: data, co się zmieniło, o ile, jaki wpływ na marżę.
- *(dopisane 2026-10-19 po A4, decyzje Kuby)* **Definicje:** `ZALOZENIA.md` 16–26. **Ekonomia kampanii** (koszt pozyskania, wynik na pacjenta) według przyjętej reguły źródła, a obok według sesji płatności. Jeśli wynik kampanii zmienia znak zależnie od reguły, opisujemy go jako niepewny. **Wejścia z newslettera i SMS-ów zalogowane od wejścia** (dwie trzecie wejść z CRM, bez zakupu w sesji) dołączamy do sprawy sesji zalogowanych, bo CRM to główny kanał powrotów. **Tropy z A4** (`ZNALEZISKA.md`, A4): spadek powrotu w obrębie Meta (pozyskanie), zwroty po wizycie przy pierwszym zamówieniu z Meta i TikToka, zmiana struktury źródeł.
- **Wykonanie A5** *(decyzja Kuby 2026-10-19)*: dwie sesje równoległe.
  - **Sesja retencji:** na start przenosi przyjęte definicje do wspólnego modułu `analiza/definicje.py` i robi commit. Potem: kohorty dzienne; powroty w 30, 60 i 90 dniach; rozdzielenie zmiany struktury pacjentów od zmiany ich zachowania, co najmniej po kampanii, pierwszej usłudze, zniżce i przebiegu pierwszej wizyty; to, co dzieje się po zakupie (czy wizyta się odbyła, czy na czas, zwrot, ocena), i czy to zmienia powroty; zdarzenia w tych seriach. **Spadek powrotu w Mecie sprawdzamy na poziomie kampanii**, bo w drugim roku w Mecie pojawiła się nowa kampania na L4. Zdanie, że sama zmiana struktury źródeł nie tłumaczy spadku w Mecie, to na razie hipoteza. Zatrzymuje się u Kuby po rozdzieleniu struktury od zachowania (odpowiedź na główne pytanie) i na końcu.
  - **Sesja pozyskania:** lejek od sesji do płatności dzień po dniu, w podziałach na urządzenie, przeglądarkę, źródło i stronę wejścia; zdarzenia w lejku; pogłębienie sprawy sesji zalogowanych od wejścia. Lejek liczy się na sesjach, więc rusza od razu na schemacie `czyste`. Zatrzymuje się u Kuby raz, na końcu.
  - **Zasady:** żadna sesja nie przebudowuje bazy. Każda zapisuje wyniki i notatki we własnych plikach. Wspólne notatki (`ZALOZENIA.md`, `ZNALEZISKA.md`, `DECYZJE.md`, `PLAN.md`, `PRZEKAZANIE.md`, `analiza/README.md`) scala sesja prowadząca po obu.
  - **Przydział pozostałych pozycji A5** (propozycja sesji prowadzącej, do korekty przez Kubę): sezon a wydatki trafia do sesji pozyskania. Wpływ newslettera i SMS-ów na powroty trafia do sesji retencji, a sesja pozyskania bada tylko to, co dzieje się w samych sesjach z newslettera i SMS-ów. Ekonomię kampanii (koszt pozyskania, wynik na pacjenta) liczy sesja prowadząca po scaleniu, bo potrzebuje powrotów z jednej sesji i lejka z drugiej.

**Jak obchodzimy pułapki:**
- **Start od zera.** W pierwszym roku każdy pacjent jest nowy i nie ma bazy powracających, więc roczne sumy zamówień i przychodu z definicji faworyzują drugi rok. Rozbijamy zamówienia i przychód na nowych i powracających. Porównujemy kohorty w tym samym wieku, nie sumy roczne. ~~Okres rozruchu (pierwsze tygodnie, kod startowy `START10`) oznaczamy osobno i sprawdzamy, czy wnioski trzymają się bez niego.~~ *(zmienione 2026-10-19 po A2, decyzja Kuby)* START10 działa przez całe dwa lata, a nowi pacjenci od pierwszego tygodnia są na zbliżonym poziomie — od zera rośnie tylko baza powracających. Osobnego okresu rozruchu nie wyznaczamy. Sprawdzamy, czy wnioski o retencji trzymają się bez kohort z października 2024.
- **Młode kohorty miały mniej czasu na powrót.** Każdą miarę powrotu liczymy tylko dla kohort, które miały pełne okno (powrót w 90 dni — tylko kohorty do 2 lipca 2026). Porównujemy krzywe „dzień od pierwszego zakupu”. W narzędziu niedojrzałe komórki są wyszarzone.
- **Sezon a wydatki** *(dopisane 2026-10-19)*: liczba nowych pacjentów rośnie od października 2024 do stycznia 2025, ale w tym samym czasie rosną wydatki na kampanie. Rozdzielamy wpływ sezonu i wydatków (np. pozyskanie na złotówkę wydatków, źródła bezpłatne osobno). Do tego czasu przyczyna wzrostu jest otwarta.
- **Sezonowość.** Jesień i zima = więcej infekcji, więcej L4 i e-recept. Porównujemy te same miesiące rok do roku i retencję w obrębie tej samej usługi (L4 z L4). W kohortach dziennych wygładzamy efekt dnia tygodnia (średnia z 7 dni albo porównanie z tym samym dniem tygodnia). Ograniczenie: dwa lata danych to jedna obserwacja każdego sezonu na rok — sezonowości nie oddzielimy w pełni od trendu; to trafia na listę „czego nie da się rozstrzygnąć”.
- **Zmiana struktury pacjentów.** Retencję porównujemy w obrębie tego samego źródła i tej samej usługi, bo zmiana udziału źródeł potrafi obniżyć retencję całości, choć w każdym źródle się nie zmienia. *(dopisane 2026-10-19 po recenzji Codeksa w A4)* Pokazujemy dwa wyniki: powrót całej pozyskanej bazy i powrót przy stałej strukturze kanałów z okresu 1; potem to samo dla pierwszej usługi i zniżki. TikTok (brak w okresie 1) pokazujemy jako nowy, osobny segment. Wynik po wyrównaniu struktury nie jest dowodem przyczyny.
- **Porównanie okresów** *(dopisane 2026-10-19, `ZALOZENIA.md` 27)*: na tych samych dniach kalendarzowych, z liczbą pacjentów przy każdym wyniku.

**Stop — wstępne wnioski z Kubą.** Potem propozycja rundy konsylium na wstępnych wnioskach (brief bez naszej opinii, do 3 USD).

---

## B. Narzędzie — dopiero po wspólnej wstępnej analizie
- Strona statyczna, dane przeliczone wcześniej do plików JSON, wykresy i filtry w przeglądarce. Technologię wybieramy razem na starcie tej fazy.
- Zawartość: odpowiedź „czy to wzrost”, kohorty dzienne z filtrami, lejek w podziałach i w czasie, sekcja „po zakupie”, oś czasu wykrytych zdarzeń, wynik biznesu (przychód i marża), jakość danych, priorytety, czego nie wiemy.
- *(dopisane 2026-10-19 po A4)* Filtr kohort według statusu pierwszego zamówienia. Przy ekonomii kampanii wynik według sesji płatności obok wyniku według przyjętej reguły źródła. Przy CRM okno 24 godzin, a obok okno 7 dni.

- *(dopisane 2026-10-19 po części pozyskania A5)* Oś czasu zdarzeń (`analiza/wyniki/a5p_zdarzenia.csv`), lejek w podziałach z pliku `analiza/wyniki/a5p_lejek_dzienny.csv.gz`, osobne wiersze sesji zalogowanych od wejścia i zakupów samego TelemediGO. Przy lejku nagłówek nie gubi awarii w Safari na iOS ani strat w przeglądarkach wbudowanych w aplikacje (dopisek Kuby).
- *(dopisane 2026-10-19 po części retencji A5)* Kohorty z plików `analiza/wyniki/a5r_kohorty_dzienne.csv` (nowi, powroty w 30/60/90 dniach, kolejne zamówienia i marża w 30–365 dniach; puste = brak pełnego okna), opóźnienia wizyt z `a5r_punktualnosc_tygodnie.csv`, zdarzenia retencji z `a5r_zdarzenia.csv`. Spadek powrotu w 90 dniach (z 23,9% do 17,4%) pokazujemy w obu wersjach reguły źródła: przyjęta reguła 4,6 punktu nowych kampanii i 2,0 starych, sesja płatności 3,0 i 3,5 (dopisek Kuby).
- *(dopisane 2026-10-20 po ekonomii kampanii A5)* Do narzędzia (punkt B): zestawienie `analiza/wyniki/a5e_kampanie.csv` (grupy, kampanie, kanały; obie reguły; okna 90, 180 i pełny rok). **Wynik po 180 dniach zawsze obok wyniku po 90 dniach** (dopisek Kuby), z dopiskiem, że to inne kohorty (do 3.04.2026). Przy każdej kampanii obie reguły obok siebie i oznaczenie „wynik zależny od reguły atrybucji”. Przedziały 95% opisane jako warunkowe.
- *(decyzja Kuby 2026-10-19)* **Kolejność:** najpierw szkielet (układ strony, lejek, oś zdarzeń, jakość danych), kohorty po drugim zatrzymaniu sesji retencji. Warunki techniczne do czasu wyboru hostingu i własność plików: `DECYZJE.md`, wpis „szkielet narzędzia (punkt B) przed końcem A5”.

**Stop — na starcie: Kuba wybiera technologię i układ strony. Na końcu: Kuba przegląda narzędzie lokalnie, przed jakąkolwiek publikacją.**

## C. Uzupełnienie analizy
- Pogłębienie przyczyn wykrytych zdarzeń. Każdy słaby wynik oglądamy oczami marketingu i obsługi pacjenta (zasada „najpierw napraw, potem wyłączaj”): obietnica reklamy, strona wejścia, przebieg wizyty, komunikacja po zakupie.
- **Lista priorytetów, wartość w marży.** Marża = przychód z konsultacji po zwrotach + przychód z TelemediGO − koszt lekarza (także za wizyty zwrócone) − wydatki na kampanie − prowizja afiliacyjna. Przy każdej pozycji: założenia, po czym poznamy, że zadziałała, ile zajmie wdrożenie. Przy słabych wynikach dwie opcje — naprawić albo wyłączyć — każda z wartością w marży.
- Lista „czego nie da się rozstrzygnąć” — przy każdej pozycji test albo dane, których brakuje. Pozycje już wpisane: (1) sesje zalogowane od wejścia bez zakupu — oba odczytania (zepsuta ścieżka zakupu dla powracających albo inny cel wizyty / sposób pomiaru), test rozstrzygający (zalogować się, wejść ponownie zalogowanym, spróbować kupić bez ponownego logowania, sprawdzić zapisane kroki) i wartość wariantu pesymistycznego w marży; (2) koszt lekarza za wizyty testowe (51 775 zł według zasady z zadania). *(dopisane 2026-10-19 po A4)* (3) wartość remarketingu porzuconego koszyka — reguła pierwszego wejścia z definicji przypisuje mu mało pacjentów; test: grupa kontrolna bez remarketingu; (4) czy newsletter i SMS wywołują zakup, czy pacjent kupiłby i tak — widać tylko kliknięcia, nie wysyłki; test: grupa kontrolna bez wysyłki; (5) warunki umowy z rankingiem lekarzy (która wizyta daje prowizję) — liczymy naszą regułą źródła, wariant po kodzie RANKING10 obok.
- *(dopisane 2026-10-19 po części pozyskania A5, `notatki/a5_pozyskanie.md`, sekcja 5)* Kolejne pozycje listy niewiadomych i priorytetów: przyczyna awarii w Safari na iOS (lista zmian z 16–17.03.2026, logi błędów rejestracji, powtórzenie na iPhonie; wartość naprawy w marży: około 105 pierwszych zamówień na 30 dni plus ich powroty); sesje zalogowane od wejścia (dane do wariantu pesymistycznego w `a5_pozyskanie.md`, sekcja 3); sezon a wydatki (do rozdzielenia tylko testem z grupą kontrolną); przeglądarki wbudowane w aplikacje (wartość naprawy wobec ograniczenia budżetu, z powrotami tych pacjentów); strata między kliknięciem reklamy a sesją w Meta i TikToku (trzy odczytania, test w panelach reklamowych i logach serwera). Ekonomię kampanii liczy sesja prowadząca po scaleniu obu części A5.
- *(dopisane 2026-10-19 po części retencji A5, `notatki/a5_retencja.md`)* **Kandydaci na listę priorytetów**, przy każdym opcje „naprawić” i „wyłączyć” z wartością w marży: poranna przepustowość internistów (opóźnienia od listopada 2025), zwroty po wizytach L4 w nowych kampaniach (17,4% wobec 5,3%), niska zgoda marketingowa pacjentów nowych kampanii (37,8% wobec około 64%). Wartość powrotu do scenariuszy: `ZALOZENIA.md` 38.
- *(dopisane 2026-10-19 po części retencji A5)* **Kolejne pozycje listy niewiadomych:**
  - **Grafiki lekarzy i ich obciążenie spoza B2C (dopisek Kuby):** w danych nie ma grafików lekarzy ani ich pracy dla pacjentów firmowych, których Telemedi też obsługuje, a lekarze mogą być wspólni. Potrzebne: liczba lekarzy na porannej zmianie według godziny, przed i po 3.11.2025, i ich obciążenie poza B2C. Test: zwiększyć poranną obsadę internistów B2C albo ograniczyć poranne terminy z kampanii na L4 na część dni (losowo) i porównać opóźnienia oraz powroty pozostałych pacjentów.
  - **Powód zwrotów po wizycie L4 z nowych kampanii** (17,4% wobec 5,3%): w danych nie ma powodu zwrotu ani informacji, czy L4 wystawiono. Potrzebne: powód zwrotu, decyzja lekarza, treść reklamy.
  - **Czy pacjenci nowych kampanii są dodatkowi:** sprawa pozyskania (sesja prowadząca, ekonomia kampanii).
  - **Wysyłki CRM:** widać kliknięcia, nie wysyłki. Liczba wejść na 1 000 pacjentów spada z 56–108 do 24–52 miesięcznie; nie wiemy, czy z powodu mniejszej liczby wysyłek, czy mniejszej klikalności.
  - **Luty 2026:** brak spadku mimo opóźnień; różni się od marca–maja w porównaniu nominalnym (z = 2,35), wynik eksploracyjny.
  - **Mechanizm opóźnień:** w tym samym miesiącu i przy tej samej liczbie wizyt w godzinie obecność pacjentów nowych kampanii prawie nie zmienia opóźnienia (0,7 punktu). Potrzebne dane o obsadzie, kolejce i zaległościach z wcześniejszych godzin.
- *(dopisane 2026-10-20 po ekonomii kampanii A5, `notatki/a5_ekonomia.md`)* **Kandydaci na listę priorytetów z ekonomii kampanii:**
  - Do punktu C, lista priorytetów, trzy pozycje z obiema drogami i liczbami z punktu 7, każda z wynikiem po 90 i po 180 dniach (dopisek Kuby):
    - TikTok na L4 (wyłączyć albo naprawić zwroty);
    - Meta na L4 (decyzja po teście dodatkowości);
    - zwroty po wizytach L4 (obietnica reklamy).
    Do tego `gs_generic_specjalisci` jako nowy kandydat.
- *(dopisane 2026-10-20 po ekonomii kampanii A5)* **Kolejne pozycje listy niewiadomych:**
  1. **Czy pacjenci nowych kampanii są dodatkowi.** Test: wyłączenie kampanii na L4 w losowej połowie województw na 4–6 tygodni (punkt 6) i badanie przyrostu w panelach reklamowych. Od wyniku zależy, czy wyłączenie Meta na L4 kosztuje, czy daje marżę (od −27,8 do +163,3 tys. zł rocznie). Przy okazji warto policzyć L4 tygodniowo z trendem przed startem i niepewnością uwzględniającą zależność między dniami (recenzja Codeksa).
  2. **Która reguła źródła jest bliższa prawdy dla kampanii bez kodu** (Google Ads ogólne, Meta lekarz online). Znak ich wyniku zależy od reguły. To ten sam test: grupa kontrolna bez reklamy.
  3. **Powód zwrotów po wizycie L4** (już na liście z części retencji). Od niego zależy, czy naprawa zwrotów jest bliżej wariantu A (+57 tys. zł), czy B (+22 tys. zł).
  4. **Koszt porannej obsady internistów.** Bez niego nie wycenimy netto naprawy przepustowości poranka.
  5. **`gs_generic_specjalisci` traci w obu regułach** (marża 32 zł na pacjenta w 90 dniach przy koszcie pozyskania 56–78 zł). Kandydat do punktu C, z obiema drogami.
  6. **Rachunek w 90 i 180 dniach nie obejmuje marży po 180 dniach.** Dla kampanii z powracającymi pacjentami to zaniża wynik. W okresie 1 marża na pacjenta w 365 dniach wynosiła 83,6 zł wobec 66,6 zł w 90 dniach. Dla nowych kampanii na L4 różnica jest mała.
- *(dopisane 2026-10-20 po przeglądzie szkicu C, decyzja Kuby, `DECYZJE.md`)* Szkic przyjęty co do kierunku. Dopiski: (1) w odpowiedzi „czy to wzrost” marża po kwartałach rok do roku z wydatkami na kampanie obok; jeśli potwierdzi się niższa marża w VII–IX 2026 przy ponad dwa razy wyższych wydatkach, to zdanie zamyka odpowiedź; (2) nowa pozycja „naprawić pomiar” (dashboard bez duplikatów i kont testowych, przychód po zwrotach, zamknięcie kodu TEST-QA, wynagrodzenie lekarzy za wizyty testowe) zaraz po Safari na iOS; (3) poranna przepustowość internistów przed testem zalogowanych i testem Meta; (4) runda konsylium na liście priorytetów, z kandydatem „pomiar” i faktem o marży w ostatnim kwartale w briefie. Po konsylium ostateczna lista do akceptacji Kuby, potem przekazanie odpowiedzi, priorytetów i niewiadomych sesji B.
- Uzupełnienie narzędzia.

**Stop — przegląd z Kubą.**

## D. Weryfikacja
- **Najpierw: dokładny przegląd zamówień testowych** (decyzja Kuby z 2026-10-19 przy zamknięciu A2). Do tego czasu 22 konta testowe są wyłączone ze wszystkich liczb. Na końcu sprawdzamy jeszcze raz, czy wyłączenie jest słuszne i kompletne, czy test nie przykrywa prawdziwych zamówień i jak liczyć koszt lekarza za testy (51 775 zł według zasady z zadania).
- Codex (model Sol): przegląd kodu. *(zmienione 2026-10-19)* Definicje sprawdził już w A4.
- Konsylium: główny wniosek i lista priorytetów.
- Codex (model Astra): końcowa weryfikacja liczb.
- Agent Opus: lektura całości jako obcy recenzent.
- Każda weryfikacja zapisana w `notatki/`.
- Publikacja narzędzia i mail do Telemedi tylko po zgodzie Kuby na każdą akcję. Treść maila przygotowuje Claude, wysyła Kuba.
- *(decyzja Kuby 2026-10-19, hosting)* W dniu wysyłki, każdy krok za osobną zgodą Kuby: powtórzone sprawdzenie repozytorium przed upublicznieniem (brak surowych danych, bazy i wierszy pojedynczych pacjentów), przełączenie repozytorium na publiczne, włączenie GitHub Pages, sprawdzenie obu linków. Po rekrutacji repozytorium wraca do prywatnych. Szczegóły: `DECYZJE.md`, wpis o hostingu.
