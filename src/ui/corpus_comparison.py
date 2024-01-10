from dash import html, dcc, callback, Output, Input
import pandas as pd

from src.ui.common import corpus_dict  # Assuming this module contains the dictionary of available corpora

# Assuming 'corpus_dict' is a dictionary containing instances of the 'Corpus' class
corpus_names = list(corpus_dict.keys())

layout = html.Div([
    html.Label("Select the first corpus", htmlFor="corpus-selector-1"),
    dcc.Dropdown(
        options=[{'label': name, 'value': name} for name in corpus_names],
        value=corpus_names[0],
        id="corpus-selector-1"
    ),

    html.Label("Select the second corpus", htmlFor="corpus-selector-2"),
    dcc.Dropdown(
        options=[{'label': name, 'value': name} for name in corpus_names],
        value=corpus_names[1],
        id="corpus-selector-2"
    ),

    html.Div([
        html.Div([
            html.H3("Term Frequency (mat_TF)"),
            dcc.Graph(id="tf-matrix")
        ], className="six columns"),

        html.Div([
            html.H3("Term Frequency-Inverse Document Frequency (mat_TFxIDF)"),
            dcc.Graph(id="tfidf-matrix")
        ], className="six columns")
    ], className="row"),

    html.Div([
        html.Div([
            html.H3("Authors - Corpus 1"),
            dcc.Markdown(id="authors-1")
        ], className="six columns"),

        html.Div([
            html.H3("Authors - Corpus 2"),
            dcc.Markdown(id="authors-2")
        ], className="six columns")
    ], className="row")
])

@callback(
    [Output('tf-matrix', 'figure'), Output('tfidf-matrix', 'figure'), Output("authors-1", "children"), Output("authors-2", "children")],
    [Input('corpus-selector-1', 'value'), Input('corpus-selector-2', 'value')]
)
def update_matrices(selected_corpus_1, selected_corpus_2):
    corpus_1 = corpus_dict[selected_corpus_1]
    corpus_2 = corpus_dict[selected_corpus_2]

    # Load corpora if not loaded
    if not corpus_1.is_loaded():
        corpus_1.load(200)
    if not corpus_2.is_loaded():
        corpus_2.load(200)

    # Assuming that 'mat_TF' and 'mat_TFxIDF' are csr_matrix objects for both corpora
    tf_matrix_df_1 = pd.DataFrame(corpus_1.mat_TF.toarray(), columns=list(corpus_1.vocab.keys()))
    tf_matrix_df_2 = pd.DataFrame(corpus_2.mat_TF.toarray(), columns=list(corpus_2.vocab.keys()))

    tfidf_matrix_df_1 = pd.DataFrame(corpus_1.mat_TFxIDF.toarray(), columns=list(corpus_1.vocab.keys()))
    tfidf_matrix_df_2 = pd.DataFrame(corpus_2.mat_TFxIDF.toarray(), columns=list(corpus_2.vocab.keys()))

    # Your comparison logic here...

    tf_figure = {
        'data': [{'z': tf_matrix_df_1.values, 'type': 'heatmap', 'colorscale': 'Viridis'}],
        'layout': {'title': f'Term Frequency Matrix - {selected_corpus_1} vs {selected_corpus_2}'}
    }

    tfidf_figure = {
        'data': [{'z': tfidf_matrix_df_1.values, 'type': 'heatmap', 'colorscale': 'Viridis'}],
        'layout': {'title': f'TF-IDF Matrix - {selected_corpus_1} vs {selected_corpus_2}'}
    }
    
    return tf_figure, tfidf_figure
