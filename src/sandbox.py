import praw

from src import config
from src.model.document import Document


def main():
    r = praw.Reddit(client_id=config.REDDIT_CID, client_secret=config.REDDIT_SECRET, user_agent=config.REDDIT_AGENT)
    hot_posts = r.subreddit('football').hot(limit=1)
    id2doc = {}
    for i, post in enumerate(hot_posts):
        id2doc[i] = Document(title=post.title, author=post.author_flair_text, date=post.created_utc, url=post.url, text=post.selftext)

    print(id2doc)


if __name__ == "__main__":
    main()
