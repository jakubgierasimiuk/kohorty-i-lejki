"""D — przegląd zamówień testowych przed publikacją (zastrzeżenie Kuby z A2, plan punkt D; 2026-10-21).

Pytania z planu: czy wyłączenie 22 kont testowych jest słuszne i kompletne, czy test nie przykrywa prawdziwych
zamówień (ani sesji), jak liczyć koszt lekarza za wizyty testowe. Reguła z A2 (ZALOZENIA.md 7): konto testowe =
konto, które choć raz użyło kodu TEST-QA; wyłączamy jego zamówienia, konto, sesje (także anonimowe z jego
przeglądarek) i zdarzenia lejka. Skrypt tylko czyta bazę (surowe i czyste), niczego nie zmienia.

Uruchomienie z głównego folderu: python -I analiza/d_testy.py  →  analiza/wyniki/d_testy.txt
"""
import os
import sys

import duckdb

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAZA = os.path.join(KATALOG, "analiza", "telemedi.duckdb")
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "d_testy.txt")
OKRES2 = "2025-10-01"
KOSZT_INTERNISTY = 25  # zasada z zadania: koszt lekarza za odbytą wizytę u internisty (zł)

linie = []


def r(s=""):
    linie.append(s)


def naglowek(s):
    r()
    r("=" * 110)
    r(s)
    r("=" * 110)


