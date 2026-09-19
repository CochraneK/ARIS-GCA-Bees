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

  function sortCards(cards, sort){
    if(sort === "progress-desc") cards.sort((a,b)=>Number(b.dataset.progress)-Number(a.dataset.progress));
    else if(sort === "progress-asc") cards.sort((a,b)=>Number(a.dataset.progress)-Number(b.dataset.progress));
    else if(sort === "recent") cards.sort((a,b)=>new Date(b.dataset.lastCommit||0)-new Date(a.dataset.lastCommit||0));
    else if(sort === "activity"){
      const rank={active:0,gated:1,blocked:2,quiet:3};
      cards.sort((a,b)=>(rank[a.dataset.activity]??9)-(rank[b.dataset.activity]??9)||String(a.dataset.id).localeCompare(String(b.dataset.id)));
    }else cards.sort((a,b)=>String(a.dataset.id).localeCompare(String(b.dataset.id)));
    return cards;
  }

  function apply(){
    const q = ($("searchInput")?.value || "").trim().toLowerCase();
    const sort = $("sortFilter")?.value || "id";
    const grid = $("paperGrid");
    const showcaseTrack = $("showcaseTrack");
    const showcaseSection = $("showcaseSection");
    const portfolioSection = $("portfolioSection");
    const hero = document.querySelector(".hero");
    const cards = [...grid.querySelectorAll(".paper-card")];

    // The portfolio summary belongs only to the top-level overview.
    // Category views should open directly into their working project cards.
    hero?.classList.toggle("hidden", currentFilter !== "all");

    cards.forEach(card => {
      const hay = (card.dataset.search || "").toLowerCase();
      const visible = matchesFilter(card) && (!q || hay.includes(q));
      card.classList.toggle("hidden", !visible);
    });

    const visible = cards.filter(c => !c.classList.contains("hidden"));
    sortCards(cards, sort).forEach(c=>grid.appendChild(c));

    const useShowcase = currentFilter === "all" && !q;
    showcaseSection?.classList.toggle("hidden", !useShowcase);
    portfolioSection?.classList.toggle("hidden", useShowcase);

    if(useShowcase && showcaseTrack){
      const showcaseCards=[...showcaseTrack.querySelectorAll('.showcase-card[data-showcase-original="true"]')];
      sortCards(showcaseCards, sort).forEach(c=>showcaseTrack.appendChild(c));
    }

    $("resultCount").textContent = (useShowcase ? cards.length : visible.length) + " / " + cards.length + " projects";
    $("emptyState").classList.toggle("hidden", useShowcase || visible.length !== 0);
    refreshShowcase();
  }

  function counts(){
    const cards=[...document.querySelectorAll(".paper-card")];
    const count = activity => cards.filter(c=>c.dataset.activity===activity).length;
    const statusCounts={
      active:count("active"),
      gated:count("gated"),
      quiet:count("quiet"),
      blocked:count("blocked")
    };
    const meceTotal=Object.values(statusCounts).reduce((sum,n)=>sum+n,0);

    $("navAllCount").textContent=cards.length;
    $("navActiveCount").textContent=statusCounts.active;
    $("navGatedCount").textContent=statusCounts.gated;
    $("navQuietCount").textContent=statusCounts.quiet;
    $("navBlockedCount").textContent=statusCounts.blocked;

    document.documentElement.dataset.statusMece=meceTotal===cards.length?"valid":"invalid";
    if(meceTotal!==cards.length){
      console.warn("ARIS4C status taxonomy is not MECE:", {all:cards.length, ...statusCounts, total:meceTotal});
    }
  }


  function initShowcase(){
    const section=$("showcaseSection");
    const viewport=$("showcaseViewport");
    const track=$("showcaseTrack");
    if(!section || !viewport || !track) return;

    const prefersReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let raf=0;
    let lastTs=0;
    let paused=false;
    let loopWidth=0;
    let resizeTimer=0;
    const speedPxPerSecond=22;

    const originals=()=>[...track.querySelectorAll('.showcase-card[data-showcase-original="true"]')];

    const removeClones=()=>{
      track.querySelectorAll(".showcase-clone").forEach(x=>x.remove());
    };

    const stopLoop=()=>{
      paused=true;
      if(raf){ cancelAnimationFrame(raf); raf=0; }
    };

    const frame=ts=>{
      if(paused || prefersReduced || section.classList.contains("hidden")){ raf=0; return; }
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
      if(prefersReduced || raf || section.classList.contains("hidden")) return;
      lastTs=0;
      raf=requestAnimationFrame(frame);
    }

    const rebuild=()=>{
      if(raf){ cancelAnimationFrame(raf); raf=0; }
      removeClones();
      viewport.scrollLeft=0;
      loopWidth=0;

      if(section.classList.contains("hidden") || prefersReduced) return;

      const cards=originals();
      if(!cards.length) return;

      cards.forEach(card=>{
        const clone=card.cloneNode(true);
        clone.classList.add("showcase-clone");
        clone.removeAttribute("data-showcase-original");
        clone.setAttribute("aria-hidden","true");
        clone.querySelectorAll("a,button,[tabindex]").forEach(el=>el.tabIndex=-1);
        track.appendChild(clone);
      });

      loopWidth=track.scrollWidth/2;
      if(!paused) startLoop();
    };

    const stepSize=()=>{
      const card=originals()[0];
      if(!card) return Math.min(viewport.clientWidth*.85,320);
      const gap=parseFloat(getComputedStyle(track).gap||"12")||12;
      return card.getBoundingClientRect().width+gap;
    };

    const nudge=dir=>{
      stopLoop();
      const step=stepSize();
      if(dir<0 && loopWidth>0 && viewport.scrollLeft<step){
        viewport.scrollLeft += loopWidth;
      }
      viewport.scrollBy({left:dir*step,behavior:prefersReduced?"auto":"smooth"});
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
      const shouldRun=!section.classList.contains("hidden");
      paused=!shouldRun;
      rebuild();
      if(shouldRun) startLoop();
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
