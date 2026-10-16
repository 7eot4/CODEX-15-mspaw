# M-SPAW — zasady aktualizacji

- Użytkownik zlecił publikację podglądu na GitHub oraz aktualizowanie repozytorium przy kolejnych zmianach tej strony. W ramach tego zakresu wykonuj adekwatne testy, commit, push i kontrolę wdrożenia; nie pozostawiaj gotowych zmian wyłącznie lokalnie.
- Repozytorium: `7eot4/mspaw`, gałąź `main`. Podgląd: https://7eot4.github.io/mspaw/ .
- Publikowany katalog `_site` powstaje przez `python build_pages.py`. GitHub Actions testuje i publikuje go po push do `main`.
- GitHub Pages to demonstracja: fikcyjny cennik i kontakt, obliczenia w przeglądarce, symulacja zapytania. Nie przedstawiaj symulacji jako wysłania do firmy. Rzeczywisty odbiór zapytań wymaga odrębnego podłączenia.
- `.local`, baza zapytań, eksport odbioru, dane klientów i załączniki nigdy nie trafiają do Git ani do artefaktu Pages. Zachowaj ich wykluczenia.
- Przed push: testy Python, kontrola składni JavaScript i budowa Pages. Po push: zgodność lokalnego i zdalnego SHA, wynik wdrożenia dla tego SHA oraz dostępność strony i jej zasobów.
