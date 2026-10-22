# Propozycja graficzna narzędzia — runda 1 (recenzent: Fable)

Obejrzałem 24 zrzuty (komputer 1366 px, telefon 375 px), kod strony (`index.html`, `styl.css`, `app.js`, `widoki.js`, `widoki_c.js`, `karty.js`), teksty zakładek (`b_teksty_strony.md`) i kształt danych (załącznik A plus wyrywkowo pliki `dane_strony/`). Nic nie zmieniałem.

## A. Werdykt ogólny

Strona ma już dobrą kość: nagłówek karty jest wnioskiem, liczby stoją w kafelkach, stany i zmiany mają jeden słownik (ikona plus słowo plus kolor), a wykres kroków lejka jest najlepszym elementem całości, bo odpowiada wprost na pytanie „gdzie i od kiedy tracimy”. Najbardziej szkodzą trzy rzeczy. Po pierwsze, liczby, które niosą główny wniosek, czyta się z tabel i zdań, a nie z obrazu: powrót w czterech oknach, mostek od dashboardu, kwartały rok do roku, opóźnienia według godziny, skład ruchu nowych osób — wszystko to są porównania „przed i po”, które oko łapie w sekundę z hantli albo słupka, a z tabeli po dziesięciu. Po drugie, wykresy dzienne (uPlot) wyglądają surowo: 3–4 linie o równej wadze bez wyróżnienia tej, o którą chodzi, czternaście przerywanych linii zdarzeń z numerami, które na telefonie zlewają się w „3 4 5 6 7 8”, domyślna legenda uPlota z myślnikami i dwukropkami, obrócona etykieta osi „%”. Po trzecie, gęstość nie idzie za częstością użycia: panel filtrów kohort to ściana czternastu list rozwijanych, z których jedenaście stoi na „wszystkie”, a tabele „w podziale” mają dziesięć kolumn z dwiema liniami w komórce i obcinają się już przy 1366 px.

## B. System wizualny

### Kolory (tokeny w `styl.css`)

- **Zostaje:** pasek `#13213a`, tło `#eef1f5`, karty białe, akcent `#1f5fcc`, cztery stany i fiolet „Test”, tryb ciemny z własnymi wartościami. To jest poprawny, powściągliwy słownik trybu „Operate”.
- **Jedna reguła porównania okresów na całej stronie:** „ostatnie 12 miesięcy / okres B” = niebieski `--series-1`, „rok wcześniej / okres A” = ciemny szary `--ink-2`. Dziś tak jest w krzywej powrotu i na wykresie kroków (pasek niebieski, kreska granatowa); tę samą parę mają dostać hantle, słupki kwartałów i wykres godzin. Czytelnik uczy się jej raz.
- **Paleta serii:** zostawić sześć kategorii `--series-1…5, 7` (niebieski, pomarańcz, zieleń morska, bursztyn, róż, fiolet). Usunąć z puli `--series-6 #008300` (zlewa się z `--series-3` i z zielenią stanu „dobrze”) i `--series-8 #e34948` (to czerwień stanu „źle”; seria „Opera” na wykresie wyglądałaby jak alarm). W ich miejsce `--series-6: #7a6c5d` (brąz) i `--series-8: #4f7f9c` (stalowy). Limit serii na wykresie zostaje 8, ale od piątej serii proponuję małe wielokrotności (punkt D).
- **Tła okresów:** `--okres-b` podnieść z 0,08 do 0,12 i dodać na wykresie etykiety „rok wcześniej” / „ostatnie 12 miesięcy” w górnym rogu cienia (dziś szare pola są prawie niewidoczne i nikt nie wie, co znaczą bez przypisu).
- **Mapa ciepła macierzy:** `RAMPA` w `widoki.js` i kolory tekstu `#fff`/`#0b0b0b` są wpisane na sztywno, więc w trybie ciemnym macierz świeci. Zamienić na sześć tokenów `--heat-0…--heat-5` (od `--wash-2` do `--bar`) z wariantem ciemnym i dołożyć pasek legendy koloru.
- **Tryb ciemny:** poza macierzą jest spójny; sprawdzić jeszcze `.u-select` (`rgba(31,95,204,0.12)` na sztywno) i pasek `.nr` (`#fff`).

### Typografia

