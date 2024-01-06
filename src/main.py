from sys import platform, path

if platform == "win32":
    path.append("./")

from src.model.corpus import Corpus

if __name__ == '__main__':
    theme = 'football'

    corpus = Corpus()
    corpus.load(theme, count=200)

    if not corpus.is_save:
        corpus.save()

    documents = corpus.get_documents()
    authors = corpus.get_authors()

    print(corpus, end="\n\n")
    print(*documents, sep="\n")
    print("")
    print(*authors, sep="\n")
