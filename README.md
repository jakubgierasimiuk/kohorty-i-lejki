# Telemedi B2C: czy to, co widać na dashboardzie, jest wzrostem?

Rozwiązanie zadania rekrutacyjnego na stanowisko Head of B2C. Dane to dwa lata biznesu B2C (1.10.2024 – 30.09.2026), wygenerowane na potrzeby zadania.

**Narzędzie:** https://jakubgierasimiuk.github.io/kohorty-i-lejki/ — strona otwiera się w przeglądarce, bez instalacji i bez konta.

**Repozytorium (ślad pracy):** https://github.com/jakubgierasimiuk/kohorty-i-lejki

## Odpowiedź w skrócie

**Nie.** Prawie cały przyrost pacjentów (86%) to pacjenci dwóch nowych kampanii na zwolnienie lekarskie (L4), w Mecie i w TikToku, a na ich pacjencie po koszcie pozyskania prawie nic nie zostaje: 7 zł w ciągu 180 dni wobec 30 zł na pacjencie pozostałych kampanii płatnych, a na pacjentach pozyskanych od wiosny 2026 szacunkowo wychodzimy na zero. Marża po wszystkich kosztach wzrosła o 27% prawie wyłącznie dzięki zakupom pacjentów pozyskanych w pierwszym roku. Pacjenci pozyskani w ostatnich 12 miesiącach zarobili w roku pozyskania, po kosztach kampanii, tylko o 3% więcej niż ci pozyskani rok wcześniej, choć było ich o 52% więcej.

- **Więcej pacjentów: tak, ale.** Nowych pacjentów jest o 52% więcej niż rok wcześniej (24 687 wobec 16 231), ale bez dwóch nowych kampanii na L4 tylko o 7%.
- **Lepsza retencja: nie.** W ciągu 90 dni wraca 17% nowych pacjentów wobec 24% rok wcześniej (te same dni kalendarzowe). Pacjenci nowych kampanii prawie nie wracają (4%), a bez nich powrót też spada, do 22%.
- **Więcej zarabiamy: tak, ale.** Marża po wszystkich kosztach (po wynagrodzeniu lekarzy, wydatkach na kampanie i prowizji afiliacyjnej) wzrosła z 828 do 1 048 tys. zł. 88% tego przyrostu to kolejne zakupy pacjentów pozyskanych w pierwszym roku, a wynik pacjentów pozyskanych w danym roku, po kosztach kampanii, wzrósł tylko o 3%. To nie jest lepsza retencja: tych zakupów rok wcześniej nie było, bo w danych nie ma pacjentów sprzed 1.10.2024.
- **Ile zostaje na nowym pacjencie po koszcie pozyskania** (marża w 180 dniach od pierwszego zakupu minus wydatki na kampanię podzielone przez jej nowych pacjentów): na pacjencie nowych kampanii na L4 7 zł, na pacjencie pozostałych kampanii płatnych 30 zł (rok wcześniej 32 zł). Koszt pozyskania pacjenta nowych kampanii rośnie z 27–30 zł (listopad 2025 – luty 2026) do 33–37 zł (kwiecień – wrzesień 2026), a jego marża stoi na poziomie 34–40 zł, więc od kwietnia zostaje od −1 do +3 zł. TikTok na L4 traci od marca 2026. Według sesji z płatnością obie kampanie średnio tracą na pacjencie od grudnia 2025.
- **Z kwartału na kwartał wydatki na kampanie rosną szybciej, a marża przed ich kosztem wolniej.** W III kwartale 2026 wydatki były ponad dwa razy wyższe niż rok wcześniej, a marża przed ich kosztem wyższa o 25%. Wzrost marży po kosztach kampanii się zatrzymał: w III kwartale 2026 spadła o 7% rok do roku, a po odjęciu jednorazowego startu sprzedaży TelemediGO w newsletterze rok wcześniej byłaby wyższa tylko o 1%.
- **Czego nie wiemy przy tej odpowiedzi:** ilu pacjentów nowych kampanii przyszłoby i bez reklamy. Odpowie na to test z pozycji 9 listy priorytetów: wyłączenie kampanii Meta na L4 na 4–6 tygodni w losowej połowie województw i porównanie wszystkich nowych pacjentów z drugą połową.
- **Gdzie i od kiedy tracimy pacjentów:** wśród osób, które jeszcze nie kupowały, od kwietnia 2026 płaci 8% sesji wobec 11% w tych samych miesiącach rok wcześniej (liczba płatności rośnie, spada ich odsetek). Powody są dwa. Pierwszy to zmiana ruchu: spadek zaczyna się w lutym 2026, gdy ruch z nowych kampanii przekracza 30% sesji nowych osób, a te sesje płacą o połowę rzadziej niż pozostałe. Drugi to awaria: od 17.03.2026 nowe osoby w Safari na iPhone'ach rzadziej kończą zakładanie konta. Poza osobami z nowych kampanii (licząc według pierwszego wejścia, jak w retencji) od kwietnia wyraźnie płacą rzadziej tylko sesje w Safari na iPhone'ach: 8% wobec 12% rok wcześniej. W innych przeglądarkach konwersja jest bez istotnej zmiany.
- **TelemediGO rośnie razem z liczbą zamówień** (+40%), a nie dzięki większej chęci zakupu. Opłata 89 zł nie pokrywa zniżek, co widać w marży powtórnych zamówień.
- **Dashboard pokazuje więcej wzrostu, niż jest w danych.** Liczy 604 zdublowane zamówienia, zamówienia 22 kont testowych i przychód przed zwrotami. Po oczyszczeniu zamówień przybyło o 56%, a nie o 61%, a przychodu z konsultacji po zwrotach o 45%, a nie o 50%.

