# A5 — pozyskanie (sesja „A5: pozyskanie”, 2026-10-19)

Część punktu A5 o pozyskaniu: lejek od sesji do płatności, zdarzenia w lejku, sesje zalogowane od wejścia oraz sezon a wydatki. Równolegle pracuje sesja retencji (`notatki/a5_retencja.md`). Wspólne notatki scala sesja prowadząca. Propozycje wpisów są w sekcji 6.

**Status:** przyjęte przez Kubę 2026-10-19 do scalenia, z dwoma dopiskami (sekcja 8, oba wprowadzone). Czeka na scalenie wspólnych notatek przez sesję prowadzącą. Odczytania, przy których dane dopuszczają więcej niż jedno wyjaśnienie, są opisane jako otwarte.

## Pliki

| Skrypt | Co robi | Wynik |
|---|---|---|
| `analiza/a5p_lejek.py` | Lejek od sesji do płatności: typy sesji, kwartały i miesiące, podziały na urządzenie, przeglądarkę, kanał, kampanię, stronę wejścia i to, czy odwiedzający kupował już wcześniej. Rozkład zmiany konwersji na strukturę ruchu i konwersję w obrębie grup. Czasy między krokami. Od kliknięcia reklamy do sesji (sekcja 6b). Serie dzienne do pliku. Około 85 sekund. | `analiza/wyniki/a5p_lejek.txt`, `analiza/wyniki/a5p_lejek_dzienny.csv.gz` |
| `analiza/a5p_zdarzenia.py` | Wykrywanie dni, od których zmienia się konwersja kroku albo ruch (seria dzienna, podział binarny). Sprawdzenie wybranych zdarzeń na bazie (Safari na iOS, start kampanii Meta na L4, remarketing). Starty kampanii. Uruchamiać po `a5p_lejek.py`. Około 100 sekund. | `analiza/wyniki/a5p_zdarzenia.txt`, `analiza/wyniki/a5p_zdarzenia.csv` |
| `analiza/a5p_zalogowane.py` | Sesje zalogowane od wejścia: skala, krok odpadania, strony i kampanie (z CRM), zakupy po takiej sesji, porównanie z podobnymi pacjentami, czas między wyborem terminu a krokiem 3, dane do wariantu pesymistycznego. Importuje `analiza/definicje.py`. Około 15 sekund. | `analiza/wyniki/a5p_zalogowane.txt` |
| `analiza/a5p_sezon.py` | Sezon a wydatki: nowi pacjenci w kanałach płatnych i bezpłatnych miesiąc po miesiącu, koszt pozyskania kampanii, popyt w wyszukiwarce, cel pierwszej wizyty, zima wobec lata. Importuje `analiza/definicje.py`. | `analiza/wyniki/a5p_sezon.txt`, `analiza/wyniki/a5p_sezon_miesiace.csv` |

Wszystkie skrypty tylko czytają schemat `czyste` i uruchamia się je z głównego folderu przez `python -I`.

---

## 1. Lejek — gdzie i od kiedy tracimy pacjentów

**W skrócie:**
- **Tracimy pacjentów w dwóch miejscach, które trzeba naprawić na stronie.**
  - Przeglądarki wbudowane w aplikacje (Instagram, Facebook, TikTok) tracą pacjentów na każdym kroku lejka. Płacą w 5–7% sesji, a Chrome i Safari w 16–18%.
  - W Safari na iPhone'ach i iPadach od 17.03.2026 gwałtownie spada skuteczność zakładania nowego konta (konta dalej powstają, ale rzadziej; brzmienie poprawione 2026-10-21 po konsylium). Kosztuje to około 95–105 pierwszych zamówień na 30 dni (sekcja 2).
- Konwersja sesji do płatności spadła z 16,0% w okresie 1 (X 2024 – IX 2025) do 13,7% w okresie 2 (X 2025 – IX 2026).
- Rachunkowo prawie cały ten spadek to większy udział ruchu z przeglądarek wbudowanych w aplikacje: z 10,7% do 35,6% sesji, głównie z reklam Meta i TikToka.
- To nie jest tylko „inny ruch”. Ten ruch płaci 2–4 razy rzadziej i traci na każdym kroku lejka, także na zakładaniu konta, a nie tylko na pierwszym kroku. Część tej różnicy da się naprawić na stronie, zanim zaczniemy ciąć budżet (zasada „najpierw napraw, potem wyłączaj”). Ile, pokaże dopiero test (sekcja 5, punkt 4).
- Przed lejkiem jest jeszcze strata między kliknięciem reklamy a sesją w Meta i TikToku (sekcja 5, punkt 6).

**Typy sesji** (`a5p_lejek.txt`, sekcja 1). W danych oczyszczonych jest 457 464 sesji:
- 434 710 zwykłych: 154 085 w okresie 1 i 280 625 w okresie 2;
- 22 068 zalogowanych od wejścia: 8 026 i 14 042. Pokazujemy je osobnym wierszem, a żadna z nich nie kończy się zakupem konsultacji;
- 686 zakupów samego TelemediGO: 225 i 461. Mają tylko kroki 4 i 5, płacą w 100%. Wszystkie wchodzą na `/telemedigo` z kampanii `crm_go_upsell`, od 8.09.2025.

