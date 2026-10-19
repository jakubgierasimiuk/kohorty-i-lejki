"""A2 — jakość danych: raport, każda tabela osobno.

Tylko czyta bazę analiza/telemedi.duckdb (budowaną przez analiza/a1_baza.py). Niczego nie usuwa ani nie poprawia:
decyzje o czyszczeniu podejmujemy razem po przeglądzie tego raportu.

Sekcje:
  1. Duplikaty w każdej tabeli i kiedy występują
  2. Zamówienia testowe (kod TEST-QA i pozostałe zamówienia tych samych kont)
  3. Kliknięcia z marketing_spend wobec sesji z tych samych kampanii, dzień po dniu
  4. Moment płatności w systemie transakcyjnym wobec kroku płatności w analityce (test strefy czasowej)
  5. Pozostałe kontrole spójności i realności

Uruchomienie z głównego folderu projektu:
    python -I analiza/a2_jakosc.py
Wynik: ekran + analiza/wyniki/a2_jakosc.txt
"""

import datetime as dt
import os

import duckdb
import pandas as pd

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAZA = os.path.join(KATALOG, "analiza", "telemedi.duckdb")
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "a2_jakosc.txt")
OKRES2 = "2025-10-01"  # początek ostatnich 12 miesięcy z dashboardu (X 2025 – IX 2026)

pd.set_option("display.width", 200)

# Widoki pomocnicze (tymczasowe, w pamięci — baza zostaje nietknięta)
WIDOKI = f"""
-- zamówienia unikalne: duplikaty są identyczne w całości (sekcja 1), więc wystarcza DISTINCT
CREATE TEMP VIEW zam AS SELECT DISTINCT * EXCLUDE (wiersz_w_pliku) FROM surowe.orders;
-- konta testowe: każde konto, które choć raz użyło kodu TEST-QA
CREATE TEMP VIEW konta_testowe AS SELECT DISTINCT user_id FROM surowe.orders WHERE promo_code = 'TEST-QA';
CREATE TEMP VIEW platnosci AS
  SELECT session_id, count(*) n, min(event_at_pl) t_pl, min(event_at_utc) t_utc
  FROM surowe.events WHERE event_name = 'payment_succeeded' GROUP BY 1;
CREATE TEMP VIEW kroki AS
  SELECT session_id,
    max((event_name = 'service_selected')::INT)  k1, max((event_name = 'slot_selected')::INT)   k2,
    max((event_name = 'account_completed')::INT) k3, max((event_name = 'payment_started')::INT) k4,
    max((event_name = 'payment_succeeded')::INT) k5,
    min(event_at_utc) FILTER (WHERE event_name = 'service_selected')  t1,
    min(event_at_utc) FILTER (WHERE event_name = 'slot_selected')     t2,
    min(event_at_utc) FILTER (WHERE event_name = 'account_completed') t3,
    min(event_at_utc) FILTER (WHERE event_name = 'payment_started')   t4,
    min(event_at_utc) FILTER (WHERE event_name = 'payment_succeeded') t5
  FROM surowe.events GROUP BY 1;
"""


