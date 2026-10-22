# F — kontrola techniczna ostatecznej wersji (część 2 ostatniej kontroli przed publikacją)

**Data:** noc z 22 na 23 października 2026. **Wersja:** `HEAD` na master, commit `a4d52c9`. Strona była sprawdzana z plików na dysku po ponownym eksporcie; treść danych jest identyczna z commitem (punkt 1).
**Zlecenie Kuby:** „Kontrola techniczna ostatecznej wersji: kontrola liczb w eksporcie i kontrola liczb na wykresach względem tekstu kart, 9 zakładek na komputerze i telefonie, tryb jasny i ciemny, konsola, odnośniki z filtrami po odświeżeniu strony, brak pobierania czegokolwiek z internetu, czas ładowania.”
**Zasady tej części:** niczego nie poprawiano w plikach strony, skryptach ani wspólnych notatkach; bez commitów; strony otwierane tylko z 127.0.0.1.

## Puenta

**Wersja `a4d52c9` jest technicznie gotowa do publikacji po jednej małej poprawce.** Liczby się zgadzają, strona nie pobiera niczego z internetu i ładuje się szybko także na wolnym telefonie.

- **Przed wysłaniem: 1 problem.** Na tablecie trzymanym pionowo i w wąskim oknie (szerokość od 761 do około 990 pikseli) pasek zakładek chowa „Priorytety” i „Czego nie wiemy”. Pasek da się przewinąć w bok, ale nic tego nie pokazuje. Poprawka to jedna reguła w stylach, sprawdzona w przeglądarce (lista poprawek, pozycja 1). Kuba może uznać to za kosmetykę, bo obie zakładki są osiągalne przez odnośniki i przycisk „Dalej”.
- **Materiał na rozmowę: 10 drobnych spraw strony i 1 uwaga do skryptu kontroli** (zrzut całej strony urywa się na 16 384 pikselach). Najbardziej widoczne sprawy strony dotyczą telefonu: w Safari zakładka „Lejek” daje się przesunąć w bok o około 100 pikseli, a w tabelach kohort i lejka ostatnie cyfry widać dopiero po przesunięciu tabeli.
- **Liczby:** eksport przeszedł 115 kontroli bez różnic. Liczby na wykresach porównano z tekstem i tabelami kart w 1 956 miejscach na każdy silnik przeglądarki. W Edge, w WebKit (silnik Safari) i w Firefoksie nie było ani jednej niezgodności.
- **Odnośniki:** 305 różnych odnośników z filtrami w adresie otwiera ten sam stan po wejściu wprost i po odświeżeniu.
- **Sieć i czas:** każde żądanie idzie do lokalnego serwera. Na telefonie z wolnym 4G i czterokrotnie wolniejszym procesorem pierwsza zakładka jest gotowa po 1,6 sekundy, a najcięższa („Kohorty”) po kolejnych 2,2 sekundy.

## Wynik w liczbach

| Punkt zlecenia | Sprawdzeń | Wyszło źle |
|---|---|---|
| 1. Liczby w eksporcie | 115 kontroli krzyżowych, 4 218 liczb w tekstach wobec szkiców, 15 plików danych porównanych z commitem wartość po wartości | 0 (zmieniły się tylko daty przeliczenia, skrót commitu i szum zmiennoprzecinkowy w 11 wartościach) |
| 2. Liczby na wykresach wobec tekstu kart | 1 956 porównań na silnik, razem 5 868 w Edge, WebKit i Firefoksie | 0 niezgodności; 4 uwagi kosmetyczne |
| 3. 9 zakładek, komputer i telefon, tryb jasny i ciemny, konsola | 36 widoków zakładek, 628 sprawdzeń odnośników, 26 532 teksty i 1 252 elementy wykresów zmierzone pod kątem kontrastu, 25 obejrzanych fragmentów zrzutów | 0 błędów w konsoli; 3 sprawy kosmetyczne (tabele na telefonie, kontrast liczb na kolorowych słupkach, ucięte podpisy linii); 1 uwaga do skryptu zrzutów (limit 16 384 pikseli wysokości) |
| 4. Odnośniki z filtrami po odświeżeniu | 305 odnośników, 8 251 sprawdzeń; 12 zmian filtrów z odświeżeniem; 2 przejścia wstecz i dalej (8 kroków) | 0 błędów (6 trafień to porządkowanie adresu bez zmiany widoku) |
| 5. Nic nie jest pobierane z internetu | 92 żądania w 4 wariantach; przeszukanie 27 plików strony | 0 żądań poza 127.0.0.1 |
| 6. Czas ładowania | 4 warianty × 9 zakładek | bez problemu (najwolniej 7,7 s dla „Kohort” bez kompresji na wolnym 4G, z kompresją 2,2 s) |
| 7. Publikacja i przeglądarki | plik GitHub Pages, robots i noindex, podścieżka, 768 i 1920 px, WebKit i Firefox na 2 szerokościach | 1 przed wysłaniem (pasek zakładek na tablecie), 1 kosmetyczny (Safari: „Lejek” przesuwa się w bok) |

## 1. Liczby w eksporcie

**Wynik: eksport na tym samym stanie daje te same dane strony.** Różnią się tylko metadane i szum zmiennoprzecinkowy, którego na stronie nie widać.

**Uruchomienie** (kolejność z `analiza/README.md`):
- `python -I analiza/e_poprawki.py`: około 50 sekund, bez błędu. W raporcie `wyniki/e_poprawki.txt` zmieniła się tylko godzina w nagłówku; `e_poprawki.json` bez zmian.
- `python -I analiza/e_wykresy.py`: 5 sekund, „96 wierszy, 0 różnic wobec d_retencja”; `e_wykresy.json` bez zmian.
- `python -I analiza/b_eksport.py`: 7 sekund. **„Różnic: 0 z 115 kontroli.”** Pokrycie liczb w tekstach strony przez szkice:
  - teksty punktu C wobec `c_szkic.md`: 50 fragmentów, 1 176 liczb, 0 bez pokrycia;
  - teksty pozostałych zakładek wobec `d_teksty_strony.md`: 8 sekcji, 247 liczb, 0 bez pokrycia;
  - nowe teksty „Czy to wzrost”, „Priorytety” i „Czego nie wiemy” wobec notatek E: 45 kart, 1 297 liczb, 0 bez pokrycia;
  - nowe karty zakładek wobec notatek E: 36 kart, 1 498 liczb, 0 bez pokrycia.
