# Brief dla konsylium: końcowa weryfikacja rozwiązania zadania rekrutacyjnego przed wysłaniem

## Cel

Sprawdzić całe rozwiązanie zadania rekrutacyjnego, zanim trafi do firmy, która je zleciła. Każdy członek zespołu ma dwie role naraz:

1. **Weryfikator:**
   - czy liczby zgadzają się między zakładkami narzędzia, README i notatkami;
   - czy definicje i rachunki są poprawne;
   - czy któryś wniosek mówi więcej, niż pokazują dane;
   - czy pominięto coś ważnego w kohortach, lejku, zdarzeniach, jakości danych, priorytetach albo niewiadomych.
2. **Osoba, która dała to zadanie i decyduje, czy kandydat się nadaje:**
   - co jest niejasne;
   - co nie przekonuje;
   - czego brakuje wobec tego, o co prosiło zadanie.

## Kontekst

- Zadanie dotyczy stanowiska szefa sprzedaży bezpośredniej do pacjentów (B2C) w firmie z konsultacjami lekarskimi online. Treść zadania jest w załączniku A.
- Dane obejmują dwa lata (1.10.2024 – 30.09.2026). Firma wygenerowała je na potrzeby zadania, więc nie opisują prawdziwych pacjentów.
- Kandydat oddaje trzy rzeczy:
  - działające narzędzie, czyli stronę w przeglądarce z dziewięcioma zakładkami (pełne teksty w załączniku C);
  - listę priorytetów (w narzędziu i w notatkach);
  - repozytorium ze śladem pracy (README w załączniku B).
- Kandydat pracował z AI. Analizę zrobił kodem (Python, DuckDB). Każdy krok sprawdzał drugi model, a listę priorytetów oceniała wcześniejsza runda kilku modeli.
- Założenia, znaleziska w danych i decyzje z całej pracy są w załączniku D. Najważniejsze zestawienia liczb z raportów są w załączniku E.

## Co sprawdzić

**Jako weryfikator:**
1. **Spójność liczb:** ta sama liczba w zakładkach (C), w README (B), w notatkach (D) i w raportach (E). Wypisz każdą rozbieżność z miejscem i obiema wartościami.
2. **Definicje i rachunki:**
   - nowy pacjent, powrót, źródło pozyskania (dwie reguły), przychód po zwrotach, marża, koszt lekarza, koszt pozyskania;
   - porównanie okresów na tych samych dniach kalendarzowych;
   - przeliczenia na pełny rok, scenariusze „naprawić albo wyłączyć”, próby testów.
   Gdzie się da, przelicz z liczb podanych w załącznikach.
3. **Wnioski ponad dane:** zdania o przyczynie, pewności, „wszystkie” i „zawsze”, uogólnienia z jednej grupy na całość.
4. **Pominięcia:** czego brakuje w kohortach, lejku, zdarzeniach, jakości danych, priorytetach albo niewiadomych, a co wynika z danych opisanych w załącznikach.

**Jako osoba, która zleciła zadanie:**
5. Porównaj rozwiązanie z wymaganiami z załącznika A, punkt po punkcie:
   - kohorty w rozdzielczości dziennej i zdarzenia znalezione w danych;
   - lejki: gdzie i od kiedy tracimy pacjentów;
   - narzędzie, na którym da się prowadzić biznes;
   - priorytety z wartością, sposobem pomiaru i czasem wdrożenia;
   - lista tego, czego nie da się rozstrzygnąć.
6. Co jest niejasne dla kogoś, kto czyta to pierwszy raz? Co nie przekonuje? Czego brakuje?
7. Twoja decyzja, gdybyś to Ty oceniał(a) kandydata, z uzasadnieniem: co przesądza na plus, a co na minus.

## Forma odpowiedzi

Po polsku, konkretnie.

1. **Lista poprawek od najważniejszej.** Przy każdej:
   - waga (krytyczna / ważna / drobna);
   - miejsce (zakładka i fragment, plik i sekcja);
   - co jest nie tak;
   - dowód (liczba z załącznika, Twoje przeliczenie, cytat do 15 słów);
   - propozycja poprawki.
2. **Co się potwierdziło:** liczby, definicje i wnioski, które sprawdziłeś(-aś) i które są poprawne.
3. **Ocena z perspektywy zlecającego:** trzy najmocniejsze strony, trzy najsłabsze, czego brakuje wobec zadania i Twoja decyzja z uzasadnieniem.

## Po czym poznać dobrą odpowiedź

- Każda uwaga wskazuje konkretne miejsce i da się ją sprawdzić. Ogólniki nie pomagają.
- Uwaga odróżnia błąd od stylu i od różnicy zdań.
- Przeliczenia pokazują, z jakich liczb wychodzą.
- Odpowiedź zaznacza, czego nie dało się sprawdzić z samych załączników.

## Ograniczenia i czego nie wiemy

- Oceniasz na podstawie załączników. Bazy danych nie masz (dwaj członkowie zespołu mają dostęp do plików i przeliczają liczby z bazy osobno).
- Zakładki narzędzia są w załączniku C jako tekst. Wykresów nie widać, a długie tabele są skrócone.
- Nie znamy oczekiwań firmy poza treścią zadania.
- W notatkach osoba prowadząca pracę nazywa się „kandydat”.

---
