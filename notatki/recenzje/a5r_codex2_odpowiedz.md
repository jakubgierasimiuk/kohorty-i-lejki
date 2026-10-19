Dane pasują do hipotezy przeciążenia internistów, ale jej nie dowodzą, a definicja opóźnienia, przypisanie części spadku punktualności i niektóre interpretacje statystyczne wymagają poprawy.

Wszystkie przeliczenia wykonałem własnym kodem w pamięci, na bazie otwartej z `read_only=True`. Nie zmieniałem ani nie tworzyłem plików. Nie znalazłem błędu krytycznego.

1. **Ważna — kod nie liczy dokładnego opóźnienia zgodnie z podaną definicją.**

   W [a5r_punktualnosc.py:51](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_punktualnosc.py:51>) `date_diff('minute', scheduled_at, started_at)` liczy przekroczone granice minut. W tych danych do koszyka „15 minut” trafiają również opóźnienia sięgające 15 minut i 59 sekund. Takie wizyty powinny spełniać warunek „ponad 15 minut”.

   Moje przeliczenie dokładnej różnicy czasu daje dla pierwszych porannych wizyt u internisty w starych kampaniach:
   
   - okres 1: **170 / 2 656 = 6,40%**, zamiast 146 / 2 656 = 5,50%;
   - okres 2: **1 090 / 2 893 = 37,68%**, zamiast 1 045 / 2 893 = 36,12%.

   Zmieniają się również koszyki powrotów. Przy dokładnym czasie powrót po wizycie rozpoczętej do 5 minut po terminie wynosi **24,9% wobec 27,0%**. Dla opóźnienia ponad 30 minut wynosi **14,3% wobec 10,1%**.

   **Poprawka:** liczyć `epoch(started_at - scheduled_at) / 60.0`. Następnie przeliczyć koszyki, rozkład i wykrywanie zdarzeń. To ostatnie ma znaczenie: pierwszy podział serii opóźnień przesuwa się u mnie z **17 na 24 listopada 2025**. Dokładna zbieżność z datą skoku kampanii nie jest więc odporna na poprawienie definicji.

2. **Ważna — miesięczne 14,3%, 27,4% i 39,9% dotyczą wszystkich pacjentów, a nie pacjentów spoza nowych kampanii.**

   W [a5r_punktualnosc.py:161](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_punktualnosc.py:161>) miesięczny odsetek nie zawiera wykluczenia nowych kampanii. Raport prawidłowo odtwarza ten kod, ale liczby nie odpowiadają grupie wskazanej w pytaniu.

   Nawet zachowując dotychczasowe liczenie minut, dla pozostałych pacjentów otrzymuję **14,59% w listopadzie, 27,53% w grudniu i 40,84% w styczniu**. Przy dokładnej różnicy czasu jest to odpowiednio **15,74%, 29,73% i 42,60%**.

   **Poprawka:** pokazywać osobno wszystkich pacjentów oraz pacjentów spoza dwóch nowych kampanii. W notatce jednoznacznie podpisywać każdą serię.

3. **Ważna — 0,58 i 1,28 punktu procentowego są poprawnymi wynikami dotychczasowego rozkładu, ale nie wyodrębniają samej punktualności.**

   Niezależnie odtworzyłem **−0,5801** oraz **−1,2798 punktu procentowego**. Problem dotyczy opisu w [notatce:71](</C:/Users/K/Desktop/Zadanie - TM/notatki/a5_retencja.md:71>), a nie arytmetyki funkcji [rozklad():84](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_struktura.py:84>).

   Składnik „struktura” dla podziału **kampania × usługa × opóźnienie** obejmuje zmianę udziałów całych takich komórek. Zawiera zatem również zmianę struktury kampanii i usług. Dowód: bez opóźnienia składnik struktury wynosi **+0,1273 punktu** według pierwszego wejścia z rozstrzygnięciem kodem kampanii oraz **−0,6441 punktu** według sesji płatności.

   Różnica między rozkładami wynosi około −0,71 i −0,64 punktu. Ona również nie stanowi automatycznie czystego wkładu opóźnienia, ponieważ zmieniają się wspólne komórki i ich normalizacja. Ponadto **160 z 308 wspólnych komórek** pierwszego wariantu ma mniej niż 10 pacjentów w przynajmniej jednym okresie.

   **Poprawka:** napisać: „Przy podziale według kampanii, usługi i koszyka opóźnienia składnik zmiany struktury wynosi…”. Aby oddzielić punktualność, utrzymać stałe udziały kampanii i usług, a zmieniać wyłącznie rozkład opóźnienia wewnątrz nich. Brak odbytej wizyty pokazać osobno. Po poprawieniu czasu obecny składnik wynosi około **−0,61 oraz −1,28 punktu**.

