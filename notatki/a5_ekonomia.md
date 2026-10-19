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

1. **Nowe kampanie na L4 pozyskują pacjenta taniej niż reszta kampanii płatnych, ale ten pacjent zostawia prawie o połowę mniej marży.** Według przyjętej reguły źródła wynik na pacjenta w 90 dniach to +3,6 zł, a według sesji płatności −9,4 zł. Znak zależy od reguły atrybucji, więc to wynik **niepewny**.
2. **Kampania na TikToku ma wynik ujemny w obu regułach** (−4,6 i −17,8 zł na pacjenta w 90 dniach). Kampania Meta na L4 jest niepewna (+6,5 i −6,5 zł).
3. **Niska marża tych pacjentów to kody rabatowe, zwroty po wizycie L4 i prawie zerowe powroty.** Tańszy lekarz (internista) częściowo to równoważy.
4. **Zgoda marketingowa i przeglądarki wbudowane w aplikacje nie dają w tym rachunku wyraźnej wartości.** U pacjentów nowych kampanii zgoda prawie nie zmienia powrotu. Surowa konwersja w przeglądarkach wbudowanych nie jest w tych kampaniach niższa niż w zwykłych.
5. **Największa dźwignia naprawy to zwroty po wizytach L4.** Gdyby spadły do poziomu pozostałych pacjentów, dawałoby to od 22 do 57 tys. zł marży rocznie według przyjętej reguły.
6. **Dane nie rozstrzygają, czy pacjenci tych kampanii są dodatkowi.** Łączne pozyskanie w pozostałych kanałach po startach kampanii nie spadło wyraźnie. Widać jednak sygnał względnego osłabienia L4 w pozostałych kanałach po starcie kampanii Meta.
7. **Hipoteza porannych opóźnień to tylko scenariusz: od 0 do 65 tys. zł marży rocznie.** W wariancie wąskim wychodzi około 12 tys. zł. Na pacjenta nowych kampanii to od 0 do 12,6 zł. Szeroki wariant zjada cały ich wynik według przyjętej reguły.

---

## 1. Koszt pozyskania i wynik na pacjenta — nowe kampanie na L4 wobec pozostałych

Okres 2, kohorty z pełnym oknem 90 dni (1.10.2025–2.07.2026). Wydatki pochodzą z tych samych dni. Wynik na pacjenta to marża w 90 dniach minus koszt pozyskania. Przedział 95% jest warunkowy: liczymy go tylko z rozrzutu marży, przy stałym koszcie pozyskania i danej regule źródła. Nie obejmuje niepewności atrybucji ani dodatkowości (`a5e_ekonomia.txt`, sekcja 1a; `a5e_scenariusze.txt`, sekcja A).

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
- **Dlaczego reguły się różnią.** Sesja płatności przypisuje nowym kampaniom o 1 383 pacjentów mniej w 90-dniowej próbie (4 893 wobec 3 510), a przy tych samych wydatkach koszt pozyskania rośnie z 32,7 do 45,6 zł. Ci pacjenci mieli kod kampanii albo pierwsze wejście z kampanii, ale zapłacili w innej sesji (przeliczenie Codeksa):
  - 575 w sesji bezpośredniej;
  - 325 z bezpłatnego wyszukiwania Google;
  - 299 z wyszukiwania marki;
  - 184 z remarketingu Meta.

  W całym okresie 2 dotyczy to 2 081 z 7 268 pacjentów (`a5e_scenariusze.txt`, D3; `ZNALEZISKA.md`, A4, punkt 6).
- **Prognoza marży rocznika** (nowi z 12 miesięcy × marża w 90 dniach − wydatki z 12 miesięcy, każda kampania osobno, potem suma): +15 917 zł według przyjętej reguły i −59 536 zł według sesji płatności (`a5e_scenariusze.txt`, E0).
- **Kontrola brzegu okna** (recenzja Codeksa): gdyby okno wyznaczać dniem pierwszego wejścia zamiast dnia płatności, nowe kampanie miałyby 4 912 pacjentów zamiast 4 893, a koszt pozyskania wyniósłby 32,55 zł zamiast 32,68 zł.

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

