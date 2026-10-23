"""G — ile zmian w tabelach grup „Kohort” i „Lejka” jest większych niż przypadek (uwaga Kuby z 2026-10-23).

Kuba ustawił w „Kohortach” porównanie „60 dni przed i po: godzina bez danych” w podziale na pierwszą usługę i zobaczył,
że prawie każda komórka tabeli jest czerwona albo zielona, przy grupach po 100–500 pacjentów i różnicach rzędu 1–3
punktów procentowych. Ten skrypt odtwarza tabele strony z tych samych plików danych, które czyta strona
(`narzedzie/dane_strony/kohorty.js`, `lejek_*.js`, `zdarzenia.js`), tą samą logiką okresów i okien, i dla każdej komórki
sprawdza, czy zmiana jest istotna:
  - odsetki (powrót w oknie, przejścia lejka): 95% przedział różnicy dwóch odsetków w przybliżeniu normalnym nie obejmuje
    zera (założenie 56);
  - marża na pacjenta: 95% przedział różnicy dwóch średnich (przybliżenie normalne, wariancje osobno w każdym okresie,
    z marży pacjent po pacjencie) nie obejmuje zera.
Dziś strona koloruje każdą komórkę, w której zmiana po zaokrągleniu do jednego miejsca po przecinku nie jest zerem.

Mała grupa: mniej niż 100 pacjentów (w lejku: 100 sesji w mianowniku przejścia) w którymkolwiek okresie porównania.

Uruchomienie z głównego folderu: python -I analiza/g_istotnosc.py
Wynik: analiza/wyniki/g_istotnosc.txt i g_istotnosc.json
"""
import json
import math
import os
import re
import sys
from datetime import date

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DANE = os.path.join(KATALOG, "narzedzie", "dane_strony")
WYNIKI = os.path.join(KATALOG, "analiza", "wyniki")
ZN = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
Z95 = 1.959963984540054
MALA = 100


def czytaj(plik):
    """Plik danych strony (window.D=...; D.klucz=JSON; ...) jako słownik {klucz: obiekt}."""
    t = open(os.path.join(DANE, plik + ".js"), encoding="utf-8").read()
    wynik, dec = {}, json.JSONDecoder()
    for m in re.finditer(r"(?:^|;)D(?:\.([A-Za-z_]+))?(?:\[\"?([A-Za-z_]+)\"?\])?\s*=\s*(?=[\[{])", t, re.M):
        obj, _ = dec.raw_decode(t[m.end():])
        wynik[(m.group(1) or "") + ("." + m.group(2) if m.group(2) else "")] = obj
    return wynik


P = czytaj("podsumowanie")["P"]
ET = P["etykiety"]
ZD = czytaj("zdarzenia")["zdarzenia"]
START = date.fromisoformat(P["meta"]["start"])
KONIEC = date.fromisoformat(P["meta"]["koniec"])
NDNI = (KONIEC - START).days + 1


def idx(iso):
    return (date.fromisoformat(iso) - START).days


def ogranicz(i):
    return max(0, min(NDNI - 1, i))


def okresy(preset):
    """Okresy A i B jak okresyPreset() / ustawPreset() na stronie."""
    O = P["meta"]["okresy"]
    if preset == "rok":
        return [idx(O[0]["od"]), idx(O[0]["do"])], [idx(O[1]["od"]), idx(O[1]["do"])]
    if preset.startswith("zd:"):
        z = [x for x in ZD["lista"] if x["id"] == preset[3:]][0]
        d = idx(z["od"])
        return [ogranicz(d - 60), ogranicz(d - 1)], [ogranicz(d), ogranicz(d + 59)]
    raise ValueError(preset)


def roznica_odsetkow(lA, mA, lB, mB):
    pA, pB = lA / mA, lB / mB
    se = math.sqrt(pA * (1 - pA) / mA + pB * (1 - pB) / mB)
    d = 100 * (pB - pA)
    return d, d - 100 * Z95 * se, d + 100 * Z95 * se


def roznica_srednich(xA, xB):
    def sr_war(x):
        n = len(x)
        s = sum(x) / n
        return s, sum((v - s) ** 2 for v in x) / (n - 1) if n > 1 else 0.0
    sA, wA = sr_war(xA)
    sB, wB = sr_war(xB)
    se = math.sqrt(wA / len(xA) + wB / len(xB))
    d = sB - sA
    return d, d - Z95 * se, d + Z95 * se


def kolor_dzis(d):
    """Strona dziś: zero po zaokrągleniu do 1 miejsca = szare, inaczej czerwone albo zielone."""
    return abs(d) >= 0.05


# ------------------------------------------------------------------ kohorty
K = czytaj("kohorty")["kohorty"]
KOD = {k: [ZN.index(c) for c in s] for k, s in K["kat"].items()}


