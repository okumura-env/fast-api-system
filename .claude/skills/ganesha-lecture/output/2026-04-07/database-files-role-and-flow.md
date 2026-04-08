# 🗄️ FastAPIプロジェクトのDB関連ファイル — 役割と流れ

> **結論: データベースのテーブルが作られるまでには「設定」「設計図」「実行」の3ファイルが連携している。**
> `database.py`（接続設定）→ `models/tag.py`（テーブルの設計図）→ `init_database.py`（テーブル作成の実行）。
> そして **「ファイルを作る＋Baseを継承する＋インポートする」の3点セットで初めてテーブルが作られる。**

---

## 🎬 導入 — 「家を建てるのに何が必要？」

🐘「ええか、ナツキ。今日はデータベース関連のファイルについて教えたるわ」

👩‍💻「database.pyとかmodelsとか色々あって、正直どれが何してるのかよくわかんないんですよね…」

🐘「せやろな。ほんなら **家を建てる** のに置き換えて考えてみ？」

👩‍💻疑問「家を建てる…ですか？」

🐘「そや！家を建てるには3つ必要やろ？ 👇こういうことや」

| 家を建てるとき | FastAPIプロジェクト | ファイル |
|---|---|---|
| 🏗️ **土地と住所を決める** | どのDBに、どう接続するか決める | `database.py` |
| 📐 **設計図を描く** | テーブルの列や型を定義する | `models/tag.py` |
| 👷 **工事を実行する** | テーブルを実際に作る | `init_database.py` |

🐘得意げ「土地も決めんと設計図だけ描いても家は建たんし、設計図なしに工事もできひん。**3つセットで初めて動く**んや」

👩‍💻笑顔「あ、なるほど！それぞれが別の役割を持ってるんですね」

🐘「さすガネーシャや！✨ ワシの説明、わかりやすいやろ？」

👩‍💻呆れ「…自分で言いますか。で、具体的にはどうなってるんですか？」

---

## 🔌 まず覚える3つ

🐘「まずこの3つだけ覚えたらOKや。全体の中での位置づけを見てみ」

```
┌─────────────────────────────────────────────┐
│           FastAPIプロジェクト全体              │
│                                             │
│   ① database.py        ← 接続設定           │
│     │                                       │
│     ├─ Base（設計図の親）を作る               │
│     ├─ engine（DBへの通り道）を作る           │
│     └─ session（会話の窓口）を作る            │
│                                             │
│   ② models/tag.py      ← テーブルの設計図    │
│     │                                       │
│     └─ Baseを継承して Tag クラスを定義        │
│                                             │
│   ③ init_database.py   ← テーブル作成の実行   │
│     │                                       │
│     ├─ Tag をインポート（ここが超重要！）      │
│     └─ Base.metadata.create_all で作成       │
│                                             │
└─────────────────────────────────────────────┘
```

👩‍💻「①で準備して、②で設計して、③で実行する…って流れですね」

🐘「そういうことや！ほなら1つずつ見ていこか」

---

## 📁 ファイル① database.py — 「どのDBに、どうやって接続するか」

🐘「まず `database.py` や。これは **DB接続の設定ファイル** やで」

👩‍💻「設定ファイル…？」

🐘「例えるなら **スマホのWi-Fi設定画面** みたいなもんや。「どのWi-Fiに繋ぐか」「パスワードは何か」を設定するやろ？」

| Wi-Fi設定 | database.py |
|---|---|
| 📶 接続先のWi-Fi名 | `DATABASE_URL`（どのDBファイルに繋ぐか） |
| 🔑 パスワード | 接続方式（`sqlite+aiosqlite:///`） |
| 📡 Wi-Fiアンテナ | `engine`（DBへの通り道） |
| 💬 ネットで会話する | `async_session`（DBとやり取りする窓口） |

🐘「ほんで、もう1つ超大事なもんがあるねん。**Base** や」

👩‍💻疑問「Base…？」

🐘「**Base**は「設計図の親」みたいなもんや。これから作るテーブルの設計図は、全部このBaseを継承して作るんやで」

> 💡 **「Base（ベース）」とは？**
> テーブルの設計図（モデル）を作るための**土台**のこと。
> 「うちのプロジェクトのテーブルは全部ここから生まれますよ」という**親クラス**です。
> Baseは自分の子供（＝テーブルの設計図）を全部覚えていて、後で「全部まとめて作って！」と命令できます。

> 💡 **「declarative_base()」とは？**
> 「設計図の親」を1つ作るための**おまじない**みたいな関数。
> これを1回呼ぶと、Base（親）が生まれる。以降、全てのテーブル設計図はこのBaseを継承して作ります。

🐘「ほな、実際のコードを見てみよか 👇」

