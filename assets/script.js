
async function loadJSON(path){ const r = await fetch(path); return r.json(); }

function fmtDate(iso){
  try{
    const d = new Date(iso);
    return d.toLocaleDateString(undefined, {year:'numeric', month:'short', day:'numeric'});
  }catch{ return iso; }
}

function linkForPaper(p){
  // Prefer direct paper link; otherwise fall back to venue homepage
  if (p.url && p.url.trim() !== "") return p.url;
  if (p.venue_url && p.venue_url.trim() !== "") return p.venue_url;
  return null;
}

function paperHTML(p){
  const url = linkForPaper(p);
  const title = p.title || "Untitled";
  const venue = [p.venue, p.year].filter(Boolean).join(", ");
  const authors = p.authors || "";
  const note = p.url ? "" : (p.venue_url ? " (link to venue homepage)" : " (link TBD)");
  const badges = (p.badges||[]).map(b => `<span class="badge">${b}</span>`).join(" ");
  const titleHTML = url ? `<a href="${url}" target="_blank" rel="noopener">${title}</a>${note}` : `${title}${note}`;
  return `
    <div class="paper">
      <h3>${titleHTML}</h3>
      <div class="meta">${authors}</div>
      <div class="meta">${venue}</div>
      <div>${badges}</div>
    </div>
  `;
}

function newsItemHTML(n){
  const when = fmtDate(n.date);
  const link = n.link ? `<a href="${n.link}" target="_blank" rel="noopener">${n.link_text || "Link"}</a>` : "";
  const tag = n.tag ? `<span class="tag">${n.tag}</span>` : "";
  return `<li>
    <div class="small">${when} ${tag}</div>
    <div>${n.text} ${link}</div>
  </li>`;
}

(async function init(){
  const intro = await loadJSON("data/intro.json");
  const papers = await loadJSON("data/papers.json");
  const news = await loadJSON("data/news.json");

  // Intro
  document.getElementById("intro-text").innerHTML = intro.html;

  // News (sorted newest first)
  news.sort((a,b)=> new Date(b.date) - new Date(a.date));
  document.getElementById("news-list").innerHTML = news.map(newsItemHTML).join("");

  // Papers
  const container = document.getElementById("papers-list");
  container.innerHTML = papers.map(paperHTML).join("");

  // Footer year
  document.getElementById("year").textContent = new Date().getFullYear();
})();
