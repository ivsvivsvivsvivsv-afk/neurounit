document.addEventListener('DOMContentLoaded', () => {
    // 1. Matrix
    const cvs = document.getElementById('matrix');
    const ctx = cvs.getContext('2d');
    function resize() { cvs.width=window.innerWidth; cvs.height=window.innerHeight; }
    window.onresize = resize; resize();
    const cols = Math.floor(cvs.width/20); const ypos = Array(cols).fill(0);
    setInterval(() => {
        ctx.fillStyle='#0001'; ctx.fillRect(0,0,cvs.width,cvs.height);
        ctx.fillStyle='#0F0'; ctx.font='15pt monospace';
        ypos.forEach((y,i)=>{
            ctx.fillText(String.fromCharCode(Math.random()*128), i*20, y);
            ypos[i] = y>100+Math.random()*10000 ? 0 : y+20;
        });
    }, 50);

    // 2. Glitch Text
    const t = document.querySelector('.glitch');
    const txt = t.getAttribute('data-text');
    let i=0;
    const inv = setInterval(() => {
        t.innerText = txt.split("").map((l,idx) => idx<i ? txt[idx] : "X0#@"[Math.floor(Math.random()*4)]).join("");
        if(i>=txt.length) clearInterval(inv); i+=1/3;
    }, 40);

    // 3. Game
    let active = true;
    window.checkClone = (el, real) => {
        if(!active) return;
        el.querySelector(real ? '.succ' : '.err').style.display='flex';
        if(real) { active=false; el.style.borderColor='#00F0FF'; alert(GAME_ALERT); }
        else { el.style.borderColor='#FF2050'; setTimeout(()=>{el.querySelector('.err').style.display='none';el.style.borderColor='#333'},1000); }
    };

    // 4. Scroll
    const iron = document.querySelector('.iron-man');
    const layers = document.querySelectorAll('.layer');
    window.onscroll = () => {
        const r = iron.getBoundingClientRect();
        const p = -r.top / (r.height - window.innerHeight);
        if(p>0 && p<1.2) {
            layers[0].style.opacity = 1;
            layers[1].style.opacity = p > 0.33 ? 1 : 0;
            layers[2].style.opacity = p > 0.66 ? 1 : 0;
        }
    };

    // 5. Terminal
    window.runTerm = () => {
        const out = document.getElementById('term-out');
        let k=0;
        function log() {
            if(k<LOGS.length) { out.innerHTML+=`<div>${LOGS[k]}</div>`; out.scrollTop=out.scrollHeight; k++; setTimeout(log,600); }
        }
        log();
    };

    // 6. Form
    document.getElementById('lead-form').onsubmit = async (e) => {
        e.preventDefault();
        const d = new FormData(e.target);
        const res = await fetch('/api/lead', {
            method:'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify(Object.fromEntries(d))
        });
        const j = await res.json();
        if(j.status=='ok') window.location.href = j.redirect;
    };
    
    window.scrollToId = (id) => document.getElementById(id).scrollIntoView({behavior:'smooth'});
});