```python
# database.py — DB接続の設定ファイル

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# ① 設計図の親を作る（全テーブルの土台）
Base = declarative_base()

# ② 接続先を決める（このプロジェクトではSQLiteファイル）
base_dir = os.path.dirname(__file__)
DATABASE_URL = 'sqlite+aiosqlite:///' + os.path.join(base_dir, 'tagdb.sqlite')

# ③ DBへの通り道を作る
engine = create_async_engine(DATABASE_URL, echo=True)

# ④ DBとやり取りする窓口を作る
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# ⑤ 実際にDBセッションを取得する関数
async def get_dbsession():
    async with async_session() as session:
        yield session
```

👩‍💻疑問「`sessionmaker` って何ですか？あと `yield` も気になる…」

🐘「`sessionmaker` は **セッション（DBとの会話）を作る工場** みたいなもんや。DBに何か聞いたり書いたりするたびに、ここからセッションを1個もらうんやで」

🐘「`yield` は **「使い終わったら自動で片付けてくれる」** 仕組みや。DBとの会話が終わったら、接続を自動で閉じてくれるから便利やねん」

👩‍💻笑顔「なるほど！後片付けまで面倒見てくれるんですね」

👩‍💻「コードの中に①〜⑤まで役割があるんですね。でも `echo=True` って何ですか？」

🐘ボケをかます「ええ質問やな！`echo=True` は **DBとのやり取りを全部ターミナルに表示する** 設定や。開発中は超便利やで。裏で何やってるか丸見えになるからな」

👩‍💻「デバッグ用ってことですね」

🐘「そや。本番では `False` にするのが普通やけどな。ワシの教え子の **ザッカーバーグくん** もな、Facebookの開発初期はログ全部出してたって言うてたわ」

👩‍💻呆れ「…本当ですか、それ？」

---

## 📐 ファイル② models/tag.py — 「テーブルの設計図」

🐘「次は `models/tag.py` や。これは **テーブルの設計図** やで」

👩‍💻「設計図っていうのは…？」

🐘「例えるなら **Excelの表のテンプレート** みたいなもんや。「この表には何列あって、それぞれどんな種類のデータが入るか」を決めるやろ？」

| Excelのテンプレート | models/tag.py |
|---|---|
| 📊 シート名 | `__tablename__ = "tags"` |
| 🔢 番号列（自動連番） | `tag_id = Column(Integer, primary_key=True)` |
| 📝 タイトル列 | `title = Column(String(50), nullable=False)` |
| 📅 作成日列 | `created_at = Column(DateTime, ...)` |
| 📅 更新日列 | `updated_at = Column(DateTime)` |

🐘「ポイントは **Baseを継承している** ことやで。`class Tag(Base):` ← ここが超重要！」

👩‍💻疑問「継承すると何が起きるんですか？」

🐘得意げ「めっちゃええ質問やな！Baseを継承した瞬間、Baseが **「あ、tagsっていうテーブルの設計図ができたな」** って自動的に覚えるんや」

```
Base = declarative_base()
  │
  │  ← 「ワシが設計図の親やで」
  │
  ├── class Tag(Base):        ← Baseが「tagsテーブル」を記憶！
  │     __tablename__ = "tags"
  │
  ├── class Recipe(Base):     ← Baseが「recipesテーブル」も記憶！
  │     __tablename__ = "recipes"
  │
  └── （他にも増やせる）       ← 全部Baseが覚えてる
```

👩‍💻笑顔「へぇ〜！Baseが自分の子供を全部覚えてるってことですね」

🐘「そういうことや！ほんで実際のコードはこうなっとる 👇」

```python
# models/tag.py — テーブルの設計図

from sqlalchemy import Column, Integer, String, DateTime
from database import Base  # ← database.pyからBaseを借りてくる
from datetime import datetime

class Tag(Base):
    __tablename__ = "tags"  # ← 実際のテーブル名

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    #        ↑ 整数型    ↑ 主キー（一意のID）  ↑ 自動で1,2,3...と増える

    title = Column(String(50), nullable=False)
    #       ↑ 文字列型（50文字まで）  ↑ 空っぽはダメ！

    created_at = Column(DateTime, default=datetime.now())
    #           ↑ 日時型        ↑ 何も指定しなければ「今」が入る

    updated_at = Column(DateTime)
    #           ↑ 更新日。最初はなし（None）
```

🐘「これで「tagsっていうテーブルには4つの列があるで」っていう設計図ができたわけや」

👩‍💻「`from database import Base` で、さっきのdatabase.pyからBaseを借りてきてるんですね」

🐘「そや！ここで **つながり** ができるんや。database.pyで作ったBaseを、models/tag.pyで使う。この関係が大事やで」

---

## 🚀 ファイル③ init_database.py — 「テーブル作成の実行」

🐘「最後は `init_database.py` や。これが **実際にテーブルを作る実行スクリプト** やで」

👩‍💻「設計図があるだけじゃダメなんですか？」

