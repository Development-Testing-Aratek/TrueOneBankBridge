const money = n => new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:0}).format(Number.isFinite(n)?n:0);
const amount = document.getElementById('amount'), rate = document.getElementById('rate'), tenure = document.getElementById('tenure');
function updateEmi(){
  let p = Math.max(0,Number(amount.value)||0), annual = Math.min(36,Math.max(0,Number(rate.value)||0)), years = Math.min(30,Math.max(1,Number(tenure.value)||1));
  rate.value = annual; tenure.value = years;
  let r=annual/1200,n=years*12,emi=r===0?p/n:p*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1);
  if(!Number.isFinite(emi)) emi=0;
  let total=emi*n, interest=Math.max(0,total-p);
  document.getElementById('amountLabel').textContent=money(p);
  document.getElementById('emiValue').textContent=money(emi);
  document.getElementById('principalValue').textContent=money(p);
  document.getElementById('interestValue').textContent=money(interest);
  document.getElementById('totalValue').textContent=money(total);
}
[amount,rate,tenure].forEach(el=>el.addEventListener('input',updateEmi));
document.getElementById('resetCalc').addEventListener('click',()=>{amount.value=1000000;rate.value=10.5;tenure.value=5;updateEmi();});
document.querySelectorAll('[data-loan]').forEach(link=>link.addEventListener('click',()=>{document.getElementById('loanType').value=link.dataset.loan;}));
const menuToggle=document.getElementById('menuToggle'), nav=document.getElementById('mainNav');
menuToggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');menuToggle.setAttribute('aria-expanded',String(open));});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menuToggle.setAttribute('aria-expanded','false');}));
document.getElementById('year').textContent=new Date().getFullYear();
document.getElementById('enquiryForm').addEventListener('submit',e=>{
  e.preventDefault();
  const form=e.currentTarget, status=document.getElementById('formStatus');
  if(!form.checkValidity()){form.reportValidity();return;}
  window.location.href='https://forms.gle/hXJwg6kA5zxyamW47';
});
updateEmi();
