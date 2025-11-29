import csv
from dataclasses import dataclass
from typing import List


@dataclass
class Book:
    title: str
    price_gbp: float
    in_stock: bool
    stock_text: str
    rating: str
    product_url: str


def load_books_from_csv(filename: str) -> List[Book]:
    books: List[Book] = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                price = float(row["price_gbp"])
            except (KeyError, ValueError):
                price = 0.0

            in_stock_raw = row.get("in_stock", "False")
            in_stock = str(in_stock_raw).lower() in ("true", "1", "yes")

            books.append(
                Book(
                    title=row.get("title", "").strip(),
                    price_gbp=price,
                    in_stock=in_stock,
                    stock_text=row.get("stock_text", "").strip(),
                    rating=row.get("rating", "").strip(),
                    product_url=row.get("product_url", "").strip(),
                )
            )
    return books


def print_books(books: List[Book], limit: int = 10) -> None:
    for i, book in enumerate(books[:limit], start=1):
        stock_flag = "[Y]" if book.in_stock else "[N]"
        print(
            f"{i:2d}. {book.title[:60]:60} | £{book.price_gbp:6.2f} | {book.rating:7} | {stock_flag}"
        )
        print(f"    {book.product_url}")
    if not books:
        print("No books to show.")


def show_cheapest_books(books: List[Book], limit: int = 10) -> None:
    print("\n=== Cheapest Books ===")
    sorted_books = sorted(books, key=lambda b: b.price_gbp)
    print_books(sorted_books, limit=limit)


def show_most_expensive_books(books: List[Book], limit: int = 10) -> None:
    print("\n=== Most Expensive Books ===")
    sorted_books = sorted(books, key=lambda b: b.price_gbp, reverse=True)
    print_books(sorted_books, limit=limit)


def show_rating_counts(books: List[Book]) -> None:
    print("\n=== Rating Distribution ===")
    counts = {}
    for b in books:
        rating = b.rating or "Unknown"
        counts[rating] = counts.get(rating, 0) + 1
    for rating, count in sorted(counts.items(), key=lambda x: x[0]):
        print(f"{rating:8}: {count}")


def show_stock_summary(books: List[Book]) -> None:
    print("\n=== Stock Summary ===")
    total = len(books)
    in_stock_count = sum(1 for b in books if b.in_stock)
    out_stock_count = total - in_stock_count
    print(f"Total books      : {total}")
    print(f"In stock         : {in_stock_count}")
    print(f"Out of stock     : {out_stock_count}")


def filter_by_min_rating(books: List[Book]) -> None:
    print("\nAvailable ratings are usually: One, Two, Three, Four, Five, Unknown")
    min_rating = input("Enter minimum rating (e.g. Three, Four, Five): ").strip()
    if not min_rating:
        print("No rating entered. Returning to menu.")
        return

    preferred_order = ["One", "Two", "Three", "Four", "Five"]
    try:
        min_index = preferred_order.index(min_rating)
    except ValueError:
        print(f"Unknown rating: {min_rating}")
        return

    allowed = set(preferred_order[min_index:])
    filtered = [b for b in books if b.rating in allowed]
    print(f"\n=== Books with rating >= {min_rating} ({len(filtered)} found) ===")
    print_books(filtered, limit=20)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Explore scraped books CSV with a simple terminal menu."
    )
    parser.add_argument(
        "-f",
        "--file",
        default="books.csv",
        help="Path to books CSV file (default: books.csv)",
    )
    args = parser.parse_args()

    print(f"[INFO] Loading books from {args.file} ...")
    try:
        books = load_books_from_csv(args.file)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {args.file}")
        return

    if not books:
        print("[WARN] No books loaded.")
        return

    while True:
        print("\n==================== BOOKS EXPLORER ====================")
        print("1) Show 10 cheapest books")
        print("2) Show 10 most expensive books")
        print("3) Show rating distribution")
        print("4) Show stock summary")
        print("5) Show books with minimum rating")
        print("q) Quit")
        choice = input("Select an option: ").strip().lower()

        if choice == "1":
            show_cheapest_books(books)
        elif choice == "2":
            show_most_expensive_books(books)
        elif choice == "3":
            show_rating_counts(books)
        elif choice == "4":
            show_stock_summary(books)
        elif choice == "5":
            filter_by_min_rating(books)
        elif choice == "q":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
