# F — ostatnia kontrola przed publikacją (zlecenie Kuby, 2026-10-22 wieczorem)

Sesja prowadząca: `local_e4232e55-24be-46f8-a2c8-d411b47ebc48`. Wersja sprawdzana: `a4d52c9` (master).

## 1. Zlecenie (słowa Kuby, dosłownie)

> Grafika skończona, więc robimy ostatnią kontrolę przed publikacją. Trzy części, mogą iść równolegle.
>
> 1. Zgodność z zadaniem: Astra i Fable, niezależnie.
> Chcę, żeby ktoś z zewnątrz sprawdził, czy po wszystkich rundach nie odjechaliśmy od tego, o co Telemedi prosiło. Oryginalne zadanie jest tutaj: [link do strony z zadaniem]
> Recenzenci mają dostać pełny tekst zadania, słowo w słowo, a nie streszczenie z CLAUDE.md. Jeśli z linku da się wyciągnąć tylko streszczenie albo pustą stronę, powiedz mi. Tekstu zadania nie zapisuj w repozytorium.
> Poza tym dostają tylko to, co zobaczy Telemedi: zrzuty wszystkich zakładek ostatecznej wersji (komputer i telefon), pełne teksty strony, README i listę plików repozytorium. Bez naszych notatek i bez naszej oceny w briefie. Astra przez Codeksa (profil astra), Fable jako agent, każdy osobno, bez wglądu w odpowiedź drugiego.
> Pytania do nich:
> - Najpierw tylko pierwsza zakładka, dwie minuty czytania: jaka jest odpowiedź, dlaczego i co robimy w pierwszym tygodniu.
> - Dla każdego punktu z „Czego oczekujemy” i „Co oddajesz”: czy jest, gdzie, jak dobrze i czego brakuje. Osobno ślad pracy: zadanie mówi „prompty, ślepe uliczki, poprawki, nie sprzątaj go”. Czy repozytorium to pokazuje?
> - Gdzie przesunęliśmy akcent względem zadania: co jest rozbudowane ponad potrzebę, a co pokazane za słabo. Szczególnie: czy widać, które zdarzenie albo która decyzja zmieniła zachowanie kohort i wynik.
> - Czy osoba, która dała to zadanie, prowadziłaby na tym narzędziu biznes na co dzień? Co by ją zatrzymało?
> - Najwyżej trzy rzeczy do poprawy przed wysłaniem, tylko takie, które zmieniają ocenę rozwiązania. I czego nie ruszać.
> Pokaż mi brief, zanim go wyślesz. Poprawiamy tylko braki wobec zadania i to, co zmienia odpowiedź. Resztę zapisz jako materiał na rozmowę.
>
> 2. Kontrola techniczna ostatecznej wersji: kontrola liczb w eksporcie i kontrola liczb na wykresach względem tekstu kart, 9 zakładek na komputerze i telefonie, tryb jasny i ciemny, konsola, odnośniki z filtrami po odświeżeniu strony, brak pobierania czegokolwiek z internetu, czas ładowania.
>
> 3. Język tylko tam, gdzie tekst zmienił się od rana: nowe zdania, podpisy wykresów, legendy, objaśnienia. Całości drugi raz nie przepisujemy.
>
> Nic nie publikuj. Po wszystkim zatrzymaj się u mnie z wynikiem i listą poprawek.

Link do strony z zadaniem pominięty w tej notatce (zadanie nie trafia do repozytorium).

## 2. Podział pracy

- **Część 1 (ta sesja):** recenzja zgodności z zadaniem — Astra przez Codeksa (profil `astra`) i Fable jako agent, każdy osobno. Pliki: `notatki/recenzje/f_*`, ta notatka.
- **Część 2:** sesja „F2: kontrola techniczna przed publikacją” (`local_ffe2f6b6-4957-46af-a45a-bc387d0f5ea1`). Pliki: `analiza/f_*.py`, `analiza/wyniki/f_*`, `notatki/f_techniczna.md`.
- **Część 3:** sesja „F3: język tekstów zmienionych od rana” (`local_00805ea0-b3fc-4dbd-9579-b08237769a17`). Plik: `notatki/f_jezyk.md`.
- Sesje 2 i 3 niczego nie poprawiają i nie commitują; poprawki wprowadzamy dopiero po decyzji Kuby. Commit robi sesja prowadząca.
- **Założenie sesji prowadzącej:** „od rana” to od wersji `ccc3c61` (22.10.2026, godz. 00:31), którą Kuba przeglądał rano. Między nią a `a4d52c9` teksty zmieniały: druga lista Kuby (`4c594b5`), trzecia lista (`351f556`) i dopracowanie grafiki (`6c5c683` … `87b55b2`).

