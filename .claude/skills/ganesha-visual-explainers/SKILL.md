---
name: ganesha-visual-explainers
description: "ガネーシャ×ナツキの対話形式に、図解ビジュアルを融合した解説HTMLを生成し、surge.shに公開する。「図解で解説して」「図解付きで教えて」「ビジュアルで説明して」「〜を図で解説して」「このファイルを図解して」と依頼された際に使用する。"
user-invocable: true
argument-hint: "[テーマや解説したい内容]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Agent
context: fork
agent: general-purpose
---

# ganesha-visual-explainers スキル

ガネーシャ×ナツキの対話で話を進めつつ、対話の合間にTailwind CSSベースのリッチな図解ビジュアルを挟んで理解を深めるHTMLを生成し、surge.shに公開する。

品質基準は「入社したての新卒社会人が読んでも腹落ちする明快さ」。

## 依存

- [references/character-usage.md](references/character-usage.md) — キャラクター設定・表情使い分け・対話HTMLパターン・セリフの書き方
- [references/html-structure.md](references/html-structure.md) — テンプレート構造・gvカラーシステム・Lucideアイコン・コンポーネントパターン
- [references/exemplar.md](references/exemplar.md) — 模範解答の構造・再利用可能なHTMLスニペット・品質チェックリスト
- [references/term-dictionary.md](references/term-dictionary.md) — 技術用語→やさしい言葉の変換辞書・用語解説ボックスの書き方
- [references/base.html](references/base.html) — HTMLテンプレート本体
- `.claude/assets/avatars/` — ガネーシャ・ナツキのアバター画像

---

## ワークフロー

### Phase 0: リサーチ（サブエージェント）

トピックが **このプロジェクト（tokuyama-project）に関連するか** を判定し、調査方法を分岐する。

#### A. プロジェクト関連トピックの場合

「このプロジェクトの認証」「うちのDB設計」「このアプリのルーティング」など、tokuyama-projectのコード・設計・使用技術に関わるトピックの場合。

**2つのサブエージェントを並列起動する：**

```
// サブエージェント1: コードベース調査
Agent({
  subagent_type: "Explore",
  description: "プロジェクトのコード調査",
  prompt: `
    tokuyama-projectプロジェクトのコードベースを調査してください。

    【調査対象】{トピック名}（例: 認証の仕組み、ルーティング設計、データモデル等）

    調査手順：
    1. まず CLAUDE.md を読んでプロジェクト全体像を把握
    2. docs/ 内の関連仕様書を読む（architecture/, features/, db/, business/）
    3. トピックに関連するソースコード（app/配下）を読む
    4. マイグレーション（database/migrations/）があれば確認

    出力形式：
    - このプロジェクトでの実装方法（具体的なファイルパス・関数名・コード抜粋を含む）
    - 使用している技術・ライブラリ
    - 設計上の判断とその理由（わかる範囲で）
    - 関連ファイル一覧
  `
})

// サブエージェント2: 技術の一般知識を調査
Agent({
  subagent_type: "Explore",
  description: "技術の一般知識を調査",
  prompt: `
    以下の技術トピックについて一般的な知識を調査してください：
    【対象】{トピックの技術名}（例: Laravel Sanctum, Vue Router, Eloquent ORM等）

    調査項目：
    1. この技術の正確な定義（公式ドキュメント優先）
    2. 仕組み・動作原理
    3. 典型的なユースケース
    4. 初心者がつまずきやすいポイント
    5. 関連する公式ドキュメントのURL

    結果は箇条書きで整理して返してください。
  `
})
```

**Phase 1以降では両方の結果を組み合わせて**、「このプロジェクトではこう実装されていて、その裏にはこういう仕組みがある」という解説を作る。図解にはプロジェクトの実際のコード・ファイル構成・データフローを題材として使う。

#### B. 一般トピックの場合

プロジェクトに直接関係しないトピック（例: CSRF、Git、Dockerなど）。

```
Agent({
  subagent_type: "Explore",
  description: "トピックの調査",
  prompt: `
    以下のトピックについて徹底的に調査してください：
    【対象】{URL or トピック名}

    調査項目：
    1. このトピックの正確な定義（公式ドキュメント優先）
    2. 主要な概念・用語の一覧
    3. 典型的なユースケース3つ以上
    4. 初心者がつまずきやすいポイント
    5. 最新の動向・変更点
    6. 関連する公式ドキュメントのURL

    結果は箇条書きで整理して返してください。
  `
})
```

