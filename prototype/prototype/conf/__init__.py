#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright: (c)  : @Time 2025/9/21 10  @Author  : hjl
# @Site    : 
# @File    : __init__.py.py
# @Project: oslo.prototype
# @Software: PyCharm
# @Desc    :
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from oslo_config import cfg
from prototype.conf import api
from prototype.conf import common
from prototype.conf import core
from prototype.conf import db

CONF = cfg.CONF

api.register_opts(CONF)
common.register_opts(CONF)
core.register_opts(CONF)
db.register_opts(CONF)
