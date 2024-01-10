import pandas as pd
from dash import html, dcc, callback, Output, Input

from src.ui.common import corpus_dict, corpus_size

corpus_names = list(corpus_dict.keys())

layout = html.Div([
    html.Label("Select the first corpus", htmlFor="corpus-selector-1"),
    dcc.Dropdown(
        options=corpus_names,
        value=corpus_names[0],
        id="corpus-selector-1"
    ),

    html.Label("Select the second corpus", htmlFor="corpus-selector-2"),
    dcc.Dropdown(
        options=corpus_names,
        value=corpus_names[1],
        id="corpus-selector-2"
    ),

    html.Label("Select the amount of word to display", htmlFor="word-count-input"),
    dcc.Slider(0, 50, value=20, id="word-count-input"),

    dcc.Tabs(id="content-tabs", value="def", children=[
        dcc.Tab(label="Reddit vs arxiv", value="def", id="def"),
        dcc.Tab(label="Arxiv vs reddit", value="rev", id="rev")
    ]),

    html.Div([
        html.Div([
            html.H3("Term Frequency"),
            dcc.Graph(id="graph-tf")
        ], className="six columns"),

        html.Div([
            html.H3("Term Frequency-Inverse Document Frequency"),
            dcc.Graph(id="graph-tfidf")
        ], className="six columns")
    ], className="row"),
])


@callback(
    Output('def', 'label'),
    Output('rev', 'label'),
    Input('corpus-selector-1', 'value'),
    Input('corpus-selector-2', 'value')
)
def update_labels(c1, c2):
    return f"{c1} vs {c2}", f"{c2} vs {c1}"


@callback(
    Output('graph-tf', 'figure'),
    Output('graph-tfidf', 'figure'),
    Input('corpus-selector-1', 'value'),
    Input('corpus-selector-2', 'value'),
    Input('word-count-input', 'value'),
    Input('content-tabs', 'value'),
)
def update_matrices(selected_corpus_1, selected_corpus_2, count, tab):
    corpus_1 = corpus_dict[selected_corpus_1]
    corpus_2 = corpus_dict[selected_corpus_2]

    if not corpus_1.is_loaded():
        corpus_1.load(corpus_size)
    if not corpus_2.is_loaded():
        corpus_2.load(corpus_size)

    tf_matrix_df_1 = pd.DataFrame(corpus_1.mat_TF.toarray(), columns=list(corpus_1.vocab.keys()))
    tf_matrix_df_2 = pd.DataFrame(corpus_2.mat_TF.toarray(), columns=list(corpus_2.vocab.keys()))
    
    average_values_1 = tf_matrix_df_1.mean(axis=0)
    average_values_2 = tf_matrix_df_2.mean(axis=0)

    tfidf_matrix_df_1 = pd.DataFrame(corpus_1.mat_TFxIDF.toarray(), columns=list(corpus_1.vocab.keys()))
    tfidf_matrix_df_2 = pd.DataFrame(corpus_2.mat_TFxIDF.toarray(), columns=list(corpus_2.vocab.keys()))

    average_values_idf_1 = tfidf_matrix_df_1.mean(axis=0)
    average_values_idf_2 = tfidf_matrix_df_2.mean(axis=0)

    top = {
        'def':
            {
                'tf': average_values_1.nlargest(count).index,
                'tfidf': average_values_idf_1.nlargest(count).index
            },
        'rev':
            {
                'tf': average_values_2.nlargest(count).index,
                'tfidf': average_values_idf_2.nlargest(count).index
            }
    }

    average_values_1 = average_values_1.reindex(average_values_1.index.union(average_values_2.index), fill_value=0)
    average_values_2 = average_values_2.reindex(average_values_1.index, fill_value=0)
    average_values_idf_1 = average_values_idf_1.reindex(average_values_idf_1.index.union(average_values_idf_2.index), fill_value=0)
    average_values_idf_2 = average_values_idf_2.reindex(average_values_idf_1.index, fill_value=0)

    tf_figure = {
        'data': [
            {
                'x': top[tab]['tf'],
                'y': average_values_1.loc[top[tab]['tf']],
                'type': 'bar',
                'name': selected_corpus_1
            },
            {
                'x': top[tab]['tf'],
                'y': average_values_2.loc[top[tab]['tf']],
                'type': 'bar',
                'name': selected_corpus_2
            }
        ],
    }

    tfidf_figure = {
        'data': [
            {
                'x': top[tab]['tfidf'],
                'y': average_values_idf_1.loc[top[tab]['tfidf']],
                'type': 'bar',
                'name': selected_corpus_1
            },
            {
                'x': top[tab]['tfidf'],
                'y': average_values_idf_2.loc[top[tab]['tfidf']],
                'type': 'bar',
                'name': selected_corpus_2
            }
        ],
    }

    return tf_figure, tfidf_figure

    
