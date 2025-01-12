from scrapers.site1_scraper import Site1Scraper
from scrapers.free_proxy_list import FreeProxyListScraper

class ScraperManager:
    def __init__(self):
        # Registra tutti gli scraper disponibili
        self.scrapers = [
            #Site1Scraper(),
            FreeProxyListScraper(),
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
