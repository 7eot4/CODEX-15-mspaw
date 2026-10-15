import json
import sqlite3
import tempfile
import threading
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import pricing
import server
from test_server import sample
from test_pricing import fixture, specification

class HTTPTests(unittest.TestCase):
    def test_estimate_and_saved_inquiry_use_server_prices(self):
        with tempfile.TemporaryDirectory() as folder:
            config_path = Path(folder) / 'prices.json'
            config_path.write_text(json.dumps(fixture()), encoding='utf-8')
            with patch.object(pricing, 'CONFIG', config_path), patch.object(server, 'DATA', Path(folder)):
                httpd = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
                thread = threading.Thread(target=httpd.serve_forever, daemon=True)
                thread.start()
                try:
                    base = f'http://127.0.0.1:{httpd.server_port}'
                    def post(path, body, origin=None):
                        headers = {'Content-Type': 'application/json'}
                        if origin: headers['Origin'] = origin
                        request = Request(base + path, data=json.dumps(body).encode(), headers=headers)
                        with urlopen(request, timeout=5) as response:
                            return response.status, json.load(response)
                    code, result = post('/api/estimate', specification())
                    self.assertEqual(code, 200)
                    self.assertEqual(result['min'], 710)
                    code, saved = post('/api/inquiries', sample() | {'estimate': {'min': 1, 'max': 1}})
                    self.assertEqual(code, 201)
                    with closing(sqlite3.connect(Path(folder) / 'inquiries.sqlite3')) as db:
                        payload = json.loads(db.execute('SELECT payload FROM inquiries WHERE id=?', (saved['id'],)).fetchone()[0])
                        self.assertEqual(payload['estimate'], result)
                    with self.assertRaises(HTTPError) as failure:
                        post('/api/estimate', specification() | {'length': 'NaN'})
                    self.assertEqual(failure.exception.code, 400)
                    failure.exception.close()
                    with self.assertRaises(HTTPError) as failure:
                        post('/api/inquiries', sample(), 'https://unrelated.example')
                    self.assertEqual(failure.exception.code, 403)
                    failure.exception.close()
                finally:
                    httpd.shutdown(); httpd.server_close(); thread.join(timeout=5)

if __name__ == '__main__': unittest.main()
