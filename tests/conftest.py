from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.oauth2 import create_access_token

############### TEST DATABASE ###############
from app.config import settings
from app.database import  get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import models

db1 = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
db2 = f'{settings.database_url_real}'
db3 = 'postgresql://aaripostgres:Zapopan10@localhost:5432/fastapi'

SQLALCHEMY_URL = db1
print('-------------------')
print('database settings testing: ', SQLALCHEMY_URL)
print('-------------------')

engine = create_engine(SQLALCHEMY_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#-------------- TEST DATABASE #--------------



############### INITIALIZE APP ###############
@pytest.fixture()
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
#-------------- INITIALIZE APP #--------------

@pytest.fixture()
def test_user(client):
    user_data = {
            'email': 'test@test.com',
            'password': 'test'
            }
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = 'test'
    return new_user

@pytest.fixture()
def test_user_2(client):
    user_data = {
            'email': 'test1@test.com',
            'password': 'test'
            }
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = 'test'
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token(data = {'user_id': test_user['id']})
    
@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client


@pytest.fixture
def create_test_posts(test_user, test_user_2, db_session):
    _post_data = [
        {
            'title': 'first title',
            'content': 'first content',
            'owner_id': test_user['id']
        }, {
            'title': 'second title',
            'content': 'second content',
            'owner_id': test_user['id']
        }, {
            'title': 'third title',
            'content': 'third content',
            'owner_id': test_user['id']
        }, {
            'title': 'Other Poster',
            'content': 'shit poster',
            'owner_id': test_user_2['id']
        }]

    def create_post_model(obj):
        return models.Post(**obj)
    
    _posts_map = map(create_post_model, _post_data)
    _posts_list = list(_posts_map)
    db_session.add_all(_posts_list)
    db_session.commit()
    return db_session.query(models.Post).order_by(models.Post.id).all()