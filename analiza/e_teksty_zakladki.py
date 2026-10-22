"""E — karty tekstowe zakładek „Kohorty”, „Po zakupie”, „Zdarzenia”, „Wynik biznesu” i „Jakość danych” w nowym kształcie
(notatki/e_runda.md, punkt 3). Wywołuje go analiza/b_eksport.py po zbudowaniu danych zakładek. Wspólne narzędzia
(karty, słownik, numery niewiadomych, kontrola liczb): analiza/e_teksty.py.

Zasada liczb: żadnej liczby wpisanej ręcznie w zdaniach. Liczby przychodzą z danych zakładek (koh, pz, wy, jak, zdz, wz,
mostek), z raportów (V z b2_eksport_c.wartosci i odczyty Z) i z analiza/wyniki/e_merytoryka.json (E).

Odwołania do „Czego nie wiemy” piszemy w dawnej numeracji, a ET.popraw (słownik i nowe numery) przechodzi po każdej
karcie i każdym zdarzeniu dokładnie raz, na końcu.

Notatka z tekstami (notatki/e_teksty_zakladki.md) to szkic do przeglądu Kuby i wzorzec kontroli liczb. Odtwarza ją
z plików strony polecenie (po eksporcie):
    python -I analiza/e_teksty_zakladki.py
"""
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e_teksty as ET  # noqa: E402

B2 = ET.B2
liczba, proc, zn, tz, tzn, zl = ET.liczba, ET.proc, ET.zn, ET.tz, ET.tzn, ET.zl
karta, akapit, punkty, tabela, wiersz, zmiana, podtytul = ET.karta, ET.akapit, ET.punkty, ET.tabela, ET.wiersz, ET.zmiana, ET.podtytul

O1, O2 = B2.O1, B2.O2                      # (początek, koniec) roku wcześniej i ostatnich 12 miesięcy
O1_NAZWA, O2_NAZWA = B2.O1_NAZWA, B2.O2_NAZWA
MIESIACE_RZ = B2.MIESIACE_RZ
NOWE_NAZWY = {"meta_prosp_l4_szybko": "Meta na L4", "tt_prosp_l4_15min": "TikTok na L4", "gs_brand": "Google Ads na markę",
              "meta_rmkt_koszyk": "remarketing Meta"}

FORMY = {"pacjent": ("pacjent", "pacjentów", "pacjentów"), "wizyta": ("wizyta", "wizyty", "wizyt"),
         "zamowienie": ("zamówienie", "zamówienia", "zamówień"), "sesja": ("sesja", "sesje", "sesji"),
         "ocena": ("ocena", "oceny", "ocen"), "zakup": ("zakup", "zakupy", "zakupów"), "konto": ("konto", "konta", "kont"),
         "dzien": ("dzień", "dni", "dni"), "czlonkostwo": ("członkostwo", "członkostwa", "członkostw")}


def ile(n, rzecz):
    """Liczba z rzeczownikiem w poprawnej formie: 1 wizyta, 2 wizyty, 5 wizyt, 183,7 sesji."""
    f1, f2, f5 = FORMY[rzecz]
    if n != int(n):
        return f"{liczba(n, 1)} {f5}"
    n = int(n)
    forma = f1 if n == 1 else f2 if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14) else f5
    return f"{liczba(n)} {forma}"


DOPELNIACZ_1 = {"wizyta": "wizyty", "pacjent": "pacjenta", "ocena": "oceny", "zamowienie": "zamówienia", "sesja": "sesji",
                "zakup": "zakupu", "konto": "konta", "dzien": "dnia", "czlonkostwo": "członkostwa"}


def zile(n, rzecz):
    """Liczba z rzeczownikiem w dopełniaczu, po „z”: z 1 wizyty, z 1 363 wizyt, z 44 ocen."""
    n = int(round(n))
    return f"{liczba(n)} {DOPELNIACZ_1[rzecz] if n == 1 else FORMY[rzecz][2]}"


def pp(x, m=1):
    """Różnica w punktach procentowych, słownie."""
    w = round(abs(x), m)
    if m > 0 or w != int(w):
        slowo = "punktu procentowego"
    elif int(w) == 1:
        slowo = "punkt procentowy"
    elif int(w) % 10 in (2, 3, 4) and int(w) % 100 not in (12, 13, 14):
        slowo = "punkty procentowe"
    else:
        slowo = "punktów procentowych"
    return f"{liczba(abs(x), m)} {slowo}"


def pk(x, m=1):
    """Zmiana w punktach procentowych do komórki tabeli: „−6,5 pkt proc.”."""
    return f"{zn(x, m)} pkt proc."


def zlz(x, m=1):
    """Kwota na pacjenta ze znakiem: „+3,6 zł”, „−9,4 zł”."""
    return f"{zn(x, m)} zł"


def data(d):
    return f"{d.day}.{d:%m.%Y}"


def okresy(t):
    """Dawne nazwy okresów w przenoszonych zdaniach → słownik bez dat w nawiasie (ET.popraw dokończy resztę)."""
    for a, b in ((f"W okresie {O1_NAZWA}", "Rok wcześniej"), (f"w okresie {O1_NAZWA}", "rok wcześniej"),
                 (f"W okresie {O2_NAZWA}", "W ostatnich 12 miesiącach"), (f"w okresie {O2_NAZWA}", "w ostatnich 12 miesiącach"),
                 (f"okres {O2_NAZWA}", "ostatnie 12 miesięcy"), (f"okres {O1_NAZWA}", "rok wcześniej")):
        t = t.replace(a, b)
    return t


def zacz(lista, poczatek):
    return next(x for x in lista if x.startswith(poczatek))


def zdania(t):
    """Podział akapitu na zdania (po kropce i spacji przed wielką literą)."""
    return re.split(r"(?<=\.) (?=[A-ZĄĆĘŁŃÓŚŹŻ„])", t)


# ---------------------------------------------------------------- Kohorty

def karta_kohorty(koh, wz, V, E, Z):
    o90 = next(o for o in wz["retencja"]["okna"] if o["dni"] == 90)
    g1, g2 = dt.date.fromisoformat(o90["do1"]), dt.date.fromisoformat(o90["do2"])
    dok = B2.powroty_dokladne(koh)            # {okno: (powrót 1, powrót 2, pacjenci 1, pacjenci 2)} z danych kohort strony
    u1k, u2 = B2.udzial_nowych_w_spadku(Z)
    bez1, bez2, nz = V["pow_bez_z1k"], V["pow_bez_z2"], V["pow_nowe_z1k"]
    m90 = V["m90"]
    p180 = V["p180"]   # n1, n2, powrót 1, powrót 2, zmiana, marża 1, marża 2
    demo = zacz(koh["zdania"], "Wiek, płeć")
    wiersze = []
    for o in (30, 60, 90, 180):
        a, b, na, nb = dok[o]
        wiersze.append(wiersz(f"{o} dni", [{"tekst": proc(b), "pod": ile(nb, "pacjent")},
                                          {"tekst": proc(a), "pod": ile(na, "pacjent")},
                                          zmiana(pk(b - a), b - a)]))
    k = karta(
        "Nowi pacjenci wracają rzadziej niż rok wcześniej, w każdym oknie od 30 do 180 dni",
        wniosek=f"W ciągu 90 dni od pierwszego zakupu wraca {proc(o90['p2'], 0)} nowych pacjentów, a rok wcześniej "
                f"wracało {proc(o90['p1'], 0)}.",
        tresc=[
            akapit(f"Marża na pacjenta w 90 dniach, przed kosztem pozyskania, spadła z {liczba(m90[1], 0)} do "
                   f"{liczba(m90[2], 0)} zł."),
            akapit(f"Około {proc(u1k, 0)} spadku powrotu przypada na zmianę składu pacjentów. Pacjenci dwóch nowych kampanii "
                   f"na L4 (Meta i TikTok) wracają w 90 dniach tylko w {proc(nz['p90_o2'], 0)}, a jest ich coraz więcej."),
            akapit(f"Bez nich powrót też spada, z {proc(bez1['p90_o1'], 0)} do {proc(bez1['p90_o2'], 0)}. Wiek, płeć, "
                   f"wielkość miejscowości i województwo tego spadku nie tłumaczą."),
        ],
        zastrzezenie="Podział spadku opisuje skład pacjentów i nie wskazuje przyczyny: nie mówi, jak wracaliby pacjenci "
                     "nowych kampanii, gdyby przyszli innym kanałem.",
        szczegoly=[
            tabela(["Powrót w ciągu", "Ostatnie 12 miesięcy", "Rok wcześniej", "Zmiana"], wiersze,
                   tytul="Powrót nowych pacjentów: odsetek pacjentów, którzy złożyli kolejne zamówienie (nieanulowane)"),
            akapit(f"Powrót w 90 dniach w ostatnich 12 miesiącach: pacjenci nowych kampanii {proc(nz['p90_o2'])} z "
                   f"{zile(nz['n90_o2'], 'pacjent')}, pozostali {proc(bez1['p90_o2'])} z {zile(bez1['n90_o2'], 'pacjent')} "
                   f"(rok wcześniej {proc(bez1['p90_o1'])})."),
            akapit(f"Marża na pacjenta w 90 dniach: {liczba(m90[2], 1)} zł wobec {liczba(m90[1], 1)} zł rok wcześniej; w 180 "
                   f"dniach {liczba(p180[6], 1)} zł wobec {liczba(p180[5], 1)} zł."),
            akapit(f"Porównujemy te same dni kalendarzowe w obu latach i tylko kohorty z pełnym oknem. W oknie 90 dni to "
                   f"pierwsze zakupy od {data(O2[0])} do {data(g2)} i od {data(O1[0])} do {data(g1)}."),
            akapit("Podział spadku liczymy opisowo, czyli bez mierzenia wpływu: część przypisana nowym kampaniom to ich udział "
                   "w nowych pacjentach razy różnica powrotu między pozostałymi pacjentami a nimi, a reszta to spadek powrotu "
                   "pozostałych pacjentów."),
            akapit(f"Źródło pacjenta liczymy według pierwszego wejścia. Według sesji z płatnością bez nowych kampanii powrót "
                   f"spada do {proc(bez2['p90_o2'])} ({ile(bez2['n90_o2'], 'pacjent')}), marża na pacjenta w 90 dniach do "
                   f"{liczba(V['m90_bez_z2'], 1)} zł, a na nowe kampanie przypada około {proc(u2, 0)} spadku. Cała różnica "
                   f"między podziałami to jedna grupa: według sesji z płatnością do innych kanałów trafia "
                   f"{liczba(E['r_X_n'])} pacjentów nowych kampanii na L4 z tych kohort ({liczba(E['p_X_caly'])} w całych "
                   f"ostatnich 12 miesiącach). {liczba(E['r_X_wejscie_n'])} z nich weszło pierwszy raz z reklamy nowej "
                   f"kampanii, a zapłaciło w innej sesji, a {liczba(E['r_X_tylko_kod_n'])} weszło z innego kanału, ale "
                   f"zapłaciło z kodem nowej kampanii. Bez nich oba podziały dają ten sam powrót i tę samą marżę. Dlatego "
                   f"opis liczymy według pierwszego wejścia, a w filtrach można wybrać oba podziały."),
            akapit("Część spadku w kampaniach działających w obu latach może wiązać się z porannymi opóźnieniami u "
                   "internistów: po spóźnionej pierwszej wizycie pacjenci wracają rzadziej. Dane tego nie rozstrzygają "
                   "(Czego nie wiemy, punkt 4)."),
            akapit(okresy(demo).replace("pozostałych w obu okresach", "pozostałych w obu latach")),
        ],
        zrodlo="analiza/a5r_kohorty.py → analiza/wyniki/a5r_kohorty.txt; analiza/wyniki/a5r_struktura.txt; "
               "analiza/wyniki/c_priorytety.txt (W2); analiza/wyniki/e_merytoryka.txt (punkt 1); "
               "analiza/wyniki/d_retencja.txt (punkt 5); eksport analiza/b_eksport.py.")
    return ET.popraw(k), ["d:Wiek, płeć i województwo", "c:wzrost"]


