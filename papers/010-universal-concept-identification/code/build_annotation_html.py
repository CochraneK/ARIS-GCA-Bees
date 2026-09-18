"""Build standalone, no-backend HTML calibration forms.

Each generated HTML embeds exactly one participant form and downloads a JSON
response file locally at completion. No network request or external library is
used by the generated page.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
FORMS=ROOT/"data"/"human_forms"/"forms.generated.json"
OUT=ROOT/"data"/"human_forms"/"html"


TEMPLATE="""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UCID calibration · __FORM_ID__</title>
<style>
:root{font-family:Inter,system-ui,sans-serif;color:#171717;background:#f6f5f2}
*{box-sizing:border-box}body{margin:0}.wrap{max-width:780px;margin:0 auto;padding:32px 20px 80px}
.card{background:#fff;border:1px solid #e5e3df;border-radius:22px;padding:28px;box-shadow:0 8px 28px #0000000a}
.muted{color:#73706a}.progress{height:8px;background:#ece9e3;border-radius:99px;overflow:hidden;margin:18px 0}
.bar{height:100%;background:#202020;width:0}.context{background:#f5f3ef;border-radius:14px;padding:14px;margin:14px 0;white-space:pre-wrap}
.query{font-size:1.25rem;line-height:1.45;margin:22px 0}.responses{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
button{border:1px solid #d8d4cc;border-radius:12px;background:#fff;padding:13px;font:inherit;cursor:pointer}
button:hover{background:#f4f2ed}.selected{outline:2px solid #171717}.next{width:100%;background:#171717;color:#fff;margin-top:18px}
input[type=text]{width:100%;padding:12px;border:1px solid #d8d4cc;border-radius:10px;font:inherit}
input[type=range]{width:100%}.hidden{display:none}code{font-size:.86em}
@media(max-width:560px){.responses{grid-template-columns:1fr}}
</style>
</head>
<body><div class="wrap">
<div class="card" id="start">
<h1>Semantic judgment calibration</h1>
<p class="muted">Form <strong>__FORM_ID__</strong> · Protocol <strong>__PROTOCOL__</strong></p>
<p>You will see a target meaning or scenario, followed by one question. Judge the question under the supplied definition and context. Some items may recur.</p>
<div id="protocolHelp"></div>
<label>Pseudonymous participant ID<br><input id="pid" type="text" autocomplete="off" placeholder="e.g. P001"></label>
<button class="next" onclick="begin()">Begin</button>
<p class="muted">This page stores responses only in your browser memory and downloads a JSON file at the end. It does not send responses anywhere.</p>
</div>
<div class="card hidden" id="trial">
<div class="muted"><span id="counter"></span></div>
<div class="progress"><div class="bar" id="bar"></div></div>
<h2 id="target"></h2>
<p id="definition"></p>
<div class="context hidden" id="context"></div>
<div class="query" id="query"></div>
<div class="responses" id="responses"></div>
<p>Confidence: <strong id="confLabel">50</strong>/100</p>
<input id="confidence" type="range" min="0" max="100" value="50" oninput="confLabel.textContent=this.value">
<button class="next" id="next" onclick="submitTrial()" disabled>Next</button>
</div>
<div class="card hidden" id="done">
<h1>Complete</h1>
<p>Your response file will download automatically. Keep it until it has been submitted through the study's approved collection channel.</p>
<button class="next" onclick="download()">Download again</button>
</div>
</div>
<script>
const FORM=__FORM_JSON__;
let index=0, selected=null, startedAt=0, participant="", rows=[];
const protocolHelp={
 P2:"<p><b>YES</b> = applies/true. <b>NO</b> = meaningful and applicable, but false. This condition intentionally forces binary judgment.</p>",
 P6:"<p><b>YES</b> = applies/true; <b>NO</b> = applicable but false; <b>BORDERLINE</b> = genuinely graded; <b>UNKNOWN</b> = determinate in principle but not knowable from allowed information; <b>UNDEFINED</b> = not properly truth-evaluable as posed; <b>BOTH</b> = positive and negative support coexist under the supplied non-explosive representation.</p>"
};
document.getElementById("protocolHelp").innerHTML=protocolHelp[FORM.protocol];

function begin(){
 participant=document.getElementById("pid").value.trim();
 if(!participant){alert("Enter a pseudonymous participant ID.");return}
 document.getElementById("start").classList.add("hidden");
 document.getElementById("trial").classList.remove("hidden");
 render();
}
function displayTarget(item){
 return item.lemma || item.target || item.target_id || "Target";
}
function render(){
 const item=FORM.items[index]; selected=null;
 document.getElementById("next").disabled=true;
 document.getElementById("counter").textContent=(index+1)+" / "+FORM.items.length;
 document.getElementById("bar").style.width=((index/FORM.items.length)*100)+"%";
 document.getElementById("target").textContent=displayTarget(item);
 document.getElementById("definition").textContent=item.definition || "";
 const ctx=document.getElementById("context");
 if(item.frozen_context && Object.keys(item.frozen_context).length){
   ctx.classList.remove("hidden");
   ctx.textContent="Context\n"+JSON.stringify(item.frozen_context,null,2);
 }else{ctx.classList.add("hidden");ctx.textContent=""}
 document.getElementById("query").textContent=item.query_text;
 const box=document.getElementById("responses"); box.innerHTML="";
 item.allowed_responses.forEach(resp=>{
   const b=document.createElement("button"); b.textContent=resp;
   b.onclick=()=>{selected=resp;[...box.children].forEach(x=>x.classList.remove("selected"));b.classList.add("selected");document.getElementById("next").disabled=false};
   box.appendChild(b);
 });
 document.getElementById("confidence").value=50;
 document.getElementById("confLabel").textContent="50";
 startedAt=performance.now();
}
function submitTrial(){
 if(!selected)return;
 const item=FORM.items[index];
 rows.push({
   participant_id:participant,
   form_id:FORM.form_id,
   protocol:FORM.protocol,
   trial_number:index+1,
   pair_id:item.pair_id,
   source:item.source,
   target_id:item.target_id,
   query_id:item.query_id,
   response:selected,
   confidence:Number(document.getElementById("confidence").value)/100,
   response_time_ms:Math.round(performance.now()-startedAt),
   occurrence_index:rows.filter(r=>r.pair_id===item.pair_id).length+1
 });
 index++;
 if(index>=FORM.items.length){
   document.getElementById("trial").classList.add("hidden");
   document.getElementById("done").classList.remove("hidden");
   download();
 }else render();
}
function download(){
 const payload={study:"ARIS4C010-UCID-calibration",form_id:FORM.form_id,protocol:FORM.protocol,participant_id:participant,completed_at:new Date().toISOString(),rows};
 const blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"});
 const a=document.createElement("a"); a.href=URL.createObjectURL(blob);
 a.download=FORM.form_id+"_"+participant+"_responses.json"; a.click(); URL.revokeObjectURL(a.href);
}
</script>
</body></html>"""


def sanitize_form(form):
    # Strip fields that reveal retest status or research-design provenance from
    # participant-visible embedded data. Repetition can be recovered by pair_id.
    clean={k:v for k,v in form.items() if k!="items"}
    clean["items"]=[]
    for item in form["items"]:
        clean["items"].append({
            "source":item["source"],
            "pair_id":item["pair_id"],
            "target_id":item["target_id"],
            "lemma":item.get("lemma"),
            "target":item.get("target"),
            "definition":item.get("definition"),
            "frozen_context":item.get("frozen_context"),
            "query_id":item["query_id"],
            "query_text":item["query_text"],
            "allowed_responses":item["allowed_responses"],
        })
    return clean


def main():
    payload=json.loads(FORMS.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[]
    for form in payload["forms"]:
        clean=sanitize_form(form)
        page=(TEMPLATE
              .replace("__FORM_ID__",html.escape(form["form_id"]))
              .replace("__PROTOCOL__",html.escape(form["protocol"]))
              .replace("__FORM_JSON__",json.dumps(clean,ensure_ascii=False).replace("</","<\\/")))
        path=OUT/f"{form['form_id']}.html"
        path.write_text(page,encoding="utf-8")
        rows.append(f'<li><a href="{path.name}">{html.escape(form["form_id"])}</a></li>')

    index="<!doctype html><meta charset=utf-8><title>UCID calibration forms</title><h1>UCID calibration forms</h1><p>Research administration index. Assign exactly one form per participant.</p><ul>"+"".join(rows)+"</ul>"
    (OUT/"index.html").write_text(index,encoding="utf-8")
    print("PASS standalone HTML form build")
    print("forms:",len(payload["forms"]))
    print("html files:",len(list(OUT.glob("*.html"))))


if __name__=="__main__":
    main()
