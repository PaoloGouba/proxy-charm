from core.scraper_manager import ScraperManager
from core.validator import validate_proxies
from core.storage import save_proxies_to_file
import os

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    # scraper paralleli
    scraper_manager = ScraperManager(max_workers=3)

    print("Fetching proxies from all sources...")
    all_proxies = scraper_manager.run_all_scrapers()
    print(f"Fetched {len(all_proxies)} proxies.")

    # validazione aggressiva e rapida
    print("Validating proxies...")
    valid_proxies = validate_proxies(
        all_proxies,
        repetitions=1,     # 1 basta; porta a 2 solo se vuoi più confidenza
        max_threads=80,    # I/O-bound
        save_rejected=False
    )
    print(f"Found {len(valid_proxies)} valid proxies.")

    print("Saving valid proxies to file...")
    save_proxies_to_file(valid_proxies)
    print("Done!")
