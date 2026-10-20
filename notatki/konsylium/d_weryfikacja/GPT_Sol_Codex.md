# GPT Sol (Codex) — gpt-6.1-sol (Codex, wysiłek high)

**Główny wniosek się broni: nowych pacjentów jest więcej, ale obserwowana retencja jest gorsza.** Nie znalazłem w załącznikach błędu rachunkowego, który odwracałby tę odpowiedź. Przed wysłaniem poprawiłbym jednak kilka istotnych rzeczy: zależności między priorytetami, zbyt pewne rozpoznania przyczyn oraz rozbieżności w opisie segmentów.

Oceniam wyłącznie załączniki. Potwierdzenie rachunku oznacza poniżej przeliczenie podanych liczb, a nie niezależne sprawdzenie bazy.

**1. Lista poprawek od najważniejszej**

**1. Krytyczna przed wysłaniem: brakuje rzeczywistego linku do narzędzia.**

**Miejsce:** B, początek README; A, „Co oddajemy”.

README zawiera adres z `<organizacja>` i `<repozytorium>`. Nie pozwala sprawdzić wymogu otwarcia narzędzia bez konta i instalacji.

**Poprawka:** przed wysłaniem uzupełnić oba rzeczywiste adresy: narzędzia i repozytorium. Sprawdzić je bez zalogowania. To zaplanowany ostatni krok, ale obecny załącznik nie dowodzi jego wykonania.

---

**2. Ważna: próg decyzji o Meta nie uwzględnia wcześniejszej naprawy zwrotów.**

**Miejsce:** C8, „Zasady listy” oraz priorytety 5 i 9; C9, niewiadoma 1.

Lista deklaruje wycenę przy założeniu wykonania wcześniejszych pozycji. Tymczasem próg około 85% w pozycji 9 pochodzi z ekonomii **przed** naprawą zwrotów z pozycji 5.

**Dowód:** dla Meta wydatki z dni działania wynoszą około 163,3 tys. zł. Obecna prognozowana marża pacjentów przed kampanią wynosi:

- 163,3 + 27,8 = 191,1 tys. zł;
- próg dodatkowości: 163,3 / 191,1 = **85,5%**.

Po górnym wariancie naprawy zwrotów wynik kampanii wynosi +70,1 tys. zł:

- próg: 163,3 / (163,3 + 70,1) = **70,0%**.

**Poprawka:** rozdzielić wyceny obecnego stanu od wycen po wcześniejszych działaniach. Przeliczyć próg Meta po rzeczywiście uzyskanym wyniku testu obietnicy L4. Zaktualizować również niewiadomą 1.

---

**3. Ważna: test Meta nie ma jeszcze podstaw do obietnicy rozstrzygnięcia po 4–6 tygodniach.**

**Miejsce:** C8, priorytet 9.

Dobry jest pomysł losowania województw i mierzenia wszystkich nowych pacjentów. Brakuje jednak sprawdzenia, czy test odróżni wynik poniżej progu od wyniku powyżej progu.

**Dowód:** załączniki nie podają minimalnej wykrywalnej zmiany, zmienności wyników województw ani mocy testu. W danych o wydatkach z A nie ma województwa, więc pomiar oszczędzonego budżetu wymaga dodatkowych danych. Wspólna obsada lekarzy może też przenosić korzyści z mniejszego obciążenia do województw kontrolnych.

Koszt „najwyżej 1,6–1,8 tys. zł” również zależy od obecnej ekonomii. Po górnym wariancie naprawy zwrotów, przy wyłączeniu połowy skali kampanii, rachunek daje około:

- 77,1 tys. zł × ½ × 28/365 = **3,0 tys. zł**;
- 79,3 tys. zł × ½ × 42/365 = **4,6 tys. zł**.

To nadal scenariusze, nie gwarantowane granice kosztu.

**Poprawka:** przed startem ustalić moc testu, sposób rozliczania wydatków regionalnych, opóźnienie zakupów po reklamie i regułę dla wyniku nierozstrzygającego. Decyzję oprzeć na przedziale niepewności, a nie samym oszacowaniu poniżej lub powyżej 85%.

---

**4. Ważna: niska konwersja przeglądarek wbudowanych nie dowodzi problemu technicznego.**

