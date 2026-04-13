import subprocess
from pathlib import Path
from langchain_core.tools import tool

@tool
def file_read(path: str) -> str:
    """Read the contents of a file from disk given an absolute or relative path."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def file_write(path: str, content: str) -> str:
    """Write content to a file on disk. Creates directories if they don't exist."""
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {e}"

@tool
def python_run(code: str) -> str:
    """Execute Python code in a subprocess sandbox and return stdout/stderr."""
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"
        return output or "Code executed successfully with no output."
    except subprocess.TimeoutExpired:
        return "Error: Python execution timed out."
    except Exception as e:
        return f"Error executing Python code: {e}"

def get_tools():
    return [file_read, file_write, python_run]
