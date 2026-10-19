"""A2 — oczyszczona warstwa danych (schemat `czyste`) według decyzji przyjętych z Kubą 2026-10-19.

Decyzje (notatki/ZALOZENIA.md, punkty 6–9):
  6. Zdublowane zamówienia: zostaje jedna kopia (duplikaty są identyczne w całości).
  7. Konta testowe (każde konto, które choć raz użyło kodu TEST-QA) wyłączone ze wszystkiego:
     zamówienia, konta, sesje, zdarzenia lejka. Na końcu pracy przegląd testów jeszcze raz (plan, punkt D).
  9. Drobne niespójności zostają w danych.

Dane surowe w schemacie `surowe` zostają nietknięte. Skrypt za każdym razem buduje `czyste` od nowa.
Kolejność uruchamiania z głównego folderu projektu:
    python -I analiza/a1_baza.py      # baza i schemat surowe
    python -I analiza/a2_czyste.py    # schemat czyste
Wynik kontroli: ekran + analiza/wyniki/a2_czyste.txt
"""

import datetime as dt
import os

import duckdb

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAZA = os.path.join(KATALOG, "analiza", "telemedi.duckdb")
WYNIK = os.path.join(KATALOG, "analiza", "wyniki", "a2_czyste.txt")
TABELE = ("users", "sessions", "events", "orders", "go_memberships", "marketing_spend")

BUDOWA = """
DROP SCHEMA IF EXISTS czyste CASCADE;
CREATE SCHEMA czyste;

-- konta testowe: każde konto, które choć raz użyło kodu TEST-QA
CREATE TABLE czyste.konta_testowe AS
  SELECT DISTINCT user_id FROM surowe.orders WHERE promo_code = 'TEST-QA' ORDER BY 1;

CREATE TABLE czyste.users AS
  SELECT * EXCLUDE (plik, wiersz_w_pliku) FROM surowe.users
  WHERE user_id NOT IN (SELECT user_id FROM czyste.konta_testowe) ORDER BY user_id;

-- sesje kont testowych: zalogowane na konto testowe albo z przeglądarki, której używało konto testowe
CREATE TABLE czyste.przegladarki_testowe AS
  SELECT DISTINCT visitor_id FROM surowe.sessions WHERE user_id IN (SELECT user_id FROM czyste.konta_testowe);

CREATE TABLE czyste.sessions AS
  SELECT * EXCLUDE (plik, wiersz_w_pliku) FROM surowe.sessions
  WHERE coalesce(user_id, -1) NOT IN (SELECT user_id FROM czyste.konta_testowe)
    AND visitor_id NOT IN (SELECT visitor_id FROM czyste.przegladarki_testowe)
  ORDER BY started_at_utc, session_id;

CREATE TABLE czyste.events AS
  SELECT * EXCLUDE (plik, wiersz_w_pliku) FROM surowe.events
  WHERE session_id IN (SELECT session_id FROM czyste.sessions)
  ORDER BY event_at_utc, session_id;

-- duplikaty zamówień są identyczne w całości, więc DISTINCT zostawia dokładnie jedną kopię
CREATE TABLE czyste.orders AS
  SELECT DISTINCT * EXCLUDE (plik, wiersz_w_pliku) FROM surowe.orders
  WHERE user_id NOT IN (SELECT user_id FROM czyste.konta_testowe)
  ORDER BY created_at, order_id;

CREATE TABLE czyste.go_memberships AS
  SELECT * EXCLUDE (plik, wiersz_w_pliku) FROM surowe.go_memberships
  WHERE user_id NOT IN (SELECT user_id FROM czyste.konta_testowe) ORDER BY purchased_at, membership_id;

CREATE TABLE czyste.marketing_spend AS
  SELECT * EXCLUDE (plik, wiersz_w_pliku) FROM surowe.marketing_spend ORDER BY date, utm_campaign;
"""