**Kroki lejka głównego** (sesje zwykłe, okres 1 → okres 2, konwersja kroku wobec poprzedniego):

```
krok                              okres 1   okres 2
wybór usługi / sesje                37,7%     34,4%
wybór terminu / usługa              72,7%     71,3%
logowanie albo konto / termin       73,8%     71,0%
wejście na płatność / konto         86,8%     86,4%
płatność przyjęta / wejście         91,5%     91,1%
sesja do płatności                  16,0%     13,7%
```

Najwięcej pacjentów tracimy na pierwszym kroku: dwie trzecie sesji w ogóle nie wybiera usługi. Drugie i trzecie miejsce to wybór terminu i krok konta. Kroki płatności są stabilne przez całe dwa lata.

**Struktura ruchu a konwersja** (`a5p_lejek.txt`, sekcja 4). Zmianę o −2,33 punktu procentowego rozkładamy na dwie części. Rozkład opisuje, co się zmieniło, ale nie wskazuje przyczyny.
- W podziale na przeglądarkę struktura ruchu daje −3,00 punktu procentowego, a konwersja w obrębie przeglądarek +0,67.
- W podziale na kanał: −2,99 i +0,66.
- W podziale na kampanię: −2,44 i +0,11.
- Zmiana w obrębie grup jest więc bliska zera albo dodatnia. Spadek bierze się z tego, że przybyło ruchu, który płaci rzadko.
- Rozkład zależy od wyboru wag. Codex w wersji symetrycznej dostał dla przeglądarek −2,88 i +0,56, czyli ten sam kierunek. Wyniku +0,67 nie czytamy jako poprawy produktu, bo w obrębie przeglądarek zmieniają się też kanały i udział pacjentów powracających.

**Przeglądarki wbudowane w aplikacje** (`a5p_lejek.txt`, sekcja 3, przeglądarka):
- Udział Instagrama, Facebooka i TikToka w sesjach zwykłych urósł z 10,7% do 35,6%.
- Te sesje płacą w 4,8–7,2% przypadków. Chrome płaci w 17,4–18,1%, Safari w 16,1–17,2%.
- Tracą na każdym kroku: usługę wybiera 19–25% sesji (Chrome i Safari około 40%), termin 57–62% (około 74%), krok konta 59–62% (około 75%).
- Oczami marketingu i obsługi pacjenta, zgodnie z zasadą „najpierw napraw”: to pacjent, który klika reklamę w aplikacji i ląduje w okrojonej przeglądarce. Może nie mieć tam zapisanego hasła i może nie chcieć zakładać konta w środku aplikacji. Możliwe naprawy do sprawdzenia, zanim ruszymy budżet: krótsza rejestracja, logowanie przez Google albo Apple, podpowiedź „otwórz w przeglądarce”, zapamiętanie koszyka do dokończenia później.

**Nowi odwiedzający a pacjenci powracający** (`a5p_lejek.txt`, sekcja 2c i sekcja 3, podział „pacjent”):
- Konwersja sesji osób, które jeszcze nie kupowały, stoi przez cały pierwszy rok na 10,8–11,6%.
- Cały lejek rośnie w pierwszym roku z 11,8% (X 2024) do 18,9% (VII 2025). Powód: przybywa sesji pacjentów powracających, które płacą w około 90%. To efekt startu od zera, a nie zdarzenie.
- Od X 2025 konwersja nowych odwiedzających spada do 8,1–8,4% w VI–IX 2026. To głównie zmiana struktury (Meta na L4, TikTok) i Safari na iOS.

---

## 2. Zdarzenia w lejku

Metoda (`a5p_zdarzenia.py`):
- Każdą serię dzienną (podział × wartość × krok) dzielimy binarnie na odcinki o różnym poziomie. Uwzględniamy rozrzut ponad losowość. Kara wynosi 25, a odcinek ma co najmniej 14 dni. Zmiana musi wynosić co najmniej 1 punkt procentowy i 5% względnie.
- Szukamy w sesjach osób, które jeszcze nie kupowały. Bez tego metoda znajduje pozorne „zdarzenia” w pierwszym roku, czyli dorastanie bazy powracających.
- Wpływ liczymy jako: (poziom po − poziom przed) × sesje wchodzące na krok × dalsza konwersja do płatności.

**Lista zdarzeń** (od najważniejszego dla lejka):

