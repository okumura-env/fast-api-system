# 模範解答パターン

## 成功する図解の構造

```
1. ヘッダー（gv-primary → gv-secondary グラデーション背景）
   └─ タイトル（ガネーシャ口調） + サブタイトル

2. 結論ボックス（引用スタイル）
   └─ 核心を1文で

3. 導入（キャラクター対話）
   └─ ガネーシャ: 結論を宣言 + たとえ話で概要説明
   └─ ナツキ: 素朴な疑問

4. 図解ブロック
   └─ 結論・たとえ話を1枚の図で視覚化

5. 概念解説（対話 + 図解の交互繰り返し）
   └─ 【対話】ガネーシャが例え話で解説、ナツキがツッコミ
   └─ 【図解】例え話のビジュアル化
   └─ 【対話】深掘り、偉人エピソード
   └─ 【図解】技術詳細の図示（コード例、テーブル、UIモック）
   └─ ...繰り返し

6. まとめ（キャラクター対話）
   └─ ガネーシャ: 要点を整理
   └─ ナツキ: 「さすガネーシャや！✨」→ ツッコミで締め
   └─ ガネーシャ: 「はい、Oh, My God!! 🙏✨」（決めポーズ）

7. 目次（フローティング）
   └─ デスクトップのみ表示（右側固定）
   └─ 各セクションへのジャンプリンク
```

---

## ヘッダーの書き方

```html
<div class="bg-gradient-to-r from-gv-primary to-gv-secondary rounded-2xl p-8 mb-8 text-white">
  <h1 class="text-3xl md:text-4xl font-black leading-tight">変数ってなんやねん？📦</h1>
  <p class="mt-3 text-white/70 text-sm">ガネーシャ×ナツキの対話で学ぶ、プログラミングの基礎</p>
</div>
```

---

## 「まず覚える3つ」の書き方

```html
<div class="bg-white rounded-2xl shadow-sm border border-gv-border p-8 mb-8">
  <div class="flex items-center gap-3 mb-6">
    <div class="w-12 h-12 bg-gradient-to-br from-rose-500 to-pink-500 rounded-xl flex items-center justify-center">
      <i data-lucide="star" class="w-6 h-6 text-white"></i>
    </div>
    <div>
      <h2 class="text-2xl font-bold text-gv-heading">まず覚える3つ</h2>
      <p class="text-gv-muted">最初はこれだけでOK！</p>
    </div>
  </div>

  <div class="grid gap-4">
    <div class="flex items-start gap-4 p-4 bg-gradient-to-r from-red-50 to-red-100 rounded-xl border-l-4 border-red-500">
      <div class="w-10 h-10 bg-red-500 text-white rounded-full flex items-center justify-center font-bold text-lg flex-shrink-0">1</div>
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="font-bold text-lg text-gv-heading">ポイント名</span>
          <span class="bg-gradient-to-r from-red-600 to-red-500 text-white px-3 py-0.5 rounded-full text-xs font-bold">必須</span>
        </div>
        <p class="text-gv-text">説明文。</p>
      </div>
    </div>

    <div class="flex items-start gap-4 p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl border-l-4 border-blue-500">
      <div class="w-10 h-10 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold text-lg flex-shrink-0">2</div>
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="font-bold text-lg text-gv-heading">ポイント名</span>
          <span class="bg-gradient-to-r from-blue-600 to-blue-500 text-white px-3 py-0.5 rounded-full text-xs font-bold">推奨</span>
        </div>
        <p class="text-gv-text">説明文。</p>
      </div>
    </div>

    <div class="flex items-start gap-4 p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-xl border-l-4 border-green-500">
      <div class="w-10 h-10 bg-green-500 text-white rounded-full flex items-center justify-center font-bold text-lg flex-shrink-0">3</div>
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="font-bold text-lg text-gv-heading">ポイント名</span>
          <span class="bg-gradient-to-r from-gray-500 to-gray-400 text-white px-3 py-0.5 rounded-full text-xs font-bold">任意</span>
        </div>
        <p class="text-gv-text">説明文。</p>
      </div>
    </div>
  </div>
</div>
```

---

## たとえ話の展開パターン

### パターン1: 身近な場所

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

### パターン2: デジタルな体験

```html
<div class="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border border-blue-200 my-6">
  <div class="flex items-center gap-2 mb-3">
    <i data-lucide="smartphone" class="w-6 h-6 text-blue-600"></i>
    <span class="font-bold text-blue-800">たとえ話：スマホの権限ダイアログ</span>
  </div>
  <div class="space-y-3 text-gv-text">
    <p>スマホでアプリを使うとき、こんな画面を見たことありませんか？</p>
    <div class="bg-white p-4 rounded-lg border text-center my-3">
      「カメラへのアクセスを許可しますか？」<br>
      <span class="text-blue-600">[許可する]</span> / <span class="text-gray-500">[許可しない]</span>
    </div>
  </div>
</div>
```

