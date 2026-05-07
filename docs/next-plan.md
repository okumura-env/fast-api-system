# 次の作業計画 — Service 完成 + deps 整理 + Laravel 比較振り返り

このドキュメントは `docs/learning-roadmap.md` の **Step 2（Service 層）以降の実行計画**。
Service が中途半端に止まっている状態から、3 Phase で締めて学習ロードマップを完走する。

---

## 全体の流れ

| Phase | 内容 | 主な変更ファイル | 完了基準 |
|---|---|---|---|
| **Phase 1** | Service クラスの完成と全体接続 | `services/recipe.py`<br>`deps/recipe.py`<br>`usecases/recipe/update.py` | Create も Update も Service 経由 + pytest 緑 |
| **Phase 2** | `deps/` を usecase / repository / service に分類 | `deps/` 配下を再編 + routers の import 更新 | 起動 OK + pytest 緑 |
| **Phase 3** | FastAPI ↔ Laravel 総まとめドキュメント作成 | `docs/fastapi-vs-laravel.md`（新規）or `learning-roadmap.md` 末尾追記 | 主要観点が一望できる表が完成 |

---

## Phase 1: Service クラスの完成と全体接続

### 出発点（着手前の状態）

- `services/recipe.py` の `RecipeService` が **未完成** で import するだけで死ぬ
  - `select` の import 漏れ → `NameError`
  - `fetch_ingredients_or_404` に `return` 漏れ → 暗黙の `None` を返す
- `usecases/recipe/create.py` は **Service を受け取る 2 引数版に変更済み**
- 一方 `deps/recipe.py` は **1 引数のまま `RecipeCreateUseCase(db_session)` を組み立てている** → 起動して `POST /recipes` を叩いた瞬間 `TypeError: missing 1 required positional argument: 'service'`
- `usecases/recipe/update.py` は **直書きの `select(Tag)` を残していて Service を使っていない** → Service の "再利用される部品" としての存在意義がまだ出ていない

### Step 1-1: `services/recipe.py` を完成させる

| やること | ヒント |
|---|---|
| `select` を import | `from sqlalchemy import select`（`cruds/recipe.py` や `usecases/recipe/update.py` を参考）|
| `fetch_ingredients_or_404` の末尾に `return ingredients` を追加 | タグ側 `fetch_tags_or_404` と同じ閉じ方 |

**実行確認:**
```bash
cd backend
python -c "from services.recipe import RecipeService; print(RecipeService)"
```
→ `<class 'services.recipe.RecipeService'>` が表示されれば OK

> 📚 **Laravel 対応:** `select` は Eloquent の `Tag::query()` や `DB::table('tags')->select(...)` に相当する **クエリビルダの起点**。Laravel と違い SQLAlchemy 2.0 では関数として **明示的に import** して使う。
> Python は型ヒント（`-> list[Ingredient]`）が **実行時には強制されない** ので、return 漏れは静的解析（mypy 等）以外では検出できない。

### Step 1-2: `deps/recipe.py` で Service の DI プロバイダを足し、UseCase に注入する

| やること | Laravel 対応 |
|---|---|
| `get_recipe_service` プロバイダ追加（`db_session` を受け取って `RecipeService` を返す）| サービスコンテナの `bind` |
| 型エイリアス `RecipeServiceDep = Annotated[RecipeService, Depends(get_recipe_service)]` を追加 | - |
| `get_recipe_create_usecase` に **`service: RecipeServiceDep` を引数追加** し、`RecipeCreateUseCase(db_session, service)` で組み立てる | 多段 DI: Container → UseCase → Service → DB |
| `get_recipe_update_usecase` も同様に Service を受け取る形に変更（1-3 で UseCase 側を直すための準備）| 同上 |

**実行確認:**
```bash
cd backend
uvicorn main:app --reload
```
→ 起動エラーが出ないこと（このタイミングではまだ Update 側が Service を受け取らないので、起動チェックだけ）

### Step 1-3: `RecipeUpdateUseCase` も Service 経由に書き換える

