import logging
import sys


def configure_logging() -> None:
    """터미널에 secom·main 로그가 보이도록 설정합니다."""
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    stream_handlers = [h for h in root.handlers if isinstance(h, logging.StreamHandler)]
    if stream_handlers:
        for stream_handler in stream_handlers:
            stream_handler.setFormatter(formatter)
    else:
        root.addHandler(handler)

    for name in (
        "main",
        "database",
        "secom",
        "secom.app.auth_routes",
        "secom.app.controllers.user_controller",
        "secom.app.services.user_service",
        "secom.app.repositories.user_repository",
        "secom.app.models.user_model",
        "secom.app.auth_flow_log",
        "music",
        "music.app.controllers.list_controller",
        "music.app.services.list_service",
        "music.app.repositories.list_repository",
        "music.app.services.video_audio_preprocess",
        "music.app.services.librosa_vocal_analysis",
        "music.app.services.emotion_analysis",
        "music.app.services.video_analysis_service",
        "music.app.controllers.video_analysis_controller",
        "music.app.controllers.sing_controller",
        "music.app.services.sing_service",
        "music.app.repositories.sing_repository",
        "titanic",
        "titanic.app.titanic_flow_log",
        "titanic.adapter.inbound.api.v1.james_router",
        "titanic.app.ports.input.james_use_case",
        "titanic.app.ports.output.james_repository",
        "titanic.adapter.outbound.pg.james_pg_repository",
        "titanic.adapter.inbound.api.v1.walter_router",
        "titanic.app.use_cases.walter_query",
        "titanic.app.use_cases.walter_use_case",
        "titanic.app.ports.output.walter_repository",
        "titanic.adapter.outbound.pg.walter_pg_repository",
    ):
        pkg_logger = logging.getLogger(name)
        pkg_logger.setLevel(logging.INFO)
        pkg_logger.propagate = True

    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
