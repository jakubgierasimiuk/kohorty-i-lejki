"""B — eksport danych do plików strony narzędzia (narzedzie/dane_strony/*.js).

Strona nie ma ani jednej liczby wpisanej ręcznie w tekst (zasada Kuby z pierwszego zatrzymania punktu B).
Każde zdanie z liczbą powstaje tutaj, z bazy (schemat `czyste`, a przy jakości danych też `surowe`)
albo z wyników części pozyskania A5 (`analiza/wyniki/a5p_lejek_dzienny.csv.gz`, `a5p_zdarzenia.csv`).

Pliki danych są skryptami JS (`window.D...`), a nie JSON-em. Dzięki temu strona działa z serwera
statycznego i po otwarciu `narzedzie/index.html` wprost z dysku.

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
         "zakup": ("zakup", "zakupy", "zakupów"), "przegladarka": ("przeglądarka", "przeglądarki", "przeglądarek")}


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


def naglowek_lejka(d, zd, kontrole):
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
        "To jednak nie jest tylko „inny ruch”. Dwie rzeczy trzeba naprawić na stronie:",
    ]
    naprawy = [
        {"tytul": f"Safari na iPhone'ach i iPadach: od {data(dz)} nie działa zakładanie konta",
         "tekst": f"Krok konta po wyborze terminu u osób, które jeszcze nie kupowały, spadł z {proc(st(s_przed))} "
                  f"({ile(s_przed['k2'], 'sesja')} z wyborem terminu, {data(przed[0])}–{data(przed[1])}) do "
                  f"{proc(st(s_po60))} ({ile(s_po60['k2'], 'sesja')}, {data(po60[0])}–{data(po60[1])}). "
                  f"Pozostałe przeglądarki w tych samych dniach: {proc(st(r_przed))} i {proc(st(r_po60))}. "
                  f"Szacunek: {liczba(utr_tlo)}–{liczba(utr)} utraconych pierwszych zamówień do {data(KONIEC)}, "
                  f"czyli {liczba(utr_tlo / dni_po * 30)}–{liczba(utr / dni_po * 30)} na 30 dni.",
         "link": f"#lejek?pac=nie_kupowal&podz=system_przegladarka&krok=k3&a={przed[0]}_{przed[1]}"
                 f"&b={po60[0]}_{po60[1]}&w=iOS%20Safari"},
        {"tytul": "Przeglądarki wbudowane w aplikacje tracą pacjentów na każdym kroku",
         "tekst": f"W obu okresach płacą w {zakres(ka['k5s'].min(), ka['k5s'].max(), 1)} sesji, a Chrome i Safari "
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
    ]
    return {"zdania": zdania, "naprawy": naprawy, "osobne": osobne, "safari": safari,
            "konw": [k1, k2], "sesje": [int(a1["sesje"]), int(a2["sesje"])]}


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

def zdarzenia(con, d, zd, lejek_nag, jak, kontrole):
    lista = []
    s = lejek_nag["safari"]
    lista.append({
        "id": "safari_ios", "obszar": "lejek", "od": s["data"], "rodzaj": "awaria",
        "tytul": "Safari na iOS: przestaje działać zakładanie konta",
        "co": "U osób, które jeszcze nie kupowały, krok logowania albo zakładania konta po wyborze terminu spada "
              "w Safari na iPhone'ach i iPadach i zostaje niski do końca danych. Psuje się zakładanie nowego konta, "
              "a logowanie do istniejącego działa.",
        "ile": f"Z {proc(s['przed_proc'])} ({ile(s['przed_k2'], 'sesja')} z wyborem terminu w 60 dniach przed) do "
               f"{proc(s['po60_proc'])} ({ile(s['po60_k2'], 'sesja')} w 60 dniach po). Pozostałe przeglądarki: "
               f"{proc(s['reszta_przed_proc'])} i {proc(s['reszta_po60_proc'])}. Szacunek: {liczba(s['utracone_od'])}–"
               f"{liczba(s['utracone_do'])} utraconych pierwszych zamówień w {liczba(s['dni_po'])} dniach do "
               f"{data(KONIEC)}, czyli {liczba(s['na30_od'])}–{liczba(s['na30_do'])} na 30 dni.",
        "skad": "Metoda wykrywania zmian w seriach dziennych (podział binarny) wskazała ten dzień. Sprawdzenie na bazie: "
                "spadek jest w każdym kanale, więc to nie zmiana struktury ruchu. Przyczyny w danych nie widać. "
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
    lista.append({
        "id": "start_go_upsell", "obszar": "lejek", "od": od_go.isoformat(), "rodzaj": "start kampanii",
        "tytul": "Start sprzedaży TelemediGO w newsletterze (crm_go_upsell)",
        "co": "Newsletter do pacjentów, którzy już kupowali, prowadzi na stronę /telemedigo. Pojawiają się zakupy "
              "samego TelemediGO, bez konsultacji.",
        "ile": f"{ile(tg['k5'], 'zakup')} samego TelemediGO do {data(KONIEC)}, czyli {proc(100 * tg['k5'] / wszystkie, 0)} "
               f"z {liczba(wszystkie)} wejść z tej kampanii. Pozostałe {liczba(zal['sesje'])} wejść to sesje zalogowane "
               f"od wejścia, bez zakupu.",
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
    zz = lambda z, o: zrodla[(zrodla["zrodlo"] == z) & (zrodla["o"] == o)].iloc[0]  # noqa: E731
    det = zd[(zd["podzial"] == "kampania") & (zd["wartosc"] == "meta_rmkt_koszyk") & (zd["przejscie"] == "sesja_do_platn")].iloc[0]
    kontrole += [("remarketing: płatność na sesję IV kw. 2025 (%)", round(q4["konw"], 1), 28.2),
                 ("remarketing: udział w aplikacjach IV kw. 2025 (%)", round(q4["w_apl"], 1), 13.3)]
    lista.append({
        "id": "remarketing_meta", "obszar": "lejek", "od": "2026-01-01", "rodzaj": "zmiana stopniowa",
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
               f"w 2026; z Meta (pozyskanie): {proc(zz('meta_pozyskanie', 1)['konw'])} i "
               f"{proc(zz('meta_pozyskanie', 3)['konw'])}.",
        "skad": f"Metoda wykrywania zmian wskazała {data(dt.date.fromisoformat(det['data']))} jako dzień zmiany poziomu "
                f"płatności na sesję ({proc(det['przed'])} → {proc(det['po'])}), ale zmiana narasta od początku 2026. "
                f"Źródło: analiza/a5p_zdarzenia.py, sekcje 5h i 5i; notatki/a5_pozyskanie.md, punkt 2.5.",
        "link": "#lejek?pac=nie_kupowal&podz=kampania&krok=k5&w=meta_rmkt_koszyk"})

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


# ---------------------------------------------------------------- main

def main():
    sys.stdout.reconfigure(errors="replace")
    kontrole = []
    d = wczytaj_lejek()
    zd = pd.read_csv(ZDARZENIA_CSV, dtype={"wartosc": str})
    etykiety_pochodne(sorted(d.loc[d["podzial"] == "system_przegladarka", "wartosc"].unique()),
                      sorted(d.loc[d["podzial"] == "urzadzenie_przegladarka", "wartosc"].unique()))

    rozmiary = eksport_lejka(d, kontrole)
    nag = naglowek_lejka(d, zd, kontrole)

    con = D.polacz()
    mostek, jak = jakosc(con, kontrole)
    wz = czy_wzrost(con, mostek, kontrole)
    zdz = zdarzenia(con, d, zd, nag, jak, kontrole)
    con.close()

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

    linie = [f"B — EKSPORT DANYCH NARZĘDZIA ({meta['wygenerowano']}, commit {commit})", "",
             "1. Pliki w narzedzie/dane_strony/ (bajty)"]
    for k, v in rozmiary.items():
        linie.append(f"   {k:28} {v:>12,}")
    linie.append(f"   {'razem':28} {sum(rozmiary.values()):>12,}")
    linie += ["", "2. Kontrola: liczby z eksportu wobec notatek i wcześniejszych raportów",
              f"   {'co':66} {'eksport':>10} {'oczekiwane':>11}  wynik"]
    bledy = 0
    for opis, wartosc, oczek in kontrole:
        ok = abs(float(wartosc) - float(oczek)) < 1e-9
        bledy += not ok
        linie.append(f"   {opis:66} {wartosc!s:>10} {oczek!s:>11}  {'zgodne' if ok else 'RÓŻNICA'}")
    linie += ["", f"   Różnic: {bledy} z {len(kontrole)} kontroli.", "",
              "3. Zdarzenia na osi czasu"]
    for z in zdz["lista"]:
        linie.append(f"   {z['od']}  {z['obszar']:8} {z['tytul']}")
    linie.append(f"   Zmiany wykryte automatycznie (tabela pod osią): {len(zdz['wykryte']['wiersze'])}")
    with open(RAPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linie) + "\n")
    print("\n".join(linie))


if __name__ == "__main__":
    main()
