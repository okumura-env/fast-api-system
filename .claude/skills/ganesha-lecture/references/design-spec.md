# ビジュアルデザイン仕様書 — miyata-press

> Claude / LLM でページコンテンツを生成する際のレイアウト・カラー・タイポグラフィ参照仕様。
> コード内のインラインCSSと完全に対応する。

---

## 1. カラーパレット

### 1-1. ブランドカラー

| トークン | HEX | 用途 |
|---------|-----|------|
| Primary | `#4f46e5` | ボタン、グラデーション起点、ヘッダー |
| Primary Dark | `#312e81` | 見出しテキスト、コードブロック背景ボーダー |
| Secondary | `#7c3aed` | グラデーション終点、太字テキスト、引用ボーダー |
| Accent Indigo | `#6366f1` | リンク、タブアクティブ、追加ボタン |
| Accent Light | `#818cf8` | ホバーボーダー、リンクホバー、ナツキボーダー |

### 1-2. テキストカラー

| トークン | HEX | 用途 |
|---------|-----|------|
| Text Primary | `#374151` | 本文テキスト |
| Text Heading | `#312e81` | H1〜H4 見出し |
| Text Secondary | `#6b7280` | 補助テキスト、ボタンラベル |
| Text Tertiary | `#9ca3af` | キャプション、フッター |
| Text Code | `#c7d2fe` | コードブロック内テキスト |
| Text Slate | `#1e293b` | 吹き出し内テキスト、入力値 |
| Text Bold (dialogue) | `#7c3aed` | 吹き出し内の `**太字**` |
| Text Blockquote | `#4c1d95` | 引用ブロック内テキスト |
| Text White | `#ffffff` | ヘッダー上、テーブルヘッダー |
| Text White Muted | `rgba(255,255,255,0.7)` | ヘッダーサブタイトル |

### 1-3. 背景カラー

| トークン | 値 | 用途 |
|---------|-----|------|
| Page BG | `linear-gradient(135deg, #f0f4ff 0%, #f5f0ff 50%, #eef2ff 100%)` | 公開/管理者ページ全体 |
| Simulator BG | `#0a0e17` | A0シミュレーター |
| Card BG | `#ffffff` | カード、吹き出し、モーダル |
| Code BG | `#1e1b4b` | コードブロック、テキストエリア |
| Blockquote BG | `linear-gradient(135deg, #eef2ff 0%, #f5f3ff 100%)` | 引用ブロック |
| Header BG | `linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #6366f1 100%)` | ページヘッダー |
| Button BG | `linear-gradient(135deg, #4f46e5, #7c3aed)` | プライマリボタン |
| Table Header BG | `linear-gradient(135deg, #4f46e5, #6366f1)` | テーブルヘッダー行 |
| Hover Tint | `#eef2ff` | ドロップゾーンアクティブ等 |

### 1-4. ボーダーカラー

| トークン | HEX | 用途 |
|---------|-----|------|
| Border Default | `#e0e7ff` | カード、入力、テーブルセル |
| Border Light | `#e2e8f0` | 区切り線 |
| Border Dashed | `#c7d2fe` | 追加ボタン点線、ドロップゾーン |
| Border Focus | `#818cf8` | ホバー・フォーカス |
| Border Code | `#312e81` | コードブロック |
| Border Error | `#fecaca` | エラー状態 |
| Border Subtle | `#d1d5db` | 薄いボーダー |

### 1-5. キャラクターカラー

| キャラクター | ID | ボーダー | シャドウ（15%透過） |
|-------------|-----|---------|-------------------|
| ガネーシャ | `ganesha` | `#f59e0b` | `rgba(245,158,11,0.15)` |
| ナツキ | `natsuki` | `#818cf8` | `rgba(129,140,248,0.15)` |
| 夏希 | `natsuki` | `#FFB7C5` | `rgba(255,183,197,0.15)` |
| 岡田 | `okada` | `#6366f1` | `rgba(99,102,241,0.15)` |
| アンゼック | `anzekku` | `#6366f1` | `rgba(99,102,241,0.15)` |

### 1-6. セマンティックカラー

| 状態 | HEX | 用途 |
|------|-----|------|
| Success | `#10b981` / `#16a34a` | 保存完了、成功状態 |
| Error | `#dc2626` / `#ef4444` | エラー、削除ボタン |
| Warning | `#f59e0b` | 警告 |

---

## 2. タイポグラフィ

### 2-1. フォントファミリー

```css
/* テキスト */
font-family: "Noto Sans JP", "Hiragino Sans", sans-serif;

/* コード */
font-family: "JetBrains Mono", "Fira Code", monospace;
```

