# Decyzje

Decyzje podjęte w trakcie pracy (metoda, podziały, narzędzie, hosting) — co wybraliśmy, dlaczego i jakie były alternatywy.

## 2026-10-19 — plan pracy i sposób współpracy

**Decyzja:** pracujemy według planu z `notatki/PLAN.md` (wersja 2, zatwierdzona przez Kubę). Kolejność: wstępna analiza → narzędzie → uzupełnienie analizy → weryfikacja.

**Dlaczego tak:** pierwsza wersja planu zakładała, że Claude wykona całą analizę samodzielnie, a narzędzie zbuduje równolegle z analizą. Kuba ją odrzucił:
- wnioski wyciągamy razem — Claude liczy i pokazuje, po każdym większym kroku jest przegląd, a wnioski weryfikuje konsylium;
- narzędzie dopiero po wspólnym pierwszym etapie analizy, żeby budować je na sprawdzonych definicjach;
- przed rozpoczęciem każdego punktu Kuba decyduje, czy idziemy dalej;
- bez dat w planie.

**Co Kuba dodał do treści planu:** dokładne odtworzenie liczb dashboardu (a nie „mniej więcej”) i zestawienie ich z miarami po oczyszczeniu; rozszerzona kontrola jakości (duplikaty w każdej tabeli osobno, profil zamówień TEST-QA, kliknięcia wobec sesji, czas zamówień wobec czasu płatności); wspólne ustalenie definicji z wariantami przed kohortami; opis obejścia pułapek (start od zera, młode kohorty, sezonowość); analiza tego, co dzieje się po zakupie; wartość priorytetów w marży; stała zasada „najpierw napraw, potem wyłączaj” (dopisana do CLAUDE.md, punkt 9).

**Wykonanie:** osobna sesja Claude Code prowadzi plan punkt po punkcie, w tym samym folderze projektu.

## 2026-10-19 — budowa bazy danych (punkt A1)

**Decyzja:** jedna baza DuckDB `analiza/telemedi.duckdb`, odtwarzana od zera skryptem `python -I analiza/a1_baza.py`. Plik bazy jest poza repozytorium (`.gitignore`), tak jak surowe dane. W repozytorium są skrypt i raport z kontroli.

**Jak zbudowana:**
- Schemat `surowe`: sześć tabel o nazwach jak w słowniku danych (`users`, `sessions`, `events`, `orders`, `go_memberships`, `marketing_spend`). Pliki kwartalne sesji i półroczne zdarzeń są połączone w jedną tabelę.
- Każda kolumna ma typ podany jawnie w skrypcie. Pliki są czytane jako tekst i dopiero potem zamieniane na typy, bez zgadywania. Wartość, której nie da się zamienić, zatrzymuje skrypt z błędem, zamiast po cichu zamienić się w pustą.
- Przy każdym wierszu zostaje plik źródłowy i numer linii w pliku. Będą potrzebne w punkcie A2 do szukania duplikatów na stykach plików kwartalnych i półrocznych.
- Tabela `surowe.pliki`: liczba wierszy, rozmiar i skrót SHA-256 każdego pliku.

**Dlaczego przeliczenie czasu sprawdzamy drugim sposobem (A1):** czas polski liczy DuckDB. Skrypt przelicza ten sam czas jeszcze raz w Pythonie (moduł `zoneinfo`) i porównuje oba wyniki wiersz po wierszu. Wynik: zero różnic w 459 557 sesjach i 494 605 zdarzeniach.

## 2026-10-19 — czyszczenie danych po przeglądzie jakości (punkt A2)

**Decyzja Kuby:** przyjęte obie propozycje z raportu jakości danych (`analiza/wyniki/a2_jakosc.txt`):
- ze zdublowanych zamówień zostaje jedna kopia (604 zamówienia z okna 10–24.06.2026);
- 22 konta testowe są wyłączone ze wszystkiego: zamówień, pacjentów, przychodu, sesji i lejka; kosztu lekarza za testy nie liczymy, wariant z kosztem idzie na listę niewiadomych.

**Zastrzeżenie Kuby:** zamówieniom testowym przyglądamy się jeszcze raz dokładnie na końcu pracy. Dopisane do planu jako pierwszy krok punktu D.

**Jak wykonane:** dane surowe zostają nietknięte w schemacie `surowe`. Oczyszczona kopia powstaje obok, w schemacie `czyste` (skrypt `analiza/a2_czyste.py`). Dzięki temu w A3 da się porównać dashboard liczony na surowo z liczbami po oczyszczeniu, a każdą decyzję o czyszczeniu można cofnąć bez ponownego ładowania danych.

