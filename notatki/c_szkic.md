# C — szkic na poranny przegląd Kuby (sesja prowadząca, 2026-10-20)

**Status:** przyjęte przez Kubę 2026-10-20: szkic z czterema dopiskami, runda konsylium, ostateczna lista 12 priorytetów i 18 niewiadomych, pięć poprawek spójności (`DECYZJE.md`, sekcja 9 niżej). Propozycje z sekcji 7 są scalone we wspólnych notatkach. Na stronę narzędzia przenosi to osobna sesja. Zakres: `DECYZJE.md`, wpis z 2026-10-20 o nowej sesji prowadzącej.

**2026-10-21:** poprawki po konsylium końcowej weryfikacji według listy Kuby (`notatki/d_poprawki.md`): karta streszczenia na górze sekcji 1, rozkład spadku marży III kwartału, nowe brzmienia zdań mocniejszych niż dane, test Mety z regułą na wynik niejednoznaczny, kod rabatowy Mety, cztery nowe niewiadome (19–22, razem 22). Nowe liczby: `analiza/d_retencja.py`, `analiza/d_kampanie.py`, `analiza/d_wynik.py` (raporty `analiza/wyniki/d_*.txt`).

**Pliki:**

| Plik | Co zawiera |
|---|---|
| `analiza/c_telemedigo.py` → `analiza/wyniki/c_telemedigo.txt` | TelemediGO: skąd wzrost sprzedaży, opłaty wobec zniżek, zniżki wobec kosztu lekarza, powroty z kontrolami samoselekcji i projektem testu. Zestawienia miesięczne dla narzędzia: `c_telemedigo_miesiace.csv` i `c_telemedigo_miesiace_znizki.csv`. |
| `analiza/c_priorytety.py` → `analiza/wyniki/c_priorytety.txt` | W1–W3: liczby do odpowiedzi „czy to wzrost” (nowi pacjenci, powroty, marża na pacjenta, wynik biznesu). P1–P10: wartość pozycji listy priorytetów. Liczby przepisane z wcześniejszych raportów skrypt sprawdza w tych raportach (funkcja `z_raportu`). |
| `notatki/recenzje/c_codex_*.md` | Recenzja Codeksa (model Sol): polecenie, odpowiedź, podsumowanie. |
| `notatki/konsylium/c_priorytety/brief.md` | Brief dla konsylium, bez naszej opinii. **Nie wysłany** — czeka na decyzję Kuby. |

Oba skrypty uruchamia się z głównego folderu przez `python -I`, każdy w kilka sekund. Tylko czytają bazę.

Okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026. „Przyjęta reguła” = źródło według pierwszego wejścia, kod kampanii rozstrzyga (`ZALOZENIA.md` 22). „Sesja płatności” = reguła porównawcza (punkt 23). „Nowe kampanie” = `meta_prosp_l4_szybko` (Meta, od 3.11.2025) i `tt_prosp_l4_15min` (TikTok, od 9.02.2026), obie na zwolnienie lekarskie (L4).

---

## 1. Propozycja odpowiedzi „czy to wzrost” (do akceptacji Kuby)

**Karta na górze zakładki, dla kogoś, kto otwiera stronę pierwszy raz (dopisek Kuby 2026-10-21):**
- **Odpowiedź:** nie, to nie jest wzrost w rozumieniu Telemedi. Pacjentów jest więcej, ale wracają rzadziej, a pod koniec okresu marża spada.
- **Trzy liczby:**
  - nowych pacjentów jest o 52,1% więcej: 24 687 w X 2025 – IX 2026 wobec 16 231 w X 2024 – IX 2025;
  - powrót w 90 dniach spadł z 23,9% do 17,4% (kohorty 1.10–2.07 w obu latach, na tych samych dniach kalendarzowych; 12 867 i 18 924 pacjentów);
  - w III kwartale 2026 marża była o 6,8% niższa niż rok wcześniej, przy wydatkach na kampanie 2,08 raza wyższych.
- **Trzy decyzje na pierwszy tydzień:**
  - naprawić zakładanie konta w Safari na iOS (pozycja 1);
  - wstrzymać TikToka na L4 i Google Ads na specjalistów jako pauzy, które da się cofnąć w jeden dzień (pozycje 3 i 4);
  - oczyścić codzienny raport i dodać alarmy na lejku (pozycja 2).
- **Jedna kwota:** górny scenariusz odzyskania marży po naprawie Safari na iOS to 75–83 tys. zł na pełny rok, w horyzoncie 90 dni od pozyskania, przed kosztem naprawy (pozycja 1).

**Propozycja w dwóch zdaniach:** w rozumieniu Telemedi to nie jest wzrost, bo z dwóch warunków spełniony jest tylko pierwszy: pacjentów z pierwszym zakupem jest o 52,1% więcej (24 687 wobec 16 231), ale retencja jest gorsza (powrót w 90 dniach 17,4% wobec 23,9% na tych samych dniach kalendarzowych, a marża na pacjenta w 90 dniach 58,3 zł wobec 66,6 zł). Obecność pacjentów dwóch nowych kampanii na L4 odpowiada opisowo za około 46–71% spadku powrotu, zależnie od reguły źródła, ale bez nich retencja też spada (do 22,0% według przyjętej reguły albo 20,4% według sesji płatności), a nowych pacjentów spoza tych kampanii przybyło tylko o 7,3–20,1%.

**Zdanie zamykające (dopisek Kuby, potwierdzone naszym kodem):** pod koniec okresu wzrost przestał się przekładać na wynik: w III kwartale 2026 marża była o 6,8% niższa niż rok wcześniej (207,7 tys. zł wobec 222,8 tys. zł), choć wydatki na kampanie były 2,08 raza wyższe (181,6 tys. zł wobec 87,4 tys. zł).

*Uzupełnienie po konsylium (poprawione 2026-10-21, dopisek Kuby):* szacowana marża utracona przez awarię zakładania konta w Safari na iOS w samym III kwartale 2026 to 14,6–18,3 tys. zł, zależnie od odjęcia tła i założonego tempa strat, a osobny scenariusz powrotów pacjentów utraconych od 17.03 do 30.06 daje 4,1–4,5 tys. zł. To kwota tego samego rzędu co cały spadek marży kwartału (15,1 tys. zł). Wyniku kwartału bez awarii nie mierzymy: to scenariusz przy założeniach pozycji 1 (`d_wynik.txt`, punkt 1f).

### 1a. Więcej pacjentów: tak

- Nowych pacjentów jest 24 687 w okresie 2 wobec 16 231 w okresie 1, czyli +52,1% (`c_priorytety.txt`, W1).
- Bez pacjentów dwóch nowych kampanii na L4 jest ich 17 419 według przyjętej reguły (+7,3%) albo 19 500 według sesji płatności (+20,1%).
- Z kanałów bezpłatnych (wejścia bezpośrednie, bezpłatne wyszukiwanie, program poleceń) przybyło 12,1%: z 7 069 do 7 924.
- Nie wiemy, ilu pacjentów nowych kampanii przyszłoby i bez nich (dodatkowość, sekcja 4, punkt 1).

### 1b. Lepsza retencja: nie

- Powrót, czyli kolejne nieanulowane zamówienie, liczony na tych samych dniach kalendarzowych (`c_priorytety.txt`, W2):
  - w 30 dniach 7,8% (22 646 pacjentów) wobec 11,0% (14 984);
  - w 60 dniach 13,7% (20 823) wobec 19,1% (13 941);
  - w 90 dniach 17,4% (18 924) wobec 23,9% (12 867);
  - w 180 dniach 22,2% (12 591) wobec 27,5% (9 125) (`a5r_kohorty.txt`).
- Marża na pacjenta w 90 dniach przed kosztem pozyskania: 58,3 zł wobec 66,6 zł, czyli −8,3 zł.
- **Kolejne zamówienia na pacjenta w 90 dniach** (dopisek Kuby 2026-10-21): 0,234 wobec 0,334, czyli o 29,8% mniej (te same dni kalendarzowe, 18 924 i 12 867 pacjentów; `d_retencja.txt`, punkt 4). Bez pacjentów nowych kampanii 0,300 według przyjętej reguły i 0,277 według sesji płatności.
- **Bez pacjentów nowych kampanii retencja też spada.** Powrót w 90 dniach wynosi 22,0% według przyjętej reguły (14 031 pacjentów) i 20,4% według sesji płatności (15 414), wobec 23,9%. **Marża na pacjenta w 90 dniach poza nowymi kampaniami prawie stoi według przyjętej reguły** (66,0 zł wobec 66,6 zł), a według sesji płatności spada do 63,3 zł (dopisek Kuby 2026-10-21).
- Pacjenci nowych kampanii wracają w 90 dniach w 4,1% (4 893 pacjentów).
- **Według pierwszej usługi, bez pacjentów nowych kampanii** (`d_retencja.txt`, punkt 3; 95% przedział różnicy):
  - spada: po e-recepcie z 33,4% (3 206 pacjentów) do 29,9% (3 570), po wizycie u innego specjalisty z 25,2% (2 325) do 20,6% (2 549);
  - bez istotnej zmiany: pediatra z 22,3% (673) do 26,3% (711), od −0,5 do +8,5 punktu; psychiatra z 22,5% (550) do 24,6% (605), od −2,8 do +7,0 punktu. To małe grupy, więc nie piszemy, że powrót tam rośnie (dopisek Kuby 2026-10-21);
  - pierwsze L4 u internisty z pozostałych kanałów: według przyjętej reguły bez istotnej zmiany, z 14,6% (2 795) do 13,8% (2 969), od −2,6 do +1,0 punktu; według sesji płatności spada do 11,0% (4 114), od −5,2 do −1,9 punktu. „Bez zmiany” trzyma się więc tylko w jednej regule.
- **Liczba osób, które wróciły w 90 dniach, rośnie:** 3 289 wobec 3 076 (+6,9%). Spada odsetek, a nie liczba powracających. Porównanie 90-dniowe obejmuje pierwsze zakupy do 2 lipca każdego roku, a nie pełne roczniki (`c_priorytety.txt`, W2).

### 1c. Najważniejsze zastrzeżenia