---

## 図解パターンの展開

### レイヤー図（積み上げ構造）

アーキテクチャの階層関係（MVC、3層構成、ミドルウェアスタック等）を表現する。幅を段階的に広げることで「上層ほど薄く、下層ほど厚い」を視覚化。

```html
<div class="flex flex-col items-center gap-0 my-8">
  <!-- 最上層 -->
  <div class="w-full max-w-md bg-gradient-to-r from-blue-100 to-blue-200 border-2 border-blue-300 rounded-t-xl p-4 text-center">
    <div class="flex items-center justify-center gap-2">
      <i data-lucide="monitor" class="w-5 h-5 text-blue-600"></i>
      <span class="font-bold text-blue-800">Controller</span>
    </div>
    <p class="text-sm text-blue-600 mt-1">HTTPの受付だけ</p>
  </div>
  <!-- 矢印 -->
  <div class="py-1">
    <i data-lucide="arrow-down" class="w-6 h-6 text-gv-dim"></i>
  </div>
  <!-- 中間層 -->
  <div class="w-full max-w-lg bg-gradient-to-r from-purple-100 to-purple-200 border-2 border-purple-300 p-4 text-center">
    <div class="flex items-center justify-center gap-2">
      <i data-lucide="cpu" class="w-5 h-5 text-purple-600"></i>
      <span class="font-bold text-purple-800">UseCase</span>
    </div>
    <p class="text-sm text-purple-600 mt-1">ビジネスロジック・トランザクション管理</p>
  </div>
  <!-- 矢印 -->
  <div class="py-1">
    <i data-lucide="arrow-down" class="w-6 h-6 text-gv-dim"></i>
  </div>
  <!-- 最下層 -->
  <div class="w-full max-w-xl bg-gradient-to-r from-green-100 to-green-200 border-2 border-green-300 rounded-b-xl p-4 text-center">
    <div class="flex items-center justify-center gap-2">
      <i data-lucide="database" class="w-5 h-5 text-green-600"></i>
      <span class="font-bold text-green-800">Model</span>
    </div>
    <p class="text-sm text-green-600 mt-1">データアクセス・リレーション</p>
  </div>
</div>
```

### シーケンス図（やり取りの流れ）

複数のアクター間のリクエスト/レスポンスの時系列を表現する。SPA認証フロー、API通信などに最適。

```html
<div class="my-8 overflow-x-auto">
  <!-- アクター名 -->
  <div class="flex justify-between min-w-[500px] mb-2 px-4">
    <div class="w-28 text-center">
      <div class="w-14 h-14 bg-blue-100 border-2 border-blue-300 rounded-full flex items-center justify-center mx-auto mb-1">
        <i data-lucide="monitor" class="w-6 h-6 text-blue-600"></i>
      </div>
      <span class="text-sm font-bold text-blue-800">ブラウザ</span>
    </div>
    <div class="w-28 text-center">
      <div class="w-14 h-14 bg-purple-100 border-2 border-purple-300 rounded-full flex items-center justify-center mx-auto mb-1">
        <i data-lucide="server" class="w-6 h-6 text-purple-600"></i>
      </div>
      <span class="text-sm font-bold text-purple-800">APIサーバー</span>
    </div>
    <div class="w-28 text-center">
      <div class="w-14 h-14 bg-green-100 border-2 border-green-300 rounded-full flex items-center justify-center mx-auto mb-1">
        <i data-lucide="database" class="w-6 h-6 text-green-600"></i>
      </div>
      <span class="text-sm font-bold text-green-800">データベース</span>
    </div>
  </div>
  <!-- ライフライン + メッセージ -->
  <div class="relative min-w-[500px] px-4">
    <!-- 縦のライフライン（点線） -->
    <div class="absolute left-[calc(14.3%)] top-0 bottom-0 border-l-2 border-dashed border-blue-200"></div>
    <div class="absolute left-[calc(50%)] top-0 bottom-0 border-l-2 border-dashed border-purple-200"></div>
    <div class="absolute left-[calc(85.7%)] top-0 bottom-0 border-l-2 border-dashed border-green-200"></div>

    <!-- メッセージ1: リクエスト（→方向） -->
    <div class="relative py-3">
      <div class="ml-[14.3%] mr-[50%] flex items-center">
        <div class="flex-1 border-t-2 border-blue-400"></div>
        <i data-lucide="arrow-right" class="w-4 h-4 text-blue-500 -ml-1"></i>
      </div>
      <p class="text-xs text-blue-600 text-center font-medium mt-1">① POST /login</p>
    </div>

    <!-- メッセージ2: DB問い合わせ（→方向） -->
    <div class="relative py-3">
      <div class="ml-[50%] mr-[14.3%] flex items-center">
        <div class="flex-1 border-t-2 border-purple-400"></div>
        <i data-lucide="arrow-right" class="w-4 h-4 text-purple-500 -ml-1"></i>
      </div>
      <p class="text-xs text-purple-600 text-center font-medium mt-1">② SELECT * FROM users</p>
    </div>

    <!-- メッセージ3: DB応答（←方向、点線=レスポンス） -->
    <div class="relative py-3">
      <div class="ml-[50%] mr-[14.3%] flex items-center flex-row-reverse">
        <div class="flex-1 border-t-2 border-dashed border-green-400"></div>
        <i data-lucide="arrow-left" class="w-4 h-4 text-green-500 -mr-1"></i>
      </div>
      <p class="text-xs text-green-600 text-center font-medium mt-1">③ ユーザーデータ返却</p>
    </div>

    <!-- メッセージ4: レスポンス（←方向、点線） -->
    <div class="relative py-3">
      <div class="ml-[14.3%] mr-[50%] flex items-center flex-row-reverse">
        <div class="flex-1 border-t-2 border-dashed border-blue-400"></div>
        <i data-lucide="arrow-left" class="w-4 h-4 text-blue-500 -mr-1"></i>
      </div>
      <p class="text-xs text-blue-600 text-center font-medium mt-1">④ 200 OK + Set-Cookie</p>
    </div>
  </div>
</div>
```

