# coding=utf-8
#    Copyright 2012 IBM Corp.
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

"""Client side of the conductor RPC API."""
import oslo_messaging as messaging
from oslo_log import log as logging
from prototype.common import rpc
from prototype.conf import CONF

LOG = logging.getLogger(__name__)


class ConductorAPI(object):
    """
    Client side of the console RPC API
    API version history:
    * 1.0 - Initial version.
    * 1.1 - Added migration_update
    """
    BASE_RPC_API_VERSION = '1.0'

    def __init__(self, topic=None):
        super(ConductorAPI, self).__init__(
            topic=topic or CONF.conductor_topic,
            default_version=self.BASE_RPC_API_VERSION)
        target = messaging.Target(topic=topic, version=self.BASE_RPC_API_VERSION)
        # 使用默认序列化器
        self.client = rpc.get_client(target)

    def test_service(self, ctxt):
        cctxt = self.client.prepare()
        ret = cctxt.call(ctxt, 'test_service')
        return ret
