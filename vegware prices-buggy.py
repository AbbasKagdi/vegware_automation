from selenium import webdriver
import csv
import pandas as pd
import os
import time
import itertools 

# start counter
start_time = time.time()

driver = webdriver.Firefox()
# fetch all categories
driver.get("https://www.vegware.com/uk/catalogue/")

caturls = []
catanchors = driver.find_elements_by_xpath('//a[@class="catBox shadow"]')
for anchor in catanchors:
    caturls.append(anchor.get_attribute('href'))

catnames = []
texts = driver.find_elements_by_xpath('//div[@class="catBox__title"]')
for text in texts:
    catnames.append(text.get_attribute('innerHTML'))

# delete home essentials and delivery
#del caturls[:2]
#del catnames[:2]

# preloop setup
rows = [[] for _ in range(8)]
header = []
skus = []
urls = []
names = []
categories = [] # not the most efficient way to do it
case_price = []
pack_price = []
case_count = []
pack_count = []
cp_price = []
cp_count = []
pp_price = []
pp_count = []

# field names 
fields = ["SKU", "Name", "category", "case price", "case count", "pack price", "pack count", "url"]
header.append(fields)
filename = os.path.join(".", "vegware_sales_excercise", "vegware-prices-new.csv")

with open(filename, 'w+') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)
    
    # writing the header
    csvwriter.writerows(header)

# category loop
for catname,caturl in zip(catnames, caturls):
    driver.get(caturl)
    print("\n\n --- Scraping category: ", catname, " --- \n\n")

    # fetching URLs and names
    name_anchors = driver.find_elements_by_xpath('//h3[@class="product__title h6"]/a')
    for anchor in name_anchors:
        urls.append(anchor.get_attribute('href'))
        names.append(anchor.text)
        categories.append(catname)

    # sku
    sku_anchors = driver.find_elements_by_xpath('//div[@class="product__sku"]/a')
    for sku in sku_anchors:
        skus.append(sku.text)
        print("\n Added sku: ",sku.text)

    price_count_anchors = driver.find_elements_by_xpath('//div[@class="pricing pricing--list"]')
    for elems in price_count_anchors:
        cp_price = elems.find_element_by_xpath("(//span[@class='pricing__price'])")
        case_price.append(cp_price.text.strip("Â"))
        cp_count = elems.find_element_by_xpath("(//span[@class='pricing__type'])")
        case_count.append(cp_count.text)
        try:
            pp_price = elems.find_element_by_xpath("(//div[@class='catAdditionalInfo']/span/span[@class='pricing__price'])")
            pack_price.append(pp_price.text.text.strip("Â"))
            pp_count = elems.find_element_by_xpath("(//div[@class='catAdditionalInfo']/span/span[@class='pricing__type'])")
            pack_count.append(pp_count.text)
        except:
            pack_price.append("empty")
            pack_count.append("empty")

    """
    cp_price = [x for x in cp_price]
    case_price.append(cp_price)
    cp_count = [y for y in cp_count]
    case_count.append(cp_count)
    pp_price = [p.strip("Â") for p in pp_price]
    pack_price.append(pp_price)
    pp_count = [q for q in pp_count]
    pack_count.append(pp_count)

    counter = 0

    for x,y,p,q in zip(cp_price, cp_count, pp_price, pp_count):
        if y[0:6] == "/Case ":
            case_price.append(x.strip("Â"))
            case_count.append(y.strip("/Case "))
            counter = 1
        if y[0:6] == "/Pack ":
            pack_price.append(x.strip("Â"))
            pack_count.append(y.strip("/Pack "))
            counter = 0
        elif counter > 0:
            pack_price.append("empty")
            pack_count.append("empty")

    
    # price
    price_anchors = driver.find_elements_by_xpath('//span[@class="pricing__price"]')
    for price in price_anchors:
        # filter out utf-8 Â£ symbol error .strip("Â")
        case_price.append(price.get_attribute('innerHTML'))
        #try:
        #    pack_price.append(real_price.span[2].string)
        #except:
        #    pack_price.append("NA")

    # price type
    item_count_anchors = driver.find_elements_by_xpath('//span[@class="pricing__type"]')
    for count in item_count_anchors:
        # substring assuming fetching only case count
        case_count.append(count.get_attribute('innerHTML'))
        #try:
        #    pack_count.append(real_count.span[2].string)
        #except:
        #    pack_count.append("NA")
    """
    # ------------------------------- end of loop -------------------------------
    break

for (s, n, c, cp, cc, pp, pc, u) in itertools.zip_longest(skus, names, categories, case_price, case_count, pack_price, pack_count, urls, fillvalue="Blank"):
    info = [s, n, c, cp, cc, pp, pc, u]
    
    # data rows of csv file 
    rows.append(info)
    print(info)

# writing to csv file 
with open(filename, 'a+') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)
    
    # writing the data rows 
    csvwriter.writerows(rows)

# sanitise csv
# utf-8 encoding not supported on windows
# debugging data from https://stackoverflow.com/questions/18039057/python-pandas-error-tokenizing-data
# remove after usage
df = pd.read_csv(filename, encoding='cp1252', error_bad_lines=False)
# experimental
df.drop_duplicates(subset='SKU')
df.to_csv(filename, index=False)

driver.close()
# record execution time
print("\n--- finsihed in %s seconds ---" % (time.time() - start_time))