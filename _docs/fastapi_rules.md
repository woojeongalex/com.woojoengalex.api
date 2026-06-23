# FastAPI 규칙 & 초기 설정

> 백엔드 허브 → `woojeongai/CLAUDE.md`  
> **자동 적용:** `backend/.cursorrules` → [BACKEND_RULES.md](../Backend/BACKEND_RULES.md)  
> **인덱스:** [DevOPs README](../README.md)

---

## 1. 환경 설정 (PowerShell)

```powershell
cd C:\Users\hi\Documents\tjwatson-cloud

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]" pandas
pip freeze > requirements.txt
```

활성화가 막힐 경우 (세션 한정):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 고정 규칙

- 터미널 열면 항상 루트로 이동 후 `.venv` 활성화
- 패키지 추가·업데이트는 루트에서만 수행
- 변경 후 항상 `pip freeze > requirements.txt` 갱신
- 다른 PC/CI 환경 동기화: `pip install -r requirements.txt`

> **한 줄 결론:** 루트 `.venv` + 루트 `requirements.txt` 만 사용

---

## 2. 초기 코드 — `james.py`

```python
from fastapi import FastAPI, Query

from .walter import Walter

app = FastAPI(title="Titanic API")


@app.get("/")
def health_check():
    return {"message": "제인스가 메인이다", "docs": "/docs"}

@app.get("/data")
def read_titanic_preview():
    w = Walter()
    return w.get_data()

@app.get("/titanic/preview")
def preview(limit: int = Query(default=10, ge=1, le=100)):
    w = Walter()
    return {"rows": w.get_data(limit=limit)}


if __name__ == "__main__":
    import uvicorn

    print("제임스가 메인이다. (uvicorn)")
    uvicorn.run("james:app", host="127.0.0.1", port=8000, reload=True)
```

### 엔드포인트 요약

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 헬스 체크 |
| `GET` | `/data` | 전체 데이터 반환 |
| `GET` | `/titanic/preview` | 미리보기 (limit: 1~100, 기본값 10) |

### 실행

```bash
python james.py
# 또는
uvicorn james:app --host 127.0.0.1 --port 8000 --reload
```

API 문서: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
