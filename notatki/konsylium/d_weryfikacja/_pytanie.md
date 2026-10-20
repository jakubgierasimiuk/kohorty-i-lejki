# Brief dla konsylium: końcowa weryfikacja rozwiązania zadania rekrutacyjnego przed wysłaniem

## Cel

Sprawdzić całe rozwiązanie zadania rekrutacyjnego, zanim trafi do firmy, która je zleciła. Każdy członek zespołu ma dwie role naraz:

1. **Weryfikator:**
   - czy liczby zgadzają się między zakładkami narzędzia, README i notatkami;
   - czy definicje i rachunki są poprawne;
   - czy któryś wniosek mówi więcej, niż pokazują dane;
   - czy pominięto coś ważnego w kohortach, lejku, zdarzeniach, jakości danych, priorytetach albo niewiadomych.
2. **Osoba, która dała to zadanie i decyduje, czy kandydat się nadaje:**
   - co jest niejasne;
   - co nie przekonuje;
   - czego brakuje wobec tego, o co prosiło zadanie.

## Kontekst

- Zadanie dotyczy stanowiska szefa sprzedaży bezpośredniej do pacjentów (B2C) w firmie z konsultacjami lekarskimi online. Treść zadania jest w załączniku A.
- Dane obejmują dwa lata (1.10.2024 – 30.09.2026). Firma wygenerowała je na potrzeby zadania, więc nie opisują prawdziwych pacjentów.
- Kandydat oddaje trzy rzeczy:
  - działające narzędzie, czyli stronę w przeglądarce z dziewięcioma zakładkami (pełne teksty w załączniku C);
  - listę priorytetów (w narzędziu i w notatkach);
  - repozytorium ze śladem pracy (README w załączniku B).
- Kandydat pracował z AI. Analizę zrobił kodem (Python, DuckDB). Każdy krok sprawdzał drugi model, a listę priorytetów oceniała wcześniejsza runda kilku modeli.
- Założenia, znaleziska w danych i decyzje z całej pracy są w załączniku D. Najważniejsze zestawienia liczb z raportów są w załączniku E.

## Co sprawdzić

**Jako weryfikator:**
1. **Spójność liczb:** ta sama liczba w zakładkach (C), w README (B), w notatkach (D) i w raportach (E). Wypisz każdą rozbieżność z miejscem i obiema wartościami.
2. **Definicje i rachunki:**
   - nowy pacjent, powrót, źródło pozyskania (dwie reguły), przychód po zwrotach, marża, koszt lekarza, koszt pozyskania;
   - porównanie okresów na tych samych dniach kalendarzowych;
   - przeliczenia na pełny rok, scenariusze „naprawić albo wyłączyć”, próby testów.
   Gdzie się da, przelicz z liczb podanych w załącznikach.
3. **Wnioski ponad dane:** zdania o przyczynie, pewności, „wszystkie” i „zawsze”, uogólnienia z jednej grupy na całość.
4. **Pominięcia:** czego brakuje w kohortach, lejku, zdarzeniach, jakości danych, priorytetach albo niewiadomych, a co wynika z danych opisanych w załącznikach.

**Jako osoba, która zleciła zadanie:**
5. Porównaj rozwiązanie z wymaganiami z załącznika A, punkt po punkcie:
   - kohorty w rozdzielczości dziennej i zdarzenia znalezione w danych;
   - lejki: gdzie i od kiedy tracimy pacjentów;
   - narzędzie, na którym da się prowadzić biznes;
   - priorytety z wartością, sposobem pomiaru i czasem wdrożenia;
   - lista tego, czego nie da się rozstrzygnąć.
6. Co jest niejasne dla kogoś, kto czyta to pierwszy raz? Co nie przekonuje? Czego brakuje?
7. Twoja decyzja, gdybyś to Ty oceniał(a) kandydata, z uzasadnieniem: co przesądza na plus, a co na minus.

## Forma odpowiedzi

Po polsku, konkretnie.

1. **Lista poprawek od najważniejszej.** Przy każdej:
   - waga (krytyczna / ważna / drobna);
   - miejsce (zakładka i fragment, plik i sekcja);
   - co jest nie tak;
   - dowód (liczba z załącznika, Twoje przeliczenie, cytat do 15 słów);
   - propozycja poprawki.
2. **Co się potwierdziło:** liczby, definicje i wnioski, które sprawdziłeś(-aś) i które są poprawne.
3. **Ocena z perspektywy zlecającego:** trzy najmocniejsze strony, trzy najsłabsze, czego brakuje wobec zadania i Twoja decyzja z uzasadnieniem.

## Po czym poznać dobrą odpowiedź

- Każda uwaga wskazuje konkretne miejsce i da się ją sprawdzić. Ogólniki nie pomagają.
- Uwaga odróżnia błąd od stylu i od różnicy zdań.
- Przeliczenia pokazują, z jakich liczb wychodzą.
- Odpowiedź zaznacza, czego nie dało się sprawdzić z samych załączników.

## Ograniczenia i czego nie wiemy

- Oceniasz na podstawie załączników. Bazy danych nie masz (dwaj członkowie zespołu mają dostęp do plików i przeliczają liczby z bazy osobno).
- Zakładki narzędzia są w załączniku C jako tekst. Wykresów nie widać, a długie tabele są skrócone.
- Nie znamy oczekiwań firmy poza treścią zadania.
- W notatkach osoba prowadząca pracę nazywa się „kandydat”.

---


# Załącznik A — treść zadania (streszczenie i cytaty z zadania)

## 2. Kontekst biznesowy (z treści zadania)

- B2C to część Telemedi, w której pacjent płaci z własnej kieszeni na telemedi.com. Sprzedawane są konsultacje online i **TelemediGO** (program zniżkowy).
- Dane: dwa lata biznesu (1.10.2024 – 30.09.2026) — każda sesja na stronie, każdy krok lejka zakupowego, każde zamówienie, każdy zakup TelemediGO i każda złotówka wydana na kampanie. Źródła: analityka strony i system transakcyjny. **Nikt ich wcześniej nie czyścił.**
- Dashboard — ostatnie 12 miesięcy (X 2025 – IX 2026) wobec poprzednich 12 (X 2024 – IX 2025):
  - **+52%** pacjentów z pierwszym zakupem,
  - **+61%** zamówień,
  - **+50%** przychodu z konsultacji,
  - **+40%** sprzedanych TelemediGO.
- „Dla nas wzrost to dwie rzeczy naraz: więcej pacjentów i lepsza retencja. Chcemy wiedzieć, czy to, co widać na dashboardzie, jest wzrostem.”
- „Ten biznes prowadzimy na kohortach. Codziennie patrzymy, jak zachowują się kolejne kohorty, i chcemy rozumieć, które zdarzenie albo która nasza decyzja zmieniła ich zachowanie i wynik. To jest najważniejsza umiejętność w tej roli i najważniejsza część tego zadania.”

## 3. Czego oczekują (kolejność = waga)

1. **Analiza kohortowa — obowiązkowa i najważniejsza.** Kohorty w **rozdzielczości dziennej**, pocięte tak, żeby było widać, **co się wydarzyło, kiedy, i jak zmieniło zachowanie pacjentów i wynik biznesu**. Listy zmian w produkcie ani kalendarza kampanii nie dostajemy — **zdarzenia trzeba znaleźć w danych**.
2. **Lejki — obowiązkowe.** Od wejścia na stronę do płatności, w podziale, który pokazuje, **gdzie i od kiedy** tracimy pacjentów.
3. **Narzędzie, nie raport.** Kohorty i lejki zbudowane z AI jako działające narzędzie, na którym samemu prowadziłoby się ten biznes na co dzień. Ma działać na tych danych i otwierać się z linku.
4. **Lista priorytetów.** Co robimy po kolei, od najważniejszego. Każda pozycja wynika z danych i ma trzy rzeczy: **ile jest warta** (w złotych, z założeniami), **po czym poznamy, że zadziałała**, **ile zajmie wdrożenie**.
5. **Czego nie da się rozstrzygnąć.** Co z tych danych nie wynika i jakiego testu albo jakich informacji brakuje, żeby to domknąć.

## 4. Co oddajemy

| Element | Wymagania |
|---|---|
| **Link do narzędzia** | Działające, otwierane w przeglądarce **bez instalacji i bez zakładania konta**. Kohorty i lejki muszą w nim być. Stack dowolny. |
| **Lista priorytetów** | Od najważniejszego, z wartością, sposobem pomiaru i szacunkiem czasu wdrożenia każdej pozycji. Może być częścią narzędzia. |
| **Ślad pracy** | Repozytorium tego projektu (kod z historią zmian i notatki). |

## 5. Zasady Telemedi (dosłownie z zadania)

- **Nie rób slajdów.** Pokaż to, na czym faktycznie pracujesz.
- **Pracuj z AI tak, jak pracujesz na co dzień.** Nie oceniają wyboru narzędzi. Oceniają wnioski, to, co zbudujesz, i sposób, w jaki do tego dojdziesz.
- **Nie pytaj o definicje.** Jeśli czegoś brakuje, przyjmij założenie i je nazwij.
- **Jeśli coś w danych wygląda podejrzanie, powiedz o tym.** To też jest odpowiedź.
- **Dane są wygenerowane na potrzeby zadania.** Nie opisują prawdziwych pacjentów ani wyników Telemedi; skala, kampanie i koszty są fikcyjne.

---

## 6. Dane

Paczka `telemedi-b2c-dane.zip` (~14 MB spakowane, 84 MB po rozpakowaniu): 17 plików CSV + `README.md` (słownik danych). Razem 1 082 369 wierszy. Okres 1.10.2024 – 30.09.2026.

**Strefy czasowe:** sesje i zdarzenia (analityka strony) — **UTC**. Pozostałe tabele (system transakcyjny) — **czas polski**. Kohorty dzienne liczymy w czasie polskim (Europe/Warsaw, ze zmianą czasu letni/zimowy).

**Źródła pozyskania pacjenta nie ma w żadnej tabeli** — trzeba je wyprowadzić z sesji i samemu zdecydować, jak je przypisać (reguła zapisana w `notatki/ZALOZENIA.md`).

| Plik | Wiersze | Jeden wiersz to | Kolumny |
|---|---|---|---|
| `users.csv` | 52 422 | konto pacjenta | user_id, registered_at, birth_year, gender (K/M), region (województwo), city_size (wieś albo miasto w trzech przedziałach), marketing_consent (1 = zgoda) |
| `sessions_2024q4.csv` … `sessions_2026q3.csv` (8 plików) | 459 557 | sesja na telemedi.com (UTC) | session_id, visitor_id (cookie; pacjent może mieć kilka), user_id (tylko gdy zalogowany), started_at_utc, utm_source (puste = wejście bezpośrednie), utm_medium, utm_campaign, device (mobile/desktop/tablet), os, browser (Instagram, Facebook, TikTok = przeglądarki wbudowane w aplikacje), landing_page |
| `events_2024h2.csv` … `events_2026h2.csv` (5 plików) | 494 605 | krok lejka (UTC) | session_id, event_name (kolejno: service_selected, slot_selected, account_completed — logowanie albo rejestracja, payment_started, payment_succeeded), event_at_utc. Sesja bez zdarzeń = pacjent nie wybrał usługi. |
| `orders.csv` | 65 882 | opłacone zamówienie konsultacji | order_id, user_id, session_id, created_at (moment płatności), specialization (internista, pediatra albo jeden z ośmiu specjalistów), visit_purpose (konsultacja, e_recepta, l4, skierowanie), consultation_mode (phone, chat, video), scheduled_at, started_at (faktyczny start wizyty), duration_min, list_price, discount_type (none, go, promo), promo_code, amount_paid (bez opłaty za GO), payment_method (blik, card, transfer), status (completed; cancelled — przed wizytą, pełny zwrot; no_show — pacjent nie odebrał, bez zwrotu; refunded — wizyta odbyta, zwrot po niej), refund_amount, rating (1–5, większość nie ocenia) |
| `go_memberships.csv` | 4 227 | zakup TelemediGO | membership_id, user_id, purchased_at, valid_until, amount_paid (89.00), order_id (puste = kupione osobno), session_id |
| `marketing_spend.csv` | 5 676 | dzień × kampania płatna za klik | date (czas polski), utm_source, utm_medium, utm_campaign, impressions, clicks, spend_pln (netto) |

**Zasady biznesowe podane w zadaniu:**
- **TelemediGO:** jednorazowo 89 zł za 12 miesięcy; 50% zniżki na wizyty u internisty (w tym e-recepta, L4, skierowanie) i 20% u pozostałych specjalistów. Kupowane przy kasie z konsultacją albo osobno. **Nie odnawia się samo.**
- **Koszt lekarza** (nie ma go w danych; do liczenia marży): za każdą odbytą wizytę 25 zł internista, 200 zł psychiatra, 100 zł każdy inny specjalista. **Lekarz dostaje wynagrodzenie także za wizytę, za którą zwrócono pacjentowi opłatę.**
- **Afiliacja:** prowizja 25 zł za pierwsze opłacone zamówienie pacjenta; nie ma jej w `marketing_spend.csv`.
- Koszt e-maili i SMS-ów pomijamy.

Szczegóły i dodatkowe objaśnienia: `dane/README.md` (czytać dopiero po kontroli bezpieczeństwa — patrz punkt 7).

---

# Załącznik B — README repozytorium

# Telemedi B2C: czy to, co widać na dashboardzie, jest wzrostem?

Rozwiązanie zadania rekrutacyjnego na stanowisko Head of B2C. Dane to dwa lata biznesu B2C (1.10.2024 – 30.09.2026), wygenerowane na potrzeby zadania.

**Narzędzie:** `https://<organizacja>.github.io/<repozytorium>/` — adres uzupełnimy w dniu publikacji. Strona otwiera się w przeglądarce, bez instalacji i bez konta.

## Odpowiedź w skrócie

**Nie: w rozumieniu Telemedi („więcej pacjentów i lepsza retencja naraz”) to nie jest wzrost.** Z dwóch warunków spełniony jest tylko pierwszy.

- **Więcej pacjentów: tak.**
  - Pacjentów z pierwszym zakupem jest o 52,1% więcej: 24 687 w roku X 2025 – IX 2026 wobec 16 231 rok wcześniej.
  - Prawie jedna trzecia z nich (29%) przyszła z dwóch nowych kampanii na zwolnienie lekarskie (L4) w Meta i TikToku.
  - Poza tymi kampaniami nowych pacjentów przybyło o 7–20%, zależnie od reguły przypisania źródła.
- **Lepsza retencja: nie.**
  - Powrót w 90 dniach spadł z 23,9% do 17,4%, liczony na tych samych dniach kalendarzowych.
  - Marża na pacjenta w 90 dniach spadła z 66,6 zł do 58,3 zł.
  - Bez pacjentów nowych kampanii retencja też jest niższa: powrót w 90 dniach 22,0% albo 20,4%, zależnie od reguły przypisania.
  - Liczba osób, które wróciły w 90 dniach, rośnie (3 289 wobec 3 076). Spada odsetek, a nie liczba powracających.
- **Wynik:** w III kwartale 2026 marża była o 6,8% niższa niż rok wcześniej, choć wydatki na kampanie były 2,08 raza wyższe.
- **Dashboard liczy dane na surowo.** Zawiera 604 zdublowane zamówienia, zamówienia 22 kont testowych i przychód przed zwrotami. Po oczyszczeniu zamówienia rosną o 55,7% zamiast 61%, a przychód z konsultacji po zwrotach o 44,8% zamiast 50%.

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
| `notatki/konsylium/` | ocena listy priorytetów przez kilka modeli AI różnych firm i jej wynik |
| `bezpieczenstwo/` | kontrola paczki z danymi przed rozpakowaniem i raporty z niej |

Surowych danych, paczki i bazy danych nie ma w repozytorium.

## Jak odtworzyć liczby

1. Python 3.13 z pakietami `duckdb` 1.5.5, `pandas` 2.3.3 i `pyarrow`.
2. Rozpakowane pliki CSV z zadania w folderze `dane/`.
3. Z głównego folderu repozytorium uruchom kolejno skrypty z tabeli w `analiza/README.md`, zawsze przez `python -I`. Pierwsze dwa budują bazę: `python -I analiza/a1_baza.py`, potem `python -I analiza/a2_czyste.py`. Każdy następny skrypt tylko czyta bazę i zapisuje raport do `analiza/wyniki/`.
4. Dane strony narzędzia odtwarza `python -I analiza/b_eksport.py`. Skrypt sprawdza liczby na stronie z raportami i notatkami.
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


# Załącznik C — pełne teksty zakładek narzędzia

# Teksty strony narzędzia — wszystkie zakładki, tak jak widzi je czytelnik

Wygenerowane 2026-10-20 21:38 skryptem `analiza/b2_teksty_strony.py` ze strony w `narzedzie/` (stan repozytorium 1c874ef), otwartej w przeglądarce bez okna (Microsoft Edge), szerokość 1366 px. Każda zakładka przy ustawieniach domyślnych, bez klikania. Tabele dłuższe niż 40 wierszy są skrócone do 15 pierwszych i 5 ostatnich wierszy. Rozwijane sekcje są rozwinięte. Wykresy opisane nazwami serii. W komórkach tabel `<br>` oddziela linie, które strona pokazuje jedna pod drugą (zwykle: wartość w okresie B, pod spodem okres A i zmiana). Odnośniki do innych zakładek są oznaczone strzałką albo wypisane po „Zobacz w danych”.

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
| 180 dni | 27,5% (9 125 pacjentów) | 22,2% (12 591 pacjentów) | −5,3 pkt proc. |

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

1. Dashboard liczy dane na surowo. Zawiera 604 zdublowane zamówienia z 10–24.06.2026, 2 071 zamówień kont testowych i przychód przed zwrotami. Po oczyszczeniu zamówienia rosną o 55,7% (24 716 → 38 491) zamiast 61%, a przychód z konsultacji po zwrotach o 44,8% zamiast 50%. Nowi pacjenci (+52%) i TelemediGO się nie zmieniają.
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

Większość spadku powrotów wiąże się z pacjentami dwóch nowych kampanii na L4, ale w kampaniach działających w obu latach też jest spadek, którego sprawdzone cechy nie tłumaczą. Podział zależy od reguły źródła, dlatego obie reguły są do wyboru w filtrach.

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
- Kohorty: tygodniowe (do wyboru: tygodniowe / miesięczne)

*Wiersz to kohorta (nowi pacjenci z tego samego tygodnia albo miesiąca pierwszego zakupu), kolumna to okno: odsetek pacjentów kohorty, którzy wrócili w ciągu tylu dni. Kolor: ciemniej znaczy wyżej, skala osobno w każdej kolumnie. Kropka oznacza kohortę bez pełnego okna. Kolumna „Zdarzenia” podaje numery zdarzeń z osi, które wypadają w tej kohorcie. Te same filtry co wyżej, bez podziału na serie.*

| Kohorta (tydzień od) | Nowi pacjenci | Zdarzenia | 7 dni | 14 dni | 30 dni | 60 dni | 90 dni | 180 dni |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.10.2024 | 198 |  | 3,5 | 6,1 | 10,6 | 15,7 | 21,7 | 23,7 |
| 7.10.2024 | 296 |  | 1,7 | 6,1 | 12,2 | 20,3 | 25,0 | 28,0 |
| 14.10.2024 | 291 |  | 1,7 | 4,8 | 9,6 | 18,6 | 23,4 | 27,1 |
| 21.10.2024 | 309 |  | 1,0 | 3,2 | 7,4 | 14,6 | 16,5 | 21,4 |
| 28.10.2024 | 281 |  | 0,7 | 5,3 | 12,1 | 19,2 | 24,9 | 27,8 |
| 4.11.2024 | 352 |  | 2,3 | 6,8 | 12,2 | 21,6 | 26,4 | 30,4 |
| 11.11.2024 | 320 |  | 1,3 | 3,4 | 8,1 | 16,6 | 22,5 | 25,9 |
| 18.11.2024 | 344 |  | 1,5 | 6,7 | 11,6 | 20,3 | 24,4 | 27,3 |
| 25.11.2024 | 338 |  | 2,1 | 7,4 | 12,1 | 21,0 | 24,0 | 27,8 |
| 2.12.2024 | 361 |  | 1,4 | 5,0 | 9,7 | 18,3 | 23,5 | 26,6 |
| 9.12.2024 | 353 |  | 2,8 | 6,5 | 15,0 | 21,5 | 24,9 | 28,3 |
| 16.12.2024 | 375 |  | 0,8 | 5,6 | 11,7 | 18,9 | 24,5 | 27,7 |
| 23.12.2024 | 275 |  | 4,0 | 8,4 | 13,8 | 22,5 | 28,7 | 29,8 |
| 30.12.2024 | 327 |  | 2,1 | 5,5 | 13,1 | 22,6 | 28,4 | 32,7 |
| 6.01.2025 | 360 |  | 1,9 | 5,8 | 10,8 | 19,4 | 25,6 | 28,3 |
| … pominięto 85 wierszy, tabela ma ich 105 … |  |  |  |  |  |  |  |  |
| 31.08.2026 | 462 |  | 1,1 | 4,1 | · | · | · | · |
| 7.09.2026 | 434 |  | 1,2 | 2,8 | · | · | · | · |
| 14.09.2026 | 478 |  | 1,5 | · | · | · | · | · |
| 21.09.2026 | 492 |  | · | · | · | · | · | · |
| 28.09.2026 | 245 |  | · | · | · | · | · | · |

### Krzywa powrotu według dnia od pierwszego zakupu: okres A i okres B

*Dla każdego dnia od pierwszego zakupu: odsetek pacjentów, którzy do tego dnia wrócili. Na każdy dzień bierzemy tylko kohorty, które ten dzień już osiągnęły, a okres A obcinamy tak samo jak w tabeli. Legenda pod kursorem pokazuje liczbę pacjentów i poziom B jako odsetek poziomu A.*

*[Wykres] serie: Okres A (1.10.2024–30.09.2025); Okres B (1.10.2025–30.09.2026)*

*Jak liczymy: nowy pacjent to konto z pierwszym opłaconym zamówieniem, bez względu na status. Źródło pozyskania według przyjętej reguły (pierwsze wejście pacjenta, także anonimowe sesje jego przeglądarek, a kod kampanii na pierwszym zamówieniu rozstrzyga) albo według sesji płatności. Urządzenie i przeglądarka z sesji płatności. Pierwsza usługa: internista według celu wizyty, pediatra, psychiatra, inny specjalista. Opóźnienie i pora z pierwszej wizyty. Źródło danych: analiza/definicje.py, analiza/a5r_kohorty.py, eksport analiza/b_eksport.py.*

# Zakładka 3: Lejek (`#lejek`)

## Lejek: od wejścia na stronę do płatności

Konwersja sesji do płatności spadła z 16,0% w okresie X 2024 – IX 2025 (154 085 sesji, 24 717 płatności) do 13,7% w okresie X 2025 – IX 2026 (280 625 sesji, 38 490 płatności).

Rachunkowo prawie cały spadek to zmiana ruchu. Udział przeglądarek wbudowanych w aplikacje Instagram, Facebook i TikTok wzrósł z 10,7% do 35,6% sesji. Sama zmiana struktury ruchu według przeglądarki daje −3,00 punktu procentowego, a zmiana konwersji w obrębie przeglądarek +0,67 punktu procentowego.

To jednak nie jest tylko „inny ruch”. Dwie rzeczy trzeba naprawić na stronie:

#### Safari na iPhone'ach i iPadach: od 17.03.2026 nie działa zakładanie konta

Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spadł z 66,2% (1 763 sesje z wyborem terminu, 16.01.2026–16.03.2026) do 45,1% (1 553 sesje, 17.03.2026–15.05.2026). Pozostałe przeglądarki w tych samych dniach: 64,8% i 63,4%. Szacunek: 628–695 utraconych pierwszych zamówień do 30.09.2026, czyli 95–105 na 30 dni.

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
12. 17.03.2026: Safari na iOS: przestaje działać zakładanie konta
13. 10.06.2026: Duplikaty zamówień w eksporcie

*Jak liczymy: lejek główny obejmuje sesje zwykłe, czyli bez konta na wejściu albo z kontem, które pojawia się dopiero na kroku logowania. Sesje zalogowane od wejścia i zakupy samego TelemediGO są osobnymi typami sesji. „Jeszcze nie kupowali” to osoby bez zakupu przed początkiem sesji, także na koncie, na które logowały się w tej samej przeglądarce. Dzień sesji liczymy w czasie polskim. Źródło danych: analiza/a5p_lejek.py, eksport analiza/b_eksport.py.*

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
| Do 5 minut po terminie | 31,3% z 11 007<br>A: 31,9% z 10 534 ▼0,6 | 4,45% z 3 446<br>A: 4,47% z 3 361 ▼0,02 | 1,1% z 3 446<br>A: 1,2% z 3 361 ▼0,2 |
| Ponad 5 do 15 minut | 30,8% z 6 198<br>A: 33,4% z 5 394 ▼2,6 | 4,38% z 1 909<br>A: 4,37% z 1 802 ▲0,01 | 1,5% z 1 909<br>A: 1,7% z 1 802 ▼0,3 |
| Ponad 15 do 30 minut | 31,7% z 1 786<br>A: 30,3% z 492 ▲1,4 | 3,69% z 566<br>A: 3,82% z 149 ▼0,13 | 8,7% z 566<br>A: 6,7% z 149 ▲1,9 |
| Ponad 30 minut | 30,3% z 1 550<br>A: 33,3% z 132 ▼3,1 | 2,92% z 469<br>A: 2,95% z 44 ▼0,03 | 31,8% z 469<br>A: 31,8% z 44 = 0,0 |

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

Zobacz w jakości danych

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

Zobacz w jakości danych

*6. 13.11.2025 · Obsługa pacjenta · zmiana obsługi pacjenta*

### Więcej pierwszych zamówień zwracanych po wizycie

**Co się zmieniło:**
Rośnie odsetek pierwszych zamówień, za które pacjent dostaje zwrot po odbytej wizycie. Skupia się w wizytach L4 pacjentów nowych kampanii. Lekarz dostaje wynagrodzenie także za te wizyty.

**O ile:**
2,1% od 1.10.2024 (18 260 pacjentów) → 3,9% od 13.11.2025 (7 142 pacjentów) → 6,9% od 23.02.2026 (15 516 pacjentów).

**Skąd wiemy:**
Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. Daty to kandydaci zmian, nie potwierdzone zdarzenia.

Zobacz w jakości danych

*7. 24.11.2025 · Obsługa pacjenta · zmiana obsługi pacjenta*

### Poranne wizyty u internisty zaczynają się z opóźnieniem

**Co się zmieniło:**
Rośnie odsetek wizyt u internisty z terminem 6:00–11:59, które zaczynają się ponad 15 minut po terminie, także u pacjentów spoza nowych kampanii. Przy tym samym porannym ruchu opóźnień jest teraz dużo więcej niż rok wcześniej, więc spadła poranna przepustowość (bez przesądzania przyczyny).

**O ile:**
6,3% od 1.10.2024 (6 148 wizyt) → 27,8% od 24.11.2025 (615 wizyt) → 41,9% od 26.12.2025 (730 wizyt) → 50,2% od 2.02.2026 (4 248 wizyt).

**Skąd wiemy:**
Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. Seria: wizyty u internisty rano, pacjenci spoza nowych kampanii. Daty to kandydaci zmian, nie potwierdzone zdarzenia.

Zobacz w jakości danych

*8. 1.01.2026 · Lejek · zmiana stopniowa*

### Remarketing Meta słabnie, bo zmienia się pula odbiorców

**Co się zmieniło:**
Remarketing wraca coraz częściej do osób, które pierwszy raz przyszły z Meta i TikToka, a rzadziej do osób z wyszukiwarki. Te osoby płacą rzadziej. W obrębie źródła pierwszej wizyty konwersja stoi.

