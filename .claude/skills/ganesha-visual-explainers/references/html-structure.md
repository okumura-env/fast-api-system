# HTML構造ガイド

## テンプレート構造

`base.html` の構造:

```
<!DOCTYPE html>
├── <head>
│   ├── meta（noindex, OG tags）
│   ├── favicon（SVGインライン）
│   ├── Google Fonts（Noto Sans JP, JetBrains Mono）
│   ├── Tailwind CSS CDN + gvカラーシステム設定
│   └── 印刷用CSS
├── <body>
│   ├── PDF出力ボタン（no-print）
│   ├── <main>
│   │   ├── <!-- CONTENT_START -->
│   │   └── <!-- CONTENT_END -->
│   ├── <footer>（© miyata-press）
│   ├── Lucide Icons CDN
│   └── lucide.createIcons()
```

### プレースホルダー

| プレースホルダー | 置換先 |
|----------------|--------|
| `<!-- TITLE -->` | タイトル（ガネーシャ口調。例:「変数ってなんやねん？」） |
| `<!-- DESCRIPTION -->` | 内容を要約した1文 |
| `<!-- CONTENT_START -->` 〜 `<!-- CONTENT_END -->` | 生成したコンテンツ全体 |

---

## gv カラーシステム

| カラー名 | 値 | 用途 |
|---------|-----|------|
| `gv-bg` | `#f0f4ff` | ページ背景 |
| `gv-surface` | `#ffffff` | カード・吹き出し背景 |
| `gv-border` | `#e0e7ff` | 区切り線 |
| `gv-primary` | `#4f46e5` | インディゴ系メインカラー |
| `gv-secondary` | `#7c3aed` | 紫系サブカラー、太字キーワード |
| `gv-accent` | `#6366f1` | アクセント |
| `gv-text` | `#374151` | 本文テキスト |
| `gv-heading` | `#312e81` | 見出し |
| `gv-muted` | `#6b7280` | 補足テキスト |
| `gv-dim` | `#9ca3af` | 出典、注釈 |
| `gv-code` | `#1e1b4b` | コードブロック背景 |
| `gv-ganesha` | `#f59e0b` | ガネーシャのボーダー |
| `gv-natsuki` | `#818cf8` | ナツキのボーダー |
| `gv-positive` | `#10b981` | 肯定・OK |
| `gv-negative` | `#ef4444` | 否定・NG |
| `gv-warning` | `#f59e0b` | 警告 |
| `gv-quote` | `#4c1d95` | 引用ボックスのテキスト |

---

## Lucide Icon の使い方

### 基本構文

```html
<i data-lucide="icon-name" class="w-6 h-6"></i>
```

### よく使うアイコン

| 用途 | アイコン名 | コード |
|-----|----------|--------|
| 重要 | `alert-circle` | `<i data-lucide="alert-circle" class="w-6 h-6 text-red-500"></i>` |
| ヒント | `lightbulb` | `<i data-lucide="lightbulb" class="w-6 h-6 text-yellow-500"></i>` |
| チェック | `check-circle` | `<i data-lucide="check-circle" class="w-6 h-6 text-green-500"></i>` |
| 情報 | `info` | `<i data-lucide="info" class="w-6 h-6 text-blue-500"></i>` |
| 警告 | `triangle-alert` | `<i data-lucide="triangle-alert" class="w-6 h-6 text-orange-500"></i>` |
| コード | `code` | `<i data-lucide="code" class="w-6 h-6 text-purple-500"></i>` |
| 質問 | `help-circle` | `<i data-lucide="help-circle" class="w-6 h-6 text-blue-500"></i>` |
| 本 | `book-open` | `<i data-lucide="book-open" class="w-6 h-6 text-indigo-500"></i>` |
| 学習 | `graduation-cap` | `<i data-lucide="graduation-cap" class="w-6 h-6 text-purple-500"></i>` |
| 矢印 | `arrow-right` | `<i data-lucide="arrow-right" class="w-6 h-6"></i>` |
| セキュリティ | `shield-check` | `<i data-lucide="shield-check" class="w-6 h-6 text-green-500"></i>` |
| ロック | `lock` | `<i data-lucide="lock" class="w-6 h-6 text-gray-600"></i>` |
| 設定 | `settings` | `<i data-lucide="settings" class="w-6 h-6 text-gray-500"></i>` |

---

## コンポーネントパターン

### セクションカード

```html
<div class="bg-white rounded-2xl shadow-sm border border-gv-border p-8 mb-8">
  <div class="flex items-center gap-3 mb-6">
    <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center">
      <i data-lucide="shield-check" class="w-6 h-6 text-gv-primary"></i>
    </div>
    <div>
      <h2 class="text-2xl font-bold text-gv-heading">セクションタイトル</h2>
      <p class="text-gv-muted">サブタイトル</p>
    </div>
  </div>
  <!-- コンテンツ -->
</div>
```