- `python -I analiza/b2_eksport_c.py` uruchomiony osobno, bo raport `b_eksport_c.txt` w commicie był nieaktualny (opis niżej). Wynik: **„Różnic: 0 z 28 kontroli”**, pokrycie C 1 176 liczb, D 237 liczb w 7 sekcjach (bez tekstów dodatkowych, które dokłada tylko `b_eksport.py`), E 1 297 liczb, wszystkie z pokryciem. Plik `c.js` z tego uruchomienia jest identyczny z wersją z `b_eksport.py`, poza godziną przeliczenia.

**`git status` po eksporcie:** zmieniło się 6 śledzonych plików. Nie commitowano ich i nie cofano.
- `narzedzie/dane_strony/`: nowy skrypt `analiza/f_eksport_powtarzalnosc.py` porównał każdy z 15 plików danych z wersją z `HEAD` wartość po wartości (wynik: `analiza/wyniki/f_eksport_powtarzalnosc.txt`). **Różnic w treści: 0.**
  - 12 plików jest identycznych co do bajtu.
  - `c.js` i `podsumowanie.js` różnią się tylko godziną przeliczenia, a `podsumowanie.js` także skrótem commitu w stopce strony (`329d075` → `a4d52c9`).
  - `jakosc.js` różni się 11 wartościami w sumach przychodu w mostku dashboardu (na przykład 2 381 880,5999999936 → 2 381 880,599999993). Różnica jest mniejsza niż jedna miliardowa wartości i wynika z kolejności sumowania w bazie. Na stronie te liczby wyglądają tak samo.
- `analiza/wyniki/b_eksport.txt`: godzina, skrót commitu, rozmiar `jakosc.js` o 1 bajt większy (15 777 → 15 778 bajtów).
- `analiza/wyniki/e_poprawki.txt`: godzina w nagłówku.
- `analiza/wyniki/b_eksport_c.txt`: **w commicie był raport z 11:27**, który opisywał starszą wersję `c.js` (96 429 bajtów wobec 97 199 bajtów dziś; 1 292 wobec 1 297 liczb w kartach E). `b_eksport.py` dopisuje kontrole części C do swojego raportu, ale tego pliku nie odświeża. Odświeżył go dopiero osobny `b2_eksport_c.py` (lista poprawek, pozycja 11).

## 2. Liczby na wykresach wobec tekstu kart

**Wynik: na żadnym wykresie nie ma liczby, która nie zgadzałaby się z tekstem albo tabelą tej samej karty.** Dotyczy to obu szerokości i trzech silników przeglądarek.

**Narzędzie:** nowy skrypt `analiza/f_wykresy_tekst.py`. Czyta liczby z wyrenderowanej strony (DOM w przeglądarce): podpisy, podpowiedzi, teksty kart i tabele, także w zwiniętych sekcjach. Kodu, który rysuje wykresy, nie czyta. Wynik: `analiza/wyniki/f_wykresy_tekst.txt` (Edge); te same porównania w WebKit i Firefoksie: `f_wykresy_tekst_webkit.txt` i `f_wykresy_tekst_firefox.txt` (opcja `--silnik`).

| Silnik | 1 366 px | 375 px | Niezgodnych | Błędy w konsoli |
|---|---|---|---|---|
| Edge 155 | 992 | 964 | 0 | 0 |
| WebKit 26.0 (silnik Safari) | 992 | 964 | 0 | 0 |
| Firefox 146.0.1 | 992 | 964 | 0 | 0 |

Według zakładek (jeden silnik, obie szerokości): „Czy to wzrost” 192 porównania, „Kohorty” 118, „Lejek” 288, „Po zakupie” 420, „Zdarzenia” 66, „Wynik biznesu” 684, „Jakość danych” 60, „Priorytety” 100, „Czego nie wiemy” 28.

**Co porównano.** Gdy karta danej liczby nie podaje, skrypt bierze niezależne źródło i zapisuje je w raporcie przy każdym porównaniu.
- **„Czy to wzrost”:**
  - słupki nowych pacjentów (16 231, 17 419, 7 268, 24 687) wobec tekstu karty;
  - hantle powrotu w 30, 60, 90 i 180 dniach wobec tabeli karty: odsetki, zmiana w punktach procentowych i liczba pacjentów w podpowiedzi;
  - słupki TelemediGO wobec tabeli;
  - słupki kwartałów wobec tabeli: zmiana rok do roku i poziom w tysiącach złotych;
  - schodki mostka wobec tabeli mostka, także wiersze „bez zmian”;
  - kafelki werdyktu wobec wykresów i kart: +52% i +7% przeliczone ze słupków, 17% i 24% z hantla 90 dni, „×2,1” z wydatków III kwartału (+107,7%), +25% marży;
  - dopisek werdyktu (27%, „z 828 do 1 048 tys. zł”) wobec karty kwartałów.
- **„Kohorty”:**
  - hantle wobec tabeli nagłówka i wobec wiersza „Wszyscy w filtrze” tabeli „Kohorty w podziale”, którą przeglądarka liczy z danych pacjent po pacjencie, czyli inną drogą;
  - zdanie nad mapą wobec komórek mapy: średnia ważona liczbą pacjentów daje 23,6% dla kohort do października 2025 (w zdaniu „około 24%”) i 14,6% od marca 2026 (w zdaniu „około 15%”);
  - oba twierdzenia zdania o listopadzie 2025 i marcu 2026;
  - 6 stanów zdania: widoczne przy mapie miesięcznej, ukryte przy tygodniowej, dziennej i przy zawężeniu;
  - kolumna „Zdarzenia” mapy wobec dat 14 kart zdarzeń.
