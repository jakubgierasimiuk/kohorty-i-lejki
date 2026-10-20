# Opus 5.5 (agent Claude Code)

## Puenta

Rozwiązanie jest poprawne w rachunkach i mocne analitycznie. Każdą liczbę, którą przeliczyłem własnym kodem na bazie (schemat `czyste`, tylko odczyt), dostałem tak samo jak narzędzie, co do dziesiątej części. Błędu krytycznego w treści nie znalazłem.

Przed wysłaniem trzeba poprawić dwa błędy wyświetlania na stronie. Pierwszy to zły podpis odnośników przy sześciu zdarzeniach. Drugi to znak procentu przy średniej ocenie. Trzeba też złagodzić kilka zdań mocniejszych niż dane i ujednolicić kilka liczb między zakładkami.

Największa słabość z perspektywy zlecającego nie leży w liczbach. Przekaz jest bardzo gęsty: na stronie jest dużo zastrzeżeń i dużo liczb w każdym zdaniu. Do tego najdroższa decyzja na liście, czyli test kampanii Meta na L4, stoi dopiero na 9. miejscu.

---

## 1. Lista poprawek od najważniejszej

### Warunek wysyłki (to nie jest błąd, ale bez tego zadanie nie jest spełnione)

**0. Link do narzędzia i widoczność repozytorium.**
- **Miejsce:** README, pierwsza linia: `https://<organizacja>.github.io/<repozytorium>/`.
- **Co jest nie tak:** w README jest jeszcze adres zastępczy. Zadanie wymaga narzędzia, które „otwiera się z linku”.
- **Propozycja:** wpisać prawdziwy adres. Repozytorium przełączyć na publiczne i włączyć Pages. Oba linki sprawdzić w oknie prywatnym przeglądarki, bez zalogowania do GitHuba. Sprawdzić też na telefonie. Lokalnie przy szerokości 375 pikseli strona nie ma przewijania w poziomie, więc powinno działać.

### Ważne

**1. Zła etykieta odnośnika przy sześciu zdarzeniach retencji i obsługi pacjenta.** Waga: ważna, bo to najważniejsza część zadania.
- **Miejsce:** zakładka „Zdarzenia”, zdarzenia 3, 5, 6, 7, 10 i 11.
- **Co jest nie tak:** pod każdym z tych zdarzeń stoi napis „Zobacz w jakości danych”. Odnośnik prowadzi jednak do „Kohort” albo do „Po zakupie”.
- **Dowód:** w `narzedzie/app.js` (linie 502–503) każdy odnośnik, który nie zaczyna się od `#lejek`, dostaje napis „Zobacz w jakości danych”. W `dane_strony/zdarzenia.js` cztery takie odnośniki prowadzą do `#kohorty?…`, a dwa do `#po-zakupie`.
- **Propozycja:** napis zależny od celu odnośnika: „Pokaż w kohortach”, „Pokaż w zakładce Po zakupie”, „Zobacz w jakości danych” (tylko dla `#jakosc`).

**2. Średnia ocena pokazana jako procent.**
- **Miejsce:** „Po zakupie”, tabela „Oceny według opóźnienia wizyty”, kolumna „Średnia ocena (1–5)”.
- **Co jest nie tak:** strona pokazuje na przykład „4,45% z 3 446” i „2,92% z 469”.
- **Dowód:** `widoki.js:641` przekazuje jednostkę jako pusty tekst `""`. Funkcja `komorka` (`widoki.js:79`) ma zapis `j = jedn || "%"`, więc pusty tekst zamienia się na „%”.
- **Propozycja:** `j = jedn === undefined ? "%" : jedn` oraz brak spacji przy pustej jednostce. Tylko to jedno wywołanie ma pustą jednostkę, sprawdziłem wszystkie.

**3. Poprawka Astry o Safari nie dotarła do dwóch zakładek.**
- **Miejsce:**
  - nagłówek karty w „Lejku”: „od 17.03.2026 nie działa zakładanie konta”;
  - zdarzenie 12, tytuł: „przestaje działać zakładanie konta”;
  - zdarzenie 12, opis: „Psuje się zakładanie nowego konta”.