1. **Dashboard liczy dane na surowo.** Zawiera 604 zdublowane zamówienia z czerwca 2026, 2 071 zamówień kont testowych i przychód przed zwrotami. Po oczyszczeniu zamówienia rosną o 55,7% zamiast 61%, a przychód z konsultacji po zwrotach o 44,8% zamiast 50% (`ZNALEZISKA.md`, A3). Nowi pacjenci prawie się nie zmieniają (+51,9% na surowo, +52,1% po oczyszczeniu), a TelemediGO wcale (+40,3%; `a3_dashboard.txt`).
2. **Start od zera.** W okresie 1 nie było bazy pacjentów z poprzedniego roku. W okresie 2 pacjenci pozyskani w okresie 1 złożyli 5 289 zamówień powtórnych, które dały 153 tys. zł marży konsultacji (`c_priorytety.txt`, W3). Sumy roczne z definicji faworyzują więc drugi rok.
3. **Wynik biznesu rośnie wolniej niż sprzedaż.** Marża po koszcie lekarza, kampaniach i prowizji wynosi 828 tys. zł w okresie 1 i 1 048 tys. zł w okresie 2, czyli +26,6%. Po odjęciu marży powtórnych konsultacji pacjentów pozyskanych w okresie 1 to +8,1%, a po odjęciu także ich opłat za TelemediGO (41,5 tys. zł) +3,1%. To rozbicie księgowe, a nie wynik biznesu, który startuje od zera: nie modeluje zmian wydatków ani zachowania pacjentów. Wydatki na kampanie rosną o 77% (z 368 do 650 tys. zł).
4. **Struktura pacjentów się zmieniła.** Pacjenci nowych kampanii to 29% nowych pacjentów okresu 2 według przyjętej reguły (7 268 z 24 687) i 21% według sesji płatności (5 187). Zostawiają 36,3 zł marży w 90 dniach wobec 66,0 zł pozostałych.
5. **Obie reguły źródła.** Podział spadku powrotu (z 23,9% do 17,4%) na nowe i stare kampanie zależy od reguły. Według przyjętej reguły to 4,6 punktu procentowego nowych kampanii i 2,0 punktu starych (nowe kampanie: około 71% spadku). Według sesji płatności to 3,0 i 3,5 punktu (około 46%) (`ZNALEZISKA.md`, A5 retencja). Kierunek jest ten sam w obu, a to rozkład opisowy, nie zmierzony wpływ kampanii.
6. **Marża po kwartałach rok do roku** (`c_priorytety.txt`, W4). Wzrost marży słabnie z kwartału na kwartał, a wydatki na kampanie rosną coraz szybciej:

   ```
   kwartał    marża         rok wcześniej   zmiana   wydatki na kampanie   rok wcześniej   iloraz
   IV 2025    259,4 tys. zł   151,3 tys. zł   +71,4%       113,1 tys. zł        87,3 tys. zł    1,30
   I 2026     324,4 tys. zł   226,9 tys. zł   +43,0%       170,6 tys. zł       102,6 tys. zł    1,66
   II 2026    256,6 tys. zł   227,0 tys. zł   +13,0%       184,4 tys. zł        90,4 tys. zł    2,04
   III 2026   207,7 tys. zł   222,8 tys. zł    −6,8%       181,6 tys. zł        87,4 tys. zł    2,08
   ```

   - Marża przed kampaniami (przychód po zwrotach + TelemediGO − koszt lekarza) rośnie w III kwartale 2026 o 25,2% (+79,0 tys. zł), ale wydatki na kampanie rosną o 94,1 tys. zł.
   - We wrześniu 2025 ruszyła sprzedaż TelemediGO w newsletterze (225 zakupów w 23 dni), co podnosi III kwartał 2025. Bez opłat za TelemediGO marża III kwartału 2026 też jest niższa: −4,9% rok do roku.
   - W samych miesiącach: lipiec 2026 73,4 tys. zł wobec 66,8 tys. zł, sierpień 66,3 wobec 67,2 tys. zł, wrzesień 68,0 wobec 88,8 tys. zł. Niższy jest więc kwartał jako całość, a nie każdy miesiąc.
   - **Rozkład spadku III kwartału** (dopisek Kuby 2026-10-21; `d_wynik.txt`, punkt 1; opis księgowy, nie zmierzony wpływ). Marża spadła o 15,1 tys. zł. Według przyjętej reguły pacjenci nowych kampanii zostawili 89,0 tys. zł marży przed kampaniami przy 87,9 tys. zł wydatków, czyli wyszli prawie na zero (+1,1 tys. zł). Reszta biznesu straciła 16,2 tys. zł:
     - opłaty TelemediGO −11,2 tys. zł, w tym −10,5 tys. zł sprzedaży osobnej w newsletterze (225 zakupów we wrześniu 2025 wobec 107 w całym III kwartale 2026);
     - wyższe wydatki kampanii działających w obu latach −6,2 tys. zł;
     - marża konsultacji +1,2 tys. zł: powtórnych zamówień jest więcej (3 140 wobec 2 879), ale każde zostawia mniej marży (32,81 zł wobec 35,86 zł);
     - prowizja bez zmian.
   - **Księgowo lukę, która zostaje po odjęciu TelemediGO (5,0 tys. zł), wyjaśnia wzrost wydatków kampanii działających w obu latach, częściowo skompensowany wzrostem marży konsultacji.** Rozkład księgowy nie rozdziela wpływu Safari od innych zmian przychodu: awaria mogła obniżyć marżę konsultacji, która mimo to wzrosła o 1,2 tys. zł. Według sesji płatności podział się odwraca: nowe kampanie −25,2 tys. zł, reszta +10,1 tys. zł. Suma jest ta sama, a podział między nowe kampanie a resztę zależy od reguły źródła. Cały spadek przypada na wrzesień (−20,8 tys. zł); lipiec +6,6 tys. zł, sierpień −0,9 tys. zł.
   - **Wcześniejsze kwartały okresu 1 nie miały jeszcze bazy powracających** (`d_wynik.txt`, punkt 2). Marża z pacjentów pozyskanych w poprzednich kwartałach to 0% marży IV kwartału 2024, 23,4% I kwartału 2025 i 51,7% III kwartału 2025. Bez tej bazy marża rośnie rok do roku o 8,5% zamiast 71,4% w IV kwartale 2025 i o 26,1% zamiast 43,0% w I kwartale 2026. Wzrost tych kwartałów jest więc zawyżony startem od zera, a miarodajne jest porównanie III kwartałów (baza 51,7% i 51,1% marży). W III kwartale 2026 baza 35 032 pacjentów dała mniej marży niż rok wcześniej baza 12 794 pacjentów (106,2 wobec 115,2 tys. zł): baza jest starsza, a nowsze roczniki wracają rzadziej (opis, bez rozdzielenia tych dwóch rzeczy).
7. **To opis, nie przyczyna.** Widzimy spadek obserwowanej retencji, także po wyłączeniu pacjentów nowych kampanii. Nie dowodzi to, że identyczni pacjenci zachowują się gorzej. Rozkład na strukturę i zachowanie nie mówi też, co by się stało bez nowych kampanii. Spadek w starych kampaniach zbiega się z porannymi opóźnieniami u internistów, ale ich nie dowodzi (sekcja 4, punkt 4).

---

## 2. TelemediGO — cztery pytania Kuby

Raport: `analiza/wyniki/c_telemedigo.txt`. Każde członkostwo kosztuje 89 zł i trwa 365 dni, bez wyjątków. Każde z 9 738 zamówień ze zniżką TelemediGO przypada w czasie ważności członkostwa.

### 2.1 Skąd wzrost sprzedaży o 40%

**W skrócie:** wzrost o 709 zakupów (z 1 759 do 2 468, +40,3%) wynika z tego, że jest więcej zamówień, i z pełnego roku sprzedaży w newsletterze. Odsetek kupujących przy pierwszym zamówieniu spada, a przy kolejnych zamówieniach rośnie tylko lekko (z 9,27% do 9,86%).

- **Typ zakupu** (sekcja 1a):

  ```
  typ zakupu                                   okres 1   okres 2   zmiana   udział we wzroście
  przy kasie z pierwszym zamówieniem pacjenta      905      1 089     +184         26%
  przy kasie z kolejnym zamówieniem                629        918     +289         41%
  osobno, z newslettera crm_go_upsell              225        461     +236         33%
  razem                                          1 759      2 468     +709        100%
  ```

- **Sprzedaż osobna w newsletterze** ruszyła 8.09.2025. W okresie 1 działała więc tylko 23 dni, a sprzedała w nich 225 członkostw. W okresie 2 sprzedaje średnio 38 miesięcznie (sekcja 1b). Możliwe odczytanie: start kampanii zebrał od razu pacjentów, którzy czekali na ofertę. Wysyłek w danych nie ma, więc nie wiemy, ile wiadomości poszło w kolejnych miesiącach.
- **Przy kasie: więcej zamówień, a nie wyższy odsetek kupujących** (sekcja 1e). Liczymy zamówienia pacjentów bez ważnego członkostwa:
  - przy pierwszym zamówieniu odsetek kupujących spada z 5,58% do 4,41%. Więcej zamówień dodaje 471 zakupów, a niższy odsetek odejmuje 287;
  - przy kolejnych zamówieniach odsetek rośnie lekko, z 9,27% do 9,86%. Więcej zamówień dodaje 234 zakupy, a wyższy odsetek 55. Zamówień powtórnych jest więcej głównie przez start od zera.
- **Spadek odsetka przy pierwszym zamówieniu to w całości pacjenci nowych kampanii na L4** (sekcja 1f). Kupuje u nich 1,5% (Meta na L4 1,48%, TikTok 1,49%). Bez nich odsetek stoi: 5,58% wobec 5,63%. W rozkładzie zmiany −1,16 punktu procentowego, a z tego −1,22 przypada na nowe segmenty.
- **Kupujący** (sekcja 1c): nowi pacjenci przy pierwszym zamówieniu +184, pacjenci, którzy już kupowali, ale pierwszy raz biorą TelemediGO, +440, a drugie członkostwo po wygaśnięciu pierwszego +85.
- **Ponowne zakupy są rzadkie** (sekcja 1d). W 90 dniach po wygaśnięciu odnawia 5,4% członków (62 z 1 140), a w 180 dniach 6,3%. Tylko 8,8% byłych członków składa w 90 dniach po wygaśnięciu jakiekolwiek zamówienie. Większość członków nie jest więc aktywna, gdy członkostwo wygasa. W okresie 2 wygasa 1 759 członkostw. W danych nie widać przypomnienia o wygaśnięciu.
- **Kanały** (sekcja 1g): przybyło głównie u pacjentów z wejść bezpośrednich (+212), z bezpłatnego wyszukiwania (+141) i z Google Ads ogólnych (+123).

### 2.2 Ile dają opłaty wobec zniżek udzielonych na wizytach

**W skrócie:** opłata 89 zł nie pokrywa średniej zniżki. Przy założeniu, że te same wizyty zostałyby kupione po cenie katalogowej i bez TelemediGO, opłaty są niższe od zniżek o 11–16 zł na członkostwo. To nie jest strata programu, bo nie wiemy, ile wizyt członkostwo dokłada. Pacjenci, którzy kupują przy kolejnym zamówieniu, dostają zniżek dużo więcej niż płacą.

- **Zniżka efektywna** liczy tylko wizyty, za które zapłata zostaje (odbyte i nieodebrane). Przy anulowanej i zwróconej wizycie pacjent dostaje całą zapłatę z powrotem, więc zniżka nie zmienia przychodu.
- **Członkostwa z okresu 1** mają pełne 365 dni w danych (sekcja 2a):
  - 1 759 członkostw, 156 551 zł opłat;
  - 183 939 zł zniżki efektywnej na 4 902 zamówieniach, czyli 104,57 zł na członkostwo;
  - opłaty minus zniżki: −27 388 zł, czyli −15,57 zł na członkostwo, przy założeniu, że te same wizyty zostałyby kupione bez TelemediGO.
- **Według typu zakupu** (okres 1, zniżka efektywna na członkostwo):
  - przy kasie z pierwszym zamówieniem: 88,94 zł, czyli prawie tyle, ile opłata;
  - przy kasie z kolejnym zamówieniem: 136,36 zł, czyli 47,4 zł więcej niż opłata;
  - osobno z newslettera: 78,56 zł, czyli 10,4 zł mniej niż opłata. Ale 41,8% tych członków nie wykorzystuje zniżki ani razu.
- 38% członkostw dostaje więcej zniżki niż 89 zł. Mediana wynosi 66,3 zł.
- **Członkostwa z okresu 2** idą tym samym torem (sekcja 2b): w pierwszych 180 dniach 77,91 zł zniżki wobec 81,68 zł w okresie 1. Przy tej samej proporcji na resztę roku wyszłoby około 99,7 zł, czyli −10,7 zł na członkostwo. To przybliżenie, nie wynik.
- **Widok kasowy, rok do roku** (sekcja 2c): w okresie 1 opłaty przewyższyły zniżki o 35,8 tys. zł, a w okresie 2 zniżki przewyższyły opłaty o 24,9 tys. zł. W okresie 2 zniżki dostają też członkowie z okresu 1.
- **Zastrzeżenie:** zniżka jest kosztem tylko wtedy, gdy wizyta odbyłaby się i bez TelemediGO. Jeśli członkostwo przyciąga dodatkowe wizyty, każda dodatkowa wizyta u internisty daje marżę (punkt 2.3), a u większości specjalistów stratę.

