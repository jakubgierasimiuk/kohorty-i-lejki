**1. Zgoda / sprzeciw dla sekcji 1–5**

V1 wymaga kilku korekt przed wdrożeniem. Ocena opiera się na zrzutach i kodzie; nie testowałem interakcji w przeglądarce. Nie zmieniałem plików.

- **Sekcja 1 — jeden panel filtrów na każdą zakładkę jest błędem.** W „Po zakupie” poszczególne analizy mają różne zakresy filtrów. Potwierdzają to kod i wcześniejsze decyzje projektowe. Wspólny panel zachować dla kohort i lejka. Ustawienia dotyczące pojedynczego wykresu pozostawić przy nim.

- **Sekcja 1 — nie usuwać stałego podkreślenia odnośników w tekście.** Na telefonie nie ma najechania kursorem, a sam kolor osłabia rozpoznawalność odnośnika. „Zobacz w danych” może dostać osobny styl, ale nadal powinno być odnośnikiem z konkretną nazwą celu. Ikony dziewięciu zakładek nie są potrzebne.

- **Sekcje 1–2 — rozdzielić kodowanie okresu od kodowania kategorii.** Niebieski nie może jednocześnie oznaczać okresu B i konkretnej kampanii na wykresie porównującym oba wymiary. Para szary–niebieski obowiązuje przy porównaniu okresów; przy porównaniu kategorii obowiązuje stała paleta bytów. Safari wymaga podpisów „przed awarią” i „po awarii” z datami, a nie automatycznych etykiet dwóch lat.

- **Sekcje 1 i 3 — najpierw wykres dzienny, potem opcjonalny skład ruchu.** W lejku proponowany wykres udziałów ponownie odsuwa odpowiedź „od kiedy tracimy pacjentów”. Dodatkowe odniesienie „Razem” w wykresie kroków odłożyłbym: obok znacznika poprzedniego roku tworzy drugą bazę porównania. Kliknięcie przejścia jako skrót do trendu popieram.

- **Sekcje 1 i 3 — nie chować warunków interpretacji pod ogólną regułą upraszczania.** W priorytetach obok kwoty muszą zostać horyzont, warunek scenariusza i czas wdrożenia. W niewiadomych widoczny powinien pozostać także proponowany test. Zastrzeżenie ograniczające główny wniosek umieszczać przy nim, nawet jeśli oznacza to odstępstwo od kolejności „wniosek → wykres → zastrzeżenie”.

- **Sekcje 2–3 — słupki skumulowane wymagają doprecyzowania.** Porównanie liczby pacjentów między latami powinno używać długości odpowiadającej liczbie pacjentów, bez normalizacji do 100%. Dla trzech sposobów zakupu TelemediGO lepsze są słupki parami: wszystkie porównywane wartości mają wspólny początek. To nadal wymaga eksportu pól liczbowych.

- **Sekcja 3 — znacznik „Czyste” może sugerować pełną certyfikację danych.** Nie nadawać nowej pozytywnej oceny samą warstwą graficzną. Jeśli eksport nie dostarcza takiego stanu, zachować neutralną prezentację.

- **Sekcje 3 i 5 — nakład jest niedoszacowany.** Kilka nowych wykresów, przebudowa filtrów, mobilnych tabel i dostępnych interakcji nie stanowi jednej zmiany M. Etap trzeci trzeba rozbić na osobne, opcjonalne dostawy. Każda obejmuje również telefon, tryb ciemny i sprawdzenie zgodności wartości.

**2. Głos w R1–R4**

- **R1: a — wspólna, stała skala.** Kod obecnie wyznacza granice osobno dla kolumn z ich rozkładu wartości. Kolor zmienia więc znaczenie między oknami i filtrami. Brak pełnego okna musi mieć odrębne oznaczenie; przedziały legendy powinny być jawne.

- **R2: a — przycisk z nazwą bieżącej zakładki.** Oszczędza wysokość telefonu i pokazuje bieżące miejsce. Po rozwinięciu wszystkie dziewięć nazw powinno być dostępne bez poziomego przewijania.

- **R3: a — słowo widoczne zawsze, kiedy występuje kolor stanu.** Legenda „zielone = lepiej” nie zastępuje słowa przy konkretnej wartości. Dla zmian bez jednoznacznej oceny stosować neutralną etykietę, bez dopisywania „lepiej” lub „gorzej”.

- **R4: c — porównanie marży przed kosztem kampanii z wydatkami, niżej wynik po kosztach.** Najlepiej odpowiada głównemu wnioskowi zakładki. Trzeba jawnie określić miejsce prowizji afiliacyjnej, zgodnie z istniejącym rachunkiem. Dla ekonomii kampanii wybieram **dwa symbole wyniku względem zera**: bezpośrednio pokazują rentowność według dwóch reguł przypisania.

**3. Czego brakuje**

1. **Dostępności istniejących wykresów uPlot.** Wspólna podpowiedź tylko dla SVG nie rozwiązuje obsługi trendów dotykiem i klawiaturą. Potrzebny jest również dostępny odczyt ich wartości.
2. **Jawnego zakresu filtrów i dojrzałości kohort.** Stały wniosek wprowadzający należy odróżnić od filtrowanego wyniku. Wykres udziałów pacjentów nie może sugerować, że najnowsze kohorty mają już obserwację powrotu w pełnym oknie.
3. **Weryfikacji odnośników po przebudowie.** Skoki muszą zachować ustawienia, odsłonić zwinięty cel i doprowadzić użytkownika do właściwego dowodu.

**4. Czy kolejność etapów jest dobra?**

**Nie w obecnym podziale.** Przy małej ilości czasu proponuję:

1. **Samodzielna poprawa obecnej wersji:** stała skala macierzy, czytelne etykiety, szerokość wykresów, mobilna lista zdarzeń, typografia.
2. **Samodzielna poprawa pracy:** wykresy dzienne wyżej, dostępne legendy i odczyt wartości, czytelne tabele mobilne, jawny zakres filtrów.
3. **Pojedyncze nowe dowody:** najpierw hantle retencji i Safari, następnie wynik kampanii względem zera.
4. **Opcjonalne rozszerzenia:** skład ruchu, schodki korekt i propozycje wymagające eksportu.

Każdy etap kończyć sprawdzeniem liczb, odnośników oraz widoku na komputerze i telefonie. Nie uzależniać wysłania od całego katalogu nowych wykresów.