### アノテーション付きコード図

コードブロックの特定部分に色分けされた注釈を紐づける。コード解説の質が大幅に向上する。

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
  <!-- 注釈リスト -->
  <div class="mt-3 space-y-2">
    <div class="flex items-start gap-2">
      <span class="inline-block w-3 h-3 mt-1 bg-yellow-400 rounded-sm flex-shrink-0"></span>
      <p class="text-sm text-gv-text"><strong>fetch(url)</strong> — サーバーにHTTPリクエストを送る関数。「お店に注文を出す」イメージ</p>
    </div>
    <div class="flex items-start gap-2">
      <span class="inline-block w-3 h-3 mt-1 bg-green-400 rounded-sm flex-shrink-0"></span>
      <p class="text-sm text-gv-text"><strong>.json()</strong> — レスポンスをJSONに変換する。「届いた荷物を開封する」イメージ</p>
    </div>
  </div>
</div>
```

### ツリー図（階層・入れ子構造）

ディレクトリ構造、DOMツリー、クラス継承など、親子関係のある階層を表現する。

```html
<div class="bg-white rounded-xl border border-gv-border p-6 my-8 font-mono text-sm">
  <div class="flex items-center gap-2 mb-4">
    <i data-lucide="folder-tree" class="w-5 h-5 text-gv-primary"></i>
    <span class="font-bold text-gv-heading font-sans">ディレクトリ構造</span>
  </div>
  <div class="text-gv-text">
    <div class="flex items-center gap-1">
      <i data-lucide="folder" class="w-4 h-4 text-amber-500"></i>
      <span class="font-bold">app/</span>
    </div>
    <div class="ml-6 border-l-2 border-gray-200 pl-4 mt-1 space-y-1">
      <div class="flex items-center gap-1">
        <i data-lucide="folder" class="w-4 h-4 text-amber-500"></i>
        <span class="font-bold">Http/Controllers/</span>
        <span class="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-sans ml-2">HTTPの受付</span>
      </div>
      <div class="ml-6 border-l-2 border-gray-200 pl-4 space-y-1">
        <div class="flex items-center gap-1">
          <i data-lucide="file-code" class="w-4 h-4 text-blue-500"></i>
          <span>UserController.php</span>
        </div>
      </div>
      <div class="flex items-center gap-1">
        <i data-lucide="folder" class="w-4 h-4 text-amber-500"></i>
        <span class="font-bold">UseCases/</span>
        <span class="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full font-sans ml-2">ビジネスロジック</span>
      </div>
      <div class="flex items-center gap-1">
        <i data-lucide="folder" class="w-4 h-4 text-amber-500"></i>
        <span class="font-bold">Models/</span>
        <span class="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-sans ml-2">データ</span>
      </div>
    </div>
  </div>
