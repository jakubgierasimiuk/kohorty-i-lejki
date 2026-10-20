Liczby główne się zgadzają, ale interpretacja samoselekcji, liczebność próby testu i przedstawienie wyniku „bez poprzedniego rocznika” wymagają korekt.

Nie znalazłem uwag krytycznych. Poniżej uwagi od najważniejszych. Obliczenia wykonałem własnym kodem w pamięci, bez importowania Waszych skryptów. Bazę otworzyłem z `read_only=True`. Niczego nie zapisywałem. Plik `notatki/c_szkic.md` jeszcze nie istnieje, więc ocena wniosków dotyczy raportów tekstowych.

1. **Ważna — liczebność próby w projekcie B jest zaniżona.**

   **Problem:** wzór używa tej samej wariancji dla obu grup, mimo że zakładany wzrost odsetka powrotów jest duży. To przybliżenie nie wystarcza do deklarowania mocy 80%. Ponadto darmowe członkostwo po pierwszym zamówieniu różni się od płatnego programu kupowanego przy kasie. Różnica obserwacyjna z 4a może służyć do budowania scenariuszy testu, ale nie jest oszacowaniem jego oczekiwanego efektu.

   **Dowód:** [c_telemedigo.py:495](<C:/Users/K/Desktop/Zadanie - TM/analiza/c_telemedigo.py:495>)–505. Przy zachowaniu Waszej bazowej retencji 17,38% standardowe przybliżenie dla dwóch proporcji daje około **136, 487 i 1 823 osób na grupę**, zamiast 105, 422 i 1 687. Dotyczy to odpowiednio wzrostu o 14,62, 7,31 i 3,655 punktu procentowego.

   **Poprawka:** przeliczyć próbę z osobnymi proporcjami grup i zaokrąglać liczebność w górę. Projekt B opisać jako test *bezpłatnego dostępu do zniżek przez 90 dni*. Nie rozstrzyga on samodzielnie rentowności płatnego programu za 89 zł. W projekcie A trzeba też ustalić losowanie przed zakupem i uwzględnić możliwość wpływu oferty na samą pierwszą płatność.

2. **Ważna — „+8,1%” jest poprawnym rachunkiem, ale nie pełną korektą startu od zera.**

   **Problem:** odejmujecie marżę powtórnych konsultacji poprzedniego rocznika, pozostawiając jego zakupy TelemediGO.

   **Dowód:** [c_priorytety.py:128](<C:/Users/K/Desktop/Zadanie - TM/analiza/c_priorytety.py:128>)–133. Potwierdzam odjęcie **152 960,50 zł** marży konsultacji. W okresie 2 pacjenci pozyskani w okresie 1 przynoszą ponadto **41 474 zł opłat TelemediGO**. Po odjęciu obu pozycji wynik wynosi **853 634,84 zł**, czyli **+3,1%**, zamiast +8,1%.

   **Poprawka:** zachować +8,1% pod precyzyjną nazwą „po odjęciu marży powtórnych konsultacji poprzedniego rocznika”. Nie nazywać tego wynikiem hipotetycznego biznesu startującego od zera. Także +3,1% jest tylko dodatkowym rozbiciem księgowym: nie modeluje zmian wydatków ani zachowania pacjentów.

3. **Ważna — grupa „nie kupili” w 4c obejmuje późniejszych kupujących.**

   **Problem:** kontrola wyklucza zakup przez pierwsze 30 dni, ale wynik mierzy przez 180 dni. Nazwa grupy sugeruje brak członkostwa przez cały okres.

   **Dowód:** [c_telemedigo.py:472](<C:/Users/K/Desktop/Zadanie - TM/analiza/c_telemedigo.py:472>)–481. Niezależnie odtworzyłem **450 kupujących, 189 osób porównawczych i różnicę różnic +0,398 zamówienia na pacjenta**. Jednak **15 ze 189 osób porównawczych, czyli 7,9%, kupuje członkostwo później w obserwowanym oknie**.

   **Poprawka:** nazwać tę grupę „bez zakupu przy wejściu i przez następne 30 dni”. Pokazać późniejsze zakupy jako osobną kontrolę wrażliwości. Samo wykluczenie wszystkich późniejszych kupujących również selekcjonowałoby pacjentów według przyszłego zachowania.

   Lepsze porównanie na tych danych to dopasowanie przy wejściu z kampanii `crm_go_upsell` według miesiąca, stażu pacjenta, czasu od ostatniej konsultacji oraz wcześniejszej liczby i rodzaju zamówień. Następnie warto porównać przebieg zamówień w kilku oknach przed zakupem i po nim. Obecna różnica różnic jest poprawną statystyką opisową, ale nie identyfikuje wpływu programu bez założenia o równoległych trendach.

