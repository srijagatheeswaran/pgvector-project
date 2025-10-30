import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

from .db import Base
from .config import settings


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    embedding = Column(Vector(dim=settings.PGVECTOR_DIM), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DataSubject(Base):
    __tablename__ = "data_subjects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_identifier = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ErasureRequest(Base):
    __tablename__ = "erasure_requests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = Column(String, nullable=False)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
