#!/usr/bin/python3
# This file is executed by a cron job
import json
import requests
import sys
import res.Dto as Dto
import res.Urls as Urls
import base64

assignment_id = sys.argv[1]
# json_str = requests.get(Urls.base_url+"?assignment_id="+assignment_id).text
# data_users_assigned = list(json.loads(json_str))  # json to list[dict]
data_users_assigned = [Dto.UsersModel(id=1, user_id="ryann1", password="qwer123!",
                                      name="금나1", user_num=1914391, role="학생"),
                       Dto.UsersModel(id=2, user_id="ryann2", password="qwer123!",
                                      name="금나2", user_num=1914392, role="학생"),
                       Dto.UsersModel(id=3, user_id="ryann3", password="qwer123!",
                                      name="금나3", user_num=1914393, role="학생"), ]

dir_path = Urls.dir_path_professor
dir_path_student = Urls.dir_path_student

for user in data_users_assigned:
    # mkdir in student
    encoded_dir_path_student = base64.b64encode((
        dir_path_student+"/"+str(assignment_id)).encode('ascii')).decode('ascii')  # base64 encode
    url = Urls.student_base_url+"/files/"+encoded_dir_path_student
    json_str = requests.get(url).text
    # json to dict
    result = json.loads(json.loads(json_str))

    # write files
    for filename, content in result.items():
        assignment_dir_path = "%s/%s/%d/%s" % (
            dir_path, assignment_id, user.id, filename)
        f = open(assignment_dir_path, 'w')
        f.write(content)
        f.close()
