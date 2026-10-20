# Grok (xAI) — x-ai/grok-4.7

Nie wysyłałbym paczki w tym stanie tylko z jednego powodu operacyjnego: w README nie ma działającego linku. Samej odpowiedzi „to nie jest wzrost w sensie z zadania” nie podważam. Żaden sprawdzony rozjazd nie zmienia znaku tej odpowiedzi ani znaku pauzy TikToka i Google Ads na specjalistów.

Czego nie dało się sprawdzić z załączników: wykresów, 85 z 105 wierszy macierzy kohort, 225 z 245 zmian lejka oraz plików `a5e_scenariusze.txt`, `a5r_struktura.txt` i pełnego `c_szkic.md`. Kwoty scenariuszy pauzy i naprawy, których nie ma w E6, są więc niesprawdzone, nie „błędne”.

## 1. Lista poprawek

**1. Brak linku, który zadanie uznaje za oddanie pracy**
- Waga: krytyczna przed wysłaniem, nie błąd analizy.
- Miejsce: README, sekcja „Narzędzie”; `DECYZJE.md`, wpis o trzeciej wersji („Publikacji na razie nie robimy”).
- Co jest nie tak: adres to `https://<organizacja>.github.io/<repozytorium>/`. Zadanie wymaga strony bez instalacji i bez konta.
- Dowód: „adres uzupełnimy w dniu publikacji”.
- Poprawka: opublikować, wstawić prawdziwy URL i otworzyć go w czystej przeglądarce. Dopiero wtedy wysyłać.

**2. Karta TikToka zaprzecza własnej tabeli**
- Waga: ważna.
- Miejsce: Priorytety, pozycja 3, akapit „Propozycja”; ta sama pewność w tabeli przeglądu.
- Co jest nie tak: tekst mówi, że naprawa „w najlepszym razie doprowadza wynik do zera”, a tabela pokazuje po naprawie zwrotów +3,0 i +1,4 tys. zł. „Wysoka pewność co do znaku” kłóci się z własnym przedziałem 180 dni przy przyjętej regule: −5,3 do +3,0 zł na pacjenta (299 pacjentów).
- Dowód: „w najlepszym razie doprowadza wynik do zera”; tabela: „+3,0 tys. zł” / „+1,4 tys. zł”. E6 potwierdza −4,6 i −17,8 zł oraz −1,1 i −11,0 zł na pacjenta, więc punktowo znak jest ujemny.
- Poprawka: „naprawa przy pełnym budżecie daje co najwyżej mały plus w jednej regule i dalej duży minus w drugiej; przedział 180 dni przy przyjętej regule zawiera zero. Pewny jest brak wyraźnej korzyści, nie każda złotówka straty.” Pauza jako decyzja odwracalna może zostać.

**3. Dolna granica 14 tys. zł za Safari w III kwartale nie wynika z podanej metody**
- Waga: ważna.
- Miejsce: „Czy to wzrost”, karta „Wynik pod koniec okresu”; Priorytety, pozycja 1.
- Co jest nie tak: tekst mówi, że 14–21 tys. zł to przybliżenie ze średniej straty z 198 dni. Przy równomiernym rozłożeniu wychodzi około 19–21 tys. zł, nie 14–21.
- Przeliczenie: 628 × 92/198 × 64,6 zł = 18,8 tys. zł; 695 × 92/198 × 64,6 zł = 20,9 tys. zł. Spadek kwartału: 222 824 − 207 713 = 15 111 zł.
- Poprawka: albo pokazać osobny rachunek, z którego wychodzi 14, albo napisać 19–21 tys. zł. Zdanie, że wyniku kwartału bez awarii nie ustalono, zostawić. Przy 19–21 problem jest większy niż spadek kwartału, nie tylko „porównywalny”.

**4. Dwa różne wyniki L4 „z pozostałych kanałów”**
- Waga: ważna.
- Miejsce: „Czy to wzrost”, akapit pod tabelą powrotów; E1, W2.
- Co jest nie tak: zakładka podaje 13,9% (2 797) wobec 14,8% (2 639). Raport W2 dla internisty L4 bez nowych kampanii, ta sama reguła i te same dni: 13,8% (2 969) wobec 14,6% (2 795). Kierunek „bez istotnej zmiany” jest w obu cięciach, ale to nie są te same liczby. Źródło cytowane przy zdaniu to `a5r_struktura.txt`, którego tu nie ma.
- Dowód: cytat zakładki „13,9% (2 797 pacjentów) wobec 14,8% (2 639)”; W2: `14.6 / 13.8`, `2795 / 2969`.
- Poprawka: jedno cięcie, z nazwą reguły i mianownikiem jak w W2, albo jawnie napisać, czym „pozostałe kanały” różnią się od „bez nowych kampanii”.

