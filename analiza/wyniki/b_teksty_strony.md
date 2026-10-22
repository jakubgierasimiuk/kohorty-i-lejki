# Teksty strony narzędzia — wszystkie zakładki, tak jak widzi je czytelnik

Wygenerowane 2026-10-22 22:21 skryptem `analiza/b2_teksty_strony.py` ze strony w `narzedzie/` (stan repozytorium 63ddc3d), otwartej w przeglądarce bez okna (Microsoft Edge), szerokość 1366 px. Każda zakładka przy ustawieniach domyślnych, bez klikania. Tabele dłuższe niż 40 wierszy są skrócone do 15 pierwszych i 5 ostatnich wierszy. Rozwijane sekcje są rozwinięte. Wykresy opisane nazwami serii. W komórkach tabel `<br>` oddziela linie, które strona pokazuje jedna pod drugą (zwykle: wartość w okresie B, pod spodem okres A i zmiana). Odnośniki do innych zakładek są oznaczone strzałką albo wypisane po „Zobacz w danych”.

**Nagłówek strony:** B2C: czy to wzrost? — Narzędzie do zadania rekrutacyjnego na stanowisko Head of B2C

**Uwaga na każdej stronie:** Dane są syntetyczne, wygenerowane na potrzeby zadania. Nie opisują prawdziwych pacjentów ani wyników firmy.

**Zakładki:** Czy to wzrost (`#wzrost`), Kohorty (`#kohorty`), Lejek (`#lejek`), Po zakupie (`#po-zakupie`), Zdarzenia (`#zdarzenia`), Wynik biznesu (`#wynik`), Jakość danych (`#jakosc`), Priorytety (`#priorytety`), Czego nie wiemy (`#niewiadome`)

# Zakładka 1: Czy to wzrost (`#wzrost`)

## Czy to, co widać na dashboardzie, jest wzrostem?

Wzrost to dwie rzeczy naraz: więcej pacjentów i lepsza retencja. Sprawdzamy oba warunki osobno, na danych oczyszczonych, porównując ostatnie 12 miesięcy (X 2025 – IX 2026) z rokiem wcześniej (X 2024 – IX 2025).

**Werdykt (znacznik „Nie”):** Pacjentów przybywa, ale wracają rzadziej. Wydatki na kampanie rosną dużo szybciej niż marża, którą biznes zarabia przed ich kosztem.

Za cały rok marża po koszcie lekarza, kampaniach i prowizji wzrosła o 27%: z 828 do 1 048 tys. zł.

- **+52%** [lepiej] nowych pacjentów niż rok wcześniej — bez dwóch nowych kampanii na L4: +7%
- **17%** [gorzej] nowych pacjentów wraca w ciągu 90 dni — rok wcześniej 24%
- **×2,1** [uwaga] wydatki na kampanie w III kwartale 2026 wobec roku wcześniej — marża przed ich kosztem: +25%

### Decyzje na pierwszy tydzień

1. Naprawić zakładanie konta w Safari na iPhone'ach (pozycja 1 · do 83 tys. zł marży rocznie)
2. Wstrzymać kampanię TikTok na L4 i kampanię Google Ads na specjalistów (pozycje 3 i 4 · obie tracą na każdym pacjencie według obu reguł przypisania, a pauzę da się cofnąć w jeden dzień)
3. Oczyścić codzienny raport i dodać alarmy na lejku (pozycja 2 · awaria Safari trwała 198 dni bez alarmu)
4. Zrobić krótkie sprawdzenia: obietnica reklam L4, poranne grafiki internistów, zakup po zalogowaniu, kliknięcia w panelach reklam (pierwsze kroki pozycji 5, 6, 8 i 11 · każde zajmuje dzień albo dwa)

### Więcej pacjentów: Pacjentów przybywa, ale głównie z dwóch nowych kampanii na L4 — znacznik „Tak”

Nowych pacjentów jest o 52% więcej niż rok wcześniej, a bez kampanii Meta i TikTok na L4 tylko o 7%.

*[Wykres] Nowi pacjenci rok wcześniej i w ostatnich 12 miesiącach, w podziale na nowe kampanie na L4 i pozostałe*

- rok wcześniej: pozostałe kampanie i kanały 16 231, nowe kampanie na L4 0, razem 16 231
- ostatnie 12 miesięcy: pozostałe kampanie i kanały 17 419, nowe kampanie na L4 7 268, razem 24 687

*Nowi pacjenci według pierwszego wejścia; długość słupka to liczba pacjentów.*

- 24 687 nowych pacjentów w ostatnich 12 miesiącach wobec 16 231 rok wcześniej.
- Bez pacjentów dwóch nowych kampanii na L4: 17 419. Te kampanie dały 29% nowych pacjentów, a ich pacjent zostawia w 90 dniach 36 zł marży przed kosztem pozyskania wobec 66 zł pozostałych.
- Z kanałów bezpłatnych (wejścia bezpośrednie, bezpłatna wyszukiwarka, program poleceń) przybyło 12% nowych pacjentów, licząc według pierwszego wejścia.

**Zastrzeżenie.** Nie wiemy, ilu pacjentów nowych kampanii przyszłoby i bez nich. Sprawdzi to test z wyłączeniem reklamy w części kraju (pozycja 9 listy priorytetów).

Zobacz w danych: Kohorty: nowi pacjenci według źródła pozyskania *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

- Dokładnie: +52,1% wszystkich nowych pacjentów, +7,3% bez nowych kampanii, +12,1% z kanałów bezpłatnych (z 7 069 do 7 924). Pacjenci nowych kampanii: 7 268 z 24 687 (29%), marża w 90 dniach 36,3 zł wobec 66,0 zł.
- Źródło pacjenta liczymy według pierwszego wejścia: pacjent nowej kampanii to ten, który pierwszy raz wszedł z jej reklamy albo zapłacił z jej kodem rabatowym. Według sesji z płatnością pacjentów bez nowych kampanii jest 19 500, czyli +20,1%. Różnica to 2 081 pacjentów, którzy według pierwszego wejścia należą do nowych kampanii, a według sesji z płatnością do innych kanałów: 1 918 weszło pierwszy raz z reklamy nowej kampanii, a zapłaciło w innej sesji (najczęściej po wejściu bezpośrednim albo z wyszukiwarki), a 163 weszło z innego kanału, ale zapłaciło z kodem nowej kampanii. Wracają tak rzadko jak pozostali pacjenci nowych kampanii. Bez nich oba podziały dają ten sam przyrost pacjentów, ten sam powrót i tę samą marżę, więc pacjentów i retencję opisujemy według pierwszego wejścia. W ekonomii kampanii pokazujemy oba podziały.

Skąd liczby: analiza/wyniki/c_priorytety.txt (W1), analiza/wyniki/e_merytoryka.txt (punkt 1). Notatki: notatki/c_szkic.md (sekcja 1a), notatki/e_teksty.md.

### Lepsza retencja: Pacjenci wracają rzadziej, także poza nowymi kampaniami — znacznik „Nie”

W ciągu 90 dni wraca 17% nowych pacjentów, a rok wcześniej wracało 24%.

*[Wykres] Powrót nowych pacjentów w ciągu 30, 60, 90 i 180 dni: rok wcześniej i ostatnie 12 miesięcy*

- w ciągu 30 dni: rok wcześniej 11,0%, ostatnie 12 miesięcy 7,8% [−3,2 pkt proc. gorzej]
- w ciągu 60 dni: rok wcześniej 19,1%, ostatnie 12 miesięcy 13,7% [−5,4 pkt proc. gorzej]
- w ciągu 90 dni: rok wcześniej 23,9%, ostatnie 12 miesięcy 17,4% [−6,5 pkt proc. gorzej]
- w ciągu 180 dni: rok wcześniej 27,5%, ostatnie 12 miesięcy 22,2% [−5,3 pkt proc. gorzej]

**Tabela z liczbami** *(sekcja rozwijana, tu rozwinięta)*

| Powrót w ciągu | Rok wcześniej | Ostatnie 12 miesięcy | Zmiana |
| --- | --- | --- | --- |
| 30 dni | 11,0% (14 984 pacjentów) | 7,8% (22 646 pacjentów) | −3,2 pkt proc.<br>gorzej |
| 60 dni | 19,1% (13 941 pacjentów) | 13,7% (20 823 pacjentów) | −5,4 pkt proc.<br>gorzej |
| 90 dni | 23,9% (12 867 pacjentów) | 17,4% (18 924 pacjentów) | −6,5 pkt proc.<br>gorzej |
| 180 dni | 27,5% (9 125 pacjentów) | 22,2% (12 591 pacjentów) | −5,2 pkt proc.<br>gorzej |

- Bez pacjentów nowych kampanii powrót też spada: 22% wobec 24%.
- Pacjenci nowych kampanii wracają w 4%. Ich większy udział odpowiada za około 71% spadku, a reszta to spadek w kanałach działających w obu latach.
- Marża na pacjenta w 90 dniach, przed kosztem pozyskania, spadła z 67 do 58 zł. Poza nowymi kampaniami prawie stoi.

**Zastrzeżenie.** To opis zmiany, który nie wskazuje jej przyczyny. Nie wiemy, czy ci sami pacjenci zachowują się dziś gorzej, czy zmieniło się to, kto do nas trafia.

Zobacz w danych: Kohorty: powrót w 90 dniach, nowe kampanie na L4 i pozostałe; Kohorty: powrót bez pacjentów nowych kampanii *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

- Powrót to kolejne zamówienie, które nie zostało anulowane. Liczymy go na tych samych dniach kalendarzowych (pierwsze zakupy do 2 lipca w obu latach przy oknie 90 dni) i tylko w kohortach z pełnym oknem obserwacji. Liczba pacjentów: 12 867 rok wcześniej i 18 924 w ostatnich 12 miesiącach; bez nowych kampanii 14 031 (powrót 22,0% wobec 23,9%), pacjenci nowych kampanii 4 893 (powrót 4,1%). Marża na pacjenta w 90 dniach: 58,3 zł wobec 66,6 zł, bez nowych kampanii 66,0 zł.
- Kolejne zamówienia na pacjenta w 90 dniach: 0,234 wobec 0,334, czyli o 29,8% mniej; bez pacjentów nowych kampanii 0,300.
- Według sesji z płatnością bez nowych kampanii powrót wynosi 20,4%, a marża 63,3 zł. Cała różnica to 1 383 pacjentów nowych kampanii (z pełnym oknem 90 dni), których ten podział przypisuje innym kanałom: 1 279 weszło z reklamy nowej kampanii, a zapłaciło w innej sesji, a 104 zapłaciło z kodem nowej kampanii po wejściu z innego kanału. Wracają w 4,3%. Bez nich oba podziały dają 22,0% i 66,0 zł, a udział nowych kampanii w spadku powrotu wynosi w obu 71% (według sesji z płatnością bez tej poprawki 46%).
- „Około 71% spadku” to podział opisowy, czyli bez mierzenia wpływu: udział pacjentów nowych kampanii (25,9% kohort) razy różnica powrotu między nimi a resztą (4,6 z 6,5 punktu procentowego). Nie mówi, co by się stało bez tych kampanii.
- Według pierwszej usługi, bez pacjentów nowych kampanii (95% przedział różnicy): spada po e-recepcie z 33,4% (3 206 pacjentów) do 29,9% (3 570), a po wizycie u innego specjalisty z 25,2% (2 325 pacjentów) do 20,6% (2 549). Bez istotnej zmiany: pediatra z 22,3% (673 pacjentów) do 26,3% (711), od −0,5 do +8,5 punktu, psychiatra z 22,5% (550 pacjentów) do 24,6% (605), od −2,8 do +7,0 punktu, pierwsze L4 u internisty z 14,6% (2 795 pacjentów) do 13,8% (2 969), od −2,6 do +1,0 punktu. Według sesji z płatnością L4 spada do 11,0%, ale to ta sama grupa: do 2 969 pacjentów według pierwszego wejścia dochodzi 1 145 pacjentów nowych kampanii z pierwszym L4.
- Liczba osób, które wróciły w 90 dniach, rośnie: 3 289 wobec 3 076 (+6,9%). Spada tylko ich odsetek.
- W 180 dniach liczymy tylko kohorty z pełnym oknem (9 125 i 12 591 pacjentów), więc to wcześniejsze, mniejsze grupy niż w 90 dniach.
- Część spadku w kanałach działających w obu latach może wiązać się z porannymi opóźnieniami u internistów: po spóźnionej pierwszej wizycie pacjenci wracają rzadziej. Dane tego nie rozstrzygają (Czego nie wiemy, punkt 4).

Skąd liczby: analiza/wyniki/c_priorytety.txt (W2), analiza/wyniki/a5r_kohorty.txt (180 dni), analiza/wyniki/d_retencja.txt (usługi, kolejne zamówienia), analiza/wyniki/e_merytoryka.txt (punkt 1).

### TelemediGO rośnie razem z liczbą zamówień, a nie dzięki większej chęci zakupu

Sprzedaż wzrosła o 40%, bo jest więcej zamówień i przez cały rok działała sprzedaż w newsletterze, a odsetek kupujących przy kasie nie rośnie.

*[Wykres] Sprzedaż TelemediGO według sposobu zakupu: rok wcześniej i ostatnie 12 miesięcy*

- Przy kasie z pierwszym zamówieniem: rok wcześniej 905, ostatnie 12 miesięcy 1 089 [+184]
- Przy kasie z kolejnym zamówieniem: rok wcześniej 629, ostatnie 12 miesięcy 918 [+289]
- Osobno, z newslettera: rok wcześniej 225, ostatnie 12 miesięcy 461 [+236]

*Liczba zakupów TelemediGO.*

**Tabela z liczbami** *(sekcja rozwijana, tu rozwinięta)*

| Typ zakupu | Rok wcześniej | Ostatnie 12 miesięcy | Zmiana | Udział we wzroście |
| --- | --- | --- | --- | --- |
| Przy kasie z pierwszym zamówieniem pacjenta | 905 | 1 089 | +184 | 26% |
| Przy kasie z kolejnym zamówieniem | 629 | 918 | +289 | 41% |
| Osobno, z newslettera | 225 | 461 | +236 | 33% |
| Razem | 1 759 | 2 468 | +709 | 100% |

- Opłata 89 zł nie pokrywa zniżek: członkostwa sprzed roku dostały średnio o około 16 zł więcej zniżek, niż przyniosły opłat.
- Widać to w marży: powtórne zamówienie pacjenta spoza nowych kampanii zostawiło w III kwartale 2026 około 33 zł marży wobec 36 zł rok wcześniej. Prawie cały ten spadek to rosnący udział wizyt ze zniżką TelemediGO: z 34% do 42% powtórnych zamówień.

**Zastrzeżenie.** Nie wiemy, ile wizyt członkostwo dokłada. Test z pozycji 12 pokaże wpływ samej zniżki, ale nie opłacalność oferty za 89 zł.

Zobacz w danych: Priorytety: pozycja 12, test TelemediGO; Priorytety: pozycja 10, warunki TelemediGO u specjalistów; Kohorty: kupujący TelemediGO przy pierwszym zakupie; Lejek: zakupy samego TelemediGO *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

- Sprzedaż osobna w newsletterze ruszyła 8.09.2025. Rok wcześniej działała więc tylko 23 dni, a sprzedała w nich 225 członkostw. W ostatnich 12 miesiącach sprzedaje średnio 38 miesięcznie.
- Przy kasie przybywa zakupów, bo jest więcej zamówień, a nie wyższy odsetek kupujących. Przy pierwszym zamówieniu odsetek kupujących spada z 5,58% (16 231 zamówień) do 4,41% (24 687): więcej zamówień dodaje 471 zakupów, a niższy odsetek odejmuje 287. Przy kolejnych zamówieniach odsetek rośnie lekko, z 9,27% (6 784) do 9,86% (9 307).
- Spadek odsetka przy pierwszym zamówieniu to w całości pacjenci nowych kampanii na L4: kupuje u nich 1,5% (7 268 pacjentów). Bez nich odsetek stoi: 5,58% wobec 5,63% (17 419 pacjentów).
- Opłata 89 zł nie pokrywa średniej zniżki. Członkostwa sprzed roku (1 759, pełne 365 dni) przyniosły 156 551 zł opłat i dostały 183 939 zł zniżki efektywnej, czyli −27 388 zł (−15,57 zł na członkostwo). W ostatnich 12 miesiącach przybliżenie to −10,7 zł na członkostwo. To rachunek przy założeniu, że te same wizyty zostałyby kupione bez TelemediGO, a nie strata programu: nie wiemy, ile wizyt członkostwo dokłada.
- Kupujący TelemediGO przy pierwszym zamówieniu wracają w 90 dniach częściej niż podobni pacjenci: 34,7% wobec 20,0% w ostatnich 12 miesiącach (858 kupujących). Dane nie mówią, ile z tego to wpływ zniżki, a ile to, że kupują ci, którzy i tak planują wracać. Test z pozycji 12 (losowy, bezpłatny dostęp do zniżek) pokaże wpływ samej zniżki.
- Powtórne zamówienie pacjenta spoza nowych kampanii zostawiło w III kwartale 2026 32,81 zł marży wobec 35,86 zł rok wcześniej. Wizyta ze zniżką TelemediGO zostawia średnio 11,01 zł marży, bez zniżki 48,78 zł, a wizyta u specjalisty ze zniżką traci 5,59 zł. Udział wizyt ze zniżką wśród powtórnych zamówień: 34,3% (2 879 zamówień) i 41,6% (3 140). Zmiana tego udziału daje 2,71 zł z 3,05 zł spadku marży na zamówienie (rozkład na strukturę i marżę w obrębie rodzaju zniżki).

Skąd liczby: analiza/c_telemedigo.py → analiza/wyniki/c_telemedigo.txt (1a, 1b, 1e, 1f, 2a, 2b, 4a). Notatka: notatki/c_szkic.md, sekcja 2. Marża powtórnych zamówień: analiza/wyniki/e_merytoryka.txt (punkt 3).

### Z każdym kwartałem wydatki na kampanie rosną rok do roku szybciej, a marża przed ich kosztem wolniej

W III kwartale 2026 marża przed kosztem kampanii wzrosła o 25%, a wydatki na kampanie były ponad dwa razy wyższe niż rok wcześniej.

*[Wykres] Zmiana rok do roku w każdym kwartale: marża przed kosztem kampanii i wydatki na kampanie*

- IV kw. 2025: marża przed kosztem kampanii +55,2%, wydatki na kampanie +29,6%
- I kw. 2026: marża przed kosztem kampanii +49,7%, wydatki na kampanie +66,4%
- II kw. 2026: marża przed kosztem kampanii +38,4%, wydatki na kampanie +104,0%
- III kw. 2026: marża przed kosztem kampanii +25,2%, wydatki na kampanie +107,7%

*Zmiana wobec tego samego kwartału rok wcześniej. Marża przed kosztem kampanii to przychód z konsultacji po zwrotach i z TelemediGO minus koszt lekarza; wydatki na kampanie bez prowizji afiliacyjnej.*

**Tabela z liczbami** *(sekcja rozwijana, tu rozwinięta)*

*Zmiana wobec tego samego kwartału rok wcześniej; pod nią wartość w kwartale*

| Kwartał | Marża przed kosztem kampanii | Wydatki na kampanie | Marża po kosztach kampanii |
| --- | --- | --- | --- |
| IV 2025 | +55,2%<br>lepiej<br>376,0 tys. zł | +29,6%<br>uwaga<br>113,1 tys. zł | +71,4%<br>lepiej<br>259,4 tys. zł |
| I 2026 | +49,7%<br>lepiej<br>500,2 tys. zł | +66,4%<br>uwaga<br>170,6 tys. zł | +43,0%<br>lepiej<br>324,4 tys. zł |
| II 2026 | +38,4%<br>lepiej<br>444,5 tys. zł | +104,0%<br>uwaga<br>184,4 tys. zł | +13,0%<br>lepiej<br>256,6 tys. zł |
| III 2026 | +25,2%<br>lepiej<br>392,5 tys. zł | +107,7%<br>uwaga<br>181,6 tys. zł | −6,8%<br>gorzej<br>207,7 tys. zł |

- Za cały rok marża po koszcie lekarza, kampaniach i prowizji wzrosła o 27%.
- Marża przed kosztem kampanii wzrosła za cały rok o 41%, a wydatki na kampanie o 77%.

**Zastrzeżenie.** Spadek marży w III kwartale 2026, o 7% rok do roku, zależy od jednorazowego zdarzenia: rok wcześniej we wrześniu ruszyła sprzedaż TelemediGO w newsletterze. Po odjęciu jednorazowej nadwyżki tego startu marża kwartału jest o 1% wyższa niż rok wcześniej.

Zobacz w danych: Wynik biznesu: marża po kwartałach; Priorytety: pozycja 1, Safari *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

- Za cały rok marża po koszcie lekarza, kampaniach i prowizji wzrosła z 828 do 1 048 tys. zł, czyli o 26,6%. Marża przed kosztem kampanii wzrosła o 41,5%, a wydatki na kampanie o 76,7%.
- W III kwartale 2026 marża była o 6,8% niższa niż rok wcześniej. Sprzedaż TelemediGO w newsletterze sprzedała w pierwszych 23 dniach 225 członkostw; po odjęciu szacowanej nadwyżki tego startu marża kwartału rośnie o 1,1%.
- Warianty III kwartału: bez nadwyżki startu sprzedaży w newsletterze (196 z 225 zakupów ponad zwykłe tempo 29 na 23 dni, 17,4 tys. zł) +1,1%; bez całej sprzedaży w newsletterze w obu latach −2,3%; bez wszystkich opłat za TelemediGO −4,9%. Marża przed kosztem kampanii bez nadwyżki startu rośnie o 32,6%.
- Awaria zakładania konta w Safari na iPhone'ach kosztowała w samym III kwartale 2026 szacunkowo 14,6–18,3 tys. zł marży. Wyniku kwartału bez awarii nie mierzymy; to scenariusz z pozycji 1 listy priorytetów.
- W samych miesiącach: lipiec 2026 73,4 tys. zł wobec 66,8 tys. zł, sierpień 66,3 wobec 67,2 tys. zł, wrzesień 68,0 wobec 88,8 tys. zł. Cały spadek kwartału przypada na wrzesień.
- Baza powracających pacjentów (marża z pacjentów pozyskanych w poprzednich kwartałach): w III kwartale 2026 106,2 tys. zł wobec 115,2 tys. zł rok wcześniej. Rok wcześniej zawierała jednorazowy start sprzedaży w newsletterze; po odjęciu części nadwyżki przypadającej na bazę (210 z 225 zakupów) to 99,0 tys. zł, więc w 2026 baza dała o 7,3% więcej (bez całej sprzedaży w newsletterze w obu latach o 1,0% więcej). Wszystkich pacjentów pozyskanych w poprzednich kwartałach jest prawie trzy razy więcej (35 032 wobec 12 794), ale tych, którzy w kwartale coś kupili, tylko o 15% więcej (1 735 wobec 1 503). Baza jest starsza, a nowsze roczniki wracają rzadziej; tych dwóch rzeczy dane nie rozdzielają.
- Pierwsze kwartały nie miały jeszcze bazy powracających. Marża z pacjentów pozyskanych w poprzednich kwartałach to 0% marży IV kwartału 2024, 23,4% I kwartału 2025 i 51,7% III kwartału 2025. Bez tej bazy marża rośnie rok do roku o 8,5% zamiast 71,4% w IV kwartale 2025 i o 26,1% zamiast 43,0% w I kwartale 2026. Wzrost tych kwartałów jest więc zawyżony startem od zera.
- Rozkład spadku III kwartału na pacjentów nowych kampanii i resztę biznesu to rozkład księgowy, czyli przypisanie składników marży grupom pacjentów bez mierzenia wpływu. Marża spadła o 15,1 tys. zł. Według pierwszego wejścia pacjenci nowych kampanii zostawili 89,0 tys. zł marży przed kampaniami przy 87,9 tys. zł wydatków, czyli wyszli prawie na zero (+1,1 tys. zł). Reszta biznesu straciła 16,2 tys. zł: opłaty TelemediGO −11,2 tys. zł, w tym −10,5 tys. zł sprzedaży osobnej w newsletterze (225 zakupów we wrześniu 2025 wobec 107 w całym III kwartale 2026), wyższe wydatki kampanii działających w obu latach −6,2 tys. zł, marża konsultacji +1,2 tys. zł: powtórnych zamówień jest więcej (3 140 wobec 2 879), ale każde zostawia mniej marży, głównie przez większy udział wizyt ze zniżką TelemediGO (32,81 zł wobec 35,86 zł), prowizja bez zmian. Po odjęciu TelemediGO reszta biznesu traci 5,0 tys. zł; księgowo to wyższe wydatki kampanii działających w obu latach, częściowo zrównoważone wyższą marżą konsultacji. Według sesji z płatnością podział między nowe kampanie (−25,2 tys. zł) a resztę (+10,1 tys. zł) się odwraca; suma jest ta sama.

Skąd liczby: analiza/wyniki/c_priorytety.txt (W3, W4), analiza/wyniki/d_wynik.txt (punkty 1 i 2), analiza/wyniki/e_merytoryka.txt (punkt 2).

### Dashboard pokazuje więcej wzrostu, niż jest w danych

Po oczyszczeniu danych zamówień przybyło o 56%, a nie o 61%.

*[Wykres] Wzrost zamówień i przychodu z konsultacji rok do roku po każdym kroku od dashboardu do danych oczyszczonych*

**Zamówienia**
- Zamówienia, Dashboard (dane surowe): +60,7%
- Zamówienia, Bez duplikatów zamówień: +58,3%
- Zamówienia, Bez duplikatów i bez kont testowych: +55,7%
- Zamówienia, Do tego przychód po odjęciu zwrotów: +55,7% (bez zmian)

**Przychód z konsultacji**
- Przychód z konsultacji, Dashboard (dane surowe): +50,3%
- Przychód z konsultacji, Bez duplikatów zamówień: +48,1%
- Przychód z konsultacji, Bez duplikatów i bez kont testowych: +47,7%
- Przychód z konsultacji, Do tego przychód po odjęciu zwrotów: +44,8%

*Wzrost: ostatnie 12 miesięcy (X 2025 – IX 2026) wobec roku wcześniej (X 2024 – IX 2025). Każdy słupek to poziom po danym kroku, liczony od zera, a nie różnica między krokami.*

- Dashboard liczy dane na surowo: z 604 zdublowanymi zamówieniami z 10–24.06.2026, z 2 071 zamówieniami 22 kont testowych i z przychodem przed zwrotami.
- Po oczyszczeniu przychód z konsultacji po zwrotach rośnie o 45% zamiast 50%. Liczba nowych pacjentów i sprzedaż TelemediGO prawie się nie zmieniają.

**Tabela z liczbami** *(sekcja rozwijana, tu rozwinięta)*

*Zmiana: ostatnie 12 miesięcy (X 2025 – IX 2026) wobec roku wcześniej (X 2024 – IX 2025). Pod zmianą: wartość rok wcześniej → wartość w ostatnich 12 miesiącach.*

| Krok | Nowi pacjenci | Zamówienia | Przychód z konsultacji | TelemediGO |
| --- | --- | --- | --- | --- |
| Dashboard (dane surowe) | +51,9%<br>16 251 → 24 689 | +60,7%<br>25 269 → 40 613 | +50,3%<br>2,382 → 3,580 mln zł | +40,3%<br>1 759 → 2 468 |
| Bez duplikatów zamówień | bez zmian | +58,3%<br>25 269 → 40 009 | +48,1%<br>2,382 → 3,529 mln zł | bez zmian |
| Bez duplikatów i bez kont testowych | +52,1%<br>16 231 → 24 687 | +55,7%<br>24 716 → 38 491 | +47,7%<br>2,375 → 3,508 mln zł | bez zmian |
| Do tego przychód po odjęciu zwrotów | bez zmian | bez zmian | +44,8%<br>2,230 → 3,228 mln zł | bez zmian |

**Zastrzeżenie.** Pierwszy rok startował od zera, bez bazy powracających pacjentów, więc sumy roczne z definicji faworyzują drugi rok.

Zobacz w danych: Jakość danych: od dashboardu do danych oczyszczonych *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

- Dashboard liczy dane na surowo. Zawiera 604 zdublowane zamówienia z 10–24.06.2026, 2 071 zamówień kont testowych i przychód przed zwrotami. Po oczyszczeniu zamówienia rosną o 55,7% (24 716 → 38 491) zamiast 61%, a przychód z konsultacji po zwrotach o 44,8% zamiast 50%. Nowi pacjenci prawie się nie zmieniają (+51,9% na surowo, +52,1% po oczyszczeniu), a TelemediGO wcale (+40,3%).
- Start od zera. Rok wcześniej nie było bazy pacjentów z poprzedniego roku. W ostatnich 12 miesiącach pacjenci pozyskani rok wcześniej złożyli 5 289 zamówień powtórnych, które dały 153 tys. zł marży konsultacji. Sumy roczne z definicji faworyzują więc drugi rok.
- Wynik biznesu rośnie wolniej niż sprzedaż. Marża po koszcie lekarza, kampaniach i prowizji wynosi 828 tys. zł rok wcześniej i 1 048 tys. zł w ostatnich 12 miesiącach, czyli +26,6%. Po odjęciu marży powtórnych konsultacji pacjentów pozyskanych rok wcześniej to +8,1%, a po odjęciu także ich opłat za TelemediGO (41,5 tys. zł) +3,1%. To rozbicie księgowe, które nie modeluje zmian wydatków ani zachowania pacjentów. Wydatki na kampanie rosną o 77% (z 368 do 650 tys. zł).

Skąd liczby: analiza/a3_dashboard.py, analiza/a2_czyste.py, analiza/wyniki/c_priorytety.txt (W3).

### Decyzje są na liście priorytetów, a otwarte pytania w zakładce „Czego nie wiemy”

Lista priorytetów idzie od najważniejszej pozycji i przy każdej podaje wartość w marży. Zakładka „Czego nie wiemy” zbiera to, czego dane nie rozstrzygają, z testem, który to domknie.

Zobacz w danych: Priorytety; Czego nie wiemy *(odnośniki)*

*Skąd liczby: analiza/c_priorytety.py → analiza/wyniki/c_priorytety.txt (W1–W4, P1), analiza/wyniki/a5r_kohorty.txt (180 dni), analiza/wyniki/a5r_struktura.txt (L4 z L4, rozkład spadku), analiza/wyniki/a5e_ekonomia.txt, analiza/wyniki/c_telemedigo.txt. Notatka: notatki/c_szkic.md, sekcja 1. Sprawdzenia przed publikacją: analiza/wyniki/e_merytoryka.txt i analiza/wyniki/e_poprawki.txt. Teksty strony: notatki/e_teksty.md.*

Dalej: Kohorty

# Zakładka 2: Kohorty (`#kohorty`)

## Kohorty dzienne nowych pacjentów

### Nowi pacjenci wracają rzadziej niż rok wcześniej, w każdym oknie od 30 do 180 dni

W ciągu 90 dni od pierwszego zakupu wraca 17% nowych pacjentów, a rok wcześniej wracało 24%.

*[Wykres] Powrót nowych pacjentów w ciągu 30, 60, 90 i 180 dni: rok wcześniej i ostatnie 12 miesięcy*

- w ciągu 30 dni: rok wcześniej 11,0%, ostatnie 12 miesięcy 7,8% [−3,2 pkt proc. gorzej]
- w ciągu 60 dni: rok wcześniej 19,1%, ostatnie 12 miesięcy 13,7% [−5,4 pkt proc. gorzej]
- w ciągu 90 dni: rok wcześniej 23,9%, ostatnie 12 miesięcy 17,4% [−6,5 pkt proc. gorzej]
- w ciągu 180 dni: rok wcześniej 27,5%, ostatnie 12 miesięcy 22,2% [−5,3 pkt proc. gorzej]

Marża na pacjenta w 90 dniach, przed kosztem pozyskania, spadła z 67 do 58 zł.

Około 71% spadku powrotu przypada na zmianę składu pacjentów. Pacjenci dwóch nowych kampanii na L4 (Meta i TikTok) wracają w 90 dniach tylko w 4%, a jest ich coraz więcej.

Bez nich powrót też spada, z 24% do 22%. Wiek, płeć, wielkość miejscowości i województwo tego spadku nie tłumaczą.

**Zastrzeżenie.** Podział spadku opisuje skład pacjentów i nie wskazuje przyczyny: nie mówi, jak wracaliby pacjenci nowych kampanii, gdyby przyszli innym kanałem.

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