| やること | 学びポイント |
|---|---|
| `__init__` を `(self, db_session, service: RecipeService)` に変更 | UseCase が複数の依存を受け取る形 |
| `select(Tag).where(Tag.id.in_(...))` の直書き部分を `service.fetch_tags_or_404(...)` に置換 | **Service の再利用が初めて意味を持つ瞬間**（題材の無理やり感が消える） |
| `recipe_data.ingredients` から `ingredient_id` を抽出して `service.fetch_ingredients_or_404(...)` を呼ぶ | UseCase が "存在チェック" 責務を Service に委譲 |

> 📚 **Laravel 対応:** 1 つの Service クラスを `CreateUseCase` と `UpdateUseCase` の両方の `__construct` で受け取る形 = **サービスコンテナで bind された依存が複数 UseCase に注入される** イメージ。

### Step 1-4: 回帰確認（pytest + 手動起動）

```bash
cd backend
pytest -v
```
→ 全テスト緑

```bash
uvicorn main:app --reload
# 別ターミナルで
curl -X POST http://localhost:8000/recipes \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"title":"...","servings":2,"tag_ids":[1],"ingredients":[{"ingredient_id":1,"quantity":"100g"}]}'
```
→ 200 OK + `recipes` / `recipe_tags` / `recipe_ingredients` の 3 テーブルに INSERT されている

### Phase 1 完了基準（2026-05-07 達成）

- [✅] `services/recipe.py` の Service が完成し import で死なない
- [✅] `deps/recipe.py` で Service が UseCase に注入される **多段 DI** が組めている
- [✅] `RecipeCreateUseCase` と `RecipeUpdateUseCase` の **両方** が Service を経由して tag / ingredient を解決している
- [✅] pytest 全緑（6 passed）
- [✅] `uvicorn` 起動 + Service の存在チェックが効いて 404 が返ることを確認

---

## Phase 2: deps/ を usecase / repository / service に分類

### 現状（フラット）

```
backend/deps/
├── __init__.py
├── recipe.py      ← UseCase 系（RecipeCreateUseCaseDep / RecipeUpdateUseCaseDep）
└── tag.py         ← Repository 系（TagRepoDep）
```

→ Phase 1 完了時点で **Service 系も増える** ので 3 種類が同レイヤーに混ざる。意図を表現するためにサブディレクトリで分類する。

### 目標構成（**案 B: 複数形採用 — 外側の `usecases/` `services/` と一致**）

```
backend/deps/
├── __init__.py
├── repositories/
│   ├── __init__.py
│   └── tag.py             ← TagRepoDep
├── services/
│   ├── __init__.py
│   └── recipe.py          ← get_recipe_service プロバイダ（※ RecipeServiceDep は Phase 1 中に削除済み）
└── usecases/
    ├── __init__.py
    └── recipe.py          ← RecipeCreateUseCaseDep / RecipeUpdateUseCaseDep
```

### やること

| Step | 内容 |
|---|---|
| 2-1 | `deps/repositories/`, `deps/services/`, `deps/usecases/` を作成し、それぞれに空の `__init__.py` を置く |
| 2-2 | 現在の `deps/recipe.py` から **Service 系**（`get_recipe_service`）を `deps/services/recipe.py` に切り出し（UseCase が import する側なので先に確定させる）|
| 2-3 | 現在の `deps/recipe.py` から **UseCase 系**（`get_recipe_create_usecase` / `get_recipe_update_usecase` / 型エイリアス 2 つ）を `deps/usecases/recipe.py` に移動。Service の import 先を `deps.services.recipe` に切り替え |
| 2-4 | 現在の `deps/tag.py` の中身（Repository 系）を `deps/repositories/tag.py` に移動 |
| 2-5 | `routers/` 配下の import 文を **すべて新パスに更新**（`grep -rn "from deps\." backend/routers` で抽出）|
| 2-6 | 古い `deps/recipe.py` `deps/tag.py` を削除 |
| 2-7 | `pytest -v` + `uvicorn main:app --reload` で回帰確認 |

