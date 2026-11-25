# 茯苓的告白 — 四神藥膳包 動畫短片

Remotion + three.js 製作的 1:30（2700 幀 / 30fps / 1920×1080）愛情小劇場。

## 分鏡

| 幕 | 幀 | 內容 |
|---|---|---|
| S1 片頭 | 0–150 | 「茯苓的告白」標題、3D 花瓣飄落 |
| S2 臥房 | 150–540 | 茯苓窩在被窩、想念蓮子、想買花卻被濕氣雲壓回床上 |
| S3 救援 | 540–990 | 芡實、川芎破門而入：用拉的、用拖的、用背的 |
| S4 屋外 | 990–1290 | 外頭濕氣更重，茯苓吸飽水氣腫成一大團，兩人推不動倒地 |
| S5 靈光 | 1290–1470 | 川芎想到辦法 → 當歸、淮山、枸杞 三大廚神登場 |
| S6 熬湯 | 1470–1890 | three.js 3D 湯鍋，七味藥材（依包裝配方錢數）依序下鍋、熬成四神湯 |
| S7 變身 | 1890–2190 | 喝湯後水氣蒸發、消腫變苗條、長出肌肉，元氣滿滿 |
| S8 告白 | 2190–2550 | 摘玫瑰、按門鈴、半蹲獻花；五位好友躲在樹叢偷看，蓮子收下後全員衝出歡呼（3D 彩帶） |
| S9 字卡 | 2550–2700 | 四神藥膳包包裝 + 「健脾祛濕・找回好元氣」 |

## 指令

```bash
npm i
npm run dev                                   # Remotion Studio 預覽
npx remotion render SishenLove out/sishen-love.mp4
```

雲端／無 GPU 環境：`remotion.config.ts` 已設定 `swangle` GL；若需指定瀏覽器，設 `REMOTION_BROWSER=/path/to/chrome-headless-shell`。

## 素材流程（tools/）

- `extract.py`：從角色設定圖（`src_art/1,3,5.webp`）去背切出 30 個姿勢 → `public/sprites/`
- `extract_goji.py`：用 GrabCut 從包裝插圖切出枸杞（無獨立設定圖）
- `assets.py`：產生 `src/sprites.json`、紙紋 `public/paper.jpg`、包裝正反面去背
- `fonts.py`：下載只含片中用字的粉圓（Huninn）與霞鶩文楷 TC 子集字型 → `public/fonts/`
  （改了台詞若出現新字，重跑這支）
- `soundtrack.py`：numpy 合成五聲音階配樂＋音效（門鈴、彈簧、滴水、蒸氣、彩帶），對齊分鏡幀數 → `public/soundtrack.wav`

改了場景長度時，同步更新 `tools/soundtrack.py` 頂端的場景起點並重跑。
