#    Copyright 2011 OpenStack Foundation
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

import pbr.version

from prototype.common.i18n import _LE

PROTOTYPE_VENDOR = "OpenStack Foundation"
PROTOTYPE_PRODUCT = "OpenStack Prototype"
PROTOTYPE_PACKAGE = None  # OS distro package version suffix

loaded = False
version_info = pbr.version.VersionInfo('prototype')
version_string = version_info.version_string


def _load_config():
    # Don't load in global context, since we can't assume
    # these modules are accessible when distutils uses
    # this module
    from six.moves import configparser

    from oslo_config import cfg

    from oslo_log import log as logging

    global loaded, PROTOTYPE_VENDOR, PROTOTYPE_PRODUCT, PROTOTYPE_PACKAGE
    if loaded:
        return

    loaded = True

    cfgfile = cfg.CONF.find_file("release")
    if cfgfile is None:
        return

    try:
        cfg = configparser.RawConfigParser()
        cfg.read(cfgfile)

        PROTOTYPE_VENDOR = cfg.get("Prototype", "vendor")
        if cfg.has_option("Prototype", "vendor"):
            PROTOTYPE_VENDOR = cfg.get("Prototype", "vendor")

        PROTOTYPE_PRODUCT = cfg.get("Prototype", "product")
        if cfg.has_option("Prototype", "product"):
            PROTOTYPE_PRODUCT = cfg.get("Prototype", "product")

        PROTOTYPE_PACKAGE = cfg.get("Prototype", "package")
        if cfg.has_option("Prototype", "package"):
            PROTOTYPE_PACKAGE = cfg.get("Prototype", "package")
    except Exception as ex:
        LOG = logging.getLogger(__name__)
        LOG.error(_LE("Failed to load %(cfgfile)s: %(ex)s"),
                  {'cfgfile': cfgfile, 'ex': ex})


def vendor_string():
    _load_config()

    return PROTOTYPE_VENDOR


def product_string():
    _load_config()

    return PROTOTYPE_PRODUCT


def package_string():
    _load_config()

    return PROTOTYPE_PACKAGE


def version_string_with_package():
    if package_string() is None:
        return version_info.version_string()
    else:
        return "%s-%s" % (version_info.version_string(), package_string())
