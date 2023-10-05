from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# set up the driver to control the browser
op = webdriver.ChromeOptions()

# Uncomment the following line to run in `headless` mode
# op.add_argument('--headless')

driver = webdriver.Chrome(options=op)

# set up dictionaries to store what we find
products = []  # store name of the product
prices = []  # store price of the product
ratings = []  # store rating of the product

# dictionary of URLs we want to scrape
urls = ["https://www.amazon.com/dp/B00NSFBXXW",
        "https://www.amazon.com/dp/B07CP9VTV7",
        "https://www.amazon.com/dp/B07PHVPC8X",
        "https://www.amazon.com/dp/B01M1HB0BN",
        "https://www.amazon.com/dp/B07PHVPC8X",
        "https://www.amazon.com/dp/B004XEDR54",
        "https://www.amazon.com/dp/B07PVKSR5C"]

# Loop through the pages, scrape each, then parse it with BeautifulSoup
for url in urls:

    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    # loop through the HTML elements to extract what we want
    # in this case starting at the `body` and searching all child tags
    for body in soup.findAll('body'):
        # find each HTML tag we want
        name = body.find('span', attrs={'id': 'productTitle'})
        price = body.find('span', attrs={'class': 'a-offscreen'})
        rating = body.find('span', attrs={'class': 'a-icon-alt'})

        # save its value to our dictionaries
        products.append(name.text.strip())
        prices.append(price.text.strip())
        ratings.append(rating.text.strip())

# Format data as a table
df = pd.DataFrame({'Product Name': products, 'Price': prices, 'Rating': ratings})

# Print to screen
print(df.to_string())

# Save to CSV file
df.to_csv('products.csv', index=False, encoding='utf-8')