1. **17.03.2026 (wtorek): w Safari na iOS gwałtownie spada skuteczność zakładania nowego konta** (brzmienie poprawione 2026-10-21 po konsylium; wcześniej „przestaje działać”). Sprawdzenie: `a5p_zdarzenia.txt`, sekcja 5a–5f.
   - Krok konta po wyborze terminu, u osób, które jeszcze nie kupowały, spada z 66,2% (16.01–16.03.2026) do 45,1% (17.03–15.05.2026) i zostaje na 45,6% do 30.09.2026.
   - Inne przeglądarki tego nie mają. Wszystkie poza Safari na iOS razem spadają z 64,8% do 63,4%. W tym przeglądarki poza iOS i Mac z 64,8% do 63,8%, inne przeglądarki na iOS z 64,4% do 61,2%, Safari na komputerach Mac z 66,4% do 64,0%.
   - Spadek widać w każdym kanale poza TikTokiem, gdzie próba jest za mała (9 i 26 sesji z wyborem terminu). Na przykład wejścia bezpośrednie spadają z 68,0% do 46,4%, ogólne kampanie Google Ads z 65,3% do 39,8%, Meta (pozyskanie) z 65,1% do 42,4%. To nie jest zmiana struktury ruchu.
   - Psuje się zakładanie nowego konta, a nie logowanie. Zakładanie kont w Safari na iOS spada z 1 082 do 668 w 60 dniach. Logowania do istniejących kont stoją (659 i 619), zakupy powtórne też (574 i 586). W innych przeglądarkach zakładanie kont stoi (5 285 i 5 234).
   - Odpadnięci nie wracają później częściej: w ciągu 30 dni w tej samej przeglądarce kupuje 6,4% z nich, przed zdarzeniem 6,7%.
   - Szacunek: około 695 utraconych pierwszych zamówień od 17.03 do 30.09.2026, czyli około 105 na 30 dni. Szacunek zakłada, że bez zdarzenia Safari na iOS trzymałoby poziom z 1.10.2025–16.03.2026 (66,1%).
   - Sprawdzenie wrażliwości (po recenzji Codeksa): po odjęciu równoległego spadku tego kroku w pozostałych przeglądarkach (2,0 punktu procentowego wobec 20,6 w Safari na iOS) wychodzi około 628 zamówień, czyli 95 na 30 dni. To nie jest liczba bezpowrotnie utraconych pacjentów, tylko zamówień w sesjach, w których doszło do wyboru terminu.
   - Przyczyny w danych nie widać. Pasuje do niej zmiana w formularzu rejestracji albo aktualizacja systemu iOS. Test i potrzebne informacje: sekcja 5.
2. **3.11.2025: start kampanii Meta na L4** (`meta_prosp_l4_szybko`). Ruch rośnie skokami 17.11 i 8.12.2025 oraz 2.01 i 19.01.2026.
   - Średnio 183,7 sesji i 10,8 zamówienia dziennie, konwersja 5,89%, razem 3 594 zamówienia.
   - Kampania płaci w lejku lepiej niż starsza kampania Meta (`meta_prosp_lekarz_online`: 3,61% od tego samego dnia). Obie płacą jednak 2–3 razy rzadziej niż wyszukiwarka.
   - Strona `/zwolnienie-l4-online` traci na konwersji tylko przez ten ruch. Bez ruchu z Meta i TikToka płaci 9,45% sesji przed startem, 9,75% po starcie i 9,96% od 9.02.2026.
   - Powroty pacjentów z tej kampanii bada sesja retencji.
3. **9.02.2026: start kampanii TikTok** (`tt_prosp_l4_15min`). Średnio 143,0 sesji i 6,8 zamówienia dziennie, konwersja 4,76%, razem 1 593 zamówienia.
4. **8.09.2025: start kampanii sprzedaży TelemediGO** (`crm_go_upsell`). 686 zakupów samego TelemediGO (69% wejść). Pozostałe wejścia to 306 sesji zalogowanych od wejścia, bez zakupu.
5. **Od początku 2026: remarketing Meta słabnie przez zmianę puli odbiorców.**
   - Sesja do płatności spada z 28,2% (IV kwartał 2025) do 18,9–19,1% (II i III kwartał 2026). Udział przeglądarek wbudowanych w aplikacje rośnie z 13,3% do 22–23%.
   - W obrębie źródła, z którego osoba trafiła na stronę pierwszy raz, konwersja stoi: u osób z Google i Bing 27,9% w okresie 1 i 26,7% w 2026, u osób z Meta (pozyskanie) 11,5% i 13,2%.
   - W 2026 remarketing wraca głównie do osób z Meta i TikToka (sekcja 5h–5i).
6. **Sezon w ruchu bezpłatnym** (sekcja 4, zmiany ruchu). Bezpłatne wyszukiwanie, wejścia bezpośrednie i wyszukiwanie marki rosną o około 30% od 4.11.2024. Spadają o około 30% od 1.05.2025 i znowu rosną od X–XI 2025. Szczegóły w sekcji 4 tej notatki.

