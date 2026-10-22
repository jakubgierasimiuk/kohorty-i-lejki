# Propozycja Claude (Opus 5.5, sesja grafiki) — runda 1, pisana przed przeczytaniem pozostałych

## A. Werdykt
System kart, znaczników i priorytetów jest spójny i wygląda profesjonalnie. Najsłabsza jest warstwa wykresów: wykresy liniowe mają domyślną legendę biblioteki („Dzień: — □ Przychód: —”), nachodzące numery zdarzeń, za dużo serii bez wyróżnienia i pokazują nie to, co mówi wniosek nad nimi (np. „Wynik biznesu” mówi o marży przed kosztem kampanii wobec wydatków, a wykres pokazuje przychód i trzy koszty). Najważniejsze liczby analizy (rozbicie +52%, spadek powrotu w 4 oknach, mostek od dashboardu, wartość priorytetów) są podane tekstem albo tabelą, choć każda z nich to jeden prosty obraz. Układ: w lejku dowód (filtry i wykres) jest za ekranem tekstu; tabele kwartałów i kohort nie mieszczą się w karcie; tytuł i wniosek karty są oba pogrubione, więc hierarchia jest płaska; zastrzeżenia i kafelki to karty w kartach.

## B. System wizualny
- **Kolor:** zostaje granat paska, tło, białe karty i akcent `#1f5fcc` tylko dla interakcji. Rozdzielić akcent od danych: seria „ostatnie 12 miesięcy” w kolorze danych (np. `#2a78d6` zostaje), ale **„rok wcześniej” zawsze szary** (`#8a94a6`) we wszystkich wykresach (dziś czarna kreska w lejku, ciemnoszara linia w krzywej, pomarańcz w innych). Stałe przypisanie bytów do kolorów na całej stronie: „nowe kampanie na L4” = pomarańcz (`--series-2`) wszędzie, „pozostałe kanały” = niebieski. Tła okresów A/B na wykresach dziennych słabsze (lub tylko pasek pod osią X).
- **Typografia:** jedna rodzina (Segoe UI Variable), skala 13 / 14 / 16 / 18 / 22 / 28 px. Tytuł karty 18 px półgruby, **wniosek 16 px zwykły w kolorze `--ink`** (dziś pogrubiony — konkuruje z tytułem). Cyfry tabelaryczne w tabelach, kafelkach i podpisach wykresów.
- **Układ:** treść do 1 200 px, proza do ~70 znaków. Na komputerze karta z wykresem w układzie „tekst po lewej, wykres po prawej” (60/40), gdy wykres jest mały (hantle, słupek skumulowany). Bez kart w kartach: zastrzeżenie jako wiersz z ikoną i cienką kreską nad nim, kafelki w „Czy to wzrost” jako rząd bez cienia z cienkimi separatorami.
- **Komponenty:** odnośniki bez podkreślenia (podkreślenie po najechaniu), „Zobacz w danych” jako małe przyciski z ikoną strzałki. Własna legenda HTML nad wykresem (kreska koloru + nazwa), wartości w podpowiedzi, podpis bezpośredni na końcu linii. Numery zdarzeń na wykresach w pasku nad wykresem, rozsunięte, z podpowiedzią (krótka nazwa). Linie zdarzeń ciągłe i jasne, nie przerywane.
- **Nawigacja:** bez zmian na komputerze; na telefonie zostaje zawijanie (wszystkie zakładki widoczne).

