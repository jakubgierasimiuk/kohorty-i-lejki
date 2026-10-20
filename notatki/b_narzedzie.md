# B — narzędzie, szkielet (sesja „B: narzędzie”, 2026-10-19)

Pierwsza wersja narzędzia: układ strony, lejek, oś zdarzeń i jakość danych. Kohorty dochodzą po drugim zatrzymaniu sesji retencji (`DECYZJE.md`, wpis „szkielet narzędzia (punkt B) przed końcem A5”). Wspólne notatki scala sesja prowadząca. Propozycje wpisów do nich są w sekcji „Propozycje wpisów do wspólnych notatek”.

**Status:** druga wersja narzędzia przyjęta przez Kubę 2026-10-20, po trzech poprawkach (sekcje 10 i 11). Trzecia wersja (2026-10-20, sekcja 12): wynik punktu C na stronie, czyli ostateczne „Czy to wzrost”, „Priorytety” i „Czego nie wiemy”. Kuba ją przejrzał i dał trzy poprawki (sekcja 13); wprowadzone, czekają na jego przyjęcie przed próbną publikacją. Propozycje wpisów do wspólnych notatek z sekcji 12 i 13 czekają na scalenie przez sesję prowadzącą. Nic nie jest opublikowane.

**Jak uruchomić lokalnie** (z głównego folderu projektu):
1. Jeśli zmieniły się wyniki lejka: `python -I analiza/b_eksport.py` (około 10 sekund, baza tylko do odczytu). Raport z kontrolą: `analiza/wyniki/b_eksport.txt`.
2. `cd narzedzie` i `python -I -m http.server 8765 --bind 127.0.0.1`, potem w przeglądarce `http://127.0.0.1:8765/`.
3. Strona otwiera się też dwuklikiem w `narzedzie/index.html`, bez serwera, bo dane są plikami skryptów, a nie JSON-em.

## 1. Decyzje Kuby na pierwszym zatrzymaniu (2026-10-19)

1. **Technologia: zwykły HTML, CSS i JavaScript, bez budowania, z jedną biblioteką do wykresów czasowych (uPlot).** Odrzucone warianty: Apache ECharts 6.1.0 (około 1 MB, około 20 razy cięższy, wygląd gotowego szablonu) i wykresy bez żadnej biblioteki (najwięcej pracy i ryzyka przed terminem). Wybór tej opcji był też zgodą Kuby na pobranie biblioteki do repozytorium.
2. **Układ: zakładki jak w aplikacji.** Pasek u góry z dziewięcioma sekcjami, każda pod własnym adresem (`#lejek`, `#zdarzenia`). Strona startowa to „Czy to wzrost”. Zdarzenia są pionowymi znacznikami na wykresach czasowych. Kliknięcie zdarzenia otwiera lejek z ustawionym filtrem. Odrzucony wariant: jedna długa strona z menu bocznym (bliżej raportu niż narzędzia).
3. **Sekcja „Czy to wzrost” w pierwszej wersji: odpowiedź wstępna z liczbami przyjętymi w A3 i A4, z wyraźnym znacznikiem „wstępne”.** Odrzucony wariant: samo miejsce „w przygotowaniu”.
4. **Cztery zasady dla całej strony (dopisek Kuby, słowa przekazane w treści):**
   1. Przy każdym odsetku podajemy liczbę pacjentów albo sesji i okres.
   2. Żadnych liczb wpisanych ręcznie w tekstach. Nagłówki i opisy biorą liczby z plików danych, które tworzy `analiza/b_eksport.py`. Dzięki temu po dojściu wyników retencji nic się nie rozjedzie.
   3. Oś zdarzeń ma podział na obszary: lejek, retencja, obsługa pacjenta, jakość danych. Zdarzenia z sesji retencji dojdą później.
   4. Kiedy szkielet będzie gotowy do przeglądu Kuby, planujemy próbną publikację we wtorek wieczorem (20.10.2026): na chwilę publiczne repozytorium, sprawdzenie linku, powrót do prywatnego. Publikacja nadal wymaga wyraźnej zgody Kuby przy każdej akcji.

## 2. Biblioteka w repozytorium

| Plik w `narzedzie/lib/` | Źródło | Wersja | Rozmiar | SHA-256 |
|---|---|---|---|---|
| `uPlot.iife.min.js` | pakiet npm `uplot` (`https://registry.npmjs.org/uplot/-/uplot-1.6.32.tgz`), plik `dist/uPlot.iife.min.js` | 1.6.32 (14.03.2025) | 51 081 bajtów | `19c8d4c6ad88929a79f4ae49d6f7161566dfd0ba3d15cc495e974f787eb78f1f` |
| `uPlot.min.css` | ten sam pakiet, `dist/uPlot.min.css` | 1.6.32 | 1 857 bajtów | `df630c6a8d6f8eeaff264b50f73ce5b114f646ffd9a0bb74f049b0a00135fa04` |
| `uPlot.LICENSE.txt` | ten sam pakiet, `LICENSE` (licencja MIT) | 1.6.32 | 1 078 bajtów | `8f989229699b4fe2f1a0432d0e9edc338a8a911e250e2d1b01ecd770a5f5b1bd` |

- Pakiet pobrany poleceniem `npm pack uplot@1.6.32` do folderu tymczasowego poza projektem. npm sprawdził sumę kontrolną pakietu (integrity `sha512-KIMVnG68…TxpiQIw==`). Do repozytorium trafiły tylko trzy pliki z tabeli.
- Kontrola: w skrypcie biblioteki nie ma odwołań do sieci (`fetch`, `XMLHttpRequest`) ani `eval`. Strona niczego nie pobiera z internetu.

## 3. Co jest na stronie (pierwsza wersja)

Dziewięć zakładek, każda pod własnym adresem (`#wzrost`, `#kohorty`, `#lejek`, `#po-zakupie`, `#zdarzenia`, `#wynik`, `#jakosc`, `#priorytety`, `#niewiadome`). Na górze każdej strony jest informacja, że dane są syntetyczne. Strona nie ma logo ani identyfikacji wizualnej Telemedi.