# ---------------------------------------------------------------- Po zakupie

def _i2(pz):
    return (O2[0] - dt.date.fromisoformat(pz["start"])).days


def _suma(tab, o, i2):
    return sum(tab[:i2]) if o == 1 else sum(tab[i2:])


def karty_po_zakupie(pz, wz, V, E, Z):
    i2 = _i2(pz)
    start = dt.date.fromisoformat(pz["start"])
    D = V["D"]
    K = {}

    # --- punktualność (dzień terminu, wizyty odbyte)
    def grupa(spec, pora=None, bez_pory=None, nowa=None):
        n, p = [0] * pz["dni"], [0] * pz["dni"]
        for g in pz["punktualnosc"]:
            if g["spec"] != spec or (pora and g["pora"] != pora) or (bez_pory and g["pora"] == bez_pory) \
                    or (nowa is not None and g["nowa"] != nowa):
                continue
            for i, (a, b) in enumerate(zip(g.get("n", [0] * pz["dni"]), g.get("p15", [0] * pz["dni"]))):
                n[i] += a
                p[i] += b
        return n, p
    rn, rp = grupa("internista", pora="a_rano_6_11", nowa=False)
    r1, r2 = 100 * _suma(rp, 1, i2) / _suma(rn, 1, i2), 100 * _suma(rp, 2, i2) / _suma(rn, 2, i2)
    mies = {}
    for i, (a, b) in enumerate(zip(rn, rp)):
        m = f"{start + dt.timedelta(days=i):%Y-%m}"
        x = mies.setdefault(m, [0, 0])
        x[0] += a
        x[1] += b
    mp = {m: 100 * b / a for m, (a, b) in mies.items() if a}
    przed = [v for m, v in mp.items() if m <= "2025-10"]
    po = [v for m, v in mp.items() if "2026-02" <= m <= f"{O2[1]:%Y-%m}"]
    assert 45 <= min(po) and max(po) <= 55, "„około połowy” wymaga 45–55% od lutego 2026"
    assert all(mp[a] < mp[b] for a, b in (("2025-10", "2025-11"), ("2025-11", "2025-12"), ("2025-12", "2026-01"),
                                          ("2026-01", "2026-02")))
    inn, inp = grupa("internista", bez_pory="a_rano_6_11", nowa=False)
    pr = lambda k: D["op_pozostali_lekarze_wszyscy_rano_6_11_" + k]  # noqa: E731
    assert D["op_pozostali_lekarze_wszyscy_rano_6_11_ponad15_zmiana_od"] < 0 < D["op_pozostali_lekarze_wszyscy_rano_6_11_ponad15_zmiana_do"]
    assert round(pr("ponad15_proc_okres1")) == round(pr("ponad15_proc_okres2")), "„około tyle samo w obu latach”"
    # ta sama seria co w pozycji 6 listy priorytetów i w zdarzeniu na osi (a5r_punktualnosc.txt, 2b): jedna wersja liczb
    rs = V["rano"]["int_rano_ponad15_spoza_nowych"]
    assert all(round(mp[m], 1) == rs[m] for m in mp), "seria poranna z danych strony = a5r_punktualnosc.txt (2b)"
    K["punktualnosc"] = karta(
        "Od lutego 2026 około połowy porannych wizyt u internisty zaczyna się ponad 15 minut po terminie",
        wniosek=f"W ostatnich 12 miesiącach ponad 15 minut po terminie zaczęło się {proc(r2, 0)} porannych wizyt u "
                f"internisty, a rok wcześniej {proc(r1, 0)}.",
        tresc=[
            akapit(f"Do października 2025 było to {B2.zakres(min(przed), max(przed), 0, '%')} wizyt miesięcznie. Od listopada "
                   f"2025 odsetek rośnie z miesiąca na miesiąc, a od lutego 2026 stoi na poziomie "
                   f"{B2.zakres(min(po), max(po), 0, '%')}."),
            akapit(f"U pozostałych lekarzy rano bez istotnej zmiany: około {proc(pr('ponad15_proc_okres2'), 0)} w obu latach. "
                   f"U internisty w innych porach odsetek rośnie dużo mniej, głównie na brzegach porannego bloku (karta "
                   f"niżej)."),
        ],
        zastrzezenie="Przyczyny opóźnień w danych nie widać, bo nie mamy grafików ani identyfikatorów lekarzy (Czego nie "
                     "wiemy, punkt 4).",
        szczegoly=[
            akapit(f"Wizyty u internisty z terminem 6:00–11:59, pacjenci spoza nowych kampanii: "
                   f"{B2.zakres(min(przed), max(przed), 1, '%')} miesięcznie do X 2025, {proc(mp['2025-11'])} w XI 2025 "
                   f"({ile(mies['2025-11'][0], 'wizyta')}), {proc(mp['2025-12'])} w XII 2025, {proc(mp['2026-01'])} w I 2026 "
                   f"i {B2.zakres(min(po), max(po), 1, '%')} od II do IX 2026. W całym roku: {proc(r2)} z "
                   f"{zile(_suma(rn, 2, i2), 'wizyta')} wobec {proc(r1)} z {zile(_suma(rn, 1, i2), 'wizyta')} rok wcześniej."),
            akapit(f"U internisty w innych porach (pacjenci spoza nowych kampanii): "
                   f"{proc(100 * _suma(inp, 2, i2) / _suma(inn, 2, i2))} wizyt spóźnionych ponad 15 minut w ostatnich 12 "
                   f"miesiącach ({ile(_suma(inn, 2, i2), 'wizyta')}) wobec {proc(100 * _suma(inp, 1, i2) / _suma(inn, 1, i2))} "
                   f"rok wcześniej ({ile(_suma(inn, 1, i2), 'wizyta')})."),
            akapit(f"U pozostałych lekarzy rano (wszyscy pacjenci): {proc(pr('ponad15_proc_okres2'))} z "
                   f"{zile(pr('wizyty_okres2'), 'wizyta')} wobec {proc(pr('ponad15_proc_okres1'))} z "
                   f"{zile(pr('wizyty_okres1'), 'wizyta')} rok wcześniej; przedział różnicy obejmuje zero."),
            akapit("Długość wizyty i czas od zapłaty do terminu się nie zmieniają."),
            akapit("Opóźnienie to faktyczny start wizyty minus umówiony termin. Liczymy tylko wizyty odbyte, a dzień i porę "
                   "według terminu. Pacjenci nowych kampanii na L4 to pacjenci kampanii meta_prosp_l4_szybko i "
                   "tt_prosp_l4_15min według pierwszego wejścia; „spoza nowych kampanii” to wszyscy pozostali."),
        ],
        zrodlo="analiza/a5r_punktualnosc.py → analiza/wyniki/a5r_punktualnosc.txt; analiza/wyniki/d_retencja.txt "
               "(punkt 1); eksport analiza/b_eksport.py.")

    # --- godziny terminu (tabela pod kartą rysuje strona z pz["godziny"])
    op = lambda k: D["op_internista_wszyscy_" + k]  # noqa: E731
    h610 = range(6, 11)
    p2 = [op(f"godz{h:02d}_ponad15_proc_okres2") for h in h610]
    p1 = [op(f"godz{h:02d}_ponad15_proc_okres1") for h in h610]
    n2 = [op(f"godz{h:02d}_wizyty_okres2") for h in h610]
    para = lambda h: (f"{proc(op(f'godz{h:02d}_ponad15_proc_okres2'))} z {zile(op(f'godz{h:02d}_wizyty_okres2'), 'wizyta')}, "  # noqa: E731
                      f"rok wcześniej {proc(op(f'godz{h:02d}_ponad15_proc_okres1'))} z {liczba(op(f'godz{h:02d}_wizyty_okres1'))}")
    poza, pol, noc = "poza_5_13_czyli_0_4_i_14_23_", "poludnie_bez_12_czyli_13_15_", "noc_bez_5_czyli_0_4_"
    assert abs(op(poza + "ponad15_proc_okres2") - op(poza + "ponad15_proc_okres1")) < 0.5, "„poza blokiem tyle samo”"
    K["godziny"] = karta(
        "Opóźnienia u internisty skupiają się w jednym porannym bloku od 5:00 do 13:59",
        wniosek=f"Od 6:00 do 10:59 ponad 15 minut po terminie zaczyna się {B2.zakres(min(p2), max(p2), 0, '%')} wizyt u "
                f"internisty, a poza blokiem 5:00–13:59 prawie tyle samo co rok wcześniej.",
        tresc=[
            akapit("Najmocniej rośnie od 6:00 do 11:59. Wzrost w porach „południe” i „noc” z karty wyżej to głównie brzegi "
                   "bloku: godziny 12:00 i 5:00, a o 13:00 już niewiele."),
            akapit("U pozostałych lekarzy żadna godzina wyraźnie nie odstaje."),
        ],
        szczegoly=[
            punkty([f"o 5:00: {para(5)};",
                    f"od 6:00 do 10:59: od {proc(min(p2))} do {proc(max(p2))} ({B2.zakres(min(n2), max(n2))} wizyt w godzinie), "
                    f"rok wcześniej {B2.zakres(min(p1), max(p1), 1, '%')};",
                    f"o 11:00: {para(11)};", f"o 12:00: {para(12)};", f"o 13:00: {para(13)};",
                    f"poza 5:00–13:59: {proc(op(poza + 'ponad15_proc_okres2'))} z {zile(op(poza + 'wizyty_okres2'), 'wizyta')}, "
                    f"rok wcześniej {proc(op(poza + 'ponad15_proc_okres1'))} z {liczba(op(poza + 'wizyty_okres1'))}."]),
            akapit(f"Bez godziny 12:00 południe rośnie tylko z {proc(op(pol + 'ponad15_proc_okres1'))} do "
                   f"{proc(op(pol + 'ponad15_proc_okres2'))}, a noc bez 5:00 z {proc(op(noc + 'ponad15_proc_okres1'))} do "
                   f"{proc(op(noc + 'ponad15_proc_okres2'))}."),
            akapit("Wszyscy pacjenci; oba lata liczymy według dnia terminu wizyty."),
        ],
        zrodlo="analiza/d_retencja.py → analiza/wyniki/d_retencja.txt (punkt 1).")
    # nagłówki tabeli godzin w słowniku strony
    G = pz["godziny"]
    G["kolumny"] = [okresy(k) for k in G["kolumny"]]

    # --- ten sam poranny ruch (pz["ruch"]: przedział ruchu × okres)
    rt = {}
    for r in pz["ruch"]:
        rt.setdefault(r["przedzial"], {})[r["okres"]] = r
    wsp = {k: v for k, v in rt.items() if 1 in v and 2 in v}
    waga = {k: v[1]["odbyte"] + v[2]["odbyte"] for k, v in wsp.items()}
    rozn = 100 * sum((v[2]["spoznione"] / v[2]["odbyte"] - v[1]["spoznione"] / v[1]["odbyte"]) * waga[k]
                     for k, v in wsp.items()) / sum(waga.values())
    przyk = rt["17–20"]
    rz = zacz(pz["zdania_ruch"], f"W okresie {O1_NAZWA}")
    rp1, rp2 = D["ranek_pierwsza_okres_2_ponad15_proc"], D["ranek_kolejne_okres_2_ponad15_proc"]
    K["ruch"] = karta(
        "Przy tym samym porannym ruchu opóźnień jest dużo więcej niż rok wcześniej",
        wniosek=f"W dni z tą samą liczbą porannych wizyt u internisty spóźnionych jest średnio o {pp(rozn, 0)} więcej wizyt "
                f"niż rok wcześniej.",
        tresc=[
            akapit("Rok wcześniej opóźnienia nie zależały od ruchu. Dziś dni z większym ruchem w tym samym miesiącu też "
                   "prawie nie mają ich więcej."),
            akapit(f"Już pierwsza poranna wizyta dnia jest spóźniona prawie tak często jak kolejne: {proc(rp1, 0)} wobec "
                   f"{proc(rp2, 0)}. To bardziej pasuje do stałego przesunięcia od początku dnia (późniejszy start względem "
                   f"grafiku albo inna organizacja zapisów) niż do kolejki, która narasta w ciągu poranka."),
        ],
        zastrzezenie="To nasze odczytanie danych. Najwcześniejszy termin dnia liczymy dla całej sieci, bo w danych nie ma "
                     "identyfikatorów lekarzy ani grafików (Czego nie wiemy, punkt 4).",
        szczegoly=[
            akapit(f"Porównanie obejmuje {liczba(len(wsp))} przedziałów ruchu obecnych w obu latach "
                   f"({ile(sum(waga.values()), 'wizyta')}); różnica to {pp(rozn)}. Na przykład w dni z 17–20 porannymi "
                   f"wizytami spóźnionych było {proc(100 * przyk[1]['spoznione'] / przyk[1]['odbyte'])} wizyt rok wcześniej "
                   f"({ile(przyk[1]['dni'], 'dzien')}) i {proc(100 * przyk[2]['spoznione'] / przyk[2]['odbyte'])} w ostatnich "
                   f"12 miesiącach ({ile(przyk[2]['dni'], 'dzien')})."),
            akapit(okresy(rz)),
            akapit(f"Wizyty z najwcześniejszym porannym terminem dnia są spóźnione ponad 15 minut w {proc(rp1)} "
                   f"({ile(D['ranek_pierwsza_okres_2_wizyty'], 'wizyta')}), kolejne w {proc(rp2)} "
                   f"({ile(D['ranek_kolejne_okres_2_wizyty'], 'wizyta')}), średnio "
                   f"{liczba(D['ranek_pierwsza_okres_2_srednie_min'], 1)} wobec "
                   f"{liczba(D['ranek_kolejne_okres_2_srednie_min'], 1)} minuty (ostatnie 12 miesięcy). W tym samym miesiącu "
                   f"(II–IX 2026) godziny z 8 i więcej wizytami mają o "
                   f"{pp(D['ranek_ii_ix_2026_w_miesiacu_wysokie_minus_niskie_obciazenie_pkt'])} więcej spóźnionych niż "
                   f"godziny z 1–3 wizytami."),
            akapit("Ruch poranny w dniu to wszystkie nieanulowane wizyty u internisty z terminem 6:00–11:59 tego dnia. Dni "
                   "grupujemy według tego ruchu i w każdej grupie porównujemy odsetek porannych wizyt spóźnionych ponad 15 "
                   "minut w obu latach."),
        ],
        zrodlo="analiza/a5r_punktualnosc.py → analiza/wyniki/a5r_punktualnosc.txt (sekcje 3f–3g); "
               "analiza/wyniki/d_retencja.txt (punkt 2); eksport analiza/b_eksport.py.")

    # --- powrót według opóźnienia pierwszej wizyty (tabelę pod kartą liczy strona z danych kohort)
    rx = r"^\s+a_rano_ {k}\s+{{N}}\s+{{N}}\s+{{N}}\s+{{N}}\s+{{N}}\s+{{N}}\s+{{N}}"
    pw = {k: Z.r("a5r_punktualnosc.txt", rx.format(k=k), od="1f.")
          for k in ("a_do_5_min", "b_5_15_min", "c_15_30_min", "d_ponad_30_min", "brak_wizyty")}   # n1, n2, u1, u2, p1, p2, zm.
    kol = [pw[k][5] for k in ("a_do_5_min", "b_5_15_min", "c_15_30_min", "d_ponad_30_min")]
    assert all(a > b for a, b in zip(kol, kol[1:])), "powrót ma spadać z każdym przedziałem opóźnienia"
    ok90 = next(o for o in wz["retencja"]["okna"] if o["dni"] == 90)
    g1, g2 = dt.date.fromisoformat(ok90["do1"]), dt.date.fromisoformat(ok90["do2"])
    K["powrot"] = karta(
        "Po spóźnionej pierwszej wizycie pacjenci wracają rzadziej",
        wniosek=f"W ostatnich 12 miesiącach po porannej wizycie u internisty zaczętej ponad 30 minut po terminie wraca w 90 "
                f"dniach {proc(pw['d_ponad_30_min'][5], 0)} pacjentów, a po wizycie punktualnej {proc(pw['a_do_5_min'][5], 0)}.",
        tresc=[akapit("Powrót spada z każdym przedziałem opóźnienia. Spóźnionych pierwszych wizyt rano jest dziś dużo więcej "
                      "niż rok wcześniej (karty wyżej)."),
               akapit("Tabela pokazuje też rok wcześniej, ale wtedy spóźnionych pierwszych wizyt rano było mało, więc tych "
                      "porównań nie oceniamy.")],
        zastrzezenie="To porównanie obserwacyjne: pacjenci spóźnionych wizyt mogą różnić się od pozostałych także czymś, "
                     "czego w danych nie widać.",
        szczegoly=[
            punkty([f"do 5 minut po terminie: {proc(pw['a_do_5_min'][5])} z {zile(pw['a_do_5_min'][1], 'pacjent')};",
                    f"ponad 5 do 15 minut: {proc(pw['b_5_15_min'][5])} z {zile(pw['b_5_15_min'][1], 'pacjent')};",
                    f"ponad 15 do 30 minut: {proc(pw['c_15_30_min'][5])} z {zile(pw['c_15_30_min'][1], 'pacjent')};",
                    f"ponad 30 minut: {proc(pw['d_ponad_30_min'][5])} z {zile(pw['d_ponad_30_min'][1], 'pacjent')};",
                    f"brak wizyty (anulowana albo nieodebrana): {proc(pw['brak_wizyty'][5])} z "
                    f"{zile(pw['brak_wizyty'][1], 'pacjent')}."]),
            akapit(f"Wniosek opieramy na ostatnich 12 miesiącach. Rok wcześniej pacjentów ze spóźnioną pierwszą wizytą rano "
                   f"było {liczba(pw['c_15_30_min'][0])} przy 15–30 minutach i {liczba(pw['d_ponad_30_min'][0])} powyżej 30 "
                   f"minut."),
            akapit(f"Pierwsza wizyta u internisty z terminem 6:00–11:59, pacjenci spoza nowych kampanii według przyjętej "
                   f"reguły źródła. Powrót w 90 dniach na tych samych dniach kalendarzowych, tylko kohorty z pełnym oknem: "
                   f"od {data(O2[0])} do {data(g2)} i rok wcześniej od {data(O1[0])} do {data(g1)}."),
        ],
        zrodlo="analiza/a5r_punktualnosc.py → analiza/wyniki/a5r_punktualnosc.txt (1f); tabela pod kartą z danych kohort "
               "strony.")

    # --- zwroty (dzień płatności)
    def zw_suma(cel=None, nowa=None, o=2, kol="zwrocone"):
        s = 0
        for g in pz["zwroty"]:
            if (cel and g["cel"] != cel) or (nowa is not None and g["nowa"] != nowa):
                continue
            s += _suma(g.get(kol, [0]), o, i2) if kol in g else 0
        return s
    l4n = (zw_suma("l4", True, 2), zw_suma("l4", True, 2, "odbyte"))
    l4s = (zw_suma("l4", False, 2), zw_suma("l4", False, 2, "odbyte"))
    l41 = (zw_suma("l4", None, 1), zw_suma("l4", None, 1, "odbyte"))
    nowe2 = (zw_suma(None, True, 2), zw_suma(None, True, 2, "zw_zl"), zw_suma(None, True, 2, "kl_zw"))
    # te same zbiory policzone niezależnie na bazie (analiza/e_poprawki.py, punkt 2) i w pozycji 5 (a5e_scenariusze.txt)
    assert (nowe2[0], l4n[0], l4n[1]) == (E["zw_nowe_wszystkie"], E["zw_nowe_l4"], E["zw_nowe_l4_odbyte"])
    assert l4n[0] == V["e2a"][1] and l4n[1] == V["e2a"][0]
    K["zwroty"] = karta(
        "Zwroty po wizycie skupiają się w L4 z nowych kampanii",
        wniosek=f"W ostatnich 12 miesiącach zwrot po odbytej wizycie dostaje {proc(100 * l4n[0] / l4n[1], 0)} wizyt L4 "
                f"pacjentów nowych kampanii, a u pozostałych pacjentów {proc(100 * l4s[0] / l4s[1], 0)}.",
        tresc=[
            akapit(f"Rok wcześniej, bez nowych kampanii, zwrot dostawało {proc(100 * l41[0] / l41[1], 0)} wizyt L4, więc u "
                   f"pozostałych pacjentów odsetek nie wzrósł."),
            akapit(f"Lekarz dostaje wynagrodzenie także za wizytę, za którą zwracamy pieniądze. U pacjentów nowych kampanii "
                   f"to w ostatnich 12 miesiącach {tz(nowe2[1], 0)} zwróconych zapłat i {tz(nowe2[2], 0)} kosztu lekarza."),
        ],
        zastrzezenie="Powodu zwrotu w danych nie ma. To, że lekarz nie wystawia L4, którego pacjent oczekuje po obietnicy "
                     "reklamy, jest hipotezą (Czego nie wiemy, punkt 3).",
        szczegoly=[
            akapit(f"Ostatnie 12 miesięcy: {proc(100 * l4n[0] / l4n[1])} z {zile(l4n[1], 'wizyta')} L4 pacjentów nowych "
                   f"kampanii i {proc(100 * l4s[0] / l4s[1])} z {zile(l4s[1], 'wizyta')} L4 pozostałych pacjentów. Rok "
                   f"wcześniej: {proc(100 * l41[0] / l41[1])} z {zile(l41[1], 'wizyta')} L4."),
            akapit(f"Zwroty po wizycie u pacjentów nowych kampanii w ostatnich 12 miesiącach: {ile(nowe2[0], 'wizyta')} we "
                   f"wszystkich celach wizyty, z tego {liczba(l4n[0])} przy wizytach L4 (te liczy pozycja 5 listy "
                   f"priorytetów), {zl(nowe2[1])} zwróconych zapłat i {zl(nowe2[2])} kosztu lekarza."),
            akapit("Odsetek zwrotów liczymy wśród odbytych wizyt, według dnia płatności."),
        ],
        zrodlo="analiza/a5r_po_zakupie.py → analiza/wyniki/a5r_po_zakupie.txt (2b); eksport analiza/b_eksport.py.")

    # --- oceny (internista, pacjenci spoza nowych kampanii)
    oc = {}
    for r in pz["oceny"]:
        if r["spec"] == "internista" and not r["nowa"]:
            x = oc.setdefault((r["koszyk"], r["okres"]), [0, 0, 0, 0])
            for i, k in enumerate(("odbyte", "ocenione", "suma", "niskie")):
                x[i] += r[k]
    sr = lambda k, o: oc[(k, o)][2] / oc[(k, o)][1]  # noqa: E731
    nis = lambda k, o: 100 * oc[(k, o)][3] / oc[(k, o)][1]  # noqa: E731
    wsz2 = [0, 0]
    for r in pz["oceny"]:
        if r["okres"] == 2:
            wsz2[0] += r["odbyte"]
            wsz2[1] += r["ocenione"]
    oc_proc = 100 * wsz2[1] / wsz2[0]
    K["oceny"] = karta(
        "Wizyty spóźnione ponad 30 minut dostają dużo gorsze oceny",
        wniosek=f"W ostatnich 12 miesiącach wizyta u internisty zaczęta ponad 30 minut po terminie dostaje średnio "
                f"{liczba(sr('d_ponad_30_min', 2), 2)}, a wizyta punktualna {liczba(sr('a_do_5_min', 2), 2)} (skala 1–5).",
        tresc=[akapit(f"Po takim opóźnieniu {proc(nis('d_ponad_30_min', 2), 0)} ocen to 1 albo 2, a po wizycie punktualnej "
                      f"{proc(nis('a_do_5_min', 2), 0)}.")],
        zastrzezenie=f"Ocenę dostaje tylko {proc(oc_proc, 0)} odbytych wizyt, więc oceny pokazują tylko kierunek.",
        szczegoly=[
            akapit(f"Internista, pacjenci spoza nowych kampanii, ostatnie 12 miesięcy: przy opóźnieniu ponad 30 minut średnia "
                   f"{liczba(sr('d_ponad_30_min', 2), 2)} z {zile(oc[('d_ponad_30_min', 2)][1], 'ocena')}, przy wizycie "
                   f"zaczętej do 5 minut po terminie {liczba(sr('a_do_5_min', 2), 2)} z {zile(oc[('a_do_5_min', 2)][1], 'ocena')}. "
                   f"Ocenę dostało {liczba(wsz2[1])} z {zile(wsz2[0], 'wizyta')} odbytych w ostatnich 12 miesiącach "
                   f"(wszyscy lekarze i pacjenci)."),
            akapit(f"Rok wcześniej średnia przy opóźnieniu ponad 30 minut była podobna ({liczba(sr('d_ponad_30_min', 1), 2)}), "
                   f"ale z {zile(oc[('d_ponad_30_min', 1)][1], 'ocena')}, więc porównania z rokiem wcześniej nie "
                   f"interpretujemy."),
        ],
        zrodlo="analiza/a5r_po_zakupie.py → analiza/wyniki/a5r_po_zakupie.txt (3a); eksport analiza/b_eksport.py.")
    dawne = {"punktualnosc": [], "godziny": ["d:Opóźnienia po godzinach"], "ruch": ["d:Opóźnienia po godzinach"],
             "powrot": [], "zwroty": [], "oceny": []}
    return {k: ET.popraw(v) for k, v in K.items()}, dawne


