from core.scraper_manager import ScraperManager
from core.validator import validate_proxies
from core.storage import save_proxies_to_file
import os

if __name__ == "__main__":
    # Crea la cartella output se non esiste
    os.makedirs("output", exist_ok=True)

    # Esegui il gestore degli scraper
    scraper_manager = ScraperManager()

    print("Fetching proxies from all sources...")
    all_proxies = scraper_manager.run_all_scrapers()

    print("Validating proxies...")
    valid_proxies = validate_proxies(all_proxies)

    print(f"Found {len(valid_proxies)} valid proxies. Saving to file...")
    save_proxies_to_file(valid_proxies)

    print("Done!")
