# Przejrzystość narzędzia: przegląd zakładek oczami czytelnika

## Kontekst

To narzędzie jest rozwiązaniem zadania rekrutacyjnego na stanowisko Head of B2C w firmie telemedycznej (Telemedi). Pacjent płaci tam z własnej kieszeni za konsultacje online i za program zniżkowy TelemediGO. Zadanie dało dwa lata surowych danych (sesje na stronie, kroki lejka zakupowego, zamówienia, TelemediGO, wydatki na kampanie) i pytanie: czy to, co widać na dashboardzie (+52% nowych pacjentów, +61% zamówień rok do roku), jest wzrostem, rozumianym jako więcej pacjentów i lepsza retencja naraz.

Zadanie wymaga, w tej kolejności wagi:
1. analizy kohortowej w rozdzielczości dziennej, pociętej tak, żeby było widać, co się wydarzyło, kiedy i jak zmieniło zachowanie pacjentów i wynik (zdarzenia trzeba znaleźć w danych);
2. lejków od wejścia na stronę do płatności, w podziale, który pokazuje, gdzie i od kiedy tracimy pacjentów;
3. **działającego narzędzia, nie raportu** — takiego, na którym samemu prowadziłoby się ten biznes na co dzień;
4. listy priorytetów (wartość w złotych, sposób pomiaru, czas wdrożenia);
5. listy tego, czego z danych nie da się rozstrzygnąć.

Czytelnik to ktoś z Telemedi (osoba rekrutująca, przyszły przełożony), który otwiera link na laptopie (najczęściej 1366 albo 1920 pikseli szerokości), czasem na telefonie. Nie zna naszych notatek ani historii poprawek. Dane są syntetyczne.

Analiza jest skończona i liczby są sprawdzone. Autor narzędzia (Kuba) ocenił jednak, że **za mocno skupiliśmy się na liczbach, a za mało na przejrzystości i czytelności**. Przejrzał zakładkę „Kohorty” jako ktoś z Telemedi i napisał listę zmian (niżej, dosłownie). Ta lista jest już w realizacji. Teraz chce, żeby te same wnioski zastosować do pozostałych zakładek.

## Uwagi Kuby do zakładki „Kohorty” (dosłownie)

> Przejrzałem zakładkę „Kohorty” jak ktoś z Telemedi i układ jest do przebudowy. Zakładka nazywa się „Kohorty”, a pierwsze dwa ekrany to tabela zdarzeń z kwotami i priorytetami, więc kohort nie widać bez przewijania. Filtry wiszą osobno, choć sterują wykresem pod nimi. Wniosek o powrotach stoi w środku, między rzeczami zależnymi od filtrów, choć sam od nich nie zależy. Mapa kohort, czyli to, czego każdy tu szuka, jest prawie na dole. Tabela „Kohorty w podziale” jest nieczytelna. Proszę o zmiany w tej kolejności:
>
> 1. Tabela zdarzeń idzie do zakładki „Zdarzenia” jako jej pierwsza karta. Tam pasuje, bo połowa wierszy dotyczy lejka i sprzedaży (Safari, Google Ads na markę, newsletter). W „Czy to wzrost” i w „Kohortach” zostaje do niej odnośnik. Popraw wszystkie odnośniki, które dziś do niej prowadzą.
> 2. Nowa kolejność „Kohort”, od góry:
>    * wniosek z hantlami, krótko, szczegóły zwinięte (jedyna rzecz niezależna od ustawień, więc stoi nad nimi);
>    * jeden pasek „Pacjenci w analizie”: przypisanie źródła, zawężenia jako etykiety i przycisk „Przywróć domyślne”; widoczny przy przewijaniu, działa na wszystko pod spodem;
>    * mapa kohort (domyślnie miesięczna, przełącznik na tygodniową i dzienną), w kolumnie zdarzeń krótkie nazwy zamiast numerów;
>    * jedna karta „dzień po dniu”: w nagłówku wszystko, co nią steruje (miara, okno, wygładzenie, podział, porównanie); pod wykresem zdarzenia jako przyciski, które ustawiają porównanie 60 dni przed i po i jednym zdaniem mówią, co się zmieniło; w tej samej karcie tabela grup, bo dzieli z wykresem podział, porównanie i zaznaczone serie;
>    * krzywa powrotu na końcu, z okresami nazwanymi słowami.
>
>    Przy każdej karcie zależnej od ustawień jedna krótka linijka, od których.
> 3. Zdarzenia na wykresie kohort. Dziś pionowe linie to głównie zmiany wykryte w samych kohortach, czyli skutki. Przyczyny (start kampanii Meta i TikTok na L4, zwroty, poranne opóźnienia) są schowane pod „wszystkie obszary”. Domyślnie pokaż przyczyny. W liście „60 dni przed i po” zostaw tylko zdarzenia, które mogły zmienić kohorty: bez godziny bez danych i bez duplikatów w eksporcie.
> 4. Tabela grup od nowa:
>    * jedna miara naraz, ta sama co na wykresie; widok wszystkich okien jako opcja, wtedy w komórce tylko zmiana, a wartości po najechaniu;
>    * liczba pacjentów raz na wiersz, nie w każdej komórce;
>    * okresy słowami („rok wcześniej”, „ostatnie 12 miesięcy”), bez „A:” i „B”;
>    * zmiana z jednostką („−6,5 pkt proc.”, „−9 zł”);
>    * nagłówek pierwszej kolumny jako nazwa podziału, wiersz sumy „Wszyscy wybrani pacjenci”;
>    * mieści się bez przewijania w bok przy szerokości 1366 pikseli.
>
>    Kolor tylko wtedy, gdy różnica jest większa niż przypadek. […] prawie każda komórka jest czerwona albo zielona, przy grupach po 100–500 pacjentów i różnicach rzędu 1–3 punktów. […] Resztę pokaż szarym „bez wyraźnej zmiany”, a małe grupy oznacz. To samo w tabeli lejka.
> 5. „Przywróć domyślne” także w „Lejku”. Przycisk przywraca ustawienia startowe, czyści adres i jest aktywny tylko wtedy, gdy coś zmieniono.

