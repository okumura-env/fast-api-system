# 学習ロードマップ — FastAPIで「Laravelの一通り」を学ぶ

このドキュメントは、Laravel経験者が **Controller / Model / Request / ApiResource / UseCase / Service / Test** という観点をFastAPIで一周するための学習計画です。

---

## ✅ ここまで習得できたこと

| Laravel概念 | FastAPIでの実装 | 状態 |
|---|---|---|
| **Controller** | `routers/`（`APIRouter` でリソース分割） | ✅ 学習済み |
| **Model** | `models/`（SQLAlchemy） | ✅ 学習済み |
| **FormRequest** | `schemas/` の `Insert/Update`（`Field` 宣言的バリデーション） | ✅ 学習済み（※ `field_validator` / `model_validator` の高度版は未経験。必要になったときに） |
| **ApiResource** | `schemas/` のレスポンス用クラス + `from_attributes=True` | ✅ 学習済み |
| **多対多 + ピボット属性** | `recipe_ingredients`（Association Object パターン） | ✅ Laravel の `withPivot('quantity')` 相当 |
| **サービスコンテナ / DI** | `cruds/class_tag.py`（Repository クラス化）+ `deps/tag.py`（`Annotated[..., Depends(...)]`） | ✅ tag で1周完了。**他リソースに展開する必要なし**（パターンは同じ） |
| **UseCase** | `usecases/recipe/create.py` の `RecipeCreateUseCase`（複数テーブルINSERT＋トランザクション境界） | ✅ 学習済み（2026-05-01 時点）|
| **Test (Feature/Unit)** | `tests/conftest.py`（fixture）+ `pytest-asyncio` + `httpx.AsyncClient` + `app.dependency_overrides` | ✅ 学習済み（2026-05-01 完了）|

> ここまでで FastAPI の **入出力層（Controller / Schema）/ DB アクセス層（Model / Repository）/ ビジネスロジック層（UseCase）/ 品質保証（Test）** を一通り体験済み。残るは **Service 層の切り出し練習** のみ（題材は無理やり感あり）。

---

## 用語の方針 — UseCase と Service を厳密に分ける

このロードマップでは **クリーンアーキテクチャ厳密派** の定義で進めます:

| | 定義 | 単位 |
|---|---|---|
| **UseCase** | **「ユーザーがやりたいこと1個」** に対応するビジネスロジック | 1ユースケース = 1クラス（1メソッドが基本） |
| **Service** | **複数のUseCaseから呼ばれる部品** | 1テーマ = 1クラス（複数メソッド可） |

ディレクトリ構成（**1ファイル = 1クラス** で統一・**リソース単位でサブディレクトリ**）:

```
backend/
├── usecases/
│   └── recipe/
│       ├── __init__.py
│       ├── create.py       ← RecipeCreateUseCase
│       ├── update.py       ← RecipeUpdateUseCase（将来）
│       └── delete.py       ← RecipeDeleteUseCase（将来）
└── services/
    └── recipe_reference.py ← RecipeReferenceResolver（複数メソッド可）
```

> - 既存の `cruds/class_tag.py`（→ `TagRepository`）や `models/recipe.py`（→ `Recipe`）と同じく 1ファイル1クラス
> - `usecases/` 配下は **Laravel の `app/UseCases/Recipe/` 構造**に対応するサブディレクトリ方式
> - ディレクトリ名は **単数形**（既存の `models/recipe.py` などと一貫）

---

## 🎯 Step 1: UseCase 層 — `RecipeCreateUseCase` を作る

**Laravel 経験者にとって一番大事な学び。** レシピ作成は `recipes` + `recipe_tags` + `recipe_ingredients` の3テーブルへの INSERT をまとめて行うので、UseCase の練習材料として最適。

