# A5 — ekonomia kampanii (sesja „a5-ekonomia”, 2026-10-19)

Notatka robocza sesji ekonomii kampanii, ostatniej pozycji punktu A5. Wspólnych notatek (`ZALOZENIA.md`, `ZNALEZISKA.md`, `DECYZJE.md`, `PLAN.md`, `PRZEKAZANIE.md`, `analiza/README.md`) ta sesja nie edytuje. Propozycje wpisów są w sekcji 9. Scali je sesja prowadząca.

## Pliki

| Plik | Co zawiera |
|---|---|
| `analiza/a5e_ekonomia.py` → `analiza/wyniki/a5e_ekonomia.txt`, `analiza/wyniki/a5e_kampanie.csv` | Wydatki, prowizja, nowi pacjenci, koszt pozyskania, marża na pacjenta w 90 i 180 dniach, wynik po koszcie pozyskania. Kampanie, kanały i grupy, okres 1 i okres 2, obie reguły źródła. Zestawienie CSV dla narzędzia (bez wierszy pacjentów). |
| `analiza/a5e_scenariusze.py` → `analiza/wyniki/a5e_scenariusze.txt` | Skład marży nowych kampanii na L4, zwroty po wizycie i zgoda marketingowa, scenariusz porannych opóźnień, dodatkowość pacjentów, naprawić albo wyłączyć. Importuje `a5e_ekonomia.py`. |
| `notatki/recenzje/a5e_codex_*.md` | Recenzja Codeksa (model Sol): polecenie, odpowiedź, podsumowanie. |

Oba skrypty uruchamia się z głównego folderu przez `python -I`, każdy w kilka sekund. Tylko czytają bazę. Kontrola: skrypt ekonomii odtwarza liczby części retencji co do dziesiątej części złotówki (12 867 i 18 924 pacjentów, marża 66,6 i 58,3 zł w 90 dniach; 9 125 i 12 591 pacjentów, 75,5 i 67,7 zł w 180 dniach). Skrypt scenariuszy odtwarza wartość powrotu 95,6 zł (założenie 38) i liczby zwrotów po wizycie L4 z `ZNALEZISKA.md` (1 024 z 5 895 i 270 z 5 080).

## W skrócie

1. **Nowe kampanie na L4 pozyskują pacjenta taniej niż reszta kampanii płatnych, ale ten pacjent zostawia prawie o połowę mniej marży.** Według przyjętej reguły źródła wynik na pacjenta w 90 dniach to +3,6 zł, a według sesji płatności −9,4 zł. Znak zależy od reguły, więc to wynik **niepewny**.
2. **Kampania na TikToku ma wynik ujemny w obu regułach** (−4,6 i −17,8 zł na pacjenta w 90 dniach). Kampania Meta na L4 jest niepewna (+6,5 i −6,5 zł).
3. **Niska marża tych pacjentów to kody rabatowe, zwroty po wizycie L4 i prawie zerowe powroty.** Tańszy lekarz (internista) częściowo to równoważy.
4. **Zgoda marketingowa i przeglądarki wbudowane w aplikacje nie są dźwignią dla tych kampanii.** U ich pacjentów zgoda prawie nie zmienia powrotu. Przeglądarki wbudowane konwertują w tych kampaniach nie gorzej niż zwykłe.
5. **Największa dźwignia naprawy to zwroty po wizytach L4.** Gdyby spadły do poziomu pozostałych pacjentów, dawałoby to od 18 do 57 tys. zł marży rocznie (przyjęta reguła).
6. **Czy pacjenci są dodatkowi, dane nie rozstrzygają.** Pozyskanie w pozostałych kanałach po startach kampanii nie spadło wyraźnie. Jest jeden słaby sygnał: przejmowania części pacjentów L4 z Google Ads.
7. **Hipoteza porannych opóźnień, jako scenariusz, kosztuje od 12 do 65 tys. zł marży rocznie.** To od 1,7 do 12,6 zł na pacjenta nowych kampanii, czyli tyle, ile cały ich wynik według przyjętej reguły.

---

## 1. Koszt pozyskania i wynik na pacjenta — nowe kampanie na L4 wobec pozostałych

Okres 2, kohorty z pełnym oknem 90 dni (1.10.2025–2.07.2026). Wydatki pochodzą z tych samych dni. Wynik na pacjenta to marża w 90 dniach minus koszt pozyskania. Przedział 95% liczymy tylko z rozrzutu marży (`a5e_ekonomia.txt`, sekcja 1a; `a5e_scenariusze.txt`, sekcja A).

