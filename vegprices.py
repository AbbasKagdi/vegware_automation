from selenium import webdriver
import csv 
import random
import pandas as pd
import os
import time
from itertools import zip_longest

# preloop setup
rows = [[] for _ in range(5)]

# field names 
fields = ['SKU', 'Name', 'url', 'category', 'retail']

# arrays
skus = []
names = []
urls = []
categories = []
retails = []
#case_prices = []
#case_counts = []
#pack_prices = []
#pack_counts = []

# name of csv file 
filename = os.path.join(".", "main.csv")

# initialising csv file
with open(filename, 'w+') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
    
    # writing the fields 
    csvwriter.writerow(fields) 

# starting counter
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


# category loop
for catname,caturl in zip(catnames, caturls):
    driver.get(caturl)

    print("----------------- opened category: ", catname, "-----------------\n")

    # fetching URLs, names, and categories
    urls = []
    anchors = driver.find_elements_by_xpath('//h3[@class="product__title h6"]/a')
    for anchor in anchors:
        urls.append(anchor.get_attribute('href'))
        names.append(anchor.text)
        categories.append(catname)

    # fetching skus
    codes = driver.find_elements_by_xpath('//div[@class="product__sku"]/a')
    for code in codes:
        skus.append(code.text)
        print("added product: ", code.text, " \n")

    # fetching prices and counts
    retailed = driver.find_elements_by_xpath('//div[@class="pricing pricing--list"]')
    for retail in retailed:
        retails.append(retail.get_attribute('innerHTML'))

    # end of loop --------------------------------------------------------------

print("Done fetching products.\nCreating CSV file.\n")

# soup
for sku, name, url, category, ret in zip_longest(skus, names, urls, categories, retails):
    info = [sku, name, url, category, ret]
    rows.append(info)

with open(filename, 'a') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)
    
    # writing the data rows 
    csvwriter.writerows(rows)

# sanitise csv
# utf-8 encoding not supported on windows
# debugging data from https://stackoverflow.com/questions/18039057/python-pandas-error-tokenizing-data
# remove after usage
df = pd.read_csv(filename, encoding='cp1252', error_bad_lines=False)
df.to_csv(filename, index=False)

print("Operation completed in %s seconds" % (time.time() - start_time))
driver.close()