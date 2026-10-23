# F, poprawka 2: ślad pracy — prompty, ślepe uliczki, poprawki (sesja B, 2026-10-23)

Sesja „F: ślad pracy i zapis rozmów” (`local_4102aedd-1d8f-4480-89ae-f3336b9f767e`), uruchomiona przez sesję prowadzącą `local_e4232e55-24be-46f8-a2c8-d411b47ebc48`. Zlecenie: poprawka 2 z `notatki/f_propozycja.md`, wariant C, razem z lekcjami z pamięci projektu. Decyzja Kuby: „tak, wszystko według rekomendacji, ruszaj z dwiema sesjami”.

**Stan: przyjęte przez Kubę i zacommitowane.** Słowa Kuby (23.10.2026, w tej sesji): „Przejrzałem raport ze skanu i kilka plików z rozmowami. Tak, zapisz rozmowy, lekcje i zmiany w README w repozytorium i zgłoś się do sesji prowadzącej.”

## 1. Co powstało

| Plik | Co jest w środku |
|---|---|
| `README.md` | Nowa sekcja „Jak pracowaliśmy z AI: prompty, ślepe uliczki, poprawki” w miejscu punktu „Ślepe uliczki zostały w historii commitów”: gdzie są prompty i rozmowy oraz 10 historii (co myśleliśmy, co pokazało błąd, co zmieniliśmy, commit, notatka). Do tego poprawka P9 z `notatki/f_jezyk.md` w dwóch miejscach („oba podziały” → „obie reguły przypisania”; „podziałem według sesji z płatnością” → „wynikiem według sesji z płatnością (druga reguła przypisania)”). Na prośbę sesji A (poprawka 3, kolejność decyzji jak na liście priorytetów) w „Co robimy w pierwszym tygodniu” punkty 2 i 3 zamienione miejscami, żeby lista zgadzała się ze stroną: raport z alarmami (pozycja 2) przed pauzą kampanii (pozycje 3 i 4). Reszty README nie ruszałem. |
| `analiza/f_rozmowy.py` | Skrypt, który robi `rozmowy/` i `notatki/lekcje.md`, a na końcu skanuje wynik. Powtarzalny: ten sam stan plików rozmów daje te same pliki. |
| `rozmowy/` | Oczyszczony zapis rozmów z Claude Code: 18 plików rozmów i `README.md` (co jest w środku, czego nie ma i dlaczego, lista rozmów, miejsca historii z README). |
| `notatki/lekcje.md` | 27 lekcji z pamięci projektu w 7 grupach tematycznych, każda z odnośnikiem do rozmowy, w której powstała. |

Każdą z 10 historii sprawdziłem w `DECYZJE.md`, w notatkach punktów i w `git log` (commit, w którym zmiana weszła). Liczby w historiach są tylko te, które stoją w notatkach repozytorium (`DECYZJE.md`, `d_poprawki.md`, `e_runda.md`, `e_teksty_zakladki.md`, `a5_retencja.md`, `recenzje/a5p_codex.md`, `recenzje/a5r_codex2.md`, `recenzje/d_astra.md`, `f_kontrola.md`) albo w README.

## 2. Jak uruchomić ponownie (przed publikacją, żeby dołączyć ostatnią rundę)

```
python -I analiza/f_rozmowy.py --zadanie <tekst zadania> --nazwy <lista nazw spoza projektu> --raport <raport>
```

Wszystkie trzy pliki muszą leżeć poza repozytorium; skrypt odmawia, gdy któryś jest w środku. Tekst zadania i lista nazw nie mogą trafić do repozytorium, dlatego skrypt dostaje je jako argumenty. Gdzie leżą: notatka dla sesji prowadzącej we wspólnym folderze notatek sesji (poza repozytorium). Pliki rozmów skrypt bierze z lokalnego zapisu Claude Code dla tego folderu (sam wylicza ścieżkę), bez podfolderów agentów, wyników narzędzi i pamięci. Ponowne uruchomienie nadpisuje `rozmowy/` i `notatki/lekcje.md`; README repozytorium tylko skanuje.

## 3. Decyzje w skrypcie (do wiadomości Kuby)

