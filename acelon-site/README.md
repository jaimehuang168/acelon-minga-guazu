# ACELON Minga Guazú — 新廠設計圖、3D 概念模型與建造成本

台巴智慧科技園區（PTITP）內 ACELON 原絲／假撚新廠的設計整理網站（靜態頁面，GitHub Pages / Vercel）。

- `index.html` 首頁
- `model.html` 互動式 3D 概念模型（Three.js，內嵌 Salum & Wenz IFC 結構、各層設備、向量平面）
- `plans.html` 台灣方全套圖說 P0A30011–P0A30170 與園區管線系統圖
- `cost.html` 巴拉圭總建造成本估算（AACE Class 3）
- `rfi.html` 31 項 RFI 與台灣方 9/4 回覆對照
- `assets/files/` 成本估算 Excel、GLB / OBJ 模型、平面向量資料 JS

重新產生頁面：`python3 build_site.py`（讀取 `assets/cost_data.json`、`assets/rfi_raw.json`）。

資料基準：Salum & Wenz IFC 2026‑07‑31、台灣方圖說 2026‑09‑03 版、9/4 回覆、CYPE／costeo.com.py 單價、BCP 匯率 2026‑09‑15。本站內容為概念設計與估算，非正式報價。
