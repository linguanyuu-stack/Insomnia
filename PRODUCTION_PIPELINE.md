# Insomnia 製作流程

## 階段與交付

| 階段 | 負責 | 交付與完成條件 |
| --- | --- | --- |
| 研究與立案 | ChatGPT、工作室負責人 | 確定受眾、主問題、範圍及來源。可查證主張編入文稿。 |
| 導演前期 | ChatGPT、工作室負責人 | 核准文稿、分鏡、角色、動畫規格與風格樣張（如適用）。 |
| 製作交接 | Codex、工作室負責人 | 整理素材、授權、版本與技術基準，檢查全部必要依賴，核准後將交接狀態標為 `ready`。 |
| 試片、動畫與渲染 | Claude Code | 從指定引擎 commit 開實作分支，驗證指定鏡頭，按規格完成全片、字幕及輸出。 |
| 驗收 | 工作室負責人、Claude Code、Codex | 比對文稿、分鏡、素材權利、畫面、聲音與技術規格，記錄檢查結果、輸出位置及實作 commit。 |

## 從前期版本交給 Claude Code

1. 從 [單集模板](production/templates/episode/README.md) 開案。跨文件沿用 `BEAT-01`（敘事段落）、`SHOT-010`（鏡頭）、`CHAR-01`（角色）、`ASSET-001`（素材）和 `REF-01`（來源）這類穩定 ID。刪除或拆分項目時更新所有引用。
2. 審核 `HANDOFF.md` 的文件、技術基準、素材可存取性與驗收條件。必要欄位填實值或寫明不適用的原因。阻擋實作的缺口保留在 `blocked`，可延期的項目要注明核准的替代方案及影響。
3. 提交核准文件。工作室在啟動訊息附上 repo、前期 commit SHA、單集 `HANDOFF.md` 路徑，並在 `HANDOFF.md` 記載實作來源分支和完整 SHA。前期 SHA 由啟動訊息傳遞，因此同一 commit 的文件就能固定版本。
4. Claude Code 從已取得的實作 SHA 開新分支。若兩份文件樹分屬不同基準，可從 repo 根目錄使用以下命令。先把 `IMPLEMENTATION_SOURCE_BRANCH`、`IMPLEMENTATION_SHA`、`IMPLEMENTATION_BRANCH`、`IMPLEMENTATION_WORKTREE` 分別設為來源分支、核准的實作 commit、新分支和本機新目錄。此例以 Insomnia 為 `origin`。

   ```bash
   git fetch origin "${IMPLEMENTATION_SOURCE_BRANCH:?}" &&
   git merge-base --is-ancestor "${IMPLEMENTATION_SHA:?}" FETCH_HEAD &&
   git worktree add -b "${IMPLEMENTATION_BRANCH:?}" "${IMPLEMENTATION_WORKTREE:?}" "${IMPLEMENTATION_SHA:?}"
   ```

5. 啟動訊息可直接寫「請依 Insomnia 前期 commit `<SHA>` 下的 `production/episodes/<episode-id>/HANDOFF.md` 實作。前期檢出為 `<絕對路徑>`。依其中的基準 commit 建立實作分支，按交付與驗收清單回報。」交接文件應自足，決策要寫入該集文件。
6. 規格變更時，更新受影響的文件與素材版本，在 `HANDOFF.md` 記錄影響和核准者，建立新版前期 commit。實作回報注明使用的交接版本和前期 SHA。

## 公開權限與素材存放

- 分支與 PR 仍屬公開儲存庫。提交前檢查新增檔案與差異，檔名、內文、圖片及音檔中繼資料、引用連結與簽名網址都可能暴露資料。
- 權利確定且可公開的文件、輕量素材與必要的來源證明，可用一般 Git 追蹤。人聲、患者資料、合約、存取憑證與未授權資產應按實際權限處理。受限素材透過受控儲存取得，Git 清單只記可公開的 ID、版本和取得方式。保留授權條款、署名及同意紀錄於核准的位置。
- 建議從 **50 MiB** 起在提交前評估體積、改版頻率與下載成本。GitHub 一般 Git 檔案超過 **50 MiB** 會警告，超過 **100 MiB** 會阻擋。需與原始碼版本同步且可公開的大型來源素材，可在確認配額、可用性後用 Git LFS，並以窄範圍規則追蹤。LFS 提供版本對應，下載權限應按實際託管設定確認。
- 可重建的暫存檔、預覽或輸出，依發布需求放在核准的儲存、成品交付管道或公開 Release。清單記載版本、檔名、取得方式和需要時的 SHA-256。新的 LFS 規則或歷史遷移另案評估。
- 若發現曝露的憑證或受限資料，應先通知工作室、撤銷或輪替憑證並確認曝露範圍，再決定移除方式。公開歷史可能已被複製。

更多 GitHub 檔案限制與 LFS 說明見官方文件。 [大型檔案限制](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) · [Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
