from sys import platform

REDDIT_SECRET = "qj8ZzIfpLH8wMcN99i0GfBG-K2gFUQ"
REDDIT_CID = "YvHn5bV1pAosVjV0XmrxDg"
REDDIT_AGENT = "search_engine"

if platform == "win32":
    DATA_FOLDER = "resource/data"
else:
    DATA_FOLDER = "../resource/data"

CSV_SEP = '\t'