- **Co jest nie tak:** w README i w pozycji 1 priorytetów brzmienie jest już poprawione („gwałtownie spada skuteczność zakładania nowego konta”). W lejku i na osi zostało stare, zbyt mocne brzmienie.
- **Dowód z bazy:** po 17.03.2026 krok konta przechodzi 45,6% osób, które wybrały termin i jeszcze nie kupowały. To 2 132 z 4 678 sesji, więc konta dalej powstają.
- **Propozycja:** „od 17.03.2026 gwałtownie spada skuteczność zakładania konta” w obu miejscach.

**4. Zdanie „Opóźnienia rosną tylko u internisty rano” przeczy tabeli pod nim.**
- **Miejsce:** „Po zakupie”, pierwsze zdanie karty o punktualności.
- **Dowód (tabela na tej samej stronie):**
  - internista w południe: 3,0% → 8,9% wizyt spóźnionych ponad 15 minut (3 748 wizyt w okresie B);
  - internista w nocy: 1,9% → 5,7%.
- **Dowód z bazy:** wizyty z terminem o 12:00 w okresie 2 są spóźnione ponad 15 minut w 22,3% przypadków, wobec 3,4% w okresie 1.
- **Propozycja:** „Opóźnienia rosną najsilniej u internisty rano. W południe i w nocy też rosną, ale z niskiego poziomu.”

**5. Przeliczenie kampanii „na pełny rok” zaniża kwoty, bo średnio liczy też okres rozruchu.**
- **Miejsce:**
  - „Zasady listy”;
  - pozycje 3, 5 i 9 priorytetów;
  - niewiadoma 1;
  - założenia 53 i 54.
- **Co jest nie tak:** mnożnik 365 / liczba dni działania zakłada średnie tempo z całego okresu działania kampanii. Obie kampanie rozkręcały się jednak przez pierwsze miesiące.
- **Dowód z bazy (wydatki miesięczne):**
  - TikTok na L4: 1,7 tys. zł w lutym, 7,1 tys. zł w marcu, potem stale 12,1–12,7 tys. zł miesięcznie. Od kwietnia do września 2026 to 73,7 tys. zł, czyli w tempie rocznym około 147 tys. zł. Strona podaje 128,6 tys. zł.
  - Meta na L4: od kwietnia do września 2026 to 103,4 tys. zł, czyli w tempie rocznym około 207 tys. zł. Strona podaje 179,6 tys. zł.
- **Wpływ:** znak żadnej decyzji się nie zmienia. Kwoty w wariancie „0% pacjentów dodatkowych” i w pozostałych wariantach są zaniżone o około 13–15%. To błąd ostrożny, więc nie podważa wniosków.
- **Propozycja:** dopisać w „Zasadach listy”, że mnożnik liczy średnią z rozruchu, a tempo z ostatnich 6 miesięcy jest o około 15% wyższe. Albo pokazać obok drugą kwotę, w tempie z ostatnich 6 miesięcy.

**6. „Wzrost marży słabnie z kwartału na kwartał” jest częściowo mechaniczny przez start od zera.**
- **Miejsce:** „Czy to wzrost”, karta „Wynik pod koniec okresu” (nagłówek i tabela); „Wynik biznesu”, kwartały rok do roku.
- **Co jest nie tak:** w IV kwartale 2024 firma prawie nie miała jeszcze pacjentów powracających. W III kwartale 2025 baza była już dojrzała. Dlatego wynik +71,4% w IV kwartale 2025 jest zawyżony przez start od zera, a malejący ciąg +71% → +43% → +13% → −7% jest w części artefaktem.
- **Dowód (tabela miesięczna na stronie, przychód z kolejnych zamówień):**
  - X–XII 2024: 68,9 tys. zł; X–XII 2025: 262,0 tys. zł, czyli 3,8 raza więcej;
  - VII–IX 2025: 241,3 tys. zł; VII–IX 2026: 273,9 tys. zł, czyli +13,5%.