### 結論ボックス（引用スタイル）

```html
<div class="bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-gv-secondary rounded-xl p-5 my-8">
  <p class="text-gv-quote text-lg font-bold leading-relaxed">
    <i data-lucide="quote" class="w-5 h-5 inline-block mr-1 text-gv-secondary"></i>
    結論を1文で。
  </p>
</div>
```

### コード例の前の日本語解説

コードを見せる前に、必ず「このコードが何をするのか」を日本語で説明する。

```html
<!-- ❌ 悪い例: いきなりコード -->
<pre class="bg-gv-code text-indigo-200 p-4 rounded-xl"><code>hook.onPreToolUse(...);</code></pre>

<!-- ✅ 良い例: まず日本語で解説してからコード -->
<div class="mb-4">
  <div class="flex items-center gap-2 mb-2">
    <i data-lucide="code" class="w-5 h-5 text-gv-secondary"></i>
    <span class="font-bold text-gv-heading">このコードがやること</span>
  </div>
  <p class="text-gv-text ml-7">
    「Writeツール（ファイルを書き込む道具）」が使われそうになったら、
    <strong class="text-gv-negative font-bold">許可しない</strong>というルールを設定しています。
  </p>
</div>
<pre class="bg-gv-code text-indigo-200 p-4 rounded-xl font-mono text-sm"><code>hook.onPreToolUse((event) => {
  if (event.toolName === 'Write') {
    return { permissionDecision: 'deny' };
  }
});</code></pre>
```

### フローチャート（直線型）

```html
<div class="flex flex-col md:flex-row items-center justify-center gap-4 my-8">
  <div class="bg-indigo-100 px-6 py-4 rounded-xl text-center">
    <i data-lucide="play" class="w-8 h-8 text-gv-primary mx-auto mb-2"></i>
    <div class="font-bold">開始</div>
  </div>
  <i data-lucide="arrow-right" class="w-8 h-8 text-gv-dim hidden md:block"></i>
  <i data-lucide="arrow-down" class="w-8 h-8 text-gv-dim md:hidden"></i>
  <div class="bg-purple-100 px-6 py-4 rounded-xl text-center">
    <i data-lucide="shield-check" class="w-8 h-8 text-gv-secondary mx-auto mb-2"></i>
    <div class="font-bold">チェック</div>
  </div>
  <i data-lucide="arrow-right" class="w-8 h-8 text-gv-dim hidden md:block"></i>
  <i data-lucide="arrow-down" class="w-8 h-8 text-gv-dim md:hidden"></i>
  <div class="bg-green-100 px-6 py-4 rounded-xl text-center">
    <i data-lucide="check-circle" class="w-8 h-8 text-gv-positive mx-auto mb-2"></i>
    <div class="font-bold">完了</div>
  </div>
</div>
```

### フローチャート（分岐型）

条件判定（YES/NO）で処理が分岐するフローに使用する。エラーハンドリング、バリデーション、ルーティングなど「条件→アクション」の連鎖を視覚化するのに最適。

```html
<div class="bg-gray-50 rounded-2xl p-6 md:p-8 my-8">
  <!-- セクション見出し -->
  <div class="flex items-center gap-3 mb-6">
    <div class="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center">
      <i data-lucide="git-branch" class="w-5 h-5 text-gv-primary"></i>
    </div>
    <div>
      <h3 class="text-lg font-bold text-gv-heading">処理の流れ</h3>
      <p class="text-sm text-gv-muted">サブタイトル</p>
    </div>
  </div>

  <!-- フロー本体 -->
  <div class="flex flex-col items-center gap-3">
    <!-- 開始ノード -->
    <div class="bg-indigo-100 border border-indigo-200 px-8 py-4 rounded-xl text-center max-w-md w-full">
      <i data-lucide="wifi" class="w-6 h-6 text-gv-primary mx-auto mb-1"></i>
      <div class="font-bold text-gv-heading">開始の状態</div>
    </div>
    <i data-lucide="arrow-down" class="w-6 h-6 text-gv-dim"></i>

    <!-- 判定ノード（黄色） -->
    <div class="bg-yellow-50 border-2 border-yellow-300 px-8 py-4 rounded-xl text-center max-w-md w-full">
      <div class="font-bold text-yellow-800">条件を判定？</div>
      <div class="text-sm text-yellow-600">（補足説明）</div>
    </div>

    <!-- YES / NO 分岐 -->
    <div class="grid grid-cols-2 gap-4 w-full max-w-2xl">
      <!-- YES 側 -->
      <div class="flex flex-col items-center gap-2">
        <span class="text-sm font-bold text-gv-positive">YES</span>
        <i data-lucide="arrow-down" class="w-5 h-5 text-gv-dim"></i>
        <!-- アクションノード（赤＝エラー系 / 青＝遷移系 / 緑＝成功系） -->
        <div class="bg-red-50 border border-red-200 px-4 py-3 rounded-xl text-center w-full">
          <div class="font-bold text-red-700">エラー処理</div>
          <div class="text-sm text-red-500">「メッセージ」</div>
        </div>
      </div>
      <!-- NO 側 -->
      <div class="flex flex-col items-center gap-2">
        <span class="text-sm text-gv-muted">NO → 次のチェックへ</span>
        <i data-lucide="arrow-down" class="w-5 h-5 text-gv-dim"></i>
        <!-- 次の判定ノード or アクション -->
        <div class="bg-yellow-50 border-2 border-yellow-300 px-4 py-3 rounded-xl text-center w-full">
          <div class="font-bold text-yellow-800">次の条件？</div>
        </div>
      </div>
    </div>
  </div>
</div>
```

