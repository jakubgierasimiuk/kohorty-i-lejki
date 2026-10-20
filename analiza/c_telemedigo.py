"""C — TelemediGO: skąd wzrost sprzedaży, opłaty wobec zniżek, zniżki wobec kosztu lekarza, powroty (2026-10-20).

Cztery pytania Kuby (notatki/DECYZJE.md, 2026-10-20):
  1. skąd wzrost sprzedaży o 40% (1 759 zakupów w okresie 1, 2 468 w okresie 2): zakup przy kasie z konsultacją
     wobec zakupu osobno (kampania crm_go_upsell od 8.09.2025), nowi i powracający kupujący, ponowne zakupy
     (TelemediGO nie odnawia się samo), kanały i pierwsza usługa;
  2. ile dają opłaty (89 zł) wobec zniżek udzielonych na wizytach w czasie ważności członkostwa (365 dni);
  3. czy wizyty ze zniżką pokrywają koszt lekarza, dla każdej specjalizacji, z uwzględnieniem zwrotów;
  4. czy TelemediGO zmienia powroty — z zastrzeżeniem samoselekcji (kupują pacjenci, którzy i tak planują wracać):
     porównanie z podobnymi pacjentami, dwie kontrole i projekt testu.

Definicje: analiza/definicje.py (ZALOZENIA.md 16–43). Okres zakupu TelemediGO = dzień zakupu (czas polski),
okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026. Zniżka w złotych = cena katalogowa − zapłata
(ZALOZENIA.md 14). „Zniżka efektywna” liczy tylko wizyty, za które zapłata zostaje (odbyte i nieodebrane), bo przy
anulowanej i zwróconej wizycie pacjent dostaje całą zapłatę z powrotem i zniżka nie zmienia przychodu.
Koszt lekarza: definicje.KOSZT_LEKARZA (25 zł internista, 200 zł psychiatra, 100 zł pozostali, także pediatra i
psycholog; za wizyty odbyte i zwrócone po wizycie).

Tylko czyta schemat `czyste`. Uruchomienie z głównego folderu projektu:
    python -I analiza/c_telemedigo.py
Wynik: analiza/wyniki/c_telemedigo.txt, analiza/wyniki/c_telemedigo_miesiace.csv (zestawienie miesięczne dla narzędzia,
bez wierszy pacjentów).
"""

import datetime as dt
import math
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import definicje as D  # noqa: E402
from a5r_struktura import GRUPA, USLUGA  # noqa: E402

WYNIK = os.path.join(D.KATALOG, "analiza", "wyniki", "c_telemedigo.txt")
WYNIK_CSV = os.path.join(D.KATALOG, "analiza", "wyniki", "c_telemedigo_miesiace.csv")
KONIEC = D.KONIEC
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)

GR_SPEC = """
  CASE WHEN specialization = 'internista' THEN '1_internista'
       WHEN specialization = 'psychiatra' THEN '2_psychiatra'
       WHEN specialization = 'pediatra' THEN '3_pediatra'
       ELSE '4_inny_specjalista' END"""


def zbuduj_go(con):
    """`go`: członkostwo z okresem zakupu, typem zakupu i kupującym; `go_zam`: zamówienia ze zniżką TelemediGO
    przypisane do członkostwa (w czasie ważności), z kosztem lekarza i zniżką."""
    con.execute(f"""
      CREATE TEMP TABLE go AS
      SELECT g.membership_id, g.user_id, g.purchased_at, g.purchased_at::DATE dzien, g.valid_until, g.order_id,
             g.session_id, CASE WHEN g.purchased_at < TIMESTAMP '{D.OKRES2}' THEN 1 ELSE 2 END okres,
             row_number() OVER (PARTITION BY g.user_id ORDER BY g.purchased_at) nr_go,
             z.nr nr_zam, s.utm_campaign kampania_sesji,
             CASE WHEN g.order_id IS NOT NULL AND z.nr = 1 THEN '1_kasa_z_pierwszym_zamowieniem'
                  WHEN g.order_id IS NOT NULL THEN '2_kasa_z_kolejnym_zamowieniem'
                  WHEN s.utm_campaign = 'crm_go_upsell' THEN '3_osobno_newsletter_crm_go_upsell'
                  ELSE '4_osobno_inne' END typ
      FROM czyste.go_memberships g
      LEFT JOIN zam z ON z.order_id = g.order_id
      LEFT JOIN czyste.sessions s ON s.session_id = g.session_id""")
    con.execute("""
      CREATE TEMP TABLE go_zam AS
      SELECT m.membership_id, m.okres okres_go, m.dzien dzien_go, m.typ, o.order_id, o.user_id, o.created_at,
             o.specialization, o.visit_purpose, o.status, o.list_price::DOUBLE cena, o.amount_paid::DOUBLE zaplata,
             o.refund_amount::DOUBLE zwrot,
             date_diff('day', m.dzien, o.created_at::DATE) dni_od_zakupu,
             (o.list_price - o.amount_paid)::DOUBLE znizka,
             CASE WHEN o.status IN ('completed', 'no_show') THEN (o.list_price - o.amount_paid)::DOUBLE ELSE 0 END znizka_efektywna,
             (o.amount_paid - o.refund_amount)::DOUBLE przychod,
             (CASE WHEN o.status IN ('completed', 'refunded')
                   THEN CASE o.specialization WHEN 'internista' THEN 25 WHEN 'psychiatra' THEN 200 ELSE 100 END
                   ELSE 0 END)::DOUBLE koszt_lekarza
      FROM go m JOIN czyste.orders o ON o.user_id = m.user_id AND o.created_at >= m.purchased_at
                                     AND o.created_at::DATE <= m.valid_until AND o.discount_type = 'go'""")


def rozklad_symetryczny(df, komorka, miara, waga="n"):
    """Zmiana średniej ważonej okres 2 − okres 1 rozłożona na nowe/zniknięte komórki, strukturę i zachowanie
    w komórkach wspólnych (jak a5r_struktura.rozklad). df: kolumny okres, komorka, n, miara (średnia w komórce)."""
    p = df.pivot_table(index=komorka, columns="okres", values=[waga, miara], aggfunc="sum").fillna(0)
    n1, n2 = p[(waga, 1)], p[(waga, 2)]
    r1 = df[df.okres == 1].set_index(komorka)[miara].reindex(p.index)
    r2 = df[df.okres == 2].set_index(komorka)[miara].reindex(p.index)
    R1 = (n1 * r1.fillna(0)).sum() / n1.sum()
    R2 = (n2 * r2.fillna(0)).sum() / n2.sum()
    C = (n1 > 0) & (n2 > 0)
    s1, s2 = n1[C] / n1[C].sum(), n2[C] / n2[C].sum()
    r1C, r2C = (s1 * r1[C]).sum(), (s2 * r2[C]).sum()
    return {"okres_1": R1, "okres_2": R2, "zmiana": R2 - R1, "nowe_komorki": R2 - r2C, "znikniete": r1C - R1,
            "struktura": ((s2 - s1) * (r1[C] + r2[C]) / 2).sum(), "zachowanie": ((r2[C] - r1[C]) * (s1 + s2) / 2).sum()}