```
grupa                                reguła          pacjenci  koszt pozyskania  marża 90 dni  wynik na pacjenta (95%)
nowe kampanie na L4 (Meta + TikTok)  przyjęta          4 893        32,7 zł          36,3 zł     +3,6 zł (od +2,5 do +4,7)
nowe kampanie na L4 (Meta + TikTok)  sesja płatności   3 510        45,6 zł          36,1 zł     −9,4 zł (od −10,7 do −8,1)
pozostałe kampanie płatne            przyjęta          7 076        44,2 zł          64,2 zł    +20,0 zł (od +18,8 do +21,2)
pozostałe kampanie płatne            sesja płatności   7 141        43,8 zł          62,4 zł    +18,7 zł (od +17,5 do +19,9)
ranking lekarzy (prowizja)           przyjęta            489        25,0 zł          57,2 zł    +32,2 zł
kanały bezpłatne                     przyjęta          6 466         0,0 zł          68,6 zł    +68,6 zł
wszyscy poza nowymi kampaniami       przyjęta         14 031        23,1 zł          66,0 zł    +42,8 zł
```

- **Okno 180 dni** (kohorty 1.10.2025–3.04.2026, głównie kampania Meta na L4, bo TikTok wystartował 9.02.2026): nowe kampanie +7,0 zł według przyjętej reguły i −5,2 zł według sesji płatności. Pozostałe kampanie płatne +29,7 zł i +27,5 zł.
- **Pełny okres 2** (12 miesięcy, bez marży, bo młode kohorty nie mają pełnego okna). Koszt pozyskania nowych kampanii wynosi 33,8 zł (7 268 pacjentów) według przyjętej reguły i 47,4 zł (5 187 pacjentów) według sesji płatności. Pozostałe kampanie płatne: 45,5 zł i 44,6 zł. W okresie 1 było to 43,0 zł i 46,4 zł.
- **Dlaczego reguły się różnią.** Sesja płatności przypisuje nowym kampaniom o 1 383 pacjentów mniej w 90-dniowej próbie (4 893 wobec 3 510), a przy tych samych wydatkach koszt pozyskania rośnie z 32,7 do 45,6 zł. Ci pacjenci mieli kod kampanii albo pierwsze wejście z kampanii, ale zapłacili w sesji bezpośredniej, z wyszukiwania marki albo z remarketingu. W całym okresie 2 dotyczy to 2 081 z 7 268 pacjentów (`a5e_scenariusze.txt`, D3; `ZNALEZISKA.md`, A4, punkt 6).
- **Wynik całej grupy przez rok** (nowi z 12 miesięcy × marża w 90 dniach − wydatki z 12 miesięcy): +17 849 zł według przyjętej reguły i −58 372 zł według sesji płatności (`a5e_scenariusze.txt`, E0).

## 2. Kampanie po kolei, okres 1 i okres 2

Wynik na pacjenta w 90 dniach, w złotych (`a5e_ekonomia.txt`, sekcje 2a, 2b i 3). Liczby w nawiasach to nowi pacjenci według danej reguły.

```
kampania                    wydatki o1 / o2 (90 dni)   przyjęta reguła: o1 → o2          sesja płatności: o1 → o2        ocena
meta_prosp_l4_szybko        — / 113 677 zł             — → +6,5 (3 628)                  — → −6,5 (2 589)                niepewna (znak zależy od reguły)
tt_prosp_l4_15min           — / 46 220 zł              — → −4,6 (1 265)                  — → −17,8 (921)                 ujemna w obu regułach
gs_generic_erecepta         58 242 / 73 741 zł         +28,6 (1 193) → +15,7 (1 233)     +10,7 (859) → −7,9 (881)        niepewna w okresie 2
gs_generic_lekarz_online    72 141 / 68 786 zł         +14,8 (1 429) → +16,6 (1 399)     −7,9 (985) → −2,8 (1 003)       niepewna
gs_generic_l4               54 841 / 57 180 zł         +14,9 (1 078) → +14,4 (1 072)     −6,4 (758) → −9,1 (743)         niepewna
meta_prosp_lekarz_online    45 530 / 45 855 zł         +6,8 (786) → +6,3 (835)           −11,7 (585) → −11,7 (632)       niepewna
gs_generic_specjalisci      36 086 / 40 319 zł         −27,1 (602) → −23,7 (719)         −50,0 (430) → −44,7 (519)       ujemna w obu regułach
gs_brand                    10 792 / 17 899 zł         +59,9 (1 522) → +56,7 (1 715)     +60,8 (1 927) → +54,9 (2 407)   dodatnia w obu
meta_rmkt_koszyk            4 478 / 8 647 zł           +24,3 (95) → −18,8 (103)          +61,5 (708) → +50,6 (956)       nie oceniamy przyjętą regułą (założenie 24)
ranking lekarzy (prowizja)  12 225 / 12 225 zł         +32,2 (489) → +32,2 (489)         +32,1 (348) → +30,8 (319)       dodatnia w obu
```

