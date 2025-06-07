from dash import Dash, html

from api_client.mock_client import MockERPClient

erp_client = MockERPClient()
active_workers = [w for w in erp_client.get_workers() if w.status]

# Initialize Dash app
app = Dash()

app.layout = html.Div(style={
    'backgroundColor': '#f5f7fa',
    'minHeight': '100vh',
    'padding': '40px',
    'fontFamily': 'Segoe UI, sans-serif'
}, children=[
    html.H2('OnSite Presence Monitor', style={
        'textAlign': 'center',
        'color': '#333',
        'marginBottom': '30px'
    }),
    html.Div([
        html.Div([
            html.Img(src=f'assets/employee_images/{worker.id_number}.png',
                     style={
                         'height': '100px',
                         'width': '100px',
                         'objectFit': 'cover',
                         'borderRadius': '50%',
                         'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
                     }),
            html.P(worker.name, style={
                'textAlign': 'center',
                'marginTop': '10px',
                'fontWeight': 'bold',
                'color': '#444'
            })
        ], style={
            'display': 'inline-block',
            'margin': '20px',
            'textAlign': 'center',
            'backgroundColor': '#fff',
            'padding': '15px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'
        })
        for worker in active_workers
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
