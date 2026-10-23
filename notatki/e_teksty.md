# E — nowe teksty strony: „Czy to wzrost”, „Priorytety”, „Czego nie wiemy”, nagłówek lejka (szkic sesji prowadzącej, 2026-10-21)

To szkic tekstów w nowym kształcie karty (notatki/e_runda.md, punkt 3), napisany według zasad języka Kuby (część 2 zlecenia) i wyników części 1 (e_runda.md, punkt 4). Każda sekcja „### klucz” to wzorzec kontroli liczb dla jednej karty: każda liczba na stronie w tej karcie musi stać tutaj albo w dawnym fragmencie (c_szkic.md, d_teksty_strony.md), z którego przeniesione jest zdanie w szczegółach. Liczby pochodzą z raportów: `c_priorytety.txt`, `c_telemedigo.txt`, `d_*.txt`, `e_merytoryka.txt`.

Słownik w całym tekście: „ostatnie 12 miesięcy” = X 2025 – IX 2026, „rok wcześniej” = X 2024 – IX 2025. Reguła przypisania źródła ma w całym narzędziu jedną parę nazw: „według pierwszego wejścia” (pierwsze wejście pacjenta, a kod kampanii na pierwszym zamówieniu rozstrzyga; tak opisujemy pacjentów i retencję) i „według sesji z płatnością”.

Druga lista poprawek Kuby (2026-10-22, zlecenie w notatki/e_runda.md): sekcje niżej poprawione według niej; nowe liczby (lejek „dziś”, dwa zbiory zwrotów) liczy analiza/e_poprawki.py → analiza/wyniki/e_poprawki.txt.

Trzecia lista Kuby (2026-10-22, po przeglądzie 4c594b5): nagłówek lejka według pierwszego wejścia, z Safari (punkt 1; e_poprawki.txt, punkt 3), wydatki w tabeli kwartałów w procentach (punkt 2), konkretne wdrożenie pozycji 1 i stopka „Skąd liczby” bez nazwy rundy (punkt 4).

## 1. Czy to wzrost

Przebudowa po publikacji (wątek Kuby z 2026-10-23, runda G): zakładka odpowiada najpierw, dlaczego „Nie”, mimo że marża po wszystkich kosztach wzrosła o 27%. Liczby nowych zdań: analiza/g_werdykt.py → analiza/wyniki/g_werdykt.txt (G1–G4). Kuba wybrał „od wiosny wychodzimy na zero” (według pierwszego wejścia; obie kampanie razem w II i III kwartale 2026 poniżej 1 zł na pacjencie), a TikTok i reguła sesji z płatnością idą do kroku 4. Układ: werdykt z trzema linijkami i dwoma pojęciami, cztery kafelki, osiem kroków (pytanie, odpowiedź w jednym zdaniu, co to znaczy dla biznesu, szczegóły zwinięte), TelemediGO jako osobna karta na końcu.

### wzrost/wstep

Wzrost to dwie rzeczy naraz: więcej pacjentów i lepsza retencja. Sprawdzamy oba warunki osobno, na danych oczyszczonych, porównując ostatnie 12 miesięcy (X 2025 – IX 2026) z rokiem wcześniej (X 2024 – IX 2025). Na końcu sprawdzamy, ile biznes na tym zarabia.

### wzrost/werdykt

Znacznik: Nie.
Prawie cały przyrost pacjentów (86%) to pacjenci dwóch nowych kampanii na L4, a na ich pacjencie po koszcie pozyskania prawie nic nie zostaje: 7 zł w ciągu 180 dni wobec 30 zł na pacjencie pozostałych kampanii płatnych, a na pacjentach pozyskanych od wiosny szacunkowo wychodzimy na zero. Marża po wszystkich kosztach wzrosła o 27% prawie wyłącznie dzięki zakupom pacjentów pozyskanych w pierwszym roku. Pacjenci pozyskani w ostatnich 12 miesiącach zarobili w roku pozyskania, po kosztach kampanii, tylko o 3% więcej niż ci pozyskani rok wcześniej, choć było ich o 52% więcej.
(Po recenzji Codeksa i agenta-czytelnika: „to pacjenci” zamiast „dały”, kto wychodzi na zero, „w roku pozyskania”.)
Trzy linijki:
- Więcej pacjentów — Tak, ale: Nowych pacjentów jest o 52% więcej niż rok wcześniej, ale bez dwóch nowych kampanii na L4 tylko o 7%.
- Lepsza retencja — Nie: W ciągu 90 dni wraca 17% nowych pacjentów, a rok wcześniej wracało 24%; rzadziej wracają też pacjenci spoza nowych kampanii.
- Więcej zarabiamy — Tak, ale: Marża po wszystkich kosztach wzrosła z 828 do 1 048 tys. zł, ale 88% tego przyrostu to kolejne zakupy pacjentów pozyskanych w pierwszym roku, a wynik pacjentów pozyskanych w danym roku wzrósł tylko o 3%.
Dwa pojęcia, raz, prostymi słowami:
- Marża: to, co zostaje z zapłaty pacjenta po zwrotach i po wynagrodzeniu lekarza, razem z opłatą za TelemediGO. Marża po wszystkich kosztach odejmuje do tego wydatki na kampanie i prowizję afiliacyjną.
- Koszt pozyskania: wydatki na kampanię podzielone przez liczbę nowych pacjentów, którzy z niej przyszli. „Zostaje na pacjencie” to jego marża w ciągu 180 dni od pierwszego zakupu minus koszt jego pozyskania.
- Reguły przypisania (dodane po teście agenta-czytelnika): pacjenta przypisujemy do kampanii według pierwszego wejścia na stronę (tak liczymy w całym narzędziu) albo według sesji, w której zapłacił. Odpowiedź „Nie” jest taka sama przy obu regułach.
Zastrzeżenie: Nie wiemy, ilu pacjentów nowych kampanii przyszłoby i bez reklamy. Odpowie na to test z pozycji 9 listy priorytetów: wyłączenie kampanii Meta na L4 na 4–6 tygodni w losowej połowie województw i porównanie wszystkich nowych pacjentów z drugą połową.

### wzrost/kafelki

- 86% — przyrostu nowych pacjentów to pacjenci dwóch nowych kampanii na L4; według sesji z płatnością 61%.
- 7 zł — zostaje w ciągu 180 dni na pacjencie nowych kampanii na L4 po koszcie pozyskania; pozostałe kampanie płatne: 30 zł.
- 17% — nowych pacjentów wraca w ciągu 90 dni; rok wcześniej 24%.
- 88% — przyrostu marży to zakupy pacjentów z pierwszego roku; pacjenci pozyskani w danym roku po kosztach kampanii: +3%.

### wzrost/dashboard

Etykieta: Krok 1.
Tytuł: Ile z liczb z dashboardu jest prawdą?
Odpowiedź: Liczba nowych pacjentów i sprzedaż TelemediGO się zgadzają, ale zamówień przybyło o 56%, a nie o 61%, a przychodu z konsultacji po zwrotach o 45%, a nie o 50%.
Co to znaczy dla biznesu: Zanim na dashboardzie zaczniemy podejmować decyzje, trzeba go oczyścić z podwójnych zamówień i kont testowych i liczyć przychód po zwrotach (pozycja 2 listy priorytetów).
- Dashboard liczy dane na surowo: z 604 zdublowanymi zamówieniami z 10–24.06.2026, z 2 071 zamówieniami 22 kont testowych i z przychodem przed zwrotami.
- Nowi pacjenci: +52,1% po oczyszczeniu wobec +51,9% na dashboardzie; sprzedaż TelemediGO bez zmian, +40,3%.
Wykres: schodki od dashboardu do danych oczyszczonych (tabela mostka w zwiniętej sekcji).
Zastrzeżenie: Pierwszy rok startował od zera, bez bazy powracających pacjentów, więc sumy roczne z definicji faworyzują drugi rok (krok 5).
Szczegóły (słownikiem: rok wcześniej, ostatnie 12 miesięcy): zastrzeżenia 1–3 z c_szkic.md, sekcja 1c (5 289 zamówień powtórnych pacjentów sprzed roku, 153 tys. zł marży konsultacji; rozbicie +26,6%, +8,1%, +3,1%; wydatki +77%); dokładnie 44,8% przychodu.

### wzrost/pacjenci

