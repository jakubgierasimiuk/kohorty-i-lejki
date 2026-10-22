# E — nowe teksty zakładek „Kohorty”, „Po zakupie”, „Zdarzenia”, „Wynik biznesu” i „Jakość danych” (szkic do przeglądu Kuby, 2026-10-21)

Teksty kart w nowym kształcie (notatki/e_runda.md, punkt 3), napisane według zasad języka Kuby (część 2 zlecenia) i wyników części 1 (e_runda.md, punkt 4). Buduje je `analiza/e_teksty_zakladki.py` z danych zakładek i raportów; ten plik pierwszy raz powstał z plików strony; od 2026-10-22, po przeglądzie sesji prowadzącej, jest wzorcem kontroli poprawianym ręcznie (decyzja w notatki/e_runda.md). Każda sekcja „### klucz” to wzorzec kontroli liczb jednej karty albo jednego zdarzenia: każda liczba na stronie w tej karcie musi tu stać. Odwołania do „Czego nie wiemy” są już w nowej numeracji (dawna pozycja 13 wypadła).

Słownik: „ostatnie 12 miesięcy” = X 2025 – IX 2026, „rok wcześniej” = X 2024 – IX 2025. Reguła przypisania źródła ma jedną parę nazw: „według pierwszego wejścia” (pierwsze wejście pacjenta, a kod kampanii na pierwszym zamówieniu rozstrzyga) i „według sesji z płatnością”.

Druga lista poprawek Kuby (2026-10-22): sekcje kart, które zmieniła, podmienione na brzmienie z danych strony po sprawdzeniu, że kontrola liczb pokazywała w nich tylko liczby wprowadzone celowo; nazwy reguły ujednolicone w całej notatce.

## Kohorty

### kohorty

Tytuł: Nowi pacjenci wracają rzadziej niż rok wcześniej, w każdym oknie od 30 do 180 dni
Wniosek: W ciągu 90 dni od pierwszego zakupu wraca 17% nowych pacjentów, a rok wcześniej wracało 24%.
Marża na pacjenta w 90 dniach, przed kosztem pozyskania, spadła z 67 do 58 zł.
Około 71% spadku powrotu przypada na zmianę składu pacjentów. Pacjenci dwóch nowych kampanii na L4 (Meta i TikTok) wracają w 90 dniach tylko w 4%, a jest ich coraz więcej.
Bez nich powrót też spada, z 24% do 22%. Wiek, płeć, wielkość miejscowości i województwo tego spadku nie tłumaczą.
Zastrzeżenie: Podział spadku opisuje skład pacjentów i nie wskazuje przyczyny: nie mówi, jak wracaliby pacjenci nowych kampanii, gdyby przyszli innym kanałem.
Szczegóły:
*Powrót nowych pacjentów: odsetek pacjentów, którzy złożyli kolejne zamówienie (nieanulowane)*
| Powrót w ciągu | Ostatnie 12 miesięcy | Rok wcześniej | Zmiana |
|---|---|---|---|
| 30 dni | 7,8% (22 646 pacjentów) | 11,0% (14 984 pacjentów) | −3,2 pkt proc. |
| 60 dni | 13,7% (20 823 pacjentów) | 19,1% (13 941 pacjentów) | −5,4 pkt proc. |
| 90 dni | 17,4% (18 924 pacjentów) | 23,9% (12 867 pacjentów) | −6,5 pkt proc. |
| 180 dni | 22,2% (12 591 pacjentów) | 27,5% (9 125 pacjentów) | −5,2 pkt proc. |
Powrót w 90 dniach w ostatnich 12 miesiącach: pacjenci nowych kampanii 4,1% z 4 893 pacjentów, pozostali 22,0% z 14 031 pacjentów (rok wcześniej 23,9%).
Marża na pacjenta w 90 dniach: 58,3 zł wobec 66,6 zł rok wcześniej; w 180 dniach 67,7 zł wobec 75,5 zł.
Porównujemy te same dni kalendarzowe w obu latach i tylko kohorty z pełnym oknem. W oknie 90 dni to pierwsze zakupy od 1.10.2025 do 2.07.2026 i od 1.10.2024 do 2.07.2025.
Podział spadku liczymy opisowo, czyli bez mierzenia wpływu: część przypisana nowym kampaniom to ich udział w nowych pacjentach razy różnica powrotu między pozostałymi pacjentami a nimi, a reszta to spadek powrotu pozostałych pacjentów.
Źródło pacjenta liczymy według pierwszego wejścia. Według sesji z płatnością bez nowych kampanii powrót spada do 20,4% (15 414 pacjentów), marża na pacjenta w 90 dniach do 63,3 zł, a na nowe kampanie przypada około 46% spadku. Cała różnica między podziałami to jedna grupa: według sesji z płatnością do innych kanałów trafia 1 383 pacjentów nowych kampanii na L4 z tych kohort (2 081 w całych ostatnich 12 miesiącach). 1 279 z nich weszło pierwszy raz z reklamy nowej kampanii, a zapłaciło w innej sesji, a 104 weszło z innego kanału, ale zapłaciło z kodem nowej kampanii. Bez nich oba podziały dają ten sam powrót i tę samą marżę. Dlatego opis liczymy według pierwszego wejścia, a w filtrach można wybrać oba podziały.
Część spadku w kampaniach działających w obu latach może wiązać się z porannymi opóźnieniami u internistów: po spóźnionej pierwszej wizycie pacjenci wracają rzadziej. Dane tego nie rozstrzygają (Czego nie wiemy, punkt 4).
Wiek, płeć, wielkość miejscowości i województwo nie zmieniają wniosku. Pacjenci nowych kampanii są młodsi (średnio 27,6 roku, 7 268 pacjentów, wobec 38,0 roku pozostałych w obu latach), ale pierwsze L4 z nowych kampanii wraca w 90 dniach rzadko w każdej grupie wieku: 3,5% do 29 lat (2 532 pacjentów), 4,7% w wieku 30–44 lat (1 505) i 5,1% od 45 lat (39), wobec 13,3–15,3% u pozostałych pacjentów z pierwszym L4 (668–1 507 pacjentów w grupie wieku; ostatnie 12 miesięcy, kohorty do 2.07.2026). Po przeważeniu ostatnich 12 miesięcy strukturą wieku i płci roku wcześniej spadek powrotu w 90 dniach bez nowych kampanii zostaje ten sam: −1,9 punktu procentowego według pierwszego wejścia i −3,3 zamiast −3,5 punktu według sesji z płatnością. Udział nowych kampanii w nowych pacjentach ostatnich 12 miesięcy jest podobny we wszystkich województwach (26,2–31,5%). Jeden trop regionalny: w dolnośląskim powrót poza nowymi kampaniami spada z 27,6% (1 024 pacjentów) do 19,7% (1 001), ale test wszystkich województw razem nie odrzuca, że zmiana jest wszędzie podobna, a dolnośląskie miało najwyższy powrót rok wcześniej.
Skąd liczby: analiza/a5r_kohorty.py → analiza/wyniki/a5r_kohorty.txt; analiza/wyniki/a5r_struktura.txt; analiza/wyniki/c_priorytety.txt (W2); analiza/wyniki/e_merytoryka.txt (punkt 1); analiza/wyniki/d_retencja.txt (punkt 5); eksport analiza/b_eksport.py.

