# Recenzja: nowy werdykt pierwszej zakładki „Czy to wzrost” (runda G, 2026-10-23)

Jesteś niezależnym drugim recenzentem. Pracujesz w repozytorium zadania rekrutacyjnego (dane syntetyczne, wygenerowane na potrzeby zadania). Niczego nie zmieniaj w plikach. Odpowiedz po polsku.

## Kontekst

Firma pyta, czy to, co widać na dashboardzie (+52% nowych pacjentów, +61% zamówień, +50% przychodu, +40% TelemediGO; ostatnie 12 miesięcy X 2025 – IX 2026 wobec X 2024 – IX 2025), jest wzrostem, rozumianym jako jednocześnie więcej pacjentów i lepsza retencja. Pierwsza zakładka narzędzia odpowiada „Nie”. Właściciel zapytał, dlaczego „Nie”, skoro marża po wszystkich kosztach wzrosła o 27% (z 828 do 1 048 tys. zł). Jego hipoteza została sprawdzona kodem i przepisana na nowy werdykt.

Pliki do przeczytania:
- `analiza/g_werdykt.py` (nowy skrypt) i jego wynik `analiza/wyniki/g_werdykt.txt` (sekcje G1–G4);
- `analiza/definicje.py` (przyjęte definicje: nowy pacjent, powrót, źródło pozyskania według pierwszego wejścia „Z1K” i według sesji z płatnością „Z2”, marża);
- `analiza/a5e_ekonomia.py` (ekonomia kampanii: koszt pozyskania = wydatki kampanii z dni kohort / nowi pacjenci; marża na pacjenta w N dniach);
- `notatki/ZALOZENIA.md`, punkty 16–43 (definicje i założenia), oraz `notatki/e_teksty.md`, sekcja 1 (szkic tekstów);
- baza `analiza/telemedi.duckdb` (otwieraj tylko do odczytu: `duckdb.connect(ścieżka, read_only=True)`; schemat `czyste`).

Zasady biznesowe: koszt lekarza za odbytą wizytę 25 zł internista, 200 zł psychiatra, 100 zł pozostali (także za wizytę zwróconą); prowizja afiliacyjna 25 zł za pierwsze opłacone zamówienie pacjenta; TelemediGO 89 zł.

## Co sprawdzić

1. **Liczby, własnym kodem, niezależnie od `g_werdykt.py`** (możesz użyć `definicje.py`, ale nie kopiuj obliczeń z `g_werdykt.py`):
   a) udział dwóch nowych kampanii na L4 (`meta_prosp_l4_szybko`, `tt_prosp_l4_15min`) w przyroście nowych pacjentów: 86,0% według pierwszego wejścia, 61,3% według sesji z płatnością (przyrost 16 231 → 24 687);
   b) wynik na pacjenta w 180 dniach (marża w 180 dniach minus koszt pozyskania), pierwsze zakupy 1.10–3.04 w obu latach: nowe kampanie na L4 +7,0 zł (2 352 pacjentów), pozostałe kampanie płatne +29,7 zł (5 130) i rok wcześniej +31,8 zł (4 717); według sesji z płatnością −5,2 zł, 27,5 zł i 30,0 zł;
   c) nowe kampanie na L4 razem, miesiąc po miesiącu (według pierwszego wejścia): koszt pozyskania, marża w 180 dniach (od kwietnia 2026 przybliżona: marża w najdłuższym pełnym oknie + średni przyrost do 180 dni zmierzony na kohortach z pełnym oknem) i wynik; w szczególności II kwartał 2026 +0,7 zł i III kwartał 2026 +0,4 zł na pacjenta, oraz według sesji z płatnością od kwietnia od −11,6 do −15,9 zł;
   d) rozbicie przyrostu marży po wszystkich kosztach 828 085 → 1 048 069 zł: pacjenci pozyskani w pierwszym roku, ich zakupy w drugim roku, 194 434 zł (88,4% przyrostu); pacjenci pozyskani w danym roku po kosztach kampanii i prowizji 828 085 → 853 635 zł (+3,1%), na nowego pacjenta 51,02 → 34,58 zł.
   Podaj przy każdej liczbie: zgodna / niezgodna (z Twoją wartością) i krótko, jak liczyłeś.

2. **Metoda.** Czy coś w metodzie zmienia wniosek? W szczególności: przybliżenie marży w 180 dniach dla młodszych kohort; łączenie wydatków z kohortami po dniu kalendarzowym; porównanie „pacjenci pozyskani w danym roku” rok do roku (obie strony mają ten sam rozkład czasu obserwacji w roku?); start danych od zera (w pierwszym roku nie ma pacjentów z poprzedniego roku).

3. **Brzmienie: czy któreś zdanie mówi więcej, niż pokazują liczby?** Szczególnie:
   - zdanie główne werdyktu (całe);
   - „od wiosny wychodzimy na zero” (według pierwszego wejścia; według sesji z płatnością tracimy);
   - „Marża po wszystkich kosztach wzrosła o 27% prawie wyłącznie dzięki pacjentom z pierwszego roku”;
   - „88% tego przyrostu to kolejne zakupy pacjentów pozyskanych w pierwszym roku, a nie lepszy wynik na nowych pacjentach”;
   - „Wzrost liczby pacjentów zależy od dwóch kampanii, a nie od szerszego popytu”;
   - „Nowe kampanie kupują liczbę pacjentów, ale prawie nie kupują zysku, a od wiosny koszt pozyskania zjada całą marżę ich pacjenta”;
   - „Sam przyrost liczby pacjentów prawie nie podniósł zysku”;
   - „Marża po kosztach kampanii już nie rośnie: w III kwartale 2026 była na poziomie roku wcześniej”.
   Dla każdego zdania: w porządku / za mocne (dlaczego) / propozycja brzmienia.

4. Czy czytelnik z firmy, który zobaczy tylko tę zakładkę, zrozumie, dlaczego „Nie”, skoro marża wzrosła o 27%? Co jest niejasne?

Odpowiedz w punktach 1–4, zwięźle. Na końcu tabela: zgłoszenie, waga (błąd / za mocne / drobne), propozycja.

## Tekst pierwszej zakładki (z rozwiniętymi szczegółami), tak jak widzi go czytelnik

