# E — dopracowanie grafiki narzędzia (sesja „E: grafika”, 2026-10-22)

**Zlecenie:** sesja prowadząca (`local_1bf06826`) uruchomiła tę sesję, żeby razem z Kubą dopracować narzędzie od strony graficznej: ta sesja projektuje i wprowadza zmiany wyglądu, Kuba mówi, co zmienić, i ocenia. Pliki tej sesji: `narzedzie/index.html`, `styl.css`, `app.js`, `widoki.js`, `widoki_c.js`, `karty.js`, nowe pliki w `narzedzie/` poza `dane_strony/`, `analiza/e_przegladarka.py`, `analiza/b2_teksty_strony.py`, ta notatka i katalog `notatki/e_grafika_rundy/`. Teksty, liczby i dane strony zostają w rękach sesji prowadzącej.

Do commita `351f556` (trzecia lista Kuby w sesji `local_61aff6c2`) ta sesja nie zmieniała plików projektu — tylko czytała kod i oglądała stronę.

## 1. Przegląd obecnej strony (etap 0)

`python -I analiza/e_przegladarka.py --wyjscie <katalog tymczasowy>` na stanie sprzed `351f556`: 9 zakładek przy 1366 i 375 px, 0 błędów w konsoli, brak przewijania w bok, 296 odnośników działa. Zrzuty pocięte na ekrany i obejrzane. Pięć rzeczy, które najbardziej odstawały (wysłane Kubie):

1. Lejek: filtry i wykres kroków są około ekranu niżej, pod kartą nagłówka i dwiema kartami napraw.
2. Oś zdarzeń: same numery na jednakowych kropkach, numery nachodzą na siebie („3 5”, „9 10”); to samo na liniach zdarzeń na wykresach dziennych.
3. Wykresy liniowe z domyślną legendą biblioteki („Dzień: — □ Przychód: —”, „Dzień:” także przy grupowaniu miesięcznym).
4. Szerokie tabele: tabela kwartałów w „Wyniku biznesu” i tabela kohort obcięte już przy 1366 px; wąskie tabele rozciągnięte na całą szerokość.
5. Płaska hierarchia kart: wszystkie odnośniki podkreślone, nierówne wysokości kart obok siebie, ścieżki plików widoczne w kartach zdarzeń.

## 2. Narada modeli: jak przedstawić graficznie cały projekt (polecenie Kuby)

**Słowa Kuby:** „zaangażuj fable sol i astrę, usatlcie wspólną wersję jak przedstawić graficznie cały projekt/deliverables aby były 1. zgodne ze sztuką 2. maksymalnie czytelne 3. dodajcie gdzie się da graficzną reprezentacje danych 4. przeanalizujcie w jaki sposób (wykresy, wykresy kołowe, infografiki) wspomóc odbiór danych i poprawić czytelność analizy. UI i kolorystyka, układ oddawanego produktu: wykorzytaj impeccable z innych projektów by poprawić warstwę wizualną.”

**impeccable:** zestaw zasad projektowania interfejsów (wersja 4.3.1), którego Kuba używa w pracy. Przeczytane tylko pliki samych zasad (SKILL.md, operate, craft-floor, layout, colorize, typeset, visualize, nagłówki critique). Do briefu weszły: tryb „Operate” z elementami „Read”, powściągliwy kolor, jedna rodzina pisma i stała skala ról, test zmrużonych oczu, lista odrzucanych wzorców (karty w kartach, kolorowa ramka po lewej, mini-wykresy dla ozdoby, znaki Unicode zamiast ikon), heurystyki Nielsena i obciążenie poznawcze. Automatyczny detektor impeccable (`impeccable detect`) uruchomiony na **kopii** kodu strony w katalogu tymczasowym, żeby nic nie zapisał w projekcie: 0 uchybień.

