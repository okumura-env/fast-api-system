# FastAPI ↔ Laravel 比較ガイド

このドキュメントは **Laravel 経験者がレシピ管理システム（FastAPI + SQLAlchemy）を一通り実装した経験** をもとに、Laravel と FastAPI で「どこが同じで・どこが違うか」を整理した参照ドキュメントです。

> 関連ドキュメント:
> - [`docs/learning-roadmap.md`](./learning-roadmap.md) — 学習を進めた順序の記録
> - [`docs/next-plan.md`](./next-plan.md) — Service 完成 + deps 整理 + 本ドキュメント作成までの作業計画
> - [`docs/system-overview.md`](./system-overview.md) — システム全体のテーブル構成・画面一覧

---

## 0. 一望表（先に全体感）

| 観点 | Laravel | FastAPI（このプロジェクトでの実装） |
|---|---|---|
| **言語** | PHP（同期） | Python（**async/await 全面**） |
| **ルーティング** | `routes/api.php` + Controller | `APIRouter(prefix=..., tags=[...])` をリソース単位で分割 |
| **モデル定義** | Eloquent（規約ベース） | SQLAlchemy（明示的・コードファースト） |
| **バリデーション** | `FormRequest` クラス | Pydantic Schema（型ヒント駆動）|
| **DB アクセス** | Eloquent ORM が万能 | **層を分ける必要**（cruds 関数 / Repository クラス） |
| **DI（依存性注入）** | サービスコンテナが型ヒントから自動解決 | `Depends()` で **配線を手書き** |
| **DI 配線の置き場所** | `app/Providers/AppServiceProvider.php` の `bind()` | `deps/` ディレクトリ（自分で配置を決める）|
| **トランザクション** | `DB::transaction(fn () => ...)` | `async with db_session.begin():` |
| **テスト時の差し替え** | `$this->mock(Class::class)` | `app.dependency_overrides[provider] = ...` |
| **モデル ⇄ レスポンス** | `ApiResource` | Pydantic Schema + `from_attributes=True` |
| **多対多 + ピボット属性** | `withPivot('quantity')` | Association Object パターン（中間モデルを明示）|
| **ファイル/ディレクトリ命名** | フレームワーク規約で半固定 | **自分で決める**（命名のブレが起きやすい）|
| **API ドキュメント** | 別途 Scribe / L5-Swagger 等を入れる | **標準で `/docs` に Swagger UI** が自動生成 |

---

## 1. DI（依存性注入）— 一番大きな違い

### Laravel: サービスコンテナが自動解決

```php
// Controller
class RecipeCreateController {
    public function __construct(
        private RecipeService $service,  // ← 型を書くだけで自動注入
    ) {}
}
```

`AppServiceProvider::register()` で bind しておけば、**型ヒントだけ** で勝手に解決される。

### FastAPI: 配線を全部手書き

```python
# deps/usecases/recipe.py
def get_recipe_create_usecase(
    db_session: AsyncSession = Depends(get_dbsession),
    service: RecipeService = Depends(get_recipe_service),
) -> RecipeCreateUseCase:
    return RecipeCreateUseCase(db_session, service)
```

Laravel が**裏で勝手にやってる "解決の連鎖"** を、FastAPI では `Depends()` で 1 段ずつ書く。

### 多段 DI の流れ

このプロジェクトでは **router → UseCase → Service → DB** の 4 段の DI が組まれている:

```
ルーター（routers/recipe.py）
  usecase: RecipeCreateUseCaseDep
       ↓ FastAPI が解決
DI プロバイダ（deps/usecases/recipe.py）
  get_recipe_create_usecase(
      db_session = Depends(get_dbsession),     ← FastAPI が解決
      service = Depends(get_recipe_service),   ← FastAPI が解決
  )
       ↓ ここで完成済みオブジェクトが渡される
UseCase の __init__（usecases/recipe/create.py）
  def __init__(self, db_session, service):     ← 普通の Python の世界
      self.db_session = db_session
      self.service = service
```

→ **`deps/` までが FastAPI の世界、UseCase の `__init__` から先は普通の Python**。この境界線を意識すると、型ヒントの書き方が決まる。

### `Annotated` と `Depends` の正体

エイリアスではない。**Python 標準の `Annotated`（型に付箋を貼る）** と **FastAPI が定義した `Depends()` クラス**を組み合わせて使う:

```python
RecipeServiceDep = Annotated[RecipeService, Depends(get_recipe_service)]
#                            ^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                            ① 型情報       ② FastAPI への "作り方" 指示
```

- `Annotated` は **Python 自体は何もしない**。ただ追加情報を持ち運ぶだけ
- `Depends(...)` は **FastAPI が見たときだけ意味を持つ**

→ つまり「FastAPI 経由で値を解決する場面（router 引数 / DI プロバイダ引数）」**でしか効かない**。普通のクラスの `__init__` 引数では `Depends(...)` 部分は **誰も見ない死文**になる。

### 「層の依存方向」の罠

Phase 1 で実際に踏んだ罠:

```python
# 間違い：UseCase が deps を import している（逆流）
# usecases/recipe/create.py
from deps.usecases.recipe import RecipeServiceDep   # ❌

class RecipeCreateUseCase:
    def __init__(self, db_session, service: RecipeServiceDep):  # ❌
```

これは **Laravel で言えば「Controller の `__construct` に AppServiceProvider を import する」** くらい変。配線（deps）はロジック層（usecase）の上位に位置する責務なので、**逆流させない**。

正しい書き方:

```python
# usecases/recipe/create.py
from services.recipe import RecipeService   # ✅ 型だけ知っていればいい

class RecipeCreateUseCase:
    def __init__(self, db_session, service: RecipeService):  # ✅
```

**健全な依存方向**:

```
   router         ← FastAPI に近い
     ↓ (deps を import する)
   deps           ← 配線層
     ↓ (usecase / service / repository を import する)
   usecase / service / repository  ← ロジック層
     ↓ (model / db を import する)
   models / database               ← データ層
```

「上から下への一方通行」を守る。1 箇所許すと **循環 import + 層の責務崩壊** が始まる。

---

## 2. 層の責務分担

Laravel は **Service が万能** になりがちで、Controller / Service / Model だけで済ませることも多い。
FastAPI でクリーンに作るなら **5 層** を意識する:

| 層 | 役割 | このプロジェクトの該当 |
|---|---|---|
| **routers** | HTTP の入出力。Schema 検証 → UseCase 呼び出し → Resource 返却 | `backend/routers/` |
| **schemas** | リクエスト/レスポンスのバリデーション + 型定義 | `backend/schemas/` |
| **usecases** | 「ユーザーがやりたいこと 1 個」に対応するビジネスロジック。1 ユースケース = 1 クラス | `backend/usecases/recipe/` |
| **services** | 複数 UseCase から呼ばれる **再利用部品** | `backend/services/recipe.py` |
| **cruds / repositories** | DB 操作（関数群 or Repository クラス） | `backend/cruds/` |
| **models** | SQLAlchemy のテーブル定義 | `backend/models/` |

### UseCase と Service の使い分け

| | 定義 | 単位 |
|---|---|---|
| **UseCase** | 「ユーザーがやりたいこと 1 個」に対応 | 1 ユースケース = 1 クラス（メソッドは `execute` 1 本が基本）|
| **Service** | 複数 UseCase から呼ばれる部品 | 1 テーマ = 1 クラス（複数メソッド可）|

> 💡 実務では「最初は UseCase に直接書いて、再利用したくなった瞬間に Service に切り出す」が現実的。
> このプロジェクトでは `RecipeCreateUseCase` と `RecipeUpdateUseCase` の両方が `service.fetch_tags_or_404` `service.fetch_ingredients_or_404` を呼ぶ形で **Service の存在意義が出た**。

### Laravel との対応

| Laravel | FastAPI |
|---|---|
| `app/Http/Controllers/Api/RecipeController.php` | `routers/recipe.py` |
| `app/Http/Requests/StoreRecipeRequest.php` | `schemas/recipe.py` の `InsertAndUpdateRecipeSchema` |
| `app/UseCases/Recipe/CreateRecipeUseCase.php` | `usecases/recipe/create.py` の `RecipeCreateUseCase` |
| `app/Services/RecipeService.php` | `services/recipe.py` の `RecipeService` |
| `app/Repositories/TagRepository.php` | `cruds/class_tag.py` の `TagRepository`（※命名の揺れ — 第 8 章参照）|
| `app/Models/Recipe.php` | `models/recipe.py` の `Recipe` |
| `app/Http/Resources/RecipeResource.php` | `schemas/recipe.py` の `RecipeSchema` + `from_attributes=True` |
| `app/Providers/AppServiceProvider.php` | `deps/usecases/`, `deps/services/`, `deps/repositories/` の DI プロバイダ群 |