*Powrót nowych pacjentów: odsetek pacjentów, którzy złożyli kolejne zamówienie (nieanulowane)*

| Powrót w ciągu | Ostatnie 12 miesięcy | Rok wcześniej | Zmiana |
| --- | --- | --- | --- |
| 30 dni | 7,8%<br>22 646 pacjentów | 11,0%<br>14 984 pacjentów | −3,2 pkt proc.<br>gorzej |
| 60 dni | 13,7%<br>20 823 pacjentów | 19,1%<br>13 941 pacjentów | −5,4 pkt proc.<br>gorzej |
| 90 dni | 17,4%<br>18 924 pacjentów | 23,9%<br>12 867 pacjentów | −6,5 pkt proc.<br>gorzej |
| 180 dni | 22,2%<br>12 591 pacjentów | 27,5%<br>9 125 pacjentów | −5,2 pkt proc.<br>gorzej |

Powrót w 90 dniach w ostatnich 12 miesiącach: pacjenci nowych kampanii 4,1% z 4 893 pacjentów, pozostali 22,0% z 14 031 pacjentów (rok wcześniej 23,9%).

Marża na pacjenta w 90 dniach: 58,3 zł wobec 66,6 zł rok wcześniej; w 180 dniach 67,7 zł wobec 75,5 zł.

Porównujemy te same dni kalendarzowe w obu latach i tylko kohorty z pełnym oknem. W oknie 90 dni to pierwsze zakupy od 1.10.2025 do 2.07.2026 i od 1.10.2024 do 2.07.2025.

Podział spadku liczymy opisowo, czyli bez mierzenia wpływu: część przypisana nowym kampaniom to ich udział w nowych pacjentach razy różnica powrotu między pozostałymi pacjentami a nimi, a reszta to spadek powrotu pozostałych pacjentów.

Źródło pacjenta liczymy według pierwszego wejścia. Według sesji z płatnością bez nowych kampanii powrót spada do 20,4% (15 414 pacjentów), marża na pacjenta w 90 dniach do 63,3 zł, a na nowe kampanie przypada około 46% spadku. Cała różnica między podziałami to jedna grupa: według sesji z płatnością do innych kanałów trafia 1 383 pacjentów nowych kampanii na L4 z tych kohort (2 081 w całych ostatnich 12 miesiącach). 1 279 z nich weszło pierwszy raz z reklamy nowej kampanii, a zapłaciło w innej sesji, a 104 weszło z innego kanału, ale zapłaciło z kodem nowej kampanii. Bez nich oba podziały dają ten sam powrót i tę samą marżę. Dlatego opis liczymy według pierwszego wejścia, a w filtrach można wybrać oba podziały.

Część spadku w kampaniach działających w obu latach może wiązać się z porannymi opóźnieniami u internistów: po spóźnionej pierwszej wizycie pacjenci wracają rzadziej. Dane tego nie rozstrzygają (Czego nie wiemy, punkt 4).

Wiek, płeć, wielkość miejscowości i województwo nie zmieniają wniosku. Pacjenci nowych kampanii są młodsi (średnio 27,6 roku, 7 268 pacjentów, wobec 38,0 roku pozostałych w obu latach), ale pierwsze L4 z nowych kampanii wraca w 90 dniach rzadko w każdej grupie wieku: 3,5% do 29 lat (2 532 pacjentów), 4,7% w wieku 30–44 lat (1 505) i 5,1% od 45 lat (39), wobec 13,3–15,3% u pozostałych pacjentów z pierwszym L4 (668–1 507 pacjentów w grupie wieku; ostatnie 12 miesięcy, kohorty do 2.07.2026). Po przeważeniu ostatnich 12 miesięcy strukturą wieku i płci roku wcześniej spadek powrotu w 90 dniach bez nowych kampanii zostaje ten sam: −1,9 punktu procentowego według pierwszego wejścia i −3,3 zamiast −3,5 punktu według sesji z płatnością. Udział nowych kampanii w nowych pacjentach ostatnich 12 miesięcy jest podobny we wszystkich województwach (26,2–31,5%). Jeden trop regionalny: w dolnośląskim powrót poza nowymi kampaniami spada z 27,6% (1 024 pacjentów) do 19,7% (1 001), ale test wszystkich województw razem nie odrzuca, że zmiana jest wszędzie podobna, a dolnośląskie miało najwyższy powrót rok wcześniej.

Skąd liczby: analiza/a5r_kohorty.py → analiza/wyniki/a5r_kohorty.txt; analiza/wyniki/a5r_struktura.txt; analiza/wyniki/c_priorytety.txt (W2); analiza/wyniki/e_merytoryka.txt (punkt 1); analiza/wyniki/d_retencja.txt (punkt 5); eksport analiza/b_eksport.py.

*Filtry (ustawienia domyślne):*
- Przypisanie źródła: Według pierwszego wejścia (do wyboru: Według pierwszego wejścia / Według sesji z płatnością)
- Podział na serie: Nowe kampanie na L4 (do wyboru: bez podziału / Źródło (kanał) / Kampania / Nowe kampanie na L4 / Urządzenie / Przeglądarka / … (razem 12 opcji))
- Porównanie: Ostatnie 12 miesięcy wobec roku wcześniej (do wyboru: Ostatnie 12 miesięcy wobec roku wcześniej / Ostatnie 90 dni wobec poprzednich 90 / Ostatnie 30 dni wobec tych samych dni rok wcześniej / 60 dni przed i po: Godzina bez danych (17.05.2025) / 60 dni przed i po: Start sprzedaży TelemediGO w newsletterze (8.09.2025) / 60 dni przed i po: Marża na pacjenta w 30 dniach spada (30.10.2025) / … (razem 18 opcji))
- Okres A: 2024-10-01 – 2025-09-30
- Okres B: 2025-10-01 – 2026-09-30
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

### Powrót w oknie (90 dni) według dnia pierwszego zakupu, suma z 7 dni kończących się danego dnia

*Filtry (ustawienia domyślne):*
- Miara: Powrót w oknie (do wyboru: Powrót w oknie / Marża na pacjenta w oknie / Nowi pacjenci dziennie / Udział w nowych pacjentach)
- Okno: 90 dni od pierwszego zakupu (do wyboru: 30 dni od pierwszego zakupu / 60 dni od pierwszego zakupu / 90 dni od pierwszego zakupu / 180 dni od pierwszego zakupu)
- Wygładzenie: suma z 7 dni (do wyboru: bez wygładzenia (dzień) / suma z 7 dni / suma z 28 dni)

*Oś pozioma to dzień pierwszego zakupu. Szare pola to okresy porównania, pionowe linie to zdarzenia z obszaru „Retencja” (numery jak na osi zdarzeń). Serie dodasz i usuniesz w legendzie pod wykresem albo w tabeli niżej.*

*[Wykres] serie: brak*

Najedź na wykres, żeby zobaczyć wartości.

Pozostałe kampanie i kanały

×

Nowe kampanie na L4

×

Wszyscy w filtrze

×

1. 30.10.2025: Marża na pacjenta w 30 dniach spada
2. 3.11.2025: Rośnie udział nowych kampanii w nowych pacjentach
3. 10.02.2026: Spada powrót w 30 dniach
4. 2.03.2026: Powrót w kampaniach działających w obu latach

Zdarzenia ze wszystkich obszarów (14)

**Jak czytać** *(sekcja rozwijana, tu rozwinięta)*

Powrót i marża kończą się na ostatniej kohorcie z pełnym oknem. Przeciągnij po wykresie, żeby przybliżyć, kliknij dwukrotnie, żeby wrócić.

### Kohorty w podziale

*Okres A: 1.10.2024–30.09.2025. Okres B: 1.10.2025–30.09.2026. Kohorty z pełnym oknem: 30 dni: A 1.10.2024–31.08.2025, B 1.10.2025–31.08.2026; 60 dni: A 1.10.2024–1.08.2025, B 1.10.2025–1.08.2026; 90 dni: A 1.10.2024–2.07.2025, B 1.10.2025–2.07.2026; 180 dni: A 1.10.2024–3.04.2025, B 1.10.2025–3.04.2026.*

*W komórce: wartość w okresie B i liczba pacjentów, pod spodem okres A i zmiana. Zaznaczone wiersze są na wykresie wyżej.*

| Nowe kampanie na L4 | Nowi pacjenci B (A) | Udział B (A) | Powrót w 30 dniach | Powrót w 60 dniach | Powrót w 90 dniach | Powrót w 180 dniach | Marża na pacjenta, 90 dni | Marża na pacjenta, 180 dni |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wszyscy w filtrze | 24 687<br>A: 16 231 | 100,0%<br>A: 100,0% | 7,8% z 22 646<br>A: 11,0% z 14 984<br>−3,2<br>(gorzej) | 13,7% z 20 823<br>A: 19,1% z 13 941<br>−5,4<br>(gorzej) | 17,4% z 18 924<br>A: 23,9% z 12 867<br>−6,5<br>(gorzej) | 22,2% z 12 591<br>A: 27,5% z 9 125<br>−5,2<br>(gorzej) | 58,3 zł z 18 924<br>A: 66,6 zł z 12 867<br>−8,3<br>(gorzej) | 67,7 zł z 12 591<br>A: 75,5 zł z 9 125<br>−7,8<br>(gorzej) |
| Pozostałe kampanie i kanały | 17 419<br>A: 16 231 | 70,6%<br>A: 100,0% | 10,0% z 16 228<br>A: 11,0% z 14 984<br>−1,0<br>(gorzej) | 17,5% z 15 164<br>A: 19,1% z 13 941<br>−1,6<br>(gorzej) | 22,0% z 14 031<br>A: 23,9% z 12 867<br>−1,9<br>(gorzej) | 26,2% z 10 239<br>A: 27,5% z 9 125<br>−1,3<br>(gorzej) | 66,0 zł z 14 031<br>A: 66,6 zł z 12 867<br>−0,6<br>(gorzej) | 74,7 zł z 10 239<br>A: 75,5 zł z 9 125<br>−0,8<br>(gorzej) |
| Nowe kampanie na L4 | 7 268<br>A: 0 | 29,4%<br>A: 0,0% | 2,4% z 6 418<br>A: — z 0 | 3,6% z 5 659<br>A: — z 0 | 4,1% z 4 893<br>A: — z 0 | 5,0% z 2 352<br>A: — z 0 | 36,3 zł z 4 893<br>A: — z 0 | 37,3 zł z 2 352<br>A: — z 0 |

Etykiety zmiany wobec okresu A: lepiej gorzej bez oceny Strzałka pokazuje kierunek, kolor ocenę; słowo także po najechaniu na etykietę.

**Jak liczymy** *(sekcja rozwijana, tu rozwinięta)*

Kohorta to nowi pacjenci z tego samego dnia pierwszego zakupu. Powrót to kolejne zamówienie, które nie zostało anulowane, w ciągu N dni. Marża na pacjenta to przychód z konsultacji po zwrotach i z TelemediGO minus koszt lekarza, przed kosztem pozyskania.

Liczymy tylko kohorty z pełnym oknem. Okres A obcinamy do tej samej długości co dojrzała część okresu B, więc przy porównaniu rok do roku to te same dni kalendarzowe.

### Macierz kohort: powrót według dni od pierwszego zakupu

Od listopada 2025 kohorty wracają rzadziej, a od marca 2026 spadek się pogłębia: w ciągu 90 dni wraca około 15% nowych pacjentów, wobec około 24% w kohortach do października 2025.

*Wiersz to kohorta, kolumna to okno: odsetek pacjentów kohorty, którzy wrócili w ciągu tylu dni. Ten sam kolor znaczy w każdej kolumnie to samo.*

Powrót w oknie:

1. poniżej 5%
2. 5–10%
3. 10–15%
4. 15–20%
5. 20–25%
6. 25–30%
7. 30–35%
8. 35% i więcej

brak pełnego okna

| Kohorta (miesiąc) | Nowi pacjenci | Zdarzenia | 7 dni | 14 dni | 30 dni | 60 dni | 90 dni | 180 dni |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X 2024 | 1 285 |  | 1,6 | 5,1 | 10,3 | 17,9 | 22,2 | 25,5 |
| XI 2024 | 1 400 |  | 1,8 | 6,0 | 10,9 | 19,2 | 23,9 | 27,5 |
| XII 2024 | 1 501 |  | 2,4 | 6,3 | 12,8 | 20,7 | 25,6 | 28,6 |
| I 2025 | 1 628 |  | 2,3 | 6,4 | 11,9 | 21,0 | 26,3 | 30,2 |
| II 2025 | 1 560 |  | 2,2 | 4,6 | 9,9 | 18,3 | 22,8 | 26,2 |
| III 2025 | 1 601 |  | 2,4 | 5,9 | 12,2 | 19,9 | 24,1 | 27,0 |
| IV 2025 | 1 430 |  | 2,4 | 5,9 | 11,3 | 18,0 | 22,5 | 26,2 |
| V 2025 | 1 266 | 1 | 2,1 | 6,4 | 11,5 | 19,0 | 24,2 | 28,7 |
| VI 2025 | 1 123 |  | 1,6 | 4,6 | 10,6 | 18,6 | 22,7 | 26,6 |
| VII 2025 | 1 116 |  | 1,6 | 4,7 | 9,1 | 17,6 | 21,7 | 24,6 |
| VIII 2025 | 1 074 |  | 2,0 | 4,7 | 9,7 | 16,6 | 21,3 | 24,9 |
| IX 2025 | 1 247 | 2 | 1,7 | 4,7 | 10,2 | 19,3 | 24,1 | 27,5 |
| X 2025 | 1 383 | 3 | 2,2 | 5,2 | 11,1 | 19,2 | 23,5 | 27,8 |
| XI 2025 | 1 692 | 4, 5, 6, 7 | 2,1 | 5,5 | 9,5 | 15,6 | 20,0 | 24,2 |
| XII 2025 | 1 889 |  | 0,8 | 3,8 | 8,7 | 15,6 | 18,9 | 21,4 |
| I 2026 | 2 423 | 8 | 1,7 | 4,7 | 9,2 | 15,7 | 20,0 | 23,5 |
| II 2026 | 2 303 | 9, 10 | 2,0 | 4,5 | 8,8 | 15,2 | 19,1 | 21,6 |
| III 2026 | 2 682 | 11, 12 | 1,4 | 3,6 | 7,2 | 12,2 | 15,6 | 18,4 |
| IV 2026 | 2 256 |  | 1,4 | 3,5 | 6,2 | 11,4 | 14,2 | · |
| V 2026 | 2 199 | 13 | 1,1 | 3,0 | 5,9 | 10,8 | 13,7 | · |
| VI 2026 | 1 974 | 14 | 1,0 | 2,8 | 6,1 | 11,6 | 14,7 | · |
| VII 2026 | 1 958 |  | 1,5 | 4,2 | 7,7 | 12,7 | · | · |
| VIII 2026 | 1 887 |  | 1,1 | 3,8 | 7,5 | · | · | · |
| IX 2026 | 2 041 |  | · | · | · | · | · | · |

**Jak czytać** *(sekcja rozwijana, tu rozwinięta)*

Kohorta to nowi pacjenci z tego samego miesiąca, tygodnia albo dnia pierwszego zakupu; domyślnie miesiąc. Kohorty dzienne mają po około 40 pacjentów, więc ich wartości skaczą z dnia na dzień; rozdzielczość dzienną pokazuje wykres dzień po dniu wyżej.

Skala koloru jest jedna dla całej macierzy: progi są te same w każdej kolumnie i przy każdym filtrze, więc ten sam kolor zawsze oznacza ten sam przedział odsetka. Kolumna „Zdarzenia” podaje numery zdarzeń z osi, które wypadają w tej kohorcie. Filtry są te same co wyżej, bez podziału na serie.

### Krzywa powrotu według dnia od pierwszego zakupu: okres A i okres B

*Dla każdego dnia od pierwszego zakupu: odsetek pacjentów, którzy do tego dnia wrócili. Legenda pod kursorem pokazuje liczbę pacjentów i poziom B jako odsetek poziomu A.*

*[Wykres] serie: brak*

Najedź na wykres, żeby zobaczyć wartości.

Rok wcześniej

Ostatnie 12 miesięcy

*Każdy punkt krzywej liczymy z innych pacjentów: dzień N bierze tylko kohorty, które ten dzień już osiągnęły. W okresie B dzień 30 to 22 646 pacjentów, a dzień 180 już tylko 12 591, z najstarszych kohort. Wyższe wartości późnych dni nie znaczą więc, że młodsze kohorty nadrabiają.*

**Jak liczymy** *(sekcja rozwijana, tu rozwinięta)*

Na każdy dzień bierzemy tylko kohorty, które ten dzień już osiągnęły, a okres A obcinamy tak samo jak w tabeli.

**Jak liczymy w tej zakładce** *(sekcja rozwijana, tu rozwinięta)*

Nowy pacjent to konto z pierwszym opłaconym zamówieniem, bez względu na status. Źródło pozyskania przypisujemy według pierwszego wejścia (pierwsze wejście pacjenta, także z anonimowych sesji jego przeglądarek; kod kampanii na pierwszym zamówieniu rozstrzyga) albo według sesji z płatnością.

Urządzenie i przeglądarka z sesji z płatnością. Pierwsza usługa: internista według celu wizyty, pediatra, psychiatra, inny specjalista. Opóźnienie i pora z pierwszej wizyty.

Źródło danych: analiza/definicje.py, analiza/a5r_kohorty.py, eksport analiza/b_eksport.py.

Dalej: Lejek

# Zakładka 3: Lejek (`#lejek`)

## Lejek: od wejścia na stronę do płatności

### Na spadek konwersji nowych osób składają się głównie dwie rzeczy: więcej ruchu z nowych kampanii na L4 i awaria zakładania konta w Safari

Od kwietnia do września 2026 płatnością kończy się około 8% sesji osób, które jeszcze nie kupowały, a w tych samych miesiącach rok wcześniej około 11%.

- Do stycznia 2026 nowe osoby płaciły prawie tak samo często jak rok wcześniej. Od lutego 2026, gdy ruszył TikTok na L4, przybywa ruchu z nowych kampanii na L4. Od kwietnia to prawie połowa sesji nowych osób, a te sesje płacą o połowę rzadziej niż pozostałe.
- Wśród pozostałych nowych osób od kwietnia 2026 wyraźnie płacą rzadziej tylko sesje w Safari na iPhone'ach: około 8% wobec 12% rok wcześniej. Spadek skupia się na kroku zakładania konta, który działa gorzej od 17 marca 2026. W innych przeglądarkach konwersja jest bez istotnej zmiany.
- Liczba płatności nowych osób rośnie, spada tylko ich odsetek.
- Safari trzeba naprawić (pozycja 1 listy priorytetów). Do sprawdzenia jest niższa konwersja przeglądarek w aplikacjach w remarketingu Meta, kampanii Google Ads na markę i wejściach bezpośrednich (karta niżej).

**Zastrzeżenie.** Niższa konwersja nie mówi, ilu pacjentów nowe kampanie dokładają, bo nie wiemy, ilu z nich przyszłoby i bez reklamy.

Zobacz w danych: Lejek: osoby, które jeszcze nie kupowały, według kampanii *(odnośniki)*

**Sesje zalogowane od wejścia nie kończą się płatnością, a ponad co piąte konto nie ma żadnego zakupu** *(sekcja rozwijana, tu rozwinięta)*

Sesje zalogowane od wejścia: 8 026 rok wcześniej (X 2024 – IX 2025) i 14 042 w ostatnich 12 miesiącach (X 2025 – IX 2026). Usługę wybiera 20,7% z nich, termin 112 sesji przez dwa lata, a płatności nie ma żadnej. Pokazujemy je osobno, bo dane nie rozstrzygają, czy to wizyty „sprawdzam konto”, czy zepsuta ścieżka zakupu.

Zakupy samego TelemediGO: 225 rok wcześniej (X 2024 – IX 2025) i 461 w ostatnich 12 miesiącach (X 2025 – IX 2026). Mają tylko kroki płatności i płacą zawsze.

11 482 z 52 400 kont (21,9%) nie ma żadnego zakupu, a odsetek jest podobny w obu okresach (21,3% z 20 620 kont założonych rok wcześniej i 22,3% z 31 780 w ostatnich 12 miesiącach). Każde z tych kont wybrało usługę i przeszło krok konta, a 37,1% z nich zaczęło płatność. 58,1% z 11 482 ma zgodę marketingową (stan na 30.09.2026), ale w danych nie ma ani jednego ich wejścia z newslettera albo SMS-a (widać kliknięcia, nie wysyłki). Test: Czego nie wiemy, punkt 19.

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

- Ile płacą dziś: od kwietnia do września 2026 płatnością kończy się 8,41% z 146 402 sesji osób, które jeszcze nie kupowały (od 8,11% do 8,87% miesięcznie), a w tych samych miesiącach rok wcześniej 11,12% z 65 262 sesji. Średnia z całych ostatnich 12 miesięcy to 9,3% wobec 11,2% rok wcześniej.
- Przebieg rok do roku: od października 2025 do stycznia 2026 konwersja była o 0,2–0,8 punktu procentowego niższa niż rok wcześniej, w lutym i marcu 2026 o 1,5–1,6 punktu, a od kwietnia 2026 o 2,3–3,1 punktu. Sesje nowych kampanii przekroczyły 30% ruchu nowych osób w lutym 2026 (31,8%), a od kwietnia to 42–47% (tabela niżej).
- Sesje z reklam nowych kampanii płacą w 5,5% (94 462 sesje w ostatnich 12 miesiącach; od kwietnia do września 2026 5,30% z 66 725 sesji). Nowe osoby spoza nowych kampanii liczymy według pierwszego wejścia, tak jak pacjentów i retencję: od kwietnia do września 2026 płaci 10,26% z 71 441 sesji, a w tych samych miesiącach rok wcześniej 11,12% z 65 262 sesji (zmiana −0,86 punktu procentowego). W całych ostatnich 12 miesiącach 10,9% wobec 11,2% rok wcześniej.
- Safari na iPhone'ach i iPadach w tej grupie, od kwietnia do września 2026: płaci 8,27% z 14 323 sesji wobec 11,99% z 12 887 rok wcześniej, a krok konta po wyborze terminu przechodzi 45,7% sesji wobec 67,0%. Pogorszenie skupia się na kroku konta; pozostałe kroki w Safari prawie się nie zmieniają. Pozostałe przeglądarki: 10,76% z 57 118 sesji wobec 10,91% z 52 375 (zmiana −0,15 punktu, 95% przedział od −0,52 do +0,22, czyli bez istotnej zmiany), krok konta 65,4% wobec 66,4%. Od października 2025 do lutego 2026, przed awarią, Safari płaciło tak jak rok wcześniej: 12,07% wobec 12,15%. Sprawdzenie reguły łączenia osób (osoba z reklamy L4, która wróciła w innej przeglądarce bez logowania, liczy się do pozostałych): bez wszystkich osób, których pierwsze zamówienie to L4, w obu latach, Safari spada o 2,81 punktu, a pozostałe przeglądarki są bez istotnej zmiany (−0,05 punktu, przedział od −0,39 do +0,29).
- Podział zmiany od kwietnia do września 2026 (opisowo, czyli bez mierzenia wpływu): z −0,86 punktu u nowych osób spoza nowych kampanii −0,74 punktu to spadek w Safari, −0,12 punktu spadek w pozostałych przeglądarkach, a zmiana udziału Safari w ruchu daje około zera. Dla wszystkich nowych osób (−2,71 punktu, z 11,12% do 8,41%) zmiana struktury ruchu daje −2,07 punktu, spadek w Safari −0,55 punktu, a spadek w pozostałych przeglądarkach −0,09 punktu.
- Licząc według sesji, czyli bez samych sesji z reklam nowych kampanii, konwersja pozostałych sesji rośnie z 11,2% do 11,4%, a od kwietnia do września 2026 stoi (11,02% wobec 11,12%). W całych ostatnich 12 miesiącach ten podział zostawia w średniej 11 577 sesji, w których osoby nowych kampanii wracają bezpośrednio, z wyszukiwarki albo z innej reklamy. Płaci w nich 18,0% (2 081 płatności, czyli ci sami pacjenci, których w retencji oba podziały przypisują różnie). Od kwietnia do września 2026 to 8 236 sesji, w których płaci 17,6%. Te sesje podnosiły średnią i przykrywały spadek w Safari.
- Osoby, które jeszcze nie kupowały: 144 813 sesji i 16 232 płatności rok wcześniej, 265 264 sesji i 24 686 płatności w ostatnich 12 miesiącach. Najbardziej pogorszyło się przejście do wyboru usługi (z 33,7% do 30,6% sesji) i krok konta po wyborze terminu (z 66,4% do 62,6%).
- Wszystkie sesje, także osób, które już kupowały (płacą w 91,5% i 89,9% sesji): 16,0% rok wcześniej (154 085 sesji, 24 717 płatności) i 13,7% w ostatnich 12 miesiącach (280 625 sesji, 38 490 płatności).
- Podział zmiany konwersji osób, które jeszcze nie kupowały, według kampanii (opisowo, czyli bez mierzenia wpływu): zmiana struktury ruchu −1,43 punktu, zmiana w obrębie kampanii −0,47 punktu. Nowe kampanie nie mają roku wcześniej, więc liczą się w całości do struktury.
- Wszystkie sesje razem, w całych ostatnich 12 miesiącach: Rachunkowo prawie cały spadek to zmiana ruchu. Udział przeglądarek wbudowanych w aplikacje Instagram, Facebook i TikTok wzrósł z 10,7% do 35,6% sesji. Wynik rozkładu zależy od podziału. Według przeglądarki zmiana struktury ruchu daje −3,00 punktu procentowego, a zmiana konwersji w obrębie grup +0,67 punktu. Według kampanii to −2,44 i +0,11 punktu. Według strony wejścia (−0,45 i −1,87 punktu) i według tego, czy osoba już kupowała (−0,44 i −1,89 punktu), większość spadku wychodzi jako zmiana konwersji w obrębie grup. Przyjmujemy podział według przeglądarki i kampanii, bo ruch zmienił się właśnie w tym wymiarze: przybyło sesji nowych kampanii w przeglądarkach w aplikacjach, których rok wcześniej nie było. Na tej samej stronie wejścia albo w tej samej grupie pacjentów nowy ruch miesza się ze starym, więc jego niższa konwersja wygląda jak spadek w obrębie grupy.

*Osoby, które jeszcze nie kupowały: sesja do płatności, miesiąc po miesiącu*

| Miesiąc | Ostatnie 12 miesięcy | Rok wcześniej | Zmiana | Udział sesji nowych kampanii |
| --- | --- | --- | --- | --- |
| X 2025 | 11,05% | 11,30% | −0,25 pkt<br>gorzej | — |
| XI 2025 | 11,09% | 11,42% | −0,34 pkt<br>gorzej | 10,1% |
| XII 2025 | 10,39% | 11,14% | −0,76 pkt<br>gorzej | 18,4% |
| I 2026 | 10,88% | 11,08% | −0,20 pkt<br>gorzej | 24,2% |
| II 2026 | 9,99% | 11,56% | −1,57 pkt<br>gorzej | 31,8% |
| III 2026 | 9,72% | 11,23% | −1,51 pkt<br>gorzej | 36,7% |
| IV 2026 | 8,39% | 11,10% | −2,72 pkt<br>gorzej | 42,1% |
| V 2026 | 8,87% | 11,21% | −2,34 pkt<br>gorzej | 45,4% |
| VI 2026 | 8,28% | 11,02% | −2,74 pkt<br>gorzej | 46,6% |
| VII 2026 | 8,44% | 11,08% | −2,64 pkt<br>gorzej | 46,9% |
| VIII 2026 | 8,11% | 10,76% | −2,64 pkt<br>gorzej | 47,1% |
| IX 2026 | 8,37% | 11,50% | −3,14 pkt<br>gorzej | 45,9% |

*Nowe osoby spoza nowych kampanii (według pierwszego wejścia): odsetek sesji z płatnością i krok konta po wyborze terminu, Safari na iPhone'ach i pozostałe przeglądarki*

| Miesiąc | Safari na iPhone'ach | Zmiana | Krok konta | Pozostałe przeglądarki | Zmiana | Krok konta |
| --- | --- | --- | --- | --- | --- | --- |
| X 2025 | 11,82%<br>2 487 sesji; rok wcześniej 12,08% | −0,26 pkt<br>gorzej | 65,7%<br>rok wcześniej 69,4% | 10,86%<br>10 020 sesji; rok wcześniej 11,10% | −0,24 pkt<br>gorzej | 64,9%<br>rok wcześniej 66,0% |
| XI 2025 | 11,38%<br>2 723 sesje; rok wcześniej 12,07% | −0,68 pkt<br>gorzej | 67,0%<br>rok wcześniej 66,9% | 11,63%<br>10 844 sesje; rok wcześniej 11,27% | +0,36 pkt<br>lepiej | 66,2%<br>rok wcześniej 66,9% |
| XII 2025 | 11,97%<br>3 017 sesji; rok wcześniej 11,62% | +0,34 pkt<br>lepiej | 65,9%<br>rok wcześniej 64,7% | 10,94%<br>11 417 sesji; rok wcześniej 11,02% | −0,08 pkt<br>gorzej | 66,0%<br>rok wcześniej 65,2% |
| I 2026 | 12,98%<br>3 335 sesji; rok wcześniej 12,50% | +0,48 pkt<br>lepiej | 66,1%<br>rok wcześniej 66,0% | 11,94%<br>12 943 sesje; rok wcześniej 10,72% | +1,22 pkt<br>lepiej | 67,5%<br>rok wcześniej 66,0% |
| II 2026 | 11,97%<br>2 915 sesji; rok wcześniej 12,45% | −0,47 pkt<br>gorzej | 64,9%<br>rok wcześniej 66,9% | 11,34%<br>11 861 sesji; rok wcześniej 11,35% | −0,01 pkt<br>gorzej | 66,9%<br>rok wcześniej 67,1% |
| III 2026 | 11,03%<br>3 201 sesji; rok wcześniej 12,65% | −1,62 pkt<br>gorzej | 58,5%<br>rok wcześniej 68,1% | 11,54%<br>13 021 sesji; rok wcześniej 10,88% | +0,66 pkt<br>lepiej | 65,6%<br>rok wcześniej 64,8% |
| IV 2026 | 7,45%<br>2 912 sesji; rok wcześniej 11,13% | −3,68 pkt<br>gorzej | 43,0%<br>rok wcześniej 65,2% | 10,72%<br>11 324 sesje; rok wcześniej 11,10% | −0,38 pkt<br>gorzej | 64,5%<br>rok wcześniej 67,1% |
| V 2026 | 8,82%<br>2 425 sesji; rok wcześniej 12,36% | −3,54 pkt<br>gorzej | 47,0%<br>rok wcześniej 68,1% | 11,12%<br>9 669 sesji; rok wcześniej 10,93% | +0,19 pkt<br>lepiej | 66,9%<br>rok wcześniej 65,3% |
| VI 2026 | 8,29%<br>2 352 sesje; rok wcześniej 11,38% | −3,09 pkt<br>gorzej | 45,2%<br>rok wcześniej 64,5% | 10,58%<br>9 079 sesji; rok wcześniej 10,93% | −0,35 pkt<br>gorzej | 65,1%<br>rok wcześniej 66,6% |
| VII 2026 | 8,87%<br>2 154 sesje; rok wcześniej 13,16% | −4,29 pkt<br>gorzej | 47,5%<br>rok wcześniej 69,4% | 11,00%<br>8 803 sesje; rok wcześniej 10,59% | +0,40 pkt<br>lepiej | 66,9%<br>rok wcześniej 66,5% |
| VIII 2026 | 7,37%<br>2 116 sesji; rok wcześniej 11,77% | −4,40 pkt<br>gorzej | 44,9%<br>rok wcześniej 66,3% | 10,65%<br>8 884 sesje; rok wcześniej 10,50% | +0,15 pkt<br>lepiej | 65,4%<br>rok wcześniej 65,8% |
| IX 2026 | 8,93%<br>2 364 sesje; rok wcześniej 12,35% | −3,43 pkt<br>gorzej | 47,2%<br>rok wcześniej 68,8% | 10,47%<br>9 359 sesji; rok wcześniej 11,30% | −0,83 pkt<br>gorzej | 63,9%<br>rok wcześniej 67,2% |

Skąd liczby: analiza/a5p_lejek.py → analiza/wyniki/a5p_lejek_dzienny.csv.gz; analiza/e_merytoryka.py → analiza/wyniki/e_merytoryka.txt (punkt 4); analiza/e_poprawki.py → analiza/wyniki/e_poprawki.txt (punkty 1 i 3).

