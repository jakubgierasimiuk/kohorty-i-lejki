"""Wspólny moduł przyjętych definicji (A4 → A5, 2026-10-19).

Kod przeniesiony z analiza/a4_definicje.py, tylko warianty przyjęte przez Kubę (notatki/ZALOZENIA.md, 16–27):
  - nowy pacjent = N1: pierwsze opłacone zamówienie konsultacji, dowolny status (tabela `koh`);
  - powrót = R2: kolejne zamówienie nieanulowane, okna 30/60/90 dni (tabela `powr`, kolumna `dni_R2`);
  - źródło = Z1K: pierwsze wejście z anonimowymi sesjami przeglądarek pacjenta, kod kampanii rozstrzyga;
    obok Z2 (sesja płatności) — tabele `ses_pac`, `sp`, `reg`, `zr` (długi format) i `zrodlo` (szeroki);
  - CRM: wejście z newslettera albo SMS-a, okno 24 godzin, tylko zamówienia nieanulowane, przy przypisaniu
    sprzedaży ostatnie wejście przed płatnością — tabele `kontakt`, `po_kontakcie_wszystkie`, `po_kontakcie`,
    `crm_rozl`;
  - porównanie okresów na tych samych dniach kalendarzowych: `stopy_por()`.

Wszystko powstaje jako tabele tymczasowe na podanym połączeniu (baza otwarta tylko do odczytu):

    import definicje as D
    con = D.polacz()
    D.zbuduj(con)            # albo po kolei: podstawy, kohorty, zrodla, crm

Moduł edytuje tylko sesja retencji A5 (notatki/PRZEKAZANIE.md). Pliku a4_definicje.py nie zmieniamy;
analiza/a5r_kontrola_definicji.py sprawdza, że ten moduł odtwarza co do sztuki sekcję 6 jego raportu.
"""

import datetime as dt
import os

import duckdb

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAZA = os.path.join(KATALOG, "analiza", "telemedi.duckdb")

KONIEC = "2026-09-30"   # ostatni dzień danych
OKRES2 = "2025-10-01"   # początek drugiego roku dashboardu (czas polski)
OKNA = (30, 60, 90)

KANAL = """
  CASE WHEN utm_source IS NULL THEN 'bezposrednie'
       WHEN utm_campaign = 'gs_brand' THEN 'google_ads_marka'
       WHEN utm_campaign LIKE 'gs_generic%' THEN 'google_ads_ogolne'
       WHEN utm_medium = 'organic' THEN 'wyszukiwarka_bezplatna'
       WHEN utm_campaign LIKE 'meta_prosp%' THEN 'meta_pozyskanie'
       WHEN utm_campaign = 'meta_rmkt_koszyk' THEN 'meta_remarketing'
       WHEN utm_source = 'tiktok' THEN 'tiktok'
       WHEN utm_medium = 'affiliate' THEN 'afiliacja_ranking'
       WHEN utm_medium = 'referral' THEN 'program_polecen'
       WHEN utm_medium IN ('email', 'sms') THEN 'crm'
       ELSE 'inne' END"""

# kod kampanii na pierwszym zamówieniu -> kanał i kampania, które kod wskazuje
KODY = {"L4SZYBKO20": ("meta_pozyskanie", "meta_prosp_l4_szybko"),
        "TIKTOK25": ("tiktok", "tt_prosp_l4_15min"),
        "RANKING10": ("afiliacja_ranking", "rankinglekarzy_affiliate")}


def polacz():
    """Połączenie z bazą tylko do odczytu (tabele tymczasowe działają)."""
    return duckdb.connect(BAZA, read_only=True)


def zbuduj_podstawy(con):
    """`zam` (zamówienia z numerem kolejnym pacjenta), `ses` (sesje z kanałem i kampanią),
    `przeg` (przeglądarka -> konto), `ses_pac` (sesje konta i anonimowe sesje jego przeglądarek)."""
    con.execute("""
      CREATE TEMP TABLE zam AS
      SELECT o.*, row_number() OVER (PARTITION BY user_id ORDER BY created_at, order_id) nr
      FROM czyste.orders o""")
    con.execute(f"""
      CREATE TEMP TABLE ses AS
      SELECT session_id, visitor_id, user_id, started_at_pl, started_at_utc, utm_source, utm_medium, utm_campaign, landing_page,
             {KANAL} kanal,
             coalesce(utm_campaign, utm_source || '_' || utm_medium, 'bezposrednie') kampania
      FROM czyste.sessions""")
    con.execute("CREATE TEMP TABLE przeg AS SELECT DISTINCT visitor_id, user_id FROM czyste.sessions WHERE user_id IS NOT NULL")
    con.execute("""
      CREATE TEMP TABLE ses_pac AS
      SELECT coalesce(s.user_id, p.user_id) pacjent, s.*, s.user_id IS NULL anonimowa
      FROM ses s LEFT JOIN przeg p ON p.visitor_id = s.visitor_id
      WHERE coalesce(s.user_id, p.user_id) IS NOT NULL""")


