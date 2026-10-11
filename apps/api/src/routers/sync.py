from fastapi import APIRouter, Depends
from src.jobs.sync_user import sync_user
from src.models.user import User
from src.services.auth import current_active_user

router = APIRouter()

@router.post("", status_code=202)
def trigger_sync(full: bool = False, user: User = Depends(current_active_user)):

    result = sync_user.delay(user.id, full)
    return {"task_id": result.id}