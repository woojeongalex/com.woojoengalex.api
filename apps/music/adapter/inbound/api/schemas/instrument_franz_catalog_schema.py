from pydantic import BaseModel


class InstrumentCatalogHit(BaseModel):
    instrument_id: str
    label: str
    description: str
    standard_tuning: str


class InstrumentCatalogResponse(BaseModel):
    query: str = ""
    hits: list[InstrumentCatalogHit]
    count: int
