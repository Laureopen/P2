import requests
from bs4 import BeautifulSoup
import csv
from importCSV import scraping
import re 

# Fonction pour nettoyer les caractères spéciaux
def clean_special_chars(text):
    if isinstance(text, str):
        return re.sub(r'[Â�]', '', text)
    return text

# URL de la catégorie de livres
base_url = 'https://books.toscrape.com/catalogue/category/books/historical-fiction_4/'
catalogue_url = 'https://books.toscrape.com/catalogue/'
page_url = 'index.html'



# Nom du fichier CSV à créer
CSV_filename = 'product_pod.csv'

# Noms des en-têtes de colonnes
fieldnames = [
    'product_page_url',
    'universal_product_code (upc)',
    'title',
    'price_including_tax',
    'price_excluding_tax',
    'number_available',
    'product_description',
    'category',
    'review_rating',
    'image_url'
]


# Créer et ouvrir le fichier CSV en mode écriture pour y ajouter les en-têtes
with open(CSV_filename, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Écrire les en-têtes de colonnes


while True:
    # Construire l'URL complète de la page à scraper
    url = base_url + page_url
    print(f'Scrapping page: {url}')  # Afficher l'URL de la page en cours de scraping
    response = requests.get(url)  # Envoyer une requête GET à l'URL

    # Vérifier si la requête a réussi
    if response.status_code != 200:
        print(f'Arrêt du scraping. Code de statut : {response.status_code}')
        break

    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver tous les éléments de livres sur la page
    book_elements = soup.find_all(class_='product_pod')

    # Parcourir tous les éléments de livre trouvés pour extraire les informations
    for element in book_elements:
        product_page_url = catalogue_url + element.a['href'].replace("../", "")
        # Nettoyer les caractères spéciaux dans l'URL
        product_page_url = clean_special_chars(product_page_url)
        print(product_page_url)

        # Appel de la fonction avec son argument 
        scraping(product_page_url, "product_pod.csv")

    # Vérifier la présence d'un lien "next" pour la pagination
    next_button = soup.find(class_='next')
    if next_button:
        next_page_url = next_button.find('a')['href']
        page_url = next_page_url  # Mettre à jour page_url pour la page suivante
    else:
        break  # Sortir de la boucle si aucune page suivante n'est trouvée



