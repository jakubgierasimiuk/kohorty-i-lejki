Jesteś niezależnym recenzentem liczb w projekcie analitycznym (zadanie rekrutacyjne, dane syntetyczne). Pracujesz tylko do odczytu. Odpowiadasz po polsku, krótko i konkretnie.

KONTEKST
- Folder projektu: bieżący katalog. Baza DuckDB: analiza/telemedi.duckdb (schemat `czyste` = dane oczyszczone; otwieraj read_only=True). Python: `python -I`.
- Przyjęte definicje są w analiza/definicje.py: źródło Z1K = pierwsze wejście pacjenta z anonimowymi sesjami jego przeglądarek, kod kampanii na pierwszym zamówieniu rozstrzyga (na stronie „według pierwszego wejścia”); Z2 = sesja płatności (na stronie „według sesji z płatnością”). Okres 1 = 1.10.2024–30.09.2025, okres 2 = 1.10.2025–30.09.2026, czas polski (dzień sesji = czyste.sessions.dzien_pl). Nowe kampanie = meta_prosp_l4_szybko i tt_prosp_l4_15min.
- Lejek (analiza/a5p_lejek.py): sesje zwykłe (bez zakupu samego TelemediGO i bez sesji zalogowanych od wejścia, czyli z user_id i bez zdarzenia account_completed); „osoba, która jeszcze nie kupowała” = sesja rozpoczęta przed pierwszym zamówieniem konta sesji albo konta przeglądarki (visitor_id), w której konto kiedyś było zalogowane. Kroki: k2 slot_selected, k3 account_completed, k5 payment_succeeded.
- Dotychczas nagłówek lejka mówił: „poza sesjami z nowych kampanii na L4 konwersja się nie zmieniła” (bez sesji, których własny utm_campaign to nowa kampania: 11,21% → 11,42%). Właściciel projektu podejrzewa, że osoby, które pierwszy raz weszły z reklamy L4, a zapłaciły w innej sesji, podbijają tę średnią i przykrywają awarię zakładania konta w Safari na iPhone'ach (od 17.03.2026).
- Nowe liczby liczy analiza/e_poprawki.py, punkt 3 → analiza/wyniki/e_poprawki.txt (punkt 3) i e_poprawki.json (klucze lj_pw_*). Reguła „według pierwszego wejścia” dla osób: osoba = konto (sesje konta i anonimowe sesje jego przeglądarek), a bez konta przeglądarka (visitor_id); pierwsze wejście osoby = utm_campaign jej pierwszej sesji (bez UTM: utm_source_utm_medium albo „bezposrednie”), a gdy osoba ma zamówienie — kampania Z1K z definicje.py. Grupa „bez nowych kampanii według pierwszego wejścia” = sesje zwykłe osób, które jeszcze nie kupowały, bez wszystkich sesji osób, których pierwsze wejście to nowa kampania. Safari na iPhone'ach = os = 'iOS' AND browser = 'Safari' (także iPady).
- Teksty: analiza/e_teksty.py (funkcja karty_lejka), dane strony: narzedzie/dane_strony/podsumowanie.js (D.P.lejek_naglowek.karta), README.md (punkt „Gdzie i od kiedy tracimy pacjentów”).

ZADANIE
Przelicz NIEZALEŻNIE, własnym kodem (nie uruchamiaj e_poprawki.py jako dowodu), punkty 1–8. Punkt 9 sprawdź w raportach (analiza/wyniki/e_merytoryka.json, kwartaly; analiza/wyniki/d_wynik.txt). Dla każdego napisz: zgodne / różnica (Twoja wartość) / nie da się sprawdzić (dlaczego). Potem oceń zdania a–g.

