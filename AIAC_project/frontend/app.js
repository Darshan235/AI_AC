// Simple invoice generator: asks only for customer name.
// Generates invoice of form: [PREFIX]-[YYYYMMDDHHMMSS]-[RAND4]
// PREFIX: up to 4 uppercase chars extracted from customer name (initials or first letters).

const form = document.getElementById('form');
const cust = document.getElementById('cust');
const result = document.getElementById('result');
const invoiceEl = document.getElementById('invoice');
const rname = document.getElementById('rname');
const copyBtn = document.getElementById('copy');
const newBtn = document.getElementById('new');

function makePrefix(name){
  if(!name) return 'CUST';
  // take initials, else first letters up to 4
  const parts = name.trim().split(/\s+/).filter(Boolean).map(p=>p[0].toUpperCase());
  if(parts.length>=2){
    return (parts.slice(0,4)).join('').slice(0,4);
  }
  const plain = name.replace(/[^A-Za-z0-9]/g,'').toUpperCase();
  return plain.slice(0,4) || 'CUST';
}

function rand4(){
  const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  let s='';
  for(let i=0;i<4;i++) s += chars.charAt(Math.floor(Math.random()*chars.length));
  return s;
}

function timestamp(){
  const d = new Date();
  const pad = (n)=>n.toString().padStart(2,'0');
  return d.getFullYear().toString()
    + pad(d.getMonth()+1)
    + pad(d.getDate())
    + pad(d.getHours())
    + pad(d.getMinutes())
    + pad(d.getSeconds());
}

function generateInvoiceFor(name){
  const pref = makePrefix(name);
  const ts = timestamp();
  const r = rand4();
  return `${pref}-${ts}-${r}`;
}

form.addEventListener('submit', (e)=>{
  e.preventDefault();
  const name = cust.value.trim();
  if(!name){ cust.focus(); return; }
  const inv = generateInvoiceFor(name);
  invoiceEl.value = inv;
  rname.textContent = name;
  result.hidden = false;
  invoiceEl.select();
});

copyBtn.addEventListener('click', async ()=>{
  if(!invoiceEl.value) return;
  try{
    await navigator.clipboard.writeText(invoiceEl.value);
    copyBtn.textContent = 'Copied ✓';
    setTimeout(()=>copyBtn.textContent='Copy',1200);
  }catch(e){
    alert('Copy failed — select and copy manually');
  }
});

newBtn.addEventListener('click', ()=>{
  cust.value = '';
  invoiceEl.value = '';
  result.hidden = true;
  cust.focus();
});

// usability: focus input
cust.focus();
