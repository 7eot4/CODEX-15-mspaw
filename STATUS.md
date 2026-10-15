# Stan realizacji — 2026-10-15

Cel uruchomienia strony dla rzeczywistych klientów nie jest ukończony. Na wyraźną prośbę użytkownika uzupełniono fikcyjne dane kontaktowe i włączono demonstracyjny cennik. Brak danych wykonawcy nie blokuje już lokalnej prezentacji i testowania natychmiastowej wyceny. Dane i ceny demo są jawnie oznaczone; nie zostały przypisane Maciejowi jako jego rzeczywista oferta.

| Wymaganie | Dowód aktualnego stanu | Ocena |
|---|---|---|
| Research innych wykonawców | RESEARCH.md: źródła oraz wnioski z formularzy i konfiguratorów | Wykonane, ograniczony odczyt profili firmy |
| Strona Macieja | dist/index.html, style.css; nazwisko i miejscowość potwierdzone przez użytkownika | Przygotowana lokalnie; zakres usług i wygląd wymagają zatwierdzenia/sprawdzenia |
| Zapytanie o zlecenie | server.py, test_http.py: żądanie HTTP zapisuje zgłoszenie; test_server.py sprawdza odczyt i załącznik | Działa lokalnie; brak dostawy do Macieja |
| Odczyt zleceń | inbox.py, ODBIOR.cmd, test_inbox.py | Działa lokalnie, poza katalogiem publicznym |
| Natychmiastowa wycena | pricing.py, pricing.json, test_pricing.py, test_http.py | Działa w trybie demo; przykład 6,5 m daje 4700–6330 PLN brutto. approved=false, mode=demo, demoEnabled=true; wynik zapisuje demo=true |
| Rzeczywista oferta cenowa | Brak zatwierdzonych stawek, przekrojów i zakresów wariantów | Nieukończone; wymagane dane Macieja |
| Test wyglądu i pełnej obsługi w przeglądarce | Próba otwarcia: brak przeglądarki IAB, tworzenie karty Chrome odmówione przez konektor | Niezweryfikowane |
| Publikacja | Brak zewnętrznego repozytorium/hostingu i adresu publikacji | Nieopublikowane; wymaga przygotowania docelowego odbioru i potwierdzenia działania zewnętrznego |

Weryfikacja ostatniej zmiany: `python -m unittest discover -s tests -v` — 12 testów poprawnych, w tym demonstracyjny cennik i brak domniemanej zgody wykonawcy; `node --check dist/app.js` — poprawna składnia; `git diff --check` — brak błędów. Nie wykonano testu wysłania wiadomości do firmy. Testy zapisu wykonują się w katalogach tymczasowych.

Teraz: podgląd lokalny i testy z przyciskiem „Wczytaj przykład demonstracyjny”. Następnie: kontrola w przeglądarce. Backlog przed obsługą prawdziwych klientów: rzeczywiste dane i stawki Macieja, podłączenie uzgodnionego odbioru zapytań, zdjęcia realizacji i publikacja do zatwierdzenia. Lokalny zapis testowy nie oznacza dostarczenia wiadomości do firmy.