- **Co zostaje bez zmian:** sam wynik III kwartału (−6,8%) jest odporny na ten efekt. Wtedy baza z okresu 2 jest większa, więc spadek jest raczej zaniżony niż zawyżony.
- **Propozycja:** jedno zdanie przy tabeli: „Wcześniejsze kwartały okresu 1 nie miały jeszcze bazy powracających, więc ich wzrost rok do roku jest zawyżony. Miarodajny jest III kwartał.” Zastrzeżenie 2 („start od zera”) mówi dziś tylko o sumach rocznych.

**7. „Rachunkowo prawie cały spadek to zmiana ruchu” zależy od tego, jak podzielimy ruch.**
- **Miejsce:** „Lejek”, drugi akapit.
- **Dowód (załącznik E3, sekcja 4):**
  - podział według przeglądarki: −3,00 pkt proc. (punktu procentowego) to struktura ruchu, +0,67 pkt proc. to konwersja;
  - podział według kampanii: −2,44 pkt proc. struktura, +0,11 pkt proc. konwersja;
  - podział według strony wejścia: −0,45 pkt proc. struktura, −1,87 pkt proc. konwersja;
  - podział na nowych i powracających: −0,44 pkt proc. struktura, −1,89 pkt proc. konwersja.
- **Co jest nie tak:** czytelnik z dostępem do repozytorium zobaczy podziały, które mówią coś odwrotnego. Strona tego nie tłumaczy.
- **Propozycja:** jedno zdanie wyjaśnienia. Nowe kampanie kierują ruch na istniejące strony wejścia, a cały ich ruch to nowe osoby. Dlatego w podziale według strony wejścia albo według typu pacjenta zmiana struktury „chowa się” w konwersji. Podział według przeglądarki i kampanii jest tu właściwy.

**8. Pozycja 6 (poranna obsada) pokazuje tylko szeroki zakres, bez wariantu bazowego.**
- **Miejsce:** „Priorytety”, przegląd i karta pozycji 6 („od 0 do 65 tys. zł”).
- **Dowód:** `c_priorytety.txt`, P8: wariant wąski to 11,9–12,7 tys. zł, a szeroki 31,8–65,2 tys. zł.
  - Wariant szeroki przypisuje opóźnieniom cały spadek powrotu w starych kampaniach.
  - Rozkład z części retencji przypisuje im tylko część: −0,76 z −1,91 pkt proc. (przyjęta reguła) i −0,64 z −3,50 pkt proc. (sesja płatności).
- **Propozycja:** „około 12 tys. zł w wariancie wąskim, do 65 tys. zł w szerokim, koszt obsady nieznany”. Przy tej kwocie i niskiej pewności miejsce 6 jest wysokie (zob. punkt 10).

**9. Pozycja 3 (TikTok): „wysoka pewność co do znaku” jest mocniejsza niż karta tej pozycji.**
- **Miejsce:** „Priorytety”, przegląd, kolumna „Pewność”.
- **Dowód:** karta sama podaje wynik po 180 dniach według przyjętej reguły: −1,1 zł na pacjenta, przedział od −5,3 do +3,0 zł (299 pacjentów). Przeliczyłem to: −1,14 zł ± 4,16 zł. W horyzoncie 180 dni znak nie jest więc pewny.
- **Propozycja:** w przeglądzie wpisać „wysoka: brak korzyści; strata niewielka”. To samo zdanie już stoi w karcie.

**10. Kolejność listy: test Meta na L4 jest za nisko.** To różnica zdań, a nie błąd.
- **Miejsce:** „Priorytety”, pozycja 9.
- **Argument:** to decyzja o największej kwocie na liście, od −30,6 do +179,6 tys. zł rocznie.
  - Według przyjętej reguły wyłączenie kampanii traci pieniądze dopiero wtedy, gdy ponad 85% jej pacjentów jest dodatkowych.
  - Według sesji płatności wyłączenie zyskuje zawsze.
  - Test kosztuje najwyżej 1,6–1,8 tys. zł utraconej marży.