---

## 3. バリデーション

### Laravel: FormRequest クラス

```php
class StoreRecipeRequest extends FormRequest {
    public function rules() {
        return [
            'title' => 'required|string|min:1',
            'servings' => 'required|integer',
            'tag_ids' => 'array',
            'tag_ids.*' => 'integer',
        ];
    }
}
```

文字列ベースのルール記述。

### FastAPI: Pydantic Schema（型ヒント駆動）

```python
class InsertAndUpdateRecipeSchema(BaseModel):
    user_id: int = Field(..., description="投稿者を一意に識別するID番号", example=1)
    title: str = Field(..., description="タイトル", example="カレー", min_length=1)
    servings: int = Field(..., description="何人前か", example=1)
    tag_ids: list[int] = []
    ingredients: list[RecipeIngredientInput] = []
```

**型ヒント自体がバリデーションルール**。`int` なら数値、`list[int]` なら整数のリスト、`min_length=1` なら 1 文字以上。

### 違いのポイント

| | Laravel | FastAPI |
|---|---|---|
| ルール記述 | 文字列（`'required\|string\|min:1'`）| 型ヒント + `Field()` 引数 |
| 型安全 | ルール文字列のミスタイプは実行時まで気づかない | エディタの型チェックで即発見 |
| エラーメッセージ | `messages()` メソッドでカスタム | デフォルトで詳細 JSON が返る |
| OpenAPI 連携 | 別途 Scribe 等が必要 | **自動的に `/docs` に反映** |

---

## 4. トランザクション境界

### Laravel

```php
DB::transaction(function () use ($recipe) {
    $recipe->save();
    $recipe->tags()->sync($tag_ids);
});
```

### FastAPI / SQLAlchemy

```python
async with self.db_session.begin():
    new_recipe = Recipe(...)
    new_recipe.tags = tags
    self.db_session.add(new_recipe)
```

**`async with`** ブロックを抜けたタイミングで自動コミット、例外なら自動ロールバック。Laravel のクロージャ版と概念は同じ。

---

## 5. テスト

### Laravel

```php
class RecipeTest extends TestCase {
    use RefreshDatabase;
    
    public function test_create_recipe() {
        $response = $this->postJson('/api/recipes', [...]);
        $response->assertStatus(200);
    }
    
    public function test_with_mock() {
        $this->mock(RecipeRepository::class, function ($mock) {
            $mock->shouldReceive('save')->once();
        });
    }
}
```

### FastAPI / pytest

```python
@pytest.fixture
async def client(test_db_session):
    app.dependency_overrides[get_dbsession] = lambda: test_db_session
    async with AsyncClient(app=app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_put_recipe_returns_404(client):
    response = await client.put("/recipes/999", json={...})
    assert response.status_code == 404
```

### 対応関係

| Laravel | FastAPI |
|---|---|
| `php artisan test` | `pytest` |
| `RefreshDatabase` トレイト | fixture で `Base.metadata.create_all` / `drop_all` |
| `$this->postJson('/api/recipes', [...])` | `await client.post('/recipes', json=...)` |
| `$this->mock(Class::class)` | `app.dependency_overrides[provider] = ...` |
| Factory | `@pytest.fixture` で Repository 経由のシード |
| `phpunit.xml` の `DB_CONNECTION=sqlite, DB_DATABASE=:memory:` | `create_async_engine("sqlite+aiosqlite:///:memory:", poolclass=StaticPool, ...)` |

### 「DI を仕込んでおく」ことの最大のご褒美

`app.dependency_overrides[get_dbsession] = test_session` で **本番 DB をテスト用 in-memory DB に差し替えられる**。
これは tag で Repository + DI を仕込んだことの真の価値で、**`Depends` で組んでなかったら差し替え不可能** だった。手を動かして体感した最大の収穫の 1 つ。

---

## 6. 非同期 IO

Laravel は基本同期。FastAPI は **async/await が全面に出る**:

| 場面 | Laravel | FastAPI |
|---|---|---|
| Controller / Router | `public function store(...)` | `async def create_recipe(...)` |
| DB セッション | `$user = User::find(1);` | `result = await db_session.execute(select(User).where(User.id == 1))` |
| HTTP クライアント（テスト含む）| `$this->getJson(...)` | `await client.get(...)` |
| トランザクション | `DB::transaction(fn () => ...)` | `async with db_session.begin():` |

