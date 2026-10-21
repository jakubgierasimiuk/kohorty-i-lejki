# Teksty strony narzędzia — wszystkie zakładki, tak jak widzi je czytelnik

Wygenerowane 2026-10-21 19:48 skryptem `analiza/b2_teksty_strony.py` ze strony w `narzedzie/` (stan repozytorium efdd8e2), otwartej w przeglądarce bez okna (Microsoft Edge), szerokość 1366 px. Każda zakładka przy ustawieniach domyślnych, bez klikania. Tabele dłuższe niż 40 wierszy są skrócone do 15 pierwszych i 5 ostatnich wierszy. Rozwijane sekcje są rozwinięte. Wykresy opisane nazwami serii. W komórkach tabel `<br>` oddziela linie, które strona pokazuje jedna pod drugą (zwykle: wartość w okresie B, pod spodem okres A i zmiana). Odnośniki do innych zakładek są oznaczone strzałką albo wypisane po „Zobacz w danych”.

**Nagłówek strony:** B2C: czy to wzrost? — Narzędzie do zadania rekrutacyjnego na stanowisko Head of B2C. Kohorty, lejki, zdarzenia i jakość danych w jednym miejscu.

**Uwaga na każdej stronie:** Dane są syntetyczne, wygenerowane na potrzeby zadania. Nie opisują prawdziwych pacjentów ani wyników firmy.

**Zakładki:** Czy to wzrost (`#wzrost`), Kohorty (`#kohorty`), Lejek (`#lejek`), Po zakupie (`#po-zakupie`), Zdarzenia (`#zdarzenia`), Wynik biznesu (`#wynik`), Jakość danych (`#jakosc`), Priorytety (`#priorytety`), Czego nie wiemy (`#niewiadome`)

# Zakładka 1: Czy to wzrost (`#wzrost`)

## Czy to, co widać na dashboardzie, jest wzrostem?

Wzrost to dwie rzeczy naraz: więcej pacjentów i lepsza retencja. Sprawdzamy oba warunki osobno, na danych oczyszczonych, porównując okres 2 (ostatnie 12 miesięcy) z okresem 1 (poprzednie 12 miesięcy).

Nie. Pacjentów jest więcej, ale wracają rzadziej, więc z dwóch warunków wzrostu spełniony jest tylko jeden.

To nie jest wzrost w rozumieniu z zadania (więcej pacjentów i lepsza retencja naraz), bo z dwóch warunków spełniony jest tylko pierwszy. Pacjentów z pierwszym zakupem jest o 52,1% więcej (24 687 wobec 16 231), ale retencja jest gorsza: powrót w 90 dniach 17,4% wobec 23,9% na tych samych dniach kalendarzowych, a marża na pacjenta w 90 dniach 58,3 zł wobec 66,6 zł.

Obecność pacjentów dwóch nowych kampanii na L4 odpowiada opisowo za około 46–71% spadku powrotu, zależnie od reguły źródła, ale bez nich retencja też spada (do 22,0% według przyjętej reguły albo 20,4% według sesji płatności), a nowych pacjentów spoza tych kampanii przybyło tylko o 7,3–20,1%.

### Więcej pacjentów: tak

+52,1%

*16 231 → 24 687 nowych pacjentów*

- Nowych pacjentów jest 24 687 w okresie 2 wobec 16 231 w okresie 1, czyli +52,1%.
- Bez pacjentów dwóch nowych kampanii na L4 jest ich 17 419 według przyjętej reguły (+7,3%) albo 19 500 według sesji płatności (+20,1%).
- Z kanałów bezpłatnych (wejścia bezpośrednie, bezpłatne wyszukiwanie, program poleceń) przybyło 12,1%: z 7 069 do 7 924.
- Nie wiemy, ilu pacjentów nowych kampanii przyszłoby i bez nich (dodatkowość, pierwsza pozycja w zakładce „Czego nie wiemy”).

### Lepsza retencja: nie

23,9% → 17,4%

*powrót w 90 dniach, 12 867 i 18 924 pacjentów*

| Powrót w ciągu | Okres 1 (X 2024 – IX 2025) | Okres 2 (X 2025 – IX 2026) | Zmiana |
| --- | --- | --- | --- |
| 30 dni | 11,0% (14 984 pacjentów) | 7,8% (22 646 pacjentów) | −3,2 pkt proc. |
| 60 dni | 19,1% (13 941 pacjentów) | 13,7% (20 823 pacjentów) | −5,4 pkt proc. |
| 90 dni | 23,9% (12 867 pacjentów) | 17,4% (18 924 pacjentów) | −6,5 pkt proc. |
| 180 dni | 27,5% (9 125 pacjentów) | 22,2% (12 591 pacjentów) | −5,2 pkt proc. |

- Powrót to kolejne zamówienie, które nie zostało anulowane. Liczymy go na tych samych dniach kalendarzowych i tylko w kohortach z pełnym oknem obserwacji.
- Marża na pacjenta w 90 dniach przed kosztem pozyskania: 58,3 zł wobec 66,6 zł, czyli −8,3 zł.
- Bez pacjentów nowych kampanii retencja też spada. Powrót w 90 dniach wynosi 22,0% według przyjętej reguły (14 031 pacjentów) i 20,4% według sesji płatności (15 414), wobec 23,9%. Marża na pacjenta w 90 dniach 66,0 zł i 63,3 zł, wobec 66,6 zł.
- Pacjenci nowych kampanii wracają w 90 dniach w 4,1% (4 893 pacjentów).
- W jednej grupie spadku nie wykazaliśmy: pacjenci z pierwszym L4 z pozostałych kanałów wracają w 13,9% (2 797 pacjentów) wobec 14,8% (2 639), bez istotnej zmiany. W innych usługach powrót spada także bez pacjentów nowych kampanii: po e-recepcie z 33,4% do 29,9% (3 206 i 3 570 pacjentów), po wizycie u innego specjalisty z 25,2% do 20,6% (2 325 i 2 549).
- Liczba osób, które wróciły w 90 dniach, rośnie: 3 289 wobec 3 076 (+6,9%). Spada odsetek, a nie liczba powracających. Porównanie 90-dniowe obejmuje pierwsze zakupy do 2 lipca każdego roku, a nie pełne roczniki.

### TelemediGO: skąd +40,3% sprzedaży

Wzrost o 709 zakupów (z 1 759 do 2 468, +40,3%) wynika z tego, że jest więcej zamówień, i z pełnego roku sprzedaży w newsletterze. Odsetek pacjentów, którzy kupują TelemediGO, nie rośnie.

| Typ zakupu | Okres 1 | Okres 2 | Zmiana | Udział we wzroście |
| --- | --- | --- | --- | --- |
| Przy kasie z pierwszym zamówieniem pacjenta | 905 | 1 089 | +184 | 26% |
| Przy kasie z kolejnym zamówieniem | 629 | 918 | +289 | 41% |
| Osobno, z newslettera crm_go_upsell | 225 | 461 | +236 | 33% |
| Razem | 1 759 | 2 468 | +709 | 100% |

- Sprzedaż osobna w newsletterze ruszyła 8.09.2025. W okresie 1 działała więc tylko 23 dni, a sprzedała w nich 225 członkostw. W okresie 2 sprzedaje średnio 38 miesięcznie.
- Przy kasie przybywa zakupów, bo jest więcej zamówień, a nie wyższy odsetek kupujących. Przy pierwszym zamówieniu odsetek kupujących spada z 5,58% (16 231 zamówień) do 4,41% (24 687): więcej zamówień dodaje 471 zakupów, a niższy odsetek odejmuje 287. Przy kolejnych zamówieniach odsetek rośnie lekko, z 9,27% (6 784) do 9,86% (9 307).
- Spadek odsetka przy pierwszym zamówieniu to w całości pacjenci nowych kampanii na L4: kupuje u nich 1,5% (7 268 pacjentów). Bez nich odsetek stoi: 5,58% wobec 5,63% (17 419 pacjentów).
- Opłata 89 zł nie pokrywa średniej zniżki. Członkostwa z okresu 1 (1 759, pełne 365 dni) przyniosły 156 551 zł opłat i dostały 183 939 zł zniżki efektywnej, czyli −27 388 zł (−15,57 zł na członkostwo). W okresie 2 przybliżenie to −10,7 zł na członkostwo. To rachunek przy założeniu, że te same wizyty zostałyby kupione bez TelemediGO, a nie strata programu: nie wiemy, ile wizyt członkostwo dokłada.
- Kupujący TelemediGO przy pierwszym zamówieniu wracają w 90 dniach częściej niż podobni pacjenci: 34,7% wobec 20,0% w okresie 2 (858 kupujących). Dane nie mówią, ile z tego to wpływ zniżki, a ile to, że kupują ci, którzy i tak planują wracać. Rozstrzygnie to test z pozycji 12: losowy, bezpłatny dostęp do zniżek.

Zobacz w danych: Priorytety: pozycja 12, test TelemediGO · Priorytety: pozycja 10, warunki TelemediGO u specjalistów · Kohorty: kupujący TelemediGO przy pierwszym zakupie · Lejek: zakupy samego TelemediGO

*Liczby: analiza/c_telemedigo.py → analiza/wyniki/c_telemedigo.txt (1a, 1b, 1e, 1f, 2a, 2b, 4a). Notatka: notatki/c_szkic.md, sekcja 2.*

### Wynik pod koniec okresu

Pod koniec okresu wzrost przestał się przekładać na wynik: w III kwartale 2026 marża była o 6,8% niższa niż rok wcześniej (207,7 tys. zł wobec 222,8 tys. zł), choć wydatki na kampanie były 2,08 raza wyższe (181,6 tys. zł wobec 87,4 tys. zł).

Szacowana skala problemu z zakładaniem konta w Safari na iOS w III kwartale 2026 (około 14–21 tys. zł marży) jest porównywalna ze spadkiem marży tego kwartału (15,1 tys. zł), ale wyniku kwartału bez tego problemu nie ustaliliśmy. To przybliżenie ze średniej straty z 198 dni, a nie pomiar kwartału.

#### Wzrost marży słabnie z kwartału na kwartał, a wydatki na kampanie rosną coraz szybciej.

| Kwartał | Marża | Rok wcześniej | Zmiana marży | Wydatki na kampanie | Rok wcześniej | Wydatki: ile razy więcej |
| --- | --- | --- | --- | --- | --- | --- |
| IV 2025 | 259,4 tys. zł | 151,3 tys. zł | +71,4% | 113,1 tys. zł | 87,3 tys. zł | 1,30 |
| I 2026 | 324,4 tys. zł | 226,9 tys. zł | +43,0% | 170,6 tys. zł | 102,6 tys. zł | 1,66 |
| II 2026 | 256,6 tys. zł | 227,0 tys. zł | +13,0% | 184,4 tys. zł | 90,4 tys. zł | 2,04 |
| III 2026 | 207,7 tys. zł | 222,8 tys. zł | −6,8% | 181,6 tys. zł | 87,4 tys. zł | 2,08 |

- Marża przed kampaniami (przychód po zwrotach + TelemediGO − koszt lekarza) rośnie w III kwartale 2026 o 25,2% (+79,0 tys. zł), ale wydatki na kampanie rosną o 94,1 tys. zł.
- We wrześniu 2025 ruszyła sprzedaż TelemediGO w newsletterze (225 zakupów w 23 dni), co podnosi III kwartał 2025. Bez opłat za TelemediGO marża III kwartału 2026 też jest niższa: −4,9% rok do roku.
- W samych miesiącach: lipiec 2026 73,4 tys. zł wobec 66,8 tys. zł, sierpień 66,3 wobec 67,2 tys. zł, wrzesień 68,0 wobec 88,8 tys. zł. Niższy jest więc kwartał jako całość, a nie każdy miesiąc.

### Najważniejsze zastrzeżenia

1. Dashboard liczy dane na surowo. Zawiera 604 zdublowane zamówienia z 10–24.06.2026, 2 071 zamówień kont testowych i przychód przed zwrotami. Po oczyszczeniu zamówienia rosną o 55,7% (24 716 → 38 491) zamiast 61%, a przychód z konsultacji po zwrotach o 44,8% zamiast 50%. Nowi pacjenci prawie się nie zmieniają (+51,9% na surowo, +52,1% po oczyszczeniu), a TelemediGO wcale (+40,3%).
2. Start od zera. W okresie 1 nie było bazy pacjentów z poprzedniego roku. W okresie 2 pacjenci pozyskani w okresie 1 złożyli 5 289 zamówień powtórnych, które dały 153 tys. zł marży konsultacji. Sumy roczne z definicji faworyzują więc drugi rok.
3. Wynik biznesu rośnie wolniej niż sprzedaż. Marża po koszcie lekarza, kampaniach i prowizji wynosi 828 tys. zł w okresie 1 i 1 048 tys. zł w okresie 2, czyli +26,6%. Po odjęciu marży powtórnych konsultacji pacjentów pozyskanych w okresie 1 to +8,1%, a po odjęciu także ich opłat za TelemediGO (41,5 tys. zł) +3,1%. To rozbicie księgowe, a nie wynik biznesu, który startuje od zera: nie modeluje zmian wydatków ani zachowania pacjentów. Wydatki na kampanie rosną o 77% (z 368 do 650 tys. zł).
4. Struktura pacjentów się zmieniła. Pacjenci nowych kampanii to 29% nowych pacjentów okresu 2 według przyjętej reguły (7 268 z 24 687). Zostawiają 36,3 zł marży w 90 dniach wobec 66,0 zł pozostałych.
5. Obie reguły źródła. Podział spadku powrotu (z 23,9% do 17,4%) na nowe i stare kampanie zależy od reguły. Według przyjętej reguły to 4,6 punktu procentowego nowych kampanii i 2,0 punktu starych (nowe kampanie: około 71% spadku). Według sesji płatności to 3,0 i 3,5 punktu (około 46%). Kierunek jest ten sam w obu, a to rozkład opisowy, nie zmierzony wpływ kampanii.
6. Marża po kwartałach rok do roku. Wzrost marży słabnie z kwartału na kwartał, a wydatki na kampanie rosną coraz szybciej. Tabela i liczby są w karcie „Wynik pod koniec okresu” wyżej.
7. To opis, nie przyczyna. Widzimy spadek obserwowanej retencji, także po wyłączeniu pacjentów nowych kampanii. Nie dowodzi to, że identyczni pacjenci zachowują się gorzej. Rozkład na strukturę i zachowanie nie mówi też, co by się stało bez nowych kampanii. Spadek w starych kampaniach zbiega się z porannymi opóźnieniami u internistów, ale ich nie dowodzi (czwarta pozycja w zakładce „Czego nie wiemy”).

### Dashboard a dane oczyszczone

Dashboard pokazuje +52% pacjentów, +61% zamówień, +50% przychodu i +40% TelemediGO, ale liczy dane na surowo. Po usunięciu duplikatów i zamówień testowych wzrost zamówień wynosi +55,7%, a przychodu +47,7% przed zwrotami i +44,8% po zwrotach.

*Wzrost: okres X 2025 – IX 2026 wobec okresu X 2024 – IX 2025. Pod wzrostem: wartości w obu okresach.*

| Krok | Nowi pacjenci | Zamówienia | Przychód z konsultacji | TelemediGO |
| --- | --- | --- | --- | --- |
| Dashboard (dane surowe) | +51,9%<br>16 251 → 24 689 | +60,7%<br>25 269 → 40 613 | +50,3%<br>2,382 → 3,580 mln zł | +40,3%<br>1 759 → 2 468 |
| Bez duplikatów zamówień | bez zmian | +58,3%<br>25 269 → 40 009 | +48,1%<br>2,382 → 3,529 mln zł | bez zmian |
| Bez duplikatów i bez kont testowych | +52,1%<br>16 231 → 24 687 | +55,7%<br>24 716 → 38 491 | +47,7%<br>2,375 → 3,508 mln zł | bez zmian |
| Do tego przychód po odjęciu zwrotów | bez zmian | bez zmian | +44,8%<br>2,230 → 3,228 mln zł | bez zmian |

### Co dalej

Zobacz w danych: Kohorty: powrót w 90 dniach, nowe kampanie na L4 i pozostałe · Kohorty: powrót bez pacjentów nowych kampanii · Wynik biznesu: marża po kwartałach · Jakość danych: od dashboardu do danych oczyszczonych

Co z tego robimy: lista priorytetów, od najważniejszej pozycji, z wartością w marży. Czego dane nie rozstrzygają i jakim testem to domknąć: czego nie wiemy.

*Liczby: analiza/c_priorytety.py → analiza/wyniki/c_priorytety.txt (W1–W4, P1), analiza/wyniki/a5r_kohorty.txt (180 dni), analiza/wyniki/a5r_struktura.txt (L4 z L4, rozkład spadku), analiza/wyniki/a5e_ekonomia.txt, analiza/wyniki/c_telemedigo.txt. Notatka: notatki/c_szkic.md, sekcja 1.*

# Zakładka 2: Kohorty (`#kohorty`)

## Kohorty dzienne nowych pacjentów

Powrót nowych pacjentów spada w każdym oknie. Okres X 2025 – IX 2026 wobec X 2024 – IX 2025, te same dni kalendarzowe, tylko kohorty z pełnym oknem: w 30 dniach 7,8% (22 646 pacjentów) wobec 11,0% (14 984 pacjentów); w 60 dniach 13,7% (20 823 pacjentów) wobec 19,1% (13 941 pacjentów); w 90 dniach 17,4% (18 924 pacjentów) wobec 23,9% (12 867 pacjentów); w 180 dniach 22,2% (12 591 pacjentów) wobec 27,5% (9 125 pacjentów).

Marża na pacjenta przed kosztem pozyskania (przychód z konsultacji po zwrotach, TelemediGO, minus koszt lekarza): w 90 dniach 58,3 zł wobec 66,6 zł, w 180 dniach 67,7 zł wobec 75,5 zł.

Obecność pacjentów dwóch nowych kampanii na L4 odpowiada opisowo za około 46–71% spadku powrotu w 90 dniach, zależnie od reguły źródła, ale w kampaniach działających w obu latach też jest spadek, którego sprawdzone cechy nie tłumaczą. Dlatego obie reguły są do wyboru w filtrach.