| やること | 学べるエッセンス |
|---|---|
| `usecases/recipe/create.py` を作り `RecipeCreateUseCase` クラスを定義（`usecases/recipe/__init__.py` も忘れずに） | 1ファイル1ユースケースの粒度 |
| `__init__` で `RecipeRepository` などの依存を受け取る | 多段DI（UseCase が Repository に依存） |
| `execute(input_schema)` メソッド1本を公開 | UseCase は **1クラス1メソッド** が基本 |
| `async with db_session.begin():` でトランザクション境界を切る | Laravel の `DB::transaction(...)` 相当 |
| `deps/recipe.py` に `get_recipe_create_usecase` を追加 | UseCase の DI プロバイダ |
| `routers/recipe.py` の作成エンドポイントを **Schema検証 → UseCase呼び出し → Resource返却** に痩せさせる | Skinny Controller 原則 |

### 🔑 Laravel との対応

| Laravel | FastAPI |
|---|---|
| `app/UseCases/Recipe/CreateRecipeUseCase.php` | `usecases/recipe/create.py` の `RecipeCreateUseCase` |
| `__construct(RecipeRepository $repo)` | `def __init__(self, repo: RecipeRepository)` |
| `public function execute(...)` | `async def execute(self, ...)` |
| `DB::transaction(fn () => ...)` | `async with db_session.begin():` |
| ファサード経由の自動解決 | `Depends(get_recipe_create_usecase)` |

### 🔑 ここでの気づき

ルーターから UseCase を呼ぶようになると、「**ビジネスロジックがどこに住んでいるか**」が一目でわかる。tag で作った Repository + DI の仕組みが **「UseCase を載せる土台だった」** ことが腹落ちする段階。

---

## 🎯 Step 2: Service 層 — `RecipeReferenceResolver` を作る

UseCase の中で「**他のUseCaseでも再利用しそうな部品**」を切り出す段階。

### お題: `RecipeReferenceResolver`

`tag_ids` / `ingredient_ids` から **実体を取り出して、存在しないIDがあれば 404 を投げる** ロジックを Service として切り出す。

将来 `RecipeUpdateUseCase` を作ったときに **そのまま再利用できる**ことが Service として成立する根拠。

| やること | 学べるエッセンス |
|---|---|
| `services/recipe_reference.py` を作り `RecipeReferenceResolver` クラスを定義 | 横断的な部品の置き場所 |
| `fetch_tags_or_404(ids: list[int]) -> list[Tag]` メソッド | 1テーマに複数メソッド |
| `fetch_ingredients_or_404(ids: list[int]) -> list[Ingredient]` メソッド | 同上 |
| `__init__` で `TagRepository` / `IngredientRepository` を受け取る | Service も DI で組む |
| `RecipeCreateUseCase` から `Resolver` を呼ぶように書き換え | UseCase が Service を使う構造 |
| `deps/recipe.py` に `get_recipe_reference_resolver` を追加 | Service の DI プロバイダ |

### 🔑 Laravel との対応

| Laravel | FastAPI |
|---|---|
| `app/Services/RecipeReferenceResolver.php` | `services/recipe_reference.py` の `RecipeReferenceResolver` |
| 複数の UseCase から呼ばれる前提 | 複数の UseCase の `__init__` で `Depends` 注入 |
| メソッド複数（`fetchTags`, `fetchIngredients`...） | クラス内メソッド複数OK |

### 🔑 ここでの気づき

UseCase（Create専用の塊）と Service（再利用される部品）の **粒度の違い** が手で分かる段階。
「これは1ユースケース固有か？それとも他から呼ばれるか？」で置き場所が決まる、という感覚が掴める。

> 💡 小さいアプリなので Service の題材を **無理やり捻出している側面** はあります。実務では「**最初は UseCase に直接書いて、再利用したくなった瞬間に Service に切り出す**」のが現実的な進め方です。学習目的としては「Service という器を1度作ってみる」ことに意味があります。

---

## ✅ Step 3: Test — pytest で書く（2026-05-01 完了）

