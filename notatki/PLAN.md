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
| A3 | Odtworzenie dashboardu | wynik gotowy (`analiza/a3_dashboard.py`, `analiza/wyniki/a3_dashboard.txt`), czeka na przegląd z Kubą |
| A4 | Definicje (razem) | do zrobienia |
| A5 | Pierwsze kohorty, lejek, po zakupie, zdarzenia | do zrobienia |
| B | Narzędzie | do zrobienia |
| C | Uzupełnienie analizy, priorytety, niewiadome | do zrobienia |
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

**Stop — przyjmujemy definicje razem.** Zapis w `notatki/ZALOZENIA.md`.

### A5. Pierwsze kohorty dzienne, lejek, to, co dzieje się po zakupie, zdarzenia
- **Kohorty:** powrót w 30/60/90 dniach, zamówienia na pacjenta, marża na pacjenta w kolejnych miesiącach. Podziały: źródło i kampania, urządzenie i przeglądarka, pierwsza usługa, zniżka i TelemediGO.
- **Lejek:** od sesji do płatności, dzień po dniu, w tych samych podziałach. Uwzględnić wyjątki z README: pacjent zalogowany na wejściu nie ma kroku logowania; zakup samego TelemediGO ma tylko dwa ostatnie kroki.
- **Sesje zalogowane od wejścia** *(dopisane 2026-10-19 po A2, decyzja Kuby)*: w lejku osobny wiersz. Pogłębienie: na którym kroku odpadają; z jakich stron i kampanii przychodzą (np. przypomnienie o recepcie — pacjenci, którzy chcą ją przedłużyć); czy kupują potem rzadziej niż podobni pacjenci bez takich sesji; czas między wyborem terminu a krokiem logowania w zakupach powtórnych (kilkadziesiąt sekund = prawdziwe logowanie, 1–2 sekundy = raczej automatyczny zapis dla zalogowanych).
- **Po zakupie, w czasie:** czy wizyta się odbyła, czy zaczęła się na czas (faktyczny start wobec umówionego terminu), ile pacjent czekał od zapłaty do terminu, zwroty, nieodebrane wizyty, oceny. Czy pacjent ze spóźnioną, nieodbytą albo zwróconą wizytą wraca rzadziej. Kampanie komunikacji po zakupie widoczne w sesjach (`crm_reactivation`, `crm_recepta_przypomnienie`, `crm_sms_przypomnienie`, `crm_go_upsell`): od kiedy działają i czy zmieniają powroty. Newsletter i SMS oceniamy na poziomie pacjenta (powrót w ciągu kilku dni od kontaktu), nie konwersją sesji — wejścia z nich są często zalogowane, a zakup dzieje się w innej sesji.
- **Wykrywanie zdarzeń:** w każdej serii dziennej szukamy dni, od których zmienia się poziom. Każde zdarzenie: data, co się zmieniło, o ile, jaki wpływ na marżę.

**Jak obchodzimy pułapki:**
- **Start od zera.** W pierwszym roku każdy pacjent jest nowy i nie ma bazy powracających, więc roczne sumy zamówień i przychodu z definicji faworyzują drugi rok. Rozbijamy zamówienia i przychód na nowych i powracających. Porównujemy kohorty w tym samym wieku, nie sumy roczne. ~~Okres rozruchu (pierwsze tygodnie, kod startowy `START10`) oznaczamy osobno i sprawdzamy, czy wnioski trzymają się bez niego.~~ *(zmienione 2026-10-19 po A2, decyzja Kuby)* START10 działa przez całe dwa lata, a nowi pacjenci od pierwszego tygodnia są na zbliżonym poziomie — od zera rośnie tylko baza powracających. Osobnego okresu rozruchu nie wyznaczamy. Sprawdzamy, czy wnioski o retencji trzymają się bez kohort z października 2024.
- **Młode kohorty miały mniej czasu na powrót.** Każdą miarę powrotu liczymy tylko dla kohort, które miały pełne okno (powrót w 90 dni — tylko kohorty do 2 lipca 2026). Porównujemy krzywe „dzień od pierwszego zakupu”. W narzędziu niedojrzałe komórki są wyszarzone.
- **Sezon a wydatki** *(dopisane 2026-10-19)*: liczba nowych pacjentów rośnie od października 2024 do stycznia 2025, ale w tym samym czasie rosną wydatki na kampanie. Rozdzielamy wpływ sezonu i wydatków (np. pozyskanie na złotówkę wydatków, źródła bezpłatne osobno). Do tego czasu przyczyna wzrostu jest otwarta.
- **Sezonowość.** Jesień i zima = więcej infekcji, więcej L4 i e-recept. Porównujemy te same miesiące rok do roku i retencję w obrębie tej samej usługi (L4 z L4). W kohortach dziennych wygładzamy efekt dnia tygodnia (średnia z 7 dni albo porównanie z tym samym dniem tygodnia). Ograniczenie: dwa lata danych to jedna obserwacja każdego sezonu na rok — sezonowości nie oddzielimy w pełni od trendu; to trafia na listę „czego nie da się rozstrzygnąć”.
- **Zmiana struktury pacjentów.** Retencję porównujemy w obrębie tego samego źródła i tej samej usługi, bo zmiana udziału źródeł potrafi obniżyć retencję całości, choć w każdym źródle się nie zmienia.

