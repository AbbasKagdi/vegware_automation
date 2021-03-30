from selenium import webdriver
import csv
import pandas as pd
import re
import os

skus = [
'10201',
'10206',
'10205',
'10204',
'10202',
'10203',
'10301',
'10302',
'10303',
'10306',
'10305',
'10304',
'10501',
'10502',
'10506',
'10505',
'10504',
'10207',
'10307',
'20101',
'20111',
'20102',
'20112',
'20103',
'20113',
'20201',
'20202',
'20203',
'20204',
'20205',
'11023',
'11022',
'11011',
'11004',
'11024',
'11003',
'11002',
'11012',
'11001',
'11202',
'11201',
'11026',
'11013',
'11014',
'11016',
'12011',
'12002',
'12012',
'12004',
'12014',
'12003',
'12013',
'12023',
'12005',
'12015',
'12007',
'12017',
'12027',
'13011',
'13012',
'13017',
'14003',
'14002',
'14001',
'14005',
'14006',
'14007',
'14008',
'15001',
'15002',
'15003',
'15004',
'50021',
'50011',
'50001',
'50022',
'50012',
'50002',
'50023',
'50013',
'50003',
'50024',
'50014',
'50004',
'50025',
'50005',
'50015',
'50026',
'50016',
'50006',
'30001',
'30002',
'30006',
'30003',
'30004',
'30005',
'30013',
'30011',
'30012',
'30030',
'30031',
'40002',
'40001',
'40003',
'40004',
'40012',
'40011',
'40013',
'40014',
'40021',
'40023',
'40022',
'40024'

]


