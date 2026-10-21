"""B2 — eksport wyniku punktu C na stronę narzędzia: „czy to wzrost”, priorytety, czego nie wiemy.

Zasada Kuby dla strony: żadnych liczb wpisanych ręcznie w tekstach. Ten skrypt nie liczy niczego od nowa na bazie.
Każdą liczbę odczytuje z raportów w analiza/wyniki (głównie c_priorytety.txt i c_telemedigo.txt, a tam, gdzie szkic
powołuje się na część A5, z jej raportów) i wstawia do zdań. Teksty idą za notatką notatki/c_szkic.md (sekcje 1, 3
i 4), przyjętą przez Kubę 2026-10-20, przepisaną dla czytelnika z Telemedi (bez odnośników do notatek w zdaniach;
odnośniki są w polu „skąd liczby”).

Kontrola zgodności:
  1. liczby odczytane z dwóch miejsc (np. c_priorytety.txt i a5e_scenariusze.txt) muszą się zgadzać;
  2. każda liczba w każdym zdaniu musi stać w odpowiadającym mu fragmencie c_szkic.md (ta sama pozycja listy, ta sama
     niewiadoma, ta sama sekcja). Wyjątek: liczebności i okresy dopisane przy odsetkach (zasada Kuby) oraz kwoty
     w dniach działania kampanii; każda z nich jest odczytana z raportu i wypisana w raporcie kontroli jako „dodana”;
  3. uruchomiony z analiza/b_eksport.py porównuje też liczby z tym, co eksport liczy sam na bazie (nowi pacjenci,
     powroty, mostek dashboardu, marża po kwartałach).

Uruchomienie z głównego folderu (bez bazy, około sekundy):
    python -I analiza/b2_eksport_c.py
Wynik: narzedzie/dane_strony/c.js i raport analiza/wyniki/b_eksport_c.txt. Ten sam eksport uruchamia
analiza/b_eksport.py i dopisuje kontrole do swojego raportu.
"""
import datetime as dt
import json
import os
import re
import sys

import pandas as pd

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WYNIKI = os.path.join(KATALOG, "analiza", "wyniki")
DANE = os.path.join(KATALOG, "narzedzie", "dane_strony")
SZKIC = os.path.join(KATALOG, "notatki", "c_szkic.md")
D_TEKSTY = os.path.join(os.path.dirname(SZKIC), "d_teksty_strony.md")
RAPORT = os.path.join(WYNIKI, "b_eksport_c.txt")

CP, CT = "c_priorytety.txt", "c_telemedigo.txt"
NOWE = ("meta_prosp_l4_szybko", "tt_prosp_l4_15min")
MIESIACE_RZ = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
MIESIACE_MSC = ["styczniu", "lutym", "marcu", "kwietniu", "maju", "czerwcu", "lipcu", "sierpniu", "wrześniu",
                "październiku", "listopadzie", "grudniu"]
MIESIACE_DOP = ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca", "sierpnia", "września",
                "października", "listopada", "grudnia"]

# Czas wdrożenia i parametry planu testów to nasz szacunek z c_szkic.md, a nie liczby z danych.
SZACUNEK = {
    1: "dni", 2: "1 dzień sprawdzenie, 1–2 tygodnie raport", 3: "1 dzień", 4: "1 dzień",
    5: "1–2 tygodnie + 4–6 tygodni pomiaru", 6: "diagnoza 1–2 dni, test 2–4 tygodnie",
    7: "dane o wysyłkach dni, sekwencja 2–4 tygodnie, pomiar 90 dni", 8: "1 dzień", 9: "1 tydzień + 4–6 tygodni",
    10: "1–2 tygodnie + test dwóch cen 4 tygodnie", 11: "1–2 dni", 12: "2–8 tygodni + 90 dni",
}
KOSZT_INTERNISTY = 25   # zasada z zadania: koszt lekarza za odbytą wizytę u internisty (zł)
ZNIZKA_SPEC = 20        # zasada z zadania: zniżka TelemediGO u specjalistów (%)
OPLATA_GO = 89          # zasada z zadania: opłata za TelemediGO (zł)


# ---------------------------------------------------------------- formatowanie (jak w b_eksport.py)

def liczba(x, m=0):
    s = f"{x:,.{m}f}".replace(",", "\xa0").replace(".", ",")
    s = s.replace("-", "−")
    return "0" if re.fullmatch(r"−0(,0*)?", s) else s


def proc(x, m=1):
    return liczba(x, m) + "%"


def zn(x, m=1):
    """Liczba ze znakiem: +3,0 albo −23,2."""
    return ("+" if round(x, m) > 0 else "") + liczba(x, m)


def zl(x):
    return liczba(x) + " zł"


def t1(x, m=1):
    """Kwota w tysiącach złotych bez jednostki: 11 928 → '11,9', −30 801 → '−30,8'."""
    return liczba(x / 1000, m)


def tz(x, m=1):
    return t1(x, m) + " tys. zł"


def tzn(x, m=1):
    return zn(x / 1000, m) + " tys. zł"


FORMY = {"wizyta": ("wizyta", "wizyty", "wizyt"), "pacjent": ("pacjent", "pacjentów", "pacjentów")}


def ile(n, rzecz):
    """Liczba z rzeczownikiem w poprawnej formie: 1 wizyta, 572 wizyty, 9 979 wizyt."""
    f1, f2, f5 = FORMY[rzecz]
    n = int(n)
    forma = f1 if n == 1 else f2 if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14) else f5
    return f"{liczba(n)} {forma}"


def zakres(a, b, m=0, jedn=""):
    return f"{liczba(a, m)}–{liczba(b, m)}{jedn}"


def data(d):
    return f"{d.day}.{d:%m.%Y}"


def kw_nazwa(q):
    """'2026-Q3' → 'III kwartale 2026'."""
    r, k = q.split("-Q")
    return f"{MIESIACE_RZ[int(k) - 1]} kwartale {r}"


def kw_krotko(q):
    r, k = q.split("-Q")
    return f"{MIESIACE_RZ[int(k) - 1]} {r}"


def dziesiatki(x):
    return int(round(x / 10.0) * 10)


# ---------------------------------------------------------------- odczyt raportów

NUM = r"((?<![\d.,])[−+-]?(?:\d{1,3}(?:[ \xa0]\d{3})+|\d+)(?:[.,]\d+)?(?![\d]))"


def num(s):
    s = s.strip().replace("\xa0", "").replace(" ", "").replace("−", "-").replace(",", ".")
    return float(s)


class Zrodla:
    """Odczyt liczb z raportów w analiza/wyniki. Każdy odczyt trafia do listy (raport kontroli)."""

    def __init__(self):
        self._t = {}
        self.odczyty = []

    def tekst(self, plik, od=None, do=None):
        if plik not in self._t:
            with open(os.path.join(WYNIKI, plik), encoding="utf-8") as f:
                self._t[plik] = f.read()
        t = self._t[plik]
        if od is not None:
            i = t.find(od)
            if i < 0:
                raise ValueError(f"{plik}: brak znacznika {od!r}")
            t = t[i:]
        if do is not None:
            j = t.find(do, 1)
            if j > 0:
                t = t[:j]
        return t

    def r(self, plik, wzorzec, od=None, do=None):
        """Wzorzec to wyrażenie regularne, w którym {N} oznacza liczbę. Zwraca liczbę albo krotkę liczb."""
        t = self.tekst(plik, od, do)
        m = re.search(wzorzec.replace("{N}", NUM), t, re.M)
        if not m:
            raise ValueError(f"{plik}: brak wzorca {wzorzec!r} (od {od!r})")
        v = tuple(num(g) for g in m.groups())
        self.odczyty.append((plik, od or "", v))
        return v[0] if len(v) == 1 else v

    def s(self, plik, wzorzec, od=None, do=None):
        """Jak r(), ale zwraca tekst grup (daty, okresy)."""
        t = self.tekst(plik, od, do)
        m = re.search(wzorzec, t, re.M)
        if not m:
            raise ValueError(f"{plik}: brak wzorca {wzorzec!r}")
        return m.groups() if len(m.groups()) > 1 else m.group(1)

    def tabela(self, plik, kolumny, od=None, do=None):
        """Tabela z wydruku pandas: pierwszy wiersz, którego początek to `kolumny`, i wiersze o tej samej długości."""
        linie = self.tekst(plik, od, do).splitlines()
        for i, l in enumerate(linie):
            if l.split()[:len(kolumny)] == kolumny:
                nag = l.split()
                wiersze = []
                for w in linie[i + 1:]:
                    p = w.split()
                    if len(p) != len(nag):
                        break
                    wiersze.append(p)
                df = pd.DataFrame(wiersze, columns=nag)
                for k in df.columns:
                    try:
                        df[k] = df[k].map(num)
                    except ValueError:
                        pass
                self.odczyty.append((plik, od or " ".join(kolumny), f"tabela {len(df)} wierszy"))
                return df
        raise ValueError(f"{plik}: brak tabeli {kolumny} (od {od!r})")


RX_ROZKLAD_Z1K = r"^\s+kampania\s+12\s+12867\s+18924\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}"
RX_ROZKLAD_Z2 = r"\(Z2\)\s+kampania\s+12867\s+18924\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}"


def udzial_nowych_w_spadku(Z=None):
    """Udział nowych kampanii w spadku powrotu w 90 dniach (%): przyjęta reguła i sesja płatności (a5r_struktura.txt)."""
    Z = Z or Zrodla()
    r1, r2 = Z.r("a5r_struktura.txt", RX_ROZKLAD_Z1K), Z.r("a5r_struktura.txt", RX_ROZKLAD_Z2)
    return 100 * r1[5] / r1[4], 100 * r2[3] / r2[2]


def wczytaj_js(nazwa, klucz):
    """Odczyt pliku danych strony (window.D...) zapisanego przez b_eksport.py."""
    with open(os.path.join(DANE, nazwa), encoding="utf-8") as f:
        linia = f.read().splitlines()[1]
    return json.loads(linia[len(f"D{klucz}="):].rstrip(";"))


# ---------------------------------------------------------------- wartości

def wartosci(Z):
    V = {}
    # W1: nowi pacjenci
    w1 = Z.tabela(CP, ["okres", "nowi", "bez_nowych_z1k"], od="W1.").set_index("okres")
    V["nowi"] = {o: int(w1.loc[o, "nowi"]) for o in (1, 2)}
    V["bez_z1k"] = int(w1.loc[2, "bez_nowych_z1k"])
    V["bez_z2"] = int(w1.loc[2, "bez_nowych_z2"])
    V["bezpl"] = {o: int(w1.loc[o, "bezplatne_z1k"]) for o in (1, 2)}
    V["w1_zm"] = Z.r(CP, r"zmiana %: nowi: {N}%, bez_nowych_z1k: {N}%, bez_nowych_z2: {N}%, bezplatne_z1k: {N}%")
    # W2: powroty i marża na pacjenta, te same dni kalendarzowe
    for klucz, etyk in (("wszyscy", "wszyscy:"), ("bez_z1k", "bez nowych kampanii (Z1K):"),
                        ("bez_z2", "bez nowych kampanii (Z2):"), ("nowe_z1k", "tylko nowe kampanie (Z1K):")):
        t = Z.tabela(CP, ["p30_o1", "p30_o2"], od=etyk).iloc[0]
        V[f"pow_{klucz}"] = {k: float(t[k]) for k in t.index}
    V["powracajacy"] = Z.r(CP, r"Liczba pacjentów, którzy wrócili w 90 dniach \(kohorty do (\d{4})-(\d\d)-(\d\d) i do \d{4}-\d\d-\d\d.*?\): "
                                r"{N} wobec {N} \({N}%\)", od="W2.")
    us = Z.tabela(CP, ["usluga", "p90_o1", "p90_o2"], od="W2.").set_index("usluga")
    V["uslugi_bez"] = us
    m = Z.tabela(CP, ["okres", "pacjenci", "marza_wszyscy"], od="W2.").set_index("okres")
    V["m90"] = {o: float(m.loc[o, "marza_wszyscy"]) for o in (1, 2)}
    V["m90_bez_z1k"] = float(m.loc[2, "marza_bez_nowych_z1k"])
    V["m90_bez_z2"] = float(m.loc[2, "marza_bez_nowych_z2"])
    # 180 dni: raport kohort części retencji
    V["p180"] = Z.r("a5r_kohorty.txt", r"^\s+180\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}",
                    od="okno_dni  n_o1  n_o2  powrot_o1")  # n1, n2, p1, p2, zmiana, marża1, marża2
    V["p90_kohorty"] = Z.r("a5r_kohorty.txt", r"^\s+90\s+{N}\s+{N}\s+{N}\s+{N}", od="okno_dni  n_o1  n_o2  powrot_o1")
    # L4 z L4 w pozostałych kanałach (a5r_struktura.txt, 3d)
    l4 = Z.tabela("a5r_struktura.txt", ["grupa", "n_o1", "n_o2"], od="3d.").set_index("grupa").loc["4_pozostale_kanaly"]
    V["l4_pozostale"] = (int(l4["n_o1"]), int(l4["n_o2"]), float(l4["o1"]), float(l4["o2"]))
    # rozkład spadku na nowe i stare kampanie, obie reguły
    V["rozklad_z1k"] = Z.r("a5r_struktura.txt", RX_ROZKLAD_Z1K)
    V["rozklad_z2"] = Z.r("a5r_struktura.txt", RX_ROZKLAD_Z2)
    # W3: wynik biznesu w okresach
    w3 = Z.tabela(CP, ["pozycja", "okres_1", "okres_2"], od="W3.").set_index("pozycja")
    V["w3"] = w3
    V["w3_bez"] = Z.r(CP, r"okres 2 {N} zł \({N}% wobec okresu 1; bez odjęcia {N}%\)", od="W3.")
    V["w3_bez_go"] = Z.r(CP, r"\({N} zł\): {N} zł \({N}%\)", od="W3.")
    # W4: marża po kwartałach
    kw = Z.tabela(CP, ["kwartal", "zamowienia", "przychod"], od="W4.").set_index("kwartal")
    rr = Z.tabela(CP, ["kwartal", "marza", "marza_rok_wczesniej"], od="W4.").set_index("kwartal")
    mm = Z.tabela(CP, ["miesiac", "przed_kampaniami", "wydatki"], od="W4.").set_index("miesiac")
    V["kw"], V["rr"], V["mm"] = kw, rr, mm
    V["kw_rozbicie"] = Z.r(CP, r"Rozbicie zmiany marży III kwartału \({N} zł\): marża przed kampaniami {N} zł, "
                                r"wydatki na kampanie {N} zł", od="W4.")
    V["go_start"] = Z.r(CT, r"Pierwsze {N} dni kampanii: {N} zakupów")   # dni, zakupy
    # P1: Safari na iOS
    p1 = Z.tabela(CP, ["n90", "marza90", "n180", "marza180"], od="P1.").iloc[0]
    V["p1_marza"] = p1
    for k, etyk in (("lo", "po odjęciu tła"), ("hi", "bez odjęcia tła")):
        V[f"p1_{k}"] = Z.r(CP, etyk + r": {N} pierwszych zamówień w {N} dniach, czyli {N} rocznie; marża w 90 dniach "
                                      r"{N} zł, w 180 dniach {N} zł rocznie", od="P1.")
        V[f"p1_q3_{k}"] = Z.r(CP, r"\(92 dni\), " + etyk + r": {N} utraconych pierwszych zamówień; marża z dnia "
                                  r"pierwszego zamówienia {N} zł, a z pierwszego zamówienia i dalszych zamówień w ciągu "
                                  r"kwartału najwyżej {N} zł \(spadek marży III kwartału rok do roku: {N} zł", od="P1.")
    V["safari_okresy"] = Z.s("a5p_zdarzenia.txt", r"Przed = (\d+\.\d+\.\d{4})–(\d+\.\d+\.\d{4}), po = (\d+\.\d+)–(\d+\.\d+\.\d{4}) \((\d+) dni\)", od="5f.")
    V["safari_krok"] = Z.r("a5p_zdarzenia.txt", r"^\s+nowi\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}", od="5f.")
    V["safari_konta"] = Z.r("a5p_zdarzenia.txt", r"^\s+True\s+{N}\s+{N}", od="5d.")
    # P1b: pomiar
    V["dash_surowo"] = Z.r("a3_dashboard.txt", r"wszystko surowo\s+{N}%\s+{N}%\s+{N}%\s+{N}%")   # nowi, zam., przychód, GO
    V["dash_zam"] = Z.r(CP, r"zamówienia {N}% \({N} → {N}\), przychód z konsultacji {N}% \({N} → {N} mln zł\)", od="P1b.")
    V["czyste_zam"] = Z.r(CP, r"zamówienia {N}% \({N} → {N}\); przychód po zwrotach {N}%", od="P1b.")
    V["dup"] = Z.r(CP, r"Duplikaty: {N} zamówienia z", od="P1b.")
    V["dup_daty"] = Z.s(CP, r"Duplikaty: \d+ zamówienia z (\d+–\d+\.\d+\.\d{4})", od="P1b.")
    t = Z.tabela(CP, ["okres", "zamowienia_testowe", "wizyty_odbyte"], od="P1b.").set_index("okres")
    V["testy"] = {o: int(t.loc[o, "zamowienia_testowe"]) for o in (1, 2)}
    V["testy_koszt2"] = float(t.loc[2, "koszt_lekarza_wg_zasady_zl"])
    t = Z.tabela(CP, ["zamowienia_testowe", "u_internisty", "trwajace_1_minute"], od="P13.").iloc[0]
    V["testy_razem"] = (int(t["zamowienia_testowe"]), int(t["u_internisty"]), int(t["trwajace_1_minute"]))
    V["testy_konta"] = Z.r("a2_jakosc.txt", r"Kod TEST-QA: .*?, {N} konta")
    V["testy_koszt_2lata"] = Z.r("a2_jakosc.txt", r"^\s+2071\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s*$", od="2e.")[-1]
    V["p15"] = Z.r(CP, r"Wykrycie po 7 dniach ograniczyłoby stratę do {N}% tej liczby, czyli do {N}–{N} zamówień")
    # P2, P11: zwroty L4 i kwoty na pełny rok
    V["p2"] = Z.r(CP, r"90 dni: przyjęta reguła od {N} zł \(wariant B\) do {N} zł \(wariant A\); sesja płatności od "
                      r"{N} zł do {N} zł rocznie")
    dk = Z.tabela(CP, ["kampania", "dni_z_wydatkami"], od="P11.").set_index("kampania")
    V["dni"] = {k: int(dk.loc[k, "dni_z_wydatkami"]) for k in NOWE}
    V["mn"] = {k: 365 / V["dni"][k] for k in NOWE}
    V["mn_raport"] = {k: float(dk.loc[k, "mnoznik_na_rok"]) for k in NOWE}
    V["start"] = {k: dt.date.fromisoformat(dk.loc[k, "od"]) for k in NOWE}
    V["p11_tt"] = Z.r(CP, r"dziś {N} zł \(przyjęta reguła\) i {N} zł \(sesja płatności\) w 90 dniach; wyłączenie przy "
                          r"100% dodatkowych \+{N} zł do \+{N} zł, przy 0% \+{N} zł", od="P11.")
    V["p11_meta"] = Z.r(CP, r"dziś {N} zł i {N} zł; rozpiętość decyzji od {N} zł do \+{N} zł", od="P11.")
    V["p11_180"] = Z.r(CP, r"Horyzont 180 dni na pełny rok .*?wyłączenie przy 100% dodatkowych \+{N} zł do \+{N} zł; Meta — dziś "
                           r"{N} zł i {N} zł, rozpiętość decyzji od {N} zł do \+{N} zł", od="P11.")
    V["p11_prog"] = Z.r(CP, r"Próg decyzji Meta .*?: {N}% w horyzoncie 90 dni i {N}% w horyzoncie 180 dni", od="P11.")
    V["p11_test"] = Z.r(CP, r"gdy wszyscy pacjenci są dodatkowi: {N} zł w dniach działania, {N} zł na pełny rok", od="P11.")
    V["p11_zwroty"] = Z.r(CP, r"wariant B–A {N}–{N} zł \(przyjęta\s+reguła\) i {N}–{N} zł \(sesja płatności\) w dniach "
                              r"działania; na pełny rok ×{N}: {N} zł–{N} zł i {N} zł–{N} zł", od="P11.")
    V["p3_cp"] = Z.r(CP, r"Dziś \(90 dni\): {N} zł \(Z1K\), {N} zł \(Z2\)\. 180 dni: {N} zł i {N} zł\.", od="P3.")
    V["p3_cp_napr"] = Z.r(CP, r"wariant A\) {N} zł \(Z1K\) i {N} zł \(Z2\) w 90 dniach; {N} i {N} zł w 180 dniach", od="P3.")
    V["p4_cp"] = Z.r(CP, r"Dziś \(90 dni\): {N} zł \(Z1K\), {N} zł \(Z2\); 180 dni: {N} zł i {N} zł\.", od="P4.")
    # macierz kampanii: a5e_scenariusze.txt, E1, E3 i E3b
    e1 = Z.tabela("a5e_scenariusze.txt", ["kampania", "regula", "dodatkowi_proc"], od="E1.")
    e3 = Z.tabela("a5e_scenariusze.txt", ["kampania", "regula", "obecny_wynik", "napraw_zwroty_A"], od="E3.")
    e3b = Z.tabela("a5e_scenariusze.txt", ["kampania", "regula", "obecny_wynik_90", "obecny_wynik_180"], od="E3b.")
    V["e1"], V["e3"], V["e3b"] = e1, e3, e3b
    V["nowe_7268"] = Z.r("a5e_scenariusze.txt", r"^\s+obie\s+Z1K\s+{N}", od="E0.")
    V["e2a"] = Z.r("a5e_scenariusze.txt", r"^\s+nowe kampanie\s+Z1K\s+{N}\s+{N}", od="E2a.")   # wizyty L4, zwroty
    V["zgoda_1900"] = Z.r("a5e_scenariusze.txt", r"^\s+nowe kampanie\s+Z1K\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}", od="E2b.")[-2]
    # ekonomia kampanii na pacjenta: a5e_kampanie.csv
    ek = pd.read_csv(os.path.join(WYNIKI, "a5e_kampanie.csv"))
    Z.odczyty.append(("a5e_kampanie.csv", "kampanie okres 2", f"{len(ek)} wierszy"))
    ek = ek[(ek["okres"] == 2) & (ek["poziom"] == "kampania")]
    V["ek"] = {(r["kampania"], r["regula"], str(r["okno_dni"])): r for _, r in ek.iterrows()}
    V["nowe_marza"] = Z.r("a5e_ekonomia.txt", r"^\s+1_nowe_kampanie_L4\s+Z1K\s+2\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}", od="1a.")
    # P5: zalogowani
    V["p5"] = (Z.r(CP, r"× {N} zł marży zamówienia powtórnego = {N} zł rocznie", od="P5.")[1],
               Z.r(CP, r"pacjenci zamiast sesji.*?: {N} zł rocznie", od="P5."),
               Z.r(CP, r"wysoki scenariusz × .*?: {N} zł rocznie", od="P5."))
    V["zal_sesje"] = Z.r("a5p_zalogowane.txt", r"^\s+{N}\s+{N}\s+{N}\s+{N}\s*$", od="sesje  pacjenci  pacjenci_z_co_najmniej_2")[0]
    V["zal_powt"] = Z.r("a5p_zalogowane.txt", r"2: zamowienie powtorne\s+{N}")
    # P6: TelemediGO u specjalistów
    t = Z.tabela(CP, ["okres", "zamowienia", "marza", "znizka_efektywna"], od="P6.").set_index("okres")
    V["p6"] = t
    V["p6_scen"] = (Z.r(CP, r"znikają wszystkie te zamówienia: {N} zł", od="P6."),
                    Z.r(CP, r"znikają tylko zamówienia, które dziś przynoszą stratę: {N} zł", od="P6."),
                    Z.r(CP, r"wszystkie zostają po cenie katalogowej: {N} zł", od="P6."))
    # P7: gs_generic_specjalisci
    V["p7"] = {}
    for reg in ("Z1K", "Z2"):
        for okno in ("90", "180"):
            V["p7"][(reg, okno)] = Z.r(CP, reg + ", " + okno + r" dni: nowi rocznie {N}, wydatki {N} zł, koszt pozyskania "
                                       r"{N} zł, marża na pacjenta {N} zł, wynik {N} zł; wyłączyć przy 100% / 50% / 0% "
                                       r"dodatkowych: {N} zł / {N} zł / {N} zł", od="P7.")
    # P8, P9, P10, P12, P13, P14
    V["p8"] = Z.r(CP, r"Brak efektu 0 zł; wąski {N}–{N} zł; szeroki {N}–{N} zł", od="P8.")
    V["p9"] = Z.r(CP, r"Górna granica okresu 2: {N} sesji, do {N} zamówień, {N} zł wydatków", od="P9.")
    V["p9_zl"] = Z.r(CP, r"= {N} zł rocznie", od="P9.")
    V["p10"] = [Z.r(CP, r"^\s+" + str(n) + r" pacjentów w grupie próbnej .*?około {N} zł dodatkowego kosztu", od="P10.")
                for n in (487, 1823)]
    V["p10_n"] = Z.r(CT, r"\(B\) połowa: .*?potrzeba {N} pacjentów"), Z.r(CT, r"\(B\) jedna czwarta: .*?potrzeba {N} pacjentów")
    V["p12"] = Z.r(CP, r"× 1 punkt procentowy powrotu w 90 dniach × {N} zł = {N} zł", od="P12.")
    V["p12_bez"] = Z.r(CP, r"Bez pacjentów nowych kampanii \({N} według przyjętej reguły\): {N} zł", od="P12.")
    V["dlugosc"] = Z.tabela(CP, ["okres", "dlugosc_porannej_wizyty_internisty_min"], od="P13.").set_index("okres")
    ce = Z.tabela(CP, ["specialization", "cena", "koszt_lekarza"], od="P14.").set_index("specialization")
    V["cennik_p14"] = ce
    V["p14"] = Z.r(CP, r"Razem okres 2: {N} zamówień u tych specjalistów, {N} z zapłatą", od="P14.")
    V["p14_go"] = Z.r(CP, r"Przy obecnej zniżce TelemediGO 20% na {N} z tych wizyt podwyżka ceny katalogowej o 10 zł daje {N} zł", od="P14.")
    V["p16"] = Z.r(CP, r"pacjenci okresu 2 z pełnymi 270 dniami obserwacji: {N}", od="P16.")
    V["p6_reakcja"] = Z.r(CP, r"przy osobnej reakcji przy każdym zamówieniu: od {N} do {N} zł", od="P6.")
    V["p7_dokladnie"] = {(r, o): Z.r(CP, r"bez zaokrąglania marży \(uwaga Astry\): " + r + ", " + o + r" dni: marża {N} zł, wynik {N} zł", od="P7.")
                         for r in ("Z1K", "Z2") for o in ("90", "180")}
    V["p14_zl"] = Z.r(CP, r"każde 10 zł podwyżki ceny przy tej samej liczbie wizyt to {N} zł", od="P14.")
    # TelemediGO (c_telemedigo.txt)
    V["cennik"] = Z.tabela(CT, ["specialization", "cena", "liczba_cen", "cena_z_go"], od="3a.").set_index("specialization")
    V["go_bilans"] = Z.r(CT, r"oplata_minus_znizka_efektywna_na_czlonkostwo\s+{N}")
    V["go_typy"] = Z.tabela(CT, ["typ", "okres_1", "okres_2", "zmiana"], od="1a.").set_index("typ")
    V["go_start_data"] = Z.s(CT, r"start (\d+\.\d+\.\d{4})", od="1b.")
    V["go_osobno_mies"] = Z.r(CT, r"w okresie 2 średnio {N} miesięcznie", od="1b.")
    V["go_kasa"] = Z.tabela(CT, ["okres", "zamowienie", "zamowienia_do_oferty"], od="1e.")
    V["go_rozklad_1"] = Z.r(CT, r"1_pierwsze_zamowienie: zmiana \+{N} zakupów = więcej zamówień \+{N} \+ zmiana odsetka {N}", od="1e.")
    V["go_grupy"] = Z.tabela(CT, ["grupa", "n_okres_1", "n_okres_2", "odsetek_okres_1"], od="1f.").set_index("grupa")
    V["go_bez_nowych"] = Z.tabela(CT, ["okres", "n", "odsetek", "z_go"], od="bez pacjentów dwóch nowych kampanii").set_index("okres").loc[2]
    g2a = Z.tabela(CT, ["miara", "okres_1"], od="2a.").set_index("miara")["okres_1"]
    V["go_2a"] = g2a
    V["go_okres2"] = Z.r(CT, r"czyli {N} zł opłaty ponad zniżkę na członkostwo", od="2b.")
    odn = Z.tabela(CT, ["dni_po_wygasnieciu", "wygasle_czlonkostwa"], od="1d.").set_index("dni_po_wygasnieciu")
    V["odnowienia"] = (int(odn.loc[90, "wygasle_czlonkostwa"]), int(odn.loc[90, "odnowione"]), float(odn.loc[90, "odnowione_proc"]))
    V["go_kupujacy"] = Z.r(CT, r"odsetek kupujących przy pierwszym zamówieniu {N}%")
    V["go_miesiace_A"] = Z.r(CT, r"\(A\) cała różnica z 4a to wpływ ceny: .*?czyli {N} miesiąca pozyskania")
    V["go_miesiace_B"] = Z.r(CT, r"\(B\) jedna czwarta: .*?czyli {N} miesiąca pozyskania")
    V["go_4a"] = Z.r(CT, r"powrót w 90 dniach \(%\)\s+2\s+kanał\+usługa\+miesiąc\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}")
    # obsługa pacjenta: punktualność, zwroty, oceny, CRM
    V["rano"] = Z.tabela("a5r_punktualnosc.txt", ["miesiac", "int_rano", "int_rano_ponad15_wszyscy"], od="2b.").set_index("miesiac")
    V["ruch"] = Z.r("a5r_punktualnosc.txt", r"o {N} punktu procentowego więcej porannych wizyt spóźnionych ponad 15 minut "
                                            r"\({N} przedziałów, {N} wizyt\)")
    V["rano_powrot"] = Z.r("a5r_punktualnosc.txt", r"^\s+a_rano_6_11\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}", od="1c.")
    z2b = Z.tabela("a5r_po_zakupie.txt", ["visit_purpose", "okres", "grupa", "wizyty_odbyte"], od="2b.")
    V["zwroty_l4"] = z2b[(z2b["visit_purpose"] == "l4") & (z2b["okres"] == 2)].set_index("grupa")
    oc = Z.tabela("a5r_po_zakupie.txt", ["okres", "grupa", "koszyk", "n"], od="3a.")
    V["oceny"] = oc[(oc["okres"] == 2) & (oc["grupa"] == "pozostali")].set_index("koszyk")
    V["crm"] = Z.tabela("a5r_po_zakupie.txt", ["miesiac", "pacjenci", "reaktywacja"], od="5e.")
    V["crm_kontakt"] = Z.tabela("a5r_po_zakupie.txt", ["grupa2", "okres", "n", "zgoda"], od="5a.")
    V["crm_powrot"] = Z.r("a5r_po_zakupie.txt", r"po CRM: {N}% wobec {N}%.*?\n\s+bez CRM: {N}% wobec {N}%", od="5c.")
    # kliknięcia a sesje (a2_jakosc.txt, 3c)
    V["klik"] = Z.tabela("a2_jakosc.txt", ["kampania", "klikniecia", "sesje", "sesje_na_klik"], od="3c.").set_index("kampania")
    # sezon: od pierwszego miesiąca do miesiąca z największą liczbą nowych pacjentów w okresie 1 (a5p_sezon.txt, 1)
    se = Z.tabela("a5p_sezon.txt", ["m", "nowi", "nowi_platne"], od="1. NOWI PACJENCI")
    se = se[se["m"] < "2025-10"]
    rz = lambda m: f"{MIESIACE_RZ[int(m[5:]) - 1]} {m[:4]}"  # noqa: E731
    V["sezon"] = (rz(se["m"].iloc[0]), rz(se.loc[se["nowi"].idxmax(), "m"]))
    # liczby po konsylium (sesja prowadząca): analiza/wyniki/d_retencja.json, d_kampanie.json, d_wynik.json
    D = {}
    for n in ("d_retencja", "d_kampanie", "d_wynik"):
        with open(os.path.join(WYNIKI, n + ".json"), encoding="utf-8") as f:
            D.update(json.load(f))
        Z.odczyty.append((n + ".json", "klucz → wartość", f"{len(D)} kluczy razem"))
    V["D"] = D

    def wbud(grupa, okres):   # d_kampanie.txt 1e (V1): przeglądarka w aplikacji wobec zwykłej w tej samej kampanii
        return Z.r("d_kampanie.txt", re.escape(grupa) + r"\s+" + okres + r"\s+" + r"\s+".join(["{N}"] * 9), od="1e.")
    V["wbud"] = {"lekarz_oba": wbud("Meta lekarz online (meta_prosp_lekarz_online)", "oba"),
                 "rmkt2": wbud("remarketing Meta (meta_rmkt_koszyk)", "2"), "brand2": wbud("Google Ads marka (gs_brand)", "2"),
                 "bezp2": wbud("wejścia bezpośrednie", "2")}
    V["prog_pac"] = {w: Z.r("d_wynik.txt", r"^\s+Z1K\s+90\s+" + w + r"\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}")[-1]
                     for w in ("dziś", "po naprawie zwrotów A")}
    V["prog_pac_z2"] = Z.r("d_wynik.txt", r"^\s+Z2\s+90\s+dziś\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}")[-1]
    V["q3_go_osobno"] = Z.r("d_wynik.txt", r"TelemediGO kupione osobno \(crm_go_upsell\)\s+" + r"\s+".join(["{N}"] * 9))
    V["q3_powtorne"] = Z.r("d_wynik.txt", r"Z1K, powtórne zamówienia reszty: {N} → {N} zamówień, marża na zamówienie {N} → {N} zł")
    V["q3_baza_pac"] = {q: Z.r("d_wynik.txt", r"^\s+" + q + r"\s+" + r"\s+".join(["{N}"] * 10))[7] for q in ("2025-Q3", "2026-Q3")}
    V["test_wojewodztwa"] = Z.r("d_wynik.txt", r"na sumach {N} województw")
    V["tt_wczesne"] = Z.s("d_kampanie.txt", r"tt_prosp_l4_15min\s+Z1K\s+180 dni: wczesne kohorty (\d{4}-\d\d-\d\d) (\d{4}-\d\d-\d\d)")
    V["marka_okna"] = {o: Z.r("d_kampanie.txt", r"^\s+" + o + r"\s+" + r"\s+".join(["{N}"] * 14), od="5a.") for o in ("A_przed_caly", "D_po_spadku")}
    V["marka_na30"] = Z.r("d_kampanie.txt", r"wobec poziomu A: {N} \(na 30 dni {N}\); wobec poziomu B: {N} \(na 30 dni {N}\)", od="5b.")
    V["wbud"].update({"meta2": wbud("nowe: Meta na L4", "2"), "tt2": wbud("nowe: TikTok na L4", "2")})
    V["zwykle_nowe"] = {k: Z.r("d_kampanie.txt", r"^\s+" + kamp + r"\s+2\s+" + r"\s+".join(["{N}"] * 9), od="1b.")[3]
                        for k, kamp in (("meta", "meta_prosp_l4_szybko"), ("tt", "tt_prosp_l4_15min"))}
    V["rozklad_lejka"] = {g: Z.r("a5p_lejek.txt", r"^\s+" + g + r"\s+{N}\s+{N}\s+{N}\s+{N}\s+{N}", od="4. ZMIANA KONWERSJI")[3:5]
                          for g in ("przegladarka", "kampania", "strona_wejscia", "pacjent")}
    V["standaryzacja"] = {r: Z.r("d_retencja.txt", r"^\s+" + r + r"\s+wiek_x_plec\s+" + r"\s+".join(["{N}"] * 8), od="5e.")
                          for r in ("z1k", "z2")}
    V["pozostali_godz"] = {h: Z.r("d_retencja.txt", r"^\s+" + str(h) + r"\s+" + r"\s+".join(["{N}"] * 11),
                                  od="1.pozostali_lekarze — wszyscy: według godziny terminu") for h in range(24)}
    V["start10"] = Z.r("d_kampanie.txt", r"meta_prosp_l4_szybko\s+Z1K\s+START10\s+{N}\s+{N}", od="6b.")[1]
    V["marka_daty"] = {o: Z.s("d_kampanie.txt", re.escape(o) + r": (\d{4}-\d\d-\d\d) – (\d{4}-\d\d-\d\d)", od="5.")
                       for o in ("A_przed_caly", "B_po_awarii_safari", "D_po_spadku")}
    V["marka_rok_wczesniej"] = Z.r("d_kampanie.txt", r"D0_rok_wczesniej_22_05_30_09 − A0_rok_wczesniej_przed\s+{N}", od="5b.")
    # prowizja i pediatra
    V["prowizja"] = Z.r("a5e_ekonomia.txt", r"dwa lata: {N} zł \(przyjęta reguła\), {N} zł \(sesja płatności\), {N} zł \(kod RANKING10\)")
    ped = Z.tabela("a5r_kohorty.txt", ["okres", "n", "marza90_przyjeta"], od="7.").set_index("okres")
    V["pediatra"] = [float(ped.loc[o, "marza90_pediatra_25zl"] - ped.loc[o, "marza90_przyjeta"]) for o in (1, 2)]
    return V


