import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Dictionnaire de correspondance pour les évaluations
review_rating_mapping = {
    'One': '1',
    'Two': '2',
    'Three': '3',
    'Four': '4',
    'Five': '5'
}

# Fonction pour scraper les détails d'un produit
def scraping(product_page_url):
    try:
        response = requests.get(product_page_url, timeout=10)
        response.raise_for_status()
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
        image_url = urljoin(product_page_url, soup.find('img')['src'].replace('../../', 'https://books.toscrape.com/'))

        # Mapping de review_rating
        review_rating = review_rating_mapping.get(review_rating, '0')
        
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
        
    except Exception as e:
        print(f"Erreur lors du scraping de {product_page_url}: {e}")
        return None

# Fonction pour télécharger une image depuis une URL donnée
def download_image(url, directory, filename):
    try:
        # Crée le répertoire s'il n'existe pas
        os.makedirs(directory, exist_ok=True)
        
        # Nettoie le nom du fichier pour éviter les problèmes de système de fichiers
        filename = "".join([c if c.isalnum() or c in "._-" else "_" for c in filename])

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(os.path.join(directory, filename), 'wb') as f:
            f.write(response.content)
        print(f"Image {filename} téléchargée avec succès depuis {url}.")
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image {filename} depuis {url}: {e}")

# URL de la page d'accueil
homepage_url = 'https://books.toscrape.com/'

response = requests.get(homepage_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver tous les liens de catégories
categories = soup.find('ul', class_='nav nav-list').find('ul').find_all('a')

category_links = {}
for category in categories:
    category_name = category.get_text().strip()
    category_url = urljoin(homepage_url, category['href'])
    category_links[category_name] = category_url

# Créer un dossier principal 'images' pour les images
images_folder = os.path.join(os.getcwd(), 'images')
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# Créer un dossier principal 'csv_files' pour les fichiers CSV
csv_folder = os.path.join(os.getcwd(), 'csv_files')
if not os.path.exists(csv_folder):
    os.makedirs(csv_folder)

# Scraper pour chaque catégorie
for category, category_url in category_links.items():
    page_url = 'index.html'
    category_csv_folder = os.path.join(csv_folder, category)
    if not os.path.exists(category_csv_folder):
        os.makedirs(category_csv_folder)
    csv_filename = os.path.join(category_csv_folder, f'{category}.csv')

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'product_page_url',
            'universal_product_code (upc)',
            'title',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'product_description',
            'category',
            'review_rating',
            'image_url',
            'image_filename'
        ], delimiter=';')
        writer.writeheader()  # Écrire les en-têtes de colonnes

        bpage = True

        while bpage:
            # Construire l'URL complète de la page à scraper
            url = urljoin(category_url, page_url)
            print(f'Scraping page: {url}')  # Afficher l'URL de la page en cours de scraping
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
                product_page_url = urljoin('https://books.toscrape.com/catalogue/', element.a['href'].replace("../", ""))
                print(f"Scraping product page: {product_page_url}")

                # Extraire les informations du produit
                product_info = scraping(product_page_url)

                # Télécharger l'image du produit
                if product_info:
                    image_url = product_info['image_url']
                    filename = f"{product_info['title']}.jpg"
                    directory = os.path.join(images_folder, category)
                    download_image(image_url, directory, filename)
                    product_info['image_filename'] = filename

                    # Écriture des données dans le fichier CSV de la catégorie
                    writer.writerow(product_info)
                    
            # Vérifier la présence d'un lien "next" pour la pagination
            next_button = soup.find(class_='next')
            if next_button:
                next_page_url = next_button.find('a')['href']
                page_url = next_page_url  # Mettre à jour page_url pour la page suivante
            else:
                bpage = False  # Sortir de la boucle si aucune page suivante n'est trouvée

print('Scraping terminé.')