**ノードの色ルール:**

| ノード種別 | 背景色 | ボーダー | 用途 |
|-----------|--------|---------|------|
| 開始/状態 | `bg-indigo-100` | `border-indigo-200` | フローの起点・現在の状態 |
| 判定 | `bg-yellow-50` | `border-2 border-yellow-300` | YES/NO の条件分岐 |
| エラー処理 | `bg-red-50` | `border-red-200` | エラー表示・中断 |
| 遷移/リダイレクト | `bg-blue-50` | `border-blue-200` | 画面遷移・リダイレクト |
| 成功/続行 | `bg-green-50` | `border-green-200` | 正常終了・次へ進む |
| スルー/パス | `bg-gray-100` | `border-gray-200` | 何もせず次の処理へ |

**分岐の深さ:** 判定ノードをネストする場合は `grid grid-cols-2` を再帰的に使う。3段以上の深い分岐はセクションを分割して可読性を維持する。

### たとえ話ボックス

```html
<div class="bg-gradient-to-r from-amber-50 to-orange-50 p-6 rounded-xl border border-amber-200 my-6">
  <div class="flex items-center gap-2 mb-3">
    <i data-lucide="building-2" class="w-6 h-6 text-amber-600"></i>
    <span class="font-bold text-amber-800">たとえ話：会社のセキュリティゲート</span>
  </div>
  <div class="space-y-3 text-gv-text">
    <p>あなたが会社に出勤するとき、入口にはセキュリティゲートがありますよね。</p>
    <ul class="list-disc list-inside space-y-1 ml-2">
      <li><strong>社員証をかざす</strong> → 本人確認</li>
      <li><strong>ゲートが開く</strong> → 許可された行動が実行される</li>
      <li><strong>入館記録が残る</strong> → ログ記録</li>
    </ul>
  </div>
</div>
```

### 比較カード（左右対比）

```html
<div class="grid md:grid-cols-2 gap-4 my-6">
  <div class="bg-red-50 border border-red-200 rounded-xl p-5">
    <div class="flex items-center gap-2 mb-3">
      <i data-lucide="x-circle" class="w-6 h-6 text-gv-negative"></i>
      <span class="font-bold text-red-800">Before</span>
    </div>
    <p class="text-gv-text">改善前の状態を説明</p>
  </div>
  <div class="bg-green-50 border border-green-200 rounded-xl p-5">
    <div class="flex items-center gap-2 mb-3">
      <i data-lucide="check-circle" class="w-6 h-6 text-gv-positive"></i>
      <span class="font-bold text-green-800">After</span>
    </div>
    <p class="text-gv-text">改善後の状態を説明</p>
  </div>
</div>
```

### インライン出典

```html
<span class="text-xs text-gv-dim">
  (<a href="https://example.com" target="_blank" rel="noopener noreferrer" class="underline hover:text-gv-primary">出典</a>)
</span>
```

### レイヤー図（積み上げ構造）