# ---------------------------------------------------------------- Wynik biznesu

def karta_wynik(wy, V, E, Z):
    D = V["D"]
    kw = E["kwartaly"]
    q3 = kw[-1]
    go = V["q3_go_osobno"]
    pw = V["q3_powtorne"]
    rok = int(q3["kw"][:4])
    nazwa_kw = lambda s: f"{MIESIACE_RZ[(int(s[5:7]) - 1) // 3]} kw. {s[:4]}"  # noqa: E731
    # wydatki w procentach, tak jak marża (trzecia lista Kuby, punkt 2); ta sama komórka co w „Czy to wzrost”
    wiersze = [wiersz(nazwa_kw(k["kw"]), [zmiana(f"{zn(k['przed_rr_dokl'])}%", k["przed_rr_dokl"]),
                                          ET.zmiana_wydatkow(k),
                                          zmiana(f"{zn(k['marza_rr_dokl'])}%", k["marza_rr_dokl"])]) for k in kw]
    baza_bez_osobno = 100 * ((E["baza_2026"] - E["baza_2026_osobno_zl"]) / (E["baza_2025"] - E["baza_2025_osobno_zl"]) - 1)
    pac = V["q3_baza_pac"]
    raz = pac["2026-Q3"] / pac["2025-Q3"]
    assert 2.5 <= raz < 3, "„prawie trzy razy więcej pacjentów” wymaga ilorazu od 2,5 do 3"
    luka = -D["q3_reszta_z1k_luka_bez_telemedigo"]
    prow = D["q3_reszta_z1k_prowizja_wklad"]
    udz_mix = 100 * E["pw_mix"] / E["pw_zmiana"]
    spec_go = Z.r("e_merytoryka.txt", r"2026-07-01\s+inni/go\s+{N}\s+{N}", od="3. MARŻA NA POWTÓRNE")[1]
    assert spec_go < 0
    safari = zacz(wy["zdania"], "Awaria zakładania konta w Safari")
    przychody = zacz(wy["zdania"], "Przychód z konsultacji po zwrotach")
    jak_liczymy = zacz(wy["zdania"], "Koszt lekarza liczymy")
    assert E["rok_wyd_zmiana_proc"] > E["rok_przed_zmiana_proc"] > E["rok_marza_zmiana_proc"] > 0 and q3["wydatki_razy"] > 2
    assert all(a["przed_rr_dokl"] > b["przed_rr_dokl"] and a["wydatki_razy"] < b["wydatki_razy"] for a, b in zip(kw, kw[1:]))
    k = karta(
        "Za cały rok marża rośnie, ale wydatki na kampanie rosną szybciej niż marża zarabiana przed ich kosztem",
        wniosek=f"W ostatnich 12 miesiącach marża przed kosztem kampanii wzrosła o {proc(E['rok_przed_zmiana_proc'], 0)}, a "
                f"wydatki na kampanie o {proc(E['rok_wyd_zmiana_proc'], 0)}.",
        tresc=[
            akapit(f"Po koszcie lekarza, kampaniach i prowizji marża i tak wzrosła o {proc(E['rok_marza_zmiana_proc'], 0)}."),
            akapit(f"Rok do roku marża przed kosztem kampanii rośnie z każdym kwartałem wolniej, a wydatki szybciej. W III "
                   f"kwartale {rok} wydatki na kampanie były ponad dwa razy wyższe niż rok wcześniej."),
            akapit(f"Powtórne zamówienie zostawia mniej marży niż rok wcześniej, bo rośnie udział wizyt ze zniżką TelemediGO: "
                   f"z {proc(E['pw_go_udzial_25'], 0)} do {proc(E['pw_go_udzial_26'], 0)} powtórnych zamówień. To spina się z "
                   f"bilansem programu: opłata za TelemediGO nie pokrywa zniżek, które dostają jego członkowie (zakładka „Czy "
                   f"to wzrost”)."),
        ],
        zastrzezenie=f"Spadek marży w III kwartale {rok}, o {proc(abs(E['q3_zmiana_proc']), 0)} rok do roku, zależy od "
                     f"jednorazowego zdarzenia: we wrześniu {rok - 1} ruszyła sprzedaż TelemediGO w newsletterze. Po odjęciu "
                     f"jednorazowej nadwyżki tego startu marża kwartału jest o {proc(E['q3_w1_zmiana_proc'], 0)} wyższa niż "
                     f"rok wcześniej.",
        szczegoly=[
            tabela(["Kwartał", "Marża przed kosztem kampanii", "Wydatki na kampanie",
                    "Marża po kosztach kampanii"], wiersze, tytul="Kwartały rok do roku"),
            akapit(f"Za cały rok: marża przed kosztem kampanii {tz(E['rok_przed_1'], 0)} → {tz(E['rok_przed_2'], 0)} "
                   f"({zn(E['rok_przed_zmiana_proc'])}%), wydatki na kampanie {tz(E['rok_wyd_1'], 0)} → "
                   f"{tz(E['rok_wyd_2'], 0)} ({zn(E['rok_wyd_zmiana_proc'])}%), marża po koszcie lekarza, kampaniach i prowizji "
                   f"{tz(E['rok_marza_1'], 0)} → {tz(E['rok_marza_2'], 0)} ({zn(E['rok_marza_zmiana_proc'])}%). Marża przed "
                   f"kosztem kampanii to przychód z konsultacji po zwrotach i z TelemediGO minus koszt lekarza."),
            podtytul(f"III kwartał {rok} bez jednorazowego startu sprzedaży TelemediGO"),
            akapit(f"Sprzedaż TelemediGO w newsletterze ruszyła {V['go_start_data']}. W pierwszych "
                   f"{liczba(E['newsletter_dni_startu'])} dniach sprzedała {ile(E['q3_osobno_25'], 'czlonkostwo')}, a przy "
                   f"późniejszym tempie ({liczba(E['newsletter_tempo_dzienne'], 2)} dziennie) sprzedałaby około "
                   f"{liczba(E['newsletter_norma_startu'])}. Jednorazowa nadwyżka to {ile(round(E['newsletter_nadwyzka']), 'zakup')}, "
                   f"czyli {tz(E['newsletter_nadwyzka_zl'])}. Bez niej marża III kwartału {rok} jest o "
                   f"{proc(E['q3_w1_zmiana_proc'])} wyższa niż rok wcześniej, a bez całej sprzedaży w newsletterze w obu "
                   f"latach o {proc(abs(E['q3_w2_zmiana_proc']))} niższa. Marża przed kosztem kampanii rośnie wtedy o "
                   f"{proc(E['q3_przed_bez_nadwyzki_zmiana_proc'])} (bez tej korekty o {proc(E['q3_przed_zmiana_proc'])})."),
            akapit(f"Cały spadek III kwartału {rok} przypada na wrzesień ({tz(D['q3_miesiac_09_zmiana_marzy'])}); lipiec "
                   f"{tzn(D['q3_miesiac_07_zmiana_marzy'])}, sierpień {tzn(D['q3_miesiac_08_zmiana_marzy'])}."),
            podtytul(f"Marża na powtórne zamówienie w III kwartale {rok}"),
            akapit(f"Pacjenci spoza nowych kampanii złożyli więcej powtórnych zamówień ({liczba(pw[1])} wobec "
                   f"{liczba(pw[0])}), ale każde zostawia mniej marży ({liczba(pw[3], 2)} zł wobec {liczba(pw[2], 2)} zł). "
                   f"Spadek o {liczba(abs(E['pw_zmiana']), 2)} zł to w {proc(udz_mix, 0)} zmiana udziału rodzajów zniżki, a w "
                   f"obrębie tego samego rodzaju zniżki marża prawie stoi ({zn(E['pw_wewnatrz'], 2)} zł). Udział wizyt ze "
                   f"zniżką TelemediGO rośnie z {proc(E['pw_go_udzial_25'])} do {proc(E['pw_go_udzial_26'])}. Wizyta ze "
                   f"zniżką zostawia {liczba(E['pw_go_m26'], 2)} zł marży, bez zniżki {liczba(E['pw_none_m26'], 2)} zł, a u "
                   f"specjalistów wizyta ze zniżką TelemediGO ma marżę ujemną "
                   f"({liczba(spec_go, 2)} zł)."),
            podtytul(f"Rozkład księgowy spadku III kwartału {rok}"),
            akapit("Rozkład księgowy dzieli różnicę marży między kwartałami na składniki. Pokazuje, gdzie w rachunku jest "
                   "różnica; jej przyczyny nie wskazuje."),
            akapit(f"Marża spadła o {tz(-D['q3_zmiana_marzy'])}. Według przyjętej reguły źródła pacjenci nowych kampanii "
                   f"zostawili {tz(D['q3_nowe_z1k_przed_kampaniami_2026'])} marży przed kosztem kampanii przy "
                   f"{tz(D['q3_nowe_z1k_wydatki_2026'])} wydatków, czyli wyszli prawie na zero "
                   f"({tzn(D['q3_nowe_z1k_marza_2026'])}). Pozostała część biznesu straciła {tz(-D['q3_reszta_z1k_zmiana'])}:"),
            punkty([f"opłaty TelemediGO {tz(D['q3_reszta_z1k_telemedigo_zmiana'])}, w tym {tz(go[8])} sprzedaży osobnej w "
                    f"newsletterze ({liczba(go[0])} zakupów we wrześniu {rok - 1} wobec {liczba(go[1])} w całym III kwartale "
                    f"{rok});",
                    f"wyższe wydatki kampanii działających w obu latach {tz(D['q3_reszta_z1k_wydatki_wklad'])};",
                    f"marża konsultacji {tzn(D['q3_reszta_z1k_konsultacje_marza_zmiana'])}: powtórnych zamówień jest więcej, "
                    f"ale każde zostawia mniej marży;",
                    "prowizja bez zmian." if abs(prow) < 100 else f"prowizja {tzn(prow)}."]),
            akapit(f"Po odjęciu TelemediGO zostaje {tz(luka)} spadku. W rachunku przypada on na wyższe wydatki kampanii "
                   f"działających w obu latach, częściowo zrównoważone wyższą marżą konsultacji. Rozkład nie oddziela skutków "
                   f"awarii w Safari od innych zmian przychodu. Według sesji płatności podział się odwraca: nowe kampanie "
                   f"{tz(D['q3_nowe_z2_marza_2026'])}, reszta {tzn(D['q3_reszta_z2_zmiana'])}; suma jest ta sama."),
            podtytul(f"Awaria Safari w III kwartale {rok}"),
            akapit(okresy(safari)),
            podtytul("Baza powracających pacjentów"),
            akapit(f"Pierwsze kwartały roku wcześniej nie miały jeszcze pełnej bazy powracających pacjentów. Marża z pacjentów "
                   f"pozyskanych w poprzednich kwartałach to {proc(D['baza_udzial_w_marzy_proc_2024_q4'], 0)} marży IV "
                   f"kwartału 2024, {proc(D['baza_udzial_w_marzy_proc_2025_q1'])} I kwartału 2025 i "
                   f"{proc(D['baza_udzial_w_marzy_proc_2025_q3'])} III kwartału 2025. Bez tej bazy marża rośnie rok do roku o "
                   f"{proc(D['marza_bez_bazy_zmiana_proc_2025_q4'])} zamiast {proc(D['marza_zmiana_proc_2025_q4'])} w IV "
                   f"kwartale 2025 i o {proc(D['marza_bez_bazy_zmiana_proc_2026_q1'])} zamiast "
                   f"{proc(D['marza_zmiana_proc_2026_q1'])} w I kwartale 2026. Miarodajne jest więc porównanie III kwartałów "
                   f"(baza to {proc(D['baza_udzial_w_marzy_proc_2025_q3'])} i {proc(D['baza_udzial_w_marzy_proc_2026_q3'])} "
                   f"marży)."),
            akapit(f"Bez jednorazowej nadwyżki startu sprzedaży TelemediGO (jej części przypadającej na bazę: "
                   f"{liczba(E['baza_2025_osobno'])} z {liczba(E['q3_osobno_25'])} zakupów) baza dała w III kwartale {rok} "
                   f"więcej marży niż rok wcześniej: {tz(E['baza_2026'])} wobec {tz(E['baza_2025_bez_nadwyzki'])} "
                   f"({zn(E['baza_zmiana_bez_nadwyzki_proc'])}%; bez całej sprzedaży w newsletterze w obu latach "
                   f"{zn(baza_bez_osobno)}%). Wszystkich pacjentów pozyskanych w poprzednich kwartałach jest prawie trzy razy "
                   f"więcej ({liczba(pac['2026-Q3'])} wobec {liczba(pac['2025-Q3'])}), ale tych, którzy w kwartale coś kupili, "
                   f"tylko o {proc(100 * (E['baza_2026_aktywni'] / E['baza_2025_aktywni'] - 1), 0)} więcej "
                   f"({liczba(E['baza_2026_aktywni'])} wobec {liczba(E['baza_2025_aktywni'])}). Dane nie rozdzielają, ile to "
                   f"wiek bazy, a ile to, że nowsze roczniki wracają rzadziej."),
            podtytul("Przychód i koszty za cały rok"),
            akapit(przychody),
            akapit(jak_liczymy),
        ],
        zrodlo="analiza/wyniki/e_merytoryka.txt (punkty 2 i 3); analiza/wyniki/d_wynik.txt (punkty 1 i 2); "
               "analiza/wyniki/c_priorytety.txt (W4, P1); eksport analiza/b_eksport.py.")
    return ET.popraw(k), ["d:Rozkład spadku marży w III kwartale 2026"]


