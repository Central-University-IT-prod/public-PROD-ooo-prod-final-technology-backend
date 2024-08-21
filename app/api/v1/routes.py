from fastapi import APIRouter
from api.v1.endpoints.user import router as user_router
from api.v1.endpoints.admin import router as admin_router
from api.v1.endpoints.event import router as event_router
from api.v1.endpoints.admin_events import router as admin_events_router
from api.v1.endpoints.skills import router as skills_router
from api.v1.endpoints.user_skills import router as user_skills_router
from api.v1.endpoints.upload_members import router as upload_members_router
from api.v1.endpoints.teams import router as teams_router
from api.v1.endpoints.user_events import router as user_events_router


routers = APIRouter(
    prefix='/api'
)

router_list = [
    user_router,
    admin_router,
    event_router,
    admin_events_router,
    skills_router,
    user_skills_router,
    upload_members_router,
    teams_router,
    user_events_router
]

for router in router_list:
    routers.include_router(router)