**5. Nagłówek TelemediGO mówi więcej niż własna tabela**
- Waga: ważna.
- Miejsce: „Czy to wzrost”, „TelemediGO: skąd +40,3% sprzedaży”.
- Co jest nie tak: „Odsetek pacjentów, którzy kupują TelemediGO, nie rośnie.” Przy kolejnym zamówieniu rośnie z 9,27% (6 784) do 9,86% (9 307). Przy pierwszym spada z 5,58% do 4,41%.
- Przeliczenie udziałów we wzroście: 184/709 = 25,95% → 26%; 289/709 = 40,8% → 41%; 236/709 = 33,3% → 33%. To się zgadza. Rozkład z E7 (nowe komórki −1,22 pkt przy zmianie −1,16 pkt) nie uprawnia też do słowa „w całości” przy spadku odsetka na pierwszym zamówieniu.
- Poprawka: „odsetek przy pierwszym zamówieniu nie rośnie; przy kolejnym rośnie lekko; sprzedaż rośnie głównie liczbą zamówień i pełnym rokiem newslettera.”

**6. 65,2 tys. zł za poranek nie da się odtworzyć z karty**
- Waga: ważna.
- Miejsce: Priorytety, pozycja 6; zestawienie z `ZNALEZISKA.md` i założeniem 43.
- Co jest nie tak: karta daje zakres 0–65,2 tys. zł bez wzoru. Prosty rachunek ze spadku starych kampanii przy przyjętej regule tego nie daje. Wąski wariant z notatek, około 12 tys. zł, na karcie znika, więc 65 tys. wygląda jak równorzędna górna granica. Założenie 43 samo mówi, że szeroki wariant nie jest formalną górną granicą.
- Przeliczenie: 17 419 × 1,9% × 95,6 zł ≈ 31,6 tys. zł. Z notatek: 0,76 pkt z 1,91 pkt × ta sama baza × 95,6 zł ≈ 12,7 tys. zł. 19 500 × 3,5% × 95,6 zł = 65,2 tys. zł, czyli najszersze cięcie (sesja płatności, wszyscy pacjenci okresu 2, nie tylko kohorty z pełnym oknem). Tego wzoru na karcie nie ma.
- Poprawka: na karcie i w przeglądzie napisać 0 / około 12 / do 65 tys. zł oraz dokładnie: reguła, liczba pacjentów, punkty procentowe, 95,6 zł.

**7. Jedna kolumna kosztu pozyskania nie pasuje do wyniku po 180 dniach**
- Waga: ważna.
- Miejsce: „Wynik biznesu”, tabela ekonomii kampanii.
- Co jest nie tak: koszt 32,7 zł stoi przy wyniku +3,6 zł (90 dni) i przy +7,0 zł (180 dni). 36,3 − 32,7 = 3,6, ale 37,3 − 32,7 = 4,6, nie 7,0. Po 180 dniach koszt z E6 to 30,3 zł (37,3 − 7,0).
- Dowód: E6, okno 180, Z1K: koszt 30,3, marża 37,3, wynik 7,0, 2 352 pacjentów.
- Poprawka: osobna kolumna kosztu dla 180 dni albo podpis, że 32,7 zł dotyczy tylko okna 90 dni.

**8. Średnia ocena jest pokazana jako procent**
- Waga: ważna.
- Miejsce: „Po zakupie”, tabela „Oceny według opóźnienia wizyty”.
- Co jest nie tak: „4,45% z 3 446” to średnia ocen 1–5, nie odsetek. To samo przy 4,38%, 3,69%, 2,92%.
- Dowód: nagłówek kolumny „Średnia ocena (1–5)” i komórka „4,45% z 3 446”. Liczby ocen się zgadzają: 3 446 + 3 361 = 6 807; 469 + 44 = 513.
- Poprawka: zdjąć znak procenta ze średniej. Odsetek ocen 1–2 zostawić jako procent.

