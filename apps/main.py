"""FastAPI ASGI entry — `backend/apps`에서 `uvicorn main:app --reload` 실행용."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_APPS_DIR = Path(__file__).resolve().parent
_BACKEND_DIR = _APPS_DIR.parent

from dotenv import load_dotenv

load_dotenv(_BACKEND_DIR / ".env", override=True)

for _dir in (_APPS_DIR, _BACKEND_DIR):
    _entry = str(_dir)
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

def _load_backend_app():
    """`backend/main.py`의 `app`을 이 모듈로 노출 (이 파일과 이름 충돌 방지)."""
    module_name = "backend_main"
    main_path = _BACKEND_DIR / "main.py"
    spec = importlib.util.spec_from_file_location(module_name, main_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"FastAPI app을 불러올 수 없습니다: {main_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.app


app = _load_backend_app()
