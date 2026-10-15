"""Informational estimates from approved workshop rates; never client-supplied prices."""
import hashlib
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

CONFIG = Path(__file__).with_name('pricing.json')
CHOICES = {
    'type': ('balustrada', 'ogrodzenie', 'konstrukcja', 'naprawa'),
    'material': ('nie-wiem', 'stal', 'nierdzewna', 'aluminium'),
    'finish': ('do-ustalenia', 'surowe', 'proszek', 'ocynk'),
    'installation': ('do-ustalenia', 'tak', 'nie'),
}

def number(value, minimum, maximum):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError('Nieprawidłowa liczba.')
    try:
        result = Decimal(str(value))
        if not result.is_finite() or not Decimal(str(minimum)) <= result <= Decimal(str(maximum)):
            raise ValueError('Liczba poza zakresem.')
        return result
    except InvalidOperation:
        raise ValueError('Nieprawidłowa liczba.') from None

def parameters(payload):
    if not isinstance(payload, dict):
        raise ValueError('Nieprawidłowy format parametrów.')
    clean = {}
    for key, allowed in CHOICES.items():
        if payload.get(key) not in allowed:
            raise ValueError('Nieprawidłowy wybór: ' + key)
        clean[key] = payload[key]
    for key, maximum in [('length', 200), ('height', 10)]:
        value = payload.get(key, '')
        clean[key] = None if value in ('', None) else float(number(value, '.1', maximum))
    return clean

def estimate(payload):
    clean = parameters(payload)
    def individual(reason, message):
        return dict(status='individual', reason=reason, message=message, parameters=clean)

    if clean['type'] in ('konstrukcja', 'naprawa'):
        return individual('assessment', 'Ta praca wymaga indywidualnej oceny wykonawcy na podstawie opisu i zdjęć.')
    try:
        raw = CONFIG.read_bytes()
        config = json.loads(raw)
        if not isinstance(config, dict) or config.get('approved') is not True:
            return individual('unapproved', 'Cennik Macieja nie jest jeszcze zatwierdzony. Przygotuj parametry do indywidualnej oferty.')
        rate = config.get('rates', {})
        for key in ('type', 'material', 'finish', 'installation'):
            rate = rate.get(clean[key]) if isinstance(rate, dict) else None
        if rate is None:
            return individual('variant', 'Ten wariant nie ma zatwierdzonej stawki. Maciej wyceni go indywidualnie.')
        if not isinstance(rate, dict):
            raise ValueError('Nieprawidłowa reguła cenowa.')
        low = number(rate.get('min'), '.01', 1000000)
        high = number(rate.get('max'), low, 1000000)
        fixed = number(rate.get('fixed'), 0, 1000000)
        min_height = number(rate.get('minHeight'), '.1', 10)
        max_height = number(rate.get('maxHeight'), min_height, 10)
        min_length = number(rate.get('minLength'), '.1', 200)
        max_length = number(rate.get('maxLength'), min_length, 200)
        scope = rate.get('scope')
        if not isinstance(scope, str) or not 15 <= len(scope.strip()) <= 1500:
            raise ValueError('Brak zatwierdzonego zakresu.')
        if clean['length'] is None or clean['height'] is None:
            return individual('dimensions', 'Podaj długość i wysokość, aby sprawdzić dostępność wyceny automatycznej.')
        length, height = Decimal(str(clean['length'])), Decimal(str(clean['height']))
        if not (min_length <= length <= max_length and min_height <= height <= max_height):
            return individual('dimensions', 'Wymiary wykraczają poza zatwierdzony wariant. Potrzebna jest wycena indywidualna.')
        def rounded(value):
            return int((value / 10).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * 10)
        return dict(status='estimated', min=rounded(length * low + fixed),
                    max=rounded(length * high + fixed), currency='PLN', tax='gross',
                    revision=hashlib.sha256(raw).hexdigest()[:16], scope=scope.strip(),
                    parameters=clean, message='Szacunek brutto, nie oferta końcowa. Transport i nietypowe warunki wymagają osobnej oceny. Cenę potwierdza Maciej.')
    except (OSError, ValueError, TypeError):
        return individual('unavailable', 'Wycena automatyczna jest chwilowo niedostępna. Możesz przygotować zapytanie do indywidualnej oferty.')
