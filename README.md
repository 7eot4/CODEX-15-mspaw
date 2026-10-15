# M-SPAW — Maciej Kowalczyk, Niedźwiedź

Lokalna wersja strony firmy spawalniczej. Cel: klient przekazuje komplet parametrów potrzebnych do oferty, a dla standardowych konstrukcji otrzymuje orientacyjny koszt po zatwierdzeniu cennika wykonawcy.

## Uruchomienie

Otwórz `START.cmd` (wymaga dostępnego Pythona 3.11+). Podgląd: http://127.0.0.1:8015. Okno serwera musi pozostać otwarte. Zatrzymanie: Ctrl+C w oknie serwera. Przy ponownym uruchomieniu nie uruchamiaj drugiej instancji, jeśli pierwsza nadal działa.

## Odczyt zapisanych zapytań

Otwórz `ODBIOR.cmd`. Program odczyta lokalną bazę i otworzy czytelny widok: opis, wymiary, kontakt klienta, zapisany szacunek z wersją cennika oraz pliki do pobrania. Nowe zgłoszenia pojawią się po ponownym uruchomieniu tego pliku. Nie potrzeba działającego serwera strony.

Widok zapisuje się w `.local/inbox/index.html`, a kopie załączników w `.local/inbox/files/`. Te pliki zawierają dane zapytań, pozostają poza serwowanym katalogiem `dist` i są wykluczone z Git. Odczyt nie zmienia bazy. Nie ma publicznego adresu listy zgłoszeń. Jest to lokalny odbiór testów, nie skrzynka Macieja na innym komputerze. Zakończenie i retencję danych, w tym kopii w tym widoku, trzeba ustalić przed obsługą rzeczywistych klientów.

## Aktualny stan

- Strona dostosowana do telefonów i komputerów, autorska ilustracja konstrukcji stalowej, wybór rodzaju zlecenia, opis procesu i FAQ.
- Formularz z parametrami, danymi kontaktowymi, terminem oraz maksymalnie 3 załącznikami po 5 MB. Serwer sprawdza dane i podstawową sygnaturę pliku. Nie jest to skaner bezpieczeństwa ani parser dokumentacji.
- Zapytania i załączniki zapisują się transakcyjnie w `.local/inquiries.sqlite3`. Dane nie są dostępne przez statyczny serwer i są wyłączone z Git. Brak wysyłki e-mail oraz powiadomień. Formularz wyraźnie opisuje lokalny tryb testowy; używaj danych testowych.
- Można pobrać opis zapytania jako TXT. Załączniki trzeba wtedy przekazać osobno. Pobranie nie oznacza wysłania.
- Na prośbę użytkownika włączono demonstracyjny cennik: `mode: demo`, `demoEnabled: true`, `approved: false`. Są to fikcyjne ceny, nie zatwierdzona oferta firmy. W formularzu przycisk „Wczytaj przykład demonstracyjny” uzupełnia fikcyjne dane klienta i balustradę 6,5 × 1,1 m; wynik to 4700–6330 PLN brutto (wyłącznie przykład). Dane kontaktowe do oceny układu: `000 000 000`, `mspaw@example.com`; nie uruchamiają połączenia ani wysyłki. Nie dodano fikcyjnych opinii, certyfikatów ani zdjęć cudzych realizacji.
- Dane potwierdzone przez użytkownika: Maciej Kowalczyk, Niedźwiedź. Instagram i Google pochodzą od użytkownika. Dokładny zakres usług i materiałów jest propozycją do potwierdzenia.
- Strona nieopublikowana, brak zewnętrznego repozytorium. `noindex` obowiązuje dla podglądu.

## Konfiguracja wyceny

Zatwierdzenie stawek wymaga danych od Macieja. Struktura: `rates[rodzaj][material][wykonczenie][montaz]`. Każdy końcowy obiekt ma `min`, `max` (PLN brutto / m), `fixed` (stała kwota PLN brutto), `minHeight`, `maxHeight`, `minLength`, `maxLength` (zakresy wymiarów w metrach) oraz `scope` (opis założeń, minimum 15 znaków: m.in. przekroje, wypełnienie, zakres montażu). Dozwolone klucze odpowiadają wartościom formularza. Następnie `approved: true` (wartość logiczna). Bez dokładnie dopasowanego wariantu nadal obowiązuje wycena indywidualna. Dotyczy tylko balustrad i ogrodzeń; naprawy i konstrukcje nietypowe wymagają oceny. Transport nie jest automatycznie liczony. Wynik to długość × stawka + kwota stała, zaokrąglony do 10 PLN; połowa kroku zaokrąglana jest w górę.

Wycena jest liczona na serwerze przez `POST /api/estimate`. Przeglądarka przesyła tylko parametry konstrukcji, bez danych kontaktowych. Przy zapisie zapytania serwer ponownie liczy wynik z bieżącego cennika, ignoruje cenę dostarczoną przez klienta i zachowuje wynik, parametry, opis zakresu oraz identyfikator wersji cennika w rekordzie zapytania. Wynik jest szacunkiem, nie ofertą wiążącą. Wadliwy lub niedostępny cennik nie generuje ceny; niezatwierdzone stawki są dostępne wyłącznie w wyraźnie włączonym trybie demonstracyjnym. Wynik demonstracyjny ma zapisane `demo: true`, ostrzeżenie i identyfikator cennika, widoczne również w pobranym opisie i lokalnym odbiorze. Zmiana parametrów usuwa poprzedni wynik do czasu otrzymania nowego; spóźnione odpowiedzi są ignorowane. Aby przejść do rzeczywistych cen, należy zastąpić stawki, zatwierdzić je i wyłączyć tryb demo — nie wystarczy zmienić samą etykietę na stronie.

## Weryfikacja

`python -m unittest discover -s tests -v` — zapis zapytania z załącznikiem, odczyt bazy, walidacja pól, dat i wymiarów, odrzucanie niewłaściwych plików; obliczenia i zaokrąglenia, zakresy cennika, niezatwierdzone i wadliwe reguły. Test HTTP uruchamia serwer na losowym lokalnym porcie i potwierdza, że zapisana wycena ignoruje cenę podmienioną w zapytaniu klienta. Dane testowe i cennik powstają w katalogach tymczasowych.

`node --check dist/app.js` — składnia JavaScript.

Weryfikacja HTTP: strona, pliki CSS/JS i odpowiedzi walidacji API; po przeniesieniu obliczeń także wycena i jej zapis w bazie przez rzeczywiste żądania HTTP w teście integracyjnym. Kontrola wizualna w przeglądarce pozostaje do wykonania: dostępny konektor Chrome nie pozwolił otworzyć karty, a przeglądarka w aplikacji jest niedostępna. Układ telefonu nie jest jeszcze potwierdzony wizualnie.

## Dalej

Teraz: lokalna prezentacja z fikcyjnymi danymi i działającą wyceną demonstracyjną. Następnie: kontrola wyglądu i ścieżki zapytania. Backlog przed uruchomieniem dla klientów: rzeczywiste dane, zatwierdzone stawki i usługi, dostawa zapytań i załączników, obsługa błędów dostawy, ochrona antyspamowa, informacja o danych i retencji, testy przeglądarkowe oraz wybór hostingu. Lokalny serwer standardowej biblioteki Pythona nie służy do publicznego wdrożenia. Publikacja i wysyłka danych poza komputer wymagają potwierdzenia użytkownika.
