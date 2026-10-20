# Fable 5.1 (agent Claude Code)

Data: 2026-10-20. Rola: weryfikator z dostępem do plików i bazy oraz osoba oceniająca kandydata.

**Co zrobiłem poza przeczytaniem briefu.** Przeszedłem narzędzie w przeglądarce (lokalny serwer, wszystkie dziewięć zakładek, odnośniki „Pokaż w lejku”, filtry, konsola przeglądarki bez błędów). Przeliczyłem najważniejsze liczby własnym kodem z bazy `analiza/telemedi.duckdb` (schemat `czyste`, tylko odczyt, bez importu skryptów projektu). Mój kod i wydruki: katalog roboczy sesji (`weryfikacja.py`, `weryfikacja2.py`, `weryfikacja3.py` i pliki `*_wynik.txt`), nie w repozytorium.

**Puenta.** Liczby trzymają się co do sztuki: 24 z 24 głównych wartości odtworzyłem niezależnie bez żadnej rozbieżności, w tym nowych pacjentów, powroty na tych samych dniach kalendarzowych, marżę na pacjenta, awarię Safari na iOS z szacunkiem 628–695 utraconych zamówień i marżę po kwartałach. Nie znalazłem błędu, który zmieniałby odpowiedź „nie, to nie jest wzrost w rozumieniu zadania”. Do poprawy są trzy rzeczy ważne: (1) zakładka „Lejek” i README mówią, że przeglądarki wbudowane w aplikacje „trzeba naprawić na stronie”, a w obrębie tej samej kampanii nie konwertują gorzej od zwykłych, czyli to cecha ruchu z reklam, nie strony; (2) etykieta pewności „wysoka co do znaku” przy wstrzymaniu TikToka kłóci się z własnym przedziałem w karcie; (3) spadek marży w III kwartale 2026 nie jest rozłożony na nowe kampanie i resztę biznesu, a rozłożony pokazuje, że nowe kampanie w tym kwartale wychodzą na zero, a spada baza. Do tego kilka drobiazgów (w tym błąd wyświetlania: średnia ocena 4,45 pokazana jako „4,45%”).

---

## 1. Lista poprawek, od najważniejszej

Nie znalazłem poprawki krytycznej (takiej, która zmienia odpowiedź albo kierunek którejkolwiek pozycji listy).

### 1.1 Ważna — „Przeglądarki wbudowane w aplikacje tracą pacjentów na każdym kroku” nie jest problemem strony, tylko ruchu z reklam

- **Miejsce:** zakładka „Lejek”, karta „Przeglądarki wbudowane w aplikacje tracą pacjentów na każdym kroku” pod zdaniem „Dwie rzeczy trzeba naprawić na stronie”; README, sekcja „Co w danych wygląda podejrzanie” nie, ale ZNALEZISKA (A5 pozyskanie, „W skrócie”): „tracimy pacjentów w dwóch miejscach, które trzeba naprawić na stronie: w przeglądarkach wbudowanych w aplikacje i w zakładaniu konta w Safari na iOS”.
- **Co jest nie tak:** porównanie „Instagram/Facebook/TikTok 4,8–7,2% wobec Chrome i Safari 16,1–18,1%” miesza przeglądarkę z kampanią. Prawie cały ruch w przeglądarkach wbudowanych przychodzi z reklam Meta i TikToka, a ten ruch płaci rzadko w każdej przeglądarce.
- **Dowód (moje przeliczenie, okres 2, sesje zwykłe osób, które jeszcze nie kupowały, sesja do płatności):**
  - kampania Meta na L4: w aplikacji 5,99% (46 091 sesji), zwykła przeglądarka 5,58% (14 901 sesji);
  - kampania TikTok na L4: w aplikacji 4,80% (28 160), zwykła 4,56% (5 310);
  - Meta lekarz online: w aplikacji 3,65% (14 708), zwykła 3,51% (7 977);
  - w tych kampaniach także wybór usługi (24,6% wobec 24,3%), wybór terminu (55,8% wobec 56,1%) i krok konta (60,1% wobec 57,6%) są takie same w obu typach przeglądarek;
  - odwrotnie w ruchu bezpłatnym z Google: w aplikacji 14,9% (2 311), zwykła 8,9% (42 414), czyli przeglądarka w aplikacji nie szkodzi.
  Projekt sam to policzył (ZNALEZISKA, ekonomia kampanii, punkt 4: „surowa konwersja w przeglądarkach wbudowanych nie jest w tych kampaniach niższa”), a w „Priorytetach” wycenia to na 0 zł. Zakładka „Lejek” i ZNALEZISKA mówią jednak czytelnikowi co innego.
