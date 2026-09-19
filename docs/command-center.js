(() => {
  const $ = id => document.getElementById(id);
  let currentFilter = "all";
  let refreshShowcase = () => {};

  function removeLegacyNearFinal(){
    document.querySelectorAll("[data-filter=\"near-final\"], #navNearCount").forEach(el=>{
      const button=el.closest("button");
      (button || el).remove();
    });
    document.querySelectorAll(".legend-row, .metric, .filter-chip").forEach(el=>{
      if(/near[- ]?final/i.test(el.textContent || "")) el.remove();
    });
  }

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
      const rank={active:0,wait:1,block:2,finish:3};
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
    const historySection = $("progressHistorySection");
    const cards = [...grid.querySelectorAll(".paper-card")];

    // The portfolio summary belongs only to the top-level overview.
    // Category views should open directly into their working project cards.
    hero?.classList.toggle("hidden", currentFilter !== "all");
    historySection?.classList.toggle("hidden", currentFilter !== "all" || Boolean(q));

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

    const portfolioTitle=$("portfolioTitle");
    if(portfolioTitle && !useShowcase){
      portfolioTitle.textContent = q
        ? "Search results"
        : (document.querySelector("[data-filter].is-active")?.dataset.label || "Project portfolio");
    }
    $("resultCount").textContent = (useShowcase ? cards.length : visible.length) + " / " + cards.length + " projects";
    $("emptyState").classList.toggle("hidden", useShowcase || visible.length !== 0);
    refreshShowcase();
  }

  function counts(){
    const cards=[...document.querySelectorAll("#paperGrid > .paper-card")];
    const count = activity => cards.filter(c=>c.dataset.activity===activity).length;
    const statusCounts={
      finish:count("finish"),
      active:count("active"),
      wait:count("wait"),
      block:count("block")
    };
    const meceTotal=Object.values(statusCounts).reduce((sum,n)=>sum+n,0);

    $("navAllCount").textContent=cards.length;
    $("navFinishCount").textContent=statusCounts.finish;
    $("navActiveCount").textContent=statusCounts.active;
    $("navWaitCount").textContent=statusCounts.wait;
    $("navBlockCount").textContent=statusCounts.block;

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


  function initProgressHistory(){
    const raw=$("progressHistoryData")?.textContent || "";
    const svg=$("progressHistoryChart");
    const legend=$("progressHistoryLegend");
    const summary=$("progressHistorySummary");
    if(!raw || !svg || !legend) return;

    let data;
    try{ data=JSON.parse(raw); }catch(err){ console.warn("Invalid progress history",err); return; }
    const points=Array.isArray(data.points)?data.points:[];
    if(!points.length){
      svg.innerHTML='<text x="500" y="165" text-anchor="middle" class="history-empty">No dashboard checkpoints for today yet.</text>';
      if(summary) summary.textContent="No checkpoints today";
      return;
    }

    const ids=[...new Set(points.flatMap(p=>Object.keys(p.projects||{})))].sort((a,b)=>a.localeCompare(b));
    const palette=[
      "#2563eb","#7c3aed","#0891b2","#059669","#65a30d","#ca8a04",
      "#ea580c","#dc2626","#db2777","#9333ea","#4f46e5","#0284c7",
      "#0d9488","#16a34a","#84cc16","#d97706","#e11d48","#6366f1"
    ];
    const colorFor=id=>palette[Math.max(0,ids.indexOf(id))%palette.length];
    const escHtml=value=>String(value??"").replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]));
    const fmtTime=value=>{
      const d=new Date(value);
      if(!Number.isFinite(d.getTime())) return "—";
      return d.toLocaleTimeString(undefined,{hour:"2-digit",minute:"2-digit"});
    };

    const W=1000,H=330,L=50,R=20,T=20,B=36;
    const innerW=W-L-R, innerH=H-T-B;
    const times=points.map(p=>new Date(p.timestamp).getTime()).filter(Number.isFinite);
    let minT=Math.min(...times), maxT=Math.max(...times);
    if(minT===maxT) maxT=minT+1;
    const x=t=>L+(new Date(t).getTime()-minT)/(maxT-minT)*innerW;
    const y=v=>T+(100-v)/100*innerH;

    const grid=[0,25,50,75,100].map(v=>`
      <line x1="${L}" y1="${y(v)}" x2="${W-R}" y2="${y(v)}" class="history-grid-line"/>
      <text x="${L-9}" y="${y(v)+4}" text-anchor="end" class="history-axis-label">${v}%</text>
    `).join("");

    const tickIndexes=[0,Math.floor((points.length-1)/3),Math.floor((points.length-1)*2/3),points.length-1]
      .filter((v,i,a)=>a.indexOf(v)===i);
    const labels=tickIndexes.map((idx,i)=>{
      const p=points[idx];
      const anchor=i===0?"start":i===tickIndexes.length-1?"end":"middle";
      return `<text x="${x(p.timestamp)}" y="${H-11}" text-anchor="${anchor}" class="history-axis-label">${escHtml(fmtTime(p.timestamp))}</text>`;
    }).join("");

    const paths=ids.map(id=>{
      const sp=points.map(p=>({p,value:Number(p.projects?.[id])})).filter(row=>Number.isFinite(row.value));
      if(!sp.length) return "";
      const d=sp.map((row,i)=>`${i?"L":"M"} ${x(row.p.timestamp).toFixed(1)} ${y(row.value).toFixed(1)}`).join(" ");
      const changed=sp.filter((row,i)=>i===0 || i===sp.length-1 || row.value!==sp[i-1].value);
      const dots=changed.map(row=>`<circle cx="${x(row.p.timestamp)}" cy="${y(row.value)}" r="2.8" fill="${colorFor(id)}" class="history-series-dot"><title>#${id} · ${row.value}% · ${escHtml(fmtTime(row.p.timestamp))}</title></circle>`).join("");
      return `<g data-history-series="${id}"><path d="${d}" class="history-series-line" stroke="${colorFor(id)}"><title>#${id}</title></path>${dots}</g>`;
    }).join("");

    svg.innerHTML=`<g>${grid}</g><g>${paths}</g><g>${labels}</g>`;

    const latest=points.at(-1)?.projects||{};
    legend.innerHTML=ids.map(id=>`
      <span class="history-legend-item" data-series="${id}">
        <i style="background:${colorFor(id)}"></i>
        <strong>#${id}</strong>
        <span>${Number.isFinite(Number(latest[id]))?Number(latest[id])+"%":"—"}</span>
      </span>
    `).join("");

    legend.querySelectorAll(".history-legend-item").forEach(item=>{
      item.addEventListener("mouseenter",()=>{
        const id=item.dataset.series;
        svg.querySelectorAll("[data-history-series]").forEach(g=>g.classList.toggle("history-series-muted",g.dataset.historySeries!==id));
      });
      item.addEventListener("mouseleave",()=>svg.querySelectorAll("[data-history-series]").forEach(g=>g.classList.remove("history-series-muted")));
    });

    if(summary){
      summary.textContent=`${data.date||"Today"} · ${points.length} checkpoints · ${ids.length} papers on one chart`;
    }
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

  removeLegacyNearFinal();
  initTheme();
  wire();
  counts();
  refreshCommitHeartbeats();
  apply();
  initShowcase();
  initProgressHistory();
  setInterval(refreshCommitHeartbeats, 60000);
})();
