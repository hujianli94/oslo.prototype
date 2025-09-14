#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright: (c)  : @Time 2025/9/11 13  @Author  : hjl
# @Site    : 
# @File    : prototype_api_test_v3.py
# @Project: oslo.prototype
# @Software: PyCharm
# @Desc    :
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import json
import requests
import urllib3

urllib3.disable_warnings()

data_v3 = {
    "auth": {
        "identity": {
            "methods": ["password"],
            "password": {
                "user": {
                    "domain": {
                        "name": "default"
                    },
                    "name": "prototype",
                    "password": "prototype"
                }
            }
        },
        "scope": {
            "project": {
                "domain": {
                    "name": "default"
                },
                "name": "service"
            }
        }
    }
}
tokens_url = "http://172.22.180.123:5000/v3/auth/tokens?nocatalog"
identity_res = requests.post(tokens_url, verify=False, json=data_v3)
# print(identity_res.status_code)
# print(identity_res.text)
token_id = identity_res.headers.get("X-Subject-Token")
print(token_id)

PROTOTYPE_API_URL = "http://172.22.180.123:8778/v1/services"
identity_res = requests.post(PROTOTYPE_API_URL, headers={"X-Auth-Token": token_id})
print(identity_res.status_code)
print(identity_res.text)
