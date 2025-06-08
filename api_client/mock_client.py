from typing import List
from datetime import datetime
from pathlib import Path

import pandas as pd

from .base_client import BaseERPClient, UsersList

"""
MockERPClient
-------------

A mock implementation of the BaseERPClient interface, used for local
development and testing of the OnSite Presence Monitor application.

This client reads a static CSV file from the local `data/` directory
containing fake employee records, including clock-in/out times, names,
locations, and IDs.

It simulates the logic of a real ERP client by determining which
employees are currently clocked in based on the system time at app startup.

Fields expected in the sample_data.csv:
- id_number: Unique ID of the employee
- name: Employee name
- location: Physical work location (e.g. "Factory", "Office")
- clocked_in: Time the user is expected to be present (HH:MM)
- clocked_out: Time the user is no longer considered present (HH:MM)

This client is primarily used for:
- Testing the dashboard UI without ERP connectivity
- Rapid prototyping of new features
- Demonstrating location filtering logic

Output is a list of UsersList dataclass instances, consistent with all
other ERP client implementations.
"""


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
