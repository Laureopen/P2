# Books to Scrape!

Description:
	
Ce projet est conçu pour extraire  des données de livre et les images associées depuis le site " Books to Scrape". Les données et les images  sont ensuite stokées dans des dossiers organisés par catégorie.

# Prérequis

* Python installé sur votre machine
* Beautifulsoup4 installé sur votre machine

## Etape1: Clonez le projet

    git clone http:github.com/

## Etape2: Se mettre à la racine du projet

    cd P2

## Etape 3: Installez les dépendences

    pip install -r requirements.txt

## Etape 4: Lancer  le script pour extraire les données d'un seul produit

    python importCSV.py
   *Si le script à fonctionner il indiquera en invite de commande "Les données ont été écrites  dans product_info.csv" 
		
## Etape 5: Lancer le script pour extraire toutes les données des produits d'une catégorie

    python importCSV2.py
 * Si le script  fonctionne il indique le "nombre de ligne"   
  

## Etape 6: Extraire tout les produits de toutes les catégories

    python importCSV3.py
   * Si le script fonctionne  il indiquera  visuellement l'ensemble  des urls et des catégories de ces livres.
   * Pour chaque catégories 1 fichiers csv sera créer avec la liste de ces livres.

## Etape 7: Extraire et enregistrer les fichiers images

    python importImagescsv.py
   * Le script enregistre l'ensemble  des images  de chaque catégories de livres et les ranges individuellement dans un dossier.