- **Czy to wzrost** (wstępne, z wyraźnym znacznikiem). Dwa warunki osobno: nowi pacjenci w obu okresach i wzrost, powrót w 30, 60 i 90 dniach na tych samych dniach kalendarzowych, z liczbą pacjentów i datą ostatniej kohorty. Do tego zdanie o dashboardzie i mostek od dashboardu do danych oczyszczonych. Bez wniosków o przyczynach.
- **Lejek.** Nagłówek z trzech zdań i dwóch kart „do naprawienia”: Safari na iOS od 17.03.2026 oraz przeglądarki wbudowane w aplikacje (dopisek Kuby). Pod spodem sesje zalogowane od wejścia i zakupy samego TelemediGO jako osobna informacja. Filtry w jednym rzędzie: typ sesji (zwykłe, zalogowane od wejścia, zakup samego TelemediGO), kto (wszyscy, jeszcze nie kupowali, kupowali wcześniej), podział (całość, urządzenie, przeglądarka, system i przeglądarka, urządzenie i przeglądarka, źródło, kampania, strona wejścia), porównanie (rok do roku, ostatnie 90 dni, ostatnie 30 dni rok do roku, 60 dni przed i po każdym zdarzeniu, własne daty).
  - Tabela: wiersz na wartość podziału, sesje i udział w okresie B (pod spodem A), sześć przejść lejka. W każdej komórce odsetek w okresie B z liczbą sesji, od której go liczymy, a pod spodem odsetek w okresie A z liczbą sesji i zmiana w punktach procentowych.
  - Wykres dzień po dniu wybranej miary (każde przejście lejka, sesje dziennie albo udział w sesjach), z wygładzeniem z 1, 7 albo 28 dni. Okresy A i B są zaznaczone tłem, zdarzenia pionowymi liniami z numerami. Legenda pod kursorem pokazuje odsetek i liczbę sesji. Przeciąganie przybliża.
  - Ustawienia lejka zapisują się w adresie, więc każdy widok ma swój link. Z tego korzystają linki „Pokaż w lejku” w kartach napraw i w zdarzeniach.
- **Zdarzenia.** Oś czasu z czterema torami: lejek, retencja, obsługa pacjenta, jakość danych (dopisek Kuby). Tory retencji i obsługi pacjenta są na razie puste, z opisem, co dojdzie. Siedem zdarzeń: start sprzedaży TelemediGO w newsletterze (8.09.2025), start Meta na L4 (3.11.2025), remarketing Meta słabnie (od początku 2026), start TikToka (9.02.2026), Safari na iOS (17.03.2026), duplikaty zamówień (10–24.06.2026), godzina bez danych (17.05.2025). Przy każdym: data, co się zmieniło, o ile, skąd wiemy, link do lejka. Pod osią jest rozwijana tabela wszystkich 245 zmian wykrytych automatycznie, z linkiem do lejka ustawionego na okres przed i po.
- **Jakość danych.** Mostek od dashboardu do danych oczyszczonych, duplikaty z wykresem dziennym, zamówienia testowe z rozkładem na kwartały, godzina bez danych, drobne niespójności i lista rzeczy sprawdzonych i czystych.
- **Kohorty, Po zakupie, Wynik biznesu, Priorytety, Czego nie wiemy:** miejsca z opisem „w przygotowaniu”.

## 4. Jak spełniamy zasady Kuby i warunki techniczne

- **Liczby tylko z danych.** Każde zdanie z liczbą powstaje w `analiza/b_eksport.py`, z bazy (`czyste`, a przy jakości danych `surowe`) albo z plików części pozyskania (`a5p_lejek_dzienny.csv.gz`, `a5p_zdarzenia.csv`). Strona sama liczy tylko odsetki i sumy z danych dziennych dla wybranych filtrów. W tekstach HTML i JavaScript nie ma wyników wpisanych ręcznie. Są tylko parametry kontrolek, np. „suma z 7 dni”.
- **Kontrola zgodności.** Eksport porównuje 36 liczb z notatkami i raportami A3, A4 i A5 (pozyskanie), w tym z siatką dashboardu A3 komórka po komórce. Wynik: 0 różnic (`analiza/wyniki/b_eksport.txt`).
- **Odsetek z liczebnością i okresem.** W tabeli lejka każda komórka ma liczbę sesji. W retencji jest liczba pacjentów i data ostatniej kohorty. Nad tabelami są daty okresów A i B.
- **Pliki statyczne**, ścieżki względne, kotwice w adresie, bez serwera. Dane to 11 plików, razem 2,27 MB bez kompresji, największy ma 0,59 MB (`lejek_system_przegladarka.js`). Całość z biblioteką: 2,38 MB. Pliki lejka wczytują się dopiero po wybraniu podziału.
- **Bez internetu.** Biblioteka jest w repozytorium, a strona niczego nie pobiera z sieci, także czcionek. Jest `<meta name="robots" content="noindex, nofollow, noarchive">` i `robots.txt` z `Disallow: /`. Plik `.nojekyll` jest na wypadek hostingu GitHub Pages.
- **Wygląd:** paleta kolorów sprawdzona pod kątem daltonizmu, tryb jasny i ciemny według ustawień systemu. Kolor serii idzie za wartością, a nie za kolejnością w tabeli. Na telefonie (szerokość 390 px) strona nie przewija się w bok, a tabele przewijają się wewnątrz ramki.

## 5. Jak sprawdziłem stronę

- Zrzuty ekranu w przeglądarce bez okna (Playwright z Edge, tylko adres 127.0.0.1) dla szerokości 1366 px i 390 px: wszystkie zakładki, bez błędów w konsoli.
- Test klikania:
  - link „Pokaż w lejku” przy Safari na iOS ustawia podział, osoby, przejście i okresy; wiersz Safari na iOS pokazuje 66,2% z 1 763 i 45,1% z 1 553, zgodnie z notatką A5;
  - zmiana podziału, porównania i typu sesji przelicza tabelę;
  - kliknięcie znacznika na osi podświetla kartę zdarzenia;
  - link z tabeli wykrytych zmian otwiera lejek z okresami przed i po;
  - strona otwarta wprost z dysku działa tak samo.
- Skrypty testów są poza repozytorium (folder tymczasowy sesji), bo to narzędzia sprawdzające, a nie część wyniku.

## 6. Pułapka znaleziona przy commicie

