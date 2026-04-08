# 🏗️ tokuyama-project ディレクトリ構成ガイド

> **結論: このプロジェクトは Laravel 9（バックエンド）+ Vue 3（フロントエンド）の完全分離型SPA。車両配車管理システムで、`app/` にビジネスロジック、`resources/js/` にフロントエンド、`database/` にDB定義が入っとる。迷ったらこの3つを押さえれば大丈夫や！**

---

## 🎬 導入 ー 家に例えたら一発でわかるで！

🐘「ナツキ、今日はこのプロジェクトの**ディレクトリ構成**を教えたるわ！」

👩‍💻「お願いします！ファイル多すぎてどこに何があるか全然わからないんです...」

🐘「せやろな。昔ワシの教え子の**エジソンくん**がな、『整理整頓は発明の母や！』って言うてたんや。コードも同じやで」

👩‍💻「それ、本当にエジソンの言葉ですか...？」

🐘誤魔化し「ま、まぁ細かいことはええやんけ！とにかくな、このプロジェクトは**家**に例えると一発でわかるで！」

```
🏠 tokuyama-project（家全体）
├── 🍳 app/           ← キッチン（料理＝ビジネスロジックを作る場所）
├── 🛋️ resources/js/  ← リビング（お客さん＝ユーザーが見る画面）
├── 🗄️ database/      ← 倉庫（食材＝データを保管する場所）
├── 🚪 routes/        ← 玄関・廊下（どの部屋に案内するかの道標）
├── ⚙️ config/        ← 設計図（家のルール・設定）
├── 🧪 tests/         ← 検査室（品質チェック）
└── 📦 public/        ← 表札・門構え（外から見える部分）
```

👩‍💻「なるほど！それぞれの場所に役割があるんですね」

🐘得意げ「そういうことや！さすガネーシャや、この例えは天才的やろ！✨」

👩‍💻「自分で言うの恥ずかしくないんですか...（笑）」

---

## 📂 プロジェクト全体の俯瞰図

🐘「まずは全体をざっと見せたるわ。こういう構成になっとる」

```
tokuyama-project/
├── 📱 app/              ← バックエンドのビジネスロジック（Laravel）
├── 🎨 resources/        ← フロントエンドのコード（Vue 3）+ Bladeテンプレート
├── 🗄️ database/         ← マイグレーション・シーダー・ファクトリー
├── 🚏 routes/           ← URLルーティング定義
├── ⚙️ config/           ← Laravel設定ファイル群
├── 🧪 tests/            ← PHPUnit テストコード
├── 🐳 docker/           ← Docker環境設定
├── 📦 public/           ← 公開ディレクトリ（Webルート）
├── 🗂️ storage/          ← ログ・キャッシュ・アップロードファイル
├── 📚 docs/             ← プロジェクトドキュメント群
├── 📚 vendor/           ← PHPパッケージ（Composer）
└── 📦 node_modules/     ← JSパッケージ（npm）
```

👩‍💻「ルートに10個以上あるんですね。どこから見ればいいですか？」

🐘「**日常的に触るのは3つだけ**や。`app/`、`resources/js/`、`database/`。この3つで開発の90%以上をカバーできるで」

| よく触る度 | ディレクトリ | 何をする場所？ |
|---|---|---|
| ⭐⭐⭐ | `app/` | API・ビジネスロジック・バリデーション |
| ⭐⭐⭐ | `resources/js/` | Vue画面・composable・コンポーネント |
| ⭐⭐ | `database/` | テーブル定義・初期データ |
| ⭐⭐ | `routes/api.php` | APIルート追加 |
| ⭐⭐ | `tests/` | テスト作成・実行 |
| ⭐ | `config/` | 設定変更時のみ |
| ⭐ | `docs/` | ドキュメント参照・更新 |

---

## 🍳 `app/` ー バックエンドの心臓部

🐘「ここがこのプロジェクトの**心臓部**や！リクエストを受け取って、処理して、レスポンスを返す。全部ここでやっとる」