🐘「当たり前やがな！設計図描いただけで家が建つか？ **工事する人** がおらなアカンやろ」

👩‍💻笑顔「あ、そうか！設計図をもとに実際に建てる人が必要なんですね」

🐘「そや！ほんで、ここで **めちゃくちゃ重要なポイント** があるねん」

> 💡 **超重要: `create_all` は「Pythonにインポートされたモデル」だけを検知する**
> ファイルを作っただけではダメ！
> `init_database.py` の中で `from models.tag import Tag` と**インポートして初めて**、
> Baseが「tagsテーブルを作らなあかんな」と認識します。

> 💡 **「metadata（メタデータ）」とは？**
> Baseが持っている **「設計図リスト」** のこと。
> Baseを継承したクラスが作られるたびに、このリストに自動で追加されます。
> `create_all` はこのリストを見て「どのテーブルを作ればいいか」を判断します。

🐘「ここ、マジで大事やから、もう一回たとえ話するで」

👩‍💻「お願いします！」

🐘「**工事現場の朝礼** を想像してみ？」

| 工事現場の朝礼 | init_database.py |
|---|---|
| 👷 現場監督が集合をかける | `init_database.py` を実行する |
| 📋 設計図を持ってきた人だけが参加できる | **インポートされたモデルだけ** が対象 |
| 📐 「Aさんの設計図」を受け取る | `from models.tag import Tag` |
| 📐 「Bさんの設計図」も受け取る | `from models.recipe import Recipe` |
| 🏗️ 「全員分の設計図で工事開始！」 | `Base.metadata.create_all` |
| ❌ 設計図を持ってこなかった人は無視される | インポートしてないモデルは作られない！ |

👩‍💻感動「あ〜〜！だから `import Tag` が必要なんですね！設計図を「持ってくる」行為がインポートなんだ！」

🐘得意げ「さすガネーシャや！✨ ええ教え方やろ？」

👩‍💻呆れ「…自画自賛はいいので、コード見せてください」

```python
# init_database.py — テーブル作成の実行スクリプト

import os
from sqlalchemy.ext.asyncio import create_async_engine
from database import Base
from models.tag import Tag  # ← ★このインポートが超重要！★
import asyncio
# ↑ Tagをインポートした瞬間、Baseが「tagsテーブル作るで」と記憶する

base_dir = os.path.dirname(__file__)
DATABASE_URL = 'sqlite+aiosqlite:///' + os.path.join(base_dir, 'tagdb.sqlite')

engine = create_async_engine(DATABASE_URL, echo=True)

async def init_db():
    print("=== データベースの初期化を開始 ===")
    async with engine.begin() as conn:
        # 既存テーブルを全部消す（開発中のリセット用）
        await conn.run_sync(Base.metadata.drop_all)
        print(">>> 既存のテーブルを削除しました。")

        # Baseが覚えている設計図を全部テーブルにする
        await conn.run_sync(Base.metadata.create_all)
        print(">>> 新しいテーブルを作成しました。")

if __name__ == "__main__":
    asyncio.run(init_db())
```

🐘「`if __name__ == "__main__":` は **「このファイルを直接実行したときだけ動く」** って意味や。ターミナルで `python init_database.py` って打つと動くで」

---

## 🔄 テーブルが作られるまでの全体の流れ

🐘「ほな、3つのファイルがどう連携してテーブルが作られるか、流れを見てみよか」

```
【ステップ1】database.py が読み込まれる
┌──────────────────────────────────┐
│  Base = declarative_base()       │
│  engine = create_async_engine()  │
│                                  │
│  Base:「ワシが設計図の親や。     │
│        まだ子供はおらんで」       │
└──────────────────────────────────┘
              │
              ▼
【ステップ2】from models.tag import Tag が実行される
┌──────────────────────────────────┐
│  class Tag(Base):                │
│      __tablename__ = "tags"      │
│                                  │
│  Base:「お！tagsの設計図が来た。 │
│        覚えたで！」              │
└──────────────────────────────────┘
              │
              ▼
【ステップ3】Base.metadata.create_all が実行される
┌──────────────────────────────────┐
│  await conn.run_sync(            │
│      Base.metadata.create_all    │
│  )                               │
│                                  │
│  Base:「覚えてる設計図、全部     │
│        テーブルにするで！」       │
│                                  │
│  → tagsテーブルが作られる！🎉    │
└──────────────────────────────────┘
```

👩‍💻笑顔「Baseがずっと主役みたいな感じですね！設計図を受け取って、最後にまとめて作る」

🐘「その通りや！Baseは **設計図の管理人** みたいなもんやな」

---

## ➕ 新しいテーブルを追加するときの流れ

🐘「ほんなら、例えば **recipesテーブル** を追加したいとき、どうするか教えたるわ」

👩‍💻「はい！知りたいです」

