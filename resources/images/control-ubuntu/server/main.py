#!/usr/bin/python3
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import yaml
import res.Dto as Dto
import res.Urls as Urls
import numpy as np

app = FastAPI()

# CORS
origins = [
    "http://moaroom-front.duckdns.org:3000",
    "http://moaroom-back.duckdns.org:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def yaml_to_json(id, isProfessor):
    if isProfessor:
        role = "professor"
    else:
        role = "student"
    f = open("./res/remote-deploy-%s.yml" % role, 'r')
    ID = id

    port_list = list(np.load("./res/port_list.npy"))
    # find available port
    for port_num in range(8887, len(port_list)):
        # no pod assigned
        if port_list[port_num] == False:
            PORT = port_num
            port_list[port_num] = True
            np.save("./res/port_list.npy", port_list)
            break
        else:
            continue

    # find api url's port
    port_list = list(np.load("./res/port_list.npy"))
    # find available port
    for port_num in range(8004, 8887):
        # no pod assigned
        if port_list[port_num] == False:
            API_PORT = port_num
            port_list[port_num] = True
            np.save("./res/port_list.npy", port_list)
            break
        else:
            continue

    # apply env var
    file = f.read().replace("{{ ID }}", ID)
    file = file.replace("{ PORT }", str(PORT))
    file = file.replace("{ API_PORT }", str(API_PORT))
    contents = file.split("---")
    for i in range(len(contents)):
        with open("./res/tmp%d.yml" % i, "w") as tmp:
            tmp.write(contents[i])

    # convert yaml to json
    for i in range(len(contents)):
        with open("./res/tmp%d.yml" % i, 'r') as yaml_in, open("./res/tmp%d.json" % i, "w") as json_out:
            yaml_object = yaml.safe_load(yaml_in)
            json.dump(yaml_object, json_out)

    return len(contents), PORT, API_PORT  # object file num, port


@app.post("/professor/")
# : Dto.UsersModel = None):
# dict = None):
async def create_professor_res(professor_info: Dto.UsersModel = None):
    id = professor_info.id

    json_num, PORT, API_PORT = yaml_to_json(id, True)

    for i in range(json_num):
        json_str = json.load(open(
            "./res/tmp%d.json" % i))
        if json_str['kind'] == "Pod":
            url = Urls.kube_api_server+"/api/v1/namespaces/professor-ns/pods"
        elif json_str['kind'] == "Service":
            url = Urls.kube_api_server+"/api/v1/namespaces/professor-ns/services"
        headers = {"Authorization": "Bearer %s" % (os.getenv('TOKEN')),
                   'Accept': 'application/json', "Content-Type": "application/json"}
        result = requests.post(url, data=json.dumps(json_str),
                               headers=headers, verify=os.getenv('CACERT')).text
        if result == False:
            print("Error in creating professor, id:"+id)
            return 0

    print("Professor %s's port is %d, api port id %d" %
          (id, PORT, API_PORT))
    # url: webssh, api_url: internal api in k8s
    url = Urls.kube_base_url+":%d" % PORT
    api_url = Urls.kube_base_url+":%d" % API_PORT
    # professor has multiple lectures, lecture_id doesn't matter(-1)
    return Dto.URLModel(id=professor_info.user_id, lecture_id=professor_info.user_id, container_address=url, api_endpoint=api_url)


# **deprecated**
@app.post("/lecture/")
# Dto.LectureModel = None):
# : dict = None):
async def create_lecture(lecture_info: Dto.LectureModel = None):
    json_str = requests.get(
        Urls.base_url+"?lecture_id="+lecture_info.lecture_id).text
    data_users_assigned = list(json.loads(json_str))  # json to list[dict]

    student_pod_infos = []
    for user in data_users_assigned:
        id = user["id"]
        lecture_id = lecture_info.lecture_id
        json_num, PORT, API_PORT = yaml_to_json(
            id+"-"+lecture_id, False)  # no api port for student
        for i in range(json_num):
            json_str = json.load(open("./res/tmp%d.json" % i))
            if json_str['kind'] == "Pod":
                url = Urls.kube_api_server+"/api/v1/namespaces/student-ns/pods"
            elif json_str['kind'] == "Service":
                url = Urls.kube_api_server+"/api/v1/namespaces/student-ns/services"
            headers = {"Authorization": "Bearer %s" % (os.getenv('TOKEN')),
                       'Accept': 'application/json', "Content-Type": "application/json"}
            result = requests.post(url, data=json.dumps(json_str),
                                   headers=headers, verify=os.getenv('CACERT')).text
            if result == False:
                print("Error in creating student, id:"+id)
            else:
                student_pod_infos.append(
                    Dto.URLModel(id=id, lecture_id=lecture_id, container_address=Urls.kube_base_url+":%d" % PORT, api_endpoint=str(API_PORT)))
                print("Student %s's port is %d" %
                      (id, PORT))
    return student_pod_infos
# **deprecated**


@app.post("/student/")
# Dto.UsersModel = None, lecture_id: str = None):
# student_info: Dto.UsersModel = None, lecture_id: str = None):
async def create_container(reqBody: dict = None):
    student_info = reqBody["student_info"]
    lecture_id = reqBody["lecture_id"]

    id = student_info["id"]
    pod_id = id+"-"+lecture_id
    json_num, PORT, API_PORT = yaml_to_json(pod_id, False)
    for i in range(json_num):
        json_str = json.load(open("./res/tmp%d.json" % i))
        if json_str['kind'] == "Pod":
            url = Urls.kube_api_server+"/api/v1/namespaces/student-ns/pods"
        elif json_str['kind'] == "Service":
            url = Urls.kube_api_server+"/api/v1/namespaces/student-ns/services"
        headers = {"Authorization": "Bearer %s" % (os.getenv('TOKEN')),
                   'Accept': 'application/json', "Content-Type": "application/json"}
        result = requests.post(url, data=json.dumps(json_str),
                               headers=headers, verify=os.getenv('CACERT')).text
        if result == False:
            print("Error in creating student, id:"+pod_id)
            return 0
    print("Student %s's port is %d, api port id %d" %
          (pod_id, PORT, API_PORT))
    # url: webssh, api_url: internal api in k8s
    url = Urls.kube_base_url+":%d" % PORT
    api_url = "http://student-%s-svc.student-ns.svc.cluster.local:%d" % (
        pod_id, API_PORT)
    return Dto.URLModel(id=student_info["user_id"], lecture_id=lecture_id, container_address=url, api_endpoint=api_url)
