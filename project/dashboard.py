import sqlite3
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def load_data():
    conn = sqlite3.connect('cluster_usage.db')
    query = 'SELECT * FROM cluster_usage'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_data()
df['Start'] = pd.to_datetime(df['Start'], errors='coerce', format='%Y-%m-%dT%H:%M:%S')
df['End'] = pd.to_datetime(df['End'], errors='coerce', format='%Y-%m-%dT%H:%M:%S')

# Filter out NaN or None values from 'User' column
valid_users = df['User'].dropna().unique()

# Generate options for the dropdown
dropdown_options = [{'label': user, 'value': user} for user in valid_users]


# App layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("HPC Cluster Usage Dashboard", className='text-center text-primary mb-4'))),
    
    dbc.Row([
        dbc.Col([
            html.Label('Select User:'),
            dcc.Dropdown(
                id='user-dropdown',
                options=dropdown_options,
                value=valid_users[0] if valid_users.size > 0 else None,
                clearable=False
            ),
        ], width=4),

        dbc.Col([
            html.Label('Select Date Range:'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=df['Start'].min(),
                end_date=df['End'].max(),
                display_format='YYYY-MM-DD'
            ),
        ], width=8),
    ]),

    dbc.Row(dbc.Col(dcc.Graph(id='cpu-usage-graph'))),

    dbc.Row(dbc.Col(dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10
    ))),
])

# Callback for updating the graph
@app.callback(
    Output('cpu-usage-graph', 'figure'),
    [Input('user-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(selected_user, start_date, end_date):
    # Convert date strings to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the DataFrame
    filtered_df = df[(df['User'] == selected_user) &
                     (df['Start'] >= start_date) &
                     (df['End'] <= end_date)]

    # Update the plot
    fig = px.bar(filtered_df, x='User', y='AllocCPUS', title='CPU Usage per User')
    fig.update_layout(transition_duration=500)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

