# Stan realizacji — 2026-10-15

Cel nie jest ukończony. Projekt lokalny ma działający zapis i odczyt zapytań oraz mechanizm automatycznej wyceny przygotowany do stawek wykonawcy. Brak danych nie został zastąpiony danymi innych firm ani fikcyjnymi cenami.

| Wymaganie | Dowód aktualnego stanu | Ocena |
|---|---|---|
| Research innych wykonawców | RESEARCH.md: źródła oraz wnioski z formularzy i konfiguratorów | Wykonane, ograniczony odczyt profili firmy |
| Strona Macieja | dist/index.html, style.css; nazwisko i miejscowość potwierdzone przez użytkownika | Przygotowana lokalnie; zakres usług i wygląd wymagają zatwierdzenia/sprawdzenia |
| Zapytanie o zlecenie | server.py, test_http.py: żądanie HTTP zapisuje zgłoszenie; test_server.py sprawdza odczyt i załącznik | Działa lokalnie; brak dostawy do Macieja |
| Odczyt zleceń | inbox.py, ODBIOR.cmd, test_inbox.py | Działa lokalnie, poza katalogiem publicznym |
| Natychmiastowa wycena | pricing.py, test_pricing.py, test_http.py | Mechanizm przetestowany na danych syntetycznych; pricing.json nadal approved=false, rates={} |
| Rzeczywista oferta cenowa | Brak zatwierdzonych stawek, przekrojów i zakresów wariantów | Nieukończone; wymagane dane Macieja |
| Test wyglądu i pełnej obsługi w przeglądarce | Próba otwarcia: brak przeglądarki IAB, tworzenie karty Chrome odmówione przez konektor | Niezweryfikowane |
| Publikacja | Brak zewnętrznego repozytorium/hostingu i adresu publikacji | Nieopublikowane; wymaga przygotowania docelowego odbioru i potwierdzenia działania zewnętrznego |

Weryfikacja ostatniej zmiany: `python -m unittest discover -s tests -v` — 10 testów poprawnych; `node --check dist/app.js` — poprawna składnia; `git diff --check` — brak błędów. Wygenerowano pusty lokalny widok `.local/inbox/index.html`, bez tworzenia bazy i bez rzeczywistych danych klientów. Nie wykonano testu wysłania wiadomości do firmy.

Teraz: oczekiwanie na telefon i e-mail Macieja oraz jego cennik i zakres wycenianych wariantów. Następnie: podłączenie uzgodnionego sposobu odbioru, kontrola w przeglądarce i przygotowanie publikacji do zatwierdzenia. Backlog: własne zdjęcia realizacji i dopracowanie treści z wykonawcą. Nie rozbudowywać dalej architektury w zastępstwie brakujących danych.