## Zadanie dla Ciebie

Pracujesz niezależnie; nie widzisz odpowiedzi innych recenzentów.

1. **Wyciągnij z uwag Kuby ogólne zasady** (5–10, każda jednym zdaniem), które da się zastosować do każdej zakładki. Nazwij wzorzec błędu, a nie konkretny przypadek z „Kohort”.
2. **Przejrzyj siedem pozostałych zakładek** tymi zasadami: „Lejek”, „Po zakupie”, „Zdarzenia”, „Wynik biznesu”, „Jakość danych”, „Priorytety”, „Czego nie wiemy”. Pierwszej zakładki („Czy to wzrost”) **nie oceniaj** — Kuba pisze do niej uwagi osobno. „Kohorty” są przebudowywane według listy wyżej; dodaj do nich najwyżej 3 uwagi, których ta lista nie obejmuje, albo żadnej.
   Dla każdej zakładki:
   - czego czytelnik w niej szuka (jedno zdanie) i czy widzi to na pierwszym ekranie;
   - co dziś przeszkadza (konkretnie, z odwołaniem do zrzutu, np. `lejek_03`);
   - **proponowany układ od góry**: kolejność kart, co przenieść do innej zakładki, co połączyć, co zwinąć, co usunąć, co przemianować;
   - tabele: co poprawić (jednostki, okresy słowami, powtarzane liczebności, kolor bez istotności, szerokość, nagłówki);
   - sterowanie: czy filtry stoją przy tym, czym sterują, czy jest jasne, od których ustawień zależy karta, czy da się wrócić do ustawień domyślnych;
   - pracochłonność każdej zmiany: mała (do godziny), średnia (kilka godzin), duża.
3. **Sprawy wspólne dla wielu zakładek:** nawigacja między zakładkami, powtórzenia tej samej treści w kilku miejscach (gdzie co powinno mieszkać), nazewnictwo okresów i grup, legenda kolorów, odnośniki, telefon.
4. **Dziesięć zmian o największym zysku dla czytelnika** w stosunku do pracy, od najważniejszej, każda z jednym zdaniem „dlaczego”.
5. **Czego nie ruszać**, bo działa dobrze.

## Ramy

- Bez nowych analiz i bez zmiany liczb. Liczby na stronie pochodzą z eksportu i zostają. Chodzi o układ, kolejność, nazwy, tabele, sterowanie, zwijanie, przenoszenie treści i odnośniki. Wyjątek: jeśli kolor albo słowo sugeruje zmianę, której dane nie potwierdzają (jak w punkcie 4 Kuby), wskaż to.
- Strona jest statyczna (HTML, JavaScript, wykresy uPlot), otwierana z linku, bez konta. Propozycje muszą dać się zrobić w takim układzie.
- Zasada stała projektu: tekst na stronie nie używa pojęć znanych tylko z notatek; akapit zaczyna się od tego, co czytelnik ma wiedzieć (kwota, fakt, okres).
- Pisz po polsku, pełnymi zdaniami, konkretnie. Bez ogólników w rodzaju „poprawić czytelność” bez wskazania, co dokładnie. Około 2500–3500 słów łącznie.

## Materiał

- `z/` — zrzuty ekranu zakładek przy szerokości 1366 pikseli, ustawienia domyślne. Nazwa: `<zakładka>_<odcinek>.jpg`; każdy odcinek to jedno okno 1366 × 900 pikseli, kolejne odcinki to przewijanie w dół (z zakładką około 60 pikseli). Zakładki: `kohorty` (stan przed przebudową, dla odniesienia), `lejek`, `po-zakupie`, `zdarzenia`, `wynik`, `jakosc`, `priorytety`, `niewiadome`.
- `teksty_zakladek_2_9.md` — pełne teksty tych zakładek tak, jak widzi je czytelnik (sekcje rozwinięte, tabele w Markdown).
- `index.html` — szkielet strony (kolejność kart w każdej zakładce, filtry).