## 3. Część 1 — jak przygotowaliśmy recenzję

**Tekst zadania.** Narzędzie odczytu strony z zadaniem (artefakt claude.ai spoza organizacji) zwróciło tylko streszczenie, ale zapisało surową stronę na dysku. Pełny tekst wyciągnęliśmy z niej kodem: 1 568 słów, wszystkie sekcje (Kontekst, Czego oczekujemy, Co oddajesz, Dane, Zasady). Skan nie znalazł ukrytych elementów, niewidocznych znaków ani tekstu zwracającego się do AI. Układ zamieniony na Markdown (nagłówki, listy, tabele); kontrola skryptem: ciąg słów identyczny z oryginałem, poza tytułem karty przeglądarki i numerami listy. Tekst został w folderze roboczym sesji, poza repozytorium (decyzja Kuby).

**Materiał dla recenzentów (tylko to, co zobaczy Telemedi):**
1. tekst zadania słowo w słowo;
2. zrzuty 9 zakładek przy 1366 i 375 px, w ustawieniach domyślnych, z danymi z commita `a4d52c9` (`analiza/e_przegladarka.py --dane-z-gita HEAD`), pocięte na 66 obrazów (komputer: fragmenty 1366 × 1350 px; telefon: po trzy fragmenty 375 × 1500 px obok siebie);
3. pełne teksty stron odtworzone ze stanu `a4d52c9` (`analiza/b2_teksty_strony.py` uruchomiony na kopii `git archive HEAD`);
4. README, lista plików repozytorium (205 plików) i lista 88 commitów.

**Brief** pokazany Kubie przed wysłaniem i przyjęty („tak, wysyłaj, obie rzeczy zostają”). Dwie rzeczy dodane ponad zlecenie i przyjęte przez Kubę: lista commitów jako materiał (bez niej ślad pracy da się ocenić tylko po nazwach plików) i czwarte pytanie etapu 1 („co było jasne od razu, a co trzeba było przeczytać drugi raz”). Treść poleceń: `notatki/recenzje/f_astra_polecenie_etap1.md`, `f_astra_polecenie_etap2.md`, `f_fable_polecenie.md` (bez tekstu zadania).

**Przebieg.** Etap 1: tylko tekst zadania i 6 zrzutów pierwszej zakładki. Etap 2: cały materiał. Astra: dwa osobne wywołania Codeksa (`codex exec -p astra -s read-only`, model `gpt-6-astra`), polecenie na stdin, zrzuty jako załączniki, w pustym katalogu roboczym, z zakazem czytania plików z dysku; w etapie 2 dostała własną odpowiedź z etapu 1. Fable: agent (`model: fable`), czyta tylko folder z materiałem danego etapu, etap 2 jako dalszy ciąg tej samej rozmowy. Żaden recenzent nie widział odpowiedzi drugiego.

**Ślepa uliczka techniczna:** pierwsze uruchomienie etapu 2 Astry nie wystartowało, bo 66 bezwzględnych ścieżek do zrzutów przekroczyło limit wiersza poleceń Windows (8 191 znaków; `codex` to skrypt `.cmd`). Zrzuty skopiowane do podkatalogu katalogu roboczego i podane krótkimi ścieżkami względnymi. Przed etapem 1 krótki test na modelu Sol potwierdził, że Codex dostaje zrzuty z załączników.

**Wada zrzutów, wyłapana przez Astrę:** zrzut całej strony „Priorytety” przy 375 px (strona ma 24 464 px wysokości) urywa się na 16 384 px i dalej powtarza górę strony. To limit wysokości zrzutu całej strony w Chromium/Edge, nie błąd narzędzia: zrzuty okna odcinkami po 6 000 px pokazują, że karta 7 przechodzi normalnie w kartę 8, rysuje się wszystkie 12 kart, 0 błędów strony. Pozostałe zakładki są niższe niż 16 384 px. Recenzenci mieli tę część w pełnych tekstach; Fable dostał w trakcie etapu 2 wiadomość o wadzie, Astra sama oznaczyła to jako możliwy błąd zrzutów. Dotyczy też `analiza/e_przegladarka.py` (zrzut `375_priorytety.png`) — uwaga przekazana sesji kontroli technicznej.

