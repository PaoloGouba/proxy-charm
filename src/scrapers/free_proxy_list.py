import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class FreeProxyListScraper(BaseScraper):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "FreeProxyListScraper"

    def fetch_proxies(self):
        """
        Scarica e analizza le proxy da https://free-proxy-list.net/
        """
        url = "https://free-proxy-list.net/"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Solleva un'eccezione per errori HTTP

            # Parsing HTML con BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find("table", {"class": "table table-striped table-bordered"})

            # Verifica se la tabella esiste
            if not table:
                print(f"Errore: Tabella proxy non trovata nella pagina {url}")
                return []

            # Estrai le righe dalla tabella
            rows = table.find_all("tr")[1:]  # Ignora l'intestazione della tabella
            proxies = []
            for row in rows:
                columns = row.find_all("td")
                if len(columns) >= 2:
                    proxy_ip = columns[0].text.strip()
                    proxy_port = columns[1].text.strip()
                    proxies.append({"ip": proxy_ip, "port": proxy_port})
            return proxies

        except requests.RequestException as e:
            print(f"Errore durante il download delle proxy: {e}")
            return []
