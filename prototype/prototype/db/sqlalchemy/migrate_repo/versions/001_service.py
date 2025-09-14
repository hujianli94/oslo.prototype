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
                     Column('type', String(length=255)),
                     Column('topic', String(length=255)),
                     Column('report_count', Integer, nullable=False, default=0),  # 上报次数
                     Column('disabled', Boolean),
                     Column('availability_zone', String(length=255)),
                     mysql_engine='InnoDB',
                     mysql_charset='utf8'
                     )
    try:
        services.create()
    except Exception:
        LOG.info(repr(services))
        LOG.exception('Exception while creating table')
        meta.drop_all(tables=[services])
        raise


# def downgrade(migrate_engine):
#     meta = schema.MetaData()
#     meta.bind = migrate_engine
#     services = schema.Table('service', meta, autoload=True)
#     services.drop()
def downgrade(migrate_engine):
    LOG.exception(_('Downgrade from initial Prototype install is unsupported.'))
