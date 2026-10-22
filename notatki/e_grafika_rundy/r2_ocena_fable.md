# Runda 2 — ocena wspólnej wersji v1 (recenzent: Fable)

## 1. Zgoda / sprzeciw (sekcje 1–5)

Z resztą się zgadzam. Sprzeciwy i ryzyka:

- **Kolejność kart (sekcja 3, kohorty i lejek) a sterowanie seriami.** Wykres dzienny ma iść nad tabelę, ale to tabela ma pola wyboru „które wiersze na wykresie”: sterowanie znajdzie się pod rzeczą, którą steruje. Poprawka: wybór serii w legendzie wykresu (chipy z polem wyboru, „+ dodaj” jako lista wartości; tabela tylko odczytem) **albo** tabela zostaje nad wykresem.
- **Lejek: karty napraw po dwóch wykresach.** „Do naprawy” (Safari) i „Do sprawdzenia” to wnioski; wylądują pod drugim ekranem. Poprawka: nagłówek → dwie karty napraw w rzędzie (z hantlem Safari) → filtry → kroki → skład ruchu → dzień po dniu → tabela.
- **Pierwsza zakładka nie może zależeć od `kohorty.js` (1,4 MB).** „Więcej pacjentów” i 180 dni powrotu oznaczone jako P z tego pliku opóźnią pierwsze wyświetlenie strony ocenianej w pierwszych minutach. Poprawka: oba jako E (cztery liczby i jeden wiersz `okna`; eksport już je ma).
- **Tabele 14/20.** Gęste tabele „w podziale” mają 13 px i już obcinają kolumny przy 1366 px. Poprawka: 13 px w tabelach z liczbami, 14 px tylko w tabelach tekstowych (jak dziś).
- **Odnośniki bez stałego podkreślenia.** W listach i chipach dobrze; w tekście ciągłym (decyzje, zdania kart) odnośnik tylko kolorem łamie „nigdy sam kolor”. Poprawka: w akapitach podkreślenie zostaje.
- **Usunięcie `Math.max(320, …)` bez zapasu.** Przy ukrytym elemencie `clientWidth` bywa 0 i uPlot narysuje pusty wykres. Poprawka: `cel.clientWidth || 300`.
- **„Najwyżej 4 serie”** — doprecyzować: 4 w kolorze plus seria odniesienia („Wszyscy w filtrze” / „Razem”) w kolorze tuszu.
- **Liczby liczone w przeglądarce muszą zgadzać się z tekstem.** „Marża przed kosztem kampanii” w `c.js` (IV kw. 2025: 376,0 tys. zł) to marża + wydatki + prowizja (259 375 + 113 089 + 3 525); słupki parami z `wynik.serie` muszą użyć tej samej definicji. Podobnie „udział sesji nowych kampanii” (szczegóły lejka: 10,1% → 45,9%, tylko `nie_kupowal`, sesje zwykłe).

## 2. Głos w R1–R4

