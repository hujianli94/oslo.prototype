#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prototype.api.openstack import wsgi


class ViewBuilder(object):
    """Model a server API response as a python dictionary."""

    def list(self, req, service_data):
        """Generate a list of services."""
        services = service_data.get("services", [])
        services_list = []
        for service in services:
            services_list.append(self._build_service(service))

        return {
            "service": services_list,
            "count": service_data.get("count", 0)
        }

    def show(self, req, service_data):
        """Generate a service detail."""
        # 检查是否有错误信息
        if "error" in service_data:
            return service_data
        return {
            "service": self._build_service(service_data)
        }

    def _build_service(self, service):
        """Build a single service structure."""
        service_dict = {
            "id": service.get("id"),
            "host": service.get("host"),
            "type": service.get("type"),
            "topic": service.get("topic"),
            "report_count": service.get("report_count", 0),
            "disabled": service.get("disabled", False),
            "availability_zone": service.get("availability_zone", "prototype")
        }

        # 添加时间戳信息（如果存在）
        if "created_at" in service:
            service_dict["created_at"] = service["created_at"]
        if "updated_at" in service:
            service_dict["updated_at"] = service["updated_at"]

        return service_dict
