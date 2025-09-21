#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prototype.api.openstack import wsgi
from prototype.api.views import service as service_views
from oslo_context import context
from prototype import db
from oslo_log import log as logging
import webob

LOG = logging.getLogger(__name__)


class ServiceController(wsgi.Controller):
    def __init__(self):
        self._view_builder_class = service_views.ViewBuilder
        super(ServiceController, self).__init__()

    def index(self, req):
        """获取所有服务列表"""
        ctxt = context.get_admin_context()
        services = db.service_get_all(ctxt)
        service_data = {
            "services": services,
            "count": len(services),
            "version": "v2"
        }
        view_builder = self._view_builder_class()
        result = view_builder.list(req, service_data)
        return result

    def show(self, req, id):
        """获取指定ID的服务详情"""
        ctxt = context.get_admin_context()
        try:
            service = db.service_get(ctxt, id)
            view_builder = self._view_builder_class()
            return view_builder.show(req, service)
        except Exception as e:
            service_data = {
                "error": "Service not found",
                "service_id": id,
                "version": "v2"
            }
            view_builder = self._view_builder_class()
            result = view_builder.show(req, service_data)
            return result

    def create(self, req, body=None):
        """创建新服务"""
        # LOG.debug("Raw request body: %s", req.body)
        # LOG.debug("Parsed body parameter: %s", body)
        ctxt = context.get_admin_context()
        # 处理两种可能的数据格式
        if body and isinstance(body, dict):
            # 首先检查是否是嵌套格式 { "service": { ... } }
            if "service" in body and isinstance(body["service"], dict):
                service_data = body["service"]
            else:
                service_data = body
        else:
            service_data = {}

        # LOG.debug("Extracted service data: %s", service_data)

        # 设置默认值
        if "host" not in service_data:
            service_data["host"] = "localhost"
        if "type" not in service_data:
            service_data["type"] = "compute"
        if "topic" not in service_data:
            service_data["topic"] = "prototype"
        if "report_count" not in service_data:
            service_data["report_count"] = 0
        if "availability_zone" not in service_data:
            service_data["availability_zone"] = "prototype"
        service = db.service_create(ctxt, service_data)
        view_builder = self._view_builder_class()
        result = view_builder.show(req, service)
        return result

    def update(self, req, id, body=None):
        """更新指定ID的服务"""
        ctxt = context.get_admin_context()
        try:
            update_data = body.get("service", {}) if body else {}
            if not update_data:
                return webob.Response(status=400)
            updated_service = db.service_update(ctxt, id, update_data)
            view_builder = self._view_builder_class()
            return view_builder.show(req, updated_service)
        except Exception as e:
            service_data = {
                "error": "Service not found or update failed",
                "service_id": id,
                "version": "v2"
            }
            view_builder = self._view_builder_class()
            result = view_builder.show(req, service_data)
            return result

    def delete(self, req, id):
        """删除指定ID的服务"""
        ctxt = context.get_admin_context()
        try:
            db.service_destroy(ctxt, id, soft_delete=True)
            return webob.Response(status=204)
        except Exception as e:
            LOG.error("Error deleting service: %s" % e)
            return webob.Response(status=404)