def main():
    sys.stdout.reconfigure(errors="replace")
    con = duckdb.connect(BAZA, read_only=True)
    df = lambda q: con.execute(q).df()
    jedna = lambda q: con.execute(q).fetchone()[0]

    # bez zdublowanych kopii: jak w a2_czyste.py (kopie różnią się tylko plikiem i numerem wiersza w pliku)
    con.execute("""CREATE TEMP TABLE zam AS SELECT DISTINCT * EXCLUDE (plik, wiersz_w_pliku) FROM surowe.orders""")
    kontrola = con.execute("SELECT count(*) = count(DISTINCT order_id) FROM zam").fetchone()[0]
    assert kontrola, "po usunięciu kopii zostały zdublowane numery zamówień"
    con.execute("""CREATE TEMP TABLE test_kod AS SELECT DISTINCT user_id FROM surowe.orders WHERE promo_code = 'TEST-QA'""")
    con.execute(f"""CREATE TEMP TABLE zam_t AS
      SELECT z.*, z.user_id IN (SELECT user_id FROM test_kod) testowe,
             CASE WHEN z.created_at < TIMESTAMP '{OKRES2}' THEN 1 ELSE 2 END okres
      FROM zam z""")

    r("D — PRZEGLĄD ZAMÓWIEŃ TESTOWYCH PRZED PUBLIKACJĄ (schematy `surowe` i `czyste`, tylko odczyt)")
    r("Reguła z A2 (ZALOZENIA.md 7): konto testowe = konto, które choć raz użyło kodu TEST-QA. Zamówienia liczone")
    r("bez zdublowanych kopii z czerwca 2026 (DISTINCT na surowych wierszach). Okres według dnia płatności.")

    naglowek("1. CZY REGUŁA JEST TA SAMA: konta testowe w schemacie `czyste` a konta z kodem TEST-QA w danych surowych")
    a = jedna("SELECT count(*) FROM test_kod")
    b = jedna("SELECT count(*) FROM czyste.konta_testowe")
    c = jedna("SELECT count(*) FROM (SELECT user_id FROM test_kod EXCEPT SELECT user_id FROM czyste.konta_testowe)")
    d = jedna("SELECT count(*) FROM (SELECT user_id FROM czyste.konta_testowe EXCEPT SELECT user_id FROM test_kod)")
    r(f"   konta z TEST-QA: {a}; czyste.konta_testowe: {b}; różnica w jedną stronę: {c}, w drugą: {d}")

    naglowek("2. PROFIL ZAMÓWIEŃ KONT TESTOWYCH (czy wśród nich są zamówienia wyglądające na prawdziwe)")
    r(df("""SELECT okres, count(*) zamowienia, count(*) FILTER (WHERE promo_code = 'TEST-QA') z_kodem_test_qa,
                   count(*) FILTER (WHERE promo_code IS NULL) bez_kodu,
                   count(*) FILTER (WHERE promo_code IS NOT NULL AND promo_code <> 'TEST-QA') z_innym_kodem,
                   count(*) FILTER (WHERE specialization <> 'internista') nie_internista,
                   count(*) FILTER (WHERE duration_min IS DISTINCT FROM 1) czas_inny_niz_1_min,
                   count(*) FILTER (WHERE status = 'completed') odbyte, count(*) FILTER (WHERE status <> 'completed') inny_status,
                   round(sum(amount_paid), 2) zaplacono_zl, round(sum(coalesce(refund_amount, 0)), 2) zwroty_zl,
                   count(*) FILTER (WHERE rating IS NOT NULL) z_ocena
            FROM zam_t WHERE testowe GROUP BY okres ORDER BY okres""").to_string(index=False))
    r()
    r("   Cel wizyty, tryb i metoda płatności zamówień testowych (oba okresy):")
    r(df("""SELECT visit_purpose, consultation_mode, payment_method, count(*) n FROM zam_t WHERE testowe
            GROUP BY ALL ORDER BY n DESC LIMIT 12""").to_string(index=False))
    r()
    r("   Liczba zamówień na konto testowe (min, mediana, maks) i zakres dat:")
    r(df("""SELECT min(n) min_n, median(n) med_n, max(n) max_n, min(od) pierwsze, max(do_) ostatnie FROM (
              SELECT user_id, count(*) n, min(created_at) od, max(created_at) do_ FROM zam_t WHERE testowe GROUP BY 1)""").to_string(index=False))

    naglowek("3. CZY SĄ TESTY POZA REGUŁĄ (kompletność): podpisy testu w zamówieniach pozostałych kont")
    r(df("""SELECT
              count(*) FILTER (WHERE duration_min = 1) wizyty_1_min,
              count(*) FILTER (WHERE upper(coalesce(promo_code, '')) LIKE '%TEST%' OR upper(coalesce(promo_code, '')) LIKE '%QA%') kod_test_lub_qa,
              count(*) FILTER (WHERE amount_paid = 0) zaplata_0_zl,
              count(*) FILTER (WHERE duration_min <= 2) wizyty_do_2_min
            FROM zam_t WHERE NOT testowe""").to_string(index=False))
    r()
    r("   Rozkład czasu wizyty odbytych w pozostałych kontach (najkrótsze wartości):")
    r(df("""SELECT duration_min, count(*) n FROM zam_t WHERE NOT testowe AND status IN ('completed', 'refunded')
            GROUP BY 1 ORDER BY 1 LIMIT 6""").to_string(index=False))
    r()
    r("   Konta z największą liczbą zamówień poza kontami testowymi (czy któreś wygląda na test):")
    r(df("""SELECT user_id, count(*) zamowienia, count(DISTINCT specialization) specjalizacje,
                   round(avg(duration_min), 1) sr_czas_min, count(*) FILTER (WHERE promo_code IS NOT NULL) z_kodem
            FROM zam_t WHERE NOT testowe GROUP BY 1 ORDER BY 2 DESC LIMIT 5""").to_string(index=False))
    r()
    r("   Ile zamówień ma przeciętne konto testowe, a ile konto z największą liczbą zamówień poza testami:")
    r(df("""SELECT (SELECT round(avg(n), 1) FROM (SELECT count(*) n FROM zam_t WHERE testowe GROUP BY user_id)) sr_na_konto_testowe,
                   (SELECT max(n) FROM (SELECT count(*) n FROM zam_t WHERE NOT testowe GROUP BY user_id)) maks_poza_testami""").to_string(index=False))

    naglowek("4. CZY WYŁĄCZENIE NIE ZABIERA PRAWDZIWYCH SESJI: przeglądarki kont testowych a inne konta")
    r(df("""WITH pt AS (SELECT DISTINCT visitor_id FROM surowe.sessions WHERE user_id IN (SELECT user_id FROM test_kod))
            SELECT (SELECT count(*) FROM pt) przegladarki_testowe,
                   (SELECT count(DISTINCT visitor_id) FROM surowe.sessions
                     WHERE visitor_id IN (SELECT visitor_id FROM pt) AND user_id IS NOT NULL
                       AND user_id NOT IN (SELECT user_id FROM test_kod)) wspolne_z_innym_kontem,
                   (SELECT count(*) FROM surowe.sessions WHERE visitor_id IN (SELECT visitor_id FROM pt)) sesje_tych_przegladarek,
                   (SELECT count(*) FROM surowe.sessions WHERE visitor_id IN (SELECT visitor_id FROM pt) AND user_id IS NULL) w_tym_anonimowe""").to_string(index=False))
    r()
    r("   Źródło wejścia sesji kont testowych (czy testy wchodzą z kampanii płatnych i zawyżają ich sesje):")
    r(df("""SELECT coalesce(utm_source, '(wejście bezpośrednie)') zrodlo, count(*) sesje FROM surowe.sessions
            WHERE user_id IN (SELECT user_id FROM test_kod)
               OR visitor_id IN (SELECT DISTINCT visitor_id FROM surowe.sessions WHERE user_id IN (SELECT user_id FROM test_kod))
            GROUP BY 1 ORDER BY 2 DESC""").to_string(index=False))

    naglowek("5. CZY `czyste` JEST WOLNE OD TESTÓW")
    r(df("""SELECT (SELECT count(*) FROM czyste.orders WHERE user_id IN (SELECT user_id FROM test_kod)) zamowienia,
                   (SELECT count(*) FROM czyste.users WHERE user_id IN (SELECT user_id FROM test_kod)) konta,
                   (SELECT count(*) FROM czyste.sessions WHERE user_id IN (SELECT user_id FROM test_kod)) sesje_zalogowane,
                   (SELECT count(*) FROM czyste.sessions WHERE visitor_id IN
                      (SELECT DISTINCT visitor_id FROM surowe.sessions WHERE user_id IN (SELECT user_id FROM test_kod))) sesje_przegladarek_testowych,
                   (SELECT count(*) FROM czyste.go_memberships WHERE user_id IN (SELECT user_id FROM test_kod)) telemedigo,
                   (SELECT count(*) FROM czyste.orders WHERE promo_code = 'TEST-QA') zamowienia_z_kodem_test_qa,
                   (SELECT count(*) FROM czyste.orders WHERE duration_min = 1) wizyty_1_min""").to_string(index=False))

    naglowek("6. KOSZT LEKARZA ZA WIZYTY TESTOWE (zasada z zadania: 25 zł za odbytą wizytę u internisty)")
    k = df(f"""SELECT okres, count(*) FILTER (WHERE status IN ('completed', 'refunded')) wizyty_odbyte,
                      {KOSZT_INTERNISTY} * count(*) FILTER (WHERE status IN ('completed', 'refunded')
                          AND specialization = 'internista') koszt_zl
               FROM zam_t WHERE testowe GROUP BY okres ORDER BY okres""")
    r(k.to_string(index=False))
    r(f"   razem: {int(k['koszt_zl'].sum()):,} zł".replace(",", " "))
    r("   Przyjęte w A2 (ZALOZENIA.md 8): kosztu lekarza za wizyty testowe nie liczymy; wariant z kosztem jest niewiadomą 14")
    r("   i częścią pozycji 2 listy priorytetów (sprawdzenie w dziale rozliczeń).")

    naglowek("7. TESTÓW PRZYBYWA: zamówienia testowe w kwartałach")
    r(df("""SELECT strftime(date_trunc('quarter', created_at), '%Y-%m') kwartal_od, count(*) zamowienia_testowe,
                   count(DISTINCT user_id) aktywne_konta_testowe
            FROM zam_t WHERE testowe GROUP BY 1 ORDER BY 1""").to_string(index=False))

    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"Raport: {os.path.relpath(WYNIK, KATALOG)} ({len(linie)} linii)")


if __name__ == "__main__":
    main()
