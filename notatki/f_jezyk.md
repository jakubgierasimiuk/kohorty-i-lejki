# F, część 3 — język w tekstach zmienionych od rana (kontrola przed publikacją, 2026-10-22)

**Założenie o zakresie (od sesji prowadzącej):** „od rana” to od wersji `ccc3c61` (22.10.2026, godz. 00:31), którą Kuba przeglądał rano. Sprawdzone jest wszystko, co zobaczy Telemedi, a co zmieniło się między `ccc3c61` a `HEAD` (`a4d52c9`, 22.10.2026, godz. 22:46): teksty kart, podpisy wykresów, legendy, objaśnienia, etykiety filtrów i przycisków, podpowiedzi po najechaniu, napisy widoczne tylko na telefonie i README. Tekstów, które od rana się nie zmieniły, ta kontrola nie ocenia (słowa Kuby: „Całości drugi raz nie przepisujemy”). Wyjątek: dwa miejsca sprzed rana, które powtarzają dokładnie ten sam błąd co nowy tekst, są dopisane „przy okazji”.

## Wynik w skrócie

**Przed wysłaniem warto poprawić 12 miejsc. Żadne z nich nie zmienia odpowiedzi na pytanie z zadania. Cztery mogą wprowadzić czytelnika w błąd (P1–P4), w tym jeden podpis wykresu niezgodny z tytułem karty (P2).**

- **Sprawdzone miejsca: 890.** 690 to zmienione albo nowe linie w zrzucie tekstów strony: 524 zdania, nagłówki, podpisy i etykiety oraz 166 wierszy tabel. 185 to nowe napisy w kodzie strony: podpowiedzi po najechaniu, etykiety dla czytników ekranu, przyciski i napisy na telefonie (część z nich to te same teksty co w zrzucie). 15 to zmienione miejsca w README.
- **Waga „przed wysłaniem”: 12 poprawek.** Siedem to zmiana tekstu w kodzie tekstów i w szkicach kontroli liczb (P1, P3, P4, P6, P8, P9, P12). Cztery to kod strony (P5, P7, P10, P11). Jedna to pole w eksporcie (P2). Trzy są oznaczone osobno, bo zmieniają sens zdania albo dotykają liczby (P1, P4, P7).
- **Waga „materiał na rozmowę”: 35 uwag** (słownik, zdania do wygładzenia, powtórzenia, README, podpisy na wykresach).
- **Poza językiem: 4 uwagi** do przekazania sesji prowadzącej albo technicznej (zrzut tekstów w repozytorium, stopka, okna na wykresie Safari).
- **Rozwidlenie dla Kuby:** jeśli stosować ściśle zasadę „poprawiamy tylko to, co zmienia odpowiedź”, żadna poprawka jej nie spełnia. Jeśli liczy się też to, czy Telemedi nie przeczyta czegoś błędnie, minimum to P1–P4. Pozostałe osiem to drobne błędy języka, każdy do poprawy w jednym miejscu.

## Jak sprawdzone

- Obie wersje strony (`ccc3c61` i `HEAD`) rozpakowane z gita (`git archive`) do katalogu roboczego poza projektem, bo kontrola techniczna w tym czasie nadpisywała `narzedzie/dane_strony/`. Z każdej wersji odtworzony zrzut tekstów skryptem `analiza/b2_teksty_strony.py` (Edge bez okna, tylko 127.0.0.1) i oba zrzuty porównane linia po linii. Poranny zrzut jest identyczny z zapisanym w `ccc3c61`.
- Kod strony: nowe napisy w `app.js`, `widoki.js`, `widoki_c.js`, `karty.js` i `index.html` wobec `ccc3c61`. Na wyrenderowanej stronie: podpowiedzi i etykiety dla czytników ekranu na 9 zakładkach, napisy widoczne tylko przy 375 px, numery zdarzeń pod wykresami i zrzuty ekranu kart z nowymi wykresami na sześciu zakładkach.
- README: zmiany od `ccc3c61`.
- Eksport nie był uruchamiany. Poza tą notatką pliki projektu są bez zmian.
- Każda zmiana tekstu z danych to zmiana w kodzie tekstów i w szkicu (`notatki/e_teksty.md`, `notatki/e_teksty_zakladki.md`), zgodnie z zasadą z `PRZEKAZANIE.md`. Kontrola liczb porównuje tylko liczby, więc same słowa jej nie zepsują, ale szkic ma zostać zgodny z tekstem.

## 1. Poprawki „przed wysłaniem” (od najważniejszej)

### P1. „Czy to wzrost” → karta „Więcej pacjentów”, trzeci punkt pod wykresem

