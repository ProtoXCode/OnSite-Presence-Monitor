from typing import List
from datetime import datetime
from pathlib import Path

import pandas as pd

from .base_client import BaseERPClient, UsersList


class MockERPClient(BaseERPClient):
    def __init__(self, sample_data_path=None):
        if sample_data_path is None:
            sample_data_path = Path(
                __file__).parent.parent / 'data' / 'sample_data.csv'
            self.sample_data_path = sample_data_path
        self.current_time = datetime.now().strftime('%H:%M')

    def get_workers(self) -> List[UsersList]:
        df = pd.read_csv(self.sample_data_path)

        # Checks if sample user is clocked in.
        df['status'] = (
                (df['clocked_in'] <= self.current_time) &
                (df['clocked_out'] >= self.current_time)
        )

        output = [
            UsersList(
                id_number=row['id_number'],
                name=row['name'],
                location=row['location'],
                status=row['status']
            )
            for _, row in df.iterrows()
        ]

        return output
