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


## 2026-10-19 — wykonanie punktu A5 w dwóch sesjach

**Decyzja Kuby:** A5 robią dwie sesje równoległe, z podziałem na retencję i pozyskanie. Zakres każdej, zatrzymania i zasady są w `PLAN.md`, sekcja A5, punkt „Wykonanie A5”. Żadna sesja nie przebudowuje bazy, każda pisze we własnych plikach, a wspólne notatki scala sesja prowadząca.

**Dlaczego taki podział (Kuba):** sesja proponowała podział na kohorty z zdarzeniami i lejek z tym, co po zakupie. Kuba połączył to, co dzieje się po zakupie, z retencją, bo przebieg wizyty może zmieniać powroty. Lejek liczy się na sesjach, więc sesja pozyskania nie musi czekać na wspólny moduł definicji.

**Korekta po uwadze Kuby:** w podsumowaniu A4 napisałem, że sama zmiana struktury źródeł nie tłumaczy spadku powrotu w Mecie (z 20,7% do 6,7% w 90 dniach). To hipoteza, nie wniosek: w drugim roku w Mecie pojawiła się nowa kampania na L4 (`meta_prosp_l4_szybko`, od 3.11.2025). Spadek sprawdzamy na poziomie kampanii, a strukturę rozdzielamy co najmniej po kampanii, pierwszej usłudze, zniżce i przebiegu pierwszej wizyty.

## 2026-10-19 — wyniki części pozyskania (punkt A5)

**Decyzja Kuby:** wyniki części pozyskania przyjęte do scalenia, z dwoma dopiskami. Sesja prowadząca scaliła: założenia 28–32, znaleziska (sekcja A5, pozyskanie), plan (punkty B i C), spis skryptów. Pełny opis: `notatki/a5_pozyskanie.md`, sekcja 8.
1. Nagłówek „konwersja spadła, bo zmienił się ruch” nie może gubić awarii zakładania konta w Safari na iOS od 17.03.2026 ani tego, że przeglądarki wbudowane w aplikacje tracą na każdym kroku. To problemy do naprawienia na stronie, a nie tylko „inny ruch”. Ta sama zasada obowiązuje w narzędziu i na liście priorytetów.
2. Do niewiadomych dochodzi strata między kliknięciem reklamy a sesją w Meta i TikToku.

## 2026-10-19 — szkielet narzędzia (punkt B) przed końcem A5

**Decyzja Kuby** (przekazana dosłownie przez pierwszą sesję projektu): „Kiedy scalisz część pozyskania, nie czekaj na koniec retencji. Zacznij szkielet narzędzia (punkt B): układ strony, lejek, oś zdarzeń i jakość danych. Kohorty dołożymy po drugim zatrzymaniu sesji retencji.”

**Co to zmienia w planie:** punkt B startuje przed końcem A5. Pierwsza wersja narzędzia obejmuje układ strony, lejek, oś zdarzeń i jakość danych. Kohorty dochodzą po drugim zatrzymaniu sesji retencji. Technologię strony sesja B uzgadnia z Kubą na swoim pierwszym zatrzymaniu.

**Warunki do czasu wyboru hostingu** (hosting wybiera Kuba w pierwszej sesji projektu): same pliki statyczne, ścieżki względne, nawigacja przez kotwice w adresie (`#lejek`, `#zdarzenia`), bez serwera. Dane jako statyczne pliki obok strony, każdy poniżej 25 MB, całość jak najlżejsza. Biblioteki zapisane w repozytorium w przypiętej wersji, nie pobierane z sieci. Meta `noindex` i `robots.txt` blokujący indeksowanie. Podgląd lokalny przez `python -m http.server` uruchomiony z folderu `narzedzie/`. Publikacja, dodanie zdalnego repozytorium i push wymagają za każdym razem zgody Kuby.

**Własność plików:** sesja B pisze tylko w `narzedzie/`, we własnym skrypcie eksportu `analiza/b_eksport.py` (z wynikami `analiza/wyniki/b_*`) i we własnej notatce `notatki/b_narzedzie.md`. Nie rusza plików sesji retencji ani pozyskania. Wspólne notatki dalej scala sesja prowadząca.

## 2026-10-19 — hosting narzędzia i repozytorium

**Decyzja Kuby** (przekazana dosłownie przez pierwszą sesję projektu): „Wybieram GitHub: neutralna organizacja, repozytorium prywatne do dnia wysyłki, potem publiczne z GitHub Pages. Założę organizację i podam nazwę.”

