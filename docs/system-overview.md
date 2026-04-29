# レシピ管理システム 全体図

## テーブル構成（6テーブル）

```
users (ユーザー)
├── id
├── username     (ユニーク)
├── password_hash(ハッシュ化済みパスワード)
└── created_at

recipes (レシピ)
├── id
├── user_id      ──→ users.id (投稿者)
├── title        (タイトル)
├── description  (説明文)
├── servings     (何人前)
└── created_at

tags (タグ)
├── id
└── name         (例: 和食, 簡単, 時短)

ingredients (食材)
├── id
└── name         (例: 鶏もも肉, 玉ねぎ)

recipe_tags (中間テーブル)
├── recipe_id  ──→ recipes.id
└── tag_id     ──→ tags.id

recipe_ingredients (中間テーブル・数量付き)
├── recipe_id     ──→ recipes.id
├── ingredient_id ──→ ingredients.id
└── quantity       (例: "200g", "大さじ1")
```

## リレーション

```
users   ←──一対多──→ recipes       (1人のユーザーが複数レシピを投稿)
recipes ←──多対多──→ tags          (1つのレシピに複数タグ、1つのタグに複数レシピ)
recipes ←──多対多──→ ingredients   (数量付き)
```

## フロントエンド画面（想定）

| 画面 | 内容 |
|------|------|
| レシピ一覧 | 検索・タグ絞り込み付き |
| レシピ詳細 | タグ・食材と数量を表示 |
| レシピ作成/編集 | タグ選択、食材+数量の入力 |
| タグ管理 | タグのCRUD |
| 食材管理 | 食材のCRUD |
| 買い物リスト | レシピを複数選んでリスト生成 |
| ダッシュボード | 統計情報を表示 |
