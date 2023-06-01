import os

kube_api_server = os.getenv('APISERVER')  # https://kubernetes.default.svc
kube_base_url = os.getenv('KUBE_BASE_URL')  # http://172... ## 8080

base_url = os.getenv('BASE_URL')  # "http://moaroom-back.duckdns.org:8080"
student_base_url = os.getenv('STUDENT_BASE_URL')  # "http://localhost:8001"
# student_base_url = "http://student-ubuntu-svc.student-ns.svc.cluster.local:8001"

dir_path_student = os.getenv('DIR_PATH_STUDENT')  # "/root/assignment"
dir_path_professor = os.getenv('DIR_PATH_PROFESSOR')  # "/root/assignment"
