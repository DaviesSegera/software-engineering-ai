"use strict";
const answers = () => [...document.querySelectorAll('details.practice-answer')];
document.getElementById('show-answers')?.addEventListener('click',()=>answers().forEach(x=>x.open=true));
document.getElementById('hide-answers')?.addEventListener('click',()=>answers().forEach(x=>x.open=false));
document.getElementById('print-notes')?.addEventListener('click',()=>window.print());
document.querySelectorAll('.copy-code').forEach(button=>button.addEventListener('click',async()=>{
 const code=document.getElementById(button.dataset.code), status=button.parentElement.querySelector('.code-status');
 try{await navigator.clipboard.writeText(code.textContent);status.textContent='Copied';}
 catch{const selection=window.getSelection(),range=document.createRange();range.selectNodeContents(code);selection.removeAllRanges();selection.addRange(range);status.textContent='Code selected. Press Ctrl+C or use Copy.';}
}));
