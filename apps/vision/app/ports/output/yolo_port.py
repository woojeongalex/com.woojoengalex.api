from abc import ABC, abstractmethod


class YoloPort(ABC):
    @abstractmethod
    def get_dataset_config_path(self) -> str: ...
