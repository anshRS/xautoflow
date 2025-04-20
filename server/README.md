# XAutoFlow - Multi-Agent Fintech Brokerage System

A robust, modular FastAPI application for a multi-agent fintech system that emulates advanced agentic applications focusing on financial research, strategy development, backtesting, and analysis.

## Architecture

This system integrates several advanced technologies:

1. **Web Framework:** FastAPI for asynchronous API endpoints and dependency injection
2. **Agent Workflow Orchestration:** LangGraph for editable, stateful agentic workflows
3. **Multi-Agent Communication:** Autogen for communication between specialized agents
4. **Context Retrieval (RAG):** LlamaIndex for efficient retrieval from domain-specific knowledge base
5. **LLM Configuration:** Configurable settings for various LLM providers
6. **Data Layer:** AsyncSQL with SQLAlchemy for data persistence
7. **Fintech Libraries:** Integration with financial analysis and backtesting tools

## Key Components

- **Specialized Agents:**
  - Market Research Agent: Analyzes financial markets and gathers information
  - Strategy Development Agent: Creates and optimizes trading strategies
  - Backtesting Agent: Tests strategies on historical data
  - Knowledge Base Agent: Retrieves relevant information from the KB

- **LangGraph Workflow:**
  - Planning Node: Breaks down high-level tasks
  - Market Research Node: Gathers and analyzes market data
  - Strategy Development Node: Creates trading strategies
  - Backtesting Node: Evaluates strategies on historical data
  - Finalization Node: Compiles results into coherent reports

## Getting Started

### Prerequisites

- Python 3.10+ 
- PostgreSQL database
- OpenAI API key or other LLM provider API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/xautoflow.git
   cd xautoflow/server
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   
5. Edit the `.env` file and update the configuration values, including:
   - DATABASE_URL
   - OPENAI_API_KEY or other LLM provider credentials
   - Other settings as needed

6. Create the required directories:
   ```bash
   mkdir -p storage knowledge_base output
   ```

7. Initialize the database:
   ```bash
   # Using SQLAlchemy metadata in development
   # In production, use proper database migration tools like Alembic
   ```

### Running the Application

Start the server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

## API Endpoints

### Agent Endpoints

- `POST /api/v1/agents/tasks`: Create a new agent task
- `GET /api/v1/agents/tasks/{task_id}`: Get task status and results
- `GET /api/v1/agents/tasks`: List recent tasks
- `POST /api/v1/agents/workflows/end-to-end`: Create an end-to-end workflow

### Knowledge Base Endpoints

- `POST /api/v1/kb/query`: Query the knowledge base
- `POST /api/v1/kb/documents/upload`: Upload a document to the KB
- `GET /api/v1/kb/documents`: List all documents in the KB

## Project Structure

```
server/
├── app/
│   ├── agents/             # Agent definitions (Autogen, LangGraph)
│   ├── core/               # Core configuration and utilities
│   ├── data/               # Database setup and data access
│   ├── models/             # API and database models
│   ├── routers/            # API route definitions
│   ├── services/           # Business logic
│   ├── tools/              # Tools used by agents
│   └── main.py             # Application entry point
├── storage/                # LlamaIndex storage location
├── knowledge_base/         # Documents for the knowledge base
├── output/                 # Generated outputs (strategies, reports)
├── .env.example            # Example environment variables
└── requirements.txt        # Python dependencies
```

## Configuration

The application is configured using environment variables defined in `.env` file. See `.env.example` for documentation on available settings.

## Development

### Adding New Agents

To add a new agent:

1. Define the agent in `app/agents/autogen_agents.py`
2. Add necessary tool implementations in `app/tools/`
3. Update the workflow in `app/agents/langgraph_workflow.py` if needed
4. Add API endpoints in `app/routers/` and service methods in `app/services/`

### Adding New Tools

Tools are functions that agents can use:

1. Create a new tool file in `app/tools/` or add to an existing one
2. Implement the tool function with proper error handling
3. Register the tool with the appropriate agent in `app/agents/autogen_agents.py`

## License

[MIT License](LICENSE) 