Etykieta: Krok 2.
Tytuł: Skąd są nowi pacjenci?
Odpowiedź: Z 8 456 nowych pacjentów więcej niż rok wcześniej 7 268, czyli 86% przyrostu, to pacjenci dwóch nowych kampanii na L4: Meta od listopada 2025 i TikTok od lutego 2026.
Co to znaczy dla biznesu: Przyrost pacjentów przypisujemy prawie w całości dwóm kampaniom: poza nimi nowych pacjentów przybyło tylko o 7%, więc o wzroście decyduje to, ile zostaje na pacjencie tych kampanii (krok 4).
Wykres: słupki nowych pacjentów w obu latach, nowe kampanie na L4 i pozostałe (24 687 i 16 231; 17 419 bez nowych kampanii).
- Meta na L4 dała 5 059 nowych pacjentów, a TikTok na L4 2 209.
- Pozostałe kampanie płatne dały o 332 nowych pacjentów więcej niż rok wcześniej, kanały bezpłatne (wejścia bezpośrednie, bezpłatna wyszukiwarka, program poleceń) o 855 więcej, a ranking lekarzy tyle samo.
- Według sesji z płatnością nowe kampanie dały 5 187 pacjentów, czyli 61% przyrostu, a bez nich pacjentów przybyło o 20%.
Szczegóły:
- Dokładnie: +52,1% wszystkich nowych pacjentów, +7,3% bez nowych kampanii, +12,1% z kanałów bezpłatnych (z 7 069 do 7 924). Pacjenci nowych kampanii: 7 268 z 24 687 (29%), marża w 90 dniach 36,3 zł wobec 66,0 zł.
- Źródło pacjenta liczymy według pierwszego wejścia: pacjent nowej kampanii to ten, który pierwszy raz wszedł z jej reklamy albo zapłacił z jej kodem rabatowym. Według sesji z płatnością pacjentów bez nowych kampanii jest 19 500, czyli +20,1%. Różnica to 2 081 pacjentów, którzy według pierwszego wejścia należą do nowych kampanii, a według sesji z płatnością do innych kanałów: 1 918 weszło pierwszy raz z reklamy nowej kampanii, a zapłaciło w innej sesji (najczęściej po wejściu bezpośrednim albo z wyszukiwarki), a 163 weszło z innego kanału, ale zapłaciło z kodem nowej kampanii. Wracają tak rzadko jak pozostali pacjenci nowych kampanii. Bez nich obie reguły przypisania dają ten sam przyrost pacjentów, ten sam powrót i tę samą marżę, więc pacjentów i retencję opisujemy według pierwszego wejścia. W ekonomii kampanii pokazujemy obie reguły.
- Pozostałe kampanie płatne: 8 546 i 8 878 nowych pacjentów (+3,9%); ranking lekarzy 616 i 617.

### wzrost/retencja

Etykieta: Krok 3.
Tytuł: Czy wracają?
Odpowiedź: Rzadziej niż rok wcześniej: w ciągu 90 dni wraca 17% nowych pacjentów wobec 24%, a pacjenci nowych kampanii na L4 tylko w 4%.
Co to znaczy dla biznesu: Nowy pacjent zostawia dziś mniej w kolejnych miesiącach: jego marża w 90 dniach, przed kosztem pozyskania, spadła z 67 do 58 zł.
Tabela: powrót w ciągu 30, 60, 90 i 180 dni, rok wcześniej i w ostatnich 12 miesiącach, ze zmianą (liczby jak w c_szkic.md, sekcja 1b, i a5r_kohorty.txt).
- Liczymy tylko pacjentów, którzy mają już pełne okno od pierwszego zakupu (na przykład pełne 90 dni), na tych samych dniach kalendarzowych w obu latach.
- Bez pacjentów nowych kampanii powrót też spada: 22% wobec 24%.
- Pacjenci nowych kampanii wracają w 4%. Ich większy udział wśród nowych pacjentów odpowiada za około 71% spadku powrotu (4,6 z 6,5 punktu procentowego), a reszta to spadek w kanałach działających w obu latach.
- Poza nowymi kampaniami marża na pacjenta w 90 dniach prawie stoi: 66 zł wobec 67 zł.
Zastrzeżenie: Te liczby opisują zmianę, ale nie wskazują jej przyczyny. Nie wiemy, dlaczego spada powrót w kanałach działających w obu latach: czy ci sami pacjenci zachowują się dziś gorzej, czy zmieniło się to, kto do nas trafia.
Szczegóły (jak dotąd):
- Liczba pacjentów: 12 867 rok wcześniej i 18 924 w ostatnich 12 miesiącach; bez nowych kampanii 14 031 (powrót 22,0% wobec 23,9%), pacjenci nowych kampanii 4 893 (powrót 4,1%). Marża na pacjenta w 90 dniach: 58,3 zł wobec 66,6 zł, bez nowych kampanii 66,0 zł.
- Kolejne zamówienia na pacjenta w 90 dniach: 0,234 wobec 0,334, czyli o 29,8% mniej; bez pacjentów nowych kampanii 0,300.
- Według sesji z płatnością bez nowych kampanii powrót wynosi 20,4%, a marża 63,3 zł. Cała różnica to 1 383 pacjentów nowych kampanii (z pełnym oknem 90 dni), których ta reguła przypisuje innym kanałom: 1 279 weszło z reklamy nowej kampanii, a zapłaciło w innej sesji, a 104 zapłaciło z kodem nowej kampanii po wejściu z innego kanału. Wracają w 4,3%. Bez nich obie reguły dają 22,0% i 66,0 zł, a udział nowych kampanii w spadku powrotu wynosi w obu 71% (według sesji z płatnością bez tej poprawki 46%).
- „Około 71% spadku” to podział opisowy, czyli bez mierzenia wpływu: udział pacjentów nowych kampanii (25,9% kohort) razy różnica powrotu między nimi a resztą (4,6 z 6,5 punktu procentowego). Nie mówi, co by się stało bez tych kampanii.
- Według pierwszej usługi (zdanie z c_szkic.md, sekcja 1b, z drugą regułą wyjaśnioną tak samo): pierwsze L4 u internisty według sesji z płatnością spada do 11,0%, ale to ta sama grupa: do 2 969 pacjentów według pierwszego wejścia dochodzi 1 145 pacjentów nowych kampanii z pierwszym L4.
- Liczba osób, które wróciły w 90 dniach, rośnie: 3 289 wobec 3 076 (+6,9%). Spada tylko ich odsetek.
- W 180 dniach liczymy tylko kohorty z pełnym oknem (9 125 i 12 591 pacjentów).
- Część spadku w kanałach działających w obu latach może wiązać się z porannymi opóźnieniami u internistów: po spóźnionej pierwszej wizycie pacjenci wracają rzadziej. Dane tego nie rozstrzygają (Czego nie wiemy, punkt 4).

### wzrost/na-pacjencie

Etykieta: Krok 4.
Tytuł: Ile zarabiamy na nowym pacjencie po koszcie pozyskania?
Odpowiedź: Na pacjencie nowych kampanii na L4 zostaje w ciągu 180 dni 7 zł, a na pacjencie pozostałych kampanii płatnych 30 zł (rok wcześniej 32 zł).
Co to znaczy dla biznesu: Pacjent przypisany nowym kampaniom zostawia po koszcie pozyskania kilka razy mniej niż pacjent pozostałych kampanii płatnych, a u pacjentów pozyskanych od kwietnia szacowany wynik jest bliski zeru.
Wykres: zostaje na pacjencie nowych kampanii na L4, miesiąc po miesiącu (miesiąc pierwszego zakupu, listopad 2025 – wrzesień 2026), według obu reguł przypisania; pionowa linia to zero (liczby z tabeli w szczegółach).
- Pacjent nowych kampanii zostawia w 180 dniach 37 zł marży, a jego pozyskanie kosztuje 30 zł. Pacjent pozostałych kampanii płatnych zostawia 72 zł marży przy koszcie pozyskania 43 zł.
- Miesiąc po miesiącu koszt pozyskania pacjenta nowych kampanii rośnie z 27–30 zł (listopad 2025 – luty 2026) do 33–37 zł (kwiecień – wrzesień 2026), a marża pacjenta zostaje na poziomie 34–40 zł. Od kwietnia zostaje od −1 do +3 zł na pacjencie.
- Osobno: TikTok na L4 traci od marca 2026 (w II kwartale 6 zł na pacjencie), a Meta na L4 zostaje na plusie (w III kwartale 2 zł na pacjencie).
- Według sesji z płatnością obie kampanie razem tracą od grudnia 2025, a od kwietnia średnio 12–16 zł na pacjencie.
- Razem w roku pozyskania pacjenci nowych kampanii zostawili 263 tys. zł marży przy 246 tys. zł wydatków na te kampanie, czyli 17 tys. zł.
Zastrzeżenie: Pacjenci z pierwszym zakupem od kwietnia 2026 nie mają jeszcze pełnych 180 dni. Ich marżę przybliżamy: do marży z krótszego okresu dodajemy to, co starsi pacjenci tych kampanii zostawili później, od 0,35 zł, gdy znamy już 90 dni, do 2,87 zł, gdy znamy tylko dzień zakupu. Dopłata jest mała, bo ci pacjenci prawie nie wracają.
Szczegóły:
Tabela (według pierwszego wejścia: nowi pacjenci, koszt pozyskania, marża w 180 dniach, zostaje; według sesji z płatnością: zostaje), miesiąc pierwszego zakupu, okno 180 dni zmierzone do marca 2026, potem przybliżenie (90 dni do czerwca, 30 dni do sierpnia, dzień zakupu we wrześniu):
- XI 2025: 121, 27,3 zł, 34,3 zł, +7,0 zł; +0,4 zł
- XII 2025: 279, 27,7 zł, 37,4 zł, +9,6 zł; −8,7 zł
- I 2026: 445, 30,1 zł, 40,4 zł, +10,3 zł; −0,3 zł
- II 2026: 610, 29,6 zł, 39,7 zł, +10,1 zł; −1,4 zł
- III 2026: 826, 31,7 zł, 35,5 zł, +3,8 zł; −7,9 zł
- IV 2026: 825, 36,0 zł, 35,0 zł, −1,0 zł; −15,9 zł
- V 2026: 910, 33,1 zł, 36,1 zł, +3,0 zł; −11,6 zł
- VI 2026: 818, 35,9 zł, 35,6 zł, −0,3 zł; −12,9 zł
- VII 2026: 799, 37,3 zł, 37,0 zł, −0,3 zł; −14,5 zł
- VIII 2026: 785, 36,4 zł, 36,5 zł, +0,1 zł; −14,0 zł
- IX 2026: 850, 34,8 zł, 36,1 zł, +1,3 zł; −15,5 zł
- Porównanie płatnych z płatnymi liczymy na pierwszych zakupach od 1.10 do 3.04 w obu latach, bo tylko one mają pełne 180 dni: 2 352 pacjentów nowych kampanii (przedział 95% od 5,4 do 8,6 zł), 5 130 pacjentów pozostałych kampanii płatnych (29,7 zł) i rok wcześniej 4 717 (31,8 zł).
- Według sesji z płatnością pacjent nowych kampanii daje −5,2 zł, a pacjent pozostałych kampanii płatnych 27,5 zł (rok wcześniej 30,0 zł).
- Na całym roczniku, z przybliżoną marżą w 180 dniach dla młodszych pacjentów: nowe kampanie 2,8 zł na pacjencie (7 268 pacjentów), pozostałe kampanie płatne 26,7 zł wobec 30,8 zł rok wcześniej.
- Ranking lekarzy (prowizja 25 zł za pacjenta) zostawia 37,0 zł wobec 34,8 zł rok wcześniej; liczymy go osobno, bo płacimy za pacjenta, a nie za kliknięcie.
- W kwartałach (według pierwszego wejścia): 8,9 zł, 7,4 zł, 0,7 zł i 0,4 zł na pacjencie w IV kwartale 2025 i w I, II i III kwartale 2026; według sesji z płatnością −5,5 zł, −4,0 zł, −13,4 zł i −14,7 zł.
- Kwota na pacjencie to średnia ze wszystkich pacjentów przypisanych kampanii. Nie mówi, ile dałaby kolejna złotówka budżetu.

