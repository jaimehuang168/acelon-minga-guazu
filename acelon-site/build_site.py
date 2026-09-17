# -*- coding: utf-8 -*-
"""Static site generator for the ACELON Minga Guazú project site (GitHub Pages)."""
import json, re, html, os
ROOT = os.path.dirname(os.path.abspath(__file__))
def esc(s): return html.escape(str(s), quote=False)

CSS = """
:root{--paper:#F3F1EB;--panel:#FAF9F5;--line:#D6D2C8;--ink:#1C232B;--ink2:#5B6068;--mute:#8A8F96;--accent:#C8401C;--cyan:#1D7F9C;--chip:#ECE9E1;--tot:#D6D2C8;
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--s5:#e87ba4}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#171B1F;--panel:#1F252B;--line:#3A4149;--ink:#EAE7E0;--ink2:#B7B3AA;--mute:#7F868E;--accent:#E0623E;--cyan:#3FA6C4;--chip:#2A3037;--tot:#3A4149;--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181}}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 "IBM Plex Sans","Noto Sans TC",system-ui,sans-serif}
a{color:var(--cyan)}h1,h2,h3{font-family:"Barlow Condensed","Noto Sans TC",sans-serif;letter-spacing:.01em;text-wrap:balance;margin:0}
h1{font-size:34px;line-height:1.08;font-weight:700}h2{font-size:24px;font-weight:700;margin:0 0 10px}h3{font-size:18px;font-weight:600}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
nav.top{position:sticky;top:0;z-index:10;background:var(--panel);border-bottom:1px solid var(--line)}
nav.top .wrap{display:flex;align-items:center;gap:18px;height:54px;flex-wrap:wrap}
nav.top .brand{font:700 18px "Barlow Condensed","Noto Sans TC",sans-serif;color:var(--ink);text-decoration:none;border-left:4px solid var(--accent);padding-left:10px}
nav.top a.l{color:var(--ink2);text-decoration:none;font-weight:500;font-size:14px;padding:6px 2px;border-bottom:2px solid transparent}
nav.top a.l[aria-current]{color:var(--ink);border-bottom-color:var(--accent)}
.hero{padding:44px 0 26px}.hero p{max-width:66ch;color:var(--ink2);margin:10px 0 0}
.meta{font:500 12px/1.4 "IBM Plex Mono",monospace;color:var(--mute);display:flex;gap:16px;flex-wrap:wrap;margin-top:12px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin:24px 0}
.card{background:var(--panel);border:1px solid var(--line);padding:16px 18px;text-decoration:none;color:var(--ink);display:block}
.card:hover{border-color:var(--accent)}.card .k{font:600 11px/1 "Barlow Condensed","Noto Sans TC",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin-bottom:8px}
.card p{margin:6px 0 0;color:var(--ink2);font-size:13.5px}.card img{width:100%;aspect-ratio:16/9;object-fit:cover;border:1px solid var(--line);margin:10px 0 6px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:18px 0}
.tile{background:var(--panel);border:1px solid var(--line);padding:14px 16px}.tile .v{font:700 28px/1 "Barlow Condensed","Noto Sans TC",sans-serif;font-variant-numeric:tabular-nums}.tile .l{font-size:12px;color:var(--mute);margin-top:6px}
section{padding:26px 0;border-top:1px solid var(--line)}section:first-of-type{border-top:0}
table{border-collapse:collapse;width:100%;font-size:13.5px;background:var(--panel)}th,td{border:1px solid var(--line);padding:6px 9px;vertical-align:top;text-align:left}
th{background:var(--chip);font:600 12px/1.3 "Barlow Condensed","Noto Sans TC",sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--ink2)}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}tr.tot td{background:var(--tot);font-weight:600}tr.sec td{background:var(--chip);font-weight:600}
.tw{overflow-x:auto;margin:10px 0 16px}.small{font-size:12px;color:var(--ink2)}.mono{font-family:"IBM Plex Mono",monospace;font-size:12.5px}
details{border:1px solid var(--line);background:var(--panel);margin:10px 0}summary{cursor:pointer;padding:10px 14px;font:600 15px "Barlow Condensed","Noto Sans TC",sans-serif;font-size:17px}details>div{padding:0 14px 14px}
.tag{display:inline-block;font:500 11px/1 "IBM Plex Mono",monospace;padding:3px 7px;border:1px solid var(--line);margin:2px 4px 2px 0;white-space:nowrap}
.tag.ok{border-color:var(--s3);color:var(--s3)}.tag.open{border-color:var(--accent);color:var(--accent)}.tag.part{border-color:var(--s4);color:var(--s4)}
.btn{display:inline-block;background:var(--ink);color:var(--paper);padding:9px 14px;text-decoration:none;font:600 13px "Barlow Condensed","Noto Sans TC",sans-serif;letter-spacing:.06em;margin:4px 6px 4px 0}
.btn.o{background:transparent;color:var(--ink);border:1px solid var(--line)}
footer{border-top:1px solid var(--line);padding:24px 0 40px;color:var(--mute);font-size:12px}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}
.gal figure{margin:0;background:var(--panel);border:1px solid var(--line);cursor:zoom-in}.gal img{width:100%;aspect-ratio:1.41;object-fit:cover;display:block;background:#fff}
.gal figcaption{padding:8px 10px;font-size:12.5px}.gal figcaption b{font-family:"IBM Plex Mono",monospace;font-weight:500;color:var(--cyan);display:block;font-size:12px}
#lb{position:fixed;inset:0;background:rgba(20,24,28,.94);display:none;z-index:50;flex-direction:column}#lb.on{display:flex}
#lb .bar{display:flex;gap:10px;align-items:center;padding:10px 16px;color:#EAE7E0;font-size:13px}#lb .bar b{font-family:"IBM Plex Mono",monospace;font-weight:500}
#lb .bar button{margin-left:auto;background:transparent;color:#fff;border:1px solid #666;padding:6px 12px;cursor:pointer;font:inherit}
#lb .vp{flex:1;overflow:hidden;position:relative;cursor:grab}#lb img{position:absolute;left:0;top:0;transform-origin:0 0;user-select:none;-webkit-user-drag:none;background:#fff}
.chart{background:var(--panel);border:1px solid var(--line);padding:14px 16px;margin:12px 0}.chart svg{width:100%;height:auto;display:block}
.chart text{font:12px "IBM Plex Sans","Noto Sans TC",sans-serif;fill:var(--ink2)}.chart .v{fill:var(--ink);font-weight:600;font-variant-numeric:tabular-nums}
.leg{display:flex;gap:14px;flex-wrap:wrap;font-size:12.5px;margin:6px 0 0}.leg i{display:inline-block;width:12px;height:12px;vertical-align:-1px;margin-right:5px}
.tip{position:fixed;pointer-events:none;background:var(--ink);color:var(--paper);font-size:12px;padding:5px 8px;display:none;z-index:20}
@media (max-width:640px){h1{font-size:28px}nav.top .wrap{height:auto;padding:8px 16px}}
"""
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;700&display=swap">'
NAV = [("index.html", "首頁"), ("model.html", "3D 模型"), ("plans.html", "設計圖"), ("cost.html", "建造成本"), ("rfi.html", "RFI 與回覆")]