- **„Lejek”:**
  - hantle Safari wobec tekstu karty z tymi samymi okresami: 66,2% i 45,6% dla Safari, 64,8% i 63,4% dla pozostałych przeglądarek;
  - hantle przeglądarek w aplikacjach wobec tekstu i raportu `d_kampanie.txt`;
  - kolumny udziału nowych kampanii wobec tabeli miesięcy w karcie nagłówka i wobec rachunku w Pythonie na pliku `lejek_kampania.js` (24 miesiące, liczby sesji co do jednej);
  - wykres kroków wobec tabeli w wierszach „Razem” i „Safari”.
- **„Po zakupie”:**
  - 96 komórek opóźnień według godziny wobec tabeli, znak w znak;
  - podcieniowany blok poranny i kolumna zmiany;
  - zdania tekstu: „o 5:00 15,3% z 459 wizyt”, zakres 40–47% oraz „poza 5:00–13:59: 2,7% z 14 898 wizyt”, przeliczone z liczników w podpowiedziach;
  - hantle porannego ruchu wobec tabeli w obu stanach przełącznika „Pacjenci”.
- **„Zdarzenia”:**
  - numer, data i tytuł każdego znacznika osi wobec karty zdarzenia;
  - położenie znacznika na osi (zgodne z datą co do 0,6 piksela);
  - liczby przy chipach obszarów;
  - pionowa lista na telefonie;
  - listy zdarzeń pod wykresami dziennymi na wszystkich zakładkach.
- **„Wynik biznesu”:**
  - kwartały wobec tabeli kwartałów: marża przed kosztem kampanii przeliczona z przychodu minus koszt lekarza;
  - punkty ekonomii kampanii wobec tabeli w 12 stanach przełączników (3 poziomy × 2 okresy × 2 okna), razem ze znacznikiem „Znak zależy od przypisania”;
  - zdania karty: TikTok −4,6 i −17,8 zł, nowe kampanie +3,6 i −9,4 zł, po 180 dniach +7,0 i −5,2 zł.
- **„Jakość danych”:** schodki mostka; słupki zamówień testowych wobec tekstu (553 rok wcześniej, 1 518 w ostatnich 12 miesiącach, razem 2 071).
- **„Priorytety” i „Czego nie wiemy”:** wykres Safari w pozycji 1 wobec lejka; kwota, pewność i wdrożenie 12 pozycji w przeglądzie wobec pasków kart; pigułki 1–12; nazwy pozycji w kolumnie niewiadomych.

**Czego nie dało się porównać i dlaczego.** Wykresy dzienne rysuje biblioteka uPlot na płótnie, więc ich liczby nie istnieją w DOM; widać je tylko pod kursorem. Dotyczy to wykresu dzień po dniu i krzywej powrotu w „Kohortach”, wykresu dziennego „Lejka”, punktualności i zwrotów w „Po zakupie”, dwóch wykresów „Wyniku biznesu” i duplikatów w „Jakości danych”. Numery zdarzeń na tych wykresach sprawdzono przez listę pod wykresem, a sumy roczne „Wyniku biznesu” przez tekst karty i tabelę miesięcy.

**Uwagi przy porównaniu (liczby zgodne, kosmetyka):**
- ten sam krok lejka nazywa się na wykresie kroków „Logowanie albo założenie konta”, a w tabeli i w polu „Miara” „Logowanie albo konto”;
- hantle Safari: „po awarii” to dla Safari okres 17.03–30.09.2026, a dla pozostałych przeglądarek 17.03–15.05.2026. Przypis to opisuje, a tekst karty podaje liczby dla tych samych okresów;
- tabele powrotu mają różną kolejność kolumn: w „Czy to wzrost” najpierw rok wcześniej, w nagłówku „Kohort” najpierw ostatnie 12 miesięcy;
- podpis wiersza TelemediGO na wykresie jest krótszy niż w tabeli („Przy kasie z pierwszym zamówieniem” wobec „… zamówieniem pacjenta”).

## 3. Dziewięć zakładek: komputer i telefon, tryb jasny i ciemny, konsola

**Wynik: wszystkie zakładki rysują się w obu trybach i na obu szerokościach, w konsoli nie ma błędów, a w trybie ciemnym nic nie znika.** Do poprawy kosmetycznej są tabele na telefonie, kontrast liczb na kolorowych słupkach i ucięte podpisy na końcach linii.

**Istniejąca kontrola** `python -I analiza/e_przegladarka.py`, osobno w trybie jasnym i z opcją `--ciemny`: 9 zakładek przy 1 366 i 375 pikselach. Wynik w obu trybach: 0 problemów, 0 błędów w konsoli, bez przewijania strony w bok, wykresy mieszczą się w kartach. Działa 314 odnośników między zakładkami. Przycisk „Zakładki” na telefonie pojawia się po przewinięciu i ma 9 zakładek. Raporty i zrzuty leżą w katalogu tymczasowym sesji.

**Pomiar kontrastu** (nowy skrypt `analiza/f_kontrast.py`, wynik `analiza/wyniki/f_kontrast.txt`): każda zakładka z rozwiniętymi wszystkimi zwijanymi sekcjami, w czterech wariantach. Progi są według WCAG 2.1: 4,5:1 dla zwykłego tekstu, 3:1 dla dużego tekstu i dla elementów wykresu.
- **Teksty poniżej progu:** w trybie jasnym 15 z 6 805 (komputer) i 15 z 6 461 (telefon), w ciemnym 3 i 3. Wszystkie dotyczą dwóch miejsc:
  - białe liczby na częściach słupka w karcie „Więcej pacjentów”: 3,2:1 na pomarańczowym i 4,4:1 na niebieskim w trybie jasnym, 3,9:1 i 3,6:1 w ciemnym;
  - białe liczby w mapie kohort w przedziale 25–30% (12 komórek): 4,2:1, tylko w trybie jasnym.