Reguła `dane/` w `.gitignore` projektu wyklucza każdy folder o tej nazwie, także `narzedzie/dane/`. Dane strony nie trafiłyby do repozytorium, a strona opublikowana z repozytorium byłaby pusta. Folder danych strony nazywa się więc `narzedzie/dane_strony/`. `.gitignore` nie zmieniałem, bo to wspólny plik.

## 7. Co zostało na potem

1. *(zrobione 2026-10-20, sekcja 10)* **Kohorty** po scaleniu części retencji przez sesję prowadzącą. Potrzebne: kohorty dzienne z filtrami (źródło pozyskania, urządzenie i przeglądarka, pierwsza usługa, zniżka i TelemediGO, status pierwszego zamówienia), powroty w 30, 60 i 90 dniach, zamówienia i marża na pacjenta, zdarzenia retencji na osi. Eksport dojdzie jako nowa sekcja `analiza/b_eksport.py`.
2. *(zrobione 2026-10-20, sekcja 10)* **Po zakupie** oraz tory „retencja” i „obsługa pacjenta” na osi zdarzeń, z plików sesji retencji (`a5r_zdarzenia.csv`, `notatki/a5_retencja.md`) po ich przyjęciu.
3. *(wynik biznesu zrobiony 2026-10-20, sekcja 10; priorytety i niewiadome zrobione 2026-10-20, sekcja 12)* **Wynik biznesu, Priorytety, Czego nie wiemy** po punkcie C. Przy ekonomii kampanii obok wynik według sesji płatności, przy CRM okno 24 godzin i obok 7 dni (PLAN.md, punkt B).
4. **Próbna publikacja we wtorek wieczorem** (dopisek Kuby): na chwilę publiczne repozytorium, sprawdzenie linku, powrót do prywatnego. Hosting jest już wybrany (sekcja 9). Plik publikacji jest gotowy, a reszta to akcje Kuby na GitHubie.

## 9. Hosting: GitHub Pages (decyzja Kuby przekazana przez sesję prowadzącą, 2026-10-19)

- Kuba wybrał GitHub Pages z jednego repozytorium w neutralnej organizacji. Wpis: `DECYZJE.md`, „hosting narzędzia i repozytorium”, oraz `CLAUDE.md`, punkt 10.
- Adres będzie pod podścieżką, w rodzaju `https://<organizacja>.github.io/<repozytorium>/`. Sprawdzone: wszystkie ścieżki na stronie są względne (style, skrypty, biblioteka, pliki danych, także wczytywane później pliki lejka), a nawigacja jest na kotwicach.
- **Plik publikacji `.github/workflows/pages.yml`** (dopisany do plików tej sesji przez sesję prowadzącą). Publikuje folder `narzedzie/` po każdym commicie na `master` albo po ręcznym uruchomieniu. Uprawnienia: `contents: read`, `pages: write`, `id-token: write`. Oficjalne akcje przypięte do commitów (wersje sprawdzone poleceniem `git ls-remote` 2026-10-19):

  | Akcja | Wersja | Commit |
  |---|---|---|
  | `actions/checkout` | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
  | `actions/configure-pages` | v6.0.0 | `45bfe0192ca1faeb007ade9deae92b16b8254a0d` |
  | `actions/upload-pages-artifact` | v5.0.0 | `fc324d3547104276b827a68afc52ff2a11cc49c9` |
  | `actions/deploy-pages` | v5.0.1 | `368f82528645a54fb793d4d04e342629a3f51346` |

- Plik sam nic nie publikuje. Zadziała dopiero po włączeniu Pages w ustawieniach repozytorium, ze źródłem „GitHub Actions”.
- **Czego ta sesja nie robi:** zakłada organizację, tworzy zdalne repozytorium, dodaje `git remote`, robi push, zmienia widoczność ani włącza Pages. Każda z tych akcji jest osobna i wymaga zgody Kuby.
- Uwaga przy publikacji: przy publikacji przez GitHub Actions GitHub nie przepuszcza strony przez Jekyll, więc plik `.nojekyll` nie jest potrzebny, ale nie szkodzi. Warunki z wcześniejszego wpisu zostają bez zmian: `noindex`, `robots.txt`, biblioteka w repozytorium, każdy plik danych poniżej 25 MB (największy ma 0,59 MB).

## 8. Propozycje wpisów do wspólnych notatek (scala sesja prowadząca)

### Do `DECYZJE.md`
- **2026-10-19 — technologia i układ narzędzia (punkt B), pierwsze zatrzymanie.** Decyzje Kuby z sekcji 1 tej notatki:
  - HTML z biblioteką uPlot 1.6.32; odrzucone: ECharts i wykresy bez biblioteki;
  - zakładki jak w aplikacji; odrzucone: jedna długa strona;
  - wstępna odpowiedź „czy to wzrost” z liczbami A3 i A4; odrzucone: samo miejsce „w przygotowaniu”;
  - cztery zasady Kuby dla strony: odsetek z liczebnością i okresem, żadnych liczb wpisanych ręcznie w tekstach, oś zdarzeń w czterech obszarach, próbna publikacja we wtorek wieczorem.
- **Folder danych strony to `narzedzie/dane_strony/`**, bo `.gitignore` wyklucza każdy folder `dane/` (sekcja 6). Do rozważenia przez sesję prowadzącą: zmiana reguły na `/dane/`, żeby obejmowała tylko surowe dane w głównym folderze.

### Do `ZALOZENIA.md`
- **Na stronie narzędzia lejek liczymy tak jak w A5 (pozyskanie):** sesje zwykłe, dzień sesji w czasie polskim, „jeszcze nie kupowali” według pierwszego zakupu konta albo przeglądarki. Przy wygładzeniu wykresu odsetek to suma licznika z N dni podzielona przez sumę mianownika z tych samych dni, a nie średnia odsetków dziennych.

### Do `analiza/README.md`
Nowy wiersz tabeli:

| B | `python -I analiza/b_eksport.py` | Eksport danych do plików strony narzędzia (`narzedzie/dane_strony/*.js`): lejek dzienny w ośmiu podziałach, zdania z liczbami do nagłówków, oś zdarzeń, jakość danych, wstępna odpowiedź „czy to wzrost”. Kontrola 36 liczb wobec notatek i siatki A3. Uruchamiać po `a5p_lejek.py` i `a5p_zdarzenia.py`. Importuje `definicje.py`. Około 10 s. | `wyniki/b_eksport.txt`, `narzedzie/dane_strony/` |