**Co nie jest zdarzeniem** (sprawdzone, żeby nie trafiło na oś czasu):
- Wzrost konwersji w pierwszym roku to dorastanie bazy powracających (sekcja 1).
- Spadki kroku konta z 5–12.02.2026 w wejściach bezpośrednich, w wyszukiwaniu marki i na stronie głównej znikają po oddzieleniu Safari na iOS. To ten sam problem z 17.03 plus zmiana struktury. Metoda przesunęła datę, bo zmiana w całym ruchu jest rozmyta.
- Spadek wyboru usługi wiosną 2026 (telefony, Chrome, cały lejek) to zmiana struktury. W obrębie kampanii i stron wejścia wybór usługi stoi przez dwa lata. Tylko wejścia bezpośrednie i wyszukiwanie marki tracą 2–3 punkty procentowe w 2026.
- Kroki płatności (wejście na płatność i płatność przyjęta) są stabilne w każdym podziale.

---

## 3. Sesje zalogowane od wejścia

**W skrócie:**
- Dane nie rozstrzygają między odczytaniami (DECYZJE.md, 2026-10-19, trzy odczytania).
- Kilka faktów przemawia przeciw „zepsutej ścieżce, która odbiera nam zakupy”:
  - pacjenci odpadają przed krokiem konta, a nie na nim;
  - pacjenci z takimi sesjami wracają częściej niż podobni bez nich;
  - krok konta w zakupach powtórnych trwa kilkadziesiąt sekund, a nie 1–2 sekundy.
- Mocna niespójność zostaje: według słownika danych zalogowany pacjent nie ma kroku konta, a w danych krok konta ma każdy zakup bez wyjątku.

Liczby (`a5p_zalogowane.txt`):

- **Kto.** 22 068 sesji i 12 461 pacjentów, średnio 1,77 sesji na pacjenta. Każdy z nich kupował już wcześniej. Po pierwszym zakupie pacjent nie ma ani jednej anonimowej sesji w przeglądarce, w której się logował. Wszystkie 47 387 sesji pacjentów po pierwszym zakupie mają konto. Każda taka sesja jest więc albo zalogowana od wejścia (22 068, bez zakupu), albo jest zakupem samego TelemediGO (686), albo ma krok konta (24 633, z czego około 90% kończy się zakupem).
- **Na którym kroku odpadają** (sekcja 2):
  - usługę wybiera 20,7% sesji w obu okresach;
  - termin wybiera tylko 2,5% i 2,4% z tych, którzy wybrali usługę, czyli 112 sesji przez dwa lata;
  - do kroku konta nie dochodzi żadna.
  - Dla porównania: u osób, które jeszcze nie kupowały, termin wybiera około 70% tych, którzy wybrali usługę.
  - Pacjenci odpadają więc między usługą a terminem, czyli przed krokiem, który miałby być zepsuty.
- **Skąd przychodzą** (sekcja 3):
  - Strony wejścia: `/konto` 66,9%, `/recepta-online` 16,0%, strona główna 15,7%, `/telemedigo` 1,4%. Zakupy powracających wchodzą też na `/lekarz-online` (9,9%) i `/zwolnienie-l4-online` (5,1%), a sesje zalogowane od wejścia nigdy.
  - Kampanie: newsletter reaktywacyjny 26,7%, wejścia bezpośrednie 23,9%, przypomnienie o recepcie 13,2%, bezpłatne wyszukiwanie 13,2%, SMS z przypomnieniem 13,0%, wyszukiwanie marki 8,6%, sprzedaż TelemediGO 1,4%. Z CRM (newsletter i SMS) jest więc 54,3%.
  - Wejścia z CRM są zalogowane od wejścia w 67–68% (reaktywacja 68,3%, recepta 67,2%, SMS 68,4%). Pozostałe 32% to sesje z krokiem konta, czyli sesje zakupu.
  - **Przypomnienie o recepcie:** 2 920 sesji zalogowanych od wejścia. Usługę wybiera 21,0%. Zamówienie pada w ciągu 24 godzin po 0,3% z nich, a w ciągu 7 dni po 2,4%.
- **Co pacjent robi potem** (sekcja 4):
  - Po sesji zalogowanej od wejścia zamówienie w ciągu godziny nie pada nigdy (0,0%), w ciągu doby po 0,2–0,6%, w ciągu 7 dni po 2,6–5,5% (po 4,7% sesji z wyborem terminu z CRM).
  - Po wejściach z CRM to tyle co tło: tło tych samych pacjentów wynosi 0,38% na dobę, czyli około 2,7% w 7 dni, a po sesji z CRM 2,6–2,8%. Po wejściach z innych źródeł zamówienie pada dwa razy częściej niż tło (5,4–5,5%).
  - Szansa zamówienia jest płaska przez dwa tygodnie: 0,45% w pierwszej dobie i 0,50–0,69% w kolejnych.
  - Gdyby to były nieudane próby zakupu, a pacjent obchodził problem (nowa sesja, inne urządzenie), zobaczylibyśmy skok zamówień w pierwszych minutach albo godzinach. Takiego skoku nie ma: tylko 17 sesji z wyborem usługi kończy się zamówieniem w ciągu doby, większość po 6–24 godzinach.
  - Odwrotnie: zamówienie powtórne poprzedza sesja zalogowana od wejścia tylko w 0,5% przypadków w ciągu doby, w 4,0% w ciągu 7 dni i w 16,5% w ciągu 30 dni.
