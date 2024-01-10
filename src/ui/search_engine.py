import pandas as pd
from dash import html, dcc, callback, Output, Input, State

from src.ui.common import corpus_dict, corpus_size

base_author_opt = {'label': "None", 'value': -1}

layout = html.Div([
    html.Label("Select the first corpus", htmlFor="corpus-selector"),
    dcc.Dropdown(
        options=list(corpus_dict.keys()),
        value=list(corpus_dict.keys())[0],
        id="corpus-selector"
    ),

    html.Label("Select an author (optional)", htmlFor="author-selector"),
    dcc.Dropdown(
        options=[base_author_opt],
        value=-1,
        id="author-selector"
    ),

    html.Label("Date", htmlFor='date'),
    dcc.DatePickerRange(id='date'),

    html.Label("Select the amount of document to display", htmlFor="doc-count-input"),
    dcc.Slider(0, corpus_size, value=20, id="doc-count-input"),

    html.Label("Enter some keywords", htmlFor="keywords"),
    dcc.Input(
        id="keywords",
        type="text"
    ),

    html.Button(
        "Search",
        id="search-button",
        n_clicks=0
    ),

    html.Ul(id="content", style={"paddingLeft": "50px", 'marginTop': "20px"}),
])


@callback(
    Output('author-selector', 'options'),
    Output('date', 'start_date'),
    Output('date', 'max_date_allowed'),
    Output('date', 'end_date'),
    Output('date', 'min_date_allowed'),
    Input('corpus-selector', 'value'),
)
def set_author_and_date_on_corpus(corpus_name):
    corpus = corpus_dict[corpus_name]

    if not corpus.is_loaded():
        corpus.load(corpus_size)

    opts = [{'label': v.get_name(), 'value': v.get_name()} for i, v in enumerate(corpus.get_authors())]

    document_sort_by_date = corpus.get_documents(sort="date")

    min_date = document_sort_by_date[0].get_date()
    max_date = document_sort_by_date[-1].get_date()

    return [base_author_opt, *opts], min_date, max_date, max_date, min_date


@callback(
    Output('content', 'children'),
    Input('search-button', 'n_clicks'),
    State('keywords', 'value'),
    State('corpus-selector', 'value'),
    State('author-selector', 'value'),
    State('doc-count-input', 'value'),
    State('date', 'start_date'),
    State('date', 'end_date'),
    prevent_initial_call=True,
)
def on_search(btn, keywords, corpus_name, author, count, s_date, e_date):

    documents = corpus_dict[corpus_name].sort_by_score(keywords or "", corpus_size)

    if len(documents) == 0:
        return "None of there word are contain in the corpus"
    else:

        documents = list(filter(lambda x: e_date >= x.get_date() >= s_date, documents))

        if author != -1:
            documents = list(filter(lambda x: x.get_author() == author, documents))

        if len(documents) <= 0:
            return "No document match your filters."

        if len(documents) > count:
            documents = documents[0:count]

        return [
            html.Div([f"{len(documents)} results."], style={'marginBottom': "5px"}),
            *[
                html.Li([
                    f"[{doc.get_type()}]\t\t",
                    dcc.Link(doc.get_title(), href=doc.get_url(), target='_blank'),
                ])
                for doc in documents
            ]
        ]