学習ロードマップの **総仕上げ**。Step 1〜2 で作ったレイヤー分離が **「テストしやすさ」** という具体的なメリットに変わるのが体感できる。

### セットアップ

| やること | 学べるエッセンス |
|---|---|
| `pytest` + `pytest-asyncio` + `httpx` をインストール | 非同期テストランナー |
| `tests/conftest.py` に **テスト用 SQLite (in-memory) のセッション fixture** を作る | テスト独立性 |
| `app.dependency_overrides[get_dbsession] = test_session` で本番DBを差し替え | **DI の真価** — Laravel の `$this->mock()` を超える柔軟さ |

### 書くテストの種類（薄く広く1周）

| テストの種類 | お題例 | Laravel での対応 |
|---|---|---|
| **ルーターの統合テスト** | `httpx.AsyncClient` で `POST /recipes` を叩き、ステータスコード+レスポンスbody検証 | Feature Test |
| **UseCase の単体テスト** | `RecipeCreateUseCase` をテスト用DBで直接呼び、3テーブルにINSERTされているか検証 | Unit Test（メイン） |
| **Service の単体テスト** | `RecipeReferenceResolver.fetch_tags_or_404` で存在しないIDで 404 が出るか検証 | Unit Test（小粒） |
| **fixture でのテストデータ準備** | `@pytest.fixture` でユーザー・タグを事前に作っておく | Factory + RefreshDatabase |

### 🔑 Laravel との対応

| Laravel | FastAPI |
|---|---|
| `php artisan test` | `pytest` |
| `RefreshDatabase` トレイト | fixture で `Base.metadata.create_all` / `drop_all` |
| `$this->postJson('/api/recipes', [...])` | `await client.post('/recipes', json=...)` |
| `$this->mock(RecipeRepository::class)` | `app.dependency_overrides[get_xxx] = ...` |
| Factory | `@pytest.fixture` で Repository 経由のシード |

### 🔑 ここでの気づき

**`dependency_overrides` で本番DBを in-memory DB に差し替えられる**のは、tag で DI を仕込んだことの **ご褒美**。`Depends` で組んでなかったら差し替えできなかった、というのが手を動かして分かる。

---

## 🪤 Step 3 で踏んだ罠と学び（2026-05-01 実録）

実際にやってみて遭遇した問題と、その教訓。Python / FastAPI 周辺の「Laravel と違う」ポイントが集約されている。

### 罠①: `pytest.ini` の置き場所で挙動が劇的に変わる

- `backend/pytest.ini`: 正解。pytest が `backend/` を rootdir として認識する
- `backend/tests/pytest.ini`: NG。空ファイルでも置くと rootdir が `tests/` に変わり、`backend/pytest.ini` が読まれなくなる
- ファイルが無い: pytest はデフォルト動作で進むが、`sys.path` が思った場所にならない

**教訓**: pytest.ini は **「ここがソースルート」という pytest への目印**。中身が空でも `[pytest]` セクションヘッダーだけは書いておく。

### 罠②: `pythonpath = .` を書かないと `sys.path` が通らない

```ini
[pytest]
pythonpath = .
```

これがないと `from database import Base` のような **「`backend/` 配下のモジュールを参照する import」** が解決できない。conftest.py の import が真っ先に死ぬ。

**教訓**: pytest 7+ の `pythonpath` 設定は **rootdir を sys.path に明示的に追加する**もの。Python は実行場所で挙動が変わる言語なので、テストでもソースルートを宣言する必要がある。

### 罠③: SQLAlchemy 2.0 の async は `aiosqlite` + `greenlet` が必要

```bash
pip install "sqlalchemy[asyncio]"
```

これで両方インストールされる。`uvicorn main:app` は `create_async_engine()` の生成自体ではエラーにならず、**実際に session を使った瞬間**に初めて気づく落とし穴。

**教訓**: 非同期DBスタックは **「依存ライブラリの抜け」が遅延発火する**。`pip install` のドキュメントは extras 込みで読む。

