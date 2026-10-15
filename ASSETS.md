# Oprawa wizualna — jasny projekt

## Aktualne materiały z Instagrama

Na polecenie użytkownika zastąpiono obrazy demonstracyjne w widocznej stronie rzeczywistymi materiałami M-SPAW:

- `dist/assets/logo-mspaw.jpg` — niezmieniona kopia logo dostarczonego przez użytkownika; białe marginesy kadrowane wyłącznie przez CSS.
- `dist/assets/balustrada-wewnetrzna.jpg`, `balustrada-balkonowa.jpg`, `brama-wjazdowa.jpg`, `balustrady-francuskie.jpg`, `balustrady-zewnetrzne.jpg`, `balustrada-pionowa.jpg` — sześć różnych zdjęć/postów z profilu `mspaw_uslugi`, wyodrębnionych bez modyfikacji z PDF zapisanego przez użytkownika. Nie usunięto logo ani oznaczeń firmy z fotografii. Powtórzone ujęcie balustrady wewnętrznej pominięto.

Dostęp do profilu przez zwykły HTTP zwrócił tytuł i opis profilu, lecz nie listę fotografii. Wykorzystano więc obrazy osadzone w lokalnym zapisie Instagrama, nie zrzut całej strony. PDF zawiera elementy interfejsu konta i nie jest publikowany ani śledzony w Git. Z PDF do publikacji trafiają wyłącznie wybrane obrazy realizacji. Pozyskane z treści firmowego posta dane kontaktowe: `538 792 159`, `firma.mspaw@gmail.com`.

Poprzednie obrazy AI opisane niżej pozostają historycznymi materiałami koncepcyjnymi; nie są już używane w stronie i nie trafiają do nowego artefaktu publikacji. `build_pages.py` kopiuje wyłącznie siedem wymienionych plików rzeczywistych materiałów.

Kierunek wybrany przez użytkownika: „Nowoczesne konstrukcje — jasna strona, minimalizm, eleganckie balustrady”. Ciepła biel, grafit, delikatna oliwkowa zieleń, typografia DM Sans. Zastąpiono poprzedni ciemny projekt i schemat SVG nową kompozycją. Formularz i cennik demonstracyjny zachowano.

Grafiki utworzono wbudowanym narzędziem ImageGen. Nie przedstawiają obiektów ani warsztatu firmy. Obie mają widoczne opisy na stronie. Docelowe pliki w projekcie:

- `dist/assets/architecture.png` — główna ilustracja nowoczesnej balustrady.
- `dist/assets/workshop.png` — ilustracja procesu w dalszej sekcji strony.
- `dist/assets/gate.png` — brama i furtka, przykład do galerii.
- `dist/assets/stairs.png` — schody stalowe z drewnianymi stopniami, przykład do galerii.

## Prompt: gate.png

Use case: photorealistic-natural. Asset type: conceptual project gallery image for a bright minimalist Polish steel fabrication website. High end editorial architecture photograph of a completed modern graphite steel driveway gate and matching pedestrian gate, horizontal metal slats with clean straight geometry, warm off-white plaster pillars and light limestone garden wall, contemporary European home slightly visible behind it, ornamental grasses and simple neat planting. Quiet premium residential architecture, warm bright natural daylight, soft shadows, charcoal metal and cream stone, restrained muted olive foliage. Landscape 3:2, no people, no vehicles, no text, no logos, no watermark. This is a fictional illustrative project, not a real business portfolio. Focus on elegant metal fabrication and believable correct gate structure.

## Prompt: stairs.png

Use case: photorealistic-natural. Asset type: conceptual project gallery image for a bright minimalist Polish steel fabrication website. Premium editorial interior architecture photograph showing a completed straight staircase with an elegant graphite steel stringer construction, warm pale oak treads and slim vertical graphite steel balustrade. Believable properly supported stairs, uniform step rise and run, railing firmly attached to steel construction. Contemporary European home interior with off-white plaster walls, pale limestone floor and natural daylight from a large side window. Quiet uncluttered warm minimalist design, cream and charcoal palette, fine steel and oak textures, soft shadows. Wide landscape 3:2 composition framing the whole stair flight with enough surrounding room. No people, no text, no logos, no watermark. Fictional architectural concept, not a real company's portfolio.

## Prompt: architecture.png

Use case: photorealistic-natural. Asset type: hero photograph for a bright minimalist Polish metal fabrication website. Primary request: elegant graphite steel balustrade with slim vertical bars, finely crafted modern straight lines, on a light limestone terrace beside a contemporary off-white house. Photography of architectural steel detail, not a web mockup. Scene: sunlit modern European home, pale warm plaster, natural limestone slabs, a glimpse of ornamental grasses and quiet garden. Composition: landscape 3:2, railing runs diagonally from near foreground right toward left background, sculptural structural geometry, beautifully straight slender bars with believable spacing and solid baseplates, calm composition, architecture editorial photography. Palette warm whites, creamy limestone, graphite metal, muted olive green. Soft bright natural morning light, gentle shadows, realistic fine materials. Premium architecture magazine look. No people, no welding, no text, no logos, no watermark. This is an illustrative concept image, not a company's actual portfolio.

## Prompt: workshop.png

Use case: photorealistic-natural. Asset type: wide cinematic background image for a premium Polish welding workshop website. Create a highly realistic editorial photograph of a welder working at a substantial steel fabrication table in an authentic tidy dark industrial workshop. Subject on the RIGHT HALF of the image, wearing fully enclosed dark welding helmet, protective leather welding gloves and a heavy dark protective jacket, holding a welding torch close to a real steel rectangular tube joint with a small bright blue-white arc and warm orange sparks. Natural steel textures, charcoal shadows, subtle atmospheric blue smoke, restrained warm amber lighting, believable tools and steel profiles in background. LEFT HALF must be very dark softly defocused negative space for big white website headline added later in code. Landscape 16:9 composition, professional industrial photography, cinematic but grounded, no logos, no text, no watermarks, no visible face, no exaggerated shower of sparks. This is illustrative imagery, not a real business portfolio.
