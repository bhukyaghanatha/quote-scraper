import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

URL = "https://quotes.toscrape.com/"

def fetch_quotes():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("Error fetching page:", e)
        return None

def parse_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes_data = []

    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()

        quotes_data.append((text, author))

    return quotes_data

def save_to_file(quotes):
    if not os.path.exists("output"):
        os.makedirs("output")

    file_path = "output/quotes.txt"

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Quotes Scraped On: {current_time}\n")
        file.write("=" * 50 + "\n\n")

        for index, (text, author) in enumerate(quotes, start=1):
            file.write(f"{index}. {text}\n")
            file.write(f"   — {author}\n\n")

    print("Quotes saved successfully with timestamp.")

def main():
    html = fetch_quotes()
    if html:
        quotes = parse_quotes(html)
        save_to_file(quotes)

if __name__ == "__main__":
    main()
