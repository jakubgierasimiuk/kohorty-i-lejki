# Założenia

Każde założenie przyjęte tam, gdzie zadanie nie daje definicji (zasada Telemedi: „nie pytaj o definicje — przyjmij założenie i je nazwij”). Przy każdym: co zakładamy, dlaczego, jaki ma wpływ na wynik.

## 2026-10-19 — baza danych i czas (punkt A1)

1. **Dane w bazie są surowe.** Baza `analiza/telemedi.duckdb` (schemat `surowe`) zawiera wszystkie wiersze z 17 plików CSV, bez deduplikacji i bez filtrów. README mówi wprost, że eksport jest surowy. Czyszczenie to osobny krok (punkt A2), żeby każdą decyzję o usunięciu wiersza dało się pokazać i policzyć jej wpływ.
2. **Puste pole = brak wartości (NULL).** Dotyczy to też źródła wejścia: puste `utm_source`, `utm_medium` i `utm_campaign` oznaczają wejście bezpośrednie (tak mówi README).
3. **Sesje i zdarzenia przeliczamy z UTC na czas polski (Europe/Warsaw).** Dzień sesji i zdarzenia to dzień według czasu polskiego (kolumna `dzien_pl`). Przeliczenie uwzględnia cztery zmiany czasu, które wypadają w okresie danych: 27.10.2024, 30.03.2025, 26.10.2025 i 29.03.2026. Wpływ: 2,1% sesji i 2,5% zdarzeń trafia do innego dnia niż według UTC. To są wejścia po 22:00 albo 23:00 czasu polskiego, które w UTC wypadają jeszcze poprzedniego dnia.
4. **Tabele z systemu transakcyjnego bierzemy jako czas polski, bez przeliczania.** Dotyczy to kont pacjentów (`users`), zamówień (`orders`) i zakupów TelemediGO (`go_memberships`). Tak mówi README. Sprawdzimy to w punkcie A2: porównamy moment płatności w zamówieniu z krokiem `payment_succeeded` w analityce po przeliczeniu strefy.
5. **Czas trwania i kolejność kroków w analityce liczymy na kolumnach UTC, nie na czasie polskim.** W noc zmiany czasu z letniego na zimowy godzina 2:00–3:00 czasu polskiego występuje dwa razy. Różnica dwóch czasów polskich z tej nocy byłaby błędna o godzinę. W kolumnach UTC tego problemu nie ma.