def zbuduj_kohorty(con):
    """`koh`: nowy pacjent N1 (t0 = moment płatności pierwszego zamówienia, d0 = dzień kohorty, okres 1 albo 2).
    `powr`: dni od d0 do pierwszego powrotu R2 (kolejne zamówienie nieanulowane); NULL = brak powrotu."""
    con.execute(f"""
      CREATE TEMP TABLE koh AS
      SELECT user_id, created_at t0, session_id, order_id, created_at::DATE d0,
             CASE WHEN created_at < TIMESTAMP '{OKRES2}' THEN 1 ELSE 2 END okres
      FROM zam WHERE nr = 1""")
    con.execute("""
      CREATE TEMP TABLE powr AS
      SELECT k.user_id, k.d0, k.okres, k.session_id,
             min(date_diff('day', k.d0, z.created_at::DATE)) FILTER (WHERE z.status <> 'cancelled') dni_R2
      FROM koh k LEFT JOIN zam z ON z.user_id = k.user_id AND z.created_at > k.t0
      GROUP BY ALL""")


def zbuduj_zrodla(con):
    """`sp`: sesje pacjenta do chwili pierwszej płatności; `reg`: reguły Z1 i Z2 na pacjenta;
    `zr`: długi format pacjent x reguła (Z1, Z2, Z1K) -> kanał, kampania;
    `zrodlo`: szeroki format, kanal/kampania według Z1K oraz kanal_z2/kampania_z2 według sesji płatności."""
    con.execute("""
      CREATE TEMP TABLE sp AS
      SELECT k.user_id, k.t0, k.okres, k.session_id sesja_platnosci, s.session_id, s.started_at_pl,
             s.kanal, s.kampania, s.anonimowa, s.landing_page
      FROM koh k JOIN ses_pac s ON s.pacjent = k.user_id AND s.started_at_pl <= k.t0""")
    con.execute("""
      CREATE TEMP TABLE reg AS
      SELECT user_id, okres, any_value(z.promo_code) kod,
             arg_min(kanal, (started_at_pl, session_id)) Z1_kanal, arg_min(kampania, (started_at_pl, session_id)) Z1_kampania,
             any_value(kanal) FILTER (WHERE session_id = sesja_platnosci) Z2_kanal,
             any_value(kampania) FILTER (WHERE session_id = sesja_platnosci) Z2_kampania,
             count(*) sesje_do_zakupu, count(*) FILTER (WHERE anonimowa) sesje_anonimowe
      FROM sp JOIN (SELECT user_id u, promo_code FROM zam WHERE nr = 1) z ON z.u = sp.user_id
      GROUP BY 1, 2""")
    przyp_k = " ".join(f"WHEN '{k}' THEN '{v[0]}'" for k, v in KODY.items())
    przyp_c = " ".join(f"WHEN '{k}' THEN '{v[1]}'" for k, v in KODY.items())
    con.execute(f"""
      CREATE TEMP TABLE zr AS
      SELECT user_id, okres, kod, 'Z1' regula, Z1_kanal kanal, Z1_kampania kampania FROM reg
      UNION ALL
      SELECT user_id, okres, kod, 'Z2' regula, Z2_kanal kanal, Z2_kampania kampania FROM reg
      UNION ALL
      SELECT user_id, okres, kod, 'Z1K' regula,
             coalesce(CASE kod {przyp_k} END, Z1_kanal) kanal,
             coalesce(CASE kod {przyp_c} END, Z1_kampania) kampania FROM reg""")
    con.execute("""
      CREATE TEMP TABLE zrodlo AS
      SELECT user_id, okres, kod,
             any_value(kanal) FILTER (WHERE regula = 'Z1K') kanal,
             any_value(kampania) FILTER (WHERE regula = 'Z1K') kampania,
             any_value(kanal) FILTER (WHERE regula = 'Z2') kanal_z2,
             any_value(kampania) FILTER (WHERE regula = 'Z2') kampania_z2
      FROM zr GROUP BY ALL""")


