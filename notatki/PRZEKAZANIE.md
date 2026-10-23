# Przekazanie — stan prac dla kolejnej sesji

Zasada z `CLAUDE.md`, punkt 14: każda sesja czyta ten plik na starcie i aktualizuje go na końcu swojej pracy.

**Ostatnia aktualizacja:** 2026-10-23 przed południem, sesja prowadząca `local_e4232e55-24be-46f8-a2c8-d411b47ebc48` (punkt F i publikacja), zamknięta na prośbę Kuby. **Rozwiązanie jest opublikowane** (https://jakubgierasimiuk.github.io/kohorty-i-lejki/, repozytorium https://github.com/jakubgierasimiuk/kohorty-i-lejki). **Następne: nowe wątki Kuby z poprawkami merytorycznymi narzędzia.** Każdy push zmienia publiczną stronę, więc tylko za zgodą Kuby. Wcześniejsze sesje prowadzące: `local_1bf06826` (E, merytoryka, język, wygląd), `local_791c102e` (D, poprawki po konsylium), `local_06eb3146` (A1–A5), `local_ca1efb6a` (C i D do konsylium).

## 1. Gdzie jesteśmy

| Punkt | Stan | Commit |
|---|---|---|
| 0 Kontrola bezpieczeństwa | zrobione | `e5897ac` |
| A1 Baza danych | zrobione | `025d6f0` |
| A2 Jakość danych | zrobione, czyszczenie przyjęte przez Kubę | `b7466aa`, `95140a0`, `12a0128` |
| A3 Odtworzenie dashboardu | zrobione, przyjęte przez Kubę | `b91975a` |
| A4 Definicje (razem z Kubą) | zrobione, definicje przyjęte przez Kubę, recenzja Codeksa (Sol) uwzględniona | commit „A4: definicje przyjęte…” (pierwszy po `78e69a9`) |
| A5 Kohorty, lejek, po zakupie, zdarzenia — część pozyskania | zrobione, przyjęte przez Kubę, scalone we wspólnych notatkach (założenia 28–32) | `9923800`, `0b157c4`, `f240505` |
| A5 — część retencji | zrobione, przyjęte przez Kubę, scalone we wspólnych notatkach (założenia 33–38) | `c5b17ea` … `f8fda6d` |
| A5 — ekonomia kampanii | zrobione, przyjęte przez Kubę, scalone (założenia 39–43) | `d6f63e4` … `7d8a58f` |
| B Narzędzie | trzecia wersja przyjęta przez Kubę 2026-10-20, scalone (założenia 44–46 i 54); publikacja to ostatni, osobny krok, za zgodą Kuby | `b76a7de` … `df4d23c` |
| C TelemediGO, „czy to wzrost”, priorytety, niewiadome | zrobione, przyjęte przez Kubę 2026-10-20, scalone (założenia 47–53); przeniesienie do narzędzia w sesji `local_0ea34a6a` | `bae2920` … (commit „C: lista priorytetów przyjęta…”) |
| D Poprawki po konsylium (lista Kuby `notatki/d_poprawki.md`) | zrobione i przyjęte przez Kubę 2026-10-21; recenzja Codeksa (Sol) uwzględniona (założenia 55–63) | `bfbc5cf`, `ebf37d5`, `b7b55ba`, `1bfa75f`, `3470f54` |

Status wszystkich punktów: `notatki/PLAN.md`.

**Dla nowych wątków z poprawkami (stan na 2026-10-23, zamknięcie sesji publikacji):**
- **Publikacja:** repozytorium publiczne, `origin` = `jakubgierasimiuk/kohorty-i-lejki`, gałąź `master`; workflow `.github/workflows/pages.yml` wdraża stronę przy każdym pushu. **Push tylko za wyraźną zgodą Kuby.** Lokalnie niewypchnięte są commity z notatkami po publikacji (od `c90c0d4`); wejdą z najbliższym pushem.
- **Poprawka tekstu albo liczby:** zmiana w kodzie tekstów (`analiza/e_teksty.py`, `analiza/e_teksty_zakladki.py`, `analiza/b2_eksport_c.py`) i w szkicu kontroli (`notatki/e_teksty.md`, `notatki/e_teksty_zakladki.md`, `notatki/c_szkic.md`); szkic pisany ręcznie, nie z kodu. Nowa liczba = nowy kod w `analiza/` i przejrzenie przez Codeksa (Sol).
- **Kolejność:** commit kodu, potem eksport (`analiza/README.md`: `e_poprawki.py`, `e_wykresy.py`, `b_eksport.py`; osobno `b2_eksport_c.py` i `b2_teksty_strony.py`), żeby stopka strony wskazywała właściwy stan; potem commit danych strony i wyników.
- **Kontrole przed pushem:** eksport 0 różnic i pełne pokrycie w szkicach; `f_wykresy_tekst.py` (Edge, WebKit, Firefox), `f_odnosniki.py`, `e_przegladarka.py` w trybie jasnym i `--ciemny`, `f_publikacja.py`; ponowny zapis rozmów `analiza/f_rozmowy.py` z plikami spoza repozytorium (tekst zadania, lista nazw: folder `poza_repo` w danych Claude Code tego projektu; wzór polecenia i lista kontrolna w `notatki/f_slad_pracy.md`).
- **Po pushu:** `python -I analiza/f_strona_publiczna.py https://jakubgierasimiuk.github.io/kohorty-i-lejki/ <katalog poza repozytorium>` (9 zakładek na komputerze i telefonie, pliki danych, odnośniki po odświeżeniu, `noindex`).
- **Sesje rundy F** (kontrola techniczna, język, poprawki strony, ślad pracy) są zarchiwizowane; ich wyniki są w `notatki/f_*.md`.

**Stan na 2026-10-23 po publikacji:** repozytorium `jakubgierasimiuk/kohorty-i-lejki` publiczne, zdalne `origin`, gałąź `master`, GitHub Pages z workflow `.github/workflows/pages.yml` (środowisko `github-pages` dopuszcza gałęzie `main` i `master`). Ostatni zapis rozmów przed wypchnięciem: commit `8750ca4`; późniejsze rozmowy wejdą do repozytorium dopiero przy kolejnym uruchomieniu `analiza/f_rozmowy.py` i pushu za zgodą Kuby. Wiersze Meta i TikTok w tabeli zdarzeń zostały bez zmian (daty to skoki ruchu, nie budżetu; `DECYZJE.md`).

**Stan na 2026-10-23 po rundzie poprawek F:** strona (sesja A `local_e5cfeeb6`: `2fcd78a`, `27d85fb`, a po przejrzeniu przez Codeksa `a1d4465`, `559ed00`), pasek zakładek (`7bae553`) i ślad pracy (sesja B `local_4102aedd`: `55c0fcb`, za zgodą Kuby) są w repozytorium; README poprawione przez sesję prowadzącą (tabela zdarzeń w opisie „Kohort”, „górny scenariusz” zamiast „największa pewna strata”). Kontrole na ostatecznej wersji bez problemów (`DECYZJE.md`, ostatni wpis). Założenia 83–86. **Przed publikacją:** (1) decyzje Kuby: ścieżka do folderu innego projektu w historii (`911d2ff`) i fragmenty tekstu zadania w repozytorium (warianty A, B, C w `DECYZJE.md`); (2) ponowne uruchomienie `analiza/f_rozmowy.py` tuż przed publikacją, żeby zapis objął ostatnie rozmowy — wzór polecenia w `notatki/f_slad_pracy.md`; tekst zadania i lista nazw spoza projektu leżą poza repozytorium (folder roboczy sesji prowadzącej i wspólny folder notatek sesji); po uruchomieniu: brak linii „UWAGA”, 0 trafień w kategoriach „powinno zniknąć”, tekst zadania tylko w tytule README; (3) nazwa organizacji od Kuby i adres narzędzia w README; (4) zdalne repozytorium, push, widoczność publiczna i GitHub Pages — każda akcja osobno za zgodą Kuby; (5) po publikacji link na iPhonie, iPadzie i telefonie z Androidem; (6) mail do Telemedi tą samą drogą, którą przyszło zadanie.

**Stan na 2026-10-23 (punkt F, ostatnia kontrola przed publikacją):** sesja prowadząca `local_e4232e55` zrobiła z dwiema sesjami (kontrola techniczna `local_ffe2f6b6`, język `local_00805ea0`) trzy części zlecenia Kuby (`notatki/f_kontrola.md`). Wyniki: recenzje Astry i Fable (`notatki/recenzje/f_*`), `notatki/f_techniczna.md` (nowe skrypty `analiza/f_*.py`, wyniki `analiza/wyniki/f_*`), `notatki/f_jezyk.md`. Kuba poprosił o propozycję jednej rundy poprawek przed jakąkolwiek zmianą: `notatki/f_propozycja.md` — **czeka na jego decyzję**; nic na stronie, w tekstach ani w README się nie zmienia. W folderze zostało 6 śledzonych plików odświeżonych eksportem w kontroli technicznej (treść danych bez zmian: tylko godzina, skrót commitu w stopce i szum zmiennoprzecinkowy) — niezacommitowane, pójdą razem z poprawkami. Tekst zadania wyciągnięty z linku leży tylko w folderze roboczym sesji prowadzącej, poza repozytorium (decyzja Kuby). Następny krok: decyzja Kuby, potem runda poprawek (propozycja: sesja A — teksty, eksport, strona; sesja B — ślad pracy i oczyszczony zapis rozmów), komplet kontroli, publikacja i mail, każdy krok za zgodą Kuby.

**Stan na 2026-10-22 po dopracowaniu grafiki:** sesja `local_dc5102f3` (zamknięta przez Kubę) zrobiła etapy 1–4 wyglądu (`6c5c683` … `63ddc3d`, poprawka wykresu powrotu `87b55b2`, opis `notatki/e_grafika.md`), sesja prowadząca etap 5 i pola dla wykresów w eksporcie (`c3bde09`, `83353f8`, `05dc624`; nowy skrypt `analiza/e_wykresy.py` uruchamiany przed eksportem). Kontrole: eksport 115/0, przeglądarka w obu trybach bez błędów, 314 odnośników, 162 porównania wykresów z tabelami bez niezgodności. Następny krok: przegląd Kuby; publikacja i mail tylko za jego zgodą.

**Stan na 2026-10-22 po trzeciej liście Kuby:** cztery poprawki zrobione w commicie `351f556` (sesja wyglądu; `notatki/e_wyglad.md`, punkt 10; założenia 78–82; znaleziska i decyzje z 2026-10-22). Najważniejsze: lejek nowych osób „bez nowych kampanii” liczony według pierwszego wejścia spada przez Safari na iPhone'ach. Kontrole 104/0, Codex (Sol) 9/9. Grafikę dopracowuje z Kubą sesja `local_dc5102f3` (pliki strony w `narzedzie/`). Następny krok: przegląd Kuby; publikacja i mail tylko za jego zgodą.

**Stan na 2026-10-22 po drugiej liście Kuby:** Kuba przejrzał wersję `ccc3c61` i wysłał 15 poprawek do sesji wyglądu; zrobione w commicie `4c594b5` (opis: `notatki/e_wyglad.md`, punkt 9; założenia 71–77; ostatni wpis w `DECYZJE.md`). Kontrole: 104/0 różnic, 0 liczb bez pokrycia, Codex (Sol) 9/9, przeglądarka bez błędów. Nowy skrypt: `analiza/e_poprawki.py` uruchamiany osobno, przed eksportem (raport `wyniki/e_poprawki.txt` i `.json`, z którego czyta `analiza/e_teksty.py`). Następny krok: przegląd Kuby; publikacja i mail tylko za jego zgodą.

**Stan na 2026-10-22 (runda E, przed przeglądem Kuby):**
- **Zlecenie i wynik:** `notatki/e_runda.md` (słowa Kuby, podział pracy, kontrakt danych, wynik części 1 w punkcie 4, postęp i recenzja Codeksa w punkcie 5). Decyzje: `DECYZJE.md`, ostatni wpis; założenia 64–70; znaleziska z 2026-10-21 wieczorem.
- **Kod:** `analiza/e_merytoryka.py` (część 1, raport `wyniki/e_merytoryka.txt` i `.json`); teksty strony w kształcie karty: `analiza/e_teksty.py` (sesja prowadząca) i `analiza/e_teksty_zakladki.py` (agent, przejrzany i poprawiony); oba uruchamia `python -I analiza/b_eksport.py`. Szkice-wzorce kontroli liczb: `notatki/e_teksty.md`, `notatki/e_teksty_zakladki.md` (ten drugi zamrożony, poprawiany ręcznie, generator tylko z `--nadpisz`). Zmiana tekstu = zmiana w kodzie i w szkicu.
- **Strona:** nowy wygląd z sesji `local_61aff6c2` (commit `888ebca`, `notatki/e_wyglad.md`). Kontrola w przeglądarce: `python -I analiza/e_przegladarka.py --wyjscie <katalog>`. Teksty stron: `python -I analiza/b2_teksty_strony.py` → `analiza/wyniki/b_teksty_strony.md`.
- **Stan kontroli:** 104 kontrole, 0 różnic; 80 nowych kart z pokryciem liczb; 9 zakładek przy 1366 i 375 px bez błędów; 296 odnośników działa.
- **Zostaje:** przegląd Kuby; po nim publikacja (repozytorium publiczne, GitHub Pages, adres w README) i mail — każdy krok tylko za zgodą Kuby.

**Stan na 2026-10-21 wieczorem (po poprawkach po konsylium):**
- **Lista Kuby z `notatki/d_poprawki.md` jest zrobiona w całości.** Jak i dlaczego: `DECYZJE.md`, wpis „2026-10-21 — poprawki po konsylium: jak je zrobiliśmy”. Wyniki wątpliwości Kuby: `ZNALEZISKA.md`, sekcja z 2026-10-21.
- **Nowe skrypty:** `analiza/d_retencja.py`, `analiza/d_kampanie.py`, `analiza/d_wynik.py` (każdy tylko czyta bazę; raporty `analiza/wyniki/d_*.txt` i `d_*.json` — z JSON-ów strona odczytuje nowe liczby). `d_wynik.py` liczy testy pozorne testu Mety i trwa dłużej niż pozostałe.
- **Teksty:** zakładki C za `notatki/c_szkic.md` (karta streszczenia, rozkład III kwartału, test Mety, niewiadome 19–22, razem 22), pozostałe zakładki za `notatki/d_teksty_strony.md`.
- **Strona:** sesja narzędzia `local_0ea34a6a-6b84-45c6-87b7-e953f33e3452` zrobiła etap 1 (`bfbc5cf`) i etap 2 (`3470f54`: nowe liczby i brzmienia, poprawki po recenzji Codeksa). Kontrola `python -I analiza/b_eksport.py`: 102 kontrole, 0 różnic; 1 179 liczb w tekstach zakładek C i 245 liczb w pozostałych zakładkach, wszystkie z pokryciem w `c_szkic.md` i `d_teksty_strony.md`. Teksty zakładek: `analiza/wyniki/b_teksty_strony.md`. Szczegóły sesji narzędzia: `notatki/b_narzedzie.md`, sekcja 15.
- **Recenzja Codeksa (Sol):** 34 z 35 liczb zgodnych, jeden błąd jednostki poprawiony, 11 uwag do brzmienia przyjętych (`notatki/recenzje/d2_codex.md`).
- **Decyzja Kuby (2026-10-21):** pakiet przyjęty razem z regułą testu Mety (oszacowanie punktowe); „nie mieści się w luce” usunięte z „Czy to wzrost” (`DECYZJE.md`, ostatni wpis).
- **Przegląd zamówień testowych (zastrzeżenie z A2) zrobiony 2026-10-21:** reguła i traktowanie bez zmian (`analiza/d_testy.py` → `analiza/wyniki/d_testy.txt`; `ZNALEZISKA.md` A2 punkt 2; `DECYZJE.md`, ostatni wpis).
- **Akapit o Safari w „Wyniku biznesu”** przeredagowany na prośbę Kuby: zaczyna się od szacowanego kosztu awarii w III kwartale, bez porównania z „luką”.
- **Zostaje (każdy krok za zgodą Kuby):** publikacja (repozytorium publiczne, GitHub Pages, adres w README) i mail do Telemedi. Z syntezy konsylium nie robiliśmy widoku „wczoraj i ostatnie 7 dni z alarmami” (nie było go na liście Kuby).

**Stan na 2026-10-21 rano (dla nowej sesji prowadzącej):**
- Punkty 0, A1–A5, B (trzy wersje narzędzia) i C są zrobione, przyjęte przez Kubę i scalone we wspólnych notatkach (założenia 1–54).
- **D w toku.**
  - Weryfikacja liczb Codeksem (model Astra) jest zrobiona: `notatki/recenzje/d_astra.md`.
  - README dla Telemedi jest w głównym folderze. Adres narzędzia to jeszcze szablon do uzupełnienia w dniu publikacji.
  - Konsylium końcowej weryfikacji jest zrobione: `notatki/konsylium/d_weryfikacja/synteza.md`. Błędu krytycznego nie ma.
- **Teraz:** poprawki według listy Kuby w `notatki/d_poprawki.md`. Nowa sesja prowadząca sama decyduje, czy podzielić pracę na dwie sesje naraz (kod strony osobno, teksty i liczby osobno). Na końcu Codex (model Sol) przelicza nowe liczby. Publikacji nie robimy. Zatrzymanie u Kuby z gotowym pakietem.
- **Pliki i skrypty:**
  - punkt C: `analiza/c_telemedigo.py`, `analiza/c_priorytety.py`; teksty źródłowe dla strony: `notatki/c_szkic.md` (sekcje 1–4);
  - strona: `narzedzie/`, eksport `python -I analiza/b_eksport.py` (uruchamia też `analiza/b2_eksport_c.py`, kontrola 93 liczb i zgodności każdej liczby z `c_szkic.md`);
  - teksty zakładek do przeglądu: `python -I analiza/b2_teksty_strony.py` → `analiza/wyniki/b_teksty_strony.md`.
- **Sesja narzędzia** `local_0ea34a6a-6b84-45c6-87b7-e953f33e3452` ma kontekst strony. Czeka na zbiorczą listę poprawek i do tego czasu nic nie zmienia. Można jej dać część dotyczącą kodu strony albo uruchomić nową sesję.
- **Pułapki techniczne:**
  - Pliki notatek mają końce linii CRLF.
  - Dłuższe skrypty i wiadomości commitów z polskim tekstem zapisuj narzędziem do plików i uruchamiaj z pliku, bo heredoc w powłoce psuje cudzysłowy i `\n`.
  - Skrypty uruchamiaj przez `python -I`, z `sys.stdout.reconfigure(errors="replace")` w main().

**Stan na 2026-10-20 rano (dla nowej sesji prowadzącej):**
- **A5 ekonomia kampanii:** zrobiona, przyjęta przez Kubę (dopisek: wynik po 180 dniach zawsze obok wyniku po 90 dniach) i scalona we wspólnych notatkach (założenia 39–43). Commity `d6f63e4` … `24ac35d`. **Punkt A5 jest zamknięty w całości.** Rola sesji prowadzącej i wspólne notatki przechodzą do nowej sesji prowadzącej (decyzja Kuby, `DECYZJE.md` 2026-10-20).
- **B szkielet narzędzia:** zbudowany (commit `b76a7de`), plik publikacji GitHub Pages gotowy (`66ce8f8`, nic nie publikuje). Czeka na przegląd Kuby w sesji „B: szkielet narzędzia” (`local_3d5ab14b-1c4c-4fbb-b051-cdffdbeabf1b`), podgląd lokalny pod http://127.0.0.1:8765/. Jej propozycje wpisów będą w `notatki/b_narzedzie.md`. Kohorty dochodzą do narzędzia po zamknięciu A5 (dane retencji: `PLAN.md`, sekcja B).
- **Hosting:** GitHub Pages z repozytorium w neutralnej organizacji (`DECYZJE.md`). Organizację zakłada Kuba i poda nazwę. Każda akcja na GitHubie tylko za zgodą Kuby.
- **C (stan 2026-10-20):** zrobione i przyjęte przez Kubę. Szkic, cztery dopiski, konsylium (9 z 9), ostateczna lista 12 priorytetów i 18 niewiadomych, pięć poprawek spójności: `notatki/c_szkic.md`. Scalone we wspólnych notatkach (założenia 47–53, znaleziska, decyzje). Kod: `analiza/c_telemedigo.py`, `analiza/c_priorytety.py`; recenzja Codeksa (Sol): `notatki/recenzje/c_codex.md`; konsylium: `notatki/konsylium/c_priorytety/synteza.md`.
- **W toku:** sesja „Narzędzie: czy to wzrost, priorytety i niewiadome” (`local_0ea34a6a-6b84-45c6-87b7-e953f33e3452`) przenosi sekcje 1, 3 i 4 szkicu na stronę i zatrzymuje się u Kuby przed próbną publikacją. Sesja prowadząca (`local_ca1efb6a-0cb9-4abb-b08b-9d90f7e7de79`): końcowa weryfikacja liczb Codeksem (Astra) zrobiona, 45 liczb zgodnych, uwagi wprowadzone (`notatki/recenzje/d_astra.md`, commit `8ebd2a4`); README dla Telemedi w głównym folderze (adres narzędzia do uzupełnienia w dniu publikacji). Konsylium końcowej weryfikacji zrobione (`notatki/konsylium/d_weryfikacja/synteza.md`): błędu krytycznego nie ma, lista poprawek czeka na decyzję Kuby; po decyzji sesja narzędzia (`local_0ea34a6a`) poprawia stronę, a sesja prowadząca notatki, README i raporty. Zostaje z punktu D: przegląd zamówień testowych, publikacja i mail — każdy krok za zgodą Kuby. Propozycje sesji narzędzia scala sesja prowadząca.
- Sesje A4, A5 retencja i A5 pozyskanie są zamknięte. Pierwsza sesja projektu (bezpieczeństwo, hosting): `local_20b4afd7-a9cf-430c-a930-9737c9b50eb9`.

**Własność plików w A5 (dwie sesje pracują naraz w tym samym folderze):**
- sesja retencji (zamknięta): `analiza/a5r_*.py`, `analiza/wyniki/a5r_*`, `notatki/a5_retencja.md`, `notatki/recenzje/a5r_*`. Moduł `analiza/definicje.py` od zamknięcia retencji należy do sesji prowadzącej;
- sesja pozyskania: `analiza/a5p_*.py`, `analiza/wyniki/a5p_*`, `notatki/a5_pozyskanie.md`, `notatki/recenzje/a5p_*`;
- sesja punktu B (narzędzie): `narzedzie/`, `analiza/b_eksport.py`, `analiza/wyniki/b_*`, `notatki/b_narzedzie.md` oraz plik publikacji `.github/workflows/pages.yml` (hosting: GitHub Pages, `DECYZJE.md`). Pliki sesji retencji i pozyskania czyta tylko do odczytu;
- wspólne notatki (`ZALOZENIA.md`, `ZNALEZISKA.md`, `DECYZJE.md`, `PLAN.md`, ten plik, `analiza/README.md`) oraz pliki A1–A4 edytuje tylko sesja prowadząca. Propozycje wpisów do nich sesje zapisują we własnych notatkach.

**Warunki techniczne narzędzia do czasu wyboru hostingu:** `DECYZJE.md`, wpis „szkielet narzędzia (punkt B) przed końcem A5”. W skrócie: pliki statyczne, ścieżki względne, kotwice w adresie, dane obok strony (każdy plik poniżej 25 MB), biblioteki w repozytorium w przypiętej wersji, `noindex` i `robots.txt`, podgląd przez `python -m http.server` z folderu `narzedzie/`. Publikacja, zdalne repozytorium i push tylko za zgodą Kuby, za każdym razem.

## 2. Dane i kod

- **Baza:** `analiza/telemedi.duckdb` (poza repozytorium, tak jak `dane/`). Dwa schematy:
  - `surowe` — 17 plików CSV bez czyszczenia; sesje i zdarzenia mają też `started_at_pl` / `event_at_pl` i `dzien_pl` (czas polski);
  - `czyste` — bez 604 zdublowanych kopii zamówień i bez 22 kont testowych. **Wszystkie dalsze liczby liczymy na `czyste`.**
- **Odtworzenie bazy od zera:** `python -I analiza/a1_baza.py`, potem `python -I analiza/a2_czyste.py`. Lista skryptów i wyników: `analiza/README.md`.
- **Uruchamianie:** z głównego folderu projektu, zawsze `python -I`. DuckDB 1.5.5, pandas 2.3.3, pyarrow — zainstalowane.
- **Pułapka techniczna:** konsola Windows ma kodowanie cp1250, a przy `python -I` zmienna `PYTHONIOENCODING` nie działa. W nowym skrypcie na początku `main()` daj `sys.stdout.reconfigure(errors="replace")`. Raporty zapisuj do plików w UTF-8.
- **Wzorzec skryptu:** skrypt tylko czyta bazę (`read_only=True`, tabele tymczasowe działają), pisze raport do `analiza/wyniki/<punkt>_<nazwa>.txt`, a do rozmowy trafia tylko to, co potrzebne do decyzji.
- **A4:** `analiza/a4_definicje.py` (około 4 sekund). Liczy warianty definicji, w sekcji 6 liczby według przyjętych definicji, a w osobnym pliku przykłady pacjentów do ręcznej kontroli. Kod tabel pomocniczych (kohorty, powroty, sesje pacjenta z anonimowymi sesjami przeglądarek, reguły źródła, kontakty z CRM) nadaje się do przeniesienia do A5 — patrz punkt 4.

## 3. Najważniejsze fakty (szczegóły i liczby: `ZNALEZISKA.md`, `ZALOZENIA.md` 1–27, `DECYZJE.md`)

- **Dane oczyszczone:** 63 207 zamówień, 457 464 sesje, 484 228 zdarzeń lejka, 52 400 kont, 4 227 zakupów TelemediGO. Okres: 1.10.2024 – 30.09.2026.
- **Dashboard (A3):** liczony na surowo. Po oczyszczeniu: nowi pacjenci +52,1%, zamówienia +55,7%, przychód +47,7% przed zwrotami i +44,8% po zwrotach, TelemediGO +40,3%.
- **Przyjęte definicje (A4, `ZALOZENIA.md` 16–27):**
  - nowy pacjent = konto z pierwszym opłaconym zamówieniem, bez względu na status; status pierwszego zamówienia to podział kohort;
  - powrót = kolejne zamówienie nieanulowane, w 30, 60 i 90 dniach kalendarzowych, tylko kohorty z pełnym oknem;
  - TelemediGO mierzone osobno, nie jako powrót;
  - przychód z konsultacji po zwrotach (zwrot w dniu płatności), TelemediGO osobno;
  - źródło = pierwsze wejście pacjenta (z anonimowymi sesjami przeglądarek, w których kiedykolwiek był zalogowany), kod kampanii na pierwszym zamówieniu rozstrzyga; przy ekonomii kampanii obok wynik według sesji płatności;
  - prowizja afiliacyjna tą samą regułą: 30 825 zł za dwa lata, obok kod RANKING10: 14 875 zł;
  - okno CRM = 24 godziny od wejścia z newslettera albo SMS-a, na pacjenta, w dowolnej sesji, tylko zamówienia nieanulowane; przy przypisaniu sprzedaży zamówienie idzie do ostatniego wejścia z CRM przed płatnością; obok okno 7 dni;
  - okresy porównujemy na tych samych dniach kalendarzowych, z liczbą pacjentów przy każdym wyniku.
- **Liczby odniesienia według przyjętych definicji** (`analiza/wyniki/a4_definicje.txt`, sekcja 6): 16 231 nowych pacjentów w okresie 1 i 24 687 w okresie 2; powrót w 90 dniach 23,6% i 17,4%, a na tych samych dniach kalendarzowych 23,9% (12 867 pacjentów) i 17,4% (18 924 pacjentów); udział Meta (pozyskanie) w nowych pacjentach 6,3% i 24,9%, TikTok 0% i 8,9%.
- **Tropy do A5 (obserwacje, nie wnioski — `ZNALEZISKA.md`, sekcja A4):** powrót spada we wszystkich wariantach definicji; zmienia się struktura źródeł w stronę kanałów z niskim powrotem, ale powrót Meta (pozyskanie) spada też w obrębie kanału (z 20,7% do 6,7% w 90 dniach); zwroty po wizycie przy pierwszym zamówieniu rosną z 341 do 1 394 i skupiają się w Meta i TikToku; dwie trzecie wejść z CRM to sesje zalogowane od wejścia bez zakupu.
- **Starsze fakty (A2):** każda sesja z zamówieniem ma krok logowania; sesje zalogowane od wejścia nigdy nie kończą się zakupem konsultacji (trzy odczytania w `DECYZJE.md`). Kody rabatowe to stała kwota w złotych. Starty kampanii: Meta `meta_prosp_l4_szybko` od 3.11.2025, TikTok `tt_prosp_l4_15min` od 9.02.2026, newsletter `crm_go_upsell` od 8.09.2025.

## 4. Punkt A5 — co jest potrzebne

Zakres: `PLAN.md`, sekcja A5, z dopiskami po A4. Najważniejsze dla sesji, która go weźmie:

- **Definicje są ustalone i zrecenzowane** (Codex, model Sol: `notatki/recenzje/a4_codex.md`). Nie wymyślamy ich od nowa. Kod przyjętych definicji jest w `analiza/a4_definicje.py`: tabele `koh` (wariant `N1`), `powr` (kolumna `dni_R2`), funkcja `stopy_por()` (porównanie na tych samych dniach kalendarzowych), `ses_pac`, `sp`, `reg`, `zr` (reguła `Z1K`, obok `Z2`), `kontakt` i `po_kontakcie` (zamówienia nieanulowane; `po_kontakcie_wszystkie` z anulowanymi), rozłączne przypisanie do CRM w sekcji 6e. Rozsądnie jest wydzielić je do wspólnego modułu (np. `analiza/definicje.py`) i użyć w A5, zamiast kopiować SQL.
- **Ekonomia kampanii:** według `Z1K`, a obok według `Z2` (sesja płatności). Zmiana znaku wyniku zależnie od reguły oznacza „niepewne”.
- **CRM:** przy ocenie kampanii CRM jedno zamówienie przypisujemy ostatniemu wejściu przed płatnością (`ZALOZENIA.md` 26). Odstępy od wejścia liczymy w UTC.
- **Struktura a zachowanie** (metoda z recenzji Codeksa, `PLAN.md` A5): powrót całej bazy obok powrotu przy stałej strukturze kanałów z okresu 1, potem pierwsza usługa i zniżka; TikTok osobno. Codex policzył własnym kodem 21,29% przy stałej strukturze i 23,72% w okresie 1 bez kohort z października 2024. Te liczby trzeba powtórzyć naszym kodem, zanim trafią do notatek.
- **Sesje zalogowane od wejścia:** dołączyć wejścia z CRM (dopisek Kuby).
- **Pułapki z planu:** start od zera, młode kohorty, sezon a wydatki, struktura pacjentów, kohorty z października 2024.
- **Zwroty po wizycie** i ich związek z kanałem i usługą (L4) — trop z A3 i A4.

## 5. Jak pracujemy z Kubą (skrót, pełne zasady w `CLAUDE.md`)

- Przed każdym punktem pytamy, czy idziemy dalej. Claude liczy i pokazuje, a wnioski wyciągamy razem. Niczego nie nazywamy wnioskiem przed akceptacją Kuby.
- **Lekcja z przeglądu A2:** nie przesądzamy przyczyny, gdy w danych widać więcej niż jedno wyjaśnienie. Takie sprawy podajemy jako otwarte, z planem rozdzielenia.
- Kuba odpowiada chętnie na pytania z gotowymi wariantami i krótką rekomendacją, ale dopisuje własne warunki. Każdy dopisek trzeba zapisać w `DECYZJE.md` i w planie.
- Pisanie do Kuby: po polsku, pełnymi zdaniami, wnioski przed dowodami, liczby zawsze z jednostką, bazą porównania i okresem, rozwinięte nazwy, bez żargonu narzędzi.
- Przed każdym zatrzymaniem do przeglądu: aktualizacja `PLAN.md`, notatek i commit po polsku na `master` (z linią `Co-Authored-By`), bez rebase, squash i force push.
- Pytamy Kubę przed: instalacją pakietów, rundą konsylium, Codeksem na modelu Astra, publikacją narzędzia, mailem do Telemedi.
- **Codex (Sol):** `codex exec -p review -s read-only --skip-git-repo-check -o <plik odpowiedzi> - < <plik polecenia>`, uruchamiany w tle (kilka minut). Polecenie i odpowiedź zapisujemy w `notatki/recenzje/`.
- Łączniki claude.ai są wyłączone (sprawdzone 2026-10-19). Serwerów spoza claude.ai, przeglądarek i sterowania komputerem w tym projekcie nie używamy.

## 6. Otwarte sprawy na później

- **A5:** jak w punkcie 4.
- **C:** lista niewiadomych jest w `notatki/c_szkic.md`, sekcja 4 (16 pozycji). Możliwe uzupełnienie po przeglądzie (sugestia Codeksa): lepsza kontrola samoselekcji TelemediGO — dopasowanie pacjentów z wejściem z `crm_go_upsell` według stażu i historii zamówień.
- **B:** propozycje wpisów z `notatki/b_narzedzie.md` scala sesja prowadząca po zakończeniu przeglądu w sesji B (jej raport przekaże poprzednia sesja prowadząca).
- **D:** dokładny przegląd zamówień testowych jeszcze raz (zastrzeżenie Kuby) — zrobione 2026-10-21, bez zmian.
