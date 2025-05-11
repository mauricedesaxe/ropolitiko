import pytest  # noqa: F401
from app.scraper.scraping_bee import sbclient
from bs4 import BeautifulSoup

def test_scraping_bee_protv():
    """Test that ScrapingBee can successfully scrape protv.ro/articole and extract content"""
    # Make the request to ProTV articles page
    response = sbclient.get("https://www.protv.ro/articole")
    
    # Check that the request was successful
    assert response.status_code == 200
    
    # Verify we got HTML content back
    assert b"<!DOCTYPE html>" in response.content
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Verify we can extract specific elements from the page
    # Find the main title section
    title_element = soup.find("h1")
    assert title_element is not None
    assert "Articole" in title_element.text
    
    # Verify we can find at least some article elements
    articles = soup.find_all("article")
    assert len(articles) > 0, "No articles found on the page"
    
    # Check that we can extract titles from articles
    article_titles = [a.find("h3") for a in articles if a.find("h3")]
    assert len(article_titles) > 0, "No article titles found"
    
    # Print first few article titles for verification (helpful for debugging)
    print("\nExtracted article titles:")
    for i, title in enumerate(article_titles[:3]):
        print(f"{i+1}. {title.text.strip()}")