import requests
from scrapers.base_scraper import BaseScraper

class Site1Scraper(BaseScraper):
    @property
    def name(self):
        return "Site1Scraper"

    def fetch_proxies(self):
        url = "https://example.com/proxies.txt"
        response = requests.get(url)
        raw_proxies = response.text.splitlines()
        proxies = [{"ip": proxy.split(":")[0], "port": proxy.split(":")[1]} for proxy in raw_proxies]
        return proxies
