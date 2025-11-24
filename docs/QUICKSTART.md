# Quick Start Guide

## Installation

### From PyPI (when published)

```bash
pip install mycli
```

### From Source

```bash
git clone https://github.com/mycli/mycli.git
cd mycli
pip install -e ".[dev,openai]"
```

## Initial Setup

### 1. Configure API Key

You can set your OpenAI API key in two ways:

**Method 1: Environment Variable (Recommended)**

```bash
export MYCLI_OPENAI_API_KEY="your-api-key-here"
```

Add this to your `~/.bashrc` or `~/.zshrc` to make it permanent.

**Method 2: Configuration Wizard**

```bash
mycli config init
```

### 2. Verify Installation

```bash
mycli --version
mycli --help
```

## Basic Usage

### Create Your First Agent

```bash
# Create a general purpose agent
mycli agent create --name assistant --type general

# Create a developer agent
mycli agent create --name dev --type developer --description "Coding assistant"

# List all agents
mycli agent list
```

### Chat with an Agent

**Quick Question (Command Mode)**

```bash
# Using default agent
mycli chat "What is Python?"

# Using specific agent
mycli chat --agent dev "Explain async/await in Python"

# Stream the response
mycli chat --stream "Tell me a story"
```

**Interactive Session (REPL Mode)**

```bash
# Start REPL with default agent
mycli repl

# Start REPL with specific agent
mycli repl --agent dev
```

In REPL mode, you can use these commands:
- `/help` - Show help
- `/exit` or `/quit` - Exit REPL
- `/clear` - Clear chat history
- `/save` - Save current session
- `/agent [name]` - Switch agent or show current
- `/history` - Show chat history

### Manage Agents

```bash
# View agent details
mycli agent show assistant

# Update agent
mycli agent update assistant --description "My helpful assistant"
mycli agent update assistant --model gpt-4

# Disable/enable agent
mycli agent update assistant --disable
mycli agent update assistant --enable

# Delete agent
mycli agent delete assistant
```

### Configuration Management

```bash
# View current configuration
mycli config show

# Initialize/update configuration
mycli config init
```

## Advanced Usage

### Using with Pipes

```bash
# Analyze code from file
cat myfile.py | mycli chat "Review this code"

# Save response to file
mycli chat "Generate a README" > README.md

# Process output
mycli chat "List 10 random numbers" | grep -o "[0-9]+"
```

### Custom Configuration

Create a configuration file at `~/.config/mycli/config.yaml`:

```yaml
general:
  default_agent: dev
  log_level: INFO

ai_service:
  default_model: gpt-4
  timeout: 120
```

See `config.example.yaml` for all available options.

### Environment Variables

All configuration options can be set via environment variables with the `MYCLI_` prefix:

```bash
export MYCLI_DEFAULT_AGENT=dev
export MYCLI_LOG_LEVEL=DEBUG
export MYCLI_OPENAI_API_KEY=sk-...
export MYCLI_AI_SERVICE_DEFAULT_MODEL=gpt-4
```

## Troubleshooting

### API Key Issues

If you get "API key not configured" error:

1. Verify environment variable is set: `echo $MYCLI_OPENAI_API_KEY`
2. Run `mycli config init` to set it in config file
3. Check if key is valid

### Permission Errors

If you get permission errors accessing config/data directories:

```bash
# Check permissions
ls -la ~/.config/mycli
ls -la ~/.local/share/mycli

# Fix permissions if needed
chmod 755 ~/.config/mycli
chmod 755 ~/.local/share/mycli
```

### Verbose Logging

Enable verbose logging for debugging:

```bash
mycli --verbose agent list
mycli --verbose chat "test"
```

Check logs at: `~/.local/share/mycli/logs/mycli.log`

## Next Steps

- Read the full documentation (coming soon)
- Explore example workflows
- Contribute to the project
- Join the community

## Getting Help

- GitHub Issues: https://github.com/mycli/mycli/issues
- Documentation: https://mycli.readthedocs.io
- Discussions: https://github.com/mycli/mycli/discussions
