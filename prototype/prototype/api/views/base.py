# coding=utf-8
"""
Base views for Prototype API.
"""

import time


class ViewBuilder(object):
    """Base class for Prototype API views."""

    def __init__(self):
        super(ViewBuilder, self).__init__()
        # 可以定义一个默认的资源名称，子类可以覆盖
        self._resource_name = None

    def _wrap_data(self, data):
        """
        将数据包装在资源名称键下。
        如果 _resource_name 未设置，则直接返回数据。
        :param data: 要包装的数据。
        :return: 包装后的数据字典或原始数据。
        """
        if self._resource_name:
            return {self._resource_name: data}
        return data

    def build_base_response(self, request, data, meta_dict=None):
        """
        构建一个基础的 API 响应结构。
        :param request: The WSGI request object.
        :param data: 包含主要数据的字典或对象。
        :param meta_dict: 可选的元数据字典。
        :return: 格式化的响应字典。
        """
        # 防御性检查，确保 request 和 api_version_request 存在
        api_version = "unknown"
        if request and hasattr(request, 'api_version_request'):
            try:
                api_version = request.api_version_request.get_string()
            except (AttributeError, TypeError):
                # 如果获取失败，使用默认值
                pass

        response = {
            "prototype": {
                "api_version": api_version,
                "timestamp": time.time(),
            },
            "data": data
        }
        if meta_dict:
            response["meta"] = meta_dict
        return response
