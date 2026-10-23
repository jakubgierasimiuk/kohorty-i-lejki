# Runda G: przejrzystość zakładek 2–9 (2026-10-23)

Sesja `local_01c85eb0` (Claude Code, Opus 5.5). Równolegle sesja `local_975acd06` przebudowywała pierwszą zakładkę („Czy to wzrost”). Podział plików był uzgodniony między sesjami (opis niżej, punkt 6).

## 1. Polecenie Kuby (dosłownie)

> Przejrzałem zakładkę „Kohorty” jak ktoś z Telemedi i układ jest do przebudowy. Zakładka nazywa się „Kohorty”, a pierwsze dwa ekrany to tabela zdarzeń z kwotami i priorytetami, więc kohort nie widać bez przewijania. Filtry wiszą osobno, choć sterują wykresem pod nimi. Wniosek o powrotach stoi w środku, między rzeczami zależnymi od filtrów, choć sam od nich nie zależy. Mapa kohort, czyli to, czego każdy tu szuka, jest prawie na dole. Tabela „Kohorty w podziale” jest nieczytelna. Proszę o zmiany w tej kolejności: (1) tabela zdarzeń do „Zdarzeń” jako pierwsza karta, odnośniki w „Czy to wzrost” i „Kohortach”; (2) nowa kolejność „Kohort”: wniosek z hantlami krótko, pasek „Pacjenci w analizie” z „Przywróć domyślne”, mapa kohort z krótkimi nazwami zdarzeń, jedna karta „dzień po dniu” ze sterowaniem w nagłówku, zdarzeniami jako przyciskami 60 dni przed i po i tabelą grup, krzywa powrotu na końcu; przy każdej karcie zależnej od ustawień linijka, od których; (3) domyślnie przyczyny na wykresie kohort, bez godziny bez danych i duplikatów na liście porównań; (4) tabela grup od nowa: jedna miara, liczba pacjentów raz na wiersz, okresy słowami, zmiana z jednostką, „Wszyscy wybrani pacjenci”, bez przewijania w bok przy 1366 px, kolor tylko przy zmianie większej niż przypadek (sprawdzić kodem przypadek „godziny bez danych” w podziale na pierwszą usługę), to samo w tabeli lejka; (5) „Przywróć domyślne” także w „Lejku”. Na koniec sprawdzenie w przeglądarce (1366 i 1920 px, telefon, tryb ciemny), kontrola liczb i odnośniki. Nic nie publikuj.
>
> Generalizując — mam poczucie, że za mocno skupiliśmy się na kwestiach liczbowych, a za mało na przejrzystości i czytelności dashboardu. Wyciągnij wnioski z powyższych zmian i przeanalizuj wszystkie pozostałe zakładki pod podobnym kątem, wprowadź zmiany, które uważasz za stosowne, ocenię je na żywo po zmianach. Do wnioskowania użyj wsparcia Astry i Fable.
>
> (dopisek) Nie zajmuj się pierwszą zakładką — do niej piszę uwagi oddzielnie.

## 2. Recenzje Astry i Fable

Obie dostały to samo polecenie (`notatki/recenzje/g_przejrzystosc_polecenie.md`): uwagi Kuby jako wzorzec, 58 zrzutów zakładek 2–9 przy 1366 px, pełne teksty stron i szkielet HTML. Każda pracowała niezależnie i nie widziała odpowiedzi drugiej. Astra: Codex `-p astra` (model `gpt-6-astra`), jedno wywołanie. Fable: agent w sesji (`model: fable`), który dodatkowo sprawdził działającą stronę w Edge bez okna. Odpowiedzi: `notatki/recenzje/g_astra_odpowiedz.md`, `notatki/recenzje/g_fable_odpowiedz.md`.

**Na czym się zgadzają:**
- Zasady wspólne: zakładka otwiera się tym, co obiecuje jej nazwa. Treść niezależna od ustawień stoi nad paskiem ustawień, zależna pod nim. Sterowanie stoi przy tym, czym steruje, a każda karta zależna od ustawień mówi, od których. Tabela pokazuje jedną miarę naraz, okresy słowami, a kolor oznacza tylko zmianę większą niż przypadek. Każdy widok da się przywrócić do ustawień startowych.
- „Lejek”: kroki lejka za daleko od początku; tabela szersza niż ekran (ucięta najważniejsza kolumna „Sesja do płatności”); kolor przy szumie (np. Opera); filtry daleko od tabeli; brak przycisku powrotu.
- „Po zakupie”: kolorowy szum w tabelach (np. średnia ocena „−0,02 gorzej”); karta zwrotów przerywa wątek opóźnień; tabela zwrotów ucięta.
- „Zdarzenia”: tabela z „Kohort” na górę; opisy zdarzeń krócej; różne brzmienia odnośników.
- „Wynik biznesu”: jedna karta na cztery ekrany; 14 linii zdarzeń na wykresach i lista powtórzona dwa razy; tabela miesięcy powinna być zwinięta; tabela ekonomii szersza niż ekran.
- „Priorytety” i „Czego nie wiemy”: zasady listy zwinięte, nazwy zamiast „punkt 6”, „—” zamiast słów, stopki z wewnętrznymi ścieżkami.

