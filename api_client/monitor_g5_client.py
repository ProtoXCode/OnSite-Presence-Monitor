import requests
import re
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

API URL build:
https://{host}:8001/{languageCode}/{companyNumber}/api/v1
- Host          - IP or hostname
- LanguageCode  - Two letter language code
- CompanyNumber - Database-number (Ex. 004.1, 004 is the database, 1 company ID) 

Expected API endpoints:
- GET /api/v1/TimeRecording/AttendanceChart
- GET /api/v1/Persons

Returned values are mapped to the UsersList dataclass for use by the app.
"""

# Activating DEBUG will print out part of the responses to check filtering.
DEBUG = False


class MonitorG5Client(BaseERPClient):
    def __init__(self) -> None:
        config_path = Path(__file__).resolve().parent.parent / 'config.yaml'
        if config_path.exists():
            with open(config_path, mode='r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        else:
            logger.critical(f'Config.yaml not found: {config_path}')
            raise FileNotFoundError('config.yaml not found')

        self.api_url = config.get('erp_api_url', '').rstrip('/')
        self.api_user = config.get('erp_api_user', '')
        self.api_key = config.get('erp_api_key', '')
        self.target_location = config.get('location', 'Factory')
        self.allowed_locations = ['Factory', 'Office']
        self._validate_api_url(self.api_url)  # Check if URL format is correct

        self.session = requests.Session()
        self.session.verify = False

    def authenticate(self) -> str:
        """ Authenticate with the Monitor G5 API """
        header = {
            'content-type': 'application/json',
            'cache-control': 'no-cache',
            'accept': 'application/json'
        }

        payload = {
            'Username': self.api_user,
            'Password': self.api_key,
            'ForceRelogin': True
        }

        response = requests.post(
            url=f'{self.api_url}/login',
            headers=header,
            json=payload,
            verify=False
        )

        session_id = response.headers['x-monitor-sessionid']

        self.session.headers.update({
            'accept': 'application/json',
            'x-monitor-sessionid': session_id
        })

        return session_id

    def get_workers(self) -> List[UsersList]:
        logger.info('Fetching REAL active attendance from Monitor ERP...')

        try:
            self.authenticate()

            persons = self._fetch_persons()
            attendance = self._fetch_attendance_chart()

            # Collect only workers who are actively clocked in
            active_ids = {
                str(a['EmployeeId'])
                for a in attendance
                if not a.get('IsClosedInterval', True)
            }

            workers = []

            for pid in active_ids:
                person = persons.get(pid)
                if not person:
                    logger.warning(
                        f'No person info found for EmployeeId {pid}')
                    continue

                # Use the *employee_number* for display / images,
                # fall back to pid if for some reason it's missing
                display_id = person.get('employee_number') or pid

                workers.append(UsersList(
                    id_number=int(display_id),
                    name=person['name'],
                    location=person.get('location', None),
                    status=True
                ))

            logger.info(f'Active workers: {len(workers)}')
            return workers

        except Exception as e:
            logger.error(f'MonitorG5Client error: {e}')
            return []

    @staticmethod
    def _validate_api_url(url: str) -> None:
        """
        Validates Monitor ERP API URL format:
        https://host:8001/cc/NNN.X/

        cc    = 2-letter country code
        NNN   = database number (001, 004, etc.)
        X     = company ID (Usually 1)
        """

        pattern = re.compile(
            r'^https://[A-Za-z0-9.\-]+:8001/[A-Za-z]{2}/[0-9]{3}.[0-9]+/?$'
        )

        if not pattern.match(url):
            logger.critical(f'Invalid Monitor ERP API URL: "{url}"')
            raise ValueError(
                f'Invalid ERP API URL format: "{url}". '
                'Expected format: https://host:800/cc/NNN.X/'
            )

    def _fetch_attendance_chart(self) -> List[dict]:
        """ Fetch real attendance info with EmployeeId + intervals. """
        url = f'{self.api_url}/api/v1/TimeRecording/AttendanceChart'
        res = self.session.get(url)

        if DEBUG:
            print('\n=== RAW ATTENDANCE CHART RESPONSE ===')
            print(res.status_code, res.text[:800], '...')  # Trim dump
            print('=== END RAW ATTENDANCE CHART RESPONSE ===\n')

        res.raise_for_status()
        return res.json()

    def _fetch_persons(self) -> Dict[str, dict]:
        url = f'{self.api_url}/api/v1/Common/Persons'
        res = self.session.get(url)

        if DEBUG:
            print("\n=== RAW PERSONS RESPONSE ===")
            print(res.status_code, res.text)  # Dump all
            print("=== END RAW PERSONS RESPONSE ===\n")

        res.raise_for_status()
        data = res.json()

        result = {
            str(p['Id']): {
                'employee_number': p.get('EmployeeNumber'),
                'name': f"{p.get('FirstName', '')} {p.get('LastName', '')}".strip(),
                'location': int(p.get('WarehouseId'))
            }
            for p in data
        }

        if DEBUG:
            print(f'{result=}')

        return result
