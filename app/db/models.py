from sqlmodel import Field, Session, SQLModel, create_engine
from app.env import DATABASE_URL
from datetime import datetime
from enum import Enum

class ArticleStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"

class Article(SQLModel, table=True):
    __tablename__ = "articles"
    id: int = Field(default=None, primary_key=True)
    title: str
    url: str = Field(unique=True)
    image_url: str | None = Field(default=None)
    source: str
    content: str | None = Field(default=None)
    published_at: datetime | None = Field(default=None)
    lead: str | None = Field(default=None)
    status: ArticleStatus = Field(default=ArticleStatus.PENDING)
    error_message: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

class ArticleRepository:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        SQLModel.metadata.create_all(self.engine)

    def get_article(self, article_id: int):
        with Session(self.engine) as session:
            return session.get(Article, article_id)