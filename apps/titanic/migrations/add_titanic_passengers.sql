-- 타이타닉 CSV 업로드 저장 테이블 (신규 DB는 init_db create_all 로도 생성 가능)
CREATE TABLE IF NOT EXISTS titanic_passengers (
    id SERIAL PRIMARY KEY,
    source_file VARCHAR(255) NOT NULL,
    dataset_passenger_id VARCHAR(32) NOT NULL,
    survived VARCHAR(8) NOT NULL,
    pclass VARCHAR(8) NOT NULL,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(16) NOT NULL,
    age VARCHAR(32) NOT NULL,
    sib_sp VARCHAR(8) NOT NULL,
    parch VARCHAR(8) NOT NULL,
    ticket VARCHAR(64) NOT NULL,
    fare VARCHAR(32) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_titanic_passengers_source_file
    ON titanic_passengers (source_file);
CREATE INDEX IF NOT EXISTS ix_titanic_passengers_dataset_passenger_id
    ON titanic_passengers (dataset_passenger_id);