### Od 17 marca 2026 nowi pacjenci w Safari na iPhone'ach rzadziej kończą zakładanie konta — znacznik „Do naprawy”

Krok konta po wyborze terminu spadł z 66% do 46% i nie wraca, a w innych przeglądarkach prawie się nie zmienił.

*[Wykres] Krok konta po wyborze terminu, osoby, które jeszcze nie kupowały: Safari na iPhone'ach i pozostałe przeglądarki przed awarią i po niej*

- Safari na iPhone'ach: przed awarią 66%, po awarii 46% [−20 pkt proc. gorzej]
- Pozostałe przeglądarki: przed awarią 65%, po awarii 63% [−2 pkt proc.]

*Odsetek sesji po wyborze terminu, które przechodzą przez krok konta. Przed awarią: 16.01.2026–16.03.2026. Po awarii: Safari 17.03.2026–30.09.2026, pozostałe przeglądarki 17.03.2026–15.05.2026.*

- Konta dalej powstają, ale rzadziej. To około 100 utraconych pierwszych zamówień miesięcznie.
- Od kwietnia 2026 to prawie cały spadek konwersji nowych osób spoza nowych kampanii na L4.

Zobacz w danych: Pokaż w lejku *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Krok konta po wyborze terminu u osób, które jeszcze nie kupowały: 66,1% od 1.10.2025 do 16.03.2026 i 45,6% od 17.03 do 30.09.2026 (4 678 sesji z wyborem terminu). W 60 dniach przed awarią i po niej: 66,2% (16.01.2026–16.03.2026, 1 763 sesje) i 45,1% (17.03.2026–15.05.2026, 1 553 sesje); pozostałe przeglądarki w tych samych dniach 64,8% i 63,4%. Szacunek: 628–695 utraconych pierwszych zamówień do 30.09.2026, czyli 95–105 na 30 dni.

Skąd liczby: analiza/a5p_zdarzenia.py → analiza/wyniki/a5p_zdarzenia.txt; analiza/wyniki/c_priorytety.txt (P1); analiza/wyniki/e_poprawki.txt (punkt 3).

### Przeglądarki w aplikacjach płacą rzadziej niż zwykłe w remarketingu, kampanii na markę i wejściach bezpośrednich — znacznik „Do sprawdzenia”

W tych kampaniach różnica wynosi 4–12 punktów procentowych, a w reklamach Meta i TikTok na L4, które trafiają do nowych osób, jej nie ma.

*[Wykres] Odsetek sesji zakończonych płatnością w przeglądarkach w aplikacjach i w zwykłych przeglądarkach w tych samych warunkach*

- Remarketing Meta: zwykłe przeglądarki w tych samych warunkach 26,3%, przeglądarka w aplikacji 14,1% [−12,2 pkt proc.]
- Google Ads na markę: zwykłe przeglądarki w tych samych warunkach 22,5%, przeglądarka w aplikacji 17,4% [−5,1 pkt proc.]
- Wejścia bezpośrednie: zwykłe przeglądarki w tych samych warunkach 25,4%, przeglądarka w aplikacji 21,0% [−4,4 pkt proc.]

**Dla porównania: kampanie na L4, które trafiają do nowych osób**
- Kampania Meta na L4: zwykłe przeglądarki w tych samych warunkach 5,6%, przeglądarka w aplikacji 6,0% [+0,4 pkt proc.]
- Kampania TikTok na L4: zwykłe przeglądarki w tych samych warunkach 4,6%, przeglądarka w aplikacji 4,8% [+0,2 pkt proc.]

*Odsetek sesji zakończonych płatnością, ostatnie 12 miesięcy. Zwykłe przeglądarki „w tych samych warunkach”: odsetek, jaki miałyby te same sesje przy konwersji zwykłych przeglądarek w tej samej kampanii i tej samej grupie osób.*

- Niska konwersja kampanii na L4 nie wynika więc wyraźnie z przeglądarki. Przyczynę różnicy w pozostałym ruchu trzeba sprawdzić, zanim zaplanujemy naprawę (Czego nie wiemy, punkt 18).

**Zastrzeżenie.** To porównanie obserwacyjne: nie rozdziela wpływu przeglądarki od tego, kto z niej korzysta.

Zobacz w danych: Pokaż w lejku *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

W kampaniach do nowych odbiorców nie wykryliśmy niższej konwersji przeglądarki w aplikacji niż zwykłej w tej samej kampanii (ostatnie 12 miesięcy: Meta na L4 5,99% z 46 091 sesji wobec 5,58% z 14 901, TikTok 4,80% z 28 160 wobec 4,56% z 5 310; Meta „lekarz online” różnica −0,15 punktu procentowego, od −0,51 do +0,21, 29 330 sesji w przeglądarkach wbudowanych w dwóch latach). Niska konwersja tych kampanii nie wynika więc wyraźnie z przeglądarki; naprawą, którą da się wycenić, jest obietnica reklamy i strona wejścia (Priorytety, pozycja 5). W ruchu osób, które już znają stronę albo markę (remarketing Meta, Google Ads na markę i wejścia bezpośrednie), jest inaczej: w ostatnich 12 miesiącach sesje w przeglądarkach w aplikacjach płacą rzadziej niż zwykłe w tej samej kampanii: w remarketingu Meta o 12,2 punktu (1 772 sesje w przeglądarkach wbudowanych), w Google Ads na markę o 5,1 punktu (2 357), w wejściach bezpośrednich o 4,4 punktu (4 261). Luka jest na wyborze usługi i na kroku konta.

Dla porównania cały ruch osób, które jeszcze nie kupowały (wszystkie kampanie razem): przeglądarki w aplikacjach płacą w obu latach w 3,8–6,6% sesji, a Chrome i Safari w 9,9–12,2%. Usługę wybiera 18,5–24,9% sesji w przeglądarkach w aplikacjach (Chrome i Safari 34,3–35,9%), termin 53,9–60,6% tych, które wybrały usługę (wobec 67,7–68,6%), a krok konta 56,0–60,0% tych, które wybrały termin (wobec 56,7–66,9%; najniżej Safari po awarii).

Skąd liczby: analiza/d_kampanie.py → analiza/wyniki/d_kampanie.txt (punkt 1); analiza/wyniki/e_merytoryka.txt (punkt 5c).

*Filtry (ustawienia domyślne):*
- Kto: Jeszcze nie kupowali (do wyboru: Jeszcze nie kupowali / Kupowali wcześniej / Wszyscy)
- Typ sesji: Sesje zwykłe (lejek) (do wyboru: Sesje zwykłe (lejek) / Zalogowane od wejścia / Zakup samego TelemediGO)
- Podział: Przeglądarka (do wyboru: Całość / Urządzenie / Przeglądarka / System i przeglądarka / Urządzenie i przeglądarka / Źródło (kanał) / Kampania / Strona wejścia)
- Porównanie: Ostatnie 12 miesięcy wobec roku wcześniej (do wyboru: Ostatnie 12 miesięcy wobec roku wcześniej / Ostatnie 90 dni wobec poprzednich 90 / Ostatnie 30 dni wobec tych samych dni rok wcześniej / 60 dni przed i po: Godzina bez danych (17.05.2025) / 60 dni przed i po: Start sprzedaży TelemediGO w newsletterze (8.09.2025) / 60 dni przed i po: Marża na pacjenta w 30 dniach spada (30.10.2025) / … (razem 18 opcji))
- Okres A: 2024-10-01 – 2025-09-30
- Okres B: 2025-10-01 – 2026-09-30

### Kroki lejka: ostatnie 12 miesięcy wobec roku wcześniej, razem

*Filtry (ustawienia domyślne):*
- Pokaż dla: Razem (wszystkie wartości) (do wyboru: Razem (wszystkie wartości) / Chrome / Safari / Instagram (w aplikacji) / Facebook (w aplikacji) / TikTok (w aplikacji) / … (razem 10 opcji))

*Kto: jeszcze nie kupowali. Okres A: 1.10.2024–30.09.2025 (365 dni). Okres B: 1.10.2025–30.09.2026 (365 dni).*

| Krok | Sesje (B) | Odsetek sesji (B) | Porównanie | Przejście do kroku |
| --- | --- | --- | --- | --- |
| Wejście na stronę | 265 264 sesji | 100,0% | rok wcześniej: 100,0% |  |
| Wybór usługi | 81 294 sesji | 30,6% | rok wcześniej: 33,7% | Przechodzi dalej: 30,6% rok wcześniej: 33,7% −3,0 gorzej Najbardziej obniża płatności |
| Wybór terminu | 53 527 sesji | 20,2% | rok wcześniej: 22,7% | Przechodzi dalej: 65,8% rok wcześniej: 67,5% −1,6 gorzej |
| Logowanie albo założenie konta | 33 525 sesji | 12,6% | rok wcześniej: 15,1% | Przechodzi dalej: 62,6% rok wcześniej: 66,4% −3,7 gorzej |
| Wejście na płatność | 27 824 sesji | 10,5% | rok wcześniej: 12,6% | Przechodzi dalej: 83,0% rok wcześniej: 83,4% −0,4 gorzej |
| Płatność przyjęta | 24 686 sesji | 9,3% | rok wcześniej: 11,2% | Przechodzi dalej: 88,7% rok wcześniej: 89,2% −0,5 gorzej |

Ostatnie 12 miesięcy: odsetek sesji, które doszły do kroku

Ten sam odsetek: rok wcześniej

**Jak czytać** *(sekcja rozwijana, tu rozwinięta)*

Pasek to odsetek sesji, które doszły do kroku. Pionowa kreska to ten sam odsetek w okresie porównania. Między krokami: jaka część sesji z poprzedniego kroku przechodzi dalej.

Etykieta „Najbardziej obniża płatności” wskazuje przejście, które najbardziej obniża odsetek sesji zakończonych płatnością. Mierzymy to spadkiem względnym wobec okresu porównania, bo odsetek płatności to iloczyn przejść. Ten sam spadek w punktach procentowych waży więcej tam, gdzie dalej przechodzi mniejsza część sesji. Liczby sesji przy krokach są z okresu B.

### Udział sesji nowych kampanii na L4 w ruchu osób, które jeszcze nie kupowały, miesiąc po miesiącu

*[Wykres] Udział sesji nowych kampanii na L4 w sesjach osób, które jeszcze nie kupowały, w każdym miesiącu*

- X 2024: 0,0% (0 z 11 375 sesji)
- XI 2024: 0,0% (0 z 12 256 sesji)
- XII 2024: 0,0% (0 z 13 472 sesji)
- I 2025: 0,0% (0 z 14 699 sesji)
- II 2025: 0,0% (0 z 13 490 sesji)
- III 2025: 0,0% (0 z 14 259 sesji)
- IV 2025: 0,0% (0 z 12 878 sesji)
- V 2025: 0,0% (0 z 11 290 sesji)
- VI 2025: 0,0% (0 z 10 190 sesji)
- VII 2025: 0,0% (0 z 10 070 sesji)
- VIII 2025: 0,0% (0 z 9 986 sesji)
- IX 2025: 0,0% (0 z 10 848 sesji)
- X 2025: 0,0% (0 z 12 507 sesji)
- XI 2025: 10,1% (1 541 z 15 263 sesji)
- XII 2025: 18,4% (3 348 z 18 189 sesji)
- I 2026: 24,2% (5 389 z 22 273 sesji)
- II 2026: 31,8% (7 336 z 23 056 sesji)
- III 2026: 36,7% (10 123 z 27 574 sesji)
- IV 2026: 42,1% (11 314 z 26 903 sesji)
- V 2026: 45,4% (11 263 z 24 795 sesji)
- VI 2026: 46,6% (11 120 z 23 848 sesji)
- VII 2026: 46,9% (10 876 z 23 195 sesji)
- VIII 2026: 47,1% (10 954 z 23 264 sesji)
- IX 2026: 45,9% (11 198 z 24 397 sesji)

*Odsetek sesji zwykłych osób, które jeszcze nie kupowały, z kampanii Meta pozyskanie: L4 szybko i TikTok: L4 w 15 minut, w każdym miesiącu kalendarzowym. Wykres nie zależy od podziału, „Kto” ani okresów wybranych w filtrach wyżej.*

### Sesja do płatności (płatność / sesje), suma z 7 dni kończących się danego dnia

*Filtry (ustawienia domyślne):*
- Miara: Sesja do płatności (płatność / sesje) (do wyboru: Wybór usługi (usługa / sesje) / Wybór terminu (termin / usługa) / Logowanie albo konto (konto / termin) / Wejście na płatność (płatność / konto) / Płatność przyjęta (przyjęta / wejście) / Sesja do płatności (płatność / sesje) / Sesje dziennie / Udział w sesjach)
- Wygładzenie: suma z 7 dni (do wyboru: bez wygładzenia (dzień) / suma z 7 dni / suma z 28 dni)

*Szare pola to okresy porównania, pionowe linie to zdarzenia z obszaru „Lejek” (numery jak na osi zdarzeń). Serie dodasz i usuniesz w legendzie pod wykresem albo w tabeli niżej.*

*[Wykres] serie: brak*

Najedź na wykres, żeby zobaczyć wartości.

Chrome

×

Safari

×

Instagram (w aplikacji)

×

TikTok (w aplikacji)

×

+ Dodaj serię

Razem

Facebook (w aplikacji)

Samsung Internet

Firefox

Edge

Opera

1. 8.09.2025: Start sprzedaży TelemediGO w newsletterze
2. 3.11.2025: Start kampanii Meta na L4
3. 1.01.2026: Remarketing Meta słabnie
4. 9.02.2026: Start kampanii TikTok na L4
5. 17.03.2026: Awaria zakładania konta w Safari na iOS
6. 22.05.2026: Spada konwersja Google Ads na markę

Zdarzenia ze wszystkich obszarów (14)

### Kroki lejka w podziale

*Okres A: 1.10.2024–30.09.2025 (365 dni). Okres B: 1.10.2025–30.09.2026 (365 dni). Typ: Sesje zwykłe. Kto: jeszcze nie kupowali.*

*W komórce: odsetek w okresie B i liczba sesji, od której go liczymy. Pod spodem ten sam odsetek w okresie A i zmiana w punktach procentowych. Zaznaczone wiersze są na wykresie wyżej.*

| Przeglądarka | Sesje B (A) | Udział w sesjach B (A) | Wybór usługi | Wybór terminu | Logowanie albo konto | Wejście na płatność | Płatność przyjęta | Sesja do płatności |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Razem | 265 264<br>A: 144 813 | 100,0%<br>A: 100,0% | 30,6% z 265 264<br>A: 33,7% z 144 813<br>−3,0<br>(gorzej) | 65,8% z 81 294<br>A: 67,5% z 48 753<br>−1,6<br>(gorzej) | 62,6% z 53 527<br>A: 66,4% z 32 890<br>−3,7<br>(gorzej) | 83,0% z 33 525<br>A: 83,4% z 21 826<br>−0,4<br>(gorzej) | 88,7% z 27 824<br>A: 89,2% z 18 203<br>−0,5<br>(gorzej) | 9,3% z 265 264<br>A: 11,2% z 144 813<br>−1,9<br>(gorzej) |
| Chrome | 88 809<br>A: 69 541 | 33,5%<br>A: 48,0% | 34,3% z 88 809<br>A: 35,4% z 69 541<br>−1,2<br>(gorzej) | 68,2% z 30 448<br>A: 68,6% z 24 650<br>−0,4<br>(gorzej) | 66,3% z 20 760<br>A: 66,8% z 16 904<br>−0,5<br>(gorzej) | 83,7% z 13 758<br>A: 83,8% z 11 295<br>−0,1<br>(gorzej) | 89,0% z 11 513<br>A: 89,1% z 9 462<br>−0,1<br>(gorzej) | 11,5% z 88 809<br>A: 12,1% z 69 541<br>−0,6<br>(gorzej) |
| Safari | 43 095<br>A: 32 475 | 16,2%<br>A: 22,4% | 35,0% z 43 095<br>A: 35,9% z 32 475<br>−0,9<br>(gorzej) | 67,7% z 15 067<br>A: 68,1% z 11 662<br>−0,3<br>(gorzej) | 56,7% z 10 205<br>A: 66,9% z 7 936<br>−10,1<br>(gorzej) | 83,1% z 5 791<br>A: 83,1% z 5 308<br>0,0 | 88,5% z 4 813<br>A: 89,4% z 4 413<br>−0,9<br>(gorzej) | 9,9% z 43 095<br>A: 12,2% z 32 475<br>−2,3<br>(gorzej) |
| Instagram (w aplikacji) | 39 417<br>A: 9 452 | 14,9%<br>A: 6,5% | 24,9% z 39 417<br>A: 18,5% z 9 452<br>+6,5<br>(lepiej) | 60,6% z 9 823<br>A: 55,9% z 1 745<br>+4,7<br>(lepiej) | 60,0% z 5 954<br>A: 56,0% z 975<br>+4,0<br>(lepiej) | 81,4% z 3 573<br>A: 77,1% z 546<br>+4,3<br>(lepiej) | 88,9% z 2 909<br>A: 86,0% z 421<br>+2,9<br>(lepiej) | 6,6% z 39 417<br>A: 3,8% z 9 452<br>+2,7<br>(lepiej) |
| TikTok (w aplikacji) | 31 459<br>A: 0 | 11,9%<br>A: 0,0% | 23,0% z 31 459<br>A: — z 0 | 60,1% z 7 251<br>A: — z 0 | 59,0% z 4 359<br>A: — z 0 | 81,2% z 2 572<br>A: — z 0 | 86,7% z 2 088<br>A: — z 0 | 5,8% z 31 459<br>A: — z 0 |
| Facebook (w aplikacji) | 28 487<br>A: 6 788 | 10,7%<br>A: 4,7% | 24,8% z 28 487<br>A: 18,9% z 6 788<br>+5,9<br>(lepiej) | 60,4% z 7 057<br>A: 53,9% z 1 283<br>+6,5<br>(lepiej) | 59,5% z 4 259<br>A: 56,2% z 691<br>+3,4<br>(lepiej) | 81,9% z 2 536<br>A: 80,9% z 388<br>+1,0<br>(lepiej) | 89,1% z 2 077<br>A: 87,6% z 314<br>+1,5<br>(lepiej) | 6,5% z 28 487<br>A: 4,1% z 6 788<br>+2,4<br>(lepiej) |
| Samsung Internet | 15 157<br>A: 11 627 | 5,7%<br>A: 8,0% | 33,5% z 15 157<br>A: 35,3% z 11 627<br>−1,7<br>(gorzej) | 68,8% z 5 085<br>A: 67,4% z 4 102<br>+1,4<br>(lepiej) | 66,1% z 3 497<br>A: 68,1% z 2 765<br>−2,0<br>(gorzej) | 83,7% z 2 312<br>A: 83,3% z 1 884<br>+0,4<br>(lepiej) | 88,9% z 1 935<br>A: 89,1% z 1 570<br>−0,2<br>(gorzej) | 11,3% z 15 157<br>A: 12,0% z 11 627<br>−0,7<br>(gorzej) |
| Firefox | 8 617<br>A: 6 751 | 3,2%<br>A: 4,7% | 35,5% z 8 617<br>A: 35,3% z 6 751<br>+0,2<br>(lepiej) | 68,0% z 3 055<br>A: 67,6% z 2 381<br>+0,4<br>(lepiej) | 67,2% z 2 077<br>A: 67,1% z 1 610<br>+0,1<br>(lepiej) | 83,2% z 1 396<br>A: 84,6% z 1 081<br>−1,4<br>(gorzej) | 89,8% z 1 161<br>A: 89,5% z 914<br>+0,3<br>(lepiej) | 12,1% z 8 617<br>A: 12,1% z 6 751<br>0,0 |
| Edge | 7 659<br>A: 6 131 | 2,9%<br>A: 4,2% | 34,3% z 7 659<br>A: 36,0% z 6 131<br>−1,7<br>(gorzej) | 68,4% z 2 624<br>A: 69,2% z 2 207<br>−0,9<br>(gorzej) | 66,6% z 1 794<br>A: 65,2% z 1 528<br>+1,4<br>(lepiej) | 82,8% z 1 195<br>A: 85,2% z 997<br>−2,3<br>(gorzej) | 87,5% z 990<br>A: 89,9% z 849<br>−2,4<br>(gorzej) | 11,3% z 7 659<br>A: 12,4% z 6 131<br>−1,1<br>(gorzej) |
| Opera | 2 564<br>A: 2 048 | 1,0%<br>A: 1,4% | 34,5% z 2 564<br>A: 35,3% z 2 048<br>−0,8<br>(gorzej) | 70,4% z 884<br>A: 66,5% z 723<br>+3,8<br>(lepiej) | 63,0% z 622<br>A: 68,0% z 481<br>−5,0<br>(gorzej) | 86,2% z 392<br>A: 79,5% z 327<br>+6,7<br>(lepiej) | 87,6% z 338<br>A: 90,8% z 260<br>−3,2<br>(gorzej) | 11,5% z 2 564<br>A: 11,5% z 2 048<br>0,0 |

Etykiety zmiany wobec okresu A, w punktach procentowych: lepiej gorzej bez oceny Strzałka pokazuje kierunek, kolor ocenę; słowo także po najechaniu na etykietę.

**Jak liczymy w tej zakładce** *(sekcja rozwijana, tu rozwinięta)*

Lejek główny obejmuje sesje zwykłe, czyli bez konta na wejściu albo z kontem, które pojawia się dopiero na kroku logowania. Sesje zalogowane od wejścia i zakupy samego TelemediGO są osobnymi typami sesji.

„Jeszcze nie kupowali” to osoby bez zakupu przed początkiem sesji, także na koncie, na które logowały się w tej samej przeglądarce. Dzień sesji liczymy w czasie polskim.

Płatności w lejku (24 717 rok wcześniej, X 2024 – IX 2025, i 38 490 w ostatnich 12 miesiącach, X 2025 – IX 2026) i zamówienia (24 716 i 38 491) różnią się o 1 na granicy okresów, bo sesję liczymy do dnia jej rozpoczęcia, a zamówienie do dnia płatności.

Źródło danych: analiza/a5p_lejek.py, eksport analiza/b_eksport.py.

Dalej: Po zakupie

# Zakładka 4: Po zakupie (`#po-zakupie`)

## Po zakupie: przebieg wizyty

### Od lutego 2026 około połowy porannych wizyt u internisty zaczyna się ponad 15 minut po terminie

W ostatnich 12 miesiącach ponad 15 minut po terminie zaczęło się 41% porannych wizyt u internisty, a rok wcześniej 6%.

Do października 2025 było to 5–7% wizyt miesięcznie. Od listopada 2025 odsetek rośnie z miesiąca na miesiąc, a od lutego 2026 stoi na poziomie 47–53%.

U pozostałych lekarzy rano bez istotnej zmiany: około 3% w obu latach. U internisty w innych porach odsetek rośnie dużo mniej, głównie na brzegach porannego bloku (karta niżej).

**Zastrzeżenie.** Przyczyny opóźnień w danych nie widać, bo nie mamy grafików ani identyfikatorów lekarzy (Czego nie wiemy, punkt 4).

*Filtry (ustawienia domyślne):*
- Specjalizacja (wykres): Internista (do wyboru: Internista / Pediatra / Psychiatra / Inni specjaliści / Wszyscy)
- Pacjenci: Spoza nowych kampanii (do wyboru: Spoza nowych kampanii / Nowe kampanie na L4 / Wszyscy)
- Opóźnienie: ponad 15 minut (do wyboru: ponad 15 minut / ponad 30 minut)
- Wygładzenie: suma z 28 dni (do wyboru: dzień / suma z 7 dni / suma z 28 dni)
- Wyróżnij porę: Rano (6–11) (do wyboru: Rano (6–11) / Południe (12–15) / Wieczór (16–23) / Noc (0–5))

*Wykres: odsetek wizyt spóźnionych w wybranej specjalizacji, osobno dla każdej pory, z liczbą wizyt w legendzie.*

*[Wykres] serie: brak*

Najedź na wykres, żeby zobaczyć wartości.

Rano (6–11)

Południe (12–15)

Wieczór (16–23)

Noc (0–5)

1. 13.11.2025: Więcej zwrotów po wizycie
2. 24.11.2025: Poranne opóźnienia u internisty

Zdarzenia ze wszystkich obszarów (14)

| Specjalizacja | Pora terminu | Spóźnione ponad 15 minut: ostatnie 12 miesięcy (X 2025 – IX 2026), pod spodem rok wcześniej |
| --- | --- | --- |
| Internista | Rano (6–11) | 41,2% z 6 522<br>rok wcześniej: 6,0% z 5 219<br>+35,3<br>gorzej |
| Internista | Południe (12–15) | 8,9% z 3 748<br>rok wcześniej: 3,0% z 2 974<br>+5,9<br>gorzej |
| Internista | Wieczór (16–23) | 2,6% z 8 852<br>rok wcześniej: 2,8% z 7 027<br>−0,3<br>lepiej |
| Internista | Noc (0–5) | 5,7% z 1 418<br>rok wcześniej: 1,9% z 1 322<br>+3,8<br>gorzej |
| Pediatra | Rano (6–11) | 3,8% z 393<br>rok wcześniej: 4,0% z 326<br>−0,2<br>lepiej |
| Pediatra | Południe (12–15) | 2,0% z 245<br>rok wcześniej: 2,7% z 187<br>−0,6<br>lepiej |
| Pediatra | Wieczór (16–23) | 2,1% z 621<br>rok wcześniej: 2,5% z 529<br>−0,4<br>lepiej |
| Pediatra | Noc (0–5) | 1,9% z 104<br>rok wcześniej: 1,2% z 82<br>+0,7<br>gorzej |
| Psychiatra | Rano (6–11) | 3,7% z 481<br>rok wcześniej: 3,2% z 349<br>+0,6<br>gorzej |
| Psychiatra | Południe (12–15) | 3,5% z 257<br>rok wcześniej: 4,5% z 200<br>−1,0<br>lepiej |
| Psychiatra | Wieczór (16–23) | 2,8% z 608<br>rok wcześniej: 3,1% z 448<br>−0,3<br>lepiej |
| Psychiatra | Noc (0–5) | 2,5% z 79<br>rok wcześniej: 3,8% z 78<br>−1,3<br>lepiej |
| Inni specjaliści | Rano (6–11) | 2,6% z 1 625<br>rok wcześniej: 2,4% z 1 274<br>+0,2<br>gorzej |
| Inni specjaliści | Południe (12–15) | 2,7% z 1 051<br>rok wcześniej: 2,3% z 826<br>+0,4<br>gorzej |
| Inni specjaliści | Wieczór (16–23) | 2,9% z 2 459<br>rok wcześniej: 2,1% z 1 913<br>+0,8<br>gorzej |
| Inni specjaliści | Noc (0–5) | 1,9% z 360<br>rok wcześniej: 2,4% z 328<br>−0,5<br>lepiej |

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Wizyty u internisty z terminem 6:00–11:59, pacjenci spoza nowych kampanii: 4,7–6,9% miesięcznie do X 2025, 15,7% w XI 2025 (521 wizyt), 29,7% w XII 2025, 42,6% w I 2026 i 47,3–52,7% od II do IX 2026. W całym roku: 41,2% z 6 522 wizyt wobec 6,0% z 5 219 wizyt rok wcześniej.

U internisty w innych porach (pacjenci spoza nowych kampanii): 4,6% wizyt spóźnionych ponad 15 minut w ostatnich 12 miesiącach (14 018 wizyt) wobec 2,8% rok wcześniej (11 323 wizyty).

U pozostałych lekarzy rano (wszyscy pacjenci): 3,0% z 2 757 wizyt wobec 2,8% z 1 949 wizyt rok wcześniej; przedział różnicy obejmuje zero.

Długość wizyty i czas od zapłaty do terminu się nie zmieniają.

Opóźnienie to faktyczny start wizyty minus umówiony termin. Liczymy tylko wizyty odbyte, a dzień i porę według terminu. Pacjenci nowych kampanii na L4 to pacjenci kampanii meta_prosp_l4_szybko i tt_prosp_l4_15min według pierwszego wejścia; „spoza nowych kampanii” to wszyscy pozostali.

Skąd liczby: analiza/a5r_punktualnosc.py → analiza/wyniki/a5r_punktualnosc.txt; analiza/wyniki/d_retencja.txt (punkt 1); eksport analiza/b_eksport.py.

### Opóźnienia u internisty skupiają się w jednym porannym bloku od 5:00 do 13:59

Od 6:00 do 10:59 ponad 15 minut po terminie zaczyna się 40–47% wizyt u internisty, a poza blokiem 5:00–13:59 prawie tyle samo co rok wcześniej.

*[Wykres: Internista] Internista: odsetek wizyt spóźnionych ponad 15 minut według godziny terminu, rok wcześniej i ostatnie 12 miesięcy*

- 0:00–0:59, internista: rok wcześniej 1,1% (4 z 359 wizyt), ostatnie 12 miesięcy 3,0% (17 z 559 wizyt)
- 1:00–1:59, internista: rok wcześniej 3,0% (6 z 198 wizyt), ostatnie 12 miesięcy 3,8% (11 z 291 wizyt)
- 2:00–2:59, internista: rok wcześniej 2,8% (4 z 145 wizyt), ostatnie 12 miesięcy 2,8% (6 z 214 wizyt)
- 3:00–3:59, internista: rok wcześniej 3,6% (6 z 166 wizyt), ostatnie 12 miesięcy 4,0% (9 z 224 wizyt)
- 4:00–4:59, internista: rok wcześniej 0,5% (1 z 187 wizyt), ostatnie 12 miesięcy 1,8% (5 z 276 wizyt)
- 5:00–5:59, internista: rok wcześniej 1,5% (4 z 267 wizyt), ostatnie 12 miesięcy 15,3% (70 z 459 wizyt); blok poranny
- 6:00–6:59, internista: rok wcześniej 5,7% (27 z 473 wizyt), ostatnie 12 miesięcy 45,3% (392 z 865 wizyt); blok poranny
- 7:00–7:59, internista: rok wcześniej 6,9% (55 z 799 wizyt), ostatnie 12 miesięcy 44,3% (672 z 1 517 wizyt); blok poranny
- 8:00–8:59, internista: rok wcześniej 6,0% (61 z 1 021 wizyt), ostatnie 12 miesięcy 47,0% (873 z 1 858 wizyt); blok poranny
- 9:00–9:59, internista: rok wcześniej 7,5% (79 z 1 055 wizyt), ostatnie 12 miesięcy 45,3% (835 z 1 844 wizyt); blok poranny
- 10:00–10:59, internista: rok wcześniej 5,9% (61 z 1 037 wizyt), ostatnie 12 miesięcy 40,4% (688 z 1 704 wizyt); blok poranny
- 11:00–11:59, internista: rok wcześniej 3,4% (28 z 834 wizyt), ostatnie 12 miesięcy 36,2% (493 z 1 363 wizyt); blok poranny
- 12:00–12:59, internista: rok wcześniej 3,4% (26 z 774 wizyt), ostatnie 12 miesięcy 22,3% (291 z 1 303 wizyt); blok poranny
- 13:00–13:59, internista: rok wcześniej 2,5% (18 z 719 wizyt), ostatnie 12 miesięcy 5,6% (68 z 1 207 wizyt)
- 14:00–14:59, internista: rok wcześniej 2,3% (16 z 699 wizyt), ostatnie 12 miesięcy 3,0% (34 z 1 131 wizyt)
- 15:00–15:59, internista: rok wcześniej 3,8% (30 z 782 wizyt), ostatnie 12 miesięcy 2,9% (32 z 1 113 wizyt)
- 16:00–16:59, internista: rok wcześniej 2,8% (21 z 749 wizyt), ostatnie 12 miesięcy 2,0% (25 z 1 245 wizyt)
- 17:00–17:59, internista: rok wcześniej 2,1% (18 z 862 wizyt), ostatnie 12 miesięcy 3,2% (43 z 1 356 wizyt)
- 18:00–18:59, internista: rok wcześniej 2,8% (27 z 954 wizyt), ostatnie 12 miesięcy 2,2% (33 z 1 529 wizyt)
- 19:00–19:59, internista: rok wcześniej 3,0% (31 z 1 026 wizyt), ostatnie 12 miesięcy 2,6% (42 z 1 608 wizyt)
- 20:00–20:59, internista: rok wcześniej 4,0% (44 z 1 093 wizyt), ostatnie 12 miesięcy 2,5% (42 z 1 648 wizyt)
- 21:00–21:59, internista: rok wcześniej 2,7% (26 z 953 wizyt), ostatnie 12 miesięcy 2,7% (39 z 1 455 wizyt)
- 22:00–22:59, internista: rok wcześniej 2,6% (20 z 775 wizyt), ostatnie 12 miesięcy 2,7% (34 z 1 261 wizyt)
- 23:00–23:59, internista: rok wcześniej 1,8% (11 z 615 wizyt), ostatnie 12 miesięcy 2,6% (26 z 988 wizyt)