- **Co dziś stoi wyżej:** pozycja 6 (niska pewność, wariant wąski około 12 tys. zł) i pozycja 8 (sama karta mówi, że dane wskazują raczej na 0 zł).
- **Propozycja:** przesunąć test Meta na 4. albo 5. miejsce. Pozycja 8 i tak jest robiona w pierwszym tygodniu, niezależnie od miejsca na liście.

**11. Pominięcie: kohorty nie mają podziałów demograficznych.** Waga: ważna jako pominięcie wymiaru. Samo znalezisko niżej jest niepewne.
- **Miejsce:** „Kohorty”, filtry. Tabela kont ma województwo, wiek, płeć, wielkość miejscowości i zgodę marketingową. Żadna z tych cech nie jest filtrem ani podziałem.
- **Dowód (szybkie sprawdzenie):**
  - Do starych kampanii zaliczyłem pacjentów bez kodu nowych kampanii i bez sesji płatności z nowych kampanii. To przybliżenie, nie przyjęta reguła.
  - Powrót w 90 dniach w województwie dolnośląskim spada z 27,6% (1 024 pacjentów) do 19,4% (1 028 pacjentów), czyli o 8,2 pkt proc.
  - W większości województw spadek wynosi 0–5 pkt proc., a w kilku powrót nawet rośnie.
  - Kwartalnie spadek jest stopniowy: 29,4% w IV kwartale 2024, potem 21,5%, a na końcu 18,5% w II kwartale 2026. Liczebności to około 250–400 pacjentów na kwartał.
- **Pewność:** przy 16 województwach to może być przypadek. Według mojego szacunku to około 3 odchylenia standardowe od średniego spadku, więc to trop, a nie wniosek.
- **Propozycja:** dodać filtr województwa i grupy wieku w „Kohortach”. Albo dopisać niewiadomą: „regionalne różnice powrotu nie zostały zbadane”.

**12. Odczytanie „spadła poranna przepustowość” można doprecyzować danymi.** Waga: między ważną a drobną.
- **Miejsce:** „Po zakupie”, karta „Opóźnienia przy tym samym porannym ruchu”; zdarzenie 7; pozycja 6.
- **Dowód z bazy (okres 2, internista):** udział wizyt spóźnionych ponad 15 minut jest prawie płaski w ciągu poranka:

  | Godzina terminu | 6:00 | 7:00 | 8:00 | 9:00 | 10:00 |
  |---|---|---|---|---|---|
  | Spóźnione ponad 15 minut | 45,4% | 44,4% | 47,0% | 45,3% | 40,4% |

  Mediana opóźnienia wynosi około 13 minut o każdej z tych godzin.
- **Co to znaczy:** opóźnienie nie narasta w ciągu poranka. Do tego narzędzie samo pokazuje, że w obrębie miesiąca opóźnienia nie zależą od ruchu. Taki obraz bardziej pasuje do stałej przyczyny niż do kolejki, która przerasta przepustowość. Przykłady stałej przyczyny: lekarze zaczynają później, najpierw obsługują inną kolejkę albo system zapisów przesuwa terminy.
- **Propozycja:** w diagnozie z pozycji 6 dopisać, że opóźnienie jest od pierwszej godziny i nie rośnie w ciągu poranka. To zawęża rozmowę z osobami od grafików.

### Drobne

**13. Zmiana powrotu w 180 dniach ma dwie wartości.**
- „Czy to wzrost”: −5,3 pkt proc.
- „Kohorty”: ▼5,2.
- Z bazy: 27,47% − 22,24% = 5,23, więc poprawna wartość to 5,2. Wartość 5,3 wynika z odejmowania zaokrągleń (tak też w `a5r_kohorty.txt` 1b).

**14. Pozycja 6: zła liczebność przy średnich ocenach.**
- Zdanie podaje średnią ocenę 2,9 wobec 4,5, a w nawiasie „1 550 i 11 007 wizyt”.
- Średnie liczono jednak z 469 i 3 446 ocen. Tyle ocen jest w tabeli w „Po zakupie”.

