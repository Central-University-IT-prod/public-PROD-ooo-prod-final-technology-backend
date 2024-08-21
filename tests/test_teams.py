from httpx import AsyncClient


async def test_create_team(
    async_client: AsyncClient,
    user_token,
    event_id: str,
):
    headers = {
        'Authorization': f"Bearer {user_token}"
    }
    data = {
        'event_id': event_id,
        'title': 'Title',
        'description': '13131231',
    }
    response = await async_client.post('/api/teams', json=data, headers=headers)
    assert response.status_code == 201

    new_data = {
        'event_id': event_id,
        'title': 'Title1',
        'description': '13131231',
    }

    response = await async_client.post('/api/teams', json=new_data, headers=headers)
    assert response.status_code == 409


# async def test_send_request_to_team(
#     async_client: AsyncClient,
#     user_token,
#     event_id: int,
#     team_id: int,
# ):
#     headers = {
#         'Authorization': f"Bearer {user_token}"
#     }

#     response = await async_client.post(f'/api/teams/req/{team_id}', headers=headers)

#     assert response.status_code == 201


# async def test_get_teams_request(
#     async_client: AsyncClient,
#     team_id: int,
#     user_token: int,
# ):
#     headers = {
#         'Authorization': f"Bearer {user_token}"
#     }

#     response = await async_client.post(f'/api/teams/req/{team_id}', headers=headers)

#     assert response.status_code == 201

