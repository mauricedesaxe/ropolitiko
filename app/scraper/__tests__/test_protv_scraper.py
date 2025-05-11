import pytest
from app.scraper.protv import ProTVArticleScraper
from app.scraper.scraping_bee import sbclient
import pprint

def test_protv_article_scraper_page_1():
    """Test that ProTVArticleScraper can extract articles properly"""
    # Check API access first
    try:
        response = sbclient.get("https://www.protv.ro")
        if response.status_code != 200:
            pytest.skip(f"Skipping test: ScrapingBee API returned {response.status_code}")
    except Exception as e:
        pytest.skip(f"Skipping test: ScrapingBee API error - {str(e)}")
    
    # If we get here, API is working
    scraper = ProTVArticleScraper()
    articles = scraper.scrape_article_list_from_top_read(page=1)
    
    # Verify we got some articles
    assert len(articles) > 0, "No articles found"
    
    # Test article structure
    assert all(["title" in article for article in articles])
    assert all(["url" in article for article in articles])
    assert all(["source" in article for article in articles])

def test_protv_article_scraper_page_2():
    """Test that ProTVArticleScraper can extract articles properly"""
    # Check API access first
    try:
        response = sbclient.get("https://www.protv.ro")
        if response.status_code != 200:
            pytest.skip(f"Skipping test: ScrapingBee API returned {response.status_code}")
    except Exception as e:
        pytest.skip(f"Skipping test: ScrapingBee API error - {str(e)}")
    
    # If we get here, API is working
    scraper = ProTVArticleScraper()
    articles = scraper.scrape_article_list_from_top_read(page=2)
    
    # Verify we got some articles
    assert len(articles) > 0, "No articles found"
    
    # Test article structure
    assert all(["title" in article for article in articles])
    assert all(["url" in article for article in articles])
    assert all(["source" in article for article in articles])