👩‍💻「中身はどうなってるんですか？」

🐘「レイヤーごとに分かれとるんや。**リクエストの流れ**に沿って説明するで！」

```
リクエストの流れ 🚀

ブラウザ → routes/api.php → Middleware → Controller → UseCase → Model → DB
                                ↓            ↓           ↓
                             認証チェック   Request      Eloquent
                                         (バリデーション) (ORM)
                                              ↓
                                           Resource
                                        (レスポンス整形)
```

### app/ の詳細構成

```
app/
├── Http/
│   ├── Controllers/Api/     ← APIコントローラー（36ファイル）
│   ├── Requests/            ← バリデーション（33ファイル）
│   ├── Resources/           ← レスポンス整形（28ファイル）
│   ├── Middleware/           ← 認証・CORSなど（9ファイル）
│   └── Responses/
│       └── ApiResponse.php  ← 統一レスポンスフォーマット
│
├── UseCases/                ← ビジネスロジック層（80ファイル！）
│   ├── DumpOrder/           ← ダンプ注文（12ファイル、最大規模）
│   ├── DumpSchedule/        ← ダンプスケジュール（5ファイル）
│   ├── User/                ← ユーザー管理（7ファイル）
│   ├── Vehicle/             ← 車両管理（6ファイル）
│   └── ... 他多数
│
├── Models/                  ← Eloquentモデル（28ファイル）
│   ├── DumpSchedule.php     ← ダンプスケジュール
│   ├── Vehicle.php          ← 車両
│   ├── User.php             ← ユーザー
│   └── ... 他多数
│
├── Constants/               ← 定数クラス（マジックナンバー撲滅！）
│   ├── RoleIds.php          ← ロールID定数
│   ├── VehicleGroups.php    ← 車両グループ定数
│   └── ... 他
│
├── Exceptions/              ← 例外クラス
│   ├── ApiExceptionHandler.php  ← API例外を一括処理
│   └── ConflictException.php    ← 競合エラー
│
├── Services/                ← ドメインサービス（2ファイル）
├── Helpers/                 ← ヘルパー関数
│   └── SentryHelper.php     ← Sentry通知
├── Mail/                    ← メール送信クラス（8ファイル）
├── Providers/               ← サービスプロバイダ（DI設定）
└── DTO/                     ← Data Transfer Object
```

👩‍💻「UseCaseが80個もあるんですか！？ 多くないですか？」

🐘得意げ「そう思うやろ？でもな、**1UseCase = 1責務**の原則を守っとるからこそ、この数になるんや」

👩‍💻「どういうことですか？」

🐘「例えばダンプ注文（DumpOrder）だけでも、**作成・更新・削除・インポート・ルール適用**...と処理が全然違うやろ？それぞれを別のUseCaseにしとけば、1ファイルが**小さくて読みやすい**し、変更の影響範囲も限定できるんや」

| レイヤー | 役割 | 禁止事項 |
|---|---|---|
| **Controller** | HTTP処理・認証認可・バリデーション | ビジネスロジックを書くな！ |
| **UseCase** | 複雑なビジネスロジック・トランザクション | HTTPリクエストを直接触るな！ |
| **Model** | DBアクセス・リレーション・スコープ | トランザクション管理するな！ |

🐘ボケをかます「ちなみにな、昔ワシの教え子の**ナポレオンちゃん**がな、『軍隊は分けて統治せよ！』って言うてたんや。UseCaseもまさにそれや！」

👩‍💻「分割統治法ですね。...でもナポレオンが"ちゃん"付けされるの、本人が聞いたら怒りそう」

🐘焦り「い、いやいや！ナポレオンちゃんはワシに感謝しとるで！...多分な！」

---

## 🛋️ `resources/js/` ー フロントエンドの世界

🐘「次はフロントエンドや！ユーザーが実際に目にする画面はぜ〜んぶここに入っとる」

