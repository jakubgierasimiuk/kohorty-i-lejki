# Wspólna wersja v2 (końcowa) — grafika narzędzia

Powstała z czterech niezależnych propozycji (Fable, Sol, Astra, Claude) i drugiej rundy, w której każdy z trzech recenzentów ocenił syntezę v1. Zmiany wobec v1 wynikają z ich sprzeciwów. Oznaczenia: **P** = w przeglądarce z danych, które strona już ma; **E** = wymaga eksportu (sesja prowadząca); S / M / L = wysiłek.

## 1. Puenta

Zostaje obecna identyfikacja: granatowy pasek, białe karty, jeden akcent, znaczniki stanu z ikoną i słowem, wykres kroków lejka. Zmieniamy warstwę dowodów: porównania „przed → po” mają być obrazem (hantle), wykresy dzienne mają mówić to, co wniosek nad nimi, a mapa kohort ma jedną, jawną skalę. **Zero wykresów kołowych.** Wdrażamy w etapach, z których każdy sam nadaje się do pokazania.

## 2. Zasady wspólne (zgoda wszystkich po drugiej rundzie)

**Kolor**
- Bez zmian: pasek `#13213a`, tło `#eef1f5`, karty białe, akcent `#1f5fcc` tylko dla odnośników, wyboru i fokusu, tokeny stanów i fiolet „Test”, tryb ciemny.
- **Dwa kodowania, nigdy pomieszane.** (1) Porównanie jednej miary między okresami: szary = okres wcześniejszy, niebieski `#2a78d6` = okres późniejszy. (2) Porównanie grup: stała paleta grup, a okres odróżnia styl (linia ciągła / przerywana, punkt pełny / pusty). Legenda zawsze mówi, które kodowanie obowiązuje.
- **Nazwy okresów idą za wyborem**, tak jak dziś w tytule wykresu kroków: „rok wcześniej / ostatnie 12 miesięcy”, „przed awarią / po awarii” (z datami), litery A/B tylko przy własnych datach.
- **Kolor idzie za grupą, nie za kolejnością zaznaczenia** (dziś `przydzielKolory` w `app.js` i `przydziel` w `widoki.js` dają pierwszy wolny kolor). Mapa klucz → kolor; „nowe kampanie na L4” mają jeden kolor wszędzie.
- **Paleta serii bez kolorów stanów:** `--series-6 #008300` i `--series-8 #e34948` wymienione na barwy neutralne, paleta sprawdzona walidatorem (daltonizm, tryb jasny i ciemny). Na wykresie najwyżej 4 grupy w kolorze plus seria odniesienia („Wszyscy w filtrze”, „Razem”) w kolorze tuszu.
- **Tła okresów** na wykresach dziennych: dwa neutralne szare poziomy (niebieskie tło B konkuruje z niebieską serią) z podpisem i datami przy górnej krawędzi.
- **Mapa kohort:** kolory z tokenów (dziś `RAMPA`, `#fff` i `#0b0b0b` wpisane na sztywno — w trybie ciemnym macierz „świeci”), legenda skali, brak pełnego okna oznaczony inaczej niż zero. Skala: rozwidlenie R1.

**Typografia**
- Jedna rodzina systemowa. Akapity i wnioski do `72ch`; tytuł-wniosek karty do `64ch` z `text-wrap: balance`.
- Tytuł zakładki 26/32 (telefon 22/28), tytuł karty 18/24 półgruby, wniosek 16/24 o stopień lżejszy niż tytuł, tekst 15/23, tabele z liczbami 13 px (14 px tylko tabele tekstowe), przypisy i osie min. 12 px.
- Cyfry tabelaryczne także na osiach, w legendach i podpowiedziach.

