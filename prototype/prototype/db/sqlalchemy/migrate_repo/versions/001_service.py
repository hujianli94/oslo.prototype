# coding=utf-8
# Copyright 2011 OpenStack Foundation
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

from sqlalchemy import schema
from sqlalchemy import Table, Column, ForeignKey, Index, MetaData
from sqlalchemy import DateTime, Integer, String, BigInteger, Boolean, Text, Unicode, Float
from prototype.common.i18n import _
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


def upgrade(migrate_engine):
    meta = schema.MetaData()
    meta.bind = migrate_engine
    services = Table('service', meta,
                     Column('created_at', DateTime),
                     Column('updated_at', DateTime),
                     Column('deleted_at', DateTime),
                     Column('deleted', Integer),
                     Column('id', Integer, primary_key=True, nullable=False),
                     Column('host', String(length=255)),
                     Column('binary', String(length=255)),  # 服务运行的二进制文件名
                     Column('topic', String(length=255)),
                     Column('report_count', Integer, nullable=False, default=0),  # 上报次数
                     Column('disabled', Boolean),
                     Column('availability_zone', String(length=255)),
                     mysql_engine='InnoDB',
                     mysql_charset='utf8'
                     )
    worker_nodes = Table('worker_nodes', meta,
                         Column('created_at', DateTime(timezone=False)),
                         Column('updated_at', DateTime(timezone=False)),
                         Column('deleted_at', DateTime(timezone=False)),
                         Column('deleted', Boolean(create_constraint=True, name=None)),
                         Column('id', Integer(), primary_key=True, nullable=False),
                         Column('hostname', String(length=255), nullable=False),
                         Column('os', String(length=255), nullable=False),
                         Column('os_version', String(length=255), nullable=False),
                         Column('cpu_count', Integer(), nullable=False),
                         Column('cpu_count_logical', Integer(), nullable=False),
                         Column('memory_total_gb', Integer(), nullable=False),
                         Column('memory_available_gb', Integer(), nullable=False),
                         Column('memory_percent', Float(), nullable=False),
                         # 添加MySQL字符集配置
                         mysql_charset='utf8',
                         mysql_collate='utf8_general_ci'
                         )
    try:
        services.create()
    except Exception:
        LOG.info(repr(services))
        LOG.exception('Exception while creating table')
        meta.drop_all(tables=[services])
        raise

    try:
        worker_nodes.create()
    except Exception:
        LOG.info(repr(worker_nodes))
        LOG.exception('Exception while creating table')
        meta.drop_all(tables=[worker_nodes])
        raise


# def downgrade(migrate_engine):
#     meta = schema.MetaData()
#     meta.bind = migrate_engine
#     services = schema.Table('service', meta, autoload=True)
#     services.drop()
#     worker_nodes = schema.Table('worker_nodes', meta, autoload=True)
#     worker_nodes.drop()


def downgrade(migrate_engine):
    LOG.exception(_('Downgrade from initial Prototype install is unsupported.'))
