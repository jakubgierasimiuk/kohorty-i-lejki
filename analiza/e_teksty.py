"""E — teksty strony w nowym kształcie karty (notatki/e_runda.md, punkt 3), runda „merytoryka, język, wygląd”.

Ten moduł ma dwie części:
  1. wspólne narzędzia dla nowych tekstów (używa ich też analiza/e_teksty_zakladki.py): budowa kart i bloków, słownik
     (okres 1 → rok wcześniej itd.), nowe numery niewiadomych po usunięciu dawnej pozycji 13, kontrola liczb;
  2. teksty zakładek „Czy to wzrost”, „Priorytety”, „Czego nie wiemy” i nagłówka lejka (sesja prowadząca).

Zasada liczb bez zmian: żadnej liczby wpisanej ręcznie. Liczby przychodzą z raportów (przez b2_eksport_c.wartosci, V)
i z analiza/wyniki/e_merytoryka.json (E). Kontrola: każda liczba w tekstach karty musi stać we fragmencie notatki
z tekstami (notatki/e_teksty.md albo notatki/e_teksty_zakladki.md, sekcja „### <klucz>”) albo w fragmencie dawnej
notatki (c_szkic.md, d_teksty_strony.md), z której pochodzi przeniesione zdanie.
"""
import json
import os
import re

import b2_eksport_c as B2

KATALOG = B2.KATALOG
WYNIKI = B2.WYNIKI
E_TEKSTY = os.path.join(KATALOG, "notatki", "e_teksty.md")
E_TEKSTY_ZAKLADKI = os.path.join(KATALOG, "notatki", "e_teksty_zakladki.md")

liczba, proc, zn, zl, tz, tzn, t1, ile, zakres = B2.liczba, B2.proc, B2.zn, B2.zl, B2.tz, B2.tzn, B2.t1, B2.ile, B2.zakres