**Otwarte po przeglądzie (czekają na Kubę):** jak czytać sesje zalogowane od wejścia, które nigdy nie kończą się zakupem; jak wyznaczyć okres rozruchu, skoro START10 działa przez całe dwa lata (zmiana w planie, punkt A5); kody rabatowe jako stała kwota w złotych.

## 2026-10-19 — trzy otwarte sprawy z przeglądu A2

**Decyzja Kuby:** przyjęte wszystkie trzy propozycje, z dopiskami. Założenia: `ZALOZENIA.md`, punkty 10–15. Zmiany w planie: A4 (źródło pozyskania i prowizja), A5 (lejek, komunikacja po zakupie, pułapki), C (lista niewiadomych).

1. **Sesje zalogowane od wejścia.** Osobny wiersz w lejku, newsletter i SMS oceniane na poziomie pacjenta. Dopisek Kuby: wyjaśnienie nadal niepełne. Rozważamy trzy odczytania: zepsuta ścieżka zakupu dla zalogowanych, inny cel wizyty albo sposób pomiaru (krok logowania zapisywany każdemu przy kasie). Pogłębienie w A5: na którym kroku odpadają, z jakich stron i kampanii przychodzą (np. przypomnienie o recepcie), czy kupują potem rzadziej niż podobni pacjenci, czas między wyborem terminu a krokiem logowania. Zepsuta ścieżka uderzałaby wyłącznie w powracających, czyli w retencję. Dlatego na liście niewiadomych będą oba odczytania, test rozstrzygający i wartość wariantu pesymistycznego w marży.
2. **Okres rozruchu.** Zgoda na zmianę w A5: nie wyznaczamy okresu rozruchu kodem START10. Dopisek Kuby: nie przesądzamy, że wzrost od października do stycznia to sezon infekcji, bo w tym samym czasie rosną wydatki na kampanie. Sezon i wydatki rozdzielamy w A5.
3. **Kody rabatowe.** Zgoda. Kody kampanii służą jako kontrola reguł przypisania źródła w A4. Dopisek Kuby: prowizję dla rankingu liczymy tą samą regułą co źródło pozyskania, drugi wariant jedną liczbą obok. Jeśli różnica jest mała, nie poświęcamy temu więcej czasu.

**Korekta po uwadze Kuby:** w rozmowie napisałem, że wzrost liczby nowych pacjentów od października 2024 do stycznia 2025 „pasuje do sezonu infekcji”. To było za szybkie. W tej samej tabeli rosną wydatki na kampanie, więc przyczyna jest otwarta.

## 2026-10-19 — wynik odtworzenia dashboardu (punkt A3)

**Decyzja Kuby:** wynik A3 przyjęty. Jako sposób liczenia dashboardu przyjmujemy najprostszą z 14 pasujących kombinacji. Każdy wiersz pliku zamówień to zamówienie, z duplikatami i z testami. Przychód z konsultacji to suma zapłat bez TelemediGO i bez odejmowania zwrotów. Nowy pacjent to konto z pierwszym zamówieniem. Granice okresów są w czasie polskim. Pozostałe pasujące kombinacje różnią się od niej najwyżej o 0,64 punktu procentowego w każdej miarze.

## 2026-10-19 — higiena kontekstu i praca w wielu sesjach

**Decyzja Kuby:** jedna sesja nie przekracza 60% dostępnego kontekstu. Nowy punkt planu albo duże przeliczenia najchętniej robimy w nowej sesji. Sesje komunikują się przez `notatki/PRZEKAZANIE.md`. Zasada jest w `CLAUDE.md`, punkt 14. Sesja prowadząca decyduje na bieżąco, czy zostaje przy punkcie, czy uruchamia nową sesję.

**Pierwsze zastosowanie:** punkt A4 robi nowa sesja. Ta sesja prowadziła A1–A3 z dużymi wydrukami, a A4 to nowy punkt, który wymaga uważnej, wspólnej pracy nad definicjami.

## 2026-10-19 — definicje przed kohortami (punkt A4)

**Decyzja Kuby:** przyjęte definicje z `ZALOZENIA.md`, punkty 16–26. Warianty i ich wpływ policzył `analiza/a4_definicje.py` (raport `analiza/wyniki/a4_definicje.txt`). Pracę prowadziła osobna sesja, zgodnie z zasadą higieny kontekstu.