**Przebieg:**
- Brief (`e_grafika_rundy/brief.md`): zlecenie Kuby, kto ogląda produkt, stan obecny, twarde ograniczenia (strona statyczna, nic z sieci, liczby tylko z eksportu, kolory stanu z ikoną i słowem, telefon), zasady impeccable i dataviz, struktura odpowiedzi A–G, w załączniku kształt danych strony (klucze i typy, bez wartości). Do tego 24 zrzuty ekranu (komputer i telefon).
- Runda 1, niezależnie i równolegle: Fable (agent Claude, `model: fable`), Sol (`codex exec -p review`, gpt-6.1-sol), Astra (`codex exec -p astra`, gpt-6-astra), plus własna propozycja tej sesji napisana przed przeczytaniem pozostałych. Pliki `r1_propozycja_*.md`.
- Synteza `wspolna_v1.md` z czterema rozwidleniami.
- Runda 2: każdy z trzech recenzentów ocenił v1 (sprzeciwy z poprawką, głos w rozwidleniach, braki, kolejność etapów). Pliki `r2_ocena_*.md`.
- Wersja końcowa `wspolna_v2.md`.

**Twierdzenia recenzentów sprawdzone w kodzie przed syntezą:**
- kolory serii zależą od kolejności zaznaczenia, a nie od grupy (`przydzielKolory` w `app.js`, `przydziel` w `widoki.js`) — potwierdzone;
- mapa kohort ma osobną skalę kwantylową dla każdej kolumny (`rysujMacierz` w `widoki.js`) — potwierdzone;
- na telefonie oś zdarzeń to pomniejszona miniatura wersji z komputera — potwierdzone na zrzucie 375 px;
- wykresy mają minimalną szerokość 320 px (`Math.max(320, …)` w czterech miejscach) — potwierdzone;
- pierwsza zakładka nie ładuje `kohorty.js` (dane podziałów i kohort wczytywane dopiero po wejściu w zakładkę) — potwierdzone w `index.html`, dlatego „Więcej pacjentów” i 180 dni na pierwszej zakładce wymagają eksportu;
- klucze danych wskazane w propozycjach istnieją (`wzrost.retencja.okna` z oknami 30/60/90, `lejek_naglowek.safari`, `wynik.ekonomia.wiersze`, `jakosc.mostek.kroki`, `zdarzenia.lista` z polami `obszar`, `rodzaj`, `krotko`).

**Wynik (szczegóły w `wspolna_v2.md`):** identyfikacja zostaje; porównania „przed → po” jako hantle; wykresy dzienne z wyróżnieniem jednej serii, własną legendą z wyborem serii i zdarzeniami tylko z obszaru wykresu; „Wynik biznesu” jako dwa wykresy (marża przed kosztem kampanii i wydatki, pod nimi marża po kosztach); ekonomia kampanii jako punkt wyniku względem zera z dwoma symbolami reguł; mapa kohort z legendą i tokenami. Zero wykresów kołowych; bez Sankeya, wodospadów rozkładów opisowych, wykresu kwot priorytetów i dwóch osi. Etapy 1–5, każdy z warunkami odbioru (w tym nowa kontrola zgodności liczb na wykresach z tekstem karty w `e_przegladarka.py`).

**Decyzje Kuby (2026-10-22), słowa Kuby:** „1. Mapa kohort: wspólna skala z jawnymi progami. Ten sam kolor ma wszędzie znaczyć to samo. 2. Zakładki na telefonie: widoczne pigułki (ciaśniej) i przycisk „Zakładki” po przewinięciu. Kto otworzy link na telefonie, ma od razu zobaczyć kohorty, lejek, priorytety i niewiadome. 3. Słowo „lepiej/gorzej”: tu inaczej, niż proponujesz. Ma być widoczne w kafelkach, na wykresach i w małych tabelach. W dużych tabelach podziałów (kohorty, lejek) wystarczy linijka objaśnienia pod tabelą i słowo w podpowiedzi, bo kilkadziesiąt słów „gorzej” w jednej tabeli to szum. Tam, gdzie w jednym wierszu mieszają się dobre i złe zmiany (np. kwartały), słowo zostaje.” Ponadto: etap 4 nie jest opcjonalny; etap 5 (eksport) robi równolegle sesja prowadząca (przekazane wiadomością); podgląd strony na bieżąco w panelu przeglądarki w aplikacji; `.claude/` w `.gitignore`; w repozytorium bez odwołań do innych projektów; po etapie 1 przegląd Kuby, potem etapy 2–4 bez zatrzymywania, z kontrolą po każdym; nic nie publikować.