def powroty_dokladne(koh):
    """Powrót w 30, 60, 90 i 180 dniach na tych samych dniach kalendarzowych, liczony z danych pacjent po pacjencie
    (narzedzie/dane_strony/kohorty.js), tak jak zakładka „Kohorty”: {okno: (p1, p2, n1, n2)}."""
    koniec, start, okres2 = dt.date(2026, 9, 30), dt.date(2024, 10, 1), dt.date(2025, 10, 1)
    out = {}
    for o in (30, 60, 90, 180):
        g2 = koniec - dt.timedelta(days=o)
        g1 = dt.date(g2.year - 1, g2.month, g2.day)
        i1, i2, i0 = (g1 - start).days, (g2 - start).days, (okres2 - start).days
        n = {1: 0, 2: 0}
        r = {1: 0, 2: 0}
        for d, x in zip(koh["d"], koh["r"]):
            k = 1 if d <= i1 else 2 if i0 <= d <= i2 else 0
            if k:
                n[k] += 1
                r[k] += 0 <= x <= o
        out[o] = (100 * r[1] / n[1], 100 * r[2] / n[2], n[1], n[2])
    return out


# ---------------------------------------------------------------- pomocnicze do tekstów

class Dodane:
    """Liczby dopisane poza szkicem (liczebność przy odsetku, kwoty w dniach działania); kontrola je wypisuje."""

    def __init__(self):
        self.lista = []

    def __call__(self, s):
        self.lista.append(s)
        return s


def okres_nazwa(od, do):
    return f"{MIESIACE_RZ[od.month - 1]} {od.year} – {MIESIACE_RZ[do.month - 1]} {do.year}"


O1 = (dt.date(2024, 10, 1), dt.date(2025, 9, 30))
O2 = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
O1_NAZWA, O2_NAZWA = okres_nazwa(*O1), okres_nazwa(*O2)


def pl_data(s):
    """'17.03.2026' albo '2026-03-17' → date."""
    if "-" in s:
        return dt.date.fromisoformat(s)
    d, m, r = s.split(".")
    return dt.date(int(r), int(m), int(d))


def kw_dop(q):
    """'2025-Q4' → 'IV kwartału 2025'."""
    r, k = q.split("-Q")
    return f"{MIESIACE_RZ[int(k) - 1]} kwartału {r}"


def q3_teksty(V):
    """Rozkład spadku marży III kwartału 2026, Safari w kwartale i baza powracających (d_wynik.txt, punkty 1 i 2).
    Używają go zakładki „Czy to wzrost” (za c_szkic.md, sekcja 1c) i „Wynik biznesu” (za d_teksty_strony.md)."""
    D, q = V["D"], V["rr"]
    ost = q.index[-1]
    rok = int(ost[:4])
    pop = f"{rok - 1}{ost[4:]}"
    go = V["q3_go_osobno"]
    pw = V["q3_powtorne"]
    zaks = [D[k] for k in ("safari_zaksiegowane_q3_po_odjeciu_tla", "safari_zaksiegowane_q3_bez_odjecia_tla",
                           "safari_zaksiegowane_q3_tempo_q3_po_odjeciu_tla", "safari_zaksiegowane_q3_tempo_q3_bez_odjecia_tla")]
    utr = [D["safari_utracone_q3_po_odjeciu_tla"], D["safari_utracone_q3_bez_odjecia_tla"], V["p1_q3_lo"][0], V["p1_q3_hi"][0]]
    przed_d, po_d = V["safari_okresy"][1], V["safari_okresy"][2]
    q3_od = dt.date(rok, 3 * int(ost[-1]) - 2, 1)
    przed_q3 = q3_od - dt.timedelta(days=1)
    prow = D["q3_reszta_z1k_prowizja_wklad"]
    t = {}
    t["wstep"] = (f"Marża spadła o {tz(-D['q3_zmiana_marzy'])}. Według przyjętej reguły pacjenci nowych kampanii zostawili "
                  f"{tz(D['q3_nowe_z1k_przed_kampaniami_2026'])} marży przed kampaniami przy {tz(D['q3_nowe_z1k_wydatki_2026'])} "
                  f"wydatków, czyli wyszli prawie na zero ({tzn(D['q3_nowe_z1k_marza_2026'])}). Reszta biznesu straciła "
                  f"{tz(-D['q3_reszta_z1k_zmiana'])}:")
    t["reszta"] = [
        f"opłaty TelemediGO {tz(D['q3_reszta_z1k_telemedigo_zmiana'])}, w tym {tz(go[8])} sprzedaży osobnej w newsletterze "
        f"({liczba(go[0])} zakupów we wrześniu {rok - 1} wobec {liczba(go[1])} w całym {kw_nazwa(ost)});",
        f"wyższe wydatki kampanii działających w obu latach {tz(D['q3_reszta_z1k_wydatki_wklad'])};",
        f"marża konsultacji {tzn(D['q3_reszta_z1k_konsultacje_marza_zmiana'])}: powtórnych zamówień jest więcej "
        f"({liczba(pw[1])} wobec {liczba(pw[0])}), ale każde zostawia mniej marży ({liczba(pw[3], 2)} zł wobec "
        f"{liczba(pw[2], 2)} zł);",
        "prowizja bez zmian." if abs(prow) < 100 else f"prowizja {tzn(prow)}.",
    ]
    luka = -D["q3_reszta_z1k_luka_bez_telemedigo"]
    t["luka"] = (f"Księgowo lukę, która zostaje po odjęciu TelemediGO ({tz(luka)}), wyjaśnia wzrost wydatków kampanii "
                 f"działających w obu latach, częściowo skompensowany wzrostem marży konsultacji. Rozkład księgowy nie "
                 f"rozdziela wpływu Safari od innych zmian przychodu: awaria mogła obniżyć marżę konsultacji, która mimo to "
                 f"wzrosła o {t1(D['q3_reszta_z1k_konsultacje_marza_zmiana'])} tys. zł. Według sesji płatności podział się "
                 f"odwraca: nowe kampanie "
                 f"{tz(D['q3_nowe_z2_marza_2026'])}, reszta {tzn(D['q3_reszta_z2_zmiana'])}. Suma jest ta sama, a podział między "
                 f"nowe kampanie a resztę zależy od reguły źródła. Cały spadek przypada na wrzesień "
                 f"({tz(D['q3_miesiac_09_zmiana_marzy'])}); lipiec {tzn(D['q3_miesiac_07_zmiana_marzy'])}, sierpień "
                 f"{tzn(D['q3_miesiac_08_zmiana_marzy'])}.")
    t["baza"] = (f"Wcześniejsze kwartały okresu 1 nie miały jeszcze bazy powracających. Marża z pacjentów pozyskanych w "
                 f"poprzednich kwartałach to {proc(D['baza_udzial_w_marzy_proc_2024_q4'], 0)} marży {kw_dop('2024-Q4')}, "
                 f"{proc(D['baza_udzial_w_marzy_proc_2025_q1'])} {kw_dop('2025-Q1')} i {proc(D['baza_udzial_w_marzy_proc_2025_q3'])} "
                 f"{kw_dop(pop)}. Bez tej bazy marża rośnie rok do roku o {proc(D['marza_bez_bazy_zmiana_proc_2025_q4'])} zamiast "
                 f"{proc(D['marza_zmiana_proc_2025_q4'])} w {kw_nazwa('2025-Q4')} i o {proc(D['marza_bez_bazy_zmiana_proc_2026_q1'])} "
                 f"zamiast {proc(D['marza_zmiana_proc_2026_q1'])} w {kw_nazwa('2026-Q1')}.")
    t["baza_szkic"] = (f" Wzrost tych kwartałów jest więc zawyżony startem od zera, a miarodajne jest porównanie III kwartałów "
                       f"(baza {proc(D['baza_udzial_w_marzy_proc_2025_q3'])} i {proc(D['baza_udzial_w_marzy_proc_2026_q3'])} marży). "
                       f"W {kw_nazwa(ost)} baza {liczba(V['q3_baza_pac']['2026-Q3'])} pacjentów dała mniej marży niż rok wcześniej "
                       f"baza {liczba(V['q3_baza_pac']['2025-Q3'])} pacjentów ({t1(D['baza_marza_2026_q3'])} wobec "
                       f"{tz(D['baza_marza_2025_q3'])}): baza jest starsza, a nowsze roczniki wracają rzadziej (opis, bez "
                       f"rozdzielenia tych dwóch rzeczy).")
    t["baza_wynik"] = (f" Miarodajne jest więc porównanie III kwartałów (baza to {proc(D['baza_udzial_w_marzy_proc_2025_q3'])} i "
                       f"{proc(D['baza_udzial_w_marzy_proc_2026_q3'])} marży).")
    assert min(zaks) > luka
    t["safari"] = (f"Szacowana marża utracona przez awarię zakładania konta w Safari na iOS w samym {kw_nazwa(ost)} to "
                   f"{zakres(min(zaks) / 1000, max(zaks) / 1000, 1)} tys. zł, zależnie od odjęcia tła i założonego tempa strat, "
                   f"a osobny scenariusz powrotów pacjentów utraconych od {po_d} do {przed_q3.day}.{przed_q3:%m} daje "
                   f"{zakres(D['safari_powroty_q3_utraconych_przed_q3_od'] / 1000, D['safari_powroty_q3_utraconych_przed_q3_do'] / 1000, 1)} "
                   f"tys. zł. To kwota tego samego rzędu co cały spadek marży kwartału ({tz(-D['q3_zmiana_marzy'])}). "
                   f"Wyniku kwartału bez awarii nie mierzymy: to scenariusz przy założeniach pozycji 1.")
    t["safari_utr"] = (round(min(utr)), round(max(utr)))
    t["safari_p1"] = (f"W samym {kw_nazwa(ost)} szacowana marża utracona to około "
                      f"{zakres(min(zaks) / 1000, max(zaks) / 1000, 1)} tys. zł ({liczba(min(utr))}–{liczba(max(utr))} "
                      f"utracone pierwsze zamówienia z ich powrotami w tym samym kwartale, zależnie od odjęcia tła i założonego "
                      f"tempa strat), a osobny scenariusz powrotów pacjentów utraconych od {po_d} do {przed_q3.day}.{przed_q3:%m} "
                      f"daje {zakres(D['safari_powroty_q3_utraconych_przed_q3_od'] / 1000, D['safari_powroty_q3_utraconych_przed_q3_do'] / 1000, 1)} "
                      f"tys. zł. To kwota tego samego rzędu co spadek marży rok do roku ({tz(-D['q3_zmiana_marzy'])}); wyniku "
                      f"kwartału bez awarii nie mierzymy.")
    t["safari_zaks"] = (min(zaks), max(zaks))
    t["safari_wynik"] = (f"Awaria zakładania konta w Safari na iOS kosztowała w samym {kw_nazwa(ost)} szacunkowo "
                         f"{zakres(min(zaks) / 1000, max(zaks) / 1000, 1)} tys. zł marży ({liczba(min(utr))}–{liczba(max(utr))} "
                         f"utracone pierwsze zamówienia z ich powrotami w tym samym kwartale, zależnie od odjęcia tła i założonego "
                         f"tempa strat). Osobny scenariusz powrotów pacjentów utraconych od {po_d} do {przed_q3.day}.{przed_q3:%m} "
                         f"daje jeszcze {zakres(D['safari_powroty_q3_utraconych_przed_q3_od'] / 1000, D['safari_powroty_q3_utraconych_przed_q3_do'] / 1000, 1)} "
                         f"tys. zł. Wyniku kwartału bez awarii nie mierzymy: to rachunek przy założeniach pozycji 1 listy "
                         f"priorytetów.")
    t["wynik_rozklad"] = (
        f"Rozkład spadku {kw_nazwa(ost).replace('kwartale', 'kwartału')} (opis księgowy, nie zmierzony wpływ). " + t["wstep"][:-1]
        + f": opłaty TelemediGO {tz(D['q3_reszta_z1k_telemedigo_zmiana'])} (w tym sprzedaż osobna w newsletterze {tz(go[8])}: "
          f"{liczba(go[0])} zakupów we wrześniu {rok - 1} wobec {liczba(go[1])} w całym {kw_nazwa(ost)}), wyższe wydatki "
          f"kampanii działających w obu latach {tz(D['q3_reszta_z1k_wydatki_wklad'])}, marża konsultacji "
          f"{tzn(D['q3_reszta_z1k_konsultacje_marza_zmiana'])} (więcej powtórnych zamówień, ale każde zostawia mniej marży: "
          f"{liczba(pw[3], 2)} zł wobec {liczba(pw[2], 2)} zł). Księgowo lukę, która zostaje po odjęciu TelemediGO "
          f"({tz(luka)}), wyjaśnia wzrost wydatków kampanii działających w obu latach, częściowo skompensowany wzrostem marży "
          f"konsultacji. Rozkład księgowy nie rozdziela wpływu Safari od innych zmian przychodu. Według sesji płatności podział "
          f"się odwraca: nowe "
          f"kampanie {tz(D['q3_nowe_z2_marza_2026'])}, reszta {tzn(D['q3_reszta_z2_zmiana'])}; suma jest ta sama. Cały spadek "
          f"przypada na wrzesień ({tz(D['q3_miesiac_09_zmiana_marzy'])}); lipiec {tzn(D['q3_miesiac_07_zmiana_marzy'])}, "
          f"sierpień {tzn(D['q3_miesiac_08_zmiana_marzy'])}.")
    t["wynik_baza"] = t["baza"] + t["baza_wynik"]
    return t


def godziny_tekst(V, wariant):
    """Opóźnienia u internisty według godziny terminu (d_retencja.txt, punkt 1). Wariant "c" to pozycja 6 listy priorytetów
    (c_szkic.md), "d" to zakładka „Po zakupie” (d_teksty_strony.md); różnią się tylko początkiem i jednym słowem."""
    D = V["D"]
    op = lambda k: D["op_internista_wszyscy_" + k]  # noqa: E731
    h610 = range(6, 11)
    p2 = [op(f"godz{h:02d}_ponad15_proc_okres2") for h in h610]
    p1 = [op(f"godz{h:02d}_ponad15_proc_okres1") for h in h610]
    n2 = [op(f"godz{h:02d}_wizyty_okres2") for h in h610]
    poza, pol, noc = "poza_5_13_czyli_0_4_i_14_23_", "poludnie_bez_12_czyli_13_15_", "noc_bez_5_czyli_0_4_"
    pr = lambda k: D["op_pozostali_lekarze_wszyscy_rano_6_11_" + k]  # noqa: E731
    para = lambda h: (f"{proc(op(f'godz{h:02d}_ponad15_proc_okres2'))} ({liczba(op(f'godz{h:02d}_wizyty_okres2'))}) wobec "  # noqa: E731
                      f"{proc(op(f'godz{h:02d}_ponad15_proc_okres1'))} ({liczba(op(f'godz{h:02d}_wizyty_okres1'))})")
    poczatek = ("największy wzrost to jeden blok od 5:00 do 12:59, a mniejszy zostaje o 13:00. Wizyt spóźnionych ponad "
                "15 minut jest o 5:00 " if wariant == "c" else
                "rosną najbardziej w jednym porannym bloku od 5:00 do 12:59, a mniej o 13:00. Odsetek wizyt spóźnionych "
                "ponad 15 minut: o 5:00 ")
    srodek = "w południe i w nocy" if wariant == "c" else "w porach „południe” i „noc”"
    pol_t = (f"południe bez 12:00 rośnie z {proc(op(pol + 'ponad15_proc_okres1'))} do {proc(op(pol + 'ponad15_proc_okres2'))}, "
             f"noc bez 5:00 z" if wariant == "c" else
             f"bez godziny 12:00 południe rośnie tylko z {proc(op(pol + 'ponad15_proc_okres1'))} do "
             f"{proc(op(pol + 'ponad15_proc_okres2'))}, a noc bez 5:00 z")
    pozostali = (f"U pozostałych lekarzy rano bez istotnej zmiany ({proc(pr('ponad15_proc_okres1'))} z "
                 f"{liczba(pr('wizyty_okres1'))} wizyt wobec {proc(pr('ponad15_proc_okres2'))} z {liczba(pr('wizyty_okres2'))})."
                 if wariant == "c" else
                 f"U pozostałych lekarzy rano bez istotnej zmiany: {proc(pr('ponad15_proc_okres2'))} z "
                 f"{liczba(pr('wizyty_okres2'))} wizyt wobec {proc(pr('ponad15_proc_okres1'))} z {liczba(pr('wizyty_okres1'))}.")
    assert pr("ponad15_zmiana_od") < 0 < pr("ponad15_zmiana_do")
    return (poczatek + f"{proc(op('godz05_ponad15_proc_okres2'))} ({liczba(op('godz05_wizyty_okres2'))} wizyt) wobec "
            f"{proc(op('godz05_ponad15_proc_okres1'))} ({liczba(op('godz05_wizyty_okres1'))}) rok wcześniej, o 6:00–10:00 "
            f"od {proc(min(p2))} do {proc(max(p2))} ({zakres(min(n2), max(n2))} wizyt w godzinie) wobec "
            f"{zakres(min(p1), max(p1), 1)}%, o 12:00 {para(12)}, o 13:00 {para(13)}. Poza 5:00–13:59 odsetek jest prawie "
            f"taki sam: {proc(op(poza + 'ponad15_proc_okres2'))} z {liczba(op(poza + 'wizyty_okres2'))} wizyt wobec "
            f"{proc(op(poza + 'ponad15_proc_okres1'))} z {liczba(op(poza + 'wizyty_okres1'))}. Wzrost {srodek} to głównie "
            f"brzegi porannego bloku: {pol_t} {proc(op(noc + 'ponad15_proc_okres1'))} do "
            f"{proc(op(noc + 'ponad15_proc_okres2'))}. " + pozostali)