Skala ról już istnieje i ma dobry stosunek (12 / 13 / 14 / 15 / 17 / 22 / 26 / 32, czyli około 1,15). Zmiany: (1) tytuł-wniosek karty (`h3`) ograniczyć do `max-width: 64ch` i dodać `text-wrap: balance` — dziś zdania w rodzaju „Od lutego 2026 nowe osoby płacą rzadziej; poza sesjami…” ciągną się przez 110 znaków w jednym wierszu, co łamie miarę trybu „Read”; (2) `.wniosek` 16/500 zostaje, treść 15, przypis 13; (3) cyfry tabelaryczne są już w tabelach i kafelkach — dodać je także do etykiet osi i legend (`.u-legend .u-value` ma, osie uPlota nie); (4) jedna czcionka systemowa bez zmian.

### Układ i siatka

- Rytm: `h2` + wstęp → karta nagłówka → panel filtrów → karty danych → cicha karta „Jak liczymy”. Działa, ale wszędzie jest 14 px, więc test zmrużonych oczu pokazuje jednolitą drabinkę kart. Skala odstępów 8 / 12 / 16 / 24 / 32: 12 px wewnątrz karty, 16 px między kartami tej samej grupy, 24 px przed panelem filtrów i przed cichą kartą.
- Karty tekstowe rozciągają się do 1320 px, a tekst kończy się na 860–900 px; prawa trzecia karty jest pusta. Na ekranach ≥1100 px wewnętrzna siatka `minmax(0,1fr) 360px`: po lewej wniosek i punkty, po prawej zastrzeżenie, „Zobacz w danych” i mały wykres z tej karty (np. hantle powrotu). To dwie kolumny tej samej karty, nie karty w kartach.
- Co zostaje kartą: karta nagłówka zakładki, każda karta z wykresem lub tabelą, karta zdarzenia, karta pozycji priorytetu. Co nie jest kartą: panel filtrów chipów w „Zdarzeniach” (wchodzi do karty osi jako jej nagłówek), oś zdarzeń i lista zdarzeń (oś plus karty zdarzeń = jedna grupa, bez osobnej karty-ramki na samą oś). Kafelki, pasek priorytetu i zastrzeżenie zostają szarymi panelami bez cienia — to dopuszczalna druga warstwa, nie karta.
- Szerokie tabele: pierwsza kolumna przyklejona (`position: sticky; left: 0`) i cień na krawędzi przewijania. Dziś tabela kohort obcina kolumnę „Marża na pacjenta, 180 dni” już przy 1366 px, a na telefonie przewijając w prawo traci się nazwę wiersza.

### Komponenty

- **Znacznik stanu:** bez zmian (ikona + słowo + kolor). Dodać wariant „Do naprawy / Do sprawdzenia / Czyste” jako ten sam komponent — już tak jest w lejku.
- **Etykieta zmiany:** bez zmian; w nowych wykresach ta sama etykieta pojawia się przy hantlu jako podpis różnicy.
- **Kafelek:** zostaje tylko w werdykcie (trzy kafelki Kuby). Nie mnożyć go w innych zakładkach.
- **Legenda:** zastąpić domyślną legendę uPlota własną: chipy z kreską w kolorze serii i nazwą, wartość pod kursorem w tym samym chipie, bez „Dzień: —” jako serii (data pod kursorem idzie do nagłówka legendy). Czyste CSS i opcja `legend.markers`, bez nowej biblioteki.
- **Podpowiedź na wykresie:** w uPlocie legenda żywa pełni tę rolę; w wykresach SVG (kroki lejka, hantle, mostek, oś zdarzeń) jeden wspólny element `div.podpowiedz` pozycjonowany przy wskazanym elemencie, pokazywany na `mouseenter` i `focus` (dziś `title` nie działa na dotyku ani z klawiatury).
- **Panel filtrów:** dwa poziomy. „Główne” (porównanie, okresy, podział na serie) zawsze widoczne; „Zawęź” (filtry wartości) zwinięte z licznikiem aktywnych, a aktywne filtry pokazane jako chipy z krzyżykiem. Dotyczy kohort (14 list) i w mniejszym stopniu lejka.
- **Tabela:** nagłówki bez skrótów „B (A)”: gdy wybrany jest preset, nazwy okresów („Ostatnie 12 mies.”, pod spodem „rok wcześniej”), litery A/B tylko przy własnych datach — jak już zrobiono w tytule wykresu kroków. Komórki z udziałem dostają pasek danych w tle (szerokość = wartość). To pasek kodujący wartość komórki, a nie sparkline-ozdoba.
- **Odnośniki „Zobacz w danych”:** zostają listą; mała ikona zakładki docelowej przed każdym.
- **Sekcje zwijane:** dwa napisy zamiast trzech: „Szczegóły i źródło liczb” oraz „Jak liczymy”.

