# coding=utf-8
# prototype/api/views/system_info.py
"""Views for System Info related functions."""

from prototype.api.views import base


class ViewBuilder(base.ViewBuilder):
    """OpenStack API View Builder for System Info."""

    def __init__(self):
        super(ViewBuilder, self).__init__()
        # 设置资源名称，基类的 _wrap_data 会用到
        self._resource_name = "worker_info"

    def show(self, request, worker_info_data):
        """
        Build a view of the system information.
        :param request: The WSGI request object.
        :param worker_info_data: The worker_info_data
        :return: Formatted response dictionary.
        """
        # 使用基类的 _wrap_data 方法自动包装数据
        # 如果 worker_info_data 是 {'cpu': '...'}, 结果会是 {'worker_info': {'cpu': '...'}}
        # 如果 worker_info_data 包含错误信息，也会被包装
        wrapped_data = self._wrap_data(worker_info_data)
        # 使用基类的 build_base_response 构建基础响应结构
        return self.build_base_response(request, wrapped_data)