1. **Lista dozwolona, jak w zleceniu.** Wiadomości Kuby (wpisy od człowieka, bloki tekstu, bez bloków systemowych), tekstowe odpowiedzi Claude i treść poleceń dla innych sesji i agentów (uruchomienie agenta, uruchomienie albo propozycja sesji, wiadomość do sesji albo agenta). Wiadomości Kuby wysłane w trakcie pracy Claude aplikacja zapisuje jako wpisy innego typu; sprawdziłem, że w tym projekcie nie ma wśród nich ani jednej wiadomości Kuby (są tam tylko powiadomienia), więc nic nie ginie.
2. **Rozmowy wznawiane.** Dwie rozmowy zapisały się w kilku plikach z tą samą początkową częścią („D: poprawki po konsylium” w 2 plikach, „E: nowy wygląd narzędzia” w 3). Łączę je po identyfikatorach wpisów i pokazuję wspólną część raz. Stąd 18 plików na 21 sesji.
3. **Polecenie startowe sesji potomnej** nie jest powtarzane w jej pliku. Na górze stoi odnośnik do tej wiadomości w pliku sesji, która ją uruchomiła. Wiadomości od innych sesji to odnośnik do wiadomości w pliku nadawcy.
4. **Komunikaty aplikacji:** zostały tylko dwa oznaczenia bez treści: „Kuba przerwał odpowiedź” (3 razy) i „rozmowa skrócona automatycznie” (1 raz).
5. **Zostawione celowo:** lokalne adresy podglądu strony (127.0.0.1) oraz nazwy usług „claude.ai” i „Booking.com” jako nazwy łączników, bez adresu strony (obie są w `CLAUDE.md`). Jeśli Kuba woli usunąć i te, to jedna zmiana w skrypcie (`DOZWOLONE_DOMENY`, `RE_LOKALNY`).
6. **Nazwy rozszerzeń aplikacji używanych poza projektem** (6 wystąpień w jednym poleceniu) usuwam osobnym oznaczeniem. Nazwy usług wymienione w `CLAUDE.md` (łączniki do wyłączenia) zostają.
7. **Formatowanie bez zmiany słów:** nagłówki w treści o trzy poziomy niżej (nagłówkami są numery wiadomości), znaczniki HTML jako zwykły tekst, odnośniki do plików projektu i do innych sesji poprawione tak, żeby działały z folderu `rozmowy/`, wklejone bloki Kuby jako cytat z podpisem „Wklejony tekst”.
8. **Poza listą dozwoloną zostały też** pytania z wyborem odpowiedzi, które Claude zadawał Kubie przez narzędzie (4 razy), i podsumowania tur. To wywołania narzędzi; jeśli Kuba chce je w zapisie, trzeba rozszerzyć listę.

## 4. Liczby (uruchomienie przed commitem, 23.10.2026, 09:53)

| Co | Liczba |
|---|---:|
| pliki sesji | 21 |
| pliki rozmów w `rozmowy/` | 18 |
| wiadomości Kuby | 64 (50 060 znaków) |
| odpowiedzi Claude | 797 (345 885 znaków) |
| polecenia i wiadomości do innych sesji i agentów | 114 (253 420 znaków) |
| wszystkie pliki `rozmowy/` razem | 753 240 znaków |
| odnośniki: polecenie startowe od innej sesji / wiadomość od innej sesji | 15 / 70 |
| lekcje w `notatki/lekcje.md` | 27 |

Liczby odpowiedzi Claude rosną z każdym uruchomieniem, dopóki trwają sesje tej rundy.

**Usunięte z zachowanego tekstu (oznaczenie w miejscu fragmentu):**

| Co | Ile |
|---|---:|
| adresy stron (w tym link do strony z zadaniem) | 5 |
| adresy e-mail | 6 |
| ścieżki spoza folderu projektu | 32 |
| nazwy innych projektów | 1 |
| nazwy rozszerzeń aplikacji używanych poza projektem | 6 |
| fragmenty tekstu zadania (8 i więcej słów z rzędu) | 11 |
| ciągi wyglądające na klucz albo hasło | 0 |
| zostawione celowo (punkt 3.5) | 39 |

