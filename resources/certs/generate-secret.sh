ROOT_CA=root-ca
NAME=student
NAMESPACE=student-ns

kubectl create -n $NAMESPACE secret tls $NAME-credential --key=$NAME.key --cert=$NAME.crt --dry-run=client -o yaml