</div>
```

### タイムライン（時系列図）

ライフサイクル、HTTPリクエストの流れなど「時間軸に沿った変化」を表現する。縦軸にグラデーション線を引き、各イベントを丸アイコンで配置。

```html
<div class="my-8 px-4">
  <div class="relative">
    <!-- 縦の軸線 -->
    <div class="absolute left-5 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-400 via-purple-400 to-green-400"></div>

    <!-- イベント1 -->
    <div class="relative flex items-start gap-4 pb-8">
      <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0 z-10 shadow-md">
        <i data-lucide="play" class="w-5 h-5 text-white"></i>
      </div>
      <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 flex-1">
        <div class="font-bold text-blue-800">setup()</div>
        <p class="text-sm text-gv-text mt-1">コンポーネント作成前。リアクティブデータを定義する。</p>
      </div>
    </div>

    <!-- イベント2 -->
    <div class="relative flex items-start gap-4 pb-8">
      <div class="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center flex-shrink-0 z-10 shadow-md">
        <i data-lucide="eye" class="w-5 h-5 text-white"></i>
      </div>
      <div class="bg-purple-50 border border-purple-200 rounded-xl p-4 flex-1">
        <div class="font-bold text-purple-800">onMounted()</div>
        <p class="text-sm text-gv-text mt-1">DOMが描画された直後。API呼び出しはここで。</p>
      </div>
    </div>

    <!-- イベント3 -->
    <div class="relative flex items-start gap-4">
      <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0 z-10 shadow-md">
        <i data-lucide="refresh-cw" class="w-5 h-5 text-white"></i>
      </div>
      <div class="bg-green-50 border border-green-200 rounded-xl p-4 flex-1">
        <div class="font-bold text-green-800">onUpdated()</div>
        <p class="text-sm text-gv-text mt-1">リアクティブデータが変更され、DOMが再描画された後。</p>
      </div>
    </div>
  </div>
</div>
```

### サイクル図（循環フロー）

TDDサイクル、リアクティブ更新ループなど「始点に戻る循環」を表現する。

```html
<div class="my-8 flex justify-center">
  <div class="relative w-72 h-72">
    <!-- 中央ラベル -->
    <div class="absolute inset-0 flex items-center justify-center">
      <div class="bg-white rounded-full w-20 h-20 flex items-center justify-center shadow-md border-2 border-gv-border">
        <span class="text-sm font-bold text-gv-heading text-center leading-tight">TDD<br>サイクル</span>
      </div>
    </div>
    <!-- 上（12時の位置） -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 text-center">
      <div class="w-16 h-16 bg-red-100 border-2 border-red-300 rounded-full flex items-center justify-center mx-auto">
        <i data-lucide="x-circle" class="w-7 h-7 text-red-500"></i>
      </div>
      <span class="text-xs font-bold text-red-700 mt-1 block">Red</span>
    </div>
    <!-- 右下（4時の位置） -->
    <div class="absolute bottom-4 right-0 text-center">
      <div class="w-16 h-16 bg-green-100 border-2 border-green-300 rounded-full flex items-center justify-center mx-auto">
        <i data-lucide="check-circle" class="w-7 h-7 text-green-500"></i>
      </div>
      <span class="text-xs font-bold text-green-700 mt-1 block">Green</span>
    </div>
    <!-- 左下（8時の位置） -->
    <div class="absolute bottom-4 left-0 text-center">
      <div class="w-16 h-16 bg-blue-100 border-2 border-blue-300 rounded-full flex items-center justify-center mx-auto">
        <i data-lucide="sparkles" class="w-7 h-7 text-blue-500"></i>
      </div>
      <span class="text-xs font-bold text-blue-700 mt-1 block">Refactor</span>
    </div>
    <!-- 矢印 -->
    <div class="absolute top-16 right-8">
      <i data-lucide="arrow-right" class="w-5 h-5 text-gv-dim rotate-[135deg]"></i>
    </div>
    <div class="absolute bottom-12 right-1/3">
      <i data-lucide="arrow-right" class="w-5 h-5 text-gv-dim rotate-[225deg]"></i>
    </div>
    <div class="absolute top-16 left-8">
      <i data-lucide="arrow-right" class="w-5 h-5 text-gv-dim rotate-[315deg]"></i>
    </div>
  </div>
