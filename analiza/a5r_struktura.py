"""A5 retencja, krok 3 — zmiana struktury pacjentów a zmiana ich zachowania (2026-10-19).

Pytanie: czy niższy powrót w okresie 2 wynika z tego, że przychodzą inni pacjenci (inne kampanie, usługi,
zniżki, przebieg pierwszej wizyty), czy z tego, że podobni pacjenci wracają rzadziej.

Metoda (recenzja Codeksa w A4, PLAN.md A5):
  - powrót całej bazy obok powrotu przy stałej strukturze z okresu 1;
  - rozkład zmiany na: nowe segmenty (których nie było w okresie 1, np. TikTok, kampania Meta na L4),
    zmianę struktury i zmianę zachowania w segmentach obecnych w obu okresach (rozkład symetryczny:
    struktura = Σ (udział2 − udział1) · (stopa1 + stopa2) / 2, zachowanie = Σ (stopa2 − stopa1) · (udział1 + udział2) / 2);
  - rozkład na coraz drobniejszych podziałach (kanał → kampania → usługa → zniżka → przebieg pierwszej wizyty).
  Wynik po wyrównaniu struktury opisuje, ile różnicy przypada na skład, a ile na zachowanie wewnątrz podziałów.
  To nie jest dowód przyczyny.

Okno główne: powrót w 90 dniach, okresy na tych samych dniach kalendarzowych (okres 1: kohorty 1.10.2024 –
2.07.2025, okres 2: 1.10.2025 – 2.07.2026; ZALOZENIA.md 27). Kontrole: okno 30 dni, bez kohort z października,
reguła źródła Z2 (sesja płatności), liczby Codeksa z recenzji A4.

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/a5r_struktura.py
Wynik: analiza/wyniki/a5r_struktura.txt
"""

import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402

WYNIK = os.path.join(D.KATALOG, "analiza", "wyniki", "a5r_struktura.txt")
KONIEC = D.KONIEC
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)

USLUGA = """
  CASE WHEN z.specialization = 'internista' THEN 'internista_' || z.visit_purpose
       WHEN z.specialization IN ('pediatra', 'psychiatra') THEN z.specialization
       ELSE 'inny_specjalista' END"""
ZNIZKA = """
  CASE WHEN z.discount_type = 'go' THEN 'TelemediGO' WHEN z.discount_type = 'promo' THEN z.promo_code ELSE 'brak' END"""
GRUPA = """
  CASE WHEN r.kampania = 'meta_prosp_lekarz_online' THEN '1_meta_lekarz_online'
       WHEN r.kampania = 'meta_prosp_l4_szybko' THEN '2_meta_l4_szybko'
       WHEN r.kanal = 'tiktok' THEN '3_tiktok'
       ELSE '4_pozostale_kanaly' END"""


def zbuduj_atr(con):
    """`atr`: nowy pacjent z cechami pierwszego zakupu i miarami powrotu oraz marży w 30 i 90 dniach."""
    con.execute(f"""
      CREATE TEMP TABLE atr AS
      SELECT p.user_id, p.d0, p.okres, p.dni_R2, r.kanal, r.kampania, r.kanal_z2, r.kampania_z2,
             {GRUPA} grupa, {USLUGA} usluga, z.visit_purpose cel, {ZNIZKA} znizka, z.status status1,
             z.consultation_mode tryb, s.device urzadzenie,
             CASE WHEN s.browser IN ('Instagram', 'Facebook', 'TikTok') THEN 'aplikacja_' || s.browser ELSE 'przegladarka' END przegladarka,
             coalesce(m.marza90, 0) marza90, coalesce(m.marza30, 0) marza30, coalesce(m.marza0, 0) marza0
      FROM powr p JOIN zrodlo r USING (user_id) JOIN zam z ON z.user_id = p.user_id AND z.nr = 1
      JOIN czyste.sessions s ON s.session_id = z.session_id
      LEFT JOIN (SELECT user_id, sum(marza) FILTER (WHERE dni <= 90) marza90, sum(marza) FILTER (WHERE dni <= 30) marza30,
                        sum(marza) FILTER (WHERE dni = 0) marza0
                 FROM ek GROUP BY 1) m ON m.user_id = p.user_id""")