- **Obecnie:** „Z kanałów bezpłatnych (wejścia bezpośrednie, bezpłatna wyszukiwarka, program poleceń) przybyło 12% nowych pacjentów, licząc według pierwszego wejścia.”
- **Proponowane:** „Nowych pacjentów z kanałów bezpłatnych (wejścia bezpośrednie, bezpłatna wyszukiwarka, program poleceń) jest o 12% więcej niż rok wcześniej, licząc według pierwszego wejścia.”
- **Dlaczego:** zdanie stoi zaraz pod „Te kampanie dały 29% nowych pacjentów” i czyta się jak udział, czyli 12% wszystkich nowych pacjentów. Chodzi o przyrost z 7 069 do 7 924 pacjentów. Kanały bezpłatne dają w rzeczywistości około 32% nowych pacjentów ostatnich 12 miesięcy (7 924 z 24 687), więc obecne zdanie wprowadza w błąd. Rano zdanie było jednoznaczne („przybyło 12%: z 7 069 do 7 924”).
- **Waga:** przed wysłaniem (zdanie mylące, widoczna część karty na pierwszej zakładce).
- **Źródło:** `analiza/e_teksty.py:367`; szkic `notatki/e_teksty.md:40`.
- **Liczby i sens:** liczba bez zmian. **Zmienia sens zdania** na zgodny z liczbą, więc zmiana w kodzie i w szkicu.

### P2. „Po zakupie” → karta „Opóźnienia u internisty skupiają się w jednym porannym bloku od 5:00 do 13:59”, dwa wykresy godzin

- **Obecnie:** wykres podcienia i podpisuje „blok poranny” od 5:00 do 12:59. Słupek godziny 13:00 (5,6% wobec 2,5% rok wcześniej) stoi poza blokiem. Tytuł karty tuż nad wykresem, wniosek („poza blokiem 5:00–13:59”), szczegóły pozycji 6 listy priorytetów i niewiadoma 4 mówią o bloku od 5:00 do 13:59 (założenie 75).
- **Proponowane:** blok na wykresie od 5:00 do 13:59, czyli w eksporcie `"blok": 5 <= h <= 13` zamiast `5 <= h <= 12`. Teksty bez zmian.
- **Dlaczego:** podpis wykresu niezgodny z tytułem karty.
- **Waga:** przed wysłaniem (podpis niezgodny z wykresem).
- **Źródło:** `analiza/b2_eksport_c.py:766` (pole `blok`). Strona rysuje blok z danych (`narzedzie/widoki.js:820–825`); to samo pole podświetla wiersze tabeli godzin.
- **Liczby i sens:** liczby bez zmian. Po eksporcie w zrzucie tekstów i w podpowiedzi przy godzinie 13:00 dochodzi „; blok poranny”.

### P3. „Czy to wzrost” → karta kwartałów oraz „Wynik biznesu” → pierwsza karta: zastrzeżenie

- **Obecnie:** „Spadek marży w III kwartale 2026, o 7% rok do roku, zależy od jednorazowego zdarzenia: …”
- **Proponowane:** „Marża po koszcie lekarza, kampaniach i prowizji spadła w III kwartale 2026 o 7% rok do roku, ale ten spadek zależy od jednorazowego zdarzenia: rok wcześniej we wrześniu ruszyła sprzedaż TelemediGO w newsletterze. Po odjęciu jednorazowej nadwyżki tego startu marża kwartału jest o 1% wyższa niż rok wcześniej.” W „Wyniku biznesu” dalsza część zdania bez zmian („we wrześniu 2025 ruszyła…”).
- **Dlaczego:** w widocznej części karty nic wcześniej nie mówi o spadku, a wykres tuż nad zastrzeżeniem pokazuje marżę przed kosztem kampanii w III kwartale 2026 na plusie (+25,2%). Czytelnik nie wie, która marża spadła. Spadek o 6,8% widać dopiero po rozwinięciu „Tabeli z liczbami” albo „Szczegółów”. Wtrącenie „, o 7% rok do roku,” dodatkowo łamie zdanie.
- **Waga:** przed wysłaniem (zdanie mylące na pierwszej zakładce i w „Wyniku biznesu”).
- **Źródło:** `analiza/e_teksty.py:533`, `analiza/e_teksty_zakladki.py:486`; szkice `notatki/e_teksty.md:84`, `notatki/e_teksty_zakladki.md:136`.
- **Liczby i sens:** liczby bez zmian (7% i 1%).

### P4. „Lejek” → karta nagłówka („Na spadek konwersji nowych osób składają się głównie dwie rzeczy…”), pierwszy punkt

- **Obecnie:** „Do stycznia 2026 nowe osoby płaciły prawie tak samo często jak rok wcześniej. Od lutego 2026, gdy ruszył TikTok na L4, przybywa ruchu z nowych kampanii na L4. Od kwietnia to prawie połowa sesji nowych osób, a te sesje płacą o połowę rzadziej niż pozostałe.”
- **Proponowane:** „Do stycznia 2026 nowe osoby płaciły prawie tak samo często jak rok wcześniej, choć ruchu z nowych kampanii na L4 przybywało już od listopada 2025. W lutym 2026, gdy ruszył TikTok na L4, sesje nowych kampanii przekroczyły 30% ruchu nowych osób, a od kwietnia to prawie połowa. Te sesje płacą o połowę rzadziej niż pozostałe.”
- **Dlaczego:** obecne zdanie sugeruje, że ruch z nowych kampanii zaczął rosnąć w lutym 2026. Wykres udziału na tej samej zakładce pokazuje wzrost od listopada 2025: 10%, 18%, 24% i 32% sesji nowych osób w kolejnych miesiącach. README mówi to dokładniej („spadek zaczyna się w lutym 2026, gdy ruch z nowych kampanii przekracza 30% sesji nowych osób”).
- **Waga:** przed wysłaniem (zdanie niezgodne z wykresem na tej samej zakładce).
- **Źródło:** `analiza/e_teksty.py:1230–1232`; szkic `notatki/e_teksty.md:292`.
- **Liczby i sens:** **dotyka liczby**, bo w widocznym punkcie dochodzi „30%”. Ta liczba jest już w „Szczegółach” tej karty i we fragmencie szkicu `lejek/naglowek`, więc kontrola liczb ją pokryje. Sens zdania zmienia się na zgodny z wykresem.