**Przy okazji (do listy poprawek):** zapisany w repozytorium zrzut tekstów `analiza/wyniki/b_teksty_strony.md` powstał na stanie `63ddc3d`, przed poprawką wykresu powrotu `87b55b2`. W dwóch miejscach podaje −5,3 pkt proc. (powrót w ciągu 180 dni), a strona pokazuje −5,2. Do odtworzenia skryptem `b2_teksty_strony.py`.

## 4. Część 1 — wynik recenzji (Astra i Fable, niezależnie)

Odpowiedzi: `notatki/recenzje/f_astra_odpowiedz_etap1.md`, `f_astra_odpowiedz_etap2.md`, `f_fable_odpowiedz_etap1.md`, `f_fable_odpowiedz_etap2.md`.

**Puenta.** Oba modele uznają, że rozwiązanie odpowiada na zadanie i że odpowiedź „Nie” jest dobrze uzasadniona. Oba niezależnie wskazują te same dwie słabości wobec zadania: związek „zdarzenie → zachowanie kohort → wynik” trzeba składać z kilku zakładek, a ślad pracy deklaruje ślepe uliczki i prompty, ale ich nie pokazuje. Oba oceniają narzędzie jako dobre do diagnozy i przeglądów tygodniowych, a słabsze do pracy dzień w dzień.

**Etap 1 (dwie minuty, tylko pierwsza zakładka).** Oba modele odczytały odpowiedź, trzy powody i decyzje na pierwszy tydzień zgodnie z intencją strony. Miejsca, które trzeba było czytać dwa razy, sprawdzone w tekstach strony (ze stanu `a4d52c9`):
- „Z kanałów bezpłatnych … przybyło 12% nowych pacjentów” brzmi jak udział, a to przyrost: z 7 069 do 7 924, czyli +12,1% (`analiza/e_teksty.py`, szkic `notatki/e_teksty.md`). Potwierdzone.
- Zastrzeżenie „spadek marży w III kwartale 2026, o 7% rok do roku” nie mówi, o którą marżę chodzi, a wykres nad nim pokazuje marżę przed kosztem kampanii (+25%). Potwierdzone.
- Decyzja 2 „według obu reguł przypisania” — reguły nie są nazwane w tym miejscu. Potwierdzone.
- „Około 71% spadku” obok zastrzeżenia „nie wiemy, czy ci sami pacjenci zachowują się dziś gorzej, czy zmieniło się to, kto do nas trafia” czyta się jak zaprzeczenie. Potwierdzone (zastrzeżenie dotyczy w praktyce reszty spadku).
- „Awaria Safari trwała 198 dni bez alarmu” (decyzja 3 i karta pozycji 2): dane pokazują spadek trwający 198 dni do końca danych, ale nie mówią nic o alarmach. Potwierdzone (zdanie w trzech miejscach).
- Kolejność decyzji na pierwszy tydzień (pozycje 1, 3–4, 2, 5–6–8–11) nie idzie za numeracją priorytetów; nagłówek TelemediGO mówi o „chęci zakupu”, a wykres pokazuje liczby zakupów bez odsetków (Astra). Uwagi do rozmowy.

**Etap 2 — zbieżne wnioski i ocena sesji prowadzącej (przyjmuję / odkładam):**

