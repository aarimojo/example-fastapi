from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from time import time
# from psycopg2.extras import RealDictCursor

db1 = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
db2 = f'{settings.database_url_real}'

SQLALCHEMY_URL = db1
print('-------------------')
print('database settings: ', SQLALCHEMY_URL)
print('-------------------')

try:
    engine = create_engine(SQLALCHEMY_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()


    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # while True:
    #     try:
    #         conn = psycopg2.connect(host='localhost', database='fastapi', user='aaripostgres', 
    #         password='Zapopan10', cursor_factory=RealDictCursor)
    #         cursor = conn.cursor()
    #         print('Database connection successful')
    #         break
    #     except Exception as error:
    #         print('Connection to database failed')
    #         print('Error: ', error)
    #         time.sleep(2)

except:
    print('shits fucked')