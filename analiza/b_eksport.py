"""B — eksport danych do plików strony narzędzia (narzedzie/dane_strony/*.js).

Strona nie ma ani jednej liczby wpisanej ręcznie w tekst (zasada Kuby z pierwszego zatrzymania punktu B).
Każde zdanie z liczbą powstaje tutaj, z bazy (schemat `czyste`, a przy jakości danych też `surowe`)
albo z wyników części pozyskania A5 (`analiza/wyniki/a5p_lejek_dzienny.csv.gz`, `a5p_zdarzenia.csv`).

Pliki danych są skryptami JS (`window.D...`), a nie JSON-em. Dzięki temu strona działa z serwera
statycznego i po otwarciu `narzedzie/index.html` wprost z dysku.

Na końcu uruchamia analiza/b2_eksport_c.py (wynik punktu C, plik c.js) i dopisuje jego kontrole do raportu.

Uruchamianie z głównego folderu projektu, po `a5p_lejek.py` i `a5p_zdarzenia.py`:
    python -I analiza/b_eksport.py
Baza tylko do odczytu. Raport z kontrolą zgodności z notatkami: analiza/wyniki/b_eksport.txt.
"""
import datetime as dt
import json
import os
import subprocess
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
import a5r_punktualnosc as RP  # noqa: E402  (KOSZYK, PORA, NOWE: definicje części retencji, ZALOZENIA 37)
import a5r_struktura as RS  # noqa: E402  (USLUGA, ZNIZKA: cechy pierwszego zakupu, ZALOZENIA 35)
import e_teksty as ET  # noqa: E402  (runda E: nowe karty tekstowe)
import e_teksty_zakladki as EZ  # noqa: E402
import b2_eksport_c as B2  # noqa: E402  (wynik punktu C: czy to wzrost, priorytety, czego nie wiemy)

KATALOG = D.KATALOG
WYNIKI = os.path.join(KATALOG, "analiza", "wyniki")
DANE = os.path.join(KATALOG, "narzedzie", "dane_strony")
RAPORT = os.path.join(WYNIKI, "b_eksport.txt")
LEJEK_CSV = os.path.join(WYNIKI, "a5p_lejek_dzienny.csv.gz")
ZDARZENIA_CSV = os.path.join(WYNIKI, "a5p_zdarzenia.csv")
SIATKA_A3 = os.path.join(WYNIKI, "a3_siatka.csv")

START = dt.date(2024, 10, 1)
KONIEC = dt.date.fromisoformat(D.KONIEC)
OKRES2 = dt.date.fromisoformat(D.OKRES2)
KROKI = ["k1", "k2", "k3", "k4", "k5"]
W_APLIKACJI = ["Instagram", "Facebook", "TikTok"]
PODZIALY = ["calosc", "urzadzenie", "przegladarka", "system_przegladarka", "urzadzenie_przegladarka",
            "kanal", "kampania", "strona_wejscia"]

MIESIACE_RZ = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


# ---------------------------------------------------------------- formatowanie po polsku

def liczba(x, miejsca=0):
    """1 781 → '1 781' (twarda spacja), 5.89 → '5,89'."""
    s = f"{x:,.{miejsca}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


def proc(x, miejsca=1):
    return liczba(x, miejsca) + "%"


def zl(x):
    return liczba(x) + " zł"


def pp(x, miejsca=1):
    """Różnica w punktach procentowych, słownie (ułamek → 'punktu procentowego')."""
    w = round(abs(x), miejsca)
    if miejsca > 0 or w != int(w):
        slowo = "punktu procentowego"
    elif int(w) == 1:
        slowo = "punkt procentowy"
    elif int(w) % 10 in (2, 3, 4) and int(w) % 100 not in (12, 13, 14):
        slowo = "punkty procentowe"
    else:
        slowo = "punktów procentowych"
    return f"{liczba(abs(x), miejsca)} {slowo}"


def data(d):
    return f"{d.day}.{d:%m.%Y}"


FORMY = {"sesja": ("sesja", "sesje", "sesji"), "zamowienie": ("zamówienie", "zamówienia", "zamówień"),
         "pacjent": ("pacjent", "pacjentów", "pacjentów"), "minuta": ("minuta", "minuty", "minut"),
         "zakup": ("zakup", "zakupy", "zakupów"), "przegladarka": ("przeglądarka", "przeglądarki", "przeglądarek"),
         "wizyta": ("wizyta", "wizyty", "wizyt")}


def ile(n, rzecz):
    """Liczba z rzeczownikiem w poprawnej formie: 1 sesja, 1 763 sesje, 1 011 sesji, 183,7 sesji."""
    f1, f2, f5 = FORMY[rzecz]
    if n != int(n):
        return f"{liczba(n, 1)} {f5}"
    n = int(n)
    forma = f1 if n == 1 else f2 if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14) else f5
    return f"{liczba(n)} {forma}"


def zakres(a, b, miejsca=0):
    """'40%' gdy oba końce po zaokrągleniu są równe, inaczej '19–26%'."""
    if round(a, miejsca) == round(b, miejsca):
        return proc(a, miejsca)
    return f"{liczba(a, miejsca)}–{proc(b, miejsca)}"


def okres_nazwa(od, do):
    return f"{MIESIACE_RZ[od.month - 1]} {od.year} – {MIESIACE_RZ[do.month - 1]} {do.year}"


O1 = (START, OKRES2 - dt.timedelta(days=1))
O2 = (OKRES2, KONIEC)
O1_NAZWA, O2_NAZWA = okres_nazwa(*O1), okres_nazwa(*O2)


def zapisz_js(nazwa, klucz, obiekt):
    """Zapisuje `window.D.<klucz> = {...}` do narzedzie/dane_strony/<nazwa>.js. Zwraca rozmiar w bajtach."""
    os.makedirs(DANE, exist_ok=True)
    tresc = json.dumps(obiekt, ensure_ascii=False, separators=(",", ":"))
    sciezka = os.path.join(DANE, nazwa)
    with open(sciezka, "w", encoding="utf-8", newline="\n") as f:
        f.write("window.D=window.D||{};\n")
        f.write(f"D{klucz}={tresc};\n")
    return os.path.getsize(sciezka)


# ---------------------------------------------------------------- etykiety

ETYKIETY = {
    "typ": {"zwykla": "Sesje zwykłe", "zalogowana_od_wejscia": "Sesje zalogowane od wejścia",
            "samo_telemedigo": "Zakup samego TelemediGO"},
    "pacjent": {"nie_kupowal": "Jeszcze nie kupowali", "kupowal_wczesniej": "Kupowali wcześniej"},
    "kroki": {"k1": "Wybór usługi", "k2": "Wybór terminu", "k3": "Logowanie albo założenie konta",
              "k4": "Wejście na płatność", "k5": "Płatność przyjęta"},
    "podzial": {"calosc": "Całość", "urzadzenie": "Urządzenie", "przegladarka": "Przeglądarka",
                "system_przegladarka": "System i przeglądarka", "urzadzenie_przegladarka": "Urządzenie i przeglądarka",
                "kanal": "Źródło (kanał)", "kampania": "Kampania", "strona_wejscia": "Strona wejścia"},
    "urzadzenie": {"desktop": "Komputer", "mobile": "Telefon", "tablet": "Tablet"},
    "kanal": {"afiliacja_ranking": "Afiliacja (ranking lekarzy)", "bezposrednie": "Wejścia bezpośrednie",
              "crm": "CRM (newsletter i SMS)", "google_ads_marka": "Google Ads: hasło marki",
              "google_ads_ogolne": "Google Ads: hasła ogólne", "meta_pozyskanie": "Meta: pozyskanie",
              "meta_remarketing": "Meta: remarketing", "program_polecen": "Program poleceń", "tiktok": "TikTok",
              "wyszukiwarka_bezplatna": "Wyszukiwarka bezpłatna"},
    "kampania": {"bezposrednie": "Wejścia bezpośrednie", "bing_organic": "Bing bezpłatnie",
                 "crm_go_upsell": "Newsletter: sprzedaż TelemediGO", "crm_reactivation": "Newsletter reaktywacyjny",
                 "crm_recepta_przypomnienie": "Newsletter: przypomnienie o recepcie",
                 "crm_sms_przypomnienie": "SMS z przypomnieniem", "google_organic": "Google bezpłatnie",
                 "gs_brand": "Google Ads: marka", "gs_generic_erecepta": "Google Ads: e-recepta",
                 "gs_generic_l4": "Google Ads: L4", "gs_generic_lekarz_online": "Google Ads: lekarz online",
                 "gs_generic_specjalisci": "Google Ads: specjaliści",
                 "meta_prosp_l4_szybko": "Meta pozyskanie: L4 szybko",
                 "meta_prosp_lekarz_online": "Meta pozyskanie: lekarz online",
                 "meta_rmkt_koszyk": "Meta remarketing: koszyk", "program_polecen": "Program poleceń",
                 "rankinglekarzy_affiliate": "Afiliacja: ranking lekarzy",
                 "tt_prosp_l4_15min": "TikTok: L4 w 15 minut"},
    "przegladarka": {"Instagram": "Instagram (w aplikacji)", "Facebook": "Facebook (w aplikacji)",
                     "TikTok": "TikTok (w aplikacji)"},
    "w_aplikacji": W_APLIKACJI,
    "obszary": {"lejek": "Lejek", "retencja": "Retencja", "obsluga": "Obsługa pacjenta", "jakosc": "Jakość danych"},
}
SYSTEMY = {"iOS": "na iOS", "Android": "na Androidzie", "Windows": "na Windowsie", "macOS": "na macOS",
           "Linux": "na Linuksie"}
URZ = {"desktop": "Komputer", "mobile": "Telefon", "tablet": "Tablet"}


def etykiety_pochodne(wartosci_sp, wartosci_up):
    ETYKIETY["system_przegladarka"] = {}
    for w in wartosci_sp:
        sys_, prz = w.split(" ", 1)
        dop = " (w aplikacji)" if prz in W_APLIKACJI else ""
        ETYKIETY["system_przegladarka"][w] = f"{prz}{dop} {SYSTEMY.get(sys_, sys_)}"
    ETYKIETY["urzadzenie_przegladarka"] = {}
    for w in wartosci_up:
        u, prz = w.split(" ", 1)
        dop = " (w aplikacji)" if prz in W_APLIKACJI else ""
        ETYKIETY["urzadzenie_przegladarka"][w] = f"{URZ.get(u, u)}: {prz}{dop}"


def et(podzial, wartosc):
    return ETYKIETY.get(podzial, {}).get(wartosc, wartosc)


# ---------------------------------------------------------------- 1. lejek

def wczytaj_lejek():
    d = pd.read_csv(LEJEK_CSV, dtype={"wartosc": str})
    d["dzien"] = pd.to_datetime(d["dzien"]).dt.date
    for k in KROKI + ["zamowienia", "pierwsze_zamowienia"]:
        d[k] = d[k].fillna(0).astype(int)
    return d


def suma(d, od=None, do=None, **war):
    """Suma sesji i kroków w podzbiorze (od, do włącznie)."""
    m = pd.Series(True, index=d.index)
    if od:
        m &= d["dzien"] >= od
    if do:
        m &= d["dzien"] <= do
    for k, v in war.items():
        m &= d[k].isin(v) if isinstance(v, (list, tuple, set)) else (d[k] == v)
    return d.loc[m, ["sesje"] + KROKI].sum()


def eksport_lejka(d, kontrole):
    """Pliki lejek_<podział>.js: gęste tablice dzienne (sesje, k1..k5) dla każdej serii typ × pacjent × wartość."""
    # zgodność kolumn, które pomijamy w eksporcie
    zw = d[d["typ"] == "zwykla"]
    kontrole.append(("zamówienia = płatność przyjęta (sesje zwykłe)", int((zw["zamowienia"] != zw["k5"]).sum()), 0))
    nk = zw[zw["pacjent"] == "nie_kupowal"]
    kontrole.append(("pierwsze zamówienia = płatności u osób, które jeszcze nie kupowały",
                     int((nk["pierwsze_zamowienia"] != nk["k5"]).sum()), 0))
    kontrole.append(("pierwsze zamówienia u osób, które kupowały wcześniej",
                     int(zw.loc[zw["pacjent"] == "kupowal_wczesniej", "pierwsze_zamowienia"].sum()), 0))
    dni = (KONIEC - START).days + 1
    rozmiary = {}
    for p in PODZIALY:
        x = d[d["podzial"] == p]
        serie = []
        for (typ, pac, w), g in x.groupby(["typ", "pacjent", "wartosc"], sort=True):
            idx = [(dz - START).days for dz in g["dzien"]]
            s = {"typ": typ, "pacjent": pac, "w": w}
            for k in ["sesje"] + KROKI:
                tab = [0] * dni
                for i, v in zip(idx, g[k]):
                    tab[i] = int(v)
                if any(tab):
                    s["s" if k == "sesje" else k] = tab
            serie.append(s)
        rozmiary[p] = zapisz_js(f"lejek_{p}.js", f".lejek=D.lejek||{{}};D.lejek[{json.dumps(p)}]",
                                {"start": START.isoformat(), "dni": dni, "serie": serie})
    return rozmiary