### wzrost/marza

Etykieta: Krok 5.
Tytuł: Skąd w takim razie +27% marży?
Odpowiedź: Z pacjentów pozyskanych w pierwszym roku: ich zakupy w ostatnich 12 miesiącach dały 194 tys. zł, czyli 88% przyrostu marży o 220 tys. zł.
Co to znaczy dla biznesu: Łączny wynik pacjentów pozyskanych w danym roku, po kosztach kampanii, wzrósł tylko o 3% przy 52% więcej pacjentów, a na jednym nowym pacjencie spadł z 51 do 35 zł.
Wykres: słupki skumulowane marży po wszystkich kosztach w obu latach: pacjenci pozyskani w tym samym roku (828 i 854 tys. zł) i pacjenci z pierwszego roku (194 tys. zł); razem 828 i 1 048 tys. zł.
- Rok wcześniej cała marża, 828 tys. zł, pochodziła od pacjentów pozyskanych w tym samym roku. Wcześniejszych pacjentów w danych nie ma, bo dane zaczynają się 1.10.2024.
- W ostatnich 12 miesiącach pacjenci z pierwszego roku dali 194 tys. zł: 153 tys. zł z kolejnych wizyt i 41 tys. zł z opłat za TelemediGO.
- Pacjenci pozyskani w ostatnich 12 miesiącach zostawili w tym samym roku 1 519 tys. zł marży przed kosztem kampanii, o 25% więcej niż rok wcześniej. Wydatki na kampanie wzrosły jednak o 77%, z 368 do 650 tys. zł, więc po odjęciu wydatków i prowizji afiliacyjnej (15 tys. zł) zostaje 854 tys. zł wobec 828 tys. zł.
- To nie jest lepsza retencja: nowi pacjenci wracają rzadziej (krok 3). Tej kwoty rok wcześniej nie było, bo w danych nie ma pacjentów sprzed 1.10.2024.
Zastrzeżenie: To rozbicie księgowe: przypisuje marżę i koszty grupom pacjentów, ale nie mierzy, co by się stało bez nowych kampanii.
Szczegóły:
- Dokładnie: marża po wszystkich kosztach 828 085 zł rok wcześniej i 1 048 069 zł w ostatnich 12 miesiącach, czyli +219 984 zł (+26,6%). Pacjenci z pierwszego roku: 194 434 zł (88,4% przyrostu). Pacjenci pozyskani w danym roku, po kosztach kampanii i prowizji: 828 085 zł i 853 635 zł, czyli +25 550 zł (+3,1%; 11,6% przyrostu). Na nowego pacjenta: 51,02 zł (16 231 pacjentów) i 34,58 zł (24 687). To porównanie zawiera też krótszą obserwację: od pierwszego zakupu do końca roku minęło średnio 191,0 dnia rok wcześniej i 177,8 dnia w ostatnich 12 miesiącach (uwaga Codeksa, policzone w g_werdykt.py). Porównanie w stałym oknie 180 dni jest w kroku 4.
- Pacjenci nowych kampanii na L4 zostawili w roku pozyskania 263 tys. zł marży przy 246 tys. zł wydatków, czyli 17 tys. zł (2,38 zł na pacjenta). Pozostali pacjenci pozyskani w ostatnich 12 miesiącach dali po kosztach kampanii i prowizji 836 tys. zł wobec 828 tys. zł rok wcześniej (+1,0%), a na pacjenta 48,01 zł wobec 51,02 zł.
- Według sesji z płatnością nowe kampanie tracą w roku pozyskania 58 tys. zł (−11,23 zł na pacjenta), a pozostali pacjenci dają o 10,2% więcej niż rok wcześniej.
- Marża przed kosztem kampanii pacjentów pozyskanych w danym roku: 1 211 tys. zł i 1 519 tys. zł; wydatki na kampanie 367 632 zł i 649 675 zł; prowizja 15 400 zł i 15 425 zł.

### wzrost/wynik

Etykieta: Krok 6.
Tytuł: W którą stronę to idzie z kwartału na kwartał?
Odpowiedź: Z każdym kwartałem wydatki na kampanie rosną rok do roku szybciej, a marża przed ich kosztem wolniej: w III kwartale 2026 wydatki były ponad dwa razy wyższe niż rok wcześniej, a marża przed ich kosztem wyższa o 25%.
Co to znaczy dla biznesu: Wzrost marży po kosztach kampanii się zatrzymał: w III kwartale 2026 spadła o 7% rok do roku, a po odjęciu jednorazowego startu sprzedaży TelemediGO w newsletterze rok wcześniej byłaby wyższa tylko o 1%.
Tabela kwartałów (zmiana rok do roku): marża przed kosztem kampanii +55,2%, +49,7%, +38,4%, +25,2% (376,0, 500,2, 444,5, 392,5 tys. zł); wydatki na kampanie +29,6%, +66,4%, +104,0%, +107,7% (113,1, 170,6, 184,4, 181,6 tys. zł); marża po kosztach kampanii +71,4%, +43,0%, +13,0%, −6,8% (259,4, 324,4, 256,6, 207,7 tys. zł).
- Na pacjencie nowych kampanii na L4 zostawało po koszcie pozyskania 9 zł w IV kwartale 2025 i 7 zł w I kwartale 2026, a w II i III kwartale 2026 mniej niż 1 zł.
- Bez zakupów pacjentów pozyskanych w poprzednich kwartałach marża po kosztach kampanii rosła rok do roku o 8,5% w IV kwartale 2025 i o 26,1% w I kwartale 2026, a w II i III kwartale 2026 spadła o 6,7% i 5,6%.
- Marża przed kosztem kampanii wzrosła za cały rok o 41%, a wydatki na kampanie o 77%.
Zastrzeżenie: Marża po koszcie lekarza, kampaniach i prowizji spadła w III kwartale 2026 o 7% rok do roku, ale ten spadek zależy od jednorazowego zdarzenia: rok wcześniej we wrześniu ruszyła sprzedaż TelemediGO w newsletterze. Po odjęciu jednorazowej nadwyżki tego startu marża kwartału jest o 1% wyższa niż rok wcześniej.
Szczegóły (jak dotąd):
- Za cały rok marża po koszcie lekarza, kampaniach i prowizji wzrosła z 828 do 1 048 tys. zł, czyli o 26,6%. Marża przed kosztem kampanii wzrosła o 41,5%, a wydatki na kampanie o 76,7%.
- W III kwartale 2026 marża była o 6,8% niższa niż rok wcześniej. W pierwszych 23 dniach sprzedaży TelemediGO w newsletterze pacjenci kupili 225 członkostw; po odjęciu szacowanej nadwyżki tego startu marża kwartału jest o 1,1% wyższa niż rok wcześniej.
- Warianty III kwartału: bez nadwyżki startu sprzedaży w newsletterze (196 z 225 zakupów ponad zwykłe tempo 29 na 23 dni, 17,4 tys. zł) +1,1%; bez całej sprzedaży w newsletterze w obu latach −2,3%; bez wszystkich opłat za TelemediGO −4,9%. Marża przed kosztem kampanii bez nadwyżki startu rośnie o 32,6%.
- Awaria zakładania konta w Safari na iPhone'ach kosztowała w samym III kwartale 2026 szacunkowo 14,6–18,3 tys. zł marży. Wyniku kwartału bez awarii nie mierzymy; to scenariusz z pozycji 1 listy priorytetów.
- Baza powracających pacjentów (marża z pacjentów pozyskanych w poprzednich kwartałach): w III kwartale 2026 106,2 tys. zł wobec 115,2 tys. zł rok wcześniej. Rok wcześniej zawierała jednorazowy start sprzedaży w newsletterze; po odjęciu części nadwyżki przypadającej na bazę (210 z 225 zakupów) to 99,0 tys. zł, więc w 2026 baza dała o 7,3% więcej (bez całej sprzedaży w newsletterze w obu latach o 1,0% więcej). Wszystkich pacjentów pozyskanych w poprzednich kwartałach jest prawie trzy razy więcej (35 032 wobec 12 794), ale tych, którzy w kwartale coś kupili, tylko o 15% więcej (1 735 wobec 1 503). Baza jest starsza, a nowsze roczniki wracają rzadziej; tych dwóch rzeczy dane nie rozdzielają.
- Rozkład spadku III kwartału na pacjentów nowych kampanii i resztę biznesu (rozkład księgowy, czyli przypisanie składników marży grupom pacjentów bez mierzenia wpływu): zdania z c_szkic.md, sekcja 1c, i d_teksty_strony.md.

