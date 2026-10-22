# E — część 3: wygląd narzędzia (sesja „E: nowy wygląd narzędzia”, 2026-10-21/22)

**Zlecenie:** część 3 listy Kuby z `notatki/e_runda.md` (słowa Kuby, punkt 1), równolegle z sesją prowadzącą (`local_1bf06826`), która robi część 1 (merytoryka) i część 2 (teksty). Podział plików: `e_runda.md`, punkt 2. Ta sesja nie zmieniała danych strony (`narzedzie/dane_strony/`), eksportu ani wspólnych notatek.

## 1. Lista Kuby, punkt po punkcie

| Punkt z listy Kuby | Co jest na stronie |
|---|---|
| Ciemnogranatowy pasek z nazwą i zakładkami | Pasek na całą szerokość: nazwa, podtytuł i uwaga o danych syntetycznych w pierwszym wierszu, zakładki w drugim. Aktywna zakładka ma jasnoniebieskie podkreślenie. Na komputerze pasek jest przyklejony do góry. Na telefonie zakładki zawijają się w kilka rzędów przycisków (wszystkie widać od razu), a pasek nie jest przyklejony, żeby nie zabierał ekranu. |
| Białe karty z delikatnym cieniem na jasnoszarym tle | Tło `#eef1f5`, karty białe z cienką ramką i miękkim cieniem. Karty wewnątrz kart (kafelki, pasek priorytetu, zastrzeżenie) mają szare tło zamiast cienia. |
| Jeden kolor do odnośników i wyborów | Niebieski `#1f5fcc`: odnośniki, pola wyboru (checkboxy), obramowanie wybranych pól, zaznaczone wiersze tabel (jasnoniebieskie tło), wybrane tory na osi zdarzeń. |
| Bez kolorowych pasków po lewej stronie kart | Usunięte: pasek przy karcie „W skrócie”, czerwony pasek kart napraw w lejku i kolorowy pasek zaznaczonych wierszy tabel (zostaje kolorowa kropka serii i jasnoniebieskie tło wiersza). |
| Kolory stanu zawsze z ikoną SVG i słowem, bez znaków typu ▲ | Znacznik stanu (`karty.js`, funkcja `znacznik`): pigułka z ikoną SVG i słowem, kolor według stanu (dobrze: zielony i „ptaszek”, źle: czerwony i „krzyżyk”, uwaga: bursztynowy i trójkąt, neutralnie: szary i kreska). Wszystkie znaki ▲ ▼ ↑ zniknęły z kodu strony. W tabeli ekonomii kampanii dawny czerwony napis „niepewny: znak zależy od reguły” jest znacznikiem „uwaga” z ikoną i słowem. |
| „Czy to wzrost”: werdykt ze znacznikiem „Nie”, trzy kafelki, ponumerowane decyzje prowadzące do priorytetów; karty „Więcej pacjentów” i „Lepsza retencja” ze znacznikami „Tak” i „Nie” | Karta werdyktu: duży znacznik z danych, obok werdykt i dopisek. Pod spodem trzy kafelki (duża liczba, etykieta zmiany ze strzałką, jedna linijka podpisu, szary dopisek). Niżej „Decyzje na pierwszy tydzień”: numer w kółku i decyzja jako odnośnik do karty priorytetu, pod nią dopisek. Dwie pierwsze karty stoją obok siebie (na telefonie jedna pod drugą). Gdy karta ma krótką etykietę (`etykieta`, np. „Więcej pacjentów”), etykieta i znacznik „Tak”/„Nie” stoją w wierszu nad tytułem-wnioskiem. |
| Lejek: wykres kroków od wejścia do płatności | Nowa karta „Kroki lejka” nad tabelą (szczegóły w punkcie 3). |
| Lejek domyślnie dla osób, które jeszcze nie kupowały | Pole „Kto” stoi pierwsze w panelu i ma domyślnie „Jeszcze nie kupowali”, także gdy odnośnik nie podaje tego pola (punkt 5). |
| Priorytety: pewność jako kolorowe znaczniki (Wysoka, Średnia, Niska, Test), wyróżniona kwota, w karcie pasek „Ile warte · Pewność · Wdrożenie” | Przegląd: kwota pogrubiona i większa, pod nią szary dopisek; pewność jako znacznik (Wysoka: zielony z „ptaszkiem”, Średnia: bursztynowy z półpełnym kółkiem, Niska: czerwony z wykrzyknikiem, Test: fioletowy z kolbą), pod nim dopisek. W karcie pozycji pod tytułem i wnioskiem pasek z trzema polami: „Ile warte rocznie (marża)”, „Pewność”, „Wdrożenie”. |
| Zmiany rok do roku jako małe zielone albo czerwone etykiety ze strzałką | Etykieta zmiany (`karty.js`, funkcja `zmiana`): strzałka SVG w górę, w dół albo w bok, wartość ze znakiem, tło zielone (lepiej), czerwone (gorzej), bursztynowe (uwaga) albo szare. Dla czytników ekranu etykieta ma też słowo „lepiej” albo „gorzej”, a po najechaniu podpowiedź „Wzrost o …”. Używają jej tabele lejka, kohort, po zakupie, kwartałów w wyniku biznesu, wykrytych zmian na osi zdarzeń i tabele z danych. |
| Filtry w jednym panelu nad treścią | Lejek i kohorty: jeden biały panel z podpisem, na co działa („Filtry: kroki lejka, tabela i wykres dzień po dniu”), pod nagłówkiem zakładki, nad wykresami i tabelami. Oś zdarzeń: wybór torów w tym samym panelu. W „Po zakupie” i „Wyniku biznesu” każda karta ma własne, inne filtry, więc stoją w szarym pasku na górze swojej karty (połączenie ich w jeden panel zmieniłoby znaczenie: filtr specjalizacji wykresu punktualności nie dotyczy zwrotów). Miara i wygładzenie wykresu dzień po dniu zostają w nagłówku wykresu, którego dotyczą. |
| Telefon działa tak samo dobrze | Zakładki zawijane, kafelki jeden pod drugim, pasek priorytetu w trzech wierszach, tabele przeglądu priorytetów i niewiadomych jako karty z podpisem przy każdym polu, szerokie tabele przewijają się wewnątrz swojej ramki. Wykres kroków lejka na telefonie: nazwa kroku i wartość nad paskiem. Żadna zakładka nie przewija się w bok przy 375 px (punkt 6). |

