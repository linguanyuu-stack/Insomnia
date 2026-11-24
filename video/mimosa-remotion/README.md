# 1729：含羞草的時鐘（Remotion）

約 32 秒、1920×1080 / 30fps 的色鉛筆風知識動畫：德梅朗把含羞草關進不透光的櫃子，葉子仍按日夜開合——植物身體裡有自己的時鐘。

成片：`mimosa-1729.mp4`

## 指令

```bash
npm i
npm run dev        # Remotion Studio 預覽、拖時間軸
npm run render     # 輸出 out/mimosa-1729.mp4
npm run fonts      # 改過中文字後重建字型子集（需 pip install fonttools brotli）
```

## 結構

| 檔案 | 內容 |
|---|---|
| `src/timeline.ts` | **每一幕長度、轉場長度、字幕文字與時間**（改節奏改這裡） |
| `src/MimosaVideo.tsx` | 主影片：`TransitionSeries` 串起 6 幕 + 字幕軌 |
| `src/Root.tsx` | 主影片 `Mimosa1729`，以及 `Scenes/` 資料夾下可單獨預覽的 6 幕 |
| `src/scenes/*` | 各幕：1729、德梅朗、含羞草日夜、看太陽？、不透光的櫃子、體內時鐘 |
| `src/components/Paper.tsx` | 紙張底紋 + 色鉛筆濾鏡（線條每 3 格「抖」一次） |
| `src/components/MimosaStage.tsx`, `CabinetStage.tsx` | 第 3/4 幕、第 5/6 幕共用的場景 |
| `src/lib/draw.ts` | 程式化繪圖：含羞草葉片開合、德梅朗、太陽月亮、懷錶… |

字型：霞鶩文楷 TC（LXGW WenKai TC）、IM Fell English、Pinyon Script，皆為 SIL OFL，取自 @fontsource。