- **Prawie wszystkie kampanie płatne, które pozyskują nowych pacjentów, są „niepewne”, a nie tylko nowe kampanie na L4.** Według sesji płatności kampanie Google Ads ogólne i Meta mają w 90 dniach wynik ujemny, a według przyjętej reguły dodatni. To własność reguły. Sesja płatności przenosi pacjentów, którzy przyszli z reklamy, do wejść bezpośrednich, wyszukiwania marki i remarketingu, czyli tam, gdzie zapłacili. Przyjęta reguła zgadza się z kodami kampanii w 97% przypadków, a sesja płatności w 67–71% (założenie 22). Kontrola kodami obejmuje jednak tylko trzy kampanie.
- **Znak zależy też od okna.** W 180 dniach kampanie z powracającymi pacjentami zyskują więcej. Na przykład `gs_generic_lekarz_online` według sesji płatności przechodzi z −2,8 zł w 90 dniach na +10,1 zł w 180 dniach. Nowe kampanie na L4 prawie nie zyskują, bo ich pacjenci prawie nie wracają (marża rośnie z 36,3 do 37,3 zł).
- **`gs_generic_specjalisci` traci w obu regułach i w obu oknach** (−23,7 i −44,7 zł w 90 dniach w okresie 2, −14,3 i −36,6 zł w 180 dniach). Marża pacjenta po 90 dniach wynosi tylko 32 zł. To kandydat do punktu C, poza zakresem tej notatki.
- **`gs_generic_erecepta` drożeje.** Koszt pozyskania według przyjętej reguły rośnie z 48,8 zł do 59,8 zł, a wynik na pacjenta spada z +28,6 zł do +15,7 zł. Kampania wydaje o 15 499 zł więcej przy podobnej liczbie pacjentów.

## 3. Prowizja afiliacyjna

`a5e_ekonomia.txt`, sekcja 4.

- **Przyjęta reguła:** 15 400 zł w okresie 1 (616 pacjentów) i 15 425 zł w okresie 2 (617), razem 30 825 zł. Jak w założeniu 25.
- **Sesja płatności:** 10 925 zł i 10 125 zł, razem 21 050 zł.
- **Kod RANKING10:** 7 500 zł i 7 375 zł, razem 14 875 zł.
- **Wynik rankingu na pacjenta w 90 dniach w okresie 2:**
  - przyjęta reguła: +32,2 zł (marża 57,2 zł minus 25 zł prowizji);
  - wariant RANKING10: +45,1 zł, bo prowizja za 237 kodów rozłożona na 489 pacjentów to 12,1 zł na pacjenta;
  - ranking jest dodatni w każdym wariancie.
- **Zbieżność, którą sprawdziliśmy:** w oknie 90 dni oba okresy mają po 489 pacjentów rankingu i po 237 kodów. Miesiące się różnią, więc to zbieżność sum, a nie błąd. W pełnych okresach liczby też są prawie równe (616 i 617). Ranking daje stałą liczbę pacjentów, a na dane z generatora to wygląda bardziej niż na przypadek. Nie wpływa to na wnioski.

## 4. Skąd niska marża pacjentów nowych kampanii i koszty widoczne tylko u nich

### 4a. Skład marży na pacjenta w 90 dniach

Okres 2, przyjęta reguła, w złotych na pacjenta (`a5e_scenariusze.txt`, A).

```
                             cena   zniżka  zapłata  zwrot  koszt lekarza  TelemediGO  dni 1–90  marża
nowe kampanie na L4          95,9    16,1     79,8   14,7       32,3          1,2         2,2     36,3
pozostałe kampanie płatne   102,6     3,3     99,4    6,0       48,5          5,0        14,3     64,2
```

Różnica 27,9 zł na pacjenta składa się z pięciu części:
- **wyższa zniżka:** −12,8 zł, bo kody L4SZYBKO20 i TIKTOK25 obniżają cenę o 20 i 25 zł;
- **niższa cena katalogowa:** −6,7 zł, bo L4 u internisty jest tańsze niż wizyty u specjalistów;
- **więcej zwrotów:** −8,7 zł;
- **prawie brak powrotów:** −12,1 zł, bo marża dni 1–90 to 2,2 wobec 14,3 zł, przy powrocie 4,1% wobec 21,1%;
- **rzadziej TelemediGO:** −3,8 zł.