**Teksty statyczne** (nagłówki, podpisy filtrów, przypisy w `index.html` i w kodzie), według zasad części 2, bez nowych liczb:
- „okres 1 / okres 2” → „ostatnie 12 miesięcy / rok wcześniej” w nazwach wyboru porównania, w tabeli „Miesiące i sumy obu lat”, w wyborze okresu ekonomii kampanii, w podpisie mostka i w tabeli retencji (stary kształt danych). „Okres A / okres B” zostały tam, gdzie wybiera się własne daty;
- opisy metody („jak liczymy”) przeniesione do zwijanych sekcji „Jak liczymy” / „Jak czytać” pod kartami i na dole zakładek; widoczne zostaje jedno zdanie o tym, jak czytać tabelę albo wykres;
- skrócony podtytuł strony (bez wyliczanki);
- „↑ Wróć do przeglądu” → „Wróć do przeglądu”.

## 2. Kontrakt danych: co rysuje strona

- **Ogólna karta** (`narzedzie/karty.js`, nowy plik): `tytul`, `znacznik`, `wniosek`, `tresc` (bloki `akapit`, `punkty`, `numerowane`, `podtytul`, `liczba`, `tabela`), `wstaw`, `zastrzezenie` (szare pole z ikoną i słowem „Zastrzeżenie:”), `linki` („Zobacz w danych:”), `szczegoly` i `zrodlo` (zwinięte „Szczegóły”, na końcu „Skąd liczby: …”). Kolejne bloki `liczba` stają w jednym rzędzie kafelków. Komórka tabeli z polem `zmiana` to etykieta zmiany, z polem `stan` (bez `zmiana`) — znacznik stanu, z polem `pod` — druga, szara linia.
- **Karta wpisana w istniejącą kartę strony** (po zakupie, wynik biznesu, jakość danych, kohorty, nagłówek lejka): tytuł z danych zastępuje statyczny nagłówek, wniosek, treść, zastrzeżenie i odnośniki stoją nad filtrami, wykresem i tabelą, a „Szczegóły” na końcu karty. Statyczne przypisy oznaczone w `index.html` klasą `zastap` (np. opis mostka, przypis tabeli godzin) chowają się, gdy przychodzi karta.
- **Klucze:** dokładnie według tabeli kluczy w `e_runda.md` (uzupełnienie sesji prowadzącej z 2026-10-21 wieczorem): `lejek_naglowek.karta`, `.naprawy_karty`, `.osobne_karta`; `kohorty.karta`; `po_zakupie.karty.{punktualnosc, godziny, ruch, powrot, zwroty, oceny}`; `wynik.karta`, `wynik.ekonomia.karta`; `jakosc.karty.{mostek, duplikaty, testy, godzina, drobne, czyste}` i `jakosc.karta` (wstęp); `zdarzenia.karta` (wstęp). Karty wstępu (`jakosc.karta`, `zdarzenia.karta`) stają pod nagłówkiem zakładki zamiast akapitu wstępu. W „Czy to wzrost” `"wstaw": "mostek"` wstawia tabelę mostka; w jakości danych ta sama wartość wskazuje istniejącą tabelę mostka (bez drugiej kopii).
- **„Czy to wzrost”, „Priorytety”, „Czego nie wiemy”:** kształty z punktów 3.2–3.4 i uzupełnienia sesji prowadzącej: `dopisek` przy werdykcie, kafelku i decyzji oraz `etykieta` karty. Nowy kształt rozpoznaje `werdykt` jako obiekt z listą `karty`; w „Priorytetach” każde pole osobno (`pasek`, `wniosek`, `szczegoly`, `zasady` i `nie_robimy` jako karty, `pewnosc` jako obiekt albo dotychczasowy napis).
- **Krótkie nazwy zdarzeń** (`krotko`, prośba sesji prowadzącej): w liście porównań „60 dni przed i po: …” (lejek, kohorty), w legendzie zdarzeń pod wykresem lejka i w podpowiedzi kolumny „Zdarzenia” macierzy kohort strona bierze `krotko`, a gdy go nie ma — `tytul`. Pełny tytuł zostaje na osi zdarzeń i w kartach zdarzeń.
- **„Po zakupie”, karta powrotu:** statyczne zdanie z wnioskiem („Rano spada powrót po wizytach spóźnionych…”) zastąpione neutralnym opisem tabeli; wniosek przychodzi z danych (`po_zakupie.karty.powrot`).
- **Stary kształt dalej działa:** gdy w danych nie ma karty, strona rysuje dotychczasowe zdania, w nowym wyglądzie (znaczniki, etykiety zmiany, kafelki). W dotychczasowym kształcie pewność przychodzi jako napis („wysoka: …”, „— (to jest test)”); strona czyta z niego poziom znacznika, a resztę pokazuje jako dopisek.

