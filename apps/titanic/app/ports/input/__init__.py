"""입력 Port — v1 라우터와 1:1 (James·Walter + 캐릭터 스텁)."""

from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTestUseCase
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainUseCase
from titanic.app.ports.input.crew_james_use_case import JamesUseCase
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.input.passenger_ruth_survivor_use_case import RuthSurvivorUseCase
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.crew_walter_use_case import WalterUseCase

__all__ = [
    "JamesUseCase",
    "WalterUseCase",
    "RoseModelUseCase",
    "AndrewsArchitectUseCase",
    "JackTrainUseCase",
    "RuthSurvivorUseCase",
    "IsidorCoupleUseCase",
    "SmithCaptainUseCase",
    "HartleyViolinUseCase",
    "CalTestUseCase",
    "LoweBoatUseCase",
    "MollyScalerUseCase",
]