def poranek_tekst(V, wariant):
    """Wizyty z najwcześniejszym porannym terminem dnia (d_retencja.txt, punkt 2)."""
    D = V["D"]
    if wariant == "c":
        wstep = ("już wizyty z najwcześniejszym porannym terminem w danym dniu są często spóźnione, a w danych zagregowanych "
                 "nie widać narastania opóźnień w ciągu poranka. Wizyty z najwcześniejszym porannym terminem dnia są "
                 "spóźnione ponad 15 minut w ")
        n1 = f" ({liczba(D['ranek_pierwsza_okres_2_wizyty'])} wizyt, okres 2)"
    else:
        wstep = ("Już wizyty z najwcześniejszym porannym terminem w danym dniu są często spóźnione, a w danych zagregowanych "
                 "nie widać narastania opóźnień w ciągu poranka: wizyty z najwcześniejszym porannym terminem dnia są "
                 "spóźnione ponad 15 minut w ")
        n1 = f" ({liczba(D['ranek_pierwsza_okres_2_wizyty'])} wizyt)"
    return (wstep + proc(D["ranek_pierwsza_okres_2_ponad15_proc"]) + n1 +
            f", kolejne w {proc(D['ranek_kolejne_okres_2_ponad15_proc'])} ({liczba(D['ranek_kolejne_okres_2_wizyty'])}), "
            f"średnio {liczba(D['ranek_pierwsza_okres_2_srednie_min'], 1)} wobec {liczba(D['ranek_kolejne_okres_2_srednie_min'], 1)} "
            f"minuty. W tym samym miesiącu (II–IX 2026) godziny z 8 i więcej wizytami mają o "
            f"{liczba(D['ranek_ii_ix_2026_w_miesiacu_wysokie_minus_niskie_obciazenie_pkt'], 1)} punktu procentowego więcej "
            f"spóźnionych niż godziny z 1–3 wizytami.")


def teksty_d(V):
    """Nowe brzmienia zakładek „Lejek”, „Kohorty”, „Po zakupie”, „Wynik biznesu” i „Zdarzenia” (notatki/d_teksty_strony.md).
    Klucze słownika `kontrola` wskazują sekcję notatki (nagłówek ###), z którą kontrola porównuje liczby."""
    D, wb = V["D"], V["wbud"]
    T, dod = {}, {}
    # Lejek: rozkład zmiany konwersji (a5p_lejek.txt, sekcja 4)
    rz = V["rozklad_lejka"]
    assert all(abs(rz[g][1]) > abs(rz[g][0]) for g in ("strona_wejscia", "pacjent"))
    para = lambda g: f"{zn(rz[g][0], 2)} i {zn(rz[g][1], 2)} punktu"  # noqa: E731
    T["lejek_rozklad"] = (
        f"Wynik rozkładu zależy od podziału. Według przeglądarki zmiana struktury ruchu daje {zn(rz['przegladarka'][0], 2)} "
        f"punktu procentowego, a zmiana konwersji w obrębie grup {zn(rz['przegladarka'][1], 2)} punktu. Według kampanii to "
        f"{para('kampania')}. Według strony wejścia ({para('strona_wejscia')}) i według tego, czy osoba już kupowała "
        f"({para('pacjent')}), większość spadku wychodzi jako zmiana konwersji w obrębie grup. Przyjmujemy podział według "
        f"przeglądarki i kampanii, bo ruch zmienił się właśnie w tym wymiarze: przybyło sesji nowych kampanii w przeglądarkach "
        f"w aplikacjach, których w okresie 1 nie było. Na tej samej stronie wejścia albo w tej samej grupie pacjentów nowy "
        f"ruch miesza się ze starym, więc jego niższa konwersja wygląda jak spadek w obrębie grupy.")
    T["lejek_naprawy"] = ("To nie zwalnia z naprawy. Jedną rzecz trzeba naprawić na stronie na pewno (Safari na iOS), a drugą "
                          "sprawdzić (przeglądarki wbudowane w aplikacje w ruchu osób, które znają już stronę).")
    # Lejek: przeglądarki wbudowane w aplikacje (d_kampanie.txt, 1e)
    ex = Dodane()
    m2, t2, lo = wb["meta2"], wb["tt2"], wb["lekarz_oba"]
    T["przegl_tytul"] = ("Przeglądarki wbudowane w aplikacje: w reklamach do nowych odbiorców nie płacą rzadziej niż zwykłe, "
                         "w ruchu powracających płacą rzadziej")
    zw_ = V["zwykle_nowe"]
    T["przegl_tekst"] = (
        f"W kampaniach do nowych odbiorców nie wykryliśmy niższej konwersji przeglądarki w aplikacji niż zwykłej w tej samej "
        f"kampanii (okres {ex('2')}: Meta na L4 {proc(m2[4], 2)} z {liczba(m2[0])} sesji wobec {proc(m2[5], 2)} z "
        f"{liczba(zw_['meta'])}, TikTok {proc(t2[4], 2)} z {liczba(t2[0])} wobec {proc(t2[5], 2)} z {liczba(zw_['tt'])}; Meta "
        f"„lekarz online” różnica {liczba(lo[6], 2)} punktu procentowego, od {liczba(lo[7], 2)} do {zn(lo[8], 2)}, "
        f"{liczba(lo[0])} sesji w przeglądarkach wbudowanych w dwóch latach). Niska konwersja tych kampanii nie wynika więc "
        f"wyraźnie z przeglądarki; naprawą, którą da się wycenić, jest obietnica reklamy i strona wejścia (Priorytety, "
        f"pozycja 5). W ruchu osób, które znają już stronę, jest inaczej: w okresie 2 sesje w przeglądarkach w aplikacjach "
        f"płacą rzadziej niż zwykłe w tej samej kampanii: w remarketingu Meta o {liczba(-wb['rmkt2'][6], 1)} punktu "
        f"({liczba(wb['rmkt2'][0])} sesje w przeglądarkach wbudowanych), w Google Ads na markę o {liczba(-wb['brand2'][6], 1)} "
        f"punktu ({liczba(wb['brand2'][0])}), w wejściach bezpośrednich o {liczba(-wb['bezp2'][6], 1)} punktu "
        f"({liczba(wb['bezp2'][0])}). Luka jest na wyborze usługi i na kroku konta. Porównanie jest obserwacyjne: nie "
        f"rozdziela wpływu przeglądarki od cech użytkowników (Czego nie wiemy, punkt 19).")
    dod["Przeglądarki wbudowane w aplikacje"] = ex.lista
    # Lejek: konta bez zakupu (d_retencja.txt, punkt 6)
    ex = Dodane()
    assert D["konta_bez_zakupu_proc_z_wejsciem_crm"] == 0
    assert D["konta_bez_zakupu_proc_z_krokiem_konta"] == 100 and D["konta_bez_zakupu_proc_z_wyborem_uslugi"] == 100
    T["konta"] = (
        f"{liczba(D['konta_bez_zakupu_konta'])} z {liczba(D['konta_wszystkie'])} kont ({proc(D['konta_bez_zakupu_proc_kont'])}) "
        f"nie ma żadnego zakupu, a odsetek jest podobny w obu okresach ({proc(D['konta_rejestracja_okres1.0_bez_zakupu_proc'])} "
        f"z {ex(liczba(D['konta_rejestracja_okres1.0_konta']))} kont założonych w okresie 1 i "
        f"{proc(D['konta_rejestracja_okres2.0_bez_zakupu_proc'])} z {ex(liczba(D['konta_rejestracja_okres2.0_konta']))} "
        f"w okresie 2). Każde z tych kont wybrało usługę i przeszło krok konta, a "
        f"{proc(D['konta_bez_zakupu_proc_ze_startem_platnosci'])} z nich zaczęło płatność. "
        f"{proc(D['konta_bez_zakupu_proc_zgoda'])} z {liczba(D['konta_bez_zakupu_konta'])} ma zgodę marketingową (stan na "
        f"{data(O2[1])}), ale w danych nie ma ani jednego ich wejścia z newslettera albo SMS-a (widać kliknięcia, nie "
        f"wysyłki). Test: Czego nie wiemy, punkt 20.")
    dod["Konta bez zakupu"] = ex.lista
    # Kohorty: wiek, płeć i województwo (d_retencja.txt, punkt 5)
    ex = Dodane()
    l4 = lambda g, gr: D[f"demo_l4_powrot90_wiek_rec_l4_{g}_z1k_{gr}_" + ("proc_okres2" if True else "")]  # noqa: E731
    l4n = lambda g: D[f"demo_l4_powrot90_wiek_rec_l4_{g}_z1k_nowe_pacjenci_okres2"]  # noqa: E731
    gr_w = ("a_do_29", "b_30_44", "c_45_plus")
    reszta_l4 = [l4(g, "reszta") for g in gr_w]
    reszta_n = [D[f"demo_l4_powrot90_wiek_rec_l4_{g}_z1k_reszta_pacjenci_okres2"] for g in gr_w]
    wiek_r = [D["demo_z1k_okres1_reszta_wszystkie_sredni_wiek"], D["demo_z1k_okres2_reszta_wszystkie_sredni_wiek"]]
    assert round(wiek_r[0], 1) == round(wiek_r[1], 1)
    st = V["standaryzacja"]
    woj1 = {k: v for k, v in D.items() if k.startswith("demo_woj_") and k.endswith("_z1k_reszta_powrot90_proc_okres1")}
    assert max(woj1, key=woj1.get) == "demo_woj_dolnoslaskie_z1k_reszta_powrot90_proc_okres1"
    assert D["demo_wojewodztwa_z1k_zmiana_powrotu_q_p"] > 0.05
    dl = lambda k: D["demo_woj_dolnoslaskie_z1k_reszta_" + k]  # noqa: E731
    T["kohorty_demo"] = (
        f"Wiek, płeć, wielkość miejscowości i województwo nie zmieniają wniosku. Pacjenci nowych kampanii są młodsi (średnio "
        f"{liczba(D['demo_z1k_okres2_nowe_kampanie_wszystkie_sredni_wiek'], 1)} roku, "
        f"{liczba(D['demo_z1k_okres2_nowe_kampanie_wszystkie_pacjenci'])} pacjentów, wobec {liczba(wiek_r[1], 1)} roku pozostałych "
        f"w obu okresach), ale pierwsze L4 z nowych kampanii wraca w 90 dniach rzadko w każdej grupie wieku: "
        f"{proc(l4('a_do_29', 'nowe'))} do 29 lat ({liczba(l4n('a_do_29'))} pacjentów), {proc(l4('b_30_44', 'nowe'))} "
        f"w wieku 30–44 lat ({liczba(l4n('b_30_44'))}) i {proc(l4('c_45_plus', 'nowe'))} od 45 lat ({liczba(l4n('c_45_plus'))}), "
        f"wobec {zakres(min(reszta_l4), max(reszta_l4), 1)}% u pozostałych pacjentów z pierwszym L4 "
        f"({zakres(min(reszta_n), max(reszta_n))} pacjentów w grupie wieku; okres 2, kohorty do {data(O2[1] - dt.timedelta(days=90))}). "
        f"Po przeważeniu okresu 2 "
        f"strukturą wieku i płci okresu 1 spadek powrotu w 90 dniach bez nowych kampanii zostaje ten sam: "
        f"{liczba(st['z1k'][7], 1)} punktu procentowego według przyjętej reguły i {liczba(st['z2'][7], 1)} zamiast "
        f"{liczba(st['z2'][6], 1)} punktu według sesji płatności. Udział nowych kampanii w nowych pacjentach okresu 2 jest "
        f"podobny we wszystkich województwach ({zakres(D['demo_wojewodztwa_z1k_udzial_nowych_min_proc'], D['demo_wojewodztwa_z1k_udzial_nowych_max_proc'], 1)}%). "
        f"Jeden trop regionalny: w dolnośląskim powrót poza nowymi kampaniami spada z {proc(dl('powrot90_proc_okres1'))} "
        f"({liczba(dl('pacjenci_okres1'))} pacjentów) do {proc(dl('powrot90_proc_okres2'))} ({liczba(dl('pacjenci_okres2'))}), "
        f"ale test wszystkich województw razem nie odrzuca, że zmiana jest wszędzie podobna, a dolnośląskie miało najwyższy "
        f"powrót w okresie 1.")
    dod["Wiek, płeć i województwo"] = ex.lista
    # Po zakupie: opóźnienia po godzinach i w ciągu poranka (d_retencja.txt, punkty 1 i 2)
    ex = Dodane()
    op = lambda k: D["op_internista_wszyscy_" + k]  # noqa: E731
    pg = V["pozostali_godz"]   # h → n_o1, n_o2, p15_o1, p15_o2, ...
    T["po_blok"] = "Opóźnienia u internisty " + godziny_tekst(V, "d")
    T["po_poranek"] = (
        poranek_tekst(V, "d") + " Odczytanie, nie pomiar: to bardziej pasuje do stałego przesunięcia od początku dnia "
        "(późniejszy start względem grafiku, inna organizacja zapisów albo kolejki) niż do kolejki, która narasta, bo "
        "pacjentów jest więcej, niż lekarze zdążą przyjąć. Najwcześniejszy termin liczymy dla całej sieci, a nie dla "
        "pojedynczego lekarza; bez identyfikatorów lekarzy i grafików mechanizmu nie rozstrzygamy (Czego nie wiemy, punkt 4).")
    dod["Opóźnienia po godzinach i w ciągu poranka"] = ex.lista
    komorka = lambda p_, n_: f"{proc(p_)} ({liczba(n_)})"  # noqa: E731
    T["po_godziny"] = {
        "tytul": "Opóźnienia według godziny terminu: wizyty spóźnione ponad 15 minut (w nawiasie liczba wizyt odbytych)",
        "kolumny": ["Godzina terminu", f"Internista, okres {O1_NAZWA}", f"Internista, okres {O2_NAZWA}",
                    "Internista: zmiana (punkty procentowe)", f"Pozostali lekarze, okres {O1_NAZWA}",
                    f"Pozostali lekarze, okres {O2_NAZWA}"],
        "wiersze": [{"opis": f"{h}:00–{h}:59", "komorki": [
            komorka(op(f"godz{h:02d}_ponad15_proc_okres1"), op(f"godz{h:02d}_wizyty_okres1")),
            komorka(op(f"godz{h:02d}_ponad15_proc_okres2"), op(f"godz{h:02d}_wizyty_okres2")),
            zn(op(f"godz{h:02d}_ponad15_proc_okres2") - op(f"godz{h:02d}_ponad15_proc_okres1")).replace("−0,0", "0,0")
            if abs(op(f"godz{h:02d}_ponad15_proc_okres2") - op(f"godz{h:02d}_ponad15_proc_okres1")) >= 0.05 else "0,0",
            komorka(pg[h][2], pg[h][0]), komorka(pg[h][3], pg[h][1])],
            "blok": 5 <= h <= 12} for h in range(24)],
        "przypis": "Internista i pozostali lekarze, wszyscy pacjenci, okres według dnia terminu. Źródło: "
                   "analiza/wyniki/d_retencja.txt, punkt 1 (analiza/d_retencja.py).",
    }
    # Wynik biznesu: rozkład spadku III kwartału, Safari, baza (d_wynik.txt, punkty 1 i 2)
    q3t = q3_teksty(V)
    T["wynik_rozklad"], T["wynik_safari"], T["wynik_baza"] = q3t["wynik_rozklad"], q3t["safari_wynik"], q3t["wynik_baza"]
    # Zdarzenia: Google Ads na markę (d_kampanie.txt, punkt 5)
    mk, md = V["marka_okna"], {k: [pl_data(x) for x in v] for k, v in V["marka_daty"].items()}
    A_, B_, D_ = md["A_przed_caly"], md["B_po_awarii_safari"], md["D_po_spadku"]
    T["zdarzenie_marka"] = {
        "id": "marka_konwersja", "obszar": "lejek", "od": D_[0].isoformat(), "rodzaj": "zmiana poziomu",
        "tytul": "Google Ads na markę: spada konwersja sesji do płatności",
        "co": "Sesja do płatności u osób, które jeszcze nie kupowały, spada w kampanii Google Ads na markę (gs_brand). "
              "Przyczyny w danych nie widać (Czego nie wiemy, punkt 22).",
        "ile": f"Z {proc(mk['A_przed_caly'][-1])} ({liczba(mk['A_przed_caly'][1])} sesji, {data(A_[0])}–{data(A_[1])}) do "
               f"{proc(mk['D_po_spadku'][-1])} ({liczba(mk['D_po_spadku'][1])} sesje, {D_[0].day}.{D_[0]:%m}–{data(D_[1])}), "
               f"czyli o około {zakres(-V['marka_na30'][3], -V['marka_na30'][1], 1)} zamówienia na 30 dni zależnie od okna "
               f"porównania. Bez Safari na iOS spadek jest prawie taki sam "
               f"({liczba(D['p5_kanal_google_ads_marka_bez_safari_ios_D_minus_B_pkt'], 1)} punktu procentowego wobec "
               f"{B_[0].day}.{B_[0]:%m}–{data(B_[1])}), zmiana struktury ruchu (urządzenie, przeglądarka, strona wejścia) daje "
               f"około zera, a inne kanały w tych dniach się nie zmieniają. Rok wcześniej w tym samym sezonie spadek był "
               f"mniejszy ({liczba(V['marka_rok_wczesniej'], 1)} punktu) i nieistotny, więc część może być sezonowa. W tym "
               f"samym czasie rośnie koszt kliknięcia tej kampanii (z {liczba(D['p4_gs_brand_koszt_klikniecia_okres1_zl'], 2)} zł "
               f"w okresie 1 do {liczba(D['p4_gs_brand_koszt_klikniecia_okres2_zl'], 2)} zł w okresie 2).",
        "skad": "Metoda wykrywania zmian w seriach dziennych wskazała ten dzień; sprawdzenie w oknach przed i po, bez Safari "
                "na iOS, ze strukturą ruchu i z tym samym sezonem rok wcześniej. Źródło: analiza/d_kampanie.py → "
                "analiza/wyniki/d_kampanie.txt, punkt 5.",
        "link": f"#lejek?pac=nie_kupowal&podz=kampania&krok=k5&a={A_[0]}_{A_[1]}&b={D_[0]}_{D_[1]}&w=gs_brand",
    }
    T["kontrola"] = {
        "Rozkład zmiany konwersji": [T["lejek_rozklad"]],
        "Przeglądarki wbudowane w aplikacje": [T["lejek_naprawy"], T["przegl_tytul"], T["przegl_tekst"]],
        "Konta bez zakupu": [T["konta"]],
        "Wiek, płeć i województwo": [T["kohorty_demo"]],
        "Opóźnienia po godzinach i w ciągu poranka": [T["po_blok"], T["po_poranek"]],
        "Rozkład spadku marży w III kwartale 2026": [T["wynik_rozklad"], T["wynik_safari"], T["wynik_baza"]],
        "Google Ads na markę od 22.05.2026": [T["zdarzenie_marka"][k] for k in ("tytul", "co", "ile")],
    }
    T["dodane"] = dod
    return T


def kontrola_d(T, dodatkowe=None):
    """Liczby w tekstach pozostałych zakładek wobec sekcji ### w notatki/d_teksty_strony.md (jak kontrola ze szkicem).
    `dodatkowe`: {nagłówek: ([teksty], [liczby dodane])} z eksportu b_eksport.py (np. dni kampanii crm_go_upsell)."""
    with open(D_TEKSTY, encoding="utf-8") as f:
        s = f.read().replace("\r\n", "\n")
    fr = {m.group(1).strip(): m.group(0) for m in re.finditer(r"^### (.+?)$.*?(?=^### |^## |\Z)", s, re.M | re.S)}
    bloki = {k: (v, T["dodane"].get(k, [])) for k, v in T["kontrola"].items()}
    for k, (tk, dd) in (dodatkowe or {}).items():
        bloki[k] = (bloki.get(k, ([], []))[0] + tk, bloki.get(k, ([], []))[1] + dd)
    wynik = []
    for nazwa, (tk, dd) in bloki.items():
        klucz = next((h for h in fr if h.startswith(nazwa)), None)
        if klucz is None:
            wynik.append((f"d:{nazwa[:14]}", 0, ["brak sekcji w notatce"], []))
            continue
        wzor, dod = set(tokeny(fr[klucz])), set(tokeny(" | ".join(dd)))
        toks = [x for t in tk for x in tokeny(t)]
        wynik.append((f"d:{nazwa[:14]}", len(toks), sorted({x for x in toks if x not in wzor and x not in dod}),
                      sorted({x for x in toks if x not in wzor and x in dod})))
    return wynik


# ---------------------------------------------------------------- 1. czy to wzrost