def naglowek_lejka(d, zd, kontrole, td, V2):
    """Zdania nagłówka lejka (dopisek Kuby: nie gubić Safari na iOS ani przeglądarek w aplikacjach)."""
    c = d[(d["podzial"] == "calosc") & (d["typ"] == "zwykla")]
    a1, a2 = suma(c, *O1), suma(c, *O2)
    k1, k2 = 100 * a1["k5"] / a1["sesje"], 100 * a2["k5"] / a2["sesje"]
    kontrole += [("konwersja sesji do płatności, okres 1 (%)", round(k1, 1), 16.0),
                 ("konwersja sesji do płatności, okres 2 (%)", round(k2, 1), 13.7)]

    # rozkład zmiany według przeglądarki: struktura (u2 − u1) × c1 i konwersja w obrębie u2 × (c2 − c1)
    p = d[(d["podzial"] == "przegladarka") & (d["typ"] == "zwykla")]
    g1 = p[p["dzien"] <= O1[1]].groupby("wartosc")[["sesje", "k5"]].sum()
    g2 = p[p["dzien"] >= O2[0]].groupby("wartosc")[["sesje", "k5"]].sum()
    g = g1.join(g2, how="outer", lsuffix="_1", rsuffix="_2").fillna(0)
    g["u1"], g["u2"] = g["sesje_1"] / g["sesje_1"].sum(), g["sesje_2"] / g["sesje_2"].sum()
    g["c1"] = (g["k5_1"] / g["sesje_1"]).where(g["sesje_1"] > 0)
    g["c2"] = g["k5_2"] / g["sesje_2"]
    nowe = g["c1"].isna()   # grupy nowe w okresie 2 w całości do efektu struktury (ZALOZENIA, A5 pozyskanie)
    struktura = 100 * (((g["u2"] - g["u1"]) * g["c1"].fillna(0)).sum() + (g.loc[nowe, "u2"] * g.loc[nowe, "c2"]).sum())
    w_obrebie = 100 * (g.loc[~nowe, "u2"] * (g.loc[~nowe, "c2"] - g.loc[~nowe, "c1"])).sum()
    kontrole += [("rozkład według przeglądarki: struktura (pp)", round(struktura, 2), -3.00),
                 ("rozkład według przeglądarki: w obrębie (pp)", round(w_obrebie, 2), 0.67)]
    ua1 = 100 * g.loc[W_APLIKACJI, "sesje_1"].sum() / g["sesje_1"].sum()
    ua2 = 100 * g.loc[W_APLIKACJI, "sesje_2"].sum() / g["sesje_2"].sum()
    kontrole += [("udział przeglądarek w aplikacjach, okres 1 (%)", round(ua1, 1), 10.7),
                 ("udział przeglądarek w aplikacjach, okres 2 (%)", round(ua2, 1), 35.6)]

    # kroki w przeglądarkach w aplikacjach wobec Chrome i Safari (oba okresy, zakres)
    def kroki_grupy(wartosci):
        wyn = []
        for od, do in (O1, O2):
            for w in wartosci:
                s = suma(p, od, do, wartosc=w)
                if s["sesje"] > 0:
                    wyn.append({"k1": s["k1"] / s["sesje"], "k2": s["k2"] / s["k1"], "k3": s["k3"] / s["k2"],
                                "k5s": s["k5"] / s["sesje"], "sesje": s["sesje"]})
        return pd.DataFrame(wyn) * [100, 100, 100, 100, 1]
    ka, kc = kroki_grupy(W_APLIKACJI), kroki_grupy(["Chrome", "Safari"])
    kontrole += [("przeglądarki w aplikacjach: płatność na sesję, min (%)", round(ka["k5s"].min(), 1), 4.8),
                 ("przeglądarki w aplikacjach: płatność na sesję, max (%)", round(ka["k5s"].max(), 1), 7.2)]

    # Safari na iOS: krok konta u osób, które jeszcze nie kupowały
    sp = d[(d["podzial"] == "system_przegladarka") & (d["typ"] == "zwykla") & (d["pacjent"] == "nie_kupowal")]
    wiersz = zd[(zd["podzial"] == "system_przegladarka") & (zd["wartosc"] == "iOS Safari")
                & (zd["przejscie"] == "logowanie")].iloc[0]
    dz = dt.date.fromisoformat(wiersz["data"])
    przed = (dz - dt.timedelta(days=60), dz - dt.timedelta(days=1))
    po60 = (dz, dz + dt.timedelta(days=59))
    po = (dz, KONIEC)
    ios = lambda od, do: suma(sp, od, do, wartosc="iOS Safari")  # noqa: E731
    reszta = lambda od, do: suma(sp[sp["wartosc"] != "iOS Safari"], od, do)  # noqa: E731
    s_przed, s_po60, s_po = ios(*przed), ios(*po60), ios(*po)
    r_przed, r_po60 = reszta(*przed), reszta(*po60)
    st = lambda s: 100 * s["k3"] / s["k2"]  # noqa: E731
    kontrole += [("Safari na iOS, krok konta 60 dni przed (%)", round(st(s_przed), 1), 66.2),
                 ("Safari na iOS, krok konta 60 dni po (%)", round(st(s_po60), 1), 45.1),
                 ("Safari na iOS, krok konta do końca danych (%)", round(st(s_po), 1), 45.6)]
    # szacunek utraconych pierwszych zamówień (a5p_zdarzenia.py, sekcja 5f)
    baza = (OKRES2, dz - dt.timedelta(days=1))
    b_ios, b_r, p_r = ios(*baza), reszta(*baza), reszta(*po)
    dni_po = (KONIEC - dz).days + 1
    dalej = s_po["k5"] / s_po["k3"]
    utr = (b_ios["k3"] / b_ios["k2"] - s_po["k3"] / s_po["k2"]) * s_po["k2"] * dalej
    tlo = b_r["k3"] / b_r["k2"] - p_r["k3"] / p_r["k2"]
    utr_tlo = (b_ios["k3"] / b_ios["k2"] - s_po["k3"] / s_po["k2"] - tlo) * s_po["k2"] * dalej
    kontrole += [("Safari na iOS: utracone pierwsze zamówienia do końca danych", round(utr), 695),
                 ("Safari na iOS: to samo po odjęciu tła", round(utr_tlo), 628)]
    safari = {
        "data": dz.isoformat(), "przed": [przed[0].isoformat(), przed[1].isoformat()],
        "po60": [po60[0].isoformat(), po60[1].isoformat()],
        "przed_proc": st(s_przed), "po60_proc": st(s_po60), "po_proc": st(s_po),
        "przed_k2": int(s_przed["k2"]), "po60_k2": int(s_po60["k2"]),
        "przed_od": str(przed[0]), "przed_do": str(przed[1]), "po60_od": str(po60[0]), "po60_do": str(po60[1]),
        "reszta_przed_proc": st(r_przed), "reszta_po60_proc": st(r_po60),
        "utracone_od": round(utr_tlo), "utracone_do": round(utr), "dni_po": dni_po,
        "na30_od": utr_tlo / dni_po * 30, "na30_do": utr / dni_po * 30,
    }

    zal = d[(d["podzial"] == "calosc") & (d["typ"] == "zalogowana_od_wejscia")]
    tgo = d[(d["podzial"] == "calosc") & (d["typ"] == "samo_telemedigo")]
    z1, z2, t1, t2 = suma(zal, *O1), suma(zal, *O2), suma(tgo, *O1), suma(tgo, *O2)
    zal_razem = suma(zal)

    zdania = [
        f"Konwersja sesji do płatności spadła z {proc(k1)} w okresie {O1_NAZWA} ({liczba(a1['sesje'])} sesji, "
        f"{liczba(a1['k5'])} płatności) do {proc(k2)} w okresie {O2_NAZWA} ({liczba(a2['sesje'])} sesji, "
        f"{liczba(a2['k5'])} płatności).",
        f"Rachunkowo prawie cały spadek to zmiana ruchu. Udział przeglądarek wbudowanych w aplikacje Instagram, "
        f"Facebook i TikTok wzrósł z {proc(ua1)} do {proc(ua2)} sesji. Sama zmiana struktury ruchu według "
        f"przeglądarki daje {liczba(struktura, 2)} {pp(struktura, 2).split(' ', 1)[1]}, a zmiana konwersji w obrębie "
        f"przeglądarek {'+' if w_obrebie >= 0 else '−'}{pp(w_obrebie, 2)}.",
        td["lejek_rozklad"],
        td["lejek_naprawy"],
    ]
    # ten sam rozkład według przeglądarki w raporcie a5p_lejek.txt (sekcja 4), z którego idzie zdanie o podziałach
    kontrole += [("lejek: rozkład według przeglądarki, struktura i konwersja (pp) = a5p_lejek.txt",
                  f"{struktura:.2f} / {w_obrebie:.2f}", "{:.2f} / {:.2f}".format(*V2["rozklad_lejka"]["przegladarka"]))]
    naprawy = [
        {"tytul": f"Safari na iPhone'ach i iPadach: od {data(dz)} gwałtownie spada skuteczność zakładania nowego konta",
         "tekst": f"Konta dalej powstają, ale rzadziej. Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, "
                  f"spadł z {proc(st(s_przed))} w 60 dniach przed awarią ({data(przed[0])}–{data(przed[1])}, "
                  f"{ile(s_przed['k2'], 'sesja')} z wyborem terminu) do {proc(st(s_po60))} w 60 dniach po niej "
                  f"({data(po60[0])}–{data(po60[1])}, {ile(s_po60['k2'], 'sesja')}). "
                  f"Pozostałe przeglądarki w tych samych dniach: {proc(st(r_przed))} i {proc(st(r_po60))}. "
                  f"Szacunek: {liczba(utr_tlo)}–{liczba(utr)} utraconych pierwszych zamówień do {data(KONIEC)}, "
                  f"czyli {liczba(utr_tlo / dni_po * 30)}–{liczba(utr / dni_po * 30)} na 30 dni.",
         "link": f"#lejek?pac=nie_kupowal&podz=system_przegladarka&krok=k3&a={przed[0]}_{przed[1]}"
                 f"&b={po60[0]}_{po60[1]}&w=iOS%20Safari"},
        {"tytul": td["przegl_tytul"],
         "tekst": td["przegl_tekst"] + " Dla porównania cały ruch osób, które jeszcze nie kupowały (wszystkie kampanie "
                  f"razem): przeglądarki w aplikacjach płacą w obu okresach w {zakres(ka['k5s'].min(), ka['k5s'].max(), 1)} "
                  f"sesji, a Chrome i Safari "
                  f"w {zakres(kc['k5s'].min(), kc['k5s'].max(), 1)}. Usługę wybiera "
                  f"{zakres(ka['k1'].min(), ka['k1'].max())} sesji (Chrome i Safari "
                  f"{zakres(kc['k1'].min(), kc['k1'].max())}), termin {zakres(ka['k2'].min(), ka['k2'].max())} tych, "
                  f"które wybrały usługę (wobec {zakres(kc['k2'].min(), kc['k2'].max())}), a krok konta "
                  f"{zakres(ka['k3'].min(), ka['k3'].max())} tych, które wybrały termin (wobec "
                  f"{zakres(kc['k3'].min(), kc['k3'].max())}). Liczby sesji są w tabeli lejka po wybraniu podziału "
                  f"według przeglądarki.",
         "link": "#lejek?pac=nie_kupowal&podz=przegladarka&krok=k5&w=Chrome,Safari,Instagram,Facebook,TikTok"},
    ]
    osobne = [
        f"Sesje zalogowane od wejścia: {liczba(z1['sesje'])} w okresie {O1_NAZWA} i {liczba(z2['sesje'])} w okresie "
        f"{O2_NAZWA}. Usługę wybiera {proc(100 * zal_razem['k1'] / zal_razem['sesje'])} z nich, termin "
        f"{ile(zal_razem['k2'], 'sesja')} przez dwa lata, a płatności nie ma żadnej. Pokazujemy je osobno, "
        f"bo dane nie rozstrzygają, czy to wizyty „sprawdzam konto”, czy zepsuta ścieżka zakupu.",
        f"Zakupy samego TelemediGO: {liczba(t1['sesje'])} w okresie {O1_NAZWA} i {liczba(t2['sesje'])} w okresie "
        f"{O2_NAZWA}. Mają tylko kroki płatności i płacą zawsze.",
        td["konta"],
    ]
    return {"zdania": zdania, "naprawy": naprawy, "osobne": osobne, "safari": safari,
            "konw": [k1, k2], "sesje": [int(a1["sesje"]), int(a2["sesje"])], "platnosci": [int(a1["k5"]), int(a2["k5"])]}


# ---------------------------------------------------------------- 2. czy to wzrost (wstępne)

def czy_wzrost(con, mostek, kontrole):
    D.zbuduj_podstawy(con)
    D.zbuduj_kohorty(con)
    n = dict(con.execute("SELECT okres, count(*) FROM koh GROUP BY 1").fetchall())
    r = con.execute(D.stopy_por()).df().iloc[0]
    kontrole += [("nowi pacjenci, okres 1", n[1], 16231), ("nowi pacjenci, okres 2", n[2], 24687),
                 ("powrót w 90 dniach, okres 1 (%)", r["p90_o1"], 23.9), ("powrót w 90 dniach, okres 2 (%)", r["p90_o2"], 17.4),
                 ("pacjenci w porównaniu 90 dni, okres 1", r["n90_o1"], 12867),
                 ("pacjenci w porównaniu 90 dni, okres 2", r["n90_o2"], 18924)]
    wzrost = 100 * (n[2] / n[1] - 1)
    okna = []
    for o in D.OKNA:
        g1, g2 = D.granice_por(o)
        okna.append({"dni": o, "p1": r[f"p{o}_o1"], "p2": r[f"p{o}_o2"], "n1": int(r[f"n{o}_o1"]),
                     "n2": int(r[f"n{o}_o2"]), "do1": g1.isoformat(), "do2": g2.isoformat()})
    # okno 180 dni dla wykresu pierwszej zakładki (etap 5 grafiki): ta sama funkcja, te same dni kalendarzowe
    r180 = con.execute(D.stopy_por(okna=(180,))).df().iloc[0]
    g1, g2 = D.granice_por(180)
    okna.append({"dni": 180, "p1": r180["p180_o1"], "p2": r180["p180_o2"], "n1": int(r180["n180_o1"]),
                 "n2": int(r180["n180_o2"]), "do1": g1.isoformat(), "do2": g2.isoformat()})
    # zmiana w punktach z wartości niezaokrąglonych, tak jak w tabeli karty „Lepsza retencja” (prośba sesji grafiki)
    rd = con.execute(D.stopy_por(okna=tuple(D.OKNA) + (180,), zaokr=10)).df().iloc[0]
    for ok_ in okna:
        ok_["zm_pkt"] = round(float(rd[f"p{ok_['dni']}_o2"] - rd[f"p{ok_['dni']}_o1"]), 1)
    kontrole += [("powrót w 180 dniach, pacjenci okresu 1 (pierwsza zakładka)", int(r180["n180_o1"]), 9125),
                 ("powrót w 180 dniach, pacjenci okresu 2 (pierwsza zakładka)", int(r180["n180_o2"]), 12591),
                 ("powrót w 180 dniach, okres 1 (%)", r180["p180_o1"], 27.5), ("powrót w 180 dniach, okres 2 (%)", r180["p180_o2"], 22.2)]
    g1, g2 = D.granice_por(90)
    dash = mostek["kroki"][0]["miary"]
    czyste = mostek["kroki"][2]["miary"]
    return {
        "pacjenci": {"n1": n[1], "n2": n[2], "wzrost": wzrost,
                     "zdanie": f"Nowych pacjentów jest więcej: {liczba(n[2])} w okresie {O2_NAZWA} wobec {liczba(n[1])} "
                               f"w okresie {O1_NAZWA}, czyli {'+' if wzrost >= 0 else ''}{proc(wzrost)}."},
        "retencja": {"okna": okna,
                     "zdanie": f"Retencja jest niższa: w ciągu 90 dni od pierwszego zakupu wraca {proc(r['p90_o2'])} nowych "
                               f"pacjentów z okresu {O2_NAZWA} ({ile(r['n90_o2'], 'pacjent')} z kohort do {data(g2)}) "
                               f"wobec {proc(r['p90_o1'])} z okresu {O1_NAZWA} ({ile(r['n90_o1'], 'pacjent')} z kohort "
                               f"z tych samych dni kalendarzowych, do {data(g1)})."},
        "dashboard": {
            "zdanie": f"Dashboard pokazuje {'+'}{proc(dash['nowi']['wzrost'], 0)} pacjentów, "
                      f"+{proc(dash['zamowienia']['wzrost'], 0)} zamówień, +{proc(dash['przychod']['wzrost'], 0)} "
                      f"przychodu i +{proc(dash['go']['wzrost'], 0)} TelemediGO, ale liczy dane na surowo. Po usunięciu "
                      f"duplikatów i zamówień testowych wzrost zamówień wynosi +{proc(czyste['zamowienia']['wzrost'])}, "
                      f"a przychodu +{proc(czyste['przychod']['wzrost'])} przed zwrotami i "
                      f"+{proc(mostek['kroki'][3]['miary']['przychod']['wzrost'])} po zwrotach."},
    }