*[Wykres: Pozostali lekarze] Pozostali lekarze: odsetek wizyt spóźnionych ponad 15 minut według godziny terminu, rok wcześniej i ostatnie 12 miesięcy*

- 0:00–0:59, pozostali lekarze: rok wcześniej 2,3% (4 z 176 wizyt), ostatnie 12 miesięcy 3,9% (8 z 204 wizyt)
- 1:00–1:59, pozostali lekarze: rok wcześniej 3,0% (2 z 66 wizyt), ostatnie 12 miesięcy 2,2% (2 z 91 wizyt)
- 2:00–2:59, pozostali lekarze: rok wcześniej 1,7% (1 z 60 wizyt), ostatnie 12 miesięcy 0,0% (0 z 51 wizyt)
- 3:00–3:59, pozostali lekarze: rok wcześniej 1,9% (1 z 53 wizyt), ostatnie 12 miesięcy 1,7% (1 z 59 wizyt)
- 4:00–4:59, pozostali lekarze: rok wcześniej 2,0% (1 z 49 wizyt), ostatnie 12 miesięcy 0,0% (0 z 77 wizyt)
- 5:00–5:59, pozostali lekarze: rok wcześniej 3,6% (3 z 84 wizyt), ostatnie 12 miesięcy 1,8% (2 z 113 wizyt); blok poranny
- 6:00–6:59, pozostali lekarze: rok wcześniej 0,7% (1 z 139 wizyt), ostatnie 12 miesięcy 3,3% (8 z 246 wizyt); blok poranny
- 7:00–7:59, pozostali lekarze: rok wcześniej 3,2% (10 z 312 wizyt), ostatnie 12 miesięcy 2,8% (12 z 423 wizyt); blok poranny
- 8:00–8:59, pozostali lekarze: rok wcześniej 4,4% (16 z 367 wizyt), ostatnie 12 miesięcy 3,3% (18 z 545 wizyt); blok poranny
- 9:00–9:59, pozostali lekarze: rok wcześniej 2,9% (11 z 376 wizyt), ostatnie 12 miesięcy 2,4% (14 z 574 wizyt); blok poranny
- 10:00–10:59, pozostali lekarze: rok wcześniej 1,8% (7 z 382 wizyt), ostatnie 12 miesięcy 3,4% (17 z 495 wizyt); blok poranny
- 11:00–11:59, pozostali lekarze: rok wcześniej 2,4% (9 z 373 wizyt), ostatnie 12 miesięcy 3,2% (15 z 474 wizyt); blok poranny
- 12:00–12:59, pozostali lekarze: rok wcześniej 3,5% (11 z 312 wizyt), ostatnie 12 miesięcy 3,5% (15 z 426 wizyt); blok poranny
- 13:00–13:59, pozostali lekarze: rok wcześniej 2,4% (7 z 296 wizyt), ostatnie 12 miesięcy 1,9% (8 z 420 wizyt)
- 14:00–14:59, pozostali lekarze: rok wcześniej 2,3% (7 z 300 wizyt), ostatnie 12 miesięcy 2,7% (11 z 410 wizyt)
- 15:00–15:59, pozostali lekarze: rok wcześniej 2,6% (8 z 305 wizyt), ostatnie 12 miesięcy 2,9% (12 z 410 wizyt)
- 16:00–16:59, pozostali lekarze: rok wcześniej 2,4% (8 z 328 wizyt), ostatnie 12 miesięcy 2,5% (10 z 393 wizyt)
- 17:00–17:59, pozostali lekarze: rok wcześniej 2,5% (9 z 365 wizyt), ostatnie 12 miesięcy 2,0% (9 z 455 wizyt)
- 18:00–18:59, pozostali lekarze: rok wcześniej 2,1% (8 z 389 wizyt), ostatnie 12 miesięcy 3,4% (20 z 584 wizyt)
- 19:00–19:59, pozostali lekarze: rok wcześniej 2,3% (10 z 440 wizyt), ostatnie 12 miesięcy 3,3% (19 z 572 wizyt)
- 20:00–20:59, pozostali lekarze: rok wcześniej 1,6% (7 z 436 wizyt), ostatnie 12 miesięcy 2,0% (12 z 588 wizyt)
- 21:00–21:59, pozostali lekarze: rok wcześniej 2,7% (10 z 371 wizyt), ostatnie 12 miesięcy 2,8% (15 z 544 wizyt)
- 22:00–22:59, pozostali lekarze: rok wcześniej 3,0% (10 z 331 wizyt), ostatnie 12 miesięcy 2,8% (13 z 458 wizyt)
- 23:00–23:59, pozostali lekarze: rok wcześniej 2,2% (5 z 230 wizyt), ostatnie 12 miesięcy 2,2% (7 z 320 wizyt)

Odsetek wizyt odbytych, które zaczęły się ponad 15 minut po terminie, według godziny terminu. Ta sama skala w obu wykresach.

Najmocniej rośnie od 6:00 do 11:59. Wzrost w porach „południe” i „noc” z karty wyżej to głównie brzegi bloku: godziny 12:00 i 5:00, a o 13:00 już niewiele.

U pozostałych lekarzy żadna godzina wyraźnie nie odstaje.

**Tabela z liczbami** *(sekcja rozwijana, tu rozwinięta)*

*Opóźnienia według godziny terminu: wizyty spóźnione ponad 15 minut (w nawiasie liczba wizyt odbytych)*

| Godzina terminu | Internista, rok wcześniej | Internista, ostatnie 12 miesięcy | Internista: zmiana (punkty procentowe) | Pozostali lekarze, rok wcześniej | Pozostali lekarze, ostatnie 12 miesięcy |
| --- | --- | --- | --- | --- | --- |
| 0:00–0:59 | 1,1% (359) | 3,0% (559) | +1,9 | 2,3% (176) | 3,9% (204) |
| 1:00–1:59 | 3,0% (198) | 3,8% (291) | +0,7 | 3,0% (66) | 2,2% (91) |
| 2:00–2:59 | 2,8% (145) | 2,8% (214) | 0,0 | 1,7% (60) | 0,0% (51) |
| 3:00–3:59 | 3,6% (166) | 4,0% (224) | +0,4 | 1,9% (53) | 1,7% (59) |
| 4:00–4:59 | 0,5% (187) | 1,8% (276) | +1,3 | 2,0% (49) | 0,0% (77) |
| 5:00–5:59 | 1,5% (267) | 15,3% (459) | +13,8 | 3,6% (84) | 1,8% (113) |
| 6:00–6:59 | 5,7% (473) | 45,3% (865) | +39,6 | 0,7% (139) | 3,3% (246) |
| 7:00–7:59 | 6,9% (799) | 44,3% (1 517) | +37,4 | 3,2% (312) | 2,8% (423) |
| 8:00–8:59 | 6,0% (1 021) | 47,0% (1 858) | +41,0 | 4,4% (367) | 3,3% (545) |
| 9:00–9:59 | 7,5% (1 055) | 45,3% (1 844) | +37,8 | 2,9% (376) | 2,4% (574) |
| 10:00–10:59 | 5,9% (1 037) | 40,4% (1 704) | +34,5 | 1,8% (382) | 3,4% (495) |
| 11:00–11:59 | 3,4% (834) | 36,2% (1 363) | +32,8 | 2,4% (373) | 3,2% (474) |
| 12:00–12:59 | 3,4% (774) | 22,3% (1 303) | +19,0 | 3,5% (312) | 3,5% (426) |
| 13:00–13:59 | 2,5% (719) | 5,6% (1 207) | +3,1 | 2,4% (296) | 1,9% (420) |
| 14:00–14:59 | 2,3% (699) | 3,0% (1 131) | +0,7 | 2,3% (300) | 2,7% (410) |
| 15:00–15:59 | 3,8% (782) | 2,9% (1 113) | −1,0 | 2,6% (305) | 2,9% (410) |
| 16:00–16:59 | 2,8% (749) | 2,0% (1 245) | −0,8 | 2,4% (328) | 2,5% (393) |
| 17:00–17:59 | 2,1% (862) | 3,2% (1 356) | +1,1 | 2,5% (365) | 2,0% (455) |
| 18:00–18:59 | 2,8% (954) | 2,2% (1 529) | −0,7 | 2,1% (389) | 3,4% (584) |
| 19:00–19:59 | 3,0% (1 026) | 2,6% (1 608) | −0,4 | 2,3% (440) | 3,3% (572) |
| 20:00–20:59 | 4,0% (1 093) | 2,5% (1 648) | −1,5 | 1,6% (436) | 2,0% (588) |
| 21:00–21:59 | 2,7% (953) | 2,7% (1 455) | 0,0 | 2,7% (371) | 2,8% (544) |
| 22:00–22:59 | 2,6% (775) | 2,7% (1 261) | +0,1 | 3,0% (331) | 2,8% (458) |
| 23:00–23:59 | 1,8% (615) | 2,6% (988) | +0,8 | 2,2% (230) | 2,2% (320) |

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

- o 5:00: 15,3% z 459 wizyt, rok wcześniej 1,5% z 267;
- od 6:00 do 10:59: od 40,4% do 47,0% (865–1 858 wizyt w godzinie), rok wcześniej 5,7–7,5%;
- o 11:00: 36,2% z 1 363 wizyt, rok wcześniej 3,4% z 834;
- o 12:00: 22,3% z 1 303 wizyt, rok wcześniej 3,4% z 774;
- o 13:00: 5,6% z 1 207 wizyt, rok wcześniej 2,5% z 719;
- poza 5:00–13:59: 2,7% z 14 898 wizyt, rok wcześniej 2,8% z 9 563.

Bez godziny 12:00 południe rośnie tylko z 2,9% do 3,9%, a noc bez 5:00 z 2,0% do 3,1%.

Wszyscy pacjenci; oba lata liczymy według dnia terminu wizyty.

Skąd liczby: analiza/d_retencja.py → analiza/wyniki/d_retencja.txt (punkt 1).

### Przy tym samym porannym ruchu opóźnień jest dużo więcej niż rok wcześniej

W dni z tą samą liczbą porannych wizyt u internisty spóźnionych jest średnio o 26 punktów procentowych więcej wizyt niż rok wcześniej.

Rok wcześniej opóźnienia nie zależały od ruchu. Dziś dni z większym ruchem w tym samym miesiącu też prawie nie mają ich więcej.

Już pierwsza poranna wizyta dnia jest spóźniona prawie tak często jak kolejne: 42% wobec 43%. To bardziej pasuje do stałego przesunięcia od początku dnia (późniejszy start względem grafiku albo inna organizacja zapisów) niż do kolejki, która narasta w ciągu poranka.

**Zastrzeżenie.** To nasze odczytanie danych. Najwcześniejszy termin dnia liczymy dla całej sieci, bo w danych nie ma identyfikatorów lekarzy ani grafików (Czego nie wiemy, punkt 4).

*Filtry (ustawienia domyślne):*
- Pacjenci: Wszyscy (do wyboru: Wszyscy / Spoza nowych kampanii)

*[Wykres] Odsetek porannych wizyt u internisty spóźnionych ponad 15 minut według ruchu porannego w dniu: rok wcześniej i ostatnie 12 miesięcy*

- 9–12 wizyt: rok wcześniej 4,7%, ostatnie 12 miesięcy 15,1% [+10,4 pkt proc. gorzej]
- 13–16 wizyt: rok wcześniej 6,8%, ostatnie 12 miesięcy 22,4% [+15,6 pkt proc. gorzej]
- 17–20 wizyt: rok wcześniej 6,0%, ostatnie 12 miesięcy 30,6% [+24,6 pkt proc. gorzej]
- 21–24 wizyt: rok wcześniej 4,8%, ostatnie 12 miesięcy 39,6% [+34,7 pkt proc. gorzej]
- 25–28 wizyt: rok wcześniej 8,3%, ostatnie 12 miesięcy 46,9% [+38,6 pkt proc. gorzej]

*Odsetek porannych wizyt u internisty (6:00–11:59) spóźnionych ponad 15 minut, w dniach z takim samym ruchem porannym.*

**Tabela z liczbami** *(sekcja rozwijana, tu rozwinięta)*

| Poranne wizyty u internisty w dniu | Spóźnione ponad 15 minut: ostatnie 12 miesięcy (X 2025 – IX 2026), pod spodem rok wcześniej | Dni z takim ruchem |
| --- | --- | --- |
| do 8 | —<br>rok wcześniej: 6,2% z 178 | —<br>rok wcześniej: 29 |
| 9–12 | 15,1% z 86<br>rok wcześniej: 4,7% z 973<br>+10,4<br>gorzej | 8<br>rok wcześniej: 94 |
| 13–16 | 22,4% z 438<br>rok wcześniej: 6,8% z 1 602<br>+15,6<br>gorzej | 30<br>rok wcześniej: 113 |
| 17–20 | 30,6% z 1 054<br>rok wcześniej: 6,0% z 1 580<br>+24,6<br>gorzej | 58<br>rok wcześniej: 89 |
| 21–24 | 39,6% z 1 347<br>rok wcześniej: 4,8% z 681<br>+34,7<br>gorzej | 61<br>rok wcześniej: 32 |
| 25–28 | 46,9% z 2 013<br>rok wcześniej: 8,3% z 205<br>+38,6<br>gorzej | 78<br>rok wcześniej: 8 |
| 29–32 | 46,6% z 1 746<br>rok wcześniej: — | 59<br>rok wcześniej: — |
| 33–40 | 49,6% z 2 296<br>rok wcześniej: — | 67<br>rok wcześniej: — |
| 41 i więcej | 52,0% z 171<br>rok wcześniej: — | 4<br>rok wcześniej: — |

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Porównanie obejmuje 5 przedziałów ruchu obecnych w obu latach (9 979 wizyt); różnica to 26,4 punktu procentowego. Na przykład w dni z 17–20 porannymi wizytami spóźnionych było 6,0% wizyt rok wcześniej (89 dni) i 30,6% w ostatnich 12 miesiącach (58 dni).

Rok wcześniej opóźnienia nie zależą od ruchu (4,7–8,3% w każdym przedziale). W obrębie miesiąca dni z większym ruchem prawie nie mają więcej opóźnień: w tercylach dni według ruchu 5,4%, 6,1%, 6,1% rok wcześniej i 42,1%, 43,5%, 43,6% w ostatnich 12 miesiącach. Mediana ruchu porannego to 15 wizyt na dzień rok wcześniej i 26 w ostatnich 12 miesiącach.

Wizyty z najwcześniejszym porannym terminem dnia są spóźnione ponad 15 minut w 41,9% (391 wizyt), kolejne w 43,3% (8 760 wizyt), średnio 18,7 wobec 20,2 minuty (ostatnie 12 miesięcy). W tym samym miesiącu (II–IX 2026) godziny z 8 i więcej wizytami mają o 4,2 punktu procentowego więcej spóźnionych niż godziny z 1–3 wizytami.

Ruch poranny w dniu to wszystkie nieanulowane wizyty u internisty z terminem 6:00–11:59 tego dnia. Dni grupujemy według tego ruchu i w każdej grupie porównujemy odsetek porannych wizyt spóźnionych ponad 15 minut w obu latach.

Skąd liczby: analiza/a5r_punktualnosc.py → analiza/wyniki/a5r_punktualnosc.txt (sekcje 3f–3g); analiza/wyniki/d_retencja.txt (punkt 2); eksport analiza/b_eksport.py.

### Po spóźnionej pierwszej wizycie pacjenci wracają rzadziej

W ostatnich 12 miesiącach po porannej wizycie u internisty zaczętej ponad 30 minut po terminie wraca w 90 dniach 10% pacjentów, a po wizycie punktualnej 27%.

Powrót spada z każdym przedziałem opóźnienia. Spóźnionych pierwszych wizyt rano jest dziś dużo więcej niż rok wcześniej (karty wyżej).

Tabela pokazuje też rok wcześniej, ale wtedy spóźnionych pierwszych wizyt rano było mało, więc tych porównań nie oceniamy.

**Zastrzeżenie.** To porównanie obserwacyjne: pacjenci spóźnionych wizyt mogą różnić się od pozostałych także czymś, czego w danych nie widać.

*Filtry (ustawienia domyślne):*
- Pierwsza wizyta: Internista rano (6–11) (do wyboru: Internista rano (6–11) / Internista, każda pora / Wszystkie)
- Pacjenci (według pierwszego wejścia): Spoza nowych kampanii (do wyboru: Spoza nowych kampanii / Nowe kampanie na L4 / Wszyscy)

| Opóźnienie pierwszej wizyty | Powrót w 90 dniach: kohorty 1.10.2025–2.07.2026, pod spodem te same dni rok wcześniej (1.10.2024–2.07.2025) |
| --- | --- |
| Do 5 minut po terminie | 27,0% z 826<br>rok wcześniej: 24,9% z 1 415<br>+2,1 |
| Ponad 5 do 15 minut | 19,9% z 977<br>rok wcześniej: 23,2% z 1 071<br>−3,4 |
| Ponad 15 do 30 minut | 16,0% z 557<br>rok wcześniej: 22,2% z 135<br>−6,2 |
| Ponad 30 minut | 10,1% z 533<br>rok wcześniej: 14,3% z 35<br>−4,2 |
| Brak wizyty (anulowana, nieodebrana) | 14,7% z 224<br>rok wcześniej: 19,1% z 188<br>−4,4 |

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

- do 5 minut po terminie: 27,0% z 826 pacjentów;
- ponad 5 do 15 minut: 19,9% z 977 pacjentów;
- ponad 15 do 30 minut: 16,0% z 557 pacjentów;
- ponad 30 minut: 10,1% z 533 pacjentów;
- brak wizyty (anulowana albo nieodebrana): 14,7% z 224 pacjentów.

Wniosek opieramy na ostatnich 12 miesiącach. Rok wcześniej pacjentów ze spóźnioną pierwszą wizytą rano było 135 przy 15–30 minutach i 35 powyżej 30 minut.

Pierwsza wizyta u internisty z terminem 6:00–11:59, pacjenci spoza nowych kampanii według pierwszego wejścia. Powrót w 90 dniach na tych samych dniach kalendarzowych, tylko kohorty z pełnym oknem: od 1.10.2025 do 2.07.2026 i rok wcześniej od 1.10.2024 do 2.07.2025.

Skąd liczby: analiza/a5r_punktualnosc.py → analiza/wyniki/a5r_punktualnosc.txt (1f); tabela pod kartą z danych kohort strony.

### Zwroty po wizycie skupiają się w L4 z nowych kampanii

W ostatnich 12 miesiącach zwrot po odbytej wizycie dostaje 17% wizyt L4 pacjentów nowych kampanii, a u pozostałych pacjentów 5%.

Rok wcześniej, bez nowych kampanii, zwrot dostawało 6% wizyt L4, więc u pozostałych pacjentów odsetek nie wzrósł.

Lekarz dostaje wynagrodzenie także za wizytę, za którą zwracamy pieniądze. U pacjentów nowych kampanii to w ostatnich 12 miesiącach 84 tys. zł zwróconych zapłat i 34 tys. zł kosztu lekarza.

**Zastrzeżenie.** Powodu zwrotu w danych nie ma. To, że lekarz nie wystawia L4, którego pacjent oczekuje po obietnicy reklamy, jest hipotezą (Czego nie wiemy, punkt 3).

*Filtry (ustawienia domyślne):*
- Pacjenci: Wszyscy (do wyboru: Wszyscy / Nowe kampanie na L4 / Spoza nowych kampanii)
- Zamówienia: Wszystkie (do wyboru: Wszystkie / Pierwsze / Kolejne)
- Wygładzenie: suma z 28 dni (do wyboru: dzień / suma z 7 dni / suma z 28 dni)
- Wyróżnij cel: L4 (do wyboru: L4 / E-recepta / Konsultacja / Skierowanie)

*Wykres: odsetek odbytych wizyt, za które pacjent dostał zwrot po wizycie, według celu wizyty i dnia płatności. Tabela: ostatnie 12 miesięcy wobec roku wcześniej.*

*[Wykres] serie: brak*

Najedź na wykres, żeby zobaczyć wartości.

L4

E-recepta

Konsultacja

Skierowanie

1. 13.11.2025: Więcej zwrotów po wizycie
2. 24.11.2025: Poranne opóźnienia u internisty

Zdarzenia ze wszystkich obszarów (14)

| Cel wizyty | Zwrot po odbytej wizycie | Anulowane przed wizytą | Pacjent nie odebrał | Zwrócone zapłaty | Koszt lekarza za zwrócone wizyty |
| --- | --- | --- | --- | --- | --- |
| L4 | 11,8% z 10 975<br>rok wcześniej: 6,0% z 4 474<br>+5,8<br>gorzej | 4,2% z 11 777<br>rok wcześniej: 4,5% z 4 815<br>−0,4<br>lepiej | 2,6% z 11 777<br>rok wcześniej: 2,5% z 4 815<br>+0,1<br>gorzej | 105 743 zł<br>rok wcześniej: 23 637 zł | 40 575 zł<br>rok wcześniej: 7 900 zł |
| E-recepta | 1,3% z 11 295<br>rok wcześniej: 1,2% z 8 091<br>+0,1<br>gorzej | 3,9% z 12 093<br>rok wcześniej: 4,3% z 8 677<br>−0,4<br>lepiej | 2,7% z 12 093<br>rok wcześniej: 2,5% z 8 677<br>+0,2<br>gorzej | 14 223 zł<br>rok wcześniej: 9 276 zł | 7 625 zł<br>rok wcześniej: 4 650 zł |
| Konsultacja | 1,3% z 10 764<br>rok wcześniej: 1,3% z 8 245<br>0,0 | 3,9% z 11 498<br>rok wcześniej: 3,8% z 8 791<br>+0,1<br>gorzej | 2,5% z 11 498<br>rok wcześniej: 2,4% z 8 791<br>+0,1<br>gorzej | 15 593 zł<br>rok wcześniej: 11 438 zł | 11 325 zł<br>rok wcześniej: 7 650 zł |
| Skierowanie | 1,3% z 2 926<br>rok wcześniej: 0,8% z 2 285<br>+0,5<br>gorzej | 4,1% z 3 123<br>rok wcześniej: 4,2% z 2 433<br>−0,1<br>lepiej | 2,2% z 3 123<br>rok wcześniej: 1,8% z 2 433<br>+0,4<br>gorzej | 2 973 zł<br>rok wcześniej: 1 534 zł | 1 025 zł<br>rok wcześniej: 525 zł |
| Razem | 4,5% z 35 960<br>rok wcześniej: 2,1% z 23 095<br>+2,4<br>gorzej | 4,0% z 38 491<br>rok wcześniej: 4,2% z 24 716<br>−0,2<br>lepiej | 2,6% z 38 491<br>rok wcześniej: 2,4% z 24 716<br>+0,2<br>gorzej | 138 532 zł<br>rok wcześniej: 45 884 zł | 60 550 zł<br>rok wcześniej: 20 725 zł |

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Ostatnie 12 miesięcy: 17,4% z 5 895 wizyt L4 pacjentów nowych kampanii i 5,3% z 5 080 wizyt L4 pozostałych pacjentów. Rok wcześniej: 6,0% z 4 474 wizyt L4.

Zwroty po wizycie u pacjentów nowych kampanii w ostatnich 12 miesiącach: 1 044 wizyty we wszystkich celach wizyty, z tego 1 024 przy wizytach L4 (te liczy pozycja 5 listy priorytetów), 84 112 zł zwróconych zapłat i 33 975 zł kosztu lekarza.

Odsetek zwrotów liczymy wśród odbytych wizyt, według dnia płatności.

Skąd liczby: analiza/a5r_po_zakupie.py → analiza/wyniki/a5r_po_zakupie.txt (2b); eksport analiza/b_eksport.py.

### Wizyty spóźnione ponad 30 minut dostają dużo gorsze oceny

W ostatnich 12 miesiącach wizyta u internisty zaczęta ponad 30 minut po terminie dostaje średnio 2,92, a wizyta punktualna 4,45 (skala 1–5).

Po takim opóźnieniu 32% ocen to 1 albo 2, a po wizycie punktualnej 1%.

**Zastrzeżenie.** Ocenę dostaje tylko 31% odbytych wizyt, więc oceny pokazują tylko kierunek.

*Filtry (ustawienia domyślne):*
- Specjalizacja: Internista (do wyboru: Internista / Pediatra / Psychiatra / Inni specjaliści / Wszyscy)
- Pacjenci: Spoza nowych kampanii (do wyboru: Spoza nowych kampanii / Nowe kampanie na L4 / Wszyscy)

| Opóźnienie wizyty | Odsetek ocenionych | Średnia ocena (1–5) | Oceny 1–2 |
| --- | --- | --- | --- |
| Do 5 minut po terminie | 31,3% z 11 007<br>rok wcześniej: 31,9% z 10 534<br>−0,6<br>gorzej | 4,45 z 3 446<br>rok wcześniej: 4,47 z 3 361<br>−0,02<br>gorzej | 1,1% z 3 446<br>rok wcześniej: 1,2% z 3 361<br>−0,2<br>lepiej |
| Ponad 5 do 15 minut | 30,8% z 6 198<br>rok wcześniej: 33,4% z 5 394<br>−2,6<br>gorzej | 4,38 z 1 909<br>rok wcześniej: 4,37 z 1 802<br>+0,01<br>lepiej | 1,5% z 1 909<br>rok wcześniej: 1,7% z 1 802<br>−0,3<br>lepiej |
| Ponad 15 do 30 minut | 31,7% z 1 786<br>rok wcześniej: 30,3% z 492<br>+1,4<br>lepiej | 3,69 z 566<br>rok wcześniej: 3,82 z 149<br>−0,13<br>gorzej | 8,7% z 566<br>rok wcześniej: 6,7% z 149<br>+1,9<br>gorzej |
| Ponad 30 minut | 30,3% z 1 550<br>rok wcześniej: 33,3% z 132<br>−3,1<br>gorzej | 2,92 z 469<br>rok wcześniej: 2,95 z 44<br>−0,03<br>gorzej | 31,8% z 469<br>rok wcześniej: 31,8% z 44<br>0,0 |

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Internista, pacjenci spoza nowych kampanii, ostatnie 12 miesięcy: przy opóźnieniu ponad 30 minut średnia 2,92 z 469 ocen, przy wizycie zaczętej do 5 minut po terminie 4,45 z 3 446 ocen. Ocenę dostało 11 234 z 35 960 wizyt odbytych w ostatnich 12 miesiącach (wszyscy lekarze i pacjenci).

Rok wcześniej średnia przy opóźnieniu ponad 30 minut była podobna (2,95), ale z 44 ocen, więc porównania z rokiem wcześniej nie interpretujemy.

Skąd liczby: analiza/a5r_po_zakupie.py → analiza/wyniki/a5r_po_zakupie.txt (3a); eksport analiza/b_eksport.py.

Dalej: Zdarzenia

# Zakładka 5: Zdarzenia (`#zdarzenia`)

## Oś zdarzeń: co się stało i kiedy

### Większość zmian zaczyna się między listopadem 2025 a marcem 2026

W tych miesiącach ruszają dwie nowe kampanie na L4, rosną poranne opóźnienia u internistów i psuje się zakładanie konta w Safari na iOS.

Listy zmian w produkcie i kalendarza kampanii nie mamy, więc każde zdarzenie znaleźliśmy w danych. Przy każdym jest data, co się zmieniło, o ile i skąd to wiemy.

**Zastrzeżenie.** Zdarzenia z tych samych miesięcy nakładają się, więc bez testu nie rozdzielamy ich skutków.

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Tory na osi: lejek (pozyskanie), retencja (kohorty), obsługa pacjenta (przebieg wizyt) i jakość danych. Metoda wykrywania zmian dzieli serię dzienną na odcinki o różnym poziomie (podział binarny); zmianę uznajemy, gdy różnica poziomów wynosi co najmniej 4 błędy standardowe (|z| ≥ 4). Daty to kandydaci zmian; każdego sprawdzamy potem na danych.

### Zdarzenia na osi czasu

*Filtry (ustawienia domyślne):*
- ☑ Lejek (6)
- ☑ Retencja (4)
- ☑ Obsługa pacjenta (2)
- ☑ Jakość danych (2)

start kampanii

awaria, błąd albo luka w danych

zmiana

kandydat poniżej progu

zdarzenie z datą początku i końca

*[Oś czasu, rysunek] tory: Lejek, Retencja, Obsługa pacjenta, Jakość danych; znaczników zdarzeń: 14*

*1. 17.05.2025 · Jakość danych · luka w danych*

### Jednej godziny prawie nie ma w danych, ale wyników to nie zmienia

**Co się zmieniło:**
17.05.2025 od 13:00 do 14:00 jest 1 sesja zamiast typowych 21 (mediana tej samej godziny w 15 dniach wokół) i 0 zamówień. To jedyna taka godzina w dwóch latach.

**O ile:**
Zamówień w tej godzinie jest zwykle około 2, więc ich brak niewiele mówi. Nie wiemy, czy to przerwa w działaniu strony, czy w zbieraniu danych. Wpływ na wyniki jest pomijalny.

Zobacz w jakości danych

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Liczba sesji i zamówień w każdej godzinie wobec mediany tej samej godziny w 15 dniach wokół. Źródło: analiza/a2_jakosc.py, sekcja o lukach; analiza/wyniki/e_merytoryka.txt, punkt 5e.

*2. 8.09.2025 · Lejek · start kampanii*

### Newsletter zaczyna sprzedawać samo TelemediGO, a pierwsze tygodnie dają jednorazowy skok sprzedaży

**Co się zmieniło:**
Newsletter do pacjentów, którzy już kupowali, prowadzi na stronę /telemedigo. Pojawiają się zakupy samego TelemediGO, bez konsultacji.

**O ile:**
W pierwszych 23 dniach newsletter sprzedał 225 członkostw, a przy późniejszym tempie sprzedałby około 29. Ta jednorazowa nadwyżka (196 zakupów, 17,4 tys. zł) podnosi marżę III kwartału 2025, z którą porównujemy III kwartał 2026. Razem: 686 zakupów samego TelemediGO do 30.09.2026, czyli 69% z 992 wejść z tej kampanii. Pozostałe 306 wejść to sesje zalogowane od wejścia, bez zakupu.

Pokaż w lejku

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Pierwszy dzień z sesjami z kodem kampanii crm_go_upsell. Sesje z tej kampanii są w 326 dniach, a od pierwszego dnia (8.09.2025) do końca danych (30.09.2026) mija 388 dni kalendarzowych, bo newsletter nie wychodzi codziennie. Kampanie płatne mają sesje każdego dnia, więc u nich obie liczby są równe (Meta na L4: 332 dni). Późniejsze tempo to średnia z ostatnich 12 miesięcy (1,26 zakupu dziennie). Źródło: analiza/a5p_lejek.py, sekcja 1; analiza/wyniki/e_merytoryka.txt, punkt 2; notatki/a5_pozyskanie.md, punkt 2.4.

*3. 30.10.2025 · Retencja · zmiana wyniku kohort*

### Marża nowego pacjenta w pierwszych 30 dniach spada w trzech krokach, głównie przez skład pacjentów

**Co się zmieniło:**
Marża nowego pacjenta w pierwszych 30 dniach, przed kosztem pozyskania, spada trzema stopniami. Przybywa pacjentów nowych kampanii na L4, którzy zostawiają mniej marży.

**O ile:**
56,0 zł od 1.10.2024 (17 520 pacjentów) → 53,1 zł od 30.10.2025 (5 549 pacjentów) → 50,1 zł od 26.01.2026 (6 064 pacjentów) → 46,8 zł od 8.04.2026 (9 744 pacjentów).

Pokaż w kohortach

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

*4. 3.11.2025 · Lejek · start kampanii*

### Rusza kampania Meta na L4; jej sesje płacą rzadziej niż sesje z wyszukiwarki

**Co się zmieniło:**
Pierwszy dzień z sesjami i kosztem kampanii Meta na L4. Kampania przyprowadza głównie ruch z przeglądarek wbudowanych w aplikacje Instagrama i Facebooka. Jej sesje płacą rzadziej niż sesje z wyszukiwarki.

