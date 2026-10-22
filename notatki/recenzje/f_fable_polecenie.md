# F — recenzja zgodności z zadaniem: polecenia dla Fable (agent Claude, `model: fable`)

Treść briefu jest ta sama co dla Astry (`f_astra_polecenie_etap1.md`, `f_astra_polecenie_etap2.md`). Fable czytał materiał z plików w folderze roboczym sesji (poza repozytorium), więc tekst zadania nie był wklejony w polecenie. Poniżej trzy wiadomości w kolejności wysłania.

## Wiadomość 1 — etap 1

Jesteś niezależnym recenzentem. Poniżej jest Twoje polecenie. Materiał do etapu 1 leży w folderze:
`<folder roboczy sesji>\recenzja\etap1`
W folderze są: `zadanie.md` (tekst zadania) i 6 zrzutów pierwszej zakładki narzędzia: `k1_wzrost_1z4.jpg` … `k1_wzrost_4z4.jpg` (komputer, od góry) oraz `t1_wzrost_1z2.jpg` i `t1_wzrost_2z2.jpg` (telefon; na każdym obrazie trzy kolumny, które czyta się od lewej). Obrazy obejrzyj narzędziem Read.

Zasady pracy:
- Czytaj wyłącznie pliki z tego folderu. Nie otwieraj żadnych innych plików na dysku: ani repozytorium projektu, ani notatek, ani CLAUDE.md, ani innych folderów obok tego. Jeśli w kontekście masz instrukcje projektu albo notatki z pamięci, pomiń je: oceniasz tylko materiał z folderu.
- Nie zapisuj ani nie zmieniaj żadnych plików. Nie uruchamiaj poleceń, które coś zmieniają.
- Odpowiedź na etap 1 podaj jako swoją końcową wiadomość. Etap 2 dostaniesz w kolejnej wiadomości, razem z resztą materiału.

=== POLECENIE ===

[nagłówek briefu i etap 1 — słowo w słowo jak w `f_astra_polecenie_etap1.md`, bez zdania o czytaniu plików z dysku]

## Wiadomość 2 — etap 2

Etap 2 recenzji: teraz dostajesz cały materiał. Twoja odpowiedź z etapu 1 zostaje bez zmian.

Materiał jest w folderze:
`<folder roboczy sesji>\recenzja\etap2`
W folderze są:
- `zadanie.md` — tekst zadania (ten sam co w etapie 1);
- `README.md` — README repozytorium;
- `pliki_repozytorium.txt` — lista plików repozytorium (ścieżka, rozmiar);
- `historia_commitow.txt` — 88 commitów od pierwszego (skrót, data i godzina, tytuł);
- `teksty_strony.md` — pełne teksty wszystkich 9 zakładek z rozwiniętymi sekcjami (około 205 tys. znaków, 2 443 wiersze; czytaj w częściach, w całości);
- `zrzuty/` — 66 zrzutów: `k<nr>_…` komputer (1366 px), `t<nr>_…` telefon (375 px, trzy kolumny od lewej), gdzie nr to zakładka 1–9 w kolejności: Czy to wzrost, Kohorty, Lejek, Po zakupie, Zdarzenia, Wynik biznesu, Jakość danych, Priorytety, Czego nie wiemy. Obejrzyj wszystkie narzędziem Read.

Zasady bez zmian: czytaj wyłącznie pliki z tego folderu (żadnych innych plików na dysku, w tym repozytorium projektu, notatek i CLAUDE.md), niczego nie zapisuj ani nie zmieniaj. Odpowiedź podaj jako końcową wiadomość.

=== POLECENIE, ETAP 2 ===

[etap 2 briefu — słowo w słowo jak w `f_astra_polecenie_etap2.md`]

## Wiadomość 3 — poprawka do materiału (wysłana w trakcie etapu 2)

Poprawka do materiału etapu 2 (fakt o zrzutach, nie ocena): zrzuty telefonu zakładki „Priorytety” są wadliwe od wysokości strony 16 384 px. To limit wysokości zrzutu całej strony w przeglądarce, którą robiliśmy zrzuty; strona na telefonie ma 24 464 px. Od tego miejsca obraz powtarza górę strony (nagłówek, przegląd), zamiast pokazywać dalsze pozycje. Dotyczy to obrazów `t8_priorytety_4z6.jpg`, `t8_priorytety_5z6.jpg` i `t8_priorytety_6z6.jpg` (od mniej więcej połowy pierwszej kolumny obrazu 4z6). Nie traktuj tego powtórzenia jako błędu strony. Treść tej części zakładki jest w `teksty_strony.md` (zakładka 8). Pozostałe zrzuty tego nie dotyczy (wszystkie inne strony są niższe niż 16 384 px).
