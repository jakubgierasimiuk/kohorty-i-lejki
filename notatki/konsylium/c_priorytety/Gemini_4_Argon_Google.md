# Gemini 4 Argon (Google) — google/gemini-4-argon

### Diagnoza wykonawcza: dlaczego biznes hamuje?

Zestawienie danych z obu okresów pokazuje klasyczny kryzys wzrostu opartego na złej ekonomii jednostkowej. Choć w całym okresie 2 marża wzrosła o 27% (do 1 048 tys. zł), **w III kwartale 2026 biznes wszedł w fazę kurczenia się wyniku rok do roku (−6,8% marży, a bez programu zniżkowego −4,9%) przy ponad dwukrotnie wyższych wydatkach reklamowych (2,08× r/r)**. 

Złożyły się na to cztery zjawiska:
1. **Zalanie lejka niskomarżowymi pacjentami L4** (Meta od XI 2025, TikTok od II 2026) – odpowiadają za 29% nowych pacjentów, mają 4% retencji, 17,4% zwrotów (za które i tak płacimy lekarzom po 25 zł) i niemal połowę niższą marżę (36 zł vs 66 zł).
2. **Zepsucie konwersji w Safari na iOS od 17.03.2026 (E)** – zbiegło się dokładnie z początkiem II kwartału 2026, w którym dynamika marży załamała się z +43% do +13%, bo zaczęliśmy tracić 1/3 już opłaconego w reklamach ruchu z iPhone'ów.
3. **Zatkanie porannej przepustowości internistów od XI 2025 (G)** – zbiegło się co do miesiąca ze startem kampanii Meta na L4 (3.11.2025), wypychając z porannych grafików regularnych, powracających pacjentów.
4. **Ślepota decyzyjna (K)** – codzienny raport zawyża dynamikę zamówień (+61% vs +56%) i przychodów (+50% vs +45%), ukrywając zwroty i koszty wizyt testowych.

---

### 1. Ranking działań od najważniejszego (A–K)

**Kryterium priorytetyzacji:** 
$$\text{Priorytet} = \frac{\text{Skorygowana Wartość Oczekiwana (EV)} \times \text{Pewność efektu}}{\text{Czas wdrożenia i koszt alternatywny}}$$
Uwzględniam też **zależności logiczne**: najpierw ucinamy czyste krwawienie gotówki (1 dzień pracy) i naprawiamy błędy techniczne w lejku, potem naprawiamy cennik i pomiar, a na końcu prowadzimy wielotygodniowe eksperymenty.