4. **Ważna — porównanie z sekcji 3c nie utrzymuje „tego samego obciążenia” i silnie miesza obecność nowych kampanii z czasem.**

   [Kod:190](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_punktualnosc.py:190>) porównuje szerokie przedziały: do 4, od 5 do 9 oraz co najmniej 10 wizyt. Jedna i cztery wizyty należą do tej samej grupy. Godziny z nowymi kampaniami częściej pochodzą też z późniejszych miesięcy, kiedy opóźnienia są już wyższe.

   Dodatkowa kontrola pokazuje skalę problemu. Według dotychczasowej miary różnica między godzinami z nowymi kampaniami i bez nich wynosi ogółem **18,73 punktu procentowego**. Po porównaniu wewnątrz tego samego miesiąca i przy dokładnie tej samej liczbie wizyt, a następnie uśrednieniu wspólnych grup, pozostaje **3,68 punktu**. Kontrola obejmuje 72 grupy i 4 764 wizyty. Nie dowodzi zaniku związku, ale pokazuje znaczenie kalendarza i sposobu grupowania.

   **Poprawka:** zastąpić „przy tym samym obciążeniu” przez „w tych samych przedziałach liczby wizyt”. Dalsze porównanie powinno uwzględniać miesiąc, godzinę, dzień tygodnia, obsadę i zaległości z wcześniejszych godzin.

   Zdanie **„dane pasują do hipotezy, ale jej nie dowodzą” jest uprawnione**. Brakuje jednak liczby dostępnych lekarzy i ich identyfikatorów, obciążenia na lekarza, kolejki przed terminem oraz informacji o zasadach przydzielania wizyt. Alternatywą jest zmiana porannej obsady lub organizacji zapisów, która równocześnie zwiększyła opóźnienia i zbiegła się ze wzrostem kampanii.

   Opóźnienie może też odzwierciedlać cechy pacjenta: pilność potrzeby, wybór konkretnej godziny, dnia lub najbliższego terminu. Te cechy mogą niezależnie wpływać na powrót. Stała mediana czasu od płatności do terminu tego nie wyklucza. Najmocniejszym rozstrzygnięciem byłby proponowany losowy test zwiększenia porannej obsady.

5. **Ważna — kwoty „utraconej marży” są scenariuszem, a wariant sesji płatności używa niewłaściwej liczby pacjentów.**

   W [a5r_zdarzenia.py:244](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_zdarzenia.py:244>) wszystkie warianty mnoży się przez **17 419 pacjentów** starych kampanii według pierwszej reguły źródła. Według sesji płatności takich pacjentów w pełnym okresie 2 jest **19 500**. Przy zachowaniu pozostałych założeń 3,50 punktu oznaczałoby około **683**, zamiast 610 hipotetycznych powrotów mniej.

   Ważniejszy problem: różnica marży **95,58 zł** między powracającymi i niepowracającymi jest obserwacyjną różnicą między grupami. Nie jest oszacowaniem dodatkowej marży wywołanej odzyskaniem jednego powrotu. Sam raport to zastrzega, ale tabela w [notatce:96](</C:/Users/K/Desktop/Zadanie - TM/notatki/a5_retencja.md:96>) przedstawia wynik zbyt konkretnie jako wpływ opóźnień.

   **Poprawka:** opisać wyliczenia jako scenariusz przy założeniu przeniesienia różnicy retencji na cały rocznik oraz wartości 95,58 zł na dodatkowy powrót. Dopasować liczebność do reguły źródła. Do czasu wyodrębnienia punktualności nie nazywać 10–21 tys. zł jej kosztem.

