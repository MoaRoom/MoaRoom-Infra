#!/usr/bin/python3
import requests
from fastapi import FastAPI
from flask_pydantic import validate
import os
import json
import yaml
import base64
import res.Dto as Dto
import res.Urls as Urls
import datetime

app = FastAPI()


def yaml_to_json(id, isProfessor):
    if isProfessor:
        role = "professor"
    else:
        role = "student"
    f = open("./res/remote-deploy-%s.yml" % role, 'r')
    # apply env var
    ID, PORT = str(id), str(8887+id)
    file = f.read().replace("{{ ID }}", ID)
    file = file.replace("{ PORT }", PORT)
    contents = file.split("---")
    for i in range(len(contents)):
        with open("./res/tmp%d.yml" % i, "w") as tmp:
            tmp.write(contents[i])

    # convert yaml to json
    for i in range(len(contents)):
        with open("./res/tmp%d.yml" % i, 'r') as yaml_in, open("./res/tmp%d.json" % i, "w") as json_out:
            yaml_object = yaml.safe_load(yaml_in)
            json.dump(yaml_object, json_out)

    return len(contents)  # object file num


@app.post("/professor/{professor_info}")
async def create_professor_res(professor_info: str):  # Dto.UsersModel):
    # pid = professor_info.id
    pid = 0

    json_num = yaml_to_json(pid, True)

    for i in range(json_num):
        json_str = json.load(open(
            "./res/tmp%d.json" % i))
        if json_str['kind'] == "Pod":
            url = Urls.kube_base_url+"/api/v1/namespaces/professor-ns/pods"
        elif json_str['kind'] == "Service":
            url = Urls.kube_base_url+"/api/v1/namespaces/professor-ns/services"
        headers = {"Authorization": "Bearer %s" % (os.getenv('TOKEN')),
                   'Accept': 'application/json', "Content-Type": "application/json"}
        result = requests.post(url, data=json.dumps(json_str),
                               headers=headers, verify=os.getenv('CACERT')).text
        if result == False:  # TODO deliver error message
            print("Error in creating professor, id:"+pid)
        else:
            print("success")


@app.post("/lecture/{lecture_info}")
async def create_lecture(lecture_info: str):  # Dto.LectureModel
    json_str = requests.get(
        Urls.base_url+"?lecture_id="+lecture_info.lecture_id).text
    data_users_assigned = list(json.loads(json_str))  # json to list[dict]

    studend_pod_infos = []
    for user in data_users_assigned:
        id = user.id
        json_num = yaml_to_json(id, False)
        for i in range(json_num):
            json_str = json.load(open("./res/tmp%d.json" % i))
            if json_str['kind'] == "Pod":
                url = Urls.kube_base_url+"/api/v1/namespaces/student-ns/pods"
            elif json_str['kind'] == "Service":
                url = Urls.kube_base_url+"/api/v1/namespaces/student-ns/services"
            headers = {"Authorization": "Bearer %s" % (os.getenv('TOKEN')),
                       'Accept': 'application/json', "Content-Type": "application/json"}
            result = requests.post(url, data=json.dumps(json_str),
                                   headers=headers, verify=os.getenv('CACERT')).text
            if result == False:  # TODO deliver error message
                print("Error in creating student, id:"+id)
            else:
                print("success")