- **Czy kupują rzadziej niż podobni pacjenci** (sekcja 5). Punkt kontrolny: 30 dni po pierwszym zakupie. Do porównania biorę pacjentów bez żadnego zamówienia w dniach 1–30, a wynikiem jest powrót w dniach 31–90. Warstwy: okres, zgoda marketingowa, cel i status pierwszego zamówienia, kanał pozyskania.
  - Z sesją zalogowaną od wejścia w dniach 1–30: 1 142 pacjentów, powrót 15,9%.
  - Bez niej: 30 637 pacjentów, powrót 11,9%, a po wyrównaniu warstw 13,2%.
  - W okresie 2: 16,3% wobec 12,0%.
  - Sprawdzenie wrażliwości, punkt kontrolny 60 dni, wynik w dniach 61–120: 8,6% wobec 7,7%. W okresie 2 po równo, 7,2% i 7,2%.
  - Wniosek: pacjenci z takimi sesjami nie kupują rzadziej. Odwiedzenie strony samo świadczy jednak o zainteresowaniu, więc to porównanie nie wyklucza, że część ich zakupów przepadła. Wynik dotyczy tylko pacjentów bez zamówienia w pierwszych 30 dniach. Codex sprawdził dwa dodatkowe warianty (z miesiącem kohorty w warstwach: 16,5% wobec 13,7%; z wyrównaniem dat kohort: 15,9% wobec 13,2%) i kierunek się nie odwraca.
- **Czas od wyboru terminu do kroku konta** (sekcja 6, sekundy, UTC):
  - pierwsze zakupy: mediana 148, najmniej 35;
  - zakupy powtórne: mediana 83, najmniej 15, 10% sesji poniżej 28;
  - żaden zakup nie ma tego odstępu krótszego niż 11 sekund. Kilkadziesiąt sekund wskazuje na prawdziwe logowanie, a nie na automatyczny zapis;
  - w zakupie powtórnym krok konta nigdy nie jest założeniem nowego konta.
  - **Podejrzane:** w zakupach powtórnych odstęp usługa → termin i odstęp termin → konto mają te same kwantyle (mediana 83, p10 28, p90 137 sekund), a rozkłady są bardzo podobne (Codex: nie identyczne). Wygląda to na cechę generatora danych, a nie na zachowanie ludzi. Długość logowania nie jest więc mocnym dowodem ani za prawdziwym logowaniem, ani przeciw niemu.

**Materiał na listę niewiadomych (punkt C):**
- **Odczytanie A — wizyty „sprawdzam konto”.** Pacjent wchodzi z newslettera, SMS-a albo zakładki `/konto`. Przegląda historię, receptę albo cennik i nie kupuje. Do zakupu przechodzi przez logowanie. Za tym przemawia: krok odpadania przed kontem, brak skoku zakupów po sesji, częstsze powroty tych pacjentów.
- **Odczytanie B — zepsuta albo inaczej mierzona ścieżka zakupu dla zalogowanych.** Przemawia za tym niespójność ze słownikiem danych: krok konta ma każdy z 22 289 zakupów powtórnych, a sesje bez kroku konta nie kończą się zakupem nigdy, w żadnym kwartale. Do tego 20,7% tych sesji wybiera usługę, a prawie nikt potem terminu (2,4% wobec około 70% u nowych). Ten spadek między usługą a terminem może być miejscem awarii dla zalogowanych.
- **Test rozstrzygający:**
  - Na stronie: zalogować się, zamknąć kartę, wrócić zalogowanym z linku w newsletterze i z `/konto`, wybrać usługę i termin, spróbować zapłacić. Sprawdzić, które zdarzenia zapisała analityka.
  - W danych: poprosić o logi błędów i odsłon dla sesji zalogowanych od wejścia, zwłaszcza na kroku wyboru terminu, oraz o znacznik „zalogowany na wejściu” w analityce.
- **Dane wejściowe do wariantu pesymistycznego** (sekcja 7; wartość w marży policzy sesja prowadząca):
  - W grze: 4 557 sesji zalogowanych od wejścia z wyborem usługi, po których pacjent nie złożył zamówienia w ciągu 24 godzin. To 3 890 pacjentów: 1 651 sesji w okresie 1 i 2 906 w okresie 2. Węższa wersja: 112 sesji z wyborem terminu.
  - Przeliczniki: z wyboru usługi do płatności przechodzi 40,9% sesji (wszyscy), z wyboru terminu 56,9%, a sesja powracającego z krokiem konta płaci w 90,5%. Ostatni przelicznik jest wysoki częściowo z definicji grupy (sesje powracających bez kroku konta trafiają do sesji zalogowanych od wejścia), więc nadaje się tylko jako górna granica.
  - Przykład w zamówieniach: 4 557 × 40,9% ≈ 1 864 zamówień w dwa lata. Górna granica: 4 557 × 90,5% ≈ 4 124.
  - Średnia marża zamówienia powtórnego przed kosztem pozyskania: 38,20 zł w okresie 1 i 33,99 zł w okresie 2, a dla zamówień nieanulowanych 39,86 zł i 35,40 zł. To przychód po zwrotach minus koszt lekarza, bez TelemediGO.
  - Zastrzeżenie: ci pacjenci i tak kupują później częściej niż podobni. Część „utraconych” zakupów mogła się tylko przesunąć.