### Nawigacja

- Komputer: 9 zakładek zostaje, z dwoma cienkimi separatorami: [Czy to wzrost] | Kohorty · Lejek · Po zakupie · Zdarzenia · Wynik biznesu · Jakość danych | Priorytety · Czego nie wiemy (odpowiedź / dane / decyzje).
- Na dole każdej zakładki wiersz „Dalej: Kohorty →”, żeby osoba czytająca raz szła ścieżką bez wracania do paska.
- Telefon: pigułki w trzech rzędach zostają; dodać przycisk „Zakładki ↑” po przewinięciu, bo pasek nie jest przyklejony.

## C. Zakładka po zakładce

Skrót w kolumnie „z jakich danych”: **P** = w przeglądarce z istniejących danych, **E** = wymaga eksportu.

### 1. Czy to wzrost

| element | dziś | propozycja | dane | dlaczego czytelniej | wysiłek |
|---|---|---|---|---|---|
| Werdykt, kafelki, decyzje | duży znacznik, 3 kafelki, 4 decyzje | bez zmian w treści; kafelek dostaje jednolitą wysokość i dopisek na dole | — | już działa; nie dokładać | S |
| Karta „Lepsza retencja”: tabela 4 okien | tabela 4×3 z etykietą zmiany | **hantle**: 4 wiersze (30/60/90/180 dni), punkt szary = rok wcześniej, punkt niebieski = ostatnie 12 mies., między nimi etykieta „−6,5 pkt proc.”; tabela zostaje w „Szczegółach” | P: `podsumowanie.js` `wzrost.retencja.okna` (30/60/90, liczby); 180 dni — E (dopisać do `okna`) | spadek w każdym oknie i jego wielkość widać bez czytania ośmiu liczb | S |
| Karta „Więcej pacjentów” | 3 punkty | pod wnioskiem jeden **pasek-licznik** 100%: „nowe kampanie na L4 29% / pozostałe 71%” z liczbami 7 268 / 17 419 | E: dwie liczby do karty (`liczba`, `udzial`) | „głównie z dwóch kampanii” staje się obrazem | S |
| Karta TelemediGO: kolumna „Udział we wzroście” | tabela 4×5 | pod tabelą jeden **słupek skumulowany** 26 / 41 / 33 (trzy części, nazwy obok) | P: komórki tabeli w `c.js` (wartości „26%”) albo E dla czystych liczb | części całości ≤3, słupek zamiast koła | S |
| Karta kwartałów: tabela zmian r/r | tabela 4×3 z etykietami | **słupki parami** na kwartał: wydatki r/r (bursztyn) obok marży przed kampaniami r/r (niebieski), nad słupkiem wartość; tabela w „Szczegółach” | E: 8 liczb numerycznych (dziś są tekstem „+55,2%”) | „wydatki rosną szybciej niż marża” to jedna para słupków rosnąca i druga malejąca | S |
| Karta „Dashboard pokazuje więcej…”: mostek | tabela 4×4 | **mostek-schodki** dla zamówień i przychodu: od słupka „+60,7%” przez „bez duplikatów”, „bez testów”, „po zwrotach” do „+55,7%” i „+44,8%”; tabela zostaje | P: `jakosc.js` `mostek.kroki` (liczby) | ile zawyża dashboard i który krok — jeden rzut oka | M |
| Ostatnia karta (odnośniki) | cicha karta | zostaje; dodać wiersz „Dalej: Kohorty →” | — | ścieżka czytania | S |

### 2. Kohorty