**9. Dwa okna Safari wyglądają jak sprzeczność**
- Waga: ważna jako niejasność, nie błąd rachunku.
- Miejsce: Lejek i Zdarzenia wobec Priorytetów, pozycja 1.
- Co jest nie tak: 66,2% → 45,1% (1 763 i 1 553 sesje, po 60 dni) oraz 66,1% → 45,6% (4 678 sesji po 17.03, okno od 1.10.2025). Oba są w E4, ale karty nie odsyłają do siebie.
- Dowód: E4, sekcja 5f: `66.1 / 45.6`, `4678`, utracone 695 i po odjęciu tła 628.
- Poprawka: przy 66,1/45,6 dopisać „to inne okno niż 60 dni wokół 17.03”. Roczne 1 158–1 281 i 75–83 / 86–95 tys. zł schodzą się z 628–695, 365/198 i marżą 64,6 / 74,3 zł. Tych marż jednostkowych w E nie ma.

**10. Strzałka 180 dni w tabeli kohort**
- Waga: drobna.
- Miejsce: Kohorty, wiersz „Wszyscy w filtrze”, kolumna powrotu w 180 dniach; ta sama liczba w „Czy to wzrost” i w E2.
- Co jest nie tak: tabela pokazuje ▼5,2 przy 27,5% i 22,2%. Różnica wynosi 5,3 pkt.
- Dowód: E2, `powrot_zmiana_pkt` dla 180 dni = −5,3; zakładka „Czy to wzrost”: „−5,3 pkt proc.”
- Poprawka: ▼5,3. Reszta strzałek w tym wierszu (3,2 / 5,4 / 6,5 oraz marże 8,3 i 7,8) jest zgodna z E2.

**11. Rozjazdy o 1 zł i o 1 zamówienie**
- Waga: drobna.
- Miejsce: E2 sekcja 5, W3, założenie 21; Lejek wobec zamówień; „Po zakupie”, wiersz „Razem” zwrotów.
- Co jest nie tak:
  - przychód po zwrotach: W3 i narzędzie w milionach opierają się na 2 230 266 i 3 228 342; założenie 21 ma 2 230 267; E2: 1 490 983 + 739 283 = 2 230 266, ale 2 075 848 + 1 152 495 = 3 228 343;
  - suma miesięcy „przychód pierwszych zamówień” okresu 2 = 2 075 847, wiersz okresu = 2 075 848;
  - lejek: 24 717 i 38 490 płatności wobec 24 716 i 38 491 zamówień; w kwartałach to samo ±1 (III kw. 2025: 6 317 wobec 6 316; IV kw. 2025: 8 104 wobec 8 105);
  - zwroty okresu 1: 23 637 + 9 276 + 11 438 + 1 534 = 45 885, wiersz razem 45 884.
- Poprawka: jedna definicja złotówki i jedno zdanie, czemu płatność sesji może różnić się od zamówienia o 1. Na wniosek to nie wpływa.

**12. Drobne zaokrąglenia, które brzmią mocniej niż liczba**
- Waga: drobna.
- Miejsce: README i „Czy to wzrost”; zastrzeżenie 3; Priorytety, pozycja 11 wobec `ZNALEZISKA.md`.
- Co jest nie tak: 7 268 / 24 687 = 29,4%, a README mówi „prawie jedna trzecia (29%)”. Wydatki: 649 675 / 367 632 − 1 = 76,7%, zastrzeżenie mówi „o 77%”. Górna granica kliknięć: notatki 50 494 zł wydatków, priorytet „do 52 tys. zł” bez wzoru (1 434 × 36,3 zł ≈ 52,1 tys. zł marży, jeśli tak liczone).
- Poprawka: 29,4%; 76,7%; przy 52 tys. zł napisać, czy to marża, czy wydatek.

## 2. Co się potwierdziło

Sprawdzone i zgodne między B, C, D i E:

