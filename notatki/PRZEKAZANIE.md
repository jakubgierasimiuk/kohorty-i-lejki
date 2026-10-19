# Przekazanie — stan prac dla kolejnej sesji

Zasada z `CLAUDE.md`, punkt 14: każda sesja czyta ten plik na starcie i aktualizuje go na końcu swojej pracy.

**Ostatnia aktualizacja:** 2026-10-19, po zamknięciu punktu A3 (sesja, która prowadziła A1–A3).

## 1. Gdzie jesteśmy

| Punkt | Stan | Commit |
|---|---|---|
| 0 Kontrola bezpieczeństwa | zrobione | `e5897ac` |
| A1 Baza danych | zrobione | `025d6f0` |
| A2 Jakość danych | zrobione, czyszczenie przyjęte przez Kubę | `b7466aa`, `95140a0`, `12a0128` |
| A3 Odtworzenie dashboardu | zrobione, przyjęte przez Kubę | `b91975a` |
| **A4 Definicje (razem z Kubą)** | **następny — robi go nowa sesja** | — |

Status wszystkich punktów: `notatki/PLAN.md`.

## 2. Dane i kod

- **Baza:** `analiza/telemedi.duckdb` (19 MB, poza repozytorium, tak jak `dane/`). Dwa schematy:
  - `surowe` — 17 plików CSV bez czyszczenia, z kolumnami `plik` i `wiersz_w_pliku`; sesje i zdarzenia mają też `started_at_pl` / `event_at_pl` i `dzien_pl` (czas polski);
  - `czyste` — bez 604 zdublowanych kopii zamówień i bez 22 kont testowych (z ich zamówieniami, sesjami i zdarzeniami). **Wszystkie dalsze liczby liczymy na `czyste`.** Tabele `czyste.konta_testowe` i `czyste.przegladarki_testowe` trzymają wyłączone identyfikatory.
- **Odtworzenie bazy od zera:** `python -I analiza/a1_baza.py`, potem `python -I analiza/a2_czyste.py`. Lista wszystkich skryptów i ich wyników: `analiza/README.md`.
- **Uruchamianie:** z głównego folderu projektu, zawsze `python -I` (izolacja od plików w folderach z danymi). DuckDB 1.5.5, pandas 2.3.3, pyarrow — zainstalowane, nic nie trzeba doinstalowywać.
- **Pułapka techniczna:** konsola Windows ma kodowanie cp1250 i przy `python -I` zmienna `PYTHONIOENCODING` nie działa. Znaki spoza cp1250 (np. minus „−”, strzałka „→”) wywracają `print`. W nowym skrypcie na początku `main()` daj `sys.stdout.reconfigure(errors="replace")`. Raporty zapisuj do plików w UTF-8.
- **Wzorzec skryptu:** skrypt tylko czyta bazę (`read_only=True`), pisze raport tekstowy do `analiza/wyniki/<punkt>_<nazwa>.txt`, a w rozmowie pokazuje się tylko to, co potrzebne do decyzji. Każda liczba w notatkach i w rozmowie musi wynikać z kodu w repozytorium.

## 3. Najważniejsze fakty (szczegóły i liczby: `ZNALEZISKA.md`, `ZALOZENIA.md` 1–15, `DECYZJE.md`)

- **Dane oczyszczone:** 63 207 zamówień, 457 464 sesje, 484 228 zdarzeń lejka, 52 400 kont, 4 227 zakupów TelemediGO, 5 676 wierszy kosztów kampanii. Okres: 1.10.2024 – 30.09.2026.
- **Dashboard (A3):** liczony na surowo, czyli z duplikatami, z testami i z przychodem przed zwrotami. Po oczyszczeniu: nowi pacjenci +52,1%, zamówienia +55,7% (dashboard +61%), przychód +47,7% przed zwrotami i +44,8% po zwrotach (dashboard +50%), TelemediGO +40,3%.
- **Czas i powiązania są czyste:** moment płatności w zamówieniu jest co do sekundy równy krokowi `payment_succeeded`. Każde zamówienie i każde TelemediGO ma sesję tego samego konta. Żadna przeglądarka (`visitor_id`) nie jest dzielona przez dwa konta, a 3 835 kont (7,3%) ma więcej niż jedną przeglądarkę.
- **Każda sesja z zamówieniem ma krok logowania** (`account_completed`), także wszystkie 24 338 zakupów powtórnych. Sesje zalogowane od wejścia (konto w sesji, bez kroku logowania): 22 068, żadna nie kończy się zakupem konsultacji. Trzy odczytania i plan pogłębienia: `DECYZJE.md` (2026-10-19, trzy otwarte sprawy) i `PLAN.md` A5.
- **Kody rabatowe** to stała kwota w złotych. L4SZYBKO20, TIKTOK25, RANKING10 i START10 występują tylko na pierwszym zamówieniu, a WRACAM15 tylko na kolejnych (w 100% z `crm_reactivation`). Około 30% pacjentów z kodem kampanii płaci w sesji z innego źródła (bezpośrednio, z wyszukiwania marki, z bezpłatnego Google). Liczby: `analiza/wyniki/a2_dyskusja.txt`.
- **Starty kampanii** (kandydaci na zdarzenia w A5): Meta `meta_prosp_l4_szybko` od 3.11.2025 (kod L4SZYBKO20 od 4.11.2025), TikTok `tt_prosp_l4_15min` od 9.02.2026 (TIKTOK25 od 10.02.2026), newsletter `crm_go_upsell` od 8.09.2025.
- **Trop do A5:** zwroty rosną prawie dwa razy szybciej niż sprzedaż (+93,7% rok do roku). Zwroty po odbytej wizycie (status `refunded`) rosną z 492 do 1 626 zamówień.

