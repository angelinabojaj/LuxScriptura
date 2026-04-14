import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://bible.usccb.org/bible/"


def _format_reference(reference: str) -> str:
    """
    Converts 'John 3:16' → 'john/3'
    USCCB uses book + chapter pages, not verse-level API.
    """
    reference = reference.lower().strip()

    # Split book from chapter/verse
    match = re.match(r"([a-z\s]+)\s+(\d+)", reference)
    if not match:
        raise ValueError("Use format like 'John 3' or 'Genesis 1' (chapter-based only for USCCB scraping).")

    book = match.group(1).replace(" ", "")
    chapter = match.group(2)

    return f"{book}/{chapter}"


def get_bible_verse(reference: str) -> str:
    """
    Fetches Bible chapter text from USCCB.

    NOTE:
    USCCB is structured by chapter, not individual verse.
    Example: 'John 3' → full chapter 3.
    """

    try:
        path = _format_reference(reference)
        url = BASE_URL + path + "/"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # USCCB stores scripture in divs with class "content-body" or similar
        content_div = soup.find("div", class_="content-body")

        if not content_div:
            return "Could not locate scripture text on USCCB page."

        # Extract readable paragraphs
        paragraphs = content_div.find_all("p")
        text = "\n".join(p.get_text(strip=True) for p in paragraphs)

        return text.strip() if text else "No text found."

    except Exception as e:
        return f"Error fetching USCCB scripture: {str(e)}"


# =========================================================
# Example usage
# =========================================================
if __name__ == "__main__":
    print(get_bible_verse("John 3"))