### 2.3 Czy wizyty ze zniżką pokrywają koszt lekarza

**W skrócie:** u internisty po zniżce 50% tak, u psychiatry po zniżce 20% ledwo, u pozostałych specjalistów nie. W okresie 2 wizyty ze zniżką u specjalistów poza psychiatrą przyniosły 14,7 tys. zł straty.

- **Cennik** (sekcja 3a; ceny z danych, koszt lekarza za wizytę odbytą):

  ```
  specjalizacja                          cena   po zniżce   koszt lekarza   marża bez zniżki   marża ze zniżką
  internista (zniżka 50%)                 89,0      44,5          25              64,0             +19,5
  psychiatra                             269,0     215,2         200              69,0             +15,2
  endokrynolog, ginekolog                119,0      95,2         100              19,0              −4,8
  dermatolog, kardiolog, neurolog, urolog 109,0     87,2         100               9,0             −12,8
  psycholog                               99,0      79,2         100              −1,0             −20,8
  pediatra                                95,0      76,0         100              −5,0             −24,0
  ```

- **Rzeczywiste zamówienia z obu lat, z anulacjami, nieodebranymi i zwrotami** (sekcja 3b, marża na zamówienie):
  - internista: 18,6 zł ze zniżką wobec 59,4 zł bez zniżki;
  - psychiatra: 17,0 zł wobec 65,4 zł;
  - pediatra: −21,8 zł wobec −3,6 zł;
  - pozostali specjaliści ze zniżką od −2,6 zł (ginekolog) do −19,4 zł (psycholog).
- **Razem** (sekcja 3c): u specjalistów poza internistą i psychiatrą marża zamówień ze zniżką wynosi −7 845 zł w okresie 1 (753 zamówienia) i −14 682 zł w okresie 2 (1 512 zamówień). Zniżka efektywna na tych zamówieniach to 15 539 zł i 31 405 zł.
- **Znalezisko poboczne (zależy od założenia 33):** wizyta u pediatry przynosi stratę także bez zniżki (cena 95 zł przy koszcie lekarza 100 zł), a u psychologa wychodzi prawie na zero. Przy koszcie pediatry 25 zł (wariant z założenia 33) wizyta u pediatry jest dochodowa; psycholog (99 zł przy koszcie 100 zł) zostaje na granicy zera. Prawdziwej stawki pediatry nie znamy (sekcja 4).

### 2.4 Czy TelemediGO zmienia powroty

**W skrócie:** kupujący TelemediGO wracają dużo częściej niż podobni pacjenci, ale dane nie mówią, ile z tego to wpływ zniżki, a ile to, że kupują ci, którzy i tak planują wracać. Obie kontrole dają wyniki zgodne z kilkoma wyjaśnieniami i żadna tego nie rozstrzyga. Rozstrzygnie test.

- **Porównanie z podobnymi pacjentami** (sekcja 4a). Nowi pacjenci, którzy kupili TelemediGO przy pierwszym zamówieniu, wobec pacjentów bez niego z tego samego okresu, kanału pozyskania, pierwszej usługi i miesiąca kohorty:
  - powrót w 90 dniach: okres 1 — 34,3% wobec 24,2% (905 kupujących), czyli +10,1 punktu procentowego (od +6,9 do +13,4); okres 2 — 34,7% wobec 20,0% (858), czyli +14,6 punktu (od +11,4 do +17,8);
  - kolejne zamówienia w 365 dniach (okres 1): 1,31 wobec 0,74 na pacjenta;
  - marża w dniach 1–365 jest u kupujących niższa o 21,9 zł, bo płacą mniej za każdą wizytę;
  - **z opłatą 89 zł i zniżką na pierwszym zamówieniu** (dni 0–365) kupujący zostawiają o 31,6 zł więcej marży niż podobni pacjenci (117,3 zł wobec 85,7 zł);
  - dodanie statusu pierwszego zamówienia do warstw prawie nic nie zmienia.
- **Kontrola 1: przebieg zamówień przed wygaśnięciem członkostwa i po nim, wśród kupujących bez kolejnego zakupu członkostwa** (sekcja 4b, okres 1, 683 kupujących). Gdyby przewagę dawała tylko niższa cena, po wygaśnięciu powinna zniknąć:
  - dni 1–90: zamawia 34,7% kupujących wobec 19,1% podobnych, iloraz 1,82;
  - dni 276–365 (ostatni kwartał ważności): 8,5% wobec 2,3%, iloraz 3,77. Możliwe odczytanie: pacjenci wykorzystują zniżkę przed końcem ważności;
  - dni 366–455 (po wygaśnięciu): 2,9% wobec 1,7%, iloraz 1,77, różnica +1,3 punktu (od −0,2 do +2,7).
  - wśród wszystkich pierwotnych kupujących (707, także odnawiający) po wygaśnięciu zamawia 6,2% wobec 1,6%, ale tu część zamówień jest już na nowym członkostwie;
  - **Odczytanie:** w punktach przewaga maleje, ale w proporcji zostaje prawie taka sama jak na początku. Wynik jest zgodny z kilkoma wyjaśnieniami (samoselekcja, nawyk, zniżka) i nie rozstrzyga między nimi. Liczby po wygaśnięciu są małe, a wyłączenie odnawiających zależy od zachowania po zakupie i zabiera z grupy najaktywniejszych (recenzja Codeksa).
- **Kontrola 2: pacjenci, którzy weszli z newslettera sprzedającego TelemediGO** (sekcja 4c). Kupujący osobno wobec pacjentów bez zakupu przy wejściu i przez następne 30 dni. Obie grupy zainteresowały się ofertą:
  - w 180 dniach przed zakupem (albo przed wejściem bez zakupu) mieli prawie tyle samo zamówień: 2,93 kupujący (450 pacjentów) i 3,04 pozostali (189);
  - w 180 dniach po: 1,51 wobec 1,22;
  - różnica różnic: +0,40 zamówienia na pacjenta w 180 dniach. 15 ze 189 pacjentów grupy porównawczej kupuje członkostwo później; bez nich różnica wynosi +0,49;
  - **Odczytanie:** przy podobnej historii kupujący zamawiają potem więcej. To statystyka opisowa, która zakłada równoległe trendy obu grup. Dopuszcza wpływ zniżki, ale decyzja o zakupie może też wynikać z wizyty, którą pacjent już planował. Grupa porównawcza jest mała. Lepsze porównanie na tych danych to dopasowanie przy wejściu według miesiąca, stażu, czasu od ostatniej konsultacji i wcześniejszych zamówień (recenzja Codeksa; do zrobienia, jeśli Kuba uzna to za potrzebne).
- **Test, który to rozstrzygnie** (sekcja 4d; koszt: `c_priorytety.txt`, P10):
  - **losowe członkostwo próbne:** połowa nowych pacjentów dostaje bezpłatny dostęp do zniżek TelemediGO na 90 dni, od dnia po pierwszym zamówieniu. Druga połowa nie dostaje. Porównujemy powrót w 90 dniach i marżę. Tu nie ma samoselekcji, bo o członkostwie decyduje losowanie. Test mierzy wpływ niższej ceny, ale sam nie rozstrzyga, czy płatny program za 89 zł się opłaca;
  - różnice z porównania służą tylko jako scenariusze efektu. Jeśli wpływ zniżki to jedna czwarta obecnej różnicy (3,7 punktu procentowego), potrzeba 1 823 pacjentów na grupę, czyli około 1,8 miesiąca pozyskania plus 90 dni obserwacji. Dodatkowy koszt to około 12,2 tys. zł zniżek przy obecnym zachowaniu pacjentów. Jeśli wpływ to połowa różnicy, wystarczy 487 pacjentów na grupę i około 3,3 tys. zł;
  - losowe pokazywanie samej oferty przy kasie nie wystarczy, bo kupuje tylko 4,5% pacjentów i efekt ginie w grupie (potrzeba ponad 4 lat pozyskania).

### 2.5 Co z tego wynika dla listy priorytetów (propozycja)

- Warunki TelemediGO u specjalistów i cennik specjalistów to pozycja 10 listy.
- **Nie promujemy mocniej sprzedaży ani odnowień TelemediGO przed testem.** Jeśli wizyty odbyłyby się i bez członkostwa, opłaty są niższe od zniżek o około 11–16 zł na członkostwo. Program opłaca się tylko wtedy, gdy przyciąga dodatkowe wizyty, zwłaszcza u internisty. Test to pozycja 12 listy.

---

## 3. Lista priorytetów — wersja ostateczna, przyjęta przez Kubę 2026-10-20 (po konsylium)

**Zasady listy:**
- Wartość to zmiana marży na rok. Rokiem bazowym jest okres 2. Marża = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza − wydatki na kampanie − prowizja.
- Przy kampaniach podajemy wynik po 90 i po 180 dniach od pozyskania (dopisek Kuby) oraz obie reguły źródła. Kwoty kampanii, które działały krócej niż rok, przeliczamy na pełny rok przy tym samym tempie: TikTok działał w okresie 2 przez 234 dni (mnożnik 1,56), Meta na L4 przez 332 dni (1,10) (`c_priorytety.txt`, P11).
- **Tempo ostatniego półrocza** (dopisek Kuby 2026-10-21; `d_kampanie.txt`, punkt 3): od 1.04 do 30.09.2026 obie kampanie wydają dziennie więcej niż średnio (Meta na L4 o 14,9%, TikTok o 14,3%), a nowych pacjentów przybywa dziennie tylko o 9,2% i 12,5% więcej. W tym tempie wynik kampanii jest gorszy niż w przeliczeniu ze średniej: Meta na L4 +23,1 zamiast +30,6 tys. zł rocznie, TikTok −23,2 zamiast −18,6 tys. zł (przyjęta reguła, 90 dni). Kierunek żadnej decyzji się nie zmienia.
- **Każda kwota to osobny scenariusz** liczony względem tego, co działo się w okresie 2, a nie wynik po kolei wdrożonych wcześniejszych pozycji. Jedyny wyjątek: naprawę obietnicy L4 (pozycja 5) wyceniamy tylko dla Meta, bo zakładamy wstrzymanie TikToka (pozycja 3). **Kwot nie sumujemy:** mają różne horyzonty i nakładają się na siebie.
- **Kolejność to waga, a nie kalendarz** (dopisek Kuby 2026-10-21). Najpierw pewne straty, które rosną każdego dnia i łatwo je naprawić (pozycje 1 i 2). Potem pauzy, które da się cofnąć (3 i 4). Potem naprawy, diagnozy, testy i sprawdzenia (5–10). Na końcu rzeczy o nieznanym znaku albo nieznanej wartości (11 i 12). Pozycje 1, 3, 4 i krótkie sprawdzenia (pierwsze kroki pozycji 2, 6, 8 i 11) zespół może zrobić równolegle w pierwszym tygodniu.
- **Zasada budżetu:** pieniędzy uwolnionych przez pozycje 3 i 4 nie przesuwamy automatycznie do innych kampanii, bo kolejna złotówka zarabia zwykle mniej niż średnia. Przesuwamy tylko z testem. Niewydanie ich też liczy się do marży.
- Czas wdrożenia to nasz szacunek, a nie liczba z danych.
- **Co się zmieniło po przeglądzie Kuby i po konsylium:**
  - pomiar zaraz po Safari (dopisek Kuby), rozszerzony o alarmy w codziennym raporcie;
  - wstrzymanie TikToka i kampanii Google Ads na specjalistów na miejsca 3 i 4 (konsylium: strata w obu regułach i horyzontach, wyłączenie darmowe i odwracalne);
  - obietnica L4 na miejsce 5 i tylko w Meta;
  - poranna obsada przed testem zalogowanych i testem Meta (dopisek Kuby), jako diagnoza;
  - nowa pozycja 7: komunikacja po wizycie z grupą kontrolną (konsylium);
  - cennik specjalistów dołączony do warunków TelemediGO w pozycji 10 (konsylium).

