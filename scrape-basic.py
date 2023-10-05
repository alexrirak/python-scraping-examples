from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# set up the driver to control the browser
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=op)

# set up dictionaries to store what we find
products = []  # store name of the product
prices = []  # store price of the product
ratings = []  # store rating of the product

# the URL we want to scrape
url = "https://www.amazon.com/dp/B00NSFBXXW"

# Tell the driver to open the page, then parse it with BeautifulSoup
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