def zakres_okna(n, A, B):
    ost = NDNI - 1 - n
    bk = min(B[1], ost)
    if bk < B[0]:
        return None
    dl = bk - B[0]
    ak = min(A[1], A[0] + dl, ost)
    if ak < A[0]:
        return None
    return [A[0], ak], [B[0], bk]


def grupy_kohort(podz):
    if podz == "grupa":
        kody, wart = KOD["kampania"], K["wart"]["kampania"]
        return ["nowe" if wart[k] in ET["nowe_kampanie"] else "pozostale" for k in kody]
    kody, wart = KOD[podz], K["wart"][podz]
    return [wart[k] for k in kody]


def etykieta_kohorty(podz, w):
    if w == "__razem":
        return "Wszyscy wybrani pacjenci"
    if podz == "grupa":
        return "Nowe kampanie na L4" if w == "nowe" else "Pozostałe kampanie i kanały"
    return (ET.get(podz) or {}).get(w, w)


def tabela_kohort(podz, preset):
    A, B = okresy(preset)
    gr = grupy_kohort(podz)
    wiersze = []
    for w in ["__razem"] + sorted(set(gr)):
        ids = [i for i in range(K["n"]) if w == "__razem" or gr[i] == w]
        komorki = []
        for n in K["okna"]:
            z = zakres_okna(n, A, B)
            if not z:
                continue
            zA, zB = z
            iA = [i for i in ids if zA[0] <= K["d"][i] <= zA[1]]
            iB = [i for i in ids if zB[0] <= K["d"][i] <= zB[1]]
            if not iA or not iB:
                continue
            rA = sum(1 for i in iA if 0 <= K["r"][i] <= n)
            rB = sum(1 for i in iB if 0 <= K["r"][i] <= n)
            d, lo, hi = roznica_odsetkow(rA, len(iA), rB, len(iB))
            komorki.append({"miara": f"powrót w {n} dniach", "nA": len(iA), "nB": len(iB), "A": 100 * rA / len(iA),
                            "B": 100 * rB / len(iB), "zmiana": d, "od": lo, "do": hi})
            if n in (90, 180):
                m = K["m" + str(n)]
                d, lo, hi = roznica_srednich([m[i] / 10 for i in iA], [m[i] / 10 for i in iB])
                komorki.append({"miara": f"marża na pacjenta w {n} dniach (zł)", "nA": len(iA), "nB": len(iB),
                                "A": sum(m[i] for i in iA) / 10 / len(iA), "B": sum(m[i] for i in iB) / 10 / len(iB),
                                "zmiana": d, "od": lo, "do": hi})
        for k in komorki:
            k["istotna"] = k["od"] > 0 or k["do"] < 0
            k["kolor_dzis"] = kolor_dzis(k["zmiana"])
            k["mala"] = min(k["nA"], k["nB"]) < MALA
        wiersze.append({"grupa": etykieta_kohorty(podz, w), "komorki": komorki,
                        "nA": sum(1 for i in ids if A[0] <= K["d"][i] <= A[1]),
                        "nB": sum(1 for i in ids if B[0] <= K["d"][i] <= B[1])})
    return {"podzial": podz, "porownanie": preset, "A": A, "B": B, "wiersze": wiersze}


# ------------------------------------------------------------------ lejek
KROKI = [("k1", "s", "Wybór usługi"), ("k2", "k1", "Wybór terminu"), ("k3", "k2", "Logowanie albo konto"),
         ("k4", "k3", "Wejście na płatność"), ("k5", "k4", "Płatność przyjęta"), ("k5", "s", "Sesja do płatności")]


def tabela_lejka(podz, preset, typ="zwykla", pac="nie_kupowal"):
    A, B = okresy(preset)
    L = czytaj("lejek_" + podz)["lejek." + podz]
    serie = [s for s in L["serie"] if s["typ"] == typ and (typ != "zwykla" or pac == "wszyscy" or s["pacjent"] == pac)]
    grupy = {}
    for s in serie:
        g = grupy.setdefault(s["w"], {k: [0] * NDNI for k in ("s", "k1", "k2", "k3", "k4", "k5")})
        for k in g:
            a = s.get(k)
            if a:
                for i in range(NDNI):
                    g[k][i] += a[i]
    razem = {k: [sum(grupy[w][k][i] for w in grupy) for i in range(NDNI)] for k in ("s", "k1", "k2", "k3", "k4", "k5")}

    def suma(arr, z):
        return sum(arr[z[0]:z[1] + 1])
    wiersze = []
    for w, g in [("__razem", razem)] + sorted(grupy.items(), key=lambda x: -suma(x[1]["s"], B)):
        if suma(g["s"], A) + suma(g["s"], B) == 0:
            continue
        komorki = []
        for licz, mian, naz in KROKI:
            lA, mA, lB, mB = suma(g[licz], A), suma(g[mian], A), suma(g[licz], B), suma(g[mian], B)
            if not mA or not mB:
                continue
            d, lo, hi = roznica_odsetkow(lA, mA, lB, mB)
            komorki.append({"miara": naz, "nA": mA, "nB": mB, "A": 100 * lA / mA, "B": 100 * lB / mB, "zmiana": d,
                            "od": lo, "do": hi, "istotna": lo > 0 or hi < 0, "kolor_dzis": kolor_dzis(d),
                            "mala": min(mA, mB) < MALA})
        wiersze.append({"grupa": "Razem" if w == "__razem" else (ET.get(podz) or {}).get(w, w), "komorki": komorki,
                        "nA": suma(g["s"], A), "nB": suma(g["s"], B)})
    return {"podzial": podz, "porownanie": preset, "A": A, "B": B, "wiersze": wiersze}