**O ile:**
Średnio 183,7 sesji i 10,8 płatności dziennie, konwersja sesji do płatności 5,89%, razem 3 594 zamówienia do 30.09.2026. Od tego samego dnia: starsza kampania Meta 3,61% (20 687 sesji), wyszukiwarka bezpłatna 9,10% (43 291 sesji), Google Ads na hasła ogólne 8,55% (42 624 sesje). Ruch kampanii rośnie skokami: 17.11.2025, 8.12.2025, 2.01.2026, 19.01.2026.

Pokaż w lejku

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Pierwszy dzień z sesjami z kodem kampanii meta_prosp_l4_szybko w analityce; ten sam dzień w wydatkach na kampanie. Źródło: analiza/a5p_zdarzenia.py, sekcja 6; notatki/a5_pozyskanie.md, punkt 2.

*5. 3.11.2025 · Retencja · zmiana struktury pacjentów*

### Coraz więcej nowych pacjentów przychodzi z kampanii na L4, a ci pacjenci prawie nie wracają

**Co się zmieniło:**
Od startu kampanii Meta na L4 coraz większa część nowych pacjentów przychodzi z dwóch nowych kampanii na L4 (Meta i TikTok). Ci pacjenci prawie nie wracają, więc ich udział obniża powrót całej kohorty.

**O ile:**
Udział w nowych pacjentach: 0,0% od 1.10.2024 do 2.11.2025 (17 676 pacjentów), 8,0% od 3.11.2025 do 5.12.2025 (1 972 pacjentów), 17,4% od 6.12.2025 do 2.02.2026 (4 127 pacjentów), 29,4% od 3.02.2026 do 9.04.2026 (5 503 pacjentów), 41,0% od 10.04.2026 do 30.09.2026 (11 640 pacjentów).

Pokaż w kohortach

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

*6. 13.11.2025 · Obsługa pacjenta · zmiana obsługi pacjenta*

### Coraz więcej pierwszych zamówień kończy się zwrotem po odbytej wizycie

**Co się zmieniło:**
Rośnie odsetek pierwszych zamówień, za które pacjent dostaje zwrot po odbytej wizycie. Skupia się w wizytach L4 pacjentów nowych kampanii. Lekarz dostaje wynagrodzenie także za te wizyty.

**O ile:**
2,1% od 1.10.2024 (18 260 pacjentów) → 3,9% od 13.11.2025 (7 142 pacjentów) → 6,9% od 23.02.2026 (15 516 pacjentów).

Pokaż w zakładce „Po zakupie”

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

*7. 24.11.2025 · Obsługa pacjenta · zmiana obsługi pacjenta*

### Poranne wizyty u internisty coraz częściej zaczynają się ponad 15 minut po terminie

**Co się zmieniło:**
Rośnie odsetek wizyt u internisty z terminem 6:00–11:59, które zaczynają się ponad 15 minut po terminie, także u pacjentów spoza nowych kampanii. Przy tym samym porannym ruchu opóźnień jest dużo więcej niż rok wcześniej, a już pierwsza poranna wizyta dnia jest często spóźniona. Przyczyny w danych nie widać (Czego nie wiemy, punkt 4).

**O ile:**
6,3% od 1.10.2024 (6 148 wizyt) → 27,8% od 24.11.2025 (615 wizyt) → 41,9% od 26.12.2025 (730 wizyt) → 50,2% od 2.02.2026 (4 248 wizyt). To średnie poziomy odcinków wyznaczonych przez metodę. Miesiąc po miesiącu od lutego do września 2026 to 47,3–52,7% porannych wizyt, jak w zakładce „Po zakupie”.

Pokaż w zakładce „Po zakupie”

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). Seria: wizyty u internisty rano, pacjenci spoza nowych kampanii. Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

*8. 1.01.2026 · Lejek · zmiana stopniowa*

### Remarketing Meta coraz rzadziej kończy się płatnością, a jednocześnie trafia do innych osób niż wcześniej

**Co się zmieniło:**
Remarketing wraca coraz częściej do osób, które pierwszy raz przyszły z Meta i TikToka, a rzadziej do osób z wyszukiwarki. Te osoby płacą rzadziej. W obrębie źródła pierwszej wizyty konwersja stoi.

**O ile:**
Płatność na sesję u osób, które jeszcze nie kupowały: 28,2% w IV kwartale 2025 (1 011 sesji), 18,9% w II kwartale 2026 (1 603 sesje) i 19,1% w III kwartale 2026 (1 534 sesje). Udział przeglądarek w aplikacjach w tym ruchu rośnie z 13,3% do 22,1–23,4%. Osoby, które pierwszy raz przyszły z Google albo Bing: 27,9% rok wcześniej i 26,7% od 1.01.2026 do 30.09.2026; z Meta (pozyskanie): 11,5% i 13,2%.

Pokaż w lejku

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Metoda wykrywania zmian wskazała 20.03.2026 jako dzień zmiany poziomu płatności na sesję (27,3% → 19,1%), ale zmiana narasta od 1.01.2026. Kod kampanii: meta_rmkt_koszyk. Źródło: analiza/a5p_zdarzenia.py, sekcje 5h i 5i; notatki/a5_pozyskanie.md, punkt 2.5.

*9. 9.02.2026 · Lejek · start kampanii*

### Rusza kampania TikTok na L4; jej sesje płacą rzadziej niż sesje z wyszukiwarki i kampanii Meta na L4

**Co się zmieniło:**
Pierwszy dzień z sesjami i kosztem kampanii TikTok na L4. Kampania przyprowadza głównie ruch z przeglądarek wbudowanych w aplikację TikToka. Jej sesje płacą rzadziej niż sesje z wyszukiwarki i kampanii Meta na L4.

**O ile:**
Średnio 143,0 sesji i 6,8 płatności dziennie, konwersja sesji do płatności 4,76%, razem 1 593 zamówienia do 30.09.2026. Od tego samego dnia: kampania Meta na L4 5,90% (48 952 sesje), wyszukiwarka bezpłatna 8,97% (29 242 sesje). Ruch kampanii rośnie skokami: 23.02.2026, 13.03.2026, 6.04.2026.

Pokaż w lejku

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Pierwszy dzień z sesjami z kodem kampanii tt_prosp_l4_15min w analityce; ten sam dzień w wydatkach na kampanie. Źródło: analiza/a5p_zdarzenia.py, sekcja 6; notatki/a5_pozyskanie.md, punkt 2.

*10. 10.02.2026 · Retencja · zmiana zachowania kohort*

### Powrót nowych pacjentów w 30 dniach spada skokowo, głównie przez skład pacjentów

**Co się zmieniło:**
Powrót w 30 dniach całej kohorty spada skokowo zaraz po starcie kampanii TikTok na L4 (9.02.2026); metoda wskazała dzień później. To głównie skład pacjentów: rośnie udział nowych kampanii, których pacjenci prawie nie wracają.

**O ile:**
9,7% (12 514 pacjentów, 5.06.2025–9.02.2026) → 6,9% (14 536 pacjentów, 10.02.2026–31.08.2026). Wcześniejszy kandydat 5.06.2025: 11,4% → 9,7%; wypada w pierwszym roku, więc może być porą roku.

Pokaż w kohortach

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). Udział składu pokazuje rozkład spadku powrotu (notatki/a5_retencja.md, krok 3). Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

*11. 2.03.2026 · Retencja · kandydat poniżej progu*

### W kampaniach działających w obu latach powrót też spada, ale bez wyraźnego skoku

**Co się zmieniło:**
W kampaniach obecnych w obu latach powrót w 90 dniach też spada, ale metoda nie znalazła zmiany skokowej powyżej progu. Najsilniejszy kandydat to ten dzień.

**O ile:**
23,3% przed (24 511 pacjentów) i 20,9% po (5 751 pacjentów, kohorty z pełnym oknem 90 dni).

Pokaż w kohortach

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Kandydata wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki); różnica jest poniżej progu. Brak skoku nie znaczy, że spadek musi być rozłożony w czasie. Luty 2026 nie pasuje do hipotezy, że większe opóźnienia zawsze obniżają powrót: opóźnienia były wtedy już wysokie, a powrót w tych kampaniach nie spadł. To trop do sprawdzenia. Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5.

*12. 17.03.2026 · Lejek · awaria*

### Od 17 marca 2026 w Safari na iPhone'ach i iPadach dużo rzadziej udaje się założyć nowe konto

**Co się zmieniło:**
U osób, które jeszcze nie kupowały, krok logowania albo zakładania konta po wyborze terminu spada w Safari na iPhone'ach i iPadach i zostaje niski do końca danych. Gwałtownie spada skuteczność zakładania nowego konta (konta dalej powstają, ale rzadziej), a logowanie do istniejącego działa.

**O ile:**
Krok konta po wyborze terminu spadł z 66,1% (od 1.10.2025 do 16.03.2026) do 45,6% (od 17.03 do 30.09.2026, 4 678 sesji z wyborem terminu) i nie wraca. W 60 dniach przed awarią i po niej: 66,2% (1 763 sesje) i 45,1% (1 553 sesje); pozostałe przeglądarki 64,8% i 63,4%. Szacunek: 628–695 utraconych pierwszych zamówień w 198 dniach do 30.09.2026, czyli 95–105 na 30 dni.

Pokaż w lejku

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Metoda wykrywania zmian w seriach dziennych (podział binarny) wskazała ten dzień. Sprawdzenie na bazie: spadek jest w głównych kanałach (TikTok ma za małą próbę do oceny), więc to nie zmiana struktury ruchu. Przyczyny w danych nie widać. Źródło: analiza/a5p_zdarzenia.py, sekcja 5; notatki/a5_pozyskanie.md, punkt 2.1.

*13. 22.05.2026 · Lejek · zmiana poziomu*

### W kampanii Google Ads na markę mniej sesji kończy się płatnością, a przyczyny w danych nie widać

**Co się zmieniło:**
Sesja do płatności u osób, które jeszcze nie kupowały, spada w kampanii Google Ads na markę. Przyczyny w danych nie widać (Czego nie wiemy, punkt 21).

**O ile:**
Z 21,2% (21 186 sesji, 1.10.2024–21.05.2026) do 17,8% (5 152 sesje, 22.05–30.09.2026), czyli o około 28,5–39,6 zamówienia na 30 dni zależnie od okna porównania. Bez Safari na iOS spadek jest prawie taki sam (−2,2 punktu procentowego wobec 17.03–21.05.2026), zmiana struktury ruchu (urządzenie, przeglądarka, strona wejścia) daje około zera, a inne kanały w tych dniach się nie zmieniają. Rok wcześniej w tym samym sezonie spadek był mniejszy (−1,3 punktu) i nieistotny, więc część może być sezonowa. W tym samym czasie rośnie koszt kliknięcia tej kampanii (z 1,01 zł rok wcześniej do 1,19 zł w ostatnich 12 miesiącach).

Pokaż w lejku

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Metoda wykrywania zmian w seriach dziennych wskazała ten dzień; sprawdzenie w oknach przed i po, bez Safari na iOS, ze strukturą ruchu i z tym samym sezonem rok wcześniej. Kod kampanii: gs_brand. Źródło: analiza/d_kampanie.py → analiza/wyniki/d_kampanie.txt, punkt 5.

*14. 10.06.2026–24.06.2026 · Jakość danych · błąd danych*

### W czerwcu 2026 eksport zapisał część zamówień dwa razy; zostawiamy jedną kopię

**Co się zmieniło:**
W eksporcie dwa razy zapisano 604 zamówienia, wszystkie od 10.06.2026 do 24.06.2026. W tych dniach zdublowanych jest od 28% do 42% zamówień dziennie. Dzień przed oknem i dzień po nim: 0 zamówień zdublowanych.

**O ile:**
Wszystkie kopie są w ostatnich 12 miesiącach i dodają do nich 604 zamówienia i 51 293 zł zapłat, czyli 45 805 zł po odjęciu zwrotów. W analityce każde z tych zamówień ma jeden krok płatności, więc to wygląda na błąd eksportu: pacjent zapłacił raz. Zostawiamy jedną kopię.

Zobacz w jakości danych

**Skąd wiemy** *(sekcja rozwijana, tu rozwinięta)*

Dwie identyczne kopie zamówienia w sąsiednich liniach pliku zamówień. Źródło: analiza/a2_jakosc.py; czyszczenie: analiza/a2_czyste.py.

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
| 22.05.2026 | Źródło (kanał) | Google Ads: hasło marki | Sesja do płatności | 21,2% | 17,8% | −3,4 pkt proc.<br>(gorzej) | 598 / 132 | −39,6 | w lejku |
| 22.05.2026 | Kampania | Google Ads: marka | Sesja do płatności | 21,2% | 17,8% | −3,4 pkt proc.<br>(gorzej) | 598 / 132 | −39,6 | w lejku |
| 2.07.2026 | Strona wejścia | /blog/e-recepta-jak-zrealizowac | Sesje dziennie | 6,7 | 4,3 | −2,4 | 255 / 91 | — | w lejku |

Etykiety zmiany po zmianie wobec okresu przed nią: lepiej gorzej bez oceny Strzałka pokazuje kierunek, kolor ocenę; słowo także po najechaniu na etykietę.

Dalej: Wynik biznesu

# Zakładka 6: Wynik biznesu (`#wynik`)

## Wynik biznesu: przychód, marża i ekonomia kampanii

### Za cały rok marża rośnie, ale wydatki na kampanie rosną szybciej niż marża zarabiana przed ich kosztem

W ostatnich 12 miesiącach marża przed kosztem kampanii wzrosła o 41%, a wydatki na kampanie o 77%.

Po koszcie lekarza, kampaniach i prowizji marża i tak wzrosła o 27%.

Rok do roku marża przed kosztem kampanii rośnie z każdym kwartałem wolniej, a wydatki szybciej. W III kwartale 2026 wydatki na kampanie były ponad dwa razy wyższe niż rok wcześniej.

Powtórne zamówienie zostawia mniej marży niż rok wcześniej, bo rośnie udział wizyt ze zniżką TelemediGO: z 34% do 42% powtórnych zamówień. To spina się z bilansem programu: opłata za TelemediGO nie pokrywa zniżek, które dostają jego członkowie (zakładka „Czy to wzrost”).

**Zastrzeżenie.** Spadek marży w III kwartale 2026, o 7% rok do roku, zależy od jednorazowego zdarzenia: we wrześniu 2025 ruszyła sprzedaż TelemediGO w newsletterze. Po odjęciu jednorazowej nadwyżki tego startu marża kwartału jest o 1% wyższa niż rok wcześniej.

*Filtry (ustawienia domyślne):*
- Grupowanie: miesiące (do wyboru: miesiące / tygodnie / dni)

#### Marża przed kosztem kampanii i wydatki na kampanie

*Obie linie w złotych, na jednej osi. Marża przed kosztem kampanii to przychód z konsultacji po zwrotach i z TelemediGO minus koszt lekarza.*

*[Wykres] serie: brak*

Najedź na wykres, żeby zobaczyć wartości.

Marża przed kosztem kampanii

Wydatki na kampanie

1. 17.05.2025: Godzina bez danych
2. 8.09.2025: Start sprzedaży TelemediGO w newsletterze
3. 30.10.2025: Marża na pacjenta w 30 dniach spada
4. 3.11.2025: Start kampanii Meta na L4
5. 3.11.2025: Rośnie udział nowych kampanii w nowych pacjentach
6. 13.11.2025: Więcej zwrotów po wizycie
7. 24.11.2025: Poranne opóźnienia u internisty
8. 1.01.2026: Remarketing Meta słabnie
9. 9.02.2026: Start kampanii TikTok na L4
10. 10.02.2026: Spada powrót w 30 dniach
11. 2.03.2026: Powrót w kampaniach działających w obu latach
12. 17.03.2026: Awaria zakładania konta w Safari na iOS
13. 22.05.2026: Spada konwersja Google Ads na markę
14. 10.06.2026: Duplikaty zamówień w eksporcie

#### Marża po koszcie lekarza, kampaniach i prowizji

*[Wykres] serie: brak*

Najedź na wykres, żeby zobaczyć wartości.

Marża po koszcie lekarza, kampaniach i prowizji

1. 17.05.2025: Godzina bez danych
2. 8.09.2025: Start sprzedaży TelemediGO w newsletterze
3. 30.10.2025: Marża na pacjenta w 30 dniach spada
4. 3.11.2025: Start kampanii Meta na L4
5. 3.11.2025: Rośnie udział nowych kampanii w nowych pacjentach
6. 13.11.2025: Więcej zwrotów po wizycie
7. 24.11.2025: Poranne opóźnienia u internisty
8. 1.01.2026: Remarketing Meta słabnie
9. 9.02.2026: Start kampanii TikTok na L4
10. 10.02.2026: Spada powrót w 30 dniach
11. 2.03.2026: Powrót w kampaniach działających w obu latach
12. 17.03.2026: Awaria zakładania konta w Safari na iOS
13. 22.05.2026: Spada konwersja Google Ads na markę
14. 10.06.2026: Duplikaty zamówień w eksporcie

#### Kwartały rok do roku

*[Wykres] Zmiana rok do roku w każdym kwartale: marża przed kosztem kampanii i wydatki na kampanie*

- IV kw. 2025: marża przed kosztem kampanii +55,2%, wydatki na kampanie +29,6%
- I kw. 2026: marża przed kosztem kampanii +49,7%, wydatki na kampanie +66,4%
- II kw. 2026: marża przed kosztem kampanii +38,4%, wydatki na kampanie +104,0%
- III kw. 2026: marża przed kosztem kampanii +25,2%, wydatki na kampanie +107,7%

*Zmiana wobec tego samego kwartału rok wcześniej. Marża przed kosztem kampanii to przychód z konsultacji po zwrotach i z TelemediGO minus koszt lekarza; wydatki na kampanie bez prowizji afiliacyjnej.*

| Kwartał wobec tego samego kwartału rok wcześniej | Marża | Wydatki na kampanie | Przychód: konsultacje po zwrotach i TelemediGO | Koszt lekarza | Nowi pacjenci |
| --- | --- | --- | --- | --- | --- |
| IV kw. 2025 wobec IV kw. 2024 | 259 375 zł<br>rok wcześniej: 151 340 zł<br>+71,4%<br>lepiej | 113 089 zł<br>rok wcześniej: 87 253 zł<br>+29,6%<br>uwaga | 756 915 zł<br>rok wcześniej: 479 343 zł<br>+57,9%<br>lepiej | 380 925 zł<br>rok wcześniej: 237 125 zł<br>+60,6% | 4 964<br>rok wcześniej: 4 186<br>+18,6%<br>lepiej |
| I kw. 2026 wobec I kw. 2025 | 324 423 zł<br>rok wcześniej: 226 877 zł<br>+43,0%<br>lepiej | 170 625 zł<br>rok wcześniej: 102 565 zł<br>+66,4%<br>uwaga | 998 098 zł<br>rok wcześniej: 657 568 zł<br>+51,8%<br>lepiej | 497 875 zł<br>rok wcześniej: 323 375 zł<br>+54,0% | 7 408<br>rok wcześniej: 4 789<br>+54,7%<br>lepiej |
| II kw. 2026 wobec II kw. 2025 | 256 558 zł<br>rok wcześniej: 227 044 zł<br>+13,0%<br>lepiej | 184 405 zł<br>rok wcześniej: 90 383 zł<br>+104,0%<br>uwaga | 896 013 zł<br>rok wcześniej: 635 002 zł<br>+41,1%<br>lepiej | 451 550 zł<br>rok wcześniej: 313 825 zł<br>+43,9% | 6 429<br>rok wcześniej: 3 819<br>+68,3%<br>lepiej |
| III kw. 2026 wobec III kw. 2025 | 207 713 zł<br>rok wcześniej: 222 824 zł<br>−6,8%<br>gorzej | 181 555 zł<br>rok wcześniej: 87 431 zł<br>+107,7%<br>uwaga | 796 968 zł<br>rok wcześniej: 614 905 zł<br>+29,6%<br>lepiej | 404 475 zł<br>rok wcześniej: 301 375 zł<br>+34,2% | 5 886<br>rok wcześniej: 3 437<br>+71,3%<br>lepiej |

#### Miesiące i sumy obu lat

| Okres | Zamówienia | Nowi pacjenci | Przychód: pierwsze zamówienia (zł) | Przychód: kolejne zamówienia (zł) | TelemediGO (zł) | Koszt lekarza (zł) | Kampanie (zł) | Prowizja afiliacyjna (zł) | Marża (zł) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rok wcześniej (X 2024 – IX 2025) | 24 716 | 16 231 | 1 490 983 | 739 284 | 156 551 | 1 175 700 | 367 632 | 15 400 | 828 085 |
| Ostatnie 12 miesięcy (X 2025 – IX 2026) | 38 491 | 24 687 | 2 075 848 | 1 152 495 | 219 652 | 1 734 825 | 649 675 | 15 425 | 1 048 069 |
| Zmiana rok do roku | +55,7% | +52,1% | +39,2% | +55,9% | +40,3% | +47,6% | +76,7% | +0,2% | +26,6% |
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

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

*Kwartały rok do roku*

| Kwartał | Marża przed kosztem kampanii | Wydatki na kampanie | Marża po kosztach kampanii |
| --- | --- | --- | --- |
| IV kw. 2025 | +55,2%<br>lepiej | +29,6%<br>uwaga | +71,4%<br>lepiej |
| I kw. 2026 | +49,7%<br>lepiej | +66,4%<br>uwaga | +43,0%<br>lepiej |
| II kw. 2026 | +38,4%<br>lepiej | +104,0%<br>uwaga | +13,0%<br>lepiej |
| III kw. 2026 | +25,2%<br>lepiej | +107,7%<br>uwaga | −6,8%<br>gorzej |

Za cały rok: marża przed kosztem kampanii 1 211 tys. zł → 1 713 tys. zł (+41,5%), wydatki na kampanie 368 tys. zł → 650 tys. zł (+76,7%), marża po koszcie lekarza, kampaniach i prowizji 828 tys. zł → 1 048 tys. zł (+26,6%). Marża przed kosztem kampanii to przychód z konsultacji po zwrotach i z TelemediGO minus koszt lekarza.

#### III kwartał 2026 bez jednorazowego startu sprzedaży TelemediGO

Sprzedaż TelemediGO w newsletterze ruszyła 8.09.2025. W pierwszych 23 dniach sprzedała 225 członkostw, a przy późniejszym tempie (1,26 dziennie) sprzedałaby około 29. Jednorazowa nadwyżka to 196 zakupów, czyli 17,4 tys. zł. Bez niej marża III kwartału 2026 jest o 1,1% wyższa niż rok wcześniej, a bez całej sprzedaży w newsletterze w obu latach o 2,3% niższa. Marża przed kosztem kampanii rośnie wtedy o 32,6% (bez tej korekty o 25,2%).

Cały spadek III kwartału 2026 przypada na wrzesień (−20,8 tys. zł); lipiec +6,6 tys. zł, sierpień −0,9 tys. zł.

#### Marża na powtórne zamówienie w III kwartale 2026

Pacjenci spoza nowych kampanii złożyli więcej powtórnych zamówień (3 140 wobec 2 879), ale każde zostawia mniej marży (32,81 zł wobec 35,86 zł). Spadek o 3,05 zł to w 89% zmiana udziału rodzajów zniżki, a w obrębie tego samego rodzaju zniżki marża prawie stoi (−0,35 zł). Udział wizyt ze zniżką TelemediGO rośnie z 34,3% do 41,6%. Wizyta ze zniżką zostawia 11,01 zł marży, bez zniżki 48,78 zł, a u specjalistów wizyta ze zniżką TelemediGO ma marżę ujemną (−5,59 zł).

#### Rozkład księgowy spadku III kwartału 2026

Rozkład księgowy dzieli różnicę marży między kwartałami na składniki. Pokazuje, gdzie w rachunku jest różnica; jej przyczyny nie wskazuje.

Marża spadła o 15,1 tys. zł. Według pierwszego wejścia pacjenci nowych kampanii zostawili 89,0 tys. zł marży przed kosztem kampanii przy 87,9 tys. zł wydatków, czyli wyszli prawie na zero (+1,1 tys. zł). Pozostała część biznesu straciła 16,2 tys. zł:

- opłaty TelemediGO −11,2 tys. zł, w tym −10,5 tys. zł sprzedaży osobnej w newsletterze (225 zakupów we wrześniu 2025 wobec 107 w całym III kwartale 2026);
- wyższe wydatki kampanii działających w obu latach −6,2 tys. zł;
- marża konsultacji +1,2 tys. zł: powtórnych zamówień jest więcej, ale każde zostawia mniej marży;
- prowizja bez zmian.

Po odjęciu TelemediGO zostaje 5,0 tys. zł spadku. W rachunku przypada on na wyższe wydatki kampanii działających w obu latach, częściowo zrównoważone wyższą marżą konsultacji. Rozkład nie oddziela skutków awarii w Safari od innych zmian przychodu. Według sesji z płatnością podział się odwraca: nowe kampanie −25,2 tys. zł, reszta +10,1 tys. zł; suma jest ta sama.

#### Awaria Safari w III kwartale 2026

Awaria zakładania konta w Safari na iOS kosztowała w samym III kwartale 2026 szacunkowo 14,6–18,3 tys. zł marży (258–323 utracone pierwsze zamówienia z ich powrotami w tym samym kwartale, zależnie od odjęcia tła i założonego tempa strat). Osobny scenariusz powrotów pacjentów utraconych od 17.03 do 30.06 daje jeszcze 4,1–4,5 tys. zł. Wyniku kwartału bez awarii nie mierzymy: to rachunek przy założeniach pozycji 1 listy priorytetów.

#### Baza powracających pacjentów

Pierwsze kwartały roku wcześniej nie miały jeszcze pełnej bazy powracających pacjentów. Marża z pacjentów pozyskanych w poprzednich kwartałach to 0% marży IV kwartału 2024, 23,4% I kwartału 2025 i 51,7% III kwartału 2025. Bez tej bazy marża rośnie rok do roku o 8,5% zamiast 71,4% w IV kwartale 2025 i o 26,1% zamiast 43,0% w I kwartale 2026. Miarodajne jest więc porównanie III kwartałów (baza to 51,7% i 51,1% marży).

Bez jednorazowej nadwyżki startu sprzedaży TelemediGO (jej części przypadającej na bazę: 210 z 225 zakupów) baza dała w III kwartale 2026 więcej marży niż rok wcześniej: 106,2 tys. zł wobec 99,0 tys. zł (+7,3%; bez całej sprzedaży w newsletterze w obu latach +1,0%). Wszystkich pacjentów pozyskanych w poprzednich kwartałach jest prawie trzy razy więcej (35 032 wobec 12 794), ale tych, którzy w kwartale coś kupili, tylko o 15% więcej (1 735 wobec 1 503). Dane nie rozdzielają, ile to wiek bazy, a ile to, że nowsze roczniki wracają rzadziej.

#### Przychód i koszty za cały rok

Przychód z konsultacji po zwrotach rośnie o 44,8% (2 230 266 zł → 3 228 342 zł), TelemediGO rośnie o 40,3% (156 551 zł → 219 652 zł). Koszt lekarza rośnie o 47,6% (1 175 700 zł → 1 734 825 zł), wydatki na kampanie rosną o 76,7% (367 632 zł → 649 675 zł), prowizja afiliacyjna rośnie o 0,2% (15 400 zł → 15 425 zł).

Koszt lekarza liczymy także za wizyty zwrócone po wizycie (zasada z zadania), a koszt i zwrot przypisujemy do dnia płatności. Prowizję afiliacyjną liczymy według pierwszego wejścia, w dniu pierwszego zamówienia.

Skąd liczby: analiza/wyniki/e_merytoryka.txt (punkty 2 i 3); analiza/wyniki/d_wynik.txt (punkty 1 i 2); analiza/wyniki/c_priorytety.txt (W4, P1); eksport analiza/b_eksport.py.

### Kampania TikTok na L4 nie zwraca kosztu pozyskania pacjenta

Po odjęciu kosztu pozyskania TikTok na L4 traci w 90 dniach około 5 zł na pacjencie według pierwszego wejścia i około 18 zł według sesji z płatnością.

Obie nowe kampanie na L4 razem wychodzą blisko zera: około +4 zł na pacjenta w 90 dniach według pierwszego wejścia i około −9 zł według sesji z płatnością. Znak zależy od reguły. Test z wyłączeniem reklamy Meta na L4 w części kraju zmierzy przyrost pacjentów niezależnie od reguły (pozycja 9 listy priorytetów).

Pozostałe kampanie płatne, afiliacja i kanały bezpłatne mają wynik dodatni w obu regułach (tabela niżej).

**Zastrzeżenie.** Wynik Google Ads na markę i remarketingu Meta jest liczony ostrożnie: rachunek kosztu pozyskania liczy tylko nowych pacjentów, a 37% i 24% zamówień w sesjach tych kampanii to zamówienia powtórne, których marży tym kampaniom nie przypisujemy.

*Filtry (ustawienia domyślne):*
- Poziom: Grupy kampanii (do wyboru: Grupy kampanii / Kampanie / Kanały)
- Okres: Ostatnie 12 miesięcy (X 2025 – IX 2026) (do wyboru: Ostatnie 12 miesięcy (X 2025 – IX 2026) / Rok wcześniej (X 2024 – IX 2025))

*[Wykres] Wynik na pacjenta po koszcie pozyskania w 90 dniach według dwóch reguł przypisania źródła*

- Nowe kampanie na L4 (Meta i TikTok): według pierwszego wejścia +3,6 zł, według sesji z płatnością −9,4 zł
- Pozostałe kampanie płatne: według pierwszego wejścia +20,0 zł, według sesji z płatnością +18,7 zł
- Afiliacja (ranking lekarzy): według pierwszego wejścia +32,2 zł, według sesji z płatnością +30,8 zł
- Kanały bezpłatne: według pierwszego wejścia +68,6 zł, według sesji z płatnością +64,5 zł

*Wynik na pacjenta w 90 dniach: marża na pacjenta minus koszt pozyskania. Pionowa linia to zero: na lewo od niej kampania traci na każdym pacjencie.*

**Tabela: koszt pozyskania i wynik na pacjenta (90 i 180 dni)** *(sekcja rozwijana, tu rozwinięta)*

*Wynik na pacjenta to marża na pacjenta w 90 albo 180 dniach minus koszt pozyskania. Pod kosztem: liczba pacjentów; pod wynikiem: marża minus koszt. Przedział warunkowy pokazuje się po najechaniu na wynik.*

| Grupa | Według pierwszego wejścia — Koszt pozyskania, 90 dni | Według pierwszego wejścia — Wynik na pacjenta, 90 dni | Według pierwszego wejścia — Koszt pozyskania, 180 dni | Według pierwszego wejścia — Wynik na pacjenta, 180 dni | Według sesji z płatnością — Koszt pozyskania, 90 dni | Według sesji z płatnością — Wynik na pacjenta, 90 dni | Według sesji z płatnością — Koszt pozyskania, 180 dni | Według sesji z płatnością — Wynik na pacjenta, 180 dni | Ocena |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nowe kampanie na L4 (Meta i TikTok) | 32,7 zł<br>4 893 pac. | +3,6 zł<br>marża 36,3 zł − koszt 32,7 zł | 30,3 zł<br>2 352 pac. | +7,0 zł<br>marża 37,3 zł − koszt 30,3 zł | 45,6 zł<br>3 510 pac. | −9,4 zł<br>marża 36,1 zł − koszt 45,6 zł | 42,1 zł<br>1 693 pac. | −5,2 zł<br>marża 36,9 zł − koszt 42,1 zł | Niepewny: znak zależy od przypisania źródła |
| Pozostałe kampanie płatne | 44,2 zł<br>7 076 pac. | +20,0 zł<br>marża 64,2 zł − koszt 44,2 zł | 42,6 zł<br>5 130 pac. | +29,7 zł<br>marża 72,3 zł − koszt 42,6 zł | 43,8 zł<br>7 141 pac. | +18,7 zł<br>marża 62,4 zł − koszt 43,8 zł | 43,5 zł<br>5 029 pac. | +27,5 zł<br>marża 71,0 zł − koszt 43,5 zł |  |
| Afiliacja (ranking lekarzy) | 25,0 zł<br>489 pac. | +32,2 zł<br>marża 57,2 zł − koszt 25,0 zł | 25,0 zł<br>352 pac. | +37,0 zł<br>marża 62,0 zł − koszt 25,0 zł | 25,0 zł<br>319 pac. | +30,8 zł<br>marża 55,8 zł − koszt 25,0 zł | 25,0 zł<br>229 pac. | +35,6 zł<br>marża 60,6 zł − koszt 25,0 zł |  |
| Kanały bezpłatne | 0,0 zł<br>6 466 pac. | +68,6 zł<br>marża 68,6 zł − koszt 0,0 zł | 0,0 zł<br>4 757 pac. | +78,1 zł<br>marża 78,1 zł − koszt 0,0 zł | 0,0 zł<br>7 954 pac. | +64,5 zł<br>marża 64,5 zł − koszt 0,0 zł | 0,0 zł<br>5 640 pac. | +74,2 zł<br>marża 74,2 zł − koszt 0,0 zł |  |

