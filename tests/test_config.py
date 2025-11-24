"""Test configuration module."""

import tempfile
from pathlib import Path
import pytest

from mycli.config import Config


def test_config_initialization():
    """Test config initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        config = Config(config_path=config_path)
        
        assert config.config_path == config_path
        assert config.general.default_agent == "default"
        assert config.ai_service.default_provider == "openai"


def test_config_save_and_load():
    """Test config save and load."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        
        # Create and save config
        config = Config(config_path=config_path)
        config.general.default_agent = "test-agent"
        config.ai_service.default_model = "gpt-4"
        config.save()
        
        # Load config
        config2 = Config(config_path=config_path)
        config2.load()
        
        assert config2.general.default_agent == "test-agent"
        assert config2.ai_service.default_model == "gpt-4"


def test_config_data_dir():
    """Test data directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        config = Config(config_path=config_path)
        
        data_dir = config.get_data_dir()
        assert isinstance(data_dir, Path)