def karta_ekonomia(ek, V, E):
    rows = ek["wiersze"]

    def r(poziom, klucz, regula, okno, okres=2):
        return next(x for x in rows if x["poziom"] == poziom and x["klucz"] == klucz and x["regula"] == regula
                    and x["okno"] == okno and x["okres"] == okres)
    tt = {reg: r("kampania", "tt_prosp_l4_15min", reg, 90)["wynik"] for reg in ("Z1K", "Z2")}
    assert max(tt.values()) < 0, "TikTok na L4 ma mieć wynik ujemny w obu regułach"
    g = {(reg, o): r("grupa", "1_nowe_kampanie_L4", reg, o)["wynik"] for reg in ("Z1K", "Z2") for o in (90, 180)}
    assert g[("Z1K", 90)] > 0 > g[("Z2", 90)], "znak wyniku nowych kampanii ma zależeć od reguły"
    assert all(r("grupa", gr, reg, 90)["wynik"] > 0 for gr in ("2_pozostale_platne", "3_afiliacja_ranking", "4_bezplatne")
               for reg in ("Z1K", "Z2"))
    w2 = lambda k, o: (E[f"powtorne_{k}_{o}_proc"], E[f"powtorne_{k}_{o}_zam"])  # noqa: E731
    k = karta(
        "Kampania TikTok na L4 nie zwraca kosztu pozyskania pacjenta",
        wniosek=f"Po odjęciu kosztu pozyskania TikTok na L4 traci w 90 dniach około {liczba(-tt['Z1K'], 0)} zł na pacjencie "
                f"według pierwszego wejścia i około {liczba(-tt['Z2'], 0)} zł według sesji z płatnością.",
        tresc=[
            akapit(f"Obie nowe kampanie na L4 razem wychodzą blisko zera: około {zlz(g[('Z1K', 90)], 0)} na pacjenta w 90 "
                   f"dniach według pierwszego wejścia i około {zlz(g[('Z2', 90)], 0)} według sesji z płatnością. Znak zależy "
                   f"od reguły. Test z wyłączeniem reklamy Meta na L4 w części kraju zmierzy przyrost pacjentów niezależnie od "
                   f"reguły (pozycja 9 listy priorytetów)."),
            akapit("Pozostałe kampanie płatne, afiliacja i kanały bezpłatne mają wynik dodatni w obu regułach (tabela niżej)."),
        ],
        zastrzezenie=f"Wynik Google Ads na markę i remarketingu Meta jest liczony ostrożnie: rachunek kosztu pozyskania "
                     f"liczy tylko nowych pacjentów, a {proc(w2('gs_brand', 2)[0], 0)} i "
                     f"{proc(w2('meta_rmkt_koszyk', 2)[0], 0)} zamówień w sesjach tych kampanii to zamówienia powtórne, których marży "
                     f"tym kampaniom nie przypisujemy.",
        szczegoly=[
            akapit(f"W 90 dniach: TikTok na L4 {zlz(tt['Z1K'])} i {zlz(tt['Z2'])} na pacjenta, obie nowe kampanie razem "
                   f"{zlz(g[('Z1K', 90)])} i {zlz(g[('Z2', 90)])}. Po 180 dniach nowe kampanie na L4 dają "
                   f"{zlz(g[('Z1K', 180)])} na pacjenta według pierwszego wejścia i {zlz(g[('Z2', 180)])} według sesji z "
                   f"płatnością."),
            akapit(f"Według pierwszego wejścia pacjent należy do kanału, z którego pierwszy raz wszedł na stronę, a kod "
                   f"kampanii na pierwszym zamówieniu rozstrzyga; według sesji z płatnością należy do kanału sesji, w której "
                   f"zapłacił. W nowych kampaniach różnica między tymi podziałami to jedna grupa: według sesji z płatnością "
                   f"do innych kanałów trafia {liczba(E['p_X_caly'])} pacjentów nowych kampanii na L4 z ostatnich 12 "
                   f"miesięcy. {liczba(E['p_X_caly_wejscie_n'])} z nich weszło pierwszy raz z reklamy nowej kampanii, a "
                   f"zapłaciło w innej sesji, a {liczba(E['p_X_caly_tylko_kod_n'])} weszło z innego kanału, ale zapłaciło z "
                   f"kodem nowej kampanii. W ekonomii kampanii pokazujemy oba podziały, bo od nich zależy, której kampanii "
                   f"przypisujemy koszt pozyskania."),
            akapit(f"Zamówienia powtórne w sesjach kampanii w ostatnich 12 miesiącach: Google Ads na markę "
                   f"{proc(w2('gs_brand', 2)[0])} z {zile(w2('gs_brand', 2)[1], 'zamowienie')}, remarketing Meta "
                   f"{proc(w2('meta_rmkt_koszyk', 2)[0])} z {zile(w2('meta_rmkt_koszyk', 2)[1], 'zamowienie')}. Rok wcześniej "
                   f"{proc(w2('gs_brand', 1)[0])} i {proc(w2('meta_rmkt_koszyk', 1)[0])}."),
            akapit("Obok wyniku po 90 dniach pokazujemy wynik po 180 dniach: pacjenci kampanii na L4 prawie nie wracają, a "
                   "pozostali tak, więc 90 dni zaniża wartość pozostałych kampanii. Przedział przy wyniku jest warunkowy: "
                   "liczony tylko z rozrzutu marży, bez niepewności przypisania źródła."),
            akapit("Nazwy kampanii w danych: Meta na L4 to meta_prosp_l4_szybko, TikTok na L4 to tt_prosp_l4_15min, Google "
                   "Ads na markę to gs_brand, remarketing Meta to meta_rmkt_koszyk."),
        ],
        zrodlo="analiza/a5e_ekonomia.py → analiza/wyniki/a5e_kampanie.csv i a5e_ekonomia.txt; "
               "analiza/wyniki/e_merytoryka.txt (punkty 1 i 5a).")
    return ET.popraw(k), []


