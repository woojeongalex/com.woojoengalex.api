import asyncio
import logging
import sys
from contextlib import asynccontextmanager

import requests

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from logging_setup import configure_logging

configure_logging()

from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from adapters.db_health_adapter import DbHealthAdapter
from adapters.openweather_adapter import CITY_ORDER, WEATHER_CITIES, OpenWeatherAdapter
from database import dispose_engine, get_db, init_db
import music.app.models.list_model  # noqa: F401
import music.app.models.ai_vocal_analysis_model  # noqa: F401
import music.app.models.user_vocal_recording_model  # noqa: F401
import music.app.models.evaluation_models  # noqa: F401
import music.app.models.sing_model  # noqa: F401
import music.app.models.suggest_model  # noqa: F401
import music.app.models.instrument_evaluation_model  # noqa: F401
import music.app.models.instrument_recording_model  # noqa: F401
import music.app.models.instrument_tuning_analysis_model  # noqa: F401
import music.app.models.speech_evaluation_model  # noqa: F401
import music.app.models.speech_recording_model  # noqa: F401
import music.app.models.speech_feedback_analysis_model  # noqa: F401
import secom.app.entities.user_entity  # noqa: F401
from doro.app.doro_director import DoroDirector
from matrix.app.keymaker import get_keymaker
from music.app.controllers.list_controller import ListController
from music.app.controllers.evaluation_controller import EvaluationController
from music.app.controllers.suggest_controller import SuggestController
from music.app.controllers.video_analysis_controller import VideoAnalysisController
from music.app.services.instrument_service import InstrumentService
from music.app.services.speech_service import SpeechService
from music.app.schemas.video_analysis_schema import VideoVocalAnalysisResponse
from music.app.schemas.list_schema import SongMrSearchResponse
from music.app.schemas.sing_schema import SingEvaluationCreateRequest, SingEvaluationResponse
from music.app.schemas.suggest_schema import (
    VocalRecommendationCreateRequest,
    VocalRecommendationResponse,
)
from music.app.schemas.instrument_schemas import (
    InstrumentCatalogResponse,
    InstrumentEvaluationCreateRequest,
    InstrumentEvaluationResponse,
)
from music.app.schemas.speech_schemas import (
    SpeechEvaluationCreateRequest,
    SpeechEvaluationResponse,
    SpeechTopicsResponse,
)
from secom.app import auth_routes
from secom.app.schemas.user_schema import (
    LoginRequest,
    LoginResponse,
    SignupRequest,
    SignupResponse,
    UsernameCheckResponse,
)
from titanic.app.controllers.james_controller import JamesController
from titanic.app.schemas.titanic_schema import TitanicDatasetSchemaResponse



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


@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}


@app.post("/api/auth/signup", response_model=SignupResponse)
async def signup(
    request: SignupRequest,
    db: AsyncSession = Depends(get_db),
) -> SignupResponse:
    logger.info(
        "[AUTH-FLOW][signup][1/main] POST /api/auth/signup username=%s",
        request.username.strip(),
    )
    return await auth_routes.signup_user(db, request)


@app.get("/api/auth/check-id", response_model=UsernameCheckResponse)
async def check_username(
    username: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
) -> UsernameCheckResponse:
    return await auth_routes.check_username_available(db, username)


@app.get("/api/auth/check-nickname", response_model=UsernameCheckResponse)
async def check_nickname(
    nickname: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
) -> UsernameCheckResponse:
    return await auth_routes.check_nickname_available(db, nickname)


@app.post("/api/auth/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    logger.info(
        "[AUTH-FLOW][login][1/main] POST /api/auth/login username=%s",
        request.username.strip(),
    )
    return await auth_routes.login_user(db, request)