### P5. „Lejek” → karta „Udział sesji nowych kampanii na L4 w ruchu osób, które jeszcze nie kupowały, miesiąc po miesiącu”, przypis pod wykresem

- **Obecnie:** „Odsetek sesji zwykłych osób, które jeszcze nie kupowały, z kampanii Meta pozyskanie: L4 szybko i TikTok: L4 w 15 minut, w każdym miesiącu kalendarzowym. Wykres nie zależy od podziału, „Kto” ani okresów wybranych w filtrach wyżej.”
- **Proponowane:** „Udział sesji z dwóch nowych kampanii na L4 (Meta i TikTok) w zwykłych sesjach osób, które jeszcze nie kupowały, w każdym miesiącu kalendarzowym. Wykres nie zależy od filtrów „Podział” i „Kto” ani od okresów wybranych wyżej.”
- **Dlaczego:** „zwykłych osób” nic nie znaczy; chodzi o typ sesji „Sesje zwykłe (lejek)”. Nazwy kampanii z dwukropkami w środku zdania utrudniają czytanie, a w tekstach te kampanie nazywamy „dwie nowe kampanie na L4 (Meta i TikTok)”. Nazwy filtrów stoją raz w cudzysłowie, raz bez.
- **Waga:** przed wysłaniem (zdanie niezrozumiałe).
- **Źródło:** kod strony `narzedzie/app.js:810–811`.
- **Liczby i sens:** bez liczb.

### P6. „Wynik biznesu” → pierwsza karta, ostatni akapit treści

- **Obecnie:** „Powtórne zamówienie zostawia mniej marży niż rok wcześniej, bo rośnie udział wizyt ze zniżką TelemediGO: z 34% do 42% powtórnych zamówień.”
- **Proponowane:** „W III kwartale 2026 powtórne zamówienie pacjenta spoza nowych kampanii zostawia mniej marży niż rok wcześniej, bo rośnie udział wizyt ze zniżką TelemediGO: z 34% do 42% powtórnych zamówień.”
- **Dlaczego:** odsetki stoją bez okresu i bez grupy pacjentów, więc można je wziąć za cały rok. Rano okres był („spadła w III kwartale 2026”) i zgubił się przy skracaniu. W „Czy to wzrost” to samo zdanie ma i okres, i grupę.
- **Waga:** przed wysłaniem (liczby bez okresu).
- **Źródło:** `analiza/e_teksty_zakladki.py:481`; szkic `notatki/e_teksty_zakladki.md:135`.
- **Liczby i sens:** liczby bez zmian.

### P7. „Kohorty” → mapa kohort, „Jak czytać”

- **Obecnie:** „Kohorty dzienne mają po około 40 pacjentów, więc ich wartości skaczą z dnia na dzień; …”
- **Proponowane:** „Kohorty dzienne mają po kilkadziesiąt pacjentów, więc ich wartości skaczą z dnia na dzień; …”
- **Dlaczego:** liczba jest wpisana w kod strony, a nie wzięta z danych, i jest za niska. W danych strony dzienna kohorta ma medianę 54 nowych pacjentów: 44 rok wcześniej i 68 w ostatnich 12 miesiącach (policzone z `D.kohorty.d` w `narzedzie/dane_strony/kohorty.js` w wersji `HEAD`). Na stronę trafił szacunek z opisu problemu w poleceniu.
- **Waga:** przed wysłaniem (liczba niezgodna z danymi, widoczna dla Telemedi).
- **Źródło:** `narzedzie/index.html:159`.
- **Liczby i sens:** **dotyka liczby**, bo usuwa liczbę spoza eksportu. Szkiców nie dotyczy.

### P8. „Czy to wzrost” → karta kwartałów, „Szczegóły”, drugi punkt

