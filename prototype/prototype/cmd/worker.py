# coding=utf-8
# Copyright (c) 2010 OpenStack Foundation
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

"""Starter script for Prototype Console Proxy."""
import os
import sys

from oslo_log import log as logging
from prototype.conf import CONF
from prototype.common import service
from prototype.common import utils
from prototype.common import rpc
from prototype.conf import CONF
from prototype import version


def main():
    CONF(sys.argv[1:], project='prototype',
         version=version.version_string())
    logdir = CONF.log_dir
    is_exists = os.path.exists(logdir)
    if not is_exists:
        os.makedirs(logdir)
    logging.setup(CONF, "prototype")
    utils.monkey_patch()

    rpc.init(CONF)

    # 使用 serve 启动方式
    # server = service.Service.create(binary="prototype-worker", topic=CONF.worker_topic)
    # service.serve(server)
    # service.wait()

    # 使用 launch_service 启动方式
    launcher = service.get_launcher()
    server = service.Service.create(binary="prototype-worker", topic=CONF.worker_topic)
    launcher.launch_service(server)
    launcher.wait()


if __name__ == '__main__':
    main()
