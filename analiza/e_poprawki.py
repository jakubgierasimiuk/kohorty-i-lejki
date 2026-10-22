"""E2 — liczby do drugiej listy poprawek Kuby (runda E, 2026-10-22): tylko te, których nie ma w żadnym raporcie.

1. Lejek osób, które jeszcze nie kupowały: ile płaci „dziś”. Konwersja sesji do płatności w miesiącach IV–IX 2026
   (poziom po pogłębieniu spadku, notatki/e_runda.md, punkt 4.4) wobec tych samych miesięcy rok wcześniej (IV–IX 2025)
   i, dla porównania, w III kwartale 2026 wobec III kwartału 2025. Sprawdzenie: suma miesięcy = miesiące z
   analiza/wyniki/e_merytoryka.json (lj_miesiace).
2. Zwroty po wizycie u pacjentów nowych kampanii w ostatnich 12 miesiącach: wszystkie cele wizyty a same wizyty L4
   (dlaczego „Po zakupie” pokazuje 1 044 zwroty, a pozycja 5 listy priorytetów 1 024). Liczone niezależnie na bazie,
   według dnia płatności, jak w analiza/a5r_po_zakupie.py (2b).
3. (Trzecia lista Kuby, 2026-10-22, punkt 1.) Osoby, które jeszcze nie kupowały, bez nowych kampanii na L4: czy
   „poza nowymi kampaniami konwersja się nie zmieniła” zależy od reguły przypisania i czy płaska średnia przykrywa
   Safari na iPhone'ach. Dotychczasowy nagłówek lejka liczył bez sesji, których własna kampania to nowa kampania
   („według sesji”). Tu liczymy też bez wszystkich sesji osób, których pierwsze wejście przypisuje do nowej kampanii
   („według pierwszego wejścia”, ta sama reguła co w retencji). Osoba = konto (sesje konta i anonimowe sesje
   przeglądarek, w których konto kiedyś było zalogowane), a bez konta przeglądarka (visitor_id); pierwsze wejście
   osoby = kampania jej pierwszej sesji, a gdy osoba ma zamówienie — źródło według pierwszego wejścia z definicje.py
   (kod kampanii na pierwszym zamówieniu rozstrzyga). W tej grupie osobno Safari na iPhone'ach (system iOS
   i przeglądarka Safari, także iPady, jak w karcie Safari) i pozostałe przeglądarki, miesiąc po miesiącu, z krokiem
   konta po wyborze terminu. Test rozróżniający: rozkład zmiany IV–IX 2026 wobec IV–IX 2025 na Safari i resztę.
   Sprawdzenia: wszystkie sesje = lejek dzienny (a5p_lejek_dzienny.csv.gz), wersja według sesji = e_merytoryka.json,
   płatności w sesjach powrotnych osób nowych kampanii = 2 081 pacjentów z e_merytoryka.json (p_X_caly).

Czyta bazę analiza/telemedi.duckdb tylko do odczytu (schemat `czyste`, definicje z analiza/definicje.py) i plik
analiza/wyniki/a5p_lejek_dzienny.csv.gz (lejek dzienny, z którego liczy też e_merytoryka.py). Raport:
analiza/wyniki/e_poprawki.txt, liczby dla strony: analiza/wyniki/e_poprawki.json.
Uruchomienie z głównego folderu: python -I analiza/e_poprawki.py
"""

import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
from a5r_punktualnosc import zbuduj_wizyty  # noqa: E402

WYNIKI = os.path.join(D.KATALOG, "analiza", "wyniki")
DZIS = ("2026-04", "2026-09")          # miesiące „dziś”: od pogłębienia spadku (kwiecień 2026) do końca danych
ROK_WCZESNIEJ = ("2025-04", "2025-09")
Q3 = (("2026-07", "2026-09"), ("2025-07", "2025-09"))
NOWE = ("meta_prosp_l4_szybko", "tt_prosp_l4_15min")   # nowe kampanie na L4 (jak w e_merytoryka.py i b2_eksport_c.py)
PRZED_AWARIA = (("2025-10", "2026-02"), ("2024-10", "2025-02"))   # pełne miesiące przed awarią Safari (17.03.2026)


