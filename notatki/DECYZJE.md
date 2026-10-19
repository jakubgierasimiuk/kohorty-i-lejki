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

## 2026-10-19 — trzy otwarte sprawy z przeglądu A2

**Decyzja Kuby:** przyjęte wszystkie trzy propozycje, z dopiskami. Założenia: `ZALOZENIA.md`, punkty 10–15. Zmiany w planie: A4 (źródło pozyskania i prowizja), A5 (lejek, komunikacja po zakupie, pułapki), C (lista niewiadomych).

1. **Sesje zalogowane od wejścia.** Osobny wiersz w lejku, newsletter i SMS oceniane na poziomie pacjenta. Dopisek Kuby: wyjaśnienie nadal niepełne. Rozważamy trzy odczytania: zepsuta ścieżka zakupu dla zalogowanych, inny cel wizyty albo sposób pomiaru (krok logowania zapisywany każdemu przy kasie). Pogłębienie w A5: na którym kroku odpadają, z jakich stron i kampanii przychodzą (np. przypomnienie o recepcie), czy kupują potem rzadziej niż podobni pacjenci, czas między wyborem terminu a krokiem logowania. Zepsuta ścieżka uderzałaby wyłącznie w powracających, czyli w retencję. Dlatego na liście niewiadomych będą oba odczytania, test rozstrzygający i wartość wariantu pesymistycznego w marży.
2. **Okres rozruchu.** Zgoda na zmianę w A5: nie wyznaczamy okresu rozruchu kodem START10. Dopisek Kuby: nie przesądzamy, że wzrost od października do stycznia to sezon infekcji, bo w tym samym czasie rosną wydatki na kampanie. Sezon i wydatki rozdzielamy w A5.
3. **Kody rabatowe.** Zgoda. Kody kampanii służą jako kontrola reguł przypisania źródła w A4. Dopisek Kuby: prowizję dla rankingu liczymy tą samą regułą co źródło pozyskania, drugi wariant jedną liczbą obok. Jeśli różnica jest mała, nie poświęcamy temu więcej czasu.

**Korekta po uwadze Kuby:** w rozmowie napisałem, że wzrost liczby nowych pacjentów od października 2024 do stycznia 2025 „pasuje do sezonu infekcji”. To było za szybkie. W tej samej tabeli rosną wydatki na kampanie, więc przyczyna jest otwarta.