Źródło pacjenta przypisujemy na dwa sposoby i w całym narzędziu nazywamy je tak samo. Pacjentów i retencję liczymy **według pierwszego wejścia** (pierwsze wejście pacjenta na stronę, a kod kampanii na pierwszym zamówieniu rozstrzyga). **Według sesji z płatnością** do innych kanałów trafia 2 081 pacjentów nowych kampanii: 1 918 weszło z ich reklamy, a zapłaciło w innej sesji, a 163 zapłaciło z kodem kampanii po wejściu z innego kanału. Bez nich obie reguły przypisania dają ten sam przyrost pacjentów, powrót i marżę. W ekonomii kampanii pokazujemy oba.

## Co robimy w pierwszym tygodniu

Ta sama lista stoi w narzędziu: w zakładce „Czy to wzrost” i w zasadach listy priorytetów (pozycje 1, 3 i 4 oraz pierwsze kroki pozycji 2, 5, 6, 8 i 11).

1. Naprawiamy zakładanie konta w Safari na iPhone'ach (od 17.03.2026 konta powstają tam rzadziej). Awaria jest widoczna w danych, a naprawa jest warta do 83 tys. zł marży rocznie (górny scenariusz, pozycja 1).
2. Czyścimy codzienny raport (bez duplikatów, bez kont testowych, przychód po zwrotach), dodajemy alarmy na lejku i sprawdzamy, czy lekarze dostają wynagrodzenie za wizyty testowe (pozycja 2).
3. Wstrzymujemy kampanię TikTok na L4 i kampanię Google Ads na specjalistów. Obie średnio tracą na pacjencie według obu reguł przypisania, a pauzę da się cofnąć w jeden dzień (pozycje 3 i 4).
4. Robimy krótkie sprawdzenia, każde na dzień albo dwa: co obiecują reklamy L4 (pozycja 5), poranne grafiki internistów (pozycja 6), ręczny zakup po zalogowaniu (pozycja 8) i kliknięcia w panelach Meta i TikToka wobec sesji (pozycja 11).

## Jak używać narzędzia na co dzień

