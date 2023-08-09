import requests
import time

class BaseScraper:
    def __init__(self, use_proxy=False):
        self.use_proxy = use_proxy

    def make_request(self, url, user_agent=None):
        headers = {'User-Agent': user_agent} if user_agent else {}
        
        if self.use_proxy:
            # Codice per gestire le richieste con proxy
            pass
        else:
            # Aggiungi un ritardo tra le richieste
            time.sleep(1)  # Ritardo di 1 secondo tra le richieste
            
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Solleva un'eccezione se la richiesta non ha successo
                return response.content
            except requests.exceptions.RequestException as e:
                print(f"Errore durante la richiesta: {e}")
                return None

