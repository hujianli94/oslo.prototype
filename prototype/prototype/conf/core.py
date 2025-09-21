#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright: (c)  : @Time 2025/9/21 10  @Author  : hjl
# @Site    : 
# @File    : core.py.py
# @Project: oslo.prototype
# @Software: PyCharm
# @Desc    :
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
from oslo_config import cfg

core_opts = [
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


def register_opts(conf):
    conf.register_cli_opts(core_opts)
