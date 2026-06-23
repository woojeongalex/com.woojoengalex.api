# 클린 아키텍처 & SOLID (Robert C. Martin)

> 백엔드 허브 → `woojeongai/CLAUDE.md`

**Cursor 연동:** 저장소 루트 `.cursorrules` · `backend/apps/**` 작업 시 본 문서를 따른다.  
**우선순위:** `docs/` 본문 > `.cursor/rules/*.mdc` > `.cursorrules` 요약.

---

## 1. 의존성 규칙 (Dependency Rule)

- 소스 코드 의존성은 **안쪽(고수준 정책)** 으로만 향한다.
- **Entities / Domain** 은 바깥 계층을 알지 못한다. ORM·FastAPI·HTTP 스키마·프레임워크 import 금지.

## 2. 4대 계층

| 계층 | 역할 | 금지 |
|------|------|------|
| **Entities** | 순수 도메인·비즈니스 규칙 | 프레임워크, ORM, 외부 DTO |
| **Use Cases** | 애플리케이션 흐름·오케스트레이션 | ORM 모델·Request 객체 직접 수신 |
| **Interface Adapters** | Controller, Presenter, Repository 구현 | Use Case에 ORM/HTTP 타입 누수 |
| **Frameworks & Drivers** | FastAPI, DB, UI | 비즈니스 규칙 |

## 3. Ports & Adapters (DIP)

- **Port(Protocol)** 는 `app/ports/` 에 정의한다.
- **Adapter 구현** 은 `adapter/inbound|outbound/` 에 둔다.
- Use Case / Entity 경계에서는 **Domain Entity 또는 `app/dtos/`** 만 사용한다.
- HTTP·DB 변환은 **Adapter 경계** 에서 1회 수행한다.

## 4. 디렉터리 (Titanic 예시)

```
titanic/
  domain/entities/          # [Entities]
  app/dtos/                 # 애플리케이션 DTO (Use Case 입출력)
  app/ports/input/          # 입력 Port (JamesUseCase, WalterUseCase)
  app/use_cases/            # *_interactor (업무 오케스트레이션 · input Port 구현)
  app/ports/output/         # 출력 Port (JamesRepositoryPort, WalterRepositoryPort)
  adapter/inbound/api/      # [Inbound Adapters] Controller·HTTP 스키마
  adapter/outbound/pg/      # [Outbound Adapters] Repository·ORM
  app/factories/            # [Use Cases] Abstract Factory (인터페이스)
  adapter/outbound/factories/  # Concrete Factory (PG·In-Memory 등)
```

### Friday13th (인증)

```
friday13th/
  domain/entities/friday13th.py     # UserAccount
  app/dtos/auth_result.py
  app/ports/input/signup_use_case.py
  app/use_cases/signup_Interactor.py
  app/ports/output/signup_repository_port.py
  adapter/inbound/api/v1/signup_router.py
  adapter/outbound/pg/signup_pg_repository.py
  adapter/outbound/orm/user_model.py   # users · bcrypt
```

- `backend/main.py`는 `signup_router`만 `include_router` (인라인 `/api/auth/*` 중복 금지).
- Use Case·Port는 `app/dtos`·domain만; HTTP 스키마 변환은 router·`adapter/inbound/api/schemas`.

### Inbound v1 라우터 (Titanic · 클린 기준)

**스켈레톤 정본:** `adapter/inbound/api/v1/andrews_blueprint_router.py` — 라우터 파일은 **HTTP 경계만** 둔다.

| 단계 | 예시 | 라우터에 둘 것 |
|------|------|----------------|
| 스텁 | `andrews_blueprint_router`, `hartley_violin_router` | `APIRouter(prefix, tags)` + `@router.get/post` 시그니처. 미구현은 `pass` 또는 501 |
| Thin (권장) | `walter_router` | `Depends(get_*_use_case)` + `handlers.*` 한 줄 위임. **Port 타입**만 import |
| 정적 메타 | `rose_router` | DB 없는 스키마·상수 응답만 (예외적으로 router에 매핑 가능) |

