from dash import Dash, dcc, html, Input, Output, callback

from src.ui.source_comparison import layout as sc_layout
from src.ui.search_engine import layout as se_layout
from src.ui.corpus_comparison import layout as cc_layout

layout_dict = {
    "sc": sc_layout,
    "se": se_layout,
    "cc": cc_layout
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

application = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

application.layout = html.Div([
    dcc.Tabs(id='main-tabs', value='sc', children=[
        dcc.Tab(label='Source comparison', value='sc'),
        dcc.Tab(label='Search engine', value='se'),
        dcc.Tab(label='Corpus comparison', value='cc'),
    ]),

    html.Div(id='tabs-content')
])


@callback(
    Output('tabs-content', 'children'),
    Input('main-tabs', 'value')
)
def render(tab):
    return layout_dict[tab]
