from unittest.mock import patch, MagicMock

import pytest

from api_client.monitor_g5_client import MonitorG5Client

GOOD_CONFIG = {
    'erp_api_url': 'https://testhost:8001/no/001.1/',
    'erp_api_user': 'dummy',
    'erp_api_key': 'dummy',
    'location': 'Factory'
}


@pytest.fixture(autouse=True)
def fake_config(monkeypatch):
    monkeypatch.setattr(
        'api_client.monitor_g5_client.yaml.safe_load',
        lambda *_: GOOD_CONFIG
    )


@patch('api_client.monitor_g5_client.requests.Session.get')
def test_fetch_persons(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {'Id': 10, 'FirstName': 'Tom', 'LastName': 'Harnes',
         'WarehouseId': 1},
        {'Id': 11, 'FirstName': 'Jane', 'LastName': 'Doe',
         'WarehouseId': 2}
    ]
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    client = MonitorG5Client()

    persons = client._fetch_persons()

    assert persons['10']['name'] == 'Tom Harnes'
    assert persons['10']['location'] == 1
    assert persons['11']['name'] == 'Jane Doe'


@patch('api_client.monitor_g5_client.requests.Session.get')
def test_fetch_attendance_chart(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {'EmployeeId': 10, 'IsClosedInterval': False},
        {'EmployeeId': 11, 'IsClosedInterval': True},
    ]
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    client = MonitorG5Client()
    result = client._fetch_attendance_chart()

    assert len(result) == 2
    assert result[0]['EmployeeId'] == 10


@patch('api_client.monitor_g5_client.MonitorG5Client.authenticate')
@patch('api_client.monitor_g5_client.MonitorG5Client._fetch_attendance_chart')
@patch('api_client.monitor_g5_client.MonitorG5Client._fetch_persons')
def test_get_workers(mock_persons, mock_attendance, mock_auth):
    mock_auth.return_value = 'SESSION-123'

    mock_attendance.return_value = [
        {'EmployeeId': 10, 'IsClosedInterval': False},
        {'EmployeeId': 11, 'IsClosedInterval': True},
    ]

    mock_persons.return_value = {
        '10': {'name': 'Tom Erik Harnes', 'location': 1},
        '11': {'name': 'Jane Doe', 'location': 2},
    }

    client = MonitorG5Client()

    workers = client.get_workers()

    assert len(workers) == 1
    assert workers[0].id_number == 10
    assert workers[0].name == 'Tom Erik Harnes'
    assert workers[0].status is True


def test_invalid_api_url(monkeypatch):
    monkeypatch.setattr(
        'api_client.monitor_g5_client.yaml.safe_load',
        lambda *_: {'erp_api_url': 'http://bad-url.com'}
    )

    with pytest.raises(ValueError):
        MonitorG5Client()