### wzrost/co-robimy

Etykieta: Krok 7.
Tytuł: Co robimy?
Odpowiedź: Najpierw naprawiamy to, co psuje wynik niezależnie od kampanii, potem wstrzymujemy kampanie, które średnio tracą na pacjencie, a o kampanii Meta na L4 rozstrzyga test w części kraju.
Co to znaczy dla biznesu: Każda pozycja listy priorytetów ma wartość w marży, sposób pomiaru i czas wdrożenia; niżej decyzje na pierwszy tydzień.
Decyzje na pierwszy tydzień (bez zmian, kolejność jak na liście priorytetów):
1. Naprawić zakładanie konta w Safari na iPhone'ach — pozycja 1, do 83 tys. zł marży rocznie.
2. Oczyścić codzienny raport i dodać alarmy na lejku — pozycja 2; awaria Safari trwała 198 dni, do końca danych.
3. Wstrzymać kampanię TikTok na L4 i kampanię Google Ads na specjalistów — pozycje 3 i 4; obie średnio tracą na pacjencie według obu reguł przypisania źródła (pierwsze wejście i sesja z płatnością), a pauzę da się cofnąć w jeden dzień.
4. Zrobić krótkie sprawdzenia: obietnica reklam L4, poranne grafiki internistów, zakup po zalogowaniu, kliknięcia w panelach reklam — pierwsze kroki pozycji 5, 6, 8 i 11; każde zajmuje dzień albo dwa.
Odnośniki: lista priorytetów, pozycja 9 (test Meta na L4).

### wzrost/niewiadome

Etykieta: Krok 8.
Tytuł: Czego nie wiemy?
Odpowiedź: Trzech rzeczy, od których zależą decyzje: ilu pacjentów nowych kampanii przyszłoby i bez reklamy, dlaczego rzadziej wracają pacjenci z kanałów działających w obu latach i ile wizyt dokłada zniżka TelemediGO.
Co to znaczy dla biznesu: Dlatego decyzje, które od nich zależą, są na liście priorytetów testami z regułą ustaloną z góry, a nie pewnymi kwotami.
- Ilu pacjentów nowych kampanii przyszłoby i bez reklamy: test z pozycji 9, czyli wyłączenie kampanii Meta na L4 na 4–6 tygodni w losowej połowie województw. Da wynik orientacyjny, więc decyzję podejmujemy według reguły ustalonej z góry (Czego nie wiemy, punkt 1).
- Dlaczego rzadziej wracają pacjenci z kanałów działających w obu latach: jedną z możliwych przyczyn są poranne opóźnienia u internistów, ale dane tego nie rozstrzygają (Czego nie wiemy, punkt 4).
- Ile wizyt i powrotów dokłada zniżka TelemediGO: losowy, bezpłatny dostęp do zniżek (pozycja 12; Czego nie wiemy, punkt 8).
Odnośniki: Czego nie wiemy, punkty 1, 4 i 8 oraz cała lista.

### wzrost/telemedigo

Osobna karta pod krokami (bez numeru kroku), treść bez zmian.
Tytuł: TelemediGO rośnie razem z liczbą zamówień, a nie dzięki większej chęci zakupu
Wniosek: Sprzedaż wzrosła o 40%, bo jest więcej zamówień i przez cały rok działała sprzedaż w newsletterze, a odsetek kupujących przy kasie nie rośnie.
Tabela: typ zakupu, rok wcześniej, ostatnie 12 miesięcy, zmiana, udział we wzroście (c_szkic.md, sekcja 2).
- Opłata 89 zł nie pokrywa zniżek: członkostwa sprzed roku dostały średnio o około 16 zł więcej zniżek, niż przyniosły opłat.
- Widać to w marży: powtórne zamówienie pacjenta spoza nowych kampanii zostawiło w III kwartale 2026 około 33 zł marży wobec 36 zł rok wcześniej. Prawie cały ten spadek to rosnący udział wizyt ze zniżką TelemediGO: z 34% do 42% powtórnych zamówień.
Zastrzeżenie: Nie wiemy, ile wizyt członkostwo dokłada. Test z pozycji 12 pokaże wpływ samej zniżki, ale nie opłacalność oferty za 89 zł.
Szczegóły (nowe zdania; reszta jak w c_szkic.md, sekcja 2):
- Powtórne zamówienie pacjenta spoza nowych kampanii zostawiło w III kwartale 2026 32,81 zł marży wobec 35,86 zł rok wcześniej. Wizyta ze zniżką TelemediGO zostawia średnio 11,01 zł marży, bez zniżki 48,78 zł, a wizyta u specjalisty ze zniżką traci 5,59 zł. Udział wizyt ze zniżką wśród powtórnych zamówień: 34,3% (2 879 zamówień) i 41,6% (3 140). Zmiana tego udziału daje 2,71 zł z 3,05 zł spadku marży na zamówienie (rozkład na strukturę i marżę w obrębie rodzaju zniżki).

## 2. Priorytety

Przegląd: kolumny „Co robimy”, „Ile warte”, „Pewność”, „Wdrożenie”. Pewność jako znacznik: Wysoka, Średnia, Niska, Test. W karcie pozycji pasek „Ile warte · Pewność · Wdrożenie”. Pod widoczną częścią karty zwinięte „Szczegóły” z dawną treścią karty (c_szkic.md, sekcja 3, ta sama pozycja), po zmianie słownika i z poprawkami z części 1.

### priorytety/wstep

Lista od najważniejszej pozycji. Przy każdej: dlaczego, co robimy, ile jest warta w złotych marży na rok, po czym poznamy, że zadziałała, i ile zajmie wdrożenie. Pełne rachunki i założenia są w szczegółach każdej karty.

### priorytety/zasady

Tytuł: Najpierw pewne straty i pauzy, które da się cofnąć, potem testy
Wniosek: Kolejność oznacza wagę decyzji. Każda kwota to osobny scenariusz, więc kwot nie sumujemy.
- Najpierw pewne straty, które rosną każdego dnia i łatwo je naprawić (pozycje 1 i 2). Potem pauzy, które da się cofnąć (3 i 4). Potem naprawy, diagnozy i testy, które mają wycenę (5–10). Test Mety (pozycja 9) ma nieznany znak, ale wycenę i największą stawkę, więc stoi w tej grupie. Na końcu dwie pozycje bez oszacowanego efektu: pozycja 11 ma tylko górną granicę możliwej korzyści, a pozycja 12 tylko koszt testu.
- W pierwszym tygodniu zespół może zrobić równolegle pozycje 1, 3 i 4 oraz pierwsze, krótkie kroki pozycji 2, 5, 6, 8 i 11 (decyzje na pierwszy tydzień w zakładce „Czy to wzrost”).
- Wartość to zmiana marży na rok: przychód z konsultacji po zwrotach i opłaty TelemediGO minus koszt lekarza, wydatki na kampanie i prowizja afiliacyjna. Rokiem bazowym są ostatnie 12 miesięcy.
- Pieniędzy uwolnionych przez pozycje 3 i 4 nie przesuwamy automatycznie do innych kampanii, tylko z testem.
Szczegóły: dawne zasady listy i definicje (c_szkic.md, sekcja 3, „Zasady listy”), słownikiem i z tym samym kryterium kolejności; definicje okresów: rok wcześniej = X 2024 – IX 2025, ostatnie 12 miesięcy = X 2025 – IX 2026; reguły: według pierwszego wejścia i według sesji z płatnością; nowe kampanie: meta_prosp_l4_szybko (Meta, od 3.11.2025) i tt_prosp_l4_15min (TikTok, od 9.02.2026).

### priorytety/1

