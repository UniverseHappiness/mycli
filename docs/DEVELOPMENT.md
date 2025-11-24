# Development Guide

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip and virtualenv
- Git

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/mycli/mycli.git
cd mycli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev,openai]"
```

## Project Structure

```
mycli/
├── src/mycli/           # Source code
│   ├── __init__.py
│   ├── cli.py           # CLI entry point
│   ├── ai/              # AI service layer
│   │   ├── base.py      # Base interface
│   │   └── openai.py    # OpenAI implementation
│   ├── config/          # Configuration management
│   ├── core/            # Core business logic
│   │   └── agent.py     # Agent management
│   ├── repl/            # REPL interface
│   ├── storage/         # Database layer
│   │   ├── models.py    # Data models
│   │   └── database.py  # Database operations
│   └── utils/           # Utility functions
│       └── logger.py    # Logging setup
├── tests/               # Test files
├── docs/                # Documentation
├── pyproject.toml       # Project configuration
└── README.md
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mycli --cov-report=html

# Run specific test file
pytest tests/test_agent.py

# Run specific test
pytest tests/test_agent.py::test_create_agent

# Run with verbose output
pytest -v
```

## Code Quality

### Formatting

```bash
# Format code with black
black src tests

# Check formatting without changes
black --check src tests
```

### Linting

```bash
# Lint with ruff
ruff check src tests

# Auto-fix issues
ruff check --fix src tests
```

### Type Checking

```bash
# Type check with mypy
mypy src
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following the project style
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run tests
pytest

# Check code quality
black src tests
ruff check src tests
mypy src
```

### 4. Commit and Push

```bash
git add .
git commit -m "Description of your changes"
git push origin feature/your-feature-name
```

### 5. Create Pull Request

- Open a PR on GitHub
- Describe your changes
- Wait for review

## Adding New Features

### Adding a New AI Provider

1. Create a new file in `src/mycli/ai/` (e.g., `anthropic.py`)
2. Implement the `AIService` interface
3. Register the provider in `src/mycli/ai/__init__.py`
4. Add configuration options to `src/mycli/config/__init__.py`
5. Update documentation

Example:

```python
# src/mycli/ai/anthropic.py
from mycli.ai.base import AIService, Message, CompletionResponse

class AnthropicService(AIService):
    async def complete(self, messages, **kwargs):
        # Implementation
        pass
    
    async def complete_stream(self, messages, **kwargs):
        # Implementation
        pass
    
    async def validate_connection(self):
        # Implementation
        pass
```

### Adding a New Command

1. Add command function to `src/mycli/cli.py`
2. Use Click decorators for options and arguments
3. Add tests in `tests/`
4. Update documentation

Example:

```python
@cli.command()
@click.argument("name")
@click.option("--option", help="An option")
def mycommand(name, option):
    """Command description."""
    # Implementation
    pass
```

## Testing Guidelines

### Writing Tests

- Use pytest fixtures for setup/teardown
- Test both success and error cases
- Mock external dependencies
- Keep tests focused and readable

Example:

```python
def test_agent_creation(agent_manager):
    """Test creating an agent."""
    agent = agent_manager.create_agent(
        name="test",
        type="general"
    )
    assert agent.name == "test"
    assert agent.type == "general"
```

### Test Coverage

Aim for at least 80% code coverage. Check coverage report:

```bash
pytest --cov=mycli --cov-report=html
# Open htmlcov/index.html in browser
```

## Debugging

### Enable Debug Logging

```bash
mycli --verbose agent list
```

### Python Debugger

Add breakpoint in code:

```python
import pdb; pdb.set_trace()
```

Or use IDE debugger (VS Code, PyCharm, etc.)

### Check Logs

Logs are stored at: `~/.local/share/mycli/logs/mycli.log`

```bash
tail -f ~/.local/share/mycli/logs/mycli.log
```

## Common Issues

### Import Errors

Make sure to install in development mode:

```bash
pip install -e ".[dev,openai]"
```

### Database Issues

Delete the database and recreate:

```bash
rm ~/.local/share/mycli/mycli.db
# Run mycli again to recreate
```

### Configuration Issues

Reset configuration:

```bash
rm ~/.config/mycli/config.yaml
mycli config init
```

## Release Process

1. Update version in `pyproject.toml` and `src/mycli/__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v0.1.0`
4. Push tag: `git push origin v0.1.0`
5. Build package: `python -m build`
6. Upload to PyPI: `python -m twine upload dist/*`

## Contributing

See CONTRIBUTING.md for contribution guidelines.

## Resources

- Python Packaging: https://packaging.python.org
- Click Documentation: https://click.palletsprojects.com
- SQLAlchemy: https://www.sqlalchemy.org
- Pytest: https://docs.pytest.org
