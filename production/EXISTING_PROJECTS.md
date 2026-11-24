# 既有製作索引

基準為這次提案檢查時的公開分支。下列連結固定到 commit，交接每集時應以該集核准的 commit 為準。路徑均相對於各自分支的倉庫根目錄。

| 分支 | 基準 commit | 內容與入口 |
| --- | --- | --- |
| `claude/nice-dirac-99lodh`（預設） | [`03a91d5`](https://github.com/linguanyuu-stack/Insomnia/tree/03a91d506264958499c8de8b4624fecaa98f6bce) | 圖解書及民眾版 HTML，`figs/`、`figs_public/` 插圖與產生腳本，`kit/build.py`、`kit/build_public.py` 建置流程，`public/source.html` 民眾版來源。 |
| `claude/wonderful-wright-3tju9u` | [`fb12404`](https://github.com/linguanyuu-stack/Insomnia/tree/fb12404143f40222cff0b4f633c7e346230f97b2/video/mimosa-clock) | `video/mimosa-clock/` 的 Remotion、React 與 Three.js 動畫，含分鏡原畫、切件、字型和既有 MP4。從該目錄 `README.md`、`package.json`、`src/Root.tsx` 查閱預覽及渲染入口。 |
| `claude/sleepy-ride-tcxtvh` | [`dc2680e`](https://github.com/linguanyuu-stack/Insomnia/tree/dc2680e29992043300c8f18dbd145021307c2309) | `site/insomnia-shorts/ch01/index.html` 預覽短片，`site/insomnia-shorts/lib/engine.js` 為網頁動畫引擎。文稿、原始錄音、素材、MP4 和 SRT 在 `books/insomnia-shorts/`，旁白資料在 `content/insomnia-shorts/`，相關程式在 `tools/insomnia-shorts/`。 |
| `claude/intelligent-planck-xaw3og` | [`626f79a`](https://github.com/linguanyuu-stack/Insomnia/tree/626f79a0f55bc3f0e2e17233f2a16bce152f08af/books/insomnia-film) | `books/insomnia-film/` 保有長版腳本及短版 v1。 |

過往版本可由既有分支歷史查閱。前期分支的用途與跨分支交接方式見 [製作流程](../PRODUCTION_PIPELINE.md)。
