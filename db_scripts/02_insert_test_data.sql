-- テストデータ挿入
INSERT INTO users (email, password_hash) 
VALUES ('testuser@example.com', 'hashed_password_123');

INSERT INTO mfa (user_id, secret_key, backup_codes) 
VALUES (1, 'abcdefg1234567', ARRAY['backup1', 'backup2', 'backup3']);

INSERT INTO social_accounts (user_id, provider, provider_id, access_token) 
VALUES (1, 'google', 'google_user_123', 'example_access_token');
