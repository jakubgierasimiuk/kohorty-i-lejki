# F — propozycja jednej rundy poprawek przed publikacją (do decyzji Kuby, 2026-10-23)

Podstawa: recenzje Astry i Fable (`notatki/recenzje/f_*`), kontrola języka (`notatki/f_jezyk.md`), synteza w `notatki/f_kontrola.md`, punkt 4. Wynik kontroli technicznej (`notatki/f_techniczna.md`) jest w punkcie 6.

**Ramy Kuby:** poprawiamy tylko braki wobec zadania i to, co zmienia ocenę rozwiązania; bez nowych analiz, raczej lepiej pokazać to, co już mamy; jedna runda poprawek, potem publikacja. Do decyzji Kuby nic się nie zmienia.

**Decyzja Kuby (2026-10-23):** „tak, wszystko według rekomendacji, ruszaj z dwiema sesjami”. Zdarzenie 8 (remarketing Meta) zostaje tylko na osi. Wykonanie: sesja A `local_e5cfeeb6` (strona), sesja B `local_4102aedd` (ślad pracy). Zapis: `DECYZJE.md`, ostatni wpis.

## Puenta

Proponujemy pięć poprawek. Dwie największe odpowiadają na to, co obaj recenzenci wskazali niezależnie:
1. tabela „co zmieniło kohorty i wynik” jako pierwsza karta zakładki „Kohorty”, złożona wyłącznie z liczb, które już są na stronie;
2. ślad pracy: sekcja w README z konkretnymi ślepymi uliczkami i poprawkami oraz folder `rozmowy/` z oczyszczonym zapisem rozmów.

Trzy mniejsze to zdania na pierwszej zakładce, pozostałe poprawki z kontroli języka i wykres Safari na równych oknach czasu. Do tego trzy drobne poprawki techniczne z kontroli technicznej (punkt 6). Razem około 10–12 godzin pracy. W dwóch sesjach naraz to około 6 godzin, plus 30–45 minut Kuby na przejrzenie zapisu rozmów. Żadna liczba w odpowiedzi się nie zmienia.

## Poprawka 1. Jedno miejsce: które zdarzenie albo która decyzja zmieniła kohorty i wynik

**Co zmieniamy i gdzie.** Nowa pierwsza karta zakładki „Kohorty”: tabela, w której wiersz to jedno zdarzenie albo jedna decyzja firmy z osi zdarzeń. Kolumny: kiedy; co się stało (decyzja czy zdarzenie); których pacjentów dotyczy; co zmieniło się w ich zachowaniu (przed → po, z liczebnością i okresem); skutek w złotych albo „nie policzono”; pewność; co z tym robimy (pozycja listy priorytetów albo punkt „Czego nie wiemy”). Obecna pierwsza karta „Kohort” (roczny spadek powrotu, powtórzony z „Czy to wzrost”) schodzi pod dzienny wykres kohort. W „Zdarzeniach” i w „Czy to wzrost” dochodzi jedna linijka z odnośnikiem do tabeli.

**Wiersze (liczby z obecnej strony; w tabeli wezmą je pola eksportu, nie ręczne przepisanie):**