- **Obecnie:** „Sprzedaż TelemediGO w newsletterze sprzedała w pierwszych 23 dniach 225 członkostw; po odjęciu szacowanej nadwyżki tego startu marża kwartału rośnie o 1,1%.”
- **Proponowane:** „W pierwszych 23 dniach sprzedaży TelemediGO w newsletterze pacjenci kupili 225 członkostw; po odjęciu szacowanej nadwyżki tego startu marża kwartału jest o 1,1% wyższa niż rok wcześniej.”
- **Dlaczego:** „sprzedaż sprzedała” to błąd językowy, a „rośnie o 1,1%” nie mówi, wobec czego.
- **Waga:** przed wysłaniem (błąd językowy widoczny po rozwinięciu szczegółów).
- **Źródło:** `analiza/e_teksty.py:543`; szkic `notatki/e_teksty.md:87`.
- **Przy okazji (tekst sprzed rana):** ten sam błąd w „Wyniku biznesu”, sekcja „III kwartał 2026 bez jednorazowego startu sprzedaży TelemediGO”: „Sprzedaż TelemediGO w newsletterze ruszyła 8.09.2025. W pierwszych 23 dniach sprzedała 225 członkostw, a przy późniejszym tempie (1,26 dziennie) sprzedałaby około 29.” Propozycja: „W pierwszych 23 dniach pacjenci kupili 225 członkostw, a przy późniejszym tempie (1,26 dziennie) kupiliby około 29.” Źródło: `analiza/e_teksty_zakladki.py` (około linii 500), szkic `notatki/e_teksty_zakladki.md:147`.
- **Liczby i sens:** liczby bez zmian.

### P9. Słownik: „podział” i „podziały” w znaczeniu reguły przypisania źródła (szczegóły czterech zakładek, „Czego nie wiemy” i README)

- **Obecnie (około 14 miejsc):** „oba podziały dają ten sam przyrost…”, „ten podział przypisuje innym kanałom”, „Cała różnica między podziałami…”, „w filtrach można wybrać oba podziały”, „ci sami pacjenci, których w retencji oba podziały przypisują różnie”, „różnica między tymi podziałami”, „W ekonomii kampanii pokazujemy oba podziały”, „podział według pierwszego wejścia z definicji przypisuje mu mało pacjentów” (niewiadoma 10), a w README „oba podziały” i „podziałem według sesji z płatnością”.
- **Proponowane:** „obie reguły przypisania”, „ta reguła”, „między regułami”, „reguła pierwszego wejścia”, tak jak w decyzjach na pierwszy tydzień, w pozycjach 3 i 4 („kampania traci według obu reguł przypisania”), w tytule wykresu ekonomii („według dwóch reguł przypisania źródła”) i w README („według obu reguł przypisania”). Nazwy samych reguł zostają: „według pierwszego wejścia” i „według sesji z płatnością”.
- **Dlaczego:** w tych samych „Szczegółach” słowo „podział” znaczy też rozkład spadku („Podział spadku liczymy opisowo”, „podział opisowy”, „Podział zmiany…”) i wymiar filtra („Podział: Przeglądarka”, „Wynik rozkładu zależy od podziału”). W „Kohortach” trzy akapity z rzędu używają go w dwóch znaczeniach. Kuba prosił o jeden słownik w całym narzędziu, a dziś obie reguły mają razem cztery nazwy zbiorcze: reguły, sposoby, podziały i przypisanie źródła.
- **Waga:** przed wysłaniem (zdania mylące w szczegółach). Jeśli ma być minimum, wystarczy zamiana „podziałów” w szczegółach „Kohort”, „Lejka” i karty „Lepsza retencja”.
- **Źródło:** `analiza/e_teksty.py`: zamiany w `REGULY` (linie 174–177) i zdania w liniach 384–385, 440–445 i 1292–1296; `analiza/e_teksty_zakladki.py:152–157` i `601–605`; README, linie 18 i 37; szkice `notatki/e_teksty.md` i `notatki/e_teksty_zakladki.md`.
- **Liczby i sens:** bez liczb, sens bez zmian.

### P10. „Po zakupie” → karta „Przy tym samym porannym ruchu opóźnień jest dużo więcej niż rok wcześniej”, etykieta wiersza wykresu

- **Obecnie:** „21–24 wizyt”.
- **Proponowane:** „21–24 wizyty”. Forma rzeczownika idzie za ostatnią liczbą przedziału (22, 23, 24 wizyty). Pozostałe etykiety tego wykresu są poprawne.
- **Waga:** przed wysłaniem (błąd językowy widoczny dla Telemedi).
- **Źródło:** kod strony `narzedzie/widoki.js:655` (`pz + " wizyt"`). Formę wystarczy wybrać według ostatniej liczby przedziału, tą samą regułą co `odm()` w `analiza/e_teksty.py:306`.
- **Liczby i sens:** bez zmian.

### P11. „Zdarzenia” → objaśnienie pod tabelą wykrytych zmian

- **Obecnie:** „Etykiety zmiany po zmianie wobec okresu przed nią: lepiej, gorzej, bez oceny. Strzałka pokazuje kierunek, …”
- **Proponowane:** „Etykiety zmiany (poziom po wykrytej zmianie wobec poziomu przed nią): lepiej, gorzej, bez oceny. …”
- **Dlaczego:** „zmiany po zmianie” trudno przeczytać za pierwszym razem.
- **Waga:** przed wysłaniem (zdanie niezrozumiałe).
- **Źródło:** kod strony `narzedzie/app.js:1013` (napis przekazywany do objaśnienia); zdanie składa `narzedzie/karty.js:104`.
- **Liczby i sens:** bez liczb.

### P12. „Po zakupie” → karta zwrotów, „Szczegóły”, drugi akapit