**Układ**
- Rytm odstępów 8 / 12 / 16 / 24 / 32 px zamiast jednego 14 px.
- Kartą jest samodzielna jednostka pracy. Filtry lokalne, legenda, zastrzeżenie i „Szczegóły” są częścią karty, bez własnego pudełka. Zastrzeżenie: ikona + słowo „Zastrzeżenie” + tekst na tle karty, oddzielone cienką linią. Zastrzeżenie, które ogranicza główny wniosek, stoi przy nim. Wyjątki: trzy kafelki werdyktu i pasek priorytetu (płaskie, trzy pola rozdzielone liniami).
- Sąsiednie karty bez wymuszonej równej wysokości.
- **Filtry:** wspólny panel tylko w kohortach i lejku (dwa poziomy: „Główne” zawsze widoczne, „Zawęź” zwinięte z licznikiem i chipami aktywnych zawężeń). W „Po zakupie” i „Wyniku biznesu” filtry zostają przy wykresie, którego dotyczą, z jasnym zakresem działania.

**Komponenty**
- **Odnośniki:** w tekście ciągłym podkreślenie zostaje (bez niego odnośnik jest rozpoznawalny tylko po kolorze, a na telefonie nie ma najechania). „Zobacz w danych” jako osobny, spokojny styl przycisku-odnośnika z konkretną nazwą celu.
- **Legenda wykresów dziennych:** własna (kreska w kolorze + nazwa, wartość pod kursorem w tym samym miejscu, data w nagłówku), z **polami wyboru serii** (warunek przeniesienia wykresu nad tabelę — dziś wybór serii jest w tabeli). Bez „Dzień: —” i obróconej etykiety „%”. Podpisy na końcach linii dla 1–3 serii.
- **Zdarzenia na wykresach:** domyślnie tylko z obszaru wykresu (pole `obszar`), przełącznik „wszystkie”; znaczniki w pasku pod lub nad wykresem, rozsuwane przy kolizji; linie jasne i ciągłe; po wskazaniu krótka nazwa i data; na telefonie bez numerów.
- **Podpowiedź i dostępność:** jedna obsługa najechania, dotyku i klawiatury dla wykresów SVG i odczyt wartości także dla wykresów uPlot; każdy nowy SVG z `role="img"` i opisem równym wnioskowi, kolory tylko z tokenów, obszar dotyku ≥ 44 px, sprawdzenie w trybie ciemnym.
- **Tabele:** przyklejona pierwsza kolumna i nagłówek; nazwy okresów słowami; liczby do prawej; pasek danych w komórkach udziału; na telefonie widok jednej wybranej miary (nazwa, oba okresy, zmiana, liczebność), pełna tabela pod przełącznikiem. Tabela zastąpiona wykresem idzie do „Szczegółów”.
- **Etykieta zmiany:** rozwidlenie R3. Zmiana bez oceny (np. struktura) — etykieta neutralna, bez „lepiej/gorzej”.
- **Sekcje zwijane:** cały wiersz jako obszar dotyku ≥ 44 px.
- **Szerokość wykresów:** zamiast `Math.max(320, cel.clientWidth)` szerokość karty z zapasem na ukryty element (`cel.clientWidth || 300`), żeby wykres nie wychodził poza kartę na telefonie.
- **Bez nowych ocen samą grafiką:** np. lista „sprawdzone i czyste” nie dostaje zielonego znacznika „Czyste”, jeśli dane go nie niosą.

**Nawigacja:** komputer bez zmian, z dwoma cienkimi separatorami grup ([Czy to wzrost] | zakładki z danymi | Priorytety · Czego nie wiemy) i „Dalej: …” na dole zakładki. Telefon: rozwidlenie R2.

## 3. Formy wykresów (SVG bez nowej biblioteki; uPlot zostaje do serii dziennych)

