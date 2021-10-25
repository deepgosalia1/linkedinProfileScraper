#!/usr/bin/env python

# importing required libraries

import importlib, os
def import_neccessary_modules(modname):
    '''
        Import a Module,
        and if that fails, try to use the Command Window PIP.exe to install it,
        if that fails, because PIP in not in the Path,
        try find the location of PIP.exe and again attempt to install from the Command Window.
    '''
    try:
        # If Module it is already installed, try to Import it
        importlib.import_module(modname)
        print(f"Importing {modname}", end = "\r")
    except ImportError:
        # Error if Module is not installed Yet,  the '\033[93m' is just code to print in certain colors
        print(f"\033[93mSince you don't have the Python Module [{modname}] installed..")
        print("Installing it using Python's PIP.exe command.\033[0m")
        if os.system('PIP --version') == 0:
            # No error from running PIP in the Command Window, therefor PIP.exe is in the %PATH%
            os.system(f'pip install {modname}')
        else:
            # Error, PIP.exe is NOT in the Path!! So I'll try to find it.
            pip_location_attempt_1 = sys.executable.replace("python.exe", "") + "pip.exe"
            pip_location_attempt_2 = sys.executable.replace("python.exe", "") + "scripts\pip.exe"
            if os.path.exists(pip_location_attempt_1):
                # The Attempt #1 File exists!!!
                os.system(pip_location_attempt_1 + " install " + modname)
            elif os.path.exists(pip_location_attempt_2):
                # The Attempt #2 File exists!!!
                os.system(pip_location_attempt_2 + " install " + modname)
            else:
                # Neither Attempts found the PIP.exe file, So i Fail...
                print(f"\033[91mAbort!!!  I can't find PIP.exe program!")
                print(f"You'll need to manually install the Module: {modname} in order for this program to work.")
                print(f"Find the PIP.exe file on your computer and in the CMD Command window...")
                print(f"   in that directory, type    PIP.exe install {modname}\033[0m")
                exit()


import_neccessary_modules('bs4')
import_neccessary_modules('selenium')
import_neccessary_modules('pandas')
import_neccessary_modules('pycountry')
import_neccessary_modules('emoji')

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from csv import DictWriter
import random as rand
from pycountry import countries
import emoji
import re
random = str(rand.randint(-15,100))

df = pd.read_csv(r'inputProfileLinks.csv')
urls = df.iloc[:,0] # profile link column
field_names = ['Name','Location','Postion','Company','Email']


#print('Starting the browser in the background mode...')
print('\033[91m Scraping may reduce the PC speed, preferable to keep it on overnight.')
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = False
driver = webdriver.Chrome("chromedriver.exe", options=options)
driver.get('https://www.linkedin.com')
driver.implicitly_wait(10)
print('Logging you in', end = "\r")
username = driver.find_element_by_xpath('//*[@type="text"]')
username.send_keys('Your log-in Email') # Your log-in Email

password = driver.find_element_by_xpath('//*[@type="password"]')
password.send_keys('Your password') # Your password

log_in_button= driver.find_element_by_xpath('//*[@class="sign-in-form__submit-button"]')
log_in_button.click()
driver.implicitly_wait(1) #driver will wait for 1 second to load everything completely

def cleanText(text):
    print('Found',emoji.emoji_count(text),'emojis in this idiot\'s name. removing emojis...')
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text

def extraction(profileUrl):
    random = str(rand.randint(25,100))
    driver.get(profileUrl)
    driver.implicitly_wait(1)

    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    profile_link = (driver.current_url)

    # personal details    
    name_div = soup.find('div', {'class': 'display-flex justify-space-between pt2'})
    connections_div = soup.find('div',{'class':'pv-deferred-area__content'})

    # name
    try:
        name = cleanText(name_div.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip().replace('"',''))
    except IndexError: # To ignore any kind of error
        name = 'NULL'
    except AttributeError:
        name = 'NULL'
    driver.execute_script("window.scrollBy(0,"+random+");")
    # location
    try:
        locations = name_div.find('span', {'class': 'text-body-small inline t-black--light break-words'}).get_text().strip().split(', ')
        for loc in locations[1:]:
            if loc in countries:
                location = loc
                break
        else: location = ', '.join(x for x in locations)
    except IndexError:
        location = 'NULL'
    except AttributeError:
        location = 'NULL'
    driver.execute_script('window.scrollBy(0,'+random+')')
    # No. of connections            
    try:
        connections = soup.find('span', {'class': 'align-self-center t-14 t-black--light'}).get_text().strip().replace('"','')
    except IndexError:
        connections = 'NULL'
    except AttributeError:
        connections = 'NULL'

    # recent positions
    try:
        job_title = name_div.find('div', {'class': 'text-body-medium break-words'}).get_text().strip().replace('"','')
    except IndexError:
        job_title = 'NULL'
    except AttributeError:
        job_title = 'NULL'
    driver.execute_script('window.scrollBy(0,'+random+')')

    #company name
    try:
        company_name = soup.find('div', {'class': 'inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp'}).get_text().strip().replace('"','')
    except IndexError:
        company_name = 'NULL'
    except AttributeError:
        company_name = 'NULL'

    #email extraction
    contactBTN = driver.find_element_by_xpath('//*[@class="ember-view link-without-visited-state cursor-pointer text-heading-small inline-block break-words"]')
    ActionChains(driver).click(contactBTN).perform()
    time.sleep(5)
    driver.switch_to.default_content
    section = driver.find_element_by_xpath("//div[@class='artdeco-modal__content ember-view']")
    innerSoup = BeautifulSoup(driver.page_source, 'lxml')
    user, email = 'Dummy', 'NONE'
    for j,i in enumerate(innerSoup.find_all('a')):
        if 'mailto:' in i.get('href'):
            email = i.get('href')[7:]
            break
    else: print('\033[91m Sorry, Email is privatized for', name)
    driver.execute_script('window.scrollBy(0,'+random+')')
    time.sleep(rand.randint(5,20))
    # saving outputs
    output = {'Name': name, 'Location': location, 'Postion': job_title, 'Company': company_name, 'Email': email}
    
    return output

with open('scrapedResults.csv', 'a', encoding='utf-8-sig') as f_object:
    dictwriter_object = DictWriter(f_object, fieldnames=field_names)
    for link in urls:
        print('\033[93mCurrently ongoing - ', link, end = "\r")
        extractedRes = extraction(link)
        dictwriter_object.writerow(extractedRes)
    f_object.close()
    print('\n\n\n\033[91m Congrats, all given contacts have been scraped.')
    print('\n\033[93m View the results in a file named, \'scrapedResults.csv\'')
    
driver.close()
