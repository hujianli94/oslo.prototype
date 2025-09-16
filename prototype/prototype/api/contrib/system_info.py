# coding=utf-8
# prototype/api/contrib/system_info.py
"""System Info Extension."""

from prototype.api import extensions
from prototype.api.openstack import wsgi
from prototype.api.views import system_info as system_info_views
from prototype.worker import rpcapi
from oslo_context import context
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


# 定义扩展的基本信息
class System_info(extensions.ExtensionDescriptor):
    """System Info API support."""

    name = "SystemInfo"
    alias = "os-system-info"  # 扩展的别名，用于 URL 和标识
    namespace = ("http://docs.openstack.org/prototype/ext/"
                 "system_info/api/v2")
    updated = "2023-10-27T00:00:00+00:00"

    def get_resources(self):
        """Register the RESTful resources for this extension."""
        resources = []

        # 创建控制器实例
        controller = SystemInfoController()

        # 创建资源
        resource = extensions.ResourceExtension('system_info',
                                                controller,  # <-- 直接传递 controller 实例
                                                collection_actions={'index': 'GET'})  # 修正为字典
        # member_actions={'action': 'POST'} # 如果有成员动作也应为字典
        resources.append(resource)
        return resources


# 创建扩展的 Controller
class SystemInfoController(wsgi.Controller):
    """The System Info API controller for the OpenStack API."""

    def __init__(self):
        # 可以在这里初始化 ViewBuilder 或其他依赖
        self._view_builder_class = system_info_views.ViewBuilder
        # 初始化 RPC 客户端，用于调用 worker 服务
        self.worker_rpcapi = rpcapi.WorkerRPCAPI()
        super(SystemInfoController, self).__init__()

    def index(self, req):
        """Return system information."""
        # 获取上下文
        ctxt = context.get_admin_context()  # 或 req.environ['prototype.context'] 如果适用
        LOG.debug("Fetching system info via RPC...")
        try:
            # 通过 RPC 调用 worker 服务获取系统信息
            system_info_data = self.worker_rpcapi.get_system_info(ctxt)
            LOG.debug("Received system info: %s", system_info_data)
        except Exception as e:
            LOG.error("Failed to get system info: %s", e)
            # 返回错误信息
            system_info_data = {
                'error': 'Failed to retrieve system information',
                'message': str(e)
            }

        # 构建响应视图
        view_builder = self._view_builder_class()
        return view_builder.show(req, system_info_data)  # 假设 ViewBuilder.show 处理数据包装
