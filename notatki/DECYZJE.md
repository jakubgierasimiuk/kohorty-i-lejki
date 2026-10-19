# Decyzje

Decyzje podjęte w trakcie pracy (metoda, podziały, narzędzie, hosting) — co wybraliśmy, dlaczego i jakie były alternatywy.

## 2026-10-19 — plan pracy i sposób współpracy

**Decyzja:** pracujemy według planu z `notatki/PLAN.md` (wersja 2, zatwierdzona przez Kubę). Kolejność: wstępna analiza → narzędzie → uzupełnienie analizy → weryfikacja.

**Dlaczego tak:** pierwsza wersja planu zakładała, że Claude wykona całą analizę samodzielnie, a narzędzie zbuduje równolegle z analizą. Kuba ją odrzucił:
- wnioski wyciągamy razem — Claude liczy i pokazuje, po każdym większym kroku jest przegląd, a wnioski weryfikuje konsylium;
- narzędzie dopiero po wspólnym pierwszym etapie analizy, żeby budować je na sprawdzonych definicjach;
- przed rozpoczęciem każdego punktu Kuba decyduje, czy idziemy dalej;
- bez dat w planie.

**Co Kuba dodał do treści planu:** dokładne odtworzenie liczb dashboardu (a nie „mniej więcej”) i zestawienie ich z miarami po oczyszczeniu; rozszerzona kontrola jakości (duplikaty w każdej tabeli osobno, profil zamówień TEST-QA, kliknięcia wobec sesji, czas zamówień wobec czasu płatności); wspólne ustalenie definicji z wariantami przed kohortami; opis obejścia pułapek (start od zera, młode kohorty, sezonowość); analiza tego, co dzieje się po zakupie; wartość priorytetów w marży; stała zasada „najpierw napraw, potem wyłączaj” (dopisana do CLAUDE.md, punkt 9).

**Wykonanie:** osobna sesja Claude Code prowadzi plan punkt po punkcie, w tym samym folderze projektu.

## 2026-10-19 — budowa bazy danych (punkt A1)

**Decyzja:** jedna baza DuckDB `analiza/telemedi.duckdb`, odtwarzana od zera skryptem `python -I analiza/a1_baza.py`. Plik bazy jest poza repozytorium (`.gitignore`), tak jak surowe dane. W repozytorium są skrypt i raport z kontroli.

**Jak zbudowana:**
- Schemat `surowe`: sześć tabel o nazwach jak w słowniku danych (`users`, `sessions`, `events`, `orders`, `go_memberships`, `marketing_spend`). Pliki kwartalne sesji i półroczne zdarzeń są połączone w jedną tabelę.
- Każda kolumna ma typ podany jawnie w skrypcie. Pliki są czytane jako tekst i dopiero potem zamieniane na typy, bez zgadywania. Wartość, której nie da się zamienić, zatrzymuje skrypt z błędem, zamiast po cichu zamienić się w pustą.
- Przy każdym wierszu zostaje plik źródłowy i numer linii w pliku. Będą potrzebne w punkcie A2 do szukania duplikatów na stykach plików kwartalnych i półrocznych.
- Tabela `surowe.pliki`: liczba wierszy, rozmiar i skrót SHA-256 każdego pliku.

**Dlaczego przeliczenie czasu sprawdzamy drugim sposobem (A1):** czas polski liczy DuckDB. Skrypt przelicza ten sam czas jeszcze raz w Pythonie (moduł `zoneinfo`) i porównuje oba wyniki wiersz po wierszu. Wynik: zero różnic w 459 557 sesjach i 494 605 zdarzeniach.

## 2026-10-19 — czyszczenie danych po przeglądzie jakości (punkt A2)

**Decyzja Kuby:** przyjęte obie propozycje z raportu jakości danych (`analiza/wyniki/a2_jakosc.txt`):
- ze zdublowanych zamówień zostaje jedna kopia (604 zamówienia z okna 10–24.06.2026);
- 22 konta testowe są wyłączone ze wszystkiego: zamówień, pacjentów, przychodu, sesji i lejka; kosztu lekarza za testy nie liczymy, wariant z kosztem idzie na listę niewiadomych.

**Zastrzeżenie Kuby:** zamówieniom testowym przyglądamy się jeszcze raz dokładnie na końcu pracy. Dopisane do planu jako pierwszy krok punktu D.

**Jak wykonane:** dane surowe zostają nietknięte w schemacie `surowe`. Oczyszczona kopia powstaje obok, w schemacie `czyste` (skrypt `analiza/a2_czyste.py`). Dzięki temu w A3 da się porównać dashboard liczony na surowo z liczbami po oczyszczeniu, a każdą decyzję o czyszczeniu można cofnąć bez ponownego ładowania danych.

**Otwarte po przeglądzie (czekają na Kubę):** jak czytać sesje zalogowane od wejścia, które nigdy nie kończą się zakupem; jak wyznaczyć okres rozruchu, skoro START10 działa przez całe dwa lata (zmiana w planie, punkt A5); kody rabatowe jako stała kwota w złotych.