## Po zakupie

### po_zakupie/punktualnosc

Tytuł: Od lutego 2026 około połowy porannych wizyt u internisty zaczyna się ponad 15 minut po terminie
Wniosek: W ostatnich 12 miesiącach ponad 15 minut po terminie zaczęło się 41% porannych wizyt u internisty, a rok wcześniej 6%.
Do października 2025 było to 5–7% wizyt miesięcznie. Od listopada 2025 odsetek rośnie z miesiąca na miesiąc, a od lutego 2026 stoi na poziomie 47–53%.
U pozostałych lekarzy rano bez istotnej zmiany: około 3% w obu latach. U internisty w innych porach odsetek rośnie dużo mniej, głównie na brzegach porannego bloku (karta niżej).
Zastrzeżenie: Przyczyny opóźnień w danych nie widać, bo nie mamy grafików ani identyfikatorów lekarzy (Czego nie wiemy, punkt 4).
Szczegóły:
Wizyty u internisty z terminem 6:00–11:59, pacjenci spoza nowych kampanii: 4,7–6,9% miesięcznie do X 2025, 15,7% w XI 2025 (521 wizyt), 29,7% w XII 2025, 42,6% w I 2026 i 47,3–52,7% od II do IX 2026. W całym roku: 41,2% z 6 522 wizyt wobec 6,0% z 5 219 wizyt rok wcześniej.
U internisty w innych porach (pacjenci spoza nowych kampanii): 4,6% wizyt spóźnionych ponad 15 minut w ostatnich 12 miesiącach (14 018 wizyt) wobec 2,8% rok wcześniej (11 323 wizyty).
U pozostałych lekarzy rano (wszyscy pacjenci): 3,0% z 2 757 wizyt wobec 2,8% z 1 949 wizyt rok wcześniej; przedział różnicy obejmuje zero.
Długość wizyty i czas od zapłaty do terminu się nie zmieniają.
Opóźnienie to faktyczny start wizyty minus umówiony termin. Liczymy tylko wizyty odbyte, a dzień i porę według terminu. Pacjenci nowych kampanii na L4 to pacjenci kampanii meta_prosp_l4_szybko i tt_prosp_l4_15min według pierwszego wejścia; „spoza nowych kampanii” to wszyscy pozostali.
Skąd liczby: analiza/a5r_punktualnosc.py → analiza/wyniki/a5r_punktualnosc.txt; analiza/wyniki/d_retencja.txt (punkt 1); eksport analiza/b_eksport.py.

### po_zakupie/godziny

Tytuł: Opóźnienia u internisty skupiają się w jednym porannym bloku od 5:00 do 13:59
Wniosek: Od 6:00 do 10:59 ponad 15 minut po terminie zaczyna się 40–47% wizyt u internisty, a poza blokiem 5:00–13:59 prawie tyle samo co rok wcześniej.
Najmocniej rośnie od 6:00 do 11:59. Wzrost w porach „południe” i „noc” z karty wyżej to głównie brzegi bloku: godziny 12:00 i 5:00, a o 13:00 już niewiele.
U pozostałych lekarzy żadna godzina wyraźnie nie odstaje.
Szczegóły:
- o 5:00: 15,3% z 459 wizyt, rok wcześniej 1,5% z 267;
- od 6:00 do 10:59: od 40,4% do 47,0% (865–1 858 wizyt w godzinie), rok wcześniej 5,7–7,5%;
- o 11:00: 36,2% z 1 363 wizyt, rok wcześniej 3,4% z 834;
- o 12:00: 22,3% z 1 303 wizyt, rok wcześniej 3,4% z 774;
- o 13:00: 5,6% z 1 207 wizyt, rok wcześniej 2,5% z 719;
- poza 5:00–13:59: 2,7% z 14 898 wizyt, rok wcześniej 2,8% z 9 563.
Bez godziny 12:00 południe rośnie tylko z 2,9% do 3,9%, a noc bez 5:00 z 2,0% do 3,1%.
Wszyscy pacjenci; oba lata liczymy według dnia terminu wizyty.
Skąd liczby: analiza/d_retencja.py → analiza/wyniki/d_retencja.txt (punkt 1).

### po_zakupie/ruch

Tytuł: Przy tym samym porannym ruchu opóźnień jest dużo więcej niż rok wcześniej
Wniosek: W dni z tą samą liczbą porannych wizyt u internisty spóźnionych jest średnio o 26 punktów procentowych więcej wizyt niż rok wcześniej.
Rok wcześniej opóźnienia nie zależały od ruchu. Dziś dni z większym ruchem w tym samym miesiącu też prawie nie mają ich więcej.
Już pierwsza poranna wizyta dnia jest spóźniona prawie tak często jak kolejne: 42% wobec 43%. To bardziej pasuje do stałego przesunięcia od początku dnia (późniejszy start względem grafiku albo inna organizacja zapisów) niż do kolejki, która narasta w ciągu poranka.
Zastrzeżenie: To nasze odczytanie danych. Najwcześniejszy termin dnia liczymy dla całej sieci, bo w danych nie ma identyfikatorów lekarzy ani grafików (Czego nie wiemy, punkt 4).
Szczegóły:
Porównanie obejmuje 5 przedziałów ruchu obecnych w obu latach (9 979 wizyt); różnica to 26,4 punktu procentowego. Na przykład w dni z 17–20 porannymi wizytami spóźnionych było 6,0% wizyt rok wcześniej (89 dni) i 30,6% w ostatnich 12 miesiącach (58 dni).
Rok wcześniej opóźnienia nie zależą od ruchu (4,7–8,3% w każdym przedziale). W obrębie miesiąca dni z większym ruchem prawie nie mają więcej opóźnień: w tercylach dni według ruchu 5,4%, 6,1%, 6,1% rok wcześniej i 42,1%, 43,5%, 43,6% w ostatnich 12 miesiącach. Mediana ruchu porannego to 15 wizyt na dzień rok wcześniej i 26 w ostatnich 12 miesiącach.
Wizyty z najwcześniejszym porannym terminem dnia są spóźnione ponad 15 minut w 41,9% (391 wizyt), kolejne w 43,3% (8 760 wizyt), średnio 18,7 wobec 20,2 minuty (ostatnie 12 miesięcy). W tym samym miesiącu (II–IX 2026) godziny z 8 i więcej wizytami mają o 4,2 punktu procentowego więcej spóźnionych niż godziny z 1–3 wizytami.
Ruch poranny w dniu to wszystkie nieanulowane wizyty u internisty z terminem 6:00–11:59 tego dnia. Dni grupujemy według tego ruchu i w każdej grupie porównujemy odsetek porannych wizyt spóźnionych ponad 15 minut w obu latach.
Skąd liczby: analiza/a5r_punktualnosc.py → analiza/wyniki/a5r_punktualnosc.txt (sekcje 3f–3g); analiza/wyniki/d_retencja.txt (punkt 2); eksport analiza/b_eksport.py.

### po_zakupie/powrot

