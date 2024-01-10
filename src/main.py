"""
    This is the main entry, just run the script to open the interface
"""

from sys import platform, path

if platform == "win32":
    path.append("./")

from src.ui.application import application
from src.model.corpus import Corpus

if __name__ == '__main__':
    application.run(debug=True)
    # c = Corpus("python")
    # c.load(500)
    # c.save()