Część tej różnicy równoważy tańszy lekarz: koszt lekarza jest niższy o 16,2 zł, bo internista kosztuje 25 zł, a specjalista 100 zł. Według sesji płatności skład jest prawie taki sam.

### 4b. Zwroty po wizycie i koszt lekarza za te wizyty

Okres 2, wszystkie zamówienia pacjentów (`a5e_scenariusze.txt`, B1).

- **Pacjenci nowych kampanii** (przyjęta reguła, 7 268 pacjentów):
  - 1 044 wizyty zwrócone po odbyciu;
  - 84 112 zł zwróconych zapłat i 33 975 zł kosztu lekarza za te wizyty;
  - na pacjenta 11,6 zł zwrotów i 4,7 zł kosztu lekarza, czyli 16,3 zł.
- **Pozostali pacjenci** (17 419): 582 wizyty, 54 420 zł i 26 575 zł, na pacjenta 4,6 zł.
- **Wizyty L4:**
  - nowe kampanie: 17,4% kończy się zwrotem (1 024 z 5 895);
  - pozostali pacjenci w okresie 2: 5,3% (270 z 5 080);
  - okres 1: 6,0% (267 z 4 474);
  - według sesji płatności: 17,6% wobec 8,2%.
- Oba koszty są już w marży z punktu 4a, więc nie odejmujemy ich drugi raz.

### 4c. Zgoda marketingowa

Kohorty okresu 2 do 2.07.2026 (`a5e_scenariusze.txt`, B2).

- **Zgodę ma 37,8% pacjentów nowych kampanii wobec 64,4% pozostałych** (przyjęta reguła). Według sesji płatności 37,9% wobec 61,9%.
- **U pacjentów nowych kampanii zgoda prawie nie zmienia powrotu w 90 dniach:** 4,2% ze zgodą i 4,1% bez niej. Pacjenci ze zgodą wracają w 1,03% przez newsletter albo SMS, a pacjenci bez zgody nie mają takich powrotów wcale. Bez zgody wracają więc prawie tak samo często inną drogą. U kampanii TikTok powrotów przez newsletter i SMS w 90 dniach nie ma wcale.
- **U pozostałych pacjentów różnica jest większa,** ale też mała: 22,6% wobec 20,9%. Przez newsletter albo SMS wraca 6,19% pacjentów ze zgodą.
- **Odczytanie, do oceny Kuby.** Niska zgoda to cecha pacjentów nowych kampanii. Na podstawie tych danych nie jest to osobny koszt w marży. Nie wiemy, czy wiadomości wywołują zakup (lista niewiadomych, punkt 4 w `PLAN.md`, sekcja C).

## 5. Scenariusz hipotezy Kuby: poranne godziny internistów

`a5e_scenariusze.txt`, C. **To scenariusz, nie wynik.**

- **Wartość powrotu:** 95,6 zł marży w dniach 1–180 (założenie 38, odtworzone kodem).
- **Spadek powrotu w 90 dniach u pacjentów starych kampanii** z raportu części retencji (`a5r_zdarzenia.txt`):
  - **tylko zmiana rozkładu opóźnień pierwszej wizyty:** −0,76 punktu procentowego według przyjętej reguły (17 419 pacjentów) i −0,64 punktu według sesji płatności (19 500 pacjentów), czyli 132 i 125 powrotów mniej rocznie, 12 656 zł i 11 931 zł marży;
  - **cały spadek w starych kampaniach (górna granica):** −1,91 i −3,50 punktu, czyli 333 i 683 powroty, 31 806 zł i 65 247 zł marży.
- **Na pacjenta nowych kampanii** (7 268 według przyjętej reguły, 5 187 według sesji płatności) to od 1,7 do 12,6 zł. Kwotę dzielimy na tych pacjentów tylko po to, żeby pokazać rząd wielkości obok wyniku na pacjenta.
- **Co z tego wynika dla wyniku nowych kampanii.** Według przyjętej reguły wynik to +3,6 zł na pacjenta w 90 dniach. Z kosztem z wariantu opóźnień (1,7 zł) zostaje +1,9 zł. Z górną granicą (4,4 zł) wychodzi −0,8 zł. Według sesji płatności wynik jest ujemny bez scenariusza.
- **Dlaczego to tylko scenariusz.** Część retencji pokazała, że przy tym samym porannym ruchu opóźnień jest dużo więcej niż rok wcześniej (+26,4 punktu procentowego). Spadła więc przepustowość poranka, a kampanie mogą nie być przyczyną. Nie wiemy też, czy wyłączenie kampanii podniosłoby powroty pozostałych pacjentów.