def roznica_dopasowana(df, warstwy, wynik, grupa="go1"):
    """Różnica średnich wyniku między grupą z TelemediGO a podobnymi pacjentami bez niego, w tych samych
    warstwach (dokładne dopasowanie), ważona liczbą kupujących w warstwie (efekt wśród kupujących).
    Błąd standardowy z wariancji w warstwach; w warstwach z jednym pacjentem wariancja całej grupy."""
    v_cal = {g: df.loc[df[grupa] == g, wynik].var(ddof=1) for g in (0, 1)}
    s = df.groupby(warstwy + [grupa])[wynik].agg(["count", "mean", "var"]).unstack(grupa)
    s = s[(s[("count", 1)] > 0) & (s[("count", 0)] > 0)].copy()
    n_go = int((df[grupa] == 1).sum())
    if s.empty:
        return None
    w = s[("count", 1)] / s[("count", 1)].sum()
    v1 = s[("var", 1)].fillna(v_cal[1])
    v0 = s[("var", 0)].fillna(v_cal[0])
    m1 = (w * s[("mean", 1)]).sum()
    m0 = (w * s[("mean", 0)]).sum()
    se = math.sqrt((w ** 2 * (v1 / s[("count", 1)] + v0 / s[("count", 0)])).sum())
    return {"kupujacy": n_go, "dopasowani_kupujacy": int(s[("count", 1)].sum()),
            "pokrycie_proc": round(100 * s[("count", 1)].sum() / n_go, 1),
            "podobni_bez_go": int(s[("count", 0)].sum()), "z_go": m1, "podobni": m0, "roznica": m1 - m0,
            "od": m1 - m0 - 1.96 * se, "do": m1 - m0 + 1.96 * se}