- **Lejek:** domyślnie osoby, które jeszcze nie kupowały. Każdy krok dzień po dniu według przeglądarki i kampanii. Spadek jednego kroku w jednej przeglądarce to sygnał awarii, tak jak w Safari 17.03.2026.
- **Kohorty:** kohorty dzienne z ostatnich dni, w podziale na źródło i pierwszą usługę. Najpierw powrót w 30 dniach u kohort, które mają już pełne okno, potem marża na pacjenta.
- **Po zakupie:** punktualność porannych wizyt u internisty i zwroty po wizycie według kampanii.
- **Wynik biznesu:** marża przed kosztem kampanii i po nim, kwartał do kwartału rok wcześniej, i wynik na pacjenta każdej kampanii według pierwszego wejścia i według sesji z płatnością.
- **Zdarzenia:** czy zmiana, którą widać w kohortach albo w lejku, ma już datę i opis.

Pełna odpowiedź, lista 12 priorytetów (wartość w marży, sposób pomiaru, czas wdrożenia) i lista niewiadomych z testami są w narzędziu, w zakładkach „Czy to wzrost”, „Priorytety” i „Czego nie wiemy”. Każda karta ma zwijane „Szczegóły” z liczebnościami, wynikiem według sesji z płatnością (druga reguła przypisania), metodą i źródłem liczb.

## Co jest w narzędziu

| Zakładka | Co pokazuje |
|---|---|
| Czy to wzrost | odpowiedź na pytanie zadania: werdykt z trzema linijkami (więcej pacjentów, lepsza retencja, więcej zarabiamy) i osiem kroków, każdy z pytaniem, odpowiedzią i tym, co znaczy dla biznesu: liczby z dashboardu, skąd są nowi pacjenci, czy wracają, ile zostaje na nowym pacjencie po koszcie pozyskania, skąd +27% marży, kierunek z kwartału na kwartał, co robimy (z decyzjami na pierwszy tydzień) i czego nie wiemy; TelemediGO osobno |
| Kohorty | wniosek o powrotach, pasek „Pacjenci w analizie” (przypisanie źródła, zawężenia, „Przywróć domyślne”), mapa kohort miesięcznych, tygodniowych albo dziennych z nazwami zdarzeń, kohorty dzień po dniu z przyciskami zdarzeń (porównanie 60 dni przed i po) i tabelą grup (kolor tylko przy zmianie większej niż przypadek), krzywa powrotu |
| Lejek | pasek „Sesje w analizie” z „Przywróć domyślne”, kroki od wejścia na stronę do płatności, dzień po dniu z przyciskami zdarzeń i tabelą grup (urządzenie, przeglądarka, kanał, kampania, strona wejścia), rozpoznane problemy (Safari, przeglądarki w aplikacjach) |
| Po zakupie | punktualność wizyt według pory i specjalizacji, opóźnienia według godziny i porannego ruchu, powrót i oceny po spóźnionej wizycie, zwroty, anulacje i wizyty nieodebrane |
| Zdarzenia | na górze tabela zdarzeń i naszych decyzji, które zmieniły kohorty i wynik (skutek w złotych, pewność, co robimy, odnośnik do porównania 60 dni przed i po na kohortach dziennych); oś czasu zdarzeń znalezionych w danych (lejek, retencja, obsługa pacjenta, jakość danych) i ich opisy |
| Wynik biznesu | wniosek o marży, kwartały rok do roku, marża i wydatki na kampanie w czasie, ekonomia kampanii według pierwszego wejścia i według sesji z płatnością |
| Jakość danych | podejrzane rzeczy w danych i to, jak je potraktowaliśmy |
| Priorytety | 12 działań od najważniejszego |
| Czego nie wiemy | czego dane nie rozstrzygają i jaki test albo jakie dane by to domknęły |

## Co jest w repozytorium