## C. Zakładka po zakładce (najważniejsze)
| Zakładka | Element | Dziś | Propozycja | Dane | Wysiłek |
|---|---|---|---|---|---|
| Czy to wzrost | Więcej pacjentów | punkty z liczbami | słupek skumulowany dwóch lat: pozostałe kanały + nowe kampanie (widać +52% i +7%) | kohorty.js, w przeglądarce | M |
| Czy to wzrost | Lepsza retencja | tabela 4 okien | wykres hantlowy: 30/60/90/180 dni, rok wcześniej (szary) → ostatnie 12 m; tabela do „Szczegółów” | kohorty.js albo komórki tabeli, w przeglądarce | S–M |
| Czy to wzrost | TelemediGO | tabela 3 typów | poziomy słupek skumulowany obu lat (3 części) | wymaga eksportu (liczby w polu danych) albo z tabeli | S |
| Kohorty | wykres dzienny | 3 serie, domyślna legenda | wyróżnienie wybranej serii, reszta szara; legenda własna; rozsunięte zdarzenia | w przeglądarce | M |
| Kohorty | panel filtrów | 13 pól naraz | 4 najczęstsze widoczne, reszta pod „Więcej filtrów” | — | S |
| Lejek | kolejność | tekst → karty napraw → filtry → wykres | wniosek → filtry → wykres kroków → trend → karty napraw → tabela | — | S |
| Lejek | trend | wykres dzienny | miesięczna konwersja nowych osób, rok wcześniej szary; pod nim (osobny wykres, ta sama oś X) udział sesji nowych kampanii | lejek_*.js, w przeglądarce | M |
| Po zakupie | punktualność | 4 pory w kolorach | „Rano” wyróżnione, pozostałe szare | w przeglądarce | S |
| Po zakupie | godziny | tabela 24 wierszy | mapa ciepła godzina × rok albo słupki hantlowe | po_zakupie.godziny, w przeglądarce | M |
| Zdarzenia | oś | same numery | krótka nazwa przy kropce, podpowiedź, kliknięcie przewija do karty; „Skąd wiemy” zwinięte | zdarzenia.js | M |
| Wynik biznesu | wykres | przychód + 3 koszty | dwa wykresy jeden pod drugim: (1) marża przed kosztem kampanii i wydatki na kampanie (ta sama jednostka, jedna oś), (2) marża po wszystkich kosztach w słupkach miesięcznych | wynik.js, w przeglądarce | M |
| Wynik biznesu | tabela kwartałów | ucięta | zawężona: kolumny metryk jako wiersze albo przewijanie z przyklejoną 1. kolumną | — | S |
| Jakość danych | mostek | tabela | wykres wodospadowy dla zamówień i przychodu (dashboard → duplikaty → testy → zwroty) | jakosc.mostek.kroki, w przeglądarce | M |
| Jakość danych | duplikaty | tekst | słupki dzienne zamówień z kopiami (czerwiec 2026) | jakosc.duplikaty.*_d, w przeglądarce | S |
| Priorytety | przegląd | tabela | wykres przedziałów wartości (od–do, tys. zł rocznie) na wspólnej osi z zerem, kolor = pewność (z ikoną i słowem w wierszu) | wymaga eksportu (liczby od/do) | M |
| Czego nie wiemy | tabela | długa tabela | bez wykresu; pozycja listy jako przycisk, wiersze pogrupowane według pozycji | — | S |

## D. Formy
- **Wykresy kołowe: nie.** Żadna liczba w tym projekcie nie jest „częścią całości na jedno spojrzenie” bez porównania z rokiem wcześniej; tam, gdzie są części całości (TelemediGO, nowe kampanie w pacjentach), zawsze porównujemy dwa lata — słupki skumulowane robią to lepiej. Udział 29% nowych kampanii to dwie części → pasek-licznik.
- **Infografika:** jedna — diagram werdyktu (dwa warunki wzrostu z wynikiem) już jest. Nie rysujemy „drzewa przyczyn” — dane nie rozstrzygają przyczyn.
- **Tak:** wodospad (mostek), hantle (rok do roku), małe wielokrotności (lejek w czasie, punktualność według pory), mapa ciepła (kohorty, godziny), oś czasu zdarzeń. **Nie:** Sankey (lejek jest liniowy, wykres kroków jest lepszy), wskaźniki-zegary, 3D, dwie osie.

## E. Inne elementy
README: jeden zrzut „Czy to wzrost” (PNG w repozytorium) i diagram Mermaid przepływu pracy (dane → kontrola → baza → analiza → eksport → narzędzie). Bez wykresów z liczbami w README (liczby tylko z kontrolowanych tekstów).

## F. Czego nie robić
Nie dublować tabeli wykresem bez schowania tabeli do „Szczegółów”. Nie dodawać ozdobnych mini-wykresów w kafelkach. Nie rysować strzałek przyczynowych. Nie wprowadzać nowych kolorów stanu. Nie łamać zasady „liczby z eksportu”: wykres może pokazać to, co jest w danych, ale podpisy z liczbami tylko z danych.

## G. Dziesięć zmian (wartość ÷ wysiłek)
1. Kolejność w lejku: filtry i wykres zaraz pod wnioskiem (S).
2. Wspólny komponent wykresu liniowego: własna legenda, podpis na końcu linii, rozsunięte zdarzenia z podpowiedzią (M).
3. „Rok wcześniej” zawsze szary, „nowe kampanie” zawsze pomarańczowe (S).
4. Hantle retencji w „Czy to wzrost” (S–M).
5. Słupek skumulowany „Więcej pacjentów” (M).
6. Wynik biznesu: wykres marży przed kampaniami wobec wydatków (M).
7. Wodospad mostka w jakości danych (M).
8. Oś zdarzeń z nazwami (M).
9. Hierarchia karty: wniosek bez pogrubienia, zastrzeżenie bez szarego pudełka, spokojne odnośniki (S).
10. Tabele: mieszczą się albo mają przyklejoną pierwszą kolumnę; wąskie tabele nie rozciągają się (S).
