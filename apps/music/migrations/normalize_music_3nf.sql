-- Music 3NF: sing_evaluations 허브화 + vocal_recommendations → ai_vocal_analyses FK
-- 대상: PostgreSQL (Neon). 실행 전 백업 권장.
-- 신규 DB에서 `init_db` / create_all 만 쓰는 경우 이 파일은 생략 가능.

-- ---------------------------------------------------------------------------
-- 1) vocal_recommendations: AI FK 추가 및 백필
-- ---------------------------------------------------------------------------
ALTER TABLE vocal_recommendations
  ADD COLUMN IF NOT EXISTS ai_vocal_analysis_id BIGINT;

UPDATE vocal_recommendations vr
SET ai_vocal_analysis_id = sub.aid
FROM (
  SELECT vr2.id AS rid, a.id AS aid
  FROM vocal_recommendations vr2
  INNER JOIN user_vocal_recordings u ON u.sing_evaluation_id = vr2.sing_evaluation_id
  INNER JOIN ai_vocal_analyses a ON a.user_vocal_recording_id = u.id
) AS sub
WHERE vr.id = sub.rid
  AND (vr.ai_vocal_analysis_id IS NULL OR vr.ai_vocal_analysis_id = 0);

-- 백필 불가 행이 있으면 수동 정리 후 NOT NULL / FK 진행:
-- DELETE FROM vocal_recommendations WHERE ai_vocal_analysis_id IS NULL;

ALTER TABLE vocal_recommendations
  ALTER COLUMN ai_vocal_analysis_id SET NOT NULL;

ALTER TABLE vocal_recommendations
  ADD CONSTRAINT fk_vocal_recommendations_ai
  FOREIGN KEY (ai_vocal_analysis_id) REFERENCES ai_vocal_analyses(id)
  ON DELETE CASCADE;

ALTER TABLE vocal_recommendations DROP COLUMN IF EXISTS pitch_score_snapshot;
ALTER TABLE vocal_recommendations DROP COLUMN IF EXISTS rhythm_score_snapshot;
ALTER TABLE vocal_recommendations DROP COLUMN IF EXISTS vocal_grade_snapshot;

-- ---------------------------------------------------------------------------
-- 2) sing_evaluations: 이행 종속 제거 (세션은 허브만)
-- ---------------------------------------------------------------------------
ALTER TABLE sing_evaluations DROP COLUMN IF EXISTS catalog_song_id;
ALTER TABLE sing_evaluations DROP COLUMN IF EXISTS mr_search_list_id;
ALTER TABLE sing_evaluations DROP COLUMN IF EXISTS input_source;
ALTER TABLE sing_evaluations DROP COLUMN IF EXISTS pitch_score;
ALTER TABLE sing_evaluations DROP COLUMN IF EXISTS rhythm_score;
ALTER TABLE sing_evaluations DROP COLUMN IF EXISTS vocal_grade;
ALTER TABLE sing_evaluations DROP COLUMN IF EXISTS summary;
ALTER TABLE sing_evaluations DROP COLUMN IF EXISTS file_name;
ALTER TABLE sing_evaluations DROP COLUMN IF EXISTS duration_sec;