| Folder | Zawartość |
|---|---|
| `narzedzie/` | strona narzędzia: HTML, JavaScript, biblioteka wykresów uPlot w przypiętej wersji i przeliczone dane (`dane_strony/`, bez danych pojedynczych pacjentów z identyfikatorami) |
| `analiza/` | cały kod analizy w Pythonie (DuckDB i pandas), kolejność uruchamiania w `analiza/README.md` |
| `analiza/wyniki/` | raporty i zestawienia z każdego kroku; każda liczba w notatkach i w narzędziu pochodzi z tych plików |
| `notatki/` | ślad pracy: założenia (`ZALOZENIA.md`), znaleziska w danych (`ZNALEZISKA.md`), decyzje (`DECYZJE.md`), plan (`PLAN.md`) i notatki z kolejnych kroków |
| `notatki/recenzje/` | niezależne recenzje drugiego modelu AI: polecenia, odpowiedzi i to, co poprawiliśmy |
| `notatki/konsylium/` | ocena listy priorytetów i końcowa weryfikacja całego rozwiązania przez kilka modeli AI różnych firm, z wynikiem |
| `bezpieczenstwo/` | kontrola paczki z danymi przed rozpakowaniem i raporty z niej |

Surowych danych, paczki i bazy danych nie ma w repozytorium.

## Jak odtworzyć liczby

1. Python 3.13 z pakietami `duckdb` 1.5.5, `pandas` 2.3.3 i `pyarrow`.
2. Rozpakowane pliki CSV z zadania w folderze `dane/`.
3. Z głównego folderu repozytorium uruchom kolejno skrypty z tabeli w `analiza/README.md`, zawsze przez `python -I`. Pierwsze dwa budują bazę: `python -I analiza/a1_baza.py`, potem `python -I analiza/a2_czyste.py`. Każdy następny skrypt tylko czyta bazę i zapisuje raport do `analiza/wyniki/`.
4. Dane strony narzędzia odtwarza `python -I analiza/b_eksport.py`. Uruchamia on też `analiza/b2_eksport_c.py` i moduły tekstów `analiza/e_teksty.py` oraz `analiza/e_teksty_zakladki.py`, które składają zdania z liczb w raportach. Eksport sprawdza każdą liczbę na stronie z raportami i z notatkami z tekstami.
5. Podgląd strony lokalnie: `python -m http.server 8765` uruchomione w folderze `narzedzie/`, potem http://127.0.0.1:8765/.

## Jak pracowaliśmy

- **Kolejność:**
  - kontrola bezpieczeństwa paczki;
  - jakość danych;
  - dokładne odtworzenie liczb dashboardu;
  - definicje (nowy pacjent, powrót, źródło pozyskania, przychód) ustalone przed kohortami;
  - kohorty, lejek, to, co dzieje się po zakupie, i zdarzenia;
  - ekonomia kampanii;
  - lista priorytetów i niewiadomych.
- Każdy krok kończył się przeglądem i decyzją, zapisaną w `notatki/DECYZJE.md`.
- **Analiza i narzędzie powstały z AI** (Claude Code). Analizę robiliśmy kodem, a do rozmowy trafiały tylko wyliczenia.
- **Każdy większy krok sprawdzał drugi, niezależny model** (Codex, OpenAI). Przeliczał liczby własnym kodem i recenzował definicje, metodę i brzmienie wniosków. Uwagi i poprawki są w `notatki/recenzje/`.
- **Listę priorytetów oceniło konsylium:** kilka modeli różnych firm dostało ten sam opis bez naszej opinii. Zarzuty, które dało się sprawdzić w danych, sprawdziliśmy kodem.
- **Każde założenie jest nazwane** w `notatki/ZALOZENIA.md`. Tam, gdzie dane dopuszczają więcej niż jedno wyjaśnienie, nie przesądzamy przyczyny i podajemy test, który ją rozstrzygnie.

## Jak pracowaliśmy z AI: prompty, ślepe uliczki, poprawki