Tytuł: Naprawić zakładanie konta w Safari na iPhone'ach
Wniosek: Od 17 marca 2026 nowi pacjenci na iPhone'ach rzadziej kończą zakładanie konta, co kosztuje około 100 pierwszych zamówień miesięcznie.
Pasek: 75–83 tys. zł (rocznie, górny scenariusz; w horyzoncie 180 dni 86–95 tys. zł) · Wysoka (awaria widoczna w danych) · diagnoza 1–2 dni, poprawka 2–5 dni, sprawdzenie 1 tydzień.
Wdrożenie (trzecia lista Kuby, punkt 4; ta sama wersja w przeglądzie i w pasku): diagnoza 1–2 dni (powtórzyć rejestrację na iPhonie, przejrzeć logi błędów rejestracji i listę zmian z 16–17 marca 2026, jak w c_szkic.md, pozycja 1), poprawka 2–5 dni (nasz szacunek; c_szkic.md mówi „zwykle dni”), sprawdzenie 1 tydzień (krok konta w Safari wraca z około 46% do około 66% w ciągu tygodnia od poprawki, jak w „Po czym poznamy”).
Dlaczego: W 60 dniach po awarii krok konta po wyborze terminu u osób, które jeszcze nie kupowały, przechodzi w Safari na iPhone'ach 45% sesji wobec 66% w 60 dniach przed nią, i do końca danych nie wraca. W innych przeglądarkach takiego spadku nie ma. (Runda F, poprawka 5: te same okna co wykres w karcie, 66,2% → 45,1%.)
Co robimy: Powtórzyć rejestrację na iPhonie, przejrzeć logi błędów rejestracji i listę zmian z 16–17 marca 2026, wdrożyć poprawkę.

### priorytety/2

Tytuł: Oczyścić codzienny raport i dodać alarmy na lejku i zwrotach
Wniosek: Raport pokazuje wzrost zamówień o 61% zamiast 56% i nie pokazuje ani marży, ani powrotów kohort.
Pasek: 0 albo 38 tys. zł (rocznie bezpośrednio; przede wszystkim warunek pozostałych decyzji) · Wysoka (oba błędy widoczne w danych) · 1 dzień sprawdzenie, 1–2 tygodnie raport.
Dlaczego: Awaria w Safari trwała 198 dni, do końca danych. Alarm na krokach lejka wykryłby ją po kilku dniach. Gdyby awarię wykryto i usunięto w ciągu tygodnia, strata wyniosłaby około 22–25 pierwszych zamówień zamiast 628–695. (Po przejrzeniu przez Codeksa, Sol: samo wykrycie nie zatrzymuje straty, więc zdanie mówi o wykryciu i usunięciu.)

### priorytety/3

Tytuł: Wstrzymać kampanię TikTok na L4
Wniosek: Kampania traci na każdym pozyskanym pacjencie według obu reguł przypisania, a jej pacjenci prawie nie wracają.
Pasek: +19 do +48 tys. zł (rocznie, nawet gdy każdy jej pacjent przyszedł tylko dzięki niej; więcej, gdy część przyszłaby i tak) · Wysoka (kampania traci według obu reguł przypisania; niepewna jest tylko wielkość zysku z pauzy) · 1 dzień.
Dlaczego: Wynik na pacjenta po koszcie pozyskania jest ujemny według obu reguł przypisania i po 90, i po 180 dniach. Nawet najkorzystniejsza naprawa zwrotów, czyli zmiana ich zasad, daje według pierwszego wejścia wynik bliski zera, a według sesji z płatnością dalej stratę.
Co robimy: Wstrzymać od razu, jako pauzę, którą da się cofnąć w jeden dzień. Naprawy obietnicy i ładowania strony sprawdzić najpierw na Mecie; TikTok może wrócić jako mały test, jeśli zadziałają.
Tabela (wiersze słowami): wynik dziś; po samej nowej kreacji reklamy (pozycja 5); po zmianie zasad zwrotów; zmiana marży po wyłączeniu, gdy każdy pacjent przyszedł tylko dzięki kampanii, gdy połowa przyszłaby i bez niej, gdy wszyscy przyszliby i bez niej.
Szczegóły (nowe): W scenariuszu samej nowej kreacji (pozycja 5), w którym uczciwa obietnica zniechęca osoby, które dostałyby zwrot, wynik w 234 dniach działania wynosi −6,1 tys. zł albo −27,8 tys. zł po 90 dniach i −7,7 tys. zł albo −29,4 tys. zł po 180 dniach, więc kampania nadal traci według obu reguł przypisania. Po zmianie zasad zwrotów +3,0 albo −23,2 tys. zł (dawniej „wariant A”).

### priorytety/4

Tytuł: Wstrzymać kampanię Google Ads na specjalistów do czasu zmiany cennika
Wniosek: Pozyskanie pacjenta kosztuje około 58 zł, a pacjent zostawia w 90 dniach około 32 zł marży.
Pasek: +19 do +32 tys. zł (rocznie, nawet gdy każdy jej pacjent przyszedł tylko dzięki niej; do +53 tys. zł, gdy przyszliby i bez niej) · Wysoka (kampania traci według obu reguł przypisania; niepewna jest tylko wielkość zysku z pauzy) · 1 dzień.
Dlaczego: Wizyta u specjalisty po cenie katalogowej zostawia ponad koszt lekarza tylko 9–19 zł, więc kampania nie ma z czego pokryć kosztu pozyskania (pozycja 10).
Co robimy: Wstrzymać. Wrócić po zmianie cennika albo gdy koszt pozyskania nie przekracza marży pacjenta w 90 dniach w obu regułach.
Po czym poznamy: Liczymy wszystkich nowych pacjentów z pierwszą wizytą u specjalisty, ze wszystkich kanałów (w ostatnich 12 miesiącach średnio 66 tygodniowo), i marżę całego biznesu po wydatkach, wobec tych samych tygodni rok wcześniej, tak jak w teście Mety. Pauza się opłaca, dopóki nowych pacjentów u specjalistów ubywa mniej niż około 31 tygodniowo; kampania przypisuje sobie 13–18 tygodniowo.
Tabela: tytuł „Kampania Google Ads na specjalistów: kwoty roczne z ostatnich 12 miesięcy”, wiersze słowami jak w pozycji 3.
Szczegóły (nowe): Próg = wydatki kampanii w ostatnich 12 miesiącach (53,2 tys. zł) podzielone przez marżę jej pacjenta w 90 dniach (32,4 zł według pierwszego wejścia, 32,9 zł według sesji z płatnością, bez zaokrąglenia): 1 640 albo 1 614 pacjentów rocznie. Kampania przypisuje sobie 923 albo 657 nowych pacjentów rocznie. Wszystkich nowych pacjentów z pierwszą wizytą u specjalisty (bez internisty, pediatry i psychiatry) było 3 427 w ostatnich 12 miesiącach i 2 971 rok wcześniej.

### priorytety/5

Tytuł: Zmienić obietnicę w reklamach Meta na L4; zasady zwrotów rozważyć osobno
Wniosek: 17% wizyt L4 z nowych kampanii kończy się zwrotem pieniędzy, wobec 5% u pozostałych pacjentów, a lekarz i tak dostaje wynagrodzenie.
Pasek: 11–18 tys. zł (rocznie za samą nową kreację; zmiana zasad zwrotów przy odmowie L4 to osobna decyzja: 27–46 tys. zł) · Średnia (nie znamy powodu zwrotów) · 1–2 tygodnie + 4–6 tygodni pomiaru.
Dwie różne decyzje:
- Nowa kreacja i pytanie przed płatnością („lekarz wystawia L4 tylko przy wskazaniach medycznych”). Uczciwa obietnica zniechęca część osób, które i tak dostałyby zwrot. Warta 10,7–18,1 tys. zł rocznie, zależnie od reguły przypisania.
- Zmiana zasad zwrotów przy odmowie L4: wizyta zostaje opłacona, bo pacjent dostał konsultację. Warta 26,7–46,5 tys. zł rocznie, ale to osobna decyzja z ryzykiem prawnym i wizerunkowym (Czego nie wiemy, punkt 17).
- Obie kwoty to scenariusze tych samych zwrotów, więc się nie sumują. Po wstrzymaniu TikToka dotyczą tylko Mety.
Co robimy: Najpierw jednodniowe sprawdzenie, co obiecują reklama, strona wejścia i regulamin przy odmowie L4. Potem w Mecie losowy podział ruchu na starą i nową kreację. Przy okazji przetestować wysokość kodu rabatowego (dziś 20 zł).
Szczegóły (nowe): wariant kreacji (dawniej „dolny”, w tabelach pozycji 3 i 9 „po samej nowej kreacji”): 16,5 tys. zł w 332 dniach działania kampanii według pierwszego wejścia i 9,7 tys. zł według sesji z płatnością, na pełny rok 18,1 i 10,7 tys. zł; wariant zasad zwrotów (dawniej „górny”, „wariant A”): 42,3 i 24,3 tys. zł, na pełny rok 46,5 i 26,7 tys. zł. 1 024 to zwroty przy samych wizytach L4. Zakładka „Po zakupie” pokazuje 1 044 zwroty po wizycie u pacjentów nowych kampanii, bo liczy wszystkie cele wizyty, także e-receptę i konsultację (analiza/wyniki/e_poprawki.txt, punkt 2).

### priorytety/6

