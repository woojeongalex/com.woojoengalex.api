"""PG Repository — v1 라우터·output Port와 1:1 (*_pg_repository)."""

from titanic.adapter.outbound.pg.crew_andrews_architect_pg_repository import (
    AndrewsArchitectPgRepository,
)
from titanic.adapter.outbound.pg.passenger_cal_tester_pg_repository import CalTestPgRepository
from titanic.adapter.outbound.pg.crew_hartley_violin_pg_repository import HartleyViolinPgRepository
from titanic.adapter.outbound.pg.passenger_isidor_couple_pg_repository import IsidorCouplePgRepository
from titanic.adapter.outbound.pg.passenger_jack_trainer_pg_repository import JackTrainPgRepository
from titanic.adapter.outbound.pg.crew_james_pg_repository import JamesPgRepository
from titanic.adapter.outbound.pg.crew_lowe_boat_pg_repository import LoweBoatPgRepository
from titanic.adapter.outbound.pg.passenger_molly_scaler_pg_repository import MollyScalerPgRepository
from titanic.adapter.outbound.pg.passenger_rose_model_pg_repository import RoseModelPgRepository
from titanic.adapter.outbound.pg.passenger_ruth_survivor_pg_repository import RuthSurvivorPgRepository
from titanic.adapter.outbound.pg.crew_smith_captain_pg_repository import SmithCaptainPgRepository
from titanic.adapter.outbound.pg.crew_walter_pg_repository import WalterPgRepository

__all__ = [
    "JamesPgRepository",
    "WalterPgRepository",
    "RoseModelPgRepository",
    "AndrewsArchitectPgRepository",
    "JackTrainPgRepository",
    "RuthSurvivorPgRepository",
    "IsidorCouplePgRepository",
    "SmithCaptainPgRepository",
    "HartleyViolinPgRepository",
    "CalTestPgRepository",
    "LoweBoatPgRepository",
    "MollyScalerPgRepository",
]
