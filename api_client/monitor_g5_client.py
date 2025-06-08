import requests
from typing import List, Dict
from pathlib import Path

import yaml

from api_client.base_client import BaseERPClient, UsersList
from logger import logger

"""
MonitorG5Client
---------------

This ERP client implementation provides integration with the Monitor G5 API
to retrieve and filter currently clocked-in workers for use in the
OnSite Presence Monitor application.

It pulls raw attendance interval data from the Monitor TimeRecording API,
enriches that data with person metadata (name, location), and filters
the resulting user list by location (e.g. Factory, Office, Home Office).

The goal is to deliver an accurate, real-time list of personnel
physically present at a specified site — enabling use cases such as:

- Evacuation dashboards and roll calls
- Real-time personnel visibility
- Factory zone safety boards

This client adheres to the BaseERPClient interface and can be swapped
out with other ERP implementations (e.g. mock, database-backed) without
modifying the app itself.

Configuration is loaded from `config.yaml` and includes:
- erp_api_url: Base URL of the Monitor G5 API
- erp_api_key: Bearer token for authorization (if required)
- location: The physical site to filter for (e.g. "Factory")

Expected API endpoints:
- GET /v1/TimeRecording/AttendanceIntervals
- GET /v1/Persons

Returned values are mapped to the UsersList dataclass for use by the app.

"""


class MonitorG5Client(BaseERPClient):
    def __init__(self) -> None:
        config_path = Path('config.yaml')
        if config_path.exists():
            with open(config_path, mode='r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        else:
            logger.critical('Config.yaml not found.')
            raise FileNotFoundError('config.yaml not found')

        self.api_url = config.get('erp_api_url', '').rstrip('/')
        self.api_key = config.get('erp_api_key', '')
        self.target_location = config.get('location', 'Factory')

        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Accept': 'application/json'
            })

    def get_workers(self) -> List[UsersList]:
        logger.info('Fetching active intervals from Monitor ERP...')
        try:
            intervals = self._fetch_attendance_intervals()
            person_data = self._fetch_persons()

            workers = []
            seen = set()

            for interval in intervals:
                person_id = interval.get('PersonId')
                if not person_id or person_id in seen:
                    continue

                person_info = person_data.get(
                    str(person_id))  # ID might be a string
                if not person_info:
                    logger.warning(f'No person info found for ID {person_id}')
                    continue

                if person_info.get('location') != self.target_location:
                    continue

                workers.append(UsersList(
                    id_number=person_id,
                    name=person_info.get('name', f'ID {person_id}'),
                    location=person_info.get('location'),
                    status=True
                ))
                seen.add(person_id)

            logger.info(f'Active filtered workers: {len(workers)}')
            return workers

        except Exception as e:
            logger.error(f'MonitorG5Client error: {e}')
            return []

    def _fetch_attendance_intervals(self) -> List[dict]:
        url = f'{self.api_url}/v1/TimeRecording/AttendanceIntervals'
        res = self.session.get(url)
        res.raise_for_status()
        data = res.json()

        return [
            i for i in data
            if not i.get('IsClosedInterval', True)
               and not i.get('IsBreak', False)
               and i.get('AbsenceCodeId') is None
        ]

    def _fetch_persons(self) -> Dict[str, dict]:
        url = f'{self.api_url}/v1/Persons'
        res = self.session.get(url)
        res.raise_for_status()
        data = res.json()

        # Turn into {person_id: {name, location}} mapping
        return {
            str(p['Id']): {
                'name': f"{p.get('FirstName', '')} {p.get('LastName', '')}".strip(),
                'location': p.get('WorkLocation', 'Unknown')
            }
            for p in data
        }
