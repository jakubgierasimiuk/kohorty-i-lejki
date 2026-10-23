# F — runda poprawek, część strony (sesja A, 2026-10-23)

**Zlecenie:** sesja prowadząca `local_e4232e55`, na podstawie decyzji Kuby z 23.10.2026 („tak, wszystko według rekomendacji, ruszaj z dwiema sesjami”) i propozycji `notatki/f_propozycja.md`. Ta sesja robi poprawki 3, 4, 1, 5 oraz 6a, 6b i 6c, w tej kolejności. Poprawkę 2 (ślad pracy) robi równolegle sesja B.

## Puenta

**Wszystkie siedem poprawek strony jest zrobionych, a liczby na stronie się nie zmieniły.** Nowa pierwsza karta „Kohort” pokazuje osiem zdarzeń i decyzji z osi: kiedy, co się stało, kogo dotyczy, co zmieniło się po nim, ile to jest warte, z jaką pewnością i co z tym robimy. Każda liczba w tabeli pochodzi z tych samych pól eksportu co karty zdarzeń, przegląd listy priorytetów i ekonomia kampanii. Skrypt kontroli porównuje każdą komórkę z tą samą liczbą w karcie źródłowej.

Wyniki kontroli w liczbach są w punkcie „Kontrola”. Propozycje wpisów do wspólnych notatek są na końcu.

## Co zrobione

### Poprawka 3. Sześć zdań na pierwszej zakładce

1. „Z kanałów bezpłatnych … przybyło 12% nowych pacjentów” → „Nowych pacjentów z kanałów bezpłatnych (…) jest o 12% więcej niż rok wcześniej” (P1).
2. Zastrzeżenie o III kwartale nazywa marżę: „Marża po koszcie lekarza, kampaniach i prowizji spadła w III kwartale 2026 o 7% rok do roku, ale ten spadek zależy od jednorazowego zdarzenia…”. To samo w „Wyniku biznesu” (P3). W kodzie doszła kontrola, że marża rzeczywiście spadła, a po korekcie jest wyższa.
3. Decyzja na pierwszy tydzień: „według obu reguł przypisania źródła (pierwsze wejście i sesja z płatnością)”.
4. Karta „Lepsza retencja”: zastrzeżenie „Te liczby opisują zmianę, ale nie wskazują jej przyczyny. Nie wiemy, dlaczego spada powrót w kanałach działających w obu latach: czy ci sami pacjenci zachowują się dziś gorzej, czy zmieniło się to, kto do nas trafia.” Zastrzeżenie dotyczy teraz reszty spadku, więc nie przeczy zdaniu o 71% spadku przypadającym na większy udział nowych kampanii.
5. „Awaria Safari trwała 198 dni bez alarmu” → „… trwała 198 dni, do końca danych” w decyzji na pierwszy tydzień i w dwóch miejscach pozycji 2 („Dlaczego” i „Ile warta” w szczegółach).
6. Kolejność decyzji na pierwszy tydzień jak na liście priorytetów: 1 (Safari), 2 (raport i alarmy), 3 (TikTok i Google Ads na specjalistów, pozycje 3 i 4), 4 (sprawdzenia). Zdanie w zasadach listy („pozycje 1, 3 i 4 oraz pierwsze kroki pozycji 2, 5, 6, 8 i 11”) zostaje, bo mówi, co da się zrobić równolegle, a nie w jakiej kolejności.

Pliki: `analiza/e_teksty.py`, `analiza/e_teksty_zakladki.py`, `analiza/b2_eksport_c.py`; szkice `notatki/e_teksty.md`, `notatki/e_teksty_zakladki.md`.

### Poprawka 4. Dziesięć poprawek z kontroli języka (P2, P4–P12)

