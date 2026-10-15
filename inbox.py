"""Read local inquiries into an owner-only HTML file, outside the served directory."""
import argparse
import html
import json
import re
import sqlite3
import webbrowser
from contextlib import closing
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABELS = {
    'name': 'Imię', 'email': 'E-mail', 'phone': 'Telefon', 'location': 'Miejscowość',
    'deadline': 'Preferowany termin', 'type': 'Rodzaj pracy', 'material': 'Materiał',
    'length': 'Długość [m]', 'height': 'Wysokość [m]', 'finish': 'Wykończenie',
    'installation': 'Montaż',
}
VALUES = {
    'balustrada': 'Balustrada', 'ogrodzenie': 'Ogrodzenie', 'konstrukcja': 'Własna konstrukcja',
    'naprawa': 'Naprawa', 'stal': 'Stal węglowa', 'nierdzewna': 'Stal nierdzewna',
    'aluminium': 'Aluminium', 'nie-wiem': 'Do doboru', 'do-ustalenia': 'Do ustalenia',
    'surowe': 'Bez powłoki', 'proszek': 'Malowanie proszkowe', 'ocynk': 'Ocynk',
    'tak': 'Z montażem', 'nie': 'Bez montażu',
}

def escape(value):
    return html.escape(str(value), quote=True)

def render_inbox(data_dir):
    data_dir = Path(data_dir)
    database = data_dir / 'inquiries.sqlite3'
    output = data_dir / 'inbox'
    output.mkdir(parents=True, exist_ok=True)
    items = []
    if database.exists():
        with closing(sqlite3.connect(database.resolve().as_uri() + '?mode=ro', uri=True)) as db:
            for identifier, created, raw in db.execute('SELECT id, created, payload FROM inquiries ORDER BY created DESC, id DESC'):
                payload = json.loads(raw)
                fields = []
                for key, label in LABELS.items():
                    value = payload.get(key)
                    display = 'Do ustalenia' if value is None or value == '' else VALUES.get(str(value), value) if key in ('type','material','finish','installation') else value
                    fields.append(f'<dt>{escape(label)}</dt><dd>{escape(display)}</dd>')
                attachments = []
                for storage, original, content in db.execute('SELECT storage_name, original_name, content FROM attachments WHERE inquiry_id=?', (identifier,)):
                    if not re.fullmatch(r'[a-f0-9]{32}\.(jpg|png|webp|pdf)', storage):
                        raise ValueError('Nieprawidłowa nazwa zapisanego załącznika.')
                    directory = output / 'files'
                    directory.mkdir(exist_ok=True)
                    (directory / storage).write_bytes(content)
                    attachments.append(f'<li><a href="files/{storage}" download>{escape(original)}</a> · {len(content):,} B</li>')
                estimate = payload.get('estimate', {})
                if estimate.get('status') == 'estimated':
                    pricing = f"{escape(estimate.get('min'))}–{escape(estimate.get('max'))} PLN brutto"
                    pricing += f"<p>Wersja cennika: {escape(estimate.get('revision', ''))}</p><p>{escape(estimate.get('scope', ''))}</p>"
                else:
                    pricing = 'Wycena indywidualna'
                message = escape(estimate.get('message', 'Brak zapisanego szacunku w starszym zapytaniu.'))
                items.append(f'''<article><p class="reference">Zapytanie {escape(identifier)} · {escape(created)}</p>
<h2>{escape(payload.get('name',''))} / {escape(payload.get('location',''))}</h2>
<dl>{''.join(fields)}</dl><h3>Opis</h3><p class="description">{escape(payload.get('description',''))}</p>
<h3>Zapisany szacunek</h3><div>{pricing}</div><p>{message}</p>
<h3>Załączniki ({len(attachments)})</h3><ul>{''.join(attachments) or '<li>Brak załączników</li>'}</ul></article>''')
    empty = '<p class="empty">Brak lokalnych zapytań. Zapisz zapytanie testowe na stronie i ponownie uruchom ODBIOR.cmd.</p>'
    document = f'''<!doctype html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>M-SPAW — lokalne zapytania</title><style>
body{{font:15px/1.6 Arial,sans-serif;background:#ecece5;color:#192023;max-width:1050px;margin:auto;padding:35px 20px}}
h1{{font-size:32px}}h2{{font-size:24px}}h3{{margin-bottom:6px;font-size:16px}}article{{background:white;padding:25px;margin:22px 0;border-top:4px solid #b74f24}}
.notice,.empty{{padding:18px;background:#fff4e8}}.reference{{font-size:11px;overflow-wrap:anywhere;color:#536166}}
dl{{display:grid;grid-template-columns:180px 1fr;gap:8px 20px}}dt{{font-weight:bold}}dd{{margin:0;overflow-wrap:anywhere}}
.description{{white-space:pre-wrap;overflow-wrap:anywhere}}a{{color:#873c1b}}li{{overflow-wrap:anywhere}}
@media(max-width:550px){{dl{{grid-template-columns:1fr;gap:3px}}dd{{margin-bottom:10px}}article{{padding:18px}}}}
</style></head><body><h1>M-SPAW / Zapytania lokalne</h1>
<p class="notice">Tylko dane z tego komputera. Te zapytania nie zostały wysłane do Macieja. Widok zawiera dane kontaktowe i załączniki; znajduje się poza katalogiem strony.</p>
<p>Liczba zapytań: {len(items)}. Wygenerowano: {escape(datetime.now().astimezone().isoformat(timespec='seconds'))}. Aby wczytać nowe zgłoszenia, uruchom ponownie ODBIOR.cmd.</p>
{''.join(items) or empty}</body></html>'''
    target = output / 'index.html'
    target.write_text(document, encoding='utf-8')
    return target

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lokalny odbiór zapytań M-SPAW')
    parser.add_argument('--open', action='store_true', help='Otwórz wygenerowany plik w domyślnej przeglądarce')
    args = parser.parse_args()
    try:
        target = render_inbox(ROOT / '.local')
    except (OSError, sqlite3.Error, ValueError) as error:
        raise SystemExit(f'Nie utworzono widoku zapytań: {error}')
    print(target)
    if args.open:
        webbrowser.open(target.as_uri())
