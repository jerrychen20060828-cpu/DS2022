#!/usr/bin/env python3
"""Print a bookstore inventory report from MongoDB Atlas."""

import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

AUTHOR_IDS = ["author_002", "author_003", "author_004"]
LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Connect to Atlas and print each selected author's linked books."""
    client = None
    try:
        # Fail with a useful message instead of passing missing credentials to Atlas.
        credentials = {
            "MONGODB_ATLAS_URL": MONGODB_ATLAS_URL,
            "MONGODB_ATLAS_USER": MONGODB_ATLAS_USER,
            "MONGODB_ATLAS_PWD": MONGODB_ATLAS_PWD,
        }
        missing = [name for name, value in credentials.items() if not value]
        if missing:
            raise RuntimeError(
                "Missing MongoDB environment variables: " + ", ".join(missing)
            )

        LOGGER.info("Connecting to MongoDB Atlas")
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )
        client.admin.command("ping")
        LOGGER.info("Connected to MongoDB Atlas")

        # Use the same database and collections populated by bookstore.js.
        database = client["bookstore"]
        authors = database["authors"]
        books = database["books"]

        author_count = authors.count_documents({"_id": {"$in": AUTHOR_IDS}})
        print(f"Authors: {author_count}")

        # Query by each author id so co-authored books appear under every author.
        for author_id in AUTHOR_IDS:
            author = authors.find_one({"_id": author_id})
            if author is None:
                LOGGER.warning("Author %s was not found", author_id)
                continue

            print(f"\n{author['name']}")
            linked_books = books.find({"author_ids": author_id}).sort(
                [("published_year", 1), ("title", 1)]
            )
            for book in linked_books:
                print(f"  {book['title']} ({book['published_year']})")
    except (PyMongoError, RuntimeError):
        LOGGER.exception("Unable to generate the bookstore report")
        raise
    finally:
        if client is not None:
            client.close()
            LOGGER.info("MongoDB connection closed")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    main()