def czy_wzrost(V):
    ex = Dodane()
    n1, n2 = V["nowi"][1], V["nowi"][2]
    wz = V["w1_zm"]
    W, B1, B2, NZ = V["pow_wszyscy"], V["pow_bez_z1k"], V["pow_bez_z2"], V["pow_nowe_z1k"]
    q = V["rr"]
    ost = q.index[-1]
    m2, m1 = q.loc[ost, "marza"], q.loc[ost, "marza_rok_wczesniej"]
    w2, w1 = q.loc[ost, "wydatki"], q.loc[ost, "wydatki_rok_wczesniej"]
    lo, hi = V["p1_q3_lo"], V["p1_q3_hi"]
    spadek = -V["kw_rozbicie"][0]
    rz1, rz2 = V["rozklad_z1k"], V["rozklad_z2"]
    udzial_nowych = (100 * rz1[5] / rz1[4], 100 * rz2[3] / rz2[2])   # udział nowych kampanii w spadku: Z1K, Z2
    puenta = [
        f"To nie jest wzrost w rozumieniu z zadania (więcej pacjentów i lepsza retencja naraz), bo z dwóch warunków "
        f"spełniony jest tylko pierwszy. Pacjentów z pierwszym zakupem jest o {proc(wz[0])} więcej ({liczba(n2)} wobec "
        f"{liczba(n1)}), ale retencja jest gorsza: powrót w 90 dniach {proc(W['p90_o2'])} wobec {proc(W['p90_o1'])} na "
        f"tych samych dniach kalendarzowych, a marża na pacjenta w 90 dniach {liczba(V['m90'][2], 1)} zł wobec "
        f"{liczba(V['m90'][1], 1)} zł.",
        f"Obecność pacjentów dwóch nowych kampanii na L4 odpowiada opisowo za około "
        f"{zakres(min(udzial_nowych), max(udzial_nowych), 0, '%')} spadku powrotu, zależnie od reguły źródła, ale bez nich "
        f"retencja też spada (do {proc(B1['p90_o2'])} według przyjętej reguły albo {proc(B2['p90_o2'])} według sesji "
        f"płatności), a nowych pacjentów spoza tych kampanii przybyło tylko o {zakres(wz[1], wz[2], 1, '%')}.",
    ]
    zamkniecie = (f"Pod koniec okresu wzrost przestał się przekładać na wynik: w {kw_nazwa(ost)} marża była o "
                  f"{liczba(abs(q.loc[ost, 'marza_zmiana_proc']), 1)}% niższa niż rok wcześniej ({tz(m2)} wobec {tz(m1)}), "
                  f"choć wydatki na kampanie były {liczba(q.loc[ost, 'wydatki_iloraz'], 2)} raza wyższe ({tz(w2)} wobec "
                  f"{tz(w1)}).")
    safari = q3_teksty(V)["safari"]
    pacjenci = [
        f"Nowych pacjentów jest {liczba(n2)} w okresie 2 wobec {liczba(n1)} w okresie 1, czyli {zn(wz[0])}%.",
        f"Bez pacjentów dwóch nowych kampanii na L4 jest ich {liczba(V['bez_z1k'])} według przyjętej reguły "
        f"({zn(wz[1])}%) albo {liczba(V['bez_z2'])} według sesji płatności ({zn(wz[2])}%).",
        f"Z kanałów bezpłatnych (wejścia bezpośrednie, bezpłatne wyszukiwanie, program poleceń) przybyło "
        f"{proc(wz[3])}: z {liczba(V['bezpl'][1])} do {liczba(V['bezpl'][2])}.",
        "Nie wiemy, ilu pacjentów nowych kampanii przyszłoby i bez nich (dodatkowość, pierwsza pozycja w zakładce "
        "„Czego nie wiemy”).",
    ]
    n180_1, n180_2, p180_1, p180_2 = V["p180"][:4]
    okna = [{"dni": o, "p1": W[f"p{o}_o1"], "n1": int(W[f"n{o}_o1"]), "p2": W[f"p{o}_o2"], "n2": int(W[f"n{o}_o2"])}
            for o in (30, 60, 90)]
    okna.append({"dni": 180, "p1": p180_1, "n1": int(n180_1), "p2": p180_2, "n2": int(n180_2)})
    dok = V["powroty_dokladne"]
    for o in okna:
        o["tekst1"] = f"{proc(o['p1'])} ({liczba(o['n1'])} pacjentów)"
        o["tekst2"] = f"{proc(o['p2'])} ({liczba(o['n2'])} pacjentów)"
        p1d, p2d = dok[o["dni"]][:2]
        o["zmiana"] = ex(f"{zn(p2d - p1d)} pkt proc.")   # różnica z liczb niezaokrąglonych
    us, pw = V["uslugi_bez"], V["powracajacy"]
    Dd = V["D"]

    def usl(u, reg, przedzial=False):
        k = f"powrot90_{u}_bez_nowych_{reg}_"
        tekst = (f"{proc(Dd[k + 'proc_okres1'])} ({liczba(Dd[k + 'pacjenci_okres1'])} pacjentów) do "
                 f"{proc(Dd[k + 'proc_okres2'])} ({liczba(Dd[k + 'pacjenci_okres2'])})")
        if przedzial:
            tekst += f", od {liczba(Dd[k + 'zmiana_od'], 1)} do {zn(Dd[k + 'zmiana_do'])} punktu"
        return tekst
    retencja = [
        "Powrót to kolejne zamówienie, które nie zostało anulowane. Liczymy go na tych samych dniach kalendarzowych "
        "i tylko w kohortach z pełnym oknem obserwacji.",
        f"Marża na pacjenta w 90 dniach przed kosztem pozyskania: {liczba(V['m90'][2], 1)} zł wobec "
        f"{liczba(V['m90'][1], 1)} zł, czyli {liczba(V['m90'][2] - V['m90'][1], 1)} zł.",
        f"Kolejne zamówienia na pacjenta w 90 dniach: {liczba(Dd['kolejne90_wszyscy_okres2_srednia_na_pacjenta'], 3)} wobec "
        f"{liczba(Dd['kolejne90_wszyscy_okres1_srednia_na_pacjenta'], 3)}, czyli o "
        f"{proc(100 * (1 - Dd['kolejne90_wszyscy_okres2_srednia_na_pacjenta'] / Dd['kolejne90_wszyscy_okres1_srednia_na_pacjenta']))} "
        f"mniej (te same dni kalendarzowe, {liczba(Dd['kolejne90_wszyscy_okres2_pacjenci'])} i "
        f"{liczba(Dd['kolejne90_wszyscy_okres1_pacjenci'])} pacjentów). Bez pacjentów nowych kampanii "
        f"{liczba(Dd['kolejne90_bez_nowych_z1k_okres2_srednia_na_pacjenta'], 3)} według przyjętej reguły i "
        f"{liczba(Dd['kolejne90_bez_nowych_z2_okres2_srednia_na_pacjenta'], 3)} według sesji płatności.",
        f"Bez pacjentów nowych kampanii retencja też spada. Powrót w 90 dniach wynosi {proc(B1['p90_o2'])} według "
        f"przyjętej reguły ({liczba(B1['n90_o2'])} pacjentów) i {proc(B2['p90_o2'])} według sesji płatności "
        f"({liczba(B2['n90_o2'])}), wobec {proc(W['p90_o1'])}. Marża na pacjenta w 90 dniach poza nowymi kampaniami prawie "
        f"stoi według przyjętej reguły ({liczba(V['m90_bez_z1k'], 1)} zł wobec {liczba(V['m90'][1], 1)} zł), a według sesji "
        f"płatności spada do {liczba(V['m90_bez_z2'], 1)} zł.",
        f"Pacjenci nowych kampanii wracają w 90 dniach w {proc(NZ['p90_o2'])} ({liczba(NZ['n90_o2'])} pacjentów).",
        "Według pierwszej usługi, bez pacjentów nowych kampanii (95% przedział różnicy): spada po e-recepcie z "
        f"{usl('internista_e_recepta', 'z1k')}, a po wizycie u innego specjalisty z {usl('inny_specjalista', 'z1k')}. Bez "
        f"istotnej zmiany: pediatra z {usl('pediatra', 'z1k', True)}, psychiatra z {usl('psychiatra', 'z1k', True)}. To małe "
        f"grupy, więc nie piszemy, że powrót tam rośnie. Pierwsze L4 u internisty z pozostałych kanałów: według przyjętej "
        f"reguły bez istotnej zmiany, z {usl('internista_l4', 'z1k', True)}; według sesji płatności spada do "
        f"{proc(Dd['powrot90_internista_l4_bez_nowych_z2_proc_okres2'])} "
        f"({liczba(Dd['powrot90_internista_l4_bez_nowych_z2_pacjenci_okres2'])}), od "
        f"{liczba(Dd['powrot90_internista_l4_bez_nowych_z2_zmiana_od'], 1)} do "
        f"{liczba(Dd['powrot90_internista_l4_bez_nowych_z2_zmiana_do'], 1)} punktu. „Bez zmiany” trzyma się więc tylko w "
        f"jednej regule.",
        f"Liczba osób, które wróciły w 90 dniach, rośnie: {liczba(pw[4])} wobec {liczba(pw[3])} ({zn(pw[5])}%). Spada "
        f"odsetek, a nie liczba powracających. Porównanie 90-dniowe obejmuje pierwsze zakupy do {int(pw[2])} "
        f"{MIESIACE_DOP[int(pw[1]) - 1]} każdego roku, a nie pełne roczniki.",
    ]
    w3 = V["w3"]
    marza = w3.loc["marza"]
    wyd = w3.loc["wydatki_kampanie"]
    dz, cz = V["dash_zam"], V["czyste_zam"]
    rz1, rz2 = V["rozklad_z1k"], V["rozklad_z2"]
    zastrz = [
        {"tytul": "Dashboard liczy dane na surowo.",
         "tekst": f"Zawiera {liczba(V['dup'])} zdublowane zamówienia z {ex(V['dup_daty'])}, {liczba(V['testy_razem'][0])} zamówień kont "
                  f"testowych i przychód przed zwrotami. Po oczyszczeniu zamówienia rosną o {proc(cz[0])} "
                  f"({ex(liczba(cz[1]))} → {ex(liczba(cz[2]))}) zamiast {proc(round(dz[0]), 0)}, a przychód z konsultacji "
                  f"po zwrotach o {proc(cz[3])} zamiast {proc(round(dz[3]), 0)}. Nowi pacjenci prawie się nie zmieniają "
                  f"({zn(V['dash_surowo'][0])}% na surowo, {zn(wz[0])}% po oczyszczeniu), a TelemediGO wcale "
                  f"({zn(V['dash_surowo'][3])}%)."},
        {"tytul": "Start od zera.",
         "tekst": f"W okresie 1 nie było bazy pacjentów z poprzedniego roku. W okresie 2 pacjenci pozyskani w okresie 1 "
                  f"złożyli {liczba(w3.loc['zam_powt_o1', 'okres_2'])} zamówień powtórnych, które dały "
                  f"{liczba(w3.loc['marza_powt_kohorty_o1', 'okres_2'] / 1000)} tys. zł marży konsultacji. Sumy roczne "
                  f"z definicji faworyzują więc drugi rok."},
        {"tytul": "Wynik biznesu rośnie wolniej niż sprzedaż.",
         "tekst": f"Marża po koszcie lekarza, kampaniach i prowizji wynosi {liczba(marza['okres_1'] / 1000)} tys. zł w "
                  f"okresie 1 i {liczba(marza['okres_2'] / 1000)} tys. zł w okresie 2, czyli "
                  f"{zn(100 * (marza['okres_2'] / marza['okres_1'] - 1))}%. Po odjęciu marży powtórnych konsultacji "
                  f"pacjentów pozyskanych w okresie 1 to {zn(V['w3_bez'][1])}%, a po odjęciu także ich opłat za "
                  f"TelemediGO ({tz(V['w3_bez_go'][0])}) {zn(V['w3_bez_go'][2])}%. To rozbicie księgowe, a nie wynik "
                  f"biznesu, który startuje od zera: nie modeluje zmian wydatków ani zachowania pacjentów. Wydatki na "
                  f"kampanie rosną o {proc(100 * (wyd['okres_2'] / wyd['okres_1'] - 1), 0)} (z "
                  f"{liczba(wyd['okres_1'] / 1000)} do {liczba(wyd['okres_2'] / 1000)} tys. zł)."},
        {"tytul": "Struktura pacjentów się zmieniła.",
         "tekst": f"Pacjenci nowych kampanii to {proc(100 * V['nowe_7268'] / n2, 0)} nowych pacjentów okresu 2 według "
                  f"przyjętej reguły ({liczba(V['nowe_7268'])} z {liczba(n2)}) i "
                  f"{proc(100 * Dd['demo_z2_okres2_nowe_kampanie_wszystkie_pacjenci'] / n2, 0)} według sesji płatności "
                  f"({liczba(Dd['demo_z2_okres2_nowe_kampanie_wszystkie_pacjenci'])}). Zostawiają {liczba(V['nowe_marza'][4], 1)} zł "
                  f"marży w 90 dniach wobec {liczba(V['m90_bez_z1k'], 1)} zł pozostałych."},
        {"tytul": "Obie reguły źródła.",
         "tekst": f"Podział spadku powrotu (z {proc(W['p90_o1'])} do {proc(W['p90_o2'])}) na nowe i stare kampanie zależy "
                  f"od reguły. Według przyjętej reguły to {liczba(abs(rz1[5]), 1)} punktu procentowego nowych kampanii i "
                  f"{liczba(abs(rz1[8]), 1)} punktu starych (nowe kampanie: około {proc(udzial_nowych[0], 0)} spadku). "
                  f"Według sesji płatności to {liczba(abs(rz2[3]), 1)} i {liczba(abs(rz2[6]), 1)} punktu (około "
                  f"{proc(udzial_nowych[1], 0)}). Kierunek jest ten sam w obu, a to rozkład opisowy, nie zmierzony wpływ "
                  f"kampanii."},
    ]
    # marża po kwartałach rok do roku
    kw, mm = V["kw"], V["mm"]
    wiersze = []
    for k in q.index:
        wiersze.append({"kw": kw_krotko(k), "m2": tz(q.loc[k, "marza"]), "m1": tz(q.loc[k, "marza_rok_wczesniej"]),
                        "zm": f"{zn(q.loc[k, 'marza_zmiana_proc'])}%", "w2": tz(q.loc[k, "wydatki"]),
                        "w1": tz(q.loc[k, "wydatki_rok_wczesniej"]), "il": liczba(q.loc[k, "wydatki_iloraz"], 2),
                        "minus": bool(q.loc[k, "marza"] < q.loc[k, "marza_rok_wczesniej"])})
    rozb = V["kw_rozbicie"]
    przed_proc = q.loc[ost, "przed_kampaniami_zmiana_proc"]
    rok = int(ost[:4])
    mies = []
    for mc in (7, 8, 9):
        a, b = mm.loc[f"{rok - 1}-{mc:02d}", "marza"], mm.loc[f"{rok}-{mc:02d}", "marza"]
        mies.append((mc, a, b))
    nazwy = {7: "lipiec", 8: "sierpień", 9: "wrzesień"}
    go_dni, go_n = V["go_start"]
    q3t = q3_teksty(V)
    kwartaly = {
        "naglowek": "Wzrost marży słabnie z kwartału na kwartał, a wydatki na kampanie rosną coraz szybciej.",
        "wiersze": wiersze,
        "punkty": [
            f"Marża przed kampaniami (przychód po zwrotach + TelemediGO − koszt lekarza) rośnie w {kw_nazwa(ost)} o "
            f"{proc(przed_proc)} ({tzn(rozb[1])}), ale wydatki na kampanie rosną o {tz(-rozb[2])}.",
            f"We wrześniu {rok - 1} ruszyła sprzedaż TelemediGO w newsletterze ({liczba(go_n)} zakupów w {liczba(go_dni)} "
            f"dni), co podnosi {kw_krotko(ost).split()[0]} kwartał {rok - 1}. Bez opłat za TelemediGO marża "
            f"{kw_krotko(ost).split()[0]} kwartału {rok} też jest niższa: {zn(q.loc[ost, 'marza_bez_telemedigo_zmiana_proc'])}% "
            f"rok do roku.",
            "W samych miesiącach: " + ", ".join(
                f"{nazwy[mc]}{' ' + str(rok) if i == 0 else ''} {t1(b)}{' tys. zł' if i == 0 else ''} wobec {t1(a)} tys. zł"
                for i, (mc, a, b) in enumerate(mies)) +
            ". Niższy jest więc kwartał jako całość, a nie każdy miesiąc.",
        ],
        "rozklad_tytul": f"Rozkład spadku {kw_nazwa(ost).replace('kwartale', 'kwartału')} (opis księgowy, nie zmierzony wpływ)",
        "rozklad_wstep": q3t["wstep"], "rozklad_punkty": q3t["reszta"], "luka": q3t["luka"],
        "baza": q3t["baza"] + q3t["baza_szkic"],
    }
    opis = {"tytul": "To opis, nie przyczyna.",
            "tekst": "Widzimy spadek obserwowanej retencji, także po wyłączeniu pacjentów nowych kampanii. Nie dowodzi to, "
                     "że identyczni pacjenci zachowują się gorzej. Rozkład na strukturę i zachowanie nie mówi też, co by "
                     "się stało bez nowych kampanii. Spadek w starych kampaniach zbiega się z porannymi opóźnieniami "
                     "u internistów, ale ich nie dowodzi (czwarta pozycja w zakładce „Czego nie wiemy”)."}
    # TelemediGO: jedna z czterech liczb dashboardu (dopisek Kuby po przeglądzie trzeciej wersji)
    exg = Dodane()
    ty = V["go_typy"]
    razem = ty.loc["razem"]
    nazwy_typow = {"1_kasa_z_pierwszym_zamowieniem": "Przy kasie z pierwszym zamówieniem pacjenta",
                   "2_kasa_z_kolejnym_zamowieniem": "Przy kasie z kolejnym zamówieniem",
                   "3_osobno_newsletter_crm_go_upsell": "Osobno, z newslettera crm_go_upsell", "razem": "Razem"}
    tab_go = [{"opis": nazwy_typow[t], "komorki": [liczba(ty.loc[t, "okres_1"]), liczba(ty.loc[t, "okres_2"]),
                                                   zn(ty.loc[t, "zmiana"], 0), proc(ty.loc[t, "udzial_we_wzroscie_proc"], 0)]}
              for t in ty.index]
    ka = V["go_kasa"]
    k = {(int(r["okres"]), r["zamowienie"][:1]): r for _, r in ka.iterrows()}
    gr, bn, roz = V["go_grupy"], V["go_bez_nowych"], V["go_rozklad_1"]
    nowe_n = gr.loc["2_meta_l4_szybko", "n_okres_2"] + gr.loc["3_tiktok", "n_okres_2"]
    nowe_proc = (gr.loc["2_meta_l4_szybko", "n_okres_2"] * gr.loc["2_meta_l4_szybko", "odsetek_okres_2"]
                 + gr.loc["3_tiktok", "n_okres_2"] * gr.loc["3_tiktok", "odsetek_okres_2"]) / nowe_n
    g2a = V["go_2a"]
    go_dni2, go_n2 = V["go_start"]
    g4 = V["go_4a"]
    telemedigo = {
        "tytul": f"TelemediGO: skąd {zn(razem['zmiana_proc'])}% sprzedaży",
        "puenta": f"Wzrost o {liczba(razem['zmiana'])} zakupów (z {liczba(razem['okres_1'])} do {liczba(razem['okres_2'])}, "
                  f"{zn(razem['zmiana_proc'])}%) wynika z tego, że jest więcej zamówień, i z pełnego roku sprzedaży "
                  f"w newsletterze. Odsetek kupujących przy pierwszym zamówieniu spada, a przy kolejnych zamówieniach rośnie "
                  f"tylko lekko (z {proc(k[(1, '2')]['odsetek_proc'], 2)} do {proc(k[(2, '2')]['odsetek_proc'], 2)}).",
        "tabela": {"kolumny": ["Typ zakupu", "Okres 1", "Okres 2", "Zmiana", "Udział we wzroście"], "wiersze": tab_go},
        "punkty": [
            f"Sprzedaż osobna w newsletterze ruszyła {V['go_start_data']}. W okresie 1 działała więc tylko "
            f"{liczba(go_dni2)} dni, a sprzedała w nich {liczba(go_n2)} członkostw. W okresie 2 sprzedaje średnio "
            f"{liczba(V['go_osobno_mies'])} miesięcznie.",
            f"Przy kasie przybywa zakupów, bo jest więcej zamówień, a nie wyższy odsetek kupujących. Przy pierwszym "
            f"zamówieniu odsetek kupujących spada z {proc(k[(1, '1')]['odsetek_proc'], 2)} "
            f"({exg(liczba(k[(1, '1')]['zamowienia_do_oferty']))} zamówień) do {proc(k[(2, '1')]['odsetek_proc'], 2)} "
            f"({exg(liczba(k[(2, '1')]['zamowienia_do_oferty']))}): więcej zamówień dodaje {liczba(roz[1])} zakupów, "
            f"a niższy odsetek odejmuje {liczba(abs(roz[2]))}. Przy kolejnych zamówieniach odsetek rośnie lekko, z "
            f"{proc(k[(1, '2')]['odsetek_proc'], 2)} ({exg(liczba(k[(1, '2')]['zamowienia_do_oferty']))}) do "
            f"{proc(k[(2, '2')]['odsetek_proc'], 2)} ({exg(liczba(k[(2, '2')]['zamowienia_do_oferty']))}).",
            f"Spadek odsetka przy pierwszym zamówieniu to w całości pacjenci nowych kampanii na L4: kupuje u nich "
            f"{proc(nowe_proc)} ({exg(liczba(nowe_n))} pacjentów). Bez nich odsetek stoi: "
            f"{proc(k[(1, '1')]['odsetek_proc'], 2)} wobec {proc(bn['odsetek'], 2)} ({exg(liczba(bn['n']))} pacjentów).",
            f"Opłata {OPLATA_GO} zł nie pokrywa średniej zniżki. Członkostwa z okresu 1 ({liczba(g2a['czlonkostwa'])}, "
            f"pełne 365 dni) przyniosły {zl(g2a['oplaty_zl'])} opłat i dostały {zl(g2a['znizka_efektywna_zl'])} zniżki "
            f"efektywnej, czyli {zl(g2a['oplaty_minus_znizki_efektywne_zl'])} ({liczba(g2a['oplata_minus_znizka_efektywna_na_czlonkostwo'], 2)} zł "
            f"na członkostwo). W okresie 2 przybliżenie to {liczba(V['go_okres2'], 1)} zł na członkostwo. To rachunek "
            f"przy założeniu, że te same wizyty zostałyby kupione bez TelemediGO, a nie strata programu: nie wiemy, "
            f"ile wizyt członkostwo dokłada.",
            f"Kupujący TelemediGO przy pierwszym zamówieniu wracają w 90 dniach częściej niż podobni pacjenci: "
            f"{proc(g4[4])} wobec {proc(g4[5])} w okresie 2 ({liczba(g4[0])} kupujących). Dane nie mówią, ile z tego to "
            f"wpływ zniżki, a ile to, że kupują ci, którzy i tak planują wracać. Rozstrzygnie to test z pozycji 12: "
            f"losowy, bezpłatny dostęp do zniżek.",
        ],
        "linki": [{"tekst": "Priorytety: pozycja 12, test TelemediGO", "href": "#priorytety?p=12"},
                  {"tekst": "Priorytety: pozycja 10, warunki TelemediGO u specjalistów", "href": "#priorytety?p=10"},
                  {"tekst": "Kohorty: kupujący TelemediGO przy pierwszym zakupie", "href": "#kohorty?okno=90&podz=go0&wygl=28"},
                  {"tekst": "Lejek: zakupy samego TelemediGO",
                   "href": "#lejek?typ=samo_telemedigo&pac=wszyscy&podz=kampania&krok=sesje&w=crm_go_upsell"}],
        "zrodlo": "Liczby: analiza/c_telemedigo.py → analiza/wyniki/c_telemedigo.txt (1a, 1b, 1e, 1f, 2a, 2b, 4a). "
                  "Notatka: notatki/c_szkic.md, sekcja 2.",
        "_dodane": exg.lista,
    }
    do90 = O2[1] - dt.timedelta(days=90)
    skrot = {
        "odpowiedz": "Nie, to nie jest wzrost w rozumieniu Telemedi. Pacjentów jest więcej, ale wracają rzadziej, a pod koniec "
                     "okresu marża spada.",
        "liczby": [
            f"nowych pacjentów jest o {proc(wz[0])} więcej: {liczba(n2)} w {O2_NAZWA} wobec {liczba(n1)} w {O1_NAZWA};",
            f"powrót w 90 dniach spadł z {proc(W['p90_o1'])} do {proc(W['p90_o2'])} (kohorty {O2[0].day}.{O2[0]:%m}–"
            f"{do90.day}.{do90:%m} w obu latach, na tych samych dniach kalendarzowych; {liczba(W['n90_o1'])} i "
            f"{liczba(W['n90_o2'])} pacjentów);",
            f"w {kw_nazwa(ost)} marża była o {liczba(abs(q.loc[ost, 'marza_zmiana_proc']), 1)}% niższa niż rok wcześniej, przy "
            f"wydatkach na kampanie {liczba(q.loc[ost, 'wydatki_iloraz'], 2)} raza wyższych.",
        ],
        "decyzje": [
            {"tekst": "naprawić zakładanie konta w Safari na iOS (pozycja 1);", "href": "#priorytety?p=1"},
            {"tekst": "wstrzymać TikToka na L4 i Google Ads na specjalistów jako pauzy, które da się cofnąć w jeden dzień "
                      "(pozycje 3 i 4);", "href": "#priorytety?p=3"},
            {"tekst": "oczyścić codzienny raport i dodać alarmy na lejku (pozycja 2).", "href": "#priorytety?p=2"},
        ],
        "kwota": f"górny scenariusz odzyskania marży po naprawie Safari na iOS to "
                 f"{zakres(V['p1_lo'][3] / 1000, V['p1_hi'][3] / 1000)} tys. zł na pełny rok, w horyzoncie 90 dni od "
                 f"pozyskania, przed kosztem naprawy (pozycja 1).",
    }
    return {
        "skrot": skrot,
        "werdykt": "Nie. Pacjentów jest więcej, ale wracają rzadziej, więc z dwóch warunków wzrostu spełniony jest tylko jeden.",
        "telemedigo": telemedigo,
        "puenta": puenta, "zamkniecie": zamkniecie, "safari": safari,
        "pacjenci": {"liczba": f"{zn(wz[0])}%", "podpis": f"{liczba(n1)} → {liczba(n2)} nowych pacjentów", "punkty": pacjenci},
        "retencja": {"liczba": f"{proc(W['p90_o1'])} → {proc(W['p90_o2'])}",
                     "podpis": f"powrót w 90 dniach, {liczba(W['n90_o1'])} i {liczba(W['n90_o2'])} pacjentów", "okna": okna,
                     "punkty": retencja},
        "kwartaly": kwartaly, "zastrzezenia": zastrz + [{"tytul": "Marża po kwartałach rok do roku.",
                                                        "tekst": kwartaly["naglowek"] + " Tabela i liczby są w karcie "
                                                                 "„Wynik pod koniec okresu” wyżej."}, opis],
        "linki": [{"tekst": "Kohorty: powrót w 90 dniach, nowe kampanie na L4 i pozostałe", "href": "#kohorty?okno=90&podz=grupa&wygl=28"},
                  {"tekst": "Kohorty: powrót bez pacjentów nowych kampanii", "href": "#kohorty?okno=90&f_grupa=pozostale&wygl=28"},
                  {"tekst": "Wynik biznesu: marża po kwartałach", "href": "#wynik"},
                  {"tekst": "Jakość danych: od dashboardu do danych oczyszczonych", "href": "#jakosc"}],
        "zrodlo": "Liczby: analiza/c_priorytety.py → analiza/wyniki/c_priorytety.txt (W1–W4, P1), analiza/wyniki/a5r_kohorty.txt "
                  "(180 dni), analiza/wyniki/a5r_struktura.txt (L4 z L4, rozkład spadku), analiza/wyniki/a5e_ekonomia.txt, "
                  "analiza/wyniki/c_telemedigo.txt. Notatka: notatki/c_szkic.md, sekcja 1.",
        "_dodane": ex.lista,
    }


# ---------------------------------------------------------------- 2. priorytety

def macierz(V, kampania, mnoznik=None):
    """Tabela kampanii: wynik dziś, po naprawie zwrotów, wyłączenie przy 100/50/0% pacjentów dodatkowych; obie reguły,
    90 i 180 dni, kwoty z dni działania kampanii i przeliczone na pełny rok."""
    e1, e3, e3b = V["e1"], V["e3"], V["e3b"]
    kol = [("Z1K", 90), ("Z1K", 180), ("Z2", 90), ("Z2", 180)]

    def w3(reg, k):
        return e3[(e3["kampania"] == kampania) & (e3["regula"] == reg)].iloc[0][k]

    def w3b(reg, k):
        return e3b[(e3b["kampania"] == kampania) & (e3b["regula"] == reg)].iloc[0][k]

    def w1(reg, proc_, k):
        return e1[(e1["kampania"] == kampania) & (e1["regula"] == reg) & (e1["dodatkowi_proc"] == proc_)].iloc[0][k]

    wiersze = [
        ("Wynik kampanii dziś", lambda r, o: w3(r, "obecny_wynik") if o == 90 else w3b(r, "obecny_wynik_180")),
        ("Wynik po naprawie zwrotów (wariant A)", lambda r, o: w3(r, "po_naprawie_A") if o == 90 else w3b(r, "po_naprawie_A_180")),
        ("Zmiana marży po wyłączeniu: 100% pacjentów dodatkowych", lambda r, o: w1(r, 100, f"zmiana_marzy{o}")),
        ("Zmiana marży po wyłączeniu: 50% pacjentów dodatkowych", lambda r, o: w1(r, 50, f"zmiana_marzy{o}")),
        ("Zmiana marży po wyłączeniu: 0% pacjentów dodatkowych", lambda r, o: w1(r, 0, f"zmiana_marzy{o}")),
    ]
    out = []
    for opis, f in wiersze:
        kom = []
        for reg, o in kol:
            v = float(f(reg, o))
            kom.append({"w": tzn(v), "rok": tzn(v * mnoznik) if mnoznik else None, "minus": v < 0})
        out.append({"opis": opis, "komorki": kom})
    return out


KOLUMNY_MACIERZY = ["Przyjęta reguła, 90 dni", "Przyjęta reguła, 180 dni", "Sesja płatności, 90 dni", "Sesja płatności, 180 dni"]


