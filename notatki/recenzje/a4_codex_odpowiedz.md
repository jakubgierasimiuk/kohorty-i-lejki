**Nie znalazłem błędu odwracającego ogólny wynik: nowych pacjentów przybywa, a retencja całej bazy spada.** Przed analizą kohort trzeba jednak doprecyzować porównanie okresów i definicję powrotu po newsletterze lub SMS-ie. Poniżej uwagi od najważniejszej.

1. **Waga: ważna — brakuje rozdzielenia zmiany struktury pacjentów od zmiany ich zachowania.**

   Spadek łącznej retencji nie oznacza, że porównywalni pacjenci zaczęli wracać równie mocno rzadziej. Na wynik wpływa również większy udział kanałów pozyskujących pacjentów o niskiej retencji.

   **Dowód:** [raport, linia 364](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/wyniki/a4_definicje.txt:364). Udział Meta w pozyskaniu wzrasta z 6,3% do 24,9%. TikTok pojawia się dopiero w drugim okresie. Własne przeliczenie na kohortach z pełnym oknem pokazuje, że przy strukturze kanałów z pierwszego okresu retencja drugiego wynosiłaby **21,29%**, wobec rzeczywistych **17,38%**. Pierwszy okres osiąga **23,60%**. To przeliczenie nadaje TikTokowi zerową wagę, ponieważ nie występował w pierwszym okresie.

   **Propozycja poprawki:** zapisać dwa osobne wyniki: retencję całej pozyskanej bazy oraz zmianę retencji przy stałej strukturze kanałów. Następnie porównać również pierwszą usługę i zniżkę. TikTok pokazać osobno jako nowy segment. Wyniku po ujednoliceniu struktury nie przedstawiać jako dowodu przyczynowego.

2. **Waga: ważna — pełne okno obserwacji nie zapewnia porównywalnego zakresu kalendarzowego.**

   `stopy()` poprawnie odrzuca niedojrzałe kohorty. W rezultacie porównuje jednak cały pierwszy rok z krótszą częścią drugiego roku, co pozostawia wpływ sezonowości.

   **Dowód:** [kod, linia 149](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a4_definicje.py:149). Dla retencji w 90 dniach pierwszy okres obejmuje 16 231 pacjentów z 365 dni. Drugi obejmuje 18 924 pacjentów z 275 dni, do 2.07.2026. Po ograniczeniu pierwszego okresu do analogicznej daty, 2.07.2025, otrzymuję **23,91% wobec 17,38%**. Kierunek wniosku pozostaje ten sam.

   **Propozycja poprawki:** zachować obecne liczby jako opis dostępnych dojrzałych kohort. Do porównania okresów dodać jednak odpowiadające sobie dni kalendarzowe, osobno dla okien 30, 60 i 90 dni. Pokazywać liczebność mianownika przy każdym wyniku.

3. **Waga: ważna — „powrót po CRM” obejmuje anulowane zamówienia, choć przyjęta retencja je wyklucza.**

   Punkt 26 mówi o zapłacie, więc kod realizuje jego dosłowne brzmienie. Powstaje jednak druga definicja powrotu, niespójna z punktem 19. Wyników tych nie należy bezpośrednio zestawiać.

   **Dowód:** [kod, linia 501](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a4_definicje.py:501). `po_kontakcie` nie filtruje statusu zamówienia. Dla trzech kampanii konsultacyjnych, bez sprzedaży TelemediGO, w ciągu 24 godzin liczy **2 892 przypisania zamówień, w tym 103 anulowane**. Wykluczenie anulowanych obniża wynik z **189,2 do 182,4 zamówienia na 1 000 wejść**. Przykład: pacjent **100157**, zamówienie **5003007**, anulowane po płatności 24.10.2024 o 21:44:50, jest liczone po wejściu o 21:39:23.

   **Propozycja poprawki:** podstawowy wynik liczyć według przyjętej definicji retencji, czyli bez anulowanych zamówień. Wszystkie płatności pokazać jako osobną miarę, z jednoznaczną nazwą.

