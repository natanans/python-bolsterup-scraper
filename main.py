from src.scrapper import PenetronScraper

def main():
    base_url = 'https://penetron.gr'
    scraper = PenetronScraper(base_url=base_url)
    scraper.fetch_product_links()
    scraper.scrape_product_details()
    scraper.save_to_database_script()

if __name__ == '__main__':
    main()