def proba(atr, okno, bez_pazdziernika=False, por=True):
    """Pacjenci z pełnym oknem, okresy na tych samych dniach kalendarzowych (por=True) albo okres 1 w całości."""
    g1, g2 = D.granice_por(okno)
    if not por:
        g1 = dt.date(2025, 9, 30)
    a = atr[((atr.okres == 1) & (atr.d0 <= pd.Timestamp(g1))) | ((atr.okres == 2) & (atr.d0 <= pd.Timestamp(g2)))].copy()
    if bez_pazdziernika:
        a = a[a.d0.dt.month != 10]
    a["y"] = (a.dni_R2 <= okno).astype(float)
    return a


PELNE = pd.MultiIndex.from_product([["count", "mean"], [1, 2]])


def rozklad(a, wymiary, miara="y"):
    """Rozkład różnicy okres 2 − okres 1 (w jednostkach miary: punkty procentowe dla powrotu, zł dla marży)."""
    g = a.groupby(wymiary + ["okres"])[miara].agg(["count", "mean"]).unstack("okres").reindex(columns=PELNE)
    n1, n2 = g[("count", 1)].fillna(0), g[("count", 2)].fillna(0)
    r1, r2 = g[("mean", 1)], g[("mean", 2)]
    R1, R2 = (n1 * r1.fillna(0)).sum() / n1.sum(), (n2 * r2.fillna(0)).sum() / n2.sum()
    C = (n1 > 0) & (n2 > 0)
    s1, s2 = n1[C] / n1[C].sum(), n2[C] / n2[C].sum()
    r1C, r2C = (s1 * r1[C]).sum(), (s2 * r2[C]).sum()
    skala = 100 if miara == "y" else 1
    return {"podzial": " x ".join(wymiary), "komorki_wspolne": int(C.sum()),
            "n_o1": int(n1.sum()), "n_o2": int(n2.sum()),
            "pokrycie_o1_proc": round(100 * n1[C].sum() / n1.sum(), 1), "pokrycie_o2_proc": round(100 * n2[C].sum() / n2.sum(), 1),
            "o1": round(skala * R1, 2), "o2": round(skala * R2, 2), "zmiana": round(skala * (R2 - R1), 2),
            "nowe_segmenty": round(skala * (R2 - r2C), 2), "znikniete": round(skala * (r1C - R1), 2),
            "struktura": round(skala * ((s2 - s1) * (r1[C] + r2[C]) / 2).sum(), 2),
            "zachowanie": round(skala * ((r2[C] - r1[C]) * (s1 + s2) / 2).sum(), 2),
            "o2_przy_strukturze_o1": round(skala * (s1 * r2[C]).sum(), 2)}