# ---------------------------------------------------------------- 3. jakość danych

def jakosc(con, kontrole):
    con.execute("""
      CREATE TEMP TABLE zs AS
      SELECT order_id, user_id, status, specialization, visit_purpose, discount_type, promo_code, duration_min,
             amount_paid::DOUBLE zap, refund_amount::DOUBLE zw, created_at, session_id,
             row_number() OVER (PARTITION BY order_id ORDER BY wiersz_w_pliku) > 1 kopia,
             user_id IN (SELECT user_id FROM surowe.orders WHERE promo_code = 'TEST-QA') test,
             CASE WHEN created_at < TIMESTAMP '%s' THEN 1 ELSE 2 END okres
      FROM surowe.orders""" % D.OKRES2)
    go = dict(con.execute(f"""SELECT CASE WHEN purchased_at < TIMESTAMP '{D.OKRES2}' THEN 1 ELSE 2 END, count(*)
                              FROM surowe.go_memberships GROUP BY 1""").fetchall())

    def miary(warunek, netto=False):
        z = dict(con.execute(f"SELECT okres, count(*) FROM zs WHERE {warunek} GROUP BY 1").fetchall())
        prz = dict(con.execute(f"SELECT okres, sum(zap{' - zw' if netto else ''}) FROM zs WHERE {warunek} GROUP BY 1").fetchall())
        nowi = dict(con.execute(f"""SELECT okres, count(*) FROM (SELECT user_id, arg_min(okres, (created_at, order_id)) okres
                                     FROM zs WHERE {warunek} GROUP BY 1) GROUP BY 1""").fetchall())
        w = lambda a: {"p1": a[1], "p2": a[2], "wzrost": 100 * (a[2] / a[1] - 1)}  # noqa: E731
        return {"nowi": w(nowi), "zamowienia": w(z), "przychod": w(prz), "go": w(go)}

    kroki = [("Dashboard (dane surowe)", "TRUE", False),
             ("Bez duplikatów zamówień", "NOT kopia", False),
             ("Bez duplikatów i bez kont testowych", "NOT kopia AND NOT test", False),
             ("Do tego przychód po odjęciu zwrotów", "NOT kopia AND NOT test", True)]
    mostek = {"kroki": [{"opis": o, "miary": miary(w, n)} for o, w, n in kroki]}
    # kontrola: te same liczby co w siatce A3
    s = pd.read_csv(SIATKA_A3)
    s = s[(s["statusy"] == "wszystkie") & (s["granice"] == "pl")]
    wz = {"nowi": "pierwsze_zamowienie", "zamowienia": "-", "go": "wszystkie"}
    roznice = 0
    for (opis, warunek, netto), krok in zip(kroki, mostek["kroki"]):
        dup = "z" if warunek == "TRUE" else "bez"
        test = "bez_kont" if "test" in warunek else "z"
        for m, v in krok["miary"].items():
            wariant = ("netto/bez_go" if netto else "zaplata/bez_go") if m == "przychod" else wz[m]
            ref = s[(s["duplikaty"] == dup) & (s["testy"] == test) & (s["miara"] == m) & (s["wariant"] == wariant)].iloc[0]
            roznice += int(abs(ref["p1"] - v["p1"]) > 0.01 or abs(ref["p2"] - v["p2"]) > 0.01)
    kontrole.append(("mostek: różnice wobec siatki A3 (komórki)", roznice, 0))

    # duplikaty: dzień po dniu w całym okresie
    dup = con.execute("""
      SELECT created_at::DATE dzien, count(*) FILTER (WHERE NOT kopia) zamowienia, count(*) FILTER (WHERE kopia) kopie
      FROM zs GROUP BY 1 ORDER BY 1""").df()
    dup["dzien"] = pd.to_datetime(dup["dzien"]).dt.date
    dni = (KONIEC - START).days + 1
    zam_d, kop_d = [0] * dni, [0] * dni
    for _, w in dup.iterrows():
        i = (w["dzien"] - START).days
        zam_d[i], kop_d[i] = int(w["zamowienia"]), int(w["kopie"])
    zk = dup[dup["kopie"] > 0]
    d_od, d_do = zk["dzien"].min(), zk["dzien"].max()
    udz = 100 * zk["kopie"] / zk["zamowienia"]
    kop = con.execute("""SELECT count(*), sum(zap), sum(zap - zw), min(okres), max(okres),
                                count(*) FILTER (WHERE test) FROM zs WHERE kopia""").fetchone()
    przed_po = con.execute(f"""SELECT count(*) FILTER (WHERE kopia) FROM zs
                               WHERE created_at::DATE IN (DATE '{d_od - dt.timedelta(days=1)}', DATE '{d_do + dt.timedelta(days=1)}')""").fetchone()[0]
    kontrole += [("duplikaty: liczba kopii", kop[0], 604)]
    duplikaty = {
        "od": d_od.isoformat(), "do": d_do.isoformat(), "kopie": kop[0], "zamowienia_d": zam_d, "kopie_d": kop_d,
        "zdania": [
            f"W eksporcie dwa razy zapisano {ile(kop[0], 'zamowienie')}, wszystkie od {data(d_od)} do {data(d_do)}. "
            f"W tych dniach zdublowanych jest od {proc(udz.min(), 0)} do {proc(udz.max(), 0)} zamówień dziennie. "
            f"Dzień przed oknem i dzień po nim: {ile(przed_po, 'zamowienie')} zdublowanych.",
            f"Wszystkie kopie są w okresie {O2_NAZWA}. Dodają mu {ile(kop[0], 'zamowienie')} i {zl(kop[1])} zapłat, "
            f"czyli {zl(kop[2])} po odjęciu zwrotów. W analityce każde z tych zamówień ma jeden krok płatności, "
            f"więc to wygląda na błąd eksportu, a nie na podwójne płatności. Zostawiamy jedną kopię.",
        ]}

    # zamówienia testowe
    t = con.execute("""
      SELECT count(DISTINCT user_id) konta, count(*) zam, count(*) FILTER (WHERE promo_code = 'TEST-QA') z_kodem,
             count(*) FILTER (WHERE coalesce(promo_code, '') <> 'TEST-QA') bez_kodu,
             count(*) FILTER (WHERE duration_min = 1) minuta,
             count(*) FILTER (WHERE specialization = 'internista') internista,
             count(*) FILTER (WHERE okres = 1) o1, count(*) FILTER (WHERE okres = 2) o2,
             sum(zap) zap, sum(zw) zw, count(*) FILTER (WHERE status IN ('completed', 'refunded')) odbyte,
             count(*) FILTER (WHERE status = 'refunded' AND zw = zap AND coalesce(promo_code, '') <> 'TEST-QA') bez_kodu_zwrocone
      FROM zs WHERE test AND NOT kopia""").df().iloc[0]
    minuta_poza = con.execute("SELECT count(*) FROM zs WHERE duration_min = 1 AND NOT test").fetchone()[0]
    najkrotsza = con.execute("SELECT min(duration_min) FROM zs WHERE NOT test AND duration_min IS NOT NULL").fetchone()[0]
    kw = con.execute("""SELECT strftime(date_trunc('quarter', created_at), '%Y-%m') kw, count(*) n FROM zs
                        WHERE test AND NOT kopia GROUP BY 1 ORDER BY 1""").df()
    kontrole += [("testy: konta", t["konta"], 22), ("testy: zamówienia", t["zam"], 2071), ("testy: bez kodu", t["bez_kodu"], 290)]
    koszt_lek = 25 * t["odbyte"]
    testy = {
        "kwartaly": [{"kw": w["kw"], "n": int(w["n"])} for _, w in kw.iterrows()],
        "zdania": [
            f"Zamówienia testowe: {ile(t['zam'], 'zamowienie')} z {liczba(t['konta'])} kont. Kod TEST-QA ma "
            f"{ile(t['z_kodem'], 'zamowienie')}. Pozostałe {ile(t['bez_kodu'], 'zamowienie')} nie ma kodu"
            + (", ale każde jest zapłacone w pełni i w całości zwrócone" if t['bez_kodu_zwrocone'] == t['bez_kodu']
               else f", a {ile(t['bez_kodu_zwrocone'], 'zamowienie')} z nich jest zapłacone w pełni i w całości zwrócone")
            + ", czyli wygląda na test procesu zwrotu. Filtr po samym kodzie by ich nie złapał.",
            f"Drugi, niezależny podpis: wszystkie trwają dokładnie 1 minutę ({liczba(t['minuta'])} z {liczba(t['zam'])}), "
            f"a taki czas nie występuje u żadnego innego pacjenta ({ile(minuta_poza, 'zamowienie')}; najkrótsza prawdziwa "
            f"wizyta trwa {ile(najkrotsza, 'minuta')}).",
            f"Testów przybywa: {ile(t['o1'], 'zamowienie')} w okresie {O1_NAZWA} i {ile(t['o2'], 'zamowienie')} w okresie {O2_NAZWA}. "
            f"Zawyżały więc wzrost zamówień. Wyłączamy te konta ze wszystkiego: zamówień, pacjentów, przychodu, sesji i lejka.",
            f"Pieniądze: {zl(t['zap'])} zapłat i {zl(t['zw'])} zwrotów. Gdyby lekarz dostawał 25 zł za każdą taką "
            f"wizytę, koszt wyniósłby {zl(koszt_lek)}. Czy dostawał, z danych nie wiemy, więc to idzie na listę niewiadomych.",
        ]}

    # godzina bez danych
    con.execute("""
      CREATE TEMP TABLE godziny AS
      WITH h AS (SELECT unnest(generate_series(TIMESTAMP '2024-10-01 00:00', TIMESTAMP '2026-09-30 23:00', INTERVAL 1 HOUR)) g)
      SELECT h.g, hour(h.g) godz, coalesce(s.n, 0) sesje, coalesce(o.n, 0) zamowienia
      FROM h
      LEFT JOIN (SELECT date_trunc('hour', started_at_pl) g, count(*) n FROM surowe.sessions GROUP BY 1) s USING (g)
      LEFT JOIN (SELECT date_trunc('hour', created_at) g, count(*) n FROM zs WHERE NOT kopia GROUP BY 1) o USING (g)""")
    luka = con.execute("""
      WITH w AS (SELECT *, median(sesje) OVER (PARTITION BY godz ORDER BY g ROWS BETWEEN 7 PRECEDING AND 7 FOLLOWING) ms
                 FROM godziny)
      SELECT g, sesje, ms, zamowienia FROM w WHERE ms >= 10 ORDER BY sesje / ms LIMIT 1""").fetchone()
    kontrole += [("godzina bez danych: sesje", luka[1], 1)]
    godzina = {"od": luka[0].isoformat(), "do": (luka[0] + dt.timedelta(hours=1)).isoformat(),
               "zdanie": f"{data(luka[0])} od {luka[0]:%H:%M} do {(luka[0] + dt.timedelta(hours=1)):%H:%M} jest "
                         f"{liczba(luka[1])} {'sesja' if luka[1] == 1 else 'sesji'} zamiast typowych {liczba(luka[2])} (mediana tej samej godziny w 15 dniach "
                         f"wokół) i {ile(luka[3], 'zamowienie')}. To jedyna taka godzina w dwóch latach. Wpływ na wyniki "
                         f"jest pomijalny, ale to luka w zbieraniu danych."}

    # drobne niespójności
    psych = con.execute("""SELECT count(*) FROM zs WHERE NOT kopia AND NOT test AND specialization = 'psycholog'
                           AND visit_purpose = 'e_recepta'""").fetchone()[0]
    go_bez = con.execute("""
      WITH a AS (SELECT z.order_id, z.discount_type,
                        max(CASE WHEN g.purchased_at <= z.created_at AND z.created_at::DATE <= g.valid_until THEN 1 ELSE 0 END) aktywne
                 FROM zs z LEFT JOIN surowe.go_memberships g ON g.user_id = z.user_id
                 WHERE NOT z.kopia AND NOT z.test GROUP BY 1, 2)
      SELECT count(*) FROM a WHERE aktywne = 1 AND discount_type = 'none'""").fetchone()[0]
    pol = con.execute("""SELECT count(*) FILTER (WHERE landing_page = '/polecenie' AND coalesce(utm_source, '') <> 'polecenie'),
                                count(*) FILTER (WHERE utm_source = 'polecenie' AND landing_page <> '/polecenie')
                         FROM surowe.sessions""").fetchone()
    kontrole += [("psycholog + e-recepta", psych, 24), ("TelemediGO aktywne bez zniżki", go_bez, 1)]
    drobne = [
        f"„Psycholog + e-recepta”: {ile(psych, 'zamowienie')}. Psycholog nie jest lekarzem i nie wystawia recept, "
        f"więc to wartość nierealna.",
        f"Mimo aktywnego TelemediGO bez zniżki zapłacono {ile(go_bez, 'zamowienie')}.",
        f"Program poleceń: na stronę /polecenie wchodzi z innym źródłem (bezpośrednio, z Google albo z Meta) "
        f"{ile(pol[0], 'sesja')}, a źródło „polecenie” z inną stroną wejścia ma {ile(pol[1], 'sesja')}. Ma to "
        f"znaczenie przy przypisywaniu źródła pacjenta.",
    ]

    # co jest czyste
    zgodne = con.execute("""
      SELECT count(*), count(*) FILTER (WHERE EXISTS (SELECT 1 FROM surowe.events e WHERE e.session_id = o.session_id
                         AND e.event_name = 'payment_succeeded' AND e.event_at_pl = o.created_at))
      FROM (SELECT DISTINCT order_id, session_id, created_at FROM surowe.orders) o""").fetchone()
    zgodne_go = con.execute("""
      SELECT count(*), count(*) FILTER (WHERE EXISTS (SELECT 1 FROM surowe.events e WHERE e.session_id = g.session_id
                         AND e.event_name = 'payment_succeeded' AND e.event_at_pl = g.purchased_at))
      FROM surowe.go_memberships g""").fetchone()
    klik = con.execute("""
      WITH k AS (SELECT utm_source, date_trunc('quarter', date) kw, sum(clicks) klik FROM surowe.marketing_spend GROUP BY 1, 2),
           s AS (SELECT utm_source, date_trunc('quarter', dzien_pl) kw, count(*) ses FROM surowe.sessions
                 WHERE utm_campaign IN (SELECT DISTINCT utm_campaign FROM surowe.marketing_spend) GROUP BY 1, 2)
      SELECT k.utm_source, min(ses / klik), max(ses / klik) FROM k JOIN s USING (utm_source, kw) GROUP BY 1 ORDER BY 1""").fetchall()
    dupl_inne = con.execute("""
      SELECT (SELECT count(*) - count(DISTINCT session_id) FROM surowe.sessions),
             (SELECT count(*) - count(DISTINCT (session_id, event_name)) FROM surowe.events),
             (SELECT count(*) - count(DISTINCT user_id) FROM surowe.users),
             (SELECT count(*) - count(DISTINCT membership_id) FROM surowe.go_memberships),
             (SELECT count(*) - count(DISTINCT (date, utm_source, utm_medium, utm_campaign)) FROM surowe.marketing_spend)""").fetchone()
    kolejnosc = con.execute("""
      WITH e AS (SELECT session_id, max((event_name = 'service_selected')::INT) k1, max((event_name = 'slot_selected')::INT) k2,
                        max((event_name = 'account_completed')::INT) k3, max((event_name = 'payment_started')::INT) k4,
                        max((event_name = 'payment_succeeded')::INT) k5 FROM surowe.events GROUP BY 1)
      SELECT count(*) FILTER (WHERE NOT (k1 >= k2 AND k2 >= k3 AND k3 >= k4 AND k4 >= k5)
                                AND NOT (k1 + k2 + k3 = 0 AND k4 = 1)
                                AND NOT (k1 + k2 + k4 + k5 = 0 AND k3 = 1)) poza_kolejnoscia,
             count(*) FILTER (WHERE k1 + k2 + k3 = 0 AND k4 = 1) samo_go,
             count(*) FILTER (WHERE k1 + k2 + k4 + k5 = 0 AND k3 = 1) samo_konto
      FROM e""").fetchone()
    tozs = con.execute("""
      SELECT (SELECT count(*) FROM (SELECT visitor_id FROM surowe.sessions WHERE user_id IS NOT NULL
                                    GROUP BY 1 HAVING count(DISTINCT user_id) > 1)),
             (SELECT count(*) FROM (SELECT user_id FROM surowe.sessions WHERE user_id IS NOT NULL
                                    GROUP BY 1 HAVING count(DISTINCT visitor_id) > 1)),
             (SELECT count(*) FROM surowe.users),
             (SELECT max(n) FROM (SELECT count(DISTINCT visitor_id) n FROM surowe.sessions WHERE user_id IS NOT NULL GROUP BY user_id))
      """).fetchone()
    wart = con.execute("""SELECT min(duration_min), max(duration_min) FROM czyste.orders WHERE duration_min IS NOT NULL""").fetchone()
    nazwy_zr = {"google": "Google Ads", "meta": "Meta", "tiktok": "TikTok"}
    czyste_l = [
        f"Czas płatności: {liczba(zgodne[1])} z {liczba(zgodne[0])} zamówień i {liczba(zgodne_go[1])} z "
        f"{liczba(zgodne_go[0])} zakupów TelemediGO ma krok płatności w analityce co do sekundy po przeliczeniu z UTC na "
        f"czas polski. Zmiana czasu jest obsłużona poprawnie.",
        "Sesje na kliknięcie są stałe w każdym kwartale: " + ", ".join(
            f"{nazwy_zr.get(z, z)} " + (f"od {liczba(a, 2)} do {liczba(b, 2)}" if round(a, 2) != round(b, 2) else liczba(a, 2))
            for z, a, b in klik) +
        ". Nie ma dni z kosztem bez sesji ani sesji z kampanii płatnej bez kosztu.",
        f"Duplikaty w pozostałych tabelach: sesje {liczba(dupl_inne[0])}, kroki lejka {liczba(dupl_inne[1])}, konta "
        f"{liczba(dupl_inne[2])}, TelemediGO {liczba(dupl_inne[3])}, wydatki na kampanie {liczba(dupl_inne[4])}.",
        f"Kroki lejka idą zawsze po kolei: {liczba(kolejnosc[0])} sesji ma krok bez poprzedniego. Jedyne wyjątki "
        f"zgodne z opisem danych to {ile(kolejnosc[1], 'zakup')} samego TelemediGO (tylko kroki płatności) i "
        f"{ile(kolejnosc[2], 'sesja')} kont testowych z samym założeniem konta.",
        ("Tożsamość: żadna przeglądarka nie jest dzielona przez dwa konta. " if tozs[0] == 0 else
         f"Tożsamość: {ile(tozs[0], 'przegladarka')} dzieli więcej niż jedno konto. ") +
        f"Więcej niż jednej przeglądarki używa {proc(100 * tozs[1] / tozs[2])} kont ({liczba(tozs[1])} z "
        f"{liczba(tozs[2])}), najwięcej {ile(tozs[3], 'przegladarka')}.",
        f"Wartości realne: wizyty po oczyszczeniu trwają od {liczba(wart[0])} do {liczba(wart[1])} minut; ceny "
        f"katalogowe i zniżki TelemediGO zgadzają się z zasadami co do złotówki (raport A2).",
    ]
    kontrole += [("czas płatności zgodny: zamówienia", zgodne[0] - zgodne[1], 0),
                 ("czas płatności zgodny: TelemediGO", zgodne_go[0] - zgodne_go[1], 0),
                 ("kroki bez poprzedniego", kolejnosc[0], 0)]
    return mostek, {"mostek": mostek, "duplikaty": duplikaty, "testy": testy, "godzina": godzina,
                    "drobne": drobne, "czyste": czyste_l, "start": START.isoformat(), "dni": dni}