| Sprawa | Przyjęte | Odrzucone warianty | Dlaczego |
|---|---|---|---|
| Nowy pacjent | pierwsze opłacone zamówienie, dowolny status; status pierwszego zamówienia jako podział kohort | pierwsza jakakolwiek płatność (daje to samo), pierwsze nieanulowane, pierwsza odbyta wizyta | Najbliżej słów zadania: dashboard („pacjenci z pierwszym zakupem”), słownik zamówień i reguła prowizji. Warianty zmieniają wzrost najwyżej o 0,5 punktu procentowego. Status pierwszej wizyty różnicuje powroty, więc lepiej go pokazywać niż wycinać. |
| Powrót | kolejne zamówienie nieanulowane, okna 30/60/90 dni | każde kolejne opłacone, kolejna odbyta wizyta | Anulacja to pełny zwrot przed wizytą, więc pacjent nic nie kupił. Nieodebrana wizyta to zapłata, która zostaje. |
| TelemediGO jako powrót | nie, mierzone osobno | tak | W obecnych danych bez wpływu. Odrębna miara jest czytelniejsza. |
| Przychód | po zwrotach, TelemediGO osobno, zwrot w dniu płatności | przed zwrotami (jak dashboard) | Standard z `CLAUDE.md`, punkt 9. Słownik oddziela TelemediGO od konsultacji. Daty zwrotu w danych nie ma. |
| Źródło pozyskania | pierwsze wejście z anonimowymi sesjami przeglądarek pacjenta; kod kampanii rozstrzyga | pierwsze wejście bez kodu, ostatnie oznaczone wejście, sesja płatności | Najwyższa zgodność z kodami kampanii (97% wobec 67–81%). |
| Prowizja afiliacyjna | ta sama reguła co źródło: 30 825 zł za dwa lata | sam kod RANKING10: 14 875 zł, pokazywany obok jedną liczbą | Zasada z A2. Różnica 15 950 zł to 0,29% przychodu, więc więcej czasu temu nie poświęcamy. |
| Okno po newsletterze i SMS-ie | 24 godziny, na pacjenta, w dowolnej sesji, tylko zamówienia nieanulowane; przy przypisaniu sprzedaży ostatnie wejście przed płatnością; 7 dni obok jako wrażliwość | tylko ta sama sesja, 7 dni | Nadwyżka ponad zwykłe tempo jest prawie cała w tej samej sesji. 24 godziny łapią też zmianę urządzenia. |

**Dopiski Kuby przy przyjęciu:**
1. Przy ekonomii kampanii (koszt pozyskania, wynik na pacjenta) pokazujemy obok wynik według sesji płatności, także w narzędziu. Jeśli wynik kampanii zmienia znak zależnie od reguły, opisujemy go jako niepewny, a nie jako wniosek. Wartość remarketingu trafia na listę niewiadomych razem z testem.
2. Większość wejść z newslettera i SMS-ów to sesje zalogowane bez żadnego zakupu. To dopisujemy do sprawy sesji zalogowanych w A5, bo CRM to nasz główny kanał powrotów.
3. Podstawę przyjęcia definicji nowego pacjenta zapisujemy w założeniach, bo zadanie nie definiuje go wprost (`ZALOZENIA.md`, punkt 16).
4. Recenzję definicji przez Codeksa (model Sol, profil `review`) robimy przed zamknięciem A4, a nie dopiero w punkcie D. Błąd w definicjach znaleziony w środę oznaczałby przeliczanie wszystkiego od nowa. Na tym etapie nie używamy modelu Astra, konsylium ani Fable.

**Recenzja definicji przez Codeksa (model Sol, profil `review`, tylko odczyt), 2026-10-19.** Polecenie: `notatki/recenzje/a4_codex_prompt.md`. Odpowiedź: `notatki/recenzje/a4_codex_odpowiedz.md`. Podsumowanie i nasze decyzje: `notatki/recenzje/a4_codex.md`. Codex nie znalazł błędu, który zmieniałby odpowiedź. Ręcznie sprawdził siedmiu pacjentów. Przyjęliśmy wszystkie siedem uwag:
- trzy poprawki techniczne w kodzie (czas w UTC, pełne 61 dni obserwacji tła, wyjątek dla samego TelemediGO w sesjach zalogowanych);
- trzy doprecyzowania definicji, przyjęte przez Kubę: okno CRM tylko z zamówieniami nieanulowanymi, rozłączne przypisanie sprzedaży do ostatniego wejścia z CRM oraz porównanie okresów na tych samych dniach kalendarzowych (`ZALOZENIA.md` 26 i 27);
- jedną metodę do A5: oddzielenie zmiany struktury pacjentów od zmiany ich zachowania.