**15. Safari: dwie pary liczb dla tego samego zjawiska.**
- „Lejek”: 66,2% → 45,1% (okna po 60 dni, 1 763 i 1 553 sesji).
- Pozycja 1: 66,1% → 45,6% (okna od 1.10.2025 i do 30.09.2026, 4 678 sesji po awarii).
- Obie pary przeliczyłem i obie są poprawne. Czytelnik zobaczy jednak dwie wartości. Warto w obu miejscach jednym słowem nazwać okno.

**16. Zdarzenie 8: niezdefiniowany okres.** Zdanie kończy się „i 26,7% w 2026”. Reszta strony używa okresów X–IX, a „2026” nie jest okresem zdefiniowanym na stronie.

**17. Daty z przyszłości w raporcie.** `analiza/wyniki/c_priorytety.txt` ma w nagłówkach W4 i P1b datę 2026-10-21, a dziś jest 2026-10-20. Raport trafi do publicznego repozytorium.

**18. Różnica 1 zł w przychodzie okresu 1.**
- Strona: 2 230 266 zł.
- `ZALOZENIA.md`, punkt 21: 2 230 267 zł.
- Suma z bazy to 2 230 266,5 zł, więc to tylko zaokrąglenie.

**19. README: brak drugiej reguły przy udziale nowych kampanii.** Zdanie „Prawie jedna trzecia (29%)” nie mówi, że to przyjęta reguła. Według sesji płatności udział wynosi 21% (5 187 z 24 687).

**20. Adres e-mail osoby rekrutującej w publicznym repozytorium.**
- Adres jest w śledzonych plikach `CLAUDE.md` i `notatki/konsylium/d_weryfikacja/zbuduj_brief.py`.
- Po upublicznieniu repozytorium trafi do automatów zbierających adresy.
- Propozycja: usunąć go z bieżącej wersji tych plików. Historia zostaje, bo nie przepisujemy jej, i to jest decyzja Kuby.

**21. `robots.txt` pod podścieżką nic nie robi.** Roboty czytają ten plik tylko w głównym katalogu domeny. Blokadę indeksowania zapewnia znacznik `noindex` w `index.html`, który jest na miejscu. Nic nie trzeba zmieniać, ale nie warto na `robots.txt` liczyć.

**22. Płatności w lejku a zamówienia różnią się o 1.**
- Lejek: 24 717 i 38 490 płatności.
- Zamówienia: 24 716 i 38 491.
- Przyczyna: sesja liczy się do dnia rozpoczęcia, a zamówienie do dnia płatności. Na granicy okresów jedna sesja zaczęła się przed północą, a płatność przyszła po północy.
- Jedno zdanie w „Jak liczymy” uprzedzi pytanie.

---

## 2. Co się potwierdziło

Wszystko liczyłem własnym kodem (DuckDB, `read_only=True`, schemat `czyste`). Nie importowałem skryptów projektu.

| Co | Moje przeliczenie | Na stronie |
|---|---|---|
| Nowi pacjenci, okres 1 i 2 | 16 231 i 24 687 (+52,1%) | to samo |
| Powrót w 30 dniach (kohorty do 31.08) | 11,02% (14 984) i 7,84% (22 646) | 11,0% i 7,8% |
| Powrót w 60 dniach (do 1.08) | 19,09% (13 941) i 13,73% (20 823) | 19,1% i 13,7% |
| Powrót w 90 dniach (do 2.07.2025 i 2.07.2026) | 23,91% (12 867) i 17,38% (18 924); wróciło 3 076 i 3 289 osób | to samo |
| Powrót w 180 dniach (do 3.04) | 27,47% (9 125) i 22,24% (12 591) | zob. poprawka 13 |
| Marża na pacjenta w 90 i 180 dniach | 66,6 i 58,3 zł; 75,45 i 67,68 zł | to samo |
| Pacjenci nowych kampanii według przyjętej reguły (mój kod reguły) | 7 268 (Meta 5 059, TikTok 2 209) | 7 268 |
| Powrót w 90 dniach: pozostali i nowe kampanie | 21,99% (14 031) i 4,15% (4 893) | 22,0% i 4,1% |
| Marża przed kampaniami, III kwartał 2025 i 2026 | 313 530 i 392 493 zł | to samo |
| Wydatki na kampanie, III kwartał 2025 i 2026 | 87 431 i 181 555 zł (2,08 raza) | to samo |
| Marża III kwartału z prowizją projektu | 222 824 i 207 713 zł (−6,8%) | to samo |
| TelemediGO: zakupy | 1 759 i 2 468, w tym osobno 225 i 461; 156 551 i 219 652 zł | to samo |
| Safari na iOS, krok konta u osób, które jeszcze nie kupowały | 66,13% (4 254) → 45,58% (4 678); dalej do płatności 72,28% | to samo |
| Safari na iOS, utracone pierwsze zamówienia | 695 bez odjęcia tła i 628 po odjęciu tła | to samo |
| TikTok, wynik na pacjenta według przyjętej reguły | −4,61 zł ± 1,97 zł (90 dni) i −1,14 zł ± 4,16 zł (180 dni) | −4,6 i −1,1 zł |
| Meta na L4, wynik na pacjenta według przyjętej reguły | +6,45 zł (90 dni) i +8,16 zł (180 dni) | +6,5 i +8,2 zł |