```
resources/js/
├── api/
│   └── axiosClient.js       ← API通信の窓口（これ以外でaxios使用禁止！）
│
├── Views/                   ← 画面コンポーネント（84ファイル）
│   ├── DumpSchedules/       ← ダンプスケジュール画面（7ファイル）
│   ├── JetpackSchedules/    ← ジェットパック画面（9ファイル）
│   ├── WpPksSchedules/      ← WP PKS画面（7ファイル）
│   ├── MasterManagement/    ← マスタ管理画面（31ファイル）
│   │   ├── Vehicles/        ← 車両マスタ
│   │   ├── Users/           ← ユーザーマスタ
│   │   ├── IndexFormat.vue  ← 共通一覧テンプレート
│   │   └── FormFormat.vue   ← 共通フォームテンプレート
│   ├── NotificationSettings/ ← 通知設定（7ファイル）
│   ├── Auth/                ← ログイン画面
│   └── Profile/             ← プロフィール設定
│
├── composables/             ← 再利用ロジック（61ファイル）
│   ├── api/                 ← API共通処理（CRUD）
│   ├── shared/              ← 全画面共通（21ファイル、最大）
│   ├── dump-schedules/      ← ダンプ専用（11ファイル）
│   ├── jetpack-schedules/   ← ジェットパック専用（7ファイル）
│   ├── drivers/             ← ドライバー関連（8ファイル）
│   ├── navigation/          ← 画面遷移（5ファイル）
│   ├── wp-pks-schedules/    ← WP PKS専用（4ファイル）
│   └── ...
│
├── components/              ← 再利用UIコンポーネント（25ファイル）
├── stores/                  ← Pinia状態管理（4ファイル）
├── utils/                   ← ユーティリティ関数（6ファイル）
├── Layouts/                 ← レイアウト（3ファイル）
├── router.js                ← Vue Routerルーティング
├── app.js                   ← エントリーポイント
└── App.vue                  ← ルートコンポーネント
```

👩‍💻「composablesが61ファイルもあるんですね。これって何の役割ですか？」

🐘「**Composition API**で使う再利用可能なロジックや！**工具箱**に例えるとわかりやすいで」

| 🔧 工具箱の道具 | 💻 composable | 役割 |
|---|---|---|
| 🔨 ハンマー | `api/useFetchData.js` | データ一覧取得 |
| 🪛 ドライバー | `api/useStoreOrUpdateData.js` | 作成・更新処理 |
| 📏 メジャー | `shared/useFormErrors.js` | バリデーションエラー表示 |
| 🔔 ベル | `shared/useNotifier.js` | トースト通知 |
| 🚪 ドア | `shared/useModal.js` | モーダル開閉制御 |

🐘得意げ「ドメインごとにサブディレクトリに分かれとるから、どこに何があるかすぐわかるやろ？さすガネーシャや！✨」

👩‍💻「それはプロジェクトの設計者が偉いのであって、ガネーシャの手柄じゃないですよね？」

🐘焦り「う...まぁまぁ、ワシが**裏で指導した**ということにしといてくれ...」

---

## 🗄️ `database/` ー データの設計図

🐘「次はデータベース関連や！テーブル設計からテストデータまで全部ここにあるで」

```
database/
├── migrations/     ← テーブル定義（36ファイル）← 設計図
├── seeders/        ← 初期データ投入（31ファイル）← 家具配置
└── factories/      ← テストデータ生成（27ファイル）← ダミー家具
```

👩‍💻「migrations・seeders・factoriesの違いがイマイチ...」

🐘ボケをかます「家を建てる例えでいくで！」

```
🏗️ 家を建てるプロセス

1. 📐 migrations  = 設計図を描く    → テーブル構造を定義
2. 🪑 seeders     = 本物の家具を置く → 本番用の初期データ
3. 🧸 factories   = ダミー家具を置く → テスト用のランダムデータ
```

