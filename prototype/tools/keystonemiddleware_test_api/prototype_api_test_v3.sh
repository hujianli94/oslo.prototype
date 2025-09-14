#!/bin/bash
# -*- coding: utf-8 -*-
# @Project Name : oslo.prototype
# @Author       : hjl
# @Time         : 2025/9/11 11:08
# @File         : curl_authtoken.sh
# @Software     : PyCharm
# @Description  : scripts function describe

# 设置变量
KEYSTONE_URL="http://172.22.180.123:5000/v3"
PROTOTYPE_API_URL="http://172.22.180.123:8778/v1/services"
USERNAME="prototype"
PASSWORD="prototype"
PROJECT_NAME="service"
DOMAIN_NAME="default"

# --- 修改点：改进 Token 获取逻辑 ---
# 获取 Token
# 使用 -D - 将响应头输出到 stderr，然后重定向到 stdout 以便 grep
# 使用 -o /dev/null 丢弃响应体
echo "Fetching token from Keystone..."
RESPONSE_HEADERS=$(mktemp) # 创建一个临时文件来存储响应头
curl -s -D "$RESPONSE_HEADERS" -o /dev/null \
  -H "Content-Type: application/json" \
  -d '{
  "auth": {
    "identity": {
      "methods": ["password"],
      "password": {
        "user": {
          "name": "'"$USERNAME"'",
          "domain": { "name": "'"$DOMAIN_NAME"'" },
          "password": "'"$PASSWORD"'"
        }
      }
    },
    "scope": {
      "project": {
        "name": "'"$PROJECT_NAME"'",
        "domain": { "name": "'"$DOMAIN_NAME"'" }
      }
    }
  }
}' \
  "$KEYSTONE_URL/auth/tokens"

# 从响应头文件中提取 Token
TOKEN=$(grep -i "X-Subject-Token:" "$RESPONSE_HEADERS" | awk '{print $2}' | tr -d '\r')

rm -f "$RESPONSE_HEADERS"

# 检查 Token 是否获取成功
if [ -z "$TOKEN" ]; then
  echo "Failed to retrieve token!"
  exit 1
fi

# 打印 Token
echo "Token: $TOKEN"
#
echo "Token retrieved successfully."

# 使用 Token 访问 Prototype API
echo "Accessing Prototype API..."
curl -i -X GET $PROTOTYPE_API_URL \
  -H "X-Auth-Token: $TOKEN"