| Uwaga | Kto | Ocena sesji prowadzącej |
|---|---|---|
| Związek zdarzenie → kohorty → wynik rozproszony; brak jednego miejsca „zdarzenie, które kohorty objęło, miara przed i po, skutek w złotych”; skoki budżetu (najważniejsza decyzja w danych) nie są zdarzeniami na osi | oba (Astra: E1, Fable: E2) | **przyjmuję jako kandydata „przed wysłaniem”** — dotyczy części, którą zadanie nazywa najważniejszą; liczby w większości już są na stronie (porównania 60 dni przed i po dla 14 zdarzeń, ekonomia kampanii, Safari, newsletter) |
| Ślad pracy: README deklaruje ślepe uliczki, ale żadnej nie wskazuje; nie ma rozmów z głównym narzędziem (Claude Code); README nie wskazuje `CLAUDE.md` jako zasad pracy z AI | oba (Astra: E3, Fable: E1) | **przyjmuję jako kandydata „przed wysłaniem”** — zadanie wymienia to wprost w „Co oddajesz”; README, wiersz „Ślepe uliczki zostały w historii commitów”, potwierdza zarzut. Eksport rozmów wymaga decyzji Kuby (zawierają m.in. globalne instrukcje z odwołaniami do innych projektów) |
| Pięć zdań na pierwszej zakładce (wyżej) | Fable: E3, Astra: etap 1 i E2 (198 dni) | **przyjmuję jako kandydata „przed wysłaniem”** — to dwuminutowe czytanie, od którego zaczyna osoba oceniająca; poprawki tylko językowe, liczby bez zmian |
| Wartość pozycji 7 (23,6 tys. zł za punkt procentowy), 11 i 12 (koszt testu) nie jest kwotą „ile jest warta”; pewność problemu i kwoty w jednym znaczniku; kryterium sukcesu alarmów | oba (Astra: A i E2, Fable: A) | odkładam do decyzji Kuby — częściowy brak wobec zadania, ale zmiana wymaga nowych założeń (np. zakładanego efektu wiadomości), a wyceny przeszły konsylium |
| Narzędzie analityczne, nie operacyjne: domyślnie 12 miesięcy wobec roku wcześniej, brak widoku „ostatnie 7 dni” i alarmów w narzędziu, ekonomia kampanii bez serii czasowej | oba (D) | odkładam do decyzji Kuby — ten sam widok proponowało konsylium D i nie wszedł na listę Kuby; żaden recenzent nie dał go do swoich trzech poprawek |
| Za dużo tekstu (około 205 tys. znaków), rozbudowane „Po zakupie” i tabele scenariuszy, dwie reguły przypisania obok siebie wszędzie | Fable: C, Astra: C | materiał na rozmowę — oba modele jednocześnie radzą nie dodawać i nie przepisywać tekstu teraz |
| Karta Safari w lejku porównuje różne okresy po awarii (Safari 17.03–30.09, inne przeglądarki 17.03–15.05), a porównanie równych 60 dni jest w szczegółach | Astra: A | materiał na rozmowę — wniosek się nie zmienia (66% → 46% wobec 64,8% → 63,4%) |
| Drobne zmiany oznaczone „lepiej/gorzej” mimo braku istotności (oceny w „Po zakupie”, różnica 0,01) | Astra: D | do sprawdzenia z wynikiem części 3; materiał na rozmowę |
| Szerokie tabele na telefonie wymagają przewijania w bok (Kohorty, Lejek, Wynik biznesu) | oba (D) | materiał na rozmowę — przewijanie w tabeli jest zamierzone; sprawdza część 2 |
| Seria kohortowa bez kosztu pozyskania; 9 niewiadomych bez przypisanego priorytetu | Fable: A | materiał na rozmowę |

**Czego nie ruszać (zgodnie u obu):** odpowiedzi „Nie” na pierwszej stronie, liczb i definicji, dwóch sposobów przypisania źródła, zasady pełnych okien obserwacji, oddzielania obserwacji od przyczyny, struktury 9 zakładek, zakładki „Czego nie wiemy”. Nie dodawać nowych analiz, recenzji modeli ani tekstu.

## 5. Część 2 — wynik kontroli technicznej (sesja `local_ffe2f6b6`, raport `notatki/f_techniczna.md`)

Wersja `a4d52c9` jest technicznie gotowa po jednej małej poprawce. Eksport: 115 kontroli bez różnic, 4 218 liczb w tekstach z pokryciem w szkicach; ponowny eksport daje te same dane strony (różnią się godzina, skrót commitu w stopce i szum zmiennoprzecinkowy w 11 sumach przychodu). Liczby na wykresach wobec tekstu i tabel kart: 1 956 porównań na silnik, 0 niezgodności w Edge, WebKit i Firefoksie. 305 odnośników z filtrami działa wprost i po odświeżeniu. 0 żądań poza 127.0.0.1. Na telefonie z wolnym 4G pierwsza zakładka gotowa po 1,6 s. Przed wysłaniem: pasek zakładek przy 761–990 px chowa „Priorytety” i „Czego nie wiemy”. Na rozmowę: 10 drobnych spraw strony (m.in. przesuwanie „Lejka” w bok w Safari na telefonie, ucięte cyfry w tabelach na telefonie, kontrast białych liczb na kolorowych polach) i uwaga do skryptu zrzutów (limit 16 384 px). Nowe skrypty kontroli: `analiza/f_eksport_powtarzalnosc.py`, `f_wykresy_tekst.py`, `f_kontrast.py`, `f_odnosniki.py`, `f_siec_czas.py`, `f_publikacja.py`. Po zakończeniu w folderze zostało 6 śledzonych plików odświeżonych eksportem (`narzedzie/dane_strony/c.js`, `jakosc.js`, `podsumowanie.js`, `analiza/wyniki/b_eksport.txt`, `b_eksport_c.txt`, `e_poprawki.txt`) — treść danych bez zmian; nie commitujemy ich przed decyzją Kuby, pójdą razem z poprawkami.

