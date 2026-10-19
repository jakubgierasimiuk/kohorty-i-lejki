# Analiza — kolejność uruchamiania

Wszystkie skrypty uruchamiamy z głównego folderu projektu. Wymagają rozpakowanych danych w `dane/` (poza repozytorium) oraz Pythona z pakietami `duckdb`, `pandas` i `pyarrow`.

| Krok | Polecenie | Co robi | Wynik |
|---|---|---|---|
| A1 | `python -I analiza/a1_baza.py` | Buduje od zera bazę `analiza/telemedi.duckdb`. Schemat `surowe` zawiera dane z 17 plików CSV bez czyszczenia, z czasem polskim przy sesjach i zdarzeniach. | `wyniki/a1_baza.txt` |
| A2 | `python -I analiza/a2_jakosc.py` | Raport jakości danych. Tylko czyta schemat `surowe`. | `wyniki/a2_jakosc.txt` |
| A2 | `python -I analiza/a2_czyste.py` | Buduje schemat `czyste`: zamówienia bez duplikatów, bez 22 kont testowych i ich sesji. Decyzje: `notatki/ZALOZENIA.md`, punkty 6–9. | `wyniki/a2_czyste.txt` |
| A2 | `python -I analiza/a2_dyskusja.py` | Wyliczenia do trzech otwartych spraw z przeglądu A2 (sesje zalogowane, pierwsze tygodnie, kody rabatowe). Czyta `czyste`. | `wyniki/a2_dyskusja.txt` |
| A3 | `python -I analiza/a3_dashboard.py` | Odtworzenie dashboardu: siatka 864 kombinacji definicji na danych surowych, kombinacje zgodne z czterema liczbami, mostek do danych oczyszczonych. | `wyniki/a3_dashboard.txt`, `wyniki/a3_siatka.csv` |
| A4 | `python -I analiza/a4_definicje.py` | Warianty definicji (nowy pacjent, anulacje i zwroty, powrót, źródło pozyskania i prowizja, okno CRM) i ich wpływ, liczby według przyjętych definicji (sekcja 6), przykłady pacjentów do ręcznej kontroli kodu. Czyta `czyste`. Definicje: `notatki/ZALOZENIA.md`, punkty 16–26. | `wyniki/a4_definicje.txt`, `wyniki/a4_zrodla_kampanie.csv`, `wyniki/a4_przyklady.txt` |
| A5 | `python -I analiza/a5p_lejek.py` | Lejek od sesji do płatności: typy sesji, kwartały i miesiące, podziały (urządzenie, przeglądarka, kanał, kampania, strona wejścia, czy kupował wcześniej), rozkład zmiany konwersji, czasy między krokami, od kliknięcia do sesji. Około 85 s. | `wyniki/a5p_lejek.txt`, `wyniki/a5p_lejek_dzienny.csv.gz` |
| A5 | `python -I analiza/a5p_zdarzenia.py` | Zdarzenia w lejku (podział binarny serii dziennych) i ich sprawdzenie na bazie. Uruchamiać po `a5p_lejek.py`. Około 100 s. | `wyniki/a5p_zdarzenia.txt`, `wyniki/a5p_zdarzenia.csv` |
| A5 | `python -I analiza/a5p_zalogowane.py` | Sesje zalogowane od wejścia: krok odpadania, strony i kampanie, zakupy po takiej sesji, porównanie z podobnymi pacjentami, czas do kroku logowania, dane do wariantu pesymistycznego. Importuje `definicje.py`. | `wyniki/a5p_zalogowane.txt` |
| A5 | `python -I analiza/a5p_sezon.py` | Sezon a wydatki: nowi pacjenci w kanałach płatnych i bezpłatnych miesiąc po miesiącu, koszt pozyskania kampanii, popyt w wyszukiwarce. Importuje `definicje.py`. | `wyniki/a5p_sezon.txt`, `wyniki/a5p_sezon_miesiace.csv` |
| A5 | `python -I analiza/a5r_kontrola_definicji.py` | kontrola wspólnego modułu `analiza/definicje.py` wobec sekcji 6 raportu A4. | `wyniki/a5r_kontrola_definicji.txt` |
| A5 | `python -I analiza/a5r_kohorty.py` | kohorty dzienne, powroty w 30/60/90 dniach, zamówienia i marża na pacjenta, kohorty miesięczne i tygodniowe, start od zera, wrażliwość na koszt pediatry. | `wyniki/a5r_kohorty.txt`, `wyniki/a5r_kohorty_dzienne.csv` |
| A5 | `python -I analiza/a5r_punktualnosc.py` | opóźnienie wizyt (co do sekundy), pora, obciążenie godzin i ruch poranny w dniu u internisty (przepustowość poranka), powrót według opóźnienia pierwszej wizyty, rozkład zagnieżdżony punktualności, opóźnienia w czasie. Importuje `a5r_struktura.py`. | `wyniki/a5r_punktualnosc.txt`, `wyniki/a5r_punktualnosc_tygodnie.csv` |
| A5 | `python -I analiza/a5r_po_zakupie.py` | czekanie, długość wizyty, statusy i zwroty, oceny, rozkład z przebiegiem pierwszej wizyty, newsletter i SMS a powroty. Importuje `a5r_punktualnosc.py` i `a5r_struktura.py`. | `wyniki/a5r_po_zakupie.txt` |
| A5 | `python -I analiza/a5r_zdarzenia.py` | zdarzenia w seriach retencji i po zakupie (podział binarny), miesiące spadku z datami kampanii na L4 i opóźnieniami, Safari na iOS, przybliżony wpływ na marżę. | `wyniki/a5r_zdarzenia.txt`, `wyniki/a5r_zdarzenia.csv` |
| A5 | `python -I analiza/a5r_struktura.py` | rozdzielenie zmiany struktury pacjentów od zmiany zachowania (kanał, kampania, usługa, zniżka, przebieg pierwszej wizyty, przeglądarka), Meta po kampaniach, L4 z L4, TikTok osobno, kontrole wrażliwości, niepewność. | `wyniki/a5r_struktura.txt` |
| A5 | `analiza/definicje.py` (moduł, nie uruchamiać) | Wspólny moduł przyjętych definicji (A4): kohorty, powroty, sesje pacjenta, reguły źródła, kontakty z newslettera i SMS-ów. Importują go skrypty A5. Zgodność z raportem A4 sprawdza `a5r_kontrola_definicji.py`. | — |

Plik bazy jest poza repozytorium. Krok A1 usuwa go i buduje od nowa, więc po nim trzeba ponownie uruchomić `a2_czyste.py`.

Dalsze liczby (kohorty, lejki, przychód, marża) liczymy na schemacie `czyste`. Na schemacie `surowe` liczymy tylko odtworzenie dashboardu (punkt A3).
