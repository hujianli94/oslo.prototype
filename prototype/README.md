## 测试 服务端

```shell
# 初始化数据库
prototype-manage --config-file /etc/prototype/prototype.conf db sync

# 启动 api 服务
prototype-api --config-file /etc/prototype/prototype.conf

# 运行 worker 进程
prototype-worker --config-file /etc/prototype/prototype.conf
```

## 测试 SDK

版本和健康检查：

```shell
#根路径 / (版本发现)
#获取 API 支持的版本信息。
curl -i -X GET http://172.22.180.123:8778/

#健康检查 /healthcheck
#一个简单的健康检查端点。
curl -i -X GET http://172.22.180.123:8778/healthcheck
```

### API v1 测试

```shell
#1. GET /v1/services
# 列出所有服务
curl -i -X GET http://172.22.180.123:8778/v1/services
# -s 只提取响应体部分
curl -s -X GET http://172.22.180.123:8778/v1/services | python -m json.tool

#2. POST /v1/services
# 创建服务
curl -i -X POST http://172.22.180.123:8778/v1/services \
  -H "Content-Type: application/json" \
  -d '{"host": "compute01", "type": "compute", "topic": "worker"}'

#3. GET /v1/services/{service_id}
# 获取指定ID的服务详情
curl -i -X GET http://172.22.180.123:8778/v1/services/{service_id}
curl -s -X GET http://172.22.180.123:8778/v1/services/{service_id} | python -m json.tool

#4. PUT /v1/services/{service_id}
# 更新服务
curl -i -X PUT http://172.22.180.123:8778/v1/services/{service_id} \
  -H "Content-Type: application/json" \
  -d '{"service": {"disabled": true}}'
  
#5. DELETE /v1/services/{service_id}
# 删除服务
curl -i -X DELETE http://172.22.180.123:8778/v1/services/{service_id}

# 6. POST /v1/services/rpc_debug
# RPC调试接口
# 启动后端 prototype-worker 服务的 RPC 方法
# 先启动 worker 进程
prototype-worker --config-file /etc/prototype/prototype.conf
# 调用 rpc 方法
curl -i -X GET http://172.22.180.123:8778/v1/services/rpc_test
```

### API v2 测试

同上，只需将API版本号改为v2即可。

## 测试 keystone认证

设置 `auth_strategy = keystone` 后 启动 api 服务

```shell
bash tool/api_test/prototype_api_test_v3.sh
# 或者
python tool/api_test/prototype_api_test_v3.py
```

## 客户端使用示例

如果使用python-prototypeclient，可以使用以下命令：

```shell
# 安装客户端
pip install python-prototypeclient

# 设置环境变量
export OS_PROTOTYPE_URL=http://172.22.180.123:8778
export OS_PROTOTYPE_USERNAME=admin
export OS_PROTOTYPE_PASSWORD=password
export OS_PROTOTYPE_PROJECT_NAME=admin
export OS_PROTOTYPE_PROJECT_DOMAIN_NAME=Default
export OS_PROTOTYPE_USER_DOMAIN_NAME=Default

# 测试

# 列出所有服务
prototype service-list

# 创建服务
prototype service-create --host compute01 --type rpc --topic worker

# 显示服务详情
prototype service-show {service_id}

# 更新服务
prototype service-update {service_id} --disabled True
# 更新服务的 report_count
prototype service-update <service_id> --report-count 5
# 同时更新多个字段
prototype service-update <service_id> --report-count 3 --host compute01 --binary prototype-agent --type rpc --topic worker
# 查看服务详情确认更新
prototype service-show <service_id>

# 删除服务
prototype service-delete {service_id}

# 调用RPC调试接口
prototype service-rpc-debug
```