def main():
    con = duckdb.connect(BAZA, read_only=True)
    for polecenie in [p for p in WIDOKI.split(";") if p.strip()]:
        con.execute(polecenie)
    linie = []

    def r(tekst=""):
        print(tekst)
        linie.append(tekst)

    def tab(sql, wciecie="     "):
        df = con.sql(sql).df()
        for linia in df.to_string(index=False).splitlines():
            r(wciecie + linia)
        return df

    def jedna(sql):
        return con.execute(sql).fetchone()

    r(f"A2 — JAKOŚĆ DANYCH ({dt.datetime.now():%Y-%m-%d %H:%M})")
    r("Baza: analiza/telemedi.duckdb (schemat `surowe`, dane bez czyszczenia). Czas polski, chyba że napisano UTC.")
    r(f"Okresy dashboardu: rok 1 = X 2024 – IX 2025, rok 2 = X 2025 – IX 2026 (od {OKRES2}).")

    # =====================================================================================
    r("\n" + "=" * 100 + "\n1. DUPLIKATY\n" + "=" * 100)
    r("\n1a. Każda tabela: wiersze, wiersze unikalne w całości, unikalne identyfikatory")
    tab("""
      SELECT 'users' tabela, 'user_id' identyfikator, count(*) wiersze,
             count(DISTINCT (user_id, registered_at, birth_year, gender, region, city_size, marketing_consent)) unikalne_w_calosci,
             count(DISTINCT user_id) unikalne_id FROM surowe.users
      UNION ALL SELECT 'sessions', 'session_id', count(*),
             count(DISTINCT (session_id, visitor_id, user_id, started_at_utc, utm_source, utm_medium, utm_campaign,
                             device, os, browser, landing_page)), count(DISTINCT session_id) FROM surowe.sessions
      UNION ALL SELECT 'events', 'session_id + event_name', count(*),
             count(DISTINCT (session_id, event_name, event_at_utc)), count(DISTINCT (session_id, event_name)) FROM surowe.events
      UNION ALL SELECT 'orders', 'order_id', count(*),
             count(DISTINCT (order_id, user_id, session_id, created_at, specialization, visit_purpose, consultation_mode,
                             scheduled_at, started_at, duration_min, list_price, discount_type, promo_code, amount_paid,
                             payment_method, status, refund_amount, rating)), count(DISTINCT order_id) FROM surowe.orders
      UNION ALL SELECT 'go_memberships', 'membership_id', count(*),
             count(DISTINCT (membership_id, user_id, purchased_at, valid_until, amount_paid, order_id, session_id)),
             count(DISTINCT membership_id) FROM surowe.go_memberships
      UNION ALL SELECT 'marketing_spend', 'date + utm (3 pola)', count(*),
             count(DISTINCT (date, utm_source, utm_medium, utm_campaign, impressions, clicks, spend_pln)),
             count(DISTINCT (date, utm_source, utm_medium, utm_campaign)) FROM surowe.marketing_spend""")
    r("   Gdy 'unikalne_w_calosci' = 'unikalne_id', ten sam identyfikator nigdy nie ma dwóch różnych treści.")
    r("   Duplikaty są tylko w orders. W pozostałych tabelach nie ma ani jednego, także na stykach plików.")

    r("\n1b. Styki plików kwartalnych i półrocznych (zakres czasu UTC w każdym pliku)")
    tab("""
      SELECT plik, count(*) wiersze, min(started_at_utc) pierwszy_utc, max(started_at_utc) ostatni_utc
      FROM surowe.sessions GROUP BY 1
      UNION ALL
      SELECT plik, count(*), min(event_at_utc), max(event_at_utc) FROM surowe.events GROUP BY 1 ORDER BY 1""")
    r("   Pliki są pocięte według północy czasu polskiego (np. ostatnia sesja IV kwartału 2024: 22:55 UTC = 23:55 w Polsce).")
    r("   Na stykach nie ma ani zdublowanych, ani zgubionych godzin: każdy plik zaczyna się tuż po końcu poprzedniego.")

    r("\n1c. Duplikaty zamówień: ile kopii i gdzie w pliku")
    tab("""
      WITH d AS (SELECT order_id, count(*) kopie, max(wiersz_w_pliku) - min(wiersz_w_pliku) odstep
                 FROM surowe.orders GROUP BY 1 HAVING count(*) > 1)
      SELECT kopie, odstep odstep_linii_miedzy_kopiami, count(*) zamowienia FROM d GROUP BY ALL""")
    r("   Każde zdublowane zamówienie ma dokładnie dwie kopie, w dwóch sąsiednich liniach pliku.")

    r("\n1d. Duplikaty zamówień w czasie")
    pierwszy, ostatni, przed, po = jedna("""
      WITH u AS (SELECT order_id, count(*) k, any_value(created_at) c FROM surowe.orders GROUP BY 1)
      SELECT min(c) FILTER (WHERE k > 1), max(c) FILTER (WHERE k > 1),
             max(c) FILTER (WHERE c < (SELECT min(c) FROM u WHERE k > 1)),
             min(c) FILTER (WHERE c > (SELECT max(c) FROM u WHERE k > 1)) FROM u""")
    r(f"   Pierwszy zdublowany: {pierwszy}, ostatni zdublowany: {ostatni}.")
    r(f"   Ostatnie zamówienie przed oknem: {przed}, pierwsze po oknie: {po} — oba bez duplikatu.")
    tab("""
      WITH u AS (SELECT order_id, count(*) k, any_value(created_at) c FROM surowe.orders GROUP BY 1)
      SELECT CAST(c AS DATE) dzien, count(*) zamowienia_unikalne, count(*) FILTER (WHERE k > 1) zdublowane,
             round(100.0 * count(*) FILTER (WHERE k > 1) / count(*), 1) proc_zdublowanych
      FROM u WHERE c >= DATE '2026-06-08' AND c < DATE '2026-06-27' GROUP BY 1 ORDER BY 1""")
    r("   Udział zdublowanych wobec cech zamówienia w oknie 10–24.06.2026 (podobny = duplikacja przypadkowa):")
    tab("""
      WITH u AS (SELECT order_id, count(*) k, any_value(payment_method) metoda, any_value(status) status,
                        any_value(discount_type) znizka
                 FROM surowe.orders WHERE created_at >= DATE '2026-06-10' AND created_at < DATE '2026-06-25' GROUP BY 1)
      SELECT 'metoda platnosci' cecha, metoda wartosc, count(*) zamowienia,
             round(100.0 * count(*) FILTER (WHERE k > 1) / count(*), 1) proc_zdublowanych FROM u GROUP BY 1, 2
      UNION ALL SELECT 'status', status, count(*), round(100.0 * count(*) FILTER (WHERE k > 1) / count(*), 1) FROM u GROUP BY 1, 2
      UNION ALL SELECT 'znizka', znizka, count(*), round(100.0 * count(*) FILTER (WHERE k > 1) / count(*), 1) FROM u GROUP BY 1, 2
      ORDER BY 1, 2""")
    r("   Skala w okresach dashboardu (dodatkowe kopie = wiersze ponad zamówienia unikalne):")
    tab(f"""
      WITH kopie AS (SELECT order_id, any_value(created_at) c, any_value(amount_paid) zapl,
                            any_value(refund_amount) zwrot, count(*) - 1 nadmiar
                     FROM surowe.orders GROUP BY 1)
      SELECT CASE WHEN c < DATE '{OKRES2}' THEN 'rok 1' ELSE 'rok 2' END okres,
             sum(nadmiar + 1)::BIGINT wiersze_surowe, count(*) zamowienia_unikalne, sum(nadmiar)::BIGINT dodatkowe_kopie,
             sum(nadmiar * zapl) zaplata_w_kopiach_zl, sum(nadmiar * (zapl - zwrot)) zaplata_po_zwrotach_w_kopiach_zl
      FROM kopie GROUP BY 1 ORDER BY 1""")

    # =====================================================================================
    r("\n" + "=" * 100 + "\n2. ZAMÓWIENIA TESTOWE\n" + "=" * 100)
    n_wiersze, n_unik, n_konta = jedna("""
      SELECT (SELECT count(*) FROM surowe.orders WHERE promo_code = 'TEST-QA'),
             (SELECT count(*) FROM zam WHERE promo_code = 'TEST-QA'), (SELECT count(*) FROM konta_testowe)""")
    r(f"\n2a. Kod TEST-QA: {n_wiersze:,} wierszy surowych, {n_unik:,} zamówień unikalnych (reszta to duplikaty "
      f"z sekcji 1), {n_konta} konta.")
    r("   Wszystkie zamówienia kont testowych (z kodem i bez):")
    tab("""
      SELECT coalesce(promo_code, '(bez kodu)') kod, status, specialization, consultation_mode, count(*) zamowienia,
             min(list_price) cena_kat, min(amount_paid) zaplata_min, max(amount_paid) zaplata_max,
             max(refund_amount) zwrot_max, min(duration_min) czas_min, max(duration_min) czas_max, count(rating) z_ocena
      FROM zam WHERE user_id IN (SELECT user_id FROM konta_testowe) GROUP BY ALL ORDER BY 5 DESC""")
    r("   Kontrola podpisu: czas wizyty 1 minuta wobec kont testowych w całych danych:")
    tab("""
      SELECT (user_id IN (SELECT user_id FROM konta_testowe)) konto_testowe, duration_min, count(*) zamowienia
      FROM zam WHERE duration_min <= 3 GROUP BY ALL ORDER BY ALL""")
    r("   Czas trwania 1 minuta występuje tylko u kont testowych. Najkrótsza wizyta u pozostałych pacjentów trwa 3 minuty.")
    r("   Zatem zbiór 'konta, które użyły TEST-QA' i zbiór 'zamówienia trwające 1 minutę' to to samo.")

    r("\n2b. Konta testowe w tabeli users")
    tab("""
      SELECT region, city_size, marketing_consent, count(*) konta, min(birth_year) rocznik_od, max(birth_year) rocznik_do,
             min(registered_at)::DATE pierwsze_konto, max(registered_at)::DATE ostatnie_konto
      FROM surowe.users WHERE user_id IN (SELECT user_id FROM konta_testowe) GROUP BY ALL""")

    r("\n2c. Kiedy składane (dzień tygodnia i godzina, czas polski)")
    tab("""
      SELECT CASE dayofweek(created_at) WHEN 0 THEN '7 niedziela' WHEN 1 THEN '1 poniedzialek' WHEN 2 THEN '2 wtorek'
             WHEN 3 THEN '3 sroda' WHEN 4 THEN '4 czwartek' WHEN 5 THEN '5 piatek' ELSE '6 sobota' END dzien_tygodnia,
             count(*) zamowienia, min(hour(created_at)) godzina_od, max(hour(created_at)) godzina_do
      FROM zam WHERE user_id IN (SELECT user_id FROM konta_testowe) GROUP BY 1 ORDER BY 1""")
    r("   Liczba zamówień testowych w kwartałach:")
    tab("""
      SELECT strftime(date_trunc('quarter', created_at), '%Y-%m') kwartal_od,
             count(*) FILTER (WHERE user_id IN (SELECT user_id FROM konta_testowe)) zamowienia_testowe,
             count(*) wszystkie_unikalne
      FROM zam GROUP BY 1 ORDER BY 1""")
    tab(f"""
      SELECT CASE WHEN created_at < DATE '{OKRES2}' THEN 'rok 1' ELSE 'rok 2' END okres, count(*) zamowienia_unikalne,
             count(*) FILTER (WHERE user_id IN (SELECT user_id FROM konta_testowe)) testowe,
             count(DISTINCT user_id) FILTER (WHERE user_id IN (SELECT user_id FROM konta_testowe)) konta_testowe_aktywne
      FROM zam GROUP BY 1 ORDER BY 1""")

    r("\n2d. Ślad w analityce")
    tab("""
      SELECT count(*) sesje_kont_testowych, count(DISTINCT visitor_id) przegladarki,
             count(*) FILTER (WHERE session_id IN (SELECT session_id FROM zam)) z_zamowieniem,
             count(*) FILTER (WHERE session_id NOT IN (SELECT session_id FROM zam)) bez_zamowienia
      FROM surowe.sessions WHERE user_id IN (SELECT user_id FROM konta_testowe)""")
    tab("""
      SELECT coalesce(utm_source, '(bezposrednie)') zrodlo, device, browser, landing_page, count(*) sesje
      FROM surowe.sessions WHERE user_id IN (SELECT user_id FROM konta_testowe) GROUP BY ALL""")
    tab("""
      SELECT k.k1 || k.k2 || k.k3 || k.k4 || k.k5 kroki_12345, count(*) sesje
      FROM surowe.sessions s JOIN kroki k USING (session_id)
      WHERE s.user_id IN (SELECT user_id FROM konta_testowe) GROUP BY 1""")
    r("   Kroki: 1 wybór usługi, 2 wybór terminu, 3 logowanie lub konto, 4 wejście na płatność, 5 płatność przyjęta.")
    r("   Sesje bez zamówienia (po jednej na konto) to sesje założenia konta. Konta testowe nie mają TelemediGO: "
      f"{jedna('SELECT count(*) FROM surowe.go_memberships WHERE user_id IN (SELECT user_id FROM konta_testowe)')[0]} zakupów.")

    r("\n2e. Pieniądze w zamówieniach testowych")
    tab("""
      SELECT count(*) zamowienia, sum(amount_paid) zaplata_zl, sum(refund_amount) zwroty_zl,
             sum(amount_paid - refund_amount) przychod_po_zwrotach_zl,
             count(*) FILTER (WHERE status IN ('completed', 'refunded')) wizyty_odbyte,
             25 * count(*) FILTER (WHERE status IN ('completed', 'refunded')) koszt_lekarza_wg_zasady_zl
      FROM zam WHERE user_id IN (SELECT user_id FROM konta_testowe)""")
    r("   Koszt lekarza według zasady z zadania: 25 zł za odbytą wizytę u internisty, także zwróconą.")
    r("   Czy lekarz naprawdę dostał wynagrodzenie za wizytę testową trwającą 1 minutę, z danych nie wiemy.")

    # =====================================================================================
    r("\n" + "=" * 100 + "\n3. KLIKNIĘCIA (marketing_spend) WOBEC SESJI\n" + "=" * 100)
    r("\n3a. Źródła wejścia w sesjach")
    tab("""
      SELECT coalesce(utm_source, '(brak)') utm_source, coalesce(utm_medium, '(brak)') utm_medium,
             coalesce(utm_campaign, '(brak)') utm_campaign, count(*) sesje, min(dzien_pl) pierwszy_dzien, max(dzien_pl) ostatni_dzien
      FROM surowe.sessions GROUP BY ALL ORDER BY 1, 2, 3""")
    r("   Bing ma utm_medium = organic (bezpłatne wyniki wyszukiwania), tak jak google/organic. Brak kosztu jest zgodny z oznaczeniem.")
    r("\n3b. Kampanie w marketing_spend")
    tab("""
      SELECT utm_source, utm_medium, utm_campaign, count(*) dni, sum(impressions)::BIGINT wyswietlenia, sum(clicks)::BIGINT klikniecia,
             sum(spend_pln) koszt_zl, min(date) pierwszy_dzien, max(date) ostatni_dzien
      FROM surowe.marketing_spend GROUP BY ALL ORDER BY 1, 3""")
    con.execute("""
      CREATE TEMP TABLE klik_sesje AS
      SELECT coalesce(m.date, s.dzien_pl) dzien, coalesce(m.utm_campaign, s.utm_campaign) kampania, m.clicks klikniecia,
             coalesce(s.sesje, 0) sesje
      FROM surowe.marketing_spend m
      FULL JOIN (SELECT dzien_pl, utm_source, utm_medium, utm_campaign, count(*) sesje FROM surowe.sessions
                 WHERE utm_medium IN ('cpc', 'paid_social') GROUP BY ALL) s
        ON s.dzien_pl = m.date AND s.utm_source = m.utm_source AND s.utm_medium = m.utm_medium
       AND s.utm_campaign = m.utm_campaign""")
    bez_kosztu, bez_sesji = jedna("""
      SELECT count(*) FILTER (WHERE klikniecia IS NULL), count(*) FILTER (WHERE sesje = 0) FROM klik_sesje""")
    r(f"\n3c. Dzień × kampania: {bez_kosztu} par z sesjami płatnymi bez wiersza kosztu, {bez_sesji} par z kosztem bez sesji.")
    r("   Sesje na kliknięcie: cały okres oraz najniższy i najwyższy kwartał")
    tab("""
      WITH kw AS (SELECT kampania, date_trunc('quarter', dzien) k, sum(sesje) / sum(klikniecia) wsk FROM klik_sesje GROUP BY 1, 2)
      SELECT c.kampania, sum(c.klikniecia)::BIGINT klikniecia, sum(c.sesje)::BIGINT sesje, round(sum(c.sesje) / sum(c.klikniecia), 3) sesje_na_klik,
             (SELECT round(min(wsk), 3) FROM kw WHERE kw.kampania = c.kampania) kwartal_min,
             (SELECT round(max(wsk), 3) FROM kw WHERE kw.kampania = c.kampania) kwartal_max
      FROM klik_sesje c GROUP BY 1 ORDER BY 4 DESC""")
    r("   Największe odchylenia pojedynczego dnia od średniej kampanii (w odchyleniach standardowych rozkładu dwumianowego):")
    tab("""
      WITH k AS (SELECT kampania, sum(sesje) / sum(klikniecia) p FROM klik_sesje GROUP BY 1)
      SELECT c.dzien, c.kampania, c.klikniecia, c.sesje, round(k.p * c.klikniecia, 1) oczekiwane,
             round((c.sesje - k.p * c.klikniecia) / sqrt(c.klikniecia * k.p * (1 - k.p)), 1) odchylenie
      FROM klik_sesje c JOIN k USING (kampania) ORDER BY abs(odchylenie) DESC LIMIT 5""")
    r(f"   Przy {jedna('SELECT count(*) FROM klik_sesje')[0]:,} parach dzień × kampania odchylenie ok. 3,5–4 to zwykły szum losowy.")
    r("   Wniosek kontroli: nie ma dni z utratą śledzenia kampanii płatnych.")

    # =====================================================================================
    r("\n" + "=" * 100 + "\n4. MOMENT PŁATNOŚCI: SYSTEM TRANSAKCYJNY WOBEC ANALITYKI\n" + "=" * 100)
    r(f"\n   Najwięcej kroków payment_succeeded w jednej sesji: {jedna('SELECT max(n) FROM platnosci')[0]}.")
    r("4a. orders.created_at wobec payment_succeeded tej samej sesji, przeliczonego na czas polski (różnica w sekundach)")
    tab("""
      SELECT date_diff('second', p.t_pl, z.created_at) roznica_s, count(*) zamowienia
      FROM zam z JOIN platnosci p USING (session_id) GROUP BY 1 ORDER BY 2 DESC""")
    r("   Ta sama różnica wobec czasu UTC (w godzinach): przesunięcie zimowe i letnie")
    tab("""
      SELECT date_diff('second', p.t_utc, z.created_at) / 3600 roznica_h, count(*) zamowienia,
             min(z.created_at) od_chwili, max(z.created_at) do_chwili
      FROM zam z JOIN platnosci p USING (session_id) GROUP BY 1 ORDER BY 1""")
    r("4b. go_memberships.purchased_at wobec payment_succeeded tej samej sesji")
    tab("""
      SELECT (g.order_id IS NULL) kupione_osobno, count(*) zakupy, count(p.session_id) z_krokiem_platnosci,
             count(*) FILTER (WHERE g.purchased_at = p.t_pl) czas_identyczny
      FROM surowe.go_memberships g LEFT JOIN platnosci p USING (session_id) GROUP BY 1""")
    r("   Wniosek kontroli: system transakcyjny zapisuje czas polski i poprawnie obsługuje zmianę czasu.")

    # =====================================================================================
    r("\n" + "=" * 100 + "\n5. POZOSTAŁE KONTROLE\n" + "=" * 100)
    r("\n5a. Powiązania między tabelami")
    tab("""
      SELECT 'zamowienia unikalne' co, count(*) wszystkie, count(s.session_id) z_istniejaca_sesja,
             count(*) FILTER (WHERE s.user_id = z.user_id) sesja_tego_samego_konta,
             count(*) FILTER (WHERE z.user_id IN (SELECT user_id FROM surowe.users)) konto_istnieje
      FROM zam z LEFT JOIN surowe.sessions s USING (session_id)
      UNION ALL
      SELECT 'zakupy TelemediGO', count(*), count(s.session_id), count(*) FILTER (WHERE s.user_id = g.user_id),
             count(*) FILTER (WHERE g.user_id IN (SELECT user_id FROM surowe.users))
      FROM surowe.go_memberships g LEFT JOIN surowe.sessions s USING (session_id)
      UNION ALL
      SELECT 'zdarzenia lejka', count(*), count(s.session_id), NULL, NULL
      FROM surowe.events e LEFT JOIN surowe.sessions s USING (session_id)""")
    tab("""
      SELECT count(*) kroki_payment_succeeded,
             count(*) FILTER (WHERE session_id IN (SELECT session_id FROM zam)) z_zamowieniem,
             count(*) FILTER (WHERE session_id IN (SELECT session_id FROM surowe.go_memberships WHERE order_id IS NULL)) samo_telemedigo,
             count(*) FILTER (WHERE session_id NOT IN (SELECT session_id FROM zam)
                               AND session_id NOT IN (SELECT session_id FROM surowe.go_memberships)) bez_pokrycia
      FROM platnosci""")
    tab("""
      SELECT count(*) sesje_zalogowane,
             count(*) FILTER (WHERE user_id NOT IN (SELECT user_id FROM surowe.users)) konto_nieznane
      FROM surowe.sessions WHERE user_id IS NOT NULL""")

    r("\n5b. Kolejność w czasie: zamówienia, TelemediGO i sesje wobec założenia konta")
    tab("""
      SELECT (SELECT count(*) FROM zam z JOIN surowe.users u USING (user_id) WHERE z.created_at < u.registered_at) zam_przed_kontem,
             (SELECT count(*) FROM surowe.go_memberships g JOIN surowe.users u USING (user_id) WHERE g.purchased_at < u.registered_at) go_przed_kontem,
             (SELECT count(*) FROM surowe.sessions s JOIN surowe.users u USING (user_id) WHERE s.started_at_pl < u.registered_at) sesje_przed_kontem,
             (SELECT count(DISTINCT s.user_id) FROM surowe.sessions s JOIN surowe.users u USING (user_id) WHERE s.started_at_pl < u.registered_at) konta_z_taka_sesja,
             (SELECT max(date_diff('minute', s.started_at_pl, u.registered_at)) FROM surowe.sessions s JOIN surowe.users u USING (user_id) WHERE s.started_at_pl < u.registered_at) max_minut_przed""")
    r("   Sesja zalogowana zaczęta przed założeniem konta to sesja, w której konto powstało (jedna na konto).")
    tab("""
      SELECT count(*) konta, count(*) FILTER (WHERE user_id IN (SELECT user_id FROM zam)) z_zamowieniem,
             count(*) FILTER (WHERE user_id IN (SELECT user_id FROM surowe.go_memberships)) z_telemedigo,
             count(*) FILTER (WHERE user_id NOT IN (SELECT user_id FROM zam) AND user_id NOT IN (SELECT user_id FROM surowe.go_memberships)) bez_zakupu
      FROM surowe.users""")

    r("\n5c. Status wizyty wobec startu, czasu trwania, zwrotu i oceny")
    tab("""
      SELECT status, count(*) zamowienia, count(started_at) ze_startem, count(duration_min) z_czasem_trwania,
             count(*) FILTER (WHERE refund_amount = 0) zwrot_zero, count(*) FILTER (WHERE refund_amount = amount_paid) zwrot_pelny,
             count(*) FILTER (WHERE refund_amount > amount_paid) zwrot_wiekszy_niz_zaplata,
             count(*) FILTER (WHERE refund_amount > 0 AND refund_amount < amount_paid) zwrot_czesciowy, count(rating) z_ocena
      FROM zam GROUP BY 1 ORDER BY 2 DESC""")

    r("\n5d. Cena katalogowa: czy stała w czasie dla każdej specjalizacji")
    tab("""
      SELECT specialization, count(DISTINCT list_price) rozne_ceny, min(list_price) cena, count(*) zamowienia,
             string_agg(DISTINCT visit_purpose, ', ' ORDER BY visit_purpose) cele_wizyt
      FROM zam GROUP BY 1 ORDER BY 3, 1""")

    r("\n5e. Zapłata wobec zniżki")
    tab("""
      SELECT discount_type, coalesce(promo_code, '-') kod, (specialization = 'internista') internista,
             list_price - amount_paid rabat_zl, round(amount_paid / list_price, 3) zaplata_do_ceny, count(*) zamowienia,
             min(created_at)::DATE pierwszy_dzien, max(created_at)::DATE ostatni_dzien
      FROM zam GROUP BY ALL ORDER BY 1, 2, 3, 4""")
    r("   TelemediGO: 50% u internisty, 20% u pozostałych — zgodnie z zasadą. Kody rabatowe to stała kwota w złotych,")
    r("   nie procent (START10 i RANKING10: 10 zł, WRACAM15: 15 zł, L4SZYBKO20: 20 zł, TIKTOK25: 25 zł, TEST-QA: 88 zł).")
    tab("""
      SELECT count(*) FILTER (WHERE discount_type = 'go' AND round(amount_paid / list_price, 2) <> CASE WHEN specialization = 'internista' THEN 0.5 ELSE 0.8 END) go_niezgodne,
             count(*) FILTER (WHERE discount_type = 'none' AND amount_paid <> list_price) bez_znizki_niezgodne,
             count(*) FILTER (WHERE discount_type = 'promo' AND promo_code IS NULL) promo_bez_kodu,
             count(*) FILTER (WHERE discount_type <> 'promo' AND promo_code IS NOT NULL) kod_bez_promo
      FROM zam""")
    r("   Kody rabatowe na pierwszym i kolejnym zamówieniu pacjenta (zamówienia unikalne, kolejność według created_at):")
    con.execute("CREATE TEMP VIEW zam_nr AS SELECT *, row_number() OVER (PARTITION BY user_id ORDER BY created_at) nr FROM zam")
    tab("""
      SELECT promo_code kod, count(*) zamowienia, count(*) FILTER (WHERE nr = 1) na_pierwszym, count(*) FILTER (WHERE nr > 1) na_kolejnym
      FROM zam_nr WHERE promo_code IS NOT NULL GROUP BY 1 ORDER BY 2 DESC""")
    r("   START10 w kwartałach — czy to kod tylko z okresu startu:")
    tab("""
      SELECT strftime(date_trunc('quarter', created_at), '%Y-%m') kwartal_od, count(*) FILTER (WHERE promo_code = 'START10') start10,
             count(*) FILTER (WHERE nr = 1) pierwsze_zamowienia,
             round(100.0 * count(*) FILTER (WHERE promo_code = 'START10') / count(*) FILTER (WHERE nr = 1), 1) proc_pierwszych
      FROM zam_nr GROUP BY 1 ORDER BY 1""")
    r("   Zniżka TelemediGO wobec członkostwa aktywnego w chwili zamówienia (zakup <= zamówienie <= valid_until):")
    tab("""
      WITH a AS (SELECT z.order_id, any_value(z.discount_type) znizka,
                        max(CASE WHEN g.purchased_at <= z.created_at AND z.created_at::DATE <= g.valid_until THEN 1 ELSE 0 END) aktywne_go
                 FROM zam z LEFT JOIN surowe.go_memberships g ON g.user_id = z.user_id GROUP BY 1)
      SELECT znizka, aktywne_go, count(*) zamowienia FROM a GROUP BY ALL ORDER BY ALL""")
    r("   TelemediGO kupione przy zamówieniu wobec zniżki w tym zamówieniu:")
    tab("""
      SELECT z.discount_type znizka_w_zamowieniu, count(*) zakupy_go,
             count(*) FILTER (WHERE g.purchased_at = z.created_at AND g.session_id = z.session_id AND g.user_id = z.user_id) ta_sama_chwila_sesja_konto
      FROM surowe.go_memberships g JOIN zam z USING (order_id) GROUP BY 1""")

    r("\n5f. TelemediGO: cena, ważność, nakładanie się członkostw")
    tab("""
      SELECT amount_paid, date_diff('day', purchased_at::DATE, valid_until) dni_waznosci, count(*) zakupy,
             count(DISTINCT user_id) pacjenci FROM surowe.go_memberships GROUP BY ALL""")
    tab("""
      SELECT count(*) pary_nakladajacych_sie_czlonkostw FROM surowe.go_memberships a JOIN surowe.go_memberships b
        ON a.user_id = b.user_id AND a.membership_id < b.membership_id AND b.purchased_at::DATE <= a.valid_until""")

    r("\n5g. Luki w zbieraniu danych")
    con.execute("""
      CREATE TEMP TABLE dni AS
      SELECT d.dzien, coalesce(s.n, 0) sesje, coalesce(e.n, 0) zdarzenia, coalesce(o.n, 0) zamowienia
      FROM (SELECT unnest(generate_series(DATE '2024-10-01', DATE '2026-09-30', INTERVAL 1 DAY))::DATE dzien) d
      LEFT JOIN (SELECT dzien_pl dzien, count(*) n FROM surowe.sessions GROUP BY 1) s USING (dzien)
      LEFT JOIN (SELECT dzien_pl dzien, count(*) n FROM surowe.events GROUP BY 1) e USING (dzien)
      LEFT JOIN (SELECT created_at::DATE dzien, count(*) n FROM zam GROUP BY 1) o USING (dzien)""")
    tab("""
      SELECT count(*) dni, count(*) FILTER (WHERE sesje = 0) bez_sesji, count(*) FILTER (WHERE zdarzenia = 0) bez_zdarzen,
             count(*) FILTER (WHERE zamowienia = 0) bez_zamowien, min(sesje) min_sesji, min(zamowienia) min_zamowien FROM dni""")
    r("   Dni najniższe wobec mediany z 15 dni wokół (sesje, zamówienia):")
    tab("""
      WITH w AS (SELECT *, median(sesje) OVER (ORDER BY dzien ROWS BETWEEN 7 PRECEDING AND 7 FOLLOWING) ms,
                           median(zamowienia) OVER (ORDER BY dzien ROWS BETWEEN 7 PRECEDING AND 7 FOLLOWING) mz FROM dni)
      SELECT dzien, sesje, round(sesje / ms, 2) sesje_do_mediany, zamowienia, round(zamowienia / mz, 2) zam_do_mediany
      FROM w ORDER BY least(sesje / ms, zamowienia / mz) LIMIT 10""")
    r("   Wszystkie to święta i dni wokół nich (1.11, 24–26.12, 31.12, 1.05, 3.05) — spadek naturalny, nie luka.")
    con.execute("""
      CREATE TEMP TABLE godziny AS
      WITH h AS (SELECT unnest(generate_series(TIMESTAMP '2024-10-01 00:00', TIMESTAMP '2026-09-30 23:00', INTERVAL 1 HOUR)) g)
      SELECT h.g, hour(h.g) godz, coalesce(s.n, 0) sesje, coalesce(e.n, 0) zdarzenia, coalesce(o.n, 0) zamowienia
      FROM h
      LEFT JOIN (SELECT date_trunc('hour', started_at_pl) g, count(*) n FROM surowe.sessions GROUP BY 1) s USING (g)
      LEFT JOIN (SELECT date_trunc('hour', event_at_pl) g, count(*) n FROM surowe.events GROUP BY 1) e USING (g)
      LEFT JOIN (SELECT date_trunc('hour', created_at) g, count(*) n FROM zam GROUP BY 1) o USING (g)""")
    con.execute("""
      CREATE TEMP TABLE godziny_w AS SELECT *,
        median(sesje) OVER (PARTITION BY godz ORDER BY g ROWS BETWEEN 7 PRECEDING AND 7 FOLLOWING) ms,
        median(zdarzenia) OVER (PARTITION BY godz ORDER BY g ROWS BETWEEN 7 PRECEDING AND 7 FOLLOWING) mz FROM godziny""")
    r("   Godziny z najmniejszą liczbą sesji wobec tej samej godziny w 15 dniach wokół (gdy mediana >= 10):")
    tab("""SELECT strftime(g, '%Y-%m-%d %H:%M') godzina, sesje, ms mediana_sesji, zdarzenia, zamowienia FROM godziny_w
           WHERE ms >= 10 ORDER BY sesje / ms, ms DESC LIMIT 5""")
    r("   Godziny z najmniejszą liczbą zdarzeń lejka wobec tej samej godziny w 15 dniach wokół (gdy mediana >= 10):")
    tab("""SELECT strftime(g, '%Y-%m-%d %H:%M') godzina, sesje, zdarzenia, mz mediana_zdarzen, zamowienia FROM godziny_w
           WHERE mz >= 10 ORDER BY zdarzenia / mz, mz DESC LIMIT 5""")
    r("   Jedyna wyraźna luka: 17.05.2025 13:00–14:00 (1 sesja zamiast ok. 21, zero zamówień).")
    r("   Dwie godziny z sesjami, ale bez zdarzeń lejka: 11.10.2024 16:00 (14 sesji) i 14.12.2024 13:00 (15 sesji).")
    r("   Zdarzenie lejka ma ok. 35% sesji, więc 14–15 sesji bez zdarzenia to szansa ok. 1:500 na godzinę. Przy ok. 2 500")
    r("   godzinach dziennych w pierwszym półroczu jedna–dwie takie godziny mogą być przypadkiem. Wpływ pomijalny.")

    r("\n5h. Kroki lejka w sesjach")
    tab("""
      SELECT CASE WHEN s.user_id IS NULL THEN 'niezalogowana' ELSE 'zalogowana' END sesja,
             coalesce(k.k1 || k.k2 || k.k3 || k.k4 || k.k5, '(bez zdarzeń)') kroki_12345, count(*) sesje,
             count(*) FILTER (WHERE s.session_id IN (SELECT session_id FROM zam)) z_zamowieniem,
             count(*) FILTER (WHERE s.session_id IN (SELECT session_id FROM surowe.go_memberships WHERE order_id IS NULL)) samo_telemedigo
      FROM surowe.sessions s LEFT JOIN kroki k USING (session_id) GROUP BY ALL ORDER BY 1, 3 DESC""")
    r("   Kroki: 1 wybór usługi, 2 wybór terminu, 3 logowanie lub konto, 4 wejście na płatność, 5 płatność przyjęta.")
    tab("""
      SELECT count(*) FILTER (WHERE t2 < t1) termin_przed_usluga, count(*) FILTER (WHERE t3 < t2) konto_przed_terminem,
             count(*) FILTER (WHERE t4 < coalesce(t3, t2)) platnosc_przed_poprzednim, count(*) FILTER (WHERE t5 < t4) sukces_przed_wejsciem,
             count(*) FILTER (WHERE k2 = 1 AND k1 = 0) termin_bez_uslugi, count(*) FILTER (WHERE k5 = 1 AND k4 = 0) sukces_bez_wejscia
      FROM kroki""")
    r("   Sesje zalogowane od wejścia (konto w sesji, bez kroku 3), poza zakupem samego TelemediGO:")
    tab("""
      SELECT strftime(date_trunc('quarter', s.dzien_pl), '%Y-%m') kwartal_od, count(*) sesje,
             count(*) FILTER (WHERE k.k1 = 1) z_wyborem_uslugi, count(*) FILTER (WHERE k.k2 = 1) z_wyborem_terminu,
             count(*) FILTER (WHERE k.k5 = 1) z_platnoscia,
             count(*) FILTER (WHERE EXISTS (SELECT 1 FROM zam z WHERE z.user_id = s.user_id AND z.created_at < s.started_at_pl)) pacjent_juz_kupowal
      FROM surowe.sessions s LEFT JOIN kroki k USING (session_id)
      WHERE s.user_id IS NOT NULL AND coalesce(k.k3, 0) = 0
        AND s.session_id NOT IN (SELECT session_id FROM surowe.go_memberships WHERE order_id IS NULL)
      GROUP BY 1 ORDER BY 1""")
    tab("""
      WITH z AS (SELECT user_id, session_id, row_number() OVER (PARTITION BY user_id ORDER BY created_at) nr FROM zam)
      SELECT count(*) FILTER (WHERE nr > 1) sesje_zamowien_powtornych,
             count(*) FILTER (WHERE nr > 1 AND k.k3 = 1) z_krokiem_logowania FROM z JOIN kroki k USING (session_id)""")

    r("\n5i. Realność wartości")
    tab("""
      SELECT min(birth_year) rocznik_min, max(birth_year) rocznik_max, count(*) FILTER (WHERE gender NOT IN ('K', 'M')) plec_inna
      FROM surowe.users""")
    tab("""
      SELECT min(date_diff('minute', created_at, scheduled_at)) min_minut_zaplata_do_terminu,
             max(date_diff('hour', created_at, scheduled_at)) max_godzin_zaplata_do_terminu,
             count(*) FILTER (WHERE scheduled_at < created_at) termin_przed_zaplata,
             count(*) FILTER (WHERE started_at < created_at) start_przed_zaplata,
             min(date_diff('minute', scheduled_at, started_at)) min_minut_opoznienia,
             max(date_diff('minute', scheduled_at, started_at)) max_minut_opoznienia
      FROM zam""")
    tab("""
      SELECT consultation_mode, min(duration_min) czas_min, median(duration_min) czas_mediana, max(duration_min) czas_max
      FROM zam WHERE user_id NOT IN (SELECT user_id FROM konta_testowe) AND duration_min IS NOT NULL GROUP BY 1 ORDER BY 1""")
    tab("""
      SELECT count(*) FILTER (WHERE clicks > impressions) klikniecia_ponad_wyswietlenia, count(*) FILTER (WHERE spend_pln <= 0) koszt_zero,
             round(min(spend_pln / clicks), 2) min_koszt_klikniecia_zl, round(max(spend_pln / clicks), 2) max_koszt_klikniecia_zl
      FROM surowe.marketing_spend""")
    tab("""
      SELECT specialization, visit_purpose, count(*) zamowienia FROM zam
      WHERE specialization = 'psycholog' GROUP BY ALL ORDER BY 3 DESC""")
    r("   Psycholog nie jest lekarzem i w Polsce nie wystawia e-recept. Zamówienia 'psycholog + e_recepta' są nierealne.")

    r("\n5j. Tożsamość: przeglądarki (visitor_id) wobec kont")
    tab("""
      SELECT count(*) przegladarki_z_kontem, count(*) FILTER (WHERE n > 1) przegladarki_kilku_kont
      FROM (SELECT visitor_id, count(DISTINCT user_id) n FROM surowe.sessions WHERE user_id IS NOT NULL GROUP BY 1)""")
    tab("""
      SELECT count(*) konta, count(*) FILTER (WHERE n > 1) konta_z_kilkoma_przegladarkami, round(avg(n), 2) srednio, max(n) najwiecej
      FROM (SELECT user_id, count(DISTINCT visitor_id) n FROM surowe.sessions WHERE user_id IS NOT NULL GROUP BY 1)""")
    tab("""
      SELECT count(*) przegladarki, count(*) FILTER (WHERE zalogowane > 0) kiedys_zalogowane,
             count(*) FILTER (WHERE zalogowane = 0) nigdy_zalogowane
      FROM (SELECT visitor_id, count(user_id) zalogowane FROM surowe.sessions GROUP BY 1)""")

    r("\n5k. Program poleceń: strona /polecenie wobec źródła polecenie")
    tab("""
      SELECT coalesce(utm_source, '(bezposrednie)') zrodlo, coalesce(utm_medium, '-') kanal,
             (landing_page = '/polecenie') wejscie_na_polecenie, count(*) sesje
      FROM surowe.sessions WHERE landing_page = '/polecenie' OR utm_source = 'polecenie' GROUP BY ALL ORDER BY 4 DESC""")

    con.close()
    os.makedirs(os.path.dirname(WYNIK), exist_ok=True)
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"\nRaport zapisany: {os.path.relpath(WYNIK, KATALOG)}")


if __name__ == "__main__":
    main()
