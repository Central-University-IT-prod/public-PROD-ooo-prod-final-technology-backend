import datetime as dt

from utils.time import get_utc


# async def test_upload_google_sheet(async_client, admin_token):
#     headers = {
#         'Authorization': f"Bearer {admin_token}"
#     }
#     data = {
#         "title": "string",
#         "max_member_qty": 3,
#         "team_creation_deadline": (get_utc() + dt.timedelta(days=3)).strftime('%Y-%m-%d')
#     }
#     response = await async_client.post('/api/admin-events', json=data, headers=headers)
#     assert response.status_code == 201
#     data = {
#         "spreadsheet_url": "https://docs.google.com/spreadsheets/d/1skT4wd7Ns5I-2x0zBMPfU80Qpz1mN6-pnlOB5k2Hq00/edit"
#                            "#gid=0",
#         "event_id": 1
#     }
#     response = await async_client.post('/api/upload-members', json=data, headers=headers)
#     assert response.status_code == 200
