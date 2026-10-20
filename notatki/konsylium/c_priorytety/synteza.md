# Konsylium — lista priorytetów: wynik (2026-10-20)

Runda na briefie `brief.md` (zgoda Kuby 2026-10-20, z dopisanym kandydatem „pomiar” i faktem o marży w III kwartale). Odpowiedzi członków leżą w tym folderze. Liczby, które zespół kwestionował, sprawdziliśmy kodem: `analiza/c_priorytety.py`, sekcje P1, P11–P15 i W4.

## Puenta

Kolejność zespołu w dużej mierze zgadza się z naszą: na górze naprawa Safari na iOS i naprawa pomiaru. Dwie zmiany są dobrze uzasadnione:

- **Wstrzymanie TikToka na L4 i kampanii Google Ads na specjalistów wyżej.** Obie kampanie robić od razu, w pierwszym tygodniu. Obie tracą w obu regułach przypisania i w obu horyzontach, a wyłączenie jest darmowe i odwracalne.
- **Uczciwa obietnica L4 niżej i tylko w kampanii Meta.** Po wstrzymaniu TikToka zostaje tylko Meta, a wartość naprawy zależy od testu dodatkowości.

## Uzasadnienie

- **Safari na iOS** jest pewne, tanie i warte najwięcej. Sprawdziliśmy to: szacowana skala problemu w III kwartale 2026 (około 14–21 tys. zł marży) jest porównywalna ze spadkiem marży rok do roku (15,1 tys. zł). *(Korekta po weryfikacji Astrą: wyniku kwartału bez awarii nie ustaliliśmy; pierwotnie pisaliśmy, że bez awarii kwartał byłby na poziomie roku wcześniej.)*
- **Pomiar** jest warunkiem oceny wszystkich pozostałych pozycji. Najcenniejsze w nim nie są złotówki za wizyty testowe, tylko codzienny raport z marżą po koszcie pozyskania, zwrotami według kampanii, powrotem kohort i alarmami na krokach lejka według przeglądarki. Awaria Safari trwała 198 dni bez reakcji. Wykrycie po tygodniu ograniczyłoby stratę do 3,5%.
- **Pauza zamiast naprawy przy TikToku:**
  - wyłączenie zyskuje przy każdym udziale pacjentów dodatkowych;
  - najlepsza naprawa doprowadza wynik najwyżej do zera;
  - naprawa przy pełnym budżecie w najlepszym razie doprowadza wynik do zera;
  - naprawy (obietnica, ładowanie strony) da się sprawdzić na Meta, a TikTok może wrócić jako mały test.
- **Google Ads na specjalistów to problem cennika, a nie tylko kampanii.** Wizyta u specjalisty po cenie katalogowej zostawia 9–19 zł ponad koszt lekarza, a u pediatry i psychologa cena jest niższa niż koszt lekarza. Obniżka kosztu pozyskania o 40–60% to inny model kampanii, nie naprawa. Wstrzymać, a wrócić po zmianie cennika albo przy koszcie pozyskania nie wyższym niż marża pacjenta.
- **Test Meta ma z góry ustalony próg decyzji.** Według przyjętej reguły wyłączenie traci pieniądze tylko wtedy, gdy ponad około 85% pacjentów kampanii przyszłoby i bez niej (163,3 ÷ (163,3 + 27,8)). Test mówi więc tylko, czy jesteśmy powyżej, czy poniżej progu. Projekt:
  - województwa łączone w podobne pary, losowanie w parach;
  - wskaźnik główny to wszyscy nowi pacjenci i marża w województwie, a nie pacjenci przypisani Meta;
  - budżetu z wyłączonych województw nie przesuwamy.
  - W aktywnej połowie dzielimy ruch na starą i nową kreację: to mierzy naprawę obietnicy L4.
