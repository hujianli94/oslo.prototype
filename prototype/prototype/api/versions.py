# coding=utf-8
# Copyright 2010 OpenStack Foundation
# Copyright 2015 Clinton Knight
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import copy

from prototype.conf import CONF
from six.moves import http_client

from prototype.api import extensions
from prototype.api import openstack
from prototype.api.openstack import api_version_request
from prototype.api.openstack import wsgi
from prototype.api.views import versions as views_versions

_LINKS = [{
    "rel": "describedby",
    "type": "text/html",
    "href": "https://docs.openstack.org/",
}]

# 修改KNOWN_VERSIONS以支持v1.0和v2.0
_KNOWN_VERSIONS = {
    "v1.0": {
        "id": "v1.0",
        "status": "CURRENT",
        "version": api_version_request._MAX_API_VERSION,
        "min_version": api_version_request._MIN_API_VERSION,
        "updated": api_version_request.UPDATED,
        "links": _LINKS,
        "media-types": [{
            "base": "application/json",
            "type": "application/vnd.openstack.compute+json;version=1",
        }]
    },
    "v2.0": {
        "id": "v2.0",
        "status": "EXPERIMENTAL",
        "version": "",
        "min_version": "",
        "updated": "2025-10-23T11:33:21Z",
        "links": _LINKS,
        "media-types": [{
            "base": "application/json",
            "type": "application/vnd.openstack.compute+json;version=2",
        }]
    },
}


class Versions(openstack.APIRouter):
    """Route versions requests."""

    ExtensionManager = extensions.ExtensionManager

    def _setup_routes(self, mapper, ext_mgr):
        self.resources['versions'] = create_resource()
        mapper.connect('versions', '/',
                       controller=self.resources['versions'],
                       action='all')
        mapper.redirect('', '/')

    def _setup_ext_routes(self, mapper, ext_mgr):
        # NOTE(mriedem): The version router doesn't care about extensions.
        pass

    # NOTE (jose-castro-leon): Avoid to register extensions
    # on the versions router, the versions router does not offer
    # resources to be extended.
    def _setup_extensions(self, ext_mgr):
        pass


class VersionsController(wsgi.Controller):

    def __init__(self):
        super(VersionsController, self).__init__(None)

    # 修改index方法以支持v1.0
    @wsgi.Controller.api_version('1.0')
    def index(self, req):  # pylint: disable=E0102
        """Return versions supported for v1.0."""
        builder = views_versions.get_view_builder(req)
        known_versions = copy.deepcopy(_KNOWN_VERSIONS)
        known_versions.pop('v2.0')
        return builder.build_versions(known_versions)

    # 添加v2.0的支持
    @index.api_version('2.0')
    def index(self, req):  # pylint: disable=E0102
        """Return versions supported for v2.0."""
        builder = views_versions.get_view_builder(req)
        known_versions = copy.deepcopy(_KNOWN_VERSIONS)
        known_versions.pop('v1.0')
        return builder.build_versions(known_versions)

    # NOTE (cknight): Calling the versions API without
    # /v1 or /v2 in the URL will lead to this unversioned
    # method, which should always return info about all
    # available versions.
    @wsgi.response(http_client.MULTIPLE_CHOICES)
    def all(self, req):
        """Return all known and enabled versions."""
        builder = views_versions.get_view_builder(req)
        known_versions = copy.deepcopy(_KNOWN_VERSIONS)

        # 根据配置决定启用哪些版本
        if not CONF.enable_v1_api:
            known_versions.pop('v1.0', None)
        if not CONF.enable_v2_api:
            known_versions.pop('v2.0', None)

        return builder.build_versions(known_versions)


def create_resource():
    return wsgi.Resource(VersionsController())
