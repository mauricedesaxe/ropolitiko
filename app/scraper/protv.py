from bs4 import BeautifulSoup
from app.scraper.scraping_bee import sbclient
import logging

class ProTVArticleScraper:
    BASE_URL = "https://www.protv.ro/"
    
    def scrape_article_list_from_page(self, page: int = 1):
        """
        Scrape articles from PRO TV website.
        Returns a list of article data dictionaries for future processing.
        Note: This function does not scrape the article content, only the list of articles.
        """
        try:
            # https://www.protv.ro/articole/pagina-1
            response = sbclient.get(self.BASE_URL + f"articole/pagina-{page}")
            
            if response.status_code == 402:
                logging.error("ScrapingBee API credits exhausted")
                raise Exception("ScrapingBee API credits exhausted")
            elif response.status_code != 200:
                logging.error(f"Failed to fetch data: HTTP {response.status_code}")
                raise Exception(f"Failed to fetch data: HTTP {response.status_code}")
                
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find all article elements
            article_elements = soup.find_all("article")
            
            for article in article_elements:
                # Extract the title
                title_element = article.find("h3")
                if not title_element:
                    continue
                    
                title = title_element.text.strip()
                
                # Extract the URL if available
                link_element = title_element.find("a") or article.find("a")
                url = link_element.get("href") if link_element else None
                
                # Extract image URL if available
                img_element = article.find("img")
                image_url = img_element.get("src") if img_element else None

                # Extract published_at if available
                published_at_element = article.find("time")
                published_at = published_at_element.get("datetime") if published_at_element else None

                # Extract category if available
                category_element = article.find("a", class_="category-link")
                category = category_element.text.strip() if category_element else None

                # Add the article data to our list
                articles.append({
                    "title": title,
                    "url": url,
                    "image_url": image_url,
                    "source": "PRO TV",
                    "published_at": published_at,
                    "category": category,
                })
                
            return articles
        except Exception as e:
            logging.exception(f"Error in ProTVArticleScraper: {str(e)}")
            raise