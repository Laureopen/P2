import os
import csv
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Fonction  Pour télécharger  une image depuis une URL donnée
def download_image(url, directory, filename):
    try:
        # Crée le répertoire  s"il n'existe pas
        os.makedirs(directory, exist_ok=True)

        # Télécharge l'image
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Enregitre l'image  dans le répertoire  spécifié 
        with open(os.path.join(directory, filename), 'wb') as f:
            f.write(response.content)
        print(f"Image {filename} téléchargée avec succès.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image {filename}: {e}")


# Fonction pour extraire les détails  d'un livre depuis sa page
def extract_book_details(book_url, category_name, csv_writer):
    try:
        # Télécharge  le contenu de la  page du livre
        response = requests.get(book_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')


        # Trouve l'image , le titre, le prix, la disponibilité  et le code UPC du livre
        image_tag = soup.find('div', class_='item active').find('img')
        title = soup.find('h1').text.strip()
        price = soup.find('p', class_='price_color').text.strip()
        availability = soup.find('p', class_='instock availability').text.strip()
        upc = soup.find('th', text='UPC').find_next('td').text.strip()


        if image_tag:
            # si  une image  est trouvé , téléchager et ecrire les détails dans le fichier CSV
            image_url = urljoin(book_url, image_tag['src'])
            filename = f"{upc}.jpg"
            directory = os.path.join('images', category_name)
            download_image(image_url, directory, filename)
            csv_writer.writerow([title, price, availability, image_url, filename, book_url])
    except Exception as e:
        print(f"Erreur lors de l'extraction des détails depuis {book_url}: {e}")

# Fonction  pour extraire  les livres d'une catégorie donnée
def extract_books_from_category(category_url, category_name, csv_writer):
    try:
        # Télécharger  le contenu de la page  de la catégorie
        response = requests.get(category_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Trouver les livres vers les pages  des livres 
        book_links = soup.select('h3 a')
        for link in book_links:
            book_url = urljoin(category_url, link['href'])
            extract_book_details(book_url, category_name, csv_writer)
    except Exception as e:
        print(f"Erreur lors de l'extraction des livres depuis {category_url}: {e}")
# URL  de la page  principale du site
main_page_url = 'https://books.toscrape.com/index.html'

#Ouvrir  le fichier CSV  pour écrire  les détails  des livres
with open('books_details.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Availability', 'Image URL', 'Image Filename', 'Book URL'])
    
    # Télécharger le contenu  de la page principale
    try:
        response = requests.get(main_page_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Trouve  les liens  vers les pages  des catégories
        category_links = soup.select('ul.nav-list > li > ul > li > a')
        for link in category_links:
            category_name = link.text.strip()
            category_url = urljoin(main_page_url, link['href'])
            extract_books_from_category(category_url, category_name, writer)
    except Exception as e:
        print(f"Erreur lors de l'extraction des catégories depuis {main_page_url}: {e}")
