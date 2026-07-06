from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from vision.adapter.outbound.repositories.vision_pg_repository import (
    VisionPgRepository,
)
from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.app.ports.output.vision_repository_port import VisionRepositoryPort
from vision.app.use_cases.face_recognition_interactor import (
    FaceRecognitionInteractor,
)
from vision.app.use_cases.vision_interactor import VisionInteractor

try:
    from database import get_db
except ModuleNotFoundError:
    from apps.database import get_db


def get_vision_repository(
    db: AsyncSession = Depends(get_db),
) -> VisionRepositoryPort:
    return VisionPgRepository(session=db)


def get_vision_use_case(
    repository: VisionRepositoryPort = Depends(get_vision_repository),
) -> VisionUseCase:
    return VisionInteractor(repository=repository)


def get_face_recognition_use_case(
    repository: VisionRepositoryPort = Depends(get_vision_repository),
) -> VisionUseCase:
    return FaceRecognitionInteractor(repository=repository)
