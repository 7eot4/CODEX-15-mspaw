"""Local preview and inquiry inbox. Bind only to loopback; not a production server."""
import base64
import binascii
import json
import re
import sqlite3
import uuid
from contextlib import closing
from datetime import date, datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from pricing import parameters, estimate

ROOT = Path(__file__).resolve().parent
DATA = ROOT / '.local'
MAX_BODY = 22 * 1024 * 1024

def validate(payload):
    if not isinstance(payload, dict):
        raise ValueError('Nieprawidłowy format zapytania.')
    clean = {}
    for key, limit in [('name',100), ('email',200), ('phone',30), ('description',4000), ('location',100), ('deadline',10)]:
        value = payload.get(key, '')
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError('Nieprawidłowe pole: ' + key)
        clean[key] = value.strip()
    if not clean['name'] or not clean['location'] or len(clean['description']) < 15:
        raise ValueError('Uzupełnij imię, miejscowość i opis (minimum 15 znaków).')
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', clean['email']):
        raise ValueError('Podaj poprawny e-mail.')
    if payload.get('acknowledge') != 'on':
        raise ValueError('Potwierdź lokalny tryb testowy.')
    if clean['deadline']:
        try:
            if date.fromisoformat(clean['deadline']) < date.today():
                raise ValueError()
        except ValueError:
            raise ValueError('Podaj termin dzisiejszy lub przyszły.')
    clean.update(parameters(payload))
    attachments = payload.get('attachments', [])
    if not isinstance(attachments, list) or len(attachments) > 3:
        raise ValueError('Maksymalnie 3 załączniki.')
    decoded = []
    for item in attachments:
        if not isinstance(item, dict) or not isinstance(item.get('name'),str) or len(item['name']) > 200:
            raise ValueError('Nieprawidłowy załącznik.')
        try:
            blob = base64.b64decode(item['data'], validate=True)
        except (KeyError, TypeError, ValueError, binascii.Error):
            raise ValueError('Nieprawidłowe dane załącznika.')
        if not 0 < len(blob) <= 5 * 1024 * 1024:
            raise ValueError('Plik przekracza 5 MB lub jest pusty.')
        ext = None
        if blob.startswith(b'\xff\xd8\xff'): ext = '.jpg'
        elif blob.startswith(b'\x89PNG\r\n\x1a\n'): ext = '.png'
        elif blob.startswith(b'%PDF-'): ext = '.pdf'
        elif blob.startswith(b'RIFF') and blob[8:12] == b'WEBP': ext = '.webp'
        if not ext:
            raise ValueError('Dozwolone są JPG, PNG, WEBP i PDF.')
        decoded.append((uuid.uuid4().hex + ext, item['name'], blob))
    return clean, decoded

def save_inquiry(payload):
    clean, files = validate(payload)
    clean['estimate'] = estimate(clean)
    inquiry_id = uuid.uuid4().hex
    DATA.mkdir(exist_ok=True)
    with closing(sqlite3.connect(DATA / 'inquiries.sqlite3')) as db, db:
        db.execute('CREATE TABLE IF NOT EXISTS inquiries (id TEXT PRIMARY KEY, created TEXT, payload TEXT)')
        db.execute('CREATE TABLE IF NOT EXISTS attachments (inquiry_id TEXT, storage_name TEXT, original_name TEXT, content BLOB)')
        db.execute('INSERT INTO inquiries VALUES (?,?,?)', (inquiry_id, datetime.now(timezone.utc).isoformat(), json.dumps(clean, ensure_ascii=False)))
        db.executemany('INSERT INTO attachments VALUES (?,?,?,?)', [(inquiry_id,*f) for f in files])
    return inquiry_id

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'dist'), **kwargs)

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def reply(self, code, body):
        content = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if self.path.startswith('/api/'):
            return self.reply(404, {'error':'Nie znaleziono.'})
        super().do_GET()

    def do_POST(self):
        if self.path not in ('/api/inquiries', '/api/estimate'):
            return self.reply(404, {'error':'Nie znaleziono.'})
        origin = self.headers.get('Origin')
        if origin and origin not in (f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}'):
            return self.reply(403, {'error':'Niedozwolone źródło.'})
        if self.headers.get_content_type() != 'application/json':
            return self.reply(415, {'error':'Wymagany JSON.'})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            limit = 64 * 1024 if self.path == '/api/estimate' else MAX_BODY
            if not 0 < size <= limit:
                return self.reply(413, {'error':'Zapytanie zbyt duże lub puste.'})
            payload = json.loads(self.rfile.read(size))
            if self.path == '/api/estimate':
                return self.reply(200, estimate(payload))
            identifier = save_inquiry(payload)
        except (ValueError, TypeError, UnicodeError) as error:
            return self.reply(400, {'error':str(error)})
        self.reply(201, {'id':identifier, 'delivery':'local-only'})

if __name__ == '__main__':
    print('M-SPAW — lokalny podgląd: http://127.0.0.1:8015', flush=True)
    ThreadingHTTPServer(('127.0.0.1',8015),Handler).serve_forever()