| Kiedy | Co | Zachowanie przed → po | Skutek w złotych | Co robimy |
|---|---|---|---|---|
| 8.09.2025 | decyzja: newsletter sprzedaje samo TelemediGO | 225 członkostw w pierwszych 23 dniach wobec około 29 przy późniejszym tempie | jednorazowo 17,4 tys. zł w III kw. 2025; przez to III kw. 2026 wygląda na −7% marży, a po odjęciu tej nadwyżki na +1% | kontekst porównania kwartałów |
| 3.11.2025, ruch rośnie skokami od 17.11.2025 | decyzja: kampania Meta na L4 | udział nowych kampanii w nowych pacjentach 0% → 41%; ci pacjenci wracają w 90 dniach w 4% wobec 22% pozostałych; marża nowego pacjenta w 30 dniach 56,0 → 46,8 zł | decyzja o wyłączeniu warta od −31 do +180 tys. zł rocznie, dlatego test | pozycje 5 i 9 |
| 13.11.2025 | zdarzenie: więcej zwrotów po odbytej wizycie | 2,1% → 6,9% pierwszych zamówień | 84 tys. zł zwrotów i 34 tys. zł kosztu lekarza w 12 miesiącach (pacjenci nowych kampanii) | pozycja 5 |
| 24.11.2025 | zdarzenie: poranne opóźnienia u internistów | 6,3% → 50,2% porannych wizyt ponad 15 minut po terminie | 0–65 tys. zł rocznie, scenariusz | pozycja 6 |
| 9.02.2026, ruch rośnie skokami do 6.04.2026 | decyzja: kampania TikTok na L4 | powrót nowych pacjentów w 30 dniach 9,7% → 6,9% od 10.02.2026 | traci na każdym pacjencie według obu reguł przypisania; pauza +19 do +48 tys. zł rocznie | pozycja 3 |
| 2.03.2026 | zmiana bez znanej przyczyny: powrót w kampaniach działających w obu latach | 23,3% → 20,9% w 90 dniach (poniżej progu metody) | nie policzono | „Czego nie wiemy” |
| 17.03.2026 | awaria: zakładanie konta w Safari na iPhone'ach | krok konta 66% → 45% w 60 dniach przed i po; inne przeglądarki 65% → 63% | 628–695 utraconych pierwszych zamówień; 75–83 tys. zł marży rocznie | pozycja 1 |
| 22.05.2026 | zmiana bez znanej przyczyny: Google Ads na markę | płatność na sesję 21,2% → 17,8% | 28,5–39,6 zamówienia na 30 dni | „Czego nie wiemy” |

Dwa zdarzenia jakości danych (1 i 14) zostają tylko na osi. Zdarzenia 3 i 10 (zmiany wyniku kohort) nie są osobnymi wierszami, tylko skutkiem w wierszach kampanii. Zdarzenie 8 (remarketing Meta) do decyzji: dziewiąty wiersz albo tylko oś.

**Jak to zobaczy ktoś z Telemedi.** Otwiera „Kohorty” i pierwsza rzecz to odpowiedź na najważniejsze pytanie zadania: daty, zdarzenia i decyzje, co po każdym zmieniło się w kohortach i ile to jest warte. Przy każdym wierszu dwa odnośniki: „Pokaż na kohortach dziennych” (ustawia porównanie „60 dni przed i po” tym zdarzeniem i przewija do dziennego wykresu kohort z liniami zdarzeń) i „Opis zdarzenia” (karta na osi). Tytuł karty to wniosek; przykład do sprawdzenia z liczbami: „Kohorty zmieniły się głównie po naszych decyzjach o kampaniach na L4; wynik dodatkowo obniżyła awaria Safari”. Jedno zastrzeżenie: zdarzenia z tych samych miesięcy nakładają się, więc tabela pokazuje, co zmieniło się po zdarzeniu, a nie dowodzi przyczyny. Na telefonie każdy wiersz jako mała karta.

**Skąd liczby i jak je sprawdzimy.** Każda liczba już jest na stronie (karty osi zdarzeń, priorytety, ekonomia kampanii); tabela bierze je z tych samych pól eksportu. Kontrola: (1) nowa sekcja w szkicu `notatki/e_teksty_zakladki.md`, więc kontrola eksportu obejmie każdą liczbę tabeli; (2) skrypt porównujący liczby na wyrenderowanej stronie (z części 2) porówna każdą komórkę tabeli z tą samą liczbą w karcie zdarzenia albo priorytetu; (3) w przeglądarce każdy odnośnik wiersza otwiera właściwe porównanie, także po odświeżeniu strony. Nowych obliczeń nie ma, więc Codex nie musi niczego przeliczać; przejrzy tylko, czy tytuł i zastrzeżenie nie mówią więcej niż dane.

**Ile.** 3–4 godziny.

