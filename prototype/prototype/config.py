# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# Copyright 2012 Red Hat, Inc.
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
import os
from oslo_config import cfg
from oslo_db import options
from oslo_log import log
from prototype.common.i18n import _
from prototype.common import rpc
from prototype import version

import socket
from oslo_utils import netutils

CONF = cfg.CONF



core_opts = [
    cfg.StrOpt('connection_type',
               default=None,
               help='Virtualization api connection type : libvirt, xenapi, '
                    'or fake'),
    cfg.StrOpt('sql_connection',
               default='sqlite:///$state_path/$sqlite_db',
               help='The SQLAlchemy connection string used to connect to the '
                    'database',
               secret=True),
    cfg.IntOpt('sql_connection_debug',
               default=0,
               help='Verbosity of SQL debugging information. 0=None, '
                    '100=Everything'),
    cfg.StrOpt('api_paste_config',
               default="api-paste.ini",
               help='File name for the paste.deploy config for prototype-api'),
    cfg.StrOpt('pybasedir',
               default=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '../')),
               help='Directory where the prototype python module is installed'),
    cfg.StrOpt('bindir',
               default='$pybasedir/bin',
               help='Directory where prototype binaries are installed'),
    cfg.StrOpt('state_path',
               default='$pybasedir',
               help="Top-level directory for maintaining prototype's state"), ]

debug_opts = [
]

tests_opts = [
    cfg.StrOpt('testdb_manager',
               default='prototype.tests.db.manager.TestDBManager',
               help='full class name for the Manager for servicemanage backup'),
    cfg.StrOpt('testdb_topic',
               default='prototype-testdb',
               help='the topic testdb nodes listen on'),
]

CONF.register_cli_opts(core_opts)
CONF.register_cli_opts(debug_opts)
CONF.register_cli_opts(tests_opts)

global_opts = [
    cfg.StrOpt('my_ip',
               default=netutils.get_my_ipv4(),
               help='ip address of this host'),
    cfg.BoolOpt('use_ipv6',
                default=False,
                help='Use IPv6'),
    cfg.StrOpt('storage_availability_zone',
               default='prototype',
               help='Availability zone of this node'),
    cfg.StrOpt('conductor_topic',
               default='prototype-conductor',
               help='the topic conductor service listen on'),
    cfg.StrOpt('scheduler_topic',
               default='prototype-scheduler',
               help='the topic scheduler service listen on'),
    cfg.BoolOpt('enable_v1_api',
                default=True,
                help=_("Deploy v1 of the Prototype API. ")),
    cfg.BoolOpt('enable_v2_api',
                default=True,
                help=_("Deploy v2 of the Prototype API. ")),
    cfg.BoolOpt('api_rate_limit',
                default=True,
                help='whether to rate limit the api'),
    cfg.StrOpt('prototype_availability_zone',
               default='nova',
               help='availability zone of this node'),
    cfg.ListOpt('osapi_servicemanage_ext_list',
                default=[],
                help='Specify list of extensions to load when using osapi_'
                     'servicemanage_extension option with prototype.api.contrib.'
                     'select_extensions'),
    cfg.MultiStrOpt('osapi_servicemanage_extension',
                    default=['prototype.api.contrib.standard_extensions'],
                    help='osapi servicemanage extension to load'),
    cfg.StrOpt('osapi_servicemanage_base_URL',
               default=None,
               help='Base URL that will be presented to users in links '
                    'to the OpenStack ServiceManage API',
               deprecated_name='osapi_compute_link_prefix'),
    cfg.IntOpt('osapi_max_limit',
               default=1000,
               help='the maximum number of items returned in a single '
                    'response from a collection resource'),
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
    cfg.StrOpt('host',
               default=socket.gethostname(),
               help='Name of this node.  This can be an opaque identifier.  '
                    'It is not necessarily a hostname, FQDN, or IP address.'),
    cfg.ListOpt('memcached_servers',
                default=None,
                help='Memcached servers or None for in process cache.'),
    cfg.StrOpt('root_helper',
               default='sudo',
               help='Deprecated: command to use for running commands as root'),
    cfg.StrOpt('rootwrap_config',
               default=None,
               help='Path to the rootwrap configuration file to use for '
                    'running commands as root'),
    cfg.BoolOpt('monkey_patch',
                default=False,
                help='Whether to log monkey patching'),
    cfg.ListOpt('monkey_patch_modules',
                default=[],
                help='List of modules/decorators to monkey patch'),
    cfg.StrOpt('auth_strategy',
               default='noauth',
               help='The strategy to use for auth. Supports noauth, keystone, '
                    'and deprecated.'),
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
]

CONF.register_opts(global_opts)

_DEFAULT_LOG_LEVELS = ['amqp=WARN', 'amqplib=WARN', 'boto=WARN',
                       'qpid=WARN', 'sqlalchemy=WARN', 'suds=INFO',
                       'oslo.messaging=INFO', 'iso8601=WARN',
                       'requests.packages.urllib3.connectionpool=WARN',
                       'urllib3.connectionpool=WARN', 'websocket=WARN',
                       'keystonemiddleware=WARN', 'routes.middleware=WARN',
                       'stevedore=WARN']

_DEFAULT_LOGGING_CONTEXT_FORMAT = ('%(asctime)s.%(msecs)03d %(process)d '
                                   '%(levelname)s %(name)s [%(request_id)s '
                                   '%(user_identity)s] %(instance)s'
                                   '%(message)s')


def parse_args(argv, default_config_files=None):
    log.set_defaults(_DEFAULT_LOGGING_CONTEXT_FORMAT, _DEFAULT_LOG_LEVELS)
    options.set_defaults(CONF, connection=CONF.sql_connection)
    rpc.set_defaults(control_exchange='prototype')
    CONF(argv[1:],
         project='prototype',
         version=version.version_string(),
         default_config_files=default_config_files)