def tabela_segmentow(a, wymiar, miara="y", min_n=0):
    g = a.groupby([wymiar, "okres"])[miara].agg(["count", "mean"]).unstack("okres").reindex(columns=PELNE)
    skala = 100 if miara == "y" else 1
    t = pd.DataFrame({
        "n_o1": g[("count", 1)].fillna(0).astype(int), "n_o2": g[("count", 2)].fillna(0).astype(int)})
    t["udzial_o1"] = (100 * t.n_o1 / t.n_o1.sum()).round(1)
    t["udzial_o2"] = (100 * t.n_o2 / t.n_o2.sum()).round(1)
    t["o1"] = (skala * g[("mean", 1)]).round(1)
    t["o2"] = (skala * g[("mean", 2)]).round(1)
    t["zmiana"] = (t.o2 - t.o1).round(1)
    t = t[(t.n_o1 + t.n_o2) >= min_n]
    return t.sort_values("n_o2", ascending=False).reset_index()


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False)
    zbuduj_atr(con)
    atr = con.sql("SELECT * FROM atr").df()
    atr["d0"] = pd.to_datetime(atr.d0)
    atr["dni_R2"] = atr.dni_R2.astype(float)   # brak powrotu = NaN, porównanie daje False (nie wypada z mianownika)
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    def df(sql):
        return con.sql(sql).df()

    r(f"A5 RETENCJA — STRUKTURA PACJENTÓW A ICH ZACHOWANIE ({dt.datetime.now():%Y-%m-%d %H:%M})")
    r("Schemat `czyste`, definicje z analiza/definicje.py. Powrót R2 (kolejne zamówienie nieanulowane), źródło Z1K.")
    r("Okno główne 90 dni, okresy na tych samych dniach kalendarzowych: okres 1 = kohorty 1.10.2024–2.07.2025,")
    r("okres 2 = kohorty 1.10.2025–2.07.2026. Zmiany w punktach procentowych (powrót) albo w zł (marża na pacjenta).")
    r("Rozkład: zmiana = nowe_segmenty + znikniete + struktura + zachowanie. nowe_segmenty = wpływ pacjentów z komórek,")
    r("których nie było w okresie 1 (np. TikTok); struktura i zachowanie liczone w komórkach obecnych w obu okresach.")
    r("o2_przy_strukturze_o1 = powrót okresu 2, gdyby komórki wspólne miały udziały z okresu 1.")
    r("Składniki zaokrąglane osobno, więc ich suma może różnić się od zmiany o 0,01. Rozkład jest opisowy: „nowe")
    r("segmenty” to różnica między okresem 2 z tymi pacjentami i bez nich, a „zachowanie” to reszta, której nie")
    r("tłumaczą uwzględnione cechy (recenzja Codeksa, notatki/recenzje/a5r_codex.md).")

    # ============ 0. LICZBY CODEKSA ============
    r("\n" + "=" * 120)
    r("0. POWTÓRZENIE LICZB CODEKSA Z RECENZJI A4 (okres 1 w całości, okres 2 do 2.07.2026, kanał Z1K, 90 dni)")
    r("=" * 120)
    a_cx = proba(atr, 90, por=False)
    x = rozklad(a_cx, ["kanal"])
    r(f"     okres 1 (całość): {x['o1']:.2f}% (n = {x['n_o1']}), okres 2: {x['o2']:.2f}% (n = {x['n_o2']}),")
    r(f"     okres 2 przy strukturze kanałów okresu 1 (TikTok z wagą 0): {x['o2_przy_strukturze_o1']:.2f}%   [Codex: 23,60 / 17,38 / 21,29]")
    a_cx2 = a_cx[~((a_cx.okres == 1) & (a_cx.d0.dt.month == 10) & (a_cx.d0.dt.year == 2024))]
    y = rozklad(a_cx2, ["kanal"])
    r(f"     okres 1 bez kohort z października 2024: {y['o1']:.2f}% (n = {y['n_o1']}), okres 2: {y['o2']:.2f}%   [Codex: 23,72 / 17,38]")

    # ============ 1. ROZKŁAD NA CORAZ DROBNIEJSZYCH PODZIAŁACH ============
    a90 = proba(atr, 90)
    poziomy = [["kanal"], ["kampania"], ["usluga"], ["znizka"], ["status1"], ["przegladarka"], ["urzadzenie"],
               ["kampania", "usluga"], ["kampania", "usluga", "znizka"],
               ["kampania", "usluga", "znizka", "status1"],
               ["kampania", "usluga", "znizka", "status1", "przegladarka"]]
    r("\n" + "=" * 120)
    r("1. ROZKŁAD ZMIANY POWROTU W 90 DNIACH (punkty procentowe), okresy na tych samych dniach kalendarzowych")
    r("=" * 120)
    pokaz(pd.DataFrame([rozklad(a90, p) for p in poziomy]))
    r("     pokrycie = % pacjentów okresu w komórkach obecnych w obu okresach. Przy drobnych podziałach rośnie szum")
    r("     w małych komórkach; status pierwszego zamówienia to przebieg wizyty, który sam może zależeć od kampanii.")

    r("\n1b. To samo bez pacjentów dwóch nowych kampanii (meta_prosp_l4_szybko od 3.11.2025, tt_prosp_l4_15min od 9.02.2026)")
    a90b = a90[~a90.kampania.isin(["meta_prosp_l4_szybko", "tt_prosp_l4_15min"])]
    pokaz(pd.DataFrame([rozklad(a90b, p) for p in poziomy[:2] + poziomy[2:5] + [["kampania", "usluga"],
                                                                                 ["kampania", "usluga", "znizka", "status1"]]]))

    r("\n1c. Rozkład zmiany marży na pacjenta w 90 dniach (zł, przed kosztem pozyskania)")
    pokaz(pd.DataFrame([rozklad(a90, p, "marza90") for p in (["kanal"], ["kampania"], ["usluga"], ["kampania", "usluga"],
                                                               ["kampania", "usluga", "znizka", "status1"])]))

    # ============ 2. SEGMENTY ============
    r("\n" + "=" * 120)
    r("2. POWRÓT W 90 DNIACH W SEGMENTACH (%, te same dni kalendarzowe); zmiana w punktach procentowych")
    r("=" * 120)
    for w in ("kanal", "kampania", "usluga", "znizka", "status1", "przegladarka", "urzadzenie", "tryb", "grupa"):
        r(f"\n2.{w}")
        pokaz(tabela_segmentow(a90, w))
    r("\n2.kanal bez dwóch nowych kampanii")
    pokaz(tabela_segmentow(a90b, "kanal"))

    # ============ 3. META NA POZIOMIE KAMPANII ============
    r("\n" + "=" * 120)
    r("3. META NA POZIOMIE KAMPANII")
    r("=" * 120)
    r("3a. Kohorty miesięczne według grupy kampanii: liczba nowych pacjentów i powrót w 30 i 90 dniach (%)")
    r("    (powrót tylko dla miesięcy z pełnym oknem dla wszystkich dni miesiąca)")
    t = df(f"""
      SELECT strftime(date_trunc('month', d0), '%Y-%m') miesiac, grupa, count(*) n,
             CASE WHEN last_day(min(d0)) <= DATE '{KONIEC}' - 30 THEN round(100.0 * count(*) FILTER (WHERE dni_R2 <= 30) / count(*), 1) END p30,
             CASE WHEN last_day(min(d0)) <= DATE '{KONIEC}' - 90 THEN round(100.0 * count(*) FILTER (WHERE dni_R2 <= 90) / count(*), 1) END p90
      FROM atr GROUP BY 1, 2 ORDER BY 1, 2""")
    piv = t.pivot(index="miesiac", columns="grupa", values=["n", "p30", "p90"])
    piv.columns = [f"{b[2:]}_{a}" for a, b in piv.columns]
    piv = piv[[c for g in sorted(t.grupa.unique()) for c in (f"{g[2:]}_n", f"{g[2:]}_p30", f"{g[2:]}_p90")]]
    pokaz(piv.reset_index())

    for kamp in ("meta_prosp_lekarz_online", "meta_prosp_l4_szybko"):
        a_k = a90[a90.kampania == kamp]
        r(f"\n3b. {kamp}: powrót w 90 dniach według pierwszej usługi, zniżki i statusu pierwszego zamówienia")
        for w in ("usluga", "znizka", "status1", "przegladarka"):
            pokaz(tabela_segmentow(a_k, w))
            r("")
        if (a_k.okres == 1).sum() == 0:
            r(f"     {kamp} nie ma pacjentów w okresie 1, więc rozkładu w jej obrębie nie liczymy.")
            continue
        r(f"     Rozkład w obrębie {kamp}:")
        pokaz(pd.DataFrame([rozklad(a_k, p) for p in (["usluga"], ["usluga", "znizka"], ["usluga", "znizka", "status1"])]))

    r("\n3c. Meta pozyskanie razem: rozkład zmiany na kampanie i zachowanie w kampaniach (90 dni)")
    a_m = a90[a90.kanal == "meta_pozyskanie"]
    pokaz(pd.DataFrame([rozklad(a_m, p) for p in (["kampania"], ["kampania", "usluga"], ["kampania", "usluga", "status1"])]))

    r("\n3d. Pierwsza usługa L4 u internisty (L4 z L4): powrót w 90 dniach według grupy kampanii i kanału")
    a_l4 = a90[a90.usluga == "internista_l4"]
    pokaz(tabela_segmentow(a_l4, "grupa"))
    r("")
    pokaz(tabela_segmentow(a_l4, "kanal"))
    r("     Rozkład w obrębie pierwszego zamówienia L4:")
    pokaz(pd.DataFrame([rozklad(a_l4, p) for p in (["kampania"], ["kampania", "znizka"], ["kampania", "znizka", "status1"])]))

    # ============ 4. TIKTOK OSOBNO ============
    r("\n" + "=" * 120)
    r("4. TIKTOK JAKO NOWY SEGMENT (tylko okres 2; kohorty z pełnym oknem)")
    r("=" * 120)
    for okno in (30, 60, 90):
        a_t = atr[(atr.kanal == "tiktok") & (atr.d0 <= pd.Timestamp(D.granice_por(okno)[1]))]
        reszta = atr[(atr.kanal != "tiktok") & (atr.okres == 2) & (atr.d0 >= pd.Timestamp("2026-02-09"))
                     & (atr.d0 <= pd.Timestamp(D.granice_por(okno)[1]))]
        r(f"     {okno} dni: TikTok {100 * (a_t.dni_R2 <= okno).mean():.1f}% (n = {len(a_t)}); pozostałe kanały w tych samych "
          f"dniach od 9.02.2026: {100 * (reszta.dni_R2 <= okno).mean():.1f}% (n = {len(reszta)})")
    a_t90 = atr[(atr.kanal == "tiktok") & (atr.d0 <= pd.Timestamp(D.granice_por(90)[1]))].copy()
    a_t90["y"] = (a_t90.dni_R2 <= 90).astype(float)
    for w in ("usluga", "znizka", "status1", "przegladarka"):
        g = a_t90.groupby(w).y.agg(["count", "mean"]).reset_index()
        g["mean"] = (100 * g["mean"]).round(1)
        pokaz(g.rename(columns={"count": "n", "mean": "powrot90"}).sort_values("n", ascending=False))
        r("")
    r(f"     Udział TikToka w okresie 2 (kohorty do 2.07.2026): {100 * (a90[a90.okres == 2].kanal == 'tiktok').mean():.1f}% pacjentów.")
    bez_tt = a90[(a90.okres == 2) & (a90.kanal != "tiktok")]
    r(f"     Powrót okresu 2 bez TikToka: {100 * bez_tt.y.mean():.2f}% (n = {len(bez_tt)}) wobec {100 * a90[a90.okres == 2].y.mean():.2f}% z TikTokiem.")

    # ============ 5. KONTROLE ============
    r("\n" + "=" * 120)
    r("5. KONTROLE WRAŻLIWOŚCI ROZKŁADU (kanał i kampania x usługa x zniżka x status)")
    r("=" * 120)
    kontrole = []
    for etyk, a_k in (("90 dni, te same dni (główny)", a90),
                      ("30 dni, te same dni", proba(atr, 30)),
                      ("60 dni, te same dni", proba(atr, 60)),
                      ("90 dni, bez kohort z października w obu okresach", proba(atr, 90, bez_pazdziernika=True)),
                      ("90 dni, okres 1 w całości", proba(atr, 90, por=False))):
        for p in (["kanal"], ["kampania", "usluga", "znizka", "status1"]):
            d = rozklad(a_k, p)
            d = {"wariant": etyk, **d}
            kontrole.append(d)
    a90z2 = a90.copy()
    a90z2["kanal"], a90z2["kampania"] = a90z2.kanal_z2, a90z2.kampania_z2
    for p in (["kanal"], ["kampania"], ["kampania", "usluga"], ["kampania", "usluga", "znizka", "status1"]):
        kontrole.append({"wariant": "90 dni, źródło według sesji płatności (Z2)", **rozklad(a90z2, p)})
    k = pd.DataFrame(kontrole)
    pokaz(k[["wariant", "podzial", "n_o1", "n_o2", "o1", "o2", "zmiana", "nowe_segmenty", "znikniete", "struktura",
             "zachowanie", "o2_przy_strukturze_o1", "pokrycie_o2_proc"]])
    nowe_z2 = a90z2.kampania.isin(["meta_prosp_l4_szybko", "tt_prosp_l4_15min"])
    r(f"     Pacjenci dwóch nowych kampanii: {int((a90.kampania.isin(['meta_prosp_l4_szybko', 'tt_prosp_l4_15min'])).sum())}"
      f" według Z1K, {int(nowe_z2.sum())} według sesji płatności (Z2). Przy podziale z usługą, zniżką i statusem „nowe")
    r("     segmenty” obejmują też nowe komórki w kampaniach obecnych w obu okresach, więc porównujemy reguły na poziomie kampanii.")

    r("\n5a. Małe komórki w podziale kampania x usługa x zniżka x status (90 dni)")
    g = a90.groupby(["kampania", "usluga", "znizka", "status1", "okres"]).size().unstack("okres").fillna(0)
    wsp = g[(g[1] > 0) & (g[2] > 0)]
    male = wsp[(wsp[1] < 10) | (wsp[2] < 10)]
    r(f"     Komórek wspólnych: {len(wsp)}, z nich z mniej niż 10 pacjentami w którymś okresie: {len(male)}, obejmują "
      f"{100 * male.values.sum() / wsp.values.sum():.1f}% pacjentów komórek wspólnych.")

    r("\n5c. Pierwsze L4 u internisty na wspólnych datach pozyskania (kohorty 9.02.2026–2.07.2026, wszystkie grupy naraz)")
    a_l4w = a90[(a90.usluga == "internista_l4") & (a90.d0 >= pd.Timestamp("2026-02-09"))]
    pokaz(tabela_segmentow(a_l4w.assign(okres=2), "grupa")[["grupa", "n_o2", "o2"]].rename(columns={"n_o2": "n", "o2": "powrot90"}))
    r("\n5d. Rozkład bez dwóch nowych kampanii według miesiąca kohorty (struktura miesięcy a spadek wewnątrz miesięcy)")
    a90b_m = a90b.assign(mies=a90b.d0.dt.month)
    pokaz(pd.DataFrame([rozklad(a90b_m, ["mies"]), rozklad(a90b_m, ["mies", "kampania"])]))

    r("\n5b. Te same miesiące rok do roku, bez dwóch nowych kampanii: powrót w 90 dniach (%)")
    t = df(f"""
      SELECT strftime(d0, '%m') mm, okres, count(*) n,
             CASE WHEN max(d0) <= DATE '{KONIEC}' - 90 THEN round(100.0 * count(*) FILTER (WHERE dni_R2 <= 90) / count(*), 1) END p90
      FROM atr WHERE kampania NOT IN ('meta_prosp_l4_szybko', 'tt_prosp_l4_15min') GROUP BY 1, 2 ORDER BY 1, 2""")
    pv = t.pivot(index="mm", columns="okres", values=["n", "p90"])
    pv.columns = [f"{a}_o{b}" for a, b in pv.columns]
    pv["zmiana_pkt"] = (pv.p90_o2 - pv.p90_o1).round(1)
    pv = pv.reset_index()
    pv["kolejnosc"] = (pv.mm.astype(int) - 10) % 12
    pokaz(pv.sort_values("kolejnosc").drop(columns="kolejnosc"))

    # ============ 6. NIEPEWNOŚĆ I MARŻA ============
    r("\n" + "=" * 120)
    r("6. NIEPEWNOŚĆ KLUCZOWYCH RÓŻNIC (powrót w 90 dniach, te same dni; 95% przedział, przybliżenie normalne)")
    r("=" * 120)
    wiersze = []
    for etyk, maska in (("wszyscy", a90.okres > 0),
                        ("bez dwóch nowych kampanii", ~a90.kampania.isin(["meta_prosp_l4_szybko", "tt_prosp_l4_15min"])),
                        ("meta_prosp_lekarz_online", a90.kampania == "meta_prosp_lekarz_online"),
                        ("L4 u internisty, pozostałe kanały", (a90.usluga == "internista_l4") & (a90.grupa == "4_pozostale_kanaly"))
                        ) + tuple((f"kampania {k}", a90.kampania == k) for k in (
                            "google_organic", "bezposrednie", "gs_brand", "gs_generic_lekarz_online", "gs_generic_erecepta",
                            "gs_generic_l4", "gs_generic_specjalisci", "program_polecen", "rankinglekarzy_affiliate")):
        x = a90[maska]
        p1, p2 = x[x.okres == 1].y, x[x.okres == 2].y
        d = p2.mean() - p1.mean()
        se = np.sqrt(p1.mean() * (1 - p1.mean()) / len(p1) + p2.mean() * (1 - p2.mean()) / len(p2))
        wiersze.append({"grupa": etyk, "n_o1": len(p1), "n_o2": len(p2), "o1": round(100 * p1.mean(), 1),
                        "o2": round(100 * p2.mean(), 1), "zmiana_pkt": round(100 * d, 1),
                        "od": round(100 * (d - 1.96 * se), 1), "do": round(100 * (d + 1.96 * se), 1)})
    pokaz(pd.DataFrame(wiersze))

    r("\n6b. Marża na pacjenta (zł, przed kosztem pozyskania): dzień 0 (pierwsze zamówienie i TelemediGO przy kasie)")
    r("    i dni 1–90; te same dni kalendarzowe, okno 90 dni")
    wiersze = []
    for etyk, maska in (("wszyscy", a90.okres > 0),
                        ("bez dwóch nowych kampanii", ~a90.kampania.isin(["meta_prosp_l4_szybko", "tt_prosp_l4_15min"])),
                        ("dwie nowe kampanie", a90.kampania.isin(["meta_prosp_l4_szybko", "tt_prosp_l4_15min"]))):
        for o in (1, 2):
            x = a90[maska & (a90.okres == o)]
            if len(x):
                wiersze.append({"grupa": etyk, "okres": o, "n": len(x), "marza_dzien0": round(x.marza0.mean(), 1),
                                "marza_dni_1_90": round((x.marza90 - x.marza0).mean(), 1), "marza_90": round(x.marza90.mean(), 1),
                                "powrot90": round(100 * x.y.mean(), 1)})
    pokaz(pd.DataFrame(wiersze))

    con.close()
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Raport: {os.path.relpath(WYNIK, D.KATALOG)} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