### Do `PLAN.md`
- Punkt B, szkielet: zrobione (układ, lejek, oś zdarzeń, jakość danych, wstępne „czy to wzrost”), czeka na przegląd Kuby lokalnie. Dalej: kohorty, po zakupie, zdarzenia retencji, wynik biznesu, priorytety i niewiadome (sekcja 7 tej notatki). Próbna publikacja we wtorek wieczorem, po zgodzie Kuby.

### Do `ZNALEZISKA.md`
- Nic nowego w danych. Pułapka z `.gitignore` (sekcja 6) dotyczy repozytorium, a nie danych.

## 10. Druga wersja: kohorty, po zakupie, wynik biznesu (2026-10-20)

**Decyzja Kuby (przegląd szkieletu, 2026-10-20, słowa Kuby):** „Przejrzałem szkielet i przyjmuję go. A5 jest zamknięte i scalone, więc dobuduj teraz pozostałe zakładki z wyników A5. Kohorty: kohorty dzienne i powroty w 30, 60 i 90 dniach, z filtrami źródło (obie reguły), urządzenie i przeglądarka, pierwsza usługa, zniżka i TelemediGO. Po zakupie: punktualność według pory i specjalizacji, zwroty, oceny. Wynik biznesu: przychód i marża w czasie oraz ekonomia kampanii według obu reguł. Na osi zdarzeń dołóż zdarzenia z retencji i obsługi pacjenta. Priorytety i niewiadome zostaw jako miejsca na wynik punktu C. Te same zasady co dotąd: liczebność przy każdym odsetku, żadnych liczb wpisanych ręcznie. Nic nie publikuj. Zatrzymaj się u mnie z całością rano.”

Do tego dopisek Kuby z przeglądu ekonomii kampanii (`notatki/a5_ekonomia.md`, sekcja 11): obok wyniku po 90 dniach pokazujemy wynik po 180 dniach. Jest w tabeli ekonomii kampanii i w kohortach (okno 180 dni).

### Co doszło na stronie

- **Kohorty** (`#kohorty`). Dane są zapisane pacjent po pacjencie (40 918 nowych pacjentów, bez identyfikatorów), więc strona liczy dowolne połączenie filtrów.
  - Filtry: reguła źródła (przyjęta albo sesja płatności), źródło (kanał), kampania, nowe kampanie na L4 albo pozostałe, urządzenie, przeglądarka, pierwsza usługa, zniżka, TelemediGO kupione przy pierwszym zakupie, status pierwszego zamówienia, opóźnienie i pora pierwszej wizyty.
  - Podział na serie według każdego z tych wymiarów. Porównanie okresów A i B działa jak w lejku.
  - Tabela: nowi pacjenci, udział, powrót w 30, 60, 90 i 180 dniach, marża na pacjenta w 90 i 180 dniach. Przy każdej wartości stoi liczba pacjentów z pełnym oknem.
  - Wykres według dnia pierwszego zakupu: powrót, marża na pacjenta, nowi pacjenci dziennie albo udział, z wygładzeniem z 1, 7 albo 28 dni i ze zdarzeniami.
- **Po zakupie** (`#po-zakupie`): punktualność według pory i specjalizacji (wykres i tabela, okres 1 wobec okresu 2), powrót według opóźnienia pierwszej wizyty, zwroty, anulacje i wizyty nieodebrane według celu wizyty, oceny według opóźnienia.
- **Wynik biznesu** (`#wynik`): przychód z konsultacji po zwrotach (pierwsze i kolejne zamówienia), TelemediGO, koszt lekarza, kampanie, prowizja i marża, w miesiącach, tygodniach albo dniach, z sumami okresów. Pod spodem ekonomia kampanii z pliku sesji ekonomii (`a5e_kampanie.csv`): grupy, kampanie albo kanały, obie reguły źródła obok siebie, wynik na pacjenta po 90 i po 180 dniach. Gdy znak wyniku zależy od reguły, wiersz ma oznaczenie „niepewny”.
- **Oś zdarzeń:** tory retencji i obsługi pacjenta mają sześć zdarzeń z `a5r_zdarzenia.csv`:
  - udział nowych kampanii w nowych pacjentach (od 3.11.2025);
  - powrót w 30 dniach (10.02.2026);
  - marża na pacjenta w 30 dniach (od 30.10.2025);
  - kandydat w powrocie w 90 dniach w kampaniach działających w obu latach (2.03.2026, poniżej progu);
  - poranne opóźnienia u internisty (od 24.11.2025);
  - zwroty pierwszych zamówień po wizycie (od 13.11.2025).
  Linki prowadzą do kohort albo do zakładki „Po zakupie” z ustawionymi filtrami.
- **Czy to wzrost:** zostaje znacznik „wstępne”. Tekst odsyła do kohort, a ostateczną odpowiedź przygotowuje punkt C.
- **Priorytety i Czego nie wiemy:** miejsca na wynik punktu C.

### Kontrola liczb

- Eksport porównuje teraz 63 liczby z notatkami i raportami (A3, A4, A5: pozyskanie, retencja i ekonomia). Wynik: 0 różnic (`analiza/wyniki/b_eksport.txt`).
- Nowe kontrole: powroty w 30, 60, 90 i 180 dniach z liczbą pacjentów, marża na pacjenta w 30, 90 i 180 dniach, poranne opóźnienia u internisty od XI 2025 do II 2026, zwroty L4 (1 024 z 5 895 i 270 z 5 080), zwroty nowych kampanii w złotych, średnie oceny, przychód po zwrotach i zakupy TelemediGO w obu okresach, prowizja afiliacyjna, wynik nowych kampanii według obu reguł, kandydat z 2.03.2026.
- Oceny początkowo się nie zgadzały. Część retencji liczyła je tylko u internisty i osobno dla pacjentów nowych kampanii. Eksport liczy je teraz tak samo, a strona pozwala wybrać specjalizację i grupę pacjentów.
- W przeglądarce tabele pokazują te same liczby co notatki. Na przykład spadek powrotu w 90 dniach w kampaniach działających w obu latach to −1,9 punktu procentowego według przyjętej reguły i −3,5 według sesji płatności. Powrót po porannej wizycie u internisty spóźnionej ponad 30 minut to 10,1% (533 pacjentów) wobec 14,3% (35 pacjentów).