- **Na liście brakowało trzech rzeczy:**
  - komunikacji po wizycie z losową grupą kontrolną (retencja to połowa definicji wzrostu, a w trzonie biznesu spada);
  - przeglądu cennika specjalistów (wspólna przyczyna problemów z TelemediGO i z kampanią na specjalistów);
  - zasady budżetu: uwolnionych pieniędzy nie przesuwamy automatycznie do innych kampanii, bo kolejna złotówka zarabia zwykle mniej niż średnia.

## Rozwidlenie: poranna obsada internistów

Zespół widział ją niżej (miejsca 6–11). Powód: związek opóźnień z powrotami może wynikać z tego, kto przychodzi rano, a kwota 0–65 tys. zł jest scenariuszem. Twój argument też stoi: to jedyna dźwignia na retencję kanałów działających w obu latach, a pierwszy krok jest tani (dane o grafikach, 1–2 dni, plus rozmowa z osobami od grafików). **Rekomendacja:** zostawić wysoko, ale jako diagnozę. Decyzja o obsadzie zapada po diagnozie. Część wyjaśnień zespołu wykluczyliśmy w danych: długość porannej wizyty się nie zmieniła (8,5 minuty w obu okresach), a przy tym samym ruchu opóźnień jest o 26,4 punktu procentowego więcej.

## Ryzyka i co poprawiliśmy w wycenach

- **Kwoty „na rok” dla nowych kampanii obejmowały tylko dni działania.** TikTok działał w okresie 2 przez 234 dni, Meta przez 332. Przy tym samym tempie na pełny rok:
  - wstrzymanie TikToka: +18,6 do +48,0 tys. zł przy 100% pacjentów dodatkowych;
  - rozpiętość decyzji o Meta: od −30,6 do +179,6 tys. zł;
  - naprawa zwrotów L4 w samej Meta: 18,1–46,5 tys. zł według przyjętej reguły i 10,7–26,7 tys. zł według sesji płatności.
- **Safari to górna granica.** Część zablokowanych mogła kupić na innym urządzeniu. Przeliczenie z marca–września na rok pomija zimę, więc może być zaniżone. Marża jest liczona przed kosztem pozyskania, więc wydatków nie odejmujemy dwa razy (to sprawdziliśmy).
- **Górny wariant obietnicy L4** („wizyta zostaje opłacona”) może wymagać zmiany zasad zwrotów, a nie tylko treści reklamy. To decyzja z ryzykiem prawnym i wizerunkowym, osobna od samej reklamy. Odsetek 5,3% pochodzi z innej grupy pacjentów, więc pełne zrównanie jest optymistyczne.
- **Warunki TelemediGO u specjalistów:** w pierwszym roku efekt to mniej więcej połowa kwoty, bo obecni członkowie mają stare warunki do końca ważności. Zamiast usuwać zniżkę, można ją ustawić tak, żeby cena nie spadała poniżej kosztu lekarza.
- **Test TelemediGO z darmowym dostępem** mierzy wpływ zniżki, a nie opłacalność oferty za 89 zł. Wskaźnikiem głównym ma być marża na pacjenta. Do odnowień nie zachęcamy przed wynikiem.
- **Wizyty testowe są wszystkie u internisty** (2 071 przez dwa lata, 1 518 w okresie 2), więc stawka 25 zł jest właściwa. Jeśli lekarze już dostali te pieniądze, koszt przeszły jest utopiony. Oszczędność dotyczy tylko kolejnych miesięcy.

## Pewność

- **Wysoka** co do góry listy: Safari, pomiar, wstrzymanie dwóch kampanii ze stratą w obu regułach.
- **Średnia** co do środka listy: obietnica L4, poranna obsada, komunikacja po wizycie.
- **Niska** co do kolejności pozycji testowych między sobą. Mogą się zamienić po pierwszym tygodniu sprawdzeń.

Konsylium: 9 z 9 odpowiedziało, koszt 0,49 USD (około 2 zł). Kto co mówił — na życzenie.