4. **Ważna — spadek różnicy po wygaśnięciu w 4b nie rozdziela wpływu ceny od samoselekcji.**

   **Problem:** wyłączenie odnawiających zależy od zachowania po zakupie programu. Usuwa między innymi najbardziej aktywnych członków. Raport słusznie wymienia to ograniczenie, ale wcześniejsze zdanie, że kontrole pokazują, „która część jest bardziej prawdopodobna”, nadal jest zbyt mocne.

   **Dowód:** [c_telemedigo.py:428](<C:/Users/K/Desktop/Zadanie - TM/analiza/c_telemedigo.py:428>)–458. Potwierdzam różnice **15,59, 6,26 i 1,28 punktu procentowego** w kolejnych oknach. Po wygaśnięciu iloraz odsetków wynosi nadal **1,77**, wobec **1,82** w dniach 1–90. Sama mniejsza różnica bezwzględna nie przesądza o mechanizmie.

   **Poprawka:** opisać 4b jako analizę przebiegu zamówień *wśród osób bez kolejnego zakupu członkostwa*. Obok pokazać wszystkich pierwotnych kupujących. Wniosek powinien brzmieć: „wynik jest zgodny z kilkoma wyjaśnieniami i nie rozstrzyga między nimi”.

5. **Ważna — wartości P6 są scenariuszami, a nie dolną i górną granicą korzyści.**

   **Problem:** pacjenci mogą reagować różnie. Mogą zniknąć tylko niektóre wizyty, a pozostałe przejść na cenę katalogową. Ponadto opis „znikają wizyty przynoszące stratę” nie odpowiada rachunkowi odejmującemu marżę wszystkich zamówień.

   **Dowód:** [c_telemedigo.py:371](<C:/Users/K/Desktop/Zadanie - TM/analiza/c_telemedigo.py:371>)–374 oraz [c_priorytety.py:201](<C:/Users/K/Desktop/Zadanie - TM/analiza/c_priorytety.py:201>). W okresie 2 zamówienia nieodebrane przynoszą **4 233,60 zł dodatniej marży**. Gdyby zniknęły wyłącznie zamówienia z ujemną marżą, korzyść wyniosłaby **18 915,20 zł**, a nie 14 681,60 zł.

   Przy dopuszczeniu osobnej reakcji każdego zamówienia „znika albo zostaje po cenie katalogowej” rachunek daje od **10 895,60 zł do 35 190,60 zł**. To także wynik warunkowy, bez wpływu na sprzedaż członkostw.

   **Poprawka:** wartości **14 682 zł** i **31 405 zł** nazwać dwoma scenariuszami: „znikają wszystkie analizowane zamówienia” oraz „wszystkie zostają po cenie katalogowej”. Nie przedstawiać ich jako granic.

6. **Ważna — porównanie opłaty ze zniżkami wymaga jawnego założenia o niezmienionej liczbie wizyt.**

   **Problem:** definicja „zniżki efektywnej” jest rozsądna, ale różnica między opłatą a zniżkami nie jest wynikiem ekonomicznym programu.

   **Dowód:** [c_telemedigo.py:278](<C:/Users/K/Desktop/Zadanie - TM/analiza/c_telemedigo.py:278>)–306. Potwierdzam **183 939,20 zł zniżek**, czyli **104,57 zł na członkostwo**, wobec 89 zł opłaty. W tej sekcji brakuje jednak wyraźnego zastrzeżenia, że porównanie zakłada te same wizyty bez programu.

   **Poprawka:** dodać: „Przy założeniu, że te same wizyty zostałyby kupione po cenie katalogowej bez TelemediGO, opłaty są o 27 388,20 zł niższe od udzielonych zniżek”. Nie nazywać tej kwoty stratą programu.

   Wyłączenie zamówień anulowanych i zwróconych z tej miary jest poprawne przy pełnych zwrotach. Koszt lekarza za wizytę zwróconą pozostaje natomiast kosztem w rachunku marży — kod uwzględnia to prawidłowo.

7. **Drobna — P10 liczy nominalne zniżki, a nie dokładny dodatkowy koszt testu.**

   **Problem:** część pacjentów otrzymuje już inne rabaty. Zastąpienie rabatu z kodu zniżką TelemediGO kosztuje mniej niż pełna zniżka od ceny katalogowej.

   **Dowód:** [c_priorytety.py:234](<C:/Users/K/Desktop/Zadanie - TM/analiza/c_priorytety.py:234>)–246. Potwierdzam **17 569 pacjentów**, **6,76496 zł nominalnej zniżki na pacjenta** oraz kwoty **2 855 zł i 11 412 zł**. W analizowanych zamówieniach jest jednak **1 035 zł już udzielonych rabatów z kodów**. Przy ich zastąpieniu dodatkowy koszt wynosi około **6,71 zł na pacjenta**.

   **Poprawka:** rozdzielić nominalną wartość zniżek i dodatkowy koszt względem obecnych cen. Kwoty testu zaktualizować po korekcie liczebności próby. Zdanie o pierwszym zamówieniu zmienić na „bez zniżki z członkostwa próbnego”, ponieważ inne kody rabatowe nadal mogą obowiązywać.

