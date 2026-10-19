# Recenzja części „pozyskanie” punktu A5 przez Codeksa (model Sol) — podsumowanie

**Kiedy i jak:** 2026-10-19, `codex exec -p review -s read-only --skip-git-repo-check` (model `gpt-6.1-sol`, tylko odczyt). Polecenie: `a5p_codex_prompt.md`. Odpowiedź: `a5p_codex_odpowiedz.md`. Codex liczył wszystko własnym kodem na bazie otwartej tylko do odczytu i nie uruchamiał naszych skryptów.

**Wynik w skrócie:** wszystkie pięć zestawów liczb się potwierdza. Codex znalazł jeden błąd w kodzie, który zmieniał wynik (mianownik w sesjach zalogowanych), i pięć miejsc, w których opis był szerszy niż dane. Wszystko poprawione.

## Co Codex potwierdził

1. Lejek: 16,04% wobec 13,72% sesji zakończonych płatnością, rozkład według przeglądarki −3,00 i +0,67 punktu procentowego.
2. Pierwszy rok: konwersja osób, które jeszcze nie kupowały, stoi; wzrost całości to pacjenci powracający. Rozpoznanie „kupował wcześniej” poprawne.
3. Safari na iOS: data 17.03.2026 (jedyna wskazana przez jego własną segmentację przy karach 15, 25, 50 i 100), spadek z 66,2% do 45,1%, zakładanie kont 1 082 → 668, logowania 659 → 619, szacunek 695 utraconych zamówień.
4. Sesje zalogowane od wejścia: 22 068 sesji, 12 461 pacjentów, 20,7% z wyborem usługi, 2,4% z nich z wyborem terminu, zero anonimowych sesji po pierwszym zakupie, porównanie po punkcie kontrolnym 16,0% wobec 13,2%.
5. Sezon: mnożniki zima / lato 1,37 (bezpłatne), 1,20 (płatne), 1,06 (wydatki), 1,21 (nowi z Google Ads) przy 1,06 (wydatki Google).

## Co poprawiliśmy

| Uwaga Codeksa | Co zrobiliśmy |
|---|---|
| **Błąd w kodzie:** w `a5p_zalogowane.py` (sekcje 3d i 4) średnie pomijały sesje bez późniejszego zamówienia (wartość pusta), co zawyżało odsetki, np. 14,3% zamiast 2,6% zamówień w 7 dni po wejściu z CRM. | Poprawione w trakcie recenzji: brak zamówienia liczymy jako „nigdy”. Notatka po poprawce: po wejściach z CRM zamówienie w 7 dni pada w 2,6–2,8%, czyli tyle co tło. |
| Opis sekcji 4c (tło) mówił o dniach bez sesji zalogowanej, a kod liczył wszystkie dni (0,375 wobec 0,364 zamówienia na 100 pacjento-dni). | Opis poprawiony do tego, co liczy kod; wartość Codeksa podana obok. |
| Zakres miesięczny konwersji nowych odwiedzających w pierwszym roku to 10,8–11,6%, a nie 11,0–11,6% (sierpień 2025). | Poprawione wcześniej w notatce; tabela miesięczna dodana do `a5p_lejek.txt`, sekcja 2c. |
| Grupa porównawcza dla Safari była węższa niż opis: wszystkie inne przeglądarki razem mają 64,8% → 63,4%, a nie 63,8%. | Dodany wiersz „wszystkie poza iOS Safari” w `a5p_zdarzenia.txt`, sekcja 5a; notatka poprawiona. |
| Spadek w Safari na iOS nie występuje „w każdym kanale”: w TikToku 33,3% → 38,5% (9 i 26 sesji). | Notatka: „w każdym kanale poza TikTokiem, gdzie próba jest za mała”. |
| Po odjęciu równoległego pogorszenia w innych przeglądarkach szacunek wynosi około 628 zamówień. | Dodane do `a5p_zdarzenia.txt`, sekcja 5f, jako sprawdzenie wrażliwości (628, czyli 95 na 30 dni). |
| „Meta ze stałym budżetem nie ma sezonu” to za mocne zdanie: 351 wobec 324 nowych pacjentów (+8,3%) przy wydatkach +5,3%. | Dodana sekcja 5c w `a5p_sezon.txt`; notatka: „co najwyżej słaby sezon”. |
| Zimą Google Ads ma 16,0% więcej kliknięć przy wydatkach +6,3%, koszt kliknięcia −8,4%. Część przewagi zimowej to tańszy ruch. | Dodane do `a5p_sezon.txt`, sekcja 5c, i do notatki. |
| Rozkład struktury zależy od wag (symetrycznie −2,88 i +0,56); +0,67 nie jest dowodem poprawy produktu. | Dopisane w notatce jako zastrzeżenie. |
| Przelicznik 90,5% dla powracających jest wysoki częściowo z definicji grupy. | Dopisane przy danych do wariantu pesymistycznego (tylko górna granica). |
| Czasy kroków w zakupach powtórnych mają te same kwantyle, ale nie identyczny rozkład; nie są dowodem prawdziwego logowania. | Sformułowanie w notatce złagodzone. |

## Słabości metody, które zostają (do opisu w narzędziu i na liście niewiadomych)

- Wykrywanie zmian nie widzi epizodów krótszych niż 14 dni i grup z mniej niż 3 000 wejść na krok. Trend albo sezon może się w nim pokazać jako skok. Kara 25 nie daje deklarowanej istotności przy tylu przeszukanych seriach. Dlatego każde zdarzenie sprawdzamy osobno na bazie.
- Porównanie pacjentów z sesjami zalogowanymi od wejścia i bez nich nie usuwa różnicy w zainteresowaniu zakupem.
- Sezonu nie oddzieliliśmy przyczynowo od wydatków: wyświetlenia Google Ads zależą też od budżetu, a kanały bezpłatne mogą reagować na reklamę.
