# A5: ekonomia kampanii

Rozmowa z Claude Code w projekcie zadania Telemedi, od 19.10.2026, 21:42 do 21.10.2026, 22:39 (czas polski). Wiadomości Kuby: 3. Odpowiedzi Claude: 19. Polecenia i wiadomości do innych sesji i agentów: 1.

Sesję uruchomiła sesja [„Telemedi: prowadzenie planu analizy punkt po punkcie”](2026-10-19_telemedi-prowadzenie-planu-analizy-punkt-po-punkcie.md), poleceniem z [wiadomości 54](2026-10-19_telemedi-prowadzenie-planu-analizy-punkt-po-punkcie.md#w54).

Co jest w zapisie, czego w nim nie ma i jakie są oznaczenia: [README](README.md).

### <a id="w1"></a>1. Claude · 19.10.2026, 21:42

Czytam notatki projektu; teraz sprawdzam łączniki i potem pokażę plan liczenia.

### <a id="w2"></a>2. Claude · 19.10.2026, 21:47

Pierwsza tabela gotowa. Teraz sprawdzam resztę raportu (prowizja, kanały), a potem liczę koszty nowych kampanii na L4 i scenariusze.

### <a id="w3"></a>3. Claude · 19.10.2026, 21:48

Teraz drugi skrypt: koszty widoczne tylko w nowych kampaniach na L4, scenariusz poranka, dodatkowość pacjentów i rachunek „naprawić albo wyłączyć”.

### <a id="w4"></a>4. Claude · 19.10.2026, 21:52

Wklejenie fragmentu przez powłokę się nie udało, plik został bez zmian. Zapisuję fragment osobno i wstawiam go do skryptu.

### <a id="w5"></a>5. Claude · 19.10.2026, 21:53

Wszystkie liczby są policzone. Zanim napiszę notatkę, zlecam Codeksowi (model Sol) niezależną recenzję kluczowych liczb i kodu. Działa w tle kilka minut.

### <a id="w6"></a>6. Claude · 19.10.2026, 21:54

Codex pracuje w tle. W tym czasie zapisuję w repozytorium skrypty i wyniki, potem piszę notatkę.

### <a id="w7"></a>7. Claude · 19.10.2026, 21:55

Teraz piszę notatkę z wynikami i propozycjami wpisów do wspólnych notatek.

### <a id="w8"></a>8. Claude · 19.10.2026, 21:57

Codex (model Sol) wciąż sprawdza liczby; jego wynik przyjdzie sam. Do tego czasu policzone i zapisane w repozytorium jest:
- skrypty i wyniki w commicie `d6f63e4`;
- notatka [notatki/a5_ekonomia.md](../notatki/a5_ekonomia.md) w commicie `77c18aa`.

Po odpowiedzi Codeksa uwzględnię jego uwagi i przyjdę z całością na przegląd.

### <a id="w9"></a>9. Claude · 19.10.2026, 21:59

Codex potwierdził co do sztuki wszystkie liczby, które dał do niezależnego przeliczenia. Ma osiem uwag do scenariuszy i opisów. Wprowadzam je.

### <a id="w10"></a>10. Claude · 19.10.2026, 22:01

Wprowadzam poprawki po recenzji do skryptu scenariuszy. Brakuje jeszcze jednej kolumny, dokładam ją i uruchamiam skrypt.

### <a id="w11"></a>11. Claude · 19.10.2026, 22:02

Liczby po poprawkach są gotowe. Aktualizuję notatkę i zapisuję podsumowanie recenzji.

### <a id="w12"></a>12. Claude · 19.10.2026, 22:03

Teraz sekcje 6 i 7 notatki: dodatkowość i rachunek „naprawić albo wyłączyć” po poprawkach.

### <a id="w13"></a>13. Claude · 19.10.2026, 22:05

Ekonomia kampanii jest policzona, sprawdzona przez Codeksa (model Sol) i zapisana w repozytorium. Proszę o przegląd. To jedyne zatrzymanie w tym punkcie.

**Najważniejsze: wynik kampanii na L4 zależy od reguły źródła.** Pozyskują pacjenta taniej niż reszta kampanii płatnych, ale ten pacjent zostawia prawie o połowę mniej marży. Dlatego wynik na pacjenta jest blisko zera, a jego znak zależy od reguły źródła.

Tabela dotyczy okresu 2 i kohort od 1.10.2025 do 2.07.2026. Wynik to marża w 90 dniach minus koszt pozyskania:

| Kampanie | Reguła źródła | Koszt pozyskania | Marża w 90 dniach | Wynik na pacjenta |
|---|---|---|---|---|
| Dwie nowe kampanie na L4 | pierwsze wejście z kodem (przyjęta) | 32,7 zł | 36,3 zł | **+3,6 zł** |
| Dwie nowe kampanie na L4 | sesja płatności | 45,6 zł | 36,1 zł | **−9,4 zł** |
| Pozostałe kampanie płatne | przyjęta / sesja płatności | 44,2 / 43,8 zł | 64,2 / 62,4 zł | +20,0 / +18,7 zł |

**Osobno każda z dwóch kampanii:**
- TikTok traci w obu regułach: −4,6 zł i −17,8 zł na pacjenta.
- Meta na L4 jest niepewna: +6,5 zł albo −6,5 zł.
- Przez rok kampanie te dają od +15,9 tys. zł do −59,5 tys. zł marży, zależnie od reguły.

**Skąd niska marża.** Pacjent nowych kampanii zostawia o 27,9 zł mniej niż pacjent pozostałych kampanii płatnych. Składa się na to:
- kody rabatowe: −12,8 zł;
- brak powrotów: −12,1 zł;
- zwroty po wizycie: −8,7 zł.

Tańszy lekarz (internista) oddaje +16,2 zł. Zwrotem kończy się 17,4% wizyt L4 tych pacjentów, wobec 5,3% u pozostałych.

**Naprawić albo wyłączyć, rocznie, według przyjętej reguły:**
- **Zwroty L4 do poziomu pozostałych pacjentów** to największa dźwignia: od +22 do +57 tys. zł.
- **Zgoda marketingowa i przeglądarki wbudowane w aplikacje** dają w tym rachunku prawie nic. Zgoda nie zmienia powrotu tych pacjentów: 4,2% ze zgodą wobec 4,1% bez niej.
- **TikTok:** wyłączenie nie pogarsza marży przy żadnej regule i żadnym udziale pacjentów dodatkowych.
- **Meta na L4:** wyłączenie kosztuje 27,8 tys. zł albo daje 28,7 tys. zł, zależnie od reguły, przy założeniu, że wszyscy jej pacjenci są dodatkowi.

**Czy pacjenci są dodatkowi, dane nie rozstrzygają.** Łączne pozyskanie w pozostałych kanałach po startach kampanii nie spadło wyraźnie. Po starcie kampanii Meta widać jednak słaby sygnał przejmowania pacjentów L4 z innych kanałów: wskaźnik 0,73, gdzie 1 oznacza brak zmiany, z przedziałem od 0,56 do 0,95. Rozstrzygnie to test: wyłączyć kampanię w losowej połowie województw na 4–6 tygodni.

**Twoja hipoteza o porannych opóźnieniach to tylko scenariusz.** Kosztowałaby od 0 do 65 tys. zł marży rocznie, w wariancie wąskim około 12 tys. zł. W wariancie szerokim zjada cały dodatni wynik nowych kampanii.

**Dwie rzeczy poza samymi kampaniami na L4:**
- **Według sesji płatności prawie każda kampania płatna pozyskująca pacjentów ma wynik ujemny.** To cecha tej reguły, a nie błąd kodu.
- **Google Ads na specjalistów (`gs_generic_specjalisci`) traci pieniądze przy obu regułach.**

**Prowizja dla rankingu lekarzy w okresie 2:** 15 425 zł według przyjętej reguły, 10 125 zł według sesji płatności, 7 375 zł według kodu RANKING10.

**Recenzja Codeksa.** Codex przeliczył wszystkie liczby główne własnym kodem i wszystkie się zgadzają. Miał 8 uwag do scenariuszy i opisów, wszystkie wprowadziłem. Kierunek żadnego wyniku się nie zmienił.

Szczegóły i propozycje wpisów do wspólnych notatek są w [notatki/a5_ekonomia.md](../notatki/a5_ekonomia.md), w sekcji 9.

### <a id="w14"></a>14. Kuba · 20.10.2026, 09:18

Przyjmuję wyniki do scalenia, z jednym dopiskiem. W narzędziu i przy priorytetach pokazuj obok wyniku po 90 dniach także wynik po 180 dniach. Pacjenci kampanii na L4 prawie nie wracają, a pozostali tak, więc 90 dni zaniża wartość pozostałych kampanii.

### <a id="w15"></a>15. Claude · 20.10.2026, 09:20

Dopisuję do notatki wynik po 180 dniach w rachunku „naprawić albo wyłączyć” i decyzję Kuby, potem zapisuję zmiany.

### <a id="w16"></a>16. Claude · 20.10.2026, 09:20

Zostawiam krótką notatkę przekazania dla sesji prowadzącej we wspólnym folderze.

### <a id="w17"></a>17. Claude · 20.10.2026, 09:21

Ekonomia kampanii jest skończona i ma Twoją akceptację. Wynik po 180 dniach stoi teraz obok wyniku po 90 dniach w notatce i w raporcie. Wszystko jest w czterech commitach na master: `d6f63e4`, `77c18aa`, `8e362bf` i `24ac35d`.

**Najważniejsze wyniki** (okres 2, wynik na pacjenta = marża minus koszt pozyskania):
- **Nowe kampanie na L4 razem:**
  - według przyjętej reguły źródła koszt pozyskania to 32,7 zł, a wynik +3,6 zł po 90 dniach i +7,0 zł po 180 dniach;
  - według sesji płatności koszt to 45,6 zł, a wynik −9,4 zł i −5,2 zł;
  - znak zależy od reguły, więc wynik jest niepewny.
- **Pozostałe kampanie płatne:** +20,0 zł po 90 dniach i +29,7 zł po 180 dniach według przyjętej reguły. Według sesji płatności +18,7 zł i +27,5 zł.
- **TikTok traci przy obu regułach.** Meta na L4 jest niepewna.
- **Okno 180 dni zmienia ocenę dwóch kampanii Google Ads.** `gs_generic_lekarz_online` i `gs_generic_erecepta` są po 180 dniach dodatnie przy obu regułach.
- **Prowizja dla rankingu lekarzy w okresie 2:** 15 425 zł według przyjętej reguły, 10 125 zł według sesji płatności i 7 375 zł według kodu RANKING10.

**Gdzie są szczegóły:**
- propozycje wpisów do wspólnych notatek są w sekcji 9 pliku [notatki/a5_ekonomia.md](../notatki/a5_ekonomia.md): założenia 39–43, znaleziska, plan, opis skryptów i decyzja;
- Twoja decyzja i dopisek są w sekcji 11;
- dla sesji prowadzącej zostawiłem krótką notatkę przekazania we wspólnym folderze sesji.

**Co zostało otwarte** (sekcja 8 notatki):
- czy pacjenci nowych kampanii są dodatkowi; rozstrzygnie to test z wyłączeniem kampanii w losowej połowie województw;
- która reguła źródła jest bliższa prawdy dla kampanii bez kodu;
- powód zwrotów po wizytach L4;
- koszt porannej obsady internistów;
- Google Ads na specjalistów (`gs_generic_specjalisci`), który traci pieniądze w każdym wariancie.

### <a id="w18"></a>18. Kuba · 20.10.2026, 12:31

wznów, chyba, że zakończyłeś

### <a id="w19"></a>19. Claude · 20.10.2026, 12:32

Skończyłem, więc nie ma czego wznawiać. Ekonomia kampanii ma Twoją akceptację z dopiskiem o wyniku po 180 dniach. Jest zapisana w czterech commitach na master: `d6f63e4`, `77c18aa`, `8e362bf` i `24ac35d`.

Sprawdziłem stan repozytorium: nie ma niezapisanych zmian. Plik ze skryptem ekonomii jest taki sam jak w moim ostatnim commicie. Po mnie nowa sesja prowadząca dodała commit `96eefba` ze szkicem punktu C.

Propozycje wpisów do wspólnych notatek są w [notatki/a5_ekonomia.md](../notatki/a5_ekonomia.md), w sekcji 9. Scali je sesja prowadząca. Ta sesja niczego więcej nie zmienia.

### <a id="w20"></a>20. Kuba · 20.10.2026, 14:12

zamykamy tą sesję. zaktualizuj pamięć jeśli coś zostało i zamknij

### <a id="w21"></a>21. Claude · 20.10.2026, 14:13

Pamięć jest zaktualizowana, a sesję możesz zamknąć.

W pamięci zmieniłem jedną rzecz: do istniejącej notatki o wklejaniu długich skryptów przez powłokę dopisałem, co się popsuło w tej sesji. Wniosek dla kolejnych sesji: takie skrypty zapisywać najpierw do pliku. W międzyczasie inna sesja dodała tę notatkę do spisu pamięci, więc usunąłem drugi, zdublowany wpis.

Twojego dopisku o wyniku po 180 dniach nie zapisywałem w pamięci. Jest już w repozytorium, w [notatki/a5_ekonomia.md](../notatki/a5_ekonomia.md), w sekcjach 9 i 11. Stamtąd sesja prowadząca przeniesie go do wspólnych notatek.

Cała praca tej sesji jest w czterech commitach na master: `d6f63e4`, `77c18aa`, `8e362bf` i `24ac35d`. Nie zostało nic niezapisanego.

*Wiadomość od sesji „D: poprawki po konsylium (sesja prowadząca)”: [2026-10-21_d-poprawki-po-konsylium-sesja-prowadzaca.md, wiadomość 57](2026-10-21_d-poprawki-po-konsylium-sesja-prowadzaca.md#w57).*

### <a id="w22"></a>22. Claude → sesja [„D: poprawki po konsylium (sesja prowadząca)”](2026-10-21_d-poprawki-po-konsylium-sesja-prowadzaca.md) · 21.10.2026, 22:38

> Wątek ekonomii kampanii (a5-ekonomia): nic nowego, nie utworzyłem żadnego pliku pamięci.
>
> Wszystko, czego się tu nauczyłem, jest już w repozytorium. Wynik po 180 dniach obok wyniku po 90 dniach jest w DECYZJE.md. Scenariusz z wariantem „brak efektu” jest w ZALOZENIA.md, w punkcie 43. Zakaz sumowania kwot z różnych horyzontów jest w punkcie 51. Poprawki rachunków po Codeksie są w notatki/recenzje/a5e_codex.md.
>
> Jedno zdanie do dopisania w istniejącym wpisie odsetki-puste-wypadaja-z-mianownika.md: to samo dzieje się w pandas. Kolumna liczb całkowitych z pustymi wartościami (np. dni_R2 z DuckDB przez .df()) ma typ Int64 z pd.NA. Wtedy (x <= 90).mean() pomija puste i liczy odsetek tylko wśród tych, którym zdarzenie kiedyś zaszło. W tym wątku dało to 88,6% zamiast 4,1%. Przed porównaniem trzeba zrobić fillna(10**6).
>
> Kończę pracę.

### <a id="w23"></a>23. Claude · 21.10.2026, 22:39

Nie dodałem nic do pamięci, bo wszystko z ekonomii kampanii jest już w repozytorium. Wynik po 180 dniach obok wyniku po 90 dniach jest w `DECYZJE.md`. Scenariusz z wariantem „brak efektu” to założenie 43 w `ZALOZENIA.md`. Zakaz sumowania kwot z różnych horyzontów to założenie 51.

Sesji prowadzącej przekazałem jedno zdanie do dopisania w istniejącym wpisie o pustych wartościach w odsetkach. W pandas puste wartości też wypadają z mianownika. W tej sesji dało to najpierw 88,6% zamiast 4,1% powrotu, zanim to poprawiłem. Dopisze je sama.

Kończę pracę w tej sesji. Zamknięciem wątków zajmuje się sesja prowadząca.
