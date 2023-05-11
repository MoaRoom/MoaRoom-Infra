from typing import Optional
from pydantic import BaseModel
import datetime


class UsersModel(BaseModel):
    id: int
    user_id: str
    password: str
    name: str
    user_num: int
    role: int


class LectureModel(BaseModel):
    lecture_id: int
    title: str
    room: int
    professor_id: int


class StepModel(BaseModel):
    assignment_id: int
    lecture_id: int
    user_id: int
    step: int
    score: int


class AssignmentModel(BaseModel):
    assignment_id: int
    lecture_id: int
    title: str
    start_date: datetime.datetime
    due_date: datetime.datetime
    description: str


class URLModel(BaseModel):
    id: int
    lecture_id: int
    url: str
    
