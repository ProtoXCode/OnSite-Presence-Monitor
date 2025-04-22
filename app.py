from dash import Dash, html
import pandas as pd
import datetime

# Get the current local time in hh:mm format
current_time = datetime.datetime.now().strftime('%H:%M')

# Sample data
df = pd.read_csv('data/sample_data.csv')
df['image'] = df['id_number'].apply(lambda x: f'assets/employee_images/{x}.png')
filtered_df = df[
    (df['clocked_in'] <= current_time) & (df['clocked_out'] >= current_time)]

# Initialize Dash app
app = Dash()

app.layout = html.Div(style={
    'backgroundColor': '#f5f7fa',
    'minHeight': '100vh',
    'padding': '40px',
    'fontFamily': 'Segoe UI, sans-serif'
}, children=[
    html.H2('INnOUT - Who\'s at Work', style={
        'textAlign': 'center',
        'color': '#333',
        'marginBottom': '30px'
    }),
    html.Div([
        html.Div([
            html.Img(src=row['image'], style={
                'height': '100px',
                'width': '100px',
                'objectFit': 'cover',
                'borderRadius': '50%',
                'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
            }),
            html.P(row['name'], style={
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
        for _, row in filtered_df.iterrows()
    ], style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'center'
    })
])

if __name__ == '__main__':
    app.run(debug=True)