- **Propozycja:** przepisać kartę na: „Ruch z reklam Meta i TikToka płaci 3–4 razy rzadziej niż wyszukiwarka i traci na każdym kroku, niezależnie od przeglądarki (w obrębie kampanii przeglądarka w aplikacji nie konwertuje gorzej). To problem obietnicy reklamy, odbiorców i strony wejścia, nie przeglądarki.” Zdanie „Dwie rzeczy trzeba naprawić na stronie” zmienić na jedną (Safari na iOS). W ZNALEZISKACH poprawić zdanie „W skrócie”. Odnośnik „Pokaż w lejku” tej karty powinien prowadzić do podziału „Kampania”, nie „Przeglądarka”.

### 1.2 Ważna — pewność pozycji 3 (wstrzymać TikToka): „wysoka co do znaku” kłóci się z własną kartą

- **Miejsce:** zakładka „Priorytety”, tabela przeglądu, wiersz 3, kolumna „Pewność”; karta 3, sekcja „Propozycja”.
- **Co jest nie tak:** tabela mówi „wysoka co do znaku”, a karta: „wynik na pacjenta według przyjętej reguły to −1,1 zł z warunkowym przedziałem od −5,3 do +3,0 zł (299 pacjentów), więc (...) pewny jest tylko brak korzyści”. Przedział obejmuje zero, więc znak w horyzoncie 180 dni według przyjętej reguły nie jest pewny. Pewny jest brak korzyści (wynik w najlepszym razie około zera) i to, że wyłączenie poprawia marżę w każdym wariancie dodatkowości.
- **Dowód:** liczby z karty 3 i z załącznika E6 (TikTok 180 dni, Z1K: −1,1 zł, 299 pacjentów). Sprawdziłem też wydatki: 82 464 zł w 234 dniach i mnożnik 365/234 = 1,56 (−11 928 × 1,56 = −18 607 zł, zgodne z „−18,6 tys. zł”).
- **Propozycja:** w tabeli: „wysoka co do braku korzyści; znak w 180 dniach według przyjętej reguły niepewny (−5,3 do +3,0 zł na pacjenta)”. Treść propozycji („odwracalna pauza”) jest dobra i może zostać.

### 1.3 Ważna — spadek marży w III kwartale 2026 nie jest rozłożony, a rozłożony mówi coś innego niż sugeruje tekst

- **Miejsce:** zakładka „Czy to wzrost”, karta „Wynik pod koniec okresu”; zakładka „Wynik biznesu”, akapit o kwartałach; README („marża była o 6,8% niższa niż rok wcześniej, choć wydatki na kampanie były 2,08 raza wyższe”).
- **Co jest nie tak:** zestawienie „marża −6,8%, choć wydatki ×2,08” zaprasza do odczytania, że to wydatki na nowe kampanie zjadły marżę kwartału. Rozbicie na pacjentów nowych kampanii i resztę (reguła przyjęta, księgowanie w dniu płatności, jak W4) pokazuje inny obraz.
- **Dowód (moje przeliczenie, III kwartał 2026):**
  - pacjenci nowych kampanii: marża przed kosztem pozyskania 88 993 zł (2 589 zamówień), wydatki na obie nowe kampanie w kwartale 87 926 zł (Meta 50 940 zł, TikTok 36 986 zł), czyli wynik +1 067 zł, w praktyce zero;
  - pozostali pacjenci: marża przed kampaniami 303 500 zł, wydatki pozostałych kampanii 93 630 zł (rok wcześniej 87 431 zł), prowizja 3 225 zł, czyli 206 645 zł po wydatkach wobec 222 824 zł rok wcześniej (−16 179 zł, −7,3%);
  - z tych −16 179 zł około −11 214 zł to opłaty TelemediGO (56 693 zł → 45 479 zł; wrzesień 2025 zawyżony startem newslettera, co strona zauważa), a reszta to baza bez wzrostu: przychód z konsultacji pozostałych 577 696 zł wobec 558 212 zł (+3,5%) przy koszcie lekarza +6,1%; szacunek Safari (14–21 tys. zł) mieści się w tej luce.
  Suma rozbicia zgadza się z W4: 88 993 + 303 500 = 392 493 zł (przed kampaniami), 87 926 + 93 630 = 181 556 zł (wydatki).
