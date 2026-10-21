# E — ostatnia duża runda przed publikacją: merytoryka, język, wygląd (zlecenie Kuby, 2026-10-21)

## 1. Zlecenie Kuby (słowa Kuby, bez zmian)

Przejrzałem całe narzędzie tak, jakbym był kimś z Telemedi, kto widzi je pierwszy raz. Merytorycznie jest mocne. Graficznie jest za słabe, a teksty są za gęste: za dużo liczb w jednym zdaniu, za dużo asekuracji, za mało wniosków. To ostatnia duża runda przed publikacją. Są trzy części, a kolejność ma znaczenie. Najpierw merytoryka, bo zmienia teksty. Potem język. Na końcu wygląd. Wygląd możesz robić równolegle w osobnej sesji, jeśli rozdzielicie pliki.

**Część 1. Merytoryka.** Każdą rzecz najpierw sprawdź kodem. Jeśli wyjdzie inaczej, niż myślę, powiedz mi o tym, zamiast poprawiać na siłę.

1. Mam wątpliwość co do liczb „bez nowych kampanii według sesji płatności” w opisie retencji (20,4%, 63,3 zł, „46%” udziału kampanii, +20,1% pacjentów). Sesja płatności przypisuje do starych kanałów pacjentów kampanii na L4, którzy weszli z reklamy, a zapłacili w innej sesji, często z kodem kampanii. Sprawdź, czy cała różnica między regułami w retencji starych kanałów to nie jest po prostu ta grupa. Jeśli tak, to w opisie retencji i przyrostu pacjentów zostaw regułę główną, a drugą przenieś do szczegółów z jednym zdaniem wyjaśnienia. W ekonomii kampanii obie reguły zostają.
2. Trzecia liczba na górze, czyli marża w III kwartale 2026 niższa o 6,8%, budzi moją wątpliwość. Rok wcześniej we wrześniu ruszyła sprzedaż TelemediGO w newsletterze: 225 zakupów w 23 dni. To było jednorazowe. Do tego w tym kwartale działa awaria Safari. Policz, ile zostaje ze spadku bez tego jednorazowego skoku. Jeśli spadek nie jest odporny, nie stawiaj go na górze. Daj tam fakt, który jest odporny: marża przed kosztami kampanii rośnie o 25%, a wydatki na kampanie są ponad dwa razy wyższe. Obok uczciwie podaj, że za cały rok marża wzrosła. To samo popraw w README i w akapicie o bazie powracających pacjentów.
3. Marża na powtórne zamówienie spada (35,86 wobec 32,81 zł). Sprawdź, czy to nie jest głównie rosnący udział wizyt ze zniżką TelemediGO. Jeśli tak, napisz to, bo to się spina z wnioskiem, że opłata 89 zł nie pokrywa zniżek.
4. Nagłówek lejka mówi o wszystkich sesjach (16,0% wobec 13,7%), a w nich są też pacjenci powracający, którzy płacą prawie zawsze. Dla pozyskania liczą się osoby, które jeszcze nie kupowały. Zacznij od nich:
   * ile z nich płaci dziś, a ile rok temu;
   * od którego miesiąca to spada i co się wtedy działo.
   To jest odpowiedź na pytanie z zadania, gdzie i od kiedy tracimy pacjentów. Sprawdź też, czy zdanie o przeglądarkach w aplikacjach („4,8–7,2% wobec 16,1–18,1%”) dotyczy tej grupy, którą nazywa.