Głównym narzędziem był Claude Code. Pracował w kilku sesjach naraz: sesja prowadząca rozdzielała punkty planu, a pozostałe sesje je wykonywały i zgłaszały wynik. Kuba (autor rozwiązania) zatwierdzał każdy punkt planu i każdy wniosek.

**Gdzie są prompty i rozmowy:**
- `rozmowy/` — oczyszczony zapis wszystkich rozmów z Claude Code: polecenia Kuby słowo w słowo, odpowiedzi Claude i polecenia, które sesje wysyłały sobie nawzajem i agentom pomocniczym. W `rozmowy/README.md` jest opis, co usunęliśmy i dlaczego (między innymi tekst zadania i adresy stron).
- `notatki/e_runda.md`, `notatki/d_poprawki.md` i cytaty w `notatki/DECYZJE.md` — dłuższe polecenia Kuby z kolejnych rund, przepisane do notatek.
- `CLAUDE.md` — zasady pracy z AI w tym projekcie: kontrola bezpieczeństwa danych, kiedy zatrzymać się u Kuby, jak sprawdzamy liczby, kiedy sięgamy po drugi model.
- `notatki/recenzje/` — polecenia i odpowiedzi drugiego modelu (Codex) oraz tabele „co przyjmujemy, co odrzucamy i dlaczego”.
- `notatki/konsylium/` — briefy i odpowiedzi konsylium, czyli kilku modeli różnych firm, które oceniały to samo bez naszej opinii.
- `notatki/lekcje.md` — lekcje, które Claude zapisywał po drodze w pamięci projektu: co poszło źle, dlaczego i jak tego unikać.

**Ślepe uliczki i poprawki.** Historii commitów nie przepisywaliśmy, więc każda pomyłka jest w repozytorium razem z poprawką. Poniżej dziesięć najważniejszych. Miejsca, w których dzieją się w rozmowach, są w `rozmowy/README.md`.