### 2-2. フォントスケール

| 要素 | サイズ | ウェイト | 行間 | 色 |
|------|-------|---------|------|-----|
| H1 | 28–32px | 800 | 1.4 | `#312e81` |
| H2 | 24px | 700 | 1.4 | `#312e81` |
| H3 | 20px | 700 | 1.4 | `#312e81` |
| H4 | 17px | 700 | 1.4 | `#312e81` |
| 本文 (p) | 15px | 400 | 1.85 | `#374151` |
| 吹き出しテキスト | 15px | 400 | 1.85 | `#1e293b` |
| テーブルセル | 13–14px | 400 | 1.6 | `#374151` |
| テーブルヘッダー | 13px | 700 | — | `#ffffff` |
| コードブロック | 13px | 400 | 1.7 | `#c7d2fe` |
| ボタン | 13px | 600 | — | `#ffffff` |
| ラベル | 12px | 700 | — | 文脈依存 |
| バッジ | 12px | 600 | — | 文脈依存 |
| キャプション | 11–13px | 400 | — | `#9ca3af` |
| フッター | 11px | 400 | — | `#9ca3af` |

---

## 3. レイアウト

### 3-1. コンテナ幅

| 用途 | max-width |
|------|-----------|
| 公開ページ（チャプター等） | **880px** |
| ホーム・グリッドセクション | 900px |
| コレクション一覧 | 700px |
| 管理者エディタ | 1400px |
| 管理者リスト | 880px |
| モーダル/ダイアログ | 460–540px |

### 3-2. ページコンテナ

```js
{
  maxWidth: 880,
  margin: "0 auto",
  padding: "32px 24px",
  fontFamily: '"Noto Sans JP", "Hiragino Sans", sans-serif',
  background: "linear-gradient(135deg, #f0f4ff 0%, #f5f0ff 50%, #eef2ff 100%)",
  minHeight: "100vh",
}
```

### 3-3. スペーシング

#### マージン

| 要素 | 上 | 下 |
|------|---|---|
| H2 | 40px | 16px |
| H3 | 32px | 12px |
| H4 | 28px | 10px |
| 段落 (p) | 12px | 12px |
| コードブロック | 16px | 16px |
| 画像 | 20px | 20px |
| 吹き出し行 | 24px | 24px |
| 引用ブロック | 24px | 24px |

#### パディング

| 要素 | 値 |
|------|-----|
| ページコンテナ | `32px 24px` |
| カード | `16px 20px` |
| ボタン（プライマリ） | `7px 20px` |
| 入力フィールド | `6px 12px` |
| コードブロック | `16px 20px` |
| 引用ブロック | `20px 24px` |
| テーブルセル（th/td） | `10px 14px` |
| 吹き出し | `14px 18px` |
| ヘッダー | `40px 20px` |
| フッター | `32px 20px` |

#### ギャップ (flex/grid)

| コンテキスト | 値 |
|-------------|-----|
| カードグリッド | 16px |
| ナビゲーション | 12px |
| アイコン＋テキスト | 12–16px |
| 吹き出し（アバター↔バブル） | 12px |

---

## 4. コンポーネント詳細

### 4-1. 吹き出し（対話バブル）

#### レイアウト構造

```
┌─ dialogue row (flex, gap:12px) ──────────────────┐
│                                                    │
│  ┌─────┐  ┌─ bubble ──────────────────────────┐  │
│  │avatar│◁─│ テキストテキストテキスト           │  │
│  │96×96 │  │ **太字は紫** で強調               │  │
│  └─────┘  └────────────────────────────────────┘  │
│                                                    │
└────────────────────────────────────────────────────┘
```

- **左配置キャラ（ガネーシャ等）**: `flexDirection: "row"`
- **右配置キャラ（ナツキ等）**: `flexDirection: "row-reverse"`

#### バブル本体

```js
{
  background: "#ffffff",
  border: `1px solid ${character.borderColor}`,
  borderRadius: 10,
  padding: "14px 18px",
  fontSize: 15,
  lineHeight: 1.85,
  color: "#1e293b",
  boxShadow: `0 1px 3px ${character.borderColor}25`,  // 15% opacity
}
```

#### 吹き出しの尻尾（三角形）

```
外側三角: 幅11px × 高さ9px（キャラクターボーダー色）
内側三角: 幅9px × 高さ7px（白 #ffffff）
位置: 上端から18px、バブル外側に-11px突出
```

#### アバター