5. Pozycja 7: zdanie „po newsletterze wraca 3,16%, bez niego 18,84%” czyta się tak, jakby newsletter szkodził. To chyba podział tej samej grupy pacjentów, a nie porównanie dwóch grup. Popraw. Dopisz też, że 23,6 tys. zł to marża do 180. dnia.
6. Pozycja 4: sposób sprawdzenia, czy pauza Google Ads na specjalistów zadziałała, powinien patrzeć na wszystkich nowych pacjentów u specjalistów i na marżę po wydatkach, tak jak w teście Mety.
7. Pozycja 5 łączy dwie różne decyzje: nową kreację reklamy i zmianę zasad zwrotów przy odmowie L4. Rozdziel kwoty, bo sama kreacja jest warta mniej, niż pokazuje górny koniec zakresu.
8. Test TelemediGO nie „rozstrzygnie” roli programu. Pokaże wpływ samej zniżki. Popraw zapowiedzi w trzech miejscach i dopisz, że koszt testu liczysz przy niezmienionej liczbie wizyt.
9. Dopisz jedno zdanie, dlaczego test Mety, czyli największa kwota na liście, stoi na 9. miejscu.
10. Drobne:
   * stawka pediatry to założenie z zadania (100 zł), a nie niewiadoma; wariant 25 zł pokaż jako sprawdzenie wrażliwości;
   * niewiadoma 2: test bez reklamy mierzy przyrost niezależnie od reguły, a nie wybiera reguły;
   * wynik kampanii na markę i remarketingu jest ostrożny, bo część zamówień z tych reklam to powroty;
   * poranne opóźnienia oprzyj na wynikach z ostatniego roku, bo grupy spóźnionych rok wcześniej są małe;
   * „godzina bez danych” jest opisana za stanowczo;
   * zdanie w README o sesjach zalogowanych („według słownika powinny”) nie ma pokrycia w słowniku.

**Część 2. Język.** Profesjonalnie, ale zrozumiale dla menedżera, krótko i nie jak tekst z AI. Zasady na całe narzędzie i README:

* Nagłówek karty to wniosek, a nie temat. Na przykład zamiast „TelemediGO: skąd +40,3% sprzedaży” coś w stylu „TelemediGO rośnie razem z liczbą zamówień, a nie dzięki większej chęci zakupu”.
* Pod nagłówkiem jedno zdanie z wnioskiem, w którym są najwyżej dwie liczby, zaokrąglone.
* Szczegóły chowaj do zwijanej sekcji „Szczegóły”: drugą regułę, przedziały, liczebności, metodę i to, skąd są liczby. Zasada „liczebność przy każdym odsetku” zostaje, ale wystarczy, że jest w tabeli albo w szczegółach.
* Jedno zastrzeżenie na kartę, powiedziane wprost. Bez asekuracji w każdym zdaniu.
* Ten sam słownik wszędzie. W tekstach „ostatnie 12 miesięcy” i „rok wcześniej” zamiast „okres 1” i „okres 2”. „Okres A” i „okres B” zostają tylko tam, gdzie wybiera się własne daty. Słowa „opisowo”, „rozkład księgowy”, „dodatkowość” i „reguła porównawcza” tylko w szczegółach, z wyjaśnieniem.
* Bez wyliczanek po trzy przymiotniki, bez „warto zauważyć” i „kluczowe”, bez nagłówków typu „X: tak”.
* Rekomendacje pisz jako decyzje: „Wstrzymać kampanię…”, a nie jako opis. Nazwy techniczne kampanii przenieś do szczegółów.
* Na górze „Czy to wzrost” werdykt w jednym, dwóch zdaniach, na przykład: „Pacjentów przybywa, ale wracają rzadziej. Wydatki na kampanie rosną dużo szybciej niż marża, którą biznes zarabia przed ich kosztem.” Oczywiście tylko jeśli część 1 to potwierdzi.
* Kontrola zgodności liczb zostaje taka sama: każda liczba z eksportu i ze szkicu.

**Część 3. Wygląd.** Ma wyglądać jak profesjonalne narzędzie biznesowe: kolorowe, ale z umiarem. Użyj skilli do projektowania interfejsu (frontend-design) i do wykresów (dataviz). Kierunek:

* Strona: u góry ciemnogranatowy pasek z nazwą i zakładkami, białe karty z delikatnym cieniem na jasnoszarym tle i jeden kolor do odnośników i wyborów.
* Kolory stanu (dobrze, źle, uwaga) zawsze razem z ikoną i słowem, nigdy sam kolor. Ikony rysowane w SVG, a nie znaki typu ▲.
* Bez kolorowych pasków po lewej stronie kart.
* „Czy to wzrost”: na górze werdykt ze znacznikiem „Nie”, pod nim trzy kafelki z dużą liczbą i jedną linijką podpisu, niżej ponumerowane decyzje na pierwszy tydzień, które prowadzą do priorytetów. Karty „Więcej pacjentów” i „Lepsza retencja” mają znaczniki „Tak” i „Nie”.
* Lejek: potrzebny wykres kroków od wejścia do płatności, a nie tylko tabela. Dla każdego kroku pasek z odsetkiem sesji, które do niego doszły, i znacznik tego samego odsetka rok wcześniej. Między krokami: ile przechodzi dalej. Wyróżnij przejście, które najbardziej się pogorszyło. Domyślnie pokaż osoby, które jeszcze nie kupowały. Wykres ma reagować na filtry.
* Priorytety: pewność jako kolorowe znaczniki (Wysoka, Średnia, Niska, Test), kwota wyróżniona, a w karcie pozycji pasek „Ile warte · Pewność · Wdrożenie”.
* Zmiany rok do roku jako małe zielone albo czerwone etykiety ze strzałką.
* Filtry w jednym panelu nad treścią.
* Telefon: ma działać tak samo dobrze.
* Kontrola: sprawdź wszystko w przeglądarce, na komputerze i na telefonie.

Na koniec niech Codex przeliczy nowe liczby. Nic nie publikuj. Zatrzymaj się u mnie z gotową wersją do przeglądu.

## 2. Podział pracy (decyzja sesji prowadzącej, zgodnie ze zgodą Kuby na osobną sesję od wyglądu)

**Sesja prowadząca (ta): część 1, potem część 2.** Liczy wątpliwości Kuby własnymi skryptami (`analiza/e_*.py`, raporty `analiza/wyniki/e_*`), potem przepisuje teksty w nowym kształcie danych (punkt 3).

**Sesja wyglądu: część 3.** Pracuje równolegle, od razu.

**Własność plików (dwie sesje nie edytują tych samych plików):**

| Sesja | Pliki |
|---|---|
| prowadząca (teksty i liczby) | `analiza/*.py` (w tym `b_eksport.py`, `b2_eksport_c.py`), `analiza/wyniki/*`, `narzedzie/dane_strony/*` (tylko przez eksport), `notatki/*` poza `notatki/e_wyglad.md`, `README.md`, `CLAUDE.md` |
| wyglądu | `narzedzie/index.html`, `narzedzie/styl.css`, `narzedzie/app.js`, `narzedzie/widoki.js`, `narzedzie/widoki_c.js`, nowe pliki w `narzedzie/` (np. ikony, nowe skrypty rysujące), `notatki/e_wyglad.md`, skrypty kontroli w przeglądarce (np. `analiza/e_przegladarka.py` — wyjątek: tylko ten jeden plik w `analiza/`) |

- Commity: każda sesja dodaje do commita tylko swoje pliki (`git add <ścieżki>`, nigdy `git add -A` ani `git add .`). Gdy git zgłosi zablokowany indeks (`index.lock`), odczekać chwilę i powtórzyć.
- Sesja wyglądu nie numeruje założeń w `ZALOZENIA.md` i nie edytuje wspólnych notatek. Propozycje wpisów zapisuje w `notatki/e_wyglad.md`, scala je sesja prowadząca.
- Teksty statyczne w plikach sesji wyglądu (nagłówki narzędziowe, podpisy filtrów, przypisy „jak liczymy” w `index.html` i w JS) sesja wyglądu poprawia sama według zasad części 2, **bez dopisywania nowych liczb**. Wszystkie zdania z liczbami i wnioskami przychodzą z danych (`dane_strony/*.js`), które pisze sesja prowadząca.

## 3. Kontrakt danych: jak teksty trafiają na stronę (nowy kształt)

Cel: każdy tekst analityczny przychodzi z danych w jednym, ogólnym kształcie **karty**, a strona tylko go rysuje. Dzięki temu sesja prowadząca może przepisywać teksty, a sesja wyglądu projektować karty niezależnie. Do czasu, aż eksport zacznie dawać nowy kształt, strona musi dalej działać ze starym (rysowanie: najpierw nowy kształt, gdy go nie ma — dotychczasowy).

