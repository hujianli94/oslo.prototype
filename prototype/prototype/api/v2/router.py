#!/usr/bin/env python
# -*- coding: utf-8 -*-
from prototype.api.openstack import APIRouter as BaseAPIRouter
from prototype.api import extensions
from prototype.api.v2 import service as service_v2


class APIRouter(BaseAPIRouter):
    """Routes requests on the V2 API to the appropriate controller and method."""

    def __init__(self, ext_mgr=None):
        if ext_mgr is None:
            ext_mgr = extensions.ExtensionManager()

        # 调用父类的 __init__ 方法，传入有效的 ext_mgr
        super(APIRouter, self).__init__(ext_mgr)

    def _setup_routes(self, mapper, ext_mgr):
        """Setup routes for the v2 API."""
        # 创建控制器实例
        service_controller = service_v2.ServiceController()

        from prototype.api.openstack import wsgi as os_wsgi
        service_resource = os_wsgi.Resource(service_controller)

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

    @classmethod
    def factory(cls, global_config, **local_config):
        """Factory method for paste.deploy."""
        return cls()
