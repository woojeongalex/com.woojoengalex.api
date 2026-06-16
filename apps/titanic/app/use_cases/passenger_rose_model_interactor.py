from __future__ import annotations

import math

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from titanic.app.ports.input.passenger_rose_model_use_case import PredictionStrategy, RoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

_HIGH = frozenset({"여성", "아이", "어린이", "구조", "생존", "탈출", "구명", "1등석", "부유"})
_LOW  = frozenset({"남성", "침몰", "사망", "익사", "죽음", "3등석", "빈곤"})


def _signals(keywords: list[str]) -> tuple[int, int]:
    kw = set(keywords)
    return len(kw & _HIGH), len(kw & _LOW)


# ── 1. XGBoost ──────────────────────────────────────────────────────────────
class XGBoostStrategy:
    """그래디언트 부스팅: 가중 점수 + 정규화."""

    def predict(self, keywords: list[str]) -> float:
        pos, neg = _signals(keywords)
        score = (pos * 1.5 - neg * 1.2) / max(len(keywords), 1)
        return min(max(0.5 + score * 0.2, 0.0), 1.0)


# ── 2. Random Forest ─────────────────────────────────────────────────────────
class RandomForestStrategy:
    """배깅: 서브셋 5개 다수결."""

    _SURVIVAL_TREES = [
        frozenset({"여성", "구조", "생존"}),
        frozenset({"아이", "탈출", "구명"}),
        frozenset({"1등석", "부유"}),
    ]
    _DEATH_TREES = [
        frozenset({"남성", "침몰", "사망"}),
        frozenset({"3등석", "죽음", "익사"}),
    ]

    def predict(self, keywords: list[str]) -> float:
        kw = set(keywords)
        votes = [1 for t in self._SURVIVAL_TREES if kw & t]
        votes += [0 for t in self._DEATH_TREES if kw & t]
        return sum(votes) / len(votes) if votes else 0.50


# ── 3. LightGBM ──────────────────────────────────────────────────────────────
class LightGBMStrategy:
    """리프 중심: 가장 구체적으로 매칭되는 키워드 우선."""

    _LEAF: dict[str, float] = {
        "여성": 0.74, "아이": 0.71, "1등석": 0.63,
        "남성": 0.21, "3등석": 0.24, "침몰": 0.18,
    }

    def predict(self, keywords: list[str]) -> float:
        scores = [self._LEAF[k] for k in keywords if k in self._LEAF]
        return max(scores) if scores else 0.50


# ── 4. CatBoost ──────────────────────────────────────────────────────────────
class CatBoostStrategy:
    """범주형 최적화: 인코딩 없이 범주 매핑 직접 적용."""

    _CAT: dict[str, float] = {
        "여성": 0.74, "남성": 0.19,
        "1등석": 0.63, "2등석": 0.47, "3등석": 0.24,
        "아이": 0.71, "성인": 0.38, "노인": 0.28,
    }

    def predict(self, keywords: list[str]) -> float:
        scores = [self._CAT[k] for k in keywords if k in self._CAT]
        return sum(scores) / len(scores) if scores else 0.50


# ── 5. Logistic Regression ───────────────────────────────────────────────────
class LogisticRegressionStrategy:
    """선형 가중합 → 시그모이드."""

    _WEIGHTS: dict[str, float] = {
        "여성": 2.1, "아이": 1.8, "구명": 1.5, "1등석": 1.2,
        "남성": -1.9, "3등석": -1.3, "침몰": -2.0, "사망": -2.5,
    }

    def predict(self, keywords: list[str]) -> float:
        z = sum(self._WEIGHTS.get(k, 0.0) for k in keywords)
        return 1.0 / (1.0 + math.exp(-z))


# ── 6. Decision Tree ─────────────────────────────────────────────────────────
class DecisionTreeStrategy:
    """명시적 규칙 트리."""

    def predict(self, keywords: list[str]) -> float:
        kw = set(keywords)
        if "여성" in kw or "아이" in kw:
            return 0.74 if kw & {"1등석", "2등석"} else 0.50
        if "남성" in kw:
            return 0.11 if "3등석" in kw else 0.21
        return 0.50


# ── 7. SVM ───────────────────────────────────────────────────────────────────
class SVMStrategy:
    """마진 최대화: 결정 경계로부터의 거리."""

    def predict(self, keywords: list[str]) -> float:
        pos, neg = _signals(keywords)
        margin = (pos - neg) / max(pos + neg, 1)
        return min(max(0.5 + margin * 0.3, 0.0), 1.0)


# ── 8. KNN ───────────────────────────────────────────────────────────────────
class KNNStrategy:
    """최근접 이웃: 알려진 승객 프로파일과의 자카드 유사도."""

    _PROFILES: list[tuple[frozenset, float]] = [
        (frozenset({"여성", "1등석"}), 0.97),
        (frozenset({"아이", "2등석"}), 0.89),
        (frozenset({"남성", "선원"}), 0.22),
        (frozenset({"남성", "3등석"}), 0.13),
    ]

    def predict(self, keywords: list[str]) -> float:
        kw = set(keywords)
        best_sim, best_prob = 0.0, 0.50
        for profile, prob in self._PROFILES:
            union = len(profile | kw)
            sim = len(profile & kw) / union if union else 0.0
            if sim > best_sim:
                best_sim, best_prob = sim, prob
        return best_prob


# ── 9. Naive Bayes ───────────────────────────────────────────────────────────
class NaiveBayesStrategy:
    """베이즈 정리: P(생존|키워드) 반복 갱신."""

    _PRIOR = 0.384  # 타이타닉 실제 생존율
    _LIKELIHOOD: dict[str, float] = {
        "여성": 3.8, "아이": 3.2, "1등석": 2.1,
        "남성": 0.21, "3등석": 0.48, "침몰": 0.30,
    }

    def predict(self, keywords: list[str]) -> float:
        p = self._PRIOR
        for k in keywords:
            lr = self._LIKELIHOOD.get(k, 1.0)
            p = (p * lr) / (p * lr + (1 - p))
        return round(p, 4)


# ── 10. K-Means & PCA ────────────────────────────────────────────────────────
class KMeansPCAStrategy:
    """군집 배정: 키워드를 생존/사망/중립 클러스터에 매핑."""

    _CLUSTER_PROB = {"고생존군": 0.78, "저생존군": 0.17, "중립군": 0.45}
    _RULES = [
        (frozenset({"여성", "아이", "1등석", "부유"}), "고생존군"),
        (frozenset({"남성", "3등석", "빈곤"}),          "저생존군"),
    ]

    def predict(self, keywords: list[str]) -> float:
        kw = set(keywords)
        for signals, cluster in self._RULES:
            if kw & signals:
                return self._CLUSTER_PROB[cluster]
        return self._CLUSTER_PROB["중립군"]


# ── Interactor ───────────────────────────────────────────────────────────────
class RoseModelInteractor(RoseModelUseCase):
    def __init__(
        self,
        repository: RoseModelRepository,
        strategy: PredictionStrategy = RandomForestStrategy(),
    ) -> None:
        self.repository = repository
        self._strategy = strategy

    async def predict(self, keywords: list[str]) -> float:
        return self._strategy.predict(keywords)

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        return await self.repository.introduce_myself(RoseModelQuery(
            id=schema.id,
            name=schema.name,
        ))