def rozklad(d1, d2, grupa):
    """Rozkład zmiany odsetka sesji z płatnością (d2 wobec d1, punkty procentowe) na grupy kolumny `grupa`, wzór
    symetryczny: struktura = (u2 − u1) × (k1 + k2) / 2, w obrębie grupy = (u1 + u2) / 2 × (k2 − k1). Grupa bez sesji
    w d1 (nowe kampanie) dostaje k1 = k2, więc liczy się w całości do struktury (jak w e_merytoryka.py, punkt 4).
    Suma składników = zmiana średniej. Zwraca (zmiana, {grupa: (struktura, w obrębie)})."""
    a1 = d1.groupby(grupa).k5.agg(["size", "sum"])
    a2 = d2.groupby(grupa).k5.agg(["size", "sum"])
    n1, n2 = a1["size"].sum(), a2["size"].sum()
    out = {}
    for g in a1.index.union(a2.index):
        u1 = a1["size"].get(g, 0) / n1
        u2 = a2["size"].get(g, 0) / n2
        k2 = a2["sum"][g] / a2["size"][g] if g in a2.index else None
        k1 = a1["sum"][g] / a1["size"][g] if g in a1.index else k2
        k2 = k1 if k2 is None else k2
        out[g] = (100 * (u2 - u1) * (k1 + k2) / 2, 100 * (u1 + u2) / 2 * (k2 - k1))
    zm = 100 * (d2.k5.mean() - d1.k5.mean())
    assert abs(sum(a + b for a, b in out.values()) - zm) < 1e-9
    return zm, out


def przedzial(d1, d2):
    """Zmiana odsetka sesji z płatnością (punkty procentowe) z 95% przedziałem w przybliżeniu normalnym. Sesje traktujemy
    jak niezależne, choć część to sesje tej samej osoby, więc przedział jest raczej za wąski."""
    p1, p2, n1, n2 = d1.k5.mean(), d2.k5.mean(), len(d1), len(d2)
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    zm = p2 - p1
    return 100 * zm, 100 * (zm - 1.96 * se), 100 * (zm + 1.96 * se)


