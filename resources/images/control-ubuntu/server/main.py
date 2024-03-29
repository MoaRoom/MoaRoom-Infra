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
    "http://localhost:3000",  # for dev
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
    f = open(f"./res/remote-deploy-{role}.yml", 'r')
    ID = id

    # find webssh url's container port
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

    # find api url's container port
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

    # find api url's node port
    port_list = list(np.load("./res/port_list.npy"))
    # find available port
    for port_num in range(30002, 31000):
        # no pod assigned
        if port_list[port_num] == False:
            WEB_NODE_PORT = port_num
            port_list[port_num] = True
            np.save("./res/port_list.npy", port_list)
            break
        else:
            continue
    # find api url's node port
    port_list = list(np.load("./res/port_list.npy"))
    # find available port
    for port_num in range(31001, 32767):
        # no pod assigned
        if port_list[port_num] == False:
            APP_NODE_PORT = port_num
            port_list[port_num] = True
            np.save("./res/port_list.npy", port_list)
            break
        else:
            continue

    # apply env var
    file = f.read().replace("{{ ID }}", ID)
    file = file.replace("{ PORT }", str(PORT))
    file = file.replace("{ API_PORT }", str(API_PORT))
    file = file.replace("{ WEB_NODE_PORT }", str(WEB_NODE_PORT))
    file = file.replace("{ APP_NODE_PORT }", str(APP_NODE_PORT))

    contents = file.split("---")
    for i in range(len(contents)):
        with open(f"./res/tmp{i}.yml", "w") as tmp:
            tmp.write(contents[i])

    # convert yaml to json
    for i in range(len(contents)):
        with open(f"./res/tmp{i}.yml", 'r') as yaml_in, open(f"./res/tmp{i}.json", "w") as json_out:
            yaml_object = yaml.safe_load(yaml_in)
            json.dump(yaml_object, json_out)

    # object file num, ports
    return len(contents), WEB_NODE_PORT, APP_NODE_PORT, API_PORT


@app.post("/professor/")
# : Dto.UsersModel = None):
# dict = None):
async def create_professor_res(professor_info: Dto.UsersModel = None):
    id = professor_info.id

    json_num, PORT, API_PORT, _API_PORT = yaml_to_json(
        id, True)  # use nodePort for api

    for i in range(json_num):
        json_str = json.load(open(
            f"./res/tmp{i}.json"))
        if json_str['kind'] == "Pod":
            url = f"{Urls.kube_api_server}/api/v1/namespaces/professor-ns/pods"
        elif json_str['kind'] == "Service":
            url = f"{Urls.kube_api_server}/api/v1/namespaces/professor-ns/services"
        else:
            url = f"{Urls.kube_api_server}"
        headers = {"Authorization": f"Bearer {os.getenv('TOKEN')}",
                   'Accept': 'application/json', "Content-Type": "application/json"}
        result = requests.post(url, data=json.dumps(json_str),
                               headers=headers, verify=os.getenv('CACERT')).text
        if result == False:
            print(f"Error in creating professor, id: {id}")
            return 0

    print(f"Professor {id}'s node port is {PORT}, api node port id {API_PORT}")
    # url: webssh, api_url: internal api in k8s
    url = f"{Urls.kube_base_url}:{PORT}"
    api_url = f"{Urls.kube_base_url}:{API_PORT}"
    # professor has multiple lectures, lecture_id doesn't matter(-1)
    return Dto.URLModel(id=professor_info.user_id, lecture_id=professor_info.user_id, container_address=url, api_endpoint=api_url)


@app.post("/student/")
# Dto.UsersModel = None, lecture_id: str = None):
# student_info: Dto.UsersModel = None, lecture_id: str = None):
async def create_container(reqBody: dict = None):
    student_info = reqBody["student_info"]
    lecture_id = reqBody["lecture_id"]

    id = student_info["id"]
    pod_id = f"{id}-{lecture_id}"
    json_num, PORT, _API_PORT, API_PORT = yaml_to_json(
        pod_id, False)  # use containerPort for api
    for i in range(json_num):
        json_str = json.load(open(f"./res/tmp{i}.json"))
        if json_str['kind'] == "Pod":
            url = f"{Urls.kube_api_server}/api/v1/namespaces/student-ns/pods"
        elif json_str['kind'] == "Service":
            url = f"{Urls.kube_api_server}/api/v1/namespaces/student-ns/services"
        else:
            url = f"{Urls.kube_api_server}"
        headers = {"Authorization": f"Bearer {os.getenv('TOKEN')}",
                   'Accept': 'application/json', "Content-Type": "application/json"}
        result = requests.post(url, data=json.dumps(json_str),
                               headers=headers, verify=os.getenv('CACERT')).text
        if result == False:
            print(f"Error in creating student, id:{pod_id}")
            return 0
    print(f"Student {pod_id}'s port is {PORT}, api port id {API_PORT}")
    # url: webssh, api_url: internal api in k8s
    url = f"{Urls.kube_base_url}:{PORT}"
    api_url = f"http://student-{pod_id}-svc.student-ns.svc.cluster.local:{API_PORT}"
    return Dto.URLModel(id=student_info["user_id"], lecture_id=lecture_id, container_address=url, api_endpoint=api_url)
