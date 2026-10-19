"""A2 — wyliczenia do dyskusji o trzech otwartych sprawach z przeglądu jakości danych (2026-10-19).

  1. Co robią pacjenci po sesji zalogowanej od wejścia (konto w sesji bez kroku logowania).
  2. Pierwsze tygodnie biznesu: nowi pacjenci, zamówienia powtórne, START10 — czy jest „okres rozruchu”.
  3. Kody rabatowe wobec źródła sesji, w której pacjent zapłacił.

Tylko czyta schemat `czyste` (analiza/a2_czyste.py). Uruchomienie z głównego folderu projektu:
    python -I analiza/a2_dyskusja.py
Wynik: ekran + analiza/wyniki/a2_dyskusja.txt
"""

import datetime as dt
import os

import duckdb
import pandas as pd

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAZA = os.path.join(KATALOG, "analiza", "telemedi.duckdb")
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "a2_dyskusja.txt")
pd.set_option("display.width", 200)


def main():
    con = duckdb.connect(BAZA, read_only=True)
    linie = []

    def r(tekst=""):
        print(tekst)
        linie.append(tekst)

    def tab(sql, wciecie="     "):
        for linia in con.sql(sql).df().to_string(index=False).splitlines():
            r(wciecie + linia)

    r(f"A2 — WYLICZENIA DO DYSKUSJI ({dt.datetime.now():%Y-%m-%d %H:%M}), schemat `czyste`")

    r("\n1. Sesje zalogowane od wejścia (bez kroku logowania, bez zakupu samego TelemediGO):")
    r("   kiedy ten sam pacjent składa następne zamówienie")
    con.execute("""
      CREATE TEMP TABLE kroki AS SELECT session_id, max((event_name = 'service_selected')::INT) k1,
             max((event_name = 'account_completed')::INT) k3 FROM czyste.events GROUP BY 1""")
    con.execute("""
      CREATE TEMP TABLE zalogowane AS
      SELECT s.session_id, s.user_id, s.visitor_id, s.started_at_pl, coalesce(k.k1, 0) k1,
             (SELECT min(o.created_at) FROM czyste.orders o WHERE o.user_id = s.user_id AND o.created_at > s.started_at_pl) nast
      FROM czyste.sessions s LEFT JOIN kroki k USING (session_id)
      WHERE s.user_id IS NOT NULL AND coalesce(k.k3, 0) = 0
        AND s.session_id NOT IN (SELECT session_id FROM czyste.go_memberships WHERE order_id IS NULL)""")
    tab("""
      SELECT CASE WHEN k1 = 1 THEN 'wybrał usługę' ELSE 'bez zdarzeń lejka' END sesja, count(*) sesje,
             round(100.0 * count(*) FILTER (WHERE date_diff('minute', started_at_pl, nast) <= 60) / count(*), 1) proc_zam_do_1h,
             round(100.0 * count(*) FILTER (WHERE date_diff('hour', started_at_pl, nast) <= 24) / count(*), 1) proc_zam_do_24h,
             round(100.0 * count(*) FILTER (WHERE date_diff('day', started_at_pl, nast) <= 7) / count(*), 1) proc_zam_do_7_dni,
             round(100.0 * count(*) FILTER (WHERE date_diff('day', started_at_pl, nast) <= 30) / count(*), 1) proc_zam_do_30_dni
      FROM zalogowane GROUP BY 1 ORDER BY 1""")

    r("\n2. Pierwsze tygodnie (tydzień od poniedziałku; pierwszy tydzień ma 6 dni: 1–6.10.2024)")
    tab("""
      WITH pierwsze AS (SELECT user_id, min(created_at) t FROM czyste.orders GROUP BY 1),
           tyg AS (SELECT unnest(generate_series(DATE '2024-09-30', DATE '2025-03-31', INTERVAL 7 DAY))::DATE tydzien_od)
      SELECT t.tydzien_od,
             (SELECT count(*) FROM pierwsze p WHERE date_trunc('week', p.t) = t.tydzien_od) nowi_pacjenci,
             (SELECT count(*) FROM czyste.orders o WHERE date_trunc('week', o.created_at) = t.tydzien_od) zamowienia,
             (SELECT count(*) FROM czyste.orders o WHERE date_trunc('week', o.created_at) = t.tydzien_od)
               - (SELECT count(*) FROM pierwsze p WHERE date_trunc('week', p.t) = t.tydzien_od) zamowienia_powtorne,
             (SELECT count(*) FROM czyste.sessions s WHERE date_trunc('week', s.dzien_pl) = t.tydzien_od) sesje,
             (SELECT round(sum(spend_pln)) FROM czyste.marketing_spend m WHERE date_trunc('week', m.date) = t.tydzien_od) koszt_kampanii_zl,
             (SELECT count(*) FROM czyste.orders o WHERE o.promo_code = 'START10' AND date_trunc('week', o.created_at) = t.tydzien_od) start10
      FROM tyg t ORDER BY 1""")

    r("\n3a. Kody rabatowe: źródło sesji, w której pacjent zapłacił (cztery najczęstsze)")
    tab("""
      WITH a AS (SELECT o.promo_code kod, coalesce(s.utm_source, '(bezposrednie)') || ' / ' || coalesce(s.utm_campaign, s.utm_medium, '-') zrodlo_sesji,
                        count(*) n
                 FROM czyste.orders o JOIN czyste.sessions s USING (session_id) WHERE o.promo_code IS NOT NULL GROUP BY 1, 2)
      SELECT kod, zrodlo_sesji, n zamowienia, round(100.0 * n / sum(n) OVER (PARTITION BY kod), 1) proc_kodu
      FROM a QUALIFY row_number() OVER (PARTITION BY kod ORDER BY n DESC) <= 4 ORDER BY kod, n DESC""")
    r("\n3b. Pierwsze zamówienia według źródła sesji płatności: udział kodów kampanii")
    tab("""
      WITH p AS (SELECT o.*, row_number() OVER (PARTITION BY user_id ORDER BY created_at) nr FROM czyste.orders o)
      SELECT coalesce(s.utm_campaign, s.utm_source, '(bezposrednie)') zrodlo_sesji, count(*) pierwsze_zamowienia,
             round(100.0 * count(*) FILTER (WHERE promo_code = 'L4SZYBKO20') / count(*), 1) proc_l4szybko20,
             round(100.0 * count(*) FILTER (WHERE promo_code = 'TIKTOK25') / count(*), 1) proc_tiktok25,
             round(100.0 * count(*) FILTER (WHERE promo_code = 'RANKING10') / count(*), 1) proc_ranking10,
             round(100.0 * count(*) FILTER (WHERE promo_code = 'START10') / count(*), 1) proc_start10
      FROM p JOIN czyste.sessions s USING (session_id) WHERE nr = 1 GROUP BY 1 ORDER BY 2 DESC""")
    r("\n3c. Wartość zniżek w złotych (cena katalogowa minus zapłata), dwa lata")
    tab("""
      SELECT coalesce(promo_code, 'TelemediGO') znizka, count(*) zamowienia, sum(list_price - amount_paid) zl_zniżki,
             round(avg(100 * (list_price - amount_paid) / list_price), 1) sredni_proc_ceny
      FROM czyste.orders WHERE discount_type <> 'none' GROUP BY 1 ORDER BY 3 DESC""")

    con.close()
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"\nRaport zapisany: {os.path.relpath(WYNIK, KATALOG)}")


if __name__ == "__main__":
    main()
