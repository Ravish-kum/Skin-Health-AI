document.addEventListener("DOMContentLoaded", () => {
    // ── Icon texture on canvas ──
    const canvas = document.getElementById('texture-canvas');
    if (!canvas) return; // Only run on signup page
    
    const ctx = canvas.getContext('2d');

    const ICONS = [
        // leaf
        (x, y, s, a) => {
            ctx.beginPath();
            ctx.moveTo(x, y - s);
            ctx.bezierCurveTo(x+s, y-s, x+s, y+s*0.5, x, y+s*0.8);
            ctx.bezierCurveTo(x-s, y+s*0.5, x-s, y-s, x, y-s);
            ctx.globalAlpha = a; ctx.stroke(); ctx.globalAlpha = 1;
        },
        // circle
        (x, y, s, a) => {
            ctx.beginPath();
            ctx.arc(x, y, s, 0, Math.PI*2);
            ctx.globalAlpha = a; ctx.stroke(); ctx.globalAlpha = 1;
        },
        // sparkle / plus
        (x, y, s, a) => {
            ctx.beginPath();
            ctx.moveTo(x, y-s); ctx.lineTo(x, y+s);
            ctx.moveTo(x-s, y); ctx.lineTo(x+s, y);
            ctx.globalAlpha = a; ctx.stroke(); ctx.globalAlpha = 1;
        },
        // diamond
        (x, y, s, a) => {
            ctx.beginPath();
            ctx.moveTo(x, y-s); ctx.lineTo(x+s*0.65, y);
            ctx.lineTo(x, y+s); ctx.lineTo(x-s*0.65, y);
            ctx.closePath();
            ctx.globalAlpha = a; ctx.stroke(); ctx.globalAlpha = 1;
        },
        // drop
        (x, y, s, a) => {
            ctx.beginPath();
            ctx.moveTo(x, y-s*1.1);
            ctx.bezierCurveTo(x+s*0.9, y-s*0.2, x+s*0.9, y+s*0.5, x, y+s*1.1);
            ctx.bezierCurveTo(x-s*0.9, y+s*0.5, x-s*0.9, y-s*0.2, x, y-s*1.1);
            ctx.globalAlpha = a; ctx.stroke(); ctx.globalAlpha = 1;
        },
        // star 4-pt
        (x, y, s, a) => {
            ctx.beginPath();
            for(let i=0;i<8;i++){
                const r = i%2===0 ? s : s*0.4;
                const angle = (i/8)*Math.PI*2 - Math.PI/2;
                i===0 ? ctx.moveTo(x+Math.cos(angle)*r, y+Math.sin(angle)*r)
                      : ctx.lineTo(x+Math.cos(angle)*r, y+Math.sin(angle)*r);
            }
            ctx.closePath();
            ctx.globalAlpha = a; ctx.stroke(); ctx.globalAlpha = 1;
        },
        // small cross
        (x, y, s, a) => {
            const t = s*0.35;
            ctx.beginPath();
            ctx.moveTo(x-t, y-s); ctx.lineTo(x+t, y-s);
            ctx.lineTo(x+t, y-t); ctx.lineTo(x+s, y-t);
            ctx.lineTo(x+s, y+t); ctx.lineTo(x+t, y+t);
            ctx.lineTo(x+t, y+s); ctx.lineTo(x-t, y+s);
            ctx.lineTo(x-t, y+t); ctx.lineTo(x-s, y+t);
            ctx.lineTo(x-s, y-t); ctx.lineTo(x-t, y-t);
            ctx.closePath();
            ctx.globalAlpha = a; ctx.stroke(); ctx.globalAlpha = 1;
        },
        // hex
        (x, y, s, a) => {
            ctx.beginPath();
            for(let i=0;i<6;i++){
                const angle = (i/6)*Math.PI*2 - Math.PI/6;
                i===0 ? ctx.moveTo(x+Math.cos(angle)*s, y+Math.sin(angle)*s)
                      : ctx.lineTo(x+Math.cos(angle)*s, y+Math.sin(angle)*s);
            }
            ctx.closePath();
            ctx.globalAlpha = a; ctx.stroke(); ctx.globalAlpha = 1;
        },
    ];

    let icons = [];

    function buildIcons() {
        icons = [];
        const W = canvas.width, H = canvas.height;
        const count = Math.floor((W * H) / 9000);
        for (let i = 0; i < count; i++) {
            icons.push({
                x: Math.random() * W,
                y: Math.random() * H,
                size: 4 + Math.random() * 10,
                type: Math.floor(Math.random() * ICONS.length),
                alpha: 0.04 + Math.random() * 0.09,
                rot: Math.random() * Math.PI * 2,
            });
        }
    }

    function draw() {
        canvas.width  = window.innerWidth;
        canvas.height = window.innerHeight;
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 0.75;
        buildIcons();
        icons.forEach(ic => {
            ctx.save();
            ctx.translate(ic.x, ic.y);
            ctx.rotate(ic.rot);
            ICONS[ic.type](0, 0, ic.size, ic.alpha);
            ctx.restore();
        });
    }

    draw();
    window.addEventListener('resize', draw);

    // ── Floating particles ──
    function spawnParticle() {
        const p = document.createElement('div');
        p.className = 'particle';
        const size = 2 + Math.random() * 5;
        p.style.cssText = `
            width:${size}px; height:${size}px;
            left:${Math.random()*100}vw;
            bottom:-10px;
            animation-duration:${8 + Math.random()*12}s;
            animation-delay:${Math.random()*4}s;
        `;
        document.body.appendChild(p);
        setTimeout(() => p.remove(), 24000);
    }
    for(let i=0;i<12;i++) spawnParticle();
    setInterval(spawnParticle, 2800);
});

// ── Button handlers ──
function handleGoogle() {
    const btn = document.querySelector('.btn-google');
    if (btn) {
        btn.style.transform = 'scale(0.97)';
        setTimeout(() => btn.style.transform = '', 200);
    }
    alert('Google Auth flow — wire up your OAuth client ID here.');
}

function handleGuest() {
    const btn = document.querySelector('.btn-guest');
    if (btn) {
        btn.style.transform = 'scale(0.97)';
        setTimeout(() => btn.style.transform = '', 200);
    }
    alert('Continuing as guest…');
}
