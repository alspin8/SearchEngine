from sys import path, platform
from unittest import TestCase, main

if platform == "win32":
    path.append("../")

from src.utility.data_query import DataQuery


class TestDataQuery(TestCase):

    THEME = "test"

    def test_reddit(self):
        res = DataQuery.reddit(self.THEME, 5)
        self.assertEqual(len(res), 5)
        res1 = DataQuery.reddit(self.THEME, 5, offset=res[-2].get_fullname())
        self.assertEqual(len(res1), 5)
        self.assertEqual(res[-1].get_fullname(), res1[0].get_fullname())

    def test_arxiv(self):
        res = DataQuery.arxiv(self.THEME, 5)
        self.assertEqual(len(res), 5)
        res1 = DataQuery.arxiv(self.THEME, 5, offset=res[-2].get_api_index())
        self.assertEqual(len(res1), 5)
        self.assertEqual(res[-1].get_api_index(), res1[0].get_api_index())


if __name__ == '__main__':
    main()