def main():
    sys.stdout.reconfigure(errors="replace")
    con = D.polacz()
    D.zbuduj(con, crm=False, ekonomia=True)
    zbuduj_go(con)
    linie = []

    def r(tekst=""):
        linie.append(tekst)

    def pokaz(ramka, wciecie="     "):
        for linia in ramka.to_string(index=False).splitlines():
            r(wciecie + linia)

    def naglowek(t):
        r("\n" + "=" * 110)
        r(t)
        r("=" * 110)

    q = lambda s: con.sql(s).df()  # noqa: E731

    r(f"C — TELEMEDIGO ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")
    r("Okres zakupu = dzień zakupu członkostwa (czas polski): okres 1 = X 2024 – IX 2025, okres 2 = X 2025 – IX 2026.")
    r("TelemediGO: 89 zł za 365 dni, 50% zniżki u internisty, 20% u pozostałych; nie odnawia się samo.")
    r("Zniżka = cena katalogowa − zapłata. Zniżka efektywna = tylko wizyty, za które zapłata zostaje (odbyte i nieodebrane).")
    r("Koszt lekarza: 25 zł internista, 200 zł psychiatra, 100 zł pozostali (pediatra i psycholog też), za wizyty odbyte i")
    r("zwrócone po wizycie (ZALOZENIA.md 33). Obserwacje, nie wnioski: przyczyn nie przesądzamy.")

    # ---------- 0. kontrola ----------
    naglowek("0. KONTROLA: liczba zakupów TelemediGO w okresach (A3: 1 759 i 2 468, +40,3%)")
    k = q("SELECT okres, count(*) zakupy, sum(amount_paid)::DOUBLE oplaty_zl FROM go JOIN czyste.go_memberships USING (membership_id) GROUP BY 1 ORDER BY 1")
    pokaz(k)
    r(f"     zmiana: {k.zakupy[1] - k.zakupy[0]:+d} zakupów, {100 * (k.zakupy[1] / k.zakupy[0] - 1):+.1f}%")
    wyj = q("SELECT count(*) FILTER (WHERE date_diff('day', purchased_at::DATE, valid_until) <> 365 OR amount_paid <> 89) n FROM czyste.go_memberships").n[0]
    r(f"     każde członkostwo trwa dokładnie 365 dni i kosztuje 89 zł: {wyj} wyjątków")
    zn_spr = q("SELECT count(*) n, count(*) FILTER (WHERE membership_id IS NULL) bez_czlonkostwa FROM czyste.orders o LEFT JOIN go_zam g USING (order_id) WHERE o.discount_type = 'go'")
    r(f"     zamówienia ze zniżką TelemediGO: {zn_spr.n[0]}, w tym poza okresem ważności członkostwa: {zn_spr.bez_czlonkostwa[0]}")

    # ---------- 1. skąd wzrost ----------
    naglowek("1. SKĄD WZROST SPRZEDAŻY O 40%")
    r("1a. Typ zakupu. Przy kasie = razem z zamówieniem konsultacji; osobno = sam TelemediGO (strona /telemedigo).")
    t = q("SELECT typ, okres, count(*) n FROM go GROUP BY ALL").pivot_table(index="typ", columns="okres", values="n", fill_value=0)
    t.columns = ["okres_1", "okres_2"]
    t["zmiana"] = t.okres_2 - t.okres_1
    t["zmiana_proc"] = (100 * (t.okres_2 / t.okres_1.replace(0, np.nan) - 1)).round(1)
    t["udzial_we_wzroscie_proc"] = (100 * t.zmiana / t.zmiana.sum()).round(1)
    t.loc["razem"] = [t.okres_1.sum(), t.okres_2.sum(), t.zmiana.sum(), round(100 * (t.okres_2.sum() / t.okres_1.sum() - 1), 1), 100.0]
    pokaz(t.reset_index())
    kasa = t.loc[["1_kasa_z_pierwszym_zamowieniem", "2_kasa_z_kolejnym_zamowieniem"]].sum()
    r(f"     przy kasie razem: {int(kasa.okres_1)} → {int(kasa.okres_2)} ({100 * (kasa.okres_2 / kasa.okres_1 - 1):+.1f}%); "
      f"osobno razem: {int(t.okres_1.iloc[2:4].sum())} → {int(t.okres_2.iloc[2:4].sum())}")
    r("\n1b. Zakupy osobne w kampanii crm_go_upsell miesiąc po miesiącu (start 8.09.2025; w okresie 1 tylko 23 dni września).")
    m = q("""SELECT strftime(dzien, '%Y-%m') miesiac, count(*) FILTER (WHERE typ LIKE '3_%') osobno_crm,
                    count(*) FILTER (WHERE typ LIKE '1_%' OR typ LIKE '2_%') przy_kasie, count(*) razem
             FROM go WHERE dzien >= DATE '2025-07-01' GROUP BY 1 ORDER BY 1""")
    pokaz(m)
    wrz = q("""SELECT count(*) FILTER (WHERE dzien BETWEEN DATE '2025-09-08' AND DATE '2025-09-30') w_23_dniach,
                      count(*) FILTER (WHERE okres = 2) / 12.0 srednio_na_miesiac_okres_2
               FROM go WHERE typ LIKE '3_%'""")
    r(f"     Pierwsze 23 dni kampanii: {int(wrz.w_23_dniach[0])} zakupów; w okresie 2 średnio {wrz.srednio_na_miesiac_okres_2[0]:.1f} miesięcznie.")
    r("     Odczytanie do sprawdzenia: start kampanii zebrał od razu pacjentów, którzy czekali na ofertę, a potem sprzedaż")
    r("     osobna ustala się na niższym poziomie. Wysyłek w danych nie ma (widać tylko wejścia), więc nie wiemy, ile")
    r("     wiadomości wysłano w kolejnych miesiącach.")

    r("\n1c. Kupujący: pierwsze członkostwo pacjenta wobec drugiego (ponowny zakup po wygaśnięciu pierwszego).")
    t = q("""SELECT CASE WHEN nr_go = 1 AND typ LIKE '1_%' THEN '1_nowy_pacjent_pierwsze_go'
                         WHEN nr_go = 1 THEN '2_pacjent_juz_kupowal_pierwsze_go'
                         ELSE '3_ponowny_zakup_drugie_go' END kupujacy, okres, count(*) n
             FROM go GROUP BY ALL""").pivot_table(index="kupujacy", columns="okres", values="n", fill_value=0)
    t.columns = ["okres_1", "okres_2"]
    t["zmiana"] = t.okres_2 - t.okres_1
    t["udzial_we_wzroscie_proc"] = (100 * t.zmiana / t.zmiana.sum()).round(1)
    pokaz(t.reset_index())

    r("\n1d. Ponowne zakupy. Członkostwa z okresu 1 wygasają w okresie 2 (ważność 365 dni). Odnowienie = kolejny zakup")
    r("    tego samego pacjenta. Liczymy tylko członkostwa, po których wygaśnięciu jest N dni obserwacji.")
    odn = []
    for n in (30, 90, 180):
        x = q(f"""SELECT count(*) wygasle,
                        count(*) FILTER (WHERE EXISTS (SELECT 1 FROM go g2 WHERE g2.user_id = g.user_id AND g2.nr_go = g.nr_go + 1
                                                       AND g2.dzien <= g.valid_until + INTERVAL {n} DAY)) odnowione,
                        count(*) FILTER (WHERE EXISTS (SELECT 1 FROM zam z WHERE z.user_id = g.user_id AND z.status <> 'cancelled'
                                                       AND z.created_at::DATE > g.valid_until
                                                       AND z.created_at::DATE <= g.valid_until + INTERVAL {n} DAY)) z_zamowieniem_po
                 FROM go g WHERE g.valid_until + INTERVAL {n} DAY <= DATE '{KONIEC}'""")
        odn.append({"dni_po_wygasnieciu": n, "wygasle_czlonkostwa": int(x.wygasle[0]), "odnowione": int(x.odnowione[0]),
                    "odnowione_proc": round(100 * x.odnowione[0] / x.wygasle[0], 1),
                    "pacjenci_z_zamowieniem_po_wygasnieciu": int(x.z_zamowieniem_po[0]),
                    "z_zamowieniem_proc": round(100 * x.z_zamowieniem_po[0] / x.wygasle[0], 1)})
    pokaz(pd.DataFrame(odn))
    dr = q("""SELECT g2.typ, count(*) n, median(date_diff('day', g1.valid_until, g2.dzien)) mediana_dni_od_wygasniecia,
                     min(date_diff('day', g1.valid_until, g2.dzien)) min_dni
              FROM go g2 JOIN go g1 ON g1.user_id = g2.user_id AND g1.nr_go = g2.nr_go - 1 GROUP BY 1 ORDER BY 1""")
    r("    Drugie członkostwa (wszystkie są w okresie 2), według typu zakupu i odstępu od wygaśnięcia pierwszego:")
    pokaz(dr)
    wyg = q(f"SELECT count(*) n FROM go WHERE valid_until BETWEEN DATE '{D.OKRES2}' AND DATE '{KONIEC}'").n[0]
    r(f"    W okresie 2 wygasa {wyg} członkostw. Odnowienia nie są przypominane automatycznie (słownik danych),")
    r("    a w danych nie widać kampanii przypominającej o wygaśnięciu.")

    r("\n1e. Zakup przy kasie jako odsetek zamówień, przy których pacjent nie miał ważnego członkostwa (zamówienia „do")
    r("    oferty”). Rozbicie wzrostu zakupów przy kasie na liczbę zamówień i odsetek kupujących.")
    zk = q("""SELECT CASE WHEN created_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres,
                     CASE WHEN nr = 1 THEN '1_pierwsze_zamowienie' ELSE '2_kolejne_zamowienie' END zamowienie,
                     count(*) zamowienia_do_oferty,
                     count(*) FILTER (WHERE EXISTS (SELECT 1 FROM go g WHERE g.order_id = z.order_id)) z_go_przy_kasie
              FROM zam z
              WHERE NOT EXISTS (SELECT 1 FROM go g WHERE g.user_id = z.user_id AND g.purchased_at < z.created_at
                                                    AND g.valid_until >= z.created_at::DATE)
              GROUP BY ALL ORDER BY 2, 1""")
    zk["odsetek_proc"] = (100 * zk.z_go_przy_kasie / zk.zamowienia_do_oferty).round(2)
    pokaz(zk)
    for zam_typ in ("1_pierwsze_zamowienie", "2_kolejne_zamowienie"):
        a = zk[zk.zamowienie == zam_typ].set_index("okres")
        p1 = a.z_go_przy_kasie[1] / a.zamowienia_do_oferty[1]
        ef_wol = (a.zamowienia_do_oferty[2] - a.zamowienia_do_oferty[1]) * p1
        ef_ods = a.zamowienia_do_oferty[2] * (a.z_go_przy_kasie[2] / a.zamowienia_do_oferty[2] - p1)
        r(f"     {zam_typ}: zmiana {a.z_go_przy_kasie[2] - a.z_go_przy_kasie[1]:+d} zakupów = więcej zamówień "
          f"{ef_wol:+.0f} + zmiana odsetka {ef_ods:+.0f}")

    r("\n1f. Odsetek nowych pacjentów, którzy kupują TelemediGO przy pierwszym zamówieniu, według grupy kampanii")
    r("    pozyskania (przyjęta reguła źródła, ZALOZENIA.md 22) i według pierwszej usługi.")
    con.execute(f"""
      CREATE TEMP TABLE np AS
      SELECT k.user_id, k.order_id order1, k.okres, k.d0, r.kanal, r.kampania, r.kanal_z2, {GRUPA} grupa, {USLUGA} usluga,
             z.status status1, z.discount_type znizka1, (g.membership_id IS NOT NULL)::INT go1
      FROM koh k JOIN zrodlo r USING (user_id) JOIN zam z ON z.order_id = k.order_id
      LEFT JOIN go g ON g.order_id = k.order_id""")
    for wymiar in ("grupa", "kanal", "usluga"):
        t = q(f"SELECT {wymiar}, okres, count(*) n, avg(go1) * 100 odsetek FROM np GROUP BY ALL")
        p = t.pivot_table(index=wymiar, columns="okres", values=["n", "odsetek"])
        p.columns = [f"{a}_okres_{b}" for a, b in p.columns]
        p = p.fillna(0).round(2).reset_index()
        for c in ("n_okres_1", "n_okres_2"):
            p[c] = p[c].astype(int)
        pokaz(p)
        r()
    tot = q("SELECT okres, count(*) n, avg(go1) * 100 odsetek, sum(go1) z_go FROM np GROUP BY 1 ORDER BY 1")
    pokaz(tot)
    bez_nowych = q("SELECT okres, count(*) n, avg(go1) * 100 odsetek, sum(go1) z_go FROM np WHERE grupa NOT IN ('2_meta_l4_szybko', '3_tiktok') GROUP BY 1 ORDER BY 1")
    r("     bez pacjentów dwóch nowych kampanii na L4:")
    pokaz(bez_nowych)
    kom = q("SELECT okres, grupa || ' | ' || usluga komorka, count(*) n, avg(go1) odsetek FROM np GROUP BY ALL")
    rz = rozklad_symetryczny(kom, "komorka", "odsetek")
    r("     Rozkład zmiany odsetka (punkty procentowe) na komórki grupa kampanii × pierwsza usługa:")
    r("     " + ", ".join(f"{k_}: {100 * v:+.2f}" for k_, v in rz.items()))
    r("     „nowe_komorki” = segmenty bez pacjentów w okresie 1 (np. nowe kampanie na L4). Opis, nie przyczyna.")

    r("\n1g. Wszystkie zakupy TelemediGO według kanału pozyskania kupującego (przyjęta reguła źródła).")
    t = q("""SELECT r.kanal, g.okres, count(*) n FROM go g JOIN zrodlo r USING (user_id) GROUP BY ALL""")
    p = t.pivot_table(index="kanal", columns="okres", values="n", fill_value=0)
    p.columns = ["okres_1", "okres_2"]
    p["zmiana"] = p.okres_2 - p.okres_1
    p["udzial_we_wzroscie_proc"] = (100 * p.zmiana / p.zmiana.sum()).round(1)
    pokaz(p.sort_values("zmiana", ascending=False).reset_index())

    # ---------- 2. opłaty wobec zniżek ----------
    naglowek("2. OPŁATY ZA TELEMEDIGO WOBEC ZNIŻEK UDZIELONYCH NA WIZYTACH")
    r("2a. Na członkostwo, w czasie jego ważności (365 dni). Członkostwa z okresu 1 mają pełne okno (wygasają najpóźniej")
    r("    30.09.2026). Członkostwa z okresu 2 jeszcze trwają, więc pokazujemy je w 2b w tych samych dniach od zakupu.")
    a = q("""SELECT m.okres, count(DISTINCT m.membership_id) czlonkostwa, 89.0 * count(DISTINCT m.membership_id) oplaty_zl,
                    coalesce(sum(z.znizka), 0) znizka_nominalna_zl, coalesce(sum(z.znizka_efektywna), 0) znizka_efektywna_zl,
                    count(z.order_id) zamowienia_ze_znizka
             FROM go m LEFT JOIN go_zam z USING (membership_id) WHERE m.okres = 1 GROUP BY 1""")
    a["znizka_efektywna_na_czlonkostwo"] = (a.znizka_efektywna_zl / a.czlonkostwa).round(2)
    a["oplata_minus_znizka_efektywna_na_czlonkostwo"] = (89 - a.znizka_efektywna_na_czlonkostwo).round(2)
    a["oplaty_minus_znizki_efektywne_zl"] = (a.oplaty_zl - a.znizka_efektywna_zl).round(0)
    a["zamowienia_na_czlonkostwo"] = (a.zamowienia_ze_znizka / a.czlonkostwa).round(2)
    pokaz(a.T.reset_index().rename(columns={"index": "miara", 0: "okres_1"}))
    roznica_zl = f"{-a.oplaty_minus_znizki_efektywne_zl[0]:,.0f}".replace(",", " ")
    r(f"    Przy założeniu, że te same wizyty zostałyby kupione po cenie katalogowej bez TelemediGO, opłaty są o {roznica_zl} zł")
    r("    niższe od udzielonych zniżek. To nie jest wynik programu:")
    r("    nie wiemy, ile wizyt członkostwo dokłada (sekcja 4), a koszt lekarza za wizyty zwrócone jest w rachunku marży (sekcja 3).")
    r("    Okres 1 według typu zakupu i grupy specjalizacji (zniżka efektywna na członkostwo, zł):")
    t = q("""SELECT m.typ, count(DISTINCT m.membership_id) czlonkostwa,
                    sum(z.znizka_efektywna) FILTER (WHERE z.specialization = 'internista') / count(DISTINCT m.membership_id) internista,
                    sum(z.znizka_efektywna) FILTER (WHERE z.specialization <> 'internista') / count(DISTINCT m.membership_id) specjalisci,
                    coalesce(sum(z.znizka_efektywna), 0) / count(DISTINCT m.membership_id) razem,
                    count(z.order_id) / count(DISTINCT m.membership_id) zamowienia_na_czlonkostwo
             FROM go m LEFT JOIN go_zam z USING (membership_id) WHERE m.okres = 1 GROUP BY 1 ORDER BY 1""")
    bez = q("""SELECT m.typ, avg((NOT EXISTS (SELECT 1 FROM go_zam z WHERE z.membership_id = m.membership_id AND z.znizka_efektywna > 0))::INT) * 100 bez_zniżki_efektywnej_proc,
                      avg((SELECT count(*) FROM go_zam z WHERE z.membership_id = m.membership_id AND z.znizka_efektywna > 0 AND z.order_id <> coalesce(m.order_id, -1))) wizyty_po_zakupie
               FROM go m WHERE m.okres = 1 GROUP BY 1 ORDER BY 1""")
    t = t.merge(bez, on="typ")
    pokaz(t.round(2))
    r("    „wizyty_po_zakupie” = wizyty ze zniżką efektywną poza zamówieniem, przy którym kupiono członkostwo.")
    r("    Rozkład zniżki efektywnej na członkostwo (okres 1, zł):")
    roz = q("""SELECT m.membership_id, coalesce(sum(z.znizka_efektywna), 0) zn FROM go m LEFT JOIN go_zam z USING (membership_id)
               WHERE m.okres = 1 GROUP BY 1""")
    r("     " + ", ".join(f"{p_}%: {roz.zn.quantile(p_ / 100):.1f}" for p_ in (10, 25, 50, 75, 90, 99)) +
      f"; powyżej 89 zł: {100 * (roz.zn > 89).mean():.1f}% członkostw")

    r("\n2b. Zniżka efektywna narastająco w dniach od zakupu, członkostwa z pełnym oknem N dni (oba okresy).")
    rows = []
    for n in (0, 30, 90, 180, 365):
        x = q(f"""SELECT m.okres, count(DISTINCT m.membership_id) czlonkostwa,
                         coalesce(sum(z.znizka_efektywna), 0) / count(DISTINCT m.membership_id) znizka_na_czlonkostwo
                  FROM go m LEFT JOIN go_zam z ON z.membership_id = m.membership_id AND z.dni_od_zakupu <= {n}
                  WHERE m.dzien + INTERVAL {n} DAY <= DATE '{KONIEC}' GROUP BY 1 ORDER BY 1""")
        for _, w in x.iterrows():
            rows.append({"dni": n, "okres": int(w.okres), "czlonkostwa": int(w.czlonkostwa), "znizka_na_czlonkostwo_zl": round(w.znizka_na_czlonkostwo, 2)})
    t = pd.DataFrame(rows).pivot_table(index="dni", columns="okres", values=["czlonkostwa", "znizka_na_czlonkostwo_zl"])
    t.columns = [f"{a_}_okres_{b}" for a_, b in t.columns]
    pokaz(t.reset_index())
    r("    Dzień 0 = zamówienie, przy którym kupiono członkostwo (dla zakupów przy kasie), i inne zamówienia tego dnia.")
    t180 = t.loc[180]
    proj = t.loc[365, "znizka_na_czlonkostwo_zl_okres_1"] * t180["znizka_na_czlonkostwo_zl_okres_2"] / t180["znizka_na_czlonkostwo_zl_okres_1"]
    r(f"    Przybliżenie dla okresu 2 (dni 181–365 w tej samej proporcji co w okresie 1): {proj:.1f} zł zniżki na członkostwo,")
    r(f"    czyli {89 - proj:+.1f} zł opłaty ponad zniżkę na członkostwo. To przybliżenie, nie wynik.")

    r("\n2c. Rok kalendarzowy (widok kasowy): opłaty za członkostwa kupione w okresie wobec zniżek na zamówieniach")
    r("    złożonych w tym samym okresie (także na członkostwach kupionych wcześniej).")
    kas = q("""SELECT o.okres, o.oplaty_zl, z.znizka_nominalna_zl, z.znizka_efektywna_zl, z.zamowienia_ze_znizka
               FROM (SELECT okres, 89.0 * count(*) oplaty_zl FROM go GROUP BY 1) o
               JOIN (SELECT CASE WHEN created_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres,
                            sum(znizka) znizka_nominalna_zl, sum(znizka_efektywna) znizka_efektywna_zl, count(*) zamowienia_ze_znizka
                     FROM go_zam GROUP BY 1) z USING (okres) ORDER BY 1""")
    kas["oplaty_minus_znizki_efektywne_zl"] = kas.oplaty_zl - kas.znizka_efektywna_zl
    pokaz(kas.round(0))

    # ---------- 3. zniżki wobec kosztu lekarza ----------
    naglowek("3. CZY WIZYTY ZE ZNIŻKĄ TELEMEDIGO POKRYWAJĄ KOSZT LEKARZA")
    r("3a. Cennik (z danych): cena katalogowa, cena po zniżce TelemediGO, koszt lekarza za wizytę odbytą, marża na wizycie.")
    c = q("""SELECT specialization, any_value(list_price)::DOUBLE cena, count(DISTINCT list_price) liczba_cen,
                    avg(amount_paid) FILTER (WHERE discount_type = 'go')::DOUBLE cena_z_go,
                    CASE specialization WHEN 'internista' THEN 25 WHEN 'psychiatra' THEN 200 ELSE 100 END koszt_lekarza
             FROM czyste.orders GROUP BY 1 ORDER BY 2""")
    c["znizka_proc"] = (100 * (1 - c.cena_z_go / c.cena)).round(1)
    c["marza_bez_znizki"] = c.cena - c.koszt_lekarza
    c["marza_z_go"] = (c.cena_z_go - c.koszt_lekarza).round(2)
    pokaz(c)

    r("\n3b. Rzeczywiste zamówienia ze zniżką TelemediGO wobec zamówień bez zniżki, obie lata razem, z anulacjami,")
    r("    nieodebranymi i zwrotami. Marża = przychód po zwrotach − koszt lekarza (także za wizyty zwrócone po wizycie).")
    b = q(f"""SELECT {GR_SPEC} grupa, specialization, discount_type znizka, count(*) zamowienia,
                     avg((status = 'refunded')::INT) * 100 zwrocone_po_wizycie_proc, avg((status = 'cancelled')::INT) * 100 anulowane_proc,
                     sum(amount_paid - refund_amount)::DOUBLE przychod_zl, sum({D.KOSZT_LEKARZA})::DOUBLE koszt_lekarza_zl
              FROM czyste.orders WHERE discount_type IN ('go', 'none') GROUP BY ALL ORDER BY 1, 2, 3""")
    b["marza_zl"] = b.przychod_zl - b.koszt_lekarza_zl
    b["marza_na_zamowienie"] = (b.marza_zl / b.zamowienia).round(2)
    pokaz(b.round(1))

    r("\n3c. Suma marży na zamówieniach ze zniżką TelemediGO, według grupy specjalizacji i okresu zamówienia (zł).")
    s3 = q(f"""SELECT {GR_SPEC} grupa, CASE WHEN created_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres, count(*) zamowienia,
                      sum(amount_paid - refund_amount)::DOUBLE przychod_zl, sum({D.KOSZT_LEKARZA})::DOUBLE koszt_lekarza_zl,
                      sum(CASE WHEN status IN ('completed', 'no_show') THEN list_price - amount_paid ELSE 0 END)::DOUBLE znizka_efektywna_zl
               FROM czyste.orders WHERE discount_type = 'go' GROUP BY ALL ORDER BY 1, 2""")
    s3["marza_zl"] = s3.przychod_zl - s3.koszt_lekarza_zl
    pokaz(s3.round(0))
    pod = q(f"""SELECT CASE WHEN created_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres,
                       count(*) zamowienia, sum(amount_paid - refund_amount - {D.KOSZT_LEKARZA})::DOUBLE marza_zl,
                       sum(CASE WHEN status IN ('completed', 'no_show') THEN list_price - amount_paid ELSE 0 END)::DOUBLE znizka_efektywna_zl
                FROM czyste.orders WHERE discount_type = 'go' AND specialization NOT IN ('internista', 'psychiatra') GROUP BY 1 ORDER BY 1""")
    r("     Specjaliści z ceną po zniżce poniżej kosztu lekarza (wszyscy poza internistą i psychiatrą):")
    pokaz(pod.round(0))
    r("     Scenariusze zmiany warunków (zniżka 0% u tych specjalistów, internista i psychiatra bez zmian), rocznie. To")
    r("     scenariusze, nie granice (recenzja Codeksa): pacjenci mogą reagować różnie przy różnych wizytach.")
    sc = q(f"""SELECT CASE WHEN created_at < TIMESTAMP '2025-10-01' THEN 1 ELSE 2 END okres, m, d FROM (
                 SELECT created_at, (amount_paid - refund_amount - {D.KOSZT_LEKARZA})::DOUBLE m,
                        CASE WHEN status IN ('completed', 'no_show') THEN list_price - amount_paid ELSE 0 END::DOUBLE d
                 FROM czyste.orders WHERE discount_type = 'go' AND specialization NOT IN ('internista', 'psychiatra'))""")
    sc["znika"] = -sc.m
    sc = sc.groupby("okres").apply(lambda g: pd.Series({
        "znikaja_wszystkie": g.znika.sum(), "zostaja_wszystkie_po_cenie_katalogowej": g.d.sum(),
        "znikaja_tylko_zamowienia_ze_strata": g.znika[g.m < 0].sum(),
        "kazde_zamowienie_najgorzej": np.minimum(g.znika, g.d).sum(), "kazde_zamowienie_najlepiej": np.maximum(g.znika, g.d).sum()}),
        include_groups=False).reset_index()
    pokaz(sc.round(0))
    r("     „znikaja_wszystkie” = znikają wszystkie te zamówienia (także nieodebrane, które dziś dają marżę bez kosztu lekarza);")
    r("     „zostaja_...” = wszystkie zostają po cenie katalogowej; ostatnie dwie kolumny = każde zamówienie osobno znika albo")
    r("     zostaje, w wariancie najgorszym i najlepszym. Bez wpływu na sprzedaż członkostw (część pacjentów może rzadziej")
    r("     kupować TelemediGO).")

    # ---------- 4. powroty ----------
    naglowek("4. CZY TELEMEDIGO ZMIENIA POWROTY (zastrzeżenie samoselekcji)")
    r("Uwaga: TelemediGO kupują pacjenci, którzy i tak planują wracać. Różnica w powrotach między kupującymi a podobnymi")
    r("pacjentami bez TelemediGO to suma dwóch rzeczy: wpływu niższej ceny i tego, że kupują inni ludzie. Dane")
    r("obserwacyjne ich nie rozdzielają. Kontrole w 4b i 4c to opisy zgodne z kilkoma wyjaśnieniami; żadna z nich")
    r("nie rozstrzyga między nimi (recenzja Codeksa).")
    r("\n4a. Nowi pacjenci, którzy kupili TelemediGO przy pierwszym zamówieniu, wobec podobnych pacjentów bez niego.")
    r("    Dopasowanie dokładne w warstwach: okres, kanał pozyskania (przyjęta reguła), pierwsza usługa, miesiąc kohorty.")
    r("    Wynik ważony liczbą kupujących w warstwie. Przedział 95% z wariancji w warstwach (bez niepewności dopasowania).")
    con.execute("""
      CREATE TEMP TABLE np2 AS
      SELECT n.*, p.dni_R2, strftime(n.d0, '%Y-%m') miesiac,
             coalesce((SELECT count(*) FROM zam z WHERE z.user_id = n.user_id AND z.nr > 1 AND z.status <> 'cancelled'
                       AND date_diff('day', n.d0, z.created_at::DATE) BETWEEN 1 AND 365), 0) zam_365,
             coalesce((SELECT sum(marza) FROM ek e WHERE e.user_id = n.user_id AND e.dni BETWEEN 1 AND 90), 0) marza_1_90,
             coalesce((SELECT sum(marza) FROM ek e WHERE e.user_id = n.user_id AND e.dni BETWEEN 1 AND 180), 0) marza_1_180,
             coalesce((SELECT sum(marza) FROM ek e WHERE e.user_id = n.user_id AND e.dni BETWEEN 1 AND 365), 0) marza_1_365,
             coalesce((SELECT sum(marza) FROM ek e WHERE e.user_id = n.user_id AND e.dni BETWEEN 0 AND 90), 0) marza_0_90,
             coalesce((SELECT sum(marza) FROM ek e WHERE e.user_id = n.user_id AND e.dni BETWEEN 0 AND 365), 0) marza_0_365
      FROM np n JOIN powr p USING (user_id)""")
    np2 = q("SELECT * FROM np2")
    np2["d0"] = pd.to_datetime(np2["d0"])
    kon = pd.Timestamp(KONIEC)
    wyniki = []
    for okno, wynik, opis in ((90, "y90", "powrót w 90 dniach (%)"), (180, "y180", "powrót w 180 dniach (%)"),
                              (365, "zam_365", "kolejne zamówienia nieanulowane w 365 dniach"),
                              (90, "marza_1_90", "marża dni 1–90 (zł)"), (180, "marza_1_180", "marża dni 1–180 (zł)"),
                              (365, "marza_1_365", "marża dni 1–365 (zł)"),
                              (90, "marza_0_90", "marża dni 0–90 z opłatą 89 zł (zł)"),
                              (365, "marza_0_365", "marża dni 0–365 z opłatą 89 zł (zł)")):
        a_ = np2[np2.d0 <= kon - pd.Timedelta(days=okno)].copy()
        # brak powrotu = puste dni_R2; bez wypełnienia pandas pomija te wiersze w średniej (zawyżony powrót)
        dni = a_.dni_R2.astype("float64").fillna(1e9)
        a_["y90"] = 100.0 * (dni <= 90)
        a_["y180"] = 100.0 * (dni <= 180)
        for okr in ([1], [2], [1, 2]):
            b_ = a_[a_.okres.isin(okr)]
            if (b_.go1 == 1).sum() < 30 or (len(okr) == 2 and (b_.okres == 2).sum() == 0):
                continue
            surowe = b_.groupby("go1")[wynik].mean()
            for warstwy, nazwa in ((["okres", "kanal", "usluga", "miesiac"], "kanał+usługa+miesiąc"),
                                   (["okres", "kanal", "usluga", "miesiac", "status1"], "+ status pierwszego zamówienia")):
                d_ = roznica_dopasowana(b_, warstwy, wynik)
                wyniki.append({"miara": opis, "okresy": "+".join(map(str, okr)), "warstwy": nazwa,
                               "kupujacy": d_["kupujacy"], "pokrycie_proc": d_["pokrycie_proc"],
                               "surowe_z_go": round(surowe[1], 2), "surowe_bez_go": round(surowe[0], 2),
                               "dopasowane_z_go": round(d_["z_go"], 2), "podobni_bez_go": round(d_["podobni"], 2),
                               "roznica": round(d_["roznica"], 2), "od": round(d_["od"], 2), "do": round(d_["do"], 2)})
    w4 = pd.DataFrame(wyniki)
    pokaz(w4)
    r("    Marża dni 1–N obejmuje niższe ceny wizyt ze zniżką i ewentualny drugi zakup TelemediGO; nie obejmuje opłaty")
    r("    89 zł z dnia 0. Wiersze „dni 0–N” dodają dzień 0: opłatę 89 zł i zniżkę na pierwszym zamówieniu.")

    r("\n4b. Kontrola 1 — przebieg zamówień przed wygaśnięciem członkostwa i po nim. Gdyby różnica brała się tylko z niższej")
    r("    ceny, po wygaśnięciu (dzień 366) powinna zniknąć; gdyby tylko z tego, że kupują inni pacjenci, powinna zostać.")
    r("    Okres 1, kohorty do 3.07.2025 (pełne 455 dni). Grupa porównawcza: bez żadnego zakupu TelemediGO do dnia 455.")
    r("    Dwie wersje grupy z TelemediGO: (1) bez kolejnego zakupu członkostwa do dnia 455 — wyłączenie zależy od zachowania")
    r("    po zakupie i usuwa najaktywniejszych; (2) wszyscy pierwotni kupujący, także odnawiający (recenzja Codeksa).")
    con.execute("""
      CREATE TEMP TABLE kontrola_wyg AS
      SELECT n.user_id, n.okres, n.kanal, n.usluga, strftime(n.d0, '%Y-%m') miesiac, n.go1, n.d0,
             EXISTS (SELECT 1 FROM go g WHERE g.user_id = n.user_id AND g.order_id IS DISTINCT FROM n.order1
                     AND date_diff('day', n.d0, g.dzien) BETWEEN 0 AND 455) inne_go_do_455,
             EXISTS (SELECT 1 FROM zam z WHERE z.user_id = n.user_id AND z.nr > 1 AND z.status <> 'cancelled'
                     AND date_diff('day', n.d0, z.created_at::DATE) BETWEEN 276 AND 365)::INT * 100 ost_kwartal_waznosci,
             EXISTS (SELECT 1 FROM zam z WHERE z.user_id = n.user_id AND z.nr > 1 AND z.status <> 'cancelled'
                     AND date_diff('day', n.d0, z.created_at::DATE) BETWEEN 366 AND 455)::INT * 100 kwartal_po_wygasnieciu,
             EXISTS (SELECT 1 FROM zam z WHERE z.user_id = n.user_id AND z.nr > 1 AND z.status <> 'cancelled'
                     AND date_diff('day', n.d0, z.created_at::DATE) BETWEEN 1 AND 90)::INT * 100 pierwszy_kwartal
      FROM np n
      WHERE n.okres = 1 AND n.d0 <= DATE '2025-07-03'""")
    kw_all = q("SELECT * FROM kontrola_wyg")
    kw_all = kw_all[(kw_all.go1 == 1) | ~kw_all.inne_go_do_455]
    for wersja, kw in (("(1) bez odnawiających", kw_all[~kw_all.inne_go_do_455]), ("(2) wszyscy kupujący", kw_all)):
        rows = []
        for wynik, opis in (("pierwszy_kwartal", "dni 1–90 (członkostwo ważne)"), ("ost_kwartal_waznosci", "dni 276–365 (członkostwo ważne)"),
                            ("kwartal_po_wygasnieciu", "dni 366–455 (po wygaśnięciu)")):
            d_ = roznica_dopasowana(kw, ["kanal", "usluga", "miesiac"], wynik)
            rows.append({"wersja": wersja, "okno": opis, "kupujacy": d_["kupujacy"], "pokrycie_proc": d_["pokrycie_proc"],
                         "z_go_proc": round(d_["z_go"], 2), "podobni_proc": round(d_["podobni"], 2),
                         "roznica_pkt": round(d_["roznica"], 2), "od": round(d_["od"], 2), "do": round(d_["do"], 2),
                         "iloraz": round(d_["z_go"] / d_["podobni"], 2)})
        pokaz(pd.DataFrame(rows))
    r("    Miara: odsetek pacjentów z co najmniej jednym nieanulowanym zamówieniem w danym oknie. Iloraz = z_go / podobni.")
    r("    Różnica w punktach maleje po wygaśnięciu, ale poziom zamówień też spada, więc patrzymy też na iloraz. Wynik jest")
    r("    zgodny z kilkoma wyjaśnieniami i nie rozstrzyga między nimi (recenzja Codeksa).")

    r("\n4c. Kontrola 2 — pacjenci, którzy weszli z newslettera crm_go_upsell: kupili TelemediGO osobno wobec tych, którzy")
    r("    nie kupili przy wejściu i przez następne 30 dni. Obie grupy zainteresowały się ofertą. Zamówienia nieanulowane na")
    r("    pacjenta w 180 dniach przed i po dniu odniesienia (zakup albo pierwsze wejście bez zakupu), dzień odniesienia do")
    r("    3.04.2026 (pełne 180 dni). Wiersz kupil = 0 obejmuje też pacjentów, którzy kupili członkostwo później w oknie")
    r("    180 dni; wiersz kupil = -1 to ta sama grupa bez nich (kontrola wrażliwości; wyłączenie też selekcjonuje według")
    r("    przyszłego zachowania).")
    con.execute(f"""
      CREATE TEMP TABLE upsell AS
      WITH wej AS (
        SELECT pacjent user_id, min(started_at_pl) pierwsze_wejscie FROM ses_pac WHERE utm_campaign = 'crm_go_upsell' GROUP BY 1),
      kup AS (SELECT user_id, min(purchased_at) zakup FROM go WHERE typ LIKE '3_%' GROUP BY 1)
      SELECT w.user_id, (k.zakup IS NOT NULL)::INT kupil, coalesce(k.zakup, w.pierwsze_wejscie) t_ref
      FROM wej w LEFT JOIN kup k USING (user_id)
      WHERE NOT EXISTS (SELECT 1 FROM go g WHERE g.user_id = w.user_id AND g.purchased_at < coalesce(k.zakup, w.pierwsze_wejscie)
                                              AND g.valid_until >= coalesce(k.zakup, w.pierwsze_wejscie)::DATE)
        AND (k.zakup IS NOT NULL OR NOT EXISTS (SELECT 1 FROM go g WHERE g.user_id = w.user_id
                                                 AND g.purchased_at >= w.pierwsze_wejscie
                                                 AND g.purchased_at < w.pierwsze_wejscie + INTERVAL 30 DAY))""")
    u = q(f"""SELECT kupil, kupil_pozniej, count(*) pacjenci,
                     avg((SELECT count(*) FROM zam z WHERE z.user_id = u.user_id AND z.status <> 'cancelled'
                          AND z.created_at < u.t_ref AND z.created_at >= u.t_ref - INTERVAL 180 DAY)) zam_180_przed,
                     avg((SELECT count(*) FROM zam z WHERE z.user_id = u.user_id AND z.status <> 'cancelled'
                          AND z.created_at > u.t_ref AND z.created_at <= u.t_ref + INTERVAL 180 DAY)) zam_180_po,
                     avg((SELECT count(*) FROM zam z WHERE z.user_id = u.user_id AND z.status <> 'cancelled' AND z.created_at < u.t_ref)) zam_wczesniej_razem
              FROM (SELECT u.*, CASE WHEN u.kupil = 0 AND EXISTS (SELECT 1 FROM go g WHERE g.user_id = u.user_id
                                             AND g.purchased_at > u.t_ref AND g.purchased_at <= u.t_ref + INTERVAL 180 DAY)
                                     THEN 1 ELSE 0 END kupil_pozniej FROM upsell u) u
              WHERE u.t_ref::DATE <= DATE '{KONIEC}' - INTERVAL 180 DAY
              GROUP BY GROUPING SETS ((kupil), (kupil, kupil_pozniej)) ORDER BY 1""")
    u = u[u.pacjenci > 0]
    u["kupil"] = u.kupil.astype(int)
    # wiersze: (kupil) — cała grupa; (kupil, kupil_pozniej) z kupil=0 i kupil_pozniej=0 — bez późniejszych kupujących
    gl = u[u.kupil_pozniej.isna()].drop(columns="kupil_pozniej")
    wr = u[(u.kupil == 0) & (u.kupil_pozniej == 0)].drop(columns="kupil_pozniej").assign(kupil=-1)
    u = pd.concat([gl, wr], ignore_index=True)
    u["zmiana_po_minus_przed"] = u.zam_180_po - u.zam_180_przed
    pokaz(u.round(3))
    poz = q(f"""SELECT count(*) FILTER (WHERE kupil = 0) bez_zakupu,
                       count(*) FILTER (WHERE kupil = 0 AND EXISTS (SELECT 1 FROM go g WHERE g.user_id = u.user_id
                                         AND g.purchased_at > u.t_ref AND g.purchased_at <= u.t_ref + INTERVAL 180 DAY)) kupili_pozniej
                FROM upsell u WHERE u.t_ref::DATE <= DATE '{KONIEC}' - INTERVAL 180 DAY""")
    r(f"     W grupie bez zakupu {int(poz.kupili_pozniej[0])} z {int(poz.bez_zakupu[0])} pacjentów kupuje członkostwo później w oknie 180 dni.")
    zm = u.set_index("kupil").zmiana_po_minus_przed
    if 1 in zm.index and 0 in zm.index:
        r(f"     Różnica różnic (kupili − bez zakupu przy wejściu i przez 30 dni): {zm[1] - zm[0]:+.3f} zamówienia na pacjenta w 180 dniach;"
          f" bez późniejszych kupujących: {zm[1] - zm[-1]:+.3f}.")
    r("     To statystyka opisowa: zakłada równoległe trendy obu grup. Decyzja o zakupie może sama wynikać z planowanej")
    r("     wizyty, grupa bez zakupu jest mała, a to nie jest grupa kontrolna z losowania. Lepsze porównanie na tych danych:")
    r("     dopasowanie przy wejściu według miesiąca, stażu, czasu od ostatniej konsultacji i wcześniejszych zamówień.")

    r("\n4d. Test, który to rozstrzygnie. Dwa projekty, wielkość próby przy istotności 5% i mocy 80%, okno 90 dni, liczby z")
    r("    okresu 2. (A) Losowa oferta: połowa nowych pacjentów widzi ofertę TelemediGO przy kasie, połowa nie; porównujemy")
    r("    wszystkich pacjentów z obu połówek, także tych, którzy nie kupili, więc efekt rozcieńcza mały odsetek kupujących.")
    r("    Losowanie przed zakupem; oferta może też zmienić samą pierwszą płatność, więc ją też porównujemy.")
    r("    (B) Losowe członkostwo próbne: połowa nowych pacjentów dostaje bezpłatny dostęp do zniżek TelemediGO na 90 dni,")
    r("    od dnia po pierwszym zamówieniu; mierzy wpływ niższej ceny, bez samoselekcji. Nie rozstrzyga sam rentowności")
    r("    płatnego programu za 89 zł (recenzja Codeksa). Koszt testu (B) = zniżki udzielone grupie próbnej.")
    r("    Różnice z 4a służą tylko jako scenariusze efektu, nie jako oszacowanie oczekiwanego wyniku testu.")
    r("    Wzór: dwie proporcje z osobnymi wariancjami grup, liczebność zaokrąglona w górę.")
    p2 = np2[(np2.okres == 2) & (np2.d0 <= kon - pd.Timedelta(days=90))]
    ods = p2.go1.mean()
    baza = (p2.dni_R2.astype("float64").fillna(1e9) <= 90).mean()
    efekt = w4[(w4.miara.str.startswith("powrót w 90")) & (w4.okresy == "2") & (w4.warstwy == "kanał+usługa+miesiąc")].roznica.iloc[0] / 100
    miesiecznie = len(np2[np2.okres == 2]) / 12
    for projekt, udzial in (("A", ods), ("B", 1.0)):
        for frac, opis in ((1.0, "cała różnica z 4a to wpływ ceny"), (0.5, "połowa"), (0.25, "jedna czwarta")):
            delta = udzial * efekt * frac
            p1_, p2_ = baza, baza + delta
            pm = (p1_ + p2_) / 2
            n_ram = math.ceil((1.959964 * math.sqrt(2 * pm * (1 - pm)) + 0.841621 * math.sqrt(p1_ * (1 - p1_) + p2_ * (1 - p2_))) ** 2
                              / delta ** 2) if delta > 0 else float("nan")
            r(f"     ({projekt}) {opis}: różnica między połówkami {100 * delta:.2f} punktu procentowego, potrzeba "
              f"{n_ram:,.0f} pacjentów na połówkę, czyli {2 * n_ram / miesiecznie:.1f} miesiąca pozyskania (+90 dni obserwacji)".replace(",", " "))
    r(f"     Założenia: odsetek kupujących przy pierwszym zamówieniu {100 * ods:.2f}%, powrót w 90 dniach {100 * baza:.1f}%,")
    r(f"     różnica z 4a (okres 2) {100 * efekt:.2f} punktu, {miesiecznie:.0f} nowych pacjentów miesięcznie. Przy tak małym")
    r("     odsetku kupujących projekt (A) jest niewykonalny w rozsądnym czasie. Projekt (B) wystarczy na kilka tygodni")
    r("     pozyskania, ale kosztuje zniżki. Wariant pośredni: losowa grupa bez newslettera crm_go_upsell wśród pacjentów")
    r("     po drugim zamówieniu (tam kupuje większy odsetek).")

    # ---------- 5. zestawienie miesięczne dla narzędzia ----------
    mies = q("""SELECT strftime(dzien, '%Y-%m') miesiac, typ, count(*) zakupy, 89.0 * count(*) oplaty_zl FROM go GROUP BY ALL ORDER BY 1, 2""")
    zn_m = q("""SELECT strftime(created_at, '%Y-%m') miesiac, sum(znizka_efektywna) znizka_efektywna_zl,
                       sum(przychod - koszt_lekarza) marza_wizyt_ze_znizka_zl, count(*) zamowienia_ze_znizka
                FROM go_zam GROUP BY 1 ORDER BY 1""")
    mies.to_csv(WYNIK_CSV, index=False)
    zn_m.to_csv(WYNIK_CSV.replace(".csv", "_znizki.csv"), index=False)
    r(f"\n(Zestawienia miesięczne: {os.path.relpath(WYNIK_CSV, D.KATALOG)} i {os.path.relpath(WYNIK_CSV.replace('.csv', '_znizki.csv'), D.KATALOG)})")

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Zapisano {WYNIK} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
