Jesteś niezależnym recenzentem liczb w projekcie analitycznym (zadanie rekrutacyjne, dane syntetyczne). Pracujesz tylko do odczytu. Odpowiadasz po polsku, krótko i konkretnie.

KONTEKST
- Folder projektu: bieżący katalog. Baza DuckDB: analiza/telemedi.duckdb (schemat `czyste` = dane oczyszczone; otwieraj read_only=True). Python: `python -I`.
- Przyjęte definicje są w analiza/definicje.py (nowy pacjent = pierwsze opłacone zamówienie, dowolny status; powrót = kolejne zamówienie nieanulowane; źródło Z1K = pierwsze wejście pacjenta z anonimowymi sesjami jego przeglądarek, kod kampanii na pierwszym zamówieniu rozstrzyga; Z2 = sesja płatności; koszt lekarza KOSZT_LEKARZA; marża = przychód po zwrotach + TelemediGO − koszt lekarza − wydatki na kampanie − prowizja 25 zł za pierwsze zamówienie pacjenta z afiliacji). Okres 1 = 1.10.2024–30.09.2025, okres 2 = 1.10.2025–30.09.2026, czas polski. Nowe kampanie = meta_prosp_l4_szybko i tt_prosp_l4_15min. Porównanie powrotu w 90 dniach na tych samych dniach kalendarzowych: kohorty 1.10–2.07 w obu latach.
- Nasz kod tej rundy: analiza/e_merytoryka.py → analiza/wyniki/e_merytoryka.txt i .json. Teksty strony: analiza/e_teksty.py (szkic: notatki/e_teksty.md) i README.md.

ZADANIE
Przelicz NIEZALEŻNIE, własnym kodem (nie uruchamiaj e_merytoryka.py jako dowodu), poniższe liczby i dla każdej napisz: zgodne / różnica (Twoja wartość) / nie da się sprawdzić (dlaczego). Potem oceń, czy zdania podane niżej wynikają z tych liczb.

A. Reguły źródła w retencji „bez nowych kampanii” (kohorty okresu 2 z pełnym oknem 90 dni na tych samych dniach co okres 1):
  1. Pacjenci przypisani nowym kampaniom według Z1K, a starym według Z2 („grupa X”): 1 383; ich powrót w 90 dniach 4,34%; grupa odwrotna (stara według Z1K, nowa według Z2): 0 pacjentów.
  2. Bez nowych według Z1K: 14 031 pacjentów, powrót 21,99%, marża w 90 dniach 65,97 zł; według Z2: 15 414, 20,41%, 63,34 zł. Cała różnica to grupa X.
  3. W całym okresie 2 grupa X liczy 2 081 pacjentów; 92,2% z nich miało pierwsze wejście z reklamy nowej kampanii, 72,9% zapłaciło z kodem L4SZYBKO20 albo TIKTOK25, 82,9% zaczęło od L4 u internisty. Nowi pacjenci bez nowych kampanii: 17 419 (Z1K, +7,3% wobec 16 231) i 19 500 (Z2, +20,1%).
  4. Udział nowych kampanii w spadku powrotu (23,91% → 17,38%) liczony jako udział nowych × (powrót reszty − powrót nowych): 71% według Z1K, 46% według Z2, 71% według Z2 po przeniesieniu grupy X do nowych.
B. III kwartał (VII–IX) 2026 wobec 2025, marża całego biznesu w dniach księgowania (przychód i koszt lekarza w dniu płatności zamówienia, TelemediGO w dniu zakupu, wydatki w dniu z pliku kampanii, prowizja w dniu pierwszego zamówienia):
  5. Marża 222 824 zł → 207 713 zł (−6,8%).
  6. TelemediGO kupione osobno (order_id puste): III kw. 2025 225 zakupów (wszystkie od 8.09.2025), III kw. 2026 108; w okresie 2 461 zakupów (1,26 dziennie, 29 na 23 dni). Nadwyżka startu 196 zakupów × 89 zł = 17 440 zł.
  7. Marża III kw. 2025 bez tej nadwyżki: 205 384 zł, czyli III kw. 2026 o +1,1%; bez całej sprzedaży osobnej w obu kwartałach −2,3%; bez wszystkich opłat TelemediGO −4,9%.
  8. Marża przed kampaniami (przychód po zwrotach + TelemediGO − koszt lekarza): 313 530 → 392 493 zł (+25,2%); bez nadwyżki +32,6%. Wydatki na kampanie 87 431 → 181 555 zł (× 2,08).
  9. Cały rok: marża 828 085 → 1 048 069 zł (+26,6%); przed kampaniami 1 211 118 → 1 713 169 zł (+41,5%); wydatki 367 632 → 649 675 zł (+76,7%).
  10. Kwartały IV 2025 – III 2026, zmiana rok do roku marży przed kampaniami: +55,2%, +49,7%, +38,4%, +25,2%; wydatki × 1,30, 1,66, 2,04, 2,08; marża +71,4%, +43,0%, +13,0%, −6,8%.
  11. Baza powracających w III kwartale (marża zamówień i TelemediGO pacjentów, których pierwsze zamówienie było w poprzednich kwartałach): 2025 115 235 zł (w tym 210 zakupów osobnych TelemediGO, 18 690 zł), 2026 106 171 zł (97 zakupów, 8 633 zł). Bez nadwyżki startu: 97 796 zł, czyli +8,6% w 2026; bez całej sprzedaży osobnej +1,0%.