**Co może pójść źle.**
- Tabela przeczytana jako dowód przyczyny. Zabezpieczenie: nagłówki „co zmieniło się po”, kolumna pewności, jedno zastrzeżenie.
- Różne miary w różnych wierszach (powrót, marża, krok lejka). Zabezpieczenie: w każdej komórce nazwa miary i okres; jednolite porównanie kohort jest pod odnośnikiem „60 dni przed i po”.
- Więcej tekstu, choć obaj recenzenci radzą go nie dodawać. Zabezpieczenie: tabela zastępuje na górze powtórzoną kartę, a nie dochodzi do niej.
- Szeroka tabela na telefonie. Zabezpieczenie: układ kart przy 375 px, sprawdzony zrzutami.

**Warianty.**
- Miejsce: (a) pierwsza karta „Kohort” — **rekomendacja**, bo zadanie wiąże to pytanie z analizą kohortową i tam osoba oceniająca zajrzy zaraz po „Czy to wzrost”; (b) góra „Zdarzeń” (propozycja Fable) — naturalne miejsce przy osi, ale dalej od kohort; (c) skrót na pierwszej zakładce — odradzamy, bo jest już gęsta.
- Liczby: (i) tylko liczby już policzone, różne miary dla różnych zdarzeń, jednolite porównanie pod odnośnikiem — **rekomendacja**; (ii) jedna miara dla każdego zdarzenia (np. powrót i marża w 30 dniach, 60 dni przed i po) liczona w eksporcie — czytelniejsza, ale to nowe obliczenia: około 3–4 godzin więcej, druga ścieżka liczenia obok tej w przeglądarce i przeliczenie przez Codeksa; kłóci się z „bez nowych analiz”.

## Poprawka 2. Ślad pracy: prompty, ślepe uliczki, poprawki

**Co zmieniamy i gdzie.**

(a) **README:** zamiast zdania „Ślepe uliczki zostały w historii commitów” sekcja „Jak pracowaliśmy z AI: prompty, ślepe uliczki, poprawki”:
- gdzie są prompty: polecenia Kuby słowo w słowo (`rozmowy/`, a także `notatki/e_runda.md`, `notatki/d_poprawki.md` i cytaty w `DECYZJE.md`), zasady pracy z AI (`CLAUDE.md`), polecenia i odpowiedzi drugiego modelu (`notatki/recenzje/`), briefy i odpowiedzi konsylium (`notatki/konsylium/`);
- 8–10 konkretnych historii, każda w 2–3 zdaniach: co myśleliśmy, co pokazało, że to błąd, co zmieniliśmy, odnośnik do commita i notatki.

Kandydaci na historie (każdą sprawdzimy w notatkach i commitach przed wpisaniem):
1. odtworzenie dashboardu: które definicje dają dokładnie +52%, +61%, +50% i +40% (A3);
2. „luka” wycofana z „Czy to wzrost” i z „Wyniku biznesu”, bo zdanie nie miało rachunku (`849e12c`, `825c977`);
3. Safari: najpierw wyglądało na zmianę struktury ruchu, potem okazało się awarią jednej przeglądarki; lejek przeliczony według pierwszego wejścia (`351f556`);
4. Codex: 34 z 35 liczb zgodnych, jeden błąd jednostki (`1bfa75f`);
5. reguła testu Mety: uzasadnienie „oczekiwaną marżą” wycofane po recenzji Codeksa (`DECYZJE.md`);
6. spadek marży w III kwartale 2026 okazał się skutkiem jednorazowego startu newslettera rok wcześniej (wątpliwość Kuby, policzona);
7. zasada „najpierw napraw, potem wyłączaj” (19.10) a końcowe „wstrzymać”: dlaczego pauzy, które da się cofnąć w jeden dzień, i gdzie jest wariant „naprawić” (Astra zwróciła uwagę na tę zmianę stanowiska);
8. zamówienia testowe przejrzane dwa razy, reguła bez zmian (A2, D);
9. błąd w kodzie wyłapany po drodze, jeśli jest opisany w repozytorium (inaczej pomijamy);
10. ta kontrola: zewnętrzna recenzja wyłapała wadliwy zrzut ekranu i nieaktualny plik z tekstami strony.