- **Znaki danych na wykresach** (punkty, słupki, kolumny, znaczniki osi zdarzeń): 0 poniżej 3:1 z 322 na komputerze i 304 na telefonie.
- **Elementy pomocnicze** mają 1,6–2,1:1 i tak zostały zaprojektowane jako tło: odcinek łączący punkty hantla, linia zera i tło toru osi.
- **Znaczniki stanu** („Nie”, „Wysoka” i podobne) mają jasne tło, ale znaczenie niosą ikona i słowo.
- Nie ma tekstów uciętych przez pole ani tabel szerszych od ramki bez możliwości przewinięcia. Strona nie przewija się w bok.

**Obejrzane zrzuty** (pocięte Pillowem na fragmenty):
- tryb ciemny na komputerze: „Czy to wzrost” (3 fragmenty), „Kohorty” (3), „Lejek” (2), „Zdarzenia” i „Wynik biznesu”;
- telefon w trybie jasnym: „Czy to wzrost”, „Kohorty”, „Lejek”, „Po zakupie”, „Zdarzenia”, „Wynik biznesu” i „Priorytety”, a do tego zbliżenia wykresu dziennego i tabeli kohort;
- telefon w trybie ciemnym: „Czego nie wiemy” i rozwinięty przycisk „Zakładki”;
- tryb jasny na komputerze obejrzano na zrzutach z punktu 7 (768 i 1 920 pikseli); „Jakość danych” na telefonie i w trybie ciemnym sprawdzono tylko automatycznie (kontrola zakładek i pomiar kontrastu, bez błędów).

W trybie ciemnym linie, podpisy i numery zdarzeń na wykresach, znaczniki stanu, mapa kohort i tabele są czytelne. Na zrzutach widać trzy drobne rzeczy:
- **telefon:** tabele „Kohorty w podziale” i „Kroki lejka w podziale” w widoku jednej miary są szersze od ramki o 16 i 20 pikseli. Ostatnie cyfry widać dopiero po przesunięciu tabeli, na przykład „z 18 92” zamiast „z 18 924” albo „−1,” zamiast „−1,9”. Szersze tabele w „Po zakupie”, „Wyniku biznesu” i „Priorytetach” przewijają się w ramce zgodnie z projektem;
- **komputer:** podpisy na końcach linii wykresów dziennych są ucięte („Marża przed kosztem k…”, „Pozostałe kampanie i …”). Pełne nazwy są w legendzie pod wykresem;
- **telefon:** na wykresie zwrotów napis „Rok wcześniej” leży na szarych liniach (drobiazg).

**Uwaga do skryptu kontroli, nie do strony.** Zakładka „Priorytety” ma na telefonie 24 464 piksele wysokości. Zrzut całej strony w Edge (Chromium) ma limit 16 384 pikseli. Od tej wysokości zrzut z `analiza/e_przegladarka.py` (`375_priorytety.png` i `ciemny_375_priorytety.png`) powtarza górę strony, czyli nagłówek i przegląd, w połowie karty 7, zamiast pokazać pozycje 8–12. Zauważyła to sesja prowadząca. Potwierdziłam to na własnym zrzucie (wycinek 15 600–17 200 pikseli). Sesja prowadząca sprawdziła stronę zrzutami okna odcinkami po 6 000 pikseli: karta 7 przechodzi w kartę 8, wszystkie 12 kart się rysuje, bez błędów. Mój przegląd tej zakładki objął tylko pierwsze 6 000 pikseli zrzutu, więc nie opierał się na wadliwej części. Kontrole liczb i kontrastu czytają DOM, a nie zrzuty, i objęły wszystkie 12 kart. Pozostałe zakładki są niższe niż 10 000 pikseli.

## 4. Odnośniki z filtrami po odświeżeniu strony

**Wynik: każdy odnośnik z parametrami otwiera właściwą zakładkę z właściwymi filtrami, podświetla właściwą kartę i przewija do niej. Po odświeżeniu stan jest ten sam.**

**Narzędzie:** nowy skrypt `analiza/f_odnosniki.py`, wynik `analiza/wyniki/f_odnosniki.txt`, Edge przy 1 366 pikselach.
- **Zebrane odnośniki:** 305 różnych adresów z 397 miejsc na stronie. Jest wśród nich 245 odnośników „w lejku” z tabeli wykrytych zmian, 14 do zdarzeń (`?z=`), 14 do niewiadomych (`?n=`), 12 do pozycji priorytetów (`?p=`), 9 do kohort z filtrami i 11 innych do lejka.
- **Sprawdzenia:** każdy odnośnik otwarto w nowej karcie wprost z adresu, zapisano stan, odświeżono i porównano. Stan to: zakładka, adres po wczytaniu, wartości wszystkich pól filtrów, podświetlona karta i jej położenie na ekranie. Sprawdzono też zgodność stanu z parametrami odnośnika. Razem 8 251 sprawdzeń. Strona nie zgłosiła żadnego błędu.
- **6 trafień to nie błąd.** Trzy odnośniki z podziałem „Całość” mają w adresie `w=calosc`. Strona zamienia go na `w=__razem&lw=calosc` i pokazuje ten sam, jedyny w tym podziale wiersz „Razem”.

**Zmiana filtra w interfejsie, potem odświeżenie.** To opis stanu rzeczy, a nie błędy.
- Filtry „Kohort” (podział na serie, okno, zawężenia pacjentów) i „Lejka” (podział, „Pokaż dla”, „Kto”) zapisują się w adresie i wracają po odświeżeniu.
- W adresie nie zapisują się: rozdzielczość mapy kohort, filtry „Po zakupie”, filtry „Wyniku biznesu” (grupowanie, poziom i okres ekonomii kampanii), chipy obszarów na osi zdarzeń i filtr pozycji w „Czego nie wiemy”. Po odświeżeniu wracają do ustawień domyślnych, więc takiego widoku nie da się wysłać linkiem.