```html
<div class="flex flex-col items-center gap-0 my-8">
  <div class="w-full max-w-md bg-gradient-to-r from-blue-100 to-blue-200 border-2 border-blue-300 rounded-t-xl p-4 text-center">
    <div class="flex items-center justify-center gap-2">
      <i data-lucide="monitor" class="w-5 h-5 text-blue-600"></i>
      <span class="font-bold text-blue-800">上層レイヤー名</span>
    </div>
    <p class="text-sm text-blue-600 mt-1">役割の説明</p>
  </div>
  <div class="py-1"><i data-lucide="arrow-down" class="w-6 h-6 text-gv-dim"></i></div>
  <div class="w-full max-w-lg bg-gradient-to-r from-purple-100 to-purple-200 border-2 border-purple-300 p-4 text-center">
    <div class="flex items-center justify-center gap-2">
      <i data-lucide="cpu" class="w-5 h-5 text-purple-600"></i>
      <span class="font-bold text-purple-800">中間レイヤー名</span>
    </div>
    <p class="text-sm text-purple-600 mt-1">役割の説明</p>
  </div>
  <div class="py-1"><i data-lucide="arrow-down" class="w-6 h-6 text-gv-dim"></i></div>
  <div class="w-full max-w-xl bg-gradient-to-r from-green-100 to-green-200 border-2 border-green-300 rounded-b-xl p-4 text-center">
    <div class="flex items-center justify-center gap-2">
      <i data-lucide="database" class="w-5 h-5 text-green-600"></i>
      <span class="font-bold text-green-800">下層レイヤー名</span>
    </div>
    <p class="text-sm text-green-600 mt-1">役割の説明</p>
  </div>
</div>
```

### シーケンス図（通信フロー）

```html
<div class="my-8 overflow-x-auto">
  <div class="flex justify-between min-w-[500px] mb-2 px-4">
    <div class="w-28 text-center">
      <div class="w-14 h-14 bg-blue-100 border-2 border-blue-300 rounded-full flex items-center justify-center mx-auto mb-1">
        <i data-lucide="monitor" class="w-6 h-6 text-blue-600"></i>
      </div>
      <span class="text-sm font-bold text-blue-800">アクター1</span>
    </div>
    <div class="w-28 text-center">
      <div class="w-14 h-14 bg-purple-100 border-2 border-purple-300 rounded-full flex items-center justify-center mx-auto mb-1">
        <i data-lucide="server" class="w-6 h-6 text-purple-600"></i>
      </div>
      <span class="text-sm font-bold text-purple-800">アクター2</span>
    </div>
    <div class="w-28 text-center">
      <div class="w-14 h-14 bg-green-100 border-2 border-green-300 rounded-full flex items-center justify-center mx-auto mb-1">
        <i data-lucide="database" class="w-6 h-6 text-green-600"></i>
      </div>
      <span class="text-sm font-bold text-green-800">アクター3</span>
    </div>
  </div>
  <div class="relative min-w-[500px] px-4">
    <div class="absolute left-[calc(14.3%)] top-0 bottom-0 border-l-2 border-dashed border-blue-200"></div>
    <div class="absolute left-[calc(50%)] top-0 bottom-0 border-l-2 border-dashed border-purple-200"></div>
    <div class="absolute left-[calc(85.7%)] top-0 bottom-0 border-l-2 border-dashed border-green-200"></div>
    <!-- リクエスト（実線 + arrow-right） -->
    <div class="relative py-3">
      <div class="ml-[14.3%] mr-[50%] flex items-center">
        <div class="flex-1 border-t-2 border-blue-400"></div>
        <i data-lucide="arrow-right" class="w-4 h-4 text-blue-500 -ml-1"></i>
      </div>
      <p class="text-xs text-blue-600 text-center font-medium mt-1">① リクエスト内容</p>
    </div>
    <!-- レスポンス（点線 + arrow-left） -->
    <div class="relative py-3">
      <div class="ml-[14.3%] mr-[50%] flex items-center flex-row-reverse">
        <div class="flex-1 border-t-2 border-dashed border-blue-400"></div>
        <i data-lucide="arrow-left" class="w-4 h-4 text-blue-500 -mr-1"></i>
      </div>
      <p class="text-xs text-blue-600 text-center font-medium mt-1">② レスポンス内容</p>
    </div>
  </div>
</div>
```

### テーブル関連図（ER Diagram 簡易版）

テーブル同士のリレーション（1対多・多対多）を視覚化する。DB設計、マイグレーション、モデルのリレーション解説に使用。