(b) **Folder `rozmowy/`** z oczyszczonym zapisem rozmów z Claude Code.
- **Źródło:** 19 sesji tego projektu zapisanych lokalnie przez Claude Code (około 160 MB; z rozmowami agentów pomocniczych 219 MB).
- **Bierzemy wyłącznie (lista dozwolona, nic poza nią):** wiadomości Kuby słowo w słowo (178 wiadomości po stronie użytkownika, około 290 tys. znaków, w tym automatyczne powiadomienia do odfiltrowania), tekstowe odpowiedzi Claude (794, około 354 tys. znaków) i polecenia, które Claude wysłał innym sesjom i agentom.
- **Nie bierzemy:** niczego, co aplikacja dokleja do rozmowy (globalne instrukcje Kuby z odwołaniami do innych projektów, pamięć, lista podłączonych usług i umiejętności, informacje o środowisku), wywołań narzędzi i ich wyników (treść plików, wydruki danych), wewnętrznych rozmów agentów. Skan pokazał, że nazwy innych projektów są właśnie tam: w 79 blokach doklejanych przez aplikację i w 27 wynikach narzędzi, a nie w samej rozmowie.
- **Usuwamy:** link do strony z zadaniem i do paczki danych (zadanie nie trafia do repozytorium), adresy e-mail (są w 10 wiadomościach), 2 ścieżki spoza folderu projektu, 1 wzmiankę o innym projekcie i wszystko, co wyłapie skan.
- **Format:** jeden plik Markdown na sesję, chronologicznie, przy każdej wiadomości data, godzina i autor („Kuba”, „Claude”); `rozmowy/README.md` mówi, co jest w środku, co usunęliśmy i dlaczego, i prowadzi do miejsc z historiami z README.
- **Kontrola, zanim cokolwiek trafi do repozytorium:** (1) skrypt przepuszcza tylko tekst z listy dozwolonej; (2) drugi skrypt skanuje wynik: nazwy innych projektów i usług, adresy e-mail i stron, ścieżki spoza projektu, wzorce kluczy i haseł; każde trafienie idzie do raportu; (3) Kuba przegląda raport i wyrywkowo pliki; (4) commit dopiero po jego „tak”. Opcjonalnie Codex (Sol) czyta oczyszczone pliki wyłącznie pod kątem treści spoza projektu. Repozytorium po rekrutacji wraca do prywatnych (decyzja z 19.10).

**Jak to zobaczy ktoś z Telemedi.** W README krótka sekcja z 8–10 historiami i odnośnikami. Kto chce więcej, otwiera `rozmowy/` i czyta, jak zmieniały się polecenia, gdzie AI się myliło i jak to poprawialiśmy.

**Ile.** README 1,5 godziny; zapis rozmów 2–3 godziny; przegląd Kuby 30–45 minut.

**Co może pójść źle.**
- Wycieknie coś spoza projektu. Zabezpieczenia: lista dozwolona zamiast listy zakazanej, skan, przegląd Kuby, commit dopiero po zgodzie.
- 650 tys. znaków nikt nie przeczyta w całości. Zabezpieczenie: indeks i odnośniki z README do konkretnych miejsc.
- Rozmowy pokazują pomyłki i nerwowe momenty. Tego właśnie chce zadanie („nie sprzątaj go”), ale to decyzja Kuby.
- Wiadomości Kuby mogą zawierać coś prywatnego, czego skan nie rozpozna (np. o samej rekrutacji). Zabezpieczenie: przegląd Kuby.

**Warianty.**
- (A) tylko sekcja w README — 1,5 godziny, bez ryzyka, ale prompty do głównego narzędzia dalej niewidoczne, a obaj recenzenci właśnie tego szukali;
- (B) README i same wiadomości Kuby — około 1,5 godziny więcej; widać polecenia, nie widać, jak odpowiadało AI;
- (C) README, wiadomości Kuby, odpowiedzi Claude i polecenia dla innych sesji — **rekomendacja**, bo dopiero to pokazuje sposób pracy; 2–3 godziny więcej;
- surowe pliki rozmów albo eksport z aplikacji — odradzamy: globalne instrukcje, pamięć i inne projekty, razem 219 MB;
- dodatkowo: lekcje zapisane przez Claude w pamięci projektu (26 wpisów, każdy to ślepa uliczka z uzasadnieniem) jako `notatki/lekcje.md`; jeden wpis wymienia usługi spoza projektu i trzeba go przyciąć. Rekomendacja: tak, razem z wariantem C.