**Koszt:** 6 wywołań (Codex: 2 × Sol, 2 × Astra; Fable: 2), wszystko w ramach subskrypcji, bez OpenRoutera.

## 3. Propozycje dla sesji prowadzącej (pliki poza tą sesją)

- Zmiany wymagające eksportu (etap 5 w `wspolna_v2.md`): powrót po 180 dniach i liczby „Więcej pacjentów” w danych pierwszej zakładki; liczby TelemediGO (trzy sposoby zakupu, oba lata) jako pola liczbowe; przeglądarki w aplikacjach (6 liczb); opóźnienia według godziny jako liczniki i mianowniki; podpisy grup priorytetów.
- README: na górze prawdziwy link; jeden zrzut „Czy to wzrost” w repozytorium (z opisem alternatywnym, robiony skryptem, z datą i commitem); opcjonalnie diagram Mermaid drogi pracy bez liczb.
- Proponowane klucze dla etapu 5 wysłane sesji prowadzącej wiadomością (2026-10-22): `D.P.wzrost.retencja.okna` z oknem 180, `D.P.wzrost.pacjenci.grupy`, pole `wykres` w karcie TelemediGO, liczby przeglądarek w aplikacjach w karcie „Do sprawdzenia”, liczniki godzin opóźnień, `priorytety.przeglad[].grupa`.
- Propozycja do `DECYZJE.md`: wygląd według wspólnej wersji v2 (`e_grafika_rundy/wspolna_v2.md`) z decyzjami Kuby R1–R3 jak wyżej.

## 4. Etap 1 — naprawy obecnych dowodów (2026-10-22)

