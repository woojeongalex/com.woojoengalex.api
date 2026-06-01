"""[Layer: Ports] 보컬 추천 출력 Port — 조회·저장 계약."""

from abc import ABC, abstractmethod

from music.adapter.outbound.orm.ai_vocal_analysis_model import AiVocalAnalysisEntity
from music.adapter.outbound.orm.sing_model import SingEvaluationEntity
from music.adapter.outbound.orm.suggest_model import VocalRecommendationEntity


class SuggestRepositoryPort(ABC):
    @abstractmethod
    async def get_sing_evaluation_by_id(
        self, evaluation_id: int
    ) -> SingEvaluationEntity | None:
        pass

    @abstractmethod
    async def get_ai_analysis_for_sing_evaluation(
        self, sing_evaluation_id: int
    ) -> AiVocalAnalysisEntity | None:
        pass

    @abstractmethod
    async def get_ai_analysis_by_id(
        self, ai_analysis_id: int
    ) -> AiVocalAnalysisEntity | None:
        pass

    @abstractmethod
    async def save_recommendation(
        self, row: VocalRecommendationEntity
    ) -> VocalRecommendationEntity:
        pass

    @abstractmethod
    async def get_latest_by_evaluation_id(
        self, sing_evaluation_id: int
    ) -> VocalRecommendationEntity | None:
        pass