**Szczegóły zatwierdzone przez Kubę:**
- Jedno repozytorium w nowej organizacji o neutralnej nazwie, bez nazwiska Kuby i najlepiej bez słowa „Telemedi”. Organizację zakłada Kuba i podaje jej nazwę.
- Narzędzie stoi na GitHub Pages z tego samego repozytorium, pod adresem w rodzaju `https://<organizacja>.github.io/<repozytorium>/`, czyli pod podścieżką. Ścieżki względne są obowiązkowe.
- Publikację robi plik w `.github/workflows/` z oficjalnymi akcjami GitHub Pages (`configure-pages`, `upload-pages-artifact`, `deploy-pages`), który publikuje folder `narzedzie/` przy każdym commicie na master. Plik może powstać już teraz, a zadziała dopiero po włączeniu Pages. Przygotowuje go sesja punktu B.
- Do dnia wysyłki repozytorium jest prywatne i służy jako kopia zapasowa. W dniu wysyłki przełączamy je na publiczne, włączamy Pages i sprawdzamy oba linki (repozytorium i narzędzie) przed wysłaniem maila. Po rekrutacji repozytorium wraca do prywatnych.
- Kuba loguje gita na swoim komputerze do konta GitHub. Utworzenie zdalnego repozytorium, dodanie go do gita, pierwszy i każdy kolejny push, zmiana widoczności i włączenie Pages wymagają osobnej zgody Kuby przy każdej akcji.
- Kuba wie, że publiczna historia commitów pokaże jego imię i nazwisko oraz adres e-mail z ustawień gita. Historii nie przepisujemy.
- Sprawdzenie przed publikacją (pierwsza sesja projektu, 2026-10-19): 60 plików, historia 1,3 MB, surowe dane, paczka i baza DuckDB nie są śledzone, a pliki CSV w `analiza/wyniki/` to zestawienia dzienne bez wierszy pojedynczych pacjentów. **Przed przełączeniem na publiczne sprawdzenie powtarzamy na aktualnym stanie** (punkt D).
- Warunki techniczne strony z wpisu „szkielet narzędzia (punkt B) przed końcem A5” zostają: `noindex`, `robots.txt`, biblioteki w repozytorium w przypiętej wersji, każdy plik danych poniżej 25 MB.

## 2026-10-19 — wynik kroku 3 retencji A5 (struktura a zachowanie)

**Decyzja Kuby:** wynik przyjęty z poprawkami po recenzji Codeksa (Sol), z trzema dopiskami (tekst z notatki sesji retencji):

1. **Zapis na teraz:** większość spadku powrotów wiąże się z pacjentami dwóch nowych kampanii na L4, ale w kampaniach działających w obu latach też jest spadek, którego sprawdzone cechy nie tłumaczą. Podział zależy od reguły źródła, więc w notatkach i w narzędziu podajemy obie wersje (pierwsze wejście z kodem kampanii: 4,6 i 2,0 punktu; sesja płatności: 3,0 i 3,5 punktu).
2. **„Przebieg pierwszej wizyty” w kroku 3 to był tylko status, bez punktualności.** W kroku 4 najpierw: czy spadek w starych kampaniach siedzi w pierwszych wizytach, które zaczęły się z opóźnieniem, według godziny i specjalizacji, zwłaszcza u internisty rano. Czy opóźnienia rosną od startu kampanii na L4 (3.11.2025) i przy kolejnych skokach jej ruchu (17.11, 8.12.2025, 2.01, 19.01.2026 — notatka sesji pozyskania) oraz od startu TikToka (9.02.2026). **Hipoteza Kuby do sprawdzenia, nie do założenia:** nowe kampanie przeciążyły internistów w godzinach, w których przychodzą też pozostali pacjenci. Jeśli tak, koszt tych kampanii obejmuje też gorszą retencję pozostałych pacjentów.
3. **Spadek w starych kampaniach jest w listopadzie–styczniu i w marcu–maju, nie w październiku i lutym.** Przy zdarzeniach w kroku 5 zestawiamy te miesiące z datami startu i skoków kampanii na L4 oraz z opóźnieniami wizyt.

## 2026-10-19 — wyniki kroków 4 i 5 retencji A5 (przebieg wizyty, zdarzenia)

**Decyzja Kuby:** wyniki przyjęte po poprawkach z recenzji Codeksa (Sol), z czterema dopiskami (tekst z notatki sesji retencji):

1. **Kontrolę Codeksa Kuba czyta inaczej:** to, że przy tej samej liczbie wizyt w godzinie obecność pacjentów nowych kampanii nie zmienia opóźnień, jest oczekiwanym wynikiem przy przeciążeniu, bo lekarza nie obchodzi, skąd przyszedł pacjent. Hipotezę rozstrzyga co innego: (a) odsetek spóźnionych porannych wizyt u internisty przy tym samym porannym ruchu w dniu, okres 1 wobec okresu 2; (b) czy w obrębie miesiąca dni z większym ruchem mają więcej opóźnień. Jeśli przy tym samym ruchu opóźnień jest teraz dużo więcej, to spadła poranna przepustowość (obsada, organizacja zapisów albo lekarze zajęci pacjentami spoza B2C), a nie tylko przybyło pacjentów; zapisać jako odczytanie, bez przesądzania przyczyny. **Policzone:** (a) +26,4 punktu procentowego przy tym samym ruchu; (b) brak wyraźnej zależności od ruchu w obrębie miesiąca (krok 4a).
2. **Do listy niewiadomych:** grafiki lekarzy i ich obciążenie spoza B2C. Telemedi ma też pacjentów firmowych, których w tych danych nie ma, a lekarze mogą być wspólni.
3. **Do znalezisk (ważne dla listy priorytetów):** zwroty po wizytach L4 w nowych kampaniach i niska zgoda marketingowa ich pacjentów.
4. **Niespójność lutego zostaje jako trop eksploracyjny**, tak jak opisany w kroku 5.

