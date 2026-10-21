# D2 — recenzja Codeksa (model Sol) nowych liczb po konsylium (2026-10-21)

**Polecenie:** `d2_codex_prompt.md`. **Odpowiedź:** `d2_codex_odpowiedz.md`. Uruchomienie: `codex exec -p review -s read-only --skip-git-repo-check -o notatki/recenzje/d2_codex_odpowiedz.md - < notatki/recenzje/d2_codex_prompt.md`, tylko do odczytu, baza z `read_only=True`, liczenie własnym kodem bez importu naszych skryptów `d_*`.

**Werdykt w skrócie:** 34 z 35 sprawdzonych liczb zgodnych co do zaokrąglenia, także przed zaokrągleniem (opóźnienia po godzinach, poranek, powroty według usługi z przedziałami, kolejne zamówienia, wiek, konta bez zakupu, przeglądarki, TikTok po 180 dniach, tempo półrocza, Google Ads na markę, kod rabatowy, rozkład III kwartału w obu regułach, Safari w kwartale, baza powracających, progi Mety, błąd testu po 4 i 6 tygodniach, warianty porannej obsady). Jeden błąd jednostki w tekście. W definicjach trzech skryptów Codex nie znalazł rozbieżności zmieniającej wyniki.

## Uwagi i co z nimi zrobiliśmy

| # | Uwaga Codeksa | Decyzja | Co zmieniliśmy |
|---|---|---|---|
| 1 | Błąd: próg Mety w pacjentach „4 320 rocznie” to liczba z 332 dni działania kampanii | przyjmuję | „około 4 320 nowych pacjentów w 332 dniach działania kampanii (według sesji płatności około 4 360), po naprawie zwrotów A 3 540” — szkic (pozycja 9), założenie 59, znaleziska. Nie przeliczamy na rok, żeby liczba była prosto z raportu (`d_wynik.txt`, 3a) |
| 2 | Błąd metody: „89 tygodni” zakłada, że cały błąd maleje jak 1/√czasu, a szum okresu odniesienia zostaje | przyjmuję | usunięte; zdanie, że dłuższy test wymaga osobnego przeliczenia. Liczba zostaje tylko w raporcie `d_wynik.txt` jako ekstrapolacja |
| 3 | Uzasadnienie reguły „oczekiwaną marżą” nie wynika z liniowości bez modelu rozkładu | przyjmuję | reguła zostaje (oszacowanie punktowe), opisana jako „świadomie przyjęta reguła decyzji przy dużej niepewności, a nie rozstrzygnięcie statystyczne”; do zatwierdzenia przez Kubę |
| 4 | Godzina 13:00 pominięta; „u pozostałych lekarzy nie rosną o żadnej godzinie” nieprawdziwe | przyjmuję | „największy wzrost 5:00–12:59, mniejszy o 13:00 (2,5% → 5,6%)”, „poza 5:00–13:59 prawie taki sam”; u pozostałych lekarzy „rano bez istotnej zmiany (2,8% z 1 949 wobec 3,0% z 2 757)” zamiast zdania o każdej godzinie |
| 5 | Przeglądarki: „cecha ruchu, a nie przeglądarki” przesądza przyczynę; brak różnicy to nie test równoważności | przyjmuję | „nie wykryliśmy niższej konwersji”, „porównanie obserwacyjne nie rozdziela wpływu przeglądarki od cech użytkowników” — szkic, teksty strony, znaleziska, `a5_pozyskanie.md` |
| 6 | „Luka to wydatki, a nie Safari” — rozkład księgowy tego nie rozstrzyga | przyjmuję częściowo | „księgowo lukę wyjaśnia wzrost wydatków starych kampanii, częściowo skompensowany marżą konsultacji; rozkład nie rozdziela wpływu Safari”. Zostaje zdanie Kuby, że Safari się w luce nie mieści, bo szacunek Safari (14,6–18,3 tys. zł) jest większy niż luka (5,0 tys. zł) — to porównanie dwóch kwot, a nie wniosek z rozkładu |
| 7 | Najwcześniejszy poranny termin liczony dla sieci, nie dla lekarza | przyjmuję | „wizyty z najwcześniejszym porannym terminem w danym dniu”, zdanie o sieci i braku danych o lekarzach i grafikach; „liczba wizyt prawie nie zmienia” zastąpione zmierzoną różnicą 4,2 punktu |
| 8 | Testy pozorne to ocena orientacyjna; pary dobrane na całym okresie 2 | przyjmuję | „ocena orientacyjna przy założeniach modelu”, „sam dobór par prawdopodobnie nie wystarczy”, „test może wykryć dużą różnicę”, pary i estymator ustalane przed testem na danych sprzed testu |
| 9 | Zakres Safari 14,6–18,3 tys. zł miesza dwa założenia o tempie strat | przyjmuję | „zależnie od odjęcia tła i założonego tempa strat”; 4,1–4,5 tys. zł jako osobny scenariusz |
| 10 | Brak części liczebności przy odsetkach | przyjmuję | oba mianowniki przy przeglądarkach (Meta na L4 46 091 i 14 901, TikTok 28 160 i 5 310 sesji), liczebności grup wieku, 865–1 858 wizyt w godzinie, mianownik 11 482 i stan na 30.09.2026 przy kontach, 3 680 i 1 379 przy zwrotach z kodem; progi 33,7% i 20,2% nazwane progami rachunku |
| 11 | Karta streszczenia: okresy i ostrożniejsza kwota | przyjmuję | okresy przy liczbie nowych pacjentów, kohorty 1.10–2.07 przy retencji, kwota jako „górny scenariusz odzyskania marży … przed kosztem naprawy” |
| 12 | Kod: przedział przybliżenia rocznika (`d_kampanie.py`, 2b) pomija kowariancję | przyjmuję, bez zmiany kodu | dla TikToka przyrost marży z dni 91–180 wynosi 0 u wszystkich wczesnych pacjentów, więc przedział (−7,4 do −3,4 zł) jest taki sam; przedziału dla Mety nie podajemy w tekstach. Zapisane jako ograniczenie metody |

Żadna uwaga nie zmienia kierunku wniosku ani kolejności listy priorytetów.
