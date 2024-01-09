import re


def singleton(cls):
    """
    A decorator to mark singleton
    :param cls: the class to create the singleton
    :type cls: Any
    :return: the unique instance of the class
    :rtype: Any
    """
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


def string_preprocessing(string):
    """
    Return a string without all special character list \n, \t...
    :param string: the string to process
    :type string: str
    :return: process string
    :rtype: str
    """
    return " ".join(string.split()) if len(string) > 0 else "Empty"


def clean_text(string):
    """
    Return a string with only character, as lower case and without leading and ending spaces
    :param string: the string to process
    :type string: str
    :return: process string
    :rtype: str
    """
    return re.sub(r'[^a-zA-Z\s]', '', string).lower().strip()


def stringify_list_to_list(x):
    """
    Return a list of string
    :param x: A stringify list as "[1, 2, 3]"
    :type x: str
    :return: a list of string
    :rtype: list[str]
    """
    return x.strip("[]").replace("'", "").split(", ") if x != '[]' else []


def split_string(string):
    """
    Return a list of word
    :param string: the string to split
    :type string: str
    :return: a list of string
    :rtype: list[str]
    """
    return re.split(r'\s+', string)
