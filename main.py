import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

import requests

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

_CURRENT_DIR = Path(__file__).resolve().parent
_APPS_DIR = _CURRENT_DIR / "apps"
for _path in (_CURRENT_DIR, _APPS_DIR):
    _entry = str(_path)
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

from logging_setup import configure_logging

configure_logging()

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from adapters.db_health_adapter import DbHealthAdapter
from adapters.openweather_adapter import CITY_ORDER, WEATHER_CITIES, OpenWeatherAdapter
try:
    from database import dispose_engine, get_db, init_db
except ModuleNotFoundError:
    from apps.database import dispose_engine, get_db, init_db
import titanic.adapter.outbound.orm.passenger_orm  # noqa: F401
import titanic.adapter.outbound.orm.booking_orm  # noqa: F401
import titanic.adapter.outbound.orm.passenger_rose_model_orm  # noqa: F401
import titanic.adapter.outbound.orm.passenger_jack_trainer_orm  # noqa: F401
import music.adapter.outbound.orm.ai_vocal_analysis_model  # noqa: F401
import music.adapter.outbound.orm.user_vocal_recording_model  # noqa: F401
import music.adapter.outbound.orm.evaluation_models  # noqa: F401
import music.adapter.outbound.orm.sing_model  # noqa: F401
import music.adapter.outbound.orm.suggest_model  # noqa: F401
import music.adapter.outbound.orm.instrument_evaluation_model  # noqa: F401
import music.adapter.outbound.orm.instrument_recording_model  # noqa: F401
import music.adapter.outbound.orm.instrument_tuning_analysis_model  # noqa: F401
import music.adapter.outbound.orm.speech_evaluation_model  # noqa: F401
import music.adapter.outbound.orm.speech_recording_model  # noqa: F401
import music.adapter.outbound.orm.speech_feedback_analysis_model  # noqa: F401
import music.adapter.outbound.orm.list_model  # noqa: F401
import friday13th.adapter.outbound.orm.user_model  # noqa: F401
from core.matrix.keymaker_api import get_keymaker
from music.adapter.inbound.api import music_router
from friday13th.adapter.inbound.api.v1 import login_router, signup_router
from titanic.adapter.inbound.api import titanic_router

logger = logging.getLogger(__name__)

keymaker = get_keymaker()

# primary 모델 실패(404·429) 시 순서대로 재시도
GEMINI_FALLBACK_MODELS = (
    "gemini-2.5-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash-8b",
)

class ChatRequest(BaseModel):
    """채팅 요청 본문. 사용자 메시지를 JSON으로 전달합니다."""

    message: str = Field(..., min_length=1, description="사용자 메시지")


class ChatResponse(BaseModel):
    reply: str


class WeatherResponse(BaseModel):
    temp: int
    description: str


class DailyForecastItem(BaseModel):
    date: str
    temp: int
    temp_min: int
    temp_max: int
    description: str
    icon: str | None = None


class WeeklyForecastResponse(BaseModel):
    city: str = "Seoul"
    city_id: str = "seoul"
    city_ko: str = "서울"
    current: WeatherResponse | None = None
    days: list[DailyForecastItem]


class CityCurrentWeather(BaseModel):
    id: str
    name: str
    name_ko: str
    temp: int
    description: str
    icon: str | None = None


class CitiesWeatherResponse(BaseModel):
    cities: list[CityCurrentWeather]


class CityForecastBundle(BaseModel):
    id: str
    name: str
    name_ko: str
    current: CityCurrentWeather
    days: list[DailyForecastItem]


class AllForecastsResponse(BaseModel):
    cities: list[CityForecastBundle]


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        logger.info("Neon DB 테이블 초기화 완료")
    except Exception as exc:
        logger.exception("Neon DB init_db 실패 — auth API가 동작하지 않을 수 있습니다: %s", exc)
    try:
        yield
    finally:
        await dispose_engine()


app = FastAPI(title="Woojeongalex Main Page", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signup_router)
app.include_router(login_router)
app.include_router(titanic_router)
app.include_router(music_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}


def _require_openweather_key() -> str:
    api_key = keymaker.get_secret("OPENWEATHER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OPENWEATHER_API_KEY가 설정되지 않았습니다. backend/.env 를 확인하세요.",
        )
    return api_key


def _openweather_http_error(exc: requests.HTTPError) -> HTTPException:
    status = exc.response.status_code if exc.response is not None else 502
    if status == 401:
        return HTTPException(
            status_code=401,
            detail="OpenWeather API 키가 올바르지 않습니다. backend/.env 의 OPENWEATHER_API_KEY 를 확인하세요.",
        )
    body = exc.response.text[:200] if exc.response is not None else str(exc)
    return HTTPException(
        status_code=status if 400 <= status < 600 else 502,
        detail=f"OpenWeather API 오류: {body}",
    )