- **Prawie wszystkie kampanie płatne, które pozyskują nowych pacjentów, mają wynik zależny od reguły atrybucji, a nie tylko nowe kampanie na L4.** Według sesji płatności kampanie Google Ads ogólne i Meta mają w 90 dniach wynik ujemny, a według przyjętej reguły dodatni. To własność reguły, a nie błąd kodu (Codex to potwierdził). Sesja płatności przenosi pacjentów, którzy przyszli z reklamy, do wejść bezpośrednich, wyszukiwania marki i remarketingu, czyli tam, gdzie zapłacili. Przyjęta reguła zgadza się z kodami kampanii w 97% przypadków, a sesja płatności w 67–71% (założenie 22). Kontrola kodami obejmuje jednak tylko trzy kampanie.
- **Wynik dodatni w obu regułach też nie dowodzi, że dodatkowy budżet się opłaci.** To średnia wszystkich przypisanych pacjentów, a nie pacjentów pozyskanych za ostatnią wydaną złotówkę.
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
- **U pacjentów nowych kampanii zgoda prawie nie zmienia powrotu w 90 dniach:** 4,2% ze zgodą i 4,1% bez niej. Pacjenci ze zgodą wracają w 1,03% zamówieniem przypisanym do newslettera albo SMS-a, a pacjenci bez zgody nie mają takich powrotów wcale. Bez zgody wracają więc prawie tak samo często inną drogą. Przypisanie to nie wpływ: pacjent mógłby kupić także bez wiadomości. U kampanii TikTok powrotów przypisanych do newslettera i SMS-a w 90 dniach nie ma wcale.
- **U pozostałych pacjentów różnica jest większa,** ale też mała: 22,6% wobec 20,9%. Przez newsletter albo SMS wraca 6,19% pacjentów ze zgodą.
- **Odczytanie, do oceny Kuby.** Niska zgoda to cecha pacjentów nowych kampanii. Na podstawie tych danych nie jest to osobny koszt w marży. Nie wiemy, czy wiadomości wywołują zakup (lista niewiadomych, punkt 4 w `PLAN.md`, sekcja C).

## 5. Scenariusz hipotezy Kuby: poranne godziny internistów

`a5e_scenariusze.txt`, C. **To scenariusz, nie wynik.**

- **Wartość powrotu:** 95,6 zł marży w dniach 1–180 (założenie 38, odtworzone kodem; Codex: 95,581 zł).
- **Trzy warianty scenariusza** (spadek powrotu w 90 dniach u pacjentów starych kampanii z raportu części retencji, `a5r_zdarzenia.txt`):
  - **brak efektu:** kampanie nie zmieniają powrotów pozostałych pacjentów, 0 zł;
  - **wąski — tylko zmiana rozkładu opóźnień pierwszej wizyty:** −0,76 punktu procentowego według przyjętej reguły (17 419 pacjentów) i −0,64 punktu według sesji płatności (19 500 pacjentów). To 132 i 125 powrotów mniej rocznie, czyli 12 656 zł i 11 931 zł marży;
  - **szeroki — cały spadek w starych kampaniach:** −1,91 i −3,50 punktu, czyli 333 i 683 powroty, 31 806 zł i 65 247 zł marży.

  To warianty, a nie przedział możliwego efektu. Szeroki wariant nie jest formalną górną granicą (recenzja Codeksa).
- **Na pacjenta nowych kampanii** (7 268 według przyjętej reguły, 5 187 według sesji płatności) to od 0 do 12,6 zł. Kwotę dzielimy na tych pacjentów tylko po to, żeby pokazać rząd wielkości obok wyniku na pacjenta.
- **Co z tego wynika dla wyniku nowych kampanii.** Według przyjętej reguły wynik to +3,6 zł na pacjenta w 90 dniach. W wariancie wąskim (1,7 zł) zostaje +1,9 zł. W wariancie szerokim (4,4 zł) wychodzi −0,8 zł. Według sesji płatności wynik jest ujemny bez scenariusza.
- **Dlaczego to tylko scenariusz.** Część retencji pokazała, że przy tym samym porannym ruchu opóźnień jest dużo więcej niż rok wcześniej (+26,4 punktu procentowego). Spadła więc przepustowość poranka, a kampanie mogą nie być przyczyną. Nie wiemy też, czy wyłączenie kampanii podniosłoby powroty pozostałych pacjentów.

