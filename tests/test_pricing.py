import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pricing

def specification():
    return dict(type='balustrada', material='stal', finish='proszek', installation='tak', length='6.5', height='1.1')

def fixture():
    # Synthetic test inputs only. These numbers are not M-SPAW prices.
    rule = dict(min=100, max=150, fixed=55, minHeight=1, maxHeight=1.2,
                minLength=2, maxLength=10, scope='Testowy zakres: prosty odcinek, wypełnienie profilowe.')
    return dict(approved=True, rates={'balustrada': {'stal': {'proszek': {'tak': rule}}}})

class PricingTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = Path(self.folder.name) / 'pricing.json'
        self.override = patch.object(pricing, 'CONFIG', self.path)
        self.override.start()

    def tearDown(self):
        self.override.stop()
        self.folder.cleanup()

    def write_config(self, config):
        self.path.write_text(json.dumps(config), encoding='utf-8')

    def test_calculation_and_recorded_revision(self):
        self.write_config(fixture())
        result = pricing.estimate(specification())
        self.assertEqual((result['min'], result['max']), (710, 1030))
        self.assertEqual(result['tax'], 'gross')
        self.assertEqual(result['parameters']['length'], 6.5)
        self.assertEqual(len(result['revision']), 16)
        config = fixture(); config['rates']['balustrada']['stal']['proszek']['tak']['min'] = 120
        self.write_config(config)
        self.assertNotEqual(pricing.estimate(specification())['revision'], result['revision'])

    def test_unapproved_and_missing_variants_never_receive_prices(self):
        config = fixture(); config['approved'] = False; self.write_config(config)
        self.assertEqual(pricing.estimate(specification())['reason'], 'unapproved')
        config['approved'] = 'true'; self.write_config(config)
        self.assertNotIn('min', pricing.estimate(specification()))
        self.write_config(fixture())
        for change in [dict(type='naprawa'), dict(type='konstrukcja'), dict(material='nie-wiem'), dict(length=''), dict(height='2'), dict(length='20')]:
            with self.subTest(change=change):
                self.assertNotIn('min', pricing.estimate(specification() | change))

    def test_bad_config_fails_closed(self):
        for changes in [dict(min=-1), dict(max=1), dict(scope=''), dict(fixed='NaN'), dict(minLength=1000)]:
            config = fixture(); config['rates']['balustrada']['stal']['proszek']['tak'].update(changes)
            self.write_config(config)
            self.assertEqual(pricing.estimate(specification())['reason'], 'unavailable')
        self.path.write_text('{broken', encoding='utf-8')
        self.assertEqual(pricing.estimate(specification())['reason'], 'unavailable')

    def test_demo_never_implies_owner_approval(self):
        config = fixture() | {'approved': False, 'mode': 'demo', 'demoEnabled': True}
        self.write_config(config)
        result = pricing.estimate(specification())
        self.assertTrue(result['demo'])
        self.assertIn('fikcyjne', result['message'])
        config['demoEnabled'] = False
        self.write_config(config)
        self.assertEqual(pricing.estimate(specification())['reason'], 'unapproved')

    def test_shipped_demo_configuration(self):
        with patch.object(pricing, 'CONFIG', Path(pricing.__file__).with_name('pricing.json')):
            result = pricing.estimate(specification())
            self.assertEqual((result['min'], result['max']), (4700, 6330))
            self.assertTrue(result['demo'])
            self.assertIn('fikcyjne', result['message'])

    def test_bad_dimensions_rejected(self):
        for invalid in ('NaN', 'Infinity', '-1', '201', True, [], {}):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    pricing.estimate(specification() | dict(length=invalid))

if __name__ == '__main__': unittest.main()
