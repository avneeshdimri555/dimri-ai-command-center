/* DIMRI AI Persona Engine v2 — provider-ready persona builder */
(() => {
  const KEY = 'dimriPersonaEngineV2';
  const SLOT_KEY = 'dimriPersonaSlotsV2';
  const defaults = {
    name:'', niche:'Creator', gender:'Feminine', age:'Adult 25–34',
    face:'Soft oval', skin:'Warm medium', eyes:'Large almond', iris:'Hazel',
    hair:'Long wavy', hairColor:'Dark brown', body:'Balanced',
    outfit:'Modern casual', expression:'Warm smile', pose:'3/4 portrait',
    background:'Studio teal', lighting:'Cinematic soft', referenceCount:0,
    identityLocked:false, createdAt:null, updatedAt:null
  };
  let state = {...defaults};

  const options = {
    face:['Soft oval','Round','Heart','Square','Long oval'],
    skin:['Fair neutral','Light warm','Warm medium','Tan','Deep warm','Deep neutral'],
    eyes:['Large almond','Round expressive','Upturned','Deep set','Soft hooded'],
    iris:['Hazel','Brown','Dark brown','Green','Blue'],
    hair:['Long wavy','Long straight','Curly','Shoulder bob','Short textured','Braided'],
    hairColor:['Dark brown','Black','Chestnut','Honey brown','Auburn','Platinum'],
    body:['Balanced','Petite','Athletic','Curvy','Tall editorial'],
    outfit:['Modern casual','Streetwear','Luxury minimal','Activewear','Creator studio'],
    expression:['Warm smile','Natural neutral','Confident','Playful','Thoughtful'],
    pose:['3/4 portrait','Front portrait','Full body','Walking','Seated creator'],
    background:['Studio teal','Luxury interior','Outdoor golden hour','Clean white','Neon city'],
    lighting:['Cinematic soft','Golden hour','Clean daylight','Editorial contrast','Night neon']
  };

  const esc = s => String(s??'').replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  const read = () => { try { const x=JSON.parse(localStorage.getItem(KEY)||'null'); if(x) state={...defaults,...x}; } catch{} };
  const write = () => { state.updatedAt=new Date().toISOString(); localStorage.setItem(KEY,JSON.stringify(state)); };

  function slots(){
    try { return JSON.parse(localStorage.getItem(SLOT_KEY)||'[]'); } catch { return []; }
  }
  function saveSlots(v){ localStorage.setItem(SLOT_KEY,JSON.stringify(v)); }

  function ensureStyles(){
    if(document.getElementById('dimri-engine-css')) return;
    const s=document.createElement('style'); s.id='dimri-engine-css';
    s.textContent=`
      .de-wrap{margin:0 0 16px;background:linear-gradient(145deg,#0d2035,#091423 70%);border:1px solid #2b536d;border-radius:16px;box-shadow:0 22px 65px #0006;overflow:hidden}
      .de-top{padding:17px 18px 13px;border-bottom:1px solid #203b53;display:flex;justify-content:space-between;gap:14px;align-items:flex-start}
      .de-kicker{font-size:9px;letter-spacing:1.8px;color:#58dfd1;text-transform:uppercase}.de-title{font-size:19px;font-weight:850;margin-top:5px}.de-sub{font-size:10px;color:#8fa9bd;margin-top:5px;line-height:1.5}
      .de-badge{padding:6px 9px;border-radius:20px;border:1px solid #276b68;background:#0d2b30;color:#75e7d3;font-size:9px;white-space:nowrap}
      .de-slots{display:none;gap:6px;overflow:auto;padding:11px 14px;border-bottom:1px solid #1e364c;background:#091726}.de-slot{min-width:78px;height:46px;border:1px solid #263f58;background:#0d1d30;color:#8fa8bb;border-radius:9px;font-size:9px;text-align:left;padding:6px}.de-slot b{display:block;color:#dcebf6;font-size:9px}.de-slot.active{border-color:#39d9ef;background:#123447;box-shadow:0 0 0 1px #39d9ef33}.de-slot.saved{border-color:#286957}.de-slot.add{color:#68e0e4;border-style:dashed}
      .de-grid{display:grid;grid-template-columns:minmax(240px,.72fr) minmax(350px,1.28fr);gap:13px;padding:14px}.de-card{background:#091625;border:1px solid #213b54;border-radius:12px;padding:13px}.de-card h3{margin:0 0 9px;font-size:11px}.de-preview{min-height:390px;border-radius:11px;position:relative;overflow:hidden;background:radial-gradient(circle at 50% 28%,#234d61,#0a1828 68%);display:grid;place-items:center}
      .de-scene{display:none;width:220px;height:330px;position:relative;filter:drop-shadow(0 22px 20px #0008);transform:scale(.96)}.de-head{position:absolute;left:58px;top:55px;width:104px;height:132px;background:#d7a07e;border-radius:var(--face,48%) var(--face,48%) 48% 48%;box-shadow:inset -10px -5px 20px #7f4d3622}.de-hair{position:absolute;left:42px;top:30px;width:137px;height:155px;background:var(--hair,#241b20);border-radius:55% 55% 40% 40%;clip-path:var(--clip,polygon(0 0,100% 0,94% 72%,78% 55%,65% 77%,50% 56%,35% 78%,18% 55%,3% 73%));z-index:4}.de-eyes{position:absolute;z-index:6;top:111px;left:79px;display:flex;gap:30px}.de-eye{width:18px;height:12px;background:#f4f8f1;border-radius:50%;position:relative}.de-eye:after{content:'';position:absolute;width:7px;height:9px;border-radius:50%;background:var(--iris,#6d5a34);left:6px;top:1px}.de-mouth{position:absolute;z-index:6;top:158px;left:98px;width:27px;height:10px;border-bottom:3px solid #99525a;border-radius:50%}.de-neck{position:absolute;left:90px;top:177px;width:40px;height:50px;background:#bf8668;border-radius:0 0 13px 13px}.de-body{position:absolute;left:30px;top:213px;width:160px;height:118px;background:linear-gradient(115deg,#173c50,#396b78);clip-path:polygon(25% 0,75% 0,100% 100%,0 100%);border-radius:40px}.de-flower{position:absolute;z-index:8;left:152px;top:45px;font-size:20px;color:#f28bd5;text-shadow:0 0 12px #ef85d4}.de-label{position:absolute;left:10px;right:10px;bottom:10px;display:flex;justify-content:space-between;font-size:9px;color:#9db6c9}.de-controls{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.de-field{display:grid;gap:5px}.de-field label{font-size:9px;color:#a9bed0}.de-field select,.de-field input{width:100%;background:#07121f;border:1px solid #29445d;color:#eaf6ff;border-radius:8px;padding:9px;font-size:10px;outline:none}.de-field select:focus,.de-field input:focus{border-color:#35cadb}.de-actions{display:flex;flex-wrap:wrap;gap:7px;margin-top:11px}.de-btn{border:1px solid #294961;background:#11253a;color:#d9edf8;border-radius:8px;padding:9px 11px;font-size:9px;font-weight:800}.de-btn.primary{border:0;background:linear-gradient(110deg,#39d9ef,#40e0bd);color:#04121a}.de-btn.violet{border:0;background:linear-gradient(110deg,#8a74f7,#d278e7);color:#fff}.de-score{display:flex;gap:7px;align-items:center;margin-top:10px}.de-bar{flex:1;height:6px;background:#172c40;border-radius:10px;overflow:hidden}.de-bar i{display:block;height:100%;background:linear-gradient(90deg,#40e0bd,#39d9ef);border-radius:10px}.de-small{font-size:9px;color:#7e98ad;line-height:1.45}.de-concepts{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:10px}.de-concept{height:118px;border:1px solid #203c55;border-radius:8px;background:radial-gradient(circle at 50% 30%,#315e70,#0c1829 70%);position:relative;overflow:hidden}.de-concept .minihead{position:absolute;left:0;right:0;top:6px;text-align:center;font-size:8px;color:#cfe5f2}.de-concept .mini-face{position:absolute;width:43px;height:55px;border-radius:50%;background:#d7a07e;left:calc(50% - 21px);top:28px}.de-concept .mini-hair{position:absolute;width:57px;height:65px;border-radius:50%;background:var(--hair,#241b20);left:calc(50% - 28px);top:22px;opacity:.95}.de-concept .mini-body{position:absolute;width:80px;height:52px;background:#315c6c;left:calc(50% - 40px);top:78px;clip-path:polygon(25% 0,75% 0,100% 100%,0 100%)}.de-queue{display:grid;gap:7px;margin-top:9px}.de-q{display:flex;justify-content:space-between;gap:10px;padding:9px;background:#0b1a2c;border:1px solid #213a52;border-radius:8px}.de-q b{font-size:9px}.de-q span{font-size:8px;color:#73dccf}.de-note{margin-top:10px;padding:9px;border-radius:8px;background:#161c25;border:1px solid #51462d;color:#d7c28e;font-size:9px;line-height:1.45}
      @media(max-width:900px){.de-grid{grid-template-columns:1fr}.de-preview{min-height:330px}.de-concepts{grid-template-columns:repeat(2,1fr)}}@media(max-width:600px){.de-controls{grid-template-columns:1fr}.de-top{flex-direction:column}.de-slot{min-width:70px}.de-preview{min-height:300px}}
    `;
    document.head.appendChild(s);
  }

  function selectOptions(key){
    return options[key].map(x=>'<option>'+esc(x)+'</option>').join('');
  }

  function render(){
    const page=document.getElementById('page-creator'); if(!page) return;
    let root=document.getElementById('dimri-engine-root');
    if(!root){
      root=document.createElement('div'); root.id='dimri-engine-root'; root.className='de-wrap';
      page.insertBefore(root,page.querySelector('.stepper'));
    }
    const slotsArr=slots();
    const score=Math.min(100,35+(state.referenceCount*15)+(state.identityLocked?25:0)+(state.name?10:0)+(state.niche?10:0));
    root.innerHTML=`
      <div class="de-top">
        <div><div class="de-kicker">DIMRI PERSONA ENGINE · V2</div><div class="de-title">Build once. Keep the identity consistent.</div><div class="de-sub">Create one persona at a time. Use My Personas to manage saved profiles; generate real photos when the image provider is configured.</div></div>
        <span class="de-badge">Provider-ready architecture</span>
      </div>
      <div class="de-slots">
        <button class="de-slot add" data-de-new>＋ New persona</button>
        ${Array.from({length:50},(_,i)=>{
          const p=slotsArr[i]; const active=p&&p.id===state.id;
          return '<button class="de-slot '+(active?'active ':'')+(p?'saved':'')+'" data-de-slot="'+i+'"><b>Slot '+String(i+1).padStart(2,'0')+'</b>'+esc(p?.name||'Empty')+'</button>';
        }).join('')}
      </div>
      <div class="de-grid">
        <div class="de-card">
          <h3>Live visual blueprint</h3>
          <div class="de-preview" id="de-preview">
            <div class="de-scene" id="de-scene">
              <div class="de-hair"></div><div class="de-head"></div>
              <div class="de-eyes"><span class="de-eye"></span><span class="de-eye"></span></div>
              <div class="de-mouth"></div><div class="de-neck"></div><div class="de-body"></div><div class="de-flower">✿</div>
            </div>
            <div class="de-label"><span><b id="de-name-label">${esc(state.name||'New Persona')}</b><br>${esc(state.gender)} · ${esc(state.face)}</span><span>LIVE BLUEPRINT</span></div>
          </div>
          <div class="de-score"><span class="de-small">Identity strength</span><div class="de-bar"><i style="width:${score}%"></i></div><b style="font-size:9px">${score}%</b></div>
          <div class="de-actions">
            <button class="de-btn violet" data-de-generate>✨ Generate Real Photo</button><button class="de-btn" data-de-video>▷ Generate Video</button><button class="de-btn primary" data-de-lock>${state.identityLocked?'✓ Identity Locked':'🔒 Lock Identity'}</button>
            <button class="de-btn" data-de-save>Save Blueprint</button>
            <button class="de-btn violet" data-de-daily>＋ Daily Content Set</button>
          </div>
          <div id="de-real-output" style="margin-top:10px"></div><div class="de-note">The visual blueprint is an interactive design preview. Real photorealistic image/video generation is only activated when a provider is connected; the UI never pretends a mock image is a generated asset.</div>
        </div>
        <div class="de-card">
          <h3>Appearance &amp; creator DNA</h3>
          <div class="de-controls">
            <div class="de-field"><label>Persona name</label><input data-de-key="name" value="${esc(state.name)}" placeholder="e.g. Maya Kapoor"></div>
            <div class="de-field"><label>Content niche</label><input data-de-key="niche" value="${esc(state.niche)}" placeholder="Fashion, travel, beauty…"></div>
            <div class="de-field"><label>Gender presentation</label><select data-de-key="gender">${['Feminine','Masculine','Androgynous'].map(x=>'<option '+(x===state.gender?'selected':'')+'>'+x+'</option>').join('')}</select></div>
            <div class="de-field"><label>Age range</label><select data-de-key="age">${['Adult 18–24','Adult 25–34','Adult 35–44','Adult 45+'].map(x=>'<option '+(x===state.age?'selected':'')+'>'+x+'</option>').join('')}</select></div>
            ${['face','skin','eyes','iris','hair','hairColor','body','outfit','expression','pose','background','lighting'].map(k=>'<div class="de-field"><label>'+k.replace(/([A-Z])/g,' $1').replace(/^./,c=>c.toUpperCase())+'</label><select data-de-key="'+k+'">'+selectOptions(k).replace('<option>'+esc(state[k])+'</option>','<option selected>'+esc(state[k])+'</option>')+'</select></div>').join('')}
          </div>
          <div class="de-actions"><button class="de-btn violet" data-de-concepts>Generate 4 concepts</button><button class="de-btn" data-de-reference>Use reference library</button><button class="de-btn" data-de-open-dna>Open Persona DNA</button></div>
          <div class="de-small" style="margin-top:10px">Reference library → approved images become the identity anchor for future provider calls.</div>
          <div class="de-concepts" id="de-concepts"><div class="de-small" style="grid-column:1/-1">Generate concepts to compare four controlled visual directions.</div></div>
          <div class="de-queue" id="de-queue"></div>
        </div>
      </div>`;
    bind(root);
    renderQueue(root);
    applyVisual(root);
  }

  function applyVisual(root){
    const scene=root.querySelector('#de-scene'); if(!scene)return;
    const hairMap={'Long wavy':'polygon(0 0,100% 0,96% 78%,82% 54%,68% 83%,51% 58%,37% 84%,20% 56%,4% 79%)','Long straight':'polygon(0 0,100% 0,96% 100%,78% 80%,62% 100%,45% 82%,25% 100%,4% 88%)','Curly':'none','Shoulder bob':'polygon(0 0,100% 0,94% 82%,72% 62%,52% 78%,28% 60%,6% 85%)','Short textured':'polygon(0 0,100% 0,94% 58%,75% 42%,58% 60%,40% 40%,22% 62%,5% 48%)','Braided':'polygon(0 0,100% 0,90% 70%,72% 56%,55% 78%,38% 57%,18% 76%,4% 58%)'};
    const faceMap={'Soft oval':'48%','Round':'52%','Heart':'55% 45% 48% 48%','Square':'34%','Long oval':'42%'};
    const skinMap={'Fair neutral':'#f0c5a8','Light warm':'#e3b08f','Warm medium':'#d7a07e','Tan':'#b97959','Deep warm':'#8d583f','Deep neutral':'#6e4638'};
    const irisMap={'Hazel':'#75643a','Brown':'#4c3326','Dark brown':'#2b1c18','Green':'#3c765d','Blue':'#4f7595'};
    const bgMap={'Studio teal':'radial-gradient(circle at 50% 28%,#234d61,#0a1828 68%)','Luxury interior':'linear-gradient(145deg,#3a2d3e,#0c1728)','Outdoor golden hour':'linear-gradient(145deg,#704d35,#101a28)','Clean white':'linear-gradient(145deg,#536271,#0d1725)','Neon city':'radial-gradient(circle at 70% 25%,#59365d,#091321 68%)'};
    const head=scene.querySelector('.de-head'),hair=scene.querySelector('.de-hair');
    head.style.background=skinMap[state.skin]||skinMap['Warm medium'];
    head.style.borderRadius=faceMap[state.face]||'48%';
    hair.style.background=state.hairColor==='Black'?'#17151a':state.hairColor==='Chestnut'?'#4a2922':state.hairColor==='Honey brown'?'#8a5a32':state.hairColor==='Auburn'?'#6a3024':state.hairColor==='Platinum'?'#d6d0c8':'#241b20';
    hair.style.clipPath=hairMap[state.hair]||hairMap['Long wavy'];
    scene.style.setProperty('--iris',irisMap[state.iris]||'#6d5a34');
    root.querySelector('#de-preview').style.background=bgMap[state.background]||bgMap['Studio teal'];
    const mouth=root.querySelector('.de-mouth'); mouth.style.transform=state.expression==='Warm smile'?'scaleY(1.2)':state.expression==='Confident'?'rotate(-4deg)':state.expression==='Thoughtful'?'scaleY(.55)':'none';
    root.querySelector('#de-name-label').textContent=state.name||'New Persona';
  }

  function renderQueue(root){
    const q=JSON.parse(localStorage.getItem('dimriDailyQueueV2')||'[]').filter(x=>x.personaId===state.id).slice(0,5);
    const box=root.querySelector('#de-queue'); if(!box)return;
    box.innerHTML=q.length?'<div class="de-small">Latest production queue</div>'+q.map(x=>'<div class="de-q"><b>'+esc(x.type)+' · '+esc(x.title)+'</b><span>'+esc(x.status)+'</span></div>').join(''):'';
  }

  function saveBlueprint(){
    if(!state.name.trim()){window.alert('Give the persona a name first.');return}
    state.id=state.id||'persona-'+Date.now(); state.createdAt=state.createdAt||new Date().toISOString(); write();
    const a=slots(), existing=a.findIndex(x=>x?.id===state.id);
    const compact={...state,referenceCount:Number(state.referenceCount||0)};
    if(existing>=0)a[existing]=compact; else { const empty=a.findIndex(x=>!x); if(empty>=0)a[empty]=compact; else a.push(compact); }
    saveSlots(a.slice(0,50));
    try { if(window.draft){ Object.assign(window.draft,{name:state.name,niche:state.niche,gender:state.gender}); } } catch{}
    if(typeof window.toast==='function') window.toast('Persona Blueprint saved · Slot assigned');
    render();
  }

  function newPersona(){
    state={...defaults,id:'persona-'+Date.now(),createdAt:new Date().toISOString()};
    write(); render();
  }

  function loadSlot(i){
    const p=slots()[i]; if(!p){newPersona();return;}
    state={...defaults,...p}; write(); render();
  }

  function dailySet(){
    if(!state.id){state.id='persona-'+Date.now();}
    const q=JSON.parse(localStorage.getItem('dimriDailyQueueV2')||'[]');
    const now=Date.now();
    const items=[1,2,3].map((n,j)=>({id:'q-'+(now+j),personaId:state.id,type:'PHOTO '+n,title:state.niche+' concept '+n,status:'Awaiting provider'}));
    items.push({id:'q-'+(now+4),personaId:state.id,type:'VIDEO',title:state.niche+' short video',status:'Awaiting provider'});
    localStorage.setItem('dimriDailyQueueV2',JSON.stringify([...items,...q].slice(0,200)));
    if(typeof window.toast==='function') window.toast('Daily set queued: 3 photos + 1 video');
    render();
  }

  function concepts(){
    const root=document.getElementById('dimri-engine-root'), box=root?.querySelector('#de-concepts'); if(!box)return;
    const variants=[['Hero portrait','3/4 portrait'],['Lifestyle','Walking'],['Creator','Seated creator'],['Editorial','Full body']];
    box.innerHTML=variants.map((v,i)=>'<div class="de-concept" style="--hair:'+(i%2?'#4a2922':'#241b20')+'"><div class="minihead">'+v[0]+'</div><div class="mini-hair"></div><div class="mini-face"></div><div class="mini-body"></div></div>').join('');
    if(typeof window.toast==='function') window.toast('4 controlled concepts created · design previews');
  }


  async function generateRealPhoto(){
    const btn=document.querySelector('#dimri-engine-root [data-de-generate]');
    const out=document.getElementById('de-real-output');
    if(!btn||!out)return;
    btn.disabled=true; btn.textContent='Generating…';
    out.innerHTML='<div class="de-small">Calling the configured image provider securely from the backend…</div>';
    try{
      const api=(window.DIMRI_API_URL||'https://dimri-ai-god-board-api.onrender.com').replace(/\/$/,'');
      const response=await fetch(api+'/api/personas/generate-image',{
        method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({profile:state,scene:'premium creator social-media portrait',size:'1024x1536'})
      });
      const data=await response.json();
      if(!response.ok) throw new Error(data.detail||'Generation failed');
      const img=data.image||{};
      const src=img.b64_json?'data:image/png;base64,'+img.b64_json:img.url;
      if(!src) throw new Error('Provider returned no image');
      out.innerHTML='<div class="de-small" style="margin-bottom:6px">REAL PROVIDER OUTPUT · '+esc(img.model||'image model')+'</div><img src="'+esc(src)+'" alt="Generated persona" style="display:block;width:100%;max-height:560px;object-fit:contain;border-radius:10px;border:1px solid #28516b;background:#07101d">';
      if(typeof window.toast==='function')window.toast('Real persona photo generated');
    }catch(err){
      out.innerHTML='<div class="de-note">Generation unavailable: '+esc(err.message||String(err))+'</div>';
      if(typeof window.toast==='function')window.toast('Image generation unavailable');
    }finally{btn.disabled=false;btn.textContent='✨ Generate Real Photo';}
  }

  async function generateRealVideo(){
    const btn=document.querySelector('#dimri-engine-root [data-de-video]'), out=document.getElementById('de-real-output');
    if(!btn||!out)return;
    btn.disabled=true; btn.textContent='Starting…';
    try{
      const api=(window.DIMRI_API_URL||'https://dimri-ai-god-board-api.onrender.com').replace(/\/$/,'');
      const response=await fetch(api+'/api/personas/generate-video',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({profile:state,scene:'premium vertical social-media creator clip',seconds:'4',size:'720x1280'})});
      const data=await response.json(); if(!response.ok)throw new Error(data.detail||'Video generation failed');
      const v=data.video||{}; out.innerHTML='<div class="de-small">VIDEO JOB · '+esc(v.id||'queued')+' · '+esc(v.status||'queued')+'</div><div class="de-note">Sora video generation is asynchronous. Use the video job status endpoint to retrieve progress and the finished asset.</div>';
      if(typeof window.toast==='function')window.toast('Video generation job started');
    }catch(err){out.innerHTML='<div class="de-note">Video generation unavailable: '+esc(err.message||String(err))+'</div>';if(typeof window.toast==='function')window.toast('Video generation unavailable');}
    finally{btn.disabled=false;btn.textContent='▷ Generate Video';}
  }

  function bind(root){
    root.querySelectorAll('[data-de-key]').forEach(el=>{
      el.oninput=el.onchange=()=>{state[el.dataset.deKey]=el.value;write();applyVisual(root);};
    });
    root.querySelector('[data-de-generate]')?.addEventListener('click',generateRealPhoto);
    root.querySelector('[data-de-video]')?.addEventListener('click',generateRealVideo);
    root.querySelector('[data-de-lock]')?.addEventListener('click',()=>{state.identityLocked=!state.identityLocked;write();render();});
    root.querySelector('[data-de-save]')?.addEventListener('click',saveBlueprint);
    root.querySelector('[data-de-daily]')?.addEventListener('click',dailySet);
    root.querySelector('[data-de-concepts]')?.addEventListener('click',concepts);
    root.querySelector('[data-de-new]')?.addEventListener('click',newPersona);
    root.querySelector('[data-de-reference]')?.addEventListener('click',()=>{ const f=document.querySelector('input[type=file]'); if(f)f.click(); else if(typeof window.jumpStep==='function')window.jumpStep(7); });
    root.querySelector('[data-de-open-dna]')?.addEventListener('click',()=>{if(typeof window.go==='function')window.go('dna');});
    root.querySelectorAll('[data-de-slot]').forEach(b=>b.addEventListener('click',()=>loadSlot(Number(b.dataset.deSlot))));
  }

  read();
  ensureStyles();
  const boot=()=>{ if(document.getElementById('page-creator')) render(); };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
  window.addEventListener('storage',()=>{read();if(document.getElementById('page-creator')?.classList.contains('active'))render();});
})();