| キャラクター | サイズ | ボーダー |
|-------------|-------|---------|
| ガネーシャ | 96×96px | `2px solid #f59e0b` |
| その他 | 80×80px | `2px solid ${borderColor}` |

- 形状: `borderRadius: "50%"` (正円)
- オブジェクトフィット: `cover`

#### 吹き出し内テキスト装飾

| 記法 | レンダリング |
|------|-------------|
| `**太字**` | `color: #7c3aed`, `fontWeight: 700` |

### 4-2. 引用ブロック（結論ボックス）

```js
{
  background: "linear-gradient(135deg, #eef2ff 0%, #f5f3ff 100%)",
  borderLeft: "none",
  border: "2px solid #7c3aed",
  borderRadius: 12,
  padding: "20px 24px",
  margin: "24px 0",
  fontSize: 15,
  lineHeight: 1.85,
  color: "#4c1d95",
}
```

### 4-3. コードブロック

```js
{
  background: "#1e1b4b",
  border: "1px solid #312e81",
  borderRadius: 8,
  padding: "16px 20px",
  fontFamily: '"JetBrains Mono", "Fira Code", monospace',
  fontSize: 13,
  lineHeight: 1.7,
  color: "#c7d2fe",
  overflowX: "auto",
  whiteSpace: "pre-wrap",
  wordBreak: "break-all",
}
```

### 4-4. テーブル

```js
// テーブル全体
{ width: "100%", borderCollapse: "collapse", margin: "16px 0", fontSize: 14 }

// ヘッダーセル (th)
{
  background: "linear-gradient(135deg, #4f46e5, #6366f1)",
  color: "#ffffff",
  padding: "10px 14px",
  border: "1px solid #c7d2fe",
  fontWeight: 700,
  fontSize: 13,
  textAlign: "left",
}

// データセル (td)
{
  background: "#ffffff",
  color: "#374151",
  padding: "10px 14px",
  border: "1px solid #e0e7ff",
  fontSize: 13,
  lineHeight: 1.6,
}
```

### 4-5. カード

```js
// 通常状態
{
  background: "#ffffff",
  border: "1px solid #e0e7ff",
  borderRadius: 10,
  padding: "16px 20px",
  boxShadow: "0 1px 3px rgba(99,102,241,0.08)",
  transition: "all 0.2s",
}

// ホバー
{
  borderColor: "#818cf8",
  boxShadow: "0 4px 12px rgba(99,102,241,0.12)",
  transform: "translateY(-1px)",
}
```

### 4-6. ボタン

#### プライマリ

```js
{
  background: "linear-gradient(135deg, #4f46e5, #7c3aed)",
  color: "#fff",
  border: "none",
  borderRadius: 6,
  padding: "7px 20px",
  fontSize: 13,
  fontWeight: 600,
  cursor: "pointer",
}
// disabled: opacity 0.5, cursor "default"
```

#### セカンダリ（削除等）

```js
{
  background: "none",
  border: "1px solid #e0e7ff",  // or #fecaca for delete
  borderRadius: 4,
  width: 26,
  height: 26,
  color: "#6b7280",  // or #ef4444 for delete
  fontSize: 13,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
}
```

### 4-7. 入力フィールド

```js
{
  border: "1px solid #e0e7ff",
  borderRadius: 6,
  padding: "6px 12px",
  fontSize: 14,
  fontFamily: '"Noto Sans JP", "Hiragino Sans", sans-serif',
  outline: "none",
  color: "#1e293b",
  background: "#ffffff",
}
```

### 4-8. 画像

```js
{
  maxWidth: "100%",
  height: "auto",
  borderRadius: 8,
  border: "1px solid #e0e7ff",
  display: "block",
  margin: "0 auto",
}

// キャプション
{
  textAlign: "center",
  fontSize: 13,
  color: "#9ca3af",
  marginTop: 6,
}
```

### 4-9. ヘッダー

```js
{
  background: "linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #6366f1 100%)",
  borderBottom: "1px solid #c7d2fe",
  padding: "40px 20px",
  textAlign: "center",
}

// H1
{ margin: 0, fontSize: 28, color: "#ffffff", fontWeight: 700, letterSpacing: 1 }

// サブタイトル
{ margin: "12px 0 0", fontSize: 13, color: "rgba(255,255,255,0.7)", maxWidth: 600 }
```

### 4-10. フッター

```js
{
  textAlign: "center",
  padding: "32px 20px",
  borderTop: "1px solid #e0e7ff",
  color: "#9ca3af",
  fontSize: 11,
}
```

### 4-11. フローティング目次（デスクトップのみ）

