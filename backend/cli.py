import typer
from rich.console import Console
from rich.markdown import Markdown

app = typer.Typer(help="OpenCode AI Agent CLI")
console = Console()

@app.command()
def interact(
    model: str = typer.Option("llama3", "--model", "-m", help="Model backend to use"),
    cloud: str = typer.Option("", "--cloud", "-c", help="Cloud provider to use (if any)"),
    workspace: str = typer.Option(".", "--workspace", "-w", help="Workspace path context")
):
    """
    Start an interactive chat session with the OpenCode AI Agent.
    """
    console.print(f"[bold green]Starting OpenCode CLI...[/bold green]")
    console.print(f"[dim]Model: {model} | Cloud: {cloud or 'None'} | Workspace: {workspace}[/dim]\n")
    
    while True:
        user_input = typer.prompt("You")
        if user_input.lower() in ("exit", "quit", "q"):
            console.print("[dim]Exiting OpenCode CLI...[/dim]")
            break
        
        response_text = f"**Agent:** Mock response for: *{user_input}*"
        console.print(Markdown(response_text))

@app.command()
def run_task(task: str = typer.Argument(..., help="Single task for the agent to execute")):
    """
    Run a single headless task through the agent and return the result.
    """
    console.print(f"[bold blue]Executing task:[/bold blue] {task}")
    console.print("[green]Task complete.[/green]")

if __name__ == "__main__":
    app()