def main():
    con = duckdb.connect(BAZA)
    for polecenie in [p for p in BUDOWA.split(";") if p.strip()]:
        con.execute(polecenie)
    linie = []

    def r(tekst=""):
        print(tekst)
        linie.append(tekst)

    def jedna(sql):
        return con.execute(sql).fetchone()[0]

    r(f"A2 — WARSTWA `czyste` ({dt.datetime.now():%Y-%m-%d %H:%M})")
    r("Decyzje: notatki/ZALOZENIA.md, punkty 6–9 (przyjęte z Kubą 2026-10-19).")

    r("\n1. Bilans wierszy: surowe wobec czyste")
    r(f"   {'tabela':16} {'surowe':>9} {'czyste':>9} {'mniej':>7}")
    for t in TABELE:
        s, c = jedna(f"SELECT count(*) FROM surowe.{t}"), jedna(f"SELECT count(*) FROM czyste.{t}")
        r(f"   {t:16} {s:>9,} {c:>9,} {s - c:>7,}")

    r("\n2. Skąd różnica — każda pozycja policzona osobno")
    n_testowe = jedna("SELECT count(*) FROM czyste.konta_testowe")
    kopie = jedna("SELECT count(*) - count(DISTINCT order_id) FROM surowe.orders")
    zam_test = jedna("""SELECT count(DISTINCT order_id) FROM surowe.orders
                        WHERE user_id IN (SELECT user_id FROM czyste.konta_testowe)""")
    kopie_test = jedna("""SELECT count(*) - count(DISTINCT order_id) FROM surowe.orders
                          WHERE user_id IN (SELECT user_id FROM czyste.konta_testowe)""")
    ses_test = jedna("""SELECT count(*) FROM surowe.sessions WHERE user_id IN (SELECT user_id FROM czyste.konta_testowe)
                        OR visitor_id IN (SELECT visitor_id FROM czyste.przegladarki_testowe)""")
    ses_test_anon = jedna("""SELECT count(*) FROM surowe.sessions WHERE user_id IS NULL
                             AND visitor_id IN (SELECT visitor_id FROM czyste.przegladarki_testowe)""")
    zd_test = jedna("SELECT count(*) FROM surowe.events WHERE session_id NOT IN (SELECT session_id FROM czyste.sessions)")
    r(f"   users:    {n_testowe} kont testowych.")
    r(f"   orders:   {kopie:,} dodatkowych kopii (w tym {kopie_test} kopii zamówień testowych) + "
      f"{zam_test:,} zamówień testowych (każde liczone raz) = {kopie + zam_test:,} wierszy.")
    r(f"   sessions: {ses_test:,} sesji kont i przeglądarek testowych, w tym {ses_test_anon} niezalogowanych.")
    r(f"   events:   {zd_test:,} zdarzeń lejka z tych sesji.")
    r("   go_memberships i marketing_spend: bez zmian (konta testowe nie kupowały TelemediGO).")

    r("\n3. Kontrole")
    kontrole = [
        ("bilans orders: ubyło = kopie + zamówienia testowe",
         "SELECT (SELECT count(*) FROM surowe.orders) - (SELECT count(*) FROM czyste.orders)", kopie + zam_test),
        ("bilans sessions: ubyło = sesje kont i przeglądarek testowych",
         "SELECT (SELECT count(*) FROM surowe.sessions) - (SELECT count(*) FROM czyste.sessions)", ses_test),
        ("zamówienia unikalne w czyste.orders", "SELECT count(*) - count(DISTINCT order_id) FROM czyste.orders", 0),
        ("zamówienia z kodem TEST-QA", "SELECT count(*) FROM czyste.orders WHERE promo_code = 'TEST-QA'", 0),
        ("zamówienia trwające 1 minutę (drugi podpis testów)", "SELECT count(*) FROM czyste.orders WHERE duration_min = 1", 0),
        ("zamówienia bez sesji w czyste.sessions",
         "SELECT count(*) FROM czyste.orders WHERE session_id NOT IN (SELECT session_id FROM czyste.sessions)", 0),
        ("zakupy TelemediGO bez sesji w czyste.sessions",
         "SELECT count(*) FROM czyste.go_memberships WHERE session_id NOT IN (SELECT session_id FROM czyste.sessions)", 0),
        ("zamówienia bez konta w czyste.users",
         "SELECT count(*) FROM czyste.orders WHERE user_id NOT IN (SELECT user_id FROM czyste.users)", 0),
        ("sesje zalogowane na konto spoza czyste.users",
         "SELECT count(*) FROM czyste.sessions WHERE user_id IS NOT NULL AND user_id NOT IN (SELECT user_id FROM czyste.users)", 0),
        ("kroki payment_succeeded bez zamówienia i bez TelemediGO",
         """SELECT count(*) FROM czyste.events WHERE event_name = 'payment_succeeded'
            AND session_id NOT IN (SELECT session_id FROM czyste.orders)
            AND session_id NOT IN (SELECT session_id FROM czyste.go_memberships)""", 0),
    ]
    wszystko_ok = True
    for opis, sql, oczek in kontrole:
        wynik = jedna(sql)
        ok = wynik == oczek
        wszystko_ok &= ok
        r(f"   {opis:58} {wynik:>6}  {'zgodne' if ok else 'BŁĄD'}")

    con.close()
    os.makedirs(os.path.dirname(WYNIK), exist_ok=True)
    with open(WYNIK, "w", encoding="utf-8") as f:
        f.write("\n".join(linie) + "\n")
    print(f"\nRaport zapisany: {os.path.relpath(WYNIK, KATALOG)}")
    if not wszystko_ok:
        raise SystemExit("Kontrola warstwy czyste nie przeszła — sprawdź raport.")


if __name__ == "__main__":
    main()
