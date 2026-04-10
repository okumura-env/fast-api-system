# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリで作業する際のガイドラインです。

**長くなっても良いので端折らずに「品質」を最優先とすること。**

## 概要

レシピ管理システム — レシピ・タグ・食材を管理し、買い物リストの自動生成や統計ダッシュボードを提供するWebアプリケーション。

- バックエンド: **FastAPI** + **SQLAlchemy**（非同期） + **SQLite**
- フロントエンド: **Vue 3** + **Vite** + **axios** + **vue-router**

## リポジトリ構成

```
backend/
├── main.py              ← FastAPIアプリケーション定義・エントリポイント
├── database.py          ← DB接続設定（非同期エンジン・セッション管理）
├── models/              ← SQLAlchemyモデル（テーブル定義）
│   └── tag.py
├── schemas/             ← Pydanticスキーマ（リクエスト/レスポンス定義）
│   └── tag.py
├── crud/                ← DB操作（CRUD関数）
│   └── tag.py
└── routers/             ← APIルーター（エンドポイント定義）
    └── tag.py

frontend/
├── src/
│   ├── App.vue          ← ルートコンポーネント
│   ├── main.js          ← エントリポイント
│   └── style.css        ← グローバルスタイル
├── index.html
├── vite.config.js
└── package.json

docs/
├── system-overview.md   ← テーブル構成・リレーション・画面一覧
└── about.md             ← 機能一覧

.claude/skills/          ← Claude Code カスタムスキル
├── ganesha-lecture/     ← ガネーシャ対話コンテンツ生成スキル（MD→HTML）
└── ganesha-visual-explainers/ ← 図解付きHTML解説生成スキル
```

## データベース設計（5テーブル）

```
recipes         ← レシピ本体（title, description, servings）
tags            ← タグ（name）
ingredients     ← 食材（name）
recipe_tags     ← レシピ×タグの中間テーブル（多対多）
recipe_ingredients ← レシピ×食材の中間テーブル（quantity付き・多対多）
```

現在実装済み: `tags` テーブルのみ。他テーブルは未実装。

## 開発コマンド

```bash
# バックエンド起動
cd backend
uvicorn main:app --reload

# フロントエンド起動
cd frontend
npm run dev
```

## バックエンドのアーキテクチャ（レイヤー構成）

リクエストの流れ: `routers/ → crud/ → models/`、バリデーションは `schemas/` が担当。

| レイヤー | 役割 |
|---------|------|
| `routers/` | エンドポイント定義。HTTPリクエストを受け取り、CRUDを呼び出す |
| `schemas/` | Pydanticスキーマ。リクエスト/レスポンスのバリデーションと型定義 |
| `crud/` | データベース操作。SQLAlchemy非同期セッションを使ったCRUD関数 |
| `models/` | SQLAlchemyモデル。テーブル定義とカラム設定 |
| `database.py` | DB接続設定。非同期エンジン・セッションファクトリ・`get_dbsession` |

## コーディング規約

- **非同期**: DB操作はすべて `async/await` で行う（`AsyncSession` 使用）
- **スキーマ**: 登録/更新用と取得用でPydanticスキーマを分離する
- **ルーター**: `APIRouter` を使い、`prefix` と `tags` を設定してリソースごとに分割する
- **エラーハンドリング**: 存在しないリソースは `HTTPException(404)`、操作失敗は `HTTPException(400)` を返す

## 現在の開発状況

- タグのCRUD（models / schemas / crud / routers）が実装途中
- `main.py` にはルーターを使わない仮実装のエンドポイントが残っている
- フロントエンドは初期テンプレート状態
- recipes, ingredients, recipe_tags, recipe_ingredients は未実装
