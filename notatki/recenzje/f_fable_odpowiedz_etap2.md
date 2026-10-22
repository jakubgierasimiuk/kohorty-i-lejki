Etap 2 — recenzja całości (odpowiedź z etapu 1 bez zmian)

**Wniosek ogólny.** Rozwiązanie odpowiada na wszystkie pięć oczekiwań i trzy elementy oddania; jest kompletne, policzone i uczciwe co do niepewności. Ocenę obniżają trzy rzeczy: ślad pracy deklaruje ślepe uliczki, ale ich nie pokazuje; związek „zdarzenie → zachowanie kohort → wynik” trzeba składać z czterech zakładek; narzędzie jest analityczne, nie operacyjne.

## A. Zgodność z zadaniem

| Punkt | Gdzie | Ocena | Czego brakuje |
|---|---|---|---|
| 1. Analiza kohortowa | Zakładka Kohorty: wykres dzienny (okna 30/60/90/180 dni, marża na pacjenta, wygładzenie 1/7/28 dni), macierz miesiąc/tydzień/dzień z kolumną „Zdarzenia”, 12 filtrów, dwie reguły źródła, porównanie „60 dni przed i po” dla każdego z 14 zdarzeń | dobrze | Kosztu pozyskania nie ma w serii kohortowej (jest tylko w tabeli w Wyniku biznesu), więc „wynik” kohorty to marża przed kosztem. Macierz domyślnie miesięczna. |
| 2. Lejki | Zakładka Lejek: kroki z przejściami i etykietą „Najbardziej obniża płatności”, 8 podziałów, seria dzienna z liniami zdarzeń, tabela z liczebnościami, karta Safari z datą 17.03.2026 | dobrze | Jeden wymiar podziału naraz; kampania × przeglądarka tylko przez filtr „Pokaż dla”. |
| 3. Narzędzie, nie raport | 9 zakładek, statyczna strona z przeliczonymi danymi, filtry, wersja na telefon | dobrze / częściowo | Domyślne widoki to 12 miesięcy wobec roku wcześniej; brak widoku „ostatnie 7 dni” i alarmów (punkt D). Około 205 tys. znaków tekstu: czyta się jak raport. |
| 4. Lista priorytetów | Zakładka Priorytety: 12 pozycji, przegląd (wartość, pewność, wdrożenie), karty „Dlaczego / Co robimy / Po czym poznamy”, scenariusze naprawić/wyłączyć, lista „Nie robimy teraz” | dobrze | Pozycje 7, 11 i 12 nie mają wartości w sensie zadania (7: „23,6 tys. zł za punkt”, 12: tylko koszt testu). Wartości 3, 4 i 9 to zakresy zależne od reguły, czytelne dopiero po tabeli scenariuszy. |
| 5. Czego nie da się rozstrzygnąć | Zakładka Czego nie wiemy: 21 pozycji, każda z „dlaczego ważne”, testem albo danymi i odnośnikiem do priorytetu | dobrze | Dziewięć pozycji bez przypisanego priorytetu (np. 2, 10, 11, 14, 15) wisi bez decyzji, co z nimi. |
| Link do narzędzia | README: adres jest szablonem; w repozytorium jest `.github/workflows/pages.yml` | nie da się ocenić | Prawdziwy adres; otwarcie na cudzym telefonie. Dolnej części zakładki Priorytety na telefonie zrzuty nie obejmują. |
| Lista priorytetów (oddanie) | W narzędziu i w skrócie w README („pierwszy tydzień”) | dobrze | — |
| Ślad pracy | 88 commitów, `notatki/` (założenia, znaleziska, decyzje, plan, przekazanie), `notatki/recenzje/` (11 poleceń i odpowiedzi Codeksa), `notatki/konsylium/` (2 rundy, 8–9 modeli), `analiza/wyniki/` | częściowo | Ślepe uliczki i prompty do głównego narzędzia — punkt B. |

## B. Ślad pracy

Repozytorium pokazuje proces bogato, ale zbyt porządnie. Widać kolejność kroków, przeglądy i weryfikacje: tytuły commitów typu „przed przeglądem Kuby”, „recenzja Codeksa (Sol) uwzględniona”, „34 z 35 zgodnych”; polecenia i odpowiedzi drugiego modelu w `notatki/recenzje/`; dwie rundy konsylium z odpowiedziami każdego modelu i syntezą; raporty z kontroli bezpieczeństwa paczki. To więcej niż większość kandydatów pokaże.

Czego zabraknie osobie, która chce zobaczyć, jak kandydat pracował:
- **Ślepych uliczek.** README mówi, że zostały w historii, ale nie wskazuje żadnej. Z 88 tytułów commitów da się wyłuskać ledwie kilka poprawek: wycofanie zdania o „luce” (849e12c, 825c977), przeliczenie Safari według pierwszego wejścia (351f556), przenumerowanie założeń (26a2526). Historia czyta się jak linia prosta.
- **Promptów do głównego narzędzia.** W repozytorium są polecenia dla Codeksa i briefy konsylium, ale nie ma śladu rozmów z Claude Code, którym powstała analiza. Zadanie dopuszcza samo repozytorium, ale „jak pracujesz” widać wtedy tylko przez notatki, a te są duże (DECYZJE 48 KB, c_szkic 75 KB) i bez mapy, od czego zacząć.
- **Wskazania na `CLAUDE.md`** (17 KB) jako kontrakt pracy z AI: to najlepszy dowód metody, a README o nim milczy.

## C. Akcenty