| element | dziś | propozycja | dane | dlaczego czytelniej | wysiłek |
|---|---|---|---|---|---|
| Karta nagłówka | tekst | w prawej kolumnie te same hantle powrotu co w zakładce 1 (jeden komponent) | P (jak wyżej) | spójność; liczba z wniosku ma obraz | S |
| Panel filtrów | 14 list w ścianie | „Główne”: przypisanie, podział na serie, porównanie, okresy; „Zawęź pacjentów (0)” zwinięte, aktywne filtry jako chipy | P | ściana opcji znika; codzienny użytkownik widzi, co jest zawężone | M |
| Tabela „Kohorty w podziale” | 10 kolumn, obcina się | nagłówki okresów słowami; pasek danych w „Udział”; pierwsza kolumna przyklejona; kolumny „60 dni” i „Marża 180” domyślnie schowane za „Więcej kolumn” | P | mieści się w 1366 px; udziały widać bez czytania | S |
| Wykres „Dzień po dniu” | 3 linie równej wagi, 14 numerów zdarzeń | seria „Wszyscy w filtrze” w kolorze `--ink` grubości 2,5 px, podziały cieńsze w kolorach; **podpisy na końcu linii** zamiast tylko legendy; linie zdarzeń domyślnie tylko z obszaru „Retencja” (przełącznik „wszystkie zdarzenia”); na telefonie numery ukryte, linie zostają | P (`zdarzenia.js` ma `obszar`) | wyróżnienie jednej serii, mniej szumu | M |
| Macierz kohort | mapa ciepła, skala per kolumna, kolumna „Zdarzenia” prawie pusta | pasek legendy koloru nad macierzą („jaśniej = niższy powrót w kolumnie, skala 5–95 percentyl”); kolumna „Zdarzenia” → mały znacznik przy dacie kohorty z podpowiedzią; nagłówek przyklejony; tokeny koloru | P | legenda mapy ciepła to warunek czytelności; mniej pustych kolumn | S |
| Krzywa powrotu | 2 linie | podpis na końcu każdej linii („rok wcześniej 27,5%”, „ostatnie 12 mies. 22,2%”), pionowe prowadnice w dniach 30/60/90/180 | P | odczyt bez kursora | S |

### 3. Lejek

| element | dziś | propozycja | dane | dlaczego czytelniej | wysiłek |
|---|---|---|---|---|---|
| Karta nagłówka | tekst + zwijana sekcja | w prawej kolumnie **mały wykres skumulowany 100%** udziału sesji nowych kampanii w sesjach nowych osób miesiąc po miesiącu (10% → 47%) | P: `lejek_kampania.js` (sumy `s` dla `nowe_kampanie` vs reszta, `pacjent = nie_kupowal`) | „zmiana ruchu” jest obrazem, nie zdaniem | M |
| Karta Safari (Do naprawy) | tekst | **hantel przed → po**: Safari na iOS 66% → 46% i pod nim „pozostałe przeglądarki 65% → 63%” | P: `podsumowanie.js` `lejek_naglowek.safari` (`przed_proc`, `po60_proc`, `reszta_*`) | kontrast awarii wobec reszty w jednym spojrzeniu | S |
| Karta przeglądarek w aplikacjach (Do sprawdzenia) | tekst | hantle dla 3 kampanii: w aplikacji vs zwykła (remarketing −12,2; marka −5,1; bezpośrednie −4,4 pkt) | E: 6 liczb do karty | różnica 4–12 pkt staje się widoczna i porównywalna | S |
| Wykres kroków lejka | dobry | zostaje; w podpowiedzi dodać „ubyło N sesji wobec kroku wyżej”; przy „Pokaż dla” wartość inna niż „Razem” rysować drugi, cienki szary zestaw kresek dla „Razem” jako odniesienie | P | jedna wartość podziału wobec całości bez przełączania | S |
| Tabela „w podziale” | 9 kolumn, obcina się | jak w kohortach: nazwy okresów, pasek danych w „Udział w sesjach”, przyklejona pierwsza kolumna | P | mix przeglądarek widać od razu | S |
| Wykres „Dzień po dniu” | 5 linii, szum przy 7 dniach, etykieta „%” obrócona | usunąć etykietę osi (jednostka jest w podziałce); domyślne wygładzenie 28 dni dla odsetków, 7 dla „sesje dziennie”; linie zdarzeń tylko z obszaru „Lejek”; podpisy na końcu linii; przy ≥5 seriach przełącznik „małe wielokrotności” (siatka 2×3 małych wykresów, wspólna oś Y) | P | mniej szumu, serie nie nakładają się | M |
| Legenda zdarzeń pod wykresem | 14 pozycji w 2 kolumnach | zostaje, ale tylko dla widocznych zdarzeń (po filtrze obszaru) | P | spójność z wykresem | S |

