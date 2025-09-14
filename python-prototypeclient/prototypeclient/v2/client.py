# coding=utf-8
# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from prototypeclient.common import http
from prototypeclient.v2 import services


class Client(object):
    """Client for the Heat v2 API.

    :param string endpoint: A user-supplied endpoint URL for the prototype
                            service.
    :param string token: Token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    """

    def __init__(self, version, *args, **kwargs):
        """Initialize a new client for the Prototype API."""
        # 从kwargs中获取version参数
        version = kwargs.pop('version', '2')
        kwargs['api_version'] = version
        self.http_client = http._construct_http_client(*args, **kwargs)
        self.services = services.ServiceManager(self.http_client)
