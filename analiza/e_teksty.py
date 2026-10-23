"""E — teksty strony w nowym kształcie karty (notatki/e_runda.md, punkt 3), runda „merytoryka, język, wygląd”.

Ten moduł ma dwie części:
  1. wspólne narzędzia dla nowych tekstów (używa ich też analiza/e_teksty_zakladki.py): budowa kart i bloków, słownik
     (okres 1 → rok wcześniej itd.), nowe numery niewiadomych po usunięciu dawnej pozycji 13, kontrola liczb;
  2. teksty zakładek „Czy to wzrost”, „Priorytety”, „Czego nie wiemy” i nagłówka lejka (sesja prowadząca).

Zasada liczb bez zmian: żadnej liczby wpisanej ręcznie. Liczby przychodzą z raportów (przez b2_eksport_c.wartosci, V)
i z analiza/wyniki/e_merytoryka.json oraz e_poprawki.json (razem E; druga lista poprawek Kuby, 2026-10-22).
Jedna para nazw reguły przypisania w całym narzędziu: „według pierwszego wejścia” i „według sesji z płatnością”
(funkcje regula() i nazwy(), stosowane na końcu do wszystkich tekstów). Kontrola: każda liczba w tekstach karty musi stać we fragmencie notatki
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
    """Liczby części 1 (e_merytoryka.json) i drugiej listy poprawek Kuby (e_poprawki.json, klucze bez kolizji)."""
    with open(os.path.join(WYNIKI, "e_merytoryka.json"), encoding="utf-8") as f:
        E = json.load(f)
    with open(os.path.join(WYNIKI, "e_poprawki.json"), encoding="utf-8") as f:
        P = json.load(f)
    assert not set(P) & set(E), "klucze e_poprawki.json powtarzają klucze e_merytoryka.json"
    E.update(P)
    return E


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


def zmiana_wydatkow(r, z_wartoscia=False):
    """Komórka ze zmianą wydatków na kampanie rok do roku w procentach (trzecia lista Kuby, punkt 2), liczona z ilorazu
    wydatków kwartału i tego samego kwartału rok wcześniej (e_merytoryka.json, kwartaly). Wzrost wydatków ma stan
    „uwaga”, jak kafelek o wydatkach w „Czy to wzrost”: sam wzrost nie jest zły, zły jest wzrost szybszy niż marża."""
    w = 100 * (r["wydatki_razy"] - 1)
    assert abs(round(w, 1) - r["wydatki_rr"]) < 1e-9, "zmiana wydatków niezgodna z e_merytoryka.json (wydatki_rr)"
    k = zmiana(f"{zn(w)}%", w, lepiej_gdy_rosnie=False, pod=tz(r["wydatki"]) if z_wartoscia else None)
    if k["zmiana"] == "wzrost":
        k["stan"] = "uwaga"
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


# Jedna para nazw reguły przypisania źródła w całym narzędziu (druga lista Kuby, punkt 9): „według pierwszego wejścia”
# i „według sesji z płatnością”. Zamiany są idempotentne, więc można je stosować więcej niż raz (w słowniku i na końcu).
REGULY = [
    (r"których przyjęta reguła przypisuje nowym kampaniom, a sesja płatności innym kanałom",
     "którzy według pierwszego wejścia należą do nowych kampanii, a według sesji z płatnością do innych kanałów"),
    (r"Według drugiej reguły źródła, czyli sesji płatności,", "Według sesji z płatnością"),
    (r"Według drugiej reguły \(sesja płatności\)", "Według sesji z płatnością"),
    # runda F, P9: zbiorcza nazwa to „reguła przypisania”; słowo „podział” zostaje dla rozkładu spadku i wymiaru filtra
    (r"Druga reguła \(sesja płatności\) daje", "Reguła sesji z płatnością daje"),
    (r"\bprzyjęta reguła z definicji", "reguła pierwszego wejścia z definicji"),
    (r"\bsesja płatności przypisuje", "reguła sesji z płatnością przypisuje"),
    (r"trzymamy się (?:przyjętej reguły|reguły przyjętej)", "liczymy według pierwszego wejścia"),
    (r"\bpacjentów reguły przyjętej\b", "pacjentów według pierwszego wejścia"),
    (r"\b([Ww])edług (?:przyjętej reguły(?: źródła)?|reguły przyjętej|naszej reguły)", r"\1edług pierwszego wejścia"),
    (r"\b([Ww])edług sesji płatności", r"\1edług sesji z płatnością"),
    (r"\((?:przyjęta reguła(?: źródła)?|reguła przyjęta)([,);])", r"(według pierwszego wejścia\1"),
    (r"\(sesja płatności([,);])", r"(według sesji z płatnością\1"),
    (r"\bPrzyjęta reguła, (\d+) dni", r"Według pierwszego wejścia, \1 dni"),
    (r"\bSesja płatności, (\d+) dni", r"Według sesji z płatnością, \1 dni"),
    (r", przyjęta reguła\)", ", według pierwszego wejścia)"),
]


def regula(t):
    for a, b in REGULY:
        t = re.sub(a, b, t)
    return t


def nazwy(obj):
    """Nazwy reguły przypisania we wszystkich napisach struktury (bez odnośników i pól technicznych)."""
    if isinstance(obj, str):
        return regula(obj)
    if isinstance(obj, list):
        return [nazwy(x) for x in obj]
    if isinstance(obj, dict):
        return {k: (v if k in ("href", "zrodlo", "id", "poziom", "stan", "zmiana", "typ", "link") else nazwy(v))
                for k, v in obj.items()}
    return obj


def slownik(t):
    for a, b in SLOWNIK:
        t = re.sub(a, b, t)
    return przenumeruj(regula(t))


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


def odm(n, f1, f2, f5):
    """Liczba całkowita z rzeczownikiem w poprawnej formie (1 / 2–4 / 5+): odm(1044, 'zwrot', 'zwroty', 'zwrotów')."""
    n = int(n)
    forma = f1 if n == 1 else f2 if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14) else f5
    return f"{liczba(n)} {forma}"


def wczytaj_g():
    """Liczby nowego werdyktu pierwszej zakładki (runda G, wątek Kuby z 2026-10-23): analiza/g_werdykt.py →
    analiza/wyniki/g_werdykt.json (G1 przyrost pacjentów, G2 i G3 wynik na pacjencie po koszcie pozyskania, G4 rozbicie
    przyrostu marży)."""
    with open(os.path.join(WYNIKI, "g_werdykt.json"), encoding="utf-8") as f:
        return json.load(f)


RZYMSKIE = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")


def miesiac_rz(okres):
    """'2026-04' → 'IV 2026' (miesiąc kohorty w tabeli i na wykresie)."""
    r, m = okres.split("-")
    return f"{RZYMSKIE[int(m) - 1]} {r}"


def wzrost(V, E, C):
    """„Czy to wzrost” od nowa (runda G, wątek Kuby z 2026-10-23; szkic: notatki/e_teksty.md, sekcja 1). Werdykt odpowiada
    najpierw, dlaczego „Nie”, choć marża po wszystkich kosztach rośnie: przyrost pacjentów dały dwie nowe kampanie na L4,
    na ich pacjencie po koszcie pozyskania prawie nic nie zostaje, a marża rośnie dzięki pacjentom z pierwszego roku. Pod
    werdyktem trzy linijki (więcej pacjentów, lepsza retencja, więcej zarabiamy), dwa pojęcia i cztery kafelki, dalej osiem
    kroków: pytanie w nagłówku, odpowiedź w jednym zdaniu, co to znaczy dla biznesu, szczegóły zwinięte. TelemediGO jako
    osobna karta na końcu. C = dawne dane zakładki (do przeniesienia zdań)."""
    W0 = C["wzrost"]
    G = wczytaj_g()
    n1, n2 = V["nowi"][1], V["nowi"][2]
    wz = V["w1_zm"]
    W, B1, B2_, NZ = V["pow_wszyscy"], V["pow_bez_z1k"], V["pow_bez_z2"], V["pow_nowe_z1k"]
    Dd = V["D"]
    kw = E["kwartaly"]
    q3 = kw[-1]
    q3t = B2.q3_teksty(V)
    zaks = q3t["safari_zaks"]
    bloki = []

    # ---------------------------------------------------------------- liczby rundy G i ich zgodność z dotychczasowymi
    g1, g4 = G["g1"], G["g4"]
    assert (g1["nowi_o1"], g1["nowi_o2"], g1["nowe_z1k"]) == (n1, n2, V["nowe_7268"]), "g_werdykt.json niezgodny z W1"
    assert abs(g4["marza_o1"] - E["rok_marza_1"]) < 1 and abs(g4["marza_o2"] - E["rok_marza_2"]) < 1, "G4 niezgodny z W3"
    assert abs(g4["przyrost_proc"] - E["rok_marza_zmiana_proc"]) < 0.05

    def g2(reg, grupy, okres, okno=180):
        return next(r for r in G["g2"]["okno"]
                    if (r["regula"], r["grupy"], r["okres"], r["okno"]) == (reg, grupy, okres, okno))

    def rocz(reg, grupy, okres):
        return next(r for r in G["g2"]["rocznik"] if (r["regula"], r["grupy"], r["okres"]) == (reg, grupy, okres))

    def g3(kamp, reg, poziom):
        return sorted((r for r in G["g3"]["tabela"] if (r["kampanie"], r["regula"], r["poziom"]) == (kamp, reg, poziom)),
                      key=lambda r: r["okres"])

    L4, P1, P2 = g2("Z1K", "1", 2), g2("Z1K", "2", 1), g2("Z1K", "2", 2)
    L4z2, P1z2, P2z2 = g2("Z2", "1", 2), g2("Z2", "2", 1), g2("Z2", "2", 2)
    AF1, AF2 = g2("Z1K", "3", 1), g2("Z1K", "3", 2)
    R_L4, R_P1, R_P2 = rocz("Z1K", "1", 2), rocz("Z1K", "2", 1), rocz("Z1K", "2", 2)
    m1 = g3("razem", "Z1K", "miesiac")
    m2 = {r["okres"]: r for r in g3("razem", "Z2", "miesiac")}
    Q = {r["okres"]: r for r in g3("razem", "Z1K", "kwartal")}
    Qz2 = {r["okres"]: r for r in g3("razem", "Z2", "kwartal")}
    Qt = {r["okres"]: r for r in g3("tiktok", "Z1K", "kwartal")}
    Qm = {r["okres"]: r for r in g3("meta", "Z1K", "kwartal")}
    PU = G["g3"]["pierwszy_ujemny"]
    zima = [r for r in m1 if "2025-11" <= r["okres"] <= "2026-02"]
    wiosna = [r for r in m1 if r["okres"] >= "2026-04"]
    wios_z2 = [m2[r["okres"]]["wynik"] for r in wiosna]
    prz = G["g3"]["przyrosty"]["razem_Z1K"]["przyrost_do_180"]
    prz_od, prz_do = min(prz[k] for k in ("90", "30", "0")), max(prz[k] for k in ("90", "30", "0"))
    gr180 = G["g2"]["granica_180"]
    udz = g1["udzial_nowych_w_przyroscie_z1k"]
    udz_b = g4["baza_udzial_w_przyroscie_proc"]
    grupy1 = {(r["regula"], r["grupa"]): r for r in g1["grupy"]}
    pp, bz, af = (grupy1[("Z1K", g)] for g in ("2_pozostale_platne", "4_bezplatne", "3_afiliacja_ranking"))
    pod = {(r["regula"], r["okres"]): r for r in g4["podzial"]}
    # zdania werdyktu i kroków wymagają tych kierunków (inaczej trzeba zmienić tekst, a nie liczbę)
    assert udz > 80 and udz_b > 80, "„prawie cały” i „prawie wyłącznie” wymagają udziału ponad 80%"
    assert L4["wynik"] > 0 and L4["wynik"] < P2["wynik"] / 3, "„prawie nic nie zostaje” wobec pozostałych kampanii płatnych"
    for g_ in (L4, P2):   # krok 4: marża minus koszt z jednym miejscem po przecinku = podany wynik (uwaga Kuby)
        assert abs(round(g_["marza"], 1) - round(g_["koszt_pozysk"], 1) - round(g_["wynik"], 1)) < 1e-9, g_
    assert abs(Q["2026Q2"]["wynik"]) < 1 and abs(Q["2026Q3"]["wynik"]) < 1, "„od wiosny wychodzimy na zero” (II i III kwartał)"
    assert all(abs(r["wynik"]) < 5 for r in wiosna), "od kwietnia każdy miesiąc blisko zera"
    assert PU["meta_Z1K"]["pierwszy_ujemny"] is None and Qm["2026Q3"]["wynik"] > 0, "Meta na L4 na plusie w każdym miesiącu"
    assert PU["tiktok_Z1K"]["ujemny_w_kazdym_miesiacu_od"] == "2026-03" and Qt["2026Q2"]["wynik"] < 0, "TikTok traci od marca"
    assert PU["razem_Z2"]["ujemny_w_kazdym_miesiacu_od"] == "2025-12" and all(x < 0 for x in wios_z2), "sesja z płatnością: od grudnia"
    assert B1["p90_o2"] < W["p90_o1"], "„rzadziej wracają też pacjenci spoza nowych kampanii”"
    assert g4["wlasni_zmiana_proc"] > 0 and g4["wlasni_na_pacjenta_o2"] < g4["wlasni_na_pacjenta_o1"]
    assert Q["2025Q4"]["wynik"] > 1 and Q["2026Q1"]["wynik"] > 1
    bb = {k: Dd[f"marza_bez_bazy_zmiana_proc_{k}"] for k in ("2025_q4", "2026_q1", "2026_q2", "2026_q3")}
    assert bb["2025_q4"] > 0 and bb["2026_q1"] > 0 and bb["2026_q2"] < 0 and bb["2026_q3"] < 0, "„rosła … spadła”"

    # ---------------------------------------------------------------- werdykt
    werdykt = {
        "znacznik": znacznik("Nie", "zle"),
        # zdanie dodane na prośbę Kuby (2026-10-23) po recenzjach; na stronie jako nagłówek werdyktu nad zdaniem głównym
        "naglowek": "Nie: pacjentów przybywa, ale wracają rzadziej.",
        "tekst": f"Prawie cały przyrost pacjentów ({z0(udz)}%) to pacjenci dwóch nowych kampanii na L4, a na ich pacjencie po "
                 f"koszcie pozyskania prawie nic nie zostaje: {z0(L4['wynik'])} zł w ciągu 180 dni wobec {z0(P2['wynik'])} zł "
                 f"na pacjencie pozostałych kampanii płatnych, a na pacjentach pozyskanych od wiosny szacunkowo wychodzimy na "
                 f"zero. Marża po wszystkich kosztach wzrosła o {z0(g4['przyrost_proc'])}%, w {z0(udz_b)}% dzięki zakupom "
                 f"pacjentów pozyskanych w pierwszym roku. Pacjenci pozyskani w ostatnich 12 miesiącach zarobili w roku "
                 f"pozyskania, po kosztach kampanii, tylko o {z0(g4['wlasni_zmiana_proc'])}% więcej niż ci pozyskani rok "
                 f"wcześniej, choć było ich o {z0(wz[0])}% więcej.",
        "linie": [
            {"etykieta": "Więcej pacjentów", "znacznik": znacznik("Tak, ale", "uwaga"),
             "tekst": f"Nowych pacjentów jest o {z0(wz[0])}% więcej niż rok wcześniej, ale bez dwóch nowych kampanii na L4 "
                      f"tylko o {z0(wz[1])}%."},
            {"etykieta": "Lepsza retencja", "znacznik": znacznik("Nie", "zle"),
             "tekst": f"W ciągu 90 dni wraca {z0(W['p90_o2'])}% nowych pacjentów, a rok wcześniej wracało "
                      f"{z0(W['p90_o1'])}%; rzadziej wracają też pacjenci spoza nowych kampanii."},
            {"etykieta": "Więcej zarabiamy", "znacznik": znacznik("Tak, ale", "uwaga"),
             "tekst": f"Marża po wszystkich kosztach wzrosła z {z0(g4['marza_o1'] / 1000)} do {z0(g4['marza_o2'] / 1000)} "
                      f"tys. zł, ale {z0(udz_b)}% tego przyrostu to kolejne zakupy pacjentów pozyskanych w pierwszym roku, a "
                      f"wynik pacjentów pozyskanych w danym roku wzrósł tylko o {z0(g4['wlasni_zmiana_proc'])}%."},
        ],
        "pojecia": [
            {"nazwa": "Marża",
             "tekst": "to, co zostaje z zapłaty pacjenta po zwrotach i po wynagrodzeniu lekarza, razem z opłatą za "
                      "TelemediGO. Marża po wszystkich kosztach odejmuje do tego wydatki na kampanie i prowizję afiliacyjną."},
            {"nazwa": "Koszt pozyskania",
             "tekst": "wydatki na kampanię podzielone przez liczbę nowych pacjentów, którzy z niej przyszli. „Zostaje na "
                      "pacjencie” to jego marża w ciągu 180 dni od pierwszego zakupu minus koszt jego pozyskania."},
            {"nazwa": "Reguły przypisania",
             "tekst": "pacjenta przypisujemy do kampanii według pierwszego wejścia na stronę (tak liczymy w całym "
                      "narzędziu) albo według sesji, w której zapłacił. Odpowiedź „Nie” jest taka sama przy obu regułach."},
        ],
        "zastrzezenie": "Nie wiemy, ilu pacjentów nowych kampanii przyszłoby i bez reklamy. Odpowie na to test z pozycji 9 "
                        "listy priorytetów: wyłączenie kampanii Meta na L4 na 4–6 tygodni w losowej połowie województw i "
                        "porównanie wszystkich nowych pacjentów z drugą połową.",
        "zastrzezenie_link": link("Priorytety: pozycja 9, test w części kraju", "#priorytety?p=9"),
    }
    kafelki = [
        {"liczba": f"{z0(udz)}%", "podpis": "przyrostu nowych pacjentów to pacjenci dwóch nowych kampanii na L4",
         "dopisek": f"według sesji z płatnością {z0(g1['udzial_nowych_w_przyroscie_z2'])}%", "stan": "uwaga"},
        {"liczba": f"{z0(L4['wynik'])} zł", "podpis": "zostaje w ciągu 180 dni na pacjencie nowych kampanii na L4 po koszcie "
                                                       "pozyskania",
         "dopisek": f"pozostałe kampanie płatne: {z0(P2['wynik'])} zł", "stan": "zle"},
        {"liczba": f"{z0(W['p90_o2'])}%", "podpis": "nowych pacjentów wraca w ciągu 90 dni",
         "dopisek": f"rok wcześniej {z0(W['p90_o1'])}%", "zmiana": "spadek", "stan": "zle"},
        {"liczba": f"{z0(udz_b)}%", "podpis": "przyrostu marży to zakupy pacjentów z pierwszego roku",
         "dopisek": f"pacjenci pozyskani w danym roku po kosztach kampanii: {zn(g4['wlasni_zmiana_proc'], 0)}%",
         "stan": "uwaga"},
    ]
    bloki.append(("wzrost/werdykt", werdykt, [], []))
    bloki.append(("wzrost/kafelki", kafelki, [], []))

    # ---------------------------------------------------------------- krok 1: dashboard
    dz, cz = V["dash_zam"], V["czyste_zam"]
    zast = {z["tytul"]: z["tekst"] for z in W0["zastrzezenia"]}
    dash = karta(
        "Ile z liczb z dashboardu jest prawdą?", etykieta="Krok 1", id="dashboard",
        wniosek=f"Liczba nowych pacjentów i sprzedaż TelemediGO się zgadzają, ale zamówień przybyło o {z0(cz[0])}%, a nie o "
                f"{z0(dz[0])}%, a przychodu z konsultacji po zwrotach o {z0(cz[3])}%, a nie o {z0(dz[3])}%.",
        znaczy="Zanim na dashboardzie zaczniemy podejmować decyzje, trzeba go oczyścić z podwójnych zamówień i kont "
               "testowych i liczyć przychód po zwrotach (pozycja 2 listy priorytetów).",
        tresc=[punkty([
            f"Dashboard liczy dane na surowo: z {liczba(V['dup'])} zdublowanymi zamówieniami z {V['dup_daty']}, z "
            f"{liczba(V['testy_razem'][0])} zamówieniami {liczba(V['testy_konta'])} kont testowych i z przychodem przed "
            f"zwrotami.",
        ])],
        wstaw="mostek",
        zastrzezenie="Pierwszy rok startował od zera, bez bazy powracających pacjentów, więc sumy roczne z definicji "
                     "faworyzują drugi rok (krok 5).",
        szczegoly=[punkty([slownik(t + " " + zast[t]).replace(
            "To rozbicie księgowe, a nie wynik biznesu, który startuje od zera: nie modeluje",
            "To rozbicie księgowe, które nie modeluje")
            for t in ("Dashboard liczy dane na surowo.", "Start od zera.", "Wynik biznesu rośnie wolniej niż sprzedaż.")])],
        linki=[link("Jakość danych: od dashboardu do danych oczyszczonych", "#jakosc"),
               link("Priorytety: pozycja 2, codzienny raport", "#priorytety?p=2")],
        zrodlo="analiza/a3_dashboard.py, analiza/a2_czyste.py, analiza/wyniki/c_priorytety.txt (W3).")
    bloki.append(("wzrost/dashboard", dash, ["c:wzrost"], W0["_dodane"]))

    # ---------------------------------------------------------------- krok 2: skąd nowi pacjenci
    nowe_udz = 100 * V["nowe_7268"] / n2
    pac = karta(
        "Skąd są nowi pacjenci?", etykieta="Krok 2", id="pacjenci",
        wniosek=f"Z {liczba(g1['przyrost'])} nowych pacjentów więcej niż rok wcześniej {liczba(g1['nowe_z1k'])}, czyli "
                f"{z0(udz)}% przyrostu, to pacjenci dwóch nowych kampanii na L4: Meta od listopada 2025 i TikTok od lutego "
                f"2026.",
        znaczy=f"Przyrost pacjentów przypisujemy prawie w całości dwóm kampaniom: poza nimi nowych pacjentów przybyło tylko o "
               f"{z0(wz[1])}%, więc o wzroście decyduje to, ile zostaje na pacjencie tych kampanii (krok 4).",
        tresc=[punkty([
            f"Meta na L4 dała {liczba(g1['nowe_meta_z1k'])} nowych pacjentów, a TikTok na L4 {liczba(g1['nowe_tiktok_z1k'])}.",
            f"Pozostałe kampanie płatne dały o {liczba(pp['przyrost'])} nowych pacjentów więcej niż rok wcześniej, kanały "
            f"bezpłatne (wejścia bezpośrednie, bezpłatna wyszukiwarka, program poleceń) o {liczba(bz['przyrost'])} więcej, "
            f"a ranking lekarzy prawie tyle samo ({liczba(af['okres_2'])} wobec {liczba(af['okres_1'])}).",
            f"Według sesji z płatnością nowe kampanie dały {liczba(g1['nowe_z2'])} pacjentów, czyli "
            f"{z0(g1['udzial_nowych_w_przyroscie_z2'])}% przyrostu, a bez nich pacjentów przybyło o {z0(wz[2])}%.",
        ])],
        szczegoly=[punkty([
            f"Dokładnie: {zn(wz[0])}% wszystkich nowych pacjentów, {zn(wz[1])}% bez nowych kampanii, {zn(wz[3])}% z "
            f"kanałów bezpłatnych (z {liczba(V['bezpl'][1])} do {liczba(V['bezpl'][2])}). Pacjenci nowych kampanii: "
            f"{liczba(V['nowe_7268'])} z {liczba(n2)} ({z0(nowe_udz)}%), marża w 90 dniach {liczba(V['nowe_marza'][4], 1)} zł "
            f"wobec {liczba(V['m90_bez_z1k'], 1)} zł.",
            f"Pozostałe kampanie płatne: {liczba(pp['okres_1'])} i {liczba(pp['okres_2'])} nowych pacjentów "
            f"({zn(100 * (pp['okres_2'] / pp['okres_1'] - 1))}%); ranking lekarzy {liczba(af['okres_1'])} i "
            f"{liczba(af['okres_2'])}.",
            f"Źródło pacjenta liczymy według pierwszego wejścia: pacjent nowej kampanii to ten, który pierwszy raz wszedł "
            f"z jej reklamy albo zapłacił z jej kodem rabatowym. Według sesji z płatnością pacjentów bez nowych kampanii jest "
            f"{liczba(V['bez_z2'])}, czyli {zn(wz[2])}%. Różnica to {liczba(E['p_X_caly'])} pacjentów, którzy według "
            f"pierwszego wejścia należą do nowych kampanii, a według sesji z płatnością do innych kanałów: "
            f"{liczba(E['p_X_caly_wejscie_n'])} weszło pierwszy raz z reklamy nowej kampanii, a zapłaciło w innej sesji "
            f"(najczęściej po wejściu bezpośrednim albo z wyszukiwarki), a {liczba(E['p_X_caly_tylko_kod_n'])} weszło "
            f"z innego kanału, ale zapłaciło z kodem nowej kampanii. Wracają tak rzadko jak pozostali pacjenci nowych "
            f"kampanii. Bez nich obie reguły przypisania dają ten sam przyrost pacjentów, ten sam powrót i tę samą marżę, więc "
            f"pacjentów i retencję opisujemy według pierwszego wejścia. W ekonomii kampanii pokazujemy obie reguły.",
        ])],
        linki=[link("Kohorty: nowi pacjenci według źródła pozyskania", "#kohorty?okno=90&podz=kanal&wygl=28")],
        zrodlo="analiza/g_werdykt.py → analiza/wyniki/g_werdykt.txt (G1), analiza/wyniki/c_priorytety.txt (W1), "
               "analiza/wyniki/e_merytoryka.txt (punkt 1).")
    bloki.append(("wzrost/pacjenci", pac, ["c:wzrost"], W0["_dodane"]))

    # ---------------------------------------------------------------- krok 3: czy wracają
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
        "Czy wracają?", etykieta="Krok 3", id="retencja",
        wniosek=f"Rzadziej niż rok wcześniej: w ciągu 90 dni wraca {z0(W['p90_o2'])}% nowych pacjentów wobec "
                f"{z0(W['p90_o1'])}%, a pacjenci nowych kampanii na L4 tylko w {z0(NZ['p90_o2'])}%.",
        znaczy=f"Nowy pacjent zostawia dziś mniej w kolejnych miesiącach: jego marża w 90 dniach, przed kosztem pozyskania, "
               f"spadła z {z0(V['m90'][1])} do {z0(V['m90'][2])} zł.",
        tresc=[tab, punkty([
            "Liczymy tylko pacjentów, którzy mają już pełne okno od pierwszego zakupu (na przykład pełne 90 dni), na "
            "tych samych dniach kalendarzowych w obu latach.",
            f"Bez pacjentów nowych kampanii powrót też spada: {z0(B1['p90_o2'])}% wobec {z0(W['p90_o1'])}%.",
            f"Pacjenci nowych kampanii wracają w {z0(NZ['p90_o2'])}%. Ich większy udział wśród nowych pacjentów "
            f"odpowiada za około {z0(u_z1k)}% spadku powrotu ({liczba(abs(rz1[5]), 1)} z {liczba(abs(rz1[4]), 1)} punktu "
            f"procentowego), a reszta to spadek w kanałach działających w obu latach.",
            f"Poza nowymi kampaniami marża na pacjenta w 90 dniach prawie stoi: {z0(V['m90_bez_z1k'])} zł wobec "
            f"{z0(V['m90'][1])} zł.",
        ])],
        zastrzezenie="Te liczby opisują zmianę, ale nie wskazują jej przyczyny. Nie wiemy, dlaczego spada powrót w kanałach "
                     "działających w obu latach: czy ci sami pacjenci zachowują się dziś gorzej, czy zmieniło się to, kto do "
                     "nas trafia.",
        szczegoly=[punkty([
            f"Powrót to kolejne zamówienie, które nie zostało anulowane. Liczymy go na tych samych dniach kalendarzowych "
            f"(pierwsze zakupy do {int(pw[2])} {B2.MIESIACE_DOP[int(pw[1]) - 1]} w obu latach przy oknie 90 dni) i tylko "
            f"w kohortach z pełnym oknem obserwacji. Liczba pacjentów: {liczba(W['n90_o1'])} rok wcześniej i "
            f"{liczba(W['n90_o2'])} w ostatnich 12 miesiącach; bez nowych kampanii {liczba(B1['n90_o2'])} (powrót "
            f"{proc(B1['p90_o2'])} wobec {proc(W['p90_o1'])}), pacjenci nowych kampanii {liczba(NZ['n90_o2'])} (powrót "
            f"{proc(NZ['p90_o2'])}). Marża na pacjenta w 90 dniach: {liczba(V['m90'][2], 1)} zł wobec "
            f"{liczba(V['m90'][1], 1)} zł, bez nowych kampanii {liczba(V['m90_bez_z1k'], 1)} zł.",
            f"Kolejne zamówienia na pacjenta w 90 dniach: {liczba(Dd['kolejne90_wszyscy_okres2_srednia_na_pacjenta'], 3)} "
            f"wobec {liczba(Dd['kolejne90_wszyscy_okres1_srednia_na_pacjenta'], 3)}, czyli o "
            f"{proc(100 * (1 - Dd['kolejne90_wszyscy_okres2_srednia_na_pacjenta'] / Dd['kolejne90_wszyscy_okres1_srednia_na_pacjenta']))} "
            f"mniej; bez pacjentów nowych kampanii {liczba(Dd['kolejne90_bez_nowych_z1k_okres2_srednia_na_pacjenta'], 3)}.",
            f"Według sesji z płatnością bez nowych kampanii powrót wynosi {proc(B2_['p90_o2'])}, a marża "
            f"{liczba(V['m90_bez_z2'], 1)} zł. Cała różnica to {liczba(E['r_X_n'])} pacjentów nowych kampanii (z pełnym "
            f"oknem 90 dni), których ta reguła przypisuje innym kanałom: {liczba(E['r_X_wejscie_n'])} weszło z reklamy "
            f"nowej kampanii, a zapłaciło w innej sesji, a {liczba(E['r_X_tylko_kod_n'])} zapłaciło z kodem nowej "
            f"kampanii po wejściu z innego kanału. Wracają w {liczba(E['r_X_powrot'], 1)}%. Bez nich obie reguły dają "
            f"{proc(B1['p90_o2'])} i {liczba(V['m90_bez_z1k'], 1)} zł, a udział nowych kampanii w spadku powrotu wynosi w "
            f"obu {z0(u_z1k)}% (według sesji z płatnością bez tej poprawki {z0(E['rozklad_Z2_udzial_nowych_w_spadku'])}%).",
            f"„Około {z0(u_z1k)}% spadku” to podział opisowy, czyli bez mierzenia wpływu: udział pacjentów nowych kampanii "
            f"({liczba(100 - rz1[1], 1)}% kohort) razy różnica powrotu między nimi a resztą ({liczba(abs(rz1[5]), 1)} z "
            f"{liczba(abs(rz1[4]), 1)} punktu procentowego). Nie mówi, co by się stało bez tych kampanii.",
            "Według pierwszej usługi, bez pacjentów nowych kampanii (95% przedział różnicy): spada po e-recepcie z "
            f"{usl('internista_e_recepta')}, a po wizycie u innego specjalisty z {usl('inny_specjalista')}. Bez istotnej "
            f"zmiany: pediatra z {usl('pediatra', True)}, psychiatra z {usl('psychiatra', True)}, pierwsze L4 u internisty "
            f"z {usl('internista_l4', True)}. Według sesji z płatnością L4 spada do {proc(Dd[l4 + 'z2_proc_okres2'])}, ale "
            f"to ta sama grupa: do {liczba(Dd[l4 + 'z1k_pacjenci_okres2'])} pacjentów według pierwszego wejścia dochodzi "
            f"{liczba(Dd[l4 + 'z2_pacjenci_okres2'] - Dd[l4 + 'z1k_pacjenci_okres2'])} pacjentów nowych kampanii z pierwszym L4.",
            f"Liczba osób, które wróciły w 90 dniach, rośnie: {liczba(pw[4])} wobec {liczba(pw[3])} ({zn(pw[5])}%). Spada "
            f"tylko ich odsetek.",
            f"W 180 dniach liczymy tylko kohorty z pełnym oknem ({liczba(p180[0])} i {liczba(p180[1])} pacjentów), więc to "
            f"wcześniejsze, mniejsze grupy niż w 90 dniach.",
            "Część spadku w kanałach działających w obu latach może wiązać się z porannymi opóźnieniami u internistów: po "
            "spóźnionej pierwszej wizycie pacjenci wracają rzadziej. Dane tego nie rozstrzygają (Czego nie wiemy, punkt 4).",
        ])],
        linki=[link("Zdarzenia: co zmieniło się po każdym zdarzeniu i każdej decyzji", "#zdarzenia"),   # runda G: tabela w „Zdarzeniach”
               link("Kohorty: powrót w 90 dniach, nowe kampanie na L4 i pozostałe", "#kohorty?okno=90&podz=grupa&wygl=28"),
               link("Kohorty: powrót bez pacjentów nowych kampanii", "#kohorty?okno=90&f_grupa=pozostale&wygl=28")],
        zrodlo="analiza/wyniki/c_priorytety.txt (W2), analiza/wyniki/a5r_kohorty.txt (180 dni), analiza/wyniki/d_retencja.txt "
               "(usługi, kolejne zamówienia), analiza/wyniki/e_merytoryka.txt (punkt 1).")
    bloki.append(("wzrost/retencja", ret, ["c:wzrost"], W0["_dodane"]))

    # ---------------------------------------------------------------- krok 4: ile zostaje na pacjencie
    a1, a2 = pod[("Z1K", 1)], pod[("Z1K", 2)]
    g180 = B2.dt.date.fromisoformat(gr180)
    kol_m = ["Miesiąc pierwszego zakupu", "Nowi pacjenci", "Koszt pozyskania", "Marża w 180 dniach", "Zostaje na pacjencie",
             "Zostaje na pacjencie według sesji z płatnością"]
    tab_m = tabela(kol_m, [wiersz(miesiac_rz(r["okres"]), [
        liczba(r["nowi"]), f"{liczba(r['koszt_pozysk'], 1)} zł", f"{liczba(r['marza180'], 1)} zł",
        zmiana(f"{zn(r['wynik'])} zł", r["wynik"]), zmiana(f"{zn(m2[r['okres']]['wynik'])} zł", m2[r["okres"]]["wynik"])])
        for r in m1],
        tytul=f"Nowe kampanie na L4 według miesiąca pierwszego zakupu, według pierwszego wejścia (ostatnia kolumna: według "
              f"sesji z płatnością). Pełne 180 dni mają pierwsze zakupy do {g180.day}.{g180:%m.%Y}; dla późniejszych marża "
              f"w 180 dniach jest przybliżona.")
    q_nazwy = (("2025Q4", "IV kwartale 2025"), ("2026Q1", "I"), ("2026Q2", "II"), ("2026Q3", "III kwartale 2026"))
    nap = karta(
        "Ile zarabiamy na nowym pacjencie po koszcie pozyskania?", etykieta="Krok 4", id="na-pacjencie",
        wniosek=f"Na pacjencie nowych kampanii na L4 zostaje w ciągu 180 dni {z0(L4['wynik'])} zł, a na pacjencie pozostałych "
                f"kampanii płatnych {z0(P2['wynik'])} zł (rok wcześniej {z0(P1['wynik'])} zł).",
        znaczy="Pacjent przypisany nowym kampaniom zostawia po koszcie pozyskania kilka razy mniej niż pacjent pozostałych "
               "kampanii płatnych, a u pacjentów pozyskanych od kwietnia szacowany wynik jest bliski zeru.",
        tresc=[punkty([
            # jedno miejsce po przecinku, żeby marża minus koszt dawała w głowie podaną kwotę (uwaga Kuby, 2026-10-23)
            f"Pacjent nowych kampanii zostawia w 180 dniach {liczba(L4['marza'], 1)} zł marży, a jego pozyskanie kosztuje "
            f"{liczba(L4['koszt_pozysk'], 1)} zł, więc zostaje {liczba(L4['wynik'], 1)} zł. Pacjent pozostałych kampanii "
            f"płatnych zostawia {liczba(P2['marza'], 1)} zł marży przy koszcie pozyskania {liczba(P2['koszt_pozysk'], 1)} zł, "
            f"więc zostaje {liczba(P2['wynik'], 1)} zł.",
            f"Miesiąc po miesiącu koszt pozyskania pacjenta nowych kampanii rośnie z "
            f"{zakres(min(r['koszt_pozysk'] for r in zima), max(r['koszt_pozysk'] for r in zima))} zł (listopad 2025 – luty "
            f"2026) do {zakres(min(r['koszt_pozysk'] for r in wiosna), max(r['koszt_pozysk'] for r in wiosna))} zł (kwiecień – "
            f"wrzesień 2026), a marża pacjenta zostaje na poziomie "
            f"{zakres(min(r['marza180'] for r in m1), max(r['marza180'] for r in m1))} zł. Od kwietnia zostaje od "
            f"{liczba(min(r['wynik'] for r in wiosna), 0)} do {zn(max(r['wynik'] for r in wiosna), 0)} zł na pacjencie.",
            f"Osobno: TikTok na L4 traci od marca 2026 (w II kwartale {z0(abs(Qt['2026Q2']['wynik']))} zł na pacjencie), a "
            f"Meta na L4 zostaje na plusie (w III kwartale {z0(Qm['2026Q3']['wynik'])} zł na pacjencie).",
            f"Według sesji z płatnością obie kampanie razem tracą od grudnia 2025, a od kwietnia średnio "
            f"{zakres(-max(wios_z2), -min(wios_z2))} zł na pacjencie.",
            f"Razem w roku pozyskania pacjenci nowych kampanii zostawili {z0(a2['nowe_marza_przed'] / 1000)} tys. zł marży "
            f"przy {z0(a2['nowe_wydatki'] / 1000)} tys. zł wydatków na te kampanie, czyli {z0(a2['nowe_wynik'] / 1000)} "
            f"tys. zł.",
        ])],
        zastrzezenie=f"Pacjenci z pierwszym zakupem od kwietnia 2026 nie mają jeszcze pełnych 180 dni. Ich marżę przybliżamy: "
                     f"do marży z krótszego okresu dodajemy to, co starsi pacjenci tych kampanii zostawili później: od "
                     f"{liczba(prz_od, 2)} zł, gdy znamy już 90 dni, do {liczba(prz_do, 2)} zł, gdy znamy tylko dzień "
                     f"zakupu. Dopłata jest mała, bo ci pacjenci prawie nie wracają.",
        szczegoly=[tab_m, punkty([
            f"Porównanie płatnych z płatnymi liczymy na pierwszych zakupach od 1.10 do {g180.day}.{g180:%m} w obu latach, bo "
            f"tylko one mają pełne 180 dni: {liczba(L4['nowi'])} pacjentów nowych kampanii (przedział 95% od "
            f"{liczba(L4['wynik_od'], 1)} do {liczba(L4['wynik_do'], 1)} zł), {liczba(P2['nowi'])} pacjentów pozostałych "
            f"kampanii płatnych ({liczba(P2['wynik'], 1)} zł) i rok wcześniej {liczba(P1['nowi'])} ({liczba(P1['wynik'], 1)} zł).",
            f"Według sesji z płatnością pacjent nowych kampanii daje {liczba(L4z2['wynik'], 1)} zł, a pacjent pozostałych "
            f"kampanii płatnych {liczba(P2z2['wynik'], 1)} zł (rok wcześniej {liczba(P1z2['wynik'], 1)} zł).",
            f"Na całym roczniku, z przybliżoną marżą w 180 dniach dla młodszych pacjentów: nowe kampanie "
            f"{liczba(R_L4['wynik'], 1)} zł na pacjencie ({liczba(R_L4['nowi'])} pacjentów), pozostałe kampanie płatne "
            f"{liczba(R_P2['wynik'], 1)} zł wobec {liczba(R_P1['wynik'], 1)} zł rok wcześniej.",
            f"Ranking lekarzy (prowizja {z0(AF2['prowizja_zl'] / AF2['nowi'])} zł za pacjenta) zostawia "
            f"{liczba(AF2['wynik'], 1)} zł wobec {liczba(AF1['wynik'], 1)} zł rok wcześniej; liczymy go osobno, bo płacimy "
            f"za pacjenta, a nie za kliknięcie.",
            "W kwartałach (według pierwszego wejścia): "
            + ", ".join(f"{liczba(Q[k]['wynik'], 1)} zł" for k, _ in q_nazwy)
            + " na pacjencie w IV kwartale 2025 i w I, II i III kwartale 2026; według sesji z płatnością "
            + ", ".join(f"{liczba(Qz2[k]['wynik'], 1)} zł" for k, _ in q_nazwy) + ".",
            "Kwota na pacjencie to średnia ze wszystkich pacjentów przypisanych kampanii. Nie mówi, ile dałaby kolejna "
            "złotówka budżetu.",
        ])],
        linki=[link("Wynik biznesu: ekonomia kampanii, obie reguły", "#wynik"),
               link("Priorytety: pozycja 3, TikTok na L4", "#priorytety?p=3"),
               link("Priorytety: pozycja 9, test kampanii Meta na L4", "#priorytety?p=9")],
        zrodlo="analiza/g_werdykt.py → analiza/wyniki/g_werdykt.txt (G2, G3), analiza/wyniki/a5e_ekonomia.txt (1b).")
    nap["wykres"] = {
        "opis": "Zostaje na pacjencie nowych kampanii na L4 po koszcie pozyskania, według miesiąca pierwszego zakupu i dwóch "
                "reguł przypisania",
        "przypis": "Zostaje na pacjencie: marża w 180 dniach minus koszt pozyskania. Pionowa linia to zero: na lewo od niej "
                   "pozyskanie kosztuje więcej, niż pacjent zostawia. Gwiazdka: marża w 180 dniach przybliżona.",
        "wiersze": [{"etykieta": miesiac_rz(r["okres"]), "przyblizone": r["okno"] < 180,
                     "z1k": round(r["wynik"], 1), "z2": round(m2[r["okres"]]["wynik"], 1)} for r in m1]}
    bloki.append(("wzrost/na-pacjencie", nap, [], []))

    # ---------------------------------------------------------------- krok 5: skąd +27% marży
    z1, z2 = pod[("Z2", 1)], pod[("Z2", 2)]
    mar = karta(
        f"Skąd w takim razie {zn(g4['przyrost_proc'], 0)}% marży?", etykieta="Krok 5", id="marza",
        wniosek=f"Z pacjentów pozyskanych w pierwszym roku: ich zakupy w ostatnich 12 miesiącach dały "
                f"{z0(g4['baza_o1_w_o2'] / 1000)} tys. zł, czyli {z0(udz_b)}% przyrostu marży o {z0(g4['przyrost'] / 1000)} "
                f"tys. zł.",
        znaczy=f"Łączny wynik pacjentów pozyskanych w danym roku, po kosztach kampanii, wzrósł tylko o "
               f"{z0(g4['wlasni_zmiana_proc'])}% przy {z0(wz[0])}% więcej pacjentów, a na jednym nowym pacjencie spadł z "
               f"{z0(g4['wlasni_na_pacjenta_o1'])} do {z0(g4['wlasni_na_pacjenta_o2'])} zł.",
        tresc=[punkty([
            f"Rok wcześniej cała marża, {z0(g4['marza_o1'] / 1000)} tys. zł, pochodziła od pacjentów pozyskanych w tym "
            f"samym roku. Wcześniejszych pacjentów w danych nie ma, bo dane zaczynają się 1.10.2024.",
            f"W ostatnich 12 miesiącach pacjenci z pierwszego roku dali {z0(g4['baza_o1_w_o2'] / 1000)} tys. zł: "
            f"{z0(g4['baza_konsultacje'] / 1000)} tys. zł z kolejnych wizyt i {z0(g4['baza_telemedigo'] / 1000)} tys. zł z "
            f"opłat za TelemediGO.",
            f"Pacjenci pozyskani w ostatnich 12 miesiącach zostawili w tym samym roku "
            f"{z0(g4['przed_kampaniami_wlasni_o2'] / 1000)} tys. zł marży przed kosztem kampanii, o "
            f"{z0(100 * (g4['przed_kampaniami_wlasni_o2'] / g4['przed_kampaniami_wlasni_o1'] - 1))}% więcej niż rok "
            f"wcześniej. Wydatki na kampanie wzrosły jednak o {z0(100 * (g4['wydatki_o2'] / g4['wydatki_o1'] - 1))}%, z "
            f"{z0(g4['wydatki_o1'] / 1000)} do {z0(g4['wydatki_o2'] / 1000)} tys. zł, więc po odjęciu wydatków i prowizji "
            f"afiliacyjnej ({z0(g4['prowizja_o2'] / 1000)} tys. zł) zostaje {z0(g4['wlasni_o2'] / 1000)} tys. zł wobec "
            f"{z0(g4['wlasni_o1'] / 1000)} tys. zł.",
            "To nie jest lepsza retencja: nowi pacjenci wracają rzadziej (krok 3). Tej kwoty rok wcześniej nie było, bo w "
            "danych nie ma pacjentów sprzed 1.10.2024.",
        ])],
        zastrzezenie="To rozbicie księgowe: przypisuje marżę i koszty grupom pacjentów, ale nie mierzy, co by się stało bez "
                     "nowych kampanii.",
        szczegoly=[punkty([
            f"Dokładnie: marża po wszystkich kosztach {zl(g4['marza_o1'])} rok wcześniej i {zl(g4['marza_o2'])} w ostatnich "
            f"12 miesiącach, czyli +{zl(g4['przyrost'])} ({zn(g4['przyrost_proc'])}%). Pacjenci z pierwszego roku: "
            f"{zl(g4['baza_o1_w_o2'])} ({liczba(udz_b, 1)}% przyrostu). Pacjenci pozyskani w danym roku, po kosztach kampanii "
            f"i prowizji: {zl(g4['wlasni_o1'])} i {zl(g4['wlasni_o2'])}, czyli +{zl(g4['wlasni_zmiana'])} "
            f"({zn(g4['wlasni_zmiana_proc'])}%; {liczba(g4['wlasni_udzial_w_przyroscie_proc'], 1)}% przyrostu). Na nowego "
            f"pacjenta: {liczba(g4['wlasni_na_pacjenta_o1'], 2)} zł ({liczba(n1)} pacjentów) i "
            f"{liczba(g4['wlasni_na_pacjenta_o2'], 2)} zł ({liczba(n2)}). To porównanie zawiera też krótszą obserwację: od "
            f"pierwszego zakupu do końca roku minęło średnio {liczba(g4['obserwacja_dni_o1'], 1)} dnia rok wcześniej i "
            f"{liczba(g4['obserwacja_dni_o2'], 1)} dnia w ostatnich 12 miesiącach. Porównanie w stałym oknie 180 dni jest "
            f"w kroku 4.",
            f"Pacjenci nowych kampanii na L4 zostawili w roku pozyskania {z0(a2['nowe_marza_przed'] / 1000)} tys. zł marży "
            f"przy {z0(a2['nowe_wydatki'] / 1000)} tys. zł wydatków, czyli {z0(a2['nowe_wynik'] / 1000)} tys. zł "
            f"({liczba(a2['nowe_wynik'] / a2['nowe_pacjenci'], 2)} zł na pacjenta). Pozostali pacjenci pozyskani w ostatnich "
            f"12 miesiącach dali po kosztach kampanii i prowizji {z0(a2['reszta_wynik'] / 1000)} tys. zł wobec "
            f"{z0(a1['reszta_wynik'] / 1000)} tys. zł rok wcześniej ({zn(100 * (a2['reszta_wynik'] / a1['reszta_wynik'] - 1))}%), "
            f"a na pacjenta {liczba(a2['reszta_wynik'] / a2['reszta_pacjenci'], 2)} zł wobec "
            f"{liczba(a1['reszta_wynik'] / a1['reszta_pacjenci'], 2)} zł.",
            f"Według sesji z płatnością nowe kampanie tracą w roku pozyskania {z0(abs(z2['nowe_wynik']) / 1000)} tys. zł "
            f"({liczba(z2['nowe_wynik'] / z2['nowe_pacjenci'], 2)} zł na pacjenta), a pozostali pacjenci dają o "
            f"{liczba(100 * (z2['reszta_wynik'] / z1['reszta_wynik'] - 1), 1)}% więcej niż rok wcześniej.",
            f"Marża przed kosztem kampanii pacjentów pozyskanych w danym roku: {z0(g4['przed_kampaniami_wlasni_o1'] / 1000)} "
            f"tys. zł i {z0(g4['przed_kampaniami_wlasni_o2'] / 1000)} tys. zł; wydatki na kampanie {zl(g4['wydatki_o1'])} i "
            f"{zl(g4['wydatki_o2'])}; prowizja {zl(g4['prowizja_o1'])} i {zl(g4['prowizja_o2'])}.",
        ])],
        linki=[link("Wynik biznesu: marża po kwartałach", "#wynik")],
        zrodlo="analiza/g_werdykt.py → analiza/wyniki/g_werdykt.txt (G4), analiza/wyniki/c_priorytety.txt (W3).")
    assert z2["nowe_wynik"] < 0 < a2["nowe_wynik"]
    mar["wykres"] = {
        "opis": "Marża po wszystkich kosztach rok wcześniej i w ostatnich 12 miesiącach: pacjenci pozyskani w tym samym roku "
                "po kosztach kampanii i pacjenci z pierwszego roku",
        "czesci": ["pacjenci pozyskani w tym samym roku, po kosztach kampanii", "pacjenci z pierwszego roku"],
        "przypis": "Marża po wszystkich kosztach w tysiącach złotych; długość słupka to kwota.",
        "wiersze": [{"etykieta": "rok wcześniej", "wartosci": [round(g4["wlasni_o1"] / 1000, 3), 0.0]},
                    {"etykieta": "ostatnie 12 miesięcy",
                     "wartosci": [round(g4["wlasni_o2"] / 1000, 3), round(g4["baza_o1_w_o2"] / 1000, 3)]}]}
    bloki.append(("wzrost/marza", mar, [], []))

    # ---------------------------------------------------------------- krok 6: kwartały
    nazwy_kw = {"2025-10-01": "IV 2025", "2026-01-01": "I 2026", "2026-04-01": "II 2026", "2026-07-01": "III 2026"}
    tab_kw = tabela(["Kwartał", "Marża przed kosztem kampanii", "Wydatki na kampanie", "Marża po kosztach kampanii"],
                    [wiersz(nazwy_kw[r["kw"]], [
                        zmiana(f"{zn(r['przed_rr_dokl'])}%", r["przed_rr_dokl"], pod=tz(r["przed"])),
                        zmiana_wydatkow(r, z_wartoscia=True),
                        zmiana(f"{zn(r['marza_rr_dokl'])}%", r["marza_rr_dokl"], pod=tz(r["marza"]))]) for r in kw],
                    tytul="Zmiana wobec tego samego kwartału rok wcześniej; pod nią wartość w kwartale")
    baza1 = (E["baza_2026"] - E["baza_2026_osobno_zl"]) / (E["baza_2025"] - E["baza_2025_osobno_zl"]) - 1
    luka = -Dd["q3_reszta_z1k_luka_bez_telemedigo"]
    assert q3["wydatki_razy"] > 2
    assert all(a["przed_rr_dokl"] > b["przed_rr_dokl"] and a["wydatki_razy"] < b["wydatki_razy"] for a, b in zip(kw, kw[1:])), \
        "„coraz szybciej / coraz wolniej” wymaga monotonicznych zmian w kolejnych kwartałach"
    assert E["q3_zmiana_proc"] < 0 < E["q3_w1_zmiana_proc"], "zastrzeżenie mówi „spadła” i „wyższa”"
    wy = karta(
        "W którą stronę to idzie z kwartału na kwartał?", etykieta="Krok 6", id="wynik",
        wniosek=f"Z każdym kwartałem wydatki na kampanie rosną rok do roku szybciej, a marża przed ich kosztem wolniej: w III "
                f"kwartale 2026 wydatki były ponad dwa razy wyższe niż rok wcześniej, a marża przed ich kosztem wyższa o "
                f"{z0(q3['przed_rr_dokl'])}%.",
        znaczy=f"Wzrost marży po kosztach kampanii się zatrzymał: w III kwartale 2026 spadła o "
               f"{z0(abs(E['q3_zmiana_proc']))}% rok do roku, a po odjęciu jednorazowego startu sprzedaży TelemediGO w "
               f"newsletterze we wrześniu 2025 byłaby wyższa tylko o {z0(E['q3_w1_zmiana_proc'])}%.",
        tresc=[tab_kw, punkty([
            f"Na pacjencie nowych kampanii na L4 zostawało po koszcie pozyskania {z0(Q['2025Q4']['wynik'])} zł w IV kwartale "
            f"2025 i {z0(Q['2026Q1']['wynik'])} zł w I kwartale 2026, a w II i III kwartale 2026 mniej niż 1 zł.",
            f"Bez zakupów pacjentów pozyskanych w poprzednich kwartałach marża po kosztach kampanii rosła rok do roku o "
            f"{liczba(bb['2025_q4'], 1)}% w IV kwartale 2025 i o {liczba(bb['2026_q1'], 1)}% w I kwartale 2026, a w II i III "
            f"kwartale 2026 spadła o {liczba(abs(bb['2026_q2']), 1)}% i {liczba(abs(bb['2026_q3']), 1)}%.",
            f"Marża przed kosztem kampanii wzrosła za cały rok o {z0(E['rok_przed_zmiana_proc'])}%, a wydatki na kampanie "
            f"o {z0(E['rok_wyd_zmiana_proc'])}%.",
        ])],
        # bez zastrzeżenia: spadek o 7% i wariant +1% stoją w zdaniu „Co to znaczy dla biznesu” (uwaga Kuby, 2026-10-23)
        szczegoly=[punkty([
            f"Za cały rok marża po koszcie lekarza, kampaniach i prowizji wzrosła z {z0(E['rok_marza_1'] / 1000)} do "
            f"{z0(E['rok_marza_2'] / 1000)} tys. zł, czyli o {liczba(E['rok_marza_zmiana_proc'], 1)}%. Marża przed kosztem "
            f"kampanii wzrosła o {liczba(E['rok_przed_zmiana_proc'], 1)}%, a wydatki na kampanie o "
            f"{liczba(E['rok_wyd_zmiana_proc'], 1)}%.",
            f"W III kwartale 2026 marża była o {liczba(abs(E['q3_zmiana_proc']), 1)}% niższa niż rok wcześniej. W pierwszych "
            f"{liczba(E['newsletter_dni_startu'])} dniach sprzedaży TelemediGO w newsletterze pacjenci kupili "
            f"{odm(E['q3_osobno_25'], 'członkostwo', 'członkostwa', 'członkostw')}; po odjęciu szacowanej nadwyżki tego "
            f"startu marża kwartału jest o {liczba(E['q3_w1_zmiana_proc'], 1)}% wyższa niż rok wcześniej.",
            f"Warianty III kwartału: bez nadwyżki startu sprzedaży w newsletterze ({z0(E['newsletter_nadwyzka'])} z "
            f"{liczba(E['q3_osobno_25'])} zakupów ponad zwykłe tempo {z0(E['newsletter_norma_startu'])} na "
            f"{liczba(E['newsletter_dni_startu'])} dni, {tz(E['newsletter_nadwyzka_zl'])}) {zn(E['q3_w1_zmiana_proc'])}%; "
            f"bez całej sprzedaży w newsletterze w obu latach {zn(E['q3_w2_zmiana_proc'])}%; bez wszystkich opłat za "
            f"TelemediGO {zn(E['q3_w3_zmiana_proc'])}%. Marża przed kosztem kampanii bez nadwyżki startu rośnie o "
            f"{liczba(E['q3_przed_bez_nadwyzki_zmiana_proc'], 1)}%.",
            f"Awaria zakładania konta w Safari na iPhone'ach kosztowała w samym III kwartale 2026 szacunkowo "
            f"{zakres(zaks[0] / 1000, zaks[1] / 1000, 1)} tys. zł marży. Wyniku kwartału bez awarii nie mierzymy; to "
            f"scenariusz z pozycji 1 listy priorytetów.",
            slownik(zacz(W0["kwartaly"]["punkty"], "W samych miesiącach")),
            f"Baza powracających pacjentów (marża z pacjentów pozyskanych w poprzednich kwartałach): w III kwartale 2026 "
            f"{tz(E['baza_2026'])} wobec {tz(E['baza_2025'])} rok wcześniej. Rok wcześniej zawierała jednorazowy start "
            f"sprzedaży w newsletterze; po odjęciu części nadwyżki przypadającej na bazę ({liczba(E['baza_2025_osobno'])} z "
            f"{liczba(E['q3_osobno_25'])} zakupów) to {tz(E['baza_2025_bez_nadwyzki'])}, więc w 2026 baza dała o "
            f"{liczba(E['baza_zmiana_bez_nadwyzki_proc'], 1)}% więcej (bez całej sprzedaży w newsletterze w obu latach o "
            f"{liczba(100 * baza1, 1)}% więcej). Wszystkich pacjentów pozyskanych w poprzednich kwartałach jest prawie trzy "
            f"razy więcej ({liczba(V['q3_baza_pac']['2026-Q3'])} wobec {liczba(V['q3_baza_pac']['2025-Q3'])}), ale "
            f"tych, którzy w kwartale coś kupili, tylko o {z0(100 * (E['baza_2026_aktywni'] / E['baza_2025_aktywni'] - 1))}% "
            f"więcej ({liczba(E['baza_2026_aktywni'])} wobec {liczba(E['baza_2025_aktywni'])}). Baza jest starsza, a nowsze "
            f"roczniki wracają rzadziej; tych dwóch rzeczy dane nie rozdzielają.",
            slownik(q3t["baza"]) + " Wzrost tych kwartałów jest więc zawyżony startem od zera.",
            "Rozkład spadku III kwartału na pacjentów nowych kampanii i resztę biznesu to rozkład księgowy, czyli "
            "przypisanie składników marży grupom pacjentów bez mierzenia wpływu. " + slownik(q3t["wstep"][:-1]) + ": "
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
               "analiza/wyniki/e_merytoryka.txt (punkt 2), analiza/wyniki/g_werdykt.txt (G3).")
    bloki.append(("wzrost/wynik", wy, ["c:wzrost", "c:pozycja:1", "d:Rozkład spadku"], W0["_dodane"]))

    # ---------------------------------------------------------------- krok 7: co robimy
    decyzje = {"tytul": "Decyzje na pierwszy tydzień", "punkty": [
        {"nr": 1, "tekst": "Naprawić zakładanie konta w Safari na iPhone'ach", "href": "#priorytety?p=1",
         "dopisek": f"pozycja 1 · do {z0(V['p1_hi'][3] / 1000)} tys. zł marży rocznie"},
        {"nr": 2, "tekst": "Oczyścić codzienny raport i dodać alarmy na lejku", "href": "#priorytety?p=2",
         "dopisek": f"pozycja 2 · awaria Safari trwała {liczba(V['p1_lo'][1])} dni, do końca danych"},
        {"nr": 3, "tekst": "Wstrzymać kampanię TikTok na L4 i kampanię Google Ads na specjalistów", "href": "#priorytety?p=3",
         "dopisek": "pozycje 3 i 4 · obie średnio tracą na pacjencie według obu reguł przypisania źródła (pierwsze wejście "
                    "i sesja z płatnością), a pauzę da się cofnąć w jeden dzień"},
        {"nr": 4, "tekst": "Zrobić krótkie sprawdzenia: obietnica reklam L4, poranne grafiki internistów, zakup po "
                           "zalogowaniu, kliknięcia w panelach reklam", "href": "#priorytety?p=5",
         "dopisek": "pierwsze kroki pozycji 5, 6, 8 i 11 · każde zajmuje dzień albo dwa"},
    ]}
    rob = karta(
        "Co robimy?", etykieta="Krok 7", id="co-robimy",
        wniosek="Najpierw naprawiamy to, co psuje wynik niezależnie od kampanii, potem wstrzymujemy kampanie, które średnio "
                "tracą na pacjencie, a o kampanii Meta na L4 rozstrzyga test w części kraju.",
        znaczy="Każda pozycja listy priorytetów ma wartość w marży, sposób pomiaru i czas wdrożenia; niżej decyzje na "
               "pierwszy tydzień.",
        decyzje=decyzje,
        linki=[link("Priorytety: cała lista", "#priorytety"),
               link("Priorytety: pozycja 9, test kampanii Meta na L4", "#priorytety?p=9")])
    bloki.append(("wzrost/co-robimy", rob, [], []))

    # ---------------------------------------------------------------- krok 8: czego nie wiemy
    niew = karta(
        "Czego nie wiemy?", etykieta="Krok 8", id="niewiadome",
        wniosek="Trzech rzeczy, od których zależą decyzje: ilu pacjentów nowych kampanii przyszłoby i bez reklamy, dlaczego "
                "rzadziej wracają pacjenci z kanałów działających w obu latach i ile wizyt dokłada zniżka TelemediGO.",
        znaczy="Dlatego decyzje, które od nich zależą, są na liście priorytetów testami z regułą ustaloną z góry, a nie "
               "pewnymi kwotami.",
        tresc=[punkty([
            "Ilu pacjentów nowych kampanii przyszłoby i bez reklamy: test z pozycji 9, czyli wyłączenie kampanii Meta na L4 "
            "na 4–6 tygodni w losowej połowie województw. Da wynik orientacyjny, więc decyzję podejmujemy według reguły "
            "ustalonej z góry (Czego nie wiemy, punkt 1).",
            "Dlaczego rzadziej wracają pacjenci z kanałów działających w obu latach: jedną z możliwych przyczyn są poranne "
            "opóźnienia u internistów, ale dane tego nie rozstrzygają (Czego nie wiemy, punkt 4).",
            "Ile wizyt i powrotów dokłada zniżka TelemediGO: losowy, bezpłatny dostęp do zniżek (pozycja 12; Czego nie "
            "wiemy, punkt 8).",
        ])],
        linki=[link("Czego nie wiemy: punkt 1", "#niewiadome?n=1"), link("Czego nie wiemy: punkt 4", "#niewiadome?n=4"),
               link("Czego nie wiemy: punkt 8", "#niewiadome?n=8"), link("Czego nie wiemy: cała lista", "#niewiadome")])
    bloki.append(("wzrost/niewiadome", niew, [], []))

    # ---------------------------------------------------------------- TelemediGO (osobna karta, bez numeru kroku)
    G0 = W0["telemedigo"]
    tab_go = tabela(["Typ zakupu", "Rok wcześniej", "Ostatnie 12 miesięcy", "Zmiana", "Udział we wzroście"],
                    [wiersz(r["opis"].replace("Osobno, z newslettera crm_go_upsell", "Osobno, z newslettera"),
                            r["komorki"], podsuma=(r["opis"] == "Razem")) for r in G0["tabela"]["wiersze"]])
    g2a = V["go_2a"]
    razem = V["go_typy"].loc["razem"]
    go = karta(
        "TelemediGO rośnie razem z liczbą zamówień, a nie dzięki większej chęci zakupu", id="telemedigo",
        wniosek=f"Sprzedaż wzrosła o {z0(razem['zmiana_proc'])}%, bo jest więcej zamówień i przez cały rok działała "
                f"sprzedaż w newsletterze, a odsetek kupujących przy kasie nie rośnie.",
        tresc=[tab_go, punkty([
            f"Opłata 89 zł nie pokrywa zniżek: członkostwa sprzed roku dostały średnio o około "
            f"{z0(abs(g2a['oplata_minus_znizka_efektywna_na_czlonkostwo']))} zł więcej zniżek, niż przyniosły opłat.",
            f"Widać to w marży: powtórne zamówienie pacjenta spoza nowych kampanii zostawiło w III kwartale 2026 około "
            f"{z0(E['pw_m26'])} zł marży wobec {z0(E['pw_m25'])} zł rok wcześniej. Prawie cały ten spadek to rosnący udział "
            f"wizyt ze zniżką TelemediGO: z {z0(E['pw_go_udzial_25'])}% do {z0(E['pw_go_udzial_26'])}% powtórnych zamówień.",
        ])],
        zastrzezenie="Nie wiemy, ile wizyt członkostwo dokłada. Test z pozycji 12 pokaże wpływ samej zniżki, ale nie "
                     "opłacalność oferty za 89 zł.",
        szczegoly=[punkty([popraw(x).replace("Rozstrzygnie to test z pozycji 12: losowy, bezpłatny dostęp do zniżek.",
                                             "Test z pozycji 12 (losowy, bezpłatny dostęp do zniżek) pokaże wpływ samej "
                                             "zniżki.")
                           for x in G0["punkty"]] + [
            f"Powtórne zamówienie pacjenta spoza nowych kampanii zostawiło w III kwartale 2026 {liczba(E['pw_m26'], 2)} zł "
            f"marży wobec {liczba(E['pw_m25'], 2)} zł rok wcześniej. "
            f"Wizyta ze zniżką TelemediGO zostawia średnio {liczba(E['pw_go_m26'], 2)} zł marży, bez zniżki "
            f"{liczba(E['pw_none_m26'], 2)} zł, a wizyta u specjalisty ze zniżką traci {liczba(abs(E['pw_inni_go_m26']), 2)} zł. "
            f"Udział wizyt ze zniżką wśród powtórnych zamówień: {liczba(E['pw_go_udzial_25'], 1)}% "
            f"({liczba(E['pw_n25'])} zamówień) i {liczba(E['pw_go_udzial_26'], 1)}% ({liczba(E['pw_n26'])}). Zmiana tego "
            f"udziału daje {liczba(abs(E['pw_mix']), 2)} zł z {liczba(abs(E['pw_zmiana']), 2)} zł spadku marży na zamówienie "
            f"(rozkład na strukturę i marżę w obrębie rodzaju zniżki)."])],
        linki=G0["linki"], zrodlo=G0["zrodlo"].replace("Liczby: ", "") + " Marża powtórnych zamówień: "
                                                                          "analiza/wyniki/e_merytoryka.txt (punkt 3).")
    # liczby do wykresu strony (etap 5 grafiki): trzy sposoby zakupu, oba lata; te same co w tabeli karty
    ty = V["go_typy"]
    nazwy_go = {"1_kasa_z_pierwszym_zamowieniem": "Przy kasie z pierwszym zamówieniem",
                "2_kasa_z_kolejnym_zamowieniem": "Przy kasie z kolejnym zamówieniem",
                "3_osobno_newsletter_crm_go_upsell": "Osobno, z newslettera"}
    go["wykres"] = {"wiersze": [{"opis": nazwy_go[t_], "p1": int(ty.loc[t_, "okres_1"]), "p2": int(ty.loc[t_, "okres_2"])}
                                for t_ in nazwy_go]}
    assert sum(w["p2"] for w in go["wykres"]["wiersze"]) == int(razem["okres_2"])
    bloki.append(("wzrost/telemedigo", go, ["c:telemedigo"], G0["_dodane"]))

    nowe = {"tytul": "Czy to, co widać na dashboardzie, jest wzrostem?",
            "wstep": f"Wzrost to dwie rzeczy naraz: więcej pacjentów i lepsza retencja. Sprawdzamy oba warunki osobno, na "
                     f"danych oczyszczonych, porównując {O2_TEKST} z rokiem wcześniej (X 2024 – IX 2025). Na końcu "
                     f"sprawdzamy, ile biznes na tym zarabia.",
            "werdykt": werdykt, "kafelki": kafelki,
            "karty": [dash, pac, ret, nap, mar, wy, rob, niew, go],
            # bez wewnętrznej nazwy rundy pracy (trzecia lista Kuby, punkt 4)
            "zrodlo": "Skąd liczby: " + W0["zrodlo"].replace("Liczby: ", "") + " Werdykt, ekonomia pacjenta i przyrost "
                      "marży: analiza/g_werdykt.py → analiza/wyniki/g_werdykt.txt. Sprawdzenia przed publikacją: "
                      "analiza/wyniki/e_merytoryka.txt i analiza/wyniki/e_poprawki.txt. Teksty strony: notatki/e_teksty.md."}
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
    e3, e3b = V["e3"], V["e3b"]
    sc3 = lambda kamp, reg, kol, t=e3: float(t[(t["kampania"] == kamp) & (t["regula"] == reg)].iloc[0][kol])  # noqa: E731
    p3b = [sc3(B2.NOWE[1], "Z1K", "po_naprawie_B"), sc3(B2.NOWE[1], "Z2", "po_naprawie_B"),
           sc3(B2.NOWE[1], "Z1K", "po_naprawie_B_180", e3b), sc3(B2.NOWE[1], "Z2", "po_naprawie_B_180", e3b)]
    assert max(p3b) < 0, "„po samej nowej kreacji TikTok dalej traci” wymaga wyniku ujemnego w obu regułach i oknach"
    Dd = V["D"]
    prog_b, prog_a = Dd["meta_prog_proc_z1k_90_dni_po_naprawie_b"], Dd["meta_prog_proc_z1k_90_dni_po_naprawie_a"]
    wd = {nr: PR0[nr]["wdrozenie"] for nr in PR0}
    wd[7] = wd[7].replace("dane o wysyłkach dni", "dane o wysyłkach kilka dni")   # brzmienie szkicu (c_szkic.md, pozycja 7)

    def pozycja(nr, tytul, wniosek, ile, ile_dop, pew, sekcje_widoczne, szczegoly, fr_dod=None, dodane=None):
        k0 = K0[nr]
        k = {"nr": nr, "tytul": tytul, "wniosek": wniosek,
             "pasek": {"ile": ile, "ile_dopisek": ile_dop, "pewnosc": pew, "wdrozenie": wd[nr]},
             "sekcje": [{"tytul": t, "punkty": p} for t, p in sekcje_widoczne],
             "szczegoly": szczegoly, "zrodlo": k0["zrodlo"],
             # lejek domyślnie pokazuje osoby, które jeszcze nie kupowały; odnośnik bez „pac” dostaje „wszyscy” jawnie
             "linki": [dict(l_, href=l_["href"] + ("&pac=wszyscy" if l_["href"].startswith("#lejek?")
                                                    and "pac=" not in l_["href"] else "")) for l_ in k0["linki"]]}
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
    so_ = V["safari_okresy"]   # przed od, przed do, po od (bez roku), po do, dni
    d_saf0 = B2.pl_data(so_[2] + "." + so_[3].split(".")[-1])
    dz_saf = f"{d_saf0.day} {B2.MIESIACE_DOP[d_saf0.month - 1]} {d_saf0.year}"
    ce = V["cennik"]
    spec_marza = f"{liczba(ce.loc['kardiolog', 'marza_bez_znizki'])}–{liczba(ce.loc['ginekolog', 'marza_bez_znizki'])} zł"
    dodaj(pozycja(
        1, "Naprawić zakładanie konta w Safari na iPhone'ach",
        f"Od {dz_saf} nowi pacjenci na iPhone'ach rzadziej kończą zakładanie konta, co kosztuje około "
        f"{liczba(na30)} pierwszych zamówień miesięcznie.",
        f"{zakres(lo[3] / 1000, hi[3] / 1000)} tys. zł",
        f"rocznie, górny scenariusz; w horyzoncie 180 dni {zakres(lo[4] / 1000, hi[4] / 1000)} tys. zł",
        pewnosc("wysoka", "awaria widoczna w danych"),
        [("Dlaczego", [f"W 60 dniach po awarii krok konta po wyborze terminu u osób, które jeszcze nie kupowały, przechodzi "
                       f"w Safari na iPhone'ach {z0(V['safari_60'][1])}% sesji wobec {z0(V['safari_60'][0])}% w 60 dniach "
                       f"przed nią, i do końca danych nie wraca. W innych przeglądarkach takiego spadku nie ma."]),
         ("Co robimy", [f"Powtórzyć rejestrację na iPhonie, przejrzeć logi błędów rejestracji i listę zmian z "
                        f"{d_saf0.day - 1}–{dz_saf}, wdrożyć poprawkę."]),
         ("Po czym poznamy", sekcja(K0[1], "Po czym poznamy"))],
        stare_sekcje(K0[1], pomin=("Po czym poznamy", "Wdrożenie"),
                     zamiany={q3_zdanie: "Wyniku kwartału", r" Wcześniejsza kwota „14–21 tys\. zł”[^.]*\.": ""})))

    k2 = K0[2]
    dodaj(pozycja(
        2, "Oczyścić codzienny raport i dodać alarmy na lejku i zwrotach",
        f"Raport pokazuje wzrost zamówień o {z0(dz[0])}% zamiast {z0(cz[0])}% i nie pokazuje ani marży, ani powrotów kohort.",
        f"0 albo {z0(V['testy_koszt2'] / 1000)} tys. zł", "rocznie bezpośrednio; przede wszystkim warunek pozostałych decyzji",
        pewnosc("wysoka", "oba błędy widoczne w danych"),
        [("Dlaczego", [f"Awaria w Safari trwała {liczba(lo[1])} dni, do końca danych. Alarm na krokach lejka wykryłby ją po kilku "
                       f"dniach. Gdyby awarię wykryto i usunięto w ciągu tygodnia, strata wyniosłaby około "
                       f"{zakres(V['p15'][1], V['p15'][2])} pierwszych zamówień zamiast {zakres(lo[0], hi[0])}."]),
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
        pewnosc("wysoka", "kampania traci według obu reguł przypisania; niepewna jest tylko wielkość zysku z pauzy"),
        [("Dlaczego", ["Wynik na pacjenta po koszcie pozyskania jest ujemny według obu reguł przypisania i po 90, i po 180 "
                       "dniach. Nawet najkorzystniejsza naprawa zwrotów, czyli zmiana ich zasad, daje według pierwszego "
                       "wejścia wynik bliski zera, a według sesji z płatnością dalej stratę."]),
         ("Co robimy", ["Wstrzymać od razu, jako pauzę, którą da się cofnąć w jeden dzień. Naprawy obietnicy i ładowania "
                        "strony sprawdzić najpierw na Mecie; TikTok może wrócić jako mały test, jeśli zadziałają."]),
         ("Po czym poznamy", sekcja(k3, "Po czym poznamy"))],
        stare_sekcje(k3, pomin=("Po czym poznamy", "Wdrożenie"), dopisz={"Naprawić albo wyłączyć": [
            f"W scenariuszu samej nowej kreacji (pozycja 5), w którym uczciwa obietnica zniechęca osoby, które dostałyby "
            f"zwrot, wynik w {liczba(V['dni'][B2.NOWE[1]])} dniach działania wynosi {tzn(p3b[0])} albo {tzn(p3b[1])} po "
            f"90 dniach i {tzn(p3b[2])} albo {tzn(p3b[3])} po 180 dniach, więc kampania nadal traci według obu reguł "
            f"przypisania."]})))

    k4 = K0[4]
    pr = (E["gs_spec_prog_Z1K_90"], E["gs_spec_prog_Z2_90"])
    dodaj(pozycja(
        4, "Wstrzymać kampanię Google Ads na specjalistów do czasu zmiany cennika",
        f"Pozyskanie pacjenta kosztuje około {z0(p7[('Z1K', '90')][2])} zł, a pacjent zostawia w 90 dniach około "
        f"{z0(p7[('Z1K', '90')][3])} zł marży.",
        f"+{z0(min(w100) / 1000)} do +{z0(max(w100) / 1000)} tys. zł",
        f"rocznie, nawet gdy każdy jej pacjent przyszedł tylko dzięki niej; do +{z0(p7[('Z1K', '90')][7] / 1000)} tys. zł, "
        f"gdy przyszliby i bez niej",
        pewnosc("wysoka", "kampania traci według obu reguł przypisania; niepewna jest tylko wielkość zysku z pauzy"),
        [("Dlaczego", [f"Wizyta u specjalisty po cenie katalogowej zostawia ponad koszt lekarza tylko {spec_marza}, więc "
                       f"kampania nie ma z czego pokryć kosztu pozyskania (pozycja 10)."]),
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
                        f"rabatowego (dziś {liczba(Dd['p6_kod_l4szybko20_znizka_zl'])} zł)."]),
         ("Po czym poznamy", sekcja(k5, "Po czym poznamy"))],
        [podtytul("Ile warte, osobno dla dwóch decyzji"), punkty([
            f"Wariant kreacji (uczciwa obietnica zniechęca osoby, które nie dostałyby L4): {tz(zw[0])} w {V['dni']['meta_prosp_l4_szybko']} "
            f"dniach działania kampanii według przyjętej reguły i {tz(zw[2])} według sesji płatności, na pełny rok "
            f"{tz(zw[5])} i {tz(zw[7])}.",
            f"Wariant zasad zwrotów (wizyty, które dziś kończą się zwrotem, zostają opłacone): {tz(zw[1])} i {tz(zw[3])}, "
            f"na pełny rok {tz(zw[6])} i {tz(zw[8])}."])]
        + stare_sekcje(k5, pomin=("Ile warta po wstrzymaniu TikToka (tylko Meta)", "Po czym poznamy", "Wdrożenie"),
                       dopisz={"Z danych": [
                           f"{liczba(E['zw_nowe_l4'])} to zwroty przy samych wizytach L4. Zakładka „Po zakupie” pokazuje "
                           f"{odm(E['zw_nowe_wszystkie'], 'zwrot', 'zwroty', 'zwrotów')} po wizycie u pacjentów nowych kampanii, bo liczy "
                           f"wszystkie cele wizyty, także e-receptę i konsultację."]},
                       zamiany={"zmniejszenie luki o połowę": "zmniejszenie tej różnicy o połowę",
                                "[Dd]olny wariant zakłada": "Wariant kreacji zakłada",
                                r"[Gg]órny wariant \(„wizyta zostaje opłacona”\)": "Wariant zasad zwrotów („wizyta zostaje opłacona”)"})))

    k6 = K0[6]
    rano, ks = V["rano"], "int_rano_ponad15_spoza_nowych"
    r_lut, r_przed = rano.loc["2026-02":"2026-09", ks], rano.loc["2024-10":"2025-10", ks]
    rano_zdanie = (
        f"Od listopada 2025 do lutego 2026 poranne opóźnienia u internisty rosły z miesiąca na miesiąc, a potem "
        f"utrzymywały się na poziomie około połowy wizyt. Odsetek wizyt z terminem "
        f"6:00–11:59, które zaczynają się ponad 15 minut po terminie (pacjenci spoza nowych kampanii, jak w zakładce „Po "
        f"zakupie”), wynosi {proc(rano.loc['2025-11', ks])} w listopadzie 2025, {proc(rano.loc['2025-12', ks])} w grudniu "
        f"i {proc(rano.loc['2026-01', ks])} w styczniu 2026, a od lutego do września 2026 około połowy "
        f"({zakres(r_lut.min(), r_lut.max(), 1, '%')} miesięcznie). Od października 2024 do października 2025 było to "
        f"{zakres(r_przed.min(), r_przed.max(), 1, '%')} miesięcznie. Liczby wizyt są w szczegółach zakładki „Po zakupie”.")
    assert 45 <= r_lut.min() and r_lut.max() <= 55
    dodaj(pozycja(
        6, "Zdiagnozować poranne opóźnienia internistów, potem przetestować obsadę",
        f"Od lutego 2026 około połowy porannych wizyt u internisty zaczyna się ponad 15 minut po terminie; do października "
        f"2025 było to {z0(r_przed.min())}–{z0(r_przed.max())}%.",
        f"{zakres(0, p8[3] / 1000)} tys. zł",
        f"rocznie, scenariusz; wariant wąski około {z0((p8[0] + p8[1]) / 2000)} tys. zł; bez kosztu obsady",
        pewnosc("niska", "opóźnienia są pewne; nie wiemy, ile powrotów przywróci punktualność"),
        [("Dlaczego", ["To jedna z konkretnych hipotez spadku retencji w kanałach działających w obu latach, a pierwszy krok, "
                       "diagnoza, jest tani. W ostatnich 12 miesiącach pacjenci po spóźnionej porannej pierwszej wizycie "
                       "wracają rzadziej niż po punktualnej, a spóźnione wizyty mają dużo niższe oceny (zakładka „Po zakupie”)."]),
         ("Co robimy", sekcja(k6, "Co robimy")),
         ("Po czym poznamy", sekcja(k6, "Po czym poznamy"))],
        stare_sekcje(k6, pomin=("Dlaczego wysoko", "Co robimy", "Po czym poznamy", "Wdrożenie"),
                     zamiany={r" Rano spada powrót po wizytach spóźnionych\.": "",
                              r"^Od listopada 2025 poranne opóźnienia u internisty rosną z miesiąca na miesiąc\..*$":
                                  rano_zdanie})))

    k7 = K0[7]
    cp = V["crm_powrot"]
    B1 = V["pow_bez_z1k"]
    dodaj(pozycja(
        7, "Wprowadzić komunikację po wizycie, zawsze z losową grupą bez wysyłki",
        "Co siódmy powrót zaczyna się od wejścia z newslettera albo SMS-a, ale nie wiemy, ile z tych zakupów wiadomość "
        "faktycznie wywołała.",
        tz(p12[1]), "za każdy punkt procentowy powrotu w 90 dniach; marża do 180. dnia; scenariusz",
        pewnosc("niska", "nie wiemy, ile powrotów wywoła sama wiadomość"),
        [("Dlaczego", [f"Retencja spada także poza nowymi kampaniami: w 90 dniach wraca {z0(B1['p90_o2'])}% pacjentów wobec "
                       f"{z0(B1['p90_o1'])}% rok wcześniej. Około {z0(cp[1])} z tych {z0(B1['p90_o2'])} punktów "
                       f"procentowych to pacjenci, którzy wrócili w ciągu doby po kliknięciu newslettera albo SMS-a; "
                       f"pozostali wrócili inną drogą. To jedna grupa pacjentów podzielona według drogi powrotu."]),
         ("Co robimy", sekcja(k7, "Co robimy")),
         ("Po czym poznamy", sekcja(k7, "Po czym poznamy"))],
        [podtytul("Ile warta"), punkty([
            f"Każdy punkt procentowy powrotu w 90 dniach to około {tz(p12[1])} marży rocznie: {liczba(V['nowi'][2])} nowych "
            f"pacjentów × 1% × {liczba(p12[0], 1)} zł, gdzie {liczba(p12[0], 1)} zł to różnica marży do 180. dnia między "
            f"pacjentem, który wrócił w 90 dniach, a takim, który nie wrócił. Bez pacjentów nowych kampanii "
            f"({liczba(V['p12_bez'][0])}) {tz(V['p12_bez'][1])}. To różnica obserwacyjna; efektu samej wiadomości nikt "
            f"jeszcze nie zmierzył.",
            f"Podział powrotu w 90 dniach poza nowymi kampaniami ({proc(B1['p90_o2'])}) według drogi powrotu: "
            f"{proc(cp[1], 2)} po wejściu z newslettera albo SMS-a i {proc(cp[3], 2)} inną drogą; rok wcześniej "
            f"{proc(cp[0], 2)} i {proc(cp[2], 2)}."])]
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
        f"Według pierwszego wejścia kampania zarabia {z0(meta[0] / 1000)} tys. zł rocznie, według sesji z płatnością "
        f"traci {z0(abs(meta[1]) / 1000)} tys. zł, a dane nie mówią, ilu jej pacjentów przyszłoby i bez niej.",
        f"od {z0(-abs(meta[2]) / 1000)} do +{z0(meta[3] / 1000)} tys. zł",
        "rocznie: tyle warta jest decyzja o wyłączeniu, zależnie od tego, ilu pacjentów przyszłoby i bez kampanii",
        pewnosc("test"),
        [("Dlaczego dopiero 9. miejsce", [
            "To największa kwota na liście, ale nie znamy nawet jej znaku, a test w 4–6 tygodni da tylko orientacyjny "
            "wynik. Wcześniej idą pewne straty i tanie kroki, które zespół może zrobić od razu."]),
         ("Co robimy", [
             "Na 4–6 tygodni wyłączyć kampanię w połowie województw, losowo w parach podobnych województw, i porównać "
             f"wszystkich nowych pacjentów oraz marżę. Wyłączamy na stałe, jeśli w województwach bez reklamy, w porównaniu "
             f"z ich parami, ubędzie mniej nowych pacjentów niż około {z0(V['p11_prog'][0])}% tych, których kampania sobie "
             f"tam w tym czasie przypisuje. Po samej nowej kreacji z pozycji 5 ten próg spada do około {z0(prog_b)}%, a po "
             f"zmianie zasad zwrotów do około {z0(prog_a)}% (progi dla marży w 90 dniach).",
             "Gdy wynik testu jest niejednoznaczny, i tak decydujemy według jego wyniku: poniżej progu wyłączamy, powyżej "
             "zostawiamy. Taki wynik może przez przypadek wypaść po złej stronie progu, ale obie decyzje da się cofnąć, a "
             "pomiar powtórzyć."]),
         ("Po czym poznamy", sekcja(k9, "Po czym poznamy"))],
        stare_sekcje(k9, pomin=("Po czym poznamy", "Wdrożenie"))))

    k10 = K0[10]
    ce = V["cennik"]
    assert all(ce.loc[s, "cena"] < ce.loc[s, "koszt_lekarza"] for s in ("pediatra", "psycholog"))
    dodaj(pozycja(
        10, "Zmienić cennik specjalistów i warunki TelemediGO u specjalistów",
        f"Wizyta u specjalisty zostawia ponad koszt lekarza tylko {spec_marza}, a ze zniżką TelemediGO przynosi stratę.",
        f"{zakres(V['p6_scen'][0] / 1000, V['p6_scen'][2] / 1000)} tys. zł",
        f"rocznie za warunki TelemediGO po pełnym roku; cennik do {z0(V['p14_zl'] / 1000)} tys. zł za każde 10 zł podwyżki, "
        f"górna granica",
        pewnosc("srednia", "kierunek jest pewny; nie wiemy, ile da zmiana cennika"),
        [("Co robimy", [
            f"Ustawić zniżkę TelemediGO u specjalistów tak, żeby cena nie spadała poniżej kosztu lekarza: najwyżej około "
            f"{z0(100 * ce.loc['kardiolog', 'marza_bez_znizki'] / ce.loc['kardiolog', 'cena'])}% przy cenie "
            f"{liczba(ce.loc['kardiolog', 'cena'])} zł.",
            f"U pediatry i psychologa samo wyłączenie zniżki nie wystarczy, bo już cena katalogowa "
            f"({liczba(ce.loc['pediatra', 'cena'])} i {liczba(ce.loc['psycholog', 'cena'])} zł) jest niższa niż koszt "
            f"lekarza ({liczba(ce.loc['pediatra', 'koszt_lekarza'])} zł, przy założeniu opartym na zadaniu). Tu trzeba "
            f"podnieść cenę.",
            "Przetestować dwie ceny dla nowych pacjentów przez 4 tygodnie i mierzyć marżę na sesję, nie sam odsetek "
            "kupujących."]),
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
        pewnosc("niska", "nie wiemy, czy brakujące sesje da się odzyskać"),
        [("Co robimy", ["Porównać w panelach Meta i TikToka kliknięcia w link i wyświetlenia strony docelowej z sesjami w "
                        "analityce, dzień po dniu, i zmierzyć czas ładowania strony w przeglądarkach w aplikacjach."]),
         ("Po czym poznamy", ["Wiemy, czy brakujące sesje to ludzie, którzy porzucają ładowanie strony (do odzyskania), czy "
                              "inny sposób liczenia kliknięć w panelu (wtedy pozycja jest warta 0 zł). Wynik zmienia ocenę "
                              "pozycji 3 i 9."])],
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
                     r"^Dodatkowy koszt testu to około .*?zniżek\.$": ""})))

    # zasady listy i „czego nie robimy”
    zas = karta(
        "Najpierw pewne straty i pauzy, które da się cofnąć, potem testy",
        wniosek="Kolejność oznacza wagę decyzji. Każda kwota to osobny scenariusz, więc kwot nie sumujemy.",
        tresc=[punkty([
            "Najpierw pewne straty, które rosną każdego dnia i łatwo je naprawić (pozycje 1 i 2). Potem pauzy, które da się "
            "cofnąć (3 i 4). Potem naprawy, diagnozy i testy, które mają wycenę (5–10). Test Mety "
            "(pozycja 9) ma nieznany znak, ale wycenę i największą stawkę, więc stoi w tej grupie. Na końcu dwie pozycje "
            "bez oszacowanego efektu: pozycja 11 ma tylko górną granicę możliwej korzyści, a pozycja 12 tylko koszt "
            "testu.",
            "W pierwszym tygodniu zespół może zrobić równolegle pozycje 1, 3 i 4 oraz pierwsze, krótkie kroki pozycji 2, 5, "
            "6, 8 i 11 (decyzje na pierwszy tydzień w zakładce „Czy to wzrost”).",
            "Wartość to zmiana marży na rok: przychód z konsultacji po zwrotach i opłaty TelemediGO minus koszt lekarza, "
            "wydatki na kampanie i prowizja afiliacyjna. Rokiem bazowym są ostatnie 12 miesięcy."])],
        szczegoly=[punkty([popraw(x) for x in P0["zasady"]]), akapit(popraw(P0["definicje"])),
                   podtytul("Nie robimy teraz: rachunki"),
                   punkty([popraw(x) for x in P0["nie_robimy"] if not x.startswith("Mocniejsza sprzedaż i odnowienia TelemediGO")])])
    # runda G (Kuba, 2026-10-23): zakres listy nazwany wprost i dawna karta „Nie robimy teraz” w tej samej karcie co zasady;
    # punkt o TelemediGO wypada (mówi to zakres), zasada o uwolnionym budżecie stoi raz, w „Nie robimy teraz”
    zas["zakres"] = {
        "tytul": "Zakres listy",
        "tekst": "Lista obejmuje działania, które wynikają z problemów widocznych w danych: naprawy, pauzy i testy. Celowo nie "
                 "obejmuje działań na wzrost, które wymagają wiedzy spoza tych danych, czyli nowych kanałów i kampanii, rozwoju "
                 "oferty i TelemediGO (poza naprawą warunków, które dziś przynoszą stratę, pozycja 10) ani rozmów z pacjentami. "
                 "Taka kolejność jest celowa: dopóki zakładanie konta w Safari nie działa i nie wiemy, ilu pacjentów kampanie "
                 "naprawdę dokładają, dodatkowy budżet częściowo trafiałby w ten sam dziurawy lejek. Plan wzrostu przygotujemy "
                 "po wynikach pierwszych testów (pozycje 7, 9 i 12)."}
    zas["nie_robimy"] = {
        "tytul": "Nie robimy teraz rzeczy bez podstaw w danych albo bez testu",
        "punkty": [
            f"Kampanii o zgodę marketingową pacjentów nowych kampanii: w najlepszym razie {liczba(V['zgoda_1900'] / 1000, 1)} "
            f"tys. zł rocznie.",
            "Osobnej naprawy przeglądarek w aplikacjach w reklamach do nowych osób: w tej samej kampanii płacą tak samo jak "
            "zwykłe.",
            "Przesuwania pieniędzy uwolnionych przez pozycje 3 i 4 do innych kampanii bez testu."]}
    bloki.append(("priorytety/zasady", zas, ["c:zasady", "c:nie_robimy"], []))
    nie = None
    # podpis grupy w przeglądzie (etap 5 grafiki), według kryterium kolejności listy (założenie 74)
    GRUPY = [((1, 2), "Pewne straty"), ((3, 4), "Pauzy, które da się cofnąć"), (tuple(range(5, 11)), "Działania z wyceną"),
             ((11, 12), "Bez oszacowanego efektu")]
    for r_ in przeglad:
        r_["grupa"] = next(nazwa for nry, nazwa in GRUPY if r_["nr"] in nry)
    nowe = {"tytul": "Priorytety: co robimy po kolei",
            "wstep": "Lista od najważniejszej pozycji. Przy każdej: dlaczego, co robimy, ile jest warta w złotych marży na rok, "
                     "po czym poznamy, że zadziałała, i ile zajmie wdrożenie. Pełne rachunki i założenia są w szczegółach "
                     "każdej karty.",
            "przeglad": przeglad, "zasady": zas, "karty": karty, "nie_robimy": nie,
            # bez wewnętrznej nazwy części pracy („raporty części A5”; trzecia lista Kuby, punkt 4)
            "zrodlo": P0["zrodlo"].replace(" i raporty części A5, wskazane przy każdej pozycji",
                                           " i raporty wskazane przy każdej pozycji")}
    assert "A5," not in nowe["zrodlo"], "w stopce priorytetów została nazwa części pracy"
    bloki.append(("priorytety/wstep", {"w": nowe["wstep"]}, [], []))
    return nowe, bloki


def niewiadome(V, E, C):
    """„Czego nie wiemy”: słownik, nowe numery (bez dawnej pozycji 13) i trzy przeredagowane wiersze."""
    N0 = C["niewiadome"]
    wiersze, bloki = [], []
    pm_, zw = V["p11_meta"], V["p11_zwroty"]
    rano_wys = V["rano"].loc["2026-02", "int_rano_ponad15_spoza_nowych"]
    assert rano_wys > 45, "„w lutym 2026 opóźnienia były już wysokie” wymaga ponad 45% spóźnionych porannych wizyt"
    nowe_teksty = {
        1: {"co": "Ilu pacjentów nowych kampanii na L4 przyszłoby i bez nich",
            "dlaczego": f"od tego zależy decyzja o kampanii Meta na L4: jej wyłączenie jest warte od około "
                        f"{z0(pm_[2] / 1000)} do +{z0(pm_[3] / 1000)} tys. zł rocznie, a próg decyzji to około "
                        f"{z0(V['p11_prog'][0])}% pacjentów, którzy bez kampanii by nie przyszli (pozycja 9)"},
        4: {"co": "Skąd poranne opóźnienia u internistów (blok od 5:00 do 13:59, już przy wizytach z najwcześniejszym "
                  "terminem dnia, bez widocznego narastania w ciągu poranka) i czy obniżają powroty",
            "dlaczego": f"scenariusz od 0 do {z0(V['p8'][3] / 1000)} tys. zł rocznie. Luty 2026 nie pasuje do hipotezy, że "
                        f"większe opóźnienia zawsze obniżają powrót: opóźnienia były już wtedy wysokie, a powrót pacjentów "
                        f"kampanii działających w obu latach nie spadł"},
        11: {"co": "Ile wzrostu daje pora roku, a ile wyższe wydatki na kampanie",
             "dlaczego": f"od {V['sezon'][0]} do {V['sezon'][1]} rosną naraz pora roku i wydatki. W dwóch latach danych "
                         f"każdy miesiąc występuje tylko dwa razy, a wydatki rosły w obu latach, więc wpływu sezonu nie da "
                         f"się oddzielić od wpływu wydatków"},
        19: {"co": "Czy sesje w przeglądarkach w aplikacjach płacą rzadziej w remarketingu Meta, kampanii Google Ads na "
                   "markę i wejściach bezpośrednich przez samą przeglądarkę, czy przez to, kto z niej korzysta"},
        2: {"co": "Ilu pacjentów kampanii bez kodu rabatowego (Google Ads ogólne, Meta „lekarz online”) przyszłoby i bez "
                  "reklamy",
            "dlaczego": "znak wyniku tych kampanii zależy od reguły przypisania, a żadna reguła nie mówi, ilu pacjentów "
                        "kampania naprawdę dokłada",
            "test": "ten sam test z grupą bez reklamy; mierzy przyrost pacjentów niezależnie od reguły przypisania, więc nie "
                    "trzeba wybierać reguły"},
        3: {"dlaczego": f"po wstrzymaniu TikToka dotyczy tylko Meta: od niego zależy, ile da nowa kreacja "
                        f"({zakres(zw[7] / 1000, zw[5] / 1000)} tys. zł rocznie) i czy potrzebna jest zmiana zasad zwrotów "
                        f"({zakres(zw[8] / 1000, zw[6] / 1000)} tys. zł rocznie; pozycja 5)"},
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
    # runda G (prośba Kuby, 2026-10-23): pytania pogrupowane tematycznie; numery bez zmian (prowadzą do nich odnośniki
    # z innych zakładek), w grupie rosnąco. Każdy numer w dokładnie jednej grupie; słowo kluczowe pilnuje, żeby numer
    # nadal oznaczał to samo pytanie (założenie 95).
    klucz = {1: "kampanii na L4", 2: "bez kodu rabatowego", 3: "zwrotów po wizycie", 4: "opóźnienia", 5: "zalogowane",
             6: "Safari", 7: "Safari", 8: "TelemediGO", 9: "newsletter", 10: "remarketingu", 11: "pora roku",
             12: "kliknięciem", 13: "testowe", 14: "rankingiem", 15: "rocznika", 16: "specjalistów", 17: "zwrotów",
             18: "aplikacjach", 19: "konta", 20: "kodu rabatowego", 21: "Google Ads na markę"}
    grupy = [("Kampanie i pozyskanie pacjentów", [1, 2, 10, 11, 12, 20, 21]),
             ("Obsługa pacjenta: zwroty i opóźnienia", [3, 4, 17]),
             ("Strona i ścieżka zakupu", [5, 6, 7, 18]),
             ("Ceny i TelemediGO", [8, 16]),
             ("Komunikacja z pacjentami i konta bez zakupu", [9, 19]),
             ("Dane, umowy i czas obserwacji", [13, 14, 15])]
    po_nr = {w["nr"]: w for w in wiersze}
    assert sorted(x for _, nry in grupy for x in nry) == sorted(po_nr), "każde pytanie w dokładnie jednej grupie"
    for nazwa, nry in grupy:
        for x in nry:
            assert klucz[x] in po_nr[x]["co"], f"pytanie {x} zmieniło treść: brak „{klucz[x]}”"
            po_nr[x]["grupa"] = nazwa
    nowe = {"tytul": "Czego z tych danych nie wiemy",
            "wstep": "Rzeczy, których te dane nie rozstrzygają, pogrupowane według tematu, i test albo dane, które je "
                     "domkną. Numer pytania się nie zmienia, a numer pozycji listy priorytetów prowadzi do karty, której "
                     "kwota od tego zależy.",
            "grupy": [g for g, _ in grupy], "wiersze": wiersze, "zrodlo": N0["zrodlo"]}
    return nowe, bloki


def teksty_c(V, E, C):
    """Nowe „Czy to wzrost”, „Priorytety” i „Czego nie wiemy”. C = dane w dotychczasowym kształcie (z b2_eksport_c),
    z których przenosimy zdania. Na stronę idzie tylko nowy kształt: strona po przebudowie (sesja wyglądu, commit
    888ebca) rysuje go bez dawnych pól, więc dawne teksty nie zostają w opublikowanych danych.
    Zwraca (C, bloki do kontroli)."""
    bloki = []
    wz, b = wzrost(V, E, C)
    bloki += b
    pr, b = priorytety(V, E, C)
    bloki += b
    nw, b = niewiadome(V, E, C)
    bloki += b
    C = dict(C)
    C["wzrost"], C["priorytety"], C["niewiadome"] = nazwy(wz), nazwy(pr), nazwy(nw)
    bloki = [(n, nazwy(o), d, a) for n, o, d, a in bloki]
    return C, bloki


def macierz_kohort(koh):
    """Jedno zdanie nad miesięczną mapą kohort (polecenie Kuby przez sesję grafiki, 2026-10-22). Liczone z tych samych
    danych co mapa w przeglądarce (kohorty.js: dzień kohorty `d`, dni do powrotu `r`), wszyscy nowi pacjenci, okno 90 dni,
    tylko miesiące z pełnym oknem. Zapisuje koh["macierz"] i zwraca wynik kontroli liczb."""
    import datetime as dt_
    start, n_dni, okno = dt_.date(2024, 10, 1), 730, 90
    mies = {}
    for d, r in zip(koh["d"], koh["r"]):
        dzien = start + dt_.timedelta(days=d)
        s = mies.setdefault((dzien.year, dzien.month), [0, 0])
        s[0] += 1
        s[1] += 0 <= r <= okno
    def pelne(k):
        y, m = k
        ost = dt_.date(y + (m == 12), m % 12 + 1, 1) - dt_.timedelta(days=1)
        return (ost - start).days <= n_dni - 1 - okno
    p = {k: 100 * v[1] / v[0] for k, v in mies.items() if pelne(k)}
    A = [k for k in p if k <= (2025, 10)]
    B = [k for k in p if (2025, 11) <= k <= (2026, 2)]
    C = [k for k in p if k >= (2026, 3)]
    # warunki zdania: każdy miesiąc od XI 2025 niżej niż każdy do X 2025, a każdy od III 2026 niżej niż każdy z XI–II
    assert max(p[k] for k in B) < min(p[k] for k in A) and max(p[k] for k in C) < min(p[k] for k in B), \
        "zdanie nad mapą kohort nie pasuje już do danych"
    pa = 100 * sum(mies[k][1] for k in A) / sum(mies[k][0] for k in A)
    pc = 100 * sum(mies[k][1] for k in C) / sum(mies[k][0] for k in C)
    ost = max(C)
    koh["macierz"] = {
        "wniosek": f"Od listopada 2025 kohorty wracają rzadziej, a od marca 2026 spadek się pogłębia: w ciągu 90 dni wraca "
                   f"około {z0(pc)}% nowych pacjentów, wobec około {z0(pa)}% w kohortach do października 2025.",
        "zrodlo": f"Kohorty miesięczne, wszyscy nowi pacjenci, powrót w ciągu 90 dni (kolejne zamówienie nieanulowane), tylko "
                  f"miesiące z pełnym oknem: X 2024 – X 2025 razem ({liczba(sum(mies[k][0] for k in A))} pacjentów) i III – "
                  f"{B2.MIESIACE_RZ[ost[1] - 1]} {ost[0]} razem ({liczba(sum(mies[k][0] for k in C))} pacjentów). Liczone z danych "
                  f"tej mapy (analiza/e_teksty.py, macierz_kohort)."}
    return kontrola([("kohorty/macierz", koh["macierz"], [], [])])


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
    # Safari na iPhone'ach i pozostałe przeglądarki u nowych osób spoza nowych kampanii (według pierwszego wejścia),
    # miesiąc po miesiącu (trzecia lista Kuby, punkt 1; analiza/wyniki/e_poprawki.txt, punkt 3)
    PM = {r["mies"]: r for r in E["lj_pw_miesiace"]}
    rw = lambda m: str(int(m[:4]) - 1) + m[4:]  # noqa: E731

    def kom_saf(m, g):
        a, b = PM[rw(m)], PM[m]
        return [{"tekst": proc(b[f"{g}_konw"], 2),
                 "pod": f"{odm(b[f'{g}_sesje'], 'sesja', 'sesje', 'sesji')}; rok wcześniej {proc(a[f'{g}_konw'], 2)}"},
                zmiana(f"{zn(b[f'{g}_zm'], 2)} pkt", b[f"{g}_zm"]),
                {"tekst": proc(b[f"{g}_konto"]), "pod": f"rok wcześniej {proc(a[f'{g}_konto'])}"}]
    tab_saf = tabela(["Miesiąc", "Safari na iPhone'ach", "Zmiana", "Krok konta", "Pozostałe przeglądarki", "Zmiana",
                      "Krok konta"],
                     [wiersz(B2.MIESIACE_RZ[int(m[5:]) - 1] + " " + m[:4], kom_saf(m, "saf") + kom_saf(m, "res"))
                      for m in m_a + m_b + m_c],
                     tytul="Nowe osoby spoza nowych kampanii (według pierwszego wejścia): odsetek sesji z płatnością i krok "
                           "konta po wyborze terminu, Safari na iPhone'ach i pozostałe przeglądarki")
    for m in m_a + m_b + m_c:   # zmiana w tabeli = różnica tych samych liczb, które stoją w komórkach
        for g in ("saf", "res"):
            assert abs(PM[m][f"{g}_zm"] - (PM[m][f"{g}_konw"] - PM[rw(m)][f"{g}_konw"])) < 1e-9
    dod_tab += [x for w_ in tab_saf["wiersze"] for k_ in w_["komorki"] for x in (k_["tekst"], k_.get("pod", ""))]
    stare = [popraw(z) for z in nag["zdania"]]
    # „Wszystkie sesje razem”: zdanie o rachunku bez powtórzonego wyniku rozkładu według przeglądarki (stoi w stare[2])
    wszystkie = stare[1].split(" Sama zmiana struktury ruchu")[0] + " " + stare[2]
    assert "Według przeglądarki zmiana struktury ruchu daje" in stare[2]
    dz_k, rw_k = E["lj_nk_dzis_konw"], E["lj_nk_rok_wczesniej_konw"]
    assert min(udz_c) >= 40, "„prawie połowa ruchu nowych osób” wymaga co najmniej 40% sesji nowych kampanii od kwietnia"
    assert max(zm(m_a)) < 1 and min(zm(m_b)) > max(zm(m_a)) and min(zm(m_c)) > max(zm(m_b))
    d_s = B2.dt.date.fromisoformat(nag["safari"]["data"])
    dzien_saf = f"{d_s.day} {B2.MIESIACE_DOP[d_s.month - 1]} {d_s.year}"
    assert V["start"][B2.NOWE[1]].month == 2 and V["start"][B2.NOWE[1]].year == 2026, "„w lutym 2026 ruszył TikTok na L4”"
    # Nowe osoby spoza nowych kampanii według pierwszego wejścia, jak w retencji (trzecia lista Kuby, punkt 1;
    # analiza/wyniki/e_poprawki.txt, punkt 3). „pw” = bez osób nowych kampanii, „saf” / „res” = Safari na iPhone'ach /
    # pozostałe przeglądarki w tej grupie, „ses” = dawna wersja według sesji.
    pw = lambda g, okno, m: E[f"lj_pw_{g}_{okno}_{m}"]  # noqa: E731
    roz = lambda g, s: E[f"lj_pw_rozklad_{g}_{s}"]  # noqa: E731
    assert 0.4 <= pw("nowe_ses", "dzis", "konw") / pw("pw", "dzis", "konw") <= 0.6, "„o połowę rzadziej niż pozostałe”"
    assert 0.4 <= pw("nowe_ses", "o2", "konw") / pw("pw", "o2", "konw") <= 0.6
    assert E["lj_pw_saf_zmiana_dzis_do"] < 0, "„Safari płaci rzadziej” wymaga przedziału całego poniżej zera"
    assert E["lj_pw_res_zmiana_dzis_od"] < 0 < E["lj_pw_res_zmiana_dzis_do"], \
        "„w innych przeglądarkach konwersja się nie zmieniła” wymaga przedziału przez zero"
    assert E["lj_pw_saf_zmiana_przed_od"] < 0 < E["lj_pw_saf_zmiana_przed_do"], "„przed awarią Safari płaciło tak jak rok wcześniej”"
    assert E["lj_pw_saf_udzial_kroku_konta"] >= 90, "„spadek skupia się na kroku konta” wymaga co najmniej 90% w kroku konta"
    assert 0.97 < E["lj_pw_saf_iloraz_platnosc_po_koncie"] < 1.03 and 0.97 < E["lj_pw_saf_iloraz_termin"] < 1.04
    # a: tytuł jako składniki rozkładu, a nie „dwa powody”; obie rzeczy razem to co najmniej 90% spadku
    assert (E["lj_pw_rozklad_wszyscy_struktura_razem"] + roz("wszyscy", "safari_wewnatrz")) / roz("wszyscy", "zmiana") >= 0.9
    # wrażliwość reguły tożsamości (uwaga g): bez osób z pierwszym zamówieniem L4 wniosek ten sam
    assert E["lj_pw_bez_l4_saf_zmiana_do"] < 0 < E["lj_pw_bez_l4_res_zmiana_do"] and E["lj_pw_bez_l4_res_zmiana_od"] < 0
    pow_dz = (pw("nowe_os", "dzis", "sesje") - pw("nowe_ses", "dzis", "sesje"),
              pw("nowe_os", "dzis", "k5") - pw("nowe_ses", "dzis", "k5"))
    udz_saf = roz("pw", "safari_wewnatrz") / roz("pw", "zmiana")
    assert udz_saf >= 0.8, "„prawie cały spadek to Safari” wymaga co najmniej 80% zmiany średniej"
    struk_pw = roz("pw", "safari_struktura") + roz("pw", "reszta_struktura")
    assert abs(struk_pw) < 0.05, "„zmiana udziału Safari daje około zera”"
    assert pw("ses", "dzis", "k5") - pw("pw", "dzis", "k5") == pw("nowe_os", "dzis", "k5") - pw("nowe_ses", "dzis", "k5")
    assert abs(pw("ses", "dzis", "konw") - pw("ses", "rok_wczesniej", "konw")) < 0.2, "„według sesji od kwietnia stoi”"
    assert abs(pw("wszyscy", "dzis", "konw") - dz_k) < 1e-9 and abs(pw("wszyscy", "rok_wczesniej", "konw") - rw_k) < 1e-9
    assert E["lj_nie_kupowal_2_platnosci"] > E["lj_nie_kupowal_1_platnosci"], "„liczba płatności nowych osób rośnie”"
    u_ = lambda m: MK[m]["udzial_sesji_nowe_kampanie"]  # noqa: E731
    assert not u_("2025-10") > 0 and 0 < u_("2025-11") < u_("2025-12") < u_("2026-01") < 30 < u_("2026-02"), \
        "„przybywało już od listopada 2025” i „w lutym 2026 przekroczyły 30%” (runda F, P4)"
    karta_n = karta(
        "Na spadek konwersji nowych osób składają się głównie dwie rzeczy: więcej ruchu z nowych kampanii na L4 i awaria "
        "zakładania konta w Safari",
        wniosek=f"Od kwietnia do września 2026 płatnością kończy się około {z0(dz_k)}% sesji osób, które jeszcze nie "
                f"kupowały, a w tych samych miesiącach rok wcześniej około {z0(rw_k)}%.",
        # runda G (przejrzystość): wniosek krótko, rozwinięcie i zastrzeżenie w zwiniętych „Szczegółach”, żeby kroki lejka
        # były blisko początku zakładki
        szczegoly=[punkty([
            "Do stycznia 2026 nowe osoby płaciły prawie tak samo często jak rok wcześniej, choć ruchu z nowych kampanii na "
            "L4 przybywało już od listopada 2025. W lutym 2026, gdy ruszył TikTok na L4, sesje nowych kampanii przekroczyły "
            "30% ruchu nowych osób, a od kwietnia to prawie połowa. Te sesje płacą o połowę rzadziej niż pozostałe.",
            f"Wśród pozostałych nowych osób od kwietnia 2026 wyraźnie płacą rzadziej tylko sesje w Safari na iPhone'ach: "
            f"około {z0(pw('saf', 'dzis', 'konw'))}% wobec {z0(pw('saf', 'rok_wczesniej', 'konw'))}% rok wcześniej. Spadek "
            f"skupia się na kroku zakładania konta, który działa gorzej od {dzien_saf}. W innych przeglądarkach konwersja "
            f"jest bez istotnej zmiany.",
            "Liczba płatności nowych osób rośnie, spada tylko ich odsetek.",
            "Safari trzeba naprawić (pozycja 1 listy priorytetów). Do sprawdzenia jest niższa konwersja przeglądarek "
            "w aplikacjach w remarketingu Meta, kampanii Google Ads na markę i wejściach bezpośrednich (karta niżej)."]),
            akapit("Zastrzeżenie: niższa konwersja nie mówi, ilu pacjentów nowe kampanie dokładają, bo nie wiemy, ilu z nich "
                   "przyszłoby i bez reklamy."),
            punkty([
            f"Ile płacą dziś: od kwietnia do września 2026 płatnością kończy się {proc(dz_k, 2)} z "
            f"{liczba(E['lj_nk_dzis_sesje'])} sesji osób, które jeszcze nie kupowały (od {proc(E['lj_nk_dzis_mies_min'], 2)} "
            f"do {proc(E['lj_nk_dzis_mies_max'], 2)} miesięcznie), a w tych samych miesiącach rok wcześniej "
            f"{proc(rw_k, 2)} z {liczba(E['lj_nk_rok_wczesniej_sesje'])} sesji. Średnia z całych ostatnich 12 miesięcy to "
            f"{proc(nk2)} wobec {proc(nk1)} rok wcześniej.",
            f"Przebieg rok do roku: od października 2025 do stycznia 2026 konwersja była o "
            f"{zakres(min(zm(m_a)), max(zm(m_a)), 1)} punktu procentowego niższa niż rok wcześniej, w lutym i marcu 2026 o "
            f"{zakres(min(zm(m_b)), max(zm(m_b)), 1)} punktu, a od kwietnia 2026 o {zakres(min(zm(m_c)), max(zm(m_c)), 1)} "
            f"punktu. Sesje nowych kampanii przekroczyły 30% ruchu nowych osób w lutym 2026 "
            f"({proc(MK['2026-02']['udzial_sesji_nowe_kampanie'])}), a od kwietnia to {zakres(min(udz_c), max(udz_c))}% "
            f"(tabela niżej).",
            f"Sesje z reklam nowych kampanii płacą w {proc(pw('nowe_ses', 'o2', 'konw'))} ("
            f"{odm(pw('nowe_ses', 'o2', 'sesje'), 'sesja', 'sesje', 'sesji')} w ostatnich 12 miesiącach; od kwietnia do "
            f"września 2026 {proc(pw('nowe_ses', 'dzis', 'konw'), 2)} z {liczba(pw('nowe_ses', 'dzis', 'sesje'))} sesji). "
            f"Nowe osoby spoza "
            f"nowych kampanii liczymy według pierwszego wejścia, tak jak pacjentów i retencję: od kwietnia do września 2026 "
            f"płaci {proc(pw('pw', 'dzis', 'konw'), 2)} z {liczba(pw('pw', 'dzis', 'sesje'))} sesji, a w "
            f"tych samych miesiącach rok wcześniej {proc(pw('pw', 'rok_wczesniej', 'konw'), 2)} z "
            f"{liczba(pw('pw', 'rok_wczesniej', 'sesje'))} sesji (zmiana {zn(E['lj_pw_pw_zmiana_dzis'], 2)} "
            f"punktu procentowego). W całych ostatnich 12 miesiącach {proc(pw('pw', 'o2', 'konw'))} wobec "
            f"{proc(pw('pw', 'o1', 'konw'))} rok wcześniej.",
            f"Safari na iPhone'ach i iPadach w tej grupie, od kwietnia do września 2026: płaci "
            f"{proc(pw('saf', 'dzis', 'konw'), 2)} z {liczba(pw('saf', 'dzis', 'sesje'))} sesji wobec "
            f"{proc(pw('saf', 'rok_wczesniej', 'konw'), 2)} z {liczba(pw('saf', 'rok_wczesniej', 'sesje'))} rok wcześniej, a "
            f"krok konta po wyborze terminu przechodzi {proc(pw('saf', 'dzis', 'konto'))} sesji wobec "
            f"{proc(pw('saf', 'rok_wczesniej', 'konto'))}. Pogorszenie skupia się na kroku konta; pozostałe kroki w Safari "
            f"prawie się nie zmieniają. Pozostałe przeglądarki: "
            f"{proc(pw('res', 'dzis', 'konw'), 2)} z {liczba(pw('res', 'dzis', 'sesje'))} sesji wobec "
            f"{proc(pw('res', 'rok_wczesniej', 'konw'), 2)} z {liczba(pw('res', 'rok_wczesniej', 'sesje'))} (zmiana "
            f"{zn(E['lj_pw_res_zmiana_dzis'], 2)} punktu, 95% przedział od {zn(E['lj_pw_res_zmiana_dzis_od'], 2)} do "
            f"{zn(E['lj_pw_res_zmiana_dzis_do'], 2)}, czyli bez istotnej zmiany), krok konta "
            f"{proc(pw('res', 'dzis', 'konto'))} wobec {proc(pw('res', 'rok_wczesniej', 'konto'))}. Od października 2025 do "
            f"lutego 2026, przed awarią, Safari płaciło tak jak rok wcześniej: {proc(pw('saf', 'przed26', 'konw'), 2)} wobec "
            f"{proc(pw('saf', 'przed25', 'konw'), 2)}. Sprawdzenie reguły łączenia osób (osoba z reklamy L4, która wróciła "
            f"w innej przeglądarce bez logowania, liczy się do pozostałych): bez wszystkich osób, których pierwsze zamówienie "
            f"to L4, w obu latach, Safari spada o {liczba(abs(E['lj_pw_bez_l4_saf_zmiana']), 2)} punktu, a pozostałe "
            f"przeglądarki są bez istotnej zmiany ({zn(E['lj_pw_bez_l4_res_zmiana'], 2)} punktu, przedział od "
            f"{zn(E['lj_pw_bez_l4_res_zmiana_od'], 2)} do {zn(E['lj_pw_bez_l4_res_zmiana_do'], 2)}).",
            f"Podział zmiany od kwietnia do września 2026 (opisowo, czyli bez mierzenia wpływu): z "
            f"{zn(roz('pw', 'zmiana'), 2)} punktu u nowych osób spoza nowych kampanii {zn(roz('pw', 'safari_wewnatrz'), 2)} "
            f"punktu to spadek w Safari, {zn(roz('pw', 'reszta_wewnatrz'), 2)} punktu spadek w pozostałych przeglądarkach, "
            f"a zmiana udziału Safari w ruchu daje około zera. Dla wszystkich nowych osób ({zn(roz('wszyscy', 'zmiana'), 2)} "
            f"punktu, z {proc(rw_k, 2)} do {proc(dz_k, 2)}) zmiana struktury ruchu daje "
            f"{zn(E['lj_pw_rozklad_wszyscy_struktura_razem'], 2)} punktu, spadek w Safari "
            f"{zn(roz('wszyscy', 'safari_wewnatrz'), 2)} punktu, a spadek w pozostałych przeglądarkach "
            f"{zn(roz('wszyscy', 'reszta_wewnatrz'), 2)} punktu.",
            f"Licząc według sesji, czyli bez samych sesji z reklam nowych kampanii, konwersja pozostałych sesji rośnie z "
            f"{proc(pw('ses', 'o1', 'konw'))} do {proc(pw('ses', 'o2', 'konw'))}, a od kwietnia do września 2026 stoi "
            f"({proc(pw('ses', 'dzis', 'konw'), 2)} wobec {proc(pw('ses', 'rok_wczesniej', 'konw'), 2)}). W całych "
            f"ostatnich 12 miesiącach ta reguła zostawia w średniej "
            f"{odm(E['lj_pw_powrotne_sesje'], 'sesja', 'sesje', 'sesji')}, w których osoby nowych kampanii wracają "
            f"bezpośrednio, z wyszukiwarki albo z innej reklamy. Płaci w nich {proc(E['lj_pw_powrotne_konw'])} "
            f"({odm(E['lj_pw_powrotne_platnosci'], 'płatność', 'płatności', 'płatności')}, czyli ci sami pacjenci, których "
            f"w retencji obie reguły przypisują różnie). Od kwietnia do września 2026 to "
            f"{odm(pow_dz[0], 'sesja', 'sesje', 'sesji')}, w których płaci {proc(100 * pow_dz[1] / pow_dz[0])}. Te sesje "
            f"podnosiły średnią i przykrywały spadek w Safari.",
            f"Osoby, które jeszcze nie kupowały: {liczba(E['lj_nie_kupowal_1_sesje'])} sesji i "
            f"{liczba(E['lj_nie_kupowal_1_platnosci'])} płatności rok wcześniej, {liczba(E['lj_nie_kupowal_2_sesje'])} sesji i "
            f"{liczba(E['lj_nie_kupowal_2_platnosci'])} płatności w ostatnich 12 miesiącach. Najbardziej pogorszyło się "
            f"przejście do wyboru usługi (z {proc(E['lj_nie_kupowal_1_p_k1'])} do {proc(E['lj_nie_kupowal_2_p_k1'])} sesji) i "
            f"krok konta po wyborze terminu (z {proc(E['lj_nie_kupowal_1_p_k3'])} do {proc(E['lj_nie_kupowal_2_p_k3'])}).",
            f"Wszystkie sesje, także osób, które już kupowały (płacą w {proc(E['lj_kupowal_wczesniej_1_konw'])} i "
            f"{proc(E['lj_kupowal_wczesniej_2_konw'])} sesji): {proc(nag['konw'][0])} rok wcześniej ({liczba(nag['sesje'][0])} "
            f"sesji, {liczba(nag['platnosci'][0])} płatności) i {proc(nag['konw'][1])} w ostatnich 12 miesiącach "
            f"({liczba(nag['sesje'][1])} sesji, {liczba(nag['platnosci'][1])} płatności).",
            f"Podział zmiany konwersji osób, które jeszcze nie kupowały, według kampanii (opisowo, czyli bez mierzenia "
            f"wpływu): zmiana struktury ruchu {zn(E['lj_nk_rozklad_kampania_struktura'], 2)} punktu, zmiana w obrębie kampanii "
            f"{zn(E['lj_nk_rozklad_kampania_wewnatrz'], 2)} punktu. Nowe kampanie nie mają roku wcześniej, więc liczą się w "
            f"całości do struktury.",
            # całe 12 miesięcy i wszystkie sesje: to nie przeczy awarii Safari, która dotyczy IV–IX 2026 (trzecia lista Kuby)
            "Wszystkie sesje razem, w całych ostatnich 12 miesiącach: " + wszystkie]), tab_m, tab_saf],
        linki=[link("Lejek: osoby, które jeszcze nie kupowały, według kampanii",
                    "#lejek?typ=zwykla&pac=nie_kupowal&podz=kampania&krok=k5&wygl=28")],
        zrodlo="analiza/a5p_lejek.py → analiza/wyniki/a5p_lejek_dzienny.csv.gz; analiza/e_merytoryka.py → "
               "analiza/wyniki/e_merytoryka.txt (punkt 4); analiza/e_poprawki.py → analiza/wyniki/e_poprawki.txt (punkty 1 "
               "i 3).")
    s = nag["safari"]
    nap0, nap1 = nag["naprawy"]
    sk = V["safari_krok"]   # od 1.10.2025 do dnia przed awarią, od awarii do końca danych, sesje z wyborem terminu po
    d_saf = B2.dt.date.fromisoformat(s["data"])
    dzien = f"{d_saf.day} {B2.MIESIACE_DOP[d_saf.month - 1]} {d_saf.year}"
    na30 = B2.dziesiatki((s["na30_od"] + s["na30_do"]) / 2)
    so = V["safari_okresy"]   # od, do przed awarią; od, do po awarii (do końca danych); dni
    dd = lambda x: B2.data(B2.dt.date.fromisoformat(x))  # noqa: E731
    assert s["po_proc"] < s["przed_proc"] - 15 and abs(s["po_proc"] - s["po60_proc"]) < 2, \
        "„do końca danych nie wraca”: poziom do 30.09.2026 jak w 60 dniach po awarii (runda F, poprawka 5)"
    safari = karta(
        f"Od {dzien} nowi pacjenci w Safari na iPhone'ach rzadziej kończą zakładanie konta",
        znacznik=znacznik("Do naprawy", "zle"),
        wniosek=f"W 60 dniach po awarii krok konta po wyborze terminu przechodzi {z0(s['po60_proc'])}% sesji wobec "
                f"{z0(s['przed_proc'])}% w 60 dniach przed nią i do końca danych nie wraca, a w innych przeglądarkach "
                f"prawie się nie zmienił.",
        tresc=[punkty([f"Konta dalej powstają, ale rzadziej. To około {liczba(na30)} utraconych pierwszych zamówień "
                       f"miesięcznie.",
                       # trzecia lista Kuby, punkt 1 (warunek „prawie cały” sprawdza assert przy karcie nagłówka)
                       "Od kwietnia 2026 to prawie cały spadek konwersji nowych osób spoza nowych kampanii na L4."])],
        szczegoly=[akapit(
            f"Krok konta po wyborze terminu u osób, które jeszcze nie kupowały: {proc(sk[0])} od {so[0]} do {so[1]} i "
            f"{proc(sk[1])} od {so[2]} do {so[3]} ({liczba(sk[2])} sesji z wyborem terminu). W 60 dniach przed awarią i po "
            f"niej: {proc(s['przed_proc'])} ({dd(s['przed_od'])}–{dd(s['przed_do'])}, "
            f"{odm(s['przed_k2'], 'sesja', 'sesje', 'sesji')}) i {proc(s['po60_proc'])} ({dd(s['po60_od'])}–"
            f"{dd(s['po60_do'])}, {odm(s['po60_k2'], 'sesja', 'sesje', 'sesji')}); pozostałe "
            f"przeglądarki w tych samych dniach {proc(s['reszta_przed_proc'])} i "
            f"{proc(s['reszta_po60_proc'])}. Szacunek: {liczba(s['utracone_od'])}–{liczba(s['utracone_do'])} utraconych "
            f"pierwszych zamówień do {B2.data(B2.O2[1])}, czyli {liczba(s['na30_od'])}–{liczba(s['na30_do'])} na 30 dni.")],
        linki=[link("Pokaż w lejku", nap0["link"])], zrodlo="analiza/a5p_zdarzenia.py → analiza/wyniki/a5p_zdarzenia.txt; "
                                                           "analiza/wyniki/c_priorytety.txt (P1); "
                                                           "analiza/wyniki/e_poprawki.txt (punkt 3).")
    P = {r["wartosc"] + str(r["okres"]): r for r in E["nk_przegl_kroki_wartosc"]}
    apl = [P[k] for k in P if k[:-1] in ("Instagram", "Facebook", "TikTok")]
    zw_ = [P[k] for k in P if k[:-1] in ("Chrome", "Safari")]
    rz = lambda L, kol, m=1: zakres(min(r[kol] for r in L), max(r[kol] for r in L), m)  # noqa: E731
    stary = popraw(nap1["tekst"])
    stary = stary[:stary.index("Dla porównania")] if "Dla porównania" in stary else stary
    obs = " Porównanie jest obserwacyjne: nie rozdziela wpływu przeglądarki od cech użytkowników"
    assert obs in stary and "W ruchu osób, które znają już stronę, jest inaczej:" in stary
    stary = stary[:stary.index(obs)].rstrip()
    stary = stary.replace("W ruchu osób, które znają już stronę, jest inaczej:",
                          "W ruchu osób, które już znają stronę albo markę (remarketing Meta, Google Ads na markę i wejścia "
                          "bezpośrednie), jest inaczej:")
    wb = V["wbud"]
    rozn = [-wb[k][6] for k in ("rmkt2", "brand2", "bezp2")]
    przegl = karta(
        "Przeglądarki w aplikacjach płacą rzadziej niż zwykłe w remarketingu, kampanii na markę i wejściach bezpośrednich",
        znacznik=znacznik("Do sprawdzenia", "uwaga"),
        wniosek=f"W tych kampaniach różnica wynosi {z0(min(rozn))}–{z0(max(rozn))} punktów procentowych, a w reklamach Meta "
                f"i TikTok na L4, które trafiają do nowych osób, jej nie ma.",
        tresc=[punkty(["Niska konwersja kampanii na L4 nie wynika więc wyraźnie z przeglądarki. Przyczynę różnicy w "
                       "pozostałym ruchu trzeba sprawdzić, zanim zaplanujemy naprawę (Czego nie wiemy, punkt "
                       f"{NIEWIADOMA[19]})."])],
        zastrzezenie="To porównanie obserwacyjne: nie rozdziela wpływu przeglądarki od tego, kto z niej korzysta.",
        szczegoly=[akapit(stary.strip()), akapit(
            f"Dla porównania cały ruch osób, które jeszcze nie kupowały (wszystkie kampanie razem): przeglądarki w aplikacjach "
            f"płacą w obu latach w {rz(apl, 'platnosc_z_sesji')}% sesji, a Chrome i Safari w {rz(zw_, 'platnosc_z_sesji')}%. "
            f"Usługę wybiera {rz(apl, 'usluga')}% sesji w przeglądarkach w aplikacjach (Chrome i Safari "
            f"{rz(zw_, 'usluga')}%), termin {rz(apl, 'termin_z_uslugi')}% tych, które wybrały usługę (wobec "
            f"{rz(zw_, 'termin_z_uslugi')}%), a krok konta {rz(apl, 'konto_z_terminu')}% tych, które wybrały termin (wobec "
            f"{rz(zw_, 'konto_z_terminu')}%; najniżej Safari po awarii).")],
        linki=[link("Pokaż w lejku", nap1["link"])], zrodlo="analiza/d_kampanie.py → analiza/wyniki/d_kampanie.txt (punkt 1); "
                                                           "analiza/wyniki/e_merytoryka.txt (punkt 5c).")
    Dd = V["D"]
    bez_zak = Dd["konta_bez_zakupu_proc_kont"]
    assert 20 < bez_zak < 25, "„ponad co piąte konto” wymaga od 20% do 25% kont bez zakupu"
    osobne = karta("Sesje zalogowane od wejścia nie kończą się płatnością, a ponad co piąte konto nie ma żadnego zakupu",
                   tresc=[akapit(popraw(z)) for z in nag["osobne"]])
    nag["karta"] = nazwy(karta_n)
    # liczby do wykresu karty przeglądarek (etap 5 grafiki): ta sama kampania, ostatnie 12 miesięcy (d_kampanie.json,
    # punkt 1, zbiorczo, wariant V1). „zwykla_w_tych_samych_warunkach” to odsetek, jaki miałyby te same sesje przy
    # konwersji zwykłych przeglądarek w tej samej kampanii i grupie osób (ważony sesjami w aplikacjach, założenie 63).
    with open(os.path.join(WYNIKI, "d_kampanie.json"), encoding="utf-8") as f:
        DK = json.load(f)
    kamp = [("meta_remarketing", "Remarketing Meta", "znaja_strone"), ("gs_brand", "Google Ads na markę", "znaja_strone"),
            ("bezposrednie", "Wejścia bezpośrednie", "znaja_strone"), ("meta_l4", "Kampania Meta na L4", "nowe_osoby"),
            ("tiktok_l4", "Kampania TikTok na L4", "nowe_osoby")]
    wiersze_w = []
    for klucz, opis, rodzaj in kamp:
        k_ = f"p1_zbiorczo_v1_{klucz}_okres_2"
        wiersze_w.append({"kampania": opis, "rodzaj": rodzaj,
                          "w_aplikacji": {"proc": DK[k_ + "_sesja_do_platnosci_wbudowane_proc"],
                                          "sesje": int(DK[k_ + "_sesje_wbudowane"])},
                          "zwykla_w_tych_samych_warunkach": {"proc": DK[k_ + "_sesja_do_platnosci_oczekiwana_proc"]},
                          "roznica_pkt": DK[k_ + "_roznica_pkt"], "od_pkt": DK[k_ + "_roznica_od_pkt"],
                          "do_pkt": DK[k_ + "_roznica_do_pkt"]})
    przegl["wykres"] = {"okres": "ostatnie 12 miesięcy", "wiersze": wiersze_w}
    nag["naprawy_karty"] = [nazwy(safari), nazwy(przegl)]
    nag["osobne_karta"] = nazwy(osobne)
    return kontrola([("lejek/naglowek", nag["karta"], ["d:Rozkład zmiany"], dod_tab),
                     ("lejek/safari", nag["naprawy_karty"][0], [], []),
                     ("lejek/przegladarki", nag["naprawy_karty"][1], ["d:Przeglądarki wbudowane"], []),
                     ("lejek/osobne", nag["osobne_karta"], ["d:Konta bez zakupu"], [])])
