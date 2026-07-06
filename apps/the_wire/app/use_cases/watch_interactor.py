import logging
import os
from pathlib import Path

from the_wire.app.dtos.watch_dto import (
    PolicyFilterCommand,
    PolicyFilterResult,
    WatchStatusResult,
)
from the_wire.app.ports.input.watch_use_case import WatchUseCase
from the_wire.app.ports.output.watch_repository_port import WatchRepositoryPort

logger = logging.getLogger(__name__)

_MODEL_DIR = Path(
    os.getenv(
        "POLICY_FILTER_MODEL_DIR",
        "/app/output/watson-policy-filter",
    )
)
_BLOCK_THRESHOLD = float(os.getenv("POLICY_FILTER_THRESHOLD", "0.5"))


class WatchInteractor(WatchUseCase):
    def __init__(self, repository: WatchRepositoryPort) -> None:
        self.repository = repository
        self._tokenizer = None
        self._model = None
        self._load_model()

    def _load_model(self) -> None:
        if not _MODEL_DIR.exists():
            logger.warning(
                "[WatchInteractor] 정책 필터 모델 없음 (%s) — 필터 비활성화", _MODEL_DIR
            )
            return
        try:
            from transformers import AutoModelForSequenceClassification, AutoTokenizer

            self._tokenizer = AutoTokenizer.from_pretrained(str(_MODEL_DIR))
            self._model = AutoModelForSequenceClassification.from_pretrained(
                str(_MODEL_DIR)
            )
            self._model.eval()
            logger.info("[WatchInteractor] 정책 필터 모델 로드 완료: %s", _MODEL_DIR)
        except Exception:
            logger.exception("[WatchInteractor] 모델 로드 실패 — 필터 비활성화")

    async def read_status(self) -> WatchStatusResult | None:
        logger.info("[WatchInteractor] read_status")
        return await self.repository.find_latest()

    def filter(self, command: PolicyFilterCommand) -> PolicyFilterResult:
        if self._model is None or self._tokenizer is None:
            # 모델 없으면 전부 PASS (fallback)
            return PolicyFilterResult(
                verdict="PASS", score=0.0, reason="모델 미탑재 — 필터 비활성화"
            )

        import torch

        text = f"{command.subject}\n{command.sender}\n{command.body}"
        inputs = self._tokenizer(
            text, return_tensors="pt", truncation=True, max_length=128, padding=True
        )
        with torch.no_grad():
            logits = self._model(**inputs).logits
            probs = torch.softmax(logits, dim=-1)
            block_score = float(probs[0][1])

        verdict = "BLOCK" if block_score >= _BLOCK_THRESHOLD else "PASS"
        reason = f"정책 필터 점수: {block_score:.3f} (임계값 {_BLOCK_THRESHOLD})"
        logger.info(
            "[WatchInteractor] filter verdict=%s score=%.3f", verdict, block_score
        )
        return PolicyFilterResult(verdict=verdict, score=block_score, reason=reason)