# ---------------------------------------------------------------- 4. zdarzenia

def zdarzenia(con, d, zd, lejek_nag, jak, kontrole, td, V2, Z2):
    lista = []
    dzs = lambda x: data(dt.date.fromisoformat(str(x)[:10]))  # noqa: E731
    s = lejek_nag["safari"]
    lista.append({
        "id": "safari_ios", "obszar": "lejek", "od": s["data"], "rodzaj": "awaria",
        "tytul": "Safari na iOS: gwałtownie spada skuteczność zakładania nowego konta",
        "co": "U osób, które jeszcze nie kupowały, krok logowania albo zakładania konta po wyborze terminu spada "
              "w Safari na iPhone'ach i iPadach i zostaje niski do końca danych. Gwałtownie spada skuteczność "
              "zakładania nowego konta (konta dalej powstają, ale rzadziej), a logowanie do istniejącego działa.",
        "ile": f"Z {proc(s['przed_proc'])} w 60 dniach przed awarią ({dzs(s['przed_od'])}–{dzs(s['przed_do'])}, "
               f"{ile(s['przed_k2'], 'sesja')} z wyborem terminu) do {proc(s['po60_proc'])} w 60 dniach po niej "
               f"({dzs(s['po60_od'])}–{dzs(s['po60_do'])}, {ile(s['po60_k2'], 'sesja')}). Pozostałe przeglądarki: "
               f"{proc(s['reszta_przed_proc'])} i {proc(s['reszta_po60_proc'])}. Szacunek: {liczba(s['utracone_od'])}–"
               f"{liczba(s['utracone_do'])} utraconych pierwszych zamówień w {liczba(s['dni_po'])} dniach do "
               f"{data(KONIEC)}, czyli {liczba(s['na30_od'])}–{liczba(s['na30_do'])} na 30 dni.",
        "skad": "Metoda wykrywania zmian w seriach dziennych (podział binarny) wskazała ten dzień. Sprawdzenie na bazie: "
                "spadek jest w głównych kanałach (TikTok ma za małą próbę do oceny), więc to nie zmiana struktury ruchu. "
                "Przyczyny w danych nie widać. "
                "Źródło: analiza/a5p_zdarzenia.py, sekcja 5; notatki/a5_pozyskanie.md, punkt 2.1.",
        "link": lejek_nag["naprawy"][0]["link"]})

    k = d[(d["podzial"] == "kampania") & (d["typ"] == "zwykla")]
    kan = d[(d["podzial"] == "kanal") & (d["typ"] == "zwykla") & (d["pacjent"] == "nie_kupowal")]

    def start_kampanii(kamp, tytul, id_, porownaj):
        x = k[(k["wartosc"] == kamp) & (k["sesje"] > 0)]
        od = x["dzien"].min()
        dni = (KONIEC - od).days + 1
        t = suma(k, od, KONIEC, wartosc=kamp)
        skoki = zd[(zd["podzial"] == "kampania") & (zd["wartosc"] == kamp) & (zd["rodzaj"] == "ruch")
                   & (zd["zmiana"] > 0)]["data"].tolist()
        por = []
        for nazwa, ramka, w in porownaj:
            p = suma(ramka, od, KONIEC, wartosc=w)
            por.append(f"{nazwa} {proc(100 * p['k5'] / p['sesje'], 2)} ({ile(p['sesje'], 'sesja')})")
        opis = (f"Średnio {liczba(t['sesje'] / dni, 1)} sesji i {liczba(t['k5'] / dni, 1)} płatności dziennie, konwersja "
               f"sesji do płatności {proc(100 * t['k5'] / t['sesje'], 2)}, razem {ile(t['k5'], 'zamowienie')} do "
               f"{data(KONIEC)}. Od tego samego dnia: " + ", ".join(por) + ".")
        if skoki:
            opis += " Ruch kampanii rośnie skokami: " + ", ".join(data(dt.date.fromisoformat(x)) for x in skoki) + "."
        lista.append({"id": id_, "obszar": "lejek", "od": od.isoformat(), "rodzaj": "start kampanii", "tytul": tytul,
                      "co": "Pierwszy dzień z sesjami i kosztem tej kampanii. Kampania przyprowadza głównie ruch "
                            "w przeglądarkach wbudowanych w aplikacje, który płaci rzadziej niż wyszukiwarka.",
                      "ile": opis,
                      "skad": "Pierwszy dzień z sesjami z tym kodem kampanii w analityce; ten sam dzień w wydatkach na "
                              "kampanie. Źródło: analiza/a5p_zdarzenia.py, sekcja 6; notatki/a5_pozyskanie.md, punkt 2.",
                      "link": f"#lejek?pac=nie_kupowal&podz=kampania&krok=k5&w={kamp},"
                              + ",".join(w for _, r, w in porownaj if r is nk)})
        return od

    nk = k[k["pacjent"] == "nie_kupowal"]
    start_kampanii("meta_prosp_l4_szybko", "Start kampanii Meta na L4 (meta_prosp_l4_szybko)", "start_meta_l4",
                   [("starsza kampania Meta", nk, "meta_prosp_lekarz_online"),
                    ("wyszukiwarka bezpłatna", kan, "wyszukiwarka_bezplatna"),
                    ("Google Ads na hasła ogólne", kan, "google_ads_ogolne")])
    start_kampanii("tt_prosp_l4_15min", "Start kampanii TikTok na L4 (tt_prosp_l4_15min)", "start_tiktok",
                   [("kampania Meta na L4", nk, "meta_prosp_l4_szybko"),
                    ("wyszukiwarka bezpłatna", kan, "wyszukiwarka_bezplatna")])

    # sprzedaż TelemediGO w newsletterze
    g = d[(d["podzial"] == "kampania") & (d["wartosc"] == "crm_go_upsell")]
    od_go = g[g["sesje"] > 0]["dzien"].min()
    tg = suma(g[g["typ"] == "samo_telemedigo"])
    zal = suma(g[g["typ"] == "zalogowana_od_wejscia"])
    zw = suma(g[g["typ"] == "zwykla"])
    wszystkie = tg["sesje"] + zal["sesje"] + zw["sesje"]
    kontrole.append(("sprzedaż TelemediGO: zakupy samego TelemediGO", int(tg["k5"]), 686))
    # dni z sesjami a dni kalendarzowe (a5p_zdarzenia.txt, sekcja 6: kolumna dni = liczba różnych dni z sesjami)
    dni_go = int(g[g["sesje"] > 0]["dzien"].nunique())
    dni_kal = (KONIEC - od_go).days + 1
    kontrole.append(("sprzedaż TelemediGO: dni z sesjami = a5p_zdarzenia.txt (sekcja 6)", dni_go,
                     Z2.r("a5p_zdarzenia.txt", r"crm_go_upsell\s+\d{4}-\d\d-\d\d\s+{N}")))
    dni_tekst = (f" Sesje z tej kampanii są w {liczba(dni_go)} dniach, a od pierwszego dnia ({data(od_go)}) do końca danych "
                 f"({data(KONIEC)}) mija {liczba(dni_kal)} dni kalendarzowych, bo newsletter nie wychodzi codziennie. Kampanie "
                 f"płatne mają sesje każdego dnia, więc u nich obie liczby są równe (Meta na L4: "
                 f"{liczba(V2['dni']['meta_prosp_l4_szybko'])} dni).")
    lista.append({
        "id": "start_go_upsell", "obszar": "lejek", "od": od_go.isoformat(), "rodzaj": "start kampanii",
        "tytul": "Start sprzedaży TelemediGO w newsletterze (crm_go_upsell)",
        "co": "Newsletter do pacjentów, którzy już kupowali, prowadzi na stronę /telemedigo. Pojawiają się zakupy "
              "samego TelemediGO, bez konsultacji.",
        "ile": f"{ile(tg['k5'], 'zakup')} samego TelemediGO do {data(KONIEC)}, czyli {proc(100 * tg['k5'] / wszystkie, 0)} "
               f"z {liczba(wszystkie)} wejść z tej kampanii. Pozostałe {liczba(zal['sesje'])} wejść to sesje zalogowane "
               f"od wejścia, bez zakupu." + dni_tekst,
        "skad": "Pierwszy dzień z sesjami z tym kodem kampanii. Źródło: analiza/a5p_lejek.py, sekcja 1; "
                "notatki/a5_pozyskanie.md, punkt 2.4.",
        "link": "#lejek?pac=wszyscy&podz=kampania&krok=sesje&typ=samo_telemedigo&w=crm_go_upsell"})

    # remarketing Meta: zmiana puli odbiorców
    con.execute("""
      CREATE TEMP TABLE ev AS
      SELECT session_id, max((event_name = 'service_selected')::INT) k1, max((event_name = 'account_completed')::INT) k3,
             max((event_name = 'payment_succeeded')::INT) k5
      FROM czyste.events GROUP BY 1""")
    con.execute("CREATE OR REPLACE TEMP TABLE przeg AS SELECT DISTINCT visitor_id, user_id FROM czyste.sessions WHERE user_id IS NOT NULL")
    con.execute("CREATE OR REPLACE TEMP TABLE pierwszy AS SELECT user_id, min(created_at) t FROM czyste.orders GROUP BY 1")
    con.execute("""
      CREATE TEMP TABLE rm AS
      SELECT s.session_id, s.visitor_id, s.dzien_pl, s.browser, coalesce(e.k1, 0) k1, coalesce(e.k5, 0) k5
      FROM czyste.sessions s
      LEFT JOIN ev e USING (session_id)
      LEFT JOIN przeg p ON p.visitor_id = s.visitor_id AND s.user_id IS NULL
      LEFT JOIN pierwszy pz ON pz.user_id = coalesce(s.user_id, p.user_id)
      WHERE NOT (s.user_id IS NOT NULL AND coalesce(e.k3, 0) = 0)
        AND s.session_id NOT IN (SELECT session_id FROM czyste.go_memberships WHERE order_id IS NULL)
        AND NOT coalesce(pz.t < s.started_at_pl, FALSE)
        AND s.utm_campaign = 'meta_rmkt_koszyk'""")
    kw = con.execute("""
      SELECT date_trunc('quarter', dzien_pl)::DATE kw, count(*) sesje, 100 * avg(k5) konw,
             100 * avg((browser IN ('Instagram', 'Facebook'))::INT) w_apl
      FROM rm GROUP BY 1 ORDER BY 1""").df()
    kw["kw"] = pd.to_datetime(kw["kw"]).dt.date
    q4 = kw[kw["kw"] == dt.date(2025, 10, 1)].iloc[0]
    q26 = kw[kw["kw"] >= dt.date(2026, 4, 1)]
    zrodla = con.execute(f"""
      WITH pierw AS (SELECT visitor_id, arg_min(CASE WHEN utm_campaign LIKE 'meta_prosp%' THEN 'meta_pozyskanie'
                                                     WHEN utm_source IN ('google', 'bing') THEN 'google_bing' ELSE 'inne' END,
                                                (started_at_utc, session_id)) zrodlo FROM czyste.sessions GROUP BY 1)
      SELECT p.zrodlo, CASE WHEN dzien_pl < DATE '{D.OKRES2}' THEN 1 WHEN dzien_pl >= DATE '2026-01-01' THEN 3 ELSE 2 END o,
             count(*) sesje, 100 * avg(k5) konw
      FROM rm JOIN pierw p USING (visitor_id) GROUP BY 1, 2""").df()
    od_2026 = dt.date(2026, 1, 1)   # granica okresu porównania w zapytaniu wyżej
    zz = lambda z, o: zrodla[(zrodla["zrodlo"] == z) & (zrodla["o"] == o)].iloc[0]  # noqa: E731
    det = zd[(zd["podzial"] == "kampania") & (zd["wartosc"] == "meta_rmkt_koszyk") & (zd["przejscie"] == "sesja_do_platn")].iloc[0]
    kontrole += [("remarketing: płatność na sesję IV kw. 2025 (%)", round(q4["konw"], 1), 28.2),
                 ("remarketing: udział w aplikacjach IV kw. 2025 (%)", round(q4["w_apl"], 1), 13.3)]
    lista.append({
        "id": "remarketing_meta", "obszar": "lejek", "od": od_2026.isoformat(), "rodzaj": "zmiana stopniowa",
        "tytul": "Remarketing Meta słabnie, bo zmienia się pula odbiorców",
        "co": "Remarketing wraca coraz częściej do osób, które pierwszy raz przyszły z Meta i TikToka, a rzadziej do osób "
              "z wyszukiwarki. Te osoby płacą rzadziej. W obrębie źródła pierwszej wizyty konwersja stoi.",
        "ile": f"Płatność na sesję u osób, które jeszcze nie kupowały: {proc(q4['konw'])} w IV kwartale 2025 "
               f"({ile(q4['sesje'], 'sesja')}), " + " i ".join(
                   f"{proc(w['konw'])} w {MIESIACE_RZ[(w['kw'].month - 1) // 3]} kwartale "
                   f"{w['kw'].year} ({ile(w['sesje'], 'sesja')})" for _, w in q26.iterrows()) +
               f". Udział przeglądarek w aplikacjach w tym ruchu rośnie z {proc(q4['w_apl'])} do "
               f"{zakres(q26['w_apl'].min(), q26['w_apl'].max(), 1)}. Osoby, które pierwszy raz przyszły z Google "
               f"albo Bing: {proc(zz('google_bing', 1)['konw'])} w okresie {O1_NAZWA} i {proc(zz('google_bing', 3)['konw'])} "
               f"od {data(od_2026)} do {data(KONIEC)}; z Meta (pozyskanie): {proc(zz('meta_pozyskanie', 1)['konw'])} i "
               f"{proc(zz('meta_pozyskanie', 3)['konw'])}.",
        "skad": f"Metoda wykrywania zmian wskazała {data(dt.date.fromisoformat(det['data']))} jako dzień zmiany poziomu "
                f"płatności na sesję ({proc(det['przed'])} → {proc(det['po'])}), ale zmiana narasta od {data(od_2026)}. "
                f"Źródło: analiza/a5p_zdarzenia.py, sekcje 5h i 5i; notatki/a5_pozyskanie.md, punkt 2.5.",
        "link": "#lejek?pac=nie_kupowal&podz=kampania&krok=k5&w=meta_rmkt_koszyk"})

    lista.append(td["zdarzenie_marka"])

    du = jak["duplikaty"]
    lista.append({
        "id": "duplikaty", "obszar": "jakosc", "od": du["od"], "do": du["do"], "rodzaj": "błąd danych",
        "tytul": "Duplikaty zamówień w eksporcie", "co": du["zdania"][0], "ile": du["zdania"][1],
        "skad": "Dwie identyczne kopie zamówienia w sąsiednich liniach pliku zamówień. Źródło: analiza/a2_jakosc.py; "
                "czyszczenie: analiza/a2_czyste.py.", "link": "#jakosc"})
    gz = jak["godzina"]
    lista.append({
        "id": "luka_godzina", "obszar": "jakosc", "od": gz["od"][:10], "rodzaj": "luka w danych",
        "tytul": "Godzina bez danych", "co": gz["zdanie"], "ile": "",
        "skad": "Liczba sesji w każdej godzinie wobec mediany tej samej godziny w 15 dniach wokół. "
                "Źródło: analiza/a2_jakosc.py, sekcja o lukach.", "link": "#jakosc"})
    lista.sort(key=lambda z: z["od"])

    # wszystkie zmiany wykryte automatycznie w lejku (surowy wynik metody)
    kol = ["rodzaj", "podzial", "wartosc", "przejscie", "data", "przed", "po", "zmiana", "dni_przed", "dni_po",
           "zamowienia_na_30_dni"]
    w = zd[kol].astype(object).where(zd[kol].notna(), None)
    wykryte = {"kolumny": kol, "wiersze": w.values.tolist()}
    obszary = [{"id": "lejek", "puste": ""},
               {"id": "retencja", "puste": "Zdarzenia z analizy kohort i powrotów dojdą po przeglądzie części retencji."},
               {"id": "obsluga", "puste": "Zdarzenia z przebiegu wizyt (punktualność, zwroty, oceny) dojdą po przeglądzie "
                                          "części retencji."},
               {"id": "jakosc", "puste": ""}]
    return {"lista": lista, "wykryte": wykryte, "obszary": obszary}