```html
<div class="bg-gray-50 rounded-2xl p-6 md:p-8 my-8">
  <div class="flex items-center gap-3 mb-6">
    <div class="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center">
      <i data-lucide="database" class="w-5 h-5 text-gv-primary"></i>
    </div>
    <div>
      <h3 class="text-lg font-bold text-gv-heading">テーブル関連図</h3>
      <p class="text-sm text-gv-muted">サブタイトル</p>
    </div>
  </div>

  <div class="flex flex-col md:flex-row items-center md:items-start justify-center gap-6 md:gap-4">
    <!-- テーブル A -->
    <div class="w-full max-w-[220px]">
      <div class="rounded-xl border-2 border-indigo-300 overflow-hidden shadow-sm">
        <div class="bg-indigo-100 px-4 py-2 font-bold text-gv-heading text-sm flex items-center gap-2">
          <i data-lucide="table-2" class="w-4 h-4"></i>
          users
        </div>
        <div class="bg-white divide-y divide-gray-100 text-sm">
          <div class="px-4 py-1.5 flex items-center gap-2">
            <span class="text-amber-500 text-xs font-bold">PK</span>
            <span class="font-mono">id</span>
          </div>
          <div class="px-4 py-1.5 font-mono">name</div>
          <div class="px-4 py-1.5 flex items-center gap-2">
            <span class="text-blue-500 text-xs font-bold">FK</span>
            <span class="font-mono">company_id</span>
          </div>
        </div>
      </div>
    </div>

    <!-- リレーション線 -->
    <div class="flex flex-col items-center justify-center py-2 md:py-8">
      <i data-lucide="arrow-down" class="w-6 h-6 text-gv-dim md:hidden"></i>
      <div class="hidden md:flex items-center gap-1">
        <span class="text-xs font-bold text-gv-muted">N</span>
        <div class="w-12 border-t-2 border-dashed border-gv-dim"></div>
        <span class="text-xs font-bold text-gv-muted">1</span>
      </div>
      <span class="text-xs text-gv-muted mt-1">belongs to</span>
    </div>

    <!-- テーブル B -->
    <div class="w-full max-w-[220px]">
      <div class="rounded-xl border-2 border-purple-300 overflow-hidden shadow-sm">
        <div class="bg-purple-100 px-4 py-2 font-bold text-gv-heading text-sm flex items-center gap-2">
          <i data-lucide="table-2" class="w-4 h-4"></i>
          companies
        </div>
        <div class="bg-white divide-y divide-gray-100 text-sm">
          <div class="px-4 py-1.5 flex items-center gap-2">
            <span class="text-amber-500 text-xs font-bold">PK</span>
            <span class="font-mono">id</span>
          </div>
          <div class="px-4 py-1.5 font-mono">name</div>
        </div>
      </div>
    </div>
  </div>

  <!-- 多対多の場合: 中間テーブルを中央に配置 -->
  <!--
  <div class="flex flex-col md:flex-row items-center md:items-start justify-center gap-6 md:gap-4 mt-8">
    テーブルA — N:N線 — 中間テーブル — N:N線 — テーブルB
    中間テーブルのヘッダー色は bg-amber-100 / border-amber-300 を使う
  </div>
  -->
</div>
```

**テーブルヘッダーの色ルール:**

| テーブル種別 | ヘッダー背景 | ボーダー | 用途 |
|------------|------------|---------|------|
| メインテーブル | `bg-indigo-100` | `border-indigo-300` | 説明の主対象 |
| 関連テーブル | `bg-purple-100` | `border-purple-300` | リレーション先 |
| 中間テーブル（多対多） | `bg-amber-100` | `border-amber-300` | 多対多の結合テーブル |

**カラムバッジ:**

| バッジ | 色 | 意味 |
|-------|-----|------|
| `PK` | `text-amber-500` | 主キー |
| `FK` | `text-blue-500` | 外部キー |
| `UQ` | `text-green-500` | ユニーク制約 |

**リレーション表記:**

| 表記 | 意味 |
|------|------|
| `1 ── N` | 1対多（実線） |
| `N ┄┄ N` | 多対多（破線、中間テーブル経由） |
| `1 ── 1` | 1対1（実線） |

### アノテーション付きコード

コードの各部分に色分けハイライトを付け、下に注釈リストで対応を示す。

```html
<div class="my-8">
  <div class="bg-gv-code rounded-xl overflow-hidden">
    <div class="p-4 font-mono text-sm leading-loose">
      <div class="flex items-start gap-0">
        <span class="text-indigo-200">const response = await </span>
        <span class="bg-yellow-500/20 text-yellow-300 px-1 rounded border border-yellow-500/30">fetch</span>
        <span class="text-indigo-200">(url);</span>
      </div>
      <div class="flex items-start gap-0">
        <span class="text-indigo-200">const data = await response.</span>
        <span class="bg-green-500/20 text-green-300 px-1 rounded border border-green-500/30">json</span>
        <span class="text-indigo-200">();</span>
      </div>
    </div>
  </div>
  <div class="mt-3 space-y-2">
    <div class="flex items-start gap-2">
      <span class="inline-block w-3 h-3 mt-1 bg-yellow-400 rounded-sm flex-shrink-0"></span>
      <p class="text-sm text-gv-text"><strong>fetch(url)</strong> — やさしい言葉での説明</p>
    </div>
    <div class="flex items-start gap-2">
      <span class="inline-block w-3 h-3 mt-1 bg-green-400 rounded-sm flex-shrink-0"></span>
      <p class="text-sm text-gv-text"><strong>.json()</strong> — やさしい言葉での説明</p>
    </div>
  </div>
</div>
```

