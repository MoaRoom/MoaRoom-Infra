from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import base64

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


@app.post("/mkdir/{dir_name}")
async def make_dir(dir_name: str = None):
    # base64 decoded
    decoded_dir_name = base64.b64decode(dir_name).decode('ascii')
    print("decoded_dir_name: %s" % decoded_dir_name)
    try:
        os.makedirs(decoded_dir_name)
        return True
    except:
        return False


@app.get("/files/{dir_path}")
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