LICZBY
  1. Wszystkie sesje zwykłe osób, które jeszcze nie kupowały: okres 1 144 813 sesji i 16 232 płatności, okres 2 265 264 i 24 686.
  2. Według sesji (bez sesji z utm_campaign nowej kampanii): okres 1 144 813 sesji, 11,21%; okres 2 170 802 sesji, 11,42%; IV–IX 2026 79 677 sesji, 11,02%; IV–IX 2025 65 262 sesji, 11,12%.
  3. Według pierwszego wejścia: okres 2 159 225 sesji, 17 418 płatności, 10,94%; IV–IX 2026 71 441 sesji, 7 328 płatności, 10,26%; IV–IX 2025 65 262 sesji, 7 257 płatności, 11,12%; zmiana −0,86 punktu procentowego (95% przedział w przybliżeniu normalnym od −1,19 do −0,53).
  4. Sesje osób nowych kampanii, których własna kampania nie jest nową kampanią (powroty bezpośrednio, z wyszukiwarki, z innej reklamy), okres 2: 11 577 sesji, 2 081 płatności (17,98%) — tyle samo co pacjentów, których Z1K przypisuje nowym kampaniom, a Z2 innym kanałom. Sesji z utm_campaign nowej kampanii u osób, których pierwsze wejście to inny kanał: 0.
  5. Safari na iPhone'ach w grupie z punktu 3: IV–IX 2026 14 323 sesji, 1 184 płatności, 8,27%, krok konta po wyborze terminu (k3/k2) 45,7% z 3 561 sesji z terminem; IV–IX 2025 12 887 sesji, 1 545 płatności, 11,99%, krok konta 67,0% z 3 112; przed awarią X 2025 – II 2026 12,07% (14 477 sesji) wobec X 2024 – II 2025 12,15% (12 803).
  6. Pozostałe przeglądarki w tej grupie: IV–IX 2026 57 118 sesji, 6 144 płatności, 10,76%, krok konta 65,4%; IV–IX 2025 52 375 sesji, 5 712 płatności, 10,91%, krok konta 66,4%; zmiana −0,15 punktu (od −0,52 do +0,22).
  7. Rozkład zmiany IV–IX 2026 wobec IV–IX 2025, wzór symetryczny (struktura = (u2 − u1)(k1 + k2)/2, w obrębie = (u1 + u2)/2 (k2 − k1); grupa bez sesji w roku wcześniej liczy się w całości do struktury): w grupie z punktu 3 −0,86 = Safari w obrębie −0,74 + pozostałe w obrębie −0,12 + struktura około 0 (+0,03 i −0,03). Wszystkie osoby, które jeszcze nie kupowały (11,12% → 8,41%, −2,71): struktura razem −2,07 (osoby nowych kampanii jako osobna grupa), Safari w obrębie −0,55, pozostałe w obrębie −0,09.
  8. Safari, który krok: iloraz odsetka sesji z płatnością 0,690 = termin/sesje 1,030 × konto/termin 0,682 × płatność/konto 0,982; miesiące: IV 2026 Safari 7,45% (2 912 sesji) wobec 11,13% rok wcześniej, krok konta 43,0% wobec 65,2%; IX 2026 Safari 8,93% (2 364) wobec 12,35%; pozostałe IV 2026 10,72% (11 324) wobec 11,10%, IX 2026 10,47% (9 359) wobec 11,30%.
  9. Tabela kwartałów („Czy to wzrost” i „Wynik biznesu”): wydatki na kampanie rok do roku +29,6%, +66,4%, +104,0%, +107,7% (IV 2025, I, II i III kwartał 2026; 113,1, 170,6, 184,4 i 181,6 tys. zł) zamiast „×1,30, ×1,66, ×2,04, ×2,08”.

ZDANIA DO OCENY (czy wynikają z liczb, czy są za mocne albo za słabe; jeśli trzeba, zaproponuj brzmienie)
  a. Tytuł karty lejka: „Nowe osoby płacą rzadziej z dwóch powodów: więcej ruchu z nowych kampanii na L4 i awaria zakładania konta w Safari”.
  b. „Pozostałe nowe osoby płacą od kwietnia 2026 rzadziej tylko w Safari na iPhone'ach: około 8% sesji wobec 12% rok wcześniej. Spadek przypada na krok zakładania konta, który działa gorzej od 17 marca 2026. W innych przeglądarkach konwersja się nie zmieniła.”
  c. „Od kwietnia to prawie połowa sesji nowych osób, a te sesje płacą o połowę rzadziej niż pozostałe” (sesje z reklam nowych kampanii 5,49% wobec 10,94% w grupie z punktu 3, cały okres 2).
  d. „Licząc według sesji … konwersja pozostałych sesji rośnie z 11,2% do 11,4%, a od kwietnia do września 2026 stoi. Różnica to 11 577 sesji, w których osoby nowych kampanii wracają … Płaci w nich 18,0%. Te sesje podnosiły średnią i przykrywały spadek w Safari.”
  e. Karta Safari: „Od kwietnia 2026 to prawie cały spadek konwersji nowych osób spoza nowych kampanii na L4.”
  f. README: „Poza osobami z nowych kampanii (licząc według pierwszego wejścia, jak w retencji) od kwietnia płaci rzadziej tylko Safari na iPhone'ach: 8% sesji wobec 12% rok wcześniej. W innych przeglądarkach konwersja się nie zmieniła.”
  g. Reguła przypisania osoby, która jeszcze nie kupiła (przeglądarka bez konta = osoba; pierwsza sesja = pierwsze wejście). Czy jest rozsądna i czy jej słabości (np. ta sama osoba w dwóch przeglądarkach bez logowania) mogą odwrócić wniosek z punktów 5–7?

FORMAT ODPOWIEDZI
1. Tabela: nr | nasza wartość | Twoja wartość | zgodne/różnica/nie sprawdzono | uwaga (jedno zdanie).
2. Zdania a–g: ocena i, jeśli trzeba, poprawione brzmienie.
3. Inne błędy, które zauważyłeś w analiza/e_poprawki.py (punkt 3) albo w nowych zdaniach w e_teksty.py (najwyżej 5, od najważniejszego).
Nie zmieniaj żadnych plików.
