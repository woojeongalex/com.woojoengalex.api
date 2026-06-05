"""Titanic Use Case 조립 — DB 세션은 여기서만 주입."""

from titanic.dependencies.james_director import get_james_use_case
from titanic.dependencies.walter_roaster import get_walter_use_case

__all__ = ["get_james_use_case", "get_walter_use_case"]
