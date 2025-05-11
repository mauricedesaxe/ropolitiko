from sqlmodel import Field, Session, SQLModel, create_engine
from app.env import DATABASE_URL
from datetime import datetime

class NewsArticle(SQLModel, table=True):
    __tablename__ = "news_articles"
    id: int = Field(default=None, primary_key=True)
    title: str
    url: str = Field(unique=True)
    source: str
    content: str
    published_at: datetime
    scraped_at: datetime = Field(default_factory=datetime.now)
    processed: bool = Field(default=False)

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

class NewsArticleRepository:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        SQLModel.metadata.create_all(self.engine)

    def get_news_article(self, news_article_id: int):
        with Session(self.engine) as session:
            return session.get(NewsArticle, news_article_id)
    