## 4. Punkt A4 — co obejmuje

Z `PLAN.md` (sekcja A4, z dopiskami po A2). Każdą definicję pokazujemy Kubie w wariantach. Przy każdym wariancie podajemy, ile zmienia w liczbie nowych pacjentów, w powrotach i w strukturze źródeł.

- **Nowy pacjent:** pierwsze opłacone zamówienie konsultacji / pierwsza jakakolwiek płatność, łącznie z samym TelemediGO / pierwsza wizyta, która się odbyła. Czy łączymy konta po przeglądarce — dane pokazują, że żadna przeglądarka nie należy do dwóch kont.
- **Powrót:** kolejne opłacone zamówienie / kolejna odbyta wizyta / czy zakup TelemediGO liczy się jako powrót. Okna 30, 60 i 90 dni.
- **Źródło pozyskania:** pierwsze wejście / sesja płatności / ostatnie oznaczone wejście w oknie przed zakupem. Łączenie anonimowych sesji z kontem przez przeglądarkę. **Kody kampanii jako kontrola każdej reguły** i wariant, w którym kod wskazuje źródło. **Prowizja afiliacyjna** tą samą regułą co źródło, a drugi wariant (po kodzie RANKING10) jedną liczbą obok. Jeśli różnica jest mała, nie poświęcamy temu więcej czasu. Punkt wyjścia: 842 pierwsze zamówienia w sesji z rankingu wobec 595 z kodem RANKING10.
- **Anulacje i zwroty:** czy pacjent z anulowanym pierwszym zamówieniem jest nowym pacjentem, czy anulowany powrót jest powrotem, jak liczymy przychód netto.
- **Do ustalenia przy okazji (`ZALOZENIA.md`, punkt 11):** okno, w którym liczymy powrót pacjenta po kontakcie z newslettera albo SMS-a.
- **Stop:** definicje przyjmujemy razem z Kubą i zapisujemy w `ZALOZENIA.md`, a uzasadnienie wyboru w `DECYZJE.md`.

## 5. Jak pracujemy z Kubą (skrót, pełne zasady w `CLAUDE.md`)

- Przed każdym punktem pytamy, czy idziemy dalej. Claude liczy i pokazuje, a wnioski wyciągamy razem. Niczego nie nazywamy wnioskiem przed akceptacją Kuby.
- **Lekcja z przeglądu A2:** nie przesądzamy przyczyny, gdy w danych widać więcej niż jedno wyjaśnienie. Przykład: wzrost nowych pacjentów od października do stycznia to nie „sezon infekcji”, bo w tym samym czasie rosną wydatki na kampanie. Takie sprawy podajemy jako otwarte, z planem rozdzielenia.
- Pisanie do Kuby: po polsku, pełnymi zdaniami, wnioski przed dowodami, liczby zawsze z jednostką, bazą porównania i okresem, rozwinięte nazwy, bez żargonu narzędzi.
- Przed każdym zatrzymaniem do przeglądu: aktualizacja `PLAN.md`, notatek i commit po polsku na `master` (z linią `Co-Authored-By`), bez rebase, squash i force push.
- Pytamy Kubę przed: instalacją pakietów, rundą konsylium, Codeksem na modelu Astra, publikacją narzędzia, mailem do Telemedi.
- Łączniki claude.ai są wyłączone (sprawdzone 2026-10-19). Serwerów spoza claude.ai (foodango-meta, ga4-analytics, Metabase, slack-workspace2, metricool, scheduled-tasks, microsoft-learn), przeglądarek i sterowania komputerem w tym projekcie nie używamy.

## 6. Otwarte sprawy na później

- **A5:** pogłębienie sesji zalogowanych od wejścia; rozdzielenie sezonu i wydatków; zwroty po wizycie; wykrywanie zdarzeń (w tym starty kampanii z punktu 3); sprawdzenie, czy wnioski o retencji trzymają się bez kohort z października 2024.
- **C (lista niewiadomych):** sesje zalogowane od wejścia (oba odczytania, test, wariant pesymistyczny w marży); koszt lekarza za wizyty testowe (51 775 zł).
- **D:** dokładny przegląd zamówień testowych jeszcze raz (zastrzeżenie Kuby).