### 4. Po zakupie

| element | dziś | propozycja | dane | dlaczego czytelniej | wysiłek |
|---|---|---|---|---|---|
| Wykres punktualności (4 pory) | 4 linie równej wagi | wyróżnienie: wybrana pora (domyślnie „Rano”) w `--series-1`, pozostałe w `--axis` cieńsze; pole „Wyróżnij porę” w filtrach karty | P | wniosek jest o poranku; reszta to tło | S |
| Tabela godzin (24 wiersze × 5) | tabela | **słupki według godziny**: internista rok wcześniej (szary) i ostatnie 12 mies. (niebieski) obok siebie, blok 5:00–13:59 podcieniowany; tabela w „Szczegółach” | E: liczby (dziś komórki to tekst „45,3% (865)”) | blok poranny widać jako kształt, nie trzeba skanować 24 wierszy | M |
| Tabela „ten sam poranny ruch” | 5 wierszy A/B | hantle per przedział ruchu | P: `po_zakupie.ruch` (liczby) | „przy tym samym ruchu więcej opóźnień” to pięć równoległych hantli w tę samą stronę | S |
| Tabela powrotu wg opóźnienia | 5 wierszy | poziome słupki powrotu w 90 dniach dla 5 koszyków (tylko ostatnie 12 mies.; rok wcześniej jako szara kreska) | P (liczone w przeglądarce z `kohorty.js`) | „spada z każdym przedziałem” = malejąca drabinka | S |
| Wykres zwrotów (4 cele) | 4 linie | wyróżnienie serii L4, reszta szara; filtry bez zmian | P | wniosek jest o L4 | S |
| Tabela ocen | 4 wiersze | słupek skumulowany „oceny 1–2 / 3 / 4–5” per koszyk opóźnienia | E (dziś tylko `niskie` i `suma`; brak rozkładu) — alternatywa P: słupek „odsetek ocen 1–2” | 32% wobec 1% widać jako długość | S |

### 5. Zdarzenia

| element | dziś | propozycja | dane | dlaczego czytelniej | wysiłek |
|---|---|---|---|---|---|
| Chipy obszarów | osobna karta | wchodzą do nagłówka karty osi jako jej legenda-filtr | P | mniej pudełek | S |
| Oś zdarzeń (SVG) | kropki z numerami, kolizje „3 5”, „6 7”; na telefonie nieczytelna | kształt według `rodzaj`: koło = start kampanii, kwadrat = awaria / błąd danych, romb = zmiana wykryta, pasek = zakres; numery w pigułkach z przesunięciem przy kolizji; podpowiedź z tytułem; na telefonie zamiast SVG **pionowa oś**: lista dat z kropką na lewej linii | P | typ zdarzenia widać bez czytania; telefon dostaje czytelną formę | M |
| Karty zdarzeń | data, obszar, rodzaj, 3 pola | zostają; dla zdarzeń z wpisem w `wykryte` mały hantel „przed → po” (np. 33,7% → 30,6%) w nagłówku karty | P: `zdarzenia.wykryte` (`przed`, `po`) tam, gdzie jest dopasowanie po dacie i wartości | „o ile” ma obraz | M |
| Tabela wykrytych (245 wierszy) | zwijana | dodać sortowanie po kolumnie „Zmiana” i filtr rodzaju | P | surowy wynik metody staje się przeszukiwalny | S |

### 6. Wynik biznesu

| element | dziś | propozycja | dane | dlaczego czytelniej | wysiłek |
|---|---|---|---|---|---|
| Wykres 4 linii (przychód, koszt lekarza, kampanie, marża) | 4 linie z punktami | **słupki skumulowane miesięczne**: koszt lekarza + kampanie i prowizja + marża = przychód (trzy części), marża na górze w kolorze, koszty szare; linia przychodu zbędna, bo to suma | P: `wynik.js` `serie` | widać, że kampanie zjadają rosnącą część przychodu | M |
| Kwartały rok do roku | tabela 4×5 z etykietami | nad tabelą **słupki parami** (marża r/r, wydatki r/r) dla 4 kwartałów; tabela zostaje | P (sumy kwartalne liczone już w `rysujKwartaly`) | ta sama forma co w zakładce 1 | S |
| Miesiące i sumy (24 wiersze × 10) | tabela w karcie | do „Szczegółów” (zwinięta) z wierszami sum na wierzchu | P | gęstość tam, gdzie jest potrzebna | S |
| Ekonomia kampanii (9 kolumn) | tabela | **hantle koszt → marża** per grupa/kampania: szary punkt koszt pozyskania, niebieski marża, odcinek zielony (wynik dodatni) albo czerwony z ikoną (ujemny); dwa wiersze na pozycję: „według pierwszego wejścia” i „według sesji z płatnością”; przełącznik 90/180 dni; tabela w „Szczegółach” | P: `wynik.ekonomia.wiersze` (`cac`, `marza`, `wynik`, `od`, `do`) | znak i wielkość wyniku oraz zależność od reguły widać jako kierunek odcinka | M |

