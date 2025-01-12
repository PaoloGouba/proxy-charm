# ProxyCharm

**ProxyCharm** is a Python-based tool designed to fetch, validate, and save working proxies. It uses modular scraping and validation to ensure reliable results and offers extensibility for adding new proxy sources.

---

## Features

- Fetch proxies from multiple sources using modular scrapers.
- Validate proxies for:
  - Connectivity.
  - Speed.
  - Anonymity.
- Multi-threaded validation for faster performance.
- Save valid proxies to a `.txt` file for easy use.
- Extensible by adding custom scrapers.

---

## Requirements

- **Python**: 3.8 or higher
- **Dependencies**:
  - `requests`
  - `beautifulsoup4`
  - `concurrent.futures` (standard library)

Install required packages:
```bash
pip install -r requirements.txt
```
How to Use
Clone the repository:

```bash
git clone https://github.com/yourusername/proxycharm.git
cd proxycharm
```

Run the main script:

```bash
Copier le code
python main.py
```

Check the output:

Valid proxies are saved in: output/proxies.txt
Rejected proxies (for debugging) are saved in: rejected_proxies.txt

## Adding New Scrapers
You can contribute by adding new scrapers to fetch proxies from additional sources. Follow these steps:

1. Create a New Scraper
Add a new Python file in the scrapers directory.
Inherit from the BaseScraper class to ensure compatibility.
Example:

```python
import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class ExampleScraper(BaseScraper):
    @property
    def name(self):
        return "ExampleScraper"

    def fetch_proxies(self):
        url = "https://example.com/proxies"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        proxies = []

        # Extract proxies from the page
        for row in soup.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) >= 2:
                ip = columns[0].text.strip()
                port = columns[1].text.strip()
                proxies.append({"ip": ip, "port": port})

        return proxies
```        
2. Register the Scraper
Add your scraper to the ScraperManager in core/scraper_manager.py.
Example:

```python
from scrapers.example_scraper import ExampleScraper

class ScraperManager:
    def __init__(self):
        self.scrapers = [
            ExampleScraper(),
            # Other scrapers
        ]
```        
3. Test the Scraper
Run the main script to verify your scraper:

```bash
python main.py
```
## Contributions
We welcome contributions to improve ProxyCharm! You can contribute by:

Adding new scrapers for additional proxy sources.
Optimizing the validation process.
Reporting and fixing bugs.
Improving documentation.
Feel free to fork the repository and submit a pull request!

## License
This project is licensed under the MIT License. See the LICENSE file for details.

Enjoy using ProxyCharm! 🚀






