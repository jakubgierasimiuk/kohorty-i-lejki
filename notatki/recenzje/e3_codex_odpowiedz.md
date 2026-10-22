# E3 — recenzja Codeksa (Sol, profil `-p review`) trzeciej listy poprawek: co przyjęliśmy (2026-10-22)

Polecenie: `notatki/recenzje/e3_codex_polecenie.md`. Odpowiedź: `notatki/recenzje/e3_codex.md`.

**Liczby: 9 z 9 pozycji zgodnych.** Codex przeliczył własnym kodem punkty 1–8 z `analiza/e_poprawki.py`, punkt 3 (osoby, które jeszcze nie kupowały, bez nowych kampanii według pierwszego wejścia i według sesji; sesje powrotne osób nowych kampanii, 11 577 sesji i 2 081 płatności; Safari na iPhone'ach i pozostałe przeglądarki z krokiem konta; rozkład zmiany; przedziały), i potwierdził w raportach zmianę wydatków w tabeli kwartałów (+29,6%, +66,4%, +104,0%, +107,7%). Błędu w liczbach nie znalazł. Uwagi dotyczyły brzmienia i zakresu porównań.

## Przyjęte

- a. Tytuł karty lejka był za mocny przyczynowo („z dwóch powodów”). Teraz: „Na spadek konwersji nowych osób składają się głównie dwie rzeczy: więcej ruchu z nowych kampanii na L4 i awaria zakładania konta w Safari”. To język rozkładu (obie rzeczy razem to 2,62 z 2,71 punktu procentowego spadku, IV–IX 2026), a nie twierdzenie o wyłącznych przyczynach. Nie wzięliśmy brzmienia „wiąże się głównie”, bo zasada pisania Kuby każe pisać wniosek bez asekuracji, a nagłówek ma nazwać awarię Safari wprost.
- b i f. „Tylko w Safari” i „konwersja się nie zmieniła” były za mocne. Teraz: „wyraźnie płacą rzadziej tylko sesje w Safari na iPhone'ach” i „w innych przeglądarkach konwersja jest bez istotnej zmiany” (zasada projektu: przedział przez zero = „bez istotnej zmiany”). Tak samo w README. Liczby w widocznym zdaniu zostają zaokrąglone (8% i 12%), dokładne są w szczegółach.
- c. „O połowę rzadziej” liczymy teraz na tych samych miesiącach co „od kwietnia”: sesje z reklam nowych kampanii płacą w IV–IX 2026 5,30% (66 725 sesji) wobec 10,26% pozostałych nowych osób; szczegóły podają obie wersje (cały rok 5,5%). Kontrola w kodzie sprawdza iloraz w obu okresach.
- d. Sesje powrotne osób nowych kampanii mają w szczegółach dwa okresy: 11 577 sesji (18,0%) w całych ostatnich 12 miesiącach i 8 236 sesji (17,6%) od kwietnia do września 2026.
- Uwaga 1. „Cały spadek przypada na krok konta” zastąpione przez „Pogorszenie skupia się na kroku konta; pozostałe kroki w Safari prawie się nie zmieniają” (krok konta ×0,682, płatność po koncie ×0,982, wybór terminu ×1,030). W widocznym zdaniu: „Spadek skupia się na kroku zakładania konta”.
- Uwaga 2. Źródła kart: nagłówek lejka wskazuje `e_poprawki.txt` (punkty 1 i 3), karta Safari dostała `e_poprawki.txt` (punkt 3).
- g. Wrażliwość reguły łączenia osób (Codex jej nie dokończył): policzyliśmy ją w `analiza/e_poprawki.py`, punkt 3. Najgroźniejszy błąd tożsamości to osoba z reklamy L4, która wróciła w innej przeglądarce bez logowania i trafia do „pozostałych”. Bez wszystkich osób, których pierwsze zamówienie to L4, w obu latach, Safari spada o 2,81 punktu (przedział od −3,48 do −2,15), a pozostałe przeglądarki są bez istotnej zmiany (−0,05 punktu, od −0,39 do +0,29). Wniosek się nie zmienia. Zdanie o tym sprawdzeniu jest w szczegółach karty. Tych trzech liczb Codex nie przeliczał.

## Odrzucone

- e. Karta Safari: „Od kwietnia 2026 to prawie cały spadek konwersji nowych osób spoza nowych kampanii na L4” zostaje bez liczby „86%”. Codex uznał brzmienie za uzasadnione opisowo; dokładny rozkład (Safari −0,74 z −0,86 punktu, podział opisowy) stoi w szczegółach karty nagłówka, a karta Safari ma zostać krótka.

## Kontrola po poprawkach

`python -I analiza/b_eksport.py`: 0 różnic w 104 kontrolach, 0 liczb bez pokrycia w szkicach. Zdania karty nagłówka lejka (bez tabel) mają pokrycie w `notatki/e_teksty.md` także bez listy liczb dodanych z tabel.