**Przegląd:**

| # | Co robimy | Ile warte rocznie (marża) | Pewność | Wdrożenie |
|---|---|---|---|---|
| 1 | Naprawić zakładanie konta w Safari na iOS | 75–83 tys. zł (90 dni), 86–95 tys. zł (180 dni); górna granica | wysoka: awaria widoczna w danych | dni |
| 2 | Naprawić pomiar: raport bez duplikatów i kont testowych, przychód po zwrotach, zamknąć testy TEST-QA, wynagrodzenie lekarzy za testy, alarmy na lejku i zwrotach | 0 albo 38 tys. zł bezpośrednio; pośrednio warunek pozostałych decyzji | wysoka: oba błędy widoczne w danych | 1 dzień sprawdzenie, 1–2 tygodnie raport |
| 3 | Wstrzymać TikToka na L4 | przy 100% pacjentów dodatkowych, pełny rok: +18,6 do +48,0 tys. zł (90 dni), +21,0 do +50,4 tys. zł (180 dni); więcej przy mniejszej dodatkowości | wysoka co do znaku: wynik ujemny w obu regułach po 90 dniach i, w przybliżeniu dla całego rocznika, po 180 dniach | 1 dzień |
| 4 | Wstrzymać `gs_generic_specjalisci` (Google Ads na specjalistów) do czasu zmiany cennika | +19,4 do +31,5 tys. zł przy 100% pacjentów dodatkowych, do +53,2 tys. zł | wysoka co do znaku | 1 dzień |
| 5 | Uczciwa obietnica w reklamach L4 Meta (test dwóch kreacji) | 18,1–46,5 tys. zł (przyjęta reguła), 10,7–26,7 tys. zł (sesja płatności), pełny rok | średnia: nie znamy powodu zwrotów | 1–2 tygodnie + 4–6 tygodni pomiaru |
| 6 | Poranna obsada internistów: diagnoza, potem test | scenariusz od 0 do 65 tys. zł; wariant wąski około 12 tys. zł; koszt obsady nieznany | niska co do kwoty | diagnoza 1–2 dni, test 2–4 tygodnie |
| 7 | Komunikacja po wizycie z losową grupą kontrolną (retencja) | scenariusz: 23,6 tys. zł za każdy punkt procentowy powrotu w 90 dniach | niska co do kwoty | dane o wysyłkach dni, sekwencja 2–4 tygodnie, pomiar 90 dni |
| 8 | Sprawdzić ręcznie zakup dla zalogowanych pacjentów | 0 albo 36–40 tys. zł (wysoki scenariusz 89 tys. zł) | niska: dane wskazują raczej na 0 zł | 1 dzień |
| 9 | Test dodatkowości Meta na L4 w parach województw, z progiem decyzji około 85% (po naprawie zwrotów około 70%) | decyzja warta od −30,6 (90 dni) albo −32,9 (180 dni) do +179,6 tys. zł, pełny rok | — (to jest test; w 4–6 tygodni nie odróżni wyniku od progu, więc decyduje reguła ustalona z góry) | 1 tydzień + 4–6 tygodni |
| 10 | Cennik specjalistów i warunki TelemediGO u specjalistów | TelemediGO: scenariusze 15–31 tys. zł po pełnym roku (w pierwszym około połowa); cennik: do 73,6 tys. zł za każde 10 zł podwyżki przy tej samej liczbie wizyt (górna granica) | wysoka co do kierunku, niska co do kwoty cennika | 1–2 tygodnie + test dwóch cen 4 tygodnie |
| 11 | Sprawdzić stratę między kliknięciem a sesją w Meta i TikToku | 0 albo do 52 tys. zł (górna granica, po wstrzymaniu TikToka mniej) | niska | 1–2 dni |
| 12 | Test TelemediGO z losowym, bezpłatnym dostępem do zniżek | decyduje o roli programu; koszt testu 3–12 tys. zł | — (to jest test) | 2–8 tygodni + 90 dni |

### Pozycja 1. Naprawić zakładanie konta w Safari na iOS

- **Z danych:** od 17.03.2026 w Safari na iPhone'ach i iPadach gwałtownie spada skuteczność zakładania nowego konta (konta dalej powstają, ale rzadziej: 668 zamiast 1 082 w 60 dniach). Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spada z 66,1% (1.10.2025–16.03.2026) do 45,6% (17.03–30.09.2026) i nie wraca. Logowanie do istniejących kont działa. Inne przeglądarki tego nie mają, a spadek jest w głównych kanałach; TikTok ma za małą próbę do oceny (`a5_pozyskanie.md`, sekcja 2).
- **Ile warta:** w 198 dniach od 17.03 do 30.09.2026 to 628–695 utraconych pierwszych zamówień, czyli 1 158–1 281 rocznie. Nowy pacjent z pierwszą płatnością w Safari na iOS zostawia w okresie 2 średnio 64,6 zł marży przed kosztem pozyskania w 90 dniach i 74,3 zł w 180 dniach. Daje to **75–83 tys. zł rocznie w horyzoncie 90 dni i 86–95 tys. zł w horyzoncie 180 dni** (`c_priorytety.txt`, P1). **W samym III kwartale 2026 szacowana marża utracona to około 14,6–18,3 tys. zł (258–323 utracone pierwsze zamówienia z ich powrotami w tym samym kwartale, zależnie od odjęcia tła i założonego tempa strat), a osobny scenariusz powrotów pacjentów utraconych od 17.03 do 30.06 daje 4,1–4,5 tys. zł. To kwota tego samego rzędu co spadek marży rok do roku (15,1 tys. zł); wyniku kwartału bez awarii nie mierzymy** (`d_wynik.txt`, punkt 1f). Wcześniejsza kwota „14–21 tys. zł” mieszała marżę z dnia zakupu z marżą rocznika do 91. dnia. 628–695 to scenariusz przy przyjętych założeniach, a nie przedział ufności.
- **Założenia:** utracone pierwsze zamówienie to utracony nowy pacjent (górna granica: odpadnięci nie kupują później częściej w tej samej przeglądarce, ale innych urządzeń nie widzimy); nie doliczamy kosztu pozyskania, bo wejście już zostało opłacone; skala problemu utrzymywałaby się przez rok (przeliczenie z marca–września może zaniżać, bo pomija zimę). Kwoty to marża rocznika odzyskanych pacjentów, a nie wpływy w całości w tym samym roku.
- **Po czym poznamy:** krok konta po wyborze terminu w Safari na iOS u osób, które jeszcze nie kupowały, wraca z około 46% do około 66% w ciągu tygodnia od poprawki, a zakładanie kont wraca do poziomu sprzed 17.03 (około 1 080 w 60 dniach).
- **Wdrożenie:** powtórzenie rejestracji na iPhonie, logi błędów i lista zmian z 16–17.03.2026 to 1–2 dni. Sama poprawka to zwykle dni.

### Pozycja 2. Naprawić pomiar (dopisek Kuby; rozszerzone o alarmy po konsylium)

- **Z danych:** codzienny raport liczy dane na surowo. Zawiera 604 zdublowane zamówienia z 10–24.06.2026, 2 071 zamówień 22 kont testowych i przychód przed zwrotami. Konta testowe mają kod TEST-QA albo zamówienia bez kodu, a wszystkie ich wizyty trwają 1 minutę u internisty. Przez to raport pokazuje +60,7% zamówień zamiast +55,7% i +50,3% przychodu z konsultacji zamiast +44,8% po zwrotach. Testów przybywa: 553 zamówienia w okresie 1 i 1 518 w okresie 2. Raport liczy też zamówienia i przychód, a nie marżę po koszcie pozyskania i powroty kohort. Dlatego kampanie na L4 wyglądały na nim jak wzrost.
- **Co robimy:**
  - raport bez duplikatów i kont testowych, przychód po zwrotach;
  - testy przeniesione z produkcji na środowisko testowe;
  - jednodniowe sprawdzenie w dziale rozliczeń, czy lekarze dostają wynagrodzenie za wizyty testowe;
  - sprawdzenie, czy kod TEST-QA nie wyciekł poza 22 konta i czy przy duplikatach nikt nie zapłacił dwa razy;
  - do raportu marża po koszcie pozyskania według źródła, zwroty po wizycie według kampanii, powrót w 90 dniach każdej kohorty dziennej i kroki lejka według przeglądarki, z alarmami;
  - **do pilnowania: koszt kliknięcia w Google Ads na markę rośnie** (dopisek Kuby 2026-10-21; `d_kampanie.txt`, punkt 4). Z 1,01 zł do 1,19 zł (+17,9% rok do roku, 13 894 i 19 828 kliknięć), co kwartał wyżej. Koszt pierwszego zamówienia z tej kampanii rośnie z 7,53 zł do 11,33 zł (przyjęta reguła). Kampania na e-receptę drożeje o 18,9% za kliknięcie, a całe Google Ads tanieje o 3,5%. Od 22.05.2026 spada też konwersja sesji tej kampanii do płatności (niewiadoma 22).
- **Ile warta** (`c_priorytety.txt`, P1b i P15):
  - bezpośrednio **37 950 zł rocznie**, jeśli lekarze dostają 25 zł za każdą wizytę testową (wszystkie są u internisty), albo 0 zł, jeśli nie dostają. Pieniądze już wypłacone są stracone, a oszczędność dotyczy kolejnych miesięcy;
  - pośrednio: bez poprawnych liczb nie da się prowadzić biznesu na kohortach. Alarm na krokach lejka wykryłby awarię Safari po kilku dniach, a nie po 198. Wykrycie po tygodniu ograniczyłoby stratę do 3,5% (22–25 zamówień zamiast 628–695).
- **Po czym poznamy:** raport pokazuje te same liczby co nasza oczyszczona warstwa danych (w okresie 2: 38 491 zamówień i 3,228 mln zł przychodu z konsultacji po zwrotach), a od ustalonej daty na produkcji nie ma zamówień testowych.
- **Wdrożenie:** sprawdzenie wynagrodzeń 1 dzień; raport i testy 1–2 tygodnie; alarmy 2–4 tygodnie.

### Pozycja 3. Wstrzymać kampanię TikTok na L4

- **Z danych:** wynik na pacjenta jest ujemny w obu regułach i w obu oknach: −4,6 i −17,8 zł po 90 dniach, −1,1 i −11,0 zł po 180 dniach. Pacjenci wracają w 90 dniach w 3,2% (`a5_ekonomia.md`, sekcje 1–2).
- **Naprawić albo wyłączyć — obie drogi** (`c_priorytety.txt`, P3 i P11; kwoty z 234 dni działania, w nawiasie pełny rok):
  - **dziś:** −11,9 tys. zł (−18,6) według przyjętej reguły i −30,8 tys. zł (−48,0) według sesji płatności po 90 dniach; −13,5 i −32,3 tys. zł po 180 dniach;
  - **naprawić zwroty** (wariant A, najlepszy): wynik +3,0 tys. zł albo −23,2 tys. zł po 90 dniach; +1,4 i −24,7 tys. zł po 180 dniach. Przeglądarki wbudowane w aplikacje nie dają w tym rachunku nic;
  - **wyłączyć:** przy 100% pacjentów dodatkowych +11,9 do +30,8 tys. zł (+18,6 do +48,0 na pełny rok) po 90 dniach i +13,5 do +32,3 tys. zł (+21,0 do +50,4 na pełny rok) po 180 dniach; przy 0% +82,5 tys. zł (+128,6).