8. **Drobna — P5 potrzebuje założenia o odrębności odzyskanych zamówień.**

   **Problem:** jednostką rachunku jest sesja, a kilka sesji jednego pacjenta może dotyczyć tego samego zamiaru zakupu. Wskaźnik 90,5% pochodzi ponadto z późniejszego etapu ścieżki, więc nie jest formalną górną granicą konwersji po wyborze usługi.

   **Dowód:** [c_priorytety.py:185](<C:/Users/K/Desktop/Zadanie - TM/analiza/c_priorytety.py:185>)–193. Rachunki **40 399 zł i 89 391 zł** są poprawne. Raport źródłowy wskazuje jednak **2 906 sesji należących do 2 557 pacjentów**.

   **Poprawka:** nazwać oba wyniki scenariuszami. Dopisać założenie, że odzyskane płatności są odrębnymi, dodatkowymi zamówieniami. Warto pokazać wariant po połączeniu bliskich czasowo sesji pacjenta.

Pozostałe sprawdzone elementy są poprawne:

- **Sekcja 1e:** mianownik prawidłowo wyklucza zamówienia z wcześniej aktywnym członkostwem. Dla pierwszych zamówień wzrost o **184 zakupy** rozkłada się na **+471,49** z większej liczby zamówień i **−287,49** ze zmiany odsetka. Dla kolejnych zamówień wzrost o **289 zakupów** to odpowiednio **+233,93** i **+55,07**. Jest to poprawny rozkład przy odsetku z okresu 1 jako bazie.
- **Sekcja 4a:** kod rzeczywiście stosuje opisane warstwy i waży wynik liczbą kupujących. Odtworzyłem między innymi różnicę **14,62 punktu procentowego** w okresie 2 oraz **15,33 punktu procentowego** po dodaniu statusu pierwszego zamówienia. To porównanie obserwacyjne; wariant ze statusem pozostawiłbym jako kontrolę wrażliwości.
- **P1:** rachunek i dobór marży są poprawne. Potwierdzam **74 786–82 765 zł** dla marży w 90 dniach oraz **86 043–95 222 zł** dla marży w 180 dniach, przy rocznej liczbie odzyskanych pacjentów. Pominięcie kosztu pozyskania jest uzasadnione przy niezmienionych wydatkach. Warto dopisać założenie utrzymania skali problemu przez rok. Są to marże rocznika pacjentów, a nie pieniądze uzyskane w całości w tym samym roku.
- **P7:** wzór „oszczędzone wydatki − udział pacjentów dodatkowych × liczba pacjentów × marża” jest poprawny. Wszystkie cztery zestawy wartości zgadzają się z danymi wejściowymi. Założenia są nazwane w punkcie 42 `ZALOZENIA.md`; warto przywołać ten punkt bezpośrednio w P7.
- **W1–W2:** zdanie o większej liczbie pacjentów i niższej retencji jest podparte. Potwierdzam wzrost nowych pacjentów o **52,1%**. Powrót w 90 dniach wynosi **23,91% dla 12 867 pacjentów okresu 1** oraz **17,38% dla 18 924 pacjentów okresu 2**. Bez nowych kampanii w okresie 2 wynosi **21,99% dla 14 031 pacjentów** według przyjętej reguły oraz **20,41% dla 15 414 pacjentów** według sesji płatności. To spadek obserwowanej retencji, również po wyłączeniu kampanii; nie dowodzi jeszcze pogorszenia zachowania identycznych pacjentów.

W tabeli pary oznaczają **okres 1 / okres 2**. Drobne różnice wynikają wyłącznie z pokazania groszy lub większej liczby miejsc po przecinku.

| Miara | Wasz wynik | Moje niezależne przeliczenie |
|---|---:|---:|
| Zakupy TelemediGO | 1 759 / 2 468 | 1 759 / 2 468 |
| Przy kasie z pierwszym zamówieniem | 905 / 1 089 | 905 / 1 089 |
| Przy kasie z kolejnym zamówieniem | 629 / 918 | 629 / 918 |
| Osobno, z kampanii `crm_go_upsell` | 225 / 461 | 225 / 461 |
| Udział nowych pacjentów kupujących przy pierwszym zamówieniu | 5,58% z 16 231 / 4,41% z 24 687 | 5,57575% / 4,41123%; te same mianowniki |
| Udział bez dwóch nowych kampanii, okres 2 | 5,63% z 17 419 | 981 / 17 419 = 5,63178% |
| Zniżki efektywne członkostw kupionych w okresie 1 | 183 939 zł | 183 939,20 zł |
| Zniżka na członkostwo z okresu 1 | 104,57 zł | 104,57032 zł |
| Marża zamówień ze zniżką u specjalistów poza internistą i psychiatrą | −7 845 zł / −14 682 zł | −7 844,80 zł / −14 681,60 zł |
| Liczba tych zamówień | 753 / 1 512 | 753 / 1 512 |
| Wynik biznesu według W3 | 828 085 zł / 1 048 069 zł | 828 085,25 zł / 1 048 069,34 zł |