Dodatkowo potwierdzone:
- **Wszystkie 8 kwartałów:** marża przed kampaniami i wydatki zgadzają się z tabelą W4.
- **III kwartał nie zależy od reguły prowizji afiliacyjnej.** Przy prowizji liczonej samym kodem RANKING10 (63 i 58 pierwszych zamówień) spadek marży wynosi −6,7% zamiast −6,8%.
- **Safari jako pozycja o najwyższej wycenie:** sprawdziłem ją drugą drogą, liczbą nowych pacjentów płacących w Safari na iOS.
  - 60 dni przed i 60 dni po 17.03.2026: 880 → 521.
  - Te same dni rok wcześniej: 702 → 584, czyli sezonowo −17%.
  - Niedobór ponad sezon to około 211 pacjentów w 60 dniach, czyli około 105 na 30 dni. To zgadza się z szacunkiem 95–105.
  - Pacjenci powracający w Safari na iOS przechodzą krok konta w 100% przed awarią i po niej, więc logowanie rzeczywiście działa.
- **Rachunki na liczbach z załączników:**
  - próg decyzji Meta 85,4% i 84,5%;
  - wycena Safari 1 158–1 281 zamówień rocznie × 64,6 zł, czyli 75–83 tys. zł; w III kwartale 14,1–20,9 tys. zł;
  - 23,6 tys. zł za punkt procentowy powrotu (24 687 × 1% × 95,6 zł);
  - 37 950 zł za wizyty testowe;
  - cennik: 73,6 i 70,8 tys. zł;
  - TelemediGO: −27 388 zł;
  - sumy miesięcy zgadzają się z kwartałami i z rokiem (1 048 069 zł);
  - udział przeglądarek wbudowanych 10,7% → 35,6%;
  - udział nowych kampanii w spadku powrotu 46–71%;
  - zwroty L4: 1 024 z 5 895 (same wizyty L4) i 1 044 (wszystkie wizyty), czyli dwie różne liczby, obie spójne.
- **Odczyt zwykłej sprzedaży TelemediGO:** odsetek kupujących przy pierwszym zamówieniu 5,58% → 4,41%, rozbicie +471 i −287. Zgadza się.
- **Strona:** w 9 zakładkach (lokalny serwer, który już działał) przeglądarka nie zgłasza błędów. Przy szerokości telefonu nie ma przewijania w poziomie.
- **Definicje są spójne i nazwane:** nowy pacjent, powrót, przychód po zwrotach, koszt lekarza (także za wizyty zwrócone, bez wizyt nieodebranych), te same dni kalendarzowe, pełne okna obserwacji.

**Czego nie sprawdziłem:**
- reguły sesji płatności;
- tabeli ekonomii wszystkich kampanii;
- wariantów A i B naprawy zwrotów;
- liczebności testów z pozycji 9 i 12;
- okna 24 godzin dla newslettera;
- listy 245 automatycznie wykrytych zmian.

