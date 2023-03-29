# This is executed by a cron job

import json
import requests

# 학생 api list가 있어서, 여기서 받은 거 다 내 디렉토리에 파일화함
#  ~/강의명/과제명/학번


dir_path = "/Users/nkeum/1914395"
url = "http://localhost:8001/files/L1VzZXJzL25rZXVtL3Rlc3Q="
json_str = requests.get(url).text
# json_str = "{\"2.py\": \"import os\\nimport json\\n\\n\\nprint(\\\"Hello World\\\")\\n\", \"1.txt\": \"sldkf\\nsadklfj\\ndsfksld\\nsdlkfjskd\\n\\n\"}"

# json to dict
result = json.loads(json.loads(json_str))

# write files
for filename, str in result.items():
    f = open(dir_path+"/"+filename, 'w')
    f.write(str)
    f.close()
