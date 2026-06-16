"""[Layer: Use Cases] Smith captain (SmithCaptainUseCase 구현)."""
import logging


from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema, SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTestUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.input.passenger_walter_use_case import WalterUseCase


logger = logging.getLogger("titanic_flow_log")


class SmithCaptainInteractor(SmithCaptainUseCase):
    def __init__(
        self,
        repository: SmithCaptainRepository,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
        cal: CalTestUseCase,
        walter: WalterUseCase
    ):
        self._repository = repository
        self._jack = jack
        self._rose = rose
        self._cal = cal
        self._walter = walter
        
    
        
    async def chat(self, schema: ChatSchema) -> SmithCaptainResponse:
        logger.info("[SmithCaptainInteractor] chat 진입 | messages=%s", schema.messages)
        analysis = await self._jack.analyze_message_intent(schema.messages)
        survival_prob = await self._rose.predict(analysis["keywords"])
        train_set = await self._jack.get_model_train()
        test_set = await self._cal.test_models(train_set)
        
        context = (
            f"{schema.messages}"
            f" [의도: {analysis['intent']}"
            f", 키워드: {', '.join(analysis['keywords']) or '없음'}"
            f", 생존확률: {survival_prob:.0%}]"
        )
        return await self._repository.chat(message=context)

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        return await self._repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name,
        ))