**Co zmienione (pliki `narzedzie/styl.css`, `app.js`, `widoki.js`, `karty.js`, `index.html`):**
- **Paleta serii bez kolorów stanów:** `--series-6` i `--series-8` (zieleń i czerwień, mylone z „dobrze” i „źle”) zamienione na brązowy i oliwkowy; paleta sprawdzona walidatorem dataviz (`validate_palette.js`) w trybie jasnym (tło `#ffffff`) i ciemnym (tło `#182130`): pasmo jasności, minimalne nasycenie, rozróżnialność sąsiednich kolorów przy daltonizmie i bez niego — bez błędów (ostrzeżenie o kontraście trzech jasnych kolorów bazowej palety zostaje; łagodzą je legenda i tabele).
- **Dwa kodowania, nigdy pomieszane:** nowe tokeny `--seria-a` (okres wcześniejszy, szary), `--seria-b` (okres późniejszy, niebieski), `--seria-ref` (seria odniesienia, kolor tuszu). Kreska „rok wcześniej” na wykresie kroków lejka i linia okresu wcześniejszego na krzywej powrotu są szare; nazwy linii krzywej idą za wyborem porównania („Rok wcześniej”, „Ostatnie 12 miesięcy”).
- **Kolor idzie za grupą:** w lejku miejsce w palecie według rankingu wartości po liczbie wszystkich sesji w pliku podziału, w kohortach według stałej kolejności wartości wymiaru; przy kolizji następny wolny kolor, przydział niezależny od kolejności klikania. „Razem” i „Wszyscy w filtrze” w kolorze tuszu; nowe kampanie na L4 zawsze pomarańczowe, pozostałe kanały niebieskie. Domyślnie lejek pokazuje 4 wartości (było 5).
- **Tła okresów:** dwa neutralne szare poziomy zamiast niebieskiego tła okresu B (konkurowało z niebieską serią) i nazwa okresu na dole pola, na jasnym tle, żeby linie jej nie przecinały.
- **Mapa kohort (R1):** jedna skala dla całej macierzy, progi 5, 10, 15, 20, 25, 30 i 35% (osiem przedziałów), kolory z tokenów `--heat-0…7` z osobnym wariantem dla trybu ciemnego (wcześniej kolory wpisane w kodzie), legenda nad macierzą, brak pełnego okna jako kreskowane pole. Tekst „Jak czytać” poprawiony.
- **Etykieta zmiany (R3):** słowo „lepiej / gorzej / uwaga” widoczne w etykiecie (kafelki, wykres kroków lejka, tabele po zakupie, kwartały, tabele z danych); w dużych tabelach podziałów (kohorty, lejek, wykryte zmiany na osi zdarzeń) słowo jest w podpowiedzi i dla czytników ekranu, a pod tabelą stoi objaśnienie kolorów (`BK.legendaZmian`).
- **Typografia i rytm:** tytuł karty 18 px, do 64 znaków szerokości z wyrównanym łamaniem; wniosek 16 px zwykłej grubości (był półgruby i konkurował z tytułem); treść karty w drugim kolorze tekstu; akapity do 72 znaków; odstępy między kartami 16 px; sąsiednie karty bez rozciągania do równej wysokości.
- **Zastrzeżenie bez pudełka:** ikona, słowo „Zastrzeżenie” i tekst na tle karty, oddzielone cienką linią (koniec „karty w karcie”).
- **„Zobacz w danych”:** spokojne przyciski-odnośniki z obwódką i strzałką; odnośniki w tekście ciągłym zostają podkreślone.
- **Szerokość wykresów:** `cel.clientWidth || 300` zamiast minimum 320 px (na telefonie wykres wychodził poza kartę).
- **Oś zdarzeń na telefonie:** poniżej 600 px szerokości pionowa lista (numer, data, obszar, krótka nazwa jako odnośnik do karty zdarzenia) zamiast pomniejszonego rysunku.
- **Zakładki na telefonie (R2):** ciaśniejsze pigułki i krótszy nagłówek; po przewinięciu poza pasek w prawym dolnym rogu przycisk „Zakładki”, który rozwija listę 9 zakładek (bieżąca wyróżniona; zamyka się po wyborze, klawiszem Escape albo kliknięciem obok).
- **Tabela kwartałów w „Wyniku biznesu”:** komórki się zawijają, żeby sześć kolumn z etykietami zmiany mieściło się w karcie.

**Podgląd dla Kuby:** `.claude/launch.json` (poza repozytorium, `.claude/` dopisane do `.gitignore`) uruchamia `.claude/serwer_podgladu.py` na 127.0.0.1:8771 z nagłówkiem `Cache-Control: no-store`, żeby odświeżenie panelu zawsze pokazywało nowe pliki (zwykły `http.server` zostawiał w panelu stare skrypty). Port 8765 zajmował proces innej sesji — nieruszany.

**Kontrola (`analiza/e_przegladarka.py`, rozszerzony):** nowa opcja `--ciemny` (tryb ciemny, zrzuty z przedrostkiem `ciemny_`), nowe sprawdzenia: wykres szerszy niż karta, przycisk „Zakładki” na telefonie (widoczny po przewinięciu, 9 zakładek na liście).

## 5. Uwagi Kuby po etapie 1: mapa kohort (2026-10-22)

**Słowa Kuby (skrót polecenia):** wersja dzienna mapy jest nieczytelna (730 wierszy po około 40 pacjentów, liczby skaczą, do 2026 trzeba przewinąć setki wierszy); domyślnie kohorty miesięczne, przełącznik „miesięczne / tygodniowe / dzienne” jako widoczne przyciski; wszystkie 24 miesiące bez przewijania w ramce; nad mapą jedno zdanie, co z niej wynika, z liczbami od sesji prowadzącej. „Dla zakładki i wykresu dziennego [rozdzielczość dzienna] zostaje, mapa jest wyjątkiem.”

**Zrobione:** domyślna rozdzielczość mapy `mies`; przełącznik jako trzy przyciski (`.przelacznik`, `aria-pressed`); ramka bez ograniczenia wysokości przy mapie miesięcznej (24 wiersze widać od razu), przy tygodniowej i dziennej przewijana jak dotąd; miejsce na zdanie nad mapą (`#ko-macierz-wniosek`, wypełniane z `D.kohorty.macierz.wniosek`, gdy eksport je poda — prośba wysłana sesji prowadzącej); tekst „Jak czytać” poprawiony.

