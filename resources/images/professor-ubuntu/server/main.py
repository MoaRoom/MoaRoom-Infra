#!/usr/bin/python3
import requests
from fastapi import FastAPI
from flask_pydantic import validate
import os
import json
import base64
import res.Dto as Dto
import res.Urls as Urls

app = FastAPI()


def schedule_cronjob(dt, assignment_id):
    month, day, hour, minute = dt.month, dt.day, dt.hour, dt.minute
    os.system('/bin/bash %s/cronjob.sh %d %d %d %d %d' %
              (os.path.dirname(os.path.realpath(__file__)), minute, hour, day, month, assignment_id))


def create_directories(assignment_id, data_users_assigned):
    dir_path_student = Urls.dir_path_student
    dir_path_professor = Urls.dir_path_professor
    for user in data_users_assigned:
        # mkdir in student
        encoded_dir_path_student = base64.b64encode((
            dir_path_student+"/"+str(assignment_id)).encode('ascii')).decode('ascii')  # base64 encode
        url = Urls.student_base_url+"/mkdir/"+encoded_dir_path_student
        result = requests.post(url).text
        if result == False:
            print("Error in mkdir, uid:"+user.id)

        # mkdir in professor
        os.makedirs("%s/%s/%s" % (dir_path_professor, assignment_id, user.id))


@app.post("/assignment/")
async def create_assignment(assignment_info: Dto.AssignmentModel = None):
    assignment_id = assignment_info.assignment_id
    json_str = requests.get(Urls.base_url+"?assignment_id="+assignment_id).text
    data_users_assigned = list(json.loads(json_str))  # json to list[dict]
    due_date = assignment_info.due_date

    # mkdir
    create_directories(assignment_id, data_users_assigned)

    # cron
    schedule_cronjob(due_date, assignment_id)
