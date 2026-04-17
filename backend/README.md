# OpenCode AI Agent

OpenCode is an AI agent framework built with LangGraph, LangChain, and FastAPI. It provides both a RESTful API and a Command-Line Interface (CLI) for interacting with various Large Language Models (LLMs) including Anthropic, OpenAI, Google Gemini, and local Ollama instances.

## Features

- **Multi-Provider Support**: Seamlessly switch between OpenAI, Anthropic, Google Gemini, and Ollama.
- **Agentic Logic**: Built on LangGraph for robust agent state management and tool calling.
- **Dual Interface**:
  - **CLI**: Interactive terminal-based chat and headless task execution.
  - **REST API**: FastAPI backend with support for synchronous and streaming responses.
- **Session Management**: Persistent chat history stored in a local SQLite database.
- **Extensible Tools**: Infrastructure for adding custom tools in `app/tools/`.

## Project Structure

```text
.
├── app/
│   ├── agent/       # LangGraph agent definition and core logic
│   ├── api/         # FastAPI schemas and endpoints
│   ├── core/        # Model factory and base configurations
│   ├── memory/      # SQLite-based history management
│   └── tools/       # Built-in and custom tool definitions
├── cli.py           # Command-line interface
├── main.py          # FastAPI server entry point
└── requirements.txt # Project dependencies
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd opencode
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables** (Optional, based on provider):
   - OpenAI: `export OPENAI_API_KEY='your-key'`
   - Anthropic: `export ANTHROPIC_API_KEY='your-key'`
   - Google Gemini: `export GOOGLE_API_KEY='your-key'`
   - Ollama: Ensure Ollama is running locally.

## Usage

### Command Line Interface (CLI)

OpenCode provides a powerful CLI using `typer`.

**Interactive Mode:**
```bash
python cli.py interact --model llama3.1 --cloud openai
```

**Single Task Mode:**
```bash
python cli.py run-task "Write a python script to scrape news" --model gpt-4o --cloud openai
```

### API Server

**Start the server:**
```bash
python main.py
```
The server will run at `http://127.0.0.1:8000`.

**Endpoints:**
- `GET /health`: Check API status.
- `POST /chat/run`: Synchronous chat response.
- `POST /chat/stream`: Server-Sent Events (SSE) streaming response.
- `GET /history/sessions`: List all chat sessions.
- `GET /history/sessions/{session_id}`: Get messages for a specific session.

## Development

- **Adding Tools**: Add new functions in `app/tools/builtins.py` and register them in the LangGraph graph in `app/agent/graph.py`.
- **Database**: The application initializes a local SQLite database automatically on startup for history persistence.

## License

[Specify License Here, e.g., MIT]