### Decyzje techniczne

- **Kohorty na stronie liczone z danych pacjent po pacjencie**, bez identyfikatorów i bez danych demograficznych. Zapisane są: dzień kohorty, dzień pierwszego powrotu, marża w 30, 60, 90 i 180 dniach (w dziesiątych częściach złotówki) i cechy pierwszego zakupu zakodowane jednym znakiem. Plik `kohorty.js` ma 1,44 MB.
- **Porównanie okresów w kohortach:** okres B obcinamy do kohort z pełnym oknem, a okres A do tej samej długości od jego początku. Przy porównaniu rok do roku to dokładnie te same dni kalendarzowe (ZALOZENIA 27). Przy własnych datach to ta sama długość.
- **Wynik w czasie:** przychód, zwrot i koszt lekarza liczymy w dniu płatności, TelemediGO w dniu zakupu, wydatki w dniu z pliku kampanii, a prowizję afiliacyjną według przyjętej reguły źródła, w dniu pierwszego zamówienia.
- **Nowe kampanie na L4 w zakładce „Po zakupie”** wyznaczamy według przyjętej reguły źródła, tak jak w części retencji.

### Pliki

- `analiza/b_eksport.py`: nowe części 5–8 (kohorty, po zakupie, wynik biznesu z ekonomią kampanii, zdarzenia retencji). Importuje definicje z `a5r_punktualnosc.py` (opóźnienie, pora, nowe kampanie) i `a5r_struktura.py` (usługa, zniżka), żeby nie powielać kodu. Działa około 13 sekund.
- `narzedzie/widoki.js`: nowe zakładki. `narzedzie/app.js` udostępnia im funkcje pomocnicze i wczytuje dane dopiero przy pierwszym wejściu na zakładkę.
- Dane strony to 14 plików, razem 4,1 MB bez kompresji, największy ma 1,44 MB (`kohorty.js`). Cała strona ma 4,25 MB.

### Propozycje wpisów do wspólnych notatek

- **`DECYZJE.md`:** przyjęcie szkieletu przez Kubę 2026-10-20 i polecenie dobudowania kohort, zakładki „Po zakupie” i wyniku biznesu (słowa Kuby wyżej).
- **`ZALOZENIA.md`:** sposób porównania okresów w kohortach przy własnych datach oraz dni księgowania w wyniku biznesu (sekcja „Decyzje techniczne”).
- **`analiza/README.md`:** w wierszu `b_eksport.py` dopisać kohorty, „Po zakupie”, wynik biznesu i zdarzenia retencji; kontrola 63 liczb; około 13 sekund; importuje `a5r_punktualnosc.py` i `a5r_struktura.py`.
- **`PLAN.md`:** punkt B: kohorty, „Po zakupie”, wynik biznesu i oś zdarzeń zrobione. Zostają priorytety i niewiadome z punktu C oraz ostateczna odpowiedź „czy to wzrost”.

## 11. Trzy poprawki Kuby po przeglądzie drugiej wersji (2026-10-20)

**Poprawki Kuby (wklejone do rozmowy, w skrócie):**
1. „Po zakupie” nie może mówić, że dane „pasują do hipotezy przeciążenia, ale jej nie dowodzą”. Przyjęte odczytanie: przy tym samym porannym ruchu w dniu opóźnień jest o 26,4 punktu procentowego więcej niż rok wcześniej, więc spadła poranna przepustowość (obsada, organizacja zapisów albo lekarze zajęci pacjentami spoza B2C), a nie tylko przybyło pacjentów. Pokazać to porównanie.
2. W „Kohortach” brakuje macierzy kohort (kohorta tygodniowa × dni od pierwszego zakupu: 7, 14, 30, 60, 90, 180, mapa ciepła) i krzywej powrotu według dnia od pierwszego zakupu dla okresu A i B, z tymi samymi filtrami.
3. W „Wyniku biznesu” marża w ostatnim kwartale jest niższa niż rok wcześniej mimo dwa razy wyższych wydatków, a suma roczna (+26,6%) to ukrywa. Pokazać marżę po kwartałach rok do roku z wydatkami obok i dopisać to zdanie w nagłówku zakładki.

**Co zrobione:**
1. **Po zakupie.** Usunięte zdanie o hipotezie. Nowa karta „Opóźnienia przy tym samym porannym ruchu”: trzy zdania (różnica przy tym samym ruchu, brak zależności od ruchu w okresie 1 i w obrębie miesiąca, odczytanie) i tabela przedziałów ruchu, okres 1 wobec okresu 2, z liczbą wizyt i dni, dla wszystkich pacjentów albo spoza nowych kampanii. Liczone tym samym kodem co `a5r_punktualnosc.py`, sekcje 3f–3g. Kontrola: +26,4 punktu procentowego, 5 przedziałów, 9 979 wizyt, zgodne. Tercyle ruchu w miesiącu różnią się od raportu retencji najwyżej o 0,4 punktu procentowego, bo przy równym ruchu o przydziale dnia do tercyla decyduje kolejność wierszy, a skrypt retencji jej nie ustalał. Eksport ustala ją według daty, a kontrola ma tolerancję 0,5 punktu.
2. **Kohorty.** Dwie nowe karty pod wykresem, z tymi samymi filtrami (bez podziału na serie):
   - macierz kohort: tygodnie albo miesiące × okna 7, 14, 30, 60, 90 i 180 dni, mapa ciepła z jednej barwy (skala osobno w każdej kolumnie), kropka przy kohorcie bez pełnego okna, kolumna z numerami zdarzeń z osi w danej kohorcie;
   - krzywa powrotu od 1. do 180. dnia dla okresu A i B. Na każdy dzień liczymy tylko kohorty, które go już osiągnęły, z tym samym obcięciem okresu A co w tabeli. Legenda pokazuje liczbę pacjentów i poziom B jako odsetek poziomu A. Przy porównaniu rok do roku krzywa kończy się na 27,5% i 22,2% w 180 dniach, jak w notatkach.
