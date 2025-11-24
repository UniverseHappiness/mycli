"""REPL (Read-Eval-Print Loop) interface for mycli."""

import asyncio
import sys
import uuid
from datetime import datetime
from typing import List, Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.markdown import Markdown

from mycli.config import get_config
from mycli.core.agent import AgentManager
from mycli.storage.database import get_database
from mycli.storage.models import Session as SessionModel
from mycli.ai import Message
from mycli.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


class REPLSession:
    """REPL session manager."""
    
    def __init__(self, agent_name: Optional[str] = None) -> None:
        """Initialize REPL session.
        
        Args:
            agent_name: Agent name to use. If None, use default.
        """
        self.config = get_config()
        self.agent_manager = AgentManager()
        
        # Get agent
        agent_name = agent_name or self.config.general.default_agent
        self.agent = self.agent_manager.get_agent(agent_name)
        
        if not self.agent:
            # Create default agent if not exists
            if agent_name == "default":
                console.print("[yellow]Creating default agent...[/yellow]")
                self.agent = self.agent_manager.create_agent(
                    name="default",
                    type="general",
                    description="Default agent",
                )
            else:
                raise ValueError(f"Agent '{agent_name}' not found")
        
        # Session data
        self.session_id = str(uuid.uuid4())
        self.messages: List[Message] = []
        
        # Setup prompt
        history_file = self.config.get_data_dir() / "repl_history.txt"
        history_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.prompt_session = PromptSession(
            history=FileHistory(str(history_file)),
            auto_suggest=AutoSuggestFromHistory(),
            completer=WordCompleter(
                ["/help", "/exit", "/clear", "/save", "/agent", "/history"],
                ignore_case=True,
            ),
        )
    
    def print_welcome(self) -> None:
        """Print welcome message."""
        console.print("\n[bold cyan]Welcome to mycli REPL![/bold cyan]")
        console.print(f"Using agent: [green]{self.agent.name}[/green] ({self.agent.type})")
        console.print("\nType your message and press Enter to chat.")
        console.print("Special commands: [dim]/help /exit /clear /save /agent /history[/dim]\n")
    
    def print_help(self) -> None:
        """Print help message."""
        help_text = """
## REPL Commands

- `/help` - Show this help message
- `/exit` or `/quit` - Exit the REPL
- `/clear` - Clear chat history
- `/save` - Save current session
- `/agent [name]` - Switch to another agent or show current agent
- `/history` - Show chat history
"""
        console.print(Markdown(help_text))
    
    def print_history(self) -> None:
        """Print chat history."""
        if not self.messages:
            console.print("[dim]No messages yet[/dim]")
            return
        
        console.print("\n[bold]Chat History:[/bold]")
        for msg in self.messages:
            role_color = "cyan" if msg.role == "user" else "green"
            console.print(f"\n[{role_color}]{msg.role.upper()}:[/{role_color}]")
            console.print(msg.content)
    
    def save_session(self) -> None:
        """Save current session to database."""
        if not self.messages:
            console.print("[yellow]No messages to save[/yellow]")
            return
        
        try:
            db = get_database()
            db_session = db.get_session()
            
            # Convert messages to dict
            messages_data = [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": datetime.utcnow().isoformat(),
                }
                for msg in self.messages
            ]
            
            # Create session model
            session_model = SessionModel(
                id=self.session_id,
                title=f"REPL Session - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
                agent_id=self.agent.id,
                messages=messages_data,
            )
            
            db_session.add(session_model)
            db_session.commit()
            db_session.close()
            
            console.print(f"[green]✓[/green] Session saved (ID: {self.session_id})")
        
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            console.print(f"[red]✗[/red] Failed to save session: {e}")
    
    async def run(self) -> None:
        """Run REPL loop."""
        self.print_welcome()
        
        try:
            while True:
                try:
                    # Get user input
                    user_input = await self.prompt_session.prompt_async(">>> ")
                    user_input = user_input.strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle special commands
                    if user_input.startswith("/"):
                        await self.handle_command(user_input)
                        continue
                    
                    # Add user message
                    user_message = Message(role="user", content=user_input)
                    self.messages.append(user_message)
                    
                    # Get agent response
                    console.print("\n[green]Assistant:[/green]")
                    
                    response = await self.agent.chat(
                        message=user_input,
                        history=self.messages[:-1],  # Exclude the last user message
                        stream=True,
                    )
                    
                    # Add assistant message
                    assistant_message = Message(role="assistant", content=response)
                    self.messages.append(assistant_message)
                    
                    console.print()  # Empty line
                
                except KeyboardInterrupt:
                    console.print("\n[dim]Press Ctrl+C again or type /exit to quit[/dim]")
                    continue
                except EOFError:
                    break
        
        finally:
            # Auto-save if configured
            if self.config.repl.auto_save and self.messages:
                self.save_session()
            
            # Cleanup
            self.agent_manager.close()
            console.print("\n[dim]Goodbye![/dim]")
    
    async def handle_command(self, command: str) -> None:
        """Handle special commands.
        
        Args:
            command: Command string.
        """
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd in ["/exit", "/quit"]:
            raise EOFError()
        
        elif cmd == "/help":
            self.print_help()
        
        elif cmd == "/clear":
            self.messages.clear()
            console.print("[green]✓[/green] Chat history cleared")
        
        elif cmd == "/save":
            self.save_session()
        
        elif cmd == "/history":
            self.print_history()
        
        elif cmd == "/agent":
            if len(parts) > 1:
                # Switch agent
                new_agent_name = parts[1]
                new_agent = self.agent_manager.get_agent(new_agent_name)
                
                if new_agent:
                    # Save current session
                    if self.config.repl.auto_save and self.messages:
                        self.save_session()
                    
                    # Switch to new agent
                    self.agent = new_agent
                    self.session_id = str(uuid.uuid4())
                    self.messages.clear()
                    
                    console.print(f"[green]✓[/green] Switched to agent: {self.agent.name}")
                else:
                    console.print(f"[red]✗[/red] Agent '{new_agent_name}' not found")
            else:
                # Show current agent
                console.print(f"Current agent: [green]{self.agent.name}[/green] ({self.agent.type})")
        
        else:
            console.print(f"[red]Unknown command: {cmd}[/red]")
            console.print("[dim]Type /help for available commands[/dim]")


def start_repl(agent: Optional[str] = None) -> None:
    """Start REPL session.
    
    Args:
        agent: Agent name to use.
    """
    try:
        session = REPLSession(agent_name=agent)
        asyncio.run(session.run())
    except Exception as e:
        logger.error(f"REPL error: {e}", exc_info=True)
        console.print(f"[red]✗[/red] Error: {e}", err=True)
        sys.exit(1)
