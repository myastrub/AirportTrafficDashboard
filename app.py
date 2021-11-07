import pandas as pd
import numpy as np
import data as ds
import json
from data import dataset
import constants as c
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from dash.dash_table.Format import Format, Scheme
import plotly.graph_objects as go
import plotly.express as px
from scipy import signal
from datetime import date

app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    '/assets/1_dashboard_styles.css'
    ], 
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ]
)
server = app.server

with open('assets/europe.geojson') as file:
    countries = json.load(file)

container_margins = {"margin-left": "2%", "margin-right": "2%"}
checklist_margins = {'margin': '2%'}
checklist_title_margins = {'margin': '3%'}

# TODO: remove sidebar and replace it with horizontal header

header = dbc.Container(children=[
    dbc.Row([
        dbc.Col(
            html.H3('Airport Traffic Dashboard',
                style={
                    'textAlign': 'center'
                }),
            xs=12, md=12, lg=12, xl=12,
        )
    ], justify='center',
    style={'backgroundColor': 'rgb(229, 236, 246)'}),
    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Dropdown(
                    options=[{'label': x, 'value': x} for x in ds.get_list_of_states(dataset)],
                    id='states_list',
                    multi=True,
                    clearable=True,
                    placeholder='Select States',
                    style={
                        'border': '0px',
                        'borderColor': 'transparent'
                    }
                )
            ])
            ,xs=12, md=12, lg=3, xl=3,
            align='center'
        ),
        dbc.Col(
            html.Div([
                dcc.Dropdown(
                    options=[{'label': x, 'value': x} for x in ds.get_list_of_airports(dataset)],
                    id='airports_list',
                    multi=True,
                    clearable=True,
                    placeholder='Select Airports',
                    style={
                        'border': '0px',
                        'borderColor': 'transparent'
                    }
                )
            ])
            ,xs=12, md=12, lg=3, xl=3,
            align='center'
        ),
        dbc.Col(
            html.Div([
            dcc.DatePickerRange(
                    id='period_selection',
                    min_date_allowed=ds.get_date(dataset, min),
                    max_date_allowed=ds.get_last_date(dataset),
                    start_date=ds.get_date(dataset, min),
                    end_date=ds.get_date(dataset, max)
                )
            ], className='period_and_movement')
            ,xs=6, md=6, lg=3, xl=3,
            align='center'
        ),
        dbc.Col(
            html.Div([
                dbc.Checklist(
                    options=[{'label': x, 'value': x} for x in ['Arrival', 'Departure']],
                    id='ifr_movements',
                    value=[x for x in ['Arrival', 'Departure']],
                    switch=True,
                    inline=True
                )
            ], className='period_and_movement')
            ,xs=6, md=6, lg=3, xl=3,
            align='center'
        )
    ], justify='center',
    className='control_container',
    style={'margin-bottom': '1%'}
    )
], fluid=True)

content = html.Div(
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Evolution of number of flights", className='section_title'),
                    dcc.Graph(
                        id='number_of_flights',
                        config={'displaylogo':False}
                    )
                ])
                ,xs=12, md=12, lg=12, xl=12
            )
        ]),
    ], fluid=True)
)

table_container = html.Div(
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5(
                        "Top 5 Airports (NM recorded flights)",
                        className='section_title',
                        style={'margin-bottom': '4%'}),
                    html.Div([], id='div_top_5_nm_airports')
                ])
            ],xs=12, md=12, lg=12, xl=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5(
                        "Top 5 Airports (Airport recorded flights)", 
                        className='section_title',
                        style={
                            'margin-bottom': '4%',
                            'margin-top': '3%'
                            }),
                    html.Div([], id='div_top_5_apt_airports')
                ])
            ],xs=12, md=12, lg=12, xl=12)
        ])
        
    ], fluid=True)
)

state_summary_container = dbc.Container(
    dbc.Row(
         dbc.Col(
            html.Div([
                html.H5(
                    "Daily average flights per state",
                    className='section_title'
                ),
                dcc.Graph(
                    id='map_summary',
                    config={'displaylogo':False}
                )
            ])
        )
    ), fluid=True
)

