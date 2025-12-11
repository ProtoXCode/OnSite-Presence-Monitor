import urllib3
import os

import yaml
from dash import Dash, html, Output, Input, dcc

# Change the imported client to mathch your ERP system.
from api_client.mock_client import MockERPClient as APIClient
from logger import logger

"""
OnSite Presence Monitor
=======================

Author: Tom Erik Harnes
Created: 2025-06
Version: 1.1.1

A Dash-based dashboard for displaying currently clocked-in employees
retrieved from a connected ERP system. Primarily designed for use in
factory and industrial environments, where knowing who is physically
present on-site is critical for safety, evacuation, and visibility.

Supports:
- Real-time auto-refresh of presence data
- Location-based filtering (Factory, Office, Remote)
- Configurable ERP client (mock, Monitor G5, etc.)
- Responsive UI with image fallback handling
- Kiosk mode and production deployment (via Waitress)

Configuration is managed via `config.yaml`, generated automatically
on first launch if missing. Employee images are loaded from the path
defined in the config file.

This file is the entry point for both development and production use.

Usage:
    python app.py             # development mode
    python run_production.py  # production via Waitress
"""

APP_TITLE = 'OnSite Presence Monitor'
__version__ = '1.1.1'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_CONFIG = {
    'location': 'Factory',
    'update_interval': 30000,
    'image_directory': 'assets/employee_images/',
    'erp_api_url': 'https://{host}:8001/{languageCode}/{companyNumber}/',
    'erp_api_key': '',
    'erp_api_client': '',
    'erp_api_secret': '',
    'db_type': '',
    'db_host': '',
    'db_port': 5432,
    'db_name': 'onsite',
    'db_user': 'user',
    'db_password': 'password',
    'jwt_secret': '',
    'location:': 1,
    'jwt_algo': 'HS256'
}


def load_config(path='config.yaml') -> dict:
    """ Loads local config file, creates a default if the file is missing. """
    if not os.path.exists(path):
        logger.info(f'No config file found, creating default at {path}')
        with open(path, mode='w', encoding='utf-8') as f:
            yaml.dump(DEFAULT_CONFIG, f)
        return DEFAULT_CONFIG
    with open(path, mode='r', encoding='utf-8') as f:
        return yaml.safe_load(f)


CONFIG = load_config()
UPDATE_INTERVAL = CONFIG['update_interval']
IMAGE_DIRECTORY = CONFIG['image_directory']
LOCATION = CONFIG['location']

erp_client = APIClient()
app = Dash(title=APP_TITLE,
           meta_tags=[
               {'name': 'viewport', 'content':
                   'width=device-width, initial-scale=1'},
               {'name': 'description',
                'content': 'Live factory presence monitor dashboar'}
           ])

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

app.layout = html.Div([
    html.H2(APP_TITLE),
    dcc.Interval(id='update-interval', interval=UPDATE_INTERVAL,
                 n_intervals=0),
    html.Div(id='worker-container', className='dashboard-container')
])


def get_image_path(worker_id: int) -> str:
    path = f'{IMAGE_DIRECTORY}{worker_id}.png'
    if not os.path.exists(path):
        return 'assets/default.png'
    return path


def render_workers() -> list[html.Div] | html.Div:
    active_workers = [w for w in erp_client.get_workers() if
                      w.status and w.location == LOCATION]
    logger.info(f'Active workers updated: {len(active_workers)}')

    if not active_workers:
        return html.Div('No one is currently clocked in.',
                        className='empty-message')

    return [
        html.Div([
            html.Img(
                src=get_image_path(worker.id_number),
            ),
            html.P(worker.name)
        ], className='card')
        for worker in active_workers
    ]


@app.callback(
    Output('worker-container', 'children'),
    Input('update-interval', 'n_intervals'))
def update_worker_cards(_):
    return render_workers()


if __name__ == '__main__':
    logger.info('Starting OnSite Presence Monitor from app.py')
    app.run(debug=True)
