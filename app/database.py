from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from time import time
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_URL = f'{settings.database_url}'
print(SQLALCHEMY_URL)
engine = create_engine(SQLALCHEMY_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='aaripostgres', 
        password='Zapopan10', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection successful')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error: ', error)
        time.sleep(2)