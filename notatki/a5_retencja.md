# A5 — retencja (sesja „A5: retencja”, 2026-10-19)

Notatka robocza sesji retencji. Sesja prowadząca scali stąd wpisy do wspólnych notatek (`ZALOZENIA.md`, `ZNALEZISKA.md`, `DECYZJE.md`, `PLAN.md`, `PRZEKAZANIE.md`, `analiza/README.md`). Tych plików ta sesja nie edytuje.

## Stan

| Krok | Co | Stan |
|---|---|---|
| 1 | Wspólny moduł definicji `analiza/definicje.py` | zrobione, odtwarza sekcję 6 raportu A4 co do znaku |
| 2 | Kohorty dzienne, powroty 30/60/90, zamówienia i marża na pacjenta | w toku |
| 3 | Struktura pacjentów a ich zachowanie, Meta po kampaniach — STOP 1 | do zrobienia |
| 4 | Po zakupie, newsletter i SMS a powroty | do zrobienia |
| 5 | Zdarzenia w seriach — STOP 2 | do zrobienia |

## Krok 1 — wspólny moduł definicji

- `analiza/definicje.py`: przyjęte definicje z A4 jako funkcje, które tworzą tabele tymczasowe na połączeniu tylko do odczytu. `D.polacz()`, potem `D.zbuduj(con)` albo po kolei `zbuduj_podstawy`, `zbuduj_kohorty`, `zbuduj_zrodla`, `zbuduj_crm`.
- Tabele: `zam`, `ses`, `przeg`, `ses_pac`, `koh` (nowy pacjent N1), `powr` (kolumna `dni_R2`), `sp`, `reg`, `zr` (reguły Z1, Z2, Z1K w długim formacie), `zrodlo` (Z1K i Z2 w jednym wierszu na pacjenta), `logow`, `kontakt`, `po_kontakcie_wszystkie`, `po_kontakcie`, `crm_rozl` (rozłączne przypisanie zamówienia do ostatniego wejścia z CRM). Funkcje SQL: `stopy()` i `stopy_por()` (porównanie na tych samych dniach kalendarzowych, z liczbą pacjentów).
- Różnice wobec `a4_definicje.py`: tylko przyjęte warianty (bez N2–N4, R1, R3, R4, Z1b, Z3), więc `koh` i `powr` nie mają kolumny `war`. Parametr `dni_obserwacji` w `zbuduj_crm` (domyślnie 61 jak w A4; do samego okna 24 godzin wystarczy 1).
- Kontrola: `python -I analiza/a5r_kontrola_definicji.py` liczy podpunkty 6a–6e na tabelach modułu i porównuje z `analiza/wyniki/a4_definicje.txt`. Wynik: 53 wiersze, 0 różnic (`analiza/wyniki/a5r_kontrola_definicji.txt`).
- Import w skrypcie uruchamianym przez `python -I`: `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`, potem `import definicje as D` (tryb `-I` nie dodaje folderu skryptu do ścieżki).

## Propozycje wpisów do wspólnych notatek (do scalenia przez sesję prowadzącą)

### `analiza/README.md`
- `python -I analiza/a5r_kontrola_definicji.py` — kontrola wspólnego modułu `analiza/definicje.py` wobec sekcji 6 raportu A4. Wynik: `wyniki/a5r_kontrola_definicji.txt`.

## Dopiski Kuby

(brak)
