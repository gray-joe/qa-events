from abc import abstractmethod, ABC
from typing import Any


class AbstractModel(ABC):
    @abstractmethod
    def build_from_json(self, gitlab_event: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def save(self, database_connection) -> None:
        pass
