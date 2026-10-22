## 1. Zgoda / sprzeciw dla sekcji 1–5

**Sekcja 1 — kolor ma dwa konkurencyjne znaczenia.** Zasada „okres B zawsze niebieski” koliduje ze stałym kolorem kategorii. Przyjąć: w porównaniu jednej miary między okresami niebieski/szary oznacza okres; na wykresie wielu grup kolor oznacza grupę, a okres odróżniamy linią ciągłą/przerywaną lub pełnym/pustym symbolem. Oba znaczenia muszą być opisane w legendzie.

**Sekcja 1 — nazwy okresów muszą odpowiadać filtrom.** „Rok wcześniej / ostatnie 12 miesięcy” nie pasuje do porównania przed awarią i po niej ani do własnych dat. Zachować obecne dynamiczne nazewnictwo, również w nowych wykresach.

**Sekcja 1 — jeden panel filtrów na każdą zakładkę jest zbyt szeroką regułą.** W „Po zakupie” specjalizacja wykresu punktualności nie filtruje zwrotów. W „Wyniku biznesu” grupowanie czasu i reguła przypisania kampanii dotyczą innych analiz. Jeden panel wspólny stosować w kohortach i lejku; pozostałe ustawienia zostawić przy odpowiednim wykresie, z wyraźnym zakresem działania.

**Sekcja 1 — zostawić podkreślenia odnośników w treści.** Usunięcie ich osłabia rozpoznawalność, szczególnie na telefonie, gdzie nie ma najechania. „Zobacz w danych” może mieć wygląd odrębnej akcji, ale powinno pozostać semantycznym odnośnikiem.

**Sekcje 2–3 — wykres składu ruchu musi pozostać niezależny od wybranego podziału.** Dane według przeglądarki nie zawierają równocześnie przekroju kampanii. Udział nowych kampanii liczyć z pliku kampanii, uwzględniając tylko obsługiwane filtry. Nie sugerować, że przedstawia skład ruchu wybranej przeglądarki. Analogicznie przy kohortach zaznaczyć, czy skład dotyczy wszystkich pacjentów w filtrze, czy zaznaczonych serii.

**Sekcja 3 — usunąć niepewność przy 180 dniach.** Dane pacjentów i obecny kod kohort pozwalają policzyć to w przeglądarce. Warunkiem jest użycie tych samych reguł pełnego okna i liczebności co w tabeli. Eksport nie jest tutaj konieczny.

**Sekcja 3 — dodatkowe odniesienie „Razem” w krokach lejka odłożyć.** Już porównujemy dwa okresy. Trzeci znacznik zwiększy obciążenie i wymaga kolejnego rozróżnienia. Można go później udostępnić jako opcję.

**Sekcja 5 — wycena nowych form jest zbyt optymistyczna.** Wspólna obsługa dotyku i klawiatury, mobilne tabele, filtry oraz kilka komponentów wykresów to osobne zadania. Nie traktowałbym całego etapu 3 jako pewnych 1–2 dni.

## 2. Głos w R1–R4

- **R1: (a), wspólna stała skala.** Ten sam odcień musi oznaczać ten sam odsetek, także po zmianie filtrów. Proponowane nierówne przedziały są dopuszczalne, jeżeli legenda pokazuje je wprost; brak pełnego okna musi wyglądać inaczej niż zero.
- **R2: (a), przycisk bieżącej zakładki z rozwijaną listą.** Odzyskuje miejsce na treść i zachowuje dostęp do wszystkich dziewięciu pozycji. Przycisk powinien pozostać dostępny podczas przewijania, bez przyklejania całego rozbudowanego nagłówka.
- **R3: (a), słowo widoczne zawsze.** Pozostałe opcje nie spełniają dosłownie zasady Kuby. W gęstej tabeli można przenieść etykietę do drugiego wiersza komórki; podpowiedź ani objaśnienie kolorów w nagłówku nie zastępują widocznego słowa.
- **R4: (c), marża przed kampaniami i wydatki, poniżej marża końcowa.** Bezpośrednio pokazuje główny problem biznesowy. Trzeba jednoznacznie zdefiniować, gdzie uwzględniono prowizję afiliacyjną, żeby rachunek zgadzał się z tabelą.
- **Ekonomia kampanii: punkt wyniku względem zera, dwa symbole reguł.** Odpowiada wprost na pytanie, które kampanie tracą. Hantle koszt–marża wymagają dodatkowego odejmowania w głowie.

## 3. Czego brakuje

1. **Warunków odbioru każdego etapu:** dziewięć zakładek, szerokości 1366 i 375 px, oba motywy, dotyk i klawiatura, brak przewijania strony w bok oraz zgodność wykresu z tabelą.
2. **Zachowania pełnego stanu w odnośnikach.** Nowe wybory miary, zaznaczenia i rozwinięcia wskazane odnośnikiem muszą odtwarzać właściwy dowód. To szczególnie ważne po przeniesieniu tabel do „Szczegółów”.
3. **Rozróżnienia braku danych:** niepełne okno, brak pacjentów i nieistniejąca wcześniej kampania nie mogą wyglądać jak wynik zerowy.

## 4. Czy kolejność etapów jest dobra?

**Kierunek jest dobry, ale zakres etapów trzeba zmniejszyć.** Najpierw poprawić istniejące dowody: skalę macierzy, kolory, szerokości wykresów, legendy i znaczniki zdarzeń. Razem z tym wdrożyć mobilną nawigację oraz czytelny dostęp do jednej miary tabeli.

Następnie zrobić jeden kompletny komponent hantli i zastosować go do retencji oraz Safari. Dopiero potem dodać wynik kampanii względem zera i przebudować wykres biznesowy.

Wykresy składu w czasie, schodki mostka i dodatki wymagające eksportu zostawić na koniec. Każdy etap powinien kończyć się działającym, sprawdzonym widokiem; przy małej ilości czasu można wtedy bezpiecznie zakończyć prace.