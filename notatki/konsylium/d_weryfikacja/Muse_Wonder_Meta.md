# Muse Wonder (Meta) — meta/muse-wonder

# Końcowa weryfikacja rozwiązania — konsylium

Ocena wyłącznie na podstawie załączników A–E. Nie miałem dostępu do bazy, kodu ani działającej strony, więc nie sprawdzam: poprawności SQL/Pythona, wykresów, filtrów po kliknięciu, linku na żywo i tego, czy liczby w plikach `analiza/wyniki/` rzeczywiście wynikają z CSV. Tam, gdzie piszę „nie da się sprawdzić”, to znaczy właśnie to.

---

## 1. Lista poprawek od najważniejszej

### KRYTYCZNE

**1. [Krytyczna] Link do narzędzia nie istnieje w oddawanym materiale**
- Miejsce: Załącznik B, README, nagłówek: `https://<organizacja>.github.io/<repozytorium>/` — „adres uzupełnimy w dniu publikacji”.
- Co jest nie tak: Zadanie (A pkt 4) wymaga jako pierwszego deliverable „działające, otwierane w przeglądarce bez instalacji i bez zakładania konta”. W dniu wysyłki to jest warunek formalny, nie kosmetyka. Z załączników nie da się zweryfikować ani linku, ani działania filtrów/wykresów.
- Propozycja: przed wysłaniem wpisać prawdziwy URL, otworzyć go w trybie prywatnym bez logowania, sprawdzić wszystkie 9 zakładek i filtry kohort/lejka. Bez tego nie wysyłać.

**2. [Krytyczna] „Kohorty dzienne” są obiecywane, ale w tekście narzędzia dominują agregaty okresowe i macierz tygodniowa/miesięczna**
- Miejsce: Zakładka 2 „Kohorty” (C); Załącznik A pkt 3.1: „Kohorty w rozdzielczości dziennej”.
- Co jest nie tak: Główna tabela porównuje okres A vs B zagregowane; macierz jest „tygodniowe (do wyboru: tygodniowe / miesięczne)”. Dzienna rozdzielczość pojawia się dopiero w wykresie „suma z 7 dni kończących się danego dnia”. Opcja „bez wygładzenia (dzień)” istnieje w filtrze wykresu, ale czytelnik z domyślnego widoku nie widzi kohorty dzień-po-dniu.
- Dlaczego to krytyczne: zadanie mówi wprost, że kohorty dzienne to „najważniejsza część tego zadania” i że codziennie prowadzi się na nich biznes. Recenzent może uznać, że wymóg jest spełniony tylko przez wykres.
- Propozycja: dodać widoczną tabelę/widok kohort dziennych (dzień pierwszego zakupu × powrót 30/60/90/180 + n + marża), choćby zwijaną, i wprost nazwać ją w nagłówku zakładki. Nie usuwać 7-dniowego wygładzenia, ale nie chować pod nim rozdzielczości dziennej.

### WAŻNE

**3. [Ważna] Rozbieżność liczby powracających wyliczonej z odsetków vs podanej**
- Miejsce: Zakładka 1, tabela retencji i tekst „3 289 wobec 3 076 (+6,9%)”; E1 W2.
- Przeliczenie: 23,9% × 12 867 = 3 075,2 (zgadza się z 3 076); 17,4% × 18 924 = 3 292,8, a nie 3 289. Różnica wynika z zaokrąglenia odsetków (3 289/18 924 = 17,38%), ale czytelnik odtwarzający liczbę dostanie 3 293.
- Propozycja: dopisać „liczby powracających liczone przed zaokrągleniem odsetków” albo podać odsetki do 2 miejsc przy tej jednej liczbie. To drobiazg liczbowo, ale to jest liczba, którą sami dodaliście po uwadze Astry — będzie sprawdzana.

**4. [Ważna] Lejek: liczba płatności nie zgadza się z liczbą zamówień oczyszczonych — różnica ±1 w obu okresach, bez wyjaśnienia**
- Miejsce: Zakładka 3: okres 1 „24 717 płatności”, okres 2 „38 490 płatności”; Zakładka 6 i E2: 24 716 i 38 491 zamówień; E3 sekcja 1: zwykłe sesje 24 717 / 38 490.
- Co jest nie tak: W okresie 1 lejek ma o 1 płatność więcej niż jest zamówień, w okresie 2 o 1 mniej. Przy tak pedantycznym mostku dashboard→czyszczenie (604 duplikaty itd.) brak przypisu do różnicy 1 zamówienia osłabia zaufanie do reszty.
- Propozycja: jeden przypis: skąd różnica (np. płatność bez zamówienia / zamówienie bez kroku w sesji zwykłej / granica dnia UTC-PL). Jeśli to błąd eksportu — naprawić.