**Scalenie:** sesja prowadząca scaliła część retencji we wspólnych notatkach: założenia 33–38, znaleziska (sekcja A5, retencja), plan (B i C), przekazanie, spis skryptów. Moduł `analiza/definicje.py` przejmuje sesja prowadząca.


## 2026-10-20 — nowa sesja prowadząca i szkic punktu C na poranny przegląd

**Decyzja Kuby:** po scaleniu ekonomii kampanii rola sesji prowadzącej przechodzi do nowej sesji, bo dotychczasowa jest już długa (zasada 60% kontekstu, `CLAUDE.md` punkt 14). Nowa sesja przygotowuje na poranny przegląd Kuby szkic punktu C:
- **najpierw brakująca analiza TelemediGO:** skąd wzrost sprzedaży o 40%; ile dają opłaty wobec zniżek udzielonych na wizytach; czy wizyty ze zniżką u specjalistów pokrywają koszt lekarza; czy TelemediGO zmienia powroty, z zastrzeżeniem samoselekcji (kupują je pacjenci, którzy i tak planują wracać);
- **lista priorytetów** od najważniejszego, każda pozycja z wartością w marży i założeniami, sposobem pomiaru i czasem wdrożenia, a przy słabych wynikach obie drogi: naprawić albo wyłączyć;
- **lista „czego nie da się rozstrzygnąć”**, z testem przy każdej pozycji;
- **propozycja ostatecznej odpowiedzi „czy to wzrost”** do akceptacji Kuby.

O rundzie konsylium na liście priorytetów Kuba decyduje rano.

**Jak wykonane:** sesja ekonomii kampanii jeszcze wprowadzała uwagę Kuby z przeglądu, gdy przyszła ta decyzja. Żeby nie tracić czasu i nie mieć dwóch piszących we wspólnych notatkach, nowa sesja prowadząca startuje od razu, od analizy TelemediGO we własnych plikach. Ekonomię scala dotychczasowa sesja prowadząca po przyjęciu wyników przez Kubę. Potem jedną wiadomością przekazuje nowej sesji wspólne notatki i całą rolę.

## 2026-10-20 — wyniki ekonomii kampanii (punkt A5)

Decyzja Kuby: wyniki przyjęte do scalenia, z jednym dopiskiem. W narzędziu i przy priorytetach obok wyniku po 90 dniach pokazujemy też wynik po 180 dniach. Pacjenci kampanii na L4 prawie nie wracają, a pozostali tak, więc okno 90 dni zaniża wartość pozostałych kampanii. Recenzja Codeksa (Sol) uwzględniona przed przeglądem: `notatki/recenzje/a5e_codex.md`. Pełny opis: `notatki/a5_ekonomia.md`.

**Scalenie:** sesja prowadząca scaliła ekonomię kampanii we wspólnych notatkach: założenia 39–43, znaleziska (sekcja ekonomia kampanii), plan (B i C), spis skryptów. Punkt A5 jest zamknięty w całości.

## 2026-10-20 — przegląd szkicu punktu C

**Decyzja Kuby:** szkic dobry, kierunek przyjęty (`notatki/c_szkic.md`, commit `bae2920`), z czterema dopiskami (brzmienie Kuby, lekko skrócone):

1. **Odpowiedź „czy to wzrost”:** dodać marżę po kwartałach rok do roku, z wydatkami na kampanie obok. W tabeli miesięcznej narzędzia w VII–IX 2026 marża jest niższa niż rok wcześniej, przy ponad dwa razy wyższych wydatkach. Policzyć to naszym kodem; jeśli się potwierdzi, to zdanie zamyka odpowiedź.
2. **Nowa pozycja listy priorytetów „naprawić pomiar”:** dashboard bez duplikatów i kont testowych, przychód po zwrotach, wyjaśnić i zamknąć kod TEST-QA, sprawdzić, czy lekarze dostają wynagrodzenie za wizyty testowe. Pewna i tania, a bez niej nie da się prowadzić biznesu na kohortach. Wysoko, zaraz po Safari na iOS.
3. **Poranna przepustowość internistów wyżej,** przed test zalogowanych i test Meta. To jedyna dźwignia na retencję pacjentów z kanałów działających w obu latach, a pierwszy krok (grafiki i obsada) jest tani.
4. **Konsylium na liście priorytetów: tak.** Przed wysłaniem dopisać do briefu kandydata „pomiar” i do kontekstu fakt o marży w ostatnim kwartale. Wynik pokazać jako wynik, a nie przegląd modeli.

**Dalej:** po konsylium ostateczna wersja listy do akceptacji Kuby. Po akceptacji odpowiedź, priorytety i niewiadome przekazujemy sesji B do narzędzia.

## 2026-10-19 / 2026-10-20 — narzędzie (punkt B): technologia, układ, druga wersja

Scalone przez sesję prowadzącą z `notatki/b_narzedzie.md` (sekcje 1, 8, 10 i 11), po przyjęciu drugiej wersji przez Kubę.

**2026-10-19, pierwsze zatrzymanie — decyzje Kuby:**
- strona HTML z biblioteką uPlot 1.6.32 zapisaną w repozytorium; odrzucone: ECharts i wykresy bez biblioteki;
- zakładki jak w aplikacji; odrzucone: jedna długa strona;
- wstępna odpowiedź „czy to wzrost” z liczbami A3 i A4; odrzucone: samo miejsce „w przygotowaniu”;
- cztery zasady dla strony: odsetek zawsze z liczebnością i okresem, żadnych liczb wpisanych ręcznie w tekstach, oś zdarzeń w czterech obszarach, próbna publikacja we wtorek wieczorem (po zgodzie Kuby).