def page(fname, title, body, extra_head="", extra_js=""):
    CUR = ' aria-current="page"'
    nav = "".join(f'<a class="l" href="{h}"{CUR if h == fname else ""}>{t}</a>' for h, t in NAV)
    doc = f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · ACELON Minga Guazú</title>{FONTS}<style>{CSS}</style>{extra_head}</head><body>
<nav class="top"><div class="wrap"><a class="brand" href="index.html">ACELON · Minga Guazú</a>{nav}</div></nav>
<main class="wrap">{body}</main>
<footer><div class="wrap">PTITP 台巴智慧科技園區 · 資料基準：Salum &amp; Wenz IFC 2026‑07‑31、台灣方圖說 P0A30011–170、9/4 回覆、CYPE／costeo 單價、BCP 匯率 2026‑09‑15 · 本站內容為概念設計與 Class 3 估算，非正式報價。</div></footer>
{extra_js}</body></html>"""
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(doc)

# ---------------- data ----------------
COST = json.load(open(os.path.join(ROOT, "assets/cost_data.json"), encoding="utf-8"))
RFI = json.load(open(os.path.join(ROOT, "assets/rfi_raw.json"), encoding="utf-8"))
summ = COST["摘要"]
def find(rows, key, col=1):
    for r in rows:
        if len(r) > col and isinstance(r[col], str) and r[col].startswith(key): return r
    return None
def money(v):
    try: return f"{float(v):,.0f}"
    except: return esc(v)
A = find(summ, "原絲廠房 Nave N 直接成本"); B = find(summ, "假撚廠房 DTY 直接成本"); C = find(summ, "公用廠房與公用設備"); D = find(summ, "基地工程直接成本")
DIRECT = find(summ, "直接成本小計"); PRE = find(summ, "總建造成本（未稅）"); TOT = find(summ, "總建造成本（含 IVA）"); RANGE = find(summ, "估算區間")

# ---------------- index ----------------
body = f"""
<div class="hero"><h1>ACELON 巴拉圭新廠 · 設計圖、3D 概念模型與建造成本</h1>
<p>台巴智慧科技園區（PTITP，Minga Guazú, Alto Paraná）內 ACELON 原絲／假撚新廠之設計整理：Salum &amp; Wenz 執行設計的結構模型、台灣方全套圖說、各層設備配置、31 項 RFI 與 9/4 回覆，以及依巴拉圭 2026 年單價作成的總建造成本估算。</p>
<div class="meta"><span>Manzana XI · 第一次租賃範圍 158 × 106 m</span><span>更新 2026‑09‑17</span><span>中文 · ES · EN（3D 頁）</span></div></div>
<div class="tiles">
<div class="tile"><div class="v">3 棟</div><div class="l">原絲廠房 RC 4 層＋1.5F＋地下風道 · 假撚廠房鋼構 2 層 · 公用廠房 RC 2 層</div></div>
<div class="tile"><div class="v">15,340 m²</div><div class="l">總樓地板面積（9,040 + 4,700 + 1,600）</div></div>
<div class="tile"><div class="v">USD {money(PRE[2])}</div><div class="l">總建造成本（未稅，Class 3 ±15–25%）</div></div>
<div class="tile"><div class="v">USD {money(TOT[2])}</div><div class="l">含 IVA 10%</div></div>
<div class="tile"><div class="v">31 項</div><div class="l">Salum &amp; Wenz RFI · 12 項已由台灣方 9/4 回覆</div></div>
</div>
<div class="grid">
<a class="card" href="model.html"><div class="k">01 · 3D 概念模型</div><h3>互動式廠區模型</h3><img src="assets/preview_3d.jpg" alt="3D 模型預覽"><p>IFC 結構、各層設備、向量平面線條與文字、假撚廠房機台與房間、公用區設備、基地設施；逐層剖切、三語切換。</p></a>
<a class="card" href="plans.html"><div class="k">02 · 設計圖</div><h3>台灣方全套圖說 27 張＋園區管線 3 張</h3><img src="assets/plans/P0A30031_thumb.jpg" alt="平面圖預覽"><p>總平面、各層平面（含設備／無設備版）、屋頂、7 組剖面、管道間細部、圍牆基礎；可放大細看。</p></a>
<a class="card" href="cost.html"><div class="k">03 · 建造成本</div><h3>巴拉圭總建造成本估算</h3><img src="assets/preview_cost.svg" alt="成本圖"><p>由 IFC 量得工程數量，套用 CYPE／costeo 巴拉圭單價；分棟明細、假設、風險與 ACELON 概算比較；Excel 可下載。</p></a>
<a class="card" href="rfi.html"><div class="k">04 · RFI 與回覆</div><h3>31 項技術諮詢對照表</h3><img src="assets/plans/P0A30011_thumb.jpg" alt="RFI"><p>Salum &amp; Wenz 提問（ES／EN／中文）、台灣方 9/4 回覆、狀態與對造價的影響。</p></a>
</div>
<section><h2>下載</h2><p><a class="btn" href="assets/files/ACELON_巴拉圭建造成本估算_2026-09.xlsx">成本估算 Excel</a><a class="btn o" href="assets/files/acelon_site_concept.glb">3D 模型 GLB</a><a class="btn o" href="assets/files/acelon_site_concept.obj">3D 模型 OBJ</a><a class="btn o" href="assets/files/acelon_floorplans.js">平面向量資料 JS</a></p>
<p class="small">GLB／OBJ 座標：公尺，X 向東、Z 向南，原點為第一次租賃範圍西北角；可直接匯入 Revit、Blender。</p></section>
"""
page("index.html", "首頁", body)

# ---------------- plans ----------------
SHEETS = [
 ("總平面", [("P0A30011", "一期巴拉圭廠房（總平面配置）"), ("P0A30011A", "一期巴拉圭廠房（套入舊廠房）")]),
 ("原絲廠房平面", [("P0A30021", "地下風道平面圖"), ("P0A30031", "一樓平面配置圖"), ("P0A30031A", "一樓平面配置圖（無設備）"), ("P0A30041", "一樓半平面配置圖"), ("P0A30041A", "一樓半平面配置圖（無設備）"), ("P0A30051", "二樓平面配置圖"), ("P0A30051A", "二樓平面配置圖（無設備）"), ("P0A30061", "三樓平面配置圖"), ("P0A30061A", "三樓平面配置圖（無設備）"), ("P0A30071", "四樓平面配置圖"), ("P0A30071A", "四樓平面配置圖（無設備）"), ("P0A30081", "屋頂平面配置圖")]),
 ("剖面", [("P0A30091", "斷面圖"), ("P0A30091A", "斷面圖（無設備）"), ("P0A30101", "A‑A 剖視圖"), ("P0A30111", "B‑B 剖視圖"), ("P0A30121", "C‑C 剖視圖"), ("P0A30131", "D‑D 剖視圖"), ("P0A30141", "E‑E 剖視圖"), ("P0A30141A", "E‑E 剖視圖（無設備）"), ("P0A30141B", "E‑E 剖視圖（無設備有風管）"), ("P0A30151", "F‑F 剖視圖")]),
 ("細部與基礎", [("P0A30160", "「G」detail 管道間管路及線槽配置（管材由業主自行處理）"), ("P0A30170", "廠房四周柱基礎、牆壁及底樑參考圖")]),
 ("園區管線系統（PTITP 提供）", [("園區供水系統", "園區供水系統"), ("園區汙水系統", "園區汙水系統"), ("園區雨水排放系統", "園區雨水排放系統")]),
]
gal = ""
for grp, items in SHEETS:
    gal += f'<section><h2>{esc(grp)}</h2><div class="gal">'
    for code, name in items:
        if not os.path.exists(os.path.join(ROOT, f"assets/plans/{code}.jpg")): continue
        gal += f'<figure data-src="assets/plans/{code}.jpg" data-t="{esc(code)} · {esc(name)}"><img loading="lazy" src="assets/plans/{code}_thumb.jpg" alt="{esc(name)}"><figcaption><b>{esc(code)}</b>{esc(name)}</figcaption></figure>'
    gal += "</div></section>"
body = f"""<div class="hero"><h1>設計圖</h1><p>台灣方（聚隆纖維）提供之原絲廠房圖說 P0A30011–P0A30170（2026‑09‑03 版）與 PTITP 園區管線系統圖。點圖放大，滾輪縮放、拖曳平移；圖面座標系與 3D 模型一致（軸線 A–D 7.5 m、1–9 列 72.5 m）。</p>
<div class="meta"><span>圖號說明 20260903</span><span>A3 · 1:100 / 1:500</span></div></div>{gal}
<div id="lb"><div class="bar"><b id="lbt"></b><span class="small" style="color:#B7B3AA">滾輪縮放 · 拖曳平移 · Esc 關閉</span><button id="lbc">關閉 ×</button></div><div class="vp" id="vp"><img id="lbi" alt=""></div></div>"""
js = """<script>
const lb=document.getElementById('lb'),img=document.getElementById('lbi'),vp=document.getElementById('vp'),lbt=document.getElementById('lbt');let s=1,x=0,y=0,drag=null;
function apply(){img.style.transform=`translate(${x}px,${y}px) scale(${s})`}
document.querySelectorAll('.gal figure').forEach(f=>f.onclick=()=>{img.src=f.dataset.src;lbt.textContent=f.dataset.t;lb.classList.add('on');img.onload=()=>{const r=vp.getBoundingClientRect();s=Math.min(r.width/img.naturalWidth,r.height/img.naturalHeight);x=(r.width-img.naturalWidth*s)/2;y=(r.height-img.naturalHeight*s)/2;apply()}});
document.getElementById('lbc').onclick=()=>lb.classList.remove('on');document.addEventListener('keydown',e=>{if(e.key==='Escape')lb.classList.remove('on')});
vp.addEventListener('wheel',e=>{e.preventDefault();const r=vp.getBoundingClientRect();const mx=e.clientX-r.left,my=e.clientY-r.top;const k=e.deltaY<0?1.15:1/1.15;x=mx-(mx-x)*k;y=my-(my-y)*k;s*=k;apply()},{passive:false});
vp.addEventListener('pointerdown',e=>{drag=[e.clientX-x,e.clientY-y];vp.setPointerCapture(e.pointerId)});vp.addEventListener('pointermove',e=>{if(drag){x=e.clientX-drag[0];y=e.clientY-drag[1];apply()}});vp.addEventListener('pointerup',()=>drag=null);
</script>"""
page("plans.html", "設計圖", body, extra_js=js)

# ---------------- cost ----------------
def table(rows, cols, numcols, klass_fn=None, hdrs=None):
    h = "<div class='tw'><table>"
    if hdrs: h += "<tr>" + "".join(f"<th{' class=n' if i in numcols else ''}>{esc(x)}</th>" for i, x in enumerate(hdrs)) + "</tr>"
    for r in rows:
        k = klass_fn(r) if klass_fn else ""
        h += f"<tr class='{k}'>" + "".join(f"<td{' class=n' if i in numcols else ''}>{money(r[c]) if (i in numcols and isinstance(r[c],(int,float))) else esc(r[c])}</td>" for i, c in enumerate(cols)) + "</tr>"
    return h + "</table></div>"

# summary rows
ia = [i for i, r in enumerate(summ) if r[0] == "A"][0]
srows = [r for r in summ[ia:] if r[1] and not str(r[1]).startswith(("與 ACELON", "註：", "圖例", "項目"))]
srows_main = [r for r in srows if r[2] != "" or str(r[1]).startswith("估算區間")]
def kls(r):
    t = str(r[1]);
    return "tot" if t.startswith(("直接成本小計", "工程費用", "總建造成本")) else ""
main_rows = []
for r in srows_main:
    if str(r[1]).startswith("估算區間"): break
    main_rows.append(r)
sum_tbl = table(main_rows, [0, 1, 2, 3, 4, 5], {2, 3, 4}, kls, ["項次", "項目", "金額 (USD)", "USD/m²", "金額 (₲ 百萬)", "說明"])
# comparison
ci = [i for i, r in enumerate(summ) if str(r[1]).startswith("與 ACELON")][0]
cmp_rows = [r for r in summ[ci + 2:ci + 6]]
cmp_tbl = "<div class='tw'><table><tr><th>項目</th><th class=n>ACELON 概算 (NT$)</th><th class=n>換算 USD（32 NT$/USD）</th><th class=n>本估算 USD（含管理費，未稅）</th><th class=n>差異</th></tr>"
for r in cmp_rows:
    pct = f"{float(r[5])*100:+.0f}%" if isinstance(r[5], (int, float)) else ""
    cmp_tbl += f"<tr class='{'tot' if r[1]=='合計' else ''}'><td>{esc(r[1])}</td><td class=n>{money(r[2])}</td><td class=n>{money(r[3])}</td><td class=n>{money(r[4])}</td><td class=n>{pct}</td></tr>"
cmp_tbl += "</table></div>"

# chart 1: by building (single series) ; chart 2: stacked by section per building
bld = [("原絲廠房", float(A[2])), ("假撚廠房", float(B[2])), ("公用廠房＋公用設備", float(C[2])), ("基地工程", float(D[2]))]
def sections_of(name):
    out = []
    for r in COST[name]:
        if isinstance(r[1], str) and r[1].startswith("小計"): out.append((r[1].split(". ", 1)[1] if ". " in r[1] else r[1][3:], float(r[5])))
    return out
W = 900; LH = 34; PAD = 190
mx = max(v for _, v in bld); scale = (W - PAD - 110) / mx
svg1 = f'<svg viewBox="0 0 {W} {LH*len(bld)+30}" role="img" aria-label="各棟直接成本">'
for i, (n, v) in enumerate(bld):
    y = 10 + i * LH; w = v * scale
    svg1 += f'<text x="{PAD-10}" y="{y+17}" text-anchor="end">{esc(n)}</text><rect x="{PAD}" y="{y}" width="{w:.1f}" height="22" rx="0" fill="var(--s1)"/><rect x="{PAD+w-4:.1f}" y="{y}" width="4" height="22" rx="2" fill="var(--s1)"/><text class="v" x="{PAD+w+8:.1f}" y="{y+16}">USD {v:,.0f}</text>'
svg1 += "</svg>"
# stacked
cats = ["土方與基礎", "結構", "外殼與地坪", "內部裝修", "垂直運輸", "建築機電", "公用設備", "基地"]
colors = ["var(--s1)", "var(--s2)", "var(--s3)", "var(--s4)", "var(--s5)", "#4a3aa7", "#008300", "#8A8F96"]
def cat_of(t):
    if "土方" in t: return 0
    if "結構" in t: return 1
    if "外殼" in t: return 2
    if "裝修" in t: return 3
    if "垂直" in t: return 4
    if "機電" in t: return 5
    if "公用設備" in t: return 6
    return 7
stack = []
for nm, sheet in [("原絲廠房", "原絲廠房"), ("假撚廠房", "假撚廠房"), ("公用廠房", "公用廠房"), ("基地工程", "基地工程")]:
    segs = [0.0] * 8
    for t, v in sections_of(sheet): segs[cat_of(t)] += v
    stack.append((nm, segs))
mx2 = max(sum(s) for _, s in stack); sc2 = (W - PAD - 110) / mx2
svg2 = f'<svg viewBox="0 0 {W} {LH*len(stack)+30}" role="img" aria-label="各棟成本組成">'
for i, (n, segs) in enumerate(stack):
    y = 10 + i * LH; x = PAD
    svg2 += f'<text x="{PAD-10}" y="{y+17}" text-anchor="end">{esc(n)}</text>'
    for j, v in enumerate(segs):
        if v <= 0: continue
        w = v * sc2
        svg2 += f'<rect x="{x:.1f}" y="{y}" width="{max(w-2,1):.1f}" height="22" fill="{colors[j]}"><title>{esc(n)} · {esc(cats[j])}：USD {v:,.0f}</title></rect>'; x += w
    svg2 += f'<text class="v" x="{x+8:.1f}" y="{y+16}">USD {sum(segs):,.0f}</text>'
svg2 += "</svg>"
leg = "<div class='leg'>" + "".join(f"<span><i style='background:{colors[j]}'></i>{esc(c)}</span>" for j, c in enumerate(cats)) + "</div>"
# preview svg for index card
open(os.path.join(ROOT, "assets/preview_cost.svg"), "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {LH*len(bld)+30}" style="background:#FAF9F5;font:12px sans-serif">' + svg1.split(">", 1)[1].replace("var(--s1)", "#2a78d6").replace('class="v"', 'font-weight="600" fill="#1C232B"').replace("<text ", "<text fill=\"#5B6068\" "))

# assumptions table
arows = [r for r in COST["假設與單價"][4:] if r[0] and r[0] not in ("代號",)]
ass_tbl = "<div class='tw'><table><tr><th>代號</th><th>項目</th><th class=n>數值</th><th>單位</th><th>來源 / 說明</th></tr>"
for r in arows:
    v = r[2]
    if r[3] == "%": vs = f"{float(v)*100:.1f}%"
    elif isinstance(v, (int, float)): vs = f"{v:,.2f}" if float(v) < 100 else f"{v:,.0f}"
    else: vs = esc(v)
    ass_tbl += f"<tr><td class=mono>{esc(r[0])}</td><td>{esc(r[1])}</td><td class=n>{vs}</td><td>{esc(r[3])}</td><td class=small>{esc(r[4])}</td></tr>"
ass_tbl += "</table></div>"

def boq_html(sheet):
    rows = COST[sheet][4:]
    h = "<div class='tw'><table><tr><th>項次</th><th>工程項目</th><th class=n>數量</th><th>單位</th><th class=n>單價 (USD)</th><th class=n>金額 (USD)</th><th>依據 / 說明</th></tr>"
    for r in rows:
        if r[1] == "" and r[0] == "": continue
        t = str(r[1])
        if t.startswith("小計") or t.startswith("直接成本合計"): k = "tot"
        elif isinstance(r[0], (int, float)) and r[2] == "": k = "sec"
        else: k = ""
        q = f"{float(r[2]):,.1f}" if isinstance(r[2], (int, float)) else esc(r[2])
        u = f"{float(r[4]):,.2f}" if isinstance(r[4], (int, float)) else esc(r[4])
        m = money(r[5]) if isinstance(r[5], (int, float)) else esc(r[5])
        h += f"<tr class='{k}'><td class=mono>{esc(r[0])}</td><td>{esc(r[1])}</td><td class=n>{q}</td><td>{esc(r[3])}</td><td class=n>{u}</td><td class=n>{m}</td><td class=small>{esc(r[6]) if len(r)>6 else ''}</td></tr>"
    return h + "</table></div>"

qto = COST["數量計算-原絲廠房"]
qto_tbl = "<div class='tw'><table><tr><th>樓層</th><th>構件</th><th class=n>IFC 數量</th><th class=n>混凝土 m³</th><th class=n>表面積 m²</th><th class=n>含鋼率 kg/m³</th><th class=n>鋼筋 kg</th><th class=n>模板 m²</th><th>說明</th></tr>"
for r in qto[4:]:
    if r[0] == "補充數量（IFC 未含，依圖說與 9/4 回覆）": break
    if r[0] in ("樓層", ""): continue
    def f(v, d=0): return f"{float(v):,.{d}f}" if isinstance(v, (int, float)) else esc(v)
    qto_tbl += f"<tr class='{'tot' if r[0]=='IFC 結構合計' else ''}'><td>{esc(r[0])}</td><td>{esc(r[1])}</td><td class=n>{f(r[2])}</td><td class=n>{f(r[3],1)}</td><td class=n>{f(r[4])}</td><td class=n>{f(r[5])}</td><td class=n>{f(r[6])}</td><td class=n>{f(r[8])}</td><td class=small>{esc(r[9])}</td></tr>"
qto_tbl += "</table></div>"
risk = COST["風險與待確認"][4:]
risk_tbl = "<div class='tw'><table><tr><th>RFI</th><th>事項</th><th>目前估算假設</th><th class=n>可能影響 (USD)</th><th>說明</th></tr>" + "".join(f"<tr><td class=mono>{esc(r[0])}</td><td>{esc(r[1])}</td><td class=small>{esc(r[2])}</td><td class=n>{esc(r[3])}</td><td class=small>{esc(r[4])}</td></tr>" for r in risk if r[0] != "RFI") + "</table></div>"
src = COST["資料來源"][2:]
def srcli(r):
    link = f' — <a href="{esc(r[1])}">連結</a>' if str(r[1]).startswith("http") else ""
    return f"<li>{esc(r[0])}{link}</li>"
src_html = "<ul class=small>" + "".join(srcli(r) for r in src if r[0]) + "</ul>"

body = f"""<div class="hero"><h1>巴拉圭總建造成本估算</h1><p>AACE Class 3（±15–25%）。範圍：三棟廠房土建、外殼、裝修、建築機電（五大管線）、公用設備土建整合、基地工程；不含製程設備、製程管線與製程空調、土地租金。原絲廠房數量直接由 Salum &amp; Wenz IFC 實體量得，單價取自 CYPE 巴拉圭價格產生器（2024 基準 +10%）與 costeo.com.py 現價。</p>
<div class="meta"><span>估算日 2026‑09‑16</span><span>匯率 ₲5,934.88/USD（BCP 2026‑09‑15）</span><span>GFA 15,340 m²</span></div>
<p><a class="btn" href="assets/files/ACELON_巴拉圭建造成本估算_2026-09.xlsx">下載 Excel（458 個公式，改假設即重算）</a></p></div>
<div class="tiles">
<div class="tile"><div class="v">USD {money(DIRECT[2])}</div><div class="l">直接成本小計 · USD {money(DIRECT[3])}/m²</div></div>
<div class="tile"><div class="v">USD {money(PRE[2])}</div><div class="l">總建造成本（未稅）· USD {money(PRE[3])}/m²</div></div>
<div class="tile"><div class="v">USD {money(TOT[2])}</div><div class="l">含 IVA 10% · ₲ {money(TOT[4])} 百萬</div></div>
<div class="tile"><div class="v">{money(RANGE[2])} – {money(RANGE[4])}</div><div class="l">估算區間 USD（未稅，−15% / +25%）</div></div>
</div>
<section><h2>摘要</h2>{sum_tbl}</section>
<section><h2>各棟直接成本</h2><div class="chart">{svg1}</div><div class="chart">{svg2}{leg}</div></section>
<section><h2>與 ACELON 概算比較</h2>{cmp_tbl}<p class="small">ACELON 概算（WhatsApp 2026‑09‑10）未含基地工程、公用設備、預備費與稅，幣別依單價量級判定為新台幣。原絲廠房差異來自台灣 RC 廠房單價 NT$31,600/m²（≈ USD 990/m²）與巴拉圭同規格約 USD 545/m² 之落差；把基地工程、預備費與 IVA 一併計入後，總額 USD {money(TOT[2])} 與 ACELON 之 14.3M 相近。</p></section>
<section><h2>假設與單價</h2>{ass_tbl}</section>
<section><h2>原絲廠房工程數量（IFC 量算）</h2>{qto_tbl}</section>
<section><h2>分棟明細</h2>
<details open><summary>原絲廠房 Nave N — USD {money(A[2])}</summary><div>{boq_html('原絲廠房')}</div></details>
<details><summary>假撚廠房 DTY — USD {money(B[2])}</summary><div>{boq_html('假撚廠房')}</div></details>
<details><summary>公用廠房與公用設備 — USD {money(C[2])}</summary><div>{boq_html('公用廠房')}</div></details>
<details><summary>基地工程 — USD {money(D[2])}</summary><div>{boq_html('基地工程')}</div></details></section>
<section><h2>影響造價之未決事項</h2>{risk_tbl}</section>
<section><h2>資料來源</h2>{src_html}<p class="small">本估算供招商談判與預算檢核使用，非巴拉圭合格估價師或稅務顧問之正式意見；正式投標價應由當地總包商依執行設計報價。</p></section>
"""
page("cost.html", "建造成本", body)

# ---------------- RFI ----------------
ANS = {
 7: ("ok", "此為 RC 基礎示意。", "Es una representación de la fundación de H°A°."),
 8: ("ok", "材質為 RC 製造；兩道風道需連通（詳 P0A30021）。", "Ductos en hormigón armado; los dos ductos deben conectarse (P0A30021)."),
 9: ("ok", "現場所有隔間（含樓梯）採砌磚，需粉刷及油漆（1–4 樓）。", "Todas las divisiones (incl. escaleras) en mampostería, revocada y pintada (1–4F)."),
 10: ("ok", "主要為標示該區域用途，已移除。", "Solo señalaba el uso del área; se eliminó."),
 11: ("ok", "(1) 樓梯圍護採砌磚（粉刷及油漆）(2) 各樓層廁所位於一樓、一樓半、二樓、三樓樓梯平台處，合計 8 處（P0A30031/41/51/61/121）。", "(1) Cerramiento de escalera en mampostería revocada y pintada. (2) Sanitarios en los descansos de 1F, 1.5F, 2F y 3F — 8 en total."),
 12: ("ok", "主要為標示該區域用途，已移除。", "Solo señalaba el uso del área; se eliminó."),
 13: ("ok", "主要為標示該區域，放孔無樓板。", "Señala la zona; son aberturas sin losa."),
 14: ("part", "9/4 回覆未針對此項說明（僅回覆 15/16 之風管與補強）。", "Sin respuesta específica en la comunicación del 04‑09."),
 15: ("ok", "風管材質為鍍鋅鋼板＋PE 板保冷，對結構沒有影響。", "Ductos de chapa galvanizada con aislación PE; sin impacto estructural."),
 16: ("ok", "RC 放孔處補強，避免 RC 結構因受力崩裂；材質為黑鐵 SS400。", "Refuerzo de las aberturas de losa para evitar fisuración; acero negro SS400."),
 17: ("part", "9/4 回覆未明確確認（依 15 之說明應為風管）。", "No confirmado explícitamente; según el punto 15 son ductos de aire."),
 18: ("ok", "材質為黑鐵 SS400。", "Acero negro SS400."),
 19: ("open", "未回覆；S&W 建議三明治板並於第 2 階段確認鎂成分。", "Pendiente; S&W propone panel sándwich y confirmar el magnesio en la etapa 2."),
 20: ("ok", "天車軌道為現場粒包原料，若輸送系統臨時故障應急用，或設備故障維修用。", "El riel Skycar es para big‑bags de materia prima en caso de falla del sistema de transporte o para mantenimiento de equipos."),
 21: ("open", "未回覆。", "Pendiente."),
}
def split_q(q):
    parts = [t.strip() for t in q.strip().split("\n") if t.strip()]
    if len(parts) >= 3: return parts[0], parts[1], " ".join(parts[2:])
    if len(parts) == 2: return parts[0], parts[1], ""
    return q, "", ""
rows = ""
cnt = {"ok": 0, "part": 0, "open": 0}
for r in RFI:
    es, en, zh = split_q(r["q"])
    st, azh, aes = ANS.get(r["n"], ("open", "待決（尚未回覆）", "Abierta"))
    cnt[st] += 1
    lab = {"ok": "已回覆", "part": "部分回覆", "open": "待決"}[st]
    rows += f"<tr><td class=mono>{r['n']}</td><td class=mono>{esc(r['cat'])}</td><td><b>{esc(zh)}</b><div class=small style='margin-top:4px'>{esc(es)}</div><div class=small>{esc(en)}</div></td><td class=small>{esc(str(r['ref']).split(chr(10))[0])}</td><td><span class='tag {st}'>{lab}</span><div style='margin-top:4px'>{esc(azh)}</div><div class=small>{esc(aes)}</div></td></tr>"
extra = [
 ("地下室風道", "因製程輸送空調冷風用，需採 RC 製造（非鐵板），且兩個風道需連通（P0A30021）。"),
 ("3F Q/A 放孔", "1000×1000 共 20 孔未繪出（P0A30091A、P0A30061 圓圈處）。"),
 ("電梯機房", "維修保養樓梯示意及位置（P0A30071、P0A30111、P0A30121、P0A30131）。"),
 ("五大管線", "電氣、電信、給／排水及消防請一併規劃報價。"),
 ("外牆", "1–3 樓四周外牆採 RC 混凝土，不可用空心磚（後續管路施工須增設管支撐架，空心磚膨脹螺絲無法固定）。"),
 ("隔間", "現場所有隔間（含樓梯）採砌磚，需粉刷及油漆（1–4 樓）。"),
 ("放孔補強", "所有空調放孔周圍需加防水墩，設備放孔周圍需角鐵補強（P0A30091A 圓圈標示）。"),
 ("管道間", "結構為 RC，內部管路材質由業主自行處理（P0A30041）。"),
 ("快速捲門", "空調廠房用快速捲門，請建築師提供當地合適廠商確認；開關速度建議 50–100 cm/sec。"),
 ("施工階段", "原絲廠房所有工程結構採一次施工，不分階段；樓板及梁柱混凝土強度依建築師及結構技師計算提供。"),
 ("廁所", "位於一樓、一樓半、二樓、三樓樓梯平台處，合計 8 處。"),
 ("一般考量事項", "結構採 RC（H°A°）；基礎由第 2 階段地質勘測驗證；屋頂 Zincalum 4 合 1；1–3 層側牆改為 RC（原提空心磚）；4 層側牆 Zincalum 2 合 1；原提 2 階段建造改採一階段建造。"),
]
extra_html = "<div class='tw'><table><tr><th>主題</th><th>台灣方指示（2026‑09‑04）</th></tr>" + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td></tr>" for a, b in extra) + "</table></div>"
body = f"""<div class="hero"><h1>RFI 與回覆對照</h1><p>Salum &amp; Wenz（Arq. Jenny Curis González，2026‑09‑01）就 Revit 執行設計提出 31 項技術諮詢；台灣方於 2026‑09‑04 以「巴拉圭建築師問題點聯繫」回覆。下表逐項對照，並標出對造價有影響者（詳「建造成本」頁之未決事項）。</p>
<div class="meta"><span>已回覆 {cnt['ok']}</span><span>部分回覆 {cnt['part']}</span><span>待決 {cnt['open']}</span></div></div>
<section><h2>31 項 RFI</h2><div class="tw"><table><tr><th>No.</th><th>類別</th><th>問題（中文 · ES · EN）</th><th>參考</th><th>台灣方回覆 / 狀態</th></tr>{rows}</table></div>
<p class="small">類別：A 一般範圍／BIM · B 建築與材料 · C 結構與設備載重 · D 機電／MEP。</p></section>
<section><h2>台灣方 9/4 補充指示（非 RFI 編號項）</h2>{extra_html}</section>
"""
page("rfi.html", "RFI 與回覆", body)

# ---------------- model page ----------------
src3d = open("/tmp/claude-0/-home-claude/9c48902a-dc41-5562-85e3-84f377bbeda1/scratchpad/acelon_3d.html", encoding="utf-8").read()
navlink = '<div class="seg" role="group"><a href="index.html" style="display:inline-block;padding:9px 12px;font:600 13px \'Barlow Condensed\',\'Noto Sans TC\',sans-serif;letter-spacing:.05em;color:var(--ink2);text-decoration:none">← 首頁</a><a href="cost.html" style="display:inline-block;padding:9px 12px;font:600 13px \'Barlow Condensed\',\'Noto Sans TC\',sans-serif;letter-spacing:.05em;color:var(--ink2);text-decoration:none">建造成本</a></div>\n    '
src3d = src3d.replace('<div class="seg mobtabs"', navlink + '<div class="seg mobtabs"', 1)
open(os.path.join(ROOT, "model.html"), "w", encoding="utf-8").write('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + src3d.split("\n", 1)[0] + "</head><body>" + src3d.split("\n", 1)[1] + "</body></html>")
print("built")