**5. [Ważna] Safari iOS: trzy różne okna „przed” używane wymiennie, a zakres 628–695 to dwie metody, nie jeden szacunek**
- Miejsce: Zakładka 3 (66,2%, 1 763 sesje, 16.01–16.03.2026); Zdarzenia pkt 12 (66,2%, „60 dni przed”); Priorytet 1 (66,1% „od 1.10.2025 do 16.03.2026”); E4 5f.
- Dowód z E4: 695 to wprost (66,1−45,6) na oknie od 1.10.2025; 628 to wariant po odjęciu tła innych przeglądarek (różnica różnic, spadek tła 2,0 p.p.). W narzędziu zakres „628–695” wygląda jak przedział jednego oszacowania.
- Dobrze, że Priorytet 1 dopisuje „to nie przedział ufności”, ale Zakładka 3 i Zdarzenia tego zastrzeżenia przy liczbie nie mają.
- Propozycja: wszędzie przy „628–695” dodać „695 = kontra faktyczne bez korekty; 628 = po odjęciu równoległej zmiany w innych przeglądarkach”. Ujednolicić też 66,1 vs 66,2 (różne okna — nazwać je).

**6. [Ważna] Kwota Safari za III kwartał 2026 (14–21 tys. zł) nie odtwarza się z liczb podanych obok**
- Miejsce: Zakładka 1 „Wynik pod koniec okresu”; Priorytet 1; D (ZNALEZISKA, wynik biznesu).
- Przeliczenie z podanych składników: 95–105 zamówień/30 dni × ok. 92 dni kwartału = 291–322 zamówień; × 64,6 zł marży 90-dniowej (Priorytet 1) = 18,8–20,8 tys. zł. Dolna granica 14 tys. zł z tych składników nie wychodzi (wychodziłaby przy marży ok. 48 zł albo krótszym oknie).
- Propozycja: pokazać składniki kwartału osobno (ile zamówień × jaka marża × ile dni po 17.03 w kwartale) albo zawęzić zakres do odtwarzalnego. To zdanie stoi obok spadku marży kwartału (−15,1 tys. zł) i będzie czytane jako „Safari tłumaczy kwartał” — musi być policzalne.

**7. [Ważna] Priorytet 4 (gs_generic_specjalisci): kwot rocznych nie da się odtworzyć z E6 i z własnej tabeli**
- Miejsce: Priorytet 4; E6 sekcja 2a.
- Przeliczenie: E6 (90 dni, reguła przyjęta) daje 719 pacjentów × wynik −23,7 zł = −17,0 tys. zł, a karta mówi „Dziś: −23,2 tys. zł”. Karta podaje jednocześnie koszt 57,6 zł i marżę „32–37 zł”: 923 pacjentów × (ok. 32,4 − 57,6) ≈ −23,3 tys. zł — czyli kwota wynika z pełnorocznej liczby pacjentów (923) przemnożonej przez parametry z kohort dojrzałych, a nie z kohorty E6. To jest defensywne metodologicznie (tak samo liczona jest „prognoza marży rocznika”, zał. 40), ale karta tego nie mówi, więc wygląda na niespójność z tabelą ekonomii w narzędziu.
- Ten sam problem, słabszy, w Priorytecie 9 (Meta L4): E6 daje 3 628 × +6,5 zł = 23,6 tys. zł, karta mówi +27,8 tys. zł.
- Propozycja: w kartach 4 i 9 dopisać jedną linijkę: „kwota roczna = pacjenci z całego okresu × wynik na pacjenta z kohort z pełnym oknem (jak prognoza rocznika, zał. 40); dlatego różni się od iloczynu z tabeli 90-dniowej”. Bez tego recenzent policzy tak jak ja i uzna liczby za niespójne.