## 6. Czy pacjenci nowych kampanii są dodatkowi

`a5e_scenariusze.txt`, D. Według przyjętej reguły, bo sesja płatności z definicji przenosi część pacjentów nowych kampanii do kanałów bezpłatnych.

**Co widać: łączne pozyskanie w pozostałych kanałach po startach kampanii nie spadło wyraźnie. Widać jednak sygnał względnego osłabienia L4 w pozostałych kanałach po starcie kampanii Meta. Dane nie rozstrzygają dodatkowości** (brzmienie po recenzji Codeksa). Brak spadku rok do roku nie wyklucza przejmowania pacjentów, bo bez kampanii pozostałe kanały mogłyby rosnąć szybciej.

- **Miesiące rok do roku.** Pacjenci pozostałych kanałów rosną rok do roku od 0% do +21% w miesiącach XI 2025 – VIII 2026, a we wrześniu 2026 spadają o 4%. W październiku 2025, przed startem kampanii Meta, wzrost wynosił +8%. Kanały bezpłatne rosną o 4–29% (we wrześniu 2026 spadają o 5%).
- **28 dni przed startem i 28 dni po nim, wobec tych samych dni rok wcześniej.** Iloraz 1,00 znaczy brak zmiany. W nawiasach przedział 95%.
  - **Start Meta na L4 (3.11.2025):**
    - wszyscy pacjenci pozostałych kanałów: 1,04 (od 0,94 do 1,16);
    - pacjenci z inną pierwszą usługą niż L4: 1,12;
    - pacjenci L4 w pozostałych kanałach: 0,81 (od 0,64 do 1,03);
    - kampania Google Ads na L4 (`gs_generic_l4`): 0,67 (od 0,45 do 0,98). To jedyny przedział, który wyklucza brak zmiany.
    - **L4 wobec innych usług w pozostałych kanałach,** skorygowane o tę samą zmianę rok wcześniej: 0,73 (od 0,56 do 0,95). To porównanie zaproponował Codex. Przedział jest orientacyjny, bo zakłada niezależne zliczenia i wspólny trend.
  - **Start TikToka (9.02.2026):** wszystko lekko poniżej 1. Wszyscy pacjenci pozostałych kanałów 0,91 (od 0,83 do 1,01), L4 0,84, L4 wobec innych usług 0,90 (od 0,71 do 1,14). Rok wcześniej w tych dniach nie działała żadna nowa kampania, a w roku startu przez 28 dni przed startem działała już Meta na L4.
- **Kontrola fikcyjnymi datami startu.** Ten sam iloraz L4 wobec innych usług (28 dni po dacie i 28 dni przed, bez korekty o rok wcześniej) policzyliśmy dla każdego poniedziałku okresu 1, kiedy nowych kampanii nie było.
  - Przy starcie Meta iloraz wynosi 0,88. Tak niski albo niższy wyszedł w 4 z 44 poniedziałków okresu 1.
  - Przy starcie TikToka wynosi 1,01, czyli tyle co w połowie poniedziałków.
  - Sygnał przy starcie Meta jest więc słaby, ale nie zerowy.