### ツリー図（ディレクトリ・階層）

```html
<div class="bg-white rounded-xl border border-gv-border p-6 my-8 font-mono text-sm">
  <div class="flex items-center gap-2 mb-4">
    <i data-lucide="folder-tree" class="w-5 h-5 text-gv-primary"></i>
    <span class="font-bold text-gv-heading font-sans">ディレクトリ構造</span>
  </div>
  <div class="text-gv-text">
    <div class="flex items-center gap-1">
      <i data-lucide="folder" class="w-4 h-4 text-amber-500"></i>
      <span class="font-bold">ルート/</span>
    </div>
    <div class="ml-6 border-l-2 border-gray-200 pl-4 mt-1 space-y-1">
      <div class="flex items-center gap-1">
        <i data-lucide="folder" class="w-4 h-4 text-amber-500"></i>
        <span class="font-bold">サブディレクトリ/</span>
        <span class="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-sans ml-2">役割ラベル</span>
      </div>
      <div class="ml-6 border-l-2 border-gray-200 pl-4 space-y-1">
        <div class="flex items-center gap-1">
          <i data-lucide="file-code" class="w-4 h-4 text-blue-500"></i>
          <span>ファイル名.ext</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

### タイムライン（時系列・ライフサイクル）

```html
<div class="my-8 px-4">
  <div class="relative">
    <div class="absolute left-5 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-400 via-purple-400 to-green-400"></div>
    <div class="relative flex items-start gap-4 pb-8">
      <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0 z-10 shadow-md">
        <i data-lucide="play" class="w-5 h-5 text-white"></i>
      </div>
      <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 flex-1">
        <div class="font-bold text-blue-800">イベント名</div>
        <p class="text-sm text-gv-text mt-1">説明文</p>
      </div>
    </div>
    <div class="relative flex items-start gap-4 pb-8">
      <div class="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center flex-shrink-0 z-10 shadow-md">
        <i data-lucide="eye" class="w-5 h-5 text-white"></i>
      </div>
      <div class="bg-purple-50 border border-purple-200 rounded-xl p-4 flex-1">
        <div class="font-bold text-purple-800">イベント名</div>
        <p class="text-sm text-gv-text mt-1">説明文</p>
      </div>
    </div>
    <div class="relative flex items-start gap-4">
      <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0 z-10 shadow-md">
        <i data-lucide="check-circle" class="w-5 h-5 text-white"></i>
      </div>
      <div class="bg-green-50 border border-green-200 rounded-xl p-4 flex-1">
        <div class="font-bold text-green-800">イベント名</div>
        <p class="text-sm text-gv-text mt-1">説明文</p>
      </div>
    </div>
  </div>
</div>
```

### サイクル図（循環フロー）

```html
<div class="my-8 flex justify-center">
  <div class="relative w-72 h-72">
    <div class="absolute inset-0 flex items-center justify-center">
      <div class="bg-white rounded-full w-20 h-20 flex items-center justify-center shadow-md border-2 border-gv-border">
        <span class="text-sm font-bold text-gv-heading text-center leading-tight">中央<br>ラベル</span>
      </div>
    </div>
    <div class="absolute top-0 left-1/2 -translate-x-1/2 text-center">
      <div class="w-16 h-16 bg-red-100 border-2 border-red-300 rounded-full flex items-center justify-center mx-auto">
        <i data-lucide="x-circle" class="w-7 h-7 text-red-500"></i>
      </div>
      <span class="text-xs font-bold text-red-700 mt-1 block">ステップ1</span>
    </div>
    <div class="absolute bottom-4 right-0 text-center">
      <div class="w-16 h-16 bg-green-100 border-2 border-green-300 rounded-full flex items-center justify-center mx-auto">
        <i data-lucide="check-circle" class="w-7 h-7 text-green-500"></i>
      </div>
      <span class="text-xs font-bold text-green-700 mt-1 block">ステップ2</span>
    </div>
    <div class="absolute bottom-4 left-0 text-center">
      <div class="w-16 h-16 bg-blue-100 border-2 border-blue-300 rounded-full flex items-center justify-center mx-auto">
        <i data-lucide="sparkles" class="w-7 h-7 text-blue-500"></i>
      </div>
      <span class="text-xs font-bold text-blue-700 mt-1 block">ステップ3</span>
    </div>
    <div class="absolute top-16 right-8"><i data-lucide="arrow-right" class="w-5 h-5 text-gv-dim rotate-[135deg]"></i></div>
    <div class="absolute bottom-12 right-1/3"><i data-lucide="arrow-right" class="w-5 h-5 text-gv-dim rotate-[225deg]"></i></div>
    <div class="absolute top-16 left-8"><i data-lucide="arrow-right" class="w-5 h-5 text-gv-dim rotate-[315deg]"></i></div>
  </div>
