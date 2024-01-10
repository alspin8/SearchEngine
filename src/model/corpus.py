import os
import re
import sys

import numpy as np
import numpy.linalg
import pandas as pd
from scipy.sparse import csr_matrix

from src.utility import config
from src.utility.data_query import DataQuery
from src.model.author import Author
from src.model.document import Document, RedditDocument, ArxivDocument
from src.utility.utils import clean_text, split_string, stringify_list_to_list


# @singleton
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
    file_path : Path
        the path to the saved corpus
    unique_chain : str
        the string that contain all document text
    vocab : dict[str, dict[str, int]]
        the dict that contain all unique word of the corpus as key and some his freq, document_freq and id as value
    mat_TF : csr_matrix
        the term frequency matrix with word as column and document as row, populated with word occurrence
    mat_TFxIDF : csr_matrix
        the term frequency-inverse document frequency matrix with word as column and document as row, populated with word occurrence

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
    concorde(keyword, context_size)
        Return a dataframe with three column, left context of len <context_size>, the keyword, right context of len <context_size>
    search(keyword)
        Same as concorde, but return a list of string with 2 word of context
    stats(top_count)
        Print some statistic about the corpus. The total number of unique word and the <top_count> most frequent words
    """

    def __init__(self, name):
        self.name = name
        self.id2doc = {}
        self.authors = {}
        self.ndoc = 0
        self.naut = 0
        self.saved = False
        self.loaded = False
        self.file_path = config.DATA_FOLDER.joinpath(f"{name}.csv")
        self.unique_chain = ""
        self.vocab = {}
        self.mat_TF = None
        self.mat_TFxIDF = None

    def load(self, count):
        """
        Load corpus with data depend on name and count
        :param count: The amount of document to retrieve
        :type count: int
        """

        if not os.path.isfile(self.file_path):
            self.saved = False
            data_list = DataQuery().all(self.name, count)
            self.id2doc = dict([(i, doc) for i, doc in enumerate(data_list)])
        else:
            self.saved = True
            df = pd.read_csv(self.file_path, sep=config.CSV_SEP, index_col=0, converters={"co_authors": stringify_list_to_list})
            if len(df) < count:
                self.saved = False
                r_off = df.loc[df.type == "reddit", :].tail(1).iloc[0].fullname
                a_off = df.loc[(df.type == "arxiv") & (df.api_index == df.api_index.max()), :].tail(1).iloc[0].api_index
                data_list = DataQuery().all(self.name, count - len(df), r_off, a_off)

                df2 = pd.DataFrame([data.__dict__ | dict(type=data.get_type()) for data in data_list])
                df = pd.concat([df, df2], ignore_index=True)
            else:
                df = df.iloc[0:count, :]

            df.index.name = "id"
            self.id2doc = dict(
                [(i, RedditDocument(**kwargs) if kwargs["type"] == "reddit" else ArxivDocument(**kwargs)) for i, kwargs
                 in enumerate(df.to_dict(orient='records'))])

        self.authors = Author.dict_from_documents(list(self.id2doc.values()))

        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)

        self.unique_chain = " ".join(map(Document.get_text, self.id2doc.values()))

        # Creation of term frequency matrix and vocabulary dictionary
        indptr = [0]
        indices = []
        data = []

        document_len = []  # for tf-idf computation

        for document in self.id2doc.values():
            split_words = split_string(clean_text(document.get_text()))
            document_len.append(len(split_words))
            for word in split_words:
                index = self.vocab.setdefault(word, {"id": len(self.vocab)})["id"]
                indices.append(index)
                data.append(1)
            indptr.append(len(indices))

        self.mat_TF = csr_matrix((data, indices, indptr), dtype=int)

        # Total occurrence of words in corpus computation
        for k, v in self.vocab.items():
            self.vocab[k]["freq"] = self.mat_TF.getcol(v["id"]).sum()
            self.vocab[k]["document_freq"] = np.count_nonzero(self.mat_TF.getcol(v["id"]).toarray())

        # Creation of term frequency-inverse document frequency matrix
        idf = np.log(self.mat_TF.shape[0] / np.array([v["document_freq"] for v in self.vocab.values()]))
        tf_div = np.array([np.array([length for _ in range(len(idf))]) for length in document_len])
        self.mat_TFxIDF = (self.mat_TF / tf_div).multiply(idf).tocsr()

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

    def concorde(self, keyword, context_size):
        """
        Return a dataframe with three column, left context of len <context_size>, the keyword, right context of len <context_size>
        :param keyword: the keyword to match
        :type keyword: str
        :param context_size: the size (in word) of context
        :type context_size: int
        :return: the dataframe
        :rtype DataFrame
        """
        regex = r"(\w+)\W+" * context_size + f"({keyword})" + r"\W+(\w+)" * context_size
        matches = re.findall(regex, self.unique_chain.lower())

        list_of_dict = [dict(left=" ".join(match[0:context_size]), pattern=match[context_size], right=" ".join(match[context_size + 1:])) for match in matches]

        return pd.DataFrame(list_of_dict)

    def search(self, keyword):
        """
        Same as concorde, but return a list of string with 2 word of context
        :param keyword: the keyword to match
        :type keyword: str
        :return: a list of string with 2 word context and the keyword in the middle
        :rtype: list[str]
        """
        return self.concorde(keyword, 2)[['left', 'pattern', 'right']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1).tolist()

    def stats(self, top_count):
        """
        Print some statistic about the corpus. The total number of unique word and the <top_count> most frequent words
        :param top_count: the number of word to print
        :type top_count: int
        :return: None
        """
        print(f"Number of words: {len(self.vocab)}\n")
        print(
            *list(map(
                lambda tp: tp[0],
                sorted(
                    self.vocab.items(),
                    key=lambda row: row[1]["freq"],
                    reverse=True
                )[0:top_count]
            )),
            sep="\n"
        )

    def sort_by_score(self, keywords, max_count=5):
        """
        Return <max_count> sorted document by keywords match
        :param keywords: the string to match with document
        :type keywords: str
        :param max_count: the document count to return
        :type max_count: int
        :return: the sorted by score list of document
        :rtype: list[Document]
        """
        words = split_string(clean_text(keywords))
        vector = np.array([1 if k in words else 0 for k in self.vocab.keys()])
        if np.count_nonzero(vector) < 1:
            print("None of the key words provide match this corpus vocabulary", file=sys.stderr)
            return []
        else:
            scores = np.array([(np.dot(vector, col.toarray().T) / (numpy.linalg.norm(vector) * numpy.linalg.norm(col.toarray())))[0] for col in self.mat_TFxIDF])
            return np.array(list(self.id2doc.values()))[np.argsort(scores)[::-1]][0:max_count]

    def __str__(self):
        return f"Corpus({self.name}, documents={self.ndoc}, authors={self.naut})"

    def __repr__(self):
        return self.__str__()
