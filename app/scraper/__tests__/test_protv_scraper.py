import pytest
from app.scraper.protv import ProTVArticleScraper
from app.scraper.scraping_bee import sbclient

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

def test_scrape_article_content():
    """Test that article content can be extracted from a PRO TV article"""
    # Check API access first
    try:
        response = sbclient.get("https://www.protv.ro")
        if response.status_code != 200:
            pytest.skip(f"Skipping test: ScrapingBee API returned {response.status_code}")
    except Exception as e:
        pytest.skip(f"Skipping test: ScrapingBee API error - {str(e)}")
    
    # If API is working, test the content scraper
    scraper = ProTVArticleScraper()
    test_url = "https://stirileprotv.ro/stiri/actualitate/ce-spun-ungurii-despre-rezultatul-alegerilor-prezidentiale-din-romania-l-au-descris-pe-george-simion-intr-un-singur-cuvant.html"
    content = scraper.scrape_article_content(test_url)
    
    # Verify we got content
    assert isinstance(content, str)
    assert len(content) > 0, "No article content found"
    
    # Print sample of content for debugging
    print(f"Content sample: \n\n{content[:250]}...\n\n")