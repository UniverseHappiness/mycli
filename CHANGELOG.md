# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-11-24

### Added

- Initial release of mycli
- Basic CLI framework using Click
- Agent management commands (create, list, show, update, delete)
- Chat command for single-question interactions
- REPL mode for continuous conversations
- Configuration management system
- OpenAI API integration as first AI service provider
- SQLite-based data persistence for agents and sessions
- Structured logging with loguru
- Rich terminal output with colors and tables
- Command history and auto-suggestion in REPL
- Auto-save sessions in REPL mode
- Environment variable support for configuration
- Comprehensive documentation (README, QUICKSTART, DEVELOPMENT)
- Basic test coverage for core modules
- Project packaging with pyproject.toml

### Features

**Agent Management**
- Create agents with different types (general, developer, devops, data_analyst)
- Configure agent parameters (model, temperature, max_tokens, system_prompt)
- Enable/disable agents
- List and filter agents
- View detailed agent information
- Delete agents with confirmation

**Chat Capabilities**
- Command mode: Quick one-off questions
- REPL mode: Continuous conversations with context
- Streaming responses for real-time output
- Chat history management
- Session persistence
- Agent switching in REPL

**Configuration**
- YAML-based configuration files
- Environment variable overrides
- Configuration wizard (mycli config init)
- Secure API key management
- Platform-specific default locations

**Developer Experience**
- Type hints throughout codebase
- Comprehensive docstrings
- Unit tests with pytest
- Code formatting with black
- Linting with ruff
- Example configuration files
- Development documentation

### Technical Details

- Python 3.9+ support
- Async/await for AI service calls
- SQLAlchemy 2.0 for database operations
- Click for CLI framework
- Prompt Toolkit for REPL
- Rich for terminal formatting
- Pydantic for configuration validation

### Documentation

- README with project overview and quick examples
- QUICKSTART guide for new users
- DEVELOPMENT guide for contributors
- CONTRIBUTING guidelines
- Example configuration file
- Inline code documentation

### Known Limitations

- Only OpenAI provider supported (more coming soon)
- No local LLM support yet
- No task automation or workflow features
- No plugin system
- No HTTP API server
- Limited test coverage (expanding in next release)

## [0.1.0-alpha] - 2025-11-24

### Added

- Project scaffolding
- Basic structure and dependencies
- Initial development setup

---

[Unreleased]: https://github.com/mycli/mycli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/mycli/mycli/releases/tag/v0.1.0
[0.1.0-alpha]: https://github.com/mycli/mycli/releases/tag/v0.1.0-alpha
