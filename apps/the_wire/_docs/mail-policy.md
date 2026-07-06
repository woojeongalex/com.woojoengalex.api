"""
# Gmail → Pub/Sub → n8n → FastAPI 실시간 수신 런북
# 프로젝트: woojeongalex.cloud / the_wire 앱 (2026-07-01 기준)

## 0. 아키텍처

    Gmail 새 메일
        │  (historyId 알림 Push)
        ▼
    Google Cloud Pub/Sub  (gmail-push-topic)
        │  (Push 구독 → 공개 HTTPS)
        ▼
    Cloudflare Tunnel  (localhost:5678 → https://xxxx.trycloudflare.com)
        │
        ▼
    n8n Webhook 노드  (POST /webhook/gmail-push)
        │  historyId만 도착 → Gmail API 재조회
        ▼
    n8n Gmail 조회 노드  (메시지 1건 pull)
        │
        ▼
    n8n HTTP Request  →  POST http://host.docker.internal:8000/api/the-wire/inbox
        │
        ▼
    FastAPI InboxInteractor  →  wire_inbox 테이블 (pgvector_container, port 5432)

## 1. 현재 구현 완료된 백엔드 레이어

    [Router]      the_wire/adapter/inbound/api/v1/inbox_router.py
                      POST /api/the-wire/inbox  <- n8n이 여기로 전송
                      GET  /api/the-wire/inbox  <- 프론트엔드 받은 메일함

    [Schema]      the_wire/adapter/inbound/api/schemas/inbox_schemas.py
                      ReceiveMailRequest { sender, subject, body }
                      InboxMailResponse  { id, sender, subject, body, received_at, is_read }
                      InboxListResponse  { mails: [...] }

    [Mapper]      the_wire/adapter/inbound/api/mappers/inbox_mapper.py
    [Interactor]  the_wire/app/use_cases/inbox_interactor.py
    [Repository]  the_wire/adapter/outbound/repositories/inbox_pg_repository.py
    [ORM]         the_wire/adapter/outbound/orm/inbox_model.py  (wire_inbox 테이블)
    [Provider]    the_wire/dependencies/inbox_provider.py

    ※ main.py에 이미 inbox_router 포함, InboxBase.metadata.create_all 실행 중

## 2. 기존 n8n 워크플로우 현황

    파일: n8n_gmail_inbox_workflow.json  (폴링 방식, 아직 Push 전환 안 됨)
    컨테이너: n8n_container (port 5678, docker-compose로 실행 중)
    기존 발송 워크플로우: the_wire Gmail Agent  <- 건드리지 말 것

## 3. 설정 순서

Step 1 — Cloudflare Tunnel 설치 (Windows)
    # PowerShell (관리자)
    winget install --id Cloudflare.cloudflared

    # 터널 실행 (n8n 포트 공개)
    cloudflared tunnel --url http://localhost:5678

    # 출력 예시:
    #   https://rough-cherry-1234.trycloudflare.com  <- 이 URL 복사
    #
    # 주의: Quick Tunnel은 프로세스 재시작 시 URL 바뀜
    # 영구 URL이 필요하면 Named Tunnel 사용:
    #   cloudflared tunnel login
    #   cloudflared tunnel create the-wire
    #   cloudflared tunnel route dns the-wire n8n.woojeongalex.cloud

Step 2 — n8n Webhook 노드 생성
    1) http://localhost:5678 접속
    2) New Workflow 생성 → 이름: "the_wire Gmail Inbox Push"
    3) 노드 추가: Webhook
           Method    : POST
           Path      : gmail-push
           Respond   : Immediately
    4) 최종 공개 URL:
           https://xxxx.trycloudflare.com/webhook/gmail-push

Step 3 — Google Cloud Pub/Sub 설정
    1) https://console.cloud.google.com → Pub/Sub API 활성화
    2) 토픽 생성
           이름: gmail-push-topic
    3) 토픽에 Publisher 권한 부여
           주 구성원: gmail-api-push@system.gserviceaccount.com
           역할     : Pub/Sub 게시자 (Pub/Sub Publisher)
    4) Push 구독 생성
           구독 ID       : gmail-push-sub
           전송 유형     : Push
           엔드포인트 URL: https://xxxx.trycloudflare.com/webhook/gmail-push

Step 4 — Gmail watch 등록 (1회 실행)
    n8n -> 새 HTTP Request 노드 (1회성 트리거용):
        Method  : POST
        URL     : https://gmail.googleapis.com/gmail/v1/users/me/watch
        Auth    : Gmail OAuth2  (기존 the_wire Gmail Agent 크레덴셜 재사용 가능)
        Body (JSON):
            {
                "topicName": "projects/<PROJECT_ID>/topics/gmail-push-topic",
                "labelIds": ["INBOX"]
            }

    성공 응답:
        { "historyId": "1234567", "expiration": "1751234567890" }
        ※ expiration = 약 7일 후 Unix 밀리초 → 갱신 필요

Step 5 — n8n 메인 워크플로우 구성
    [Webhook 노드]  POST /webhook/gmail-push
        ↓ (Pub/Sub 페이로드: data 필드가 base64 인코딩된 {emailAddress, historyId})
    [Gmail 조회 노드]  (Gmail > Get Many > 최신 안 읽은 1건)
        ↓
    [HTTP Request 노드]
        Method  : POST
        URL     : http://host.docker.internal:8000/api/the-wire/inbox
        Headers : Content-Type: application/json
        Body:
            {
                "sender" : "={{ $json.from }}",
                "subject": "={{ $json.subject }}",
                "body"   : "={{ $json.text ?? $json.snippet ?? '' }}"
            }

    ※ 기존 n8n_gmail_inbox_workflow.json은 폴링 방식
       Push 전환 시 Gmail Trigger 노드를 위 Webhook 노드로 교체

Step 6 — watch 자동 갱신 (7일 만료 대응)
    n8n -> 별도 워크플로우:
        [Schedule Trigger]  매일 새벽 3시
            ↓
        [HTTP Request]  Step 4와 동일 (watch 재등록)

## 4. Pub/Sub 페이로드 구조

    Pub/Sub -> n8n Webhook이 받는 실제 JSON:
    {
        "message": {
            "data": "<base64: {\"emailAddress\":\"you@gmail.com\",\"historyId\":\"1234\"}>",
            "messageId": "...",
            "publishTime": "2026-07-01T00:00:00Z"
        },
        "subscription": "projects/PROJECT_ID/subscriptions/gmail-push-sub"
    }

    ※ data를 base64 디코딩해도 historyId만 있음 → 실제 메일 내용은 Gmail API 재조회 필수

## 5. 비용 정리

    서비스              | 비용
    --------------------|-------
    n8n 셀프호스팅      | 무료 (n8n_container 이미 운영 중)
    Gmail API           | 무료
    Pub/Sub             | 무료 (월 10GiB 한도, 실사용 수 KB)
    Cloudflare Tunnel   | 무료 (Quick Tunnel 기준)
    pgvector DB         | 무료 (pgvector_container 이미 운영 중)
    Google Cloud 프로젝트| 무료 (기존 OAuth 설정 재사용 시)

## 6. 트러블슈팅

    증상                               | 원인 / 조치
    -----------------------------------|--------------------------------------------
    Webhook URL 404                    | n8n 워크플로우 Active 여부 확인
    cloudflared 재시작 후 Push 안 옴   | Pub/Sub 구독 엔드포인트 URL 업데이트 필요
    watch expiration 지남              | Step 6 Schedule Trigger 미작동 → 수동 재등록
    n8n Gmail 조회 0건                 | Gmail OAuth2 토큰 만료 → 크레덴셜 재인증
    FastAPI 422 Unprocessable Entity   | sender/subject/body 필드명 오타 확인
    wire_inbox 테이블 없음             | 서버 재시작하면 InboxBase.create_all 자동 생성
    포트 충돌 (8000 다중 실행)         | Get-Process python | Stop-Process -Force 후 재시작

## 7. 폴링 vs Push 비교

    방식   | 지연      | 비용    | 복잡도 | 적합 상황
    -------|-----------|---------|--------|---------------------------
    폴링   | 1~5분     | 무료    | 낮음   | 프로토타입·개발 테스트
    Push   | 수 초     | 무료    | 중간   | 프로덕션·실시간 요구 시
    ※ 현재 n8n_gmail_inbox_workflow.json = 폴링 방식 (1분마다)
"""