combined_container = html.Div([dbc.Container(children=[
    dbc.Row([
        dbc.Col(
            content
            ,xs=12, md=12, lg=7, xl=7
        ),
        dbc.Col(
            state_summary_container
            ,xs=12, md=12, lg=5, xl=5
        ) 
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5("Seasonal variability of traffic", className='section_title'),
                dcc.Graph(
                    id='seasonal_variability',
                    config={'displaylogo':False},
                    style={'margin-left': '2%'}
                )
            ])
            ,xs=12, md=12, lg=8, xl=8
        ),
        dbc.Col([
                html.Div([
                    html.H5(
                        "Top 5 Airports",
                        className='section_title'
                    ),
                    html.H6(
                        "(NM recorded flights)",
                        className='section_title',
                        style={'margin-bottom': '4%'}),
                    html.Div([
                        # generate_table(dataset, 'top_5_nm_airports', 'NM')
                    ], id='div_top_5_nm_airports')
                ])
            ],xs=12, md=12, lg=2, xl=2
        ),
        dbc.Col([
                html.Div([
                    html.H5(
                        "Top 5 Airports",
                        className='section_title'
                    ),
                    html.H6(
                        "(Airport recorded flights)",
                        className='section_title',
                        style={'margin-bottom': '4%'}),
                    html.Div([
                        # generate_table(dataset, 'top_5_apt_airports', 'APT')
                    ], id='div_top_5_apt_airports')
                ])
            ],xs=12, md=12, lg=2, xl=2)
    ], style={'margin-top': '1%'}
    )
], fluid=True)
])



footer = dbc.Container(children=[
    dbc.Row(
        dbc.Col(
            html.Footer(
                html.Div(
                    children=[
                        html.Hr(style={"border-color": "#fff"}),
                        html.H5(
                             "About airport traffic dashboard"
                        ),
                        html.P(
                            children=[
                                "This small dashboard has been created using the data coming from EUROCONTROL, the European Organisation for the Safety of Air Navigation.",
                                html.Br(),
                                "The dataset used in the dashboard can be found on  ",
                                html.A(
                                    href="https://ansperformance.eu/data/",
                                    children="Aviation Intelligence Portal",
                                ),
                                ".",
                                html.Br(),
                                "The credits for the map of Europe go to Justas (",
                                html.A(
                                    href="https://github.com/leakyMirror",
                                    children="leakyMirror"
                                ),
                                ")."
                            ]
                        ),
                    ], style={"font-size": "90%"},   
                )
            )
        )
    )
])

app.layout=html.Div(children=[
    # html.H3('Airport Traffic Dashboard', style={
    #    'textAlign': 'center',
    #    'margin': '20px'
    # }, className='main-wrapper'),
    header,
    combined_container,
    footer
])


