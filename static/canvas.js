document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById('texture-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const ICONS = [
    (x,y,s,a)=>{ctx.beginPath();ctx.moveTo(x,y-s);ctx.bezierCurveTo(x+s,y-s,x+s,y+s*.5,x,y+s*.8);ctx.bezierCurveTo(x-s,y+s*.5,x-s,y-s,x,y-s);ctx.globalAlpha=a;ctx.stroke();ctx.globalAlpha=1;},
    (x,y,s,a)=>{ctx.beginPath();ctx.arc(x,y,s,0,Math.PI*2);ctx.globalAlpha=a;ctx.stroke();ctx.globalAlpha=1;},
    (x,y,s,a)=>{ctx.beginPath();ctx.moveTo(x,y-s);ctx.lineTo(x,y+s);ctx.moveTo(x-s,y);ctx.lineTo(x+s,y);ctx.globalAlpha=a;ctx.stroke();ctx.globalAlpha=1;},
    (x,y,s,a)=>{ctx.beginPath();ctx.moveTo(x,y-s);ctx.lineTo(x+s*.65,y);ctx.lineTo(x,y+s);ctx.lineTo(x-s*.65,y);ctx.closePath();ctx.globalAlpha=a;ctx.stroke();ctx.globalAlpha=1;},
    (x,y,s,a)=>{ctx.beginPath();ctx.moveTo(x,y-s*1.1);ctx.bezierCurveTo(x+s*.9,y-s*.2,x+s*.9,y+s*.5,x,y+s*1.1);ctx.bezierCurveTo(x-s*.9,y+s*.5,x-s*.9,y-s*.2,x,y-s*1.1);ctx.globalAlpha=a;ctx.stroke();ctx.globalAlpha=1;},
    (x,y,s,a)=>{ctx.beginPath();for(let i=0;i<8;i++){const r=i%2===0?s:s*.4,angle=(i/8)*Math.PI*2-Math.PI/2;i===0?ctx.moveTo(x+Math.cos(angle)*r,y+Math.sin(angle)*r):ctx.lineTo(x+Math.cos(angle)*r,y+Math.sin(angle)*r);}ctx.closePath();ctx.globalAlpha=a;ctx.stroke();ctx.globalAlpha=1;},
    (x,y,s,a)=>{ctx.beginPath();for(let i=0;i<6;i++){const angle=(i/6)*Math.PI*2-Math.PI/6;i===0?ctx.moveTo(x+Math.cos(angle)*s,y+Math.sin(angle)*s):ctx.lineTo(x+Math.cos(angle)*s,y+Math.sin(angle)*s);}ctx.closePath();ctx.globalAlpha=a;ctx.stroke();ctx.globalAlpha=1;},
  ];
  function draw() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 0.75;
    const count = Math.floor((canvas.width * canvas.height) / 9000);
    for (let i = 0; i < count; i++) {
      const x=Math.random()*canvas.width, y=Math.random()*canvas.height;
      const s=4+Math.random()*10, a=0.04+Math.random()*0.09;
      const type=Math.floor(Math.random()*ICONS.length);
      ctx.save(); ctx.translate(x,y); ctx.rotate(Math.random()*Math.PI*2);
      ICONS[type](0,0,s,a);
      ctx.restore();
    }
  }
  draw();
  window.addEventListener('resize', draw);
});