## Poprawka 3. Pierwsza zakładka: zdania, które recenzenci czytali dwa razy

Liczby bez zmian; zmiana w kodzie tekstów i w szkicu `notatki/e_teksty.md`.
1. „Z kanałów bezpłatnych … przybyło 12% nowych pacjentów” → „… jest o 12% więcej niż rok wcześniej” (Fable i kontrola języka, P1; to przyrost z 7 069 do 7 924, a nie udział).
2. Zastrzeżenie o III kwartale nazywa marżę: „Marża po koszcie lekarza, kampaniach i prowizji spadła w III kwartale 2026 o 7%…”; to samo w „Wyniku biznesu” (Fable, P3).
3. Decyzja 2: „według obu reguł przypisania” → „według obu reguł przypisania źródła (pierwsze wejście i sesja z płatnością)” (Fable).
4. Karta „Lepsza retencja”: zastrzeżenie przepisane tak, żeby nie przeczyło zdaniu o 71% spadku przypadającym na skład pacjentów (Fable).
5. „Awaria Safari trwała 198 dni bez alarmu” (decyzja 3 i dwa miejsca w pozycji 2) → „awaria trwała 198 dni, do końca danych”; dane nie mówią nic o alarmach (Astra).
6. Kolejność decyzji na pierwszy tydzień taka jak na liście priorytetów (1, 2, 3–4, potem sprawdzenia); dziś 1, 3–4, 2, co myliło Astrę. Rekomendacja: tak.

**Jak to zobaczy ktoś z Telemedi:** te same liczby, bez zdań do czytania dwa razy i bez twierdzenia, którego dane nie pokazują. **Sprawdzenie:** kontrola eksportu, zrzut tekstów, przeglądarka. **Ile:** 1 godzina. **Ryzyko:** małe; zmiana zdania bez zmiany szkicu zatrzyma kontrolę eksportu.

## Poprawka 4. Pozostałe poprawki z kontroli języka

Z 12 poprawek „przed wysłaniem” dwie są w poprawce 3 (P1, P3). Zostaje 10:
- niezgodne z danymi albo z wykresem: P2 (podświetlony blok poranny na wykresie godzin kończy się o 12:59, a tytuł karty mówi o 13:59), P4 (zdanie w „Lejku” sugeruje wzrost ruchu nowych kampanii od lutego, a wykres na tej samej zakładce pokazuje wzrost od listopada), P7 („około 40 pacjentów” w objaśnieniu mapy kohort jest wpisane w kod, a mediana kohorty dziennej w danych to 54);
- liczby bez okresu i grupy: P6;
- błędy językowe i niezrozumiałe zdania: P5, P8, P10, P11, P12 i P9 (słowo „podział” w znaczeniu reguły przypisania, około 14 miejsc w szczegółach i 2 w README).

**Rekomendacja:** wszystkie dziesięć, bo i tak robimy jeden eksport i jedną kontrolę; około 1,5–2 godzin. **Minimum:** P2, P4, P6, P7. **Sprawdzenie:** jak w poprawce 3; P2 zmienia pole eksportu, więc dochodzi zrzut wykresu godzin. **Ryzyko:** P9 dotyka wielu miejsc; wersja minimalna to szczegóły „Kohort”, „Lejka” i karty „Lepsza retencja”. 35 uwag „na rozmowę” z kontroli języka zostaje bez zmian.

## Poprawka 5. Wykres Safari na równych oknach czasu (mała, opcjonalna)

**Co:** wykres w karcie Safari („Lejek”, ten sam w pozycji 1 priorytetów) porównuje dziś okres po awarii 17.03–30.09.2026 dla Safari z 17.03–15.05.2026 dla pozostałych przeglądarek. Zamiana na porównanie, które już jest w szczegółach karty: 60 dni przed awarią i 60 dni po niej dla obu (Safari 66,2% → 45,1%, pozostałe przeglądarki 64,8% → 63,4%). **Dlaczego:** Astra i kontrola języka niezależnie zauważyły niesymetryczne okna w obowiązkowej części zadania (lejek). Wniosek się nie zmienia, a znika zarzut do metody. **Skąd liczby:** już w eksporcie. **Ile:** 45 minut. **Ryzyko:** zdania cytujące wartości z wykresu trzeba zgrać z nowym wykresem; kontrola wykresu z tekstem karty to wyłapie. **Rekomendacja:** tak.