- **Propozycja:** dopisać do karty „Wynik pod koniec okresu” dwa zdania: „W samym III kwartale 2026 pacjenci nowych kampanii zostawili 89,0 tys. zł marży przy 87,9 tys. zł wydatków, czyli wyszli na zero. Spadek marży kwartału siedzi w pozostałej części biznesu: 206,6 tys. zł po wydatkach wobec 222,8 tys. zł rok wcześniej, z czego około 11,2 tys. zł to niższe opłaty TelemediGO wobec września 2025, a resztę tłumaczy skala awarii Safari na iOS.” To wzmacnia odpowiedź, a nie osłabia: nowe kampanie nie budują wyniku, a stary biznes stoi.

### 1.4 Ważna — dane demograficzne nie są użyte nigdzie, a mówią coś o nowych kampaniach

- **Miejsce:** zakładka „Kohorty” (filtry), „Czy to wzrost” (zastrzeżenie 4 „Struktura pacjentów się zmieniła”), ZALOZENIA (brak punktu o demografii).
- **Co jest nie tak:** `users.csv` ma wiek, płeć, województwo i wielkość miejscowości. Żadna z tych cech nie pojawia się w narzędziu, w notatkach ani w „sprawdzonych cechach” rozkładu struktura/zachowanie. Zadanie każe pociąć kohorty tak, żeby było widać, co zmieniło zachowanie pacjentów; wiek jest tu najprostszym cięciem.
- **Dowód (moje przeliczenie, okres 2, reguła przyjęta):**
  - pacjenci nowych kampanii mają średnio 27,6 roku, pozostali 38,3 roku; w samym L4: 27,6 wobec 36,7 roku; zgoda marketingowa 37,3% wobec 64,3% (to ostatnie strona ma);
  - wiek nie tłumaczy braku powrotów: wśród pacjentów z pierwszym L4 (kohorty do 2.07.2026) nowe kampanie wracają w 3,5% (<30 lat, 2 508 pacjentów), 4,6% (30–44, 1 526) i 4,8% (45+, 42), a pozostali 13,6% (767), 13,4% (1 515) i 15,0% (687). To dobry argument za tezą strony („sprawdzone cechy nie tłumaczą”), którego strona nie ma;
  - bez nowych kampanii powrót spada w każdej grupie wieku o 1–2 punkty procentowe (30–44 lat: 23,2% → 22,0%; 45–59: 25,5% → 23,2%), więc zmiana wieku nie tłumaczy też spadku w starych kampaniach;
  - udział nowych kampanii według województwa jest jednorodny (26–31% nowych pacjentów), co wprost wspiera projekt testu w parach województw z pozycji 9. Tej liczby w karcie 9 brakuje.
- **Propozycja:** dodać filtr i podział „Wiek” (cztery przedziały) w „Kohortach”, jedno zdanie o wieku do zastrzeżenia 4 w „Czy to wzrost”, zdanie o jednorodności województw do karty 9. Jeśli nie ma czasu na filtr, przynajmniej punkt w ZALOZENIACH: „demografii nie użyliśmy, sprawdziliśmy, że wiek nie zmienia wniosku”.

### 1.5 Ważna — konta, które nigdy nie kupiły: 11 482 kont (21,9%) bez żadnego zamówienia, nikt o nich nie pisze