6. **Ważna — wykrywanie podziałów jest rozsądną metodą eksploracyjną, ale statystyki nie mają pełnej interpretacji potwierdzającej.**

   Wzór w [a5r_zdarzenia.py:66](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_zdarzenia.py:66>) odpowiada różnicy średnich podzielonej przez niepołączony błąd standardowy. Dla odpowiednio dużych, niezależnych prób jest poprawnym przybliżeniem. Minimalne 28 dni po obu stronach jest zaimplementowane poprawnie; dodatkowo wymagane jest po 30 obserwacji.

   Próg 4 jest jednak arbitralnym progiem wykrywania. Kod przeszukuje wiele dat, wiele serii i kolejne fragmenty. Nie kalibruje wyniku na to przeszukiwanie, sezonowość ani zależność wizyt w tej samej godzinie lub u tego samego pacjenta.

   **Potwierdzam wyniki dla starych kampanii:**
   
   - powrót w 90 dniach: **2.03.2026, z = −3,9432**, poziomy 23,30% i 20,94%;
   - powrót w 30 dniach: **5.06.2025, z = −3,9678**.

   Oba wyniki są poniżej progu 4. Zapis „brak podziału” jest poprawny, choć warto podać trzy miejsca po przecinku, aby uniknąć pozornego konfliktu z zaokrągleniem do −4,0. Nie wynika z tego, że spadek musi być rozłożony w czasie — metoda mogła również nie wykryć słabszej zmiany skokowej.

   Jest też problem przypisania statystyk do sąsiednich poziomów w [notatce:96](</C:/Users/K/Desktop/Zadanie - TM/notatki/a5_retencja.md:96>). **z ≈ 54 porównuje 5,37% przed 17 listopada z 44,09% w całym późniejszym odcinku**, a nie bezpośrednio z 24,23% w pierwszym wydzielonym fragmencie.

   **Poprawka:** nazywać daty kandydatami zmian. Oddzielić statystykę używaną do znalezienia podziału od różnicy między końcowymi sąsiednimi odcinkami. Jeżeli potrzebne jest wnioskowanie statystyczne, skalibrować maksimum statystyki z uwzględnieniem zależności czasowych.

7. **Ważna — październik i luty są zgodne z brakiem zmiany, lecz różnicy lutego wobec marca–maja nie można po prostu nazwać szumem.**

   Potwierdzam przedziały rok do roku:
   
   - październik: **+1,32 punktu procentowego**, przedział 95% od −1,87 do +4,51;
   - luty: **+1,22 punktu**, przedział od −1,69 do +4,13.

   Można napisać, że nie wykryto zmiany w tych miesiącach. Nie można na tej podstawie stwierdzić, że zmiany nie było.

   Zdanie w [notatce:107](</C:/Users/K/Desktop/Zadanie - TM/notatki/a5_retencja.md:107>) pomija natomiast, że różnica **lutowego wyniku rok do roku** wobec analogicznej zmiany w marcu–maju wynosi **4,06 punktu**, przy błędzie standardowym 1,73 punktu. Przy tej samej metodzie normalnej daje to **z = 2,35**, nominalne **p = 0,019** i przedział od **0,67 do 7,44 punktu**.

   **Poprawka:** napisać: „Luty różni się od marca–maja w nominalnym porównaniu. Ponieważ miesiące wybrano po obejrzeniu wyników i wykonano wiele porównań, wynik pozostaje eksploracyjny”. To rzeczywista niespójność z prostą hipotezą „większe opóźnienia zawsze oznaczają niższy powrót”.

8. **Drobna — limit czterech podziałów oznacza w kodzie cztery poziomy rekurencji.**

   Warunek w [a5r_zdarzenia.py:56](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_zdarzenia.py:56>) pozwala na maksymalnie **15 podziałów**, a nie cztery. W obecnych raportach limit nie został przekroczony, więc nie zmienia to przedstawionych wyników.

   Ponadto [wybór kandydata:98](</C:/Users/K/Desktop/Zadanie - TM/analiza/a5r_zdarzenia.py:98>) przeszukuje również podfragmenty przy progu zero. Ogólnie nie musi zwrócić najlepszego podziału całej serii. W sprawdzonych seriach starych kampanii zwrócił właściwego kandydata.

   **Poprawka:** zastosować wspólny licznik zaakceptowanych podziałów. Najsilniejszego kandydata całej serii pobierać bez rekurencji.