# ---------------------------------------------------------------- Jakość danych

def karty_jakosc(jak, mostek, V, E):
    K = {}
    du, te, gz = jak["duplikaty"], jak["testy"], jak["godzina"]
    m = lambda i, kl: mostek["kroki"][i]["miary"][kl]  # noqa: E731
    K["karta"] = karta(
        "Dane wymagały dwóch poprawek; pozostałe niespójności są drobne",
        wniosek=f"Usunęliśmy zamówienia zapisane w eksporcie dwa razy ({liczba(du['kopie'])}) i zamówienia kont testowych "
                f"({liczba(V['testy_razem'][0])}).",
        tresc=[akapit("Danych nikt wcześniej nie czyścił. Poza tymi dwiema rzeczami jedna godzina bez danych i kilka "
                      "drobnych niespójności dotyczą małej części danych.")],
        zrodlo="analiza/a2_jakosc.py, analiza/a2_czyste.py, analiza/a3_dashboard.py; liczby liczy analiza/b_eksport.py.")
    K["mostek"] = karta(
        "Dashboard zawyża wzrost zamówień i przychodu, a liczbę pacjentów pokazuje prawie dobrze",
        wniosek=f"Po oczyszczeniu zamówienia rosną o {proc(m(2, 'zamowienia')['wzrost'], 0)}, a nie o "
                f"{proc(m(0, 'zamowienia')['wzrost'], 0)}, jak na dashboardzie.",
        tresc=[akapit(f"Przychód z konsultacji po odjęciu zwrotów rośnie o {proc(m(3, 'przychod')['wzrost'], 0)}, a nie o "
                      f"{proc(m(0, 'przychod')['wzrost'], 0)}. Nowych pacjentów jest więcej o {proc(m(2, 'nowi')['wzrost'], 0)}, "
                      f"prawie tak samo jak na dashboardzie, a sprzedaż TelemediGO rośnie o {proc(m(2, 'go')['wzrost'], 0)}, "
                      f"bez zmian.")],
        wstaw="mostek",
        szczegoly=[
            akapit("Każdy wiersz tabeli zmienia jedną rzecz: najpierw usuwa kopie zamówień, potem konta testowe, a na końcu "
                   "odejmuje zwroty od przychodu."),
            akapit(f"Zamówienia: {liczba(m(0, 'zamowienia')['p1'])} → {liczba(m(0, 'zamowienia')['p2'])} na dashboardzie i "
                   f"{liczba(m(2, 'zamowienia')['p1'])} → {liczba(m(2, 'zamowienia')['p2'])} po oczyszczeniu. Przychód z "
                   f"konsultacji: {liczba(m(0, 'przychod')['p1'] / 1e6, 3)} → {liczba(m(0, 'przychod')['p2'] / 1e6, 3)} mln zł "
                   f"na dashboardzie i {liczba(m(3, 'przychod')['p1'] / 1e6, 3)} → {liczba(m(3, 'przychod')['p2'] / 1e6, 3)} "
                   f"mln zł po oczyszczeniu i odjęciu zwrotów."),
        ],
        zrodlo="analiza/a3_dashboard.py → analiza/wyniki/a3_dashboard.txt i a3_siatka.csv; eksport analiza/b_eksport.py.")

    # duplikaty
    od, do = dt.date.fromisoformat(du["od"]), dt.date.fromisoformat(du["do"])
    i0, i1 = (od - dt.date.fromisoformat(jak["start"])).days, (do - dt.date.fromisoformat(jak["start"])).days
    udz = [100 * k / z for k, z in zip(du["kopie_d"][i0:i1 + 1], du["zamowienia_d"][i0:i1 + 1])]
    assert du["kopie_d"][i0 - 1] == 0 and du["kopie_d"][i1 + 1] == 0
    mz = re.search(r"i ([\d\s]+?)\szł zapłat, czyli ([\d\s]+?)\szł po odjęciu zwrotów", du["zdania"][1])
    zap, net = (int(re.sub(r"\D", "", x)) for x in mz.groups())
    K["duplikaty"] = karta(
        f"W czerwcu {od.year} eksport zapisał część zamówień dwa razy; zostawiamy jedną kopię",
        wniosek=f"Od {data(od)} do {data(do)} eksport zapisał dwa razy {ile(du['kopie'], 'zamowienie')}.",
        tresc=[
            akapit(f"W tych dniach to od {proc(min(udz), 0)} do {proc(max(udz), 0)} zamówień dziennie, a dzień przed i dzień "
                   f"po nie ma ani jednej kopii."),
            akapit(f"Wszystkie kopie są w ostatnich 12 miesiącach i dodają do nich {zl(zap)} zapłat ({zl(net)} po odjęciu "
                   f"zwrotów). W analityce każde z tych zamówień ma jeden krok płatności, więc to wygląda na błąd eksportu: "
                   f"pacjent zapłacił raz."),
        ],
        szczegoly=[akapit("Kopia to druga, identyczna linia tego samego zamówienia, tuż pod pierwszą w pliku zamówień. "
                          "Wykres pokazuje dzień po dniu zamówienia bez kopii i kopie.")],
        zrodlo="analiza/a2_jakosc.py; czyszczenie: analiza/a2_czyste.py.")

    # zamówienia testowe
    t0 = te["zdania"][0]
    t_kod = t0.split(". ", 1)[1]                                         # bez pierwszego zdania („Zamówienia testowe: …”)
    t_przyb = zacz(te["zdania"], "Testów przybywa")
    t_pien = zacz(te["zdania"], "Pieniądze").split(". ")[0].replace("Pieniądze: ", "Zamówienia testowe to ") + "."
    raz_t = V["testy"][2] / V["testy"][1]
    assert 2.5 <= raz_t < 3, "„prawie trzy razy więcej” wymaga ilorazu od 2,5 do 3"
    K["testy"] = karta(
        "Zamówienia testowe zawyżały wzrost zamówień, bo jest ich prawie trzy razy więcej niż rok wcześniej",
        wniosek=f"Zamówienia testowe to {ile(V['testy_razem'][0], 'zamowienie')} z {liczba(V['testy_konta'])} kont; "
                f"wyłączamy je ze wszystkich liczb.",
        tresc=[akapit(t_kod), akapit(zacz(te["zdania"], "Drugi, niezależny podpis")), akapit(okresy(t_przyb))],
        zastrzezenie=f"Nie wiemy, czy lekarze dostawali wynagrodzenie za te wizyty. Gdyby tak, kosztowałoby to około "
                     f"{liczba(V['testy_koszt_2lata'] / 1000, 0)} tys. zł w dwóch latach, w tym około "
                     f"{liczba(V['testy_koszt2'] / 1000, 0)} tys. zł w ostatnich 12 miesiącach (Czego nie wiemy, punkt 14).",
        szczegoly=[akapit(t_pien),
                   akapit(f"Koszt liczymy po stawce internisty z zadania ({B2.KOSZT_INTERNISTY} zł), bo wszystkie wizyty "
                          f"testowe są u internisty ({liczba(V['testy_razem'][1])} z {liczba(V['testy_razem'][0])}): "
                          f"{zl(V['testy_koszt_2lata'])} w dwóch latach i {zl(V['testy_koszt2'])} w ostatnich 12 "
                          f"miesiącach.")],
        zrodlo="analiza/a2_jakosc.py → analiza/wyniki/a2_jakosc.txt (2e); analiza/wyniki/c_priorytety.txt (P1b, P13).")

    # godzina bez danych
    g0 = dt.datetime.fromisoformat(gz["od"])
    ml = re.search(r"jest (\d+) (?:sesja|sesji|sesje) zamiast typowych (\d+)", gz["zdanie"])
    ses, typ = int(ml.group(1)), int(ml.group(2))
    K["godzina"] = karta(
        "Jednej godziny prawie nie ma w danych, ale wyników to nie zmienia",
        wniosek=f"{data(g0.date())} od {g0:%H:%M} do {(g0 + dt.timedelta(hours=1)):%H:%M} jest {ile(ses, 'sesja')} zamiast "
                f"typowych {liczba(typ)}.",
        tresc=[akapit(f"Zamówień w tej godzinie jest zwykle około {liczba(E['godzina_zam_mediana'])}, więc to, że nie ma "
                      f"żadnego, niewiele mówi. To jedyna taka godzina w dwóch latach, a jej wpływ na wyniki jest pomijalny.")],
        zastrzezenie="Nie wiemy, czy to przerwa w działaniu strony, czy w zbieraniu danych.",
        szczegoly=[akapit(f"Typowa liczba to mediana tej samej godziny w 15 dniach wokół: {liczba(typ)} sesji i "
                          f"{ile(E['godzina_zam_mediana'], 'zamowienie')}. Szukamy godzin, w których sesji jest dużo mniej niż "
                          f"ta mediana; w dwóch latach jest tylko ta jedna.")],
        zrodlo="analiza/a2_jakosc.py, sekcja o lukach; analiza/wyniki/e_merytoryka.txt (punkt 5e).")
    K["drobne"] = karta(
        "Drobne niespójności dotyczą małej części danych",
        wniosek="Każda z nich dotyczy najwyżej kilkudziesięciu zamówień albo kilkuset sesji.",
        tresc=[punkty(jak["drobne"])],
        zrodlo="analiza/a2_jakosc.py → analiza/wyniki/a2_jakosc.txt.")
    K["czyste"] = karta(
        "Pozostałe sprawdzenia wyszły czysto",
        wniosek="Czas płatności, kolejność kroków lejka, koszty kampanii, tożsamość pacjentów i pozostałe tabele są spójne.",
        tresc=[punkty(jak["czyste"])],
        zrodlo="analiza/a2_jakosc.py, analiza/a2_czyste.py; liczby liczy analiza/b_eksport.py.")
    return {k: ET.popraw(v) for k, v in K.items()}