urls = [

'https://www.cookplay.eu/product-page/jomon-mini-white',
'https://www.cookplay.eu/product-page/jomon-mini-black',
'https://www.cookplay.eu/product-page/jomon-mini-silver',
'https://www.cookplay.eu/product-page/jomon-mini-gold',
'https://www.cookplay.eu/product-page/jomon-mini-blue',
'https://www.cookplay.eu/product-page/jomon-mini-green',
'https://www.cookplay.eu/product-page/jomon-s-white',
'https://www.cookplay.eu/product-page/jomon-s-blue',
'https://www.cookplay.eu/product-page/jomon-s-green',
'https://www.cookplay.eu/product-page/jomon-s-black',
'https://www.cookplay.eu/product-page/jomon-s-silver',
'https://www.cookplay.eu/product-page/jomon-s-gold',
'https://www.cookplay.eu/product-page/jomon-l-white',
'https://www.cookplay.eu/product-page/jomon-l-blue',
'https://www.cookplay.eu/product-page/jomon-l-black',
'https://www.cookplay.eu/product-page/jomon-l-silver',
'https://www.cookplay.eu/product-page/jomon-l-gold',
'https://www.cookplay.eu/product-page/jomon-mini-beltz',
'https://www.cookplay.eu/product-page/jomon-s-beltz',
'https://www.cookplay.eu/product-page/jo-1-glazed',
'https://www.cookplay.eu/product-page/jo-1-matt',
'https://www.cookplay.eu/product-page/jo-2-glazed',
'https://www.cookplay.eu/product-page/jo-2-matt',
'https://www.cookplay.eu/product-page/jo-plate-glazed',
'https://www.cookplay.eu/product-page/jo-plate-matt',
'https://www.cookplay.eu/product-page/jo-1-bamboo',
'https://www.cookplay.eu/product-page/jo-2-bamboo',
'https://www.cookplay.eu/product-page/jo-5-bamboo',
'https://www.cookplay.eu/product-page/jo-8-bamboo',
'https://www.cookplay.eu/product-page/jo-12-bamboo',
'https://www.cookplay.eu/product-page/yayoi-deep-6u-1',
'https://www.cookplay.eu/product-page/yayoi-side-6u-1',
'https://www.cookplay.eu/product-page/yayoi-appetizer-6u',
'https://www.cookplay.eu/product-page/yayoi-flat-6u',
'https://www.cookplay.eu/product-page/yayoi-flat-6u-1',
'https://www.cookplay.eu/product-page/yayoi-deep-6u',
'https://www.cookplay.eu/product-page/yayoi-side-6u',
'https://www.cookplay.eu/product-page/yayoi-side-6u',
'https://www.cookplay.eu/product-page/yayoi-appetizer-6u',
'https://www.cookplay.eu/product-page/yayoi-big-tray',
'https://www.cookplay.eu/product-page/yayoi-small-tray',
'https://www.cookplay.eu/product-page/yayoi-superflat-black-4u',
'https://www.cookplay.eu/product-page/yayoi-deep-matt-by-willie-marquez-6u',
'https://www.cookplay.eu/product-page/yayoi-flat-matt-by-willie-marquez-6u',
'https://www.cookplay.eu/product-page/yayoi-superflat-matt-by-willie-marquez-4u',
'https://www.cookplay.eu/product-page/shell-dinner-2-u',
'https://www.cookplay.eu/product-page/shell-deep-2-u',
'https://www.cookplay.eu/product-page/shell-deep-2-u',
'https://www.cookplay.eu/product-page/shell-dessert-2-u',
'https://www.cookplay.eu/product-page/shell-dessert-2-u',
'https://www.cookplay.eu/product-page/shell-bowl-2-u',
'https://www.cookplay.eu/product-page/shell-bowl-2-u',
'https://www.cookplay.eu/product-page/shell-salad-bowl-black',
'https://www.cookplay.eu/product-page/shell-line-ramen-bowl-2u',
'https://www.cookplay.eu/product-page/shell-line-ramen-bowl-2u',
'https://www.cookplay.eu/product-page/shell-line-ice-cream-bowl-2u',
'https://www.cookplay.eu/product-page/shell-line-ice-cream-bowl-2u',
'https://www.cookplay.eu/product-page/shell-line-ice-cream-bowl-black-2u',
'https://www.cookplay.eu/product-page/fly-60-set',
'https://www.cookplay.eu/product-page/fly-140-set',
'https://www.cookplay.eu/product-page/fly-jug',
'https://www.cookplay.eu/product-page/the-nest',
'https://www.cookplay.eu/product-page/the-pot',
'https://www.cookplay.eu/product-page/the-tablet-base',
'https://www.cookplay.eu/product-page/the-board',
'https://www.cookplay.eu/product-page/the-saucer',
'https://www.cookplay.eu/product-page/the-plate',
'https://www.cookplay.eu/product-page/the-platter',
'https://www.cookplay.eu/product-page/gochi-baby',
'https://www.cookplay.eu/product-page/gochi-girl',
'https://www.cookplay.eu/product-page/gochi-dad',
'https://www.cookplay.eu/product-page/shell-dinner-by-willie-marquez-2u',
'https://www.cookplay.eu/product-page/naoto-side-white-12u',
'https://www.cookplay.eu/product-page/naoto-side-dark-grey-12u',
'https://www.cookplay.eu/product-page/naoto-side-blanco-12u',
'https://www.cookplay.eu/product-page/naoto-bowl-ice-blue',
'https://www.cookplay.eu/product-page/naoto-bowl-dark-gray-6u',
'https://www.cookplay.eu/product-page/naoto-bowl-white-6u',
'https://www.cookplay.eu/product-page/naoto-plate-17-cm-ice-blue',
'https://www.cookplay.eu/product-page/naoto-plate-17-dark-gray-6u',
'https://www.cookplay.eu/product-page/naoto-plate-17-white-6u',
'https://www.cookplay.eu/product-page/naoto-deep-ice-blue-4u',
'https://www.cookplay.eu/product-page/naoto-deep-dark-gray-4u',
'https://www.cookplay.eu/product-page/naoto-deep-white-4u',
'https://www.cookplay.eu/product-page/naoto-plate-25-cm-ice-blue-6u',
'https://www.cookplay.eu/product-page/naoto-plate-25-cm-white-6u',
'https://www.cookplay.eu/product-page/naoto-plate-25-cm-dark-gray-6u',
'https://www.cookplay.eu/product-page/naoto-plate-29-cm-ice-blue-4u',
'https://www.cookplay.eu/product-page/naoto-plate-29-cm-dark-gray-4u',
'https://www.cookplay.eu/product-page/naoto-plate-29-cm-white-4u',
'https://www.cookplay.eu/product-page/eko-jomon-supermini-25u',
'https://www.cookplay.eu/product-page/eko-jomon-medium-15u',
'https://www.cookplay.eu/product-page/eko-nest-15-units',
'https://www.cookplay.eu/product-page/eko-yayoi-side-15',
'https://www.cookplay.eu/product-page/eko-yayoi-flat-15u',
'https://www.cookplay.eu/product-page/eko-fly-15u',
'https://www.cookplay.eu/product-page/eko-nest-15u',
'https://www.cookplay.eu/product-page/eko-bowl-1400-ml',
'https://www.cookplay.eu/product-page/eko-bowl-1000-ml',
'https://www.cookplay.eu/product-page/eko-side',
'https://www.cookplay.eu/product-page/eko-burger',
'https://www.cookplay.eu/product-page/eko-spoon-white-50-units-1',
'https://www.cookplay.eu/product-page/eko-fork-white-50-units-1',
'https://www.cookplay.eu/product-page/eko-knife-white-50-units-1',
'https://www.cookplay.eu/product-page/eko-coffee-spoon-white-50-units-1',
'https://www.cookplay.eu/product-page/eko-spoon-black-50-units-1',
'https://www.cookplay.eu/product-page/eko-fork-black-50-units-1',
'https://www.cookplay.eu/product-page/eko-knife-black-50-units-1',
'https://www.cookplay.eu/product-page/eko-coffee-spoon-black-50-units-1',
'https://www.cookplay.eu/product-page/eko-set-1-white-fork-knife-spoon-and-napkin-50-units-1',
'https://www.cookplay.eu/product-page/eko-set-2-white-fork-knife-and-napkin-50-units-1',
'https://www.cookplay.eu/product-page/eko-set-1-black-fork-knife-spoon-and-napkin-50-units-1',
'https://www.cookplay.eu/product-page/eko-set-2-black-fork-knife-and-napkin-50-units-1'

]


driver = webdriver.Firefox()

# preloop setup
rows = [[] for _ in range(5)]

# field names 
fields = ['SKU', 'Name', 'Description', 'url', 'price']

# initialising csv file
filename = os.path.join(".", "cookplay", "cookplay.csv")
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
    
    # writing the fields 
    csvwriter.writerow(fields)

# category loop
for sku, url in zip(skus, urls):
    driver.get(url)

    # fetching data
    name = driver.find_element_by_xpath('//h1').text
    desc = driver.find_element_by_xpath('//pre[@class="_28cEs"]').text
    price = driver.find_element_by_xpath('//*[@id="TPAMultiSection_jckc8mzf"]/div/div/article/div[1]/div/article/section[2]/div[2]/div/div/div/span[1]').text
    
    """price = price.strip('€')
    price = price.strip("'")
    price = price.strip('"')
"""
    #extracting bulk details
    info = [sku, name, desc, url, price]

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