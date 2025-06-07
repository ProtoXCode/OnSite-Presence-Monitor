from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class UsersList:
    id_number: int
    name: str
    location: str
    status: bool


class BaseERPClient(ABC):
    @abstractmethod
    def get_workers(self) -> List[UsersList]:
        pass
