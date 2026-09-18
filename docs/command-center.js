(() => {
  const $ = id => document.getElementById(id);
  let currentFilter = "all";

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
    else if(sort === "activity"){
      const rank={active:0,gated:1,blocked:2,quiet:3};
      cards.sort((a,b)=>(rank[a.dataset.activity]??9)-(rank[b.dataset.activity]??9)||String(a.dataset.id).localeCompare(String(b.dataset.id)));
    }else cards.sort((a,b)=>String(a.dataset.id).localeCompare(String(b.dataset.id)));

    cards.forEach(c=>grid.appendChild(c));
    $("resultCount").textContent = visible.length + " / " + cards.length + " projects";
    $("emptyState").classList.toggle("hidden", visible.length !== 0);
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
  apply();
})();