**O ile:**
Płatność na sesję u osób, które jeszcze nie kupowały: 28,2% w IV kwartale 2025 (1 011 sesji), 18,9% w II kwartale 2026 (1 603 sesje) i 19,1% w III kwartale 2026 (1 534 sesje). Udział przeglądarek w aplikacjach w tym ruchu rośnie z 13,3% do 22,1–23,4%. Osoby, które pierwszy raz przyszły z Google albo Bing: 27,9% w okresie X 2024 – IX 2025 i 26,7% w 2026; z Meta (pozyskanie): 11,5% i 13,2%.

**Skąd wiemy:**
Metoda wykrywania zmian wskazała 20.03.2026 jako dzień zmiany poziomu płatności na sesję (27,3% → 19,1%), ale zmiana narasta od początku 2026. Źródło: analiza/a5p_zdarzenia.py, sekcje 5h i 5i; notatki/a5_pozyskanie.md, punkt 2.5.

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
Powrót w 30 dniach całej kohorty spada skokowo w dniu startu kampanii TikTok na L4. To głównie skład pacjentów (rosnący udział nowych kampanii), co pokazuje krok 3 analizy retencji.

**O ile:**
9,7% (12 514 pacjentów, 5.06.2025–9.02.2026) → 6,9% (14 536 pacjentów, 10.02.2026–31.08.2026). Wcześniejszy kandydat 5.06.2025: 11,4% → 9,7%; wypada w pierwszym roku, więc może być porą roku.

**Skąd wiemy:**
Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. Daty to kandydaci zmian, nie potwierdzone zdarzenia.

Zobacz w jakości danych

*11. 2.03.2026 · Retencja · kandydat poniżej progu*

### Powrót w 90 dniach w kampaniach działających w obu latach: brak wyraźnego skoku

**Co się zmieniło:**
W kampaniach obecnych w obu latach powrót też spada, ale metoda nie znalazła zmiany skokowej powyżej progu. Najsilniejszy kandydat to ten dzień. Brak skoku nie znaczy, że spadek musi być rozłożony w czasie.

**O ile:**
23,3% przed (24 511 pacjentów) i 20,9% po (5 751 pacjentów, kohorty z pełnym oknem 90 dni).

**Skąd wiemy:**
Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. Luty 2026 nie pasuje do prostej hipotezy przeciążenia (opóźnienia już wysokie, powrót bez spadku), to trop eksploracyjny.

Zobacz w jakości danych

*12. 17.03.2026 · Lejek · awaria*

### Safari na iOS: przestaje działać zakładanie konta

**Co się zmieniło:**
U osób, które jeszcze nie kupowały, krok logowania albo zakładania konta po wyborze terminu spada w Safari na iPhone'ach i iPadach i zostaje niski do końca danych. Psuje się zakładanie nowego konta, a logowanie do istniejącego działa.

**O ile:**
Z 66,2% (1 763 sesje z wyborem terminu w 60 dniach przed) do 45,1% (1 553 sesje w 60 dniach po). Pozostałe przeglądarki: 64,8% i 63,4%. Szacunek: 628–695 utraconych pierwszych zamówień w 198 dniach do 30.09.2026, czyli 95–105 na 30 dni.

**Skąd wiemy:**
Metoda wykrywania zmian w seriach dziennych (podział binarny) wskazała ten dzień. Sprawdzenie na bazie: spadek jest w każdym kanale, więc to nie zmiana struktury ruchu. Przyczyny w danych nie widać. Źródło: analiza/a5p_zdarzenia.py, sekcja 5; notatki/a5_pozyskanie.md, punkt 2.1.

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

*Wynik na pacjenta to marża na pacjenta w 90 albo 180 dniach minus koszt pozyskania (wydatki na kampanię albo prowizja afiliacyjna na nowego pacjenta). Obie reguły źródła stoją obok siebie. Liczymy kohorty z pełnym oknem, a wydatki z tych samych dni. Pod wynikiem: marża, liczba pacjentów i przedział warunkowy.*

| Grupa | Przyjęta reguła źródła — Nowi pacjenci | Przyjęta reguła źródła — Koszt pozyskania na pacjenta | Przyjęta reguła źródła — Wynik na pacjenta, 90 dni | Przyjęta reguła źródła — Wynik na pacjenta, 180 dni | Sesja płatności — Nowi pacjenci | Sesja płatności — Koszt pozyskania na pacjenta | Sesja płatności — Wynik na pacjenta, 90 dni | Sesja płatności — Wynik na pacjenta, 180 dni | Ocena |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nowe kampanie na L4 (Meta i TikTok) | 4 893 | 32,7 zł | +3,6 zł<br>marża 36,3 zł, 4 893 pac. | +7,0 zł<br>marża 37,3 zł, 2 352 pac. | 3 510 | 45,6 zł | −9,4 zł<br>marża 36,1 zł, 3 510 pac. | −5,2 zł<br>marża 36,9 zł, 1 693 pac. | niepewny: znak zależy od reguły |
| Pozostałe kampanie płatne | 7 076 | 44,2 zł | +20,0 zł<br>marża 64,2 zł, 7 076 pac. | +29,7 zł<br>marża 72,3 zł, 5 130 pac. | 7 141 | 43,8 zł | +18,7 zł<br>marża 62,4 zł, 7 141 pac. | +27,5 zł<br>marża 71,0 zł, 5 029 pac. |  |
| Afiliacja (ranking lekarzy) | 489 | 25,0 zł | +32,2 zł<br>marża 57,2 zł, 489 pac. | +37,0 zł<br>marża 62,0 zł, 352 pac. | 319 | 25,0 zł | +30,8 zł<br>marża 55,8 zł, 319 pac. | +35,6 zł<br>marża 60,6 zł, 229 pac. |  |
| Kanały bezpłatne | 6 466 | 0,0 zł | +68,6 zł<br>marża 68,6 zł, 6 466 pac. | +78,1 zł<br>marża 78,1 zł, 4 757 pac. | 7 954 | 0,0 zł | +64,5 zł<br>marża 64,5 zł, 7 954 pac. | +74,2 zł<br>marża 74,2 zł, 5 640 pac. |  |

*Źródło danych: analiza/definicje.py (koszt lekarza, marża), analiza/a5e_ekonomia.py (ekonomia kampanii), eksport analiza/b_eksport.py.*

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
- Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spada z 66,1% do 45,6% i nie wraca (od 1.10.2025 do 16.03.2026 wobec 17.03–30.09.2026; po awarii 4 678 sesji z wyborem terminu).
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
- Wizyty spóźnione ponad 30 minut mają średnią ocenę 2,9 wobec 4,5 przy punktualnych (okres 2, pacjenci spoza nowych kampanii, 1 550 i 11 007 wizyt). Rano spada powrót po wizytach spóźnionych.

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

**Stopka strony:** Dane od 1.10.2024 do 30.09.2026. Liczby przeliczone 2026-10-20 15:07 skryptami analiza/b_eksport.py i analiza/b2_eksport_c.py (stan repozytorium cfa8c57). Strona nie pobiera niczego z internetu.


# Załącznik D — notatki/ZALOZENIA.md

# Założenia

Każde założenie przyjęte tam, gdzie zadanie nie daje definicji (zasada Telemedi: „nie pytaj o definicje — przyjmij założenie i je nazwij”). Przy każdym: co zakładamy, dlaczego, jaki ma wpływ na wynik.

## 2026-10-19 — baza danych i czas (punkt A1)

1. **Dane w bazie są surowe.** Baza `analiza/telemedi.duckdb` (schemat `surowe`) zawiera wszystkie wiersze z 17 plików CSV, bez deduplikacji i bez filtrów. README mówi wprost, że eksport jest surowy. Czyszczenie to osobny krok (punkt A2), żeby każdą decyzję o usunięciu wiersza dało się pokazać i policzyć jej wpływ.
2. **Puste pole = brak wartości (NULL).** Dotyczy to też źródła wejścia: puste `utm_source`, `utm_medium` i `utm_campaign` oznaczają wejście bezpośrednie (tak mówi README).
3. **Sesje i zdarzenia przeliczamy z UTC na czas polski (Europe/Warsaw).** Dzień sesji i zdarzenia to dzień według czasu polskiego (kolumna `dzien_pl`). Przeliczenie uwzględnia cztery zmiany czasu, które wypadają w okresie danych: 27.10.2024, 30.03.2025, 26.10.2025 i 29.03.2026. Wpływ: 2,1% sesji i 2,5% zdarzeń trafia do innego dnia niż według UTC. To są wejścia po 22:00 albo 23:00 czasu polskiego, które w UTC wypadają jeszcze poprzedniego dnia.
4. **Tabele z systemu transakcyjnego bierzemy jako czas polski, bez przeliczania.** Dotyczy to kont pacjentów (`users`), zamówień (`orders`) i zakupów TelemediGO (`go_memberships`). Tak mówi README. Sprawdzimy to w punkcie A2: porównamy moment płatności w zamówieniu z krokiem `payment_succeeded` w analityce po przeliczeniu strefy.
5. **Czas trwania i kolejność kroków w analityce liczymy na kolumnach UTC, nie na czasie polskim.** W noc zmiany czasu z letniego na zimowy godzina 2:00–3:00 czasu polskiego występuje dwa razy. Różnica dwóch czasów polskich z tej nocy byłaby błędna o godzinę. W kolumnach UTC tego problemu nie ma.

## 2026-10-19 — czyszczenie danych (punkt A2, przyjęte z kandydatem)

Oczyszczone dane są w schemacie `czyste` bazy, budowanym skryptem `analiza/a2_czyste.py`. Wszystkie dalsze liczby (kohorty, lejki, przychód, marża) liczymy na `czyste`. Na danych surowych liczymy tylko odtworzenie dashboardu (punkt A3).

6. **Zdublowane zamówienia: zostaje jedna kopia.** 604 zamówienia z okna 10–24.06.2026 mają dwie identyczne kopie. Traktujemy to jako błąd eksportu, a nie jako podwójne płatności, bo w analityce każde z nich ma tylko jeden krok płatności. Wpływ: drugi rok dashboardu traci 604 zamówienia i 45 805 zł zapłat po zwrotach.
7. **Konta testowe są wyłączone ze wszystkiego.** Konto testowe to konto, które choć raz użyło kodu TEST-QA (22 konta). Ten sam zbiór wyznaczają zamówienia trwające 1 minutę. Wyłączamy wszystkie ich zamówienia (2 071, także 290 bez kodu), same konta, sesje (2 093) i zdarzenia lejka. Wpływ: 553 zamówienia mniej w pierwszym roku dashboardu i 1 518 w drugim. **Na końcu pracy przyglądamy się testom jeszcze raz dokładnie** (punkt D w planie).
8. **Za wizyty testowe nie liczymy kosztu lekarza.** Wizyta testowa trwa 1 minutę i wygląda na test systemu, a nie na pracę lekarza. Wariant z kosztem według zasady z zadania (25 zł za odbytą wizytę u internisty, razem 51 775 zł) trafia na listę rzeczy, których nie da się rozstrzygnąć.
9. **Drobne niespójności zostają w danych, z adnotacją w `ZNALEZISKA.md`.** Dotyczy to godziny bez danych (17.05.2025 13:00–14:00), 24 zamówień „psycholog + e-recepta”, jednego zamówienia bez zniżki mimo aktywnego TelemediGO i niespójnych oznaczeń programu poleceń. Żadna z nich nie zmienia wyników w widoczny sposób.

## 2026-10-19 — trzy otwarte sprawy z A2 (przyjęte z kandydatem)

Wyliczenia: `analiza/a2_dyskusja.py`, wynik w `analiza/wyniki/a2_dyskusja.txt`.

10. **Sesja zalogowana od wejścia** = sesja, w której jest konto pacjenta, nie ma kroku `account_completed` i nie jest to zakup samego TelemediGO (w danych oczyszczonych 22 068 sesji). W lejku pokazujemy ją jako osobny wiersz. To rozpoznanie pośrednie: w danych nie ma informacji, czy pacjent był zalogowany w chwili wejścia.
11. **Newsletter i SMS oceniamy na poziomie pacjenta**, czyli po tym, czy pacjent wraca w ciągu kilku dni od kontaktu, a nie po konwersji sesji. Okno ustalimy w A4.
12. **Nie wyznaczamy osobnego okresu rozruchu.** Nowi pacjenci od pierwszego tygodnia są na zbliżonym poziomie: 198 w pierwszym, 6-dniowym tygodniu, potem około 300 tygodniowo w październiku 2024. Od zera rośnie tylko baza powracających: zamówienia powtórne rosną z 2 w pierwszym tygodniu do 224 tygodniowo pod koniec marca 2025. Start od zera obsługujemy rozbiciem na nowych i powracających oraz porównaniem kohort w tym samym wieku. Sprawdzamy, czy wnioski o retencji trzymają się bez kohort z października 2024. **Przyczyna wzrostu liczby nowych pacjentów od października 2024 do stycznia 2025 jest otwarta**, bo w tym samym czasie rosną wydatki na kampanie. Sezon i wydatki rozdzielamy w A5.
13. **START10 to stały kod dla nowych pacjentów** (10 zł na pierwszym zamówieniu, przez całe dwa lata), czyli zwykła zniżka pozyskania, a nie znacznik okresu startu.
14. **Zniżkę liczymy w złotych** jako cenę katalogową minus zapłatę (`list_price − amount_paid`). Kody rabatowe obniżają cenę o stałą kwotę, TelemediGO o 50% u internisty i o 20% u pozostałych.
15. **Prowizję afiliacyjną liczymy tą samą regułą, którą w A4 wybierzemy dla źródła pozyskania.** Obok pokazujemy jedną liczbą drugi wariant, czyli prowizję za pierwsze zamówienia z kodem RANKING10. Punkt wyjścia: 842 pierwsze zamówienia zapłacone w sesji z rankingu wobec 595 zamówień z kodem RANKING10.

## 2026-10-19 — definicje przed kohortami (punkt A4, przyjęte z kandydatem)

Warianty i ich wpływ: `analiza/a4_definicje.py`, wynik w `analiza/wyniki/a4_definicje.txt` (sekcje 1–5 to warianty, sekcja 6 to liczby według przyjętych definicji). Przykłady pojedynczych pacjentów do ręcznej kontroli kodu: `analiza/wyniki/a4_przyklady.txt`. Okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026. Uzasadnienia wyborów: `DECYZJE.md`.

16. **Nowy pacjent = konto z pierwszym opłaconym zamówieniem konsultacji, bez względu na jego status.** Dzień wejścia do kohorty to dzień płatności tego zamówienia (`created_at`, czas polski).
    - **Na czym to opieramy.** Zadanie nie definiuje nowego pacjenta wprost. Są trzy pośrednie podstawy i wszystkie wskazują ten wariant: (a) miara na dashboardzie to „pacjenci z pierwszym zakupem”; (b) słownik danych mówi, że każdy wiersz `orders.csv` to opłacone zamówienie konsultacji; (c) słownik danych przyznaje prowizję afiliacyjną „za każde pierwsze opłacone zamówienie pacjenta, także wtedy, gdy zostało potem anulowane albo zwrócone”. Zasada Telemedi: „nie pytaj o definicje — przyjmij założenie i je nazwij”.
    - **Wpływ:** 16 231 nowych pacjentów w okresie 1 i 24 687 w okresie 2, czyli +52,1%. Warianty odrzucone: pierwsze zamówienie nieanulowane (1 432 pacjentów mniej, +51,8%) i pierwsza odbyta wizyta (2 295 pacjentów mniej, +51,6%). Wariant „pierwsza jakakolwiek płatność, także samo TelemediGO” daje dokładnie to samo, bo nikt nie kupił samego TelemediGO przed pierwszą konsultacją. Żaden wariant nie zmienia udziału kanału o więcej niż 0,3 punktu procentowego.
17. **Status pierwszego zamówienia to osobny podział kohort** (odbyte, anulowane, nieodebrane, zwrócone po wizycie). Powód: mocno różnicuje powroty. Powrót w 90 dniach (punkt 19) w okresie 1: 24,5% po odbytej wizycie, 17,6% po anulowanej, 16,2% po nieodebranej i 5,0% po zwróconej po wizycie.
18. **Nie łączymy kont po przeglądarce.** Żadna z 57 473 przeglądarek nie należy do dwóch kont, więc łączenie nic by nie zmieniło. Przeglądarka służy tylko do dołączania anonimowych sesji do konta przy źródle pozyskania (punkt 22).
19. **Powrót = kolejne zamówienie tego samego pacjenta, które nie zostało anulowane** (status odbyte, nieodebrane albo zwrócone po wizycie), najpóźniej N-tego dnia kalendarzowego po dniu wejścia do kohorty, w oknach 30, 60 i 90 dni.
    - Anulowane zamówienie nie jest powrotem: to pełny zwrot przed wizytą, pacjent nic nie kupił. Nieodebrana wizyta jest powrotem, bo pacjent zapłacił, a pieniądze zostają.
    - Powrót liczymy tylko dla kohort z pełnym oknem: 30 dni — kohorty do 31.08.2026, 60 dni — do 1.08.2026, 90 dni — do 2.07.2026.
    - W danych nie ma dwóch zamówień jednego pacjenta tego samego dnia (najkrótsza przerwa to 1 474 minuty), więc sprawa „powrotu tego samego dnia” nie powstaje.
    - **Wpływ:** powrót w 90 dniach 23,6% w okresie 1 i 17,4% w okresie 2. Dla porównania: każde kolejne opłacone zamówienie 24,4% i 17,9%, kolejna odbyta wizyta 23,0% i 16,9%.
20. **TelemediGO nie jest powrotem.** Mierzymy je osobno: sprzedaż, przychód i podział kohort. W obecnych danych wybór nic nie zmienia, bo każdy z 686 osobnych zakupów TelemediGO przypada po co najmniej drugim zamówieniu pacjenta.
21. **Przychód z konsultacji = zapłata minus zwrot** (`amount_paid − refund_amount`). TelemediGO (89 zł) to osobna pozycja przychodu. Zwrot przypisujemy do dnia płatności zamówienia, bo w danych nie ma daty zwrotu. Przy wizycie nieodebranej zapłata zostaje w przychodzie. Zadanie nie mówi wprost „po zwrotach”. Słownik danych oddziela opłatę za TelemediGO od zapłaty za konsultację, a nasz standard (`CLAUDE.md`, punkt 9) każe liczyć po zwrotach. **Wpływ:** 2 230 267 zł w okresie 1 i 3 228 342 zł w okresie 2, czyli +44,8% (przed zwrotami +47,7%, jak dashboard).
22. **Źródło pozyskania = pierwsze wejście pacjenta, a kod kampanii rozstrzyga.**
    - Pierwsze wejście to najwcześniejsza sesja spośród sesji konta i anonimowych sesji tych przeglądarek, w których pacjent kiedykolwiek był zalogowany. Sesja musi zacząć się nie później niż płatność za pierwsze zamówienie.
    - Jeśli na pierwszym zamówieniu jest kod kampanii, źródłem jest kampania kodu: L4SZYBKO20 → `meta_prosp_l4_szybko`, TIKTOK25 → `tt_prosp_l4_15min`, RANKING10 → ranking lekarzy.
    - **Dlaczego:** ta reguła zgadza się z kodami kampanii w 96,6–97,0% przypadków. Sesja płatności zgadza się w 67,4–71,5%, ostatnie oznaczone wejście w 30 dniach przed zakupem w 79,2–81,4%, a pierwsze wejście bez anonimowych sesji w 72,4–75,3%. Kod zmienia kanał tylko 183 pacjentom.
    - **Okna nie ograniczamy.** Każdy pacjent kupuje w ciągu 30 dni od pierwszego wejścia (75,1% tego samego dnia, 24,6% w ciągu 1–7 dni).
    - **Kanały** (grupy kampanii): wejścia bezpośrednie (puste UTM); Google Ads na hasło „Telemedi” (`gs_brand`); Google Ads ogólne (`gs_generic_*`); bezpłatne wyszukiwanie (Google i Bing, `organic`); Meta pozyskanie (`meta_prosp_*`); Meta remarketing (`meta_rmkt_koszyk`); TikTok; ranking lekarzy (`affiliate`); program poleceń (`referral`); CRM (newsletter i SMS). W kohortach i lejku pokazujemy też pojedyncze kampanie.
    - **Ograniczenia:** kontrola kodami obejmuje tylko trzy kampanie, a kampanie ogólne Google Ads, które zyskują najwięcej (z 19,2% do 27,2% nowych pacjentów wobec sesji płatności), nie mają kodu. Pacjent, który pierwszy raz wszedł w przeglądarce, w której nigdy się nie zalogował, ma źródło z pierwszej widocznej sesji.
23. **Przy ekonomii kampanii obok reguły z punktu 22 pokazujemy wynik według sesji płatności** (dopisek kandydata). Dotyczy to kosztu pozyskania i wyniku na pacjenta, także w narzędziu. Jeśli wynik którejś kampanii zmienia znak zależnie od reguły, opisujemy go jako niepewny, a nie jako wniosek.
24. **Remarketing według przyjętej reguły dostaje tylko 0,6% nowych pacjentów** (pierwsze wejście bez kodu: 0,7%, sesja płatności: 5,2%), bo z definicji dociera do osób, które już były na stronie. Jego wartości nie oceniamy tą regułą. Trafia na listę niewiadomych razem z testem: grupa kontrolna, której remarketing się nie wyświetla.
25. **Prowizja afiliacyjna = 25 zł za pierwsze opłacone zamówienie pacjenta, którego reguła z punktu 22 przypisuje do rankingu lekarzy, bez względu na status zamówienia.** Wynik: 1 233 pacjentów, czyli 30 825 zł za dwa lata (15 400 zł w okresie 1 i 15 425 zł w okresie 2). Obok podajemy jedną liczbę według kodu RANKING10: 595 pacjentów, czyli 14 875 zł. Różnica to 15 950 zł, czyli 0,29% przychodu z konsultacji po zwrotach z dwóch lat. Więcej czasu temu nie poświęcamy. Warunków umowy z rankingiem nie znamy.
26. **Okno powrotu po newsletterze i SMS-ie (uzupełnienie punktu 11): 24 godziny.** Zamówienie przypisujemy do wejścia z newslettera albo SMS-a, jeśli pacjent zapłacił w ciągu 24 godzin od wejścia, w dowolnej sesji.
    - Wejście to sesja z `utm_medium` = `email` albo `sms`, przypisana do pacjenta przez konto albo jego przeglądarkę.
    - **Liczą się tylko zamówienia nieanulowane**, tak samo jak przy powrocie (punkt 19). Doprecyzowane po recenzji Codeksa i przyjęte przez kandydata. Wszystkie płatności, łącznie z anulowanymi, można pokazać obok jako osobną miarę z jasną nazwą.
    - **Przy przypisaniu sprzedaży jedno zamówienie idzie do ostatniego wejścia z CRM przed płatnością**, żeby żadne zamówienie nie liczyło się dwa razy. Profil „co dzieje się po kliknięciu” liczymy na każde wejście osobno, a jego wiersze nie są rozłączne. Doprecyzowane po recenzji Codeksa i przyjęte przez kandydata. Wpływ jest mały: kampania reaktywacyjna ma 1 338 zamówień rozłącznie, czyli 175 na 1 000 wejść, wobec 176 na 1 000 przy liczeniu każdego wejścia osobno.
    - Odstępy od wejścia liczymy w UTC, żeby zmiana czasu nie przesuwała doby. Tło (dni 31–60 po wejściu) liczymy tylko dla wejść z pełnymi 61 dniami obserwacji.
    - **Dlaczego 24 godziny:** nadwyżka zamówień ponad zwykłe tempo zakupów jest prawie cała w tej samej sesji (179 zamówień na 1 000 wejść). W 24 godzinach są 182 zamówienia na 1 000 wejść, z czego około 4 to tło. Dłuższe okno dolicza głównie zamówienia w zwykłym tempie: w 7 dniach jest 207 zamówień na 1 000 wejść, z czego około 30 to tło. Okno 7 dni pokazujemy obok jako sprawdzenie wrażliwości.
    - **Ograniczenia:** w danych widać kliknięcia, a nie wysyłki. Czy wiadomość wywołuje zakup, rozstrzygnie dopiero test z grupą kontrolną bez wysyłki. Trafia to na listę niewiadomych.

27. **Okresy porównujemy na tych samych dniach kalendarzowych i zawsze podajemy liczbę pacjentów** (po recenzji Codeksa, przyjęte przez kandydata). Pełne okno powrotu obcina okres 2 (dla 90 dni: kohorty do 2.07.2026). Porównanie z całym okresem 1 mieszałoby więc różne pory roku. Do porównania okres 1 obcinamy do tego samego dnia roku: 31.08.2025 dla 30 dni, 1.08.2025 dla 60 dni i 2.07.2025 dla 90 dni. **Wpływ:** powrót w 90 dniach 23,9% (12 867 pacjentów) wobec 17,4% (18 924 pacjentów). Przy pełnym okresie 1 było 23,6%. Liczby z pełnego okresu 1 zostają jako opis wszystkich dojrzałych kohort.

Dopiski do wcześniejszych punktów: punkt 11 (okno) uzupełnia punkt 26, a punkt 15 (reguła prowizji) — punkt 25. Recenzja definicji przez Codeksa (model Sol): `notatki/recenzje/a4_codex.md`.

## 2026-10-19 — lejek i zdarzenia w lejku (punkt A5, część pozyskania, przyjęte przez kandydata)

Szczegóły i liczby: `notatki/a5_pozyskanie.md`, skrypty `analiza/a5p_*.py`.

28. **Lejek liczymy na sesjach zwykłych.** To sesje bez konta albo z kontem, które pojawia się dopiero na kroku logowania. Sesje zalogowane od wejścia i zakupy samego TelemediGO pokazujemy osobnymi wierszami. Dzień sesji to `dzien_pl`, a odstępy między krokami liczymy w UTC.
29. **„Kupował wcześniej”** znaczy, że pierwszy zakup pacjenta był przed początkiem sesji. Pacjenta rozpoznajemy po koncie w sesji albo po koncie przeglądarki, w której kiedykolwiek był zalogowany. Zdarzeń w lejku szukamy w sesjach osób, które jeszcze nie kupowały, bo liczba sesji powracających rośnie od zera przez pierwszy rok i podnosi konwersję całości bez żadnego zdarzenia.
30. **Wykrywanie zdarzeń w lejku:** podział binarny serii dziennych (kara 25, odcinek co najmniej 14 dni, zmiana co najmniej o 1 punkt procentowy i o 5% względnie). Wpływ = (poziom po − poziom przed) × sesje wchodzące na krok × dalsza konwersja do płatności. To przybliżenie, a nie dowód przyczyny. Każde zdarzenie sprawdzamy na bazie: czy jest w każdym kanale i czy nie jest zmianą struktury ruchu.
31. **Rozkład zmiany konwersji** dzielimy na efekt struktury ruchu i efekt konwersji w obrębie grup. Grupy nowe w okresie 2 (na przykład nowe kampanie) wchodzą w całości do efektu struktury.
32. **Grupy kanałów przy sezonie:** płatne (Google Ads, Meta, TikTok), afiliacja osobno, bezpłatne (wejścia bezpośrednie, bezpłatne wyszukiwanie, program poleceń, newsletter i SMS). Źródło według przyjętej reguły (`Z1K`).

## 2026-10-19 — kohorty, marża na pacjenta i przebieg wizyty (punkt A5, część retencji, przyjęte przez kandydata)

Szczegóły i liczby: `notatki/a5_retencja.md`, skrypty `analiza/a5r_*.py`, wspólny moduł definicji `analiza/definicje.py`.