**Miejsce:** C3, fragment poprzedzający dwa problemy do naprawienia; D, `ZNALEZISKA.md`, podsumowanie pozyskania.

Narzędzie przedstawia przeglądarki wbudowane jako drugi rozpoznany problem strony. Pokazane porównanie jest jednak przede wszystkim porównaniem różnych grup ruchu.

**Dowód:** w C3 konwersja przeglądarek wbudowanych wynosi 4,8–7,2%, wobec 16,1–18,1% w Chrome i Safari. Ale D, sekcja ekonomii, stwierdza, że **w tych samych nowych kampaniach** surowa konwersja przeglądarek wbudowanych nie jest niższa. Zaznaczono też brak rozdzielenia urządzenia, daty i pacjenta.

**Poprawka:** napisać: „Ruch w przeglądarkach wbudowanych ma niższą konwersję. Nie ustaliliśmy, ile wynika z jakości ruchu, a ile z działania strony”. Następnie porównać przeglądarki w obrębie kampanii, urządzenia i okresu oraz wykonać test techniczny.

Safari ma znacznie mocniejsze dowody na konkretny problem niż cała kategoria przeglądarek wbudowanych.

---

**5. Ważna: opis walidacji źródła pozyskania miesza regułę z jej sprawdzeniem.**

**Miejsce:** D, `ZALOZENIA.md`, punkt 22; `DECYZJE.md`, tabela definicji.

Opis podaje zgodność reguły z kodami na poziomie 96,6–97,0%, chociaż ta sama reguła nadpisuje źródło kodem kampanii.

**Dowód:** po takim nadpisaniu zgodność dla trzech jednoznacznie mapowanych kodów powinna wynosić **100% z definicji**. Wynik około 97% może dotyczyć pierwszego wejścia **przed** zastosowaniem kodu.

**Poprawka:** zapisać osobno:

- zgodność pierwszego wejścia z kodem przed nadpisaniem;
- liczbę pacjentów zmienionych przez nadpisanie — podano 183;
- ograniczenie: sprawdzenie obejmuje trzy kampanie z kodami.

Nie podważa to samej reguły. Wymaga poprawienia uzasadnienia jej wyboru.

---

**6. Ważna: pogorszenie punktualności jest potwierdzone, spadek przepustowości pozostaje interpretacją.**

**Miejsce:** C4, „Opóźnienia przy tym samym porannym ruchu”; C5, zdarzenie 7; C9, niewiadoma 4.

Porównanie podobnej liczby wizyt dziennie nie kontroluje liczby dostępnych lekarzy, skupienia terminów w konkretnych godzinach, rodzaju przypadków ani organizacji zapisów. Pozwala odrzucić proste wyjaśnienie samym dziennym wolumenem. Nie mierzy bezpośrednio przepustowości.

**Dowód:** różnicę **+26,4 punktu procentowego** można odtworzyć z pokazanych przedziałów ruchu. Grafików lekarzy jednak nie ma.

Dodatkowo zdanie „Opóźnienia rosną tylko u internisty rano” przeczy tabeli:

- internista w południe: **3,0% → 8,9%**;
- internista w nocy: **1,9% → 5,7%**.

**Poprawka:** „Największe pogorszenie występuje rano u internisty. Utrzymuje się przy podobnym dziennym ruchu. Jest to zgodne z pogorszeniem dostępnej obsady lub organizacji pracy, ale przyczyny wymagają sprawdzenia”.

---

**7. Ważna: rekomendacja pauzy TikToka jest rozsądna, lecz pewność została zawyżona.**

**Miejsce:** C8, priorytet 3, „Propozycja”.

Zdanie „pewny jest tylko brak korzyści” nie wynika z przedstawionego przedziału. Brak przekonującego dowodu korzyści nie jest dowodem jej braku.

**Dowód:** dla 299 pacjentów wynik po 180 dniach wynosi −1,1 zł, z warunkowym przedziałem **od −5,3 do +3,0 zł**. Dodatni wynik pozostaje dopuszczony nawet przez ten ograniczony przedział.

Także stwierdzenie, że naprawa najwyżej doprowadza do zera, jest zbyt skrótowe. Tabela pokazuje w przyjętej regule +3,0 tys. zł po 90 dniach i +1,4 tys. zł po 180 dniach.

