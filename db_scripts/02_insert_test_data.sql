
-- テストデータの挿入

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

-- units テーブルにテストデータを挿入
INSERT INTO units (name, subject, grade, description)
VALUES
('分数の足し算', '算数', '小3', '分数の計算を学ぶ単元'),
('電流と回路', '理科', '中1', '電流の基本原理を学ぶ');

-- plans テーブルにテストデータを挿入
INSERT INTO plans (title, unit_id, created_by)
VALUES 
('分数の足し算の指導案', 1, 1),
('電流と回路の指導案', 2, 2);

-- plan_tree テーブルにテストデータを挿入（初期バージョン）
INSERT INTO plan_tree (plan_id, parent_version_id, depth, description, grade, lesson_goal, lesson_hours, content, created_by)
VALUES 
(1, NULL, 0, '分数の理解を深める', '小3', '分数の加法を理解する', 3, '# 分数の指導内容...', 1),
(2, NULL, 0, '電流の基本を学ぶ', '中1', '電流の流れを理解する', 2, '# 電流の指導内容...', 2);

-- user_achievements テーブルにテストデータを挿入
INSERT INTO user_achievements (user_id, badge_name) 
VALUES 
(1, '初投稿バッジ'),
(2, '人気指導案バッジ');

-- plan_reviews テーブルにテストデータを挿入
INSERT INTO plan_reviews (plan_id, user_id, rating, review_text)
VALUES 
(1, 2, 5, 'とても分かりやすい指導案です！'),
(2, 1, 4, '応用問題がもう少しあるとよい');

-- user_poins テーブルにテストデータを挿入
INSERT INTO user_points (user_id, points)
VALUES 
(1, 50),
(2, 30);

-- monthly_awards テーブルにテストデータを挿入
INSERT INTO monthly_tawards (award_name, plan_id, user_id)
VALUES 
('今月のベスト指導案', 1, 1),
('トップレビュアー', NULL, 2);
