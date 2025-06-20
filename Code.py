import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

# Change this to a path accessible in Colab
desktop_path = "/content/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Create the directory if it doesn't exist
os.makedirs(desktop_path, exist_ok=True)


# ---------- 1. Scrape Homepage ----------
homepage_url = "http://books.toscrape.com/"
response = requests.get(homepage_url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

homepage_books = []
books = soup.find_all("article", class_="product_pod")

for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text.strip()
    rating = book.p["class"][1]
    homepage_books.append([title, price, rating])

# Save homepage data to Desktop
with open(desktop_path + "books_homepage.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Rating"])
    writer.writerows(homepage_books)

print("✅ Homepage scraped and saved to Desktop → books_homepage.csv")


# ---------- 2. Scrape All Books (All Pages) ----------
all_books = []

for page in range(1, 51):  # 50 pages
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.strip()
        rating = book.p["class"][1]
        all_books.append([title, price, rating])

    print(f"📄 Page {page}/50 scraped")

# Save all book data to Desktop
with open(desktop_path + "all_books.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Rating"])
    writer.writerows(all_books)

print("✅ All books scraped and saved to Desktop → all_books.csv")

# Optional: Load and preview
df = pd.read_csv(desktop_path + "all_books.csv")
print("\n📚 Sample books from all_books.csv:")
display(df.head())
