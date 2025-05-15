import requests
from typing import List, Dict
from langchain_community.tools import DuckDuckGoSearchResults
from app.utils.config import Config
import logging
from datetime import datetime
import uuid  # Added for consistent ID generation


class SearchService:
    @staticmethod
    def search_web(query: str, num_results: int = 5) -> List[Dict]:
        """Search the web using configured providers and return consistent results."""
        try:
            # Determine which search provider to use
            if Config.SERPER_API_KEY:
                raw_results = SearchService._serper_search(query, num_results)
                provider = "serper"
            else:
                raw_results = SearchService._duckduckgo_search(query, num_results)
                provider = "duckduckgo"

            formatted_results = []
            for i, result in enumerate(raw_results[:num_results], 1):
                # Generate a base result with consistent fields
                base_result = {
                    "id": str(uuid.uuid4())[:8],  # Consistent ID format with scraper
                    "title": result.get("title", f"Result {i}"),
                    "url": result.get("link", result.get("url", "")),
                    "text": result.get("snippet", result.get("body", "")),
                    "snippet": result.get("snippet", result.get("body", "")[:200] + "..."),
                    "metadata": {
                        "source": provider,
                        "timestamp": datetime.now().isoformat(),
                        "position": i
                    }
                }
                formatted_results.append(base_result)

            return formatted_results

        except Exception as e:
            logging.error(f"Search failed: {str(e)}")
            return [{
                "id": "error_" + str(uuid.uuid4())[:4],  # Consistent error ID format
                "title": "Search Error",
                "url": "",
                "text": str(e),
                "snippet": str(e),
                "metadata": {"error": True}
            }]

    @staticmethod
    def _duckduckgo_search(query: str, num_results: int) -> List[Dict]:
        """Perform search using DuckDuckGo."""
        try:
            search = DuckDuckGoSearchResults()
            results = search.run(f"{query} -num={num_results}")

            # Normalize DuckDuckGo results to our expected format
            if isinstance(results, dict):
                return [{
                    "title": results.get("title", ""),
                    "link": results.get("link", ""),
                    "snippet": results.get("snippet", ""),
                    "body": results.get("body", "")
                }]
            elif isinstance(results, list):
                return [{
                    "title": r.get("title", ""),
                    "link": r.get("link", ""),
                    "snippet": r.get("snippet", ""),
                    "body": r.get("body", "")
                } for r in results]
            return []
        except Exception as e:
            raise Exception(f"DuckDuckGo failed: {str(e)}")

    @staticmethod
    def _serper_search(query: str, num_results: int) -> List[Dict]:
        """Perform search using Serper API."""
        if not Config.SERPER_API_KEY:
            raise ValueError("Missing SERPER_API_KEY")

        try:
            response = requests.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": Config.SERPER_API_KEY,
                    "Content-Type": "application/json",
                },
                json={"q": query, "num": num_results},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            # Normalize Serper results to our expected format
            return [{
                "title": r.get("title", ""),
                "link": r.get("link", ""),
                "snippet": r.get("snippet", ""),
                "body": r.get("body", "")
            } for r in data.get("organic", [])]
        except Exception as e:
            raise Exception(f"Serper failed: {str(e)}")