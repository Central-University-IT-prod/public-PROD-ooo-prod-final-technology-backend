async def test_create_user(async_client):
    data = {
        'email': 'john.doe@example.com',
        'fullname': "Andrey Krytoi",
        'password': 'test123151661',
        'telegram_username': "telegram_username",
        'age': 1,
        'profession': 'backend',
        'skills': [1, 2, 5],
        'bio': 'backend',
    }
    response = await async_client.post('/api/users', json=data)
    assert response.status_code == 200


async def test_login_user(async_client):
    data = {
        'email': 'john.doe@example.com',
        'fullname': "Andrey Krytoi",
        'password': 'test123151661',
        'telegram_username': "telegram_username",
        'age': 1,
        'profession': 'backend',
        'skills': [1, 2, 5],
        'bio': 'backend',
    }
    response = await async_client.post('/api/users', json=data)
    assert response.status_code == 200
    data = {
        'email': 'john.doe@example.com',
        'password': 'test123151661',
    }
    response = await async_client.post('/api/users/login', json=data)
    assert response.status_code == 200
    token = response.json()['access_token']
    response = await async_client.get('/api/users/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200


async def test_create_admin(async_client):
    data = {
        'email': 'john.doe@example.com',
        'password': 'test123151661',
    }
    response = await async_client.post('/api/admin', json=data)
    assert response.status_code == 200


async def test_login_admin(async_client):
    data = {
        'email': 'john.doe@example.com',
        'password': 'test123151661',
    }
    response = await async_client.post('/api/admin', json=data)
    assert response.status_code == 200
    data = {
        'email': 'john.doe@example.com',
        'password': 'test123151661',
    }
    response = await async_client.post('/api/admin/login', json=data)
    assert response.status_code == 200
    token = response.json()['access_token']
    response = await async_client.get('/api/admin/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
