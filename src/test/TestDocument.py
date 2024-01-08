from datetime import datetime
from unittest import TestCase, main

from sys import platform, path

if platform == "win32":
    path.append("../")

from src.model.document import Document, RedditDocument, ArxivDocument
from src.utility.data_query import DataQuery


class TestDocument(TestCase):

    DT = datetime.now()
    DOCUMENT = Document(
        title="test",
        author="test_author",
        date=DT,
        url="http://test_url",
        text="Bonjour"
    )

    def test_title(self):
        self.assertEqual(self.DOCUMENT.get_title(), "test")

    def test_author(self):
        self.assertEqual(self.DOCUMENT.get_author(), "test_author")

    def test_date(self):
        self.assertEqual(self.DOCUMENT.get_date(), self.DT)

    def test_url(self):
        self.assertEqual(self.DOCUMENT.get_url(), "http://test_url")

    def test_text(self):
        self.assertEqual(self.DOCUMENT.get_text(), "Bonjour")

    def test_type(self):
        self.assertRaises(NotImplementedError, self.DOCUMENT.get_type)


class TestRedditDocument(TestCase):
    DT = datetime.now()
    DOCUMENT = RedditDocument(
        title="test",
        author="test_author",
        date=DT,
        url="http://test_url",
        text="Bonjour",
        comment_count=5,
        fullname="fullname_reddit"
    )

    def test_title(self):
        self.assertEqual(self.DOCUMENT.get_title(), "test")

    def test_author(self):
        self.assertEqual(self.DOCUMENT.get_author(), "test_author")

    def test_date(self):
        self.assertEqual(self.DOCUMENT.get_date(), self.DT)

    def test_url(self):
        self.assertEqual(self.DOCUMENT.get_url(), "http://test_url")

    def test_text(self):
        self.assertEqual(self.DOCUMENT.get_text(), "Bonjour")

    def test_type(self):
        self.assertEqual(self.DOCUMENT.get_type(), "reddit")

    def test_comment_count(self):
        self.assertEqual(self.DOCUMENT.get_comment_count(), 5)

    def test_fullname(self):
        self.assertEqual(self.DOCUMENT.get_fullname(), "fullname_reddit")


class TestArxivDocument(TestCase):
    DT = datetime.now()
    DOCUMENT = ArxivDocument(
        title="test",
        author="test_author",
        date=DT,
        url="http://test_url",
        text="Bonjour",
        co_authors=["first", "second"],
        api_index=8
    )

    def test_title(self):
        self.assertEqual(self.DOCUMENT.get_title(), "test")

    def test_author(self):
        self.assertEqual(self.DOCUMENT.get_author(), "test_author")

    def test_date(self):
        self.assertEqual(self.DOCUMENT.get_date(), self.DT)

    def test_url(self):
        self.assertEqual(self.DOCUMENT.get_url(), "http://test_url")

    def test_text(self):
        self.assertEqual(self.DOCUMENT.get_text(), "Bonjour")

    def test_type(self):
        self.assertEqual(self.DOCUMENT.get_type(), "arxiv")

    def test_co_author(self):
        self.assertEqual(self.DOCUMENT.get_co_authors(), ["first", "second"])

    def test_fullname(self):
        self.assertEqual(self.DOCUMENT.get_api_index(), 8)


class TestDocumentFactory(TestCase):

    REDDIT_DOCUMENT = DataQuery().reddit("football", 1)[0]
    ARXIV_DOCUMENT = DataQuery().arxiv("football", 1)[0]

    def test_reddit_factory(self):
        self.assertEqual(type(self.REDDIT_DOCUMENT), RedditDocument)
        self.assertEqual(self.REDDIT_DOCUMENT.get_type(), "reddit")
        self.assertTrue(issubclass(type(self.REDDIT_DOCUMENT), Document))

    def test_arxiv_factory(self):
        self.assertEqual(type(self.ARXIV_DOCUMENT), ArxivDocument)
        self.assertEqual(self.ARXIV_DOCUMENT.get_type(), "arxiv")
        self.assertTrue(issubclass(type(self.ARXIV_DOCUMENT), Document))


if __name__ == "__main__":
    main()