🐘「4ステップや 👇」

```
【新しいテーブルを追加する4ステップ】

Step 1: models/ にファイルを作る
         → models/recipe.py を新規作成

Step 2: Baseを継承したクラスを書く
         → class Recipe(Base): ...

Step 3: init_database.py でインポートする
         → from models.recipe import Recipe  ← これを追加！

Step 4: init_database.py を実行する
         → python init_database.py
```

🐘「ここで **よくあるミス** を教えたるわ。ワシの教え子の **ラリー・ペイジくん** も同じミスしてたで」

👩‍💻呆れ「Googleの創業者がそのミスしてるわけないでしょ…」

🐘誤魔化し「ま、まぁ細かいことはええやんけ！大事なのはミスの内容や 👇」

| よくあるミス | なぜダメか | 正しいやり方 |
|---|---|---|
| ❌ models/にファイルを作っただけ | Baseが設計図を知らない | ✅ Baseを継承したクラスを書く |
| ❌ クラスは書いたがインポートしてない | create_allが検知できない | ✅ init_database.pyでインポートする |
| ❌ インポートしたが実行してない | テーブルはまだ存在しない | ✅ `python init_database.py` を実行 |

🐘「つまり **3点セット** が揃って初めてテーブルが作られるんや」

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   テーブルが作られる条件（3点セット）                  │
│                                                     │
│   ✅ ファイルを作る     → models/recipe.py           │
│           +                                         │
│   ✅ Baseを継承する     → class Recipe(Base):        │
│           +                                         │
│   ✅ インポートする     → from models.recipe import  │
│                                                     │
│   → この3つが揃うと create_all がテーブルを作る 🎉   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

👩‍💻感動「**ファイル＋継承＋インポート**！この3点セット、覚えました！」

---

## 🔍 テーブルが増えていくイメージ

🐘「最後に、テーブルが増えていくイメージを見せたるわ」

👩‍💻「お願いします！」

```
【init_database.py のインポート部分】

from database import Base
from models.tag import Tag          # ← Baseに "tags" が登録される
from models.recipe import Recipe    # ← Baseに "recipes" も登録される
from models.user import User        # ← Baseに "users" も登録される

# この時点でBaseが覚えている設計図:
#   Base.metadata = {
#     "tags":    Tag の設計図,
#     "recipes": Recipe の設計図,
#     "users":   User の設計図,
#   }

# ↓ 覚えてる設計図を全部テーブルにする！
await conn.run_sync(Base.metadata.create_all)

# 結果:
#   tagsテーブル    → 作成完了 ✅
#   recipesテーブル → 作成完了 ✅
#   usersテーブル   → 作成完了 ✅
```

🐘得意げ「インポートの数だけテーブルが増えるわけや。シンプルやろ？」

👩‍💻笑顔「めっちゃわかりやすい！インポートが「設計図を持ってくる」行為で、create_allが「まとめて建設する」ってことですね」

🐘「完璧や！」

---

## 📋 まとめ — 3つのファイルの役割

🐘「ほな、最後にまとめるで」

| ファイル | 役割 | 一言で言うと |
|---|---|---|
| `database.py` | DB接続設定＋Baseを作る | 🏗️ 土地と住所を決める人 |
| `models/tag.py` | テーブルの列と型を定義 | 📐 設計図を描く人 |
| `init_database.py` | テーブルを実際に作る | 👷 工事を実行する人 |

```
database.py           models/tag.py        init_database.py
 (設定)                 (設計図)              (実行)
┌────────┐           ┌────────────┐        ┌──────────────┐
│ Base   │──継承──→ │ class Tag  │──import→│ create_all   │
│ engine │           │ (Base)     │        │ でテーブル    │
│ session│           │ tag_id     │        │ 作成！🎉     │
└────────┘           │ title      │        └──────────────┘
                     │ created_at │
                     │ updated_at │
                     └────────────┘
```

👩‍💻笑顔「3つのファイルの役割と、テーブルが作られるまでの流れ、バッチリわかりました！」

🐘「ええか、最後にもう一回言うとくで。**ファイルを作る＋Baseを継承する＋インポートする。この3点セットを忘れたらアカンで！**」

👩‍💻「はい！新しいテーブルを追加するときは3点セットですね」

🐘ボケをかます「ちなみにワシへのお供えもんも3点セットでお願いしたいんやけどな。あんみつ🍨と、あんみつ🍨と、あんみつ🍨や」

👩‍💻怒る「全部あんみつじゃないですか！」

🐘誤魔化し「ま、まぁ細かいことはええやんけ…！」

🐘得意げ「さすガネーシャや！✨ 今日もええ授業やったな」

👩‍💻呆れ「…自分で言うスタイル、ほんとにブレないですね」

🐘決めポーズ「はい、Oh, My God!! 🙏✨」