**Przyciski wstecz i dalej.**
- Między zakładkami działają poprawnie.
- Zmiana filtra nie dodaje kroku w historii (strona podmienia adres), więc „wstecz” po zmianie filtra w lejku prowadzi do poprzedniej zakładki, a „dalej” wraca do lejka już ze zmienionym filtrem.
- Po kliknięciu odnośnika z karty i „wstecz” strona wraca na górę poprzedniej zakładki. Przed kliknięciem była przewinięta o 894 piksele, po powrocie o 0.
- Odnośniki do „Kohort” otwierają zakładkę na górze, z ustawionymi filtrami. Odnośniki do lejka przewijają do wykresu kroków.

## 5. Nic nie jest pobierane z internetu

**Wynik: strona nie wysyła żadnego żądania poza lokalny serwer i nie ma w plikach adresów, fontów, CDN ani skryptów analityki.**

- **Żądania** (nowy skrypt `analiza/f_siec_czas.py`, część 1; wynik `analiza/wyniki/f_siec_czas.txt`): tryb jasny i ciemny, 1 366 i 375 pikseli, przejście przez 9 zakładek i zmiany filtrów (wszystkie podziały lejka, filtry kohort, mapa, „Po zakupie”, „Wynik biznesu”, oś zdarzeń, niewiadome). W każdym wariancie było 23 żądania do 23 różnych plików, razem 92. Wszystkie poszły do 127.0.0.1, żadne nie zostało przerwane i żadne nie dostało statusu błędu. Rodzaje: dokument, skrypt, arkusz stylów. Ikona strony jest wpisana w kod (`data:`), więc nie ma żądania o ikonę.
- **Przeszukanie 27 plików `narzedzie/`** (adresy http i https, fonty, CDN, analityka, `fetch`, `XMLHttpRequest`, `sendBeacon`, `WebSocket`, `import`, `@import`, `preconnect`): 3 trafienia i żadne nie jest żądaniem. Dwa to przestrzeń nazw SVG w `app.js` i `karty.js`, jedno to adres repozytorium w komentarzu licencji biblioteki uPlot. Strona nie korzysta też z pamięci przeglądarki (localStorage, sessionStorage, ciasteczka).

## 6. Czas ładowania

**Wynik: po publikacji strona powinna być gotowa po około 1,5–2 sekundach nawet na wolnym telefonie.** Najcięższa zakładka „Kohorty” dokłada około 2 sekund przy pierwszym otwarciu.

Czas mierzono od otwarcia adresu albo przełączenia zakładki do narysowania jej ostatniego elementu (na przykład wierszy mapy kohort). Każdą zakładkę otwierano po raz pierwszy, po kolei. Przeglądarka miała wyłączoną pamięć podręczną. Ograniczenia ustawiono przez protokół narzędzi deweloperskich: wolne 4G (opóźnienie 150 milisekund, pobieranie 1,6 megabita na sekundę) i procesor 4 razy wolniejszy. Lokalny serwer w wariantach „gzip” kompresuje pliki tak, jak zwykle robi to GitHub Pages. Wariant bez kompresji to górna granica.

| Wariant | „Czy to wzrost” | „Kohorty” | „Lejek” | „Po zakupie” | Pozostałe 5 | Przez sieć razem |
|---|---|---|---|---|---|---|
| Komputer, bez ograniczeń, bez kompresji | 0,2 s (611 KB) | 0,2 s (1 414 KB) | 0,1 s (498 KB) | 0,1 s (306 KB) | do 0,1 s, bez pobierania | 2 829 KB |
| Komputer, bez ograniczeń, gzip | 0,2 s (181 KB) | 0,3 s (308 KB) | 0,1 s (92 KB) | 0,1 s (38 KB) | do 0,1 s | 618 KB |
| Telefon, wolne 4G, procesor 4× wolniej, gzip | **1,6 s** (181 KB) | **2,2 s** (308 KB) | 0,9 s (92 KB) | 0,6 s (38 KB) | 0,1–0,3 s | 618 KB |
| Telefon, wolne 4G, procesor 4× wolniej, bez kompresji | 3,5 s (611 KB) | 7,7 s (1 414 KB) | 3,0 s (498 KB) | 1,9 s (306 KB) | 0,1–0,3 s | 2 829 KB |

- Na telefonie w wariancie z gzip pierwsza karta jest widoczna po 1,6 sekundy (zdarzenie DOMContentLoaded po 1,5 sekundy). Powrót na „Kohorty” z danymi już w pamięci strony trwa 0,4 sekundy.
- **Rozmiar plików strony:** razem 4 496 KB w 27 plikach, w tym `dane_strony/` 4 164 KB. Po kompresji gzip razem 866 KB, z tego dane 766 KB. Największy plik to `kohorty.js`: 1 414 KB, po kompresji 308 KB. Zgodnie z warunkiem z `DECYZJE.md` każdy plik ma mniej niż 25 MB.
- **Ograniczenie pomiaru:** lokalny serwer działa po HTTP/1.1, a GitHub Pages podaje pliki przez sieć CDN po HTTP/2. Wolne 4G to scenariusz ostrożny. Prawdziwe czasy powinny być takie jak w tabeli albo krótsze.

## 7. Publikacja, szerokości pośrednie, Safari i Firefox

**Wynik: plik publikacji i ścieżki są gotowe na GitHub Pages pod podścieżką. Do poprawy jest pasek zakładek na tablecie, a w Safari na telefonie zakładka „Lejek” przesuwa się w bok.**

- **`.github/workflows/pages.yml`** publikuje wyłącznie folder `narzedzie/` (`path: narzedzie`).
  - Uruchamia się przy wypchnięciu gałęzi `master` albo ręcznie. Repozytorium w organizacji musi więc mieć gałąź `master`, inaczej trzeba będzie uruchomić publikację ręcznie.
  - Uprawnienia są minimalne: odczyt treści oraz zapis Pages i tokenu.
  - Akcje są przypięte do skrótów commitów. Wersji akcji nie sprawdzano w sieci, bo tej kontroli nie wolno wychodzić poza 127.0.0.1.
  - W folderze jest `.nojekyll`; opublikuje się też pusty `.gitkeep`, co nie przeszkadza.