- **P2:** blok poranny na wykresach godzin i w tabeli godzin obejmuje 5:00–13:59 (pole `blok` w eksporcie, `analiza/b2_eksport_c.py`). Przy godzinie 13:00 doszło „; blok poranny” w podpowiedzi.
- **P4:** pierwszy punkt nagłówka „Lejka”: ruchu z nowych kampanii przybywało już od listopada 2025, a w lutym 2026 przekroczył 30% sesji nowych osób. Kod sprawdza oba twierdzenia na danych miesięcy (10,1%, 18,4%, 24,2%, 31,8%).
- **P5:** przypis wykresu udziału nowych kampanii w „Lejku” (`narzedzie/app.js`).
- **P6:** „W III kwartale 2026 powtórne zamówienie pacjenta spoza nowych kampanii…” w „Wyniku biznesu”.
- **P7:** „Kohorty dzienne mają po kilkadziesiąt pacjentów” zamiast „około 40” (`narzedzie/index.html`).
- **P8:** „sprzedaż sprzedała” poprawione w dwóch wskazanych miejscach („Czy to wzrost”, karta kwartałów, i „Wynik biznesu”). **Poza listą:** ten sam błąd stał w trzecim miejscu, w szczegółach karty TelemediGO na pierwszej zakładce („a sprzedała w nich 225 członkostw … sprzedaje średnio 38 miesięcznie”); poprawione tak samo („pacjenci kupili w tym czasie 225 członkostw … kupują w niej średnio 38 członkostw miesięcznie”), w kodzie (`b2_eksport_c.py`) i w szkicu `notatki/c_szkic.md`. Liczby bez zmian.
- **P9:** „reguła przypisania” zamiast „podział” w znaczeniu reguły: zamiany w `REGULY` i 6 zdań w `e_teksty.py`, 4 zdania w `e_teksty_zakladki.py`, szkice. W zrzucie tekstów strony nie zostało ani jedno „podział” w tym znaczeniu; słowo zostaje dla rozkładu spadku i wymiaru filtra. Dwa miejsca w README robi sesja B.
- **P10:** etykiety wykresu porannego ruchu odmieniają „wizyta” według ostatniej liczby przedziału („21–24 wizyty”, „25–28 wizyt”, „do 8 wizyt”, `narzedzie/widoki.js`).
- **P11:** „Etykiety zmiany (poziom po wykrytej zmianie wobec poziomu przed nią): …” w „Zdarzeniach”.
- **P12:** „1 044 wizyty we wszystkich celach (w tym 1 024 wizyty L4, które liczy pozycja 5 listy priorytetów)”.

### Poprawka 1. Tabela „co zmieniło kohorty i wynik” jako pierwsza karta „Kohort”