### 3.1. Karta tekstowa

```
karta = {
  "id": "pacjenci",                       // opcjonalnie, kotwica
  "tytul": "Pacjentów przybywa: o połowę więcej niż rok wcześniej",   // nagłówek = wniosek
  "znacznik": {"tekst": "Tak", "stan": "dobrze"},   // opcjonalnie; stan: dobrze | zle | uwaga | neutralnie
  "wniosek": "Jedno zdanie, najwyżej dwie liczby.", // opcjonalnie
  "tresc": [blok, ...],                   // widoczna treść, krótka; opcjonalnie
  "zastrzezenie": "Jedno zastrzeżenie wprost.",     // opcjonalnie, najwyżej jedno
  "szczegoly": [blok, ...],               // zwinięte pod „Szczegóły”; opcjonalnie
  "linki": [{"tekst": "...", "href": "#kohorty?..."}],   // opcjonalnie: „Zobacz w danych”
  "zrodlo": "analiza/wyniki/...",         // opcjonalnie; rysowane na końcu szczegółów jako „Skąd liczby”
  "wstaw": "mostek"                       // opcjonalnie: miejsce na element rysowany przez stronę (np. tabela mostka z podsumowanie.js)
}
```

Bloki (w `tresc` i `szczegoly`):

```
{"typ": "akapit", "tekst": "..."}
{"typ": "punkty", "punkty": ["...", "..."]}           // lista nienumerowana
{"typ": "numerowane", "punkty": ["...", "..."]}       // lista numerowana
{"typ": "podtytul", "tekst": "..."}
{"typ": "liczba", "liczba": "+52%", "podpis": "...", "zmiana": "wzrost"|"spadek"|"bez", "stan": "dobrze"|"zle"|"uwaga"|"neutralnie"}
{"typ": "tabela", "tytul": "...", "kolumny": ["...", ...],
   "wiersze": [{"opis": "...", "komorki": [komorka, ...], "podsuma": true|false}]}
```

Komórka tabeli: zwykły tekst albo obiekt
`{"tekst": "−6,5 pkt proc.", "zmiana": "wzrost"|"spadek"|"bez", "stan": "dobrze"|"zle"|"neutralnie", "pod": "druga linia (np. liczba pacjentów)"}`.
Komórka z polem `zmiana` to etykieta zmiany rok do roku (strzałka według `zmiana`, kolor i słowo według `stan`). Wszystkie teksty to zwykły tekst, bez HTML.

### 3.2. „Czy to wzrost” (`D.C.wzrost`)

```
{
  "tytul": "Czy to, co widać na dashboardzie, jest wzrostem?",
  "wstep": "...",
  "werdykt": {"znacznik": {"tekst": "Nie", "stan": "zle"}, "tekst": "Jedno, dwa zdania."},
  "kafelki": [{"liczba": "+52%", "podpis": "jedna linijka", "zmiana": "wzrost", "stan": "dobrze"}, ... (3)],
  "decyzje": {"tytul": "Decyzje na pierwszy tydzień",
              "punkty": [{"nr": 1, "tekst": "Naprawić zakładanie konta w Safari na iPhone'ach", "href": "#priorytety?p=1", "dopisek": "pozycja 1"}, ...]},
  "karty": [karta, ...],      // w kolejności; dwie pierwsze to „Więcej pacjentów” (znacznik Tak) i „Lepsza retencja” (znacznik Nie), mogą stać obok siebie
  "zrodlo": "..."
}
```

### 3.3. „Priorytety” (`D.C.priorytety`)