## 6. Czy pacjenci nowych kampanii są dodatkowi

`a5e_scenariusze.txt`, D. Według przyjętej reguły, bo sesja płatności z definicji przenosi część pacjentów nowych kampanii do kanałów bezpłatnych.

**Co widać: po startach kampanii pozyskanie w pozostałych kanałach nie spadło wyraźnie. Jest słaby sygnał przejmowania części pacjentów L4 z Google Ads.**

- **Miesiące rok do roku.** Pacjenci pozostałych kanałów rosną rok do roku od 0% do +21% w miesiącach XI 2025 – VIII 2026, a we wrześniu 2026 spadają o 4%. W październiku 2025, przed startem kampanii Meta, wzrost wynosił +8%. Kanały bezpłatne rosną o 4–29% (we wrześniu 2026 spadają o 5%).
- **28 dni przed startem i 28 dni po nim, wobec tych samych dni rok wcześniej.** Iloraz 1,00 znaczy brak zmiany. W nawiasach przedział 95%.
  - **Start Meta na L4 (3.11.2025):**
    - wszyscy pacjenci pozostałych kanałów: 1,04 (od 0,94 do 1,16);
    - pacjenci z inną pierwszą usługą niż L4: 1,12;
    - pacjenci L4 w pozostałych kanałach: 0,81 (od 0,64 do 1,03);
    - kampania Google Ads na L4 (`gs_generic_l4`): 0,67 (od 0,45 do 0,98). To jedyny przedział, który wyklucza brak zmiany.
  - **Start TikToka (9.02.2026):** wszystko lekko poniżej 1. Wszyscy pacjenci pozostałych kanałów 0,91 (od 0,83 do 1,01), L4 0,84. Rok wcześniej w tych dniach nie działała żadna nowa kampania, a w roku startu przez 28 dni przed startem działała już Meta na L4.
- **Przybliżenie.** Bez kampanii udział L4 w pozostałych kanałach byłby taki jak w tym samym miesiącu okresu 1. Wtedy w miesiącach XI 2025 – IX 2026 brakuje 227 pacjentów L4, czyli 3,1% z 7 268 pacjentów nowych kampanii. W październiku 2025, bez kampanii, ten sam wzór myli się o 58 pacjentów w drugą stronę, więc to przybliżenie ma błąd rzędu samego wyniku.
- **Czego te dane nie mówią.** Nie widać pacjentów, którzy bez kampanii wyszukaliby Telemedi sami albo trafiliby do konkurencji. Dane nie pozwalają ich odróżnić od tych, których przyprowadziła reklama. Według przyjętej reguły 163 pacjentów nowych kampanii miało wcześniejsze wejście z innego kanału, a kod kampanii przypisał ich do kampanii.
- **Test rozstrzygający (do listy niewiadomych).** Na 4–6 tygodni wyłączyć albo mocno obniżyć budżet kampanii na L4 w losowo wybranej połowie województw (pole `region` jest w danych pacjenta). Potem porównać nowych pacjentów ze wszystkich kanałów, osobno L4, i powroty pozostałych pacjentów w województwach z kampanią i bez niej. Ten sam test sprawdza hipotezę porannych opóźnień, jeśli przy okazji zmierzymy opóźnienia porannych wizyt u internisty. Uzupełnienie: badanie przyrostu konwersji w panelach Meta i TikToka, czyli grupa kontrolna, której reklama się nie wyświetla.

## 7. Naprawić albo wyłączyć — rachunek w marży na rok

`a5e_scenariusze.txt`, E. Podstawa to cały okres 2: nowi pacjenci i wydatki z 12 miesięcy, marża na pacjenta w 90 dniach z kohort z pełnym oknem. Obok podajemy marżę w 180 dniach, która daje prawie to samo. Kwoty to zmiana marży rocznie.