def podsumuj(t):
    kom = [k for w in t["wiersze"] for k in w["komorki"]]
    return {"komorek": len(kom), "kolor_dzis": sum(k["kolor_dzis"] for k in kom),
            "istotnych": sum(k["istotna"] for k in kom),
            "kolor_dzis_a_nieistotne": sum(k["kolor_dzis"] and not k["istotna"] for k in kom),
            "w_malych_grupach": sum(k["mala"] for k in kom)}


def data_pl(i):
    d = date.fromordinal(START.toordinal() + i)
    return f"{d.day}.{d.month:02d}.{d.year}"


def opis(t, f, nazwa):
    s = podsumuj(t)
    f.write(f"\n## {nazwa}\n")
    f.write(f"Podział: {t['podzial']}, porównanie: {t['porownanie']}, okres A {data_pl(t['A'][0])}–{data_pl(t['A'][1])}, "
            f"okres B {data_pl(t['B'][0])}–{data_pl(t['B'][1])}.\n")
    f.write(f"Komórek ze zmianą: {s['komorek']}. Dziś kolorowe (czerwone albo zielone): {s['kolor_dzis']}. "
            f"Istotne (95% przedział różnicy bez zera): {s['istotnych']}. Kolorowe dziś, choć nieistotne: "
            f"{s['kolor_dzis_a_nieistotne']}. W małych grupach (poniżej {MALA} w którymś okresie): {s['w_malych_grupach']}.\n\n")
    f.write("| Grupa | n A | n B | Miara | A | B | Zmiana | 95% przedział | Istotna | Kolor dziś | Mała |\n")
    f.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
    for w in t["wiersze"]:
        for k in w["komorki"]:
            f.write(f"| {w['grupa']} | {k['nA']} | {k['nB']} | {k['miara']} | {k['A']:.1f} | {k['B']:.1f} | {k['zmiana']:+.1f} | "
                    f"{k['od']:+.1f} do {k['do']:+.1f} | {'tak' if k['istotna'] else 'nie'} | "
                    f"{'tak' if k['kolor_dzis'] else 'nie'} | {'tak' if k['mala'] else ''} |\n")
    return s


def main():
    sys.stdout.reconfigure(errors="replace")
    scenariusze = [
        ("Kohorty: 60 dni przed i po godzinie bez danych, podział na pierwszą usługę (przypadek Kuby)",
         tabela_kohort("usluga", "zd:luka_godzina")),
        ("Kohorty: ustawienia domyślne (ostatnie 12 miesięcy wobec roku wcześniej, nowe kampanie na L4)",
         tabela_kohort("grupa", "rok")),
        ("Kohorty: ostatnie 12 miesięcy wobec roku wcześniej, podział na pierwszą usługę", tabela_kohort("usluga", "rok")),
        ("Kohorty: 60 dni przed i po starcie kampanii Meta na L4, podział na źródło (kanał)",
         tabela_kohort("kanal", "zd:start_meta_l4")),
        ("Lejek: ustawienia domyślne (osoby, które jeszcze nie kupowały, przeglądarka, rok do roku)",
         tabela_lejka("przegladarka", "rok")),
        ("Lejek: 60 dni przed i po godzinie bez danych, przeglądarka", tabela_lejka("przegladarka", "zd:luka_godzina")),
        ("Lejek: 60 dni przed i po awarii Safari, system i przeglądarka", tabela_lejka("system_przegladarka", "zd:safari_ios")),
    ]
    os.makedirs(WYNIKI, exist_ok=True)
    wynik = []
    with open(os.path.join(WYNIKI, "g_istotnosc.txt"), "w", encoding="utf-8") as f:
        f.write("# G — istotność zmian w tabelach grup („Kohorty” i „Lejek”)\n\n" + __doc__.split("Uruchomienie")[0])
        for nazwa, t in scenariusze:
            s = opis(t, f, nazwa)
            wynik.append({"nazwa": nazwa, "podsumowanie": s, "tabela": t})
            print(nazwa)
            print("  ", s)
    with open(os.path.join(WYNIKI, "g_istotnosc.json"), "w", encoding="utf-8") as f:
        json.dump(wynik, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