**라우터 금지:** `AsyncSession` / `get_db` / `select` / Repository / Use Case 구현 / 비즈니스 분기·반복.  
**조립:** `adapter/inbound/api/deps/` — `get_db` + PG Repository + Interactor.  
**예외·DB 오류:** `adapter/inbound/api/handlers/` — `SQLAlchemyError` → HTTP는 handler 또는 `run_with_db_guard` 패턴.

```python
# 스켈레톤 (andrews) — 기능 추가 전
andrews_blueprint_router = APIRouter(prefix="/api/andrews/blueprint", tags=["andrews-blueprint"])

@andrews_blueprint_router.get("/")
async def get_andrews_blueprint():
    pass  # 구현 시: handler / UseCase 로 위임만 추가
```

```python
# Thin 완성 (walter) — 라우터 목표 형태
@walter_router.get("/passengers", response_model=WalterPassengerPageResponse)
async def read_walter_passengers(..., walter: WalterUseCase = Depends(get_walter_use_case)):
    return await handle_walter_read(request, source_file, page, size, walter)
```

`friday13th`의 `signup_router` / `login_router`도 동일: `Depends(get_*_use_case)` + handler, DB import 없음.

### Abstract Factory (Titanic)

- **추상:** `app/factories/titanic_use_case_factory.py` — `TitanicUseCaseFactory`가 `JamesUseCase`·`WalterUseCase` 패밀리를 생성.
- **구현:** `adapter/outbound/factories/pg_titanic_use_case_factory.py` — Neon/PG Repository를 묶어 주입.
- **조립:** `adapter/inbound/api/deps/titanic_deps.py` — FastAPI `Depends(get_titanic_use_case_factory)`.
- **Port ABC**는 `ports/input`·`ports/output`. **구현**은 `*_interactor`(input 계약), `*_pg_repository`(output 계약).

### 흐름 로그 (Titanic)

- `titanic_flow_log`는 **실행되는 adapter·use case만** 기록: `inbound` → `usecase` → `outbound`.
- `ports/input`·`ports/output`은 추상 계약이라 **로그 레이어로 쓰지 않음** (`input`/`output` 태그 금지).
- `titanic_flow_log`에 잘못된 layer를 넘기면 `ValueError`로 차단.

## 5. SOLID 원칙

클린 아키텍처의 Ports/Adapters·의존성 규칙은 아래 SOLID를 **구체화**한다. 코드·리뷰 시 각 변경이 어느 원칙을 지키는지(또는 위반하는지) 확인한다.

### S — Single Responsibility Principle (단일 책임)

- 클래스·모듈은 **변경 이유가 하나**여야 한다.
- **적용:** Router는 HTTP·검증·매핑만, Use Case는 애플리케이션 규칙만, `*_pg_repository`는 영속화만.
- **금지:** 한 클래스에 CSV 파싱 + DB 저장 + 응답 포맷 + 로깅 정책을 모두 넣기.
- **KISS:** 한 줄만 위임하는 Controller/Service는 만들지 않거나, 검증·매핑 역할이 있을 때만 둔다 (`BACKEND_RULES.md`).

### O — Open/Closed Principle (개방-폐쇄)

- 동작 **확장**은 열고, 기존 코드 **수정**은 닫는다.
- **적용:** 새 저장소·외부 API는 `JamesRepositoryPort` 등 **새 Adapter 구현**으로 추가. Use Case 본문은 Port 시그니처가 같으면 수정 최소화.
- **금지:** Use Case 안에서 `if db_type == "neon"` 분기로 저장 방식을 바꾸기.

### L — Liskov Substitution Principle (리스코프 치환)

- Port(Protocol)를 구현한 Adapter는 **호출자가 기대하는 계약**을 깨지 않는다.
- **적용:** Mock/In-Memory Repository를 실제 PG Repository 자리에 넣어도 Use Case 테스트가 동일하게 통과.
- **금지:** Port 메서드가 예외 없이 `None`만 반환하거나, 성공 시 반환 타입·필드 의미를 구현체마다 다르게 하기.

### I — Interface Segregation Principle (ISP, 인터페이스 분리)

**한 줄:** 클라이언트(호출자)는 **자기가 쓰는 메서드만** 담긴 인터페이스에만 의존한다. 쓰지 않는 메서드를 끼워 넣은 **Fat Interface** 는 금지.

#### 1. Fat / Polluted Interface 금지

