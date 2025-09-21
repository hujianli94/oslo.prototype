#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright: (c)  : @Time 2025/9/21 10  @Author  : hjl
# @Site    : 
# @File    : common.py.py
# @Project: oslo.prototype
# @Software: PyCharm
# @Desc    :
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import socket

from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import netutils
from prototype.common.i18n import _

global_opts = [
    cfg.StrOpt('my_ip',
               default=netutils.get_my_ipv4(),
               help='IP address of this host'),
    cfg.StrOpt('prototypemanager_topic',
               default='prototype-prototypemanager',
               help='The topic that prototypemanager nodes listen on'),
    cfg.BoolOpt('enable_v1_api',
                default=True,
                help=_("Deploy v1 of the Prototype API. ")),
    cfg.BoolOpt('enable_v2_api',
                default=True,
                help=_("Deploy v2 of the Prototype API. ")),
    cfg.BoolOpt('api_rate_limit',
                default=True,
                help='whether to rate limit the api'),
    cfg.ListOpt('osapi_prototype_ext_list',
                default=[],
                help='Specify list of extensions to load when using osapi_'
                     'prototype_extension option with prototype.api.contrib.'
                     'select_extensions'),
    cfg.MultiStrOpt('osapi_prototype_extension',
                    default=['prototype.api.contrib.standard_extensions'],
                    help='osapi prototype extension to load'),
    cfg.StrOpt('prototypemanager_manager',
               default='prototype.prototypemanager.'
                       'manager.PrototypemanagerManager',
               help='Full class name for '
                    'the Manager for prototypemanager'),
    cfg.StrOpt('host',
               default=socket.gethostname(),
               help='Name of this node.  This can be an opaque identifier.  '
                    'It is not necessarily a hostname, FQDN, or IP address.'),
    cfg.StrOpt('rootwrap_config',
               default='/etc/prototype/rootwrap.conf',
               help='Path to the rootwrap configuration file to '
                    'use for running commands as root'),
    cfg.BoolOpt('disable_rootwrap',
                default=False,
                help='This option allows a fallback to sudo for performance '
                     'reasons. For example see '
                     'https://bugs.launchpad.net/prototype/+bug/1415106'),
    cfg.BoolOpt('monkey_patch',
                default=False,
                help='Whether to log monkey patching'),
    cfg.ListOpt('monkey_patch_modules',
                default=[],
                help='List of modules/decorators to monkey patch'),
    cfg.StrOpt('prototypemanager_api_class',
               default='prototype.prototypemanager.api.API',
               help='The full class name of the '
                    'prototypemanager API class to use'),
    cfg.StrOpt('auth_strategy',
               default='noauth',
               help='The strategy to use for auth. Supports noauth, keystone, '
                    'and deprecated.'),
    cfg.StrOpt('os_privileged_user_name',
               default=None,
               help='OpenStack privileged account username. Used for '
                    'requests to other services (such as Nova) that '
                    'require an account with special rights.'),
    cfg.StrOpt('os_privileged_user_password',
               default=None,
               help='Password associated with the OpenStack '
                    'privileged account.',
               secret=True),
    cfg.StrOpt('os_privileged_user_project',
               default=None,
               help='Project name associated with the OpenStack '
                    'privileged account.'),
    cfg.StrOpt('os_privileged_user_auth_url',
               default=None,
               help='Auth URL associated with the OpenStack '
                    'privileged account.'),
    cfg.StrOpt('os_region_name',
               default='RegionOne',
               help='os region name'),
    cfg.BoolOpt('tcp_keepalive',
                default=True,
                help="Sets the value of TCP_KEEPALIVE (True/False) for each "
                     "server socket."),
    cfg.IntOpt('tcp_keepidle',
               default=600,
               help="Sets the value of TCP_KEEPIDLE in seconds for each "
                    "server socket. Not supported on OS X."),
    cfg.IntOpt('wsgi_default_pool_size',
               default=1000,
               help="Size of the pool of greenthreads used by wsgi"),
    cfg.IntOpt('tcp_keepalive_interval',
               help="Sets the value of TCP_KEEPINTVL in seconds for each "
                    "server socket. Not supported on OS X."),
    cfg.IntOpt('tcp_keepalive_count',
               help="Sets the value of TCP_KEEPCNT for each "
                    "server socket. Not supported on OS X."),
    cfg.StrOpt('ssl_ca_file',
               default=None,
               help="CA certificate file to use to verify "
                    "connecting clients"),
    cfg.StrOpt('ssl_cert_file',
               default=None,
               help="Certificate file to use when starting "
                    "the server securely"),
    cfg.StrOpt('ssl_key_file',
               default=None,
               help="Private key file to use when starting "
                    "the server securely"),
    cfg.IntOpt('max_header_line',
               default=16384,
               help="Maximum line size of message headers to be accepted. "
                    "max_header_line may need to be increased when using "
                    "large tokens (typically those generated by the "
                    "Keystone v3 API with big service catalogs)."),
    cfg.IntOpt('client_socket_timeout', default=900,
               help="Timeout for client connections\' socket operations. "
                    "If an incoming connection is idle for this number of "
                    "seconds it will be closed. A value of \'0\' means "
                    "wait forever."),
    cfg.BoolOpt('wsgi_keep_alive',
                default=True,
                help='If False, closes the client socket connection '
                     'explicitly. Setting it to True to maintain backward '
                     'compatibility. Recommended settings is set it '
                     'to False.'),
    cfg.BoolOpt('fatal_exception_format_errors',
                default=False,
                help='Make exception message format errors fatal.'),
    cfg.StrOpt('prototype_internal_project_id',
               default=None,
               help='ID of the project which will be used as the Prototype '
                    'internal project.'),
    cfg.StrOpt('prototype_internal_user_id',
               default=None,
               help='ID of the user to be used'
                    ' in prototype operations as the '
                    'Prototype internal project.'),
    cfg.StrOpt('db_driver',
               default='prototype.db',
               help='Driver to use for database access'),
    cfg.BoolOpt('use_forwarded_for',
                default=False,
                help='Treat X-Forwarded-For as the canonical remote address. '
                     'Only enable this if you have a sanitizing proxy.'),
    # Default request size is 112k
    cfg.IntOpt('osapi_max_request_body_size',
               default=114688,
               help='Max size for body of a request'),
    cfg.StrOpt('public_endpoint', default=None,
               help="Public URL to use for versions endpoint. The default "
                    "is None, which will use the request's host_url "
                    "attribute to populate the URL base. If Venus is "
                    "operating behind a proxy, you will want to change "
                    "this to represent the proxy's URL."),
    cfg.IntOpt('osapi_max_limit',
               default=1000,
               help='The maximum number of items that a collection '
                    'resource returns in a single response'),
    cfg.StrOpt('osapi_prototype_base_URL',
               default=None,
               help='Base URL that will be presented to users in links '
                    'to the OpenStack Prototype API',
               deprecated_name='osapi_compute_link_prefix'),
    cfg.StrOpt('task_manager',
               default="prototype.manager.Manager",
               help='Btask_manager'),
    cfg.BoolOpt('use_ipv6',
                default=False,
                help='Use IPv6'),
    cfg.StrOpt('conductor_topic',
               default='prototype-conductor',
               help='the topic conductor service listen on'),
    cfg.StrOpt('scheduler_topic',
               default='prototype-scheduler',
               help='the topic scheduler service listen on'),
    cfg.StrOpt('worker_topic',
               default='worker',
               help='The topic console proxy nodes listen on'),
    cfg.StrOpt('prototype_availability_zone',
               default='prototype',
               help='availability zone of this node'),
    cfg.StrOpt('sqlite_db',
               default='prototype.sqlite',
               help='the filename to use with sqlite'),
    cfg.BoolOpt('sqlite_synchronous',
                default=True,
                help='If passed, use synchronous mode for sqlite'),
    cfg.IntOpt('sql_idle_timeout',
               default=3600,
               help='timeout before idle sql connections are reaped'),
    cfg.IntOpt('sql_max_retries',
               default=10,
               help='maximum db connection retries during startup. '
                    '(setting -1 implies an infinite retry count)'),
    cfg.IntOpt('sql_retry_interval',
               default=10,
               help='interval between retries of opening a sql connection'),
    cfg.StrOpt('conductor_manager',
               default='prototype.conductor.manager.ConductorManager',
               help='full class name for the Manager for Conductor'),
    cfg.StrOpt('scheduler_manager',
               default='prototype.scheduler.manager.SchedulerManager',
               help='full class name for the Manager for Scheduler'),
    cfg.ListOpt('memcached_servers',
                default=None,
                help='Memcached servers or None for in process cache.'),
    cfg.StrOpt('root_helper',
               default='sudo',
               help='Deprecated: command to use for running commands as root'),
    cfg.ListOpt('enabled_backends',
                default=None,
                help='A list of backend names to use. These backend names '
                     'should be backed by a unique [CONFIG] group '
                     'with its options'),
    cfg.IntOpt('password_length',
               default=12,
               help='Length of generated instance admin passwords'),
    cfg.StrOpt('tempdir',
               help='Explicitly specify the temporary working directory'),
    cfg.StrOpt('prototype_internal_tenant_project_id',
               help='ID of the project which will be used as the Prototype '
                    'internal tenant.'),
    cfg.StrOpt('prototype_internal_tenant_user_id',
               help='ID of the user to be used in volume operations as the '
                    'Prototype internal tenant.'),
]


def register_opts(conf):
    logging.register_options(conf)
    conf.register_opts(global_opts)