**8. [Ważna] Porządek priorytetów nie ma jawnego kryterium — a liczby same go nie uzasadniają**
- Miejsce: Zakładka 8, przegląd i „Zasady listy”: „Kolejność to waga, a nie kalendarz”.
- Co nie przekonuje: Pozycja 1 to 75–95 tys. zł, ale pozycja 9 to decyzja „od −30,6 do +179,6 tys. zł”, pozycja 6 to „0 do 65 tys. zł” przy niskiej pewności, a pozycja 7 jest czystym scenariuszem (23,6 tys. zł „za każdy punkt” przy zerowym dowodzie, że komunikacja działa). Czytelnik nie wie, czy sortujecie po wartości, pewności, odwracalności, czy blokowaniu innych decyzji. Priorytet 2 ma 0–38 tys. zł i jest nr 2 — słusznie, ale z powodu „warunku pozostałych decyzji”, co jest innym kryterium niż wartość.
- Propozycja: dodać 3–4 zdania kryterium, np. „najpierw: pewna strata, która rośnie każdego dnia i jest tania w naprawie; potem: zatrzymanie pewnych strat gotówkowych; potem decyzje wymagające testu; na końcu opcje o nieznanym znaku”. To zamieni zarzut „kolejność arbitralna” w świadomą tezę.

**9. [Ważna] Wniosek o porannej przepustowości jest mocniejszy, niż pozwala projekt porównania**
- Miejsce: Zakładka 4 „Odczytanie: spadła poranna przepustowość…”; DECYZJE 2026-10-19 (kroki 4–5 retencji).
- Co jest dobrze: pokazujecie porównanie przy tym samym ruchu dziennym (+26,4 p.p., 5 przedziałów, 9 979 wizyt) i brak zależności od ruchu wewnątrz miesiąca. To jest najlepszy dowód w całym rozwiązaniu.
- Co jest ponad dane: porównujecie dni według liczby wizyt porannych, ale nie kontrolujecie składu tych wizyt (cel wizyty, nowi vs powracający, udział L4), długości kolejki terminów ani tego, czy zmienił się horyzont rezerwacji (czas zapłata→termin — piszecie, że się nie zmienia, ale tylko ogólnie). „Przepustowość spadła” jest odczytaniem, nie pomiarem; sami listujecie trzy możliwe przyczyny, z których żadnej dane nie rozstrzygają.
- Propozycja: tytuł odczytania zmienić na „przy tym samym ruchu opóźnień jest o 26 p.p. więcej — to nie jest samo przeciążenie liczbą wizyt; przyczyny (obsada/organizacja/pacjenci spoza B2C) dane nie rozstrzygają”. Treść już to faktycznie mówi; nagłówek mówi więcej.

**10. [Ważna] Pominięcie: kohorty nie są cięte cechami pacjenta z `users.csv`, choć plik je zawiera**
- Miejsce: Zakładka 2 — filtry: źródło, kampania, urządzenie, przeglądarka, usługa, zniżka, GO, status, punktualność. Brak: płeć, rocznik/wiek, województwo, wielkość miejscowości, zgoda marketingowa jako cecha kohorty (zgoda wraca tylko w priorytetach jako hipoteza).
- Dlaczego ważne: zadanie prosi ciąć kohorty „tak, żeby było widać, co się wydarzyło”. Region jest wam zresztą potrzebny w teście dodatkowości (pary województw, Priorytet 9) — skoro test zakłada porównywalność województw, baza powinna pokazać, czy kohorty różnią się regionalnie już dziś. Jeśli sprawdziliście te cięcia i nic nie wyszło — to też jest wynik, który warto zapisać („sprawdzone, bez sygnału”), tak jak robicie to w zakładce Jakość danych.
- Propozycja: dodać jedną linijkę w Kohortach albo w „Czego nie wiemy”: które cięcia demograficzne sprawdzono i z jakim wynikiem.

**11. [Ważna] Założenie 19 nie obejmuje okna 180 dni, a narzędzie i wnioski na nim stoją**
- Miejsce: D, ZALOZENIA pkt 19 („okna 30, 60 i 90 dni”) vs pkt 27, zakładki 1–2, E2 (okna 180, 270, 365).
- Propozycja: dopisać 180 dni do definicji powrotu (i datę obcięcia 3.04). Definicje mają być „ustalone przed kohortami” — recenzent porówna je z narzędziem.

### DROBNE