- **Tytuł:** „Kohorty zmieniły się głównie po naszych decyzjach o kampaniach na L4, a wynik obniża dodatkowo awaria Safari”. „Głównie” opiera się na rozkładzie spadku powrotu z „Czy to wzrost” (około 71% przypada na większy udział nowych kampanii; kod sprawdza, że to ponad połowa). „Po” mówi o kolejności w czasie, nie o przyczynie.
- **Wniosek:** „Od 10 kwietnia 2026 nowe kampanie na L4 dają 41% nowych pacjentów, a największą pewną stratą jest awaria Safari: 75–83 tys. zł marży rocznie.” Kod sprawdza, że pozycja 1 ma najwyższą kwotę wśród pozycji o wysokiej pewności.
- **Zastrzeżenie (jedno, jak w decyzji):** „Zdarzenia z tych samych miesięcy nakładają się, więc tabela pokazuje, co zmieniło się po zdarzeniu, a nie dowodzi przyczyny.”
- **Kolumny:** Kiedy · Co się stało (rodzaj: decyzja, zdarzenie, awaria albo zmiana bez znanej przyczyny) · Kogo dotyczy · Co zmieniło się po nim (przed → po, liczebność i okres w drugim wierszu komórki) · Skutek w złotych · Pewność · Co robimy.
- **Wiersze (8, jak w propozycji):** start sprzedaży TelemediGO w newsletterze (8.09.2025), start Meta na L4 (3.11.2025), zwroty po wizycie (13.11.2025), poranne opóźnienia (24.11.2025), start TikToka na L4 (9.02.2026), powrót w kampaniach działających w obu latach (2.03.2026), awaria Safari (17.03.2026), Google Ads na markę (22.05.2026). Remarketing Meta i dwa zdarzenia jakości danych zostają tylko na osi; spadek marży i powrotu w 30 dniach stoi w wierszach kampanii na L4.
- **Skąd liczby (bez nowych obliczeń):** kwota, dopisek i pewność wierszy z pozycją listy to dosłownie pola przeglądu priorytetów (`C["priorytety"]["przeglad"]`); poziomy i liczebności zdarzeń to te same odcinki serii, z których eksport składa zdania kart zdarzeń (`b_eksport.py` przekazuje je tabeli w polach pomocniczych, które nie trafiają na stronę); Safari z tych samych pól co karta Safari w „Lejku”; zwroty z tej samej funkcji co karta zwrotów w „Po zakupie”; TikTok na pacjenta z wierszy ekonomii kampanii; powrót 4,1% i 22,0% z karty „Lepsza retencja”; Google Ads na markę z tych samych pól co karta zdarzenia.
- **Pewność:** przy wierszach z pozycją listy znacznik i dopisek tej pozycji. Przy trzech wierszach bez pozycji (newsletter, powrót w kampaniach działających w obu latach, Google Ads na markę) bez znacznika poziomu, tylko zdanie z karty zdarzenia („skok sprzedaży widoczny w danych; nadwyżkę szacujemy z późniejszego tempa”, „zmiana poniżej progu metody wykrywania zmian”, „część może być sezonowa…”). Poziomu, którego nie nadała lista priorytetów, nie wymyślamy.
- **Odnośniki w każdym wierszu:** pozycja listy albo punkt „Czego nie wiemy” (numer brany z danych po treści punktu), „Pokaż na kohortach dziennych” i „Opis zdarzenia”. „Pokaż na kohortach dziennych” ustawia w adresie okna 60 dni przed i po dacie zdarzenia (to samo porównanie co na liście porównań w filtrach) i przewija do wykresu dzień po dniu. Strona rozpoznaje te okna i pokazuje na liście porównań właściwe zdarzenie, a nie „własne daty”.
- **Przewijanie (`f_techniczna.md`, punkt 10):** każdy odnośnik do „Kohort” z parametrami w adresie przewija teraz do wykresu dzień po dniu, tak jak odnośniki do lejka przewijają do wykresu kroków. To dotyczy też dawnych odnośników z kart (np. „Kohorty: nowi pacjenci według źródła pozyskania”). Bez tego po dodaniu tabeli na górze zmieniony filtr byłby daleko pod ekranem. Sama zakładka (`#kohorty`) otwiera się na górze, przy tabeli.
- **Dawna pierwsza karta** (roczny spadek powrotu) stoi pod wykresem dziennym. W „Zdarzeniach” (wstęp) i w „Czy to wzrost” (karta „Lepsza retencja”) doszła jedna linijka z odnośnikiem do tabeli.
- **Telefon:** każdy wiersz jako osobna karta z etykietami kolumn (styl `tabela-tekst`, ten sam co w przeglądzie priorytetów i w „Czego nie wiemy”).
- **Szkic:** sekcja `### kohorty/zdarzenia` w `notatki/e_teksty_zakladki.md`, pisana ręcznie z liczb widocznych na stronie w wersji `3b5eeaa` (dane z plików strony), a nie z kodu.
- Pliki: `analiza/e_teksty_zakladki.py` (funkcja `tabela_zdarzen`), `analiza/b_eksport.py`, `analiza/e_teksty.py` (odnośnik w karcie retencji), `narzedzie/index.html`, `narzedzie/widoki.js`, `narzedzie/styl.css`; dane w `narzedzie/dane_strony/kohorty.js` (klucz `zdarzenia`).

### Poprawka 5. Wykres Safari na równych oknach

- Wykres w karcie Safari („Lejek”) i w pozycji 1 porównuje teraz oba wiersze w tych samych dniach: 60 dni przed awarią (16.01–16.03.2026) i 60 dni po niej (17.03–15.05.2026). Safari 66,2% → 45,1%, pozostałe przeglądarki 64,8% → 63,4%. Przypis dodaje poziom Safari do końca danych (45,6% od 17.03 do 30.09.2026), więc „nie wraca” ma pokrycie pod wykresem.
- Zgrane zdania, które cytują wartości z wykresu: wniosek karty Safari w „Lejku” i „Dlaczego” w pozycji 1 („W 60 dniach po awarii krok konta … przechodzi 45% sesji wobec 66% w 60 dniach przed nią, i do końca danych nie wraca”). Kod sprawdza, że poziom do końca danych jest taki jak w 60 dniach po awarii. „Po czym poznamy” w pozycji 1 („wraca z około 46% do około 66%”) zostaje, bo opisuje poziom do końca danych.
- Pliki: `narzedzie/app.js` (`hantleSafari`), `analiza/e_teksty.py`, `analiza/b2_eksport_c.py` (pole `safari_60`), szkic `notatki/e_teksty.md`; skrypt `analiza/f_wykresy_tekst.py` sprawdza teraz, że oba wiersze mają te same okna.