### Laravel との対応

| Laravel | この再編成での対応 |
|---|---|
| `app/Providers/AppServiceProvider.php` の `bind(...)` 群 | `deps/usecases/`, `deps/services/`, `deps/repositories/` で **層ごとにファイル分割** |
| サービスコンテナが自動解決 | FastAPI は **手書きの DI プロバイダ** がその役。**自分で「コンテナの中身」を書いている** |

### Phase 2 完了基準（2026-05-07 達成）

- [x] `deps/` 配下が usecases / services / repositories に分類されている
- [x] 古い `deps/recipe.py` `deps/tag.py` は削除済み
- [x] routers の import がすべて新パスを向いている（`routers/class_tag.py:5` / `routers/recipe.py:5`）
- [x] pytest 全緑（6 passed）
- [x] `main.py` の import OK

---

## Phase 3: FastAPI ↔ Laravel 総まとめドキュメント

Phase 1, 2 を踏み終えた時点で、**全部の層に自分で手を入れた状態** になる。その経験を踏まえて「Laravel と比べて FastAPI ではどこが違ったか」を 1 枚にまとめる。

### 配置先の選択肢

- **案 A:** `docs/fastapi-vs-laravel.md` を新規作成（独立した参照ドキュメント）
- **案 B:** `docs/learning-roadmap.md` の末尾に「総括」章として追記（学習の物語として一貫する）

→ 着手時に決定する。

### 押さえる観点（叩き台）

| 観点 | Laravel | FastAPI で自分でやったこと |
|---|---|---|
| **DI の自動性** | 型ヒントだけでサービスコンテナが自動解決 | `Depends()` を **手で書く**。`Annotated[X, Depends(...)]` 型エイリアスで簡略化 |
| **層の責務分担** | Service が万能になりがち | **crud / repository / usecase / service / router** の **5 層の役割を厳密に意識**する必要（書く場所を間違えると意味が崩れる）|
| **バリデーション** | `FormRequest` クラス | Pydantic Schema（型ヒント駆動・宣言的）|
| **トランザクション境界** | `DB::transaction(fn () => ...)` | `async with db_session.begin():` |
| **テスト時の差し替え** | `$this->mock(Class::class)` | `app.dependency_overrides[provider] = ...` |
| **非同期 IO** | 基本同期 | `async/await` 全面（`AsyncSession` / `httpx.AsyncClient`）|
| **ルーティング** | ルートファイル + Controller | `APIRouter(prefix=..., tags=[...])` でリソース単位分割 |
| **モデル ⇄ レスポンス変換** | `ApiResource` | Pydantic Schema + `from_attributes=True` |
| **多対多 + ピボット属性** | `withPivot('quantity')` | Association Object パターン（`recipe_ingredients` 中間モデルを明示）|
| **ファイル/ディレクトリ命名** | フレームワーク規約で固定 | **自分で決める必要**（`crud` vs `cruds` のリネームを踏んだ 等）|
| **遭遇した罠** | - | `pytest.ini` rootdir / `pythonpath` / `aiosqlite` / `StaticPool` / `dependency_overrides` 忘れ など |

### Phase 3 完了基準（2026-05-07 達成）

- [x] 配置先決定: **案 A**（`docs/fastapi-vs-laravel.md` 新規作成）
- [x] 主要観点が一望表で見える
- [x] Phase 1, 2 で踏んだ罠（14 個）+ 気づきリスト（9 個）+ 残課題リストも記録

---

## 全体スケジュール感

| Phase | 想定ボリューム |
|---|---|
| Phase 1 | 4 Step（小さい修正 → DI 追加 → UseCase 書き換え → 回帰確認）|
| Phase 2 | ファイル移動 + import 修正の機械的作業がメイン |
| Phase 3 | ドキュメント執筆。Phase 1, 2 で得た実体験を整理する時間 |

各 Phase の終わりに必ず `pytest` で回帰確認することで、**「動いている」** という実体で進捗を確認しながら進める。
