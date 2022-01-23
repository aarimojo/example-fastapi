import pytest
from app import schemas
from jose import jwt
from app.config import settings


def test_root_code(client):
    res = client.get('/')
    assert res.status_code == 200

def test_create_user(client):
    res = client.post('/users/', 
        json={
            'email': 'adssadas@a.com',
            'password': 'abcd'
            })
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'adssadas@a.com'
    assert int(res.json().get('id'))
    assert res.status_code == 201

def test_login(client, test_user):
    res = client.post('/login', 
        data={
            'username': test_user['email'],
            'password': test_user['password']
            })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize('email, password, status_code', [
    ('wrongemail@gmail.com', 'test', 403),
    ('test@test.com', 'fuck this shit', 403),
    ('wrongemail@gmail.com', 'fuck this shit', 403),
    (None, 'test', 422),
    ('test@test.com', None, 422),
    ('test@test.com', 'test', 200),
])
def test_correct_login(client, test_user, email, password, status_code):
    res = client.post('/login', 
        data={
            'username': email,
            'password': password
            })
    assert res.status_code == status_code