"""[Layer: Use Cases] Smith captain (SmithCaptainUseCase 구현)."""
import logging


from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema, SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTestUseCase
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.input.crew_walter_use_case import WalterUseCase


logger = logging.getLogger("titanic_flow_log")


class SmithCaptainInteractor(SmithCaptainUseCase):
    def __init__(
        self,
        repository: SmithCaptainPort,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
        cal: CalTestUseCase,
        walter: WalterUseCase,
        andrews: AndrewsArchitectUseCase,
    ):
        self._repository = repository
        self._jack = jack
        self._rose = rose
        self._cal = cal
        self._walter = walter
        self._andrews = andrews
        
    
        
    async def chat(self, schema: ChatSchema) -> SmithCaptainResponse:
        logger.info("[SmithCaptainInteractor] chat 진입 | messages=%s", schema.messages)

        # 1. Andrews: 질문 의도 분석
        question: dict = self._andrews.analyze_message_intent(schema.messages)

        # 2. Walter: DB에서 데이터 로드
        train_df = await self._walter.get_train_set()
        test_df = await self._walter.get_test_set()

        # 3. Rose: 데이터 분석 (생존 확률 예측 + 최적 전략 선택)
        survival_prob = await self._rose.predict(question["keywords"])
        rose_result: dict = await self._rose.train_model(train_df)
        best_strategy: str = rose_result.get("selected_strategy", "없음")
        best_accuracy: float = rose_result.get("selected_accuracy", 0.0)

        # 4. Jack: 모델 훈련
        await self._jack.train_model(train_df)
        model_manifest: dict = await self._jack.get_model_train()

        # 5. Cal: 검증 및 정확도 산출
        test_result: dict = await self._cal.test_models(model_manifest)
        top_cal_model: str = test_result.get("top_model") or best_strategy

        # 6. Rose: 분석 결과를 바탕으로 답변 생성
        answer = self._rose.analyze_and_answer(
            intent=question["intent"],
            question=schema.messages,
            keywords=question["keywords"],
            train_df=train_df,
            test_df=test_df,
            survival_prob=survival_prob,
            best_strategy=top_cal_model,
            best_accuracy=best_accuracy,
        )

        # 7. Smith: 최종 반환
        return SmithCaptainResponse(id=0, name="스미스 선장", answer=answer, accuracy=best_accuracy)

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        return await self._repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name,
        ))