| Poz. | Działanie | Skorygowana wartość roczna (marża) | Po czym poznamy, że zadziałało (miernik sukcesu) | Czas wdrożenia | Uzasadnienie pozycji |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1.** | **E. Naprawa zakładania konta w Safari (iPhone)** | **+105 do +135 tys. zł** *(wycena w briefie zaniżona o CAC – patrz sekcja 2)* | Powrót konwersji kroku „wybór terminu $\rightarrow$ konto” w Safari iOS z 46% do ~66% w ciągu 48h od wdrożenia. | **2–4 dni** (1–2 dni diagnoza + fix) | Najwyższy pewny zwrot. Ruch jest już opłacony w kampaniach, więc odzyskujemy marżę brutto przed CAC, a nie marżę netto. |
| **2.** | **B. Wyłączenie kampanii TikTok na L4** | **+18,6 do +48,3 tys. zł** *(zannualizowane; przy kanibalizacji do +129 tys. zł)* | Spadek wydatków reklamowych o budżet TikToka; spadek odsetka zwrotów L4; poprawa średniej marży 90d nowych kohort. | **1 dzień** | Natychmiastowe zatrzymanie straty. Kampania traci w obu regułach atrybucji, a między 90. a 180. dniem dokłada kolejną stratę. |
| **3.** | **C. Wyłączenie kampanii Google Ads na specjalistów** | **+23,3 do +53,2 tys. zł** | Zatrzymanie wydatków na kampanię; wzrost marży całkowitej w kategorii specjalistów już w pierwszym tygodniu. | **1 dzień** *(zamiast 5–9 tyg. z briefu)* | Jednostkowa ekonomika specjalistów nie pozwala na naprawę tej kampanii optymalizacją (szczegóły w sekcji 2 i 3). |
| **4.** | **K. Naprawa pomiaru i blokada testów na produkcji** | **0 lub +37,95 tys. zł** bezpośrednio + wartość decyzyjna | 0 wizyt z kodem testowym w rozliczeniach lekarzy; raport dzienny zgodny z bazą po zwrotach i deduplikacji. | **1 dzień** (wstrzymanie wypłat/testów) + **1–2 tyg.** (raport) | Weryfikacja, czy płacimy lekarzom 38 tys. zł za 1-minutowe testy, zajmuje godzinę w księgowości. Bez czystych danych nie ocenimy kolejnych kroków. |
| **5.** | **H. Audyt sesji zalogowanych od wejścia (0% zakupów)** | **0 zł** (jeśli to zachowanie) lub **+36–89 tys. zł** (jeśli to błąd sesji) | Wynik testu ręcznego (dzień 1). Jeśli to bug: wzrost konwersji sesji ze statusem `logged_in` z 0% do poziomu zbliżonego do powracających. | **1 dzień** (test ręczny) + ew. **kilka dni** na fix | Koszt sprawdzenia to kilka godzin pracy QA. Asymetria zysku do wysiłku wymusza zrobienie tego w pierwszym tygodniu. |
| **6.** | **A. Zmiana warunków programu zniżkowego u specjalistów** | **+18,9 do +31,4 tys. zł** *(docelowo, po 12 mies.)* | Wzrost średniej marży na wizycie specjalistycznej w programie z −9,7 zł powyżej 0 zł bez spadku sprzedaży samego programu. | **1–2 tygodnie** (pełny efekt po 12 mies.) | Obecnie dopłacamy do każdej wizyty (np. 87,2 zł przychodu vs 100 zł kosztu lekarza). Trzeba to zamknąć przed jakimikolwiek testami programu (J). |
| **7.** | **I. Audyt straty kliknięcie $\rightarrow$ sesja w Meta/TikTok** | **0 do +35 tys. zł** *(po odjęciu wyłączonego TikToka)* | Zwiększenie relacji sesje/kliknięcia w Meta z 0,72–0,82 w stronę >0,88 (np. przez przyspieszenie LP w przeglądarkach in-app). | **1–2 dni** (audyt) + ew. optymalizacja LP | Tani audyt. Jeśli przyczyną jest wolne ładowanie strony docelowej w aplikacji Meta, poprawa obniży efektywny CAC o 10–15%. |
| **8.** | **D. Ograniczenie zwrotów po wizytach L4 (w kampanii Meta)** | **+10 do +35 tys. zł** *(skorygowane po wyłączeniu TikToka)* | Spadek odsetka zwrotów w kohortach L4 z 17,4% w stronę bazowych 5,3% przy utrzymaniu kosztu pozyskania (CAC) w ryzach. | **1–2 tygodnie** | Każdy zwrot to 25 zł czystej straty na lekarzu. Zmiana komunikacji w reklamie i pre-kwalifikacja przed płatnością. |
| **9.** | **F. Geo-test inkrementalności kampanii Meta na L4** | **Decyzja warta od −27,8 do +163,3 tys. zł** | Różnica w łącznej marży i liczbie nowych pacjentów między połową województw z wyłączoną kampanią a grupą kontrolną. | **4–6 tygodni** pomiaru | Niezbędne, by rozstrzygnąć konflikt Reguły 1 (+27,8 tys.) z Regułą 2 (−28,7 tys.) oraz zmierzyć kanibalizację ruchu organicznego. |
| **10.** | **G. Rozładowanie opóźnień porannych u internisty (6:00–11:59)** | **0 do +65 tys. zł** *(minus koszt obsady, jeśli potrzebna)* | Spadek odsetka wizyt opóźnionych >15 min z ~50% poniżej 10%; wzrost ocen i retencji 90d pacjentów porannych. | **2–4 tygodnie** (po odcięciu TikToka i teście Meta) | **Uwaga:** Nie kupujemy dodatkowej obsady w ciemno! Najpierw wyłączamy TikToka (B) i testujemy wyłączenie Meta L4 (F) – to one zatkały poranki od XI 2025. |
| **11.** | **J. Test darmowego programu zniżkowego na 90 dni** | **Koszt testu: −3,3 do −12,2 tys. zł** (wartość nieznana, wysokie ryzyko straty) | Wzrost retencji 90d i przede wszystkim **marży netto na pacjenta** w grupie testowej powyżej grupy kontrolnej po 90 i 180 dniach. | **90+ dni** obserwacji | **Odradzam w obecnym kształcie.** Rozdawanie za darmo programu, który przynosi stratę na samych zniżkach, przed naprawą punktu A to gwarantowana strata (szczegóły niżej). |

