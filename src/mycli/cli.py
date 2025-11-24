"""CLI interface for mycli."""

import sys
import asyncio
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.table import Table

from mycli import __version__
from mycli.config import get_config
from mycli.utils.logger import setup_logging, get_logger
from mycli.core.agent import AgentManager
from mycli.ai import Message
from mycli.repl import start_repl

console = Console()
logger = get_logger(__name__)


@click.group()
@click.version_option(version=__version__)
@click.option("--config", "-c", type=click.Path(exists=True, path_type=Path), help="Config file path")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--quiet", "-q", is_flag=True, help="Quiet mode")
@click.pass_context
def cli(ctx: click.Context, config: Optional[Path], verbose: bool, quiet: bool) -> None:
    """mycli - An intelligent Agent CLI tool for developers."""
    # Setup context
    ctx.ensure_object(dict)
    
    # Setup logging
    log_level = "DEBUG" if verbose else ("ERROR" if quiet else "INFO")
    setup_logging(log_level=log_level)
    
    # Load config
    if config:
        ctx.obj["config_path"] = config
    
    logger.debug("CLI initialized")


# Agent management commands
@cli.group()
def agent() -> None:
    """Manage agents."""
    pass


@agent.command("list")
@click.option("--format", "-f", type=click.Choice(["table", "json"]), default="table", help="Output format")
def agent_list(format: str) -> None:
    """List all agents."""
    manager = AgentManager()
    agents = manager.list_agents()
    
    if format == "json":
        import json
        console.print(json.dumps([a.to_dict() for a in agents], indent=2))
    else:
        table = Table(title="Agents")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Description")
        
        for agent in agents:
            table.add_row(
                agent.name,
                agent.type,
                agent.status,
                agent.description or ""
            )
        
        console.print(table)
    
    manager.close()


@agent.command("create")
@click.option("--name", "-n", required=True, help="Agent name")
@click.option("--type", "-t", type=click.Choice(["general", "developer", "devops", "data_analyst"]), default="general", help="Agent type")
@click.option("--description", "-d", help="Agent description")
@click.option("--model", "-m", help="AI model to use")
def agent_create(name: str, type: str, description: Optional[str], model: Optional[str]) -> None:
    """Create a new agent."""
    manager = AgentManager()
    
    try:
        config = {}
        if model:
            config["model"] = model
        
        agent = manager.create_agent(
            name=name,
            type=type,
            description=description,
            config=config,
        )
        console.print(f"[green]✓[/green] Created agent: {agent.name}")
    except ValueError as e:
        console.print(f"[red]✗[/red] Error: {e}", err=True)
        sys.exit(1)
    finally:
        manager.close()


@agent.command("show")
@click.argument("name")
def agent_show(name: str) -> None:
    """Show agent details."""
    manager = AgentManager()
    
    try:
        agent = manager.get_agent(name)
        if not agent:
            console.print(f"[red]✗[/red] Agent '{name}' not found", err=True)
            sys.exit(1)
        
        console.print(f"\n[bold]Agent: {agent.name}[/bold]")
        console.print(f"ID: {agent.id}")
        console.print(f"Type: {agent.type}")
        console.print(f"Status: {agent.status}")
        console.print(f"Description: {agent.description or 'N/A'}")
        console.print(f"Created: {agent.created_at}")
        console.print(f"Updated: {agent.updated_at}")
        console.print(f"\nConfiguration:")
        
        for key, value in agent.config.items():
            console.print(f"  {key}: {value}")
    
    finally:
        manager.close()


@agent.command("delete")
@click.argument("name")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def agent_delete(name: str, yes: bool) -> None:
    """Delete an agent."""
    if not yes:
        if not click.confirm(f"Are you sure you want to delete agent '{name}'?"):
            console.print("Cancelled")
            return
    
    manager = AgentManager()
    
    try:
        if manager.delete_agent(name):
            console.print(f"[green]✓[/green] Deleted agent: {name}")
        else:
            console.print(f"[red]✗[/red] Agent '{name}' not found", err=True)
            sys.exit(1)
    finally:
        manager.close()


