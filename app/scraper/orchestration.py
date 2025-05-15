import logging
from datetime import datetime
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scraper.protv import ProTVArticleScraper
from app.db.models import Article

# Initialize scraper and scheduler
protv_scraper = ProTVArticleScraper()
scheduler = AsyncIOScheduler()

async def scrape_protv():
    """
    Scrape ProTV articles and save them to the database.
    Runs as a scheduled task.
    """
    logging.info(f"Starting ProTV scrape at {datetime.now()}")
    try:
        # Get articles from top read section
        articles = protv_scraper.scrape_article_list_from_top_read(page=1, filter_irrelevant=True)
        logging.info(f"Found {len(articles)} relevant ProTV articles")
        
        # Process each article
        for article in articles:
            try:
                # Scrape full content
                content = protv_scraper.scrape_article_content(article["url"])
                
                # Save complete article to database
                article_data = {
                    **article,
                    "content": content,
                    "scraped_at": datetime.now().isoformat()
                }
                await Article.create(article_data)
                
                # Avoid hitting rate limits
                await asyncio.sleep(1)
                
            except Exception as e:
                logging.error(f"Error processing article {article['url']}: {str(e)}")
                
        logging.info(f"Completed ProTV scrape at {datetime.now()}")
        
    except Exception as e:
        logging.exception(f"ProTV scraping job failed: {str(e)}")

def start_scraping_scheduler():
    """
    Start the scheduler for periodic scraping tasks.
    This function should be called during application startup.
    """
    # Schedule ProTV scraper to run hourly
    print("Adding jobs to scraping scheduler")
    scheduler.add_job(scrape_protv, 'interval', hours=1, id='scrape_protv')
    
    # Start the scheduler
    print("Starting scraping scheduler")
    scheduler.start()
    logging.info("News scraping scheduler started")

def stop_scraping_scheduler():
    """
    Stop the scraping scheduler.
    This function should be called during application shutdown.
    """
    print("Stopping scraping scheduler")
    scheduler.shutdown()
    logging.info("News scraping scheduler stopped")