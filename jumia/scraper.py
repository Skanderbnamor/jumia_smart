import sqlite3
import requests
from bs4 import BeautifulSoup
import json


def get_all_page():
    urls = []
    page_number = 1
    for i in range(16):
        url = f"https://www.jumia.com.tn/smartphones/?page={page_number}#catalog-listing"
        page_number += 1
        urls.append(url)
    return urls


def creer_base_de_donnees(jumia):
    conn = sqlite3.connect(jumia)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS smartphone
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, price_final FLOAT, old_price FLOAT, discount_f INTEGER, product_url TEXT , image TEXT)''')

    conn.commit()
    conn.close()


creer_base_de_donnees(r"C:\Users\skand\PycharmProjects\jumia_smart\jumia.db")


def get_smartphone(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    smartphones = soup.find_all("article", class_="prd _fb col c-prd")
    tel = []
    for smartphone in smartphones:
        nom = smartphone.find("h3", class_="name").text.strip().lower()
        price_final = float(
            smartphone.find("div", class_="prc").text.strip().replace(',', '').replace(' TND', '')) if smartphone.find(
            "div",
            class_="prc") else 0

        old_price = float(
            smartphone.find("div", class_="old").text.strip().replace(',', '').replace(' TND', '')) if smartphone.find(
            "div", class_="old") else 0
        discount_f = smartphone.find("div", class_="bdg _dsct _sm").text.strip() if smartphone.find("div",
                                                                                                    class_="bdg _dsct _sm") else "N/A"
        product_url = "https://www.jumia.com.tn" + smartphone.find("a", class_="core")["href"]
        image = smartphone.find("img")["data-src"] if smartphone.find("img") else "N/A"

        tel.append({
            "nom": nom,
            "price_final": price_final,
            "old_price": old_price,
            "discount_f": discount_f,
            "product_url": product_url,
            "image": image
        })

    conn = sqlite3.connect(r"C:\Users\skand\PycharmProjects\jumia_smart\jumia.db")
    c = conn.cursor()

    for donnee in tel:
        c.execute(
            "INSERT INTO smartphone (nom, price_final, old_price, discount_f, product_url,image) VALUES (?, ?, ?, ?, ?,?)",
            (donnee['nom'], donnee['price_final'], donnee['old_price'], donnee['discount_f'], donnee['product_url'],
             donnee['image']))

    conn.commit()
    conn.close()


def get_all_smartphone():
    pages = get_all_page()
    for page_index, page in enumerate(pages):
        get_smartphone(url=page)
        print(f"Finished scraping page {page_index + 1}.")


#get_all_smartphone()
def cree_json():
    all_smartphones = []

    for page in range(1, 15):
        print('---', page, '---')
        url = 'https://www.jumia.com.tn/mlp-telephone-tablette/smartphones/?page=' + str(page)
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
        else:
            print(f"Erreur lors de la récupération de la page : {response.status_code}")
            exit()

        # Utiliser BeautifulSoup pour analyser le HTML
        soup = BeautifulSoup(page_content, 'html.parser')

        # Trouver tous les éléments qui contiennent les informations des smartphones
        smartphones = soup.find_all("article", class_="prd _fb col c-prd")

        # Extraire les informations pour chaque smartphone
        for phone in smartphones:
            try:
                # Nom du smartphone
                nom = phone.find("h3", class_="name").text.strip().lower()
                brand = nom.split()[0]
                price_final = float(
                    phone.find("div", class_="prc").text.strip().replace(',', '').replace(' TND','')) if phone.find("div",
                    class_="prc") else 0
                old_price = float(
                    phone.find("div", class_="old").text.strip().replace(',', '').replace(' TND',
                                                                                               '')) if phone.find(
                    "div", class_="old") else 0
                discount_f = phone.find("div", class_="bdg _dsct _sm").text.strip() if phone.find("div",
                                                                                                            class_="bdg _dsct _sm") else "N/A"
                product_url = "https://www.jumia.com.tn" + phone.find("a", class_="core")["href"]
                image = phone.find("img")["data-src"] if phone.find("img") else "N/A"


                # Ajouter les informations du smartphone à la liste
                all_smartphones.append({
                    "nom": nom,
                    "brand":brand,
                    "price_final": price_final,
                    "old_price": old_price,
                    "discount_f": discount_f,
                    "product_url": product_url,
                    "image": image
                })
            except AttributeError as e:
                # Si une information manque, passer à l'élément suivant
                print(f"Erreur lors de l'extraction des informations : {e}")
                continue

    # Supprimer le contenu du fichier avant de le remplir
    with open(r'C:\Users\skand\PycharmProjects\jumia_smart\smartphones.json', 'w', encoding='utf-8') as json_file:
        # Écrire les informations dans un fichier JSON, une ligne par smartphone avec virgule
        json_file.write('[\n')  # Début de la liste JSON
        for i, smartphone in enumerate(all_smartphones):
            json_string = json.dumps(smartphone, ensure_ascii=False)
            if i < len(all_smartphones) - 1:
                json_file.write(json_string + ',\n')
            else:
                json_file.write(json_string + '\n')
        json_file.write(']')  # Fin de la liste JSON

#cree_json()