def zbuduj_crm(con, dni_obserwacji=61):
    """`kontakt`: każda sesja pacjenta (konto albo jego przeglądarka) z co najmniej `dni_obserwacji` dniami
    obserwacji po wejściu; kanał 'crm' = newsletter i SMS. `byl_pacjentem` = przed wejściem było zamówienie,
    `zalogowana` = zalogowana od wejścia (ZALOZENIA.md 10, wyjątek dla zakupu samego TelemediGO).
    `po_kontakcie_wszystkie`: zamówienia pacjenta w 61 dniach od wejścia, `dzien` liczony w UTC (0 = 24 godziny);
    `po_kontakcie`: to samo bez anulowanych (ZALOZENIA.md 26).
    `crm_rozl`: każde nieanulowane zamówienie do 24 godzin od wejścia z CRM przypisane tylko do ostatniego
    wejścia z CRM przed płatnością (pacjenci po pierwszym zakupie).
    A4 liczył z dni_obserwacji = 61 (tło w dniach 31–60); do samego okna 24 godzin wystarczy 1."""
    con.execute("""
      CREATE TEMP TABLE logow AS SELECT DISTINCT session_id FROM czyste.events WHERE event_name = 'account_completed'""")
    con.execute(f"""
      CREATE TEMP TABLE kontakt AS
      SELECT s.pacjent, s.session_id, s.started_at_pl ts, timezone('UTC', s.started_at_utc) ts_utc, s.kampania, s.kanal,
             EXISTS (SELECT 1 FROM zam z WHERE z.user_id = s.pacjent AND z.created_at < s.started_at_pl) byl_pacjentem,
             s.user_id IS NOT NULL AND s.session_id NOT IN (SELECT session_id FROM logow)
               AND s.session_id NOT IN (SELECT session_id FROM czyste.go_memberships WHERE order_id IS NULL) zalogowana
      FROM ses_pac s
      WHERE timezone('UTC', s.started_at_utc) + INTERVAL {int(dni_obserwacji)} DAY
            <= timezone('Europe/Warsaw', TIMESTAMP '2026-10-01 00:00:00')""")
    con.execute("""
      CREATE TEMP TABLE po_kontakcie_wszystkie AS
      SELECT k.session_id, k.kampania, k.kanal, k.byl_pacjentem, k.zalogowana, k.ts_utc, o.order_id, o.status,
             o.session_id = k.session_id w_sesji,
             floor((epoch(timezone('Europe/Warsaw', o.created_at)) - epoch(k.ts_utc)) / 86400)::INT dzien
      FROM kontakt k JOIN zam o ON o.user_id = k.pacjent AND timezone('Europe/Warsaw', o.created_at) >= k.ts_utc
                                AND timezone('Europe/Warsaw', o.created_at) < k.ts_utc + INTERVAL 61 DAY""")
    con.execute("CREATE TEMP TABLE po_kontakcie AS SELECT * FROM po_kontakcie_wszystkie WHERE status <> 'cancelled'")
    con.execute("""
      CREATE TEMP TABLE crm_rozl AS
      SELECT order_id, arg_max(kampania, ts_utc) kampania, arg_max(session_id, ts_utc) wejscie
      FROM po_kontakcie WHERE kanal = 'crm' AND byl_pacjentem AND dzien = 0 GROUP BY 1""")


# Koszt lekarza za wizytę, która się odbyła (completed i refunded, także zwróconą), zł — zasada z zadania.
# Pediatra liczy się jak „inny specjalista” (100 zł), bo TelemediGO daje mu zniżkę 20% jak specjalistom,
# a nie 50% jak interniście (propozycja założenia 28, notatki/a5_retencja.md).
KOSZT_LEKARZA = """
  CASE WHEN status IN ('completed', 'refunded')
       THEN CASE specialization WHEN 'internista' THEN 25 WHEN 'psychiatra' THEN 200 ELSE 100 END
       ELSE 0 END"""