# ---------------------------------------------------------------- Zdarzenia

def zdarzenia_teksty(zdz, nag, jak, V, E):
    """Teksty zdarzeń na osi (tytuł jako wniosek, krótka nazwa do list i legend, słownik, numery niewiadomych).
    Zmienia zdz["lista"] w miejscu. Zwraca kartę wstępu zakładki."""
    L = {z["id"]: z for z in zdz["lista"]}
    # opis metody stoi raz, w szczegółach wstępu zakładki; przy zdarzeniu tylko krótkie odesłanie
    metoda_opis = ("Metoda wykrywania zmian dzieli serię dzienną na odcinki o różnym poziomie (podział binarny); zmianę "
                   "uznajemy, gdy różnica poziomów wynosi co najmniej 4 błędy standardowe (|z| ≥ 4). Daty to kandydaci "
                   "zmian; każdego sprawdzamy potem na danych.")
    metoda = "Dzień wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki). "
    zr_ret = "Źródło: analiza/a5r_zdarzenia.py; notatki/a5_retencja.md, krok 5."
    r_lut = V["rano"].loc["2026-02":"2026-09", "int_rano_ponad15_spoza_nowych"]
    Z_ = {}

    gz = jak["godzina"]
    co_g = gz["zdanie"].split(" To jedyna")[0] + " To jedyna taka godzina w dwóch latach."
    Z_["luka_godzina"] = dict(
        tytul="Jednej godziny prawie nie ma w danych, ale wyników to nie zmienia", krotko="Godzina bez danych",
        co=co_g,
        ile=f"Zamówień w tej godzinie jest zwykle około {liczba(E['godzina_zam_mediana'])}, więc ich brak niewiele mówi. Nie "
            f"wiemy, czy to przerwa w działaniu strony, czy w zbieraniu danych. Wpływ na wyniki jest pomijalny.",
        skad="Liczba sesji i zamówień w każdej godzinie wobec mediany tej samej godziny w 15 dniach wokół. Źródło: "
             "analiza/a2_jakosc.py, sekcja o lukach; analiza/wyniki/e_merytoryka.txt, punkt 5e.")

    z = L["start_go_upsell"]
    ile_go, dni_go = z["ile"].split(" Sesje z tej kampanii")
    Z_["start_go_upsell"] = dict(
        tytul="Newsletter zaczyna sprzedawać samo TelemediGO, a pierwsze tygodnie dają jednorazowy skok sprzedaży",
        krotko="Start sprzedaży TelemediGO w newsletterze",
        co=z["co"],
        ile=f"W pierwszych {liczba(E['newsletter_dni_startu'])} dniach newsletter sprzedał "
            f"{ile(E['q3_osobno_25'], 'czlonkostwo')}, a przy późniejszym tempie sprzedałby około "
            f"{liczba(E['newsletter_norma_startu'])}. Ta jednorazowa nadwyżka ({ile(round(E['newsletter_nadwyzka']), 'zakup')}, "
            f"{tz(E['newsletter_nadwyzka_zl'])}) podnosi marżę III kwartału 2025, z którą porównujemy III kwartał 2026. "
            "Razem: " + ile_go,
        skad="Pierwszy dzień z sesjami z kodem kampanii crm_go_upsell. Sesje z tej kampanii" + dni_go + " Późniejsze tempo "
             f"to średnia z ostatnich 12 miesięcy ({liczba(E['newsletter_tempo_dzienne'], 2)} zakupu dziennie). Źródło: "
             "analiza/a5p_lejek.py, sekcja 1; analiza/wyniki/e_merytoryka.txt, punkt 2; notatki/a5_pozyskanie.md, "
             "punkt 2.4.")

    z = L["marza30_spada"]
    Z_["marza30_spada"] = dict(
        tytul="Marża nowego pacjenta w pierwszych 30 dniach spada w trzech krokach, głównie przez skład pacjentów",
        krotko="Marża na pacjenta w 30 dniach spada",
        co="Marża nowego pacjenta w pierwszych 30 dniach, przed kosztem pozyskania, spada trzema stopniami. Przybywa "
           "pacjentów nowych kampanii na L4, którzy zostawiają mniej marży.",
        ile=z["ile"], skad=metoda + zr_ret)

    for id_, nazwa, kod, por in (("start_meta_l4", "Meta na L4", "meta_prosp_l4_szybko", "sesje z wyszukiwarki"),
                                 ("start_tiktok", "TikTok na L4", "tt_prosp_l4_15min",
                                  "sesje z wyszukiwarki i kampanii Meta na L4")):
        z = L[id_]
        apl = "aplikacje Instagrama i Facebooka" if kod.startswith("meta") else "aplikację TikToka"
        Z_[id_] = dict(
            tytul=f"Rusza kampania {nazwa}; jej sesje płacą rzadziej niż {por}",
            krotko=f"Start kampanii {nazwa}",
            co=f"Pierwszy dzień z sesjami i kosztem kampanii {nazwa}. Kampania przyprowadza głównie ruch z przeglądarek "
               f"wbudowanych w {apl}. Jej sesje płacą rzadziej niż {por}.",
            ile=okresy(z["ile"]),
            skad=f"Pierwszy dzień z sesjami z kodem kampanii {kod} w analityce; ten sam dzień w wydatkach na kampanie. "
                 f"Źródło: analiza/a5p_zdarzenia.py, sekcja 6; notatki/a5_pozyskanie.md, punkt 2.")

    z = L["udzial_nowych"]
    Z_["udzial_nowych"] = dict(
        tytul="Coraz więcej nowych pacjentów przychodzi z kampanii na L4, a ci pacjenci prawie nie wracają",
        krotko="Rośnie udział nowych kampanii w nowych pacjentach",
        co="Od startu kampanii Meta na L4 coraz większa część nowych pacjentów przychodzi z dwóch nowych kampanii na L4 "
           "(Meta i TikTok). Ci pacjenci prawie nie wracają, więc ich udział obniża powrót całej kohorty.",
        ile=z["ile"], skad=metoda + zr_ret)

    z = L["zwroty_pierwsze"]
    Z_["zwroty_pierwsze"] = dict(
        tytul="Coraz więcej pierwszych zamówień kończy się zwrotem po odbytej wizycie",
        krotko="Więcej zwrotów po wizycie",
        co="Rośnie odsetek pierwszych zamówień, za które pacjent dostaje zwrot po odbytej wizycie. Skupia się w wizytach "
           "L4 pacjentów nowych kampanii. Lekarz dostaje wynagrodzenie także za te wizyty.",
        ile=z["ile"], skad=metoda + zr_ret)

    z = L["opoznienia_rano"]
    Z_["opoznienia_rano"] = dict(
        tytul="Poranne wizyty u internisty coraz częściej zaczynają się ponad 15 minut po terminie",
        krotko="Poranne opóźnienia u internisty",
        co="Rośnie odsetek wizyt u internisty z terminem 6:00–11:59, które zaczynają się ponad 15 minut po terminie, także "
           "u pacjentów spoza nowych kampanii. Przy tym samym porannym ruchu opóźnień jest dużo więcej niż rok wcześniej, "
           "a już pierwsza poranna wizyta dnia jest często spóźniona. Przyczyny w danych nie widać (Czego nie wiemy, "
           "punkt 4).",
        ile=z["ile"] + f" To średnie poziomy odcinków wyznaczonych przez metodę. Miesiąc po miesiącu od lutego do września "
                       f"2026 to {B2.zakres(r_lut.min(), r_lut.max(), 1, '%')} porannych wizyt, jak w zakładce „Po "
                       f"zakupie”.",
        skad=metoda + "Seria: wizyty u internisty rano, pacjenci spoza nowych kampanii. " + zr_ret)

    z = L["remarketing_meta"]
    Z_["remarketing_meta"] = dict(
        tytul="Remarketing Meta coraz rzadziej kończy się płatnością, a jednocześnie trafia do innych osób niż wcześniej",
        krotko="Remarketing Meta słabnie",
        co=z["co"], ile=okresy(z["ile"]),
        skad=z["skad"].replace("Źródło:", "Kod kampanii: meta_rmkt_koszyk. Źródło:"))

    z = L["powrot30_spada"]
    Z_["powrot30_spada"] = dict(
        tytul="Powrót nowych pacjentów w 30 dniach spada skokowo, głównie przez skład pacjentów",
        krotko="Spada powrót w 30 dniach",
        co=z["co"].split(" To głównie")[0] + " To głównie skład pacjentów: rośnie udział nowych kampanii, których pacjenci "
                                             "prawie nie wracają.",
        ile=z["ile"],
        skad=metoda + "Udział składu pokazuje rozkład spadku powrotu (notatki/a5_retencja.md, krok 3). " + zr_ret)

    z = L["powrot90_stare"]
    Z_["powrot90_stare"] = dict(
        tytul="W kampaniach działających w obu latach powrót też spada, ale bez wyraźnego skoku",
        krotko="Powrót w kampaniach działających w obu latach",
        co="W kampaniach obecnych w obu latach powrót w 90 dniach też spada, ale metoda nie znalazła zmiany skokowej "
           "powyżej progu. Najsilniejszy kandydat to ten dzień.",
        ile=z["ile"],
        skad="Kandydata wskazała metoda wykrywania zmian w serii dziennej (opis we wstępie zakładki); różnica jest poniżej "
             "progu. Brak skoku nie znaczy, że spadek musi być rozłożony w czasie. Luty 2026 nie pasuje do hipotezy, że "
                      "większe opóźnienia zawsze obniżają powrót: opóźnienia były wtedy już wysokie, a powrót w tych "
                      "kampaniach nie spadł. To trop do sprawdzenia. " + zr_ret)

    z = L["safari_ios"]
    sk, so = V["safari_krok"], V["safari_okresy"]
    d_s = dt.date.fromisoformat(nag["safari"]["data"])
    dzien_saf = f"{d_s.day} {B2.MIESIACE_DOP[d_s.month - 1]} {d_s.year}"
    s60 = nag["safari"]
    Z_["safari_ios"] = dict(
        tytul=f"Od {dzien_saf} w Safari na iPhone'ach i iPadach dużo rzadziej udaje się założyć nowe konto",
        krotko="Awaria zakładania konta w Safari na iOS",
        co=z["co"],
        ile=f"Krok konta po wyborze terminu spadł z {proc(sk[0])} (od {so[0]} do {so[1]}) do {proc(sk[1])} (od {so[2]} do "
            f"{so[3]}, {ile(sk[2], 'sesja')} z wyborem terminu) i nie wraca. W 60 dniach przed awarią i po niej: "
            f"{proc(s60['przed_proc'])} ({ile(s60['przed_k2'], 'sesja')}) i {proc(s60['po60_proc'])} "
            f"({ile(s60['po60_k2'], 'sesja')}); pozostałe przeglądarki {proc(s60['reszta_przed_proc'])} i "
            f"{proc(s60['reszta_po60_proc'])}. Szacunek: {liczba(s60['utracone_od'])}–{liczba(s60['utracone_do'])} "
            f"utraconych pierwszych zamówień w {liczba(s60['dni_po'])} dniach do {data(O2[1])}, czyli "
            f"{liczba(s60['na30_od'])}–{liczba(s60['na30_do'])} na 30 dni.",
        skad=z["skad"])

    z = L["marka_konwersja"]
    Z_["marka_konwersja"] = dict(
        tytul="W kampanii Google Ads na markę mniej sesji kończy się płatnością, a przyczyny w danych nie widać",
        krotko="Spada konwersja Google Ads na markę",
        co="Sesja do płatności u osób, które jeszcze nie kupowały, spada w kampanii Google Ads na markę. Przyczyny w danych "
           "nie widać (Czego nie wiemy, punkt 22).",
        ile=z["ile"],
        skad=z["skad"].replace("Źródło:", "Kod kampanii: gs_brand. Źródło:"))

    z = L["duplikaty"]
    Z_["duplikaty"] = dict(
        tytul=f"W czerwcu {dt.date.fromisoformat(z['od']).year} eksport zapisał część zamówień dwa razy; zostawiamy jedną "
              f"kopię",
        krotko="Duplikaty zamówień w eksporcie",
        co=z["co"],
        ile=okresy(z["ile"]).replace("Wszystkie kopie są w ostatnich 12 miesiącach. Dodają mu",
                                     "Wszystkie kopie są w ostatnich 12 miesiącach i dodają do nich").replace(
            "więc to wygląda na błąd eksportu, a nie na podwójne płatności", "więc to wygląda na błąd eksportu: pacjent "
            "zapłacił raz"),
        skad=z["skad"])

    brak = set(L) - set(Z_)
    assert not brak, f"zdarzenia bez nowego tekstu: {brak}"
    for id_, t in Z_.items():
        for k, v in t.items():
            L[id_][k] = ET.popraw(v)

    w_oknie = [z for z in zdz["lista"] if "2025-11-01" <= z["od"] <= "2026-03-31"]
    assert 2 * len(w_oknie) > len(zdz["lista"]), "„większość zmian” wymaga ponad połowy zdarzeń w tych miesiącach"
    wstep = karta(
        "Większość zmian zaczyna się między listopadem 2025 a marcem 2026",
        wniosek="W tych miesiącach ruszają dwie nowe kampanie na L4, rosną poranne opóźnienia u internistów i psuje się "
                "zakładanie konta w Safari na iOS.",
        tresc=[akapit("Listy zmian w produkcie i kalendarza kampanii nie mamy, więc każde zdarzenie znaleźliśmy w danych. "
                      "Przy każdym jest data, co się zmieniło, o ile i skąd to wiemy.")],
        zastrzezenie="Zdarzenia z tych samych miesięcy nakładają się, więc bez testu nie rozdzielamy ich skutków.",
        szczegoly=[akapit("Tory na osi: lejek (pozyskanie), retencja (kohorty), obsługa pacjenta (przebieg wizyt) i jakość "
                          "danych. " + metoda_opis)])
    return ET.popraw(wstep)