- **`robots.txt` i `noindex`:** w `index.html` jest `<meta name="robots" content="noindex, nofollow, noarchive">`, a `narzedzie/robots.txt` zawiera „Disallow: /”. Pod podścieżką projektu (`https://<organizacja>.github.io/<repozytorium>/robots.txt`) wyszukiwarki tego pliku nie czytają, bo biorą `robots.txt` tylko z katalogu głównego domeny. Działa więc znacznik `noindex` w stronie, i to wystarcza.
- **Ścieżki względne:** w plikach strony nie ma żadnej ścieżki bezwzględnej. Nowy skrypt `analiza/f_publikacja.py` (wynik `analiza/wyniki/f_publikacja.txt`) podał folder pod adresem `/b2c-narzedzie/`, a pod `/` zwracał błąd 404, tak jak GitHub Pages. Wyniki:
  - 9 zakładek się narysowało;
  - 18 żądań, wszystkie pod podścieżką, żadnego błędu;
  - 5 odnośników z parametrami otworzyło właściwe zakładki.
- **Szerokości 768 i 1 920 pikseli (Edge):** automatyczna kontrola nie znalazła problemów: bez przewijania w bok, bez błędów, wykresy mieszczą się w kartach. **Zrzut przy 768 pikselach pokazał jednak ucięty pasek zakładek.** Pomiar w szerokościach od 700 do 1 280 pikseli daje taki obraz:
  - do 760 pikseli pasek się zawija i widać wszystkie zakładki;
  - od 761 do 834 pikseli niewidoczne są „Priorytety” i „Czego nie wiemy”;
  - przy 900–960 pikselach niewidoczne jest „Czego nie wiemy”;
  - od 1 000 pikseli widać wszystkie zakładki.

  Pasek ma `overflow-x: auto` i ukryty pasek przewijania (`scrollbar-width: none`), więc nic nie podpowiada, że są dalsze zakładki. Przycisk „Zakładki” działa tylko poniżej 760 pikseli.
- **Safari i Firefox.** Niczego nie instalowano. Silniki WebKit 26.0 (silnik Safari) i Firefox 146.0.1 były już na dysku w pakiecie Playwright.
  - **WebKit, 1 366 pikseli:** bez problemów.
  - **WebKit, 375 pikseli (emulacja telefonu): zakładka „Lejek” ma 478 pikseli szerokości przy ekranie 375 pikseli**, więc stronę da się przesunąć w bok o około 100 pikseli. Pozostałe zakładki są w porządku, a przycisk „Zakładki” działa. Przyczyną jest siatka czterech list wyboru w filtrach lejka: WebKit wlicza do szerokości strony wewnętrzną szerokość listy, choć pola wyglądają dobrze. W Edge i Firefoksie tego nie ma. Wstrzyknięcie stylu w przeglądarce (bez zmiany plików) pokazało, że `.filtry { overflow-x: clip; }` albo `.filtry label { overflow: hidden; }` przywraca 375 pikseli.
  - **Firefox, 1 366 i 375 pikseli:** bez problemów. Firefox z Playwrighta nie emuluje telefonu, więc 375 pikseli to tylko wąskie okno. Firefox z Playwrighta bez ustawionego języka zwraca `navigator.language = "undefined"`. Biblioteka wykresów wtedy się nie wczytuje i zakładka „Kohorty” staje na komunikacie „uPlot is not a constructor”. To artefakt środowiska testowego: z językiem polskim albo angielskim wszystko działa, a prawdziwy Firefox zawsze ma ustawiony język. Dlatego skrypty ustawiają Firefoksowi język `pl-PL`.
  - WebKit na Windowsie rysuje podpisy osi wykresów dziennych czcionką szeryfową, bo nie zna nazwy `system-ui`. Na iPhonie i Macu tej różnicy nie będzie.

## Lista poprawek (od najważniejszej)

**1. Pasek zakładek na tablecie i w wąskim oknie chowa „Priorytety” i „Czego nie wiemy”.** Waga: **przed wysłaniem**.
- **Gdzie:** wszystkie zakładki, pasek w nagłówku, przy szerokości od 761 do około 990 pikseli. Typowe urządzenia to iPad trzymany pionowo (768–834 pikseli) i okno laptopa na pół ekranu. Kod: `narzedzie/styl.css`, reguła `.zakladki` (wiersz 141) i reguła `@media (max-width: 760px)` (wiersze 693–703).
- **Jak odtworzyć:** otworzyć stronę w oknie szerokim na 768 pikseli. Pasek kończy się na „Jakość danych | P”.
- **Propozycja poprawki:** dopisać do `styl.css` regułę `@media (max-width: 1000px) { .zakladki { flex-wrap: wrap; overflow: visible; } }`. Sprawdzone w przeglądarce bez zmiany plików: przy 768, 834, 900, 960 i 999 pikselach widać wszystkie 9 zakładek w dwóch rzędach, a nagłówek ma 174 piksele zamiast 128. Po poprawce trzeba powtórzyć `e_przegladarka.py` w obu trybach i `f_publikacja.py`.
- **Dlaczego ta waga:** w głównej nawigacji na popularnym urządzeniu nie widać dwóch wymaganych elementów zadania: listy priorytetów i tego, czego nie da się rozstrzygnąć. To ta sama zasada co decyzja Kuby dla telefonu: „Kto otworzy link na telefonie, ma od razu zobaczyć kohorty, lejek, priorytety i niewiadome”. Kuba może uznać to za kosmetykę, bo obie zakładki są osiągalne przez przycisk „Dalej” i odnośniki w ostatniej karcie „Czy to wzrost”.