- **Miejsce:** zakładka „Lejek” (brak), „Priorytety” (brak), „Czego nie wiemy” (brak).
- **Co jest nie tak:** lejek kończy się na kroku płatności w sesji, ale nie mówi, że część osób zakłada konto i nigdy nie płaci. To stała, duża grupa, poza zasięgiem CRM.
- **Dowód (moje przeliczenie):** 11 482 z 52 400 kont nie ma ani zamówienia, ani TelemediGO; odsetek według kwartału rejestracji stały 20,9–23,6% (lekko rośnie w 2026: 22,7% w II kw., 23,6% w III kw.). 58,1% z nich ma zgodę marketingową. Żadne z tych kont nie ma ani jednej sesji z newslettera ani SMS-a, czyli CRM do nich nie pisze. W okresie 2 sesji z krokiem konta bez płatności było 10 396, z czego 7 551 to osoby, które nigdy nie kupiły.
- **Propozycja:** jedno zdanie w „Lejku” (sekcja „Sesje poza lejkiem głównym” albo przy kroku „Wejście na płatność”) i pozycja na liście niewiadomych: „czy sekwencja do kont bez zakupu (z grupą kontrolną) odzyskuje część z około 1 800 kont kwartalnie”. Nie wyceniałbym tego w złotych bez testu.

### 1.6 Ważna (spójność) — ta sama miara „L4 z pozostałych kanałów” ma w narzędziu dwie różne wartości

- **Miejsce:** zakładka „Czy to wzrost”, sekcja „Lepsza retencja: nie”, zdanie „pacjenci z pierwszym L4 z pozostałych kanałów wracają w 13,9% (2 797 pacjentów) wobec 14,8% (2 639)”; załącznik E1 (W2) i zakładka „Kohorty” z filtrem „Pierwsza usługa: Internista: L4” + „Pozostałe kampanie i kanały”: 13,8% (2 969) wobec 14,6% (2 795).
- **Co jest nie tak:** 13,9/14,8 pochodzi z `a5r_struktura.txt` 3d, gdzie „pozostałe kanały” wyłączają też kampanię Meta lekarz online (grupa 1) i TikTok. Czytelnik, który kliknie w „Kohorty”, dostanie 13,8/14,6 i nie znajdzie 13,9/14,8. Wniosek („bez istotnej zmiany”) jest w obu wersjach ten sam.
- **Propozycja:** użyć liczb W2 (13,8% z 2 969 wobec 14,6% z 2 795), bo te da się odtworzyć filtrami strony, albo dopisać „bez kampanii Meta i TikToka”.

### 1.7 Drobna (błąd wyświetlania) — średnia ocena pokazana jako procent

- **Miejsce:** zakładka „Po zakupie”, tabela „Oceny według opóźnienia wizyty”, kolumna „Średnia ocena (1–5)”: strona pokazuje „4,45% z 3 446”, „2,92% z 469” itd. (sprawdzone w przeglądarce, nie artefakt eksportu tekstu).
- **Dowód:** `narzedzie/widoki.js`, funkcja `komorka`: `j = jedn || "%"` traktuje pustą jednostkę `""` jak brak i dokleja „%”. Wywołanie w `rysujOceny` przekazuje `""`.
- **Propozycja:** `var j = jedn === undefined ? "%" : jedn;` (albo przekazać jednostkę `"pkt"`). Średnia 4,45 z 3 446 ocen zgadza się z moim przeliczeniem.

### 1.8 Drobna — „nie działa zakładanie konta” to za mocne słowa

- **Miejsce:** zakładka „Lejek” (nagłówek karty), zdarzenie 12 („przestaje działać”), README („gwałtownie spada skuteczność”).
- **Co jest nie tak:** krok konta spadł z 66% do 45%, a nie do zera; karta 1 sama mówi „konta dalej powstają, ale rzadziej: 668 zamiast 1 082 w 60 dniach”. Potwierdzam: logowanie powracających w Safari na iOS działa w 100% przed i po (1 430 i 1 681 sesji z wyborem terminu).
- **Propozycja:** „zakładanie konta psuje się dla około jednej trzeciej osób” zamiast „nie działa”.