- **Przybliżenie.** Bez kampanii udział L4 w pozostałych kanałach byłby taki jak w tym samym miesiącu okresu 1. Wtedy w miesiącach XI 2025 – IX 2026 brakuje 226 pacjentów L4, czyli 3,1% z 7 268 pacjentów nowych kampanii. W październiku 2025, bez kampanii, ten sam wzór myli się o 58 pacjentów w drugą stronę, więc to przybliżenie ma błąd rzędu samego wyniku. Nie jest to też oszacowanie udziału pacjentów niedodatkowych, bo obejmuje tylko pacjentów L4 przejętych z pozostałych kanałów.
- **Czego te dane nie mówią.** Nie widać pacjentów, którzy bez kampanii wyszukaliby Telemedi sami albo trafiliby do konkurencji. Dane nie pozwalają ich odróżnić od tych, których przyprowadziła reklama. Według przyjętej reguły 163 pacjentów nowych kampanii miało wcześniejsze wejście z innego kanału, a kod kampanii przypisał ich do kampanii.
- **Test rozstrzygający (do listy niewiadomych).** Na 4–6 tygodni wyłączyć albo mocno obniżyć budżet kampanii na L4 w losowo wybranej połowie województw (pole `region` jest w danych pacjenta). Potem porównać nowych pacjentów ze wszystkich kanałów, osobno L4, i powroty pozostałych pacjentów w województwach z kampanią i bez niej. Ten sam test sprawdza hipotezę porannych opóźnień, jeśli przy okazji zmierzymy opóźnienia porannych wizyt u internisty. Uzupełnienie: badanie przyrostu konwersji w panelach Meta i TikToka, czyli grupa kontrolna, której reklama się nie wyświetla.

## 7. Naprawić albo wyłączyć — rachunek w marży na rok

`a5e_scenariusze.txt`, E. Podstawa to prognoza marży rocznika pozyskanych pacjentów: nowi pacjenci i wydatki z całego okresu 2 × marża na pacjenta w 90 dniach z kohort z pełnym oknem. Każdą kampanię liczymy osobno, a wiersz „obie” to suma. Kwoty to zmiana marży rocznie w horyzoncie 90 dni od pozyskania. Marża w 180 dniach daje prawie to samo.

```
                                        dziś      naprawić zwroty L4          wyłączyć, gdy dodatkowych jest
kampania               reguła          wynik     wariant A   wariant B       100%       50%        0%
meta_prosp_l4_szybko   przyjęta      +27 845     +42 262     +16 486      −27 845   +67 739  +163 322
meta_prosp_l4_szybko   sesja płat.   −28 735     +24 273      +9 745      +28 735   +96 029  +163 322
tt_prosp_l4_15min      przyjęta      −11 928     +14 891      +5 810      +11 928   +47 196   +82 464
tt_prosp_l4_15min      sesja płat.   −30 801      +7 605      +2 976      +30 801   +56 633   +82 464
obie                   przyjęta      +15 917     +57 112     +22 283      −15 917  +114 935  +245 787
obie                   sesja płat.   −59 536     +31 795     +12 680      +59 536  +152 661  +245 787
```

**Drogi „naprawić”, każda z założeniami:**
- **Obietnica reklamy i strona wejścia: zwroty po wizytach L4 do poziomu pozostałych pacjentów,** czyli z 17,4% do 5,3% według przyjętej reguły. Dwa warianty skrajne, liczone po recenzji Codeksa:
  - **A:** wizyta daje pacjentowi to, czego oczekiwał, i zapłata zostaje. Liczba wizyt się nie zmienia, a zwrotów jest mniej o 710,7 rocznie. Zysk to zwroty, które zostają w kasie: średnio 80,4 zł na wizytę.
  - **B:** reklama obiecuje uczciwie, więc pacjenci, którzy i tak nie dostaliby L4, nie kupują. Znika 750,6 wizyt, które dziś kończą się zwrotem. Zysk to koszt lekarza za te wizyty, średnio 32,01 zł (część z nich to psychiatra), minus dalsza marża tych pacjentów (TelemediGO i dni 1–90, średnio 2,32 zł). Przy tych samych wydatkach jest o tyle mniej zamówień.

  Prawda leży zwykle między A i B. Powodu zwrotu nie ma w danych (lista niewiadomych). Dopisek do wariantu A, jako scenariusz w horyzoncie 180 dni: pacjent bez zwrotu wraca częściej (4,3% wobec 1,9%), co daje jeszcze około 1,7 tys. zł rocznie.