**Poprawka:** „Obecne oszacowania przemawiają za odwracalną pauzą. Nie wykazaliśmy trwałej rentowności, a dojrzała próba jest mała”. Zachować rekomendację, zmienić uzasadnienie pewności.

---

**8. Ważna: opis retencji zawiera rozbieżność segmentów oraz dwa nadmierne uogólnienia.**

**Miejsce:** C1, „Lepsza retencja”; C2, wprowadzenie; E1, W2.

**Rozbieżność liczb:**

- C1: pierwsze L4 poza nowymi kampaniami — **14,8% z 2 639 → 13,9% z 2 797**;
- E1: `internista_l4` poza nowymi kampaniami — **14,6% z 2 795 → 13,8% z 2 969**.

Nie da się z załączników ustalić, czy to błąd, czy różne definicje segmentu.

**Uogólnienie pierwsze:** „W jednej grupie spadku nie wykazaliśmy”. E1 pokazuje również:

- psychiatra: **22,5% → 24,6%**;
- pediatra: **22,3% → 26,3%**.

Nie przesądza to istotnego wzrostu, ale przeczy sugestii jednej wyjątkowej grupy.

**Uogólnienie drugie:** C2 mówi o „większości” spadku związanej z nowymi kampaniami. Według sesji płatności jest to około **46%**, czyli mniej niż połowa.

**Poprawka:** uzgodnić definicję L4 i liczby. Napisać, że zmiany różnią się między usługami. Zamiast „większość” stosować konsekwentnie „około 46–71% spadku w rozkładzie opisowym”.

---

**9. Ważna: wyniki po 90 i 180 dniach nie pokazują samego efektu dłuższego czasu.**

**Miejsce:** C6, wprowadzenie do ekonomii kampanii; C8, wyceny kampanii; D, założenie 40.

Dobrze, że oba okna są pokazane. Obejmują jednak inne kohorty, co w głównym opisie ekonomii jest zbyt słabo widoczne.

**Dowód:** TikTok:

- 90 dni: **1 265 pacjentów**, marża 31,9 zł;
- 180 dni: **299 pacjentów**, marża 31,2 zł.

Spadek marży pomiędzy tymi kolumnami nie oznacza, że ta sama grupa straciła marżę w kolejnych miesiącach. Zmieniła się grupa pacjentów.

**Poprawka:** dopisać to bezpośrednio pod tabelą. Dodać porównanie 90 i 180 dni na tych samych kohortach dojrzałych do 180 dni. Roczne wyceny jasno nazwać prognozą opartą na przeniesieniu marży starszych kohort na cały rocznik.

---

**10. Ważna: test TelemediGO jest sensownym eksperymentem mechanizmu, lecz nie domyka decyzji handlowej.**

**Miejsce:** C8, priorytet 12.

Zastrzeżenie o różnicy między darmowym dostępem a ofertą za 89 zł jest poprawne. Nagłówek nadal obiecuje jednak, że test rozstrzygnie rolę programu.

Brakuje też informacji potrzebnych do sprawdzenia próby i kosztu.

**Dowód:**

- 487–1 823 pacjentów na grupę — bez podanych założeń o wielkości efektu, poziomie istotności i mocy;
- koszt 3,3–12,2 tys. zł — bez wyjaśnienia momentu przyznania zniżki;
- jeżeli zniżka obejmie pierwszą konsultację, koszt będzie inny niż przy przyznaniu jej po pierwszym zakupie;
- sam koszt testu nie jest odpowiedzią na wymaganie A dotyczące wartości działania.

**Poprawka:** określić moment losowania, zakres zniżek, wpływ na sprzedaż płatnego członkostwa oraz próbę dla marży. Nazwać wynik etapem poprzedzającym decyzję o płatnej ofercie. Podać roczną skalę ekonomiczną decyzji albo jawnie wskazać, że nie została jeszcze oszacowana.

---

**11. Ważna: zakres 14–21 tys. zł dla Safari w III kwartale jest nieodtwarzalny z opisanej metody.**

**Miejsce:** C1, „Wynik pod koniec okresu”; C8, priorytet 1; D, wynik kwartalny.