# ──────────────────────────────────────────────
# 프로젝트 내 관련 파일 경로 (참조용)
# ──────────────────────────────────────────────

RELATED_FILES = {
    "ORM"           : "the_wire/adapter/outbound/orm/inbox_model.py",
    "DTO"           : "the_wire/app/dtos/inbox_dto.py",
    "InputPort"     : "the_wire/app/ports/input/inbox_use_case.py",
    "OutputPort"    : "the_wire/app/ports/output/inbox_repository_port.py",
    "Interactor"    : "the_wire/app/use_cases/inbox_interactor.py",
    "Repository"    : "the_wire/adapter/outbound/repositories/inbox_pg_repository.py",
    "Schema"        : "the_wire/adapter/inbound/api/schemas/inbox_schemas.py",
    "Mapper"        : "the_wire/adapter/inbound/api/mappers/inbox_mapper.py",
    "Router"        : "the_wire/adapter/inbound/api/v1/inbox_router.py",
    "Provider"      : "the_wire/dependencies/inbox_provider.py",
    "n8n workflow"  : "n8n_gmail_inbox_workflow.json",
}

ENDPOINTS = {
    "수신 저장"    : "POST http://localhost:8000/api/the-wire/inbox",
    "받은 메일 조회": "GET  http://localhost:8000/api/the-wire/inbox",
}

N8N_BACKEND_URL   = "http://host.docker.internal:8000/api/the-wire/inbox"
N8N_WEBHOOK_PATH  = "/webhook/gmail-push"
PUBSUB_TOPIC      = "gmail-push-topic"
PUBSUB_SUB        = "gmail-push-sub"
GMAIL_WATCH_LABEL = "INBOX"
