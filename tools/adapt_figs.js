// Render every bank item that has a figure (`f`) to one standalone SVG for ADAPT:
//   node tools/adapt_figs.js bank/ch01.json figures/adapt
// Panels from fbx.js figBlock are laid out two per row; a particle legend (symbol = element) is redrawn in SVG.
const fs=require('fs');global.window=global;global.document={getElementById:()=>null,createElement:()=>({style:{}}),addEventListener:()=>{}};
eval(fs.readFileSync(__dirname+'/../js/fbx.js','utf8'));
const [,,bankPath,outDir]=process.argv;const B=JSON.parse(fs.readFileSync(bankPath,'utf8'));
const FF='Lato, Helvetica, Arial, sans-serif',INK='#2d3f4b';
for(const q of B){if(!q.f)continue;
 const fb=window.FBX.figBlock(q.f);
 const svgs=[...fb.matchAll(/<svg[^>]*class="fbx-fsvg"[\s\S]*?<\/svg>/g)].map(m=>m[0]);
 const dims=svgs.map(s=>{const m=s.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/);return {x:+m[1],y:+m[2],w:+m[3],h:+m[4]}});
 // legend entries from the particle key
 const leg=[];for(const f of q.f){if(f.type==='particles'&&f.key)for(const [k,v] of Object.entries(f.key))if(v.n)leg.push({c:v.c,q:v.q||'',n:v.n})}
 const per=svgs.length>=4?2:svgs.length;const gap=16;let o='',x=0,y=0,rowH=0,W=0;
 svgs.forEach((s,i)=>{if(i&&i%per===0){y+=rowH+gap;x=0;rowH=0}const d=dims[i];
  const inner=s.replace(/^<svg[^>]*>/,'').replace(/<\/svg>$/,'');
  o+=`<g transform="translate(${x},${y})"><svg x="0" y="0" width="${d.w}" height="${d.h}" viewBox="${d.x} ${d.y} ${d.w} ${d.h}">${inner}</svg></g>`;
  x+=d.w+gap;rowH=Math.max(rowH,d.h);W=Math.max(W,x-gap)});
 let H=y+rowH;
 const LW=Math.max(W,320);if(leg.length){let lx=0,ly=H+22;leg.forEach(e=>{const ew=26+e.n.length*8.5+30;if(lx>0&&lx+ew>LW){lx=0;ly+=28}o+=`<circle cx="${lx+11}" cy="${ly}" r="10" fill="${e.c}" stroke="${INK}" stroke-width="1.4"/>`+(e.q?`<text x="${lx+11}" y="${ly+4}" text-anchor="middle" font-size="11" font-weight="900" fill="#fff" font-family="${FF}">${e.q}</text>`:'')+`<text x="${lx+26}" y="${ly+5}" font-size="15" font-weight="700" fill="${INK}" font-family="${FF}">= ${e.n}</text>`;lx+=ew;W=Math.max(W,lx)});H=ly+16}
 const out=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -6 ${W+12} ${H+12}" width="${W+12}" height="${H+12}" font-family="${FF}"><rect x="-6" y="-6" width="${W+12}" height="${H+12}" fill="#fff"/>${o}</svg>`;
 const dedupe=str=>str.replace(/<([a-zA-Z]+)((?:\s+[\w:-]+="[^"]*")+)\s*(\/?)>/g,(m,tag,attrs,sl)=>{const seen=new Map();for(const a of attrs.matchAll(/([\w:-]+)="([^"]*)"/g))seen.set(a[1],a[2]);return '<'+tag+[...seen].map(([k,v])=>` ${k}="${v}"`).join('')+(sl?'/':'')+'>'});
 fs.writeFileSync(`${outDir}/${q.id}.svg`,dedupe(out));console.log(q.id,svgs.length,'panels',Math.round(W),'x',Math.round(H),'legend',leg.length);
}
