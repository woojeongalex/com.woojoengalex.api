from __future__ import annotations

import asyncio

from kiwipiepy import Kiwi
f
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

_KEYWORD_TAGS = {"NNG", "NNP", "NNB"}

_INTENT_PATTERNS: dict[str, set[str]] = {
    "count_query":    {"몇", "수", "명", "개"},
    "time_query":     {"언제", "날짜", "시간", "때"},
    "location_query": {"어디", "위치", "장소", "곳"},
    "reason_query":   {"왜", "이유", "원인"},
    "method_query":   {"어떻게", "방법", "방식"},
    "info_query":     {"뭐", "무엇", "어떤", "누구"},
}


class JackTrainerInteractor(JackTrainerUseCase):
    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository
        self.kiwi = Kiwi()

    async def analyze_message_intent(self, user_message: str) -> dict:
        '''사용자의 질문(message)을 형태소 분석하여 키워드와 의도를 파악한다'''
        tokens = await asyncio.to_thread(self.kiwi.tokenize, user_message)

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

    async def introduce_myself(self, request) -> JackTrainerResponse:
        return await self.repository.introduce_myself(JackTrainerQuery(
            id=request.id,
            name=request.name,
        ))
