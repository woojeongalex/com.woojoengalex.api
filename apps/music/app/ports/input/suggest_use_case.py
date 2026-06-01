"""[Layer: Ports] 보컬 추천 입력 Port — 생성·조회 (inbound → usecase)."""

from abc import ABC, abstractmethod

from music.app.dtos.suggest_dto import (
    VocalRecommendationCreateCommand,
    VocalRecommendationResultDto,
)


class SuggestUseCase(ABC):
    @abstractmethod
    async def create_from_saved_evaluation(
        self, command: VocalRecommendationCreateCommand
    ) -> VocalRecommendationResultDto:
        pass

    @abstractmethod
    async def get_latest(
        self, sing_evaluation_id: int
    ) -> VocalRecommendationResultDto | None:
        pass