→ **`await` を書き忘れた瞬間にコルーチンオブジェクトのまま値として扱おうとして謎のエラー** になる。Laravel と最も挙動が違うところで、慣れるまで踏みやすい。

---

## 7. ルーティング & API ドキュメント

### Laravel

```php
// routes/api.php
Route::apiResource('recipes', RecipeController::class);
```

### FastAPI

```python
# main.py
app.include_router(recipe_router)

# routers/recipe.py
router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/", response_model=RecipeSchema)
async def create_recipe(usecase: RecipeCreateUseCaseDep, recipe_data: InsertAndUpdateRecipeSchema):
    return await usecase.execute(recipe_data)
```

### 自動 API ドキュメント

FastAPI 標準で `http://localhost:8000/docs` に **Swagger UI** が出る:
- Pydantic Schema からスキーマ駆動で OpenAPI 仕様を自動生成
- 「Try it out」で curl 不要で API テスト
- リクエスト/レスポンス例も自動表示

→ Laravel は別途 Scribe / L5-Swagger を入れる必要がある。FastAPI の **入れた瞬間に動くドキュメント** はかなりの強み。

---

## 8. ファイル/ディレクトリ命名 — 自分で決める世界

### Laravel：規約があるから迷わない

- Controller は `app/Http/Controllers/`
- Model は `app/Models/`
- Service は `app/Services/`
- ファイル名 = クラス名（`RecipeService.php`）

### FastAPI：規約が無いので決め方を間違えると後で痛む

このプロジェクトで **実際に踏んだ命名の揺れ**:

| 揺れ | 状態 |
|---|---|
| `crud/` → `cruds/` にリネーム | 単複の選択。後から複数形に統一した |
| `cruds/class_tag.py` の中身が `TagRepository` | **概念は Repository なのに `cruds/` に同居**。命名と置き場所が乖離 |
| `deps/` がフラット → サブディレクトリ化 | UseCase / Service / Repository が混ざっていたのを `deps/usecases/` `deps/services/` `deps/repositories/` に分類した（Phase 2 で実施） |

→ Laravel が「フレームワークの規約」で隠してくれてた **「どこに何を置くか」の判断** が、FastAPI では全部自分の責任。設計判断の練習場としては良い反面、命名のブレが残りやすい。

### 残課題（Phase 2 終了時点）

- `cruds/class_tag.py` を `repositories/tag.py` にリネームすべきかどうか（次回検討）
- 関数型 CRUD（`cruds/tag.py` `cruds/recipe.py` ...）と Repository クラス（`cruds/class_tag.py`）が同じ `cruds/` に混在している不整合

---

## 9. モデル ⇄ レスポンス変換

### Laravel: ApiResource

```php
class RecipeResource extends JsonResource {
    public function toArray($request) {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'tags' => TagResource::collection($this->whenLoaded('tags')),
        ];
    }
}
```

### FastAPI: Pydantic Schema + `from_attributes=True`

```python
class RecipeSchema(InsertAndUpdateRecipeSchema):
    id: int = Field(..., description="レシピを一意に識別するID番号", example=123)
    tags: Optional[List[TagBase]] = None
    ingredients: Optional[List[IngredientBase]] = None
    model_config = {"from_attributes": True}   # ← SQLAlchemy オブジェクトから直接読み取る
```

`from_attributes=True` で **SQLAlchemy オブジェクトを Pydantic が読める**ようになる。Laravel の `whenLoaded` 相当の "ロード済みかどうかで分岐" を書かずに済む（リレーションが None なら `Optional[...] = None` で吸収）。

---

## 10. 多対多 + ピボット属性

### Laravel: `withPivot`

```php
class Recipe extends Model {
    public function ingredients() {
        return $this->belongsToMany(Ingredient::class)
                    ->withPivot('quantity');
    }
}
```

### FastAPI / SQLAlchemy: Association Object パターン

中間テーブルに **追加属性（quantity）** がある場合は、中間モデル `RecipeIngredient` を **明示的に定義** する:

```python
class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(Integer)
    
    recipe = relationship("Recipe", back_populates="recipe_ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")
```

そして `Recipe` モデル側:

```python
class Recipe(Base):
    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe")
```

UseCase 側:

```python
new_recipe.recipe_ingredients = [
    RecipeIngredient(ingredient_id=item.ingredient_id, quantity=item.quantity)
    for item in recipe_data.ingredients
]
```

