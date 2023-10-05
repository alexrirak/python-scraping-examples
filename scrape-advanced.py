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
productIds = []  # store name of the product
prices = []  # store price of the product
ratings = []  # store rating of the product

# the URL we want to scrape
url = "https://www.amazon.com/s?k=CLIF+BAR"

# Tell the driver to open the page, then parse it with BeautifulSoup
driver.get(url)
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

# loop through the HTML elements to extract what we want
# in this case finding a specific type of 'div' and searching all child tags
for div in soup.findAll('div', attrs={'data-component-type': 's-search-result'}):

    # find each HTML tag we want
    name = div.find('span', attrs={'class': 'a-size-base-plus'})
    price = div.find('span', attrs={'class': 'a-offscreen'})
    rating = div.find('span', attrs={'class': 'a-icon-alt'})
    productId = div["data-asin"]

    # if all the values are defined
    if name and price and rating and productId:
        # save values to our dictionaries
        products.append(name.text.strip())
        prices.append(float(price.text.strip()[1:]))
        ratings.append(float(rating.text.strip()[:3]))
        productIds.append(productId.strip())

# Format data as a table
df = pd.DataFrame({'Product Name': products, 'Product Id': productIds, 'Price': prices, 'Rating': ratings})

# Sort data by price
df = df.sort_values(by=['Price'], ascending=False)

# Print to screen
print(df.to_string())

# Save to CSV file
df.to_csv('products.csv', index=False, encoding='utf-8')
