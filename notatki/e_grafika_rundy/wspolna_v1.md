# Wspólna wersja v1 — jak przedstawić graficznie narzędzie (synteza czterech propozycji)

Źródła: propozycje Fable, Sol, Astra i Claude (sesja grafiki), runda 1, ten sam brief (`brief.md`). Poniżej to, w czym się zgadzamy, oraz cztery rozwidlenia, w których propozycje się różnią. Każda pozycja ma oznaczenie: **P** = liczone w przeglądarce z danych, które strona już ma; **E** = wymaga eksportu (inna sesja); S / M / L = wysiłek.

## 0. Puenta

Zostaje obecna identyfikacja: granatowy pasek, białe karty, jeden kolor akcentu, znaczniki stanu z ikoną i słowem, wykres kroków lejka. Zmieniamy warstwę dowodów: najważniejsze porównania „rok wcześniej → ostatnie 12 miesięcy” czytelnik ma widzieć jako obraz, a nie odczytywać z tabel. Wykresy dzienne porządkujemy według zasad dataviz. Przebudowujemy układ tak, żeby część robocza (filtry, wykres) stała wyżej. **Zero wykresów kołowych.**

## 1. System wizualny

**Kolor**
- Bez zmian: pasek `#13213a`, tło `#eef1f5`, karty białe, akcent `#1f5fcc` tylko dla odnośników, wyboru i fokusu; tokeny stanów i fiolet „Test”; tryb ciemny.
- **Jedna para okresów na całej stronie:** „ostatnie 12 miesięcy” (okres B) = niebieski serii `#2a78d6`; „rok wcześniej” (okres A) = neutralny szary. Dotyczy hantli, kresek w wykresie kroków, krzywej powrotu, słupków parami.
- **Kolor idzie za bytem, nie za kolejnością zaznaczenia** (dziś `przydzielKolory` w `app.js` i `przydziel` w `widoki.js` dają pierwszy wolny kolor). Mapa klucz → kolor, stała po zmianie filtrów. „Nowe kampanie na L4” mają jeden kolor wszędzie.
- **Paleta serii:** usunąć z puli kolory podobne do stanów (`--series-6 #008300` zlewa się z „dobrze”, `--series-8 #e34948` to czerwień „źle”); zastąpić neutralnymi barwami i przepuścić przez walidator palety (daltonizm, tryb jasny i ciemny). Domyślnie najwyżej 4 serie na wykresie; więcej — przez wybór albo małe wielokrotności.
- **Tła okresów na wykresach dziennych:** dwa neutralne szare poziomy (zamiast niebieskiego tła B, które konkuruje z niebieską serią) i podpis „rok wcześniej” / „ostatnie 12 miesięcy” przy górnej krawędzi pola.
- **Mapa ciepła kohort:** kolory z tokenów (dziś `RAMPA` i `#fff`/`#0b0b0b` wpisane na sztywno, więc w trybie ciemnym macierz „świeci") i legenda skali nad macierzą. Skala — rozwidlenie R1.

**Typografia**
- Jedna rodzina systemowa (bez zmian). Akapity i wnioski do `72ch`; tytuł-wniosek karty do `64ch` z `text-wrap: balance`.
- Tytuł zakładki 26/32 (telefon 22/28), tytuł karty 18/24 półgruby, wniosek 16/24 o grubość niżej niż tytuł (dziś obie linie wyglądają na pogrubione i hierarchia jest płaska), tekst 15/23, tabele 14/20, przypisy i osie min. 12–13 px.
- Cyfry tabelaryczne także na osiach i w legendach wykresów.

**Układ**
- Rytm odstępów 8 / 12 / 16 / 24 / 32 px zamiast jednego 14 px wszędzie.
- **Kartą jest samodzielna jednostka pracy** (werdykt, analiza z wykresem, zdarzenie, priorytet). Filtry lokalne, legenda, zastrzeżenie i „Szczegóły” to części karty, bez własnego pudełka. Zastrzeżenie: ikona + pogrubione słowo „Zastrzeżenie” + tekst, na tle karty, oddzielone cienką linią (koniec „kart w kartach”). Wyjątki zostają: trzy kafelki werdyktu i pasek priorytetu (płaskie, trzy pola rozdzielone liniami).
- Stała kolejność w karcie: **wniosek → wykres → zastrzeżenie → „Zobacz w danych” → Szczegóły**.
- Sąsiednie karty bez wymuszonej jednakowej wysokości (dziś duże puste pola w „Czy to wzrost” i lejku).
- Na ekranach ≥ 1100 px karta z małym wykresem może mieć dwie kolumny wewnątrz (tekst po lewej, wykres po prawej) — to jedna karta, nie dwie.

**Komponenty**
- **Legenda wykresów dziennych:** własna (kreska w kolorze serii + nazwa), wartość pod kursorem w tej samej pozycji, data w nagłówku legendy; bez domyślnych „Dzień: —” i obrysowanych kwadratów; bez obróconej etykiety „%” (jednostka w podziałce). Podpis bezpośredni na końcu linii dla 1–3 serii.
- **Zdarzenia na wykresach:** domyślnie tylko zdarzenia z obszaru danego wykresu (pole `obszar`), przełącznik „wszystkie”; znaczniki w pasku nad lub pod wykresem z rozsuwaniem przy kolizji („3 5”, „9 10” dziś nachodzą); linie jasne i ciągłe; po wskazaniu krótka nazwa (`krotko`) i data. Na telefonie bez numerów, same linie, nazwa po dotknięciu.
- **Podpowiedź:** jedna wspólna dla wykresów SVG (hantle, kroki, oś zdarzeń): najechanie, dotknięcie i fokus klawiatury (dziś `title`, który nie działa dotykiem).
- **Filtry:** jeden panel na zakładkę, dwa poziomy: „Główne” (porównanie, okresy, podział na serie, przypisanie) zawsze widoczne; „Zawęź” zwinięte z licznikiem; aktywne zawężenia jako chipy z krzyżykiem także po zwinięciu.
- **Tabele:** przyklejona pierwsza kolumna i nagłówek; nazwy okresów słowami zamiast „B (A)” (litery tylko przy własnych datach); liczby do prawej; pasek danych w komórkach udziału (koduje wartość tej komórki). Na telefonie domyślnie widok jednej wybranej miary (nazwa, oba okresy, zmiana, liczebność), pełna tabela pod przełącznikiem. Tabela, którą zastępuje wykres, idzie do „Szczegółów” (zostaje jako widok zapasowy i dostępnościowy).
- **Odnośniki:** bez stałego podkreślenia w treści kart (podkreślenie po najechaniu i przy fokusie); „Zobacz w danych” jako małe przyciski z ikoną zakładki docelowej.
- **Etykieta zmiany:** rozwidlenie R3.
- **Sekcje zwijane:** cały wiersz jako obszar dotyku ≥ 44 px.
- **Wykresy na telefonie:** usunąć minimalną szerokość 320 px (`Math.max(320, …)` w `app.js` i `widoki.js`), żeby wykres nie wychodził poza kartę.

**Nawigacja**
- Komputer: 9 zakładek bez zmian, dwa cienkie separatory grup: [Czy to wzrost] | Kohorty · Lejek · Po zakupie · Zdarzenia · Wynik biznesu · Jakość danych | Priorytety · Czego nie wiemy. Na dole każdej zakładki „Dalej: <następna zakładka>”.
- Telefon: rozwidlenie R2.

## 2. Katalog form wykresów (jeden komponent na formę, SVG, bez nowej biblioteki; uPlot zostaje do serii dziennych)

| Forma | Do czego w tym projekcie |
|---|---|
| **Hantle** (szary punkt = rok wcześniej, niebieski = ostatnie 12 miesięcy, etykieta zmiany przy odcinku) | powrót w 30/60/90/180 dniach; Safari na iOS przed awarią i po niej wobec pozostałych przeglądarek; poranny ruch po zakupie; przeglądarki w aplikacjach (E) |
| **Schodki poziomów** (punkt na każdym kroku korekty, bez sumowania jak w wodospadzie) | mostek „dashboard → dane oczyszczone” dla zamówień i przychodu (procent wzrostu po każdym kroku) |
| **Słupki parami** | kwartały: zmiana rok do roku marży przed kosztem kampanii obok zmiany wydatków na kampanie |
| **Skumulowany 100% w czasie** (miesięcznie) | udział sesji nowych kampanii w sesjach osób, które jeszcze nie kupowały (lejek); udział pacjentów nowych kampanii w nowych pacjentach (kohorty) — osobny wykres pod trendem, ta sama oś czasu, **nie druga oś** |
| **Pasek-licznik / słupek skumulowany ≤ 3 części** | „Więcej pacjentów”: nowe kampanie na L4 wobec pozostałych w obu latach; TelemediGO: trzy sposoby zakupu w obu latach |
| **Linie dzienne z wyróżnieniem** (jedna seria w kolorze, reszta cienka i szara) | kohorty (dzień po dniu), punktualność (pora „Rano”), zwroty (L4), lejek (wybrana przeglądarka) |
| **Wynik względem zera** | ekonomia kampanii: wynik na pacjenta, dwa symbole dla dwóch reguł przypisania, przełącznik 90/180 dni — forma: rozwidlenie R4 |
| **Mapa ciepła** | macierz kohort (jest; legenda i skala — R1); opóźnienia według godziny (E) |
| **Oś czasu zdarzeń** | zakładka „Zdarzenia”: kształt znacznika według rodzaju, numery bez kolizji, podpowiedź; na telefonie pionowa lista dat |

**Czego nie robimy (zgoda wszystkich):** wykresy kołowe i pierścieniowe (żadna część całości w projekcie nie jest „na jedno spojrzenie” bez porównania z rokiem wcześniej; dwie części → pasek, trzy → słupek skumulowany, dziewięć kanałów → słupki); Sankey lejka (lejek jest liniowy, dane nie opisują ścieżek); wodospady rozkładów opisowych („71% spadku powrotu”, rozkład III kwartału) — wykres nadałby im pewność, której tekst odmawia; wykres kwot priorytetów (kwoty to niesumowalne scenariusze o różnych horyzontach); dwie osie Y; nowe rzędy kafelków, pierścienie, mini-wykresy dla ozdoby; parsowanie liczb z napisów do wykresów (potrzebne pole liczbowe w danych → E); zmiana domyślnej rozdzielczości kohort z dziennej.

## 3. Zakładka po zakładce

| Zakładka | Zmiany | Dane | Wysiłek |
|---|---|---|---|
| **Czy to wzrost** | werdykt, kafelki, decyzje bez zmian (płaściej, ciaśniej na telefonie); „Lepsza retencja”: hantle 4 okien zamiast tabeli (tabela do Szczegółów); „Więcej pacjentów”: słupek skumulowany obu lat (nowe kampanie / pozostali); TelemediGO: słupek trzech sposobów zakupu; mostek dashboardu jako schodki | okna 30/60/90: P (`wzrost.retencja.okna`), 180: P z `kohorty.js` albo E; pacjenci: P z `kohorty.js`; TelemediGO: E (liczby są tekstem); mostek: P (`jakosc.mostek`) | M |
| **Kohorty** | kolejność: wniosek → filtry „Główne” → wykres dzień po dniu → skład pacjentów w czasie → tabela w podziale → macierz → krzywa; wyróżnienie serii „Wszyscy w filtrze”; legenda i skala macierzy; podpisy na końcu krzywej powrotu i prowadnice 30/60/90/180 | P | M |
| **Lejek** | kolejność: wniosek → filtry → wykres kroków → skład ruchu nowych osób w czasie → wykres dzień po dniu → karty napraw (z hantlem Safari) → tabela; w wykresie kroków przy wybranej wartości podziału cienkie szare odniesienie „Razem”; kliknięcie przejścia ustawia tę miarę na wykresie dziennym | P (Safari: `lejek_naglowek.safari`) | M |
| **Po zakupie** | punktualność: „Rano” wyróżnione; poranny ruch: hantle; powrót według opóźnienia: słupki poziome z szarą kreską roku wcześniej; zwroty: L4 wyróżnione; godziny: mapa ciepła lub słupki (E) | P, godziny E | M |
| **Zdarzenia** | chipy obszarów w nagłówku karty osi; kształty według rodzaju; numery bez kolizji; podpowiedź; telefon: pionowa lista; „Skąd wiemy” zwinięte; tabela wykrytych z sortowaniem | P | M |
| **Wynik biznesu** | wykres główny — R4; słupki parami kwartałów; tabela miesięcy do Szczegółów (sumy na wierzchu); tabela kwartałów mieści się w karcie; ekonomia kampanii: wynik względem zera | P (`wynik.serie`, `ekonomia.wiersze`) | M |
| **Jakość danych** | mostek jako schodki (ten sam komponent); duplikaty: podcieniowane okno 10–24.06; „Czyste” ze znacznikiem | P | S |
| **Priorytety** | przegląd zostaje; kwoty wyrównane, cyfry tabelaryczne; telefon: numer, decyzja, kwota, pewność, reszta rozwijana; pigułki 1–12 do skoku; w karcie 1 hantel Safari; w kartach z tabelą kampanii pasek wyniku od zera; odnośnik do powiązanych niewiadomych; separatory grup z podpisem — E | P, grupy E | S–M |
| **Czego nie wiemy** | „pozycja 9” → numer z nazwą decyzji; filtr według pozycji; nagłówek przyklejony; telefon: pytanie i pozycja widoczne, reszta rozwijana | P | S |

## 4. Pozostałe elementy oddawane (pliki sesji prowadzącej — tylko propozycja)

README: na górze prawdziwy link do narzędzia; pod odpowiedzią w skrócie jeden zrzut „Czy to wzrost” (PNG w repozytorium, z opisem alternatywnym, robiony skryptem przy eksporcie, z datą i commitem); opcjonalnie diagram Mermaid drogi pracy bez liczb (dane → kontrola → baza → analiza → eksport → narzędzie). Bez wykresów z liczbami w README.

## 5. Etapy wdrożenia (propozycja kolejności)

1. **Fundamenty (P, ok. 1 dzień):** stałe kolory bytów i paleta bez kolorów stanów; para kolorów okresów; tokeny mapy ciepła + legenda; usunięcie min. 320 px; typografia i rytm; zastrzeżenie bez pudełka; odnośniki; kolejność kart w lejku i kohortach.
2. **Wykresy dzienne (P, ok. 1 dzień):** wspólna legenda, zdarzenia według obszaru bez kolizji, wyróżnienie serii, podpisy końców linii.
3. **Nowe formy (P, 1–2 dni):** komponent hantli (4 miejsca), schodki mostka, skumulowany udział w czasie, słupki parami, wynik względem zera, oś zdarzeń z wersją na telefon, filtry dwupoziomowe, tabele na telefonie.
4. **Z eksportem (E, osobno):** TelemediGO, przeglądarki w aplikacjach, godziny, grupy priorytetów, ewentualnie 180 dni.

## 6. Rozwidlenia (propozycje się różnią — prosimy o głos z uzasadnieniem)

- **R1. Skala mapy ciepła kohort.** (a) wspólna, stała skala dla wszystkich okien (np. przedziały 0, 5, 10, 15, 20, 30, 50, 100%) z legendą — ten sam kolor = ten sam odsetek; (b) osobna skala dla każdego okna (jak dziś), ale nazwana w legendzie; (c) kolor = odchylenie od typowej kohorty w danym oknie (skala rozbieżna z szarym środkiem: „niżej niż zwykle” / „wyżej niż zwykle”), liczba w komórce bez zmian.
- **R2. Zakładki na telefonie.** (a) przycisk z nazwą bieżącej zakładki rozwijający listę 9 pozycji; (b) zostają pigułki w trzech rzędach + przycisk „Zakładki” po przewinięciu; (c) jeden przewijany w bok rząd zakładek z bieżącą widoczną.
- **R3. Słowo w etykiecie zmiany.** Zasada Kuby: kolory stanu zawsze z ikoną i słowem; jego zamówienie dla zmian rok do roku: „małe zielone albo czerwone etykiety ze strzałką”. Dziś słowo „lepiej/gorzej” jest tylko dla czytników ekranu, a strzałka pokazuje kierunek, nie ocenę (np. koszt rośnie = strzałka w górę, kolor czerwony). (a) słowo widoczne zawsze; (b) słowo widoczne w kafelkach, hantlach i pojedynczych etykietach, a w gęstych tabelach nagłówek kolumny mówi „zielone = lepiej, czerwone = gorzej” i słowo jest w podpowiedzi; (c) jak dziś.
- **R4. Wykres główny „Wyniku biznesu”.** (a) słupki skumulowane miesięczne: koszt lekarza + kampanie i prowizja + marża = przychód; (b) małe wielokrotności: przychód / koszty / marża, wspólny czas, każda z własną osią w złotych; (c) dwa wykresy: marża przed kosztem kampanii i wydatki na kampanie (jedna jednostka, jedna oś), pod nim marża po wszystkich kosztach. Oraz forma ekonomii kampanii: hantle koszt pozyskania → marża na pacjenta czy punkt wyniku względem zera z dwoma symbolami reguł.

## 7. Prośba do recenzenta (runda 2)

Odpowiedz najwyżej 800 słowami, po polsku, w tej strukturze:
1. **Zgoda / sprzeciw** dla sekcji 1–5: tylko to, z czym się nie zgadzasz albo co jest błędne lub ryzykowne (z uzasadnieniem i poprawką). Milczenie = zgoda.
2. **Głos w R1–R4**: wybrana opcja i jedno, dwa zdania dlaczego.
3. **Czego brakuje** (najwyżej 3 rzeczy), jeśli coś ważnego wypadło przy syntezie.
4. **Czy kolejność etapów jest dobra** przy założeniu, że czasu jest mało i każdy etap ma być gotowy do pokazania sam.
