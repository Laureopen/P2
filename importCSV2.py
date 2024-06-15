import requests
from bs4 import BeautifulSoup
import csv
from importCSV import scraping

# URL de la catégorie de livres
base_url = 'https://books.toscrape.com/catalogue/category/books/historical-fiction_4/'
catalogue_url = 'https://books.toscrape.com/catalogue/'
page_url = 'index.html'

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



