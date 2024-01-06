from sys import platform, path

if platform == "win32":
    path.append("./")

from src.model.corpus import Corpus

if __name__ == '__main__':
    theme = 'football'

    corpus = Corpus()
    corpus.load(theme, max_size=20)
    corpus.save()

    v = "\n".join(str(item) for item in corpus.get(sort="date"))

    print(v)