4. **Waga: ważna — brakuje zasady rozstrzygającej nakładające się kontakty.**

   Jedno zamówienie może zostać przypisane do kilku wejść z newslettera lub SMS-a. Jest to dopuszczalne w analizie „co nastąpiło po kliknięciu”, ale zawyża liczbę zamówień, jeśli wyniki traktujemy jako rozłączne przypisanie sprzedaży.

   **Dowód:** [kod, linia 504](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a4_definicje.py:504). W oknie 24 godzin **2 892 unikalne zamówienia otrzymują 2 903 przypisania**. Jedenaście zamówień występuje dwukrotnie. W oknie siedmiodniowym jest **3 259 zamówień i 3 366 przypisań**. Przykład: pacjent **103515**, zamówienie **5024834**, jest przypisany do kontaktów z 20.02.2025 o 08:48:14 i 18:49:21.

   **Propozycja poprawki:** do przypisywania sprzedaży wybrać ostatni kwalifikujący kontakt przed płatnością. Obecną analizę zachować jako profil zakupów po każdym kliknięciu i zaznaczyć, że jej wiersze nie są rozłączne.

5. **Waga: drobna — przedziały godzinowe są liczone z czasu polskiego bez informacji o strefie.**

   `epoch()` na takim znaczniku czasu nie uwzględnia zmiany czasu letniego i zimowego. Przedziały definiowane jako wielokrotności 24 godzin należy liczyć na czasie UTC.

   **Dowód:** [kod, linia 503](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a4_definicje.py:503). Porównanie z początkiem sesji i zdarzeniem płatności w UTC zmienia numer przedziału dla **59 par kontakt–zamówienie**. Pacjent **100326**, kontakt 24.10.2024 o 20:51:25 i zamówienie **5006936** z 20.11.2024 o 20:41:29: kod przypisuje przedział 26, a rzeczywisty upływ czasu — 27. **W sprawdzonych danych nie zmienia to kwalifikacji do okna 24 godzin ani siedmiu dni.**

   **Propozycja poprawki:** zachować polskie daty do kohort dziennych. Odstępy godzinowe liczyć z `started_at_utc` i czasu płatności w UTC. Analogicznie poprawić obliczenia zakupów TelemediGO.

6. **Waga: drobna — tło wymaga 61 dni obserwacji, a filtr zapewnia 60.**

   Przedziały `dzien BETWEEN 31 AND 60` obejmują czas od początku 31. do początku 61. doby. Dla kontaktów z 1.08.2026 końcówka tego przedziału wypada już po końcu eksportu.

   **Dowód:** [kod, linia 499](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a4_definicje.py:499) oraz [linia 576](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a4_definicje.py:576). Problem dotyczy **53 kontaktów CRM**, w tym 48 poza kampanią sprzedaży TelemediGO. Po wymaganiu pełnych 61 dni tło zmienia się z **4,4155 do 4,4229 zamówienia na 1 000 wejść na dobę**. Wpływ jest minimalny.

   **Propozycja poprawki:** zastosować dokładny warunek `ts + INTERVAL 61 DAY <= TIMESTAMP '2026-10-01'`.

7. **Waga: drobna — znacznik „zalogowana od wejścia” pomija wyjątek dotyczący samego TelemediGO.**

   Punkt 10 wyklucza takie zakupy z tego rozpoznania, ale tabela `kontakt` tego wyjątku nie stosuje.

   **Dowód:** [kod, linia 497](/C:/Users/K/Desktop/Zadanie%20-%20TM/analiza/a4_definicje.py:497). Znalazłem **621 sesji samodzielnego zakupu TelemediGO**, oznaczonych jako zalogowane od wejścia. Przykład: pacjent **120787**, sesja **30200517**, zakup 8.09.2025. Obecny podział konsultacyjnych kampanii CRM nie jest tym zniekształcony, ponieważ wyklucza kampanię `crm_go_upsell`.

   **Propozycja poprawki:** zastosować wyjątek z punktu 10 albo wydzielić osobną kategorię zakupu samego TelemediGO.

Za poprawne uznaję następujące elementy:

