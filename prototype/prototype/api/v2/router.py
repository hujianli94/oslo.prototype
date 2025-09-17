#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prototype.api.openstack import APIRouter as BaseAPIRouter
from prototype.api import extensions
from prototype.common.i18n import _
from prototype.api.v2 import service as service_v2
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class APIRouter(BaseAPIRouter):
    """Routes requests on the V2 API to the appropriate controller and method."""

    def __init__(self, ext_mgr=None):
        if ext_mgr is None:
            ext_mgr = extensions.ExtensionManager()

        # 调用父类的 __init__ 方法，传入有效的 ext_mgr
        super(APIRouter, self).__init__(ext_mgr)

    # --- 保持方法签名与基类一致 ---
    def _setup_routes(self, mapper, ext_mgr):
        """Setup routes for the v2 API."""
        LOG.info(_("Setting up standard V2 routes using mapper.resource..."))
        # 创建控制器实例
        service_controller = service_v2.ServiceController()

        # 使用Resource包装控制器，确保正确处理响应
        from prototype.api.openstack import wsgi as os_wsgi
        service_resource = os_wsgi.Resource(service_controller)

        # --- 使用 mapper.resource 注册服务相关路由 ---
        mapper.resource("service",  # member_name - 通常为单数
                        "services",  # collection_name - 通常为复数，也是URL路径的一部分
                        controller=service_resource)
        LOG.info(_("Standard V2 routes setup using mapper.resource complete."))

    @classmethod
    def factory(cls, global_config, **local_config):
        """Factory method for paste.deploy."""
        LOG.info(_("Creating APIRouter from factory..."))
        return cls()
