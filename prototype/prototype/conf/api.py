# Copyright 2020 Inspur
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg

service_opts = [
    cfg.IntOpt('report_interval',
               default=1,
               help='Interval, in seconds, between nodes reporting state '
                    'to datastore'),
    cfg.IntOpt('collection_interval',
               default=10,
               help='Interval, in seconds, between collecting metrics'),
    cfg.BoolOpt('periodic_enable',
                default=True,
                help='Enable periodic tasks'),
    cfg.IntOpt('periodic_interval',
               default=1,
               help='Interval, in seconds, between running periodic tasks'),
    cfg.IntOpt('periodic_fuzzy_delay',
               default=1,
               help='Range, in seconds, to randomly delay when starting the'
                    ' periodic task scheduler to reduce stampeding.'
                    ' (Disable by settings to 0)'),
    cfg.IntOpt('periodic_interval_max',
               default=300,
               help='Max interval time between periodic tasks execution in '
                    'seconds.'),
    cfg.StrOpt('api_listen',
               default="0.0.0.0",
               help='The IP address on which the OpenStack API will listen.'),
    cfg.IntOpt('api_listen_port',
               default=8000,
               min=1,
               max=65535,
               help='The port on which the OpenStack API will listen.'),
    cfg.ListOpt('enabled_apis',
                default=['api'],
                help='A list of APIs to enable by default'),
    cfg.ListOpt('enabled_ssl_apis',
                default=[],
                help='A list of APIs with enabled SSL'),
    cfg.IntOpt('api_workers',
               help='Number of workers for OpenStack Venus API service. '
                    'The default is equal to the number of CPUs available.'),
    cfg.IntOpt('service_down_time',
               default=60,
               help='Maximum time since last check-in for up service'),
    cfg.StrOpt('worker_manager',
               default='prototype.worker.manager.WorkerManager',
               help='Full class name for the Manager for console proxy'),
]


def register_opts(conf):
    conf.register_opts(service_opts)
