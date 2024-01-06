from datetime import datetime

clean_string = lambda string: " ".join(string.split()) if len(string) > 0 else "Empty"


class Document:

    def __init__(self, **kwargs):
        self.title = kwargs["title"]
        self.author = kwargs["author"]
        self.date = kwargs["date"] or datetime.now()
        self.url = kwargs["url"]
        self.text = kwargs["text"]

    def get_type(self):
        raise NotImplementedError()

    @staticmethod
    def from_reddit(post):
        return RedditDocument(
            title=clean_string(post.title),
            author=post.author_flair_text if post.author_flair_text else "Unknown",
            date=datetime.utcfromtimestamp(post.created_utc),
            url=post.url,
            text=clean_string(post.selftext),
            comment_count=len(post.comments),
            fullname=post.name
        )

    @staticmethod
    def from_arxiv(post):
        title = clean_string(post["title"]) if "title" in post else "Empty"
        author = post["author"][0]["name"] if type(post["author"]) is list else post["author"]["name"]
        date = datetime.strptime(post["published"], "%Y-%m-%dT%H:%M:%SZ") if "published" in post else None
        url = post["id"] if "id" in post else "Empty"
        text = clean_string(post["summary"] or "None") if "summary" in post else "Empty"
        co_authors = list(map(lambda aut: aut["name"], post["author"][1:])) if type(post["author"]) is list else []
        api_index = post["api_index"] if "api_index" in post else 0
        return ArxivDocument(title=title, author=author, date=date, url=url, text=text, co_authors=co_authors, api_index=api_index)

    def __str__(self):
        return f"Document({self.title}, source={self.get_type()})"

    def __repr__(self) -> str:
        return self.__str__()


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