- **Zgoda marketingowa do poziomu pozostałych pacjentów:** dwa odczytania w horyzoncie 180 dni, pokazywane osobno i niedodawane do sum.
  - Wariant optymistyczny, z powrotów przypisanych do newslettera i SMS-a: 1 900 zł rocznie dla obu kampanii.
  - Z całej różnicy powrotu: 53 zł.

  W obu odczytaniach to mała dźwignia (punkt 4c).
- **Przeglądarki wbudowane w aplikacje:** w tym rachunku 0 zł. W obu kampaniach sesje z Instagrama, Facebooka i TikToka kończą się pierwszym zamówieniem w tej samej sesji nie rzadziej niż sesje ze zwykłych przeglądarek. W kampanii Meta to 5,99% wobec 5,58%, w TikToku 4,80% wobec 4,56%. Przed awarią Safari na iOS (do 16.03.2026) jest podobnie. To surowe porównanie nie rozdziela wpływu urządzenia, daty, samego pacjenta ani zakupu w innej sesji. Nie przesądza więc, że przeglądarka nie ma znaczenia (recenzja Codeksa). Dla pozostałych kampanii sprawa jest otwarta (`a5_pozyskanie.md`, sekcja 5).
- **Przepustowość poranka:** od 0 do 65 247 zł rocznie w horyzoncie 180 dni, tylko jeśli opóźnienia obniżają powroty (punkt 5). Kosztu dodatkowej porannej obsady nie ma w danych, więc tej drogi nie da się wycenić netto.

**Droga „wyłączyć” (ograniczenie budżetu do zera):** zmiana marży = oszczędzone wydatki − marża pacjentów, którzy bez kampanii by nie przyszli. Dodatkowość jest nieznana (punkt 6), więc są trzy warianty: 100%, 50% i 0% pacjentów dodatkowych. Założenia (recenzja Codeksa):
- pacjenci dodatkowi mają średnią marżę wszystkich pacjentów przypisanych kampanii;
- pacjenci, którzy przyszliby bez kampanii, zachowują się tak samo jak dziś;
- koszty pozostałych kanałów się nie zmieniają;
- TelemediGO i koszt lekarza są już w marży, a marży po 90 dniach rachunek nie obejmuje.

Jeśli hipoteza porannych opóźnień jest prawdziwa, dochodzi do tego od 0 do 65 247 zł z powrotów pozostałych pacjentów (punkt 5).

**Jak to czytać (do decyzji Kuby, nie wniosek):**
- **TikTok:** przy każdej regule i każdej dodatkowości wyłączenie nie pogarsza marży w 90 dniach. Przy 100% pacjentów dodatkowych daje od +11,9 do +30,8 tys. zł rocznie. Naprawa zwrotów w najlepszym wariancie (A) doprowadza wynik do +3,0 tys. zł według przyjętej reguły. Według sesji płatności wynik zostaje ujemny (−23,2 tys. zł).
- **Meta na L4:** wynik zależy od reguły źródła (+27,8 albo −28,7 tys. zł). Przy 100% pacjentów dodatkowych wyłączenie kosztuje 27,8 tys. zł według przyjętej reguły albo daje 28,7 tys. zł według sesji płatności. Naprawa zwrotów (A) daje wynik +70,1 tys. zł według przyjętej reguły i −4,5 tys. zł według sesji płatności. Tę kampanię rozstrzygnie dopiero test dodatkowości.
- **Ograniczenie obu dróg:** rachunek mierzy marżę w 90 dniach od pozyskania. U pacjentów nowych kampanii marża w 180 dniach prawie się nie zmienia (powroty około 4%). Wniosek o kierunku jest więc odporny na wybór okna. Decyzji o wyłączeniu nie da się jednak uzasadnić samą atrybucją (recenzja Codeksa).

## 8. Otwarte (kandydaci na listę „czego nie da się rozstrzygnąć” i do punktu C)

