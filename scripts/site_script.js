'use strict';
const DATA=JSON.parse(document.getElementById('library-data').textContent);
const P=DATA.papers,CATS=DATA.categories,F=DATA.facets,VENUES=DATA.venues,$=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const external=(label,url,cls='')=>`<a class="${cls}" href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>`;
const category=id=>CATS.find(c=>c.id===id),hasWeights=p=>p.hw,publicCode=p=>'WRCU'.includes(p.st),officialTitle=p=>p.en||p.t;
const inTopic=(p,id)=>id==='all'||p.c===id||p.collections.includes(id),PAGE_SIZE=24;
const filterIds=['architecture','control','status','year','host','supervision','signal','sort'];
const defaults={view:'papers',cat:'all',q:'',status:'all',year:'all',host:'all',sort:'newest',architecture:'all',control:'all',supervision:'all',signal:'all',paper:'',venues:[]};
let state={...defaults},limit=PAGE_SIZE;
const topicCounts=Object.fromEntries(CATS.map(c=>[c.id,P.filter(p=>inTopic(p,c.id)).length]));
function hostOf(url){if(/github\.com/i.test(url))return'repo';if(/drive\.google|docs\.google/i.test(url))return'gdrive';if(/huggingface\.co/i.test(url))return'hf';if(/pan\.baidu|disk\.pku|terabox|aliyundrive|quark/i.test(url))return'cn';return'other'}
function readURL(){
  const q=new URLSearchParams(location.search);state={...defaults};
  if(['papers','datasets','tools','learn'].includes(q.get('view')))state.view=q.get('view');
  if(category(q.get('topic')))state.cat=q.get('topic');state.q=q.get('q')||'';
  for(const id of filterIds)if([...$(id).options].some(o=>o.value===q.get(id)))state[id]=q.get(id);
  const venues=(q.get('venues')||'').split(',');state.venues=VENUES.filter(v=>venues.includes(v.id)).map(v=>v.id);
  const id=q.get('paper')||location.hash.slice(1);if(P.some(p=>p.id===id)){state.paper=id;state.view='papers'}limit=PAGE_SIZE;
}
function writeURL(){const q=new URLSearchParams();for(const[k,v]of Object.entries(state)){if(k==='venues'){if(v.length)q.set(k,v.join(','))}else if(v!==defaults[k])q.set(k==='cat'?'topic':k,v)}const query=q.toString();try{history.replaceState(null,'',location.pathname+(query?'?'+query:'')+location.hash)}catch{}$('languageLink').href=ALT_FILE+(query?'?'+query:'')+location.hash}
function nav(){
 const button=(id,label,total)=>`<button type="button" class="topic" data-topic="${id}" aria-current="${state.cat===id&&state.view==='papers'}"><span>${esc(label)}</span><span class="count">${total}</span></button>`;
 $('topicNav').innerHTML=button('all',UI.all,P.length)+DATA.navigation.map(g=>`<section class="nav-group" aria-labelledby="nav-${g.id}"><h2 class="nav-label" id="nav-${g.id}">${esc(g.label)}</h2>${g.topics.map(id=>button(id,category(id).short,topicCounts[id])).join('')}</section>`).join('');
}
function initVenues(){
 const groups=['venueVision','venueLearning','venueImaging','venueWorkshops','venueJournals','venueOther','venuePreprints'];
 $('venueOptions').innerHTML=groups.map(key=>{const rows=VENUES.filter(v=>v.group===key);return rows.length?`<fieldset><legend>${esc(UI[key])}</legend><div>${rows.map(v=>`<label><input type="checkbox" name="venues" value="${v.id}"><span>${esc(v.title)}</span><small>${v.count}</small></label>`).join('')}</div></fieldset>`:''}).join('');
}
function renderVenues(){
 const selected=VENUES.filter(v=>state.venues.includes(v.id));
 $('venueSummary').textContent=!selected.length?UI.allVenues:selected.length<=2?selected.map(v=>v.title).join(' + '):`${UI.selectedVenues} · ${selected.length}`;
 $('venueSummary').title=selected.length?selected.map(v=>v.title).join(', '):UI.allVenues;
 $('venueFilter').classList.toggle('has-selection',!!selected.length);
 for(const input of $('venueOptions').querySelectorAll('input'))input.checked=state.venues.includes(input.value);
}
function searchable(p){const tags=Object.entries(p.facets).flatMap(([key,values])=>values.map(v=>`${v} ${F[key].values[v]}`));return[p.n,p.t,p.en,p.ens,p.s,p.v,p.y,p.note,p.g,category(p.c)?.title,category(p.c)?.id,...p.collections.map(id=>category(id)?.title),...tags,...p.ds,...p.impl.map(r=>`${r.n} ${r.s} ${r.g}`),...p.w.map(w=>w.label+' '+w.url)].join(' ').toLocaleLowerCase()}
function matches(text){return state.q.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean).every(t=>text.toLocaleLowerCase().includes(t))}
function filtered(){return P.filter(p=>(!state.paper||p.id===state.paper)&&inTopic(p,state.cat)&&(!state.venues.length||state.venues.includes(p.vk))&&(state.status==='all'||(state.status==='WR'?hasWeights(p):state.status.includes(p.st)))&&(state.year==='all'||String(p.y)===state.year)&&(state.host==='all'||p.w.some(w=>hostOf(w.url)===state.host))&&Object.keys(F).every(key=>state[key]==='all'||(state[key]==='unlabeled'?!p.facets[key].length:p.facets[key].includes(state[key])))&&matches(searchable(p))).sort((a,b)=>state.sort==='az'?officialTitle(a).localeCompare(officialTitle(b)):state.sort==='ready'?Number(hasWeights(b))-Number(hasWeights(a))||Number(publicCode(b))-Number(publicCode(a))||b.y-a.y||officialTitle(a).localeCompare(officialTitle(b)):b.y-a.y||officialTitle(a).localeCompare(officialTitle(b)))}
function facetButtons(p,keys){return keys.flatMap(key=>p.facets[key].map(v=>`<button type="button" class="method-tag tag-${key}" data-facet="${key}" data-value="${v}" aria-label="${esc(F[key].label+': '+F[key].values[v])}">${esc(F[key].values[v])}</button>`)).join('')}
function readingDetails(p){
 const impl=p.impl.length?`<section class="implementations"><h4>${esc(UI.implementation)}</h4>${p.impl.map(r=>`<div><strong>${esc(r.n)}</strong>${r.g?` ${external(UI.officialCode,r.g)}`:''}<p>${esc(r.s)}</p></div>`).join('')}</section>`:'';
 const downloads=p.w.length?`<span class="downloads"><span class="resource-label">${esc(UI.downloadWeights)}</span>${p.w.map(w=>external(w.label,w.url)).join('')}</span>`:'';
 const ds=p.ds.length?`<span class="related-datasets"><span class="resource-label">${esc(UI.relatedDatasets)}</span>${p.ds.map(n=>`<button type="button" class="inline-button" data-dataset="${esc(n)}">${esc(n)} ↗</button>`).join('')}</span>`:'';
 return`${impl}${downloads||ds?`<div class="paper-resources">${downloads}${ds}</div>`:''}${p.note?`<p class="paper-note">${esc(p.note)}</p>`:''}`;
}
function paperCard(p){
 const info=readingDetails(p);
 const codeLabel=p.st==='U'?UI.unofficialCode:p.st==='S'?UI.comingCode:UI.officialCode;
 const release=`<span class="paper-release"><span class="status status-${p.st}">${esc(p.st==='U'&&p.hw?UI.unofficialWeights:UI[p.st])}</span>${p.g?external(codeLabel,p.g,'code-link'):''}</span>`;
 return`<article class="paper-card" id="${p.id}" data-paper="${esc(p.n)}"><div class="paper-meta"><span class="paper-publication">${p.y} · ${esc(p.v)}</span><span>${esc(category(p.c)?.short)}</span>${facetButtons(p,['architecture','control','supervision','signal'])}${release}</div><h3 class="paper-name" lang="en">${external(officialTitle(p),p.p)}</h3>${p.en&&p.en!==p.t?`<p class="paper-translation">${esc(p.t)}</p>`:''}<p class="paper-summary">${esc(p.s)}</p>${info?`<div class="paper-info">${info}</div>`:''}</article>`;
}
function empty(){return`<div class="empty"><h3>${esc(UI.empty)}</h3><p>${esc(UI.emptyHint)}</p><button type="button" class="reset" data-reset>${esc(UI.reset)} ↺</button></div>`}
function renderPapers(){const rows=filtered(),shown=rows.slice(0,limit),cat=category(state.cat);$('resultTitle').textContent=cat?.title||UI.all;$('categoryDescription').hidden=!cat;$('categoryIntro').textContent=cat?.intro||'';$('categoryRules').textContent=cat?.description||'';$('resultCount').textContent=`${UI.showing} ${shown.length} ${UI.of} ${rows.length} ${UI.results}`;$('results').className='paper-list';$('results').innerHTML=shown.map(paperCard).join('')||empty();$('showMore').hidden=shown.length>=rows.length}
function renderResources(){const type=state.view;$('categoryDescription').hidden=true;$('showMore').hidden=true;$('resultTitle').textContent=UI[{datasets:'tabDatasets',tools:'tabTools',learn:'tabLearn'}[type]];let n=0,html='';if(type==='datasets'){const rows=DATA.datasets.filter(d=>matches(Object.values(d).join(' ')));n=rows.length;html=rows.map(d=>`<article class="resource-card"><div class="resource-meta">${d.year} / ${esc(category(d.task)?.short||UI.datasets)}</div><h3>${esc(d.name)}</h3><p>${esc(d.use)}</p><dl><dt>${esc(UI.source)}</dt><dd>${esc([d.capture,d.source].filter(Boolean).join(' · '))}</dd><dt>${esc(UI.size)}</dt><dd>${esc(d.size)}</dd></dl>${external(UI.download,d.url,'resource-link')}</article>`).join('')}else if(type==='tools'){const labels={raw:UI.toolRaw,isp:UI.toolIsp,learned:UI.toolLearned,editor:UI.toolEditor};const rows=DATA.tools.filter(t=>matches(Object.values(t).join(' ')));n=rows.length;html=rows.map(t=>`<article class="resource-card"><div class="resource-meta">${esc(labels[t.kind]||UI.tabTools)} / ${esc(t.language||'')}</div><h3>${external(t.name,t.url)}</h3><p>${esc(t.description)}</p></article>`).join('')}else{html=Object.entries(DATA.resources).map(([key,items])=>{const rows=key==='classic'?items.flatMap(g=>g.items.map(x=>({...x,stage:g.stage}))):items;const kept=rows.filter(x=>matches(Object.values(x).join(' ')));n+=kept.length;return kept.length?`<section class="learning-group"><h3>${esc(UI[key]||key)}</h3>${kept.map(x=>`<article class="learning-item">${external(x.name,x.url)}<p>${esc(x.description||x.stage||'')}</p><small>${esc(x.by||'')}</small></article>`).join('')}</section>`:''}).join('')}$('results').className=type==='learn'?'learning-list':'resource-grid';$('results').innerHTML=html||empty();$('resultCount').textContent=`${n} ${UI.results}`}
function activeFilters(){const chips=[];if(state.view==='papers'){if(state.cat!=='all')chips.push(['cat',category(state.cat).title]);if(state.paper)chips.push(['paper',officialTitle(P.find(p=>p.id===state.paper))]);for(const key of filterIds.filter(k=>k!=='sort'))if(state[key]!=='all')chips.push([key,$(key).selectedOptions[0].textContent]);for(const v of VENUES.filter(v=>state.venues.includes(v.id)))chips.push(['venue',v.title,v.id])}if(state.q)chips.push(['q',state.q]);$('activeFilters').hidden=!chips.length;$('activeFilters').innerHTML=chips.map(([key,label,value])=>`<button type="button" data-clear="${key}"${value?` data-value="${value}"`:''} aria-label="${esc(UI.clearOne+': '+label)}"><span>${esc(label)}</span> ×</button>`).join('')}
function render(){nav();renderVenues();document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===state.view)));$('paperFilters').hidden=state.view!=='papers';$('search').value=state.q;for(const id of filterIds)$(id).value=state[id];if(state.view==='papers')renderPapers();else renderResources();activeFilters();writeURL()}
function clearPaper(){state.paper='';if(location.hash.startsWith('#paper-'))history.replaceState(null,'',location.pathname+location.search+'#library')}
function closeMenu(){const wasOpen=$('sidebar').classList.contains('open');$('sidebar').classList.remove('open');$('backdrop').classList.remove('open');$('menuButton').setAttribute('aria-expanded','false');if(wasOpen)$('menuButton').focus()}
function selectTopic(id){state={...state,view:'papers',cat:category(id)?id:'all'};clearPaper();limit=PAGE_SIZE;closeMenu();render();$('library').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'})}
function reset(){state={...defaults,view:state.view};clearPaper();limit=PAGE_SIZE;render()}
$('languageLink').lang=document.documentElement.lang==='en'?'zh-CN':'en';
initVenues();
$('venueOptions').addEventListener('change',()=>{state.venues=[...$('venueOptions').querySelectorAll('input:checked')].map(input=>input.value);clearPaper();limit=PAGE_SIZE;render()});
$('venueFilter').addEventListener('click',e=>{if(e.target.closest('[data-venue-preset]')){state.venues=['cvpr','iccv','eccv'];clearPaper();limit=PAGE_SIZE;render()}if(e.target.closest('[data-venue-clear]')){state.venues=[];clearPaper();limit=PAGE_SIZE;render()}});
document.addEventListener('click',e=>{if(!$('venueFilter').contains(e.target))$('venueFilter').open=false});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&$('venueFilter').open){$('venueFilter').open=false;$('venueSummary').focus()}});
$('year').insertAdjacentHTML('beforeend',[...new Set(P.map(p=>p.y))].sort((a,b)=>b-a).map(y=>`<option value="${y}">${y}</option>`).join(''));
for(const[key,facet]of Object.entries(F))$(key).insertAdjacentHTML('beforeend',Object.entries(facet.values).map(([v,label])=>`<option value="${v}">${esc(label)}</option>`).join('')+`<option value="unlabeled">${esc(UI.unlabeled)}</option>`);
$('trends').innerHTML=DATA.trends.map((t,i)=>`<article class="trend"><div class="trend-num">${String(i+1).padStart(2,'0')}</div><h3>${esc(t.title)}</h3><p>${esc(t.text)}</p><p class="examples">${esc(t.examples)}</p></article>`).join('');
$('topicNav').addEventListener('click',e=>{const b=e.target.closest('[data-topic]');if(b)selectTopic(b.dataset.topic)});
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{state.view=b.dataset.view;state.q='';clearPaper();limit=PAGE_SIZE;render()}));
$('search').addEventListener('input',e=>{state.q=e.target.value;clearPaper();limit=PAGE_SIZE;render()});
for(const id of filterIds)$(id).addEventListener('change',e=>{state[id]=e.target.value;clearPaper();limit=PAGE_SIZE;render()});
$('reset').addEventListener('click',reset);
$('activeFilters').addEventListener('click',e=>{const b=e.target.closest('[data-clear]');if(!b)return;if(b.dataset.clear==='venue')state.venues=state.venues.filter(id=>id!==b.dataset.value);else state[b.dataset.clear]=defaults[b.dataset.clear];clearPaper();limit=PAGE_SIZE;render();$('search').focus()});
$('results').addEventListener('click',e=>{
 if(e.target.closest('[data-reset]')){reset();return}
 const tag=e.target.closest('[data-facet]');if(tag){state[tag.dataset.facet]=tag.dataset.value;clearPaper();limit=PAGE_SIZE;render();$('search').focus();return}
 const ds=e.target.closest('[data-dataset]');if(ds){state.view='datasets';state.q=ds.dataset.dataset;clearPaper();render();$('library').scrollIntoView()}
});
$('showMore').addEventListener('click',()=>{limit+=PAGE_SIZE;renderPapers()});
$('menuButton').addEventListener('click',()=>{const open=$('sidebar').classList.toggle('open');$('backdrop').classList.toggle('open',open);$('menuButton').setAttribute('aria-expanded',String(open));if(open)$('topicNav').querySelector('button').focus()});$('backdrop').addEventListener('click',closeMenu);
document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)&&!e.ctrlKey&&!e.metaKey&&!e.altKey){e.preventDefault();$('search').focus()}if(e.key==='Escape')closeMenu();if(e.key==='Tab'&&$('sidebar').classList.contains('open')){const focusable=[...$('sidebar').querySelectorAll('a,button')],first=focusable[0],last=focusable.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}});
window.addEventListener('popstate',()=>{readURL();render()});
window.addEventListener('hashchange',()=>{if(location.hash.startsWith('#paper-')){readURL();render();$(state.paper)?.scrollIntoView()}});
readURL();render();if(state.paper)requestAnimationFrame(()=>$(state.paper)?.scrollIntoView());