### 1.9 Drobna — koszt testu Meta (pozycja 9) podany tylko dla 6 tygodni

- **Miejsce:** karta 9, „Test kosztuje najwyżej około 1,6–1,8 tys. zł utraconej marży”.
- **Dowód:** `c_priorytety.txt` P11: 1 606 zł (dni działania) i 1 766 zł (pełny rok) przy 6 tygodniach i połowie kraju. Przy 4 tygodniach to około 1,1–1,3 tys. zł. Przedział „1,6–1,8” to dwie wersje przeliczenia tej samej 6-tygodniowej kwoty, nie zakres 4–6 tygodni.
- **Propozycja:** „do około 1,8 tys. zł przy 6 tygodniach (1,2 tys. zł przy 4)”.

### 1.10 Drobna — niewiadoma 2 jest szersza niż wynik po 180 dniach

- **Miejsce:** „Czego nie wiemy”, wiersz 2: „kampanie bez kodu (Google Ads ogólne, Meta lekarz online)”.
- **Dowód:** ZNALEZISKA, ekonomia, „Co zmienia okno 180 dni”: `gs_generic_lekarz_online` i `gs_generic_erecepta` są po 180 dniach dodatnie w obu regułach; zależne od reguły zostają `gs_generic_l4` i `meta_prosp_lekarz_online` (i Meta na L4).
- **Propozycja:** wymienić te dwie (trzy) kampanie z nazwy.

### 1.11 Drobna — jedno zamówienie na granicy okresów w „Lejku”

- **Miejsce:** zakładka „Lejek”: „24 717 płatności” i „38 490 płatności” wobec 24 716 i 38 491 zamówień w „Wyniku biznesu”.
- **Dowód:** odtworzyłem obie pary. Różnica to jedna sesja rozpoczęta 30.09.2025 przed północą z płatnością już 1.10.2025: lejek liczy według dnia sesji, zamówienia według dnia płatności.
- **Propozycja:** przypis przy liczbach lejka („według dnia rozpoczęcia sesji”).

### 1.12 Drobna (narzędzie) — odnośniki „Pokaż w lejku” zmieniają filtry, ale nie przewijają do tabeli

- **Miejsce:** zakładka „Lejek”, karty u góry; odnośniki z „Zdarzeń” i „Priorytetów”.
- **Dowód:** po kliknięciu „Pokaż w lejku” przy Safari strona poprawnie ustawia „Jeszcze nie kupowali”, „System i przeglądarka”, okresy 16.01–16.03 i 17.03–15.05 i zaznacza „Safari na iOS” (w tabeli: 45,1% z 1 553, A: 66,2% z 1 763), ale widok zostaje u góry strony, więc czytelnik nie widzi, że coś się zmieniło.
- **Propozycja:** po zmianie filtrów z odnośnika przewinąć do tabeli (`scrollIntoView`).

### 1.13 Drobna — poranne opóźnienia: przedział „Południe (12–15)” ukrywa, że 12:00 jest jeszcze w problemie

- **Miejsce:** zakładka „Po zakupie”, tabela według pory; karta 6.
- **Dowód (moje przeliczenie, internista, od II 2026, wizyty odbyte, opóźnienie ponad 15 minut):** 5:00 17,3%, 6:00–10:00 49–54%, 11:00 41,8%, 12:00 28,2%, 13:00 6,6%, 14:00 i później 2–4%. Zaległość narasta od 6:00 i znika około 13:00. To wygląda na jedną zmianę poranną z za małą obsadą, a nie na przeciążenie całego dnia.
- **Propozycja:** w karcie 6 dopisać profil godzinowy (jedno zdanie), bo to konkretny trop do diagnozy grafików („zmiana kończąca się około 13:00”).

---

## 2. Co się potwierdziło (moje przeliczenia wobec narzędzia i raportów)

Wszystko poniżej liczyłem od zera z `czyste`, własnymi definicjami według `ZALOZENIA.md`.

