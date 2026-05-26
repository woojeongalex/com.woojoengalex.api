-- Instrument + Speech domains (PostgreSQL / Neon)
-- 신규 DB는 init_db(create_all)만으로도 생성 가능. 레거시는 본 파일 실행.

CREATE TABLE IF NOT EXISTS instrument_evaluations (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS instrument_recordings (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    instrument_evaluation_id BIGINT NOT NULL UNIQUE
        REFERENCES instrument_evaluations(id) ON DELETE CASCADE,
    instrument_id VARCHAR(32) NOT NULL,
    file_name VARCHAR(512) NOT NULL DEFAULT '',
    duration_sec INTEGER NOT NULL DEFAULT 0,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS instrument_tuning_analyses (
    id BIGSERIAL PRIMARY KEY,
    instrument_recording_id BIGINT NOT NULL UNIQUE
        REFERENCES instrument_recordings(id) ON DELETE CASCADE,
    analysis_engine VARCHAR(64) NOT NULL DEFAULT 'client_demo',
    tuning_accuracy INTEGER NOT NULL DEFAULT 0,
    pitch_deviation_cents INTEGER NOT NULL DEFAULT 0,
    summary VARCHAR(2048) NOT NULL DEFAULT '',
    string_readings JSONB NOT NULL DEFAULT '[]'::jsonb,
    analyzed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS speech_evaluations (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS speech_recordings (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    speech_evaluation_id BIGINT NOT NULL UNIQUE
        REFERENCES speech_evaluations(id) ON DELETE CASCADE,
    topic_id VARCHAR(64) NOT NULL,
    file_name VARCHAR(512) NOT NULL DEFAULT '',
    duration_sec INTEGER NOT NULL DEFAULT 0,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS speech_feedback_analyses (
    id BIGSERIAL PRIMARY KEY,
    speech_recording_id BIGINT NOT NULL UNIQUE
        REFERENCES speech_recordings(id) ON DELETE CASCADE,
    analysis_engine VARCHAR(64) NOT NULL DEFAULT 'client_demo',
    clarity_score INTEGER NOT NULL DEFAULT 0,
    pace_score INTEGER NOT NULL DEFAULT 0,
    tone_score INTEGER NOT NULL DEFAULT 0,
    summary VARCHAR(2048) NOT NULL DEFAULT '',
    feedback_points JSONB NOT NULL DEFAULT '[]'::jsonb,
    analyzed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_instrument_evaluations_user_id
    ON instrument_evaluations(user_id);
CREATE INDEX IF NOT EXISTS ix_instrument_recordings_user_id
    ON instrument_recordings(user_id);
CREATE INDEX IF NOT EXISTS ix_speech_evaluations_user_id
    ON speech_evaluations(user_id);
CREATE INDEX IF NOT EXISTS ix_speech_recordings_topic_id
    ON speech_recordings(topic_id);
