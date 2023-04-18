# Follow the steps to set a certification

1. Edit **IP.1** of **domains.ext** to your server's gateway node IP address
2. Edit **NAME** of **generate-cert.sh**
3. Execute **generate-cert.sh**. Then, csrs, keys, crts for k8s will be generated.
4. Edit **NAME** of **generate-secret.sh**
5. Edit **NAMESPACE** for **generate-secret.sh**
6. Execute **generated-secret.sh**
7. **Copy the first yaml's tls.key and tls.crt** of the printed text, and **paste it** to tls.crt, tls.crt(should be replaced)
8. **Copy the entire second and third yaml** of the printed text, **replace** the root-ca.
<!-- 9. Copy and paste generated crt and key file to web's certs folder -->

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: professor-credential
  namespace: professor-ns
type: kubernetes.io/tls
data:
  tls.crt: READACTED
  tls.key: READACTED
```
