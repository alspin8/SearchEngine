import urllib
from sys import platform, path

import praw
import xmltodict

from src import config
from src.model.document import Document

if platform == "win32":
    path.append("./")

from src.model.corpus import Corpus

if __name__ == '__main__':
    theme = 'chess'

    # corpus = Corpus()
    # corpus.load(theme, max_size=20)
    # corpus.save()
    #
    # v = "\n".join(str(item) for item in corpus.get(sort="date"))
    #
    # print(v)

    # r = praw.Reddit(client_id=config.REDDIT_CID, client_secret=config.REDDIT_SECRET, user_agent=config.REDDIT_AGENT, check_for_async=False)
    # hot_posts = r.subreddit(theme).hot(limit=5, params={"after": "t3_18zn5g8"})
    # hot_posts2 = r.subreddit(theme).hot(limit=2, params={"after": 5})
    # res = list(map(Document.from_reddit, hot_posts))

    # limit = 15
    # posts = []
    # to_query = limit
    # cursor = ""
    # while len(posts) < limit:
    #     hot_posts = r.subreddit(theme).hot(limit=to_query, params={"after": cursor})
    #
    #     to_query = 0
    #     for p in hot_posts:
    #         if len(p.title) < 20:
    #             to_query += 1
    #         else:
    #             posts.append(p)
    #         cursor = p.name
    #
    # fl = list(map(lambda post: (post.name, post.title), posts))
    #
    # print(*fl, sep="\n")

    limit = 5
    posts = []
    to_query = limit
    cursor = 10
    while len(posts) < limit:
        url = f'http://export.arxiv.org/api/query?search_query=all:{theme}&start={cursor}&max_results={to_query}'
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

    res = list(map(lambda item: (item["api_index"], item["title"]), posts))

    print(*res, sep="\n")