1. **Czy pacjenci nowych kampanii są dodatkowi.** Test: wyłączenie kampanii na L4 w losowej połowie województw na 4–6 tygodni (punkt 6) i badanie przyrostu w panelach reklamowych. Od wyniku zależy, czy wyłączenie Meta na L4 kosztuje, czy daje marżę (od −27,8 do +163,3 tys. zł rocznie). Przy okazji warto policzyć L4 tygodniowo z trendem przed startem i niepewnością uwzględniającą zależność między dniami (recenzja Codeksa).
2. **Która reguła źródła jest bliższa prawdy dla kampanii bez kodu** (Google Ads ogólne, Meta lekarz online). Znak ich wyniku zależy od reguły. To ten sam test: grupa kontrolna bez reklamy.
3. **Powód zwrotów po wizycie L4** (już na liście z części retencji). Od niego zależy, czy naprawa zwrotów jest bliżej wariantu A (+57 tys. zł), czy B (+22 tys. zł).
4. **Koszt porannej obsady internistów.** Bez niego nie wycenimy netto naprawy przepustowości poranka.
5. **`gs_generic_specjalisci` traci w obu regułach** (marża 32 zł na pacjenta w 90 dniach przy koszcie pozyskania 56–78 zł). Kandydat do punktu C, z obiema drogami.
6. **Rachunek w 90 i 180 dniach nie obejmuje marży po 180 dniach.** Dla kampanii z powracającymi pacjentami to zaniża wynik. W okresie 1 marża na pacjenta w 365 dniach wynosiła 83,6 zł wobec 66,6 zł w 90 dniach. Dla nowych kampanii na L4 różnica jest mała.

## 9. Propozycje wpisów do wspólnych notatek (scala sesja prowadząca)

### Do `ZALOZENIA.md` (nowe punkty od 39; sekcja „ekonomia kampanii, punkt A5”)

39. **Koszt pozyskania pacjenta** = (wydatki kampanii + prowizja afiliacyjna) / nowi pacjenci kampanii. Wydatki i nowych pacjentów bierzemy z tych samych dni kalendarzowych. Dzień pacjenta to dzień pierwszej płatności. Kanały bez wydatków mają koszt 0 zł, a program poleceń nie ma kosztu w danych. Pacjent kupuje zwykle tego samego dnia co pierwsze wejście (75,1%) albo w ciągu 7 dni (24,6%), więc przesunięcie na brzegach okna jest małe.
40. **Wynik na pacjenta** = marża na pacjenta w N dniach (założenie 34) − koszt pozyskania. Główne okno to 90 dni (kohorty 1.10–2.07 w obu okresach), sprawdzenie w 180 dniach (1.10–3.04). Przedział 95% jest warunkowy: liczymy go tylko z rozrzutu marży, przy stałym koszcie pozyskania i danej regule źródła. **Prognoza marży rocznika** = nowi pacjenci i wydatki z całego okresu × marża na pacjenta w 90 dniach z kohort z pełnym oknem, każda kampania osobno, sumy z kampanii. Obejmuje też marżę pacjentów pozyskanych pod koniec okresu, która przypada po jego końcu.
41. **Kampania niepewna (wynik zależny od reguły atrybucji)** = taka, której wynik na pacjenta ma inny znak według przyjętej reguły i według sesji płatności, w którymkolwiek oknie (90 albo 180 dni) i okresie (założenie 23). Sesja płatności z definicji obniża wynik kampanii pozyskujących i podnosi wynik wejść bezpośrednich, wyszukiwania marki i remarketingu. „Niepewne” są więc prawie wszystkie kampanie pozyskujące nowych pacjentów, nie tylko nowe kampanie na L4. Wynik dodatni w obu regułach też nie dowodzi, że dodatkowy budżet się opłaci.
42. **Naprawić albo wyłączyć — rachunek.**
    - **Wyłączyć** = oszczędzone wydatki − dodatkowi pacjenci × marża na pacjenta, w trzech wariantach dodatkowości: 100%, 50% i 0%. Zakładamy, że pacjenci dodatkowi mają średnią marżę wszystkich przypisanych, że pacjenci, którzy przyszliby bez kampanii, zachowują się jak dziś, i że koszty pozostałych kanałów się nie zmieniają.
    - **Naprawa zwrotów L4** = odsetek zwrotów po wizycie L4 spada do poziomu pozostałych pacjentów. Wariant A: zapłata zostaje, czyli x_A = zwroty − wizyty × odsetek docelowy, a zysk = x_A × średni zwrot. Wariant B: pacjent nie kupuje, czyli x_B z równania (zwroty − x_B) / (wizyty − x_B) = odsetek docelowy, a zysk = x_B × (średni koszt lekarza zwróconej wizyty L4 − dalsza marża tych pacjentów).
    - **Zgoda marketingowa** = udział zgód do poziomu pozostałych pacjentów, wyceniony na dwa sposoby, pokazywane osobno i niedodawane do sum: powrotem przypisanym do newslettera i SMS-a (wariant optymistyczny) oraz całą różnicą powrotu.
    - **Przeglądarki wbudowane** = połowa luki konwersji wobec zwykłych przeglądarek w tej samej kampanii, tylko gdy luka jest dodatnia.

    Każdy powrót wyceniamy na 95,6 zł (założenie 38). Kwot w horyzoncie 180 dni (powroty, zgody, poranek) nie dodajemy do wyników w horyzoncie 90 dni.