| Forma | Gdzie |
|---|---|
| **Hantle** | powrót w 30/60/90/180 dniach („Czy to wzrost”, „Kohorty”); Safari na iOS przed awarią i po niej wobec pozostałych przeglądarek (lejek, priorytet 1); poranny ruch („Po zakupie”); przeglądarki w aplikacjach (E) |
| **Punkt wyniku względem zera, dwa symbole reguł przypisania** | ekonomia kampanii (wynik na pacjenta, przełącznik 90/180 dni; koszt i marża w podpowiedzi i tabeli w Szczegółach) |
| **Dwa wykresy jeden pod drugim** | „Wynik biznesu”: (1) marża przed kosztem kampanii i wydatki na kampanie (jedna jednostka, jedna oś), (2) marża po wszystkich kosztach. Definicja jak w eksporcie: marża przed kosztem kampanii = marża + wydatki + prowizja |
| **Słupki parami** | kwartały: zmiana rok do roku marży przed kosztem kampanii obok zmiany wydatków; TelemediGO: trzy sposoby zakupu, oba lata, wspólny początek (E) |
| **Słupki w skali liczebności (nie 100%)** | „Więcej pacjentów”: dwa lata, drugi podzielony na nowe kampanie i pozostałych (E — pierwsza zakładka nie ładuje danych kohort) |
| **Schodki poziomów** (punkt po każdym kroku, bez sumowania jak w wodospadzie) | mostek „dashboard → dane oczyszczone” dla zamówień i przychodu (P, `jakosc.mostek`) |
| **Udział w czasie** (miesięcznie, osobny wykres pod trendem, ta sama oś czasu) | lejek: udział sesji nowych kampanii w sesjach osób, które jeszcze nie kupowały (liczony z pliku kampanii, niezależnie od wybranego podziału); kohorty: udział pacjentów nowych kampanii — z oznaczeniem, które kohorty nie mają jeszcze pełnego okna |
| **Linie z wyróżnieniem** (jedna seria w kolorze, reszta cienka i szara) | kohorty, punktualność („Rano”), zwroty (L4), lejek (wybrana przeglądarka) |
| **Mapa ciepła** | macierz kohort (R1); opóźnienia według godziny (E) |
| **Oś czasu zdarzeń** | kształt znacznika według rodzaju, numery bez kolizji, podpowiedź; na telefonie pionowa lista dat |

**Nie robimy:** koło i pierścień; Sankey lejka; wodospady rozkładów opisowych („71% spadku powrotu”, rozkład III kwartału); wykres kwot priorytetów (niesumowalne scenariusze o różnych horyzontach); dwie osie Y; dodatkowe odniesienie „Razem” w wykresie kroków (druga baza porównania); nowe rzędy kafelków, pierścienie, mini-wykresy dla ozdoby; liczby do wykresów wyciągane z napisów (potrzebne pole liczbowe → E); zmiana domyślnej rozdzielczości kohort z dziennej.

## 4. Zakładka po zakładce

| Zakładka | Zmiany | Dane |
|---|---|---|
| Czy to wzrost | werdykt, kafelki, decyzje bez zmian (płaściej na telefonie); hantle powrotu zamiast tabeli (tabela do Szczegółów); słupki „Więcej pacjentów”; słupki parami TelemediGO; schodki mostka | okna 30/60/90 P, 180 E; pacjenci E; TelemediGO E; mostek P |
| Kohorty | wniosek → filtry „Główne” → wykres dzień po dniu (legenda z wyborem serii) → tabela w podziale → macierz → krzywa powrotu (podpisy końców, prowadnice 30/60/90/180) → udział nowych kampanii w czasie (opcja) | P |
| Lejek | wniosek → dwie karty napraw w rzędzie (Safari z hantlem) → filtry → wykres kroków (kliknięcie przejścia ustawia miarę na wykresie dziennym) → wykres dzień po dniu → skład ruchu nowych osób (opcja) → tabela | P |
| Po zakupie | punktualność z wyróżnionym „Rano”; hantle porannego ruchu; słupki powrotu według opóźnienia; zwroty z wyróżnionym L4; filtry przy wykresach; godziny (E) | P, godziny E |
| Zdarzenia | chipy obszarów w nagłówku karty osi; kształty według rodzaju; numery bez kolizji; podpowiedź; telefon: pionowa lista; „Skąd wiemy” zwinięte; tabela wykrytych z sortowaniem | P |
| Wynik biznesu | dwa wykresy (marża przed kampaniami i wydatki; marża po kosztach); słupki parami kwartałów; tabela kwartałów mieści się w karcie; tabela miesięcy do Szczegółów; ekonomia kampanii jako punkt względem zera | P |
| Jakość danych | schodki mostka; okno duplikatów 10–24.06 podcieniowane | P |
| Priorytety | przegląd zostaje, przy kwocie zostają horyzont i warunek; telefon: numer, decyzja, kwota, pewność, czas, reszta rozwijana; pigułki 1–12; hantel Safari w karcie 1; wynik od zera w tabelach kampanii; odnośnik do powiązanych niewiadomych; separatory grup (E) | P, grupy E |
| Czego nie wiemy | „pozycja 9” → numer z nazwą decyzji; filtr według pozycji; widoczne pytanie i test, uzasadnienie rozwijane | P |