Tytuł: Po spóźnionej pierwszej wizycie pacjenci wracają rzadziej
Wniosek: W ostatnich 12 miesiącach po porannej wizycie u internisty zaczętej ponad 30 minut po terminie wraca w 90 dniach 10% pacjentów, a po wizycie punktualnej 27%.
Powrót spada z każdym przedziałem opóźnienia. Spóźnionych pierwszych wizyt rano jest dziś dużo więcej niż rok wcześniej (karty wyżej).
Tabela pokazuje też rok wcześniej, ale wtedy spóźnionych pierwszych wizyt rano było mało, więc tych porównań nie oceniamy.
Zastrzeżenie: To porównanie obserwacyjne: pacjenci spóźnionych wizyt mogą różnić się od pozostałych także czymś, czego w danych nie widać.
Szczegóły:
- do 5 minut po terminie: 27,0% z 826 pacjentów;
- ponad 5 do 15 minut: 19,9% z 977 pacjentów;
- ponad 15 do 30 minut: 16,0% z 557 pacjentów;
- ponad 30 minut: 10,1% z 533 pacjentów;
- brak wizyty (anulowana albo nieodebrana): 14,7% z 224 pacjentów.
Wniosek opieramy na ostatnich 12 miesiącach. Rok wcześniej pacjentów ze spóźnioną pierwszą wizytą rano było 135 przy 15–30 minutach i 35 powyżej 30 minut.
Pierwsza wizyta u internisty z terminem 6:00–11:59, pacjenci spoza nowych kampanii według pierwszego wejścia. Powrót w 90 dniach na tych samych dniach kalendarzowych, tylko kohorty z pełnym oknem: od 1.10.2025 do 2.07.2026 i rok wcześniej od 1.10.2024 do 2.07.2025.
Skąd liczby: analiza/a5r_punktualnosc.py → analiza/wyniki/a5r_punktualnosc.txt (1f); tabela pod kartą z danych kohort strony.

### po_zakupie/zwroty

Tytuł: Zwroty po wizycie skupiają się w L4 z nowych kampanii
Wniosek: W ostatnich 12 miesiącach zwrot po odbytej wizycie dostaje 17% wizyt L4 pacjentów nowych kampanii, a u pozostałych pacjentów 5%.
Rok wcześniej, bez nowych kampanii, zwrot dostawało 6% wizyt L4, więc u pozostałych pacjentów odsetek nie wzrósł.
Lekarz dostaje wynagrodzenie także za wizytę, za którą zwracamy pieniądze. U pacjentów nowych kampanii to w ostatnich 12 miesiącach 84 tys. zł zwróconych zapłat i 34 tys. zł kosztu lekarza.
Zastrzeżenie: Powodu zwrotu w danych nie ma. To, że lekarz nie wystawia L4, którego pacjent oczekuje po obietnicy reklamy, jest hipotezą (Czego nie wiemy, punkt 3).
Szczegóły:
Ostatnie 12 miesięcy: 17,4% z 5 895 wizyt L4 pacjentów nowych kampanii i 5,3% z 5 080 wizyt L4 pozostałych pacjentów. Rok wcześniej: 6,0% z 4 474 wizyt L4.
Zwroty po wizycie u pacjentów nowych kampanii w ostatnich 12 miesiącach: 1 044 wizyty we wszystkich celach wizyty, z tego 1 024 przy wizytach L4 (te liczy pozycja 5 listy priorytetów), 84 112 zł zwróconych zapłat i 33 975 zł kosztu lekarza.
Odsetek zwrotów liczymy wśród odbytych wizyt, według dnia płatności.
Skąd liczby: analiza/a5r_po_zakupie.py → analiza/wyniki/a5r_po_zakupie.txt (2b); eksport analiza/b_eksport.py.

### po_zakupie/oceny

Tytuł: Wizyty spóźnione ponad 30 minut dostają dużo gorsze oceny
Wniosek: W ostatnich 12 miesiącach wizyta u internisty zaczęta ponad 30 minut po terminie dostaje średnio 2,92, a wizyta punktualna 4,45 (skala 1–5).
Po takim opóźnieniu 32% ocen to 1 albo 2, a po wizycie punktualnej 1%.
Zastrzeżenie: Ocenę dostaje tylko 31% odbytych wizyt, więc oceny pokazują tylko kierunek.
Szczegóły:
Internista, pacjenci spoza nowych kampanii, ostatnie 12 miesięcy: przy opóźnieniu ponad 30 minut średnia 2,92 z 469 ocen, przy wizycie zaczętej do 5 minut po terminie 4,45 z 3 446 ocen. Ocenę dostało 11 234 z 35 960 wizyt odbytych w ostatnich 12 miesiącach (wszyscy lekarze i pacjenci).
Rok wcześniej średnia przy opóźnieniu ponad 30 minut była podobna (2,95), ale z 44 ocen, więc porównania z rokiem wcześniej nie interpretujemy.
Skąd liczby: analiza/a5r_po_zakupie.py → analiza/wyniki/a5r_po_zakupie.txt (3a); eksport analiza/b_eksport.py.

Nagłówki tabeli godzin terminu: Godzina terminu · Internista, rok wcześniej · Internista, ostatnie 12 miesięcy · Internista: zmiana (punkty procentowe) · Pozostali lekarze, rok wcześniej · Pozostali lekarze, ostatnie 12 miesięcy.

## Wynik biznesu

### wynik

