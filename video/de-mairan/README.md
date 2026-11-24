# 1729：德梅朗與含羞草的時鐘（Remotion + Three.js）

約 52 秒、1920×1080 / 30fps。畫面直接使用分鏡圖（`assets/storyboard.webp`）裡的原畫，
切成透明圖層，放進 Three.js 的 3D 空間（每層不同深度），再用緩慢的鏡頭推移製造視差（2.5D）。
所以人物、植物、字卡都和分鏡一模一樣。

## 指令

```bash
npm i
npm run dev      # Remotion Studio：主片 DeMairan1729；Scenes/ 下可單獨預覽 5 幕
npm run render   # 輸出 out/de-mairan-1729.mp4
```

## 修改

| 想改 | 改哪裡 |
|---|---|
| 字幕文字、出現時間 | 各幕檔案 `src/scenes/*Scene.tsx` 底部的 `<Captions items=...>`（改完跑 `npm run assets` 更新字型） |
| 每幕長度 | 各幕的 `*_SECONDS` |
| 轉場長度 | `src/MairanVideo.tsx` 的 `FADE_FRAMES`（預設 45 格 = 1.5 秒） |
| 鏡頭路線、圖層淡入時間、深度 | 各幕的 `cam={...}` 與 `anims={...}`（座標 = 分鏡格子像素 × 4） |
| 圖層怎麼切 | `scripts/extract_layers.py` 的 `LAYERS` 多邊形，再跑 `npm run layers` |

## 素材流程

1. 從分鏡圖裁出 5 格 → Real-ESRGAN x4plus 放大 4 倍，與一般縮放 65:35 混合（保留色鉛筆質感）→ `assets/panels/*_x4.png`
2. `npm run layers`：依紙色差去背、切圖層 → `public/layers/`、`src/layers.json`
3. `npm run assets`：紙張底圖 `public/paper.jpg`、字幕字型（Noto Sans TC 子集）

如果有分鏡的**原始高解析度圖**，替換 `assets/panels/*_x4.png`（同比例）再跑第 2 步，畫質會更好。
