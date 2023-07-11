import os

import pytest
from fastapi.testclient import TestClient

from webtronics.api.appbuilder import build_app
from webtronics.api.entrypoint import ProductionLifeSpanBuilder
from webtronics.api.routers import posts_router, users_router


@pytest.fixture(scope='session')
def client():
    lifespanbuilder = ProductionLifeSpanBuilder(
        os.getenv('WT_DATABASE_URL'), 'secret'
    )
    fastapp = build_app(
        users_router, posts_router, lifespanbuilder=lifespanbuilder
    )
    with TestClient(fastapp) as client:
        yield client


def test_auth(client, cleanup):
    response = client.get('/users/me')
    assert response.status_code == 401

    response = client.post(
        '/users/signup',
        json={'email': 'a@local', 'username': 'a', 'password': '123456'},
    )
    assert response.status_code == 200
    user = response.json()

    response = client.post(
        '/users/signup',
        json={'email': 'a@local', 'username': 'a', 'password': '123456'},
    )
    assert response.status_code == 422

    response = client.post(
        '/users/signin', json={'email': 'a@local', 'password': '12345'}
    )
    assert response.status_code == 401

    response = client.post(
        '/users/signin', json={'email': 'a@local', 'password': '123456'}
    )
    assert response.status_code == 200

    token = response.json()['jwt_token']
    assert isinstance(token, str)

    auth_header = {'Authentication': f'Bearer {token}'}
    response = client.get('/users/me', headers=auth_header)
    assert response.status_code == 200
    assert response.json() == user

    token = 'EvilToken'
    auth_header = {'Authentication': f'Bearer {token}'}
    response = client.get('/users/me', headers=auth_header)
    assert response.status_code == 401
    response = client.get('/posts/', headers=auth_header)
    assert response.status_code == 401
    response = client.get('/posts/123', headers=auth_header)
    assert response.status_code == 401


def test_posting(client, cleanup):
    response = client.post(
        '/users/signup',
        json={'email': 'a@local', 'username': 'a', 'password': '123456'},
    )
    assert response.status_code == 200
    response = client.post(
        '/users/signin', json={'email': 'a@local', 'password': '123456'}
    )
    assert response.status_code == 200
    token = response.json()['jwt_token']
    auth_header = {'Authentication': f'Bearer {token}'}

    response = client.post(
        '/users/signup',
        json={'email': 'b@local', 'username': 'b', 'password': '123456'},
    )
    assert response.status_code == 200
    response = client.post(
        '/users/signin', json={'email': 'b@local', 'password': '123456'}
    )
    assert response.status_code == 200
    other_token = response.json()['jwt_token']
    other_header = {'Authentication': f'Bearer {other_token}'}

    response = client.post(
        '/posts/', json={'title': 'title', 'text': 'text'}, headers=auth_header
    )
    assert response.status_code == 200
    post_id = response.json()['id']
    response = client.get(f'/posts/{post_id}/', headers=auth_header)
    assert response.status_code == 200
    assert response.json()['id'] == post_id
    assert response.json()['title'] == 'title'
    assert response.json()['text'] == 'text'
    assert response.json()['author']['email'] == 'a@local'
    response = client.get('/posts/', headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.patch(
        f'/posts/{post_id}/', json={'title': 'new title'}, headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()['title'] == 'new title'

    response = client.post(f'/posts/{post_id}/like', headers=auth_header)
    assert response.status_code == 403
    response = client.post(f'/posts/{post_id}/dislike', headers=auth_header)
    assert response.status_code == 403

    response = client.post(f'/posts/{post_id}/like', headers=other_header)
    assert response.status_code == 200
    assert len(response.json()['likes']) == 1
    assert len(response.json()['dislikes']) == 0
    response = client.post(f'/posts/{post_id}/dislike', headers=other_header)
    assert response.status_code == 200
    assert len(response.json()['likes']) == 0
    assert len(response.json()['dislikes']) == 1

    response = client.delete(f'/posts/{post_id}/', headers=auth_header)
    assert response.status_code == 200
    assert response.json()['title'] == 'new title'
    response = client.get(f'/posts/{post_id}/', headers=auth_header)
    assert response.status_code == 404

    response = client.post(f'/posts/{post_id}/like', headers=auth_header)
    assert response.status_code == 404
    response = client.post(f'/posts/{post_id}/dislike', headers=auth_header)
    assert response.status_code == 404
