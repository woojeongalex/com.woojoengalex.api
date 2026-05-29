"""[Layer: Use Cases] James 업로드 결과."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UploadResultDto:
    file_name: str
    count: int
