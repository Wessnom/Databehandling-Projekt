"""
    Ok. Som ni ser nedan så har jag tagit myyycket från senaste Dashgenomgången som utgångspunkt. Basically ctrl+c ctrl+v.
    Försöker testa få in lite plots och union jack som sidbakgrund på något vis. //ISAK
"""


from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template

load_figure_template("darkly")

df_UK = pd.read_csv("../Databehandling-Projekt/data/athlete_events.csv").query("NOC == 'GBR'")

gb_rowing = df_UK[df_UK['Sport'] == 'Rowing']
gb_cycling = df_UK[df_UK['Sport'] == 'Cycling']
gb_sailing = df_UK[df_UK['Sport'] == 'Sailing']

medal_trend_rowing = gb_rowing.dropna(subset=['Medal']).groupby('Year')['Medal'].count()
medal_trend_cycling = gb_cycling.dropna(subset=['Medal']).groupby('Year')['Medal'].count()
medal_trend_sailing = gb_sailing.dropna(subset=['Medal']).groupby('Year')['Medal'].count()

medal_trend_df = pd.DataFrame({'Rowing': medal_trend_rowing, 'Cycling': medal_trend_cycling, 'Football': medal_trend_sailing}).fillna(0)

app = Dash(__name__,
        external_stylesheets=[dbc.themes.DARKLY],
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"},],)

# Skapa en bakgrund med brittiska flaggan (funkar ej)
# Hur kombo med container layout nedan?

# app.layout = html.Div(style={
#     "background-image": "url("assets/UK-flag.png")",
#     "background-repeat": "no-repeat",
#     "background-position": "right top",
#     "background-size": "150px 100px"
# }),

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Great Britian, Olympic Games", className="text-center text-primary mt-3"),
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="single_dropdown", multi=False, searchable=False, 
                className="mb-2",
                options=[sport for sport in medal_trend_df],
                style={"color": "#333"},
                #value=""
            ),
            dcc.Graph(id="medal_graph",
                        figure= {})
        ], xs=12, sm=11, md=10, lg=5),
        
        dbc.Col([
            dcc.Dropdown(
                id="multi_dropdown", multi=True, searchable=False, 
                className="mb-2",
                #options=[stock for stock in stocks["Symbols"].unique()],
                style={"color": "#333"},
                #value=["AAPL", "MSFT", "MRNA", "BNTX", "PFE"]
            ),
            dcc.Graph(id="closing_graph",
                        figure= {})
        ], xs=12, sm=11, md=10, lg=5),
    ], justify="evenly"),
    
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                #stocks.to_dict("records"), 
                #id="stock_table", 
                #columns=[{"name": i, "id": i} for i in stocks.columns], 
                page_size=10, 
                style_cell={"textAlign": "left", "backgroundColor": "#333", "color": "#fff"}, 
                style_header={"backgroundColor": "#333", "color": "#fff"}, 
                style_data={"backgroundColor": "#333", "color": "#fff"}
                ),
        ], width=12)
    ]),
    
], fluid=True)

@callback(
    Output("medal_graph", "figure"),
    Input("single_dropdown", "value")
)
def update_volume_graph(sport):
    return px.histogram(medal_trend_df)

# @callback(
#     Output("closing_graph", "figure"),
#     Input("multi_dropdown", "value")
# )
# def update_closing_graph(symbols):
#     if symbols is None: symbols = []
#     df = stocks[stocks["Symbols"].isin(symbols)]
#     return px.line(df, x=df.index, y="Close", color="Symbols")

app.run(debug=True)