43. **Scenariusz porannych opóźnień** = spadek powrotu w starych kampaniach z części retencji (sama zmiana rozkładu opóźnień albo cały spadek, obie reguły) × liczba ich pacjentów w okresie 2 × 95,6 zł, zawsze razem z wariantem „brak efektu” (0 zł). Zawsze nazywamy go scenariuszem, a nie kosztem kampanii. Wariant szeroki nie jest formalną górną granicą.

### Do `ZNALEZISKA.md` (sekcja „A5 — ekonomia kampanii”), po przeglądzie Kuby

- Nowe kampanie na L4 według przyjętej reguły: koszt pozyskania 32,7 zł, marża 36,3 zł, wynik +3,6 zł na pacjenta w 90 dniach. Według sesji płatności: 45,6 zł, 36,1 zł i −9,4 zł. Pozostałe kampanie płatne: +20,0 zł i +18,7 zł. Wynik nowych kampanii zależy od reguły atrybucji (niepewny). TikTok ma wynik ujemny w obu regułach (−4,6 i −17,8 zł), a Meta na L4 jest niepewna (+6,5 i −6,5 zł).
- Według sesji płatności prawie wszystkie kampanie pozyskujące mają wynik ujemny w 90 dniach, a według przyjętej reguły dodatni. To własność reguły, nie błąd kodu (punkt 2, potwierdził Codex).
- Marża pacjentów nowych kampanii jest niższa o 27,9 zł na pacjenta. Odpowiadają za to kody rabatowe (−12,8 zł), zwroty (−8,7 zł), brak powrotów (−12,1 zł), niższa cena (−6,7 zł) i rzadsze TelemediGO (−3,8 zł). Tańszy lekarz równoważy +16,2 zł.
- Zgoda marketingowa u pacjentów nowych kampanii prawie nie zmienia ich powrotu (4,2% wobec 4,1%).
- W nowych kampaniach surowa konwersja sesji do pierwszego zamówienia w przeglądarkach wbudowanych w aplikacje nie jest niższa niż w zwykłych (bez rozdzielenia urządzenia, daty i pacjenta).
- `gs_generic_specjalisci` ma wynik ujemny w obu regułach i oknach. `gs_generic_erecepta` drożeje: koszt pozyskania rośnie z 48,8 do 59,8 zł.
- Dodatkowość: nie widać dużego spadku łącznego pozyskania w pozostałych kanałach po startach kampanii. Widać jednak sygnał względnego osłabienia L4 po starcie Meta: L4 wobec innych usług w pozostałych kanałach 0,73 (od 0,56 do 0,95), kampania Google Ads na L4 0,67 (od 0,45 do 0,98). Na fikcyjnych datach startu w okresie 1 tak niski iloraz wychodzi w 4 z 44 tygodni. Dane nie rozstrzygają dodatkowości.
- Ranking lekarzy daje w obu okresach prawie tę samą liczbę pacjentów (616 i 617). Możliwa cecha generatora, bez wpływu na wnioski.

### Do `PLAN.md`

