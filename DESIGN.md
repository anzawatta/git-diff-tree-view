# git-diff-tree-view System Design

## Problem: 解決する課題

**現状:**
`git diff --stat` の出力はフラットなファイル一覧であり、変更がディレクトリ階層のどこに集中しているかを視覚的に把握しづらい。特にネストが深いリポジトリでは、変更の構造的全体像を掴むのにコストがかかる。

**目指す状態:**
git diff の変更ファイル一覧をtree形式で表示し、変更の空間的分布を一目で把握できる。既存のgitワークフロー（パイプライン）にゼロコストで組み込める。

## Design Principles: 設計原則

### Pure Pipe Filter
- 説明: stdin → transform → stdout の単方向パイプフィルターとして動作する。副作用ゼロ——ファイルシステムへの書き込み、gitの内部状態への介入、一切行わない
- 理由: Unix哲学の合成可能性（composability）がこのツールの存在意義。パイプラインの任意の位置に挿入・除去できる

### Plumbing Over Porcelain
- 説明: 入力として `git diff --numstat`（plumbing層・タブ区切り・フォーマット安定保証）を前提とする。`--stat`（porcelain層・人間向け整形・フォーマット不安定）は受け付けない
- 理由: gitアーキテクチャにおいてporcelain出力のフォーマットは安定性が保証されない。機械可読なplumbing出力に依存することで、gitバージョン間の互換性リスクを排除する

### Complexity Budget
- 説明: ツール全体を50行前後に収める。型の多態性はdict値の型（str/dict）で表現し、dataclass等の構造化は導入しない
- 理由: このツールが解決する問題の規模に対して、抽象化のコストが見合わない。Trie構造の構築が `setdefault` 1行で済むことが、この設計の正しさの証左

## Conflict Resolution: 原則間の衝突ルール

**Plumbing Over Porcelain** が **Complexity Budget** に優先する。
numstatパーサーはstatパーサーより若干コードが増える（stat文字列の再構築が必要）が、入力の安定性は50行の制約より重い。壊れないことが、短いことに勝つ。

**Zero Dependencies** が利便性に優先する。
rich等のライブラリで美しいtree表示は可能だが、依存ゼロの制約を破る理由にならない。組み込みの文字（`├──`, `└──`, `│`）で十分。

## Non-Goals: 意図的にやらないこと

- **インタラクティブUI**: ツリーの折りたたみ・展開等は行わない。stdout出力で完結する
- **git操作**: diffの取得自体はこのツールの責務外。入力はパイプで受け取る
- **複数diff形式の自動判定**: `--stat` と `--numstat` を自動判別するような曖昧さは持たない。入力形式は `--numstat` 一択
- **色付け・装飾**: ANSIカラー等の端末依存機能は考慮しない