3. **Wynik biznesu.** Drugie zdanie nagłówka mówi wprost, że suma ukrywa przebieg w kwartałach. Trzecie podaje zmianę marży w każdym kwartale rok do roku: +71,4%, +43,0%, +13,0% i −6,8% w III kwartale 2026 (207 713 zł wobec 222 824 zł), choć wydatki na kampanie są 2,1 raza wyższe (181 555 zł wobec 87 431 zł). Nowa tabela „Kwartały rok do roku”: marża, wydatki na kampanie, przychód z konsultacji i TelemediGO, koszt lekarza, nowi pacjenci, z obu okresów i ze zmianą.
   - **Uwaga do sformułowania Kuby:** w lipcu 2026 marża jest jeszcze wyższa niż rok wcześniej (73 384 zł wobec 66 832 zł), niższa jest w sierpniu i wrześniu. Niższy jest więc cały III kwartał, a nie każdy z trzech miesięcy. Zdanie na stronie mówi to dokładnie.
   - Do tego zdanie o bazie porównania: we wrześniu 2025 TelemediGO dało 32 930 zł wobec średnio 11 238 zł miesięcznie wcześniej (start sprzedaży w newsletterze). Bez tego wrzesień 2026 wyglądałby na mniejszy spadek.
- Ze strony zniknęły wzmianki o Kubie (stronę czyta Telemedi). W kodzie i w notatkach zostają.
- Kontrola eksportu: 66 liczb, 0 różnic.

**Propozycja wpisu do `DECYZJE.md`:** trzy poprawki Kuby do drugiej wersji narzędzia (jak wyżej) i ich wykonanie. Do `ZNALEZISKA.md` (sekcja wyniku biznesu): marża w III kwartale 2026 niższa niż rok wcześniej o 6,8% przy wydatkach na kampanie wyższych 2,1 raza; suma roczna +26,6% to ukrywa.

**Decyzja Kuby (2026-10-20, po przeglądzie poprawek, słowa Kuby):** „Przejrzałem poprawki i przyjmuję drugą wersję narzędzia. Przekaż wynik sesji prowadzącej, żeby scaliła propozycje wpisów z notatki b_narzedzie.md.”

## 12. Trzecia wersja: wynik punktu C na stronie (2026-10-20)

**Zlecenie sesji prowadzącej:** przenieść na stronę wynik punktu C, przyjęty przez Kubę 2026-10-20: ostateczną odpowiedź „czy to wzrost” bez znacznika „wstępne”, listę 12 priorytetów i listę 18 niewiadomych. Teksty idą za `notatki/c_szkic.md` (sekcje 1, 3 i 4) w wersji z commitu `8ebd2a4`. To wersja po pięciu poprawkach spójności Kuby (`bd827b0`) i po uwagach z końcowej weryfikacji Codeksem (model Astra), które sesja prowadząca przyjęła i wprowadziła (`DECYZJE.md`, wpis o weryfikacji Astrą).

### Co doszło na stronie

- **Czy to wzrost** (`#wzrost`), bez znacznika „wstępne”:
  - werdykt w jednym zdaniu i dwa zdania odpowiedzi;
  - dwie karty: „Więcej pacjentów: tak” (z liczbami, także bez nowych kampanii i w kanałach bezpłatnych) i „Lepsza retencja: nie” (tabela powrotu w 30, 60, 90 i 180 dniach z liczbą pacjentów, marża na pacjenta, wynik bez nowych kampanii, usługi, liczba powracających osób);
  - karta „Wynik pod koniec okresu”: zdanie zamykające o III kwartale 2026, zdanie o skali problemu w Safari na iOS, tabela marży po kwartałach rok do roku z wydatkami na kampanie obok i trzy zdania pod nią;
  - karta „Najważniejsze zastrzeżenia” (siedem punktów z sekcji 1c szkicu);
  - dashboard i mostek do danych oczyszczonych bez zmian, odnośniki do kohort, wyniku biznesu i jakości danych.
- **Priorytety** (`#priorytety`):
  - wstęp, zasady listy (kwoty się nie sumują, kolejność to waga, a nie kalendarz, zasada budżetu, czas wdrożenia to szacunek) i definicje okresów, reguł źródła i nowych kampanii;
  - tabela przeglądu 12 pozycji: co robimy, ile warte rocznie w marży, pewność, wdrożenie. Numer i nazwa prowadzą do karty (`#priorytety?p=N` przewija do karty i ją podświetla);
  - 12 kart. Każda ma: z danych, ile warta i założenia, naprawić albo wyłączyć (tam, gdzie dotyczy), propozycję albo co robimy, po czym poznamy, wdrożenie, odnośniki do zakładek z danymi i pole „skąd liczby”;
  - przy TikToku i Meta na L4 tabela: wynik dziś, wynik po naprawie zwrotów, zmiana marży po wyłączeniu przy 100%, 50% i 0% pacjentów dodatkowych. Kolumny: obie reguły źródła po 90 i po 180 dniach. W komórce kwota z dni działania kampanii, a pod nią pełny rok. Przy `gs_generic_specjalisci` ta sama tabela z kwotami rocznymi, przy cenniku specjalistów tabela marży na wizycie;
  - karta „Czego proponujemy teraz nie robić”.
- **Czego nie wiemy** (`#niewiadome`): tabela 18 pozycji (czego nie wiemy, dlaczego to ważne, test albo brakujące dane) z odnośnikiem do pozycji listy priorytetów.
- Na telefonie tabele przeglądu i niewiadomych układają się w karty, a każda komórka ma podpis.

### Jak to jest zbudowane

- **`analiza/b2_eksport_c.py`** zapisuje `narzedzie/dane_strony/c.js` (`window.D.C`). Działa bez bazy, w około sekundę. Każdą liczbę odczytuje z raportów (108 odczytów): z `c_priorytety.txt` i `c_telemedigo.txt`, a tam, gdzie szkic powołuje się na wcześniejsze części, z `a5e_scenariusze.txt`, `a5e_kampanie.csv`, `a5e_ekonomia.txt`, `a5r_kohorty.txt`, `a5r_struktura.txt`, `a5r_po_zakupie.txt`, `a5r_punktualnosc.txt`, `a5p_zdarzenia.txt`, `a5p_zalogowane.txt`, `a5p_sezon.txt` i `a2_jakosc.txt`. Kilka liczb liczy z odczytanych: udział nowych kampanii w spadku powrotu (46–71%), próg decyzji Meta, przeliczenie na pełny rok, zakresy od najniższej do najwyższej wartości.
- Czas wdrożenia i parametry planu testów to szacunek ze szkicu, a nie liczby z danych. Są w jednym słowniku na górze skryptu.
- **`analiza/b_eksport.py`** uruchamia ten eksport na końcu i dopisuje jego kontrole do swojego raportu. Jedno polecenie (`python -I analiza/b_eksport.py`) odświeża całą stronę.
- **`narzedzie/widoki_c.js`** rysuje trzy zakładki i nie wpisuje żadnej liczby. Rysowanie „Czy to wzrost” przeszło tu z `app.js`, który udostępnia funkcję mostka.
- Raporty: `analiza/wyniki/b_eksport_c.txt` (kontrole, liczby dopisane poza szkicem, lista odczytów) i sekcja 4 w `analiza/wyniki/b_eksport.txt`.

