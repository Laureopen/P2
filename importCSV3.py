import requests
from bs4 import BeautifulSoup
import csv
import os





# Fonction pour scraper les détails d'un produit
def scraping(product_page_url):
    response = requests.get(product_page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraire les informations nécessaires
    universal_product_code = soup.find('th', string='UPC').find_next_sibling('td').text
    title = soup.find('h1').text
    price_including_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text
    price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text
    number_available = soup.find('th', string='Availability').find_next_sibling('td').text
    number_available = ''.join(filter(str.isdigit, number_available))
    product_description = soup.find('meta', {'name': 'description'})['content'].strip()
    category = soup.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text.strip()
    review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    image_url = soup.find('img')['src'].replace('../../', 'https://books.toscrape.com/')
    
    # Stocker les infos dans un dictionnaire
    product_info = {
        'product_page_url': product_page_url,
        'universal_product_code (upc)': universal_product_code,
        'title': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'review_rating': review_rating,
        'image_url': image_url
    }
    
    return product_info


# URL de la page d'accueil
homepage_url = 'https://books.toscrape.com/'

response = requests.get(homepage_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver tous les liens de catégories
categories = soup.find('ul', class_='nav nav-list').find('ul').find_all('a')

category_links = {}
for category in categories:
    category_name = category.get_text().strip()
    category_url = 'https://books.toscrape.com/' + category['href']
    category_links[category_name] = category_url

# Afficher les catégories et leurs liens
for category, link in category_links.items():
    print(f'{category}: {link}')


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

for category, category_url in category_links.items():
    page_url = 'index.html'
    csv_filename = f'{category}.csv'

    with open(csv_filename, 'r', newline='') as csvfile_in:
        reader = csv.reader(csvfile_in, delimiter=',')
    
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()  # Écrire les en-têtes de colonnes


        while True:
            # Construire l'URL complète de la page à scraper
            url = category_url.replace('index.html', '') + page_url
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
                product_page_url = 'https://books.toscrape.com/catalogue/' + element.a['href'].replace("../", "")
                print(product_page_url)

                # Extraire les informations du produit
                product_info = scraping(product_page_url)
                
                # Écriture des données dans le fichier CSV
                writer.writerow(product_info)

            # Vérifier la présence d'un lien "next" pour la pagination
            next_button = soup.find(class_='next')
            if next_button:
                next_page_url = next_button.find('a')['href']
                page_url = next_page_url  # Mettre à jour page_url pour la page suivante
            else:
                break  # Sortir de la boucle si aucune page suivante n'est trouvée