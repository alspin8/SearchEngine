from datetime import datetime

from src.utils import clean_string


class Document:
    def __init__(self, **kwargs):
        default = "Unknown"
        self.title = clean_string(kwargs["title"]) or default
        self.author: list = kwargs["author"] or []
        self.date = kwargs["date"] or datetime.now()
        self.url = clean_string(kwargs["url"]) or default
        self.text = clean_string(kwargs["text"]) or default

    def __str__(self):
        return f"Document({self.title})"

    def __repr__(self) -> str:
        return f"Document(title={self.title}, author={self.author}, date={self.date}, url={self.url}, text={self.text})"

    @staticmethod
    def from_reddit(post):
        return Document(title=post.title, author=[post.author_flair_text] if post.author_flair_text else [], date=datetime.utcfromtimestamp(post.created_utc), url=post.url, text=post.selftext)

    @staticmethod
    def from_arxiv(post):
        title = post["title"] if "title" in post else None
        if "author" in post:
            author = list(map(lambda aut: aut["name"], post["author"])) if type(post["author"]) is list else [post["author"]["name"]]
        else:
            author = []
        date = datetime.strptime(post["published"], "%Y-%m-%dT%H:%M:%SZ") if "published" in post else None
        url = post["id"] if "id" in post else None
        text = post["summary"] if "summary" in post else None
        return Document(title=title, author=author, date=date, url=url, text=text)
