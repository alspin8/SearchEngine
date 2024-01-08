"""
    The main entry of the code is the notebook "NotebookTD5.ipynb"
"""

from sys import platform, path

if platform == "win32":
    path.append("./")

from src.model.corpus import Corpus, clean_text

if __name__ == '__main__':
    theme = 'football'
    count = 200

    corpus = Corpus()
    corpus.load(theme, count)

    # if not corpus.is_saved():
    #     corpus.save()
    #
    # documents = corpus.get_documents()
    # authors = corpus.get_authors()
    #
    print(corpus, end="\n\n")
    # print(*documents, sep="\n")
    # print("")
    # print(*authors, sep="\n")
    # print(*corpus.search("corner"), sep="\n")
    # print(corpus.concorde("corner", 2))
    # print(clean_text(corpus.unique_chain))
    corpus.stats(10)
