#!/usr/bin/python3
# This file is executed by a cron job
import json
import requests
import sys
import res.Dto as Dto
import res.Urls as Urls
import base64

assignment_id = sys.argv[1]
json_str = requests.get(
    Urls.base_url+"/assignments/"+assignment_id+"/urls").text
data_users_assigned = list(json.loads(json_str))  # json to list[dict]

dir_path = Urls.dir_path_professor
dir_path_student = Urls.dir_path_student

for user in data_users_assigned:
    # mkdir in student
    encoded_dir_path_student = base64.b64encode((
        dir_path_student+"/"+assignment_id).encode('ascii')).decode('ascii')  # base64 encode
    urlmodel = json.loads(requests.get(
        Urls.base_url+"/urls/"+user["id"]).text)
    url = urlmodel["apiEndpoint"]+"/files/" + encoded_dir_path_student
    json_str = requests.get(url).text
    # json to dict
    result = json.loads(json.loads(json_str))

    # write files
    for filename, content in result.items():
        assignment_dir_path = "%s/%s/%s/%s" % (
            dir_path, assignment_id, user["id"], filename)
        f = open(assignment_dir_path, 'w')
        f.write(content)
        f.close()
