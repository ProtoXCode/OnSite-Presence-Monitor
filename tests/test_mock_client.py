from datetime import datetime

import pandas as pd

from api_client.mock_client import MockERPClient


def test_get_workers_active_status():
    client = MockERPClient()
    workers = client.get_workers()

    # Check that it returns a list
    assert isinstance(workers, list)

    # Check if each item is marked as status=True within working hours
    now = datetime.now().strftime('%H:%M')
    df = pd.read_csv(client.sample_data_path)

    for worker in workers:
        match = df[df['id_number'] == worker.id_number]
        assert not match.empty, (f'Worker ID {worker.id_number} not found in '
                                 f'test CSV')

        row = match.iloc[0]
        expected_status = (row['clocked_in'] <= now <= row['clocked_out'])
        assert worker.status == expected_status
