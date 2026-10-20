# Końcowa weryfikacja liczb — Codex, model Astra (punkt D), 2026-10-20

**Co sprawdzał:** liczby z odpowiedzi „czy to wzrost”, wartości pierwszych pozycji listy priorytetów, najważniejsze liczby TelemediGO, zgodność `notatki/c_szkic.md` z raportami i brzmienie wniosków. Polecenie: `d_astra_prompt.md`. Odpowiedź: `d_astra_odpowiedz.md`. Wywołanie: `codex exec -p astra -s read-only --skip-git-repo-check` (model `gpt-6-astra`, jedno wywołanie, za zgodą Kuby), baza otwarta z `read_only=True`.

**Werdykt Astry:** główne liczby potwierdzają odpowiedź „więcej pacjentów, ale gorsza retencja”. Błędu krytycznego nie ma. Przed wysłaniem trzeba było poprawić kilka zbyt stanowczych zdań i niespójności w wycenach.

**Liczby przeliczone niezależnie, wszystkie zgodne** (tabela w odpowiedzi, 45 pozycji):
- nowi pacjenci, powroty w 30/60/90 dniach z nowymi kampaniami i bez nich;
- marża na pacjenta, wynik biznesu i kwartały rok do roku;
- most od dashboardu do danych oczyszczonych;
- Safari na iOS (628,4–694,9 zamówienia, marża 64,6 i 74,3 zł);
- wizyty testowe, TikTok, `gs_generic_specjalisci`, cennik specjalistów;
- TelemediGO (zakupy według typu, zniżka 104,57 zł, marża wizyt u specjalistów, różnica powrotu +10,1 i +14,6 punktu).

## Uwagi i nasze decyzje (wszystkie przyjęte)

Ważne:
1. **„Większość spadku retencji to nowe kampanie” jest prawdziwe tylko według przyjętej reguły** (około 71%; według sesji płatności około 46%), a „w obrębie tej samej usługi spadku nie widać” dotyczy tylko L4. **Poprawione:** „odpowiada opisowo za około 46–71% spadku, zależnie od reguły”. Zdanie o usłudze zawężone do L4, a obok spadek po e-recepcie (33,4% → 29,9%) i u innych specjalistów (25,2% → 20,6%), policzony naszym kodem (`c_priorytety.txt`, W2).
2. **Safari a III kwartał:** „bez awarii kwartał byłby na poziomie roku wcześniej” to za dużo. **Poprawione** w szkicu, w znaleziskach i w syntezie konsylium: skala jest porównywalna ze spadkiem, ale wyniku kwartału bez awarii nie ustaliliśmy. 628–695 to scenariusz, nie przedział ufności.
3. **„Pewna strata” przy TikToku i „przyczyną jest cennik” przy kampanii na specjalistów** — za mocne. **Poprawione:** „w przyjętych scenariuszach wyłączenie poprawia wynik; odwracalna pauza”, wynik na pacjenta po 180 dniach z przedziałem warunkowym (−1,1 zł, od −5,3 do +3,0 zł), porównanie po pauzie z ustalonym punktem odniesienia; cennik to „jedno z głównych ograniczeń marży”.
4. **Tabela pomijała horyzont 180 dni przy rocznych wycenach kampanii.** **Poprawione:** TikTok +21,0–50,4 tys. zł (180 dni) obok +18,6–48,0 tys. zł (90 dni); Meta od −32,9 tys. zł (180 dni) obok −30,6 tys. zł; próg decyzji 85,4% (90 dni) i 84,5% (180 dni) (`c_priorytety.txt`, P11).
5. **31,4 tys. zł przy warunkach TelemediGO nazwane „sufitem”.** **Poprawione:** to scenariusz; zakres przy osobnej reakcji 10,9–35,2 tys. zł; „około połowa w pierwszym roku” opisana jako założenie planistyczne.
6. **„Newsletter i SMS to główny kanał powrotów” nie wynika z danych:** po wejściu z nich wraca 3,16% pacjentów spoza nowych kampanii wobec 18,84% bez takiego wejścia, czyli około 14% obserwowanych pierwszych powrotów; spadek wejść na 1 000 pacjentów liczony jest na całej narastającej bazie. **Poprawione** w pozycji 7 i w niewiadomej 9.
7. **Czas rekrutacji testu TelemediGO** (2–6 tygodni) był za krótki dla 1 823 pacjentów na grupę, a liczebność dotyczy powrotu, nie marży. **Poprawione:** 2–8 tygodni i przed startem ustalenie najmniejszej istotnej zmiany marży.

Drobne, wszystkie poprawione:
- Safari: zakładanie konta nie „przestaje działać”, tylko gwałtownie spada jego skuteczność (668 zamiast 1 082 kont w 60 dniach); TikTok ma za małą próbę;
- `gs_generic_specjalisci`: wynik bez pośredniego zaokrąglania marży (−23,2 zamiast −23,3 tys. zł);
- cennik: 70,8 tys. zł przy obecnych zniżkach TelemediGO obok 73,6 tys. zł;
- pediatra przy 25 zł: dochodowy pediatra, a psycholog zostaje na granicy zera;
- błąd w raporcie TelemediGO („osobno razem: 1 984 → 2 929” zamiast 225 → 461): poprawiony w kodzie;
- poranna obsada to „jedna z konkretnych hipotez poprawy retencji”, a nie „jedyna dźwignia”;
- niewiadoma 14: 51 775 zł to oba okresy łącznie (37 950 zł w okresie 2);
- niewiadoma 16: najstarsze kohorty okresu 2 mają już 270 dni obserwacji (5 137 pacjentów).

**Dopisane do odpowiedzi „czy to wzrost” (sugestia Astry):** liczba osób, które wróciły w 90 dniach, rośnie z 3 076 do 3 289 (+6,9%). Spada odsetek, a nie liczba powracających. Porównanie obejmuje pierwsze zakupy do 2 lipca każdego roku.

**Kierunek żadnego wniosku się nie zmienił.** Odpowiedź „nie jest to wzrost w rozumieniu Telemedi” zostaje. Zmiany dotyczą precyzji i pewności zdań.