# ---------------------------------------------------------------- 5. kohorty (pacjent po pacjencie)

ZNAKI = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
A5R_ZDARZENIA = os.path.join(WYNIKI, "a5r_zdarzenia.csv")
A5E_KAMPANIE = os.path.join(WYNIKI, "a5e_kampanie.csv")
OKNA_KOH = (30, 60, 90, 180)
KAT_KOH = ["kanal", "kampania", "kanal_z2", "kampania_z2", "urzadzenie", "przegladarka", "usluga", "znizka", "go0",
           "status1", "koszyk", "pora"]
ETYKIETY.update({
    "usluga": {"internista_l4": "Internista: L4", "internista_e_recepta": "Internista: e-recepta",
               "internista_konsultacja": "Internista: konsultacja", "internista_skierowanie": "Internista: skierowanie",
               "pediatra": "Pediatra", "psychiatra": "Psychiatra", "inny_specjalista": "Inny specjalista"},
    "znizka": {"brak": "Bez zniżki", "TelemediGO": "Zniżka TelemediGO"},
    "go0": {"tak": "Kupił TelemediGO przy pierwszym zakupie", "nie": "Bez zakupu TelemediGO przy pierwszym zakupie"},
    "status1": {"completed": "Odbyta", "refunded": "Odbyta, zwrot po wizycie", "cancelled": "Anulowana przed wizytą",
                "no_show": "Pacjent nie odebrał"},
    "koszyk": {"a_do_5_min": "Do 5 minut po terminie", "b_5_15_min": "Ponad 5 do 15 minut",
               "c_15_30_min": "Ponad 15 do 30 minut", "d_ponad_30_min": "Ponad 30 minut",
               "brak_wizyty": "Brak wizyty (anulowana, nieodebrana)"},
    "pora": {"a_rano_6_11": "Rano (6–11)", "b_poludnie_12_15": "Południe (12–15)", "c_wieczor_16_23": "Wieczór (16–23)",
             "d_noc_0_5": "Noc (0–5)"},
    "spec": {"internista": "Internista", "pediatra": "Pediatra", "psychiatra": "Psychiatra", "inny": "Inni specjaliści"},
    "cel": {"l4": "L4", "e_recepta": "E-recepta", "konsultacja": "Konsultacja", "skierowanie": "Skierowanie"},
    "grupa_ek": {"1_nowe_kampanie_L4": "Nowe kampanie na L4 (Meta i TikTok)", "2_pozostale_platne": "Pozostałe kampanie płatne",
                 "3_afiliacja_ranking": "Afiliacja (ranking lekarzy)", "4_bezplatne": "Kanały bezpłatne"},
    "nowe_kampanie": list(RP.NOWE),
})
ETYKIETY["kanal_z2"] = ETYKIETY["kanal"]
ETYKIETY["kampania_z2"] = ETYKIETY["kampania"]


def koduj(seria):
    """Kategorie jako napis: jeden znak na pacjenta, słownik wartości od najczęstszej."""
    wart = seria.value_counts().index.tolist()
    assert len(wart) <= len(ZNAKI), seria.name
    mapa = {w: ZNAKI[i] for i, w in enumerate(wart)}
    return [str(w) for w in wart], "".join(mapa[w] for w in seria)


def stopy_z_pacjentow(p, n, kol=None):
    """Powrót (albo średnia kolumny `kol`) w oknie n na tych samych dniach kalendarzowych (ZALOZENIA 27)."""
    g1, g2 = D.granice_por(n)
    a, b = p[(p["okres"] == 1) & (p["d0"] <= g1)], p[(p["okres"] == 2) & (p["d0"] <= g2)]
    if kol:
        return a[kol].mean(), b[kol].mean(), len(a), len(b)
    f = lambda x: 100 * ((x["dni_R2"] >= 0) & (x["dni_R2"] <= n)).mean()  # noqa: E731
    return f(a), f(b), len(a), len(b)


def kohorty(con, kontrole):
    D.zbuduj_zrodla(con)
    D.zbuduj_ekonomie(con)
    con.execute(f"""
      CREATE TEMP TABLE b_pac AS
      WITH z AS (SELECT z.*, epoch(z.started_at - z.scheduled_at) / 60.0 op, hour(z.scheduled_at) h,
                        EXISTS (SELECT 1 FROM czyste.go_memberships g WHERE g.order_id = z.order_id) kupil_go
                 FROM zam z WHERE z.nr = 1),
           m AS (SELECT user_id, sum(marza) FILTER (WHERE dni <= 30) m30, sum(marza) FILTER (WHERE dni <= 60) m60,
                        sum(marza) FILTER (WHERE dni <= 90) m90, sum(marza) FILTER (WHERE dni <= 180) m180
                 FROM ek GROUP BY 1)
      SELECT p.user_id, p.d0, p.okres, coalesce(p.dni_R2, -1) dni_R2, r.kanal, r.kampania, r.kanal_z2, r.kampania_z2,
             s.device urzadzenie, s.browser przegladarka, {RS.USLUGA} usluga, {RS.ZNIZKA} znizka,
             CASE WHEN z.kupil_go THEN 'tak' ELSE 'nie' END go0, z.status status1, {RP.KOSZYK} koszyk, {RP.PORA} pora,
             coalesce(m.m30, 0) m30, coalesce(m.m60, 0) m60, coalesce(m.m90, 0) m90, coalesce(m.m180, 0) m180
      FROM powr p JOIN zrodlo r USING (user_id) JOIN z ON z.user_id = p.user_id
      JOIN czyste.sessions s ON s.session_id = z.session_id
      LEFT JOIN m ON m.user_id = p.user_id
      ORDER BY p.d0, p.user_id""")
    p = con.execute("SELECT * EXCLUDE (user_id) FROM b_pac").df()
    p["d0"] = pd.to_datetime(p["d0"]).dt.date
    for k in ("m30", "m60", "m90", "m180"):
        p[k] = (p[k] * 10).round().astype(int) / 10      # zapis w dziesiątych częściach złotówki
    dane = {"n": len(p), "d": [(x - START).days for x in p["d0"]], "r": [int(x) for x in p["dni_R2"]],
            "okna": list(OKNA_KOH), "kat": {}, "wart": {}}
    for k in ("m30", "m60", "m90", "m180"):
        dane[k] = [int(round(x * 10)) for x in p[k]]
    for k in KAT_KOH:
        dane["wart"][k], dane["kat"][k] = koduj(p[k].astype(str))

    # kontrola: liczby części retencji (ZNALEZISKA, A5 retencja) z danych zapisanych dla strony
    ocz = {30: (11.0, 7.8, 14984, 22646), 60: (19.1, 13.7, 13941, 20823), 90: (23.9, 17.4, 12867, 18924),
           180: (27.5, 22.2, 9125, 12591)}
    for n, (e1, e2, n1, n2) in ocz.items():
        a, b, la, lb = stopy_z_pacjentow(p, n)
        kontrole += [(f"kohorty: powrót {n} dni, okres 1 (%) / pacjenci", f"{a:.1f} / {la}", f"{e1:.1f} / {n1}"),
                     (f"kohorty: powrót {n} dni, okres 2 (%) / pacjenci", f"{b:.1f} / {lb}", f"{e2:.1f} / {n2}")]
    for n, (e1, e2) in {30: (55.9, 49.9), 90: (66.6, 58.3), 180: (75.5, 67.7)}.items():
        a, b, _, _ = stopy_z_pacjentow(p, n, f"m{n}")
        kontrole.append((f"kohorty: marża na pacjenta {n} dni, okres 1 / okres 2 (zł)", f"{a:.1f} / {b:.1f}", f"{e1:.1f} / {e2:.1f}"))

    zd = []
    for n in OKNA_KOH:
        a, b, la, lb = stopy_z_pacjentow(p, n)
        zd.append(f"w {n} dniach {proc(b)} ({ile(lb, 'pacjent')}) wobec {proc(a)} ({ile(la, 'pacjent')})")
    m90 = stopy_z_pacjentow(p, 90, "m90")
    m180 = stopy_z_pacjentow(p, 180, "m180")
    udzial_nowych = B2.udzial_nowych_w_spadku()   # a5r_struktura.txt: przyjęta reguła, sesja płatności
    zdania = [
        "Powrót nowych pacjentów spada w każdym oknie. Okres " + O2_NAZWA + " wobec " + O1_NAZWA +
        ", te same dni kalendarzowe, tylko kohorty z pełnym oknem: " + "; ".join(zd) + ".",
        f"Marża na pacjenta przed kosztem pozyskania (przychód z konsultacji po zwrotach, TelemediGO, minus koszt "
        f"lekarza): w 90 dniach {liczba(m90[1], 1)} zł wobec {liczba(m90[0], 1)} zł, w 180 dniach "
        f"{liczba(m180[1], 1)} zł wobec {liczba(m180[0], 1)} zł.",
        f"Obecność pacjentów dwóch nowych kampanii na L4 odpowiada opisowo za około "
        f"{zakres(min(udzial_nowych), max(udzial_nowych), 0)} spadku powrotu w 90 dniach, zależnie od reguły źródła, "
        f"ale w kampaniach działających w obu latach też jest spadek, którego sprawdzone cechy nie tłumaczą. Dlatego obie "
        f"reguły są do wyboru w filtrach.",
    ]
    return p, dane, zdania


