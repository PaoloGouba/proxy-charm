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
    print(f"Fetched {len(all_proxies)} proxies.")

    # Validazione delle proxy con multi-threading
    print("Validating proxies...")
    valid_proxies = validate_proxies(all_proxies, repetitions=3, max_threads=20)
    print(f"Found {len(valid_proxies)} valid proxies.")

    # Salvataggio delle proxy valide
    print("Saving valid proxies to file...")
    save_proxies_to_file(valid_proxies)
    print("Done!")
