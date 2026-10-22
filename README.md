# Telemedi B2C: czy to, co widać na dashboardzie, jest wzrostem?

Rozwiązanie zadania rekrutacyjnego na stanowisko Head of B2C. Dane to dwa lata biznesu B2C (1.10.2024 – 30.09.2026), wygenerowane na potrzeby zadania.

**Narzędzie:** `https://<organizacja>.github.io/<repozytorium>/` — adres uzupełnimy w dniu publikacji. Strona otwiera się w przeglądarce, bez instalacji i bez konta.

## Odpowiedź w skrócie

**Nie.** Pacjentów przybywa, ale wracają rzadziej. Wydatki na kampanie rosną dużo szybciej niż marża, którą biznes zarabia przed ich kosztem. Dla Telemedi wzrost to więcej pacjentów i lepsza retencja naraz, a spełniony jest tylko pierwszy warunek.

- **Więcej pacjentów: tak, ale głównie z dwóch nowych kampanii na L4.** Nowych pacjentów jest o 52% więcej niż rok wcześniej (24 687 wobec 16 231). Prawie co trzeci (29%) przyszedł z kampanii Meta albo TikTok na zwolnienie lekarskie (L4). Bez nich przyrost wynosi 7%.
- **Lepsza retencja: nie.** W ciągu 90 dni wraca 17% nowych pacjentów wobec 24% rok wcześniej (te same dni kalendarzowe). Pacjenci nowych kampanii prawie nie wracają (4%), a bez nich powrót też spada, do 22%.
- **Wynik: wydatki rosną szybciej niż marża przed ich kosztem.** W III kwartale 2026 marża przed kosztem kampanii wzrosła o 25%, a wydatki na kampanie były ponad dwa razy wyższe. Za cały rok marża po koszcie lekarza, kampaniach i prowizji wzrosła o 27% (z 828 do 1 048 tys. zł). Spadek marży w samym III kwartale 2026 (o 7%) zależy od jednorazowego zdarzenia: rok wcześniej we wrześniu ruszyła sprzedaż TelemediGO w newsletterze. Po odjęciu jej jednorazowej nadwyżki marża kwartału jest o 1% wyższa niż rok wcześniej.
- **Gdzie i od kiedy tracimy pacjentów:** wśród osób, które jeszcze nie kupowały, od kwietnia 2026 płaci 8% sesji wobec 11% w tych samych miesiącach rok wcześniej (liczba płatności rośnie, spada ich odsetek). Spadek zaczyna się w lutym 2026, gdy ruch z nowych kampanii przekracza 30% sesji nowych osób, i pogłębia się od kwietnia. Bez sesji nowych kampanii konwersja nowych osób nie spada. Niezależnie od tego od 17.03.2026 nowi pacjenci na iPhone'ach rzadziej kończą zakładanie konta.
- **TelemediGO rośnie razem z liczbą zamówień** (+40%), a nie dzięki większej chęci zakupu. Opłata 89 zł nie pokrywa zniżek, co widać w marży powtórnych zamówień.
- **Dashboard pokazuje więcej wzrostu, niż jest w danych.** Liczy 604 zdublowane zamówienia, zamówienia 22 kont testowych i przychód przed zwrotami. Po oczyszczeniu zamówień przybyło o 56%, a nie o 61%, a przychodu z konsultacji po zwrotach o 45%, a nie o 50%.

Źródło pacjenta przypisujemy na dwa sposoby i w całym narzędziu nazywamy je tak samo. Pacjentów i retencję liczymy **według pierwszego wejścia** (pierwsze wejście pacjenta na stronę, a kod kampanii na pierwszym zamówieniu rozstrzyga). **Według sesji z płatnością** do innych kanałów trafia 2 081 pacjentów nowych kampanii: 1 918 weszło z ich reklamy, a zapłaciło w innej sesji, a 163 zapłaciło z kodem kampanii po wejściu z innego kanału. Bez nich oba podziały dają ten sam przyrost pacjentów, powrót i marżę. W ekonomii kampanii pokazujemy oba.

## Co robimy w pierwszym tygodniu

Ta sama lista stoi w narzędziu: w zakładce „Czy to wzrost” i w zasadach listy priorytetów (pozycje 1, 3 i 4 oraz pierwsze kroki pozycji 2, 5, 6, 8 i 11).