## Punkt 6. Wynik kontroli technicznej i poprawki techniczne

**Wynik (`notatki/f_techniczna.md`):** wersja `a4d52c9` jest technicznie gotowa po jednej małej poprawce. Eksport: 115 kontroli bez różnic, 4 218 liczb w tekstach z pokryciem w szkicach. Liczby na wykresach wobec tekstu i tabel kart: 1 956 porównań na silnik przeglądarki, bez ani jednej niezgodności w Edge, WebKit (silnik Safari) i Firefoksie. 305 odnośników z filtrami otwiera ten sam stan wprost i po odświeżeniu. Wszystkie żądania idą do lokalnego serwera. Na telefonie z wolnym 4G pierwsza zakładka jest gotowa po 1,6 s. Ponowny eksport daje te same dane strony; różnią się tylko godzina, skrót commitu w stopce i 11 sum przychodu w piętnastej cyfrze (szum zmiennoprzecinkowy, na stronie niewidoczny).

**6a. Pasek zakładek na tablecie (przed wysłaniem, rekomendacja: tak).** Przy szerokości od 761 do około 990 px (iPad trzymany pionowo, okno na pół ekranu) pasek chowa „Priorytety” i „Czego nie wiemy”, a nic nie pokazuje, że da się go przewinąć. Poprawka: jedna reguła w `narzedzie/styl.css` (zakładki w dwóch rzędach poniżej 1 000 px), sprawdzona w przeglądarce przy 768, 834, 900, 960 i 999 px. 15 minut plus powtórzenie kontroli.

**6b. Safari na iPhonie: „Lejek” przesuwa się w bok o około 100 px (rekomendacja: tak).** Lejek to obowiązkowa część zadania, a iPhone to prawdopodobne urządzenie osoby oceniającej. Poprawka: jedna reguła dla filtrów na telefonie, sprawdzona w WebKit. 15 minut; potwierdzenie na prawdziwym iPhonie po publikacji.

**6c. Telefon: ucięte ostatnie cyfry w tabelach „Kohorty w podziale” i „Kroki lejka w podziale” (rekomendacja: tak, jeśli zmieści się w rundzie).** Widać np. „17,4% z 18 92”, co można wziąć za błąd liczby w najważniejszej zakładce. Poprawka: zawinąć „z N” do drugiego wiersza w widoku telefonu. Około 30 minut; ryzyko: zmiana układu komórek w innych tabelach, sprawdzana zrzutami.

**6d. Porządek przed publikacją (bez decyzji):** ostatni eksport i komplet kontroli (w tym nowe skrypty `analiza/f_*.py`), commit odświeżonych plików eksportu razem z poprawkami, odtworzenie `analiza/wyniki/b_teksty_strony.md` i `b_eksport_c.txt` (oba w commicie nieaktualne), stopka ze stanem repozytorium, adres narzędzia w README w dniu publikacji. Po publikacji Kuba otwiera link na iPhonie, iPadzie i telefonie z Androidem (tego nie da się sprawdzić lokalnie).

**Zbieżność z poprawką 1:** kontrola techniczna zauważyła, że odnośniki do „Kohort” nie przewijają do wykresu dziennego. Odnośniki „Pokaż na kohortach dziennych” z tabeli zdarzeń muszą to robić, więc poprawka 1 obejmuje przewinięcie (około 30 minut więcej). **Zbieżność z poprawką 5:** niesymetryczne okna wykresu Safari wskazały niezależnie trzy kontrole (Astra, język, technika).

## Czego nie ruszamy

Zgodnie u obu recenzentów i w kontroli języka: odpowiedź „Nie” i werdykt na pierwszej stronie; liczby i definicje; dwie reguły przypisania źródła (tylko raz je nazwać); zasada pełnych okien obserwacji; oddzielanie obserwacji od przyczyny; struktura 9 zakładek; „Czego nie wiemy”; styl zastrzeżeń; historia commitów. Żadnych nowych analiz, recenzji modeli ani tekstu ponad te poprawki.

