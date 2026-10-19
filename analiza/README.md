# Analiza — kolejność uruchamiania

Wszystkie skrypty uruchamiamy z głównego folderu projektu. Wymagają rozpakowanych danych w `dane/` (poza repozytorium) oraz Pythona z pakietami `duckdb`, `pandas` i `pyarrow`.

| Krok | Polecenie | Co robi | Wynik |
|---|---|---|---|
| A1 | `python -I analiza/a1_baza.py` | Buduje od zera bazę `analiza/telemedi.duckdb`. Schemat `surowe` zawiera dane z 17 plików CSV bez czyszczenia, z czasem polskim przy sesjach i zdarzeniach. | `wyniki/a1_baza.txt` |
| A2 | `python -I analiza/a2_jakosc.py` | Raport jakości danych. Tylko czyta schemat `surowe`. | `wyniki/a2_jakosc.txt` |
| A2 | `python -I analiza/a2_czyste.py` | Buduje schemat `czyste`: zamówienia bez duplikatów, bez 22 kont testowych i ich sesji. Decyzje: `notatki/ZALOZENIA.md`, punkty 6–9. | `wyniki/a2_czyste.txt` |
| A2 | `python -I analiza/a2_dyskusja.py` | Wyliczenia do trzech otwartych spraw z przeglądu A2 (sesje zalogowane, pierwsze tygodnie, kody rabatowe). Czyta `czyste`. | `wyniki/a2_dyskusja.txt` |

Plik bazy jest poza repozytorium. Krok A1 usuwa go i buduje od nowa, więc po nim trzeba ponownie uruchomić `a2_czyste.py`.

Dalsze liczby (kohorty, lejki, przychód, marża) liczymy na schemacie `czyste`. Na schemacie `surowe` liczymy tylko odtworzenie dashboardu (punkt A3).