*Filtry (ustawienia domyślne):*
- Reguła źródła: Przyjęta: pierwsze wejście, kod kampanii rozstrzyga (do wyboru: Przyjęta: pierwsze wejście, kod kampanii rozstrzyga / Sesja płatności)
- Źródło (kanał): wszystkie (do wyboru: wszystkie / Google Ads: hasła ogólne / Wyszukiwarka bezpłatna / Meta: pozyskanie / Wejścia bezpośrednie / Google Ads: hasło marki / … (razem 10 opcji))
- Kampania: wszystkie (do wyboru: wszystkie / Google bezpłatnie / Wejścia bezpośrednie / Meta pozyskanie: L4 szybko / Google Ads: marka / Google Ads: lekarz online / … (razem 15 opcji))
- Nowe kampanie na L4: wszystkie (do wyboru: wszystkie / Nowe kampanie na L4 / Pozostałe kampanie i kanały)
- Urządzenie: wszystkie (do wyboru: wszystkie / Telefon / Komputer / Tablet)
- Przeglądarka: wszystkie (do wyboru: wszystkie / Chrome / Safari / Samsung Internet / Instagram (w aplikacji) / Facebook (w aplikacji) / … (razem 10 opcji))
- Pierwsza usługa: wszystkie (do wyboru: wszystkie / Internista: L4 / Internista: e-recepta / Inny specjalista / Internista: konsultacja / Internista: skierowanie / Pediatra / Psychiatra)
- Zniżka: wszystkie (do wyboru: wszystkie / Bez zniżki / Kod L4SZYBKO20 / Kod START10 / Zniżka TelemediGO / Kod TIKTOK25 / Kod RANKING10)
- TelemediGO przy pierwszym zakupie: wszystkie (do wyboru: wszystkie / Bez zakupu TelemediGO przy pierwszym zakupie / Kupił TelemediGO przy pierwszym zakupie)
- Status pierwszego zamówienia: wszystkie (do wyboru: wszystkie / Odbyta / Odbyta, zwrot po wizycie / Anulowana przed wizytą / Pacjent nie odebrał)
- Opóźnienie pierwszej wizyty: wszystkie (do wyboru: wszystkie / Do 5 minut po terminie / Ponad 5 do 15 minut / Brak wizyty (anulowana, nieodebrana) / Ponad 15 do 30 minut / Ponad 30 minut)
- Pora pierwszej wizyty: wszystkie (do wyboru: wszystkie / Wieczór (16–23) / Rano (6–11) / Południe (12–15) / Noc (0–5))
- Podział na serie: Nowe kampanie na L4 (do wyboru: bez podziału / Źródło (kanał) / Kampania / Nowe kampanie na L4 / Urządzenie / Przeglądarka / … (razem 12 opcji))
- Porównanie: Okres 2 wobec okresu 1 (rok do roku) (do wyboru: Okres 2 wobec okresu 1 (rok do roku) / Ostatnie 90 dni wobec poprzednich 90 / Ostatnie 30 dni wobec tych samych dni rok wcześniej / 60 dni przed i po: Godzina bez danych (17.05.2025) / 60 dni przed i po: Start sprzedaży TelemediGO w newsletterze (crm_go_upsell) (8.09.2025) / 60 dni przed i po: Marża na pacjenta w 30 dniach spada stopniami (30.10.2025) / … (razem 17 opcji))
- Okres A: 2024-10-01 – 2025-09-30
- Okres B: 2025-10-01 – 2026-09-30

### Kohorty w podziale

*Okres A: 1.10.2024–30.09.2025. Okres B: 1.10.2025–30.09.2026. Kohorty z pełnym oknem: 30 dni: A 1.10.2024–31.08.2025, B 1.10.2025–31.08.2026; 60 dni: A 1.10.2024–1.08.2025, B 1.10.2025–1.08.2026; 90 dni: A 1.10.2024–2.07.2025, B 1.10.2025–2.07.2026; 180 dni: A 1.10.2024–3.04.2025, B 1.10.2025–3.04.2026.*

*Kohorta to nowi pacjenci z tego samego dnia pierwszego zakupu. Powrót to kolejne zamówienie, które nie zostało anulowane, w ciągu N dni. Marża na pacjenta to przychód z konsultacji po zwrotach i TelemediGO minus koszt lekarza, przed kosztem pozyskania. Liczymy tylko kohorty z pełnym oknem; okres A obcinamy do tej samej długości co dojrzała część okresu B (przy porównaniu rok do roku to te same dni kalendarzowe). W każdej komórce: wartość w okresie B i liczba pacjentów, pod spodem okres A i zmiana.*

| Nowe kampanie na L4 | Nowi pacjenci B (A) | Udział B (A) | Powrót w 30 dniach | Powrót w 60 dniach | Powrót w 90 dniach | Powrót w 180 dniach | Marża na pacjenta, 90 dni | Marża na pacjenta, 180 dni |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wszyscy w filtrze | 24 687<br>A: 16 231 | 100,0%<br>A: 100,0% | 7,8% z 22 646<br>A: 11,0% z 14 984 ▼3,2 | 13,7% z 20 823<br>A: 19,1% z 13 941 ▼5,4 | 17,4% z 18 924<br>A: 23,9% z 12 867 ▼6,5 | 22,2% z 12 591<br>A: 27,5% z 9 125 ▼5,2 | 58,3 zł z 18 924<br>A: 66,6 zł z 12 867 ▼8,3 | 67,7 zł z 12 591<br>A: 75,5 zł z 9 125 ▼7,8 |
| Pozostałe kampanie i kanały | 17 419<br>A: 16 231 | 70,6%<br>A: 100,0% | 10,0% z 16 228<br>A: 11,0% z 14 984 ▼1,0 | 17,5% z 15 164<br>A: 19,1% z 13 941 ▼1,6 | 22,0% z 14 031<br>A: 23,9% z 12 867 ▼1,9 | 26,2% z 10 239<br>A: 27,5% z 9 125 ▼1,3 | 66,0 zł z 14 031<br>A: 66,6 zł z 12 867 ▼0,6 | 74,7 zł z 10 239<br>A: 75,5 zł z 9 125 ▼0,8 |
| Nowe kampanie na L4 | 7 268<br>A: 0 | 29,4%<br>A: 0,0% | 2,4% z 6 418<br>A: — z 0 | 3,6% z 5 659<br>A: — z 0 | 4,1% z 4 893<br>A: — z 0 | 5,0% z 2 352<br>A: — z 0 | 36,3 zł z 4 893<br>A: — z 0 | 37,3 zł z 2 352<br>A: — z 0 |

### Powrót w oknie (90 dni) według dnia pierwszego zakupu, suma z 7 dni kończących się danego dnia

*Filtry (ustawienia domyślne):*
- Miara: Powrót w oknie (do wyboru: Powrót w oknie / Marża na pacjenta w oknie / Nowi pacjenci dziennie / Udział w nowych pacjentach)
- Okno: 90 dni od pierwszego zakupu (do wyboru: 30 dni od pierwszego zakupu / 60 dni od pierwszego zakupu / 90 dni od pierwszego zakupu / 180 dni od pierwszego zakupu)
- Wygładzenie: suma z 7 dni (do wyboru: bez wygładzenia (dzień) / suma z 7 dni / suma z 28 dni)

*Oś pozioma to dzień pierwszego zakupu (dzień kohorty). Szare pola to okresy A i B, pionowe linie to zdarzenia z zakładki Zdarzenia. Powrót i marża kończą się na ostatniej kohorcie z pełnym oknem. Legenda pod kursorem pokazuje wartość i liczbę pacjentów.*

*[Wykres] serie: Wszyscy w filtrze; Pozostałe kampanie i kanały; Nowe kampanie na L4*

### Macierz kohort: powrót według dni od pierwszego zakupu

*Filtry (ustawienia domyślne):*
- Kohorty: dzienne (do wyboru: dzienne / tygodniowe / miesięczne)

*Wiersz to kohorta (nowi pacjenci z tego samego dnia, tygodnia albo miesiąca pierwszego zakupu; domyślnie dzień), kolumna to okno: odsetek pacjentów kohorty, którzy wrócili w ciągu tylu dni. Kohorty dzienne są małe, więc ich wartości skaczą bardziej niż tygodniowe. Kolor: ciemniej znaczy wyżej, skala osobno w każdej kolumnie, od 5. do 95. percentyla wartości. Kropka oznacza kohortę bez pełnego okna. Kolumna „Zdarzenia” podaje numery zdarzeń z osi, które wypadają w tej kohorcie. Te same filtry co wyżej, bez podziału na serie.*

| Kohorta (dzień) | Nowi pacjenci | Zdarzenia | 7 dni | 14 dni | 30 dni | 60 dni | 90 dni | 180 dni |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.10.2024 | 32 |  | 6,3 | 6,3 | 12,5 | 15,6 | 25,0 | 34,4 |
| 2.10.2024 | 28 |  | 3,6 | 7,1 | 7,1 | 17,9 | 32,1 | 32,1 |
| 3.10.2024 | 39 |  | 0,0 | 2,6 | 5,1 | 10,3 | 15,4 | 15,4 |
| 4.10.2024 | 35 |  | 2,9 | 5,7 | 14,3 | 14,3 | 17,1 | 17,1 |
| 5.10.2024 | 39 |  | 5,1 | 10,3 | 12,8 | 17,9 | 23,1 | 25,6 |
| 6.10.2024 | 25 |  | 4,0 | 4,0 | 12,0 | 20,0 | 20,0 | 20,0 |
| 7.10.2024 | 49 |  | 0,0 | 6,1 | 8,2 | 12,2 | 14,3 | 18,4 |
| 8.10.2024 | 42 |  | 0,0 | 4,8 | 11,9 | 19,0 | 31,0 | 35,7 |
| 9.10.2024 | 44 |  | 0,0 | 4,5 | 11,4 | 22,7 | 22,7 | 25,0 |
| 10.10.2024 | 41 |  | 2,4 | 4,9 | 17,1 | 26,8 | 36,6 | 39,0 |
| 11.10.2024 | 42 |  | 2,4 | 9,5 | 14,3 | 16,7 | 21,4 | 23,8 |
| 12.10.2024 | 42 |  | 7,1 | 9,5 | 19,0 | 28,6 | 31,0 | 33,3 |
| 13.10.2024 | 36 |  | 0,0 | 2,8 | 2,8 | 16,7 | 19,4 | 22,2 |
| 14.10.2024 | 42 |  | 4,8 | 9,5 | 16,7 | 23,8 | 28,6 | 31,0 |
| 15.10.2024 | 42 |  | 4,8 | 7,1 | 14,3 | 28,6 | 33,3 | 35,7 |
| … pominięto 710 wierszy, tabela ma ich 730 … |  |  |  |  |  |  |  |  |
| 26.09.2026 | 73 |  | · | · | · | · | · | · |
| 27.09.2026 | 58 |  | · | · | · | · | · | · |
| 28.09.2026 | 92 |  | · | · | · | · | · | · |
| 29.09.2026 | 86 |  | · | · | · | · | · | · |
| 30.09.2026 | 67 |  | · | · | · | · | · | · |

### Krzywa powrotu według dnia od pierwszego zakupu: okres A i okres B

*Dla każdego dnia od pierwszego zakupu: odsetek pacjentów, którzy do tego dnia wrócili. Na każdy dzień bierzemy tylko kohorty, które ten dzień już osiągnęły, a okres A obcinamy tak samo jak w tabeli. Legenda pod kursorem pokazuje liczbę pacjentów i poziom B jako odsetek poziomu A.*

*[Wykres] serie: Okres A (1.10.2024–30.09.2025); Okres B (1.10.2025–30.09.2026)*

*Każdy punkt krzywej liczymy z innych pacjentów: dzień N bierze tylko kohorty, które ten dzień już osiągnęły. W okresie B dzień 30 to 22 646 pacjentów, a dzień 180 już tylko 12 591, z najstarszych kohort. Wyższe wartości późnych dni nie znaczą więc, że młodsze kohorty nadrabiają.*

*Jak liczymy: nowy pacjent to konto z pierwszym opłaconym zamówieniem, bez względu na status. Źródło pozyskania według przyjętej reguły (pierwsze wejście pacjenta, także anonimowe sesje jego przeglądarek, a kod kampanii na pierwszym zamówieniu rozstrzyga) albo według sesji płatności. Urządzenie i przeglądarka z sesji płatności. Pierwsza usługa: internista według celu wizyty, pediatra, psychiatra, inny specjalista. Opóźnienie i pora z pierwszej wizyty. Źródło danych: analiza/definicje.py, analiza/a5r_kohorty.py, eksport analiza/b_eksport.py.*

# Zakładka 3: Lejek (`#lejek`)

## Lejek: od wejścia na stronę do płatności

Konwersja sesji do płatności spadła z 16,0% w okresie X 2024 – IX 2025 (154 085 sesji, 24 717 płatności) do 13,7% w okresie X 2025 – IX 2026 (280 625 sesji, 38 490 płatności).

Rachunkowo prawie cały spadek to zmiana ruchu. Udział przeglądarek wbudowanych w aplikacje Instagram, Facebook i TikTok wzrósł z 10,7% do 35,6% sesji. Sama zmiana struktury ruchu według przeglądarki daje −3,00 punktu procentowego, a zmiana konwersji w obrębie przeglądarek +0,67 punktu procentowego.

To jednak nie jest tylko „inny ruch”. Dwie rzeczy trzeba naprawić na stronie:

#### Safari na iPhone'ach i iPadach: od 17.03.2026 gwałtownie spada skuteczność zakładania nowego konta

Konta dalej powstają, ale rzadziej. Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spadł z 66,2% w 60 dniach przed awarią (16.01.2026–16.03.2026, 1 763 sesje z wyborem terminu) do 45,1% w 60 dniach po niej (17.03.2026–15.05.2026, 1 553 sesje). Pozostałe przeglądarki w tych samych dniach: 64,8% i 63,4%. Szacunek: 628–695 utraconych pierwszych zamówień do 30.09.2026, czyli 95–105 na 30 dni.

→ Pokaż w lejku *(odnośnik)*

#### Przeglądarki wbudowane w aplikacje tracą pacjentów na każdym kroku

W obu okresach płacą w 4,8–7,2% sesji, a Chrome i Safari w 16,1–18,1%. Usługę wybiera 19–26% sesji (Chrome i Safari 40%), termin 57–62% tych, które wybrały usługę (wobec 73–75%), a krok konta 60–62% tych, które wybrały termin (wobec 68–76%). Liczby sesji są w tabeli lejka po wybraniu podziału według przeglądarki.

→ Pokaż w lejku *(odnośnik)*

**Sesje poza lejkiem głównym** *(sekcja rozwijana, tu rozwinięta)*

Sesje zalogowane od wejścia: 8 026 w okresie X 2024 – IX 2025 i 14 042 w okresie X 2025 – IX 2026. Usługę wybiera 20,7% z nich, termin 112 sesji przez dwa lata, a płatności nie ma żadnej. Pokazujemy je osobno, bo dane nie rozstrzygają, czy to wizyty „sprawdzam konto”, czy zepsuta ścieżka zakupu.

Zakupy samego TelemediGO: 225 w okresie X 2024 – IX 2025 i 461 w okresie X 2025 – IX 2026. Mają tylko kroki płatności i płacą zawsze.

*Filtry (ustawienia domyślne):*
- Typ sesji: Sesje zwykłe (lejek) (do wyboru: Sesje zwykłe (lejek) / Zalogowane od wejścia / Zakup samego TelemediGO)
- Kto: Wszyscy (do wyboru: Wszyscy / Jeszcze nie kupowali / Kupowali wcześniej)
- Podział: Przeglądarka (do wyboru: Całość / Urządzenie / Przeglądarka / System i przeglądarka / Urządzenie i przeglądarka / Źródło (kanał) / Kampania / Strona wejścia)
- Porównanie: Okres 2 wobec okresu 1 (rok do roku) (do wyboru: Okres 2 wobec okresu 1 (rok do roku) / Ostatnie 90 dni wobec poprzednich 90 / Ostatnie 30 dni wobec tych samych dni rok wcześniej / 60 dni przed i po: Godzina bez danych (17.05.2025) / 60 dni przed i po: Start sprzedaży TelemediGO w newsletterze (crm_go_upsell) (8.09.2025) / 60 dni przed i po: Marża na pacjenta w 30 dniach spada stopniami (30.10.2025) / … (razem 17 opcji))
- Okres A: 2024-10-01 – 2025-09-30
- Okres B: 2025-10-01 – 2026-09-30

### Kroki lejka w podziale

*Okres A: 1.10.2024–30.09.2025 (365 dni). Okres B: 1.10.2025–30.09.2026 (365 dni). Typ: Sesje zwykłe. Kto: wszyscy.*

*W każdej komórce: odsetek w okresie B i liczba sesji, od której liczymy odsetek. Pod spodem ten sam odsetek w okresie A i zmiana w punktach procentowych. Zaznacz wiersze, które mają się pojawić na wykresie.*