## 3. Wykres kroków lejka

- **Co pokazuje:** dla każdego kroku (wejście na stronę, wybór usługi, wybór terminu, logowanie albo konto, wejście na płatność, płatność przyjęta) pasek z odsetkiem sesji okresu B, które do niego doszły, i pionową kreskę z tym samym odsetkiem w okresie A. Przy kroku: liczba sesji w okresie B i oba odsetki. Między krokami: jaka część sesji z poprzedniego kroku przechodzi dalej, ta sama wartość w okresie A i etykieta zmiany w punktach procentowych.
- **Wyróżnione przejście:** to, które ma największy **względny** spadek (iloraz „przechodzi dalej” B / A najmniejszy i poniżej 1). Dlaczego względny, a nie w punktach: odsetek sesji z płatnością to iloczyn przejść, więc to przejście najbardziej obniża końcowy wynik. Przejście ma czerwone tło i znacznik „Największy spadek” z ikoną. Gdy żadne przejście się nie pogorszyło, nic nie jest wyróżnione. Uzasadnienie stoi na stronie w „Jak czytać”. **Propozycja do `ZALOZENIA.md` (numer nadaje sesja prowadząca):** „Na wykresie kroków lejka wyróżnione jest przejście z największym względnym spadkiem odsetka przechodzących dalej (B / A), bo ono najbardziej obniża odsetek sesji zakończonych płatnością”.
- **Skąd liczby:** liczone w przeglądarce z tych samych danych lejka co tabela (`dane_strony/lejek_<podział>.js`), dla bieżących filtrów: Kto, typ sesji, podział, okresy A i B. Wybór „Pokaż dla” pozwala obejrzeć jedną wartość podziału (np. Safari na iOS); domyślnie „Razem”. Odnośnik, który wskazuje jedną wartość (`w=iOS Safari`), od razu pokazuje jej lejek; wybór trafia do adresu jako `lw`. Kroki, których dany typ sesji nie ma (np. zakup samego TelemediGO zaczyna się od płatności), są pominięte.
- **Nazwy okresów** idą za wyborem porównania: „ostatnie 12 miesięcy / rok wcześniej”, „ostatnie 30 dni / te same dni rok wcześniej”, „ostatnie 90 dni / poprzednie 90 dni”, „po zdarzeniu / przed zdarzeniem”, a przy własnych datach „okres B / okres A”.

