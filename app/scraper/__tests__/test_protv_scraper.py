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
    test_urls = [
        "https://stirileprotv.ro/stiri/actualitate/ce-spun-ungurii-despre-rezultatul-alegerilor-prezidentiale-din-romania-l-au-descris-pe-george-simion-intr-un-singur-cuvant.html",
        "https://stirileprotv.ro/stiri/actualitate/cine-este-george-simion-castigator-in-primul-tur-la-alegerile-prezidentiale-2025-de-la-activist-la-favorit-la-cotroceni.html",
        "https://stirileprotv.ro/alegeri/prezidentiale/2024/basescu-critica-dur-diaspora-zei-traiesc-in-occident-si-spun-voi-care-traiti-acasa-ia-treceti-catre-tatucu-putin.html",
        "https://stirileprotv.ro/alegeri/prezidentiale/2024/kremlinul-si-a-anuntat-oficial-sprijinul-pentru-george-simion-mesajul-fantasmagoric-transmis-de-ideologul-lui-putin.html",
        "https://stirileprotv.ro/stiri/financiar/dezastru-pe-piata-valutara-cursul-oficial-anuntat-de-bnr.html"
    ]

    for test_url in test_urls:
        content = scraper.scrape_article_content(test_url)
        
        # Verify we got content
        assert isinstance(content, str)
        assert len(content) > 0, "No article content found"
        
        # Print sample of content for debugging
        print(f"Content sample: \n\n{content[:250]}...\n\n")

        # extract title from url
        title = test_url.split("/")[-1].replace(".html", "")

        # write file to ./raw_content_samples/ce-spun-ungurii.txt
        with open(f"app/scraper/__tests__/raw_content_samples/{title}.txt", "w") as f:
            f.write(content)
