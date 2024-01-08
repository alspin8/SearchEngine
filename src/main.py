"""
    The main entry of the code is the notebook "NotebookTD5.ipynb"
"""

from sys import platform, path

if platform == "win32":
    path.append("./")

from src.model.corpus import Corpus

if __name__ == '__main__':
    theme = 'physics'
    count = 20

    corpus = Corpus()
    corpus.load(theme, count)

    if not corpus.is_saved():
        corpus.save()

    documents = corpus.get_documents()
    authors = corpus.get_authors()

    print(corpus, end="\n\n")
    print(*documents, sep="\n")
    print("")
    print(*authors, sep="\n")
