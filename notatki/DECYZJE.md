# Decyzje

Decyzje podjęte w trakcie pracy (metoda, podziały, narzędzie, hosting) — co wybraliśmy, dlaczego i jakie były alternatywy.

## 2026-10-19 — plan pracy i sposób współpracy

**Decyzja:** pracujemy według planu z `notatki/PLAN.md` (wersja 2, zatwierdzona przez Kubę). Kolejność: wstępna analiza → narzędzie → uzupełnienie analizy → weryfikacja.

**Dlaczego tak:** pierwsza wersja planu zakładała, że Claude wykona całą analizę samodzielnie, a narzędzie zbuduje równolegle z analizą. Kuba ją odrzucił:
- wnioski wyciągamy razem — Claude liczy i pokazuje, po każdym większym kroku jest przegląd, a wnioski weryfikuje konsylium;
- narzędzie dopiero po wspólnym pierwszym etapie analizy, żeby budować je na sprawdzonych definicjach;
- przed rozpoczęciem każdego punktu Kuba decyduje, czy idziemy dalej;
- bez dat w planie.

**Co Kuba dodał do treści planu:** dokładne odtworzenie liczb dashboardu (a nie „mniej więcej”) i zestawienie ich z miarami po oczyszczeniu; rozszerzona kontrola jakości (duplikaty w każdej tabeli osobno, profil zamówień TEST-QA, kliknięcia wobec sesji, czas zamówień wobec czasu płatności); wspólne ustalenie definicji z wariantami przed kohortami; opis obejścia pułapek (start od zera, młode kohorty, sezonowość); analiza tego, co dzieje się po zakupie; wartość priorytetów w marży; stała zasada „najpierw napraw, potem wyłączaj” (dopisana do CLAUDE.md, punkt 9).

**Wykonanie:** osobna sesja Claude Code prowadzi plan punkt po punkcie, w tym samym folderze projektu.