- **Obecnie:** „Zwroty po wizycie u pacjentów nowych kampanii w ostatnich 12 miesiącach: 1 044 wizyty we wszystkich celach wizyty, z tego 1 024 przy wizytach L4 (te liczy pozycja 5 listy priorytetów), 84 112 zł …”
- **Proponowane:** „Zwroty po wizycie u pacjentów nowych kampanii w ostatnich 12 miesiącach: 1 044 wizyty we wszystkich celach (w tym 1 024 wizyty L4, które liczy pozycja 5 listy priorytetów), 84 112 zł zwróconych zapłat i 33 975 zł kosztu lekarza.”
- **Dlaczego:** „wizyty … wizyty” to ślad po wstawce i zdanie się nie składa.
- **Waga:** przed wysłaniem (błąd językowy widoczny po rozwinięciu szczegółów).
- **Źródło:** `analiza/e_teksty_zakladki.py:400–402`; szkic `notatki/e_teksty_zakladki.md:110`.
- **Liczby i sens:** liczby bez zmian.

**Kolejność prac po decyzji Kuby (propozycja):** kod tekstów i szkice (P1, P3, P4, P6, P8, P9, P12), kod strony (P5, P7, P10, P11) i pole w eksporcie (P2), potem eksport z kontrolą liczb, odtworzenie tekstów strony i kontrola w przeglądarce.

## 2. Materiał na rozmowę (35 uwag)

### Słownik i nazwy

- **R1. Pozostałe nazwy zbiorcze reguł.** „Oba sposoby przypisania źródła stoją obok siebie” (`narzedzie/index.html:390`), plakietka „Znak zależy od przypisania” i ocena „Niepewny: znak zależy od przypisania źródła” (`narzedzie/widoki.js:1043`, `1056`), „Znak zależy od reguły” (karta ekonomii, `analiza/e_teksty_zakladki.py`), „reguła źródła” (pozycja 9). Po P9 warto ujednolicić do „reguła przypisania”, np. „Obie reguły przypisania stoją obok siebie…”, „Znak zależy od reguły przypisania”.
- **R2. „Podział” jako rozkład spadku i jako wymiar filtra.** W szczegółach „Lejka” stoją obok siebie „Podział zmiany… (opisowo…)” i „Wynik rozkładu zależy od podziału”, w „Kohortach” „Podział spadku liczymy opisowo”, w „Czy to wzrost” „podział opisowy”. W szczegółach można wrócić do „rozkład (opisowo, czyli bez mierzenia wpływu)”; zasady Kuby dopuszczają to słowo w szczegółach z wyjaśnieniem. Źródła: `analiza/e_teksty.py` (karta retencji i lejek), `analiza/e_teksty_zakladki.py` (karta kohort), `analiza/b2_eksport_c.py:664`.
- **R3. „Okres porównania” w dwóch znaczeniach.** W przypisach wykresów dziennych to oba okresy („Szare pola to okresy porównania”). W „Jak czytać” kroków lejka to okres A („spadkiem względnym wobec okresu porównania … Liczby sesji przy krokach są z okresu B”). Propozycja dla kroków lejka: „wobec okresu A” (`narzedzie/index.html:233`).
- **R4. Krzywa powrotu w „Kohortach”.** Tytuł mówi „okres A i okres B”, a wartość w legendzie „…% poziomu A”, podczas gdy linie nazywają się „Rok wcześniej” i „Ostatnie 12 miesięcy”. Propozycja: w tytule „dwa porównywane okresy”, w legendzie „% poziomu roku wcześniej” albo nazwa z wybranego porównania (`narzedzie/index.html`, `narzedzie/widoki.js:297` i `303`).
- **R5. Kroki lejka: podpowiedzi etykiet zmiany** mówią „Spadek o 3,0 wobec okresu A: gorzej”, a obok widać „rok wcześniej: 33,7%”. Propozycja: ta sama nazwa okresu co na wykresie (`narzedzie/app.js:72–75` i wywołanie w wykresie kroków).
- **R6. Tytuł karty Safari w „Lejku”:** „Od 17 marca 2026 nowi pacjenci w Safari na iPhone'ach…”, a reszta zakładki mówi o „nowych osobach”, bo to jeszcze nie są pacjenci. Propozycja: „Od 17 marca 2026 nowe osoby w Safari na iPhone'ach rzadziej kończą zakładanie konta” (`analiza/e_teksty.py`, karta `lejek/safari`).
- **R7. Nazwy kwartałów.** Tabela w karcie kwartałów „Czy to wzrost” ma „IV 2025”, a wykres nad nią i „Wynik biznesu” mają „IV kw. 2025”. Propozycja: wszędzie „IV kw. 2025” (`analiza/e_teksty.py`, tabela kwartałów).
- **R8. Odmiana „Meta”.** Niewiadoma 3: „po wstrzymaniu TikToka dotyczy tylko Meta”, a pozycja 5: „dotyczą tylko Mety”, obok „test Mety”. Propozycja: „dotyczy tylko Mety” (`analiza/e_teksty.py:1060`).

### Zdania do wygładzenia (sens bez zmian)