| Liczba | Narzędzie / raport | Moje przeliczenie | Zgodność |
|---|---|---|---|
| Nowi pacjenci, okres 1 / 2 | 16 231 / 24 687 | 16 231 / 24 687 | tak |
| Powrót w 30 dniach, te same dni (do 31.08) | 11,0% (14 984) / 7,8% (22 646) | 11,02% / 7,84% | tak |
| Powrót w 60 dniach (do 1.08) | 19,1% (13 941) / 13,7% (20 823) | 19,09% / 13,73% | tak |
| Powrót w 90 dniach (do 2.07) | 23,9% (12 867) / 17,4% (18 924) | 23,91% / 17,38%; powracających 3 076 / 3 289 | tak |
| Powrót w 180 dniach (do 3.04) | 27,5% (9 125) / 22,2% (12 591) | 27,47% / 22,24% | tak |
| Marża na pacjenta w 90 dniach | 66,6 zł / 58,3 zł | 66,60 / 58,30 zł | tak |
| Marża na pacjenta w 180 dniach | 75,5 zł / 67,7 zł | 75,45 / 67,68 zł | tak |
| Nowi pacjenci nowych kampanii, Z1K / Z2 | 7 268 / 5 187 | 7 268 / 5 187 | tak |
| Kanały bezpłatne (Z1K) | 7 069 → 7 924 | 7 069 → 7 924 | tak |
| Powrót 90 dni bez nowych kampanii, Z1K / Z2 | 22,0% (14 031) / 20,4% (15 414) | 21,99% / 20,41% | tak |
| Powrót 90 dni nowych kampanii | 4,1% (4 893) | 4,15% (4 893) | tak |
| Safari iOS, krok konta, 60 dni przed / po | 66,2% (1 763) / 45,1% (1 553) | 66,2% / 45,1% | tak |
| Pozostałe przeglądarki, te same dni | 64,8% / 63,4% | 64,8% / 63,4% | tak |
| Safari iOS, 1.10.2025–16.03 / 17.03–30.09 | 66,1% / 45,6% (4 678 sesji) | 66,1% / 45,6% (4 678) | tak |
| Utracone pierwsze zamówienia, 198 dni | 695 / 628 po odjęciu tła | 695 / 628 | tak |
| Marża nowego pacjenta z Safari iOS, 90 / 180 dni | 64,6 zł (2 990) / 74,3 zł (2 278) | 64,60 (2 990) / 74,32 (2 278) | tak |
| Marża po kwartałach (8 kwartałów) | 151 340 … 207 713 zł | identyczne co do złotówki | tak |
| Sumy okresów: zamówienia, przychód po zwrotach, GO, koszt lekarza, wydatki, prowizja, marża | 24 716 / 38 491; 2 230 266 / 3 228 342; 156 551 / 219 652; 1 175 700 / 1 734 825; 367 632 / 649 675; 15 400 / 15 425; 828 085 / 1 048 069 | identyczne (przychód 2 230 267, zaokrąglenie) | tak |
| Dashboard na surowych | 25 269 / 40 613 zamówień; 16 251 / 24 689 pacjentów; 2,382 / 3,580 mln zł; 604 duplikaty | identyczne | tak |
| Konta testowe | 22 kont, 2 071 zamówień, wszystkie 1 minuta | 22 kont, 2 102 wierszy z duplikatami (31 kopii), wszystkie 1 minuta | tak |
| Wydatki: Meta L4 332 dni, TikTok 234 dni, gs_generic_specjalisci okres 2 | 163 322 / 82 464 / 53 158 zł | identyczne | tak |
| gs_generic_specjalisci, nowi okres 2, Z1K / Z2 | 923 / 657 | 923 / 657 | tak |
| Zwroty L4, okres 2: nowe kampanie / pozostali | 17,4% (1 024 z 5 895) / 5,3% (270 z 5 080) | identyczne | tak |
| Zwroty po wizycie nowych kampanii: wizyty, zł, koszt lekarza | 1 044 / 84 112 / 33 975 | identyczne | tak |
| Odnowienia TelemediGO | 62 z 1 140 | 62 z 1 140 | tak |
| Sesje na kliknięcie | Google 0,92–0,93, Meta 0,79–0,82, TikTok 0,72 | 0,923–0,925; 0,786–0,822; 0,723 | tak |
| Poranne opóźnienia internisty, miesiące (wszyscy) | 15,6% XI 2025 … 48,4–52,6% | 15,6; 29,7; 41,8; potem 48,4–52,6 | tak |
| Średnia ocena, internista, do 5 minut, okres 2 | 4,45 (3 446) | 4,45 (3 446) | tak |