## 5. Etapy (każdy kończy się sprawdzeniem i nadaje się do pokazania sam)

1. **Naprawy obecnych dowodów (ok. 0,5–1 dnia, P):** stałe kolory grup i paleta bez kolorów stanów; dwa kodowania okresu i grupy; skala i legenda mapy kohort (R1) z tokenami; szerokość wykresów na telefonie; etykieta zmiany (R3); typografia, rytm, zastrzeżenie bez pudełka; oś zdarzeń na telefonie jako lista; nawigacja na telefonie (R2).
2. **Główne nowe dowody (ok. 1 dnia, P):** komponent hantli (powrót 30/60/90 w „Czy to wzrost” i w kohortach, Safari w lejku i priorytecie 1, poranny ruch); „Wynik biznesu”: dwa wykresy i ekonomia kampanii względem zera.
3. **Praca na co dzień (ok. 1 dnia, P):** legenda z wyborem serii, zdarzenia według obszaru bez kolizji, wyróżnienie serii; kolejność kart w kohortach i lejku; filtry dwupoziomowe; tabele na telefonie; dostępny odczyt wartości.
4. **Dodatki (opcjonalne):** schodki mostka, słupki parami kwartałów, udział nowych kampanii w czasie, oś zdarzeń z kształtami, separatory i „Dalej”.
5. **Z eksportem (osobno, sesja prowadząca):** 180 dni i „Więcej pacjentów” na pierwszej zakładce, TelemediGO, przeglądarki w aplikacjach, godziny, grupy priorytetów.

**Warunki odbioru każdego etapu:** 9 zakładek przy 1366 i 375 px, tryb jasny i ciemny, 0 błędów w konsoli, brak przewijania strony w bok, odnośniki działają i odtwarzają pełny stan (także rozwinięte „Szczegóły”); brak danych wygląda inaczej niż zero; **liczby na wykresach zgodne z tekstem tej samej karty** — nowa kontrola w `analiza/e_przegladarka.py` czyta podpisy z SVG i legend i porównuje je z liczbami w zdaniu karty.

## 6. Rozwidlenia do decyzji Kuby

- **R1. Skala mapy kohort.** (a) wspólna, stała skala z jawnymi progami (np. 5, 10, 15, 20, 30%) — ten sam kolor = ten sam odsetek w każdym oknie i po każdej zmianie filtrów; (b) osobna skala dla każdego okna, nazwana w legendzie — lepiej widać zmianę w czasie w obrębie okna, ale ten sam kolor oznacza różne odsetki. Rekomendacja: (a), z progami dobranymi tak, żeby w każdym oknie były co najmniej dwa odcienie.
- **R2. Zakładki na telefonie.** (a) przycisk z nazwą bieżącej zakładki, rozwijający pełną listę — odzyskuje około ćwierci pierwszego ekranu; (b) zostają widoczne pigułki (ciaśniej) i dochodzi przycisk „Zakładki” po przewinięciu — osoba z telefonem od razu widzi, z czego składa się narzędzie.
- **R3. Słowo przy etykiecie zmiany.** (a) słowo „lepiej/gorzej” widoczne zawsze, także w gęstych tabelach (np. drugi wiersz komórki) — dosłownie spełnia zasadę „kolor stanu zawsze ze słowem”; (b) słowo widoczne w kafelkach, hantlach i pojedynczych etykietach, a w gęstych tabelach jedna linia objaśnienia pod tabelą i słowo w podpowiedzi — mniej szumu w tabelach z kilkudziesięcioma etykietami.

Rozstrzygnięte w drugiej rundzie: „Wynik biznesu” — dwa wykresy (marża przed kosztem kampanii i wydatki, pod nimi marża po kosztach); ekonomia kampanii — punkt wyniku względem zera z dwoma symbolami reguł.
