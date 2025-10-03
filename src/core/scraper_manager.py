from concurrent.futures import ThreadPoolExecutor, as_completed
from scrapers.proxy_scrape import ProxyScrape
from scrapers.free_proxy_list import FreeProxyListScraper
from scrapers.proxifly import ProxyFly

def _scrape_one(scraper):
    try:
        proxies = scraper.fetch_proxies()
        return scraper.name, proxies, None
    except Exception as e:
        return scraper.name, [], e

class ScraperManager:
    def __init__(self, max_workers: int = 3):
        self.scrapers = [ProxyScrape(), FreeProxyListScraper(), ProxyFly()]
        self.max_workers = max_workers

    def run_all_scrapers(self):
        all_proxies = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            futures = [ex.submit(_scrape_one, s) for s in self.scrapers]
            for fut in as_completed(futures):
                name, proxies, err = fut.result()
                if err:
                    print(f"[WARN] {name} failed: {err}")
                else:
                    print(f"[OK] {name}: {len(proxies)} proxies")
                    all_proxies.extend(proxies)

        # DEDUP subito: normalizza in "ip:port"
        seen = set()
        unique = []
        for p in all_proxies:
            key = f"{p['ip']}:{p['port']}"
            if key not in seen:
                seen.add(key)
                unique.append(p)
        print(f"[INFO] Unique proxies after dedup: {len(unique)}")
        return unique