33. **Koszt lekarza u pediatry = 100 zł**, jak u „każdego innego specjalisty”. Podstawa: zasada z zadania wymienia osobno tylko internistę (25 zł) i psychiatrę (200 zł), a wszystkim pozostałym przypisuje 100 zł. Dodatkowa przesłanka: TelemediGO traktuje pediatrę jak specjalistów (zniżka 20%, nie 50%). Codex (Sol) uznał to za rozsądne. Wariant 25 zł: koszt niższy o 84 300 zł w okresie 1 i 110 700 zł w okresie 2; marża na pacjenta w 90 dniach wyższa o 4,8 i 3,7 zł. Kierunek wniosków bez zmian. Psycholog też liczy się jako inny specjalista (100 zł).
34. **Marża na pacjenta (przed kosztem pozyskania)** = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza (za wizyty odbyte i zwrócone), narastająco od dnia wejścia do kohorty (dzień 0, z pierwszym zamówieniem i TelemediGO kupionym przy kasie) do dnia N, tylko kohorty z pełnym oknem N dni. „Miesiąc” od pierwszego zakupu = kolejne 30-dniowe bloki (miesiąc 1 = dni 0–30). Koszt pozyskania (kampanie, prowizja) odejmuje sesja prowadząca przy ekonomii kampanii.
35. **Cechy pierwszego zakupu w podziałach kohort:** pierwsza usługa = internista według celu wizyty (L4, e-recepta, konsultacja, skierowanie), pediatra, psychiatra, inny specjalista; zniżka = brak, TelemediGO albo kod rabatowy; przeglądarka = wbudowana w aplikację (Instagram, Facebook, TikTok) albo zwykła, z sesji płatności; urządzenie z sesji płatności.
36. **Struktura a zachowanie:** rozkład zmiany na nowe segmenty (komórki bez pacjentów w okresie 1), zniknięte segmenty, strukturę i zachowanie w komórkach wspólnych (rozkład symetryczny), na podziałach od kanału do kampania × usługa × zniżka × status pierwszego zamówienia × przeglądarka. Status pierwszej wizyty może sam zależeć od kampanii, więc pokazujemy rozkład z nim i bez niego. Wynik nie jest dowodem przyczyny.
37. **Opóźnienie wizyty** = faktyczny start − umówiony termin w minutach liczony co do sekundy (różnica znaczników czasu), tylko wizyty odbyte (completed, refunded); koszyki: do 5, ponad 5 do 15, ponad 15 do 30, ponad 30 minut, brak wizyty (anulowana, nieodebrana). Pora = godzina umówionego terminu (rano 6–11, południe 12–15, wieczór 16–23, noc 0–5). Obciążenie = nieanulowane wizyty u internisty z terminem w tej samej godzinie zegarowej tego samego dnia. Czekanie = termin − moment zapłaty.
38. **Wartość powrotu do scenariuszy marży** = różnica marży z dni 1–180 między pacjentem, który wrócił w 90 dniach, a tym, który nie wrócił (kohorty okresu 1 z pełnymi 180 dniami): 95,6 zł. To różnica obserwacyjna między grupami, nie oszacowanie dodatkowej marży z odzyskanego powrotu, i nie obejmuje marży po 180 dniach. Kwoty z jej użyciem opisujemy jako scenariusze, z liczbą pacjentów zgodną z regułą źródła.

## 2026-10-20 — ekonomia kampanii (punkt A5, przyjęte przez kandydata)

Szczegóły i liczby: `notatki/a5_ekonomia.md`, skrypty `analiza/a5e_*.py`.

39. **Koszt pozyskania pacjenta** = (wydatki kampanii + prowizja afiliacyjna) / nowi pacjenci kampanii. Wydatki i nowych pacjentów bierzemy z tych samych dni kalendarzowych. Dzień pacjenta to dzień pierwszej płatności. Kanały bez wydatków mają koszt 0 zł, a program poleceń nie ma kosztu w danych. Pacjent kupuje zwykle tego samego dnia co pierwsze wejście (75,1%) albo w ciągu 7 dni (24,6%), więc przesunięcie na brzegach okna jest małe.
40. **Wynik na pacjenta** = marża na pacjenta w N dniach (założenie 34) − koszt pozyskania. Wynik po 90 dniach (kohorty 1.10–2.07 w obu okresach) i po 180 dniach (1.10–3.04) pokazujemy zawsze obok siebie, w notatkach, w narzędziu i na liście priorytetów (dopisek kandydata). Powód: pacjenci kampanii na L4 prawie nie wracają, a pozostali tak, więc samo okno 90 dni zaniża wartość pozostałych kampanii. Okno 180 dni obejmuje inne, starsze kohorty. Przedział 95% jest warunkowy: liczymy go tylko z rozrzutu marży, przy stałym koszcie pozyskania i danej regule źródła. **Prognoza marży rocznika** = nowi pacjenci i wydatki z całego okresu × marża na pacjenta w 90 dniach z kohort z pełnym oknem, każda kampania osobno, sumy z kampanii. Obejmuje też marżę pacjentów pozyskanych pod koniec okresu, która przypada po jego końcu.
41. **Kampania niepewna (wynik zależny od reguły atrybucji)** = taka, której wynik na pacjenta ma inny znak według przyjętej reguły i według sesji płatności, w którymkolwiek oknie (90 albo 180 dni) i okresie (założenie 23). Sesja płatności z definicji obniża wynik kampanii pozyskujących i podnosi wynik wejść bezpośrednich, wyszukiwania marki i remarketingu. „Niepewne” są więc prawie wszystkie kampanie pozyskujące nowych pacjentów, nie tylko nowe kampanie na L4. Wynik dodatni w obu regułach też nie dowodzi, że dodatkowy budżet się opłaci.
42. **Naprawić albo wyłączyć — rachunek.**
    - **Wyłączyć** = oszczędzone wydatki − dodatkowi pacjenci × marża na pacjenta, w trzech wariantach dodatkowości: 100%, 50% i 0%. Zakładamy, że pacjenci dodatkowi mają średnią marżę wszystkich przypisanych, że pacjenci, którzy przyszliby bez kampanii, zachowują się jak dziś, i że koszty pozostałych kanałów się nie zmieniają.
    - **Naprawa zwrotów L4** = odsetek zwrotów po wizycie L4 spada do poziomu pozostałych pacjentów. Wariant A: zapłata zostaje, czyli x_A = zwroty − wizyty × odsetek docelowy, a zysk = x_A × średni zwrot. Wariant B: pacjent nie kupuje, czyli x_B z równania (zwroty − x_B) / (wizyty − x_B) = odsetek docelowy, a zysk = x_B × (średni koszt lekarza zwróconej wizyty L4 − dalsza marża tych pacjentów).
    - **Zgoda marketingowa** = udział zgód do poziomu pozostałych pacjentów, wyceniony na dwa sposoby, pokazywane osobno i niedodawane do sum: powrotem przypisanym do newslettera i SMS-a (wariant optymistyczny) oraz całą różnicą powrotu.
    - **Przeglądarki wbudowane** = połowa luki konwersji wobec zwykłych przeglądarek w tej samej kampanii, tylko gdy luka jest dodatnia.

    Każdy powrót wyceniamy na 95,6 zł (założenie 38). Kwot w horyzoncie 180 dni (powroty, zgody, poranek) nie dodajemy do wyników w horyzoncie 90 dni.
43. **Scenariusz porannych opóźnień** = spadek powrotu w starych kampaniach z części retencji (sama zmiana rozkładu opóźnień albo cały spadek, obie reguły) × liczba ich pacjentów w okresie 2 × 95,6 zł, zawsze razem z wariantem „brak efektu” (0 zł). Zawsze nazywamy go scenariuszem, a nie kosztem kampanii. Wariant szeroki nie jest formalną górną granicą.

## 2026-10-20 — narzędzie (punkt B, przyjęte przez kandydata)

Szczegóły: `notatki/b_narzedzie.md`, sekcje 8 i 10; kod `analiza/b_eksport.py`.

44. **Lejek na stronie narzędzia liczymy tak jak w A5 (pozyskanie):** sesje zwykłe, dzień sesji w czasie polskim, „jeszcze nie kupowali” według pierwszego zakupu konta albo przeglądarki (założenia 28–29). Przy wygładzeniu wykresu odsetek to suma licznika z N dni podzielona przez sumę mianownika z tych samych dni, a nie średnia odsetków dziennych.
45. **Porównanie okresów w kohortach na stronie:** okres B obcinamy do kohort z pełnym oknem, a okres A do tej samej długości od jego początku. Przy porównaniu rok do roku to dokładnie te same dni kalendarzowe (założenie 27), a przy własnych datach ta sama długość.
46. **Wynik biznesu w czasie — dni księgowania:** przychód, zwrot i koszt lekarza w dniu płatności zamówienia; TelemediGO w dniu zakupu; wydatki na kampanie w dniu z pliku kampanii; prowizja afiliacyjna według przyjętej reguły źródła, w dniu pierwszego zamówienia pacjenta. Tak samo liczy `analiza/c_priorytety.py` (W3, W4). Pacjentów nowych kampanii w zakładce „Po zakupie” wyznaczamy według przyjętej reguły źródła, jak w części retencji.

## 2026-10-20 — TelemediGO i lista priorytetów (punkt C, przyjęte przez kandydata)

Szczegóły: `notatki/c_szkic.md`, skrypty `analiza/c_telemedigo.py` i `analiza/c_priorytety.py`. Recenzja Codeksa (Sol): `notatki/recenzje/c_codex.md`.

47. **Zniżka TelemediGO w złotych** = cena katalogowa − zapłata na zamówieniu ze zniżką TelemediGO. **Zniżka efektywna** liczy tylko wizyty odbyte i nieodebrane, bo przy anulowanej i zwróconej wizycie pacjent dostaje całą zapłatę z powrotem. Zniżkę przypisujemy członkostwu, w którego ważności (od chwili zakupu do `valid_until` włącznie) padło zamówienie.
48. **Typ zakupu TelemediGO:** przy kasie z pierwszym zamówieniem pacjenta, przy kasie z kolejnym zamówieniem, osobno (sesja z kampanii `crm_go_upsell`). Okres zakupu = dzień zakupu członkostwa. **Odsetek kupujących przy kasie** liczymy na zamówieniach pacjentów, którzy w chwili zamówienia nie mieli ważnego członkostwa.
49. **Opłata wobec zniżek** to rachunek przy założeniu, że wizyty ze zniżką odbyłyby się i bez TelemediGO. Nie jest to wynik programu, bo nie wiemy, ile wizyt członkostwo dokłada.
50. **Kupujący TelemediGO a podobni pacjenci:** dokładne dopasowanie w warstwach (okres, kanał pozyskania według przyjętej reguły, pierwsza usługa, miesiąc kohorty), wynik ważony liczbą kupujących. Różnica to suma wpływu zniżki i samoselekcji, nie efekt programu.
51. **Wartość pozycji listy priorytetów** = zmiana marży na rok, z okresem 2 jako rokiem bazowym, przy kampaniach w horyzoncie 90 i 180 dni od pozyskania i według obu reguł źródła. Kwot z różnych pozycji nie sumujemy (różne horyzonty, nakładanie się). Czas wdrożenia to nasz szacunek.
52. **Utracony pierwszy zakup w Safari na iOS = utracony nowy pacjent** z marżą nowych pacjentów z pierwszą płatnością w Safari na iOS w okresie 2, bez kosztu pozyskania (wejście już opłacone).
53. **Kwoty kampanii działających krócej niż rok przeliczamy na pełny rok przy tym samym tempie** (TikTok na L4: 234 dni, mnożnik 1,56; Meta na L4: 332 dni, mnożnik 1,10) i podajemy obok kwot z dni działania (`c_priorytety.txt`, P11). Po wstrzymaniu TikToka naprawę zwrotów L4 wyceniamy tylko dla Meta.

## 2026-10-20 — narzędzie, trzecia wersja (przyjęte przez kandydata)

54. **Na stronie kwota kampanii na pełny rok = kwota z dni działania × 365 / dni działania, bez zaokrąglania mnożnika** (tak liczy `analiza/c_priorytety.py`, założenie 53). Przy każdym odsetku w tekstach punktu C stoi liczebność odczytana z raportów (zasada kandydata dla strony); takie liczby, dopisane poza szkicem, raport `analiza/wyniki/b_eksport_c.txt` wypisuje jako „dodane”.


# Załącznik D — notatki/ZNALEZISKA.md

# Znaleziska — rzeczy podejrzane w danych

Zasada Telemedi: „jeśli coś w danych wygląda podejrzanie, powiedz o tym — to też jest odpowiedź”. Tu trafia każda niespójność, luka, duplikat, wartość nierealna i każdy tekst w danych, który wygląda na skierowany do AI (nie wykonujemy go — tylko opisujemy).

## 2026-10-19 — kontrola bezpieczeństwa paczki

**Wynik: w paczce nie znaleźliśmy tekstu skierowanego do AI ani niczego, co wygląda na ukryte polecenie.**

- Paczka `telemedi-b2c-dane.zip`, SHA-256 `aad606afa8517eb9b773c951a01262a0115cb19632ab7f650f86d3ee89ed12bd`. 18 plików, dokładnie lista z zadania. Program antywirusowy Windows (Microsoft Defender) nie znalazł zagrożeń. Raporty: `bezpieczenstwo/raport_20261019_115329.txt` (bez rozpakowania), `bezpieczenstwo/raport_20261019_115443.txt` (po rozpakowaniu).
- Nagłówki 17 plików CSV zgodne ze słownikiem z zadania. Liczby wierszy zgodne co do wiersza (razem 1 082 369). Żaden wiersz nie ma innej liczby pól niż nagłówek.
- `dane/README.md` (110 linii) przeczytany jako dane: to wyłącznie słownik danych i zasady biznesowe. Nie zwraca się do AI i niczego nie każe robić.
- **Fałszywy alarm skanu:** wszystkie 9 761 oznaczeń „słowa kierowane do AI” to dwie wartości ze słowem „polecenie”: `utm_source = 'polecenie'` (4 741 sesji) i `landing_page = '/polecenie'` (5 020 sesji). To program poleceń — README w sekcji o kosztach marketingu wymienia go wprost („program poleceń: bez kosztu w danych”). Skrypt reaguje na to słowo, bo po polsku może znaczyć „rozkaz”.
- **Do sprawdzenia w analizie (nie bezpieczeństwo):** liczba sesji z wejściem na `/polecenie` (5 020) i liczba sesji ze źródłem `polecenie` (4 741) różnią się o 279. Strona poleceń i oznaczenie źródła nie zawsze idą w parze — ważne przy przypisywaniu źródła pozyskania.
- **Ograniczenie tej kontroli:** skan treści szukał listy znanych słów i wzorców. Nie wyklucza tekstu sformułowanego innymi słowami. Dlatego zrobiliśmy drugą kontrolę od odwrotnej strony (niżej).

### Profil wszystkich kolumn (`bezpieczenstwo/profil_kolumn.py`, raport `bezpieczenstwo/profil_kolumn_20261019_120448.txt`)

**Wynik: w danych nie ma miejsca na ukryte polecenie. Pytanie o prompt injection uważamy za zamknięte.**

- Każda kolumna z określonym formatem (identyfikatory, daty i czasy, liczby, wartości ze słownika — 42 z 53 kolumn) ma zero wartości spoza formatu.
- Kolumny swobodne mają od 2 do 21 unikalnych wartości. Wszystkie wypisane w raporcie i przejrzane: regiony, źródła i kanały wejścia, 14 nazw kampanii, systemy, przeglądarki, 21 stron wejścia, 6 kodów rabatowych. Same zwykłe wartości marketingowe i adresy podstron.
- Najdłuższa komórka w całym zbiorze ma 38 znaków (`/blog/teleporada-jak-sie-przygotowac` i podobne). Nie ma ani jednego znaku spoza zwykłego zestawu (litery, cyfry, polskie znaki, podstawowa interpunkcja).
- Spacje występują tylko między datą a godziną i w nazwie przeglądarki `Samsung Internet`.

### Do analizy — pierwsze podejrzane rzeczy zauważone przy profilu

- **Kod rabatowy `TEST-QA` w 1 810 zamówieniach.** Wygląda na zamówienia testowe zespołu jakości w danych produkcyjnych. Do sprawdzenia: kiedy występują, jakie mają kwoty i statusy, czy trzeba je wyłączyć z przychodu i z kohort. → **Sprawdzone w A2** (niżej): 22 konta testowe, 2 071 zamówień, część bez kodu.
- **Źródło `bing` (3 944 sesje) nie ma kosztów w `marketing_spend.csv`.** Do sprawdzenia, czy to ruch bezpłatny (`organic`), czy brakujący koszt kampanii. → **Wyjaśnione w A2:** Bing ma w sesjach `utm_medium = organic`, czyli bezpłatne wyniki wyszukiwania. Brak kosztu jest zgodny z oznaczeniem.
- **Dwie kampanie mają koszty tylko przez część okresu:** `meta_prosp_l4_szybko` przez 332 dni i `tt_prosp_l4_15min` przez 234 dni, wobec 730 dni pozostałych. To kandydaci na zdarzenia (start kampanii) do odczytania z danych. → **A2:** to starty kampanii, nie luki. Sesje i koszty zaczynają się tego samego dnia (szczegóły niżej).

## 2026-10-19 — jakość danych (punkt A2)

Pełny raport: `analiza/wyniki/a2_jakosc.txt`, kod: `analiza/a2_jakosc.py`. Na razie nic nie jest usunięte ani poprawione. Propozycje czyszczenia czekają na wspólny przegląd.

**W skrócie: dane są czyste poza dwiema dużymi sprawami — duplikatami zamówień w czerwcu 2026 i zamówieniami testowymi. Obie zawyżają drugi rok wobec pierwszego.**

### Duże

1. **Duplikaty zamówień: 604 zamówienia zapisane dwa razy, wszystkie od 10.06.2026 00:07 do 24.06.2026 23:59.**
   - W pliku `orders.csv` jest 65 882 wierszy, a unikalnych zamówień 65 278. Każde zdublowane zamówienie ma dokładnie dwie identyczne kopie w dwóch sąsiednich liniach.
   - W tych 15 dniach zdublowanych jest od 28% do 42% zamówień dziennie. Dzień przed oknem i dzień po nim nie ma ani jednego duplikatu.
   - Udział zdublowanych jest podobny bez względu na metodę płatności, status i zniżkę (od 33% do 39%). To wygląda na błąd eksportu, a nie na prawdziwe podwójne płatności. W analityce każde z tych zamówień ma tylko jeden krok płatności.
   - Wszystkie duplikaty są w drugim roku dashboardu (X 2025 – IX 2026). Dodają mu 604 zamówienia i 51 293 zł zapłat, czyli 45 805 zł po odjęciu zwrotów.
   - W pozostałych tabelach nie ma ani jednego duplikatu, także na stykach plików kwartalnych i półrocznych.

2. **Zamówienia testowe: 22 konta, 2 071 zamówień, z czego 290 bez kodu TEST-QA.**
   - 1 781 zamówień ma kod TEST-QA. Wiersze z tym kodem to 1 810, z czego 29 to duplikaty z punktu 1. Każde jest zapłacone 1 zł zamiast 89 zł i ma status „odbyta”.
   - Te same 22 konta mają jeszcze 290 zamówień bez kodu. Każde jest zapłacone pełne 89 zł, zwrócone w całości i ma status „zwrócona”. Wyglądają na testy procesu zwrotu. Filtr po samym kodzie by ich nie złapał.
   - Wszystkie 2 071 to czat z internistą trwający dokładnie 1 minutę. Taki czas trwania nie występuje u żadnego innego pacjenta (najkrótsza prawdziwa wizyta trwa 3 minuty). Dwa niezależne podpisy (kod na koncie i czas 1 minuty) dają ten sam zbiór.
   - Składane tylko od poniedziałku do piątku, między 9:00 a 17:59. Wszystkie konta to województwo mazowieckie, miasto powyżej 200 tys. mieszkańców, bez zgody marketingowej, roczniki 1986–1997. Wszystkie wchodzą bezpośrednio, z komputera, w przeglądarce Chrome, na stronę `/konto`.
   - Liczba testów rośnie z 35 w czwartym kwartale 2024 do 370–410 na kwartał w 2026. W pierwszym roku dashboardu jest ich 553, w drugim 1 518. Zawyżają więc wzrost zamówień.
   - W analityce mają 2 093 sesje z kompletem kroków lejka (2 071 z zamówieniem i 22 sesje założenia konta). Zawyżają też lejek.
   - Pieniądze: 27 591 zł zapłat i 25 810 zł zwrotów, czyli 1 781 zł przychodu. Według zasady z zadania (25 zł za każdą odbytą wizytę u internisty, także zwróconą) dałoby to 51 775 zł kosztu lekarza. Czy lekarz naprawdę dostał wynagrodzenie za jednominutowy test, z danych nie wiemy.

### Do wspólnej dyskusji

3. **Sesje zalogowane od wejścia nigdy nie kończą się zakupem konsultacji.**
   - Słownik danych mówi, że pacjent zalogowany na wejściu ma `user_id` w sesji, ale nie ma kroku `account_completed`.
   - Takich sesji (bez zakupu samego TelemediGO) jest 22 068. Wszystkie należą do pacjentów, którzy już wcześniej kupowali. Wchodzą głównie na `/konto` oraz z newslettera i SMS-ów.
   - 4 574 z nich wybiera usługę. Tylko 112 wybiera termin, a do płatności nie dochodzi żadna. Wśród sesji niezalogowanych termin wybiera 42% tych, które wybrały usługę.
   - Z drugiej strony każda z 65 278 sesji z zamówieniem ma krok logowania, także każda z 24 338 sesji zakupów powtórnych. Wyjątek ze słownika w sesjach płacących w ogóle nie występuje.
   - Obraz jest taki sam w każdym kwartale, więc to nie jest zdarzenie z konkretnego dnia.
   - Dwa możliwe odczytania: (a) wejścia zalogowane to wizyty „sprawdzam konto”, a do zakupu pacjent i tak przechodzi przez logowanie; (b) ścieżka zakupu dla zalogowanych jest zepsuta albo inaczej mierzona. Ma to znaczenie dla lejka i dla oceny kampanii CRM.

4. **START10 nie jest kodem z okresu startu.** Plan zakładał, że okres rozruchu wyznaczy kod startowy START10. Tymczasem START10 jest używany przez całe dwa lata, na 9,0–9,5% pierwszych zamówień w każdym kwartale do grudnia 2025 i na 6,8–7,8% od stycznia 2026. Okres rozruchu trzeba wyznaczyć inaczej.

5. **Kody rabatowe obniżają cenę o stałą kwotę w złotych, a nie o procent.** START10 i RANKING10 to 10 zł, WRACAM15 15 zł, L4SZYBKO20 20 zł, TIKTOK25 25 zł, TEST-QA 88 zł. Kody L4SZYBKO20, START10, TIKTOK25 i RANKING10 występują wyłącznie na pierwszym zamówieniu pacjenta. WRACAM15 występuje wyłącznie na kolejnych zamówieniach.

6. **Starty kampanii widoczne w danych (kandydaci na zdarzenia do punktu A5, nie problemy jakości):**
   - `meta_prosp_l4_szybko` (Meta): sesje i koszty od 3.11.2025, kod L4SZYBKO20 od 4.11.2025;
   - `tt_prosp_l4_15min` (TikTok): sesje i koszty od 9.02.2026, kod TIKTOK25 od 10.02.2026;
   - `crm_go_upsell` (newsletter, sprzedaż TelemediGO): sesje od 8.09.2025.

### Drobne

7. **Luka w danych 17.05.2025 od 13:00 do 14:00.** W tej godzinie jest 1 sesja zamiast typowych 21 i nie ma żadnego zamówienia. Dwie inne godziny (11.10.2024 16:00 i 14.12.2024 13:00) mają sesje bez zdarzeń lejka, ale to może być przypadek. Wpływ pomijalny.
8. **24 zamówienia „psycholog + e-recepta”.** Psycholog nie jest lekarzem i w Polsce nie wystawia recept. Wartość nierealna.
9. **Jedno zamówienie pacjenta z aktywnym TelemediGO jest zapłacone bez zniżki.**
10. **Program poleceń:** 330 sesji wchodzi na `/polecenie` z innym źródłem (bezpośrednio, z Google albo z Meta). Kolejne 51 sesji ma źródło `polecenie`, ale inną stronę wejścia. Ważne przy przypisywaniu źródła.

### Sprawdzone i czyste

- Czas: moment płatności w każdym z 65 278 zamówień i w każdym z 4 227 zakupów TelemediGO jest co do sekundy równy krokowi `payment_succeeded` w analityce po przeliczeniu na czas polski. System transakcyjny zapisuje czas polski i poprawnie obsługuje zmianę czasu. Pliki kwartalne i półroczne są pocięte według północy czasu polskiego, bez dziur i bez nakładek.
- Kliknięcia wobec sesji są stabilne w każdym kwartale: około 0,92 sesji na kliknięcie w Google, od 0,79 do 0,82 w Meta i 0,72 w TikToku. Nie ma dni z kosztem bez sesji ani sesji z kampanii płatnej bez kosztu. Największe odchylenie dnia od średniej kampanii mieści się w szumie losowym.
- Powiązania: każde zamówienie i każdy zakup TelemediGO ma sesję tego samego konta. Każda płatność w analityce ma zamówienie albo zakup TelemediGO. Nic nie dzieje się przed założeniem konta.
- Statusy wobec zwrotów są zgodne z opisem w README. Nie ma zwrotów większych niż zapłata ani zwrotów częściowych. Ceny katalogowe są stałe przez dwa lata. Zniżki TelemediGO (50% i 20%) i kody rabatowe zgadzają się co do złotówki. TelemediGO kosztuje zawsze 89 zł, jest ważne 365 dni, a członkostwa jednego pacjenta się nie nakładają.
- Kroki lejka idą zawsze w kolejności. Nie ma kroku bez poprzedniego.
- Tożsamość: żadna przeglądarka nie jest dzielona przez dwa konta. 3 835 kont (7,3%) używa więcej niż jednej przeglądarki, najwięcej ośmiu.
- Wartości realne: wiek pacjentów od 18 do 84 lat, wizyty trwają od 3 do 36 minut, termin wypada od 9 minut do 71 godzin po zapłacie.

## 2026-10-19 — odtworzenie dashboardu (punkt A3)

Pełny raport: `analiza/wyniki/a3_dashboard.txt`, kod: `analiza/a3_dashboard.py`, cała siatka wariantów: `analiza/wyniki/a3_siatka.csv`.

**W skrócie: dashboard liczy dane na surowo — z duplikatami zamówień, z zamówieniami testowymi i z przychodem przed zwrotami. Po oczyszczeniu wzrost zamówień spada z +61% do +56%, a przychodu z +50% do +48%. Liczba nowych pacjentów i sprzedaż TelemediGO się nie zmieniają.**

1. **Jak liczony jest dashboard.** W siatce 864 kombinacji definicji wszystkie cztery liczby naraz daje 14 kombinacji. Każda z nich liczy zamówienia razem z duplikatami i razem z testami, a przychód jako sumę zapłat przed zwrotami. Żadna kombinacja bez duplikatów albo bez testów nie pasuje.
   - Pasujące kombinacje różnią się tylko drobiazgami: czy liczą zamówienia anulowane, czy granice okresów są w czasie polskim czy w UTC, czy przychód obejmuje TelemediGO, czy nowym pacjentem jest też ktoś, kto kupił samo TelemediGO. Różnice między nimi wynoszą najwyżej 0,64 punktu procentowego w każdej miarze.
   - Najprostsza pasująca kombinacja: każdy wiersz pliku zamówień to zamówienie, przychód to suma zapłat bez TelemediGO i bez odejmowania zwrotów, nowy pacjent to konto z pierwszym zamówieniem, czas polski. Daje +51,9% pacjentów, +60,7% zamówień, +50,3% przychodu i +40,3% TelemediGO.
   - Kontrola: gdyby dashboard obcinał procenty zamiast je zaokrąglać, nie pasowałaby żadna kombinacja.