</div>
```

### 入れ子ボックス図（スコープ・包含関係）

```html
<div class="my-8">
  <div class="bg-blue-50 border-2 border-blue-300 rounded-xl p-5">
    <div class="flex items-center gap-2 mb-3">
      <i data-lucide="box" class="w-5 h-5 text-blue-500"></i>
      <span class="font-bold text-blue-800 text-sm">外側のスコープ</span>
    </div>
    <div class="bg-purple-50 border-2 border-purple-300 rounded-xl p-5 ml-2">
      <div class="flex items-center gap-2 mb-3">
        <i data-lucide="box" class="w-5 h-5 text-purple-500"></i>
        <span class="font-bold text-purple-800 text-sm">中間のスコープ</span>
      </div>
      <div class="bg-green-50 border-2 border-green-300 rounded-xl p-4 ml-2">
        <div class="flex items-center gap-2 mb-2">
          <i data-lucide="box" class="w-5 h-5 text-green-500"></i>
          <span class="font-bold text-green-800 text-sm">内側のスコープ</span>
        </div>
        <p class="text-sm text-gv-text">この中だけで有効な内容</p>
      </div>
    </div>
  </div>
</div>
```

### 比較マトリクス（多項目比較表）

```html
<div class="my-8 overflow-x-auto">
  <table class="w-full text-sm border-collapse">
    <thead>
      <tr>
        <th class="bg-gradient-to-r from-gv-primary to-gv-secondary text-white p-3 rounded-tl-xl text-left">比較項目</th>
        <th class="bg-gradient-to-r from-gv-primary to-gv-secondary text-white p-3 text-center">選択肢A</th>
        <th class="bg-gradient-to-r from-gv-primary to-gv-secondary text-white p-3 text-center">選択肢B</th>
        <th class="bg-gradient-to-r from-gv-primary to-gv-secondary text-white p-3 rounded-tr-xl text-center">選択肢C</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gv-border">
      <tr>
        <td class="p-3 font-medium text-gv-heading bg-gray-50">基準1</td>
        <td class="p-3 text-center"><span class="bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-xs font-bold">高い</span></td>
        <td class="p-3 text-center"><span class="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-xs font-bold">低い</span></td>
        <td class="p-3 text-center"><span class="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-xs font-bold">低い</span></td>
      </tr>
      <tr>
        <td class="p-3 font-medium text-gv-heading bg-gray-50">基準2</td>
        <td class="p-3 text-center"><i data-lucide="x-circle" class="w-5 h-5 text-gv-negative inline-block"></i></td>
        <td class="p-3 text-center"><i data-lucide="check-circle" class="w-5 h-5 text-gv-positive inline-block"></i></td>
        <td class="p-3 text-center"><i data-lucide="check-circle" class="w-5 h-5 text-gv-positive inline-block"></i></td>
      </tr>
    </tbody>
  </table>
</div>
```

### 画面UIモック（ブラウザ）

実際のシステム画面やブラウザの見た目を再現する。ログイン画面、ダッシュボード等の説明に使用。

```html
<div class="my-8">
  <div class="bg-gray-100 rounded-xl overflow-hidden border border-gray-300 shadow-sm">
    <!-- ブラウザバー -->
    <div class="bg-gray-200 px-4 py-2 flex items-center gap-2">
      <div class="flex gap-1.5">
        <div class="w-3 h-3 bg-red-400 rounded-full"></div>
        <div class="w-3 h-3 bg-yellow-400 rounded-full"></div>
        <div class="w-3 h-3 bg-green-400 rounded-full"></div>
      </div>
      <div class="flex-1 bg-white rounded-md px-3 py-1 text-xs text-gray-500 ml-2">
        https://example.com/login
      </div>
    </div>
    <!-- 画面コンテンツ -->
    <div class="bg-white p-8 text-center">
      <div class="max-w-xs mx-auto space-y-4">
        <h3 class="text-lg font-bold text-gray-800">ログイン</h3>
        <div class="bg-gray-50 border border-gray-200 rounded-lg px-4 py-2 text-left text-sm text-gray-400">メールアドレス</div>
        <div class="bg-gray-50 border border-gray-200 rounded-lg px-4 py-2 text-left text-sm text-gray-400">パスワード</div>
        <div class="bg-gv-primary text-white rounded-lg px-4 py-2 text-sm font-bold">ログイン</div>
      </div>
    </div>
  </div>