Tytuł: Za cały rok marża rośnie, ale wydatki na kampanie rosną szybciej niż marża zarabiana przed ich kosztem
Wniosek: W ostatnich 12 miesiącach marża przed kosztem kampanii wzrosła o 41%, a wydatki na kampanie o 77%.
Po koszcie lekarza, kampaniach i prowizji marża i tak wzrosła o 27%.
Rok do roku marża przed kosztem kampanii rośnie z każdym kwartałem wolniej, a wydatki szybciej. W III kwartale 2026 wydatki na kampanie były ponad dwa razy wyższe niż rok wcześniej.
Powtórne zamówienie zostawia mniej marży niż rok wcześniej, bo rośnie udział wizyt ze zniżką TelemediGO: z 34% do 42% powtórnych zamówień. To spina się z bilansem programu: opłata za TelemediGO nie pokrywa zniżek, które dostają jego członkowie (zakładka „Czy to wzrost”).
Zastrzeżenie: Spadek marży w III kwartale 2026, o 7% rok do roku, zależy od jednorazowego zdarzenia: we wrześniu 2025 ruszyła sprzedaż TelemediGO w newsletterze. Po odjęciu jednorazowej nadwyżki tego startu marża kwartału jest o 1% wyższa niż rok wcześniej.
Szczegóły:
*Kwartały rok do roku*
| Kwartał | Marża przed kosztem kampanii | Wydatki na kampanie wobec roku wcześniej | Marża po kosztach kampanii |
|---|---|---|---|
| IV kw. 2025 | +55,2% | 1,30 raza | +71,4% |
| I kw. 2026 | +49,7% | 1,66 raza | +43,0% |
| II kw. 2026 | +38,4% | 2,04 raza | +13,0% |
| III kw. 2026 | +25,2% | 2,08 raza | −6,8% |
Za cały rok: marża przed kosztem kampanii 1 211 tys. zł → 1 713 tys. zł (+41,5%), wydatki na kampanie 368 tys. zł → 650 tys. zł (+76,7%), marża po koszcie lekarza, kampaniach i prowizji 828 tys. zł → 1 048 tys. zł (+26,6%). Marża przed kosztem kampanii to przychód z konsultacji po zwrotach i z TelemediGO minus koszt lekarza.
**III kwartał 2026 bez jednorazowego startu sprzedaży TelemediGO**
Sprzedaż TelemediGO w newsletterze ruszyła 8.09.2025. W pierwszych 23 dniach sprzedała 225 członkostw, a przy późniejszym tempie (1,26 dziennie) sprzedałaby około 29. Jednorazowa nadwyżka to 196 zakupów, czyli 17,4 tys. zł. Bez niej marża III kwartału 2026 jest o 1,1% wyższa niż rok wcześniej, a bez całej sprzedaży w newsletterze w obu latach o 2,3% niższa. Marża przed kosztem kampanii rośnie wtedy o 32,6% (bez tej korekty o 25,2%).
Cały spadek III kwartału 2026 przypada na wrzesień (−20,8 tys. zł); lipiec +6,6 tys. zł, sierpień −0,9 tys. zł.
**Marża na powtórne zamówienie w III kwartale 2026**
Pacjenci spoza nowych kampanii złożyli więcej powtórnych zamówień (3 140 wobec 2 879), ale każde zostawia mniej marży (32,81 zł wobec 35,86 zł). Spadek o 3,05 zł to w 89% zmiana udziału rodzajów zniżki, a w obrębie tego samego rodzaju zniżki marża prawie stoi (−0,35 zł). Udział wizyt ze zniżką TelemediGO rośnie z 34,3% do 41,6%. Wizyta ze zniżką zostawia 11,01 zł marży, bez zniżki 48,78 zł, a u specjalistów wizyta ze zniżką TelemediGO ma marżę ujemną (−5,59 zł).
**Rozkład księgowy spadku III kwartału 2026**
Rozkład księgowy dzieli różnicę marży między kwartałami na składniki. Pokazuje, gdzie w rachunku jest różnica; jej przyczyny nie wskazuje.
Marża spadła o 15,1 tys. zł. Według pierwszego wejścia pacjenci nowych kampanii zostawili 89,0 tys. zł marży przed kosztem kampanii przy 87,9 tys. zł wydatków, czyli wyszli prawie na zero (+1,1 tys. zł). Pozostała część biznesu straciła 16,2 tys. zł:
- opłaty TelemediGO −11,2 tys. zł, w tym −10,5 tys. zł sprzedaży osobnej w newsletterze (225 zakupów we wrześniu 2025 wobec 107 w całym III kwartale 2026);
- wyższe wydatki kampanii działających w obu latach −6,2 tys. zł;
- marża konsultacji +1,2 tys. zł: powtórnych zamówień jest więcej, ale każde zostawia mniej marży;
- prowizja bez zmian.
Po odjęciu TelemediGO zostaje 5,0 tys. zł spadku. W rachunku przypada on na wyższe wydatki kampanii działających w obu latach, częściowo zrównoważone wyższą marżą konsultacji. Rozkład nie oddziela skutków awarii w Safari od innych zmian przychodu. Według sesji z płatnością podział się odwraca: nowe kampanie −25,2 tys. zł, reszta +10,1 tys. zł; suma jest ta sama.
**Awaria Safari w III kwartale 2026**
Awaria zakładania konta w Safari na iOS kosztowała w samym III kwartale 2026 szacunkowo 14,6–18,3 tys. zł marży (258–323 utracone pierwsze zamówienia z ich powrotami w tym samym kwartale, zależnie od odjęcia tła i założonego tempa strat). Osobny scenariusz powrotów pacjentów utraconych od 17.03 do 30.06 daje jeszcze 4,1–4,5 tys. zł. Wyniku kwartału bez awarii nie mierzymy: to rachunek przy założeniach pozycji 1 listy priorytetów.
**Baza powracających pacjentów**
Pierwsze kwartały roku wcześniej nie miały jeszcze pełnej bazy powracających pacjentów. Marża z pacjentów pozyskanych w poprzednich kwartałach to 0% marży IV kwartału 2024, 23,4% I kwartału 2025 i 51,7% III kwartału 2025. Bez tej bazy marża rośnie rok do roku o 8,5% zamiast 71,4% w IV kwartale 2025 i o 26,1% zamiast 43,0% w I kwartale 2026. Miarodajne jest więc porównanie III kwartałów (baza to 51,7% i 51,1% marży).
Bez jednorazowej nadwyżki startu sprzedaży TelemediGO (jej części przypadającej na bazę: 210 z 225 zakupów) baza dała w III kwartale 2026 więcej marży niż rok wcześniej: 106,2 tys. zł wobec 99,0 tys. zł (+7,3%; bez całej sprzedaży w newsletterze w obu latach +1,0%). Wszystkich pacjentów pozyskanych w poprzednich kwartałach jest prawie trzy razy więcej (35 032 wobec 12 794), ale tych, którzy w kwartale coś kupili, tylko o 15% więcej (1 735 wobec 1 503). Dane nie rozdzielają, ile to wiek bazy, a ile to, że nowsze roczniki wracają rzadziej.
**Przychód i koszty za cały rok**
Przychód z konsultacji po zwrotach rośnie o 44,8% (2 230 266 zł → 3 228 342 zł), TelemediGO rośnie o 40,3% (156 551 zł → 219 652 zł). Koszt lekarza rośnie o 47,6% (1 175 700 zł → 1 734 825 zł), wydatki na kampanie rosną o 76,7% (367 632 zł → 649 675 zł), prowizja afiliacyjna rośnie o 0,2% (15 400 zł → 15 425 zł).
Koszt lekarza liczymy także za wizyty zwrócone po wizycie (zasada z zadania), a koszt i zwrot przypisujemy do dnia płatności. Prowizję afiliacyjną liczymy według pierwszego wejścia, w dniu pierwszego zamówienia.
Skąd liczby: analiza/wyniki/e_merytoryka.txt (punkty 2 i 3); analiza/wyniki/d_wynik.txt (punkty 1 i 2); analiza/wyniki/c_priorytety.txt (W4, P1); eksport analiza/b_eksport.py.

### wynik/ekonomia

