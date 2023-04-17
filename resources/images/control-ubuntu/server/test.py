import requests
import os
import json
import yaml
import base64
import res.Dto as Dto
import res.Urls as Urls
import datetime

data_lecture = [Dto.LectureModel(
    lecture_id=2110000001, title="프입", class_num=1, professor_id=9123)]
data_assignments = [Dto.AssignmentModel(assignment_id=1, lecture_id=2110000001, title="과제이름", start_date=datetime.datetime(
    2023, 4, 4, 10, 00, 00), due_date=datetime.datetime(2023, 4, 11, 23, 59, 59), description="첫번째 과제입니다.")]
data_professors = [Dto.UsersModel(id=0, user_id="ryann0", password="qwer123!", name="금나0", user_num=9123, role="교수"),
                   ]
data_steps = [Dto.StepModel(assignment_id=1, lecture_id=2110000001, user_id=1, step="진행중"),
              Dto.StepModel(assignment_id=1, lecture_id=2110000001,
                            user_id=2, step="채점중"),
              Dto.StepModel(assignment_id=1, lecture_id=2110000001, user_id=3, step="채점 완료"), ]
data_users_assigned = [Dto.UsersModel(id=1, user_id="ryann1", password="qwer123!",
                                      name="금나1", user_num=1914391, role="학생"),
                       Dto.UsersModel(id=2, user_id="ryann2", password="qwer123!",
                                      name="금나2", user_num=1914392, role="학생"),
                       Dto.UsersModel(id=3, user_id="ryann3", password="qwer123!",
                                      name="금나3", user_num=1914393, role="학생"), ]


def yaml_to_json(id, isProfessor):
    if isProfessor:
        role = "professor"
    else:
        role = "student"
    f = open("/Users/nkeum/github/MoaRoom-Infra-local/resources/images/control-ubuntu/server/res/deploy-%s-ubuntu.yml" % role, 'r')
    # apply envvar
    file = f.read().replace("{{ ID }}", str(id))
    contents = file.split("---")
    for i in range(len(contents)-1):
        with open("/Users/nkeum/github/MoaRoom-Infra-local/resources/images/control-ubuntu/server/res/tmp%d.yml" % i, "w") as tmp:
            tmp.write(contents[i])

    # convert yaml to json
    for i in range(len(contents)-1):
        with open("/Users/nkeum/github/MoaRoom-Infra-local/resources/images/control-ubuntu/server/res/tmp%d.yml" % i, 'r') as yaml_in, open("/Users/nkeum/github/MoaRoom-Infra-local/resources/images/control-ubuntu/server/res/tmp%d.json" % i, "w") as json_out:
            # yaml_object will be a list or a dict
            yaml_object = yaml.safe_load(yaml_in)
            json.dump(yaml_object, json_out)

    return len(contents)-1


def create_professor_res(professor_info: Dto.UsersModel):
    # id = 0, user_id = "ryann0", password = "qwer123!", name = "금나0", user_num = 9123, role = "교수"
    id = professor_info.id
    # if (professor_info.role != "교수"):
    #     return "Professor authentication failed. Please check the role and try again."

    json_num = yaml_to_json(id, True)

    for i in range(json_num):
        json_str = json.load(open(
            "/Users/nkeum/github/MoaRoom-Infra-local/resources/images/control-ubuntu/server/res/tmp%d.json" % i))
        if json_str['kind'] == "Pod":
            url = Urls.kube_base_url+"/api/v1/namespaces/professor-ns/pods"
        elif json_str['kind'] == "Service":
            url = Urls.kube_base_url+"/api/v1/namespaces/professor-ns/services"
        result = requests.post(url, json=json_str).text
        if result == False:
            print("Error in creating professor, id:"+id)
        else:
            print("success")  # TODO need api-parser!!


def create_lecture(lecture_info: Dto.LectureModel, data_users_assigned):
    # lecture_id=2110000001, title="프입", class_num=1, professor_id=9123

    # json_str = requests.get(
    #     Urls.base_url+"?lecture_id="+lecture_info.lecture_id).text
    # data_users_assigned = list(json.loads(json_str))  # json to list[dict]

    studend_pod_infos = []
    for user in data_users_assigned:
        id = user.id
        json_num = yaml_to_json(id, False)
        for i in range(json_num):
            json_str = json.load(open(
                "/Users/nkeum/github/MoaRoom-Infra-local/resources/images/control-ubuntu/server/res/tmp%d.json" % i))
            if json_str['kind'] == "Pod":
                url = Urls.kube_base_url+"/api/v1/namespaces/student-ns/pods"
            elif json_str['kind'] == "Service":
                url = Urls.kube_base_url+"/api/v1/namespaces/student-ns/services"
            result = requests.post(url, json=json_str).text
            if result == False:
                print("Error in creating student, id:"+id)
            else:
                print("success")  # TODO need api-parser!!

# create_professor_res(data_professors[0])
# create_lecture(data_lecture[0], data_users_assigned)