---

### 2. Błędy i słabe założenia w wycenach kandydatów

1. **Kandydat E (Safari na iPhone'ach) – poważne zaniżenie wyceny o koszt reklamy (CAC):**
   * *Błąd:* Wycena w briefie (75–83 tys. zł w 90d) powstała przez pomnożenie utraconych w skali roku zamówień ($628 \text{ do } 695 \times \frac{365}{198} \approx 1\,158 \text{ do } 1\,281$) przez **średnią marżę netto po odjęciu wydatków reklamowych** (~58,3–66,0 zł).
   * *Dlaczego to błąd:* Użytkownik, który odpada na kroku zakładania konta *po wyborze terminu*, już kliknął w reklamę. Koszt jego pozyskania (CAC) został już poniesiony! Odzyskanie tego pacjenta daje firmie **marżę kontrybucyjną przed kosztem reklamy** (przychód minus koszt lekarza i ew. prowizja 25 zł tylko dla ruchu z rankingu). Przy średnim wydatku reklamowym ~26 zł na nowego pacjenta ($650\text{ tys. zł} / 24\,687$), realna wartość naprawy błędu Safari to **105–135 tys. zł rocznie**, a nie 75–83 tys. zł.

2. **Kandydat B (TikTok L4) – brak annualizacji i ujemna marża po 90. dniu:**
   * *Błąd 1:* Kampania TikTok ruszyła 9.02.2026, więc w okresie 2 działała tylko przez **234 dni (64% roku)**. Jeśli kwoty −11,9 tys. zł (R1) i −30,8 tys. zł (R2) to wynik z okresu 2, to pełny roczny koszt utrzymywania tej kampanii wynosi **−18,6 tys. zł (R1) do −48,3 tys. zł (R2)**.
   * *Błąd 2:* Zauważmy, że wynik w 180 dniach (−13,5 tys. i −32,3 tys. zł) jest **gorszy** niż w 90 dniach (−11,9 tys. i −30,8 tys. zł). To oznacza, że kohorta z TikToka między 90. a 180. dniem generuje **ujemną marżę na powrotach** (prawdopodobnie przez kolejne zwroty lub korzystanie ze stratnych zniżek u specjalistów).

3. **Kandydat C i A (Specjaliści) – zignorowanie zepsutej ceny bazowej:**
   * Z punktu A wiemy, że po 20% zniżki cena wizyty u specjalisty wynosi np. 87,2 zł przy koszcie lekarza 100 zł. To oznacza, że **cena katalogowa wynosi 109 zł, a marża brutto przed zniżką to zaledwie 9 zł (8,2%)!**
   * Po uwzględnieniu średniego odsetka zwrotów (5,3%, co kosztuje średnio 5,3 zł na wizytę w opłacie dla lekarza), **realna marża jednostkowa na wizycie u specjalisty bez zniżki wynosi ~3,7 zł**. Jeśli pacjent przyszedł z serwisu z rankingiem lekarzy (prowizja 25 zł), firma traci na pierwszej wizycie ponad 21 zł.
   * W tym świetle założenie w **Kandydacie C**, że kampanię Google Ads na specjalistów da się naprawić „obniżając CAC o 40–60%” (z 58–81 zł do ~30 zł), jest nierealne – przy tak niskiej marży jednostkowej (nawet podbitej przez psychiatrię do 32–37 zł w 90 dni) kampania nadal będzie balansować na granicy opłacalności.
   * Z kolei w **Kandydacie A** pominięto elastyczność popytu na sam program zniżkowy: jeśli zabierzemy zniżkę na specjalistów, część pacjentów nie kupi programu za 89 zł (który sam w sobie daje czysty przychód przy zakupie).

4. **Kandydat D (Zwroty L4) – błędne założenie behawioralne w górnym wariancie (+57,1 tys. zł):**
   * Górny wariant zakłada, że po zmianie treści reklamy i strony docelowej odsetek zwrotów spadnie z 17,4% do 5,3%, a **ci sami pacjenci nadal kupią wizytę i za nią zapłacą, mimo że nie dostaną L4**.
   * Pacjent z kampanii L4 kupuje wizytę wyłącznie po to, by otrzymać zwolnienie. Jeśli ostrzeżemy go na stronie wejścia, że lekarz może odmówić L4 i nie zwracamy wtedy pieniędzy, pacjent po prostu **nie kupi wizyty** (spadnie konwersja na stronie, więc wzrośnie CAC). Ponadto wyceny B i D nakładają się na siebie – po wyłączeniu TikToka (B) pula zwrotów do naprawy w D maleje o udział TikToka.

5. **Kandydat G (Opóźnienia poranne) – pomylenie skutku z przyczyną:**
   * Opóźnienia poranne u internisty wystrzeliły z 5–7% do ~50% **w listopadzie 2025** – dokładnie wtedy, gdy **3 listopada 2025 ruszyła duża kampania Meta na L4 (F)**. Pacjenci po zwolnienie lekarskie do pracy zgłaszają się rano (6:00–11:59). Choć w briefie zaznaczono „przy tym samym porannym ruchu opóźnień jest dużo więcej”, napływ trudnych, roszczeniowych pacjentów L4 (17,4% zwrotów, spory o zasadność zwolnienia) mógł wydłużyć czas obsługi lub zniechęcić lekarzy do brania porannych dyżurów. Zatrudnianie dodatkowej obsady przed wyłączeniem TikToka L4 i ograniczeniem Meta L4 to leczenie objawów.

6. **Kandydat J (Test darmowego programu zniżkowego) – pułapka ekonomiczna:**
   * Kupujący program płacą 89 zł z góry, a wykorzystują średnio 104,6 zł zniżek (czyli sama opłata nie pokrywa nawet wartości rabatu, a u specjalistów generuje bezpośrednią stratę gotówkową poniżej kosztu lekarza).
   * Rozdanie programu **za darmo** w teście pozbawia firmę jedynego dodatniego elementu tej układanki – 89 zł opłaty początkowej! Nawet jeśli darmowe zniżki podniosą liczbę wizyt w 90 dniach o 10–15 p.p., to przy 50% zniżce na internistę i dopłacaniu do każdego specjalisty **zwiększona liczba wizyt może wygenerować niższą (lub ujemną) marżę niż brak zniżki**. Test w tej formie ma źle zdefiniowaną hipotezę biznesową.

---

### 3. Kampanie z wynikiem ujemnym: najpierw naprawiać czy wyłączać?

Zasada ogólna: **Wyłączać natychmiast, jeśli ekonomika jednostkowa produktu jest zepsuta lub strata występuje w obu modelach atrybucji. Naprawiać/testować tylko wtedy, gdy przynajmniej jeden wiarygodny model atrybucji pokazuje plus i znamy konkretną dźwignię naprawy.**

* **TikTok na L4 (B) $\rightarrow$ WYŁĄCZYĆ NATYCHMIAST.** 
  * *Dlaczego:* Kampania jest głęboko pod kreską w obu regułach (−11,9 tys. i −30,8 tys. zł), pogłębia stratę między 90. a 180. dniem, a z danych w briefie wynika wprost, że nawet **w najbardziej optymistycznym wariancie naprawy zwrotów (D)** jej wynik to ledwie +3,0 tys. zł (Reguła 1) lub nadal **−23,2 tys. zł (Reguła 2)**. Szkoda każdego dnia przepalania budżetu.
* **Google Ads na specjalistów (C) $\rightarrow$ WYŁĄCZYĆ NATYCHMIAST (bez 4–8 tygodni pomiaru).**
  * *Dlaczego:* Wynik jest ujemny w obu regułach i obu horyzontach. Aby wyjść na zero, trzeba by obniżyć CAC o 40–60%.W aukcyjnym kanale wyszukiwarkowym (Google Ads) obniżenie CAC o połowę bez drastycznego ścięcia wolumenu lub podniesienia ceny bazowej usługi jest niemożliwe. Kampanię należy zamknąć dziś i wrócić do niej dopiero po podniesieniu cen katalogowych specjalistów.
* **Meta na L4 (F) $\rightarrow$ TEST GEO (F) + RÓWNOLEGŁA NAPRAWA ZWROTÓW (D).**
  * *Dlaczego:* W Regule 1 (która w 97% pokrywa się z kodami rabatowymi, więc lepiej oddaje pierwszy kontakt z reklamą na mobile'u – zwłaszcza gdy Safari na iPhonie nie pozwalało dokończyć zakupu w pierwszej sesji!) kampania generuje **+27,8 tys. zł marży**. Całkowite wyłączenie jej w ciemno grozi utratą tego zysku, ale z drugiej strony Reguła 2 pokazuje −28,7 tys. zł i istnieje ryzyko kanibalizacji ruchu organicznego. Dlatego jedyną słuszną drogą jest wyłączenie jej na 4–6 tygodni w losowej połowie województw, przy jednoczesnym wdrożeniu pre-kwalifikacji L4 (D) w połowie aktywnej.

---

### 4. Brakujące działania (wynikające bezpośrednio z faktów w briefie)

Na liście kandydatów A–K zabrakło pięciu działań o dużym wpływie na marżę, które wprost wynikają z przytoczonych danych:

1. **Wdrożenie automatycznego odnawiania programu zniżkowego (model subskrypcyjny) lub kampanii retencyjnej przed 365. dniem:**
   * *Fakt z briefu:* „Program nie odnawia się sam... Odnawia około 5% członków”, a jednocześnie pacjenci ci mają o 10–15 p.p. wyższe powroty (i utrzymują tę przewagę po wygaśnięciu!).
   * *Działanie:* Przejście na płatność cykliczną (kartą/BLIK-iem powtarzalnym) przy zakupie oraz uruchomienie automatycznej ścieżki e-mail/SMS na 14, 7 i 1 dzień przed końcem roku członkostwa (po uprzedniej naprawie cennika specjalistów z punktu A). Podniesienie odnowień z 5% do 20–25% to czysty zysk z opłaty 89 zł od najbardziej lojalnej grupy.

2. **Podwyżka cen katalogowych u specjalistów (poza psychiatrą):**
   * *Fakt z briefu:* Koszt lekarza specjalisty to 100 zł, a cena po 20% zniżki to np. 87,2 zł (czyli cena bazowa to ~109 zł).
   * *Działanie:* Zamiast tylko łatać program zniżkowy (A), należy podnieść ceny bazowe konsultacji specjalistycznych (np. ze 109 zł do 139–149 zł). Przy koszcie lekarza 100 zł, prowizji serwisu rankingowego 25 zł za nowego pacjenta i 5,3% zwrotów, obecna cena katalogowa (~109 zł) nie spina się finansowo nawet **bez** programu zniżkowego.

3. **Zmiana procesu obsługi i rozliczania odmów L4 (triaż przed wizytą / zmiana zasad zwrotów):**
   * *Fakt z briefu:* „Koszt lekarza za każdą odbytą wizytę, także za taką, za którą pacjent dostał zwrot: internista 25 zł... 17,4% odbytych wizyt L4 tych pacjentów kończy się zwrotem”.
   * *Działanie:* Oprócz zmiany treści reklam (D), trzeba zmienić sam produkt i politykę zwrotów:
     * wprowadzić obowiązkową ankietę medyczną **przed płatnością**, która odrzuca przypadki niekwalifikujące się do teleporady z L4 (zanim zapłacimy lekarzowi 25 zł),
     * zmienić regulamin: pacjent płaci za **konsultację lekarską (czas i wiedzę lekarza)**, a nie za wystawienie dokumentu L4. Odmowa wystawienia L4 z przyczyn medycznych po odbytej wizycie nie powinna być podstawą do automatycznego zwrotu 100% kwoty.

4. **Redukcja budżetów reklamowych w kanałach o malejącej krańcowej opłacalności (Q3/Q4):**
   * *Fakt z briefu:* W II i III kw. 2026 wydatki na kampanie wzrosły ponad dwukrotnie (2,04× i 2,08× r/r), podczas gdy marża w III kw. spadła o 6,8% r/r (z 222,8 do 207,7 tys. zł).
   * *Działanie:* Krańcowy ROAS dodatkowych wydatków reklamowych powyżej poziomu z roku poprzedniego jest głęboko ujemny. Poza wyłączeniem B i C należy przejrzeć krzywe wydatków w pozostałych kampaniach i obciąć nieefektywne nadwyżki budżetowe (skalowanie wydatków 2× przy spadku marży oznacza przepalanie budżetu na coraz droższe kliknięcia).

5. **Audyt opłacalności serwisu z rankingiem lekarzy:**
   * *Fakt z briefu:* „Prowizja dla serwisu z rankingiem lekarzy: 25 zł za pierwsze zamówienie pacjenta.”
   * *Działanie:* Dla specjalisty (koszt 100 zł + prowizja 25 zł = 125 zł kosztu przy cenie ~109 zł) każde pierwsze zamówienie z tego serwisu przynosi stratę, o ile pacjent nie wróci. Brakuje na liście analizy kohortowej pacjentów z tego kanału (jaki odsetek stanowią specjaliści vs interniści/psychiatrzy i czy kanał jest rentowny po uwzględnieniu prowizji 25 zł).

---

### 5. Czego nie wiemy (i co musimy zweryfikować w danych)

Poza czterema niewiadomymi wymienionymi wprost na końcu briefu (inkrementalność L4, właściwa reguła atrybucji bez kodów, przyczyny zwrotów L4, przyczynowość w programie zniżkowym), do podjęcia w pełni bezpiecznych decyzji **nie wiemy**:

1. **Czy lekarze faktycznie dostali przelewy za 2 071 wizyt testowych?** – W briefie jest to warunkowe („37,95 tys. zł rocznie, jeśli lekarze dostają... 0 zł, jeśli nie”). To pierwszy fakt do sprawdzenia w dziale finansowym pierwszego dnia.
2. **Jaka jest elastyczność cenowa wizyt specjalistycznych i samego programu zniżkowego?** – Nie wiemy, ilu klientów kupuje program za 89 zł głównie dla specjalistów i ilu z nich zrezygnuje z zakupu programu po wdrożeniu punktu A (dlatego wycena +31,4 tys. zł w A jest górnym sufitem, a nie wartością oczekiwaną).
3. **Dlaczego dokładnie spadła poranna przepustowość internistów od listopada 2025 (G)?** – Nie mamy danych o grafikach lekarzy. Nie wiemy, czy ubyło godzin lekarskich (problem podażowy – np. lekarze odeszli do konkurencji lub przestali brać poranne dyżury), czy wydłużył się średni czas trwania wizyty przez trudnych pacjentów z kampanii Meta L4.
4. **Jaki udział w utraconych zamówieniach Safari (E) miał ruch płatny vs organiczny vs serwis z rankingiem?** – Jeśli był to ruch z kampanii CPC (Meta/Google/TikTok), koszt reklamy już ponieśliśmy (marża krańcowa jest bardzo wysoka). Jeśli był to ruch z serwisu rankingowego (gdzie płacimy 25 zł tylko za *zrealizowane* pierwsze zamówienie), odzyskanie zamówienia wiąże się z naliczeniem prowizji 25 zł.
5. **Jak wygląda retencja i LTV w rozbiciu na specjalizacje (internista vs pediatra vs psychiatra vs pozostali)?** – Znamy tylko średnią marżę 90d (58,3 zł) i koszty lekarzy (25 / 100 / 200 zł), ale nie znamy dokładnego cennika poszczególnych specjalizacji ani tego, która specjalizacja napędza powroty.
