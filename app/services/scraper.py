from newspaper import Article
from typing import Dict
import requests
from bs4 import BeautifulSoup
import uuid  # For generating unique IDs

class ScraperService:
    @staticmethod
    def scrape_page(url: str) -> Dict:
        """Scrape article text from a URL."""
        try:
            article = Article(url)
            article.download()
            article.parse()

            return {
                "id": str(uuid.uuid4())[:8],  # Generate a short unique ID
                "title": article.title,
                "url": url,
                "text": article.text,
                "snippet": article.text[:200] + "..." if article.text else ""  # Add snippet field
            }
        except Exception:
            # Fallback to BeautifulSoup
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')

                for element in soup(['script', 'style', 'nav', 'footer']):
                    element.decompose()

                text = ' '.join(soup.stripped_strings)
                title = soup.title.string if soup.title else url

                return {
                    "id": str(uuid.uuid4())[:8],  # Generate a short unique ID
                    "title": title,
                    "url": url,
                    "text": text,
                    "snippet": text[:200] + "..." if text else ""  # Add snippet field
                }
            except Exception as e:
                return {
                    "id": "error_" + str(uuid.uuid4())[:4],
                    "title": "Failed to scrape URL",
                    "url": url,
                    "text": str(e),
                    "snippet": str(e)
                }