| Przeglądarka | Sesje B (A) | Udział w sesjach B (A) | Wybór usługi | Wybór terminu | Logowanie albo konto | Wejście na płatność | Płatność przyjęta | Sesja do płatności |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Razem | 280 625<br>A: 154 085 | 100,0%<br>A: 100,0% | 34,4% z 280 625<br>A: 37,7% z 154 085 ▼3,2 | 71,3% z 96 655<br>A: 72,7% z 58 025 ▼1,4 | 71,0% z 68 888<br>A: 73,8% z 42 162 ▼2,8 | 86,4% z 48 886<br>A: 86,8% z 31 098 ▼0,4 | 91,1% z 42 246<br>A: 91,5% z 27 003 ▼0,4 | 13,7% z 280 625<br>A: 16,0% z 154 085 ▼2,3 |
| Chrome | 96 867<br>A: 74 456 | 34,5%<br>A: 48,3% | 39,8% z 96 867<br>A: 39,7% z 74 456 = 0,0 | 74,8% z 38 506<br>A: 73,8% z 29 565 ▲1,0 | 75,7% z 28 818<br>A: 74,3% z 21 819 ▲1,4 | 87,5% z 21 816<br>A: 87,2% z 16 210 ▲0,4 | 91,8% z 19 098<br>A: 91,5% z 14 128 ▲0,3 | 18,1% z 96 867<br>A: 17,4% z 74 456 ▲0,7 |
| Safari | 46 737<br>A: 34 705 | 16,7%<br>A: 22,5% | 40,0% z 46 737<br>A: 40,0% z 34 705 = 0,0 | 74,0% z 18 709<br>A: 73,2% z 13 892 ▲0,8 | 68,1% z 13 847<br>A: 74,1% z 10 166 ▼6,0 | 87,3% z 9 433<br>A: 86,5% z 7 538 ▲0,8 | 91,6% z 8 238<br>A: 91,8% z 6 523 ▼0,2 | 16,1% z 46 737<br>A: 17,2% z 34 705 ▼1,1 |
| Instagram (w aplikacji) | 39 744<br>A: 9 560 | 14,2%<br>A: 6,2% | 25,5% z 39 744<br>A: 19,4% z 9 560 ▲6,2 | 61,9% z 10 150<br>A: 58,4% z 1 853 ▲3,4 | 62,1% z 6 281<br>A: 60,4% z 1 083 ▲1,7 | 82,0% z 3 900<br>A: 80,1% z 654 ▲1,9 | 89,0% z 3 199<br>A: 88,0% z 524 ▲1,0 | 7,2% z 39 744<br>A: 4,8% z 9 560 ▲2,3 |
| TikTok (w aplikacji) | 31 535<br>A: 0 | 11,2%<br>A: 0,0% | 23,2% z 31 535<br>A: — z 0 | 60,5% z 7 327<br>A: — z 0 | 59,7% z 4 435<br>A: — z 0 | 81,2% z 2 648<br>A: — z 0 | 86,6% z 2 149<br>A: — z 0 | 5,9% z 31 535<br>A: — z 0 |
| Facebook (w aplikacji) | 28 676<br>A: 6 873 | 10,2%<br>A: 4,5% | 25,3% z 28 676<br>A: 19,9% z 6 873 ▲5,4 | 61,4% z 7 246<br>A: 56,7% z 1 368 ▲4,7 | 61,3% z 4 448<br>A: 61,0% z 776 ▲0,3 | 82,1% z 2 725<br>A: 83,1% z 473 ▼1,0 | 89,1% z 2 237<br>A: 88,8% z 393 ▲0,3 | 7,0% z 28 676<br>A: 5,1% z 6 873 ▲1,9 |
| Samsung Internet | 16 473<br>A: 12 439 | 5,9%<br>A: 8,1% | 38,9% z 16 473<br>A: 39,5% z 12 439 ▼0,6 | 75,2% z 6 401<br>A: 72,8% z 4 914 ▲2,4 | 75,4% z 4 813<br>A: 75,4% z 3 577 = 0,0 | 87,5% z 3 628<br>A: 86,9% z 2 696 ▲0,6 | 91,7% z 3 176<br>A: 91,6% z 2 344 ▲0,1 | 17,7% z 16 473<br>A: 17,3% z 12 439 ▲0,4 |
| Firefox | 9 445<br>A: 7 287 | 3,4%<br>A: 4,7% | 41,1% z 9 445<br>A: 40,0% z 7 287 ▲1,1 | 74,8% z 3 883<br>A: 73,6% z 2 917 ▲1,2 | 76,6% z 2 905<br>A: 75,3% z 2 146 ▲1,2 | 87,3% z 2 224<br>A: 87,9% z 1 617 ▼0,6 | 92,3% z 1 942<br>A: 91,8% z 1 422 ▲0,4 | 19,0% z 9 445<br>A: 17,9% z 7 287 ▲1,1 |
| Edge | 8 344<br>A: 6 595 | 3,0%<br>A: 4,3% | 39,7% z 8 344<br>A: 40,5% z 6 595 ▼0,8 | 74,9% z 3 309<br>A: 74,6% z 2 671 ▲0,3 | 75,8% z 2 479<br>A: 73,3% z 1 992 ▲2,5 | 87,4% z 1 880<br>A: 88,4% z 1 461 ▼0,9 | 90,7% z 1 644<br>A: 92,7% z 1 291 ▼2,0 | 17,9% z 8 344<br>A: 18,2% z 6 595 ▼0,3 |
| Opera | 2 804<br>A: 2 170 | 1,0%<br>A: 1,4% | 40,1% z 2 804<br>A: 38,9% z 2 170 ▲1,1 | 76,7% z 1 124<br>A: 71,4% z 845 ▲5,3 | 73,3% z 862<br>A: 74,5% z 603 ▼1,1 | 89,1% z 632<br>A: 84,2% z 449 ▲4,9 | 91,7% z 563<br>A: 91,5% z 378 ▲0,1 | 18,4% z 2 804<br>A: 15,9% z 2 170 ▲2,5 |

### Sesja do płatności (płatność / sesje), suma z 7 dni kończących się danego dnia

*Filtry (ustawienia domyślne):*
- Miara: Sesja do płatności (płatność / sesje) (do wyboru: Wybór usługi (usługa / sesje) / Wybór terminu (termin / usługa) / Logowanie albo konto (konto / termin) / Wejście na płatność (płatność / konto) / Płatność przyjęta (przyjęta / wejście) / Sesja do płatności (płatność / sesje) / Sesje dziennie / Udział w sesjach)
- Wygładzenie: suma z 7 dni (do wyboru: bez wygładzenia (dzień) / suma z 7 dni / suma z 28 dni)

*Szare pola to okresy A i B. Pionowe linie to zdarzenia z zakładki Zdarzenia. Przeciągnij po wykresie, żeby przybliżyć, kliknij dwukrotnie, żeby wrócić. Wartość pod kursorem pokazuje legenda pod wykresem, z liczbą sesji, od której liczymy odsetek.*

*[Wykres] serie: Chrome; Safari; Instagram (w aplikacji); TikTok (w aplikacji); Facebook (w aplikacji)*

1. 17.05.2025: Godzina bez danych
2. 8.09.2025: Start sprzedaży TelemediGO w newsletterze (crm_go_upsell)
3. 30.10.2025: Marża na pacjenta w 30 dniach spada stopniami
4. 3.11.2025: Start kampanii Meta na L4 (meta_prosp_l4_szybko)
5. 3.11.2025: Rośnie udział pacjentów nowych kampanii na L4 wśród nowych pacjentów
6. 13.11.2025: Więcej pierwszych zamówień zwracanych po wizycie
7. 24.11.2025: Poranne wizyty u internisty zaczynają się z opóźnieniem
8. 1.01.2026: Remarketing Meta słabnie, bo zmienia się pula odbiorców
9. 9.02.2026: Start kampanii TikTok na L4 (tt_prosp_l4_15min)
10. 10.02.2026: Powrót nowych pacjentów w 30 dniach spada
11. 2.03.2026: Powrót w 90 dniach w kampaniach działających w obu latach: brak wyraźnego skoku
12. 17.03.2026: Safari na iOS: gwałtownie spada skuteczność zakładania nowego konta
13. 10.06.2026: Duplikaty zamówień w eksporcie

*Jak liczymy: lejek główny obejmuje sesje zwykłe, czyli bez konta na wejściu albo z kontem, które pojawia się dopiero na kroku logowania. Sesje zalogowane od wejścia i zakupy samego TelemediGO są osobnymi typami sesji. „Jeszcze nie kupowali” to osoby bez zakupu przed początkiem sesji, także na koncie, na które logowały się w tej samej przeglądarce. Dzień sesji liczymy w czasie polskim. Płatności w lejku (24 717 w okresie X 2024 – IX 2025 i 38 490 w okresie X 2025 – IX 2026) i zamówienia (24 716 i 38 491) różnią się o 1 na granicy okresów, bo sesję liczymy do dnia jej rozpoczęcia, a zamówienie do dnia płatności; przychód z konsultacji po zwrotach w okresie X 2024 – IX 2025 to 2 230 266,50 zł, więc zależnie od zaokrąglenia 2 230 266 albo 2 230 267 zł. Źródło danych: analiza/a5p_lejek.py, eksport analiza/b_eksport.py.*

# Zakładka 4: Po zakupie (`#po-zakupie`)

## Po zakupie: przebieg wizyty

### Punktualność wizyt według pory i specjalizacji

Opóźnienia rosną tylko u internisty rano. Wizyty z terminem 6:00–11:59, które zaczęły się ponad 15 minut po terminie, u pacjentów spoza nowych kampanii: 4,7–6,9% miesięcznie do X 2025, 15,7% w XI 2025 (521 wizyt), 29,7% w XII 2025, 42,6% w I 2026 i 47,3–52,7% od II do IX 2026.

U internisty w innych porach: 2,8% wizyt spóźnionych ponad 15 minut w okresie X 2024 – IX 2025 (11 323 wizyty) i 4,6% w okresie X 2025 – IX 2026 (14 022 wizyty).

Długość wizyty i czas od zapłaty do terminu się nie zmieniają.

*Filtry (ustawienia domyślne):*
- Specjalizacja (wykres): Internista (do wyboru: Internista / Pediatra / Psychiatra / Inni specjaliści / Wszyscy)
- Pacjenci: Spoza nowych kampanii (do wyboru: Spoza nowych kampanii / Nowe kampanie na L4 / Wszyscy)
- Opóźnienie: ponad 15 minut (do wyboru: ponad 15 minut / ponad 30 minut)
- Wygładzenie: suma z 28 dni (do wyboru: dzień / suma z 7 dni / suma z 28 dni)

*Opóźnienie to faktyczny start wizyty minus umówiony termin, tylko wizyty odbyte. Dzień i pora według terminu. Wykres: odsetek wizyt spóźnionych w wybranej specjalizacji, osobno dla każdej pory, z liczbą wizyt w legendzie.*

*[Wykres] serie: Rano (6–11); Południe (12–15); Wieczór (16–23); Noc (0–5)*

| Specjalizacja | Pora terminu | Spóźnione ponad 15 minut: okres B = X 2025 – IX 2026 (A = X 2024 – IX 2025) |
| --- | --- | --- |
| Internista | Rano (6–11) | 41,2% z 6 522<br>A: 6,0% z 5 219 ▲35,3 |
| Internista | Południe (12–15) | 8,9% z 3 748<br>A: 3,0% z 2 974 ▲5,9 |
| Internista | Wieczór (16–23) | 2,6% z 8 852<br>A: 2,8% z 7 027 ▼0,3 |
| Internista | Noc (0–5) | 5,7% z 1 418<br>A: 1,9% z 1 322 ▲3,8 |
| Pediatra | Rano (6–11) | 3,8% z 393<br>A: 4,0% z 326 ▼0,2 |
| Pediatra | Południe (12–15) | 2,0% z 245<br>A: 2,7% z 187 ▼0,6 |
| Pediatra | Wieczór (16–23) | 2,1% z 621<br>A: 2,5% z 529 ▼0,4 |
| Pediatra | Noc (0–5) | 1,9% z 104<br>A: 1,2% z 82 ▲0,7 |
| Psychiatra | Rano (6–11) | 3,7% z 481<br>A: 3,2% z 349 ▲0,6 |
| Psychiatra | Południe (12–15) | 3,5% z 257<br>A: 4,5% z 200 ▼1,0 |
| Psychiatra | Wieczór (16–23) | 2,8% z 608<br>A: 3,1% z 448 ▼0,3 |
| Psychiatra | Noc (0–5) | 2,5% z 79<br>A: 3,8% z 78 ▼1,3 |
| Inni specjaliści | Rano (6–11) | 2,6% z 1 625<br>A: 2,4% z 1 274 ▲0,2 |
| Inni specjaliści | Południe (12–15) | 2,7% z 1 051<br>A: 2,3% z 826 ▲0,4 |
| Inni specjaliści | Wieczór (16–23) | 2,9% z 2 459<br>A: 2,1% z 1 913 ▲0,8 |
| Inni specjaliści | Noc (0–5) | 1,9% z 360<br>A: 2,4% z 328 ▼0,5 |

### Opóźnienia przy tym samym porannym ruchu

Przy tym samym porannym ruchu opóźnień jest teraz dużo więcej niż rok wcześniej. Średnio o 26,4 punktu procentowego więcej porannych wizyt u internisty zaczyna się ponad 15 minut po terminie (5 przedziałów ruchu obecnych w obu okresach, 9 979 wizyt). Na przykład w dni z 17–20 porannymi wizytami: 6,0% (89 dni) w okresie X 2024 – IX 2025 wobec 30,6% (58 dni) w okresie X 2025 – IX 2026.

W okresie X 2024 – IX 2025 opóźnienia nie zależą od ruchu (4,7–8,3% w każdym przedziale). W obrębie miesiąca dni z większym ruchem prawie nie mają więcej opóźnień: w tercylach dni według ruchu 5,4%, 6,1%, 6,1% w okresie X 2024 – IX 2025 i 42,1%, 43,5%, 43,6% w okresie X 2025 – IX 2026. Mediana ruchu porannego to 15 wizyt na dzień w okresie X 2024 – IX 2025 i 26 w okresie X 2025 – IX 2026.

Odczytanie: spadła poranna przepustowość, a nie tylko przybyło pacjentów. Możliwe przyczyny to mniejsza obsada rano, inna organizacja zapisów albo lekarze zajęci pacjentami spoza B2C. Której z nich, z tych danych nie da się ustalić, bo nie ma w nich grafików lekarzy.

*Filtry (ustawienia domyślne):*
- Pacjenci: Wszyscy (do wyboru: Wszyscy / Spoza nowych kampanii)

*Ruch poranny w dniu to wszystkie nieanulowane wizyty u internisty z terminem 6:00–11:59 tego dnia. Dni grupujemy według tego ruchu i w każdej grupie porównujemy odsetek porannych wizyt spóźnionych ponad 15 minut w obu okresach.*

| Poranne wizyty u internisty w dniu | Spóźnione ponad 15 minut: B = X 2025 – IX 2026 (A = X 2024 – IX 2025) | Dni B (A) |
| --- | --- | --- |
| do 8 | —<br>A: 6,2% z 178 | —<br>A: 29 |
| 9–12 | 15,1% z 86<br>A: 4,7% z 973 ▲10,4 | 8<br>A: 94 |
| 13–16 | 22,4% z 438<br>A: 6,8% z 1 602 ▲15,6 | 30<br>A: 113 |
| 17–20 | 30,6% z 1 054<br>A: 6,0% z 1 580 ▲24,6 | 58<br>A: 89 |
| 21–24 | 39,6% z 1 347<br>A: 4,8% z 681 ▲34,7 | 61<br>A: 32 |
| 25–28 | 46,9% z 2 013<br>A: 8,3% z 205 ▲38,6 | 78<br>A: 8 |
| 29–32 | 46,6% z 1 746<br>A: — | 59<br>A: — |
| 33–40 | 49,6% z 2 296<br>A: — | 67<br>A: — |
| 41 i więcej | 52,0% z 171<br>A: — | 4<br>A: — |

### Powrót według opóźnienia pierwszej wizyty

*Rano spada powrót po wizytach spóźnionych, nie po punktualnych. Tabela liczy powrót w 90 dniach na tych samych dniach kalendarzowych, tylko kohorty z pełnym oknem.*

*Filtry (ustawienia domyślne):*
- Pierwsza wizyta: Internista rano (6–11) (do wyboru: Internista rano (6–11) / Internista, każda pora / Wszystkie)
- Pacjenci (reguła przyjęta): Spoza nowych kampanii (do wyboru: Spoza nowych kampanii / Nowe kampanie na L4 / Wszyscy)

| Opóźnienie pierwszej wizyty | Powrót w 90 dniach: B = kohorty 1.10.2025–2.07.2026 (A = 1.10.2024–2.07.2025) |
| --- | --- |
| Do 5 minut po terminie | 27,0% z 826<br>A: 24,9% z 1 415 ▲2,1 |
| Ponad 5 do 15 minut | 19,9% z 977<br>A: 23,2% z 1 071 ▼3,4 |
| Ponad 15 do 30 minut | 16,0% z 557<br>A: 22,2% z 135 ▼6,2 |
| Ponad 30 minut | 10,1% z 533<br>A: 14,3% z 35 ▼4,2 |
| Brak wizyty (anulowana, nieodebrana) | 14,7% z 224<br>A: 19,1% z 188 ▼4,4 |

### Zwroty, anulacje i wizyty nieodebrane

Zwroty po odbytej wizycie skupiają się w L4 z nowych kampanii: w okresie X 2025 – IX 2026 zwrot dostaje 17,4% odbytych wizyt L4 ich pacjentów (5 895 wizyt) wobec 5,3% L4 pozostałych pacjentów (5 080 wizyt) i 6,0% w okresie X 2024 – IX 2025 (4 474 wizyty).

W okresie X 2025 – IX 2026 zwroty po wizycie u pacjentów nowych kampanii to 1 044 wizyty, 84 112 zł zwróconych zapłat i 33 975 zł kosztu lekarza za te wizyty. Powodu zwrotu w danych nie ma; możliwe odczytanie: lekarz nie wystawia L4, którego pacjent oczekuje po obietnicy reklamy.

*Filtry (ustawienia domyślne):*
- Pacjenci: Wszyscy (do wyboru: Wszyscy / Nowe kampanie na L4 / Spoza nowych kampanii)
- Zamówienia: Wszystkie (do wyboru: Wszystkie / Pierwsze / Kolejne)
- Wygładzenie: suma z 28 dni (do wyboru: dzień / suma z 7 dni / suma z 28 dni)

*Wykres: odsetek odbytych wizyt, za które pacjent dostał zwrot po wizycie, według celu wizyty i dnia płatności. Tabela: okres B to ostatnie 12 miesięcy, okres A to poprzednie 12.*

*[Wykres] serie: L4; E-recepta; Konsultacja; Skierowanie*

| Cel wizyty | Zwrot po odbytej wizycie | Anulowane przed wizytą | Pacjent nie odebrał | Zwrócone zapłaty B (A) | Koszt lekarza za zwrócone B (A) |
| --- | --- | --- | --- | --- | --- |
| L4 | 11,8% z 10 975<br>A: 6,0% z 4 474 ▲5,8 | 4,2% z 11 777<br>A: 4,5% z 4 815 ▼0,4 | 2,6% z 11 777<br>A: 2,5% z 4 815 ▲0,1 | 105 743 zł<br>A: 23 637 zł | 40 575 zł<br>A: 7 900 zł |
| E-recepta | 1,3% z 11 295<br>A: 1,2% z 8 091 ▲0,1 | 3,9% z 12 093<br>A: 4,3% z 8 677 ▼0,4 | 2,7% z 12 093<br>A: 2,5% z 8 677 ▲0,2 | 14 223 zł<br>A: 9 276 zł | 7 625 zł<br>A: 4 650 zł |
| Konsultacja | 1,3% z 10 764<br>A: 1,3% z 8 245 = 0,0 | 3,9% z 11 498<br>A: 3,8% z 8 791 ▲0,1 | 2,5% z 11 498<br>A: 2,4% z 8 791 ▲0,1 | 15 593 zł<br>A: 11 438 zł | 11 325 zł<br>A: 7 650 zł |
| Skierowanie | 1,3% z 2 926<br>A: 0,8% z 2 285 ▲0,5 | 4,1% z 3 123<br>A: 4,2% z 2 433 ▼0,1 | 2,2% z 3 123<br>A: 1,8% z 2 433 ▲0,4 | 2 973 zł<br>A: 1 534 zł | 1 025 zł<br>A: 525 zł |
| Razem | 4,5% z 35 960<br>A: 2,1% z 23 095 ▲2,4 | 4,0% z 38 491<br>A: 4,2% z 24 716 ▼0,2 | 2,6% z 38 491<br>A: 2,4% z 24 716 ▲0,2 | 138 532 zł<br>A: 45 884 zł | 60 550 zł<br>A: 20 725 zł |

