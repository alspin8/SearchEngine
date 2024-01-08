import os
from unittest import TestCase, main

from sys import platform, path

if platform == "win32":
    path.append("./")

from src.model.corpus import Corpus
from src.utility import config


class TestCorpus(TestCase):

    CORPUS = Corpus()

    def test_singleton(self):
        self.assertEqual(self.CORPUS, Corpus())

    def test_init(self):
        self.assertFalse(self.CORPUS.is_loaded())
        self.assertFalse(self.CORPUS.is_saved())
        self.assertEqual(self.CORPUS.get_name(), None)
        self.assertEqual(self.CORPUS.get_document_count(), 0)
        self.assertEqual(self.CORPUS.get_documents(), [])
        self.assertEqual(self.CORPUS.get_author_count(), 0)
        self.assertEqual(self.CORPUS.get_authors(), [])

    def test_load(self):
        self.CORPUS.load("football", 20)
        self.assertTrue(self.CORPUS.is_loaded())
        self.assertTrue(self.CORPUS.is_saved())
        self.assertTrue(self.CORPUS.is_same("football", 20))
        self.assertFalse(self.CORPUS.is_same("football", 30))
        self.assertEqual(self.CORPUS.get_document_count(), 20)
        self.assertEqual(len(self.CORPUS.get_documents()), 20)
        self.assertEqual(len(self.CORPUS.get_authors()), self.CORPUS.get_author_count())

    def test_save(self):
        theme = "test"
        file_path = config.DATA_FOLDER.joinpath(f"{theme}.csv")
        if os.path.isfile(file_path):
            os.remove(file_path)

        self.CORPUS.load(theme, 10)
        self.assertTrue(self.CORPUS.is_loaded())
        self.assertFalse(self.CORPUS.is_saved())

        self.CORPUS.save()
        self.assertTrue(self.CORPUS.is_saved())

        os.remove(file_path)


if __name__ == "__main__":
    main()
