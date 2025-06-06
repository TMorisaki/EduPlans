# EduPlans 仕様書

---

## 1. システム構成（アーキテクチャ）

### 1.1 構成要素

| レイヤー     | 技術要素                        | 内容                                       |
|--------------|----------------------------------|--------------------------------------------|
| フロントエンド | Next.js + Tailwind CSS          | 教師用UI。スマートフォンUIを重視。         |
| バックエンド   | FastAPI                         | API層、JWT認証、ユーザー管理、指導案管理    |
| データベース   | PostgreSQL                      | 永続化ストレージ。docker-composeで起動     |
| 開発環境     | Docker + docker-compose         | コンテナ化による環境の一元化               |
| 認証         | JWT + Hashing(passlib)          | パスワード認証、トークン発行               |
| 保留機能     | MFA、ソーシャルログイン、メール認証 | プロトタイピング段階では未実装              |

---

## 2. 機能一覧

### 2.1 ユーザー関連

- 登録（メール＋パスワード）
- ログイン（JWT発行）
- トークン検証
- MFA・ソーシャルログイン・メール認証は将来的に対応

### 2.2 指導案管理

- Markdownでの入力と保存
- フォーク（gitのような枝分かれ）
- 引用（元ノードの記録と引用数の加算）
- バージョンの一覧・差分確認

### 2.3 UI入力補助

- 独自Markdown記法
- スマホでは下部メニューから記法ボタン入力可

---

## 3. DBスキーマ

### users

| 列名           | 型               | 説明                   |
|----------------|------------------|------------------------|
| id             | SERIAL PRIMARY KEY | ユーザーID             |
| email          | VARCHAR(255)     | メールアドレス（ユニーク）|
| email_verified | BOOLEAN          | メール認証済みか        |
| password_hash  | VARCHAR(255)     | ハッシュ化されたパスワード |
| is_active      | BOOLEAN          | 有効なユーザーか        |
| mfa_enabled    | BOOLEAN          | MFA有効か              |
| role           | VARCHAR(50)      | ユーザーのロール        |
| settings       | JSONB            | ユーザー設定            |
| created_at     | TIMESTAMP        | 作成日時               |
| updated_at     | TIMESTAMP        | 更新日時               |

### plans

| 列名         | 型           | 説明             |
|--------------|--------------|------------------|
| id           | SERIAL       | プランID         |
| title        | TEXT         | 指導案タイトル     |
| unit_id      | INTEGER      | 単元マスタへの参照  |
| created_by   | INTEGER      | 作成ユーザーID     |
| created_at   | TIMESTAMP    | 作成日時          |

### plan_trees

| 列名         | 型           | 説明                      |
|--------------|--------------|---------------------------|
| id           | SERIAL       | ノードID                  |
| plan_id      | INTEGER      | 所属プランID              |
| parent_id    | INTEGER      | 親ノードID（NULLでルート） |
| content_md   | TEXT         | マークダウン本文           |
| goal         | TEXT         | 本時の目標                |
| period       | INTEGER      | 単元内での時数             |
| grade        | INTEGER      | 学年                      |
| created_by   | INTEGER      | 作成ユーザー              |
| created_at   | TIMESTAMP    | 作成日時                  |
| forked_from  | INTEGER      | フォーク元ノードID（NULL可）|
| citation_count | INTEGER    | 被引用数                  |

### units

| 列名        | 型        | 説明             |
|-------------|-----------|------------------|
| id          | SERIAL    | 単元ID           |
| name        | TEXT      | 単元名           |
| description | TEXT      | 補足説明（任意） |

---

## 4. Markdown記法（独自構文）

| プレフィックス | 意味                     | 表記例                            |
|----------------|--------------------------|-----------------------------------|
| -D             | 導入                     | -D 今日は何を学ぶか考えてみよう    |
| -MQ            | 主発問                   | -MQ なぜ○○が必要なのだろう？       |
| -Q             | 発問                     | -Q この図から何がわかりますか？    |
| -A             | 生徒の反応（予想）        | -A ○○という意見が出る             |
| -T             | 時間（00:00形式）        | -T 00:10                          |
| -S             | 教師の手立て             | -S 板書を通じて○○に気づかせる     |

---

## 5. UI仕様（スマホ対応）

- スマホでは画面下部に記法ボタンを配置（導入、主発問など）
- ボタンを押すと、Markdownエディタに記法が自動挿入される
- モバイルUIを意識した大きめのタップ領域、キーボード表示との干渉回避

---

## 6. ゲーミフィケーション要素

| 要素         | 説明                                           |
|--------------|------------------------------------------------|
| 引用数表示    | 他の指導案からのfork・引用数を表示              |
| バッジ        | 作成数・引用数・改善数などに応じてバッジを付与   |
| ランキング    | 指導案の人気や引用数によるランキングを表示       |
| スコア        | 活動に応じたスコア算出（プロフィールに表示）     |

# API設計（概要）

## 認証関連
- `/users/register`: 登録（重複メールチェック）
- `/users/login`: ログイン（JWT発行）
- `/users/me`: トークン検証・ユーザー情報返却

## 指導案関連（未実装予定）
- `/plans`: 一覧取得・登録
- `/plans/{id}`: 詳細取得
- `/plans/{id}/edit`: 詳細
- `/plans/{id}/fork`: 他人の指導案からブランチ作成
- `/plans/{id}/bookmark`: ブックマーク登録
- `/plans/{id}/cite`: 引用登録

# その他設計指針
- ユーザーの役割（role）により画面や操作権限を切り替える設計
- markdownベースの文書構造管理
- Git的なバージョン・ブランチ管理による指導案の発展と引用数の可視化
- 将来的なゲーミフィケーション（閲覧数、引用数、フォーク数など）
