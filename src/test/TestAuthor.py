from unittest import TestCase, main

from sys import platform, path

if platform == "win32":
    path.append("./")

from src.model.author import Author
from src.model.document import Document


class TestAuthor(TestCase):

    AUTHOR = Author("test_name")

    def test_name(self):
        self.assertEqual(self.AUTHOR.get_name(), "test_name")

    def test_document(self):
        self.assertEqual(self.AUTHOR.get_document_count(), 0)
        self.assertEqual(self.AUTHOR.get_documents(), [])

        doc0 = Document(title="", author="", date="", url="", text="")
        self.AUTHOR.add_document(doc0)

        self.assertEqual(self.AUTHOR.get_document_count(), 1)
        self.assertEqual(self.AUTHOR.get_documents(), [doc0])
        self.assertEqual(self.AUTHOR.get_document(0), doc0)

        doc1 = Document(title="m", author="", date="", url="", text="")
        self.AUTHOR.add_document(doc1)

        self.assertEqual(self.AUTHOR.get_document_count(), 2)
        self.assertEqual(self.AUTHOR.get_documents(), [doc0, doc1])
        self.assertEqual(self.AUTHOR.get_document(0), doc0)
        self.assertEqual(self.AUTHOR.get_document(1), doc1)
        self.assertRaises(IndexError, self.AUTHOR.get_document, 2)


if __name__ == "__main__":
    main()
