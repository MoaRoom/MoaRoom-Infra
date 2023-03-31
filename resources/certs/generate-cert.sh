ROOT_CA=root-ca
NAME=student

# generate self-signed root cacert and private key
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:4096 -subj '/O=example Inc./CN=example.com' -keyout $ROOT_CA.key -out $ROOT_CA.crt

# generate private key and csr of artiference
openssl req -out $NAME.csr -newkey rsa:4096 -nodes -keyout $NAME.key -subj "/CN=student/O=student/C=KR"

# generate cert of artiference
openssl x509 -req -days 365 -CA $ROOT_CA.crt -CAkey $ROOT_CA.key -set_serial 0 -in $NAME.csr -out $NAME.crt -extfile domains.ext
openssl x509 -req -days 365 -CA $ROOT_CA.crt -CAkey $ROOT_CA.key -CAcreateserial -in $NAME.csr -out $NAME.crt -extfile domains.ext

cat $ROOT_CA.crt > $ROOT_CA.pem