# Przekazanie — stan prac dla kolejnej sesji

Zasada z `CLAUDE.md`, punkt 14: każda sesja czyta ten plik na starcie i aktualizuje go na końcu swojej pracy.

**Ostatnia aktualizacja:** 2026-10-20 wieczorem, nowa sesja prowadząca (`local_06eb3146-72e0-461b-a459-034c491fd691`) po szkicu punktu C na poranny przegląd Kuby. Poprzednia sesja prowadząca prowadziła A1–A5 i uruchamiała sesje A4, A5 (retencja, pozyskanie, ekonomia) i B.

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
| B Narzędzie | druga wersja przyjęta przez Kubę 2026-10-20, propozycje scalone (założenia 44–46); sesja B zamknięta; zostają zakładki „Priorytety”, „Czego nie wiemy” i ostateczne „czy to wzrost” po akceptacji C | `b76a7de` … `c9e1621` |
| **C Szkic: TelemediGO, „czy to wzrost”, priorytety, niewiadome** | **szkic gotowy, czeka na poranny przegląd Kuby (2026-10-21); recenzja Codeksa (Sol) uwzględniona** | commit „C: szkic…” (ten wpis) |

Status wszystkich punktów: `notatki/PLAN.md`.

**Stan na 2026-10-20 rano (dla nowej sesji prowadzącej):**
- **A5 ekonomia kampanii:** zrobiona, przyjęta przez Kubę (dopisek: wynik po 180 dniach zawsze obok wyniku po 90 dniach) i scalona we wspólnych notatkach (założenia 39–43). Commity `d6f63e4` … `24ac35d`. **Punkt A5 jest zamknięty w całości.** Rola sesji prowadzącej i wspólne notatki przechodzą do nowej sesji prowadzącej (decyzja Kuby, `DECYZJE.md` 2026-10-20).
- **B szkielet narzędzia:** zbudowany (commit `b76a7de`), plik publikacji GitHub Pages gotowy (`66ce8f8`, nic nie publikuje). Czeka na przegląd Kuby w sesji „B: szkielet narzędzia” (`local_3d5ab14b-1c4c-4fbb-b051-cdffdbeabf1b`), podgląd lokalny pod http://127.0.0.1:8765/. Jej propozycje wpisów będą w `notatki/b_narzedzie.md`. Kohorty dochodzą do narzędzia po zamknięciu A5 (dane retencji: `PLAN.md`, sekcja B).
- **Hosting:** GitHub Pages z repozytorium w neutralnej organizacji (`DECYZJE.md`). Organizację zakłada Kuba i poda nazwę. Każda akcja na GitHubie tylko za zgodą Kuby.
- **C (stan 2026-10-20 po południu):** Kuba przejrzał szkic, przyjął kierunek i dał cztery dopiski (`DECYZJE.md`); wszystkie wprowadzone. Konsylium na liście priorytetów zrobione (9 z 9, 0,49 USD, wynik `notatki/konsylium/c_priorytety/synteza.md`). **Ostateczna lista 12 priorytetów (`c_szkic.md`, sekcja 3) czeka na akceptację Kuby.** Po akceptacji: scalić sekcję 7 szkicu do wspólnych notatek i przekazać sesji B sekcje 1, 3 i 4 do narzędzia. Wcześniejszy opis szkicu: Zawiera propozycję odpowiedzi „czy to wzrost” (sekcja 1), analizę TelemediGO (sekcja 2), listę 10 priorytetów z wartością w marży (sekcja 3), listę 16 niewiadomych (sekcja 4) i propozycje wpisów do wspólnych notatek (sekcja 7, **jeszcze niescalone** — scalamy po przyjęciu przez Kubę). Kod: `analiza/c_telemedigo.py`, `analiza/c_priorytety.py`; wyniki: `analiza/wyniki/c_*`. Recenzja Codeksa (Sol): `notatki/recenzje/c_codex.md`, osiem uwag, wszystkie wprowadzone, liczby zgodne. Brief konsylium: `notatki/konsylium/c_priorytety/brief.md`, **niewysłany** — o rundzie decyduje Kuba rano.
- **Na porannym przeglądzie C Kuba decyduje o:** odpowiedzi „czy to wzrost”, wnioskach z TelemediGO, kolejności listy priorytetów, liście niewiadomych, rundzie konsylium na liście priorytetów. Każdy dopisek → `DECYZJE.md` i `PLAN.md`. Potem: scalenie propozycji z sekcji 7 szkicu, przekazanie gotowej treści sesji B do narzędzia (sekcje „czy to wzrost”, priorytety, niewiadome, TelemediGO), punkt D.
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
- **D:** dokładny przegląd zamówień testowych jeszcze raz (zastrzeżenie Kuby).
