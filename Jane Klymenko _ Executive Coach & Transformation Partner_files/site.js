const toggle=document.querySelector('.nav-toggle');
const links=document.querySelector('.nav-links');
if(toggle&&links){toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')==='true';toggle.setAttribute('aria-expanded',String(!open));links.classList.toggle('open',!open)});links.addEventListener('click',e=>{if(e.target.closest('a')){toggle.setAttribute('aria-expanded','false');links.classList.remove('open')}})}
