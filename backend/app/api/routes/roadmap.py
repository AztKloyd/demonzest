from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.roadmap import RoadmapResponse
from app.services.roadmap_service import load_roadmap


router = APIRouter(prefix="/roadmap", tags=["roadmap"])


@router.get("", response_model=RoadmapResponse)
def get_roadmap(_current_user: User = Depends(get_current_user)):
    return load_roadmap()