Poniżej porównanie liczb. Wartości rozdzielone strzałką oznaczają okres 1 → okres 2. „Dokładny czas” oznacza rzeczywistą różnicę znaczników czasu.

| Miara | Wasz wynik | Moje niezależne przeliczenie |
|---|---|---|
| Pierwsza wizyta rano u internisty: ponad 15 minut, stare kampanie | 5,5% → 36,1% | **6,40% → 37,68%**; 170/2 656 → 1 090/2 893 |
| Powrót w 90 dniach po pierwszej wizycie rano, stare kampanie | 23,6% → 19,0%; kohorty 2 844 → 3 117 | **23,63% → 19,02%**; 672/2 844 → 593/3 117 |
| Analogiczny powrót wieczorem | 23,5% → 23,5% | **23,47% → 23,52%**; 907/3 864 → 1 008/4 286 |
| Powrót rano, opóźnienie do 5 minut | 24,9% → 26,5% | **24,88% → 27,00%**; 352/1 415 → 223/826 |
| Powrót rano, opóźnienie ponad 30 minut | 15,2% → 9,8% | **14,29% → 10,13%**; 5/35 → 54/533 |
| Obciążenie porannej godziny z przynajmniej jedną nieanulowaną wizytą | 2,73 → 4,43 wizyty | **2,7262 → 4,4320**; 1 965 → 2 125 godzin |
| Zwroty po odbytych wizytach L4, nowe kampanie / pozostali, okres 2 | 17,4% / 5,3% | **17,37% / 5,31%**; 1 024/5 895 oraz 270/5 080 |
| Marża dni 1–180, powrót w 90 dniach / brak powrotu, okres 1 | 98,9 zł / 3,3 zł | **98,9045 zł / 3,3231 zł**; 3 830 oraz 12 401 pacjentów |

Miesięczne odsetki porannych wizyt u internisty opóźnionych ponad 15 minut pokazuję z rozdzieleniem obu źródeł rozbieżności: grupy pacjentów oraz sposobu liczenia czasu.

| Miesiąc terminu | Wasz raport: wszyscy pacjenci | Mój wynik: poza nowymi kampaniami, dotychczasowa miara | Mój wynik: poza nowymi kampaniami, dokładny czas |
|---|---:|---:|---:|
| X 2024 | 5,6% | 5,64% | 6,77% |
| XI 2024 | 4,9% | 4,86% | 5,14% |
| XII 2024 | 5,5% | 5,54% | 6,70% |
| I 2025 | 6,1% | 6,06% | 6,71% |
| II 2025 | 4,7% | 4,72% | 6,01% |
| III 2025 | 6,4% | 6,37% | 6,95% |
| IV 2025 | 4,9% | 4,91% | 5,93% |
| V 2025 | 5,7% | 5,71% | 6,59% |
| VI 2025 | 4,1% | 4,07% | 4,71% |
| VII 2025 | 4,8% | 4,79% | 5,25% |
| VIII 2025 | 5,0% | 4,95% | 5,20% |
| IX 2025 | 4,9% | 4,88% | 5,52% |
| X 2025 | 5,0% | 4,96% | 5,15% |
| XI 2025 | 14,3% | 14,59% | 15,74% |
| XII 2025 | 27,4% | 27,53% | 29,73% |
| I 2026 | 39,9% | 40,84% | 42,60% |
| II 2026 | 46,6% | 46,49% | 49,43% |
| III 2026 | 46,8% | 46,15% | 47,75% |
| IV 2026 | 49,6% | 51,10% | 52,28% |
| V 2026 | 46,3% | 46,88% | 48,63% |
| VI 2026 | 50,6% | 50,21% | 52,50% |
| VII 2026 | 47,0% | 45,31% | 47,32% |
| VIII 2026 | 50,3% | 50,55% | 52,75% |
| IX 2026 | 48,2% | 49,89% | 51,58% |