```
                                      dziś     naprawić: zwroty L4    zgoda   wyłączyć, gdy dodatkowych jest
kampania               reguła        wynik     A (zapłata)  B (nie kupuje)        100%      50%       0%
meta_prosp_l4_szybko   przyjęta    +27 845    +42 167     +12 716      +1 564     −27 908   +67 707  +163 322
meta_prosp_l4_szybko   sesja płat. −28 735    +24 173      +7 308      +1 160     +28 906   +96 114  +163 322
tt_prosp_l4_15min      przyjęta    −11 928    +14 901      +5 020          0     +11 997   +47 230   +82 464
tt_prosp_l4_15min      sesja płat. −30 801     +7 557      +2 620          0     +30 851   +56 657   +82 464
obie                   przyjęta    +17 849    +57 349     +17 832      +1 900     −18 041  +113 873  +245 787
obie                   sesja płat. −58 372    +31 593      +9 910      +1 429     +58 536  +152 162  +245 787
```

**Drogi „naprawić”, każda z założeniami:**
- **Obietnica reklamy i strona wejścia: zwroty po wizytach L4 do poziomu pozostałych pacjentów** (z 17,4% do 5,3%, czyli około 713 zwrotów mniej rocznie według przyjętej reguły). Dwa warianty skrajne:
  - **A:** wizyta daje pacjentowi to, czego oczekiwał, i zapłata zostaje (średni zwrot L4 80,4 zł);
  - **B:** reklama obiecuje uczciwie, więc pacjenci, którzy i tak nie dostaliby L4, nie kupują. Oszczędzamy 25 zł kosztu lekarza za wizytę, a przy tych samych wydatkach jest o tyle mniej zamówień.

  Prawda leży zwykle między A i B. Powodu zwrotu nie ma w danych (lista niewiadomych). Dopisek do wariantu A, jako scenariusz: pacjent bez zwrotu wraca częściej (4,3% wobec 1,9%), co daje jeszcze około 1,7 tys. zł rocznie.
- **Zgoda marketingowa do poziomu pozostałych pacjentów:** od 53 do 1 900 zł rocznie dla obu kampanii (punkt 4c). Mała dźwignia.
- **Przeglądarki wbudowane w aplikacje:** 0 zł w tym rachunku. W obu kampaniach sesje z Instagrama, Facebooka i TikToka kończą się pierwszym zamówieniem nie rzadziej niż sesje ze zwykłych przeglądarek. Kampania Meta: 5,99% wobec 5,58%. TikTok: 4,80% wobec 4,56%. Przed awarią Safari na iOS (do 16.03.2026) wyniki są podobne. Niska konwersja tych kampanii to cecha ich ruchu, a nie samej przeglądarki. Dla pozostałych kampanii sprawa jest otwarta (`a5_pozyskanie.md`, sekcja 5).
- **Przepustowość poranka:** od 11 931 do 65 247 zł rocznie, tylko jeśli opóźnienia obniżają powroty (punkt 5). Kosztu dodatkowej porannej obsady nie ma w danych, więc tej drogi nie da się wycenić netto.

**Droga „wyłączyć” (ograniczenie budżetu do zera):** zmiana marży = oszczędzone wydatki − marża pacjentów, którzy bez kampanii by nie przyszli. Dodatkowość jest nieznana (punkt 6), więc są trzy warianty: 100%, 50% i 0% pacjentów dodatkowych. Jeśli hipoteza porannych opóźnień jest prawdziwa, dochodzi do tego od 11 931 do 65 247 zł z powrotów pozostałych pacjentów.

**Jak to czytać (do decyzji Kuby, nie wniosek):**
- **TikTok:** przy każdej regule i każdej dodatkowości wyłączenie nie pogarsza marży w 90 dniach. Przy 100% pacjentów dodatkowych daje od +12,0 do +30,9 tys. zł rocznie. Naprawa zwrotów w najlepszym wariancie (A) doprowadza wynik do +3,0 tys. zł według przyjętej reguły, a według sesji płatności wynik zostaje ujemny (−23,2 tys. zł).
- **Meta na L4:** wynik zależy od reguły źródła (+27,8 albo −28,7 tys. zł). Przy 100% pacjentów dodatkowych wyłączenie kosztuje 27,9 tys. zł według przyjętej reguły albo daje 28,9 tys. zł według sesji płatności. Naprawa zwrotów (A) daje +71,6 tys. zł według przyjętej reguły i −3,4 tys. zł według sesji płatności. Tę kampanię rozstrzygnie dopiero test dodatkowości.
- Ograniczenie, które obejmuje obie drogi: rachunek mierzy marżę w 90 dniach od pozyskania. U pacjentów nowych kampanii marża w 180 dniach prawie się nie zmienia (powroty około 4%), więc wniosek o kierunku jest odporny na wybór okna.

## 8. Otwarte (kandydaci na listę „czego nie da się rozstrzygnąć” i do punktu C)

