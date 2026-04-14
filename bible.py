import requests
from bs4 import BeautifulSoup
import re
from functools import lru_cache

BASE_URL = "https://bible.usccb.org/bible/"

# Basic normalization map (expand as needed)
BOOK_MAP = {
    "genesis": "genesis",
    "exodus": "exodus",
    "matthew": "matthew",
    "mark": "mark",
    "luke": "luke",
    "john": "john",
    "1 john": "1john",
    "2 john": "2john",
    "3 john": "3john",
    "romans": "romans",
}


def _format_reference(reference: str) -> str:
    reference = reference.lower().strip()

    match = re.match(r"([1-3]?\s*[a-z\s]+)\s+(\d+)", reference)
    if not match:
        raise ValueError("Use format like 'John 3' or '1 John 4'.")

    book = match.group(1).strip()
    chapter = match.group(2)

    book_key = BOOK_MAP.get(book)
    if not book_key:
        # fallback: remove spaces
        book_key = book.replace(" ", "")

    return f"{book_key}/{chapter}"


def get_bible_verse(reference: str) -> str:
    try:
        path = _format_reference(reference)
        url = BASE_URL + path

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Try multiple fallback selectors
        content = (
            soup.find("div", class_="content-body")
            or soup.find("div", class_="content-area")
            or soup.find("article")
        )

        if not content:
            return "Could not locate scripture text."

        verses = content.find_all(["p", "span"])

        text = "\n".join(v.get_text(" ", strip=True) for v in verses)

        # Clean empty lines
        text = "\n".join(line for line in text.split("\n") if line.strip())

        return text.strip() or "No text found."

    except Exception as e:
        return f"Error fetching scripture: {e}"


if __name__ == "__main__":
    print(get_bible_verse("John 3"))