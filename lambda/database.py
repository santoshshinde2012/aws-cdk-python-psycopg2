from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from shared.get_dburl import get_dburl
from config import Config

Base = declarative_base()

class Database:
    def __init__(self):
        try:
            self.DATABASE_URL = get_dburl(Config.SECRET_NAME)
        except Exception as e:
            raise ValueError(f"Error fetching secret: {str(e)}")

        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        """Ensure all tables are created (useful for local testing)."""
        Base.metadata.create_all(bind=self.engine)
