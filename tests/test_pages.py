import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import build_pages
import pricing
from test_pricing import specification

class PagesTests(unittest.TestCase):
    def test_artifact_and_browser_calculator(self):
        with tempfile.TemporaryDirectory() as folder:
            target = build_pages.build(folder)
            self.assertEqual({p.name for p in target.iterdir()}, {'index.html','style.css','app.js','demo-estimator.js','runtime.json','demo-pricing.json','.nojekyll','assets'})
            self.assertEqual({p.name for p in (target / 'assets').iterdir()}, {'architecture.png','workshop.png','gate.png','stairs.png'})
            self.assertIn('demo-estimator.js', (target / 'index.html').read_text(encoding='utf-8'))
            settings = json.loads((target / 'runtime.json').read_text())
            self.assertEqual(settings['mode'], 'pages-demo')
            # Exercise the exact shipped browser calculator against server results.
            cases = []
            config = json.loads((target / 'demo-pricing.json').read_text(encoding='utf-8'))
            for kind, materials in config['rates'].items():
                for material, finishes in materials.items():
                    for finish, mounts in finishes.items():
                        for mount in mounts:
                            cases.append(specification() | dict(type=kind, material=material, finish=finish, installation=mount))
            script = "const fs=require('fs'), calc=require('./dist/demo-estimator.js');const input=JSON.parse(fs.readFileSync(0,'utf8')); console.log(JSON.stringify(input.cases.map(p=>calc.calculate(p,input.config,input.revision))));"
            result = subprocess.run(['node','-e',script], cwd=build_pages.ROOT, input=json.dumps(dict(cases=cases, config=config, revision=settings['pricingRevision'])), text=True, capture_output=True, check=True)
            for spec, browser in zip(cases, json.loads(result.stdout)):
                server = pricing.estimate(spec)
                self.assertEqual((browser['min'], browser['max'], browser['revision']), (server['min'], server['max'], server['revision']))
                self.assertTrue(browser['demo'])

if __name__ == '__main__': unittest.main()
