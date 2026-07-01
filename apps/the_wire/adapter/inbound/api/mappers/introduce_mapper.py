from the_wire.adapter.inbound.api.schemas.introduce_schema import (
    IntroduceResponseSchema,
)
from the_wire.app.dtos.introduce_dto import IntroduceQuery, IntroduceResponse


def schema_to_query(locale: str) -> IntroduceQuery:
    return IntroduceQuery(locale=locale)


def dto_to_response_schema(dto: IntroduceResponse) -> IntroduceResponseSchema:
    return IntroduceResponseSchema(
        agent_name=dto.agent_name,
        role=dto.role,
        capabilities=dto.capabilities,
        version=dto.version,
    )