# ---------------------------------------------------------------- główna funkcja

def dodaj_karty(kontrole, V, Z, E, wz, mostek, nag, jak, zdz, koh, pz, wy):
    """Dopisuje karty do danych zakładek (w miejscu) i kontrolę liczb do listy `kontrole`.
    Zwraca listę wyników kontroli (jak e_teksty.kontrola) do raportu."""
    bloki = []
    koh["karta"], dawne = karta_kohorty(koh, wz, V, E, Z)
    bloki.append(("kohorty", koh["karta"], dawne, []))

    pz["karty"], dawne = karty_po_zakupie(pz, wz, V, E, Z)
    for k, v in pz["karty"].items():
        bloki.append((f"po_zakupie/{k}", v, dawne[k], []))

    wy["karta"], dawne = karta_wynik(wy, V, E, Z)
    bloki.append(("wynik", wy["karta"], dawne, []))
    wy["ekonomia"]["karta"], dawne = karta_ekonomia(wy["ekonomia"], V, E)
    bloki.append(("wynik/ekonomia", wy["ekonomia"]["karta"], dawne, []))

    kj = karty_jakosc(jak, mostek, V, E)
    jak["karta"] = kj.pop("karta")
    jak["karty"] = kj
    bloki.append(("jakosc", jak["karta"], [], []))
    for k, v in kj.items():
        bloki.append((f"jakosc/{k}", v, [], []))

    zdz["karta"] = zdarzenia_teksty(zdz, nag, jak, V, E)
    bloki.append(("zdarzenia", zdz["karta"], [], []))
    dawne_zd = {"marka_konwersja": ["d:Google Ads na markę od 22.05.2026"], "start_go_upsell": ["d:Kampania `crm_go_upsell`"]}
    for z in zdz["lista"]:
        bloki.append((f"zdarzenie/{z['id']}", {k: z[k] for k in ("tytul", "krotko", "co", "ile", "skad")},
                      dawne_zd.get(z["id"], []), []))

    return ET.kontrola(bloki, notatka=ET.E_TEKSTY_ZAKLADKI, prefiks="z")


