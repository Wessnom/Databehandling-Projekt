"""
    Ok. Som ni ser nedan så har jag tagit myyycket från senaste Dashgenomgången som utgångspunkt. Basically ctrl+c ctrl+v.
    Försöker testa få in lite plots och union jack som sidbakgrund på något vis.
    
    Vad vill vi annars att sidan ska kunna visa? Alltså jag antar typ alla grafer, men på vilket sätt?
    Jag tycker personligen att det känns konstigt att ersätta px inbyggda valbarhetsfunktionalitet
    med menyer i Dash. Men helt klart behöver vi kunna välja mellan grejer, eller vill vi ha allt sammanställt på
    "startsidan", liksom side-by-side? Ska vi ha någon förklarande text? //ISAK
"""


from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template

# load_figure_template("darkly")

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

# Skapa en bakgrund med brittiska flaggan

app.layout = dbc.Container([
    html.Div([
        html.Img(src='/assets/UK-flag.png')
    ], style={
        "size": "100%",
        "position": "absolute",
        "top": "0",
        "left": "0",
        "z-index": "-1",
        "opacity": "0.2",
        "width": "100%",
        "height": "100%",
        "background-repeat": "repeat",
    }),
    dbc.Row([
        dbc.Col([
            html.H1("Great Britian - Olympic Games",
                className="text-center text-primary mt-3"),
        ], width=12)
    ]),
    
# Dropdown meny som gör noll just nu, men callar de olika sporterna i medal_trend_df
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="multi_dropdown", multi=True, searchable=False, 
                className="mb-1",
                options=[sport for sport in medal_trend_df],
                style={"color": "#333"},
                #value=""
            ),
            dcc.Graph(id="medal_graph",
                        figure= {},
                        )
        ])], justify="evenly"),
    
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

medal_trend_fig = px.line(medal_trend_df, 
    x=medal_trend_df.index,
    y=medal_trend_df.columns,
    title=f"Medal trend for {', '.join(medal_trend_df.columns)}",
    labels={'index': 'Year', 'value': 'Medals', 'variable': 'Sport'},
    color_discrete_sequence=['navy', 'red', 'green'],
)
medal_trend_fig.update_layout(
    xaxis = dict(
        tickmode='linear',
        tick0=1896,
        dtick=4,
    )
)

@callback(
    Output("medal_graph", "figure"),
    Input("single_dropdown", "value")
)
def update_medal_graph(sport):
    return medal_trend_fig

# @callback(
#     Output("closing_graph", "figure"),
#     Input("multi_dropdown", "value")
# )
# def update_closing_graph(symbols):
#     if symbols is None: symbols = []
#     df = stocks[stocks["Symbols"].isin(symbols)]
#     return px.line(df, x=df.index, y="Close", color="Symbols")

app.run(debug=True)