- 여러 역할·클라이언트를 한 ABC/Protocol에 몰아넣지 않는다.
- 인터페이스는 **한 가지 응집된 행위**(쓰기 전용, 읽기 전용, 업로드 입력 전용 등)만 표현한다.

#### 2. 클라이언트 중심 분리

- 구현체가 메서드를 **비워 두거나** (`pass`), **NotImplemented**, **항상 빈 값 반환** 하면 ISP 위반 신호다.
- 그 메서드를 인터페이스에서 **분리**하고, 필요한 클라이언트만 새 Port를 의존하게 한다.
- 기능 추가 시 "기존 Fat Interface에 메서드 하나 더"보다 **Port 경계를 먼저** 검토한다.

#### 3. 상속보다 작은 인터페이스 조합

- `AllInOneRepository` 식 대형 베이스 ABC 대신, `JamesRepositoryPort` + `WalterRepositoryPort` 처럼 **역할별 Port**를 둔다.
- 한 클래스가 여러 **작은** Port를 구현하는 것은 허용(각 Port 모두 실제로 사용할 때만).

#### Titanic 적용 예

| Port | 포함 | 제외 (다른 Port로) |
|------|------|-------------------|
| `JamesUseCase` (`ports/input/james_use_case.py`) | `upload` | `read_passengers` |
| `JamesRepositoryPort` | `upload` | 조회·페이지네이션 |
| `WalterUseCase` (`ports/input/walter_use_case.py`) | `read_passengers` | 업로드·전체 replace |
| `WalterRepositoryPort` | `read_passengers` | 업로드·`list_paginated` |
| `JamesInteractor` / `WalterInteractor` 등 | input Port 구현 (usecase) | Router가 output Port 직접 호출 금지 |

#### ISP 위반 체크 (코딩·리뷰 전)

1. 이 인터페이스를 구현하는 클래스가 **안 쓰는 메서드**가 있는가?
2. Router/Use Case가 Port 메서드 중 **일부만** 호출하는데 나머지가 붙어 있는가?
3. "나중에 쓸 것 같아서" 넣은 메서드는 없는가? → 있으면 분리 제안 **후** 구현.

#### 금지

- `TitanicRepository` 에 upload + read + train + 통계 CRUD 한곳에 선언.
- James 구현체에 `list_paginated` 를 `return []` 로만 두기.
- Input Port와 Output Port를 하나의 `TitanicPort` 로 합치기.

### D — Dependency Inversion Principle (의존성 역전)

- 고수준(Use Case)은 저수준(DB, HTTP)에 의존하지 않고, **둘 다 추상(Port)** 에 의존한다.
- **적용:** `JamesUseCase`는 `JamesRepositoryPort`만 알고, `JamesPgRepository`는 `adapter/`에서 조립(`titanic_deps.py`).
- **금지:** Use Case에서 `from titanic.adapter.outbound.pg import ...` 로 구체 클래스 import.

### SOLID ↔ 클린 아키텍처 매핑

| SOLID | 클린 아키텍처에서의 대응 |
|-------|-------------------------|
| SRP | 계층별 책임 분리 (§2) |
| OCP | Port 추가·Adapter 교체 |
| LSP | Port 구현체 치환 가능 |
| ISP | 입력/출력 Port 분리 |
| DIP | §3 Ports & Adapters, §1 의존성 규칙 |

## 6. 코드 작성·리뷰 체크리스트

1. **계층 준수:** Use Case가 `adapter.inbound` 스키마를 import 하면 위반 → 즉시 경고·수정.
2. **SOLID·ISP:** Fat Interface·미사용 abstract 메서드·Use Case→Adapter import 여부 확인. 위반 시 분리안을 먼저 제시.
3. **레이어 표기:** 리뷰·PR 설명에 `[Layer: Use Cases]` 등 명시.
4. **테스트:** Use Case는 In-Memory Mock Repository로 단위 테스트 가능해야 한다 (LSP·DIP).
5. **KISS:** pass-through Controller/Service·과도한 추상화는 `BACKEND_RULES.md` 와 동일하게 지양.

## 7. 참고

- 백엔드 공통: `BACKEND_RULES.md`
- Titanic ERD: `TITANIC_ERD.md`
