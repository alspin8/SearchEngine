from src.utils import clean_string


class Author:
    def __init__(self, name):
        self.name = clean_string(name)
        self.ndoc = 0
        self.production = []

    def add(self, production):
        self.production.append(production)
        self.ndoc += 1

    def __str__(self):
        return f"Author({self.name}, {self.ndoc})"

    def __repr__(self):
        return self.__str__()
