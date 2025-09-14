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

import platform
import psutil
from oslo_config import cfg
import oslo_messaging as messaging

from prototype.common import service
from oslo_log import log as logging
from prototype.common.service import periodic_task

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class WorkerManager(service.Manager):
    target = messaging.Target(version='2.0')

    def __init__(self, *args, **kwargs):
        super(WorkerManager, self).__init__(service_name='worker', *args, **kwargs)

    def init_host(self):
        from prototype import db
        from oslo_context import context
        ctxt = context.get_admin_context()
        LOG.info("init worker")

    def debug(self, context):
        return 'debug! this is a debug message'

    def get_system_info(self, context):
        """获取主机名、CPU 和内存信息"""
        try:
            hostname = platform.node()
            cpu_count = psutil.cpu_count(logical=True)
            memory = psutil.virtual_memory()
            memory_total_gb = round(memory.total / (1024 ** 3), 2)
            memory_available_gb = round(memory.available / (1024 ** 3), 2)
            memory_percent = memory.percent

            system_info = {
                "hostname": hostname,
                "cpu_count": cpu_count,
                "memory_total_gb": memory_total_gb,
                "memory_available_gb": memory_available_gb,
                "memory_percent": memory_percent
            }
            LOG.debug("System info retrieved: %s", system_info)
            return system_info
        except Exception as e:
            LOG.error("Failed to retrieve system info: %s", e)
            return None

    @periodic_task.periodic_task(spacing=60, run_immediately=True)
    def _periodic_worker_task(self, context):
        """周期性任务，确保服务保持运行状态"""
        LOG.debug("Worker periodic task executed")
