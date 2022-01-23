import pytest
from app import schemas
from typing import List
# from jose import jwt
# from app.config import settings



def test_get_all_posts(authorized_client, create_test_posts):
    res = authorized_client.get('/posts/')
    assert len(res.json()) == len(create_test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, create_test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, create_test_posts):
    res = client.get(f'/posts/{create_test_posts[0].id}')
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, create_test_posts):
    res = authorized_client.get(f'/posts/12312312312312312311321312312314214123')
    assert res.status_code == 404

def test_get_one_post(authorized_client, create_test_posts):
    res = authorized_client.get(f'/posts/{create_test_posts[0].id}')
    assert res.status_code == 200

@pytest.mark.parametrize('title, content, published', [
    ('awesome new post', 'awesome new content', True),
    ('2nd insertion', '2nd insertion text', False),
    ('No published status', 'content of no published status', True)
])
def test_create_post(authorized_client, test_user, create_test_posts, title, content, published):
    res = authorized_client.post('/posts/', json={
        'title': title,
        'content': content,
        'published': published
    })
    _created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert _created_post.title == title
    assert _created_post.content == content
    assert _created_post.published == published

@pytest.mark.parametrize('title, content', [
    ('B- awesome new post', 'awesome new content'),
    ('B- 2nd insertion', '2nd insertion text'),
    ('B- No published status', 'content of no published status')
])
def test_create_post_default_publish(authorized_client, test_user, create_test_posts, title, content):
    res = authorized_client.post('/posts/', json={
        'title': title,
        'content': content
    })
    _created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert _created_post.title == title
    assert _created_post.content == content
    assert _created_post.published == True

def test_unauthorized_create_post(client, test_user, create_test_posts):
    res = client.post('/posts/', json={
        'title': 'SOME TITLE SHOULDNT POST',
        'content': 'SOME CONTENT SHOULDNT POST'
    })
    assert res.status_code == 401

def test_unauthorized_delete_post(client, test_user, create_test_posts):
    res = client.delete(f'/posts/{create_test_posts[0].id}')
    assert res.status_code == 401

def test_delete_post(authorized_client, test_user, create_test_posts):
    res = authorized_client.delete(f'/posts/{create_test_posts[0].id}')
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_user, create_test_posts):
    res = authorized_client.delete(f'/posts/515231312312321313213')
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, create_test_posts):
    res = authorized_client.delete(f'/posts/{create_test_posts[3].id}')
    assert res.status_code == 403