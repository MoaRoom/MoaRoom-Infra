#!/usr/bin/python3
import os
import base64
import res.Dto as Dto
import res.Urls as Urls
import datetime
import requests
import base64


data_lecture = [Dto.LectureModel(
    lecture_id=2110000001, title="프입", class_num=1, professor_id=9123)]
data_assignments = [Dto.AssignmentModel(assignment_id=1, lecture_id=2110000001, title="과제이름", start_date=datetime.datetime(
    2023, 4, 4, 10, 00, 00), due_date=datetime.datetime(2023, 4, 11, 23, 59, 59), description="첫번째 과제입니다.")]
data_users = [Dto.UsersModel(id=0, user_id="ryann0", password="qwer123!", name="금나0", user_num=9123, role="교수"),
              Dto.UsersModel(id=1, user_id="ryann1", password="qwer123!",
                             name="금나1", user_num=1914391, role="학생"),
              Dto.UsersModel(id=2, user_id="ryann2", password="qwer123!",
                             name="금나2", user_num=1914392, role="학생"),
              Dto.UsersModel(id=3, user_id="ryann3", password="qwer123!", name="금나3", user_num=1914393, role="학생"), ]
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


def schedule_cronjob(dt, assignment_id):
    month, day, hour, minute = dt.month, dt.day, dt.hour, dt.minute
    os.system('/bin/bash %s/cronjob.sh %d %d %d %d %d' %
              (os.path.dirname(os.path.realpath(__file__)), minute, hour, day, month, assignment_id))


def create_directories(assignment_id, data_users_assigned):
    dir_path_slave = Urls.dir_path_slave
    dir_path_master = Urls.dir_path_master
    for user in data_users_assigned:
        # mkdir in slave
        encoded_dir_path_slave = base64.b64encode((
            dir_path_slave+"/"+str(assignment_id)).encode('ascii')).decode('ascii')  # base64 encode
        # slave_base_url이 slave마다 다른 점 어떻게 할지
        url = Urls.slave_base_url+"/mkdir/"+encoded_dir_path_slave
        result = requests.post(url).text
        if result == False:
            print("Error in mkdir, uid:"+user.id)

        # mkdir in master
        os.makedirs("%s/%s/%s" % (dir_path_master, assignment_id, user.id))


def create_assignment():
    assignment_id = 1
    data_users_assigned = [Dto.UsersModel(id=1, user_id="ryann1", password="qwer123!",
                                          name="금나1", user_num=1914391, role="학생"),
                           Dto.UsersModel(id=2, user_id="ryann2", password="qwer123!",
                                          name="금나2", user_num=1914392, role="학생"),
                           Dto.UsersModel(id=3, user_id="ryann3", password="qwer123!",
                                          name="금나3", user_num=1914393, role="학생"), ]
    due_date = datetime.datetime(2023, 4, 11, 23, 59, 59)

    # mkdir
    create_directories(assignment_id, data_users_assigned)

    # cron
    schedule_cronjob(due_date, assignment_id)


create_assignment()