1. **Czy pacjenci nowych kampanii są dodatkowi.** Test: wyłączenie kampanii na L4 w losowej połowie województw na 4–6 tygodni (punkt 6) i badanie przyrostu w panelach reklamowych. Od wyniku zależy, czy wyłączenie Meta na L4 kosztuje, czy daje marżę (od −27,9 do +163,3 tys. zł rocznie).
2. **Która reguła źródła jest bliższa prawdy dla kampanii bez kodu** (Google Ads ogólne, Meta lekarz online). Znak ich wyniku zależy od reguły. To ten sam test: grupa kontrolna bez reklamy.
3. **Powód zwrotów po wizycie L4** (już na liście z części retencji). Od niego zależy, czy naprawa zwrotów jest bliżej wariantu A (+57 tys. zł), czy B (+18 tys. zł).
4. **Koszt porannej obsady internistów.** Bez niego nie wycenimy netto naprawy przepustowości poranka.
5. **`gs_generic_specjalisci` traci w obu regułach** (marża 32 zł na pacjenta w 90 dniach przy koszcie pozyskania 56–78 zł). Kandydat do punktu C, z obiema drogami.
6. **Rachunek w 90 i 180 dniach nie obejmuje marży po 180 dniach.** Dla kampanii z powracającymi pacjentami to zaniża wynik. W okresie 1 marża na pacjenta w 365 dniach wynosiła 83,6 zł wobec 66,6 zł w 90 dniach. Dla nowych kampanii na L4 różnica jest mała.

## 9. Propozycje wpisów do wspólnych notatek (scala sesja prowadząca)

### Do `ZALOZENIA.md` (nowe punkty od 39; sekcja „ekonomia kampanii, punkt A5”)

39. **Koszt pozyskania pacjenta** = (wydatki kampanii + prowizja afiliacyjna) / nowi pacjenci kampanii. Wydatki i nowych pacjentów bierzemy z tych samych dni kalendarzowych. Dzień pacjenta to dzień pierwszej płatności. Kanały bez wydatków mają koszt 0 zł, a program poleceń nie ma kosztu w danych. Pacjent kupuje zwykle tego samego dnia co pierwsze wejście (75,1%) albo w ciągu 7 dni (24,6%), więc przesunięcie na brzegach okna jest małe.
40. **Wynik na pacjenta** = marża na pacjenta w N dniach (założenie 34) − koszt pozyskania. Główne okno to 90 dni (kohorty 1.10–2.07 w obu okresach), sprawdzenie w 180 dniach (1.10–3.04). Przedział 95% liczymy tylko z rozrzutu marży, a koszt pozyskania traktujemy jako stały. **Rachunek roczny** = nowi pacjenci i wydatki z całego okresu × marża na pacjenta w 90 dniach z kohort z pełnym oknem.
41. **Kampania niepewna** = taka, której wynik na pacjenta ma inny znak według przyjętej reguły i według sesji płatności, w którymkolwiek oknie (90 albo 180 dni) i okresie (założenie 23). Sesja płatności z definicji obniża wynik kampanii pozyskujących i podnosi wynik wejść bezpośrednich, wyszukiwania marki i remarketingu. „Niepewne” są więc prawie wszystkie kampanie pozyskujące nowych pacjentów, nie tylko nowe kampanie na L4.
42. **Naprawić albo wyłączyć — rachunek.**
    - **Wyłączyć** = oszczędzone wydatki − dodatkowi pacjenci × marża na pacjenta, w trzech wariantach dodatkowości: 100%, 50% i 0%.
    - **Naprawa zwrotów L4** = odsetek zwrotów po wizycie L4 spada do poziomu pozostałych pacjentów. Wariant A: zapłata zostaje. Wariant B: pacjent nie kupuje, oszczędzamy 25 zł kosztu lekarza.
    - **Zgoda marketingowa** = udział zgód do poziomu pozostałych pacjentów, wyceniony na dwa sposoby: powrotem przypisanym do newslettera i SMS-a oraz całą różnicą powrotu.
    - **Przeglądarki wbudowane** = połowa luki konwersji wobec zwykłych przeglądarek w tej samej kampanii.

    Każdy powrót wyceniamy na 95,6 zł (założenie 38).
43. **Scenariusz porannych opóźnień** = spadek powrotu w starych kampaniach z części retencji (sama zmiana rozkładu opóźnień albo cały spadek, obie reguły) × liczba ich pacjentów w okresie 2 × 95,6 zł. Zawsze nazywamy go scenariuszem, a nie kosztem kampanii.

