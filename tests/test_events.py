import datetime as dt
from utils.time import get_utc


async def test_create_event(async_client, admin_token):
    headers = {
        'Authorization': f"Bearer {admin_token}"
    }
    data = {
        "title": "string",
        "max_member_qty": 3,
        "team_creation_deadline": (get_utc() + dt.timedelta(days=3)).strftime('%Y-%m-%d')
    }
    response = await async_client.post('/api/admin-events', json=data, headers=headers)
    assert response.status_code == 201


async def test_delete_event(async_client, admin_token):
    headers = {
        'Authorization': f"Bearer {admin_token}"
    }
    data = {
        "title": "string",
        "max_member_qty": 3,
        "team_creation_deadline": (get_utc() + dt.timedelta(days=3)).strftime('%Y-%m-%d')
    }
    response = await async_client.post('/api/admin-events', json=data, headers=headers)
    assert response.status_code == 201

    response = await async_client.get('/api/admin-events', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

    response = await async_client.delete(f'/api/admin-events/1', headers=headers)
    assert response.status_code == 204

    response = await async_client.get('/api/admin-events', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0