def priorytety(V, linki_lejka):
    karty = []
    ek = V["ek"]
    tt, me = NOWE[1], NOWE[0]
    dni_tt, dni_me = V["dni"][tt], V["dni"][me]
    mn_tt, mn_me = V["mn"][tt], V["mn"][me]
    przed_od, przed_do, po_od, po_do, dni_saf = V["safari_okresy"]
    d_saf = pl_data(po_od + "." + po_do.split(".")[-1])
    d_saf_kon = pl_data(po_do)
    lo, hi = V["p1_lo"], V["p1_hi"]
    q3lo, q3hi = V["p1_q3_lo"], V["p1_q3_hi"]
    pm = V["p1_marza"]
    sk = V["safari_krok"]   # przed, po, z_terminem_po, k5_do_k3_po, utracone, na_30_dni
    D = V["D"]
    q3t = q3_teksty(V)
    kw_q3 = kw_dop(V["rr"].index[-1])

    def karta(nr, tytul, sekcje, linki, zrodlo, tabela=None, ex=None):
        k = {"nr": nr, "tytul": tytul, "sekcje": [{"tytul": t, "punkty": p} for t, p in sekcje if p],
             "linki": linki, "zrodlo": zrodlo, "wdrozenie_krotko": SZACUNEK[nr], "_dodane": ex.lista if ex else []}
        if tabela:
            k["tabela"] = tabela
        karty.append(k)

    # 1. Safari na iOS
    ex = Dodane()
    karta(1, "Naprawić zakładanie konta w Safari na iOS", [
        ("Z danych", [
            f"Od {data(d_saf)} w Safari na iPhone'ach i iPadach gwałtownie spada skuteczność zakładania nowego konta "
            f"(konta dalej powstają, ale rzadziej: {liczba(V['safari_konta'][1])} zamiast {liczba(V['safari_konta'][0])} "
            f"w 60 dniach).",
            f"Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spada z {proc(sk[0])} (od {ex(przed_od)} "
            f"do {ex(przed_do)}) do {proc(sk[1])} (od {ex(po_od)} do {ex(po_do)}, {ex(liczba(sk[2]))} sesji z wyborem "
            f"terminu) i nie wraca.",
            "Logowanie do istniejących kont działa. Inne przeglądarki tego nie mają, a spadek jest w głównych kanałach; "
            "TikTok ma za małą próbę do oceny.",
        ]),
        ("Ile warta", [
            f"W {liczba(lo[1])} dniach od {d_saf.day}.{d_saf:%m} do {data(d_saf_kon)} to {zakres(lo[0], hi[0])} utraconych "
            f"pierwszych zamówień, czyli {zakres(lo[2], hi[2])} rocznie.",
            f"Nowy pacjent z pierwszą płatnością w Safari na iOS zostawia w okresie 2 średnio {liczba(pm['marza90'], 1)} zł "
            f"marży przed kosztem pozyskania w 90 dniach ({ex(liczba(pm['n90']))} pacjentów) i {liczba(pm['marza180'], 1)} zł "
            f"w 180 dniach ({ex(liczba(pm['n180']))}).",
            f"Daje to {zakres(lo[3] / 1000, hi[3] / 1000)} tys. zł rocznie w horyzoncie 90 dni i "
            f"{zakres(lo[4] / 1000, hi[4] / 1000)} tys. zł w horyzoncie 180 dni.",
            q3t["safari_p1"],
            f"{zakres(lo[0], hi[0])} to scenariusz przy przyjętych założeniach, a nie przedział ufności.",
        ]),
        ("Założenia", [
            "Utracone pierwsze zamówienie to utracony nowy pacjent. To górna granica: odpadnięci nie kupują później częściej "
            "w tej samej przeglądarce, ale innych urządzeń nie widzimy.",
            "Nie doliczamy kosztu pozyskania, bo wejście już zostało opłacone.",
            "Skala problemu utrzymywałaby się przez rok. Przeliczenie z marca–września może zaniżać, bo pomija zimę.",
            "Kwoty to marża rocznika odzyskanych pacjentów, a nie wpływy w całości w tym samym roku.",
        ]),
        ("Po czym poznamy", [
            f"Krok konta po wyborze terminu w Safari na iOS u osób, które jeszcze nie kupowały, wraca z około "
            f"{proc(sk[1], 0)} do około {proc(sk[0], 0)} w ciągu tygodnia od poprawki, a zakładanie kont wraca do poziomu "
            f"sprzed {d_saf.day}.{d_saf:%m} (około {liczba(dziesiatki(V['safari_konta'][0]))} w 60 dniach).",
        ]),
        ("Wdrożenie", [
            f"Powtórzenie rejestracji na iPhonie, logi błędów i lista zmian z {d_saf.day - 1}–{data(d_saf)} to 1–2 dni. "
            f"Sama poprawka to zwykle dni.",
        ]),
    ], [{"tekst": "Lejek: krok konta w Safari na iOS przed awarią i po niej", "href": linki_lejka["safari"]},
        {"tekst": "Zdarzenie na osi: awaria Safari na iOS", "href": "#zdarzenia?z=safari_ios"}],
        "analiza/wyniki/c_priorytety.txt (P1, P15), analiza/wyniki/d_wynik.txt (1f), analiza/wyniki/a5p_zdarzenia.txt (5d–5f), "
        "notatki/a5_pozyskanie.md (sekcja 2).",
        ex=ex)

    # 2. Pomiar
    ex = Dodane()
    dz, cz = V["dash_zam"], V["czyste_zam"]
    p15 = V["p15"]
    przych2 = V["w3"].loc["przychod_konsultacji", "okres_2"]
    karta(2, "Naprawić pomiar: codzienny raport, zamówienia testowe i alarmy", [
        ("Z danych", [
            f"Codzienny raport liczy dane na surowo. Zawiera {liczba(V['dup'])} zdublowane zamówienia z {V['dup_daty']}, "
            f"{liczba(V['testy_razem'][0])} zamówień {liczba(V['testy_konta'])} kont testowych i przychód przed zwrotami.",
            "Konta testowe mają kod TEST-QA albo zamówienia bez kodu, a wszystkie ich wizyty trwają 1 minutę u internisty.",
            f"Przez to raport pokazuje {zn(dz[0])}% zamówień ({ex(liczba(dz[1]))} → {ex(liczba(dz[2]))}) zamiast "
            f"{zn(cz[0])}% ({ex(liczba(cz[1]))} → {liczba(cz[2])}) i {zn(dz[3])}% przychodu z konsultacji zamiast "
            f"{zn(cz[3])}% po zwrotach.",
            f"Testów przybywa: {liczba(V['testy'][1])} zamówienia w okresie 1 i {liczba(V['testy'][2])} w okresie 2.",
            "Raport liczy też zamówienia i przychód, a nie marżę po koszcie pozyskania i powroty kohort. Dlatego kampanie "
            "na L4 wyglądały na nim jak wzrost.",
        ]),
        ("Co robimy", [
            "Raport bez duplikatów i kont testowych, przychód po zwrotach.",
            "Testy przeniesione z produkcji na środowisko testowe.",
            "Jednodniowe sprawdzenie w dziale rozliczeń, czy lekarze dostają wynagrodzenie za wizyty testowe.",
            f"Sprawdzenie, czy kod TEST-QA nie wyciekł poza {liczba(V['testy_konta'])} konta i czy przy duplikatach nikt "
            f"nie zapłacił dwa razy.",
            "Do raportu: marża po koszcie pozyskania według źródła, zwroty po wizycie według kampanii, powrót w 90 dniach "
            "każdej kohorty dziennej i kroki lejka według przeglądarki, z alarmami.",
            f"Do pilnowania: koszt kliknięcia w Google Ads na markę rośnie. Z {liczba(D['p4_gs_brand_koszt_klikniecia_okres1_zl'], 2)} zł "
            f"do {liczba(D['p4_gs_brand_koszt_klikniecia_okres2_zl'], 2)} zł ({zn(D['p4_gs_brand_koszt_klikniecia_zmiana_proc'])}% "
            f"rok do roku, {liczba(D['p4_gs_brand_klikniecia_okres1'])} i {liczba(D['p4_gs_brand_klikniecia_okres2'])} kliknięć), "
            f"co kwartał wyżej. Koszt pierwszego zamówienia z tej kampanii rośnie z "
            f"{liczba(D['p4_gs_brand_okres1_koszt_na_pierwsze_zamowienie_z1k_zl'], 2)} zł do "
            f"{liczba(D['p4_gs_brand_okres2_koszt_na_pierwsze_zamowienie_z1k_zl'], 2)} zł (przyjęta reguła). Kampania na e-receptę "
            f"drożeje o {proc(D['p4_gs_generic_erecepta_koszt_klikniecia_zmiana_proc'])} za kliknięcie, a całe Google Ads tanieje "
            f"o {proc(-D['p4_google_ads_razem_koszt_klikniecia_zmiana_proc'])}. Od {data(pl_data(V['marka_daty']['D_po_spadku'][0]))} "
            f"spada też konwersja sesji tej kampanii do płatności (niewiadoma 22).",
        ]),
        ("Ile warta", [
            f"Bezpośrednio {zl(V['testy_koszt2'])} rocznie, jeśli lekarze dostają {KOSZT_INTERNISTY} zł za każdą wizytę "
            f"testową (wszystkie są u internisty), albo 0 zł, jeśli nie dostają. Pieniądze już wypłacone są stracone, "
            f"a oszczędność dotyczy kolejnych miesięcy.",
            f"Pośrednio: bez poprawnych liczb nie da się prowadzić biznesu na kohortach. Alarm na krokach lejka wykryłby "
            f"awarię Safari po kilku dniach, a nie po {liczba(lo[1])}. Wykrycie po tygodniu ograniczyłoby stratę do "
            f"{proc(p15[0])} ({zakres(p15[1], p15[2])} zamówień zamiast {zakres(lo[0], hi[0])}).",
        ]),
        ("Po czym poznamy", [
            f"Raport pokazuje te same liczby co oczyszczona warstwa danych (w okresie 2: {liczba(cz[2])} zamówień i "
            f"{liczba(przych2 / 1e6, 3)} mln zł przychodu z konsultacji po zwrotach), a od ustalonej daty na produkcji nie "
            f"ma zamówień testowych.",
        ]),
        ("Wdrożenie", ["Sprawdzenie wynagrodzeń 1 dzień; raport i testy 1–2 tygodnie; alarmy 2–4 tygodnie."]),
    ], [{"tekst": "Jakość danych: duplikaty, zamówienia testowe, mostek od dashboardu", "href": "#jakosc"},
        {"tekst": "Zdarzenie na osi: duplikaty zamówień", "href": "#zdarzenia?z=duplikaty"}],
        "analiza/wyniki/c_priorytety.txt (P1b, P13, P15, W3), analiza/wyniki/a3_dashboard.txt, analiza/wyniki/a2_jakosc.txt, "
        "analiza/wyniki/d_kampanie.txt (4).", ex=ex)

    # 3. TikTok
    ex = Dodane()
    e = lambda kamp, reg, okno: ek[(kamp, reg, okno)]  # noqa: E731
    t90, t90b, t180, t180b = e(tt, "Z1K", "90"), e(tt, "Z2", "90"), e(tt, "Z1K", "180"), e(tt, "Z2", "180")
    p3, p3n = V["p3_cp"], V["p3_cp_napr"]
    E1 = V["e1"]
    wyl = lambda kamp, reg, pr, o=90: float(E1[(E1["kampania"] == kamp) & (E1["regula"] == reg) & (E1["dodatkowi_proc"] == pr)].iloc[0][f"zmiana_marzy{o}"])  # noqa: E731
    pt, pt2 = "p2_tiktok_l4_z1k_", "p2_tiktok_l4_z2_"
    wcz_od, wcz_do = (pl_data(x) for x in V["tt_wczesne"])
    karta(3, "Wstrzymać kampanię TikTok na L4", [
        ("Z danych", [
            f"Wynik na pacjenta jest ujemny w obu regułach i w obu oknach: {liczba(t90['wynik_na_pac'], 1)} i "
            f"{liczba(t90b['wynik_na_pac'], 1)} zł po 90 dniach, {liczba(t180['wynik_na_pac'], 1)} i "
            f"{liczba(t180b['wynik_na_pac'], 1)} zł po 180 dniach. Pacjenci wracają w 90 dniach w "
            f"{proc(t90['powrot_proc'])} ({ex(liczba(t90['nowi']))} pacjentów według przyjętej reguły, kohorty od "
            f"{ex(data(V['start'][tt]))}).",
        ]),
        ("Naprawić albo wyłączyć", [
            f"Kwoty z {liczba(dni_tt)} dni działania kampanii w okresie 2, w nawiasie pełny rok (mnożnik {ex(liczba(mn_tt, 2))}).",
            f"Dziś: {tz(p3[0])} ({t1(V['p11_tt'][0])}) według przyjętej reguły i {tz(p3[1])} ({t1(V['p11_tt'][1])}) według "
            f"sesji płatności po 90 dniach; {t1(p3[2])} i {tz(p3[3])} po 180 dniach.",
            f"Naprawić zwroty (wariant A, najlepszy): wynik {tzn(p3n[0])} albo {tz(p3n[1])} po 90 dniach; {zn(p3n[2] / 1000)} "
            f"i {tz(p3n[3])} po 180 dniach. Przeglądarki wbudowane w aplikacje nie dają w tym rachunku nic.",
            f"Wyłączyć: przy 100% pacjentów dodatkowych {zn(wyl(tt, 'Z1K', 100) / 1000)} do {tzn(wyl(tt, 'Z2', 100))} "
            f"({zn(V['p11_tt'][2] / 1000)} do {zn(V['p11_tt'][3] / 1000)} na pełny rok) po 90 dniach i "
            f"{zn(wyl(tt, 'Z1K', 100, 180) / 1000)} do {tzn(wyl(tt, 'Z2', 100, 180))} ({zn(V['p11_180'][0] / 1000)} do "
            f"{zn(V['p11_180'][1] / 1000)} na pełny rok) po 180 dniach; przy 0% {tzn(wyl(tt, 'Z1K', 0))} "
            f"({zn(V['p11_tt'][4] / 1000)}).",
        ]),
        ("Propozycja", [
            "Wstrzymać od razu, jako odwracalną pauzę. W przyjętych scenariuszach wyłączenie poprawia wynik w każdej "
            "regule, każdym oknie i każdym wariancie dodatkowości, a naprawa przy pełnym budżecie w najlepszym razie "
            "doprowadza wynik do zera.",
            f"Wynik po 180 dniach ({liczba(D[pt + '180_wynik_na_pacjenta_zl'], 1)} zł na pacjenta według przyjętej reguły, "
            f"warunkowy przedział od {liczba(D[pt + '180_wynik_od_zl'], 1)} do {zn(D[pt + '180_wynik_do_zl'])} zł) obejmuje "
            f"tylko wczesne kohorty z {wcz_od.day}.{wcz_od:%m}–{data(wcz_do)} ({liczba(D[pt + '180_pacjenci'])} pacjentów). "
            f"Miały one tańsze pozyskanie niż cały rocznik ({liczba(D[pt + '180_koszt_pozyskania_zl'], 1)} zł wobec "
            f"{liczba(D[pt + 'rocznik_koszt_pozyskania_zl'], 1)} zł), a w dniach 91–180 "
            + ("nie dorobiły marży" if abs(D[pt + "przyrost_marzy_90_180_wczesne_zl"]) < 0.05 else
               f"dorobiły tylko {liczba(D[pt + 'przyrost_marzy_90_180_wczesne_zl'], 1)} zł marży")
            + f". Lepszy wynik niż po 90 dniach ({liczba(D[pt + '90_wszystkie_kohorty_wynik_zl'], 1)} zł, "
            f"{liczba(D[pt + '90_wszystkie_kohorty_pacjenci'])} pacjentów) daje więc tańsze pozyskanie, a nie późniejsze powroty.",
            f"Przybliżenie dla całego rocznika (marża w 90 dniach wszystkich kohort plus przyrost z dni 91–180 wczesnych "
            f"kohort, minus koszt pozyskania całego rocznika) daje {liczba(D[pt + 'rocznik_wynik_180_przyblizony_zl'], 1)} zł "
            f"(od {liczba(D[pt + 'rocznik_wynik_180_przyblizony_od_zl'], 1)} do "
            f"{liczba(D[pt + 'rocznik_wynik_180_przyblizony_do_zl'], 1)} zł) według przyjętej reguły i "
            f"{liczba(D[pt2 + 'rocznik_wynik_180_przyblizony_zl'], 1)} zł według sesji płatności. Znak jest więc ujemny w obu "
            f"regułach.",
            "Naprawy (obietnica, ładowanie strony) sprawdzamy na Meta. TikTok może wrócić jako mały test, jeśli zadziałają.",
        ]),
        ("Po czym poznamy", [
            "Zmianę po pauzie porównujemy z ustalonym z góry punktem odniesienia (te same tygodnie rok wcześniej i kanały "
            "bez zmian): marża całego biznesu po wydatkach rośnie, a łączna liczba nowych pacjentów spada mniej niż liczba "
            "pacjentów przypisanych dotąd TikTokowi. Sam wzrost marży po pauzie nie dowodzi skutku, bo może wynikać "
            "z sezonu. Pauza daje przy okazji słaby, darmowy pomiar dodatkowości.",
        ]),
        ("Wdrożenie", ["1 dzień."]),
    ], [{"tekst": "Wynik biznesu: ekonomia kampanii, obie reguły", "href": "#wynik"},
        {"tekst": "Kohorty: nowe kampanie na L4 i pozostałe", "href": "#kohorty?okno=90&podz=grupa&wygl=28"},
        {"tekst": "Zdarzenie na osi: start TikToka", "href": "#zdarzenia?z=start_tiktok"}],
        "analiza/wyniki/c_priorytety.txt (P3, P11), analiza/wyniki/a5e_scenariusze.txt (E1, E3, E3b), "
        "analiza/wyniki/a5e_kampanie.csv, analiza/wyniki/d_kampanie.txt (2, 3), notatki/a5_ekonomia.md.",
        tabela={"tytul": f"Kampania TikTok na L4: kwoty z {liczba(dni_tt)} dni działania, pod spodem pełny rok "
                         f"(×{liczba(mn_tt, 2)})", "kolumny": KOLUMNY_MACIERZY, "wiersze": macierz(V, tt, mn_tt)},
        ex=ex)

    # 4. gs_generic_specjalisci
    ex = Dodane()
    gs = "gs_generic_specjalisci"
    g = {(r, o): e(gs, r, o) for r in ("Z1K", "Z2") for o in ("90", "180")}
    p7, p7d = V["p7"], V["p7_dokladnie"]
    marze = [p7[k][3] for k in p7]
    ce = V["cennik"]
    obn = [100 * (1 - p7[(r, "90")][3] / p7[(r, "90")][2]) for r in ("Z1K", "Z2")]
    wyl100 = [p7[k][5] for k in p7]
    wyl50 = [p7[k][6] for k in p7]
    tab4 = []
    for opis, idx in (("Wynik kampanii dziś", 4), ("Zmiana marży po wyłączeniu: 100% pacjentów dodatkowych", 5),
                      ("Zmiana marży po wyłączeniu: 50% pacjentów dodatkowych", 6),
                      ("Zmiana marży po wyłączeniu: 0% pacjentów dodatkowych", 7)):
        kom = []
        for r, o in (("Z1K", "90"), ("Z1K", "180"), ("Z2", "90"), ("Z2", "180")):
            # wynik dziś i wyłączenie przy 100% bez pośredniego zaokrąglania marży (uwaga Astry), 50% i 0% jak w P7
            v = p7d[(r, o)][1] if idx == 4 else -p7d[(r, o)][1] if idx == 5 else p7[(r, o)][idx]
            kom.append({"w": tzn(v), "rok": None, "minus": v < 0})
        tab4.append({"opis": opis, "komorki": kom})
    karta(4, "Wstrzymać gs_generic_specjalisci (Google Ads ogólne na specjalistów) do czasu zmiany cennika", [
        ("Z danych", [
            f"Wynik na pacjenta jest ujemny w obu regułach i obu oknach: {liczba(g[('Z1K', '90')]['wynik_na_pac'], 1)} i "
            f"{liczba(g[('Z2', '90')]['wynik_na_pac'], 1)} zł po 90 dniach, {liczba(g[('Z1K', '180')]['wynik_na_pac'], 1)} i "
            f"{liczba(g[('Z2', '180')]['wynik_na_pac'], 1)} zł po 180 dniach.",
            f"Koszt pozyskania wynosi {liczba(p7[('Z1K', '90')][2], 1)} zł (przyjęta reguła) albo "
            f"{liczba(p7[('Z2', '90')][2], 1)} zł (sesja płatności) przy marży pacjenta przed kosztem pozyskania "
            f"{zakres(min(marze), max(marze))} zł.",
            f"Jednym z głównych ograniczeń marży jest cennik: wizyta u specjalisty po cenie katalogowej zostawia tylko "
            f"{zakres(ce.loc['kardiolog', 'marza_bez_znizki'], ce.loc['ginekolog', 'marza_bez_znizki'])} zł ponad koszt "
            f"lekarza (pozycja 10). Wynik zależy też od kosztu pozyskania, struktury usług i powrotów.",
        ]),
        ("Naprawić albo wyłączyć", [
            f"Rocznie {liczba(p7[('Z1K', '90')][0])} nowych pacjentów według przyjętej reguły, {liczba(p7[('Z2', '90')][0])} "
            f"według sesji płatności, wydatki {tz(p7[('Z1K', '90')][1])}.",
            f"Dziś: {tz(p7d[('Z1K', '90')][1])} i {tz(p7d[('Z2', '90')][1])} po 90 dniach; {t1(p7d[('Z1K', '180')][1])} i "
            f"{tz(p7d[('Z2', '180')][1])} po 180 dniach (bez pośredniego zaokrąglania marży).",
            f"Naprawić: sama kampania musiałaby obniżyć koszt pozyskania o {dziesiatki(min(obn))}–{dziesiatki(max(obn))}%, "
            f"a to inny model kampanii, nie naprawa. Główną drogą naprawy jest cennik (pozycja 10). Uwaga: awaria Safari od "
            f"{d_saf.day}.{d_saf:%m} zawyża koszt pozyskania także tej kampanii.",
            f"Wyłączyć: {zn(min(wyl100) / 1000)} do {tzn(max(wyl100))} przy 100% pacjentów dodatkowych, "
            f"{zn(min(wyl50) / 1000)} do {tzn(max(wyl50))} przy 50%, {tzn(p7[('Z1K', '90')][7])} przy 0%. Założenia: "
            f"pacjenci dodatkowi mają średnią marżę przypisanych, pozostali zachowują się jak dziś, koszty pozostałych "
            f"kanałów się nie zmieniają.",
        ]),
        ("Propozycja", [
            "Wstrzymać. Wrócić po zmianie cennika albo gdy koszt pozyskania nie przekracza marży pacjenta w 90 dniach "
            "w obu regułach.",
        ]),
        ("Po czym poznamy", [
            "Marża po wydatkach rośnie, a nowych pacjentów u specjalistów z pozostałych kanałów nie ubywa więcej, niż "
            "kampania przypisywała.",
        ]),
        ("Wdrożenie", ["1 dzień."]),
    ], [{"tekst": "Wynik biznesu: ekonomia kampanii (poziom: kampanie)", "href": "#wynik"},
        {"tekst": "Kohorty: pacjenci tej kampanii według pierwszej usługi",
         "href": "#kohorty?okno=90&podz=usluga&f_kampania=gs_generic_specjalisci&wygl=28"}],
        "analiza/wyniki/c_priorytety.txt (P7), analiza/wyniki/a5e_kampanie.csv, analiza/wyniki/c_telemedigo.txt (3a), "
        "notatki/ZALOZENIA.md (punkt 42).",
        tabela={"tytul": "Kampania gs_generic_specjalisci: kwoty roczne z okresu 2",
                "kolumny": KOLUMNY_MACIERZY, "wiersze": tab4}, ex=ex)

    # 5. Obietnica L4 w Meta
    ex = Dodane()
    zw = V["zwroty_l4"]
    e2a = V["e2a"]
    pz = V["p11_zwroty"]
    k6 = lambda g: {k[len(f"p6_meta_l4_z1k_{g}_"):]: v for k, v in D.items() if k.startswith(f"p6_meta_l4_z1k_{g}_")}  # noqa: E731
    k6z, k6b = k6("z_kodem"), k6("bez_kodu")
    karta(5, "Uczciwa obietnica w reklamach L4 Meta i na stronie wejścia: mniej zwrotów po wizycie", [
        ("Z danych", [
            f"{proc(zw.loc['nowe_kampanie', 'proc_zwrot_po_wizycie'])} odbytych wizyt L4 pacjentów nowych kampanii kończy "
            f"się zwrotem po wizycie ({liczba(e2a[1])} z {liczba(e2a[0])}), wobec "
            f"{proc(zw.loc['pozostali', 'proc_zwrot_po_wizycie'])} L4 pozostałych pacjentów "
            f"({ex(liczba(zw.loc['pozostali', 'wizyty_odbyte']))} wizyt) w okresie 2.",
            "Kod rabatowy ani opóźnienie wizyty nie zmieniają tego odsetka. Za zwróconą wizytę lekarz dostaje wynagrodzenie.",
        ]),
        ("Ile warta po wstrzymaniu TikToka (tylko Meta)", [
            f"{zakres(pz[5] / 1000, pz[6] / 1000, 1)} tys. zł rocznie według przyjętej reguły i "
            f"{zakres(pz[7] / 1000, pz[8] / 1000, 1)} tys. zł według sesji płatności, na pełny rok (w "
            f"{ex(liczba(dni_me))} dniach działania: {ex(zakres(pz[0] / 1000, pz[1] / 1000, 1))} i "
            f"{ex(zakres(pz[2] / 1000, pz[3] / 1000, 1))} tys. zł).",
            "Wynik po 180 dniach jest taki sam, bo ci pacjenci prawie nie wracają. Jeśli test (pozycja 9) pokaże, że Meta "
            "trzeba wyłączyć, ta pozycja jest warta zero.",
        ]),
        ("Założenia i zastrzeżenia", [
            "Dolny wariant zakłada, że uczciwa reklama odstrasza tylko tych, którzy i tak dostaliby zwrot. W praktyce "
            "odstraszy też część pozostałych, więc może być niżej.",
            "Górny wariant („wizyta zostaje opłacona”) może wymagać zmiany zasad zwrotów, a nie samej treści reklamy. To "
            "osobna decyzja z ryzykiem prawnym i wizerunkowym.",
            f"{proc(zw.loc['pozostali', 'proc_zwrot_po_wizycie'])} to odsetek z innej grupy pacjentów, więc pełne "
            f"zrównanie jest optymistyczne. Rozsądny wariant bazowy to zmniejszenie luki o połowę.",
        ]),
        ("Co robimy", [
            "Najpierw jednodniowe sprawdzenie, co obiecują reklama, strona /zwolnienie-l4-online i regulamin przy odmowie L4.",
            "Potem nowa kreacja i pytanie przed płatnością („lekarz wystawia L4 tylko przy wskazaniach medycznych”).",
            "W Meta losowy podział ruchu na starą i nową kreację, z osobnym oznaczeniem kampanii.",
            f"Wysokość kodu rabatowego do przetestowania. Kod L4SZYBKO20 ({liczba(D['p6_kod_l4szybko20_znizka_zl'])} zł) jest "
            f"na {liczba(D['p6_kod_l4szybko20_zamowienia_okres2'])} z {liczba(k6z['pierwsze_zamowienia'] + k6b['pierwsze_zamowienia'])} "
            f"pierwszych zamówień pacjentów kampanii w okresie 2 (przyjęta reguła). Daje to "
            f"{tz(D['p6_kod_l4szybko20_znizka_efektywna_pelny_rok_zl'])} zniżki efektywnej na pełny rok (bez wizyt anulowanych "
            f"i zwróconych). Zwroty po wizycie przy pierwszym zamówieniu z kodem rabatowym i bez są prawie takie same "
            f"({proc(k6z['zwrot_po_wizycie_proc'])} z {liczba(k6z['pierwsze_zamowienia'])} wobec "
            f"{proc(k6b['zwrot_po_wizycie_proc'])} z {liczba(k6b['pierwsze_zamowienia'])} pierwszych zamówień), a powrót "
            f"w 90 dniach nie różni się istotnie ({proc(k6z['powrot90_proc'], 2)} z {liczba(k6z['pacjenci_90'])} wobec "
            f"{proc(k6b['powrot90_proc'], 2)} z {liczba(k6b['pacjenci_90'])} pacjentów). Progi rachunku (parametry "
            f"scenariusza, a nie odsetki z danych): rezygnacja z kodu opłaca się, jeśli ubędzie mniej niż "
            f"{proc(D['p6_meta_l4_z1k_bez_kodu_prog_utraty_pierwszych_zamowien_proc'])} zamówień z kodem, a przejście na stały "
            f"kod START10 ({liczba(V['start10'])} zł), jeśli mniej niż "
            f"{proc(D['p6_meta_l4_z1k_start10_zamiast_kodu_prog_utraty_pierwszych_zamowien_proc'])}. Reakcji pacjentów na niższy "
            f"kod nie znamy, więc to scenariusz do testu w losowym podziale ruchu, a nie kwota (niewiadoma 21).",
        ]),
        ("Po czym poznamy", [
            "Odsetek zwrotów po wizycie L4 przy nowej kreacji spada wobec starej, a marża na kliknięcie nie spada. Liczy "
            "się marża, nie sam odsetek zwrotów.",
        ]),
        ("Wdrożenie", ["1–2 tygodnie zmian i 4–6 tygodni pomiaru."]),
    ], [{"tekst": "Po zakupie: zwroty po wizycie według celu wizyty", "href": "#po-zakupie"},
        {"tekst": "Zdarzenie na osi: więcej pierwszych zamówień zwracanych po wizycie", "href": "#zdarzenia?z=zwroty_pierwsze"}],
        "analiza/wyniki/c_priorytety.txt (P2, P11), analiza/wyniki/a5e_scenariusze.txt (E2a), "
        "analiza/wyniki/a5r_po_zakupie.txt (2b, 2d), analiza/wyniki/d_kampanie.txt (6).", ex=ex)

    # 6. Poranna obsada
    ex = Dodane()
    rano = V["rano"]
    kol = "int_rano_ponad15_wszyscy"
    lis, gru, sty = "2025-11", "2025-12", "2026-01"
    od_lut = rano.loc["2026-02":"2026-09", kol]
    przed = rano.loc["2024-10":"2025-10", kol]
    oc = V["oceny"]
    oce = V["oceny_dokladne"]   # koszyk → (średnia ocena, liczba ocen), z danych zakładki „Po zakupie”
    dl = V["dlugosc"]
    rp = V["rano_powrot"]  # n_o1, n_o2, udzial_o1, udzial_o2, o1, o2
    mies_tekst = lambda m: f"{proc(rano.loc[m, kol])} w {MIESIACE_MSC[int(m[5:]) - 1]}"  # noqa: E731
    op = lambda k: D["op_internista_wszyscy_" + k]  # noqa: E731
    g610 = [op(f"godz{h:02d}_ponad15_proc_okres2") for h in range(6, 11)]
    poza, pol, noc = "poza_5_13_czyli_0_4_i_14_23_", "poludnie_bez_12_czyli_13_15_", "noc_bez_5_czyli_0_4_"
    waski = [D["poranek_waski_z1k_zl"], D["poranek_waski_z2_zl"]]
    szeroki = [D["poranek_szeroki_z1k_zl"], D["poranek_szeroki_z2_zl"]]
    karta(6, "Poranna obsada internistów: diagnoza, potem test", [
        ("Z danych", [
            f"Od listopada {lis[:4]} poranne opóźnienia u internisty rosną z miesiąca na miesiąc. Odsetek wizyt z terminem "
            f"6:00–11:59, które zaczynają się ponad 15 minut po terminie, wynosi {mies_tekst(lis)} {lis[:4]} "
            f"({ex(ile(rano.loc[lis, 'int_rano'], 'wizyta'))}), {mies_tekst(gru)} i {mies_tekst(sty)} {sty[:4]}, a od lutego "
            f"do września {sty[:4]} około połowy ({zakres(od_lut.min(), od_lut.max(), 1, '%')} miesięcznie). Od października "
            f"{przed.index[0][:4]} do października {przed.index[-1][:4]} było to {zakres(przed.min(), przed.max(), 1, '%')} "
            f"miesięcznie (wszyscy pacjenci).",
            f"Przy tym samym porannym ruchu opóźnień jest o {liczba(V['ruch'][0], 1)} punktu procentowego więcej "
            f"({ex(liczba(V['ruch'][1]))} przedziałów ruchu, {ex(liczba(V['ruch'][2]))} wizyt).",
            f"Długość porannej wizyty się nie zmieniła ({liczba(dl.loc[1].iloc[0], 1)} minuty w obu okresach), więc dłuższe "
            f"wizyty tego nie tłumaczą.",
            "Po godzinach (internista, wszyscy pacjenci): " + godziny_tekst(V, "c"),
            "W ciągu poranka: " + poranek_tekst(V, "c"),
            "Odczytanie, nie pomiar: to bardziej pasuje do stałego przesunięcia od początku dnia (późniejszy start względem "
            "grafiku, inna organizacja zapisów albo kolejki) niż do kolejki, która narasta, bo pacjentów jest więcej, niż "
            "lekarze zdążą przyjąć. Najwcześniejszy termin liczymy dla całej sieci, a nie dla pojedynczego lekarza. Bez "
            "identyfikatorów lekarzy i grafików mechanizmu nie rozstrzygamy.",
            f"Wizyty spóźnione ponad 30 minut mają średnią ocenę {liczba(oce['d_ponad_30_min'][0], 2)} wobec "
            f"{liczba(oce['a_do_5_min'][0], 2)} przy punktualnych (okres 2, internista, pacjenci spoza nowych kampanii, "
            f"{liczba(oce['d_ponad_30_min'][1])} i {liczba(oce['a_do_5_min'][1])} ocen). Rano spada "
            f"powrót po wizytach spóźnionych.",
        ]),
        ("Dlaczego wysoko", [
            "To jedna z konkretnych hipotez poprawy retencji pacjentów z kanałów działających w obu latach (obok "
            "komunikacji po wizycie i zniżek), a pierwszy krok, diagnoza, jest tani.",
        ]),
        ("Ile warta", [
            f"Scenariusz od 0 zł do {tz(V['p8'][3])} marży rocznie w horyzoncie 180 dni.",
            f"Wariant wąski, czyli sama zmiana rozkładu opóźnień pierwszej wizyty, to {zakres(min(waski) / 1000, max(waski) / 1000, 1)} "
            f"tys. zł zależnie od reguły źródła; prawie cały przypada na poranne pierwsze wizyty u internisty "
            f"({tz(D['poranek_najwezszy_z1k_zl'])}). Wariant szeroki ({zakres(min(szeroki) / 1000, max(szeroki) / 1000, 1)} tys. zł) "
            f"przypisuje opóźnieniom cały spadek powrotu w starych kampaniach, więc nie jest górną granicą skutku obsady.",
            "Związek opóźnień z powrotami może częściowo wynikać z tego, kto przychodzi rano, więc kwota jest niepewna. "
            "Kosztu dodatkowej obsady nie ma w danych.",
        ]),
        ("Co robimy", [
            f"Diagnoza: grafiki i obsada poranna przed i po {data(V['start'][me])}, obciążenie lekarzy pacjentami spoza "
            f"B2C, rozmowa z osobami od grafików.",
            "Potem naprawy, także bez dodatkowej obsady: liczba porannych terminów dopasowana do przepustowości, "
            "przesunięcie godzin lekarzy, realny czas oczekiwania pokazany pacjentowi.",
            "Na końcu test w losowo wybrane dni.",
        ]),
        ("Po czym poznamy", [
            f"Odsetek porannych wizyt spóźnionych ponad 15 minut spada z około 50% poniżej 10%, oceny porannych wizyt "
            f"rosną, a powrót w 90 dniach pacjentów z pierwszą wizytą rano, z tego samego źródła, wraca w stronę "
            f"{int(rp[4])}–{int(rp[4]) + 1}% (w okresie 1: {ex(proc(rp[4]))}, {ex(liczba(rp[0]))} pacjentów kampanii "
            f"działających w obu latach).",
        ]),
        ("Wdrożenie", ["Diagnoza 1–2 dni, test 2–4 tygodnie, efekt w powrotach po 90 dniach."]),
    ], [{"tekst": "Po zakupie: punktualność według pory i opóźnienia przy tym samym ruchu", "href": "#po-zakupie"},
        {"tekst": "Zdarzenie na osi: poranne opóźnienia u internisty", "href": "#zdarzenia?z=opoznienia_rano"}],
        "analiza/wyniki/a5r_punktualnosc.txt (1c, 2b, 3f), analiza/wyniki/a5r_po_zakupie.txt (3a), "
        "analiza/wyniki/c_priorytety.txt (P8, P13), analiza/wyniki/d_retencja.txt (1, 2), analiza/wyniki/d_wynik.txt (4), "
        "notatki/a5_retencja.md.", ex=ex)

    # 7. Komunikacja po wizycie
    ex = Dodane()
    crm = V["crm"].dropna(subset=["wejscia_na_1000_pacjentow"])
    c1 = crm[crm["miesiac"] < "2025-10"]["wejscia_na_1000_pacjentow"]
    c2 = crm[crm["miesiac"] >= "2025-10"]["wejscia_na_1000_pacjentow"]
    B1, W = V["pow_bez_z1k"], V["pow_wszyscy"]
    cp = V["crm_powrot"]   # po CRM okres 1, okres 2, bez CRM okres 1, okres 2 (%)
    kc = V["crm_kontakt"]
    kc = kc[kc["grupa2"] == "pozostale"].set_index("okres")
    karta(7, "Komunikacja po wizycie z losową grupą kontrolną (retencja)", [
        ("Z danych", [
            f"Retencja to połowa definicji wzrostu, a spada także bez pacjentów nowych kampanii: powrót w 90 dniach "
            f"{proc(B1['p90_o2'])} ({ex(liczba(B1['n90_o2']))} pacjentów) wobec {proc(W['p90_o1'])} "
            f"({ex(liczba(W['n90_o1']))}).",
            f"Po wejściu z newslettera albo SMS-a wraca w okresie 2 {proc(cp[1], 2)} pacjentów spoza nowych kampanii, a bez "
            f"takiego wejścia {proc(cp[3], 2)}, więc to około {proc(100 * cp[1] / (cp[1] + cp[3]), 0)} obserwowanych "
            f"pierwszych powrotów ({ex(liczba(kc.loc[2, 'n']))} pacjentów kampanii działających w obu latach).",
            f"Liczba wejść z newslettera i SMS-ów na 1 000 pacjentów spada z {zakres(c1.min(), c1.max())} miesięcznie "
            f"w okresie 1 do {zakres(c2.min(), c2.max())} w okresie 2, ale mianownikiem jest cała narastająca baza "
            f"pacjentów; w pierwszych 90 dniach od zakupu odsetek pacjentów z takim wejściem rośnie lekko z "
            f"{proc(kc.loc[1, 'kontakt_crm'])} do {proc(kc.loc[2, 'kontakt_crm'])}. Widać kliknięcia, a nie wysyłki.",
        ]),
        ("Ile warta", [
            f"Scenariusz: każdy punkt procentowy powrotu w 90 dniach to około {tz(V['p12'][1])} marży rocznie "
            f"({liczba(V['nowi'][2])} nowych pacjentów × 1% × {liczba(V['p12'][0], 1)} zł), a bez pacjentów nowych kampanii "
            f"{tz(V['p12_bez'][1])}. To różnica obserwacyjna, a nie zmierzony efekt wiadomości.",
        ]),
        ("Co robimy", [
            "Dane o wysyłkach: ile, komu, kiedy.",
            "Sekwencja po pierwszej wizycie (przypomnienie o kontynuacji leczenia, recepta, kontrola), zawsze z losową grupą "
            "kontrolną bez wysyłki.",
        ]),
        ("Po czym poznamy", ["Różnica powrotu w 90 dniach i marży między grupą z wysyłką a grupą kontrolną."]),
        ("Wdrożenie", ["Dane o wysyłkach kilka dni, sekwencja 2–4 tygodnie, pomiar 90 dni."]),
    ], [{"tekst": "Kohorty: powrót bez pacjentów nowych kampanii", "href": "#kohorty?okno=90&f_grupa=pozostale&wygl=28"},
        {"tekst": "Kohorty: powrót według źródła pozyskania", "href": "#kohorty?okno=90&podz=kanal&wygl=28"}],
        "analiza/wyniki/c_priorytety.txt (W2, P12), analiza/wyniki/a5r_po_zakupie.txt (5e), notatki/a5_retencja.md (krok 4c).",
        ex=ex)

    # 8. Zalogowani od wejścia
    ex = Dodane()
    p5 = V["p5"]
    karta(8, "Sprawdzić ręcznie zakup dla pacjentów zalogowanych od wejścia", [
        ("Z danych", [
            f"{liczba(V['zal_sesje'])} sesji zalogowanych od wejścia przez dwa lata nie kończy się ani razu zakupem "
            f"konsultacji, a każdy z {liczba(V['zal_powt'])} zakupów powtórnych ma krok logowania.",
            "Dane nie rozstrzygają między odczytaniami: (A) wizyty „sprawdzam konto” albo sposób zapisu (logowanie zaczyna "
            "nową sesję) albo (B) zepsuta ścieżka zakupu dla zalogowanych. Kilka faktów przemawia za A.",
        ]),
        ("Ile warta", [
            f"W odczytaniu A 0 zł dla przychodu (ale wtedy cierpi pomiar lejka, pozycja 2). W odczytaniu B scenariusze: "
            f"około {t1(p5[0], 0)} tys. zł rocznie na sesjach, około {t1(p5[1], 0)} tys. zł na pacjentach, wysoki scenariusz "
            f"{t1(p5[2], 0)} tys. zł.",
        ]),
        ("Po czym poznamy", [
            "Test daje odpowiedź od razu. Jeśli ścieżka jest zepsuta, po naprawie sesje zalogowane od wejścia zaczynają "
            "kończyć się płatnością.",
        ]),
        ("Wdrożenie", ["1 dzień, w pierwszym tygodniu niezależnie od miejsca na liście."]),
    ], [{"tekst": "Lejek: sesje zalogowane od wejścia", "href": "#lejek?typ=zalogowana_od_wejscia&podz=calosc&krok=k1"}],
        "analiza/wyniki/c_priorytety.txt (P5), analiza/wyniki/a5p_zalogowane.txt, notatki/a5_pozyskanie.md (sekcja 3).", ex=ex)

    # 9. Meta: test dodatkowości
    ex = Dodane()
    p4, pm_ = V["p4_cp"], V["p11_meta"]
    wyl0 = wyl(me, "Z1K", 0)
    prog = 100 * wyl0 / (wyl0 + p4[0])
    prog180 = 100 * wyl0 / (wyl0 + p4[2])
    mp = lambda k: D["meta_prog_proc_z1k_" + k]  # noqa: E731
    karta(9, "Meta na L4: test dodatkowości w parach województw, z progiem decyzji", [
        ("Z danych", [
            f"Wynik kampanii zależy od reguły źródła: {tzn(p4[0])} według przyjętej reguły i {tz(p4[1])} według sesji "
            f"płatności po 90 dniach, w {liczba(dni_me)} dniach działania ({zn(pm_[0] / 1000)} i {tz(pm_[1])} na pełny rok).",
            "Dane nie rozstrzygają, ilu jej pacjentów przyszłoby i bez niej.",
        ]),
        ("Naprawić albo wyłączyć", [
            "Naprawić zwroty: pozycja 5, w tej samej kampanii.",
            f"Wyłączyć: od {tz(pm_[2])} (wszyscy pacjenci dodatkowi, horyzont 90 dni) albo {tz(V['p11_180'][4])} (180 dni) "
            f"do {tzn(pm_[3])} (żaden) na pełny rok.",
        ]),
        ("Próg decyzji, ustalony przed testem", [
            f"Według przyjętej reguły wyłączenie traci pieniądze tylko wtedy, gdy ponad około {proc(prog, 0)} pacjentów "
            f"kampanii jest dodatkowych: {proc(prog)} w horyzoncie 90 dni i {proc(prog180)} w horyzoncie 180 dni. Według "
            f"sesji płatności wyłączenie zyskuje zawsze.",
            f"Próg po naprawie zwrotów: {proc(mp('90_dni_po_naprawie_a'))} (90 dni) i {proc(mp('180_dni_po_naprawie_a'))} "
            f"(180 dni) w wariancie A, {proc(mp('90_dni_po_naprawie_b'))} i {proc(mp('180_dni_po_naprawie_b'))} w wariancie B. "
            f"Po naprawie kampania zarabia więcej na każdym pacjencie, więc opłaca się przy niższej dodatkowości. W tempie "
            f"ostatniego półrocza próg dziś rośnie do {proc(D['p3_meta_l4_z1k_prog_decyzji_90_proc_pelny_rok_tempo_polrocza'])}.",
            f"W liczbie pacjentów próg prawie nie zależy od reguły źródła: wyłączenie opłaca się, jeśli po nim ubędzie mniej "
            f"niż około {liczba(dziesiatki(V['prog_pac']['dziś']))} nowych pacjentów w {liczba(dni_me)} dniach działania "
            f"kampanii w okresie 2 (dziś, horyzont 90 dni; według sesji płatności około "
            f"{liczba(dziesiatki(V['prog_pac_z2']))}) albo {liczba(dziesiatki(V['prog_pac']['po naprawie zwrotów A']))} (po "
            f"naprawie zwrotów A). Reguła zmienia głównie to, ilu pacjentów przypisujemy kampanii.",
        ]),
        ("Czego ten test nie rozstrzygnie", [
            f"Test w {int(V['test_wojewodztwa'])} parach województw przez 4–6 tygodni nie da mocy potrzebnej do odróżnienia "
            f"wyniku od progu. W połowie kraju kampania przypisuje około {liczba(D['test_tempo_q3_meta_z1k_dziennie'] * 7 / 2, 1)} "
            f"nowego pacjenta tygodniowo (tempo {kw_q3}, przyjęta reguła), a losowy rozrzut liczby nowych pacjentów "
            f"w województwach jest duży.",
            f"Błąd oszacowania udziału dodatkowych wynosi {liczba(D['test_blad_udzialu_proc_4_tyg_z1k'], 1)} punktu "
            f"procentowego po 4 tygodniach i {liczba(D['test_blad_udzialu_proc_6_tyg_z1k'], 1)} po 6, a najmniejszy wykrywalny "
            f"efekt to {liczba(D['test_mde_proc_4_tyg_z1k'])} i {liczba(D['test_mde_proc_6_tyg_z1k'])} punktów. Test nie "
            f"odróżni więc ani 100% od 85%, ani 85% od 70%: gdy naprawdę wszyscy pacjenci są dodatkowi, orientacyjnie co "
            f"czwarty test ({zakres(D['test_P_ponizej_progu_gdy_100_proc_6_tyg'], D['test_P_ponizej_progu_gdy_100_proc_4_tyg'], 0, '%')}) "
            f"pokaże wynik poniżej progu. Dłuższy test wymaga osobnego przeliczenia, bo szum okresu odniesienia nie maleje "
            f"z długością testu.",
            "Rozrzut jest prawie czysto losowy, więc sam dobór par prawdopodobnie nie wystarczy. Test może za to wykryć dużą "
            "różnicę, na przykład gdy większość pacjentów przyszłaby i bez kampanii. Pary i sposób liczenia ustalamy przed "
            "testem, na danych sprzed testu.",
            "To ocena orientacyjna: testy pozorne na danych okresu 2, przy założeniach modelu.",
        ]),
        ("Reguła na wynik niejednoznaczny, ustalona z góry", [
            "Decyduje oszacowanie punktowe. Poniżej progu wyłączamy, powyżej zostawiamy.",
            "To świadomie przyjęta reguła decyzji przy dużej niepewności, a nie rozstrzygnięcie statystyczne. Obie decyzje są "
            "odwracalne, a pomiar warto powtórzyć w innym sezonie.",
            "Inne warianty (bez zmian, gdy przedział obejmuje próg; połowa budżetu; przedłużanie testu z punktami kontrolnymi "
            "co 2 tygodnie; decyzja według oczekiwanej marży, która wymaga osobnego modelu) opisuje raport "
            "analiza/wyniki/d_wynik.txt, punkt 3e.",
        ]),
        ("Projekt testu", [
            f"Na 4–6 tygodni wyłączyć kampanię w połowie województw, łącząc je w pary podobne wielkością i trendem i losując "
            f"w parach. Udział nowych kampanii jest podobny we wszystkich województwach "
            f"({zakres(D['demo_wojewodztwa_z1k_udzial_nowych_min_proc'], D['demo_wojewodztwa_z1k_udzial_nowych_max_proc'], 1, '%')} "
            f"nowych pacjentów okresu 2), co ułatwia dobór par.",
            "Wskaźnik główny: wszyscy nowi pacjenci i marża w województwie, a nie pacjenci przypisani Meta.",
            "Budżetu z wyłączonych województw nie przesuwać.",
            "Przy okazji mierzyć poranne opóźnienia u internisty (pozycja 6).",
            "Ryzyko: obsada lekarzy jest wspólna dla całego kraju. Wyłączenie zmniejsza obciążenie internistów, więc "
            "w województwach kontrolnych może przybyć wolnych terminów, zakupów i powrotów. Zawyża to spadek (więcej "
            "„dodatkowych”), a efekt w retencji przenosi się na województwa kontrolne. Do tego województwo konta to nie "
            "miejsce wyświetlenia reklamy, więc część reklam przecieka między województwami.",
            f"Koszt testu, jeśli wszyscy pacjenci są dodatkowi (przyjęta reguła): najwyżej około "
            f"{zakres(V['p11_test'][0] * 4 / 6 / 1000, V['p11_test'][1] * 4 / 6 / 1000, 1)} tys. zł utraconej marży przy "
            f"4 tygodniach i {zakres(V['p11_test'][0] / 1000, V['p11_test'][1] / 1000, 1)} tys. zł przy 6 tygodniach; po "
            f"naprawie zwrotów A {t1(D['test_koszt_4_tyg_z1k_tempo_q3_po_naprawie_a'])} i "
            f"{tz(D['test_koszt_6_tyg_z1k_tempo_q3_po_naprawie_a'])} (tempo {kw_q3}). Według sesji płatności test daje zysk. "
            f"Uzupełnienie: badanie przyrostu konwersji w panelu Meta.",
        ]),
        ("Po czym poznamy", [
            "Spadek wszystkich nowych pacjentów w województwach bez reklamy wobec par, w liczbie pacjentów i jako udział "
            "pacjentów przypisanych Meta; decyzja według reguły wyżej.",
        ]),
        ("Wdrożenie", ["Tydzień przygotowania i 4–6 tygodni testu. Test rusza w drugim tygodniu, równolegle z diagnozą "
                       "poranka (pozycja 6), bo oba można prowadzić w tych samych województwach. Wynik może się nie przenieść "
                       "z jesieni na lato."]),
    ], [{"tekst": "Wynik biznesu: ekonomia kampanii, obie reguły", "href": "#wynik"},
        {"tekst": "Kohorty: nowe kampanie na L4 i pozostałe", "href": "#kohorty?okno=90&podz=grupa&wygl=28"},
        {"tekst": "Zdarzenie na osi: start kampanii Meta na L4", "href": "#zdarzenia?z=start_meta_l4"}],
        "analiza/wyniki/c_priorytety.txt (P4, P11), analiza/wyniki/a5e_scenariusze.txt (E1, E3, E3b), "
        "analiza/wyniki/d_wynik.txt (3a–3e), analiza/wyniki/d_kampanie.txt (3), analiza/wyniki/d_retencja.txt (5), "
        "notatki/a5_ekonomia.md.",
        tabela={"tytul": f"Kampania Meta na L4: kwoty z {liczba(dni_me)} dni działania, pod spodem pełny rok "
                         f"(×{liczba(mn_me, 2)})", "kolumny": KOLUMNY_MACIERZY, "wiersze": macierz(V, me, mn_me)},
        ex=ex)

    # 10. Cennik specjalistów i TelemediGO
    ex = Dodane()
    p6 = V["p6"]
    sc = V["p6_scen"]
    tab10 = []
    for sp in ce.index:
        r = ce.loc[sp]
        tab10.append({"opis": sp, "komorki": [
            {"w": zl(r["cena"]), "minus": False}, {"w": liczba(r["cena_z_go"], 1) + " zł", "minus": False},
            {"w": zl(r["koszt_lekarza"]), "minus": False},
            {"w": zn(r["marza_bez_znizki"]) + " zł", "minus": r["marza_bez_znizki"] < 0},
            {"w": zn(r["marza_z_go"]) + " zł", "minus": r["marza_z_go"] < 0}]})
    karta(10, "Cennik specjalistów i warunki TelemediGO u specjalistów", [
        ("Z danych", [
            f"Po cenie katalogowej wizyta zostawia ponad koszt lekarza tylko {liczba(ce.loc['kardiolog', 'marza_bez_znizki'])} zł "
            f"(dermatolog, kardiolog, neurolog, urolog: {liczba(ce.loc['kardiolog', 'cena'])} zł) albo "
            f"{liczba(ce.loc['ginekolog', 'marza_bez_znizki'])} zł (endokrynolog, ginekolog: {liczba(ce.loc['ginekolog', 'cena'])} zł).",
            f"Pediatra ({liczba(ce.loc['pediatra', 'cena'])} zł) i psycholog ({liczba(ce.loc['psycholog', 'cena'])} zł) mają "
            f"cenę niższą niż koszt lekarza {liczba(ce.loc['pediatra', 'koszt_lekarza'])} zł (przy przyjętym koszcie pediatry "
            f"jak u specjalisty).",
            f"Po zniżce TelemediGO {ZNIZKA_SPEC}% cena jest niższa niż koszt lekarza u wszystkich specjalistów poza "
            f"psychiatrą. W okresie 2 te wizyty przyniosły {tz(-p6.loc[2, 'marza'])} straty na {liczba(p6.loc[2, 'zamowienia'])} "
            f"zamówieniach.",
            "To wspólna przyczyna strat w TelemediGO u specjalistów i w kampanii na specjalistów (pozycja 4).",
        ]),
        ("Ile warta", [
            f"Warunki TelemediGO: scenariusze {t1(sc[0])} / {t1(sc[1])} / {tz(sc[2])} rocznie (znikają wszystkie te wizyty "
            f"/ tylko te ze stratą / wszystkie zostają po cenie katalogowej). {tz(sc[2])} to scenariusz, a nie górna "
            f"granica: przy osobnej reakcji przy każdym zamówieniu wynik mieści się między {t1(V['p6_reakcja'][0])} a "
            f"{tz(V['p6_reakcja'][1])}. Wszystkie pomijają zmianę sprzedaży członkostw.",
            "Założenie planistyczne (bez osobnego rachunku): w pierwszym roku efekt to około połowa, bo obecni członkowie "
            "mają stare warunki do końca ważności.",
            f"Cennik: każde 10 zł podwyżki przy tej samej liczbie wizyt to do {tz(V['p14_zl'])} rocznie "
            f"({liczba(V['p14'][1])} opłacone wizyty w okresie 2), a przy utrzymaniu zniżki TelemediGO {ZNIZKA_SPEC}% na "
            f"{liczba(V['p14_go'][0])} z nich {tz(V['p14_go'][1])}. To górna granica, bo nie znamy reakcji pacjentów na cenę.",
        ]),
        ("Warianty", [
            f"Zniżka u specjalistów ustawiona tak, żeby cena nie spadała poniżej kosztu lekarza (najwyżej około "
            f"{proc(100 * ce.loc['kardiolog', 'marza_bez_znizki'] / ce.loc['kardiolog', 'cena'], 0)} przy "
            f"{liczba(ce.loc['kardiolog', 'cena'])} zł, bez zniżki u pediatry i psychologa).",
            "Test dwóch cen dla nowych pacjentów przez 4 tygodnie, mierzony marżą na sesję, a nie odsetkiem kupujących.",
        ]),
        ("Po czym poznamy", [
            "Marża wizyt u specjalistów (z członkami i bez) jest nieujemna, a sprzedaż TelemediGO nie spada bardziej niż "
            "ustalony z góry próg.",
        ]),
        ("Wdrożenie", ["Zmiana regulaminu i kasy 1–2 tygodnie; test cen 4 tygodnie."]),
    ], [{"tekst": "Kohorty: powrót i marża według pierwszej usługi", "href": "#kohorty?okno=90&podz=usluga&wygl=28"},
        {"tekst": "Kohorty: kupujący TelemediGO przy pierwszym zakupie", "href": "#kohorty?okno=90&podz=go0&wygl=28"}],
        "analiza/wyniki/c_telemedigo.txt (3a–3c), analiza/wyniki/c_priorytety.txt (P6, P14), notatki/ZALOZENIA.md (punkt 33).",
        tabela={"tytul": "Cennik z danych: marża na wizycie odbytej, bez zniżki i ze zniżką TelemediGO",
                "kolumny": ["Cena katalogowa", "Cena po zniżce TelemediGO", "Koszt lekarza", "Marża bez zniżki", "Marża ze zniżką"],
                "wiersze": tab10}, ex=ex)

    # 11. Kliknięcia a sesje
    ex = Dodane()
    kl = V["klik"]["sesje_na_klik"]
    g_ = kl[[k for k in kl.index if k.startswith("gs_")]]
    m_ = kl[[k for k in kl.index if k.startswith("meta_")]]
    karta(11, "Sprawdzić stratę między kliknięciem reklamy a sesją w Meta i TikToku", [
        ("Z danych", [
            f"Na kliknięcie przypada {zakres(g_.min(), g_.max(), 2)} sesji w Google Ads, {zakres(m_.min(), m_.max(), 2)} "
            f"w Meta i {liczba(kl[tt], 2)} w TikToku, stale w każdym kwartale.",
        ]),
        ("Ile warta", [
            "0 zł, jeśli plik wydatków liczy wszystkie kliknięcia (także te, które nie prowadzą na stronę).",
            f"Jeśli ludzie porzucają stronę, zanim się załaduje, i da się to odzyskać: do {t1(V['p9_zl'], 0)} tys. zł rocznie "
            f"(górna granica: {ex(liczba(V['p9'][0]))} brakujących sesji i do {ex(liczba(V['p9'][1]))} zamówień w okresie 2). "
            f"Po wstrzymaniu TikToka mniej. Realnie raczej ułamek, bo porzucający są mniej zdecydowani.",
        ]),
        ("Po czym poznamy", [
            "W panelach porównać kliknięcia w link i wyświetlenia strony docelowej z sesjami, dzień po dniu; czas ładowania "
            "w przeglądarkach wbudowanych. Wynik zmienia ocenę pozycji 3 i 9.",
        ]),
        ("Wdrożenie", ["1–2 dni, w pierwszym tygodniu."]),
    ], [{"tekst": "Lejek: sesje kampanii Meta i TikToka dzień po dniu",
         "href": "#lejek?typ=zwykla&pac=wszyscy&podz=kampania&krok=sesje&w=meta_prosp_l4_szybko,tt_prosp_l4_15min,meta_prosp_lekarz_online"}],
        "analiza/wyniki/a2_jakosc.txt (3c), analiza/wyniki/c_priorytety.txt (P9), analiza/wyniki/a5p_lejek.txt (6b), "
        "notatki/a5_pozyskanie.md (sekcja 5).", ex=ex)

    # 12. Test TelemediGO
    ex = Dodane()
    od = V["odnowienia"]
    g4 = V["go_4a"]   # kupujacy, pokrycie, a, b, a_dop, b_dop
    karta(12, "Test TelemediGO z losowym, bezpłatnym dostępem do zniżek", [
        ("Z danych", [
            f"Nie wiemy, czy TelemediGO podnosi powroty, czy tylko przyciąga pacjentów, którzy i tak wracają. Kupujący "
            f"przy pierwszym zamówieniu wracają w 90 dniach w {ex(proc(g4[4]))} wobec {ex(proc(g4[5]))} podobnych pacjentów "
            f"(okres 2, {ex(liczba(g4[0]))} kupujących), ale ta różnica łączy wpływ zniżki i to, kto kupuje.",
            f"Zniżki przewyższają opłatę średnio o {liczba(abs(V['go_bilans']), 1)} zł na członkostwo (członkostwa z okresu {ex("1")}, "
            f"przy założeniu, że te same wizyty odbyłyby się i bez TelemediGO), więc program opłaca się tylko wtedy, gdy "
            f"dokłada wizyt.",
        ]),
        ("Ile warta", [
            f"Decyduje, czy program promować (sprzedaż, przypomnienie o odnowieniu; dziś odnawia około {proc(od[2], 0)} "
            f"członków: {ex(liczba(od[1]))} z {ex(liczba(od[0]))} w 90 dniach po wygaśnięciu), czy przebudować razem "
            f"z pozycją 10.",
            f"Dodatkowy koszt testu to około {zakres(V['p10'][0] / 1000, V['p10'][1] / 1000, 1)} tys. zł zniżek.",
        ]),
        ("Zastrzeżenie", [
            f"Darmowy dostęp mierzy wpływ zniżki, a nie opłacalność oferty za {OPLATA_GO} zł. Losowanie samej oferty przy "
            f"kasie mierzyłoby decyzję biznesową, ale przy {proc(V['go_kupujacy'], 1)} kupujących potrzebuje ponad "
            f"{int(V['go_miesiace_A'] // 12)} lat pozyskania. Wskaźnikiem głównym jest marża na pacjenta.",
        ]),
        ("Po czym poznamy", ["Różnica powrotu w 90 dniach i marży między grupą z dostępem a grupą bez niego."]),
        ("Wdrożenie", [
            f"2–8 tygodni na losowe przydzielenie ({liczba(V['p10_n'][0])}–{liczba(V['p10_n'][1])} pacjentów na grupę, czyli "
            f"do około {liczba(V['go_miesiace_B'], 1)} miesiąca pozyskania), potem 90 dni obserwacji.",
            "Liczebność wyznaczyliśmy dla różnicy powrotu; przed startem trzeba ustalić najmniejszą istotną biznesowo "
            "zmianę marży i sprawdzić, jakiej próby wymaga.",
        ]),
    ], [{"tekst": "Kohorty: kupujący TelemediGO przy pierwszym zakupie i pozostali", "href": "#kohorty?okno=90&podz=go0&wygl=28"}],
        "analiza/wyniki/c_telemedigo.txt (1d, 2a, 4a, 4d), analiza/wyniki/c_priorytety.txt (P10).", ex=ex)

    # przegląd (tabela na górze)
    p2pom = V["testy_koszt2"]
    pol_do = O2[1]
    pol_od = pol_do - dt.timedelta(days=int(D["p3_meta_l4_z1k_dni_polrocza"]) - 1)
    tempo = lambda k, m: 100 * (D[f"p3_{k}_l4_z1k_{m}_polrocze" + ("_zl" if m.startswith("wydatki") else "")]  # noqa: E731
                                / D[f"p3_{k}_l4_z1k_{m}_caly" + ("_zl" if m.startswith("wydatki") else "")] - 1)
    przeglad = [
        (1, "Naprawić zakładanie konta w Safari na iOS",
         f"{zakres(lo[3] / 1000, hi[3] / 1000)} tys. zł (90 dni), {zakres(lo[4] / 1000, hi[4] / 1000)} tys. zł (180 dni); górna granica",
         "wysoka: awaria widoczna w danych"),
        (2, "Naprawić pomiar: raport bez duplikatów i kont testowych, przychód po zwrotach, zamknąć testy TEST-QA, "
            "wynagrodzenie lekarzy za testy, alarmy na lejku i zwrotach",
         f"0 albo {t1(p2pom, 0)} tys. zł bezpośrednio; pośrednio warunek pozostałych decyzji", "wysoka: oba błędy widoczne w danych"),
        (3, "Wstrzymać TikToka na L4",
         f"przy 100% pacjentów dodatkowych, pełny rok: {zn(V['p11_tt'][2] / 1000)} do {zn(V['p11_tt'][3] / 1000)} tys. zł "
         f"(90 dni), {zn(V['p11_180'][0] / 1000)} do {zn(V['p11_180'][1] / 1000)} tys. zł (180 dni); więcej przy mniejszej "
         f"dodatkowości", "wysoka co do znaku: wynik ujemny w obu regułach po 90 dniach i, w przybliżeniu dla całego "
                          "rocznika, po 180 dniach"),
        (4, "Wstrzymać gs_generic_specjalisci (Google Ads na specjalistów) do czasu zmiany cennika",
         f"{zn(min(wyl100) / 1000)} do {tzn(max(wyl100))} przy 100% pacjentów dodatkowych, do {tzn(p7[('Z1K', '90')][7])}",
         "wysoka co do znaku"),
        (5, "Uczciwa obietnica w reklamach L4 Meta (test dwóch kreacji)",
         f"{zakres(pz[5] / 1000, pz[6] / 1000, 1)} tys. zł (przyjęta reguła), {zakres(pz[7] / 1000, pz[8] / 1000, 1)} tys. zł "
         f"(sesja płatności), pełny rok", "średnia: nie znamy powodu zwrotów"),
        (6, "Poranna obsada internistów: diagnoza, potem test",
         f"scenariusz od 0 do {t1(V['p8'][3], 0)} tys. zł; wariant wąski około {t1(sum(waski) / 2, 0)} tys. zł; koszt "
         f"obsady nieznany", "niska co do kwoty"),
        (7, "Komunikacja po wizycie z losową grupą kontrolną (retencja)",
         f"scenariusz: {tz(V['p12'][1])} za każdy punkt procentowy powrotu w 90 dniach", "niska co do kwoty"),
        (8, "Sprawdzić ręcznie zakup dla zalogowanych pacjentów",
         f"0 albo {t1(p5[1], 0)}–{t1(p5[0], 0)} tys. zł (wysoki scenariusz {t1(p5[2], 0)} tys. zł)",
         "niska: dane wskazują raczej na 0 zł"),
        (9, f"Test dodatkowości Meta na L4 w parach województw, z progiem decyzji około {proc(prog, 0)} (po naprawie "
            f"zwrotów około {proc(mp('90_dni_po_naprawie_a'), 0)})",
         f"decyzja warta od {t1(pm_[2])} (90 dni) albo {t1(V['p11_180'][4])} (180 dni) do {tzn(pm_[3])}, pełny rok",
         "— (to jest test; w 4–6 tygodni nie odróżni wyniku od progu, więc decyduje reguła ustalona z góry)"),
        (10, "Cennik specjalistów i warunki TelemediGO u specjalistów",
         f"TelemediGO: scenariusze {zakres(sc[0] / 1000, sc[2] / 1000)} tys. zł po pełnym roku (w pierwszym około połowa); "
         f"cennik: do {tz(V['p14_zl'])} za każde 10 zł podwyżki przy tej samej liczbie wizyt (górna granica)",
         "wysoka co do kierunku, niska co do kwoty cennika"),
        (11, "Sprawdzić stratę między kliknięciem a sesją w Meta i TikToku",
         f"0 albo do {t1(V['p9_zl'], 0)} tys. zł (górna granica, po wstrzymaniu TikToka mniej)", "niska"),
        (12, "Test TelemediGO z losowym, bezpłatnym dostępem do zniżek",
         f"decyduje o roli programu; koszt testu {zakres(V['p10'][0] / 1000, V['p10'][1] / 1000)} tys. zł", "— (to jest test)"),
    ]
    przeglad = [{"nr": n, "co": c, "ile": i, "pewnosc": p, "wdrozenie": SZACUNEK[n]} for n, c, i, p in przeglad]

    zasady = [
        f"Wartość to zmiana marży na rok. Rokiem bazowym jest okres 2. Marża = przychód z konsultacji po zwrotach "
        f"+ TelemediGO − koszt lekarza − wydatki na kampanie − prowizja afiliacyjna.",
        f"Przy kampaniach podajemy wynik po 90 i po 180 dniach od pozyskania oraz według obu reguł źródła. Kwoty kampanii, "
        f"które działały krócej niż rok, przeliczamy na pełny rok przy tym samym tempie: TikTok działał w okresie 2 przez "
        f"{liczba(dni_tt)} dni (mnożnik {liczba(mn_tt, 2)}), Meta na L4 przez {liczba(dni_me)} dni ({liczba(mn_me, 2)}).",
        f"Tempo ostatniego półrocza: od {pol_od.day}.{pol_od:%m} do {data(pol_do)} obie kampanie wydają dziennie więcej niż "
        f"średnio (Meta na L4 o {proc(tempo('meta', 'wydatki_dziennie'))}, TikTok o {proc(tempo('tiktok', 'wydatki_dziennie'))}), "
        f"a nowych pacjentów przybywa dziennie tylko o {proc(tempo('meta', 'nowi_dziennie'))} i "
        f"{proc(tempo('tiktok', 'nowi_dziennie'))} więcej. W tym tempie wynik kampanii jest gorszy niż w przeliczeniu ze "
        f"średniej: Meta na L4 {zn(D['p3_meta_l4_z1k_wynik_dzis_90_pelny_rok_tempo_polrocza'] / 1000)} zamiast "
        f"{zn(D['p3_meta_l4_z1k_wynik_dzis_90_pelny_rok_p11'] / 1000)} tys. zł rocznie, TikTok "
        f"{t1(D['p3_tiktok_l4_z1k_wynik_dzis_90_pelny_rok_tempo_polrocza'])} zamiast "
        f"{tz(D['p3_tiktok_l4_z1k_wynik_dzis_90_pelny_rok_p11'])} (przyjęta reguła, 90 dni). Kierunek żadnej decyzji się "
        f"nie zmienia.",
        "Każda kwota to osobny scenariusz liczony względem tego, co działo się w okresie 2, a nie wynik po kolei wdrożonych "
        "wcześniejszych pozycji. Jedyny wyjątek: naprawę obietnicy L4 (pozycja 5) wyceniamy tylko dla Meta, bo zakładamy "
        "wstrzymanie TikToka (pozycja 3). Kwot nie sumujemy: mają różne horyzonty i nakładają się na siebie.",
        "Kolejność to waga, a nie kalendarz. Najpierw pewne straty, które rosną każdego dnia i łatwo je naprawić (pozycje 1 "
        "i 2). Potem pauzy, które da się cofnąć (3 i 4). Potem naprawy, diagnozy, testy i sprawdzenia (5–10). Na końcu "
        "rzeczy o nieznanym znaku albo nieznanej wartości (11 i 12). Pozycje 1, 3, 4 i krótkie sprawdzenia (pierwsze kroki "
        "pozycji 2, 6, 8 i 11) zespół może zrobić równolegle w pierwszym tygodniu.",
        "Zasada budżetu: pieniędzy uwolnionych przez pozycje 3 i 4 nie przesuwamy automatycznie do innych kampanii, bo "
        "kolejna złotówka zarabia zwykle mniej niż średnia. Przesuwamy tylko z testem. Niewydanie ich też liczy się do marży.",
        "Czas wdrożenia to nasz szacunek, a nie liczba z danych.",
    ]
    definicje = (f"Okres 1 = {O1_NAZWA}, okres 2 = {O2_NAZWA}; jeśli nie napisano inaczej, liczby dotyczą okresu 2. "
                 f"Przyjęta reguła źródła = pierwsze wejście pacjenta (także anonimowe sesje jego przeglądarek), a kod "
                 f"kampanii na pierwszym zamówieniu rozstrzyga. Sesja płatności = reguła porównawcza. Nowe kampanie = "
                 f"meta_prosp_l4_szybko (Meta, od {data(V['start'][me])}) i tt_prosp_l4_15min (TikTok, od "
                 f"{data(V['start'][tt])}), obie na zwolnienie lekarskie (L4). Pacjent dodatkowy = taki, który bez "
                 f"kampanii by nie przyszedł.")
    wb = V["wbud"]
    nie_robimy = [
        f"Zgoda marketingowa pacjentów nowych kampanii: w najlepszym odczytaniu {tz(V['zgoda_1900'])} rocznie.",
        f"Przeglądarki wbudowane w aplikacje w kampaniach do nowych odbiorców: w tym rachunku 0 zł, bo w tej samej kampanii "
        f"nie wykryliśmy niższej konwersji niż w zwykłych (także w kampanii Meta „lekarz online”: różnica "
        f"{liczba(wb['lekarz_oba'][6], 2)} punktu procentowego, od {liczba(wb['lekarz_oba'][7], 2)} do "
        f"{zn(wb['lekarz_oba'][8], 2)}, {liczba(wb['lekarz_oba'][0])} sesji w przeglądarkach wbudowanych w dwóch latach). "
        f"Porównanie jest obserwacyjne, więc nie rozdziela wpływu przeglądarki od cech użytkowników i nie uzasadnia osobnej "
        f"wyceny naprawy. Nie uogólniamy tego na resztę ruchu: w ruchu osób, które znają już stronę, sesje w przeglądarkach "
        f"w aplikacjach płacą w okresie 2 rzadziej niż zwykłe w tej samej kampanii (remarketing Meta o "
        f"{liczba(-wb['rmkt2'][6], 1)} punktu, {liczba(wb['rmkt2'][0])} sesje w przeglądarkach wbudowanych; Google Ads na markę o "
        f"{liczba(-wb['brand2'][6], 1)} punktu, {liczba(wb['brand2'][0])} sesji; wejścia bezpośrednie o "
        f"{liczba(-wb['bezp2'][6], 1)} punktu, {liczba(wb['bezp2'][0])} sesji). Dane nie rozstrzygają, czy winna jest "
        f"przeglądarka, czy to, kto z niej korzysta (niewiadoma 19).",
        "Mocniejsza sprzedaż i odnowienia TelemediGO: dopiero po teście z pozycji 12.",
        "Przesuwanie uwolnionego budżetu do innych kampanii bez testu (zasada budżetu).",
    ]
    wstep = ("Lista od najważniejszej pozycji. Przy każdej: co widać w danych, ile jest warta w złotych marży na rok "
             "(z założeniami), po czym poznamy, że zadziałała, i ile zajmie wdrożenie. Przy słabym wyniku kampanii "
             "pokazujemy obie drogi, naprawić albo wyłączyć, każdą z wartością w marży. Numer w tabeli przeglądu prowadzi "
             "do karty pozycji, a karta do zakładek z danymi.")
    return {"wstep": wstep, "definicje": definicje, "zasady": zasady, "przeglad": przeglad, "karty": karty, "nie_robimy": nie_robimy,
            "zrodlo": "Notatka: notatki/c_szkic.md, sekcja 3. Liczby: analiza/c_priorytety.py → analiza/wyniki/c_priorytety.txt, "
                      "analiza/c_telemedigo.py → analiza/wyniki/c_telemedigo.txt i raporty części A5, wskazane przy każdej "
                      "pozycji. Kolejność i wyceny sprawdziła niezależnie runda kilku modeli AI różnych firm "
                      "(notatki/konsylium/c_priorytety/synteza.md), a liczby drugi model (notatki/recenzje/c_codex.md)."}


