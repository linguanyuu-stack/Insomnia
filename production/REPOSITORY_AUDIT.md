# 儲存庫檢查紀錄

檢查基準為 2026-11-24 可取得的四個公開分支，共 21 筆可達的歷史提交。專案分支及版本見 [既有製作索引](EXISTING_PROJECTS.md)。

| 項目 | 檢查結果 |
| --- | --- |
| GitHub 可見性與權限 | 公開，GitHub Pages 未啟用。API 回傳一位 `admin` 協作者。預設分支回傳 `protected: false`，可查的儲存庫規則集和套用到預設分支的規則皆為空。細部保護、GitHub Actions 權限和 Secret Scanning 警示端點對目前整合回傳 403。 |
| 敏感資料 | Gitleaks v8.30.1 掃描 21 筆提交的歷史差異，沒有偵測到符合規則的憑證。歷史路徑檢查未見常見金鑰或 `.env` 檔名。抽查既有短片的原始 WAV 與一個 Remotion MP4 的中繼資料。掃描涵蓋 Git 歷史差異與上述抽查，錄音內容、個資、肖像同意及素材授權尚未逐項驗證。 |
| 權利資料 | 既有網頁短片帶有素材來源表及部分字型授權檔。未見儲存庫層級的 LICENSE，並可見原始錄音已在公開分支。再利用素材前按素材清單確認授權與公開同意。 |
| 大型檔案 | 565 個歷史 Git blobs 中，5 個達 10 MiB，皆為 MP4。最大為 `video/mimosa-remotion/mimosa-1729.mp4` 的歷史版本，約 35.3 MiB。沒有檔案超過 50 MiB 或 100 MiB。本地 Git pack 約 234.9 MiB，包含歷史版本。 |
| Git LFS | 歷史路徑未見 `.gitattributes`，`git lfs ls-files --all` 無項目。這次提案只有 Markdown，無需啟用 LFS。未來需要和版本同步的大型原始素材可評估 LFS，反覆產生的渲染輸出可用核准的交付儲存。 |

本次提案以預設分支的圖解書版本為基準，新增前期製作規範與模板。既有動畫實作各由原有分支管理，未來單集以交接文件指定實作基準。 [GitHub 專案](https://github.com/linguanyuu-stack/Insomnia)
