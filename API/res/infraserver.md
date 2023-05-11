# Infra Server의 API들

## Dto

```python
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

```

## ✅ Control

### endpoint: http://localhost:8003

> 구매 후 ip 및 도메인은 변경될 예정

### 1. `/professor/{professor_info : UsersModel}`

- 용도: Professor 생성 시 호출, 컨테이너 할당, url 반환
- return type: `URLModel`

### 2. `/lecture/{lecture_info : LectureModel}`

- 용도: Lecture 생성 시 호출, Lecture을 수강하는 학생들의 컨테이너 할당, 학생들의 url 반환
- **특이사항**: `lecture_info.lecture_id`를 통해 lecture를 수강하는 학생의 리스트(list(UsersModel))를 받음
- return type: `URLModel`

## ✅ Professor

### endpoint: http://localhost:8002

> 구매 후 ip 및 도메인은 변경될 예정

### 1. `/assignment/{assignment_info : AssignmentModel}`

- 용도: Assignment 생성 시 호출, Assignment를 할당받은 학생들의 pod에 과제 제출 디렉토리를 생성, 과제 마감 시 Professor 컨테이너로 과제 수거
- **특이사항**: `assignment_info.assignment_id`를 통해 해당 assignment가 할당된 학생들의 컨테이너 url 리스트(list(URLModel))를 받음
- return type: None

## ✅ Student

### endpoint: http://localhost:8887~?

> 구매 후 ip 및 도메인은 변경될 예정

### 1. `/mkdir/{dir_path : str}`

- 용도: 과제 생성 시 Student 컨테이너의 과제 디렉토리 생성
- return type: boolean

### 2. `/files/{dir_path : str}`

- 용도: 과제 마감 시 Student 컨테이너의 과제 디렉토리에 있는 내용을 전달
- return type: json
