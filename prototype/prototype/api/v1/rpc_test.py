#!/usr/bin/env python
# -*- coding: utf-8 -*-
from prototype.api.openstack import wsgi
# 导入专用的视图构建器
from prototype.api.views import rpc_test as rpc_test_views
from prototype.worker import rpcapi
from oslo_context import context
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class RpcTestController(wsgi.Controller):
    def __init__(self):
        # 使用专用的视图构建器
        self._view_builder_class = rpc_test_views.ViewBuilder
        super(RpcTestController, self).__init__()

    def rpc_test(self, req):
        """调用 RPC 获取 Worker 服务的系统信息"""
        ctxt = context.get_admin_context()
        try:
            worker_rpcapi = rpcapi.WorkerRPCAPI()
            # 调用 Worker 的 get_worker_info 方法
            system_info = worker_rpcapi.get_worker_info(ctxt)
            view_builder = self._view_builder_class()
            # 调用视图构建器的 show 方法
            result = view_builder.show(req, system_info)
            return result
        except Exception as e:
            LOG.error("Error calling rpc_test: %s" % e)
            error_data = {
                "error": "RPC call failed",
                "details": str(e)
            }
            view_builder = self._view_builder_class()
            result = view_builder.show(req, error_data)
            return result
