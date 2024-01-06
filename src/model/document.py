from datetime import datetime

from src.utils import clean_string


class Document:
    def __init__(self, **kwargs):
        default = "Unknown"
        self.title = clean_string(kwargs["title"]) or default
        self.author = kwargs["author"] or default
        self.date = kwargs["date"] or datetime.now()
        self.url = clean_string(kwargs["url"]) or default
        self.text = clean_string(kwargs["text"]) or default

    def __str__(self):
        return f"Document({self.title}, {self.get_type()})"

    def __repr__(self) -> str:
        return f"Document(title={self.title}, author={self.author}, date={self.date}, url={self.url}, text={self.text})"

    def get_type(self):
        raise NotImplementedError()

    @staticmethod
    def from_reddit(post):
        return RedditDocument(title=post.title, author=post.author_flair_text if post.author_flair_text else [], date=datetime.utcfromtimestamp(post.created_utc), url=post.url, text=post.selftext, comment_count=post.comments, fullname=post.name)

    @staticmethod
    def from_arxiv(post):
        title = post["title"] if "title" in post else None
        author = post["author"][0]["name"] if type(post["author"]) is list else post["author"]["name"]
        date = datetime.strptime(post["published"], "%Y-%m-%dT%H:%M:%SZ") if "published" in post else None
        url = post["id"] if "id" in post else None
        text = post["summary"] if "summary" in post else None
        co_authors = list(map(lambda aut: aut["name"], post["author"][1:])) if type(post["author"]) is list else []
        api_index = post["api_index"] if "api_index" in post else 0
        return ArxivDocument(title=title, author=author, date=date, url=url, text=text, co_authors=co_authors, api_index=api_index)


class RedditDocument(Document):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.comment_count = kwargs["comment_count"] if "comment_count" in kwargs else 0
        self.fullname = kwargs["fullname"] if "fullname" in kwargs else ""

    def get_type(self):
        return "reddit"


class ArxivDocument(Document):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.co_authors = kwargs["co_authors"] if "co_authors" in kwargs else []
        self.api_index = kwargs["api_index"] if "api_index" in kwargs else 0

    def get_type(self):
        return "arxiv"
