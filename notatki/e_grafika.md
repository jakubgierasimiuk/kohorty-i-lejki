# E — dopracowanie grafiki narzędzia (sesja „E: grafika”, 2026-10-22)

**Zlecenie:** sesja prowadząca (`local_1bf06826`) uruchomiła tę sesję, żeby razem z Kubą dopracować narzędzie od strony graficznej: ta sesja projektuje i wprowadza zmiany wyglądu, Kuba mówi, co zmienić, i ocenia. Pliki tej sesji: `narzedzie/index.html`, `styl.css`, `app.js`, `widoki.js`, `widoki_c.js`, `karty.js`, nowe pliki w `narzedzie/` poza `dane_strony/`, `analiza/e_przegladarka.py`, `analiza/b2_teksty_strony.py`, ta notatka i katalog `notatki/e_grafika_rundy/`. Teksty, liczby i dane strony zostają w rękach sesji prowadzącej.

Do commita `351f556` (trzecia lista Kuby w sesji `local_61aff6c2`) ta sesja nie zmieniała plików projektu — tylko czytała kod i oglądała stronę.

## 1. Przegląd obecnej strony (etap 0)

`python -I analiza/e_przegladarka.py --wyjscie <katalog tymczasowy>` na stanie sprzed `351f556`: 9 zakładek przy 1366 i 375 px, 0 błędów w konsoli, brak przewijania w bok, 296 odnośników działa. Zrzuty pocięte na ekrany i obejrzane. Pięć rzeczy, które najbardziej odstawały (wysłane Kubie):

1. Lejek: filtry i wykres kroków są około ekranu niżej, pod kartą nagłówka i dwiema kartami napraw.
2. Oś zdarzeń: same numery na jednakowych kropkach, numery nachodzą na siebie („3 5”, „9 10”); to samo na liniach zdarzeń na wykresach dziennych.
3. Wykresy liniowe z domyślną legendą biblioteki („Dzień: — □ Przychód: —”, „Dzień:” także przy grupowaniu miesięcznym).
4. Szerokie tabele: tabela kwartałów w „Wyniku biznesu” i tabela kohort obcięte już przy 1366 px; wąskie tabele rozciągnięte na całą szerokość.
5. Płaska hierarchia kart: wszystkie odnośniki podkreślone, nierówne wysokości kart obok siebie, ścieżki plików widoczne w kartach zdarzeń.

## 2. Narada modeli: jak przedstawić graficznie cały projekt (polecenie Kuby)

**Słowa Kuby:** „zaangażuj fable sol i astrę, usatlcie wspólną wersję jak przedstawić graficznie cały projekt/deliverables aby były 1. zgodne ze sztuką 2. maksymalnie czytelne 3. dodajcie gdzie się da graficzną reprezentacje danych 4. przeanalizujcie w jaki sposób (wykresy, wykresy kołowe, infografiki) wspomóc odbiór danych i poprawić czytelność analizy. UI i kolorystyka, układ oddawanego produktu: wykorzytaj impeccable z innych projektów by poprawić warstwę wizualną.”

**impeccable:** zasady projektowania interfejsów z innego projektu Kuby (`C:\Users\K\Desktop\CLAUDE\learn-ai-tutor-math\.claude\skills\impeccable`, wersja 4.3.1). Na prośbę Kuby przeczytane stamtąd tylko pliki tych zasad (SKILL.md, operate, craft-floor, layout, colorize, typeset, visualize, nagłówki critique); żadnych innych plików tamtego projektu. Do briefu weszły: tryb „Operate” z elementami „Read”, powściągliwy kolor, jedna rodzina pisma i stała skala ról, test zmrużonych oczu, lista odrzucanych wzorców (karty w kartach, kolorowa ramka po lewej, mini-wykresy dla ozdoby, znaki Unicode zamiast ikon), heurystyki Nielsena i obciążenie poznawcze. Automatyczny detektor impeccable (`impeccable detect`) uruchomiony na **kopii** kodu strony w katalogu tymczasowym, żeby nic nie zapisał w projekcie: 0 uchybień.

