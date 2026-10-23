# Lekcje z pracy z AI (pamięć projektu)

Claude Code zapisuje w trakcie pracy krótkie notatki dla kolejnych sesji: co poszło źle, dlaczego i jak tego unikać. Ten plik zbiera wszystkie takie notatki z tego projektu (27), pogrupowane według tematu. Każda to ślepa uliczka, pułapka albo poprawka Kuby, z uzasadnieniem i sposobem stosowania.

Treść wpisów jest taka jak w pamięci, z pięcioma wyjątkami: pominięte pola techniczne (nazwa pliku, opis do wyszukiwania, typ, identyfikator sesji, data zmiany); etykiety „Why” i „How to apply” zamienione na „Dlaczego” i „Jak stosować”; odnośniki między wpisami zamienione na linki w tym pliku; ścieżki spoza folderu projektu zastąpione oznaczeniem; wpis o wyłączaniu łączników przycięty do ogólnej lekcji, bez nazw usług i rozszerzeń spoza projektu. Pod każdym wpisem jest rozmowa, w której powstał (`rozmowy/`). Plik tworzy skrypt `analiza/f_rozmowy.py`.

## Współpraca z Kubą

### <a id="analiza-wspolnie-z-kuba"></a>Analiza wspólnie z Kubą

W zadaniu rekrutacyjnym Telemedi Kuba nie chce, żeby Claude wykonał analizę samodzielnie od początku do końca. Claude liczy i pokazuje wyniki po każdym większym kroku; nic nie jest wnioskiem, dopóki Kuba go nie zobaczy i razem go nie przyjmiemy. Wnioski weryfikujemy konsylium. Definicje (nowy pacjent, powrót, źródło, anulacje i zwroty) ustalamy razem przed liczeniem kohort, z wariantami i ich wpływem na wynik.

Przed rozpoczęciem każdego punktu planu (`notatki/PLAN.md`) pytamy Kubę, czy idziemy dalej — żaden punkt nie startuje bez jego „tak”.

Kolejność pracy: wstępna analiza → narzędzie → uzupełnienie analizy → weryfikacja. Narzędzie dopiero po wspólnym pierwszym etapie analizy. W planach bez oznaczeń dni („wtorek”, „środa”).

Skrypty, które tylko czytają dane, Claude uruchamia bez pytania (kontrola bezpieczeństwa paczki zamknięta 2026-10-19). Pytać dalej przed instalacją pakietów, publikacją, mailem i wszystkim, co wychodzi na zewnątrz.

**Dlaczego:** Kuba rozwiązuje zadanie na stanowisko Head of B2C — ocena dotyczy jego wniosków i sposobu dochodzenia do nich, więc musi je współtworzyć, a nie dostać gotowe (powiedział to 2026-10-19 przy odrzuceniu pierwszego planu).

**Jak stosować:** po każdym kroku analizy zatrzymaj się z wynikami i pytaniami do dyskusji; nie pisz „wniosek” o czymś, czego Kuba nie widział. Zasada „najpierw napraw, potem wyłączaj” jest w CLAUDE.md projektu, punkt 9.

*Zapisane w rozmowie [„Pierwsza sesja projektu — bezpieczeństwo”](../rozmowy/2026-10-19_pierwsza-sesja-projektu-bezpieczenstwo.md).*

### <a id="definicje-podstawa-w-zadaniu"></a>Definicje oparte na treści zadania

Przy wyborze definicji w punkcie A4 (2026-10-19) Kuba zanim wybrał wariant, zapytał: „czy zadanie definiuje, kto jest nowym pacjentem?”. Przy przychodzie odpowiedział: „zgodnie z instrukcją zadania”. Chce, żeby definicja stała na tekście zadania (`CLAUDE.md` punkty 2–6, `dane/README.md`), a nie na wygodzie analizy.

**Dlaczego:** zadanie mówi „nie pytaj o definicje — przyjmij założenie i je nazwij”, a Telemedi oceni, czy definicje pasują do ich pytania. Rozróżnienie „zadanie mówi wprost” / „pośrednio wskazuje” / „to nasz standard” musi być w notatkach.

