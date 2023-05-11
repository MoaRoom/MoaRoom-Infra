# Kubernetes의 API Server에 접근(GET/POST)

## ✅ Kuberentes proxy 서버를 노출

```bash
> k cluster-info
Kubernetes control plane is running at https://kubernetes.docker.internal:6443
CoreDNS is running at https://kubernetes.docker.internal:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

```bash
k proxy --port=8080 &
```

## ✅ 환경변수 설정

```
# Point to the internal API server hostname
APISERVER=https://kubernetes.default.svc

# Path to ServiceAccount token
SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount

# Read this Pod's namespace
NAMESPACE=$(cat ${SERVICEACCOUNT}/namespace)

# Read the ServiceAccount bearer token
TOKEN=$(cat ${SERVICEACCOUNT}/token)

# Reference the internal certificate authority (CA)
CACERT=${SERVICEACCOUNT}/ca.crt
```

## ✅ API Authentication(using Python)

```python
import os
import requests

headers = {
    'Authorization': 'Bearer ' + os.getenv('TOKEN', ''),
    'Content-Type': 'application/x-www-form-urlencoded',
}

with open('tmp0.json') as f:
    data = f.read().replace('\n', '').replace('\r', '').encode()

response = requests.post(
    'http://' + os.getenv('APISERVER', '') + '/api/v1/namespaces/student-ns/pods',
    headers=headers,
    data=data,
    verify=os.getenv('CACERT', ''),
)
```

### ex) API로 Pod 리스트

```bash
curl -v -k -X GET http://localhost:8080/api/v1/namespaces/test/pods
```

- GET 방식의 경우 auth 인증 딱히 필요 없음
- `./pod-list.json` 확인

### ex) API로 POD 생성하기

→ curl http://localhost:8080에 접속하면 apiserver가 뜸

- yaml을 json으로 변환

```bash
│ File: nginx-pod.json
───────┼──────────────────────────────────────────────────
   1   │ {
   2   │     "apiVersion": "v1",
   3   │     "kind": "Pod",
   4   │     "metadata": {
   5   │         "name": "nginx-test"
   6   │     },
   7   │     "spec": {
   8   │         "containers": [
   9   │             {
  10   │                 "name": "nginx",
  11   │                 "image": "nginx:1.7.9",
  12   │                 "ports": [
  13   │                     {
  14   │                         "containerPort": 80
  15   │                     }
  16   │                 ]
  17   │             }
  18   │         ]
  19   │     }
  20   │ }
```

- api server로 POST 날림

```bash
curl -k -v POST -H "Content-Type: application/json"  http://127.0.0.1:8080/api/v1/namespaces/test/pods -d@nginx-pod.json
```

secure 쓸 거면 권한 관련 [링크](https://coffeewhale.com/apiserver)

삭제, watch, 특정 pod 확인, pod 로그 읽기, pod 삭제 등등의 api는 처음 [링크](https://coffeewhale.com/apiserver) 및 공식 api 문서 참조