| 工程 | ファイル | いつ使う？ | 例 |
|---|---|---|---|
| 設計 | `migrations/` | テーブル作成・変更時 | `create_vehicles_table` |
| 配置 | `seeders/` | 初期データ投入時 | ロールマスタ・車両タイプ |
| テスト | `factories/` | テスト実行時 | ダミーユーザー・ダミー車両 |

🐘「ちなみにこのプロジェクトには**36テーブル**あるで。車両、ダンプ、ジェットパック、WP PKS...業務ドメインごとにテーブルが分かれとる」

👩‍💻「36個って結構多いですね。どこかに全体像はありますか？」

🐘「`docs/architecture/DB_SPECIFICATION.md`にER図含めて全部載っとるで！」

---

## 🚏 `routes/` ー URLの道標

🐘「ルーティングはURLと処理のマッピングや」

```
routes/
├── api.php       ← APIルート（/api/*）← メインで使うのはこれ！
├── web.php       ← Webルート（SPAのエントリーポイント）
├── channels.php  ← ブロードキャスト
└── console.php   ← Artisanコマンド
```

👩‍💻「普段触るのは `api.php` だけですか？」

🐘「**99%はそうや**。このプロジェクトはSPAやから、画面遷移はVue Routerが担当して、サーバーとの通信は全部APIルート経由やで」

🐘「ルーティングの命名規則も決まっとる。**kebab-case**や！」

```php
// ✅ 正しい
Route::apiResource('dump-schedules', DumpScheduleController::class);

// ❌ ダメ
Route::apiResource('dumpSchedules', DumpScheduleController::class);
```

---

## 🧪 `tests/` ー 品質の番人

🐘「テストコードはここや！」

```
tests/
├── Feature/      ← 機能テスト・統合テスト（47ファイル）
├── Unit/         ← 単体テスト（9ファイル）
├── Fixtures/     ← テスト用の固定データ（Excelファイル等）
└── TestCase.php  ← テストの基底クラス
```

👩‍💻「FeatureとUnitの違いって何ですか？」

🐘「**Feature**はAPIを叩いて結果を確認する**統合テスト**。**Unit**は1つのクラス・メソッドだけをテストする**単体テスト**や」

| テスト種別 | 何をテストする？ | 例 |
|---|---|---|
| **Feature** | APIエンドポイント全体 | `POST /api/vehicles` → 201 |
| **Unit** | 1つのメソッド | `VehicleGroups::getDumpIds()` |

🐘得意げ「昔ワシの教え子の**ライト兄弟**がな、『テスト飛行なしで本番飛行はありえへん！』と言うてたで！」

👩‍💻「テストなしでデプロイするのはパラシュートなしのスカイダイビング、ということですね」

🐘「そういうことや！💀」

---

## 📚 `docs/` ー ドキュメントの宝庫

🐘「このプロジェクトにはドキュメントが充実しとるで！困ったらまず `docs/` を見るんや」

```
docs/
├── architecture/            ← アーキテクチャ系
│   ├── ARCHITECTURE.md      ← 全体アーキテクチャ・リクエストフロー
│   ├── DIRECTORY_STRUCTURE.md ← ディレクトリ構成（このテーマ！）
│   ├── DB_SPECIFICATION.md  ← DB仕様・ER図・全36テーブル定義
│   ├── ERROR_HANDLING.md    ← エラーハンドリング方針
│   └── LAYER_RESPONSIBILITIES.md ← レイヤー責務
│
├── conventions/             ← 規約系
│   ├── NAMING_CONVENTIONS.md ← 命名規則
│   └── ROUTING_CONVENTIONS.md ← ルーティング規約
│
├── guides/                  ← ガイド系
│   ├── NEW_FEATURE_GUIDE.md ← 新機能追加の10ステップ
│   ├── COMPOSABLES_GUIDE.md ← composable作成ガイド
│   ├── AUTHENTICATION_GUIDE.md ← 認証フローガイド
│   ├── DEPLOY_CHECKLIST.md  ← デプロイチェックリスト
│   ├── N_PLUS_1_QUERY_FIXES.md ← N+1修正記録
│   └── SETUP_VEHICLE_IDS.md ← 車両定数の更新手順
│
└── implementation/          ← 実装パターン
    └── ...                  ← コンポーネント・composableリファクタリング
```

