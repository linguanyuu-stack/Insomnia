# Insomnia 前期製作

| 位置 | 用途 |
| --- | --- |
| [episodes/](episodes/README.md) | 每集的核准規格、素材清單及交接紀錄 |
| [templates/episode/](templates/episode/README.md) | 可直接複製的空白單集資料夾 |
| [library/](library/README.md) | 可跨集引用的公開素材與版本索引 |
| [EXISTING_PROJECTS.md](EXISTING_PROJECTS.md) | 既有圖解書、短片實作與文稿的分支和入口 |
| [REPOSITORY_AUDIT.md](REPOSITORY_AUDIT.md) | 建置提案時的公開權限、敏感資料與大檔檢查 |

## 開立單集

在儲存庫根目錄執行。把 `series-ep001-topic` 改成固定、唯一的小寫短 ID。中文集名填在單集 README。

```bash
episode_id=series-ep001-topic
mkdir "production/episodes/$episode_id" &&
  cp -R production/templates/episode/. "production/episodes/$episode_id/"
```

先填單集 `README.md`，依序完成各文件，最後以 `HANDOFF.md` 指定 Claude Code 的工作範圍。參考 [製作流程](../PRODUCTION_PIPELINE.md) 與 [風格指南](../STYLE_GUIDE.md)。