@agent.command("update")
@click.argument("name")
@click.option("--description", "-d", help="New description")
@click.option("--model", "-m", help="New AI model")
@click.option("--enable", is_flag=True, help="Enable agent")
@click.option("--disable", is_flag=True, help="Disable agent")
def agent_update(
    name: str,
    description: Optional[str],
    model: Optional[str],
    enable: bool,
    disable: bool,
) -> None:
    """Update agent configuration."""
    manager = AgentManager()
    
    try:
        agent = manager.get_agent(name)
        if not agent:
            console.print(f"[red]✗[/red] Agent '{name}' not found", err=True)
            sys.exit(1)
        
        config = agent.config.copy() if model else None
        if model:
            config["model"] = model
        
        status = None
        if enable:
            status = "enabled"
        elif disable:
            status = "disabled"
        
        manager.update_agent(
            name=name,
            description=description,
            config=config,
            status=status,
        )
        
        console.print(f"[green]✓[/green] Updated agent: {name}")
    
    except ValueError as e:
        console.print(f"[red]✗[/red] Error: {e}", err=True)
        sys.exit(1)
    finally:
        manager.close()


# Chat command
@cli.command()
@click.argument("message", required=False)
@click.option("--agent", "-a", help="Agent to use")
@click.option("--stream", "-s", is_flag=True, help="Stream response")
def chat(message: Optional[str], agent: Optional[str], stream: bool) -> None:
    """Chat with an agent."""
    async def _chat():
        manager = AgentManager()
        
        try:
            # Get agent
            agent_name = agent or get_config().general.default_agent
            agent_obj = manager.get_agent(agent_name)
            
            if not agent_obj:
                # Create default agent if not exists
                if agent_name == "default":
                    console.print("[yellow]Creating default agent...[/yellow]")
                    agent_obj = manager.create_agent(
                        name="default",
                        type="general",
                        description="Default agent",
                    )
                else:
                    console.print(f"[red]✗[/red] Agent '{agent_name}' not found", err=True)
                    sys.exit(1)
            
            # Get message from stdin if not provided
            if not message:
                if sys.stdin.isatty():
                    console.print("[red]✗[/red] No message provided", err=True)
                    sys.exit(1)
                user_message = sys.stdin.read().strip()
            else:
                user_message = message
            
            # Chat with agent
            response = await agent_obj.chat(user_message, stream=stream)
            
            if not stream:
                console.print(response)
        
        except Exception as e:
            logger.error(f"Chat error: {e}", exc_info=True)
            console.print(f"[red]✗[/red] Error: {e}", err=True)
            sys.exit(1)
        finally:
            manager.close()
    
    asyncio.run(_chat())


# Config commands
@cli.group()
def config() -> None:
    """Manage configuration."""
    pass


@config.command("show")
def config_show() -> None:
    """Show configuration."""
    cfg = get_config()
    
    console.print("\n[bold]General[/bold]")
    console.print(f"  default_agent: {cfg.general.default_agent}")
    console.print(f"  log_level: {cfg.general.log_level}")
    console.print(f"  data_dir: {cfg.get_data_dir()}")
    
    console.print("\n[bold]AI Service[/bold]")
    console.print(f"  default_provider: {cfg.ai_service.default_provider}")
    console.print(f"  default_model: {cfg.ai_service.default_model}")
    console.print(f"  timeout: {cfg.ai_service.timeout}s")
    console.print(f"  max_retries: {cfg.ai_service.max_retries}")
    
    console.print("\n[bold]Cache[/bold]")
    console.print(f"  enabled: {cfg.cache.enabled}")
    console.print(f"  ttl: {cfg.cache.ttl}s")
    console.print(f"  max_size: {cfg.cache.max_size}MB")
    
    console.print(f"\n[dim]Config file: {cfg.config_path}[/dim]")


@config.command("init")
def config_init() -> None:
    """Initialize configuration."""
    cfg = get_config()
    
    console.print("[yellow]Initializing configuration...[/yellow]")
    
    # Prompt for API key
    api_key = click.prompt("OpenAI API key (or press Enter to skip)", default="", hide_input=True, show_default=False)
    
    if api_key:
        cfg.ai_service.openai_api_key = api_key
    
    # Save configuration
    cfg.save()
    
    console.print(f"[green]✓[/green] Configuration saved to: {cfg.config_path}")
    console.print("\n[dim]You can also set the API key via environment variable:[/dim]")
    console.print("[dim]  export MYCLI_OPENAI_API_KEY=your-api-key[/dim]")


# REPL command
@cli.command()
@click.option("--agent", "-a", help="Agent to use")
def repl(agent: Optional[str]) -> None:
    """Start interactive REPL session."""
    start_repl(agent=agent)


def main() -> None:
    """Main entry point."""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        console.print(f"[red]✗[/red] Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
