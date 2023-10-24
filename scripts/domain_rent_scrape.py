'''This script scrap the rent property data from domain.com in the Melbourne, VIC region'''
# built-in imports
import re
import random
import json
import csv
import time
from collections import defaultdict

# user packages
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

# initial variable
BASE_URL = "https://www.domain.com.au"
price_range = ['950-any']
all_properties = defaultdict(dict)
failed_properties = [['url', 'error']]

# add price range
cur = 950
while cur > 250:
    price_range.append(f'{cur - 50}-{cur}')
    cur -= 50
price_range.append('0-250')

# init scraper
session = requests.Session()
ua = UserAgent()
session.headers.update({'User-Agent': ua.random})




# indicator of first step
print('First getting the url to each property')
time.sleep(2)

# get properties from listing page for this price range
for item in price_range:    
    # progress check
    print(f'Price range: {item}')
    
    end = False
    page = 1
    url = f'https://www.domain.com.au/rent/?price={item}&sort=price-desc&state=vic&page=1'
    while not end:
        # random delay
        time.sleep(min(random.expovariate(3), 1))
        
        # proress check
        print(f'    +Visiting  page {page}')
        print(f'     Url: {url}')
        page += 1
        

        # get all property links
        
        soup = BeautifulSoup(session.get(url).content, 'lxml')
        property_links = soup \
                                        .find("ul", {"data-testid": "results"}) \
                                        .findAll("a", href=re.compile(f"{BASE_URL}/*"))
      
        for _prop in property_links:
            # get property url and address
            if 'address' in _prop['class']:
                link = _prop['href']
                address_line1 = _prop.find('span', {'data-testid': 'address-line1'})
                
                address_line2 = _prop.find('span', {'data-testid': 'address-line2'})
                suburb = address_line2.find_all('span')[0]
                state = address_line2.find_all('span')[1]
                postcode = address_line2.find_all('span')[2]
                
                try:
                    all_properties[link]['address_line1'] = address_line1.text
                except:
                    all_properties[link]['address_line1'] = None
                try:
                    all_properties[link]['address_line2'] = address_line2.text
                except:
                    all_properties[link]['address_line2'] = None
                try:
                    all_properties[link]['suburb'] = suburb.text 
                except:
                    all_properties[link]['suburb'] = None
                try:
                    all_properties[link]['state'] = state.text
                except:
                    all_properties[link]['state'] = None
                try:
                    all_properties[link]['postcode'] = postcode.text
                except:
                    all_properties[link]['postcode'] = None
    
        # check for next page
        navi = soup.find_all('a', {'data-testid': 'paginator-navigation-button'})
        if len(navi) == 1:
            if 'page=1' == url[-6:]:
                url = BASE_URL + navi[0]['href']
                continue
            else: 
                end = True
        else:
            url = BASE_URL + navi[1]['href']





# indicator of second step
print('Now scraping each property detail')
time.sleep(2)
            
# get the detail of the property to store in the corresponding dict of all_property
property_count = 1
error_count = 0
total_properties = len(all_properties)
for prop in all_properties:
    # random delay
    time.sleep(min(random.expovariate(3), 1))
    
    # progress update
    print(f'Scraping property {property_count}/{total_properties}: {prop}')
    soup = BeautifulSoup(session.get(prop).content, 'lxml')
    
    try:
        # get price
        all_properties[prop]['price'] = soup\
                                                            .find('div', {'data-testid': 'listing-details__summary-title'})\
                                                            .text
                                                            
        # get bond, land area
        strip_content = soup\
                                    .find('div', {'data-testid': 'strip-content-list'})\
                                    .find_all('li')
        for item in strip_content:
            # bond
            if 'Bond' in item.text:
                all_properties[prop]['bond'] = item.strong.text
            # land area
            if 'area' in item.text:
                all_properties[prop]['area'] = item.strong.text
                                                                                                    
                                                                                                
        # get property type
        all_properties[prop]['type'] = soup\
                                                            .find('div', {'data-testid': 'listing-summary-property-type'})\
                                                            .span\
                                                            .text
                                                            
        # get room, bath, parking   
        feature = soup\
                            .find('div', {'data-testid': 'property-features'})\
                            .find_all('span', {'data-testid': 'property-features-text-container'})
        for item in feature:
            if 'Bed' in item.text:
                item.span.extract()
                all_properties[prop]['bed'] = item.text
            if 'Bath' in item.text:
                item.span.extract()
                all_properties[prop]['bath'] = item.text
            if 'Parking' in item.text:
                item.span.extract()
                all_properties[prop]['parking'] = item.text
        
        # get description
        desc = soup\
                        .find('div', {'data-testid': 'listing-details__description'})\
                        .find('div', {'data-testid': 'expander-wrapper'})\
                        .text
        all_properties[prop]['description'] = desc
        
        # successfully scaped
    except Exception as error:
        failed_properties.append([prop, type(error).__name__])
        error_count += 1
        
    property_count += 1

# show result
print(f'Successfully scraped the total of {property_count - error_count} properties')

# save the data
data = json.dumps(all_properties, indent=4)
with open('../data/landing/domain_properties.json', 'w') as f:
    f.write(data)
    print(f'Saved properties data')
# error log
with open('../data/error_log/domain_failed_properties.csv', 'w') as f:
    csv.writer(f).writerows(failed_properties)
    print(f'Saved properties data')