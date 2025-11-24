"""Agent management."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from mycli.storage.models import Agent as AgentModel
from mycli.storage.database import get_database
from mycli.ai import AIService, Message, OpenAIService
from mycli.config import get_config
from mycli.utils.logger import get_logger

logger = get_logger(__name__)


# Default system prompts for different agent types
DEFAULT_SYSTEM_PROMPTS = {
    "general": "You are a helpful AI assistant.",
    "developer": "You are an expert software developer assistant, helping with coding, debugging, and software design.",
    "devops": "You are a DevOps expert, assisting with automation, deployment, monitoring, and system administration.",
    "data_analyst": "You are a data analysis expert, helping with data processing, analysis, and visualization.",
}


class Agent:
    """Agent representation."""
    
    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        description: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        status: str = "enabled",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize agent.
        
        Args:
            id: Agent ID.
            name: Agent name.
            type: Agent type.
            description: Agent description.
            config: Agent configuration.
            status: Agent status.
            created_at: Creation time.
            updated_at: Update time.
            metadata: Additional metadata.
        """
        self.id = id
        self.name = name
        self.type = type
        self.description = description
        self.config = config or {}
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.metadata = metadata or {}
        
        self._ai_service: Optional[AIService] = None
    
    @property
    def ai_service(self) -> AIService:
        """Get AI service instance.
        
        Returns:
            AI service instance.
        """
        if self._ai_service is None:
            # Get provider from config
            provider = self.config.get("provider") or get_config().ai_service.default_provider
            
            if provider == "openai":
                self._ai_service = OpenAIService()
            else:
                raise ValueError(f"Unsupported AI provider: {provider}")
        
        return self._ai_service
    
    def get_system_prompt(self) -> str:
        """Get system prompt for this agent.
        
        Returns:
            System prompt.
        """
        # Use custom system prompt if configured
        if "system_prompt" in self.config:
            return self.config["system_prompt"]
        
        # Use default system prompt for agent type
        return DEFAULT_SYSTEM_PROMPTS.get(self.type, DEFAULT_SYSTEM_PROMPTS["general"])
    
    async def chat(
        self,
        message: str,
        history: Optional[List[Message]] = None,
        stream: bool = False,
    ) -> str:
        """Chat with agent.
        
        Args:
            message: User message.
            history: Chat history.
            stream: Whether to stream response.
        
        Returns:
            Assistant response.
        """
        # Build messages
        messages = []
        
        # Add system prompt
        messages.append(Message(role="system", content=self.get_system_prompt()))
        
        # Add history
        if history:
            messages.extend(history)
        
        # Add user message
        messages.append(Message(role="user", content=message))
        
        # Get AI service parameters
        model = self.config.get("model")
        temperature = self.config.get("temperature", 0.7)
        max_tokens = self.config.get("max_tokens")
        
        # Generate response
        if stream:
            # Stream response
            full_content = ""
            async for chunk in self.ai_service.complete_stream(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            ):
                full_content += chunk
                print(chunk, end="", flush=True)
            print()  # New line after streaming
            return full_content
        else:
            # Non-streaming response
            response = await self.ai_service.complete(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.content
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation.
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "config": self.config,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "metadata": self.metadata,
        }


class AgentManager:
    """Agent manager."""
    
    def __init__(self, db_session: Optional[Session] = None) -> None:
        """Initialize agent manager.
        
        Args:
            db_session: Database session. If None, create a new one.
        """
        self.db = get_database()
        self.db_session = db_session or self.db.get_session()
    
    def create_agent(
        self,
        name: str,
        type: str = "general",
        description: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> Agent:
        """Create a new agent.
        
        Args:
            name: Agent name.
            type: Agent type.
            description: Agent description.
            config: Agent configuration.
        
        Returns:
            Created agent.
        
        Raises:
            ValueError: If agent with same name exists.
        """
        # Check if agent already exists
        existing = self.db_session.query(AgentModel).filter_by(name=name).first()
        if existing:
            raise ValueError(f"Agent with name '{name}' already exists")
        
        # Create agent
        agent_id = str(uuid.uuid4())
        agent_model = AgentModel(
            id=agent_id,
            name=name,
            type=type,
            description=description,
            config=config or {},
            status="enabled",
        )
        
        self.db_session.add(agent_model)
        self.db_session.commit()
        
        logger.info(f"Created agent: {name} (id={agent_id})")
        
        return self._model_to_agent(agent_model)
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """Get agent by name.
        
        Args:
            name: Agent name.
        
        Returns:
            Agent instance or None.
        """
        agent_model = self.db_session.query(AgentModel).filter_by(name=name).first()
        if agent_model:
            return self._model_to_agent(agent_model)
        return None
    
    def get_agent_by_id(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID.
        
        Args:
            agent_id: Agent ID.
        
        Returns:
            Agent instance or None.
        """
        agent_model = self.db_session.query(AgentModel).filter_by(id=agent_id).first()
        if agent_model:
            return self._model_to_agent(agent_model)
        return None
    
    def list_agents(self, status: Optional[str] = None) -> List[Agent]:
        """List all agents.
        
        Args:
            status: Filter by status (enabled/disabled). If None, list all.
        
        Returns:
            List of agents.
        """
        query = self.db_session.query(AgentModel)
        if status:
            query = query.filter_by(status=status)
        
        agent_models = query.all()
        return [self._model_to_agent(model) for model in agent_models]
    
    def update_agent(
        self,
        name: str,
        description: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None,
    ) -> Agent:
        """Update agent.
        
        Args:
            name: Agent name.
            description: New description.
            config: New configuration.
            status: New status.
        
        Returns:
            Updated agent.
        
        Raises:
            ValueError: If agent not found.
        """
        agent_model = self.db_session.query(AgentModel).filter_by(name=name).first()
        if not agent_model:
            raise ValueError(f"Agent '{name}' not found")
        
        if description is not None:
            agent_model.description = description
        if config is not None:
            agent_model.config = config
        if status is not None:
            agent_model.status = status
        
        agent_model.updated_at = datetime.utcnow()
        
        self.db_session.commit()
        
        logger.info(f"Updated agent: {name}")
        
        return self._model_to_agent(agent_model)
    
    def delete_agent(self, name: str) -> bool:
        """Delete agent.
        
        Args:
            name: Agent name.
        
        Returns:
            True if deleted, False if not found.
        """
        agent_model = self.db_session.query(AgentModel).filter_by(name=name).first()
        if not agent_model:
            return False
        
        self.db_session.delete(agent_model)
        self.db_session.commit()
        
        logger.info(f"Deleted agent: {name}")
        
        return True
    
    def _model_to_agent(self, model: AgentModel) -> Agent:
        """Convert database model to Agent instance.
        
        Args:
            model: Database model.
        
        Returns:
            Agent instance.
        """
        return Agent(
            id=model.id,
            name=model.name,
            type=model.type,
            description=model.description,
            config=model.config,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            metadata=model.metadata_,
        )
    
    def close(self) -> None:
        """Close database session."""
        self.db_session.close()
