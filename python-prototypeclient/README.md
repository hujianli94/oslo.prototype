#  Python bindings to the Prototype API

## 有keytone认证
```shell
cat > .prototype-openrc << EOF
export OS_AUTH_URL=http://172.22.180.123:5000/v3
export OS_USERNAME=prototype
export OS_PASSWORD=prototype
export OS_PROJECT_NAME=service
export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default
export OS_SERVICE_TYPE=prototype
export OS_ENDPOINT_TYPE=publicURL
export PROTOTYPE_API_VERSION=2
EOF
```

## 无keytone认证

```shell
export PROTOTYPE_URL=http://172.22.180.123:8778/v1
export OS_NO_CLIENT_AUTH=true
```