# ---------------------------------------------------------------- notatka z tekstami (szkic do przeglądu i wzorzec kontroli)

def _md_blok(b):
    if isinstance(b, str):
        return [b]
    t = b.get("typ")
    if t == "akapit":
        return [b["tekst"]]
    if t in ("punkty", "numerowane"):
        return [f"- {p}" for p in b["punkty"]]
    if t == "podtytul":
        return [f"**{b['tekst']}**"]
    if t == "tabela":
        kom = lambda k: k if isinstance(k, str) else (k["tekst"] + (f" ({k['pod']})" if k.get("pod") else ""))  # noqa: E731
        out = [f"*{b['tytul']}*"] if b.get("tytul") else []
        out += ["| " + " | ".join(b["kolumny"]) + " |", "|" + "---|" * len(b["kolumny"])]
        out += ["| " + " | ".join([w["opis"]] + [kom(k) for k in w["komorki"]]) + " |" for w in b["wiersze"]]
        return out
    return [b.get("tekst", "")]


def _md_karta(k):
    out = [f"Tytuł: {k['tytul']}"]
    if k.get("znacznik"):
        out.append(f"Znacznik: {k['znacznik']['tekst']}")
    if k.get("wniosek"):
        out.append(f"Wniosek: {k['wniosek']}")
    for b in k.get("tresc", []):
        out += _md_blok(b)
    if k.get("wstaw"):
        out.append(f"(Tu strona rysuje element „{k['wstaw']}”.)")
    if k.get("zastrzezenie"):
        out.append(f"Zastrzeżenie: {k['zastrzezenie']}")
    if k.get("szczegoly"):
        out.append("Szczegóły:")
        for b in k["szczegoly"]:
            out += _md_blok(b)
    if k.get("zrodlo"):
        out.append(f"Skąd liczby: {k['zrodlo']}")
    return out


def zapisz_notatke():
    """Odtwarza notatki/e_teksty_zakladki.md z plików strony (po eksporcie)."""
    js = lambda n, k: B2.wczytaj_js(n, k)  # noqa: E731
    koh, pz, wy = js("kohorty.js", ".kohorty"), js("po_zakupie.js", ".po_zakupie"), js("wynik.js", ".wynik")
    jak, zdz = js("jakosc.js", ".jakosc"), js("zdarzenia.js", ".zdarzenia")
    linie = [
        "# E — nowe teksty zakładek „Kohorty”, „Po zakupie”, „Zdarzenia”, „Wynik biznesu” i „Jakość danych” "
        "(szkic do przeglądu Kuby, 2026-10-21)", "",
        "Teksty kart w nowym kształcie (notatki/e_runda.md, punkt 3), napisane według zasad języka Kuby (część 2 zlecenia) "
        "i wyników części 1 (e_runda.md, punkt 4). Buduje je `analiza/e_teksty_zakladki.py` z danych zakładek i raportów; "
        "ten plik odtwarza z plików strony polecenie `python -I analiza/e_teksty_zakladki.py` (po eksporcie). Każda sekcja "
        "„### klucz” to wzorzec kontroli liczb jednej karty albo jednego zdarzenia: każda liczba na stronie w tej karcie "
        "musi tu stać. Odwołania do „Czego nie wiemy” są już w nowej numeracji (dawna pozycja 13 wypadła).", "",
        "Słownik: „ostatnie 12 miesięcy” = X 2025 – IX 2026, „rok wcześniej” = X 2024 – IX 2025. Przyjęta reguła źródła = "
        "pierwsze wejście pacjenta, a kod kampanii na pierwszym zamówieniu rozstrzyga; druga reguła = sesja płatności.", "",
        "## Kohorty", "", "### kohorty", ""] + _md_karta(koh["karta"]) + ["", "## Po zakupie", ""]
    for k, v in pz["karty"].items():
        linie += [f"### po_zakupie/{k}", ""] + _md_karta(v) + [""]
    linie += ["Nagłówki tabeli godzin terminu: " + " · ".join(pz["godziny"]["kolumny"]) + ".", "",
              "## Wynik biznesu", "", "### wynik", ""] + _md_karta(wy["karta"]) + [""]
    linie += ["### wynik/ekonomia", ""] + _md_karta(wy["ekonomia"]["karta"]) + ["", "## Jakość danych", "", "### jakosc", ""]
    linie += _md_karta(jak["karta"]) + [""]
    for k, v in jak["karty"].items():
        linie += [f"### jakosc/{k}", ""] + _md_karta(v) + [""]
    linie += ["## Zdarzenia", "", "### zdarzenia", ""] + _md_karta(zdz["karta"]) + [""]
    for z in zdz["lista"]:
        linie += [f"### zdarzenie/{z['id']}", "", f"Data: {z['od']}" + (f" – {z['do']}" if z.get("do") else ""),
                  f"Tytuł: {z['tytul']}", f"Krótko (listy i legendy): {z['krotko']}", f"Co się zmieniło: {z['co']}"]
        if z.get("ile"):
            linie.append(f"O ile: {z['ile']}")
        linie += [f"Skąd wiemy: {z['skad']}", ""]
    with open(ET.E_TEKSTY_ZAKLADKI, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linie).rstrip() + "\n")
    print(f"zapisano {ET.E_TEKSTY_ZAKLADKI} ({len(linie)} linii)")


if __name__ == "__main__":
    # Notatka jest od 2026-10-22 wzorcem kontroli poprawianym ręcznie (decyzja sesji prowadzącej): odtworzenie jej
    # z plików strony zrobiłoby kontrolę liczb pustą. Nadpisanie tylko świadomie, z flagą --nadpisz.
    import sys
    if "--nadpisz" in sys.argv:
        zapisz_notatke()
    else:
        print("Notatka notatki/e_teksty_zakladki.md jest wzorcem kontroli i nie jest odtwarzana. Flaga --nadpisz nadpisuje ją.")
