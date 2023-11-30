from sys import platform, path


if platform == "win32":
    path.append("./")

from src.model.corpus import Corpus

if __name__ == '__main__':
    theme = 'football'

    corpus = Corpus(theme, max_size=20)
    corpus.load()
    corpus.save()

    print(corpus.naut, corpus.ndoc)
    corpus.show_sorted_by_title()
    print("\n\n")
    corpus.show_sorted_by_date()
