const form = document.querySelector('#quote-form');
const statusBox = document.querySelector('#status');
let config = { approved: false, rates: {} };
fetch('/api/pricing').then(r => r.json()).then(c => { config = c; updateEstimate(); }).catch(() => {});
function parameters() { return Object.fromEntries(new FormData(form)); }
function updateEstimate() {
  const p = parameters();
  const rate = config.rates?.[p.type]?.[p.material]?.[p.finish]?.[p.installation];
  const length = Number(p.length), height = Number(p.height);
  const eligible = ['balustrada', 'ogrodzenie'].includes(p.type) && config.approved && rate && length >= .1 && length <= 200 && height >= rate.minHeight && height <= rate.maxHeight;
  document.querySelector('#price').textContent = eligible ? `${Math.round((length * rate.min + rate.fixed) / 10) * 10}–${Math.round((length * rate.max + rate.fixed) / 10) * 10} zł brutto` : 'Wycena indywidualna';
  document.querySelector('#price-note').textContent = eligible ? 'Orientacyjny koszt według zatwierdzonych stawek. Transport i nietypowe warunki wymagają osobnej oceny. Ostateczną ofertę potwierdza Maciej.' : 'Cennik dla tej konfiguracji nie jest zatwierdzony lub potrzebna jest ocena wykonawcy. Przygotuj parametry do oferty.';
}
form.addEventListener('input', updateEstimate);
form.addEventListener('change', updateEstimate);
document.querySelectorAll('[data-type]').forEach(link => link.addEventListener('click', () => { form.elements.type.value = link.dataset.type; updateEstimate(); }));
document.querySelector('[name=deadline]').min = new Date().toLocaleDateString('en-CA');
function inquiryText() {
  const labels = { type: 'Rodzaj', material: 'Materiał', length: 'Długość [m]', height: 'Wysokość [m]', finish: 'Wykończenie', installation: 'Montaż', description: 'Opis', location: 'Miejscowość', deadline: 'Termin', name: 'Imię', email: 'E-mail', phone: 'Telefon' };
  return 'ZAPYTANIE M-SPAW — Maciej Kowalczyk\n\n' + Object.entries(parameters()).filter(([k]) => k !== 'acknowledge').map(([k,v]) => `${labels[k] || k}: ${v || 'do ustalenia'}`).join('\n') + '\n\nSzacunek: ' + document.querySelector('#price').textContent + '\nZałączniki należy dołączyć osobno. Ten plik nie jest potwierdzeniem wysłania.';
}
document.querySelector('#download').addEventListener('click', () => {
  const url = URL.createObjectURL(new Blob([inquiryText()], { type: 'text/plain;charset=utf-8' }));
  const a = document.createElement('a'); a.href = url; a.download = 'mspaw-zapytanie.txt'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  statusBox.textContent = 'Pobrano treść zapytania. Plik i zdjęcia możesz przesłać samodzielnie przez ustalony z Maciejem kanał kontaktu.';
});
form.addEventListener('submit', async event => {
  event.preventDefault();
  const button = form.querySelector('[type=submit]');
  const files = [...document.querySelector('#files').files];
  if (files.length > 3 || files.some(f => f.size > 5 * 1024 * 1024)) { statusBox.textContent = 'Wybierz maksymalnie 3 pliki, każdy do 5 MB.'; return; }
  button.disabled = true; statusBox.textContent = 'Zapisywanie zapytania lokalnie…';
  try {
    const attachments = await Promise.all(files.map(file => new Promise((resolve,reject) => {
      const reader = new FileReader(); reader.onerror = reject; reader.onload = () => resolve({ name: file.name, data: reader.result.split(',')[1] }); reader.readAsDataURL(file);
    })));
    const response = await fetch('/api/inquiries', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...parameters(), attachments }) });
    const result = await response.json(); if (!response.ok) throw Error(result.error || 'Błąd zapisu.');
    statusBox.textContent = `Zapisano lokalne zapytanie ${result.id}. Nie wysłano wiadomości do Macieja. Możesz pobrać treść zapytania.`;
  } catch (error) { statusBox.textContent = `Nie zapisano zapytania: ${error.message}. Uruchom stronę przez START.cmd lub pobierz treść zapytania.`; }
  finally { button.disabled = false; }
});
