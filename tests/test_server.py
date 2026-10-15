import base64
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server

def sample():
    return dict(name='Test',email='test@example.com',phone='',description='Testowy opis balustrady.',location='Niedźwiedź',deadline='',type='balustrada',material='stal',finish='proszek',installation='tak',length='6.5',height='1.1',acknowledge='on',attachments=[])

class InquiryTests(unittest.TestCase):
    def test_persistence_and_attachment(self):
        with tempfile.TemporaryDirectory() as folder:
            previous = server.DATA
            try:
                server.DATA = Path(folder)
                payload = sample()
                payload['attachments'] = [{'name':'../../szkic.pdf','data':base64.b64encode(b'%PDF-1.4 test').decode()}]
                identifier = server.save_inquiry(payload)
                with closing(sqlite3.connect(server.DATA / 'inquiries.sqlite3')) as db:
                    self.assertEqual(json.loads(db.execute('select payload from inquiries where id=?',(identifier,)).fetchone()[0])['length'],6.5)
                    storage, original, content = db.execute('select storage_name,original_name,content from attachments').fetchone()
                    self.assertNotIn('/',storage)
                    self.assertEqual(content,b'%PDF-1.4 test')
            finally:
                server.DATA = previous

    def test_invalid_requests(self):
        for field, value in [('email','wrong'),('length','nan'),('height','100'),('description','krótki'),('type','other'),('acknowledge',''),('deadline','2020-01-01')]:
            with self.subTest(field=field):
                payload = sample(); payload[field]=value
                with self.assertRaises(ValueError): server.validate(payload)

    def test_files_rejected(self):
        for attachments in [[{'name':'x.svg','data':base64.b64encode(b'<svg/>').decode()}], [{}]*4]:
            payload=sample();payload['attachments']=attachments
            with self.assertRaises(ValueError):server.validate(payload)

if __name__ == '__main__': unittest.main()