def wczytaj_e():
    with open(os.path.join(WYNIKI, "e_merytoryka.json"), encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- karty i bloki (kontrakt: notatki/e_runda.md, punkt 3)

def karta(tytul, wniosek=None, znacznik=None, tresc=None, zastrzezenie=None, szczegoly=None, linki=None, zrodlo=None,
          **inne):
    k = {"tytul": tytul}
    if znacznik:
        k["znacznik"] = znacznik
    if wniosek:
        k["wniosek"] = wniosek
    if tresc:
        k["tresc"] = tresc
    if zastrzezenie:
        k["zastrzezenie"] = zastrzezenie
    if szczegoly:
        k["szczegoly"] = szczegoly
    if linki:
        k["linki"] = linki
    if zrodlo:
        k["zrodlo"] = zrodlo
    k.update(inne)
    return k


def znacznik(tekst, stan):
    return {"tekst": tekst, "stan": stan}


def akapit(t):
    return {"typ": "akapit", "tekst": t}


def punkty(lista):
    return {"typ": "punkty", "punkty": list(lista)}


def numerowane(lista):
    return {"typ": "numerowane", "punkty": list(lista)}


def podtytul(t):
    return {"typ": "podtytul", "tekst": t}


def tabela(kolumny, wiersze, tytul=None):
    t = {"typ": "tabela", "kolumny": kolumny, "wiersze": wiersze}
    if tytul:
        t["tytul"] = tytul
    return t


def wiersz(opis, komorki, podsuma=False):
    w = {"opis": opis, "komorki": komorki}
    if podsuma:
        w["podsuma"] = True
    return w


def zmiana(tekst, wartosc, lepiej_gdy_rosnie=True, pod=None):
    """Komórka ze zmianą rok do roku: strzałka według znaku, kolor i słowo według tego, czy zmiana jest dobra."""
    kier = "bez" if round(wartosc, 6) == 0 else ("wzrost" if wartosc > 0 else "spadek")
    if kier == "bez":
        stan = "neutralnie"
    else:
        stan = "dobrze" if (wartosc > 0) == lepiej_gdy_rosnie else "zle"
    k = {"tekst": tekst, "zmiana": kier, "stan": stan}
    if pod:
        k["pod"] = pod
    return k


def link(tekst, href):
    return {"tekst": tekst, "href": href}


# ---------------------------------------------------------------- słownik i numery niewiadomych

# Dawna niewiadoma 13 (stawka pediatry) wypada z listy: to założenie z zadania (punkt 10 listy Kuby). Pozycje 14–22
# dostają numery 13–21. Odwołania w tekstach przenumerowuje funkcja przenumeruj().
NIEWIADOMA = {n: (n if n < 13 else n - 1) for n in range(1, 23) if n != 13}


def przenumeruj(t):
    """Odwołania do niewiadomych w przeniesionych zdaniach: „Czego nie wiemy, punkt 19” → „punkt 18”, „niewiadoma 21” → „20”."""
    def zamien(m):
        n = int(m.group(2))
        return m.group(1) + str(NIEWIADOMA.get(n, n))
    t = re.sub(r"(Czego nie wiemy, punkt )(\d+)", zamien, t)
    t = re.sub(r"(niewiadom[aąeiy] )(\d+)", zamien, t)
    return t


# Zamiany słownika (część 2 listy Kuby): „okres 1/2” → „rok wcześniej / ostatnie 12 miesięcy”. Kolejność ma znaczenie.
SLOWNIK = [
    (r"\bw okresie X 2024 – IX 2025\b", "rok wcześniej (X 2024 – IX 2025)"),
    (r"\bw okresie X 2025 – IX 2026\b", "w ostatnich 12 miesiącach (X 2025 – IX 2026)"),
    (r"\bOkres X 2024 – IX 2025\b", "Rok wcześniej (X 2024 – IX 2025)"),
    (r"\bOkres X 2025 – IX 2026\b", "Ostatnie 12 miesięcy (X 2025 – IX 2026)"),
    (r"\bWcześniejsze kwartały okresu 1\b", "Pierwsze kwartały"),
    (r"\bjest okres 2\b", "są ostatnie 12 miesięcy"),
    (r"\bw obu okresach;", "w dwóch latach;"),
    (r"\bW okresie 1\b", "Rok wcześniej"),
    (r"\bW okresie 2\b", "W ostatnich 12 miesiącach"),
    (r"\bw okresie 1\b", "rok wcześniej"),
    (r"\bw okresie 2\b", "w ostatnich 12 miesiącach"),
    (r"\bz okresu 1\b", "sprzed roku"),
    (r"\bz okresu 2\b", "z ostatnich 12 miesięcy"),
    (r"\bokresu 1\b", "roku wcześniej"),
    (r"\bokresu 2\b", "ostatnich 12 miesięcy"),
    (r"\bOkres 1\b", "Rok wcześniej"),
    (r"\bOkres 2\b", "Ostatnie 12 miesięcy"),
    (r"\bokres 1\b", "rok wcześniej"),
    (r"\bokres 2\b", "ostatnie 12 miesięcy"),
]


def slownik(t):
    for a, b in SLOWNIK:
        t = re.sub(a, b, t)
    return przenumeruj(t)


def popraw(obj):
    """Słownik i numery niewiadomych we wszystkich napisach struktury (bez odnośników i pól technicznych)."""
    if isinstance(obj, str):
        return slownik(obj)
    if isinstance(obj, list):
        return [popraw(x) for x in obj]
    if isinstance(obj, dict):
        return {k: (v if k in ("href", "zrodlo", "id", "poziom", "stan", "zmiana", "typ") else popraw(v)) for k, v in obj.items()}
    return obj


# ---------------------------------------------------------------- kontrola liczb

POMIJANE = ("linki", "zrodlo", "href", "_dodane", "_fragmenty", "nr", "id", "poziom", "stan", "zmiana", "typ", "wstaw")


def napisy(obj):
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        out = []
        for k, v in obj.items():
            if k in POMIJANE:
                continue
            out += napisy(v)
        return out
    if isinstance(obj, list):
        out = []
        for v in obj:
            out += napisy(v)
        return out
    return []


def fragmenty_notatki(sciezka):
    if not os.path.exists(sciezka):
        return {}
    with open(sciezka, encoding="utf-8") as f:
        s = f.read().replace("\r\n", "\n")
    return {m.group(1).strip(): m.group(0) for m in re.finditer(r"^### (.+?)$.*?(?=^### |^## |\Z)", s, re.M | re.S)}


def _stare():
    out = {f"c:{k}": v for k, v in B2.szkic_fragmenty().items()}
    with open(B2.D_TEKSTY, encoding="utf-8") as f:
        s = f.read().replace("\r\n", "\n")
    for m in re.finditer(r"^### (.+?)$.*?(?=^### |^## |\Z)", s, re.M | re.S):
        out["d:" + m.group(1).strip()] = m.group(0)
    return out


def kontrola(bloki, notatka=E_TEKSTY, prefiks="e"):
    """bloki: lista (nazwa, obiekt, [dodatkowe fragmenty, np. 'c:pozycja:3' albo 'd:<nagłówek>'], [liczby dodane]).
    Fragment własny to sekcja „### nazwa” w notatce. Zwraca listę (nazwa, liczb, bez pokrycia, użyte dodane)."""
    fr = fragmenty_notatki(notatka)
    stare = _stare()
    wynik = []
    for nazwa, obj, dodatkowe, dodane in bloki:
        wzor = fr.get(nazwa, "")
        for d in dodatkowe:
            if d.startswith("d:"):
                klucz = next((h for h in stare if h.startswith(d)), None)
                wzor += stare.get(klucz, "") if klucz else ""
            else:
                wzor += stare.get(d, "")
        if not wzor:
            wynik.append((f"{prefiks}:{nazwa[:22]}", 0, ["brak fragmentu w notatce"], []))
            continue
        teksty_ = [re.sub(r"\b12 miesi\w+", "", t) for t in napisy(obj)]   # „ostatnie 12 miesięcy” to słownik, nie liczba
        odw = [m.group(1) for t in teksty_ for m in re.finditer(r"(?:Czego nie wiemy, punkt |niewiadom[aąeiy] )(\d+)", t)]
        w, dod = set(B2.tokeny(wzor)), set(B2.tokeny(" | ".join(list(dodane) + odw)))
        tk = [x for t in teksty_ for x in B2.tokeny(t)]
        wynik.append((f"{prefiks}:{nazwa[:22]}", len(tk), sorted({x for x in tk if x not in w and x not in dod}),
                      sorted({x for x in tk if x not in w and x in dod})))
    return wynik


# ---------------------------------------------------------------- teksty sesji prowadzącej

O1_TEKST, O2_TEKST = "rok wcześniej (X 2024 – IX 2025)", "ostatnie 12 miesięcy (X 2025 – IX 2026)"


def zacz(lista, poczatek):
    """Napis z listy zaczynający się od `poczatek` (zdania przenoszone z dawnych tekstów)."""
    return next(x for x in lista if x.startswith(poczatek))


def z0(x):
    """Zaokrąglenie do całości do zdań z najwyżej dwiema liczbami."""
    return liczba(x, 0)


def wzrost(V, E, C):
    """„Czy to wzrost” w nowym kształcie (notatki/e_teksty.md, sekcja 1). C = dawne dane zakładki (do przeniesienia zdań)."""
    W0 = C["wzrost"]
    n1, n2 = V["nowi"][1], V["nowi"][2]
    wz = V["w1_zm"]
    W, B1, B2_, NZ = V["pow_wszyscy"], V["pow_bez_z1k"], V["pow_bez_z2"], V["pow_nowe_z1k"]
    Dd = V["D"]
    kw = E["kwartaly"]
    q3 = kw[-1]
    q3t = B2.q3_teksty(V)
    zaks = q3t["safari_zaks"]
    bloki = []

    werdykt = {"znacznik": znacznik("Nie", "zle"),
               "tekst": "Pacjentów przybywa, ale wracają rzadziej. Wydatki na kampanie rosną dużo szybciej niż marża, "
                        "którą biznes zarabia przed ich kosztem.",
               "dopisek": f"Za cały rok marża po wszystkich kosztach wzrosła o {z0(E['rok_marza_zmiana_proc'])}%: z "
                          f"{z0(E['rok_marza_1'] / 1000)} do {z0(E['rok_marza_2'] / 1000)} tys. zł."}
    kafelki = [
        {"liczba": f"+{z0(wz[0])}%", "podpis": "nowych pacjentów niż rok wcześniej",
         "dopisek": f"bez dwóch nowych kampanii na L4: +{z0(wz[1])}%", "zmiana": "wzrost", "stan": "dobrze"},
        {"liczba": f"{z0(W['p90_o2'])}%", "podpis": "nowych pacjentów wraca w ciągu 90 dni",
         "dopisek": f"rok wcześniej {z0(W['p90_o1'])}%", "zmiana": "spadek", "stan": "zle"},
        {"liczba": f"×{liczba(q3['wydatki_razy'], 1)}", "podpis": "wydatki na kampanie w III kwartale 2026 wobec roku wcześniej",
         "dopisek": f"marża przed ich kosztem: +{z0(q3['przed_rr_dokl'])}%", "zmiana": "wzrost", "stan": "uwaga"},
    ]
    decyzje = {"tytul": "Decyzje na pierwszy tydzień", "punkty": [
        {"nr": 1, "tekst": "Naprawić zakładanie konta w Safari na iPhone'ach", "href": "#priorytety?p=1",
         "dopisek": f"pozycja 1 · do {z0(V['p1_hi'][3] / 1000)} tys. zł marży rocznie"},
        {"nr": 2, "tekst": "Wstrzymać kampanię TikTok na L4 i kampanię Google Ads na specjalistów", "href": "#priorytety?p=3",
         "dopisek": "pozycje 3 i 4 · obie tracą na każdym pacjencie według obu reguł przypisania, a pauzę da się cofnąć "
                    "w jeden dzień"},
        {"nr": 3, "tekst": "Oczyścić codzienny raport i dodać alarmy na lejku", "href": "#priorytety?p=2",
         "dopisek": f"pozycja 2 · awaria Safari trwała {liczba(V['p1_lo'][1])} dni bez alarmu"},
    ]}
    bloki.append(("wzrost/werdykt", werdykt, [], []))
    bloki.append(("wzrost/kafelki", kafelki, [], []))
    bloki.append(("wzrost/decyzje", decyzje, [], []))

    # --- więcej pacjentów
    nowe_udz = 100 * V["nowe_7268"] / n2
    pac = karta(
        "Pacjentów przybywa, ale głównie z dwóch nowych kampanii na L4",
        etykieta="Więcej pacjentów", znacznik=znacznik("Tak", "dobrze"),
        wniosek=f"Nowych pacjentów jest o {z0(wz[0])}% więcej niż rok wcześniej, a bez kampanii Meta i TikTok na L4 "
                f"tylko o {z0(wz[1])}%.",
        tresc=[punkty([
            f"{liczba(n2)} nowych pacjentów w ostatnich 12 miesiącach wobec {liczba(n1)} rok wcześniej.",
            f"Bez pacjentów dwóch nowych kampanii na L4: {liczba(V['bez_z1k'])}. Te kampanie dały {z0(nowe_udz)}% nowych "
            f"pacjentów, a ich pacjent zostawia w 90 dniach {z0(V['nowe_marza'][4])} zł marży wobec "
            f"{z0(V['m90_bez_z1k'])} zł pozostałych.",
            f"Z kanałów bezpłatnych (wejścia bezpośrednie, bezpłatna wyszukiwarka, program poleceń) przybyło "
            f"{z0(wz[3])}%: z {liczba(V['bezpl'][1])} do {liczba(V['bezpl'][2])}.",
        ])],
        zastrzezenie="Nie wiemy, ilu pacjentów nowych kampanii przyszłoby i bez nich. Sprawdzi to test z wyłączeniem "
                     "reklamy w części kraju (pozycja 9 listy priorytetów).",
        szczegoly=[punkty([
            f"Dokładnie: {zn(wz[0])}% wszystkich nowych pacjentów, {zn(wz[1])}% bez nowych kampanii, {zn(wz[3])}% z "
            f"kanałów bezpłatnych. Pacjenci nowych kampanii: {liczba(V['nowe_7268'])} z {liczba(n2)} ({z0(nowe_udz)}%), "
            f"marża w 90 dniach {liczba(V['nowe_marza'][4], 1)} zł wobec {liczba(V['m90_bez_z1k'], 1)} zł.",
            f"Pacjent nowej kampanii to według przyjętej reguły ten, który pierwszy raz wszedł z jej reklamy albo zapłacił "
            f"z jej kodem rabatowym. Według drugiej reguły (sesja płatności) pacjentów bez nowych kampanii jest "
            f"{liczba(V['bez_z2'])}, czyli {zn(wz[2])}%. Różnica to {liczba(E['p_X_caly'])} pacjentów, którzy weszli z "
            f"reklamy nowej kampanii ({z0(E['p_X_caly_wejscie_proc'])}% z nich) albo zapłacili z jej kodem "
            f"({z0(E['p_X_caly_kod_proc'])}%), a płatność zrobili w innej sesji, najczęściej po wejściu bezpośrednim "
            f"albo z wyszukiwarki. Wracają tak rzadko jak pozostali pacjenci nowych kampanii, więc w opisie pacjentów "
            f"i retencji trzymamy się reguły przyjętej. W ekonomii kampanii pokazujemy obie.",
        ])],
        linki=[link("Kohorty: nowi pacjenci według źródła pozyskania", "#kohorty?okno=90&podz=kanal&wygl=28")],
        zrodlo="analiza/wyniki/c_priorytety.txt (W1), analiza/wyniki/e_merytoryka.txt (punkt 1). Notatki: "
               "notatki/c_szkic.md (sekcja 1a), notatki/e_teksty.md.")
    bloki.append(("wzrost/pacjenci", pac, ["c:wzrost"], W0["_dodane"]))

    # --- lepsza retencja
    dok = V["powroty_dokladne"]
    p180 = V["p180"]
    okna = [(o, W[f"p{o}_o1"], int(W[f"n{o}_o1"]), W[f"p{o}_o2"], int(W[f"n{o}_o2"])) for o in (30, 60, 90)]
    okna.append((180, p180[2], int(p180[0]), p180[3], int(p180[1])))
    tab = tabela(["Powrót w ciągu", "Rok wcześniej", "Ostatnie 12 miesięcy", "Zmiana"],
                 [wiersz(f"{o} dni", [f"{proc(a)} ({liczba(na)} pacjentów)", f"{proc(b)} ({liczba(nb)} pacjentów)",
                                     zmiana(f"{zn(dok[o][1] - dok[o][0])} pkt proc.", dok[o][1] - dok[o][0])])
                  for o, a, na, b, nb in okna])
    rz1 = V["rozklad_z1k"]
    u_z1k = E["rozklad_Z1K_udzial_nowych_w_spadku"]
    l4 = "powrot90_internista_l4_bez_nowych_"

    def usl(u, przedzial=False):
        k = f"powrot90_{u}_bez_nowych_z1k_"
        t = (f"{proc(Dd[k + 'proc_okres1'])} ({liczba(Dd[k + 'pacjenci_okres1'])} pacjentów) do "
             f"{proc(Dd[k + 'proc_okres2'])} ({liczba(Dd[k + 'pacjenci_okres2'])})")
        if przedzial:
            t += f", od {liczba(Dd[k + 'zmiana_od'], 1)} do {zn(Dd[k + 'zmiana_do'])} punktu"
        return t
    pw = V["powracajacy"]
    ret = karta(
        "Pacjenci wracają rzadziej, także poza nowymi kampaniami",
        etykieta="Lepsza retencja", znacznik=znacznik("Nie", "zle"),
        wniosek=f"W ciągu 90 dni wraca {z0(W['p90_o2'])}% nowych pacjentów, a rok wcześniej wracało {z0(W['p90_o1'])}%.",
        tresc=[tab, punkty([
            f"Bez pacjentów nowych kampanii powrót też spada: {proc(B1['p90_o2'])} wobec {proc(W['p90_o1'])}.",
            f"Pacjenci nowych kampanii wracają w {proc(NZ['p90_o2'])}. Ich większy udział odpowiada za około "
            f"{z0(u_z1k)}% spadku, a reszta to spadek w kanałach działających w obu latach.",
            f"Marża na pacjenta w 90 dniach, przed kosztem pozyskania: {liczba(V['m90'][2], 1)} zł wobec "
            f"{liczba(V['m90'][1], 1)} zł. Poza nowymi kampaniami prawie stoi: {liczba(V['m90_bez_z1k'], 1)} zł.",
        ])],
        zastrzezenie="To opis, a nie przyczyna. Nie wiemy, czy ci sami pacjenci zachowują się dziś gorzej, czy zmieniło "
                     "się to, kto do nas trafia.",
        szczegoly=[punkty([
            f"Powrót to kolejne zamówienie, które nie zostało anulowane. Liczymy go na tych samych dniach kalendarzowych "
            f"(pierwsze zakupy do {int(pw[2])} {B2.MIESIACE_DOP[int(pw[1]) - 1]} w obu latach przy oknie 90 dni) i tylko "
            f"w kohortach z pełnym oknem obserwacji. Liczba pacjentów: {liczba(W['n90_o1'])} rok wcześniej i "
            f"{liczba(W['n90_o2'])} w ostatnich 12 miesiącach; bez nowych kampanii {liczba(B1['n90_o2'])}, pacjenci nowych "
            f"kampanii {liczba(NZ['n90_o2'])}.",
            f"Kolejne zamówienia na pacjenta w 90 dniach: {liczba(Dd['kolejne90_wszyscy_okres2_srednia_na_pacjenta'], 3)} "
            f"wobec {liczba(Dd['kolejne90_wszyscy_okres1_srednia_na_pacjenta'], 3)}, czyli o "
            f"{proc(100 * (1 - Dd['kolejne90_wszyscy_okres2_srednia_na_pacjenta'] / Dd['kolejne90_wszyscy_okres1_srednia_na_pacjenta']))} "
            f"mniej; bez pacjentów nowych kampanii {liczba(Dd['kolejne90_bez_nowych_z1k_okres2_srednia_na_pacjenta'], 3)}.",
            f"Druga reguła (sesja płatności) daje bez nowych kampanii powrót {proc(B2_['p90_o2'])} i marżę "
            f"{liczba(V['m90_bez_z2'], 1)} zł. Cała różnica to {liczba(E['r_X_n'])} pacjentów nowych kampanii (z pełnym "
            f"oknem 90 dni), których ta reguła przypisuje starym kanałom, bo zapłacili w innej sesji niż ta, w której "
            f"weszli z reklamy. Wracają w {liczba(E['r_X_powrot'], 1)}%. Bez nich obie reguły dają {proc(B1['p90_o2'])} i "
            f"{liczba(V['m90_bez_z1k'], 1)} zł, a udział nowych kampanii w spadku powrotu wynosi w obu {z0(u_z1k)}% "
            f"(według sesji płatności bez tej poprawki {z0(E['rozklad_Z2_udzial_nowych_w_spadku'])}%).",
            f"„Około {z0(u_z1k)}% spadku” to rozkład opisowy: udział pacjentów nowych kampanii ({liczba(100 - rz1[1], 1)}% "
            f"kohort) razy różnica powrotu między nimi a resztą ({liczba(abs(rz1[5]), 1)} z {liczba(abs(rz1[4]), 1)} punktu "
            f"procentowego). Nie mówi, co by się stało bez tych kampanii.",
            "Według pierwszej usługi, bez pacjentów nowych kampanii (95% przedział różnicy): spada po e-recepcie z "
            f"{usl('internista_e_recepta')}, a po wizycie u innego specjalisty z {usl('inny_specjalista')}. Bez istotnej "
            f"zmiany: pediatra z {usl('pediatra', True)}, psychiatra z {usl('psychiatra', True)}, pierwsze L4 u internisty "
            f"z {usl('internista_l4', True)}. Według sesji płatności L4 spada do {proc(Dd[l4 + 'z2_proc_okres2'])}, ale to "
            f"ta sama grupa: do {liczba(Dd[l4 + 'z1k_pacjenci_okres2'])} pacjentów reguły przyjętej dochodzi "
            f"{liczba(Dd[l4 + 'z2_pacjenci_okres2'] - Dd[l4 + 'z1k_pacjenci_okres2'])} pacjentów nowych kampanii z pierwszym L4.",
            f"Liczba osób, które wróciły w 90 dniach, rośnie: {liczba(pw[4])} wobec {liczba(pw[3])} ({zn(pw[5])}%). Spada "
            f"odsetek, a nie liczba powracających.",
            f"W 180 dniach liczymy tylko kohorty z pełnym oknem ({liczba(p180[0])} i {liczba(p180[1])} pacjentów), więc to "
            f"wcześniejsze, mniejsze grupy niż w 90 dniach.",
            "Spadek w kanałach działających w obu latach zbiega się z porannymi opóźnieniami u internistów, ale ich nie "
            "dowodzi (Czego nie wiemy, punkt 4).",
        ])],
        linki=[link("Kohorty: powrót w 90 dniach, nowe kampanie na L4 i pozostałe", "#kohorty?okno=90&podz=grupa&wygl=28"),
               link("Kohorty: powrót bez pacjentów nowych kampanii", "#kohorty?okno=90&f_grupa=pozostale&wygl=28")],
        zrodlo="analiza/wyniki/c_priorytety.txt (W2), analiza/wyniki/a5r_kohorty.txt (180 dni), analiza/wyniki/d_retencja.txt "
               "(usługi, kolejne zamówienia), analiza/wyniki/e_merytoryka.txt (punkt 1).")
    bloki.append(("wzrost/retencja", ret, ["c:wzrost"], W0["_dodane"]))

    # --- TelemediGO
    G0 = W0["telemedigo"]
    tab_go = tabela(["Typ zakupu", "Rok wcześniej", "Ostatnie 12 miesięcy", "Zmiana", "Udział we wzroście"],
                    [wiersz(r["opis"].replace("Osobno, z newslettera crm_go_upsell", "Osobno, z newslettera"),
                            r["komorki"], podsuma=(r["opis"] == "Razem")) for r in G0["tabela"]["wiersze"]])
    g2a = V["go_2a"]
    razem = V["go_typy"].loc["razem"]
    go = karta(
        "TelemediGO rośnie razem z liczbą zamówień, a nie dzięki większej chęci zakupu",
        wniosek=f"Sprzedaż wzrosła o {z0(razem['zmiana_proc'])}%, bo jest więcej zamówień i przez cały rok działała "
                f"sprzedaż w newsletterze, a odsetek kupujących przy kasie nie rośnie.",
        tresc=[tab_go, punkty([
            f"Opłata 89 zł nie pokrywa zniżek: członkostwa sprzed roku dostały średnio o "
            f"{liczba(abs(g2a['oplata_minus_znizka_efektywna_na_czlonkostwo']), 2)} zł więcej zniżek, niż przyniosły opłat.",
            f"Widać to w marży: powtórne zamówienie pacjenta spoza nowych kampanii zostawiło w III kwartale 2026 "
            f"{liczba(E['pw_m26'], 2)} zł marży wobec {liczba(E['pw_m25'], 2)} zł rok wcześniej. Prawie cały ten spadek to "
            f"rosnący udział wizyt ze zniżką TelemediGO: z {z0(E['pw_go_udzial_25'])}% do {z0(E['pw_go_udzial_26'])}% "
            f"powtórnych zamówień.",
        ])],
        zastrzezenie="Nie wiemy, ile wizyt członkostwo dokłada. Test z pozycji 12 pokaże wpływ samej zniżki, ale nie "
                     "opłacalność oferty za 89 zł.",
        szczegoly=[punkty([popraw(x).replace("Rozstrzygnie to test z pozycji 12: losowy, bezpłatny dostęp do zniżek.",
                                             "Test z pozycji 12 (losowy, bezpłatny dostęp do zniżek) pokaże wpływ samej "
                                             "zniżki.")
                           for x in G0["punkty"]] + [
            f"Wizyta ze zniżką TelemediGO zostawia średnio {liczba(E['pw_go_m26'], 2)} zł marży, bez zniżki "
            f"{liczba(E['pw_none_m26'], 2)} zł, a wizyta u specjalisty ze zniżką traci {liczba(abs(E['pw_inni_go_m26']), 2)} zł. "
            f"Udział wizyt ze zniżką wśród powtórnych zamówień: {liczba(E['pw_go_udzial_25'], 1)}% "
            f"({liczba(E['pw_n25'])} zamówień) i {liczba(E['pw_go_udzial_26'], 1)}% ({liczba(E['pw_n26'])}). Zmiana tego "
            f"udziału daje {liczba(abs(E['pw_mix']), 2)} zł z {liczba(abs(E['pw_zmiana']), 2)} zł spadku marży na zamówienie "
            f"(rozkład na strukturę i marżę w obrębie rodzaju zniżki)."])],
        linki=G0["linki"], zrodlo=G0["zrodlo"].replace("Liczby: ", "") + " Marża powtórnych zamówień: "
                                                                          "analiza/wyniki/e_merytoryka.txt (punkt 3).")
    bloki.append(("wzrost/telemedigo", go, ["c:telemedigo"], G0["_dodane"]))

    # --- wynik
    nazwy_kw = {"2025-10-01": "IV 2025", "2026-01-01": "I 2026", "2026-04-01": "II 2026", "2026-07-01": "III 2026"}
    tab_kw = tabela(["Kwartał", "Marża przed kosztem kampanii", "Wydatki na kampanie", "Marża po wszystkich kosztach"],
                    [wiersz(nazwy_kw[r["kw"]], [
                        zmiana(f"{zn(r['przed_rr_dokl'])}%", r["przed_rr_dokl"], pod=tz(r["przed"])),
                        zmiana(f"×{liczba(r['wydatki_razy'], 2)}", r["wydatki_razy"] - 1, lepiej_gdy_rosnie=False,
                               pod=tz(r["wydatki"])),
                        zmiana(f"{zn(r['marza_rr_dokl'])}%", r["marza_rr_dokl"], pod=tz(r["marza"]))]) for r in kw],
                    tytul="Zmiana wobec tego samego kwartału rok wcześniej; pod nią wartość w kwartale")
    baza1 = (E["baza_2026"] - E["baza_2026_osobno_zl"]) / (E["baza_2025"] - E["baza_2025_osobno_zl"]) - 1
    luka = -Dd["q3_reszta_z1k_luka_bez_telemedigo"]
    wy = karta(
        "Wydatki na kampanie rosną szybciej niż marża, którą biznes zarabia przed ich kosztem",
        wniosek=f"W III kwartale 2026 marża przed kosztem kampanii wzrosła o {z0(q3['przed_rr_dokl'])}%, a wydatki na "
                f"kampanie były ponad dwa razy wyższe niż rok wcześniej.",
        tresc=[tab_kw, punkty([
            f"Za cały rok marża po wszystkich kosztach wzrosła o {liczba(E['rok_marza_zmiana_proc'], 1)}%: z "
            f"{z0(E['rok_marza_1'] / 1000)} do {z0(E['rok_marza_2'] / 1000)} tys. zł. Marża przed kosztem kampanii "
            f"wzrosła o {liczba(E['rok_przed_zmiana_proc'], 1)}%, a wydatki na kampanie o "
            f"{liczba(E['rok_wyd_zmiana_proc'], 1)}%.",
            f"Spadek marży w III kwartale 2026 ({liczba(E['q3_zmiana_proc'], 1)}%) nie jest pewny. Rok wcześniej we "
            f"wrześniu jednorazowo ruszyła sprzedaż TelemediGO w newsletterze: {liczba(E['q3_osobno_25'])} zakupów w "
            f"{liczba(E['newsletter_dni_startu'])} dni. Bez tej nadwyżki marża III kwartału 2026 jest o "
            f"{liczba(E['q3_w1_zmiana_proc'], 1)}% wyższa niż rok wcześniej.",
            f"Awaria zakładania konta w Safari na iPhone'ach kosztowała w samym III kwartale 2026 szacunkowo "
            f"{zakres(zaks[0] / 1000, zaks[1] / 1000, 1)} tys. zł marży.",
        ])],
        zastrzezenie="Wyniku kwartału bez awarii Safari nie mierzymy; to scenariusz z pozycji 1 listy priorytetów.",
        szczegoly=[punkty([
            f"Warianty III kwartału: bez nadwyżki startu sprzedaży w newsletterze ({z0(E['newsletter_nadwyzka'])} z "
            f"{liczba(E['q3_osobno_25'])} zakupów ponad zwykłe tempo {z0(E['newsletter_norma_startu'])} na "
            f"{liczba(E['newsletter_dni_startu'])} dni, {tz(E['newsletter_nadwyzka_zl'])}) {zn(E['q3_w1_zmiana_proc'])}%; "
            f"bez całej sprzedaży w newsletterze w obu latach {zn(E['q3_w2_zmiana_proc'])}%; bez wszystkich opłat za "
            f"TelemediGO {zn(E['q3_w3_zmiana_proc'])}%. Marża przed kosztem kampanii bez nadwyżki startu rośnie o "
            f"{liczba(E['q3_przed_bez_nadwyzki_zmiana_proc'], 1)}%.",
            slownik(zacz(W0["kwartaly"]["punkty"], "W samych miesiącach")),
            f"Baza powracających pacjentów (marża z pacjentów pozyskanych w poprzednich kwartałach): w III kwartale 2026 "
            f"{tz(E['baza_2026'])} wobec {tz(E['baza_2025'])} rok wcześniej. Rok wcześniej zawierała jednorazowy start "
            f"sprzedaży w newsletterze; bez tej nadwyżki to {tz(E['baza_2025_bez_nadwyzki'])}, więc w 2026 baza dała o "
            f"{liczba(E['baza_zmiana_bez_nadwyzki_proc'], 1)}% więcej (bez całej sprzedaży w newsletterze w obu latach o "
            f"{liczba(100 * baza1, 1)}% więcej). Liczy przy tym prawie trzy razy więcej pacjentów "
            f"({liczba(V['q3_baza_pac']['2026-Q3'])} wobec {liczba(V['q3_baza_pac']['2025-Q3'])}), więc marża na jednego "
            f"pacjenta bazy jest dużo niższa: baza jest starsza, a nowsze roczniki wracają rzadziej (opis, bez rozdzielenia "
            f"tych dwóch rzeczy).",
            slownik(q3t["baza"]) + " Wzrost tych kwartałów jest więc zawyżony startem od zera.",
            "Rozkład spadku III kwartału na pacjentów nowych kampanii i resztę biznesu to rozkład księgowy: przypisanie "
            "składników marży grupom pacjentów, a nie zmierzony wpływ. " + slownik(q3t["wstep"][:-1]) + ": "
            + " ".join(q3t["reszta"]).replace(";", ",").replace(
                "ale każde zostawia mniej marży", "ale każde zostawia mniej marży, głównie przez większy udział wizyt ze "
                "zniżką TelemediGO").rstrip(".") + ". "
            f"Po odjęciu TelemediGO reszta biznesu traci {tz(luka)}; księgowo to wyższe wydatki kampanii działających "
            f"w obu latach, częściowo zrównoważone wyższą marżą konsultacji. Według sesji płatności podział między nowe "
            f"kampanie ({tz(Dd['q3_nowe_z2_marza_2026'])}) a resztę ({tzn(Dd['q3_reszta_z2_zmiana'])}) się odwraca; suma "
            f"jest ta sama.",
        ])],
        linki=[link("Wynik biznesu: marża po kwartałach", "#wynik"),
               link("Priorytety: pozycja 1, Safari", "#priorytety?p=1")],
        zrodlo="analiza/wyniki/c_priorytety.txt (W3, W4), analiza/wyniki/d_wynik.txt (punkty 1 i 2), "
               "analiza/wyniki/e_merytoryka.txt (punkt 2).")
    bloki.append(("wzrost/wynik", wy, ["c:wzrost", "c:pozycja:1", "d:Rozkład spadku"], W0["_dodane"]))

    # --- dashboard a dane oczyszczone
    dz, cz = V["dash_zam"], V["czyste_zam"]
    zast = {z["tytul"]: z["tekst"] for z in W0["zastrzezenia"]}
    dash = karta(
        "Dashboard pokazuje więcej wzrostu, niż jest w danych",
        wniosek=f"Po oczyszczeniu danych zamówień przybyło o {z0(cz[0])}%, a nie o {z0(dz[0])}%.",
        tresc=[punkty([
            f"Dashboard liczy dane na surowo: z {liczba(V['dup'])} zdublowanymi zamówieniami z {V['dup_daty']}, z "
            f"{liczba(V['testy_razem'][0])} zamówieniami {liczba(V['testy_konta'])} kont testowych i z przychodem przed "
            f"zwrotami.",
            f"Po oczyszczeniu przychód z konsultacji po zwrotach rośnie o {proc(cz[3])} zamiast {z0(dz[3])}%. Liczba nowych "
            f"pacjentów i sprzedaż TelemediGO prawie się nie zmieniają.",
        ])],
        wstaw="mostek",
        zastrzezenie="Pierwszy rok startował od zera, bez bazy powracających pacjentów, więc sumy roczne z definicji "
                     "faworyzują drugi rok.",
        szczegoly=[punkty([slownik(t + " " + zast[t]) for t in ("Dashboard liczy dane na surowo.", "Start od zera.",
                                                                 "Wynik biznesu rośnie wolniej niż sprzedaż.")])],
        linki=[link("Jakość danych: od dashboardu do danych oczyszczonych", "#jakosc")],
        zrodlo="analiza/a3_dashboard.py, analiza/a2_czyste.py, analiza/wyniki/c_priorytety.txt (W3).")
    bloki.append(("wzrost/dashboard", dash, ["c:wzrost"], W0["_dodane"]))

    dalej = karta("Co dalej", tresc=[akapit("Co z tego robimy: lista priorytetów, od najważniejszej pozycji, z wartością "
                                            "w marży. Czego dane nie rozstrzygają i jakim testem to domknąć: zakładka "
                                            "„Czego nie wiemy”.")],
                  linki=[link("Priorytety", "#priorytety"), link("Czego nie wiemy", "#niewiadome")])
    nowe = {"tytul": "Czy to, co widać na dashboardzie, jest wzrostem?",
            "wstep": f"Wzrost to dwie rzeczy naraz: więcej pacjentów i lepsza retencja. Sprawdzamy oba warunki osobno, na "
                     f"danych oczyszczonych, porównując {O2_TEKST} z rokiem wcześniej (X 2024 – IX 2025).",
            "werdykt": werdykt, "kafelki": kafelki, "decyzje": decyzje,
            "karty": [pac, ret, go, wy, dash, dalej],
            "zrodlo": "Skąd liczby: " + W0["zrodlo"].replace("Liczby: ", "") + " Runda E: analiza/wyniki/e_merytoryka.txt, "
                      "notatki/e_teksty.md."}
    bloki.append(("wzrost/wstep", {"w": nowe["wstep"]}, [], []))
    return nowe, bloki


def pewnosc(poziom, dopisek=""):
    nazwy = {"wysoka": "Wysoka", "srednia": "Średnia", "niska": "Niska", "test": "Test"}
    p = {"poziom": poziom, "tekst": nazwy[poziom]}
    if dopisek:
        p["dopisek"] = dopisek
    return p


def stare_sekcje(k, pomin=(), zamiany=None, dopisz=None):
    """Dawne sekcje karty pozycji jako bloki szczegółów (podtytuł + punkty), po słowniku i zamianach."""
    out = []
    for s in k["sekcje"]:
        if s["tytul"] in pomin:
            continue
        pk = []
        for p in s["punkty"]:
            p = popraw(p)
            for a, b in (zamiany or {}).items():
                p = re.sub(a, b, p)
            if p.strip():
                pk.append(p)
        if dopisz and s["tytul"] in dopisz:
            pk += dopisz[s["tytul"]]
        if pk:
            out += [podtytul(popraw(s["tytul"])), punkty(pk)]
    return out


def sekcja(k, tytul):
    return [popraw(p) for p in next(s for s in k["sekcje"] if s["tytul"] == tytul)["punkty"]]


def priorytety(V, E, C):
    """„Priorytety” w nowym kształcie (notatki/e_teksty.md, sekcja 2)."""
    P0 = C["priorytety"]
    K0 = {k["nr"]: k for k in P0["karty"]}
    PR0 = {r["nr"]: r for r in P0["przeglad"]}
    bloki = []
    dz, cz = V["dash_zam"], V["czyste_zam"]
    lo, hi = V["p1_lo"], V["p1_hi"]
    na30 = B2.dziesiatki((lo[0] / lo[1] * 30 + hi[0] / hi[1] * 30) / 2)
    tt = V["p11_tt"]
    p7 = V["p7"]
    w100 = [p7[k][5] for k in p7]
    zw = V["p11_zwroty"]
    zl4 = V["zwroty_l4"]
    meta = V["p11_meta"]
    p8 = V["p8"]
    klik = V["klik"]
    k_meta = klik[klik.index.str.startswith("meta_")]
    k_gs = klik[klik.index.str.startswith("gs_")]
    ped = V["pediatra"]
    p10 = V["p10"]
    p10_n = V["p10_n"]
    p12 = V["p12"]
    wd = {nr: PR0[nr]["wdrozenie"] for nr in PR0}

    def pozycja(nr, tytul, wniosek, ile, ile_dop, pew, sekcje_widoczne, szczegoly, fr_dod=None, dodane=None):
        k0 = K0[nr]
        k = {"nr": nr, "tytul": tytul, "wniosek": wniosek,
             "pasek": {"ile": ile, "ile_dopisek": ile_dop, "pewnosc": pew, "wdrozenie": wd[nr]},
             "sekcje": [{"tytul": t, "punkty": p} for t, p in sekcje_widoczne],
             "szczegoly": szczegoly, "linki": k0["linki"], "zrodlo": k0["zrodlo"]}
        if k0.get("tabela"):
            k["tabela"] = popraw(k0["tabela"])
        przeg = {"nr": nr, "co": tytul, "ile": ile, "ile_dopisek": ile_dop, "pewnosc": pew, "wdrozenie": wd[nr]}
        bloki.append((f"priorytety/{nr}", {k_: v for k_, v in k.items() if k_ not in ("tabela",)},
                      [f"c:pozycja:{nr}", f"c:przeglad:{nr}"] + (fr_dod or []), K0[nr].get("_dodane", []) + (dodane or [])))
        return k, przeg

    karty, przeglad = [], []

    def dodaj(para):
        karty.append(para[0])
        przeglad.append(para[1])

    q3_zdanie = r"To kwota tego samego rzędu co spadek marży rok do roku \([^)]*\); wyniku kwartału"
    dodaj(pozycja(
        1, "Naprawić zakładanie konta w Safari na iPhone'ach",
        f"Od 17 marca 2026 nowi pacjenci na iPhone'ach rzadziej kończą zakładanie konta, co kosztuje około "
        f"{liczba(na30)} pierwszych zamówień miesięcznie.",
        f"{zakres(lo[3] / 1000, hi[3] / 1000)} tys. zł",
        f"rocznie, górny scenariusz; w horyzoncie 180 dni {zakres(lo[4] / 1000, hi[4] / 1000)} tys. zł",
        pewnosc("wysoka", "awaria widoczna w danych"),
        [("Dlaczego", [f"Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spadł w Safari na iPhone'ach z "
                       f"{z0(V['safari_krok'][0])}% do {z0(V['safari_krok'][1])}% i nie wraca. W innych przeglądarkach "
                       f"takiego spadku nie ma."]),
         ("Co robimy", ["Powtórzyć rejestrację na iPhonie, przejrzeć logi błędów rejestracji i listę zmian z 16–17 marca "
                        "2026, wdrożyć poprawkę."]),
         ("Po czym poznamy", sekcja(K0[1], "Po czym poznamy"))],
        stare_sekcje(K0[1], pomin=("Po czym poznamy", "Wdrożenie"),
                     zamiany={q3_zdanie: "Wyniku kwartału", r" Wcześniejsza kwota „14–21 tys\. zł”[^.]*\.": ""})))

    k2 = K0[2]
    dodaj(pozycja(
        2, "Oczyścić codzienny raport i dodać alarmy na lejku i zwrotach",
        f"Raport pokazuje wzrost zamówień o {z0(dz[0])}% zamiast {z0(cz[0])}% i nie pokazuje ani marży, ani powrotów kohort.",
        f"0 albo {z0(V['testy_koszt2'] / 1000)} tys. zł", "rocznie bezpośrednio; przede wszystkim warunek pozostałych decyzji",
        pewnosc("wysoka", "oba błędy widoczne w danych"),
        [("Dlaczego", [f"Awaria w Safari trwała {liczba(lo[1])} dni bez alarmu. Alarm na krokach lejka wykryłby ją po kilku "
                       f"dniach; wykrycie po tygodniu ograniczyłoby stratę do {zakres(V['p15'][1], V['p15'][2])} pierwszych "
                       f"zamówień zamiast {zakres(lo[0], hi[0])}."]),
         ("Co robimy", [p for p in sekcja(k2, "Co robimy") if not p.lower().startswith("do pilnowania")]),
         ("Po czym poznamy", sekcja(k2, "Po czym poznamy"))],
        stare_sekcje(k2, pomin=("Co robimy", "Po czym poznamy", "Wdrożenie"),
                     dopisz={"Z danych": [p for p in sekcja(k2, "Co robimy") if p.lower().startswith("do pilnowania")]})))

    k3 = K0[3]
    dodaj(pozycja(
        3, "Wstrzymać kampanię TikTok na L4",
        "Kampania traci na każdym pozyskanym pacjencie według obu reguł przypisania, a jej pacjenci prawie nie wracają.",
        f"+{z0(tt[2] / 1000)} do +{z0(tt[3] / 1000)} tys. zł",
        "rocznie, nawet gdy każdy jej pacjent przyszedł tylko dzięki niej; więcej, gdy część przyszłaby i tak",
        pewnosc("wysoka", "co do znaku"),
        [("Dlaczego", ["Wynik na pacjenta po koszcie pozyskania jest ujemny w obu regułach i po 90, i po 180 dniach, a "
                       "naprawa zwrotów w najlepszym razie doprowadza go do zera."]),
         ("Co robimy", ["Wstrzymać od razu, jako pauzę, którą da się cofnąć w jeden dzień. Naprawy obietnicy i ładowania "
                        "strony sprawdzić najpierw na Mecie; TikTok może wrócić jako mały test, jeśli zadziałają."]),
         ("Po czym poznamy", [p.replace("słaby, darmowy pomiar dodatkowości", "słaby, darmowy pomiar tego, ilu pacjentów "
                                        "przyszłoby i bez kampanii") for p in sekcja(k3, "Po czym poznamy")])],
        stare_sekcje(k3, pomin=("Po czym poznamy", "Wdrożenie"))))

    k4 = K0[4]
    pr = (E["gs_spec_prog_Z1K_90"], E["gs_spec_prog_Z2_90"])
    dodaj(pozycja(
        4, "Wstrzymać kampanię Google Ads na specjalistów do czasu zmiany cennika",
        f"Pozyskanie pacjenta kosztuje około {z0(p7[('Z1K', '90')][2])} zł, a pacjent zostawia w 90 dniach około "
        f"{z0(p7[('Z1K', '90')][3])} zł marży.",
        f"+{z0(min(w100) / 1000)} do +{z0(max(w100) / 1000)} tys. zł",
        f"rocznie, nawet gdy każdy jej pacjent przyszedł tylko dzięki niej; do +{z0(p7[('Z1K', '90')][7] / 1000)} tys. zł, "
        f"gdy przyszliby i bez niej",
        pewnosc("wysoka", "co do znaku"),
        [("Dlaczego", ["Wizyta u specjalisty po cenie katalogowej zostawia ponad koszt lekarza tylko 9–19 zł, więc kampania "
                       "nie ma z czego pokryć kosztu pozyskania (pozycja 10)."]),
         ("Co robimy", ["Wstrzymać. Wrócić po zmianie cennika albo gdy koszt pozyskania nie przekracza marży pacjenta "
                        "w 90 dniach w obu regułach."]),
         ("Po czym poznamy", [
             f"Liczymy wszystkich nowych pacjentów z pierwszą wizytą u specjalisty, ze wszystkich kanałów (w ostatnich 12 "
             f"miesiącach średnio {z0(E['spec_nowi_tydz_2'])} tygodniowo), i marżę całego biznesu po wydatkach, wobec tych "
             f"samych tygodni rok wcześniej, tak jak w teście Mety. Pauza się opłaca, dopóki nowych pacjentów u specjalistów "
             f"ubywa mniej niż około {z0(min(pr) / 52.14)} tygodniowo; kampania przypisuje sobie "
             f"{z0(E['gs_spec_nowi_tydz_z2'])}–{z0(E['gs_spec_nowi_tydz_z1k'])} tygodniowo."])],
        stare_sekcje(k4, pomin=("Po czym poznamy", "Wdrożenie"), dopisz={"Propozycja": [
            f"Próg pauzy = wydatki kampanii w ostatnich 12 miesiącach ({tz(E['gs_spec_wydatki_2'])}) podzielone przez marżę "
            f"jej pacjenta w 90 dniach ({liczba(p7[('Z1K', '90')][3], 1)} zł według przyjętej reguły, "
            f"{liczba(p7[('Z2', '90')][3], 1)} zł według sesji płatności): {liczba(round(pr[0]))} albo {liczba(round(pr[1]))} "
            f"pacjentów rocznie. Kampania przypisuje sobie {liczba(E['gs_spec_nowi_z1k'])} albo {liczba(E['gs_spec_nowi_z2'])} "
            f"nowych pacjentów rocznie. Wszystkich nowych pacjentów z pierwszą wizytą u specjalisty (bez internisty, "
            f"pediatry i psychiatry) było {liczba(E['spec_nowi_2'])} w ostatnich 12 miesiącach i {liczba(E['spec_nowi_1'])} "
            f"rok wcześniej."]})))

    k5 = K0[5]
    pz17 = NIEWIADOMA[18]
    dodaj(pozycja(
        5, "Zmienić obietnicę w reklamach Meta na L4; zasady zwrotów rozważyć osobno",
        f"{z0(zl4.loc['nowe_kampanie', 'proc_zwrot_po_wizycie'])}% wizyt L4 z nowych kampanii kończy się zwrotem pieniędzy, "
        f"wobec {z0(zl4.loc['pozostali', 'proc_zwrot_po_wizycie'])}% u pozostałych pacjentów, a lekarz i tak dostaje "
        f"wynagrodzenie.",
        f"{zakres(zw[7] / 1000, zw[5] / 1000)} tys. zł",
        f"rocznie za samą nową kreację; zmiana zasad zwrotów przy odmowie L4 to osobna decyzja: "
        f"{zakres(zw[8] / 1000, zw[6] / 1000)} tys. zł",
        pewnosc("srednia", "nie znamy powodu zwrotów"),
        [("Dwie różne decyzje", [
            "Nowa kreacja i pytanie przed płatnością („lekarz wystawia L4 tylko przy wskazaniach medycznych”). Uczciwa "
            "obietnica zniechęca część osób, które i tak dostałyby zwrot. Warta "
            f"{zakres(zw[7] / 1000, zw[5] / 1000, 1)} tys. zł rocznie, zależnie od reguły przypisania.",
            "Zmiana zasad zwrotów przy odmowie L4: wizyta zostaje opłacona, bo pacjent dostał konsultację. Warta "
            f"{zakres(zw[8] / 1000, zw[6] / 1000, 1)} tys. zł rocznie, ale to osobna decyzja z ryzykiem prawnym "
            f"i wizerunkowym (Czego nie wiemy, punkt {pz17}).",
            "Obie kwoty to scenariusze tych samych zwrotów, więc się nie sumują. Po wstrzymaniu TikToka dotyczą tylko Mety."]),
         ("Co robimy", ["Najpierw jednodniowe sprawdzenie, co obiecują reklama, strona wejścia i regulamin przy odmowie L4. "
                        "Potem w Mecie losowy podział ruchu na starą i nową kreację. Przy okazji przetestować wysokość kodu "
                        "rabatowego (dziś 20 zł)."]),
         ("Po czym poznamy", sekcja(k5, "Po czym poznamy"))],
        [podtytul("Ile warte, osobno dla dwóch decyzji"), punkty([
            f"Wariant kreacji (uczciwa obietnica zniechęca osoby, które nie dostałyby L4): {tz(zw[0])} w {V['dni']['meta_prosp_l4_szybko']} "
            f"dniach działania kampanii według przyjętej reguły i {tz(zw[2])} według sesji płatności, na pełny rok "
            f"{tz(zw[5])} i {tz(zw[7])}.",
            f"Wariant zasad zwrotów (wizyty, które dziś kończą się zwrotem, zostają opłacone): {tz(zw[1])} i {tz(zw[3])}, "
            f"na pełny rok {tz(zw[6])} i {tz(zw[8])}."])]
        + stare_sekcje(k5, pomin=("Ile warta po wstrzymaniu TikToka (tylko Meta)", "Po czym poznamy", "Wdrożenie"),
                       zamiany={"[Dd]olny wariant zakłada": "Wariant kreacji zakłada",
                                r"[Gg]órny wariant \(„wizyta zostaje opłacona”\)": "Wariant zasad zwrotów („wizyta zostaje opłacona”)"})))

    k6 = K0[6]
    dodaj(pozycja(
        6, "Zdiagnozować poranne opóźnienia internistów, potem przetestować obsadę",
        "Od lutego 2026 około połowy porannych wizyt u internisty zaczyna się ponad 15 minut po terminie; do października "
        "2025 było to 5–7%.",
        f"{zakres(0, p8[3] / 1000)} tys. zł",
        f"rocznie, scenariusz; wariant wąski około {z0((p8[0] + p8[1]) / 2000)} tys. zł; bez kosztu obsady",
        pewnosc("niska", "co do kwoty"),
        [("Dlaczego", ["To jedna z konkretnych hipotez spadku retencji w kanałach działających w obu latach, a pierwszy krok, "
                       "diagnoza, jest tani. W ostatnich 12 miesiącach pacjenci po spóźnionej porannej pierwszej wizycie "
                       "wracają rzadziej niż po punktualnej, a spóźnione wizyty mają dużo niższe oceny (zakładka „Po zakupie”)."]),
         ("Co robimy", sekcja(k6, "Co robimy")),
         ("Po czym poznamy", sekcja(k6, "Po czym poznamy"))],
        stare_sekcje(k6, pomin=("Dlaczego wysoko", "Co robimy", "Po czym poznamy", "Wdrożenie"),
                     zamiany={r" Rano spada powrót po wizytach spóźnionych\.": ""})))

    k7 = K0[7]
    cp = V["crm_powrot"]
    B1 = V["pow_bez_z1k"]
    dodaj(pozycja(
        7, "Wprowadzić komunikację po wizycie, zawsze z losową grupą bez wysyłki",
        "Co siódmy powrót zaczyna się od wejścia z newslettera albo SMS-a, ale nie wiemy, ile z tych zakupów wiadomość "
        "faktycznie wywołała.",
        tz(p12[1]), "za każdy punkt procentowy powrotu w 90 dniach; marża do 180. dnia; scenariusz",
        pewnosc("niska", "co do kwoty"),
        [("Dlaczego", [f"Retencja spada także poza nowymi kampaniami: w 90 dniach wraca {proc(B1['p90_o2'])} pacjentów wobec "
                       f"{proc(B1['p90_o1'])} rok wcześniej. Te {proc(B1['p90_o2'])} to {proc(cp[1], 2)} pacjentów, którzy "
                       f"wrócili w ciągu doby po kliknięciu newslettera albo SMS-a, i {proc(cp[3], 2)}, którzy wrócili inną "
                       f"drogą. To podział tej samej grupy pacjentów, a nie porównanie dwóch grup."]),
         ("Co robimy", sekcja(k7, "Co robimy")),
         ("Po czym poznamy", sekcja(k7, "Po czym poznamy"))],
        [podtytul("Ile warta"), punkty([
            f"Każdy punkt procentowy powrotu w 90 dniach to około {tz(p12[1])} marży rocznie: {liczba(V['nowi'][2])} nowych "
            f"pacjentów × 1% × {liczba(p12[0], 1)} zł, gdzie {liczba(p12[0], 1)} zł to różnica marży do 180. dnia między "
            f"pacjentem, który wrócił w 90 dniach, a takim, który nie wrócił. Bez pacjentów nowych kampanii "
            f"({liczba(V['p12_bez'][0])}) {tz(V['p12_bez'][1])}. To różnica obserwacyjna, a nie zmierzony efekt wiadomości.",
            f"Rok wcześniej podział powrotu wynosił {proc(cp[0], 2)} po wejściu z newslettera albo SMS-a i {proc(cp[2], 2)} "
            f"inną drogą."])]
        + stare_sekcje(k7, pomin=("Ile warta", "Co robimy", "Po czym poznamy", "Wdrożenie"),
                       zamiany={r"Po wejściu z newslettera albo SMS-a wraca [^.]*?powrotów[^.]*\.": ""})))

    k8 = K0[8]
    dodaj(pozycja(
        8, "Sprawdzić ręcznie zakup dla pacjentów zalogowanych od wejścia",
        f"Żadna z {z0(V['zal_sesje'] / 1000)} tys. sesji pacjentów zalogowanych od wejścia nie skończyła się zakupem "
        f"konsultacji; jeden ręczny test pokaże, czy to błąd ścieżki zakupu.",
        f"0 albo {zakres(V['p5'][1] / 1000, V['p5'][0] / 1000)} tys. zł", f"rocznie; wysoki scenariusz {z0(V['p5'][2] / 1000)} tys. zł",
        pewnosc("niska", "dane wskazują raczej na 0 zł"),
        [("Co robimy", ["Zalogować się, wejść ponownie już zalogowanym, spróbować kupić bez ponownego logowania i sprawdzić, "
                        "jakie kroki zapisała analityka."]),
         ("Po czym poznamy", sekcja(k8, "Po czym poznamy"))],
        stare_sekcje(k8, pomin=("Po czym poznamy", "Wdrożenie"))))

    k9 = K0[9]
    dodaj(pozycja(
        9, "Sprawdzić testem w części kraju, czy kampania Meta na L4 się opłaca",
        f"Według reguły przyjętej kampania zarabia {z0(meta[0] / 1000)} tys. zł rocznie, według sesji płatności traci "
        f"{z0(abs(meta[1]) / 1000)} tys. zł, a dane nie mówią, ilu jej pacjentów przyszłoby i bez niej.",
        f"od {z0(-abs(meta[2]) / 1000)} do +{z0(meta[3] / 1000)} tys. zł",
        "rocznie: tyle warta jest decyzja o wyłączeniu, zależnie od tego, ilu pacjentów przyszłoby i bez kampanii",
        pewnosc("test"),
        [("Dlaczego dopiero 9. miejsce", [
            "To największa kwota na liście, ale nie znamy nawet jej znaku, a test w 4–6 tygodni da tylko orientacyjny "
            "wynik. Wcześniej idą pewne straty i tanie kroki, które zespół może zrobić od razu."]),
         ("Co robimy", [
             "Na 4–6 tygodni wyłączyć kampanię w połowie województw, losowo w parach podobnych województw, i porównać "
             f"wszystkich nowych pacjentów oraz marżę. Wyłączamy na stałe, jeśli w województwach bez reklamy ubędzie mniej "
             f"niż około {z0(V['p11_prog'][0])}% pacjentów, których kampania sobie przypisuje (po naprawie zwrotów około "
             f"70%). Przy wyniku niejednoznacznym decyduje oszacowanie punktowe."]),
         ("Po czym poznamy", sekcja(k9, "Po czym poznamy"))],
        stare_sekcje(k9, pomin=("Po czym poznamy", "Wdrożenie"))))

    k10 = K0[10]
    dodaj(pozycja(
        10, "Zmienić cennik specjalistów i warunki TelemediGO u specjalistów",
        "Wizyta u specjalisty zostawia ponad koszt lekarza tylko 9–19 zł, a ze zniżką TelemediGO przynosi stratę.",
        f"{zakres(V['p6_scen'][0] / 1000, V['p6_scen'][2] / 1000)} tys. zł",
        f"rocznie za warunki TelemediGO po pełnym roku; cennik do {z0(V['p14_zl'] / 1000)} tys. zł za każde 10 zł podwyżki, "
        f"górna granica",
        pewnosc("srednia", "kierunek pewny, kwota cennika nie"),
        [("Co robimy", sekcja(k10, "Warianty")),
         ("Po czym poznamy", sekcja(k10, "Po czym poznamy"))],
        stare_sekcje(k10, pomin=("Warianty", "Po czym poznamy", "Wdrożenie"),
                     zamiany={r"\(przy założeniu 33\)": "(założenie oparte na zadaniu; sprawdzenie wrażliwości niżej)"},
                     dopisz={"Z danych": [
                         f"Stawka lekarza 100 zł za wizytę u pediatry to założenie oparte na zadaniu: 25 zł internista, "
                         f"200 zł psychiatra, 100 zł każdy inny specjalista. Sprawdzenie wrażliwości: przy stawce 25 zł, jak "
                         f"u internisty, marża na pacjenta w 90 dniach rośnie o {zakres(min(ped), max(ped), 1)} zł."]})))

    k11 = K0[11]
    dodaj(pozycja(
        11, "Sprawdzić, gdzie znika ruch między kliknięciem reklamy a wejściem na stronę w Meta i TikToku",
        f"Na kliknięcie w Meta przypada {liczba((k_meta.kwartal_min.min() + k_meta.kwartal_max.max()) / 2, 1)} sesji, a w "
        f"Google Ads {liczba((k_gs.kwartal_min.min() + k_gs.kwartal_max.max()) / 2, 1)}; nie wiemy, czy ludzie porzucają "
        f"ładowanie strony, czy panel liczy kliknięcia inaczej.",
        f"0 albo do {z0(V['p9_zl'] / 1000)} tys. zł", "rocznie, górna granica; po wstrzymaniu TikToka mniej",
        pewnosc("niska"),
        [("Po czym poznamy", sekcja(k11, "Po czym poznamy"))],
        stare_sekcje(k11, pomin=("Po czym poznamy", "Wdrożenie"))))

    k12 = K0[12]
    dodaj(pozycja(
        12, "Sprawdzić losowym testem, ile wizyt i powrotów dokłada zniżka TelemediGO",
        "Kupujący TelemediGO wracają częściej, ale nie wiemy, czy to skutek zniżki, czy tego, że kupują ci, którzy i tak "
        "planują wracać.",
        f"koszt {zakres(p10[0] / 1000, p10[1] / 1000)} tys. zł", "zniżki przy niezmienionej liczbie wizyt",
        pewnosc("test"),
        [("Co pokaże", ["Test pokaże wpływ samej zniżki na wizyty, powroty i marżę. Nie pokaże, czy opłaca się oferta za "
                        "89 zł, bo uczestnicy dostają zniżki bez opłaty. Od wyniku zależy, czy program promować, czy "
                        "przebudować razem z pozycją 10."]),
         ("Po czym poznamy", sekcja(k12, "Po czym poznamy"))],
        stare_sekcje(k12, pomin=("Po czym poznamy",), dopisz={"Ile warta": [
            f"Koszt testu ({zakres(p10[0] / 1000, p10[1] / 1000, 1)} tys. zł zniżek dla {liczba(p10_n[0])}–{liczba(p10_n[1])} "
            f"pacjentów w grupie z dostępem) liczymy przy niezmienionej liczbie wizyt; jeśli zniżka doda wizyt, koszt będzie "
            f"wyższy."]},
            zamiany={r"[Dd]ecyduje, czy program promować": "Pokaże, czy zniżka dokłada wizyt, a od tego zależy, czy program promować",
                     r"Dodatkowy koszt testu to około [^.]*zniżek\.": ""})))

    # zasady listy i „czego nie robimy”
    zas = karta(
        "Najpierw pewne straty i pauzy, które da się cofnąć, potem testy",
        wniosek="Kolejność to waga, a nie kalendarz, a każda kwota to osobny scenariusz, więc kwot nie sumujemy.",
        tresc=[punkty([
            "Najpierw pewne straty, które rosną każdego dnia i łatwo je naprawić (pozycje 1 i 2). Potem pauzy, które da się "
            "cofnąć (3 i 4). Potem naprawy, diagnozy i testy (5–10). Na końcu rzeczy o nieznanym znaku albo nieznanej "
            "wartości (11 i 12).",
            "W pierwszym tygodniu zespół może zrobić równolegle pozycje 1, 3 i 4 oraz pierwsze, krótkie kroki pozycji 2, 6, "
            "8 i 11.",
            "Wartość to zmiana marży na rok: przychód z konsultacji po zwrotach i opłaty TelemediGO minus koszt lekarza, "
            "wydatki na kampanie i prowizja afiliacyjna. Rokiem bazowym są ostatnie 12 miesięcy.",
            "Pieniędzy uwolnionych przez pozycje 3 i 4 nie przesuwamy automatycznie do innych kampanii, tylko z testem."])],
        szczegoly=[punkty([popraw(x) for x in P0["zasady"]]),
                   akapit(popraw(P0["definicje"]).replace("Sesja płatności = reguła porównawcza.",
                                                          "Sesja płatności = druga reguła, do porównania (reguła porównawcza)."))])
    bloki.append(("priorytety/zasady", zas, ["c:zasady"], []))
    nie = karta(
        "Nie robimy teraz rzeczy bez podstaw w danych albo bez testu",
        tresc=[punkty([
            f"Kampanii o zgodę marketingową pacjentów nowych kampanii: w najlepszym razie {liczba(V['zgoda_1900'] / 1000, 1)} "
            f"tys. zł rocznie.",
            "Osobnej naprawy przeglądarek w aplikacjach w reklamach do nowych osób: w tej samej kampanii płacą tak samo jak "
            "zwykłe.",
            "Mocniejszej sprzedaży i odnowień TelemediGO: dopiero po teście z pozycji 12.",
            "Przesuwania uwolnionego budżetu do innych kampanii bez testu."])],
        szczegoly=[punkty([popraw(x) for x in P0["nie_robimy"]])])
    bloki.append(("priorytety/nie_robimy", nie, ["c:nie_robimy"], []))
    nowe = {"tytul": "Priorytety: co robimy po kolei",
            "wstep": "Lista od najważniejszej pozycji. Przy każdej: dlaczego, co robimy, ile jest warta w złotych marży na rok, "
                     "po czym poznamy, że zadziałała, i ile zajmie wdrożenie. Pełne rachunki i założenia są w szczegółach "
                     "każdej karty.",
            "przeglad": przeglad, "zasady": zas, "karty": karty, "nie_robimy": nie, "zrodlo": P0["zrodlo"]}
    bloki.append(("priorytety/wstep", {"w": nowe["wstep"]}, [], []))
    return nowe, bloki


def niewiadome(V, E, C):
    """„Czego nie wiemy”: słownik, nowe numery (bez dawnej pozycji 13) i trzy przeredagowane wiersze."""
    N0 = C["niewiadome"]
    wiersze, bloki = [], []
    nowe_teksty = {
        1: {"co": "Ilu pacjentów nowych kampanii na L4 przyszłoby i bez nich"},
        2: {"co": "Ilu pacjentów kampanii bez kodu rabatowego (Google Ads ogólne, Meta „lekarz online”) przyszłoby i bez "
                  "reklamy",
            "dlaczego": "znak wyniku tych kampanii zależy od reguły przypisania, a żadna reguła nie mówi, ilu pacjentów "
                        "kampania naprawdę dokłada",
            "test": "ten sam test z grupą bez reklamy; mierzy przyrost pacjentów niezależnie od reguły przypisania, więc nie "
                    "trzeba wybierać reguły"},
        3: {"dlaczego": "po wstrzymaniu TikToka dotyczy tylko Meta: od niego zależy, ile da nowa kreacja (10,7–18,1 tys. zł "
                        "rocznie) i czy potrzebna jest zmiana zasad zwrotów (26,7–46,5 tys. zł rocznie; pozycja 5)"},
        18: {"dlaczego": "zmiana zasad zwrotów z pozycji 5 to osobna decyzja, która wymaga zmiany regulaminu i oceny ryzyka "
                         "prawnego"},
        8: {"co": "Ile wizyt i powrotów dokłada zniżka TelemediGO",
            "dlaczego": "od tego zależy, czy program promować; test pokaże wpływ samej zniżki, ale nie opłacalność oferty za "
                        "89 zł",
            "test": "losowy, bezpłatny dostęp do zniżek (pozycja 12)"},
    }
    for w in N0["wiersze"]:
        if w["nr"] == 13:
            continue
        n = {k: (popraw(v) if isinstance(v, str) else v) for k, v in w.items() if k != "_dodane"}
        n.update(nowe_teksty.get(w["nr"], {}))
        if w["nr"] == 1:
            n["dlaczego"] = n["dlaczego"].replace("pacjentów dodatkowych", "pacjentów, którzy bez kampanii by nie przyszli")
            n["test"] = n["test"].replace("rozpozna tylko niską dodatkowość",
                                          "rozpozna tylko sytuację, w której większość pacjentów przyszłaby i bez kampanii")
        n["nr"] = NIEWIADOMA[w["nr"]]
        n["co"] = re.sub(r" \(dodane 2026-10-21\)$", "", n["co"])
        wiersze.append(n)
        bloki.append((f"niewiadome/{w['nr']}", n, [f"c:niewiadoma:{w['nr']}"], w.get("_dodane", [])))
    nowe = {"tytul": "Czego z tych danych nie wiemy",
            "wstep": "Rzeczy, których te dane nie rozstrzygają, i test albo dane, które je domkną. Numer pozycji listy "
                     "priorytetów prowadzi do karty, której kwota od tego zależy.",
            "wiersze": wiersze, "zrodlo": N0["zrodlo"]}
    return nowe, bloki


def teksty_c(V, E, C):
    """Nowe „Czy to wzrost”, „Priorytety” i „Czego nie wiemy”. C = dane w dotychczasowym kształcie (z b2_eksport_c).
    Nowe klucze dopisujemy do dotychczasowych, żeby strona działała też przed przebudową rysowania.
    Zwraca (C, bloki do kontroli)."""
    bloki = []
    wz, b = wzrost(V, E, C)
    bloki += b
    pr, b = priorytety(V, E, C)
    bloki += b
    nw, b = niewiadome(V, E, C)
    bloki += b
    C = dict(C)
    C["wzrost"] = {**C["wzrost"], **wz}
    C["priorytety"] = {**C["priorytety"], **pr}
    C["niewiadome"] = {**C["niewiadome"], **nw}
    return C, bloki


def karty_lejka(nag, V, E):
    """Karty nagłówka lejka (D.P.lejek_naglowek.karta, .naprawy_karty, .osobne_karta; notatki/e_teksty.md, sekcja 4).
    Dopisuje je do `nag` w miejscu i zwraca wynik kontroli liczb."""
    M = {r["mies"]: r for r in E["lj_miesiace"]}
    MK = {r["mies"]: r for r in E["lj_miesiace_kampanie"]}
    zm = lambda ms: [abs(M[m]["zmiana_rr_pkt"]) for m in ms]  # noqa: E731
    m_a = ["2025-10", "2025-11", "2025-12", "2026-01"]
    m_b = ["2026-02", "2026-03"]
    m_c = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]
    udz_c = [MK[m]["udzial_sesji_nowe_kampanie"] for m in m_c]
    nk1, nk2 = E["lj_nie_kupowal_1_konw"], E["lj_nie_kupowal_2_konw"]
    tab_m = tabela(["Miesiąc", "Ostatnie 12 miesięcy", "Rok wcześniej", "Zmiana", "Udział sesji nowych kampanii"],
                   [wiersz(B2.MIESIACE_RZ[int(m[5:]) - 1] + " " + m[:4],
                           [proc(M[m]["konwersja"], 2), proc(M[str(int(m[:4]) - 1) + m[4:]]["konwersja"], 2),
                            zmiana(f"{zn(M[m]['zmiana_rr_pkt'], 2)} pkt", M[m]["zmiana_rr_pkt"]),
                            proc(MK[m]["udzial_sesji_nowe_kampanie"]) if MK[m]["udzial_sesji_nowe_kampanie"] == MK[m]["udzial_sesji_nowe_kampanie"] else "—"])
                    for m in m_a + m_b + m_c],
                   tytul="Osoby, które jeszcze nie kupowały: sesja do płatności, miesiąc po miesiącu")
    dod_tab = [liczba(M[m][k], 2) for m in m_a + m_b + m_c for k in ("konwersja",)] + [liczba(M[str(int(m[:4]) - 1) + m[4:]]["konwersja"], 2) for m in m_a + m_b + m_c] + \
              [zn(M[m]["zmiana_rr_pkt"], 2) for m in m_a + m_b + m_c] + \
              [liczba(MK[m]["udzial_sesji_nowe_kampanie"], 1) for m in m_a + m_b + m_c
               if MK[m]["udzial_sesji_nowe_kampanie"] == MK[m]["udzial_sesji_nowe_kampanie"]]
    stare = [popraw(z) for z in nag["zdania"]]
    karta_n = karta(
        "Od lutego 2026 płaci coraz mniej nowych osób, bo przybywa ruchu z nowych kampanii na L4",
        wniosek=f"Wśród osób, które jeszcze nie kupowały, płaci {proc(nk2)} sesji, a rok wcześniej płaciło {proc(nk1)}.",
        tresc=[punkty([
            f"Od października 2025 do stycznia 2026 konwersja była o {zakres(min(zm(m_a)), max(zm(m_a)), 1)} punktu "
            f"procentowego niższa niż rok wcześniej. W lutym i marcu 2026 o {zakres(min(zm(m_b)), max(zm(m_b)), 1)} punktu, a "
            f"od kwietnia 2026 o {zakres(min(zm(m_c)), max(zm(m_c)), 1)} punktu. W lutym 2026 ruszył TikTok na L4, a sesje "
            f"nowych kampanii przekroczyły 30% ruchu nowych osób ({proc(MK['2026-02']['udzial_sesji_nowe_kampanie'])}); od "
            f"kwietnia to {zakres(min(udz_c), max(udz_c))}%.",
            f"Sesje nowych kampanii płacą w {proc(E['lj_kampania_nowe_kampanie_2_konw'])}, mniej więcej o połowę rzadziej niż "
            f"pozostałe. Bez nich konwersja nowych osób nie spada: {proc(E['lj_nk_bez_nowych_2'])} wobec "
            f"{proc(E['lj_nk_bez_nowych_1'])} rok wcześniej.",
            "Dwie rzeczy na stronie trzeba naprawić niezależnie od struktury ruchu: zakładanie konta w Safari na iPhone'ach "
            "od 17 marca 2026 i niższą konwersję przeglądarek w aplikacjach w ruchu osób, które znają już stronę (karty niżej)."])],
        zastrzezenie="Niższa konwersja całości nie znaczy, że nowe kampanie nie przynoszą pacjentów; nie wiemy, ilu ich "
                     "pacjentów przyszłoby i bez nich.",
        szczegoly=[punkty([
            f"Osoby, które jeszcze nie kupowały: {liczba(E['lj_nie_kupowal_1_sesje'])} sesji i "
            f"{liczba(E['lj_nie_kupowal_1_platnosci'])} płatności rok wcześniej, {liczba(E['lj_nie_kupowal_2_sesje'])} sesji i "
            f"{liczba(E['lj_nie_kupowal_2_platnosci'])} płatności w ostatnich 12 miesiącach. Najbardziej pogorszyło się "
            f"przejście do wyboru usługi (z {proc(E['lj_nie_kupowal_1_p_k1'])} do {proc(E['lj_nie_kupowal_2_p_k1'])} sesji) i "
            f"krok konta po wyborze terminu (z {proc(E['lj_nie_kupowal_1_p_k3'])} do {proc(E['lj_nie_kupowal_2_p_k3'])}).",
            f"Wszystkie sesje, także osób, które już kupowały (płacą w {proc(E['lj_kupowal_wczesniej_1_konw'])} i "
            f"{proc(E['lj_kupowal_wczesniej_2_konw'])} sesji): {proc(nag['konw'][0])} rok wcześniej ({liczba(nag['sesje'][0])} "
            f"sesji, {liczba(nag['platnosci'][0])} płatności) i {proc(nag['konw'][1])} w ostatnich 12 miesiącach "
            f"({liczba(nag['sesje'][1])} sesji, {liczba(nag['platnosci'][1])} płatności).",
            f"Rozkład zmiany konwersji osób, które jeszcze nie kupowały, według kampanii: zmiana struktury ruchu "
            f"{zn(E['lj_nk_rozklad_kampania_struktura'], 2)} punktu, zmiana w obrębie kampanii "
            f"{zn(E['lj_nk_rozklad_kampania_wewnatrz'], 2)} punktu (rozkład opisowy; nowe kampanie nie mają roku wcześniej, "
            f"więc liczą się w całości do struktury).",
            "Wszystkie sesje razem: " + " ".join(stare[1:3])]), tab_m],
        linki=[link("Lejek: osoby, które jeszcze nie kupowały, według kampanii",
                    "#lejek?typ=zwykla&pac=nie_kupowal&podz=kampania&krok=k5&wygl=28")],
        zrodlo="analiza/a5p_lejek.py → analiza/wyniki/a5p_lejek_dzienny.csv.gz; analiza/e_merytoryka.py → "
               "analiza/wyniki/e_merytoryka.txt (punkt 4).")
    s = nag["safari"]
    nap0, nap1 = nag["naprawy"]
    safari = karta(
        "Safari na iPhone'ach: od 17 marca 2026 nowi pacjenci rzadziej kończą zakładanie konta",
        znacznik=znacznik("Do naprawy", "zle"),
        wniosek=f"Krok konta po wyborze terminu spadł z {z0(s['przed_proc'])}% do {z0(s['po60_proc'])}% w 60 dniach po "
                f"awarii, a w innych przeglądarkach prawie się nie zmienił.",
        tresc=[punkty([nap0["tekst"].split(". Krok konta")[0] + ". " + "Szacunek:" + nap0["tekst"].split("Szacunek:")[1]])],
        szczegoly=[akapit(popraw(nap0["tekst"]))],
        linki=[link("Pokaż w lejku", nap0["link"])], zrodlo="analiza/a5p_zdarzenia.py → analiza/wyniki/a5p_zdarzenia.txt.")
    P = {r["wartosc"] + str(r["okres"]): r for r in E["nk_przegl_kroki_wartosc"]}
    apl = [P[k] for k in P if k[:-1] in ("Instagram", "Facebook", "TikTok")]
    zw_ = [P[k] for k in P if k[:-1] in ("Chrome", "Safari")]
    rz = lambda L, kol, m=1: zakres(min(r[kol] for r in L), max(r[kol] for r in L), m)  # noqa: E731
    stary = popraw(nap1["tekst"])
    stary = stary[:stary.index("Dla porównania")] if "Dla porównania" in stary else stary
    przegl = karta(
        "Przeglądarki w aplikacjach: w reklamach do nowych osób płacą jak zwykłe, w ruchu osób, które znają stronę, rzadziej",
        znacznik=znacznik("Do sprawdzenia", "uwaga"),
        wniosek="W remarketingu Meta, Google Ads na markę i wejściach bezpośrednich sesje w przeglądarkach w aplikacjach "
                "płacą o 4–12 punktów procentowych rzadziej niż zwykłe w tej samej kampanii.",
        tresc=[punkty(["W kampaniach Meta i TikTok na L4 takiej różnicy nie ma, więc niska konwersja tych kampanii nie "
                       "wynika wyraźnie z przeglądarki."])],
        zastrzezenie=f"To porównanie obserwacyjne: nie rozdziela wpływu przeglądarki od tego, kto z niej korzysta (Czego nie "
                     f"wiemy, punkt {NIEWIADOMA[19]}).",
        szczegoly=[akapit(stary.strip()), akapit(
            f"Dla porównania cały ruch osób, które jeszcze nie kupowały (wszystkie kampanie razem): przeglądarki w aplikacjach "
            f"płacą w obu latach w {rz(apl, 'platnosc_z_sesji')}% sesji, a Chrome i Safari w {rz(zw_, 'platnosc_z_sesji')}%. "
            f"Usługę wybiera {rz(apl, 'usluga')}% sesji w przeglądarkach w aplikacjach (Chrome i Safari "
            f"{rz(zw_, 'usluga')}%), termin {rz(apl, 'termin_z_uslugi')}% tych, które wybrały usługę (wobec "
            f"{rz(zw_, 'termin_z_uslugi')}%), a krok konta {rz(apl, 'konto_z_terminu')}% tych, które wybrały termin (wobec "
            f"{rz(zw_, 'konto_z_terminu')}%; najniżej Safari po awarii).")],
        linki=[link("Pokaż w lejku", nap1["link"])], zrodlo="analiza/d_kampanie.py → analiza/wyniki/d_kampanie.txt (punkt 1); "
                                                           "analiza/wyniki/e_merytoryka.txt (punkt 5c).")
    osobne = karta("Sesje poza lejkiem głównym", tresc=[akapit(popraw(z)) for z in nag["osobne"]])
    nag["karta"] = karta_n
    nag["naprawy_karty"] = [safari, przegl]
    nag["osobne_karta"] = osobne
    return kontrola([("lejek/naglowek", karta_n, ["d:Rozkład zmiany"], dod_tab),
                     ("lejek/safari", safari, [], []),
                     ("lejek/przegladarki", przegl, ["d:Przeglądarki wbudowane"], []),
                     ("lejek/osobne", osobne, ["d:Konta bez zakupu"], [])])
