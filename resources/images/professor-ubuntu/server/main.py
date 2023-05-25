#!/usr/bin/python3
import requests
from fastapi import FastAPI
from flask_pydantic import validate
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import base64
import res.Dto as Dto
import res.Urls as Urls

app = FastAPI()

# CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def schedule_cronjob(dt, assignment_id):
    month, day, hour, minute = dt.month, dt.day, dt.hour, dt.minute
    os.system('/bin/bash %s/cronjob.sh %d %d %d %d %s' %
              (os.path.dirname(os.path.realpath(__file__)), minute, hour, day, month, assignment_id))


def create_directories(assignment_id, data_users_assigned):
    dir_path_student = Urls.dir_path_student
    dir_path_professor = Urls.dir_path_professor
    for user in data_users_assigned:
        # mkdir in student
        encoded_dir_path_student = base64.b64encode((
            dir_path_student+"/"+assignment_id).encode('ascii')).decode('ascii')  # base64 encode
        url = Urls.student_base_url+"/mkdir/" + \
            encoded_dir_path_student  # TODO URLModel 적용 필요
        result = requests.post(url).text
        if result == False:
            print("Error in mkdir, uid:"+user.id)

        # mkdir in professor
        os.makedirs("%s/%s/%s" % (dir_path_professor, assignment_id, user.id))


@app.post("/assignments/")
async def create_assignment(assignment_info: Dto.AssignmentModel = None):
    assignment_id = assignment_info.assignment_id
    json_str = requests.get(Urls.base_url+"?assignment_id="+assignment_id).text
    data_users_assigned = list(json.loads(json_str))   # TODO URLModel 적용 필요
    due_date = assignment_info.due_date

    # mkdir
    create_directories(assignment_id, data_users_assigned)

    # cron
    schedule_cronjob(due_date, assignment_id)

    return True


@app.get("/assignment/")
async def get_assignment(id: str, assignment_id: str):
    dir_path_professor = Urls.dir_path_professor
    dir_path = "%s/%s/%s" % (dir_path_professor, assignment_id, id)
    file_list = os.listdir(dir_path)
    return_dict = {}
    for file in file_list:
        f = open(dir_path+"/"+file, "r")
        content = f.read()
        return_dict["content"] = content
        f.close()

    return json.dumps(return_dict)