- **Propozycja:** wstrzymać od razu, jako odwracalną pauzę. W przyjętych scenariuszach wyłączenie poprawia wynik w każdej regule, każdym oknie i każdym wariancie dodatkowości, a naprawa przy pełnym budżecie w najlepszym razie doprowadza wynik do zera. Wynik po 180 dniach (−1,1 zł na pacjenta według przyjętej reguły, warunkowy przedział od −5,3 do +3,0 zł) obejmuje tylko wczesne kohorty z 10.02–3.04.2026 (299 pacjentów; `d_kampanie.txt`, punkt 2). Miały one tańsze pozyskanie niż cały rocznik (32,4 zł wobec 37,3 zł), a w dniach 91–180 nie dorobiły marży. Lepszy wynik niż po 90 dniach (−4,6 zł, 1 265 pacjentów) daje więc tańsze pozyskanie, a nie późniejsze powroty. Przybliżenie dla całego rocznika (marża w 90 dniach wszystkich kohort plus przyrost z dni 91–180 wczesnych kohort, minus koszt pozyskania całego rocznika) daje −5,4 zł (od −7,4 do −3,4 zł) według przyjętej reguły i −19,3 zł według sesji płatności. Znak jest więc ujemny w obu regułach (sprawdzenie po dopisku Kuby 2026-10-21). Naprawy (obietnica, ładowanie strony) sprawdzamy na Meta. TikTok może wrócić jako mały test, jeśli zadziałają.
- **Po czym poznamy:** zmianę po pauzie porównujemy z ustalonym z góry punktem odniesienia (te same tygodnie rok wcześniej i kanały bez zmian): marża całego biznesu po wydatkach rośnie, a łączna liczba nowych pacjentów spada mniej niż liczba pacjentów przypisanych dotąd TikTokowi. Sam wzrost marży po pauzie nie dowodzi skutku, bo może wynikać z sezonu. Pauza daje przy okazji słaby, darmowy pomiar dodatkowości.
- **Wdrożenie:** 1 dzień.

### Pozycja 4. Wstrzymać `gs_generic_specjalisci` (Google Ads ogólne na specjalistów) do czasu zmiany cennika

- **Z danych:** wynik na pacjenta jest ujemny w obu regułach i obu oknach: −23,7 i −44,7 zł po 90 dniach, −14,3 i −36,6 zł po 180 dniach. Koszt pozyskania wynosi 57,6 zł (przyjęta reguła) albo 80,9 zł (sesja płatności) przy marży pacjenta przed kosztem pozyskania 32–37 zł. Jednym z głównych ograniczeń marży jest cennik: wizyta u specjalisty po cenie katalogowej zostawia tylko 9–19 zł ponad koszt lekarza (pozycja 10). Wynik zależy też od kosztu pozyskania, struktury usług i powrotów.
- **Naprawić albo wyłączyć** (`c_priorytety.txt`, P7; 923 nowych pacjentów rocznie według przyjętej reguły, 657 według sesji płatności, wydatki 53,2 tys. zł):
  - **dziś:** −23,2 tys. zł i −31,5 tys. zł po 90 dniach; −19,4 i −30,2 tys. zł po 180 dniach (bez pośredniego zaokrąglania marży, `c_priorytety.txt`, P7);
  - **naprawić:** sama kampania musiałaby obniżyć koszt pozyskania o 40–60%, a to inny model kampanii, nie naprawa. Główną drogą naprawy jest cennik (pozycja 10). Uwaga: awaria Safari od 17.03 zawyża koszt pozyskania także tej kampanii;
  - **wyłączyć:** +19,4 do +31,5 tys. zł przy 100% pacjentów dodatkowych, +36,3 do +42,4 tys. zł przy 50%, +53,2 tys. zł przy 0%. Założenia: `ZALOZENIA.md` 42.
- **Propozycja:** wstrzymać. Wrócić po zmianie cennika albo gdy koszt pozyskania nie przekracza marży pacjenta w 90 dniach w obu regułach.
- **Po czym poznamy:** marża po wydatkach rośnie, a nowych pacjentów u specjalistów z pozostałych kanałów nie ubywa więcej, niż kampania przypisywała.
- **Wdrożenie:** 1 dzień.

### Pozycja 5. Uczciwa obietnica w reklamach L4 Meta i na stronie wejścia: mniej zwrotów po wizycie

- **Z danych:** 17,4% odbytych wizyt L4 pacjentów nowych kampanii kończy się zwrotem po wizycie (1 024 z 5 895), wobec 5,3% L4 pozostałych pacjentów. Kod rabatowy ani opóźnienie wizyty nie zmieniają tego odsetka. Za zwróconą wizytę lekarz dostaje wynagrodzenie.
- **Ile warta po wstrzymaniu TikToka** (tylko Meta; `c_priorytety.txt`, P11): **18,1–46,5 tys. zł rocznie według przyjętej reguły i 10,7–26,7 tys. zł według sesji płatności**, na pełny rok. Wynik po 180 dniach jest taki sam, bo ci pacjenci prawie nie wracają. Jeśli test (pozycja 9) pokaże, że Meta trzeba wyłączyć, ta pozycja jest warta zero.
- **Założenia i zastrzeżenia:**
  - dolny wariant zakłada, że uczciwa reklama odstrasza tylko tych, którzy i tak dostaliby zwrot; w praktyce odstraszy też część pozostałych, więc może być niżej;
  - górny wariant („wizyta zostaje opłacona”) może wymagać zmiany zasad zwrotów, a nie samej treści reklamy. To osobna decyzja z ryzykiem prawnym i wizerunkowym;
  - 5,3% to odsetek z innej grupy pacjentów, więc pełne zrównanie jest optymistyczne. Rozsądny wariant bazowy to zmniejszenie luki o połowę.
- **Co robimy:**
  - najpierw jednodniowe sprawdzenie, co obiecują reklama, strona `/zwolnienie-l4-online` i regulamin przy odmowie L4;
  - potem nowa kreacja i pytanie przed płatnością („lekarz wystawia L4 tylko przy wskazaniach medycznych”);
  - w Meta losowy podział ruchu na starą i nową kreację, z osobnym oznaczeniem kampanii;
  - **wysokość kodu rabatowego do przetestowania** (dopisek Kuby 2026-10-21; `d_kampanie.txt`, punkt 6). Kod L4SZYBKO20 (20 zł) jest na 3 511 z 5 059 pierwszych zamówień pacjentów kampanii w okresie 2 (przyjęta reguła). Daje to 62,8 tys. zł zniżki efektywnej na pełny rok (bez wizyt anulowanych i zwróconych). Zwroty po wizycie przy pierwszym zamówieniu z kodem rabatowym i bez są prawie takie same (14,5% z 3 680 wobec 14,3% z 1 379 pierwszych zamówień), a powrót w 90 dniach nie różni się istotnie (4,15% z 2 649 wobec 5,41% z 979 pacjentów). Progi rachunku (parametry scenariusza, a nie odsetki z danych): rezygnacja z kodu opłaca się, jeśli ubędzie mniej niż 33,7% zamówień z kodem, a przejście na stały kod START10 (10 zł), jeśli mniej niż 20,2%. Reakcji pacjentów na niższy kod nie znamy, więc to scenariusz do testu w losowym podziale ruchu, a nie kwota (niewiadoma 21).
- **Po czym poznamy:** odsetek zwrotów po wizycie L4 przy nowej kreacji spada wobec starej, a marża na kliknięcie nie spada. Liczy się marża, nie sam odsetek zwrotów.
- **Wdrożenie:** 1–2 tygodnie zmian i 4–6 tygodni pomiaru.

### Pozycja 6. Poranna obsada internistów: diagnoza, potem test (dopisek Kuby: przed testem zalogowanych i testem Meta)

- **Z danych:** od listopada 2025 poranne opóźnienia u internisty rosną z miesiąca na miesiąc. Odsetek wizyt z terminem 6:00–11:59, które zaczynają się ponad 15 minut po terminie, wynosi 15,6% w listopadzie 2025, 29,7% w grudniu i 41,8% w styczniu 2026, a od lutego do września 2026 około połowy (48,4–52,6% miesięcznie). Od października 2024 do października 2025 było to 4,7–6,9% miesięcznie (wszyscy pacjenci; `a5r_punktualnosc.txt`, tabela miesięczna). Przy tym samym porannym ruchu opóźnień jest o 26,4 punktu procentowego więcej. Długość porannej wizyty się nie zmieniła (8,5 minuty w obu okresach), więc dłuższe wizyty tego nie tłumaczą.
  - **Po godzinach** (dopisek Kuby 2026-10-21; `d_retencja.txt`, punkt 1; internista, wszyscy pacjenci): największy wzrost to jeden blok od 5:00 do 12:59, a mniejszy zostaje o 13:00. Wizyt spóźnionych ponad 15 minut jest o 5:00 15,3% (459 wizyt) wobec 1,5% (267) rok wcześniej, o 6:00–10:00 od 40,4% do 47,0% (865–1 858 wizyt w godzinie) wobec 5,7–7,5%, o 12:00 22,3% (1 303) wobec 3,4% (774), o 13:00 5,6% (1 207) wobec 2,5% (719). Poza 5:00–13:59 odsetek jest prawie taki sam: 2,7% z 14 898 wizyt wobec 2,8% z 9 563. Wzrost w południe i w nocy to głównie brzegi porannego bloku: południe bez 12:00 rośnie z 2,9% do 3,9%, noc bez 5:00 z 2,0% do 3,1%. U pozostałych lekarzy rano bez istotnej zmiany (2,8% z 1 949 wizyt wobec 3,0% z 2 757).
  - **W ciągu poranka** (dopisek Kuby 2026-10-21; `d_retencja.txt`, punkt 2): już wizyty z najwcześniejszym porannym terminem w danym dniu są często spóźnione, a w danych zagregowanych nie widać narastania opóźnień w ciągu poranka. Wizyty z najwcześniejszym porannym terminem dnia są spóźnione ponad 15 minut w 41,9% (391 wizyt, okres 2), kolejne w 43,3% (8 760), średnio 18,7 wobec 20,2 minuty. W tym samym miesiącu (II–IX 2026) godziny z 8 i więcej wizytami mają o 4,2 punktu procentowego więcej spóźnionych niż godziny z 1–3 wizytami. **Odczytanie, nie pomiar:** to bardziej pasuje do stałego przesunięcia od początku dnia (późniejszy start względem grafiku, inna organizacja zapisów albo kolejki) niż do kolejki, która narasta, bo pacjentów jest więcej, niż lekarze zdążą przyjąć. Najwcześniejszy termin liczymy dla całej sieci, a nie dla pojedynczego lekarza. Bez identyfikatorów lekarzy i grafików mechanizmu nie rozstrzygamy. Wizyty spóźnione ponad 30 minut mają średnią ocenę 2,92 wobec 4,45 przy punktualnych (469 i 3 446 ocen). Rano spada powrót po wizytach spóźnionych.