</div>
```

### 入れ子ボックス図（スコープ/コンテキスト）

クロージャのスコープ、ミドルウェアの包含関係、try-catchのネストなど「何が何に包まれているか」を表現する。

```html
<div class="my-8">
  <div class="bg-blue-50 border-2 border-blue-300 rounded-xl p-5">
    <div class="flex items-center gap-2 mb-3">
      <i data-lucide="box" class="w-5 h-5 text-blue-500"></i>
      <span class="font-bold text-blue-800 text-sm">グローバルスコープ</span>
    </div>
    <div class="bg-purple-50 border-2 border-purple-300 rounded-xl p-5 ml-2">
      <div class="flex items-center gap-2 mb-3">
        <i data-lucide="box" class="w-5 h-5 text-purple-500"></i>
        <span class="font-bold text-purple-800 text-sm">関数スコープ</span>
      </div>
      <div class="bg-green-50 border-2 border-green-300 rounded-xl p-4 ml-2">
        <div class="flex items-center gap-2 mb-2">
          <i data-lucide="box" class="w-5 h-5 text-green-500"></i>
          <span class="font-bold text-green-800 text-sm">ブロックスコープ（if / for）</span>
        </div>
        <p class="text-sm text-gv-text">ここで宣言した <code class="bg-green-200 px-1 rounded">let</code> はこの中だけで有効</p>
      </div>
      <p class="text-sm text-gv-text mt-3">関数内の変数はここからアクセスできる</p>
    </div>
    <p class="text-sm text-gv-text mt-3">グローバル変数はどこからでもアクセスできる</p>
  </div>
</div>
```

### 比較マトリクス（多項目比較表）

3つ以上の選択肢を複数の基準で比較する。技術選定の説明などに最適。

```html
<div class="my-8 overflow-x-auto">
  <table class="w-full text-sm border-collapse">
    <thead>
      <tr>
        <th class="bg-gradient-to-r from-gv-primary to-gv-secondary text-white p-3 rounded-tl-xl text-left">比較項目</th>
        <th class="bg-gradient-to-r from-gv-primary to-gv-secondary text-white p-3 text-center">Vuex</th>
        <th class="bg-gradient-to-r from-gv-primary to-gv-secondary text-white p-3 text-center">Pinia</th>
        <th class="bg-gradient-to-r from-gv-primary to-gv-secondary text-white p-3 rounded-tr-xl text-center">Composable</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gv-border">
      <tr>
        <td class="p-3 font-medium text-gv-heading bg-gray-50">学習コスト</td>
        <td class="p-3 text-center"><span class="bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-xs font-bold">高い</span></td>
        <td class="p-3 text-center"><span class="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-xs font-bold">低い</span></td>
        <td class="p-3 text-center"><span class="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-xs font-bold">低い</span></td>
      </tr>
      <tr>
        <td class="p-3 font-medium text-gv-heading bg-gray-50">TypeScript</td>
        <td class="p-3 text-center"><i data-lucide="x-circle" class="w-5 h-5 text-gv-negative inline-block"></i></td>
        <td class="p-3 text-center"><i data-lucide="check-circle" class="w-5 h-5 text-gv-positive inline-block"></i></td>
        <td class="p-3 text-center"><i data-lucide="check-circle" class="w-5 h-5 text-gv-positive inline-block"></i></td>
      </tr>
      <tr>
        <td class="p-3 font-medium text-gv-heading bg-gray-50">DevTools</td>
        <td class="p-3 text-center"><i data-lucide="check-circle" class="w-5 h-5 text-gv-positive inline-block"></i></td>
        <td class="p-3 text-center"><i data-lucide="check-circle" class="w-5 h-5 text-gv-positive inline-block"></i></td>
        <td class="p-3 text-center"><i data-lucide="x-circle" class="w-5 h-5 text-gv-negative inline-block"></i></td>
      </tr>
    </tbody>
  </table>
</div>
```

---

## 品質チェックリスト

作成後、以下を確認：

### 必須

- [ ] 全ての技術用語に用語解説がある
- [ ] たとえ話が3つ以上ある
- [ ] 導入・中間・まとめにキャラクター対話がある
- [ ] 「まず覚える3つ」のような絞り込みがある
- [ ] コード例の前に「このコードがやること」がある
- [ ] 結論ボックスが冒頭にある
- [ ] 最後は「はい、Oh, My God!! 🙏✨」（決めポーズ）

### デザイン

- [ ] Lucide icon を使用
- [ ] gv カラーシステムが適用されている
- [ ] アバター画像のパスが正しい（`images/` ディレクトリ）
- [ ] スマホでも読みやすい（レスポンシブ）
- [ ] 対話と図解が交互に配置されている（対話だけで3往復以上続いていない）

### 対話

- [ ] 1吹き出し最大150文字
- [ ] 同じキャラの連続発言は3回以内
- [ ] ガネーシャの関西弁が一貫している
- [ ] 偉人エピソードが1つ以上ある
- [ ] ナツキのツッコミが少なくとも1つある
- [ ] 「さすガネーシャや！✨」→ ナツキのツッコミで締め