def zbuduj_ekonomie(con):
    """`ek`: zdarzenia pieniężne pacjenta (zamówienie konsultacji albo osobny zakup TelemediGO) z dniem od wejścia
    do kohorty. Przychód z konsultacji po zwrotach (ZALOZENIA.md 21), TelemediGO osobno (89 zł, także kupione
    przy kasie), koszt lekarza według KOSZT_LEKARZA. marza = przychod + go - koszt_lekarza, przed kosztem
    pozyskania (kampanie, prowizja). `nieanul` = zamówienie nieanulowane, `pierwsze` = pierwsze zamówienie."""
    con.execute(f"""
      CREATE TEMP TABLE ek AS
      WITH z AS (
        SELECT user_id, created_at t, order_id, nr, status, specialization, visit_purpose,
               (amount_paid - refund_amount)::DOUBLE przychod, 0.0 go, ({KOSZT_LEKARZA})::DOUBLE koszt_lekarza,
               status <> 'cancelled' nieanul, nr = 1 pierwsze, TRUE zamowienie
        FROM zam
        UNION ALL
        SELECT user_id, purchased_at, order_id, NULL, NULL, NULL, NULL, 0.0, amount_paid::DOUBLE, 0.0, FALSE, FALSE, FALSE
        FROM czyste.go_memberships)
      SELECT z.*, k.d0, k.okres, date_diff('day', k.d0, z.t::DATE) dni, z.przychod + z.go - z.koszt_lekarza marza
      FROM z JOIN koh k USING (user_id)""")


def zbuduj(con, crm=True, dni_obserwacji=61, ekonomia=True):
    """Wszystkie tabele przyjętych definicji naraz."""
    zbuduj_podstawy(con)
    zbuduj_kohorty(con)
    zbuduj_zrodla(con)
    if crm:
        zbuduj_crm(con, dni_obserwacji)
    if ekonomia:
        zbuduj_ekonomie(con)


def granice_por(n):
    """Ostatni dzień kohorty z pełnym oknem n dni w okresie 2 i ten sam dzień roku w okresie 1 (ZALOZENIA.md 27)."""
    g2 = dt.date.fromisoformat(KONIEC) - dt.timedelta(days=n)
    return g2.replace(year=g2.year - 1), g2


def stopy(grupa=None, warunek="TRUE", tabela="powr"):
    """SQL: odsetek kohorty z powrotem R2 w 30/60/90 dniach, okres 1 i 2, wszystkie kohorty z pełnym oknem
    (okres 1 w całości). Do porównania okresów używamy stopy_por()."""
    g = f"{grupa}, " if grupa else ""
    kol = []
    for n in OKNA:
        for o in (1, 2):
            kol.append(f"""round(100.0 * count(*) FILTER (WHERE okres = {o} AND d0 <= DATE '{KONIEC}' - {n}
                                 AND dni_R2 <= {n})
                            / nullif(count(*) FILTER (WHERE okres = {o} AND d0 <= DATE '{KONIEC}' - {n}), 0), 1) p{n}_o{o}""")
    return f"SELECT {g}{', '.join(kol)} FROM {tabela} WHERE {warunek} {'GROUP BY ' + grupa if grupa else ''}"


def stopy_por(grupa=None, warunek="TRUE", tabela="powr", okna=OKNA, zaokr=1):
    """SQL: powrót R2 w oknach `okna`, okres 1 obcięty do tych samych dni kalendarzowych co dojrzała część
    okresu 2 (ZALOZENIA.md 27). Kolumny p{n}_o1, p{n}_o2 (%) i n{n}_o1, n{n}_o2 (liczba pacjentów).
    `tabela` musi mieć kolumny d0, okres, dni_R2 (np. powr albo powr połączone z podziałem)."""
    g = f"{grupa}, " if grupa else ""
    kol = []
    for n in okna:
        g1, g2 = granice_por(n)
        w1 = f"okres = 1 AND d0 <= DATE '{g1}'"
        w2 = f"okres = 2 AND d0 <= DATE '{g2}'"
        kol += [f"round(100.0 * count(*) FILTER (WHERE {w1} AND dni_R2 <= {n}) / nullif(count(*) FILTER (WHERE {w1}), 0), {zaokr}) p{n}_o1",
                f"round(100.0 * count(*) FILTER (WHERE {w2} AND dni_R2 <= {n}) / nullif(count(*) FILTER (WHERE {w2}), 0), {zaokr}) p{n}_o2",
                f"count(*) FILTER (WHERE {w1}) n{n}_o1", f"count(*) FILTER (WHERE {w2}) n{n}_o2"]
    return f"SELECT {g}{', '.join(kol)} FROM {tabela} WHERE {warunek} {'GROUP BY ' + grupa if grupa else ''}"