1. Naprawiamy zakładanie konta w Safari na iPhone'ach (od 17.03.2026 konta powstają tam rzadziej). To największa pewna strata: do 83 tys. zł marży rocznie (pozycja 1).
2. Wstrzymujemy kampanię TikTok na L4 i kampanię Google Ads na specjalistów. Obie tracą na każdym pacjencie według obu reguł przypisania, a pauzę da się cofnąć w jeden dzień (pozycje 3 i 4).
3. Czyścimy codzienny raport (bez duplikatów, bez kont testowych, przychód po zwrotach), dodajemy alarmy na lejku i sprawdzamy, czy lekarze dostają wynagrodzenie za wizyty testowe (pozycja 2).
4. Robimy krótkie sprawdzenia, każde na dzień albo dwa: co obiecują reklamy L4 (pozycja 5), poranne grafiki internistów (pozycja 6), ręczny zakup po zalogowaniu (pozycja 8) i kliknięcia w panelach Meta i TikToka wobec sesji (pozycja 11).

## Jak używać narzędzia na co dzień

- **Lejek:** domyślnie osoby, które jeszcze nie kupowały. Każdy krok dzień po dniu według przeglądarki i kampanii. Spadek jednego kroku w jednej przeglądarce to sygnał awarii, tak jak w Safari 17.03.2026.
- **Kohorty:** kohorty dzienne z ostatnich dni, w podziale na źródło i pierwszą usługę. Najpierw powrót w 30 dniach u kohort, które mają już pełne okno, potem marża na pacjenta.
- **Po zakupie:** punktualność porannych wizyt u internisty i zwroty po wizycie według kampanii.
- **Wynik biznesu:** marża przed kosztem kampanii i po nim, kwartał do kwartału rok wcześniej, i wynik na pacjenta każdej kampanii według pierwszego wejścia i według sesji z płatnością.
- **Zdarzenia:** czy zmiana, którą widać w kohortach albo w lejku, ma już datę i opis.

Pełna odpowiedź, lista 12 priorytetów (wartość w marży, sposób pomiaru, czas wdrożenia) i lista niewiadomych z testami są w narzędziu, w zakładkach „Czy to wzrost”, „Priorytety” i „Czego nie wiemy”. Każda karta ma zwijane „Szczegóły” z liczebnościami, podziałem według sesji z płatnością, metodą i źródłem liczb.

## Co jest w narzędziu

| Zakładka | Co pokazuje |
|---|---|
| Czy to wzrost | odpowiedź na pytanie zadania, osobno dla pacjentów i dla retencji, z decyzjami na pierwszy tydzień |
| Kohorty | kohorty dzienne, powroty w 30, 60, 90 i 180 dniach, marża na pacjenta, macierz kohort i krzywa powrotu; filtry: źródło (według pierwszego wejścia albo według sesji z płatnością), kampania, urządzenie, przeglądarka, pierwsza usługa, zniżka, TelemediGO, status i punktualność pierwszej wizyty |
| Lejek | wykres kroków od wejścia na stronę do płatności i tabela kroków, dzień po dniu, w podziałach na urządzenie, przeglądarkę, kanał, kampanię i stronę wejścia |
| Po zakupie | punktualność wizyt według pory i specjalizacji, zwroty, anulacje, oceny |
| Zdarzenia | oś czasu zdarzeń znalezionych w danych (pozyskanie, lejek, retencja, obsługa pacjenta) |
| Wynik biznesu | przychód, koszt lekarza, kampanie i marża w czasie, kwartały rok do roku, ekonomia kampanii według pierwszego wejścia i według sesji z płatnością |
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
- **Ślepe uliczki zostały w historii commitów.** Historii nie przepisywaliśmy.

## Co w danych wygląda podejrzanie (szczegóły: `notatki/ZNALEZISKA.md`)

- 604 zamówienia zapisane dwa razy, wszystkie z 10–24.06.2026.
- 22 konta testowe z 2 071 zamówieniami: kod TEST-QA i zamówienia bez kodu na tych samych kontach, każda wizyta trwa 1 minutę. Testów przybywa.
- Od 17.03.2026 w Safari na iPhone'ach i iPadach gwałtownie spada skuteczność zakładania nowego konta.
- Żadna z 22 068 sesji pacjentów zalogowanych od wejścia nie kończy się zakupem konsultacji. Dane nie rozstrzygają, czy to wizyty „sprawdzam konto”, czy zepsuta ścieżka zakupu.
- Na kliknięcie reklamy w Meta i TikToku przypada wyraźnie mniej sesji niż w Google Ads.
- Wizyta u pediatry kosztuje pacjenta mniej niż wynosi koszt lekarza (przy założeniu opartym na zadaniu: 100 zł za każdego specjalistę poza internistą i psychiatrą).
