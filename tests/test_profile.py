async def test_put_profile(async_client, user_token, uow):
    headers = {
        'Authorization': f"Bearer {user_token}"
    }
    response = await async_client.get('/api/users/me', headers=headers)
    assert response.status_code == 200
    data = {
        'fullname': 'Имя Фамилия',
        'telegram_username': 'telegram_username',
        'skills': [1, 3, 2, 10]
    }
    response = await async_client.put('/api/users/update', headers=headers, json=data)
    assert response.status_code == 200


async def test_put_profile_id_skill_error(async_client, user_token):
    headers = {
        'Authorization': f"Bearer {user_token}"
    }
    response = await async_client.get('/api/users/me', headers=headers)
    assert response.status_code == 200
    data = {
        'fullname': 'Имя Фамилия',
        'telegram_username': 'telegram_username',
        'skills': [0]
    }
    response = await async_client.put('/api/users/update', headers=headers, json=data)
    assert response.status_code == 400


async def test_put_profile_len_error(async_client, user_token):
    headers = {
        'Authorization': f"Bearer {user_token}"
    }
    response = await async_client.get('/api/users/me', headers=headers)
    assert response.status_code == 200
    data = {
        'fullname': 'Имя Фамилия',
        'telegram_username': 'telegram_username',
        'skills': [1, 2, 3, 4, 5, 6]
    }
    response = await async_client.put('/api/users/update', headers=headers, json=data)
    assert response.status_code == 422
