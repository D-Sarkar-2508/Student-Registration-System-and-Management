// ── Delete confirm ────────────────────────────────────────────────
function confirmDelete(formId, name) {
  if (confirm(`Delete student "${name}"? This cannot be undone.`)) {
    document.getElementById(formId).submit();
  }
}

// ── Auto-dismiss flash after 4s ──────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => el.remove(), 4000);
  });

  // Phone: digits only
  document.querySelectorAll('input[name="phone"], input[name="guardian_phone"]')
    .forEach(el => el.addEventListener('input', e => {
      e.target.value = e.target.value.replace(/\D/g, '');
    }));

  // Client-side validation on any form with data-validate
  const form = document.querySelector('form[data-validate]');
  if (!form) return;

  form.addEventListener('submit', e => {
    let ok = true;

    const check = (sel, test, msg) => {
      const el = form.querySelector(sel);
      if (!el) return;
      const valid = test(el.value.trim());
      el.classList.toggle('is-invalid', !valid);
      el.classList.toggle('is-valid', valid);
      if (!valid) { ok = false; }
    };

    check('input[name="name"]',     v => v.length >= 2,           'Name too short');
    check('input[name="email"]',    v => /^[\w\.-]+@[\w\.-]+\.\w{2,}$/.test(v), 'Bad email');
    check('input[name="phone"]',    v => /^\d{10}$/.test(v),      '10 digits needed');
    check('input[name="roll_number"]', v => v.length >= 3,        'Roll too short');
    check('select[name="branch"]',  v => v !== '',                 'Select branch');
    check('select[name="year"]',    v => v !== '',                 'Select year');

    const pw  = form.querySelector('input[name="password"]');
    const con = form.querySelector('input[name="confirm"]');
    if (pw) {
      const valid = pw.value.length >= 6;
      pw.classList.toggle('is-invalid', !valid);
      pw.classList.toggle('is-valid', valid);
      if (!valid) ok = false;
    }
    if (pw && con) {
      const match = pw.value === con.value;
      con.classList.toggle('is-invalid', !match);
      con.classList.toggle('is-valid', match);
      if (!match) ok = false;
    }

    if (!ok) e.preventDefault();
  });
});