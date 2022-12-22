# -*- coding: utf-8 -*-
import enum

from sqlalchemy import Column, Integer, String, Sequence, DateTime, func, Enum

from db.models.base import Base


class TaskStates(enum.Enum):
    NEW = 0
    ON_REVIEW = 1
    FINAL_REVIEW_REQUIRED = 2
    COMPLETED = 3


class TasksModel(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    url = Column(String, nullable=False, unique=False)
    status = Column(Enum(TaskStates), nullable=False, default=TaskStates.NEW)
    chat_id = Column(Integer, nullable=False)
    publisher_msg_id = Column(Integer, nullable=False)
    publisher_id = Column(Integer, nullable=False)
    publisher_name = Column(String, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=False)
    reply_msg_id = Column(Integer, nullable=True)
    reviewer_id = Column(Integer, nullable=True)
    reviewer_name = Column(String, nullable=True)
    taken_on_review_at = Column(DateTime(timezone=True), nullable=True)
    submitted_to_final_review_at = Column(DateTime(timezone=True), nullable=True)

    completed_at = Column(DateTime(timezone=True), nullable=True)
    final_reviewer_name = Column(String, nullable=True)
