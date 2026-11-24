# 1729：含羞草的時鐘（Remotion + Three.js）

約 60 秒、1920×1080 / 30fps。人物與物件直接取自分鏡圖（`assets/storyboard.webp`）的原畫，
切成一張張「剪紙」元件，再依文稿重新編排成 6 幕——不是照抄分鏡格。

## 手法

- **鉛筆素描 → 上色**：每個元件在 Three.js 用自訂 shader 呈現：先以石墨色的斜向排線「畫」出線稿，再沿另一個方向把顏色刷上去（`src/components/Stage.tsx`）。
- **拼貼**：部分元件帶剪刀剪過的白紙邊與陰影，像被貼到紙上一樣滑入、壓實（`collage()`）。
- **2.5D**：元件放在不同深度，鏡頭緩慢推移產生視差。
- **轉場**（`src/transitions.tsx`，每個 1.8–2.4 秒）
  1. 1729 → 德梅朗：鉛筆排線把下一頁「塗」出來
  2. 德梅朗 → 含羞草：舊頁被撕開
  3. 含羞草 → 看太陽？：新的一張紙滑進來疊上
  4. 看太陽？ → 櫃子：黑紙遮住太陽、擴散成全黑，再縮成櫃子裡的黑暗
  5. 櫃子 → 時鐘：鉛筆排線

## 分幕

| 幕 | 秒 | 內容 |
|---|---|---|
| S1 1729 | 8.5 | 年份緞帶素描上色，地球儀、書本拼貼放上 |
| S2 德梅朗 | 10 | 肖像逐線畫出，軌道、名字、望遠鏡圍繞 |
| S3 日開夜合 | 13 | 太陽落下、夜空紙片滑入、紙張轉藍；張開的葉子被擦回鉛筆線，再重畫成合起的樣子 |
| S4 看太陽？ | 12 | 太陽到葉子的虛線（「看太陽」）；黑紙遮住太陽，畫出問號 |
| S5 櫃子 | 16 | 櫃子外日月輪替、紙張變色；右側結果卡片依日夜被圈起 |
| S6 時鐘 | 11 | 懷錶，太陽與夜空繞著它轉，小含羞草跟著開合 |

## 指令

```bash
npm i
npm run dev      # Remotion Studio；Scenes/ 資料夾可單獨預覽每一幕
npm run render   # 輸出 out/mimosa-clock.mp4
```

| 想改 | 改哪裡 |
|---|---|
| 字幕文字、時間 | 各幕 `src/scenes/S*.tsx` 的 `<Captions items=...>`（改中文後 `npm run assets`） |
| 每幕長度 / 轉場長度 | 各幕 `S*_SECONDS`；`src/MimosaClock.tsx` 的 `TRANSITIONS` |
| 元件位置、出場時間 | 各幕的 `pieces`：`sketchIn(t, 開始秒, 長度)`、`collage(t, 開始秒, {從哪滑入})` |
| 元件怎麼切 | `scripts/cut_elements.py` 的 `ELEMENTS`，再 `npm run cut`（需 numpy、opencv、scipy、pillow） |

素材：分鏡 5 格以 Real-ESRGAN x4plus 放大 4 倍並與一般縮放 65:35 混合 → `assets/panels/`。
若有分鏡原始高解析度圖，替換這些檔案再 `npm run cut`，畫質會更好。
字幕字型 Noto Sans TC（SIL OFL）。