### 7. Jakość danych

| element | dziś | propozycja | dane | dlaczego czytelniej | wysiłek |
|---|---|---|---|---|---|
| Mostek | tabela | ten sam komponent mostka co w zakładce 1 (tu w pełnej wersji: 4 miary) | P: `jakosc.mostek` | mostek to z natury wykres schodkowy | M (wspólne z 1) |
| Duplikaty (linia + słupki) | dobry | podcieniować okno 10–24.06 i podpisać „604 kopie”; legenda własna | P | okno widać od razu | S |
| Testy kwartalne | słupki poziome | zostają; dodać cienką kreskę „rok wcześniej” i nagłówek osi w jednym wierszu | P | bez zmian w formie | S |
| Godzina / drobne / czyste | listy | „Sprawdzone i czyste” jako lista ze znacznikiem „Czyste” (ikona + słowo) przy każdym punkcie | P | status widać, nie czyta się | S |

### 8. Priorytety

| element | dziś | propozycja | dane | dlaczego czytelniej | wysiłek |
|---|---|---|---|---|---|
| Przegląd (tabela 12×5) | dobra | zostaje; kwoty z `tabular-nums` i wyrównane do prawej w kolumnie; pewność bez zmian; wiersze 1–2 / 3–4 / 5–10 / 11–12 rozdzielone cienkimi separatorami z podpisem grupy („pewne straty”, „pauzy”, „naprawy i testy z wyceną”, „bez wyceny”) | E: podpisy grup (tekst zasad już to mówi) | kolejność niesie informację, więc numery i grupy są uzasadnione | S |
| Wykres wartości pozycji | brak | **nie robić** (punkt F): kwoty są scenariuszami o różnych horyzontach („0 albo 38”, „od −31 do +180”, „23,6 za każdy punkt”); słupki sugerowałyby sumowalność | — | — | — |
| Karty pozycji | pasek + dl | zostają; w karcie 1 (Safari) hantel 66% → 46% (ten sam komponent co w lejku); w kartach 3, 4, 9 tabela kampanii dostaje pasek danych w komórkach wyniku (zielony/czerwony odcinek od zera) | P / komórki tabel w `c.js` | kierunek wyniku widać bez czytania czterech kolumn | S |
| Telefon | tabela → karty | dobre; dodać spis „1–12” jako pigułki u góry do skoku | P | nawigacja w długiej liście | S |

### 9. Czego nie wiemy

| element | dziś | propozycja | dane | dlaczego czytelniej | wysiłek |
|---|---|---|---|---|---|
| Tabela 21×5 | długie komórki | zostaje; kolumna „Pozycja” jako znacznik-odnośnik „poz. 9” (neutralny) albo „—” jako „bez pozycji”; nagłówek przyklejony; wiersze z pozycją i bez pozycji oddzielone separatorem | P | 14 z 21 ma test na liście; widać to w sekundę | S |
| Powiązanie z priorytetami | odnośniki | w kartach priorytetów symetryczny odnośnik „Niewiadome: 1, 3” (już częściowo jest) | P | most pamięci w obie strony | S |

## D. Wykresy kołowe, infografiki i inne formy

