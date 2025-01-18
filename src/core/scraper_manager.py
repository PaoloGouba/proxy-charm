from scrapers.proxy_scrape import ProxyScrape
from scrapers.free_proxy_list import FreeProxyListScraper
from scrapers.proxifly import ProxyFly


class ScraperManager:
    def __init__(self):
        # Registra tutti gli scraper disponibili
        self.scrapers = [
            ProxyScrape(),
            FreeProxyListScraper(),
            ProxyFly(),
        ]

    def run_all_scrapers(self):
        """
        Esegue tutti gli scraper e restituisce un'unica lista di proxy.
        """
        all_proxies = []
        for scraper in self.scrapers:
            print(f"Running scraper: {scraper.name}")
            proxies = scraper.fetch_proxies()
            all_proxies.extend(proxies)
        return all_proxies