**2. Safari na telefonie: zakładkę „Lejek” da się przesunąć w bok o około 100 pikseli.** Waga: materiał na rozmowę (lejek działa, liczby są dobre).
- **Gdzie:** „Lejek”, 375 pikseli, silnik WebKit; filtry `#lj-filtry`.
- **Jak odtworzyć:** WebKit z Playwrighta, `#lejek`, porównać `document.documentElement.scrollWidth` (478) z szerokością okna (375).
- **Propozycja:** w regule dla telefonu `.filtry { overflow-x: clip; }` albo `.filtry label { overflow: hidden; }`. Sprawdzone w WebKit wstrzyknięciem stylu. Potwierdzić na prawdziwym iPhonie.

**3. Telefon: w tabelach „Kohorty w podziale” i „Kroki lejka w podziale” ucięte są ostatnie cyfry.** Waga: materiał na rozmowę.
- **Gdzie:** „Kohorty” i „Lejek”, 375 pikseli, widok jednej miary. Tabele są o 16 i 20 pikseli szersze od ramki.
- **Jak odtworzyć:** telefon, „Kohorty w podziale”. W kolumnie „Powrót w 90 dniach” widać „17,4% z 18 92”.
- **Propozycja:** w widoku telefonu zawijać „z N” do drugiego wiersza albo zmniejszyć odstępy w komórce, tak żeby tabela mieściła się w 313 pikselach.

**4. Kontrast białych liczb na kolorowych polach.** Waga: materiał na rozmowę.
- **Gdzie:** „Czy to wzrost”, karta „Więcej pacjentów”: 3,2:1 na pomarańczowym i 4,4:1 na niebieskim w trybie jasnym, 3,9:1 i 3,6:1 w ciemnym, przy wymaganych 4,5:1. Mapa kohort, przedział 25–30%: 4,2:1 w trybie jasnym.
- **Propozycja:** ciemny tekst na pomarańczowym albo ciemniejsze kolory tych pól. Te same liczby stoją w tekście karty i w podpowiedzi.

**5. Ucięte podpisy na końcach linii wykresów dziennych.** Waga: materiał na rozmowę.
- **Gdzie:** komputer, na przykład „Marża przed kosztem k…” w „Wyniku biznesu” i „Pozostałe kampanie i …” w „Kohortach”. Pełne nazwy są w legendzie pod wykresem.
- **Propozycja:** krótsze nazwy serii na końcu linii albo szerszy margines.

**6. Dwie nazwy tego samego kroku lejka.** Waga: materiał na rozmowę.
- **Gdzie:** „Lejek”. Wykres kroków mówi „Logowanie albo założenie konta” (pole `etykiety.kroki.k3` w eksporcie), a tabela i pole „Miara” mówią „Logowanie albo konto” (stała `KROKI` w `app.js`).
- **Propozycja:** jedna nazwa w obu miejscach.

**7. Hantle Safari mają dwa różne okresy „po awarii”.** Waga: materiał na rozmowę.
- **Gdzie:** karta Safari w „Lejku” i pozycja 1 w „Priorytetach”. Dla Safari okres po awarii to 17.03–30.09.2026, a dla pozostałych przeglądarek 17.03–15.05.2026. Przypis to opisuje, a liczby zgadzają się z tekstem.
- **Propozycja:** te same okna w obu wierszach.

**8. Odwrotna kolejność kolumn w tabelach powrotu.** Waga: materiał na rozmowę.
- **Gdzie:** w „Czy to wzrost” najpierw rok wcześniej, w nagłówku „Kohort” najpierw ostatnie 12 miesięcy. Hantle w obu kartach idą od roku wcześniej.
- **Propozycja:** jedna kolejność, taka jak na hantlach.

**9. Podpis wiersza TelemediGO na wykresie krótszy niż w tabeli.** Waga: materiał na rozmowę. „Przy kasie z pierwszym zamówieniem” na wykresie, „… zamówieniem pacjenta” w tabeli.

**10. Stan rzeczy w adresie i historii przeglądarki.** Waga: materiał na rozmowę.
- Nie zapisują się w adresie: rozdzielczość mapy kohort, filtry „Po zakupie” i „Wyniku biznesu”, chipy osi zdarzeń, filtr „Czego nie wiemy”.
- „Wstecz” po odnośniku z karty wraca na górę poprzedniej zakładki.
- Odnośniki do „Kohort” nie przewijają do wykresu.
- **Propozycja (na później):** zapisywać te filtry w adresie jak w kohortach i lejku; przy odnośnikach do kohort przewijać do wykresu dzień po dniu.

**11. Ślad pracy i powtarzalność eksportu.** Waga: materiał na rozmowę.
- **Raport C:** `analiza/wyniki/b_eksport_c.txt` w commicie `a4d52c9` był z 11:27 i opisywał starszy `c.js`.
- **Stopka:** strona w commicie pokazuje „stan repozytorium 329d075”; dane się od tego nie zmieniły.
- **Szum zmiennoprzecinkowy:** eksport nie jest bajt w bajt powtarzalny, bo 11 sum przychodu w `jakosc.js` różni się w piętnastej cyfrze.
- **Propozycja:** sesja prowadząca może zacommitować 6 plików odświeżonych tym eksportem razem z poprawkami. Liczby są identyczne, zmienią się tylko godzina i skrót commitu w stopce. Na przyszłość: `b_eksport.py` mógłby zapisywać też `b_eksport_c.txt`, a kwoty w eksporcie można zaokrąglać do groszy.

**12. Skrypt kontroli `analiza/e_przegladarka.py`: zrzut całej strony urywa się na 16 384 pikselach.** Waga: materiał na rozmowę. Dotyczy skryptu kontroli, nie strony.
- **Gdzie:** zrzuty `375_priorytety.png` i `ciemny_375_priorytety.png`. Strona ma tam 24 464 piksele wysokości, a ponad 16 384 pikselami zrzut powtarza górę strony.
- **Jak odtworzyć:** obejrzeć zrzut w okolicy 16 400 pikseli od góry.
- **Propozycja:** dla stron wyższych niż około 16 000 pikseli robić zrzuty okna odcinkami (przewinięcie o wysokość okna i zrzut) zamiast jednego zrzutu całej strony.