def _city_current(api_key: str, city_id: str) -> CityCurrentWeather:
    city = OpenWeatherAdapter.get_city(city_id)
    data = OpenWeatherAdapter.fetch_current(api_key, city)
    return CityCurrentWeather(
        id=city.id,
        name=city.name,
        name_ko=city.name_ko,
        temp=int(data["temp"]),
        description=str(data["description"]),
        icon=data.get("icon") if isinstance(data.get("icon"), str) else None,
    )


def _city_forecast_bundle(api_key: str, city_id: str) -> CityForecastBundle:
    city = OpenWeatherAdapter.get_city(city_id)
    current = _city_current(api_key, city_id)
    rows = OpenWeatherAdapter.fetch_weekly(api_key, city, days=7)
    if not rows:
        raise HTTPException(status_code=502, detail=f"{city.name_ko} 예보 데이터가 비어 있습니다.")
    return CityForecastBundle(
        id=city.id,
        name=city.name,
        name_ko=city.name_ko,
        current=current,
        days=[DailyForecastItem(**row) for row in rows],
    )


@app.get("/api/weather", response_model=WeatherResponse)
def get_weather() -> WeatherResponse:
    """서울 현재 날씨(섭씨) — 하위 호환."""
    api_key = _require_openweather_key()
    try:
        data = OpenWeatherAdapter.fetch_seoul_celsius(api_key)
        return WeatherResponse(temp=int(data["temp"]), description=str(data["description"]))
    except requests.HTTPError as exc:
        raise _openweather_http_error(exc) from exc
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"OpenWeather API 연결 실패: {exc!s}") from exc
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=f"OpenWeather 응답 형식 오류: {exc!s}") from exc


@app.get("/api/weather/current", response_model=CityCurrentWeather)
def get_city_current_weather(city: str = "seoul") -> CityCurrentWeather:
    """도시별 현재 날씨."""
    api_key = _require_openweather_key()
    city_id = city.strip().lower()
    if city_id not in WEATHER_CITIES:
        raise HTTPException(status_code=404, detail=f"지원하지 않는 도시입니다: {city}")

    try:
        return _city_current(api_key, city_id)
    except requests.HTTPError as exc:
        raise _openweather_http_error(exc) from exc
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"OpenWeather API 연결 실패: {exc!s}") from exc
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=f"OpenWeather 응답 형식 오류: {exc!s}") from exc


@app.get("/api/weather/cities", response_model=CitiesWeatherResponse)
def get_cities_weather() -> CitiesWeatherResponse:
    """서울·도쿄·뉴욕·런던 현재 날씨."""
    api_key = _require_openweather_key()
    cities: list[CityCurrentWeather] = []
    try:
        for city_id in CITY_ORDER:
            cities.append(_city_current(api_key, city_id))
        return CitiesWeatherResponse(cities=cities)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"알 수 없는 도시: {exc!s}") from exc
    except requests.HTTPError as exc:
        raise _openweather_http_error(exc) from exc
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"OpenWeather API 연결 실패: {exc!s}") from exc
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=f"OpenWeather 응답 형식 오류: {exc!s}") from exc


@app.get("/api/weather/forecast", response_model=WeeklyForecastResponse)
def get_weather_forecast(city: str = "seoul") -> WeeklyForecastResponse:
    """도시별 7일 예보. `city` 기본값 seoul."""
    api_key = _require_openweather_key()
    city_id = city.strip().lower()
    if city_id not in WEATHER_CITIES:
        raise HTTPException(status_code=404, detail=f"지원하지 않는 도시입니다: {city}")

    try:
        bundle = _city_forecast_bundle(api_key, city_id)
        return WeeklyForecastResponse(
            city=bundle.name,
            city_id=bundle.id,
            city_ko=bundle.name_ko,
            current=WeatherResponse(
                temp=bundle.current.temp,
                description=bundle.current.description,
            ),
            days=bundle.days,
        )
    except HTTPException:
        raise
    except requests.HTTPError as exc:
        raise _openweather_http_error(exc) from exc
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"OpenWeather API 연결 실패: {exc!s}") from exc
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=f"OpenWeather 응답 형식 오류: {exc!s}") from exc


