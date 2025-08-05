from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = "sqlite:///C:/Users/User/Python_Projects/linkedin_auto_post/linkedin_posts.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False )
Base = declarative_base()

def init_db():
    from .models import Post, Interaction  # type: ignore # Import models to ensure they are registered
    Base.metadata.create_all(bind=engine)