### 罠④: `backend/__init__.py` がトップレベルにあると import 起点がズレる

`backend/__init__.py` を置くと Python が `backend` を **パッケージ**として扱い、pytest の `sys.path` 注入が「`backend` の親ディレクトリ」になる → `from database import Base` が解決できなくなる。

**教訓**: `backend/` は **CWD（ソースルート）として使う想定** なので、`__init__.py` は置かない。サブパッケージ（`models/__init__.py` など）には必要。「ソースルートには `__init__.py` を置かない」というのが Python の慣習。

### 罠⑤: in-memory SQLite は `StaticPool` が必須

```python
create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
```

`:memory:` は **接続ごとに別の DB** になるので、テーブル作成した接続とクエリ流す接続が違うと `no such table` エラー。

**教訓**: Laravel の `phpunit.xml` で `DB_CONNECTION=sqlite, DB_DATABASE=:memory:` だけで済んでいた裏側で、これと等価な処理が内部で行われていた。Python では明示する。

### 罠⑥: `@pytest.mark.asyncio` を忘れると strict モードで死ぬ

```
async def functions are not natively supported.
```

**教訓**: pytest-asyncio 1.0+ のデフォルトは strict モード。すべての async テスト・async fixture に明示的なデコレータが必要:
- テスト: `@pytest.mark.asyncio`
- fixture: `@pytest_asyncio.fixture`

### 罠⑦（最大の学び）: `dependency_overrides` を忘れたまま実行すると、本番DBに書き込まれる

```python
# これを忘れた状態でテスト実行すると…
app.dependency_overrides[get_dbsession] = override_get_dbsession
```

テストは `5 passed` で通る。**でも本番 DB の `tags` テーブルに「和食」が書き込まれている**。実際に再現確認済み:

```bash
$ sqlite3 backend/tagdb.sqlite "SELECT id, title, created_at FROM tags;"
1|和食|2026-05-01 14:47:03.170144   ← テスト由来の汚染
```

**教訓**:
- `Depends(get_dbsession)` で DI を仕込んでおく → 差し替え可能
- `client` fixture で `dependency_overrides` を**全テストに自動で適用** → 忘れない設計
- テスト assert は「期待値と実値の一致」しか見ない。**「どの DB を見ているか」は assert では検出できない**
- 「テストが通る = 正しい」ではない。**本番リソースに副作用を出さない仕組みは、コード設計（DI）+ fixture（自動 override）の両輪で守る**

---

## 推奨フロー

```
Step 1 (UseCase: RecipeCreateUseCase)
   ↓
Step 2 (Service: RecipeReferenceResolver) ← UseCase から切り出す形で
   ↓
Step 3 (Test) ← UseCase / Service / router をそれぞれ薄くテスト
```

**目安**: それぞれ 1リソース（`recipe`）×小さく1周 でOK。**深さより全レイヤーを一度ずつ触ることを優先**。

---

## 次の一手（2026-05-01 時点）

Step 1（UseCase）と Step 3（Test）が完了。残り選択肢:

| 選択 | 内容 | おすすめ度 |
|---|---|---|
| **A. `RecipeUpdateUseCase` を作る** | UseCase 第2弾。Create と比較して「更新ならではの分岐」を体験。テスト基盤がある状態で TDD 的に書ける | ⭐⭐⭐⭐ |
| **B. Service層 (Step 2)** | `RecipeReferenceResolver` を切り出す。題材は無理やり感あるが「器を1度作ってみる」価値はある | ⭐⭐⭐ |
| **C. Pydantic V2 警告の解消** | 既存 schema の `Field(..., example=...)` を `json_schema_extra={"example": ...}` に書き換え（15箇所程度） | ⭐⭐ |

A → C → B の順を推奨（テスト基盤を活かして UseCase を増やす → 警告掃除で気持ちよくなる → 必要を感じたら Service に戻る）。
