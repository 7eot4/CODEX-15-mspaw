"""Prepare only the static demonstration for GitHub Pages."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def build(target=None):
    target = Path(target) if target else ROOT / '_site'
    raw = (ROOT / 'pricing.json').read_bytes().replace(b'\r\n', b'\n')
    config = json.loads(raw)
    if config.get('mode') != 'demo' or config.get('demoEnabled') is not True or config.get('approved') is not False:
        raise ValueError('Pages publikuje wyłącznie jawny cennik demonstracyjny.')
    target.mkdir(parents=True, exist_ok=True)
    for name in ('index.html', 'style.css', 'app.js', 'demo-estimator.js'):
        shutil.copyfile(ROOT / 'dist' / name, target / name)
    assets = ('logo-mspaw.jpg', 'balustrada-wewnetrzna.jpg', 'balustrada-balkonowa.jpg',
              'brama-wjazdowa.jpg', 'balustrady-francuskie.jpg',
              'balustrady-zewnetrzne.jpg', 'balustrada-pionowa.jpg')
    (target / 'assets').mkdir(exist_ok=True)
    for name in assets:
        shutil.copyfile(ROOT / 'dist' / 'assets' / name, target / 'assets' / name)
    (target / 'demo-pricing.json').write_bytes(raw)
    (target / 'runtime.json').write_text(json.dumps({'mode': 'pages-demo', 'pricingRevision': hashlib.sha256(raw).hexdigest()[:16]}), encoding='utf-8')
    (target / '.nojekyll').write_text('', encoding='utf-8')
    return target

if __name__ == '__main__':
    print(build())