Tytuł: Zdiagnozować poranne opóźnienia internistów, potem przetestować obsadę
Wniosek: Od lutego 2026 około połowy porannych wizyt u internisty zaczyna się ponad 15 minut po terminie; do października 2025 było to 5–7%.
Pasek: 0–65 tys. zł (rocznie, scenariusz; wariant wąski około 12 tys. zł; bez kosztu obsady) · Niska (opóźnienia są pewne; nie wiemy, ile powrotów przywróci punktualność) · diagnoza 1–2 dni, test 2–4 tygodnie.
Dlaczego: To jedna z konkretnych hipotez spadku retencji w kanałach działających w obu latach, a pierwszy krok, diagnoza, jest tani. W ostatnich 12 miesiącach pacjenci po spóźnionej porannej pierwszej wizycie wracają rzadziej niż po punktualnej, a spóźnione wizyty mają dużo niższe oceny (zakładka „Po zakupie”).
Szczegóły (nowe; jedna wersja liczb z „Po zakupie” i zdarzeniem na osi): Od listopada 2025 do lutego 2026 poranne opóźnienia u internisty rosły z miesiąca na miesiąc, a potem utrzymywały się na poziomie około połowy wizyt. Odsetek wizyt z terminem 6:00–11:59, które zaczynają się ponad 15 minut po terminie (pacjenci spoza nowych kampanii), wynosi 15,7% w listopadzie 2025, 29,7% w grudniu i 42,6% w styczniu 2026, a od lutego do września 2026 około połowy (47,3–52,7% miesięcznie). Od października 2024 do października 2025 było to 4,7–6,9% miesięcznie. Blok poranny: od 5:00 do 13:59, najsilniej od 6:00 do 11:59.

### priorytety/7

Tytuł: Wprowadzić komunikację po wizycie, zawsze z losową grupą bez wysyłki
Wniosek: Co siódmy powrót zaczyna się od wejścia z newslettera albo SMS-a, ale nie wiemy, ile z tych zakupów wiadomość faktycznie wywołała.
Pasek: 23,6 tys. zł (za każdy punkt procentowy powrotu w 90 dniach; marża do 180. dnia; scenariusz) · Niska (nie wiemy, ile powrotów wywoła sama wiadomość) · dane o wysyłkach kilka dni, sekwencja 2–4 tygodnie, pomiar 90 dni.
Dlaczego: Retencja spada także poza nowymi kampaniami: w 90 dniach wraca 22% pacjentów wobec 24% rok wcześniej. Około 3 z tych 22 punktów procentowych to pacjenci, którzy wrócili w ciągu doby po kliknięciu newslettera albo SMS-a; pozostali wrócili inną drogą. To jedna grupa pacjentów podzielona według drogi powrotu.
Szczegóły (nowe): Każdy punkt procentowy powrotu w 90 dniach to około 23,6 tys. zł marży rocznie: 24 687 nowych pacjentów × 1% × 95,6 zł, gdzie 95,6 zł to różnica marży do 180. dnia między pacjentem, który wrócił w 90 dniach, a takim, który nie wrócił. Bez pacjentów nowych kampanii (17 419) 16,7 tys. zł. To różnica obserwacyjna; efektu samej wiadomości nikt jeszcze nie zmierzył. Podział powrotu w 90 dniach poza nowymi kampaniami (22,0%) według drogi powrotu: 3,16% po wejściu z newslettera albo SMS-a i 18,84% inną drogą; rok wcześniej 3,48% i 20,42%.

### priorytety/8

Tytuł: Sprawdzić ręcznie zakup dla pacjentów zalogowanych od wejścia
Wniosek: Żadna z 22 tys. sesji pacjentów zalogowanych od wejścia nie skończyła się zakupem konsultacji; jeden ręczny test pokaże, czy to błąd ścieżki zakupu.
Pasek: 0 albo 36–40 tys. zł (rocznie; wysoki scenariusz 89 tys. zł) · Niska (dane wskazują raczej na 0 zł) · 1 dzień.
Co robimy: Zalogować się, wejść ponownie już zalogowanym, spróbować kupić bez ponownego logowania i sprawdzić, jakie kroki zapisała analityka.

### priorytety/9

Tytuł: Sprawdzić testem w części kraju, czy kampania Meta na L4 się opłaca
Wniosek: Według pierwszego wejścia kampania zarabia 31 tys. zł rocznie, według sesji z płatnością traci 32 tys. zł, a dane nie mówią, ilu jej pacjentów przyszłoby i bez niej.
Pasek: od −31 do +180 tys. zł (rocznie: tyle warta jest decyzja o wyłączeniu, zależnie od tego, ilu pacjentów przyszłoby i bez kampanii) · Test · 1 tydzień + 4–6 tygodni.
Dlaczego dopiero 9. miejsce: To największa kwota na liście, ale nie znamy nawet jej znaku, a test w 4–6 tygodni da tylko orientacyjny wynik. Wcześniej idą pewne straty i tanie kroki, które zespół może zrobić od razu.
Co robimy: Na 4–6 tygodni wyłączyć kampanię w połowie województw, losowo w parach podobnych województw, i porównać wszystkich nowych pacjentów oraz marżę. Wyłączamy na stałe, jeśli w województwach bez reklamy, w porównaniu z ich parami, ubędzie mniej nowych pacjentów niż około 85% tych, których kampania sobie tam w tym czasie przypisuje. Po samej nowej kreacji z pozycji 5 ten próg spada do około 79%, a po zmianie zasad zwrotów do około 70% (progi dla marży w 90 dniach: 78,7% i 70,0%).
Gdy wynik testu jest niejednoznaczny, i tak decydujemy według jego wyniku: poniżej progu wyłączamy, powyżej zostawiamy. Taki wynik może przez przypadek wypaść po złej stronie progu, ale obie decyzje da się cofnąć, a pomiar powtórzyć.
Tabela (wiersze słowami): jak w pozycji 3.

### priorytety/10

Tytuł: Zmienić cennik specjalistów i warunki TelemediGO u specjalistów
Wniosek: Wizyta u specjalisty zostawia ponad koszt lekarza tylko 9–19 zł, a ze zniżką TelemediGO przynosi stratę.
Pasek: 15–31 tys. zł (rocznie za warunki TelemediGO po pełnym roku; cennik do 74 tys. zł za każde 10 zł podwyżki, górna granica) · Średnia (kierunek jest pewny; nie wiemy, ile da zmiana cennika) · 1–2 tygodnie + test dwóch cen 4 tygodnie.
Co robimy:
- Ustawić zniżkę TelemediGO u specjalistów tak, żeby cena nie spadała poniżej kosztu lekarza: najwyżej około 8% przy cenie 109 zł.
- U pediatry i psychologa samo wyłączenie zniżki nie wystarczy, bo już cena katalogowa (95 i 99 zł) jest niższa niż koszt lekarza (100 zł, przy założeniu opartym na zadaniu). Tu trzeba podnieść cenę.
- Przetestować dwie ceny dla nowych pacjentów przez 4 tygodnie i mierzyć marżę na sesję, nie sam odsetek kupujących.
Szczegóły (nowe): Stawka lekarza 100 zł za wizytę u pediatry to założenie oparte na zadaniu: 25 zł internista, 200 zł psychiatra, 100 zł każdy inny specjalista. Sprawdzenie wrażliwości: przy stawce 25 zł, jak u internisty, marża na pacjenta w 90 dniach rośnie o 3,7–4,8 zł.

### priorytety/11

Tytuł: Sprawdzić, gdzie znika ruch między kliknięciem reklamy a wejściem na stronę w Meta i TikToku
Wniosek: Na kliknięcie w Meta przypada 0,8 sesji, a w Google Ads 0,9; nie wiemy, czy ludzie porzucają ładowanie strony, czy panel liczy kliknięcia inaczej.
Pasek: 0 albo do 52 tys. zł (rocznie, górna granica; po wstrzymaniu TikToka mniej) · Niska (nie wiemy, czy brakujące sesje da się odzyskać) · 1–2 dni.
Co robimy: Porównać w panelach Meta i TikToka kliknięcia w link i wyświetlenia strony docelowej z sesjami w analityce, dzień po dniu, i zmierzyć czas ładowania strony w przeglądarkach w aplikacjach.
Po czym poznamy: Wiemy, czy brakujące sesje to ludzie, którzy porzucają ładowanie strony (do odzyskania), czy inny sposób liczenia kliknięć w panelu (wtedy pozycja jest warta 0 zł). Wynik zmienia ocenę pozycji 3 i 9.

### priorytety/12

Tytuł: Sprawdzić losowym testem, ile wizyt i powrotów dokłada zniżka TelemediGO
Wniosek: Kupujący TelemediGO wracają częściej, ale nie wiemy, czy to skutek zniżki, czy tego, że kupują ci, którzy i tak planują wracać.
Pasek: koszt 3–12 tys. zł (zniżki przy niezmienionej liczbie wizyt) · Test · 2–8 tygodni + 90 dni.
Co pokaże: Test pokaże wpływ samej zniżki na wizyty, powroty i marżę. Nie pokaże, czy opłaca się oferta za 89 zł, bo uczestnicy dostają zniżki bez opłaty. Od wyniku zależy, czy program promować, czy przebudować razem z pozycją 10.
Szczegóły (nowe; koszt testu podany raz): Koszt testu (3,3–12,2 tys. zł zniżek dla 487–1 823 pacjentów w grupie z dostępem) liczymy przy niezmienionej liczbie wizyt; jeśli zniżka doda wizyt, koszt będzie wyższy.