@app.get("/api/weather/forecasts", response_model=AllForecastsResponse)
def get_all_weather_forecasts() -> AllForecastsResponse:
    """4개 도시 현재 날씨 + 7일 예보 일괄 조회."""
    api_key = _require_openweather_key()
    bundles: list[CityForecastBundle] = []
    try:
        for city_id in CITY_ORDER:
            bundles.append(_city_forecast_bundle(api_key, city_id))
        return AllForecastsResponse(cities=bundles)
    except HTTPException:
        raise
    except requests.HTTPError as exc:
        raise _openweather_http_error(exc) from exc
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"OpenWeather API 연결 실패: {exc!s}") from exc
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=f"OpenWeather 응답 형식 오류: {exc!s}") from exc


@dataclass(frozen=True)
class _GeminiErrorRule:
    keywords: tuple[str, ...]
    status_code: int
    detail: str
    retryable: bool


_GEMINI_ERROR_RULES: tuple[_GeminiErrorRule, ...] = (
    _GeminiErrorRule(
        keywords=("429", "quota", "resource_exhausted"),
        status_code=429,
        detail=(
            "Gemini API 할당량을 초과했거나, 이 모델은 현재 요금제에서 사용할 수 없습니다. "
            "Google AI Studio에서 사용량·결제를 확인하거나, "
            "backend/.env 에 GEMINI_MODEL=gemini-2.5-flash 를 넣은 뒤 서버를 재시작해 보세요."
        ),
        retryable=True,
    ),
    _GeminiErrorRule(
        keywords=("404", "not found"),
        status_code=502,
        detail=(
            "지원하지 않는 Gemini 모델입니다. "
            "backend/.env 에 GEMINI_MODEL=gemini-2.5-flash 를 설정해 보세요."
        ),
        retryable=True,
    ),
)


def _match_gemini_rule(exc: Exception) -> _GeminiErrorRule | None:
    msg = str(exc).lower()
    for rule in _GEMINI_ERROR_RULES:
        if any(kw in msg for kw in rule.keywords):
            return rule
    return None


def _gemini_error_to_http(exc: Exception) -> HTTPException:
    rule = _match_gemini_rule(exc)
    if rule:
        return HTTPException(status_code=rule.status_code, detail=rule.detail)
    msg = str(exc)
    short = msg if len(msg) <= 280 else msg[:280] + "…"
    return HTTPException(status_code=502, detail=f"Gemini 호출 실패: {short}")


def _should_try_next_model(exc: Exception) -> bool:
    rule = _match_gemini_rule(exc)
    return rule is not None and rule.retryable


def _generate_gemini_reply(message: str) -> str:
    import google.generativeai as genai

    api_key = keymaker.get_gemini_api_key()
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY가 설정되지 않았습니다. backend/.env 에 키를 넣어 주세요.",
        )

    genai.configure(api_key=api_key)
    primary = keymaker.get_gemini_model_name()
    model_ids = [primary] + [m for m in GEMINI_FALLBACK_MODELS if m != primary]

    last_exc: Exception | None = None
    for model_id in model_ids:
        try:
            model = genai.GenerativeModel(model_id)
            response = model.generate_content(message)
            try:
                text = (response.text or "").strip()
            except ValueError as e:
                feedback = getattr(response, "prompt_feedback", None)
                raise HTTPException(
                    status_code=400,
                    detail=f"응답 텍스트를 읽을 수 없습니다: {e!s}. prompt_feedback={feedback}",
                ) from e

            if not text:
                reason = None
                if getattr(response, "candidates", None):
                    c0 = response.candidates[0]
                    reason = getattr(c0, "finish_reason", None)
                raise HTTPException(
                    status_code=502,
                    detail=(
                        "모델이 비어 있는 응답을 반환했습니다."
                        + (f" (finish_reason={reason})" if reason else "")
                    ),
                )
            return text
        except HTTPException:
            raise
        except Exception as e:
            last_exc = e
            if _should_try_next_model(e) and model_id != model_ids[-1]:
                continue
            raise _gemini_error_to_http(e) from e

    if last_exc is not None:
        raise _gemini_error_to_http(last_exc)
    raise HTTPException(status_code=502, detail="Gemini 호출에 실패했습니다.")


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """
    JSON 본문 `{"message": "..."}` 를 받아 Gemini 답변 문자열을 반환합니다.
    """
    if not keymaker.is_gemini_ready():
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY가 설정되지 않았습니다. backend/.env 에 키를 넣어 주세요.",
        )

    try:
        reply = _generate_gemini_reply(req.message)
    except HTTPException:
        raise
    except Exception as e:
        raise _gemini_error_to_http(e) from e

    return ChatResponse(reply=reply)


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    return await DbHealthAdapter.neon_time_check(db)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


