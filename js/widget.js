/* CHEM 3A textbook "Try It" widget (adapted from ItsDrDan/textbook for CHEM 3B).
   practice.html?t=ch01-method,ch01-classify&n=8     questions from bank/<chapter>.json, filtered by topic
   &ids=c1-001,c1-002   hand-picked   &q=regex   filter on the question text   &fresh=1   new random set each visit
   &title=...&kicker=...&game=<key>   header and "Play the full game" link
   Questions: {id,t,q,c:[right,wrong,wrong,wrong],y:[why right, why wrong…],h,w,d,k,f}  (fbx.js format plus y). */
(function(){
"use strict";
const P=new URLSearchParams(location.search),$=s=>document.querySelector(s);
const shuf=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const load=(src,ready)=>ready()?Promise.resolve():new Promise((res,rej)=>{const s=document.createElement('script');s.src=src;s.onload=()=>ready()?res():rej(new Error(src+' did not initialise'));s.onerror=()=>rej(new Error('Could not load '+src));document.head.appendChild(s)});
const loadFail=e=>{console.error(e);$('#host').innerHTML='<div class="rl-card">Sorry, the practice questions could not load. Please refresh the page.</div>'};
const GAMES={finalboss:['Final Boss','https://itsdrdan.github.io/finalexam/?course=3A'],elements:['Symbol Safari','https://itsdrdan.github.io/elements/'],
 sigfig:['Significant Figures','https://itsdrdan.github.io/sigfig/'],metric:['Prefix Power-Up','https://itsdrdan.github.io/metric/'],quantum:['Quantum Quest','https://itsdrdan.github.io/quantumchemistry/?course=3A'],
 polyatomic:['Polyatomic Posse','https://itsdrdan.github.io/polyatomic/?course=3A'],naming:['Name That Compound!','https://itsdrdan.github.io/ionicformula/?course=3A'],lewis:['Lewis Structure Studio','https://itsdrdan.github.io/lewisstructures/?course=3A'],
 reactions:['Reaction Rumble','https://itsdrdan.github.io/reactions/?course=3A'],redox:['LEO Goes GER!','https://itsdrdan.github.io/redox/?course=3A'],stoich:['Stoichiometry','https://itsdrdan.github.io/stoichiometry/?course=3A'],
 thermo:['Thermochemistry','https://itsdrdan.github.io/thermochemistry/?course=3A'],imf:['Sticky Molecules','https://itsdrdan.github.io/IMF/?course=3A'],gas:['Under Pressure','https://itsdrdan.github.io/gaslaws/?course=3A'],moles:['The Mole','https://itsdrdan.github.io/moles/?course=3A'],algebra:['Algebra for Chemistry','https://itsdrdan.github.io/algebratrainer/'],hub:['the Study Hub','https://itsdrdan.github.io/games/']};
/* topic id -> [name, icon]; the chapter file is the part before the first dash */
const TOPICS=[['ch01-method','Scientific Method','🔬'],['ch01-units','Numbers and Units','📏'],['ch01-sigfig','Significant Figures','🎯'],['ch01-convert','Conversions','🔁'],['ch01-classify','Classifying Matter','🧪'],['ch01-states','States of Matter','🧊'],['ch01-charge','Electric Charge','⚡'],['ch01-change','Physical & Chemical Changes','🔥'],['ch01-density','Density','⚖️'],['ch02-theory','Atomic Theory','🔭'],['ch02-particles','Protons, Neutrons & Electrons','⚛️'],['ch02-table','The Periodic Table','🗺️'],['ch02-ions','Ions','➕'],['ch02-isotopes','Isotopes','🧬'],['ch02-mass','Average Atomic Mass','📊'],['ch03-light','Light and Energy','🌈'],['ch03-bohr','Bohr Model and Spectra','💡'],['ch03-orbitals','Orbitals and Orbital Diagrams','🏨'],['ch03-config','Electron Configurations','🧩'],['ch03-valence','Valence Electrons and Ion Charges','🔋'],['ch03-trends','Periodic Trends','📈'],['ch04-formulas','Formulas and Compound Types','🔤'],['ch04-ionicformula','Writing Ionic Formulas','✖️'],['ch04-polyatomic','Polyatomic Ions','🧱'],['ch04-ionicname','Naming Ionic Compounds','🏷️'],['ch04-molecular','Naming Molecular Compounds','🔗'],['ch04-acids','Naming Acids','🍋'],['ch05-mole','The Mole and Avogadro','🥄'],['ch05-molarmass','Molar Mass','⚖️'],['ch05-convert','Mass, Moles, and Particles','🔁'],['ch05-formula','Moles Within a Formula','🧮'],['ch06-ionic','Ionic Bonding','⚡'],['ch06-lewis','Covalent Bonds and Lewis Structures','✏️'],['ch06-vsepr','Molecular Shape (VSEPR)','🔺'],['ch06-polarity','Electronegativity and Polarity','🧲'],['ch06-percent','Percent Composition','％'],['ch06-empirical','Empirical and Molecular Formulas','🧪'],['ch07-equations','Equations and Balancing','⚖️'],['ch07-types','Reaction Patterns','🔀'],['ch07-solubility','Electrolytes and Solubility','💧'],['ch07-netionic','Precipitation and Net Ionic','🧂'],['ch07-acidgas','Acid-Base and Gas Evolution','🫧'],['ch07-redox','Oxidation-Reduction','🔋'],['ch07-activity','Activity Series','🏃'],['ch08-moleratio','Mole Ratios','🚲'],['ch08-massmass','Mass-to-Mass Stoichiometry','⚖️'],['ch08-solgas','Solutions and Gases in Stoichiometry','🧪'],['ch08-limiting','Limiting Reactant','🛑'],['ch08-yield','Theoretical and Percent Yield','🎯'],['ch08-enthalpy','Enthalpy of Reaction','🔥'],['ch09-energy','Energy and Its Forms','⚡'],['ch09-temp','Temperature Scales','🌡️'],['ch09-units','Heat Units and Heat Flow','🔥'],['ch09-specheat','Specific Heat','♨️'],['ch09-phase','Phase Changes and Heating Curves','🧊'],['ch09-imf','Intermolecular Forces','🧲'],['ch09-solids','Liquids and Solids','💎'],['ch09-vapor','Vapor Pressure and Ranking','💨'],['ch10-kmt','Kinetic Molecular Theory','🎈'],['ch10-pressure','Pressure and Its Units','🧭'],['ch10-laws','The Gas Laws','🔁'],['ch10-ideal','The Ideal Gas Law','🧮'],['ch10-stoich','Gas Stoichiometry','⚗️'],['ch10-dalton','Dalton\'s Law','🫁'],['ch11-dissolve','How Solutions Form','🧂'],['ch11-solubility','Temperature, Pressure, and Solubility','🥤'],['ch11-conc','Concentration','🧪'],['ch11-dilution','Molarity and Dilution','💧'],['ch11-titration','Solution Stoichiometry and Titration','⚗️'],['ch11-colligative','Molality and Colligative Properties','🩸'],['ch12-props','Properties of Acids and Bases','🍋'],['ch12-bl','Brønsted–Lowry and Conjugate Pairs','🔄'],['ch12-strength','Strong and Weak Acids and Bases','💪'],['ch12-water','Water and Kw','💧'],['ch12-ph','pH and pOH','📏'],['ch12-buffers','Buffers','🛡️'],['ch13-rates','Reaction Rates and Collision Theory','💥'],['ch13-dynamic','Dynamic Equilibrium','⚖️'],['ch13-k','Equilibrium Constants','🔢'],['ch13-lechat','Le Chatelier\'s Principle','↔️'],['ch14-radiation','Radioactivity and Detection','☢️'],['ch14-decay','Nuclear Decay and Equations','⚛️'],['ch14-halflife','Half-Life','⏳'],['ch14-dating','Radiocarbon Dating','🦴'],['ch14-fission','Fission and Fusion','⚡'],['ch14-medicine','Radiation in Medicine','🏥']];
const title=P.get('title'),kicker=P.get('kicker');
if(title)$('#title').textContent=title;if(kicker)$('#kicker').textContent=kicker;
const g=GAMES[P.get('game')];if(g){const a=$('#gameLink');a.href=g[1];a.textContent='Play '+g[0]+' ↗';a.hidden=false}
document.title=(title||'Practice')+' — CHEM 3A';
const track=(topic,correct)=>{try{if(window.ddTrack)ddTrack({game:'textbook3a',course:'3A',mode:'Try it',topic,correct:!!correct})}catch(e){}};
const keyFull=P.get('key')||[...P.entries()].filter(([k])=>['t','ids','q'].includes(k)).map(([k,v])=>k+'='+v).join('&');
function hash(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return h>>>0}
const storeSuffix=keyFull.length<=80?keyFull:keyFull.slice(0,40)+'~'+hash(keyFull).toString(36);
async function bankMode(){
 const host=$('#host');host.innerHTML='<div class="rl-card">Loading questions…</div>';
 const ids=(P.get('ids')||'').split(',').filter(Boolean);
 let topics=(P.get('t')||'').split(',').filter(Boolean);
 const files=[...new Set((topics.length?topics:ids.map(i=>'ch'+i.split('-')[0].replace(/\D/g,'').padStart(2,'0'))).map(t=>t.split('-')[0]))];
 const fbxReady=load('js/fbx.js',()=>window.FBX);
 const lists=await Promise.all(files.map(f=>fetch('bank/'+f+'.json').then(r=>r.ok?r.json():[]).catch(e=>{console.error(e);return []})));
 let items=[].concat(...lists);
 if(topics.length)items=items.filter(q=>topics.includes(q.t));
 if(ids.length){const want=new Set(ids);items=items.filter(q=>want.has(q.id))}
 const rx=P.get('q');if(rx){let re;try{re=new RegExp(rx,'i')}catch(e){re=null}if(re)items=items.filter(q=>re.test(q.q+' '+q.c.join(' ')+' '+q.w))}
 const n=+P.get('n');
 if(n&&items.length>n&&P.get('fresh'))items=shuf(items).slice(0,n);
 else if(n&&items.length>n)items=items.map(q=>[q,hash(q.id+keyFull)]).sort((a,b)=>a[1]-b[1]).slice(0,n).map(a=>a[0]);
 if(!items.length){host.innerHTML='<div class="rl-card">No questions matched this widget. (Check the ?t= / ?ids= settings.)</div>';return}
 try{await fbxReady}catch(e){return loadFail(e)}
 host.innerHTML='';
 window.FBX.mount(host,items,{topics:TOPICS,storageKey:'tb3a-fbx-'+storeSuffix,onAnswer:(q,first,info)=>track(info.topic,first)});
 if(new Set(items.map(q=>q.t)).size===1){const s=host.querySelector('.fbx-tsel');if(s)s.hidden=true}
}
bankMode().catch(loadFail);
})();