- **R9. Tytuł karty kwartałów w „Czy to wzrost”:** „Z każdym kwartałem wydatki na kampanie rosną rok do roku szybciej, a marża przed ich kosztem wolniej” → „Wzrost wydatków na kampanie przyspiesza z kwartału na kwartał, a wzrost marży przed ich kosztem zwalnia”. Obecny tytuł jest poprawny, ale trzeba go czytać dwa razy (`analiza/e_teksty.py`, karta `wzrost/wynik`).
- **R10. Tytuł „Wyniku biznesu”:** „Za cały rok marża rośnie, ale wydatki na kampanie rosną szybciej niż marża zarabiana przed ich kosztem” → „Marża za cały rok rośnie, ale wydatki na kampanie rosną szybciej niż marża przed ich kosztem” (`analiza/e_teksty_zakladki.py`).
- **R11. „wracają w 4%”, „płacą w 5,5%”, „wracają w 90 dniach w 3,2%”** („Czy to wzrost”, „Kohorty”, „Lejek”, pozycja 3) → „wraca 4% z nich”, „płatnością kończy się 5,5% z nich”. To skrót z notatek analitycznych; zdania zmieniły się dziś tylko przez zaokrąglenie (`analiza/e_teksty.py`, `analiza/e_teksty_zakladki.py`).
- **R12.** „członkostwa sprzed roku dostały średnio o około 16 zł więcej zniżek” → „średnio około 16 zł więcej zniżek” (`analiza/e_teksty.py:479`).
- **R13.** „Lista priorytetów idzie od najważniejszej pozycji…” → „Lista priorytetów zaczyna się od najważniejszej pozycji…” (`analiza/e_teksty.py:608`).
- **R14.** „Safari trzeba naprawić (pozycja 1 listy priorytetów).” → „Zakładanie konta w Safari trzeba naprawić…”, bo naprawiamy własną stronę, a nie przeglądarkę (`analiza/e_teksty.py:1238`).
- **R15.** „Najmocniej rośnie od 6:00 do 11:59.” → „Odsetek spóźnionych rośnie najmocniej od 6:00 do 11:59.” (`analiza/e_teksty_zakladki.py:267`).
- **R16. Zastrzeżenie karty porannego ruchu:** „To nasze odczytanie danych. Najwcześniejszy termin dnia liczymy…” → „Mechanizmu nie mierzymy: najwcześniejszy termin dnia liczymy dla całej sieci, bo w danych nie ma identyfikatorów lekarzy ani grafików (Czego nie wiemy, punkt 4).” (`analiza/e_teksty_zakladki.py:310`).
- **R17.** „Urządzenie i przeglądarka z sesji z płatnością.” → „Urządzenie i przeglądarka: z sesji, w której pacjent zapłacił.” (`narzedzie/index.html:174`).
- **R18.** „Ocenę dostaje tylko 31% odbytych wizyt, więc oceny pokazują tylko kierunek.” → bez pierwszego „tylko” (`analiza/e_teksty_zakladki.py:428`).
- **R19. Pozycja 5:** „Wariant zasad zwrotów („wizyta zostaje opłacona”) wymaga zmiany zasad zwrotów, nie tylko treści reklamy.” → „Wariant „wizyta zostaje opłacona” wymaga zmiany regulaminu zwrotów, nie tylko treści reklamy.” (`analiza/b2_eksport_c.py:1443` i zamiana nazw wariantów w `analiza/e_teksty.py`).
- **R20. Pozycja 10:** „31,4 tys. zł to scenariusz. Przy osobnej reakcji…” Po usunięciu „a nie górna granica” pierwsze zdanie nic nie mówi. Propozycja: „31,4 tys. zł nie jest górną granicą: przy osobnej reakcji przy każdym zamówieniu wynik mieści się między 10,9 a 35,2 tys. zł.” (`analiza/b2_eksport_c.py:1739`).
- **R21. Pozycja 11, „Po czym poznamy”:** „Wiemy, czy brakujące sesje to ludzie…” czyta się tak, jakbyśmy już wiedzieli. Propozycja: „Po porównaniu wiemy, czy brakujące sesje to ludzie…” (`analiza/e_teksty.py:962`).
- **R22. Pozycja 3, szczegóły:** „Wyłączyć, gdy każdy pacjent przyszedł tylko dzięki kampanii: +11,9 do +30,8 tys. zł…” → układ jak w pozycji 4: „Wyłączyć: +11,9 do +30,8 tys. zł (…), gdy każdy pacjent przyszedł tylko dzięki kampanii, i +82,5 tys. zł (+128,6), gdy wszyscy przyszliby i bez niej.” (`analiza/b2_eksport_c.py:1311`).
- **R23. Niewiadoma 11:** „od X 2024 do I 2025 rosną naraz pora roku i wydatki” → „od X 2024 do I 2025 naraz zmienia się pora roku i rosną wydatki” (`analiza/e_teksty.py:1049`).
- **R24. „Wynik biznesu”, szczegóły ekonomii kampanii:** „W 90 dniach: TikTok na L4 −4,6 zł i −17,8 zł na pacjenta, obie nowe kampanie razem +3,6 zł i −9,4 zł.” Bez nazw reguł czytelnik musi zgadywać kolejność. Propozycja: „TikTok na L4 −4,6 zł na pacjenta według pierwszego wejścia i −17,8 zł według sesji z płatnością…” (`analiza/e_teksty_zakladki.py:595`).
- **R25. „Kohorty”, szczegóły:** „Dlatego opis liczymy według pierwszego wejścia” → „Dlatego wnioski podajemy według pierwszego wejścia” (`analiza/e_teksty_zakladki.py:156`).
- **R26. „Zdarzenia”:** tytuł „Remarketing Meta coraz rzadziej kończy się płatnością…” → „Sesje z remarketingu Meta coraz rzadziej kończą się płatnością…”. Krótka nazwa zdarzenia 11 „Powrót w kampaniach działających w obu latach” nie mówi, co się stało, a od dziś stoi w listach pod wykresami i na osi na telefonie. Propozycja: „Spada powrót w kampaniach działających w obu latach” (`analiza/e_teksty_zakladki.py:820` i `837`).
- **R27. Dwa „a” z rzędu** w README (akapit o źródle pacjenta) i w szczegółach „Czy to wzrost”, „Kohort” i „Wyniku biznesu”: „1 918 weszło z ich reklamy, a zapłaciło w innej sesji, a 163 zapłaciło…” → „1 918 weszło z ich reklamy i zapłaciło w innej sesji, a 163 zapłaciło…”.