**Gdzie się różnią i co wybraliśmy:**
- Etykieta „Najbardziej obniża płatności”: Astra radziła ją zmienić, bo jej zdaniem brzmi przyczynowo. Fable wskazała ją jako wzór do zachowania. Zostaje, bo opisuje rachunek (największy względny spadek przejścia), a nie przyczynę.
- „Po zakupie”: Astra proponowała przenieść zwroty wyżej, Fable na koniec. Wybraliśmy wariant Fable, bo zachowuje ciągłość wątku opóźnień: punktualność → godziny → ruch → powrót → oceny → zwroty.
- „Lejek”, miejsce wykresu udziału nowych kampanii: Fable proponowała go w karcie wniosku, Astra w wyjaśnieniu. Trafił do sekcji „Co już rozpoznaliśmy w lejku”, pod paskiem i poza jego zasięgiem, bo nie zależy od ustawień.

## 3. Co zmieniliśmy

**Kohorty** (lista Kuby, punkty 1–5):
- Kolejność: wniosek (tytuł, zdanie, hantle; reszta w „Szczegółach”) → pasek „Pacjenci w analizie” (przypisanie źródła, zawężenia jako etykiety z „×”, „Dodaj zawężenie”, „Przywróć domyślne”, liczba pacjentów) → mapa kohort (ostatnia kolumna: krótkie nazwy zdarzeń) → „Dzień po dniu” (miara, okno, wygładzenie, podział, porównanie w nagłówku; przyciski zdarzeń; tabela grup) → krzywa powrotu. Pasek jest przyklejony tylko nad kartami, którymi steruje.
- Przyciski zdarzeń ustawiają porównanie 60 dni przed i po. Jedno zdanie liczone w przeglądarce mówi, jak zmieniła się wybrana miara dla wszystkich wybranych pacjentów, czy zmiana jest większa niż przypadek i w ilu grupach tabeli zmiana jest wyraźna.
- Tabela grup: jedna miara (ta z wykresu) albo „wszystkie okna” (w komórce zmiana, wartości w podpowiedzi). Kolumny: grupa, pacjenci „rok wcześniej → ostatnie 12 miesięcy” (liczebność wybranej miary, czyli kohorty z pełnym oknem), wartość w obu okresach, zmiana z jednostką. Wiersz sumy nazywa się „Wszyscy wybrani pacjenci”.
- Okresy słowami także w krzywej powrotu i w polach własnych dat („Wcześniejszy okres”, „Późniejszy okres”).

**Lejek:** wniosek krótko; pasek „Sesje w analizie” (kto, typ sesji, podział, porównanie, „Przywróć domyślne”; pola dat tylko przy „Własne daty”) → kroki lejka („Grupa pokazana w lejku”) → „Dzień po dniu” z przyciskami zdarzeń i tabelą grup (jak w „Kohortach”, tryb „wszystkie kroki”) → „Co już rozpoznaliśmy w lejku” (Safari, przeglądarki w aplikacjach, udział nowych kampanii; stałe porównania).

**Zdarzenia:** pierwsza karta to tabela „co zmieniło kohorty i wynik” (dane przeniesione z `kohorty.js` do `zdarzenia.js`). Wstęp wpisany w kartę osi. Opisy zdarzeń są zwijanymi pozycjami. Odnośniki mają jedno brzmienie („Pokaż w zakładce „…””), a odnośniki do „Po zakupie” i „Jakości danych” prowadzą do konkretnej karty.

**Wynik biznesu:** cztery karty zamiast jednej: wniosek, kwartały rok do roku (stałe porównanie), marża i wydatki w czasie (grupowanie w nagłówku, tabela miesięcy zwinięta), ekonomia kampanii. Na wykresach jest 5 zdarzeń, które mogły zmienić wynik (starty kampanii, awaria Safari, spadek konwersji kampanii na markę), zamiast 14, i jedna lista pod drugim wykresem. Tabela ekonomii pokazuje tylko okno wybrane przełącznikiem.