**Folder danych strony to `narzedzie/dane_strony/`,** bo `.gitignore` wyklucza każdy folder o nazwie `dane/`. Sesja B zaproponowała zmianę reguły na `/dane/`. **Decyzja sesji prowadzącej: zostawiamy `dane/`,** bo szersza reguła lepiej chroni przed przypadkowym dodaniem surowych danych do repozytorium, a nazwa `dane_strony/` nic nie kosztuje.

**2026-10-20, przegląd szkieletu (słowa Kuby):** „Przejrzałem szkielet i przyjmuję go. A5 jest zamknięte i scalone, więc dobuduj teraz pozostałe zakładki z wyników A5. Kohorty: kohorty dzienne i powroty w 30, 60 i 90 dniach, z filtrami źródło (obie reguły), urządzenie i przeglądarka, pierwsza usługa, zniżka i TelemediGO. Po zakupie: punktualność według pory i specjalizacji, zwroty, oceny. Wynik biznesu: przychód i marża w czasie oraz ekonomia kampanii według obu reguł. Na osi zdarzeń dołóż zdarzenia z retencji i obsługi pacjenta. Priorytety i niewiadome zostaw jako miejsca na wynik punktu C. Te same zasady co dotąd: liczebność przy każdym odsetku, żadnych liczb wpisanych ręcznie. Nic nie publikuj. Zatrzymaj się u mnie z całością rano.”

**2026-10-20, trzy poprawki Kuby do drugiej wersji** (commit `8f7f461`):
1. „Po zakupie” nie mówi już, że dane „pasują do hipotezy przeciążenia, ale jej nie dowodzą”. Pokazuje przyjęte odczytanie: przy tym samym porannym ruchu opóźnień jest o 26,4 punktu procentowego więcej niż rok wcześniej, więc spadła poranna przepustowość (obsada, organizacja zapisów albo lekarze zajęci pacjentami spoza B2C).
2. W „Kohortach” doszła macierz kohort (tygodnie albo miesiące × 7, 14, 30, 60, 90 i 180 dni, mapa ciepła) i krzywa powrotu według dnia od pierwszego zakupu dla okresów A i B, z tymi samymi filtrami.
3. „Wynik biznesu” pokazuje marżę po kwartałach rok do roku z wydatkami obok. Nagłówek mówi, że suma roczna (+26,6%) ukrywa spadek w III kwartale 2026. Strona dokładnie opisuje, że lipiec 2026 jest jeszcze wyższy niż rok wcześniej, i że wrzesień 2025 zawyża bazę przez start sprzedaży TelemediGO w newsletterze.
- Ze strony zniknęły wzmianki o Kubie (stronę czyta Telemedi).

**2026-10-20, decyzja Kuby (słowa Kuby):** „Przejrzałem poprawki i przyjmuję drugą wersję narzędzia. Przekaż wynik sesji prowadzącej, żeby scaliła propozycje wpisów z notatki b_narzedzie.md.” Commit przyjęcia: `c9e1621`. Na stronie zostają do uzupełnienia: „Priorytety”, „Czego nie wiemy” i ostateczna odpowiedź „czy to wzrost” (dziś ze znacznikiem „wstępne”) — po akceptacji punktu C.

## 2026-10-20 — punkt C przyjęty: ostateczna lista priorytetów

**Decyzja Kuby:** ostateczna lista 12 priorytetów i 18 niewiadomych przyjęta (`notatki/c_szkic.md`, sekcje 3 i 4), razem z odpowiedzią „czy to wzrost” (sekcja 1). Przed przeniesieniem do narzędzia pięć poprawek spójności (kwoty w niewiadomych 1 i 3, przebieg porannych opóźnień w pozycji 6, numeracja w sekcji 1c, opis punktu C w planie i przekazaniu) — wprowadzone.

**Konsylium (2026-10-20, zgoda Kuby):** 9 z 9 członków, koszt 0,49 USD. Wynik: `notatki/konsylium/c_priorytety/synteza.md`. Co zmieniło na liście: wstrzymanie TikToka i Google Ads na specjalistów wyżej, obietnica L4 tylko w Meta i niżej, nowa pozycja „komunikacja po wizycie z grupą kontrolną”, cennik specjalistów dołączony do warunków TelemediGO, alarmy w pomiarze, zasada budżetu. Zarzuty sprawdzalne w danych sprawdziliśmy kodem; najważniejsza poprawka: kwoty nowych kampanii przeliczone na pełny rok (założenie 53).

**Kto przenosi wynik do narzędzia:** sesja B jest zamknięta, więc robi to nowa sesja „Narzędzie: czy to wzrost, priorytety i niewiadome” (`local_0ea34a6a-6b84-45c6-87b7-e953f33e3452`), zaproponowana przez sesję prowadzącą i uruchomiona przez Kubę. Pisze w plikach narzędzia, wspólnych notatek nie edytuje, zatrzymuje się u Kuby przed próbną publikacją. Sesja prowadząca: `local_ca1efb6a-0cb9-4abb-b08b-9d90f7e7de79`.