## 4. Decyzje projektowe

- **Kolory:** tokeny w `styl.css` (granat paska `#13213a`, tło `#eef1f5`, karty białe, akcent `#1f5fcc`, cztery stany i fiolet „Test” dla pewności). Kolory serii wykresów bez zmian (paleta sprawdzona pod kątem daltonizmu). Tryb ciemny zachowany, z własnymi wartościami tokenów.
- **Czcionki:** tylko systemowe (Segoe UI Variable na Windowsie, systemowe na innych), cyfry o stałej szerokości w tabelach i kafelkach. Strona dalej nie pobiera niczego z sieci.
- **Etykieta zmiany** ma strzałkę, wartość i kolor; słowo „lepiej”/„gorzej” jest dla czytników ekranu i w podpowiedzi, a nie widoczne przy każdej komórce (tabele lejka i kohort mają dziesiątki etykiet). Kafelki w „Czy to wzrost” pokazują słowo wprost.
- **Wartości ujemne** w tabelach kampanii są czerwone, ale zawsze ze znakiem minus, więc kolor nie jest jedynym nośnikiem.
- **Wykresy dzień po dniu:** pionowe linie zdarzeń są jaśniejsze i przerywane, żeby nie zasłaniały serii; numery zdarzeń bez zmian.
- **Ukryte słowo dla czytników ekranu** jest pozycjonowane względem etykiety (błąd złapany testem: bez tego strona przewijała się w bok o szerokość najszerszej tabeli).

## 5. Odnośniki do lejka a domyślne „Kto”

Zmiana domyślnego „Kto” na „Jeszcze nie kupowali” zmienia znaczenie tylko tych odnośników do lejka, które nie podają pola `pac`. Stan danych na dysku 2026-10-22 (po commicie `88c114a` sesji prowadzącej): **każdy odnośnik do lejka w danych podaje `pac` jawnie** (`nie_kupowal` albo `wszyscy`), także odnośnik do sesji zalogowanych od wejścia, w których pole „Kto” i tak nie działa. W wersji sprzed rundy (`b645ef9`) jedyny odnośnik bez `pac` to `#lejek?typ=zalogowana_od_wejscia&podz=calosc&krok=k1` w `c.js` — dla tego typu sesji pole „Kto” nie działa, więc znaczenie się nie zmieniało. Odnośniki budowane przez stronę (tabela wykrytych zmian na osi zdarzeń, adres zapisywany przy zmianie filtrów) podają `pac` jawnie. Odnośnik z zakładki „Lejek” w pasku (bez ustawień) otwiera lejek osób, które jeszcze nie kupowały — tak jak chciał Kuba.

