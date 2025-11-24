"""Configuration management for mycli."""

from pathlib import Path
from typing import Any, Dict, Optional
import os
import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AIServiceConfig(BaseSettings):
    """AI Service configuration."""
    
    default_provider: str = Field(default="openai", description="Default AI service provider")
    default_model: str = Field(default="gpt-3.5-turbo", description="Default model")
    timeout: int = Field(default=60, description="API request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    
    # API Keys (can be overridden by environment variables)
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_base_url: Optional[str] = Field(default=None, description="OpenAI API base URL")
    
    model_config = SettingsConfigDict(
        env_prefix="MYCLI_",
        case_sensitive=False,
    )


class CacheConfig(BaseSettings):
    """Cache configuration."""
    
    enabled: bool = Field(default=True, description="Enable caching")
    ttl: int = Field(default=3600, description="Cache TTL in seconds")
    max_size: int = Field(default=100, description="Maximum cache size in MB")
    
    model_config = SettingsConfigDict(
        env_prefix="MYCLI_CACHE_",
        case_sensitive=False,
    )


class REPLConfig(BaseSettings):
    """REPL configuration."""
    
    history_size: int = Field(default=1000, description="History size")
    auto_save: bool = Field(default=True, description="Auto-save sessions")
    theme: str = Field(default="default", description="Color theme")
    
    model_config = SettingsConfigDict(
        env_prefix="MYCLI_REPL_",
        case_sensitive=False,
    )


class GeneralConfig(BaseSettings):
    """General configuration."""
    
    default_agent: str = Field(default="default", description="Default agent name")
    log_level: str = Field(default="INFO", description="Log level")
    data_dir: Optional[Path] = Field(default=None, description="Data directory")
    
    model_config = SettingsConfigDict(
        env_prefix="MYCLI_",
        case_sensitive=False,
    )


class Config:
    """Main configuration class."""
    
    def __init__(self, config_path: Optional[Path] = None) -> None:
        """Initialize configuration.
        
        Args:
            config_path: Path to config file. If None, use default location.
        """
        self.config_path = config_path or self._get_default_config_path()
        self.general = GeneralConfig()
        self.ai_service = AIServiceConfig()
        self.cache = CacheConfig()
        self.repl = REPLConfig()
        
        # Load from file if exists
        if self.config_path.exists():
            self.load()
        else:
            # Create default config
            self._ensure_config_dir()
            self._ensure_data_dir()
    
    @staticmethod
    def _get_default_config_path() -> Path:
        """Get default config file path based on OS."""
        if os.name == 'nt':  # Windows
            config_dir = Path(os.environ.get('APPDATA', '~')) / 'mycli'
        else:  # Linux/macOS
            config_dir = Path.home() / '.config' / 'mycli'
        
        return config_dir / 'config.yaml'
    
    def _ensure_config_dir(self) -> None:
        """Ensure config directory exists."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _ensure_data_dir(self) -> None:
        """Ensure data directory exists."""
        data_dir = self.get_data_dir()
        data_dir.mkdir(parents=True, exist_ok=True)
    
    def get_data_dir(self) -> Path:
        """Get data directory path."""
        if self.general.data_dir:
            return self.general.data_dir
        
        # Default data directory
        if os.name == 'nt':  # Windows
            data_dir = Path(os.environ.get('LOCALAPPDATA', '~')) / 'mycli' / 'data'
        else:  # Linux/macOS
            data_dir = Path.home() / '.local' / 'share' / 'mycli'
        
        return data_dir
    
    def load(self) -> None:
        """Load configuration from file."""
        if not self.config_path.exists():
            return
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        
        # Update configurations
        if 'general' in data:
            for key, value in data['general'].items():
                if hasattr(self.general, key):
                    setattr(self.general, key, value)
        
        if 'ai_service' in data:
            for key, value in data['ai_service'].items():
                if hasattr(self.ai_service, key):
                    setattr(self.ai_service, key, value)
        
        if 'cache' in data:
            for key, value in data['cache'].items():
                if hasattr(self.cache, key):
                    setattr(self.cache, key, value)
        
        if 'repl' in data:
            for key, value in data['repl'].items():
                if hasattr(self.repl, key):
                    setattr(self.repl, key, value)
    
    def save(self) -> None:
        """Save configuration to file."""
        self._ensure_config_dir()
        
        data: Dict[str, Any] = {
            'general': {
                'default_agent': self.general.default_agent,
                'log_level': self.general.log_level,
                'data_dir': str(self.general.data_dir) if self.general.data_dir else None,
            },
            'ai_service': {
                'default_provider': self.ai_service.default_provider,
                'default_model': self.ai_service.default_model,
                'timeout': self.ai_service.timeout,
                'max_retries': self.ai_service.max_retries,
                # Don't save API keys to file for security
            },
            'cache': {
                'enabled': self.cache.enabled,
                'ttl': self.cache.ttl,
                'max_size': self.cache.max_size,
            },
            'repl': {
                'history_size': self.repl.history_size,
                'auto_save': self.repl.auto_save,
                'theme': self.repl.theme,
            },
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    
    def validate(self) -> bool:
        """Validate configuration.
        
        Returns:
            True if configuration is valid.
        """
        # Check if API key is available
        if self.ai_service.default_provider == 'openai':
            if not self.ai_service.openai_api_key:
                return False
        
        return True


# Global config instance
_config: Optional[Config] = None


def get_config(config_path: Optional[Path] = None) -> Config:
    """Get global config instance.
    
    Args:
        config_path: Optional config file path.
    
    Returns:
        Config instance.
    """
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config