- Status A5: ekonomia kampanii zrobiona (commity w sekcji 10). Część A5 zamknięta po przeglądzie Kuby.
- Do punktu C, lista priorytetów, trzy pozycje z obiema drogami i liczbami z punktu 7:
  - TikTok na L4 (wyłączyć albo naprawić zwroty);
  - Meta na L4 (decyzja po teście dodatkowości);
  - zwroty po wizytach L4 (obietnica reklamy).

  Do tego `gs_generic_specjalisci` jako nowy kandydat.
- Do listy niewiadomych: dodatkowość nowych kampanii z testem według województw (punkt 6). Reguła źródła dla kampanii bez kodu: ten sam test. Koszt porannej obsady.
- Do narzędzia (punkt B): zestawienie `analiza/wyniki/a5e_kampanie.csv` (grupy, kampanie, kanały; obie reguły; okna 90, 180 i pełny rok). Przy każdej kampanii obie reguły obok siebie i oznaczenie „wynik zależny od reguły atrybucji”. Przedziały 95% opisane jako warunkowe.

### Do `analiza/README.md`

| Krok | Polecenie | Co robi | Wynik |
|---|---|---|---|
| A5 | `python -I analiza/a5e_ekonomia.py` | Ekonomia kampanii: wydatki, prowizja, nowi pacjenci, koszt pozyskania, marża na pacjenta w 90 i 180 dniach, wynik po koszcie pozyskania. Kampanie, kanały i grupy, oba okresy na tych samych dniach kalendarzowych, przyjęta reguła źródła i sesja płatności, kampanie niepewne. Importuje `definicje.py`. | `wyniki/a5e_ekonomia.txt`, `wyniki/a5e_kampanie.csv` |
| A5 | `python -I analiza/a5e_scenariusze.py` | Skład marży nowych kampanii na L4, zwroty po wizycie, zgoda marketingowa, scenariusz porannych opóźnień, dodatkowość pacjentów, naprawić albo wyłączyć. Importuje `definicje.py` i `a5e_ekonomia.py`, czyta `wyniki/a5r_zdarzenia.txt`. | `wyniki/a5e_scenariusze.txt` |

### Do `DECYZJE.md`

Po przeglądzie Kuby: co przyjął, z jakimi dopiskami (sekcja 11).

## 10. Recenzja Codeksa (model Sol)

Podsumowanie i nasze decyzje: `notatki/recenzje/a5e_codex.md`. Polecenie i odpowiedź: `a5e_codex_prompt.md`, `a5e_codex_odpowiedz.md`.

- **Liczby główne Codex przeliczył niezależnie, własnym kodem.** Wszystkie zgadzają się co do sztuki i co do złotówki: koszty pozyskania, marże i wyniki obu grup według obu reguł, TikTok, trzy warianty prowizji, zwroty L4, wartość powrotu i scenariusz poranka.
- **Osiem uwag, wszystkie przyjęte:**
  - zestawienie „naprawić” mieszało horyzonty 90 i 180 dni, a wiersz „obie” nie był sumą kampanii;
  - wariant B zwrotów potrzebował innego mianownika i rzeczywistego kosztu lekarza (32,01 zł zamiast 25 zł);
  - do rachunku „wyłączyć” trzeba dopisać założenia;
  - cztery opisy sugerowały przyczynowość;
  - wniosek o dodatkowości trzeba było zawęzić (dodane porównanie L4 z innymi usługami i fikcyjne daty startu);
  - przedział 95% jest warunkowy;
  - kontrola brzegu okna;
  - nazwa „wynik zależny od reguły atrybucji”.
- **Co się zmieniło w liczbach:**
  - naprawa zwrotów: wariant A 57 112 zł zamiast 57 349 zł, wariant B 22 283 zł zamiast 17 832 zł;
  - prognoza rocznika obu kampanii: +15 917 zł zamiast +17 849 zł i −59 536 zł zamiast −58 372 zł;
  - zgody nie są już dodawane do wyniku w 90 dniach;
  - scenariusz poranka zaczyna się od 0 zł.

  Kierunek żadnego wyniku się nie zmienił.

## 11. Dopiski i decyzje Kuby

Czeka na przegląd.