Uwaga informacyjna bez poprawki: plik `robots.txt` pod podścieżką projektu nie działa, chroni znacznik `noindex` (punkt 7).

## Czego nie sprawdzono i jak Kuba może to sprawdzić sam

- **Prawdziwy iPhone i iPad (Safari) oraz telefon z Androidem (Chrome).** WebKit z Playwrighta to ten sam silnik co Safari, ale w wersji na Windows: ma inne czcionki, inne pola wyboru i daty oraz inne zachowanie ekranu przy przesuwaniu. Kuba może sprawdzić to sam po publikacji, przed wysłaniem maila, otwierając link na iPhonie i iPadzie:
  - na iPhonie w zakładce „Lejek” spróbować przesunąć stronę palcem w bok (poprawka 2);
  - na iPadzie trzymanym pionowo zobaczyć, czy w pasku widać „Priorytety” i „Czego nie wiemy” (poprawka 1);
  - na telefonie w „Kohortach” zobaczyć tabelę „Kohorty w podziale” (poprawka 3).
- **Prawdziwa sieć GitHub Pages:** czasy zmierzono lokalnie z ograniczeniem sieci. Po publikacji wystarczy otworzyć link na telefonie z wyłączonym Wi-Fi.
- **Wersje akcji w `pages.yml`:** nie sprawdzano ich w sieci, bo ta kontrola nie wychodziła poza 127.0.0.1.

## Pliki tej części

Wszystkie skrypty uruchamia się z głównego folderu przez `python -I`. Tylko czytają pliki strony i zapisują raporty.

| Skrypt | Co robi | Wynik |
|---|---|---|
| `analiza/f_eksport_powtarzalnosc.py` | pliki danych strony na dysku wobec commitu, wartość po wartości (metadane, szum zmiennoprzecinkowy, treść) | `wyniki/f_eksport_powtarzalnosc.txt` |
| `analiza/f_wykresy_tekst.py [--silnik msedge\|webkit\|firefox]` | liczby na wykresach wobec tekstu i tabel tej samej karty, odczyt z DOM, 1 366 i 375 pikseli, około 1 minuty | `wyniki/f_wykresy_tekst.txt`, `_webkit.txt`, `_firefox.txt` (każdy około 0,57 MB, bo zawiera wszystkie porównania) |
| `analiza/f_kontrast.py` | kontrast tekstów i elementów wykresów w trybie jasnym i ciemnym, teksty ucięte, tabele bez przewijania, przewijanie w bok | `wyniki/f_kontrast.txt` |
| `analiza/f_odnosniki.py` | odnośniki z parametrami: otwarcie wprost, odświeżenie, zmiana filtra, wstecz i dalej, około 8 minut | `wyniki/f_odnosniki.txt` |
| `analiza/f_siec_czas.py` | żądania sieciowe, przeszukanie plików, czas ładowania z ograniczeniem sieci i procesora, rozmiar plików, około 2,5 minuty | `wyniki/f_siec_czas.txt` |
| `analiza/f_publikacja.py --zrzuty <katalog>` | podścieżka jak na GitHub Pages, 768 i 1 920 pikseli, WebKit i Firefox | `wyniki/f_publikacja.txt` i zrzuty |

Zrzuty ekranu i skrypty pomocnicze (cięcie zrzutów, diagnoza Firefoksa i WebKit, próby poprawek stylem) zostały w katalogu tymczasowym sesji, poza repozytorium.

## Propozycje wpisów do wspólnych notatek (bez numerów; numery nada sesja prowadząca)

- **`analiza/README.md`**, nowe wiersze „F”: sześć skryptów z tabeli wyżej, z opisem i wynikiem.
- **`ZNALEZISKA.md`**, sekcja „Ostatnia kontrola techniczna (2026-10-23)”:
  - pasek zakładek przy 761–990 pikselach chowa „Priorytety” i „Czego nie wiemy”;
  - w Safari (WebKit) na telefonie zakładka „Lejek” ma 478 pikseli szerokości przez filtry z listami wyboru;
  - tabele kohort i lejka w widoku telefonu są o 16 i 20 pikseli za szerokie;
  - białe liczby na kolorowych słupkach mają kontrast 3,2–4,4:1;
  - eksport nie jest bajt w bajt powtarzalny (11 sum w `jakosc.js` różni się w piętnastej cyfrze), a `b_eksport_c.txt` w commicie był nieaktualny;
  - Firefox z Playwrighta bez ustawionego języka nie wczytuje biblioteki wykresów, co jest artefaktem testu.
- **`DECYZJE.md`**: do decyzji Kuby, czy pasek zakładek na tablecie (pozycja 1) poprawiamy przed wysłaniem, i które sprawy z pozycji 2–12 bierzemy.
- **`PRZEKAZANIE.md`**: „Stan po części 2 ostatniej kontroli (kontrola techniczna, 2026-10-23)”. Treść: eksport 115 kontroli bez różnic; wykresy wobec tekstu 1 956 porównań na silnik w Edge, WebKit i Firefoksie bez niezgodności; 305 odnośników z filtrami działa po odświeżeniu; żadnych żądań poza 127.0.0.1; pierwsza zakładka po 1,6 sekundy na wolnym 4G. Jeden problem przed wysłaniem (pasek zakładek na tablecie), reszta to materiał na rozmowę. Raport w `notatki/f_techniczna.md`. Po każdej poprawce strony powtórzyć `e_przegladarka.py` (oba tryby), `f_wykresy_tekst.py` i `f_publikacja.py`. Zakładki wyższej niż 16 384 piksele (na telefonie „Priorytety”) nie oglądać na jednym zrzucie całej strony, tylko odcinkami.
