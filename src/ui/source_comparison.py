import pandas as pd
from dash import html, dcc, callback, Output, Input

from src.ui.common import corpus_dict, corpus_size

layout = html.Div([
    html.Label("Select the corpus", htmlFor="corpus-selector"),
    dcc.Dropdown(
        options=list(corpus_dict.keys()),
        value=list(corpus_dict.keys())[0],
        id="corpus-selector"
    ),

    html.Label("Select the amount of word to display", htmlFor="word-count-input"),
    dcc.Slider(0, 50, value=20, id="word-count-input"),



    dcc.Tabs(id="content-tabs", value="rva", children=[
        dcc.Tab(label="Reddit vs arxiv", value="rva"),
        dcc.Tab(label="Arxiv vs reddit", value="avr")
    ]),

    html.H3("Term Frequency-Inverse Document Frequency"),
    dcc.Graph(id="graph"),
])


@callback(
    Output('graph', "figure"),
    Input('content-tabs', 'value'),
    Input('corpus-selector', 'value'),
    Input('word-count-input', 'value')
)
def render_mrw(tab, select, count):
    # Selection du bon corpus
    corpus = corpus_dict[select]

    # Charger le corpus s'il ne l'est pas
    if not corpus.is_loaded():
        corpus.load(corpus_size)

    # Récuperation des id des document en fonction de sa source
    reddit_ids = list(map(lambda kv: kv[0], filter(lambda kv: kv[1].get_type() == "reddit", corpus.id2doc.items())))
    arxiv_ids = [i for i in range(corpus_size) if i not in reddit_ids]

    reddit_df = pd.DataFrame(corpus.mat_TFxIDF[reddit_ids, :].toarray(), columns=list(corpus.vocab.keys()))
    arxiv_df = pd.DataFrame(corpus.mat_TFxIDF[arxiv_ids, :].toarray(), columns=list(corpus.vocab.keys()))

    reddit_v = reddit_df.mean(axis=0)
    arxiv_v = arxiv_df.mean(axis=0)

    top = {
        "rva": reddit_v.nlargest(count).index,
        "avr": arxiv_v.nlargest(count).index
    }

    return {
        'data': [
            {
                'x': top[tab],
                'y': reddit_v.loc[top[tab]],
                'type': 'bar',
                'name': 'reddit'
            },
            {
                'x': top[tab],
                'y': arxiv_v.loc[top[tab]],
                'type': 'bar',
                'name': 'arxiv'
            }
        ]
    }