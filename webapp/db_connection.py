import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("DB_USER")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
MYSQL_HOST = os.getenv("DB_HOST")
MYSQL_DATABASE = os.getenv("DB_NAME")

def get_engine():
    db_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
    return create_engine(db_url)


