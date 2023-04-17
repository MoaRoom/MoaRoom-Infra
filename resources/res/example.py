import Dto
import datetime

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
assignment_id = 1
due_date = datetime.datetime(2023, 4, 11, 23, 59, 59)