**Równolegle (decyzja Kuby):** końcowa weryfikacja liczb Codeksem (model Astra) i README repozytorium dla Telemedi.

## 2026-10-20 — końcowa weryfikacja liczb (Codex, model Astra)

**Decyzja Kuby:** weryfikacja Astrą przed wysłaniem (punkt D). **Wynik:** 45 liczb przeliczonych niezależnie, wszystkie zgodne, bez błędu krytycznego. Siedem ważnych i osiem drobnych uwag dotyczyło pewności zdań i spójności wycen. Wszystkie przyjęte i wprowadzone przez sesję prowadzącą, bez zmiany kierunku żadnego wniosku. Szczegóły: `notatki/recenzje/d_astra.md`. Do odpowiedzi „czy to wzrost” doszło zdanie, że liczba osób powracających w 90 dniach rośnie (3 076 → 3 289), a spada odsetek.

## 2026-10-20 — trzecia wersja narzędzia: wynik punktu C na stronie

Scalone przez sesję prowadzącą z `notatki/b_narzedzie.md` (sekcje 12 i 13). Pracę wykonała sesja „Narzędzie: czy to wzrost, priorytety i niewiadome” (`local_0ea34a6a-6b84-45c6-87b7-e953f33e3452`).

- **Co doszło:** ostateczne „czy to wzrost” bez znacznika „wstępne”, 12 priorytetów z kartami i 18 niewiadomych, za szkicem `notatki/c_szkic.md` w wersji z uwagami Astry (`8ebd2a4`). Liczby na stronie odczytuje z raportów skrypt `analiza/b2_eksport_c.py` i porównuje każdą liczbę z każdego zdania ze szkicem (commity `77c2aef`, `cfa8c57`).
- **Trzy poprawki Kuby (słowa Kuby):** „1. W zakładce »Priorytety« daj na górę tabelę przeglądu, a zasady listy i definicje pod nią. Czytelnik ma najpierw zobaczyć, co robimy. 2. Osobnej zakładki o TelemediGO nie rób. Dodaj za to krótką kartę w »Czy to wzrost«: skąd +40%, czy rośnie odsetek kupujących, ile dają opłaty wobec zniżek i że rozstrzygnie to test z pozycji 12. To jedna z czterech liczb dashboardu, więc odpowiedź powinna ją objąć. 3. W niewiadomej 1 dopisz horyzont tak jak w pozycji 9 (90 i 180 dni).” Wykonane w `f584585`, kontrola 93 liczb, 0 różnic.
- **Decyzja Kuby (słowa Kuby):** „Przyjmuję trzecią wersję, przekaż to sesji prowadzącej. Publikacji na razie nie robimy. To będzie ostatni krok przed wysłaniem, osobno.” Commit przyjęcia: `df4d23c`. Punkt B jest zamknięty co do treści. Publikacja (próbna i właściwa) to ostatni, osobny krok przed wysłaniem, za zgodą Kuby przy każdej akcji.

## 2026-10-20 — konsylium: końcowa weryfikacja całego rozwiązania

**Zlecenie Kuby:** „konsylium z Fable” w dwóch rolach naraz: weryfikator (spójność liczb, definicje, wnioski, pominięcia) i osoba, która zleciła zadanie. Opus i Fable dodatkowo przeszli narzędzie i repozytorium i przeliczyli liczby z bazy, tylko do odczytu. Brief: `notatki/konsylium/d_weryfikacja/brief.md` (składany skryptem `zbuduj_brief.py`, z tekstami zakładek z commitu `06ba9b8`).

**Wynik** (`notatki/konsylium/d_weryfikacja/synteza.md`): błędu krytycznego nie ma, odpowiedź i główne liczby się potwierdziły. Lista 22 poprawek i drobnych uwag od najważniejszej czeka na decyzję Kuby, co robimy przed wysyłką. Koszt rundy 2,17 USD, 8 z 10 członków odpowiedziało.

## 2026-10-21 — poprawki po konsylium robi nowa sesja prowadząca

**Decyzja Kuby:** robimy całą listę poprawek z syntezy konsylium (`notatki/konsylium/d_weryfikacja/synteza.md`), z jego dwunastoma uwagami. Pełne brzmienie: `notatki/d_poprawki.md`. Każda nowa liczba przez nasz kod i kontrolę zgodności, na końcu Codex przelicza nowe liczby jeszcze raz. Publikacji jeszcze nie robimy. Sesja zatrzymuje się u Kuby z gotowym pakietem.

**Nowa sesja prowadząca:** dotychczasowa sesja prowadząca (`local_ca1efb6a-0cb9-4abb-b08b-9d90f7e7de79`) ma prawie 80% kontekstu, więc według zasady z `CLAUDE.md` (punkt 14) przekazuje rolę nowej sesji. Nowa sesja sama decyduje, czy podzielić pracę na dwie sesje naraz (kod strony osobno, teksty i liczby osobno).

## 2026-10-21 — poprawki po konsylium: jak je zrobiliśmy

