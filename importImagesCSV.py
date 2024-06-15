import requests
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import csv

# Fonction pour télécharger une image depuis une URL et l'enregistrer localement
def download_image(url, directory, filename):
    try:
        os.makedirs(directory, exist_ok=True)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(os.path.join(directory, filename), 'wb') as f:
            f.write(response.content)
        print(f"Image {filename} téléchargée avec succès.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image {filename}: {e}")
    except Exception as e:
        print(f"Exception lors du téléchargement de l'image {filename}: {e}")

# Fonction pour extraire les détails des livres
def extract_book_details(book_url, category_name, csv_writer):
    try:
        response = requests.get(book_url, timeout=10)
        response.raise_for_status()
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            image_tag = soup.find('div', class_='item active').find('img')
            title = soup.find('h1').text.strip()
            price = soup.find('p', class_='price_color').text.strip()
            availability = soup.find('p', class_='instock availability').text.strip()
            upc = soup.find('th', text='UPC').find_next('td').text.strip()
            if image_tag:
                image_url = urljoin(book_url, image_tag['src'])
                filename = f"{upc}.jpg"
                directory = os.path.join('chemin_vers_dossier_images', category_name)
                download_image(image_url, directory, filename)
                csv_writer.writerow([title, price, availability, image_url, filename, book_url])
            else:
                print(f"Aucune image trouvée pour {book_url}")
        else:
            print(f"Échec de la requête HTTP vers {book_url}. Code de statut HTTP : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP vers {book_url}: {e}")
    except Exception as e:
        print(f"Exception lors de l'extraction des détails depuis {book_url}: {e}")

# Fonction pour extraire les livres d'une catégorie
def extract_books_from_category_page(category_url, category_name, csv_writer):
    try:
        response = requests.get(category_url, timeout=10)
        response.raise_for_status()
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            book_links = soup.select('h3 a')
            for link in book_links:
                book_url = urljoin(category_url, link['href'])
                extract_book_details(book_url, category_name, csv_writer)
        else:
            print(f"Échec de la requête HTTP vers {category_url}. Code de statut HTTP : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP vers {category_url}: {e}")
    except Exception as e:
        print(f"Exception lors de l'extraction des livres depuis {category_url}: {e}")

# Script principal
main_page_url = 'https://books.toscrape.com/index.html'

with open('books_details.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Availability', 'Image URL', 'Image Filename', 'Book URL'])
    try:
        response = requests.get(main_page_url, timeout=10)
        response.raise_for_status()
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            category_links = soup.select('ul.nav-list > li > ul > li > a')
            for link in category_links:
                category_name = link.text.strip()
                category_url = urljoin(main_page_url, link['href'])
                extract_books_from_category_page(category_url, category_name, writer)
        else:
            print(f"Échec de la requête HTTP vers {main_page_url}. Code de statut HTTP : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP vers {main_page_url}: {e}")
    except Exception as e:
        print(f"Exception lors de l'extraction des catégories depuis {main_page_url}: {e}")