**Dowód:** proporcjonalne przeliczenie 628–695 zamówień z 198 dni na 92 dni III kwartału, przy marży 64,6 zł po 90 dniach, daje:

**628–695 × 92/198 × 64,6 zł = 18,9–20,9 tys. zł.**

Przy marży 74,3 zł po 180 dniach wychodzi **21,7–24,0 tys. zł**. Z podanych składników nie wynika dolna granica 14 tys. zł.

Ponadto marża rocznika odzyskanych pacjentów w kolejnych 90 dniach nie jest tym samym co marża zaksięgowana w samym kwartale.

**Poprawka:** pokazać składniki dolnej granicy i horyzont. Do czasu wyjaśnienia usunąć porównanie tej kwoty ze spadkiem wyniku kwartału albo ograniczyć je do wyraźnie nazwanej ilustracji skali.

---

**12. Ważna: wykrycie awarii nie jest równoznaczne z jej naprawą.**

**Miejsce:** C8, priorytet 2; kryteria sukcesu priorytetu 1.

Stwierdzenie, że wykrycie po tygodniu ograniczyłoby stratę do 3,5%, pomija czas naprawy.

**Dowód:** **7/198 = 3,54%**, a **628–695 × 7/198 = 22–25 zamówień**. Rachunek jest poprawny wyłącznie przy założeniu usunięcia problemu po siedmiu dniach.

Również cel około 1 080 nowych kont w 60 dni zależy od wielkości ruchu. Sam wzrost liczby kont nie dowodzi przywrócenia skuteczności.

**Poprawka:** rozdzielić czas wykrycia i czas usunięcia awarii. Sukces Safari mierzyć przede wszystkim konwersją odpowiedniego kroku oraz liczbą pierwszych zakupów względem porównywalnego ruchu.

---

**13. Ważna: część wycen wymaga wyraźniejszego nazwania kosztów i horyzontu.**

**Miejsce:** C8, priorytety 6 i 7; D, założenie 38.

Dla porannej obsady zakres 0–65,2 tys. zł nie jest zakresem końcowego wyniku po koszcie zmiany obsady.

**Dowód:** przy braku efektu retencyjnego i dodatnim koszcie obsady wynik działania będzie ujemny, a nie zerowy.

W komunikacji po wizycie rachunek jest poprawny:

**24 687 × 1% × 95,6 zł = 23,6 tys. zł.**

Jednak 95,6 zł pochodzi z marży w dniach **1–180**, przy podziale według powrotu w 90 dniach. Nie jest to wartość zrealizowana wyłącznie w pierwszych 90 dniach.

**Poprawka:** przy poranku podać „potencjalna korzyść przed dodatkowym kosztem obsady”. Przy komunikacji: „zmiana powrotu w 90 dniach, wyceniona marżą do 180. dnia”. Zachować zastrzeżenie o obserwacyjnym charakterze 95,6 zł.

---

**14. Ważna: automatyczne wykrycie spadku Google Ads na markę pozostaje bez rozliczenia.**

**Miejsce:** C5, ostatnie wiersze surowego wyniku wykrywania zmian.

**Dowód:** od 22.05.2026 dla Google Ads na hasło marki pokazano:

- konwersję **21,2% → 17,8%**;
- przybliżenie **−39,6 zamówienia na 30 dni**.

To konkretny sygnał odpowiadający wymogowi „gdzie i od kiedy”. Nie ma go w omówionych zdarzeniach ani wyjaśnienia, dlaczego został odrzucony.

**Poprawka:** sprawdzić i zapisać, czy jest to skutek Safari, zmiany struktury ruchu, sezonu, czy osobny problem. Nie trzeba tworzyć kolejnego priorytetu, jeśli to powtórzenie znanego zjawiska.

---

**15. Drobna, ale merytoryczna: wzrost TelemediGO został opisany zbyt kategorycznie.**

**Miejsce:** C1, karta TelemediGO; D, podsumowanie TelemediGO.

Zdanie, że przy kasie przybywa zakupów dzięki większej liczbie zamówień, a nie wyższemu odsetkowi kupujących, nie obejmuje poprawnie kolejnych zamówień.

