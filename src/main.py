"""
    This is the main entry, just run the script to open the interface
"""

from sys import platform, path

if platform == "win32":
    path.append("./")

from src.ui.application import application

if __name__ == '__main__':
    application.run(debug=True)