**12. [Drobna, ale widoczna] Średnia ocena ze znakiem procentu**
- Zakładka 4, tabela ocen: „4,45% z 3 446”, „2,92% z 469”. Średnia 1–5 nie jest procentem. Poprawić na samą liczbę. Taki błąd w tabeli podważa pedantyczność całości.

**13. [Drobna] Spadek powrotu 180-dniowego: −5,3 p.p. vs −5,2 p.p.**
- Zakładka 1 i E2 (1b): −5,3 (27,5→22,2). Zakładka 2, tabela kohort: „▼3,2 / ▼5,4 / ▼6,5 / ▼5,2”. Z E2: 27,5−22,2 = 5,3. Wyrównać do −5,3 (albo pokazać, że liczono na niezaokrąglonych).

**14. [Drobna] „Nowi pacjenci i TelemediGO się nie zmieniają” po czyszczeniu — zmieniają się minimalnie**
- README „Odpowiedź w skrócie” i Zakładka 1 zastrzeżenie 1 vs mostek: dashboard 16 251→24 689, po czyszczeniu 16 231→24 687 (20 kont testowych mniej w każdym okresie; wzrost 51,9%→52,1%). W Zakładce Jakości danych mostek pokazuje to poprawnie. W skrótach napisać „prawie się nie zmieniają (+51,9% → +52,1%)”.

**15. [Drobna] E1 W3 pokazuje zmianę przychodu +45,0%, teksty mówią +44,8%**
- 3 228 342 / 2 230 266 − 1 = 44,75% → 44,8%. Kolumna raportu zaokrągla do 45,0. Skoro raporty są „źródłem każdej liczby”, wyrównać format do 1 miejsca po przecinku tak, by 44,8 było odtwarzalne (44,75 → 44,8, nie 45,0 przy zapisie z jednym miejscem — zależy od reguły; po prostu ujednolicić).

**16. [Drobna] Zdarzenia z podziału binarnego są prezentowane na osi na równi ze zdarzeniami twardymi**
- Oś ma 13 zdarzeń; starty kampanii i awaria Safari to fakty z datą dzienną, ale np. „30.10.2025 marża spada stopniami” czy „2.03.2026 brak wyraźnego skoku” to kandydaci z progu |z|≥4 nałożeni na serie kohort, których 30/90-dniowe okna wygładzają i przesuwają daty. Dopisek „daty to kandydaci zmian” jest przy kilku kartach, ale nie przy osi jako całości ani przy zdarzeniu 11, które jest de facto brakiem zdarzenia.
- Propozycja: oznaczyć na osi wizualnie dwie klasy: „data z danych źródłowych” vs „kandydat z wykrywania zmian”. Zdarzenie 11 przenieść do karty retencji jako wynik negatywny.

**17. [Drobna] Definicja „miesiąca” kohorty jest niespójna między tekstami**
- Zał. 34: miesiąc 1 = dni 0–30; E2 sekcja 3: „miesiąc 1 = dni 0–30 (z pierwszym zamówieniem), miesiąc m = dni 30(m−1)+1…30m” — czyli miesiąc 1 ma 31 dni w zapisie 0–30 włącznie, kolejne po 30. Bez wpływu na wnioski, ale definicja ma być jednoznaczna.

---

## 2. Co się potwierdziło (przeliczyłem z załączników)

