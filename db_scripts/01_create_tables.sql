-- users テーブル
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
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

-- users.email にインデックスを追加
CREATE INDEX idx_users_email ON users(email);

-- social_accounts.provider_id にインデックスを追加
CREATE INDEX idx_social_accounts_provider_id ON social_accounts(provider_id);

-- login_attempts.user_id にインデックスを追加
CREATE INDEX idx_login_attempts_user_id ON login_attempts(user_id);

-- users テーブルにテストデータを挿入
INSERT INTO users (email, password_hash, role, settings) 
VALUES 
('teacher1@example.com', 'hashed_password_1', 'user', '{"theme": "dark"}'),
('admin@example.com', 'hashed_password_2', 'admin', '{"theme": "light"}');

-- mfa テーブルにテストデータを挿入
INSERT INTO mfa (user_id, secret_key, backup_codes) 
VALUES 
(1, 'abcdefg1234567', ARRAY['backup1', 'backup2', 'backup3']);

-- social_accounts テーブルにテストデータを挿入
INSERT INTO social_accounts (user_id, provider, provider_id, access_token) 
VALUES 
(1, 'google', 'google_user_123', 'example_access_token_1');

-- login_attempts テーブルにテストデータを挿入
INSERT INTO login_attempts (user_id, ip_address, success) 
VALUES 
(1, '192.168.1.1', TRUE),
(1, '192.168.1.2', FALSE);

