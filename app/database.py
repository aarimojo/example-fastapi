from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from time import time
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_URL = f'{settings.database_url_real}'
print('-------------------')
print('database settings: ', SQLALCHEMY_URL)
print('-------------------')

engine = create_engine('postgresql://psafrjvyontlgu:a86b8d1e6a03a79c23fc8d1a84433cd4070ec1b5241f4b3a5c55198a23c1f4de@ec2-54-83-157-174.compute-1.amazonaws.com:5432/dci7spq590f2gs')

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


    print('shits fucked')