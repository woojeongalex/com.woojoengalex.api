# 백엔드 코딩 규칙 (FastAPI / IUEM)

> 백엔드 허브 → `woojeongai/CLAUDE.md`

**Cursor 자동 연동:** `backend/.cursorrules` → 본 문서.  
작업 루트: `backend/apps/` (`uvicorn main:app`).

---

## 구조 (KISS)

- **헥사고날·클린 아키텍처·SOLID:** `CLEAN_ARCHITECTURE.md` — Use Case는 `app/dtos`·`app/ports`만, HTTP/ORM은 `adapter/` 경계에서 변환. **ISP:** Fat Interface 금지, Input/Output Port 분리.
- **인증(auth):** `friday13th` — `signup_router` → `SignupUseCase` → `SignupInteractor` → `SignupRepositoryPort` → `SignupPgRepository` → `user_model`(bcrypt).
- **pass-through만** 하는 Interactor/Repository는 만들지 않거나, 검증·매핑 역할이 있을 때만.
- 라우트 등록: `backend/main.py`는 `include_router` 위주로 얇게, 비즈니스는 각 앱 `adapter/`·`app/use_cases/` 아래.

```
backend/
  main.py                    # include_router (auth·music·titanic 등)
  core/database.py           # init_db · get_db
backend/apps/
  friday13th/
    adapter/inbound/api/v1/signup_router.py   # /api/auth/*
    app/use_cases/signup_Interactor.py
    adapter/outbound/pg/signup_pg_repository.py
    adapter/outbound/orm/user_model.py        # UserEntity · bcrypt
  music/ · titanic/          # 동일 헥사고날 패턴 (CLEAN_ARCHITECTURE.md)
```

---

## 인증·보안

- 회원가입 `role`은 **서버에서 `"user"` 고정** (`SignupPgRepository.save_user`, 클라이언트 값 무시).
- 비밀번호·토큰·해시 **로그/print 금지** (DEBUG도 민감정보 노출 최소).
- `check-id` / `check-nickname`과 동일한 중복 검사를 **INSERT 전** `SignupInteractor`·`SignupPgRepository`에서 재검증.
- `ValueError` → `HTTPException`은 `signup_router` 한곳에서 일관 매핑 (409 중복, 401 로그인 실패, 422 검증).
- `.env`, `DATABASE_URL` 커밋 금지.

**API (프론트 프록시와 동일 경로):**

| 메서드 | 경로 |
|--------|------|
| POST | `/api/auth/signup` |
| POST | `/api/auth/login` |
| GET | `/api/auth/check-id` |
| GET | `/api/auth/check-nickname` |

---

## DB·비동기

- 엔티티 PK·컬럼명 규칙: `ENTITY_RULE.md` (정수 `id` PK).
- MR 검색·Neon 저장: `GET /api/songs/search?q=` → `music` **SearchUseCase** → `song_mr_search_lists`.
- 보컬 평가: `POST /api/music/sing-evaluation` → **EvaluationUseCase** → `sing_evaluations` 등 3NF, 스키마 정본 `evaluation_schemas`.
- 악기: `GET /api/music/instrument-catalog` · `POST /api/music/instrument-evaluation` → **InstrumentUseCase**.
- 스피치: `GET /api/music/speech-topics` · `POST /api/music/speech-evaluation` → **SpeechUseCase**.
- 추천: `POST` / `GET /api/music/vocal-recommendations` → **SuggestUseCase** → `vocal_recommendations`.
- 비디오 분석: `POST /api/music/analyze-video` → **VideoAnalysisUseCase** (DB 없음, 저장 시 보컬 경로 합류).
- `Depends(get_db)` + `async`/`await` 일관.
- Windows: `main.py` 또는 `database.py`에서 event loop 정책 **한 번만** 설정.
- 세션은 요청 단위; PG repository에서 commit/rollback 패턴 유지.

---

## 로깅

- AUTH·도메인 흐름: **레이어당 1줄** (동일 요청에 INFO 10줄 이상 금지). `signup_router`·use case·pg repository 로거명은 `logging_setup.py` 참고.
- 디버그 `print` 커밋 금지.

---

## 변경·리팩터

- 비즈니스 로직·스키마 깨지지 않게. diff 최소, 기존 import/스타일 유지.
- 패키지 추가 시 `backend/requirements.txt` 갱신 (`pip freeze`).

---

## 실행 (로컬)

```powershell
cd backend/apps
# venv 활성화 후
uvicorn main:app --reload
```

상세 venv 규칙: `docs/fastapi 전환 방법.md`

---

## 참고 파일

- `backend/main.py`
- `backend/apps/friday13th/adapter/inbound/api/v1/signup_router.py`
- `backend/apps/friday13th/app/use_cases/signup_Interactor.py`
- `backend/apps/friday13th/adapter/outbound/pg/signup_pg_repository.py`
- `backend/apps/friday13th/adapter/outbound/orm/user_model.py`

공통: `.cursor/rules/coding-standards.mdc`