# ---------------------------------------------------------------- 3. czego nie wiemy

def niewiadome(V):
    pm_ = V["p11_meta"]
    p4 = V["p4_cp"]
    E1 = V["e1"]
    wyl0 = float(E1[(E1["kampania"] == NOWE[0]) & (E1["regula"] == "Z1K") & (E1["dodatkowi_proc"] == 0)].iloc[0]["zmiana_marzy90"])
    prog = 100 * wyl0 / (wyl0 + p4[0])
    pz = V["p11_zwroty"]
    zw = V["zwroty_l4"]
    p5 = V["p5"]
    przed_od, przed_do, po_od, po_do, _ = V["safari_okresy"]
    d_saf = pl_data(po_od + "." + po_do.split(".")[-1])
    crm = V["crm"].dropna(subset=["wejscia_na_1000_pacjentow"])
    c1 = crm[crm["miesiac"] < "2025-10"]["wejscia_na_1000_pacjentow"]
    c2 = crm[crm["miesiac"] >= "2025-10"]["wejscia_na_1000_pacjentow"]
    ped = V["pediatra"]
    prow = V["prowizja"]
    cp = V["crm_powrot"]
    D = V["D"]
    rozn = [-V["wbud"][k][6] for k in ("rmkt2", "brand2", "bezp2")]
    mk = V["marka_okna"]
    mA_od, mA_do = (pl_data(x) for x in V["marka_daty"]["A_przed_caly"])
    mD_od, mD_do = (pl_data(x) for x in V["marka_daty"]["D_po_spadku"])
    exn = Dodane()   # niewiadoma 1: horyzont 180 dni dopisany poza szkicem (dopisek Kuby)
    w = [
        ("Czy pacjenci nowych kampanii na L4 są dodatkowi",
         f"od tego zależy decyzja o Meta na L4: od {t1(pm_[2])} tys. zł ({exn('90 dni')}) albo {exn(t1(V['p11_180'][4]))} "
         f"tys. zł ({exn('180 dni')}) do {tzn(pm_[3])} na pełny rok (pozycja 9; próg decyzji około {proc(prog, 0)} "
         f"pacjentów dodatkowych: {exn(proc(V['p11_prog'][0]))} w 90 dniach i {exn(proc(V['p11_prog'][1]))} w 180 dniach)",
         f"wyłączenie kampanii w losowej połowie województw na 4–6 tygodni; badanie przyrostu w panelach Meta i TikToka. "
         f"Taki test nie odróżni wyniku od progu (błąd {liczba(D['test_blad_udzialu_proc_6_tyg_z1k'])}–"
         f"{liczba(D['test_blad_udzialu_proc_4_tyg_z1k'])} punktów procentowych), więc rozpozna tylko niską dodatkowość, a przy "
         f"wyniku niejednoznacznym decyduje reguła ustalona z góry (pozycja 9)", 9),
        ("Która reguła źródła jest bliższa prawdy dla kampanii bez kodu (Google Ads ogólne, Meta lekarz online)",
         "znak wyniku tych kampanii zależy od reguły", "ten sam test z grupą kontrolną bez reklamy", None),
        (f"Powód zwrotów po wizycie L4 w nowych kampaniach ({proc(zw.loc['nowe_kampanie', 'proc_zwrot_po_wizycie'])} wobec "
         f"{proc(zw.loc['pozostali', 'proc_zwrot_po_wizycie'])})",
         f"po wstrzymaniu TikToka dotyczy tylko Meta: od niego zależy, czy naprawa jest bliżej górnego, czy dolnego wariantu "
         f"z pozycji 5, czyli {zakres(pz[5] / 1000, pz[6] / 1000, 1)} tys. zł według przyjętej reguły i "
         f"{zakres(pz[7] / 1000, pz[8] / 1000, 1)} tys. zł według sesji płatności na pełny rok",
         "powód zwrotu, decyzja lekarza (czy L4 wystawiono), treść reklam", 5),
        ("Skąd poranne opóźnienia u internistów (głównie od 5:00 do 12:59, już przy wizytach z najwcześniejszym terminem "
         "dnia, bez widocznego narastania w ciągu poranka) i czy obniżają powroty",
         f"scenariusz od 0 do {t1(V['p8'][3], 0)} tys. zł rocznie; luty 2026 nie pasuje do prostej hipotezy",
         f"grafiki i obsada poranna przed i po {data(V['start'][NOWE[0]])}, obciążenie lekarzy pacjentami spoza B2C, koszt "
         f"obsady; test z dodatkową poranną obsadą w losowe dni", 6),
        ("Sesje zalogowane od wejścia: wizyty „sprawdzam konto” czy zepsuta ścieżka",
         f"0 albo około {t1(p5[1], 0)}–{t1(p5[0], 0)} tys. zł rocznie (wysoki scenariusz {t1(p5[2], 0)} tys. zł)",
         "ręczny test zakupu po zalogowaniu; logi błędów; znacznik „zalogowany na wejściu” w analityce", 8),
        (f"Przyczyna awarii zakładania konta w Safari na iOS od {data(d_saf)}", "potrzebna do naprawy (pozycja 1)",
         f"lista zmian w produkcie z {d_saf.day - 1}–{data(d_saf)}, logi rejestracji według przeglądarki, powtórzenie na iPhonie", 1),
        ("Czy utraceni w Safari na iOS kupili na innym urządzeniu", "zmienia wartość pozycji 1",
         "powiązanie urządzeń po adresie e-mail albo numerze telefonu przy próbie rejestracji", 1),
        ("Czy TelemediGO podnosi powroty, czy tylko przyciąga pacjentów, którzy i tak wracają",
         "decyduje o tym, czy program promować", "losowy, bezpłatny dostęp do zniżek (pozycja 12)", 12),
        ("Czy newsletter i SMS wywołują zakup",
         f"to kanał, którego dodatkowy wpływ warto przetestować (około {proc(100 * cp[1] / (cp[1] + cp[3]), 0)} "
         f"obserwowanych pierwszych powrotów idzie po wejściu z niego); widać kliknięcia, nie wysyłki; wejść na 1 000 "
         f"pacjentów całej narastającej bazy jest coraz mniej (z {zakres(c1.min(), c1.max())} do "
         f"{zakres(c2.min(), c2.max())} miesięcznie)",
         "liczba wysyłek; losowa grupa kontrolna bez wysyłki", 7),
        ("Wartość remarketingu porzuconego koszyka", "przyjęta reguła z definicji przypisuje mu mało pacjentów",
         "grupa kontrolna, której remarketing się nie wyświetla", None),
        ("Sezon a wydatki na kampanie",
         f"wzrostu od {V['sezon'][0]} do {V['sezon'][1]} nie da się rozdzielić; dwa lata to jedna zima i jedno lato w roku",
         "zmiana budżetu w części kraju (grupa kontrolna według województw)", None),
        ("Strata między kliknięciem reklamy a sesją w Meta i TikToku", f"od 0 do {t1(V['p9_zl'], 0)} tys. zł rocznie",
         "panele reklamowe, logi serwera, czas ładowania strony w przeglądarkach wbudowanych", 11),
        (f"Prawdziwa stawka lekarza u pediatry (przyjęte {liczba(V['cennik'].loc['pediatra', 'koszt_lekarza'])} zł)",
         f"przy {liczba(V['cennik'].loc['pediatra', 'koszt_lekarza'])} zł pediatra przynosi stratę nawet bez zniżki; przy "
         f"{KOSZT_INTERNISTY} zł marża na pacjenta w 90 dniach rośnie o {zakres(min(ped), max(ped), 1)} zł",
         "stawka z umów z lekarzami", 10),
        (f"Koszt lekarza za wizyty testowe ({zl(V['testy_koszt_2lata'])} według zasady z zadania, łącznie w obu okresach; "
         f"{zl(V['testy_koszt2'])} w okresie 2)", "wynik biznesu",
         "informacja z rozliczeń, czy lekarze dostali wynagrodzenie za testy", 2),
        ("Warunki umowy z rankingiem lekarzy",
         f"prowizja {tz(prow[0])} za dwa lata według naszej reguły albo {tz(prow[2])} według kodu", "umowa z rankingiem", None),
        ("Pełna długoterminowa marża rocznika okresu 2",
         "rachunek kampanii w 90 i 180 dniach jej nie obejmuje; zaniża wartość kampanii z powracającymi pacjentami",
         f"czas; najstarsze kohorty pozwalają już częściowo ją ocenić ({liczba(V['p16'])} pacjentów okresu 2 ma pełne "
         f"270 dni obserwacji)", None),
        ("Reakcja pacjentów na cenę u specjalistów",
         f"od niej zależy, ile da zmiana cennika (do {tz(V['p14_zl'])} za 10 zł podwyżki)",
         "test dwóch cen dla nowych pacjentów przez 4 tygodnie", 10),
        ("Zasady zwrotów przy odmowie L4 i ryzyko prawne reklam L4",
         "górny wariant pozycji 5 może wymagać zmiany zasad zwrotów", "regulamin, opinia prawna, treść reklam", 5),
        ("Czy sesje w przeglądarkach wbudowanych w aplikacje płacą rzadziej w ruchu osób, które znają już stronę, przez "
         "samą przeglądarkę, czy przez to, kto z niej korzysta",
         f"w remarketingu Meta, Google Ads na markę i wejściach bezpośrednich płacą w okresie 2 rzadziej niż zwykłe o "
         f"{zakres(min(rozn), max(rozn), 1)} punktu procentowego; jeśli winna jest przeglądarka, da się to naprawić na stronie",
         "czas ładowania i błędy strony w przeglądarkach w aplikacjach; ręczny zakup w Instagramie, Facebooku i TikToku; test "
         "linku, który otwiera zwykłą przeglądarkę", None),
        (f"Dlaczego {liczba(D['konta_bez_zakupu_konta'])} konta ({proc(D['konta_bez_zakupu_proc_kont'])} z "
         f"{liczba(D['konta_wszystkie'])} kont z dwóch lat) nie mają żadnego zakupu i czy da się je odzyskać",
         f"każde z tych kont wybrało usługę i przeszło krok konta, a {proc(D['konta_bez_zakupu_proc_ze_startem_platnosci'])} "
         f"z nich zaczęło płatność; {proc(D['konta_bez_zakupu_proc_zgoda'])} z {liczba(D['konta_bez_zakupu_konta'])} ma zgodę "
         f"marketingową (stan na {data(O2[1])}), ale w danych nie ma ani jednego ich wejścia z newslettera albo SMS-a",
         "dane o wysyłkach do tych kont; sekwencja wiadomości do kont bez zakupu z losową grupą kontrolną; bez wyceny przed "
         "testem", None),
        (f"Jak liczba zamówień z Meta na L4 reaguje na wysokość kodu rabatowego (dziś {liczba(D['p6_kod_l4szybko20_znizka_zl'])} zł)",
         f"kod to {tz(D['p6_kod_l4szybko20_znizka_efektywna_pelny_rok_zl'])} zniżki efektywnej na pełny rok; próg rachunku: "
         f"rezygnacja z niego "
         f"opłaca się, jeśli ubędzie mniej niż {proc(D['p6_meta_l4_z1k_bez_kodu_prog_utraty_pierwszych_zamowien_proc'])} "
         f"zamówień z kodem (przy przejściu na START10 mniej niż "
         f"{proc(D['p6_meta_l4_z1k_start10_zamiast_kodu_prog_utraty_pierwszych_zamowien_proc'])})",
         f"losowy podział ruchu Meta na L4 na kod {liczba(D['p6_kod_l4szybko20_znizka_zl'])} zł, {liczba(V['start10'])} zł "
         f"i brak kodu, mierzony marżą na kliknięcie (pozycja 5)", 5),
        (f"Dlaczego od {data(mD_od)} spada konwersja Google Ads na markę",
         f"sesja do płatności u osób, które jeszcze nie kupowały: {proc(mk['D_po_spadku'][-1])} "
         f"({liczba(mk['D_po_spadku'][1])} sesje, {mD_od.day}.{mD_od:%m}–{data(mD_do)}) wobec {proc(mk['A_przed_caly'][-1])} "
         f"({liczba(mk['A_przed_caly'][1])} sesji, {data(mA_od)}–{data(mA_do)}), czyli około "
         f"{zakres(-V['marka_na30'][3], -V['marka_na30'][1], 1)} zamówienia mniej na 30 dni zależnie od okna porównania; to "
         f"nie Safari na iOS ani zmiana struktury ruchu; rok wcześniej w tym samym sezonie spadek był mniejszy i nieistotny "
         f"({liczba(V['marka_rok_wczesniej'], 1)} punktu); koszt kliknięcia marki rośnie (pozycja 2)",
         "lista zmian w kampanii i na stronie z maja 2026; hasła wyszukiwania i reklamy konkurencji na markę w panelu "
         "Google Ads", 2),
    ]
    return {
        "wstep": "Rzeczy, których te dane nie rozstrzygają. Przy każdej: dlaczego to ważne i jaki test albo jakie dane by "
                 "to domknęły. Kwoty to zmiana marży na rok, jak w zakładce „Priorytety”.",
        "wiersze": [{"nr": i + 1, "co": c, "dlaczego": d, "test": t, "pozycja": p, "_dodane": exn.lista if i == 0 else []}
                    for i, (c, d, t, p) in enumerate(w)],
        "zrodlo": "Notatka: notatki/c_szkic.md, sekcja 4. Liczby: analiza/wyniki/c_priorytety.txt (P4, P5, P8, P9, P11, P14), "
                  "analiza/wyniki/a5r_po_zakupie.txt (2b, 5e), analiza/wyniki/a5r_kohorty.txt (7), "
                  "analiza/wyniki/a2_jakosc.txt (2e), analiza/wyniki/a5e_ekonomia.txt, analiza/wyniki/d_kampanie.txt (1, 5, 6), "
                  "analiza/wyniki/d_retencja.txt, analiza/wyniki/d_wynik.txt (3c).",
    }


