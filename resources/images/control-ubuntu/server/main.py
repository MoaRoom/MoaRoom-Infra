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


def yaml_to_json(id, isMaster):
    if isMaster:
        role = "master"
    else:
        role = "slave"
    f = open("./res/remote-deploy-%s.yml" % role, 'r')
    # apply env var
    file = f.read().replace("{{ ID }}", str(id))
    contents = file.split("---")
    for i in range(len(contents)-1):
        with open("./res/tmp%d.yml" % i, "w") as tmp:
            tmp.write(contents[i])

    # convert yaml to json
    for i in range(len(contents)-1):
        with open("./res/tmp%d.yml" % i, 'r') as yaml_in, open("./res/tmp%d.json" % i, "w") as json_out:
            yaml_object = yaml.safe_load(yaml_in)
            json.dump(yaml_object, json_out)

    return len(contents)-1  # object file num


@app.post("/master/{master_info}")
@validate
async def create_master_res(master_info: Dto.UsersModel):
    id = master_info.id

    json_num = yaml_to_json(id, True)

    for i in range(json_num):
        json_str = json.load(open(
            "./res/tmp%d.json" % i))
        if json_str['kind'] == "Pod":
            url = Urls.kube_base_url+"/api/v1/namespaces/master-ns/pods"
        elif json_str['kind'] == "Service":
            url = Urls.kube_base_url+"/api/v1/namespaces/master-ns/services"
        result = requests.post(url, json=json_str).text
        if result == False:  # TODO deliver error message
            print("Error in creating master, id:"+id)
        else:
            print("success")


@app.post("/lecture/{lecture_info}")
@validate
async def create_lecture(lecture_info: Dto.LectureModel, data_users_assigned):
    json_str = requests.get(
        Urls.base_url+"?lecture_id="+lecture_info.lecture_id).text
    data_users_assigned = list(json.loads(json_str))  # json to list[dict]

    studend_pod_infos = []
    for user in data_users_assigned:
        id = user.id
        json_num = yaml_to_json(id, False)
        for i in range(json_num):
            json_str = json.load(open(
                "./res/tmp%d.json" % i))
            if json_str['kind'] == "Pod":
                url = Urls.kube_base_url+"/api/v1/namespaces/slave-ns/pods"
            elif json_str['kind'] == "Service":
                url = Urls.kube_base_url+"/api/v1/namespaces/slave-ns/services"
            result = requests.post(url, json=json_str).text
            if result == False:  # TODO deliver error message
                print("Error in creating slave, id:"+id)
            else:
                print("success")
