import base64
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch
import inbox
import server
from test_server import sample

class InboxTests(unittest.TestCase):
    def test_empty_inbox_does_not_create_database(self):
        with tempfile.TemporaryDirectory() as folder:
            target = inbox.render_inbox(folder)
            self.assertIn('Brak lokalnych zapytań', target.read_text(encoding='utf-8'))
            self.assertFalse((Path(folder) / 'inquiries.sqlite3').exists())

    def test_saved_request_is_readable_and_untrusted_content_is_escaped(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(server, 'DATA', Path(folder)):
            payload = sample() | {'name': '<script>alert(1)</script>', 'description': 'Pierwsza linia\nDruga linia: balustrada.'}
            file_content = b'%PDF-1.4 test only'
            payload['attachments'] = [{'name': '../../szkic<&>.pdf', 'data': base64.b64encode(file_content).decode()}]
            identifier = server.save_inquiry(payload)
            target = inbox.render_inbox(folder)
            document = target.read_text(encoding='utf-8')
            self.assertIn(identifier, document)
            self.assertIn('&lt;script&gt;', document)
            self.assertNotIn('<script>', document)
            self.assertIn('Pierwsza linia\nDruga linia', document)
            self.assertIn('Malowanie proszkowe', document)
            self.assertIn('DEMO — fikcyjna wycena', document)
            files = list((target.parent / 'files').iterdir())
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].read_bytes(), file_content)
            with closing(sqlite3.connect(Path(folder) / 'inquiries.sqlite3')) as db:
                self.assertEqual(db.execute('SELECT COUNT(*) FROM inquiries').fetchone()[0], 1)

if __name__ == '__main__': unittest.main()
