import requests
from bs4 import BeautifulSoup
import csv

from importCSV import scraping


# URL de la categorie de livres
url = 'https://books.toscrape.com/catalogue/category/books/science_22/index.html'
catalogue_url = 'https://books.toscrape.com/catalogue/'

# suffixe pour la première page de la catégorie
page_suffixe = 'index.html'

# liste pour stoker les informations des livres
books_url = []


# Boucle pour parcourir toutes les pages  de la catégorie

print(f'Scrapping page:{url}')# Afficher l'url  de la page en cours  de scraping
response = requests.get(url) # Envoyer une requête GET à l'URL

# Vérifier  si la requête à réussi
if response.status_code != 200:
    print (f'Arrêt du scraping. code de status :{response.status_code}')


# Parser la contenu HTML avec BeautifulSoup/Analyser  le contenu HTML de la réponse
soup =BeautifulSoup(response.content,'html.parser')

#Trouver tous les elements de livres suer la page
book_elements =soup.find_all(class_='product_pod')



  # Parcourir tous les elements de livre trouvés pour extraire les informations
for element in book_elements:
        product_page_url = catalogue_url+ element.a['href'].replace ("../","")
        print (product_page_url)

        url = product_page_url

       # Appel de la fonction avec son argument 
        scraping(url, "product_pod.csv")





