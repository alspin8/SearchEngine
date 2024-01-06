class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []

    def add(self, production):
        self.production.append(production)
        self.ndoc += 1

    def __str__(self):
        return f"Author({self.name}, documents={self.ndoc})"

    def __repr__(self):
        return self.__str__()
