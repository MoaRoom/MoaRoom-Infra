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
    "http://moaroom-front.duckdns.org:3000",
    "http://moaroom-back.duckdns.org:8080",
    "http://localhost:3000",  # for dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def schedule_cronjob(dt, assignment_id, lecture_id, assignment_path):
    month, day, hour, minute = dt[1], dt[2], dt[3], dt[4]
    os.system(
        f"/bin/bash {os.path.dirname(os.path.realpath(__file__))}/cronjob.sh {minute} {hour} {day} {month} {assignment_id} {lecture_id} {assignment_path}")


def create_directories(assignment_id, assignment_path, lecture_id, data_users_assigned):
    dir_path_student = Urls.dir_path_student
    dir_path_professor = Urls.dir_path_professor
    for user in data_users_assigned:
        # mkdir in student
        encoded_dir_path_student = base64.b64encode((
            f"{dir_path_student}/{assignment_path}").encode('ascii')).decode('ascii')  # base64 encode
        urlmodel = json.loads(requests.get(
            f"{Urls.base_url}/users/{user['userId']}/{lecture_id}/url").text)
        url = f"{urlmodel['apiEndpoint']}/mkdir/{encoded_dir_path_student}"
        result = requests.post(url).text
        if result == False:
            print(f"Error in mkdir, uid:{user['userId']}")

        # mkdir in professor
        os.makedirs(f"{dir_path_professor}/{assignment_id}/{user['userId']}")


@app.post("/assignments/")
async def create_assignment(assignment_info: Dto.AssignmentModel = None):
    assignment_id = assignment_info.assignment_id
    assignment_title = assignment_info.title
    lecture_id = assignment_info.lecture_id

    assignment_path = f"{assignment_title}-{assignment_id}"
    json_str = requests.get(
        f"{Urls.base_url}/assignments/{assignment_id}/urls").text
    data_users_assigned = list(json.loads(json_str))
    due_date = assignment_info.due_date

    # mkdir
    create_directories(assignment_id, assignment_path,
                       lecture_id, data_users_assigned)

    # cron
    schedule_cronjob(due_date, assignment_id, lecture_id, assignment_path)

    return True


@app.get("/assignment/")
async def get_assignment(id: str, assignment_id: str):
    dir_path_professor = Urls.dir_path_professor
    dir_path = f"{dir_path_professor}/{assignment_id}/{id}"
    curr_path = os.path.dirname(os.path.realpath(__file__))
    file_list = os.listdir(dir_path)
    return_dict = {}
    for file in file_list:
        file_path = f"{dir_path}/{file}"
        f = open(file_path, "r")
        content = f.read()
        return_dict["content"] = content
        f.close()
        os.system(f"/bin/bash {curr_path}/getValueAndTime.sh {file_path}")
        f = open(f"{curr_path}/values.txt", "r")
        values = f.read()
        return_dict["answer"] = values
        f.close()
        f = open(f"{curr_path}/time.txt", "r")
        time = f.read()
        return_dict["runtime"] = time
        f.close()

    return json.dumps(return_dict)
