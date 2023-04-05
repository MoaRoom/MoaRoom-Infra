import os
import json


def read_files_from_dir(dir_path: str):
    returnDict = {}
    file_list = os.listdir(dir_path)
    print(file_list)
    for file in file_list:
        f = open(dir_path+"/"+file, "r")
        content = f.read()
        returnDict[file] = content
        f.close()
    return json.dumps(returnDict)


def make_dir(dir_path: str):
    # current_path = os.getcwd()  # 현재 경로 가지고오기
    # os.mkdir(current_path + "/" + folder_name2)  # 현재 경로 + 폴더명 입력
    # OR os.mkdir("../ThisIsNewFolder1")  # 한번 위로
    try:
        os.makedirs(dir_path)
        return True
    except:
        return False


# print(read_files_from_dir(
#     "/Users/nkeum/github/MoaRoom-Infra-local/resources/images/slave-ubuntu/server"))
# make_dir("/Users/nkeum/github/MoaRoom-Infra-local/resources/images/slave-ubuntu/server/testDir")