### Powtórzenia

- **R28. „Priorytety”, karta zasad:** akapit o kolejności stoi w treści karty i prawie dosłownie w jej „Szczegółach” (`analiza/b2_eksport_c.py:1891`). Wersje różnią się słowami: „dwie pozycje bez oszacowanego efektu” wobec „pozycje bez wyceny”, choć pozycja 11 ma górną granicę wartości. Propozycja: w szczegółach zostawić tylko zdanie o pracy w pierwszym tygodniu.
- **R29. Mapa kohort:** o jednej skali kolorów mówią i przypis nad mapą („Ten sam kolor znaczy w każdej kolumnie to samo”), i „Jak czytać” („Skala koloru jest jedna dla całej macierzy…”). Wystarczy jedno miejsce (`narzedzie/index.html`).

### README

- **R30.** „Powody są dwa.” mówi mocniej niż tytuł karty w „Lejku” („Na spadek … składają się głównie dwie rzeczy”). Propozycja: „Składają się na to głównie dwie rzeczy.” (README, linia 14).

### Podpisy na wykresach

- **R31.** Podpisy na końcach linii są ucinane po 21 znakach: „Marża przed kosztem k…” i „Marża po koszcie leka…” w „Wyniku biznesu”, „Pozostałe kampanie i …” w „Kohortach”. Pełne nazwy są w legendzie pod wykresem. Propozycja: krótsze nazwy na końcach linii albo szerszy margines (`narzedzie/app.js:683`).
- **R32.** Na wykresie dziennym kohort linia zdarzenia przecina napis pola „Ostatnie 12 miesięcy” (`narzedzie/app.js`, kolejność rysowania pól okresów i linii zdarzeń).
- **R33. Podpowiedzi z przedziałami:** „(przedział −14,3 do −10,1)” → „(przedział od −14,3 do −10,1)” przy przeglądarkach w aplikacjach (`narzedzie/app.js`); „Przedział warunkowy −10,7–−8,1 zł” → „od −10,7 do −8,1 zł” przy ekonomii kampanii (`narzedzie/widoki.js`).
- **R34.** Przypis wykresów godzin w „Po zakupie” nie mówi, że to wszyscy pacjenci (to stoi dopiero w szczegółach), a karta wyżej domyślnie pokazuje pacjentów spoza nowych kampanii. Propozycja: dopisać „Wszyscy pacjenci.” (`narzedzie/widoki.js:834`).
- **R35.** Karta ekonomii kampanii: tytuł i wniosek mówią o TikToku, a wykres przy domyślnym poziomie „Grupy kampanii” pokazuje go tylko razem z Metą. Propozycja: domyślnie poziom „Kampanie” albo zdanie w przypisie, że TikToka widać po wybraniu tego poziomu (`narzedzie/widoki.js`).

## 3. Poza językiem (do przekazania)

- **U1.** Zapisany w repozytorium zrzut tekstów `analiza/wyniki/b_teksty_strony.md` powstał ze stanu `63ddc3d`. Od obecnej strony różni się w dwóch liniach: hantel powrotu po 180 dniach pokazuje na stronie −5,2 pkt proc., a w zrzucie −5,3 (zmiana z `87b55b2`). Przed publikacją wystarczy odtworzyć zrzut.
- **U2.** Skrypt `analiza/b2_teksty_strony.py` numeruje listy zdarzeń pod wykresami od 1, bo nie czyta numeru zapisanego w elemencie listy. Strona pokazuje numery z osi zdarzeń (w „Lejku” 2, 4, 8, 9, 12 i 13, w zrzucie 1–6). Strona jest poprawna; myli się tylko zrzut.
- **U3.** Stopka strony: „Liczby przeliczone 2026-10-22 22:16 … (stan repozytorium 329d075)”. Eksport był robiony między commitami, więc po ostatnim eksporcie przed publikacją stopka powinna wskazywać właściwy stan. W tym samym zdaniu data stoi w formacie 2026-10-22 obok dat w formacie 1.10.2024 (tekst sprzed rana).
- **U4.** Wykres Safari w „Lejku” i w pozycji 1: okno „po awarii” to dla Safari 17.03–30.09.2026 (46%), a dla pozostałych przeglądarek 17.03–15.05.2026 (63%). Przypis mówi to wprost, ale porównanie jest niesymetryczne; w tych samych 60 dniach po awarii Safari ma 45%. To sprawa treści i liczb, nie języka (założenie 76).