## Na rozmowę (bez zmian teraz)

- **Praca na co dzień.** Obaj recenzenci: narzędzie dobre do diagnozy i przeglądów tygodniowych; brakuje widoku „ostatnie 7 dni” i alarmów. Na rozmowę: codzienny raport z alarmami to pozycja 2 naszej listy, bo najpierw trzeba oczyścić dane (duplikaty, konta testowe); narzędzie pokazuje, czego ten raport ma pilnować. Ten sam widok proponowało konsylium w punkcie D i nie wszedł na listę Kuby.
- Pozycje 7, 11 i 12 mają wartość za punkt procentowy albo koszt testu zamiast kwoty; jeden znacznik pewności dla problemu i kwoty; reguła decyzji testu Mety; kryterium skuteczności alarmów.
- Ilość tekstu (około 205 tys. znaków), rozbudowane „Po zakupie”, tabele scenariuszy po 24 liczby, dwie reguły przypisania obok siebie wszędzie.
- Ekonomia kampanii bez serii tydzień po tygodniu; seria kohort bez kosztu pozyskania.
- 9 niewiadomych bez przypisanej pozycji listy priorytetów.
- Szerokie tabele na telefonie przewijane w bok.
- Etykiety „lepiej” i „gorzej” przy zmianach bez znaczenia (np. oceny wizyt, różnica 0,01).
- Nagłówek karty TelemediGO mówi o „chęci zakupu”, a wykres pokazuje liczby zakupów bez odsetków.
- 35 uwag językowych R1–R35 (`notatki/f_jezyk.md`).
- Skrypt zrzutów `analiza/e_przegladarka.py` psuje zrzuty stron wyższych niż 16 384 px.
- Z kontroli technicznej: kontrast białych liczb na kolorowych polach (3,2:1 do 4,4:1 przy wymaganych 4,5:1), ucięte podpisy na końcach linii wykresów, dwie nazwy tego samego kroku lejka, odwrotna kolejność kolumn w tabelach powrotu, krótszy podpis TelemediGO na wykresie niż w tabeli, filtry „Po zakupie”, „Wyniku biznesu”, osi zdarzeń i „Czego nie wiemy” niezapisywane w adresie, `robots.txt` niedziałający pod podścieżką (chroni znacznik `noindex`).

## Kolejność i podział pracy (po decyzji Kuby)

- **Sesja A (teksty, eksport, strona):** poprawki 3 → 4 → 1 → 5 → 6a–6c, potem eksport i kontrola liczb. Nie dotyka README.
- **Sesja B (ślad pracy):** poprawka 2: sekcja README (razem z dwoma zdaniami z P9 w README), skrypt zapisu rozmów, skan i raport dla Kuby. Nie dotyka plików sesji A.
- **Sesja prowadząca:** po obu sesjach wszystkie kontrole na ostatecznej wersji, krótkie przejrzenie przez Codeksa (Sol) nowej tabeli i zmienionych zdań pod kątem „czy nie mówią więcej niż dane”, notatki, commit i zatrzymanie u Kuby przed publikacją.

## Do decyzji Kuby

1. Poprawka 1: miejsce (rekomendacja: pierwsza karta „Kohort”), liczby (rekomendacja: tylko już policzone), zdarzenie 8 jako wiersz czy tylko na osi.
2. Poprawka 2: wariant (rekomendacja: C) i lekcje z pamięci projektu (rekomendacja: tak).
3. Poprawka 3: kolejność decyzji na pierwszy tydzień jak na liście priorytetów (rekomendacja: tak).
4. Poprawka 4: wszystkie dziesięć czy minimum (rekomendacja: wszystkie).
5. Poprawka 5: wykres Safari na równych oknach (rekomendacja: tak).
6. Poprawki techniczne 6a, 6b, 6c (rekomendacja: tak dla wszystkich trzech; 6c tylko jeśli zmieści się w rundzie).
7. Dwie sesje naraz (rekomendacja: tak; poprawki 6a–6c robi sesja A razem ze stroną).
