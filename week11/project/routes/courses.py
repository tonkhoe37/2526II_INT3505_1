from fastapi import APIRouter
from db import courses

router = APIRouter()


# CREATE
@router.post("/courses")
def create_course(course: dict):
    course["id"] = len(courses) + 1
    courses.append(course)
    return course


# READ + QUERY
@router.get("/courses")
def get_courses(search: str = None):

    if search:
        return [c for c in courses if search.lower() in c["title"].lower()]

    return courses


# HATEOAS
@router.get("/courses/{id}")
def get_course(id: int):

    course = courses[id - 1]

    return {
        "data": course,
        "_links": {"self": f"/courses/{id}", "enroll": f"/enroll/{id}"},
    }


# UPDATE
@router.put("/courses/{id}")
def update_course(id: int, course: dict):
    courses[id - 1] = course
    return course


# DELETE
@router.delete("/courses/{id}")
def delete_course(id: int):
    courses.pop(id - 1)
    return {"message": "deleted"}
