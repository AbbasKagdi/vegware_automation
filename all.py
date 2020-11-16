import urllib.request
from selenium import webdriver
import csv 
import random
import pandas as pd
import os

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

    # fetching URLs
    urls = []
    anchors = driver.find_elements_by_xpath('//h3[@class="product__title h6"]/a')
    for anchor in anchors:
        urls.append(anchor.get_attribute('href'))

    print("\n".join(urls))

    # preloop setup
    rows = [[] for _ in range(14)]

    # field names 
    fields = ['SKU', 'Name', 'Description', 'url', 'price', 'case-count', 'items-per-pack', 'packs', 'product-dimensions', 'case-dimensions', 'pallet-count', 'EAN', 'weight', 'pack-weight']

    # creating folder for category
    cur_dir = os.path.join('.', catname)
    os.mkdir(cur_dir)
    print("created folder " + cur_dir)

    # name of csv file 
    filename = catname + ".csv"
    filename = os.path.join(cur_dir, catname)
        
    # initialising csv file
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        
        # writing the fields 
        csvwriter.writerow(fields) 

    # starting loop ------------------------------------------------------------
    for url in urls:
        driver.get(url)

        # download product image with name as SKU
        image = driver.find_element_by_xpath('//div[@class="carousel-item active"]/img')
        image = image.get_attribute('src')

        #finding SKU
        sku = driver.find_element_by_xpath('//span[@class="colorGreen"]').text
        
        # downloading image
        imgpath = sku + ".jpg"
        imgpath = os.path.join(cur_dir, imgpath)
        urllib.request.urlretrieve(image, imgpath)
        print("downloaded image " + sku + ".jpg")

        # fetching data
        name = driver.find_element_by_xpath('//h1[@class="item__name pb-4 pt-md-0 h3"]').text
        desc = driver.find_element_by_xpath('//div[@class="item__description"]').text
        price = random.randint(3, 27)

        #extracting bulk details
        info = [sku, name, desc, url, price]
        details = driver.find_elements_by_xpath('//div[@class="col-7 col-md-9"]')
        for detail in details:
            words = detail.get_attribute('innerHTML')
            words = words.replace('<br>', ' ')
            info.append(words)

        # data rows of csv file 
        rows.append(info)
        
        # writing to csv file 
        with open(filename, 'a') as csvfile: 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile)
            
            # writing the data rows 
            csvwriter.writerows(rows)
            print('CSV file updated! added SKU: '+sku)

    # end of loop --------------------------------------------------------------

    # sanitise csv
    # utf-8 encoding not supported on windows
    # debugging data from https://stackoverflow.com/questions/18039057/python-pandas-error-tokenizing-data
    # remove after usage
    df = pd.read_csv(filename, encoding='cp1252', error_bad_lines=False)
    df.to_csv(filename, index=False)

driver.close()
