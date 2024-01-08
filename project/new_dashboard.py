import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc

from analysis import parse_time, getTotalTimeUser, getTotalTimeAll, calculate_daily_cpu_times, TotalTimeAccountAll, topUsers

# Initialize the Dash app with Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def load_data():
  file_path = './project/cluster_usage_data.txt'
  df = pd.read_csv(file_path, delimiter='|')
  df["CPUTimeSeconds"] = df["CPUTime"].apply(parse_time)
  df['Start'] = pd.to_datetime(df['Start'], errors='coerce', format='%Y-%m-%dT%H:%M:%S')
  df['End'] = pd.to_datetime(df['End'], errors='coerce', format='%Y-%m-%dT%H:%M:%S')
  return df

df = load_data()

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

     dbc.Row([
        dbc.Col([
            html.Label('Select Metric:'),
            dcc.Dropdown(
                id='metric-dropdown',
                options=[
                    {'label': 'CPU Usage', 'value': 'cpu_usage'},
                    {'label': 'Time Usage', 'value': 'time_usage'},
                    {'label': 'Daily CPU Times', 'value': 'daily_cpu_times'},
                    {'label': 'Total Time per Account', 'value': 'total_time_account'},
                    {'label': 'Top Users', 'value': 'top_users'}
                ],
                value='cpu_usage',
                clearable=False
            ),
        ], width=4),
    ]),

    dbc.Row(dbc.Col(dcc.Graph(id='usage-graph'))),
])

@app.callback(
    Output('usage-graph', 'figure'),
    [Input('user-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('metric-dropdown', 'value')]
)
def update_graph(selected_user, start_date, end_date, selected_metric):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the DataFrame
    filtered_df = df[(df['User'] == selected_user) &
                     (df['Start'] >= start_date) &
                     (df['End'] <= end_date)]

    if selected_metric == 'cpu_usage':
        # Logic for CPU usage visualization
        fig = px.bar(filtered_df, x='User', y='AllocCPUS', title='CPU Usage per User')
    elif selected_metric == 'time_usage':
        # Logic for time usage visualization
        total_time = getTotalTimeUser(selected_user)
        fig = px.bar(x=[selected_user], y=[total_time], labels={'x': 'User', 'y': 'Total Time (Hours)'},
                     title='Total Time Usage per User (Hours)')
         # Integration of other functions
    elif selected_metric == 'daily_cpu_times':
        # Assuming calculate_daily_cpu_times returns a DataFrame suitable for plotting
        daily_data = calculate_daily_cpu_times(filtered_df)
        fig = px.line(daily_data, x='Date', y='CPUTimeSeconds', title='Daily CPU Times for User')

    elif selected_metric == 'total_time_account':
        # Assuming TotalTimeAccountAll returns a DataFrame suitable for plotting
        account_data = TotalTimeAccountAll()
        fig = px.pie(account_data, values='CPUTimeSeconds', names=account_data.index, title='Total Time per Account')
        # Integration of topUsers function
    elif selected_metric == 'top_users':
        top_users_data = topUsers(df, start_date, end_date).head(20)  # Get top 20 users
        fig = px.bar(top_users_data, x=top_users_data.index, y='CPUTimeSeconds', title='Top 20 Users')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
