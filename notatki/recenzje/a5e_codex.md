# Recenzja ekonomii kampanii przez Codeksa (model Sol), 2026-10-19

Polecenie: `notatki/recenzje/a5e_codex_prompt.md`. Odpowiedź: `notatki/recenzje/a5e_codex_odpowiedz.md`. Wywołanie: `codex exec -p review -s read-only --skip-git-repo-check` (profil `review` = model Sol), tylko odczyt.

**Werdykt Codeksa:** liczby z punktu 1 polecenia są poprawne. Scenariusze „naprawić” wymagały korekt rachunkowych. Decyzji o wyłączeniu kampanii nie da się uzasadnić samą atrybucją ani obecnym testem dodatkowości.

**Liczby przeliczone niezależnie, własnym kodem Codeksa, wszystkie zgodne co do sztuki i co do złotówki:**
- obie nowe kampanie według przyjętej reguły: 4 893 pacjentów, koszt pozyskania 32,7 zł, marża 36,3 zł, wynik +3,6 zł;
- to samo według sesji płatności: 3 510 pacjentów, 45,6 zł, 36,1 zł, −9,4 zł;
- pozostałe kampanie płatne: 7 076 pacjentów, 44,2 zł, 64,2 zł, +20,0 zł;
- TikTok: 1 265 i 921 pacjentów, wynik −4,6 i −17,8 zł;
- prowizja: 15 425 zł, 10 125 zł i 7 375 zł;
- zwroty L4: 1 024 z 5 895 i 270 z 5 080;
- wartość powrotu: 95,581 zł;
- scenariusz poranka: 31 806, 65 247, 12 656 i 11 931 zł.

| Uwaga | Waga | Co zrobiliśmy |
|---|---|---|
| 1. Zestawienie „naprawić” miesza horyzonty (wartość zgód w 180 dniach dodana do wyniku w 90 dniach). Wiersz „obie” nie jest sumą kampanii: 17 849 zł zamiast 15 917 zł. | ważna | Poprawione. Wiersz „obie” to teraz suma kampanii liczonych osobno (+15 917 zł według przyjętej reguły, −59 536 zł według sesji płatności). Zgody pokazujemy osobno, w horyzoncie 180 dni, i nie dodajemy ich do sum. Nazwa: prognoza marży rocznika pozyskanych pacjentów. |
| 2. Wariant B zmniejszenia zwrotów potrzebuje innego mianownika i prawdziwego kosztu lekarza. Część zwróconych wizyt L4 to psychiatra, więc średnio 32,01 zł, a nie 25 zł. | ważna | Poprawione. Wariant A liczony z dokładnych odsetków: 710,7 zwrotu mniej, 57 112 zł. Wariant B z równania (zwroty − x) / (wizyty − x) = docelowy odsetek: x = 750,6. Liczymy go z rzeczywistym kosztem lekarza i odejmujemy dalszą marżę tych pacjentów (2,32 zł): 22 283 zł zamiast 17 832 zł. |
| 3. „Wyłączyć” zakłada, że pacjenci dodatkowi mają średnią marżę wszystkich przypisanych. Reszta biznesu musi się nie zmieniać. Rachunek nie obejmuje marży po przyjętym horyzoncie. | ważna | Założenia dopisane w raporcie (E1) i w notatce. Rachunek liczony bez zaokrągleń pośrednich, więc TikTok według przyjętej reguły daje +11 928, +47 196 i +82 464 zł, tak jak u Codeksa. |
| 4. Opisy sugerują przyczynowość: powrót przypisany do newslettera i SMS-a to nie „dolna granica wpływu”; wybór większej wartości zgód to wariant optymistyczny; „niska konwersja to cecha ruchu, nie przeglądarki” to za dużo; zakres scenariusza poranka nie jest przedziałem, a efekt może być zerowy. | ważna | Poprawione wszystkie cztery. W scenariuszu poranka dodany wiersz „brak efektu” (0 zł), a warianty nazywają się „wąski” i „szeroki”. Przy przeglądarkach zostało tylko to, co widać: surowa konwersja w tej samej sesji nie jest niższa. |
| 5. Brak spadku rok do roku nie wyklucza przejmowania pacjentów, bo pozostałe kanały mogłyby rosnąć szybciej. Codex dodał porównanie L4 z innymi usługami: 0,730 (od 0,560 do 0,951) po starcie Meta i 0,900 po starcie TikToka. | ważna | Dodane naszym kodem (D2): 0,73 (od 0,56 do 0,95) i 0,90 (od 0,71 do 1,14). Dodana kontrola fikcyjnymi datami startu (D2b): przy starcie Meta niższy albo równy iloraz wyszedł w 4 z 44 poniedziałków okresu 1. Wniosek zawężony do brzmienia zaproponowanego przez Codeksa. Przybliżenie D4 sumujemy bez zaokrągleń: 226 pacjentów. |
| 6. Przedział 95% można bronić tylko jako warunkowy przedział średniej marży. | ważna | Nazwa i opis zmienione w obu raportach i w notatce. Wspólne losowanie bloków tygodniowych zostawiamy jako możliwe rozszerzenie. |
| 7. Rozliczanie wydatków według dnia płatności to rozsądne przybliżenie. Kontrola brzegu okna: 4 912 pacjentów według dnia pierwszego wejścia, koszt pozyskania 32,55 zł zamiast 32,68 zł. | drobna | Kontrola dodana do raportu (sekcja 0), wynik ten sam co u Codeksa. |
| 8. „Niepewne” powinno mówić, że to niepewność atrybucji. Dodatni wynik w obu regułach nie dowodzi opłacalności dodatkowego budżetu. | drobna | Nazwa sekcji i opis zmienione, uwaga o budżecie dopisana. Rozbicie 1 383 pacjentów, którzy zapłacili w innych sesjach (575 bezpośrednich, 325 z bezpłatnego Google, 299 z wyszukiwania marki, 184 z remarketingu Meta), wpisane do notatki. |