# ---------------------------------------------------------------- kontrola ze szkicem

def tokeny(t):
    t = t.replace("\xa0", " ").replace(" ", " ")
    return [x.replace(" ", "") for x in re.findall(r"\d{1,3}(?: \d{3})+(?:,\d+)?|\d+(?:,\d+)?", t)]


def szkic_fragmenty():
    with open(SZKIC, encoding="utf-8") as f:
        s = f.read().replace("\r\n", "\n")

    def miedzy(a, b):
        i = s.index(a)
        j = s.index(b, i + len(a)) if b else len(s)
        return s[i:j]

    fr = {"wzrost": miedzy("\n## 1.", "\n## 2."), "telemedigo": miedzy("\n## 2.", "\n## 3."),
          "zasady": miedzy("**Zasady listy:**", "**Przegląd:**"),
          "nie_robimy": miedzy("### Czego proponujemy teraz nie robić", "\n## 4.")}
    p3 = miedzy("**Przegląd:**", "### Pozycja 1.")
    for m in re.finditer(r"^\| (\d+) \|.*$", p3, re.M):
        fr[f"przeglad:{m.group(1)}"] = m.group(0)
    for m in re.finditer(r"^### Pozycja (\d+)\..*?(?=^### |\Z)", miedzy("### Pozycja 1.", "\n## 4."), re.M | re.S):
        fr[f"pozycja:{m.group(1)}"] = m.group(0)
    for m in re.finditer(r"^\| (\d+) \|.*$", miedzy("\n## 4.", "\n## 5."), re.M):
        fr[f"niewiadoma:{m.group(1)}"] = m.group(0)
    return fr