**Podział pracy (decyzja sesji prowadzącej `local_791c102e-55e1-4a1b-bb12-d2b0200168ad`, zgodnie z decyzją Kuby, że sama wybiera):** dwie sesje naraz. Kod strony zrobiła sesja narzędzia (`local_0ea34a6a-6b84-45c6-87b7-e953f33e3452`), bo zna ten kod, a poprawki wyświetlania nie czekały na nowe liczby. Teksty, liczby i notatki zrobiła sesja prowadząca. Wątpliwości Kuby policzyli trzej agenci w tle, każdy we własnym, nowym skrypcie (`analiza/d_retencja.py`, `d_kampanie.py`, `d_wynik.py`). Każdy wynik sesja prowadząca sprawdziła w raporcie, zanim wpisała zdanie. Interfejs między sesjami: `notatki/c_szkic.md` (teksty zakładek C, kontrola zgodności), `notatki/d_teksty_strony.md` (pozostałe zakładki) i raporty `analiza/wyniki/d_*.txt` z plikami `d_*.json`.

**Wątpliwości Kuby — wynik (szczegóły: `ZNALEZISKA.md`, sekcja z 2026-10-21):**
- opóźnienia po godzinach — potwierdzone: jeden blok 5:00–12:59, południe i noc to jego brzegi;
- poranek — opóźnienie od pierwszej wizyty dnia, bez narastania; odczytanie „spadła przepustowość” zawężone do stałego przesunięcia od początku dnia, przyczyna otwarta;
- przeglądarki w aplikacjach poza Metą i TikTokiem — nie płacą tak samo w ruchu osób, które znają stronę, więc nie uogólniamy; nowa niewiadoma 19;
- TikTok po 180 dniach — liczony tylko z wczesnych kohort; cały rocznik w przybliżeniu ujemny w obu regułach, więc pewność co do znaku zostaje (z opisem, skąd liczba);
- pediatra i psychiatra — „bez istotnej zmiany” (założenie 56);
- spadek marży III kwartału — luka po odjęciu TelemediGO to wyższe wydatki kampanii działających w obu latach; Safari w niej się nie mieści i jest liczone jako strata zaksięgowana w kwartale (założenie 58);
- test Mety — 4–6 tygodni nie odróżni wyniku od progu; obok progu 85% próg po naprawie zwrotów 70%; reguła na wynik niejednoznaczny ustalona z góry (założenie 59).

**Reguła na wynik niejednoznaczny testu Mety (propozycja sesji prowadzącej, do zatwierdzenia przez Kubę przy przeglądzie pakietu):** decyduje oszacowanie punktowe (poniżej progu wyłączamy, powyżej zostawiamy). To świadomie przyjęta reguła decyzji przy dużej niepewności, a nie rozstrzygnięcie statystyczne (po recenzji Codeksa wycofaliśmy uzasadnienie „oczekiwaną marżą”, bo wymagałoby osobnego modelu). Inne warianty (status quo przy przedziale obejmującym próg, połowa budżetu, przedłużanie testu) są w `analiza/wyniki/d_wynik.txt`, 3e.

**Recenzja Codeksa (Sol) nowych liczb:** 34 z 35 liczb zgodnych; jeden błąd jednostki (próg Mety w pacjentach dotyczy 332 dni działania, a nie roku) i 11 uwag do brzmienia zdań — wszystkie przyjęte i wprowadzone w szkicu, w tekstach strony i w notatkach. Szczegóły: `notatki/recenzje/d2_codex.md`.

**Bez zmian na stronie:** `robots.txt` zostaje; indeksowanie blokuje znacznik `noindex`, a `robots.txt` pod podścieżką GitHub Pages nic nie daje (konsylium, drobne).

**`CLAUDE.md`:** usunięty adres e-mail osoby rekrutującej (punkt 12 listy Kuby). Historii nie przepisujemy, więc adres zostaje we wcześniejszych commitach.

## 2026-10-21 — Kuba przyjmuje pakiet poprawek po konsylium

**Decyzja Kuby (słowa Kuby):** „Przejrzałem pakiet, przyjmuję go razem z regułą testu Mety. Jedna rzecz: w »Czy to wzrost« dwa razy stoi, że Safari »nie mieści się w luce«. Ktoś z Telemedi nie będzie wiedział, o jaką lukę chodzi. Zostaw kwotę Safari, rozkład spadku marży i zdanie, że wyniku kwartału bez awarii nie mierzymy. Samo »nie mieści się w luce« usuń w obu miejscach. Potem kontrola, commit i daj znać. Publikacji jeszcze nie robimy.”

- **Reguła testu Mety przyjęta:** przy wyniku niejednoznacznym decyduje oszacowanie punktowe (poniżej progu wyłączamy, powyżej zostawiamy); świadomie przyjęta reguła decyzji, a nie rozstrzygnięcie statystyczne (założenie 59).
- **Wykonane:** zdanie „Safari się w tej luce nie mieści” usunięte z dwóch miejsc w „Czy to wzrost” (akapit o Safari w III kwartale i rozkład spadku marży) w `notatki/c_szkic.md` i w `analiza/b2_eksport_c.py`. Kontrola `python -I analiza/b_eksport.py`: 102 z 102 zgodnych, 0 różnic; teksty zakładek odtworzone. W zakładce „Wynik biznesu” zdanie zostaje, bo luka jest tam zdefiniowana w poprzednim akapicie.
- **Następne kroki, każdy za zgodą Kuby:** przegląd zamówień testowych, publikacja, mail.

