from datetime import datetime

from src.utility.utils import string_preprocessing


class Document:
    """
    A base class used to represent a document

    Attributes
    ----------
    title : str
        the title of the document
    author : str
        the name of the author
    date: datetime
        the date the document was created
    url: str
        the url of the document
    text: str
        the content of the document

    Methods
    ------
    get_type()
        Pure virtual method to know the source of the document
    get_title()
        Return the title of the document
    get_author()
        Return the author of the document
    get_date()
        Return the date the document was created
    get_url()
        Return the url of the document
    get_text()
        Return the content of the document
    from_reddit()
        Return a RedditDocument from reddit api query
    from_arxiv()
        Return a ArxivDocument from arxiv api query
    """

    def __init__(self, **kwargs):
        self.title = kwargs["title"]
        self.author = kwargs["author"]
        self.date = kwargs["date"] or datetime.now()
        self.url = kwargs["url"]
        self.text = kwargs["text"]

    def get_type(self):
        """
        Pure virtual method to know the source of the document
        :raise NotImplementedError
        """
        raise NotImplementedError()

    def get_title(self):
        """
        Return the title of the document
        :return: the title of the document
        :rtype: str
        """
        return self.title

    def get_author(self):
        """
        Return the author of the document
        :return: the author of the document
        :rtype: str
        """
        return self.author

    def get_date(self):
        """
        Return the date the document was created
        :return: the date the document was created
        :rtype: datetime
        """
        return self.date

    def get_url(self):
        """
        Return the url of the document
        :return: the url of the document
        :rtype: str
        """
        return self.url

    def get_text(self):
        """
        Return the content of the document
        :return: the content of the document
        :rtype: str
        """
        return self.text

    def __str__(self):
        return f"Document({self.title}, source={self.get_type()})"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def from_reddit(post):
        """
        Return a RedditDocument from reddit api query
        :param post: the result of praw request
        :return: a document
        :rtype: RedditDocument
        """
        return RedditDocument(
            title=string_preprocessing(post.title),
            author=post.author_flair_text if post.author_flair_text else "Unknown",
            date=datetime.utcfromtimestamp(post.created_utc),
            url=post.url,
            text=string_preprocessing(post.selftext),
            comment_count=len(post.comments),
            fullname=post.name
        )

    @staticmethod
    def from_arxiv(post):
        """
        Return a ArxivDocument from arxiv api query
        :param post: the result of arxiv request
        :return: a document
        :rtype: ArxivDocument
        """
        title = string_preprocessing(post["title"]) if "title" in post else "Empty"
        author = post["author"][0]["name"] if type(post["author"]) is list else post["author"]["name"]
        date = datetime.strptime(post["published"], "%Y-%m-%dT%H:%M:%SZ") if "published" in post else None
        url = post["id"] if "id" in post else "Empty"
        text = string_preprocessing(post["summary"] or "None") if "summary" in post else "Empty"
        co_authors = list(map(lambda aut: aut["name"], post["author"][1:])) if type(post["author"]) is list else []
        api_index = post["api_index"] if "api_index" in post else 0
        return ArxivDocument(title=title, author=author, date=date, url=url, text=text, co_authors=co_authors,
                             api_index=api_index)


class RedditDocument(Document):
    """
    A child class of Document used to represent a reddit document

    Attributes
    ----------
    comment_count : int
        the comment count of this reddit post
    fullname : str
        the fullname of this post

    Methods
    -------
    get_type()
        Override base class method that return "reddit"
    get_comment_count()
        Return the comment count of this reddit post
    get_fullname()
        Return the fullname of this post
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.comment_count = kwargs["comment_count"] if "comment_count" in kwargs else 0
        self.fullname = kwargs["fullname"] if "fullname" in kwargs else ""

    def get_type(self):
        """
        Override base class method that return "reddit"
        :return: the type of this document
        :rtype: str
        """
        return "reddit"

    def get_comment_count(self):
        """
        Return the comment count of this reddit post
        :return: the comment count of this reddit post
        :rtype: int
        """
        return self.comment_count

    def get_fullname(self):
        """
        Return the fullname of this post
        :return: the fullname of this post
        :rtype: str
        """
        return self.fullname


class ArxivDocument(Document):
    """
    A child class of Document used to represent an arxiv document

    Attributes
    ----------
    co_authors : list[str]
        the list of co-authors of this document
    api_index : int
        the index of the document in arxiv api

    Methods
    -------
    get_type()
        Override base class method that return "arxiv"
    get_co_authors()
        Return the list of co-authors of this document
    get_api_index()
        Return the index of the document in arxiv api
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.co_authors = kwargs["co_authors"] if "co_authors" in kwargs else []
        self.api_index = kwargs["api_index"] if "api_index" in kwargs else 0

    def get_type(self):
        """
        Override base class method that return "arxiv"
        :return: the type of this document
        :rtype: str
        """
        return "arxiv"

    def get_co_authors(self):
        """
        Return the list of co-authors of this document
        :return: the list of co-authors of this document
        :rtype: list[str]
        """
        return self.co_authors

    def get_api_index(self):
        """
        Return the index of the document in arxiv api
        :return: the index of the document in arxiv api
        :rtype: int
        """
        return self.api_index
