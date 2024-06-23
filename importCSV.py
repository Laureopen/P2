import requests
from bs4 import BeautifulSoup
import csv

# declaration de la fontion avec argement
def scraping (url, CSV_filename): 

    # Effectuer une requête GET à la page
    response = requests.get(url)
    response.raise_for_status() # verifier que la requête a reussi

    # Parser la contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraire les informations necessaire
    product_page_url = url
    universal_product_code = soup.find('th', string='UPC').find_next_sibling('td').text
    title = soup.find('h1').text
    price_including_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text
    price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text
    number_available = soup.find('th', string='Availability').find_next_sibling('td').text
    number_available = ''.join(filter(str.isdigit, number_available))
    product_description = soup.find('meta', {'name': 'description'})['content'].strip()
    category = soup.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text.strip()
    review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    image_url = url.rsplit('/', 3)[0] + '/' + soup.find('img')['src']

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

    # Écriture des données dans le fichier CSV
    with open(CSV_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        

        
        # Écriture de la ligne de données
        writer.writerow(product_info)


    print(f"Les données ont été écrites dans {CSV_filename}")




scraping("http://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html", "product_info.csv")

