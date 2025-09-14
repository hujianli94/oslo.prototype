# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from prototypeclient.common import base


class Service(base.Resource):
    def __repr__(self):
        return "<Service %s>" % self._info


class ServiceManager(base.BaseManager):
    resource_class = Service

    def list(self):
        """Get a list of services.

        :rtype: list of :class:`Service`
        """
        return self._list("/services", "data")

    def get(self, service):
        """Get a specific service.

        :param service: The ID of the service to get
        :rtype: :class:`Service`
        """
        return self._get("/services/%s" % base.getid(service), "service")

    def create(self, host, type, topic):
        """Create a service.

        :param host: The host of the service
        :param type: The type of the service
        :param topic: The topic of the service
        :rtype: :class:`Service`
        """
        body = {
            "host": host,
            "type": type,
            "topic": topic
        }
        return self._post("/services", body, "service")

    def delete(self, service):
        """Delete a service.

        :param service: The ID of the service to delete
        :rtype: None
        """
        return self._delete("/services/%s" % base.getid(service))

    def update(self, service, **kwargs):
        """Update a service.

        :param service: The ID of the service to update
        :param kwargs: Service attributes to update
        :rtype: :class:`Service`
        """
        body = {"service": kwargs}
        return self._put("/services/%s" % base.getid(service), body, "service")