→ Laravel の `withPivot` のような「シンタックスシュガー」は無いので、**中間モデルを 1 つのクラスとして書く**。代わりに、quantity のような追加属性を扱うコードが **明示的** になる。

---

## 11. Python ならではの落とし穴（実録）

このプロジェクトで **実際に踏んだ罠** の集約。Python / FastAPI / SQLAlchemy 周辺の "Laravel と違う" ポイント。

### 罠①: `pytest.ini` の置き場所で挙動が劇的に変わる

- `backend/pytest.ini`: 正解。pytest が `backend/` を rootdir として認識
- `backend/tests/pytest.ini`: NG。空ファイルでも置くと rootdir が `tests/` になる
- ファイルが無い: デフォルト動作で進むが、`sys.path` が思った場所にならない

→ 中身が空でも `[pytest]` セクションヘッダーだけは書いておく。

### 罠②: `pythonpath = .` を書かないと `sys.path` が通らない

```ini
[pytest]
pythonpath = .
```

これがないと `from database import Base` のような **`backend/` 配下のモジュール参照** が解決できない。

### 罠③: SQLAlchemy 2.0 の async は `aiosqlite` + `greenlet` が必要

```bash
pip install "sqlalchemy[asyncio]"
```

`uvicorn main:app` は `create_async_engine()` の生成自体ではエラーにならず、**実際に session を使った瞬間** に初めて気づく落とし穴。

### 罠④: `backend/__init__.py` がトップレベルにあると import 起点がズレる

`backend/` は **CWD（ソースルート）として使う想定** なので、`__init__.py` は置かない。サブパッケージ（`models/__init__.py` など）には必要。

### 罠⑤: in-memory SQLite は `StaticPool` が必須

```python
create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
```

`:memory:` は **接続ごとに別の DB** になるので、テーブル作成した接続とクエリ流す接続が違うと `no such table`。

### 罠⑥: `@pytest.mark.asyncio` を忘れると strict モードで死ぬ

pytest-asyncio 1.0+ のデフォルトは strict。すべての async テスト・async fixture に明示的なデコレータが必要:
- テスト: `@pytest.mark.asyncio`
- fixture: `@pytest_asyncio.fixture`

### 罠⑦（最大の学び）: `dependency_overrides` を忘れると本番 DB に書き込まれる

```python
# これを忘れた状態でテスト実行すると…
app.dependency_overrides[get_dbsession] = override_get_dbsession
```

テストは `5 passed` で通る。**でも本番 DB の `tags` テーブルに「和食」が書き込まれている**。
教訓: **テストが通る = 正しい、ではない**。本番リソースに副作用を出さない仕組みは「コード設計（DI）+ fixture（自動 override）」の両輪で守る。

### 罠⑧: `__init__` 引数を `self.xxx = xxx` で明示代入しないと使えない

```python
class RecipeUpdateUseCase:
    def __init__(self, db_session, service: RecipeService):
        self.db_session = db_session
        # self.service = service ← これを忘れると AttributeError
```

→ PHP 8 の「コンストラクタプロパティ昇格」(`public function __construct(private RecipeService $service)`)は Python に **無い**。1 行 1 行明示的に代入する。

### 罠⑨: 引数の順序ルール — デフォルト値あり/なしの混在は SyntaxError

```python
def get_recipe_create_usecase(
    db_session: AsyncSession = Depends(get_dbsession),  # デフォルト値あり
    service: RecipeServiceDep,                          # デフォルト値なし → SyntaxError
):
```

Python は「デフォルト値ありの引数の **後ろに** デフォルト値なしの引数を置けない」。

### 罠⑩: 関数定義の順序が意味を持つ

```python
# ❌ NG: get_recipe_service が定義される前に Depends(get_recipe_service) を書いている
def get_recipe_create_usecase(
    service = Depends(get_recipe_service),  # ← NameError
): ...

def get_recipe_service(): ...
```

関数の **本体** は呼ばれるまで評価されないが、関数の **デフォルト値** は **関数定義の瞬間に評価される**。だから「使われる側を先に定義」する順番が必要。

### 罠⑪: `Annotated[..., Depends(...)]` は使う場所を間違えると無意味な飾り

```python
class RecipeCreateUseCase:
    def __init__(self, db_session, service: RecipeServiceDep):  # ❌ 飾り
```

`Depends(...)` は FastAPI が見たときだけ意味を持つ。**普通のクラスの `__init__` では誰も見ない**ので、ただの `RecipeService` で書くのが正しい。

