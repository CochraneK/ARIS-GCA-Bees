(() => {
  const $ = id => document.getElementById(id);
  let currentFilter = "all";
  let refreshShowcase = () => {};

  function setTheme(theme){
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("aris4c-theme", theme);
  }

  function initTheme(){
    const saved = localStorage.getItem("aris4c-theme");
    if(saved){ setTheme(saved); return; }
    const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    setTheme(prefersDark ? "dark" : "light");
  }

  function matchesFilter(card){
    const activity = card.dataset.activity || "";
    const progress = Number(card.dataset.progress || 0);
    if(currentFilter === "all") return true;
    if(currentFilter === "near-final") return progress >= 85;
    return activity === currentFilter;
  }

  function relativeAge(value){
    if(!value) return "unknown";
    const then = new Date(value).getTime();
    if(!Number.isFinite(then)) return "unknown";
    const ms = Math.max(0, Date.now() - then);
    const min = Math.floor(ms / 60000);
    if(min < 1) return "just now";
    if(min < 60) return min + "m ago";
    const hr = Math.floor(min / 60);
    if(hr < 24) return hr + "h ago";
    const day = Math.floor(hr / 24);
    if(day < 30) return day + "d ago";
    return Math.floor(day / 30) + "mo ago";
  }

  function refreshCommitHeartbeats(){
    document.querySelectorAll(".commit-heartbeat").forEach(el=>{
      const value=el.dataset.commitTime || "";
      el.textContent="Last commit · "+relativeAge(value);
      el.title=value || "No commit timestamp available";
    });
  }

  function apply(){
    const q = ($("searchInput")?.value || "").trim().toLowerCase();
    const sort = $("sortFilter")?.value || "id";
    const grid = $("paperGrid");
    let cards = [...document.querySelectorAll(".paper-card")];

    cards.forEach(card => {
      const hay = (card.dataset.search || "").toLowerCase();
      const visible = matchesFilter(card) && (!q || hay.includes(q));
      card.classList.toggle("hidden", !visible);
    });

    const visible = cards.filter(c => !c.classList.contains("hidden"));
    if(sort === "progress-desc") cards.sort((a,b)=>Number(b.dataset.progress)-Number(a.dataset.progress));
    else if(sort === "progress-asc") cards.sort((a,b)=>Number(a.dataset.progress)-Number(b.dataset.progress));
    else if(sort === "recent") cards.sort((a,b)=>new Date(b.dataset.lastCommit||0)-new Date(a.dataset.lastCommit||0));
    else if(sort === "activity"){
      const rank={active:0,gated:1,blocked:2,quiet:3};
      cards.sort((a,b)=>(rank[a.dataset.activity]??9)-(rank[b.dataset.activity]??9)||String(a.dataset.id).localeCompare(String(b.dataset.id)));
    }else cards.sort((a,b)=>String(a.dataset.id).localeCompare(String(b.dataset.id)));

    cards.forEach(c=>grid.appendChild(c));
    $("resultCount").textContent = visible.length + " / " + cards.length + " projects";
    $("emptyState").classList.toggle("hidden", visible.length !== 0);
    refreshShowcase();
  }

  function counts(){
    const cards=[...document.querySelectorAll(".paper-card")];
    const count = activity => cards.filter(c=>c.dataset.activity===activity).length;
    $("navAllCount").textContent=cards.length;
    $("navActiveCount").textContent=count("active");
    $("navGatedCount").textContent=count("gated");
    $("navQuietCount").textContent=count("quiet");
    $("navBlockedCount").textContent=count("blocked");
    $("navNearCount").textContent=cards.filter(c=>Number(c.dataset.progress)>=85).length;
  }


  function initShowcase(){
    const viewport=$("showcaseViewport");
    const track=$("paperGrid");
    if(!viewport || !track) return;

    const prefersReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let raf=0;
    let lastTs=0;
    let paused=false;
    let loopWidth=0;
    let resizeTimer=0;
    const speedPxPerSecond=22;

    const originals=()=>[...track.querySelectorAll('.paper-card[data-showcase-original="true"]:not(.hidden)')];

    const removeClones=()=>{
      track.querySelectorAll(".showcase-clone").forEach(x=>x.remove());
    };

    const rebuild=()=>{
      const keepPaused=paused;
      if(raf){ cancelAnimationFrame(raf); raf=0; }
      removeClones();
      viewport.scrollLeft=0;
      loopWidth=0;

      const cards=originals();
      if(!cards.length || prefersReduced){
        document.querySelector(".showcase")?.classList.toggle("is-paused",prefersReduced || keepPaused);
        return;
      }

      cards.forEach(card=>{
        const clone=card.cloneNode(true);
        clone.classList.remove("paper-card");
        clone.classList.add("showcase-clone");
        clone.removeAttribute("data-showcase-original");
        clone.setAttribute("aria-hidden","true");
        clone.querySelectorAll("a,button,[tabindex]").forEach(el=>el.tabIndex=-1);
        track.appendChild(clone);
      });

      loopWidth=track.scrollWidth/2;
      lastTs=0;
      if(!keepPaused) startLoop();
    };

    const frame=ts=>{
      if(paused || prefersReduced){ raf=0; return; }
      if(!lastTs) lastTs=ts;
      const dt=Math.min(50,ts-lastTs);
      lastTs=ts;
      viewport.scrollLeft += speedPxPerSecond*dt/1000;
      if(loopWidth>0 && viewport.scrollLeft>=loopWidth){
        viewport.scrollLeft -= loopWidth;
      }
      raf=requestAnimationFrame(frame);
    };

    function startLoop(){
      paused=false;
      document.querySelector(".showcase")?.classList.remove("is-paused");
      if(prefersReduced || raf) return;
      lastTs=0;
      raf=requestAnimationFrame(frame);
    }

    const stopLoop=()=>{
      paused=true;
      document.querySelector(".showcase")?.classList.add("is-paused");
      if(raf){ cancelAnimationFrame(raf); raf=0; }
    };

    const stepSize=()=>{
      const card=originals()[0];
      if(!card) return Math.min(viewport.clientWidth*.85,320);
      const gap=parseFloat(getComputedStyle(track).gap||"12")||12;
      return card.getBoundingClientRect().width+gap;
    };

    const nudge=dir=>{
      stopLoop();
      viewport.scrollBy({left:dir*stepSize(),behavior:prefersReduced?"auto":"smooth"});
      window.setTimeout(startLoop,1600);
    };

    $("showcasePrev")?.addEventListener("click",()=>nudge(-1));
    $("showcaseNext")?.addEventListener("click",()=>nudge(1));
    viewport.addEventListener("mouseenter",stopLoop);
    viewport.addEventListener("mouseleave",startLoop);
    viewport.addEventListener("focusin",stopLoop);
    viewport.addEventListener("focusout",startLoop);
    viewport.addEventListener("pointerdown",stopLoop,{passive:true});
    viewport.addEventListener("pointerup",()=>window.setTimeout(startLoop,800),{passive:true});
    viewport.addEventListener("pointercancel",()=>window.setTimeout(startLoop,800),{passive:true});
    document.addEventListener("visibilitychange",()=>document.hidden?stopLoop():startLoop());
    window.addEventListener("resize",()=>{
      window.clearTimeout(resizeTimer);
      resizeTimer=window.setTimeout(rebuild,180);
    });

    refreshShowcase=()=>{
      const wasPaused=paused;
      paused=true;
      rebuild();
      paused=wasPaused;
      if(!wasPaused) startLoop();
    };

    paused=false;
    rebuild();
  }

  function wire(){
    document.querySelectorAll("[data-filter]").forEach(btn=>{
      btn.addEventListener("click",()=>{
        currentFilter=btn.dataset.filter;
        document.querySelectorAll("[data-filter]").forEach(x=>x.classList.toggle("is-active",x===btn));
        $("currentViewLabel").textContent=btn.dataset.label || btn.textContent.trim();
        apply();
      });
    });
    $("searchInput")?.addEventListener("input",apply);
    $("sortFilter")?.addEventListener("change",apply);
    $("themeToggle")?.addEventListener("click",()=>setTheme(document.documentElement.dataset.theme==="dark"?"light":"dark"));
    $("clearFilters")?.addEventListener("click",()=>{
      currentFilter="all";
      $("searchInput").value="";
      $("sortFilter").value="id";
      document.querySelectorAll("[data-filter]").forEach(x=>x.classList.toggle("is-active",x.dataset.filter==="all"));
      $("currentViewLabel").textContent="All projects";
      apply();
    });
  }

  initTheme();
  wire();
  counts();
  refreshCommitHeartbeats();
  apply();
  initShowcase();
  setInterval(refreshCommitHeartbeats, 60000);
})();
