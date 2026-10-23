# F — przejrzenie przez Codeksa (model Sol) po rundzie poprawek: czy nowe i zmienione zdania nie mówią więcej niż dane

**Kiedy i jak:** 2026-10-23, po commitach sesji poprawek strony (`2fcd78a`, `27d85fb`). `codex exec -p review -s read-only` (model `gpt-6.1-sol`), w osobnym katalogu z dwoma plikami: pełne teksty stron po poprawkach (`analiza/wyniki/b_teksty_strony.md` ze stanu `27d85fb`) i różnice wobec stanu sprzed rundy (`a4d52c9`). Polecenie: `f_codex_polecenie.md`, odpowiedź: `f_codex_odpowiedz.md`.

**Wynik:** bez błędów w liczbach. Wszystkie 8 wierszy nowej tabeli „Kohort” zgadza się z kartami źródłowymi (wartość, jednostka, okres, grupa). Zastrzeżenie w karcie „Lepsza retencja”, pierwszy punkt nagłówka „Lejka”, zdania o Safari na równych oknach i sześć zmienionych zdań pierwszej zakładki są w porządku. Trzy zdania są mocniejsze niż dane.

| Uwaga Codeksa | Ocena sesji prowadzącej |
|---|---|
| Tytuł nowej karty „Kohort”: „Kohorty zmieniły się głównie po naszych decyzjach o kampaniach na L4…” — „głównie” razem z „naszymi decyzjami” sugeruje ustaloną przyczynę, a około 71% to opisowy rozkład spadku | **przyjmuję**: nowy tytuł mówi o faktach w kolejności czasu („Po starcie naszych kampanii na L4 rośnie udział pacjentów, którzy rzadko wracają, a awaria Safari obniża wynik”) |
| Wniosek tej karty: „największą pewną stratą jest awaria Safari: 75–83 tys. zł” — kwota z pozycji 1 to górny scenariusz, nie pewna strata | **przyjmuję**: „naprawa awarii Safari to w górnym scenariuszu 75–83 tys. zł marży rocznie”; to samo nadużycie było w README („To największa pewna strata: do 83 tys. zł”) i zostało poprawione tam przez sesję prowadzącą |
| Pozycja 2 priorytetów (dwa miejsca): „wykrycie po tygodniu ograniczyłoby stratę do 22–25 pierwszych zamówień” — samo wykrycie nie zatrzymuje strat, rachunek zakłada też skuteczną naprawę | **przyjmuję**: „Gdyby awarię wykryto i usunięto w ciągu tygodnia, strata wyniosłaby około 22–25 pierwszych zamówień zamiast 628–695” |

Liczby się nie zmieniają. Poprawki brzmienia wprowadza sesja poprawek strony (kod tekstów, szkice, eksport z kontrolą), README sesja prowadząca.