### priorytety/nie_robimy

Tytuł: Nie robimy teraz rzeczy bez podstaw w danych albo bez testu
- Kampanii o zgodę marketingową pacjentów nowych kampanii: w najlepszym razie 1,9 tys. zł rocznie.
- Osobnej naprawy przeglądarek w aplikacjach w reklamach do nowych osób: w tej samej kampanii płacą tak samo jak zwykłe.
- Mocniejszej sprzedaży i odnowień TelemediGO: dopiero po teście z pozycji 12.
- Przesuwania uwolnionego budżetu do innych kampanii bez testu.

## 3. Czego nie wiemy

Dawna pozycja 13 (stawka lekarza u pediatry) wypada: to założenie oparte na zadaniu, a wariant 25 zł jest sprawdzeniem wrażliwości w pozycji 10. Pozycje 14–22 mają teraz numery 13–21.

### niewiadome/wstep

Rzeczy, których te dane nie rozstrzygają, i test albo dane, które je domkną. Numer pozycji listy priorytetów prowadzi do karty, której kwota od tego zależy.

### niewiadome/1

Co: Ilu pacjentów nowych kampanii na L4 przyszłoby i bez nich.
Dlaczego (zaokrąglone; dokładne kwoty w pozycji 9): od tego zależy decyzja o kampanii Meta na L4: jej wyłączenie jest warte od około −31 do +180 tys. zł rocznie, a próg decyzji to około 85% pacjentów, którzy bez kampanii by nie przyszli (pozycja 9).

### niewiadome/2

Co: Ilu pacjentów kampanii bez kodu rabatowego (Google Ads ogólne, Meta „lekarz online”) przyszłoby i bez reklamy.
Dlaczego: znak wyniku tych kampanii zależy od reguły przypisania, a żadna reguła nie mówi, ilu pacjentów kampania naprawdę dokłada.
Test: ten sam test z grupą bez reklamy; mierzy przyrost pacjentów niezależnie od reguły przypisania, więc nie trzeba wybierać reguły.

### niewiadome/8

Co: Ile wizyt i powrotów dokłada zniżka TelemediGO.
Dlaczego: od tego zależy, czy program promować; test pokaże wpływ samej zniżki, ale nie opłacalność oferty za 89 zł.
Test: losowy, bezpłatny dostęp do zniżek (pozycja 12).

### niewiadome/3

Dlaczego (zaokrąglone jak w pasku pozycji 5): po wstrzymaniu TikToka dotyczy tylko Meta: od niego zależy, ile da nowa kreacja (11–18 tys. zł rocznie) i czy potrzebna jest zmiana zasad zwrotów (27–46 tys. zł rocznie; pozycja 5).

### niewiadome/4

Co: Skąd poranne opóźnienia u internistów (blok od 5:00 do 13:59, już przy wizytach z najwcześniejszym terminem dnia, bez widocznego narastania w ciągu poranka) i czy obniżają powroty.
Dlaczego: scenariusz od 0 do 65 tys. zł rocznie. Luty 2026 nie pasuje do hipotezy, że większe opóźnienia zawsze obniżają powrót: opóźnienia były już wtedy wysokie, a powrót pacjentów kampanii działających w obu latach nie spadł (notatki/a5_retencja.md, krok 5: w lutym 49,4% spóźnionych, powrót +1,2 punktu).

### niewiadome/11

Co: Ile wzrostu daje pora roku, a ile wyższe wydatki na kampanie.
Dlaczego: od X 2024 do I 2025 rosną naraz pora roku i wydatki. W dwóch latach danych każdy miesiąc występuje tylko dwa razy, a wydatki rosły w obu latach, więc wpływu sezonu nie da się oddzielić od wpływu wydatków.

### niewiadome/19

Co: Czy sesje w przeglądarkach w aplikacjach płacą rzadziej w remarketingu Meta, kampanii Google Ads na markę i wejściach bezpośrednich przez samą przeglądarkę, czy przez to, kto z niej korzysta (bez pojęcia „osoby, które znają stronę”).

## 4. Lejek — nagłówek i karty napraw (część 1, punkt 4)

### lejek/naglowek

Trzecia lista Kuby (2026-10-22, punkt 1): dawne „poza sesjami z nowych kampanii konwersja się nie zmieniła” wynikało z reguły według sesji. Według pierwszego wejścia, tak jak w retencji, nowe osoby spoza nowych kampanii płacą od kwietnia 2026 rzadziej, i prawie cały ten spadek to Safari na iPhone'ach (analiza/wyniki/e_poprawki.txt, punkt 3). Nagłówek nazywa więc i zmianę ruchu, i awarię Safari. Po recenzji Codeksa (notatki/recenzje/e3_codex.md): tytuł jako składniki spadku zamiast „dwóch powodów”, „bez istotnej zmiany” zamiast „nie zmieniła się”, „o połowę rzadziej” na tych samych miesiącach (IV–IX 2026: 5,30% wobec 10,26%), „pogorszenie skupia się na kroku konta” zamiast „cały spadek”, okresy sesji powrotnych nazwane osobno, sprawdzenie reguły łączenia osób.

Tytuł: Na spadek konwersji nowych osób składają się głównie dwie rzeczy: więcej ruchu z nowych kampanii na L4 i awaria zakładania konta w Safari
Wniosek (ile płacą dziś, analiza/wyniki/e_poprawki.txt, punkt 1): Od kwietnia do września 2026 płatnością kończy się około 8% sesji osób, które jeszcze nie kupowały, a w tych samych miesiącach rok wcześniej około 11%.
- Do stycznia 2026 nowe osoby płaciły prawie tak samo często jak rok wcześniej, choć ruchu z nowych kampanii na L4 przybywało już od listopada 2025. W lutym 2026, gdy ruszył TikTok na L4, sesje nowych kampanii przekroczyły 30% ruchu nowych osób, a od kwietnia to prawie połowa. Te sesje płacą o połowę rzadziej niż pozostałe. (Runda F, P4: wykres udziału na tej samej zakładce pokazuje wzrost od listopada 2025: 10%, 18%, 24% i 32% sesji nowych osób w kolejnych miesiącach; kod sprawdza, że udział rośnie od listopada i przekracza 30% dopiero w lutym.)
- Wśród pozostałych nowych osób od kwietnia 2026 wyraźnie płacą rzadziej tylko sesje w Safari na iPhone'ach: około 8% wobec 12% rok wcześniej. Spadek skupia się na kroku zakładania konta, który działa gorzej od 17 marca 2026. W innych przeglądarkach konwersja jest bez istotnej zmiany.
- Liczba płatności nowych osób rośnie, spada tylko ich odsetek.
- Safari trzeba naprawić (pozycja 1 listy priorytetów). Do sprawdzenia jest niższa konwersja przeglądarek w aplikacjach w remarketingu Meta, kampanii Google Ads na markę i wejściach bezpośrednich (karta niżej).
Zastrzeżenie: Niższa konwersja nie mówi, ilu pacjentów nowe kampanie dokładają, bo nie wiemy, ilu z nich przyszłoby i bez reklamy.
Szczegóły:
- Ile płacą dziś: od kwietnia do września 2026 płatnością kończy się 8,41% z 146 402 sesji osób, które jeszcze nie kupowały (od 8,11% do 8,87% miesięcznie), a w tych samych miesiącach rok wcześniej 11,12% z 65 262 sesji. Średnia z całych ostatnich 12 miesięcy to 9,3% wobec 11,2% rok wcześniej.
- Przebieg rok do roku: od października 2025 do stycznia 2026 konwersja była o 0,2–0,8 punktu procentowego niższa niż rok wcześniej, w lutym i marcu 2026 o 1,5–1,6 punktu, a od kwietnia 2026 o 2,3–3,1 punktu. Sesje nowych kampanii przekroczyły 30% ruchu nowych osób w lutym 2026 (31,8%), a od kwietnia to 42–47% (tabela niżej).
- Sesje z reklam nowych kampanii płacą w 5,5% (94 462 sesje w ostatnich 12 miesiącach; od kwietnia do września 2026 5,30% z 66 725 sesji). Nowe osoby spoza nowych kampanii liczymy według pierwszego wejścia, tak jak pacjentów i retencję: od kwietnia do września 2026 płaci 10,26% z 71 441 sesji, a w tych samych miesiącach rok wcześniej 11,12% z 65 262 sesji (zmiana −0,86 punktu procentowego). W całych ostatnich 12 miesiącach 10,9% wobec 11,2% rok wcześniej.
- Safari na iPhone'ach i iPadach w tej grupie, od kwietnia do września 2026: płaci 8,27% z 14 323 sesji wobec 11,99% z 12 887 rok wcześniej, a krok konta po wyborze terminu przechodzi 45,7% sesji wobec 67,0%. Pogorszenie skupia się na kroku konta; pozostałe kroki w Safari prawie się nie zmieniają. Pozostałe przeglądarki: 10,76% z 57 118 sesji wobec 10,91% z 52 375 (zmiana −0,15 punktu, 95% przedział od −0,52 do +0,22, czyli bez istotnej zmiany), krok konta 65,4% wobec 66,4%. Od października 2025 do lutego 2026, przed awarią, Safari płaciło tak jak rok wcześniej: 12,07% wobec 12,15%. Sprawdzenie reguły łączenia osób (osoba z reklamy L4, która wróciła w innej przeglądarce bez logowania, liczy się do pozostałych): bez wszystkich osób, których pierwsze zamówienie to L4, w obu latach, Safari spada o 2,81 punktu, a pozostałe przeglądarki są bez istotnej zmiany (−0,05 punktu, przedział od −0,39 do +0,29).
- Podział zmiany od kwietnia do września 2026 (opisowo, czyli bez mierzenia wpływu): z −0,86 punktu u nowych osób spoza nowych kampanii −0,74 punktu to spadek w Safari, −0,12 punktu spadek w pozostałych przeglądarkach, a zmiana udziału Safari w ruchu daje około zera. Dla wszystkich nowych osób (−2,71 punktu, z 11,12% do 8,41%) zmiana struktury ruchu daje −2,07 punktu, spadek w Safari −0,55 punktu, a spadek w pozostałych przeglądarkach −0,09 punktu.
- Licząc według sesji, czyli bez samych sesji z reklam nowych kampanii, konwersja pozostałych sesji rośnie z 11,2% do 11,4%, a od kwietnia do września 2026 stoi (11,02% wobec 11,12%). W całych ostatnich 12 miesiącach ta reguła zostawia w średniej 11 577 sesji, w których osoby nowych kampanii wracają bezpośrednio, z wyszukiwarki albo z innej reklamy. Płaci w nich 18,0% (2 081 płatności, czyli ci sami pacjenci, których w retencji obie reguły przypisują różnie). Od kwietnia do września 2026 to 8 236 sesji, w których płaci 17,6%. Te sesje podnosiły średnią i przykrywały spadek w Safari.
- Tabela miesięcy dla Safari i pozostałych przeglądarek w tej grupie: liczby z analiza/wyniki/e_poprawki.txt, punkt 3 (odsetek sesji z płatnością w ostatnich 12 miesiącach, zmiana wobec tego samego miesiąca rok wcześniej, krok konta, pod nimi rok wcześniej i liczba sesji).
- Osoby, które jeszcze nie kupowały: 144 813 sesji i 16 232 płatności rok wcześniej, 265 264 sesji i 24 686 płatności w ostatnich 12 miesiącach. Najbardziej pogorszyło się przejście do wyboru usługi (z 33,7% do 30,6% sesji) i krok konta po wyborze terminu (z 66,4% do 62,6%).
- Wszystkie sesje, także osób, które już kupowały (płacą w 91,5% i 89,9% sesji): 16,0% rok wcześniej (154 085 sesji, 24 717 płatności) i 13,7% w ostatnich 12 miesiącach (280 625 sesji, 38 490 płatności).
- Podział zmiany konwersji osób, które jeszcze nie kupowały, według kampanii (opisowo, czyli bez mierzenia wpływu): zmiana struktury ruchu −1,43 punktu, zmiana w obrębie kampanii −0,47 punktu. Nowe kampanie nie mają roku wcześniej, więc liczą się w całości do struktury.
- Miesiące (tabela): konwersja nowych osób w ostatnich 12 miesiącach, rok wcześniej, zmiana i udział sesji nowych kampanii — liczby z analiza/wyniki/e_merytoryka.txt, punkt 4.
- Dawne zdania o rozkładzie wszystkich sesji według przeglądarki i kampanii (d_teksty_strony.md, „Rozkład zmiany konwersji”), z udziałem przeglądarek wbudowanych w aplikacje: z 10,7% do 35,6% sesji; wynik rozkładu według przeglądarki podany raz. Na początku dopisane „w całych ostatnich 12 miesiącach”, żeby „prawie cały spadek to zmiana ruchu” (wszystkie sesje, cały rok) nie czytało się jak zaprzeczenie awarii Safari od kwietnia 2026.

