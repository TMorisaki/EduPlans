-- users テーブル
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    password_hash VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    role VARCHAR(50) DEFAULT 'user', -- ユーザーの役割（例: user, admin）
    settings JSONB DEFAULT '{}', -- ユーザー設定（JSON形式）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- mfa テーブル
CREATE TABLE mfa (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    secret_key VARCHAR(255) NOT NULL,
    backup_codes TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- social_accounts テーブル
CREATE TABLE social_accounts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,
    provider_id VARCHAR(255) NOT NULL UNIQUE,
    access_token TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE login_attempts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    ip_address VARCHAR(45), -- IPv4/IPv6アドレス
    success BOOLEAN, -- ログイン成功か失敗か
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 試行時刻
);

-- 指導案管理関連のテーブル

-- plans テーブル（指導案のオリジン情報）
CREATE TABLE plans (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    unit_id INT REFERENCES units(id) ON DELETE SET NULL,
    created_by INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- plan_tree テーブル（指導案のバージョン管理）
CREATE TABLE plan_tree (
    id SERIAL PRIMARY KEY,
    plan_id INT REFERENCES plans(id) ON DELETE CASCADE,
    parent_version_id INT REFERENCES plan_tree(id) ON DELETE SET NULL,
    depth INT NOT NULL,
    description TEXT,
    grade VARCHAR(50),
    lesson_goal TEXT,
    lesson_hours INT,
    content TEXT NOT NULL,
    reference_count INT DEFAULT 0,
    fork_count INT DEFAULT 0,
    created_by INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- units テーブル（単元マスタ）
CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    grade VARCHAR(50),
    description TEXT
);

-- ゲーミフィケーション関連のテーブル

-- user_achievements テーブル（バッジ管理）
CREATE TABLE user_achievements (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    badge_name VARCHAR(255),
    achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- plan_reviews テーブル（レビュー管理）
CREATE TABLE plan_reviews (
    id SERIAL PRIMARY KEY,
    plan_id INT REFERENCES plans(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- user_points テーブル（ユーザーポイント管理）
CREATE TABLE user_points (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    points INT DEFAULT 0
);

-- monthly_awards テーブル（毎月の指導案アワード）
CREATE TABLE monthly_awards (
    id SERIAL PRIMARY KEY,
    award_name VARCHAR(255),
    plan_id INT REFERENCES plans(id) ON DELETE SET NULL,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    month TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- plan_shares テーブル（指導案のシェア履歴）
CREATE TABLE plan_shares (
    id SERIAL PRIMARY KEY,
    plan_id INT REFERENCES plans(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- インデックスの作成
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_social_accounts_provider_id ON social_accounts(provider_id);
CREATE INDEX idx_login_attempts_user_id ON login_attempts(user_id);
CREATE INDEX idx_plan_tree_plan_id ON plan_tree(plan_id);
CREATE INDEX idx_plan_reviews_plan_id ON plan_reviews(plan_id);
CREATE INDEX idx_plan_shares_plan_id ON plan_shares(plan_id);
