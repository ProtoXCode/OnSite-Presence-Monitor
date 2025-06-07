from dash import Dash, html

from api_client.mock_client import MockERPClient
from logger import logger

erp_client = MockERPClient()
active_workers = [w for w in erp_client.get_workers() if w.status]

app = Dash()

logger.info(f'Active workers found: {len(active_workers)}')

app.layout = html.Div([
    html.H2('OnSite Presence Monitor'),
    html.Div([
        html.Div([
            html.Img(src=f'assets/employee_images/{worker.id_number}.png'),
            html.P(worker.name)
        ], className="card")
        for worker in active_workers
    ], className="dashboard-container")
])

if __name__ == '__main__':
    logger.info('Starting OnSite Presence Monitor from app.py')
    app.run(debug=True)