### lejek/safari

Tytuł: Od 17 marca 2026 nowi pacjenci w Safari na iPhone'ach rzadziej kończą zakładanie konta
Znacznik: Do naprawy.
Wniosek (ta sama wersja co pozycja 1 listy priorytetów): W 60 dniach po awarii krok konta po wyborze terminu przechodzi 45% sesji wobec 66% w 60 dniach przed nią i do końca danych nie wraca, a w innych przeglądarkach prawie się nie zmienił. (Runda F, poprawka 5: wykres karty porównuje teraz oba wiersze na tych samych oknach, 60 dni przed awarią i po niej: Safari 66,2% → 45,1%, pozostałe przeglądarki 64,8% → 63,4%; wcześniej zdanie podawało 66% → 46%, czyli okres do końca danych, 66,1% → 45,6%, który zostaje w szczegółach i w przypisie wykresu.)
- Konta dalej powstają, ale rzadziej. To około 100 utraconych pierwszych zamówień miesięcznie.
- Od kwietnia 2026 to prawie cały spadek konwersji nowych osób spoza nowych kampanii na L4 (trzecia lista Kuby, punkt 1; nagłówek lejka, szczegóły: Safari −0,74 z −0,86 punktu, czyli około 86%; Codex uznał brzmienie za uzasadnione opisowo).
Szczegóły (bez powtórzenia punktu z widocznej części): Krok konta po wyborze terminu u osób, które jeszcze nie kupowały: 66,1% od 1.10.2025 do 16.03.2026 i 45,6% od 17.03 do 30.09.2026 (4 678 sesji z wyborem terminu). W 60 dniach przed awarią i po niej: 66,2% (16.01.2026–16.03.2026, 1 763 sesje) i 45,1% (17.03.2026–15.05.2026, 1 553 sesje); pozostałe przeglądarki w tych samych dniach 64,8% i 63,4%. Szacunek: 628–695 utraconych pierwszych zamówień do 30.09.2026, czyli 95–105 na 30 dni.

### lejek/przegladarki

Tytuł: Przeglądarki w aplikacjach płacą rzadziej niż zwykłe w remarketingu, kampanii na markę i wejściach bezpośrednich
Znacznik: Do sprawdzenia (nie ma ich na liście priorytetów; test w „Czego nie wiemy”, punkt 18).
Wniosek: W tych kampaniach różnica wynosi 4–12 punktów procentowych, a w reklamach Meta i TikTok na L4, które trafiają do nowych osób, jej nie ma.
- Niska konwersja kampanii na L4 nie wynika więc wyraźnie z przeglądarki. Przyczynę różnicy w pozostałym ruchu trzeba sprawdzić, zanim zaplanujemy naprawę (Czego nie wiemy, punkt 18).
Zastrzeżenie: To porównanie obserwacyjne: nie rozdziela wpływu przeglądarki od tego, kto z niej korzysta.
Szczegóły: dawne zdanie z d_teksty_strony.md („Przeglądarki wbudowane w aplikacje”), w którym „ruch osób, które znają już stronę” jest zdefiniowany wprost: remarketing Meta, Google Ads na markę i wejścia bezpośrednie (12,2, 5,1 i 4,4 punktu); bez powtórzonego zastrzeżenia. Dla porównania cały ruch osób, które jeszcze nie kupowały (wszystkie kampanie razem): przeglądarki w aplikacjach płacą w obu latach w 3,8–6,6% sesji, a Chrome i Safari w 9,9–12,2%. Usługę wybiera 18,5–24,9% sesji w przeglądarkach w aplikacjach (Chrome i Safari 34,3–35,9%), termin 53,9–60,6% tych, które wybrały usługę (wobec 67,7–68,6%), a krok konta 56,0–60,0% tych, które wybrały termin (wobec 56,7–66,9%; najniżej Safari po awarii).

### lejek/osobne

Tytuł (wniosek zamiast tematu; strona używa go jako napisu zwijanej sekcji): Sesje zalogowane od wejścia nie kończą się płatnością, a ponad co piąte konto nie ma żadnego zakupu.
Treść (okresy: rok wcześniej (X 2024 – IX 2025), ostatnie 12 miesięcy (X 2025 – IX 2026)): dawne zdania (sesje zalogowane od wejścia, zakupy samego TelemediGO, konta bez zakupu) po zmianie słownika; liczby jak dotąd: 8 026 i 14 042 sesje, 20,7%, 112 sesji, 225 i 461 zakupów, 11 482 z 52 400 kont (21,9%), 21,3% z 20 620, 22,3% z 31 780, 37,1%, 58,1%, 30.09.2026.

## 5. Kohorty — zdanie nad miesięczną mapą (polecenie Kuby przez sesję grafiki, 2026-10-22)

### kohorty/macierz

Od listopada 2025 kohorty wracają rzadziej, a od marca 2026 spadek się pogłębia: w ciągu 90 dni wraca około 15% nowych pacjentów, wobec około 24% w kohortach do października 2025.
Skąd: kohorty miesięczne, wszyscy nowi pacjenci, powrót w ciągu 90 dni, tylko miesiące z pełnym oknem: X 2024 – X 2025 razem (17 614 pacjentów) i III – VI 2026 razem (9 111 pacjentów). Każdy miesiąc od XI 2025 ma niższy powrót niż każdy miesiąc do X 2025, a każdy od III 2026 niższy niż każdy z XI 2025 – II 2026 (sprawdza kod).
