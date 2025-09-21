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
from oslo_log import log as logging
import oslo_messaging as messaging
from oslo_service import periodic_task
from prototype.common import exception
from prototype.common import manager
from prototype.conf import CONF
from prototype.db.sqlalchemy import api as db_api

LOG = logging.getLogger(__name__)


class WorkerManager(manager.Manager):
    target = messaging.Target(version='1.0')

    def __init__(self, *args, **kwargs):
        super(WorkerManager, self).__init__(service_name='worker', *args, **kwargs)

    def init_host(self):
        """Hook to do additional manager initialization when one requests
        the service be started.  This is called before any service record
        is created.

        Child classes should override this method.
        """
        super(WorkerManager, self).init_host()
        LOG.info("WorkerManager.init_host called")

    def get_worker_info(self, context):
        """获取主机名、CPU 和内存信息"""
        LOG.debug("WorkerManager.get_worker_info called")
        try:
            hostname = platform.node()
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            memory = psutil.virtual_memory()
            memory_total_gb = round(memory.total / (1024 ** 3), 2)
            memory_available_gb = round(memory.available / (1024 ** 3), 2)
            memory_percent = memory.percent

            info = {
                "hostname": hostname,
                'os': platform.system(),
                'os_version': platform.release(),
                "cpu_count": cpu_count,
                'cpu_count_logical': cpu_count_logical,
                "memory_total_gb": memory_total_gb,
                "memory_available_gb": memory_available_gb,
                "memory_percent": memory_percent
            }
            # LOG.debug("Worker info collected: %s", info)
            return info
        except Exception as e:
            LOG.error("Failed to collect worker info: %s", e)
            raise exception.PrototypeException(message=str(e))

    @periodic_task.periodic_task(
        spacing=CONF.collection_interval,
        run_immediately=True)
    def _periodic_worker_task(self, context):
        """周期性任务，收集worker信息并写入数据库"""
        LOG.debug("================== Worker periodic task executed =================================")
        try:
            worker_info = self.get_worker_info(context)
            hostname = worker_info['hostname']

            # 尝试获取现有的WorkerNode记录
            existing_nodes = db_api.worker_node_get_all(context, filters={'hostname': hostname})

            if existing_nodes:
                # 如果存在现有记录，则更新它
                existing_node = existing_nodes[0]
                db_api.worker_node_update(context, existing_node['id'], worker_info)
            else:
                db_api.worker_node_create(context, worker_info)
        except Exception as e:
            LOG.error("Failed to save/update worker info to database: %s", e)
            raise exception.PrototypeException(message=str(e))

    # @periodic_task.periodic_task(spacing=3)
    # def _periodic_test_task(self, context):
    #     """周期性任务，每3秒执行一次"""
    #     LOG.debug("================== Test periodic task executed =================================")
