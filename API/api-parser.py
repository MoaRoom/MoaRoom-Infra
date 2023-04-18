import pandas as pd
import numpy as np
import requests
import json
import res.Dto as Dto

host_dns = "localhost"
host_port = 8080
namespace = "student-ns"

# dir_path = "/Users/nkeum/github/MoaRoom-Infra-local/API/pod-list.json"
# json_str = open(dir_path, 'r').read()

url = "http://%s:%d/api/v1/namespaces/%s/pods" % (
    host_dns, host_port, namespace)
json_str = requests.get(url).text
data = json.loads(json_str)
all_pods = data['items']
pods = []
for i in range(len(all_pods)):
    all_containers = all_pods[i]['spec']['containers']
    containers = []
    for j in range(len(all_containers)):
        all_ports = all_containers[j]['ports']
        ports = []
        for k in range(len(all_ports)):
            ports.append(Dto.PortModel(name=all_ports[k]['name'],
                                       containerPort=all_ports[k]['containerPort'],
                                       protocol=all_ports[k]['protocol']))
        containers.append(Dto.ContainerModel(name=all_containers[j]['name'],
                                             image=all_containers[j]['image'],
                                             ports=ports))
    pods.append(Dto.PodModel(
        name=all_pods[i]['metadata']['name'],
        namespace=all_pods[i]['metadata']['namespace'],
        containers=containers,
        status_phase=all_pods[i]['status']['phase'],
        hostIP=all_pods[i]['status']['hostIP'],
        podIP=all_pods[i]['status']['podIP']))
print(pods)