**Po zakupie:** kolejność kart (zwroty na końcu); kolor zmiany tylko przy wyraźnej zmianie (średnia ocena bez oceny); legenda pod tabelami; tabela punktualności idzie za wybraną specjalizacją (wszystkie po kliknięciu); kwoty zwrotów w osobnej, zwiniętej tabeli; na wykresach starty kampanii i zmiany obsługi pacjenta.

**Priorytety, Czego nie wiemy, Jakość danych:** zasady listy zwinięte nad przeglądem; nagłówki grup między kartami; przy kartach pytania „Czego nie wiemy” zamiast numerów; „Bez osobnej pozycji na liście” zamiast „—”; filtr „Wszystkie pytania — 21”; stopki ze ścieżkami w zwiniętej sekcji „Skąd liczby w tej zakładce”; „Szczegóły”, w których są same źródła, nazywają się „Skąd liczby”.

**Na całej stronie:** podpisy na końcach linii wykresów do 34 znaków zamiast 22; na telefonie pasek ustawień nie jest przyklejony, bo zajmowałby piątą część ekranu.

## 4. Czego nie zmieniliśmy (i dlaczego)

- Liczby i wnioski: bez zmian (ramy rundy: przejrzystość, nie nowe analizy). Teksty zmieniły tylko miejsce (z treści do „Szczegółów”) albo brzmienie odnośników.
- Treść tabeli zdarzeń (gęstość, nazwa kolumny „Skutek w złotych”): bez zmian, bo była przyjęta przez Kubę i sprawdzona przez Codeksa w rundzie F. Zmieniło się tylko jej miejsce.
- Grupy tematyczne w „Czego nie wiemy” (propozycja Fable): Kuba zdecydował „pogrupuj” i grupy są zrobione (założenie 95, `DECYZJE.md`). Trzykolumnowy widok z rozwinięciami (propozycja Astry) nie był robiony.
- Łączenie kart przyczyna–skutek w „Zdarzeniach” (Fable): też zmiana treści, do decyzji Kuby.
- Pierwsza zakładka: zgodnie z dopiskiem Kuby nie ruszaliśmy jej poza odnośnikiem do tabeli zdarzeń.

## 5. Kontrole

- `analiza/g_istotnosc.py`: Python odtwarza tabele grup z tych samych plików danych co strona i sprawdza istotność każdej komórki. Wynik: `analiza/wyniki/g_istotnosc.txt`; liczby w `ZNALEZISKA.md`, sekcja z 2026-10-23 (runda G).
- Strona wobec Pythona (skrypt w folderze roboczym sesji): kolor każdej komórki i zmiana. W „Kohortach” zgodne są 2 + 2 komórki przy ustawieniach domyślnych i 32 + 16 w przypadku Kuby. W „Lejku” zgodne są 54 komórki przy ustawieniach domyślnych i 54 w przypadku godziny bez danych. Niezgodnych: 0. W przypadku Kuby nie ma żadnej kolorowej komórki.
- Zachowanie: czysty adres na starcie, „Przywróć domyślne” nieaktywny bez zmian, po zmianie aktywny i czyści adres; przyciski zdarzeń ustawiają 60 dni przed i po; pasek przyklejony pod nagłówkiem; tabele grup mieszczą się przy 1366 px; 0 błędów w konsoli.
- Komplet kontroli po wspólnym eksporcie: `PRZEKAZANIE.md`.

## 6. Podział plików z sesją pierwszej zakładki

Ta sesja: `narzedzie/index.html`, `app.js`, `widoki.js`; dopiski w `karty.js` i `styl.css` (na końcu); w `widoki_c.js` tylko funkcje priorytetów i niewiadomych; `analiza/e_teksty_zakladki.py`; w `analiza/e_teksty.py` tylko `karty_lejka()` i odnośnik do tabeli zdarzeń; skrypty kontroli (`f_wykresy_tekst.py` poza `kontrola_wzrost()`, `f_odnosniki.py`, `e_przegladarka.py`, `b2_teksty_strony.py`, `f_kontrast.py`, `f_publikacja.py`); `analiza/g_istotnosc.py`; wiersze zakładek 2–9 w README. Sesja `local_975acd06`: pierwsza zakładka (`wzrost()` w `e_teksty.py`, `widoki_c.js` poza funkcjami wyżej, `analiza/g_werdykt.py`, streszczenie README). Założenia: ta sesja 87–90, tamta od 91. Eksport i komplet kontroli robimy raz, po obu zmianach.