👩‍💻「すごい充実してますね！どういう時にどれを見ればいいんですか？」

🐘「ユースケース別にまとめたるわ！」

| やりたいこと | 見るドキュメント |
|---|---|
| 新機能を追加したい | `guides/NEW_FEATURE_GUIDE.md` |
| 命名で迷った | `conventions/NAMING_CONVENTIONS.md` |
| エラー処理を実装したい | `architecture/ERROR_HANDLING.md` |
| DB設計を確認したい | `architecture/DB_SPECIFICATION.md` |
| composableを作りたい | `guides/COMPOSABLES_GUIDE.md` |
| デプロイ前の確認 | `guides/DEPLOY_CHECKLIST.md` |

---

## ⚙️ その他の重要ファイル

🐘「ルートディレクトリにある設定ファイル群も押さえとくんやで」

```
tokuyama-project/
├── composer.json          ← PHP依存関係
├── package.json           ← JS依存関係
├── vite.config.js         ← Viteビルド設定
├── tailwind.config.js     ← TailwindCSS設定
├── phpunit.xml            ← テスト設定
├── .env                   ← 環境変数（DB接続情報など）⚠️ Gitに入れるな！
├── docker-compose.yml     ← Docker構成
├── Dockerfile             ← コンテナイメージ
├── Makefile               ← Makeコマンド定義
├── CLAUDE.md              ← Claude Code用ガイダンス
└── .github/workflows/     ← GitHub Actions（CI/CD）
```

👩‍💻「`.env`は絶対にGitに入れちゃダメってことですね」

🐘「**絶対にアカン！** DB接続情報やAPIキーが入っとるからな。`.gitignore`でちゃんと除外されとるけど、万が一にも注意やで！」

---

## 🗺️ まとめ ー 全体マップ

🐘決めポーズ「最後にビシッとまとめるで！」

```
🏠 tokuyama-project 全体マップ

【バックエンド（Laravel）】
  app/Http/Controllers/  → リクエストを受け取る門番
  app/Http/Requests/     → バリデーションの検問所
  app/UseCases/          → ビジネスロジックの工場（80個！）
  app/Models/            → データベースとの通訳（28個）
  app/Http/Resources/    → レスポンスの梱包係
  routes/api.php         → URLの道標

【フロントエンド（Vue 3）】
  resources/js/Views/       → 画面（84ファイル）
  resources/js/composables/ → 再利用ロジック（61ファイル）
  resources/js/components/  → 共通UIパーツ（25ファイル）
  resources/js/router.js    → 画面遷移の設定

【データベース】
  database/migrations/   → テーブル設計図（36テーブル）
  database/seeders/      → 初期データ
  database/factories/    → テストデータ生成

【テスト】
  tests/Feature/         → 統合テスト（47ファイル）
  tests/Unit/            → 単体テスト（9ファイル）

【ドキュメント】
  docs/                  → 困ったらここ！
```

🐘得意げ「どうや！これで迷わんやろ？さすガネーシャや！✨」

👩‍💻「確かにスッキリ整理されてて分かりやすいです。ありがとうございます！」

👩‍💻「...でも結局、ガネーシャが設計したわけじゃないですよね？」

🐘焦り「う...ま、まぁワシが**インスピレーションを与えた**ということにしといてくれ...」

👩‍💻「はいはい（笑）」

🐘決めポーズ「ほな最後はいつものやつや！はい、Oh, My God!! 🙏✨」

🐘ボケをかます「...あ、そうや。ええこと教えたったんやから、お供えもんの**あんみつ**🍨よろしゅう頼むで〜！」

👩‍💻「出た、毎回それ（笑）」
