# Penetron Product Catalogue Scraper

## Overview

This project is a web scraper designed to navigate through the Penetron product catalogue, extract key information from each product, and store it in JSON format. The data can then be inserted into a SQL database for further processing or analysis.

## Features

- **Pagination Support**: Automatically navigates through the paginated product catalogue.
- **Data Extraction**: Scrapes the following details from each product:
  - Short description
  - Consumption information
  - Metadata (e.g., categories, documents)
  - Product image URL
- **Data Storage**:
  - Saves product links to `product_links.json`.
  - Saves detailed product data to `products.json`.
  - Inserts data into an SQLite database `products.db`.

## Project Structure
project/
├── main.py
└── src/
└── scrapper.py

- `main.py`: Entry point of the application.
- `src/scrapper.py`: Contains the `PenetronScraper` class with all scraping logic.

## Requirements

- Python 3.x
- Packages:
  - `requests`
  - `beautifulsoup4`

## Installation

1. **Clone the Repository**

   ```bash
   git clone <https://github.com/natanans/python-bolsterup-scraper.git>
   cd project
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *Alternatively, install packages manually:*

   ```bash
   pip install requests beautifulsoup4
   ```

## Usage

1. **Navigate to Project Directory**

   ```bash
   cd project
   ```

2. **Run the Scraper**

   ```bash
   python main.py
   ```

   This will execute the following steps:

   - Fetch product links from the Penetron catalogue.
   - Scrape detailed information for each product.
   - Save data to `product_links.json` and `products.json`.
   - Insert data into the SQLite database `products.db`.

## How It Works

### `PenetronScraper` Class

- **Initialization**

  ```python
  scraper = PenetronScraper(base_url='https://penetron.gr')
  ```

- **Methods**

  - `fetch_product_links()`: Collects product URLs from the catalogue pages.
  - `scrape_product_details()`: Extracts details from each product page.
  - `save_to_database_script()`: Inserts scraped data into the SQLite database.

### Workflow

1. **Fetch Product Links**

   The scraper navigates through the catalogue pages, collecting links to individual product pages.

2. **Scrape Product Details**

   For each product link, the scraper extracts:

   - Detailed description
   - Consumption information
   - Image URL
   - Document links
   - Categories

3. **Save Data**

   - **JSON Files**: Data is saved to `product_links.json` and `products.json` for review.
   - **Database**: Data is inserted into `products.db` using the provided SQL schema.

## Database Schema

The SQLite database `products.db` is created with the following schema:

```sql
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    detailed_description TEXT,
    consumption_information TEXT,
    image_url TEXT,
    documents TEXT,
    categories TEXT
);
```

- **Columns**:
  - `id`: Auto-incrementing primary key.
  - `url`: Product page URL.
  - `detailed_description`: Short description and applications.
  - `consumption_information`: Usage and consumption details.
  - `image_url`: URL of the product image.
  - `documents`: JSON string of related documents.
  - `categories`: JSON string of product categories.

## Customization

- **Adjust Pagination**

  Modify the `fetch_product_links` method in `scrapper.py` to limit the number of pages or adjust the starting point.

- **Change Base URL**

  If the base URL changes, update the `base_url` parameter when initializing the `PenetronScraper` class.

## Error Handling

- The scraper includes basic error handling for network requests and parsing.
- Any failures to retrieve or parse pages are logged to the console.

## Dependencies

- **requests**: For making HTTP requests.

  ```bash
  pip install requests
  ```

- **beautifulsoup4**: For parsing HTML content.

  ```bash
  pip install beautifulsoup4
  ```

## Files Generated

- `product_links.json`: Contains all the product URLs collected.
- `products.json`: Contains the detailed product data.
- `products.db`: SQLite database with the scraped data.

## Contact

For any questions or suggestions, please contact [natananshiferaw@gmail.com](mailto:natananshiferaw@gmail.com).

## License

This project is licensed under the MIT License.

---

