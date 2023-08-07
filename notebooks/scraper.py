from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

options = Options()
options.headless = True

# sacar o numero total de paginas

url = 'https://www.era.pt/comprar?ob=1&tp=1,2&page=1&ord=3'
driver = Chrome(options=options)
driver.get(url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

num = soup.find(attrs={'class':'btn-page btn-page-lg'}).text
num = int(num)
page_nums = range(1, num+1)



# dados em cada página 
driver = Chrome(options=options)

dict_list = []

pbar = tqdm(page_nums) 

for page in pbar:
    url = f'https://www.era.pt/comprar?ob=1&tp=1,2&page={page}&ord=3'
    
    driver.get(url)
    time.sleep(3.5)

    site = BeautifulSoup(driver.page_source, 'html.parser')



    for info in site.find_all('div', attrs={'class':'info'}):
        dict = {}
        
        # price = info.find('p', attrs={'class':'price-value'})
        try:
            price = info.find('p', attrs={'class':'price-value'}).string.replace('€', '').strip()
        except:
            price = None

        location = info.find('div', attrs={'class':'col-12 location'}).string
        
        dict['Preço'] = price
        dict['Localização'] = location

        details = info.find_all('div', attrs={'class':'detail d-inline-flex mr-2'})
        for i in range(len(details)):
            var_name = info.find_all('div', attrs={'class':'detail d-inline-flex mr-2'})[i].svg['data-original-title']
            var = info.find_all('div', attrs={'class':'detail d-inline-flex mr-2'})[i].text
            dict[var_name] = var

        dict_list.append(dict)

    pbar.set_description(f'Page: {page}')
    
    

driver.quit()

pd.DataFrame(dict_list).to_csv('../data/House_prices_23.csv')