### Oceny według opóźnienia wizyty

Spóźnione wizyty są gorzej oceniane, w obu okresach tak samo. U internisty, pacjenci spoza nowych kampanii: przy opóźnieniu ponad 30 minut średnia ocena to 2,95 w okresie X 2024 – IX 2025 i 2,92 w okresie X 2025 – IX 2026, a oceny 1–2 to 32% (513 ocen). Przy wizycie zaczętej do 5 minut po terminie średnia to 4,47 i 4,45, a ocen 1–2 jest 1% (6 807 ocen). Ocenę wystawia 32% pacjentów po odbytej wizycie.

*Filtry (ustawienia domyślne):*
- Specjalizacja: Internista (do wyboru: Internista / Pediatra / Psychiatra / Inni specjaliści / Wszyscy)
- Pacjenci: Spoza nowych kampanii (do wyboru: Spoza nowych kampanii / Nowe kampanie na L4 / Wszyscy)

| Opóźnienie wizyty | Odsetek ocenionych | Średnia ocena (1–5) | Oceny 1–2 |
| --- | --- | --- | --- |
| Do 5 minut po terminie | 31,3% z 11 007<br>A: 31,9% z 10 534 ▼0,6 | 4,45 z 3 446<br>A: 4,47 z 3 361 ▼0,02 | 1,1% z 3 446<br>A: 1,2% z 3 361 ▼0,2 |
| Ponad 5 do 15 minut | 30,8% z 6 198<br>A: 33,4% z 5 394 ▼2,6 | 4,38 z 1 909<br>A: 4,37 z 1 802 ▲0,01 | 1,5% z 1 909<br>A: 1,7% z 1 802 ▼0,3 |
| Ponad 15 do 30 minut | 31,7% z 1 786<br>A: 30,3% z 492 ▲1,4 | 3,69 z 566<br>A: 3,82 z 149 ▼0,13 | 8,7% z 566<br>A: 6,7% z 149 ▲1,9 |
| Ponad 30 minut | 30,3% z 1 550<br>A: 33,3% z 132 ▼3,1 | 2,92 z 469<br>A: 2,95 z 44 ▼0,03 | 31,8% z 469<br>A: 31,8% z 44 = 0,0 |

*Nowe kampanie na L4 to pacjenci z kampanii meta_prosp_l4_szybko i tt_prosp_l4_15min według przyjętej reguły źródła. Źródło danych: analiza/a5r_punktualnosc.py, analiza/a5r_po_zakupie.py, eksport analiza/b_eksport.py.*

# Zakładka 5: Zdarzenia (`#zdarzenia`)

## Oś zdarzeń: co się stało i kiedy

Zdarzenia znalezione w danych, bo listy zmian w produkcie i kalendarza kampanii nie mamy. Przy każdym: data, co się zmieniło, o ile i skąd to wiemy. Tory: lejek (pozyskanie), retencja (kohorty), obsługa pacjenta (przebieg wizyt) i jakość danych.

*Filtry (ustawienia domyślne):*
- ☑ Lejek (5)
- ☑ Retencja (4)
- ☑ Obsługa pacjenta (2)
- ☑ Jakość danych (2)

*[Oś czasu, rysunek] tory: Lejek, Retencja, Obsługa pacjenta, Jakość danych; znaczników zdarzeń: 13*

*1. 17.05.2025 · Jakość danych · luka w danych*

### Godzina bez danych

**Co się zmieniło:**
17.05.2025 od 13:00 do 14:00 jest 1 sesja zamiast typowych 21 (mediana tej samej godziny w 15 dniach wokół) i 0 zamówień. To jedyna taka godzina w dwóch latach. Wpływ na wyniki jest pomijalny, ale to luka w zbieraniu danych.

**Skąd wiemy:**
Liczba sesji w każdej godzinie wobec mediany tej samej godziny w 15 dniach wokół. Źródło: analiza/a2_jakosc.py, sekcja o lukach.

Zobacz w jakości danych

*2. 8.09.2025 · Lejek · start kampanii*

### Start sprzedaży TelemediGO w newsletterze (crm_go_upsell)

**Co się zmieniło:**
Newsletter do pacjentów, którzy już kupowali, prowadzi na stronę /telemedigo. Pojawiają się zakupy samego TelemediGO, bez konsultacji.

**O ile:**
686 zakupów samego TelemediGO do 30.09.2026, czyli 69% z 992 wejść z tej kampanii. Pozostałe 306 wejść to sesje zalogowane od wejścia, bez zakupu.

**Skąd wiemy:**
Pierwszy dzień z sesjami z tym kodem kampanii. Źródło: analiza/a5p_lejek.py, sekcja 1; notatki/a5_pozyskanie.md, punkt 2.4.

Pokaż w lejku

*3. 30.10.2025 · Retencja · zmiana wyniku kohort*

### Marża na pacjenta w 30 dniach spada stopniami

**Co się zmieniło:**
Marża nowego pacjenta w pierwszych 30 dniach (przed kosztem pozyskania) spada trzema stopniami, głównie przez skład pacjentów.

**O ile:**
56,0 zł od 1.10.2024 (17 520 pacjentów) → 53,1 zł od 30.10.2025 (5 549 pacjentów) → 50,1 zł od 26.01.2026 (6 064 pacjentów) → 46,8 zł od 8.04.2026 (9 744 pacjentów).

**Skąd wiemy:**
Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. Daty to kandydaci zmian, nie potwierdzone zdarzenia.

Pokaż w kohortach

*4. 3.11.2025 · Lejek · start kampanii*

### Start kampanii Meta na L4 (meta_prosp_l4_szybko)

**Co się zmieniło:**
Pierwszy dzień z sesjami i kosztem tej kampanii. Kampania przyprowadza głównie ruch w przeglądarkach wbudowanych w aplikacje, który płaci rzadziej niż wyszukiwarka.

**O ile:**
Średnio 183,7 sesji i 10,8 płatności dziennie, konwersja sesji do płatności 5,89%, razem 3 594 zamówienia do 30.09.2026. Od tego samego dnia: starsza kampania Meta 3,61% (20 687 sesji), wyszukiwarka bezpłatna 9,10% (43 291 sesji), Google Ads na hasła ogólne 8,55% (42 624 sesje). Ruch kampanii rośnie skokami: 17.11.2025, 8.12.2025, 2.01.2026, 19.01.2026.

**Skąd wiemy:**
Pierwszy dzień z sesjami z tym kodem kampanii w analityce; ten sam dzień w wydatkach na kampanie. Źródło: analiza/a5p_zdarzenia.py, sekcja 6; notatki/a5_pozyskanie.md, punkt 2.

Pokaż w lejku

*5. 3.11.2025 · Retencja · zmiana struktury pacjentów*

### Rośnie udział pacjentów nowych kampanii na L4 wśród nowych pacjentów

**Co się zmieniło:**
Od startu kampanii Meta na L4 coraz większa część nowych pacjentów przychodzi z dwóch nowych kampanii na L4. Ci pacjenci prawie nie wracają, więc ich udział obniża powrót całej kohorty.

**O ile:**
Udział w nowych pacjentach: 0,0% od 1.10.2024 do 2.11.2025 (17 676 pacjentów), 8,0% od 3.11.2025 do 5.12.2025 (1 972 pacjentów), 17,4% od 6.12.2025 do 2.02.2026 (4 127 pacjentów), 29,4% od 3.02.2026 do 9.04.2026 (5 503 pacjentów), 41,0% od 10.04.2026 do 30.09.2026 (11 640 pacjentów).

**Skąd wiemy:**
Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. Daty to kandydaci zmian, nie potwierdzone zdarzenia.

Pokaż w kohortach

*6. 13.11.2025 · Obsługa pacjenta · zmiana obsługi pacjenta*

### Więcej pierwszych zamówień zwracanych po wizycie

**Co się zmieniło:**
Rośnie odsetek pierwszych zamówień, za które pacjent dostaje zwrot po odbytej wizycie. Skupia się w wizytach L4 pacjentów nowych kampanii. Lekarz dostaje wynagrodzenie także za te wizyty.

**O ile:**
2,1% od 1.10.2024 (18 260 pacjentów) → 3,9% od 13.11.2025 (7 142 pacjentów) → 6,9% od 23.02.2026 (15 516 pacjentów).

**Skąd wiemy:**
Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. Daty to kandydaci zmian, nie potwierdzone zdarzenia.

Pokaż w zakładce „Po zakupie”

*7. 24.11.2025 · Obsługa pacjenta · zmiana obsługi pacjenta*

### Poranne wizyty u internisty zaczynają się z opóźnieniem

**Co się zmieniło:**
Rośnie odsetek wizyt u internisty z terminem 6:00–11:59, które zaczynają się ponad 15 minut po terminie, także u pacjentów spoza nowych kampanii. Przy tym samym porannym ruchu opóźnień jest teraz dużo więcej niż rok wcześniej, więc spadła poranna przepustowość (bez przesądzania przyczyny).

**O ile:**
6,3% od 1.10.2024 (6 148 wizyt) → 27,8% od 24.11.2025 (615 wizyt) → 41,9% od 26.12.2025 (730 wizyt) → 50,2% od 2.02.2026 (4 248 wizyt).

**Skąd wiemy:**
Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. Seria: wizyty u internisty rano, pacjenci spoza nowych kampanii. Daty to kandydaci zmian, nie potwierdzone zdarzenia.

Pokaż w zakładce „Po zakupie”

*8. 1.01.2026 · Lejek · zmiana stopniowa*

### Remarketing Meta słabnie, bo zmienia się pula odbiorców

**Co się zmieniło:**
Remarketing wraca coraz częściej do osób, które pierwszy raz przyszły z Meta i TikToka, a rzadziej do osób z wyszukiwarki. Te osoby płacą rzadziej. W obrębie źródła pierwszej wizyty konwersja stoi.

**O ile:**
Płatność na sesję u osób, które jeszcze nie kupowały: 28,2% w IV kwartale 2025 (1 011 sesji), 18,9% w II kwartale 2026 (1 603 sesje) i 19,1% w III kwartale 2026 (1 534 sesje). Udział przeglądarek w aplikacjach w tym ruchu rośnie z 13,3% do 22,1–23,4%. Osoby, które pierwszy raz przyszły z Google albo Bing: 27,9% w okresie X 2024 – IX 2025 i 26,7% od 1.01.2026 do 30.09.2026; z Meta (pozyskanie): 11,5% i 13,2%.

**Skąd wiemy:**
Metoda wykrywania zmian wskazała 20.03.2026 jako dzień zmiany poziomu płatności na sesję (27,3% → 19,1%), ale zmiana narasta od 1.01.2026. Źródło: analiza/a5p_zdarzenia.py, sekcje 5h i 5i; notatki/a5_pozyskanie.md, punkt 2.5.

Pokaż w lejku

*9. 9.02.2026 · Lejek · start kampanii*

### Start kampanii TikTok na L4 (tt_prosp_l4_15min)

**Co się zmieniło:**
Pierwszy dzień z sesjami i kosztem tej kampanii. Kampania przyprowadza głównie ruch w przeglądarkach wbudowanych w aplikacje, który płaci rzadziej niż wyszukiwarka.

**O ile:**
Średnio 143,0 sesji i 6,8 płatności dziennie, konwersja sesji do płatności 4,76%, razem 1 593 zamówienia do 30.09.2026. Od tego samego dnia: kampania Meta na L4 5,90% (48 952 sesje), wyszukiwarka bezpłatna 8,97% (29 242 sesje). Ruch kampanii rośnie skokami: 23.02.2026, 13.03.2026, 6.04.2026.

**Skąd wiemy:**
Pierwszy dzień z sesjami z tym kodem kampanii w analityce; ten sam dzień w wydatkach na kampanie. Źródło: analiza/a5p_zdarzenia.py, sekcja 6; notatki/a5_pozyskanie.md, punkt 2.

Pokaż w lejku

*10. 10.02.2026 · Retencja · zmiana zachowania kohort*

### Powrót nowych pacjentów w 30 dniach spada

**Co się zmieniło:**
Powrót w 30 dniach całej kohorty spada skokowo zaraz po starcie kampanii TikTok na L4 (9.02.2026); metoda wskazała dzień później. To głównie skład pacjentów (rosnący udział nowych kampanii), co pokazuje krok 3 analizy retencji.

**O ile:**
9,7% (12 514 pacjentów, 5.06.2025–9.02.2026) → 6,9% (14 536 pacjentów, 10.02.2026–31.08.2026). Wcześniejszy kandydat 5.06.2025: 11,4% → 9,7%; wypada w pierwszym roku, więc może być porą roku.

**Skąd wiemy:**
Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. Daty to kandydaci zmian, nie potwierdzone zdarzenia.

Pokaż w kohortach

*11. 2.03.2026 · Retencja · kandydat poniżej progu*

### Powrót w 90 dniach w kampaniach działających w obu latach: brak wyraźnego skoku

**Co się zmieniło:**
W kampaniach obecnych w obu latach powrót też spada, ale metoda nie znalazła zmiany skokowej powyżej progu. Najsilniejszy kandydat to ten dzień. Brak skoku nie znaczy, że spadek musi być rozłożony w czasie.

**O ile:**
23,3% przed (24 511 pacjentów) i 20,9% po (5 751 pacjentów, kohorty z pełnym oknem 90 dni).

**Skąd wiemy:**
Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. Luty 2026 nie pasuje do prostej hipotezy przeciążenia (opóźnienia już wysokie, powrót bez spadku), to trop eksploracyjny.

Pokaż w kohortach

*12. 17.03.2026 · Lejek · awaria*

### Safari na iOS: gwałtownie spada skuteczność zakładania nowego konta

**Co się zmieniło:**
U osób, które jeszcze nie kupowały, krok logowania albo zakładania konta po wyborze terminu spada w Safari na iPhone'ach i iPadach i zostaje niski do końca danych. Gwałtownie spada skuteczność zakładania nowego konta (konta dalej powstają, ale rzadziej), a logowanie do istniejącego działa.

**O ile:**
Z 66,2% w 60 dniach przed awarią (16.01.2026–16.03.2026, 1 763 sesje z wyborem terminu) do 45,1% w 60 dniach po niej (17.03.2026–15.05.2026, 1 553 sesje). Pozostałe przeglądarki: 64,8% i 63,4%. Szacunek: 628–695 utraconych pierwszych zamówień w 198 dniach do 30.09.2026, czyli 95–105 na 30 dni.

**Skąd wiemy:**
Metoda wykrywania zmian w seriach dziennych (podział binarny) wskazała ten dzień. Sprawdzenie na bazie: spadek jest w głównych kanałach (TikTok ma za małą próbę do oceny), więc to nie zmiana struktury ruchu. Przyczyny w danych nie widać. Źródło: analiza/a5p_zdarzenia.py, sekcja 5; notatki/a5_pozyskanie.md, punkt 2.1.

Pokaż w lejku

*13. 10.06.2026–24.06.2026 · Jakość danych · błąd danych*

### Duplikaty zamówień w eksporcie

**Co się zmieniło:**
W eksporcie dwa razy zapisano 604 zamówienia, wszystkie od 10.06.2026 do 24.06.2026. W tych dniach zdublowanych jest od 28% do 42% zamówień dziennie. Dzień przed oknem i dzień po nim: 0 zamówień zdublowanych.

**O ile:**
Wszystkie kopie są w okresie X 2025 – IX 2026. Dodają mu 604 zamówienia i 51 293 zł zapłat, czyli 45 805 zł po odjęciu zwrotów. W analityce każde z tych zamówień ma jeden krok płatności, więc to wygląda na błąd eksportu, a nie na podwójne płatności. Zostawiamy jedną kopię.

**Skąd wiemy:**
Dwie identyczne kopie zamówienia w sąsiednich liniach pliku zamówień. Źródło: analiza/a2_jakosc.py; czyszczenie: analiza/a2_czyste.py.

Zobacz w jakości danych

**Wszystkie zmiany wykryte automatycznie w lejku (surowy wynik metody)** *(sekcja rozwijana, tu rozwinięta)*

*Metoda dzieli każdą serię dzienną (podział, wartość, krok) na odcinki o różnym poziomie, w sesjach osób, które jeszcze nie kupowały. Nie każda wykryta zmiana jest zdarzeniem: część to zmiana struktury ruchu, część to sezon. Zdarzenia powyżej zostały sprawdzone na bazie.*

*Filtry (ustawienia domyślne):*
- Podział: Wszystkie (245) (do wyboru: Wszystkie (245) / Całość (3) / Urządzenie (14) / Przeglądarka (32) / Urządzenie i przeglądarka (44) / System i przeglądarka (50) / … (razem 9 opcji))

| Data | Podział | Wartość | Miara | Przed | Po | Zmiana | Dni przed / po | Zamówienia na 30 dni |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4.11.2024 | Przeglądarka | Chrome | Sesje dziennie | 171,1 | 218,3 | +47,3 | 34 / 178 | — | w lejku |
| 4.11.2024 | Przeglądarka | Firefox | Sesje dziennie | 16,5 | 21,8 | +5,3 | 34 / 173 | — | w lejku |
| 4.11.2024 | Urządzenie i przeglądarka | Komputer: Chrome | Sesje dziennie | 54,2 | 70,4 | +16,2 | 34 / 159 | — | w lejku |
| 4.11.2024 | Urządzenie i przeglądarka | Telefon: Chrome | Sesje dziennie | 112,8 | 144,5 | +31,7 | 34 / 178 | — | w lejku |
| 4.11.2024 | System i przeglądarka | Chrome na Androidzie | Sesje dziennie | 106,0 | 135,3 | +29,3 | 34 / 178 | — | w lejku |
| 4.11.2024 | System i przeglądarka | Chrome na Windowsie | Sesje dziennie | 46,7 | 59,5 | +12,7 | 34 / 178 | — | w lejku |
| 4.11.2024 | Źródło (kanał) | Wejścia bezpośrednie | Sesje dziennie | 44,9 | 59,4 | +14,5 | 34 / 173 | — | w lejku |
| 4.11.2024 | Kampania | Wejścia bezpośrednie | Sesje dziennie | 44,9 | 59,4 | +14,5 | 34 / 173 | — | w lejku |
| 4.11.2024 | Kampania | Google Ads: L4 | Sesje dziennie | 27,0 | 34,8 | +7,8 | 34 / 178 | — | w lejku |
| 4.11.2024 | Kampania | Google Ads: lekarz online | Sesje dziennie | 35,8 | 45,6 | +9,7 | 34 / 178 | — | w lejku |
| 11.11.2024 | Źródło (kanał) | Wyszukiwarka bezpłatna | Sesje dziennie | 95,2 | 125,7 | +30,5 | 41 / 171 | — | w lejku |
| 11.11.2024 | Kampania | Google bezpłatnie | Sesje dziennie | 90,6 | 119,4 | +28,8 | 41 / 171 | — | w lejku |
| 18.11.2024 | Urządzenie | Komputer | Sesje dziennie | 92,8 | 116,6 | +23,8 | 48 / 164 | — | w lejku |
| 25.11.2024 | Źródło (kanał) | Google Ads: hasło marki | Sesje dziennie | 28,1 | 35,5 | +7,3 | 55 / 157 | — | w lejku |
| 25.11.2024 | Kampania | Google Ads: marka | Sesje dziennie | 28,1 | 35,5 | +7,3 | 55 / 157 | — | w lejku |
| … pominięto 225 wierszy, tabela ma ich 245 … |  |  |  |  |  |  |  |  |  |
| 14.05.2026 | Kampania | Google Ads: lekarz online | Sesje dziennie | 46,6 | 34,9 | −11,7 | 192 / 140 | — | w lejku |
| 16.05.2026 | Kampania | Bing bezpłatnie | Sesje dziennie | 7,1 | 4,4 | −2,7 | 131 / 138 | — | w lejku |
| 22.05.2026 | Źródło (kanał) | Google Ads: hasło marki | Sesja do płatności | 21,2% | 17,8% | −3,4 pkt proc. | 598 / 132 | −39,6 | w lejku |
| 22.05.2026 | Kampania | Google Ads: marka | Sesja do płatności | 21,2% | 17,8% | −3,4 pkt proc. | 598 / 132 | −39,6 | w lejku |
| 2.07.2026 | Strona wejścia | /blog/e-recepta-jak-zrealizowac | Sesje dziennie | 6,7 | 4,3 | −2,4 | 255 / 91 | — | w lejku |