### Kontrola liczb

- **`b_eksport.txt`: 91 kontroli, 0 różnic** (było 66). Nowych jest 25:
  - zgodność między raportami: zdania `c_priorytety.txt` wobec tabel `a5e_scenariusze.txt` (TikTok i Meta, oba horyzonty, naprawa zwrotów), przeliczenie na pełny rok, próg Meta (85,4% i 84,5%), `gs_generic_specjalisci` wobec `a5e_kampanie.csv`, powrót w 90 dniach wobec `a5r_kohorty.txt`, spadek marży III kwartału, zwroty L4 w dwóch raportach, zamówienia testowe;
  - zgodność z tym, co eksport liczy sam na bazie: nowi pacjenci, powrót w 30, 60 i 90 dniach z liczbą pacjentów, zamówienia dashboardu i po oczyszczeniu, marża w ośmiu kwartałach;
  - **zgodność ze szkicem:** każda liczba w każdym zdaniu strony (738 liczb w 45 fragmentach) musi stać w tym samym fragmencie `c_szkic.md`: w sekcji 1, w zasadach listy, w wierszu przeglądu, w karcie tej samej pozycji albo w wierszu tej samej niewiadomej. Wyjątek to liczby dopisane poza szkicem: liczebność przy odsetku (zasada Kuby), okresy i kwoty w dniach działania kampanii. Każda z nich jest odczytana z raportu i wypisana w raporcie jako „dodana”. Wynik: 0 liczb bez pokrycia.
- Ta kontrola zadziałała dwa razy. Przy pierwszym przebiegu wyłapała mój błąd (zła kolumna marży nowych kampanii: 32,7 zł zamiast 36,3 zł). Potem wyłapała poprawki po Astrze, które sesja prowadząca wnosiła do szkicu w trakcie mojej pracy (np. −23,3 → −23,2 tys. zł przy `gs_generic_specjalisci`). Po ich przeniesieniu wynik to 0.

### Poprawki przy okazji

- **Lejek:** odnośnik, w którym brakowało części ustawień, zostawiał je z poprzedniego widoku (np. typ sesji i daty). Teraz brakujące ustawienia wracają do domyślnych, tak jak w kohortach. Dotyczy to też odnośników „Pokaż w lejku” na osi zdarzeń.
- **Telefon:** siatka kart priorytetów rozszerzała się do szerokości tabeli kampanii (874 px zamiast 375 px). Poprawione w stylach.

### Jak sprawdziłem

- Podgląd http://127.0.0.1:8765/ w przeglądarce w aplikacji: wszystkie 9 zakładek bez błędów w konsoli. Przy szerokości 375 px żadna zakładka nie przewija się w bok, a przy 1366 px tabele mieszczą się w ramkach.
- 18 odnośników z kart i z „Czy to wzrost”: każdy otwiera właściwą zakładkę z ustawionym filtrem albo z podświetlonym zdarzeniem.
- `#priorytety?p=N` przewija do karty i ją podświetla, także na telefonie.
- Na stronie nie ma wzmianek o Kubie (wyszukiwanie w plikach strony).
- Nie sprawdzałem otwarcia strony wprost z dysku, bo przeglądarka w aplikacji nie otwiera plików z dysku. `c.js` jest plikiem skryptu, tak jak pozostałe dane, więc ten mechanizm się nie zmienił.

### Decyzje techniczne

- Sekcja 2 szkicu (TelemediGO) nie ma osobnej zakładki, bo nie było jej w zleceniu. Jej liczby są w pozycjach 10 i 12 i w zastrzeżeniach. To kandydat na kolejny krok, jeśli Kuba uzna, że warto.
- Pełny rok w tabelach kampanii = kwota z dni działania × 365 / dni działania, bez zaokrąglania mnożnika (tak liczy `c_priorytety.py`).
- `gs_generic_specjalisci`: wynik dziś i wyłączenie przy 100% pacjentów dodatkowych bez pośredniego zaokrąglania marży (uwaga Astry), wyłączenie przy 50% i 0% jak w raporcie (P7), bo tak stoi w szkicu.
- Przy liście priorytetów pole „skąd liczby” wskazuje syntezę rundy kilku modeli AI (`notatki/konsylium/c_priorytety/synteza.md`) i recenzję liczb (`notatki/recenzje/c_codex.md`).

### Pliki

- Nowe: `analiza/b2_eksport_c.py`, `analiza/wyniki/b_eksport_c.txt`, `narzedzie/widoki_c.js`, `narzedzie/dane_strony/c.js`.
- Zmienione: `analiza/b_eksport.py` (uruchamia eksport punktu C), `analiza/wyniki/b_eksport.txt`, `narzedzie/index.html`, `narzedzie/app.js`, `narzedzie/styl.css`, `narzedzie/dane_strony/podsumowanie.js` i `jakosc.js` (przeliczone, te same liczby).
- Dane strony: 15 plików, razem 4,15 MB bez kompresji, `c.js` ma 54 KB.

### Propozycje wpisów do wspólnych notatek (scala sesja prowadząca)

