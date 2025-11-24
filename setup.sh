#!/bin/bash
# Quick setup and test script for mycli

set -e  # Exit on error

echo "======================================"
echo "mycli Setup and Test Script"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo ""
    echo "⚠️  Not in a virtual environment!"
    echo "It's recommended to use a virtual environment."
    echo ""
    read -p "Create and activate a virtual environment? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        echo "Please activate it with:"
        echo "  source venv/bin/activate  # Linux/macOS"
        echo "  venv\\Scripts\\activate     # Windows"
        echo ""
        echo "Then run this script again."
        exit 0
    fi
fi

# Install in development mode
echo ""
echo "Installing mycli in development mode..."
pip install -e ".[dev,openai]"

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""

# Run tests
echo "Running tests..."
pytest -v

echo ""
echo "======================================"
echo "Tests Complete!"
echo "======================================"
echo ""

# Show available commands
echo "Available commands:"
echo "  mycli --help              Show help"
echo "  mycli --version           Show version"
echo "  mycli config init         Initialize configuration"
echo "  mycli agent create        Create an agent"
echo "  mycli agent list          List agents"
echo "  mycli chat \"message\"      Chat with agent"
echo "  mycli repl                Start REPL mode"
echo ""

# Check for API key
if [ -z "$MYCLI_OPENAI_API_KEY" ]; then
    echo "⚠️  OpenAI API key not set!"
    echo ""
    echo "To use mycli with OpenAI, set your API key:"
    echo "  export MYCLI_OPENAI_API_KEY='your-api-key'"
    echo ""
    echo "Or run the configuration wizard:"
    echo "  mycli config init"
    echo ""
else
    echo "✓ OpenAI API key is set"
    echo ""
fi

echo "======================================"
echo "Setup complete! Try these commands:"
echo "======================================"
echo ""
echo "1. Initialize config:"
echo "   mycli config init"
echo ""
echo "2. Create your first agent:"
echo "   mycli agent create --name assistant --type general"
echo ""
echo "3. Chat with the agent:"
echo "   mycli chat \"Hello, how are you?\""
echo ""
echo "4. Start interactive mode:"
echo "   mycli repl"
echo ""
echo "For more information, see:"
echo "  - README.md"
echo "  - docs/QUICKSTART.md"
echo "  - docs/DEVELOPMENT.md"
echo ""
