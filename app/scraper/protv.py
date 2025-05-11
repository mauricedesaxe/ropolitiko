from bs4 import BeautifulSoup
from app.scraper.scraping_bee import sbclient
import logging
from app.scraper.title_relevancy import is_relevant_title
from typing import List, TypedDict, Optional

class ArticleData(TypedDict):
    title: str
    url: str
    image_url: Optional[str]
    source: str
    published_at: Optional[str]
    lead: Optional[str]

class ProTVArticleScraper:
    BASE_URL = "https://stirileprotv.ro/"
    
    def scrape_article_list_from_top_read(self, page: int = 1, filter_irrelevant=True) -> List[ArticleData]:
        """
        Scrape articles from PRO TV website.
        Returns a list of article data dictionaries for future processing.
        Note: This function does not scrape the article content, only the list of articles.
        
        Returns:
            List[ArticleData]: A list of dictionaries with the following structure:
                {
                    "title": str,           # The article title
                    "url": str,             # The article URL
                    "image_url": str | None, # URL to the article's image (if available)
                    "source": str,          # Always "PRO TV"
                    "published_at": str | None, # Publication date/time (if available)
                    "lead": str | None,     # Article summary/lead paragraph (if available)
                }
        """
        try:
            # https://stirileprotv.ro/top-citite/?page=1
            response = sbclient.get(self.BASE_URL + f"top-citite/?page={page}")
            
            if response.status_code == 402:
                logging.error("ScrapingBee API credits exhausted")
                raise Exception("ScrapingBee API credits exhausted")
            elif response.status_code != 200:
                logging.error(f"Failed to fetch data: HTTP {response.status_code}")
                raise Exception(f"Failed to fetch data: HTTP {response.status_code}")
                
            soup = BeautifulSoup(response.content, 'html.parser')
            articles: List[ArticleData] = []
            relevant_articles: List[ArticleData] = []
            
            # Find all article elements
            article_elements = soup.find_all("article")
            
            for article in article_elements:
                # Extract the URL
                link_element = article.find("a")
                url = link_element.get("href") if link_element else None
                
                # Extract the title
                title_element = article.find("h2")
                if not title_element:
                    continue
                    
                title = title_element.text.strip() if title_element else None
                
                # Extract image URL if available
                img_element = article.select_one("picture img")
                image_url = img_element.get("src") if img_element else None

                # Extract published date if available
                date_element = article.find("div", class_="article-date")
                published_at = date_element.text.strip() if date_element else None

                # Extract lead/summary if available
                lead_element = article.find("div", class_="article-lead")
                lead = lead_element.text.strip() if lead_element else None

                # Add the article data to our list
                articles.append({
                    "title": title,
                    "url": url,
                    "image_url": image_url,
                    "source": "PRO TV",
                    "published_at": published_at,
                    "lead": lead,
                })
                
            # After gathering all articles, filter them
            if filter_irrelevant:
                for article in articles:
                    if is_relevant_title(article["title"]):
                        relevant_articles.append(article)
                return relevant_articles
            
            return articles
        except Exception as e:
            logging.exception(f"Error in ProTVArticleScraper: {str(e)}")
            raise

    def scrape_article_content(self, url: str) -> str:
        """
        Scrape the content of an article from PRO TV.
        
        Args:
            url (str): The URL of the article to scrape. 
            An example URL is https://stirileprotv.ro/stiri/actualitate/ce-spun-ungurii-despre-rezultatul-alegerilor-prezidentiale-din-romania-l-au-descris-pe-george-simion-intr-un-singur-cuvant.html

        Returns:
            str: The content of the article.
        """
        try:
            response = sbclient.get(url)
            if response.status_code == 402:
                logging.error("ScrapingBee API credits exhausted")
                raise Exception("ScrapingBee API credits exhausted")
            elif response.status_code != 200:
                logging.error(f"Failed to fetch data: HTTP {response.status_code}")
                raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find("div", class_="article--text")
            return content.text.strip() if content else ""
        except Exception as e:
            logging.exception(f"Error in ProTVArticleScraper: {str(e)}")
            raise