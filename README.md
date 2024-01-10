# Search Engine

### Logiciel requis
- Python 3.10
- Un outil de packaging (pip, conda, ...)
- Un navigateur

### Installation

Cloner le repo git.  
Plusieurs options :
- Dans un cli avec la commande suivante `git clone --branch <tag-name> https://github.com/alspin8/SearchEngine.git` 
- Télécharger l'archive dans Code/Download Zip
- Dans github desktop avec l'url `https://github.com/alspin8/SearchEngine.git`

Créer un environnement virtuel (optionnel mais recommandé).  
Plusieurs options :
- Un environement python natif `python -m venv <path>` (a la racine du projet de préférence)
- Un environement conda `conda create --name <name> python` (ou avec l'interface graphique)

Installer les packages.   
Plusieurs options :
- Env python natif `pip install -r config/requirement.txt`
- Env conda, ajouter `--file config/requirement.txt` lors de la création de l'env

### Lancement d'un script

Pour les v1 et v2, les entrées du programme sont les notebookTD5 et notebookTD7.   
Pour la v3 il faut exécuter le fichier main.py dans le dossier src `python main.py`