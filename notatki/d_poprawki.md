# D — poprawki po konsylium końcowej weryfikacji (zlecenie Kuby, 2026-10-21)

**Źródło:** synteza konsylium `notatki/konsylium/d_weryfikacja/synteza.md` (numery punktów niżej odnoszą się do jej listy „Lista poprawek od najważniejszej”). Pełne odpowiedzi członków są w tym samym folderze. Dwie z nich mają przeliczenia z bazy: `Opus_5_5.md` i `Fable_5_1.md`.

**Decyzja Kuby:** robimy całą listę z syntezy, z jego uwagami poniżej. Każda nowa liczba ma przejść przez nasz kod i kontrolę zgodności. Na koniec Codex jeszcze raz przelicza nowe liczby. Publikacji jeszcze nie robimy. Sesja zatrzymuje się u Kuby z gotowym pakietem.

## Lista Kuby (słowa Kuby, bez zmian)

1. Błędy na stronie: średnia ocena jako procent, złe etykiety przy zdarzeniach, koszt pozyskania przy wyniku po 180 dniach. Przy tym ostatnim sprawdzić, czy nie dotyczy wszystkich wierszy z kosztem, a nie jednego.
2. Zdania mocniejsze niż dane (punkty 3, 4, 10, 11, 14c i 16). Przy kilku mam wątpliwości:
   * opóźnienia: rozpisać po godzinach. Mam wrażenie, że to jeden poranny blok, a noc i południe łapią tylko jego brzegi;
   * przeglądarki w aplikacjach: sprawdzić, czy poza kampaniami Mety i TikToka płacą tak samo jak zwykłe. Jeśli nie, nie uogólniać;
   * TikTok: zanim obniżymy pewność, sprawdzić, z jakich kohort i z jakim kosztem pozyskania liczony jest wynik po 180 dniach. Jeśli to tylko wczesne kohorty, policzyć też cały rocznik;
   * pediatra i psychiatra: to małe grupy, więc raczej „bez istotnej zmiany” niż „rośnie”.
3. Zasady listy: dopisać, czym jest waga w kolejności. Najpierw pewne straty, które rosną każdego dnia i łatwo je naprawić, potem pauzy, które da się cofnąć, potem diagnozy i testy, na końcu rzeczy o nieznanym znaku. I że każda kwota to osobny scenariusz.
4. Test Mety: czy w 4–6 tygodni da się w ogóle odróżnić wynik od progu 85%? Jeśli nie, napisać to wprost i z góry ustalić, co robimy przy wyniku niejednoznacznym. Obok obecnego progu podać próg po naprawie zwrotów.
5. Kod rabatowy przy Mecie na L4: dajemy 20 zł zniżki ruchowi, który prawie nie wraca, a w „naprawić” tego nie ma. Dopisać wysokość kodu jako coś do przetestowania i jako niewiadomą.
6. „Czy to wzrost”:
   * na samej górze krótka karta dla kogoś, kto otwiera stronę pierwszy raz: odpowiedź, trzy liczby, trzy decyzje na pierwszy tydzień i jedna kwota;
   * przy retencji dodać liczbę kolejnych zamówień na pacjenta w 90 dniach;
   * dodać zdanie, że poza nowymi kampaniami marża na pacjenta prawie stoi.
7. Spadek marży w III kwartale: rozłożyć naszym kodem. Z liczb w syntezie po odjęciu TelemediGO zostaje jakieś 5 tys. zł luki, więc Safari się w niej nie mieści. Ta lukę trzeba wyjaśnić od nowa, a nie przepisywać zdanie z syntezy.
8. Kohorty: opcja dzienna w macierzy, bo dzienne kohorty to pierwsze wymaganie zadania. Przy krzywej powrotu zdanie, że późne punkty to inne, starsze kohorty.
9. Poranek: jak wygląda według godziny i czy opóźnienie jest od pierwszej wizyty dnia, czy narasta. Do „Po zakupie” i pozycji 6.
10. Krótko na stronie:
    * czy wiek, płeć i województwo zmieniają wniosek (zdanie i założenie);
    * konta bez żadnego zakupu jako niewiadoma;
    * tempo wydatków z ostatniego półrocza jednym zdaniem w zasadach listy;
    * sprawdzić, czy koszt kliknięcia w Google Ads rośnie, także na markę. Jeśli tak, dopisać jako rzecz do pilnowania.