- **Odtwarzalność raportu.** Obliczenia wykonane po wyłączeniu operacji zapisu w pamięci odtworzyły wszystkie 399 linii raportu, poza datą uruchomienia. Nie zmieniłem ani nie utworzyłem plików.
- **Nowego pacjenta i datę kohorty.** Pierwsze opłacone zamówienie dowolnego statusu jest uzasadnioną definicją wobec treści zadania. Potwierdzam 16 231 nowych pacjentów w pierwszym okresie i 24 687 w drugim, czyli wzrost o 52,1%.
- **Retencję konsultacyjną.** `z.t > k.t0` wyklucza zamówienie inicjujące kohortę. Dni są liczone kalendarzowo. Filtr pełnego okna obejmuje zarówno licznik, jak i mianownik.
- **Granice czasu i okresów.** Wszystkie sesje mają poprawnie przeliczony czas UTC na Europe/Warsaw i zgodny dzień polski. Pacjent **133036**, z pierwszą płatnością 30.09.2025, trafia do pierwszego okresu. Pacjent **133138**, z płatnością 1.10.2025 o 00:02:09, trafia do drugiego. Kohorta pacjenta **171917** z 2.07.2026 kwalifikuje się do okna 90 dni, a kohorta pacjenta **172011** z 3.07.2026 jest wykluczana mimo zaobserwowanego powrotu.
- **Przypisywanie źródła.** `ses_pac` i `sp` realizują opisaną regułę i ograniczają sesje do momentu pierwszej płatności. Nie znalazłem współdzielonych przeglądarek między kontami, remisów czasu sesji w `sp` ani częściowo pustych oznaczeń UTM. `arg_min`, `arg_max` i nadpisania kodami w `Z1K`, `Z2K`, `Z3K` działają poprawnie w tych danych. Zgodność z kodem kampanii pozostaje sprawdzeniem spójności, a nie dowodem przyczynowego pozyskania.
- **TelemediGO.** Dodatkowo sprawdziłem wpływ jego osobnych zakupów na przyjęty wariant retencji bez anulowanych zamówień. Nie zmienia wyniku w żadnym z okien 30, 60 i 90 dni.
- **Start od zera.** Po wyłączeniu kohort z października 2024 retencja pierwszego okresu wynosi 23,72%, wobec 17,38% w drugim. Początkowy miesiąc nie tłumaczy spadku.
- **Liczby w punktach 16–26.** Potwierdzam przytoczone liczebności, retencję według statusu, przychody po zwrotach i prowizję afiliacyjną. Drobny szczegół: 0,7% remarketingu w punkcie 24 dotyczy reguły bez nadpisania kodem; przy przyjętej regule udział wynosi 0,6%. Prowizja 30 825 zł jest poprawna przy zadanym założeniu, ale jej rzeczywistej należności nie da się potwierdzić bez warunków umowy.

Ręcznie porównałem surowe wiersze z wynikami dla **siedmiu różnych pacjentów** — plik zawiera osiem przypadków, ponieważ pacjent 100127 występuje dwukrotnie:

- **100127:** anulowana płatność 2.10.2024 inicjuje kohortę; pierwsza nieanulowana i odbyta konsultacja przypada 14.10.2024. Powrót następuje po 12 dniach. Anonimowa sesja organiczna poprawnie wyznacza źródło mimo dwóch przeglądarek.
- **100026:** zwrócona po wizycie konsultacja inicjuje wszystkie cztery warianty kohorty. Przychód po zwrocie wynosi 0 zł. Powrotu nie ma.
- **100081:** anonimowe wejście z ogólnej kampanii Google Ads poprzedza bezpośrednią sesję płatności. Pierwsze wejście i sesja płatności poprawnie dają różne źródła.
- **138084:** sesja jest bezpośrednia, ale kod `L4SZYBKO20` poprawnie zmienia źródło na kampanię Meta we wszystkich trzech wariantach z kodem.
- **100308:** anulowane drugie zamówienie przypada po 49 dniach. Pierwszy kwalifikujący powrót następuje dopiero po 92 dniach, więc nie jest retencją w 90 dniach.
- **101505:** pierwszy powrót następuje po 96 dniach. Zamówienie 26.02.2025 o 10:42:13 poprawnie przypisuje się do wejścia z SMS-a o 07:57:02, mimo płatności w innej sesji.
- **100197:** pierwsze wejście pochodzi z rankingu, a płatność z remarketingu Meta. Przyjęta reguła poprawnie przypisuje ranking i prowizję 25 zł.

Nie da się z tych danych potwierdzić wpływu wysyłek CRM ani remarketingu na zakupy. Są kliknięcia i zakupy, ale nie ma odpowiedniej grupy kontrolnej. Brak dat zwrotów uniemożliwia też odtworzenie ich rzeczywistego rozkładu dziennego; przypisanie do dnia płatności jest poprawnie nazwanym założeniem.