C. Marża na powtórne zamówienie pacjentów spoza nowych kampanii (Z1K), III kwartał, marża = przychód po zwrotach − koszt lekarza:
  12. 2 879 → 3 140 zamówień, 35,86 → 32,81 zł; udział zamówień ze zniżką TelemediGO (discount_type = 'go') 34,3% → 41,6%; marża zamówienia ze zniżką 11,40 → 11,01 zł, bez zniżki 48,89 → 48,78 zł; rozkład symetryczny: struktura −2,71 zł, w obrębie rodzaju zniżki −0,35 zł. Zamówienie u specjalisty (nie internista) ze zniżką TelemediGO w III kw. 2026: −5,59 zł (418 zamówień).
D. Lejek osób, które jeszcze nie kupowały (sesje zwykłe = bez konta na wejściu albo z kontem pojawiającym się na kroku logowania; „jeszcze nie kupowali” = brak zakupu konta albo przeglądarki przed początkiem sesji; dzień sesji w czasie polskim; plik analiza/wyniki/a5p_lejek_dzienny.csv.gz, kolumny k1–k5 = kroki, k5 = płatność):
  13. Konwersja sesji do płatności 11,21% (144 813 sesji) → 9,31% (265 264); wszystkie sesje 16,04% → 13,72%; osoby, które już kupowały, 91,51% → 89,86%.
  14. Zmiana rok do roku miesięcznie: X 2025 – I 2026 od −0,20 do −0,75 punktu, II–III 2026 −1,57 i −1,51, IV–IX 2026 od −2,34 do −3,13. Udział sesji nowych kampanii w lutym 2026 31,8%, od kwietnia 42,1–47,1%.
  15. Bez sesji nowych kampanii: 11,21% → 11,42%; sesje nowych kampanii 5,49%.
  16. Przeglądarki w aplikacjach (Instagram, Facebook, TikTok) wobec Chrome i Safari, osoby, które jeszcze nie kupowały, oba lata: płatność z sesji 3,8–6,6% wobec 9,9–12,2%. Wcześniejsze zdanie „4,8–7,2% wobec 16,1–18,1%” dotyczyło wszystkich sesji, a nie tej grupy.
E. Drobne:
  17. gs_generic_specjalisci, okres 2: wydatki 53 158 zł, marża na pacjenta w 90 dniach 32,4 zł (Z1K) i 32,9 zł (Z2) → próg pauzy 1 641 i 1 616 pacjentów rocznie (około 31 tygodniowo); kampania przypisuje sobie 923 (Z1K) i 657 (Z2) nowych pacjentów rocznie; wszystkich nowych pacjentów z pierwszą wizytą u specjalisty (bez internisty, pediatry i psychiatry): 2 971 i 3 427.
  18. Zamówienia opłacone w sesjach gs_brand i meta_rmkt_koszyk w okresie 2: udział zamówień powtórnych (nie pierwszych zamówień pacjenta) 37,1% i 24,1%.
  19. Zamówienia opłacone 17.05.2025 13:00–13:59: 0; mediana tej godziny w dniach 10–24.05.2025 (z dniami zerowymi): 2.

ZDANIA DO OCENY (czy wynikają z liczb, czy są za mocne albo za słabe):
  a. „Pacjentów przybywa, ale wracają rzadziej. Wydatki na kampanie rosną dużo szybciej niż marża, którą biznes zarabia przed ich kosztem.”
  b. „Spadek marży w III kwartale 2026 (−6,8%) nie jest pewny. Bez tej nadwyżki marża III kwartału 2026 jest o 1,1% wyższa niż rok wcześniej.”
  c. „Marża na powtórne zamówienie spada prawie w całości przez rosnący udział wizyt ze zniżką TelemediGO.”
  d. „Od lutego 2026 płaci coraz mniej nowych osób, bo przybywa ruchu z nowych kampanii na L4.” (Czy „bo” jest uzasadnione rachunkiem? Jeśli nie, zaproponuj brzmienie.)
  e. „Druga reguła przypisuje starym kanałom pacjentów nowych kampanii, którzy weszli z reklamy, a zapłacili w innej sesji; bez nich obie reguły dają to samo.”
  f. „Bez nadwyżki startu baza powracających dała w III kwartale 2026 więcej marży niż rok wcześniej (+8,6%), choć liczy prawie trzy razy więcej pacjentów.”

FORMAT ODPOWIEDZI
1. Tabela: nr | nasza wartość | Twoja wartość | zgodne/różnica/nie sprawdzono | uwaga (jedno zdanie).
2. Zdania a–f: ocena i, jeśli trzeba, poprawione brzmienie.
3. Inne błędy, które zauważyłeś w e_merytoryka.py albo e_teksty.py (najwyżej 5, od najważniejszego).
Nie zmieniaj żadnych plików.