- **R1: (b)** — osobna skala na okno, nazwana w legendzie (z zakresem wartości, np. „90 dni: 12–38%”). Zadanie każe widzieć, *kiedy* kohorty zmieniły zachowanie; skala per kolumna właśnie to pokazuje, a wspólna skala (a) zamieniłaby kolumnę 7 dni w jednolitą biel, a 180 dni w jednolity granat, i różnice w czasie by zniknęły. (c) wymaga nazwania „typowej kohorty” (mediana z całego okresu? z roku wcześniej?) — to nowe założenie analityczne, nie decyzja graficzna; można dodać później jako przełącznik po wpisie w `ZALOZENIA.md`.
- **R2: (b)** — pigułki w trzech rzędach plus przycisk „Zakładki ↑” po przewinięciu. Dziewięć zakładek widocznych od razu mówi osobie z telefonem, co dostała (rozpoznawanie zamiast pamiętania); koszt to 110 px raz. (a) chowa strukturę za przyciskiem, (c) chowa zakładki poza krawędzią, czego użytkownicy nie zauważają.
- **R3: (b)** — słowo widoczne w kafelkach, hantlach i pojedynczych etykietach; w gęstych tabelach wartość ze znakiem i strzałka niosą kierunek, a ocenę kolor plus podpowiedź i tekst dla czytników, z jedną linią legendy pod tabelą („zielone = lepiej, czerwone = gorzej”), nie w każdym nagłówku. (a) w tabeli 11 wierszy × 8 etykiet dodałoby ok. 90 słów szumu; (c) zostawia ocenę w samym kolorze bez żadnego nazwania na stronie.
- **R4: (c)** — dwa wykresy liniowe: marża przed kosztem kampanii obok wydatków na kampanie (jedna jednostka, jedna oś), pod nim marża po wszystkich kosztach. To wprost obraz werdyktu („wydatki rosną szybciej niż marża przed ich kosztem”), działa z istniejącym grupowaniem dni / tygodnie / miesiące i nie wymaga ręcznego składania słupków w uPlocie; (a) przy grupowaniu dziennym daje 730 słupków, (b) z osobnymi osiami psuje porównanie wielkości. Ekonomia kampanii: **punkt wyniku względem zera z dwoma symbolami reguł** (wycofuję własne hantle) — decyzję niesie znak wyniku, dwie reguły na jednej linii same pokazują „znak zależy od przypisania”, a hantle z dwiema regułami dawałyby cztery punkty w wierszu; koszt i marża w podpowiedzi i w tabeli w „Szczegółach”.

## 3. Czego brakuje

1. **Mechanizm wyboru serii w legendzie** (chipy z polem wyboru) — warunek przestawienia wykresów nad tabele; bez niego punkt o kolejności jest niewykonalny.
2. **Kontrola zgodności wykresów z tekstem.** Każdy wykres liczony w przeglądarce podpisuje liczby; test strony (`e_przegladarka.py`) powinien czytać etykiety z SVG i legend i porównywać z liczbami w zdaniu tej samej karty (hantle powrotu, schodki mostka, słupki parami, skład sesji). Inaczej zasada „warstwa graficzna nie dopisuje liczb” jest tylko deklaracją.
3. **Dostępność i tryb ciemny nowych SVG jako wymóg, nie opcja:** `role="img"` z `aria-label` równym wnioskowi, kolory wyłącznie z tokenów, obszar dotyku ≥ 44 px dla punktów hantli i znaczników osi; test przy 375 px i w trybie ciemnym dla każdego nowego komponentu.

## 4. Kolejność etapów

Niedobra przy małej ilości czasu: etap 1 to niewidoczne porządki, a najbardziej widoczna wartość (hantle, mostek, słupki parami w „Czy to wzrost”) czeka do etapu 3. Proponuję:

1. **Pół dnia, fundamenty pod dalsze etapy:** tokeny i paleta bez kolorów stanów, stałe kolory bytów, para kolorów okresów, `clientWidth || 300`, typografia, zastrzeżenie bez pudełka. Bez przestawiania kart.
2. **1 dzień, „Czy to wzrost” i wspólne komponenty:** hantle (od razu także w kohortach, Safari, porannym ruchu), schodki mostka (zakładki 1 i 7), słupki parami kwartałów. Pierwsza zakładka gotowa do pokazania.
3. **1 dzień, wykresy dzienne:** legenda z wyborem serii, zdarzenia według obszaru, wyróżnienie serii, podpisy końców linii, wynik względem zera, dwa wykresy wyniku biznesu.
4. **1 dzień, układ i narzędzie codzienne:** kolejność kart (już z legendą-sterowaniem), filtry dwupoziomowe, tabele z przyklejoną kolumną i widokiem na telefon, skład ruchu w czasie, oś zdarzeń z wersją pionową.
5. **Osobno, z eksportem:** TelemediGO, „Więcej pacjentów”, 180 dni, przeglądarki w aplikacjach, godziny, grupy priorytetów.

Każdy etap kończy przebieg `e_przegladarka.py` (1366 i 375 px, tryb jasny i ciemny).
