from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
import base64


app = FastAPI()


@app.get("/files/")
async def read_files_from_dir(dir_path: str = None):
    # base64 decoded
    decoded_dir_path = base64.b64decode(dir_path).decode('ascii')
    returnDict = {}
    file_list = os.listdir(decoded_dir_path)
    for file in file_list:
        f = open(decoded_dir_path+"/"+file, "r")
        content = f.read()
        returnDict[file] = content
        f.close()
    return json.dumps(returnDict)


@app.post("/mkdir/")
async def make_dir(dir_name: str = None):
    # base64 decoded
    decoded_dir_name = base64.b64decode(dir_name).decode('ascii')
    print("decoded_dir_name: %s" % decoded_dir_name)
    try:
        os.makedirs(decoded_dir_name)
        return True
    except:
        return False