### Poprawki 6a, 6b, 6c

- **6a** (pasek zakładek w dwóch rzędach do 1 000 px) zrobiła wcześniej sesja kontroli technicznej na polecenie Kuby; jest w commicie `7bae553`. Tu tylko sprawdzone.
- **6b** (Safari na telefonie, „Lejek” przesuwał się w bok): w regule dla telefonu `.filtry { overflow-x: hidden; overflow-x: clip; }` (starsze Safari bez `clip` biorą `hidden`). WebKit przy 375 px: szerokość dokumentu 375 zamiast 478.
- **6c** (ucięte cyfry w „Kohortach w podziale” i „Krokach lejka w podziale”): przyczyną była stała minimalna szerokość kolumny miary (140 px; trzy kolumny dawały 329 i 333 px przy ramce 313 px). W widoku jednej miary na telefonie kolumna nie ma już tej szerokości, „z N” stoi w osobnym wierszu, a „z” i liczba są sklejone twardą spacją. W widoku „Pokaż całą tabelę” bez zmian. Obie tabele mają 313 px w Edge i w WebKit.

## Kontrola

(uzupełniane po końcowym eksporcie)

## Uwagi dla sesji prowadzącej i sesji B

- **README (sesja B):** lista „Co robimy w pierwszym tygodniu” miała kolejność 1, 3–4, 2; strona ma teraz 1, 2, 3–4, sprawdzenia. Wysłałem sesji B jedną wiadomość; w README w folderze kolejność jest już taka jak na stronie (zmiana sesji B, jeszcze niezacommitowana w chwili pisania). Inne zmienione na stronie zdania (Safari 66% → 45%, „bez alarmu”, „przybyło 12%”) w README nie występują.
- Pliki niezacommitowane, które nie są moje: `README.md`, `analiza/f_rozmowy.py`, `notatki/f_slad_pracy.md`, `notatki/lekcje.md`, `rozmowy/` (sesja B).

## Propozycje wpisów do wspólnych notatek (bez numerów)

- **`ZALOZENIA.md`:** nazwa zbiorcza obu sposobów przypisania źródła to „reguły przypisania” (P9); „podział” zostaje dla rozkładu spadku i wymiaru filtra. Wykres Safari porównuje oba wiersze na tych samych oknach 60 dni przed awarią i po niej; poziom do końca danych stoi w przypisie i w szczegółach.
- **`DECYZJE.md`:** runda F, część strony zrobiona według decyzji Kuby z 23.10.2026: poprawki 3, 4 (wszystkie dziesięć, plus trzecie miejsce z błędem P8), 1 (tabela na górze „Kohort”, 8 wierszy, zdarzenie remarketingu Meta tylko na osi), 5, 6a–6c. Odnośniki do „Kohort” z parametrami przewijają do wykresu dziennego.
- **`ZNALEZISKA.md`:** nic nowego w danych.
- **`PRZEKAZANIE.md`:** stan po części strony rundy F; odnośnik do tej notatki; kolejny krok: przejrzenie przez Codeksa nowej tabeli i zmienionych zdań, komplet kontroli na ostatecznej wersji, publikacja za zgodą Kuby.
- **`analiza/README.md`:** wiersze „F” dla skryptów `analiza/f_*.py` (propozycja z `f_techniczna.md`), z dopiskiem, że `f_wykresy_tekst.py` porównuje też każdą komórkę tabeli zdarzeń w „Kohortach” z kartą źródłową, a `f_odnosniki.py` sprawdza przewinięcie do wykresu dziennego i porównanie „60 dni przed i po”.