```
{
  "tytul": "...", "wstep": "...",
  "przeglad": [{"nr": 1, "co": "Naprawić ...", "ile": "75–83 tys. zł", "ile_dopisek": "rocznie, 90 dni od pozyskania",
                "pewnosc": {"poziom": "wysoka"|"srednia"|"niska"|"test", "tekst": "Wysoka", "dopisek": "awaria widoczna w danych"},
                "wdrozenie": "dni"}],
  "zasady": karta,
  "karty": [{"nr": 1, "tytul": "decyzja", "wniosek": "jedno zdanie",
             "pasek": {"ile": "...", "ile_dopisek": "...", "pewnosc": {...jak wyżej}, "wdrozenie": "..."},
             "sekcje": [{"tytul": "Z danych", "punkty": ["..."]}, ...],
             "tabela": (dotychczasowy kształt tabeli kampanii, opcjonalnie),
             "szczegoly": [blok, ...], "linki": [...], "zrodlo": "..."}],
  "nie_robimy": karta,
  "zrodlo": "..."
}
```

### 3.4. „Czego nie wiemy” (`D.C.niewiadome`)

Bez zmian kształtu: `{"tytul", "wstep", "wiersze": [{"nr", "co", "dlaczego", "test", "pozycja"}], "zrodlo"}`.

### 3.5. Pozostałe zakładki

W każdym miejscu, w którym strona dziś rysuje listę zdań z danych (`zdania` w `podsumowanie.js`, `kohorty.js`, `po_zakupie.js`, `wynik.js`, `jakosc.js`; karty napraw `naprawy` w lejku), eksport doda obiekt `karta` (pierwsze zdania zakładki) albo listę `karty` (np. `naprawy_karty` w lejku). Strona rysuje kartę, gdy jest, a w przeciwnym razie dotychczasowe zdania. Zdarzenia na osi zostają w dotychczasowym kształcie (`tytul`, `co`, `ile`, `skad` itd.).

## 4. Część 1 — wynik sprawdzenia (skrypt `analiza/e_merytoryka.py` → `analiza/wyniki/e_merytoryka.txt` i `.json`)