**Jak liczymy** *(sekcja rozwijana, tu rozwinięta)*

Koszt pozyskania to wydatki na kampanię albo prowizja afiliacyjna na nowego pacjenta. Liczymy go osobno dla każdego okna: z kohort z pełnym oknem i z wydatków z tych samych dni, więc po 180 dniach to inne kohorty i inny koszt niż po 90 dniach.

Oba sposoby przypisania źródła stoją obok siebie: według pierwszego wejścia i według sesji z płatnością.

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

W 90 dniach: TikTok na L4 −4,6 zł i −17,8 zł na pacjenta, obie nowe kampanie razem +3,6 zł i −9,4 zł. Po 180 dniach nowe kampanie na L4 dają +7,0 zł na pacjenta według pierwszego wejścia i −5,2 zł według sesji z płatnością.

Według pierwszego wejścia pacjent należy do kanału, z którego pierwszy raz wszedł na stronę, a kod kampanii na pierwszym zamówieniu rozstrzyga; według sesji z płatnością należy do kanału sesji, w której zapłacił. W nowych kampaniach różnica między tymi podziałami to jedna grupa: według sesji z płatnością do innych kanałów trafia 2 081 pacjentów nowych kampanii na L4 z ostatnich 12 miesięcy. 1 918 z nich weszło pierwszy raz z reklamy nowej kampanii, a zapłaciło w innej sesji, a 163 weszło z innego kanału, ale zapłaciło z kodem nowej kampanii. W ekonomii kampanii pokazujemy oba podziały, bo od nich zależy, której kampanii przypisujemy koszt pozyskania.

Zamówienia powtórne w sesjach kampanii w ostatnich 12 miesiącach: Google Ads na markę 37,1% z 4 825 zamówień, remarketing Meta 24,1% z 1 642 zamówień. Rok wcześniej 32,0% i 22,8%.

Obok wyniku po 90 dniach pokazujemy wynik po 180 dniach: pacjenci kampanii na L4 prawie nie wracają, a pozostali tak, więc 90 dni zaniża wartość pozostałych kampanii. Przedział przy wyniku jest warunkowy: liczony tylko z rozrzutu marży, bez niepewności przypisania źródła.

Nazwy kampanii w danych: Meta na L4 to meta_prosp_l4_szybko, TikTok na L4 to tt_prosp_l4_15min, Google Ads na markę to gs_brand, remarketing Meta to meta_rmkt_koszyk.

Skąd liczby: analiza/a5e_ekonomia.py → analiza/wyniki/a5e_kampanie.csv i a5e_ekonomia.txt; analiza/wyniki/e_merytoryka.txt (punkty 1 i 5a).

**Jak liczymy w tej zakładce** *(sekcja rozwijana, tu rozwinięta)*

Płatności w lejku (24 717 rok wcześniej, X 2024 – IX 2025, i 38 490 w ostatnich 12 miesiącach, X 2025 – IX 2026) i zamówienia (24 716 i 38 491) różnią się o 1 na granicy okresów, bo sesję liczymy do dnia jej rozpoczęcia, a zamówienie do dnia płatności. Przychód z konsultacji po zwrotach rok wcześniej to 2 230 266,50 zł, więc zależnie od zaokrąglenia 2 230 266 albo 2 230 267 zł.

Źródło danych: analiza/definicje.py (koszt lekarza, marża), analiza/a5e_ekonomia.py (ekonomia kampanii), eksport analiza/b_eksport.py.

Dalej: Jakość danych

# Zakładka 7: Jakość danych (`#jakosc`)

## Jakość danych

### Dane wymagały dwóch poprawek; pozostałe niespójności są drobne

Usunęliśmy zamówienia zapisane w eksporcie dwa razy (604) i zamówienia kont testowych (2 071).

Danych nikt wcześniej nie czyścił. Poza tymi dwiema rzeczami jedna godzina bez danych i kilka drobnych niespójności dotyczą małej części danych.

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Skąd liczby: analiza/a2_jakosc.py, analiza/a2_czyste.py, analiza/a3_dashboard.py; liczby liczy analiza/b_eksport.py.

### Dashboard zawyża wzrost zamówień i przychodu, a liczbę pacjentów pokazuje prawie dobrze

Po oczyszczeniu zamówienia rosną o 56%, a nie o 61%, jak na dashboardzie.

*[Wykres] Wzrost zamówień i przychodu z konsultacji rok do roku po każdym kroku od dashboardu do danych oczyszczonych*

**Zamówienia**
- Zamówienia, Dashboard (dane surowe): +60,7%
- Zamówienia, Bez duplikatów zamówień: +58,3%
- Zamówienia, Bez duplikatów i bez kont testowych: +55,7%
- Zamówienia, Do tego przychód po odjęciu zwrotów: +55,7% (bez zmian)

**Przychód z konsultacji**
- Przychód z konsultacji, Dashboard (dane surowe): +50,3%
- Przychód z konsultacji, Bez duplikatów zamówień: +48,1%
- Przychód z konsultacji, Bez duplikatów i bez kont testowych: +47,7%
- Przychód z konsultacji, Do tego przychód po odjęciu zwrotów: +44,8%

*Wzrost: ostatnie 12 miesięcy (X 2025 – IX 2026) wobec roku wcześniej (X 2024 – IX 2025). Każdy słupek to poziom po danym kroku, liczony od zera, a nie różnica między krokami.*

Przychód z konsultacji po odjęciu zwrotów rośnie o 45%, a nie o 50%. Nowych pacjentów jest więcej o 52%, prawie tak samo jak na dashboardzie, a sprzedaż TelemediGO rośnie o 40%, bez zmian.

**Tabela z liczbami** *(sekcja rozwijana, tu rozwinięta)*

*Zmiana: ostatnie 12 miesięcy (X 2025 – IX 2026) wobec roku wcześniej (X 2024 – IX 2025). Pod zmianą: wartość rok wcześniej → wartość w ostatnich 12 miesiącach.*

| Krok | Nowi pacjenci | Zamówienia | Przychód z konsultacji | TelemediGO |
| --- | --- | --- | --- | --- |
| Dashboard (dane surowe) | +51,9%<br>16 251 → 24 689 | +60,7%<br>25 269 → 40 613 | +50,3%<br>2,382 → 3,580 mln zł | +40,3%<br>1 759 → 2 468 |
| Bez duplikatów zamówień | bez zmian | +58,3%<br>25 269 → 40 009 | +48,1%<br>2,382 → 3,529 mln zł | bez zmian |
| Bez duplikatów i bez kont testowych | +52,1%<br>16 231 → 24 687 | +55,7%<br>24 716 → 38 491 | +47,7%<br>2,375 → 3,508 mln zł | bez zmian |
| Do tego przychód po odjęciu zwrotów | bez zmian | bez zmian | +44,8%<br>2,230 → 3,228 mln zł | bez zmian |

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Każdy wiersz tabeli zmienia jedną rzecz: najpierw usuwa kopie zamówień, potem konta testowe, a na końcu odejmuje zwroty od przychodu.

Zamówienia: 25 269 → 40 613 na dashboardzie i 24 716 → 38 491 po oczyszczeniu. Przychód z konsultacji: 2,382 → 3,580 mln zł na dashboardzie i 2,230 → 3,228 mln zł po oczyszczeniu i odjęciu zwrotów.

Skąd liczby: analiza/a3_dashboard.py → analiza/wyniki/a3_dashboard.txt i a3_siatka.csv; eksport analiza/b_eksport.py.

### W czerwcu 2026 eksport zapisał część zamówień dwa razy; zostawiamy jedną kopię

Od 10.06.2026 do 24.06.2026 eksport zapisał dwa razy 604 zamówienia.

W tych dniach to od 28% do 42% zamówień dziennie, a dzień przed i dzień po nie ma ani jednej kopii.

Wszystkie kopie są w ostatnich 12 miesiącach i dodają do nich 51 293 zł zapłat (45 805 zł po odjęciu zwrotów). W analityce każde z tych zamówień ma jeden krok płatności, więc to wygląda na błąd eksportu: pacjent zapłacił raz.

*[Wykres] serie: brak*

Najedź na wykres, żeby zobaczyć wartości.

Zamówienia bez kopii

Kopie (duplikaty)

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Kopia to druga, identyczna linia tego samego zamówienia, tuż pod pierwszą w pliku zamówień. Wykres pokazuje dzień po dniu zamówienia bez kopii i kopie.

Skąd liczby: analiza/a2_jakosc.py; czyszczenie: analiza/a2_czyste.py.

### Zamówienia testowe zawyżały wzrost zamówień, bo jest ich prawie trzy razy więcej niż rok wcześniej

Zamówienia testowe to 2 071 zamówień z 22 kont; wyłączamy je ze wszystkich liczb.

Kod TEST-QA ma 1 781 zamówień. Pozostałe 290 zamówień nie ma kodu, ale każde jest zapłacone w pełni i w całości zwrócone, czyli wygląda na test procesu zwrotu. Filtr po samym kodzie by ich nie złapał.

Drugi, niezależny podpis: wszystkie trwają dokładnie 1 minutę (2 071 z 2 071), a taki czas nie występuje u żadnego innego pacjenta (0 zamówień; najkrótsza prawdziwa wizyta trwa 3 minuty).

Testów przybywa: 553 zamówienia rok wcześniej i 1 518 zamówień w ostatnich 12 miesiącach. Zawyżały więc wzrost zamówień. Wyłączamy te konta ze wszystkiego: zamówień, pacjentów, przychodu, sesji i lejka.

**Zastrzeżenie.** Nie wiemy, czy lekarze dostawali wynagrodzenie za te wizyty. Gdyby tak, kosztowałoby to około 52 tys. zł w dwóch latach, w tym około 38 tys. zł w ostatnich 12 miesiącach (Czego nie wiemy, punkt 13).

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

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Zamówienia testowe to 27 591 zł zapłat i 25 810 zł zwrotów.

Koszt liczymy po stawce internisty z zadania (25 zł), bo wszystkie wizyty testowe są u internisty (2 071 z 2 071): 51 775 zł w dwóch latach i 37 950 zł w ostatnich 12 miesiącach.

Skąd liczby: analiza/a2_jakosc.py → analiza/wyniki/a2_jakosc.txt (2e); analiza/wyniki/c_priorytety.txt (P1b, P13).

### Jednej godziny prawie nie ma w danych, ale wyników to nie zmienia

17.05.2025 od 13:00 do 14:00 jest 1 sesja zamiast typowych 21.

Zamówień w tej godzinie jest zwykle około 2, więc to, że nie ma żadnego, niewiele mówi. To jedyna taka godzina w dwóch latach, a jej wpływ na wyniki jest pomijalny.

**Zastrzeżenie.** Nie wiemy, czy to przerwa w działaniu strony, czy w zbieraniu danych.

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Typowa liczba to mediana tej samej godziny w 15 dniach wokół: 21 sesji i 2 zamówienia. Szukamy godzin, w których sesji jest dużo mniej niż ta mediana; w dwóch latach jest tylko ta jedna.

Skąd liczby: analiza/a2_jakosc.py, sekcja o lukach; analiza/wyniki/e_merytoryka.txt (punkt 5e).

### Drobne niespójności dotyczą małej części danych

Każda z nich dotyczy najwyżej kilkudziesięciu zamówień albo kilkuset sesji.

- „Psycholog + e-recepta”: 24 zamówienia. Psycholog nie jest lekarzem i nie wystawia recept, więc to wartość nierealna.
- Mimo aktywnego TelemediGO bez zniżki zapłacono 1 zamówienie.
- Program poleceń: na stronę /polecenie wchodzi z innym źródłem (bezpośrednio, z Google albo z Meta) 330 sesji, a źródło „polecenie” z inną stroną wejścia ma 51 sesji. Ma to znaczenie przy przypisywaniu źródła pacjenta.

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Skąd liczby: analiza/a2_jakosc.py → analiza/wyniki/a2_jakosc.txt.

### Pozostałe sprawdzenia wyszły czysto

Czas płatności, kolejność kroków lejka, koszty kampanii, tożsamość pacjentów i pozostałe tabele są spójne.

- Czas płatności: 65 278 z 65 278 zamówień i 4 227 z 4 227 zakupów TelemediGO ma krok płatności w analityce co do sekundy po przeliczeniu z UTC na czas polski. Zmiana czasu jest obsłużona poprawnie.
- Sesje na kliknięcie są stałe w każdym kwartale: Google Ads od 0,92 do 0,93, Meta od 0,79 do 0,82, TikTok 0,72. Nie ma dni z kosztem bez sesji ani sesji z kampanii płatnej bez kosztu.
- Duplikaty w pozostałych tabelach: sesje 0, kroki lejka 0, konta 0, TelemediGO 0, wydatki na kampanie 0.
- Kroki lejka idą zawsze po kolei: 0 sesji ma krok bez poprzedniego. Jedyne wyjątki zgodne z opisem danych to 686 zakupów samego TelemediGO (tylko kroki płatności) i 22 sesje kont testowych z samym założeniem konta.
- Tożsamość: żadna przeglądarka nie jest dzielona przez dwa konta. Więcej niż jednej przeglądarki używa 7,3% kont (3 835 z 52 422), najwięcej 8 przeglądarek.
- Wartości realne: wizyty po oczyszczeniu trwają od 3 do 36 minut; ceny katalogowe i zniżki TelemediGO zgadzają się z zasadami co do złotówki (raport A2).

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

Skąd liczby: analiza/a2_jakosc.py, analiza/a2_czyste.py; liczby liczy analiza/b_eksport.py.

**Skąd liczby w tej zakładce** *(sekcja rozwijana, tu rozwinięta)*

Źródło: analiza/a2_jakosc.py, analiza/a2_czyste.py, analiza/a3_dashboard.py; liczby na tej stronie liczy analiza/b_eksport.py.

Dalej: Priorytety

# Zakładka 8: Priorytety (`#priorytety`)

## Priorytety: co robimy po kolei

Lista od najważniejszej pozycji. Przy każdej: dlaczego, co robimy, ile jest warta w złotych marży na rok, po czym poznamy, że zadziałała, i ile zajmie wdrożenie. Pełne rachunki i założenia są w szczegółach każdej karty.

### Przegląd

Przejdź do pozycji:

→ 1 *(odnośnik)*

→ 2 *(odnośnik)*

→ 3 *(odnośnik)*

→ 4 *(odnośnik)*

→ 5 *(odnośnik)*

→ 6 *(odnośnik)*

→ 7 *(odnośnik)*

→ 8 *(odnośnik)*

→ 9 *(odnośnik)*

→ 10 *(odnośnik)*

→ 11 *(odnośnik)*

→ 12 *(odnośnik)*

| Nr | Co robimy | Ile warte rocznie (marża) | Pewność | Wdrożenie |
| --- | --- | --- | --- | --- |
| Pewne straty |  |  |  |  |
| 1 | Naprawić zakładanie konta w Safari na iPhone'ach | 75–83 tys. zł<br>rocznie, górny scenariusz; w horyzoncie 180 dni 86–95 tys. zł | Wysoka<br>awaria widoczna w danych | diagnoza 1–2 dni, poprawka 2–5 dni, sprawdzenie 1 tydzień |
| 2 | Oczyścić codzienny raport i dodać alarmy na lejku i zwrotach | 0 albo 38 tys. zł<br>rocznie bezpośrednio; przede wszystkim warunek pozostałych decyzji | Wysoka<br>oba błędy widoczne w danych | 1 dzień sprawdzenie, 1–2 tygodnie raport |
| Pauzy, które da się cofnąć |  |  |  |  |
| 3 | Wstrzymać kampanię TikTok na L4 | +19 do +48 tys. zł<br>rocznie, nawet gdy każdy jej pacjent przyszedł tylko dzięki niej; więcej, gdy część przyszłaby i tak | Wysoka<br>kampania traci według obu reguł przypisania; niepewna jest tylko wielkość zysku z pauzy | 1 dzień |
| 4 | Wstrzymać kampanię Google Ads na specjalistów do czasu zmiany cennika | +19 do +32 tys. zł<br>rocznie, nawet gdy każdy jej pacjent przyszedł tylko dzięki niej; do +53 tys. zł, gdy przyszliby i bez niej | Wysoka<br>kampania traci według obu reguł przypisania; niepewna jest tylko wielkość zysku z pauzy | 1 dzień |
| Działania z wyceną |  |  |  |  |
| 5 | Zmienić obietnicę w reklamach Meta na L4; zasady zwrotów rozważyć osobno | 11–18 tys. zł<br>rocznie za samą nową kreację; zmiana zasad zwrotów przy odmowie L4 to osobna decyzja: 27–46 tys. zł | Średnia<br>nie znamy powodu zwrotów | 1–2 tygodnie + 4–6 tygodni pomiaru |
| 6 | Zdiagnozować poranne opóźnienia internistów, potem przetestować obsadę | 0–65 tys. zł<br>rocznie, scenariusz; wariant wąski około 12 tys. zł; bez kosztu obsady | Niska<br>opóźnienia są pewne; nie wiemy, ile powrotów przywróci punktualność | diagnoza 1–2 dni, test 2–4 tygodnie |
| 7 | Wprowadzić komunikację po wizycie, zawsze z losową grupą bez wysyłki | 23,6 tys. zł<br>za każdy punkt procentowy powrotu w 90 dniach; marża do 180. dnia; scenariusz | Niska<br>nie wiemy, ile powrotów wywoła sama wiadomość | dane o wysyłkach kilka dni, sekwencja 2–4 tygodnie, pomiar 90 dni |
| 8 | Sprawdzić ręcznie zakup dla pacjentów zalogowanych od wejścia | 0 albo 36–40 tys. zł<br>rocznie; wysoki scenariusz 89 tys. zł | Niska<br>dane wskazują raczej na 0 zł | 1 dzień |
| 9 | Sprawdzić testem w części kraju, czy kampania Meta na L4 się opłaca | od −31 do +180 tys. zł<br>rocznie: tyle warta jest decyzja o wyłączeniu, zależnie od tego, ilu pacjentów przyszłoby i bez kampanii | Test | 1 tydzień + 4–6 tygodni |
| 10 | Zmienić cennik specjalistów i warunki TelemediGO u specjalistów | 15–31 tys. zł<br>rocznie za warunki TelemediGO po pełnym roku; cennik do 74 tys. zł za każde 10 zł podwyżki, górna granica | Średnia<br>kierunek jest pewny; nie wiemy, ile da zmiana cennika | 1–2 tygodnie + test dwóch cen 4 tygodnie |
| Bez oszacowanego efektu |  |  |  |  |
| 11 | Sprawdzić, gdzie znika ruch między kliknięciem reklamy a wejściem na stronę w Meta i TikToku | 0 albo do 52 tys. zł<br>rocznie, górna granica; po wstrzymaniu TikToka mniej | Niska<br>nie wiemy, czy brakujące sesje da się odzyskać | 1–2 dni |
| 12 | Sprawdzić losowym testem, ile wizyt i powrotów dokłada zniżka TelemediGO | koszt 3–12 tys. zł<br>zniżki przy niezmienionej liczbie wizyt | Test | 2–8 tygodni + 90 dni |

### Najpierw pewne straty i pauzy, które da się cofnąć, potem testy

Kolejność oznacza wagę decyzji. Każda kwota to osobny scenariusz, więc kwot nie sumujemy.

- Najpierw pewne straty, które rosną każdego dnia i łatwo je naprawić (pozycje 1 i 2). Potem pauzy, które da się cofnąć (3 i 4). Potem naprawy, diagnozy i testy, które mają wycenę (5–10). Test Mety (pozycja 9) ma nieznany znak, ale wycenę i największą stawkę, więc stoi w tej grupie. Na końcu dwie pozycje bez oszacowanego efektu: pozycja 11 ma tylko górną granicę możliwej korzyści, a pozycja 12 tylko koszt testu.
- W pierwszym tygodniu zespół może zrobić równolegle pozycje 1, 3 i 4 oraz pierwsze, krótkie kroki pozycji 2, 5, 6, 8 i 11 (decyzje na pierwszy tydzień w zakładce „Czy to wzrost”).
- Wartość to zmiana marży na rok: przychód z konsultacji po zwrotach i opłaty TelemediGO minus koszt lekarza, wydatki na kampanie i prowizja afiliacyjna. Rokiem bazowym są ostatnie 12 miesięcy.
- Pieniędzy uwolnionych przez pozycje 3 i 4 nie przesuwamy automatycznie do innych kampanii, tylko z testem.

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

- Wartość to zmiana marży na rok. Rokiem bazowym są ostatnie 12 miesięcy. Marża = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza − wydatki na kampanie − prowizja afiliacyjna.
- Przy kampaniach podajemy wynik po 90 i po 180 dniach od pozyskania oraz według obu reguł źródła. Kwoty kampanii, które działały krócej niż rok, przeliczamy na pełny rok przy tym samym tempie: TikTok działał w ostatnich 12 miesiącach przez 234 dni (mnożnik 1,56), Meta na L4 przez 332 dni (1,10).
- Tempo ostatniego półrocza: od 1.04 do 30.09.2026 obie kampanie wydają dziennie więcej niż średnio (Meta na L4 o 14,9%, TikTok o 14,3%), a nowych pacjentów przybywa dziennie tylko o 9,2% i 12,5% więcej. W tym tempie wynik kampanii jest gorszy niż w przeliczeniu ze średniej: Meta na L4 +23,1 zamiast +30,6 tys. zł rocznie, TikTok −23,2 zamiast −18,6 tys. zł (według pierwszego wejścia, 90 dni). Kierunek żadnej decyzji się nie zmienia.
- Każda kwota to osobny scenariusz liczony względem tego, co działo się w ostatnich 12 miesiącach; nie zakłada, że wcześniejsze pozycje już wdrożono. Jedyny wyjątek: naprawę obietnicy L4 (pozycja 5) wyceniamy tylko dla Meta, bo zakładamy wstrzymanie TikToka (pozycja 3). Kwot nie sumujemy: mają różne horyzonty i nakładają się na siebie.
- Kolejność oznacza wagę decyzji. Najpierw pewne straty, które rosną każdego dnia i łatwo je naprawić (pozycje 1 i 2). Potem pauzy, które da się cofnąć (3 i 4). Potem naprawy, diagnozy, testy i sprawdzenia, które mają wycenę (5–10); test Mety ma wśród nich nieznany znak, ale największą stawkę. Na końcu pozycje bez wyceny: 11 ma tylko górną granicę, a 12 tylko koszt testu. Pozycje 1, 3, 4 i krótkie sprawdzenia (pierwsze kroki pozycji 2, 5, 6, 8 i 11) zespół może zrobić równolegle w pierwszym tygodniu.
- Zasada budżetu: pieniędzy uwolnionych przez pozycje 3 i 4 nie przesuwamy automatycznie do innych kampanii, bo kolejna złotówka zarabia zwykle mniej niż średnia. Przesuwamy tylko z testem. Niewydanie ich też liczy się do marży.
- Czas wdrożenia szacujemy sami; w danych go nie ma.

Rok wcześniej = X 2024 – IX 2025, ostatnie 12 miesięcy = X 2025 – IX 2026; jeśli nie napisano inaczej, liczby dotyczą ostatnich 12 miesięcy. Według pierwszego wejścia = źródłem pacjenta jest jego pierwsze wejście na stronę (także anonimowe sesje jego przeglądarek), a kod kampanii na pierwszym zamówieniu rozstrzyga. Według sesji z płatnością = źródłem jest sesja, w której zapłacił; pokazujemy ją obok, do porównania. Nowe kampanie = meta_prosp_l4_szybko (Meta, od 3.11.2025) i tt_prosp_l4_15min (TikTok, od 9.02.2026), obie na zwolnienie lekarskie (L4).

### 1. Naprawić zakładanie konta w Safari na iPhone'ach

Od 17 marca 2026 nowi pacjenci na iPhone'ach rzadziej kończą zakładanie konta, co kosztuje około 100 pierwszych zamówień miesięcznie.

*Ile warte rocznie (marża): 75–83 tys. zł — rocznie, górny scenariusz; w horyzoncie 180 dni 86–95 tys. zł · Pewność: Wysoka — awaria widoczna w danych · Wdrożenie: diagnoza 1–2 dni, poprawka 2–5 dni, sprawdzenie 1 tydzień*

*[Wykres] Krok konta po wyborze terminu, osoby, które jeszcze nie kupowały: Safari na iPhone'ach i pozostałe przeglądarki przed awarią i po niej*

- Safari na iPhone'ach: przed awarią 66%, po awarii 46% [−20 pkt proc. gorzej]
- Pozostałe przeglądarki: przed awarią 65%, po awarii 63% [−2 pkt proc.]

*Odsetek sesji po wyborze terminu, które przechodzą przez krok konta. Przed awarią: 16.01.2026–16.03.2026. Po awarii: Safari 17.03.2026–30.09.2026, pozostałe przeglądarki 17.03.2026–15.05.2026.*

**Dlaczego:**
Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spadł w Safari na iPhone'ach z 66% do 46% i nie wraca. W innych przeglądarkach takiego spadku nie ma.

**Co robimy:**
Powtórzyć rejestrację na iPhonie, przejrzeć logi błędów rejestracji i listę zmian z 16–17 marca 2026, wdrożyć poprawkę.

**Po czym poznamy:**
Krok konta po wyborze terminu w Safari na iOS u osób, które jeszcze nie kupowały, wraca z około 46% do około 66% w ciągu tygodnia od poprawki, a zakładanie kont wraca do poziomu sprzed 17.03 (około 1 080 w 60 dniach).

Zobacz w danych: Lejek: krok konta w Safari na iOS przed awarią i po niej; Zdarzenie na osi: awaria Safari na iOS *(odnośniki)*

Czego nie wiemy: punkt 6; punkt 7 *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Z danych

- Od 17.03.2026 w Safari na iPhone'ach i iPadach gwałtownie spada skuteczność zakładania nowego konta (konta dalej powstają, ale rzadziej: 668 zamiast 1 082 w 60 dniach).
- Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spada z 66,1% (od 1.10.2025 do 16.03.2026) do 45,6% (od 17.03 do 30.09.2026, 4 678 sesji z wyborem terminu) i nie wraca.
- Logowanie do istniejących kont działa. Inne przeglądarki tego nie mają, a spadek jest w głównych kanałach; TikTok ma za małą próbę do oceny.

#### Ile warta

- W 198 dniach od 17.03 do 30.09.2026 to 628–695 utraconych pierwszych zamówień, czyli 1 158–1 281 rocznie.
- Nowy pacjent z pierwszą płatnością w Safari na iOS zostawia w ostatnich 12 miesiącach średnio 64,6 zł marży przed kosztem pozyskania w 90 dniach (2 990 pacjentów) i 74,3 zł w 180 dniach (2 278).
- Daje to 75–83 tys. zł rocznie w horyzoncie 90 dni i 86–95 tys. zł w horyzoncie 180 dni.
- W samym III kwartale 2026 szacowana marża utracona to około 14,6–18,3 tys. zł (258–323 utracone pierwsze zamówienia z ich powrotami w tym samym kwartale, zależnie od odjęcia tła i założonego tempa strat), a osobny scenariusz powrotów pacjentów utraconych od 17.03 do 30.06 daje 4,1–4,5 tys. zł. Wyniku kwartału bez awarii nie mierzymy.
- 628–695 to dwa scenariusze przy przyjętych założeniach: po odjęciu zmiany w pozostałych przeglądarkach i bez tego odjęcia.

#### Założenia

- Utracone pierwsze zamówienie to utracony nowy pacjent. To górna granica: odpadnięci nie kupują później częściej w tej samej przeglądarce, ale innych urządzeń nie widzimy.
- Nie doliczamy kosztu pozyskania, bo wejście już zostało opłacone.
- Skala problemu utrzymywałaby się przez rok. Przeliczenie z marca–września może zaniżać, bo pomija zimę.
- Kwoty to marża rocznika odzyskanych pacjentów; część tej marży wpływa dopiero w kolejnym roku.

Skąd liczby: analiza/wyniki/c_priorytety.txt (P1, P15), analiza/wyniki/d_wynik.txt (1f), analiza/wyniki/a5p_zdarzenia.txt (5d–5f), notatki/a5_pozyskanie.md (sekcja 2).

Wróć do przeglądu

### 2. Oczyścić codzienny raport i dodać alarmy na lejku i zwrotach

Raport pokazuje wzrost zamówień o 61% zamiast 56% i nie pokazuje ani marży, ani powrotów kohort.

*Ile warte rocznie (marża): 0 albo 38 tys. zł — rocznie bezpośrednio; przede wszystkim warunek pozostałych decyzji · Pewność: Wysoka — oba błędy widoczne w danych · Wdrożenie: 1 dzień sprawdzenie, 1–2 tygodnie raport*

**Dlaczego:**
Awaria w Safari trwała 198 dni bez alarmu. Alarm na krokach lejka wykryłby ją po kilku dniach; wykrycie po tygodniu ograniczyłoby stratę do 22–25 pierwszych zamówień zamiast 628–695.

**Co robimy:**
- Usunąć z raportu duplikaty i konta testowe, a przychód liczyć po zwrotach.
- Przenieść testy z produkcji na środowisko testowe.
- Sprawdzić w dziale rozliczeń (jeden dzień), czy lekarze dostają wynagrodzenie za wizyty testowe.
- Sprawdzić, czy kod TEST-QA nie wyciekł poza 22 konta i czy przy duplikatach nikt nie zapłacił dwa razy.
- Dodać do raportu marżę po koszcie pozyskania według źródła, zwroty po wizycie według kampanii, powrót w 90 dniach każdej kohorty dziennej i kroki lejka według przeglądarki, z alarmami.

**Po czym poznamy:**
Raport pokazuje te same liczby co oczyszczona warstwa danych (w ostatnich 12 miesiącach: 38 491 zamówień i 3,228 mln zł przychodu z konsultacji po zwrotach), a od ustalonej daty na produkcji nie ma zamówień testowych.

Zobacz w danych: Jakość danych: duplikaty, zamówienia testowe, mostek od dashboardu; Zdarzenie na osi: duplikaty zamówień *(odnośniki)*

Czego nie wiemy: punkt 13; punkt 21 *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Z danych

- Codzienny raport liczy dane na surowo. Zawiera 604 zdublowane zamówienia z 10–24.06.2026, 2 071 zamówień 22 kont testowych i przychód przed zwrotami.
- Konta testowe mają kod TEST-QA albo zamówienia bez kodu, a wszystkie ich wizyty trwają 1 minutę u internisty.
- Przez to raport pokazuje +60,7% zamówień (25 269 → 40 613) zamiast +55,7% (24 716 → 38 491) i +50,3% przychodu z konsultacji zamiast +44,8% po zwrotach.
- Testów przybywa: 553 zamówienia rok wcześniej i 1 518 w ostatnich 12 miesiącach.
- Raport liczy zamówienia i przychód, bez marży po koszcie pozyskania i bez powrotów kohort. Dlatego kampanie na L4 wyglądały na nim jak wzrost.
- Do pilnowania: koszt kliknięcia w Google Ads na markę rośnie. Z 1,01 zł do 1,19 zł (+17,9% rok do roku, 13 894 i 19 828 kliknięć), co kwartał wyżej. Koszt pierwszego zamówienia z tej kampanii rośnie z 7,53 zł do 11,33 zł (według pierwszego wejścia). Kampania na e-receptę drożeje o 18,9% za kliknięcie, a całe Google Ads tanieje o 3,5%. Od 22.05.2026 spada też konwersja sesji tej kampanii do płatności (niewiadoma 21).

#### Ile warta

- Bezpośrednio 37 950 zł rocznie, jeśli lekarze dostają 25 zł za każdą wizytę testową (wszystkie są u internisty), albo 0 zł, jeśli nie dostają. Pieniądze już wypłacone są stracone, a oszczędność dotyczy kolejnych miesięcy.
- Pośrednio: bez poprawnych liczb nie da się prowadzić biznesu na kohortach. Alarm na krokach lejka wykryłby awarię Safari po kilku dniach, a bez alarmu trwała 198 dni. Wykrycie po tygodniu ograniczyłoby stratę do 3,5% (22–25 zamówień zamiast 628–695).

