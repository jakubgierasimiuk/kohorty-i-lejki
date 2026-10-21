"""D — kampanie: sześć sprawdzeń po konsylium końcowej weryfikacji (2026-10-21).

Pytania z notatki notatki/d_poprawki.md (lista Kuby) i z syntezy konsylium (notatki/konsylium/d_weryfikacja/synteza.md):
  1. przeglądarki wbudowane w aplikacje (Instagram, Facebook, TikTok) a zwykłe POZA nowymi kampaniami na L4;
  2. TikTok na L4 po 180 dniach: z jakich kohort i z jakim kosztem pozyskania, przybliżenie dla całego rocznika;
     to samo krótko dla Meta na L4;
  3. tempo wydatków i pozyskania nowych kampanii w ostatnim półroczu (1.04–30.09.2026) a kwoty „na pełny rok” (P11);
  4. koszt kliknięcia w Google Ads miesięcznie, okres 1 wobec okresu 2, i koszt na pierwsze zamówienie;
  5. Google Ads na markę (gs_brand): spadek konwersji od 22.05.2026 — potwierdzenie i możliwe wyjaśnienia;
  6. kod rabatowy na pierwszym zamówieniu pacjentów nowych kampanii: odsetek, kody, zniżka, koszt, zwroty, powroty.

Definicje (bez zmian, tylko import): analiza/definicje.py (nowy pacjent, powrót, źródło Z1K i Z2, marża na pacjenta,
ZALOZENIA.md 16–34), analiza/a5e_ekonomia.py (koszt pozyskania z tych samych dni co kohorty i wynik na pacjenta,
ZALOZENIA.md 39–40). Lejek jak w analiza/a5p_lejek.py: sesje zwykłe, dzień sesji w czasie polskim, „jeszcze nie
kupowali” według pierwszego zakupu konta albo przeglądarki (ZALOZENIA.md 28–29). Przeliczenie na pełny rok jak
w analiza/c_priorytety.py, P11 (ZALOZENIA.md 53–54).

Okres 1 = 1.10.2024–30.09.2025, okres 2 = 1.10.2025–30.09.2026 (czas polski). Tylko czyta schemat `czyste`.
Uruchomienie z głównego folderu projektu:
    python -I analiza/d_kampanie.py
Wynik: analiza/wyniki/d_kampanie.txt (raport) i analiza/wyniki/d_kampanie.json (najważniejsze liczby, płaski słownik).
"""

import datetime as dt
import json
import math
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
import a5e_ekonomia as E  # noqa: E402

WYNIKI = os.path.join(D.KATALOG, "analiza", "wyniki")
WYNIK = os.path.join(WYNIKI, "d_kampanie.txt")
WYNIK_JSON = os.path.join(WYNIKI, "d_kampanie.json")
NOWE = E.NOWE
WBUD = ("Instagram", "Facebook", "TikTok")
AWARIA = "2026-03-17"          # awaria zakładania konta w Safari na iOS (a5p_zdarzenia.txt, 5)
POLROCZE = ("2026-04-01", "2026-09-30")
REGULY = (("Z1K", "kampania", "kanal"), ("Z2", "kampania_z2", "kanal_z2"))
SKROT = {"meta_prosp_l4_szybko": "meta_l4", "tt_prosp_l4_15min": "tiktok_l4"}
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


def wilson(k, n, z=1.96):
    if n <= 0:
        return (np.nan, np.nan)
    p = k / n
    mian = 1 + z * z / n
    c = (p + z * z / (2 * n)) / mian
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / mian
    return c - h, c + h


def newcombe(k1, n1, k2, n2):
    """Różnica odsetków p1 − p2 i jej 95% przedział (metoda Newcombe'a z przedziałów Wilsona)."""
    if n1 <= 0 or n2 <= 0:
        return (np.nan, np.nan, np.nan)
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


def werdykt(n_wb, lo, hi, min_n=300):
    if n_wb < min_n or np.isnan(lo):
        return "za mała próba"
    if hi < 0:
        return "rzadziej"
    if lo > 0:
        return "częściej"
    return "bez istotnej różnicy"


