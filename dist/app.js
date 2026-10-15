const form = document.querySelector('#quote-form');
const statusBox = document.querySelector('#status');
const menuToggle = document.querySelector('.menu-toggle');
const siteNavigation = document.querySelector('#site-navigation');
function closeNavigation() {
  siteNavigation.classList.remove('is-open');
  menuToggle.setAttribute('aria-expanded', 'false');
}
menuToggle.addEventListener('click', () => {
  const expanded = menuToggle.getAttribute('aria-expanded') !== 'true';
  menuToggle.setAttribute('aria-expanded', String(expanded));
  siteNavigation.classList.toggle('is-open', expanded);
});
siteNavigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeNavigation));
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeNavigation();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
    closeNavigation();
    menuToggle.focus();
  }
});
function parameters() { return Object.fromEntries(new FormData(form)); }
const estimateFields = ['type', 'material', 'finish', 'installation', 'length', 'height'];
const priceBox = document.querySelector('#price');
const priceNote = document.querySelector('#price-note');
let estimateSequence = 0, estimateTimer, estimateController, latestEstimate = null;
const runtime = fetch('./runtime.json').then(response => {
  if (!response.ok) throw Error('Nie wczytano konfiguracji podglądu.');
  return response.json();
}).then(async settings => {
  if (settings.mode === 'pages-demo') {
    const response = await fetch('./demo-pricing.json');
    if (!response.ok) throw Error('Nie wczytano cennika demo.');
    settings.pricing = await response.json();
    document.querySelector('.preview').textContent = 'PUBLICZNY PODGLĄD · realizacje i kontakt M-SPAW · ceny demo, formularz nie wysyła danych';
    document.querySelector('.local-note').textContent = 'To demonstracja strony. Kalkulator działa w przeglądarce. Formularz symuluje zgłoszenie; nie wysyła danych ani załączników do firmy.';
    form.querySelector('[type=submit]').textContent = 'Sprawdź zapytanie demonstracyjne ↗';
    form.querySelector('.check').lastChild.textContent = 'Rozumiem, że jest to demonstracja. Zapytanie i załączniki nie zostaną wysłane do firmy.';
  }
  return settings;
});
// Gallery uses native dialog for modal focus and Escape handling.
const projectDialog = document.querySelector('#project-view');
const projectCards = [...document.querySelectorAll('[data-project]')];
let currentProject = 0;
function showProject(index) {
  currentProject = (index + projectCards.length) % projectCards.length;
  const card = projectCards[currentProject];
  const image = card.querySelector('img');
  const expanded = document.querySelector('#project-image');
  expanded.src = image.getAttribute('src');
  expanded.alt = image.alt;
  document.querySelector('#project-title').textContent = card.querySelector('strong').textContent;
  document.querySelector('#project-description').textContent = card.querySelector('.gallery-caption').textContent;
  document.querySelector('#project-counter').textContent = `${currentProject + 1} / ${projectCards.length}`;
}
projectCards.forEach((card, index) => card.addEventListener('click', () => {
  showProject(index);
  projectDialog.showModal();
  document.body.classList.add('project-open');
}));
document.querySelector('#project-close').addEventListener('click', () => projectDialog.close());
document.querySelector('#project-prev').addEventListener('click', () => showProject(currentProject - 1));
document.querySelector('#project-next').addEventListener('click', () => showProject(currentProject + 1));
projectDialog.addEventListener('close', () => document.body.classList.remove('project-open'));
projectDialog.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    showProject(currentProject + (event.key === 'ArrowRight' ? 1 : -1));
  }
});
projectDialog.addEventListener('click', event => {
  if (event.target !== projectDialog) return;
  const box = projectDialog.getBoundingClientRect();
  if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) projectDialog.close();
});
document.querySelector('#project-quote').addEventListener('click', () => {
  form.elements.type.value = projectCards[currentProject].dataset.projectType;
  projectDialog.close();
  updateEstimate();
});
runtime.catch(() => {});
function estimateParameters() {
  const values = parameters();
  return Object.fromEntries(estimateFields.map(key => [key, values[key]]));
}
function updateEstimate() {
  const sequence = ++estimateSequence;
  const values = estimateParameters();
  clearTimeout(estimateTimer); estimateController?.abort();
  latestEstimate = null;
  priceBox.textContent = 'Sprawdzanie wyceny…';
  priceNote.textContent = 'Sprawdzamy parametry i dostępność zatwierdzonej stawki.';
  estimateTimer = setTimeout(async () => {
    const controller = new AbortController();
    estimateController = controller;
    const timeout = setTimeout(() => controller.abort(), 8000);
    try {
      const settings = await runtime;
      let result;
      if (settings.mode === 'pages-demo') result = MspawDemo.calculate(values, settings.pricing, settings.pricingRevision);
      else {
        const response = await fetch('/api/estimate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(values), signal: controller.signal });
        result = await response.json();
        if (!response.ok) throw Error(result.error || 'Nieprawidłowe parametry.');
      }
      if (sequence !== estimateSequence) return;
      latestEstimate = result;
      priceBox.textContent = result.status === 'estimated' ? `${result.demo ? 'Przykład: ' : ''}${result.min.toLocaleString('pl-PL')}–${result.max.toLocaleString('pl-PL')} zł brutto` : 'Wycena indywidualna';
      priceNote.textContent = result.message + (result.scope ? ` Zakres: ${result.scope}` : '');
    } catch (error) {
      if (sequence !== estimateSequence) return;
      priceBox.textContent = 'Wycena indywidualna';
      priceNote.textContent = error.name === 'AbortError' ? 'Nie otrzymano wyceny na czas. Możesz nadal przygotować zapytanie.' : 'Nie można obliczyć wyceny. Sprawdź wymiary i uruchom stronę przez START.cmd.';
    } finally { clearTimeout(timeout); }
  }, 250);
}
form.addEventListener('input', event => { if (estimateFields.includes(event.target.name)) updateEstimate(); });
form.addEventListener('change', event => { if (estimateFields.includes(event.target.name)) updateEstimate(); });
updateEstimate();
document.querySelector('#load-demo').addEventListener('click', () => {
  const example = { type: 'balustrada', material: 'stal', finish: 'proszek', installation: 'tak', length: '6.5', height: '1.1', description: 'PRZYKŁAD DEMO: prosta balustrada tarasowa, 6,5 m długości i 1,1 m wysokości. Pionowe wypełnienie profilowe, kolor grafitowy, montaż do przygotowanego podłoża.', location: 'Niedźwiedź', name: 'Klient demonstracyjny', email: 'klient@example.com', phone: '000 000 000', deadline: '' };
  for (const [key, value] of Object.entries(example)) form.elements[key].value = value;
  updateEstimate();
  statusBox.textContent = 'Wczytano fikcyjne dane przykładowe. Możesz zmienić wymiary i sprawdzić wynik, a następnie zapisać testowe zapytanie.';
});
document.querySelectorAll('[data-type]').forEach(link => link.addEventListener('click', () => { form.elements.type.value = link.dataset.type; updateEstimate(); }));
document.querySelector('[name=deadline]').min = new Date().toLocaleDateString('en-CA');
function inquiryText() {
  const labels = { type: 'Rodzaj', material: 'Materiał', length: 'Długość [m]', height: 'Wysokość [m]', finish: 'Wykończenie', installation: 'Montaż', description: 'Opis', location: 'Miejscowość', deadline: 'Termin', name: 'Imię', email: 'E-mail', phone: 'Telefon' };
  const estimateText = latestEstimate?.status === 'estimated' ? `${priceBox.textContent}\nWersja cennika: ${latestEstimate.revision}\nZakres: ${latestEstimate.scope}\n${latestEstimate.message}` : 'Wycena indywidualna — brak potwierdzonego szacunku.';
  return 'ZAPYTANIE M-SPAW — Maciej Kowalczyk\n\n' + Object.entries(parameters()).filter(([k]) => k !== 'acknowledge').map(([k,v]) => `${labels[k] || k}: ${v || 'do ustalenia'}`).join('\n') + '\n\nSzacunek: ' + estimateText + '\nZałączniki należy dołączyć osobno. Ten plik nie jest potwierdzeniem wysłania.';
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
  const snapshot = parameters();
  form.querySelectorAll('fieldset').forEach(fieldset => { fieldset.disabled = true; });
  document.querySelector('#download').disabled = true;
  document.querySelector('#load-demo').disabled = true;
  button.disabled = true; statusBox.textContent = 'Zapisywanie zapytania lokalnie…';
  try {
    const settings = await runtime;
    if (settings.mode === 'pages-demo') {
      statusBox.textContent = 'Demonstracja zakończona: zapytanie jest gotowe do pobrania. Nie wysłano ani nie zapisano danych i załączników. Użyj przycisku „Pobierz treść zapytania”.';
      return;
    }
    const attachments = await Promise.all(files.map(file => new Promise((resolve,reject) => {
      const reader = new FileReader(); reader.onerror = reject; reader.onload = () => resolve({ name: file.name, data: reader.result.split(',')[1] }); reader.readAsDataURL(file);
    })));
    const response = await fetch('/api/inquiries', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...snapshot, attachments }) });
    const result = await response.json(); if (!response.ok) throw Error(result.error || 'Błąd zapisu.');
    statusBox.textContent = `Zapisano lokalne zapytanie ${result.id}. Nie wysłano wiadomości do Macieja. Możesz pobrać treść zapytania.`;
  } catch (error) { statusBox.textContent = `Nie zapisano zapytania: ${error.message}. Uruchom stronę przez START.cmd lub pobierz treść zapytania.`; }
  finally {
    button.disabled = false;
    form.querySelectorAll('fieldset').forEach(fieldset => { fieldset.disabled = false; });
    document.querySelector('#download').disabled = false;
    document.querySelector('#load-demo').disabled = false;
    updateEstimate();
  }
});
