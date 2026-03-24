-- 시티 데이터탐정 사용 로그 테이블
CREATE TABLE IF NOT EXISTS bot_usage_log (
    id           SERIAL PRIMARY KEY,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id      VARCHAR(50)  NOT NULL,          -- Slack 사용자 ID (예: U012AB3CD)
    channel      VARCHAR(50),                    -- 채널 ID (DM이면 DM 채널 ID)
    channel_type VARCHAR(20)  NOT NULL,          -- 'dm' | 'channel'
    question     TEXT,                           -- 사용자가 보낸 질문
    answer       TEXT,                           -- 봇이 답한 내용
    duration_ms  INTEGER                         -- 응답 소요 시간 (밀리초)
);

-- 자주 쓸 조회를 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_bot_usage_log_created_at ON bot_usage_log (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_bot_usage_log_user_id    ON bot_usage_log (user_id);