# ---------------------------------------------------------------- 6. po zakupie

def tablice_dzienne(df, klucze, kol_dnia, miary):
    """Grupy `klucze` → tablice dzienne miar (indeks dnia od START). Puste tablice pomijamy."""
    dni = (KONIEC - START).days + 1
    df = df[(df[kol_dnia] >= START) & (df[kol_dnia] <= KONIEC)]
    wyn = []
    for kl, g in df.groupby(klucze, sort=True):
        kl = kl if isinstance(kl, tuple) else (kl,)
        s = {k: (v.item() if hasattr(v, "item") else v) for k, v in zip(klucze, kl)}
        for m in miary:
            tab = [0] * dni
            for dz, v in zip(g[kol_dnia], g[m]):
                tab[(dz - START).days] = round(float(v), 2) if not float(v).is_integer() else int(v)
            if any(tab):
                s[m] = tab
        wyn.append(s)
    return wyn


def po_zakupie(con, kontrole, td):
    con.execute(f"""
      CREATE TEMP TABLE b_wiz AS
      SELECT z.order_id, z.nr, z.created_at::DATE dz, z.scheduled_at::DATE dt, z.status, z.visit_purpose cel, z.rating,
             CASE WHEN z.specialization IN ('internista', 'pediatra', 'psychiatra') THEN z.specialization ELSE 'inny' END spec,
             epoch(z.started_at - z.scheduled_at) / 60.0 op, hour(z.scheduled_at) h, z.started_at,
             r.kampania IN {tuple(RP.NOWE)} nowa, z.refund_amount::DOUBLE zw, ({D.KOSZT_LEKARZA})::DOUBLE kl,
             CASE WHEN z.created_at < TIMESTAMP '{D.OKRES2}' THEN 1 ELSE 2 END okres
      FROM zam z JOIN zrodlo r USING (user_id)""")
    # punktualność: dzień terminu, tylko wizyty odbyte (ZALOZENIA 37)
    pt = con.execute(f"""
      SELECT dt, spec, {RP.PORA} pora, nowa, count(*) n, count(*) FILTER (WHERE op > 15) p15, count(*) FILTER (WHERE op > 30) p30
      FROM b_wiz WHERE status IN ('completed', 'refunded') GROUP BY ALL""").df()
    pt["dt"] = pd.to_datetime(pt["dt"]).dt.date
    # kontrola: internista rano, pacjenci spoza nowych kampanii, miesiące (ZNALEZISKA, A5 retencja)
    x = pt[(pt["spec"] == "internista") & (pt["pora"] == "a_rano_6_11") & (~pt["nowa"])].copy()
    x["m"] = [f"{d:%Y-%m}" for d in x["dt"]]
    mies = x.groupby("m")[["n", "p15"]].sum()
    mies["proc"] = 100 * mies["p15"] / mies["n"]
    for m, e in (("2025-11", 15.7), ("2025-12", 29.7), ("2026-01", 42.6), ("2026-02", 49.4)):
        kontrole.append((f"po zakupie: internista rano ponad 15 min, spoza nowych kampanii, {m} (%)", round(mies.loc[m, "proc"], 1), e))
    przed = mies[(mies.index >= f"{START:%Y-%m}") & (mies.index <= "2025-10")]["proc"]
    po = mies[(mies.index >= "2026-02") & (mies.index <= f"{KONIEC:%Y-%m}")]["proc"]
    reszta = pt[(pt["spec"] == "internista") & (pt["pora"] != "a_rano_6_11") & (~pt["nowa"])].copy()
    reszta["o"] = [1 if d < OKRES2 else 2 for d in reszta["dt"]]
    ro = reszta.groupby("o")[["n", "p15"]].sum()
    zdania_p = [
        td["po_blok"],
        f"Wizyty z terminem 6:00–11:59, które zaczęły się ponad 15 minut po terminie, u pacjentów spoza nowych kampanii: {zakres(przed.min(), przed.max(), 1)} miesięcznie do X 2025, "
        f"{proc(mies.loc['2025-11', 'proc'])} w XI 2025 ({ile(mies.loc['2025-11', 'n'], 'wizyta')}), "
        f"{proc(mies.loc['2025-12', 'proc'])} w XII 2025, {proc(mies.loc['2026-01', 'proc'])} w I 2026 i "
        f"{zakres(po.min(), po.max(), 1)} od II do IX 2026.",
        f"U internisty w innych porach: {proc(100 * ro.loc[1, 'p15'] / ro.loc[1, 'n'])} wizyt spóźnionych ponad 15 minut "
        f"w okresie {O1_NAZWA} ({ile(ro.loc[1, 'n'], 'wizyta')}) i {proc(100 * ro.loc[2, 'p15'] / ro.loc[2, 'n'])} w okresie "
        f"{O2_NAZWA} ({ile(ro.loc[2, 'n'], 'wizyta')}).",
        "Długość wizyty i czas od zapłaty do terminu się nie zmieniają.",
    ]
    punkt = tablice_dzienne(pt, ["spec", "pora", "nowa"], "dt", ["n", "p15", "p30"])

    # przepustowość poranka (a5r_punktualnosc.py, sekcje 3f–3g; odczytanie przyjęte przez Kubę po STOP 2 retencji)
    dz = con.execute(f"""
      SELECT dt dzien, CASE WHEN dt < DATE '{D.OKRES2}' THEN 1 ELSE 2 END okres, strftime(dt, '%Y-%m') miesiac,
             count(*) FILTER (WHERE status <> 'cancelled') ruch, count(op) odbyte, count(*) FILTER (WHERE op > 15) spoznione,
             count(op) FILTER (WHERE NOT nowa) odbyte_stare, count(*) FILTER (WHERE op > 15 AND NOT nowa) spoznione_stare
      FROM b_wiz WHERE spec = 'internista' AND {RP.PORA} = 'a_rano_6_11' AND dt <= DATE '{D.KONIEC}'
      GROUP BY ALL""").df()
    przedz = [0, 8, 12, 16, 20, 24, 28, 32, 40, 1000]
    etyk = ["do 8", "9–12", "13–16", "17–20", "21–24", "25–28", "29–32", "33–40", "41 i więcej"]
    dz["przedzial"] = pd.cut(dz["ruch"], przedz, labels=etyk)
    rt = dz.groupby(["przedzial", "okres"], observed=True).agg(
        dni=("dzien", "size"), odbyte=("odbyte", "sum"), spoznione=("spoznione", "sum"),
        odbyte_stare=("odbyte_stare", "sum"), spoznione_stare=("spoznione_stare", "sum")).reset_index()
    wsp = rt.pivot(index="przedzial", columns="okres", values=["odbyte", "spoznione"]).dropna()
    waga = wsp[("odbyte", 1)] + wsp[("odbyte", 2)]
    roz = wsp[("spoznione", 2)] / wsp[("odbyte", 2)] - wsp[("spoznione", 1)] / wsp[("odbyte", 1)]
    rozn = 100 * (roz * waga).sum() / waga.sum()
    kontrole.append(("po zakupie: przy tym samym porannym ruchu, różnica (pp) / przedziały / wizyty",
                     f"{rozn:.1f} / {len(wsp)} / {int(waga.sum())}", "26.4 / 5 / 9979"))
    # remisy w ruchu rozstrzyga data (a5r_punktualnosc.py nie ustalał kolejności wierszy, więc jego tercyle mogą się
    # nieznacznie różnić; kontrola z tolerancją 0,5 punktu procentowego)
    dz = dz.sort_values("dzien").reset_index(drop=True)
    dz["tercyl"] = dz.groupby("miesiac")["ruch"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=[1, 2, 3]))
    tc = dz.groupby(["okres", "tercyl"], observed=True)[["odbyte", "spoznione"]].sum()
    tc["proc"] = 100 * tc["spoznione"] / tc["odbyte"]
    ref = [5.8, 5.9, 6.1, 42.2, 43.6, 43.5]
    kontrole.append((f"po zakupie: tercyle ruchu w miesiącu w granicy 0,5 pp ({' '.join(f'{v:.1f}' for v in tc['proc'])})",
                     "tak" if max(abs(a - b) for a, b in zip(tc["proc"], ref)) <= 0.5 else "nie", "tak"))
    r1 = rt[rt["okres"] == 1].copy()
    r1["proc"] = 100 * r1["spoznione"] / r1["odbyte"]
    przyk = rt[rt["przedzial"] == "17–20"].set_index("okres")
    med = dz.groupby("okres")["ruch"].median()
    zdania_ruch = [
        f"Przy tym samym porannym ruchu opóźnień jest teraz dużo więcej niż rok wcześniej. Średnio o {pp(rozn)} więcej "
        f"porannych wizyt u internisty zaczyna się ponad 15 minut po terminie ({len(wsp)} przedziałów ruchu obecnych w obu "
        f"okresach, {ile(waga.sum(), 'wizyta')}). Na przykład w dni z 17–20 porannymi wizytami: "
        f"{proc(100 * przyk.loc[1, 'spoznione'] / przyk.loc[1, 'odbyte'])} ({liczba(przyk.loc[1, 'dni'])} dni) w okresie "
        f"{O1_NAZWA} wobec {proc(100 * przyk.loc[2, 'spoznione'] / przyk.loc[2, 'odbyte'])} ({liczba(przyk.loc[2, 'dni'])} dni) "
        f"w okresie {O2_NAZWA}.",
        f"W okresie {O1_NAZWA} opóźnienia nie zależą od ruchu ({zakres(r1['proc'].min(), r1['proc'].max(), 1)} w każdym "
        f"przedziale). W obrębie miesiąca dni z większym ruchem prawie nie mają więcej opóźnień: w tercylach dni według "
        f"ruchu {', '.join(proc(v) for v in tc.loc[1, 'proc'])} w okresie {O1_NAZWA} i "
        f"{', '.join(proc(v) for v in tc.loc[2, 'proc'])} w okresie {O2_NAZWA}. Mediana ruchu porannego to "
        f"{liczba(med.loc[1])} wizyt na dzień w okresie {O1_NAZWA} i {liczba(med.loc[2])} w okresie {O2_NAZWA}.",
        td["po_poranek"],
    ]
    ruch_tab = [{k: (v.item() if hasattr(v, "item") else v) for k, v in r.items()} for r in rt.astype({"przedzial": str}).to_dict("records")]

    # zwroty i statusy: dzień płatności
    zw = con.execute("""
      SELECT dz, cel, nowa, nr = 1 pierwsze, count(*) wszystkie, count(*) FILTER (WHERE status = 'cancelled') anul,
             count(*) FILTER (WHERE status = 'no_show') nieodebr, count(*) FILTER (WHERE status IN ('completed', 'refunded')) odbyte,
             count(*) FILTER (WHERE status = 'refunded') zwrocone, coalesce(sum(zw) FILTER (WHERE status = 'refunded'), 0) zw_zl,
             coalesce(sum(kl) FILTER (WHERE status = 'refunded'), 0) kl_zw
      FROM b_wiz GROUP BY ALL""").df()
    zw["dz"] = pd.to_datetime(zw["dz"]).dt.date
    zw["o"] = [1 if d < OKRES2 else 2 for d in zw["dz"]]
    s = zw.groupby(["o", "cel", "nowa"])[["odbyte", "zwrocone", "zw_zl", "kl_zw"]].sum()
    l4n, l4s, l41 = s.loc[(2, "l4", True)], s.loc[(2, "l4", False)], s.loc[1].loc["l4"].sum()
    nowe2 = s.loc[2].xs(True, level="nowa").sum()
    kontrole += [("po zakupie: zwroty L4 nowe kampanie, okres 2 (zwrócone / odbyte)", f"{int(l4n.zwrocone)} / {int(l4n.odbyte)}", "1024 / 5895"),
                 ("po zakupie: zwroty L4 pozostali, okres 2 (zwrócone / odbyte)", f"{int(l4s.zwrocone)} / {int(l4s.odbyte)}", "270 / 5080"),
                 ("po zakupie: zwroty nowe kampanie okres 2: wizyty, zł, koszt lekarza",
                  f"{int(nowe2.zwrocone)} / {round(nowe2.zw_zl)} / {round(nowe2.kl_zw)}", "1044 / 84112 / 33975")]
    zdania_z = [
        f"Zwroty po odbytej wizycie skupiają się w L4 z nowych kampanii: w okresie {O2_NAZWA} zwrot dostaje "
        f"{proc(100 * l4n.zwrocone / l4n.odbyte)} odbytych wizyt L4 ich pacjentów ({ile(l4n.odbyte, 'wizyta')}) wobec "
        f"{proc(100 * l4s.zwrocone / l4s.odbyte)} L4 pozostałych pacjentów ({ile(l4s.odbyte, 'wizyta')}) i "
        f"{proc(100 * l41.zwrocone / l41.odbyte)} w okresie {O1_NAZWA} ({ile(l41.odbyte, 'wizyta')}).",
        f"W okresie {O2_NAZWA} zwroty po wizycie u pacjentów nowych kampanii to {ile(nowe2.zwrocone, 'wizyta')}, "
        f"{zl(nowe2.zw_zl)} zwróconych zapłat i {zl(nowe2.kl_zw)} kosztu lekarza za te wizyty. Powodu zwrotu w danych "
        f"nie ma; możliwe odczytanie: lekarz nie wystawia L4, którego pacjent oczekuje po obietnicy reklamy.",
    ]
    zwroty = tablice_dzienne(zw, ["cel", "nowa", "pierwsze"], "dz",
                             ["wszystkie", "anul", "nieodebr", "odbyte", "zwrocone", "zw_zl", "kl_zw"])

    # oceny według opóźnienia wizyty (jak a5r_po_zakupie.py, sekcja 3a; na stronie z wyborem specjalizacji i grupy)
    oc = con.execute(f"""
      SELECT okres, spec, nowa, {RP.KOSZYK} koszyk, count(*) odbyte, count(rating) ocenione, coalesce(sum(rating), 0) suma,
             count(*) FILTER (WHERE rating <= 2) niskie
      FROM b_wiz WHERE status IN ('completed', 'refunded') GROUP BY ALL ORDER BY 1, 2, 3, 4""").df()
    oi = oc[(oc["spec"] == "internista") & (~oc["nowa"])].groupby(["koszyk", "okres"])[["odbyte", "ocenione", "suma", "niskie"]].sum()
    oi["sr"] = oi["suma"] / oi["ocenione"]
    o30, o5 = oi.loc["d_ponad_30_min"], oi.loc["a_do_5_min"]
    kontrole += [("po zakupie: średnia ocena internista, pozostali, ponad 30 min, okres 1 / 2",
                  f"{o30.loc[1, 'sr']:.2f} / {o30.loc[2, 'sr']:.2f}", "2.95 / 2.92"),
                 ("po zakupie: średnia ocena internista, pozostali, do 5 min, okres 1 / 2",
                  f"{o5.loc[1, 'sr']:.2f} / {o5.loc[2, 'sr']:.2f}", "4.47 / 4.45")]
    n30, n5 = o30.sum(), o5.sum()
    zdania_o = [
        f"Spóźnione wizyty są gorzej oceniane, w obu okresach tak samo. U internisty, pacjenci spoza nowych kampanii: "
        f"przy opóźnieniu ponad 30 minut średnia ocena to {liczba(o30.loc[1, 'sr'], 2)} w okresie {O1_NAZWA} i "
        f"{liczba(o30.loc[2, 'sr'], 2)} w okresie {O2_NAZWA}, a oceny 1–2 to {proc(100 * n30.niskie / n30.ocenione, 0)} "
        f"({liczba(n30.ocenione)} ocen). Przy wizycie zaczętej do 5 minut po terminie średnia to {liczba(o5.loc[1, 'sr'], 2)} "
        f"i {liczba(o5.loc[2, 'sr'], 2)}, a ocen 1–2 jest {proc(100 * n5.niskie / n5.ocenione, 0)} ({liczba(n5.ocenione)} ocen). "
        f"Ocenę wystawia {proc(100 * oc.ocenione.sum() / oc.odbyte.sum(), 0)} pacjentów po odbytej wizycie.",
    ]
    oceny = [{k: (v.item() if hasattr(v, "item") else v) for k, v in r.items() if k != "sr"} for r in oc.to_dict("records")]
    return {"godziny": td["po_godziny"],
            "punktualnosc": punkt, "zwroty": zwroty, "oceny": oceny, "ruch": ruch_tab, "zdania_ruch": zdania_ruch,
            "zdania_punktualnosc": zdania_p, "zdania_zwroty": zdania_z, "zdania_oceny": zdania_o,
            "start": START.isoformat(), "dni": (KONIEC - START).days + 1}


