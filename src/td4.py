from src.model.corpus import Corpus


def main() -> None:
    theme = 'football'

    corpus = Corpus(theme)
    corpus.load()
    corpus.save()

    print(corpus.naut, corpus.ndoc)
    corpus.show_sorted_by_title()
    print("\n\n")
    corpus.show_sorted_by_date()
