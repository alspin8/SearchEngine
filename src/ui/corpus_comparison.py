

from dash import html, dcc, callback, Output, Input
import pandas as pd

from src.ui.common import corpus_dict

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
            html.H3("Term Frequency (mat_TF) inversed"),
            dcc.Graph(id="tf-matrix-inv")
        ], className="six columns"),

        html.Div([
            html.H3("Term Frequency-Inverse Document Frequency (mat_TFxIDF) inversed"),
            dcc.Graph(id="tfidf-matrix-inv")
        ], className="six columns")
    ], className="row")
])

@callback(
    [Output('tf-matrix', 'figure'), Output('tfidf-matrix', 'figure'), Output('tf-matrix-inv', 'figure'), Output('tfidf-matrix-inv', 'figure')],
    [Input('corpus-selector-1', 'value'), Input('corpus-selector-2', 'value')]
)
def update_matrices(selected_corpus_1, selected_corpus_2):
    corpus_1 = corpus_dict[selected_corpus_1]
    corpus_2 = corpus_dict[selected_corpus_2]

    if not corpus_1.is_loaded():
        corpus_1.load(200)
    if not corpus_2.is_loaded():
        corpus_2.load(200)

    tf_matrix_df_1 = pd.DataFrame(corpus_1.mat_TF.toarray(), columns=list(corpus_1.vocab.keys()))
    tf_matrix_df_2 = pd.DataFrame(corpus_2.mat_TF.toarray(), columns=list(corpus_2.vocab.keys()))
    
    average_values_1 = tf_matrix_df_1.mean(axis=0)
    average_values_2 = tf_matrix_df_2.mean(axis=0)

    top_20_values_1 = average_values_1.nlargest(20)
    top_20_values_2 = average_values_2.nlargest(20)


    tfidf_matrix_df_1 = pd.DataFrame(corpus_1.mat_TFxIDF.toarray(), columns=list(corpus_1.vocab.keys()))
    tfidf_matrix_df_2 = pd.DataFrame(corpus_2.mat_TFxIDF.toarray(), columns=list(corpus_2.vocab.keys()))

    average_values_idf_1 = tfidf_matrix_df_1.mean(axis=0)
    average_values_idf_2 = tfidf_matrix_df_2.mean(axis=0)

    top_20_values_idf_1 = average_values_idf_1.nlargest(20)
    top_20_values_idf_2 = average_values_idf_2.nlargest(20)

    tf_figure = {
        'data': [{'x': top_20_values_1.index, 'y': top_20_values_1.values, 'type': 'bar', 'name': selected_corpus_1},
                {'x': top_20_values_2.index, 'y': top_20_values_2.values, 'type': 'bar', 'name': selected_corpus_2}
                 ],
        'layout': {'title': f'Term Frequency Matrix - {selected_corpus_1} vs {selected_corpus_2}'}
    }

    tfidf_figure = {
        'data': [{'x': top_20_values_idf_1.index, 'y': top_20_values_idf_1.values, 'type': 'bar', 'name': selected_corpus_1},
                {'x': top_20_values_idf_2.index, 'y': top_20_values_idf_2.values, 'type': 'bar', 'name': selected_corpus_2}
                 ],
        'layout': {'title': f'TF-IDF Matrix - {selected_corpus_1} vs {selected_corpus_2}'}
    }

    tf_figure_inv = {
        'data': [{'x': top_20_values_2.index, 'y': top_20_values_2.values, 'type': 'bar', 'name': selected_corpus_2},
                {'x': top_20_values_1.index, 'y': top_20_values_1.values, 'type': 'bar', 'name': selected_corpus_1}
                 ],
        'layout': {'title': f'Term Frequency Matrix - {selected_corpus_1} vs {selected_corpus_2} inversed'}
    }

    tfidf_figure_inv = {
        'data': [{'x': top_20_values_idf_2.index, 'y': top_20_values_idf_2.values, 'type': 'bar', 'name': selected_corpus_2},
                {'x': top_20_values_idf_1.index, 'y': top_20_values_idf_1.values, 'type': 'bar', 'name': selected_corpus_1}
                 ],
        'layout': {'title': f'TF-IDF Matrix - {selected_corpus_1} vs {selected_corpus_2} inversed'}
    }

    return tf_figure, tfidf_figure, tf_figure_inv, tfidf_figure_inv

    