Tytuł: Kampania TikTok na L4 nie zwraca kosztu pozyskania pacjenta
Wniosek: Po odjęciu kosztu pozyskania TikTok na L4 traci w 90 dniach około 5 zł na pacjencie według pierwszego wejścia i około 18 zł według sesji z płatnością.
Obie nowe kampanie na L4 razem wychodzą blisko zera: około +4 zł na pacjenta w 90 dniach według pierwszego wejścia i około −9 zł według sesji z płatnością. Znak zależy od reguły. Test z wyłączeniem reklamy Meta na L4 w części kraju zmierzy przyrost pacjentów niezależnie od reguły (pozycja 9 listy priorytetów).
Pozostałe kampanie płatne, afiliacja i kanały bezpłatne mają wynik dodatni w obu regułach (tabela niżej).
Zastrzeżenie: Wynik Google Ads na markę i remarketingu Meta jest liczony ostrożnie: rachunek kosztu pozyskania liczy tylko nowych pacjentów, a 37% i 24% zamówień w sesjach tych kampanii to zamówienia powtórne, których marży tym kampaniom nie przypisujemy.
Szczegóły:
W 90 dniach: TikTok na L4 −4,6 zł i −17,8 zł na pacjenta, obie nowe kampanie razem +3,6 zł i −9,4 zł. Po 180 dniach nowe kampanie na L4 dają +7,0 zł na pacjenta według pierwszego wejścia i −5,2 zł według sesji z płatnością.
Według pierwszego wejścia pacjent należy do kanału, z którego pierwszy raz wszedł na stronę, a kod kampanii na pierwszym zamówieniu rozstrzyga; według sesji z płatnością należy do kanału sesji, w której zapłacił. W nowych kampaniach różnica między tymi podziałami to jedna grupa: według sesji z płatnością do innych kanałów trafia 2 081 pacjentów nowych kampanii na L4 z ostatnich 12 miesięcy. 1 918 z nich weszło pierwszy raz z reklamy nowej kampanii, a zapłaciło w innej sesji, a 163 weszło z innego kanału, ale zapłaciło z kodem nowej kampanii. W ekonomii kampanii pokazujemy oba podziały, bo od nich zależy, której kampanii przypisujemy koszt pozyskania.
Zamówienia powtórne w sesjach kampanii w ostatnich 12 miesiącach: Google Ads na markę 37,1% z 4 825 zamówień, remarketing Meta 24,1% z 1 642 zamówień. Rok wcześniej 32,0% i 22,8%.
Obok wyniku po 90 dniach pokazujemy wynik po 180 dniach: pacjenci kampanii na L4 prawie nie wracają, a pozostali tak, więc 90 dni zaniża wartość pozostałych kampanii. Przedział przy wyniku jest warunkowy: liczony tylko z rozrzutu marży, bez niepewności przypisania źródła.
Nazwy kampanii w danych: Meta na L4 to meta_prosp_l4_szybko, TikTok na L4 to tt_prosp_l4_15min, Google Ads na markę to gs_brand, remarketing Meta to meta_rmkt_koszyk.
Skąd liczby: analiza/a5e_ekonomia.py → analiza/wyniki/a5e_kampanie.csv i a5e_ekonomia.txt; analiza/wyniki/e_merytoryka.txt (punkty 1 i 5a).

## Jakość danych

### jakosc

Tytuł: Dane wymagały dwóch poprawek; pozostałe niespójności są drobne
Wniosek: Usunęliśmy zamówienia zapisane w eksporcie dwa razy (604) i zamówienia kont testowych (2 071).
Danych nikt wcześniej nie czyścił. Poza tymi dwiema rzeczami jedna godzina bez danych i kilka drobnych niespójności dotyczą małej części danych.
Skąd liczby: analiza/a2_jakosc.py, analiza/a2_czyste.py, analiza/a3_dashboard.py; liczby liczy analiza/b_eksport.py.

### jakosc/mostek

Tytuł: Dashboard zawyża wzrost zamówień i przychodu, a liczbę pacjentów pokazuje prawie dobrze
Wniosek: Po oczyszczeniu zamówienia rosną o 56%, a nie o 61%, jak na dashboardzie.
Przychód z konsultacji po odjęciu zwrotów rośnie o 45%, a nie o 50%. Nowych pacjentów jest więcej o 52%, prawie tak samo jak na dashboardzie, a sprzedaż TelemediGO rośnie o 40%, bez zmian.
(Tu strona rysuje element „mostek”.)
Szczegóły:
Każdy wiersz tabeli zmienia jedną rzecz: najpierw usuwa kopie zamówień, potem konta testowe, a na końcu odejmuje zwroty od przychodu.
Zamówienia: 25 269 → 40 613 na dashboardzie i 24 716 → 38 491 po oczyszczeniu. Przychód z konsultacji: 2,382 → 3,580 mln zł na dashboardzie i 2,230 → 3,228 mln zł po oczyszczeniu i odjęciu zwrotów.
Skąd liczby: analiza/a3_dashboard.py → analiza/wyniki/a3_dashboard.txt i a3_siatka.csv; eksport analiza/b_eksport.py.

### jakosc/duplikaty

Tytuł: W czerwcu 2026 eksport zapisał część zamówień dwa razy; zostawiamy jedną kopię
Wniosek: Od 10.06.2026 do 24.06.2026 eksport zapisał dwa razy 604 zamówienia.
W tych dniach to od 28% do 42% zamówień dziennie, a dzień przed i dzień po nie ma ani jednej kopii.
Wszystkie kopie są w ostatnich 12 miesiącach i dodają do nich 51 293 zł zapłat (45 805 zł po odjęciu zwrotów). W analityce każde z tych zamówień ma jeden krok płatności, więc to wygląda na błąd eksportu: pacjent zapłacił raz.
Szczegóły:
Kopia to druga, identyczna linia tego samego zamówienia, tuż pod pierwszą w pliku zamówień. Wykres pokazuje dzień po dniu zamówienia bez kopii i kopie.
Skąd liczby: analiza/a2_jakosc.py; czyszczenie: analiza/a2_czyste.py.

### jakosc/testy

Tytuł: Zamówienia testowe zawyżały wzrost zamówień, bo jest ich prawie trzy razy więcej niż rok wcześniej
Wniosek: Zamówienia testowe to 2 071 zamówień z 22 kont; wyłączamy je ze wszystkich liczb.
Kod TEST-QA ma 1 781 zamówień. Pozostałe 290 zamówień nie ma kodu, ale każde jest zapłacone w pełni i w całości zwrócone, czyli wygląda na test procesu zwrotu. Filtr po samym kodzie by ich nie złapał.
Drugi, niezależny podpis: wszystkie trwają dokładnie 1 minutę (2 071 z 2 071), a taki czas nie występuje u żadnego innego pacjenta (0 zamówień; najkrótsza prawdziwa wizyta trwa 3 minuty).
Testów przybywa: 553 zamówienia rok wcześniej i 1 518 zamówień w ostatnich 12 miesiącach. Zawyżały więc wzrost zamówień. Wyłączamy te konta ze wszystkiego: zamówień, pacjentów, przychodu, sesji i lejka.
Zastrzeżenie: Nie wiemy, czy lekarze dostawali wynagrodzenie za te wizyty. Gdyby tak, kosztowałoby to około 52 tys. zł w dwóch latach, w tym około 38 tys. zł w ostatnich 12 miesiącach (Czego nie wiemy, punkt 13).
Szczegóły:
Zamówienia testowe to 27 591 zł zapłat i 25 810 zł zwrotów.
Koszt liczymy po stawce internisty z zadania (25 zł), bo wszystkie wizyty testowe są u internisty (2 071 z 2 071): 51 775 zł w dwóch latach i 37 950 zł w ostatnich 12 miesiącach.
Skąd liczby: analiza/a2_jakosc.py → analiza/wyniki/a2_jakosc.txt (2e); analiza/wyniki/c_priorytety.txt (P1b, P13).

### jakosc/godzina