# ---------------------------------------------------------------- 7. wynik biznesu

def wynik(con, kontrole, mostek, td):
    dni = (KONIEC - START).days + 1

    def dzienne(sql, kolumny):
        df = con.execute(sql).df()
        df["d"] = pd.to_datetime(df["d"]).dt.date
        out = {}
        for k in kolumny:
            tab = [0.0] * dni
            for dz, v in zip(df["d"], df[k]):
                if START <= dz <= KONIEC:
                    tab[(dz - START).days] = round(float(v), 2)
            out[k] = [int(v) if float(v).is_integer() else v for v in tab]
        return out

    s = {}
    s.update(dzienne(f"""
      SELECT created_at::DATE d, coalesce(sum(amount_paid - refund_amount) FILTER (WHERE nr = 1), 0) przychod_pierwsze,
             coalesce(sum(amount_paid - refund_amount) FILTER (WHERE nr > 1), 0) przychod_powtorne,
             sum(amount_paid) zaplaty, sum(refund_amount) zwroty, sum({D.KOSZT_LEKARZA}) koszt_lekarza,
             count(*) zamowienia, count(*) FILTER (WHERE nr = 1) nowi
      FROM zam GROUP BY 1""", ["przychod_pierwsze", "przychod_powtorne", "zaplaty", "zwroty", "koszt_lekarza",
                               "zamowienia", "nowi"]))
    s.update(dzienne("SELECT purchased_at::DATE d, sum(amount_paid) go, count(*) go_n FROM czyste.go_memberships GROUP BY 1",
                     ["go", "go_n"]))
    s.update(dzienne("""
      SELECT date d, coalesce(sum(spend_pln) FILTER (WHERE utm_source = 'google'), 0) wydatki_google,
             coalesce(sum(spend_pln) FILTER (WHERE utm_source = 'meta'), 0) wydatki_meta,
             coalesce(sum(spend_pln) FILTER (WHERE utm_source = 'tiktok'), 0) wydatki_tiktok
      FROM czyste.marketing_spend GROUP BY 1""", ["wydatki_google", "wydatki_meta", "wydatki_tiktok"]))
    s.update(dzienne("""
      SELECT k.d0 d, 25 * count(*) prowizja FROM koh k JOIN zrodlo r USING (user_id)
      WHERE r.kanal = 'afiliacja_ranking' GROUP BY 1""", ["prowizja"]))
    i2 = (OKRES2 - START).days
    sum_o = lambda k, o: sum(s[k][:i2]) if o == 1 else sum(s[k][i2:])  # noqa: E731
    prz = mostek["kroki"][3]["miary"]["przychod"]
    for o in (1, 2):
        kontrole.append((f"wynik: przychód z konsultacji po zwrotach, okres {o} (zł)",
                         round(sum_o("przychod_pierwsze", o) + sum_o("przychod_powtorne", o)), round(prz[f"p{o}"])))
        kontrole.append((f"wynik: zakupy TelemediGO, okres {o}", sum_o("go_n", o), mostek["kroki"][0]["miary"]["go"][f"p{o}"]))
    kontrole.append(("wynik: prowizja afiliacyjna za dwa lata (zł)", sum(s["prowizja"]), 30825))

    def razem(o):
        p = sum_o("przychod_pierwsze", o) + sum_o("przychod_powtorne", o)
        g, kl, pr = sum_o("go", o), sum_o("koszt_lekarza", o), sum_o("prowizja", o)
        w = sum_o("wydatki_google", o) + sum_o("wydatki_meta", o) + sum_o("wydatki_tiktok", o)
        return p, g, kl, w, pr, p + g - kl - w - pr
    r1, r2 = razem(1), razem(2)

    # marża po kwartałach rok do roku (uwaga Kuby: suma roczna ukrywa spadek w ostatnim kwartale)
    def okno_sum(k, od, do):
        return sum(s[k][(od - START).days:(do - START).days + 1])

    def marza_okna(od, do):
        p_ = okno_sum("przychod_pierwsze", od, do) + okno_sum("przychod_powtorne", od, do)
        w_ = okno_sum("wydatki_google", od, do) + okno_sum("wydatki_meta", od, do) + okno_sum("wydatki_tiktok", od, do)
        return p_ + okno_sum("go", od, do) - okno_sum("koszt_lekarza", od, do) - w_ - okno_sum("prowizja", od, do), w_

    def kwartal_od(d):
        return dt.date(d.year, 3 * ((d.month - 1) // 3) + 1, 1)

    def koniec_mies(d, n):
        m = d.month - 1 + n
        return dt.date(d.year + m // 12, m % 12 + 1, 1) - dt.timedelta(days=1)

    kw = []
    q = kwartal_od(OKRES2)
    while q <= KONIEC:
        qp = dt.date(q.year - 1, q.month, 1)
        m2, w2 = marza_okna(q, koniec_mies(q, 3))
        m1, w1 = marza_okna(qp, koniec_mies(qp, 3))
        kw.append({"q": q, "m1": m1, "m2": m2, "w1": w1, "w2": w2})
        q = koniec_mies(q, 3) + dt.timedelta(days=1)
    nazwa_kw = lambda q: f"{MIESIACE_RZ[(q.month - 1) // 3]} kwartale {q.year}"  # noqa: E731
    zdanie_kw = ("Po kwartałach rok do roku marża zmienia się tak: " + ", ".join(
        f"w {nazwa_kw(k['q'])} {'+' if k['m2'] >= k['m1'] else '−'}{liczba(abs(100 * (k['m2'] / k['m1'] - 1)), 1)}%" for k in kw) + ".")
    for k in kw:
        if k["m2"] < k["m1"]:
            mies = []
            for i in range(3):
                od = dt.date(k["q"].year, k["q"].month + i, 1)
                odp = dt.date(od.year - 1, od.month, 1)
                a, _ = marza_okna(odp, koniec_mies(odp, 1))
                b_, _ = marza_okna(od, koniec_mies(od, 1))
                mies.append((MIESIACE_RZ[od.month - 1], b_ >= a))
            wyzsze = [m for m, w in mies if w]
            nizsze = [m for m, w in mies if not w]
            zdanie_kw += (f" W {nazwa_kw(k['q'])} marża jest niższa niż rok wcześniej: {zl(k['m2'])} wobec {zl(k['m1'])}, "
                          f"choć wydatki na kampanie są {liczba(k['w2'] / k['w1'], 1)} raza wyższe ({zl(k['w2'])} wobec {zl(k['w1'])}).")
            if wyzsze:
                zdanie_kw += (f" Po miesiącach: w {', '.join(wyzsze)} marża jest jeszcze wyższa niż rok wcześniej, "
                              f"w {' i '.join(nizsze)} niższa.")
    # wrzesień ostatniego miesiąca okresu 1 jako baza porównania: start sprzedaży TelemediGO w newsletterze
    wrz = dt.date(OKRES2.year, 9, 1)
    go_wrz = okno_sum("go", wrz, koniec_mies(wrz, 1))
    go_sr = okno_sum("go", START, wrz - dt.timedelta(days=1)) / ((wrz.year - START.year) * 12 + wrz.month - START.month)
    if go_wrz > 2 * go_sr:
        zdanie_kw += (f" Bazę porównania podnosi wrzesień {wrz.year}: TelemediGO daje wtedy {zl(go_wrz)} wobec średnio "
                      f"{zl(go_sr)} miesięcznie wcześniej (start sprzedaży TelemediGO w newsletterze, zdarzenie na osi).")
    kontrole.append(("wynik: marża III kw. 2026 / III kw. 2025 (zł)", f"{round(kw[-1]['m2'])} / {round(kw[-1]['m1'])}", "207713 / 222824"))
    zm = lambda a, b: f"{'+' if b >= a else '−'}{liczba(abs(100 * (b / a - 1)), 1)}%"  # noqa: E731
    ruch = lambda n, a, b, mn=False: f"{n} {('rosną' if mn else 'rośnie') if b >= a else ('spadają' if mn else 'spada')} o {liczba(abs(100 * (b / a - 1)), 1)}% ({zl(a)} → {zl(b)})"  # noqa: E731
    zdania = [
        f"Marża po koszcie lekarza, kampaniach i prowizji afiliacyjnej: {zl(r2[5])} w okresie {O2_NAZWA} wobec "
        f"{zl(r1[5])} w okresie {O1_NAZWA}, czyli {zm(r1[5], r2[5])}. Ta suma ukrywa, jak zmienia się marża w kolejnych kwartałach.",
        zdanie_kw,
        td["wynik_rozklad"],
        td["wynik_safari"],
        td["wynik_baza"],
        f"{ruch('Przychód z konsultacji po zwrotach', r1[0], r2[0])}, {ruch('TelemediGO', r1[1], r2[1])}. "
        f"{ruch('Koszt lekarza', r1[2], r2[2])}, {ruch('wydatki na kampanie', r1[3], r2[3], True)}, "
        f"{ruch('prowizja afiliacyjna', r1[4], r2[4])}.",
        "Koszt lekarza liczymy także za wizyty zwrócone po wizycie (zasada z zadania), a koszt i zwrot przypisujemy do "
        "dnia płatności. Prowizję afiliacyjną liczymy według przyjętej reguły źródła, w dniu pierwszego zamówienia.",
    ]
    return {"dni": dni, "start": START.isoformat(), "serie": s, "zdania": zdania}


def ekonomia_kampanii(kontrole):
    """Zestawienie sesji ekonomii kampanii (a5e_kampanie.csv), obie reguły źródła, okna 90 i 180 dni."""
    e = pd.read_csv(A5E_KAMPANIE)
    e = e[e["okno_dni"].isin(["90", "180"])].copy()
    e["klucz"] = e["grupa"].fillna(e["kampania"]).fillna(e["kanal"])
    wiersze = []
    for _, r in e.iterrows():
        wiersze.append({"okres": int(r["okres"]), "regula": r["regula"], "okno": int(r["okno_dni"]), "poziom": r["poziom"],
                        "klucz": r["klucz"], "nowi": int(r["nowi"]), "wydatki": float(r["wydatki_zl"]),
                        "prowizja": float(r["prowizja_zl"]), "cac": float(r["koszt_pozysk_na_pac"]),
                        "marza": float(r["marza_na_pac"]), "wynik": float(r["wynik_na_pac"]), "od": float(r["wynik_od"]),
                        "do": float(r["wynik_do"]), "razem": float(r["wynik_razem_zl"]), "powrot": float(r["powrot_proc"])})
    g = e[(e["poziom"] == "grupa") & (e["okres"] == 2) & (e["grupa"] == "1_nowe_kampanie_L4")].set_index(["regula", "okno_dni"])
    t = e[(e["poziom"] == "kampania") & (e["okres"] == 2) & (e["kampania"] == "tt_prosp_l4_15min")].set_index(["regula", "okno_dni"])
    kontrole += [("ekonomia: nowe kampanie, wynik na pacjenta 90 dni Z1K / Z2 (zł)",
                  f"{g.loc[('Z1K', '90'), 'wynik_na_pac']} / {g.loc[('Z2', '90'), 'wynik_na_pac']}", "3.6 / -9.4")]
    w = lambda x, k="wynik_na_pac": f"{'+' if x[k] >= 0 else '−'}{liczba(abs(x[k]), 1)} zł"  # noqa: E731
    zdania = [
        f"Nowe kampanie na L4 (okres {O2_NAZWA}): wynik na pacjenta po koszcie pozyskania według przyjętej reguły źródła "
        f"{w(g.loc[('Z1K', '90')])} w 90 dniach i {w(g.loc[('Z1K', '180')])} w 180 dniach, a według sesji płatności "
        f"{w(g.loc[('Z2', '90')])} i {w(g.loc[('Z2', '180')])}. Znak zależy od reguły, więc to wynik niepewny.",
        f"Kampania na TikToku ma wynik ujemny w obu regułach: {w(t.loc[('Z1K', '90')])} i {w(t.loc[('Z2', '90')])} na "
        f"pacjenta w 90 dniach.",
        "Obok wyniku po 90 dniach pokazujemy wynik po 180 dniach: pacjenci kampanii na L4 prawie nie wracają, "
        "a pozostali tak, więc 90 dni zaniża wartość pozostałych kampanii. Przedział przy wyniku jest warunkowy: liczony tylko "
        "z rozrzutu marży, bez niepewności atrybucji.",
    ]
    return {"wiersze": wiersze, "zdania": zdania}


# ---------------------------------------------------------------- 8. zdarzenia retencji i obsługi pacjenta

def zdarzenia_retencji(zdz, pac, kontrole):
    z = pd.read_csv(A5R_ZDARZENIA)
    seria = lambda s: z[z["seria"] == s].reset_index(drop=True)  # noqa: E731
    d = lambda x: data(dt.date.fromisoformat(x))  # noqa: E731
    lista = zdz["lista"]
    zrodlo = "Źródło: analiza/a5r_zdarzenia.py (podział binarny serii dziennych, próg |z| ≥ 4), notatki/a5_retencja.md, krok 5. "
    kandydaci = "Daty to kandydaci zmian, nie potwierdzone zdarzenia."

    u = seria("udzial_nowych_kampanii")
    lista.append({"id": "udzial_nowych", "obszar": "retencja", "od": u.loc[1, "od"], "rodzaj": "zmiana struktury pacjentów",
                  "tytul": "Rośnie udział pacjentów nowych kampanii na L4 wśród nowych pacjentów",
                  "co": "Od startu kampanii Meta na L4 coraz większa część nowych pacjentów przychodzi z dwóch nowych kampanii "
                        "na L4. Ci pacjenci prawie nie wracają, więc ich udział obniża powrót całej kohorty.",
                  "ile": "Udział w nowych pacjentach: " + ", ".join(
                      f"{proc(r['poziom'])} od {d(r['od'])} do {d(r['do'])} ({ile(r['n'], 'pacjent')})" for _, r in u.iterrows()) + ".",
                  "skad": zrodlo + kandydaci,
                  "link": "#kohorty?miara=udzial&podz=grupa&wygl=28"})
    p30 = seria("powrot30_wszyscy")
    start_tt = dt.date.fromisoformat([z for z in lista if z["id"] == "start_tiktok"][0]["od"])
    lista.append({"id": "powrot30_spada", "obszar": "retencja", "od": p30.loc[2, "od"], "rodzaj": "zmiana zachowania kohort",
                  "tytul": "Powrót nowych pacjentów w 30 dniach spada",
                  "co": f"Powrót w 30 dniach całej kohorty spada skokowo zaraz po starcie kampanii TikTok na L4 "
                        f"({data(start_tt)}); metoda wskazała dzień później. To głównie skład pacjentów (rosnący udział "
                        f"nowych kampanii), co pokazuje krok 3 analizy retencji.",
                  "ile": f"{proc(p30.loc[1, 'poziom'])} ({ile(p30.loc[1, 'n'], 'pacjent')}, {d(p30.loc[1, 'od'])}–{d(p30.loc[1, 'do'])}) "
                         f"→ {proc(p30.loc[2, 'poziom'])} ({ile(p30.loc[2, 'n'], 'pacjent')}, {d(p30.loc[2, 'od'])}–{d(p30.loc[2, 'do'])}). "
                         f"Wcześniejszy kandydat {d(p30.loc[1, 'od'])}: {proc(p30.loc[0, 'poziom'])} → {proc(p30.loc[1, 'poziom'])}; "
                         f"wypada w pierwszym roku, więc może być porą roku.",
                  "skad": zrodlo + kandydaci, "link": "#kohorty?okno=30&podz=grupa&wygl=28"})
    m = seria("marza30_na_pacjenta_zl")
    lista.append({"id": "marza30_spada", "obszar": "retencja", "od": m.loc[1, "od"], "rodzaj": "zmiana wyniku kohort",
                  "tytul": "Marża na pacjenta w 30 dniach spada stopniami",
                  "co": "Marża nowego pacjenta w pierwszych 30 dniach (przed kosztem pozyskania) spada trzema stopniami, "
                        "głównie przez skład pacjentów.",
                  "ile": " → ".join(f"{liczba(r['poziom'], 1)} zł od {d(r['od'])} ({ile(r['n'], 'pacjent')})" for _, r in m.iterrows()) + ".",
                  "skad": zrodlo + kandydaci, "link": "#kohorty?miara=marza&okno=30&wygl=28"})
    # kandydat w powrocie 90 dni starych kampanii (poniżej progu): poziomy przed i po liczone z danych kohort
    data_kand = dt.date(2026, 3, 2)           # najsilniejszy kandydat z a5r_zdarzenia.txt (|z| poniżej progu 4)
    stare = pac[~pac["kampania"].isin(RP.NOWE) & (pac["d0"] <= KONIEC - dt.timedelta(days=90))]
    pr = lambda x: 100 * ((x["dni_R2"] >= 0) & (x["dni_R2"] <= 90)).mean()  # noqa: E731
    sp, sa = stare[stare["d0"] < data_kand], stare[stare["d0"] >= data_kand]
    kontrole.append(("zdarzenia: powrót 90 dni stare kampanie przed / po 2.03.2026 (%)", f"{pr(sp):.1f} / {pr(sa):.1f}", "23.3 / 20.9"))
    lista.append({"id": "powrot90_stare", "obszar": "retencja", "od": data_kand.isoformat(), "rodzaj": "kandydat poniżej progu",
                  "tytul": "Powrót w 90 dniach w kampaniach działających w obu latach: brak wyraźnego skoku",
                  "co": "W kampaniach obecnych w obu latach powrót też spada, ale metoda nie znalazła zmiany skokowej powyżej "
                        "progu. Najsilniejszy kandydat to ten dzień. Brak skoku nie znaczy, że spadek musi być rozłożony w czasie.",
                  "ile": f"{proc(pr(sp))} przed ({ile(len(sp), 'pacjent')}) i {proc(pr(sa))} po ({ile(len(sa), 'pacjent')}, "
                         f"kohorty z pełnym oknem 90 dni).",
                  "skad": zrodlo + "Luty 2026 nie pasuje do prostej hipotezy przeciążenia (opóźnienia już wysokie, powrót bez "
                          "spadku), to trop eksploracyjny.",
                  "link": "#kohorty?okno=90&f_grupa=pozostale&wygl=28"})
    o = seria("rano_internista_ponad15_stare")
    lista.append({"id": "opoznienia_rano", "obszar": "obsluga", "od": o.loc[1, "od"], "rodzaj": "zmiana obsługi pacjenta",
                  "tytul": "Poranne wizyty u internisty zaczynają się z opóźnieniem",
                  "co": "Rośnie odsetek wizyt u internisty z terminem 6:00–11:59, które zaczynają się ponad 15 minut po "
                        "terminie, także u pacjentów spoza nowych kampanii. Przy tym samym porannym ruchu opóźnień jest teraz "
                        "dużo więcej niż rok wcześniej, a już wizyty z najwcześniejszym porannym terminem dnia są często "
                        "spóźnione (bez przesądzania przyczyny).",
                  "ile": " → ".join(f"{proc(r['poziom'])} od {d(r['od'])} ({ile(r['n'], 'wizyta')})" for _, r in o.iterrows()) + ".",
                  "skad": zrodlo + "Seria: wizyty u internisty rano, pacjenci spoza nowych kampanii. " + kandydaci,
                  "link": "#po-zakupie"})
    zw = seria("pierwsze_zwrot_po_wizycie")
    lista.append({"id": "zwroty_pierwsze", "obszar": "obsluga", "od": zw.loc[1, "od"], "rodzaj": "zmiana obsługi pacjenta",
                  "tytul": "Więcej pierwszych zamówień zwracanych po wizycie",
                  "co": "Rośnie odsetek pierwszych zamówień, za które pacjent dostaje zwrot po odbytej wizycie. Skupia się "
                        "w wizytach L4 pacjentów nowych kampanii. Lekarz dostaje wynagrodzenie także za te wizyty.",
                  "ile": " → ".join(f"{proc(r['poziom'])} od {d(r['od'])} ({ile(r['n'], 'pacjent')})" for _, r in zw.iterrows()) + ".",
                  "skad": zrodlo + kandydaci, "link": "#po-zakupie"})
    lista.sort(key=lambda x: x["od"])
    for ob in zdz["obszary"]:
        if ob["id"] in ("retencja", "obsluga"):
            ob["puste"] = ""


# ---------------------------------------------------------------- main

def main():
    sys.stdout.reconfigure(errors="replace")
    kontrole = []
    d = wczytaj_lejek()
    zd = pd.read_csv(ZDARZENIA_CSV, dtype={"wartosc": str})
    etykiety_pochodne(sorted(d.loc[d["podzial"] == "system_przegladarka", "wartosc"].unique()),
                      sorted(d.loc[d["podzial"] == "urzadzenie_przegladarka", "wartosc"].unique()))

    rozmiary = eksport_lejka(d, kontrole)
    # odczyty z raportów sesji prowadzącej (c_*, d_*) i nowe brzmienia pozostałych zakładek (notatki/d_teksty_strony.md)
    Z2 = B2.Zrodla()
    V2 = B2.wartosci(Z2)
    td = B2.teksty_d(V2)
    nag = naglowek_lejka(d, zd, kontrole, td, V2)
    kontrole.append(("nowi pacjenci okresu 2: nowe kampanie + pozostali (przyjęta reguła) = wszyscy",
                     int(V2["nowe_7268"] + V2["bez_z1k"]), int(V2["nowi"][2])))

    con = D.polacz()
    mostek, jak = jakosc(con, kontrole)
    wz = czy_wzrost(con, mostek, kontrole)
    # podział nowych pacjentów dla wykresu pierwszej zakładki (etap 5 grafiki; reguła pierwszego wejścia)
    wz["pacjenci"]["grupy"] = [{"grupa": "nowe_kampanie", "n1": 0, "n2": int(V2["nowe_7268"])},
                               {"grupa": "pozostale", "n1": int(V2["nowi"][1]), "n2": int(V2["bez_z1k"])}]
    kontrole.append(("wykres pacjentów: suma grup = nowi pacjenci okresu 2",
                     sum(g["n2"] for g in wz["pacjenci"]["grupy"]), wz["pacjenci"]["n2"]))
    zdz = zdarzenia(con, d, zd, nag, jak, kontrole, td, V2, Z2)
    pac, koh, koh_zdania = kohorty(con, kontrole)
    pz = po_zakupie(con, kontrole, td)
    wy = wynik(con, kontrole, mostek, td)
    wy["ekonomia"] = ekonomia_kampanii(kontrole)
    zdarzenia_retencji(zdz, pac, kontrole)
    con.close()
    # zdanie o granicy okresów: płatności w lejku a zamówienia, zaokrąglenie przychodu (Jak liczymy)
    pl, zam = nag["platnosci"], mostek["kroki"][2]["miary"]["zamowienia"]
    prz1 = mostek["kroki"][3]["miary"]["przychod"]["p1"]
    kontrole.append(("płatności w lejku = zamówienia razem w dwóch latach", sum(pl), zam["p1"] + zam["p2"]))
    granica = (f"Płatności w lejku ({liczba(pl[0])} rok wcześniej, {O1_NAZWA}, i {liczba(pl[1])} w ostatnich 12 miesiącach, "
               f"{O2_NAZWA}) i zamówienia "
               f"({liczba(zam['p1'])} i {liczba(zam['p2'])}) różnią się o {liczba(abs(pl[0] - zam['p1']))} na granicy okresów, "
               f"bo sesję liczymy do dnia jej rozpoczęcia, a zamówienie do dnia płatności.")
    # druga lista Kuby, punkt 11: zaokrąglenie przychodu do grosza nie pasuje do „Jak liczymy” lejka; zostaje w wyniku
    nag["granica"] = granica
    wy["granica"] = (granica + f" Przychód z konsultacji po zwrotach rok wcześniej to {liczba(prz1, 2)} zł, więc zależnie od "
                     f"zaokrąglenia {liczba(int(prz1))} albo {liczba(int(prz1) + 1)} zł.")
    go = next(z for z in zdz["lista"] if z["id"] == "start_go_upsell")
    _, szkic, _ = B2.eksport_c(kontrole, wz=wz, mostek=mostek, wy=wy, nag=nag, koh=koh, pz=pz, Z=Z2, V=V2,
                               d_dodatkowe={"Kampania `crm_go_upsell`": ([go["ile"].split(" Sesje z tej kampanii")[1]], [])})
    koh["zdania"] = koh_zdania + [td["kohorty_demo"]]
    # E: karty tekstowe w nowym kształcie (notatki/e_runda.md, punkt 3): nagłówek lejka i pozostałe zakładki
    E = ET.wczytaj_e()
    sz_e = ET.karty_lejka(nag, V2, E) + ET.macierz_kohort(koh) + EZ.dodaj_karty(kontrole, V=V2, Z=Z2, E=E, wz=wz, mostek=mostek, nag=nag, jak=jak,
                                                       zdz=zdz, koh=koh, pz=pz, wy=wy)
    kontrole.append((f"E: liczby w nowych kartach zakładek bez pokrycia w notatkach ({len(sz_e)} kart, "
                     f"{sum(x[1] for x in sz_e)} liczb)", sum(len(x[2]) for x in sz_e), 0))
    szkic = szkic + sz_e

    try:
        commit = subprocess.run(["git", "-C", KATALOG, "rev-parse", "--short", "HEAD"], capture_output=True,
                                text=True, timeout=10).stdout.strip()
    except Exception:  # noqa: BLE001
        commit = ""
    meta = {"wygenerowano": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "commit": commit,
            "start": START.isoformat(), "koniec": KONIEC.isoformat(),
            "okresy": [{"od": O1[0].isoformat(), "do": O1[1].isoformat(), "nazwa": O1_NAZWA},
                       {"od": O2[0].isoformat(), "do": O2[1].isoformat(), "nazwa": O2_NAZWA}]}
    tresc = {"meta": meta, "etykiety": ETYKIETY, "wzrost": wz, "lejek_naglowek": nag}
    rozmiary["podsumowanie"] = zapisz_js("podsumowanie.js", ".P", tresc)
    rozmiary["zdarzenia"] = zapisz_js("zdarzenia.js", ".zdarzenia", zdz)
    rozmiary["jakosc"] = zapisz_js("jakosc.js", ".jakosc", jak)
    rozmiary["kohorty"] = zapisz_js("kohorty.js", ".kohorty", koh)
    rozmiary["po_zakupie"] = zapisz_js("po_zakupie.js", ".po_zakupie", pz)
    rozmiary["wynik"] = zapisz_js("wynik.js", ".wynik", wy)
    rozmiary["c"] = os.path.getsize(os.path.join(DANE, "c.js"))

    linie = [f"B — EKSPORT DANYCH NARZĘDZIA ({meta['wygenerowano']}, commit {commit})", "",
             "1. Pliki w narzedzie/dane_strony/ (bajty)"]
    for k, v in rozmiary.items():
        linie.append(f"   {k:28} {v:>12,}")
    linie.append(f"   {'razem':28} {sum(rozmiary.values()):>12,}")
    linie += ["", "2. Kontrola: liczby z eksportu wobec notatek i wcześniejszych raportów",
              f"   {'co':66} {'eksport':>10} {'oczekiwane':>11}  wynik"]
    bledy = 0
    for opis, wartosc, oczek in kontrole:
        ok = (str(wartosc) == str(oczek)) if isinstance(oczek, str) else abs(float(wartosc) - float(oczek)) < 1e-9
        bledy += not ok
        linie.append(f"   {opis:66} {wartosc!s:>10} {oczek!s:>11}  {'zgodne' if ok else 'RÓŻNICA'}")
    linie += ["", f"   Różnic: {bledy} z {len(kontrole)} kontroli.", "",
              "3. Zdarzenia na osi czasu"]
    for z in zdz["lista"]:
        linie.append(f"   {z['od']}  {z['obszar']:8} {z['tytul']}")
    linie.append(f"   Zmiany wykryte automatycznie (tabela pod osią): {len(zdz['wykryte']['wiersze'])}")
    linie += ["", "4. " + B2.raport_szkicu(szkic)[0]] + B2.raport_szkicu(szkic)[1:]
    with open(RAPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linie) + "\n")
    print("\n".join(linie))


if __name__ == "__main__":
    main()