**Jak stosować:** przy każdym wariancie definicji napisz, co mówi treść zadania i słownik danych (cytat albo parafraza i miejsce). Jeśli zadanie nie definiuje wprost, powiedz to i wypisz pośrednie podstawy. Rozróżniaj zasadę z zadania od naszego standardu z `CLAUDE.md`. Podstawę zapisz w `notatki/ZALOZENIA.md` przy definicji (wzór: punkt 16). Powiązane: [Analiza wspólnie z Kubą](#analiza-wspolnie-z-kuba), [Recenzja Codeksa przed zamknięciem punktu](#recenzja-codeksa-przed-zamknieciem).

*Zapisane w rozmowie [„A4: definicje razem z Kubą”](../rozmowy/2026-10-19_a4-definicje-razem-z-kuba.md).*

### <a id="watpliwosc-kuby-najpierw-policz"></a>Wątpliwość Kuby: najpierw policz

Wątpliwość Kuby do zdania (w notatkach albo na stronie) to zlecenie obliczenia, a nie redakcji. Najpierw liczymy naszym kodem (nowy skrypt albo sekcja w istniejącym), sprawdzamy wynik w raporcie, a dopiero potem zmieniamy zdanie. Nie przesądzamy przyczyny, gdy dane dopuszczają więcej niż jedno wyjaśnienie.

**Dlaczego:** 2026-10-21, lista poprawek po konsylium (`notatki/d_poprawki.md`). Kuba miał sześć wątpliwości i w większości miał rację: opóźnienia to jeden poranny blok 5:00–12:59 (południe i noc to jego brzegi), pediatra i psychiatra to małe grupy bez istotnej zmiany, przeglądarki w aplikacjach nie płacą tak samo poza kampaniami do nowych odbiorców, Safari nie mieściło się w luce III kwartału. TikTok po 180 dniach okazał się liczony z samych wczesnych kohort, ale cały rocznik i tak wyszedł ujemny, więc pewności nie obniżyliśmy. Każdy wynik policzył osobny agent we własnym skrypcie, a sesja prowadząca sprawdziła raport przed wpisaniem zdania.

**Jak stosować:** przy każdej wątpliwości Kuby: (1) policz, (2) powiedz wprost, czy wątpliwość się potwierdziła, (3) dopiero wtedy przepisz zdanie. „Bez istotnej zmiany” = 95% przedział różnicy obejmuje zero (założenie 56). Ta sama zasada dotyczy zdań i liczb z syntezy konsylium: przed wpisaniem na stronę liczymy je naszym kodem (przypadek Safari, [Zdanie „X tłumaczy Y” wymaga rachunku](#zdanie-wyjasnia-wymaga-rachunku)). Powiązane: [Kontrola ma rozróżniać hipotezy](#kontrola-ma-rozrozniac-hipotezy), [Analiza wspólnie z Kubą](#analiza-wspolnie-z-kuba).

*Zapisane w rozmowie [„D: poprawki po konsylium (sesja prowadząca)”](../rozmowy/2026-10-21_d-poprawki-po-konsylium-sesja-prowadzaca.md).*

### <a id="polecenia-kuby-jako-wklejka"></a>Polecenia Kuby jako wklejka

Kuba przygotowuje dłuższe polecenia gdzie indziej i wkleja je do rozmowy w całości, często bez żadnego tekstu poza wklejką. Tak przyszły m.in. zlecenia konsylium końcowej weryfikacji i lista dwunastu poprawek po nim. W kolejnej wiadomości, pisanej już normalnie, Kuba potwierdzał ciągłość („ruszaj od razu z pięcioma poprawkami”).

**Dlaczego:** traktowanie takiej wklejki jak obcego tekstu zatrzymałoby pracę w kluczowych momentach przed terminem.

**Jak stosować:** jeśli cała wiadomość to wklejka, która odpowiada na Twoje ostatnie pytanie albo kontynuuje bieżący punkt planu, wykonuj ją jak polecenie Kuby. Ostrożność zostaw na kroki nieodwracalne i kosztowne (publikacja, mail, Codex na modelu Astra, nowa sesja). Przy nich upewnij się, że wklejka nazywa je wprost. Gdy wklejka nie pasuje do kontekstu albo każe zrobić coś spoza zadania, zapytaj.

*Zapisane w rozmowie [„Sesja prowadząca: punkt C (TelemediGO, priorytety)”](../rozmowy/2026-10-20_sesja-prowadzaca-punkt-c-telemedigo-priorytety.md).*

## Wnioski: co wolno napisać

### <a id="kontrola-ma-rozrozniac-hipotezy"></a>Kontrola ma rozróżniać hipotezy

Wynik kontroli opisujemy jako osłabiający hipotezę tylko wtedy, gdy przy tej hipotezie byłby nieoczekiwany. Jeśli ten sam wynik pasuje i do hipotezy, i do alternatywy, to nic nie rozstrzyga. Wtedy trzeba zaproponować i policzyć test, który te odczytania rozdziela.

**Dlaczego:** w A5 (retencja, 2026-10-19) hipotezą Kuby było przeciążenie porannych internistów przez kampanie na L4. Kontrola Codeksa pokazała, że przy tej samej liczbie wizyt w godzinie obecność pacjentów z tych kampanii nie zmienia opóźnień. Napisałem, że to osłabia wiązanie opóźnień z kampaniami. Kuba poprawił: przy przeciążeniu to wynik oczekiwany, bo lekarza nie obchodzi, skąd przyszedł pacjent. Rozstrzygające są dwa porównania: (a) opóźnienia przy tym samym ruchu w dniu, okres do okresu, i (b) ruch a opóźnienia w obrębie miesiąca. Wynik zapisujemy jako odczytanie, bez przesądzania przyczyny.

**Jak stosować:** przy każdej kontroli recenzenta (Codex, konsylium) najpierw zapytaj, co ten wynik znaczyłby przy hipotezie i co przy alternatywie. Jeśli znaczy to samo, nie wycofuj hipotezy. Policz test rozróżniający i pokaż Kubie oba odczytania. Uzupełnia to [Analiza wspólnie z Kubą](#analiza-wspolnie-z-kuba).

*Zapisane w rozmowie [„A5: retencja”](../rozmowy/2026-10-19_a5-retencja.md).*

### <a id="streszczenie-nie-wzmacnia-wnioskow"></a>Streszczenie nie wzmacnia wniosków

Przy podsumowaniu dla Kuby zostawiamy status każdego zdania taki, jaki miał w źródle: obserwacja, trop, hipoteza albo wniosek przyjęty przez Kubę. Nie dopisujemy przyczyny, której dane nie rozstrzygają.

**Dlaczego:** sesja prowadząca dwa razy wzmocniła zdanie przy streszczaniu i Kuba to poprawił (2026-10-19). Raz napisała, że wzrost nowych pacjentów od października do stycznia „pasuje do sezonu infekcji”, choć w tej samej tabeli rosły wydatki na kampanie. Drugi raz, streszczając raport sesji A4, napisała, że „sama zmiana struktury źródeł nie tłumaczy spadku powrotu w Mecie”, a to była hipoteza: w drugim roku w Mecie doszła nowa kampania na L4. Obie poprawki trafiły do `DECYZJE.md` jako korekty.

**Jak stosować:** przed wysłaniem podsumowania sprawdź każde zdanie z przyczyną: czy w tych samych danych jest drugie wyjaśnienie (inna zmiana w tym samym czasie, nowa kampania, zmiana struktury)? Jeśli tak, napisz „przyczyna otwarta” i podaj, jak ją rozdzielimy. Przy streszczaniu raportu innej sesji przepisz jej zastrzeżenia, a nie samą puentę. Powiązane: [Kontrola ma rozróżniać hipotezy](#kontrola-ma-rozrozniac-hipotezy), [Wątpliwość Kuby: najpierw policz](#watpliwosc-kuby-najpierw-policz), [Analiza wspólnie z Kubą](#analiza-wspolnie-z-kuba).

*Zapisane w rozmowie [„Telemedi: prowadzenie planu analizy punkt po punkcie”](../rozmowy/2026-10-19_telemedi-prowadzenie-planu-analizy-punkt-po-punkcie.md).*

### <a id="zdanie-wyjasnia-wymaga-rachunku"></a>Zdanie „X tłumaczy Y” wymaga rachunku

Trzy razy z rzędu przeszło zdanie łączące dwie liczby bez rachunku:
1. „awaria Safari odpowiada mniej więcej spadkowi marży III kwartału”;
2. „bez awarii kwartał byłby na poziomie roku wcześniej”;
3. „Safari mieści się w pozostałej luce”.

Astra i Kuba kolejno je podważyli. Za trzecim razem Kuba sam odjął liczby z syntezy (16,2 − 11,2 = około 5 tys. zł luki) i pokazał, że szacunek Safari (14–21 tys. zł) w niej się nie mieści.

**Dlaczego:** takie zdania brzmią jak wniosek i trafiają na stronę dla Telemedi, a rachunek, który by je obalił, jest często jednym odejmowaniem. Do tego mieszały marżę rocznika pacjentów z marżą zaksięgowaną w kwartale.

**Jak stosować:**
- Zanim napiszesz, że jedna kwota tłumaczy drugą albo mieści się w niej, policz to w kodzie (ta sama miara, ten sam okres, te same składniki).
- Wynik rachunku wpisz do raportu.
- Jeśli kwoty mają różne podstawy, nie zestawiaj ich wprost. Podaj każdą osobno z jej podstawą.
- Dotyczy też zdań przepisywanych z syntezy konsylium i z odpowiedzi agentów.

*Zapisane w rozmowie [„Sesja prowadząca: punkt C (TelemediGO, priorytety)”](../rozmowy/2026-10-20_sesja-prowadzaca-punkt-c-telemedigo-priorytety.md).*

### <a id="struktura-nie-chowa-naprawy"></a>Struktura nie chowa naprawy

Przy opisie wyników (lejek, kohorty, priorytety, teksty narzędzia) rozkład „efekt struktury a efekt w obrębie grup” nie może schować problemów do naprawy. Jeśli segment traci na każdym kroku (np. przeglądarki wbudowane w Instagram, Facebook i TikTok), to jest problem strony do naprawienia, a nie tylko „inny ruch”. Znana awaria (np. zakładanie konta w Safari na iOS od 17.03.2026) musi być w nagłówku, nawet gdy rachunkowo spadek całości tłumaczy struktura.

**Dlaczego:** Kuba, 2026-10-19, przegląd części „pozyskanie” A5: odrzucił nagłówek „konwersja spadła, bo zmienił się ruch, a nie dlatego, że lejek działa gorzej”, bo gubił obie rzeczy. To przedłużenie zasady „najpierw napraw, potem wyłączaj” (CLAUDE.md projektu, punkt 9).

**Jak stosować:** w „W skrócie” najpierw miejsca do naprawy z kosztem, potem rachunek struktury jako wyjaśnienie liczby. Nie przesądzaj jednak, ile różnicy jest winą strony — to rozstrzyga test. Powiązane: [Analiza wspólnie z Kubą](#analiza-wspolnie-z-kuba), [Liczby na stronie narzędzia tylko z danych](#narzedzie-liczby-z-danych).

*Zapisane w rozmowie [„A5: pozyskanie”](../rozmowy/2026-10-19_a5-pozyskanie.md).*

## Pułapki w kodzie analizy

### <a id="odsetki-puste-wypadaja-z-mianownika"></a>Puste wartości wypadają z mianownika

Pułapka przy odsetkach typu „ile sesji kończy się zamówieniem w N dni”. Czas do następnego zdarzenia liczony przez `min(...)` po złączeniu `LEFT JOIN` jest pusty (NULL), gdy zdarzenia nie było. Wtedy `avg((czas <= X)::INT)` po cichu pomija takie wiersze. Odsetek wychodzi tylko wśród tych, którym zdarzenie kiedykolwiek zaszło. W A5 (część pozyskania, 2026-10-19) dało to 14,3% zamiast 2,6% zamówień w 7 dni po wejściu z CRM. Błąd złapał dopiero Codex, liczący własnym kodem.

**Dlaczego:** błąd nie daje żadnego komunikatu, a wynik wygląda wiarygodnie. Zawyżenie było pięciokrotne i zmieniało wniosek: po poprawce zakupy po wizycie są na poziomie tła.

**Jak stosować:** przy odsetkach z czasu do zdarzenia pisz `coalesce(czas, 1e12) <= X` albo licz `count(*) FILTER (...) / count(*)` na pełnej liczbie wierszy. Przy każdym nowym odsetku sprawdź, czy mianownik to wszystkie wiersze grupy. To samo dzieje się w pandas: kolumna liczb całkowitych z pustymi wartościami (np. `dni_R2` z DuckDB przez `.df()`) ma typ Int64 z `pd.NA`, a `(x <= 90).mean()` pomija puste. W wątku ekonomii kampanii dało to 88,6% zamiast 4,1%, a w retencji A5 84% powrotu zamiast 24%. Przed porównaniem zrób `fillna(10**6)` albo zamień kolumnę na float (`astype(float)`). Powiązane: [Recenzja Codeksa przed zamknięciem punktu](#recenzja-codeksa-przed-zamknieciem).

*Zapisane w rozmowie [„A5: pozyskanie”](../rozmowy/2026-10-19_a5-pozyskanie.md).*

### <a id="date-diff-liczy-granice"></a>date_diff liczy granice, nie czas

`date_diff('minute', a, b)` w DuckDB liczy, ile granic pełnych minut leży między dwoma znacznikami czasu. Nie mierzy, ile czasu upłynęło. Dlatego 15 minut i 59 sekund daje 15, a próg „ponad 15 minut” nie łapie takiej wizyty. Dokładny upływ czasu daje `epoch(b - a) / 60.0` (minuty z ułamkiem). To samo dotyczy `date_diff('hour', ...)` i `date_diff('day', ...)` na znacznikach czasu. Dni kalendarzowe między datami (`::DATE`) to co innego i tam `date_diff('day', ...)` jest poprawne.

**Dlaczego:** w A5 (retencja, 2026-10-19) opóźnienie wizyty liczyłem przez `date_diff('minute')`. Codex wykrył to w recenzji. Po poprawce odsetek porannych wizyt spóźnionych ponad 15 minut wzrósł z 5,5% do 6,4% (okres 1) i z 36,1% do 37,7% (okres 2). Kandydat zmiany w serii przesunął się z 17.11 na 24.11.2025, więc zbieżność z datą skoku kampanii okazała się nieodporna.

**Jak stosować:** przy każdym progu w minutach albo godzinach (opóźnienie, czas trwania, okno „24 godziny”) licz różnicę przez `epoch()`. Granice koszyków opisuj jako „do 5”, „ponad 5 do 15”, a nie „6–15”. Pułapka pokrewna do [Puste wartości wypadają z mianownika](#odsetki-puste-wypadaja-z-mianownika).

*Zapisane w rozmowie [„A5: retencja”](../rozmowy/2026-10-19_a5-retencja.md).*

### <a id="kolejnosc-przed-rankingiem"></a>Kolejność przed rankingiem

W `analiza/a5r_punktualnosc.py` tercyle dni według porannego ruchu liczono przez `pd.qcut(x.rank(method="first"), 3)` na wyniku zapytania DuckDB bez `ORDER BY`. Przy równym ruchu o przydziale dnia do tercyla decyduje kolejność wierszy, a ta w DuckDB nie jest stała. Eksport strony, liczący to samo, dostał wyniki inne o 0,2–0,4 punktu procentowego (5,4 / 6,1 / 6,1 wobec 5,8 / 5,9 / 6,1).

**Dlaczego:** kontrola zgodności z notatkami pokazała różnicę, której nie dało się usunąć bez zmiany cudzego skryptu. Wynik niepowtarzalny z kodu łamie zasadę, że każda liczba ma wychodzić tak samo z repozytorium.

**Jak stosować:** przed rankingiem z rozstrzyganiem remisów sortuj wiersze jawnie (np. `sort_values("dzien")`) albo dodawaj `ORDER BY` w zapytaniu. Przy porównaniu z liczbami policzonymi wcześniej bez takiego sortowania używaj tolerancji i zapisz w notatce, skąd różnica.

*Zapisane w rozmowie [„B: szkielet narzędzia (układ, lejek, zdarzenia)”](../rozmowy/2026-10-19_b-szkielet-narzedzia-uklad-lejek-zdarzenia.md).*

## Teksty strony i kontrola liczb

### <a id="narzedzie-liczby-z-danych"></a>Liczby na stronie narzędzia tylko z danych

Na stronie narzędzia (punkt B, `narzedzie/`) żadna liczba nie jest wpisana ręcznie w tekst. Nagłówki i opisy biorą liczby z plików danych tworzonych przez `analiza/b_eksport.py`. Przy każdym odsetku stoi liczba pacjentów albo sesji i okres. Oś zdarzeń ma obszary: lejek, retencja, obsługa pacjenta, jakość danych.

**Dlaczego:** Kuba, 2026-10-19, pierwsze zatrzymanie punktu B — po dojściu wyników retencji teksty nie mogą się rozjechać z danymi; odsetek bez liczebności i okresu jest bezużyteczny.

**Jak stosować:** teksty strony to szablony z polami wypełnianymi z danych; nowe liczby dodajesz najpierw w eksporcie. Liczby w zdaniach sprawdza kontrola pokrycia wobec notatki wzorcowej (`notatki/c_szkic.md`, a od 2026-10-21 także `notatki/d_teksty_strony.md`). Liczebności dopisane poza notatką raport kontroli oznacza jako „dodane”. Powiązane: [Analiza wspólnie z Kubą](#analiza-wspolnie-z-kuba).

*Zapisane w rozmowie [„B: szkielet narzędzia (układ, lejek, zdarzenia)”](../rozmowy/2026-10-19_b-szkielet-narzedzia-uklad-lejek-zdarzenia.md).*

### <a id="wzorzec-kontroli-nie-z-kodu"></a>Wzorzec kontroli nie z kodu

Kontrola „każda liczba na stronie stoi w szkicu” (zasada Kuby) ma sens tylko wtedy, gdy szkic i kod to dwa niezależne zapisy. W rundzie E (2026-10-21/22) agent piszący karty pięciu zakładek zrobił notatkę `notatki/e_teksty_zakladki.md` generowaną z plików strony — kontrola przechodziła z definicji. Sesja prowadząca przeczytała teksty, zamroziła notatkę (generator tylko z flagą `--nadpisz`) i od tej pory zmiany wprowadza ręcznie w obu miejscach; kontrola od razu znów łapała każdą zmienioną liczbę.

**Dlaczego:** Kuba wymaga, żeby kontrola zgodności liczb „została taka sama”; pusty wzorzec to fałszywe „0 różnic”.

**Jak stosować:** w zleceniu dla agenta albo sesji, która pisze teksty strony, wpisz wprost: szkic z liczbami pisany ręcznie przed kodem albo obok niego, bez skryptu odtwarzającego go ze strony. Przy przeglądzie cudzej pracy sprawdź, czy notatka-wzorzec nie ma generatora. Powiązane: [Liczby na stronie narzędzia tylko z danych](#narzedzie-liczby-z-danych), [Recenzja Codeksa przed zamknięciem punktu](#recenzja-codeksa-przed-zamknieciem).

*Zapisane w rozmowie [„Merytoryka narzędzia przed publikacją”](../rozmowy/2026-10-21_merytoryka-narzedzia-przed-publikacja.md).*

### <a id="strona-bez-wewnetrznych-pojec"></a>Strona bez wewnętrznych pojęć

Tekst na stronie narzędzia czyta ktoś z Telemedi bez naszych notatek i bez historii poprawek. Zdanie, które odwołuje się do pojęcia zdefiniowanego tylko w notatkach albo w innej zakładce, jest dla niego niezrozumiałe. Akapit zaczyna się od tego, co czytelnik ma wiedzieć (kwota, fakt, okres), a nie od sporu z wcześniejszym brzmieniem.

**Dlaczego:** 2026-10-21, przegląd pakietu poprawek po konsylium. Kuba kazał usunąć z „Czy to wzrost” zdanie, że Safari „nie mieści się w luce”: „Ktoś z Telemedi nie będzie wiedział, o jaką lukę chodzi”. Potem to samo w „Wyniku biznesu”: zamiast zaczynać od luki, napisać po prostu, ile szacunkowo kosztowała awaria w III kwartale i że wyniku kwartału bez awarii nie mierzymy. Zdanie o luce powstało z dyskusji wewnętrznej (synteza konsylium, uwaga Kuby), a nie z potrzeby czytelnika.

**Jak stosować:** przy każdym zdaniu przenoszonym z notatek na stronę zapytaj, czy czytelnik bez notatek wie, do czego się ono odnosi. Poprawki po recenzjach wpisuj jako nowe, samodzielne brzmienie, bez „wcześniej pisaliśmy…”. Powiązane: [Liczby na stronie narzędzia tylko z danych](#narzedzie-liczby-z-danych), [Struktura nie chowa naprawy](#struktura-nie-chowa-naprawy).

*Zapisane w rozmowie [„D: poprawki po konsylium (sesja prowadząca)”](../rozmowy/2026-10-21_d-poprawki-po-konsylium-sesja-prowadzaca.md).*

### <a id="odmiana-liczebnikow-w-tekstach"></a>Odmiana liczebników w tekstach

Gdy strona albo raport składa zdania z liczb w kodzie (np. `analiza/b_eksport.py`), rzeczownik trzeba odmienić po liczbie: 1 → „sesja”, 2–4 (ale nie 12–14) → „sesje”, reszta → „sesji”; ułamki zawsze jak 5+ („183,7 sesji”). Rzeczowniki męskoosobowe („pacjent”) mają przy 2–4 i 5+ tę samą formę „pacjentów”. Czasownik też musi się zgadzać, więc łatwiej budować zdania bez zgody liczby z czasownikiem („zapisano 604 zamówienia”, „Kod TEST-QA ma 1 781 zamówień”). Przy wartości w punktach procentowych z miejscem po przecinku zawsze „punktu procentowego”.

**Dlaczego:** pierwsza wersja zdań na stronie miała błędy typu „604 zamówień”, „22 kont złożyło”, „1 763 sesji”, „−3,00 punkty procentowe”. Stronę czyta Telemedi, a takie błędy psują wrażenie staranności.

**Jak stosować:** w kodzie składającym zdania używaj funkcji `ile(n, rzeczownik)` z `analiza/b_eksport.py` (formy 1 / 2–4 / 5+) i funkcji `pp()` dla punktów procentowych. Po każdym eksporcie przeczytaj wygenerowane zdania, zanim pokażesz stronę. Powiązane: [Liczby na stronie narzędzia tylko z danych](#narzedzie-liczby-z-danych), [Strona bez wewnętrznych pojęć](#strona-bez-wewnetrznych-pojec).

*Zapisane w rozmowie [„B: szkielet narzędzia (układ, lejek, zdarzenia)”](../rozmowy/2026-10-19_b-szkielet-narzedzia-uklad-lejek-zdarzenia.md).*

### <a id="zamiana-slowa-kolizja-znaczen"></a>Zamiana słowa zderza znaczenia

W rundzie E zamiany w `REGULY` w `analiza/e_teksty.py` i kilka zdań w `analiza/e_teksty_zakladki.py` nazwały obie reguły przypisania źródła „podziałami” („oba podziały”, „ten podział przypisuje”). Na stronie „podział” znaczył już rozkład spadku („Podział spadku liczymy opisowo”) i wymiar filtra („Podział: Przeglądarka”). W tych samych „Szczegółach” jedno słowo miało więc dwa albo trzy znaczenia. Kontrola języka 2026-10-23 znalazła około 14 takich miejsc (`notatki/f_jezyk.md`, P9) i zaproponowała jedną nazwę zbiorczą „reguły przypisania”; decyzja należy do Kuby.

**Dlaczego:** kontrola liczb w eksporcie porównuje tylko liczby, więc kolizji słów nie wyłapie, a czytelnik z Telemedi gubi się w szczegółach.

**Jak stosować:** przed hurtową zamianą słowa w kodzie tekstów albo w README przeszukaj `analiza/wyniki/b_teksty_strony.md` po słowie docelowym we wszystkich formach i sprawdź, czy nie ma już na stronie innego znaczenia. To samo przy nazwach filtrów i etykietach wykresów. Powiązane: [Strona bez wewnętrznych pojęć](#strona-bez-wewnetrznych-pojec), [Odmiana liczebników w tekstach](#odmiana-liczebnikow-w-tekstach), [Testy strony Playwrightem z Edge](#zrzuty-strony-playwright-edge).

*Zapisane w rozmowie [„F3: język tekstów zmienionych od rana”](../rozmowy/2026-10-22_f3-jezyk-tekstow-zmienionych-od-rana.md).*

## Drugi model i konsylium

### <a id="recenzja-codeksa-przed-zamknieciem"></a>Recenzja Codeksa przed zamknięciem punktu

W punkcie A4 (2026-10-19) Kuba przeniósł recenzję definicji przez Codeksa z końcowego punktu D na moment przed commitem zamykającym A4. Powód: „błąd znaleziony w środę oznaczałby przeliczanie wszystkiego od nowa”. Wynik recenzji chciał zobaczyć krótko: co przyjmuję, co odrzucam i dlaczego. Zmiany w definicjach proponowane przez recenzję przyjmuje sam, a poprawki czysto techniczne w kodzie mogą wejść od razu.

**Dlaczego:** termin wysyłki to 21.10.2026. Błąd w fundamencie (definicje, warstwa danych) odkryty na końcu kosztuje przeliczenie wszystkich kolejnych punktów.

**Jak stosować:**
- Gdy punkt jest podstawą dla dalszych punktów, zaproponuj recenzję Codeksa przed jego commitem. Wywołanie: `codex exec -p review -s read-only --skip-git-repo-check -o <odpowiedź> - < <polecenie>`, w tle.
- Codeksowi daj opis zadania, definicje, raport, kod i przykłady pacjentów z surowymi wierszami do ręcznej kontroli.
- Polecenie, odpowiedź i tabelę decyzji (przyjęte, odrzucone, dlaczego) zapisz w `notatki/recenzje/`. Wzór: `a4_codex.md`.
- Liczb policzonych przez Codeksa nie wpisuj do notatek, dopóki nie policzy ich nasz kod.
- Astry, konsylium ani Fable nie używaj bez zgody Kuby.
- Daj Codeksowi do sprawdzenia także brzmienie zdań, nie tylko liczby. W recenzji D2 (2026-10-21) przeliczył 34 z 35 liczb zgodnie, ale złapał błąd jednostki (próg Mety z 332 dni działania kampanii opisany jako roczny) i 11 zdań mocniejszych niż dane, np. „89 tygodni” z niepewnej ekstrapolacji czy „to cecha ruchu, a nie przeglądarki”.

Powiązane: [Definicje oparte na treści zadania](#definicje-podstawa-w-zadaniu), [Analiza wspólnie z Kubą](#analiza-wspolnie-z-kuba).

*Zapisane w rozmowie [„A4: definicje razem z Kubą”](../rozmowy/2026-10-19_a4-definicje-razem-z-kuba.md).*

### <a id="konsylium-duzy-brief-puste-odpowiedzi"></a>Konsylium: duży brief, puste odpowiedzi

Runda konsylium końcowej weryfikacji (2026-10-20) dostała brief z załącznikami: około 310 KB, czyli 100–125 tys. tokenów wejścia na model.
- **Puste odpowiedzi:** Gemini 4 Argon i GLM zużyły całe 24 tys. tokenów odpowiedzi na rozumowanie. Zastępstwo (DeepSeek Flash) też odpadło.
- **Pełne odpowiedzi:** Astra, Sol, Grok, Kimi, Muse i Qwen. Odpowiedź Qwena urwała się na samym końcu, choć skrypt jej nie oznaczył jako uciętej.
- **Koszt:** 2,17 USD przy limicie 3 USD (Muse 0,58, Argon 0,47 za pustą odpowiedź, Qwen 0,34).

**Dlaczego:** przy dużym briefie część zespołu cicho odpada, a ponowna próba może przebić limit kosztu, o który Kuba każe pytać wcześniej.

**Jak stosować:**
- Przy briefie powyżej około 50 tys. tokenów uruchom skrypt z wyższym `--max-tokens` (np. 48 tys.) albo zmniejsz załączniki.
- Przed wysłaniem oszacuj koszt: wejście razy cena wejścia każdego modelu plus około 1 USD na odpowiedzi.
- Brief z załącznikami składaj skryptem z plików repozytorium (wzór: `notatki/konsylium/d_weryfikacja/zbuduj_brief.py`), z zamianą imienia Kuby na „kandydat”.
- Długie odpowiedzi streszczaj agentem Sonnet do pliku i syntezę pisz z wyciągu, żeby nie zapchać kontekstu sesji.

*Zapisane w rozmowie [„Sesja prowadząca: punkt C (TelemediGO, priorytety)”](../rozmowy/2026-10-20_sesja-prowadzaca-punkt-c-telemedigo-priorytety.md).*

## Praca w kilku sesjach naraz

### <a id="sesje-w-glownym-folderze"></a>Sesje w głównym folderze, bez worktree

Wszystkie sesje tego projektu pracują w głównym folderze `C:\Users\K\Desktop\Zadanie - TM`, na gałęzi master, bez worktree. Powód: `dane/`, `pobrane/` i baza `analiza/telemedi.duckdb` są poza repozytorium (`.gitignore`), więc w worktree by ich nie było. Przy uruchamianiu nowej sesji: `use_worktree: false`.

Skutek: nie ma gałęzi do scalania. Gdy Kuba mówi „kiedy scalisz część X”, chodzi o przeniesienie wyników sesji X do wspólnych notatek (PLAN, ZALOZENIA, ZNALEZISKA, DECYZJE, PRZEKAZANIE) i commit.

**Dlaczego:** 2026-10-19 Kuba napisał „kiedy scalisz część pozyskania”. Commity sesji pozyskania były już na master, a w folderze leżały niezacommitowane zmiany innej sesji. Łatwo było pomylić to z git merge albo zacommitować cudze pliki.

**Jak stosować:** przed „scaleniem” sprawdź `git status`. Cudze niezacommitowane zmiany zostaw sesji, która je robi, i commituj tylko własne pliki. W briefie nowej sesji przydziel jej pliki, żeby dwie sesje nie pisały w tych samych (CLAUDE.md, punkt 14).

*Zapisane w rozmowie [„Pierwsza sesja projektu — bezpieczeństwo”](../rozmowy/2026-10-19_pierwsza-sesja-projektu-bezpieczenstwo.md).*

### <a id="numery-wpisow-przy-rownoleglych-sesjach"></a>Numery wpisów przy równoległych sesjach

Przy pracy równoległej każda sesja zapisuje propozycje wpisów do wspólnych notatek we własnej notatce, a scala je sesja prowadząca. Numery założeń w `notatki/ZALOZENIA.md` są ciągłe, więc zakresy trzeba rozdzielić już w zleceniu.

**Dlaczego:** w A5 (2026-10-19) sesja retencji dostała polecenie „nowe założenia od numeru 28”, a sesja pozyskania „bez numerów”. Pozyskanie scalono pierwsze i zajęło numery 28–32. Retencja miała już propozycje od 28, więc trzeba było ją prosić o przenumerowanie od 33 w trakcie pracy, a jej notatki odwoływały się do starych numerów.

**Jak stosować:** w zleceniu każdej równoległej sesji podaj jej własny zakres (np. retencja 33–49, pozyskanie 50–59) albo napisz „bez numerów, nada je sesja prowadząca przy scalaniu”. Ta sama zasada dotyczy każdej numerowanej listy we wspólnych plikach. Powiązane: [Zlecenie zmienia się w trakcie pracy](#zlecenie-zmienia-sie-w-trakcie).

*Zapisane w rozmowie [„Telemedi: prowadzenie planu analizy punkt po punkcie”](../rozmowy/2026-10-19_telemedi-prowadzenie-planu-analizy-punkt-po-punkcie.md).*

### <a id="scalanie-propozycji-skryptem"></a>Scalanie propozycji skryptem

Sesja prowadząca scala do wspólnych notatek propozycje innych sesji (sekcja „Propozycje wpisów” w ich notatce). Sprawdził się jednorazowy skrypt w scratchpadzie. Czyta notatkę sesji, wycina bloki między nagłówkami (np. od „### Do `ZALOZENIA.md`” do następnego „### ”), sprawdza warunkami `assert`, że blok zaczyna się od oczekiwanego numeru i ma oczekiwaną liczbę pozycji, a potem dopisuje go do wspólnych plików, zachowując końce wierszy CRLF.

**Dlaczego:** w A5 (2026-10-19/20) tak scalono części retencji i ekonomii kampanii. Teksty Kuby i liczby przeszły bez literówek i bez przepisywania długich akapitów, co oszczędziło kontekst sesji prowadzącej. Przy ręcznym scalaniu części pozyskania jedno polecenie powłoki padło na apostrofie i trzeba było je powtórzyć.

**Jak stosować:** skrypt scalający zapisz narzędziem Write i uruchom `python -I <plik>`. Zmieniaj tylko wspólne pliki i commituj je z jawnymi ścieżkami. Po uruchomieniu sprawdź `git diff --stat --ignore-cr-at-eol`, czy przybyły tylko dopiski. Powiązane: [Heredoc z polskim tekstem się sypie](#heredoc-polskie-cudzyslowy), [Końce wierszy sprawdzaj Pythonem](#konce-wierszy-sprawdzaj-pythonem), [Numery wpisów przy równoległych sesjach](#numery-wpisow-przy-rownoleglych-sesjach).

*Zapisane w rozmowie [„Telemedi: prowadzenie planu analizy punkt po punkcie”](../rozmowy/2026-10-19_telemedi-prowadzenie-planu-analizy-punkt-po-punkcie.md).*

### <a id="wlasny-identyfikator-sesji"></a>Własny identyfikator sesji

Sesja prowadząca wpisała w poleceniu dla nowej sesji identyfikator starej sesji planu (tej, która ją uruchomiła) jako „sesję prowadzącą”. Pytania sesji potomnej trafiałyby wtedy do zamkniętego wątku. Wyłapał to Kuba.

**Dlaczego:** sesja nie zna swojego identyfikatora wprost. W pierwszej wiadomości widzi tylko identyfikator rodzica, więc łatwo go pomylić z własnym.

**Jak stosować:** przed napisaniem polecenia dla sesji potomnej sprawdź własny identyfikator. Uruchom `list_sessions` z `linked: true`: pole `startedBy` przy sesjach, które sama uruchomiłaś, to twój identyfikator. Wpisz go w polecenie i w `PRZEKAZANIE.md`. Jeśli polecenie już poszło ze złym, wyślij sesji potomnej krótką poprawkę.

*Zapisane w rozmowie [„Sesja prowadząca: punkt C (TelemediGO, priorytety)”](../rozmowy/2026-10-20_sesja-prowadzaca-punkt-c-telemedigo-priorytety.md).*

### <a id="zlecenie-zmienia-sie-w-trakcie"></a>Zlecenie zmienia się w trakcie pracy

W etapie 2 poprawek po konsylium (2026-10-21) sesja narzędzia wdrażała teksty z `notatki/c_szkic.md` i `notatki/d_teksty_strony.md`. W tym samym czasie sesja prowadząca przeredagowała oba pliki po recenzji Codeksa (commit `1bfa75f`). Kontrola liczb ze szkicem nagle pokazała liczby bez pokrycia, choć kod się nie zmienił. Przyczyną była nowa wersja szkicu, a nie błąd w eksporcie.

**Dlaczego:** zlecenie przychodzi wiadomością z numerem commitu, a sesja prowadząca dalej poprawia te same pliki (inne sesje, Codex, prośby Kuby). Wdrożenie starej wersji oznacza drugą rundę poprawek przed wysyłką.

**Jak stosować:** przed końcową kontrolą i przed commitem uruchom `git log --oneline -- <plik zlecenia>` i `git diff <commit ze zlecenia> HEAD -- <plik>`. Weź bieżące brzmienia. Gdy kontrola nagle pokazuje braki pokrycia, najpierw sprawdź, czy nie zmienił się plik wzorcowy. W raporcie dla sesji prowadzącej podaj, na którym commicie jej plików liczyłeś. Powiązane: [Liczby na stronie narzędzia tylko z danych](#narzedzie-liczby-z-danych).

*Zapisane w rozmowie [„Narzędzie: „czy to wzrost', priorytety i niewiadome”](../rozmowy/2026-10-20_narzedzie-czy-to-wzrost-priorytety-i-niewiadome.md).*

## Narzędzia i środowisko pracy

### <a id="heredoc-polskie-cudzyslowy"></a>Heredoc z polskim tekstem się sypie

W sesji punktu B (2026-10-19/20) kilka poleceń Bash z heredoc (`python -I - <<'EOF'`, `cat >> plik <<'EOF'`) kończyło się błędem „unexpected EOF while looking for matching `''”, gdy tekst zawierał polskie cudzysłowy „…”, apostrofy albo długie wstawki HTML. To samo polecenie zapisane do pliku działało. W sesji ekonomii kampanii (2026-10-19/20) zdarzyło się to samo z długim fragmentem kodu wklejanym heredociem. W sesji punktu A4 (2026-10-19) tak samo padł `python -I - << 'EOF'` z łatką zawierającą potrójne cudzysłowy Pythona; łatka zapisana Write do scratchpadu zadziałała od razu. Dodatkowo `"\\n"` w tekście Pythona podanym przez heredoc trafiło do pliku jako prawdziwy znak nowej linii i zepsuło składnię.

**Dlaczego:** narzędzie Bash w tym środowisku (Windows, Git Bash) źle parsuje część takich heredoc; tracisz kroki i czas na powtórki.

To samo dotyczy PowerShella: `git commit -F -` z tekstem w here-stringu `@'…'@` się sypie, bo tekst trafia do gita jako ścieżka pliku, a nie na standardowe wejście (pierwsza sesja projektu). W sesji poprawek po konsylium (2026-10-21) `python -I -` z heredociem zawierającym polskie znaki nie znajdował w pliku szukanego tekstu, a ten sam kod zapisany do pliku działał.

W rundzie E (2026-10-21/22) heredoc zgubił też odwróconą kreskę: `"\\b"` i `"\\("` w łatce Pythona dotarły jako pojedyncze `\`, więc wzorce do zamiany nie pasowały. Łatka zapisana Write i uruchomiona z pliku zadziałała od razu.

**Jak stosować:** dłuższe skrypty poprawek, wstawki HTML i wiadomości commitów zapisuj narzędziem Write do scratchpadu sesji i uruchamiaj (`python -I <plik>`, `git commit -F <plik>`); krótkie poprawki rób narzędziem Edit. Powiązane: [Liczby na stronie narzędzia tylko z danych](#narzedzie-liczby-z-danych).

*Zapisane w rozmowie [„B: szkielet narzędzia (układ, lejek, zdarzenia)”](../rozmowy/2026-10-19_b-szkielet-narzedzia-uklad-lejek-zdarzenia.md).*

### <a id="konce-wierszy-sprawdzaj-pythonem"></a>Końce wierszy sprawdzaj Pythonem

Pliki w `notatki/` mają końce wierszy CRLF. Nowy plik zapisany narzędziem Write ma LF. Polecenie `grep -c $'\r$'` w Git Bash zgłaszało CRLF także w plikach z samym LF, więc kontrola w powłoce dawała fałszywy wynik. Wiarygodne jest tylko liczenie bajtów w Pythonie: `open(p,'rb').read().count(b'\r\n')`. Narzędzie Edit zachowuje końce wierszy istniejącego pliku.

**Dlaczego:** 2026-10-21 trzy nowe notatki (`d_teksty_strony.md`, `recenzje/d2_codex*.md`) były w LF, mimo że kontrola grepem mówiła CRLF. Wyszło to dopiero, gdy łatka szukająca `\r\n` nie znalazła końca wiersza.

**Jak stosować:** po utworzeniu notatki narzędziem Write zamień końce wierszy na CRLF skryptem Pythona i sprawdź wynik na bajtach. Łatki, które szukają końca wiersza, normalizuj do `\n`, a przy zapisie przywracaj CRLF. Powiązane: [Heredoc z polskim tekstem się sypie](#heredoc-polskie-cudzyslowy).

*Zapisane w rozmowie [„D: poprawki po konsylium (sesja prowadząca)”](../rozmowy/2026-10-21_d-poprawki-po-konsylium-sesja-prowadzaca.md).*

### <a id="zrzuty-strony-playwright-edge"></a>Testy strony Playwrightem z Edge

Panel przeglądarki w aplikacji Claude miał w tej pracy około 373 × 270 pikseli. Jego zrzuty ekranu często kończyły się przekroczeniem czasu, a przy emulowanej szerokości pokazywały tylko wycinek strony. Działało natomiast: Python z zainstalowanym Playwrightem, `p.chromium.launch(channel="msedge", headless=True)`, zrzuty całej strony dla szerokości 1366 i 390 pikseli, odczyt błędów konsoli, sprawdzenie `document.documentElement.scrollWidth` (przewijanie w bok na telefonie) i skrypty klikające filtry i linki. Przeglądarek nie trzeba było instalować.

**Dlaczego:** bez pełnych zrzutów nie da się ocenić układu i nie widać błędów, a sam odczyt tekstu strony nie pokazuje, czy wykresy i tabele się rysują.

**Jak stosować:** skrypty testowe trzymaj w scratchpadzie sesji, nie w repozytorium. Otwieraj wyłącznie lokalny serwer strony (`python -I -m http.server 8765 --bind 127.0.0.1` z folderu `narzedzie/`) albo `[adres strony usunięty]`. Wielkie zrzuty przycinaj Pillowem do potrzebnego fragmentu, zanim je obejrzysz. Panelu w aplikacji używaj tylko do pokazania strony Kubie. Powiązane: [Heredoc z polskim tekstem się sypie](#heredoc-polskie-cudzyslowy).

**Uzupełnienie z wątku narzędzia (etap 1 poprawek po konsylium, 2026-10-21, scalone z osobnego wpisu):** panel przeglądarki w aplikacji zwracał `innerWidth` równe 0 i nie zgłaszał błędu, więc test z panelu wyglądał na udany. W Playwrighcie używaj widoków 1366×900 i 375×812 z `is_mobile=True`. Na każdej z 9 zakładek porównuj `document.documentElement.scrollWidth` z `innerWidth`. Pozycję karty po kliknięciu odnośnika czytaj z `getBoundingClientRect().top`. Zbieraj `pageerror` i błędy konsoli. Wzór skryptu tekstów strony: `analiza/b2_teksty_strony.py`.

**Uzupełnienie z kontroli technicznej (2026-10-23):** w `[ścieżka spoza projektu usunięta]` są już silniki WebKit 26.0 (silnik Safari) i Firefox 146, więc `p.webkit.launch()` i `p.firefox.launch()` działają bez instalowania. Firefox z Playwrighta bez `locale` zwraca `navigator.language = "undefined"`: biblioteka uPlot rzuca wtedy „invalid language tag” i wykresy dzienne się nie rysują. To artefakt testu, więc w kontekście Firefoksa zawsze podawaj `locale="pl-PL"`. Firefox nie obsługuje `is_mobile`. WebKit złapał błąd, którego Edge nie widzi (zakładka „Lejek” szersza niż ekran przy 375 px), więc przy kontroli telefonu sprawdzaj też WebKit. Gotowe skrypty kontroli: `analiza/f_*.py` (opis w `notatki/f_techniczna.md`). Zrzut całej strony w Edge (Chromium) ma limit 16 384 pikseli wysokości. Powyżej limitu obraz po cichu powtarza górę strony, np. „Priorytety” na telefonie mają 24 464 px. Takie strony oglądaj zrzutami okna odcinkami, a nie jednym `full_page=True`.

**Uzupełnienie z kontroli języka (2026-10-23):** teksty dowolnej wersji strony bez ruszania projektu: `git archive <commit> narzedzie analiza/b2_teksty_strony.py | tar -x -C <scratchpad>/<nazwa>`, potem z rozpakowanego katalogu `python -I analiza/b2_teksty_strony.py --wyjscie <plik>` (skrypt bierze folder strony względem własnej ścieżki). Przydaje się, gdy równoległa sesja nadpisuje `narzedzie/dane_strony/` eksportem, i do porównania dwóch wersji linia po linii (tak powstało `notatki/f_jezyk.md`). Zrzut tekstów numeruje listy zdarzeń pod wykresami od 1, bo nie czyta numeru zapisanego w elemencie listy; numery zdarzeń sprawdzaj na stronie, nie w zrzucie.

*Zapisane w rozmowie [„B: szkielet narzędzia (układ, lejek, zdarzenia)”](../rozmowy/2026-10-19_b-szkielet-narzedzia-uklad-lejek-zdarzenia.md).*

### <a id="laczniki-wylaczanie"></a>Wyłączanie łączników i jego pułapki

Łączniki claude.ai wyłącza się narzędziem `set_session_connector_enabled` (enabled=false), po sprawdzeniu `session_connectors_status` (tylko wiersze kind „connector”). Na tym projekcie 2026-10-19 wyszły trzy pułapki:
- Wyłączenie zapisuje się też jako ustawienie domyślne dla nowych sesji. W innych projektach Kuba musi włączyć łączniki z powrotem (menu „+” w polu wiadomości → Connectors).
- Cztery łączniki po wyłączeniu dalej miały status „connected”. Drugie wywołanie odpowiadało „already disabled; nothing changed”. Ich narzędzia zniknęły z sesji dopiero następnego dnia.
- Serwerów spoza claude.ai (rozszerzeń aplikacji i serwerów dopisanych w konfiguracji) z sesji wyłączyć się nie da — można ich tylko nie używać.

**Dlaczego:** CLAUDE.md wymaga odcięcia od usług na starcie każdej sesji. Bez sprawdzenia statusu po wyłączeniu sesja raportuje Kubie „wyłączone”, choć narzędzia dalej są dostępne.

**Jak stosować:** po wyłączeniu sprawdź status jeszcze raz. Jeśli coś dalej jest „connected”, napisz Kubie jednym zdaniem, żeby wyłączył to ręcznie, i nie używaj tych narzędzi. Przy pierwszym wyłączeniu uprzedź Kubę o skutku dla nowych sesji.

*Zapisane w rozmowie [„Pierwsza sesja projektu — bezpieczeństwo”](../rozmowy/2026-10-19_pierwsza-sesja-projektu-bezpieczenstwo.md). Wpis przycięty do ogólnej lekcji.*
