# coding=utf-8
# prototype/api/contrib/system_info.py
"""System Info Extension."""

from prototype.api import extensions
from prototype.api.openstack import wsgi
from prototype.api.views import worker_info as work_info_view
from prototype.worker import rpcapi
from oslo_context import context
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


# 定义扩展的基本信息
class Worker_info(extensions.ExtensionDescriptor):
    """
    Worker info API support.
    """

    name = "WorkerInfo"
    alias = "worker-info"  # 扩展的别名，用于 URL 和标识
    namespace = ("http://docs.openstack.org/prototype/ext/"
                 "worker_info/api/v2")
    updated = "2023-10-27T00:00:00+00:00"

    def get_resources(self):
        """Register the RESTful resources for this extension."""
        resources = []

        # 创建资源
        resource = extensions.ResourceExtension('worker_info',
                                                WorkerCollectionController(),
                                                collection_actions={'index': 'GET'})  # 修正为字典
        # member_actions={'action': 'POST'} # 如果有成员动作也应为字典
        resources.append(resource)
        return resources


# 创建扩展的 Controller
class WorkerCollectionController(wsgi.Controller):
    """
    Worker node collection API
    """

    def __init__(self):
        # 可以在这里初始化 ViewBuilder 或其他依赖
        self._view_builder_class = work_info_view.ViewBuilder
        # 初始化 RPC 客户端，用于调用 worker 服务
        self.worker_rpcapi = rpcapi.WorkerRPCAPI()
        super(WorkerCollectionController, self).__init__()

    def index(self, req):
        """Return system information."""
        # 获取上下文
        ctxt = context.get_admin_context()  # 或 req.environ['prototype.context'] 如果适用
        LOG.debug("Fetching system info via RPC...")
        try:
            # 通过 RPC 调用 worker 服务获取系统信息
            worker_info_data = self.worker_rpcapi.get_worker_info(ctxt)
            LOG.debug("Received system info: %s", worker_info_data)
        except Exception as e:
            LOG.error("Failed to get system info: %s", e)
            # 返回错误信息
            worker_info_data = {
                'error': 'Failed to retrieve system information',
                'message': str(e)
            }

        # 构建响应视图
        view_builder = self._view_builder_class()
        return view_builder.show(req, worker_info_data)
