from bs4 import BeautifulSoup
import requests

base_link = 'https://www.colorcapital.in/'
product_link = 'collections/women-dresses-1'

get_html = requests.get(base_link + product_link).text
soup = BeautifulSoup(get_html, 'lxml')
products = soup.find_all('li', class_='grid__item scroll-trigger animate--slide-in')

product_pages = []

for product in products:
    product_pages.append(product.find('a')['href'])

# print(product_pages)

count = 0

# scrapping the product pages
product_prices = []
product_names = []
sizes = []
product_sizes = []


def clean_tag(tag):
    tag = tag.text.strip().replace('Rs.','').replace(',','').strip()
    return float(tag)

def get_prices(regular_price,sale_price):
    regular_price = clean_tag(regular_price)
    sale_price = clean_tag(sale_price)
    product_prices.append([regular_price, sale_price])

# turns out the bug was a feature lol
# def get_names(name):
#     count = 0
#     for product in product_names:
#         if product.lower() == name.lower():
#             count += 1
#     if count == 0:
#         product_names.append(name)
    

for product_page in product_pages:
    product_page_html = requests.get(base_link + product_page).text
    soup = BeautifulSoup(product_page_html, 'lxml')

    #getting prices
    regular_price = soup.find('span', class_='price-item price-item--regular')
    sale_price = soup.find('span', class_='price-item price-item--sale price-item--last')
    get_prices(regular_price,sale_price)

    #getting name
    product_name = soup.find('div', class_='product__title').text.strip().splitlines()[0]
    product_names.append(product_name)

    #getting sizes
    i=0
    while True:
        try:
            label = soup.find('label', for_='template--19401590440153__main-1-' + str(i))
            if label is None:
                break  # Exit loop if no more labels found
            sizes.append(label.text.strip())
            i += 1
        except Exception as e:
            print("Error occurred:", e)
            break

# print(product_prices)
# print(product_names)

for names in product_names:
    print(names,'costs Rs.',product_prices[count][0])
    count += 1
    
count = 0

print(product_sizes)
print(len(product_names))
print(len(product_prices))