### Do `ZNALEZISKA.md` (sekcja „A5 — ekonomia kampanii”), po przeglądzie Kuby

- Nowe kampanie na L4 według przyjętej reguły: koszt pozyskania 32,7 zł, marża 36,3 zł, wynik +3,6 zł na pacjenta w 90 dniach. Według sesji płatności: 45,6 zł, 36,1 zł i −9,4 zł. Pozostałe kampanie płatne: +20,0 zł i +18,7 zł. Wynik nowych kampanii jest niepewny. TikTok ma wynik ujemny w obu regułach (−4,6 i −17,8 zł), a Meta na L4 jest niepewna (+6,5 i −6,5 zł).
- Według sesji płatności prawie wszystkie kampanie pozyskujące mają wynik ujemny w 90 dniach, a według przyjętej reguły dodatni. To własność reguły (punkt 2).
- Marża pacjentów nowych kampanii jest niższa o 27,9 zł na pacjenta. Odpowiadają za to kody rabatowe (−12,8 zł), zwroty (−8,7 zł), brak powrotów (−12,1 zł), niższa cena (−6,7 zł) i rzadsze TelemediGO (−3,8 zł). Tańszy lekarz równoważy +16,2 zł.
- Zgoda marketingowa u pacjentów nowych kampanii prawie nie zmienia ich powrotu (4,2% wobec 4,1%).
- W nowych kampaniach przeglądarki wbudowane w aplikacje konwertują nie gorzej niż zwykłe.
- `gs_generic_specjalisci` ma wynik ujemny w obu regułach i oknach. `gs_generic_erecepta` drożeje: koszt pozyskania rośnie z 48,8 do 59,8 zł.
- Dodatkowość: po startach kampanii pozyskanie w pozostałych kanałach nie spadło wyraźnie. Jest słaby sygnał przejmowania pacjentów L4 z Google Ads przy starcie kampanii Meta: iloraz 0,67, przedział od 0,45 do 0,98. Przybliżenie to około 3% pacjentów nowych kampanii, z błędem rzędu samego wyniku.
- Ranking lekarzy daje w obu okresach prawie tę samą liczbę pacjentów (616 i 617). Możliwa cecha generatora, bez wpływu na wnioski.

### Do `PLAN.md`

- Status A5: ekonomia kampanii zrobiona (commity w sekcji 10). Część A5 zamknięta po przeglądzie Kuby.
- Do punktu C, lista priorytetów, trzy pozycje z obiema drogami i liczbami z punktu 7:
  - TikTok na L4 (wyłączyć albo naprawić zwroty);
  - Meta na L4 (decyzja po teście dodatkowości);
  - zwroty po wizytach L4 (obietnica reklamy).

  Do tego `gs_generic_specjalisci` jako nowy kandydat.
- Do listy niewiadomych: dodatkowość nowych kampanii z testem według województw (punkt 6). Reguła źródła dla kampanii bez kodu: ten sam test. Koszt porannej obsady.
- Do narzędzia (punkt B): zestawienie `analiza/wyniki/a5e_kampanie.csv` (grupy, kampanie, kanały; obie reguły; okna 90, 180 i pełny rok). Przy każdej kampanii obie reguły obok siebie i oznaczenie „niepewna”.

### Do `analiza/README.md`

| Krok | Polecenie | Co robi | Wynik |
|---|---|---|---|
| A5 | `python -I analiza/a5e_ekonomia.py` | Ekonomia kampanii: wydatki, prowizja, nowi pacjenci, koszt pozyskania, marża na pacjenta w 90 i 180 dniach, wynik po koszcie pozyskania. Kampanie, kanały i grupy, oba okresy na tych samych dniach kalendarzowych, przyjęta reguła źródła i sesja płatności, kampanie niepewne. Importuje `definicje.py`. | `wyniki/a5e_ekonomia.txt`, `wyniki/a5e_kampanie.csv` |
| A5 | `python -I analiza/a5e_scenariusze.py` | Skład marży nowych kampanii na L4, zwroty po wizycie, zgoda marketingowa, scenariusz porannych opóźnień, dodatkowość pacjentów, naprawić albo wyłączyć. Importuje `definicje.py` i `a5e_ekonomia.py`, czyta `wyniki/a5r_zdarzenia.txt`. | `wyniki/a5e_scenariusze.txt` |

### Do `DECYZJE.md`

Po przeglądzie Kuby: co przyjął, z jakimi dopiskami (sekcja 11).

## 10. Recenzja Codeksa (model Sol)

W toku.

## 11. Dopiski i decyzje Kuby

Czeka na przegląd.