</div>
```

### ターミナルUIモック

コマンドラインの出力やターミナル操作を再現する。

```html
<div class="my-8">
  <div class="bg-gv-code rounded-xl overflow-hidden shadow-sm">
    <!-- ターミナルバー -->
    <div class="bg-gray-800 px-4 py-2 flex items-center gap-2">
      <div class="flex gap-1.5">
        <div class="w-3 h-3 bg-red-500 rounded-full"></div>
        <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
        <div class="w-3 h-3 bg-green-500 rounded-full"></div>
      </div>
      <span class="text-gray-400 text-xs ml-2">Terminal</span>
    </div>
    <!-- コマンド -->
    <div class="p-4 font-mono text-sm">
      <div class="text-green-400">$ コマンド</div>
      <div class="text-indigo-200 mt-1">出力結果</div>
    </div>
  </div>
</div>
```

---

## フローティング目次（デスクトップのみ）

画面右側に固定表示される目次。セクションへのジャンプリンクを提供する。1280px以下では非表示。

### CSS（base.html の `<style>` 内に追加）

```css
.toc {
  position: fixed;
  right: 2rem;
  top: 50%;
  transform: translateY(-50%);
  background: white;
  padding: 1rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  max-height: 80vh;
  overflow-y: auto;
  z-index: 50;
}
@media (max-width: 1280px) {
  .toc { display: none; }
}
.toc a {
  display: block;
  padding: 0.375rem 0.75rem;
  color: #6b7280;
  text-decoration: none;
  font-size: 0.875rem;
  border-radius: 0.375rem;
  transition: all 0.2s;
}
.toc a:hover {
  color: #4f46e5;
  background: #eef2ff;
}
```

### HTML（`</main>` の直後、`<footer>` の前に配置）

```html
<!-- 目次（デスクトップのみ） -->
<nav class="toc">
  <div class="text-sm font-bold text-gv-heading mb-2 px-2">目次</div>
  <a href="#intro">導入</a>
  <a href="#terms">用語解説</a>
  <a href="#three-things">まず覚える3つ</a>
  <!-- セクションに応じて追加 -->
  <a href="#summary">まとめ</a>
</nav>
```

各セクションカードに対応する `id` を付与すること:

```html
<div class="bg-white rounded-2xl shadow-sm border border-gv-border p-8 mb-8" id="intro">
```

---

## 図解パターンの使い分け

| 説明したい内容 | パターン |
|--------------|---------|
| 「Xとは何か」(定義) | アナロジー図: 身近なたとえの登場人物を配置し、矢印で関係を示す |
| 「Xはどう動くか」(プロセス) | ステップフロー（直線型）: 番号つき横並び（モバイルは縦） |
| 「条件AならX、条件BならY」(条件分岐) | 分岐フローチャート: 判定ノード（黄）→ YES/NO で分岐し、アクションノード（赤/青/緑）へ |
| 「XとYの違い」(比較) | 左右対比: 2カラムで並べ、✗/✓ や赤/緑で差を一目で伝える |
| 「X vs Y vs Z」(多項目比較) | 比較マトリクス: テーブル形式で複数基準×複数選択肢を一覧 |
| 「Xの具体例」(事例) | カードグリッド: 2列のカードにアイコン＋タイトル＋説明 |
| 「Xのすごさ」(数値) | 数字カード: 3カラムに大きな数字 |
| 「Xの階層構造」(レイヤー) | レイヤー図: 幅を変えた積み上げボックスで上下関係を視覚化 |
| 「XがYに送りYがZに返す」(通信) | シーケンス図: ライフライン＋矢印で時系列のやり取りを表現 |
| 「テーブルAとBは1対多」(DB設計) | テーブル関連図: テーブルボックス＋PK/FKバッジ＋リレーション線で関係を表現 |
| 「Xの中にYがありその中にZがある」(包含) | 入れ子ボックス図: ボーダー付きボックスの入れ子でスコープを表現 |
| 「Xのライフサイクル」(時系列) | タイムライン: 縦軸グラデーション線＋丸アイコンで時間経過を表現 |
| 「X→Y→Z→Xの繰り返し」(循環) | サイクル図: 円形配置＋矢印でループを表現 |
| 「Xのファイル配置」(構造) | ツリー図: border-l＋インデントで親子関係を表現 |
| コード例 | ターミナルUIモックアップ（赤黄緑ボタン＋プロンプト） |
| コードの各部分の意味 | アノテーション付きコード: 色分けハイライト＋注釈リストで対応を示す |
| 見たことがあるもの | 画面UIの再現（ブラウザ、エディタ、チャットUI等） |
