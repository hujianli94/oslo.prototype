# coding=utf-8
"""
Views for RPC Test related functions.
"""

from prototype.api.views import base


class ViewBuilder(base.ViewBuilder):
    """OpenStack API View Builder for RPC Test."""

    def __init__(self):
        super(ViewBuilder, self).__init__()
        # 设置资源名称，build_base_response 会自动包装
        self._resource_name = "rpc_api"

    def show(self, request, rpc_api_data):
        """
        Build a view of the rpc test information.
        :param request: The WSGI request object.
        :param rpc_api_data: Dictionary containing system info or error data.
        :return: Formatted response dictionary.
        """
        # 使用基类的 _wrap_data 方法自动包装数据
        wrapped_data = self._wrap_data(rpc_api_data)
        return self.build_base_response(request, wrapped_data)
