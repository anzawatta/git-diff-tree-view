# git-diff-tree-view

`git diff --numstat` の出力をツリー形式で表示する Unix パイプフィルター。

## Locale

### Landmarks
- `git-diff-tree-view.py` — 唯一の実装（40行）。Parser + Trie + Renderer が一体
- `PRINCIPLE.md`             — 設計原則・Non-Goals・衝突ルール（変更前に必読）

### Paths
```
stdin (git diff --numstat)
  → パース（タブ区切り → added/deleted/path）
  → Trie 構築（pathlib.Path.parts + setdefault）
  → レンダリング（再帰、末尾判定で └──/├── を切り替え）
  → stdout
```

### Edges
- **stdin**  — `git diff --numstat` 形式のみ受け付ける（`--stat` 非対応。設計決定）
- **stdout** — テキスト出力のみ。ANSI 色なし、ファイル書き込みなし
- **依存**   — Python stdlib のみ（sys, pathlib）。外部ライブラリゼロ

<!-- last-verified: 2026-04-26 -->