- **Dlaczego wysoko:** to jedna z konkretnych hipotez poprawy retencji pacjentów z kanałów działających w obu latach (obok komunikacji po wizycie i zniżek), a pierwszy krok, diagnoza, jest tani (dopisek Kuby).
- **Ile warta:** scenariusz od 0 zł do 65,2 tys. zł marży rocznie w horyzoncie 180 dni (`c_priorytety.txt`, P8). Wariant wąski, czyli sama zmiana rozkładu opóźnień pierwszej wizyty, to 11,9–12,7 tys. zł zależnie od reguły źródła; prawie cały przypada na poranne pierwsze wizyty u internisty (12,6 tys. zł). Wariant szeroki (31,8–65,2 tys. zł) przypisuje opóźnieniom cały spadek powrotu w starych kampaniach, więc nie jest górną granicą skutku obsady (`d_wynik.txt`, punkt 4). Związek opóźnień z powrotami może częściowo wynikać z tego, kto przychodzi rano, więc kwota jest niepewna. Kosztu dodatkowej obsady nie ma w danych.
- **Co robimy:** diagnoza (grafiki i obsada poranna przed i po 3.11.2025, obciążenie lekarzy pacjentami spoza B2C, rozmowa z osobami od grafików). Potem naprawy, także bez dodatkowej obsady: liczba porannych terminów dopasowana do przepustowości, przesunięcie godzin lekarzy, realny czas oczekiwania pokazany pacjentowi. Na końcu test w losowo wybrane dni.
- **Po czym poznamy:** odsetek porannych wizyt spóźnionych ponad 15 minut spada z około 50% poniżej 10%, oceny porannych wizyt rosną, a powrót w 90 dniach pacjentów z pierwszą wizytą rano, z tego samego źródła, wraca w stronę 23–24%.
- **Wdrożenie:** diagnoza 1–2 dni, test 2–4 tygodnie, efekt w powrotach po 90 dniach.

### Pozycja 7. Komunikacja po wizycie z losową grupą kontrolną (nowa, po konsylium)

- **Z danych:** retencja to połowa definicji wzrostu, a spada także bez pacjentów nowych kampanii (powrót w 90 dniach 22,0% wobec 23,9%). Po wejściu z newslettera albo SMS-a wraca w okresie 2 3,16% pacjentów spoza nowych kampanii, a bez takiego wejścia 18,84%, więc to około 14% obserwowanych pierwszych powrotów. Liczba wejść z newslettera i SMS-ów na 1 000 pacjentów spada z 56–108 do 24–52 miesięcznie, ale mianownikiem jest cała narastająca baza pacjentów; w pierwszych 90 dniach od zakupu odsetek pacjentów z takim wejściem rośnie lekko z 17,5% do 17,9%. Widać kliknięcia, a nie wysyłki (`a5_retencja.md`, krok 4c; `a5r_po_zakupie.txt`).
- **Ile warta:** scenariusz: każdy punkt procentowy powrotu w 90 dniach to około **23,6 tys. zł marży rocznie** (24 687 nowych pacjentów × 1% × 95,6 zł), a bez pacjentów nowych kampanii 16,7 tys. zł (`c_priorytety.txt`, P12). To różnica obserwacyjna, a nie zmierzony efekt wiadomości.
- **Co robimy:** dane o wysyłkach (ile, komu, kiedy); sekwencja po pierwszej wizycie (przypomnienie o kontynuacji leczenia, recepta, kontrola), zawsze z losową grupą kontrolną bez wysyłki.
- **Po czym poznamy:** różnica powrotu w 90 dniach i marży między grupą z wysyłką a grupą kontrolną.
- **Wdrożenie:** dane o wysyłkach kilka dni, sekwencja 2–4 tygodnie, pomiar 90 dni.

### Pozycja 8. Sprawdzić ręcznie zakup dla pacjentów zalogowanych od wejścia

- **Z danych:** 22 068 sesji zalogowanych od wejścia nigdy nie kończy się zakupem konsultacji, a każdy z 22 289 zakupów powtórnych ma krok logowania. Dane nie rozstrzygają między odczytaniami: (A) wizyty „sprawdzam konto” albo sposób zapisu (logowanie zaczyna nową sesję) albo (B) zepsuta ścieżka zakupu dla zalogowanych. Kilka faktów przemawia za A (`a5_pozyskanie.md`, sekcja 3).
- **Ile warta** (`c_priorytety.txt`, P5): w odczytaniu A 0 zł dla przychodu (ale wtedy cierpi pomiar lejka, pozycja 2). W odczytaniu B scenariusze: około 40 tys. zł rocznie na sesjach, około 36 tys. zł na pacjentach, wysoki scenariusz 89 tys. zł.
- **Po czym poznamy:** test daje odpowiedź od razu. Jeśli ścieżka jest zepsuta, po naprawie sesje zalogowane od wejścia zaczynają kończyć się płatnością.
- **Wdrożenie:** 1 dzień, w pierwszym tygodniu niezależnie od miejsca na liście.

### Pozycja 9. Meta na L4: test dodatkowości w parach województw, z progiem decyzji

- **Z danych:** wynik kampanii zależy od reguły źródła: +27,8 tys. zł według przyjętej reguły i −28,7 tys. zł według sesji płatności po 90 dniach, w 332 dniach działania (+30,6 i −31,6 tys. zł na pełny rok). Dane nie rozstrzygają, ilu jej pacjentów przyszłoby i bez niej.
- **Naprawić albo wyłączyć** (`c_priorytety.txt`, P4 i P11):
  - naprawić zwroty: pozycja 5, w tej samej kampanii;
  - wyłączyć: od −30,6 tys. zł (wszyscy pacjenci dodatkowi, horyzont 90 dni) albo −32,9 tys. zł (180 dni) do +179,6 tys. zł (żaden) na pełny rok.
- **Próg decyzji, ustalony przed testem:** według przyjętej reguły wyłączenie traci pieniądze tylko wtedy, gdy ponad około 85% pacjentów kampanii jest dodatkowych: 85,4% w horyzoncie 90 dni i 84,5% w horyzoncie 180 dni (`c_priorytety.txt`, P11). Według sesji płatności wyłączenie zyskuje zawsze.
  - **Próg po naprawie zwrotów** (dopisek Kuby 2026-10-21; `d_wynik.txt`, punkt 3a): 70,0% (90 dni) i 69,4% (180 dni) w wariancie A, 78,7% i 77,9% w wariancie B. Po naprawie kampania zarabia więcej na każdym pacjencie, więc opłaca się przy niższej dodatkowości. W tempie ostatniego półrocza próg dziś rośnie do 89,9% (`d_kampanie.txt`, punkt 3).
  - **W liczbie pacjentów próg prawie nie zależy od reguły źródła:** wyłączenie opłaca się, jeśli po nim ubędzie mniej niż około 4 320 nowych pacjentów w 332 dniach działania kampanii w okresie 2 (dziś, horyzont 90 dni; według sesji płatności około 4 360) albo 3 540 (po naprawie zwrotów A). Reguła zmienia głównie to, ilu pacjentów przypisujemy kampanii.
- **Czego ten test nie rozstrzygnie** (dopisek Kuby 2026-10-21; `d_wynik.txt`, punkt 3c; testy pozorne na danych okresu 2, czyli ocena orientacyjna przy założeniach modelu). Test w 8 parach województw przez 4–6 tygodni nie da mocy potrzebnej do odróżnienia wyniku od progu. W połowie kraju kampania przypisuje około 55,7 nowego pacjenta tygodniowo (tempo III kwartału 2026, przyjęta reguła), a losowy rozrzut liczby nowych pacjentów w województwach jest duży. Błąd oszacowania udziału dodatkowych wynosi 24,4 punktu procentowego po 4 tygodniach i 20,1 po 6, a najmniejszy wykrywalny efekt to 68 i 56 punktów. Test nie odróżni więc ani 100% od 85%, ani 85% od 70%: gdy naprawdę wszyscy pacjenci są dodatkowi, orientacyjnie co czwarty test (23–27%) pokaże wynik poniżej progu. Dłuższy test wymaga osobnego przeliczenia, bo szum okresu odniesienia nie maleje z długością testu. Rozrzut jest prawie czysto losowy, więc sam dobór par prawdopodobnie nie wystarczy. Test może za to wykryć dużą różnicę, na przykład gdy większość pacjentów przyszłaby i bez kampanii. Pary i sposób liczenia ustalamy przed testem, na danych sprzed testu.
- **Reguła na wynik niejednoznaczny, ustalona z góry:** decyduje oszacowanie punktowe. Poniżej progu wyłączamy, powyżej zostawiamy. To świadomie przyjęta reguła decyzji przy dużej niepewności, a nie rozstrzygnięcie statystyczne. Obie decyzje są odwracalne, a pomiar warto powtórzyć w innym sezonie. Inne warianty (bez zmian, gdy przedział obejmuje próg; połowa budżetu; przedłużanie testu z punktami kontrolnymi co 2 tygodnie; decyzja według oczekiwanej marży, która wymaga osobnego modelu) są w `d_wynik.txt`, 3e.
- **Projekt testu:**
  - na 4–6 tygodni wyłączyć kampanię w połowie województw, łącząc je w pary podobne wielkością i trendem i losując w parach. Udział nowych kampanii jest podobny we wszystkich województwach (26,2–31,5% nowych pacjentów okresu 2; `d_retencja.txt`, punkt 5), co ułatwia dobór par;
  - wskaźnik główny: wszyscy nowi pacjenci i marża w województwie, a nie pacjenci przypisani Meta;
  - budżetu z wyłączonych województw nie przesuwać;
  - przy okazji mierzyć poranne opóźnienia u internisty (pozycja 6).
  - **Ryzyko:** obsada lekarzy jest wspólna dla całego kraju. Wyłączenie zmniejsza obciążenie internistów, więc w województwach kontrolnych może przybyć wolnych terminów, zakupów i powrotów. Zawyża to spadek (więcej „dodatkowych”), a efekt w retencji przenosi się na województwa kontrolne. Do tego województwo konta to nie miejsce wyświetlenia reklamy, więc część reklam przecieka między województwami.
  - **Koszt testu**, jeśli wszyscy pacjenci są dodatkowi (przyjęta reguła): najwyżej około 1,1–1,2 tys. zł utraconej marży przy 4 tygodniach i 1,6–1,8 tys. zł przy 6 tygodniach; po naprawie zwrotów A 2,5 i 3,8 tys. zł (tempo III kwartału 2026). Według sesji płatności test daje zysk (`d_wynik.txt`, punkt 3d). Uzupełnienie: badanie przyrostu konwersji w panelu Meta.
- **Po czym poznamy:** spadek wszystkich nowych pacjentów w województwach bez reklamy wobec par, w liczbie pacjentów i jako udział pacjentów przypisanych Meta; decyzja według reguły wyżej.
- **Wdrożenie:** tydzień przygotowania i 4–6 tygodni testu. Test rusza w drugim tygodniu, równolegle z diagnozą poranka (pozycja 6), bo oba można prowadzić w tych samych województwach. Wynik może się nie przenieść z jesieni na lato.

### Pozycja 10. Cennik specjalistów i warunki TelemediGO u specjalistów

- **Z danych:**
  - po cenie katalogowej wizyta zostawia ponad koszt lekarza tylko 9 zł (dermatolog, kardiolog, neurolog, urolog: 109 zł) albo 19 zł (endokrynolog, ginekolog: 119 zł);
  - pediatra (95 zł) i psycholog (99 zł) mają cenę niższą niż koszt lekarza 100 zł (przy założeniu 33);
  - po zniżce TelemediGO 20% cena jest niższa niż koszt lekarza u wszystkich specjalistów poza psychiatrą. W okresie 2 te wizyty przyniosły 14,7 tys. zł straty na 1 512 zamówieniach (punkt 2.3, `c_priorytety.txt`, P6 i P14).
  - To wspólna przyczyna strat w TelemediGO u specjalistów i w kampanii na specjalistów (pozycja 4).