- Nowi pacjenci: 16 231 → 24 687 = +52,1%. Bez nowych kampanii: 17 419 (+7,3%) i 19 500 (+20,1%). Bezpłatne: 7 069 → 7 924 = +12,1%. Udział nowych kampanii: 7 268 / 24 687 = 29,4%.
- Powrót na tych samych dniach: 30 dni 11,0% (14 984) → 7,8% (22 646); 60 dni 19,1% (13 941) → 13,7% (20 823); 90 dni 23,9% (12 867) → 17,4% (18 924). Liczby osób: 3 076 i 3 289, +6,9%. Końce okien 31.08, 1.08, 2.07 i 3.04 są zgodne z końcem danych 30.09.2026.
- Bez nowych kampanii, 90 dni: 22,0% (14 031) i 20,4% (15 414). Same nowe kampanie: 4,1% (4 893). Rozkład spadku 4,6 i 1,9–2,0 pkt oraz 3,0 i 3,5 pkt jest opisowy i rachunkowo trzyma się tych odsetków. „71%” i „46%” to 4,6/6,5 i 3,0/6,5.
- Marża na pacjenta, 90 dni: 66,6 → 58,3 zł; bez nowych kampanii 66,0 i 63,3 zł; nowe kampanie 36,3 zł. 180 dni: 75,5 → 67,7 zł.
- Mostek dashboardu: surowe +51,9% / +60,7% / +50,3% / +40,3%; bez duplikatów zamówienia +58,3% i przychód +48,1%; po testach +52,1%, +55,7%, +47,7%; po zwrotach +44,8%. Duplikaty 604 i testy 553 + 1 518 = 2 071 schodzą się z różnicami 25 269 → 24 716 i 40 009 → 38 491.
- Marża roczna: 828 085 → 1 048 069 zł = +26,6%. Po odjęciu 152 960 zł: 895 109 zł = +8,1%. Po dalszym odjęciu 41 474 zł: 853 635 zł = +3,1%. Składniki okresu 2: 3 228 342 + 219 652 − 1 734 825 − 649 675 − 15 425 = 1 048 069.
- Kwartały: +71,4%, +43,0%, +13,0%, −6,8%. Wydatki 1,30 / 1,66 / 2,04 / 2,08. III kw.: 207 713 wobec 222 824; przed kampaniami +78 963 zł, wydatki +94 124 zł. Lipiec 2026 nadal wyżej (73 384 wobec 66 832), sierpień i wrzesień niżej. Bez TelemediGO −4,9%. Miesiące sumują się do kwartałów i do 38 491 / 24 687.
- TelemediGO: 1 759 → 2 468 = +709 = +40,3%. Typy 905/1 089, 629/918, 225/461. Opłata 156 551 wobec zniżki efektywnej 183 939 = −27 388 zł = −15,57 zł. Odnowienia 62/1 140 = 5,4%. Cennik i marże po zniżce zgadzają się z E7 co do złotówki. 7 363 × 10 zł = 73 630; przy 1 425 wizytach ze zniżką 20% zostaje 70 780 zł.
- Lejek: 24 717 / 154 085 = 16,0%; 38 490 / 280 625 = 13,7%. Przeglądarki w aplikacjach: 10,7% → 35,6%. Efekt struktury −3,00 pkt, efekt konwersji +0,67 pkt. Suma przeglądarek = 154 085 i 280 625. Sesje zalogowane: 8 026 + 14 042 = 22 068, termin 112, płatności 0. Samo GO: 225 + 461 = 686, czyli 69% z 992.
- Safari: 628–695 w 198 dniach, 95–105 na 30 dni. Tydzień to 3,5% (22–25 zamówień). Koszt testów: 1 518 × 25 = 37 950; 2 071 × 25 = 51 775.
- Ekonomia z E6: nowe kampanie +3,6 / −9,4 zł (90 dni) i +7,0 / −5,2 zł (180 dni). TikTok ujemny w obu regułach. `gs_generic_specjalisci` ujemny w obu regułach i oknach (−23,7 / −44,7 oraz −14,3 / −36,6). Próg 85% dla Meta: 179,6 / (179,6 + 30,6) = 85,4%; 179,6 / (179,6 + 32,9) = 84,5%. Tabela „50% pacjentów dodatkowych” jest średnią wariantów 0% i 100%.
- Punkt procentowy powrotu: 24 687 × 1% × 95,6 zł = 23,6 tys. zł; 17 419 × 1% × 95,6 = 16,7 tys. zł.
- Opóźnienia przy tym samym ruchu: +26,4 pkt to średnia ważona liczbą wizyt w pięciu wspólnych przedziałach (9 979 wizyt). 5 895 + 5 080 = 10 975 odbytych L4. Zamówienia powtórne 8 485 + 5 289 + 8 515 = 22 289.
- Definicje 16–27, 33–34 i 39–40 są nazwane i stosowane konsekwentnie: nowy pacjent, powrót bez anulowanych, przychód po zwrotach, koszt lekarza także za wizytę zwróconą, pediatra 100 zł jako założenie, dwie reguły źródła, porównanie na tych samych dniach.

