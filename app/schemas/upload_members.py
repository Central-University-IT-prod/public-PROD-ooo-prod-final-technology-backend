from pydantic import BaseModel


class UploadMembersRequest(BaseModel):
    spreadsheet_url: str
    event_id: int