- **Ile warta:**
  - **warunki TelemediGO:** scenariusze 14,7 / 18,9 / 31,4 tys. zł rocznie (znikają wszystkie te wizyty / tylko te ze stratą / wszystkie zostają po cenie katalogowej). 31,4 tys. zł to scenariusz, a nie górna granica: przy osobnej reakcji przy każdym zamówieniu wynik mieści się między 10,9 a 35,2 tys. zł. Wszystkie pomijają zmianę sprzedaży członkostw. Założenie planistyczne (bez osobnego rachunku): w pierwszym roku efekt to około połowa, bo obecni członkowie mają stare warunki do końca ważności;
  - **cennik:** każde 10 zł podwyżki przy tej samej liczbie wizyt to do 73,6 tys. zł rocznie (7 363 opłacone wizyty w okresie 2), a przy utrzymaniu zniżki TelemediGO 20% na 1 425 z nich 70,8 tys. zł. To górna granica, bo nie znamy reakcji pacjentów na cenę.
- **Warianty:** zniżka u specjalistów ustawiona tak, żeby cena nie spadała poniżej kosztu lekarza (najwyżej około 8% przy 109 zł, bez zniżki u pediatry i psychologa); test dwóch cen dla nowych pacjentów przez 4 tygodnie, mierzony marżą na sesję, a nie odsetkiem kupujących.
- **Po czym poznamy:** marża wizyt u specjalistów (z członkami i bez) nieujemna; sprzedaż TelemediGO nie spada bardziej niż ustalony z góry próg.
- **Wdrożenie:** zmiana regulaminu i kasy 1–2 tygodnie; test cen 4 tygodnie.

### Pozycja 11. Sprawdzić stratę między kliknięciem reklamy a sesją w Meta i TikToku

- **Z danych:** na kliknięcie przypada 0,92–0,93 sesji w Google Ads, 0,79–0,82 w Meta i 0,72 w TikToku, stale w każdym kwartale (`a5_pozyskanie.md`, sekcja 5).
- **Ile warta:** 0 zł, jeśli plik wydatków liczy wszystkie kliknięcia (także te, które nie prowadzą na stronę). Jeśli ludzie porzucają stronę, zanim się załaduje, i da się to odzyskać: do 52 tys. zł rocznie (górna granica, `c_priorytety.txt`, P9). Po wstrzymaniu TikToka mniej. Realnie raczej ułamek, bo porzucający są mniej zdecydowani.
- **Po czym poznamy:** w panelach porównać kliknięcia w link i wyświetlenia strony docelowej z sesjami, dzień po dniu; czas ładowania w przeglądarkach wbudowanych. Wynik zmienia ocenę pozycji 3 i 9.
- **Wdrożenie:** 1–2 dni, w pierwszym tygodniu.

### Pozycja 12. Test TelemediGO z losowym, bezpłatnym dostępem do zniżek

- **Z danych:** punkt 2.4. Nie wiemy, czy TelemediGO podnosi powroty, czy tylko przyciąga pacjentów, którzy i tak wracają. Zniżki przewyższają opłatę średnio o 15,6 zł na członkostwo, więc program opłaca się tylko wtedy, gdy dokłada wizyt.
- **Ile warta:** decyduje, czy program promować (sprzedaż, przypomnienie o odnowieniu; dziś odnawia około 5%), czy przebudować razem z pozycją 10. Dodatkowy koszt testu to około 3,3–12,2 tys. zł zniżek (`c_priorytety.txt`, P10).
- **Zastrzeżenie:** darmowy dostęp mierzy wpływ zniżki, a nie opłacalność oferty za 89 zł. Losowanie samej oferty przy kasie mierzyłoby decyzję biznesową, ale przy 4,5% kupujących potrzebuje ponad 4 lat pozyskania. Wskaźnikiem głównym jest marża na pacjenta.
- **Po czym poznamy:** różnica powrotu w 90 dniach i marży między grupą z dostępem a grupą bez niego.
- **Wdrożenie:** 2–8 tygodni na losowe przydzielenie (487–1 823 pacjentów na grupę, czyli do około 1,8 miesiąca pozyskania), potem 90 dni obserwacji. Liczebność wyznaczyliśmy dla różnicy powrotu; przed startem trzeba ustalić najmniejszą istotną biznesowo zmianę marży i sprawdzić, jakiej próby wymaga.

### Czego proponujemy teraz nie robić (z danych)

- **Zgoda marketingowa pacjentów nowych kampanii:** w najlepszym odczytaniu 1,9 tys. zł rocznie (`a5_ekonomia.md`, sekcja 7).
- **Przeglądarki wbudowane w aplikacje w kampaniach do nowych odbiorców:** w tym rachunku 0 zł, bo w tej samej kampanii nie wykryliśmy niższej konwersji niż w zwykłych (także w kampanii Meta „lekarz online”: różnica −0,15 punktu procentowego, od −0,51 do +0,21, 29 330 sesji w przeglądarkach wbudowanych w dwóch latach; `d_kampanie.txt`, punkt 1). Porównanie jest obserwacyjne, więc nie rozdziela wpływu przeglądarki od cech użytkowników i nie uzasadnia osobnej wyceny naprawy. **Nie uogólniamy tego na resztę ruchu** (dopisek Kuby 2026-10-21): w ruchu osób, które znają już stronę, sesje w przeglądarkach w aplikacjach płacą w okresie 2 rzadziej niż zwykłe w tej samej kampanii (remarketing Meta o 12,2 punktu, 1 772 sesje w przeglądarkach wbudowanych; Google Ads na markę o 5,1 punktu, 2 357 sesji; wejścia bezpośrednie o 4,4 punktu, 4 261 sesji). Dane nie rozstrzygają, czy winna jest przeglądarka, czy to, kto z niej korzysta (niewiadoma 19).
- **Mocniejsza sprzedaż i odnowienia TelemediGO:** dopiero po teście z pozycji 12.
- **Przesuwanie uwolnionego budżetu do innych kampanii bez testu** (zasada budżetu).

---

## 4. Czego nie da się rozstrzygnąć (z testem albo brakującymi danymi)

| # | Czego nie wiemy | Dlaczego to ważne | Test albo brakujące dane |
|---|---|---|---|
| 1 | Czy pacjenci nowych kampanii na L4 są dodatkowi | od tego zależy decyzja o Meta na L4: od −30,6 tys. zł (90 dni) albo −32,9 tys. zł (180 dni) do +179,6 tys. zł na pełny rok (pozycja 9; próg decyzji około 85% pacjentów dodatkowych: 85,4% w 90 dniach i 84,5% w 180 dniach) | wyłączenie kampanii w losowej połowie województw na 4–6 tygodni; badanie przyrostu w panelach Meta i TikToka. Taki test nie odróżni wyniku od progu (błąd 20–24 punktów procentowych), więc rozpozna tylko niską dodatkowość, a przy wyniku niejednoznacznym decyduje reguła ustalona z góry (pozycja 9) |
| 2 | Która reguła źródła jest bliższa prawdy dla kampanii bez kodu (Google Ads ogólne, Meta lekarz online) | znak wyniku tych kampanii zależy od reguły | ten sam test z grupą kontrolną bez reklamy |
| 3 | Powód zwrotów po wizycie L4 w nowych kampaniach (17,4% wobec 5,3%) | po wstrzymaniu TikToka dotyczy tylko Meta: od niego zależy, czy naprawa jest bliżej górnego, czy dolnego wariantu z pozycji 5, czyli 18,1–46,5 tys. zł według przyjętej reguły i 10,7–26,7 tys. zł według sesji płatności na pełny rok | powód zwrotu, decyzja lekarza (czy L4 wystawiono), treść reklam |
| 4 | Skąd poranne opóźnienia u internistów (głównie od 5:00 do 12:59, już przy wizytach z najwcześniejszym terminem dnia, bez widocznego narastania w ciągu poranka) i czy obniżają powroty | scenariusz od 0 do 65 tys. zł rocznie; luty 2026 nie pasuje do prostej hipotezy | grafiki i obsada poranna przed i po 3.11.2025, obciążenie lekarzy pacjentami spoza B2C, koszt obsady; test z dodatkową poranną obsadą w losowe dni |
| 5 | Sesje zalogowane od wejścia: wizyty „sprawdzam konto” czy zepsuta ścieżka | 0 albo około 36–40 tys. zł rocznie (wysoki scenariusz 89 tys. zł) | ręczny test zakupu po zalogowaniu; logi błędów; znacznik „zalogowany na wejściu” w analityce |
| 6 | Przyczyna awarii zakładania konta w Safari na iOS od 17.03.2026 | potrzebna do naprawy (pozycja 1) | lista zmian w produkcie z 16–17.03.2026, logi rejestracji według przeglądarki, powtórzenie na iPhonie |
| 7 | Czy utraceni w Safari na iOS kupili na innym urządzeniu | zmienia wartość pozycji 1 | powiązanie urządzeń po adresie e-mail albo numerze telefonu przy próbie rejestracji |
| 8 | Czy TelemediGO podnosi powroty, czy tylko przyciąga pacjentów, którzy i tak wracają | decyduje o tym, czy program promować | losowy, bezpłatny dostęp do zniżek (pozycja 12) |
| 9 | Czy newsletter i SMS wywołują zakup | to kanał, którego dodatkowy wpływ warto przetestować (około 14% obserwowanych pierwszych powrotów idzie po wejściu z niego); widać kliknięcia, nie wysyłki; wejść na 1 000 pacjentów całej narastającej bazy jest coraz mniej (z 56–108 do 24–52 miesięcznie) | liczba wysyłek; losowa grupa kontrolna bez wysyłki |
| 10 | Wartość remarketingu porzuconego koszyka | przyjęta reguła z definicji przypisuje mu mało pacjentów | grupa kontrolna, której remarketing się nie wyświetla |
| 11 | Sezon a wydatki na kampanie | wzrostu od X 2024 do I 2025 nie da się rozdzielić; dwa lata to jedna zima i jedno lato w roku | zmiana budżetu w części kraju (grupa kontrolna według województw) |
| 12 | Strata między kliknięciem reklamy a sesją w Meta i TikToku | od 0 do 52 tys. zł rocznie | panele reklamowe, logi serwera, czas ładowania strony w przeglądarkach wbudowanych |
| 13 | Prawdziwa stawka lekarza u pediatry (przyjęte 100 zł) | przy 100 zł pediatra przynosi stratę nawet bez zniżki; przy 25 zł marża na pacjenta w 90 dniach rośnie o 3,7–4,8 zł | stawka z umów z lekarzami |
| 14 | Koszt lekarza za wizyty testowe (51 775 zł według zasady z zadania, łącznie w obu okresach; 37 950 zł w okresie 2) | wynik biznesu | informacja, czy lekarze dostali wynagrodzenie za testy; przegląd testów w punkcie D |
| 15 | Warunki umowy z rankingiem lekarzy | prowizja 30,8 tys. zł według naszej reguły albo 14,9 tys. zł według kodu | umowa z rankingiem |
| 16 | Pełna długoterminowa marża rocznika okresu 2 | rachunek kampanii w 90 i 180 dniach jej nie obejmuje; zaniża wartość kampanii z powracającymi pacjentami | czas; najstarsze kohorty pozwalają już częściowo ją ocenić (5 137 pacjentów okresu 2 ma pełne 270 dni obserwacji, `c_priorytety.txt`, P16) |
| 17 | Reakcja pacjentów na cenę u specjalistów | od niej zależy, ile da zmiana cennika (do 73,6 tys. zł za 10 zł podwyżki) | test dwóch cen dla nowych pacjentów przez 4 tygodnie |
| 18 | Zasady zwrotów przy odmowie L4 i ryzyko prawne reklam L4 | górny wariant pozycji 5 może wymagać zmiany zasad zwrotów | regulamin, opinia prawna, treść reklam |
| 19 | Czy sesje w przeglądarkach wbudowanych w aplikacje płacą rzadziej w ruchu osób, które znają już stronę, przez samą przeglądarkę, czy przez to, kto z niej korzysta (dodane 2026-10-21) | w remarketingu Meta, Google Ads na markę i wejściach bezpośrednich płacą w okresie 2 rzadziej niż zwykłe o 4,4–12,2 punktu procentowego; jeśli winna jest przeglądarka, da się to naprawić na stronie | czas ładowania i błędy strony w przeglądarkach w aplikacjach; ręczny zakup w Instagramie, Facebooku i TikToku; test linku, który otwiera zwykłą przeglądarkę |
| 20 | Dlaczego 11 482 konta (21,9% z 52 400) nie mają żadnego zakupu i czy da się je odzyskać (dodane 2026-10-21) | każde z tych kont wybrało usługę i przeszło krok konta, a 37,1% z nich zaczęło płatność; 58,1% z 11 482 ma zgodę marketingową (stan na 30.09.2026), ale w danych nie ma ani jednego ich wejścia z newslettera albo SMS-a | dane o wysyłkach do tych kont; sekwencja wiadomości do kont bez zakupu z losową grupą kontrolną; bez wyceny przed testem |
| 21 | Jak liczba zamówień z Meta na L4 reaguje na wysokość kodu rabatowego (dziś 20 zł) (dodane 2026-10-21) | kod to 62,8 tys. zł zniżki efektywnej na pełny rok; próg rachunku: rezygnacja z niego opłaca się, jeśli ubędzie mniej niż 33,7% zamówień z kodem (przy przejściu na START10 mniej niż 20,2%) | losowy podział ruchu Meta na L4 na kod 20 zł, 10 zł i brak kodu, mierzony marżą na kliknięcie (pozycja 5) |
| 22 | Dlaczego od 22.05.2026 spada konwersja Google Ads na markę (dodane 2026-10-21) | sesja do płatności u osób, które jeszcze nie kupowały: 17,8% (5 152 sesje, 22.05–30.09.2026) wobec 21,2% (21 186 sesji, 1.10.2024–21.05.2026), czyli około 28,5–39,6 zamówienia mniej na 30 dni zależnie od okna porównania; to nie Safari na iOS ani zmiana struktury ruchu; rok wcześniej w tym samym sezonie spadek był mniejszy i nieistotny (−1,3 punktu); koszt kliknięcia marki rośnie (pozycja 2) | lista zmian w kampanii i na stronie z maja 2026; hasła wyszukiwania i reklamy konkurencji na markę w panelu Google Ads |