Tytuł: Jednej godziny prawie nie ma w danych, ale wyników to nie zmienia
Wniosek: 17.05.2025 od 13:00 do 14:00 jest 1 sesja zamiast typowych 21.
Zamówień w tej godzinie jest zwykle około 2, więc to, że nie ma żadnego, niewiele mówi. To jedyna taka godzina w dwóch latach, a jej wpływ na wyniki jest pomijalny.
Zastrzeżenie: Nie wiemy, czy to przerwa w działaniu strony, czy w zbieraniu danych.
Szczegóły:
Typowa liczba to mediana tej samej godziny w 15 dniach wokół: 21 sesji i 2 zamówienia. Szukamy godzin, w których sesji jest dużo mniej niż ta mediana; w dwóch latach jest tylko ta jedna.
Skąd liczby: analiza/a2_jakosc.py, sekcja o lukach; analiza/wyniki/e_merytoryka.txt (punkt 5e).

### jakosc/drobne

Tytuł: Drobne niespójności dotyczą małej części danych
Wniosek: Każda z nich dotyczy najwyżej kilkudziesięciu zamówień albo kilkuset sesji.
- „Psycholog + e-recepta”: 24 zamówienia. Psycholog nie jest lekarzem i nie wystawia recept, więc to wartość nierealna.
- Mimo aktywnego TelemediGO bez zniżki zapłacono 1 zamówienie.
- Program poleceń: na stronę /polecenie wchodzi z innym źródłem (bezpośrednio, z Google albo z Meta) 330 sesji, a źródło „polecenie” z inną stroną wejścia ma 51 sesji. Ma to znaczenie przy przypisywaniu źródła pacjenta.
Skąd liczby: analiza/a2_jakosc.py → analiza/wyniki/a2_jakosc.txt.

### jakosc/czyste

Tytuł: Pozostałe sprawdzenia wyszły czysto
Wniosek: Czas płatności, kolejność kroków lejka, koszty kampanii, tożsamość pacjentów i pozostałe tabele są spójne.
- Czas płatności: 65 278 z 65 278 zamówień i 4 227 z 4 227 zakupów TelemediGO ma krok płatności w analityce co do sekundy po przeliczeniu z UTC na czas polski. Zmiana czasu jest obsłużona poprawnie.
- Sesje na kliknięcie są stałe w każdym kwartale: Google Ads od 0,92 do 0,93, Meta od 0,79 do 0,82, TikTok 0,72. Nie ma dni z kosztem bez sesji ani sesji z kampanii płatnej bez kosztu.
- Duplikaty w pozostałych tabelach: sesje 0, kroki lejka 0, konta 0, TelemediGO 0, wydatki na kampanie 0.
- Kroki lejka idą zawsze po kolei: 0 sesji ma krok bez poprzedniego. Jedyne wyjątki zgodne z opisem danych to 686 zakupów samego TelemediGO (tylko kroki płatności) i 22 sesje kont testowych z samym założeniem konta.
- Tożsamość: żadna przeglądarka nie jest dzielona przez dwa konta. Więcej niż jednej przeglądarki używa 7,3% kont (3 835 z 52 422), najwięcej 8 przeglądarek.
- Wartości realne: wizyty po oczyszczeniu trwają od 3 do 36 minut; ceny katalogowe i zniżki TelemediGO zgadzają się z zasadami co do złotówki (raport A2).
Skąd liczby: analiza/a2_jakosc.py, analiza/a2_czyste.py; liczby liczy analiza/b_eksport.py.

## Zdarzenia

### zdarzenia

Tytuł: Większość zmian zaczyna się między listopadem 2025 a marcem 2026
Wniosek: W tych miesiącach ruszają dwie nowe kampanie na L4, rosną poranne opóźnienia u internistów i psuje się zakładanie konta w Safari na iOS.
Listy zmian w produkcie i kalendarza kampanii nie mamy, więc każde zdarzenie znaleźliśmy w danych. Przy każdym jest data, co się zmieniło, o ile i skąd to wiemy.
Zastrzeżenie: Zdarzenia z tych samych miesięcy nakładają się, więc bez testu nie rozdzielamy ich skutków.
Szczegóły:
Tory na osi: lejek (pozyskanie), retencja (kohorty), obsługa pacjenta (przebieg wizyt) i jakość danych. Metoda wykrywania zmian dzieli serię dzienną na odcinki o różnym poziomie (podział binarny); zmianę uznajemy, gdy różnica poziomów wynosi co najmniej 4 błędy standardowe (|z| ≥ 4). Daty to kandydaci zmian; każdego sprawdzamy potem na danych.

### zdarzenie/luka_godzina

Data: 2025-05-17
Tytuł: Jednej godziny prawie nie ma w danych, ale wyników to nie zmienia
Krótko (listy i legendy): Godzina bez danych
Co się zmieniło: 17.05.2025 od 13:00 do 14:00 jest 1 sesja zamiast typowych 21 (mediana tej samej godziny w 15 dniach wokół) i 0 zamówień. To jedyna taka godzina w dwóch latach.
O ile: Zamówień w tej godzinie jest zwykle około 2, więc ich brak niewiele mówi. Nie wiemy, czy to przerwa w działaniu strony, czy w zbieraniu danych. Wpływ na wyniki jest pomijalny.
Skąd wiemy: Liczba sesji i zamówień w każdej godzinie wobec mediany tej samej godziny w 15 dniach wokół. Źródło: analiza/a2_jakosc.py, sekcja o lukach; analiza/wyniki/e_merytoryka.txt, punkt 5e.

### zdarzenie/start_go_upsell

Data: 2025-09-08
Tytuł: Newsletter zaczyna sprzedawać samo TelemediGO, a pierwsze tygodnie dają jednorazowy skok sprzedaży
Krótko (listy i legendy): Start sprzedaży TelemediGO w newsletterze
Co się zmieniło: Newsletter do pacjentów, którzy już kupowali, prowadzi na stronę /telemedigo. Pojawiają się zakupy samego TelemediGO, bez konsultacji.
O ile: W pierwszych 23 dniach newsletter sprzedał 225 członkostw, a przy późniejszym tempie sprzedałby około 29. Ta jednorazowa nadwyżka (196 zakupów, 17,4 tys. zł) podnosi marżę III kwartału 2025, z którą porównujemy III kwartał 2026. Razem: 686 zakupów samego TelemediGO do 30.09.2026, czyli 69% z 992 wejść z tej kampanii. Pozostałe 306 wejść to sesje zalogowane od wejścia, bez zakupu.
Skąd wiemy: Pierwszy dzień z sesjami z kodem kampanii crm_go_upsell. Sesje z tej kampanii są w 326 dniach, a od pierwszego dnia (8.09.2025) do końca danych (30.09.2026) mija 388 dni kalendarzowych, bo newsletter nie wychodzi codziennie. Kampanie płatne mają sesje każdego dnia, więc u nich obie liczby są równe (Meta na L4: 332 dni). Późniejsze tempo to średnia z ostatnich 12 miesięcy (1,26 zakupu dziennie). Źródło: analiza/a5p_lejek.py, sekcja 1; analiza/wyniki/e_merytoryka.txt, punkt 2; notatki/a5_pozyskanie.md, punkt 2.4.