def zl(x):
    return f"{x:,.0f} zł".replace(",", " ")


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=True)
    pe = E.zbuduj_pe(con)
    wyd = E.zbuduj_wyd(con)
    q = lambda s: con.sql(s).df()  # noqa: E731
    linie = []
    J = {}

    def r(tekst=""):
        linie.append(tekst)

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    def naglowek(t):
        r("\n" + "=" * 110)
        r(t)
        r("=" * 110)

    def j(klucz, wartosc):
        """Zapis do JSON: liczby całkowite bez zmian, ułamki z 4 miejscami."""
        if wartosc is None or (isinstance(wartosc, float) and np.isnan(wartosc)):
            J[klucz] = None
        elif isinstance(wartosc, (int, np.integer)):
            J[klucz] = int(wartosc)
        else:
            J[klucz] = round(float(wartosc), 4)

    r(f"D — KAMPANIE: SZEŚĆ SPRAWDZEŃ PO KONSYLIUM ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Okres 1 = 1.10.2024–30.09.2025, okres 2 = 1.10.2025–30.09.2026 (czas polski). Z1K = przyjęta reguła źródła (pierwsze")
    r("wejście, kod kampanii rozstrzyga), Z2 = sesja płatności. Nowe kampanie = meta_prosp_l4_szybko (Meta na L4, od 3.11.2025)")
    r("i tt_prosp_l4_15min (TikTok na L4, od 9.02.2026). Przeglądarki wbudowane w aplikacje = Instagram, Facebook, TikTok.")
    r("Przedziały 95%: różnica odsetków metodą Newcombe'a (Wilson); wynik na pacjenta jak w a5e_ekonomia.py (warunkowy,")
    r("tylko z rozrzutu marży). Werdykt „za mała próba”, gdy sesji w przeglądarkach wbudowanych jest mniej niż 300.")

    # ======================= tabela sesji (jak a5p_lejek.py) =======================
    con.execute("""
      CREATE TEMP TABLE ev_l AS
      SELECT session_id, max((event_name = 'service_selected')::INT) k1, max((event_name = 'slot_selected')::INT) k2,
             max((event_name = 'account_completed')::INT) k3, max((event_name = 'payment_started')::INT) k4,
             max((event_name = 'payment_succeeded')::INT) k5
      FROM czyste.events GROUP BY 1""")
    con.execute("CREATE TEMP TABLE pierwszy_l AS SELECT user_id, min(created_at) t FROM czyste.orders GROUP BY 1")
    con.execute(f"""
      CREATE TEMP TABLE sl AS
      SELECT s.session_id, s.dzien_pl dzien, s.device, s.browser, s.os, s.landing_page,
             {D.KANAL} kanal, coalesce(s.utm_campaign, s.utm_source || '_' || s.utm_medium, 'bezposrednie') kampania,
             CASE WHEN s.dzien_pl < DATE '{D.OKRES2}' THEN 1 ELSE 2 END okres,
             CASE WHEN g.session_id IS NOT NULL THEN 'samo_telemedigo'
                  WHEN s.user_id IS NOT NULL AND coalesce(e.k3, 0) = 0 THEN 'zalogowana_od_wejscia'
                  ELSE 'zwykla' END typ,
             CASE WHEN pz.t < s.started_at_pl THEN 'kupowal_wczesniej' ELSE 'nie_kupowal' END pacjent,
             coalesce(e.k1, 0) k1, coalesce(e.k2, 0) k2, coalesce(e.k3, 0) k3, coalesce(e.k4, 0) k4, coalesce(e.k5, 0) k5,
             s.browser IN {WBUD} wbud, (s.os = 'iOS' AND s.browser = 'Safari') ios_safari,
             (o.order_id IS NOT NULL)::INT zamowienie, coalesce(o.nr = 1, FALSE)::INT pierwsze_zamowienie
      FROM czyste.sessions s
      LEFT JOIN ev_l e USING (session_id)
      LEFT JOIN (SELECT DISTINCT session_id FROM czyste.go_memberships WHERE order_id IS NULL) g USING (session_id)
      LEFT JOIN przeg p ON p.visitor_id = s.visitor_id AND s.user_id IS NULL
      LEFT JOIN pierwszy_l pz ON pz.user_id = coalesce(s.user_id, p.user_id)
      LEFT JOIN zam o ON o.session_id = s.session_id""")
    kon = q("SELECT count(*) sesje, count(DISTINCT session_id) unikalne, sum(k5) platnosci, count(*) FILTER (WHERE typ = 'zwykla') zwykle FROM sl")
    r("\nKontrola tabeli sesji: " + ", ".join(f"{k} = {int(v)}" for k, v in kon.iloc[0].items()))

    # ======================= 1. PRZEGLĄDARKI WBUDOWANE =======================
    naglowek("1. PRZEGLĄDARKI WBUDOWANE W APLIKACJE A ZWYKŁE, W TEJ SAMEJ KAMPANII, TAKŻE POZA NOWYMI KAMPANIAMI NA L4")
    r("1a. Odtworzenie obecnego wniosku (a5e_scenariusze.txt, E2c): wszystkie sesje kampanii w okresie 2 (wszystkie typy),")
    r("    pierwsze zamówienie pacjenta zapłacone w tej samej sesji / sesje.")
    e2c = q(f"""
      SELECT kampania, CASE WHEN wbud THEN 'wbudowana' ELSE 'zwykla' END przegladarka, count(*) sesje,
             sum(pierwsze_zamowienie) pierwsze_zamowienia, 100.0 * sum(pierwsze_zamowienie) / count(*) konwersja_proc
      FROM sl WHERE kampania IN {NOWE} AND okres = 2 GROUP BY ALL ORDER BY 1, 2""")
    pokaz(e2c.round(2))
    for _, w in e2c.iterrows():
        k = f"p1_e2c_{SKROT[w.kampania]}_{w.przegladarka}"
        j(k + "_konwersja_do_pierwszego_zamowienia_proc", w.konwersja_proc)
        j(k + "_sesje", w.sesje)
        j(k + "_pierwsze_zamowienia", w.pierwsze_zamowienia)

    r("\n1b. Ta sama porównywarka metodą lejka z a5p_lejek.py: sesje zwykłe, sesja do płatności (k5 / sesje), wszystkie kampanie")
    r("    z choć jedną sesją zwykłą w przeglądarce wbudowanej, okres 1 i okres 2. Grupa porównawcza: wszystkie zwykłe")
    r("    przeglądarki tej samej kampanii (V1). roznica_pkt = wbudowana − zwykła w punktach procentowych, od/do = 95%.")

    def tabela(warunek_zw):
        t = q(f"""
          SELECT kampania, okres,
                 count(*) FILTER (WHERE wbud) n_wb, sum(k5) FILTER (WHERE wbud) k5_wb,
                 count(*) FILTER (WHERE NOT wbud AND {warunek_zw}) n_zw, sum(k5) FILTER (WHERE NOT wbud AND {warunek_zw}) k5_zw,
                 {', '.join(f'sum(k{i}) FILTER (WHERE wbud) k{i}_wb, sum(k{i}) FILTER (WHERE NOT wbud AND {warunek_zw}) k{i}_zw' for i in range(1, 5))}
          FROM sl WHERE typ = 'zwykla' GROUP BY 1, 2 HAVING count(*) FILTER (WHERE wbud) > 0 ORDER BY 1, 2""")
        t = t.fillna(0)
        rows = []
        for _, w in t.iterrows():
            d, lo, hi = newcombe(w.k5_wb, w.n_wb, w.k5_zw, w.n_zw)
            rows.append({"kampania": w.kampania, "okres": int(w.okres), "sesje_wbud": int(w.n_wb), "platn_wbud": int(w.k5_wb),
                         "proc_wbud": 100 * w.k5_wb / w.n_wb, "sesje_zwykle": int(w.n_zw), "platn_zwykle": int(w.k5_zw),
                         "proc_zwykle": 100 * w.k5_zw / w.n_zw if w.n_zw else np.nan,
                         "roznica_pkt": 100 * d, "od": 100 * lo, "do": 100 * hi, "werdykt": werdykt(w.n_wb, lo, hi)})
        return t, pd.DataFrame(rows)

    t_v1, w_v1 = tabela("TRUE")
    pokaz(w_v1.round(2))
    r("\n1c. To samo z grupą porównawczą V2: zwykłe przeglądarki na telefonie i tablecie (jak przeglądarki wbudowane), bez")
    r(f"    Safari na iOS od {AWARIA} (awaria zakładania konta obniża zwykłe przeglądarki w okresie 2).")
    t_v2, w_v2 = tabela(f"device IN ('mobile', 'tablet') AND NOT (ios_safari AND dzien >= DATE '{AWARIA}')")
    pokaz(w_v2.round(2))
    for nazwa, w_ in (("v1", w_v1), ("v2", w_v2)):
        for _, w in w_.iterrows():
            if w.sesje_wbud >= 300:
                k = f"p1_{nazwa}_{w.kampania}_okres{w.okres}"
                j(k + "_sesja_do_platnosci_wbudowane_proc", w.proc_wbud)
                j(k + "_sesje_wbudowane", w.sesje_wbud)
                j(k + "_sesja_do_platnosci_zwykle_proc", w.proc_zwykle)
                j(k + "_sesje_zwykle", w.sesje_zwykle)
                j(k + "_roznica_pkt", w.roznica_pkt)
                j(k + "_roznica_od_pkt", w["od"])
                j(k + "_roznica_do_pkt", w["do"])

    r("\n1d. Kroki lejka (konwersja kroku wobec poprzedniego, %) w kampaniach z co najmniej 300 sesjami w przeglądarkach")
    r("    wbudowanych, V1. usl = wybór usługi / sesje, term = termin / usługa, log = konto / termin, wpl = wejście na")
    r("    płatność / konto, pl = płatność / wejście na płatność; _wb = wbudowana, _zw = zwykła.")
    kr = t_v1[t_v1.n_wb >= 300].copy()
    out = pd.DataFrame({"kampania": kr.kampania, "okres": kr.okres.astype(int)})
    for nazwa, licz, mian in (("usl", "k1", "n"), ("term", "k2", "k1"), ("log", "k3", "k2"), ("wpl", "k4", "k3"), ("pl", "k5", "k4")):
        for g in ("wb", "zw"):
            out[f"{nazwa}_{g}"] = (100 * kr[f"{licz}_{g}"] / kr[f"{mian}_{g}"].where(kr[f"{mian}_{g}"] > 0)).round(1)
    pokaz(out)

    r("\n1e. Zbiorczo: różnica wbudowana − zwykła w obrębie tej samej kampanii, okresu i typu odwiedzającego (jeszcze nie")
    r("    kupowali / kupowali wcześniej), ważona sesjami w przeglądarkach wbudowanych (standaryzacja bezpośrednia).")
    r("    oczekiwane_platn = ile płatności dałyby sesje w przeglądarkach wbudowanych, gdyby płaciły jak zwykłe w tej samej")
    r("    warstwie; iloraz = faktyczne / oczekiwane. Warstwy bez sesji zwykłych pomijamy (pominiete_wbud). Przedział z")
    r("    przybliżenia normalnego (suma wariancji warstw).")

    def warstwy(warunek_zw, przegl=None):
        wb = f"wbud AND browser = '{przegl}'" if przegl else "wbud"
        return q(f"""
          SELECT kampania, kanal, okres, pacjent,
                 count(*) FILTER (WHERE {wb}) n_wb, coalesce(sum(k5) FILTER (WHERE {wb}), 0) k5_wb,
                 count(*) FILTER (WHERE NOT wbud AND {warunek_zw}) n_zw,
                 coalesce(sum(k5) FILTER (WHERE NOT wbud AND {warunek_zw}), 0) k5_zw
          FROM sl WHERE typ = 'zwykla' GROUP BY ALL""")

    def zbiorczo(s):
        s = s[s.n_wb > 0]
        pomin = int(s[s.n_zw == 0].n_wb.sum())
        s = s[s.n_zw > 0]
        if s.n_wb.sum() == 0:
            return None
        p_wb, p_zw = s.k5_wb / s.n_wb, s.k5_zw / s.n_zw
        w = s.n_wb
        d = float((w * (p_wb - p_zw)).sum() / w.sum())
        var = float((w ** 2 * (p_wb * (1 - p_wb) / s.n_wb + p_zw * (1 - p_zw) / s.n_zw)).sum() / w.sum() ** 2)
        ocz = float((s.n_wb * p_zw).sum())
        return {"sesje_wbud": int(s.n_wb.sum()), "platn_wbud": int(s.k5_wb.sum()), "oczekiwane_platn": ocz,
                "iloraz": s.k5_wb.sum() / ocz if ocz else np.nan, "proc_wbud": 100 * s.k5_wb.sum() / s.n_wb.sum(),
                "proc_oczekiwany": 100 * ocz / s.n_wb.sum(), "roznica_pkt": 100 * d,
                "od": 100 * (d - 1.96 * math.sqrt(var)), "do": 100 * (d + 1.96 * math.sqrt(var)), "pominiete_wbud": pomin}

    grupy = {"poza nowymi kampaniami (razem)": lambda s: ~s.kampania.isin(NOWE),
             "Meta lekarz online (meta_prosp_lekarz_online)": lambda s: s.kampania == "meta_prosp_lekarz_online",
             "remarketing Meta (meta_rmkt_koszyk)": lambda s: s.kampania == "meta_rmkt_koszyk",
             "Google Ads marka (gs_brand)": lambda s: s.kampania == "gs_brand",
             "wejścia bezpośrednie": lambda s: s.kampania == "bezposrednie",
             "Google bezpłatnie (google_organic)": lambda s: s.kampania == "google_organic",
             "newsletter i SMS (crm)": lambda s: s.kanal == "crm",
             "poza nowymi i bez Meta lekarz online": lambda s: ~s.kampania.isin(NOWE + ("meta_prosp_lekarz_online",)),
             "poza nowymi i bez Meta lekarz online, jeszcze nie kupowali":
                 lambda s: ~s.kampania.isin(NOWE + ("meta_prosp_lekarz_online",)) & (s.pacjent == "nie_kupowal"),
             "poza nowymi i bez Meta lekarz online, kupowali wcześniej":
                 lambda s: ~s.kampania.isin(NOWE + ("meta_prosp_lekarz_online",)) & (s.pacjent == "kupowal_wczesniej"),
             "poza nowymi, jeszcze nie kupowali": lambda s: ~s.kampania.isin(NOWE) & (s.pacjent == "nie_kupowal"),
             "nowe: Meta na L4": lambda s: s.kampania == "meta_prosp_l4_szybko",
             "nowe: TikTok na L4": lambda s: s.kampania == "tt_prosp_l4_15min"}
    warianty = {"V1": "TRUE", "V2": f"device IN ('mobile', 'tablet') AND NOT (ios_safari AND dzien >= DATE '{AWARIA}')"}
    zb = []
    for wnazwa, wwar in warianty.items():
        s_all = warstwy(wwar)
        for gnazwa, maska in grupy.items():
            for okres in (1, 2, "oba"):
                s = s_all[maska(s_all)]
                if okres != "oba":
                    s = s[s.okres == okres]
                wynik = zbiorczo(s)
                if wynik:
                    zb.append({"wariant": wnazwa, "grupa": gnazwa, "okres": okres, **wynik})
    ZB = pd.DataFrame(zb)
    ZB["werdykt"] = [werdykt(a, b / 100, c / 100) for a, b, c in zip(ZB.sesje_wbud, ZB["od"], ZB["do"])]
    for wnazwa in warianty:
        r(f"\n   {wnazwa}:")
        pokaz(ZB[ZB.wariant == wnazwa].drop(columns="wariant").round(2))
    kl = {"poza nowymi kampaniami (razem)": "poza_nowymi", "Meta lekarz online (meta_prosp_lekarz_online)": "meta_lekarz_online",
          "poza nowymi i bez Meta lekarz online": "poza_nowymi_bez_meta_lekarz",
          "poza nowymi i bez Meta lekarz online, jeszcze nie kupowali": "poza_nowymi_bez_meta_lekarz_nowi_odwiedzajacy",
          "poza nowymi i bez Meta lekarz online, kupowali wcześniej": "poza_nowymi_bez_meta_lekarz_powracajacy",
          "poza nowymi, jeszcze nie kupowali": "poza_nowymi_nowi_odwiedzajacy", "nowe: Meta na L4": "meta_l4",
          "nowe: TikTok na L4": "tiktok_l4", "Google Ads marka (gs_brand)": "gs_brand", "wejścia bezpośrednie": "bezposrednie",
          "remarketing Meta (meta_rmkt_koszyk)": "meta_remarketing", "Google bezpłatnie (google_organic)": "google_organic",
          "newsletter i SMS (crm)": "crm"}
    for _, w in ZB.iterrows():
        k = f"p1_zbiorczo_{w.wariant.lower()}_{kl[w.grupa]}_okres_{w.okres}"
        j(k + "_sesje_wbudowane", w.sesje_wbud)
        j(k + "_platnosci_wbudowane", w.platn_wbud)
        j(k + "_oczekiwane_platnosci", w.oczekiwane_platn)
        j(k + "_sesja_do_platnosci_wbudowane_proc", w.proc_wbud)
        j(k + "_sesja_do_platnosci_oczekiwana_proc", w.proc_oczekiwany)
        j(k + "_roznica_pkt", w.roznica_pkt)
        j(k + "_roznica_od_pkt", w["od"])
        j(k + "_roznica_do_pkt", w["do"])

    r("\n1f. Według przeglądarki wbudowanej, poza nowymi kampaniami, oba okresy razem (warstwy jak w 1e)")
    pb = []
    for wnazwa, wwar in warianty.items():
        for przegl in WBUD:
            s = warstwy(wwar, przegl)
            for okres in (1, 2):
                wynik = zbiorczo(s[(~s.kampania.isin(NOWE)) & (s.okres == okres)])
                if wynik:
                    pb.append({"wariant": wnazwa, "przegladarka": przegl, "okres": okres, **wynik})
    PB = pd.DataFrame(pb)
    PB["werdykt"] = [werdykt(a, b / 100, c / 100) for a, b, c in zip(PB.sesje_wbud, PB["od"], PB["do"])]
    pokaz(PB.round(2))
    gl = q(f"""SELECT count(*) sesje, count(*) FILTER (WHERE s.user_id IS NOT NULL) z_kontem, count(o.order_id) zamowienia
               FROM czyste.sessions s LEFT JOIN czyste.orders o USING (session_id)
               WHERE s.utm_campaign = 'gs_generic_lekarz_online' AND s.browser IN {WBUD}""").iloc[0]
    r(f"   Uwaga: gs_generic_lekarz_online ma {int(gl.sesje)} sesji w przeglądarkach wbudowanych, z czego {int(gl.z_kontem)} z kontem")
    r(f"   pacjenta i {int(gl.zamowienia)} z zamówieniem (zalogowani pacjenci), stąd 100% w 1b; werdykt „za mała próba”.")

    # ======================= 2. TIKTOK I META PO 180 DNIACH =======================
    naglowek("2. WYNIK NA PACJENTA PO 180 DNIACH: Z JAKICH KOHORT I Z JAKIM KOSZTEM POZYSKANIA (TikTok na L4, Meta na L4)")
    r("   Okna jak w a5e_ekonomia.py: 90 dni = kohorty 1.10.2025–2.07.2026, 180 dni = kohorty 1.10.2025–3.04.2026. Koszt")
    r("   pozyskania w danym oknie = wydatki kampanii z dni kohort okna / nowi pacjenci z tych dni (ZALOZENIA.md 39).")
    g90, g180 = E.granice(90)[2], E.granice(180)[2]
    w2 = []
    przybl = []
    for kamp in NOWE:
        wk = wyd[wyd.kampania == kamp]

        def wydatki(od, do):
            return float(wk[(wk.d >= od) & (wk.d <= do)].wydatki.sum())
        for reg, kol, _ in REGULY:
            p2 = pe[(pe.okres == 2) & (pe[kol] == kamp)]
            c180 = p2[p2.d0 <= g180[1]]
            c90 = p2[p2.d0 <= g90[1]]
            wyd_rok = wydatki(pd.Timestamp(D.OKRES2), pd.Timestamp(D.KONIEC))
            k180, k90, krok = wydatki(*g180) / len(c180), wydatki(*g90) / len(c90), wyd_rok / len(p2)
            se180 = c180.marza_180.std(ddof=1) / math.sqrt(len(c180))
            se90 = c90.marza_90.std(ddof=1) / math.sqrt(len(c90))
            se90w = c180.marza_90.std(ddof=1) / math.sqrt(len(c180))
            przyrost = c180.marza_180 - c180.marza_90
            se_p = przyrost.std(ddof=1) / math.sqrt(len(c180))
            w2 += [
                {"kampania": kamp, "regula": reg, "co": "180 dni: wczesne kohorty", "kohorty_od": c180.d0.min().date(),
                 "kohorty_do": c180.d0.max().date(), "pacjenci": len(c180), "wydatki_zl": wydatki(*g180), "koszt_pozysk": k180,
                 "marza": c180.marza_180.mean(), "wynik": c180.marza_180.mean() - k180,
                 "wynik_od": c180.marza_180.mean() - k180 - 1.96 * se180, "wynik_do": c180.marza_180.mean() - k180 + 1.96 * se180},
                {"kampania": kamp, "regula": reg, "co": "90 dni: te same wczesne kohorty", "kohorty_od": c180.d0.min().date(),
                 "kohorty_do": c180.d0.max().date(), "pacjenci": len(c180), "wydatki_zl": wydatki(*g180), "koszt_pozysk": k180,
                 "marza": c180.marza_90.mean(), "wynik": c180.marza_90.mean() - k180,
                 "wynik_od": c180.marza_90.mean() - k180 - 1.96 * se90w, "wynik_do": c180.marza_90.mean() - k180 + 1.96 * se90w},
                {"kampania": kamp, "regula": reg, "co": "90 dni: wszystkie kohorty z pełnym oknem", "kohorty_od": c90.d0.min().date(),
                 "kohorty_do": c90.d0.max().date(), "pacjenci": len(c90), "wydatki_zl": wydatki(*g90), "koszt_pozysk": k90,
                 "marza": c90.marza_90.mean(), "wynik": c90.marza_90.mean() - k90,
                 "wynik_od": c90.marza_90.mean() - k90 - 1.96 * se90, "wynik_do": c90.marza_90.mean() - k90 + 1.96 * se90},
                {"kampania": kamp, "regula": reg, "co": "cały rocznik okresu 2 (koszt bez marży)", "kohorty_od": p2.d0.min().date(),
                 "kohorty_do": p2.d0.max().date(), "pacjenci": len(p2), "wydatki_zl": wyd_rok, "koszt_pozysk": krok,
                 "marza": np.nan, "wynik": np.nan, "wynik_od": np.nan, "wynik_do": np.nan}]
            m180_przybl = c90.marza_90.mean() + przyrost.mean()
            se_pr = math.sqrt(se90 ** 2 + se_p ** 2)
            przybl.append({"kampania": kamp, "regula": reg, "marza90_wszystkie": c90.marza_90.mean(), "pacjenci_90": len(c90),
                           "przyrost_90_180_wczesne": przyrost.mean(), "pacjenci_180": len(c180),
                           "marza180_przyblizona": m180_przybl, "koszt_rocznika": krok,
                           "wynik180_rocznik": m180_przybl - krok, "od": m180_przybl - krok - 1.96 * se_pr,
                           "do": m180_przybl - krok + 1.96 * se_pr, "koszt_kohort_90": k90,
                           "wynik180_przy_koszcie_kohort_90": m180_przybl - k90})
            sk = f"p2_{SKROT[kamp]}_{reg.lower()}"
            j(sk + "_180_pacjenci", len(c180))
            j(sk + "_180_wydatki_zl", wydatki(*g180))
            j(sk + "_180_koszt_pozyskania_zl", k180)
            j(sk + "_180_marza_na_pacjenta_zl", c180.marza_180.mean())
            j(sk + "_180_wynik_na_pacjenta_zl", c180.marza_180.mean() - k180)
            j(sk + "_180_wynik_od_zl", c180.marza_180.mean() - k180 - 1.96 * se180)
            j(sk + "_180_wynik_do_zl", c180.marza_180.mean() - k180 + 1.96 * se180)
            j(sk + "_90_wczesne_kohorty_marza_zl", c180.marza_90.mean())
            j(sk + "_90_wszystkie_kohorty_pacjenci", len(c90))
            j(sk + "_90_wszystkie_kohorty_koszt_pozyskania_zl", k90)
            j(sk + "_90_wszystkie_kohorty_marza_zl", c90.marza_90.mean())
            j(sk + "_90_wszystkie_kohorty_wynik_zl", c90.marza_90.mean() - k90)
            j(sk + "_rocznik_pacjenci", len(p2))
            j(sk + "_rocznik_koszt_pozyskania_zl", krok)
            j(sk + "_przyrost_marzy_90_180_wczesne_zl", przyrost.mean())
            j(sk + "_rocznik_wynik_180_przyblizony_zl", m180_przybl - krok)
            j(sk + "_rocznik_wynik_180_przyblizony_od_zl", m180_przybl - krok - 1.96 * se_pr)
            j(sk + "_rocznik_wynik_180_przyblizony_do_zl", m180_przybl - krok + 1.96 * se_pr)
    pokaz(pd.DataFrame(w2).round(1))
    r("\n2b. Przybliżenie wyniku po 180 dniach dla całego rocznika: marża w 90 dniach wszystkich kohort z pełnym oknem 90 dni")
    r("    + przyrost marży z dni 91–180 zmierzony na wczesnych kohortach − koszt pozyskania całego rocznika okresu 2.")
    r("    Założenie: późniejsze kohorty dorabiają w dniach 91–180 tyle samo co wczesne. Przedział z sumy wariancji obu")
    r("    składników (bez kowariancji; wczesne kohorty są częścią kohort 90-dniowych), przy stałym koszcie pozyskania.")
    pokaz(pd.DataFrame(przybl).round(2))

    r("\n2c. Kohorty miesięczne (Z1K): nowi pacjenci, wydatki z tego miesiąca, koszt pozyskania, marża w 90 i 180 dniach")
    r("    (tylko kohorty z pełnym oknem; miesiąc częściowo w oknie = średnia z dni w oknie).")
    mies = []
    for kamp in NOWE:
        p2 = pe[(pe.okres == 2) & (pe.kampania == kamp)].assign(m=lambda x: x.d0.dt.to_period("M"))
        wk = wyd[(wyd.kampania == kamp)].assign(m=lambda x: x.d.dt.to_period("M")).groupby("m").wydatki.sum()
        for m, g in p2.groupby("m"):
            g90_ = g[g.d0 <= g90[1]]
            g180_ = g[g.d0 <= g180[1]]
            mies.append({"kampania": kamp, "miesiac": str(m), "nowi": len(g), "wydatki_zl": round(float(wk.get(m, 0.0))),
                         "koszt_pozysk": float(wk.get(m, 0.0)) / len(g),
                         "pacjenci_90": len(g90_), "marza_90": g90_.marza_90.mean() if len(g90_) else np.nan,
                         "pacjenci_180": len(g180_), "marza_180": g180_.marza_180.mean() if len(g180_) else np.nan,
                         "powrot90_proc": 100 * (g90_.dni_R2.fillna(10 ** 6) <= 90).mean() if len(g90_) else np.nan})
    pokaz(pd.DataFrame(mies).round(1))

    # ======================= 3. TEMPO OSTATNIEGO PÓŁROCZA =======================
    naglowek("3. TEMPO WYDATKÓW I POZYSKANIA W OSTATNIM PÓŁROCZU (1.04–30.09.2026) A KWOTY „NA PEŁNY ROK” (c_priorytety.txt, P11)")
    r("   P11: kwota z dni działania kampanii w okresie 2 × 365 / dni działania (dni z wydatkami). Kwota z dni działania =")
    r("   nowi pacjenci okresu 2 × marża na pacjenta (90 albo 180 dni, kohorty z pełnym oknem) − wydatki okresu 2")
    r("   (a5e_scenariusze.txt, E0). W tempie półrocza: ten sam wzór na nowych pacjentach i wydatkach z 1.04–30.09.2026,")
    r("   × 365 / dni z wydatkami w półroczu, przy tej samej marży na pacjenta.")
    w90_ = pe[(pe.okres == 2) & (pe.d0 >= g90[0]) & (pe.d0 <= g90[1])]
    w180_ = pe[(pe.okres == 2) & (pe.d0 >= g180[0]) & (pe.d0 <= g180[1])]
    kontrola_e0 = {("meta_prosp_l4_szybko", "Z1K"): (27845, 29882), ("meta_prosp_l4_szybko", "Z2"): (-28735, -27474),
                   ("tt_prosp_l4_15min", "Z1K"): (-11928, -13468), ("tt_prosp_l4_15min", "Z2"): (-30801, -32341)}
    tempo, kwoty = [], []
    for kamp in NOWE:
        wk = wyd[(wyd.kampania == kamp) & (wyd.d >= pd.Timestamp(D.OKRES2))]
        wh = wk[wk.d >= pd.Timestamp(POLROCZE[0])]
        dni_c, dni_h = wk.d.nunique(), wh.d.nunique()
        for reg, kol, _ in REGULY:
            p2 = pe[(pe.okres == 2) & (pe[kol] == kamp)]
            n_c, n_h = len(p2), int((p2.d0 >= pd.Timestamp(POLROCZE[0])).sum())
            m90 = w90_[w90_[kol] == kamp].marza_90.mean()
            m180 = w180_[w180_[kol] == kamp].marza_180.mean()
            mh = p2[(p2.d0 >= pd.Timestamp(POLROCZE[0])) & (p2.d0 <= g90[1])].marza_90.mean()
            wy_c, wy_h = wk.wydatki.sum(), wh.wydatki.sum()
            e0 = (round(n_c * m90 - wy_c), round(n_c * m180 - wy_c))
            if e0 != kontrola_e0[(kamp, reg)]:
                raise SystemExit(f"Kontrola E0 nie przeszła: {kamp} {reg} {e0} wobec {kontrola_e0[(kamp, reg)]}")
            tempo.append({"kampania": kamp, "regula": reg, "dni_dzialania": dni_c, "dni_polrocza": dni_h,
                          "wydatki_dziennie_caly": wy_c / dni_c, "wydatki_dziennie_polrocze": wy_h / dni_h,
                          "wydatki_iloraz": (wy_h / dni_h) / (wy_c / dni_c),
                          "nowi_dziennie_caly": n_c / dni_c, "nowi_dziennie_polrocze": n_h / dni_h,
                          "nowi_iloraz": (n_h / dni_h) / (n_c / dni_c),
                          "koszt_pozysk_caly": wy_c / n_c, "koszt_pozysk_polrocze": wy_h / n_h})
            f_c, f_h = 365 / dni_c, 365 / dni_h
            pozycje = {"wynik_dzis_90": (n_c * m90 - wy_c, n_h * m90 - wy_h),
                       "wynik_dzis_180": (n_c * m180 - wy_c, n_h * m180 - wy_h),
                       "wylacz_50proc_90": (wy_c - 0.5 * n_c * m90, wy_h - 0.5 * n_h * m90),
                       "wylacz_0proc_wydatki": (wy_c, wy_h),
                       "marza_rocznika_90": (n_c * m90, n_h * m90)}
            for poz, (a, b) in pozycje.items():
                kwoty.append({"kampania": kamp, "regula": reg, "pozycja": poz, "dni_dzialania": a,
                              "pelny_rok_P11": a * f_c, "pelny_rok_tempo_polrocza": b * f_h,
                              "zmiana_proc": 100 * (b * f_h / (a * f_c) - 1) if a else np.nan})
            kwoty.append({"kampania": kamp, "regula": reg, "pozycja": "wynik_dzis_90_marza_kohort_polrocza",
                          "dni_dzialania": np.nan, "pelny_rok_P11": (n_c * m90 - wy_c) * f_c,
                          "pelny_rok_tempo_polrocza": (n_h * mh - wy_h) * f_h,
                          "zmiana_proc": 100 * ((n_h * mh - wy_h) * f_h / ((n_c * m90 - wy_c) * f_c) - 1)})
            if kamp == "meta_prosp_l4_szybko":
                kwoty.append({"kampania": kamp, "regula": reg, "pozycja": "prog_decyzji_90_proc",
                              "dni_dzialania": np.nan, "pelny_rok_P11": 100 * wy_c / (n_c * m90),
                              "pelny_rok_tempo_polrocza": 100 * wy_h / (n_h * m90), "zmiana_proc": np.nan})
            sk = f"p3_{SKROT[kamp]}_{reg.lower()}"
            j(sk + "_dni_dzialania", dni_c)
            j(sk + "_dni_polrocza", dni_h)
            j(sk + "_wydatki_dziennie_caly_zl", wy_c / dni_c)
            j(sk + "_wydatki_dziennie_polrocze_zl", wy_h / dni_h)
            j(sk + "_nowi_dziennie_caly", n_c / dni_c)
            j(sk + "_nowi_dziennie_polrocze", n_h / dni_h)
            j(sk + "_nowi_caly", n_c)
            j(sk + "_nowi_polrocze", n_h)
            j(sk + "_koszt_pozyskania_caly_zl", wy_c / n_c)
            j(sk + "_koszt_pozyskania_polrocze_zl", wy_h / n_h)
    T = pd.DataFrame(tempo)
    pokaz(T.round(3))
    K = pd.DataFrame(kwoty)
    r("\n3b. Kwoty: z dni działania, na pełny rok według P11 i na pełny rok w tempie półrocza (zł); zmiana_proc = różnica")
    r("    tempa półrocza wobec P11. Wiersz _marza_kohort_polrocza: marża w 90 dniach kohort 1.04–2.07.2026 zamiast średniej")
    r("    okresu 2 (sprawdzenie wrażliwości). prog_decyzji = udział pacjentów dodatkowych, przy którym wyłączenie przestaje")
    r("    się opłacać (wydatki / marża rocznika), w procentach.")
    pokaz(K.round(1))
    for _, w in K.iterrows():
        sk = f"p3_{SKROT[w.kampania]}_{w.regula.lower()}_{w.pozycja}"
        j(sk + "_pelny_rok_p11", w.pelny_rok_P11)
        j(sk + "_pelny_rok_tempo_polrocza", w.pelny_rok_tempo_polrocza)
        j(sk + "_zmiana_proc", w.zmiana_proc)

    # ======================= 4. KOSZT KLIKNIĘCIA W GOOGLE ADS =======================
    naglowek("4. KOSZT KLIKNIĘCIA W GOOGLE ADS (wydatki / kliknięcia) I KOSZT NA PIERWSZE ZAMÓWIENIE")
    gads = q("""SELECT date d, utm_campaign kampania, spend_pln::DOUBLE wydatki, clicks klikniecia, impressions wyswietlenia
                FROM czyste.marketing_spend WHERE utm_campaign LIKE 'gs_%'""")
    gads["d"] = pd.to_datetime(gads.d)
    gads["okres"] = np.where(gads.d < pd.Timestamp(D.OKRES2), 1, 2)
    gads["miesiac"] = gads.d.dt.to_period("M").astype(str)
    gads["kwartal"] = gads.d.dt.to_period("Q").astype(str)
    r("4a. Okres 1 wobec okresu 2: kliknięcia, wydatki, koszt kliknięcia (zł), współczynnik klikalności (kliknięcia / wyświetlenia, %)")
    a = gads.groupby(["kampania", "okres"]).agg(klikniecia=("klikniecia", "sum"), wydatki=("wydatki", "sum"),
                                                wyswietlenia=("wyswietlenia", "sum")).reset_index()
    razem = gads.assign(kampania="google_ads_razem").groupby(["kampania", "okres"]).agg(
        klikniecia=("klikniecia", "sum"), wydatki=("wydatki", "sum"), wyswietlenia=("wyswietlenia", "sum")).reset_index()
    gen = gads[gads.kampania.str.startswith("gs_generic")].assign(kampania="gs_generic_razem").groupby(["kampania", "okres"]).agg(
        klikniecia=("klikniecia", "sum"), wydatki=("wydatki", "sum"), wyswietlenia=("wyswietlenia", "sum")).reset_index()
    a = pd.concat([a, gen, razem], ignore_index=True)
    a["koszt_klikniecia"] = a.wydatki / a.klikniecia
    a["ctr_proc"] = 100 * a.klikniecia / a.wyswietlenia
    sz = a.pivot(index="kampania", columns="okres", values=["klikniecia", "wydatki", "koszt_klikniecia", "ctr_proc"])
    sz.columns = [f"{x}_o{y}" for x, y in sz.columns]
    sz["koszt_klikniecia_zmiana_proc"] = 100 * (sz.koszt_klikniecia_o2 / sz.koszt_klikniecia_o1 - 1)
    sz = sz.reset_index()
    pokaz(sz.round(3))
    for _, w in sz.iterrows():
        sk = f"p4_{w.kampania}"
        j(sk + "_koszt_klikniecia_okres1_zl", w.koszt_klikniecia_o1)
        j(sk + "_koszt_klikniecia_okres2_zl", w.koszt_klikniecia_o2)
        j(sk + "_klikniecia_okres1", int(w.klikniecia_o1))
        j(sk + "_klikniecia_okres2", int(w.klikniecia_o2))
        j(sk + "_koszt_klikniecia_zmiana_proc", w.koszt_klikniecia_zmiana_proc)

    r("\n4b. Koszt kliknięcia miesięcznie (zł), z kliknięciami gs_brand obok")
    m = gads.groupby(["miesiac", "kampania"]).agg(w=("wydatki", "sum"), k=("klikniecia", "sum")).reset_index()
    m["cpc"] = m.w / m.k
    mp = m.pivot(index="miesiac", columns="kampania", values="cpc").round(3)
    mp["klikniecia_gs_brand"] = m[m.kampania == "gs_brand"].set_index("miesiac").k
    mr = gads.groupby("miesiac").agg(w=("wydatki", "sum"), k=("klikniecia", "sum"))
    mp["google_ads_razem"] = (mr.w / mr.k).round(3)
    pokaz(mp.reset_index())

    r("\n4c. Koszt kliknięcia w kwartałach i rok do roku (zł)")
    kq = gads.groupby(["kwartal", "kampania"]).agg(w=("wydatki", "sum"), k=("klikniecia", "sum")).reset_index()
    kq["cpc"] = kq.w / kq.k
    kp = kq.pivot(index="kwartal", columns="kampania", values="cpc")
    kp_rr = (100 * (kp / kp.shift(4) - 1)).round(1)
    kp_rr.columns = [f"{c}_rr_proc" for c in kp_rr.columns]
    pokaz(pd.concat([kp.round(3), kp_rr[["gs_brand_rr_proc"]]], axis=1).reset_index())

    r("\n4d. Koszt na pierwsze zamówienie (nowego pacjenta) w kampaniach Google Ads: wydatki / nowi pacjenci tych samych dni,")
    r("    obie reguły źródła, w okresach i kwartałach (dzień pacjenta = dzień pierwszej płatności)")
    pe_q = pe.assign(kwartal=pe.d0.dt.to_period("Q").astype(str))
    wiersze = []
    for kamp in sorted(gads.kampania.unique()):
        for okres in (1, 2):
            wy_ = gads[(gads.kampania == kamp) & (gads.okres == okres)].wydatki.sum()
            n1 = int(((pe.okres == okres) & (pe.kampania == kamp)).sum())
            n2 = int(((pe.okres == okres) & (pe.kampania_z2 == kamp)).sum())
            wiersze.append({"kampania": kamp, "okres": okres, "wydatki": wy_, "nowi_Z1K": n1, "koszt_Z1K": wy_ / n1,
                            "nowi_Z2": n2, "koszt_Z2": wy_ / n2})
            j(f"p4_{kamp}_okres{okres}_koszt_na_pierwsze_zamowienie_z1k_zl", wy_ / n1)
            j(f"p4_{kamp}_okres{okres}_nowi_z1k", n1)
            j(f"p4_{kamp}_okres{okres}_koszt_na_pierwsze_zamowienie_z2_zl", wy_ / n2)
            j(f"p4_{kamp}_okres{okres}_nowi_z2", n2)
    pokaz(pd.DataFrame(wiersze).round(2))
    r("\n    gs_brand w kwartałach:")
    wiersze = []
    for kw, g in gads[gads.kampania == "gs_brand"].groupby("kwartal"):
        n1 = int(((pe_q.kwartal == kw) & (pe_q.kampania == "gs_brand")).sum())
        n2 = int(((pe_q.kwartal == kw) & (pe_q.kampania_z2 == "gs_brand")).sum())
        wiersze.append({"kwartal": kw, "wydatki": g.wydatki.sum(), "klikniecia": g.klikniecia.sum(),
                        "koszt_klikniecia": g.wydatki.sum() / g.klikniecia.sum(), "nowi_Z1K": n1,
                        "koszt_Z1K": g.wydatki.sum() / n1, "nowi_Z2": n2, "koszt_Z2": g.wydatki.sum() / n2})
    pokaz(pd.DataFrame(wiersze).round(2))

    # ======================= 5. GS_BRAND OD 22.05.2026 =======================
    naglowek("5. GOOGLE ADS NA MARKĘ (gs_brand): SPADEK KONWERSJI SESJA DO PŁATNOŚCI OD 22.05.2026")
    r("   Sesje zwykłe osób, które jeszcze nie kupowały (jak w a5p_zdarzenia.py), kampania gs_brand. Okna (dzień sesji):")
    okna5 = {"A_przed_caly": ("2024-10-01", "2026-05-21"), "B_po_awarii_safari": ("2026-03-17", "2026-05-21"),
             "C_okres2_przed_awaria": ("2025-10-01", "2026-03-16"), "D_po_spadku": ("2026-05-22", "2026-09-30"),
             "A0_rok_wczesniej_przed": ("2024-10-01", "2025-05-21"), "B0_rok_wczesniej_17_03_21_05": ("2025-03-17", "2025-05-21"),
             "D0_rok_wczesniej_22_05_30_09": ("2025-05-22", "2025-09-30")}
    for k, (od, do) in okna5.items():
        r(f"     {k}: {od} – {do}")
    r("   A = odcinek przed zmianą w wykrywaniu (a5p_zdarzenia.csv: 598 dni), D = odcinek po (132 dni).")

    def okno_sql(nazwa):
        od, do = okna5[nazwa]
        return f"dzien BETWEEN DATE '{od}' AND DATE '{do}'"

    def lejek_okna(warunek):
        czesci = []
        for nazwa in okna5:
            czesci.append(f"""
              SELECT '{nazwa}' okno, count(DISTINCT dzien) dni, count(*) sesje, sum(k1) k1, sum(k2) k2, sum(k3) k3,
                     sum(k4) k4, sum(k5) k5
              FROM sl WHERE typ = 'zwykla' AND kampania = 'gs_brand' AND {okno_sql(nazwa)} AND {warunek}""")
        t = q(" UNION ALL ".join(czesci))
        t["sesje_dziennie"] = t.sesje / t.dni
        for nazwa, licz, mian in (("usluga", "k1", "sesje"), ("termin", "k2", "k1"), ("logowanie", "k3", "k2"),
                                  ("wejscie_platn", "k4", "k3"), ("platnosc", "k5", "k4"), ("sesja_do_platn", "k5", "sesje")):
            t[nazwa] = 100 * t[licz] / t[mian].where(t[mian] > 0)
        return t

    L = lejek_okna("pacjent = 'nie_kupowal'")
    r("\n5a. Lejek w oknach (konwersje w %)")
    pokaz(L.round(2))
    Li = L.set_index("okno")
    for okno in okna5:
        j(f"p5_gs_brand_{okno}_sesja_do_platnosci_proc", Li.at[okno, "sesja_do_platn"])
        j(f"p5_gs_brand_{okno}_sesje", int(Li.at[okno, "sesje"]))
        j(f"p5_gs_brand_{okno}_platnosci", int(Li.at[okno, "k5"]))

    r("\n5b. Różnice sesji do płatności (punkty procentowe, 95%) i różnica różnic wobec tych samych dat rok wcześniej")
    rows = []
    for a_, b_ in (("D_po_spadku", "A_przed_caly"), ("D_po_spadku", "B_po_awarii_safari"), ("D_po_spadku", "C_okres2_przed_awaria"),
                   ("B_po_awarii_safari", "C_okres2_przed_awaria"),
                   ("D0_rok_wczesniej_22_05_30_09", "A0_rok_wczesniej_przed"),
                   ("D0_rok_wczesniej_22_05_30_09", "B0_rok_wczesniej_17_03_21_05")):
        d, lo, hi = newcombe(Li.at[a_, "k5"], Li.at[a_, "sesje"], Li.at[b_, "k5"], Li.at[b_, "sesje"])
        rows.append({"porownanie": f"{a_} − {b_}", "roznica_pkt": 100 * d, "od": 100 * lo, "do": 100 * hi})
    for (a_, b_), (a0, b0) in ((("D_po_spadku", "B_po_awarii_safari"), ("D0_rok_wczesniej_22_05_30_09", "B0_rok_wczesniej_17_03_21_05")),
                               (("D_po_spadku", "A_przed_caly"), ("D0_rok_wczesniej_22_05_30_09", "A0_rok_wczesniej_przed"))):
        p = {x: Li.at[x, "k5"] / Li.at[x, "sesje"] for x in (a_, b_, a0, b0)}
        v = sum(p[x] * (1 - p[x]) / Li.at[x, "sesje"] for x in p)
        dd = (p[a_] - p[b_]) - (p[a0] - p[b0])
        rows.append({"porownanie": f"różnica różnic ({a_} − {b_}) − ({a0} − {b0})", "roznica_pkt": 100 * dd,
                     "od": 100 * (dd - 1.96 * math.sqrt(v)), "do": 100 * (dd + 1.96 * math.sqrt(v))})
    R5 = pd.DataFrame(rows)
    pokaz(R5.round(2))
    nazwy_por = ["D_minus_A", "D_minus_B", "D_minus_C", "B_minus_C", "D0_minus_A0", "D0_minus_B0",
                 "roznica_roznic_D_minus_B_wobec_roku_wczesniej", "roznica_roznic_D_minus_A_wobec_roku_wczesniej"]
    for i, w in R5.iterrows():
        j(f"p5_gs_brand_{nazwy_por[i]}_sesja_do_platnosci_pkt", w.roznica_pkt)
        j(f"p5_gs_brand_{nazwy_por[i]}_od_pkt", w["od"])
        j(f"p5_gs_brand_{nazwy_por[i]}_do_pkt", w["do"])
    utr = (Li.at["D_po_spadku", "sesja_do_platn"] - Li.at["A_przed_caly", "sesja_do_platn"]) / 100 * Li.at["D_po_spadku", "sesje"]
    utr_b = (Li.at["D_po_spadku", "sesja_do_platn"] - Li.at["B_po_awarii_safari", "sesja_do_platn"]) / 100 * Li.at["D_po_spadku", "sesje"]
    dni_d = int(Li.at["D_po_spadku", "dni"])
    r(f"   Zamówienia w oknie D wobec poziomu A: {utr:.1f} (na 30 dni {utr / dni_d * 30:.1f}); wobec poziomu B: {utr_b:.1f} "
      f"(na 30 dni {utr_b / dni_d * 30:.1f}). Okno D ma {dni_d} dni.")
    j("p5_gs_brand_zamowienia_roznica_wobec_A_na_30_dni", utr / dni_d * 30)
    j("p5_gs_brand_zamowienia_roznica_wobec_B_na_30_dni", utr_b / dni_d * 30)

    r("\n5c. Podgrupy: sesja do płatności (%) w oknach B, A i D, różnica D − B (95%). Bez Safari na iOS = cały okres bez tej")
    r("    przeglądarki. Ostatnie wiersze: pacjenci, którzy już kupowali (powracający), dla porównania.")
    podgr = {"wszyscy (nowi)": "pacjent = 'nie_kupowal'",
             "bez Safari na iOS": "pacjent = 'nie_kupowal' AND NOT ios_safari",
             "tylko Safari na iOS": "pacjent = 'nie_kupowal' AND ios_safari",
             "urządzenie mobile": "pacjent = 'nie_kupowal' AND device = 'mobile'",
             "urządzenie desktop": "pacjent = 'nie_kupowal' AND device = 'desktop'",
             "urządzenie tablet": "pacjent = 'nie_kupowal' AND device = 'tablet'",
             "przeglądarki wbudowane": "pacjent = 'nie_kupowal' AND wbud",
             "zwykłe bez Safari na iOS": "pacjent = 'nie_kupowal' AND NOT wbud AND NOT ios_safari",
             "powracający (kupowali wcześniej)": "pacjent = 'kupowal_wczesniej'",
             "powracający bez Safari na iOS": "pacjent = 'kupowal_wczesniej' AND NOT ios_safari"}
    for lp in q("SELECT landing_page, count(*) n FROM sl WHERE kampania = 'gs_brand' AND typ = 'zwykla' GROUP BY 1 ORDER BY 2 DESC").landing_page:
        podgr[f"strona wejścia {lp}"] = f"pacjent = 'nie_kupowal' AND landing_page = '{lp}'"
    rows = []
    for nazwa, war in podgr.items():
        t = lejek_okna(war).set_index("okno")
        d, lo, hi = newcombe(t.at["D_po_spadku", "k5"], t.at["D_po_spadku", "sesje"], t.at["B_po_awarii_safari", "k5"],
                             t.at["B_po_awarii_safari", "sesje"])
        d0, lo0, hi0 = newcombe(t.at["D0_rok_wczesniej_22_05_30_09", "k5"], t.at["D0_rok_wczesniej_22_05_30_09", "sesje"],
                                t.at["B0_rok_wczesniej_17_03_21_05", "k5"], t.at["B0_rok_wczesniej_17_03_21_05", "sesje"])
        rows.append({"podgrupa": nazwa, "sesje_B": int(t.at["B_po_awarii_safari", "sesje"]), "proc_B": t.at["B_po_awarii_safari", "sesja_do_platn"],
                     "sesje_A": int(t.at["A_przed_caly", "sesje"]), "proc_A": t.at["A_przed_caly", "sesja_do_platn"],
                     "sesje_D": int(t.at["D_po_spadku", "sesje"]), "proc_D": t.at["D_po_spadku", "sesja_do_platn"],
                     "D_minus_B": 100 * d, "od": 100 * lo, "do": 100 * hi,
                     "rok_wczesniej_D0_minus_B0": 100 * d0, "od0": 100 * lo0, "do0": 100 * hi0})
    P5 = pd.DataFrame(rows)
    pokaz(P5.round(2))
    kl5 = {"wszyscy (nowi)": "nowi", "bez Safari na iOS": "bez_safari_ios", "tylko Safari na iOS": "safari_ios",
           "urządzenie mobile": "mobile", "urządzenie desktop": "desktop", "przeglądarki wbudowane": "wbudowane",
           "powracający (kupowali wcześniej)": "powracajacy"}
    for _, w in P5.iterrows():
        if w.podgrupa in kl5:
            sk = f"p5_gs_brand_{kl5[w.podgrupa]}"
            j(sk + "_okno_B_proc", w.proc_B)
            j(sk + "_okno_B_sesje", w.sesje_B)
            j(sk + "_okno_D_proc", w.proc_D)
            j(sk + "_okno_D_sesje", w.sesje_D)
            j(sk + "_D_minus_B_pkt", w.D_minus_B)
            j(sk + "_D_minus_B_od_pkt", w["od"])
            j(sk + "_D_minus_B_do_pkt", w["do"])

    r("\n5d. Rozkład zmiany sesji do płatności (D wobec A i D wobec B, punkty procentowe) na strukturę i konwersję w grupach")
    r("    (jak a5p_lejek.py, sekcja 4); osoby, które jeszcze nie kupowały")
    rows = []
    for podzial, wyr in (("urzadzenie", "device"), ("system_przegladarka", "os || ' ' || browser"), ("strona_wejscia", "landing_page"),
                         ("wbudowana", "wbud::VARCHAR")):
        for przed in ("A_przed_caly", "B_po_awarii_safari"):
            t = q(f"""SELECT {wyr} g, CASE WHEN {okno_sql('D_po_spadku')} THEN 2 ELSE 1 END o, count(*) n, sum(k5) k5
                      FROM sl WHERE typ = 'zwykla' AND kampania = 'gs_brand' AND pacjent = 'nie_kupowal'
                        AND ({okno_sql('D_po_spadku')} OR {okno_sql(przed)}) GROUP BY 1, 2""")
            w = t.pivot(index="g", columns="o", values=["n", "k5"]).fillna(0)
            u1, u2 = w[("n", 1)] / w[("n", 1)].sum(), w[("n", 2)] / w[("n", 2)].sum()
            c2 = (w[("k5", 2)] / w[("n", 2)]).where(w[("n", 2)] > 0, 0)
            c1 = (w[("k5", 1)] / w[("n", 1)]).where(w[("n", 1)] > 0, c2)
            calk = w[("k5", 2)].sum() / w[("n", 2)].sum() - w[("k5", 1)].sum() / w[("n", 1)].sum()
            rows.append({"podzial": podzial, "przed": przed, "zmiana_pkt": 100 * calk, "efekt_struktury_pkt": 100 * ((u2 - u1) * c1).sum(),
                         "efekt_konwersji_pkt": 100 * (u2 * (c2 - c1)).sum()})
    pokaz(pd.DataFrame(rows).round(2))

    r("\n5e. Tydzień po tygodniu (poniedziałki) od 2.03 do 28.09: sesja do płatności gs_brand w 2026 i w tych samych tygodniach 2025")
    r("    (osoby, które jeszcze nie kupowały; tydzień 2025 = ten sam tydzień przesunięty o 52 tygodnie)")
    tyg = q("""
      SELECT date_trunc('week', dzien)::DATE tydzien, count(*) sesje, sum(k5) k5,
             count(*) FILTER (WHERE NOT ios_safari) sesje_bez_safari_ios, sum(k5) FILTER (WHERE NOT ios_safari) k5_bez_safari_ios
      FROM sl WHERE typ = 'zwykla' AND kampania = 'gs_brand' AND pacjent = 'nie_kupowal' GROUP BY 1""")
    tyg["tydzien"] = pd.to_datetime(tyg.tydzien)
    t26 = tyg[(tyg.tydzien >= "2026-03-02") & (tyg.tydzien <= "2026-09-28")].copy()
    t25 = tyg.assign(tydzien=tyg.tydzien + pd.Timedelta(weeks=52))
    t26 = t26.merge(t25, on="tydzien", how="left", suffixes=("", "_2025"))
    t26["proc_2026"] = 100 * t26.k5 / t26.sesje
    t26["proc_2026_bez_safari_ios"] = 100 * t26.k5_bez_safari_ios / t26.sesje_bez_safari_ios
    t26["proc_2025"] = 100 * t26.k5_2025 / t26.sesje_2025
    t26["tydzien"] = t26.tydzien.dt.date
    pokaz(t26[["tydzien", "sesje", "k5", "proc_2026", "proc_2026_bez_safari_ios", "sesje_2025", "k5_2025", "proc_2025"]].round(1))

    r("\n5f. Lejek gs_brand bez Safari na iOS w oknach (konwersje kroków w %, osoby, które jeszcze nie kupowały)")
    Lb = lejek_okna("pacjent = 'nie_kupowal' AND NOT ios_safari")
    pokaz(Lb[["okno", "sesje", "k5", "usluga", "termin", "logowanie", "wejscie_platn", "platnosc", "sesja_do_platn"]].round(2))
    Lbi = Lb.set_index("okno")
    for krok in ("usluga", "logowanie", "sesja_do_platn"):
        j(f"p5_gs_brand_bez_safari_ios_okno_B_{krok}_proc", Lbi.at["B_po_awarii_safari", krok])
        j(f"p5_gs_brand_bez_safari_ios_okno_D_{krok}_proc", Lbi.at["D_po_spadku", krok])
    j("p5_gs_brand_bez_safari_ios_okno_D_k2_sesje_z_terminem", int(Lbi.at["D_po_spadku", "k2"]))
    j("p5_gs_brand_bez_safari_ios_okno_B_k2_sesje_z_terminem", int(Lbi.at["B_po_awarii_safari", "k2"]))

    r("\n5g. Czy spadek jest tylko w gs_brand: kanały w oknach B i D (bez Safari na iOS, osoby, które jeszcze nie kupowały),")
    r("    sesja do płatności i krok konta (k3 / k2) w %, różnica D − B (95%) i ta sama różnica rok wcześniej (D0 − B0)")
    rows = []
    ch = q(f"""SELECT kanal, {', '.join(f"count(*) FILTER (WHERE {okno_sql(o)}) n_{o[:2]}, sum(k5) FILTER (WHERE {okno_sql(o)}) k5_{o[:2]}, "
                                         f"sum(k2) FILTER (WHERE {okno_sql(o)}) k2_{o[:2]}, sum(k3) FILTER (WHERE {okno_sql(o)}) k3_{o[:2]}"
                                         for o in ('B_po_awarii_safari', 'D_po_spadku', 'B0_rok_wczesniej_17_03_21_05', 'D0_rok_wczesniej_22_05_30_09'))}
               FROM sl WHERE typ = 'zwykla' AND pacjent = 'nie_kupowal' AND NOT ios_safari GROUP BY 1 ORDER BY 1""").fillna(0)
    for _, w in ch.iterrows():
        if w.n_B_ < 300:
            continue
        d, lo, hi = newcombe(w.k5_D_, w.n_D_, w.k5_B_, w.n_B_)
        d0 = (w.k5_D0 / w.n_D0 - w.k5_B0 / w.n_B0) if w.n_B0 and w.n_D0 else np.nan
        dk, lok, hik = newcombe(w.k3_D_, w.k2_D_, w.k3_B_, w.k2_B_)
        rows.append({"kanal": w.kanal, "sesje_B": int(w.n_B_), "proc_B": 100 * w.k5_B_ / w.n_B_, "sesje_D": int(w.n_D_),
                     "proc_D": 100 * w.k5_D_ / w.n_D_, "D_minus_B": 100 * d, "od": 100 * lo, "do": 100 * hi,
                     "rok_wczesniej_D0_minus_B0": 100 * d0,
                     "konto_B": 100 * w.k3_B_ / w.k2_B_, "konto_D": 100 * w.k3_D_ / w.k2_D_, "konto_D_minus_B": 100 * dk,
                     "konto_od": 100 * lok, "konto_do": 100 * hik})
    CH = pd.DataFrame(rows)
    pokaz(CH.round(2))
    for _, w in CH.iterrows():
        j(f"p5_kanal_{w.kanal}_bez_safari_ios_D_minus_B_pkt", w.D_minus_B)
        j(f"p5_kanal_{w.kanal}_bez_safari_ios_sesje_D", w.sesje_D)
        j(f"p5_kanal_{w.kanal}_bez_safari_ios_konto_D_minus_B_pkt", w.konto_D_minus_B)

    r("\n5h. Ruch i koszt w oknach: kliknięcia i wydatki gs_brand, wszystkie sesje gs_brand (wszystkie typy), sesje na kliknięcie")
    rows = []
    for nazwa, (od, do) in okna5.items():
        g = gads[(gads.kampania == "gs_brand") & (gads.d >= od) & (gads.d <= do)]
        s = q(f"SELECT count(*) n, count(*) FILTER (WHERE pacjent = 'nie_kupowal' AND typ = 'zwykla') n_nowi FROM sl "
              f"WHERE kampania = 'gs_brand' AND {okno_sql(nazwa)}").iloc[0]
        rows.append({"okno": nazwa, "klikniecia": int(g.klikniecia.sum()), "koszt_klikniecia": g.wydatki.sum() / g.klikniecia.sum(),
                     "sesje_wszystkie": int(s.n), "sesje_na_klik": s.n / g.klikniecia.sum(),
                     "udzial_sesji_nowych_proc": 100 * s.n_nowi / s.n})
    pokaz(pd.DataFrame(rows).round(3))

    # ======================= 6. KOD RABATOWY =======================
    naglowek("6. KOD RABATOWY NA PIERWSZYM ZAMÓWIENIU PACJENTÓW NOWYCH KAMPANII (okres 2)")
    r("   Pierwsze zamówienia nowych pacjentów okresu 2 przypisanych do kampanii daną regułą. Zniżka = cena katalogowa − zapłata")
    r("   (ZALOZENIA.md 14). Zniżka efektywna = tylko wizyty odbyte bez zwrotu i nieodebrane (completed, no_show), bo przy")
    r("   anulowanej i zwróconej wizycie pacjent dostaje całą zapłatę z powrotem (ZALOZENIA.md 47). Powrót w 90 dniach i marża")
    r("   w 90 dniach: kohorty do 2.07.2026. Na pełny rok: × 365 / dni działania kampanii (P11). Kody pokazujemy jako nazwę")
    r("   i liczbę użyć.")
    pierwsze = q(f"""SELECT z.user_id, z.discount_type, z.promo_code, z.list_price::DOUBLE cena, z.amount_paid::DOUBLE zaplata,
                            z.status FROM zam z WHERE z.nr = 1 AND z.created_at >= TIMESTAMP '{D.OKRES2}'""")
    f6 = pe[pe.okres == 2].merge(pierwsze, on="user_id")
    f6["promo"] = f6.discount_type == "promo"
    f6["znizka"] = f6.cena - f6.zaplata
    f6["znizka_efekt"] = np.where(f6.status.isin(["completed", "no_show"]), f6.znizka, 0.0)
    f6["zwrot_po_wizycie"] = f6.status == "refunded"
    f6["odbyta"] = f6.status.isin(["completed", "refunded"])
    f6["w90"] = f6.d0 <= pd.Timestamp(g90[1])
    f6["powrot90"] = f6.dni_R2.fillna(10 ** 6) <= 90
    dni_k = {k: int(wyd[(wyd.kampania == k) & (wyd.d >= pd.Timestamp(D.OKRES2))].d.nunique()) for k in NOWE}
    wiersze, kody_t = [], []
    for kamp in NOWE:
        mn = 365 / dni_k[kamp]
        for reg, kol, _ in REGULY:
            g = f6[f6[kol] == kamp]
            for c, nm in g[g.promo].promo_code.value_counts().items():
                kody_t.append({"kampania": kamp, "regula": reg, "kod": c, "uzycia_na_pierwszym_zamowieniu": int(nm),
                               "znizka_zl": g[g.promo_code == c].znizka.mean()})
            for promo in (True, False):
                h = g[g.promo == promo]
                h90 = h[h.w90]
                wiersze.append({"kampania": kamp, "regula": reg, "z_kodem": promo, "pierwsze_zam": len(h),
                                "udzial_proc": 100 * len(h) / len(g), "znizka_srednia": h.znizka.mean(),
                                "znizka_razem": h.znizka.sum(), "znizka_efekt_razem": h.znizka_efekt.sum(),
                                "znizka_efekt_rok": h.znizka_efekt.sum() * mn,
                                "zwrot_po_wizycie_proc": 100 * h.zwrot_po_wizycie.mean(),
                                "zwrot_wsrod_odbytych_proc": 100 * h.zwrot_po_wizycie.sum() / h.odbyta.sum() if h.odbyta.sum() else np.nan,
                                "odbyte": int(h.odbyta.sum()), "pacjenci_90": len(h90),
                                "powrot90_proc": 100 * h90.powrot90.mean() if len(h90) else np.nan,
                                "marza90": h90.marza_90.mean() if len(h90) else np.nan})
    W6 = pd.DataFrame(wiersze)
    r("\n6a. Z kodem rabatowym (discount_type = promo) i bez, obie reguły (kwoty w zł)")
    pokaz(W6.round(2))
    r("\n6b. Kody na pierwszym zamówieniu (nazwa, liczba użyć, średnia zniżka w zł)")
    pokaz(pd.DataFrame(kody_t).round(2))
    r("\n6c. Pozostałe zniżki na pierwszym zamówieniu (discount_type), obie reguły")
    pokaz(pd.concat([f6[f6[kol] == kamp].groupby("discount_type").size().rename("pierwsze_zam").reset_index()
                     .assign(kampania=kamp, regula=reg) for kamp in NOWE for reg, kol, _ in REGULY])[
        ["kampania", "regula", "discount_type", "pierwsze_zam"]])
    for _, w in W6.iterrows():
        sk = f"p6_{SKROT[w.kampania]}_{w.regula.lower()}_{'z_kodem' if w.z_kodem else 'bez_kodu'}"
        j(sk + "_pierwsze_zamowienia", w.pierwsze_zam)
        j(sk + "_udzial_proc", w.udzial_proc)
        j(sk + "_znizka_srednia_zl", w.znizka_srednia)
        j(sk + "_znizka_razem_okres2_zl", w.znizka_razem)
        j(sk + "_znizka_efektywna_okres2_zl", w.znizka_efekt_razem)
        j(sk + "_znizka_efektywna_pelny_rok_zl", w.znizka_efekt_rok)
        j(sk + "_zwrot_po_wizycie_proc", w.zwrot_po_wizycie_proc)
        j(sk + "_zwrot_wsrod_odbytych_proc", w.zwrot_wsrod_odbytych_proc)
        j(sk + "_odbyte_wizyty", w.odbyte)
        j(sk + "_powrot90_proc", w.powrot90_proc)
        j(sk + "_pacjenci_90", w.pacjenci_90)
        j(sk + "_marza90_zl", w.marza90)

    r("\n6d. Wszystkie zamówienia z kodami kampanii w okresie 2 (także kolejne zamówienia, bez względu na regułę źródła)")
    kz = q(f"""SELECT promo_code kod, count(*) zamowienia, count(*) FILTER (WHERE z.nr = 1) pierwsze, count(*) FILTER (WHERE z.nr > 1) kolejne,
                      avg(list_price - amount_paid)::DOUBLE znizka_zl, sum(list_price - amount_paid)::DOUBLE znizka_razem,
                      sum(CASE WHEN status IN ('completed', 'no_show') THEN list_price - amount_paid ELSE 0 END)::DOUBLE znizka_efekt
               FROM zam z WHERE created_at >= TIMESTAMP '{D.OKRES2}' AND promo_code IN ('L4SZYBKO20', 'TIKTOK25') GROUP BY 1 ORDER BY 1""")
    kz["dni_dzialania"] = kz.kod.map({"L4SZYBKO20": dni_k["meta_prosp_l4_szybko"], "TIKTOK25": dni_k["tt_prosp_l4_15min"]})
    kz["znizka_razem_rok"] = kz.znizka_razem * 365 / kz.dni_dzialania
    kz["znizka_efekt_rok"] = kz.znizka_efekt * 365 / kz.dni_dzialania
    kz["zamowienia_rok"] = kz.zamowienia * 365 / kz.dni_dzialania
    pokaz(kz.round(1))
    for _, w in kz.iterrows():
        sk = f"p6_kod_{w.kod.lower()}"
        j(sk + "_zamowienia_okres2", w.zamowienia)
        j(sk + "_zamowienia_kolejne_okres2", w.kolejne)
        j(sk + "_znizka_zl", w.znizka_zl)
        j(sk + "_znizka_razem_okres2_zl", w.znizka_razem)
        j(sk + "_znizka_efektywna_okres2_zl", w.znizka_efekt)
        j(sk + "_znizka_razem_pelny_rok_zl", w.znizka_razem_rok)
        j(sk + "_znizka_efektywna_pelny_rok_zl", w.znizka_efekt_rok)
        j(sk + "_zamowienia_pelny_rok", w.zamowienia_rok)

    r("\n6e. Różnica z kodem − bez kodu (punkty procentowe, 95%): zwrot po wizycie na pierwszym zamówieniu i powrót w 90 dniach.")
    r("    Porównanie obserwacyjne: pacjenci z kodem i bez kodu różnią się nie tylko kodem.")
    rows = []
    for kamp in NOWE:
        for reg, kol, _ in REGULY:
            g = f6[f6[kol] == kamp]
            a_, b_ = g[g.promo], g[~g.promo]
            dz, lz, hz = newcombe(a_.zwrot_po_wizycie.sum(), len(a_), b_.zwrot_po_wizycie.sum(), len(b_))
            a9, b9 = a_[a_.w90], b_[b_.w90]
            dp, lp_, hp = newcombe(a9.powrot90.sum(), len(a9), b9.powrot90.sum(), len(b9))
            rows.append({"kampania": kamp, "regula": reg, "zwrot_roznica_pkt": 100 * dz, "zwrot_od": 100 * lz, "zwrot_do": 100 * hz,
                         "powrot90_roznica_pkt": 100 * dp, "powrot_od": 100 * lp_, "powrot_do": 100 * hp,
                         "pacjenci_90_z_kodem": len(a9), "pacjenci_90_bez_kodu": len(b9)})
            sk = f"p6_{SKROT[kamp]}_{reg.lower()}_z_kodem_minus_bez"
            j(sk + "_zwrot_po_wizycie_pkt", 100 * dz)
            j(sk + "_zwrot_po_wizycie_od_pkt", 100 * lz)
            j(sk + "_zwrot_po_wizycie_do_pkt", 100 * hz)
            j(sk + "_powrot90_pkt", 100 * dp)
            j(sk + "_powrot90_od_pkt", 100 * lp_)
            j(sk + "_powrot90_do_pkt", 100 * hp)
    pokaz(pd.DataFrame(rows).round(2))

    r("\n6f. Scenariusz bez kodu kampanii (L4SZYBKO20 albo TIKTOK25); reakcji konwersji na brak kodu nie znamy. Pacjent, który")
    r("    kupiłby i bez kodu, płaci więcej o zniżkę efektywną; pacjent, który bez kodu by nie kupił, traci dziś przynoszoną marżę")
    r("    w 90 dniach (marza90 z kodem, przed kosztem pozyskania; wydatki na reklamę bez zmian). Dwa warianty: bez żadnej zniżki")
    r("    i z przejściem na stały kod START10 dla nowych pacjentów (10 zł). Próg = udział utraconych pierwszych zamówień z kodem,")
    r("    przy którym rezygnacja z kodu przestaje się opłacać: zniżka / (zniżka + marza90). Na pełny rok × 365 / dni działania.")
    rows = []
    for kamp, kod in (("meta_prosp_l4_szybko", "L4SZYBKO20"), ("tt_prosp_l4_15min", "TIKTOK25")):
        mn = 365 / dni_k[kamp]
        for reg, kol, _ in REGULY:
            g = f6[(f6[kol] == kamp) & (f6.promo_code == kod)]
            m90k = g[g.w90].marza_90.mean()
            efekt = g.status.isin(["completed", "no_show"])
            for wariant, oszcz in (("bez zniżki", g.znizka), ("START10 zamiast kodu", g.znizka - 10.0)):
                oe = np.where(efekt, oszcz, 0.0)
                dz = float(oe.mean())
                rows.append({"kampania": kamp, "regula": reg, "kod": kod, "wariant": wariant, "pierwsze_z_kodem_okres2": len(g),
                             "pierwsze_z_kodem_rok": len(g) * mn, "oszczednosc_na_pac": dz, "marza90_z_kodem": m90k,
                             "pacjenci_90": int(g.w90.sum()), "oszczednosc_rok_bez_utraty": oe.sum() * mn,
                             "prog_utraty_proc": 100 * dz / (dz + m90k)})
                sk = f"p6_{SKROT[kamp]}_{reg.lower()}_{'bez_kodu' if wariant == 'bez zniżki' else 'start10_zamiast_kodu'}"
                j(sk + "_oszczednosc_pelny_rok_zl", oe.sum() * mn)
                j(sk + "_oszczednosc_okres2_zl", oe.sum())
                j(sk + "_prog_utraty_pierwszych_zamowien_proc", 100 * dz / (dz + m90k))
                j(sk + "_pierwsze_z_kodem_okres2", len(g))
                j(sk + "_marza90_z_kodem_zl", m90k)
    pokaz(pd.DataFrame(rows).round(2))

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    with open(WYNIK_JSON, "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1)
    print(f"Zapisano {WYNIK} ({len(linie)} linii) i {WYNIK_JSON} ({len(J)} kluczy)")


if __name__ == "__main__":
    main()
