from abc import ABC, abstractmethod


class FaceDatasetPort(ABC):
    @abstractmethod
    def get_dataset_config_path(self) -> str: ...
