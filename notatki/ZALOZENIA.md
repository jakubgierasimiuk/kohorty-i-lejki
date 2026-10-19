# Założenia

Każde założenie przyjęte tam, gdzie zadanie nie daje definicji (zasada Telemedi: „nie pytaj o definicje — przyjmij założenie i je nazwij”). Przy każdym: co zakładamy, dlaczego, jaki ma wpływ na wynik.

## 2026-10-19 — baza danych i czas (punkt A1)

1. **Dane w bazie są surowe.** Baza `analiza/telemedi.duckdb` (schemat `surowe`) zawiera wszystkie wiersze z 17 plików CSV, bez deduplikacji i bez filtrów. README mówi wprost, że eksport jest surowy. Czyszczenie to osobny krok (punkt A2), żeby każdą decyzję o usunięciu wiersza dało się pokazać i policzyć jej wpływ.
2. **Puste pole = brak wartości (NULL).** Dotyczy to też źródła wejścia: puste `utm_source`, `utm_medium` i `utm_campaign` oznaczają wejście bezpośrednie (tak mówi README).
3. **Sesje i zdarzenia przeliczamy z UTC na czas polski (Europe/Warsaw).** Dzień sesji i zdarzenia to dzień według czasu polskiego (kolumna `dzien_pl`). Przeliczenie uwzględnia cztery zmiany czasu, które wypadają w okresie danych: 27.10.2024, 30.03.2025, 26.10.2025 i 29.03.2026. Wpływ: 2,1% sesji i 2,5% zdarzeń trafia do innego dnia niż według UTC. To są wejścia po 22:00 albo 23:00 czasu polskiego, które w UTC wypadają jeszcze poprzedniego dnia.
4. **Tabele z systemu transakcyjnego bierzemy jako czas polski, bez przeliczania.** Dotyczy to kont pacjentów (`users`), zamówień (`orders`) i zakupów TelemediGO (`go_memberships`). Tak mówi README. Sprawdzimy to w punkcie A2: porównamy moment płatności w zamówieniu z krokiem `payment_succeeded` w analityce po przeliczeniu strefy.
5. **Czas trwania i kolejność kroków w analityce liczymy na kolumnach UTC, nie na czasie polskim.** W noc zmiany czasu z letniego na zimowy godzina 2:00–3:00 czasu polskiego występuje dwa razy. Różnica dwóch czasów polskich z tej nocy byłaby błędna o godzinę. W kolumnach UTC tego problemu nie ma.

## 2026-10-19 — czyszczenie danych (punkt A2, przyjęte z Kubą)

Oczyszczone dane są w schemacie `czyste` bazy, budowanym skryptem `analiza/a2_czyste.py`. Wszystkie dalsze liczby (kohorty, lejki, przychód, marża) liczymy na `czyste`. Na danych surowych liczymy tylko odtworzenie dashboardu (punkt A3).

6. **Zdublowane zamówienia: zostaje jedna kopia.** 604 zamówienia z okna 10–24.06.2026 mają dwie identyczne kopie. Traktujemy to jako błąd eksportu, a nie jako podwójne płatności, bo w analityce każde z nich ma tylko jeden krok płatności. Wpływ: drugi rok dashboardu traci 604 zamówienia i 45 805 zł zapłat po zwrotach.
7. **Konta testowe są wyłączone ze wszystkiego.** Konto testowe to konto, które choć raz użyło kodu TEST-QA (22 konta). Ten sam zbiór wyznaczają zamówienia trwające 1 minutę. Wyłączamy wszystkie ich zamówienia (2 071, także 290 bez kodu), same konta, sesje (2 093) i zdarzenia lejka. Wpływ: 553 zamówienia mniej w pierwszym roku dashboardu i 1 518 w drugim. **Na końcu pracy przyglądamy się testom jeszcze raz dokładnie** (punkt D w planie).
8. **Za wizyty testowe nie liczymy kosztu lekarza.** Wizyta testowa trwa 1 minutę i wygląda na test systemu, a nie na pracę lekarza. Wariant z kosztem według zasady z zadania (25 zł za odbytą wizytę u internisty, razem 51 775 zł) trafia na listę rzeczy, których nie da się rozstrzygnąć.
9. **Drobne niespójności zostają w danych, z adnotacją w `ZNALEZISKA.md`.** Dotyczy to godziny bez danych (17.05.2025 13:00–14:00), 24 zamówień „psycholog + e-recepta”, jednego zamówienia bez zniżki mimo aktywnego TelemediGO i niespójnych oznaczeń programu poleceń. Żadna z nich nie zmienia wyników w widoczny sposób.

## 2026-10-19 — trzy otwarte sprawy z A2 (przyjęte z Kubą)

Wyliczenia: `analiza/a2_dyskusja.py`, wynik w `analiza/wyniki/a2_dyskusja.txt`.

10. **Sesja zalogowana od wejścia** = sesja, w której jest konto pacjenta, nie ma kroku `account_completed` i nie jest to zakup samego TelemediGO (w danych oczyszczonych 22 068 sesji). W lejku pokazujemy ją jako osobny wiersz. To rozpoznanie pośrednie: w danych nie ma informacji, czy pacjent był zalogowany w chwili wejścia.
11. **Newsletter i SMS oceniamy na poziomie pacjenta**, czyli po tym, czy pacjent wraca w ciągu kilku dni od kontaktu, a nie po konwersji sesji. Okno ustalimy w A4.
12. **Nie wyznaczamy osobnego okresu rozruchu.** Nowi pacjenci od pierwszego tygodnia są na zbliżonym poziomie: 198 w pierwszym, 6-dniowym tygodniu, potem około 300 tygodniowo w październiku 2024. Od zera rośnie tylko baza powracających: zamówienia powtórne rosną z 2 w pierwszym tygodniu do 224 tygodniowo pod koniec marca 2025. Start od zera obsługujemy rozbiciem na nowych i powracających oraz porównaniem kohort w tym samym wieku. Sprawdzamy, czy wnioski o retencji trzymają się bez kohort z października 2024. **Przyczyna wzrostu liczby nowych pacjentów od października 2024 do stycznia 2025 jest otwarta**, bo w tym samym czasie rosną wydatki na kampanie. Sezon i wydatki rozdzielamy w A5.
13. **START10 to stały kod dla nowych pacjentów** (10 zł na pierwszym zamówieniu, przez całe dwa lata), czyli zwykła zniżka pozyskania, a nie znacznik okresu startu.
14. **Zniżkę liczymy w złotych** jako cenę katalogową minus zapłatę (`list_price − amount_paid`). Kody rabatowe obniżają cenę o stałą kwotę, TelemediGO o 50% u internisty i o 20% u pozostałych.
15. **Prowizję afiliacyjną liczymy tą samą regułą, którą w A4 wybierzemy dla źródła pozyskania.** Obok pokazujemy jedną liczbą drugi wariant, czyli prowizję za pierwsze zamówienia z kodem RANKING10. Punkt wyjścia: 842 pierwsze zamówienia zapłacone w sesji z rankingu wobec 595 zamówień z kodem RANKING10.
