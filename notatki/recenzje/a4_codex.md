# Recenzja definicji A4 — Codex (model Sol), 2026-10-19

**Co sprawdzał:** czy przyjęte definicje (`ZALOZENIA.md` 16–26) odpowiadają pytaniu zadania, czy czegoś nie brakuje w wariantach i pułapkach, czy kod `analiza/a4_definicje.py` liczy to, co mówią definicje (ręcznie, na konkretnych pacjentach), i czy liczby w notatkach zgadzają się z raportem. Polecenie: `a4_codex_prompt.md`. Pełna odpowiedź: `a4_codex_odpowiedz.md`. Codex pracował tylko do odczytu (`-s read-only`), na modelu `gpt-6.1-sol`.

**Wynik:** brak błędu, który zmieniałby odpowiedź na pytanie zadania. Ręcznie sprawdzonych pacjentów jest siedmiu (100127, 100026, 100081, 138084, 100308, 101505, 100197). Codex potwierdził liczby nowych pacjentów, logikę powrotu, granice okresów, przypisanie źródła razem z nadpisaniem kodem, prowizję i liczby w notatkach.

| Nr | Uwaga Codeksa | Waga | Co zrobiliśmy |
|---|---|---|---|
| 1 | Spadek powrotu całości miesza zmianę struktury kanałów ze zmianą zachowania | ważna | Przyjęte jako metoda do A5 (`PLAN.md`, A5): powrót całej bazy obok powrotu przy stałej strukturze kanałów, potem także pierwszej usługi i zniżki; TikTok jako nowy, osobny segment; wynik nie jest dowodem przyczyny. Liczby Codeksa (np. 21,29%) wejdą do notatek dopiero po przeliczeniu naszym kodem. |
| 2 | Pełne okno obcina okres 2, więc porównanie z całym okresem 1 miesza pory roku | ważna | Przyjęte (Kuba): `ZALOZENIA.md` 27, w kodzie `stopy_por()`. Powrót w 90 dniach 23,9% (12 867 pacjentów) wobec 17,4% (18 924 pacjentów). |
| 3 | Okno CRM liczyło też zamówienia anulowane, niezgodnie z definicją powrotu | ważna | Przyjęte (Kuba): `ZALOZENIA.md` 26. Do 24 godzin 182 zamówienia na 1 000 wejść zamiast 189. |
| 4 | Jedno zamówienie mogło trafić do kilku wejść z CRM | ważna | Przyjęte (Kuba): przy przypisaniu sprzedaży ostatnie wejście przed płatnością (`ZALOZENIA.md` 26, raport sekcja 6e). Profil po kliknięciu zostaje na każde wejście. |
| 5 | Odstępy godzinowe liczone z czasu polskiego bez strefy | drobna | Poprawione w kodzie: odstępy w UTC. Nie zmienia kwalifikacji do okien 24 godzin i 7 dni. |
| 6 | Tło (dni 31–60) wymaga 61 dni obserwacji, a filtr dawał 60 | drobna | Poprawione w kodzie: 53 wejścia mniej, tło praktycznie bez zmian. |
| 7 | Znacznik „zalogowana od wejścia” pomijał wyjątek dla zakupu samego TelemediGO | drobna | Poprawione w kodzie zgodnie z `ZALOZENIA.md` 10. |
| — | Remarketing: 0,6% przy przyjętej regule, a nie 0,7% | drobna | Poprawione w `ZALOZENIA.md` 24. |

**Czego nie przyjęliśmy jako wniosku:** zdanie otwierające Codeksa („retencja całej bazy spada”) zostaje obserwacją do A5. Jego dodatkowe przeliczenia, na przykład kohorty bez października 2024 (23,72% wobec 17,38%), powtórzymy własnym kodem w A5.
