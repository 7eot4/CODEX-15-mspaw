# Stan realizacji — 2026-10-15

Najnowsza aktualizacja: dodane oryginalne logo oraz sześć różnych obrazów realizacji M-SPAW wyodrębnionych z dostarczonego zapisu Instagrama. Rzeczywiste zdjęcia zastąpiły wizualizacje w galerii i obrazach głównych. Numer 538 792 159 i e-mail firma.mspaw@gmail.com pochodzą z treści firmowego posta. Mapa używa adresu Niedźwiedź 217 potwierdzonego przez użytkownika. PDF i elementy interfejsu konta pozostają lokalnie, a publikacja kopiuje wyłącznie siedem zatwierdzonych plików JPG. Ceny i obsługa formularza w Pages nadal demonstracyjne.

Podgląd opublikowany na wyraźne polecenie użytkownika: https://7eot4.github.io/CODEX-15-mspaw/ . Publiczne repozytorium: https://github.com/7eot4/CODEX-15-mspaw , gałąź `main`. Każdy push uruchamia testy i wdrożenie. Zasady kolejnych aktualizacji zapisano w AGENTS.md.

Zmiana wyglądu na prośbę użytkownika: nowoczesne konstrukcje, jasna strona, minimalizm i eleganckie balustrady. Nowy układ i oprawa, obrazy w dist/assets, pełne opisy w ASSETS.md. Kalkulator i ścieżka zapytania pozostają demonstracyjne. Kontrola graficzna strony w przeglądarce nadal niedostępna przez konektor (brak dostępnych kart); nie zastępuj testów funkcjonalnych deklaracją oceny wizualnej.

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
| Publikacja | GitHub Pages i workflow „Deploy M-SPAW preview”; strona i zasoby HTTP 200 | Opublikowano publiczny podgląd; formularz symuluje zgłoszenie bez transmisji danych, kalkulator demonstracyjny działa w przeglądarce |

Weryfikacja publikacji: 13 testów Python, kontrola składni JavaScript, budowa statycznego podglądu, udane wdrożenie Actions oraz HTTP 200 dla strony, CSS, obu skryptów, konfiguracji i demonstracyjnego cennika. Test `test_pages.py` porównuje wynik kalkulatora przeglądarkowego z serwerem dla wszystkich wariantów fikcyjnego cennika i kontroluje zawartość katalogu publikacji. Nie wykonano wizualnego przeglądu ani wysyłki wiadomości do firmy. Testy zapisu wykonują się w katalogach tymczasowych.

Teraz: podgląd lokalny i testy z przyciskiem „Wczytaj przykład demonstracyjny”. Następnie: kontrola w przeglądarce. Backlog przed obsługą prawdziwych klientów: rzeczywiste dane i stawki Macieja, podłączenie uzgodnionego odbioru zapytań, zdjęcia realizacji i publikacja do zatwierdzenia. Lokalny zapis testowy nie oznacza dostarczenia wiadomości do firmy.