- **Wykresy kołowe: zero w całym produkcie.** Jedyne „części całości” to: udział nowych kampanii w nowych pacjentach (2 części → pasek-licznik), udział typów zakupu TelemediGO we wzroście (3 części → jeden słupek skumulowany), mix przeglądarek (9 kategorii, bliskie wartości → słupki poziome z paskiem danych w tabeli). Koło przegrywa z każdą z tych form, a mix źródeł z dziewięcioma kategoriami to wprost przypadek zakazany.
- **Mostek (wodospad):** tak, dla „dashboard → dane oczyszczone” (4 kroki, liczby w `jakosc.mostek`). Nie dla „rozkładu spadku III kwartału” (−15,1 tys. zł na cztery składniki) — to rozkład księgowy, który tekst sam nazywa „nie zmierzonym wpływem”; wykres nadałby mu pewność, której nie ma. Zostaje w „Szczegółach” jako tekst.
- **Hantle (rok do roku):** główna forma tego projektu, bo prawie każdy wniosek to „A wobec B na element”: powrót w oknach, Safari przed/po, przeglądarki w aplikacjach, poranny ruch, koszt → marża w ekonomii kampanii. Jeden komponent SVG (`hantel(wiersze, {a, b, jednostka})`) obsłuży wszystkie.
- **Małe wielokrotności:** jako przełącznik dla wykresów dziennych przy ≥5 seriach (lejek według kampanii, kohorty według źródła). Wspólna oś Y, 2×3 albo 3×3, 160 px wysokości każdy, zdarzenia tylko z obszaru.
- **Mapa ciepła kohort:** już jest; wymaga legendy koloru i tokenów. Skala per kolumna (percentyle) jest dobrą decyzją dla szukania zmian w czasie, ale musi być nazwana w legendzie.
- **Skumulowany udział w czasie:** jedna, najważniejsza instancja — skład sesji nowych osób (nowe kampanie na L4 / pozostałe, miesięcznie). To obraz zdania „spadek zaczyna się, gdy ruch z nowych kampanii przekracza 30% sesji”. Drugą (udział przeglądarek w aplikacjach 10,7% → 35,6%) pokazać tą samą formą jako opcję w „Dzień po dniu”.
- **Oś czasu zdarzeń:** zostaje jako główny widok zakładki; na telefonie wersja pionowa. Dodatkowo: na każdym wykresie dziennym zamiast 14 pionowych linii pasek zdarzeń pod osią X (małe znaczniki z numerem, tylko z obszaru wykresu), żeby linie nie przecinały serii.
- **Sankey lejka: nie.** Lejek ma pięć kolejnych kroków bez rozgałęzień; wykres kroków z paskami już pokazuje to lepiej, a Sankey dodałby tylko wstęgi i błędne wrażenie przepływów między kanałami.
- **Infografika „jak to działa”:** jedna, prosta, w README (punkt E), nie na stronie.

## E. Pozostałe elementy oddawane

- **README na GitHubie:** (1) na górze jeden zrzut zakładki „Czy to wzrost” przy 1366 px, generowany skryptem `e_przegladarka.py` przy każdym eksporcie (zrzut w repozytorium, bez pobierania z sieci; data i commit w podpisie, żeby nie rozjechał się z danymi); (2) diagram Mermaid `flowchart LR` przepływu bez liczb: paczka CSV → kontrola bezpieczeństwa → baza (a1, a2) → analizy (a3–a5) → eksport (b) → strona; GitHub renderuje go bez żadnych zależności; (3) tabela zakładek zostaje; (4) lista „co robimy w pierwszym tygodniu” zostaje jako lista numerowana — nie robić z niej grafiki. Nie dodawać do README wykresów z liczbami, bo nie przechodzą kontroli zgodności.
- **Lista priorytetów:** tabela przeglądu jest właściwą formą; dodać separatory grup i pigułki 1–12 do skoku. Żadnego wykresu kwot (punkt F).
- **„Czego nie wiemy”:** tabela zostaje; znacznik „poz. N” / „bez pozycji” i separator. Na telefonie forma kart z podpisami pól jest dobra.

## F. Czego nie robić