1. **Reguły w retencji „bez nowych kampanii”: potwierdzone w całości.** Cała różnica między regułami to jedna grupa: 1 383 pacjentów (kohorty z pełnym oknem 90 dni; 2 081 w całych ostatnich 12 miesiącach), których przyjęta reguła przypisuje nowym kampaniom na L4, a sesja płatności starym kanałom. 92% z nich weszło pierwszy raz z reklamy nowej kampanii, 73% zapłaciło z kodem tej kampanii, 83% zaczęło od L4. Płacili w sesji z wejścia bezpośredniego (42%), z bezpłatnej wyszukiwarki (24%), z Google Ads na markę (22%) i z remarketingu Meta (13%). Wracają w 90 dniach w 4,3%, tak jak pozostali pacjenci nowych kampanii (4,1%). Grupy odwrotnej (stara według przyjętej reguły, nowa według sesji płatności) nie ma. Bez tej grupy sesja płatności daje dokładnie to samo co reguła przyjęta: powrót 22,0% (a nie 20,4%), marża 66,0 zł (a nie 63,3 zł), pacjentów +7,3% (a nie +20,1%), udział nowych kampanii w spadku powrotu 71% (a nie 46%). Wniosek: w retencji i przyroście pacjentów zostaje reguła przyjęta, druga idzie do szczegółów z jednym zdaniem wyjaśnienia; w ekonomii kampanii obie zostają.
2. **III kwartał: spadek marży nie jest odporny.** Jednorazowa nadwyżka startu sprzedaży TelemediGO w newsletterze (225 zakupów w 23 dni wobec zwykłego tempa 29) to 196 zakupów, czyli 17,4 tys. zł. Bez niej marża III kwartału 2026 jest o 1,1% wyższa niż rok wcześniej; bez całej sprzedaży w newsletterze w obu latach o 2,3% niższa. Odporne: marża przed kosztem kampanii +25,2% (bez nadwyżki +32,6%) przy wydatkach na kampanie 2,08 raza wyższych; za cały rok marża +26,6% (828 → 1 048 tys. zł), marża przed kampaniami +41,5%, wydatki +76,7%. Werdykt „wydatki na kampanie rosną dużo szybciej niż marża przed ich kosztem” trzyma się i za rok, i za III kwartał. Baza powracających w III kwartale: bez nadwyżki startu 97,8 tys. zł w 2025 wobec 106,2 tys. zł w 2026 (+8,6%), bez całej sprzedaży w newsletterze +1,0%. Zdanie „baza dała mniej marży niż rok wcześniej” trzeba więc zmienić.
3. **Marża na powtórne zamówienie: potwierdzone.** Spadek o 3,05 zł (35,86 → 32,81 zł) to w 89% (2,71 zł) rosnący udział wizyt ze zniżką TelemediGO: z 34,3% do 41,6% powtórnych zamówień. Wizyta ze zniżką zostawia 11 zł marży, bez zniżki 49 zł, a u specjalistów ze zniżką marża jest ujemna (−5,6 zł). W obrębie rodzaju zniżki marża prawie stoi (−0,35 zł).
4. **Lejek osób, które jeszcze nie kupowały: nowa, ostrzejsza odpowiedź.** Płaci 9,3% ich sesji wobec 11,2% rok wcześniej (265 264 i 144 813 sesji). Do stycznia 2026 poziom stoi (11,0–11,6% miesięcznie). Spadek rok do roku zaczyna się w lutym 2026 (−1,6 punktu; start TikToka 9.02, sesje nowych kampanii ponad 30% ruchu nowych osób) i pogłębia się od kwietnia 2026 (−2,3 do −3,1 punktu; po awarii Safari 17.03, nowe kampanie 42–47% sesji). Bez sesji nowych kampanii konwersja nowych osób stoi: 11,2% → 11,4%. Sesje nowych kampanii płacą w 5,5%. **Zdanie o przeglądarkach w aplikacjach nazywa złą grupę:** „4,8–7,2% wobec 16,1–18,1%” to wszystkie sesje, a nie osoby, które jeszcze nie kupowały (u nich 3,8–6,6% wobec 9,9–12,2%).
5. **Pozycja 7: potwierdzone.** 3,16% i 18,84% to podział tej samej grupy (powrót 22,0%) według drogi powrotu: 14% powrotów idzie w 24 godziny po wejściu z newslettera albo SMS-a. 23,6 tys. zł za punkt procentowy to marża do 180. dnia (95,6 zł = różnica marży w dniach 1–180).
6. **Pozycja 4:** kryterium jak w teście Mety: wszyscy nowi pacjenci z pierwszą wizytą u specjalisty (3 427 rocznie, około 66 tygodniowo) i marża po wydatkach. Pauza się opłaca, dopóki ubywa mniej niż około 31 nowych pacjentów tygodniowo (wydatki 53,2 tys. zł / marża 32,4 zł na pacjenta w 90 dniach); kampania przypisuje sobie 13–18 tygodniowo.
7. **Pozycja 5:** sama nowa kreacja (wariant B: uczciwa obietnica odstrasza pacjentów, którzy nie dostaliby L4) to 10,7–18,1 tys. zł rocznie; zmiana zasad zwrotów przy odmowie L4 (wariant A: wizyta zostaje opłacona) 26,7–46,5 tys. zł. To dwa scenariusze tych samych zwrotów, nie do sumowania.
8. **Test TelemediGO:** koszt testu (3,3–12,2 tys. zł) jest policzony przy obecnym zachowaniu, czyli przy niezmienionej liczbie wizyt (`c_priorytety.txt`, P10).
9. Zdanie o miejscu testu Mety — do tekstu.
10. Drobne: stawka pediatry wypada z niewiadomych (założenie 33 oparte na zadaniu: „100 zł każdy inny specjalista”), wariant 25 zł w szczegółach pozycji 10; kampanie na markę i remarketing: 37,1% i 24,1% zamówień w ich sesjach to zamówienia powtórne, których rachunek kosztu pozyskania nie liczy, więc wynik jest ostrożny; godzina bez danych: zamówień w tej godzinie jest zwykle około 2 (mediana z 15 dni), więc ich brak niewiele mówi, a przyczyny (przerwa w działaniu strony czy w zbieraniu danych) nie znamy; słownik danych mówi tylko, że sesja zalogowana od wejścia nie ma kroku logowania, a nie, że powinna kończyć się zakupem.

## 5. Postęp

- Część 1 policzona (punkt 4). Część 2 w toku.