### zdarzenie/marza30_spada

Data: 2025-10-30
Tytuł: Marża nowego pacjenta w pierwszych 30 dniach spada w trzech krokach, głównie przez skład pacjentów
Krótko (listy i legendy): Marża na pacjenta w 30 dniach spada
Co się zmieniło: Marża nowego pacjenta w pierwszych 30 dniach, przed kosztem pozyskania, spada trzema stopniami. Przybywa pacjentów nowych kampanii na L4, którzy zostawiają mniej marży.
O ile: 56,0 zł od 1.10.2024 (17 520 pacjentów) → 53,1 zł od 30.10.2025 (5 549 pacjentów) → 50,1 zł od 26.01.2026 (6 064 pacjentów) → 46,8 zł od 8.04.2026 (9 744 pacjentów).
Skąd wiemy: Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

### zdarzenie/start_meta_l4

Data: 2025-11-03
Tytuł: Rusza kampania Meta na L4; jej sesje płacą rzadziej niż sesje z wyszukiwarki
Krótko (listy i legendy): Start kampanii Meta na L4
Co się zmieniło: Pierwszy dzień z sesjami i kosztem kampanii Meta na L4. Kampania przyprowadza głównie ruch z przeglądarek wbudowanych w aplikacje Instagrama i Facebooka. Jej sesje płacą rzadziej niż sesje z wyszukiwarki.
O ile: Średnio 183,7 sesji i 10,8 płatności dziennie, konwersja sesji do płatności 5,89%, razem 3 594 zamówienia do 30.09.2026. Od tego samego dnia: starsza kampania Meta 3,61% (20 687 sesji), wyszukiwarka bezpłatna 9,10% (43 291 sesji), Google Ads na hasła ogólne 8,55% (42 624 sesje). Ruch kampanii rośnie skokami: 17.11.2025, 8.12.2025, 2.01.2026, 19.01.2026.
Skąd wiemy: Pierwszy dzień z sesjami z kodem kampanii meta_prosp_l4_szybko w analityce; ten sam dzień w wydatkach na kampanie. Źródło: analiza/a5p_zdarzenia.py, sekcja 6; notatki/a5_pozyskanie.md, punkt 2.

### zdarzenie/udzial_nowych

Data: 2025-11-03
Tytuł: Coraz więcej nowych pacjentów przychodzi z kampanii na L4, a ci pacjenci prawie nie wracają
Krótko (listy i legendy): Rośnie udział nowych kampanii w nowych pacjentach
Co się zmieniło: Od startu kampanii Meta na L4 coraz większa część nowych pacjentów przychodzi z dwóch nowych kampanii na L4 (Meta i TikTok). Ci pacjenci prawie nie wracają, więc ich udział obniża powrót całej kohorty.
O ile: Udział w nowych pacjentach: 0,0% od 1.10.2024 do 2.11.2025 (17 676 pacjentów), 8,0% od 3.11.2025 do 5.12.2025 (1 972 pacjentów), 17,4% od 6.12.2025 do 2.02.2026 (4 127 pacjentów), 29,4% od 3.02.2026 do 9.04.2026 (5 503 pacjentów), 41,0% od 10.04.2026 do 30.09.2026 (11 640 pacjentów).
Skąd wiemy: Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

### zdarzenie/zwroty_pierwsze

Data: 2025-11-13
Tytuł: Coraz więcej pierwszych zamówień kończy się zwrotem po odbytej wizycie
Krótko (listy i legendy): Więcej zwrotów po wizycie
Co się zmieniło: Rośnie odsetek pierwszych zamówień, za które pacjent dostaje zwrot po odbytej wizycie. Skupia się w wizytach L4 pacjentów nowych kampanii. Lekarz dostaje wynagrodzenie także za te wizyty.
O ile: 2,1% od 1.10.2024 (18 260 pacjentów) → 3,9% od 13.11.2025 (7 142 pacjentów) → 6,9% od 23.02.2026 (15 516 pacjentów).
Skąd wiemy: Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

### zdarzenie/opoznienia_rano

Data: 2025-11-24
Tytuł: Poranne wizyty u internisty coraz częściej zaczynają się ponad 15 minut po terminie
Krótko (listy i legendy): Poranne opóźnienia u internisty
Co się zmieniło: Rośnie odsetek wizyt u internisty z terminem 6:00–11:59, które zaczynają się ponad 15 minut po terminie, także u pacjentów spoza nowych kampanii. Przy tym samym porannym ruchu opóźnień jest dużo więcej niż rok wcześniej, a już pierwsza poranna wizyta dnia jest często spóźniona. Przyczyny w danych nie widać (Czego nie wiemy, punkt 4).
O ile: 6,3% od 1.10.2024 (6 148 wizyt) → 27,8% od 24.11.2025 (615 wizyt) → 41,9% od 26.12.2025 (730 wizyt) → 50,2% od 2.02.2026 (4 248 wizyt). To średnie poziomy odcinków wyznaczonych przez metodę. Miesiąc po miesiącu od lutego do września 2026 to 47,3–52,7% porannych wizyt, jak w zakładce „Po zakupie”.
Skąd wiemy: Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). Seria: wizyty u internisty rano, pacjenci spoza nowych kampanii. Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

### zdarzenie/remarketing_meta

Data: 2026-01-01
Tytuł: Remarketing Meta coraz rzadziej kończy się płatnością, a jednocześnie trafia do innych osób niż wcześniej
Krótko (listy i legendy): Remarketing Meta słabnie
Co się zmieniło: Remarketing wraca coraz częściej do osób, które pierwszy raz przyszły z Meta i TikToka, a rzadziej do osób z wyszukiwarki. Te osoby płacą rzadziej. W obrębie źródła pierwszej wizyty konwersja stoi.
O ile: Płatność na sesję u osób, które jeszcze nie kupowały: 28,2% w IV kwartale 2025 (1 011 sesji), 18,9% w II kwartale 2026 (1 603 sesje) i 19,1% w III kwartale 2026 (1 534 sesje). Udział przeglądarek w aplikacjach w tym ruchu rośnie z 13,3% do 22,1–23,4%. Osoby, które pierwszy raz przyszły z Google albo Bing: 27,9% rok wcześniej i 26,7% od 1.01.2026 do 30.09.2026; z Meta (pozyskanie): 11,5% i 13,2%.
Skąd wiemy: Metoda wykrywania zmian wskazała 20.03.2026 jako dzień zmiany poziomu płatności na sesję (27,3% → 19,1%), ale zmiana narasta od 1.01.2026. Kod kampanii: meta_rmkt_koszyk. Źródło: analiza/a5p_zdarzenia.py, sekcje 5h i 5i; notatki/a5_pozyskanie.md, punkt 2.5.

### zdarzenie/start_tiktok