def generate_table(data, id, source):
    generated_table = dash_table.DataTable(
        id=id,
        columns = [
            {
            'name': 'Airport', 
            'id': c.AIRPORT_NAME
            },
            {
                'name': 'Daily average flights', 
                'id': c.DAILY_AVERAGE,
                'type': 'numeric',
                'format': Format(precision=1, scheme=Scheme.fixed)
            }
        ],
        style_as_list_view=True,
        style_header={
            'fontWeight': 'bold'
        },
        style_cell={
            'textAlign': 'left',
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell_conditional=[
            {
                'if': {'column_id': c.DAILY_AVERAGE},
                'textAlign': 'right'
            }
        ],
        data=ds.get_top_flight_airports(data, source).to_dict('records')
    )
    return generated_table





@app.callback(
    Output('states_list', 'options'),
    Input('airports_list', 'value')
)
def update_states_list(airports):
    if airports:
        filtered_dataset = dataset[
            dataset[c.AIRPORT_NAME].isin(airports)
        ]
        return [{'label': x, 'value': x} for x in ds.get_list_of_states(filtered_dataset)]
    else:
        return [{'label': x, 'value': x} for x in ds.get_list_of_states(dataset)]


@app.callback(
    Output('airports_list', 'options'),
    Input('states_list', 'value')
)
def update_airports_list(states):
    if states:
        filtered_dataset = dataset[
            dataset[c.STATE_NAME].isin(states)
        ]
        return [{'label': x, 'value': x} for x in ds.get_list_of_airports(filtered_dataset)]
    else:
        return [{'label': x, 'value': x} for x in ds.get_list_of_airports(dataset)]


@app.callback(
    Output('div_top_5_nm_airports', 'children'),
    Output('div_top_5_apt_airports', 'children'),
    Input('states_list', 'value'),
    Input('period_selection', 'start_date'),
    Input('period_selection', 'end_date')
)
def update_airports_tables(states, start_date, end_date):
    filtered_dataset = ds.filter_dataset(
        data=dataset,
        states=states, 
        start_date=start_date, 
        end_date=end_date
    )
    returned_tables = (
        generate_table(filtered_dataset, 'top_5_nm_airports', 'NM'), 
        generate_table(filtered_dataset, 'top_5_apt_airports', 'APT')
    )
    return returned_tables

@app.callback(
    Output('number_of_flights', 'figure'),
    Input('airports_list', 'value'),
    Input('states_list', 'value'),
    Input('ifr_movements', 'value'),
    Input('period_selection', 'start_date'),
    Input('period_selection', 'end_date')
)
def update_number_of_flights_figure(airports, states, ifr_movements, start_date, end_date):
    
    filtered_dataset = ds.filter_dataset(
        data=dataset,
        airports=airports,
        states=states,
        start_date=start_date,
        end_date=end_date
    )

    flight_columns = ds.get_flight_columns(ifr_movements)

    graph_data = ds.get_number_of_flights(filtered_dataset, flight_columns)

    chart_layout = go.Layout(
        margin={'l': 15, 'r': 15, 't': 20, 'b': 30}
    )

    fig_number_of_flights = go.Figure(layout=chart_layout)

    fig_number_of_flights.add_trace(
        go.Scatter(
            x=graph_data[c.DATE],
            y=signal.savgol_filter(
                graph_data[flight_columns[0]], 53, 3
            ),
            mode='lines',
            name='Number of flights (recorded by NM)'
        )
    )

    if ds.has_airport_data(graph_data):
        fig_number_of_flights.add_trace(
            go.Scatter(
                x=graph_data[c.DATE],
                y=signal.savgol_filter(
                    graph_data[flight_columns[1]], 53, 3
                ),
                mode='lines',
                name='Number of flights (recorded by airports)'
            )
        )

    fig_number_of_flights.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig_number_of_flights


@app.callback(
    Output('seasonal_variability', 'figure'),
    Input('airports_list', 'value'),
    Input('states_list', 'value'),
    Input('ifr_movements', 'value'),
    Input('period_selection', 'start_date'),
    Input('period_selection', 'end_date')
)
def update_seasonal_variability(airports, states, ifr_movements, start_date, end_date):
    filtered_dataset = ds.filter_dataset(
        data=dataset,
        airports=airports,
        states=states,
        start_date=start_date,
        end_date=end_date
    )
    
    flight_columns = ds.get_flight_columns(ifr_movements)

    graph_data = ds.get_average_per_month(filtered_dataset, flight_columns)

    chart_layout = go.Layout(
        margin={'l': 15, 'r': 15, 't': 20, 'b': 30},
        height=340
    )

    fig_seasonal_variability = go.Figure(layout=chart_layout)

    fig_seasonal_variability.add_trace(
        go.Scatter(
            x=graph_data[c.MONTH_MON],
            y=graph_data[flight_columns[0]],
            mode='lines+markers',
            name='Daily average number of flights (recorded by NM)'
        )
    )
    if ds.has_airport_data(graph_data):
        fig_seasonal_variability.add_trace(
            go.Scatter(
                x=graph_data[c.MONTH_MON],
                y=graph_data[flight_columns[1]],
                mode='lines+markers',
                name='Daily average number of flights (recorded by airports)'
            )
        )

    fig_seasonal_variability.update_layout(legend=dict(
        orientation='h',
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return fig_seasonal_variability


@app.callback(
    Output('map_summary', 'figure'),
    Input('ifr_movements', 'value'),
    Input('period_selection', 'start_date'),
    Input('period_selection', 'end_date')
)
def update_map_summary(ifr_movements, start_date, end_date):
    flight_columns = ds.get_flight_columns(ifr_movements)
    final_date = pd.to_datetime(end_date)
    filtered_dataset = dataset[
        dataset[c.DATE].eq(final_date)
    ]
    graph_data = ds.get_daily_average_per_state(filtered_dataset, flight_columns)
    graph_data = graph_data[[c.STATE_NAME, flight_columns[0]]]

    fig_map_summary = px.choropleth(graph_data, geojson=countries, locations=c.STATE_NAME, color=flight_columns[0],
                           color_continuous_scale="Viridis",
                           range_color=(0, max(graph_data[flight_columns[0]])),
                           featureidkey="properties.NAME",
                           scope="europe",
                           labels={flight_columns[0]:'Number of flights<br>on {}'.format(
                               final_date.strftime('%d/%m%/%Y')
                           )}
    )

    fig_map_summary.update_geos(fitbounds="locations", visible=False)
    fig_map_summary.update_layout(margin={"r":0,"t":20,"l":0,"b":30})

    return fig_map_summary


if __name__ == '__main__':
    app.run_server(debug=True)

# 229, 236, 246
