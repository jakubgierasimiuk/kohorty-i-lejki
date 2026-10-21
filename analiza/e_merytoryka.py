"""E — merytoryka: wątpliwości Kuby z ostatniej rundy przed publikacją (notatki/e_runda.md, część 1, punkty 1–4).

1. Retencja „bez nowych kampanii” według przyjętej reguły (Z1K) i według sesji płatności (Z2): czy różnica to pacjenci
   nowych kampanii na L4, którzy weszli z reklamy (albo użyli kodu kampanii), a zapłacili w innej sesji.
2. Marża III kwartału 2026 wobec III kwartału 2025 bez jednorazowego startu sprzedaży TelemediGO w newsletterze
   (8–30.09.2025); fakty odporne (marża przed kampaniami, wydatki, cały rok); baza powracających bez tego skoku.
3. Marża na powtórne zamówienie reszty biznesu w III kwartale (35,86 wobec 32,81 zł): ile to rosnący udział wizyt
   ze zniżką TelemediGO.
4. Lejek osób, które jeszcze nie kupowały: konwersja sesji do płatności rok do roku, miesiąc po miesiącu, od kiedy spada;
   sprawdzenie, której grupy dotyczy zdanie o przeglądarkach w aplikacjach („4,8–7,2% wobec 16,1–18,1%”).

Tylko czyta bazę (schemat `czyste`) i plik analiza/wyniki/a5p_lejek_dzienny.csv.gz. Raport: analiza/wyniki/e_merytoryka.txt,
liczby dla strony: analiza/wyniki/e_merytoryka.json. Uruchomienie z głównego folderu: python -I analiza/e_merytoryka.py
"""

import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402

WYNIKI = os.path.join(D.KATALOG, "analiza", "wyniki")
NOWE = ("meta_prosp_l4_szybko", "tt_prosp_l4_15min")
KODY_NOWE = ("L4SZYBKO20", "TIKTOK25")
Q3_25, Q3_26 = "2025-07-01", "2026-07-01"
START_NEWSLETTER = "2025-09-08"   # pierwszy dzień sprzedaży osobnej TelemediGO w newsletterze (crm_go_upsell)


def zl(x):
    return f"{x:,.0f} zł".replace(",", " ")