Sprawdzone rachunki pochodne (z liczb załączników): rozbicie spadku powrotu 46–71% (3,0/6,5 i 4,6/6,5); +7,3% i +20,1% bez nowych kampanii; TelemediGO 905+629+225 = 1 759 i 1 089+918+461 = 2 468, udziały 26/41/33%; 5,58% → 4,41% (471 i −287); −15,57 zł na członkostwo (183 939 − 156 551 = 27 388 / 1 759); mnożniki 365/234 = 1,56 i 365/332 = 1,10; TikTok −18,6 / −48,0 / +128,6 tys. zł; Meta próg 85,4% i 84,5% (163 322 / 191 167 i 163 322 / 193 204); gs_generic_specjalisci −23,2 / −31,5 tys. zł; 1 158 i 1 281 zamówień rocznie i 75–83 / 86–95 tys. zł; 23 601 zł na punkt powrotu; 73 630 i 70 780 zł cennika; 37 950 zł za testy; sumy miesięczne i kwartalne w „Wyniku biznesu” zgadzają się z sumami okresów; +26,6%, +8,1%, +3,1% w zastrzeżeniu 3.

Definicje: nowy pacjent, powrót (nieanulowane), źródło (dwie reguły, kod rozstrzyga), przychód po zwrotach, koszt lekarza także za zwrócone, prowizja 25 zł według reguły, porównanie na tych samych dniach kalendarzowych, obcinanie okresu A do dojrzałej części B — wszystkie zapisane i zastosowane konsekwentnie; odtworzyłem je bez zaglądania w kod projektu i dostałem te same liczby.

Narzędzie: dziewięć zakładek otwiera się ze ścieżek względnych (poprawne pod podścieżką GitHub Pages), `noindex` i `robots.txt` są, biblioteka uPlot w repozytorium, stan filtrów jest w adresie (link do konkretnego widoku da się wysłać), konsola przeglądarki bez błędów, układ działa też na szerokości telefonu. Kohorty dzienne: wykres według dnia pierwszego zakupu z opcją „bez wygładzenia (dzień)”, z 13 zdarzeniami jako pionowe linie, macierz tygodniowa i miesięczna, krzywa powrotu A wobec B, 12 filtrów i obie reguły źródła. Lejek: pięć kroków dzień po dniu w ośmiu podziałach, z porównaniem 60 dni przed i po każdym zdarzeniu. To spełnia „co się wydarzyło, kiedy i jak zmieniło zachowanie” w takim stopniu, w jakim dane to pozwalają.

Czego nie sprawdziłem z bazy: dopasowania „kupujący TelemediGO a podobni pacjenci” (34,7% wobec 20,0%; surowe, bez dopasowania, dostałem 34,5% wobec 16,6%, więc kierunek i rząd wielkości się zgadzają), rozkładu struktura/zachowanie (4,6 i 2,0 punktu), liczebności prób w pozycji 12 (487–1 823), scenariuszy zwrotów A/B w pozycji 5 i scenariusza porannego 0–65 tys. zł. Wartości pozycji 7 i 10 to scenariusze z jawnymi założeniami, a nie pomiary; narzędzie tak je nazywa.

---

## 3. Ocena z perspektywy osoby, która zleciła zadanie

**Czy odpowiada na pytanie zadania?** Tak, wprost: „nie, bo z dwóch warunków spełniony jest jeden”, z liczbami po obu stronach, na danych oczyszczonych, z zastrzeżeniami. Wymagania punkt po punkcie:

