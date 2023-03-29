from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
import base64


app = FastAPI()


class Assignment(BaseModel):
    ...


@app.post("/assignment/{assignment_info}")
async def create_assignment(assignment_info: Assignment):
    # TODO
    # 1. Slave에 과제마감 api 호출할 cron 작업을 Master에 추가
    #   - Slave의 주소 다 필요함
    #   - ./getAssignments.py 실행
    # 2. 참여자 목록 가져와서 ~/강의명/과제명/학번 생성
    ...