**Rozbudowane ponad potrzebę.** Zakładka Po zakupie to sześć kart o punktualności, zwrotach i ocenach, z wykresami godzinowymi i przedziałami ruchu; to ważne znalezisko, ale jedna karta plus odnośnik wystarczyłyby. W Priorytetach tabele scenariuszy TikToka i Mety mają po 24 liczby (6 wierszy × 2 reguły × 2 okna). Dwie reguły przypisania stoją obok siebie w każdej zakładce, co podwaja liczby. Każda karta ma akapity, zastrzeżenie, szczegóły i źródła.

**Za słabo: związek zdarzenia z kohortami i wynikiem.** Jest, ale rozproszony. Najlepiej widać go w trzech miejscach: zdanie nad macierzą kohort („od listopada 2025 kohorty wracają rzadziej, od marca 2026 spadek się pogłębia”, wiersze z numerami zdarzeń), zdarzenia 3, 5, 10 i 12 na osi (marża w 30 dniach 56,0 → 46,8 zł w trzech krokach; udział nowych kampanii 0 → 41%; powrót w 30 dniach 9,7 → 6,9% dzień po starcie TikToka; krok konta 66 → 46%) oraz linie zdarzeń na wykresach dziennych. Brakuje jednak:
- jednej tabeli „zdarzenie → miara kohort przed i po → skutek w złotych”; dziś skutek w złotych jest tylko przy Safari (14,6–18,3 tys. zł w III kw.) i newsletterze (17,4 tys. zł), a dla opóźnień i zwrotów trzeba iść do Priorytetów;
- decyzji firmy na osi: skoki budżetów (17.11.2025, 8.12.2025, 2.01.2026, 19.01.2026, 23.02, 13.03, 6.04.2026) są wymienione w tekście zdarzeń 4 i 9, ale nie jako zdarzenia; podwojenie wydatków, najważniejsza „decyzja” w danych, nie ma własnego punktu;
- dla spadku powrotu poza nowymi kampaniami (24 → 22%) rozwiązanie uczciwie mówi „kandydat poniżej progu” i nie przesądza — to dobrze, ale czytelnik powinien zobaczyć to zdanie w pierwszej zakładce, a nie dopiero w zdarzeniu 11.

## D. Praca na co dzień

Prowadziłaby na tym przeglądy tygodniowe, nie dzień w dzień. Zatrzymałyby ją: (1) domyślna optyka „12 miesięcy wobec roku wcześniej” w każdej zakładce; opcje „ostatnie 90 dni” i „ostatnie 30 dni” są, ale nie ma „ostatnie 7 dni” ani żadnego ekranu „co się zmieniło od wczoraj”; (2) brak alarmów w narzędziu: metoda wykrywania zmian istnieje (245 wierszy surowego wyniku), ale jako statyczna tabela, a alarmy trafiły na listę priorytetów zamiast do narzędzia; (3) ekonomia kampanii bez serii czasowej — koszt pozyskania i wynik na pacjenta według kampanii są tylko za okres, nie tydzień po tygodniu, więc budżetem nie da się sterować z tego ekranu; (4) odświeżenie danych to ręczne uruchomienie łańcucha skryptów z `analiza/README.md`; (5) tekst spowalnia codzienny przegląd; na telefonie szerokie tabele są przycięte i wymagają przewijania (Kohorty, Lejek).

## E. Najwyżej trzy poprawki przed wysłaniem

1. **README: sekcja „Ślepe uliczki, poprawki, prompty”.** Sześć do dziesięciu konkretów z odnośnikami do commitów i notatek (wycofane zdanie o „luce”; przeliczenie Safari; 1 z 35 liczb zakwestionowana przez Codeksa w 1bfa75f; zarzuty konsylium sprawdzone kodem w dece47a–efdd8e2), plus wskazanie `CLAUDE.md` i `notatki/recenzje/` jako miejsca promptów. Zmienia ocenę, bo to literalne oczekiwanie z „Co oddajesz”, a dziś README je deklaruje bez dowodu. Praca: 1–2 godziny.
2. **Zdarzenia: tabela „zdarzenie → kohorty → wynik” na górze zakładki** (14 wierszy: data, co, miara kohort przed → po, skutek w złotych albo „nie policzono”) i dodanie skoków budżetu jako zdarzeń. Liczby już są na stronie, trzeba je zebrać. Zmienia ocenę, bo to „najważniejsza część zadania”, a dziś składa się ją z czterech zakładek. Praca: pół dnia do dnia, z kontrolą eksportu.
3. **Pierwsza zakładka, cztery zdania z etapu 1:** wyjaśnić „reguły przypisania” przy pierwszym użyciu (decyzja 2); zastrzeżenie o −7% w III kwartale postawić przy tabeli albo dodać do wykresu serię „marża po kosztach kampanii”; „z kanałów bezpłatnych przybyło 12%” → „o 12% więcej”; pogodzić „71% spadku to skład” z zastrzeżeniem (dotyczy reszty spadku). Zmienia dwuminutowe czytanie, od którego rekrutujący zaczyna. Praca: 2–3 godziny.

Poza listą, ale obowiązkowe: wpisać prawdziwy adres w README.

**Czego nie ruszać:** liczb i definicji (sprawdzone dwoma modelami i konsylium), dwóch reguł przypisania (atut; tylko raz je wyjaśnić), kolejności priorytetów i uzasadnienia 9. miejsca Mety, struktury 9 zakładek, zakładki „Czego nie wiemy”, stylu zastrzeżeń. Nie dodawać nowych analiz ani tekstu i nie przepisywać historii commitów.
