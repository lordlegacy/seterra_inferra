from sqlalchemy import create_engine

# Example connection string, replace with actual database URL
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) 