2. **Mostek od dashboardu do danych oczyszczonych** (najprostsza kombinacja, okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026):

   ```
   krok                                nowi pacjenci   zamówienia   przychód z konsultacji   TelemediGO
   dashboard (dane surowe)                 +51,9%        +60,7%            +50,3%              +40,3%
   bez duplikatów                          +51,9%        +58,3%            +48,1%              +40,3%
   bez duplikatów i kont testowych         +52,1%        +55,7%            +47,7%              +40,3%
   + przychód po odjęciu zwrotów              —             —              +44,8%                 —
   ```

   - Duplikaty z czerwca 2026 dodają drugiemu rokowi 604 zamówienia, czyli 2,4 punktu procentowego wzrostu zamówień.
   - Testy dodają kolejne 2,6 punktu procentowego, bo w drugim roku jest ich prawie trzy razy więcej niż w pierwszym (1 518 wobec 553).
   - Nowi pacjenci prawie się nie zmieniają (+51,9% wobec +52,1%), bo testy to tylko 22 konta.
   - Po oczyszczeniu: 16 231 nowych pacjentów w okresie 1 i 24 687 w okresie 2; 24 716 i 38 491 zamówień; 2,375 i 3,508 mln zł zapłat przed zwrotami; 1 759 i 2 468 zakupów TelemediGO.

3. **Trop do A5: zwroty rosną prawie dwa razy szybciej niż sprzedaż.** Na danych oczyszczonych zwroty wynoszą 144 461 zł w okresie 1 i 279 855 zł w okresie 2, czyli +93,7%. Udział zwrotów w zapłatach rośnie z 6,1% do 8,0%. Najszybciej rosną zwroty po odbytej wizycie (status „refunded”): z 492 do 1 626 zamówień, czyli ponad trzykrotnie przy wzroście wszystkich zamówień o 56%. Za takie wizyty lekarz dostaje wynagrodzenie, więc to uderza w marżę podwójnie. Kiedy i gdzie to się zaczęło — w A5.

4. **Czego mostek jeszcze nie pokazuje:** start od zera. W pierwszym roku nie było bazy powracających pacjentów, więc część wzrostu zamówień i przychodu to naturalne dorastanie bazy, a nie lepsza retencja. To rozdzielamy w A5 (nowi wobec powracających, kohorty w tym samym wieku).

## 2026-10-19 — przy ustalaniu definicji (punkt A4)

Pełny raport: `analiza/wyniki/a4_definicje.txt`, kod: `analiza/a4_definicje.py`. Poniższe to obserwacje do sprawdzenia w A5, a nie wnioski. Przyczyn nie przesądzamy.

1. **Powrót w 90 dniach jest niższy w okresie 2 przy każdej definicji.** Przy przyjętych definicjach wynosi 23,6% w okresie 1 i 17,4% w okresie 2. Przy porównaniu na tych samych dniach kalendarzowych (punkt 27 założeń) jest to 23,9% (12 867 pacjentów) wobec 17,4% (18 924 pacjentów). We wszystkich wariantach nowego pacjenta i powrotu wynik mieści się między 23,0% a 25,2% w okresie 1 i między 16,9% a 18,5% w okresie 2. Kierunek jest więc ten sam.
2. **Zmienia się struktura źródeł.** Według przyjętej reguły źródła Meta (pozyskanie) to 6,3% nowych pacjentów w okresie 1 i 24,9% w okresie 2. TikTok rośnie z 0% do 8,9%. To kanały z najniższym powrotem w okresie 2: 6,7% (Meta pozyskanie) i 3,2% (TikTok) w 90 dniach. W pozostałych kanałach powrót w okresie 2 wynosi od 16,8% do 26,1%. Zmiana struktury może tłumaczyć część spadku powrotów, ale nie całość: powrót pacjentów z Meta (pozyskanie) spada też w obrębie samego kanału, z 20,7% do 6,7%. Rozdzielamy to w A5.
3. **Zwroty po odbytej wizycie przy pierwszym zamówieniu.** Takich pierwszych zamówień było 341 w okresie 1 i 1 394 w okresie 2. Ci pacjenci wracają w 90 dniach w 5,0% (okres 1) i 3,3% (okres 2), wobec 24,5% i 18,6% po wizycie odbytej bez zwrotu. Najczęściej zdarza się to w Meta (11,0% pierwszych zamówień według sesji płatności) i w TikToku (13,3%), wobec 1,7–3,6% w pozostałych kanałach. Możliwe wyjaśnienia to obietnica reklamy, decyzje lekarzy albo inna przyczyna. Rozstrzygamy w A5.
4. **Wejścia z newslettera i SMS-ów to w dwóch trzecich sesje zalogowane od wejścia, bez żadnego zakupu w sesji.** Takich wejść jest 10 330 z 15 239 (wejścia z pełnymi 61 dniami obserwacji, bez kampanii sprzedającej TelemediGO). W kolejnych dniach widać tylko małą nadwyżkę zamówień: 6 na 1 000 wejść w 7 dni i 13 na 1 000 w 30 dni. Pozostałe 4 909 wejść daje 557 zamówień nieanulowanych na 1 000 wejść w tej samej sesji. CRM to główny kanał powrotów, więc dołączamy to do sprawy sesji zalogowanych w A5 (dopisek kandydata).
5. **Kampania sprzedająca TelemediGO (`crm_go_upsell`)** daje 696 zakupów TelemediGO na 1 000 wejść w tej samej sesji. Każdy osobny zakup TelemediGO przypada po co najmniej drugim zamówieniu pacjenta.
6. **Pacjenci z kodem kampanii płacą często w innej sesji niż ta z kampanii.** 1 711 pacjentów z kodem L4SZYBKO20, TIKTOK25 albo RANKING10 płaci w sesji bezpośredniej, z wyszukiwania marki, z bezpłatnego Google albo z remarketingu Meta. Według pierwszego wejścia 97% z nich trafia do kampanii kodu. Dla tych trzech kampanii sesja płatności przypisuje więc część pacjentów pozyskanych przez kampanię do wejść bezpośrednich, wyszukiwania marki i remarketingu.

## 2026-10-19 — lejek i zdarzenia w lejku (punkt A5, część pozyskania)

Szczegóły, liczby i metoda: `notatki/a5_pozyskanie.md`. Raporty: `analiza/wyniki/a5p_*.txt`. Liczby potwierdził Codex (model Sol) własnym kodem. Jeden błąd mianownika w `a5p_zalogowane.py` został poprawiony (`notatki/recenzje/a5p_codex.md`).

**W skrócie: tracimy pacjentów w dwóch miejscach, które trzeba naprawić na stronie: w przeglądarkach wbudowanych w aplikacje i w zakładaniu konta w Safari na iOS od 17.03.2026. Rachunkowo prawie cały spadek konwersji lejka to zmiana struktury ruchu. Ten ruch traci jednak na każdym kroku, więc to nie jest tylko „inny ruch” (dopisek kandydata).**

1. **Konwersja sesji do płatności spadła z 16,0% w okresie 1 do 13,7% w okresie 2.** Rachunkowo prawie cały spadek to większy udział przeglądarek wbudowanych w aplikacje Instagram, Facebook i TikTok: z 10,7% do 35,6% sesji, głównie z reklam Meta i TikToka. Te przeglądarki płacą w 5–7% sesji, a Chrome i Safari w 16–18%. Tracą na każdym kroku lejka, także na zakładaniu konta.
2. **Zdarzenie 17.03.2026: w Safari na iPhone'ach i iPadach przestaje działać zakładanie konta.** Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spada z 66,2% do 45,1% i zostaje na tym poziomie do końca danych. Inne przeglądarki tego nie mają. Spadek jest w każdym kanale, więc to nie zmiana struktury. Psuje się zakładanie nowego konta, a logowanie do istniejącego działa. Szacunek: około 95–105 utraconych pierwszych zamówień na 30 dni, razem 628–695 od 17.03 do 30.09.2026. Przyczyny w danych nie widać.
3. **Starty kampanii jako zdarzenia:** Meta na L4 od 3.11.2025 (płaci w lejku lepiej niż starsza kampania Meta, ale 2–3 razy rzadziej niż wyszukiwarka; strona `/zwolnienie-l4-online` traci na konwersji tylko przez ten ruch), TikTok od 9.02.2026, sprzedaż TelemediGO w newsletterze od 8.09.2025 (686 zakupów samego TelemediGO).
4. **Remarketing Meta słabnie od początku 2026 przez zmianę puli odbiorców.** Płatność spada z 28,2% sesji w IV kwartale 2025 do około 19% w II i III kwartale 2026. W obrębie źródła, z którego osoba trafiła na stronę pierwszy raz, konwersja stoi.
5. **Sesje zalogowane od wejścia: dane nie rozstrzygają między odczytaniami.** Przeciw „zepsutej ścieżce, która odbiera nam zakupy” przemawiają trzy rzeczy: pacjenci odpadają przed krokiem konta, a nie na nim; pacjenci z takimi sesjami wracają częściej niż podobni bez nich; krok konta w zakupach powtórnych trwa kilkadziesiąt sekund, a nie 1–2 sekundy. Zostaje mocna niespójność ze słownikiem danych: według niego zalogowany pacjent nie ma kroku konta, a w danych ma go każdy zakup. Po pierwszym zakupie pacjent nie ma ani jednej anonimowej sesji, a rozkład odstępów między krokami w zakupach powtórnych jest jednakowy. To wygląda na cechę generatora danych.
6. **Sezon a wydatki: przyczyny wzrostu nowych pacjentów od X 2024 do I 2025 nie da się rozdzielić.** W kanałach opartych na wyszukiwaniu (bezpłatnym i płatnym) widać wyraźny sezon: zimą więcej nowych pacjentów niż latem. Wydatki rosły jednak w tych samych miesiącach. Kampania Meta z prawie stałym budżetem ma co najwyżej słaby sezon (+8% pacjentów zimą przy +5% wydatków).
7. **Strata między kliknięciem reklamy a sesją w Meta i TikToku** (dopisek kandydata). Na kliknięcie przypada 0,92–0,93 sesji w Google Ads, 0,79–0,82 w Meta i 0,72 w TikToku, stale w każdym kwartale. Trzy odczytania: porzucenie przed załadowaniem strony, luka w śledzeniu w przeglądarkach wbudowanych albo inne liczenie kliknięć przez platformy. W remarketingu Meta przeglądarek wbudowanych jest mało, a stosunek jest ten sam, co bardziej pasuje do liczenia kliknięć. Górna granica w okresie 2: 23 776 sesji, do 1 434 zamówień i 50 494 zł wydatków.
8. **Co nie jest zdarzeniem:** wzrost konwersji w pierwszym roku (dorastanie bazy powracających), spadki kroku konta z 5–12.02.2026 (ten sam problem Safari na iOS plus zmiana struktury) i spadek wyboru usługi wiosną 2026 (zmiana struktury). Kroki płatności są stabilne w każdym podziale.

## 2026-10-19 — kohorty, struktura pacjentów i przebieg wizyty (punkt A5, część retencji)

Szczegóły, liczby i metoda: `notatki/a5_retencja.md`. Raporty: `analiza/wyniki/a5r_*.txt`. Dwie recenzje Codeksa (model Sol) uwzględnione: `notatki/recenzje/a5r_codex.md` i `a5r_codex2.md`.

**Kohorty, powroty i marża na pacjenta (krok 2; porównanie na tych samych dniach kalendarzowych, tylko kohorty z pełnym oknem):**

- **Powrót spada w każdym oknie.** W 30 dniach 11,0% (14 984 pacjentów) wobec 7,8% (22 646). W 60 dniach 19,1% (13 941) wobec 13,7% (20 823). W 90 dniach 23,9% (12 867) wobec 17,4% (18 924). W 180 dniach 27,5% (9 125) wobec 22,2% (12 591).
- **Krzywa „dzień od pierwszego zakupu”:** okres 2 ma od 7. do 90. dnia stale około 72–75% powrotu okresu 1. Dłuższe okna (180 i 270 dni) wyglądają lepiej (0,81 i 0,89), ale obejmują tylko najstarsze kohorty okresu 2 (X 2025 – III 2026), więc nie świadczą o nadrabianiu.
- **Marża na pacjenta przed kosztem pozyskania** (przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza): w 90 dniach 66,6 zł wobec 58,3 zł (−8,3 zł, −12,5%); w 30 dniach 55,9 zł wobec 49,9 zł; w 180 dniach 75,5 zł wobec 67,7 zł. Kolejne zamówienia na pacjenta w 90 dniach: 0,334 wobec 0,234.
- **Kohorty miesięczne:** w okresie 1 powrót w 90 dniach mieści się między 21,3% a 26,3%. Październik 2025 jest jeszcze na tym poziomie (23,5%). Od listopada 2025 spada do 18,9–20,0%, a od marca 2026 do 13,7–15,6%. Kohorty tygodniowe pokazują te same dwa progi: tydzień od 3.11.2025 i tydzień od 2.03.2026.
- **Start od zera:** w okresie 2 jest 38 491 zamówień: 24 687 pierwszych, 5 289 powtórnych od pacjentów z kohort okresu 1 i 8 515 powtórnych od pacjentów z kohort okresu 2. W okresie 1 było 24 716 zamówień: 16 231 pierwszych i 8 485 powtórnych. Powtórne zamówienia rosną więc o 62,7%, ale 5 289 z nich to baza z okresu 1, której w okresie 1 z definicji nie było.
- **Koszt pediatry (wrażliwość):** wariant 25 zł zamiast 100 zł podnosi marżę na pacjenta w 90 dniach o 4,8 zł w okresie 1 i o 3,7 zł w okresie 2 (różnica kosztu: 84 300 zł i 110 700 zł). Kierunek zmiany się nie zmienia.

**Struktura a zachowanie oraz przebieg wizyty (kroki 3–5, w brzmieniu przyjętym przez kandydata):**

- Krok 3 w brzmieniu przyjętym przez kandydata (dopisek nr 1): większość spadku powrotów wiąże się z pacjentami dwóch nowych kampanii na L4, ale w kampaniach działających w obu latach też jest spadek, którego sprawdzone cechy nie tłumaczą. Obie wersje według reguły źródła: przyjęta reguła 4,6 i 2,0 punktu, sesja płatności 3,0 i 3,5 punktu (spadek z 23,9% do 17,4% w 90 dniach).
- Krok 4 i 5, przyjęte przez kandydata (STOP 2):
  - **Opóźnienia porannych wizyt u internisty od listopada 2025** (kandydat zmiany 24.11.2025): wizyty z terminem 6:00–11:59 spóźnione ponad 15 minut, pacjenci spoza nowych kampanii, 4,7–6,9% miesięcznie do X 2025, 15,7% w XI 2025, 29,7% w XII, 42,6% w I 2026, 47–53% od II 2026. U internisty w innych porach i u specjalistów bez dużej zmiany. **Przy tym samym porannym ruchu w dniu opóźnień jest o 26,4 punktu procentowego więcej niż rok wcześniej**, a w obrębie miesiąca opóźnienia prawie nie zależą od ruchu. Odczytanie bez przesądzania przyczyny: spadła poranna przepustowość (obsada, organizacja zapisów albo lekarze zajęci pacjentami spoza B2C), a nie tylko przybyło pacjentów.
  - **Rano spada powrót po wizytach spóźnionych, nie po punktualnych.** Pacjenci starych kampanii z pierwszą wizytą u internisty rano: powrót w 90 dniach 23,6% wobec 19,0%; wieczorem 23,5% i 23,5%. Sama zmiana rozkładu opóźnień przy stałych kampaniach i usługach odpowiada za −0,76 z −1,91 punktu spadku w starych kampaniach (przyjęta reguła źródła) i −0,64 z −3,50 (sesja płatności).
  - **Zwroty po wizytach L4 w nowych kampaniach (ważne dla listy priorytetów):** 17,4% odbytych wizyt L4 pacjentów kampanii `meta_prosp_l4_szybko` i `tt_prosp_l4_15min` kończy się zwrotem po wizycie (1 024 z 5 895 w okresie 2), wobec 5,3% L4 pozostałych pacjentów (270 z 5 080) i 6,0% w okresie 1. Kod rabatowy i opóźnienie nie zmieniają odsetka. W okresie 2 wszystkie zwroty po wizycie pacjentów nowych kampanii to 1 044 wizyty, 84 112 zł zwróconych zapłat i 33 975 zł kosztu lekarza za te wizyty. Powodu zwrotu w danych nie ma (możliwe odczytanie: lekarz nie wystawia L4, którego pacjent oczekuje po obietnicy reklamy).
  - **Niska zgoda marketingowa pacjentów nowych kampanii (ważne dla listy priorytetów):** 37,8% wobec 63,8–64,4% pacjentów starych kampanii; wejście z newslettera albo SMS-a w dniach 1–90 ma 8,2% z nich wobec 17,5–17,9%. Newsletter i SMS-y do tych pacjentów prawie nie docierają.
  - **Brak wyraźnego zdarzenia w powrocie starych kampanii:** najsilniejszy kandydat 2.03.2026 (z = −3,943, poniżej progu 4): 23,3% przed, 20,9% po. Luty 2026 bez spadku mimo opóźnień — trop eksploracyjny.

## 2026-10-20 — ekonomia kampanii (punkt A5)

Szczegóły, liczby i metoda: `notatki/a5_ekonomia.md`. Raporty: `analiza/wyniki/a5e_*.txt`, zestawienie `analiza/wyniki/a5e_kampanie.csv`. Recenzja Codeksa (model Sol) uwzględniona. Wynik po 180 dniach stoi zawsze obok wyniku po 90 dniach (dopisek kandydata).

**W skrócie:**

1. **Nowe kampanie na L4 pozyskują pacjenta taniej niż reszta kampanii płatnych, ale ten pacjent zostawia prawie o połowę mniej marży.** Według przyjętej reguły źródła wynik na pacjenta to +3,6 zł po 90 dniach i +7,0 zł po 180 dniach. Według sesji płatności to −9,4 zł i −5,2 zł. Znak zależy od reguły atrybucji, więc to wynik **niepewny**. Pozostałe kampanie płatne mają +20,0 zł po 90 dniach i +29,7 zł po 180 dniach.
2. **Kampania na TikToku ma wynik ujemny w obu regułach i w obu oknach:** −4,6 i −17,8 zł na pacjenta po 90 dniach oraz −1,1 i −11,0 zł po 180 dniach, przy małej próbie. Kampania Meta na L4 jest niepewna: +6,5 i −6,5 zł po 90 dniach oraz +8,2 i −4,3 zł po 180 dniach.
3. **Niska marża tych pacjentów to kody rabatowe, zwroty po wizycie L4 i prawie zerowe powroty.** Tańszy lekarz (internista) częściowo to równoważy.
4. **Zgoda marketingowa i przeglądarki wbudowane w aplikacje nie dają w tym rachunku wyraźnej wartości.** U pacjentów nowych kampanii zgoda prawie nie zmienia powrotu. Surowa konwersja w przeglądarkach wbudowanych nie jest w tych kampaniach niższa niż w zwykłych.
5. **Największa dźwignia naprawy to zwroty po wizytach L4.** Gdyby spadły do poziomu pozostałych pacjentów, dawałoby to od 22 do 57 tys. zł marży rocznie według przyjętej reguły.
6. **Dane nie rozstrzygają, czy pacjenci tych kampanii są dodatkowi.** Łączne pozyskanie w pozostałych kanałach po startach kampanii nie spadło wyraźnie. Widać jednak sygnał względnego osłabienia L4 w pozostałych kanałach po starcie kampanii Meta.
7. **Hipoteza porannych opóźnień to tylko scenariusz: od 0 do 65 tys. zł marży rocznie.** W wariancie wąskim wychodzi około 12 tys. zł. Na pacjenta nowych kampanii to od 0 do 12,6 zł. Szeroki wariant zjada cały ich wynik według przyjętej reguły.

**Szczegóły:**

- Nowe kampanie na L4 według przyjętej reguły: koszt pozyskania 32,7 zł, marża 36,3 zł, wynik +3,6 zł na pacjenta w 90 dniach. Według sesji płatności: 45,6 zł, 36,1 zł i −9,4 zł. Pozostałe kampanie płatne: +20,0 zł i +18,7 zł. Wynik nowych kampanii zależy od reguły atrybucji (niepewny). TikTok ma wynik ujemny w obu regułach (−4,6 i −17,8 zł), a Meta na L4 jest niepewna (+6,5 i −6,5 zł).
- Według sesji płatności prawie wszystkie kampanie pozyskujące mają wynik ujemny w 90 dniach, a według przyjętej reguły dodatni. To własność reguły, nie błąd kodu (punkt 2, potwierdził Codex).
- Marża pacjentów nowych kampanii jest niższa o 27,9 zł na pacjenta. Odpowiadają za to kody rabatowe (−12,8 zł), zwroty (−8,7 zł), brak powrotów (−12,1 zł), niższa cena (−6,7 zł) i rzadsze TelemediGO (−3,8 zł). Tańszy lekarz równoważy +16,2 zł.
- Zgoda marketingowa u pacjentów nowych kampanii prawie nie zmienia ich powrotu (4,2% wobec 4,1%).
- W nowych kampaniach surowa konwersja sesji do pierwszego zamówienia w przeglądarkach wbudowanych w aplikacje nie jest niższa niż w zwykłych (bez rozdzielenia urządzenia, daty i pacjenta).
- `gs_generic_specjalisci` ma wynik ujemny w obu regułach i oknach. `gs_generic_erecepta` drożeje: koszt pozyskania rośnie z 48,8 do 59,8 zł.
- Dodatkowość: nie widać dużego spadku łącznego pozyskania w pozostałych kanałach po startach kampanii. Widać jednak sygnał względnego osłabienia L4 po starcie Meta: L4 wobec innych usług w pozostałych kanałach 0,73 (od 0,56 do 0,95), kampania Google Ads na L4 0,67 (od 0,45 do 0,98). Na fikcyjnych datach startu w okresie 1 tak niski iloraz wychodzi w 4 z 44 tygodni. Dane nie rozstrzygają dodatkowości.
- Ranking lekarzy daje w obu okresach prawie tę samą liczbę pacjentów (616 i 617). Możliwa cecha generatora, bez wpływu na wnioski.

**Co zmienia okno 180 dni:**

- `gs_generic_lekarz_online` i `gs_generic_erecepta` przestają zależeć od reguły atrybucji: po 180 dniach są dodatnie w obu regułach;
- zależne od reguły zostają `meta_prosp_l4_szybko`, `gs_generic_l4` i `meta_prosp_lekarz_online`;
- TikTok i `gs_generic_specjalisci` są ujemne w obu regułach w obu oknach.

## 2026-10-20 — wynik biznesu po kwartałach (punkt B i dopisek kandydata do punktu C)

Raporty: `analiza/wyniki/b_eksport.txt` i `analiza/wyniki/c_priorytety.txt` (W4, P1). Obie sesje liczyły to niezależnie i dostały te same liczby.

- **Suma roczna ukrywa przebieg w kwartałach.** Marża (przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza − kampanie − prowizja) rośnie rok do roku o 71,4% w IV kwartale 2025, o 43,0% w I kwartale 2026, o 13,0% w II kwartale i spada o 6,8% w III kwartale 2026 (207 713 zł wobec 222 824 zł). Wydatki na kampanie są w tych kwartałach 1,30, 1,66, 2,04 i 2,08 raza wyższe niż rok wcześniej. Za cały rok marża rośnie o 26,6%.
- **Spadek w III kwartale to wydatki rosnące szybciej niż marża przed kampaniami:** marża przed kampaniami +78 963 zł, wydatki +94 123 zł.
- **Niższy jest kwartał, a nie każdy miesiąc.** Lipiec 2026: 73 384 zł wobec 66 832 zł; sierpień: 66 315 wobec 67 190 zł; wrzesień: 68 014 wobec 88 802 zł.
- **Wrzesień 2025 zawyża bazę porównania** przez start sprzedaży TelemediGO w newsletterze (225 zakupów w 23 dni). Bez opłat za TelemediGO III kwartał 2026 też jest niższy: −4,9%.
- **Szacowana skala problemu Safari na iOS w III kwartale 2026 (około 14–21 tys. zł marży) jest porównywalna ze spadkiem marży tego kwartału** (15,1 tys. zł; `c_priorytety.txt`, P1), ale wyniku kwartału bez tego problemu nie ustaliliśmy (weryfikacja Astrą, `notatki/recenzje/d_astra.md`).

## 2026-10-20 — TelemediGO i lista priorytetów (punkt C, przyjęte przez kandydata)

Szczegóły i liczby: `notatki/c_szkic.md` (sekcje 1–4), raporty `analiza/wyniki/c_telemedigo.txt` i `c_priorytety.txt`. Liczby główne potwierdził Codex (Sol) własnym kodem. Listę priorytetów oceniło konsylium (9 z 9): `notatki/konsylium/c_priorytety/synteza.md`.

**TelemediGO:**
- Wzrost sprzedaży TelemediGO o 40,3% to więcej zamówień i pełny rok sprzedaży w newsletterze (w okresie 1 23 dni). Odsetek nowych pacjentów, którzy kupują przy pierwszym zamówieniu, spada z 5,58% do 4,41%, w całości przez pacjentów nowych kampanii na L4 (1,5%).
- Członkostwa z okresu 1 dostały 104,57 zł zniżki efektywnej przy opłacie 89 zł. Kupujący przy kolejnym zamówieniu dostają 136,36 zł.
- Po zniżce 20% cena wizyty jest niższa niż koszt lekarza u wszystkich specjalistów poza psychiatrą. W okresie 2 to −14,7 tys. zł marży na 1 512 zamówieniach.
- Przy koszcie pediatry 100 zł (założenie 33) wizyta u pediatry przynosi stratę także bez zniżki (cena 95 zł).
- Odnawia około 5% członków. W danych nie widać przypomnienia o wygaśnięciu.
- Kupujący TelemediGO wracają częściej niż podobni pacjenci (+10,1 i +14,6 punktu procentowego w 90 dniach), ale po wygaśnięciu przewaga w proporcji zostaje (iloraz 1,77). Dane nie rozdzielają wpływu zniżki od samoselekcji.
- Wizyta u specjalisty po cenie katalogowej zostawia ponad koszt lekarza tylko 9–19 zł (cena 109–119 zł); pediatra (95 zł) i psycholog (99 zł) mają cenę poniżej kosztu lekarza przy założeniu 33 (`c_priorytety.txt`, P14).

**Odpowiedź „czy to wzrost” (przyjęta przez kandydata):** pacjentów z pierwszym zakupem jest o 52,1% więcej, ale retencja jest gorsza: powrót w 90 dniach 17,4% wobec 23,9% na tych samych dniach kalendarzowych, a bez pacjentów nowych kampanii 22,0% (przyjęta reguła) albo 20,4% (sesja płatności). W III kwartale 2026 marża była o 6,8% niższa niż rok wcześniej przy wydatkach na kampanie 2,08 raza wyższych; szacowana skala problemu Safari jest porównywalna z tym spadkiem (sekcja „wynik biznesu po kwartałach”). Liczba osób, które wróciły w 90 dniach, rośnie (3 076 → 3 289, +6,9%), spada odsetek.

**Lista priorytetów (przyjęta przez kandydata, 12 pozycji):** Safari na iOS; pomiar; wstrzymać TikToka na L4; wstrzymać Google Ads na specjalistów do zmiany cennika; uczciwa obietnica L4 w Meta; poranna obsada internistów; komunikacja po wizycie z grupą kontrolną; test zalogowanych; test dodatkowości Meta; cennik i warunki TelemediGO u specjalistów; strata kliknięć; test TelemediGO. Wartości, sposób pomiaru i wdrożenie: `c_szkic.md`, sekcja 3.