def main():
    sys.stdout.reconfigure(errors="replace")
    linie, J = [], {}

    def r(t=""):
        linie.append(t)

    r(f"E2 — LICZBY DO DRUGIEJ LISTY POPRAWEK ({dt.datetime.now():%Y-%m-%d %H:%M})")
    r("Okres 1 = rok wcześniej (1.10.2024–30.09.2025), okres 2 = ostatnie 12 miesięcy (1.10.2025–30.09.2026), czas polski.")

    # ------------------------------------------------------------------------------------------------ 1. lejek „dziś”
    r("\n1. LEJEK OSÓB, KTÓRE JESZCZE NIE KUPOWAŁY: SESJA DO PŁATNOŚCI „DZIŚ” (sesje zwykłe, dzień sesji w czasie polskim)")
    L = pd.read_csv(os.path.join(WYNIKI, "a5p_lejek_dzienny.csv.gz"))
    L["dzien"] = pd.to_datetime(L.dzien)
    z = L[(L.typ == "zwykla") & (L.podzial == "calosc") & (L.pacjent == "nie_kupowal")].copy()
    z["mies"] = z.dzien.dt.strftime("%Y-%m")
    m = z.groupby("mies")[["sesje", "k5"]].sum()

    def okno(od, do, nazwa):
        x = m.loc[od:do]
        s, p = int(x.sesje.sum()), int(x.k5.sum())
        k = 100 * p / s
        mies = 100 * x.k5 / x.sesje
        r(f"   {nazwa:28} {od}–{do}: {s:>7} sesji, {p:>6} płatności, konwersja {k:.2f}% "
          f"(miesiące od {mies.min():.2f}% do {mies.max():.2f}%)")
        return s, p, k, float(mies.min()), float(mies.max())

    d = okno(*DZIS, "dziś (IV–IX 2026)")
    w = okno(*ROK_WCZESNIEJ, "rok wcześniej (IV–IX 2025)")
    q2 = okno(*Q3[0], "III kwartał 2026")
    q1 = okno(*Q3[1], "III kwartał 2025")
    r(f"   Zmiana IV–IX rok do roku: {d[2] - w[2]:+.2f} punktu procentowego; III kwartał: {q2[2] - q1[2]:+.2f} punktu.")
    for k, v in (("dzis", d), ("rok_wczesniej", w), ("q3_2026", q2), ("q3_2025", q1)):
        J[f"lj_nk_{k}_sesje"], J[f"lj_nk_{k}_platnosci"], J[f"lj_nk_{k}_konw"] = v[0], v[1], v[2]
        J[f"lj_nk_{k}_mies_min"], J[f"lj_nk_{k}_mies_max"] = v[3], v[4]
    J["lj_nk_dzis_od"], J["lj_nk_dzis_do"] = DZIS
    # sprawdzenie: te same miesiące w e_merytoryka.json
    with open(os.path.join(WYNIKI, "e_merytoryka.json"), encoding="utf-8") as f:
        E = json.load(f)
    em = {x["mies"]: x for x in E["lj_miesiace"]}
    for od, do, v in ((*DZIS, d), (*ROK_WCZESNIEJ, w)):
        ms = [x for x in em if od <= x <= do]
        s_e, p_e = sum(em[x]["sesje"] for x in ms), sum(em[x]["k5"] for x in ms)
        zgodne = (s_e, int(p_e)) == (v[0], v[1])
        r(f"   Sprawdzenie z e_merytoryka.json ({od}–{do}): {s_e} sesji, {int(p_e)} płatności — "
          f"{'zgodne' if zgodne else 'RÓŻNICA'}")
        assert zgodne

    # ------------------------------------------------------------------------------- 2. zwroty po wizycie, dwa zbiory
    r("\n2. ZWROTY PO ODBYTEJ WIZYCIE U PACJENTÓW NOWYCH KAMPANII (według pierwszego wejścia), OSTATNIE 12 MIESIĘCY")
    r("   Według dnia płatności; wizyta odbyta = completed albo refunded; zwrot po wizycie = refunded.")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=False)
    zbuduj_wizyty(con)
    t = con.sql("""
      SELECT visit_purpose, count(*) odbyte, count(*) FILTER (WHERE status = 'refunded') zwroty
      FROM wiz WHERE okres = 2 AND nowa_z1k AND status IN ('completed', 'refunded')
      GROUP BY 1 ORDER BY 1""").df()
    for _, x in t.iterrows():
        r(f"   {x.visit_purpose:12} wizyty odbyte {int(x.odbyte):>6}, zwroty po wizycie {int(x.zwroty):>5} "
          f"({100 * x.zwroty / x.odbyte:.1f}%)")
    wsz, l4 = int(t.zwroty.sum()), int(t.loc[t.visit_purpose == "l4", "zwroty"].iloc[0])
    l4_odb = int(t.loc[t.visit_purpose == "l4", "odbyte"].iloc[0])
    r(f"   Razem: {wsz} zwrotów po wizycie (wszystkie cele), z tego {l4} przy wizytach L4 (z {l4_odb} wizyt L4) i "
      f"{wsz - l4} przy innych celach wizyty.")
    J.update({"zw_nowe_wszystkie": wsz, "zw_nowe_l4": l4, "zw_nowe_l4_odbyte": l4_odb, "zw_nowe_inne_cele": wsz - l4})

    # ------------------------------- 3. nowe osoby bez nowych kampanii: według pierwszego wejścia, Safari a reszta
    r("\n3. OSOBY, KTÓRE JESZCZE NIE KUPOWAŁY, BEZ NOWYCH KAMPANII: WEDŁUG PIERWSZEGO WEJŚCIA A WEDŁUG SESJI")
    r("   Sesje zwykłe osób, które jeszcze nie kupowały (lejek główny, jak analiza/a5p_lejek.py), dzień sesji w czasie polskim.")
    r("   Według sesji = bez sesji, których własna kampania to nowa kampania (dotychczasowy nagłówek lejka).")
    r("   Według pierwszego wejścia = bez wszystkich sesji osób, których pierwsze wejście to nowa kampania (jak w retencji).")
    r("   Osoba = konto (z anonimowymi sesjami jego przeglądarek), bez konta przeglądarka; pierwsze wejście osoby z zamówieniem")
    r("   według definicje.py (kod kampanii na pierwszym zamówieniu rozstrzyga), bez zamówienia = kampania jej pierwszej sesji.")
    r("   Safari na iPhone'ach = system iOS i przeglądarka Safari (także iPady). Okres 1/2 jak wyżej.")
    con.execute("""
      CREATE TEMP TABLE ev3 AS
      SELECT session_id, max((event_name = 'slot_selected')::INT) k2, max((event_name = 'account_completed')::INT) k3,
             max((event_name = 'payment_succeeded')::INT) k5
      FROM czyste.events GROUP BY 1""")
    con.execute("CREATE TEMP TABLE pierwszy3 AS SELECT user_id, min(created_at) t FROM czyste.orders GROUP BY 1")
    con.execute("""
      CREATE TEMP TABLE sl3 AS
      SELECT s.session_id, s.dzien_pl dzien, s.started_at_pl,
             coalesce(CAST(coalesce(s.user_id, p.user_id) AS VARCHAR), 'v:' || s.visitor_id) osoba,
             coalesce(s.user_id, p.user_id) pacjent_id,
             coalesce(s.utm_campaign, s.utm_source || '_' || s.utm_medium, 'bezposrednie') kampania,
             s.os = 'iOS' AND s.browser = 'Safari' safari,
             CASE WHEN g.session_id IS NOT NULL THEN 'samo_telemedigo'
                  WHEN s.user_id IS NOT NULL AND coalesce(e.k3, 0) = 0 THEN 'zalogowana_od_wejscia' ELSE 'zwykla' END typ,
             coalesce(pz.t < s.started_at_pl, FALSE) kupowal,
             coalesce(e.k2, 0) k2, coalesce(e.k3, 0) k3, coalesce(e.k5, 0) k5
      FROM czyste.sessions s
      LEFT JOIN ev3 e USING (session_id)
      LEFT JOIN (SELECT DISTINCT session_id FROM czyste.go_memberships WHERE order_id IS NULL) g USING (session_id)
      LEFT JOIN przeg p ON p.visitor_id = s.visitor_id AND s.user_id IS NULL
      LEFT JOIN pierwszy3 pz ON pz.user_id = coalesce(s.user_id, p.user_id)""")
    con.execute("""
      CREATE TEMP TABLE osoba3 AS
      WITH pw AS (SELECT osoba, arg_min(kampania, (started_at_pl, session_id)) kampania_pierwsza,
                         any_value(pacjent_id) pacjent_id
                  FROM sl3 GROUP BY 1)
      SELECT pw.osoba, pw.pacjent_id, pw.kampania_pierwsza, z.kampania z1k, g.Z1_kampania z1,
             coalesce(z.kampania, pw.kampania_pierwsza) kampania_osoby
      FROM pw LEFT JOIN zrodlo z ON z.user_id = pw.pacjent_id LEFT JOIN reg g ON g.user_id = pw.pacjent_id""")
    k = con.sql("""
      SELECT count(*) osoby, count(z1k) z_zamowieniem,
             count(*) FILTER (WHERE z1k IS NOT NULL AND z1 <> kampania_pierwsza) pierwsza_sesja_inna_niz_z1,
             count(*) FILTER (WHERE z1k IS NOT NULL AND z1k <> kampania_pierwsza) kod_zmienia_kampanie
      FROM osoba3""").df().iloc[0]
    r(f"   Osoby: {int(k.osoby)}, z zamówieniem {int(k.z_zamowieniem)}; pierwsza sesja osoby z zamówieniem inna niż pierwsze "
      f"wejście z definicje.py: {int(k.pierwsza_sesja_inna_niz_z1)}; kod kampanii zmienia kampanię u {int(k.kod_zmienia_kampanie)}.")
    assert int(k.pierwsza_sesja_inna_niz_z1) == 0, "pierwsza sesja osoby powinna być pierwszym wejściem z definicje.py"
    x = con.sql(f"""
      SELECT strftime(s.dzien, '%Y-%m') mies, CASE WHEN s.dzien < DATE '{D.OKRES2}' THEN 1 ELSE 2 END okres,
             s.safari, s.kampania IN {NOWE} ses_nowa, o.kampania_osoby IN {NOWE} os_nowa, s.k2, s.k3, s.k5,
             coalesce(s.pacjent_id IN (SELECT user_id FROM zam WHERE nr = 1 AND visit_purpose = 'l4'), FALSE) pierwsze_l4
      FROM sl3 s JOIN osoba3 o USING (osoba) WHERE s.typ = 'zwykla' AND NOT s.kupowal""").df()

    # sprawdzenia: wszystkie sesje = lejek dzienny; według sesji = e_merytoryka.json; płatności w sesjach powrotnych = 2 081
    z["okres"] = np.where(z.dzien >= "2025-10-01", 2, 1)
    for o in (1, 2):
        lj = (int(z[z.okres == o].sesje.sum()), int(z[z.okres == o].k5.sum()))
        my = (int((x.okres == o).sum()), int(x[x.okres == o].k5.sum()))
        r(f"   Sprawdzenie, okres {o}: {my[0]} sesji i {my[1]} płatności; lejek dzienny {lj[0]} i {lj[1]} — "
          f"{'zgodne' if my == lj else 'RÓŻNICA'}")
        assert my == lj
        s_ = x[(x.okres == o) & ~x.ses_nowa]
        zg = len(s_) == E[f"lj_nk_bez_nowych_sesje_{o}"] and abs(100 * s_.k5.mean() - E[f"lj_nk_bez_nowych_{o}"]) < 1e-9
        r(f"   Sprawdzenie według sesji, okres {o}: {len(s_)} sesji, {100 * s_.k5.mean():.2f}% — e_merytoryka.json "
          f"{E[f'lj_nk_bez_nowych_sesje_{o}']}, {E[f'lj_nk_bez_nowych_{o}']:.2f}% — {'zgodne' if zg else 'RÓŻNICA'}")
        assert zg
    powr = x[(x.okres == 2) & x.os_nowa & ~x.ses_nowa]
    obce = x[~x.os_nowa & x.ses_nowa]
    r(f"   Sesje osób nowych kampanii poza sesjami z reklam nowych kampanii (wracają bezpośrednio, z wyszukiwarki, z innej "
      f"reklamy): {len(powr)} sesji, {int(powr.k5.sum())} płatności ({100 * powr.k5.mean():.2f}%); pacjentów, których "
      f"według pierwszego wejścia mają nowe kampanie, a według sesji z płatnością inne kanały: {E['p_X_caly']} — "
      f"{'zgodne' if int(powr.k5.sum()) == E['p_X_caly'] else 'RÓŻNICA'}.")
    assert int(powr.k5.sum()) == E["p_X_caly"]
    r(f"   Sesje z reklam nowych kampanii u osób, których pierwsze wejście to inny kanał: {len(obce)} (obie reguły różnią się "
      f"więc tylko sesjami powrotnymi osób nowych kampanii).")
    J.update({"lj_pw_powrotne_sesje": len(powr), "lj_pw_powrotne_platnosci": int(powr.k5.sum()),
              "lj_pw_powrotne_konw": 100 * powr.k5.mean(), "lj_pw_obce_sesje": len(obce)})

    G = x[~x.os_nowa]    # bez nowych kampanii według pierwszego wejścia
    S = x[~x.ses_nowa]   # bez nowych kampanii według sesji (dotychczasowy nagłówek)
    grupy = {"pw": G, "ses": S, "saf": G[G.safari], "res": G[~G.safari], "nowe_os": x[x.os_nowa],
             "nowe_ses": x[x.ses_nowa], "wszyscy": x}

    def okn(d, od, do):
        return d[(d.mies >= od) & (d.mies <= do)]

    def miary(d):
        k2, k3 = int(d.k2.sum()), int(d.k3.sum())
        return {"sesje": len(d), "k5": int(d.k5.sum()), "konw": 100 * d.k5.mean() if len(d) else float("nan"),
                "k2": k2, "k3": k3, "konto": 100 * k3 / k2 if k2 else float("nan")}

    okna = {"o1": lambda d: d[d.okres == 1], "o2": lambda d: d[d.okres == 2],
            "dzis": lambda d: okn(d, *DZIS), "rok_wczesniej": lambda d: okn(d, *ROK_WCZESNIEJ),
            "przed26": lambda d: okn(d, *PRZED_AWARIA[0]), "przed25": lambda d: okn(d, *PRZED_AWARIA[1])}
    r("\n   Okna (sesje, płatności, odsetek sesji z płatnością, krok konta po wyborze terminu):")
    r(f"   {'grupa':9} {'okno':14} {'sesje':>7} {'płatn.':>7} {'konw. %':>8} {'z term.':>7} {'konto %':>8}")
    for g, d in grupy.items():
        for o, f_ in okna.items():
            m = miary(f_(d))
            for kk, v in m.items():
                J[f"lj_pw_{g}_{o}_{kk}"] = v
            r(f"   {g:9} {o:14} {m['sesje']:>7} {m['k5']:>7} {m['konw']:>8.2f} {m['k2']:>7} {m['konto']:>8.1f}")
    r("   (pw = bez nowych kampanii według pierwszego wejścia, ses = według sesji, saf / res = Safari na iPhone'ach / pozostałe")
    r("   przeglądarki w grupie pw, nowe_os = osoby nowych kampanii, nowe_ses = sesje z reklam nowych kampanii;")
    r(f"   dzis = {DZIS[0]}–{DZIS[1]}, rok_wczesniej = {ROK_WCZESNIEJ[0]}–{ROK_WCZESNIEJ[1]}, przed26 = "
      f"{PRZED_AWARIA[0][0]}–{PRZED_AWARIA[0][1]}, przed25 = {PRZED_AWARIA[1][0]}–{PRZED_AWARIA[1][1]})")

    # miesiąc po miesiącu
    mies = sorted(x.mies.unique())
    wiersze = []
    for mm in mies:
        w = {"mies": mm}
        for g in ("pw", "ses", "saf", "res"):
            for kk, v in miary(grupy[g][grupy[g].mies == mm]).items():
                w[f"{g}_{kk}"] = v
        wiersze.append(w)
    M3 = pd.DataFrame(wiersze).set_index("mies")
    for g in ("pw", "ses", "saf", "res"):
        M3[f"{g}_zm"] = M3[f"{g}_konw"] - M3[f"{g}_konw"].shift(12)   # z liczb niezaokrąglonych
    r("\n   Miesiąc po miesiącu (konw = odsetek sesji z płatnością, zm = zmiana wobec tego samego miesiąca rok wcześniej, punkty;")
    r("   konto = krok konta po wyborze terminu):")
    r(f"   {'mies':8} {'pw sesje':>8} {'pw konw':>8} {'pw zm':>6} {'ses konw':>8} {'ses zm':>6} | {'saf ses.':>8} {'saf konw':>8} "
      f"{'saf zm':>6} {'saf kon.':>8} | {'res ses.':>8} {'res konw':>8} {'res zm':>6} {'res kon.':>8}")
    for mm, w in M3.iterrows():
        f2 = lambda v: "     —" if pd.isna(v) else f"{v:+6.2f}"  # noqa: E731
        r(f"   {mm:8} {int(w.pw_sesje):>8} {w.pw_konw:>8.2f} {f2(w.pw_zm)} {w.ses_konw:>8.2f} {f2(w.ses_zm)} | "
          f"{int(w.saf_sesje):>8} {w.saf_konw:>8.2f} {f2(w.saf_zm)} {w.saf_konto:>8.1f} | {int(w.res_sesje):>8} "
          f"{w.res_konw:>8.2f} {f2(w.res_zm)} {w.res_konto:>8.1f}")
    J["lj_pw_miesiace"] = [{"mies": mm, **{kk: (None if pd.isna(v) else float(v)) for kk, v in w.items()}}
                           for mm, w in M3.iterrows()]

    # test rozróżniający: rozkład zmiany IV–IX 2026 wobec IV–IX 2025
    r("\n   Test rozróżniający hipotezy (IV–IX 2026 wobec IV–IX 2025, punkty procentowe, wzór symetryczny; opisowo):")
    r("   Hipoteza Kuby: płaska średnia przykrywa Safari (Safari wyraźnie spada, reszta stoi albo lekko rośnie).")
    r("   Druga możliwość: według pierwszego wejścia średnia spada (wtedy „nie zmieniła się” wynikało z reguły).")
    d1, d2 = okn(x, *ROK_WCZESNIEJ), okn(x, *DZIS)
    for klucz, nazwa, maska, kol in (
            ("pw", "według pierwszego wejścia: Safari a pozostałe przeglądarki", lambda d: ~d.os_nowa,
             lambda d: np.where(d.safari, "safari", "reszta")),
            ("ses", "według sesji: Safari, pozostałe i sesje powrotne osób nowych kampanii", lambda d: ~d.ses_nowa,
             lambda d: np.where(d.os_nowa, "powrotne_nowych", np.where(d.safari, "safari", "reszta"))),
            ("wszyscy", "wszystkie osoby, które jeszcze nie kupowały: osoby nowych kampanii, Safari i pozostałe",
             lambda d: d.k5 >= 0, lambda d: np.where(d.os_nowa, "nowe_kampanie", np.where(d.safari, "safari", "reszta")))):
        a, b = d1[maska(d1)].copy(), d2[maska(d2)].copy()
        a["g"], b["g"] = kol(a), kol(b)
        zm, roz = rozklad(a, b, "g")
        r(f"   {nazwa}: zmiana średniej {zm:+.2f} ({100 * a.k5.mean():.2f}% → {100 * b.k5.mean():.2f}%, "
          f"{len(a)} → {len(b)} sesji)")
        J[f"lj_pw_rozklad_{klucz}_zmiana"] = zm
        for g_, (st, wew) in roz.items():
            u1, u2 = (a.g == g_).mean() * 100, (b.g == g_).mean() * 100
            k1 = 100 * a[a.g == g_].k5.mean() if (a.g == g_).any() else float("nan")
            k2 = 100 * b[b.g == g_].k5.mean()
            r(f"      {g_:16} udział sesji {u1:5.1f}% → {u2:5.1f}%, konwersja {k1:6.2f}% → {k2:6.2f}%; struktura {st:+.2f}, "
              f"w obrębie grupy {wew:+.2f}, razem {st + wew:+.2f}")
            J.update({f"lj_pw_rozklad_{klucz}_{g_}_struktura": st, f"lj_pw_rozklad_{klucz}_{g_}_wewnatrz": wew,
                      f"lj_pw_rozklad_{klucz}_{g_}_udzial_1": u1, f"lj_pw_rozklad_{klucz}_{g_}_udzial_2": u2})
        if klucz == "wszyscy":
            st_razem = sum(v[0] for v in roz.values())
            r(f"      razem zmiana struktury {st_razem:+.2f}, w obrębie Safari {roz['safari'][1]:+.2f}, w obrębie pozostałych "
              f"{roz['reszta'][1]:+.2f}")
            J["lj_pw_rozklad_wszyscy_struktura_razem"] = st_razem
    r("   Zmiana z 95% przedziałem (przybliżenie normalne, sesje jak niezależne, więc przedział raczej za wąski):")
    for g in ("pw", "ses", "saf", "res"):
        zm, lo, hi = przedzial(okn(grupy[g], *ROK_WCZESNIEJ), okn(grupy[g], *DZIS))
        r(f"      {g:4} {zm:+.2f} punktu (od {lo:+.2f} do {hi:+.2f})")
        J[f"lj_pw_{g}_zmiana_dzis"], J[f"lj_pw_{g}_zmiana_dzis_od"], J[f"lj_pw_{g}_zmiana_dzis_do"] = zm, lo, hi
    for g in ("saf", "res"):
        zm, lo, hi = przedzial(okn(grupy[g], *PRZED_AWARIA[1]), okn(grupy[g], *PRZED_AWARIA[0]))
        r(f"      {g:4} przed awarią ({PRZED_AWARIA[0][0]}–{PRZED_AWARIA[0][1]} wobec roku wcześniej) {zm:+.2f} punktu "
          f"(od {lo:+.2f} do {hi:+.2f})")
        J[f"lj_pw_{g}_zmiana_przed"], J[f"lj_pw_{g}_zmiana_przed_od"], J[f"lj_pw_{g}_zmiana_przed_do"] = zm, lo, hi
    # wrażliwość na regułę tożsamości (uwaga Codeksa, e3_codex.md, zdanie g): osoba z reklamy L4, która wróciła w innej
    # przeglądarce bez logowania, liczy się jako „pozostała”. Bez wszystkich osób z pierwszym zamówieniem L4, w obu latach.
    r("   Wrażliwość: grupa pw bez osób, których pierwsze zamówienie to L4 (w obu latach), IV–IX 2026 wobec IV–IX 2025:")
    Gb = G[~G.pierwsze_l4]
    for g, d in (("saf", Gb[Gb.safari]), ("res", Gb[~Gb.safari])):
        a_, b_ = okn(d, *ROK_WCZESNIEJ), okn(d, *DZIS)
        zm, lo, hi = przedzial(a_, b_)
        r(f"      {g}: {100 * a_.k5.mean():.2f}% ({len(a_)} sesji) → {100 * b_.k5.mean():.2f}% ({len(b_)}), zmiana {zm:+.2f} "
          f"punktu (od {lo:+.2f} do {hi:+.2f})")
        J.update({f"lj_pw_bez_l4_{g}_zmiana": zm, f"lj_pw_bez_l4_{g}_zmiana_od": lo, f"lj_pw_bez_l4_{g}_zmiana_do": hi})
    # który krok: odsetek sesji z płatnością = (z wyborem terminu / sesje) × (konto / termin) × (płatność / konto)
    r("   Który krok (IV–IX 2026 wobec IV–IX 2025): sesja z płatnością = termin/sesje × konto/termin × płatność/konto;")
    r("   udział kroku = ln(iloraz kroku) / ln(iloraz odsetka sesji z płatnością).")
    for g in ("saf", "res"):
        a, b = miary(okn(grupy[g], *ROK_WCZESNIEJ)), miary(okn(grupy[g], *DZIS))
        il = {"termin": (b["k2"] / b["sesje"]) / (a["k2"] / a["sesje"]), "konto": (b["k3"] / b["k2"]) / (a["k3"] / a["k2"]),
              "platnosc_po_koncie": (b["k5"] / b["k3"]) / (a["k5"] / a["k3"])}
        cal = b["konw"] / a["konw"]
        assert abs(np.prod(list(il.values())) - cal) < 1e-9
        r(f"      {g}: iloraz odsetka sesji z płatnością {cal:.3f}; termin {il['termin']:.3f}, konto {il['konto']:.3f}, "
          f"płatność po koncie {il['platnosc_po_koncie']:.3f}; udział kroku konta "
          f"{100 * np.log(il['konto']) / np.log(cal):.0f}%")
        for kk, v in il.items():
            J[f"lj_pw_{g}_iloraz_{kk}"] = v
        J[f"lj_pw_{g}_iloraz_konw"] = cal
        J[f"lj_pw_{g}_udzial_kroku_konta"] = 100 * np.log(il["konto"]) / np.log(cal)
    con.close()

    with open(os.path.join(WYNIKI, "e_poprawki.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linie) + "\n")
    with open(os.path.join(WYNIKI, "e_poprawki.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(J, f, ensure_ascii=False, indent=1, default=lambda v: v.item() if hasattr(v, "item") else str(v))
    print("\n".join(linie))
    print("Zapisano analiza/wyniki/e_poprawki.txt i e_poprawki.json")


if __name__ == "__main__":
    main()