# Zakładka 6: Wynik biznesu (`#wynik`)

## Wynik biznesu: przychód, marża i ekonomia kampanii

### Przychód i marża w czasie

Marża po koszcie lekarza, kampaniach i prowizji afiliacyjnej: 1 048 069 zł w okresie X 2025 – IX 2026 wobec 828 085 zł w okresie X 2024 – IX 2025, czyli +26,6%. Ta suma ukrywa, jak zmienia się marża w kolejnych kwartałach.

Po kwartałach rok do roku marża zmienia się tak: w IV kwartale 2025 +71,4%, w I kwartale 2026 +43,0%, w II kwartale 2026 +13,0%, w III kwartale 2026 −6,8%. W III kwartale 2026 marża jest niższa niż rok wcześniej: 207 713 zł wobec 222 824 zł, choć wydatki na kampanie są 2,1 raza wyższe (181 555 zł wobec 87 431 zł). Po miesiącach: w VII marża jest jeszcze wyższa niż rok wcześniej, w VIII i IX niższa. Bazę porównania podnosi wrzesień 2025: TelemediGO daje wtedy 32 930 zł wobec średnio 11 238 zł miesięcznie wcześniej (start sprzedaży TelemediGO w newsletterze, zdarzenie na osi).

Przychód z konsultacji po zwrotach rośnie o 44,8% (2 230 266 zł → 3 228 342 zł), TelemediGO rośnie o 40,3% (156 551 zł → 219 652 zł). Koszt lekarza rośnie o 47,6% (1 175 700 zł → 1 734 825 zł), wydatki na kampanie rosną o 76,7% (367 632 zł → 649 675 zł), prowizja afiliacyjna rośnie o 0,2% (15 400 zł → 15 425 zł).

Koszt lekarza liczymy także za wizyty zwrócone po wizycie (zasada z zadania), a koszt i zwrot przypisujemy do dnia płatności. Prowizję afiliacyjną liczymy według przyjętej reguły źródła, w dniu pierwszego zamówienia.

*Filtry (ustawienia domyślne):*
- Grupowanie: miesiące (do wyboru: miesiące / tygodnie / dni)

*[Wykres] serie: Przychód (konsultacje po zwrotach i TelemediGO); Koszt lekarza; Kampanie i prowizja afiliacyjna; Marża*

#### Kwartały rok do roku

| Kwartał (B) wobec tego samego kwartału rok wcześniej (A) | Marża | Wydatki na kampanie | Przychód: konsultacje po zwrotach i TelemediGO | Koszt lekarza | Nowi pacjenci |
| --- | --- | --- | --- | --- | --- |
| IV kw. 2025 wobec IV kw. 2024 | 259 375 zł<br>A: 151 340 zł ▲71,4% | 113 089 zł<br>A: 87 253 zł ▲29,6% | 756 915 zł<br>A: 479 343 zł ▲57,9% | 380 925 zł<br>A: 237 125 zł ▲60,6% | 4 964<br>A: 4 186 ▲18,6% |
| I kw. 2026 wobec I kw. 2025 | 324 423 zł<br>A: 226 877 zł ▲43,0% | 170 625 zł<br>A: 102 565 zł ▲66,4% | 998 098 zł<br>A: 657 568 zł ▲51,8% | 497 875 zł<br>A: 323 375 zł ▲54,0% | 7 408<br>A: 4 789 ▲54,7% |
| II kw. 2026 wobec II kw. 2025 | 256 558 zł<br>A: 227 044 zł ▲13,0% | 184 405 zł<br>A: 90 383 zł ▲104,0% | 896 013 zł<br>A: 635 002 zł ▲41,1% | 451 550 zł<br>A: 313 825 zł ▲43,9% | 6 429<br>A: 3 819 ▲68,3% |
| III kw. 2026 wobec III kw. 2025 | 207 713 zł<br>A: 222 824 zł ▼6,8% | 181 555 zł<br>A: 87 431 zł ▲107,7% | 796 968 zł<br>A: 614 905 zł ▲29,6% | 404 475 zł<br>A: 301 375 zł ▲34,2% | 5 886<br>A: 3 437 ▲71,3% |

#### Miesiące i sumy okresów

| Okres | Zamówienia | Nowi pacjenci | Przychód: pierwsze zamówienia (zł) | Przychód: kolejne zamówienia (zł) | TelemediGO (zł) | Koszt lekarza (zł) | Kampanie (zł) | Prowizja afiliacyjna (zł) | Marża (zł) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Okres X 2024 – IX 2025 | 24 716 | 16 231 | 1 490 983 | 739 284 | 156 551 | 1 175 700 | 367 632 | 15 400 | 828 085 |
| Okres X 2025 – IX 2026 | 38 491 | 24 687 | 2 075 848 | 1 152 495 | 219 652 | 1 734 825 | 649 675 | 15 425 | 1 048 069 |
| Zmiana okres 2 wobec 1 | +55,7% | +52,1% | +39,2% | +55,9% | +40,3% | +47,6% | +76,7% | +0,2% | +26,6% |
| X 2024 | 1 351 | 1 285 | 118 984 | 6 960 | 6 853 | 64 650 | 27 160 | 1 025 | 39 962 |
| XI 2024 | 1 636 | 1 400 | 128 981 | 22 227 | 8 633 | 78 900 | 28 962 | 1 425 | 50 554 |
| XII 2024 | 1 932 | 1 501 | 137 175 | 39 740 | 9 790 | 93 575 | 31 130 | 1 175 | 60 824 |
| I 2025 | 2 218 | 1 628 | 149 106 | 52 238 | 11 392 | 106 400 | 34 406 | 1 950 | 69 979 |
| II 2025 | 2 173 | 1 560 | 144 147 | 54 149 | 10 057 | 100 750 | 32 760 | 1 300 | 73 544 |
| III 2025 | 2 435 | 1 601 | 147 477 | 75 118 | 13 884 | 116 225 | 35 399 | 1 500 | 83 354 |
| IV 2025 | 2 341 | 1 430 | 129 033 | 80 745 | 12 905 | 110 575 | 33 289 | 1 400 | 77 418 |
| V 2025 | 2 262 | 1 266 | 117 750 | 88 858 | 12 371 | 110 075 | 29 361 | 1 050 | 78 494 |
| VI 2025 | 2 052 | 1 123 | 101 413 | 77 954 | 13 973 | 93 175 | 27 733 | 1 300 | 71 132 |
| VII 2025 | 2 104 | 1 116 | 105 746 | 85 025 | 11 926 | 105 800 | 29 040 | 1 025 | 66 832 |
| VIII 2025 | 2 041 | 1 074 | 97 230 | 81 467 | 11 837 | 93 825 | 28 419 | 1 100 | 67 190 |
| IX 2025 | 2 171 | 1 247 | 113 941 | 74 803 | 32 930 | 101 750 | 29 973 | 1 150 | 88 802 |
| X 2025 | 2 432 | 1 383 | 124 508 | 85 596 | 15 664 | 113 775 | 31 860 | 950 | 79 184 |
| XI 2025 | 2 713 | 1 692 | 151 699 | 86 322 | 17 266 | 130 400 | 36 825 | 1 225 | 86 837 |
| XII 2025 | 2 960 | 1 889 | 166 480 | 90 066 | 19 313 | 136 750 | 44 405 | 1 350 | 93 354 |
| I 2026 | 3 566 | 2 423 | 213 310 | 96 071 | 21 538 | 165 850 | 52 194 | 1 675 | 111 201 |
| II 2026 | 3 449 | 2 303 | 198 385 | 97 830 | 16 821 | 159 300 | 52 694 | 1 450 | 99 592 |
| III 2026 | 3 964 | 2 682 | 226 307 | 106 030 | 21 805 | 172 725 | 65 738 | 2 050 | 113 630 |
| IV 2026 | 3 570 | 2 256 | 187 719 | 111 100 | 19 046 | 161 675 | 64 197 | 1 450 | 90 542 |
| V 2026 | 3 475 | 2 199 | 176 132 | 106 902 | 19 224 | 152 625 | 60 478 | 1 150 | 88 005 |
| VI 2026 | 3 181 | 1 974 | 157 866 | 98 713 | 19 313 | 137 250 | 59 731 | 900 | 78 011 |
| VII 2026 | 3 070 | 1 958 | 159 001 | 96 190 | 18 601 | 138 850 | 60 659 | 900 | 73 384 |
| VIII 2026 | 3 011 | 1 887 | 152 189 | 91 769 | 16 287 | 134 000 | 58 805 | 1 125 | 66 315 |
| IX 2026 | 3 100 | 2 041 | 162 251 | 85 906 | 14 774 | 131 625 | 62 092 | 1 200 | 68 014 |

### Ekonomia kampanii: koszt pozyskania i wynik na pacjenta

Nowe kampanie na L4 (okres X 2025 – IX 2026): wynik na pacjenta po koszcie pozyskania według przyjętej reguły źródła +3,6 zł w 90 dniach i +7,0 zł w 180 dniach, a według sesji płatności −9,4 zł i −5,2 zł. Znak zależy od reguły, więc to wynik niepewny.

Kampania na TikToku ma wynik ujemny w obu regułach: −4,6 zł i −17,8 zł na pacjenta w 90 dniach.

Obok wyniku po 90 dniach pokazujemy wynik po 180 dniach: pacjenci kampanii na L4 prawie nie wracają, a pozostali tak, więc 90 dni zaniża wartość pozostałych kampanii. Przedział przy wyniku jest warunkowy: liczony tylko z rozrzutu marży, bez niepewności atrybucji.

*Filtry (ustawienia domyślne):*
- Poziom: Grupy kampanii (do wyboru: Grupy kampanii / Kampanie / Kanały)
- Okres: Okres X 2025 – IX 2026 (do wyboru: Okres X 2025 – IX 2026 / Okres X 2024 – IX 2025)

*Wynik na pacjenta to marża na pacjenta w 90 albo 180 dniach minus koszt pozyskania (wydatki na kampanię albo prowizja afiliacyjna na nowego pacjenta). Koszt pozyskania liczymy osobno dla każdego okna: z kohort z pełnym oknem i z wydatków z tych samych dni, więc po 180 dniach to inne kohorty i inny koszt niż po 90 dniach. Obie reguły źródła stoją obok siebie. Pod kosztem: liczba pacjentów; pod wynikiem: marża minus koszt. Przedział warunkowy po najechaniu na wynik.*

| Grupa | Przyjęta reguła źródła — Koszt pozyskania, 90 dni | Przyjęta reguła źródła — Wynik na pacjenta, 90 dni | Przyjęta reguła źródła — Koszt pozyskania, 180 dni | Przyjęta reguła źródła — Wynik na pacjenta, 180 dni | Sesja płatności — Koszt pozyskania, 90 dni | Sesja płatności — Wynik na pacjenta, 90 dni | Sesja płatności — Koszt pozyskania, 180 dni | Sesja płatności — Wynik na pacjenta, 180 dni | Ocena |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nowe kampanie na L4 (Meta i TikTok) | 32,7 zł<br>4 893 pac. | +3,6 zł<br>marża 36,3 zł − koszt 32,7 zł | 30,3 zł<br>2 352 pac. | +7,0 zł<br>marża 37,3 zł − koszt 30,3 zł | 45,6 zł<br>3 510 pac. | −9,4 zł<br>marża 36,1 zł − koszt 45,6 zł | 42,1 zł<br>1 693 pac. | −5,2 zł<br>marża 36,9 zł − koszt 42,1 zł | niepewny: znak zależy od reguły |
| Pozostałe kampanie płatne | 44,2 zł<br>7 076 pac. | +20,0 zł<br>marża 64,2 zł − koszt 44,2 zł | 42,6 zł<br>5 130 pac. | +29,7 zł<br>marża 72,3 zł − koszt 42,6 zł | 43,8 zł<br>7 141 pac. | +18,7 zł<br>marża 62,4 zł − koszt 43,8 zł | 43,5 zł<br>5 029 pac. | +27,5 zł<br>marża 71,0 zł − koszt 43,5 zł |  |
| Afiliacja (ranking lekarzy) | 25,0 zł<br>489 pac. | +32,2 zł<br>marża 57,2 zł − koszt 25,0 zł | 25,0 zł<br>352 pac. | +37,0 zł<br>marża 62,0 zł − koszt 25,0 zł | 25,0 zł<br>319 pac. | +30,8 zł<br>marża 55,8 zł − koszt 25,0 zł | 25,0 zł<br>229 pac. | +35,6 zł<br>marża 60,6 zł − koszt 25,0 zł |  |
| Kanały bezpłatne | 0,0 zł<br>6 466 pac. | +68,6 zł<br>marża 68,6 zł − koszt 0,0 zł | 0,0 zł<br>4 757 pac. | +78,1 zł<br>marża 78,1 zł − koszt 0,0 zł | 0,0 zł<br>7 954 pac. | +64,5 zł<br>marża 64,5 zł − koszt 0,0 zł | 0,0 zł<br>5 640 pac. | +74,2 zł<br>marża 74,2 zł − koszt 0,0 zł |  |

*Płatności w lejku (24 717 w okresie X 2024 – IX 2025 i 38 490 w okresie X 2025 – IX 2026) i zamówienia (24 716 i 38 491) różnią się o 1 na granicy okresów, bo sesję liczymy do dnia jej rozpoczęcia, a zamówienie do dnia płatności; przychód z konsultacji po zwrotach w okresie X 2024 – IX 2025 to 2 230 266,50 zł, więc zależnie od zaokrąglenia 2 230 266 albo 2 230 267 zł. Źródło danych: analiza/definicje.py (koszt lekarza, marża), analiza/a5e_ekonomia.py (ekonomia kampanii), eksport analiza/b_eksport.py.*

# Zakładka 7: Jakość danych (`#jakosc`)

## Jakość danych

Danych nikt wcześniej nie czyścił. Poniżej: jak dashboard ma się do danych oczyszczonych, co usunęliśmy i dlaczego, drobne niespójności oraz to, co sprawdziliśmy i jest czyste.

### Od dashboardu do danych oczyszczonych

*Dashboard liczy dane na surowo: z duplikatami zamówień, z zamówieniami testowymi i z przychodem przed zwrotami. Każdy wiersz mostka zmienia jedną rzecz.*

*Wzrost: okres X 2025 – IX 2026 wobec okresu X 2024 – IX 2025. Pod wzrostem: wartości w obu okresach.*

| Krok | Nowi pacjenci | Zamówienia | Przychód z konsultacji | TelemediGO |
| --- | --- | --- | --- | --- |
| Dashboard (dane surowe) | +51,9%<br>16 251 → 24 689 | +60,7%<br>25 269 → 40 613 | +50,3%<br>2,382 → 3,580 mln zł | +40,3%<br>1 759 → 2 468 |
| Bez duplikatów zamówień | bez zmian | +58,3%<br>25 269 → 40 009 | +48,1%<br>2,382 → 3,529 mln zł | bez zmian |
| Bez duplikatów i bez kont testowych | +52,1%<br>16 231 → 24 687 | +55,7%<br>24 716 → 38 491 | +47,7%<br>2,375 → 3,508 mln zł | bez zmian |
| Do tego przychód po odjęciu zwrotów | bez zmian | bez zmian | +44,8%<br>2,230 → 3,228 mln zł | bez zmian |

### Duplikaty zamówień

W eksporcie dwa razy zapisano 604 zamówienia, wszystkie od 10.06.2026 do 24.06.2026. W tych dniach zdublowanych jest od 28% do 42% zamówień dziennie. Dzień przed oknem i dzień po nim: 0 zamówień zdublowanych.

Wszystkie kopie są w okresie X 2025 – IX 2026. Dodają mu 604 zamówienia i 51 293 zł zapłat, czyli 45 805 zł po odjęciu zwrotów. W analityce każde z tych zamówień ma jeden krok płatności, więc to wygląda na błąd eksportu, a nie na podwójne płatności. Zostawiamy jedną kopię.

*[Wykres] serie: Zamówienia bez kopii; Kopie (duplikaty)*

### Zamówienia testowe

Zamówienia testowe: 2 071 zamówień z 22 kont. Kod TEST-QA ma 1 781 zamówień. Pozostałe 290 zamówień nie ma kodu, ale każde jest zapłacone w pełni i w całości zwrócone, czyli wygląda na test procesu zwrotu. Filtr po samym kodzie by ich nie złapał.

Drugi, niezależny podpis: wszystkie trwają dokładnie 1 minutę (2 071 z 2 071), a taki czas nie występuje u żadnego innego pacjenta (0 zamówień; najkrótsza prawdziwa wizyta trwa 3 minuty).

Testów przybywa: 553 zamówienia w okresie X 2024 – IX 2025 i 1 518 zamówień w okresie X 2025 – IX 2026. Zawyżały więc wzrost zamówień. Wyłączamy te konta ze wszystkiego: zamówień, pacjentów, przychodu, sesji i lejka.

Pieniądze: 27 591 zł zapłat i 25 810 zł zwrotów. Gdyby lekarz dostawał 25 zł za każdą taką wizytę, koszt wyniósłby 51 775 zł. Czy dostawał, z danych nie wiemy, więc to idzie na listę niewiadomych.

