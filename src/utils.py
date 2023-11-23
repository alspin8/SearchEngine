def clean_string(string):
    if type(string) is str:
        return " ".join(string.split())
    else:
        return string


author_to_list = lambda x: x.strip("[]").replace("'", "").split(", ") if x != '[]' else []