## 6. Jak sprawdzone

`python -I analiza/e_przegladarka.py --wyjscie <katalog tymczasowy> [--dane-z-gita <commit>] [--przyklad]` — Edge bez okna przez Playwright, tylko 127.0.0.1, serwer z folderu `narzedzie/`. Sprawdza 9 zakładek przy 1366 i 375 px (czy się rysują, konsola, przewijanie w bok, zrzut każdej zakładki), wszystkie odnośniki `#…` między zakładkami (czy otwierają właściwą zakładkę i podświetlają kartę pozycji albo zdarzenia) oraz lejek (domyślne „Kto”, wykres kroków, reakcja na filtr). Pliki danych na dysku się nie zmieniają: `--dane-z-gita` podaje przeglądarce pliki `dane_strony/` z commitu, a `--przyklad` dopisuje do nich na końcu mechaniczne przekształcenie do nowego kształtu (i usuwa stare pola, żeby strona nie mogła z nich skorzystać).

Wyniki (2026-10-22, po ostatnich poprawkach), trzy przebiegi:

| Dane | 9 zakładek przy 1366 px i 375 px | Przewijanie w bok | Błędy w konsoli | Odnośniki między zakładkami | Lejek |
|---|---|---|---|---|---|
| na dysku (nowy kształt sesji prowadzącej, po `88c114a`) | rysują się | brak | 0 | 296, wszystkie działają | „Kto” = jeszcze nie kupowali, 6 kroków, 1 wyróżnione przejście, reaguje na filtr |
| z commitu `b645ef9` (stary kształt, sprzed rundy) | rysują się | brak | 0 | 295, wszystkie działają | jak wyżej |
| `b645ef9` przekształcone do nowego kształtu (`--przyklad`) | rysują się | brak | 0 | 295, wszystkie działają | jak wyżej |

Obejrzane zrzuty (komputer i telefon): „Czy to wzrost” (werdykt, kafelki, decyzje, karty ze znacznikami), lejek (karta nagłówka, karty napraw, panel filtrów, wykres kroków dla całości i dla Safari na iOS przed awarią i po niej), priorytety (przegląd i karty z paskiem), po zakupie, jakość danych; „Czy to wzrost”, wykres kroków, po zakupie i jakość danych także w trybie ciemnym. Pierwszy przebieg złapał dwa błędy, poprawione: przewijanie w bok przez ukryte słowo dla czytników ekranu i zbyt długie, niezawijane dopiski przy decyzjach na telefonie. Z oglądania zrzutów: odmiana w tytule wykresu kroków („wobec roku wcześniej”), za szeroka lista „Porównanie” w panelu filtrów, wartość kroku pod paskiem zamiast obok nazwy na telefonie, podwójne słowo w kafelkach — poprawione.

`analiza/b2_teksty_strony.py` rozumie nowe elementy (nagłówek karty ze znacznikiem i etykietą, werdykt, kafelki, decyzje, odnośniki, pasek priorytetu, wykres kroków lejka) i ma opcjonalne `--wyjscie <plik>`, żeby nie nadpisywać `analiza/wyniki/b_teksty_strony.md` (to plik sesji prowadzącej). Przebieg 2026-10-22 do pliku tymczasowego: 9 zakładek, 0 błędów w konsoli; plik w `analiza/wyniki/` nie został nadpisany.

## 7. Co zostaje do integracji

