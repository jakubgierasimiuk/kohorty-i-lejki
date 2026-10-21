# Telemedi B2C: czy to, co widać na dashboardzie, jest wzrostem?

Rozwiązanie zadania rekrutacyjnego na stanowisko Head of B2C. Dane to dwa lata biznesu B2C (1.10.2024 – 30.09.2026), wygenerowane na potrzeby zadania.

**Narzędzie:** `https://<organizacja>.github.io/<repozytorium>/` — adres uzupełnimy w dniu publikacji. Strona otwiera się w przeglądarce, bez instalacji i bez konta.

## Odpowiedź w skrócie

**Nie: w rozumieniu Telemedi („więcej pacjentów i lepsza retencja naraz”) to nie jest wzrost.** Z dwóch warunków spełniony jest tylko pierwszy.

- **Więcej pacjentów: tak.**
  - Pacjentów z pierwszym zakupem jest o 52,1% więcej: 24 687 w roku X 2025 – IX 2026 wobec 16 231 rok wcześniej.
  - Prawie jedna trzecia z nich (29%, czyli 7 268 osób, według przyjętej reguły przypisania źródła) przyszła z dwóch nowych kampanii na zwolnienie lekarskie (L4) w Meta i TikToku. Według reguły porównawczej (sesja płatności) to 21% (5 187 osób).
  - Poza tymi kampaniami nowych pacjentów przybyło o 7–20%, zależnie od reguły przypisania źródła.
- **Lepsza retencja: nie.**
  - Powrót w 90 dniach spadł z 23,9% do 17,4%, liczony na tych samych dniach kalendarzowych.
  - Marża na pacjenta w 90 dniach spadła z 66,6 zł do 58,3 zł.
  - Bez pacjentów nowych kampanii retencja też jest niższa: powrót w 90 dniach 22,0% albo 20,4%, zależnie od reguły przypisania.
  - Liczba osób, które wróciły w 90 dniach, rośnie (3 289 wobec 3 076). Spada odsetek, a nie liczba powracających.
- **Wynik:** w III kwartale 2026 marża była o 6,8% niższa niż rok wcześniej, choć wydatki na kampanie były 2,08 raza wyższe.
- **Dashboard liczy dane na surowo.** Zawiera 604 zdublowane zamówienia, zamówienia 22 kont testowych i przychód przed zwrotami. Po oczyszczeniu zamówienia rosną o 55,7% zamiast 61%, a przychód z konsultacji po zwrotach o 44,8% zamiast 50%. Nowi pacjenci prawie się nie zmieniają (+51,9% na surowo, +52,1% po oczyszczeniu), a sprzedaż TelemediGO wcale (+40,3%).

## Co robimy w pierwszym tygodniu

1. Naprawiamy zakładanie konta w Safari na iPhone'ach i iPadach (od 17.03.2026 konta powstają tam rzadziej): to największa pewna strata.
2. Wstrzymujemy kampanię TikTok na L4 i kampanię Google Ads na specjalistów jako pauzy, które da się cofnąć w jeden dzień: obie tracą w każdym wariancie rachunku.
3. Czyścimy codzienny raport (bez duplikatów, bez kont testowych, przychód po zwrotach) i sprawdzamy, czy lekarze dostają wynagrodzenie za wizyty testowe.
4. Robimy jednodniowe sprawdzenia: ręczny zakup po zalogowaniu, kliknięcia w panelach Meta i TikToka wobec sesji, co obiecują reklamy L4.
5. Zaczynamy diagnozę porannych opóźnień u internistów i przygotowujemy test kampanii Meta na L4 w parach województw.

## Jak używać narzędzia na co dzień

- **Kohorty:** kohorty dzienne z ostatnich dni, w podziale na źródło i pierwszą usługę. Najpierw powrót w 30 dniach u kohort, które mają już pełne okno, potem marża na pacjenta.
- **Lejek:** każdy krok dzień po dniu według przeglądarki i kampanii. Spadek jednego kroku w jednej przeglądarce to sygnał awarii, tak jak w Safari 17.03.2026.
- **Po zakupie:** punktualność porannych wizyt u internisty i zwroty po wizycie według kampanii.
- **Wynik biznesu:** marża po kosztach kampanii w czasie i wynik na pacjenta każdej kampanii według obu reguł przypisania źródła.
- **Zdarzenia:** czy zmiana, którą widać w kohortach albo w lejku, ma już datę i opis.

Pełna odpowiedź z zastrzeżeniami, lista 12 priorytetów (wartość w marży, sposób pomiaru, czas wdrożenia) i lista niewiadomych z testami są w narzędziu, w zakładkach „Czy to wzrost”, „Priorytety” i „Czego nie wiemy”. Ta sama treść jest w `notatki/c_szkic.md`.

## Co jest w narzędziu

| Zakładka | Co pokazuje |
|---|---|
| Czy to wzrost | odpowiedź na pytanie zadania, osobno dla pacjentów i dla retencji, z zastrzeżeniami |
| Kohorty | kohorty dzienne, powroty w 30, 60, 90 i 180 dniach, marża na pacjenta, macierz kohort i krzywa powrotu; filtry: źródło (dwie reguły), kampania, urządzenie, przeglądarka, pierwsza usługa, zniżka, TelemediGO, status i punktualność pierwszej wizyty |
| Lejek | od wejścia na stronę do płatności, dzień po dniu, w podziałach na urządzenie, przeglądarkę, kanał, kampanię i stronę wejścia |
| Po zakupie | punktualność wizyt według pory i specjalizacji, zwroty, anulacje, oceny |
| Zdarzenia | oś czasu zdarzeń znalezionych w danych (pozyskanie, lejek, retencja, obsługa pacjenta) |
| Wynik biznesu | przychód, koszt lekarza, kampanie i marża w czasie, kwartały rok do roku, ekonomia kampanii według dwóch reguł przypisania |
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
4. Dane strony narzędzia odtwarza `python -I analiza/b_eksport.py`. Uruchamia on też `analiza/b2_eksport_c.py`, który składa teksty zakładek „Czy to wzrost”, „Priorytety” i „Czego nie wiemy” z liczb w raportach. Oba sprawdzają liczby na stronie z raportami i notatkami.
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
- Sesje pacjentów zalogowanych od wejścia nigdy nie kończą się zakupem, choć według słownika danych powinny.
- Na kliknięcie reklamy w Meta i TikToku przypada wyraźnie mniej sesji niż w Google Ads.
- Wizyta u pediatry kosztuje pacjenta mniej niż wynosi koszt lekarza (przy założeniu, że pediatra to „inny specjalista” za 100 zł).
