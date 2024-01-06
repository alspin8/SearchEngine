import os
import random
import urllib
import urllib.request

import pandas as pd
import praw
import xmltodict
from src import config
from src.model.author import Author
from src.model.document import Document, RedditDocument, ArxivDocument
from src.utils import author_to_list


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class Corpus:
    def __init__(self):
        self.name = None
        self.id2doc: dict[int, Document] = dict()
        self.authors: dict[str, Author] = dict()
        self.ndoc = 0
        self.naut = 0
        self.is_save = False
        self.is_loaded = False

        self.__file_path = None

    def __reddit(self, count, offset="") -> list:
        r = praw.Reddit(client_id=config.REDDIT_CID, client_secret=config.REDDIT_SECRET, user_agent=config.REDDIT_AGENT, check_for_async=False)

        posts = []
        to_query = count
        cursor = offset
        while len(posts) < count:
            hot_posts = r.subreddit(self.name).hot(limit=to_query, params={"after": cursor})

            to_query = 0
            for post in hot_posts:
                if len(post.title) < 20:
                    to_query += 1
                else:
                    posts.append(post)
                cursor = post.name

        return list(map(Document.from_reddit, posts))

    def __arxiv(self, count, offset=0) -> list:
        posts = []
        to_query = count
        cursor = int(offset)
        while len(posts) < count:

            url = f'http://export.arxiv.org/api/query?search_query=all:{self.name}&start={cursor}&max_results={to_query}'
            xml = urllib.request.urlopen(url)
            lst = xmltodict.parse(xml.read().decode('utf-8'))["feed"]["entry"]

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

    def save(self):
        df = pd.DataFrame([data.__dict__ | dict(type=data.get_type()) for data in self.id2doc.values()])
        df.to_csv(self.__file_path, sep=config.CSV_SEP)
        self.is_save = True

    def load(self, name, count=200):
        self.name = name
        self.__file_path = os.path.join(config.DATA_FOLDER, f"{name}.csv")

        if not os.path.isfile(self.__file_path):
            self.is_save = False
            data_list = [*self.__reddit(count // 2), *self.__arxiv(count // 2)]
            df = pd.DataFrame([data.__dict__ | dict(type=data.get_type()) for data in data_list])
        else:
            self.is_save = True
            df = pd.read_csv(self.__file_path, sep=config.CSV_SEP, index_col=0, converters={"co_authors": author_to_list})
            if len(df) < count:
                self.is_save = False
                fetch_count = (count - len(df)) // 2
                data_list = [
                    *self.__reddit(fetch_count, offset=df.loc[df.type == "reddit", :].tail(1).iloc[0].fullname),
                    *self.__arxiv (fetch_count, offset=df.loc[(df.type == "arxiv") & (df.api_index == df.api_index.max()), :].tail(1).iloc[0].api_index)
                ]
                df2 = pd.DataFrame([data.__dict__ | dict(type=data.get_type()) for data in data_list])
                df = pd.concat([df, df2], ignore_index=True)
            else:
                df = df.sample(frac=1)
                df = df.iloc[0:count, :]

        df.index.name = "id"

        self.id2doc = dict(
            [(i, RedditDocument(**kwargs) if kwargs["type"] == "reddit" else ArxivDocument(**kwargs)) for i, kwargs in enumerate(df.to_dict(orient='records'))])
        self.authors = {}
        for doc in self.id2doc.values():
            if doc.author and doc.author not in self.authors:
                self.authors[doc.author] = Author(name=doc.author)
            self.authors[doc.author].add(doc)

            if doc.get_type() == "arxiv":
                for author in doc.co_authors:
                    if author not in self.authors:
                        self.authors[author] = Author(name=author)
                    self.authors[author].add(doc)

        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)

        self.is_loaded = True

    def get(self, sort="none"):
        if sort == "title":
            return sorted(self.id2doc.values(), key=lambda x: x.title)
        if sort == "date":
            return sorted(self.id2doc.values(), key=lambda x: x.date)
        else:
            return list(self.id2doc.values())

    def __len__(self):
        print(self.ndoc)
        return self.ndoc
