# Recenzja Codeksa (model Sol) — szkic punktu C, 2026-10-20

**Co sprawdzał:** analizę TelemediGO (`analiza/c_telemedigo.py`) i liczby do odpowiedzi „czy to wzrost” oraz do listy priorytetów (`analiza/c_priorytety.py`). Polecenie: `c_codex_prompt.md`. Odpowiedź: `c_codex_odpowiedz.md`. Wywołanie: `codex exec -p review -s read-only --skip-git-repo-check`, tylko odczyt, baza otwarta z `read_only=True`.

**Werdykt Codeksa:** liczby główne się zgadzają, ale interpretacja samoselekcji, liczebność próby testu i przedstawienie wyniku „bez poprzedniego rocznika” wymagały korekt. Uwag krytycznych nie było.

## Liczby przeliczone niezależnie — wszystkie zgodne

| Miara | Nasz wynik | Codex |
|---|---|---|
| Zakupy TelemediGO (okres 1 / okres 2) | 1 759 / 2 468 | 1 759 / 2 468 |
| Przy kasie z pierwszym zamówieniem | 905 / 1 089 | 905 / 1 089 |
| Przy kasie z kolejnym zamówieniem | 629 / 918 | 629 / 918 |
| Osobno, z `crm_go_upsell` | 225 / 461 | 225 / 461 |
| Odsetek nowych pacjentów kupujących przy pierwszym zamówieniu | 5,58% / 4,41% | 5,576% / 4,411% |
| To samo bez nowych kampanii, okres 2 | 5,63% (17 419) | 5,632% (981 z 17 419) |
| Zniżka efektywna członkostw z okresu 1 | 183 939 zł, 104,57 zł na członkostwo | 183 939,20 zł, 104,570 zł |
| Marża wizyt ze zniżką u specjalistów poza internistą i psychiatrą | −7 845 / −14 682 zł | −7 844,80 / −14 681,60 zł |
| Wynik biznesu | 828 085 / 1 048 069 zł | 828 085,25 / 1 048 069,34 zł |
| Powrót w 90 dniach, wszyscy | 23,9% (12 867) / 17,4% (18 924) | 23,91% / 17,38% |
| Bez nowych kampanii, okres 2 | 22,0% (14 031) i 20,4% (15 414) | 21,99% i 20,41% |
| Rozbicie wzrostu przy kasie (1e) | +471 / −287 i +234 / +55 | +471,49 / −287,49 i +233,93 / +55,07 |
| Kontrola 1 (4b), różnice | 15,59 / 6,26 / 1,28 punktu | to samo |
| Kontrola 2 (4c) | 450 / 189, +0,398 | to samo |
| P1 (Safari na iOS) | 74 786–82 765 zł (90 dni), 86 043–95 222 zł (180 dni) | to samo |
| P7 (`gs_generic_specjalisci`) | cztery zestawy wartości | zgodne |

## Uwagi i nasze decyzje (wszystkie przyjęte)

1. **Ważna — liczebność próby testu (4d) zaniżona.** Wzór używał wspólnej wariancji. **Poprawione:** dwie proporcje z osobnymi wariancjami, zaokrąglenie w górę: 136, 487 i 1 823 pacjentów na grupę zamiast 105, 422 i 1 687. Projekt B opisany jako test bezpłatnego dostępu do zniżek przez 90 dni, który sam nie rozstrzyga opłacalności płatnego programu. W projekcie A dopisane losowanie przed zakupem i porównanie pierwszej płatności.
2. **Ważna — „+8,1%” to tylko odjęcie marży powtórnych konsultacji poprzedniego rocznika.** Rocznik z okresu 1 dał w okresie 2 jeszcze 41 474 zł opłat za TelemediGO. **Poprawione:** obok +8,1% stoi +3,1% po odjęciu obu pozycji; oba opisane jako rozbicie księgowe, a nie wynik biznesu startującego od zera.
3. **Ważna — grupa porównawcza w kontroli 2 (4c) obejmuje późniejszych kupujących** (15 ze 189). **Poprawione:** nazwa „bez zakupu przy wejściu i przez następne 30 dni”, wariant bez późniejszych kupujących (+0,486), opis jako statystyka opisowa przy założeniu równoległych trendów. Lepsze porównanie (dopasowanie przy wejściu według stażu i historii zamówień) zapisane jako możliwe uzupełnienie.
4. **Ważna — kontrola 1 (4b) nie rozdziela wpływu ceny od samoselekcji.** Wyłączenie odnawiających zależy od zachowania po zakupie. **Poprawione:** nazwa „wśród kupujących bez kolejnego zakupu członkostwa”, wariant ze wszystkimi kupującymi, wniosek „zgodny z kilkoma wyjaśnieniami, nie rozstrzyga między nimi”. W szkicu usunięte zdanie, że kontrola wskazuje bardziej na samoselekcję.
5. **Ważna — wartości zmiany warunków TelemediGO (P6) to scenariusze, nie granice.** Nieodebrane wizyty dają dziś 4 233,60 zł dodatniej marży. **Poprawione:** trzy scenariusze (14 682 zł — znikają wszystkie, 18 915 zł — znikają tylko te ze stratą, 31 405 zł — wszystkie zostają po cenie katalogowej) i zakres przy osobnej reakcji przy każdym zamówieniu: 10 896–35 191 zł.
6. **Ważna — porównanie opłat ze zniżkami wymaga jawnego założenia o tych samych wizytach.** **Poprawione:** zdanie z założeniem w raporcie (sekcja 2a) i w szkicu; kwota 27 388 zł nie jest nazywana stratą programu.
7. **Drobna — koszt testu (P10) nominalny, a nie dodatkowy.** Część wizyt ma już inne kody rabatowe. **Poprawione:** dodatkowy koszt 6,71 zł na pacjenta (nominalnie 6,76 zł); koszt testu 3 266 zł i 12 225 zł dla 487 i 1 823 pacjentów; pierwsze zamówienie „bez zniżki z członkostwa próbnego”.
8. **Drobna — sesje zalogowane od wejścia (P5) potrzebują założenia o odrębnych zamówieniach.** **Poprawione:** nazwa „scenariusze”, założenie dopisane, wariant na pacjentach (2 557 pacjentów: 35 547 zł), 90,5% opisane jako wysoki scenariusz, a nie górna granica.

Dodatkowo, zgodnie z sugestiami Codeksa: w P1 dopisane założenie, że skala problemu utrzymuje się przez rok, i że kwoty to marża rocznika, a nie wpływy w tym samym roku; w P7 odnośnik do założenia 42; w W1–W2 zdanie, że spadek obserwowanej retencji nie dowodzi gorszego zachowania identycznych pacjentów.

**Kierunek żadnego wniosku się nie zmienił.**
