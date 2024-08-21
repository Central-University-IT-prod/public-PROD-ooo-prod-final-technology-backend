from pydantic import BaseModel


class SkillResponse(BaseModel):
    id: int
    title: str


class AddSkillToUser(BaseModel):
    skill_id: int


class RemoveSkillFromUser(AddSkillToUser):
    pass
