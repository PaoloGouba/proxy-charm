import requests
from scrapers.base_scraper import BaseScraper

class ProxyScrape(BaseScraper):
    @property
    def name(self):
        return "ProxyScrape"

    def fetch_proxies(self):
        url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Solleva un'eccezione per errori HTTP
            raw_proxies = response.text.splitlines()

            proxies = []
            for raw_proxy in raw_proxies:
                try:
                    # Verifica il formato protocol://ip:port
                    protocol, ip_port = raw_proxy.split("://")
                    ip, port = ip_port.split(":")
                    
                    # Aggiungi la proxy se il formato è valido
                    proxies.append({"protocol": protocol, "ip": ip, "port": port})
                except ValueError:
                    # Ignora proxy con formato errato
                    print(f"Formato errato: {raw_proxy}")
                    continue

            return proxies

        except requests.RequestException as e:
            print(f"Errore durante il download delle proxy: {e}")
            return []
