(function (root) {
  function calculate(values, config, revision) {
    const individual = message => ({ status: 'individual', demo: true, message });
    if (config.mode !== 'demo' || config.demoEnabled !== true) throw Error('Brak cennika demonstracyjnego.');
    if (!['balustrada', 'ogrodzenie'].includes(values.type)) return individual('Ta praca wymaga indywidualnej oceny. W podglądzie możesz przygotować opis zapytania.');
    const rate = config.rates?.[values.type]?.[values.material]?.[values.finish]?.[values.installation];
    if (!rate) return individual('Wybierz materiał, wykończenie i montaż albo wczytaj gotowy przykład. Ten wariant wymaga indywidualnej wyceny.');
    const length = Number(values.length), height = Number(values.height);
    if (!Number.isFinite(length) || !Number.isFinite(height) || length < rate.minLength || length > rate.maxLength || height < rate.minHeight || height > rate.maxHeight) return individual('Podaj wymiary mieszczące się w przykładowym wariancie lub przygotuj zapytanie indywidualne.');
    const round = n => Math.round((n + Number.EPSILON * n) / 10) * 10;
    return { status: 'estimated', demo: true, min: round(length * rate.min + rate.fixed), max: round(length * rate.max + rate.fixed), revision, scope: rate.scope, currency: 'PLN', tax: 'gross', message: 'DEMO: fikcyjne stawki do prezentacji kalkulatora, nie cennik firmy. Transport nie jest uwzględniony.' };
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { calculate };
  else root.MspawDemo = { calculate };
})(globalThis);
