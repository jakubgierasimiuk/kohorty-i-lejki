# B — narzędzie, szkielet (sesja „B: narzędzie”, 2026-10-19)

Pierwsza wersja narzędzia: układ strony, lejek, oś zdarzeń i jakość danych. Kohorty dochodzą po drugim zatrzymaniu sesji retencji (`DECYZJE.md`, wpis „szkielet narzędzia (punkt B) przed końcem A5”). Wspólne notatki scala sesja prowadząca. Propozycje wpisów do nich są w sekcji „Propozycje wpisów do wspólnych notatek”.

**Status:** szkielet gotowy do drugiego zatrzymania, czyli przeglądu Kuby lokalnie. Nic nie jest opublikowane.

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

1. **Kohorty** po scaleniu części retencji przez sesję prowadzącą. Potrzebne: kohorty dzienne z filtrami (źródło pozyskania, urządzenie i przeglądarka, pierwsza usługa, zniżka i TelemediGO, status pierwszego zamówienia), powroty w 30, 60 i 90 dniach, zamówienia i marża na pacjenta, zdarzenia retencji na osi. Eksport dojdzie jako nowa sekcja `analiza/b_eksport.py`.
2. **Po zakupie** oraz tory „retencja” i „obsługa pacjenta” na osi zdarzeń, z plików sesji retencji (`a5r_zdarzenia.csv`, `notatki/a5_retencja.md`) po ich przyjęciu.
3. **Wynik biznesu, Priorytety, Czego nie wiemy** po punkcie C. Przy ekonomii kampanii obok wynik według sesji płatności, przy CRM okno 24 godzin i obok 7 dni (PLAN.md, punkt B).
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