def teksty(obj):
    """Wszystkie napisy w strukturze (bez pól technicznych i odnośników)."""
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        out = []
        for k, v in obj.items():
            if k in ("linki", "zrodlo", "href", "_dodane", "wdrozenie_krotko", "tabela", "pozycja", "nr", "minus"):
                continue
            out += teksty(v)
        return out
    if isinstance(obj, list):
        out = []
        for v in obj:
            out += teksty(v)
        return out
    return []


def kontrola_szkicu(C):
    fr = szkic_fragmenty()
    tg = C["wzrost"]["telemedigo"]
    bloki = [("wzrost", {k: v for k, v in C["wzrost"].items() if k != "telemedigo"}, C["wzrost"]["_dodane"]),
             ("telemedigo", tg, tg["_dodane"]),
             ("zasady", C["priorytety"]["zasady"], []), ("nie_robimy", C["priorytety"]["nie_robimy"], [])]
    for p in C["priorytety"]["przeglad"]:
        bloki.append((f"przeglad:{p['nr']}", {k: v for k, v in p.items() if k != "wdrozenie"}, []))
    for k in C["priorytety"]["karty"]:
        bloki.append((f"pozycja:{k['nr']}", k, k["_dodane"]))
    for w in C["niewiadome"]["wiersze"]:
        bloki.append((f"niewiadoma:{w['nr']}", w, w.get("_dodane", [])))
    wynik = []
    for nazwa, obj, dodane in bloki:
        if nazwa not in fr:
            wynik.append((nazwa, 0, ["brak fragmentu w szkicu"], []))
            continue
        wzor = set(tokeny(fr[nazwa]))
        dod = set(tokeny(" | ".join(dodane)))
        tk = []
        for t in teksty(obj):
            tk += tokeny(t)
        brak = sorted({t for t in tk if t not in wzor and t not in dod})
        uzyte_dod = sorted({t for t in tk if t not in wzor and t in dod})
        wynik.append((nazwa, len(tk), brak, uzyte_dod))
    return wynik


# ---------------------------------------------------------------- kontrole krzyżowe

def kontrole_krzyzowe(V, kontrole, wz=None, mostek=None, wy=None):
    n1, n2 = V["nowi"][1], V["nowi"][2]
    wz_ = V["w1_zm"]
    kontrole += [
        ("C: wzrost nowych pacjentów z liczb W1 = zmiana w raporcie (%)", round(100 * (n2 / n1 - 1), 1), wz_[0]),
        ("C: bez nowych kampanii Z1K / Z2 (%)", f"{100 * (V['bez_z1k'] / n1 - 1):.1f} / {100 * (V['bez_z2'] / n1 - 1):.1f}",
         f"{wz_[1]:.1f} / {wz_[2]:.1f}"),
        ("C: kanały bezpłatne (%)", round(100 * (V["bezpl"][2] / V["bezpl"][1] - 1), 1), wz_[3]),
        ("C: TelemediGO: pacjenci bez nowych kampanii, okres 2 (c_telemedigo = c_priorytety W1)", int(V["go_bez_nowych"]["n"]), V["bez_z1k"]),
        ("C: TelemediGO: zamówienia pierwsze, okres 1 / 2 (c_telemedigo 1e = nowi pacjenci W1)",
         " / ".join(str(int(r["zamowienia_do_oferty"])) for _, r in V["go_kasa"][V["go_kasa"]["zamowienie"] == "1_pierwsze_zamowienie"].iterrows()),
         f"{n1} / {n2}"),
        ("C: powrót 90 dni c_priorytety = a5r_kohorty (%, pacjenci)",
         f"{V['pow_wszyscy']['p90_o1']} {V['pow_wszyscy']['p90_o2']} {int(V['pow_wszyscy']['n90_o1'])} {int(V['pow_wszyscy']['n90_o2'])}",
         f"{V['p90_kohorty'][2]} {V['p90_kohorty'][3]} {int(V['p90_kohorty'][0])} {int(V['p90_kohorty'][1])}"),
    ]
    # TikTok i Meta: zdania c_priorytety.txt wobec tabel a5e_scenariusze.txt
    e3, e3b, e1 = V["e3"], V["e3b"], V["e1"]

    def sc(tab, kamp, reg, kol, warunek=None):
        x = tab[(tab["kampania"] == kamp) & (tab["regula"] == reg)]
        if warunek is not None:
            x = x[x["dodatkowi_proc"] == warunek]
        return int(x.iloc[0][kol])
    tt, me = NOWE[1], NOWE[0]
    kontrole += [
        ("C: TikTok dziś 90/180 dni, c_priorytety = a5e_scenariusze (zł)", " ".join(str(int(x)) for x in V["p3_cp"]),
         " ".join(str(x) for x in (sc(e3, tt, "Z1K", "obecny_wynik"), sc(e3, tt, "Z2", "obecny_wynik"),
                                   sc(e3b, tt, "Z1K", "obecny_wynik_180"), sc(e3b, tt, "Z2", "obecny_wynik_180")))),
        ("C: TikTok po naprawie A 90/180 dni (zł)", " ".join(str(int(x)) for x in V["p3_cp_napr"]),
         " ".join(str(x) for x in (sc(e3, tt, "Z1K", "po_naprawie_A"), sc(e3, tt, "Z2", "po_naprawie_A"),
                                   sc(e3b, tt, "Z1K", "po_naprawie_A_180"), sc(e3b, tt, "Z2", "po_naprawie_A_180")))),
        ("C: Meta dziś 90/180 dni (zł)", " ".join(str(int(x)) for x in V["p4_cp"]),
         " ".join(str(x) for x in (sc(e3, me, "Z1K", "obecny_wynik"), sc(e3, me, "Z2", "obecny_wynik"),
                                   sc(e3b, me, "Z1K", "obecny_wynik_180"), sc(e3b, me, "Z2", "obecny_wynik_180")))),
        ("C: TikTok na pełny rok = 90 dni × 365 / dni działania (zł)",
         " ".join(str(round(x * 365 / V["dni"][tt])) for x in (sc(e3, tt, "Z1K", "obecny_wynik"), sc(e3, tt, "Z2", "obecny_wynik"),
                                                                -sc(e3, tt, "Z1K", "obecny_wynik"), -sc(e3, tt, "Z2", "obecny_wynik"),
                                                                sc(e1, tt, "Z1K", "zmiana_marzy90", 0))),
         " ".join(str(round(x)) for x in V["p11_tt"])),
        ("C: Meta na pełny rok (zł)",
         " ".join(str(round(x * 365 / V["dni"][me])) for x in (sc(e3, me, "Z1K", "obecny_wynik"), sc(e3, me, "Z2", "obecny_wynik"),
                                                                sc(e1, me, "Z1K", "zmiana_marzy90", 100), sc(e1, me, "Z1K", "zmiana_marzy90", 0))),
         " ".join(str(round(x)) for x in V["p11_meta"])),
        ("C: TikTok wyłączenie 100% po 180 dniach i Meta po 180 dniach na pełny rok (zł)",
         " ".join(str(round(x * 365 / V["dni"][k])) for x, k in ((sc(e1, tt, "Z1K", "zmiana_marzy180", 100), tt),
                                                                (sc(e1, tt, "Z2", "zmiana_marzy180", 100), tt),
                                                                (sc(e3b, me, "Z1K", "obecny_wynik_180"), me),
                                                                (sc(e3b, me, "Z2", "obecny_wynik_180"), me))),
         " ".join(str(round(x)) for x in V["p11_180"][:4])),
        ("C: próg decyzji Meta 90 / 180 dni, liczony = raport (%)",
         f"{100 * sc(e1, me, 'Z1K', 'zmiana_marzy90', 0) / (sc(e1, me, 'Z1K', 'zmiana_marzy90', 0) + sc(e3, me, 'Z1K', 'obecny_wynik')):.1f} / "
         f"{100 * sc(e1, me, 'Z1K', 'zmiana_marzy180', 0) / (sc(e1, me, 'Z1K', 'zmiana_marzy180', 0) + sc(e3b, me, 'Z1K', 'obecny_wynik_180')):.1f}",
         f"{V['p11_prog'][0]:.1f} / {V['p11_prog'][1]:.1f}"),
        ("C: naprawa zwrotów samej Meta na pełny rok (zł)",
         " ".join(str(round(x * 365 / V["dni"][me])) for x in V["p11_zwroty"][:4]),
         " ".join(str(round(x)) for x in V["p11_zwroty"][5:])),
    ]
    # dokładne odsetki powrotu (dane kohort strony) po zaokrągleniu = raporty, liczba pacjentów = raporty
    dok = V["powroty_dokladne"]
    W = V["pow_wszyscy"]
    for o in (30, 60, 90):
        kontrole.append((f"C: powrót {o} dni z danych kohort strony = c_priorytety W2 (%, pacjenci)",
                         f"{round(dok[o][0], 1)} {round(dok[o][1], 1)} {dok[o][2]} {dok[o][3]}",
                         f"{W[f'p{o}_o1']} {W[f'p{o}_o2']} {int(W[f'n{o}_o1'])} {int(W[f'n{o}_o2'])}"))
    kontrole.append(("C: powrót 180 dni z danych kohort strony = a5r_kohorty (%, pacjenci)",
                     f"{round(dok[180][0], 1)} {round(dok[180][1], 1)} {dok[180][2]} {dok[180][3]}",
                     f"{V['p180'][2]} {V['p180'][3]} {int(V['p180'][0])} {int(V['p180'][1])}"))
    oc, ocd, odb = V["oceny"], V["oceny_dokladne"], V["oceny_dokladne_odbyte"]
    kontrole.append(("C: oceny internista okres 2 (wizyty, średnia 2 miejsca) = a5r_po_zakupie 3a",
                     " ".join(f"{odb[k]} {ocd[k][0]:.2f}" for k in ("a_do_5_min", "d_ponad_30_min")),
                     " ".join(f"{int(oc.loc[k, 'n'])} {oc.loc[k, 'sr_ocena']:.2f}" for k in ("a_do_5_min", "d_ponad_30_min"))))
    # gs_generic_specjalisci: c_priorytety.txt wobec a5e_kampanie.csv
    ek = V["ek"]
    kontrole.append(("C: gs_generic_specjalisci marża na pacjenta, c_priorytety = a5e_kampanie.csv",
                     " ".join(f"{V['p7'][(r, o)][3]:.1f}" for r in ("Z1K", "Z2") for o in ("90", "180")),
                     " ".join(f"{ek[('gs_generic_specjalisci', r, o)]['marza_na_pac']:.1f}" for r in ("Z1K", "Z2") for o in ("90", "180"))))
    # P1: spadek marży III kwartału = rozbicie W4; marża i wydatki III kwartału z tabeli kwartałów
    q = V["rr"]
    ost = q.index[-1]
    kontrole += [
        ("C: spadek marży III kwartału w P1 = W4 (zł)", int(V["p1_q3_lo"][3]), int(round(-V["kw_rozbicie"][0]))),
        ("C: marża III kwartału z tabeli kwartałów = tabela rok do roku (zł)",
         f"{round(V['kw'].loc[ost, 'marza'])} / {round(V['kw'].loc[str(int(ost[:4]) - 1) + ost[4:], 'marza'])}",
         f"{round(q.loc[ost, 'marza'])} / {round(q.loc[ost, 'marza_rok_wczesniej'])}"),
        ("C: zwroty L4 nowych kampanii: a5r_po_zakupie = a5e_scenariusze (wizyty odbyte)",
         int(V["zwroty_l4"].loc["nowe_kampanie", "wizyty_odbyte"]), int(V["e2a"][0])),
        ("C: zamówienia testowe w P1b (okres 1 + 2) = P13", V["testy"][1] + V["testy"][2], V["testy_razem"][0]),
        ("C: wizyty testowe u internisty i trwające 1 minutę = wszystkie", f"{V['testy_razem'][1]} {V['testy_razem'][2]}",
         f"{V['testy_razem'][0]} {V['testy_razem'][0]}"),
    ]
    # z liczbami, które b_eksport.py liczy sam na bazie
    if wz is not None:
        kontrole.append(("C: nowi pacjenci = eksport z bazy (okres 1 / 2)", f"{n1} / {n2}",
                         f"{wz['pacjenci']['n1']} / {wz['pacjenci']['n2']}"))
        W = V["pow_wszyscy"]
        for o in wz["retencja"]["okna"]:
            d = o["dni"]
            kontrole.append((f"C: powrót {d} dni = eksport z bazy (%, pacjenci)",
                             f"{W[f'p{d}_o1']} {W[f'p{d}_o2']} {int(W[f'n{d}_o1'])} {int(W[f'n{d}_o2'])}",
                             f"{round(o['p1'], 1)} {round(o['p2'], 1)} {o['n1']} {o['n2']}"))
    if mostek is not None:
        d0, d2 = mostek["kroki"][0]["miary"]["zamowienia"], mostek["kroki"][2]["miary"]["zamowienia"]
        kontrole.append(("C: zamówienia dashboardu i oczyszczone = mostek z bazy", f"{int(V['dash_zam'][1])} {int(V['dash_zam'][2])} "
                         f"{int(V['czyste_zam'][1])} {int(V['czyste_zam'][2])}", f"{d0['p1']} {d0['p2']} {d2['p1']} {d2['p2']}"))
    if wy is not None:
        s, start = wy["serie"], dt.date.fromisoformat(wy["start"])

        def marza_okna(od, do):
            a, b = (od - start).days, (do - start).days + 1
            sm = lambda k: sum(s[k][a:b])  # noqa: E731
            return (sm("przychod_pierwsze") + sm("przychod_powtorne") + sm("go") - sm("koszt_lekarza") - sm("wydatki_google")
                    - sm("wydatki_meta") - sm("wydatki_tiktok") - sm("prowizja"))
        z, o_ = [], []
        for k in V["kw"].index:
            r, nr = int(k[:4]), int(k[-1])
            od = dt.date(r, 3 * nr - 2, 1)
            do = (dt.date(r + (nr == 4), (3 * nr) % 12 + 1, 1) - dt.timedelta(days=1))
            z.append(str(round(marza_okna(od, do))))
            o_.append(str(round(V["kw"].loc[k, "marza"])))
        kontrole.append(("C: marża po kwartałach = eksport z bazy (zł, 8 kwartałów)", " ".join(z), " ".join(o_)))


# ---------------------------------------------------------------- główna funkcja

def eksport_c(kontrole, wz=None, mostek=None, wy=None, nag=None, koh=None, pz=None, Z=None, V=None, d_dodatkowe=None):
    """Zapisuje narzedzie/dane_strony/c.js, dopisuje kontrole do listy, zwraca (dane, wynik kontroli szkicu, źródła).
    koh i pz to dane zakładek „Kohorty” i „Po zakupie”; bez nich (uruchomienie samodzielne) czyta je z plików strony."""
    Z = Z if Z is not None else Zrodla()
    V = V if V is not None else wartosci(Z)
    koh = koh if koh is not None else wczytaj_js("kohorty.js", ".kohorty")
    pz = pz if pz is not None else wczytaj_js("po_zakupie.js", ".po_zakupie")
    V["powroty_dokladne"] = powroty_dokladne(koh)
    V["oceny_dokladne"] = {r["koszyk"]: (r["suma"] / r["ocenione"], r["ocenione"]) for r in pz["oceny"]
                           if r["okres"] == 2 and r["spec"] == "internista" and not r["nowa"]}
    V["oceny_dokladne_odbyte"] = {r["koszyk"]: r["odbyte"] for r in pz["oceny"]
                                  if r["okres"] == 2 and r["spec"] == "internista" and not r["nowa"]}
    if nag is None:
        nag = wczytaj_js("podsumowanie.js", ".P")["lejek_naglowek"]
    linki_lejka = {"safari": nag["naprawy"][0]["link"]}
    C = {"wygenerowano": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "wzrost": czy_wzrost(V),
         "priorytety": priorytety(V, linki_lejka), "niewiadome": niewiadome(V)}
    kontrole_krzyzowe(V, kontrole, wz, mostek, wy)
    sz = kontrola_szkicu(C)
    liczb = sum(x[1] for x in sz)
    brakow = sum(len(x[2]) for x in sz)
    kontrole.append((f"C: liczby w tekstach bez pokrycia w c_szkic.md ({len(sz)} fragmentów, {liczb} liczb)", brakow, 0))
    sd = kontrola_d(teksty_d(V), d_dodatkowe)
    kontrole.append((f"D: liczby w tekstach innych zakładek bez pokrycia w d_teksty_strony.md ({len(sd)} sekcji, "
                     f"{sum(x[1] for x in sd)} liczb)", sum(len(x[2]) for x in sd), 0))
    sz = sz + sd
    # pola techniczne nie trafiają na stronę
    C["wzrost"].pop("_dodane", None)
    C["wzrost"]["telemedigo"].pop("_dodane", None)
    for w in C["niewiadome"]["wiersze"]:
        w.pop("_dodane", None)
    for k in C["priorytety"]["karty"]:
        k.pop("_dodane", None)
    with open(os.path.join(DANE, "c.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("window.D=window.D||{};\n")
        f.write("D.C=" + json.dumps(C, ensure_ascii=False, separators=(",", ":"), default=lambda o: o.item()) + ";\n")
    return C, sz, Z


def raport_szkicu(sz):
    linie = ["Kontrola ze szkicem (notatki/c_szkic.md): każda liczba w zdaniach strony stoi w tym samym fragmencie szkicu. "
             "Wiersze „d:” to teksty pozostałych zakładek wobec notatki notatki/d_teksty_strony.md.",
             "„Dodane” = liczby dopisane poza szkicem (liczebność przy odsetku, okres, kwoty w dniach działania), odczytane z raportów.",
             f"   {'fragment':16} {'liczb':>6}  {'bez pokrycia':14} dodane"]
    for nazwa, n, brak, dod in sz:
        linie.append(f"   {nazwa:16} {n:>6}  {(', '.join(brak) or '—'):14} {', '.join(dod) or '—'}")
    return linie


def main():
    sys.stdout.reconfigure(errors="replace")
    kontrole = []
    C, sz, Z = eksport_c(kontrole)
    linie = [f"B2 — EKSPORT PUNKTU C NA STRONĘ ({C['wygenerowano']})", "",
             f"1. Plik: narzedzie/dane_strony/c.js ({os.path.getsize(os.path.join(DANE, 'c.js')):,} bajtów). "
             f"Odczytów z raportów: {len(Z.odczyty)}.", "", "2. Kontrole krzyżowe",
             f"   {'co':78} {'eksport':>24} {'oczekiwane':>24}  wynik"]
    bledy = 0
    for opis, w, o in kontrole:
        ok = (str(w) == str(o)) if isinstance(o, str) else abs(float(w) - float(o)) < 1e-9
        bledy += not ok
        linie.append(f"   {opis:78} {w!s:>24} {o!s:>24}  {'zgodne' if ok else 'RÓŻNICA'}")
    linie += ["", f"   Różnic: {bledy} z {len(kontrole)} kontroli.", "", "3. " + raport_szkicu(sz)[0]] + raport_szkicu(sz)[1:]
    linie += ["", "4. Odczyty z raportów (plik, miejsce, wartość)"]
    for plik, gdzie, v in Z.odczyty:
        linie.append(f"   {plik:24} {gdzie[:40]:40} {v}")
    with open(RAPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linie) + "\n")
    print("\n".join(linie[:len(kontrole) + 12 + len(sz)]))


if __name__ == "__main__":
    main()
