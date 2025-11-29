import csv
import time
from dataclasses import dataclass, asdict
from typing import List, Optional

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"


@dataclass
class Book:
    title: str
    price_gbp: float
    in_stock: bool
    stock_text: str
    rating: str
    product_url: str


def fetch_page(url: str) -> Optional[str]:
    """Fetch a page and return HTML text or None on failure."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def parse_book_list_page(html: str) -> List[Book]:
    """Parse a listing page and return a list of Book objects."""
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.select("article.product_pod")
    books: List[Book] = []

    for art in articles:
        # Title
        title_tag = art.select_one("h3 a")
        title = (
            title_tag["title"].strip()
            if title_tag and title_tag.has_attr("title")
            else "UNKNOWN"
        )

        # Detail URL
        href = title_tag["href"] if title_tag and title_tag.has_attr("href") else ""
        # Handle relative URLs like "../../../"
        product_url = href.replace("../../../", "catalogue/")
        product_url = BASE_URL + product_url.lstrip("/")

        # Price
        price_tag = art.select_one(".price_color")
        raw_price = price_tag.get_text(strip=True) if price_tag else "£0.00"
        # raw_price looks like "£51.77"
        try:
            price_gbp = float(raw_price.replace("£", ""))
        except ValueError:
            price_gbp = 0.0

        # Stock
        stock_tag = art.select_one(".availability")
        stock_text = stock_tag.get_text(strip=True) if stock_tag else ""
        in_stock = "In stock" in stock_text

        # Rating (e.g. "star-rating Three")
        rating_tag = art.select_one(".star-rating")
        rating = "Unknown"
        if rating_tag and rating_tag.has_attr("class"):
            classes = rating_tag["class"]
            # classes example: ['star-rating', 'Three']
            for c in classes:
                if c not in ("star-rating",):
                    rating = c
                    break

        books.append(
            Book(
                title=title,
                price_gbp=price_gbp,
                in_stock=in_stock,
                stock_text=stock_text,
                rating=rating,
                product_url=product_url,
            )
        )

    return books


def find_next_page_url(html: str, current_url: str) -> Optional[str]:
    """Return the absolute URL of the next page, or None if there isn't one."""
    soup = BeautifulSoup(html, "html.parser")
    next_link = soup.select_one("li.next a")
    if not next_link or not next_link.has_attr("href"):
        return None

    href = next_link["href"]
    # Handle relative path like "page-2.html"
    if "catalogue/" in current_url:
        base = current_url.rsplit("/", 1)[0]
    else:
        base = BASE_URL.rstrip("/")

    if href.startswith("http"):
        return href
    elif href.startswith("/"):
        return BASE_URL.rstrip("/") + href
    else:
        return f"{base}/{href}"


def scrape_all_books(start_url: str = BASE_URL) -> List[Book]:
    """Scrape all pages starting from start_url and return list of Book."""
    all_books: List[Book] = []
    current_url = start_url

    page_num = 1
    while current_url:
        print(f"[INFO] Fetching page {page_num}: {current_url}")
        html = fetch_page(current_url)
        if html is None:
            print("[WARN] Skipping page due to fetch error.")
            break

        books = parse_book_list_page(html)
        print(f"[INFO] Found {len(books)} books on this page.")
        all_books.extend(books)

        next_url = find_next_page_url(html, current_url)
        if not next_url:
            print("[INFO] No more pages. Scraping complete.")
            break

        current_url = next_url
        page_num += 1

        # Be polite: small delay
        time.sleep(1)

    return all_books


def save_books_to_csv(books: List[Book], filename: str = "books.csv") -> None:
    """Save the list of Book objects to a CSV file."""
    if not books:
        print("[WARN] No books to save.")
        return

    fieldnames = list(asdict(books[0]).keys())
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(asdict(book))

    print(f"[INFO] Saved {len(books)} books to {filename}")


def main():
    print("[START] Scraping books.toscrape.com")
    books = scrape_all_books()
    save_books_to_csv(books)
    print("[DONE]")


if __name__ == "__main__":
    main()