```
Czy to, co widać na dashboardzie, jest wzrostem?

Wzrost to dwie rzeczy naraz: więcej pacjentów i lepsza retencja. Sprawdzamy oba warunki osobno, na danych oczyszczonych, porównując ostatnie 12 miesięcy (X 2025 – IX 2026) z rokiem wcześniej (X 2024 – IX 2025). Na końcu sprawdzamy, ile biznes na tym zarabia.

Nie

Prawie cały przyrost pacjentów (86%) dały dwie nowe kampanie na L4, a na ich pacjencie po koszcie pozyskania prawie nic nie zostaje: 7 zł w ciągu 180 dni wobec 30 zł na pacjencie pozostałych kampanii płatnych, a od wiosny wychodzimy na zero. Marża po wszystkich kosztach wzrosła o 27% prawie wyłącznie dzięki pacjentom z pierwszego roku. Pacjenci pozyskani w ostatnich 12 miesiącach zarobili po kosztach kampanii tylko o 3% więcej niż ci pozyskani rok wcześniej, choć było ich o 52% więcej.

Więcej pacjentów
Tak, ale
Nowych pacjentów jest o 52% więcej niż rok wcześniej, ale bez dwóch nowych kampanii na L4 tylko o 7%.
Lepsza retencja
Nie
W ciągu 90 dni wraca 17% nowych pacjentów, a rok wcześniej wracało 24%; rzadziej wracają też pacjenci spoza nowych kampanii.
Więcej zarabiamy
Tak, ale
Marża po wszystkich kosztach wzrosła z 828 do 1 048 tys. zł, ale 88% tego przyrostu to kolejne zakupy pacjentów pozyskanych w pierwszym roku, a nie lepszy wynik na nowych pacjentach.

Zastrzeżenie
Nie wiemy, ilu pacjentów nowych kampanii przyszłoby i bez reklamy. Odpowie na to test z pozycji 9 listy priorytetów: wyłączenie kampanii Meta na L4 na 4–6 tygodni w losowej połowie województw i porównanie wszystkich nowych pacjentów z drugą połową. Priorytety: pozycja 9, test w części kraju

86%
uwaga
przyrostu nowych pacjentów dały dwie nowe kampanie na L4
według sesji z płatnością 61%
7 zł
gorzej
zostaje w ciągu 180 dni na pacjencie nowych kampanii na L4 po koszcie pozyskania
pozostałe kampanie płatne: 30 zł
17%
gorzej
nowych pacjentów wraca w ciągu 90 dni
rok wcześniej 24%
88%
uwaga
przyrostu marży to zakupy pacjentów z pierwszego roku
pacjenci pozyskani w danym roku po kosztach kampanii: +3%
Marżato, co zostaje z zapłaty pacjenta po zwrotach i po wynagrodzeniu lekarza, razem z opłatą za TelemediGO. Marża po wszystkich kosztach odejmuje do tego wydatki na kampanie i prowizję afiliacyjną.
Koszt pozyskaniawydatki na kampanię podzielone przez liczbę nowych pacjentów, którzy z niej przyszli. „Zostaje na pacjencie” to jego marża w ciągu 180 dni od pierwszego zakupu minus koszt jego pozyskania.
KROK 1
Ile z liczb z dashboardu jest prawdą?

Liczba nowych pacjentów i sprzedaż TelemediGO się zgadzają, ale zamówień przybyło o 56%, a nie o 61%, a przychodu z konsultacji po zwrotach o 45%, a nie o 50%.

Co to znaczy dla biznesu: Zanim na dashboardzie zaczniemy podejmować decyzje, trzeba go oczyścić z podwójnych zamówień i kont testowych i liczyć przychód po zwrotach (pozycja 2 listy priorytetów).

Dashboard (dane surowe)
po kolejnych krokach oczyszczenia
poziom z dashboardu
Zamówienia
Dashboard (dane surowe)
+60,7%
Bez duplikatów zamówień
+58,3%
Bez duplikatów i bez kont testowych
+55,7%
Do tego przychód po odjęciu zwrotów
+55,7%
bez zmian
Przychód z konsultacji
Dashboard (dane surowe)
+50,3%
Bez duplikatów zamówień
+48,1%
Bez duplikatów i bez kont testowych
+47,7%
Do tego przychód po odjęciu zwrotów
+44,8%
0%
10%
20%
30%
40%
50%
60%
70%
Wzrost: ostatnie 12 miesięcy (X 2025 – IX 2026) wobec roku wcześniej (X 2024 – IX 2025). Każdy słupek to poziom po danym kroku, liczony od zera, a nie różnica między krokami.
Dashboard liczy dane na surowo: z 604 zdublowanymi zamówieniami z 10–24.06.2026, z 2 071 zamówieniami 22 kont testowych i z przychodem przed zwrotami.
Tabela z liczbami
Zmiana: ostatnie 12 miesięcy (X 2025 – IX 2026) wobec roku wcześniej (X 2024 – IX 2025). Pod zmianą: wartość rok wcześniej → wartość w ostatnich 12 miesiącach.
Krok	Nowi pacjenci	Zamówienia	Przychód z konsultacji	TelemediGO
Dashboard (dane surowe)	+51,9%
16 251 → 24 689	+60,7%
25 269 → 40 613	+50,3%
2,382 → 3,580 mln zł	+40,3%
1 759 → 2 468
Bez duplikatów zamówień	bez zmian	+58,3%
25 269 → 40 009	+48,1%
2,382 → 3,529 mln zł	bez zmian
Bez duplikatów i bez kont testowych	+52,1%
16 231 → 24 687	+55,7%
24 716 → 38 491	+47,7%
2,375 → 3,508 mln zł	bez zmian
Do tego przychód po odjęciu zwrotów	bez zmian	bez zmian	+44,8%
2,230 → 3,228 mln zł	bez zmian

Zastrzeżenie
Pierwszy rok startował od zera, bez bazy powracających pacjentów, więc sumy roczne z definicji faworyzują drugi rok (krok 5).

Zobacz w danych:
Jakość danych: od dashboardu do danych oczyszczonych
Priorytety: pozycja 2, codzienny raport
Szczegóły
Dashboard liczy dane na surowo. Zawiera 604 zdublowane zamówienia z 10–24.06.2026, 2 071 zamówień kont testowych i przychód przed zwrotami. Po oczyszczeniu zamówienia rosną o 55,7% (24 716 → 38 491) zamiast 61%, a przychód z konsultacji po zwrotach o 44,8% zamiast 50%. Nowi pacjenci prawie się nie zmieniają (+51,9% na surowo, +52,1% po oczyszczeniu), a TelemediGO wcale (+40,3%).
Start od zera. Rok wcześniej nie było bazy pacjentów z poprzedniego roku. W ostatnich 12 miesiącach pacjenci pozyskani rok wcześniej złożyli 5 289 zamówień powtórnych, które dały 153 tys. zł marży konsultacji. Sumy roczne z definicji faworyzują więc drugi rok.
Wynik biznesu rośnie wolniej niż sprzedaż. Marża po koszcie lekarza, kampaniach i prowizji wynosi 828 tys. zł rok wcześniej i 1 048 tys. zł w ostatnich 12 miesiącach, czyli +26,6%. Po odjęciu marży powtórnych konsultacji pacjentów pozyskanych rok wcześniej to +8,1%, a po odjęciu także ich opłat za TelemediGO (41,5 tys. zł) +3,1%. To rozbicie księgowe, które nie modeluje zmian wydatków ani zachowania pacjentów. Wydatki na kampanie rosną o 77% (z 368 do 650 tys. zł).

Skąd liczby: analiza/a3_dashboard.py, analiza/a2_czyste.py, analiza/wyniki/c_priorytety.txt (W3).

KROK 2
Skąd są nowi pacjenci?

Z 8 456 nowych pacjentów więcej niż rok wcześniej 7 268, czyli 86% przyrostu, to pacjenci dwóch nowych kampanii na L4: Meta od listopada 2025 i TikTok od lutego 2026.

Co to znaczy dla biznesu: Wzrost liczby pacjentów zależy od dwóch kampanii, a nie od szerszego popytu: bez nich nowych pacjentów przybyło tylko o 7%.

pozostałe kampanie i kanały
nowe kampanie na L4
rok wcześniej
16 231
16 231
ostatnie 12 miesięcy
17 419
7 268
24 687
Nowi pacjenci według pierwszego wejścia; długość słupka to liczba pacjentów.
Meta na L4 dała 5 059 nowych pacjentów, a TikTok na L4 2 209.
Pozostałe kampanie płatne dały o 332 nowych pacjentów więcej niż rok wcześniej, kanały bezpłatne (wejścia bezpośrednie, bezpłatna wyszukiwarka, program poleceń) o 855 więcej, a ranking lekarzy prawie tyle samo (617 wobec 616).
Według sesji z płatnością nowe kampanie dały 5 187 pacjentów, czyli 61% przyrostu, a bez nich pacjentów przybyło o 20%.
Zobacz w danych:
Kohorty: nowi pacjenci według źródła pozyskania
Szczegóły
Dokładnie: +52,1% wszystkich nowych pacjentów, +7,3% bez nowych kampanii, +12,1% z kanałów bezpłatnych (z 7 069 do 7 924). Pacjenci nowych kampanii: 7 268 z 24 687 (29%), marża w 90 dniach 36,3 zł wobec 66,0 zł.
Pozostałe kampanie płatne: 8 546 i 8 878 nowych pacjentów (+3,9%); ranking lekarzy 616 i 617.
Źródło pacjenta liczymy według pierwszego wejścia: pacjent nowej kampanii to ten, który pierwszy raz wszedł z jej reklamy albo zapłacił z jej kodem rabatowym. Według sesji z płatnością pacjentów bez nowych kampanii jest 19 500, czyli +20,1%. Różnica to 2 081 pacjentów, którzy według pierwszego wejścia należą do nowych kampanii, a według sesji z płatnością do innych kanałów: 1 918 weszło pierwszy raz z reklamy nowej kampanii, a zapłaciło w innej sesji (najczęściej po wejściu bezpośrednim albo z wyszukiwarki), a 163 weszło z innego kanału, ale zapłaciło z kodem nowej kampanii. Wracają tak rzadko jak pozostali pacjenci nowych kampanii. Bez nich obie reguły przypisania dają ten sam przyrost pacjentów, ten sam powrót i tę samą marżę, więc pacjentów i retencję opisujemy według pierwszego wejścia. W ekonomii kampanii pokazujemy obie reguły.

Skąd liczby: analiza/g_werdykt.py → analiza/wyniki/g_werdykt.txt (G1), analiza/wyniki/c_priorytety.txt (W1), analiza/wyniki/e_merytoryka.txt (punkt 1).

KROK 3
Czy wracają?

Rzadziej niż rok wcześniej: w ciągu 90 dni wraca 17% nowych pacjentów wobec 24%, a pacjenci nowych kampanii na L4 tylko w 4%.

Co to znaczy dla biznesu: Nowy pacjent zostawia dziś mniej w kolejnych miesiącach: jego marża w 90 dniach, przed kosztem pozyskania, spadła z 67 do 58 zł.

rok wcześniej
ostatnie 12 miesięcy
w ciągu 30 dni
11,0% → 7,8%
−3,2 pkt proc.
gorzej
w ciągu 60 dni
19,1% → 13,7%
−5,4 pkt proc.
gorzej
w ciągu 90 dni
23,9% → 17,4%
−6,5 pkt proc.
gorzej
w ciągu 180 dni
27,5% → 22,2%
−5,2 pkt proc.
gorzej
0%
10%
20%
30%
Tabela z liczbami
Powrót w ciągu	Rok wcześniej	Ostatnie 12 miesięcy	Zmiana
30 dni	11,0% (14 984 pacjentów)	7,8% (22 646 pacjentów)	
−3,2 pkt proc.
gorzej

60 dni	19,1% (13 941 pacjentów)	13,7% (20 823 pacjentów)	
−5,4 pkt proc.
gorzej

90 dni	23,9% (12 867 pacjentów)	17,4% (18 924 pacjentów)	
−6,5 pkt proc.
gorzej

180 dni	27,5% (9 125 pacjentów)	22,2% (12 591 pacjentów)	
−5,2 pkt proc.
gorzej
Bez pacjentów nowych kampanii powrót też spada: 22% wobec 24%.
Pacjenci nowych kampanii wracają w 4%. Ich większy udział odpowiada za około 71% spadku, a reszta to spadek w kanałach działających w obu latach.
Poza nowymi kampaniami marża na pacjenta w 90 dniach prawie stoi: 66 zł wobec 67 zł.

Zastrzeżenie
Te liczby opisują zmianę, ale nie wskazują jej przyczyny. Nie wiemy, dlaczego spada powrót w kanałach działających w obu latach: czy ci sami pacjenci zachowują się dziś gorzej, czy zmieniło się to, kto do nas trafia.

Zobacz w danych:
Zdarzenia: co zmieniło się po każdym zdarzeniu i każdej decyzji
Kohorty: powrót w 90 dniach, nowe kampanie na L4 i pozostałe
Kohorty: powrót bez pacjentów nowych kampanii
Szczegóły
Powrót to kolejne zamówienie, które nie zostało anulowane. Liczymy go na tych samych dniach kalendarzowych (pierwsze zakupy do 2 lipca w obu latach przy oknie 90 dni) i tylko w kohortach z pełnym oknem obserwacji. Liczba pacjentów: 12 867 rok wcześniej i 18 924 w ostatnich 12 miesiącach; bez nowych kampanii 14 031 (powrót 22,0% wobec 23,9%), pacjenci nowych kampanii 4 893 (powrót 4,1%). Marża na pacjenta w 90 dniach: 58,3 zł wobec 66,6 zł, bez nowych kampanii 66,0 zł.
Kolejne zamówienia na pacjenta w 90 dniach: 0,234 wobec 0,334, czyli o 29,8% mniej; bez pacjentów nowych kampanii 0,300.
Według sesji z płatnością bez nowych kampanii powrót wynosi 20,4%, a marża 63,3 zł. Cała różnica to 1 383 pacjentów nowych kampanii (z pełnym oknem 90 dni), których ta reguła przypisuje innym kanałom: 1 279 weszło z reklamy nowej kampanii, a zapłaciło w innej sesji, a 104 zapłaciło z kodem nowej kampanii po wejściu z innego kanału. Wracają w 4,3%. Bez nich obie reguły dają 22,0% i 66,0 zł, a udział nowych kampanii w spadku powrotu wynosi w obu 71% (według sesji z płatnością bez tej poprawki 46%).
„Około 71% spadku” to podział opisowy, czyli bez mierzenia wpływu: udział pacjentów nowych kampanii (25,9% kohort) razy różnica powrotu między nimi a resztą (4,6 z 6,5 punktu procentowego). Nie mówi, co by się stało bez tych kampanii.
Według pierwszej usługi, bez pacjentów nowych kampanii (95% przedział różnicy): spada po e-recepcie z 33,4% (3 206 pacjentów) do 29,9% (3 570), a po wizycie u innego specjalisty z 25,2% (2 325 pacjentów) do 20,6% (2 549). Bez istotnej zmiany: pediatra z 22,3% (673 pacjentów) do 26,3% (711), od −0,5 do +8,5 punktu, psychiatra z 22,5% (550 pacjentów) do 24,6% (605), od −2,8 do +7,0 punktu, pierwsze L4 u internisty z 14,6% (2 795 pacjentów) do 13,8% (2 969), od −2,6 do +1,0 punktu. Według sesji z płatnością L4 spada do 11,0%, ale to ta sama grupa: do 2 969 pacjentów według pierwszego wejścia dochodzi 1 145 pacjentów nowych kampanii z pierwszym L4.
Liczba osób, które wróciły w 90 dniach, rośnie: 3 289 wobec 3 076 (+6,9%). Spada tylko ich odsetek.
W 180 dniach liczymy tylko kohorty z pełnym oknem (9 125 i 12 591 pacjentów), więc to wcześniejsze, mniejsze grupy niż w 90 dniach.
Część spadku w kanałach działających w obu latach może wiązać się z porannymi opóźnieniami u internistów: po spóźnionej pierwszej wizycie pacjenci wracają rzadziej. Dane tego nie rozstrzygają (Czego nie wiemy, punkt 4).

Skąd liczby: analiza/wyniki/c_priorytety.txt (W2), analiza/wyniki/a5r_kohorty.txt (180 dni), analiza/wyniki/d_retencja.txt (usługi, kolejne zamówienia), analiza/wyniki/e_merytoryka.txt (punkt 1).

KROK 4
Ile zarabiamy na nowym pacjencie po koszcie pozyskania?

Na pacjencie nowych kampanii na L4 zostaje w ciągu 180 dni 7 zł, a na pacjencie pozostałych kampanii płatnych 30 zł (rok wcześniej 32 zł).

Co to znaczy dla biznesu: Nowe kampanie kupują liczbę pacjentów, ale prawie nie kupują zysku, a od wiosny koszt pozyskania zjada całą marżę ich pacjenta.

według pierwszego wejścia
według sesji z płatnością
XI 2025
+7,0 zł
+0,4 zł
XII 2025
+9,6 zł
−8,7 zł
I 2026
+10,3 zł
−0,3 zł
II 2026
+10,1 zł
−1,4 zł
III 2026
+3,8 zł
−7,9 zł
IV 2026 *
−1,0 zł
−15,9 zł
V 2026 *
+3,0 zł
−11,6 zł
VI 2026 *
−0,3 zł
−12,9 zł
VII 2026 *
−0,3 zł
−14,5 zł
VIII 2026 *
+0,1 zł
−14,0 zł
IX 2026 *
+1,3 zł
−15,5 zł
−20 zł
−15 zł
−10 zł
−5 zł
0 zł
+5 zł
+10 zł
+15 zł
Zostaje na pacjencie: marża w 180 dniach minus koszt pozyskania. Pionowa linia to zero: na lewo od niej pozyskanie kosztuje więcej, niż pacjent zostawia. Gwiazdka: marża w 180 dniach przybliżona.
Pacjent nowych kampanii zostawia w 180 dniach 37 zł marży, a jego pozyskanie kosztuje 30 zł. Pacjent pozostałych kampanii płatnych zostawia 72 zł marży przy koszcie pozyskania 43 zł.
Miesiąc po miesiącu koszt pozyskania pacjenta nowych kampanii rośnie z 27–30 zł (listopad 2025 – luty 2026) do 33–37 zł (kwiecień – wrzesień 2026), a marża pacjenta zostaje na poziomie 34–40 zł. Od kwietnia zostaje od −1 do +3 zł na pacjencie.
Osobno: TikTok na L4 traci od marca 2026 (w II kwartale 6 zł na pacjencie), a Meta na L4 zostaje na plusie (w III kwartale 2 zł na pacjencie).
Według sesji z płatnością obie kampanie razem tracą od grudnia 2025, a od kwietnia 12–16 zł na każdym pacjencie.

Zastrzeżenie
Pacjenci z pierwszym zakupem od kwietnia 2026 nie mają jeszcze pełnych 180 dni. Ich marżę przybliżamy: do marży z krótszego okresu dodajemy to, co starsi pacjenci tych kampanii zostawili później, czyli od 0,35 do 2,87 zł na pacjenta, bo ci pacjenci prawie nie wracają.

Zobacz w danych:
Wynik biznesu: ekonomia kampanii, obie reguły
Priorytety: pozycja 3, TikTok na L4
Priorytety: pozycja 9, test kampanii Meta na L4
Szczegóły
Nowe kampanie na L4 według miesiąca pierwszego zakupu, według pierwszego wejścia (ostatnia kolumna: według sesji z płatnością). Pełne 180 dni mają pierwsze zakupy do 3.04.2026; dla późniejszych marża w 180 dniach jest przybliżona.
Miesiąc pierwszego zakupu	Nowi pacjenci	Koszt pozyskania	Marża w 180 dniach	Zostaje na pacjencie	Zostaje na pacjencie według sesji z płatnością
XI 2025	121	27,3 zł	34,3 zł	
+7,0 zł
lepiej
	
+0,4 zł
lepiej

XII 2025	279	27,7 zł	37,4 zł	
+9,6 zł
lepiej
	
−8,7 zł
gorzej

I 2026	445	30,1 zł	40,4 zł	
+10,3 zł
lepiej
	
−0,3 zł
gorzej

II 2026	610	29,6 zł	39,7 zł	
+10,1 zł
lepiej
	
−1,4 zł
gorzej

III 2026	826	31,7 zł	35,5 zł	
+3,8 zł
lepiej
	
−7,9 zł
gorzej

IV 2026	825	36,0 zł	35,0 zł	
−1,0 zł
gorzej
	
−15,9 zł
gorzej

V 2026	910	33,1 zł	36,1 zł	
+3,0 zł
lepiej
	
−11,6 zł
gorzej

VI 2026	818	35,9 zł	35,6 zł	
−0,3 zł
gorzej
	
−12,9 zł
gorzej

VII 2026	799	37,3 zł	37,0 zł	
−0,3 zł
gorzej
	
−14,5 zł
gorzej

VIII 2026	785	36,4 zł	36,5 zł	
+0,1 zł
lepiej
	
−14,0 zł
gorzej

IX 2026	850	34,8 zł	36,1 zł	
+1,3 zł
lepiej
	
−15,5 zł
gorzej
Porównanie płatnych z płatnymi liczymy na pierwszych zakupach od 1.10 do 3.04 w obu latach, bo tylko one mają pełne 180 dni: 2 352 pacjentów nowych kampanii (przedział 95% od 5,4 do 8,6 zł), 5 130 pacjentów pozostałych kampanii płatnych (29,7 zł) i rok wcześniej 4 717 (31,8 zł).
Według sesji z płatnością pacjent nowych kampanii daje −5,2 zł, a pacjent pozostałych kampanii płatnych 27,5 zł (rok wcześniej 30,0 zł).
Na całym roczniku, z przybliżoną marżą w 180 dniach dla młodszych pacjentów: nowe kampanie 2,8 zł na pacjencie (7 268 pacjentów), pozostałe kampanie płatne 26,7 zł wobec 30,8 zł rok wcześniej.
Ranking lekarzy (prowizja 25 zł za pacjenta) zostawia 37,0 zł wobec 34,8 zł rok wcześniej; liczymy go osobno, bo płacimy za pacjenta, a nie za kliknięcie.
W kwartałach (według pierwszego wejścia): 8,9 zł, 7,4 zł, 0,7 zł, 0,4 zł na pacjencie w IV kwartale 2025 i w I, II i III kwartale 2026; według sesji z płatnością −5,5 zł, −4,0 zł, −13,4 zł, −14,7 zł.
Kwota na pacjencie to średnia ze wszystkich pacjentów przypisanych kampanii. Nie mówi, ile dałaby kolejna złotówka budżetu.

Skąd liczby: analiza/g_werdykt.py → analiza/wyniki/g_werdykt.txt (G2, G3), analiza/wyniki/a5e_ekonomia.txt (1b).

KROK 5
Skąd w takim razie +27% marży?

Z pacjentów pozyskanych w pierwszym roku: ich zakupy w ostatnich 12 miesiącach dały 194 tys. zł, czyli 88% przyrostu marży o 220 tys. zł.

Co to znaczy dla biznesu: Sam przyrost liczby pacjentów prawie nie podniósł zysku: na jednym nowym pacjencie zostaje w roku pozyskania, po kosztach kampanii, 35 zł wobec 51 zł rok wcześniej.

pacjenci pozyskani w tym samym roku, po kosztach kampanii
pacjenci z pierwszego roku
rok wcześniej
828 tys. zł
828 tys. zł
ostatnie 12 miesięcy
854 tys. zł
194 tys. zł
1 048 tys. zł
Marża po wszystkich kosztach w tysiącach złotych; długość słupka to kwota.
Rok wcześniej cała marża, 828 tys. zł, pochodziła od pacjentów pozyskanych w tym samym roku. Wcześniejszych pacjentów w danych nie ma, bo dane zaczynają się 1.10.2024.
W ostatnich 12 miesiącach pacjenci z pierwszego roku dali 194 tys. zł: 153 tys. zł z kolejnych wizyt i 41 tys. zł z opłat za TelemediGO.
Pacjenci pozyskani w ostatnich 12 miesiącach zostawili w tym samym roku 1 519 tys. zł marży przed kosztem kampanii, o 25% więcej niż rok wcześniej. Wydatki na kampanie wzrosły jednak o 77%, z 368 do 650 tys. zł, więc po ich odjęciu zostaje 854 tys. zł wobec 828 tys. zł.

Zastrzeżenie
To rozbicie księgowe: przypisuje marżę i koszty grupom pacjentów, ale nie mierzy, co by się stało bez nowych kampanii.

Zobacz w danych:
Wynik biznesu: marża po kwartałach
Szczegóły
Dokładnie: marża po wszystkich kosztach 828 085 zł rok wcześniej i 1 048 069 zł w ostatnich 12 miesiącach, czyli +219 984 zł (+26,6%). Pacjenci z pierwszego roku: 194 434 zł (88,4% przyrostu). Pacjenci pozyskani w danym roku, po kosztach kampanii i prowizji: 828 085 zł i 853 635 zł, czyli +25 550 zł (+3,1%; 11,6% przyrostu). Na nowego pacjenta: 51,02 zł (16 231 pacjentów) i 34,58 zł (24 687).
Pacjenci nowych kampanii na L4 zostawili w roku pozyskania 263 tys. zł marży przy 246 tys. zł wydatków, czyli 17 tys. zł (2,38 zł na pacjenta). Pozostali pacjenci pozyskani w ostatnich 12 miesiącach dali po kosztach kampanii i prowizji 836 tys. zł wobec 828 tys. zł rok wcześniej (+1,0%), a na pacjenta 48,01 zł wobec 51,02 zł.
Według sesji z płatnością nowe kampanie tracą w roku pozyskania 58 tys. zł (−11,23 zł na pacjenta), a pozostali pacjenci dają o 10,2% więcej niż rok wcześniej.
Marża przed kosztem kampanii pacjentów pozyskanych w danym roku: 1 211 tys. zł i 1 519 tys. zł; wydatki na kampanie 367 632 zł i 649 675 zł; prowizja 15 400 zł i 15 425 zł.

Skąd liczby: analiza/g_werdykt.py → analiza/wyniki/g_werdykt.txt (G4), analiza/wyniki/c_priorytety.txt (W3).

KROK 6
W którą stronę to idzie z kwartału na kwartał?

Z każdym kwartałem wydatki na kampanie rosną rok do roku szybciej, a marża przed ich kosztem wolniej: w III kwartale 2026 wydatki były ponad dwa razy wyższe niż rok wcześniej, a marża przed ich kosztem wyższa o 25%.

Co to znaczy dla biznesu: Marża po kosztach kampanii już nie rośnie: w III kwartale 2026 była na poziomie roku wcześniej, od 7% niższa do 1% wyższa, zależnie od jednorazowego startu sprzedaży TelemediGO w newsletterze rok wcześniej.

marża przed kosztem kampanii
wydatki na kampanie
IV kw. 2025
+55,2%
+29,6%
I kw. 2026
+49,7%
+66,4%
II kw. 2026
+38,4%
+104,0%
III kw. 2026
+25,2%
+107,7%
0%
+20%
+40%
+60%
+80%
+100%
+120%
Zmiana wobec tego samego kwartału rok wcześniej. Marża przed kosztem kampanii to przychód z konsultacji po zwrotach i z TelemediGO minus koszt lekarza; wydatki na kampanie bez prowizji afiliacyjnej.
Tabela z liczbami
Zmiana wobec tego samego kwartału rok wcześniej; pod nią wartość w kwartale
Kwartał	Marża przed kosztem kampanii	Wydatki na kampanie	Marża po kosztach kampanii
IV 2025	
+55,2%
lepiej
376,0 tys. zł
	
+29,6%
uwaga
113,1 tys. zł
	
+71,4%
lepiej
259,4 tys. zł

I 2026	
+49,7%
lepiej
500,2 tys. zł
	
+66,4%
uwaga
170,6 tys. zł
	
+43,0%
lepiej
324,4 tys. zł

II 2026	
+38,4%
lepiej
444,5 tys. zł
	
+104,0%
uwaga
184,4 tys. zł
	
+13,0%
lepiej
256,6 tys. zł

III 2026	
+25,2%
lepiej
392,5 tys. zł
	
+107,7%
uwaga
181,6 tys. zł
	
−6,8%
gorzej
207,7 tys. zł
Na pacjencie nowych kampanii na L4 zostawało po koszcie pozyskania 9 zł w IV kwartale 2025 i 7 zł w I kwartale 2026, a w II i III kwartale 2026 mniej niż 1 zł.
Bez zakupów pacjentów pozyskanych w poprzednich kwartałach marża po kosztach kampanii rosła rok do roku o 8,5% w IV kwartale 2025 i o 26,1% w I kwartale 2026, a w II i III kwartale 2026 spadła o 6,7% i 5,6%.
Marża przed kosztem kampanii wzrosła za cały rok o 41%, a wydatki na kampanie o 77%.

Zastrzeżenie
Marża po koszcie lekarza, kampaniach i prowizji spadła w III kwartale 2026 o 7% rok do roku, ale ten spadek zależy od jednorazowego zdarzenia: rok wcześniej we wrześniu ruszyła sprzedaż TelemediGO w newsletterze. Po odjęciu jednorazowej nadwyżki tego startu marża kwartału jest o 1% wyższa niż rok wcześniej.

Zobacz w danych:
Wynik biznesu: marża po kwartałach
Priorytety: pozycja 1, Safari
Szczegóły
Za cały rok marża po koszcie lekarza, kampaniach i prowizji wzrosła z 828 do 1 048 tys. zł, czyli o 26,6%. Marża przed kosztem kampanii wzrosła o 41,5%, a wydatki na kampanie o 76,7%.
W III kwartale 2026 marża była o 6,8% niższa niż rok wcześniej. W pierwszych 23 dniach sprzedaży TelemediGO w newsletterze pacjenci kupili 225 członkostw; po odjęciu szacowanej nadwyżki tego startu marża kwartału jest o 1,1% wyższa niż rok wcześniej.
Warianty III kwartału: bez nadwyżki startu sprzedaży w newsletterze (196 z 225 zakupów ponad zwykłe tempo 29 na 23 dni, 17,4 tys. zł) +1,1%; bez całej sprzedaży w newsletterze w obu latach −2,3%; bez wszystkich opłat za TelemediGO −4,9%. Marża przed kosztem kampanii bez nadwyżki startu rośnie o 32,6%.
Awaria zakładania konta w Safari na iPhone'ach kosztowała w samym III kwartale 2026 szacunkowo 14,6–18,3 tys. zł marży. Wyniku kwartału bez awarii nie mierzymy; to scenariusz z pozycji 1 listy priorytetów.
W samych miesiącach: lipiec 2026 73,4 tys. zł wobec 66,8 tys. zł, sierpień 66,3 wobec 67,2 tys. zł, wrzesień 68,0 wobec 88,8 tys. zł. Cały spadek kwartału przypada na wrzesień.
Baza powracających pacjentów (marża z pacjentów pozyskanych w poprzednich kwartałach): w III kwartale 2026 106,2 tys. zł wobec 115,2 tys. zł rok wcześniej. Rok wcześniej zawierała jednorazowy start sprzedaży w newsletterze; po odjęciu części nadwyżki przypadającej na bazę (210 z 225 zakupów) to 99,0 tys. zł, więc w 2026 baza dała o 7,3% więcej (bez całej sprzedaży w newsletterze w obu latach o 1,0% więcej). Wszystkich pacjentów pozyskanych w poprzednich kwartałach jest prawie trzy razy więcej (35 032 wobec 12 794), ale tych, którzy w kwartale coś kupili, tylko o 15% więcej (1 735 wobec 1 503). Baza jest starsza, a nowsze roczniki wracają rzadziej; tych dwóch rzeczy dane nie rozdzielają.
Pierwsze kwartały nie miały jeszcze bazy powracających. Marża z pacjentów pozyskanych w poprzednich kwartałach to 0% marży IV kwartału 2024, 23,4% I kwartału 2025 i 51,7% III kwartału 2025. Bez tej bazy marża rośnie rok do roku o 8,5% zamiast 71,4% w IV kwartale 2025 i o 26,1% zamiast 43,0% w I kwartale 2026. Wzrost tych kwartałów jest więc zawyżony startem od zera.
Rozkład spadku III kwartału na pacjentów nowych kampanii i resztę biznesu to rozkład księgowy, czyli przypisanie składników marży grupom pacjentów bez mierzenia wpływu. Marża spadła o 15,1 tys. zł. Według pierwszego wejścia pacjenci nowych kampanii zostawili 89,0 tys. zł marży przed kampaniami przy 87,9 tys. zł wydatków, czyli wyszli prawie na zero (+1,1 tys. zł). Reszta biznesu straciła 16,2 tys. zł: opłaty TelemediGO −11,2 tys. zł, w tym −10,5 tys. zł sprzedaży osobnej w newsletterze (225 zakupów we wrześniu 2025 wobec 107 w całym III kwartale 2026), wyższe wydatki kampanii działających w obu latach −6,2 tys. zł, marża konsultacji +1,2 tys. zł: powtórnych zamówień jest więcej (3 140 wobec 2 879), ale każde zostawia mniej marży, głównie przez większy udział wizyt ze zniżką TelemediGO (32,81 zł wobec 35,86 zł), prowizja bez zmian. Po odjęciu TelemediGO reszta biznesu traci 5,0 tys. zł; księgowo to wyższe wydatki kampanii działających w obu latach, częściowo zrównoważone wyższą marżą konsultacji. Według sesji z płatnością podział między nowe kampanie (−25,2 tys. zł) a resztę (+10,1 tys. zł) się odwraca; suma jest ta sama.

Skąd liczby: analiza/wyniki/c_priorytety.txt (W3, W4), analiza/wyniki/d_wynik.txt (punkty 1 i 2), analiza/wyniki/e_merytoryka.txt (punkt 2), analiza/wyniki/g_werdykt.txt (G3).

KROK 7
Co robimy?

Najpierw naprawiamy to, co psuje wynik niezależnie od kampanii, potem wstrzymujemy kampanie, które tracą na każdym pacjencie, a o kampanii Meta na L4 rozstrzyga test w części kraju.

Co to znaczy dla biznesu: Każda pozycja listy priorytetów ma wartość w marży, sposób pomiaru i czas wdrożenia; niżej decyzje na pierwszy tydzień.

Decyzje na pierwszy tydzień
1
Naprawić zakładanie konta w Safari na iPhone'ach
pozycja 1 · do 83 tys. zł marży rocznie
2
Oczyścić codzienny raport i dodać alarmy na lejku
pozycja 2 · awaria Safari trwała 198 dni, do końca danych
3
Wstrzymać kampanię TikTok na L4 i kampanię Google Ads na specjalistów
pozycje 3 i 4 · obie tracą na każdym pacjencie według obu reguł przypisania źródła (pierwsze wejście i sesja z płatnością), a pauzę da się cofnąć w jeden dzień
4
Zrobić krótkie sprawdzenia: obietnica reklam L4, poranne grafiki internistów, zakup po zalogowaniu, kliknięcia w panelach reklam
pierwsze kroki pozycji 5, 6, 8 i 11 · każde zajmuje dzień albo dwa
Zobacz w danych:
Priorytety: cała lista
Priorytety: pozycja 9, test kampanii Meta na L4
KROK 8
Czego nie wiemy?

Trzech rzeczy, od których zależą decyzje: ilu pacjentów nowych kampanii przyszłoby i bez reklamy, dlaczego rzadziej wracają pacjenci z kanałów działających w obu latach i ile wizyt dokłada zniżka TelemediGO.

Co to znaczy dla biznesu: Dlatego decyzje, które od nich zależą, są na liście priorytetów testami z regułą ustaloną z góry, a nie pewnymi kwotami.

Ilu pacjentów nowych kampanii przyszłoby i bez reklamy: test z pozycji 9, czyli wyłączenie kampanii Meta na L4 na 4–6 tygodni w losowej połowie województw. Da wynik orientacyjny, więc decyzję podejmujemy według reguły ustalonej z góry (Czego nie wiemy, punkt 1).
Dlaczego rzadziej wracają pacjenci z kanałów działających w obu latach: jedną z możliwych przyczyn są poranne opóźnienia u internistów, ale dane tego nie rozstrzygają (Czego nie wiemy, punkt 4).
Ile wizyt i powrotów dokłada zniżka TelemediGO: losowy, bezpłatny dostęp do zniżek (pozycja 12; Czego nie wiemy, punkt 8).
Zobacz w danych:
Czego nie wiemy: punkt 1
Czego nie wiemy: punkt 4
Czego nie wiemy: punkt 8
Czego nie wiemy: cała lista
TelemediGO rośnie razem z liczbą zamówień, a nie dzięki większej chęci zakupu

Sprzedaż wzrosła o 40%, bo jest więcej zamówień i przez cały rok działała sprzedaż w newsletterze, a odsetek kupujących przy kasie nie rośnie.

rok wcześniej
ostatnie 12 miesięcy
Przy kasie z pierwszym zamówieniem
905
1 089
+184
Przy kasie z kolejnym zamówieniem
629
918
+289
Osobno, z newslettera
225
461
+236
Liczba zakupów TelemediGO.
Tabela z liczbami
Typ zakupu	Rok wcześniej	Ostatnie 12 miesięcy	Zmiana	Udział we wzroście
Przy kasie z pierwszym zamówieniem pacjenta	905	1 089	+184	26%
Przy kasie z kolejnym zamówieniem	629	918	+289	41%
Osobno, z newslettera	225	461	+236	33%
Razem	1 759	2 468	+709	100%
Opłata 89 zł nie pokrywa zniżek: członkostwa sprzed roku dostały średnio o około 16 zł więcej zniżek, niż przyniosły opłat.
Widać to w marży: powtórne zamówienie pacjenta spoza nowych kampanii zostawiło w III kwartale 2026 około 33 zł marży wobec 36 zł rok wcześniej. Prawie cały ten spadek to rosnący udział wizyt ze zniżką TelemediGO: z 34% do 42% powtórnych zamówień.

Zastrzeżenie
Nie wiemy, ile wizyt członkostwo dokłada. Test z pozycji 12 pokaże wpływ samej zniżki, ale nie opłacalność oferty za 89 zł.

Zobacz w danych:
Priorytety: pozycja 12, test TelemediGO
Priorytety: pozycja 10, warunki TelemediGO u specjalistów
Kohorty: kupujący TelemediGO przy pierwszym zakupie
Lejek: zakupy samego TelemediGO
Szczegóły
Sprzedaż osobna w newsletterze ruszyła 8.09.2025. Rok wcześniej działała więc tylko 23 dni, a pacjenci kupili w tym czasie 225 członkostw. W ostatnich 12 miesiącach kupują w niej średnio 38 członkostw miesięcznie.
Przy kasie przybywa zakupów, bo jest więcej zamówień, a nie wyższy odsetek kupujących. Przy pierwszym zamówieniu odsetek kupujących spada z 5,58% (16 231 zamówień) do 4,41% (24 687): więcej zamówień dodaje 471 zakupów, a niższy odsetek odejmuje 287. Przy kolejnych zamówieniach odsetek rośnie lekko, z 9,27% (6 784) do 9,86% (9 307).
Spadek odsetka przy pierwszym zamówieniu to w całości pacjenci nowych kampanii na L4: kupuje u nich 1,5% (7 268 pacjentów). Bez nich odsetek stoi: 5,58% wobec 5,63% (17 419 pacjentów).
Opłata 89 zł nie pokrywa średniej zniżki. Członkostwa sprzed roku (1 759, pełne 365 dni) przyniosły 156 551 zł opłat i dostały 183 939 zł zniżki efektywnej, czyli −27 388 zł (−15,57 zł na członkostwo). W ostatnich 12 miesiącach przybliżenie to −10,7 zł na członkostwo. To rachunek przy założeniu, że te same wizyty zostałyby kupione bez TelemediGO, a nie strata programu: nie wiemy, ile wizyt członkostwo dokłada.
Kupujący TelemediGO przy pierwszym zamówieniu wracają w 90 dniach częściej niż podobni pacjenci: 34,7% wobec 20,0% w ostatnich 12 miesiącach (858 kupujących). Dane nie mówią, ile z tego to wpływ zniżki, a ile to, że kupują ci, którzy i tak planują wracać. Test z pozycji 12 (losowy, bezpłatny dostęp do zniżek) pokaże wpływ samej zniżki.
Powtórne zamówienie pacjenta spoza nowych kampanii zostawiło w III kwartale 2026 32,81 zł marży wobec 35,86 zł rok wcześniej. Wizyta ze zniżką TelemediGO zostawia średnio 11,01 zł marży, bez zniżki 48,78 zł, a wizyta u specjalisty ze zniżką traci 5,59 zł. Udział wizyt ze zniżką wśród powtórnych zamówień: 34,3% (2 879 zamówień) i 41,6% (3 140). Zmiana tego udziału daje 2,71 zł z 3,05 zł spadku marży na zamówienie (rozkład na strukturę i marżę w obrębie rodzaju zniżki).

Skąd liczby: analiza/c_telemedigo.py → analiza/wyniki/c_telemedigo.txt (1a, 1b, 1e, 1f, 2a, 2b, 4a). Notatka: notatki/c_szkic.md, sekcja 2. Marża powtórnych zamówień: analiza/wyniki/e_merytoryka.txt (punkt 3).

Skąd liczby: analiza/c_priorytety.py → analiza/wyniki/c_priorytety.txt (W1–W4, P1), analiza/wyniki/a5r_kohorty.txt (180 dni), analiza/wyniki/a5r_struktura.txt (L4 z L4, rozkład spadku), analiza/wyniki/a5e_ekonomia.txt, analiza/wyniki/c_telemedigo.txt. Notatka: notatki/c_szkic.md, sekcja 1. Werdykt, ekonomia pacjenta i przyrost marży: analiza/g_werdykt.py → analiza/wyniki/g_werdykt.txt. Sprawdzenia przed publikacją: analiza/wyniki/e_merytoryka.txt i analiza/wyniki/e_poprawki.txt. Teksty strony: notatki/e_teksty.md.

Dalej: Kohorty
```
