# coding=utf-8
# Copyright (c) 2011 X.commerce, a business unit of eBay Inc.
import six
from prototype.conf import CONF
from oslo_db.sqlalchemy import models
from oslo_utils import timeutils
from sqlalchemy.ext.declarative import declarative_base  # noqa
from sqlalchemy import orm
from sqlalchemy import Table, Column, ForeignKey, Index, MetaData
from sqlalchemy import DateTime, Integer, String, BigInteger, Boolean, Text, Unicode, Float

BASE = declarative_base()


def get_session():
    from prototype.db.sqlalchemy import api as db_api
    return db_api.get_session()


class PrototypeBase(models.SoftDeleteMixin, models.TimestampMixin, models.ModelBase):
    metadata = None
    __table_args__ = {'mysql_engine': 'InnoDB'}

    def __copy__(self):
        """Implement a safe copy.copy()."""
        session = orm.Session()
        copy = session.merge(self, load=False)
        session.expunge(copy)
        return copy

    def save(self, session=None):
        from prototype.db.sqlalchemy import api
        if session is None:
            session = api.get_session()
        super(PrototypeBase, self).save(session=session)

    def expire(self, session=None, attrs=None):
        """Expire this object ()."""
        if not session:
            session = get_session()
        session.expire(self, attrs)

    def refresh(self, session=None, attrs=None):
        """Refresh this object."""
        if not session:
            session = get_session()
        session.refresh(self, attrs)

    @staticmethod
    def delete_values():
        return {'deleted': True,
                'deleted_at': timeutils.utcnow()}

    def delete(self, session=None):
        """Delete this object."""
        if not session:
            session = get_session()
        session.begin(subtransactions=True)
        session.delete(self)
        session.commit()

    def update_and_save(self, values, session=None):
        if not session:
            session = get_session()
        session.begin(subtransactions=True)
        for k, v in six.iteritems(values):
            setattr(self, k, v)
        session.commit()


class Service(BASE, PrototypeBase):
    """Represents a running service on a host."""
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, nullable=False)
    host = Column(String(255))
    binary = Column(String(255))  # 服务运行的二进制文件名
    topic = Column(String(255))
    report_count = Column(Integer, nullable=False, default=0)  # 上报次数
    disabled = Column(Boolean, default=False)
    availability_zone = Column(String(255), default='prototype')


class WorkerNode(BASE, PrototypeBase):
    """Represents an agent node's resources."""

    __tablename__ = 'worker_nodes'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(255), nullable=False)
    os = Column(String(255), nullable=False)
    os_version = Column(String(255), nullable=False)
    cpu_count = Column(Integer, nullable=False)
    cpu_count_logical = Column(Float, nullable=False)
    memory_total_gb = Column(Float, nullable=False)
    memory_available_gb = Column(Float, nullable=False)
    memory_percent = Column(Float, default=0.0, nullable=False)

    @classmethod
    def get_all(cls, session, filters=None):
        query = session.query(cls).filter_by(deleted=False)
        if filters:
            query = query.filter_by(**filters)
        return query.all()
