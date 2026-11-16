from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'processed' / 'blinkit_cleaned.csv'
OUT = ROOT / 'dashboard' / 'index.html'

df = pd.read_csv(DATA)
cols = ['Item Fat Content','Item Identifier','Item Type','Outlet Establishment Year','Outlet Identifier','Outlet Location Type','Outlet Size','Outlet Type','Item Visibility','Item Weight','Sales','Rating']
records = df[cols].to_dict(orient='records')
for r in records:
    for k,v in list(r.items()):
        if pd.isna(v): r[k] = None
        elif hasattr(v, 'item'): r[k] = v.item()

payload = json.dumps(records, separators=(',',':'))
html = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Blinkit | Sales & Outlet Insights</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
:root{--bg:#f5f7f6;--card:#fff;--ink:#17211d;--muted:#6b7771;--green:#0c8b53;--lime:#c7ef4b;--line:#e5ebe7;--shadow:0 8px 28px rgba(20,50,35,.06)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);font:14px/1.45 Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Arial;color:var(--ink)}
header{background:#092d20;color:white;padding:26px clamp(18px,4vw,54px) 24px;position:relative;overflow:hidden}header:after{content:"";position:absolute;width:330px;height:330px;border-radius:50%;background:rgba(199,239,75,.12);right:8%;top:-220px}
.eyebrow{color:var(--lime);font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:11px}h1{font-size:clamp(24px,4vw,36px);margin:7px 0 5px;letter-spacing:-.03em}header p{margin:0;color:#c6d7ce;max-width:760px}
main{max-width:1440px;margin:auto;padding:24px clamp(14px,3vw,40px) 48px}.toolbar{display:flex;gap:12px;align-items:end;flex-wrap:wrap;background:var(--card);padding:16px;border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);margin-bottom:18px}.filter{display:flex;flex-direction:column;gap:5px;min-width:155px;flex:1}.filter label{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:700}select,button{height:38px;border:1px solid #d9e2dc;border-radius:8px;background:#fff;padding:0 10px;color:var(--ink);font:inherit}button{background:var(--green);border-color:var(--green);color:white;font-weight:700;padding:0 16px;cursor:pointer}.meta{margin-left:auto;color:var(--muted);font-size:12px;align-self:center}
.kpis{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin-bottom:18px}.kpi,.panel{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow)}.kpi{padding:17px 18px}.kpi .label{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:700}.kpi .value{font-size:clamp(20px,2.4vw,29px);font-weight:800;letter-spacing:-.04em;margin-top:8px}.kpi .hint{font-size:11px;color:var(--muted);margin-top:2px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.panel{padding:14px 14px 6px;min-width:0}.panel h2{font-size:14px;margin:2px 4px 0}.panel .sub{font-size:11px;color:var(--muted);margin:2px 4px 0}.chart{height:310px;width:100%}.wide{grid-column:1/-1}.insights{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:14px}.insight{background:#eef6f0;border:1px solid #dcebe0;border-radius:12px;padding:15px}.insight b{display:block;font-size:12px;margin-bottom:5px}.insight span{font-size:12px;color:#52635a}.foot{font-size:11px;color:var(--muted);margin:20px 3px 0;max-width:1000px}
@media(max-width:900px){.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.grid{grid-template-columns:1fr}.wide{grid-column:auto}.insights{grid-template-columns:1fr}}
@media(max-width:480px){.kpis{grid-template-columns:1fr 1fr}.kpi{padding:13px}.chart{height:280px}.meta{margin-left:0;width:100%}}
</style></head><body>
<header><div class="eyebrow">Retail analytics • Portfolio dashboard</div><h1>Blinkit Sales & Outlet Insights</h1><p>Explore sales performance across product categories, outlet formats and location tiers. Use the filters to focus the analysis.</p></header>
<main>
<section class="toolbar">
 <div class="filter"><label for="outlet">Outlet type</label><select id="outlet"><option value="All">All outlet types</option></select></div>
 <div class="filter"><label for="tier">Location tier</label><select id="tier"><option value="All">All tiers</option></select></div>
 <div class="filter"><label for="fat">Fat content</label><select id="fat"><option value="All">All types</option></select></div>
 <div class="filter"><label for="size">Outlet size</label><select id="size"><option value="All">All sizes</option></select></div>
 <button id="reset">Reset filters</button><div class="meta" id="rowcount"></div>
</section>
<section class="kpis">
 <div class="kpi"><div class="label">Total sales</div><div class="value" id="total">—</div><div class="hint">Sum of Sales field</div></div>
 <div class="kpi"><div class="label">Avg. sales / record</div><div class="value" id="avg">—</div><div class="hint">Not average order value</div></div>
 <div class="kpi"><div class="label">Average rating</div><div class="value" id="rating">—</div><div class="hint">Mean item/outlet rating</div></div>
 <div class="kpi"><div class="label">Unique products</div><div class="value" id="products">—</div><div class="hint">Distinct item identifiers</div></div>
 <div class="kpi"><div class="label">Unique outlets</div><div class="value" id="outlets">—</div><div class="hint">Distinct outlet identifiers</div></div>
</section>
<section class="grid">
 <article class="panel"><h2>Sales by item category</h2><div class="sub">Total sales, descending</div><div id="itemChart" class="chart"></div></article>
 <article class="panel"><h2>Sales by outlet type</h2><div class="sub">Compare outlet formats</div><div id="outletChart" class="chart"></div></article>
 <article class="panel"><h2>Sales by location tier</h2><div class="sub">Tier 1, Tier 2 and Tier 3</div><div id="tierChart" class="chart"></div></article>
 <article class="panel"><h2>Sales by fat content</h2><div class="sub">Low Fat versus Regular</div><div id="fatChart" class="chart"></div></article>
 <article class="panel wide"><h2>Sales by outlet establishment year</h2><div class="sub">Outlet cohort comparison — not a time series of sales transactions</div><div id="yearChart" class="chart"></div></article>
</section>
<section class="insights" id="insights"></section>
<p class="foot"><b>Data note:</b> The supplied dataset contains 8,523 item/outlet records, sales, ratings and outlet attributes. It has no transaction date, order ID, units sold, cost or profit fields. Accordingly, this report does not present sales trends over time, average order value, profit or causal claims. Dashboard charts use the cleaned dataset included in this project. Plotly is loaded from its public CDN, so an internet connection is needed to render charts.</p>
</main>
<script>
const DATA = __DATA__;
const fields={outlet:'Outlet Type',tier:'Outlet Location Type',fat:'Item Fat Content',size:'Outlet Size'};
const fmt=n=>new Intl.NumberFormat('en-IN',{maximumFractionDigits:0}).format(n);
const money=n=>'₹'+new Intl.NumberFormat('en-IN',{maximumFractionDigits:0}).format(n);
function unique(field){return [...new Set(DATA.map(d=>d[field]).filter(x=>x!==null))].sort()}
Object.entries(fields).forEach(([id,f])=>unique(f).forEach(v=>{let o=document.createElement('option');o.value=v;o.textContent=v;document.getElementById(id).appendChild(o)}));
function filtered(){return DATA.filter(d=>Object.entries(fields).every(([id,f])=>{let v=document.getElementById(id).value;return v==='All'||d[f]===v}))}
function group(rows,key){let m=new Map();rows.forEach(r=>m.set(r[key],(m.get(r[key])||0)+Number(r.Sales||0)));return [...m.entries()].sort((a,b)=>b[1]-a[1])}
const base={paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{family:'Inter,Arial',color:'#56645c',size:11},margin:{l:55,r:18,t:10,b:65},xaxis:{gridcolor:'#edf1ee',zeroline:false},yaxis:{gridcolor:'#edf1ee',zeroline:false},showlegend:false};
function bar(id,rows,key,horizontal=false){let g=group(rows,key);let x=horizontal?g.map(x=>x[1]).reverse():g.map(x=>x[0]);let y=horizontal?g.map(x=>x[0]).reverse():g.map(x=>x[1]);let trace={type:'bar',orientation:horizontal?'h':'v',x,y,marker:{color:horizontal?'#0c8b53':'#19a66a',line:{width:0}},hovertemplate:horizontal?'%{y}<br>Sales: ₹%{x:,.0f}<extra></extra>':'%{x}<br>Sales: ₹%{y:,.0f}<extra></extra>'};Plotly.react(id,[trace],{...base,margin:horizontal?{l:145,r:18,t:8,b:35}:base.margin,xaxis:{...base.xaxis,tickangle:horizontal?0:-25},yaxis:{...base.yaxis,tickprefix:horizontal?'₹':''}}, {displayModeBar:false,responsive:true})}
function donut(id,rows,key){let g=group(rows,key);Plotly.react(id,[{type:'pie',labels:g.map(x=>x[0]),values:g.map(x=>x[1]),hole:.58,textinfo:'label+percent',marker:{colors:['#0c8b53','#c7ef4b','#80c7a1','#d8e8df']},hovertemplate:'%{label}<br>Sales: ₹%{value:,.0f}<extra></extra>'}],{...base,showlegend:true,legend:{orientation:'h',y:-.18},margin:{l:10,r:10,t:10,b:30}}, {displayModeBar:false,responsive:true})}
function render(){let rows=filtered(),total=rows.reduce((s,r)=>s+Number(r.Sales||0),0),avg=rows.length?total/rows.length:0,rate=rows.length?rows.reduce((s,r)=>s+Number(r.Rating||0),0)/rows.length:0;
document.getElementById('total').textContent=money(total);document.getElementById('avg').textContent=money(avg);document.getElementById('rating').textContent=rate.toFixed(2)+'/5';document.getElementById('products').textContent=fmt(new Set(rows.map(r=>r['Item Identifier'])).size);document.getElementById('outlets').textContent=fmt(new Set(rows.map(r=>r['Outlet Identifier'])).size);document.getElementById('rowcount').textContent=fmt(rows.length)+' of '+fmt(DATA.length)+' records';
bar('itemChart',rows,'Item Type',true);bar('outletChart',rows,'Outlet Type',true);bar('tierChart',rows,'Outlet Location Type');donut('fatChart',rows,'Item Fat Content');
let yrs=group(rows,'Outlet Establishment Year').sort((a,b)=>a[0]-b[0]);Plotly.react('yearChart',[{type:'bar',x:yrs.map(x=>String(x[0])),y:yrs.map(x=>x[1]),marker:{color:'#0c8b53'},hovertemplate:'Established %{x}<br>Sales: ₹%{y:,.0f}<extra></extra>'}],{...base,xaxis:{...base.xaxis,title:'Outlet establishment year'},yaxis:{...base.yaxis,tickprefix:'₹'}},{displayModeBar:false,responsive:true});
let top=group(rows,'Item Type')[0], low=group(rows,'Item Type').slice(-1)[0], outlet=group(rows,'Outlet Type')[0];let cards=[['Leading category',top?`${top[0]} contributes ${money(top[1])} in sales.`:'No data for this selection.'],['Lowest category',low?`${low[0]} records the lowest category total (${money(low[1])}).`:'No data for this selection.'],['Leading outlet format',outlet?`${outlet[0]} contributes ${money(outlet[1])} in sales.`:'No data for this selection.']];document.getElementById('insights').innerHTML=cards.map(c=>`<div class="insight"><b>${c[0]}</b><span>${c[1]}</span></div>`).join('');}
Object.keys(fields).forEach(id=>document.getElementById(id).addEventListener('change',render));document.getElementById('reset').addEventListener('click',()=>{Object.keys(fields).forEach(id=>document.getElementById(id).value='All');render()});render();
</script></body></html>'''.replace('__DATA__', payload)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding='utf-8')
print(f'Created {OUT} ({OUT.stat().st_size:,} bytes)')