| Kwartał | Zamówienia testowe |
| --- | --- |
| IV kw. 2024 | 35 |
| I kw. 2025 | 94 |
| II kw. 2025 | 170 |
| III kw. 2025 | 254 |
| IV kw. 2025 | 330 |
| I kw. 2026 | 370 |
| II kw. 2026 | 410 |
| III kw. 2026 | 408 |

### Godzina bez danych

17.05.2025 od 13:00 do 14:00 jest 1 sesja zamiast typowych 21 (mediana tej samej godziny w 15 dniach wokół) i 0 zamówień. To jedyna taka godzina w dwóch latach. Wpływ na wyniki jest pomijalny, ale to luka w zbieraniu danych.

### Drobne niespójności

- „Psycholog + e-recepta”: 24 zamówienia. Psycholog nie jest lekarzem i nie wystawia recept, więc to wartość nierealna.
- Mimo aktywnego TelemediGO bez zniżki zapłacono 1 zamówienie.
- Program poleceń: na stronę /polecenie wchodzi z innym źródłem (bezpośrednio, z Google albo z Meta) 330 sesji, a źródło „polecenie” z inną stroną wejścia ma 51 sesji. Ma to znaczenie przy przypisywaniu źródła pacjenta.

### Sprawdzone i czyste

- Czas płatności: 65 278 z 65 278 zamówień i 4 227 z 4 227 zakupów TelemediGO ma krok płatności w analityce co do sekundy po przeliczeniu z UTC na czas polski. Zmiana czasu jest obsłużona poprawnie.
- Sesje na kliknięcie są stałe w każdym kwartale: Google Ads od 0,92 do 0,93, Meta od 0,79 do 0,82, TikTok 0,72. Nie ma dni z kosztem bez sesji ani sesji z kampanii płatnej bez kosztu.
- Duplikaty w pozostałych tabelach: sesje 0, kroki lejka 0, konta 0, TelemediGO 0, wydatki na kampanie 0.
- Kroki lejka idą zawsze po kolei: 0 sesji ma krok bez poprzedniego. Jedyne wyjątki zgodne z opisem danych to 686 zakupów samego TelemediGO (tylko kroki płatności) i 22 sesje kont testowych z samym założeniem konta.
- Tożsamość: żadna przeglądarka nie jest dzielona przez dwa konta. Więcej niż jednej przeglądarki używa 7,3% kont (3 835 z 52 422), najwięcej 8 przeglądarek.
- Wartości realne: wizyty po oczyszczeniu trwają od 3 do 36 minut; ceny katalogowe i zniżki TelemediGO zgadzają się z zasadami co do złotówki (raport A2).

*Źródło: analiza/a2_jakosc.py, analiza/a2_czyste.py, analiza/a3_dashboard.py; liczby na tej stronie liczy analiza/b_eksport.py.*

# Zakładka 8: Priorytety (`#priorytety`)

## Priorytety: co robimy po kolei

Lista od najważniejszej pozycji. Przy każdej: co widać w danych, ile jest warta w złotych marży na rok (z założeniami), po czym poznamy, że zadziałała, i ile zajmie wdrożenie. Przy słabym wyniku kampanii pokazujemy obie drogi, naprawić albo wyłączyć, każdą z wartością w marży. Numer w tabeli przeglądu prowadzi do karty pozycji, a karta do zakładek z danymi.

### Przegląd

| Nr | Co robimy | Ile warte rocznie (marża) | Pewność | Wdrożenie |
| --- | --- | --- | --- | --- |
| 1 | Naprawić zakładanie konta w Safari na iOS | 75–83 tys. zł (90 dni), 86–95 tys. zł (180 dni); górna granica | wysoka: awaria widoczna w danych | dni |
| 2 | Naprawić pomiar: raport bez duplikatów i kont testowych, przychód po zwrotach, zamknąć testy TEST-QA, wynagrodzenie lekarzy za testy, alarmy na lejku i zwrotach | 0 albo 38 tys. zł bezpośrednio; pośrednio warunek pozostałych decyzji | wysoka: oba błędy widoczne w danych | 1 dzień sprawdzenie, 1–2 tygodnie raport |
| 3 | Wstrzymać TikToka na L4 | przy 100% pacjentów dodatkowych, pełny rok: +18,6 do +48,0 tys. zł (90 dni), +21,0 do +50,4 tys. zł (180 dni); więcej przy mniejszej dodatkowości | wysoka co do znaku | 1 dzień |
| 4 | Wstrzymać gs_generic_specjalisci (Google Ads na specjalistów) do czasu zmiany cennika | +19,4 do +31,5 tys. zł przy 100% pacjentów dodatkowych, do +53,2 tys. zł | wysoka co do znaku | 1 dzień |
| 5 | Uczciwa obietnica w reklamach L4 Meta (test dwóch kreacji) | 18,1–46,5 tys. zł (przyjęta reguła), 10,7–26,7 tys. zł (sesja płatności), pełny rok | średnia: nie znamy powodu zwrotów | 1–2 tygodnie + 4–6 tygodni pomiaru |
| 6 | Poranna obsada internistów: diagnoza, potem test | scenariusz od 0 do 65 tys. zł, koszt obsady nieznany | niska co do kwoty | diagnoza 1–2 dni, test 2–4 tygodnie |
| 7 | Komunikacja po wizycie z losową grupą kontrolną (retencja) | scenariusz: 23,6 tys. zł za każdy punkt procentowy powrotu w 90 dniach | niska co do kwoty | dane o wysyłkach dni, sekwencja 2–4 tygodnie, pomiar 90 dni |
| 8 | Sprawdzić ręcznie zakup dla zalogowanych pacjentów | 0 albo 36–40 tys. zł (wysoki scenariusz 89 tys. zł) | niska: dane wskazują raczej na 0 zł | 1 dzień |
| 9 | Test dodatkowości Meta na L4 w parach województw, z progiem decyzji około 85% | decyzja warta od −30,6 (90 dni) albo −32,9 (180 dni) do +179,6 tys. zł, pełny rok | — (to jest test) | 1 tydzień + 4–6 tygodni |
| 10 | Cennik specjalistów i warunki TelemediGO u specjalistów | TelemediGO: scenariusze 15–31 tys. zł po pełnym roku (w pierwszym około połowa); cennik: do 73,6 tys. zł za każde 10 zł podwyżki przy tej samej liczbie wizyt (górna granica) | wysoka co do kierunku, niska co do kwoty cennika | 1–2 tygodnie + test dwóch cen 4 tygodnie |
| 11 | Sprawdzić stratę między kliknięciem a sesją w Meta i TikToku | 0 albo do 52 tys. zł (górna granica, po wstrzymaniu TikToka mniej) | niska | 1–2 dni |
| 12 | Test TelemediGO z losowym, bezpłatnym dostępem do zniżek | decyduje o roli programu; koszt testu 3–12 tys. zł | — (to jest test) | 2–8 tygodni + 90 dni |

### Zasady listy

- Wartość to zmiana marży na rok. Rokiem bazowym jest okres 2. Marża = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza − wydatki na kampanie − prowizja afiliacyjna.
- Przy kampaniach podajemy wynik po 90 i po 180 dniach od pozyskania oraz według obu reguł źródła. Kwoty kampanii, które działały krócej niż rok, przeliczamy na pełny rok przy tym samym tempie: TikTok działał w okresie 2 przez 234 dni (mnożnik 1,56), Meta na L4 przez 332 dni (1,10).
- Kwot nie sumujemy. Mają różne horyzonty i zależą od siebie. Każdą wyceniamy przy założeniu, że wcześniejsze pozycje są zrobione: po wstrzymaniu TikToka naprawa obietnicy L4 dotyczy już tylko Meta.
- Kolejność to waga, a nie kalendarz. Pozycje 1, 3, 4 i krótkie sprawdzenia (pierwsze kroki pozycji 2, 6, 8 i 11) zespół może zrobić równolegle w pierwszym tygodniu.
- Zasada budżetu: pieniędzy uwolnionych przez pozycje 3 i 4 nie przesuwamy automatycznie do innych kampanii, bo kolejna złotówka zarabia zwykle mniej niż średnia. Przesuwamy tylko z testem. Niewydanie ich też liczy się do marży.
- Czas wdrożenia to nasz szacunek, a nie liczba z danych.

*Okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026; jeśli nie napisano inaczej, liczby dotyczą okresu 2. Przyjęta reguła źródła = pierwsze wejście pacjenta (także anonimowe sesje jego przeglądarek), a kod kampanii na pierwszym zamówieniu rozstrzyga. Sesja płatności = reguła porównawcza. Nowe kampanie = meta_prosp_l4_szybko (Meta, od 3.11.2025) i tt_prosp_l4_15min (TikTok, od 9.02.2026), obie na zwolnienie lekarskie (L4). Pacjent dodatkowy = taki, który bez kampanii by nie przyszedł.*

### 1. Naprawić zakładanie konta w Safari na iOS

*Ile warte rocznie: 75–83 tys. zł (90 dni), 86–95 tys. zł (180 dni); górna granica · Pewność: wysoka: awaria widoczna w danych · Wdrożenie: dni*

**Z danych:**
- Od 17.03.2026 w Safari na iPhone'ach i iPadach gwałtownie spada skuteczność zakładania nowego konta (konta dalej powstają, ale rzadziej: 668 zamiast 1 082 w 60 dniach).
- Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spada z 66,1% (od 1.10.2025 do 16.03.2026) do 45,6% (od 17.03 do 30.09.2026, 4 678 sesji z wyborem terminu) i nie wraca.
- Logowanie do istniejących kont działa. Inne przeglądarki tego nie mają, a spadek jest w głównych kanałach; TikTok ma za małą próbę do oceny.

**Ile warta:**
- W 198 dniach od 17.03 do 30.09.2026 to 628–695 utraconych pierwszych zamówień, czyli 1 158–1 281 rocznie.
- Nowy pacjent z pierwszą płatnością w Safari na iOS zostawia w okresie 2 średnio 64,6 zł marży przed kosztem pozyskania w 90 dniach (2 990 pacjentów) i 74,3 zł w 180 dniach (2 278).
- Daje to 75–83 tys. zł rocznie w horyzoncie 90 dni i 86–95 tys. zł w horyzoncie 180 dni.
- W samym III kwartale 2026 to około 14–21 tys. zł marży, czyli skala porównywalna ze spadkiem marży rok do roku (15,1 tys. zł); wyniku kwartału bez awarii nie ustaliliśmy.
- 628–695 to scenariusz przy przyjętych założeniach, a nie przedział ufności.

**Założenia:**
- Utracone pierwsze zamówienie to utracony nowy pacjent. To górna granica: odpadnięci nie kupują później częściej w tej samej przeglądarce, ale innych urządzeń nie widzimy.
- Nie doliczamy kosztu pozyskania, bo wejście już zostało opłacone.
- Skala problemu utrzymywałaby się przez rok. Przeliczenie z marca–września może zaniżać, bo pomija zimę.
- Kwoty to marża rocznika odzyskanych pacjentów, a nie wpływy w całości w tym samym roku.

**Po czym poznamy:**
Krok konta po wyborze terminu w Safari na iOS u osób, które jeszcze nie kupowały, wraca z około 46% do około 66% w ciągu tygodnia od poprawki, a zakładanie kont wraca do poziomu sprzed 17.03 (około 1 080 w 60 dniach).

**Wdrożenie:**
Powtórzenie rejestracji na iPhonie, logi błędów i lista zmian z 16–17.03.2026 to 1–2 dni. Sama poprawka to zwykle dni.

Zobacz w danych: Lejek: krok konta w Safari na iOS przed awarią i po niej · Zdarzenie na osi: awaria Safari na iOS

*Skąd liczby: analiza/wyniki/c_priorytety.txt (P1, P15), analiza/wyniki/a5p_zdarzenia.txt (5d–5f), notatki/a5_pozyskanie.md (sekcja 2).*

*↑ Wróć do przeglądu*

### 2. Naprawić pomiar: codzienny raport, zamówienia testowe i alarmy

*Ile warte rocznie: 0 albo 38 tys. zł bezpośrednio; pośrednio warunek pozostałych decyzji · Pewność: wysoka: oba błędy widoczne w danych · Wdrożenie: 1 dzień sprawdzenie, 1–2 tygodnie raport*

**Z danych:**
- Codzienny raport liczy dane na surowo. Zawiera 604 zdublowane zamówienia z 10–24.06.2026, 2 071 zamówień 22 kont testowych i przychód przed zwrotami.
- Konta testowe mają kod TEST-QA albo zamówienia bez kodu, a wszystkie ich wizyty trwają 1 minutę u internisty.
- Przez to raport pokazuje +60,7% zamówień (25 269 → 40 613) zamiast +55,7% (24 716 → 38 491) i +50,3% przychodu z konsultacji zamiast +44,8% po zwrotach.
- Testów przybywa: 553 zamówienia w okresie 1 i 1 518 w okresie 2.
- Raport liczy też zamówienia i przychód, a nie marżę po koszcie pozyskania i powroty kohort. Dlatego kampanie na L4 wyglądały na nim jak wzrost.

**Co robimy:**
- Raport bez duplikatów i kont testowych, przychód po zwrotach.
- Testy przeniesione z produkcji na środowisko testowe.
- Jednodniowe sprawdzenie w dziale rozliczeń, czy lekarze dostają wynagrodzenie za wizyty testowe.
- Sprawdzenie, czy kod TEST-QA nie wyciekł poza 22 konta i czy przy duplikatach nikt nie zapłacił dwa razy.
- Do raportu: marża po koszcie pozyskania według źródła, zwroty po wizycie według kampanii, powrót w 90 dniach każdej kohorty dziennej i kroki lejka według przeglądarki, z alarmami.

**Ile warta:**
- Bezpośrednio 37 950 zł rocznie, jeśli lekarze dostają 25 zł za każdą wizytę testową (wszystkie są u internisty), albo 0 zł, jeśli nie dostają. Pieniądze już wypłacone są stracone, a oszczędność dotyczy kolejnych miesięcy.
- Pośrednio: bez poprawnych liczb nie da się prowadzić biznesu na kohortach. Alarm na krokach lejka wykryłby awarię Safari po kilku dniach, a nie po 198. Wykrycie po tygodniu ograniczyłoby stratę do 3,5% (22–25 zamówień zamiast 628–695).

**Po czym poznamy:**
Raport pokazuje te same liczby co oczyszczona warstwa danych (w okresie 2: 38 491 zamówień i 3,228 mln zł przychodu z konsultacji po zwrotach), a od ustalonej daty na produkcji nie ma zamówień testowych.

**Wdrożenie:**
Sprawdzenie wynagrodzeń 1 dzień; raport i testy 1–2 tygodnie; alarmy 2–4 tygodnie.

Zobacz w danych: Jakość danych: duplikaty, zamówienia testowe, mostek od dashboardu · Zdarzenie na osi: duplikaty zamówień

*Skąd liczby: analiza/wyniki/c_priorytety.txt (P1b, P13, P15, W3), analiza/wyniki/a3_dashboard.txt, analiza/wyniki/a2_jakosc.txt.*

*↑ Wróć do przeglądu*

### 3. Wstrzymać kampanię TikTok na L4

*Ile warte rocznie: przy 100% pacjentów dodatkowych, pełny rok: +18,6 do +48,0 tys. zł (90 dni), +21,0 do +50,4 tys. zł (180 dni); więcej przy mniejszej dodatkowości · Pewność: wysoka co do znaku · Wdrożenie: 1 dzień*

**Z danych:**
Wynik na pacjenta jest ujemny w obu regułach i w obu oknach: −4,6 i −17,8 zł po 90 dniach, −1,1 i −11,0 zł po 180 dniach. Pacjenci wracają w 90 dniach w 3,2% (1 265 pacjentów według przyjętej reguły, kohorty od 9.02.2026).

**Naprawić albo wyłączyć:**
- Kwoty z 234 dni działania kampanii w okresie 2, w nawiasie pełny rok (mnożnik 1,56).
- Dziś: −11,9 tys. zł (−18,6) według przyjętej reguły i −30,8 tys. zł (−48,0) według sesji płatności po 90 dniach; −13,5 i −32,3 tys. zł po 180 dniach.
- Naprawić zwroty (wariant A, najlepszy): wynik +3,0 tys. zł albo −23,2 tys. zł po 90 dniach; +1,4 i −24,7 tys. zł po 180 dniach. Przeglądarki wbudowane w aplikacje nie dają w tym rachunku nic.
- Wyłączyć: przy 100% pacjentów dodatkowych +11,9 do +30,8 tys. zł (+18,6 do +48,0 na pełny rok) po 90 dniach i +13,5 do +32,3 tys. zł (+21,0 do +50,4 na pełny rok) po 180 dniach; przy 0% +82,5 tys. zł (+128,6).

**Propozycja:**
- Wstrzymać od razu, jako odwracalną pauzę. W przyjętych scenariuszach wyłączenie poprawia wynik w każdej regule, każdym oknie i każdym wariancie dodatkowości, a naprawa przy pełnym budżecie w najlepszym razie doprowadza wynik do zera. W dojrzałej próbie 180 dni wynik na pacjenta według przyjętej reguły to −1,1 zł z warunkowym przedziałem od −5,3 do +3,0 zł (299 pacjentów), więc strata na pacjenta jest niewielka, a pewny jest tylko brak korzyści.
- Naprawy (obietnica, ładowanie strony) sprawdzamy na Meta. TikTok może wrócić jako mały test, jeśli zadziałają.

**Po czym poznamy:**
Zmianę po pauzie porównujemy z ustalonym z góry punktem odniesienia (te same tygodnie rok wcześniej i kanały bez zmian): marża całego biznesu po wydatkach rośnie, a łączna liczba nowych pacjentów spada mniej niż liczba pacjentów przypisanych dotąd TikTokowi. Sam wzrost marży po pauzie nie dowodzi skutku, bo może wynikać z sezonu. Pauza daje przy okazji słaby, darmowy pomiar dodatkowości.

**Wdrożenie:**
1 dzień.

*Kampania TikTok na L4: kwoty z 234 dni działania, pod spodem pełny rok (×1,56)*

