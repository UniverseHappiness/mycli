"""AI service base interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict, List, Optional


@dataclass
class Message:
    """Chat message."""
    
    role: str  # 'user', 'assistant', 'system'
    content: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class CompletionResponse:
    """Completion response."""
    
    content: str
    role: str = "assistant"
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    metadata: Optional[Dict[str, Any]] = None


class AIService(ABC):
    """Base class for AI services."""
    
    @abstractmethod
    async def complete(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> CompletionResponse:
        """Generate completion.
        
        Args:
            messages: Chat messages.
            model: Model name.
            temperature: Generation temperature (0.0-2.0).
            max_tokens: Maximum tokens to generate.
            stream: Whether to stream response.
            **kwargs: Additional parameters.
        
        Returns:
            Completion response.
        """
        pass
    
    @abstractmethod
    async def complete_stream(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """Generate streaming completion.
        
        Args:
            messages: Chat messages.
            model: Model name.
            temperature: Generation temperature (0.0-2.0).
            max_tokens: Maximum tokens to generate.
            **kwargs: Additional parameters.
        
        Yields:
            Content chunks.
        """
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """Validate service connection.
        
        Returns:
            True if connection is valid.
        """
        pass