11. README:
    * pięć linijek „co robimy w pierwszym tygodniu”;
    * krótko, jak używać narzędzia na co dzień;
    * przy 29% obie reguły;
    * „prawie się nie zmieniają”;
    * dopisać b2_eksport_c.py.
12. Drobne:
    * punkty 5, 6, 8 i 9;
    * nazwy okien przy Safari;
    * zdarzenia 8 i 10;
    * założenia 3 i 22;
    * sprawdzić, czy założenie 19 obejmuje okno 180 dni;
    * usunąć z CLAUDE.md adres e-mail osoby rekrutującej.

Każda nowa liczba przez nasz kod i kontrolę zgodności. Na koniec Codex niech jeszcze raz przeliczy nowe liczby. Publikacji jeszcze nie robimy. Zatrzymaj się u mnie z gotowym pakietem.

## Uwagi poprzedniej sesji prowadzącej do tej listy (pomoc, nie wnioski)

- **Punkty syntezy, do których odsyła Kuba:** 3 — trzy zdania sprzed poprawek Astry („większość spadku” w „Kohortach”, „nie działa zakładanie konta” w „Lejku” i w zdarzeniu 12); 4 — „opóźnienia rosną tylko u internisty rano”; 5 — dwie wartości „L4 z pozostałych kanałów”; 6 — −5,3 wobec ▼5,2 przy powrocie w 180 dniach (poprawna jest 5,2: 27,47% − 22,24%); 8 — liczebność przy średnich ocenach (469 i 3 446 ocen, nie 1 550 i 11 007 wizyt); 9 — daty „2026-10-21” w nagłówkach W4 i P1b `c_priorytety.txt` (to tekst w kodzie `analiza/c_priorytety.py`); 10 — przeglądarki w aplikacjach; 11 — pewność przy TikToku; 14c — wyceny jako osobne scenariusze; 16 — pozostałe uogólnienia (pediatra i psychiatra, odsetek kupujących TelemediGO, rozkład zmiany konwersji, założenie 22).
- **Punkt 7 Kuby:** z rozbicia w syntezie (do potwierdzenia) reszta biznesu traci 16,2 tys. zł, z czego 11,2 tys. zł to opłaty TelemediGO, więc zostaje około 5 tys. zł. Szacunek Safari (14–21 tys. zł) jest większy niż ta luka, więc zdanie „Safari mieści się w luce” jest błędne. Trzeba policzyć od nowa: pacjenci nowych kampanii a reszta, pierwsze zamówienia a powtórne, rocznik okresu 1 a okresu 2, koszt lekarza, opłaty TelemediGO, wydatki według kampanii.
- **Przeliczenia członków zespołu do potwierdzenia naszym kodem:** wiek pacjentów nowych kampanii (27,6 wobec 38,3 roku) i powrót według wieku (`Fable_5_1.md`, 1.4); konta bez zakupu (11 482 z 52 400; `Fable_5_1.md`, 1.5); opóźnienia według godziny poranka (`Opus_5_5.md`, 12); tempo wydatków z kwietnia–września 2026 (`Opus_5_5.md`, 5); próg Meta po naprawie zwrotów (około 70%; synteza 14).
- **Usterki strony zgłoszone przez sesję narzędzia przy zrzucie tekstów** (już w syntezie: 1, 3, 6): `local_0ea34a6a-6b84-45c6-87b7-e953f33e3452` czeka na zbiorczą listę i do tego czasu nic na stronie nie zmienia.
