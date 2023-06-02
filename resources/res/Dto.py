from typing import Optional, List
from pydantic import BaseModel
import datetime


class UsersModel(BaseModel):
    id: str
    user_id: str
    password: str
    name: str
    user_num: int
    role: int


class LectureModel(BaseModel):
    lecture_id: str
    title: str
    professor_id: str
    room: int
    room_count: int


class StepModel(BaseModel):
    assignment_id: str
    lecture_id: str
    user_id: str
    step: int
    score: int


class AssignmentModel(BaseModel):
    assignment_id: str
    lecture_id: str
    title: str
    start_date: List[int]
    due_date: List[int]
    description: str


class URLModel(BaseModel):
    id: str
    lecture_id: str
    container_address: str
    api_endpoint: Optional[str]