---

## 5. Konsylium

Runda odbyła się 2026-10-20 po zgodzie Kuby, na briefie z dopisanym kandydatem „pomiar” i faktem o marży w III kwartale. Odpowiedziało 9 z 9 członków, koszt 0,49 USD. Wynik: `notatki/konsylium/c_priorytety/synteza.md`. Zmiany, które wniósł do listy, są w sekcji 3 („Co się zmieniło”). Zarzuty sprawdzalne w danych sprawdziliśmy kodem (`c_priorytety.txt`, P11–P15).

## 6. Recenzja Codeksa (model Sol)

Wynik i nasze decyzje: sekcja 8.

## 7. Propozycje wpisów do wspólnych notatek (scalę po przeglądzie Kuby)

### Do `ZALOZENIA.md` (nowe punkty od 47, bo 44–46 zajęło narzędzie; sekcja „TelemediGO i priorytety, punkt C”)

47. **Zniżka TelemediGO w złotych** = cena katalogowa − zapłata na zamówieniu ze zniżką TelemediGO. **Zniżka efektywna** liczy tylko wizyty odbyte i nieodebrane, bo przy anulowanej i zwróconej wizycie pacjent dostaje całą zapłatę z powrotem. Zniżkę przypisujemy członkostwu, w którego ważności (od chwili zakupu do `valid_until` włącznie) padło zamówienie.
48. **Typ zakupu TelemediGO:** przy kasie z pierwszym zamówieniem pacjenta, przy kasie z kolejnym zamówieniem, osobno (sesja z kampanii `crm_go_upsell`). Okres zakupu = dzień zakupu członkostwa. **Odsetek kupujących przy kasie** liczymy na zamówieniach pacjentów, którzy w chwili zamówienia nie mieli ważnego członkostwa.
49. **Opłata wobec zniżek** to rachunek przy założeniu, że wizyty ze zniżką odbyłyby się i bez TelemediGO. Nie jest to wynik programu, bo nie wiemy, ile wizyt członkostwo dokłada.
50. **Kupujący TelemediGO a podobni pacjenci:** dokładne dopasowanie w warstwach (okres, kanał pozyskania według przyjętej reguły, pierwsza usługa, miesiąc kohorty), wynik ważony liczbą kupujących. Różnica to suma wpływu zniżki i samoselekcji, nie efekt programu.
51. **Wartość pozycji listy priorytetów** = zmiana marży na rok, z okresem 2 jako rokiem bazowym, przy kampaniach w horyzoncie 90 i 180 dni od pozyskania i według obu reguł źródła. Kwot z różnych pozycji nie sumujemy (różne horyzonty, nakładanie się). Czas wdrożenia to nasz szacunek.
52. **Utracony pierwszy zakup w Safari na iOS = utracony nowy pacjent** z marżą nowych pacjentów z pierwszą płatnością w Safari na iOS w okresie 2, bez kosztu pozyskania (wejście już opłacone).

### Do `ZNALEZISKA.md` (sekcja „C — TelemediGO”)

- Wzrost sprzedaży TelemediGO o 40,3% to więcej zamówień i pełny rok sprzedaży w newsletterze (w okresie 1 23 dni). Odsetek nowych pacjentów, którzy kupują przy pierwszym zamówieniu, spada z 5,58% do 4,41%, w całości przez pacjentów nowych kampanii na L4 (1,5%).
- Członkostwa z okresu 1 dostały 104,57 zł zniżki efektywnej przy opłacie 89 zł. Kupujący przy kolejnym zamówieniu dostają 136,36 zł.
- Po zniżce 20% cena wizyty jest niższa niż koszt lekarza u wszystkich specjalistów poza psychiatrą. W okresie 2 to −14,7 tys. zł marży na 1 512 zamówieniach.
- Przy koszcie pediatry 100 zł (założenie 33) wizyta u pediatry przynosi stratę także bez zniżki (cena 95 zł).
- Odnawia około 5% członków. W danych nie widać przypomnienia o wygaśnięciu.
- Kupujący TelemediGO wracają częściej niż podobni pacjenci (+10,1 i +14,6 punktu procentowego w 90 dniach), ale po wygaśnięciu przewaga w proporcji zostaje (iloraz 1,77). Dane nie rozdzielają wpływu zniżki od samoselekcji.

### Do `PLAN.md`, `PRZEKAZANIE.md`, `analiza/README.md`

- Status C, nowe skrypty i wyniki — wpisane od razu (fakty o plikach, nie wnioski).
- Do narzędzia (punkt B): sekcja „czy to wzrost” z dwiema odpowiedziami i zastrzeżeniami; lista priorytetów z tabelą przeglądu i kartami pozycji; lista niewiadomych; TelemediGO z zestawień `c_telemedigo_miesiace*.csv` — po przyjęciu przez Kubę.

## 8. Recenzja Codeksa (model Sol) — wynik

Pełne podsumowanie: `notatki/recenzje/c_codex.md`. Polecenie i odpowiedź: `c_codex_prompt.md`, `c_codex_odpowiedz.md`.

- **Wszystkie liczby główne Codex przeliczył niezależnie, własnym kodem, i zgadzają się co do sztuki i co do złotówki:** zakupy TelemediGO według typu, odsetki kupujących, zniżki członkostw z okresu 1, marża wizyt ze zniżką u specjalistów, wynik biznesu, powroty z nowymi kampaniami i bez nich, wartości P1 i P7. Uwag krytycznych nie ma.
- **Osiem uwag, wszystkie przyjęte i wprowadzone:**
  - liczebność próby testu była zaniżona (wzór ze wspólną wariancją); teraz 136, 487 i 1 823 pacjentów na grupę zamiast 105, 422 i 1 687;
  - „+8,1%” to tylko odjęcie marży powtórnych konsultacji poprzedniego rocznika; po odjęciu także jego opłat za TelemediGO wychodzi +3,1%; oba nazwane jako rozbicie księgowe;
  - grupa porównawcza w kontroli 2 obejmuje 15 późniejszych kupujących; nowa nazwa i wariant bez nich (+0,49 zamiast +0,40);
  - kontrola 1 nie rozdziela wpływu ceny od samoselekcji; nowe brzmienie „zgodny z kilkoma wyjaśnieniami” i wariant ze wszystkimi kupującymi;
  - wartości warunków TelemediGO to scenariusze, nie granice; dodane 18,9 tys. zł i zakres 10,9–35,2 tys. zł;
  - porównanie opłat ze zniżkami wymaga jawnego założenia o tych samych wizytach; dopisane w raporcie i w szkicu;
  - koszt testu: dodatkowy, a nie nominalny (6,71 zł zamiast 6,76 zł na pacjenta);
  - sesje zalogowane: scenariusze, wariant na pacjentach (35,5 tys. zł), 90,5% to nie górna granica.
- **Co się zmieniło w liczbach szkicu:** koszt testu 3,3–12,2 tys. zł zamiast 2,9–11,4 tys. zł; liczebność 487–1 823 zamiast 422–1 687; wynik bez poprzedniego rocznika +3,1% obok +8,1%. Kierunek żadnego wniosku się nie zmienił.

## 9. Dopiski i decyzje Kuby

### 2026-10-20, przegląd szkicu

**Decyzja:** szkic dobry, kierunek przyjęty, z czterema dopiskami (pełne brzmienie: `DECYZJE.md`, wpis „przegląd szkicu punktu C”):
1. marża po kwartałach rok do roku z wydatkami obok; jeśli potwierdzi się niższa marża w VII–IX 2026 przy ponad dwa razy wyższych wydatkach, to zdanie zamyka odpowiedź — **potwierdzone** (III kwartał: −6,8%, wydatki ×2,08; sekcja 1);
2. nowa pozycja „naprawić pomiar” zaraz po Safari — **wprowadzone** (pozycja 2);
3. poranna przepustowość internistów przed testem zalogowanych i testem Meta — **wprowadzone** (pozycja 6, przed 8 i 9);
4. runda konsylium z kandydatem „pomiar” i faktem o marży w ostatnim kwartale — **zrobione** (sekcja 5, synteza w `notatki/konsylium/c_priorytety/synteza.md`).

### 2026-10-20, akceptacja ostatecznej listy

**Decyzja Kuby:** ostateczna lista przyjęta, z pięcioma poprawkami spójności:
1. niewiadoma 1 z kwotami na pełny rok, jak w pozycji 9 — **wprowadzone**;
2. niewiadoma 3 z kwotami samej Meta, jak w pozycji 5 — **wprowadzone**;
3. pozycja 6: przebieg porannych opóźnień miesiąc po miesiącu — **sprawdzone i poprawione** (w listopadzie 2025 opóźnienia dopiero zaczynają rosnąć; około połowa od lutego 2026);
4. numeracja w sekcji 1c — **poprawiona**;
5. opis punktu C w `PLAN.md` i `PRZEKAZANIE.md` — **zaktualizowany**.

Potem przeniesienie do narzędzia (odpowiedź bez znacznika „wstępne”, priorytety, niewiadome) w nowej sesji, bo sesja B jest zamknięta. Równolegle weryfikacja liczb Codeksem (model Astra) i README dla Telemedi. Zatrzymanie u Kuby z narzędziem przed próbną publikacją.
