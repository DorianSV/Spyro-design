"""Builds tracker.html from data/jobs.json and data/runs.json. Run: python3 scripts/render.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
jobs = json.loads((ROOT / "data" / "jobs.json").read_text(encoding="utf-8")).get("jobs", [])
runs_path = ROOT / "data" / "runs.json"
runs = json.loads(runs_path.read_text(encoding="utf-8")).get("runs", []) if runs_path.exists() else []
payload = json.dumps({"jobs": jobs, "run": runs[-1] if runs else None}, ensure_ascii=False).replace("</", "<\\/")

HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Job Radar</title>
<style>
:root{--bg:#f5f6f9;--card:#fff;--fg:#1b2230;--muted:#5c6577;--line:#dfe3ec;--acc:#2f56c8;--good:#1f7a4d;--goodbg:#e2f3ea;--warn:#9a5b00;--warnbg:#fbefd9;--bad:#a23a3a;--badbg:#f8e3e3}
@media (prefers-color-scheme:dark){:root{--bg:#12151c;--card:#1a1f29;--fg:#e7eaf1;--muted:#9aa3b5;--line:#2c3341;--acc:#8aa6ff;--good:#6fd39f;--goodbg:#18342a;--warn:#f0b65a;--warnbg:#3a2d16;--bad:#f08a8a;--badbg:#3a1f22}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:820px;margin:0 auto;padding:24px 16px 48px;display:grid;gap:16px}
h1{margin:0;font-size:1.8rem}.sub{color:var(--muted);margin:2px 0 0}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
button,select,input{font:inherit;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:999px;padding:6px 12px}
button[aria-pressed=true]{background:var(--acc);border-color:var(--acc);color:#fff}input{border-radius:8px;flex:1;min-width:160px}
.run{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;color:var(--muted);font-size:.9rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:grid;gap:8px}
.top{display:flex;gap:12px;align-items:flex-start}.score{min-width:48px;height:48px;border-radius:10px;display:grid;place-items:center;font-weight:700;background:var(--goodbg);color:var(--good)}
.score.mid{background:#e6ecfb;color:var(--acc)}.score.low{background:var(--line);color:var(--muted)}
.title{margin:0;font-size:1.05rem}.title a{color:inherit}.co{color:var(--muted);font-size:.9rem}
.tags{display:flex;flex-wrap:wrap;gap:6px}.tag{font-size:.78rem;padding:2px 8px;border-radius:6px;border:1px solid var(--line);color:var(--muted)}
.tag.ok{background:var(--goodbg);color:var(--good);border-color:transparent}.tag.warn{background:var(--warnbg);color:var(--warn);border-color:transparent}.tag.bad{background:var(--badbg);color:var(--bad);border-color:transparent}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:600px){.cols{grid-template-columns:1fr}}
.cols h3{margin:0;font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}ul{margin:4px 0 0;padding-left:18px;font-size:.9rem}
details{font-size:.9rem}summary{cursor:pointer;color:var(--acc)}.foot{font-size:.82rem;color:var(--muted)}.empty{text-align:center;color:var(--muted);padding:30px}
</style></head><body><div class="wrap">
<header><h1>Job Radar</h1><p class="sub">Salesforce / CRM roles that fit at 70%+. To change a status, tell Claude: "mark &lt;id&gt; as Applied".</p></header>
<div class="run" id="run"></div>
<div class="bar" id="filters"></div>
<div class="bar"><input id="q" placeholder="Search company or title"><select id="sort"><option value="score">Highest score</option><option value="added">Newest first</option><option value="expires">Closing soonest</option></select></div>
<div id="list"></div></div>
<script>
const D=__DATA__;const F=[["open","Open"],["New","New"],["Interested","Interested"],["Applied","Applied"],["Interview","Interview"],["unverified","Unverified"],["closed","Closed"],["all","All"]];
let f="open";const $=i=>document.getElementById(i);const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const li=a=>(a||[]).map(x=>"<li>"+esc(x)+"</li>").join("");
if(D.run){const r=D.run;$("run").textContent=`Last run ${r.date||"?"} · checked ${r.checked??"?"} · added ${r.kept??"?"} · rechecked ${r.rechecked??"?"} · closed ${r.closed??"?"} · unverified ${r.unverified??"?"}`}else $("run").hidden=true;
$("filters").innerHTML=F.map(([k,l])=>`<button data-f="${k}">${l}</button>`).join("");
$("filters").onclick=e=>{const b=e.target.closest("button");if(b){f=b.dataset.f;draw()}};$("q").oninput=draw;$("sort").onchange=draw;
function keep(j){const s=j.status||"New",l=j.live||"unverified";if(f==="all")return true;if(f==="open")return l!=="closed"&&s!=="Rejected";if(f==="unverified"||f==="closed")return l===f;return s===f}
function draw(){document.querySelectorAll("#filters button").forEach(b=>b.setAttribute("aria-pressed",b.dataset.f===f));
const q=$("q").value.toLowerCase(),so=$("sort").value;
let v=D.jobs.filter(keep).filter(j=>!q||(j.company+" "+j.title).toLowerCase().includes(q));
v.sort((a,b)=>so==="added"?String(b.added).localeCompare(String(a.added)):so==="expires"?String(a.expires||"9999").localeCompare(String(b.expires||"9999")):b.score-a.score);
$("list").innerHTML=v.length?v.map(j=>{const l=j.live||"unverified";const lt=l==="verified"?`<span class="tag ok" title="${esc(j.liveEvidence)}">Verified ${esc(j.lastChecked||"")}</span>`:l==="closed"?`<span class="tag bad" title="${esc(j.liveEvidence)}">Closed ${esc(j.closedOn||"")}</span>`:`<span class="tag warn" title="${esc(j.liveEvidence)}">Unverified</span>`;
return `<article class="card"><div class="top"><div class="score ${j.score>=85?"":j.score>=70?"mid":"low"}">${j.score}</div><div><h2 class="title"><a href="${esc(j.url)}" target="_blank" rel="noopener">${esc(j.title)}</a></h2><div class="co">${esc(j.company)}${j.salary?" · "+esc(j.salary):""}</div></div></div>
<div class="tags">${lt}<span class="tag">${esc(j.status||"New")}</span>${[j.tier,j.mode,j.contract,j.language].filter(Boolean).map(x=>`<span class="tag">${esc(x)}</span>`).join("")}${j.expires?`<span class="tag warn">until ${esc(j.expires)}</span>`:""}${(j.flags||[]).map(x=>`<span class="tag warn">${esc(x)}</span>`).join("")}</div>
<div class="cols"><div><h3>Why it fits</h3><ul>${li(j.why)}</ul></div><div><h3>Gaps</h3><ul>${li(j.gaps)}</ul></div></div>
${(j.bullets||[]).length?`<details><summary>Tailored CV bullets</summary><ol>${li(j.bullets)}</ol></details>`:""}
<div class="foot">id: ${esc(j.id)} · added ${esc(j.added||"")} via ${esc(j.source||"")}</div></article>`}).join(""):`<div class="empty">Nothing in this view.</div>`}
draw();
</script></body></html>"""

(ROOT / "tracker.html").write_text(HTML.replace("__DATA__", payload), encoding="utf-8")
print(f"tracker.html written ({len(jobs)} jobs).")
