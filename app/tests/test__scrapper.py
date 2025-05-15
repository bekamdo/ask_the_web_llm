import pytest
from app.services.scraper import ScraperService

@pytest.fixture
def scraper():
    return ScraperService()

def test_scrape_valid_url(scraper):
    """Test scraping a known-good URL"""
    result = scraper.scrape_page("https://en.wikipedia.org/wiki/Coffee")
    assert isinstance(result, dict)
    assert "title" in result
    assert "text" in result
    assert len(result["text"]) > 100  # Should have substantial content

def test_scrape_invalid_url(scraper):
    """Test handling of invalid URLs"""
    result = scraper.scrape_page("https://invalid.url.123")
    assert isinstance(result, dict)
    assert result["id"].startswith("error_")
    assert result["title"] == "Failed to scrape URL"
    assert len(result["text"]) > 0  # Error message should exist