画面右側に固定表示される目次。1280px以下では非表示。

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

HTML（`</main>` の直後、`<footer>` の前に配置）:

```html
<nav class="toc">
  <div style="font-size:14px;font-weight:700;color:#312e81;margin-bottom:8px;padding:0 8px;">目次</div>
  <a href="#intro">導入</a>
  <a href="#section1">セクション1</a>
  <!-- セクションに応じて追加 -->
  <a href="#summary">まとめ</a>
</nav>
```

### 4-12. 戻るリンク

```js
{
  color: "#6366f1",
  textDecoration: "none",
  fontSize: 15,
  marginBottom: 24,
  display: "inline-block",
  padding: "6px 0",
}
```

---

## 5. シャドウ・深度

| レベル | 値 | 用途 |
|--------|-----|------|
| Subtle | `0 1px 3px rgba(99,102,241,0.08)` | カード通常、トップバー |
| Medium | `0 4px 12px rgba(99,102,241,0.12)` | カードホバー |
| Strong | `0 4px 16px rgba(99,102,241,0.15)` | 強調カードホバー |
| Deep | `0 8px 24px rgba(99,102,241,0.15)` | ドロップダウンメニュー |
| Modal | `0 20px 60px rgba(0,0,0,0.15)` | モーダルダイアログ |
| Character | `0 1px 3px ${borderColor}25` | 吹き出し（キャラ色の15%透過） |

---

## 6. トランジション

| 対象 | duration | property |
|------|----------|----------|
| カードホバー | 0.2s | all |
| ボタンホバー | 0.15s | all |
| タブ切替 | 0.15s | all |
| ドロップダウン | 0.2s | all |

---

## 7. グリッド・レスポンシブ

### レスポンシブ方式

メディアクエリは**不使用**。CSS Grid の `auto-fill` + `minmax` で暗黙的にレスポンシブ対応。

### グリッドパターン

| 用途 | grid-template-columns |
|------|----------------------|
| ホームカード | `repeat(auto-fill, minmax(380px, 1fr))` |
| 画像グリッド | `repeat(auto-fill, minmax(120px, 1fr))` |
| アバターグリッド | `repeat(auto-fill, minmax(90px, 1fr))` |
| エディタ2カラム | `1fr 1fr` |

---

## 8. Z-Index レイヤー

| レイヤー | z-index | 用途 |
|---------|---------|------|
| Sticky Header | 100 | トップバー |
| Dropdown/Menu | 50 | フローティングメニュー、追加メニュー |
| Overlay | — | モーダル背景 `rgba(0,0,0,0.4)` |

---

## 9. A0シミュレーター固有カラー

| 命令/領域 | HEX | 用途 |
|----------|-----|------|
| ADD | `#f87171` | 加算命令ブロック |
| CMP | `#fb923c` | 比較命令ブロック |
| JMP | `#facc15` | ジャンプ命令ブロック |
| LOAD | `#4ade80` | ロード命令ブロック |
| OUT | `#60a5fa` | 出力命令ブロック |
| HLT | `#c084fc` | 停止命令ブロック |
| FAIL | `#94a3b8` | 失敗状態 |
| UNUSED | `#334155` | 未使用メモリ |
| REF | `#2dd4bf` | 参照値 |
| INPUT | `#f472b6` | 入力メモリ |
| OUTPUT | `#fbbf24` | 出力メモリ |

---

## 10. Markdown記法とレンダリング対応表

コンテンツ内で使用可能な記法と、レンダリング結果の対応:

| Markdown記法 | レンダリング |
|-------------|-------------|
| `# H1` | 28–32px, 800weight, `#312e81` |
| `## H2` | 24px, 700weight, `#312e81`, 上40px |
| `### H3` | 20px, 700weight, `#312e81`, 上32px |
| `#### H4` | 17px, 700weight, `#312e81`, 上28px |
| `**太字**` | 本文中: そのまま太字 / 吹き出し中: `#7c3aed` 紫太字 |
| `` `code` `` | JetBrains Mono 13px, `#1e1b4b` 背景 |
| `> 引用` | 紫ボーダー引用ボックス |
| `---` | 水平線（区切り） |
| `🐘「セリフ」` | ガネーシャ吹き出し（左配置） |
| `👩‍💻「セリフ」` | ナツキ吹き出し（右配置） |
| `🐘2「セリフ」` | アバターバリアント#2で表示 |
| `\|表\|` | インディゴグラデーションヘッダーのテーブル |
| ` ```code``` ` | ダークテーマコードブロック |
| `![alt](url)` | 角丸8px、ボーダー付き画像 |