1. **Nie budować „dashboardu dla ozdoby”:** żadnych nowych rzędów kafelków poza trzema w werdykcie, żadnych pierścieni postępu, żadnych sparkline’ów w wierszach tabel. Pasek danych w komórce jest dopuszczalny tylko wtedy, gdy koduje wartość tej komórki.
2. **Nie rysować wykresu kwot priorytetów.** Kwoty mają różne horyzonty, część to „0 albo X”, część to przedział z ujemnym końcem, pozycja 12 to koszt testu, a pozycja 7 to stawka za punkt procentowy. Słupki sugerują sumowalność i porównywalność, których tekst wprost odmawia („kwot nie sumujemy”).
3. **Nie rysować rozkładów księgowych jako wodospadów** (spadek III kwartału, „71% spadku powrotu”). Tekst nazywa je opisem bez pomiaru wpływu; wykres podniósłby je do rangi wyniku.
4. **Nie zmieniać domyślnej rozdzielczości kohort na tygodniową.** Zadanie wymaga dziennej; tygodnie zostają opcją.
5. **Nie używać dwóch osi Y** (np. przychód w złotych i odsetek na jednym wykresie) ani koła.
6. **Nie przenosić stanu w samym kolorze:** hantle i mostek dostają etykietę zmiany z ikoną i słowem, odcinek ujemny w ekonomii kampanii ma ikonę „źle” i znak minus.
7. **Nie dopisywać liczb w warstwie graficznej.** Wszystkie nowe wykresy liczą się z istniejących kluczy (oznaczone P) albo czekają na eksport (E); podpisy na wykresach to te same liczby, które stoją w tekście. Nie wymyślać podpisów grup ani tytułów bez eksportu.
8. **Nie usuwać tabel po dodaniu wykresów** — tabela zostaje w „Szczegółach” jako widok zapasowy i dostępnościowy; każdy SVG dostaje `role="img"` i `aria-label` z wnioskiem.
9. **Nie dokładać biblioteki.** Hantle, mostek, słupki parami, oś pionowa i skumulowany udział to kilkadziesiąt linii SVG; uPlot zostaje do serii dziennych.
10. **Nie zostawiać kolorów wpisanych na sztywno** (`RAMPA`, `#fff`, `rgba` w `.u-select`) — każdy nowy wykres czyta kolory wyłącznie z tokenów, inaczej tryb ciemny się rozjedzie.

## G. Dziesięć najważniejszych zmian (wartość ÷ wysiłek)

1. **Komponent hantli A → B** i użycie go w czterech miejscach: powrót w oknach (zakładki 1 i 2), Safari przed/po (lejek, priorytet 1), poranny ruch (po zakupie), ekonomia kampanii koszt → marża (wynik). S na komponent, S–M na wdrożenia; w przeglądarce (180 dni powrotu: wymaga eksportu).
2. **Porządek na wykresach dziennych:** własna legenda-chipy, bez obróconej etykiety osi, linie zdarzeń tylko z obszaru wykresu, numery ukryte na telefonie, podpisy na końcu linii. S–M; w przeglądarce.
3. **Wyróżnienie jednej serii** (kohorty: „Wszyscy w filtrze” w kolorze `--ink`; punktualność: pora „Rano”; zwroty: L4), reszta cieńsza i szara. S; w przeglądarce.
4. **Mostek-schodki dashboard → dane oczyszczone** w zakładkach 1 i 7 z `jakosc.mostek`. M; w przeglądarce.
5. **Tabele szerokie:** nazwy okresów zamiast „B (A)”, przyklejona pierwsza kolumna, pasek danych w kolumnach udziału, kolumny drugorzędne za „Więcej kolumn”. S; w przeglądarce.
6. **Panel filtrów kohort** w dwóch poziomach z chipami aktywnych filtrów. M; w przeglądarce.
7. **Słupki skumulowane miesięczne w „Wyniku biznesu”** (koszt lekarza, kampanie, marża = przychód) zamiast czterech linii, plus słupki parami r/r dla kwartałów (ta sama forma w zakładce 1). M; w przeglądarce (zakładka 1: wymaga eksportu ośmiu liczb).
8. **Skład sesji nowych osób w czasie** (skumulowany 100%: nowe kampanie na L4 / pozostałe) w nagłówku lejka. M; w przeglądarce z `lejek_kampania.js`.
9. **Oś zdarzeń:** kształty według rodzaju, pigułki numerów bez kolizji, chipy obszarów w nagłówku karty, wersja pionowa na telefonie. M; w przeglądarce.
10. **Legenda koloru i tokeny mapy ciepła kohort** oraz usunięcie kolorów wpisanych na sztywno (tryb ciemny). S; w przeglądarce.

Poza dziesiątką, tanie: separatory i „Dalej →” w nawigacji (S), paleta serii bez `#008300` i czerwieni (S), słupki godzin opóźnień (M, wymaga eksportu).