### Phase 1: ソース読み込み

1. URLなら `WebFetch` で取得、ドキュメントなら内容を分析
2. **情報の全体像を把握**（漏れなく）
3. **Phase 0のリサーチ結果と照合**して抜け漏れを確認
4. 以下のreferencesを読み込む:
   - [references/character-usage.md](references/character-usage.md)
   - [references/html-structure.md](references/html-structure.md)
   - [references/exemplar.md](references/exemplar.md)
   - [references/base.html](references/base.html)

### Phase 2: 用語翻訳表を作成

技術用語を洗い出し、やさしい言葉に変換する。[references/term-dictionary.md](references/term-dictionary.md) を参照し、既存の変換を活用しつつ、トピック固有の用語も追加する。

| 技術用語 | やさしい言葉 | たとえ |
|---------|------------|--------|
| 例: コールバック関数 | チェック係 | 「何かあったら呼んでね」と登録しておく処理 |

### Phase 3: たとえ話を3つ以上考える

| 種類 | 例 |
|-----|-----|
| 身近な例 | 会社のセキュリティゲート、郵便配達 |
| デジタルな例 | スマホの権限ダイアログ |
| 視覚的な例 | 信号機、地図、フローチャート |

### Phase 4: 情報を絞り込む

- 「まず覚える3つ」を決定
- 全体の中の位置づけを示す
- 優先度の低い情報は後半に配置

### Phase 5: キャラクター対話 + 図解を設計

[references/character-usage.md](references/character-usage.md) に準拠し、対話の流れと図解の配置を設計する。

**対話と図解の交互配置が最重要ルール。** 対話が3往復以上続いたら、必ず図解を挟む。

**図解パターンの選択は `html-structure.md` 末尾の「図解パターンの使い分け」テーブルに従うこと。** 説明したい内容（プロセス・比較・階層・通信・ファイル構成など）に対応するパターンを必ず参照し、テキストやASCIIアートで代替しない。

#### 解説の手法（必ず守ること）

- **例え話**で導入し、実際の内容に**会話と図解で**マッピングする
- 偉人を「ワシの教え子」と称しエピソードを交える（テーマに合った偉人を選ぶ）
- **初心者が間違えやすそうなポイント**も丁寧に説明する
- **なぜそうなるのか？ないと何が不便か？何が便利か？** などメリットの観点に必ず言及
- ナツキ👩‍💻が時々ガネーシャ🐘の矛盾や曖昧さに鋭くツッコミを入れる

#### その他の指針

- **概論 → 各論** — いきなり詳細に入らない
- **専門用語は初出で必ず解説**（用語解説ボックスを使用）
- **たとえ話で身近な体験に結びつける** — たとえ話はテキストだけで済まさず図解化する
- **簡潔にまとめすぎない** — 理解に必要な情報量は削らない
- **図を早く見せる** — テキストが2段落以上続いたら図を入れる
- **読者のレベルに言及しない** — 「初心者向け」「入門」等は使わない
- **日本語で** — 英語メインのトピックでも、図解は日本語で書く

### Phase 6: HTML生成

1. [references/base.html](references/base.html) を `output/{スラッグ}.html` にコピー
2. [references/html-structure.md](references/html-structure.md) のコンポーネントパターンを活用してHTMLを組む
3. プレースホルダーを置換:
   - `<!-- TITLE -->` → タイトル（ガネーシャ口調）
   - `<!-- DESCRIPTION -->` → 内容を要約した1文
   - `<!-- CONTENT_START -->` 〜 `<!-- CONTENT_END -->` → 生成したコンテンツ
4. [references/term-dictionary.md](references/term-dictionary.md) の用語解説ボックスを配置
5. インライン出典を添える（`text-xs text-gv-dim`、外部リンクには `target="_blank" rel="noopener noreferrer"`）

### Phase 7: 批判的レビュー（サブエージェント）

**リテラシーが低いユーザー視点**で、忖度なくレビューする。