# Załącznik D — notatki/DECYZJE.md

# Decyzje

Decyzje podjęte w trakcie pracy (metoda, podziały, narzędzie, hosting) — co wybraliśmy, dlaczego i jakie były alternatywy.

## 2026-10-19 — plan pracy i sposób współpracy

**Decyzja:** pracujemy według planu z `notatki/PLAN.md` (wersja 2, zatwierdzona przez kandydata). Kolejność: wstępna analiza → narzędzie → uzupełnienie analizy → weryfikacja.

**Dlaczego tak:** pierwsza wersja planu zakładała, że Claude wykona całą analizę samodzielnie, a narzędzie zbuduje równolegle z analizą. kandydat ją odrzucił:
- wnioski wyciągamy razem — Claude liczy i pokazuje, po każdym większym kroku jest przegląd, a wnioski weryfikuje konsylium;
- narzędzie dopiero po wspólnym pierwszym etapie analizy, żeby budować je na sprawdzonych definicjach;
- przed rozpoczęciem każdego punktu kandydat decyduje, czy idziemy dalej;
- bez dat w planie.

**Co kandydat dodał do treści planu:** dokładne odtworzenie liczb dashboardu (a nie „mniej więcej”) i zestawienie ich z miarami po oczyszczeniu; rozszerzona kontrola jakości (duplikaty w każdej tabeli osobno, profil zamówień TEST-QA, kliknięcia wobec sesji, czas zamówień wobec czasu płatności); wspólne ustalenie definicji z wariantami przed kohortami; opis obejścia pułapek (start od zera, młode kohorty, sezonowość); analiza tego, co dzieje się po zakupie; wartość priorytetów w marży; stała zasada „najpierw napraw, potem wyłączaj” (dopisana do CLAUDE.md, punkt 9).

**Wykonanie:** osobna sesja Claude Code prowadzi plan punkt po punkcie, w tym samym folderze projektu.

## 2026-10-19 — budowa bazy danych (punkt A1)

**Decyzja:** jedna baza DuckDB `analiza/telemedi.duckdb`, odtwarzana od zera skryptem `python -I analiza/a1_baza.py`. Plik bazy jest poza repozytorium (`.gitignore`), tak jak surowe dane. W repozytorium są skrypt i raport z kontroli.

**Jak zbudowana:**
- Schemat `surowe`: sześć tabel o nazwach jak w słowniku danych (`users`, `sessions`, `events`, `orders`, `go_memberships`, `marketing_spend`). Pliki kwartalne sesji i półroczne zdarzeń są połączone w jedną tabelę.
- Każda kolumna ma typ podany jawnie w skrypcie. Pliki są czytane jako tekst i dopiero potem zamieniane na typy, bez zgadywania. Wartość, której nie da się zamienić, zatrzymuje skrypt z błędem, zamiast po cichu zamienić się w pustą.
- Przy każdym wierszu zostaje plik źródłowy i numer linii w pliku. Będą potrzebne w punkcie A2 do szukania duplikatów na stykach plików kwartalnych i półrocznych.
- Tabela `surowe.pliki`: liczba wierszy, rozmiar i skrót SHA-256 każdego pliku.

**Dlaczego przeliczenie czasu sprawdzamy drugim sposobem (A1):** czas polski liczy DuckDB. Skrypt przelicza ten sam czas jeszcze raz w Pythonie (moduł `zoneinfo`) i porównuje oba wyniki wiersz po wierszu. Wynik: zero różnic w 459 557 sesjach i 494 605 zdarzeniach.

## 2026-10-19 — czyszczenie danych po przeglądzie jakości (punkt A2)

**Decyzja kandydata:** przyjęte obie propozycje z raportu jakości danych (`analiza/wyniki/a2_jakosc.txt`):
- ze zdublowanych zamówień zostaje jedna kopia (604 zamówienia z okna 10–24.06.2026);
- 22 konta testowe są wyłączone ze wszystkiego: zamówień, pacjentów, przychodu, sesji i lejka; kosztu lekarza za testy nie liczymy, wariant z kosztem idzie na listę niewiadomych.

**Zastrzeżenie kandydata:** zamówieniom testowym przyglądamy się jeszcze raz dokładnie na końcu pracy. Dopisane do planu jako pierwszy krok punktu D.

**Jak wykonane:** dane surowe zostają nietknięte w schemacie `surowe`. Oczyszczona kopia powstaje obok, w schemacie `czyste` (skrypt `analiza/a2_czyste.py`). Dzięki temu w A3 da się porównać dashboard liczony na surowo z liczbami po oczyszczeniu, a każdą decyzję o czyszczeniu można cofnąć bez ponownego ładowania danych.

**Otwarte po przeglądzie (czekają na kandydata):** jak czytać sesje zalogowane od wejścia, które nigdy nie kończą się zakupem; jak wyznaczyć okres rozruchu, skoro START10 działa przez całe dwa lata (zmiana w planie, punkt A5); kody rabatowe jako stała kwota w złotych.

## 2026-10-19 — trzy otwarte sprawy z przeglądu A2

**Decyzja kandydata:** przyjęte wszystkie trzy propozycje, z dopiskami. Założenia: `ZALOZENIA.md`, punkty 10–15. Zmiany w planie: A4 (źródło pozyskania i prowizja), A5 (lejek, komunikacja po zakupie, pułapki), C (lista niewiadomych).

1. **Sesje zalogowane od wejścia.** Osobny wiersz w lejku, newsletter i SMS oceniane na poziomie pacjenta. Dopisek kandydata: wyjaśnienie nadal niepełne. Rozważamy trzy odczytania: zepsuta ścieżka zakupu dla zalogowanych, inny cel wizyty albo sposób pomiaru (krok logowania zapisywany każdemu przy kasie). Pogłębienie w A5: na którym kroku odpadają, z jakich stron i kampanii przychodzą (np. przypomnienie o recepcie), czy kupują potem rzadziej niż podobni pacjenci, czas między wyborem terminu a krokiem logowania. Zepsuta ścieżka uderzałaby wyłącznie w powracających, czyli w retencję. Dlatego na liście niewiadomych będą oba odczytania, test rozstrzygający i wartość wariantu pesymistycznego w marży.
2. **Okres rozruchu.** Zgoda na zmianę w A5: nie wyznaczamy okresu rozruchu kodem START10. Dopisek kandydata: nie przesądzamy, że wzrost od października do stycznia to sezon infekcji, bo w tym samym czasie rosną wydatki na kampanie. Sezon i wydatki rozdzielamy w A5.
3. **Kody rabatowe.** Zgoda. Kody kampanii służą jako kontrola reguł przypisania źródła w A4. Dopisek kandydata: prowizję dla rankingu liczymy tą samą regułą co źródło pozyskania, drugi wariant jedną liczbą obok. Jeśli różnica jest mała, nie poświęcamy temu więcej czasu.

**Korekta po uwadze kandydata:** w rozmowie napisałem, że wzrost liczby nowych pacjentów od października 2024 do stycznia 2025 „pasuje do sezonu infekcji”. To było za szybkie. W tej samej tabeli rosną wydatki na kampanie, więc przyczyna jest otwarta.

## 2026-10-19 — wynik odtworzenia dashboardu (punkt A3)

**Decyzja kandydata:** wynik A3 przyjęty. Jako sposób liczenia dashboardu przyjmujemy najprostszą z 14 pasujących kombinacji. Każdy wiersz pliku zamówień to zamówienie, z duplikatami i z testami. Przychód z konsultacji to suma zapłat bez TelemediGO i bez odejmowania zwrotów. Nowy pacjent to konto z pierwszym zamówieniem. Granice okresów są w czasie polskim. Pozostałe pasujące kombinacje różnią się od niej najwyżej o 0,64 punktu procentowego w każdej miarze.

## 2026-10-19 — higiena kontekstu i praca w wielu sesjach

**Decyzja kandydata:** jedna sesja nie przekracza 60% dostępnego kontekstu. Nowy punkt planu albo duże przeliczenia najchętniej robimy w nowej sesji. Sesje komunikują się przez `notatki/PRZEKAZANIE.md`. Zasada jest w `CLAUDE.md`, punkt 14. Sesja prowadząca decyduje na bieżąco, czy zostaje przy punkcie, czy uruchamia nową sesję.

**Pierwsze zastosowanie:** punkt A4 robi nowa sesja. Ta sesja prowadziła A1–A3 z dużymi wydrukami, a A4 to nowy punkt, który wymaga uważnej, wspólnej pracy nad definicjami.

## 2026-10-19 — definicje przed kohortami (punkt A4)

**Decyzja kandydata:** przyjęte definicje z `ZALOZENIA.md`, punkty 16–26. Warianty i ich wpływ policzył `analiza/a4_definicje.py` (raport `analiza/wyniki/a4_definicje.txt`). Pracę prowadziła osobna sesja, zgodnie z zasadą higieny kontekstu.

| Sprawa | Przyjęte | Odrzucone warianty | Dlaczego |
|---|---|---|---|
| Nowy pacjent | pierwsze opłacone zamówienie, dowolny status; status pierwszego zamówienia jako podział kohort | pierwsza jakakolwiek płatność (daje to samo), pierwsze nieanulowane, pierwsza odbyta wizyta | Najbliżej słów zadania: dashboard („pacjenci z pierwszym zakupem”), słownik zamówień i reguła prowizji. Warianty zmieniają wzrost najwyżej o 0,5 punktu procentowego. Status pierwszej wizyty różnicuje powroty, więc lepiej go pokazywać niż wycinać. |
| Powrót | kolejne zamówienie nieanulowane, okna 30/60/90 dni | każde kolejne opłacone, kolejna odbyta wizyta | Anulacja to pełny zwrot przed wizytą, więc pacjent nic nie kupił. Nieodebrana wizyta to zapłata, która zostaje. |
| TelemediGO jako powrót | nie, mierzone osobno | tak | W obecnych danych bez wpływu. Odrębna miara jest czytelniejsza. |
| Przychód | po zwrotach, TelemediGO osobno, zwrot w dniu płatności | przed zwrotami (jak dashboard) | Standard z `CLAUDE.md`, punkt 9. Słownik oddziela TelemediGO od konsultacji. Daty zwrotu w danych nie ma. |
| Źródło pozyskania | pierwsze wejście z anonimowymi sesjami przeglądarek pacjenta; kod kampanii rozstrzyga | pierwsze wejście bez kodu, ostatnie oznaczone wejście, sesja płatności | Najwyższa zgodność z kodami kampanii (97% wobec 67–81%). |
| Prowizja afiliacyjna | ta sama reguła co źródło: 30 825 zł za dwa lata | sam kod RANKING10: 14 875 zł, pokazywany obok jedną liczbą | Zasada z A2. Różnica 15 950 zł to 0,29% przychodu, więc więcej czasu temu nie poświęcamy. |
| Okno po newsletterze i SMS-ie | 24 godziny, na pacjenta, w dowolnej sesji, tylko zamówienia nieanulowane; przy przypisaniu sprzedaży ostatnie wejście przed płatnością; 7 dni obok jako wrażliwość | tylko ta sama sesja, 7 dni | Nadwyżka ponad zwykłe tempo jest prawie cała w tej samej sesji. 24 godziny łapią też zmianę urządzenia. |

**Dopiski kandydata przy przyjęciu:**
1. Przy ekonomii kampanii (koszt pozyskania, wynik na pacjenta) pokazujemy obok wynik według sesji płatności, także w narzędziu. Jeśli wynik kampanii zmienia znak zależnie od reguły, opisujemy go jako niepewny, a nie jako wniosek. Wartość remarketingu trafia na listę niewiadomych razem z testem.
2. Większość wejść z newslettera i SMS-ów to sesje zalogowane bez żadnego zakupu. To dopisujemy do sprawy sesji zalogowanych w A5, bo CRM to nasz główny kanał powrotów.
3. Podstawę przyjęcia definicji nowego pacjenta zapisujemy w założeniach, bo zadanie nie definiuje go wprost (`ZALOZENIA.md`, punkt 16).
4. Recenzję definicji przez Codeksa (model Sol, profil `review`) robimy przed zamknięciem A4, a nie dopiero w punkcie D. Błąd w definicjach znaleziony w środę oznaczałby przeliczanie wszystkiego od nowa. Na tym etapie nie używamy modelu Astra, konsylium ani Fable.

**Recenzja definicji przez Codeksa (model Sol, profil `review`, tylko odczyt), 2026-10-19.** Polecenie: `notatki/recenzje/a4_codex_prompt.md`. Odpowiedź: `notatki/recenzje/a4_codex_odpowiedz.md`. Podsumowanie i nasze decyzje: `notatki/recenzje/a4_codex.md`. Codex nie znalazł błędu, który zmieniałby odpowiedź. Ręcznie sprawdził siedmiu pacjentów. Przyjęliśmy wszystkie siedem uwag:
- trzy poprawki techniczne w kodzie (czas w UTC, pełne 61 dni obserwacji tła, wyjątek dla samego TelemediGO w sesjach zalogowanych);
- trzy doprecyzowania definicji, przyjęte przez kandydata: okno CRM tylko z zamówieniami nieanulowanymi, rozłączne przypisanie sprzedaży do ostatniego wejścia z CRM oraz porównanie okresów na tych samych dniach kalendarzowych (`ZALOZENIA.md` 26 i 27);
- jedną metodę do A5: oddzielenie zmiany struktury pacjentów od zmiany ich zachowania.


## 2026-10-19 — wykonanie punktu A5 w dwóch sesjach

**Decyzja kandydata:** A5 robią dwie sesje równoległe, z podziałem na retencję i pozyskanie. Zakres każdej, zatrzymania i zasady są w `PLAN.md`, sekcja A5, punkt „Wykonanie A5”. Żadna sesja nie przebudowuje bazy, każda pisze we własnych plikach, a wspólne notatki scala sesja prowadząca.

**Dlaczego taki podział (kandydat):** sesja proponowała podział na kohorty z zdarzeniami i lejek z tym, co po zakupie. kandydat połączył to, co dzieje się po zakupie, z retencją, bo przebieg wizyty może zmieniać powroty. Lejek liczy się na sesjach, więc sesja pozyskania nie musi czekać na wspólny moduł definicji.

**Korekta po uwadze kandydata:** w podsumowaniu A4 napisałem, że sama zmiana struktury źródeł nie tłumaczy spadku powrotu w Mecie (z 20,7% do 6,7% w 90 dniach). To hipoteza, nie wniosek: w drugim roku w Mecie pojawiła się nowa kampania na L4 (`meta_prosp_l4_szybko`, od 3.11.2025). Spadek sprawdzamy na poziomie kampanii, a strukturę rozdzielamy co najmniej po kampanii, pierwszej usłudze, zniżce i przebiegu pierwszej wizyty.

## 2026-10-19 — wyniki części pozyskania (punkt A5)

**Decyzja kandydata:** wyniki części pozyskania przyjęte do scalenia, z dwoma dopiskami. Sesja prowadząca scaliła: założenia 28–32, znaleziska (sekcja A5, pozyskanie), plan (punkty B i C), spis skryptów. Pełny opis: `notatki/a5_pozyskanie.md`, sekcja 8.
1. Nagłówek „konwersja spadła, bo zmienił się ruch” nie może gubić awarii zakładania konta w Safari na iOS od 17.03.2026 ani tego, że przeglądarki wbudowane w aplikacje tracą na każdym kroku. To problemy do naprawienia na stronie, a nie tylko „inny ruch”. Ta sama zasada obowiązuje w narzędziu i na liście priorytetów.
2. Do niewiadomych dochodzi strata między kliknięciem reklamy a sesją w Meta i TikToku.

## 2026-10-19 — szkielet narzędzia (punkt B) przed końcem A5

**Decyzja kandydata** (przekazana dosłownie przez pierwszą sesję projektu): „Kiedy scalisz część pozyskania, nie czekaj na koniec retencji. Zacznij szkielet narzędzia (punkt B): układ strony, lejek, oś zdarzeń i jakość danych. Kohorty dołożymy po drugim zatrzymaniu sesji retencji.”

**Co to zmienia w planie:** punkt B startuje przed końcem A5. Pierwsza wersja narzędzia obejmuje układ strony, lejek, oś zdarzeń i jakość danych. Kohorty dochodzą po drugim zatrzymaniu sesji retencji. Technologię strony sesja B uzgadnia z kandydatem na swoim pierwszym zatrzymaniu.

**Warunki do czasu wyboru hostingu** (hosting wybiera kandydat w pierwszej sesji projektu): same pliki statyczne, ścieżki względne, nawigacja przez kotwice w adresie (`#lejek`, `#zdarzenia`), bez serwera. Dane jako statyczne pliki obok strony, każdy poniżej 25 MB, całość jak najlżejsza. Biblioteki zapisane w repozytorium w przypiętej wersji, nie pobierane z sieci. Meta `noindex` i `robots.txt` blokujący indeksowanie. Podgląd lokalny przez `python -m http.server` uruchomiony z folderu `narzedzie/`. Publikacja, dodanie zdalnego repozytorium i push wymagają za każdym razem zgody kandydata.

**Własność plików:** sesja B pisze tylko w `narzedzie/`, we własnym skrypcie eksportu `analiza/b_eksport.py` (z wynikami `analiza/wyniki/b_*`) i we własnej notatce `notatki/b_narzedzie.md`. Nie rusza plików sesji retencji ani pozyskania. Wspólne notatki dalej scala sesja prowadząca.

## 2026-10-19 — hosting narzędzia i repozytorium

**Decyzja kandydata** (przekazana dosłownie przez pierwszą sesję projektu): „Wybieram GitHub: neutralna organizacja, repozytorium prywatne do dnia wysyłki, potem publiczne z GitHub Pages. Założę organizację i podam nazwę.”

**Szczegóły zatwierdzone przez kandydata:**
- Jedno repozytorium w nowej organizacji o neutralnej nazwie, bez nazwiska kandydata i najlepiej bez słowa „Telemedi”. Organizację zakłada kandydat i podaje jej nazwę.
- Narzędzie stoi na GitHub Pages z tego samego repozytorium, pod adresem w rodzaju `https://<organizacja>.github.io/<repozytorium>/`, czyli pod podścieżką. Ścieżki względne są obowiązkowe.
- Publikację robi plik w `.github/workflows/` z oficjalnymi akcjami GitHub Pages (`configure-pages`, `upload-pages-artifact`, `deploy-pages`), który publikuje folder `narzedzie/` przy każdym commicie na master. Plik może powstać już teraz, a zadziała dopiero po włączeniu Pages. Przygotowuje go sesja punktu B.
- Do dnia wysyłki repozytorium jest prywatne i służy jako kopia zapasowa. W dniu wysyłki przełączamy je na publiczne, włączamy Pages i sprawdzamy oba linki (repozytorium i narzędzie) przed wysłaniem maila. Po rekrutacji repozytorium wraca do prywatnych.
- kandydat loguje gita na swoim komputerze do konta GitHub. Utworzenie zdalnego repozytorium, dodanie go do gita, pierwszy i każdy kolejny push, zmiana widoczności i włączenie Pages wymagają osobnej zgody kandydata przy każdej akcji.
- kandydat wie, że publiczna historia commitów pokaże jego imię i nazwisko oraz adres e-mail z ustawień gita. Historii nie przepisujemy.
- Sprawdzenie przed publikacją (pierwsza sesja projektu, 2026-10-19): 60 plików, historia 1,3 MB, surowe dane, paczka i baza DuckDB nie są śledzone, a pliki CSV w `analiza/wyniki/` to zestawienia dzienne bez wierszy pojedynczych pacjentów. **Przed przełączeniem na publiczne sprawdzenie powtarzamy na aktualnym stanie** (punkt D).
- Warunki techniczne strony z wpisu „szkielet narzędzia (punkt B) przed końcem A5” zostają: `noindex`, `robots.txt`, biblioteki w repozytorium w przypiętej wersji, każdy plik danych poniżej 25 MB.

## 2026-10-19 — wynik kroku 3 retencji A5 (struktura a zachowanie)

**Decyzja kandydata:** wynik przyjęty z poprawkami po recenzji Codeksa (Sol), z trzema dopiskami (tekst z notatki sesji retencji):

1. **Zapis na teraz:** większość spadku powrotów wiąże się z pacjentami dwóch nowych kampanii na L4, ale w kampaniach działających w obu latach też jest spadek, którego sprawdzone cechy nie tłumaczą. Podział zależy od reguły źródła, więc w notatkach i w narzędziu podajemy obie wersje (pierwsze wejście z kodem kampanii: 4,6 i 2,0 punktu; sesja płatności: 3,0 i 3,5 punktu).
2. **„Przebieg pierwszej wizyty” w kroku 3 to był tylko status, bez punktualności.** W kroku 4 najpierw: czy spadek w starych kampaniach siedzi w pierwszych wizytach, które zaczęły się z opóźnieniem, według godziny i specjalizacji, zwłaszcza u internisty rano. Czy opóźnienia rosną od startu kampanii na L4 (3.11.2025) i przy kolejnych skokach jej ruchu (17.11, 8.12.2025, 2.01, 19.01.2026 — notatka sesji pozyskania) oraz od startu TikToka (9.02.2026). **Hipoteza kandydata do sprawdzenia, nie do założenia:** nowe kampanie przeciążyły internistów w godzinach, w których przychodzą też pozostali pacjenci. Jeśli tak, koszt tych kampanii obejmuje też gorszą retencję pozostałych pacjentów.
3. **Spadek w starych kampaniach jest w listopadzie–styczniu i w marcu–maju, nie w październiku i lutym.** Przy zdarzeniach w kroku 5 zestawiamy te miesiące z datami startu i skoków kampanii na L4 oraz z opóźnieniami wizyt.

## 2026-10-19 — wyniki kroków 4 i 5 retencji A5 (przebieg wizyty, zdarzenia)

**Decyzja kandydata:** wyniki przyjęte po poprawkach z recenzji Codeksa (Sol), z czterema dopiskami (tekst z notatki sesji retencji):

1. **Kontrolę Codeksa kandydat czyta inaczej:** to, że przy tej samej liczbie wizyt w godzinie obecność pacjentów nowych kampanii nie zmienia opóźnień, jest oczekiwanym wynikiem przy przeciążeniu, bo lekarza nie obchodzi, skąd przyszedł pacjent. Hipotezę rozstrzyga co innego: (a) odsetek spóźnionych porannych wizyt u internisty przy tym samym porannym ruchu w dniu, okres 1 wobec okresu 2; (b) czy w obrębie miesiąca dni z większym ruchem mają więcej opóźnień. Jeśli przy tym samym ruchu opóźnień jest teraz dużo więcej, to spadła poranna przepustowość (obsada, organizacja zapisów albo lekarze zajęci pacjentami spoza B2C), a nie tylko przybyło pacjentów; zapisać jako odczytanie, bez przesądzania przyczyny. **Policzone:** (a) +26,4 punktu procentowego przy tym samym ruchu; (b) brak wyraźnej zależności od ruchu w obrębie miesiąca (krok 4a).
2. **Do listy niewiadomych:** grafiki lekarzy i ich obciążenie spoza B2C. Telemedi ma też pacjentów firmowych, których w tych danych nie ma, a lekarze mogą być wspólni.
3. **Do znalezisk (ważne dla listy priorytetów):** zwroty po wizytach L4 w nowych kampaniach i niska zgoda marketingowa ich pacjentów.
4. **Niespójność lutego zostaje jako trop eksploracyjny**, tak jak opisany w kroku 5.

**Scalenie:** sesja prowadząca scaliła część retencji we wspólnych notatkach: założenia 33–38, znaleziska (sekcja A5, retencja), plan (B i C), przekazanie, spis skryptów. Moduł `analiza/definicje.py` przejmuje sesja prowadząca.


## 2026-10-20 — nowa sesja prowadząca i szkic punktu C na poranny przegląd

**Decyzja kandydata:** po scaleniu ekonomii kampanii rola sesji prowadzącej przechodzi do nowej sesji, bo dotychczasowa jest już długa (zasada 60% kontekstu, `CLAUDE.md` punkt 14). Nowa sesja przygotowuje na poranny przegląd kandydata szkic punktu C:
- **najpierw brakująca analiza TelemediGO:** skąd wzrost sprzedaży o 40%; ile dają opłaty wobec zniżek udzielonych na wizytach; czy wizyty ze zniżką u specjalistów pokrywają koszt lekarza; czy TelemediGO zmienia powroty, z zastrzeżeniem samoselekcji (kupują je pacjenci, którzy i tak planują wracać);
- **lista priorytetów** od najważniejszego, każda pozycja z wartością w marży i założeniami, sposobem pomiaru i czasem wdrożenia, a przy słabych wynikach obie drogi: naprawić albo wyłączyć;
- **lista „czego nie da się rozstrzygnąć”**, z testem przy każdej pozycji;
- **propozycja ostatecznej odpowiedzi „czy to wzrost”** do akceptacji kandydata.

O rundzie konsylium na liście priorytetów kandydat decyduje rano.

**Jak wykonane:** sesja ekonomii kampanii jeszcze wprowadzała uwagę kandydata z przeglądu, gdy przyszła ta decyzja. Żeby nie tracić czasu i nie mieć dwóch piszących we wspólnych notatkach, nowa sesja prowadząca startuje od razu, od analizy TelemediGO we własnych plikach. Ekonomię scala dotychczasowa sesja prowadząca po przyjęciu wyników przez kandydata. Potem jedną wiadomością przekazuje nowej sesji wspólne notatki i całą rolę.

## 2026-10-20 — wyniki ekonomii kampanii (punkt A5)

Decyzja kandydata: wyniki przyjęte do scalenia, z jednym dopiskiem. W narzędziu i przy priorytetach obok wyniku po 90 dniach pokazujemy też wynik po 180 dniach. Pacjenci kampanii na L4 prawie nie wracają, a pozostali tak, więc okno 90 dni zaniża wartość pozostałych kampanii. Recenzja Codeksa (Sol) uwzględniona przed przeglądem: `notatki/recenzje/a5e_codex.md`. Pełny opis: `notatki/a5_ekonomia.md`.

**Scalenie:** sesja prowadząca scaliła ekonomię kampanii we wspólnych notatkach: założenia 39–43, znaleziska (sekcja ekonomia kampanii), plan (B i C), spis skryptów. Punkt A5 jest zamknięty w całości.

## 2026-10-20 — przegląd szkicu punktu C

**Decyzja kandydata:** szkic dobry, kierunek przyjęty (`notatki/c_szkic.md`, commit `bae2920`), z czterema dopiskami (brzmienie kandydata, lekko skrócone):

1. **Odpowiedź „czy to wzrost”:** dodać marżę po kwartałach rok do roku, z wydatkami na kampanie obok. W tabeli miesięcznej narzędzia w VII–IX 2026 marża jest niższa niż rok wcześniej, przy ponad dwa razy wyższych wydatkach. Policzyć to naszym kodem; jeśli się potwierdzi, to zdanie zamyka odpowiedź.
2. **Nowa pozycja listy priorytetów „naprawić pomiar”:** dashboard bez duplikatów i kont testowych, przychód po zwrotach, wyjaśnić i zamknąć kod TEST-QA, sprawdzić, czy lekarze dostają wynagrodzenie za wizyty testowe. Pewna i tania, a bez niej nie da się prowadzić biznesu na kohortach. Wysoko, zaraz po Safari na iOS.
3. **Poranna przepustowość internistów wyżej,** przed test zalogowanych i test Meta. To jedyna dźwignia na retencję pacjentów z kanałów działających w obu latach, a pierwszy krok (grafiki i obsada) jest tani.
4. **Konsylium na liście priorytetów: tak.** Przed wysłaniem dopisać do briefu kandydata „pomiar” i do kontekstu fakt o marży w ostatnim kwartale. Wynik pokazać jako wynik, a nie przegląd modeli.