## 6. Część 3 — wynik kontroli języka (sesja `local_00805ea0`, raport `notatki/f_jezyk.md`)

Sprawdzone 890 miejsc zmienionych między `ccc3c61` a `a4d52c9` (690 linii tekstów strony, 185 nowych napisów w kodzie strony, 15 zmian w README). 12 poprawek „przed wysłaniem” (żadna nie zmienia odpowiedzi; cztery mogą wprowadzić w błąd, w tym podpis wykresu godzin niezgodny z tytułem karty) i 35 uwag na rozmowę. Dwie poprawki pokrywają się z uwagami Fable do pierwszej zakładki (12% jako przyrost, a nie udział; nienazwana marża w zastrzeżeniu o III kwartale). Poza językiem: nieaktualny zrzut tekstów w repozytorium, numeracja zdarzeń w zrzucie tekstów, stopka ze starym stanem repozytorium, niesymetryczne okna wykresu Safari.

## 7. Propozycja poprawek dla Kuby

Kuba przeczytał recenzje, kontrolę języka i syntezę i poprosił (2026-10-22, w nocy) o propozycję jednej rundy poprawek przed zmianami: tylko braki wobec zadania i to, co zmienia ocenę, bez nowych analiz, raczej lepiej pokazać to, co mamy; przy każdej poprawce co i gdzie, jak to zobaczy Telemedi, skąd liczby i jak je sprawdzimy, ile zajmie, co może pójść źle, warianty z rekomendacją; osobno czego nie ruszamy i co idzie na rozmowę; szczególnie tabela „zdarzenie albo decyzja → kohorty → wynik” i ślad pracy z zapisem rozmów bez niczego spoza projektu. Propozycja: `notatki/f_propozycja.md`. Czeka na decyzję Kuby; do tego czasu nic na stronie, w tekstach ani w README się nie zmienia.

**Skan zapisu rozmów (do poprawki 2, tylko liczby, bez treści):** 19 plików sesji tego projektu (około 160 MB; z agentami pomocniczymi 219 MB). Po stronie użytkownika 178 wiadomości (około 290 tys. znaków, w tym automatyczne powiadomienia), odpowiedzi tekstowe Claude 794 (około 354 tys. znaków). Nazwy innych projektów są w 79 blokach doklejanych przez aplikację (globalne instrukcje, umiejętności, łączniki) i w 27 wynikach narzędzi, a w samej rozmowie: 1 wiadomość z nazwą innego projektu, 10 z adresem e-mail, 2 ze ścieżką spoza folderu projektu, 0 z wzorcami kluczy i haseł. Skrypt skanu: w folderze roboczym sesji (`skan_rozmow.py`); jeśli Kuba wybierze wariant z zapisem rozmów, skrypt filtrujący i skan trafią do repozytorium.

## 8. Runda poprawek (2026-10-23): wynik

Decyzja Kuby: „tak, wszystko według rekomendacji, ruszaj z dwiema sesjami” (`DECYZJE.md`). Wykonanie i kontrole: `DECYZJE.md`, wpis „runda poprawek F: wykonanie i stan przed publikacją”; szczegóły w `notatki/f_poprawki_strona.md` (strona) i `notatki/f_slad_pracy.md` (ślad pracy); przejrzenie przez Codeksa: `notatki/recenzje/f_codex.md`.

- **Strona:** nowa pierwsza karta „Kohort” z tabelą 8 zdarzeń i decyzji („Po starcie naszych kampanii na L4 rośnie udział pacjentów, którzy rzadko wracają, a awaria Safari obniża wynik”), sześć zdań pierwszej zakładki, dziesięć poprawek języka, wykres Safari na równych oknach, pasek zakładek do 1 000 px, telefon (Safari bez przesuwania „Lejka” w bok, tabele bez uciętych cyfr). Liczby bez zmian.
- **Ślad pracy:** sekcja README z 10 historiami, `rozmowy/`, `notatki/lekcje.md`; Kuba przejrzał raport skanu i pliki i dał zgodę na commit.
- **Kontrole:** jak w `DECYZJE.md`; przejrzenie przez Codeksa bez błędów w liczbach, trzy brzmienia poprawione.
- **Zostaje przed publikacją:** dwie decyzje Kuby (ścieżka innego projektu w historii, fragmenty tekstu zadania), ponowny zapis rozmów, nazwa organizacji i adres w README, kroki publikacji za zgodą Kuby, sprawdzenie na prawdziwych telefonach, mail.
