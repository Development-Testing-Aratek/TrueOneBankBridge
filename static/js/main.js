(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#primary-nav');
  if (menuButton && nav) {
    menuButton.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('open');
      menuButton.setAttribute('aria-expanded', String(isOpen));
    });
    nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
      nav.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false');
    }));
  }
  const money = value => new Intl.NumberFormat('en-IN', {style:'currency',currency:'INR',maximumFractionDigits:0}).format(Math.max(0, value));
  const principal = document.querySelector('#principal');
  const interest = document.querySelector('#interest');
  const tenure = document.querySelector('#tenure');
  const emiOutput = document.querySelector('#emi-output');
  const principalLabel = document.querySelector('#principal-label');
  const interestOutput = document.querySelector('#interest-output');
  const totalOutput = document.querySelector('#total-output');
  function calculate() {
    if (!principal || !interest || !tenure) return;
    const p = Number(principal.value);
    const annualRate = Number(interest.value);
    const years = Number(tenure.value);
    principalLabel.textContent = money(p);
    if (!Number.isFinite(p) || !Number.isFinite(annualRate) || !Number.isFinite(years) || p <= 0 || annualRate < 1 || annualRate > 36 || years < 1 || years > 30) {
      emiOutput.textContent = 'Check inputs'; interestOutput.textContent = '—'; totalOutput.textContent = '—'; return;
    }
    const n = years * 12, r = annualRate / 1200;
    const emi = r === 0 ? p / n : p * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1);
    const total = emi * n;
    emiOutput.textContent = money(emi);
    interestOutput.textContent = money(total - p);
    totalOutput.textContent = money(total);
  }
  [principal, interest, tenure].forEach(el => el && el.addEventListener('input', calculate));
  calculate();
  document.querySelectorAll('[data-loan]').forEach(link => link.addEventListener('click', () => {
    const select = document.querySelector('#loan_type');
    if (select) select.value = link.dataset.loan;
  }));
  const year = document.querySelector('#year');
  if (year) year.textContent = new Date().getFullYear();
  const form = document.querySelector('#enquiry-form');
  if (form) form.addEventListener('submit', event => {
    const mobile = document.querySelector('#mobile');
    const cleaned = mobile.value.replace(/[\s()+-]/g, '');
    if (!/^(?:91)?[6-9]\d{9}$/.test(cleaned)) {
      event.preventDefault(); mobile.setCustomValidity('Enter a valid Indian mobile number.'); mobile.reportValidity();
    } else mobile.setCustomValidity('');
  });
})();