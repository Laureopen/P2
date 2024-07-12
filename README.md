# Books to Scrape!

Description:
	
Ce projet est conçu pour extraire  des données de livre et les images associées depuis le site " Books to Scrape". Les données et les images  sont ensuite stockées dans des dossiers organisés par catégorie.

# Prérequis

* Python 3 installé sur votre machine 
* Virtualenv installé sur votre machine

## Etape1: Se mettre à la racine du projet

    cd Projet2
##  Etape 2: Pour créer environnement virtuel

    python -m venv Projet2
   * fonctionne sous Windows, Linus et MacOS.
### Pour activer l'environnement sous Linux et MacOs

    source Projet2/bin/activate
### Pour activer l'nvironnement sous windows
			
    Projet2\Scripts\activate
    
## Etape 3: Installez les dépendances

    pip install -r requirements.txt

## Etape 4: Extraire tout les produits de toutes les catégories

    python importCSV3.py
   * Si le script fonctionne  il va créer un fichier csv_files et un fichier images. Ces deux fichiers représentent l’extraction de l’ensemble des livres des différentes catégories et des images associés à ces catégories.