## 2026-10-21 — „Wynik biznesu” bez „luki” i przegląd zamówień testowych

**Prośba Kuby (słowa Kuby):** „W »Wyniku biznesu« też to przeredaguj. Zamiast zaczynać akapit od tego, że Safari się w luce nie mieści, napisz po prostu, ile szacunkowo kosztowała awaria w III kwartale i że wyniku kwartału bez awarii nie mierzymy. Potem krótki przegląd zamówień testowych, tak jak umawialiśmy się na początku: czy nic się nie zmieniło w tym, jak je traktujemy, i czy to jest domknięte w notatkach. Publikację robimy po tym, osobno.”

- **„Wynik biznesu”:** akapit o Safari zaczyna się teraz od szacowanego kosztu awarii w III kwartale 2026 (14,6–18,3 tys. zł marży, osobno 4,1–4,5 tys. zł powrotów pacjentów utraconych wcześniej) i kończy zdaniem, że wyniku kwartału bez awarii nie mierzymy. Porównania z „luką” nie ma już nigdzie na stronie (`analiza/b2_eksport_c.py`, `notatki/d_teksty_strony.md`).
- **Przegląd zamówień testowych (zastrzeżenie Kuby z A2, punkt D planu): nic się nie zmienia.** Reguła z założenia 7 (konto, które choć raz użyło kodu TEST-QA) jest kompletna i nie zabiera prawdziwych zamówień ani sesji; koszt lekarza za wizyty testowe dalej nie wchodzi do liczb (założenie 8), a wariant z kosztem zostaje niewiadomą 14 i częścią pozycji 2 listy priorytetów. Liczby A2 odtwarzają się co do sztuki. Skrypt `analiza/d_testy.py`, raport `analiza/wyniki/d_testy.txt`, opis: `ZNALEZISKA.md`, A2 punkt 2. Przegląd jest domknięty w założeniach, znaleziskach, planie i przekazaniu.
- **Następny krok:** publikacja, osobno i za zgodą Kuby przy każdej akcji.

## 2026-10-21 wieczorem — ostatnia runda przed publikacją: merytoryka, język, wygląd (punkt E)

**Zlecenie Kuby (pełne brzmienie: `notatki/e_runda.md`, punkt 1):** trzy części w tej kolejności: merytoryka (10 wątpliwości do sprawdzenia kodem), język (nagłówek = wniosek, jedno zdanie, szczegóły zwinięte, jeden słownik), wygląd (granatowy pasek, białe karty, znaczniki stanu z ikoną i słowem, wykres lejka, znaczniki pewności). Na koniec Codex przelicza nowe liczby. Nic nie publikujemy; zatrzymanie u Kuby z gotową wersją.

**Podział pracy (decyzja sesji prowadzącej, za zgodą Kuby na osobną sesję od wyglądu):**
- sesja prowadząca: część 1 (`analiza/e_merytoryka.py`), teksty „Czy to wzrost”, „Priorytety”, „Czego nie wiemy” i nagłówka lejka (`analiza/e_teksty.py`, szkic `notatki/e_teksty.md`), README, notatki;
- agent w tle tej sesji: karty pięciu pozostałych zakładek (`analiza/e_teksty_zakladki.py`, szkic `notatki/e_teksty_zakladki.md`);
- sesja „E: nowy wygląd narzędzia” (`local_61aff6c2-0b67-4a4b-b735-4b3004d7b279`): pliki strony w `narzedzie/` (poza danymi), notatka `notatki/e_wyglad.md`;
- interfejs: kontrakt danych w `notatki/e_runda.md`, punkt 3 (kształt karty i klucze w plikach danych).

**Wynik części 1:** `notatki/e_runda.md`, punkt 4, i `ZNALEZISKA.md` (sekcja z 2026-10-21 wieczorem). Wszystkie wątpliwości Kuby potwierdziły się. Nowe w stosunku do jego przypuszczeń: lejek osób, które jeszcze nie kupowały, daje datę początku spadku (luty 2026) i pokazuje, że bez sesji nowych kampanii konwersja nowych osób nie spada; zdanie o przeglądarkach w aplikacjach podawało liczby wszystkich sesji jako liczby osób, które jeszcze nie kupowały; brak zamówień w „godzinie bez danych” niewiele mówi, bo zwykle są w niej około 2 zamówienia.

**Decyzje w tekstach (założenia 64–69):** reguła przyjęta w opisie pacjentów i retencji, sesja płatności w szczegółach; na górze „Czy to wzrost” zamiast spadku marży III kwartału fakt odporny (marża przed kosztem kampanii +25%, wydatki 2,08 raza wyższe) i marża za cały rok (+27%); lejek domyślnie dla osób, które jeszcze nie kupowały; stawka pediatry jako założenie z zadania (niewiadoma 13 wypada, kolejne przesuwają się o jeden); pozycja 5 rozdzielona na nową kreację (10,7–18,1 tys. zł) i zmianę zasad zwrotów (26,7–46,5 tys. zł); pozycja 4 z kryterium jak w teście Mety; zdanie, dlaczego test Mety stoi na 9. miejscu; test TelemediGO „pokaże wpływ samej zniżki”, a koszt testu jest liczony przy niezmienionej liczbie wizyt.