- **Wzrost nowych pacjentów:** 24 687/16 231 − 1 = 52,09% → +52,1%. ✓
- **Zamówienia po czyszczeniu:** 38 491/24 716 − 1 = 55,73% → +55,7%; dashboard 40 613/25 269 − 1 = 60,73% → +60,7%. Mostek: duplikaty −604 tylko w okresie 2 (40 613−604 = 40 009, +58,3% ✓), testy −553/−1 518 (25 269−553 = 24 716 ✓; 40 009−1 518 = 38 491 ✓).
- **Przychód:** przed zwrotami 3,508/2,375 − 1 = 47,7% ✓; po zwrotach 3 228 342/2 230 266 − 1 = 44,75% → +44,8% ✓ (z zastrzeżeniem pkt 15).
- **TelemediGO:** 2 468/1 759 − 1 = 40,3% ✓; rozbicie 905+629+225 = 1 759 ✓, 1 089+918+461 = 2 468 ✓, wzrost 184+289+236 = 709 ✓, udziały 26/41/33% ✓. Opłaty: 1 759×89 = 156 551 ✓; 2 468×89 = 219 652 ✓. Rachunek zniżek: 156 551 − 183 939 = −27 388; /1 759 = −15,57 zł ✓.
- **Retencja na tych samych dniach kalendarzowych:** wszystkie cztery okna w Zakładce 1 zgodne z E1 W2 i E2 1b (30: 11,0→7,8; 60: 19,1→13,7; 90: 23,9→17,4; 180: 27,5→22,2) wraz z n. Metoda (pełne okno + obcięcie okresu 1 do tej samej daty) jest poprawna i jest właściwą odpowiedzią na młode kohorty. Bez nowych kampanii: 22,0% (Z1K) / 20,4% (Z2) ✓ zgodne między C, D i E1.
- **Marża na pacjenta 90 dni:** 66,6 → 58,3 zł (−8,3; −12,5%) ✓ E2.
- **Marża roczna i kwartalna:** kwartały sumują się do roku: 259 375+324 423+256 558+207 713 = 1 048 069 ✓; rok wcześniej 828 085 ✓; +26,6% ✓. Q3 2026: 207 713 vs 222 824 = −6,78% ✓; wydatki 181 555/87 431 = 2,077 → 2,08× ✓; rozbicie −15 111 = +78 963 − 94 123 + 50 ✓ (E1 W4). Miesiące VII–IX zgodne z tabelą miesięczną.
- **Start od zera:** 24 687 + 5 289 + 8 515 = 38 491 ✓; korekta +26,6% → +8,1% po odjęciu marży powtórnych kohort okresu 1 (1 048 069 − 152 960 = 895 109; /828 085 = +8,09% ✓) i +3,1% po odjęciu ich GO (853 635/828 085 = +3,09% ✓). Uczciwie nazwane rozbiciem księgowym.
- **Lejek:** 24 717/154 085 = 16,04% ✓; 38 490/280 625 = 13,72% ✓; rozkład: −3,00 (struktura) + 0,67 (konwersja w grupach) = −2,33 p.p. ✓ zgodny z E3 sekcja 4 dla przeglądarki/kanału. Udział przeglądarek aplikacyjnych: (9 560+6 873)/154 085 = 10,66% ✓; (39 744+31 535+28 676)/280 625 = 35,61% ✓.
- **Ekonomia kampanii:** nowe kampanie L4 (Z1K, 90 dni): 36,3 − 32,7 = +3,6 zł ✓; (Z2): 36,1 − 45,6 = −9,5 ≈ −9,4 (zaokrąglenia) ✓. TikTok ujemny w obu regułach i oknach ✓ E6. Wniosek „znak zależy od reguły → niepewny” jest metodologicznie poprawny i konsekwentnie stosowany.
- **Koszt lekarza za testy:** 2 071 × 25 = 51 775 zł ✓; okres 2: 1 518 × 25 = 37 950 zł ✓ (Priorytet 2).
- **Cennik specjalistów (E7 3a):** wszystkie marże katalogowe i po GO policzone poprawnie (np. 109×0,8 = 87,2; 87,2−100 = −12,8 ✓; psychiatra 269×0,8 = 215,2; +15,2 ✓). Strata GO u specjalistów okres 2: −14 682 zł na 1 512 zamówieniach ✓ (E7 3c).
- **Definicje:** nowy pacjent / powrót (nieanulowane) / przychód po zwrotach / koszt lekarza także za zwrócone / prowizja 25 zł — wszystkie zgodne z zasadami z A pkt 6, nazwane przed kohortami, z policzonymi wariantami odrzuconymi (zał. 16: warianty zmieniają wzrost o ≤0,5 p.p.). Porównanie okresów na tych samych dniach kalendarzowych — poprawne i konsekwentne.
- **Jakość danych:** duplikaty (604, okno 10–24.06.2026, jeden krok płatności w analityce → błąd eksportu, nie podwójne płatności) i konta testowe (dwa niezależne podpisy: kod TEST-QA na koncie i czas wizyty 1 min przy minimum 3 min u pozostałych) — identyfikacja przekonująca. Godzina bez danych 17.05.2025 trafnie oznaczona jako pomijalna, ale odnotowana.

---

## 3. Ocena z perspektywy zlecającego zadanie