def proc(x, m=1):
    return f"{100 * x:+.{m}f}%"


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=True)
    q = lambda s: con.sql(s).df()  # noqa: E731
    linie, J = [], {}

    def r(t=""):
        linie.append(t)

    def pokaz(df, w="     "):
        for x in df.to_string(index=False).splitlines():
            r(w + x)

    def naglowek(t):
        r("\n" + "=" * 118)
        r(t)
        r("=" * 118)

    r(f"E — MERYTORYKA: WĄTPLIWOŚCI KUBY ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Okres 1 = rok wcześniej (1.10.2024–30.09.2025), okres 2 = ostatnie 12 miesięcy (1.10.2025–30.09.2026), czas polski.")
    r("Z1K = przyjęta reguła źródła (pierwsze wejście, kod kampanii rozstrzyga), Z2 = sesja płatności.")
    r("Nowe kampanie = meta_prosp_l4_szybko i tt_prosp_l4_15min.")

    # =================================================================================================================
    # 1. REGUŁY ŹRÓDŁA W RETENCJI „BEZ NOWYCH KAMPANII”
    # =================================================================================================================
    con.execute(f"""
      CREATE TEMP TABLE e_pac AS
      SELECT p.user_id, p.d0, p.okres, p.dni_R2, r.kanal, r.kampania, r.kanal_z2, r.kampania_z2, r.kod,
             r.kampania IN {NOWE} nowa_z1k, coalesce(r.kampania_z2 IN {NOWE}, FALSE) nowa_z2,
             coalesce(r.kod IN {KODY_NOWE}, FALSE) kod_nowej,
             z.visit_purpose = 'l4' AND z.specialization = 'internista' l4,
             g.Z1_kampania IN {NOWE} pierwsze_wejscie_nowa
      FROM powr p JOIN zrodlo r USING (user_id, okres) JOIN zam z ON z.user_id = p.user_id AND z.nr = 1
           JOIN reg g ON g.user_id = p.user_id""")
    con.execute("""
      CREATE TEMP TABLE e_m90 AS
      SELECT k.user_id,
             coalesce(sum(e.marza) FILTER (WHERE e.dni <= 90), 0) marza90,
             count(*) FILTER (WHERE e.zamowienie AND e.nieanul AND NOT e.pierwsze AND e.dni <= 90) kolejne90
      FROM koh k LEFT JOIN ek e USING (user_id) GROUP BY 1""")
    pac = q("SELECT * FROM e_pac JOIN e_m90 USING (user_id)")
    pac["d0"] = pd.to_datetime(pac.d0)
    g1, g2 = D.granice_por(90)
    dojr = ((pac.okres == 1) & (pac.d0 <= pd.Timestamp(g1))) | ((pac.okres == 2) & (pac.d0 <= pd.Timestamp(g2)))
    a = pac[dojr].copy()
    a["y"] = (a.dni_R2.astype(float) <= 90).astype(float)

    def grupa(x):
        if x.nowa_z1k and x.nowa_z2:
            return "N: nowa w obu regułach"
        if x.nowa_z1k:
            return "X: nowa według Z1K, stara według Z2"
        if x.nowa_z2:
            return "Y: stara według Z1K, nowa według Z2"
        return "A: stara w obu regułach"

    for df in (a, pac):
        df["grupa"] = df.apply(grupa, axis=1)

    naglowek("1. RETENCJA „BEZ NOWYCH KAMPANII”: SKĄD RÓŻNICA MIĘDZY REGUŁAMI (kohorty z pełnym oknem 90 dni, te same dni)")
    o1 = a[a.okres == 1]
    r(f"   Okres 1: {len(o1)} pacjentów, powrót w 90 dniach {100 * o1.y.mean():.2f}%, marża w 90 dniach {o1.marza90.mean():.2f} zł, "
      f"kolejne zamówienia {o1.kolejne90.mean():.3f} [c_szkic: 23,9%, 66,6 zł, 0,334]. W okresie 1 nie ma nowych kampanii "
      f"({int(o1.nowa_z1k.sum())} według Z1K, {int(o1.nowa_z2.sum())} według Z2).")
    o2 = a[a.okres == 2]
    t = o2.groupby("grupa").agg(pacjenci=("y", "size"), powrot90=("y", "mean"), marza90=("marza90", "mean"),
                                kolejne90=("kolejne90", "mean"), kod_nowej=("kod_nowej", "mean"),
                                pierwsze_wejscie_nowa=("pierwsze_wejscie_nowa", "mean"), l4=("l4", "mean")).reset_index()
    for k in ("powrot90", "kod_nowej", "pierwsze_wejscie_nowa", "l4"):
        t[k] = (100 * t[k]).round(2)
    t["marza90"] = t.marza90.round(2)
    t["kolejne90"] = t.kolejne90.round(3)
    r("   Okres 2 według grup (kod_nowej = kod L4SZYBKO20 albo TIKTOK25 na pierwszym zamówieniu, %; pierwsze_wejscie_nowa =")
    r("   pierwsze wejście z reklamy nowej kampanii, %; l4 = pierwsza wizyta to L4 u internisty, %):")
    pokaz(t)
    G = {w.grupa[0]: w for _, w in t.iterrows()}

    def sred(maska, kol):
        x = o2[maska]
        return len(x), x[kol].mean()

    for nazwa, maska in (("bez nowych według Z1K (A + Y)", ~o2.nowa_z1k), ("bez nowych według Z2 (A + X)", ~o2.nowa_z2),
                         ("tylko A (stara w obu regułach)", (~o2.nowa_z1k) & (~o2.nowa_z2))):
        n, p = sred(maska, "y")
        _, m = sred(maska, "marza90")
        _, k = sred(maska, "kolejne90")
        r(f"   {nazwa}: {n} pacjentów, powrót {100 * p:.2f}%, marża {m:.2f} zł, kolejne zamówienia {k:.3f}")
    nA, pA = sred((~o2.nowa_z1k) & (~o2.nowa_z2), "y")
    nZ1, pZ1 = sred(~o2.nowa_z1k, "y")
    nZ2, pZ2 = sred(~o2.nowa_z2, "y")
    _, mA = sred((~o2.nowa_z1k) & (~o2.nowa_z2), "marza90")
    _, mZ1 = sred(~o2.nowa_z1k, "marza90")
    _, mZ2 = sred(~o2.nowa_z2, "marza90")
    nX = int(G["X"].pacjenci)
    nY = int(G["Y"].pacjenci) if "Y" in G else 0
    r(f"   Różnica powrotu między regułami: {100 * (pZ1 - pZ2):.2f} punktu. Grupa X ({nX} pacjentów, powrót "
      f"{G['X'].powrot90:.2f}%) obniża powrót Z2 względem A o {100 * (pA - pZ2):.2f} punktu; grupa Y ({nY} pacjentów) zmienia "
      f"powrót Z1K względem A o {100 * (pZ1 - pA):+.2f} punktu.")
    udzial_x = (pA - pZ2) / (pZ1 - pZ2) if pZ1 != pZ2 else np.nan
    r(f"   Część różnicy między regułami, którą daje grupa X: {100 * udzial_x:.0f}% (reszta to grupa Y).")
    J.update({"r_z1k_powrot": 100 * pZ1, "r_z2_powrot": 100 * pZ2, "r_A_powrot": 100 * pA, "r_A_n": nA, "r_X_n": nX, "r_Y_n": nY,
              "r_X_powrot": float(G["X"].powrot90), "r_X_kod_proc": float(G["X"].kod_nowej),
              "r_X_pierwsze_wejscie_proc": float(G["X"].pierwsze_wejscie_nowa), "r_X_l4_proc": float(G["X"].l4),
              "r_X_marza90": float(G["X"].marza90), "r_A_marza90": mA, "r_z1k_marza90": mZ1, "r_z2_marza90": mZ2,
              "r_udzial_X_w_roznicy": 100 * udzial_x})
    # sesja płatności grupy X
    sx = o2[o2.grupa.str.startswith("X")].kanal_z2.fillna("brak").value_counts(normalize=True).mul(100).round(1)
    r("   Grupa X: kanał sesji płatności (% grupy):")
    pokaz(sx.reset_index().rename(columns={"index": "kanal_z2", "kanal_z2": "kanal", "proportion": "proc"}))
    J["r_X_platnosc_kanaly"] = {k: float(v) for k, v in sx.items()}

    # przyrost pacjentów (cały okres) i grupa X w całym okresie 2
    c2 = pac[pac.okres == 2]
    c1n = int((pac.okres == 1).sum())
    r(f"\n   Cały okres (nowi pacjenci): okres 1 {c1n}; okres 2 bez nowych według Z1K {int((~c2.nowa_z1k).sum())} "
      f"({proc((~c2.nowa_z1k).sum() / c1n - 1)}), według Z2 {int((~c2.nowa_z2).sum())} ({proc((~c2.nowa_z2).sum() / c1n - 1)}).")
    xc = c2[c2.grupa.str.startswith("X")]
    yc = c2[c2.grupa.str.startswith("Y")]
    r(f"   Grupa X w całym okresie 2: {len(xc)} pacjentów ({100 * xc.kod_nowej.mean():.1f}% z kodem nowej kampanii, "
      f"{100 * xc.pierwsze_wejscie_nowa.mean():.1f}% z pierwszym wejściem z reklamy nowej kampanii, {100 * xc.l4.mean():.1f}% z "
      f"pierwszym L4); grupa Y: {len(yc)}.")
    r(f"   Bez grupy X według Z2 (A): {int(((~c2.nowa_z1k) & (~c2.nowa_z2)).sum())} pacjentów, "
      f"{proc(((~c2.nowa_z1k) & (~c2.nowa_z2)).sum() / c1n - 1)} wobec okresu 1.")
    J.update({"p_o1": c1n, "p_bez_z1k": int((~c2.nowa_z1k).sum()), "p_bez_z2": int((~c2.nowa_z2).sum()),
              "p_X_caly": len(xc), "p_Y_caly": len(yc), "p_X_caly_kod_proc": 100 * xc.kod_nowej.mean(),
              "p_X_caly_wejscie_proc": 100 * xc.pierwsze_wejscie_nowa.mean()})

    # rozkład spadku powrotu na nowe i stare kampanie po przeniesieniu grupy X do nowych kampanii
    r("\n   Rozkład spadku powrotu (23,9% → 17,4%) na nowe kampanie i resztę: wkład nowych = udział nowych × (powrót reszty −")
    r("   powrót nowych) w okresie 2; wkład reszty = powrót reszty okresu 1 − okresu 2. Wariant „Z2 + X”: Z2, w którym grupa X")
    r("   wraca do nowych kampanii.")
    p1 = o1.y.mean()
    for nazwa, maska_nowe in (("Z1K", o2.nowa_z1k), ("Z2", o2.nowa_z2), ("Z2 + X do nowych", o2.nowa_z2 | o2.grupa.str.startswith("X"))):
        u = maska_nowe.mean()
        pn, pr_ = o2[maska_nowe].y.mean(), o2[~maska_nowe].y.mean()
        w_n, w_r = u * (pr_ - pn), p1 - pr_
        r(f"   {nazwa}: udział nowych {100 * u:.1f}%, powrót reszty {100 * pr_:.2f}%, wkład nowych {100 * w_n:.2f} pkt, "
          f"reszty {100 * w_r:.2f} pkt, udział nowych w spadku {100 * w_n / (w_n + w_r):.0f}%")
        J[f"rozklad_{nazwa.replace(' ', '_').replace('+', 'plus')}_udzial_nowych_w_spadku"] = 100 * w_n / (w_n + w_r)

    # =================================================================================================================
    # 2. III KWARTAŁ BEZ JEDNORAZOWEGO STARTU SPRZEDAŻY TELEMEDIGO W NEWSLETTERZE
    # =================================================================================================================
    con.execute(f"""
      CREATE TEMP TABLE e_pac2 AS
      SELECT k.user_id, k.t0, k.okres okres_koh, k.order_id pierwsze_id,
             coalesce(r.kampania IN {NOWE}, FALSE) nowa_z1k, r.kanal
      FROM koh k LEFT JOIN zrodlo r USING (user_id)""")
    con.execute(f"""
      CREATE TEMP TABLE e_zd AS
      WITH e AS (
        SELECT z.created_at ts, 'konsultacja' typ, CASE WHEN z.nr = 1 THEN 'pierwsze' ELSE 'powtorne' END rodzaj,
               CAST(NULL AS VARCHAR) typ_go, z.user_id, CAST(NULL AS VARCHAR) kampania_wyd, z.discount_type, z.specialization,
               z.visit_purpose, z.status, z.list_price::DOUBLE cena,
               (z.amount_paid - z.refund_amount)::DOUBLE przychod, 0.0::DOUBLE go, ({D.KOSZT_LEKARZA})::DOUBLE koszt_lekarza,
               0.0::DOUBLE wydatki, 0.0::DOUBLE prowizja, 1 zamowienie
        FROM zam z
        UNION ALL
        SELECT g.purchased_at, 'telemedigo', CASE WHEN g.order_id = p.pierwsze_id THEN 'pierwsze' ELSE 'powtorne' END,
               CASE WHEN g.order_id IS NULL THEN 'osobno' WHEN g.order_id = p.pierwsze_id THEN 'kasa_pierwsze' ELSE 'kasa_kolejne' END,
               g.user_id, NULL, NULL, NULL, NULL, NULL, NULL, 0.0, g.amount_paid::DOUBLE, 0.0, 0.0, 0.0, 0
        FROM czyste.go_memberships g LEFT JOIN e_pac2 p USING (user_id)
        UNION ALL
        SELECT m.date::TIMESTAMP, 'wydatki', 'pozyskanie', NULL, NULL, m.utm_campaign, NULL, NULL, NULL, NULL, NULL,
               0.0, 0.0, 0.0, m.spend_pln::DOUBLE, 0.0, 0
        FROM czyste.marketing_spend m
        UNION ALL
        SELECT p.t0, 'prowizja', 'pozyskanie', NULL, p.user_id, NULL, NULL, NULL, NULL, NULL, NULL, 0.0, 0.0, 0.0, 0.0, 25.0, 0
        FROM e_pac2 p WHERE p.kanal = 'afiliacja_ranking')
      SELECT e.*, strftime(date_trunc('quarter', e.ts), '%Y-%m-%d') kw, strftime(date_trunc('month', e.ts), '%Y-%m') mies,
             e.ts::DATE dzien, p.okres_koh, date_trunc('quarter', p.t0) kw_koh,
             CASE WHEN e.typ = 'wydatki' THEN e.kampania_wyd IN {NOWE} ELSE p.nowa_z1k END nowa_z1k,
             e.przychod + e.go - e.koszt_lekarza - e.wydatki - e.prowizja marza,
             e.przychod + e.go - e.koszt_lekarza przed_kampaniami
      FROM e LEFT JOIN e_pac2 p USING (user_id)""")
    zd = q("SELECT * FROM e_zd")
    zd["dzien"] = pd.to_datetime(zd.dzien)
    a3, b3 = zd[zd.kw == Q3_25], zd[zd.kw == Q3_26]
    m25, m26 = a3.marza.sum(), b3.marza.sum()
    naglowek("2. MARŻA III KWARTAŁU 2026 WOBEC III KWARTAŁU 2025 BEZ JEDNORAZOWEGO STARTU SPRZEDAŻY TELEMEDIGO W NEWSLETTERZE")
    r(f"   Kontrola: marża III kw. 2025 {zl(m25)}, III kw. 2026 {zl(m26)} [c_priorytety.txt W4: 222 824 i 207 713 zł], "
      f"zmiana {proc(m26 / m25 - 1)}.")
    os_ = zd[zd.typ_go == "osobno"]
    os25 = os_[os_.kw == Q3_25]
    os26 = os_[os_.kw == Q3_26]
    okres2_os = os_[os_.dzien >= "2025-10-01"]
    tempo = len(okres2_os) / 365.0
    dni_startu = (pd.Timestamp("2025-09-30") - pd.Timestamp(START_NEWSLETTER)).days + 1
    norm = tempo * dni_startu
    nadwyzka = len(os25) - norm
    r(f"   TelemediGO kupione osobno (newsletter): III kw. 2025 {len(os25)} zakupów ({zl(os25.go.sum())}), w {dni_startu} dniach od "
      f"{START_NEWSLETTER}; III kw. 2026 {len(os26)} ({zl(os26.go.sum())}). Tempo w ostatnich 12 miesiącach: {len(okres2_os)} "
      f"zakupów, {tempo:.2f} dziennie, czyli {norm:.0f} na {dni_startu} dni.")
    r(f"   Jednorazowa nadwyżka startu ponad zwykłe tempo: {nadwyzka:.0f} zakupów × 89 zł = {zl(nadwyzka * 89)}.")
    wA = (m25 - nadwyzka * 89)
    wB = (m25 - os25.go.sum(), m26 - os26.go.sum())
    r(f"   Wariant 1 — III kw. 2025 bez nadwyżki startu (zwykłe tempo zostaje): {zl(wA)} wobec {zl(m26)}: {proc(m26 / wA - 1)}.")
    r(f"   Wariant 2 — oba kwartały bez całej sprzedaży osobnej w newsletterze: {zl(wB[0])} wobec {zl(wB[1])}: "
      f"{proc(wB[1] / wB[0] - 1)}.")
    tg = (a3.go.sum(), b3.go.sum())
    r(f"   Wariant 3 — bez wszystkich opłat TelemediGO (jak dotąd w c_priorytety.txt): {zl(m25 - tg[0])} wobec {zl(m26 - tg[1])}: "
      f"{proc((m26 - tg[1]) / (m25 - tg[0]) - 1)}.")
    J.update({"q3_m25": m25, "q3_m26": m26, "q3_zmiana_proc": 100 * (m26 / m25 - 1), "q3_osobno_25": len(os25),
              "q3_osobno_26": len(os26), "q3_osobno_25_zl": os25.go.sum(), "q3_osobno_26_zl": os26.go.sum(),
              "newsletter_tempo_dzienne": tempo, "newsletter_dni_startu": dni_startu, "newsletter_norma_startu": norm,
              "newsletter_nadwyzka": nadwyzka, "newsletter_nadwyzka_zl": nadwyzka * 89,
              "q3_w1_m25": wA, "q3_w1_zmiana_proc": 100 * (m26 / wA - 1),
              "q3_w2_m25": wB[0], "q3_w2_m26": wB[1], "q3_w2_zmiana_proc": 100 * (wB[1] / wB[0] - 1),
              "q3_w3_zmiana_proc": 100 * ((m26 - tg[1]) / (m25 - tg[0]) - 1)})
    # odporne fakty
    pk25, pk26 = a3.przed_kampaniami.sum(), b3.przed_kampaniami.sum()
    wy25, wy26 = a3.wydatki.sum(), b3.wydatki.sum()
    r(f"   Marża przed kampaniami (przychód po zwrotach + TelemediGO − koszt lekarza): {zl(pk25)} → {zl(pk26)} "
      f"({proc(pk26 / pk25 - 1)}); bez nadwyżki startu {zl(pk25 - nadwyzka * 89)} → {zl(pk26)} "
      f"({proc(pk26 / (pk25 - nadwyzka * 89) - 1)}). Wydatki na kampanie {zl(wy25)} → {zl(wy26)} (× {wy26 / wy25:.2f}).")
    J.update({"q3_przed_25": pk25, "q3_przed_26": pk26, "q3_przed_zmiana_proc": 100 * (pk26 / pk25 - 1),
              "q3_przed_bez_nadwyzki_zmiana_proc": 100 * (pk26 / (pk25 - nadwyzka * 89) - 1),
              "q3_wyd_25": wy25, "q3_wyd_26": wy26, "q3_wyd_razy": wy26 / wy25})
    # cały rok
    o1z, o2z = zd[(zd.ts >= "2024-10-01") & (zd.ts < "2025-10-01")], zd[(zd.ts >= "2025-10-01") & (zd.ts < "2026-10-01")]
    R = {}
    for k, df in (("1", o1z), ("2", o2z)):
        R[k] = {"marza": df.marza.sum(), "przed": df.przed_kampaniami.sum(), "wydatki": df.wydatki.sum(), "prowizja": df.prowizja.sum()}
    r(f"   Cały rok: marża {zl(R['1']['marza'])} → {zl(R['2']['marza'])} ({proc(R['2']['marza'] / R['1']['marza'] - 1)}); "
      f"przed kampaniami {zl(R['1']['przed'])} → {zl(R['2']['przed'])} ({proc(R['2']['przed'] / R['1']['przed'] - 1)}); "
      f"wydatki {zl(R['1']['wydatki'])} → {zl(R['2']['wydatki'])} ({proc(R['2']['wydatki'] / R['1']['wydatki'] - 1)}, "
      f"× {R['2']['wydatki'] / R['1']['wydatki']:.2f}); prowizja {zl(R['1']['prowizja'])} → {zl(R['2']['prowizja'])}.")
    J.update({"rok_marza_1": R["1"]["marza"], "rok_marza_2": R["2"]["marza"],
              "rok_marza_zmiana_proc": 100 * (R["2"]["marza"] / R["1"]["marza"] - 1),
              "rok_przed_1": R["1"]["przed"], "rok_przed_2": R["2"]["przed"],
              "rok_przed_zmiana_proc": 100 * (R["2"]["przed"] / R["1"]["przed"] - 1),
              "rok_wyd_1": R["1"]["wydatki"], "rok_wyd_2": R["2"]["wydatki"],
              "rok_wyd_zmiana_proc": 100 * (R["2"]["wydatki"] / R["1"]["wydatki"] - 1)})
    # kwartały: marża przed kampaniami i wydatki rok do roku
    r("   Kwartały rok do roku (marża przed kampaniami, wydatki):")
    kw = zd[zd.ts >= "2024-10-01"].groupby("kw").agg(przed=("przed_kampaniami", "sum"), wydatki=("wydatki", "sum"),
                                                      marza=("marza", "sum")).reset_index()
    kw["przed_rr"] = (kw.przed / kw.przed.shift(4) - 1).mul(100).round(1)
    kw["wydatki_rr"] = (kw.wydatki / kw.wydatki.shift(4) - 1).mul(100).round(1)
    kw["marza_rr"] = (kw.marza / kw.marza.shift(4) - 1).mul(100).round(1)
    pokaz(kw.round(0))
    # baza powracających (pacjenci pozyskani w poprzednich kwartałach) w III kwartałach
    r("\n   Baza powracających w III kwartałach (marża zamówień i TelemediGO pacjentów pozyskanych w poprzednich kwartałach):")
    for kwx, df in ((Q3_25, a3), (Q3_26, b3)):
        baza = df[(df.typ.isin(["konsultacja", "telemedigo"])) & (df.kw_koh < pd.Timestamp(kwx))]
        bos = baza[baza.typ_go == "osobno"]
        r(f"   {kwx[:4]}-Q3: baza {zl(baza.marza.sum())}, w tym TelemediGO osobno {len(bos)} zakupów ({zl(bos.go.sum())}); "
          f"pacjentów bazy z zamówieniem albo zakupem w kwartale {baza.user_id.nunique()}.")
        J[f"baza_{kwx[:4]}"] = baza.marza.sum()
        J[f"baza_{kwx[:4]}_osobno"] = len(bos)
        J[f"baza_{kwx[:4]}_osobno_zl"] = bos.go.sum()
    r(f"   Baza III kw. 2025 bez nadwyżki startu: {zl(J['baza_2025'] - nadwyzka * 89)} wobec {zl(J['baza_2026'])} w 2026 "
      f"({proc(J['baza_2026'] / (J['baza_2025'] - nadwyzka * 89) - 1)}); bez całej sprzedaży osobnej: "
      f"{zl(J['baza_2025'] - J['baza_2025_osobno_zl'])} wobec {zl(J['baza_2026'] - J['baza_2026_osobno_zl'])} "
      f"({proc((J['baza_2026'] - J['baza_2026_osobno_zl']) / (J['baza_2025'] - J['baza_2025_osobno_zl']) - 1)}).")
    J["baza_2025_bez_nadwyzki"] = J["baza_2025"] - nadwyzka * 89
    J["baza_zmiana_bez_nadwyzki_proc"] = 100 * (J["baza_2026"] / J["baza_2025_bez_nadwyzki"] - 1)

    # =================================================================================================================
    # 3. MARŻA NA POWTÓRNE ZAMÓWIENIE RESZTY BIZNESU: ZNIŻKA TELEMEDIGO
    # =================================================================================================================
    naglowek("3. MARŻA NA POWTÓRNE ZAMÓWIENIE RESZTY BIZNESU (Z1K, III KWARTAŁ): ILE TO WIĘCEJ WIZYT ZE ZNIŻKĄ TELEMEDIGO")
    pw = zd[(zd.typ == "konsultacja") & (zd.rodzaj == "powtorne") & (~zd.nowa_z1k) & zd.kw.isin([Q3_25, Q3_26])].copy()
    pw["m"] = pw.przychod - pw.koszt_lekarza
    tot = pw.groupby("kw").agg(n=("m", "size"), m=("m", "mean"))
    r(f"   Kontrola: {int(tot.n.iloc[0])} → {int(tot.n.iloc[1])} zamówień, marża na zamówienie {tot.m.iloc[0]:.2f} → "
      f"{tot.m.iloc[1]:.2f} zł [d_wynik: 2 879 → 3 140, 35,86 → 32,81 zł].")
    t = pw.groupby(["kw", "discount_type"]).agg(n=("m", "size"), m=("m", "mean"), cena=("cena", "mean"),
                                                przychod=("przychod", "mean"), koszt=("koszt_lekarza", "mean")).reset_index()
    t["udzial"] = t.n / t.groupby("kw").n.transform("sum") * 100
    pokaz(t.round(2))
    # rozkład zmiany marży na zamówienie: struktura (udział rodzaju zniżki) i marża w obrębie rodzaju
    p = t.pivot_table(index="discount_type", columns="kw", values=["udzial", "m"]).fillna(0)
    s1, s2 = p[("udzial", Q3_25)] / 100, p[("udzial", Q3_26)] / 100
    mm1, mm2 = p[("m", Q3_25)], p[("m", Q3_26)]
    mix = ((s2 - s1) * (mm1 + mm2) / 2).sum()
    wew = (((s1 + s2) / 2) * (mm2 - mm1)).sum()
    dmm = tot.m.iloc[1] - tot.m.iloc[0]
    r(f"   Zmiana marży na zamówienie {dmm:.2f} zł = struktura zniżek {mix:.2f} zł + zmiana w obrębie rodzaju zniżki {wew:.2f} zł "
      f"(rozkład symetryczny, suma {mix + wew:.2f}).")
    for dtp in p.index:
        r(f"     {dtp}: udział {100 * s1[dtp]:.1f}% → {100 * s2[dtp]:.1f}%, marża {mm1[dtp]:.2f} → {mm2[dtp]:.2f} zł; wkład struktury "
          f"{((s2[dtp] - s1[dtp]) * (mm1[dtp] + mm2[dtp]) / 2):.2f} zł, wkład marży {(((s1[dtp] + s2[dtp]) / 2) * (mm2[dtp] - mm1[dtp])):.2f} zł")
    J.update({"pw_n25": int(tot.n.iloc[0]), "pw_n26": int(tot.n.iloc[1]), "pw_m25": tot.m.iloc[0], "pw_m26": tot.m.iloc[1],
              "pw_zmiana": dmm, "pw_mix": mix, "pw_wewnatrz": wew,
              "pw_go_udzial_25": 100 * s1.get("go", 0), "pw_go_udzial_26": 100 * s2.get("go", 0),
              "pw_go_m25": mm1.get("go", np.nan), "pw_go_m26": mm2.get("go", np.nan),
              "pw_none_m25": mm1.get("none", np.nan), "pw_none_m26": mm2.get("none", np.nan)})
    # to samo dodatkowo według specjalizacji (internista a pozostali), żeby oddzielić strukturę usług
    pw["spec"] = np.where(pw.specialization == "internista", "internista", "inni")
    pw["kom"] = pw.spec + "/" + pw.discount_type
    t2 = pw.groupby(["kw", "kom"]).agg(n=("m", "size"), m=("m", "mean")).reset_index()
    p2 = t2.pivot_table(index="kom", columns="kw", values=["n", "m"]).fillna(0)
    n1_, n2_ = p2[("n", Q3_25)], p2[("n", Q3_26)]
    s1b, s2b = n1_ / n1_.sum(), n2_ / n2_.sum()
    mb1, mb2 = p2[("m", Q3_25)], p2[("m", Q3_26)]
    r("   Podział na specjalizację (internista / inni) × rodzaj zniżki:")
    pokaz(t2.round(2))
    mix_b = ((s2b - s1b) * (mb1 + mb2) / 2).sum()
    wew_b = (((s1b + s2b) / 2) * (mb2 - mb1)).sum()
    r(f"   Ten sam rozkład w komórkach specjalizacja × zniżka: struktura {mix_b:.2f} zł, w obrębie komórek {wew_b:.2f} zł.")
    # wpływ samej zmiany udziału GO przy stałej reszcie struktury: przenieść udział GO z 2026 na 2025
    sp = pw.groupby(["kw", "spec"]).discount_type.value_counts(normalize=True).unstack().fillna(0).mul(100).round(1)
    r("   Udział rodzajów zniżki w obrębie specjalizacji (%):")
    pokaz(sp.reset_index())
    J.update({"pw_mix_spec_znizka": mix_b, "pw_wewnatrz_spec_znizka": wew_b})

    # =================================================================================================================
    # 4. LEJEK OSÓB, KTÓRE JESZCZE NIE KUPOWAŁY
    # =================================================================================================================
    naglowek("4. LEJEK OSÓB, KTÓRE JESZCZE NIE KUPOWAŁY (sesje zwykłe, dzień sesji w czasie polskim)")
    L = pd.read_csv(os.path.join(WYNIKI, "a5p_lejek_dzienny.csv.gz"))
    L["dzien"] = pd.to_datetime(L.dzien)
    L["okres"] = np.where(L.dzien >= "2025-10-01", 2, 1)
    z = L[(L.typ == "zwykla") & (L.podzial == "calosc")]
    kroki = ["sesje", "k1", "k2", "k3", "k4", "k5"]
    t = z.groupby(["pacjent", "okres"])[kroki].sum().reset_index()
    tw = z.groupby("okres")[kroki].sum().reset_index()
    tw.insert(0, "pacjent", "wszyscy")
    t = pd.concat([t, tw])
    t["konwersja"] = (100 * t.k5 / t.sesje).round(2)
    for i, k in enumerate(["k1", "k2", "k3", "k4", "k5"]):
        t[f"p_{k}"] = (100 * t[k] / t[kroki[i]]).round(1)
    r("   Rok do roku (p_kN = odsetek przechodzących z poprzedniego kroku):")
    pokaz(t)
    tz = t.set_index(["pacjent", "okres"])
    for o in (1, 2):
        for g in ("nie_kupowal", "kupowal_wczesniej", "wszyscy"):
            J[f"lj_{g}_{o}_konw"] = float(tz.at[(g, o), "konwersja"])
            J[f"lj_{g}_{o}_sesje"] = int(tz.at[(g, o), "sesje"])
            J[f"lj_{g}_{o}_platnosci"] = int(tz.at[(g, o), "k5"])
        for k in ("k1", "k2", "k3", "k4", "k5"):
            J[f"lj_nie_kupowal_{o}_p_{k}"] = float(tz.at[("nie_kupowal", o), f"p_{k}"])
    # miesiące
    z2 = z[z.pacjent == "nie_kupowal"].copy()
    z2["mies"] = z2.dzien.dt.strftime("%Y-%m")
    m = z2.groupby("mies")[kroki].sum().reset_index()
    m["konwersja"] = (100 * m.k5 / m.sesje).round(2)
    m["rok_wczesniej"] = m.konwersja.shift(12)
    m["zmiana_rr_pkt"] = (m.konwersja - m.rok_wczesniej).round(2)
    for i, k in enumerate(["k1", "k2", "k3", "k4", "k5"]):
        m[f"p_{k}"] = (100 * m[k] / m[kroki[i]]).round(1)
    r("\n   Osoby, które jeszcze nie kupowały, miesiąc po miesiącu:")
    pokaz(m)
    J["lj_miesiace"] = m[["mies", "sesje", "k5", "konwersja", "zmiana_rr_pkt"]].to_dict(orient="records")
    # struktura ruchu nowych osób według przeglądarki i kampanii, miesiąc po miesiącu
    for podz in ("przegladarka", "kampania"):
        x = L[(L.typ == "zwykla") & (L.pacjent == "nie_kupowal") & (L.podzial == podz)].copy()
        x["mies"] = x.dzien.dt.strftime("%Y-%m")
        if podz == "przegladarka":
            x["grp"] = np.where(x.wartosc.isin(["Instagram", "Facebook", "TikTok"]), "w_aplikacji", "zwykla")
        else:
            x["grp"] = np.where(x.wartosc.isin(NOWE), "nowe_kampanie", "pozostale")
        g = x.groupby(["mies", "grp"])[["sesje", "k5"]].sum().unstack("grp")
        out = pd.DataFrame({"mies": g.index})
        for grp in g.columns.levels[1]:
            out[f"udzial_sesji_{grp}"] = (100 * g[("sesje", grp)] / g["sesje"].sum(axis=1)).round(1).values
            out[f"konw_{grp}"] = (100 * g[("k5", grp)] / g[("sesje", grp)]).round(2).values
        r(f"\n   Osoby, które jeszcze nie kupowały, według {'przeglądarki (w aplikacji = Instagram, Facebook, TikTok)' if podz == 'przegladarka' else 'kampanii (nowe kampanie na L4 a pozostałe)'}:")
        pokaz(out)
        if podz == "kampania":
            J["lj_miesiace_kampanie"] = out.to_dict(orient="records")
        # rok do roku
        x["okres"] = np.where(x.dzien >= "2025-10-01", 2, 1)
        gy = x.groupby(["okres", "grp"])[["sesje", "k5"]].sum().reset_index()
        gy["konw"] = (100 * gy.k5 / gy.sesje).round(2)
        gy["udzial"] = (100 * gy.sesje / gy.groupby("okres").sesje.transform("sum")).round(1)
        pokaz(gy)
        for _, w in gy.iterrows():
            J[f"lj_{podz}_{w.grp}_{w.okres}_konw"] = float(w.konw)
            J[f"lj_{podz}_{w.grp}_{w.okres}_udzial"] = float(w.udzial)
            J[f"lj_{podz}_{w.grp}_{w.okres}_sesje"] = int(w.sesje)
    # przeglądarki według pojedynczych wartości, oba typy osób — której grupy dotyczy „4,8–7,2% wobec 16,1–18,1%”
    r("\n   Konwersja sesji do płatności według przeglądarki, oba okresy (sprawdzenie zdania „4,8–7,2% wobec 16,1–18,1%”):")
    x = L[(L.typ == "zwykla") & (L.podzial == "przegladarka") & L.wartosc.isin(["Instagram", "Facebook", "TikTok", "Chrome", "Safari"])]
    x = x.assign(okres=np.where(x.dzien >= "2025-10-01", 2, 1))
    for g, maska in (("nie_kupowal", x.pacjent == "nie_kupowal"), ("wszyscy", x.pacjent.notna())):
        gg = x[maska].groupby(["wartosc", "okres"])[["sesje", "k1", "k5"]].sum().reset_index()
        gg["konw"] = (100 * gg.k5 / gg.sesje).round(2)
        gg["wybor_uslugi"] = (100 * gg.k1 / gg.sesje).round(1)
        r(f"   {g}:")
        pokaz(gg)
        J[f"lj_przegl_{g}"] = gg.to_dict(orient="records")
    # rozkład zmiany konwersji nowych osób: struktura według kampanii a zmiana w obrębie kampanii
    x = L[(L.typ == "zwykla") & (L.pacjent == "nie_kupowal") & (L.podzial == "kampania")]
    x = x.assign(okres=np.where(x.dzien >= "2025-10-01", 2, 1))
    g = x.groupby(["wartosc", "okres"])[["sesje", "k5"]].sum().unstack("okres").fillna(0)
    n1_, n2_ = g[("sesje", 1)], g[("sesje", 2)]
    c1_ = (g[("k5", 1)] / n1_.replace(0, np.nan))
    c2_ = (g[("k5", 2)] / n2_.replace(0, np.nan))
    s1_, s2_ = n1_ / n1_.sum(), n2_ / n2_.sum()
    c1f, c2f = c1_.fillna(c2_).fillna(0), c2_.fillna(c1_).fillna(0)
    mix = ((s2_ - s1_) * (c1f + c2f) / 2).sum() * 100
    wew = (((s1_ + s2_) / 2) * (c2f - c1f)).sum() * 100
    r(f"\n   Rozkład zmiany konwersji osób, które jeszcze nie kupowały, według kampanii: struktura {mix:.2f} pkt, w obrębie "
      f"kampanii {wew:.2f} pkt (nowe kampanie bez okresu 1 dostają konwersję z okresu 2).")
    J.update({"lj_nk_rozklad_kampania_struktura": mix, "lj_nk_rozklad_kampania_wewnatrz": wew})
    # bez nowych kampanii
    bez = x[~x.wartosc.isin(NOWE)].groupby("okres")[["sesje", "k5"]].sum()
    r(f"   Bez sesji nowych kampanii: {100 * bez.k5[1] / bez.sesje[1]:.2f}% ({int(bez.sesje[1])} sesji) → "
      f"{100 * bez.k5[2] / bez.sesje[2]:.2f}% ({int(bez.sesje[2])}).")
    J.update({"lj_nk_bez_nowych_1": 100 * bez.k5[1] / bez.sesje[1], "lj_nk_bez_nowych_2": 100 * bez.k5[2] / bez.sesje[2],
              "lj_nk_bez_nowych_sesje_1": int(bez.sesje[1]), "lj_nk_bez_nowych_sesje_2": int(bez.sesje[2])})
    # bez nowych kampanii miesięcznie
    xb = x[~x.wartosc.isin(NOWE)].copy()
    xb["mies"] = xb.dzien.dt.strftime("%Y-%m")
    mb = xb.groupby("mies")[["sesje", "k5"]].sum().reset_index()
    mb["konwersja"] = (100 * mb.k5 / mb.sesje).round(2)
    mb["zmiana_rr_pkt"] = (mb.konwersja - mb.konwersja.shift(12)).round(2)
    r("   Bez sesji nowych kampanii, miesiąc po miesiącu:")
    pokaz(mb)
    J["lj_miesiace_bez_nowych"] = mb.to_dict(orient="records")

    # =================================================================================================================
    # 5. DROBNE SPRAWDZENIA DO TEKSTÓW (punkty 5, 6 i 10 listy Kuby)
    # =================================================================================================================
    naglowek("5. DROBNE SPRAWDZENIA DO TEKSTÓW")
    # 5a. kampanie na markę i remarketing: ile zamówień z ich sesji to zamówienia powtórne
    r("5a. Zamówienia opłacone w sesjach z kampanii na markę i z remarketingu: udział zamówień powtórnych (nr > 1).")
    t = q("""
      SELECT CASE WHEN z.created_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres, s.kampania,
             count(*) zamowienia, count(*) FILTER (WHERE z.nr > 1) powtorne
      FROM zam z JOIN ses s ON s.session_id = z.session_id
      WHERE s.kampania IN ('gs_brand', 'meta_rmkt_koszyk') GROUP BY 1, 2 ORDER BY 2, 1""")
    t["udzial_powtornych"] = (100 * t.powtorne / t.zamowienia).round(1)
    pokaz(t)
    for _, w in t.iterrows():
        J[f"powtorne_{w.kampania}_{w.okres}_proc"] = float(w.udzial_powtornych)
        J[f"powtorne_{w.kampania}_{w.okres}_zam"] = int(w.zamowienia)
    # 5b. gs_generic_specjalisci: próg pauzy w liczbie nowych pacjentów
    r("\n5b. gs_generic_specjalisci, okres 2: przy jakiej liczbie utraconych nowych pacjentów pauza przestaje się opłacać")
    r("    (wydatki okresu 2 / marża na pacjenta przed kosztem pozyskania; a5e_kampanie.csv, poziom kampanii).")
    K = pd.read_csv(os.path.join(WYNIKI, "a5e_kampanie.csv"))
    K = K[(K.kampania == "gs_generic_specjalisci") & (K.okres == 2) & (K.poziom == "kampania")]
    wyd2 = float(zd[(zd.typ == "wydatki") & (zd.kampania_wyd == "gs_generic_specjalisci") & (zd.ts >= "2025-10-01")].wydatki.sum())
    nowi_rok = {"Z1K": int(c2[(c2.kampania == "gs_generic_specjalisci")].shape[0]),
                "Z2": int(c2[(c2.kampania_z2 == "gs_generic_specjalisci")].shape[0])}
    for _, w in K.iterrows():
        prog = wyd2 / w.marza_na_pac
        r(f"   {w.regula}, {w.okno_dni} dni: marża na pacjenta {w.marza_na_pac:.1f} zł; próg {prog:.0f} pacjentów rocznie "
          f"({prog / 52.14:.1f} tygodniowo); kampania przypisuje sobie {nowi_rok[w.regula]} rocznie ({nowi_rok[w.regula] / 52.14:.1f} tygodniowo).")
        J[f"gs_spec_prog_{w.regula}_{w.okno_dni}"] = prog
        J[f"gs_spec_prog_tydz_{w.regula}_{w.okno_dni}"] = prog / 52.14
    J["gs_spec_wydatki_2"] = wyd2
    J["gs_spec_nowi_z1k"], J["gs_spec_nowi_z2"] = nowi_rok["Z1K"], nowi_rok["Z2"]
    J["gs_spec_nowi_tydz_z1k"], J["gs_spec_nowi_tydz_z2"] = nowi_rok["Z1K"] / 52.14, nowi_rok["Z2"] / 52.14
    # wszyscy nowi pacjenci u specjalistów (pierwsza wizyta u specjalisty poza internistą, pediatrą i psychiatrą)
    sp = q("""SELECT CASE WHEN created_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres, count(*) n
              FROM zam WHERE nr = 1 AND specialization NOT IN ('internista', 'pediatra', 'psychiatra') GROUP BY 1 ORDER BY 1""")
    r(f"   Wszyscy nowi pacjenci z pierwszą wizytą u specjalisty (bez internisty, pediatry i psychiatry): okres 1 {int(sp.n[0])}, "
      f"okres 2 {int(sp.n[1])} ({sp.n[1] / 52.14:.1f} tygodniowo).")
    J["spec_nowi_1"], J["spec_nowi_2"], J["spec_nowi_tydz_2"] = int(sp.n[0]), int(sp.n[1]), sp.n[1] / 52.14
    # 5c. przeglądarki w aplikacjach a zwykłe: kroki lejka u osób, które jeszcze nie kupowały
    r("\n5c. Kroki lejka osób, które jeszcze nie kupowały: przeglądarki w aplikacjach (Instagram, Facebook, TikTok) a Chrome i Safari")
    x = L[(L.typ == "zwykla") & (L.pacjent == "nie_kupowal") & (L.podzial == "przegladarka")
          & L.wartosc.isin(["Instagram", "Facebook", "TikTok", "Chrome", "Safari"])].copy()
    x["okres"] = np.where(x.dzien >= "2025-10-01", 2, 1)
    x["grp"] = np.where(x.wartosc.isin(["Instagram", "Facebook", "TikTok"]), "w_aplikacji", "chrome_safari")
    for gcol in ("wartosc", "grp"):
        g = x.groupby([gcol, "okres"])[kroki].sum().reset_index()
        g["usluga"] = (100 * g.k1 / g.sesje).round(1)
        g["termin_z_uslugi"] = (100 * g.k2 / g.k1).round(1)
        g["konto_z_terminu"] = (100 * g.k3 / g.k2).round(1)
        g["platnosc_z_sesji"] = (100 * g.k5 / g.sesje).round(2)
        pokaz(g[[gcol, "okres", "sesje", "usluga", "termin_z_uslugi", "konto_z_terminu", "platnosc_z_sesji"]])
        J[f"nk_przegl_kroki_{gcol}"] = g.to_dict(orient="records")
    # 5d. pozycja 7: 3,16% + 18,84% to podział tej samej grupy
    r("\n5d. Pozycja 7: a5r_po_zakupie.txt, 5c — powrót w 90 dniach pacjentów kampanii działających w obu latach, okres 2:")
    r("    3,16% (pierwszy powrót w 24 godziny po wejściu z newslettera albo SMS-a) + 18,84% (pozostałe powroty) = 22,0%")
    r("    (14 031 pacjentów). To podział jednej grupy według drogi powrotu: 3,16 / 22,0 = 14% powrotów idzie po wejściu z CRM.")
    r("    Wartość punktu procentowego powrotu (95,6 zł) to różnica marży w dniach 1–180 (a5_retencja.md, krok 5).")
    J["crm_udzial_powrotow_proc"] = 100 * 3.16 / 21.99
    # 5e. godzina bez danych: typowe zamówienia w tej godzinie
    t = q("""
      SELECT created_at::DATE d, count(*) n FROM czyste.orders
      WHERE hour(created_at) = 13 AND created_at::DATE BETWEEN DATE '2025-05-10' AND DATE '2025-05-24' GROUP BY 1 ORDER BY 1""")
    r(f"\n5e. Zamówienia opłacone 13:00–13:59 w dniach 10–24.05.2025 (system transakcyjny): {', '.join(str(int(v)) for v in t.n)}; "
      f"dni bez zamówienia w tej godzinie: {15 - len(t)}; mediana z dniami zerowymi: "
      f"{np.median(list(t.n) + [0] * (15 - len(t))):.0f}.")
    J["godzina_zam_mediana"] = float(np.median(list(t.n) + [0] * (15 - len(t))))

    with open(os.path.join(WYNIKI, "e_merytoryka.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    with open(os.path.join(WYNIKI, "e_merytoryka.json"), "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1, default=lambda v: v.item() if hasattr(v, "item") else str(v))
    print("Zapisano analiza/wyniki/e_merytoryka.txt i e_merytoryka.json")


if __name__ == "__main__":
    main()
