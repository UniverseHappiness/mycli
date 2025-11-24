# Contributing to mycli

Thank you for your interest in contributing to mycli! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, mycli version)
- Relevant logs or error messages

### Suggesting Features

We welcome feature suggestions! Please create an issue with:

- Clear description of the feature
- Use cases and benefits
- Possible implementation approach (optional)

### Submitting Pull Requests

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/mycli.git
   cd mycli
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e ".[dev,openai]"
   ```

4. **Make Your Changes**
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

5. **Test Your Changes**
   ```bash
   # Run tests
   pytest
   
   # Check code quality
   black src tests
   ruff check src tests
   mypy src
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
   
   Commit message guidelines:
   - Use present tense ("Add feature" not "Added feature")
   - Be descriptive but concise
   - Reference issues if applicable (#123)

7. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then create a Pull Request on GitHub with:
   - Clear title and description
   - Link to related issues
   - Screenshots if applicable

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and reasonably sized
- Use meaningful variable and function names

Example:

```python
def create_agent(
    name: str,
    type: str,
    description: Optional[str] = None,
) -> Agent:
    """Create a new agent.
    
    Args:
        name: Agent name.
        type: Agent type.
        description: Optional agent description.
    
    Returns:
        Created agent instance.
    
    Raises:
        ValueError: If agent with same name exists.
    """
    # Implementation
    pass
```

### Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Use pytest fixtures for setup/teardown
- Mock external dependencies
- Test both success and error cases

Example:

```python
def test_create_agent(agent_manager):
    """Test creating an agent."""
    agent = agent_manager.create_agent(
        name="test-agent",
        type="general",
    )
    assert agent.name == "test-agent"
    assert agent.type == "general"
```

### Documentation

- Update README.md if adding major features
- Add docstrings to all public APIs
- Update relevant documentation in docs/
- Include examples for new functionality

### Commit Messages

Use conventional commit format:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

Examples:
```
feat(agent): add support for custom system prompts
fix(cli): handle missing config file gracefully
docs(readme): update installation instructions
```

## Project Structure

```
mycli/
├── src/mycli/           # Source code
│   ├── ai/              # AI service implementations
│   ├── config/          # Configuration management
│   ├── core/            # Core business logic
│   ├── repl/            # REPL interface
│   ├── storage/         # Database layer
│   └── utils/           # Utility functions
├── tests/               # Test files
├── docs/                # Documentation
└── pyproject.toml       # Project configuration
```

## Review Process

1. Automated checks must pass (tests, linting, type checking)
2. Code review by maintainers
3. Address any feedback
4. Once approved, PR will be merged

## Getting Help

- GitHub Issues: For bugs and feature requests
- GitHub Discussions: For questions and discussions
- Documentation: Check docs/ directory

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to mycli! 🎉
