# -*- coding: utf-8 -*-
import enum

from sqlalchemy import Column, Integer, String, Sequence, DateTime, func, Enum

from db.models.base import Base


class TaskStates(enum.Enum):
    NEW = 0
    ON_REVIEW = 1
    COMPLETED = 2


class TasksModel(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    url = Column(String, nullable=False, unique=True)
    status = Column(Enum(TaskStates), nullable=False, default=TaskStates.NEW)
    origin_chat = Column(Integer, nullable=False)
    msg_id = Column(Integer, nullable=True)
    applicant = Column(Integer, nullable=False)
    application_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    reviewer = Column(Integer, nullable=True)
    acceptance_time = Column(DateTime(timezone=True), nullable=True)