- **`DECYZJE.md`:** wynik punktu C przeniesiony na stronę (ostateczne „czy to wzrost”, 12 priorytetów, 18 niewiadomych), za szkicem z commitu `8ebd2a4`, czyli z uwagami Astry. Czeka na przegląd Kuby lokalnie, przed próbną publikacją.
- **`ZALOZENIA.md`:** na stronie kwota kampanii na pełny rok = kwota z dni działania × 365 / dni działania; przy każdym odsetku w tekstach punktu C liczebność dopisana z raportów.
- **`analiza/README.md`:** nowy wiersz tabeli:

  | B | `python -I analiza/b2_eksport_c.py` | Wynik punktu C na stronę narzędzia (`narzedzie/dane_strony/c.js`): „czy to wzrost”, priorytety, czego nie wiemy. Liczby z raportów `c_*` i A5, kontrola zgodności między raportami i ze szkicem `notatki/c_szkic.md`. Bez bazy, około sekundy. Uruchamia go też `b_eksport.py`. | `wyniki/b_eksport_c.txt`, `narzedzie/dane_strony/c.js` |

  W wierszu `b_eksport.py`: na końcu uruchamia `b2_eksport_c.py`, kontrola 91 liczb.
- **`PLAN.md` i `PRZEKAZANIE.md`:** punkt B: „Priorytety”, „Czego nie wiemy” i ostateczne „czy to wzrost” zrobione, czekają na przegląd Kuby; kolejny krok to próbna publikacja za zgodą Kuby.
- **`ZNALEZISKA.md`:** nic nowego w danych.

## 13. Trzy poprawki Kuby po przeglądzie trzeciej wersji (2026-10-20)

**Poprawki Kuby (wklejone do rozmowy, słowa Kuby):** „Przejrzałem trzecią wersję, dobra robota. Trzy rzeczy, zanim ją przyjmę: 1. W zakładce »Priorytety« daj na górę tabelę przeglądu, a zasady listy i definicje pod nią. Czytelnik ma najpierw zobaczyć, co robimy. 2. Osobnej zakładki o TelemediGO nie rób. Dodaj za to krótką kartę w »Czy to wzrost«: skąd +40%, czy rośnie odsetek kupujących, ile dają opłaty wobec zniżek i że rozstrzygnie to test z pozycji 12. To jedna z czterech liczb dashboardu, więc odpowiedź powinna ją objąć. 3. W niewiadomej 1 dopisz horyzont tak jak w pozycji 9 (90 i 180 dni). Potem jeszcze raz kontrola liczb, commit i daj znać.”

**Co zrobione:**
1. **Priorytety:** pod wstępem najpierw tabela przeglądu, a pod nią zasady listy i definicje.
2. **Czy to wzrost:** nowa karta „TelemediGO: skąd +40,3% sprzedaży”, między kartami o pacjentach i retencji a kartą „Wynik pod koniec okresu”. Treść idzie za sekcją 2 szkicu (2.1, 2.2 i 2.4):
   - zdanie główne: wzrost o 709 zakupów to więcej zamówień i pełny rok sprzedaży w newsletterze, a odsetek kupujących nie rośnie;
   - tabela typów zakupu (przy kasie z pierwszym zamówieniem, z kolejnym, osobno z newslettera) w obu okresach, ze zmianą i udziałem we wzroście;
   - start sprzedaży w newsletterze (23 dni w okresie 1, 225 członkostw);
   - odsetek kupujących przy kasie z liczbą zamówień: przy pierwszym zamówieniu spada (5,58% → 4,41%), w całości przez pacjentów nowych kampanii (1,5%); bez nich 5,58% wobec 5,63%; przy kolejnych rośnie lekko;
   - opłaty wobec zniżek: członkostwa z okresu 1, −27 388 zł, czyli −15,57 zł na członkostwo, przy założeniu tych samych wizyt; w okresie 2 przybliżenie −10,7 zł;
   - powroty kupujących (34,7% wobec 20,0%) i zdanie, że rozstrzygnie to test z pozycji 12, z odnośnikiem do karty.
3. **Niewiadoma 1:** „od −30,6 tys. zł (90 dni) albo −32,9 tys. zł (180 dni) do +179,6 tys. zł na pełny rok (pozycja 9; próg decyzji około 85% pacjentów dodatkowych: 85,4% w 90 dniach i 84,5% w 180 dniach)”.

**Kontrola liczb:** `b_eksport.txt`: 93 kontrole, 0 różnic. Kontrola ze szkicem obejmuje teraz 790 liczb w 46 fragmentach. Karta TelemediGO jest porównywana z sekcją 2 szkicu. W niewiadomej 1 liczby horyzontu 180 dni i oba progi są dopisane poza szkicem (dopisek Kuby), odczytane z `c_priorytety.txt` (P11) i wypisane w raporcie jako „dodane”.

**Błąd złapany przy czytaniu, a nie przez kontrolę:** w pierwszej wersji karty zdanie „bez nich odsetek stoi” brało wiersz okresu 1 zamiast okresu 2 („5,58% wobec 5,58%”). Kontrola ze szkicem tego nie wykryła, bo obie liczby były poprawne, tylko z niewłaściwego wiersza. Poprawione, a do kontroli doszły dwie zgodności, które wyłapałyby taką pomyłkę: pacjenci bez nowych kampanii w raporcie TelemediGO wobec `c_priorytety.txt` (17 419) i pierwsze zamówienia w obu okresach wobec liczby nowych pacjentów (16 231 i 24 687).

**Sprawdzone w przeglądarce:** karta TelemediGO i jej cztery odnośniki (pozycje 12 i 10, kohorty według TelemediGO przy pierwszym zakupie, lejek zakupów samego TelemediGO); kolejność kart w „Priorytetach”; niewiadoma 1; wszystkie 9 zakładek na 375 px bez przewijania w bok; konsola bez błędów. Tabela typów zakupu na telefonie przewija się wewnątrz swojej ramki, jak pozostałe tabele.

**Propozycje wpisów do wspólnych notatek (scala sesja prowadząca):**
- **`DECYZJE.md`:** trzy poprawki Kuby do trzeciej wersji narzędzia (słowa wyżej) i ich wykonanie.
- **`notatki/c_szkic.md`, sekcja 4, wiersz 1:** dopisać horyzont 180 dni (−32,9 tys. zł) i oba progi (85,4% i 84,5%), tak jak na stronie, żeby szkic i strona mówiły to samo.
- **`analiza/README.md`:** w wierszu `b2_eksport_c.py` dopisać kartę TelemediGO (liczby z `c_telemedigo.txt`); w wierszu `b_eksport.py` kontrola 93 liczb.
