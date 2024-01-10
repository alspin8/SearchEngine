from dash import html, dcc, callback, Output, Input

from src.ui.common import corpus_dict

layout = html.Div([
    html.Label("Select the corpus", htmlFor="corpus-selector"),
    dcc.Dropdown(
        options=list(corpus_dict.keys()),
        value=list(corpus_dict.keys())[0],
        id="corpus-selector"
    ),

    html.Div(id="content")
])


@callback(
    Output('content', 'children'),
    Input('corpus-selector', 'value')
)
def render(select):
    corpus = corpus_dict[select]
    if not corpus.is_loaded():
        corpus.load(200)

    # return [str(auth) for auth in corpus.get_authors()]
    return corpus.get_author_count()
