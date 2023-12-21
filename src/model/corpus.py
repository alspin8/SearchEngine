import json
import os
import random
import urllib
import urllib.request

import numpy as np
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

        self.__max_size = None
        self.__file_path = None

    def __reddit(self) -> list:
        r = praw.Reddit(client_id=config.REDDIT_CID, client_secret=config.REDDIT_SECRET, user_agent=config.REDDIT_AGENT)
        hot_posts = r.subreddit(self.name).hot(limit=self.__max_size)
        return list(map(Document.from_reddit, hot_posts))

    def __arxiv(self) -> list:
        url = f'http://export.arxiv.org/api/query?search_query=all:{self.name}&start=0&max_results={self.__max_size}'
        xml = urllib.request.urlopen(url)
        return list(map(Document.from_arxiv, xmltodict.parse(xml.read().decode('utf-8'))["feed"]["entry"]))

    def save(self):
        df = pd.DataFrame([data.__dict__ | dict(type=data.get_type()) for data in self.id2doc.values()])
        df.to_csv(self.__file_path, sep=config.CSV_SEP)

    def load(self, name, max_size=200):
        self.name = name
        self.__max_size = int(max_size / 2)
        self.__file_path = os.path.join(config.DATA_FOLDER, f"{name}.csv")

        if not os.path.isfile(self.__file_path):
            data_list = [*self.__reddit(), *self.__arxiv()]
            random.shuffle(data_list)
            df = pd.DataFrame([data.__dict__ | dict(type=data.get_type()) for data in data_list])
        else:
            df = pd.read_csv(self.__file_path, sep=config.CSV_SEP, index_col=0, converters={"co_authors": author_to_list})
            if len(df) < max_size:
                data_list = [*self.__reddit(), *self.__arxiv()]
                random.shuffle(data_list)
                df = pd.DataFrame([data.__dict__ | dict(type=data.get_type()) for data in data_list])
            else:
                df = df.iloc[0:max_size, :]

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

    def get(self, sort="none"):
        if sort == "title":
            return sorted(self.id2doc.values(), key=lambda x: x.title)
        if sort == "data":
            return sorted(self.id2doc.values(), key=lambda x: x.date)
        else:
            return self.id2doc.values()