### 罠⑫: `Optional[...]` の import 漏れは `from __future__ import annotations` で隠れる

`-> Optional[Recipe]` と書いてあるのに `from typing import Optional` が無い。**`from __future__ import annotations` が型ヒントを文字列扱いにしてくれるので実行時には気づかない**。型ヒントが本当に評価される場面（mypy / runtime introspection）で初めて発覚する。

### 罠⑬: import パスの "住所変更" は機械的だが網羅必須

ファイルを移動するたびに、それを参照している全ての import 文を新パスに書き換える必要がある（Phase 2 で実施）。Laravel は autoload が解決してくれるので意識する場面が少ない。

```bash
# 移動前に必ず影響範囲を確認
grep -rn "from deps\.recipe import" backend/
```

### 罠⑭: `__init__.py` でサブパッケージを宣言する

ディレクトリを **パッケージ** として認識させるには `__init__.py` が必要（中身は空でも OK）。Python 3.3+ の名前空間パッケージで省略できるが、**置かないと挙動がブレる** ので慣習として置く。

---

## 12. このプロジェクトで身についた「気づき」リスト

実装を通じて言語化できた気づき:

1. **DI は配線 = 手書きの「サービスコンテナの中身」**。Laravel が裏でやってる仕事を自分で書く感覚
2. **`Annotated` と `Depends` は "型 + 取り出し方" の付箋付き型** であって、エイリアスではない
3. **層の依存方向は上から下への一方通行**。逆流させると循環 import + 責務崩壊
4. **Service の存在意義は「複数 UseCase から呼ばれる部品」になった瞬間** に出る。1 ヶ所だけ呼ばれる Service は UseCase に直接書けばいい
5. **副作用目的の関数呼び出し**（戻り値を捨てて例外だけ期待する）は普通のパターン。`fetch_ingredients_or_404` は存在チェックだけが目的
6. **Pydantic の型ヒントは実行時には強制されない**ので、`return` 漏れや戻り値型ミスマッチは実行時には気づかない（mypy が必要）
7. **`dependency_overrides` の存在自体が「DI で書いておくこと」へのご褒美**。Depends を仕込んでなければテスト分離もできなかった
8. **Python はモジュール = 上から実行されるスクリプト**。だから定義順、import パス、`__init__.py` の有無で挙動がブレる
9. **API ドキュメント（/docs）が標準で動く**。スキーマファースト設計と相性がいい

---

## 13. 残課題

このプロジェクトで未解決 or 後回しにした項目:

| 項目 | 内容 |
|---|---|
| **Pydantic V2 Deprecated 警告** | `Field(..., example=...)` を `json_schema_extra={"example": ...}` に書き換え（15 箇所程度）|
| **`cruds/class_tag.py` の命名整理** | 中身が `TagRepository` クラスなので `repositories/tag.py` にリネームするか、既存の関数型 CRUD と統合方針を決める |
| **frontend ⇄ backend の連携テスト** | フロントエンド側はまだ初期テンプレート状態 |
| **他リソースの UseCase 化** | 現状 `RecipeCreateUseCase` / `RecipeUpdateUseCase` のみ。`RecipeDeleteUseCase` や User/Tag 系の UseCase 化は未着手 |
| **Repository パターンの他リソース展開** | 現状 `TagRepository` のみクラス化。他は関数型 CRUD のまま（実務的には必要に応じて）|
| **`field_validator` / `model_validator` の体験** | 宣言的バリデーション（`min_length` 等）以外の高度なバリデーション未経験 |
| **マイグレーション** | 現状 `Base.metadata.create_all` で雑に作っている。Alembic の体験はまだ |

---

## まとめ — Laravel 経験者が FastAPI に来て一番違ったこと

**「フレームワークが裏でやってくれてた仕事を、自分の責任で書く」**

具体的には:
1. DI 配線（`deps/`）
2. ディレクトリ命名と置き場所
3. import パスの管理
4. async/await の境界
5. テスト時の依存差し替え

これらを **手書きする代わりに、プロジェクト構造の自由度が高い** のが FastAPI の世界。
逆に Laravel は「規約に従っている限り迷わない」のが強み。**どちらも一長一短** で、適材適所。

このプロジェクトを通じて Laravel の規約を「**裏で何を肩代わりしてくれてたか**」の視点で見直せたのは、FastAPI 学習の最大の副産物。
