Jesteś niezależnym recenzentem liczb w projekcie analitycznym (zadanie rekrutacyjne, dane syntetyczne). Pracujesz tylko do odczytu. Odpowiadasz po polsku, krótko i konkretnie.

KONTEKST
- Folder projektu: bieżący katalog. Baza DuckDB: analiza/telemedi.duckdb (schemat `czyste` = dane oczyszczone; otwieraj read_only=True). Python: `python -I`.
- Przyjęte definicje są w analiza/definicje.py (nowy pacjent = pierwsze opłacone zamówienie, dowolny status; powrót = kolejne zamówienie nieanulowane; źródło Z1K = pierwsze wejście pacjenta z anonimowymi sesjami jego przeglądarek, kod kampanii na pierwszym zamówieniu rozstrzyga — na stronie „według pierwszego wejścia”; Z2 = sesja płatności — na stronie „według sesji z płatnością”). Okres 1 = 1.10.2024–30.09.2025, okres 2 = 1.10.2025–30.09.2026, czas polski. Nowe kampanie = meta_prosp_l4_szybko i tt_prosp_l4_15min.
- Ta runda to druga lista poprawek tekstów (język i spójność). Nowe liczby liczy analiza/e_poprawki.py → analiza/wyniki/e_poprawki.txt i .json. Pozostałe liczby niżej pochodzą z istniejących raportów (analiza/wyniki/a5e_scenariusze.txt, d_wynik.txt, a5r_punktualnosc.txt, a5p_zdarzenia.txt, d_kampanie.txt, d_retencja.txt, e_merytoryka.json) i dopiero teraz trafiają na stronę albo trafiają zaokrąglone. Teksty: analiza/e_teksty.py, analiza/e_teksty_zakladki.py, analiza/b2_eksport_c.py; dane strony: narzedzie/dane_strony/*.js.
- Lejek osób, które jeszcze nie kupowały: plik analiza/wyniki/a5p_lejek_dzienny.csv.gz, wiersze typ = 'zwykla', podzial = 'calosc', pacjent = 'nie_kupowal'; kolumny sesje, k1–k5 (k5 = płatność); dzień sesji w czasie polskim.

ZADANIE
Przelicz NIEZALEŻNIE, własnym kodem (nie uruchamiaj e_poprawki.py jako dowodu), punkty 1–2. Punkty 3–9 sprawdź w raportach albo własnym kodem. Dla każdego napisz: zgodne / różnica (Twoja wartość) / nie da się sprawdzić (dlaczego). Potem oceń zdania a–h.

A. Nowe liczby (analiza/e_poprawki.py)
  1. Lejek osób, które jeszcze nie kupowały, sesja do płatności: IV–IX 2026 146 402 sesji, 12 315 płatności, 8,41% (miesiące od 8,11% do 8,87%); IV–IX 2025 65 262 sesji, 7 257 płatności, 11,12% (od 10,76% do 11,50%). Dla porównania III kwartał 2026 8,31%, III kwartał 2025 11,12%; cały okres 2 9,31%, okres 1 11,21%.
  2. Zwroty po odbytej wizycie (status = 'refunded'; wizyta odbyta = 'completed' albo 'refunded') u pacjentów nowych kampanii według Z1K, okres 2 według dnia płatności (created_at): wszystkie cele wizyty 1 044, z tego L4 1 024 (z 5 895 odbytych wizyt L4), e-recepta 10, konsultacja 10, skierowanie 0.

B. Liczby z istniejących raportów, nowe albo zaokrąglone na stronie
  3. TikTok na L4, wynik kampanii po samej nowej kreacji (wariant B z a5e_scenariusze.txt, E2a: uczciwa obietnica odstrasza pacjentów, którzy nie dostaliby L4), kwoty z 234 dni działania: −6 118 zł (Z1K, 90 dni), −27 825 zł (Z2, 90 dni), −7 658 zł (Z1K, 180 dni), −29 365 zł (Z2, 180 dni); na stronie „−6,1 albo −27,8 tys. zł po 90 dniach i −7,7 albo −29,4 tys. zł po 180 dniach, więc kampania dalej traci”. Meta na L4 po samej nowej kreacji: +44 331, −18 990, +46 368, −17 729 zł.
  4. Próg decyzji testu Mety (udział pacjentów, którzy przyszli tylko dzięki kampanii, przy którym wyłączenie przestaje się opłacać, Z1K): dziś 85,4% (90 dni) i 84,5% (180 dni); po samej nowej kreacji 78,7% i 77,9%; po zmianie zasad zwrotów (wariant A) 70,0% i 69,4%. Na stronie: „około 85%, po samej nowej kreacji około 79%, po zmianie zasad zwrotów około 70%”.
  5. Poranne opóźnienia u internisty (termin 6:00–11:59, wizyty odbyte, ponad 15 minut po terminie, pacjenci spoza nowych kampanii Z1K, miesiąc terminu): XI 2025 15,7%, XII 2025 29,7%, I 2026 42,6%, II–IX 2026 od 47,3% do 52,7%, X 2024 – X 2025 od 4,7% do 6,9%. Ta wersja zastępuje w pozycji 6 listy priorytetów wcześniejszą serię „wszyscy pacjenci” (15,6%, 29,7%, 41,8%, 48,4–52,6%).
  6. Safari na iOS, krok konta po wyborze terminu u osób, które jeszcze nie kupowały: 66,1% (1.10.2025–16.03.2026) i 45,6% (17.03–30.09.2026, 4 678 sesji z wyborem terminu); w 60 dniach przed awarią i po niej 66,2% (1 763 sesje) i 45,1% (1 553 sesje). Strona wszędzie pokazuje teraz 66% → 46%.
  7. Przeglądarki w aplikacjach wobec zwykłych w tej samej kampanii, okres 2: remarketing Meta −12,2, Google Ads na markę −5,1, wejścia bezpośrednie −4,4 punktu procentowego; na stronie „4–12 punktów procentowych”.
  8. Opóźnienia według godziny terminu (internista, wszyscy pacjenci): poza 5:00–13:59 2,7% (14 898 wizyt) wobec 2,8% (9 563) rok wcześniej; u pozostałych lekarzy rano 3,0% (2 757) wobec 2,8% (1 949); na stronie „około 3% w obu latach”.
  9. Zaokrąglenia w widocznych zdaniach: 26,6% → 27%, 41,5% → 41%, 76,7% → 77%, −6,8% → 7%, +1,1% → 1%, 15,57 zł → około 16 zł, 32,81 i 35,86 zł → około 33 i 36 zł, 66,6 i 58,3 zł → 67 i 58 zł, 22,0% i 23,9% → 22% i 24%, 4,1% → 4%, 44,8% → 45%, 3,16 punktu → około 3 z 22 punktów, 21,9% kont bez zakupu → „ponad co piąte konto”.

ZDANIA DO OCENY (czy wynikają z liczb, czy są za mocne albo za słabe; jeśli trzeba, zaproponuj brzmienie)
  a. Lejek, wniosek: „Wśród osób, które jeszcze nie kupowały, od kwietnia 2026 płaci 8% sesji, a w tych samych miesiącach rok wcześniej płaciło 11%.”
  b. Lejek: „Do stycznia 2026 nowe osoby płaciły prawie tak samo często jak rok wcześniej. W lutym 2026, gdy ruszył TikTok na L4, konwersja zaczęła spadać, a od kwietnia spadek się pogłębił: sesje nowych kampanii na L4 to od tego czasu prawie połowa ruchu nowych osób.” oraz „Sesje nowych kampanii płacą mniej więcej o połowę rzadziej niż pozostałe” (5,49% wobec 11,42%).
  c. Pozycja 9: „Wyłączamy na stałe, jeśli w województwach bez reklamy ubędzie mniej niż około 85% pacjentów, których kampania sobie przypisuje. Po samej nowej kreacji z pozycji 5 ten próg spada do około 79%, a po zmianie zasad zwrotów do około 70%.”
  d. Pozycja 3: „Po samej nowej kreacji (pozycja 5) wynik wynosi −6,1 tys. zł albo −27,8 tys. zł po 90 dniach i −7,7 tys. zł albo −29,4 tys. zł po 180 dniach, więc kampania dalej traci.”
  e. „Z kwartału na kwartał wydatki na kampanie rosną coraz szybciej, a marża przed ich kosztem coraz wolniej” (tabela kwartałów z d_wynik.txt / e_merytoryka.json, kwartaly).
  f. Zasady listy priorytetów: „Potem naprawy, diagnozy i testy, które mają wycenę (5–10). Test Mety (pozycja 9) ma nieznany znak, ale wycenę i największą stawkę, więc stoi w tej grupie. Na końcu dwie pozycje bez wyceny: pozycja 11 ma tylko górną granicę, a pozycja 12 tylko koszt testu.” (Czy kryterium zgadza się z kwotami pozycji 5–12 w c.js, D.C.priorytety.przeglad?)
  g. „Opóźnienia u internisty skupiają się w jednym porannym bloku od 5:00 do 13:59 … a poza tym blokiem tyle samo co rok wcześniej” (godziny 5:00 15,3%, 12:00 22,3%, 13:00 5,6% wobec 2,5%).
  h. Pozycja 5 i „Po zakupie”: „1 024 to zwroty przy samych wizytach L4. Zakładka „Po zakupie” pokazuje 1 044 zwroty po wizycie u pacjentów nowych kampanii, bo liczy wszystkie cele wizyty, także e-receptę i konsultację.”

FORMAT ODPOWIEDZI
1. Tabela: nr | nasza wartość | Twoja wartość | zgodne/różnica/nie sprawdzono | uwaga (jedno zdanie).
2. Zdania a–h: ocena i, jeśli trzeba, poprawione brzmienie.
3. Inne błędy, które zauważyłeś w analiza/e_poprawki.py albo w nowych zdaniach w e_teksty.py (najwyżej 5, od najważniejszego).
Nie zmieniaj żadnych plików.