Skąd liczby: analiza/wyniki/c_priorytety.txt (P1b, P13, P15, W3), analiza/wyniki/a3_dashboard.txt, analiza/wyniki/a2_jakosc.txt, analiza/wyniki/d_kampanie.txt (4).

Wróć do przeglądu

### 3. Wstrzymać kampanię TikTok na L4

Kampania traci na każdym pozyskanym pacjencie według obu reguł przypisania, a jej pacjenci prawie nie wracają.

*Ile warte rocznie (marża): +19 do +48 tys. zł — rocznie, nawet gdy każdy jej pacjent przyszedł tylko dzięki niej; więcej, gdy część przyszłaby i tak · Pewność: Wysoka — kampania traci według obu reguł przypisania; niepewna jest tylko wielkość zysku z pauzy · Wdrożenie: 1 dzień*

**Dlaczego:**
Wynik na pacjenta po koszcie pozyskania jest ujemny według obu reguł przypisania i po 90, i po 180 dniach. Nawet najkorzystniejsza naprawa zwrotów, czyli zmiana ich zasad, daje według pierwszego wejścia wynik bliski zera, a według sesji z płatnością dalej stratę.

**Co robimy:**
Wstrzymać od razu, jako pauzę, którą da się cofnąć w jeden dzień. Naprawy obietnicy i ładowania strony sprawdzić najpierw na Mecie; TikTok może wrócić jako mały test, jeśli zadziałają.

**Po czym poznamy:**
Zmianę po pauzie porównujemy z ustalonym z góry punktem odniesienia (te same tygodnie rok wcześniej i kanały bez zmian): marża całego biznesu po wydatkach rośnie, a łączna liczba nowych pacjentów spada mniej niż liczba pacjentów przypisanych dotąd TikTokowi. Sam wzrost marży po pauzie nie dowodzi skutku, bo może wynikać z sezonu. Pauza daje przy okazji słaby, darmowy pomiar tego, ilu pacjentów przyszłoby i bez kampanii.

*Kampania TikTok na L4: kwoty z 234 dni działania, pod spodem pełny rok (×1,56)*

|  | Według pierwszego wejścia, 90 dni | Według pierwszego wejścia, 180 dni | Według sesji z płatnością, 90 dni | Według sesji z płatnością, 180 dni |
| --- | --- | --- | --- | --- |
| Wynik kampanii dziś | −11,9 tys. zł<br>pełny rok: −18,6 tys. zł | −13,5 tys. zł<br>pełny rok: −21,0 tys. zł | −30,8 tys. zł<br>pełny rok: −48,0 tys. zł | −32,3 tys. zł<br>pełny rok: −50,4 tys. zł |
| Wynik po samej nowej kreacji reklamy (pozycja 5) | −6,1 tys. zł<br>pełny rok: −9,5 tys. zł | −7,7 tys. zł<br>pełny rok: −11,9 tys. zł | −27,8 tys. zł<br>pełny rok: −43,4 tys. zł | −29,4 tys. zł<br>pełny rok: −45,8 tys. zł |
| Wynik po zmianie zasad zwrotów (wizyta przy odmowie L4 zostaje opłacona) | +3,0 tys. zł<br>pełny rok: +4,6 tys. zł | +1,4 tys. zł<br>pełny rok: +2,2 tys. zł | −23,2 tys. zł<br>pełny rok: −36,2 tys. zł | −24,7 tys. zł<br>pełny rok: −38,6 tys. zł |
| Zmiana marży po wyłączeniu, gdy każdy pacjent przyszedł tylko dzięki kampanii | +11,9 tys. zł<br>pełny rok: +18,6 tys. zł | +13,5 tys. zł<br>pełny rok: +21,0 tys. zł | +30,8 tys. zł<br>pełny rok: +48,0 tys. zł | +32,3 tys. zł<br>pełny rok: +50,4 tys. zł |
| Zmiana marży po wyłączeniu, gdy połowa pacjentów przyszłaby i bez niej | +47,2 tys. zł<br>pełny rok: +73,6 tys. zł | +48,0 tys. zł<br>pełny rok: +74,8 tys. zł | +56,6 tys. zł<br>pełny rok: +88,3 tys. zł | +57,4 tys. zł<br>pełny rok: +89,5 tys. zł |
| Zmiana marży po wyłączeniu, gdy wszyscy pacjenci przyszliby i bez niej | +82,5 tys. zł<br>pełny rok: +128,6 tys. zł | +82,5 tys. zł<br>pełny rok: +128,6 tys. zł | +82,5 tys. zł<br>pełny rok: +128,6 tys. zł | +82,5 tys. zł<br>pełny rok: +128,6 tys. zł |

Zobacz w danych: Wynik biznesu: ekonomia kampanii, obie reguły; Kohorty: nowe kampanie na L4 i pozostałe; Zdarzenie na osi: start TikToka *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Z danych

- Wynik na pacjenta jest ujemny w obu regułach i w obu oknach: −4,6 i −17,8 zł po 90 dniach, −1,1 i −11,0 zł po 180 dniach. Pacjenci wracają w 90 dniach w 3,2% (1 265 pacjentów według pierwszego wejścia, kohorty od 9.02.2026).

#### Naprawić albo wyłączyć

- Kwoty z 234 dni działania kampanii w ostatnich 12 miesiącach, w nawiasie pełny rok (mnożnik 1,56).
- Dziś: −11,9 tys. zł (−18,6) według pierwszego wejścia i −30,8 tys. zł (−48,0) według sesji z płatnością po 90 dniach; −13,5 i −32,3 tys. zł po 180 dniach.
- Naprawić zwroty, zmieniając ich zasady (najkorzystniejszy wariant naprawy): wynik +3,0 tys. zł albo −23,2 tys. zł po 90 dniach; +1,4 i −24,7 tys. zł po 180 dniach. Przeglądarki wbudowane w aplikacje nie dają w tym rachunku nic.
- Wyłączyć, gdy każdy pacjent przyszedł tylko dzięki kampanii: +11,9 do +30,8 tys. zł (+18,6 do +48,0 na pełny rok) po 90 dniach i +13,5 do +32,3 tys. zł (+21,0 do +50,4 na pełny rok) po 180 dniach; gdy wszyscy przyszliby i bez niej, +82,5 tys. zł (+128,6).
- W scenariuszu samej nowej kreacji (pozycja 5), w którym uczciwa obietnica zniechęca osoby, które dostałyby zwrot, wynik w 234 dniach działania wynosi −6,1 tys. zł albo −27,8 tys. zł po 90 dniach i −7,7 tys. zł albo −29,4 tys. zł po 180 dniach, więc kampania nadal traci według obu reguł przypisania.

#### Propozycja

- Wstrzymać od razu, jako odwracalną pauzę. W przyjętych scenariuszach wyłączenie poprawia wynik według obu reguł przypisania, w obu oknach i niezależnie od tego, ilu pacjentów przyszłoby i bez kampanii. Naprawa przy pełnym budżecie daje w najlepszym razie wynik bliski zera.
- Wynik po 180 dniach (−1,1 zł na pacjenta według pierwszego wejścia, warunkowy przedział od −5,3 do +3,0 zł) obejmuje tylko wczesne kohorty z 10.02–3.04.2026 (299 pacjentów). Miały one tańsze pozyskanie niż cały rocznik (32,4 zł wobec 37,3 zł), a w dniach 91–180 nie dorobiły marży. Lepszy wynik niż po 90 dniach (−4,6 zł, 1 265 pacjentów) wynika więc z tańszego pozyskania, bez późniejszych powrotów.
- Przybliżenie dla całego rocznika (marża w 90 dniach wszystkich kohort plus przyrost z dni 91–180 wczesnych kohort, minus koszt pozyskania całego rocznika) daje −5,4 zł (od −7,4 do −3,4 zł) według pierwszego wejścia i −19,3 zł według sesji z płatnością. Znak jest więc ujemny w obu regułach.
- Naprawy (obietnica, ładowanie strony) sprawdzamy na Meta. TikTok może wrócić jako mały test, jeśli zadziałają.

Skąd liczby: analiza/wyniki/c_priorytety.txt (P3, P11), analiza/wyniki/a5e_scenariusze.txt (E1, E3, E3b), analiza/wyniki/a5e_kampanie.csv, analiza/wyniki/d_kampanie.txt (2, 3), notatki/a5_ekonomia.md.

Wróć do przeglądu

### 4. Wstrzymać kampanię Google Ads na specjalistów do czasu zmiany cennika

Pozyskanie pacjenta kosztuje około 58 zł, a pacjent zostawia w 90 dniach około 32 zł marży.

*Ile warte rocznie (marża): +19 do +32 tys. zł — rocznie, nawet gdy każdy jej pacjent przyszedł tylko dzięki niej; do +53 tys. zł, gdy przyszliby i bez niej · Pewność: Wysoka — kampania traci według obu reguł przypisania; niepewna jest tylko wielkość zysku z pauzy · Wdrożenie: 1 dzień*

**Dlaczego:**
Wizyta u specjalisty po cenie katalogowej zostawia ponad koszt lekarza tylko 9–19 zł, więc kampania nie ma z czego pokryć kosztu pozyskania (pozycja 10).

**Co robimy:**
Wstrzymać. Wrócić po zmianie cennika albo gdy koszt pozyskania nie przekracza marży pacjenta w 90 dniach w obu regułach.

**Po czym poznamy:**
Liczymy wszystkich nowych pacjentów z pierwszą wizytą u specjalisty, ze wszystkich kanałów (w ostatnich 12 miesiącach średnio 66 tygodniowo), i marżę całego biznesu po wydatkach, wobec tych samych tygodni rok wcześniej, tak jak w teście Mety. Pauza się opłaca, dopóki nowych pacjentów u specjalistów ubywa mniej niż około 31 tygodniowo; kampania przypisuje sobie 13–18 tygodniowo.

*Kampania Google Ads na specjalistów: kwoty roczne z ostatnich 12 miesięcy*

|  | Według pierwszego wejścia, 90 dni | Według pierwszego wejścia, 180 dni | Według sesji z płatnością, 90 dni | Według sesji z płatnością, 180 dni |
| --- | --- | --- | --- | --- |
| Wynik kampanii dziś | −23,2 tys. zł | −19,4 tys. zł | −31,5 tys. zł | −30,2 tys. zł |
| Zmiana marży po wyłączeniu, gdy każdy pacjent przyszedł tylko dzięki kampanii | +23,2 tys. zł | +19,4 tys. zł | +31,5 tys. zł | +30,2 tys. zł |
| Zmiana marży po wyłączeniu, gdy połowa pacjentów przyszłaby i bez niej | +38,2 tys. zł | +36,3 tys. zł | +42,4 tys. zł | +41,7 tys. zł |
| Zmiana marży po wyłączeniu, gdy wszyscy pacjenci przyszliby i bez niej | +53,2 tys. zł | +53,2 tys. zł | +53,2 tys. zł | +53,2 tys. zł |

Zobacz w danych: Wynik biznesu: ekonomia kampanii (poziom: kampanie); Kohorty: pacjenci tej kampanii według pierwszej usługi *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Z danych

- Wynik na pacjenta jest ujemny w obu regułach i obu oknach: −23,7 i −44,7 zł po 90 dniach, −14,3 i −36,6 zł po 180 dniach.
- Koszt pozyskania wynosi 57,6 zł (według pierwszego wejścia) albo 80,9 zł (według sesji z płatnością) przy marży pacjenta przed kosztem pozyskania 32–37 zł.
- Jednym z głównych ograniczeń marży jest cennik: wizyta u specjalisty po cenie katalogowej zostawia tylko 9–19 zł ponad koszt lekarza (pozycja 10). Wynik zależy też od kosztu pozyskania, struktury usług i powrotów.

#### Naprawić albo wyłączyć

- Rocznie 923 nowych pacjentów według pierwszego wejścia, 657 według sesji z płatnością, wydatki 53,2 tys. zł.
- Dziś: −23,2 tys. zł i −31,5 tys. zł po 90 dniach; −19,4 i −30,2 tys. zł po 180 dniach (bez pośredniego zaokrąglania marży).
- Naprawić: sama kampania musiałaby obniżyć koszt pozyskania o 40–60%, a to inny model kampanii, nie naprawa. Główną drogą naprawy jest cennik (pozycja 10). Uwaga: awaria Safari od 17.03 zawyża koszt pozyskania także tej kampanii.
- Wyłączyć: +19,4 do +31,5 tys. zł, gdy każdy pacjent przyszedł tylko dzięki kampanii, +36,3 do +42,4 tys. zł, gdy połowa przyszłaby i bez niej, i +53,2 tys. zł, gdy wszyscy przyszliby i bez niej. Założenia: pacjenci, którzy przyszli tylko dzięki kampanii, mają średnią marżę przypisanych, pozostali zachowują się jak dziś, koszty pozostałych kanałów się nie zmieniają.

#### Propozycja

- Wstrzymać. Wrócić po zmianie cennika albo gdy koszt pozyskania nie przekracza marży pacjenta w 90 dniach w obu regułach.
- Próg pauzy = wydatki kampanii w ostatnich 12 miesiącach (53,2 tys. zł) podzielone przez marżę jej pacjenta w 90 dniach (32,4 zł według pierwszego wejścia, 32,9 zł według sesji z płatnością): 1 640 albo 1 614 pacjentów rocznie. Kampania przypisuje sobie 923 albo 657 nowych pacjentów rocznie. Wszystkich nowych pacjentów z pierwszą wizytą u specjalisty (bez internisty, pediatry i psychiatry) było 3 427 w ostatnich 12 miesiącach i 2 971 rok wcześniej.

Skąd liczby: analiza/wyniki/c_priorytety.txt (P7), analiza/wyniki/a5e_kampanie.csv, analiza/wyniki/c_telemedigo.txt (3a), notatki/ZALOZENIA.md (punkt 42).

Wróć do przeglądu

### 5. Zmienić obietnicę w reklamach Meta na L4; zasady zwrotów rozważyć osobno

17% wizyt L4 z nowych kampanii kończy się zwrotem pieniędzy, wobec 5% u pozostałych pacjentów, a lekarz i tak dostaje wynagrodzenie.

*Ile warte rocznie (marża): 11–18 tys. zł — rocznie za samą nową kreację; zmiana zasad zwrotów przy odmowie L4 to osobna decyzja: 27–46 tys. zł · Pewność: Średnia — nie znamy powodu zwrotów · Wdrożenie: 1–2 tygodnie + 4–6 tygodni pomiaru*

**Dwie różne decyzje:**
- Nowa kreacja i pytanie przed płatnością („lekarz wystawia L4 tylko przy wskazaniach medycznych”). Uczciwa obietnica zniechęca część osób, które i tak dostałyby zwrot. Warta 10,7–18,1 tys. zł rocznie, zależnie od reguły przypisania.
- Zmiana zasad zwrotów przy odmowie L4: wizyta zostaje opłacona, bo pacjent dostał konsultację. Warta 26,7–46,5 tys. zł rocznie, ale to osobna decyzja z ryzykiem prawnym i wizerunkowym (Czego nie wiemy, punkt 17).
- Obie kwoty to scenariusze tych samych zwrotów, więc się nie sumują. Po wstrzymaniu TikToka dotyczą tylko Mety.

**Co robimy:**
Najpierw jednodniowe sprawdzenie, co obiecują reklama, strona wejścia i regulamin przy odmowie L4. Potem w Mecie losowy podział ruchu na starą i nową kreację. Przy okazji przetestować wysokość kodu rabatowego (dziś 20 zł).

**Po czym poznamy:**
Odsetek zwrotów po wizycie L4 przy nowej kreacji spada wobec starej, a marża na kliknięcie nie spada. Liczy się marża, nie sam odsetek zwrotów.

Zobacz w danych: Po zakupie: zwroty po wizycie według celu wizyty; Zdarzenie na osi: więcej pierwszych zamówień zwracanych po wizycie *(odnośniki)*

Czego nie wiemy: punkt 3; punkt 17; punkt 20 *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Ile warte, osobno dla dwóch decyzji

- Wariant kreacji (uczciwa obietnica zniechęca osoby, które nie dostałyby L4): 16,5 tys. zł w 332 dniach działania kampanii według pierwszego wejścia i 9,7 tys. zł według sesji z płatnością, na pełny rok 18,1 tys. zł i 10,7 tys. zł.
- Wariant zasad zwrotów (wizyty, które dziś kończą się zwrotem, zostają opłacone): 42,3 tys. zł i 24,3 tys. zł, na pełny rok 46,5 tys. zł i 26,7 tys. zł.

#### Z danych

- 17,4% odbytych wizyt L4 pacjentów nowych kampanii kończy się zwrotem po wizycie (1 024 z 5 895), wobec 5,3% L4 pozostałych pacjentów (5 080 wizyt) w ostatnich 12 miesiącach.
- Kod rabatowy ani opóźnienie wizyty nie zmieniają tego odsetka. Za zwróconą wizytę lekarz dostaje wynagrodzenie.
- 1 024 to zwroty przy samych wizytach L4. Zakładka „Po zakupie” pokazuje 1 044 zwroty po wizycie u pacjentów nowych kampanii, bo liczy wszystkie cele wizyty, także e-receptę i konsultację.

#### Założenia i zastrzeżenia

- Wariant kreacji zakłada, że uczciwa reklama odstrasza tylko tych, którzy i tak dostaliby zwrot. W praktyce odstraszy też część pozostałych, więc może być niżej.
- Wariant zasad zwrotów („wizyta zostaje opłacona”) wymaga zmiany zasad zwrotów, nie tylko treści reklamy. To osobna decyzja z ryzykiem prawnym i wizerunkowym.
- 5,3% to odsetek z innej grupy pacjentów, więc pełne zrównanie jest optymistyczne. Rozsądny wariant bazowy to zmniejszenie tej różnicy o połowę.

#### Co robimy

- Najpierw jednodniowe sprawdzenie, co obiecują reklama, strona /zwolnienie-l4-online i regulamin przy odmowie L4.
- Potem nowa kreacja i pytanie przed płatnością („lekarz wystawia L4 tylko przy wskazaniach medycznych”).
- W Meta losowy podział ruchu na starą i nową kreację, z osobnym oznaczeniem kampanii.
- Wysokość kodu rabatowego do przetestowania. Kod L4SZYBKO20 (20 zł) jest na 3 511 z 5 059 pierwszych zamówień pacjentów kampanii w ostatnich 12 miesiącach (według pierwszego wejścia). Daje to 62,8 tys. zł zniżki efektywnej na pełny rok (bez wizyt anulowanych i zwróconych). Zwroty po wizycie przy pierwszym zamówieniu z kodem rabatowym i bez są prawie takie same (14,5% z 3 680 wobec 14,3% z 1 379 pierwszych zamówień), a powrót w 90 dniach nie różni się istotnie (4,15% z 2 649 wobec 5,41% z 979 pacjentów). Progi rachunku to parametry scenariusza: rezygnacja z kodu opłaca się, jeśli ubędzie mniej niż 33,7% zamówień z kodem, a przejście na stały kod START10 (10 zł), jeśli mniej niż 20,2%. Reakcji pacjentów na niższy kod nie znamy, więc to scenariusz do sprawdzenia w losowym podziale ruchu, bez kwoty (niewiadoma 20).

Skąd liczby: analiza/wyniki/c_priorytety.txt (P2, P11), analiza/wyniki/a5e_scenariusze.txt (E2a), analiza/wyniki/a5r_po_zakupie.txt (2b, 2d), analiza/wyniki/d_kampanie.txt (6).

Wróć do przeglądu

### 6. Zdiagnozować poranne opóźnienia internistów, potem przetestować obsadę

Od lutego 2026 około połowy porannych wizyt u internisty zaczyna się ponad 15 minut po terminie; do października 2025 było to 5–7%.

*Ile warte rocznie (marża): 0–65 tys. zł — rocznie, scenariusz; wariant wąski około 12 tys. zł; bez kosztu obsady · Pewność: Niska — opóźnienia są pewne; nie wiemy, ile powrotów przywróci punktualność · Wdrożenie: diagnoza 1–2 dni, test 2–4 tygodnie*

**Dlaczego:**
To jedna z konkretnych hipotez spadku retencji w kanałach działających w obu latach, a pierwszy krok, diagnoza, jest tani. W ostatnich 12 miesiącach pacjenci po spóźnionej porannej pierwszej wizycie wracają rzadziej niż po punktualnej, a spóźnione wizyty mają dużo niższe oceny (zakładka „Po zakupie”).

**Co robimy:**
- Diagnoza: grafiki i obsada poranna przed i po 3.11.2025, obciążenie lekarzy pacjentami spoza B2C, rozmowa z osobami od grafików.
- Potem naprawy, także bez dodatkowej obsady: liczba porannych terminów dopasowana do przepustowości, przesunięcie godzin lekarzy, realny czas oczekiwania pokazany pacjentowi.
- Na końcu test w losowo wybrane dni.

**Po czym poznamy:**
Odsetek porannych wizyt spóźnionych ponad 15 minut spada z około 50% poniżej 10%, oceny porannych wizyt rosną, a powrót w 90 dniach pacjentów z pierwszą wizytą rano, z tego samego źródła, wraca w stronę 23–24% (rok wcześniej: 23,6%, 2 844 pacjentów kampanii działających w obu latach).

Zobacz w danych: Po zakupie: punktualność według pory i opóźnienia przy tym samym ruchu; Zdarzenie na osi: poranne opóźnienia u internisty *(odnośniki)*

Czego nie wiemy: punkt 4 *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Z danych

- Od listopada 2025 do lutego 2026 poranne opóźnienia u internisty rosły z miesiąca na miesiąc, a potem utrzymywały się na poziomie około połowy wizyt. Odsetek wizyt z terminem 6:00–11:59, które zaczynają się ponad 15 minut po terminie (pacjenci spoza nowych kampanii, jak w zakładce „Po zakupie”), wynosi 15,7% w listopadzie 2025, 29,7% w grudniu i 42,6% w styczniu 2026, a od lutego do września 2026 około połowy (47,3–52,7% miesięcznie). Od października 2024 do października 2025 było to 4,7–6,9% miesięcznie. Liczby wizyt są w szczegółach zakładki „Po zakupie”.
- Przy tym samym porannym ruchu opóźnień jest o 26,4 punktu procentowego więcej (5 przedziałów ruchu, 9 979 wizyt).
- Długość porannej wizyty się nie zmieniła (8,5 minuty w obu okresach), więc dłuższe wizyty tego nie tłumaczą.
- Po godzinach (internista, wszyscy pacjenci): wzrost to jeden poranny blok od 5:00 do 13:59, najsilniejszy od 6:00 do 11:59 i mały o 13:00. Wizyt spóźnionych ponad 15 minut jest o 5:00 15,3% (459 wizyt) wobec 1,5% (267) rok wcześniej, o 6:00–10:00 od 40,4% do 47,0% (865–1 858 wizyt w godzinie) wobec 5,7–7,5%, o 12:00 22,3% (1 303) wobec 3,4% (774), o 13:00 5,6% (1 207) wobec 2,5% (719). Poza 5:00–13:59 odsetek jest prawie taki sam: 2,7% z 14 898 wizyt wobec 2,8% z 9 563. Wzrost w południe i w nocy to głównie brzegi porannego bloku: południe bez 12:00 rośnie z 2,9% do 3,9%, noc bez 5:00 z 2,0% do 3,1%. U pozostałych lekarzy rano bez istotnej zmiany (2,8% z 1 949 wizyt wobec 3,0% z 2 757).
- W ciągu poranka: już wizyty z najwcześniejszym porannym terminem w danym dniu są często spóźnione, a w danych zagregowanych nie widać narastania opóźnień w ciągu poranka. Wizyty z najwcześniejszym porannym terminem dnia są spóźnione ponad 15 minut w 41,9% (391 wizyt, ostatnie 12 miesięcy), kolejne w 43,3% (8 760), średnio 18,7 wobec 20,2 minuty. W tym samym miesiącu (II–IX 2026) godziny z 8 i więcej wizytami mają o 4,2 punktu procentowego więcej spóźnionych niż godziny z 1–3 wizytami.
- Nasze odczytanie: to bardziej pasuje do stałego przesunięcia od początku dnia (późniejszy start względem grafiku, inna organizacja zapisów albo kolejki) niż do kolejki, która narasta, bo pacjentów jest więcej, niż lekarze zdążą przyjąć. Najwcześniejszy termin liczymy dla całej sieci, bo w danych nie ma identyfikatorów lekarzy. Bez nich i bez grafików mechanizmu nie rozstrzygamy.
- Wizyty spóźnione ponad 30 minut mają średnią ocenę 2,92 wobec 4,45 przy punktualnych (ostatnie 12 miesięcy, internista, pacjenci spoza nowych kampanii, 469 i 3 446 ocen).

#### Ile warta

- Scenariusz od 0 zł do 65,2 tys. zł marży rocznie w horyzoncie 180 dni.
- Wariant wąski, czyli sama zmiana rozkładu opóźnień pierwszej wizyty, to 11,9–12,7 tys. zł zależnie od reguły źródła; prawie cały przypada na poranne pierwsze wizyty u internisty (12,6 tys. zł). Wariant szeroki (31,8–65,2 tys. zł) przypisuje opóźnieniom cały spadek powrotu w starych kampaniach, więc nie jest górną granicą skutku obsady.
- Związek opóźnień z powrotami może częściowo wynikać z tego, kto przychodzi rano, więc kwota jest niepewna. Kosztu dodatkowej obsady nie ma w danych.

Skąd liczby: analiza/wyniki/a5r_punktualnosc.txt (1c, 2b, 3f), analiza/wyniki/a5r_po_zakupie.txt (3a), analiza/wyniki/c_priorytety.txt (P8, P13), analiza/wyniki/d_retencja.txt (1, 2), analiza/wyniki/d_wynik.txt (4), notatki/a5_retencja.md.

Wróć do przeglądu

### 7. Wprowadzić komunikację po wizycie, zawsze z losową grupą bez wysyłki

Co siódmy powrót zaczyna się od wejścia z newslettera albo SMS-a, ale nie wiemy, ile z tych zakupów wiadomość faktycznie wywołała.

*Ile warte rocznie (marża): 23,6 tys. zł — za każdy punkt procentowy powrotu w 90 dniach; marża do 180. dnia; scenariusz · Pewność: Niska — nie wiemy, ile powrotów wywoła sama wiadomość · Wdrożenie: dane o wysyłkach kilka dni, sekwencja 2–4 tygodnie, pomiar 90 dni*

**Dlaczego:**
Retencja spada także poza nowymi kampaniami: w 90 dniach wraca 22% pacjentów wobec 24% rok wcześniej. Około 3 z tych 22 punktów procentowych to pacjenci, którzy wrócili w ciągu doby po kliknięciu newslettera albo SMS-a; pozostali wrócili inną drogą. To jedna grupa pacjentów podzielona według drogi powrotu.

**Co robimy:**
- Dane o wysyłkach: ile, komu, kiedy.
- Sekwencja po pierwszej wizycie (przypomnienie o kontynuacji leczenia, recepta, kontrola), zawsze z losową grupą kontrolną bez wysyłki.

**Po czym poznamy:**
Różnica powrotu w 90 dniach i marży między grupą z wysyłką a grupą kontrolną.

Zobacz w danych: Kohorty: powrót bez pacjentów nowych kampanii; Kohorty: powrót według źródła pozyskania *(odnośniki)*

Czego nie wiemy: punkt 9 *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Ile warta

- Każdy punkt procentowy powrotu w 90 dniach to około 23,6 tys. zł marży rocznie: 24 687 nowych pacjentów × 1% × 95,6 zł, gdzie 95,6 zł to różnica marży do 180. dnia między pacjentem, który wrócił w 90 dniach, a takim, który nie wrócił. Bez pacjentów nowych kampanii (17 419) 16,7 tys. zł. To różnica obserwacyjna; efektu samej wiadomości nikt jeszcze nie zmierzył.
- Podział powrotu w 90 dniach poza nowymi kampaniami (22,0%) według drogi powrotu: 3,16% po wejściu z newslettera albo SMS-a i 18,84% inną drogą; rok wcześniej 3,48% i 20,42%.

#### Z danych

- Retencja to połowa definicji wzrostu, a spada także bez pacjentów nowych kampanii: powrót w 90 dniach 22,0% (14 031 pacjentów) wobec 23,9% (12 867).
- Liczba wejść z newslettera i SMS-ów na 1 000 pacjentów spada z 56–108 miesięcznie rok wcześniej do 24–52 w ostatnich 12 miesiącach, ale mianownikiem jest cała narastająca baza pacjentów; w pierwszych 90 dniach od zakupu odsetek pacjentów z takim wejściem rośnie lekko z 17,5% do 17,9%. Widać tylko kliknięcia, bez danych o wysyłkach.

Skąd liczby: analiza/wyniki/c_priorytety.txt (W2, P12), analiza/wyniki/a5r_po_zakupie.txt (5e), notatki/a5_retencja.md (krok 4c).

Wróć do przeglądu

### 8. Sprawdzić ręcznie zakup dla pacjentów zalogowanych od wejścia

Żadna z 22 tys. sesji pacjentów zalogowanych od wejścia nie skończyła się zakupem konsultacji; jeden ręczny test pokaże, czy to błąd ścieżki zakupu.

*Ile warte rocznie (marża): 0 albo 36–40 tys. zł — rocznie; wysoki scenariusz 89 tys. zł · Pewność: Niska — dane wskazują raczej na 0 zł · Wdrożenie: 1 dzień*

**Co robimy:**
Zalogować się, wejść ponownie już zalogowanym, spróbować kupić bez ponownego logowania i sprawdzić, jakie kroki zapisała analityka.

**Po czym poznamy:**
Test daje odpowiedź od razu. Jeśli ścieżka jest zepsuta, po naprawie sesje zalogowane od wejścia zaczynają kończyć się płatnością.

Zobacz w danych: Lejek: sesje zalogowane od wejścia *(odnośniki)*

Czego nie wiemy: punkt 5 *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Z danych

- 22 068 sesji zalogowanych od wejścia przez dwa lata nie kończy się ani razu zakupem konsultacji, a każdy z 22 289 zakupów powtórnych ma krok logowania.
- Dane nie rozstrzygają między dwoma odczytaniami. Pierwsze: to wizyty „sprawdzam konto” albo sposób zapisu (logowanie zaczyna nową sesję). Drugie: ścieżka zakupu dla zalogowanych jest zepsuta. Kilka faktów przemawia za pierwszym.

#### Ile warta

- Jeśli to wizyty „sprawdzam konto”, 0 zł dla przychodu (ale wtedy cierpi pomiar lejka, pozycja 2). Jeśli ścieżka jest zepsuta, scenariusze: około 40 tys. zł rocznie na sesjach, około 36 tys. zł na pacjentach, wysoki scenariusz 89 tys. zł.

Skąd liczby: analiza/wyniki/c_priorytety.txt (P5), analiza/wyniki/a5p_zalogowane.txt, notatki/a5_pozyskanie.md (sekcja 3).

Wróć do przeglądu

### 9. Sprawdzić testem w części kraju, czy kampania Meta na L4 się opłaca

Według pierwszego wejścia kampania zarabia 31 tys. zł rocznie, według sesji z płatnością traci 32 tys. zł, a dane nie mówią, ilu jej pacjentów przyszłoby i bez niej.

*Ile warte rocznie (marża): od −31 do +180 tys. zł — rocznie: tyle warta jest decyzja o wyłączeniu, zależnie od tego, ilu pacjentów przyszłoby i bez kampanii · Pewność: Test · Wdrożenie: 1 tydzień + 4–6 tygodni*

**Dlaczego dopiero 9. miejsce:**
To największa kwota na liście, ale nie znamy nawet jej znaku, a test w 4–6 tygodni da tylko orientacyjny wynik. Wcześniej idą pewne straty i tanie kroki, które zespół może zrobić od razu.

**Co robimy:**
- Na 4–6 tygodni wyłączyć kampanię w połowie województw, losowo w parach podobnych województw, i porównać wszystkich nowych pacjentów oraz marżę. Wyłączamy na stałe, jeśli w województwach bez reklamy, w porównaniu z ich parami, ubędzie mniej nowych pacjentów niż około 85% tych, których kampania sobie tam w tym czasie przypisuje. Po samej nowej kreacji z pozycji 5 ten próg spada do około 79%, a po zmianie zasad zwrotów do około 70% (progi dla marży w 90 dniach).
- Gdy wynik testu jest niejednoznaczny, i tak decydujemy według jego wyniku: poniżej progu wyłączamy, powyżej zostawiamy. Taki wynik może przez przypadek wypaść po złej stronie progu, ale obie decyzje da się cofnąć, a pomiar powtórzyć.