---

## 3. Ocena z perspektywy zlecającego

### Trzy najmocniejsze strony

1. **Rzetelność danych.** Kandydat odtworzył dashboard dokładnie: z 864 kombinacji definicji pasuje 14, a wybrał najprostszą. Duplikaty i konta testowe złapał dwoma niezależnymi podpisami. Pokazał też mostek od +61% do +55,7%. To dokładnie realizuje zasadę z zadania: „jeśli coś wygląda podejrzanie, powiedz”.
2. **Poprawna i uczciwa odpowiedź na główne pytanie.** Oba warunki sprawdzone są osobno, na tych samych dniach kalendarzowych i według dwóch reguł źródła. Kandydat odróżnia opis od przyczyny. Zdarzenia znalazł w danych z datami: Safari 17.03.2026, starty kampanii, poranne opóźnienia od 24.11.2025, zwroty L4. Połączył je z kohortami i z pieniędzmi.
3. **Priorytety w złotych, z drogą „naprawić albo wyłączyć”.** Każda pozycja ma sposób pomiaru i czas wdrożenia. Testy są dobrze zaprojektowane: wyłączenie w parach województw z progiem decyzji ustalonym z góry, grupy kontrolne w komunikacji. Lista niewiadomych ma test przy każdej pozycji.

### Trzy najsłabsze strony

1. **Przekaz jest przeciążony.** Prawie każde zdanie ma 3–6 liczb i zastrzeżenie. Pierwsza karta „Czy to wzrost” ma siedem zastrzeżeń. Zarząd po 5 minutach zapamięta „nie, bo retencja”, ale zgubi „co robimy w poniedziałek”. Brakuje streszczenia w pięciu linijkach: odpowiedź, trzy decyzje, jedna liczba pieniędzy.
2. **To bardziej raport w zakładkach niż codzienny pulpit.** Nie ma widoku „wczoraj i ostatnie 7 dni” z alarmami na kohortach i lejku. Pozycja 2 proponuje takie alarmy, ale narzędzie ich nie pokazuje. Lista 245 surowych zmian to szum dla osoby, która prowadzi biznes. Zadanie mówi wprost: narzędzie, „na którym samemu prowadziłoby się ten biznes na co dzień”.
3. **Decyzyjność i drobiazgi.** Szerokie zakresy kwot (0–65 tys. zł, −31 do +180 tys. zł) i test Meta na 9. miejscu osłabiają wrażenie, że kandydat wie, co zrobi pierwsze. Błędy wyświetlania w najważniejszej zakładce (etykiety odnośników, procent przy ocenie) podważają obraz dbałości o szczegóły, który budują notatki.

### Czego brakuje wobec zadania

- **Macierz kohort tylko tygodniowa albo miesięczna.** Wykres ma tryb dzienny, ale macierz w trybie dziennym, na wybranym zakresie dat, lepiej spełniałaby wymóg „rozdzielczości dziennej”.
- **Podziały demograficzne w kohortach** (punkt 11).
- **Wpływ zdarzeń w złotych na osi zdarzeń.** Dziś w złotych opisane jest tylko Safari. Przy starcie kampanii L4, porannych opóźnieniach i zwrotach kwoty są dopiero w priorytetach. Zadanie pyta wprost: które zdarzenie zmieniło wynik.

### Moja decyzja

**Zaprosić do następnego etapu. To mocny kandydat.**
- **Na plus przesądzają:** poprawność liczb (wszystko, co przeliczyłem, się zgadza), dyscyplina definicji i uczciwość co do pewności. To rzadkie w zadaniach rekrutacyjnych.
- **Na minus, do sprawdzenia w rozmowie:**
  - czy kandydat umie skrócić przekaz do decyzji dla zarządu;
  - czy umie bronić kolejności, na przykład co zrobi z Meta na L4 w pierwszym tygodniu, skoro według jednej reguły wyłączenie zyskuje zawsze;
  - czy narzędzie jest dla niego pulpitem codziennej pracy, czy prezentacją wyników.
