# coding=utf-8
# Copyright (c) 2011 X.commerce, a business unit of eBay Inc.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
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

"""Implementation of SQLAlchemy backend."""
from sqlalchemy import func
import functools
import sys
import threading
import time
import warnings
from oslo_config import cfg
from oslo_db import exception as db_exc
from oslo_db.sqlalchemy import session as db_session
from oslo_db.sqlalchemy import utils as db_utils
from oslo_utils import timeutils
from prototype.db.sqlalchemy import models
from prototype.common.i18n import _, _LI, _LE, _LW
from prototype.common import exception
from oslo_log import log as logging

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

_ENGINE_FACADE = None
_LOCK = threading.Lock()


def _create_facade_lazily():
    global _LOCK, _ENGINE_FACADE
    if _ENGINE_FACADE is None:
        with _LOCK:
            if _ENGINE_FACADE is None:
                _ENGINE_FACADE = db_session.EngineFacade.from_config(CONF)
    return _ENGINE_FACADE


def get_engine(use_slave=False):
    facade = _create_facade_lazily()
    return facade.get_engine(use_slave=use_slave)


def get_session(use_slave=False, **kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(use_slave=use_slave, **kwargs)


def get_backend():
    """The backend is this module itself. required for oslo_db."""
    return sys.modules[__name__]


def is_admin_context(context):
    """Indicates if the request context is an administrator."""
    if not context:
        warnings.warn(_('Use of empty request context is deprecated'),
                      DeprecationWarning)
        raise Exception('die')
    return context.is_admin


def is_user_context(context):
    """Indicates if the request context is a normal user."""
    if not context:
        return False
    if context.is_admin:
        return False
    if not context.user_id or not context.project_id:
        return False
    return True


def authorize_project_context(context, project_id):
    """Ensures a request has permission to access the given project."""
    if is_user_context(context):
        if not context.project_id:
            raise exception.NotAuthorized()
        elif context.project_id != project_id:
            raise exception.NotAuthorized()


def authorize_user_context(context, user_id):
    """Ensures a request has permission to access the given user."""
    if is_user_context(context):
        if not context.user_id:
            raise exception.NotAuthorized()
        elif context.user_id != user_id:
            raise exception.NotAuthorized()


def authorize_quota_class_context(context, class_name):
    """Ensures a request has permission to access the given quota class."""
    if is_user_context(context):
        if not context.quota_class:
            raise exception.NotAuthorized()
        elif context.quota_class != class_name:
            raise exception.NotAuthorized()


def require_admin_context(f):
    """Decorator to require admin request context.

    The first argument to the wrapped function must be the context.

    """

    def wrapper(*args, **kwargs):
        if not is_admin_context(args[0]):
            raise exception.AdminRequired()
        return f(*args, **kwargs)

    return wrapper


def require_context(f):
    """Decorator to require *any* user or admin context.

    This does no authorization for user or project access matching, see
    :py:func:`authorize_project_context` and
    :py:func:`authorize_user_context`.

    The first argument to the wrapped function must be the context.

    """

    def wrapper(*args, **kwargs):
        if not is_admin_context(args[0]) and not is_user_context(args[0]):
            raise exception.NotAuthorized()
        return f(*args, **kwargs)

    return wrapper


def _retry_on_deadlock(f):
    """Decorator to retry a DB API call if Deadlock was received."""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except db_exc.DBDeadlock:
                LOG.warning(_LW("Deadlock detected when running "
                                "'%(func_name)s': Retrying..."),
                            dict(func_name=f.__name__))
                # Retry!
                time.sleep(0.5)
                continue

    functools.update_wrapper(wrapped, f)
    return wrapped


def convert_datetimes(values, *datetime_keys):
    for key in values:
        if key in datetime_keys and isinstance(values[key], str):
            values[key] = timeutils.parse_strtime(values[key])
    return values


def model_query(context, *args, **kwargs):
    """Query helper that accounts for context's `read_deleted` field.

    :param context: context to query under
    :param session: if present, the session to use
    :param read_deleted: if present, overrides context's read_deleted field.
    :param project_only: if present and context is user-type, then restrict
            query to match the context's project_id.
    """
    session = kwargs.get('session') or get_session()
    read_deleted = kwargs.get('read_deleted') or getattr(context, 'read_deleted', 'no')
    project_only = kwargs.get('project_only', False)

    query = session.query(*args)

    if read_deleted == 'no':
        query = query.filter_by(deleted=False)
    elif read_deleted == 'yes':
        pass  # omit the filter to include deleted and active
    elif read_deleted == 'only':
        query = query.filter_by(deleted=True)
    else:
        raise Exception(
            _("Unrecognized read_deleted value '%s'") % read_deleted)

    if project_only and is_user_context(context):
        query = query.filter_by(project_id=context.project_id)

    return query


def exact_filter(query, model, filters, legal_keys):
    """Applies exact match filtering to a query.

    Returns the updated query.  Modifies filters argument to remove
    filters consumed.

    :param query: query to apply filters to
    :param model: model object the query applies to, for IN-style
                  filtering
    :param filters: dictionary of filters; values that are lists,
                    tuples, sets, or frozensets cause an 'IN' test to
                    be performed, while exact matching ('==' operator)
                    is used for other values
    :param legal_keys: list of keys to apply exact filtering to
    """

    filter_dict = {}

    # Walk through all the keys
    for key in legal_keys:
        # Skip ones we're not filtering on
        if key not in filters:
            continue

        # OK, filtering on this key; what value do we search for?
        value = filters.pop(key)

        if isinstance(value, (list, tuple, set, frozenset)):
            # Looking for values in a list; apply to query directly
            column_attr = getattr(model, key)
            query = query.filter(column_attr.in_(value))
        else:
            # OK, simple exact match; save for later
            filter_dict[key] = value

    # Apply simple exact matches
    if filter_dict:
        query = query.filter_by(**filter_dict)

    return query


############################ Service #################################
@require_admin_context
def service_get(context, service_id):
    """Get a service or raise ServiceNotFound if it does not exist."""
    result = model_query(context, models.Service, read_deleted="no"). \
        filter_by(id=service_id). \
        first()

    if not result:
        raise exception.ServiceNotFound(service_id=service_id)

    return result


@require_admin_context
def service_create(context, values):
    """Create a service from the values dictionary."""
    service_ref = models.Service()
    service_ref.update(values)
    if 'report_count' not in values:
        service_ref['report_count'] = 0
    if 'availability_zone' not in values:
        service_ref['availability_zone'] = 'prototype'
    service_ref.save()
    return service_ref


@require_admin_context
def service_update(context, service_id, values):
    """Set the given properties on a service and update it.

    :raises: ServiceNotFound if service does not exist
    """
    service_ref = service_get(context, service_id)
    service_ref.update(values)
    service_ref.save()
    return service_ref


@require_admin_context
def service_destroy(context, service_id):
    """Destroy the service or raise ServiceNotFound if it does not exist."""
    try:
        service_ref = service_get(context, service_id)
        # 软删除
        service_ref['deleted'] = True
        service_ref['deleted_at'] = timeutils.utcnow()
        service_ref['updated_at'] = service_ref['deleted_at']
        service_ref.save()
        # 物理删除
        # service_ref.delete(service_ref['id'])
    except exception.ServiceNotFound:
        raise
    except Exception as e:
        LOG.error("Error deleting service: %s" % e)
        raise


@require_admin_context
def service_get_all(context, disabled=None):
    """Get all services."""
    query = model_query(context, models.Service, read_deleted="no")
    if disabled is not None:
        query = query.filter_by(disabled=disabled)
    return query.all()


@require_admin_context
def service_get_all_by_topic(context, topic):
    """Get all services for a given topic."""
    return model_query(context, models.Service, read_deleted="no"). \
        filter_by(topic=topic). \
        all()


@require_admin_context
def service_get_by_host_and_topic(context, host, topic):
    result = model_query(
        context, models.Service, read_deleted="no"). \
        filter_by(disabled=False). \
        filter_by(host=host). \
        filter_by(topic=topic). \
        first()
    if not result:
        raise exception.ServiceNotFound(service_id=None)
    return result


@require_admin_context
def service_get_all_by_host(context, host):
    return model_query(
        context, models.Service, read_deleted="no"). \
        filter_by(host=host). \
        all()


@require_admin_context
def service_get_by_args(context, host, binary):
    result = model_query(context, models.Service). \
        filter_by(host=host). \
        filter_by(binary=binary). \
        first()

    if not result:
        raise exception.HostBinaryNotFound(host=host, binary=binary)

    return result


@require_admin_context
def service_get_all_by_host_and_topic(context, host, topic):
    """Get all services for a given host and topic."""
    return model_query(context, models.Service, read_deleted="no"). \
        filter_by(host=host). \
        filter_by(topic=topic). \
        all()