**Po czym poznamy:**
Spadek wszystkich nowych pacjentów w województwach bez reklamy wobec par, w liczbie pacjentów i jako udział pacjentów przypisanych Meta; decyzja według reguły wyżej.

*Kampania Meta na L4: kwoty z 332 dni działania, pod spodem pełny rok (×1,10)*

|  | Według pierwszego wejścia, 90 dni | Według pierwszego wejścia, 180 dni | Według sesji z płatnością, 90 dni | Według sesji z płatnością, 180 dni |
| --- | --- | --- | --- | --- |
| Wynik kampanii dziś | +27,8 tys. zł<br>pełny rok: +30,6 tys. zł | +29,9 tys. zł<br>pełny rok: +32,9 tys. zł | −28,7 tys. zł<br>pełny rok: −31,6 tys. zł | −27,5 tys. zł<br>pełny rok: −30,2 tys. zł |
| Wynik po samej nowej kreacji reklamy (pozycja 5) | +44,3 tys. zł<br>pełny rok: +48,7 tys. zł | +46,4 tys. zł<br>pełny rok: +51,0 tys. zł | −19,0 tys. zł<br>pełny rok: −20,9 tys. zł | −17,7 tys. zł<br>pełny rok: −19,5 tys. zł |
| Wynik po zmianie zasad zwrotów (wizyta przy odmowie L4 zostaje opłacona) | +70,1 tys. zł<br>pełny rok: +77,1 tys. zł | +72,1 tys. zł<br>pełny rok: +79,3 tys. zł | −4,5 tys. zł<br>pełny rok: −4,9 tys. zł | −3,2 tys. zł<br>pełny rok: −3,5 tys. zł |
| Zmiana marży po wyłączeniu, gdy każdy pacjent przyszedł tylko dzięki kampanii | −27,8 tys. zł<br>pełny rok: −30,6 tys. zł | −29,9 tys. zł<br>pełny rok: −32,9 tys. zł | +28,7 tys. zł<br>pełny rok: +31,6 tys. zł | +27,5 tys. zł<br>pełny rok: +30,2 tys. zł |
| Zmiana marży po wyłączeniu, gdy połowa pacjentów przyszłaby i bez niej | +67,7 tys. zł<br>pełny rok: +74,5 tys. zł | +66,7 tys. zł<br>pełny rok: +73,4 tys. zł | +96,0 tys. zł<br>pełny rok: +105,6 tys. zł | +95,4 tys. zł<br>pełny rok: +104,9 tys. zł |
| Zmiana marży po wyłączeniu, gdy wszyscy pacjenci przyszliby i bez niej | +163,3 tys. zł<br>pełny rok: +179,6 tys. zł | +163,3 tys. zł<br>pełny rok: +179,6 tys. zł | +163,3 tys. zł<br>pełny rok: +179,6 tys. zł | +163,3 tys. zł<br>pełny rok: +179,6 tys. zł |

Zobacz w danych: Wynik biznesu: ekonomia kampanii, obie reguły; Kohorty: nowe kampanie na L4 i pozostałe; Zdarzenie na osi: start kampanii Meta na L4 *(odnośniki)*

Czego nie wiemy: punkt 1 *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Z danych

- Wynik kampanii zależy od reguły źródła: +27,8 tys. zł według pierwszego wejścia i −28,7 tys. zł według sesji z płatnością po 90 dniach, w 332 dniach działania (+30,6 i −31,6 tys. zł na pełny rok).
- Dane nie rozstrzygają, ilu jej pacjentów przyszłoby i bez niej.

#### Naprawić albo wyłączyć

- Naprawić zwroty: pozycja 5, w tej samej kampanii.
- Wyłączyć: od −30,6 tys. zł (gdy każdy pacjent przyszedł tylko dzięki kampanii, horyzont 90 dni) albo −32,9 tys. zł (180 dni) do +179,6 tys. zł (gdy wszyscy przyszliby i bez niej) na pełny rok.

#### Próg decyzji, ustalony przed testem

- Według pierwszego wejścia wyłączenie traci pieniądze tylko wtedy, gdy ponad około 85% pacjentów kampanii przyszło tylko dzięki niej: 85,4% w horyzoncie 90 dni i 84,5% w horyzoncie 180 dni. Według sesji z płatnością wyłączenie zyskuje zawsze.
- Próg po samej nowej kreacji: 78,7% (90 dni) i 77,9% (180 dni); po zmianie zasad zwrotów: 70,0% i 69,4%. Po naprawie kampania zarabia więcej na każdym pacjencie, więc opłaca się już wtedy, gdy mniejsza część jej pacjentów przyszła tylko dzięki niej. W tempie ostatniego półrocza próg dziś rośnie do 89,9%.
- W liczbie pacjentów próg prawie nie zależy od reguły źródła: wyłączenie opłaca się, jeśli po nim ubędzie mniej niż około 4 320 nowych pacjentów w 332 dniach działania kampanii w ostatnich 12 miesiącach (dziś, horyzont 90 dni; według sesji z płatnością około 4 360) albo 3 540 (po zmianie zasad zwrotów). Reguła zmienia głównie to, ilu pacjentów przypisujemy kampanii.

#### Czego ten test nie rozstrzygnie

- Test w 8 parach województw przez 4–6 tygodni nie da mocy potrzebnej do odróżnienia wyniku od progu. W połowie kraju kampania przypisuje około 55,7 nowego pacjenta tygodniowo (tempo III kwartału 2026, według pierwszego wejścia), a losowy rozrzut liczby nowych pacjentów w województwach jest duży.
- Błąd oszacowania udziału pacjentów, którzy przyszli tylko dzięki kampanii, wynosi 24,4 punktu procentowego po 4 tygodniach i 20,1 po 6, a najmniejszy wykrywalny efekt to 68 i 56 punktów. Test nie odróżni więc ani 100% od 85%, ani 85% od 70%. Gdy naprawdę każdy pacjent przyszedł tylko dzięki kampanii, orientacyjnie co czwarty test (23–27%) pokaże wynik poniżej progu. Dłuższy test wymaga osobnego przeliczenia, bo szum okresu odniesienia nie maleje z długością testu.
- Rozrzut jest prawie czysto losowy, więc sam dobór par prawdopodobnie nie wystarczy. Test może za to wykryć dużą różnicę, na przykład gdy większość pacjentów przyszłaby i bez kampanii. Pary i sposób liczenia ustalamy przed testem, na danych sprzed testu.
- To ocena orientacyjna: testy pozorne na danych ostatnich 12 miesięcy, przy założeniach modelu.

#### Reguła na wynik niejednoznaczny, ustalona z góry

- Decyduje sam wynik testu, nawet gdy przedział niepewności obejmuje próg: poniżej progu wyłączamy, powyżej zostawiamy.
- To świadoma reguła decyzji przy dużej niepewności. Statystycznie test tego nie rozstrzygnie, ale obie decyzje są odwracalne, a pomiar warto powtórzyć w innym sezonie.
- Inne warianty (bez zmian, gdy przedział obejmuje próg; połowa budżetu; przedłużanie testu z punktami kontrolnymi co 2 tygodnie; decyzja według oczekiwanej marży, która wymaga osobnego modelu) opisuje raport analiza/wyniki/d_wynik.txt, punkt 3e.

#### Projekt testu

- Na 4–6 tygodni wyłączyć kampanię w połowie województw, łącząc je w pary podobne wielkością i trendem i losując w parach. Udział nowych kampanii jest podobny we wszystkich województwach (26,2–31,5% nowych pacjentów ostatnich 12 miesięcy), co ułatwia dobór par.
- Wskaźnik główny: wszyscy nowi pacjenci i marża w województwie; pacjenci przypisani Meta są tylko pomocniczy.
- Budżetu z wyłączonych województw nie przesuwać.
- Przy okazji mierzyć poranne opóźnienia u internisty (pozycja 6).
- Ryzyko: obsada lekarzy jest wspólna dla całego kraju. Wyłączenie zmniejsza obciążenie internistów, więc w województwach kontrolnych może przybyć wolnych terminów, zakupów i powrotów. Zawyża to spadek (więcej pacjentów wygląda na takich, którzy przyszli tylko dzięki kampanii), a efekt w retencji przenosi się na województwa kontrolne. Do tego województwo konta nie musi być miejscem wyświetlenia reklamy, więc część reklam przecieka między województwami.
- Koszt testu, jeśli każdy pacjent przyszedł tylko dzięki kampanii (według pierwszego wejścia): najwyżej około 1,1–1,2 tys. zł utraconej marży przy 4 tygodniach i 1,6–1,8 tys. zł przy 6 tygodniach; po zmianie zasad zwrotów 2,5 i 3,8 tys. zł (tempo III kwartału 2026). Według sesji z płatnością test daje zysk. Uzupełnienie: badanie przyrostu konwersji w panelu Meta.

Skąd liczby: analiza/wyniki/c_priorytety.txt (P4, P11), analiza/wyniki/a5e_scenariusze.txt (E1, E3, E3b), analiza/wyniki/d_wynik.txt (3a–3e), analiza/wyniki/d_kampanie.txt (3), analiza/wyniki/d_retencja.txt (5), notatki/a5_ekonomia.md.

Wróć do przeglądu

### 10. Zmienić cennik specjalistów i warunki TelemediGO u specjalistów

Wizyta u specjalisty zostawia ponad koszt lekarza tylko 9–19 zł, a ze zniżką TelemediGO przynosi stratę.

*Ile warte rocznie (marża): 15–31 tys. zł — rocznie za warunki TelemediGO po pełnym roku; cennik do 74 tys. zł za każde 10 zł podwyżki, górna granica · Pewność: Średnia — kierunek jest pewny; nie wiemy, ile da zmiana cennika · Wdrożenie: 1–2 tygodnie + test dwóch cen 4 tygodnie*

**Co robimy:**
- Ustawić zniżkę TelemediGO u specjalistów tak, żeby cena nie spadała poniżej kosztu lekarza: najwyżej około 8% przy cenie 109 zł.
- U pediatry i psychologa samo wyłączenie zniżki nie wystarczy, bo już cena katalogowa (95 i 99 zł) jest niższa niż koszt lekarza (100 zł, przy założeniu opartym na zadaniu). Tu trzeba podnieść cenę.
- Przetestować dwie ceny dla nowych pacjentów przez 4 tygodnie i mierzyć marżę na sesję, nie sam odsetek kupujących.

**Po czym poznamy:**
Marża wizyt u specjalistów (z członkami i bez) jest nieujemna, a sprzedaż TelemediGO nie spada bardziej niż ustalony z góry próg.

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

Zobacz w danych: Kohorty: powrót i marża według pierwszej usługi; Kohorty: kupujący TelemediGO przy pierwszym zakupie *(odnośniki)*

Czego nie wiemy: punkt 16 *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Z danych

- Po cenie katalogowej wizyta zostawia ponad koszt lekarza tylko 9 zł (dermatolog, kardiolog, neurolog, urolog: 109 zł) albo 19 zł (endokrynolog, ginekolog: 119 zł).
- Pediatra (95 zł) i psycholog (99 zł) mają cenę niższą niż koszt lekarza 100 zł (przy przyjętym koszcie pediatry jak u specjalisty).
- Po zniżce TelemediGO 20% cena jest niższa niż koszt lekarza u wszystkich specjalistów poza psychiatrą. W ostatnich 12 miesiącach te wizyty przyniosły 14,7 tys. zł straty na 1 512 zamówieniach.
- To wspólna przyczyna strat w TelemediGO u specjalistów i w kampanii na specjalistów (pozycja 4).
- Stawka lekarza 100 zł za wizytę u pediatry to założenie oparte na zadaniu: 25 zł internista, 200 zł psychiatra, 100 zł każdy inny specjalista. Sprawdzenie wrażliwości: przy stawce 25 zł, jak u internisty, marża na pacjenta w 90 dniach rośnie o 3,7–4,8 zł.

#### Ile warta

- Warunki TelemediGO: scenariusze 14,7 / 18,9 / 31,4 tys. zł rocznie (znikają wszystkie te wizyty / tylko te ze stratą / wszystkie zostają po cenie katalogowej). 31,4 tys. zł to scenariusz. Przy osobnej reakcji przy każdym zamówieniu wynik mieści się między 10,9 a 35,2 tys. zł. Wszystkie pomijają zmianę sprzedaży członkostw.
- Założenie planistyczne (bez osobnego rachunku): w pierwszym roku efekt to około połowa, bo obecni członkowie mają stare warunki do końca ważności.
- Cennik: każde 10 zł podwyżki przy tej samej liczbie wizyt to do 73,6 tys. zł rocznie (7 363 opłacone wizyty w ostatnich 12 miesiącach), a przy utrzymaniu zniżki TelemediGO 20% na 1 425 z nich 70,8 tys. zł. To górna granica, bo nie znamy reakcji pacjentów na cenę.

Skąd liczby: analiza/wyniki/c_telemedigo.txt (3a–3c), analiza/wyniki/c_priorytety.txt (P6, P14), notatki/ZALOZENIA.md (punkt 33).

Wróć do przeglądu

### 11. Sprawdzić, gdzie znika ruch między kliknięciem reklamy a wejściem na stronę w Meta i TikToku

Na kliknięcie w Meta przypada 0,8 sesji, a w Google Ads 0,9; nie wiemy, czy ludzie porzucają ładowanie strony, czy panel liczy kliknięcia inaczej.

*Ile warte rocznie (marża): 0 albo do 52 tys. zł — rocznie, górna granica; po wstrzymaniu TikToka mniej · Pewność: Niska — nie wiemy, czy brakujące sesje da się odzyskać · Wdrożenie: 1–2 dni*

**Co robimy:**
Porównać w panelach Meta i TikToka kliknięcia w link i wyświetlenia strony docelowej z sesjami w analityce, dzień po dniu, i zmierzyć czas ładowania strony w przeglądarkach w aplikacjach.

**Po czym poznamy:**
Wiemy, czy brakujące sesje to ludzie, którzy porzucają ładowanie strony (do odzyskania), czy inny sposób liczenia kliknięć w panelu (wtedy pozycja jest warta 0 zł). Wynik zmienia ocenę pozycji 3 i 9.

Zobacz w danych: Lejek: sesje kampanii Meta i TikToka dzień po dniu *(odnośniki)*

Czego nie wiemy: punkt 12 *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Z danych

- Na kliknięcie przypada 0,92–0,93 sesji w Google Ads, 0,79–0,82 w Meta i 0,72 w TikToku, stale w każdym kwartale.

#### Ile warta

- 0 zł, jeśli plik wydatków liczy wszystkie kliknięcia (także te, które nie prowadzą na stronę).
- Jeśli ludzie porzucają stronę, zanim się załaduje, i da się to odzyskać: do 52 tys. zł rocznie (górna granica: 23 776 brakujących sesji i do 1 434 zamówień w ostatnich 12 miesiącach). Po wstrzymaniu TikToka mniej. Realnie raczej ułamek, bo porzucający są mniej zdecydowani.

Skąd liczby: analiza/wyniki/a2_jakosc.txt (3c), analiza/wyniki/c_priorytety.txt (P9), analiza/wyniki/a5p_lejek.txt (6b), notatki/a5_pozyskanie.md (sekcja 5).

Wróć do przeglądu

### 12. Sprawdzić losowym testem, ile wizyt i powrotów dokłada zniżka TelemediGO

Kupujący TelemediGO wracają częściej, ale nie wiemy, czy to skutek zniżki, czy tego, że kupują ci, którzy i tak planują wracać.

*Ile warte rocznie (marża): koszt 3–12 tys. zł — zniżki przy niezmienionej liczbie wizyt · Pewność: Test · Wdrożenie: 2–8 tygodni + 90 dni*

**Co pokaże:**
Test pokaże wpływ samej zniżki na wizyty, powroty i marżę. Nie pokaże, czy opłaca się oferta za 89 zł, bo uczestnicy dostają zniżki bez opłaty. Od wyniku zależy, czy program promować, czy przebudować razem z pozycją 10.

**Po czym poznamy:**
Różnica powrotu w 90 dniach i marży między grupą z dostępem a grupą bez niego.

Zobacz w danych: Kohorty: kupujący TelemediGO przy pierwszym zakupie i pozostali *(odnośniki)*

Czego nie wiemy: punkt 8 *(odnośniki)*

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

#### Z danych

- Nie wiemy, czy TelemediGO podnosi powroty, czy tylko przyciąga pacjentów, którzy i tak wracają. Kupujący przy pierwszym zamówieniu wracają w 90 dniach w 34,7% wobec 20,0% podobnych pacjentów (ostatnie 12 miesięcy, 858 kupujących), ale ta różnica łączy wpływ zniżki i to, kto kupuje.
- Zniżki przewyższają opłatę średnio o 15,6 zł na członkostwo (członkostwa sprzed roku, przy założeniu, że te same wizyty odbyłyby się i bez TelemediGO), więc program opłaca się tylko wtedy, gdy dokłada wizyt.

#### Ile warta

- Pokaże, czy zniżka dokłada wizyt, a od tego zależy, czy program promować (sprzedaż, przypomnienie o odnowieniu; dziś odnawia około 5% członków: 62 z 1 140 w 90 dniach po wygaśnięciu), czy przebudować razem z pozycją 10.
- Koszt testu (3,3–12,2 tys. zł zniżek dla 487–1 823 pacjentów w grupie z dostępem) liczymy przy niezmienionej liczbie wizyt; jeśli zniżka doda wizyt, koszt będzie wyższy.

#### Zastrzeżenie

- Darmowy dostęp mierzy wpływ zniżki, a nie opłacalność oferty za 89 zł. Losowanie samej oferty przy kasie mierzyłoby decyzję biznesową, ale przy 4,5% kupujących potrzebuje ponad 4 lat pozyskania. Wskaźnikiem głównym jest marża na pacjenta.

#### Wdrożenie

- 2–8 tygodni na losowe przydzielenie (487–1 823 pacjentów na grupę, czyli do około 1,8 miesiąca pozyskania), potem 90 dni obserwacji.
- Liczebność wyznaczyliśmy dla różnicy powrotu; przed startem trzeba ustalić najmniejszą istotną biznesowo zmianę marży i sprawdzić, jakiej próby wymaga.

Skąd liczby: analiza/wyniki/c_telemedigo.txt (1d, 2a, 4a, 4d), analiza/wyniki/c_priorytety.txt (P10).

Wróć do przeglądu

### Nie robimy teraz rzeczy bez podstaw w danych albo bez testu

- Kampanii o zgodę marketingową pacjentów nowych kampanii: w najlepszym razie 1,9 tys. zł rocznie.
- Osobnej naprawy przeglądarek w aplikacjach w reklamach do nowych osób: w tej samej kampanii płacą tak samo jak zwykłe.
- Mocniejszej sprzedaży i odnowień TelemediGO: dopiero po teście z pozycji 12.
- Przesuwania uwolnionego budżetu do innych kampanii bez testu.

**Szczegóły** *(sekcja rozwijana, tu rozwinięta)*

- Zgoda marketingowa pacjentów nowych kampanii: w najlepszym odczytaniu 1,9 tys. zł rocznie.
- Przeglądarki wbudowane w aplikacje w kampaniach do nowych odbiorców: w tym rachunku 0 zł, bo w tej samej kampanii nie wykryliśmy niższej konwersji niż w zwykłych (także w kampanii Meta „lekarz online”: różnica −0,15 punktu procentowego, od −0,51 do +0,21, 29 330 sesji w przeglądarkach wbudowanych w dwóch latach). Porównanie jest obserwacyjne, więc nie rozdziela wpływu przeglądarki od cech użytkowników i nie uzasadnia osobnej wyceny naprawy. Nie uogólniamy tego na resztę ruchu. W remarketingu, kampanii na markę i wejściach bezpośrednich sesje w przeglądarkach w aplikacjach płacą w ostatnich 12 miesiącach rzadziej niż zwykłe w tej samej kampanii (remarketing Meta o 12,2 punktu, 1 772 sesje w przeglądarkach wbudowanych; Google Ads na markę o 5,1 punktu, 2 357 sesji; wejścia bezpośrednie o 4,4 punktu, 4 261 sesji). Dane nie rozstrzygają, czy winna jest przeglądarka, czy to, kto z niej korzysta (niewiadoma 18).
- Mocniejsza sprzedaż i odnowienia TelemediGO: dopiero po teście z pozycji 12.
- Przesuwanie uwolnionego budżetu do innych kampanii bez testu (zasada budżetu).

*Notatka: notatki/c_szkic.md, sekcja 3. Liczby: analiza/c_priorytety.py → analiza/wyniki/c_priorytety.txt, analiza/c_telemedigo.py → analiza/wyniki/c_telemedigo.txt i raporty wskazane przy każdej pozycji. Kolejność i wyceny sprawdziła niezależnie runda kilku modeli AI różnych firm (notatki/konsylium/c_priorytety/synteza.md), a liczby drugi model (notatki/recenzje/c_codex.md).*

Dalej: Czego nie wiemy

# Zakładka 9: Czego nie wiemy (`#niewiadome`)

## Czego z tych danych nie wiemy

Rzeczy, których te dane nie rozstrzygają, i test albo dane, które je domkną. Numer pozycji listy priorytetów prowadzi do karty, której kwota od tego zależy.

*Filtry (ustawienia domyślne):*
- Pozycja listy priorytetów: wszystkie (21) (do wyboru: wszystkie (21) / 1. Naprawić zakładanie konta w Safari na iPhone'ach (2) / 2. Oczyścić codzienny raport i dodać alarmy na lejku i zwrotach (2) / 5. Zmienić obietnicę w reklamach Meta na L4; zasady zwrotów rozważyć osobno (3) / 6. Zdiagnozować poranne opóźnienia internistów, potem przetestować obsadę (1) / 7. Wprowadzić komunikację po wizycie, zawsze z losową grupą bez wysyłki (1) / … (razem 12 opcji))

| Nr | Czego nie wiemy | Dlaczego to ważne | Test albo brakujące dane | Pozycja listy priorytetów |
| --- | --- | --- | --- | --- |
| 1 | Ilu pacjentów nowych kampanii na L4 przyszłoby i bez nich | od tego zależy decyzja o kampanii Meta na L4: jej wyłączenie jest warte od około −31 do +180 tys. zł rocznie, a próg decyzji to około 85% pacjentów, którzy bez kampanii by nie przyszli (pozycja 9) | wyłączenie kampanii w losowej połowie województw na 4–6 tygodni; badanie przyrostu w panelach Meta i TikToka. Taki test nie odróżni wyniku od progu (błąd 20–24 punktów procentowych), więc rozpozna tylko sytuację, w której większość pacjentów przyszłaby i bez kampanii, a przy wyniku niejednoznacznym decyduje reguła ustalona z góry (pozycja 9) | 9. Sprawdzić testem w części kraju, czy kampania Meta na L4 się opłaca |
| 2 | Ilu pacjentów kampanii bez kodu rabatowego (Google Ads ogólne, Meta „lekarz online”) przyszłoby i bez reklamy | znak wyniku tych kampanii zależy od reguły przypisania, a żadna reguła nie mówi, ilu pacjentów kampania naprawdę dokłada | ten sam test z grupą bez reklamy; mierzy przyrost pacjentów niezależnie od reguły przypisania, więc nie trzeba wybierać reguły | — |
| 3 | Powód zwrotów po wizycie L4 w nowych kampaniach (17,4% wobec 5,3%) | po wstrzymaniu TikToka dotyczy tylko Meta: od niego zależy, ile da nowa kreacja (11–18 tys. zł rocznie) i czy potrzebna jest zmiana zasad zwrotów (27–46 tys. zł rocznie; pozycja 5) | powód zwrotu, decyzja lekarza (czy L4 wystawiono), treść reklam | 5. Zmienić obietnicę w reklamach Meta na L4; zasady zwrotów rozważyć osobno |
| 4 | Skąd poranne opóźnienia u internistów (blok od 5:00 do 13:59, już przy wizytach z najwcześniejszym terminem dnia, bez widocznego narastania w ciągu poranka) i czy obniżają powroty | scenariusz od 0 do 65 tys. zł rocznie. Luty 2026 nie pasuje do hipotezy, że większe opóźnienia zawsze obniżają powrót: opóźnienia były już wtedy wysokie, a powrót pacjentów kampanii działających w obu latach nie spadł | grafiki i obsada poranna przed i po 3.11.2025, obciążenie lekarzy pacjentami spoza B2C, koszt obsady; test z dodatkową poranną obsadą w losowe dni | 6. Zdiagnozować poranne opóźnienia internistów, potem przetestować obsadę |
| 5 | Sesje zalogowane od wejścia: wizyty „sprawdzam konto” czy zepsuta ścieżka | 0 albo około 36–40 tys. zł rocznie (wysoki scenariusz 89 tys. zł) | ręczny test zakupu po zalogowaniu; logi błędów; znacznik „zalogowany na wejściu” w analityce | 8. Sprawdzić ręcznie zakup dla pacjentów zalogowanych od wejścia |
| 6 | Przyczyna awarii zakładania konta w Safari na iOS od 17.03.2026 | potrzebna do naprawy (pozycja 1) | lista zmian w produkcie z 16–17.03.2026, logi rejestracji według przeglądarki, powtórzenie na iPhonie | 1. Naprawić zakładanie konta w Safari na iPhone'ach |
| 7 | Czy utraceni w Safari na iOS kupili na innym urządzeniu | zmienia wartość pozycji 1 | powiązanie urządzeń po adresie e-mail albo numerze telefonu przy próbie rejestracji | 1. Naprawić zakładanie konta w Safari na iPhone'ach |
| 8 | Ile wizyt i powrotów dokłada zniżka TelemediGO | od tego zależy, czy program promować; test pokaże wpływ samej zniżki, ale nie opłacalność oferty za 89 zł | losowy, bezpłatny dostęp do zniżek (pozycja 12) | 12. Sprawdzić losowym testem, ile wizyt i powrotów dokłada zniżka TelemediGO |
| 9 | Czy newsletter i SMS wywołują zakup | to kanał, którego dodatkowy wpływ warto przetestować (około 14% obserwowanych pierwszych powrotów idzie po wejściu z niego); widać kliknięcia, nie wysyłki; wejść na 1 000 pacjentów całej narastającej bazy jest coraz mniej (z 56–108 do 24–52 miesięcznie) | liczba wysyłek; losowa grupa kontrolna bez wysyłki | 7. Wprowadzić komunikację po wizycie, zawsze z losową grupą bez wysyłki |
| 10 | Wartość remarketingu porzuconego koszyka | podział według pierwszego wejścia z definicji przypisuje mu mało pacjentów | grupa kontrolna, której remarketing się nie wyświetla | — |
| 11 | Ile wzrostu daje pora roku, a ile wyższe wydatki na kampanie | od X 2024 do I 2025 rosną naraz pora roku i wydatki. W dwóch latach danych każdy miesiąc występuje tylko dwa razy, a wydatki rosły w obu latach, więc wpływu sezonu nie da się oddzielić od wpływu wydatków | zmiana budżetu w części kraju (grupa kontrolna według województw) | — |
| 12 | Strata między kliknięciem reklamy a sesją w Meta i TikToku | od 0 do 52 tys. zł rocznie | panele reklamowe, logi serwera, czas ładowania strony w przeglądarkach wbudowanych | 11. Sprawdzić, gdzie znika ruch między kliknięciem reklamy a wejściem na stronę w Meta i TikToku |
| 13 | Koszt lekarza za wizyty testowe (51 775 zł według zasady z zadania, łącznie w dwóch latach; 37 950 zł w ostatnich 12 miesiącach) | wynik biznesu | informacja z rozliczeń, czy lekarze dostali wynagrodzenie za testy | 2. Oczyścić codzienny raport i dodać alarmy na lejku i zwrotach |
| 14 | Warunki umowy z rankingiem lekarzy | prowizja 30,8 tys. zł za dwa lata według pierwszego wejścia albo 14,9 tys. zł według kodu | umowa z rankingiem | — |
| 15 | Pełna długoterminowa marża rocznika ostatnich 12 miesięcy | rachunek kampanii w 90 i 180 dniach jej nie obejmuje; zaniża wartość kampanii z powracającymi pacjentami | czas; najstarsze kohorty pozwalają już częściowo ją ocenić (5 137 pacjentów ostatnich 12 miesięcy ma pełne 270 dni obserwacji) | — |
| 16 | Reakcja pacjentów na cenę u specjalistów | od niej zależy, ile da zmiana cennika (do 73,6 tys. zł za 10 zł podwyżki) | test dwóch cen dla nowych pacjentów przez 4 tygodnie | 10. Zmienić cennik specjalistów i warunki TelemediGO u specjalistów |
| 17 | Zasady zwrotów przy odmowie L4 i ryzyko prawne reklam L4 | zmiana zasad zwrotów z pozycji 5 to osobna decyzja, która wymaga zmiany regulaminu i oceny ryzyka prawnego | regulamin, opinia prawna, treść reklam | 5. Zmienić obietnicę w reklamach Meta na L4; zasady zwrotów rozważyć osobno |
| 18 | Czy sesje w przeglądarkach w aplikacjach płacą rzadziej w remarketingu Meta, kampanii Google Ads na markę i wejściach bezpośrednich przez samą przeglądarkę, czy przez to, kto z niej korzysta | w remarketingu Meta, Google Ads na markę i wejściach bezpośrednich płacą w ostatnich 12 miesiącach rzadziej niż zwykłe o 4,4–12,2 punktu procentowego; jeśli winna jest przeglądarka, da się to naprawić na stronie | czas ładowania i błędy strony w przeglądarkach w aplikacjach; ręczny zakup w Instagramie, Facebooku i TikToku; test linku, który otwiera zwykłą przeglądarkę | — |
| 19 | Dlaczego 11 482 konta (21,9% z 52 400 kont z dwóch lat) nie mają żadnego zakupu i czy da się je odzyskać | każde z tych kont wybrało usługę i przeszło krok konta, a 37,1% z nich zaczęło płatność; 58,1% z 11 482 ma zgodę marketingową (stan na 30.09.2026), ale w danych nie ma ani jednego ich wejścia z newslettera albo SMS-a | dane o wysyłkach do tych kont; sekwencja wiadomości do kont bez zakupu z losową grupą kontrolną; bez wyceny przed testem | — |
| 20 | Jak liczba zamówień z Meta na L4 reaguje na wysokość kodu rabatowego (dziś 20 zł) | kod to 62,8 tys. zł zniżki efektywnej na pełny rok; próg rachunku: rezygnacja z niego opłaca się, jeśli ubędzie mniej niż 33,7% zamówień z kodem (przy przejściu na START10 mniej niż 20,2%) | losowy podział ruchu Meta na L4 na kod 20 zł, 10 zł i brak kodu, mierzony marżą na kliknięcie (pozycja 5) | 5. Zmienić obietnicę w reklamach Meta na L4; zasady zwrotów rozważyć osobno |
| 21 | Dlaczego od 22.05.2026 spada konwersja Google Ads na markę | sesja do płatności u osób, które jeszcze nie kupowały: 17,8% (5 152 sesje, 22.05–30.09.2026) wobec 21,2% (21 186 sesji, 1.10.2024–21.05.2026), czyli około 28,5–39,6 zamówienia mniej na 30 dni zależnie od okna porównania; to nie Safari na iOS ani zmiana struktury ruchu; rok wcześniej w tym samym sezonie spadek był mniejszy i nieistotny (−1,3 punktu); koszt kliknięcia marki rośnie (pozycja 2) | lista zmian w kampanii i na stronie z maja 2026; hasła wyszukiwania i reklamy konkurencji na markę w panelu Google Ads | 2. Oczyścić codzienny raport i dodać alarmy na lejku i zwrotach |

*Notatka: notatki/c_szkic.md, sekcja 4. Liczby: analiza/wyniki/c_priorytety.txt (P4, P5, P8, P9, P11, P14), analiza/wyniki/a5r_po_zakupie.txt (2b, 5e), analiza/wyniki/a5r_kohorty.txt (7), analiza/wyniki/a2_jakosc.txt (2e), analiza/wyniki/a5e_ekonomia.txt, analiza/wyniki/d_kampanie.txt (1, 5, 6), analiza/wyniki/d_retencja.txt, analiza/wyniki/d_wynik.txt (3c).*

Wróć do początku: Czy to wzrost

---

**Stopka strony:** Dane od 1.10.2024 do 30.09.2026. Liczby przeliczone 2026-10-22 22:16 skryptami analiza/b_eksport.py i analiza/b2_eksport_c.py (stan repozytorium 329d075). Strona nie pobiera niczego z internetu.
