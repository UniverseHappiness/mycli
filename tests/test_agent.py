"""Test agent management."""

import tempfile
from pathlib import Path
import pytest

from mycli.core.agent import AgentManager
from mycli.storage.database import Database


@pytest.fixture
def db():
    """Create temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        database = Database(db_path=db_path)
        yield database
        database.close()


@pytest.fixture
def agent_manager(db):
    """Create agent manager."""
    manager = AgentManager(db_session=db.get_session())
    yield manager
    manager.close()


def test_create_agent(agent_manager):
    """Test creating an agent."""
    agent = agent_manager.create_agent(
        name="test-agent",
        type="general",
        description="Test agent",
    )
    
    assert agent.name == "test-agent"
    assert agent.type == "general"
    assert agent.description == "Test agent"
    assert agent.status == "enabled"


def test_create_duplicate_agent(agent_manager):
    """Test creating duplicate agent raises error."""
    agent_manager.create_agent(name="test-agent", type="general")
    
    with pytest.raises(ValueError, match="already exists"):
        agent_manager.create_agent(name="test-agent", type="general")


def test_get_agent(agent_manager):
    """Test getting an agent."""
    created = agent_manager.create_agent(name="test-agent", type="general")
    
    agent = agent_manager.get_agent("test-agent")
    
    assert agent is not None
    assert agent.name == "test-agent"
    assert agent.id == created.id


def test_get_nonexistent_agent(agent_manager):
    """Test getting non-existent agent returns None."""
    agent = agent_manager.get_agent("nonexistent")
    assert agent is None


def test_list_agents(agent_manager):
    """Test listing agents."""
    agent_manager.create_agent(name="agent1", type="general")
    agent_manager.create_agent(name="agent2", type="developer")
    
    agents = agent_manager.list_agents()
    
    assert len(agents) == 2
    assert {a.name for a in agents} == {"agent1", "agent2"}


def test_update_agent(agent_manager):
    """Test updating an agent."""
    agent_manager.create_agent(name="test-agent", type="general")
    
    updated = agent_manager.update_agent(
        name="test-agent",
        description="Updated description",
        status="disabled",
    )
    
    assert updated.description == "Updated description"
    assert updated.status == "disabled"


def test_delete_agent(agent_manager):
    """Test deleting an agent."""
    agent_manager.create_agent(name="test-agent", type="general")
    
    result = agent_manager.delete_agent("test-agent")
    
    assert result is True
    assert agent_manager.get_agent("test-agent") is None


def test_delete_nonexistent_agent(agent_manager):
    """Test deleting non-existent agent returns False."""
    result = agent_manager.delete_agent("nonexistent")
    assert result is False
