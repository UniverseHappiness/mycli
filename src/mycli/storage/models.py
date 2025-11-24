"""Database models for mycli."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import Boolean, DateTime, Integer, String, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class Agent(Base):
    """Agent model."""
    
    __tablename__ = "agents"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    config: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="enabled")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    metadata_: Mapped[Optional[Dict[str, Any]]] = mapped_column("metadata", JSON, nullable=True)
    
    def __repr__(self) -> str:
        return f"<Agent(id={self.id}, name={self.name}, type={self.type})>"


class Session(Base):
    """Chat session model."""
    
    __tablename__ = "sessions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    agent_id: Mapped[str] = mapped_column(String(36), nullable=False)
    messages: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    context: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    def __repr__(self) -> str:
        return f"<Session(id={self.id}, agent_id={self.agent_id}, messages={len(self.messages)})>"


class Task(Base):
    """Task model."""
    
    __tablename__ = "tasks"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    agent_id: Mapped[str] = mapped_column(String(36), nullable=False)
    input: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    output: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, name={self.name}, status={self.status})>"


class Workflow(Base):
    """Workflow model."""
    
    __tablename__ = "workflows"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    steps: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False)
    trigger: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    timeout: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    def __repr__(self) -> str:
        return f"<Workflow(id={self.id}, name={self.name}, steps={len(self.steps)})>"
