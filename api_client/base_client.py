from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class UsersList:
    id_number: int
    name: str
    location: int
    department: int
    status: bool


class BaseERPClient(ABC):
    @abstractmethod
    def get_workers(self) -> list[UsersList]:
        pass