**Stop — wstępne wnioski z Kubą.** Potem propozycja rundy konsylium na wstępnych wnioskach (brief bez naszej opinii, do 3 USD).

---

## B. Narzędzie — dopiero po wspólnej wstępnej analizie
- Strona statyczna, dane przeliczone wcześniej do plików JSON, wykresy i filtry w przeglądarce. Technologię wybieramy razem na starcie tej fazy.
- Zawartość: odpowiedź „czy to wzrost”, kohorty dzienne z filtrami, lejek w podziałach i w czasie, sekcja „po zakupie”, oś czasu wykrytych zdarzeń, wynik biznesu (przychód i marża), jakość danych, priorytety, czego nie wiemy.

**Stop — Kuba przegląda narzędzie lokalnie, przed jakąkolwiek publikacją.**

## C. Uzupełnienie analizy
- Pogłębienie przyczyn wykrytych zdarzeń. Każdy słaby wynik oglądamy oczami marketingu i obsługi pacjenta (zasada „najpierw napraw, potem wyłączaj”): obietnica reklamy, strona wejścia, przebieg wizyty, komunikacja po zakupie.
- **Lista priorytetów, wartość w marży.** Marża = przychód z konsultacji po zwrotach + przychód z TelemediGO − koszt lekarza (także za wizyty zwrócone) − wydatki na kampanie − prowizja afiliacyjna. Przy każdej pozycji: założenia, po czym poznamy, że zadziałała, ile zajmie wdrożenie. Przy słabych wynikach dwie opcje — naprawić albo wyłączyć — każda z wartością w marży.
- Lista „czego nie da się rozstrzygnąć” — przy każdej pozycji test albo dane, których brakuje. Pozycje już wpisane: (1) sesje zalogowane od wejścia bez zakupu — oba odczytania (zepsuta ścieżka zakupu dla powracających albo inny cel wizyty / sposób pomiaru), test rozstrzygający (zalogować się, wejść ponownie zalogowanym, spróbować kupić bez ponownego logowania, sprawdzić zapisane kroki) i wartość wariantu pesymistycznego w marży; (2) koszt lekarza za wizyty testowe (51 775 zł według zasady z zadania).
- Uzupełnienie narzędzia.

**Stop — przegląd z Kubą.**

## D. Weryfikacja
- **Najpierw: dokładny przegląd zamówień testowych** (decyzja Kuby z 2026-10-19 przy zamknięciu A2). Do tego czasu 22 konta testowe są wyłączone ze wszystkich liczb. Na końcu sprawdzamy jeszcze raz, czy wyłączenie jest słuszne i kompletne, czy test nie przykrywa prawdziwych zamówień i jak liczyć koszt lekarza za testy (51 775 zł według zasady z zadania).
- Codex (model Sol): przegląd kodu i definicji.
- Konsylium: główny wniosek i lista priorytetów.
- Codex (model Astra): końcowa weryfikacja liczb.
- Agent Opus: lektura całości jako obcy recenzent.
- Każda weryfikacja zapisana w `notatki/`.
- Publikacja narzędzia i mail do Telemedi tylko po zgodzie Kuby na każdą akcję. Treść maila przygotowuje Claude, wysyła Kuba.
