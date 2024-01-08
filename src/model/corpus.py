import os
import pandas as pd
from src.utility import config
from src.utility.data_query import DataQuery
from src.model.author import Author
from src.model.document import Document, RedditDocument, ArxivDocument
from src.utility.utils import singleton

author_to_list = lambda x: x.strip("[]").replace("'", "").split(", ") if x != '[]' else []


@singleton
class Corpus:
    """
    A class used to represent a Corpus

    Attributes
    ----------
    name : str
        the name of the corpus (fetch keyword)
    id2doc : dict[int, Document]
        the document contained into the corpus
    authors: dict[int, Author]
        the authors of documents
    ndoc : int
        the number of document in the corpus
    naut : int
        the number of authors of documents
    saved : bool
        the save status of the corpus
    loaded : bool
        the load status of the corpus

    Methods
    -------
    load(name, count)
        Load corpus with data depend on name and count
    save()
        Save the current corpus to a csv (<corpus name>.csv)
    get_name()
        Return the name of corpus
    get_document_count()
        Return the number of document in the corpus
    get_author_count()
        Return the number of author in the corpus
    is_loaded()
        Return if corpus is loaded
    is_saved()
        Return if the corpus is saved
    get_documents(sort="")
        Return sorted list of document
    get_authors(sort="")
        Return sorted list of author
    is_same(name, document_count)
        Return if corpus match with name and document_count
    """
    def __init__(self):
        self.name = None
        self.id2doc = dict()
        self.authors = dict()
        self.ndoc = 0
        self.naut = 0
        self.saved = False
        self.loaded = False
        self.file_path = None

    def load(self, name, count):
        """
        Load corpus with data depend on name and count
        :param name: The keyword to search
        :type name: str
        :param count: The amount of document to retrieve
        :type count: int
        """
        self.name = name
        self.file_path = config.DATA_FOLDER.joinpath(f"{name}.csv")

        if not os.path.isfile(self.file_path):
            self.saved = False
            data_list = DataQuery().all(self.name, count)
            self.id2doc = dict([(i, doc) for i, doc in enumerate(data_list)])
        else:
            self.saved = True
            df = pd.read_csv(self.file_path, sep=config.CSV_SEP, index_col=0, converters={"co_authors": author_to_list})
            if len(df) < count:
                self.saved = False
                r_off = df.loc[df.type == "reddit", :].tail(1).iloc[0].fullname
                a_off = df.loc[(df.type == "arxiv") & (df.api_index == df.api_index.max()), :].tail(1).iloc[0].api_index
                data_list = DataQuery().all(self.name, count - len(df), r_off, a_off)

                df2 = pd.DataFrame([data.__dict__ | dict(type=data.get_type()) for data in data_list])
                df = pd.concat([df, df2], ignore_index=True)
            else:
                df = df.sample(frac=1)
                df = df.iloc[0:count, :]

            df.index.name = "id"
            self.id2doc = dict([(i, RedditDocument(**kwargs) if kwargs["type"] == "reddit" else ArxivDocument(**kwargs)) for i, kwargs in enumerate(df.to_dict(orient='records'))])

        self.authors = Author.dict_from_documents(list(self.id2doc.values()))

        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)

        self.loaded = True

    def save(self):
        """
        Save the current corpus to a csv (<corpus name>.csv)
        """
        df = pd.DataFrame([data.__dict__ | dict(type=data.get_type()) for data in self.id2doc.values()])
        df.to_csv(self.file_path, sep=config.CSV_SEP)
        self.saved = True

    def get_name(self):
        """
        Return the name of corpus
        :return: name of the corpus
        :rtype: str
        """
        return self.name

    def get_document_count(self):
        """
        Return the number of document in the corpus
        :return: the number of document in the corpus
        :rtype: int
        """
        return self.ndoc

    def get_author_count(self):
        """
        Return the number of author in the corpus
        :return: the number of author in the corpus
        :rtype: int
        """
        return self.naut

    def is_loaded(self):
        """
        Return if corpus is loaded
        :return: True if corpus is loaded
        :rtype: bool
        """
        return self.loaded

    def is_saved(self):
        """
        Return if corpus is saved
        :return: True if corpus is saved
        :rtype: bool
        """
        return self.saved

    def get_documents(self, sort=""):
        """
        Return sorted list of document
        :param sort: Sort mode, can be "" | "title" | "date"
        :type sort: str
        :return: a list of document
        :rtype: list[Document]
        """
        if sort == "title":
            return sorted(self.id2doc.values(), key=lambda x: x.get_title())
        if sort == "date":
            return sorted(self.id2doc.values(), key=lambda x: x.get_date())
        else:
            return list(self.id2doc.values())

    def get_authors(self, sort=""):
        """
        Return sorted list of author
        :param sort: Sort mode, can be "" | "name" | "document_count"
        :type sort: str
        :return: a list of author
        :rtype: list[Author]
        """
        if sort == "name":
            return sorted(self.authors.values(), key=lambda x: x.get_name())
        elif sort == "document_count":
            return sorted(self.authors.values(), key=lambda x: x.get_document_count())
        else:
            return list(self.authors.values())

    def is_same(self, name, document_count):
        """
        Return if corpus match with name and document_count
        :param name: the expected name
        :type name: str
        :param document_count: the expected document_count
        :type document_count: int
        :return:
        :rtype: bool
        """
        return self.name == name and self.ndoc == document_count

    def __str__(self):
        return f"Corpus({self.name}, documents={self.ndoc}, authors={self.naut})"

    def __repr__(self):
        return self.__str__()
