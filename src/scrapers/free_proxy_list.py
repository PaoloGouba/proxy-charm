import requests
from bs4 import BeautifulSoup

from base_proxy import BaseProxy
from base_scraper import BaseScraper

#from utils.get_proxy_info import *

PROXY_URL = [
    'https://free-proxy-list.net/'
]

#get proxies from table in https://free-proxy-list.net/

class FreeProxyList(BaseScraper):
    def __init__(self, use_proxy=False):
        super().__init__(use_proxy)

    def get_free_proxy_list(self, url = PROXY_URL[0]):

        response = requests.get(url)

        if response.status_code == 200:

            free_proxy_list = []

            page_content = BeautifulSoup(response.content,'html.parser')
            text_area = page_content.find('textarea')
            items = text_area.text.split('\n')

            for item in items :
                try :
                    my_proxy = item.split(':')
                    proxy_ip = my_proxy[0]
                    try :
                        proxy_port = my_proxy[1]
                    except :
                        proxy_port = 'N/A' 
                    #proxy_location = get_proxy_location(proxy_ip)
                    proxy_location = "get_proxy_location(proxy_ip)"
                    proxy_instance = BaseProxy(proxy_ip, proxy_port, proxy_location)
                    free_proxy_list.append(proxy_instance) 
                except :
                    pass
             

             
                
                #print(free_proxy_list)
            return free_proxy_list
        
        else :
            print("Errore nella richiesta. Codice di stato:", response.status_code)
            
            

scraper = FreeProxyList()

lista = scraper.get_free_proxy_list()
for i in lista :        
    print(i.url)        


"""data = requests.get('https://www.paginegialle.it/ricerca/software/Pordenone')

soup = BeautifulSoup(data.content,'lxml')

print(soup)"""