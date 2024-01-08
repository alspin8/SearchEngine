import sys
import urllib
import praw
import xmltodict
from src.utility import config
from src.model.document import Document, RedditDocument, ArxivDocument


class DataQuery:
    """
    Utility class to fetch data from reddit and arxiv API

    Methods
    -------
    reddit(theme, count, offset="")
        Fetch <count> documents of <theme>, start at <offset> document from reddit
    arxiv(theme, count, offset="")
        Fetch <count> documents of <theme>, start at <offset> document from arxiv
    all(theme, count, r_off="", a_off=0)
        Fetch <count> documents shared between reddit and arxiv
    """

    REDDIT = r = praw.Reddit(client_id=config.REDDIT_CID, client_secret=config.REDDIT_SECRET, user_agent=config.REDDIT_AGENT, check_for_async=False)
    ARXIV_API_URL = "http://export.arxiv.org/api/query"

    @classmethod
    def reddit(cls, theme, count, offset=""):
        """
        Fetch <count> documents of <theme>, start at <offset> document from reddit
        :param theme: the theme to query
        :type theme: str
        :param count: the amount of document to query
        :type count: int
        :param offset: the document name to start the query
        :type offset: str
        :return: a list of document
        :rtype: list[RedditDocument]
        """
        posts = []
        to_query = count
        cursor = offset
        while len(posts) < count:
            hot_posts = cls.REDDIT.subreddit(theme).hot(limit=to_query, params={"after": cursor})

            to_query = 0
            for post in hot_posts:
                if len(post.title) < 20:
                    to_query += 1
                else:
                    posts.append(post)
                cursor = post.name

        return list(map(Document.from_reddit, posts))

    @classmethod
    def arxiv(cls, theme, count, offset=0):
        """
        Fetch <count> documents of <theme>, start at <offset> document from arxiv
        :param theme: the theme to query
        :type theme: str
        :param count: the amount of document to query
        :type count: int
        :param offset: the document index to start the query
        :type offset: int
        :return: a list of document
        :rtype: list[ArxivDocument]
        """
        posts = []
        to_query = count
        cursor = int(offset) + 1
        while len(posts) < count:

            lst = []
            url = f'{cls.ARXIV_API_URL}?search_query=all:{theme}&start={cursor}&max_results={to_query}'
            try:
                xml = urllib.request.urlopen(url)
                lst = xmltodict.parse(xml.read().decode('utf-8'))["feed"]["entry"]
            except urllib.error.HTTPError:
                print(f"Could not query arxiv with {theme} keyword", file=sys.stderr)
                return []

            if type(lst) is not list:
                lst = [lst]

            to_query = 0
            next_cursor = 0
            for i in range(len(lst)):
                if len(lst[i]["title"]) < 20:
                    to_query += 1
                else:
                    posts.append(lst[i] | dict(api_index=cursor + i))
                next_cursor = cursor + i

            cursor = next_cursor + 1

        return list(map(Document.from_arxiv, posts))

    @classmethod
    def all(cls, theme, count, r_off="", a_off=0):
        """
        Fetch <count> documents shared between reddit and arxiv
        :param theme: the theme to query
        :type theme: str
        :param count: the amount of document to query
        :type count: int
        :param r_off: the document name to start the query for reddit
        :type r_off: str
        :param a_off: the document index to start the query for arxiv
        :type a_off: int
        :return: a list of document
        :rtype: list[RedditDocument | ArxivDocument]
        """
        assert count % 2 == 0

        arxiv_doc = cls.arxiv(theme, count // 2, a_off)
        if len(arxiv_doc) > 0:
            reddit_doc = cls.reddit(theme, count // 2, r_off)
        else:
            reddit_doc = cls.reddit(theme, count, r_off)
            print(f"Due to a problem with the api arxiv, the corpus size has been compensated by reddit documents")

        return [*reddit_doc, *arxiv_doc]