## 6. Etap 2 — główne nowe dowody (2026-10-22)

**Komponenty (`narzedzie/karty.js`, bez biblioteki, HTML i CSS):** `BK.hantle` (dwa punkty na wspólnej osi i odcinek; kodowanie „okresy”: szary → niebieski, albo „grupy”: pusty pierścień → fiolet), `BK.slupkiParami` (wartość wcześniejsza szara, późniejsza niebieska, wspólny początek), `BK.slupkiSkumulowane` (długość = liczba, nie 100%), `BK.punktyZero` (punkty względem zera, dwa kształty dla dwóch reguł), `BK.wstawWykres` (wykres pod wnioskiem karty; tabela, którą zastępuje, idzie do zwijanej sekcji „Tabela z liczbami”). Każdy wiersz wykresu ma podpis z liczbami (te same co w tekście), podpowiedź z liczebnościami i opis dla czytników ekranu; etykieta zmiany ma słowo (decyzja R3).

**Gdzie:**
- „Czy to wzrost”: „Więcej pacjentów” — słupki obu lat w skali liczby pacjentów (pozostałe kanały niebieskie, nowe kampanie na L4 pomarańczowe; `D.P.wzrost.pacjenci.grupy`); „Lepsza retencja” — hantle powrotu w 30/60/90/180 dniach (`D.P.wzrost.retencja.okna`), tabela do „Tabeli z liczbami”; TelemediGO — słupki parami trzech sposobów zakupu (pole `wykres` karty), tabela zwinięta.
- „Kohorty”: te same hantle powrotu w karcie nagłówka.
- „Lejek”: karta Safari — hantle „przed awarią → po awarii” dla Safari na iPhone'ach (66% → 46%, jak w tekście karty) i pozostałych przeglądarek; karta przeglądarek w aplikacjach — hantle grup (zwykłe przeglądarki w tych samych warunkach → przeglądarka w aplikacji) dla trzech kampanii z tekstu i, osobno, dla kampanii na L4; podpis drugiej wartości według uwagi sesji prowadzącej („w tych samych warunkach”, bez liczby sesji).
- „Priorytety”: w karcie pozycji 1 ten sam wykres Safari.
- „Po zakupie”: karta porannego ruchu — hantle odsetka spóźnionych ponad 15 minut według ruchu w dniu; tabela zwinięta.
- „Wynik biznesu”: zamiast jednego wykresu z czterema liniami dwa wykresy jeden pod drugim — (1) marża przed kosztem kampanii i wydatki na kampanie (jedna jednostka, jedna oś; marża przed kosztem kampanii = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza, czyli marża + wydatki + prowizja, jak w eksporcie; wydatki bez prowizji), (2) marża po koszcie lekarza, kampaniach i prowizji. Ekonomia kampanii: punkty wyniku na pacjenta względem zera, koło = według pierwszego wejścia, romb = według sesji z płatnością, przełącznik okna 90 / 180 dni, znacznik „Znak zależy od przypisania”, gdy reguły dają różny znak; tabela w zwijanej sekcji. Na poziomie kanałów dane mają tylko okno 90 dni — przy 180 dniach zamiast pustej osi stoi informacja.

**Kontrola:** `e_przegladarka.py` (znak gotowości zakładki „Wynik biznesu” to teraz wykres ekonomii, bo tabela jest zwinięta): 9 zakładek przy 1366 i 375 px w trybie jasnym i ciemnym, 0 błędów w konsoli, bez przewijania w bok, wykresy mieszczą się w kartach, 296 odnośników działa, przycisk „Zakładki” działa. Obejrzane zrzuty: „Czy to wzrost” (komputer i telefon), lejek, wynik biznesu; poprawione po obejrzeniu: podziałka osi ekonomii (równe kroki co 20 albo 40 zł z zerem), pusty wykres przy 180 dniach na poziomie kanałów.