**Dalej:** po konsylium ostateczna wersja listy do akceptacji kandydata. Po akceptacji odpowiedź, priorytety i niewiadome przekazujemy sesji B do narzędzia.

## 2026-10-19 / 2026-10-20 — narzędzie (punkt B): technologia, układ, druga wersja

Scalone przez sesję prowadzącą z `notatki/b_narzedzie.md` (sekcje 1, 8, 10 i 11), po przyjęciu drugiej wersji przez kandydata.

**2026-10-19, pierwsze zatrzymanie — decyzje kandydata:**
- strona HTML z biblioteką uPlot 1.6.32 zapisaną w repozytorium; odrzucone: ECharts i wykresy bez biblioteki;
- zakładki jak w aplikacji; odrzucone: jedna długa strona;
- wstępna odpowiedź „czy to wzrost” z liczbami A3 i A4; odrzucone: samo miejsce „w przygotowaniu”;
- cztery zasady dla strony: odsetek zawsze z liczebnością i okresem, żadnych liczb wpisanych ręcznie w tekstach, oś zdarzeń w czterech obszarach, próbna publikacja we wtorek wieczorem (po zgodzie kandydata).

**Folder danych strony to `narzedzie/dane_strony/`,** bo `.gitignore` wyklucza każdy folder o nazwie `dane/`. Sesja B zaproponowała zmianę reguły na `/dane/`. **Decyzja sesji prowadzącej: zostawiamy `dane/`,** bo szersza reguła lepiej chroni przed przypadkowym dodaniem surowych danych do repozytorium, a nazwa `dane_strony/` nic nie kosztuje.

**2026-10-20, przegląd szkieletu (słowa kandydata):** „Przejrzałem szkielet i przyjmuję go. A5 jest zamknięte i scalone, więc dobuduj teraz pozostałe zakładki z wyników A5. Kohorty: kohorty dzienne i powroty w 30, 60 i 90 dniach, z filtrami źródło (obie reguły), urządzenie i przeglądarka, pierwsza usługa, zniżka i TelemediGO. Po zakupie: punktualność według pory i specjalizacji, zwroty, oceny. Wynik biznesu: przychód i marża w czasie oraz ekonomia kampanii według obu reguł. Na osi zdarzeń dołóż zdarzenia z retencji i obsługi pacjenta. Priorytety i niewiadome zostaw jako miejsca na wynik punktu C. Te same zasady co dotąd: liczebność przy każdym odsetku, żadnych liczb wpisanych ręcznie. Nic nie publikuj. Zatrzymaj się u mnie z całością rano.”

**2026-10-20, trzy poprawki kandydata do drugiej wersji** (commit `8f7f461`):
1. „Po zakupie” nie mówi już, że dane „pasują do hipotezy przeciążenia, ale jej nie dowodzą”. Pokazuje przyjęte odczytanie: przy tym samym porannym ruchu opóźnień jest o 26,4 punktu procentowego więcej niż rok wcześniej, więc spadła poranna przepustowość (obsada, organizacja zapisów albo lekarze zajęci pacjentami spoza B2C).
2. W „Kohortach” doszła macierz kohort (tygodnie albo miesiące × 7, 14, 30, 60, 90 i 180 dni, mapa ciepła) i krzywa powrotu według dnia od pierwszego zakupu dla okresów A i B, z tymi samymi filtrami.
3. „Wynik biznesu” pokazuje marżę po kwartałach rok do roku z wydatkami obok. Nagłówek mówi, że suma roczna (+26,6%) ukrywa spadek w III kwartale 2026. Strona dokładnie opisuje, że lipiec 2026 jest jeszcze wyższy niż rok wcześniej, i że wrzesień 2025 zawyża bazę przez start sprzedaży TelemediGO w newsletterze.
- Ze strony zniknęły wzmianki o kandydatowi (stronę czyta Telemedi).

**2026-10-20, decyzja kandydata (słowa kandydata):** „Przejrzałem poprawki i przyjmuję drugą wersję narzędzia. Przekaż wynik sesji prowadzącej, żeby scaliła propozycje wpisów z notatki b_narzedzie.md.” Commit przyjęcia: `c9e1621`. Na stronie zostają do uzupełnienia: „Priorytety”, „Czego nie wiemy” i ostateczna odpowiedź „czy to wzrost” (dziś ze znacznikiem „wstępne”) — po akceptacji punktu C.

## 2026-10-20 — punkt C przyjęty: ostateczna lista priorytetów

**Decyzja kandydata:** ostateczna lista 12 priorytetów i 18 niewiadomych przyjęta (`notatki/c_szkic.md`, sekcje 3 i 4), razem z odpowiedzią „czy to wzrost” (sekcja 1). Przed przeniesieniem do narzędzia pięć poprawek spójności (kwoty w niewiadomych 1 i 3, przebieg porannych opóźnień w pozycji 6, numeracja w sekcji 1c, opis punktu C w planie i przekazaniu) — wprowadzone.

**Konsylium (2026-10-20, zgoda kandydata):** 9 z 9 członków, koszt 0,49 USD. Wynik: `notatki/konsylium/c_priorytety/synteza.md`. Co zmieniło na liście: wstrzymanie TikToka i Google Ads na specjalistów wyżej, obietnica L4 tylko w Meta i niżej, nowa pozycja „komunikacja po wizycie z grupą kontrolną”, cennik specjalistów dołączony do warunków TelemediGO, alarmy w pomiarze, zasada budżetu. Zarzuty sprawdzalne w danych sprawdziliśmy kodem; najważniejsza poprawka: kwoty nowych kampanii przeliczone na pełny rok (założenie 53).

**Kto przenosi wynik do narzędzia:** sesja B jest zamknięta, więc robi to nowa sesja „Narzędzie: czy to wzrost, priorytety i niewiadome” (`local_0ea34a6a-6b84-45c6-87b7-e953f33e3452`), zaproponowana przez sesję prowadzącą i uruchomiona przez kandydata. Pisze w plikach narzędzia, wspólnych notatek nie edytuje, zatrzymuje się u kandydata przed próbną publikacją. Sesja prowadząca: `local_ca1efb6a-0cb9-4abb-b08b-9d90f7e7de79`.

**Równolegle (decyzja kandydata):** końcowa weryfikacja liczb Codeksem (model Astra) i README repozytorium dla Telemedi.

## 2026-10-20 — końcowa weryfikacja liczb (Codex, model Astra)

**Decyzja kandydata:** weryfikacja Astrą przed wysłaniem (punkt D). **Wynik:** 45 liczb przeliczonych niezależnie, wszystkie zgodne, bez błędu krytycznego. Siedem ważnych i osiem drobnych uwag dotyczyło pewności zdań i spójności wycen. Wszystkie przyjęte i wprowadzone przez sesję prowadzącą, bez zmiany kierunku żadnego wniosku. Szczegóły: `notatki/recenzje/d_astra.md`. Do odpowiedzi „czy to wzrost” doszło zdanie, że liczba osób powracających w 90 dniach rośnie (3 076 → 3 289), a spada odsetek.

## 2026-10-20 — trzecia wersja narzędzia: wynik punktu C na stronie

Scalone przez sesję prowadzącą z `notatki/b_narzedzie.md` (sekcje 12 i 13). Pracę wykonała sesja „Narzędzie: czy to wzrost, priorytety i niewiadome” (`local_0ea34a6a-6b84-45c6-87b7-e953f33e3452`).

- **Co doszło:** ostateczne „czy to wzrost” bez znacznika „wstępne”, 12 priorytetów z kartami i 18 niewiadomych, za szkicem `notatki/c_szkic.md` w wersji z uwagami Astry (`8ebd2a4`). Liczby na stronie odczytuje z raportów skrypt `analiza/b2_eksport_c.py` i porównuje każdą liczbę z każdego zdania ze szkicem (commity `77c2aef`, `cfa8c57`).
- **Trzy poprawki kandydata (słowa kandydata):** „1. W zakładce »Priorytety« daj na górę tabelę przeglądu, a zasady listy i definicje pod nią. Czytelnik ma najpierw zobaczyć, co robimy. 2. Osobnej zakładki o TelemediGO nie rób. Dodaj za to krótką kartę w »Czy to wzrost«: skąd +40%, czy rośnie odsetek kupujących, ile dają opłaty wobec zniżek i że rozstrzygnie to test z pozycji 12. To jedna z czterech liczb dashboardu, więc odpowiedź powinna ją objąć. 3. W niewiadomej 1 dopisz horyzont tak jak w pozycji 9 (90 i 180 dni).” Wykonane w `f584585`, kontrola 93 liczb, 0 różnic.
- **Decyzja kandydata (słowa kandydata):** „Przyjmuję trzecią wersję, przekaż to sesji prowadzącej. Publikacji na razie nie robimy. To będzie ostatni krok przed wysłaniem, osobno.” Commit przyjęcia: `df4d23c`. Punkt B jest zamknięty co do treści. Publikacja (próbna i właściwa) to ostatni, osobny krok przed wysłaniem, za zgodą kandydata przy każdej akcji.


# Załącznik E — najważniejsze zestawienia liczb (fragmenty raportów z `analiza/wyniki/`)

## E1. Odpowiedź „czy to wzrost”: nowi pacjenci, powroty, marża, wynik biznesu, kwartały (c_priorytety.txt, W1–W4)

```
C — LICZBY DO ODPOWIEDZI „CZY TO WZROST” I DO LISTY PRIORYTETÓW (2026-10-20 14:32), schemat `czyste`
Okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026. Z1K = przyjęta reguła źródła (pierwsze wejście, kod kampanii
rozstrzyga), Z2 = sesja płatności. „Nowe kampanie” = meta_prosp_l4_szybko i tt_prosp_l4_15min (oba na L4, od 3.11.2025
i 9.02.2026).

==============================================================================================================
W1. WIĘCEJ PACJENTÓW: nowi pacjenci w okresach, z nowymi kampaniami i bez nich, obie reguły
==============================================================================================================
      okres  nowi  bez_nowych_z1k  bez_nowych_z2  bezplatne_z1k
          1 16231           16231          16231           7069
          2 24687           17419          19500           7924
     zmiana %: nowi: +52.1%, bez_nowych_z1k: +7.3%, bez_nowych_z2: +20.1%, bezplatne_z1k: +12.1%

==============================================================================================================
W2. LEPSZA RETENCJA: powrót w 30/60/90 dniach na tych samych dniach kalendarzowych (ZALOZENIA.md 27)
==============================================================================================================
   wszyscy:
      p30_o1  p30_o2  n30_o1  n30_o2  p60_o1  p60_o2  n60_o1  n60_o2  p90_o1  p90_o2  n90_o1  n90_o2
        11.0     7.8   14984   22646    19.1    13.7   13941   20823    23.9    17.4   12867   18924
   bez nowych kampanii (Z1K):
      p30_o1  p30_o2  n30_o1  n30_o2  p60_o1  p60_o2  n60_o1  n60_o2  p90_o1  p90_o2  n90_o1  n90_o2
        11.0    10.0   14984   16228    19.1    17.5   13941   15164    23.9    22.0   12867   14031
   bez nowych kampanii (Z2):
      p30_o1  p30_o2  n30_o1  n30_o2  p60_o1  p60_o2  n60_o1  n60_o2  p90_o1  p90_o2  n90_o1  n90_o2
        11.0     9.2   14984   18027    19.1    16.2   13941   16758    23.9    20.4   12867   15414
   tylko nowe kampanie (Z1K):
      p30_o1  p30_o2  n30_o1  n30_o2  p60_o1  p60_o2  n60_o1  n60_o2  p90_o1  p90_o2  n90_o1  n90_o2
         NaN     2.4       0    6418     NaN     3.6       0    5659     NaN     4.1       0    4893
   Liczba pacjentów, którzy wrócili w 90 dniach (kohorty do 2025-07-02 i do 2026-07-02, uwaga Astry): 3076 wobec 3289 (+6.9%), czyli więcej powracających osób przy niższym odsetku.
   Powrót w 90 dniach według pierwszej usługi, bez pacjentów nowych kampanii (przyjęta reguła), te same dni:
                     usluga  p90_o1  p90_o2  n90_o1  n90_o2
       internista_e_recepta    33.4    29.9    3206    3570
                 psychiatra    22.5    24.6     550     605
                   pediatra    22.3    26.3     673     711
              internista_l4    14.6    13.8    2795    2969
     internista_skierowanie    20.2    19.0    1161    1335
           inny_specjalista    25.2    20.6    2325    2549
     internista_konsultacja    23.3    21.5    2157    2292
   Marża na pacjenta w 90 dniach (przed kosztem pozyskania, ZALOZENIA.md 34), te same dni kalendarzowe:
      okres  pacjenci  marza_wszyscy  marza_bez_nowych_z1k  marza_bez_nowych_z2
          1     12867           66.6                  66.6                 66.6
          2     18924           58.3                  66.0                 63.3

==============================================================================================================
W3. WYNIK BIZNESU W OKRESACH KALENDARZOWYCH (zł)
==============================================================================================================
   Marża = przychód z konsultacji po zwrotach + TelemediGO − koszt lekarza − wydatki na kampanie − prowizja afiliacyjna
   (prowizja według przyjętej reguły, ZALOZENIA.md 25). Zamówienia według dnia płatności, zwrot w dniu płatności.
                   pozycja   okres_1   okres_2    zmiana  zmiana_proc
      przychod_konsultacji 2230266.0 3228342.0  998076.0         45.0
             koszt_lekarza 1175700.0 1734825.0  559125.0         48.0
          marza_pierwszych  730408.0 1024348.0  293940.0         40.0
     marza_powt_kohorty_o1  324159.0  152960.0 -171198.0        -53.0
     marza_powt_kohorty_o2       NaN  316209.0       NaN          NaN
              zam_pierwsze   16231.0   24687.0    8456.0         52.0
               zam_powt_o1    8485.0    5289.0   -3196.0        -38.0
               zam_powt_o2       0.0    8515.0    8515.0          inf
                telemedigo  156551.0  219652.0   63101.0         40.0
     telemedigo_kohorty_o1  156551.0   41474.0 -115077.0        -74.0
          wydatki_kampanie  367632.0  649675.0  282043.0         77.0
                  prowizja   15400.0   15425.0      25.0          0.0
                     marza  828085.0 1048069.0  219984.0         27.0
   marza_powt_kohorty_o1 w okresie 2 = marża z zamówień powtórnych pacjentów pozyskanych w okresie 1 (start od zera:
   w okresie 1 takiej bazy z poprzedniego roku nie było).
   Po odjęciu marży powtórnych konsultacji pacjentów pozyskanych w okresie 1: okres 2 895 109 zł (+8.1% wobec okresu 1; bez odjęcia +26.6%).
   Po odjęciu także ich opłat za TelemediGO w okresie 2 (41 474 zł): 853 635 zł (+3.1%).
   To rozbicie księgowe, a nie wynik biznesu, który startuje od zera: nie modeluje zmian wydatków ani zachowania
   pacjentów (recenzja Codeksa).

==============================================================================================================
W4. MARŻA PO KWARTAŁACH ROK DO ROKU, Z WYDATKAMI NA KAMPANIE OBOK (dopisek kandydata 2026-10-21; zł)
==============================================================================================================
   Te same składniki co W3, według kwartału kalendarzowego (czas polski). Prowizja według przyjętej reguły, w kwartale
   pierwszego zamówienia pacjenta. „Przed kampaniami” = marża przed wydatkami na kampanie i prowizją.
     kwartal  zamowienia  przychod  telemedigo  koszt_lekarza  przed_kampaniami  wydatki  prowizja    marza
     2024-Q4        4919  454067.0     25276.0       237125.0          242218.0  87253.0    3625.0 151340.0
     2025-Q1        6826  622234.0     35333.0       323375.0          334192.0 102565.0    4750.0 226877.0
     2025-Q2        6655  595753.0     39249.0       313825.0          321177.0  90383.0    3750.0 227044.0
     2025-Q3        6316  558212.0     56693.0       301375.0          313530.0  87431.0    3275.0 222824.0
     2025-Q4        8105  704672.0     52243.0       380925.0          375990.0 113089.0    3525.0 259375.0
     2026-Q1       10979  937934.0     60164.0       497875.0          500223.0 170625.0    5175.0 324423.0
     2026-Q2       10226  838430.0     57583.0       451550.0          444463.0 184405.0    3500.0 256558.0
     2026-Q3        9181  747306.0     49662.0       404475.0          392493.0 181555.0    3225.0 207713.0
   Rok do roku (kwartał okresu 2 wobec tego samego kwartału rok wcześniej):
     kwartal     marza  marza_rok_wczesniej  marza_zmiana_proc  przed_kampaniami_zmiana_proc   wydatki  wydatki_rok_wczesniej  wydatki_iloraz  marza_bez_telemedigo_zmiana_proc
     2025-Q4 259375.37            151340.47              71.39                         55.23 113089.43               87252.53            1.30                             64.31
     2026-Q1 324423.00            226877.32              42.99                         49.68 170625.40              102565.18            1.66                             37.96
     2026-Q2 256558.10            227043.80              13.00                         38.39 184405.30               90383.10            2.04                              5.95
     2026-Q3 207712.87            222823.66              -6.78                         25.19 181554.93               87431.44            2.08                             -4.86
   Miesiące VII–IX, rok do roku:
     miesiac  przed_kampaniami  wydatki  prowizja   marza
     2025-07           96897.0  29040.0    1025.0 66832.0
     2025-08           96709.0  28419.0    1100.0 67190.0
     2025-09          119925.0  29973.0    1150.0 88802.0
     2026-07          134942.0  60659.0     900.0 73384.0
     2026-08          126245.0  58805.0    1125.0 66315.0
     2026-09          131306.0  62092.0    1200.0 68014.0
   III kwartał 2026 wobec III kwartału 2025: marża 207 713 zł wobec 222 824 zł (-6.8%), wydatki na kampanie 181 555 zł wobec 87 431 zł (×2.08).
   Rozbicie zmiany marży III kwartału (-15 111 zł): marża przed kampaniami 78 963 zł, wydatki na kampanie -94 123 zł, prowizja 50 zł.
   Bez opłat za TelemediGO (we wrześniu 2025 ruszyła ich sprzedaż w newsletterze: 225 zakupów w 23 dni) marża III kwartału
   zmienia się o -4.9% rok do roku, więc spadek nie wynika z samego startu tej kampanii.

==============================================================================================================
```

## E2. Kohorty: powroty, krzywa, marża w miesiącach, kohorty miesięczne, start od zera (a5r_kohorty.txt, sekcje 1–5)

```
1. OKRES 1 WOBEC OKRESU 2 NA TYCH SAMYCH DNIACH KALENDARZOWYCH
==============================================================================================================
      okno_dni  okres kohorty_do     n  powrot_proc  kolejne_zam_na_pac  przychod_na_pac  go_na_pac  koszt_lek_na_pac  marza_na_pac
            30      1 2025-08-31 14984         11.0               0.119            103.3        5.6              53.1          55.9
            30      2 2026-08-31 22646          7.8               0.085             92.5        4.7              47.3          49.9
            60      1 2025-08-01 13941         19.1               0.235            114.3        6.5              59.1          61.6
            60      2 2026-08-01 20823         13.7               0.164            100.1        5.5              51.3          54.3
            90      1 2025-07-02 12867         23.9               0.334            123.3        7.2              63.9          66.6
            90      2 2026-07-02 18924         17.4               0.234            106.9        6.4              55.0          58.3
           180      1 2025-04-03  9125         27.5               0.537            141.7        8.6              74.8          75.5
           180      2 2026-04-03 12591         22.2               0.401            123.9        8.8              65.0          67.7
           365      1 2025-09-30 16231         28.0               0.730            156.2       11.5              84.1          83.6
           365      2 2025-09-30     0          NaN                 NaN              NaN        NaN               NaN           NaN
     Okno 365 dni: okres 2 nie ma jeszcze kohort z pełnym rokiem (n = 0), więc liczba dotyczy tylko okresu 1.

1b. Zmiana okresu 2 wobec okresu 1 (te same dni kalendarzowe)
      okno_dni  n_o1  n_o2  powrot_o1  powrot_o2  powrot_zmiana_pkt  marza_o1  marza_o2  marza_zmiana_zl  marza_zmiana_proc
            30 14984 22646       11.0        7.8               -3.2      55.9      49.9             -6.0              -10.7
            60 13941 20823       19.1       13.7               -5.4      61.6      54.3             -7.3              -11.9
            90 12867 18924       23.9       17.4               -6.5      66.6      58.3             -8.3              -12.5
           180  9125 12591       27.5       22.2               -5.3      75.5      67.7             -7.8              -10.3

==============================================================================================================
2. ODSETEK PACJENTÓW Z POWROTEM DO DNIA d OD PIERWSZEGO ZAKUPU (każdy punkt na tych samych dniach kalendarzowych)
==============================================================================================================
      dzien  n_o1  proc_o1  n_o2  proc_o2  o2_do_o1
          1 16195      0.0 24620      0.0       NaN
          3 16116      0.5 24442      0.3      0.60
          7 15923      2.0 24176      1.5      0.75
         14 15643      5.5 23673      4.0      0.73
         21 15347      7.1 23236      5.1      0.72
         30 14984     11.0 22646      7.8      0.71
         45 14435     15.7 21715     11.1      0.71
         60 13941     19.1 20823     13.7      0.72
         90 12867     23.9 18924     17.4      0.73
        120 11752     26.1 16960     19.5      0.75
        150 10501     26.9 14796     20.9      0.78
        180  9125     27.5 12591     22.2      0.81
        270  4322     28.0  5137     24.9      0.89
        365     0      NaN     0      NaN       NaN
     o2_do_o1 = powrót okresu 2 jako ułamek powrotu okresu 1 (1,00 = bez zmiany).

==============================================================================================================
3. MARŻA I ZAMÓWIENIA NA PACJENTA W KOLEJNYCH 30-DNIOWYCH MIESIĄCACH OD PIERWSZEGO ZAKUPU
==============================================================================================================
   Miesiąc 1 = dni 0–30 (z pierwszym zamówieniem), miesiąc m = dni 30(m−1)+1 … 30m. Każdy miesiąc na tych samych
   dniach kalendarzowych: kohorty, które miały pełne 30m dni. Zamówienia = nieanulowane, w miesiącu 1 bez pierwszego.
      miesiac  n_o1  n_o2  zam_na_pac_o1  zam_na_pac_o2  marza_na_pac_o1  marza_na_pac_o2
            1 14984 22646          0.119          0.085             55.9             49.9
            2 13941 20823          0.114          0.079              5.8              4.1
            3 12867 18924          0.097          0.069              4.8              3.8
            4 11752 16960          0.078          0.054              3.8              2.7
            5 10501 14796          0.065          0.043              3.0              2.1
            6  9125 12591          0.058          0.038              2.6              1.6
            7  7583 10039          0.048          0.033              2.0              1.2
            8  5922  7544          0.045          0.031              2.0              1.0
            9  4322  5137          0.041          0.027              1.8              1.0
           10  2900  3341          0.030          0.023              1.1              0.8
           11  1431  1583          0.028          0.018              1.1              0.7
           12   173   186          0.023          0.000              0.9              NaN
     Szczegóły (przychód po zwrotach, TelemediGO, koszt lekarza na pacjenta):
      miesiac  okres     n  zam_na_pac  przychod_na_pac  go_na_pac  koszt_lek_na_pac  marza_na_pac
            1      1 14984       0.119            103.3        5.6              53.1          55.9
            1      2 22646       0.085             92.5        4.7              47.3          49.9
            2      1 13941       0.114             10.7        0.9               5.8           5.8
            2      2 20823       0.079              7.2        0.7               3.9           4.1
            3      1 12867       0.097              8.9        0.7               4.8           4.8
            3      2 18924       0.069              6.3        0.9               3.5           3.8
            4      1 11752       0.078              7.2        0.7               4.1           3.8
            4      2 16960       0.054              4.9        0.6               2.9           2.7
            5      1 10501       0.065              5.9        0.6               3.5           3.0
            5      2 14796       0.043              3.7        0.6               2.2           2.1
            6      1  9125       0.058              5.0        0.5               2.9           2.6
            6      2 12591       0.038              3.3        0.4               2.1           1.6
            7      1  7583       0.048              3.8        0.5               2.3           2.0
            7      2 10039       0.033              2.8        0.2               1.9           1.2
            8      1  5922       0.045              3.7        0.5               2.3           2.0
            8      2  7544       0.031              2.4        0.2               1.6           1.0
            9      1  4322       0.041              3.4        0.5               2.1           1.8
            9      2  5137       0.027              2.3        0.2               1.5           1.0
           10      1  2900       0.030              2.2        0.3               1.3           1.1
           10      2  3341       0.023              2.1        0.1               1.5           0.8
           11      1  1431       0.028              1.9        0.6               1.4           1.1
           11      2  1583       0.018              1.7        0.1               1.1           0.7
           12      1   173       0.023              1.8        1.0               1.9           0.9
           12      2   186       0.000              NaN        NaN               NaN           NaN

==============================================================================================================
4. KOHORTY MIESIĘCZNE (miesiąc pierwszego zakupu); puste = miesiąc bez pełnego okna dla wszystkich swoich dni
==============================================================================================================
     miesiac  okres    n  powrot30  marza30  powrot60  marza60  powrot90  marza90  marza180  marza365  kol_zam90
     2024-10      1 1285      10.3     56.0      17.9     61.5      22.2     65.5      74.2      81.8      0.315
     2024-11      1 1400      10.9     55.5      19.2     61.7      23.9     65.9      74.0      83.2      0.338
     2024-12      1 1501      12.8     55.5      20.7     61.0      25.6     66.5      77.3      86.6      0.361
     2025-01      1 1628      11.9     55.7      21.0     62.0      26.3     67.4      77.9      88.1      0.356
     2025-02      1 1560       9.9     55.6      18.3     61.3      22.8     65.7      72.8      80.8      0.320
     2025-03      1 1601      12.2     56.8      19.9     62.3      24.1     67.2      76.7      85.6      0.339
     2025-04      1 1430      11.3     55.3      18.0     60.8      22.5     65.1      74.7      80.5      0.311
     2025-05      1 1266      11.5     56.8      19.0     62.9      24.2     68.5      82.9      92.3      0.351
     2025-06      1 1123      10.6     57.2      18.6     62.9      22.7     67.4      76.0      82.5      0.305
     2025-07      1 1116       9.1     54.1      17.6     59.6      21.7     64.7      72.1      76.6      0.289
     2025-08      1 1074       9.7     56.5      16.6     61.1      21.3     66.0      73.6      79.8      0.276
     2025-09      1 1247      10.2     55.5      19.3     61.8      24.1     67.3      77.0      82.4      0.333
     2025-10      2 1383      11.1     57.6      19.2     63.9      23.5     68.4      77.3       NaN      0.328
     2025-11      2 1692       9.5     53.3      15.6     57.6      20.0     61.6      69.9       NaN      0.267
     2025-12      2 1889       8.7     52.9      15.6     57.2      18.9     60.8      66.9       NaN      0.249
     2026-01      2 2423       9.2     52.5      15.7     57.2      20.0     62.5      69.8       NaN      0.279
     2026-02      2 2303       8.8     50.3      15.2     55.2      19.1     59.1      65.3       NaN      0.257
     2026-03      2 2682       7.2     50.0      12.2     53.9      15.6     57.6      62.7       NaN      0.212
     2026-04      2 2256       6.2     47.7      11.4     50.8      14.2     54.0       NaN       NaN      0.192
     2026-05      2 2199       5.9     46.1      10.8     49.5      13.7     52.5       NaN       NaN      0.188
     2026-06      2 1974       6.1     46.5      11.6     49.7      14.7     52.7       NaN       NaN      0.182
     2026-07      2 1958       7.7     48.5      12.7     51.9       NaN      NaN       NaN       NaN        NaN
     2026-08      2 1887       7.5     46.1       NaN      NaN       NaN      NaN       NaN       NaN        NaN
     2026-09      2 2041       NaN      NaN       NaN      NaN       NaN      NaN       NaN       NaN        NaN

4b. Te same miesiące rok do roku (miesiąc okresu 2 wobec tego samego miesiąca okresu 1)
     miesiac_o1 miesiac_o2  n_o1  n_o2  n_zmiana_proc  powrot90_o1  powrot90_o2  powrot90_zmiana_pkt  marza90_o1  marza90_o2  marza90_zmiana_zl
        2024-10    2025-10  1285  1383            7.6         22.2         23.5                  1.3        65.5        68.4                2.9
        2024-11    2025-11  1400  1692           20.9         23.9         20.0                 -3.9        65.9        61.6               -4.3
        2024-12    2025-12  1501  1889           25.8         25.6         18.9                 -6.7        66.5        60.8               -5.7
        2025-01    2026-01  1628  2423           48.8         26.3         20.0                 -6.3        67.4        62.5               -4.9
        2025-02    2026-02  1560  2303           47.6         22.8         19.1                 -3.7        65.7        59.1               -6.6
        2025-03    2026-03  1601  2682           67.5         24.1         15.6                 -8.5        67.2        57.6               -9.6
        2025-04    2026-04  1430  2256           57.8         22.5         14.2                 -8.3        65.1        54.0              -11.1
        2025-05    2026-05  1266  2199           73.7         24.2         13.7                -10.5        68.5        52.5              -16.0
        2025-06    2026-06  1123  1974           75.8         22.7         14.7                 -8.0        67.4        52.7              -14.7
        2025-07    2026-07  1116  1958           75.4         21.7          NaN                  NaN        64.7         NaN                NaN
        2025-08    2026-08  1074  1887           75.7         21.3          NaN                  NaN        66.0         NaN                NaN
        2025-09    2026-09  1247  2041           63.7         24.1          NaN                  NaN        67.3         NaN                NaN

==============================================================================================================
5. START OD ZERA: ZAMÓWIENIA I PRZYCHÓD W OKRESIE WEDŁUG TEGO, KIEDY PACJENT PRZYSZEDŁ
==============================================================================================================
   Okres zamówienia (data płatności) × rodzaj: pierwsze zamówienie (nowy pacjent), powtórne pacjentów z kohort
   okresu 1, powtórne pacjentów z kohort okresu 2. Wszystkie zamówienia (także anulowane); przychód po zwrotach,
   TelemediGO osobno, marża przed kosztem pozyskania.
      okres_zdarzenia                rodzaj  zamowienia  nieanulowane  telemedigo  przychod_zl    go_zl  koszt_lek_zl  marza_zl
                    1            a_pierwsze       16231         15553           0    1490983.0      0.0      760575.0  730408.0
                    1 b_powtorne_kohorty_o1        8485          8133           0     739283.0      0.0      415125.0  324159.0
                    1          d_telemedigo           0             0        1759          0.0 156551.0           0.0  156551.0
                    2            a_pierwsze       24687         23695           0    2075848.0      0.0     1051500.0 1024348.0
                    2 b_powtorne_kohorty_o1        5289          5081           0     414861.0      0.0      261900.0  152960.0
                    2 c_powtorne_kohorty_o2        8515          8173           0     737634.0      0.0      421425.0  316209.0
                    2          d_telemedigo           0             0        2468          0.0 219652.0           0.0  219652.0
     Razem zamówienia: okres 1 24716, okres 2 38491 (+55.7%).

==============================================================================================================
```