- Sesja prowadząca: odtworzyć teksty strony (`python -I analiza/b2_teksty_strony.py`) po ostatnim eksporcie i przejrzeć je w przeglądarce razem z sesją wyglądu (komputer i telefon).
- Gdyby eksport dodał nowe wartości `wstaw` albo nowe miejsca na karty, strona ich nie narysuje, dopóki sesja wyglądu ich nie obsłuży (nieznane `wstaw` jest pomijane bez błędu).
- Propozycja do `DECYZJE.md`: wygląd narzędzia według części 3 listy Kuby (punkt 1 tej notatki); wykres kroków lejka z wyróżnieniem przejścia o największym względnym spadku; filtry „Po zakupie” i „Wyniku biznesu” w paskach swoich kart, bo każda karta ma inne filtry.

## 8. Pliki

- Nowe: `narzedzie/karty.js`, `analiza/e_przegladarka.py`, ta notatka.
- Zmienione: `narzedzie/index.html`, `narzedzie/styl.css`, `narzedzie/app.js`, `narzedzie/widoki.js`, `narzedzie/widoki_c.js`, `analiza/b2_teksty_strony.py`.

## 9. Druga lista Kuby po przeglądzie wersji `ccc3c61` (2026-10-22)

**Zlecenie:** Kuba przysłał do tej sesji listę 15 poprawek (merytoryka w tekstach, język, README), „wszystko w jednym przejściu, razem z poprzednią wiadomością”, potem kontrola liczb, odtworzenie tekstów strony i zatrzymanie u niego. Sesja prowadząca na ten czas nie zmieniała plików (potwierdziła wiadomością).

**Podział:** teksty z danych, szkice i README poprawił agent w tle tej sesji. Jego pliki: `analiza/e_teksty.py`, `analiza/e_teksty_zakladki.py`, `analiza/b2_eksport_c.py`, `analiza/b_eksport.py`, nowy `analiza/e_poprawki.py` (wyniki `analiza/wyniki/e_poprawki.txt`, `.json`), `notatki/e_teksty.md`, `notatki/e_teksty_zakladki.md`, `README.md`, `analiza/README.md`, recenzja `notatki/recenzje/e2_codex*.md` i eksport do `narzedzie/dane_strony/`. Kod strony poprawiła ta sesja.

**Kod strony (ta sesja):**
- „Po zakupie” i „Wynik biznesu” (tam nie wybiera się dat): zamiast „A: …” i „okres B = … (A = …)” stoi „rok wcześniej: …” i „ostatnie 12 miesięcy (…), pod spodem rok wcześniej” (punkt 8 Kuby);
- jedna para nazw reguły w filtrach, nagłówkach tabel i przypisach: „według pierwszego wejścia” i „według sesji z płatnością” (punkt 9);
- tabela powrotu według opóźnienia pierwszej wizyty: porównania z rokiem wcześniej szare, bez oceny „lepiej/gorzej” (punkt 5, ostatni myślnik);
- statyczne definicje w „Po zakupie” chowają się, gdy przychodzą karty z danych, bo definicje są w ich szczegółach (punkt 11);
- napis zwijanej sekcji pod nagłówkiem lejka to tytuł-wniosek karty `osobne_karta` (punkt 14);
- etykieta „Zastrzeżenie” stoi w osobnym wierszu, bez dwukropka; wcześniej doklejona etykieta z dwukropkiem dawała podwójne dwukropki (punkt 12).

**Teksty z danych (agent):** wszystkie punkty 1–15. Najważniejsze: oba warianty naprawy zwrotów nazwane słowami („po samej nowej kreacji”, „po zmianie zasad zwrotów”) w tabelach pozycji 3 i 9, a w pozycji 9 oba progi (dziś 85%, po samej nowej kreacji 79%, po zmianie zasad 70%); kryterium kolejności listy zgodne z miejscem pozycji 9; w lejku „ile płacą dziś” (kwiecień–wrzesień 2026: około 8% wobec 11% w tych samych miesiącach rok wcześniej; nowa liczba z `e_poprawki.py`); Safari „do naprawy”, przeglądarki w aplikacjach „do sprawdzenia”, z nazwanymi kampaniami zamiast „osób, które znają stronę”; jedna wersja liczb (Safari 66% → 46%, poranne opóźnienia, blok 5:00–13:59, jedna lista na pierwszy tydzień w „Czy to wzrost”, w zasadach priorytetów i w README). Pełny raport punkt po punkcie: odpowiedź agenta, streszczona w raporcie dla Kuby.

