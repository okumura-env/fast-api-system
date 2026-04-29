# 学習ロードマップ — FastAPIのエッセンスを一通り学ぶためのゴール設計

このドキュメントは「レシピ管理システムをどこまで作れば、FastAPIの主要トピックを一通り学んだと言えるか」を整理したものです。

**学習目的を優先するなら、Step 2（多対多 + 認証）までをゴールに設定するのがコスパ最強です。**

---

## 現状

- ✅ `tags` / `users` / `recipes` のCRUD（routers / schemas / cruds / models の4層構造）
- ✅ `ingredients` テーブル
- ✅ `recipe_tags` 中間テーブル（多対多）
- ❌ `recipe_ingredients` 中間テーブル（quantity付き多対多）
- ❌ 認証・認可（ログイン / JWT）
- ❌ レシピ検索・絞り込み
- ❌ 買い物リスト生成
- ❌ ダッシュボード統計

---

## 🎯 Step 1: リレーション編（マスト）

ここまでやらないと「半端」。CRUDだけでは触れられないSQLAlchemyとPydanticの本質的な使い方を学ぶ段階。

| やること | 学べるエッセンス |
|---|---|
| `ingredients` のCRUD | 既習の復習 |
| `recipe_tags` 中間テーブル（多対多・素朴版） | SQLAlchemyの `relationship(secondary=...)`、Pydanticのネストレスポンス |
| `recipe_ingredients`（**quantity付き** 多対多） | **Association Objectパターン** — 中間テーブルに属性がある場合の作法。Laravelの `belongsToMany()->withPivot('quantity')` に相当 |
| レシピ作成時にタグ・食材をまとめて登録 | リクエストスキーマのネスト、トランザクション |

### 🔑 ここでの気づき
「**Pydanticスキーマを登録用と取得用で分ける理由**」が腹落ちする段階。
レシピ取得時はタグ・食材が**ネストして返る**けど、登録時は**IDの配列で受ける**——この非対称性がFastAPI設計の肝。

---

## 🎯 Step 2: 認証編（**強く推奨**）

FastAPIの真骨頂である**依存性注入（Depends）**を体験する段階。ここをやらないとFastAPIらしさの半分を取りこぼす。

| やること | 学べるエッセンス |
|---|---|
| パスワードハッシュ化（`passlib` + bcrypt） | セキュリティの基本 |
| ログインAPI（JWT発行） | `OAuth2PasswordBearer`、トークン |
| `Depends(get_current_user)` | **依存性注入（DI）** ← FastAPI最大の特徴 |
| 「自分のレシピだけ編集・削除できる」認可 | DIを使った認可ガード |

### 🔑 ここでの気づき
LaravelでいうSanctumに相当するが、**FastAPIでは認証が `Depends` という汎用機構の応用**として実装される。
LaravelのService Container / Middlewareを統合したような体験が得られる。

---

## 🎯 Step 3: 応用編（やると面白いけど学習効率は下がる）

FastAPI固有の新規エッセンスは少なく、SQLの腕試しに近い段階。アプリとしての完成度を上げたいときの拡張枠。

| やること | 学べること |
|---|---|
| レシピ検索（タグ絞り込み・キーワード） | クエリパラメータ、動的WHERE |
| ページネーション | `limit`/`offset`、レスポンスメタ |
| 買い物リスト生成 | 複数レシピをまたぐ集計ロジック |
| ダッシュボード統計 | SQLAlchemyの `func.count()`, `group_by` |

---

## 推奨ゴール

**Step 2まで（多対多 + 認証）をゴールに設定する**のが学習目的に最も合致する。

理由：

1. FastAPIの**主要機能**（ルーター / Pydantic / 非同期DB / **DI** / 認証）を一通り経験できる
2. Laravel経験者にとって「**Laravelで当たり前にあるものをFastAPIではどう実装するか**」のマッピングが完成する
3. Step 3はFastAPI固有の学びより「SQL力」「設計力」の話になっていく

買い物リスト・ダッシュボードは **Step 2が終わってから「もっとアプリを育てたい」と思ったときの拡張枠** として残しておく形が綺麗。

---

## 次の一手

順当にいくなら **`recipe_tags` の多対多** が次のステップとして自然。
既存の `tag` / `recipe` をつなぐだけなので、新テーブル設計の負担が軽い。