**Przebieg:**
- Brief (`e_grafika_rundy/brief.md`): zlecenie Kuby, kto ogląda produkt, stan obecny, twarde ograniczenia (strona statyczna, nic z sieci, liczby tylko z eksportu, kolory stanu z ikoną i słowem, telefon), zasady impeccable i dataviz, struktura odpowiedzi A–G, w załączniku kształt danych strony (klucze i typy, bez wartości). Do tego 24 zrzuty ekranu (komputer i telefon).
- Runda 1, niezależnie i równolegle: Fable (agent Claude, `model: fable`), Sol (`codex exec -p review`, gpt-6.1-sol), Astra (`codex exec -p astra`, gpt-6-astra), plus własna propozycja tej sesji napisana przed przeczytaniem pozostałych. Pliki `r1_propozycja_*.md`.
- Synteza `wspolna_v1.md` z czterema rozwidleniami.
- Runda 2: każdy z trzech recenzentów ocenił v1 (sprzeciwy z poprawką, głos w rozwidleniach, braki, kolejność etapów). Pliki `r2_ocena_*.md`.
- Wersja końcowa `wspolna_v2.md`.

**Twierdzenia recenzentów sprawdzone w kodzie przed syntezą:**
- kolory serii zależą od kolejności zaznaczenia, a nie od grupy (`przydzielKolory` w `app.js`, `przydziel` w `widoki.js`) — potwierdzone;
- mapa kohort ma osobną skalę kwantylową dla każdej kolumny (`rysujMacierz` w `widoki.js`) — potwierdzone;
- na telefonie oś zdarzeń to pomniejszona miniatura wersji z komputera — potwierdzone na zrzucie 375 px;
- wykresy mają minimalną szerokość 320 px (`Math.max(320, …)` w czterech miejscach) — potwierdzone;
- pierwsza zakładka nie ładuje `kohorty.js` (dane podziałów i kohort wczytywane dopiero po wejściu w zakładkę) — potwierdzone w `index.html`, dlatego „Więcej pacjentów” i 180 dni na pierwszej zakładce wymagają eksportu;
- klucze danych wskazane w propozycjach istnieją (`wzrost.retencja.okna` z oknami 30/60/90, `lejek_naglowek.safari`, `wynik.ekonomia.wiersze`, `jakosc.mostek.kroki`, `zdarzenia.lista` z polami `obszar`, `rodzaj`, `krotko`).

**Wynik (szczegóły w `wspolna_v2.md`):** identyfikacja zostaje; porównania „przed → po” jako hantle; wykresy dzienne z wyróżnieniem jednej serii, własną legendą z wyborem serii i zdarzeniami tylko z obszaru wykresu; „Wynik biznesu” jako dwa wykresy (marża przed kosztem kampanii i wydatki, pod nimi marża po kosztach); ekonomia kampanii jako punkt wyniku względem zera z dwoma symbolami reguł; mapa kohort z legendą i tokenami. Zero wykresów kołowych; bez Sankeya, wodospadów rozkładów opisowych, wykresu kwot priorytetów i dwóch osi. Etapy 1–5, każdy z warunkami odbioru (w tym nowa kontrola zgodności liczb na wykresach z tekstem karty w `e_przegladarka.py`).

**Czeka na decyzję Kuby (R1–R3):** skala mapy kohort (wspólna czy osobna dla okna; rekomendacja: wspólna z jawnymi progami), zakładki na telefonie (przycisk z listą czy widoczne pigułki z przyciskiem po przewinięciu), słowo „lepiej/gorzej” przy etykiecie zmiany (zawsze widoczne czy tylko poza gęstymi tabelami).

**Koszt:** 6 wywołań (Codex: 2 × Sol, 2 × Astra; Fable: 2), wszystko w ramach subskrypcji, bez OpenRoutera.

## 3. Propozycje dla sesji prowadzącej (pliki poza tą sesją)

- Zmiany wymagające eksportu (etap 5 w `wspolna_v2.md`): powrót po 180 dniach i liczby „Więcej pacjentów” w danych pierwszej zakładki; liczby TelemediGO (trzy sposoby zakupu, oba lata) jako pola liczbowe; przeglądarki w aplikacjach (6 liczb); opóźnienia według godziny jako liczniki i mianowniki; podpisy grup priorytetów.
- README: na górze prawdziwy link; jeden zrzut „Czy to wzrost” w repozytorium (z opisem alternatywnym, robiony skryptem, z datą i commitem); opcjonalnie diagram Mermaid drogi pracy bez liczb.
- Wpisy do wspólnych notatek dopiero po decyzji Kuby w R1–R3.