**Kontrola (2026-10-22):**
- `python -I analiza/b_eksport.py`: 0 różnic w 104 kontrolach; liczby bez pokrycia w szkicach: 0 (C: 1 176 liczb, D: 247, E: 1 292 i 1 271);
- Codex (Sol, `-p review`): 9 z 9 nowych liczb zgodnych, przeliczone jego kodem (`notatki/recenzje/e2_codex.md`, odpowiedź `e2_codex_odpowiedz.md`);
- `python -I analiza/b2_teksty_strony.py`: teksty odtworzone, 9 zakładek, 0 błędów w konsoli;
- `python -I analiza/e_przegladarka.py`: 9 zakładek przy 1366 i 375 px, 0 błędów, bez przewijania w bok, 296 odnośników działa;
- w odtworzonych tekstach nie ma już: „wariant A/B”, „przyjęta reguła” w żadnej odmianie, „reguła porównawcza”, „pacjentów dodatkowych”, „co do znaku”, „co do kwoty”, „oszacowanie punktowe”, „sesja płatności”, technicznej nazwy kampanii w tytule tabeli; „, a nie” zostało tylko przy TelemediGO i przy porównaniu z dashboardem; litery okresów A/B tylko w kohortach i lejku, gdzie wybiera się daty.

**Uwagi agenta, które warto znać:**
- w kodzie tekstów było kilka liczb wpisanych ręcznie (przechodziły kontrolę, bo stały też w szkicach); teraz liczy je kod. Wniosek: sama zgodność ze szkicem nie wyłapuje liczb wpisanych ręcznie;
- samodzielne uruchomienie `b2_eksport_c.py` wywracało się na imporcie `e_teksty` pod `python -I`; naprawione;
- szkice `e_teksty*.md` i `README.md` mają końce linii LF (zachowane), `analiza/README.md` CRLF;
- w `podsumowanie.js` zostało dawne pole `naprawy`; strona go nie rysuje.

**Propozycje wpisów do wspólnych notatek (scala sesja prowadząca; numery od 71):**
- `ZALOZENIA.md`: 71 — „ile płacą dziś” w lejku to miesiące IV–IX 2026 wobec IV–IX 2025, średnia roczna tylko w szczegółach; 72 — jedna para nazw reguły („według pierwszego wejścia”, „według sesji z płatnością”), definicje bez zmian; 73 — warianty naprawy zwrotów nazwane słowami („po samej nowej kreacji”, „po zmianie zasad zwrotów”), oba w tabelach i progach; 74 — kryterium kolejności listy: najpierw pewne straty (1–2) i pauzy (3–4), potem działania z wyceną (5–10, w tym test Mety o nieznanym znaku i największej stawce), na końcu pozycje bez oszacowanego efektu (11 i 12); 75 — jedna wersja porannych opóźnień (pacjenci spoza nowych kampanii, miesiąc terminu) i blok 5:00–13:59; 76 — Safari 66% → 46% (1.10.2025–16.03.2026 wobec 17.03–30.09.2026), okna 60 dni w szczegółach; 77 — jedna lista na pierwszy tydzień;
- `DECYZJE.md`: druga lista Kuby zrobiona w jednym przejściu w sesji wyglądu (teksty: agent tej sesji, kod strony: ta sesja); przeglądarki w aplikacjach „do sprawdzenia”, bez pozycji na liście priorytetów; reguła decyzji testu Mety zostaje, z dopisanym ryzykiem (uwaga Codeksa przyjęta częściowo);
- `e_runda.md` (postęp) i `PRZEKAZANIE.md`: kontrole 0/104, Codex 9/9, naprawiony samodzielny eksport `b2_eksport_c.py`, lekcja o liczbach wpisanych ręcznie; następny krok: przegląd Kuby;
- `ZNALEZISKA.md`: w danych nic nowego.
