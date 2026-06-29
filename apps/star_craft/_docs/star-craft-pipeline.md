# star_craft Hub — DB 파이프라인 전략

## 1. 개요

`star_craft`는 스타 토폴로지의 **중앙 허브**다.
모든 에이전트는 hub를 통해서만 지식을 읽고 쓴다.
hub가 접속하는 외부 저장소는 **Graph DB(Neo4j)** 와 **Vector DB(Qdrant)** 두 가지다.

```
[RAG 에이전트]  [Faker]  [실행 에이전트]
       ↕           ↕           ↕
          star_craft Hub (FastAPI)
               ↕           ↕
           Neo4j        Qdrant
         (온톨로지)     (임베딩)
```

---

## 2. 저장소 역할 분담

| 저장소 | 용도 | 저장 대상 |
|--------|------|-----------|
| **Neo4j** | 온톨로지 그래프 | 개념 노드, 관계 엣지, Race 매핑(Zerg·Terran·Protoss) |
| **Qdrant** | 벡터 임베딩 | 문서 청크, 시맨틱 검색용 임베딩 |

---

## 3. Docker 서비스 추가 계획

현재 `docker-compose.yaml`에 Neo4j, Qdrant가 없다.
아래 서비스를 추가해야 한다.

### Neo4j (Graph DB)
- 이미지: `neo4j:5`
- 포트: `7474` (Browser UI), `7687` (Bolt 프로토콜)
- 볼륨: `neo4j_data`
- 환경변수: `NEO4J_AUTH=neo4j/<비밀번호>`

### Qdrant (Vector DB)
- 이미지: `qdrant/qdrant:latest`
- 포트: `6333` (HTTP REST API), `6334` (gRPC)
- 볼륨: `qdrant_data`

---

## 4. star_craft 클린 아키텍처 파이프라인

### 4.1 Neo4j 파이프라인

```
adapter/inbound/api or mcp
        ↓
app/use_cases/*_interactor.py
        ↓  (output port 호출)
app/ports/output/*_graph_repository_port.py  ← ABC
        ↓
adapter/outbound/repositories/*_neo4j_repository.py  ← 구현체
        ↓
adapter/outbound/orm/*_node_model.py  ← Neo4j OGM 노드 정의
        ↓
Neo4j (Docker, bolt://localhost:7687)
```

### 4.2 Qdrant 파이프라인

```
adapter/inbound/api or mcp
        ↓
app/use_cases/*_interactor.py
        ↓  (output port 호출)
app/ports/output/*_vector_repository_port.py  ← ABC
        ↓
adapter/outbound/repositories/*_qdrant_repository.py  ← 구현체
        ↓
Qdrant (Docker, http://localhost:6333)
```

---

## 5. 레이어별 파일 네이밍 규칙

| 레이어 | 파일명 예시 |
|--------|-------------|
| Port (output) | `ontology_graph_repository_port.py` |
| Port (output) | `embedding_vector_repository_port.py` |
| Repository (Neo4j) | `ontology_neo4j_repository.py` |
| Repository (Qdrant) | `embedding_qdrant_repository.py` |
| ORM/Node Model | `concept_node_model.py` |
| Director | `star_craft_director.py` |
| DTO | `ontology_dto.py`, `embedding_dto.py` |

---

## 6. 연결 설정 위치

| 설정 | 위치 |
|------|------|
| Neo4j 접속 정보 | `woojeongai/.env` → `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` |
| Qdrant 접속 정보 | `woojeongai/.env` → `QDRANT_HOST`, `QDRANT_PORT` |
| 드라이버 초기화 | `woojeongai/core/` 또는 `star_craft/dependencies/` |

---

## 7. 개발 착수 순서

```
1. docker-compose.yaml에 Neo4j, Qdrant 서비스 추가
2. .env에 접속 정보 등록
3. domain/entities/ — 온톨로지 노드·관계 정의
4. app/ports/output/ — GraphRepositoryPort, VectorRepositoryPort ABC 작성
5. adapter/outbound/repositories/ — Neo4j, Qdrant 구현체 작성
6. dependencies/star_craft_director.py — DIP 조립
7. app/use_cases/ — 허브 인터랙터 작성
8. adapter/inbound/api, mcp — 에이전트 진입점 오픈
```