---

## 4. Sezon a wydatki na kampanie

**W skrócie:**
- W kanałach opartych na wyszukiwaniu widać wyraźny sezon: zimą więcej nowych pacjentów niż latem. Dotyczy to wyszukiwania bezpłatnego i płatnego.
- Wydatki rosły jednak w tych samych miesiącach. Wzrostu od października 2024 do stycznia 2025 nie da się rozdzielić na sezon i wydatki.
- Kampania Meta z prawie stałym budżetem ma co najwyżej słaby sezon (+8% pacjentów zimą przy +5% wydatków), dużo słabszy niż kanały bezpłatne.
- Przyczyny nie przesądzamy.

Liczby (`a5p_sezon.txt`):
- **Październik 2024 → styczeń 2025, średnio na dzień** (sekcja 1b, październik 2024 = 100):
  - wydatki na kampanie: 127;
  - nowi pacjenci z kanałów płatnych: 123;
  - z bezpłatnych: 127, w tym z bezpłatnego wyszukiwania 131 i z wejść bezpośrednich 127.
  - Wszystko rośnie o tyle samo, więc ten odcinek sam niczego nie rozstrzyga.
- **Lato 2025 rozdziela oba wpływy lepiej.**
  - Wydatki spadają tylko do 105–108, a nowi pacjenci z kanałów bezpłatnych do 77–79 (VII–VIII), z płatnych do 88–93.
  - Kanały płatne dają latem mniej pacjentów na złotówkę: 24,8 nowego pacjenta na 1 000 zł w październiku 2024, 24,1 w styczniu 2025 i 20,8 w sierpniu 2025.
- **Zima (X–I) wobec lata (V–VIII), średnio na dzień** (sekcja 5b):
  - Rok 1: kanały bezpłatne ×1,37, płatne ×1,20, wydatki ×1,06. Google Ads daje ×1,21 nowych pacjentów przy wydatkach na Google ×1,06.
  - Rok 2: bezpłatne ×1,47. Google Ads ×1,35 przy wydatkach ×1,19.
  - Płatne w roku 2 mają ×0,71, bo latem 2026 działają już Meta na L4 i TikTok.
- **Meta z prawie stałym budżetem** (`meta_prosp_lekarz_online`, sekcje 2 i 5c): wydatki 4,2–5,9 tys. zł miesięcznie przez dwa lata, 70–112 nowych pacjentów miesięcznie. Zimą (X 2024 – I 2025) 351 nowych pacjentów wobec 324 latem (V–VIII 2025), czyli +8,3% przy wydatkach wyższych o 5,3%. W roku 2: 384 wobec 326 przy wydatkach wyższych o 8,4%. Ta kampania nie pokazuje sezonu porównywalnego z kanałami bezpłatnymi (×1,37), ale braku sezonu to porównanie nie dowodzi (uwaga Codeksa). Pasuje to do obrazu: reklama, która sama dociera do ludzi, zależy od sezonu słabiej niż wyszukiwanie.
- **Google Ads zimą: tańsze kliknięcia** (sekcja 5c, uwaga Codeksa). W roku 1 zimą jest 16,0% więcej kliknięć przy wydatkach wyższych o 6,3%, a koszt kliknięcia jest o 8,4% niższy. Część przewagi zimowej Google Ads to więc tańszy ruch. Nowi pacjenci na kliknięcie rosną zimą o dalsze około 4,7% (1,21 / 1,16). W roku 2 koszt kliknięcia zimą jest o 4,0% wyższy niż latem.
- **Cel pierwszej wizyty** (sekcja 4): w kanałach bezpłatnych udział L4 waha się od 16,8% do 24,0% bez wzorca zimowego. Sezon podnosi wszystkie cele wizyt naraz, a nie tylko L4.
- **Wyszukiwanie marki** (sekcja 3): wyświetlenia kampanii na hasło „Telemedi” rosną z 4 054 (X 2024) do 5 625 (I 2025), spadają do 4 472 (VIII 2025) i rosną do 8 765 (I 2026). Rok do roku w styczniu to +56%.
- **Rok do roku** (sekcja 5): nowi z kanałów bezpłatnych latem 1 906 → 2 070 (+8,6%), zimą 2 606 → 3 044 (+16,8%). Z płatnych latem 2 494 → 5 785, zimą 2 985 → 4 135. Wzrost liczby nowych pacjentów rok do roku pochodzi więc głównie z kanałów płatnych.
- **Ograniczenia:**
  - Reklama może podnosić wejścia bezpośrednie i wyszukiwanie marki (efekt marki). Kanały bezpłatne nie są więc w pełni wolne od wpływu wydatków.
  - Dwa lata to jedna zima i jedno lato w każdym roku.
  - Test rozstrzygający: wstrzymanie albo podniesienie budżetu na kilka tygodni w części kraju (grupa kontrolna według regionu) i porównanie nowych pacjentów z regionami bez zmiany.