|  | Przyjęta reguła, 90 dni | Przyjęta reguła, 180 dni | Sesja płatności, 90 dni | Sesja płatności, 180 dni |
| --- | --- | --- | --- | --- |
| Wynik kampanii dziś | −11,9 tys. zł<br>pełny rok: −18,6 tys. zł | −13,5 tys. zł<br>pełny rok: −21,0 tys. zł | −30,8 tys. zł<br>pełny rok: −48,0 tys. zł | −32,3 tys. zł<br>pełny rok: −50,4 tys. zł |
| Wynik po naprawie zwrotów (wariant A) | +3,0 tys. zł<br>pełny rok: +4,6 tys. zł | +1,4 tys. zł<br>pełny rok: +2,2 tys. zł | −23,2 tys. zł<br>pełny rok: −36,2 tys. zł | −24,7 tys. zł<br>pełny rok: −38,6 tys. zł |
| Zmiana marży po wyłączeniu: 100% pacjentów dodatkowych | +11,9 tys. zł<br>pełny rok: +18,6 tys. zł | +13,5 tys. zł<br>pełny rok: +21,0 tys. zł | +30,8 tys. zł<br>pełny rok: +48,0 tys. zł | +32,3 tys. zł<br>pełny rok: +50,4 tys. zł |
| Zmiana marży po wyłączeniu: 50% pacjentów dodatkowych | +47,2 tys. zł<br>pełny rok: +73,6 tys. zł | +48,0 tys. zł<br>pełny rok: +74,8 tys. zł | +56,6 tys. zł<br>pełny rok: +88,3 tys. zł | +57,4 tys. zł<br>pełny rok: +89,5 tys. zł |
| Zmiana marży po wyłączeniu: 0% pacjentów dodatkowych | +82,5 tys. zł<br>pełny rok: +128,6 tys. zł | +82,5 tys. zł<br>pełny rok: +128,6 tys. zł | +82,5 tys. zł<br>pełny rok: +128,6 tys. zł | +82,5 tys. zł<br>pełny rok: +128,6 tys. zł |

Zobacz w danych: Wynik biznesu: ekonomia kampanii, obie reguły · Kohorty: nowe kampanie na L4 i pozostałe · Zdarzenie na osi: start TikToka

*Skąd liczby: analiza/wyniki/c_priorytety.txt (P3, P11), analiza/wyniki/a5e_scenariusze.txt (E1, E3, E3b), analiza/wyniki/a5e_kampanie.csv, notatki/a5_ekonomia.md.*

*↑ Wróć do przeglądu*

### 4. Wstrzymać gs_generic_specjalisci (Google Ads ogólne na specjalistów) do czasu zmiany cennika

*Ile warte rocznie: +19,4 do +31,5 tys. zł przy 100% pacjentów dodatkowych, do +53,2 tys. zł · Pewność: wysoka co do znaku · Wdrożenie: 1 dzień*

**Z danych:**
- Wynik na pacjenta jest ujemny w obu regułach i obu oknach: −23,7 i −44,7 zł po 90 dniach, −14,3 i −36,6 zł po 180 dniach.
- Koszt pozyskania wynosi 57,6 zł (przyjęta reguła) albo 80,9 zł (sesja płatności) przy marży pacjenta przed kosztem pozyskania 32–37 zł.
- Jednym z głównych ograniczeń marży jest cennik: wizyta u specjalisty po cenie katalogowej zostawia tylko 9–19 zł ponad koszt lekarza (pozycja 10). Wynik zależy też od kosztu pozyskania, struktury usług i powrotów.

**Naprawić albo wyłączyć:**
- Rocznie 923 nowych pacjentów według przyjętej reguły, 657 według sesji płatności, wydatki 53,2 tys. zł.
- Dziś: −23,2 tys. zł i −31,5 tys. zł po 90 dniach; −19,4 i −30,2 tys. zł po 180 dniach (bez pośredniego zaokrąglania marży).
- Naprawić: sama kampania musiałaby obniżyć koszt pozyskania o 40–60%, a to inny model kampanii, nie naprawa. Główną drogą naprawy jest cennik (pozycja 10). Uwaga: awaria Safari od 17.03 zawyża koszt pozyskania także tej kampanii.
- Wyłączyć: +19,4 do +31,5 tys. zł przy 100% pacjentów dodatkowych, +36,3 do +42,4 tys. zł przy 50%, +53,2 tys. zł przy 0%. Założenia: pacjenci dodatkowi mają średnią marżę przypisanych, pozostali zachowują się jak dziś, koszty pozostałych kanałów się nie zmieniają.

**Propozycja:**
Wstrzymać. Wrócić po zmianie cennika albo gdy koszt pozyskania nie przekracza marży pacjenta w 90 dniach w obu regułach.

**Po czym poznamy:**
Marża po wydatkach rośnie, a nowych pacjentów u specjalistów z pozostałych kanałów nie ubywa więcej, niż kampania przypisywała.

**Wdrożenie:**
1 dzień.

*Kampania gs_generic_specjalisci: kwoty roczne z okresu 2*

|  | Przyjęta reguła, 90 dni | Przyjęta reguła, 180 dni | Sesja płatności, 90 dni | Sesja płatności, 180 dni |
| --- | --- | --- | --- | --- |
| Wynik kampanii dziś | −23,2 tys. zł | −19,4 tys. zł | −31,5 tys. zł | −30,2 tys. zł |
| Zmiana marży po wyłączeniu: 100% pacjentów dodatkowych | +23,2 tys. zł | +19,4 tys. zł | +31,5 tys. zł | +30,2 tys. zł |
| Zmiana marży po wyłączeniu: 50% pacjentów dodatkowych | +38,2 tys. zł | +36,3 tys. zł | +42,4 tys. zł | +41,7 tys. zł |
| Zmiana marży po wyłączeniu: 0% pacjentów dodatkowych | +53,2 tys. zł | +53,2 tys. zł | +53,2 tys. zł | +53,2 tys. zł |

Zobacz w danych: Wynik biznesu: ekonomia kampanii (poziom: kampanie) · Kohorty: pacjenci tej kampanii według pierwszej usługi

*Skąd liczby: analiza/wyniki/c_priorytety.txt (P7), analiza/wyniki/a5e_kampanie.csv, analiza/wyniki/c_telemedigo.txt (3a), notatki/ZALOZENIA.md (punkt 42).*

*↑ Wróć do przeglądu*

### 5. Uczciwa obietnica w reklamach L4 Meta i na stronie wejścia: mniej zwrotów po wizycie

*Ile warte rocznie: 18,1–46,5 tys. zł (przyjęta reguła), 10,7–26,7 tys. zł (sesja płatności), pełny rok · Pewność: średnia: nie znamy powodu zwrotów · Wdrożenie: 1–2 tygodnie + 4–6 tygodni pomiaru*

**Z danych:**
- 17,4% odbytych wizyt L4 pacjentów nowych kampanii kończy się zwrotem po wizycie (1 024 z 5 895), wobec 5,3% L4 pozostałych pacjentów (5 080 wizyt) w okresie 2.
- Kod rabatowy ani opóźnienie wizyty nie zmieniają tego odsetka. Za zwróconą wizytę lekarz dostaje wynagrodzenie.

**Ile warta po wstrzymaniu TikToka (tylko Meta):**
- 18,1–46,5 tys. zł rocznie według przyjętej reguły i 10,7–26,7 tys. zł według sesji płatności, na pełny rok (w 332 dniach działania: 16,5–42,3 i 9,7–24,3 tys. zł).
- Wynik po 180 dniach jest taki sam, bo ci pacjenci prawie nie wracają. Jeśli test (pozycja 9) pokaże, że Meta trzeba wyłączyć, ta pozycja jest warta zero.

**Założenia i zastrzeżenia:**
- Dolny wariant zakłada, że uczciwa reklama odstrasza tylko tych, którzy i tak dostaliby zwrot. W praktyce odstraszy też część pozostałych, więc może być niżej.
- Górny wariant („wizyta zostaje opłacona”) może wymagać zmiany zasad zwrotów, a nie samej treści reklamy. To osobna decyzja z ryzykiem prawnym i wizerunkowym.
- 5,3% to odsetek z innej grupy pacjentów, więc pełne zrównanie jest optymistyczne. Rozsądny wariant bazowy to zmniejszenie luki o połowę.

**Co robimy:**
- Najpierw jednodniowe sprawdzenie, co obiecują reklama, strona /zwolnienie-l4-online i regulamin przy odmowie L4.
- Potem nowa kreacja i pytanie przed płatnością („lekarz wystawia L4 tylko przy wskazaniach medycznych”).
- W Meta losowy podział ruchu na starą i nową kreację, z osobnym oznaczeniem kampanii.

**Po czym poznamy:**
Odsetek zwrotów po wizycie L4 przy nowej kreacji spada wobec starej, a marża na kliknięcie nie spada. Liczy się marża, nie sam odsetek zwrotów.

**Wdrożenie:**
1–2 tygodnie zmian i 4–6 tygodni pomiaru.

Zobacz w danych: Po zakupie: zwroty po wizycie według celu wizyty · Zdarzenie na osi: więcej pierwszych zamówień zwracanych po wizycie

*Skąd liczby: analiza/wyniki/c_priorytety.txt (P2, P11), analiza/wyniki/a5e_scenariusze.txt (E2a), analiza/wyniki/a5r_po_zakupie.txt (2b, 2d).*

*↑ Wróć do przeglądu*

### 6. Poranna obsada internistów: diagnoza, potem test

*Ile warte rocznie: scenariusz od 0 do 65 tys. zł, koszt obsady nieznany · Pewność: niska co do kwoty · Wdrożenie: diagnoza 1–2 dni, test 2–4 tygodnie*

**Z danych:**
- Od listopada 2025 poranne opóźnienia u internisty rosną z miesiąca na miesiąc. Odsetek wizyt z terminem 6:00–11:59, które zaczynają się ponad 15 minut po terminie, wynosi 15,6% w listopadzie 2025 (572 wizyty), 29,7% w grudniu i 41,8% w styczniu 2026, a od lutego do września 2026 około połowy (48,4–52,6% miesięcznie). Od października 2024 do października 2025 było to 4,7–6,9% miesięcznie (wszyscy pacjenci).
- Przy tym samym porannym ruchu opóźnień jest o 26,4 punktu procentowego więcej (5 przedziałów ruchu, 9 979 wizyt).
- Długość porannej wizyty się nie zmieniła (8,5 minuty w obu okresach), więc dłuższe wizyty tego nie tłumaczą.
- Wizyty spóźnione ponad 30 minut mają średnią ocenę 2,92 wobec 4,45 przy punktualnych (okres 2, internista, pacjenci spoza nowych kampanii, 469 i 3 446 ocen). Rano spada powrót po wizytach spóźnionych.

**Dlaczego wysoko:**
To jedna z konkretnych hipotez poprawy retencji pacjentów z kanałów działających w obu latach (obok komunikacji po wizycie i zniżek), a pierwszy krok, diagnoza, jest tani.

**Ile warta:**
Scenariusz od 0 zł do 65,2 tys. zł marży rocznie w horyzoncie 180 dni. Związek opóźnień z powrotami może częściowo wynikać z tego, kto przychodzi rano, więc kwota jest niepewna. Kosztu dodatkowej obsady nie ma w danych.

**Co robimy:**
- Diagnoza: grafiki i obsada poranna przed i po 3.11.2025, obciążenie lekarzy pacjentami spoza B2C, rozmowa z osobami od grafików.
- Potem naprawy, także bez dodatkowej obsady: liczba porannych terminów dopasowana do przepustowości, przesunięcie godzin lekarzy, realny czas oczekiwania pokazany pacjentowi.
- Na końcu test w losowo wybrane dni.

**Po czym poznamy:**
Odsetek porannych wizyt spóźnionych ponad 15 minut spada z około 50% poniżej 10%, oceny porannych wizyt rosną, a powrót w 90 dniach pacjentów z pierwszą wizytą rano, z tego samego źródła, wraca w stronę 23–24% (w okresie 1: 23,6%, 2 844 pacjentów kampanii działających w obu latach).

**Wdrożenie:**
Diagnoza 1–2 dni, test 2–4 tygodnie, efekt w powrotach po 90 dniach.

Zobacz w danych: Po zakupie: punktualność według pory i opóźnienia przy tym samym ruchu · Zdarzenie na osi: poranne opóźnienia u internisty

*Skąd liczby: analiza/wyniki/a5r_punktualnosc.txt (1c, 2b, 3f), analiza/wyniki/a5r_po_zakupie.txt (3a), analiza/wyniki/c_priorytety.txt (P8, P13), notatki/a5_retencja.md.*

*↑ Wróć do przeglądu*

### 7. Komunikacja po wizycie z losową grupą kontrolną (retencja)

*Ile warte rocznie: scenariusz: 23,6 tys. zł za każdy punkt procentowy powrotu w 90 dniach · Pewność: niska co do kwoty · Wdrożenie: dane o wysyłkach dni, sekwencja 2–4 tygodnie, pomiar 90 dni*

**Z danych:**
- Retencja to połowa definicji wzrostu, a spada także bez pacjentów nowych kampanii: powrót w 90 dniach 22,0% (14 031 pacjentów) wobec 23,9% (12 867).
- Po wejściu z newslettera albo SMS-a wraca w okresie 2 3,16% pacjentów spoza nowych kampanii, a bez takiego wejścia 18,84%, więc to około 14% obserwowanych pierwszych powrotów (14 031 pacjentów kampanii działających w obu latach).
- Liczba wejść z newslettera i SMS-ów na 1 000 pacjentów spada z 56–108 miesięcznie w okresie 1 do 24–52 w okresie 2, ale mianownikiem jest cała narastająca baza pacjentów; w pierwszych 90 dniach od zakupu odsetek pacjentów z takim wejściem rośnie lekko z 17,5% do 17,9%. Widać kliknięcia, a nie wysyłki.

**Ile warta:**
Scenariusz: każdy punkt procentowy powrotu w 90 dniach to około 23,6 tys. zł marży rocznie (24 687 nowych pacjentów × 1% × 95,6 zł), a bez pacjentów nowych kampanii 16,7 tys. zł. To różnica obserwacyjna, a nie zmierzony efekt wiadomości.

**Co robimy:**
- Dane o wysyłkach: ile, komu, kiedy.
- Sekwencja po pierwszej wizycie (przypomnienie o kontynuacji leczenia, recepta, kontrola), zawsze z losową grupą kontrolną bez wysyłki.

**Po czym poznamy:**
Różnica powrotu w 90 dniach i marży między grupą z wysyłką a grupą kontrolną.

**Wdrożenie:**
Dane o wysyłkach kilka dni, sekwencja 2–4 tygodnie, pomiar 90 dni.

Zobacz w danych: Kohorty: powrót bez pacjentów nowych kampanii · Kohorty: powrót według źródła pozyskania

*Skąd liczby: analiza/wyniki/c_priorytety.txt (W2, P12), analiza/wyniki/a5r_po_zakupie.txt (5e), notatki/a5_retencja.md (krok 4c).*

*↑ Wróć do przeglądu*

### 8. Sprawdzić ręcznie zakup dla pacjentów zalogowanych od wejścia

*Ile warte rocznie: 0 albo 36–40 tys. zł (wysoki scenariusz 89 tys. zł) · Pewność: niska: dane wskazują raczej na 0 zł · Wdrożenie: 1 dzień*

**Z danych:**
- 22 068 sesji zalogowanych od wejścia przez dwa lata nie kończy się ani razu zakupem konsultacji, a każdy z 22 289 zakupów powtórnych ma krok logowania.
- Dane nie rozstrzygają między odczytaniami: (A) wizyty „sprawdzam konto” albo sposób zapisu (logowanie zaczyna nową sesję) albo (B) zepsuta ścieżka zakupu dla zalogowanych. Kilka faktów przemawia za A.

**Ile warta:**
W odczytaniu A 0 zł dla przychodu (ale wtedy cierpi pomiar lejka, pozycja 2). W odczytaniu B scenariusze: około 40 tys. zł rocznie na sesjach, około 36 tys. zł na pacjentach, wysoki scenariusz 89 tys. zł.

**Po czym poznamy:**
Test daje odpowiedź od razu. Jeśli ścieżka jest zepsuta, po naprawie sesje zalogowane od wejścia zaczynają kończyć się płatnością.

**Wdrożenie:**
1 dzień, w pierwszym tygodniu niezależnie od miejsca na liście.

Zobacz w danych: Lejek: sesje zalogowane od wejścia

*Skąd liczby: analiza/wyniki/c_priorytety.txt (P5), analiza/wyniki/a5p_zalogowane.txt, notatki/a5_pozyskanie.md (sekcja 3).*

*↑ Wróć do przeglądu*

### 9. Meta na L4: test dodatkowości w parach województw, z progiem decyzji

*Ile warte rocznie: decyzja warta od −30,6 (90 dni) albo −32,9 (180 dni) do +179,6 tys. zł, pełny rok · Pewność: — (to jest test) · Wdrożenie: 1 tydzień + 4–6 tygodni*

**Z danych:**
- Wynik kampanii zależy od reguły źródła: +27,8 tys. zł według przyjętej reguły i −28,7 tys. zł według sesji płatności po 90 dniach, w 332 dniach działania (+30,6 i −31,6 tys. zł na pełny rok).
- Dane nie rozstrzygają, ilu jej pacjentów przyszłoby i bez niej.

**Naprawić albo wyłączyć:**
- Naprawić zwroty: pozycja 5, w tej samej kampanii.
- Wyłączyć: od −30,6 tys. zł (wszyscy pacjenci dodatkowi, horyzont 90 dni) albo −32,9 tys. zł (180 dni) do +179,6 tys. zł (żaden) na pełny rok.

**Próg decyzji, ustalony przed testem:**
Według przyjętej reguły wyłączenie traci pieniądze tylko wtedy, gdy ponad około 85% pacjentów kampanii jest dodatkowych: 85,4% w horyzoncie 90 dni i 84,5% w horyzoncie 180 dni. Według sesji płatności wyłączenie zyskuje zawsze.

**Projekt testu:**
- Na 4–6 tygodni wyłączyć kampanię w połowie województw, łącząc je w pary podobne wielkością i trendem i losując w parach.
- Wskaźnik główny: wszyscy nowi pacjenci i marża w województwie, a nie pacjenci przypisani Meta.
- Budżetu z wyłączonych województw nie przesuwać.
- Przy okazji mierzyć poranne opóźnienia u internisty (pozycja 6).
- Test kosztuje najwyżej około 1,6–1,8 tys. zł utraconej marży, jeśli wszyscy pacjenci są dodatkowi. Uzupełnienie: badanie przyrostu konwersji w panelu Meta.

**Po czym poznamy:**
Spadek nowych pacjentów w województwach bez reklamy wobec liczby pacjentów przypisanych Meta: poniżej progu 85% wyłączamy, powyżej zostawiamy.

**Wdrożenie:**
Tydzień przygotowania i 4–6 tygodni testu. Wynik może się nie przenieść z jesieni na lato.

*Kampania Meta na L4: kwoty z 332 dni działania, pod spodem pełny rok (×1,10)*