**Dowód:** E7 pokazuje wzrost odsetka przy kolejnych zamówieniach **9,27% → 9,86%**. Z dodatkowych 289 zakupów:

- 234 wynikają z większej liczby zamówień;
- **55 wynika ze wzrostu odsetka kupujących**.

**Poprawka:** „Wzrost wynika przede wszystkim z większej liczby zamówień oraz sprzedaży osobnej. Przy pierwszym zakupie odsetek spada, przy kolejnych lekko rośnie”.

---

**16. Pozostałe drobne niespójności i doprecyzowania**

| Waga i miejsce | Co wymaga poprawy — dowód | Propozycja |
|---|---|---|
| **Drobna — C4, tabela ocen** | Średnie oceny mają znak procentu: np. **4,45%** zamiast **4,45 w skali 1–5**. | Poprawić format średniej i jej zmiany. |
| **Drobna — C8, priorytet 6, oceny** | Przy średniej 2,9 wskazano 1 550 wizyt, ale ocen jest **469**. Przy 4,5: 11 007 wizyt, lecz **3 446 ocen**. | Podać liczbę ocen jako próbę średniej; liczbę wizyt pozostawić osobno. |
| **Drobna — C2 wobec C1, D i E2** | Zmiana powrotu po 180 dniach wynosi w tabeli **−5,2 punktu procentowego**, w pozostałych miejscach **−5,3**. | Ujednolicić obliczenie z wartości niezaokrąglonych. To rozbieżność prezentacji, nie dowód błędnej retencji. |
| **Drobna — D, założenie 21; C6; E1–E2** | Przychód okresu 1 występuje jako **2 230 267 zł** i **2 230 266 zł**. W C6 suma zaokrąglonych składników okresu 2 daje **3 228 343 zł**, wobec sumy **3 228 342 zł**. | Zachować jedną wartość główną i dopisać, że zaokrąglone składniki mogą różnić się od sumy o 1 zł. Nie traktuję tego jako potwierdzonego błędu rachunku. |
| **Drobna — C1 i D, opis oczyszczenia** | „Nowi pacjenci się nie zmieniają” jest dosłownie nieprawdziwe: **16 251 → 16 231** oraz **24 689 → 24 687**. | Napisać, że nie zmienia się wzrost zaokrąglony do pełnego procentu: około 52%. |
| **Drobna — C5, zdarzenie 10** | Zmiana datowana jest na **10.02.2026**, a start TikToka na **9.02.2026**. Tekst mówi o tym samym dniu. | „Dzień po starcie kampanii” albo „w pobliżu startu”. |
| **Drobna — D, założenie 3** | Błędnie opisano kierunek przesunięcia doby między UTC a czasem polskim. | To sesje z końca doby UTC przechodzą na następny dzień w Polsce: od 22:00 UTC latem lub 23:00 UTC zimą. Nie podważa to opisanej kontroli kodu. |
| **Drobna, do wyjaśnienia — E4, `crm_go_upsell`** | W kolumnie dni jest **326**, choć od 8.09.2025 do 30.09.2026 włącznie upływa **388 dni kalendarzowych**. | Jeśli chodzi o dni z sesjami, tak nazwać kolumnę i średnią dzienną. Z załączników nie ustalę tego na pewno. |
| **Drobna — E1, nagłówek W4** | „Dopisek kandydata **2026-10-21**” jest późniejszy od dzisiejszej daty i daty raportu: **2026-10-20**. | Poprawić datę albo oznaczenie wersji. |
| **Drobna — C9, niewiadoma 11** | Uzasadnienie sezonowości jednym latem i zimą „w roku” nie wyjaśnia ograniczenia dwóch lat danych. | Napisać wprost: mamy tylko dwa cykle roczne, a sezon i zmiany wydatków nakładają się w czasie. |

**2. Co się potwierdziło**

**Główne wzrosty i sumy są rachunkowo spójne.**

