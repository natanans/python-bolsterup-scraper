import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import os

class PenetronScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.catalogue_url_template = f'{self.base_url}/index.php/en/products/product-catalogue?start={{}}'
        self.product_links = []
        self.products = []
        self.visited_pages = set()
        self.db_name = 'products.db'

    def fetch_product_links(self, start=0, step=10):
        """Fetch product links from the paginated catalogue."""
        while True:
            current_url = self.catalogue_url_template.format(start)
            if current_url in self.visited_pages:
                break
            self.visited_pages.add(current_url)

            response = requests.get(current_url)
            if response.status_code != 200:
                print(f"Failed to retrieve page: {current_url}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            found_links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if '/en/products/item/' in href:
                    full_link = self.base_url + href if not href.startswith('http') else href
                    if full_link not in self.product_links:
                        found_links.append(full_link)

            if not found_links:
                print(f"No more products found at page {current_url}. Stopping pagination.")
                break

            self.product_links.extend(found_links)
            print(f"Page {current_url}: Found {len(found_links)} products.")
            start += step

        print(f"Total products found: {len(self.product_links)}")
        with open('product_links.json', 'w') as file:
            json.dump(self.product_links, file, indent=4)
        print("Product links saved to 'product_links.json'.")

    def scrape_product_details(self):
        """Scrape product details for all collected product links."""
        counter = 0
        for link in self.product_links:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract details
            detailed_description = ''
            consumption_information = ''
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                if 'SHORT DESCRIPTION & APPLICATIONS' in paragraph.get_text():
                    detailed_description = paragraph.get_text(strip=True).replace('SHORT DESCRIPTION & APPLICATIONS', '').strip()
                elif 'CONSUMPTION INFORMATION' in paragraph.get_text():
                    consumption_information = paragraph.get_text(strip=True).replace('CONSUMPTION INFORMATION', '').strip()

            # Extract image source
            og_image_meta = soup.find('meta', {'property': 'og:image'})
            name_image_meta = soup.find('meta', {'name': 'image'})
            image_url = og_image_meta['content'] if og_image_meta else (name_image_meta['content'] if name_image_meta else None)

            # Extract document links
            document_links = []
            for a_tag in soup.find_all('a', href=True):
                if 'docman_track_download' in a_tag.get('class', []) or 'data-title' in a_tag.attrs:
                    doc_title = a_tag.get('data-title', '').strip()
                    doc_href = a_tag['href'].strip()
                    full_doc_href = self.base_url + doc_href if doc_href.startswith('/') else doc_href
                    document_links.append({'title': doc_title, 'url': full_doc_href})

            # Extract product categories
            categories = []
            categories_block = soup.find('div', {'class': 'k2CategoriesListBlock'})
            if categories_block:
                category_links = categories_block.find_all('a', href=True)
                for category_link in category_links:
                    cat_title = category_link.find('span', {'class': 'catTitle'}).get_text(strip=True)
                    cat_href = category_link['href'].strip()
                    full_cat_href = self.base_url + cat_href if cat_href.startswith('/') else cat_href
                    categories.append({'category': cat_title, 'url': full_cat_href})

            # Add product data to the list
            self.products.append({
                'url': link,
                'detailed_description': detailed_description,
                'consumption_information': consumption_information,
                'image_url': image_url,
                'documents': document_links,
                'categories': categories
            })
            counter += 1
            print(f"Scraped {counter} products.")

        with open('products.json', 'w') as file:
            json.dump(self.products, file, indent=4)
        print("Product details saved to 'products.json'.")

    def save_to_database_script(self):
        """Save the scraped product details into an SQLite database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                detailed_description TEXT,
                consumption_information TEXT,
                image_url TEXT,
                documents TEXT,
                categories TEXT
            )
        ''')

        for product in self.products:
            cursor.execute('''
                INSERT INTO products (
                    url, detailed_description, consumption_information, image_url, documents, categories
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                product['url'],
                product['detailed_description'],
                product['consumption_information'],
                product['image_url'],
                json.dumps(product['documents']),
                json.dumps(product['categories'])
            ))

        conn.commit()
        conn.close()
        print(f"Data saved to SQLite database '{self.db_name}'.")

