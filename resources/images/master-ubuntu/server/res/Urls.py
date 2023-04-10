import os

base_url = os.getenv('BASE_URL')  # "http://"  # db server
slave_base_url = os.getenv('SLAVE_BASE_URL')  # "http://localhost:8001"
# slave_base_url = "http://slave-ubuntu-svc.slave-ns.svc.cluster.local:8001"

dir_path_slave = os.getenv('DIR_PATH_SLAVE')  # "/root/assignment"
dir_path_master = os.getenv('DIR_PATH_MASTER')  # "/Users/nkeum/test"