| Miara | Moje przeliczenie |
|---|---|
| Nowi pacjenci | 24 687 / 16 231 − 1 = **+52,10%** |
| Oczyszczone zamówienia | 38 491 / 24 716 − 1 = **+55,73%** |
| Przychód konsultacji po zwrotach | 3 228 342 / 2 230 266 − 1 = **+44,75%** |
| Zakupy TelemediGO | 2 468 / 1 759 − 1 = **+40,31%** |
| Marża po wskazanych kosztach | 1 048 069 / 828 085 − 1 = **+26,57%** |
| Wydatki na kampanie | 649 675 / 367 632 − 1 = **+76,72%** |
| Liczba powracających w 90 dniach | 3 289 / 3 076 − 1 = **+6,92%** |

Potwierdziły się również następujące rzeczy:

- **Retencja 90-dniowa:** 3 076 / 12 867 = 23,91%, a 3 289 / 18 924 = 17,38%. Spadek wynosi **6,53 punktu procentowego**. Poprawnie odróżniono wzrost liczby powracających od spadku ich udziału.
- **Porównywalność okresów:** obcięcie obu roczników do tych samych dni kalendarzowych i pełnych okien jest właściwe. Różnica między 23,6% dla całego okresu 1 a 23,9% dla porównywalnego wycinka została wyjaśniona.
- **Marża roczna:** wskazane przychody i koszty odtwarzają dokładnie **828 085 zł** i **1 048 069 zł**.
- **III kwartał:** 207 713 − 222 824 = **−15 111 zł**, czyli **−6,78%**. Wydatki 181 555 / 87 431 = **2,08 raza**. Lipiec był lepszy, sierpień i wrzesień gorsze — poprawnie uniknięto uogólnienia na każdy miesiąc.
- **Start od zera:** 24 687 + 5 289 + 8 515 = **38 491 zamówień**. Odjęcie 152 960 zł marży wcześniejszych kohort daje 895 109 zł, czyli **+8,1%**. Po odjęciu również 41 474 zł TelemediGO pozostaje 853 635 zł, czyli **+3,1%**. Zastrzeżenie, że to rozbicie księgowe, jest potrzebne i poprawne.
- **Safari w skali rocznej:** 628–695 × 365/198 daje **1 158–1 281 pacjentów**. Pomnożenie przez 64,6 zł daje **74,8–82,8 tys. zł**, a przez 74,3 zł **86,0–95,2 tys. zł**. To potwierdza podane zakresy roczne przy przyjętych założeniach.
- **Przeliczenia kampanii:** okresy 332 dni dla Meta i 234 dni dla TikToka są poprawne. Właściwe mnożniki to 365/332 i 365/234. Nie widzę błędu w zasadzie przeliczenia na pełny rok.
- **Wyłączenie kampanii:** wzór „oszczędzone wydatki minus marża utraconych dodatkowych pacjentów” jest poprawny. Scenariusze 50% dodatkowości są zgodne z tym wzorem, z dokładnością prezentowanych zaokrągleń.
- **Poranne opóźnienia:** pięć wspólnych przedziałów obejmuje **9 979 wizyt**. Ważenie pokazanych różnic łączną liczbą wizyt daje około **26,44 punktu procentowego**, zgodnie z 26,4.
- **TelemediGO:** 184 + 289 + 236 = **709 dodatkowych zakupów**. Opłaty 1 759 × 89 zł = **156 551 zł**. Po odjęciu 183 939,20 zł efektywnych zniżek pozostaje **−27 388,20 zł**. Poprawnie zaznaczono, że nie jest to zmierzona strata programu.
- **Cennik:** ceny po rabatach i marże jednostkowe zgadzają się. Przykładowo 109 × 80% − 100 = **−12,80 zł**. Podwyżka o 10 zł przy 7 363 zamówieniach daje **73 630 zł** przed zmianą popytu; z utrzymaniem rabatu na 1 425 zamówieniach — **70 780 zł**.
- **Definicje:** pierwszy opłacony zakup jako wejście do kohorty, osobny status pierwszej wizyty, brak TelemediGO w powrotach oraz koszt lekarza za wizyty odbyte i zwrócone są jawne i zgodne z przyjętym sposobem analizy. Koszt pediatry 100 zł ma uzasadnienie w treści zadania.

**Dwóch pozornych rozbieżności nie uznaję za błędy:**