Wniosek główny jest oparty na danych, nie na przeskoku: więcej pacjentów tak, lepsza retencja nie, także po wyjęciu nowych kampanii, choć wtedy spadek jest dużo mniejszy. Q3 2026 jest policzony, nie dopowiedziany. Zdanie, że to opis, nie przyczyna, jest uczciwe.

## 3. Ocena z perspektywy zlecającego

**Trzy najmocniejsze strony**

1. Odpowiedź jest wprost na definicję z zadania i od razu rozbiera dashboard: duplikaty, testy, zwroty, start od zera. Mostek +61% → +55,7% i +50% → +44,8% da się przeliczyć.
2. Zdarzenia są znalezione w danych, z datą i sprawdzeniem, czy to nie sam skład ruchu. Safari od 17.03.2026, starty 3.11.2025, 9.02.2026 i 8.09.2025 oraz poranne opóźnienia przy tym samym ruchu to jest ta umiejętność, o którą chodziło w kohortach.
3. Priorytety mają wartość, pomiar i czas, a przy słabych kampaniach obie drogi. Dwie reguły źródła są pokazane obok siebie, a nie schowane w przypisie. Niewiadome są podpięte pod pozycje listy.

**Trzy najsłabsze**

1. Kilka zdań jest pewniejszych niż własne liczby: TikTok „do zera”, „wysoka pewność znaku” przy przedziale przez zero, „odsetek TelemediGO nie rośnie”, „w całości”.
2. Część kwot, na których opiera się kolejność, nie jest policzalna z tekstu narzędzia (65,2 tys., 14–21 tys., scenariusze pauzy spoza E6). Tabela ekonomii pozwala odjąć zły koszt od marży 180 dni.
3. Pierwsze czytanie jest za gęste. Ten sam fakt ma dwa okna (Safari, L4, opóźnienia „wszyscy” wobec „spoza nowych kampanii”) bez zdania, które je godzi. Ocena jako procent psuje zaufanie do narzędzia, na którym miałoby się prowadzić biznes.

**Czego brakuje wobec zadania**

- Działającego linku. Kohorty dzienne, lejek, priorytety i lista niewiadomych w tekście narzędzia są. Wymaganie „otwiera się z linku” na dziś nie jest spełnione.
- W rozkładzie struktury i zachowania nie widać wieku, płci ani regionu, choć te pola są w `users.csv`. „Sprawdzone cechy nie tłumaczą spadku” nie obejmuje cech, które mogłyby tłumaczyć jednorazowe L4.
- Test województw nie ma mocy, progu przenikania reklamy ogólnopolskiej ani pokazanej pary województw. Jest próg 85% i zakaz przesuwania budżetu. To za mało, żeby uznać projekt testu za domknięty.
- Krzywa do dnia 270 (0,89 w E2, 5 137 pacjentów) może wyglądać jak nadrabianie. Notatki mówią, że to tylko najstarsze kohorty. Tego zastrzeżenia nie ma przy wykresie.

**Decyzja**

Nadaje się. Zaprosiłbym na rozmowę i nie odrzucałbym za znalezione rozjazdy. Rdzeń jest rzadszy niż typowe zadanie z AI: definicje przed liczbowaniem, dashboard odtworzony co do wariantu, zdarzenia z danych, wnioski cofane tam, gdzie dane nie rozstrzygają.

Przed wysłaniem do firmy: link, poprawka karty TikToka, doprecyzowanie 14–21 i 65,2, jedna liczba L4, koszt 180 dni i znak procenta przy ocenie. Bez tego paczka wygląda na niedomkniętą, mimo że wniosek jest dobry. Na rozmowie pytałbym tylko o jedną rzecz: co kandydat zrobi w pierwszym tygodniu, jeśli reguła sesji płatności jest bliższa prawdy niż przyjęta reguła. Reszta odpowiedzi już tam jest.
