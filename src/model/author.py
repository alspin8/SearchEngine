from src.model.document import Document


class Author:
    """
    A class used to represent an author

    Attributes
    ----------
    name : str
        the name of author
    ndoc : int
        the amount of document write by this author
    production : list[Document]
        documents write by this author

    Methods
    -------
    get_name()
        Return the author name
    get_document_count()
        Return the amount of document write by this author
    add_document(production)
        Add new document to the author documents
    get_document(index):
        Return document at index
    get_documents()
        Return all documents
    dict_from_documents(documents)
        Create dictionary of author from documents
    """
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []

    def get_name(self):
        """
        Return the author name
        :return: the name of the author
        :rtype: str
        """
        return self.name

    def get_document_count(self):
        """
        Return the amount of document write by this author
        :return: the amount of document
        :rtype: int
        """
        return self.ndoc

    def add_document(self, production):
        """
        Add new document to the author documents
        :param production: the document to add
        :type production: Document
        """
        self.production.append(production)
        self.ndoc += 1

    def get_document(self, index):
        """
        Return document at index
        :param index: the index of needed document
        :type index: int
        :return: the document
        :rtype: Document
        :raise IndexError
        """
        return self.production[index]

    def get_documents(self):
        """
        Return all documents
        :return: all documents
        :rtype: list[Document]
        """
        return self.production

    def __str__(self):
        return f"Author({self.name}, documents={self.ndoc})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def dict_from_documents(documents):
        """
        Create dictionary of author from documents
        :param documents: a list of document
        :type documents: list[Document]
        :return: a dict of all author named in given documents
        :rtype: dict[int, Author]
        """
        authors = {}
        for doc in documents:
            if doc.author and doc.author not in authors:
                authors[doc.author] = Author(name=doc.author)
            authors[doc.author].add_document(doc)

            if doc.get_type() == "arxiv":
                for author in doc.co_authors:
                    if author not in authors:
                        authors[author] = Author(name=author)
                    authors[author].add_document(doc)

        return authors
