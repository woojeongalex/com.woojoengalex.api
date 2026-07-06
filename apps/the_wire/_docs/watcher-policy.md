# [Specification] Multi-Agent System Test Harness Specification

## 1. System Overview & Architecture Context

본 시스템은 허브 앤 스포크(Hub-and-Spoke) 및 온톨로지 기반의 거대 비즈니스 ERP 멀티 에이전트 아키텍처이다.

- **최고 사령탑 (Hub / Brain)**: `core/lol/t1_mid_faker_orchestrator.py`
  초거대 AI 모델(EXAONE)이 상주하는 최고 권한의 오케스트레이터 에이전트.
- **온톨로지 버스 (Ontology Hub)**: `star_craft/`
  전사 데이터 흐름, 엔티티 관계(Ontology) 및 전사 컨텍스트를 총괄하는 데이터 허브 버스.
- **커뮤니케이션 스포크 (Communication Spoke)**: `the_wire/`
  외부 채널(Email, Gmail Inbox, Telegram 등)과의 소통 및 인바운드 이벤트를 전담하는 스포크.
- **기타 스포크 (Spokes)**: `titanic/`, `silicon_valley/` 등 (ERP의 개별 도메인 파트)

## 2. Agent Core Logic & Routing Criteria

외부 커뮤니케이션 채널을 통해 인입되는 이벤트는 비즈니스 중요도 및 의도(Intent)에 따라 다음과 같이 라우팅된다.

- **Case A (일반 업무)**: 중요 거래처가 아니거나 단순 문의인 경우
  ➔ `the_wire` 내부의 `InboxInteractor`가 자체적으로 컨텍스트를 소화하여 처리 및 종결.
- **Case B (중요/에스컬레이션 업무)**: 중요 거래처이거나 자동 보고서 생성을 요청하는 경우
  ➔ 상위 온톨로지 버스인 `star_craft`를 경유하여 최고 에이전트인 **페이커(Faker / EXAONE)**에게 격상(Escalation). 페이커가 전사 ERP 데이터를 취합하여 최종 보고서를 생성하고 하향 전달.

## 3. Watson (Watcher Hub / Entry Point) 역할 정의

`the_wire/adapter/inbound/` 레이어에 위치한 **왓슨(Watson)**은 본 테스트 하네스의 핵심 검증 대상이자 인바운드 게이트웨이이다.
왓슨은 단순한 라우터가 아닌 **'Triage Nurse(초진 및 분류 관문)'** 역할을 수행한다.

### 왓슨의 핵심 메커니즘

1. **감시 및 후킹 (Watch & Hook)**: Gmail Push(`inbox_router`), n8n webhook 등에서 인바운드 이벤트를 낚아챔.
2. **1차 분류 및 조율 (Validation & Triage)**: 발신자(중요 거래처 여부)와 본문(보고서 요청 의도)을 빠르게 분석.
3. **컨텍스트 스위칭 및 라우팅 (Routing Decision)**:
   - 일반 메일 ➔ `InboxInteractor`(내부 종결) 호출.
   - 중요/보고서 메일 ➔ `star_craft` 온톨로지 버스로 이벤트 발행 → `FakerOrchestrator` 최종 활성화.

## 4. 실제 파일 매핑 (woojeongai 기준)

| 역할 | 실제 파일 경로 |
|------|---------------|
| 최고 사령탑 (Faker) | `core/lol/t1_mid_faker_orchestrator.py` |
| 인바운드 게이트웨이 (Watson) | `the_wire/adapter/inbound/api/v1/inbox_router.py` |
| 일반 처리 (Holmes) | `the_wire/app/use_cases/inbox_interactor.py` |
| 온톨로지 버스 | `star_craft/hub/` |
| 임베딩 저장 | `the_wire/adapter/outbound/repositories/inbox_pg_repository.py` |
| 테스트 하네스 | `the_wire/_docs/harness/watson_test_harness.py` |

## 5. Test Harness Implementation Plan

### [지시사항 1] 가상 이벤트 생성기

- **Scenario 1**: 일반 거래처의 단순 인사/일반 문의 메일 인입
- **Scenario 2**: VIP 거래처(`important_client: true`)의 "분기 실적 자동 보고서 발행 요망" 메시지 인입

### [지시사항 2] Watson 라우팅 인터셉터

- Scenario 1 → `InboxInteractor.receive()` 호출 후 종결
- Scenario 2 → `star_craft` 이벤트 버스 발행 → `FakerOrchestrator.invoke()` 에스컬레이션

### [지시사항 3] 하네스 대시보드 및 Narrative Log

- Watson ➔ Holmes 또는 Watson ➔ StarCraft ➔ Faker 전체 여정을 콘솔 추적 서사 로그로 출력