@app.get("/api/songs/search", response_model=SongMrSearchResponse)
async def songs_search(
    q: str = Query(..., min_length=1, description="노래 제목·MR·아티스트 검색어"),
    db: AsyncSession = Depends(get_db),
) -> SongMrSearchResponse:
    logger.info("[MUSIC][search][1/main] GET /api/songs/search q=%s", q.strip())
    try:
        result = await ListController(db).search_mr(q)
        logger.info(
            "[MUSIC][search][1/main] 완료 q=%s count=%s titles=%s",
            result.query,
            result.count,
            [h.title for h in result.hits],
        )
        return result
    except SQLAlchemyError as exc:
        logger.exception("[music] GET /api/songs/search DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc


@app.get("/api/music/instrument-catalog", response_model=InstrumentCatalogResponse)
async def get_instrument_catalog(
    q: str = Query("", description="악기 검색어"),
) -> InstrumentCatalogResponse:
    return InstrumentService(None).list_catalog(q)


@app.post(
    "/api/music/instrument-evaluation",
    response_model=InstrumentEvaluationResponse,
)
async def post_instrument_evaluation(
    body: InstrumentEvaluationCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> InstrumentEvaluationResponse:
    try:
        return await InstrumentService(db).save_evaluation(body)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][instrument] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc


@app.get("/api/music/speech-topics", response_model=SpeechTopicsResponse)
async def get_speech_topics() -> SpeechTopicsResponse:
    return SpeechService(None).list_topics()


@app.post("/api/music/speech-evaluation", response_model=SpeechEvaluationResponse)
async def post_speech_evaluation(
    body: SpeechEvaluationCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> SpeechEvaluationResponse:
    try:
        return await SpeechService(db).save_evaluation(body)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][speech] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc


@app.post("/api/music/sing-evaluation", response_model=SingEvaluationResponse)
async def post_sing_evaluation(
    body: SingEvaluationCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> SingEvaluationResponse:
    logger.info(
        "[MUSIC][sing][1/main] POST /api/music/sing-evaluation input=%s",
        body.input_source,
    )
    try:
        return await EvaluationController(db).save_evaluation(body)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][sing][1/main] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc


@app.post("/api/music/vocal-recommendations", response_model=VocalRecommendationResponse)
async def post_vocal_recommendations(
    body: VocalRecommendationCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> VocalRecommendationResponse:
    """저장된 보컬 평가(`sing_evaluations.id`)을 기준으로 추천 장르·곡을 계산해 Neon에 저장."""
    logger.info(
        "[MUSIC][suggest][1/main] POST /api/music/vocal-recommendations "
        "singEvaluationId=%s",
        body.sing_evaluation_id,
    )
    try:
        return await SuggestController(db).create_recommendation(body)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][suggest][1/main] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc


@app.get("/api/music/vocal-recommendations", response_model=VocalRecommendationResponse)
async def get_vocal_recommendations(
    singEvaluationId: int = Query(
        ...,
        ge=1,
        alias="singEvaluationId",
        description="sing_evaluations.id",
    ),
    db: AsyncSession = Depends(get_db),
) -> VocalRecommendationResponse:
    """해당 평가에 대해 가장 최근에 저장된 추천 배너 데이터 조회."""
    logger.info(
        "[MUSIC][suggest][1/main] GET /api/music/vocal-recommendations "
        "singEvaluationId=%s",
        singEvaluationId,
    )
    try:
        out = await SuggestController(db).get_latest(singEvaluationId)
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][suggest][1/main] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
    if out is None:
        raise HTTPException(
            status_code=404,
            detail="해당 분석에 대한 추천이 없습니다. 먼저 POST로 생성하세요.",
        )
    return out


@app.post("/api/music/analyze-video", response_model=VideoVocalAnalysisResponse)
async def analyze_video_upload(
    file: UploadFile = File(..., description="노래 부르는 영상 (mp4, mov 등)"),
) -> VideoVocalAnalysisResponse:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="파일이 비어 있습니다.")
    filename = file.filename or "upload.mp4"
    logger.info(
        "[MUSIC][video_analysis][1/main] POST /api/music/analyze-video file=%s bytes=%s",
        filename,
        len(data),
    )
    try:
        return await asyncio.to_thread(
            VideoAnalysisController().analyze_video_upload,
            data,
            filename,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("[MUSIC][video_analysis][1/main] 분석 실패: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="비디오 분석에 실패했습니다. ffmpeg 설치·파일 형식을 확인하거나 로그를 확인하세요.",
        ) from exc


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


def _gemini_error_to_http(exc: Exception) -> HTTPException:
    msg = str(exc)
    lower = msg.lower()
    if "429" in msg or "quota" in lower or "resource_exhausted" in lower:
        return HTTPException(
            status_code=429,
            detail=(
                "Gemini API 할당량을 초과했거나, 이 모델은 현재 요금제에서 사용할 수 없습니다. "
                "Google AI Studio에서 사용량·결제를 확인하거나, "
                "backend/.env 에 GEMINI_MODEL=gemini-2.5-flash 를 넣은 뒤 서버를 재시작해 보세요."
            ),
        )
    if "404" in msg or "not found" in lower:
        return HTTPException(
            status_code=502,
            detail=(
                "지원하지 않는 Gemini 모델입니다. "
                "backend/.env 에 GEMINI_MODEL=gemini-2.5-flash 를 설정해 보세요."
            ),
        )
    short = msg if len(msg) <= 280 else msg[:280] + "…"
    return HTTPException(status_code=502, detail=f"Gemini 호출 실패: {short}")


def _should_try_next_model(exc: Exception) -> bool:
    msg = str(exc).lower()
    return (
        "429" in str(exc)
        or "quota" in msg
        or "resource_exhausted" in msg
        or "404" in str(exc)
        or "not found" in msg
    )


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


@app.get("/titanic/data")
def read_titanic_data():
    james = JamesController()
    df = james.get_data()

    return df.to_dict(orient="records")


@app.get("/titanic/count")
def read_titanic_count():
    james = JamesController()
    count = james.get_count()

    return {"count": count}


@app.get("/titanic/count/survived")
def read_titanic_survived_count():
    james = JamesController()
    count = james.get_survived_count()
    return {"survived_count": count}


@app.get("/titanic/count/dead")
def read_titanic_dead_count():
    james = JamesController()
    count = james.get_dead_count()
    return {"dead_count": count}


@app.get("/titanic/tree")
def read_titanic_tree():
    james = JamesController()
    tree = james.has_decision_tree_model()

    return {"tree": tree}


@app.get("/titanic/schema", response_model=TitanicDatasetSchemaResponse)
def read_titanic_schema() -> TitanicDatasetSchemaResponse:
    """데이터셋 컬럼 설명·ML 피처 목록."""
    return JamesController().get_dataset_schema()


@app.get("/titanic/model")
def read_titanic_model():
    metrics = JamesController().get_model_name_and_accuracy()
    return JSONResponse(content=jsonable_encoder(metrics.model_dump()))


@app.get("/doro/data")
def read_doro_data():
    doro_director = DoroDirector()
    df = doro_director.get_data()

    return df.to_dict(orient="records")

#회원가입


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


