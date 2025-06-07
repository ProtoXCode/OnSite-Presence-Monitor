from dash import Dash, html, Output, Input, dcc

from api_client.mock_client import MockERPClient
from logger import logger

APP_TITLE = 'OnSite Presence Monitor'
UPDATE_INTERVAL = 30_000
IMAGE_DIRECTORY = 'assets/employee_images/'

erp_client = MockERPClient()
app = Dash(title=APP_TITLE)

app.layout = html.Div([
    html.H2(APP_TITLE),
    dcc.Interval(id='update-interval', interval=UPDATE_INTERVAL,
                 n_intervals=0),
    # every 30 seconds
    html.Div(id='worker-container', className='dashboard-container')
])


def render_workers() -> list or html:
    active_workers = [w for w in erp_client.get_workers() if w.status]
    logger.info(f"Active workers updated: {len(active_workers)}")

    if not active_workers:
        return html.Div("No one is currently clocked in.",
                        className='empty-message')

    return [
        html.Div([
            html.Img(src=f'{IMAGE_DIRECTORY}{worker.id_number}.png'),
            html.P(worker.name)
        ], className="card")
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
