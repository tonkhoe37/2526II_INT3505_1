from fastapi import APIRouter
from core.event_bus import publish

router = APIRouter()


@router.post("/enroll/{course_id}")
def enroll(course_id: int):

    publish("USER_ENROLLED", {"course_id": course_id})

    return {"message": "enrolled"}
