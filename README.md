# python-book-scraper

Small Python project that scrapes book data from [books.toscrape.com](https://books.toscrape.com) and lets you explore the results in a simple terminal UI.

## Scripts

### `books_scraper.py`
Scrapes book data and saves it to a CSV file.

- Crawls **all pages** on `books.toscrape.com` (or a limited number if you choose).
- Extracts for each book:
  - `title`
  - `price_gbp`
  - `in_stock` (True/False)
  - `stock_text` (raw availability text)
  - `rating` (One–Five/Unknown)
  - `product_url`
- Uses `requests` + `BeautifulSoup` for HTML parsing.
- Command-line options via `argparse`.

**Usage:**

```bash
# Default: scrape all pages, save to books.csv
python books_scraper.py

# Scrape first 3 pages only, custom output
python books_scraper.py -m 3 -o partial_books.csv

# Custom delay between requests (in seconds)
python books_scraper.py --delay 0.5
```

**Main arguments:**

- -o, --output — output CSV filename (default: books.csv)

- -m, --max-pages — maximum number of pages to scrape (default: all)

- --delay — delay between page requests in seconds (default: 1.0)

### `books_filter.py`

- Loads a scraped CSV and provides a small terminal-based explorer.
- Reads books.csv (or any compatible CSV).
- Provides an interactive menu to:
  - Show 10 cheapest books
  - Show 10 most expensive books
  - Show rating distribution
  - Show stock summary (in stock vs out of stock)
  - Show books with a minimum rating (e.g. Three and above)
- Displays results in a readable, aligned format in the terminal.

**Usage:**

```bash
# Default: load books.csv, show menu
python books_filter.py

# Load a different CSV file
python books_filter.py -f custom_books.csv
```

## Requirements

- Python 3.8+
- `requests` and `beautifulsoup4` packages  

Install dependencies:
```bash
pip install -r requirements.txt
```

## Notes

- This project uses books.toscrape.com, a demo site specifically created for scraping practice.
The code and structure are intentionally simple and readable for portfolio and learning purposes.