### Trzy najmocniejsze strony
1. **Odpowiedź na pytanie zadania jest bezpośrednia i policzalna.** „Nie — pacjentów więcej (+52,1%), retencja gorsza (23,9%→17,4% na tych samych dniach), więc z dwóch warunków wzrostu spełniony jest jeden.” Do tego korekta dashboardu mostkiem (61%→55,7%, 50%→44,8%) i domknięcie tematu kwartalnego (marża Q3 2026 −6,8% przy wydatkach 2,08×). To jest dokładnie format, o który prosi zadanie.
2. **Dyscyplina atrybucji.** Dwie reguły źródła prowadzone równolegle przez kohorty, ekonomię i priorytety; kampanie o znaku zależnym od reguły nazywane „niepewnymi”, a nie wnioskami; scenariusze „naprawić albo wyłączyć” w trzech wariantach dodatkowości; kwoty niesumowane z podaną przyczyną. To jest rzadkie i zawodowe.
3. **Zdarzenia znalezione w danych, nie przepisane z kalendarza:** starty kampanii co do dnia z sesji i wydatków, awaria Safari 17.03.2026 z kontrolą na innych przeglądarkach i kanałach, poranne opóźnienia z porównaniem przy tym samym ruchu, zwroty L4 17,4% vs 5,3%. Plus uczciwa lista 18 niewiadomych, każda z testem domykającym.

### Trzy najsłabsze strony
1. **Forma oddania w chwili kontroli:** brak działającego linku w README (pkt 1) i dzienna rozdzielczość kohort schowana pod wykresem 7-dniowym oraz macierzą tygodniową (pkt 2). Obie rzeczy dotyczą wprost dwóch pierwszych wymagań zadania.
2. **Odtwarzalność części kwot priorytetów z raportów** (pkt 6 i 7): Safari-kwartał i kwoty roczne kampanii wymagają domyślenia metody „prognozy rocznika”. Przy tak silnym śladzie pracy (`analiza/wyniki/…` przy każdej liczbie) te dwa miejsca wyglądają jak luki, choć prawdopodobnie są tylko niedopisane.
3. **Brak jawnego kryterium kolejności priorytetów i brak cięć demograficznych kohort** (pkt 8 i 10) — pierwsze osłabia użyteczność listy dla decydenta, drugie jest realnym pominięciem wobec danych, które paczka zawiera.

### Czego brakuje wobec zadania (A pkt 5)
- Kohorty dzienne: częściowo (patrz pkt 2) — do domknięcia jednym widokiem.
- Lejki „gdzie i od kiedy tracimy”: spełnione (Safari od 17.03.2026, przeglądarki aplikacyjne na każdym kroku, sesje zalogowane osobno).
- Narzędzie na co dzień: nie do oceny z załączników — warunek konieczny do sprawdzenia przed wysyłką.
- Priorytety z wartością, pomiarem i czasem: spełnione przy każdej z 12 pozycji; zastrzeżenia tylko do odtwarzalności dwóch kwot i kryterium kolejności.
- Lista nierozstrzygalnego: spełniona wzorowo (18 pozycji, każda z testem i kosztem domknięcia).

### Decyzja
**Tak — kandydat nadaje się do kolejnego etapu / zatrudnienia na tę rolę, a rozwiązanie można wysłać po dwóch poprawkach krytycznych (link i widok kohort dziennych) oraz dopisaniu trzech wyjaśnień (pkt 5, 6, 7).**

Uzasadnienie: przesądza na plus to, że kandydat odpowiada na pytanie biznesowe, a nie produkuje raport: rozdziela wzrost liczby pacjentów od retencji, koryguje dashboard, znajduje zdarzenia w danych, nie wyciąga wniosków przyczynowych ponad atrybucję i zamienia analizę w kolejkę decyzji z ceną i testem. Na minus — wyłącznie wykonanie na ostatniej prostej: formalny brak linku, niedopowiedzenie rozdzielczości dziennej i trzy miejsca, w których liczba nie odtwarza się z podanych składników. To są poprawki na godziny, nie na tygodnie; ale przy zadaniu, którego sens brzmi „pokaż, na czym faktycznie pracujesz”, niedziałający link w dniu wysyłki przekreśliłby całość niezależnie od jakości analizy.

**Czego nie wiem na pewno:** czy narzędzie po kliknięciu rzeczywiście liczy kohorty dzienne i czy filtry działają — to rozstrzygnie dopiero otwarcie linku; oraz czy liczby w raportach E wynikają z bazy (sprawdzają to członkowie zespołu z dostępem do plików).
