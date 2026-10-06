"""Load authors.json and quotes.json into MongoDB.

Run from the project root:  python -m part1.seed
Re-running is safe: both collections are recreated from the files.
"""
import json
from pathlib import Path

from config import connect_db
from part1.models import Author, Quote

DATA_DIR = Path(__file__).parent / "data"


def read_json(name: str) -> list[dict]:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def seed_authors() -> dict[str, Author]:
    Author.drop_collection()
    authors = {}
    for item in read_json("authors.json"):
        authors[item["fullname"]] = Author(**item).save()
    return authors


def seed_quotes(authors: dict[str, Author]) -> int:
    Quote.drop_collection()
    count = 0
    for item in read_json("quotes.json"):
        author = authors.get(item["author"])
        if author is None:
            print(f"Skipped quote: unknown author {item['author']!r}")
            continue
        Quote(tags=item["tags"], author=author, quote=item["quote"]).save()
        count += 1
    return count


def main():
    connect_db()
    authors = seed_authors()
    quotes_count = seed_quotes(authors)
    print(f"Loaded {len(authors)} authors and {quotes_count} quotes.")


if __name__ == "__main__":
    main()
