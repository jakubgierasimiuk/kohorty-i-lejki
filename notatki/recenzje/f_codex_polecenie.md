# Recenzja: czy nowe i zmienione zdania nie mówią więcej niż dane

Jesteś niezależnym recenzentem. Sprawdzasz statyczne narzędzie analityczne (strona w przeglądarce, 9 zakładek) przygotowane jako rozwiązanie zadania rekrutacyjnego dla biznesu telemedycznego B2C. Dane są syntetyczne. Właśnie skończyła się runda poprawek. Twoje zadanie jest wąskie: sprawdzić, czy nowe i zmienione zdania na stronie nie mówią więcej, niż pokazują dane na tej samej stronie, i czy liczby w nowej tabeli zgadzają się z liczbami w kartach, z których pochodzą.

## Pliki (w bieżącym katalogu; nie czytaj żadnych innych plików)

- `teksty_strony_po.md` — pełne teksty wszystkich zakładek po poprawkach, z rozwiniętymi sekcjami (wygenerowane z wyrenderowanej strony).
- `zmiany.diff` — różnice tych tekstów wobec wersji sprzed rundy poprawek (linie z „-” to stare brzmienie, z „+” nowe).

## Co sprawdzić

1. **Nowa pierwsza karta zakładki „Kohorty”** (tabela zdarzeń i decyzji: „Kohorty zmieniły się głównie po naszych decyzjach o kampaniach na L4…”):
   - czy tytuł, jedno zdanie wniosku i zastrzeżenie nie sugerują przyczyny mocniej, niż pozwalają dane i zastrzeżenia na stronie (np. słowa „głównie”, „po”, „największą pewną stratą”);
   - czy każda liczba w ośmiu wierszach tabeli zgadza się z tą samą liczbą w karcie źródłowej na tej samej stronie: karty osi zdarzeń („Zdarzenia”), przegląd listy priorytetów („Priorytety”), ekonomia kampanii („Wynik biznesu”), karta Safari („Lejek”), karta zwrotów („Po zakupie”), karty „Lepsza retencja” i kwartałów („Czy to wzrost”) — ta sama wartość, jednostka, okres i grupa pacjentów;
   - czy zdania „pewności” w trzech wierszach bez pozycji listy priorytetów są uczciwe.
2. **Karta „Lepsza retencja”** na pierwszej zakładce: czy nowe zastrzeżenie (o części spadku, która nie wynika ze składu pacjentów) jest zgodne ze zdaniem o około 71% spadku przypadającym na skład.
3. **Pierwszy punkt karty nagłówka „Lejka”**: czy opis, od kiedy przybywa ruchu z nowych kampanii, zgadza się z wykresem udziału na tej samej zakładce.
4. **Safari na równych oknach** (karta Safari w „Lejku” i pozycja 1 w „Priorytetach”): czy zdania cytujące wartości 60 dni przed i po awarii zgadzają się z wykresem i przypisem, i czy „do końca danych nie wraca” ma pokrycie.
5. **Sześć zmienionych zdań na pierwszej zakładce** („Czy to wzrost”): przyrost pacjentów z kanałów bezpłatnych, nazwana marża w zastrzeżeniu o III kwartale, reguły przypisania przy decyzji 2, zastrzeżenie przy 71%, zdanie o awarii Safari bez słowa o alarmie, kolejność decyzji na pierwszy tydzień zgodna z numeracją listy priorytetów.
6. Pozostałe zmiany z `zmiany.diff`: tylko jeśli widzisz w nich liczbę niezgodną z inną kartą albo zdanie mocniejsze niż dane.

## Forma odpowiedzi

Po polsku, najwyżej 700 słów. Najpierw jedno zdanie: czy jest coś, co trzeba poprawić przed publikacją. Potem lista uwag; przy każdej: zakładka i karta, cytat najwyżej 15 słów, na czym polega problem, propozycja poprawki, waga („błąd” — liczba niezgodna albo zdanie sprzeczne z danymi; „do poprawy” — zdanie mocniejsze niż dane albo mylące; „drobne”). Jeśli coś sprawdziłeś i jest w porządku, napisz to jednym zdaniem przy punkcie 1–5. Nie proponuj nowych analiz.
