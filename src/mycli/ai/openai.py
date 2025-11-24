"""OpenAI service implementation."""

from typing import Any, AsyncIterator, Dict, List, Optional
import httpx

from mycli.ai.base import AIService, Message, CompletionResponse
from mycli.config import get_config
from mycli.utils.logger import get_logger

logger = get_logger(__name__)


class OpenAIService(AIService):
    """OpenAI API service implementation."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3,
    ) -> None:
        """Initialize OpenAI service.
        
        Args:
            api_key: OpenAI API key. If None, load from config.
            base_url: API base URL. If None, use default.
            timeout: Request timeout in seconds.
            max_retries: Maximum retry attempts.
        """
        config = get_config()
        
        self.api_key = api_key or config.ai_service.openai_api_key
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        self.base_url = base_url or config.ai_service.openai_base_url or "https://api.openai.com/v1"
        self.timeout = timeout or config.ai_service.timeout
        self.max_retries = max_retries or config.ai_service.max_retries
        self.default_model = config.ai_service.default_model
        
        # Create HTTP client
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=self.timeout,
        )
    
    async def complete(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> CompletionResponse:
        """Generate completion using OpenAI API.
        
        Args:
            messages: Chat messages.
            model: Model name.
            temperature: Generation temperature.
            max_tokens: Maximum tokens to generate.
            stream: Whether to stream (not used in this method).
            **kwargs: Additional OpenAI parameters.
        
        Returns:
            Completion response.
        """
        model = model or self.default_model
        
        # Convert messages to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Prepare request payload
        payload: Dict[str, Any] = {
            "model": model,
            "messages": openai_messages,
            "temperature": temperature,
            **kwargs,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        # Make API request with retry
        for attempt in range(self.max_retries):
            try:
                response = await self.client.post(
                    "/chat/completions",
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                
                # Extract response
                choice = data["choices"][0]
                return CompletionResponse(
                    content=choice["message"]["content"],
                    role=choice["message"]["role"],
                    finish_reason=choice.get("finish_reason"),
                    usage=data.get("usage"),
                )
            
            except httpx.HTTPStatusError as e:
                logger.error(f"OpenAI API error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt == self.max_retries - 1:
                    raise
            except Exception as e:
                logger.error(f"Unexpected error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt == self.max_retries - 1:
                    raise
        
        raise RuntimeError("Failed to complete request after retries")
    
    async def complete_stream(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """Generate streaming completion using OpenAI API.
        
        Args:
            messages: Chat messages.
            model: Model name.
            temperature: Generation temperature.
            max_tokens: Maximum tokens to generate.
            **kwargs: Additional OpenAI parameters.
        
        Yields:
            Content chunks.
        """
        model = model or self.default_model
        
        # Convert messages to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Prepare request payload
        payload: Dict[str, Any] = {
            "model": model,
            "messages": openai_messages,
            "temperature": temperature,
            "stream": True,
            **kwargs,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        # Make streaming request
        async with self.client.stream("POST", "/chat/completions", json=payload) as response:
            response.raise_for_status()
            
            async for line in response.aiter_lines():
                if not line or line == "data: [DONE]":
                    continue
                
                if line.startswith("data: "):
                    try:
                        import json
                        data = json.loads(line[6:])
                        delta = data["choices"][0]["delta"]
                        if "content" in delta:
                            yield delta["content"]
                    except (json.JSONDecodeError, KeyError, IndexError) as e:
                        logger.warning(f"Failed to parse streaming chunk: {e}")
                        continue
    
    async def validate_connection(self) -> bool:
        """Validate OpenAI API connection.
        
        Returns:
            True if connection is valid.
        """
        try:
            response = await self.client.get("/models")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to validate OpenAI connection: {e}")
            return False
    
    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()