**Wygląd (sesja `local_61aff6c2`, commit `888ebca`; szczegóły `notatki/e_wyglad.md`):** wszystkie punkty części 3 listy Kuby. Wykres kroków lejka liczony w przeglądarce z danych lejka, domyślnie dla osób, które jeszcze nie kupowały, z wyróżnionym przejściem o największym względnym spadku (założenie 70). Filtry „Po zakupie” i „Wyniku biznesu” są w paskach swoich kart, bo każda karta ma inne filtry. Zdarzenia mają pole `krotko` do list i legend.

**Recenzja Codeksa (Sol) nowych liczb:** 17 z 19 pozycji zgodnych, dwie różnice zaokrągleń poprawione; brzmienia poprawione według jego uwag (`notatki/e_runda.md`, punkt 5; `notatki/recenzje/e_codex.md`).

**Kontrola liczb w zakładkach pomocnika:** szkic `notatki/e_teksty_zakladki.md` powstał z wyniku kodu, więc kontrola była dla tych zakładek pusta. Sesja prowadząca przeczytała teksty i zamroziła szkic jako wzorzec poprawiany ręcznie (generator tylko z flagą `--nadpisz`).

**Integracja (sesja prowadząca, 2026-10-22):** eksport 104 kontrole, 0 różnic; nowe karty 80, każda liczba z pokryciem w szkicach; teksty strony odtworzone (`analiza/wyniki/b_teksty_strony.md`); przeglądarka: 9 zakładek przy 1366 i 375 px, 0 błędów w konsoli, bez przewijania w bok, 296 odnośników działa; zrzuty obejrzane („Czy to wzrost”, lejek z wykresem kroków, priorytety, „Wynik biznesu”, telefon). Dawne kształty tekstów „Czy to wzrost”, „Priorytetów” i „Czego nie wiemy” usunięte z danych strony. Dalej: przegląd Kuby; publikacja i mail tylko za jego zgodą.

## 2026-10-22 — druga lista Kuby po przeglądzie wersji `ccc3c61` (punkt E)

**Zlecenie Kuby:** 15 poprawek merytoryki w tekstach, języka i README, wysłane bezpośrednio do sesji wyglądu (`local_61aff6c2`), do zrobienia w jednym przejściu, potem kontrola liczb, odtworzenie tekstów strony i zatrzymanie u Kuby. Sesja prowadząca na ten czas nie zmieniała plików.

**Wykonanie (commit `4c594b5`, opis: `notatki/e_wyglad.md`, punkt 9):** teksty z danych, szkice i README poprawił agent sesji wyglądu (nowy skrypt `analiza/e_poprawki.py`), kod strony sesja wyglądu. Przeglądarki w aplikacjach opisane jako „do sprawdzenia”, bez pozycji na liście priorytetów. Reguła decyzji testu Mety zostaje (z góry ustalona w rundzie D), z dopisanym ryzykiem; uwagę Codeksa przyjęliśmy częściowo (`notatki/recenzje/e2_codex_odpowiedz.md`). Założenia 71–77.

**Kontrola:** eksport 104 kontrole, 0 różnic, 0 liczb bez pokrycia w szkicach; Codex (Sol) 9 z 9 nowych liczb zgodnych; teksty strony odtworzone; przeglądarka: 9 zakładek przy 1366 i 375 px, 0 błędów, 296 odnośników.

**Lekcja (agent sesji wyglądu):** w kodzie tekstów było kilka liczb wpisanych ręcznie; przechodziły kontrolę, bo stały też w szkicach. Teraz liczy je kod. Zgodność ze szkicem nie wyłapuje liczby wpisanej ręcznie w obu miejscach — przy przeglądzie kodu tekstów trzeba szukać literałów liczbowych w zdaniach.

**Dalej:** przegląd Kuby; publikacja i mail tylko za jego zgodą.

## 2026-10-22 — trzecia lista Kuby (punkt E)

**Zlecenie Kuby (w sesji wyglądu `local_61aff6c2`):** (1) zdanie „poza nowymi kampaniami konwersja się nie zmieniła” gryzie się z awarią Safari — policzyć według pierwszego wejścia, z Safari na iPhone'ach osobno; (2) wydatki w tabeli kwartałów w procentach zamiast „razy”; (3) etykieta wyróżnionego przejścia na wykresie kroków lejka; (4) konkretne wdrożenie pozycji 1 i stopki bez „Runda E”.

**Wykonanie (commit `351f556`, opis `notatki/e_wyglad.md`, punkt 10):** nagłówek lejka zmieniony po sprawdzeniu kodem (hipoteza Kuby potwierdzona, znaleziska z 2026-10-22); po recenzji Codeksa tytuł mówi o składnikach spadku (zmiana ruchu i awaria Safari). Etykieta wykresu kroków „Najbardziej obniża płatności” zamiast „Największy spadek” (prośba Kuby). Założenia 78–82. Kontrole: eksport 0 różnic w 104 kontrolach i 0 liczb bez pokrycia, teksty odtworzone, przeglądarka bez błędów, Codex (Sol) 9 z 9.

**Równolegle:** sesja „E: dopracowanie wyglądu narzędzia z Kubą” (`local_dc5102f3`) pracuje z Kubą nad grafiką; czekała z edycją plików strony na commit trzeciej listy.
