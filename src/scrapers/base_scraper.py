from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def fetch_proxies(self):
        pass