|  | Przyjęta reguła, 90 dni | Przyjęta reguła, 180 dni | Sesja płatności, 90 dni | Sesja płatności, 180 dni |
| --- | --- | --- | --- | --- |
| Wynik kampanii dziś | +27,8 tys. zł<br>pełny rok: +30,6 tys. zł | +29,9 tys. zł<br>pełny rok: +32,9 tys. zł | −28,7 tys. zł<br>pełny rok: −31,6 tys. zł | −27,5 tys. zł<br>pełny rok: −30,2 tys. zł |
| Wynik po naprawie zwrotów (wariant A) | +70,1 tys. zł<br>pełny rok: +77,1 tys. zł | +72,1 tys. zł<br>pełny rok: +79,3 tys. zł | −4,5 tys. zł<br>pełny rok: −4,9 tys. zł | −3,2 tys. zł<br>pełny rok: −3,5 tys. zł |
| Zmiana marży po wyłączeniu: 100% pacjentów dodatkowych | −27,8 tys. zł<br>pełny rok: −30,6 tys. zł | −29,9 tys. zł<br>pełny rok: −32,9 tys. zł | +28,7 tys. zł<br>pełny rok: +31,6 tys. zł | +27,5 tys. zł<br>pełny rok: +30,2 tys. zł |
| Zmiana marży po wyłączeniu: 50% pacjentów dodatkowych | +67,7 tys. zł<br>pełny rok: +74,5 tys. zł | +66,7 tys. zł<br>pełny rok: +73,4 tys. zł | +96,0 tys. zł<br>pełny rok: +105,6 tys. zł | +95,4 tys. zł<br>pełny rok: +104,9 tys. zł |
| Zmiana marży po wyłączeniu: 0% pacjentów dodatkowych | +163,3 tys. zł<br>pełny rok: +179,6 tys. zł | +163,3 tys. zł<br>pełny rok: +179,6 tys. zł | +163,3 tys. zł<br>pełny rok: +179,6 tys. zł | +163,3 tys. zł<br>pełny rok: +179,6 tys. zł |

Zobacz w danych: Wynik biznesu: ekonomia kampanii, obie reguły · Kohorty: nowe kampanie na L4 i pozostałe · Zdarzenie na osi: start kampanii Meta na L4

*Skąd liczby: analiza/wyniki/c_priorytety.txt (P4, P11), analiza/wyniki/a5e_scenariusze.txt (E1, E3, E3b), notatki/a5_ekonomia.md.*

*↑ Wróć do przeglądu*

### 10. Cennik specjalistów i warunki TelemediGO u specjalistów

*Ile warte rocznie: TelemediGO: scenariusze 15–31 tys. zł po pełnym roku (w pierwszym około połowa); cennik: do 73,6 tys. zł za każde 10 zł podwyżki przy tej samej liczbie wizyt (górna granica) · Pewność: wysoka co do kierunku, niska co do kwoty cennika · Wdrożenie: 1–2 tygodnie + test dwóch cen 4 tygodnie*

**Z danych:**
- Po cenie katalogowej wizyta zostawia ponad koszt lekarza tylko 9 zł (dermatolog, kardiolog, neurolog, urolog: 109 zł) albo 19 zł (endokrynolog, ginekolog: 119 zł).
- Pediatra (95 zł) i psycholog (99 zł) mają cenę niższą niż koszt lekarza 100 zł (przy przyjętym koszcie pediatry jak u specjalisty).
- Po zniżce TelemediGO 20% cena jest niższa niż koszt lekarza u wszystkich specjalistów poza psychiatrą. W okresie 2 te wizyty przyniosły 14,7 tys. zł straty na 1 512 zamówieniach.
- To wspólna przyczyna strat w TelemediGO u specjalistów i w kampanii na specjalistów (pozycja 4).

**Ile warta:**
- Warunki TelemediGO: scenariusze 14,7 / 18,9 / 31,4 tys. zł rocznie (znikają wszystkie te wizyty / tylko te ze stratą / wszystkie zostają po cenie katalogowej). 31,4 tys. zł to scenariusz, a nie górna granica: przy osobnej reakcji przy każdym zamówieniu wynik mieści się między 10,9 a 35,2 tys. zł. Wszystkie pomijają zmianę sprzedaży członkostw.
- Założenie planistyczne (bez osobnego rachunku): w pierwszym roku efekt to około połowa, bo obecni członkowie mają stare warunki do końca ważności.
- Cennik: każde 10 zł podwyżki przy tej samej liczbie wizyt to do 73,6 tys. zł rocznie (7 363 opłacone wizyty w okresie 2), a przy utrzymaniu zniżki TelemediGO 20% na 1 425 z nich 70,8 tys. zł. To górna granica, bo nie znamy reakcji pacjentów na cenę.

**Warianty:**
- Zniżka u specjalistów ustawiona tak, żeby cena nie spadała poniżej kosztu lekarza (najwyżej około 8% przy 109 zł, bez zniżki u pediatry i psychologa).
- Test dwóch cen dla nowych pacjentów przez 4 tygodnie, mierzony marżą na sesję, a nie odsetkiem kupujących.

**Po czym poznamy:**
Marża wizyt u specjalistów (z członkami i bez) jest nieujemna, a sprzedaż TelemediGO nie spada bardziej niż ustalony z góry próg.

**Wdrożenie:**
Zmiana regulaminu i kasy 1–2 tygodnie; test cen 4 tygodnie.

*Cennik z danych: marża na wizycie odbytej, bez zniżki i ze zniżką TelemediGO*

|  | Cena katalogowa | Cena po zniżce TelemediGO | Koszt lekarza | Marża bez zniżki | Marża ze zniżką |
| --- | --- | --- | --- | --- | --- |
| internista | 89 zł | 44,5 zł | 25 zł | +64,0 zł | +19,5 zł |
| pediatra | 95 zł | 76,0 zł | 100 zł | −5,0 zł | −24,0 zł |
| psycholog | 99 zł | 79,2 zł | 100 zł | −1,0 zł | −20,8 zł |
| dermatolog | 109 zł | 87,2 zł | 100 zł | +9,0 zł | −12,8 zł |
| neurolog | 109 zł | 87,2 zł | 100 zł | +9,0 zł | −12,8 zł |
| urolog | 109 zł | 87,2 zł | 100 zł | +9,0 zł | −12,8 zł |
| kardiolog | 109 zł | 87,2 zł | 100 zł | +9,0 zł | −12,8 zł |
| ginekolog | 119 zł | 95,2 zł | 100 zł | +19,0 zł | −4,8 zł |
| endokrynolog | 119 zł | 95,2 zł | 100 zł | +19,0 zł | −4,8 zł |
| psychiatra | 269 zł | 215,2 zł | 200 zł | +69,0 zł | +15,2 zł |

Zobacz w danych: Kohorty: powrót i marża według pierwszej usługi · Kohorty: kupujący TelemediGO przy pierwszym zakupie

*Skąd liczby: analiza/wyniki/c_telemedigo.txt (3a–3c), analiza/wyniki/c_priorytety.txt (P6, P14), notatki/ZALOZENIA.md (punkt 33).*

*↑ Wróć do przeglądu*

### 11. Sprawdzić stratę między kliknięciem reklamy a sesją w Meta i TikToku

*Ile warte rocznie: 0 albo do 52 tys. zł (górna granica, po wstrzymaniu TikToka mniej) · Pewność: niska · Wdrożenie: 1–2 dni*

**Z danych:**
Na kliknięcie przypada 0,92–0,93 sesji w Google Ads, 0,79–0,82 w Meta i 0,72 w TikToku, stale w każdym kwartale.

**Ile warta:**
- 0 zł, jeśli plik wydatków liczy wszystkie kliknięcia (także te, które nie prowadzą na stronę).
- Jeśli ludzie porzucają stronę, zanim się załaduje, i da się to odzyskać: do 52 tys. zł rocznie (górna granica: 23 776 brakujących sesji i do 1 434 zamówień w okresie 2). Po wstrzymaniu TikToka mniej. Realnie raczej ułamek, bo porzucający są mniej zdecydowani.

**Po czym poznamy:**
W panelach porównać kliknięcia w link i wyświetlenia strony docelowej z sesjami, dzień po dniu; czas ładowania w przeglądarkach wbudowanych. Wynik zmienia ocenę pozycji 3 i 9.

**Wdrożenie:**
1–2 dni, w pierwszym tygodniu.

Zobacz w danych: Lejek: sesje kampanii Meta i TikToka dzień po dniu

*Skąd liczby: analiza/wyniki/a2_jakosc.txt (3c), analiza/wyniki/c_priorytety.txt (P9), analiza/wyniki/a5p_lejek.txt (6b), notatki/a5_pozyskanie.md (sekcja 5).*

*↑ Wróć do przeglądu*

### 12. Test TelemediGO z losowym, bezpłatnym dostępem do zniżek

*Ile warte rocznie: decyduje o roli programu; koszt testu 3–12 tys. zł · Pewność: — (to jest test) · Wdrożenie: 2–8 tygodni + 90 dni*

**Z danych:**
- Nie wiemy, czy TelemediGO podnosi powroty, czy tylko przyciąga pacjentów, którzy i tak wracają. Kupujący przy pierwszym zamówieniu wracają w 90 dniach w 34,7% wobec 20,0% podobnych pacjentów (okres 2, 858 kupujących), ale ta różnica łączy wpływ zniżki i to, kto kupuje.
- Zniżki przewyższają opłatę średnio o 15,6 zł na członkostwo (członkostwa z okresu 1, przy założeniu, że te same wizyty odbyłyby się i bez TelemediGO), więc program opłaca się tylko wtedy, gdy dokłada wizyt.

**Ile warta:**
- Decyduje, czy program promować (sprzedaż, przypomnienie o odnowieniu; dziś odnawia około 5% członków: 62 z 1 140 w 90 dniach po wygaśnięciu), czy przebudować razem z pozycją 10.
- Dodatkowy koszt testu to około 3,3–12,2 tys. zł zniżek.

**Zastrzeżenie:**
Darmowy dostęp mierzy wpływ zniżki, a nie opłacalność oferty za 89 zł. Losowanie samej oferty przy kasie mierzyłoby decyzję biznesową, ale przy 4,5% kupujących potrzebuje ponad 4 lat pozyskania. Wskaźnikiem głównym jest marża na pacjenta.

**Po czym poznamy:**
Różnica powrotu w 90 dniach i marży między grupą z dostępem a grupą bez niego.

**Wdrożenie:**
- 2–8 tygodni na losowe przydzielenie (487–1 823 pacjentów na grupę, czyli do około 1,8 miesiąca pozyskania), potem 90 dni obserwacji.
- Liczebność wyznaczyliśmy dla różnicy powrotu; przed startem trzeba ustalić najmniejszą istotną biznesowo zmianę marży i sprawdzić, jakiej próby wymaga.

Zobacz w danych: Kohorty: kupujący TelemediGO przy pierwszym zakupie i pozostali

*Skąd liczby: analiza/wyniki/c_telemedigo.txt (1d, 2a, 4a, 4d), analiza/wyniki/c_priorytety.txt (P10).*

*↑ Wróć do przeglądu*

### Czego proponujemy teraz nie robić

- Zgoda marketingowa pacjentów nowych kampanii: w najlepszym odczytaniu 1,9 tys. zł rocznie.
- Przeglądarki wbudowane w aplikacje w nowych kampaniach: w tym rachunku 0 zł, bo konwersja nie jest tam niższa. W pozostałych kampaniach sprawa jest otwarta (pomiar w pozycji 2).
- Mocniejsza sprzedaż i odnowienia TelemediGO: dopiero po teście z pozycji 12.
- Przesuwanie uwolnionego budżetu do innych kampanii bez testu (zasada budżetu).

*Notatka: notatki/c_szkic.md, sekcja 3. Liczby: analiza/c_priorytety.py → analiza/wyniki/c_priorytety.txt, analiza/c_telemedigo.py → analiza/wyniki/c_telemedigo.txt i raporty części A5, wskazane przy każdej pozycji. Kolejność i wyceny sprawdziła niezależnie runda kilku modeli AI różnych firm (notatki/konsylium/c_priorytety/synteza.md), a liczby drugi model (notatki/recenzje/c_codex.md).*

# Zakładka 9: Czego nie wiemy (`#niewiadome`)

## Czego z tych danych nie wiemy

Rzeczy, których te dane nie rozstrzygają. Przy każdej: dlaczego to ważne i jaki test albo jakie dane by to domknęły. Kwoty to zmiana marży na rok, jak w zakładce „Priorytety”.

| Nr | Czego nie wiemy | Dlaczego to ważne | Test albo brakujące dane | Pozycja listy priorytetów |
| --- | --- | --- | --- | --- |
| 1 | Czy pacjenci nowych kampanii na L4 są dodatkowi | od tego zależy decyzja o Meta na L4: od −30,6 tys. zł (90 dni) albo −32,9 tys. zł (180 dni) do +179,6 tys. zł na pełny rok (pozycja 9; próg decyzji około 85% pacjentów dodatkowych: 85,4% w 90 dniach i 84,5% w 180 dniach) | wyłączenie kampanii w losowej połowie województw na 4–6 tygodni; badanie przyrostu w panelach Meta i TikToka | pozycja 9 |
| 2 | Która reguła źródła jest bliższa prawdy dla kampanii bez kodu (Google Ads ogólne, Meta lekarz online) | znak wyniku tych kampanii zależy od reguły | ten sam test z grupą kontrolną bez reklamy | — |
| 3 | Powód zwrotów po wizycie L4 w nowych kampaniach (17,4% wobec 5,3%) | po wstrzymaniu TikToka dotyczy tylko Meta: od niego zależy, czy naprawa jest bliżej górnego, czy dolnego wariantu z pozycji 5, czyli 18,1–46,5 tys. zł według przyjętej reguły i 10,7–26,7 tys. zł według sesji płatności na pełny rok | powód zwrotu, decyzja lekarza (czy L4 wystawiono), treść reklam | pozycja 5 |
| 4 | Dlaczego spadła poranna przepustowość internistów i czy opóźnienia obniżają powroty | scenariusz od 0 do 65 tys. zł rocznie; luty 2026 nie pasuje do prostej hipotezy | grafiki i obsada poranna przed i po 3.11.2025, obciążenie lekarzy pacjentami spoza B2C, koszt obsady; test z dodatkową poranną obsadą w losowe dni | pozycja 6 |
| 5 | Sesje zalogowane od wejścia: wizyty „sprawdzam konto” czy zepsuta ścieżka | 0 albo około 36–40 tys. zł rocznie (wysoki scenariusz 89 tys. zł) | ręczny test zakupu po zalogowaniu; logi błędów; znacznik „zalogowany na wejściu” w analityce | pozycja 8 |
| 6 | Przyczyna awarii zakładania konta w Safari na iOS od 17.03.2026 | potrzebna do naprawy (pozycja 1) | lista zmian w produkcie z 16–17.03.2026, logi rejestracji według przeglądarki, powtórzenie na iPhonie | pozycja 1 |
| 7 | Czy utraceni w Safari na iOS kupili na innym urządzeniu | zmienia wartość pozycji 1 | powiązanie urządzeń po adresie e-mail albo numerze telefonu przy próbie rejestracji | pozycja 1 |
| 8 | Czy TelemediGO podnosi powroty, czy tylko przyciąga pacjentów, którzy i tak wracają | decyduje o tym, czy program promować | losowy, bezpłatny dostęp do zniżek (pozycja 12) | pozycja 12 |
| 9 | Czy newsletter i SMS wywołują zakup | to kanał, którego dodatkowy wpływ warto przetestować (około 14% obserwowanych pierwszych powrotów idzie po wejściu z niego); widać kliknięcia, nie wysyłki; wejść na 1 000 pacjentów całej narastającej bazy jest coraz mniej (z 56–108 do 24–52 miesięcznie) | liczba wysyłek; losowa grupa kontrolna bez wysyłki | pozycja 7 |
| 10 | Wartość remarketingu porzuconego koszyka | przyjęta reguła z definicji przypisuje mu mało pacjentów | grupa kontrolna, której remarketing się nie wyświetla | — |
| 11 | Sezon a wydatki na kampanie | wzrostu od X 2024 do I 2025 nie da się rozdzielić; dwa lata to jedna zima i jedno lato w roku | zmiana budżetu w części kraju (grupa kontrolna według województw) | — |
| 12 | Strata między kliknięciem reklamy a sesją w Meta i TikToku | od 0 do 52 tys. zł rocznie | panele reklamowe, logi serwera, czas ładowania strony w przeglądarkach wbudowanych | pozycja 11 |
| 13 | Prawdziwa stawka lekarza u pediatry (przyjęte 100 zł) | przy 100 zł pediatra przynosi stratę nawet bez zniżki; przy 25 zł marża na pacjenta w 90 dniach rośnie o 3,7–4,8 zł | stawka z umów z lekarzami | pozycja 10 |
| 14 | Koszt lekarza za wizyty testowe (51 775 zł według zasady z zadania, łącznie w obu okresach; 37 950 zł w okresie 2) | wynik biznesu | informacja z rozliczeń, czy lekarze dostali wynagrodzenie za testy | pozycja 2 |
| 15 | Warunki umowy z rankingiem lekarzy | prowizja 30,8 tys. zł za dwa lata według naszej reguły albo 14,9 tys. zł według kodu | umowa z rankingiem | — |
| 16 | Pełna długoterminowa marża rocznika okresu 2 | rachunek kampanii w 90 i 180 dniach jej nie obejmuje; zaniża wartość kampanii z powracającymi pacjentami | czas; najstarsze kohorty pozwalają już częściowo ją ocenić (5 137 pacjentów okresu 2 ma pełne 270 dni obserwacji) | — |
| 17 | Reakcja pacjentów na cenę u specjalistów | od niej zależy, ile da zmiana cennika (do 73,6 tys. zł za 10 zł podwyżki) | test dwóch cen dla nowych pacjentów przez 4 tygodnie | pozycja 10 |
| 18 | Zasady zwrotów przy odmowie L4 i ryzyko prawne reklam L4 | górny wariant pozycji 5 może wymagać zmiany zasad zwrotów | regulamin, opinia prawna, treść reklam | pozycja 5 |

*Notatka: notatki/c_szkic.md, sekcja 4. Liczby: analiza/wyniki/c_priorytety.txt (P4, P5, P8, P9, P11, P14), analiza/wyniki/a5r_po_zakupie.txt (2b, 5e), analiza/wyniki/a5r_kohorty.txt (7), analiza/wyniki/a2_jakosc.txt (2e), analiza/wyniki/a5e_ekonomia.txt.*

---

**Stopka strony:** Dane od 1.10.2024 do 30.09.2026. Liczby przeliczone 2026-10-21 19:47 skryptami analiza/b_eksport.py i analiza/b2_eksport_c.py (stan repozytorium efdd8e2). Strona nie pobiera niczego z internetu.