## E3. Lejek: typy sesji, kwartały, podziały, rozkład zmiany konwersji (a5p_lejek.txt, sekcje 1–4)

```
1. TYPY SESJI I ICH KROKI (oba okresy razem i osobno)
====================================================================================================
                       typ okres  sesje       k1       k2      k3      k4      k5  zamowienia  usluga  termin  logowanie  wejscie_platn  platnosc  sesja_do_platn
           samo_telemedigo     1    225      0.0      0.0     0.0   225.0   225.0         0.0     0.0     NaN        NaN            NaN     100.0           100.0
           samo_telemedigo     2    461      0.0      0.0     0.0   461.0   461.0         0.0     0.0     NaN        NaN            NaN     100.0           100.0
           samo_telemedigo razem    686      0.0      0.0     0.0   686.0   686.0         0.0     0.0     NaN        NaN            NaN     100.0           100.0
     zalogowana_od_wejscia     1   8026   1662.0     41.0     0.0     0.0     0.0         0.0    20.7     2.5        0.0            NaN       NaN             0.0
     zalogowana_od_wejscia     2  14042   2912.0     71.0     0.0     0.0     0.0         0.0    20.7     2.4        0.0            NaN       NaN             0.0
     zalogowana_od_wejscia razem  22068   4574.0    112.0     0.0     0.0     0.0         0.0    20.7     2.4        0.0            NaN       NaN             0.0
                    zwykla     1 154085  58025.0  42162.0 31098.0 27003.0 24717.0     24717.0    37.7    72.7       73.8           86.8      91.5            16.0
                    zwykla     2 280625  96655.0  68888.0 48886.0 42246.0 38490.0     38490.0    34.4    71.3       71.0           86.4      91.1            13.7
                    zwykla razem 434710 154680.0 111050.0 79984.0 69249.0 63207.0     63207.0    35.6    71.8       72.0           86.6      91.3            14.5
   Sesje zalogowane od wejścia nie mają kroku 3 z definicji; zakup samego TelemediGO ma tylko kroki 4 i 5.

====================================================================================================
2. LEJEK GŁÓWNY (sesje zwykłe) W KWARTAŁACH
====================================================================================================
     kwartal_od  sesje      k1      k2      k3      k4      k5  zamowienia  pierwsze_zam  usluga  termin  logowanie  wejscie_platn  platnosc  sesja_do_platn
        2024-10  37882 13265.0  9228.0  6374.0  5424.0  4919.0      4919.0        4186.0    35.0    69.6       69.1           85.1      90.7            13.0
        2025-01  44656 16621.0 11934.0  8643.0  7486.0  6826.0      6826.0        4789.0    37.2    71.8       72.4           86.6      91.2            15.3
        2025-04  37493 14642.0 10883.0  8270.0  7235.0  6655.0      6655.0        3819.0    39.1    74.3       76.0           87.5      92.0            17.7
        2025-07  34054 13497.0 10117.0  7811.0  6858.0  6317.0      6317.0        3438.0    39.6    75.0       77.2           87.8      92.1            18.5
        2025-10  49419 18688.0 13778.0 10225.0  8869.0  8104.0      8104.0        4963.0    37.8    73.7       74.2           86.7      91.4            16.4
        2026-01  76835 27160.0 19337.0 13872.0 12019.0 10979.0     10979.0        7408.0    35.3    71.2       71.7           86.6      91.3            14.3
        2026-04  79812 26432.0 18705.0 13015.0 11253.0 10226.0     10226.0        6429.0    33.1    70.8       69.6           86.5      90.9            12.8
        2026-07  74559 24375.0 17068.0 11774.0 10105.0  9181.0      9181.0        5886.0    32.7    70.0       69.0           85.8      90.9            12.3

3. PODZIAŁY LEJKA GŁÓWNEGO: OKRES 1 WOBEC OKRESU 2
====================================================================================================
   udzial_ses = udział w sesjach zwykłych okresu w %. Kolumny konwersji jak wyżej, dla okresu 1 i 2;
   zm_* = zmiana w punktach procentowych (okres 2 minus okres 1).

3. urzadzenie
     wartosc  sesje_1  sesje_2  udzial_ses_1  udzial_ses_2  usluga_1  usluga_2  termin_1  termin_2  logowanie_1  logowanie_2  wejscie_platn_1  wejscie_platn_2  platnosc_1  platnosc_2  sesja_do_platn_1  sesja_do_platn_2
      mobile 110641.0 224064.0          71.8          79.8      36.8      33.0      72.3      70.2         73.7         69.5             86.5             86.0        91.5        90.9              15.5              12.6
     desktop  39069.0  49448.0          25.4          17.6      40.1      41.0      73.7      75.1         73.5         75.9             87.8             87.6        91.7        91.7              17.5              18.8
      tablet   4375.0   7113.0           2.8           2.5      38.8      35.1      72.7      71.4         76.6         70.3             86.7             87.0        91.3        90.8              17.1              13.9

3. przegladarka
              wartosc  sesje_1  sesje_2 udzial_ses_1  udzial_ses_2 usluga_1  usluga_2 termin_1  termin_2 logowanie_1  logowanie_2 wejscie_platn_1  wejscie_platn_2 platnosc_1  platnosc_2 sesja_do_platn_1  sesja_do_platn_2
               Chrome  74456.0  96867.0         48.3          34.5     39.7      39.8     73.8      74.8        74.3         75.7            87.2             87.5       91.5        91.8             17.4              18.1
               Safari  34705.0  46737.0         22.5          16.7     40.0      40.0     73.2      74.0        74.1         68.1            86.5             87.3       91.8        91.6             17.2              16.1
            Instagram   9560.0  39744.0          6.2          14.2     19.4      25.5     58.4      61.9        60.4         62.1            80.1             82.0       88.0        89.0              4.8               7.2
               TikTok        -  31535.0            -          11.2        -      23.2        -      60.5           -         59.7               -             81.2          -        86.6                -               5.9
             Facebook   6873.0  28676.0          4.5          10.2     19.9      25.3     56.7      61.4        61.0         61.3            83.1             82.1       88.8        89.1              5.1               7.0
     Samsung Internet  12439.0  16473.0          8.1           5.9     39.5      38.9     72.8      75.2        75.4         75.4            86.9             87.5       91.6        91.7             17.3              17.7
              Firefox   7287.0   9445.0          4.7           3.4     40.0      41.1     73.6      74.8        75.3         76.6            87.9             87.3       91.8        92.3             17.9              19.0
                 Edge   6595.0   8344.0          4.3           3.0     40.5      39.7     74.6      74.9        73.3         75.8            88.4             87.4       92.7        90.7             18.2              17.9
                Opera   2170.0   2804.0          1.4           1.0     38.9      40.1     71.4      76.7        74.5         73.3            84.2             89.1       91.5        91.7             15.9              18.4

3. kanal
                    wartosc  sesje_1  sesje_2 udzial_ses_1  udzial_ses_2 usluga_1  usluga_2 termin_1  termin_2 logowanie_1  logowanie_2 wejscie_platn_1  wejscie_platn_2 platnosc_1  platnosc_2 sesja_do_platn_1  sesja_do_platn_2
            meta_pozyskanie  22292.0  83677.0         14.5          29.8     17.3      22.6     51.0      54.9        55.2         58.9            80.1             81.2       86.9        88.6              3.4               5.3
     wyszukiwarka_bezplatna  40237.0  49489.0         26.1          17.6     31.3      32.8     70.3      73.0        72.4         71.2            87.4             88.8       92.1        92.8             12.8              14.1
          google_ads_ogolne  45223.0  47509.0         29.3          16.9     32.4      32.9     60.3      61.7        66.9         66.0            84.1             85.8       90.2        90.7              9.9              10.4
                     tiktok        -  33470.0            -          11.9        -      21.2        -      54.6           -         58.4               -             81.4          -        86.4                -               4.8
               bezposrednie  22118.0  31752.0         14.4          11.3     60.5      60.8     84.4      86.3        79.1         78.2            91.0             91.3       94.3        94.8             34.6              35.5
           google_ads_marka  12078.0  17170.0          7.8           6.1     57.3      55.8     81.9      83.4        74.9         73.2            88.5             88.6       92.9        93.1             28.9              28.1
           meta_remarketing   3360.0   6099.0          2.2           2.2     62.9      56.5     91.8      90.9        73.5         68.6            88.6             85.3       90.4        89.6             34.0              26.9
          afiliacja_ranking   4741.0   5275.0          3.1           1.9     31.7      31.1     61.0      57.8        64.7         59.0            82.6             83.4       89.4        86.9              9.2               7.7
                        crm   1973.0   3506.0          1.3           1.2    100.0     100.0    100.0     100.0       100.0        100.0            76.1             73.2       79.0        75.9             60.1              55.6
            program_polecen   2063.0   2678.0          1.3           1.0     50.2      47.9     69.1      68.6        72.7         68.7            81.5             88.1       93.4        91.6             19.2              18.2

4. ZMIANA KONWERSJI SESJA DO PŁATNOŚCI: STRUKTURA RUCHU A KONWERSJA W OBRĘBIE GRUP
====================================================================================================
   Rozkład zmiany (okres 2 minus okres 1, punkty procentowe) na dwie części, w każdym podziale osobno:
   efekt_struktury = suma po grupach (udział_2 − udział_1) × konwersja_1;
   efekt_konwersji = suma po grupach udział_2 × (konwersja_2 − konwersja_1).
   Grupy, których nie było w okresie 1 (nowe kampanie), wchodzą w całości do efektu struktury:
   ich konwersja_1 przyjmujemy równą konwersji_2. Rozkład opisuje, nie wskazuje przyczyny.
                     podzial  konwersja_1  konwersja_2  zmiana_pp  efekt_struktury_pp  efekt_konwersji_pp
                  urzadzenie        16.04        13.72      -2.33               -0.16               -2.17
                przegladarka        16.04        13.72      -2.33               -3.00                0.67
     urzadzenie_przegladarka        16.04        13.72      -2.33               -3.00                0.67
         system_przegladarka        16.04        13.72      -2.33               -3.00                0.67
                       kanal        16.04        13.72      -2.33               -2.99                0.66
                    kampania        16.04        13.72      -2.33               -2.44                0.11
              strona_wejscia        16.04        13.72      -2.33               -0.45               -1.87
                     pacjent        16.04        13.72      -2.33               -0.44               -1.89

====================================================================================================
```

## E4. Zdarzenia: lejek i Safari na iOS (a5p_zdarzenia.txt, sekcje 1, 5f, 6)

```
1. ZMIANY KONWERSJI W CAŁYM LEJKU GŁÓWNYM
====================================================================================================
          przejscie       data  przed   po  zmiana  zmiana_wzgl_proc  dni_przed  dni_po  phi  wejscia_po  zamowienia_razem  zamowienia_na_30_dni
          logowanie 2026-03-17   66.0 60.6    -5.4              -8.2        532     198 1.00     30635.0           -1213.0                -183.8
     sesja_do_platn 2026-03-19   10.3  8.5    -1.8             -17.5        101     196 1.04    157990.0           -2840.0                -434.6
             usluga 2026-04-01   31.0 29.3    -1.8              -5.7         34     183 1.00    146402.0            -749.0                -122.8

====================================================================================================

5f. Ile zamówień kosztuje zdarzenie w Safari na iOS: (k3/k2 przed − k3/k2 po) × sesje z wyborem terminu po
    × dalsza konwersja do płatności po (k5/k3). Przed = 1.10.2025–16.03.2026, po = 17.03–30.09.2026 (198 dni).
    Osobno osoby, które jeszcze nie kupowały (pierwsze zamówienia), i pacjenci powracający. Zakłada, że bez
    zdarzenia Safari na iOS trzymałoby poziom sprzed 17.03; nie odejmuje zakupów odłożonych na później (5e).
             kto  przed    po  z_terminem_po  k5_do_k3_po  utracone_zamowienia_198_dni  na_30_dni
            nowi   66.1  45.6         4678.0         72.3                        695.0      105.3
     powracajacy  100.0 100.0         1681.0         90.5                          0.0        0.0
    Sprawdzenie wrażliwości (po recenzji Codeksa): od spadku w Safari na iOS odejmujemy równoległą zmianę tego
    kroku we wszystkich pozostałych przeglądarkach w tych samych okresach (różnica różnic), osoby, które jeszcze
    nie kupowały.
      spadek_ios_safari_pp  spadek_pozostalych_pp  utracone_zamowienia_po_odjeciu_tla  na_30_dni
                      20.6                    2.0                               628.0       95.2

6. STARTY KAMPANII WIDOCZNE W RUCHU: ILE SESJI I ZAMÓWIEŃ W SESJI KAMPANII (wszystkie sesje zwykłe)
====================================================================================================
   Zamówienia według sesji płatności (pierwsze zamówienia osobno); źródło pozyskania według reguły Z1K
   jest w analiza/wyniki/a5p_sezon.txt, sekcja 2. Kampania sprzedaży TelemediGO: zakupy samego TelemediGO.
                  wartosc pierwszy_dzien  dni  sesje  platnosci  zamowienia  pierwsze_zamowienia  sesje_dziennie  zamowienia_dziennie  proc_sesja_do_platn
            crm_go_upsell     2025-09-08  326    992      686.0         0.0                  0.0             3.0                  0.0                69.15
     meta_prosp_l4_szybko     2025-11-03  332  60992     3594.0      3594.0               3594.0           183.7                 10.8                 5.89
        tt_prosp_l4_15min     2026-02-09  234  33470     1593.0      1593.0               1593.0           143.0                  6.8                 4.76
```

## E5. Zdarzenia: retencja i obsługa pacjenta (a5r_zdarzenia.csv)

```
seria,od,do,n,poziom,zmiana,z_przy_wyszukaniu,zbieg_z_data
powrot30_wszyscy,2024-10-01,2025-06-04,11827,11.39,,,
powrot30_wszyscy,2025-06-05,2026-02-09,12514,9.65,-1.74,-4.409,
powrot30_wszyscy,2026-02-10,2026-08-31,14536,6.87,-2.78,-12.608,start TikTok L4 (2026-02-09)
powrot30_stare_kampanie,2024-10-01,2026-08-31,32459,10.48,,,
powrot30_nowe_kampanie,2025-11-03,2026-08-31,6418,2.35,,,start Meta L4 (2025-11-03)
powrot90_stare_kampanie,2024-10-01,2026-07-02,30262,22.85,,,
udzial_nowych_kampanii,2024-10-01,2025-11-02,17676,0.0,,,
udzial_nowych_kampanii,2025-11-03,2025-12-05,1972,7.96,7.96,102.834,start Meta L4 (2025-11-03)
udzial_nowych_kampanii,2025-12-06,2026-02-02,4127,17.35,9.39,11.071,skok Meta L4 (2025-12-08)
udzial_nowych_kampanii,2026-02-03,2026-04-09,5503,29.4,12.05,39.572,start TikTok L4 (2026-02-09)
udzial_nowych_kampanii,2026-04-10,2026-09-30,11640,41.04,11.64,15.214,
rano_internista_ponad15_stare,2024-10-01,2025-11-23,6148,6.33,,,
rano_internista_ponad15_stare,2025-11-24,2025-12-25,615,27.8,21.47,54.845,skok Meta L4 (2025-11-17)
rano_internista_ponad15_stare,2025-12-26,2026-02-01,730,41.92,14.12,10.93,skok Meta L4 (2026-01-02)
rano_internista_ponad15_stare,2026-02-02,2026-09-30,4248,50.24,8.32,4.199,start TikTok L4 (2026-02-09)
pierwsze_zwrot_po_wizycie,2024-10-01,2025-11-12,18260,2.12,,,
pierwsze_zwrot_po_wizycie,2025-11-13,2026-02-22,7142,3.93,1.81,20.115,skok Meta L4 (2025-11-17)
pierwsze_zwrot_po_wizycie,2026-02-23,2026-09-30,15516,6.87,2.94,9.568,
marza30_na_pacjenta_zl,2024-10-01,2025-10-29,17520,56.02,,,
marza30_na_pacjenta_zl,2025-10-30,2026-01-25,5549,53.12,-2.9,-4.845,start Meta L4 (2025-11-03)
marza30_na_pacjenta_zl,2026-01-26,2026-04-07,6064,50.12,-3.0,-17.988,skok Meta L4 (2026-01-19)
marza30_na_pacjenta_zl,2026-04-08,2026-08-31,9744,46.84,-3.28,-5.14,
powrot30_safari_ios_stare,2024-10-01,2026-08-31,6529,11.15,,,

```

## E6. Ekonomia kampanii: obie reguły źródła, 90 i 180 dni (a5e_ekonomia.txt, sekcje 1–2b)