1. **Pierwszy plan pracy (19.10).** Claude zaproponował, że sam przeprowadzi całą analizę, a narzędzie zbuduje równolegle. Kuba odrzucił ten plan: wnioski wyciągamy razem po każdym większym kroku, narzędzie powstaje dopiero na sprawdzonych definicjach, a liczby dashboardu odtwarzamy dokładnie, a nie „mniej więcej”. Commit `f596688`, `notatki/DECYZJE.md` (19.10, plan pracy).
2. **Zdania mocniejsze niż dane (19.10).** W streszczeniach dla Kuby Claude dwa razy podał przyczynę, której dane nie rozstrzygały: że wzrost nowych pacjentów od października do stycznia „pasuje do sezonu infekcji” i że sama zmiana struktury źródeł nie tłumaczy spadku powrotu w Mecie. Kuba poprawił oba zdania, bo w tych samych miesiącach rosły wydatki na kampanie, a w Mecie doszła w drugim roku nowa kampania na L4. Oba wątki rozdzieliła potem osobna część analizy. Commity `12a0128` i `cab14b8`, `notatki/DECYZJE.md` (dwie korekty po uwadze Kuby z 19.10).
3. **Kontrola Codeksa a hipoteza Kuby (19.10).** Kuba podejrzewał, że nowe kampanie na L4 przeciążyły porannych internistów. Po kontroli Codeksa Claude wycofał to powiązanie, bo przy tej samej liczbie wizyt w godzinie pacjenci nowych kampanii zmieniali odsetek spóźnionych wizyt tylko o 0,7 punktu procentowego, a Kuba odpowiedział, że przy przeciążeniu to wynik oczekiwany, bo lekarza nie obchodzi, skąd przyszedł pacjent. Porównanie, które rozdziela oba odczytania, pokazało o 26,4 punktu procentowego więcej spóźnionych porannych wizyt niż rok wcześniej przy tym samym ruchu w dniu, więc narzędzie mówi o spadku porannej przepustowości i nie przesądza jego przyczyny. Commity `8f0a767` i `0696058`, `notatki/a5_retencja.md`, `notatki/recenzje/a5r_codex2.md`.
4. **Błędy w kodzie, które złapał drugi model (19.10).** Średnia w DuckDB po cichu pomijała sesje bez późniejszego zamówienia, więc odsetek zamówień w ciągu 7 dni po wejściu z newslettera albo SMS-a wyszedł 14,3% zamiast 2,6%. Opóźnienie wizyty liczone funkcją `date_diff` liczyło przekroczone granice minut, a nie upływ czasu; po poprawce data wzrostu opóźnień przesunęła się z 17.11 na 24.11.2025 i przestała się dokładnie pokrywać ze skokiem ruchu kampanii. Oba błędy znalazł Codex, który przeliczał liczby własnym kodem. Commity `0b157c4` i `8f0a767`, `notatki/recenzje/a5p_codex.md`, `notatki/recenzje/a5r_codex2.md`, `notatki/lekcje.md`.
5. **Safari: awaria schowana pod „zmianą ruchu” (19.10 i 22.10).** Pierwszy nagłówek części o lejku brzmiał: „Konwersja lejka spadła, bo zmienił się ruch, a nie dlatego, że lejek gorzej działa”. Kuba go odrzucił, bo gubił awarię zakładania konta w Safari na iPhone'ach od 17.03.2026 i przeglądarki w aplikacjach, które tracą na każdym kroku lejka. Trzy dni później zdanie „poza nowymi kampaniami konwersja się nie zmieniła” znów przykrywało awarię; po przeliczeniu według pierwszego wejścia, z Safari osobno, wyszło, że poza nowymi kampaniami od kwietnia 2026 wyraźnie rzadziej płacą tylko sesje w Safari na iPhone'ach (8% wobec 12% rok wcześniej). Commity `f240505` i `351f556`, `notatki/DECYZJE.md` (19.10, pozyskanie; 22.10, trzecia lista Kuby).
6. **Spadek marży w III kwartale, który zależał od jednego zdarzenia (20–21.10).** Przy przeglądzie szkicu odpowiedzi Kuba zauważył, że w lipcu–wrześniu 2026 marża jest niższa niż rok wcześniej przy ponad dwa razy wyższych wydatkach na kampanie, i ten spadek (6,8%) trafił na górę odpowiedzi. W ostatniej rundzie Kuba sam go podważył: rok wcześniej we wrześniu ruszyła sprzedaż TelemediGO w newsletterze (225 zakupów w 23 dni), a po odjęciu tej jednorazowej nadwyżki marża kwartału jest o 1,1% wyższa niż rok wcześniej. Na górze stoi teraz fakt odporny na to zdarzenie: marża przed kosztem kampanii wzrosła o 25%, a wydatki na kampanie były 2,08 raza wyższe. Commity `17603fa` i `98a5028`, `notatki/e_runda.md` (punkty 1 i 4).
7. **Kwota awarii Safari a spadek marży: zdania bez rachunku (20–21.10).** Szacowany koszt awarii Safari w III kwartale kilka razy zestawiliśmy ze spadkiem marży tego kwartału bez rachunku. Codex (model Astra) podważył zdanie „bez awarii kwartał byłby na poziomie roku wcześniej”, a po konsylium Kuba sam odjął liczby z syntezy: z 16,2 tys. zł straty reszty biznesu 11,2 tys. zł to opłaty TelemediGO, więc zostaje około 5 tys. zł, a szacunek Safari to 14–21 tys. zł. Porównanie zniknęło ze strony: zostały kwota awarii i zdanie, że wyniku kwartału bez awarii nie mierzymy. Commity `849e12c` i `825c977`, `notatki/d_poprawki.md` (punkt 7 Kuby), `notatki/recenzje/d_astra.md`.
8. **Recenzja Codeksa po konsylium: błąd jednostki i reguła bez uzasadnienia (21.10).** Codex przeliczył niezależnie 35 nowych liczb: 34 się zgadzały, a jedna miała zły okres, bo próg testu Mety w pacjentach dotyczył 332 dni działania kampanii, a nie roku. Wskazał też, że reguły decyzji przy niejednoznacznym wyniku tego testu nie da się uzasadnić „oczekiwaną marżą” bez osobnego modelu; uzasadnienie wycofaliśmy, a regułę zapisaliśmy jako świadomie przyjętą przy dużej niepewności. Wszystkie jego 11 uwag do brzmienia zdań przyjęliśmy. Commit `1bfa75f`, `notatki/recenzje/d2_codex.md`, `notatki/ZALOZENIA.md` (punkt 59).
9. **„Najpierw napraw, potem wyłączaj” a wstrzymanie dwóch kampanii (19–21.10).** Od pierwszego dnia obowiązuje zasada Kuby, że słabe źródło najpierw próbujemy naprawić, a dopiero potem wyłączamy. Mimo to lista priorytetów każe wstrzymać kampanię TikTok na L4 i Google Ads na specjalistów już w pierwszym tygodniu (pozycje 3 i 4), bo dla obu policzyliśmy obie drogi: najkorzystniejsza naprawa zwrotów doprowadza TikToka najwyżej do wyniku bliskiego zera, a kampania na specjalistów musiałaby obniżyć koszt pozyskania o 40–60%, co jest już innym modelem kampanii (główną naprawą jest cennik, pozycja 10). Konsylium przesunęło obie pauzy wyżej, bo nic nie kosztują i da się je cofnąć w jeden dzień. Commity `f596688` (zasada), `17603fa` i `bd827b0` (lista), `notatki/konsylium/c_priorytety/synteza.md`, `notatki/c_szkic.md` (pozycje 3 i 4).
10. **Kontrole, które same się myliły (21–23.10).** Pomocniczy agent Claude, który pisał teksty pięciu zakładek, wygenerował notatkę-wzorzec do kontroli liczb z plików strony, więc kontrola „każda liczba na stronie stoi we wzorcu” przechodziła z definicji. Sesja prowadząca to wyłapała i od tej pory każdą zmianę tekstu wpisujemy osobno w kodzie i we wzorcu; przy następnej liście Kuby wyszło jeszcze kilka liczb wpisanych ręcznie w obu miejscach naraz, więc teraz liczy je kod. W ostatniej kontroli Codex (model Astra) wyłapał wadliwy zrzut ekranu (zrzut całej strony urywa się na 16 384 px wysokości), a sesja prowadząca nieaktualny zapis tekstów strony w repozytorium (powrót w ciągu 180 dni: −5,3 zamiast −5,2 punktu procentowego). Commity `ba9e32c`, `4c594b5` i `3b5eeaa`, `notatki/DECYZJE.md` (21.10 wieczorem i 22.10), `notatki/f_kontrola.md` (punkt 3).

## Co w danych wygląda podejrzanie (szczegóły: `notatki/ZNALEZISKA.md`)

- 604 zamówienia zapisane dwa razy, wszystkie z 10–24.06.2026.
- 22 konta testowe z 2 071 zamówieniami: kod TEST-QA i zamówienia bez kodu na tych samych kontach, każda wizyta trwa 1 minutę. Testów przybywa.
- Od 17.03.2026 w Safari na iPhone'ach i iPadach gwałtownie spada skuteczność zakładania nowego konta.
- Żadna z 22 068 sesji pacjentów zalogowanych od wejścia nie kończy się zakupem konsultacji. Dane nie rozstrzygają, czy to wizyty „sprawdzam konto”, czy zepsuta ścieżka zakupu.
- Na kliknięcie reklamy w Meta i TikToku przypada wyraźnie mniej sesji niż w Google Ads.
- Wizyta u pediatry kosztuje pacjenta mniej niż wynosi koszt lekarza (przy założeniu opartym na zadaniu: 100 zł za każdego specjalistę poza internistą i psychiatrą).
