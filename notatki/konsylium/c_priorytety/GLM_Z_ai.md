# GLM (Z.ai) — z-ai/glm-5.3

# Ocena konsylium

## Kryterium i kolejność

Kryterium: **pewność × wartość ÷ wysiłek**, z korektą: najpierw wszystko, co naprawia dane i pewne, odwracalne kroki; decyzje nieodwracalne/strategiczne dopiero na czystych danych.

**1. E – Safari/iPhone.** Zawężone do jednej przeglądarki, jednego dnia, we wszystkich kanałach — to niemal na pewno bug, nie zachowanie pacjentów. Wartość wysoka, wdrożenie dni. Robi się od razu.

**2. K – pomiar.** Niska wartość bezpośrednia, ale bez naprawy raportu i rozstrzygnięcia reguły atrybucji nie można podejmować decyzji o F, C, B na twardych liczbach. 1–2 tygodnie. To warunek wstępny, nie pozycja rankingowa per se.

**3. B – wyłączenie TikToka na L4.** Ujemny w obu regułach i obu horyzontach, najgorszy powrót (4%) i marża (36 zł). Wdrożenie 1 dzień, decyzja odwracalna. Nie czekać na naprawę — patrz niżej.

**4. C – Google Ads na specjalistów.** Również ujemny w obu regułach; CPA 58–81 zł przy marży 32–37 zł to wada strukturalna, obniżenie kosztu o 40–60% jest mało realne. Wyłączyć lub zdusić do minimum; nie inwestować tygodni w naprawę kampanii, której ekonomia nie domyka się nawet w optymistycznym wariancie.

**5. I – kliknięcia vs sesje.** Weryfikacja w panelach 1–2 dni, do 52 tys. zł. Tania opcja czystej informacji przed ew. decyzją o naprawie strony.

**6. D – zwroty po wizytach L4.** Wysoka wartość potencjalna (22–57 tys. zł), ale nie znamy przyczyny zwrotów — wycena oparta na „gdyby odsetek spadł" nie mówi, czy da się go sprowadzić do 5,3%. Uwaga: po wyłączeniu TikToka (B) wartość D maleje, bo dotyczy częściowo tych samych pacjentów — B i D się nakładają i nie sumują.

**7. A – program zniżkowy u specjalistów.** Mała pewna kwota (14,7–18,9 tys. zł), szybkie wdrożenie, stały efekt. Bardzo dobry stosunek efektu do wysiłku, po prostu mała skala.

**8. H – zalogowani od wejścia.** Test ręczny 1 dzień, zerowy koszt — robi się przy okazji, choć wartość może być 0 zł. Kilka faktów wskazuje na „sprawdzam konto", więc nie obiecuję tu pieniędzy.

**9. F – Meta na L4.** Znak wyniku zależy od reguły atrybucji, a widełka decyzji (−27,8 do +163,3 tys. zł) jest bezwartościowa bez ustalenia inkrementalności. Test geograficzny ma sens dopiero po K i rozstrzygnięciu reguły. Tu się nie zgadzam z kolejnością kampanii w liście kandydatów — to najmniej dojrzała do decyzji kampania, mimo że TikTok/Google wyglądają gorzej na pierwszy rzut oka.

**10. J – program zniżkowy a powroty.** Test jest drogi i powolny, ale strategicznie kluczowy: średnia zniżka 104,6 zł przekracza opłatę 89 zł, więc program może być strukturalnie nieopłacalny, jeśli nie dokłada wizyt. To pytanie o sens całego produktu „89 zł/rok".

**11. G – opóźnienia poranne.** Wartość 0–65 tys. zł, nieznany koszt obsłady, brak danych o grafikach. Na razie tylko zdobycie danych i diagnoza.

## Błędy i słabe założenia w wycenach

- **E:** założenie „utracony pierwszy zakup = utracony pacjent" zawyża wartość — część osób wróci z innego urządzenia/przeglądarki. Traktować górną granicę (95 tys. zł) jako maksimum, nie oczekiwany.
- **A:** scenariusz +31,4 tys. zł (wszystko po cenie katalogowej) ignoruje spadek popytu i ryzyko rezygnacji z programu (opłata 89 zł bywa opłacana *dlatego*, że zniżka u specjalisty coś daje). Realistyczny jest scenariusz +18,9 tys. zł. Dodatkowo wyceny nie uwzględniają interakcji z przychodem z samych opłat programowych.
- **B, D:** jawne nakładanie się pacjentów — nie wolno ich sumować; suma B+D jest niemożliwa do osiągnięcia.
- **K:** założenie 25 zł za każdą wizytę testową jest wątpliwe — jeśli konta testowe klikały też specjalistów, koszt to 100–200 zł/wizytę i kwota rośnie kilkukrotnie. Trzeba sprawdzić rozkład specjalności.
- **J:** brakuje wyceny samego faktu, że program przyciąga pacjentów już wracających (subsydiowanie ich zniżką 104,6 zł za 89 zł).
- **C:** „naprawa wymaga obniżenia CPA o 40–60%" — to nie naprawa, to przekreślenie ekonomii kanału.

## Naprawiać czy wyłączać kampanie ujemne?

Rozdzielnie: **B i C — wyłączyć natychmiast.** Ujemne w obu regułach atrybucji i obu horyzontach, wyłączenie darmowe (1 dzień) i odwracalne, a naprawa wymaga wiedzy (przyczyna zwrotów) lub kosztów (CPA), których nie mamy. Zatrzymywanie krwawienia wygrywa z optymalizacją. **F — nie wyłączać bez testu**, bo wynik może być dodatni w prawdziwej regule, a koszt błędnego wyłączenia (do −163 tys. zł) jest większy niż koszt 4–6 tygodni testu geograficznego. Zasada: im bardziej znak zależy od nieznanej reguły przypisania i inkrementalności, tym bardziej test zamiast decyzji.

## Czego brakuje na liście

1. **Rozstrzygnięcie reguły atrybucji** jako osobne działanie (np. ankieta „skąd o nas wiesz", ważenie, kalibracja na kampaniach z kodami — one potwierdzają regułę 1 w 97%). Bez tego F, B, C wiszą.
2. **Retencja jako temat własny:** powrót 23,9→17,4% i marża/pacjenta 66,6→58,3 zł to centralny problem biznesu, a lista ma tylko działania na kampaniach. Brakuje sekwencji powrotu / retargetingu / onboarding pacjenta.
3. **Odnowienia programu:** tylko 5% odnawia, program nie odnawia się sam — przypomnienie/auto-renewal przy opłacie 89 zł to potencjalnie duży, tani przychód. To wynika wprost z kontekstu, a nie ma tego na liście.
4. **Zarządzanie budżetem kampanii:** wydatki 368→650 tys. zł (+77%) przy marży +27% i spadającym III kwartale 2026 — potrzeba reguł pacingu i progów rentowności per kampania, zanim pomoże cokolwiek innego.

## Czego nie wiem

- Inkrementalności kampanii L4 i prawdziwej reguły atrybucji — oba stwierdzone w briefie.
- Przyczyn zwrotów po wizytach L4 — wycena D jest warunkowa.
- Kosztu dodatkowej obsłady porannej (G) i rozkładu specjalności wizyt testowych (K).
- Czy program zniżkowy dokłada wizyty — bez testu J nie rozstrzygnięcie.
- Czasów wdrożeń w realnym zespole — wszystkie szacunki z briefu traktuję jako niezweryfikowane.