---

## 5. Otwarte sprawy (do listy niewiadomych i dalszej pracy)

1. **Przyczyna zdarzenia w Safari na iOS.** W danych nie ma wersji systemu ani komunikatów błędów. Potrzebne:
   - lista zmian w produkcie z 16–17.03.2026;
   - logi błędów rejestracji według przeglądarki;
   - powtórzenie rejestracji na iPhonie w Safari.
   Wartość naprawy w marży policzy sesja prowadząca (około 105 pierwszych zamówień na 30 dni, plus ich powroty).
2. **Sesje zalogowane od wejścia:** dwa odczytania, test i dane do wariantu pesymistycznego w sekcji 3.
3. **Sezon a wydatki:** nie rozdzielimy w pełni bez testu z grupą kontrolną (sekcja 4).
4. **Przeglądarki wbudowane w aplikacje:** wartość naprawy (krótsza rejestracja, logowanie przez Google albo Apple) wobec ograniczenia budżetu. Do policzenia w punkcie C razem z powrotami tych pacjentów od sesji retencji.
5. **Ekonomia kampanii** (koszt pozyskania według Z1K i według sesji płatności) — liczy sesja prowadząca po scaleniu. W `a5p_sezon.txt`, sekcja 2, są wydatki, kliknięcia i nowi pacjenci według Z1K w miesiącach.
6. **Strata między kliknięciem reklamy a sesją** (dopisek Kuby; `a5p_lejek.txt`, sekcja 6b).
   - **Co widać.** Na 1 kliknięcie przypada 0,92–0,93 sesji w Google Ads, 0,79–0,82 sesji w Meta i 0,72 sesji w TikToku. Stosunki są stałe w każdym kwartale (ZNALEZISKA.md, A2).
   - **Czego nie wiemy.** Trzy możliwe odczytania:
     - pacjent porzuca stronę, zanim się załaduje, np. przez wolne ładowanie w przeglądarce w aplikacji;
     - w przeglądarkach wbudowanych w aplikacje nie działa śledzenie;
     - platformy reklamowe liczą kliknięcia inaczej niż Google, np. wliczają kliknięcia, które nie prowadzą na stronę.
   - **Obserwacja, która nie rozstrzyga.** W remarketingu Meta tylko 8–29% sesji jest w przeglądarkach wbudowanych, a stosunek jest ten sam (0,80). W pozyskaniu Meta takich sesji jest 65–76%. To pasuje bardziej do sposobu liczenia kliknięć albo do zachowania na samej platformie niż do samej przeglądarki.
   - **W grze, okres 2, górna granica** (gdyby Meta i TikTok miały stosunek z Google, a brakujące osoby zachowywały się jak te, które dotarły):
     - 23 776 sesji;
     - do 1 434 zamówień;
     - 50 494 zł wydatków przypadających na brakujące sesje.
     Najwięcej dotyczy kampanii Meta na L4 (10 738 sesji, 633 zamówienia) i TikToka (9 297 sesji, 442 zamówienia).
   - **Test i dane.**
     - W panelach Meta i TikToka porównać kliknięcia w link i wyświetlenia strony docelowej z sesjami w analityce, dzień po dniu.
     - Logi serwera (wejścia z parametrami UTM) porównać z sesjami w analityce.
     - Zmierzyć czas ładowania strony w przeglądarkach wbudowanych.
     - Na kilka tygodni włączyć zliczanie wejść po stronie serwera.

---

## 6. Propozycje wpisów do wspólnych notatek (scala sesja prowadząca; numerów nie nadaję)

### Do `ZALOZENIA.md`
- **Lejek liczymy na sesjach zwykłych.** To sesje bez konta albo z kontem, które pojawia się dopiero na kroku 3. Sesje zalogowane od wejścia i zakupy samego TelemediGO pokazujemy osobnymi wierszami. Dzień sesji = `dzien_pl`, odstępy między krokami w UTC.
- **„Kupował wcześniej”:** pierwszy zakup pacjenta (konto sesji albo konto przeglądarki, w której kiedykolwiek był zalogowany) przed początkiem sesji. Zdarzeń w lejku szukamy w sesjach osób, które jeszcze nie kupowały. Powód: liczba sesji powracających rośnie od zera przez pierwszy rok i podnosi konwersję całości bez żadnego zdarzenia.
- **Wykrywanie zdarzeń:** podział binarny serii dziennych, opisany w punkcie 2. Wpływ = (poziom po − poziom przed) × sesje wchodzące na krok × dalsza konwersja. To przybliżenie, nie dowód przyczyny. Każde zdarzenie sprawdzamy na bazie: czy jest w każdym kanale, czy to zmiana struktury.
- **Rozkład zmiany konwersji:** efekt struktury i efekt konwersji w obrębie grup. Grupy nowe w okresie 2 (nowe kampanie) wchodzą w całości do efektu struktury.
- **Grupy kanałów przy sezonie:** płatne (Google Ads, Meta, TikTok), afiliacja osobno, bezpłatne (bezpośrednie, bezpłatne wyszukiwanie, program poleceń, CRM). Źródło według Z1K.