- 1 810 wierszy z TEST-QA wobec 1 781 zamówień — różnicę 29 wyjaśniają duplikaty.
- 24 717 i 38 490 płatności w lejku wobec 24 716 i 38 491 zamówień w wyniku biznesu — lejek grupuje po dniu rozpoczęcia sesji, a wynik po dniu płatności. Sumy dwuletnie są równe: **63 207**. Warto dopisać takie objaśnienie; bez bazy nie potwierdzę konkretnego zamówienia przekraczającego granicę okresów.

Nie mogłem niezależnie potwierdzić identyfikacji wszystkich duplikatów i kont testowych, działania filtrów, wykresów, kodu analizy ani odtwarzalności repozytorium. Nie można też odtworzyć podanych liczebności prób eksperymentów z samych załączników.

**3. Ocena z perspektywy zlecającego**

**Trzy najmocniejsze strony**

1. **Analiza odpowiada na najważniejszą część zadania.** Są kohorty dzienne, porównywalny wiek pacjentów, kontrola niedojrzałych kohort oraz rozdzielenie struktury pozyskania od zachowania.
2. **Kandydat przekłada dane na decyzje ekonomiczne.** Liczy marżę, pokazuje oba warianty przypisania źródła i dopuszcza oszczędzenie budżetu zamiast automatycznego przenoszenia go do innych kampanii.
3. **Ślad pracy jest przejrzysty.** Definicje, korekty i niewiadome mają uzasadnienia. Szczególnie dobre są kontrola dashboardu oraz rozróżnienie liczby i odsetka powracających.

**Trzy najsłabsze strony**

1. **Pewność języka czasem wyprzedza dowody.** Dotyczy to awarii przeglądarek wbudowanych, przepustowości oraz pewności braku korzyści z TikToka.
2. **Plan eksperymentów nie jest jeszcze gotowy do wykonania.** Brakuje mocy testu Meta, reguły dla wyniku nierozstrzygającego i pełnego projektu pomiaru marży TelemediGO.
3. **Wyceny nie tworzą jeszcze spójnej kolejności decyzji.** Część pochodzi z obecnego stanu, mimo deklaracji wykonania wcześniejszych działań. Najważniejszym przykładem jest próg Meta po naprawie zwrotów.

**Zgodność z zadaniem, punkt po punkcie**

| Wymaganie z A | Ocena |
|---|---|
| Kohorty dzienne i zdarzenia znalezione w danych | **Spełnione w opisanym rozwiązaniu.** Tygodniowa macierz nie narusza wymogu, skoro wykres pozwala wybrać dzień bez wygładzenia. Trzeba poprawić interpretację części zdarzeń i segmentów. |
| Lejki: gdzie i od kiedy tracimy pacjentów | **W dużej mierze spełnione.** Safari jest konkretnym znaleziskiem. Brakuje rozliczenia sygnału Google Ads na markę; problem przeglądarek wbudowanych opisano zbyt przyczynowo. |
| Narzędzie do prowadzenia biznesu, dostępne z linku | **Niepotwierdzone technicznie.** Zakres funkcji wygląda adekwatnie. Z tekstu nie ocenię obsługi, szybkości ani poprawności filtrów. Adres jest jeszcze zastępczy. |
| Priorytety z wartością, pomiarem i czasem | **Spełnione z istotnymi poprawkami.** Są 12 działań i kryteria sukcesu. Wymagają uzgodnienia zależności, kosztów i horyzontów. Pozycja 12 podaje koszt testu, ale nie jego roczną wartość. |
| Lista nierozstrzygniętych kwestii | **Spełnione dobrze.** Jest szeroka i powiązana z działaniami. Warto dopisać niepewność wyniku samych proponowanych testów. |

**Moja decyzja: zaliczyłbym kandydatowi tę część rekrutacji i zaprosił go do finałowej rozmowy.** Przesądza umiejętność zakwestionowania pozornego wzrostu na podstawie kohort i ekonomii, przy zachowaniu jawnych założeń.

Przed wysłaniem wymagałbym poprawienia wskazanych niespójności. Na rozmowie sprawdziłbym przede wszystkim, czy kandydat sam potrafi obronić próg wyłączenia Meta, zaprojektować rozstrzygający test i powiedzieć, co zmieniłoby jego decyzję. To lepiej odróżni przyszłego szefa biznesu od autora rozbudowanej analizy.