```
Agent({
  subagent_type: "general-purpose",
  description: "図解の批判的レビュー",
  prompt: `
    あなたは「ITに詳しくない新卒社会人」です。
    プログラミング経験はゼロ、スマホは使えるがアプリの仕組みは知りません。

    以下のHTML図解を読んで、**忖度なく**批判してください：

    【HTMLファイルパス】{path}

    ## レビュー観点

    1. **わからない言葉**: 説明されていても難しい言葉はどれか
    2. **たとえ話の違和感**: ピンとこない、逆に混乱するたとえはないか
    3. **情報過多**: 読むのが辛くなる部分、スキップしたくなる部分
    4. **キャラクターの不自然さ**: セリフが専門家っぽすぎないか
    5. **結局何がわかったか**: 読み終わって説明できる自信があるか

    ## 出力形式

    ### 致命的な問題（これがあると読めない）
    - ...

    ### 改善すべき点（直せばもっと良くなる）
    - ...

    ### 良かった点（このまま残すべき）
    - ...

    ### 総評
    5段階評価: ⭐⭐⭐☆☆（3/5）のように
    一言: 「○○だから△△な人には難しい」のように
  `
})
```

### Phase 8: ブラッシュアップ

Phase 7のレビュー結果を踏まえてHTMLを修正する。

**優先度**:
1. 致命的な問題 → 必ず修正
2. 改善すべき点 → 可能な限り対応
3. 良かった点 → 維持

**よくある修正パターン**:
- 用語解説ボックスの追加
- たとえ話の差し替え・追加
- 長いセクションの分割
- キャラクターのセリフをより素朴に

### Phase 9: デプロイ

Node.js の有無を確認する。

```bash
node --version
```

バージョン番号が表示された → そのまま公開の実行に進む。
`command not found` → [references/node-install-guide.md](references/node-install-guide.md) の手順に従ってインストールを案内する。

#### 公開の実行

```bash
bash .claude/skills/ganesha-visual-explainers/scripts/deploy.sh .claude/skills/ganesha-visual-explainers/output/{スラッグ}.html {スラッグ}
```

#### 初回の場合（Surge未登録）

> 初回のみアカウント登録が必要です。
> メールアドレスを入力して Enter → パスワードを決めて入力して Enter。
> 確認メールが届いたらリンクをクリックすれば登録完了です。

### Phase 10: INDEX.md の更新

デプロイ成功後、`.claude/skills/ganesha-visual-explainers/INDEX.md` のテーブル末尾に新しい行を追加する。

```
| {今日の日付} | {テーマ日本語名} | [HTML](output/{スラッグ}.html) | https://{subdomain}.surge.sh |
```

### Phase 11: 完了報告

#### 公開に成功した場合

```
完成・公開完了: 【タイトル】

（内容を1〜2文で要約）

公開URL:
https://ganesha-{スラッグ}-{xxxx}.surge.sh

主なポイント:
- （主要トピックを3〜5個）

この図解を削除したいとき:
チャット欄で「この図解を削除して」と伝えてください。
```

#### 公開できなかった場合

```
完成: 【タイトル】

（内容を1〜2文で要約）

ファイルの保存先:
output/{スラッグ}.html

主なポイント:
- （主要トピックを3〜5個）

URLで共有したいとき:
チャット欄で「この図解を公開して」と伝えてください。
```

### 図解の削除

ユーザーが「この図解を削除して」と依頼した場合:

1. `deploy-history.log` を読み、直近のデプロイURLを特定する
2. `npx surge teardown [ドメイン]` を実行する
3. 削除完了をユーザーに伝える

---

## 品質チェックリスト

[references/exemplar.md](references/exemplar.md) の品質チェックリストを参照。

---

## 守ること（禁止事項）

- **React・shadcn/ui を使わない**
- **インタラクティブ要素を入れない** — トグル、フェードイン、アニメーション、フォーム、クリックで開閉する要素は一切禁止
- **テンプレートに含まれるもの以外の `<style>` タグ・`<script>` を追加しない**
- **外部リソースを追加しない** — テンプレートに含まれるCDN以外の外部読み込みは禁止。ただしアバター画像（`images/`）は例外
- **テンプレートの額縁構造を変更しない**
- **対話だけで3往復以上続けない** — 必ず図解を挟む
- **図解だけで3つ以上続けない** — 必ず対話を挟む
