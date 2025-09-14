#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prototype.api.openstack import APIRouter as BaseAPIRouter
from prototype.api import extensions
from prototype.api.v1 import service as service_v1
from prototype.api.v1 import rpc_test as rpc_test_v1


class APIRouter(BaseAPIRouter):
    """Routes requests on the V1 API to the appropriate controller and method."""

    def __init__(self, ext_mgr=None):
        if ext_mgr is None:
            ext_mgr = extensions.ExtensionManager()

        # 调用父类的 __init__ 方法，传入有效的 ext_mgr
        super(APIRouter, self).__init__(ext_mgr)

    def _setup_routes(self, mapper, ext_mgr):
        """Setup routes for the v1 API."""
        # 创建控制器实例
        service_controller = service_v1.ServiceController()
        # 创建 RpcTestController 实例
        rpc_test_controller = rpc_test_v1.RpcTestController()

        # 使用Resource包装控制器，确保正确处理响应
        from prototype.api.openstack import wsgi as os_wsgi
        service_resource = os_wsgi.Resource(service_controller)
        # 为 RpcTestController 创建 Resource
        rpc_test_resource = os_wsgi.Resource(rpc_test_controller)

        # 注册服务相关路由
        mapper.connect("/services",
                       controller=service_resource,
                       action='index',
                       conditions={"method": ["GET"]})
        mapper.connect("/services",
                       controller=service_resource,
                       action='create',
                       conditions={"method": ["POST"]})
        mapper.connect("/services/{id}",
                       controller=service_resource,
                       action='show',
                       conditions={"method": ["GET"]})
        mapper.connect("/services/{id}",
                       controller=service_resource,
                       action='update',
                       conditions={"method": ["PUT"]})
        mapper.connect("/services/{id}",
                       controller=service_resource,
                       action='delete',
                       conditions={"method": ["DELETE"]})
        mapper.connect("/services/rpc_test",
                       controller=rpc_test_resource,
                       action='rpc_test',
                       conditions={"method": ["GET"]})

    @classmethod
    def factory(cls, global_config, **local_config):
        """Factory method for paste.deploy."""
        return cls()
