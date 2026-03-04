import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

URL = "https://quotes.toscrape.com/"

def create_session():
    session = requests.Session()

    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )

    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    return session


def fetch_quotes(session):
    try:
        response = session.get(URL, timeout=10)
        response.raise_for_status()
        print("Connected successfully. Status:", response.status_code)
        return response.text

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect. Your network or environment is blocking requests.")
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
    except requests.exceptions.RequestException as e:
        print("Unexpected error:", e)

    return None


def parse_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes_data = []

    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        text_tag = quote.find("span", class_="text")
        author_tag = quote.find("small", class_="author")

        if text_tag and author_tag:
            text = text_tag.get_text(strip=True)
            author = author_tag.get_text(strip=True)
            quotes_data.append((text, author))

    return quotes_data


def save_to_file(quotes):
    if not quotes:
        print("No quotes found to save.")
        return

    os.makedirs("output", exist_ok=True)
    file_path = "output/quotes.txt"

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Quotes Scraped On: {current_time}\n")
        file.write("=" * 50 + "\n\n")

        for index, (text, author) in enumerate(quotes, start=1):
            file.write(f"{index}. {text}\n")
            file.write(f"   — {author}\n\n")

    print(f"Saved {len(quotes)} quotes to {file_path}")


def main():
    session = create_session()
    html = fetch_quotes(session)

    if html:
        quotes = parse_quotes(html)
        save_to_file(quotes)
    else:
        print("Failed to retrieve HTML content.")


if __name__ == "__main__":
    main()
