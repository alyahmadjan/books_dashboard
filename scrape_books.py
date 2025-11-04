import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin
import time

base_url = "https://books.toscrape.com/catalogue/page-{}.html"
main_site = "https://books.toscrape.com/"

books = []

# Convert rating words to numbers
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def clean_price(price_str):
    """
    Clean price string by removing non-ASCII characters and currency symbols
    """
    try:
        # Remove non-ASCII characters and whitespace
        price_str = price_str.encode('utf-8', 'ignore').decode('utf-8').strip()
        # Remove currency symbols and any remaining non-numeric characters except decimal point
        price_str = re.sub(r'[^0-9.]', '', price_str)
        # Convert to float
        return float(price_str)
    except (ValueError, AttributeError):
        print(f"⚠️ Warning: Could not convert price '{price_str}' to float. Setting to 0.0")
        return 0.0

for page in range(1, 51):  # There are 50 pages total
    try:
        url = base_url.format(page)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        book_elements = soup.select(".product_pod")
        
        print(f"Scraping page {page} ... ({len(book_elements)} books found)")
        
        for book in book_elements:
            try:
                # Extract basic info
                title = book.h3.a['title']
                price_raw = book.select_one(".price_color").text.strip()
                price = clean_price(price_raw)
                
                rating_word = book.p['class'][1]
                rating = rating_map.get(rating_word, None)
                
                availability = book.select_one(".availability").text.strip()
                
                # Get the link to the book detail page
                detail_link = urljoin(main_site + "catalogue/", book.h3.a['href'])
                
                # Visit the detail page
                detail_res = requests.get(detail_link, timeout=10)
                detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
                
                # Extract category
                breadcrumb = detail_soup.select("ul.breadcrumb li a")
                category = breadcrumb[2].text if len(breadcrumb) > 2 else "Unknown"
                
                # Extract product description (if available)
                desc = detail_soup.select_one("#product_description")
                description = desc.find_next("p").text.strip() if desc else "No description available"
                
                books.append({
                    "Title": title,
                    "Price (£)": price,
                    "Rating": rating,
                    "Availability": availability,
                    "Category": category,
                    "Description": description
                })
                
            except Exception as e:
                print(f"⚠️ Error processing book on page {page}: {str(e)}")
                continue
        
        # Add delay to be respectful to the server
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Error scraping page {page}: {str(e)}")
        continue

# Convert to DataFrame
df = pd.DataFrame(books)

# Save to CSV
df.to_csv("books_data.csv", index=False, encoding="utf-8-sig")

print(f"\n✅ Successfully scraped {len(df)} books and saved to books_data.csv")