```
1. NAGŁÓWEK: NOWE KAMPANIE NA L4 (meta_prosp_l4_szybko + tt_prosp_l4_15min) WOBEC POZOSTAŁYCH, OBIE REGUŁY
   Grupy: 1 = dwie nowe kampanie na L4; 2 = pozostałe kampanie płatne (Google Ads, Meta lekarz online,
   remarketing Meta); 3 = ranking lekarzy (prowizja); 4 = kanały bezpłatne (bezpośrednie, wyszukiwarka,
   program poleceń, newsletter i SMS). Kolumny: koszt_pozysk_na_pac i wynik_na_pac w zł na pacjenta.

1a. Okno 90 dni
                   grupa regula  okres  nowi  wydatki_zl  prowizja_zl  koszt_pozysk_na_pac  marza_na_pac  wynik_na_pac  wynik_od  wynik_do  wynik_razem_zl  powrot_proc
      1_nowe_kampanie_L4    Z1K      2  4893      159897            0                 32.7          36.3           3.6       2.5       4.7           17589          4.1
      1_nowe_kampanie_L4     Z2      2  3510      159897            0                 45.6          36.1          -9.4     -10.7      -8.1          -33075          4.1
      2_pozostale_platne    Z1K      1  6705      282111            0                 42.1          65.0          22.9      21.7      24.1          153752         23.9
      2_pozostale_platne    Z1K      2  7076      312427            0                 44.2          64.2          20.0      18.8      21.2          141510         21.1
      2_pozostale_platne     Z2      1  6252      282111            0                 45.1          65.7          20.6      19.3      21.9          128866         24.2
      2_pozostale_platne     Z2      2  7141      312427            0                 43.8          62.4          18.7      17.5      19.9          133408         20.1
     3_afiliacja_ranking    Z1K      1   489           0        12225                 25.0          57.2          32.2      28.2      36.1           15723         15.5
     3_afiliacja_ranking    Z1K      2   489           0        12225                 25.0          57.2          32.2      28.0      36.5           15755         16.8
     3_afiliacja_ranking     Z2      1   348           0         8700                 25.0          57.1          32.1      27.4      36.9           11177         16.4
     3_afiliacja_ranking     Z2      2   319           0         7975                 25.0          55.8          30.8      25.7      35.9            9826         16.9
             4_bezplatne    Z1K      1  5673           0            0                  0.0          69.3          69.3      67.9      70.6          393069         24.6
             4_bezplatne    Z1K      2  6466           0            0                  0.0          68.6          68.6      67.3      69.9          443777         23.4
             4_bezplatne     Z2      1  6267           0            0                  0.0          68.0          68.0      66.7      69.3          426026         24.0
             4_bezplatne     Z2      2  7954           0            0                  0.0          64.5          64.5      63.3      65.6          512723         20.8

1b. Okno 180 dni
                   grupa regula  okres  nowi  wydatki_zl  prowizja_zl  koszt_pozysk_na_pac  marza_na_pac  wynik_na_pac  wynik_od  wynik_do  wynik_razem_zl  powrot_proc
      1_nowe_kampanie_L4    Z1K      2  2352       71325            0                 30.3          37.3           7.0       5.4       8.6           16418          4.4
      1_nowe_kampanie_L4     Z2      2  1693       71325            0                 42.1          36.9          -5.2      -7.1      -3.2           -8776          4.2
      2_pozostale_platne    Z1K      1  4717      193425            0                 41.0          72.8          31.8      29.9      33.6          149817         23.9
      2_pozostale_platne    Z1K      2  5130      218658            0                 42.6          72.3          29.7      27.9      31.4          152147         21.2
      2_pozostale_platne     Z2      1  4407      193425            0                 43.9          73.9          30.0      28.0      31.9          132171         24.2
      2_pozostale_platne     Z2      2  5029      218658            0                 43.5          71.0          27.5      25.8      29.3          138414         20.8
     3_afiliacja_ranking    Z1K      1   340           0         8500                 25.0          59.8          34.8      29.4      40.1           11816         14.7
     3_afiliacja_ranking    Z1K      2   352           0         8800                 25.0          62.0          37.0      31.1      42.8           13010         17.0
     3_afiliacja_ranking     Z2      1   246           0         6150                 25.0          60.2          35.2      28.7      41.7            8665         15.0
     3_afiliacja_ranking     Z2      2   229           0         5725                 25.0          60.6          35.6      28.3      42.9            8156         16.6
             4_bezplatne    Z1K      1  4068           0            0                  0.0          79.9          79.9      77.7      82.0          324962         25.2
             4_bezplatne    Z1K      2  4757           0            0                  0.0          78.1          78.1      76.2      80.1          371748         24.1
             4_bezplatne     Z2      1  4472           0            0                  0.0          77.8          77.8      75.8      79.8          348109         24.6
             4_bezplatne     Z2      2  5640           0            0                  0.0          74.2          74.2      72.5      75.9          418604         22.1
   powrot_proc = powrót w 90 dniach (w oknie 180 też 90 dni, dla porównania z częścią retencji).

1c. Pełne okresy (12 miesięcy): nowi pacjenci, wydatki, prowizja i koszt pozyskania (bez marży, bo młode
    kohorty nie mają pełnego okna)
                   grupa regula  okres  nowi  wydatki_zl  prowizja_zl  koszt_pozysk_na_pac
      1_nowe_kampanie_L4    Z1K      2  7268      245787            0                 33.8
      1_nowe_kampanie_L4     Z2      2  5187      245787            0                 47.4
      2_pozostale_platne    Z1K      1  8546      367632            0                 43.0
      2_pozostale_platne    Z1K      2  8878      403888            0                 45.5
      2_pozostale_platne     Z2      1  7917      367632            0                 46.4
      2_pozostale_platne     Z2      2  9062      403888            0                 44.6
     3_afiliacja_ranking    Z1K      1   616           0        15400                 25.0
     3_afiliacja_ranking    Z1K      2   617           0        15425                 25.0
     3_afiliacja_ranking     Z2      1   437           0        10925                 25.0
     3_afiliacja_ranking     Z2      2   405           0        10125                 25.0
             4_bezplatne    Z1K      1  7069           0            0                  0.0
             4_bezplatne    Z1K      2  7924           0            0                  0.0
             4_bezplatne     Z2      1  7877           0            0                  0.0
             4_bezplatne     Z2      2 10033           0            0                  0.0

2. KAMPANIE I KANAŁY BEZPŁATNE: OKRES 1 I OKRES 2, OBIE REGUŁY ŹRÓDŁA

2a. Okno 90 dni (kampanie bez pacjentów w danej regule: nowi = 0)

   reguła Z1K
                     kampania  wydatki_o1  wydatki_o2  nowi_Z1K_o1  koszt_pozysk_na_pac_Z1K_o1  marza_na_pac_Z1K_o1  wynik_na_pac_Z1K_o1  nowi_Z1K_o2  koszt_pozysk_na_pac_Z1K_o2  marza_na_pac_Z1K_o2  wynik_na_pac_Z1K_o2
         meta_prosp_l4_szybko         NaN    113677.0          NaN                         NaN                  NaN                  NaN       3628.0                        31.3                 37.8                  6.5
          gs_generic_erecepta     58242.0     73741.0       1193.0                        48.8                 77.4                 28.6       1233.0                        59.8                 75.5                 15.7
     gs_generic_lekarz_online     72141.0     68786.0       1429.0                        50.5                 65.3                 14.8       1399.0                        49.2                 65.8                 16.6
                gs_generic_l4     54841.0     57180.0       1078.0                        50.9                 65.8                 14.9       1072.0                        53.3                 67.8                 14.4
            tt_prosp_l4_15min         NaN     46220.0          NaN                         NaN                  NaN                  NaN       1265.0                        36.5                 31.9                 -4.6
     meta_prosp_lekarz_online     45530.0     45855.0        786.0                        57.9                 64.7                  6.8        835.0                        54.9                 61.2                  6.3
       gs_generic_specjalisci     36086.0     40319.0        602.0                        59.9                 32.8                -27.1        719.0                        56.1                 32.4                -23.7
                     gs_brand     10792.0     17899.0       1522.0                         7.1                 66.9                 59.9       1715.0                        10.4                 67.1                 56.7
             meta_rmkt_koszyk      4478.0      8647.0         95.0                        47.1                 71.4                 24.3        103.0                        84.0                 65.1                -18.8
                 bezposrednie         0.0         0.0       2448.0                         0.0                 69.1                 69.1       2794.0                         0.0                 69.4                 69.4
               google_organic         0.0         0.0       2644.0                         0.0                 69.4                 69.4       2975.0                         0.0                 67.3                 67.3
                 bing_organic         0.0         0.0        145.0                         0.0                 64.5                 64.5        176.0                         0.0                 75.6                 75.6
              program_polecen         0.0         0.0        436.0                         0.0                 71.3                 71.3        521.0                         0.0                 69.7                 69.7
     rankinglekarzy_affiliate         0.0         0.0        489.0                        25.0                 57.2                 32.2        489.0                        25.0                 57.2                 32.2

   reguła Z2
                     kampania  wydatki_o1  wydatki_o2  nowi_Z2_o1  koszt_pozysk_na_pac_Z2_o1  marza_na_pac_Z2_o1  wynik_na_pac_Z2_o1  nowi_Z2_o2  koszt_pozysk_na_pac_Z2_o2  marza_na_pac_Z2_o2  wynik_na_pac_Z2_o2
         meta_prosp_l4_szybko         NaN    113677.0         NaN                        NaN                 NaN                 NaN      2589.0                       43.9                37.4                -6.5
          gs_generic_erecepta     58242.0     73741.0       859.0                       67.8                78.5                10.7       881.0                       83.7                75.8                -7.9
     gs_generic_lekarz_online     72141.0     68786.0       985.0                       73.2                65.4                -7.9      1003.0                       68.6                65.8                -2.8
                gs_generic_l4     54841.0     57180.0       758.0                       72.3                65.9                -6.4       743.0                       77.0                67.8                -9.1
            tt_prosp_l4_15min         NaN     46220.0         NaN                        NaN                 NaN                 NaN       921.0                       50.2                32.4               -17.8
     meta_prosp_lekarz_online     45530.0     45855.0       585.0                       77.8                66.1               -11.7       632.0                       72.6                60.8               -11.7
       gs_generic_specjalisci     36086.0     40319.0       430.0                       83.9                34.0               -50.0       519.0                       77.7                32.9               -44.7
                     gs_brand     10792.0     17899.0      1927.0                        5.6                66.4                60.8      2407.0                        7.4                62.3                54.9
             meta_rmkt_koszyk      4478.0      8647.0       708.0                        6.3                67.8                61.5       956.0                        9.0                59.7                50.6
                 bezposrednie         0.0         0.0      3201.0                        0.0                67.5                67.5      4182.0                        0.0                64.2                64.2
               google_organic         0.0         0.0      2653.0                        0.0                68.5                68.5      3264.0                        0.0                63.7                63.7
                 bing_organic         0.0         0.0       105.0                        0.0                68.4                68.4       126.0                        0.0                73.5                73.5
              program_polecen         0.0         0.0       308.0                        0.0                68.4                68.4       382.0                        0.0                70.9                70.9
     rankinglekarzy_affiliate         0.0         0.0       348.0                       25.0                57.1                32.1       319.0                       25.0                55.8                30.8

2b. Okno 180 dni (kampanie bez pacjentów w danej regule: nowi = 0)

   reguła Z1K
                     kampania  wydatki_o1  wydatki_o2  nowi_Z1K_o1  koszt_pozysk_na_pac_Z1K_o1  marza_na_pac_Z1K_o1  wynik_na_pac_Z1K_o1  nowi_Z1K_o2  koszt_pozysk_na_pac_Z1K_o2  marza_na_pac_Z1K_o2  wynik_na_pac_Z1K_o2
         meta_prosp_l4_szybko         NaN     61645.0          NaN                         NaN                  NaN                  NaN       2053.0                        30.0                 38.2                  8.2
          gs_generic_erecepta     39393.0     51551.0        816.0                        48.3                 91.1                 42.8        847.0                        60.9                 88.8                 28.0
     gs_generic_lekarz_online     48841.0     49368.0       1019.0                        47.9                 72.4                 24.5       1057.0                        46.7                 74.2                 27.5
                gs_generic_l4     38433.0     43051.0        772.0                        49.8                 68.1                 18.3        779.0                        55.3                 73.2                 17.9
     meta_prosp_lekarz_online     31045.0     31023.0        532.0                        58.4                 67.9                  9.5        575.0                        54.0                 67.5                 13.6
       gs_generic_specjalisci     25353.0     26708.0        413.0                        61.4                 37.1                -24.3        525.0                        50.9                 36.6                -14.3
                     gs_brand      7244.0     11545.0       1092.0                         6.6                 77.9                 71.2       1272.0                         9.1                 76.2                 67.1
            tt_prosp_l4_15min         NaN      9680.0          NaN                         NaN                  NaN                  NaN        299.0                        32.4                 31.2                 -1.1
             meta_rmkt_koszyk      3117.0      5412.0         73.0                        42.7                 83.9                 41.2         75.0                        72.2                 68.1                 -4.1
                 bezposrednie         0.0         0.0       1766.0                         0.0                 79.5                 79.5       2040.0                         0.0                 79.4                 79.4
               google_organic         0.0         0.0       1903.0                         0.0                 79.5                 79.5       2199.0                         0.0                 76.4                 76.4
                 bing_organic         0.0         0.0         93.0                         0.0                 81.5                 81.5        137.0                         0.0                 85.3                 85.3
              program_polecen         0.0         0.0        306.0                         0.0                 84.3                 84.3        381.0                         0.0                 79.0                 79.0
     rankinglekarzy_affiliate         0.0         0.0        340.0                        25.0                 59.8                 34.8        352.0                        25.0                 62.0                 37.0

   reguła Z2
                     kampania  wydatki_o1  wydatki_o2  nowi_Z2_o1  koszt_pozysk_na_pac_Z2_o1  marza_na_pac_Z2_o1  wynik_na_pac_Z2_o1  nowi_Z2_o2  koszt_pozysk_na_pac_Z2_o2  marza_na_pac_Z2_o2  wynik_na_pac_Z2_o2
         meta_prosp_l4_szybko         NaN     61645.0         NaN                        NaN                 NaN                 NaN      1465.0                       42.1                37.8                -4.3
          gs_generic_erecepta     39393.0     51551.0       582.0                       67.7                92.5                24.8       606.0                       85.1                88.1                 3.0
     gs_generic_lekarz_online     48841.0     49368.0       707.0                       69.1                71.9                 2.9       752.0                       65.6                75.7                10.1
                gs_generic_l4     38433.0     43051.0       539.0                       71.3                69.2                -2.1       533.0                       80.8                73.2                -7.6
     meta_prosp_lekarz_online     31045.0     31023.0       394.0                       78.8                69.5                -9.3       443.0                       70.0                68.1                -2.0
       gs_generic_specjalisci     25353.0     26708.0       294.0                       86.2                39.5               -46.7       373.0                       71.6                35.0               -36.6
                     gs_brand      7244.0     11545.0      1373.0                        5.3                76.4                71.2      1661.0                        7.0                71.9                65.0
            tt_prosp_l4_15min         NaN      9680.0         NaN                        NaN                 NaN                 NaN       228.0                       42.5                31.5               -11.0
             meta_rmkt_koszyk      3117.0      5412.0       518.0                        6.0                76.6                70.5       661.0                        8.2                68.1                59.9
                 bezposrednie         0.0         0.0      2289.0                        0.0                76.9                76.9      2938.0                        0.0                73.7                73.7
               google_organic         0.0         0.0      1894.0                        0.0                78.1                78.1      2322.0                        0.0                74.0                74.0
                 bing_organic         0.0         0.0        69.0                        0.0                83.5                83.5        95.0                        0.0                83.5                83.5
              program_polecen         0.0         0.0       220.0                        0.0                83.0                83.0       285.0                        0.0                78.7                78.7
     rankinglekarzy_affiliate         0.0         0.0       246.0                       25.0                60.2                35.2       229.0                       25.0                60.6                35.6
```

## E7. TelemediGO (c_telemedigo.txt, sekcje 0–3; sekcja 4 w skrócie w zakładce „Czy to wzrost”)

```
C — TELEMEDIGO (2026-10-20 14:32), schemat `czyste`
Okres zakupu = dzień zakupu członkostwa (czas polski): okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026.
TelemediGO: 89 zł za 365 dni, 50% zniżki u internisty, 20% u pozostałych; nie odnawia się samo.
Zniżka = cena katalogowa − zapłata. Zniżka efektywna = tylko wizyty, za które zapłata zostaje (odbyte i nieodebrane).
Koszt lekarza: 25 zł internista, 200 zł psychiatra, 100 zł pozostali (pediatra i psycholog też), za wizyty odbyte i
zwrócone po wizycie (ZALOZENIA.md 33). Obserwacje, nie wnioski: przyczyn nie przesądzamy.

==============================================================================================================
0. KONTROLA: liczba zakupów TelemediGO w okresach (A3: 1 759 i 2 468, +40,3%)
==============================================================================================================
      okres  zakupy  oplaty_zl
          1    1759   156551.0
          2    2468   219652.0
     zmiana: +709 zakupów, +40.3%
     każde członkostwo trwa dokładnie 365 dni i kosztuje 89 zł: 0 wyjątków
     zamówienia ze zniżką TelemediGO: 9738, w tym poza okresem ważności członkostwa: 0

==============================================================================================================
1. SKĄD WZROST SPRZEDAŻY O 40%
==============================================================================================================
1a. Typ zakupu. Przy kasie = razem z zamówieniem konsultacji; osobno = sam TelemediGO (strona /telemedigo).
                                   typ  okres_1  okres_2  zmiana  zmiana_proc  udzial_we_wzroscie_proc
        1_kasa_z_pierwszym_zamowieniem    905.0   1089.0   184.0         20.3                     26.0
         2_kasa_z_kolejnym_zamowieniem    629.0    918.0   289.0         45.9                     40.8
     3_osobno_newsletter_crm_go_upsell    225.0    461.0   236.0        104.9                     33.3
                                 razem   1759.0   2468.0   709.0         40.3                    100.0
     przy kasie razem: 1534 → 2007 (+30.8%); osobno razem: 225 → 461

1b. Zakupy osobne w kampanii crm_go_upsell miesiąc po miesiącu (start 8.09.2025; w okresie 1 tylko 23 dni września).
     miesiac  osobno_crm  przy_kasie  razem
     2025-07           0         134    134
     2025-08           0         133    133
     2025-09         225         145    370
     2025-10          27         149    176
     2025-11          34         160    194
     2025-12          46         171    217
     2026-01          36         206    242
     2026-02          33         156    189
     2026-03          47         198    245
     2026-04          40         174    214
     2026-05          40         176    216
     2026-06          50         167    217
     2026-07          39         170    209
     2026-08          38         145    183
     2026-09          31         135    166
     Pierwsze 23 dni kampanii: 225 zakupów; w okresie 2 średnio 38.4 miesięcznie.
     Odczytanie do sprawdzenia: start kampanii zebrał od razu pacjentów, którzy czekali na ofertę, a potem sprzedaż
     osobna ustala się na niższym poziomie. Wysyłek w danych nie ma (widać tylko wejścia), więc nie wiemy, ile
     wiadomości wysłano w kolejnych miesiącach.

1c. Kupujący: pierwsze członkostwo pacjenta wobec drugiego (ponowny zakup po wygaśnięciu pierwszego).
                              kupujacy  okres_1  okres_2  zmiana  udzial_we_wzroscie_proc
            1_nowy_pacjent_pierwsze_go    905.0   1089.0   184.0                     26.0
     2_pacjent_juz_kupowal_pierwsze_go    854.0   1294.0   440.0                     62.1
             3_ponowny_zakup_drugie_go      0.0     85.0    85.0                     12.0

1d. Ponowne zakupy. Członkostwa z okresu 1 wygasają w okresie 2 (ważność 365 dni). Odnowienie = kolejny zakup
    tego samego pacjenta. Liczymy tylko członkostwa, po których wygaśnięciu jest N dni obserwacji.
      dni_po_wygasnieciu  wygasle_czlonkostwa  odnowione  odnowione_proc  pacjenci_z_zamowieniem_po_wygasnieciu  z_zamowieniem_proc
                      30                 1389         36             2.6                                     67                 4.8
                      90                 1140         62             5.4                                    100                 8.8
                     180                  703         44             6.3                                     73                10.4
    Drugie członkostwa (wszystkie są w okresie 2), według typu zakupu i odstępu od wygaśnięcia pierwszego:
                                   typ  n  mediana_dni_od_wygasniecia  min_dni
         2_kasa_z_kolejnym_zamowieniem 66                        33.5        1
     3_osobno_newsletter_crm_go_upsell 19                        34.0       12
    W okresie 2 wygasa 1759 członkostw. Odnowienia nie są przypominane automatycznie (słownik danych),
    a w danych nie widać kampanii przypominającej o wygaśnięciu.

1e. Zakup przy kasie jako odsetek zamówień, przy których pacjent nie miał ważnego członkostwa (zamówienia „do
    oferty”). Rozbicie wzrostu zakupów przy kasie na liczbę zamówień i odsetek kupujących.
      okres            zamowienie  zamowienia_do_oferty  z_go_przy_kasie  odsetek_proc
          1 1_pierwsze_zamowienie                 16231              905          5.58
          2 1_pierwsze_zamowienie                 24687             1089          4.41
          1  2_kolejne_zamowienie                  6784              629          9.27
          2  2_kolejne_zamowienie                  9307              918          9.86
     1_pierwsze_zamowienie: zmiana +184 zakupów = więcej zamówień +471 + zmiana odsetka -287
     2_kolejne_zamowienie: zmiana +289 zakupów = więcej zamówień +234 + zmiana odsetka +55

1f. Odsetek nowych pacjentów, którzy kupują TelemediGO przy pierwszym zamówieniu, według grupy kampanii
    pozyskania (przyjęta reguła źródła, ZALOZENIA.md 22) i według pierwszej usługi.
                    grupa  n_okres_1  n_okres_2  odsetek_okres_1  odsetek_okres_2
     1_meta_lekarz_online       1022       1076             6.46             5.02
         2_meta_l4_szybko          0       5059             0.00             1.48
                 3_tiktok          0       2209             0.00             1.49
       4_pozostale_kanaly      15209      16343             5.52             5.67

                      kanal  n_okres_1  n_okres_2  odsetek_okres_1  odsetek_okres_2
          afiliacja_ranking        616        617             6.01             6.97
               bezposrednie       3069       3399             5.38             5.77
           google_ads_marka       1864       2084             5.53             5.81
          google_ads_ogolne       5540       5597             5.72             5.54
            meta_pozyskanie       1022       6135             6.46             2.10
           meta_remarketing        120        121             5.00             5.79
            program_polecen        550        660             4.91             5.61
                     tiktok          0       2209             0.00             1.49
     wyszukiwarka_bezplatna       3450       3865             5.33             5.51

                     usluga  n_okres_1  n_okres_2  odsetek_okres_1  odsetek_okres_2
           inny_specjalista       2971       3427             5.22             4.44
       internista_e_recepta       4059       4780             8.01             7.03
     internista_konsultacja       2675       3165             4.60             5.12
              internista_l4       3526       9670             4.91             2.81
     internista_skierowanie       1467       1648             3.82             4.00
                   pediatra        845        999             4.38             5.31
                 psychiatra        688        998             5.23             4.81

      okres     n  odsetek   z_go
          1 16231 5.575750  905.0
          2 24687 4.411229 1089.0
     bez pacjentów dwóch nowych kampanii na L4:
      okres     n  odsetek  z_go
          1 16231 5.575750 905.0
          2 17419 5.631781 981.0
     Rozkład zmiany odsetka (punkty procentowe) na komórki grupa kampanii × pierwsza usługa:
     okres_1: +5.58, okres_2: +4.41, zmiana: -1.16, nowe_komorki: -1.22, znikniete: -0.00, struktura: +0.02, zachowanie: +0.04
     „nowe_komorki” = segmenty bez pacjentów w okresie 1 (np. nowe kampanie na L4). Opis, nie przyczyna.

1g. Wszystkie zakupy TelemediGO według kanału pozyskania kupującego (przyjęta reguła źródła).
                      kanal  okres_1  okres_2  zmiana  udzial_we_wzroscie_proc
               bezposrednie    318.0    530.0   212.0                     29.9
     wyszukiwarka_bezplatna    391.0    532.0   141.0                     19.9
          google_ads_ogolne    588.0    711.0   123.0                     17.3
            meta_pozyskanie     97.0    183.0    86.0                     12.1
           google_ads_marka    223.0    307.0    84.0                     11.8
                     tiktok      0.0     33.0    33.0                      4.7
          afiliacja_ranking     51.0     69.0    18.0                      2.5
            program_polecen     73.0     87.0    14.0                      2.0
           meta_remarketing     18.0     16.0    -2.0                     -0.3

==============================================================================================================
2. OPŁATY ZA TELEMEDIGO WOBEC ZNIŻEK UDZIELONYCH NA WIZYTACH
==============================================================================================================
2a. Na członkostwo, w czasie jego ważności (365 dni). Członkostwa z okresu 1 mają pełne okno (wygasają najpóźniej
    30.09.2026). Członkostwa z okresu 2 jeszcze trwają, więc pokazujemy je w 2b w tych samych dniach od zakupu.
                                            miara   okres_1
                                            okres      1.00
                                      czlonkostwa   1759.00
                                        oplaty_zl 156551.00
                              znizka_nominalna_zl 195136.70
                              znizka_efektywna_zl 183939.20
                             zamowienia_ze_znizka   4902.00
                  znizka_efektywna_na_czlonkostwo    104.57
     oplata_minus_znizka_efektywna_na_czlonkostwo    -15.57
                 oplaty_minus_znizki_efektywne_zl -27388.00
                        zamowienia_na_czlonkostwo      2.79
    Przy założeniu, że te same wizyty zostałyby kupione po cenie katalogowej bez TelemediGO, opłaty są o 27 388 zł
    niższe od udzielonych zniżek. To nie jest wynik programu:
    nie wiemy, ile wizyt członkostwo dokłada (sekcja 4), a koszt lekarza za wizyty zwrócone jest w rachunku marży (sekcja 3).
    Okres 1 według typu zakupu i grupy specjalizacji (zniżka efektywna na członkostwo, zł):
                                   typ  czlonkostwa  internista  specjalisci  razem  zamowienia_na_czlonkostwo  bez_zniżki_efektywnej_proc  wizyty_po_zakupie
        1_kasa_z_pierwszym_zamowieniem          905       71.84        17.10  88.94                       2.37                        4.75               1.29
         2_kasa_z_kolejnym_zamowieniem          629      108.46        27.90 136.36                       3.64                        4.13               2.50
     3_osobno_newsletter_crm_go_upsell          225       62.50        16.06  78.56                       2.07                       41.78               1.97
    „wizyty_po_zakupie” = wizyty ze zniżką efektywną poza zamówieniem, przy którym kupiono członkostwo.
    Rozkład zniżki efektywnej na członkostwo (okres 1, zł):
     10%: 19.0, 25%: 44.5, 50%: 66.3, 75%: 153.5, 90%: 246.9, 99%: 398.0; powyżej 89 zł: 38.0% członkostw

2b. Zniżka efektywna narastająco w dniach od zakupu, członkostwa z pełnym oknem N dni (oba okresy).
      dni  czlonkostwa_okres_1  czlonkostwa_okres_2  znizka_na_czlonkostwo_zl_okres_1  znizka_na_czlonkostwo_zl_okres_2
        0               1759.0               2468.0                             32.75                             30.66
       30               1759.0               2302.0                             41.81                             39.85
       90               1759.0               1924.0                             61.27                             58.95
      180               1759.0               1286.0                             81.68                             77.91
      365               1759.0                  NaN                            104.57                               NaN
    Dzień 0 = zamówienie, przy którym kupiono członkostwo (dla zakupów przy kasie), i inne zamówienia tego dnia.
    Przybliżenie dla okresu 2 (dni 181–365 w tej samej proporcji co w okresie 1): 99.7 zł zniżki na członkostwo,
    czyli -10.7 zł opłaty ponad zniżkę na członkostwo. To przybliżenie, nie wynik.

2c. Rok kalendarzowy (widok kasowy): opłaty za członkostwa kupione w okresie wobec zniżek na zamówieniach
    złożonych w tym samym okresie (także na członkostwach kupionych wcześniej).
      okres  oplaty_zl  znizka_nominalna_zl  znizka_efektywna_zl  zamowienia_ze_znizka  oplaty_minus_znizki_efektywne_zl
          1   156551.0             128516.0             120788.0                  3235                           35763.0
          2   219652.0             258813.0             244520.0                  6503                          -24868.0

==============================================================================================================
3. CZY WIZYTY ZE ZNIŻKĄ TELEMEDIGO POKRYWAJĄ KOSZT LEKARZA
==============================================================================================================
3a. Cennik (z danych): cena katalogowa, cena po zniżce TelemediGO, koszt lekarza za wizytę odbytą, marża na wizycie.
     specialization  cena  liczba_cen  cena_z_go  koszt_lekarza  znizka_proc  marza_bez_znizki  marza_z_go
         internista  89.0           1       44.5             25         50.0              64.0        19.5
           pediatra  95.0           1       76.0            100         20.0              -5.0       -24.0
          psycholog  99.0           1       79.2            100         20.0              -1.0       -20.8
         dermatolog 109.0           1       87.2            100         20.0               9.0       -12.8
           neurolog 109.0           1       87.2            100         20.0               9.0       -12.8
             urolog 109.0           1       87.2            100         20.0               9.0       -12.8
          kardiolog 109.0           1       87.2            100         20.0               9.0       -12.8
          ginekolog 119.0           1       95.2            100         20.0              19.0        -4.8
       endokrynolog 119.0           1       95.2            100         20.0              19.0        -4.8
         psychiatra 269.0           1      215.2            200         20.0              69.0        15.2

3b. Rzeczywiste zamówienia ze zniżką TelemediGO wobec zamówień bez zniżki, obie lata razem, z anulacjami,
    nieodebranymi i zwrotami. Marża = przychód po zwrotach − koszt lekarza (także za wizyty zwrócone po wizycie).
                  grupa specialization znizka  zamowienia  zwrocone_po_wizycie_proc  anulowane_proc  przychod_zl  koszt_lekarza_zl  marza_zl  marza_na_zamowienie
           1_internista     internista     go        6950                       1.7             3.9     291786.5          162600.0  129186.5                 18.6
           1_internista     internista   none       31804                       2.9             4.0    2633510.0          743050.0 1890460.0                 59.4
           2_psychiatra     psychiatra     go         523                       1.3             4.2     106308.8           97400.0    8908.8                 17.0
           2_psychiatra     psychiatra   none        2034                       2.1             4.0     513790.0          380800.0  132990.0                 65.4
             3_pediatra       pediatra     go         382                       1.8             3.1      27588.0           35900.0   -8312.0                -21.8
             3_pediatra       pediatra   none        2083                       0.8             4.2     188005.0          195500.0   -7495.0                 -3.6
     4_inny_specjalista     dermatolog     go         588                       1.7             4.8      47960.0           54100.0   -6140.0                -10.4
     4_inny_specjalista     dermatolog   none        2256                       1.1             3.7     234241.0          212000.0   22241.0                  9.9
     4_inny_specjalista   endokrynolog     go         291                       2.1             4.8      25799.2           27100.0   -1300.8                 -4.5
     4_inny_specjalista   endokrynolog   none        1168                       1.5             4.4     130900.0          109300.0   21600.0                 18.5
     4_inny_specjalista      ginekolog     go         587                       1.7             4.8      52264.8           53800.0   -1535.2                 -2.6
     4_inny_specjalista      ginekolog   none        2245                       1.4             4.0     252756.0          210700.0   42056.0                 18.7
     4_inny_specjalista      kardiolog     go         138                       0.7             3.6      11510.4           13100.0   -1589.6                -11.5
     4_inny_specjalista      kardiolog   none         751                       1.1             3.1      78480.0           70300.0    8180.0                 10.9
     4_inny_specjalista       neurolog     go          97                       0.0             5.2       8022.4            9000.0    -977.6                -10.1
     4_inny_specjalista       neurolog   none         633                       1.9             3.3      65400.0           59700.0    5700.0                  9.0
     4_inny_specjalista      psycholog     go          73                       0.0             6.8       5385.6            6800.0   -1414.4                -19.4
     4_inny_specjalista      psycholog   none         385                       1.6             4.4      35838.0           35600.0     238.0                  0.6
     4_inny_specjalista         urolog     go         109                       0.9             1.8       9243.2           10500.0   -1256.8                -11.5
     4_inny_specjalista         urolog   none         598                       1.7             4.8      60931.0           55500.0    5431.0                  9.1

3c. Suma marży na zamówieniach ze zniżką TelemediGO, według grupy specjalizacji i okresu zamówienia (zł).
                  grupa  okres  zamowienia  przychod_zl  koszt_lekarza_zl  znizka_efektywna_zl  marza_zl
           1_internista      1        2322      97232.0           54500.0              97232.0   42732.0
           1_internista      2        4628     194554.0          108100.0             194554.0   86454.0
           2_psychiatra      1         160      32065.0           29800.0               8016.0    2265.0
           2_psychiatra      2         363      74244.0           67600.0              18561.0    6644.0
             3_pediatra      1         135       9500.0           12600.0               2375.0   -3100.0
             3_pediatra      2         247      18088.0           23300.0               4522.0   -5212.0
     4_inny_specjalista      1         618      52655.0           57400.0              13164.0   -4745.0
     4_inny_specjalista      2        1265     107530.0          117000.0              26883.0   -9470.0
     Specjaliści z ceną po zniżce poniżej kosztu lekarza (wszyscy poza internistą i psychiatrą):
      okres  zamowienia  marza_zl  znizka_efektywna_zl
          1         753   -7845.0              15539.0
          2        1512  -14682.0              31405.0
     Scenariusze zmiany warunków (zniżka 0% u tych specjalistów, internista i psychiatra bez zmian), rocznie. To
     scenariusze, nie granice (recenzja Codeksa): pacjenci mogą reagować różnie przy różnych wizytach.
      okres  znikaja_wszystkie  zostaja_wszystkie_po_cenie_katalogowej  znikaja_tylko_zamowienia_ze_strata  kazde_zamowienie_najgorzej  kazde_zamowienie_najlepiej
          1             7845.0                                 15539.0                              9198.0                      6303.0                     17081.0
          2            14682.0                                 31405.0                             18915.0                     10896.0                     35191.0
     „znikaja_wszystkie” = znikają wszystkie te zamówienia (także nieodebrane, które dziś dają marżę bez kosztu lekarza);
     „zostaja_...” = wszystkie zostają po cenie katalogowej; ostatnie dwie kolumny = każde zamówienie osobno znika albo
     zostaje, w wariancie najgorszym i najlepszym. Bez wpływu na sprzedaż członkostw (część pacjentów może rzadziej
     kupować TelemediGO).

==============================================================================================================
```