Data: 2026-02-09
Tytuł: Rusza kampania TikTok na L4; jej sesje płacą rzadziej niż sesje z wyszukiwarki i kampanii Meta na L4
Krótko (listy i legendy): Start kampanii TikTok na L4
Co się zmieniło: Pierwszy dzień z sesjami i kosztem kampanii TikTok na L4. Kampania przyprowadza głównie ruch z przeglądarek wbudowanych w aplikację TikToka. Jej sesje płacą rzadziej niż sesje z wyszukiwarki i kampanii Meta na L4.
O ile: Średnio 143,0 sesji i 6,8 płatności dziennie, konwersja sesji do płatności 4,76%, razem 1 593 zamówienia do 30.09.2026. Od tego samego dnia: kampania Meta na L4 5,90% (48 952 sesje), wyszukiwarka bezpłatna 8,97% (29 242 sesje). Ruch kampanii rośnie skokami: 23.02.2026, 13.03.2026, 6.04.2026.
Skąd wiemy: Pierwszy dzień z sesjami z kodem kampanii tt_prosp_l4_15min w analityce; ten sam dzień w wydatkach na kampanie. Źródło: analiza/a5p_zdarzenia.py, sekcja 6; notatki/a5_pozyskanie.md, punkt 2.

### zdarzenie/powrot30_spada

Data: 2026-02-10
Tytuł: Powrót nowych pacjentów w 30 dniach spada skokowo, głównie przez skład pacjentów
Krótko (listy i legendy): Spada powrót w 30 dniach
Co się zmieniło: Powrót w 30 dniach całej kohorty spada skokowo zaraz po starcie kampanii TikTok na L4 (9.02.2026); metoda wskazała dzień później. To głównie skład pacjentów: rośnie udział nowych kampanii, których pacjenci prawie nie wracają.
O ile: 9,7% (12 514 pacjentów, 5.06.2025–9.02.2026) → 6,9% (14 536 pacjentów, 10.02.2026–31.08.2026). Wcześniejszy kandydat 5.06.2025: 11,4% → 9,7%; wypada w pierwszym roku, więc może być porą roku.
Skąd wiemy: Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). Udział składu pokazuje rozkład spadku powrotu (notatki/a5_retencja.md, krok 3). Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

### zdarzenie/powrot90_stare

Data: 2026-03-02
Tytuł: W kampaniach działających w obu latach powrót też spada, ale bez wyraźnego skoku
Krótko (listy i legendy): Powrót w kampaniach działających w obu latach
Co się zmieniło: W kampaniach obecnych w obu latach powrót w 90 dniach też spada, ale metoda nie znalazła zmiany skokowej powyżej progu. Najsilniejszy kandydat to ten dzień.
O ile: 23,3% przed (24 511 pacjentów) i 20,9% po (5 751 pacjentów, kohorty z pełnym oknem 90 dni).
Skąd wiemy: Kandydata wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki); różnica jest poniżej progu. Brak skoku nie znaczy, że spadek musi być rozłożony w czasie. Luty 2026 nie pasuje do hipotezy, że większe opóźnienia zawsze obniżają powrót: opóźnienia były wtedy już wysokie, a powrót w tych kampaniach nie spadł. To trop do sprawdzenia. Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

### zdarzenie/safari_ios

Data: 2026-03-17
Tytuł: Od 17 marca 2026 w Safari na iPhone'ach i iPadach dużo rzadziej udaje się założyć nowe konto
Krótko (listy i legendy): Awaria zakładania konta w Safari na iOS
Co się zmieniło: U osób, które jeszcze nie kupowały, krok logowania albo zakładania konta po wyborze terminu spada w Safari na iPhone'ach i iPadach i zostaje niski do końca danych. Gwałtownie spada skuteczność zakładania nowego konta (konta dalej powstają, ale rzadziej), a logowanie do istniejącego działa.
O ile: Krok konta po wyborze terminu spadł z 66,1% (od 1.10.2025 do 16.03.2026) do 45,6% (od 17.03 do 30.09.2026, 4 678 sesji z wyborem terminu) i nie wraca. W 60 dniach przed awarią i po niej: 66,2% (1 763 sesje) i 45,1% (1 553 sesje); pozostałe przeglądarki 64,8% i 63,4%. Szacunek: 628–695 utraconych pierwszych zamówień w 198 dniach do 30.09.2026, czyli 95–105 na 30 dni.
Skąd wiemy: Metoda wykrywania zmian w seriach dziennych (podział binarny) wskazała ten dzień. Sprawdzenie na bazie: spadek jest w głównych kanałach (TikTok ma za małą próbę do oceny), więc to nie zmiana struktury ruchu. Przyczyny w danych nie widać. Źródło: analiza/a5p_zdarzenia.py, sekcja 5; notatki/a5_pozyskanie.md, punkt 2.1.

### zdarzenie/marka_konwersja

Data: 2026-05-22
Tytuł: W kampanii Google Ads na markę mniej sesji kończy się płatnością, a przyczyny w danych nie widać
Krótko (listy i legendy): Spada konwersja Google Ads na markę
Co się zmieniło: Sesja do płatności u osób, które jeszcze nie kupowały, spada w kampanii Google Ads na markę. Przyczyny w danych nie widać (Czego nie wiemy, punkt 21).
O ile: Z 21,2% (21 186 sesji, 1.10.2024–21.05.2026) do 17,8% (5 152 sesje, 22.05–30.09.2026), czyli o około 28,5–39,6 zamówienia na 30 dni zależnie od okna porównania. Bez Safari na iOS spadek jest prawie taki sam (−2,2 punktu procentowego wobec 17.03–21.05.2026), zmiana struktury ruchu (urządzenie, przeglądarka, strona wejścia) daje około zera, a inne kanały w tych dniach się nie zmieniają. Rok wcześniej w tym samym sezonie spadek był mniejszy (−1,3 punktu) i nieistotny, więc część może być sezonowa. W tym samym czasie rośnie koszt kliknięcia tej kampanii (z 1,01 zł rok wcześniej do 1,19 zł w ostatnich 12 miesiącach).
Skąd wiemy: Metoda wykrywania zmian w seriach dziennych wskazała ten dzień; sprawdzenie w oknach przed i po, bez Safari na iOS, ze strukturą ruchu i z tym samym sezonem rok wcześniej. Kod kampanii: gs_brand. Źródło: analiza/d_kampanie.py → analiza/wyniki/d_kampanie.txt, punkt 5.

### zdarzenie/duplikaty

Data: 2026-06-10 – 2026-06-24
Tytuł: W czerwcu 2026 eksport zapisał część zamówień dwa razy; zostawiamy jedną kopię
Krótko (listy i legendy): Duplikaty zamówień w eksporcie
Co się zmieniło: W eksporcie dwa razy zapisano 604 zamówienia, wszystkie od 10.06.2026 do 24.06.2026. W tych dniach zdublowanych jest od 28% do 42% zamówień dziennie. Dzień przed oknem i dzień po nim: 0 zamówień zdublowanych.
O ile: Wszystkie kopie są w ostatnich 12 miesiącach i dodają do nich 604 zamówienia i 51 293 zł zapłat, czyli 45 805 zł po odjęciu zwrotów. W analityce każde z tych zamówień ma jeden krok płatności, więc to wygląda na błąd eksportu: pacjent zapłacił raz. Zostawiamy jedną kopię.
Skąd wiemy: Dwie identyczne kopie zamówienia w sąsiednich liniach pliku zamówień. Źródło: analiza/a2_jakosc.py; czyszczenie: analiza/a2_czyste.py.