1. Kohorty dzienne i zdarzenia z danych: są. Zdarzenia w retencji to „kandydaci” z podziału binarnego plus starty kampanii; narzędzie uczciwie mówi, które są potwierdzone, a które to kandydaci. Dwa zdarzenia mają realną wagę biznesową i zostały znalezione w danych, a nie podane: awaria Safari na iOS (17.03.2026) i spadek porannej przepustowości internistów (od 24.11.2025).
2. Lejek „gdzie i od kiedy”: jest, dzień po dniu, w podziałach, z datami. Z zastrzeżeniem 1.1 (jedna z dwóch „rzeczy do naprawienia” to nie strona).
3. Narzędzie, na którym da się prowadzić biznes: tak w sensie odczytu (kohorty, lejek, zdarzenia, wynik); nie ma w nim jeszcze alarmów ani odświeżania na nowych danych, ale to słusznie jest pozycją 2 listy.
4. Priorytety z wartością, pomiarem i czasem: 12 pozycji, każda ma trzy wymagane rzeczy, kwoty w marży, z obiema regułami i dwoma horyzontami, z zasadą „naprawić albo wyłączyć”.
5. Czego nie da się rozstrzygnąć: 18 pozycji z testami i odsyłaczami do priorytetów.

**Trzy najmocniejsze strony.**
- Dyscyplina liczb: każda liczba ma źródło w raporcie, dashboard odtworzony co do procenta, duplikaty i testy znalezione dwoma niezależnymi podpisami, awaria Safari wykryta metodą, a nie okiem. Moje niezależne przeliczenie 24 wartości nie znalazło ani jednej rozbieżności.
- Uczciwość wobec niepewności: dwie reguły źródła obok siebie, „niepewny: znak zależy od reguły”, scenariusz nazywany scenariuszem, rozkład opisowy nazywany opisem, a nie przyczyną.
- Narzędzie jako narzędzie: filtry, obie reguły, stan w adresie, odnośniki między zakładkami, zdarzenia na wykresach kohort i lejka.

**Trzy najsłabsze strony.**
- Gęstość tekstu. Zakładka „Czy to wzrost” ma w jednym akapicie po pięć liczb z dwóch reguł i trzech okien. Decydent chce najpierw pięciu zdań, potem dowodów. Przegląd priorytetów podaje przedziały typu „+18,6 do +48,0 (90 dni), +21,0 do +50,4 (180 dni)” bez jednej liczby bazowej, na którą ktoś się umówi.
- Rama lejka (1.1): jedno z dwóch głównych zdań o lejku przypisuje przeglądarce to, co jest cechą ruchu z reklam. Sprzeczność z własną wyceną (0 zł) rzuca się w oczy uważnemu czytelnikowi.
- Niewykorzystane dane: demografia (1.4) i konta bez zakupu (1.5). Oba cięcia są tanie i oba wzmacniają, a nie osłabiają wnioski.

**Czego brakuje wobec zadania.** Niczego, co zadanie wymienia wprost. Brakuje natomiast krótkiej, pierwszej warstwy dla czytającego pierwszy raz (jedna karta: pięć liczb, trzy decyzje) i jednej liczby bazowej przy każdej pozycji listy. Zdarzenia z danych są, ale w większości bez przyczyny („co się stało” wiemy, „dlaczego” zostaje w niewiadomych); to ograniczenie danych, nie pracy, i jest nazwane.

**Decyzja.** Gdybym oceniał kandydata: pozytywnie, zaprosiłbym dalej. Przesądza na plus to, że praca jest sprawdzalna i sprawdzona, że odpowiedź jest jednoznaczna, a niepewność nazwana, i że lista priorytetów zaczyna się od rzeczy pewnych, tanich i odwracalnych (awaria, pomiar, pauza), a dopiero potem od testów. Na minus: zbyt gęsty język wyników i jedna sprzeczność w ramie lejka. Oba minusy są do usunięcia w kilka godzin przed wysyłką; poprawki 1.1, 1.2, 1.7 zrobiłbym obowiązkowo, 1.3 i 1.4 jeśli jest czas, resztę w miarę możliwości.