### Do `ZNALEZISKA.md` (sekcja A5, pozyskanie)
- Zdarzenie w Safari na iOS od 17.03.2026 (punkt 2.1 tej notatki).
- Spadek konwersji lejka to zmiana struktury ruchu, a nie gorszy lejek w obrębie grup (punkt 1).
- Przeglądarki wbudowane w aplikacje tracą na każdym kroku (punkt 1).
- Remarketing słabnie przez zmianę puli odbiorców (punkt 2.5).
- Sesje zalogowane od wejścia: zero anonimowych sesji pacjenta po pierwszym zakupie; niespójność ze słownikiem danych; jednakowy rozkład odstępów między krokami w zakupach powtórnych, który wygląda na cechę generatora (punkt 3).
- Sezon w kanałach opartych na wyszukiwaniu i co najwyżej słaby sezon w Meta z prawie stałym budżetem (punkt 4).
- Strata między kliknięciem reklamy a sesją w Meta i TikToku: trzy odczytania i dane w grze (punkt 5.6).

### Do `DECYZJE.md`
- Przyjęcie wyników części pozyskania przez Kubę, z dwoma dopiskami (sekcja 8 tej notatki).

### Do `analiza/README.md`
- Cztery wiersze ze skryptami z tabeli „Pliki” na początku tej notatki. Kolejność: `a5p_lejek.py` przed `a5p_zdarzenia.py`.

### Do `PLAN.md`
- A5, część pozyskania: zrobione, przyjęte przez Kubę 2026-10-19 (z dwoma dopiskami). Do punktu C dopisać pozycje z sekcji 5 tej notatki, w tym nową niewiadomą: strata między kliknięciem reklamy a sesją. Do punktu B: oś czasu zdarzeń, lejek w podziałach z pliku `a5p_lejek_dzienny.csv.gz`, osobne wiersze sesji zalogowanych i zakupów samego TelemediGO.

---

## 7. Recenzja Codeksa (model Sol)

**Poprawka w trakcie recenzji:** Codex wskazał błąd w `a5p_zalogowane.py` (sekcje 3d i 4). Odsetki zamówień po sesji zalogowanej od wejścia liczyły się tylko wśród sesji, po których pacjent kiedykolwiek złożył zamówienie. Sesje bez żadnego późniejszego zamówienia wypadały z mianownika (średnia pomija wartości puste). Przykład: po wejściach z CRM bez kroków wyszło 14,3% zamówień w 7 dni, a poprawnie jest 2,6%. Poprawione (brak zamówienia liczymy jako „nigdy”), liczby w sekcji 3 tej notatki są już po poprawce. Sekcje 4b2 i 7 miały poprawny mianownik od początku.

Polecenie: `notatki/recenzje/a5p_codex_prompt.md`. Odpowiedź: `notatki/recenzje/a5p_codex_odpowiedz.md`. Podsumowanie i co z tym zrobiliśmy: `notatki/recenzje/a5p_codex.md`. Codex potwierdził własnym kodem wszystkie pięć zestawów liczb; poprawki i zawężenia są już w tej notatce.

## 8. Dopiski i decyzje Kuby

**2026-10-19, przegląd części pozyskania.** Kuba przyjął wyniki do scalenia, z dwoma dopiskami (tekst wklejony do rozmowy):

1. Nagłówek „konwersja spadła, bo zmienił się ruch, a nie dlatego, że lejek działa gorzej” ma nie gubić dwóch rzeczy:
   - awarii zakładania konta w Safari na iOS od 17.03.2026;
   - tego, że przeglądarki wbudowane w aplikacje tracą na każdym kroku. To też jest problem do naprawienia na stronie, a nie tylko „inny ruch”.
   → Przepisane w sekcji 1 („W skrócie”). Ta sama zasada obowiązuje przy opisie lejka w narzędziu i na liście priorytetów.
2. Do niewiadomych dopisać stratę między kliknięciem reklamy a sesją. W Mecie i TikToku na kliknięcie przypada wyraźnie mniej sesji niż w Google (A2). Nie wiemy, czy to porzucenie przed załadowaniem strony, czy luka w śledzeniu w przeglądarkach wbudowanych w aplikacje.
   → Sekcja 5, punkt 6. Wyliczenie w `a5p_lejek.txt`, sekcja 6b. Dodałem trzecie odczytanie (inne liczenie kliknięć przez platformy) i obserwację z remarketingu Meta.
