# M-SPAW — Maciej Kowalczyk, Niedźwiedź

Lokalna wersja strony firmy spawalniczej. Cel: klient przekazuje komplet parametrów potrzebnych do oferty, a dla standardowych konstrukcji otrzymuje orientacyjny koszt po zatwierdzeniu cennika wykonawcy.

## Uruchomienie

Otwórz `START.cmd` (wymaga dostępnego Pythona 3.11+). Podgląd: http://127.0.0.1:8015. Okno serwera musi pozostać otwarte. Zatrzymanie: Ctrl+C w oknie serwera. Przy ponownym uruchomieniu nie uruchamiaj drugiej instancji, jeśli pierwsza nadal działa.

## Aktualny stan

- Strona dostosowana do telefonów i komputerów, autorska ilustracja konstrukcji stalowej, wybór rodzaju zlecenia, opis procesu i FAQ.
- Formularz z parametrami, danymi kontaktowymi, terminem oraz maksymalnie 3 załącznikami po 5 MB. Serwer sprawdza dane i podstawową sygnaturę pliku. Nie jest to skaner bezpieczeństwa ani parser dokumentacji.
- Zapytania i załączniki zapisują się transakcyjnie w `.local/inquiries.sqlite3`. Dane nie są dostępne przez statyczny serwer i są wyłączone z Git. Brak wysyłki e-mail oraz powiadomień. Formularz wyraźnie opisuje lokalny tryb testowy; używaj danych testowych.
- Można pobrać opis zapytania jako TXT. Załączniki trzeba wtedy przekazać osobno. Pobranie nie oznacza wysłania.
- Nie ma zatwierdzonych cen: `pricing.json` zawiera `approved: false`. Kalkulator wyświetla „Wycena indywidualna”. Nie użyto wymyślonych cen, opinii, certyfikatów ani zdjęć cudzych realizacji.
- Dane potwierdzone przez użytkownika: Maciej Kowalczyk, Niedźwiedź. Instagram i Google pochodzą od użytkownika. Dokładny zakres usług i materiałów jest propozycją do potwierdzenia.
- Strona nieopublikowana, brak zewnętrznego repozytorium. `noindex` obowiązuje dla podglądu.

## Konfiguracja wyceny

Zatwierdzenie stawek wymaga danych od Macieja. Struktura: `rates[rodzaj][material][wykonczenie][montaz]`. Każdy końcowy obiekt ma `min`, `max` (PLN brutto / m), `fixed` (stała kwota PLN brutto), `minHeight`, `maxHeight`, `minLength`, `maxLength` (zakresy wymiarów w metrach) oraz `scope` (opis założeń, minimum 15 znaków: m.in. przekroje, wypełnienie, zakres montażu). Dozwolone klucze odpowiadają wartościom formularza. Następnie `approved: true` (wartość logiczna). Bez dokładnie dopasowanego wariantu nadal obowiązuje wycena indywidualna. Dotyczy tylko balustrad i ogrodzeń; naprawy i konstrukcje nietypowe wymagają oceny. Transport nie jest automatycznie liczony. Wynik to długość × stawka + kwota stała, zaokrąglony do 10 PLN; połowa kroku zaokrąglana jest w górę.

Wycena jest liczona na serwerze przez `POST /api/estimate`. Przeglądarka przesyła tylko parametry konstrukcji, bez danych kontaktowych. Przy zapisie zapytania serwer ponownie liczy wynik z bieżącego cennika, ignoruje cenę dostarczoną przez klienta i zachowuje wynik, parametry, opis zakresu oraz identyfikator wersji cennika w rekordzie zapytania. Wynik jest szacunkiem, nie ofertą wiążącą. Wadliwy, niedostępny lub niezatwierdzony cennik nie generuje ceny. Zmiana parametrów usuwa poprzedni wynik do czasu otrzymania nowego; spóźnione odpowiedzi są ignorowane. Cennik produkcyjny pozostaje pusty; syntetyczne ceny występują wyłącznie w testach.

## Weryfikacja

`python -m unittest discover -s tests -v` — zapis zapytania z załącznikiem, odczyt bazy, walidacja pól, dat i wymiarów, odrzucanie niewłaściwych plików; obliczenia i zaokrąglenia, zakresy cennika, niezatwierdzone i wadliwe reguły. Test HTTP uruchamia serwer na losowym lokalnym porcie i potwierdza, że zapisana wycena ignoruje cenę podmienioną w zapytaniu klienta. Dane testowe i cennik powstają w katalogach tymczasowych.

`node --check dist/app.js` — składnia JavaScript.

Weryfikacja HTTP: strona, pliki CSS/JS i odpowiedzi walidacji API; po przeniesieniu obliczeń także wycena i jej zapis w bazie przez rzeczywiste żądania HTTP w teście integracyjnym. Kontrola wizualna w przeglądarce pozostaje do wykonania: dostępny konektor Chrome nie pozwolił otworzyć karty, a przeglądarka w aplikacji jest niedostępna. Układ telefonu nie jest jeszcze potwierdzony wizualnie.

## Dalej

Teraz: lokalny przegląd wyglądu i ścieżki zapytania. Następnie: telefon, e-mail, zatwierdzenie oferty i stawek oraz własne zdjęcia Macieja. Backlog przed publikacją: rzeczywista dostawa zapytań i załączników, obsługa błędów dostawy, ochrona antyspamowa, docelowa informacja o danych i retencji, testy przeglądarkowe oraz wybór hostingu. Lokalny serwer standardowej biblioteki Pythona nie służy do publicznego wdrożenia. Publikacja i wysyłka danych poza komputer wymagają potwierdzenia użytkownika.
