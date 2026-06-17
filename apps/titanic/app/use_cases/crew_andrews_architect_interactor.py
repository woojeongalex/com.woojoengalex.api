from __future__ import annotations

from typing import cast

from kiwipiepy import Kiwi, Token

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_port import AndrewsArchitectPort

_KEYWORD_TAGS: set[str] = {"NNG", "NNP", "SL", "VV", "VA"}

_INTENT_PATTERNS: dict[str, set[str]] = {
    "count":   {"몇", "명", "총", "탑승객", "인원", "수", "명수", "숫자"},
    "predict": {"예측", "생존", "확률", "predict", "survival", "살았", "살아"},
    "death":   {"사망", "죽", "죽었", "죽음", "익사", "침몰", "사망했", "죽었어"},
    "train":   {"훈련", "학습", "train", "fitting"},
    "test":    {"테스트", "검증", "평가", "test", "evaluate"},
    "info":    {"정보", "알려", "설명", "info", "explain"},
}


class AndrewsArchitectInteractor(AndrewsArchitectUseCase):
    def __init__(self, repository: AndrewsArchitectPort) -> None:
        self._repository = repository
        self.kiwi = Kiwi()

    def analyze_message_intent(self, user_messages: str) -> dict:
        tokens = cast(list[Token], self.kiwi.tokenize(user_messages))
        keywords = [t.form for t in tokens if str(t.tag) in _KEYWORD_TAGS]
        forms = {t.form for t in tokens}

        intent = "general"
        for intent_name, patterns in _INTENT_PATTERNS.items():
            if forms & patterns:
                intent = intent_name
                break

        return {
            "keywords": keywords,
            "intent": intent,
            "tokens": [{"form": t.form, "tag": str(t.tag)} for t in tokens],
        }

    async def introduce_myself(self, request) -> AndrewsArchitectResponse:
        return await self._repository.introduce_myself(AndrewsArchitectQuery(
            id=request.id,
            name=request.name,
        ))
