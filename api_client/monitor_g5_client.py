from typing import List

from .base_client import BaseERPClient, UsersList


class MonitorG5ERPClient(BaseERPClient):
    def __init__(self):
        pass

    def get_workers(self) -> List[UsersList]:
        pass
