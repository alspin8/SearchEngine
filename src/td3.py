import os

import praw
import urllib
import urllib.request
import xmltodict
import pandas as pd

import config


def reddit(count: int, theme: str) -> list:
    r = praw.Reddit(client_id=config.REDDIT_CID, client_secret=config.REDDIT_SECRET, user_agent=config.REDDIT_AGENT)
    hot_posts = r.subreddit(theme).hot(limit=count)
    return list(map(lambda p: [" ".join(p.title.split()), "reddit"], hot_posts))


def arxiv(count: int, theme: str) -> list:
    url = f'http://export.arxiv.org/api/query?search_query=all:{theme}&start=0&max_results={count}'
    xml = urllib.request.urlopen(url)
    return list(map(lambda x: [" ".join(x["title"].split()), "arxiv"], xmltodict.parse(xml.read().decode('utf-8'))["feed"]["entry"]))


def main() -> None:
    theme = 'football'
    request_count = 100
    out_path = os.path.join(config.DATA_FOLDER, "td3", f"{theme}.csv")
    if not os.path.isfile(out_path):
        docs = [*reddit(request_count, theme), *arxiv(request_count, theme)]
        df = pd.DataFrame(data=docs, columns=["title", "from"])
        df.index.name = "id"
        df.to_csv(out_path, sep=config.CSV_SEP)
    else:
        df = pd.read_csv(out_path, sep=config.CSV_SEP, index_col=0)
        print(df.shape)
        for i, line in enumerate(df["title"]):
            print(f'{i} : words : {len(line.split(" "))},\t sentences: {len(line.split("."))}')
            if len(line) < 20:
                df.drop(i, inplace=True)
        df.to_csv(out_path, sep=config.CSV_SEP)