## 4. Sprawdzone miejsca bez uwag (pokrycie)

- **„Czy to wzrost”:** werdykt, kafelki i decyzje na pierwszy tydzień (zgodne z README), wykres nowych pacjentów (legenda, przypis), hantle powrotu w 30, 60, 90 i 180 dniach, wykres sposobów zakupu TelemediGO, wykres kwartałów (podpis i przypis z definicją marży), schodki dashboardu (etykiety kroków, „bez zmian”, przypis), „Tabela z liczbami” z etykietami „lepiej”, „gorzej” i „uwaga”, ostatnia karta i „Dalej”.
- **„Kohorty”:** wniosek z hantlami, filtry na dwóch poziomach („Przypisanie źródła”, „Zawęź pacjentów (aktywne: N)”, „Usuń zawężenie”), legenda wykresów dziennych („Najedź…”, „Dotknij…”, „+ Dodaj serię”, „Usuń z wykresu”), lista zdarzeń pod wykresem (numery zgodne z osią, sprawdzone na stronie), przełącznik mapy, legenda progów mapy, zdanie nad mapą, tabela na telefonie („Miara w tabeli”, „Pokaż całą tabelę”).
- **„Lejek”:** tytuł i wniosek karty nagłówka, zastrzeżenie, zwijana sekcja o sesjach zalogowanych od wejścia, tabela Safari i pozostałych przeglądarek miesiąc po miesiącu, karta Safari (wniosek, wykres „przed awarią / po awarii”), karta przeglądarek w aplikacjach (wniosek, wykres, przypis „w tych samych warunkach”), wykres kroków (etykieta „Najbardziej obniża płatności”, legenda).
- **„Po zakupie”:** tabele z „rok wcześniej” zamiast liter okresów, filtry „Wyróżnij porę” i „Wyróżnij cel”, wykresy godzin (tytuły, legenda, wspólna skala), karta powrotu według opóźnienia pierwszej wizyty (porównania bez oceny i zdanie, dlaczego), „Tabela z liczbami”.
- **„Zdarzenia”:** legenda kształtów na osi, sekcje „Skąd wiemy”, nowe opisy metody, karta awarii Safari, karta duplikatów.
- **„Wynik biznesu”:** dwa wykresy (tytuły i przypis „Obie linie w złotych, na jednej osi”), tabela kwartałów (słowo „uwaga” przy wydatkach, koszt lekarza bez oceny), wykres ekonomii kampanii (symbole reguł, plakietka, przypis o zerze, przełącznik okna i komunikat przy 180 dniach), nagłówki tabeli ekonomii.
- **„Jakość danych”:** schodki, wykres duplikatów („Okno duplikatów”), zastrzeżenie o wizytach testowych z kwotą za dwa lata i za ostatnie 12 miesięcy.
- **„Priorytety”:** pigułki „Przejdź do pozycji”, grupy w przeglądzie, nowe opisy pewności, wdrożenie pozycji 1, decyzje w formie poleceń w pozycji 2, tabele pozycji 3, 4 i 9 z wariantami nazwanymi słowami, próg i reguła decyzji testu Mety, odnośniki „Czego nie wiemy: punkt …”.
- **„Czego nie wiemy”:** kolumna pozycji z nazwą decyzji, filtr „Pozycja listy priorytetów”, nowe brzmienia wierszy 1, 3, 4, 13, 18 i 21.
- **Odwołania w zmienionych tekstach:** „Czego nie wiemy, punkt …” i „niewiadoma …” (punkty 3, 4, 5, 6, 7, 8, 9, 12, 13, 16, 17, 18, 19, 20 i 21) oraz „pozycja …” (1, 2, 5, 9 i 12) wskazują właściwe wiersze.
- **README:** odpowiedź w skrócie (poza R27 i R30), lista na pierwszy tydzień zgodna ze stroną, akapit o używaniu narzędzia, tabela zakładek, skrócone zdanie o sesjach zalogowanych od wejścia.
- **Nawigacja:** „Dalej: …”, „Wróć do początku: Czy to wzrost”, przycisk „Zakładki” na telefonie.

## 5. Propozycje wpisów do wspólnych notatek (bez numerów)

- `DECYZJE.md`: kontrola języka przed publikacją (część 3): 12 poprawek przed wysłaniem i 35 uwag na rozmowę; które z nich Kuba przyjął.
- `ZALOZENIA.md` (jeśli Kuba przyjmie P9): nazwa zbiorcza obu sposobów przypisania źródła to „reguły przypisania”; słowa „podział” w tym znaczeniu nie używamy (zostaje dla rozkładu spadku i wymiaru filtra).
- `ZNALEZISKA.md`: nic nowego w danych.
- `PRZEKAZANIE.md`: odnośnik do tej notatki przy stanie prac po kontroli przed publikacją.