**Skan gotowych plików (`rozmowy/`, `notatki/lekcje.md`, `README.md`):**
- adresy e-mail, adresy stron, ścieżki spoza projektu, nazwy innych projektów, nazwy rozszerzeń, wzorce kluczy: 0 trafień;
- tekst zadania (8 i więcej słów z rzędu): 1 trafienie, tytuł `README.md` (pytanie z zadania, 8 słów; tego miejsca zlecenie nie obejmuje);
- historie z README bez znalezionego miejsca w rozmowach: 0;
- listy do przejrzenia: 85 trafień — 34 to nazwy usług wymienionych już w `CLAUDE.md`, 31 to trafienia fałszywe („w bok”, „marca–maja”), 20 to ogólne „inne projekty” bez nazwy (część w samych opisach tego zapisu);
- miejsca, które mogą dotyczyć rekrutacji: 140 trafień, prawie wszystkie to „mail do Telemedi”, „ktoś z Telemedi” i „po rekrutacji repozytorium wraca do prywatnych”; żadnych warunków zatrudnienia ani danych kontaktowych (adres e-mail osoby rekrutującej usunięty);
- wiadomości Kuby dłuższe niż 3 000 znaków: 3.

Raport z kontekstem każdego trafienia i każdego usuniętego fragmentu jest poza repozytorium, w folderze roboczym sesji.

## 5. Znaleziska poza zakresem tej poprawki (dla sesji prowadzącej i Kuby)

1. **Tekst zadania jest już w repozytorium.** Ten sam test (8 i więcej słów z rzędu wspólnych z tekstem zadania) na śledzonych plikach: 104 fragmenty w 32 plikach. Najwięcej w `CLAUDE.md` (19 fragmentów, najdłuższy 74 słowa; punkt 5 „dosłownie z zadania” i cytaty w punkcie 2) oraz w briefie i pytaniu konsylium `notatki/konsylium/d_weryfikacja/` (po 23 fragmenty). Pojedyncze fragmenty są też w kodzie, tekstach strony i notatkach (zwykle 8–14 słów, np. cztery liczby dashboardu). Historia commitów zachowa je niezależnie od zmian w plikach.
2. **Historia repozytorium:** adres e-mail osoby rekrutującej we wcześniejszych wersjach `CLAUDE.md` (`DECYZJE.md`, 2026-10-21) i ścieżka do innego projektu Kuby w commicie `911d2ff` (rozmowa „E: dopracowanie wyglądu narzędzia z Kubą”). Zapis rozmów mówi o obu wprost, więc czytelnik wie, gdzie szukać.

## 6. Propozycje wpisów do wspólnych notatek (bez numerów)

- **`DECYZJE.md`, 2026-10-23 — ślad pracy (poprawka 2, wariant C):** README dostaje sekcję „Jak pracowaliśmy z AI: prompty, ślepe uliczki, poprawki” z 10 sprawdzonymi historiami; folder `rozmowy/` z oczyszczonym zapisem rozmów z Claude Code według listy dozwolonej (wiadomości Kuby, odpowiedzi Claude, polecenia dla innych sesji i agentów), bez tekstu zadania, adresów, ścieżek spoza projektu i nazw innych projektów; `notatki/lekcje.md` z pamięci projektu. Skrypt `analiza/f_rozmowy.py`, lista nazw i tekst zadania poza repozytorium. Zostawione celowo: lokalne adresy podglądu i nazwy usług „claude.ai”, „Booking.com”. Commit po przeglądzie Kuby (jego słowa: „Przejrzałem raport ze skanu i kilka plików z rozmowami. Tak, zapisz rozmowy, lekcje i zmiany w README w repozytorium i zgłoś się do sesji prowadzącej.”).
- **`PLAN.md` i `PRZEKAZANIE.md`:** przed publikacją ponownie uruchomić `analiza/f_rozmowy.py`, żeby zapis objął ostatnią rundę; sprawdzić, że skan nadal daje 0 trafień w kategoriach „powinno zniknąć”; nowe rozmowy przejrzeć wyrywkowo.
- **`PRZEKAZANIE.md`, do decyzji Kuby przed publikacją:** tekst zadania w `CLAUDE.md` i w briefie konsylium oraz w historii commitów (punkt 5.1); adres e-mail osoby rekrutującej i ścieżka do innego projektu w historii (punkt 5.2).
- **`ZALOZENIA.md`:** w zapisie rozmów wiadomość Kuby to wpis od człowieka; polecenie startowe sesji potomnej i wiadomości między sesjami pokazujemy raz, w pliku nadawcy, a u odbiorcy odnośnik.
