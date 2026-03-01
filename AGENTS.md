# AGENTS.md - Agentic Coding Guidelines for StorageMCP

## Project Overview

StorageMCP is a Python-based Model Context Protocol (MCP) server for file storage operations. The main implementation is in the `mcp_server/` directory, which provides a FastAPI-based weather MCP server with forecasting and alerts functionality.

## Project Structure

```
StorageMCP/
├── mcp_server/           # Main MCP server implementation
│   ├── src/
│   │   ├── main.py       # Entry point
│   │   ├── server.py     # FastAPI app & endpoints
│   │   ├── config.py     # Settings management
│   │   ├── endpoints/    # API endpoints (alerts, forecast, health, tools, prompts)
│   │   └── models/       # Pydantic request/response models
│   ├── tests/            # Test suite
│   └── pyproject.toml    # Poetry configuration
├── weather.py            # MCP tool implementations (root level)
├── pyproject.toml        # Root project config
└── README.md
```

---

## Build, Lint, and Test Commands

### Setup/Installation

```bash
# Using uv (recommended)
cd mcp_server
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

### Running the Server

```bash
cd mcp_server

# Start the server
python -m mcp_server.src.main

# With custom host/port
python mcp_server/src/main.py --host 127.0.0.1 --port 9000
```

### Running Tests

```bash
cd mcp_server

# Run all tests
pytest tests/

# Run a single test file
pytest tests/test_server.py

# Run a single test
pytest tests/test_server.py::TestServer::test_health_check

# Run with verbose output
pytest tests/ -v
```

### Code Formatting & Linting

```bash
cd mcp_server

# Format code with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/
ruff format src/ tests/

# All combined (in order)
ruff check src/ tests/ && ruff format src/ tests/ && black src/ tests/
```

### Docker

```bash
cd mcp_server

# Build image
docker build -t weather-mcp-server .

# Run container
docker run -p 8000:8000 weather-mcp-server

# Or use docker-compose
docker-compose up
```

---

## Code Style Guidelines

### General Principles

- Use **Python 3.10+** (project targets 3.12)
- Follow **PEP 8** style guidelines
- Use **type hints** throughout
- Keep functions small and focused
- Write docstrings for all public functions

### Imports

- Standard library imports first
- Third-party imports second
- Local imports third
- Use absolute imports when possible
- Group imports with blank lines between groups

```python
# Standard library
import os
import sys
from typing import Optional

# Third-party
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# Local
from .models import ResponseModel
from .endpoints import handler
```

### Naming Conventions

- **Variables/functions**: `snake_case` (e.g., `get_weather_forecast`, `log_level`)
- **Classes**: `PascalCase` (e.g., `Settings`, `MCPResponse`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `NWS_API_BASE`)
- **Private functions/variables**: Leading underscore (e.g., `_internal_func`)

### Type Hints

Always use type hints for function parameters and return values:

```python
def process_data(items: list[str], config: dict[str, Any]) -> dict[str, Any]:
    ...

async def fetch_weather(lat: float, lon: float) -> MCPResponse:
    ...
```

### Error Handling

- Use try/except blocks for operations that may fail
- Return structured error responses (see `MCPResponse` model)
- Log errors with appropriate severity levels
- Never expose internal error details to clients in production

```python
try:
    result = await some_operation()
    return MCPResponse(success=True, data=result)
except Exception as e:
    logger.error(f"Operation failed: {str(e)}")
    return MCPResponse(success=False, error=str(e))
```

### Pydantic Models

Use Pydantic for all request/response models:

```python
class ForecastRequest(BaseModel):
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")

class MCPResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
```

### Configuration

Use Pydantic `BaseSettings` for configuration:

```python
class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_prefix = "MCP_"
```

### Async/Await

- Use `async def` for endpoint handlers
- Use `asyncio.to_thread()` for blocking operations
- Use `httpx.AsyncClient` for async HTTP requests

```python
async def get_weather_forecast(request: ForecastRequest) -> MCPResponse:
    result = await asyncio.to_thread(blocking_func, arg1, arg2)
    return MCPResponse(success=True, data=result)
```

### Logging

Use Python's logging module:

```python
import logging

logger = logging.getLogger(__name__)

# Usage
logger.info(f"Getting forecast for lat={lat}, lon={lon}")
logger.error(f"Error getting forecast: {str(e)}")
```

### FastAPI Endpoints

- Use appropriate HTTP methods (GET, POST, etc.)
- Define response models
- Use async def for all endpoint handlers
- Document with docstrings

```python
@app.post("/forecast", response_model=MCPResponse)
async def forecast_endpoint(request: ForecastRequest):
    """
    Get weather forecast for a location.
    """
    return await get_weather_forecast(request)
```

### Testing

- Use `pytest` as the test framework
- Use `FastAPI TestClient` for endpoint testing
- Use `unittest.mock.patch` for mocking external dependencies
- Group tests in classes
- Name test methods with `test_` prefix

```python
class TestServer:
    """Test cases for the MCP server."""

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200

    @patch("server.get_forecast")
    def test_get_forecast_success(self, mock_get_forecast):
        mock_get_forecast.return_value = {"forecast": [...]}
        response = client.post("/forecast", json={...})
        assert response.status_code == 200
```

---

## Important File Locations

- **Main server**: `mcp_server/src/server.py`
- **Entry point**: `mcp_server/src/main.py`
- **Config**: `mcp_server/src/config.py`
- **Models**: `mcp_server/src/models/responses.py`
- **Tests**: `mcp_server/tests/test_server.py`
- **Weather tools**: `weather.py` (root level)
- **API endpoints**: `mcp_server/src/endpoints/`

---

## Environment Variables

Create a `.env` file in `mcp_server/` based on `.env.example`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_HOST` | `0.0.0.0` | Server host |
| `MCP_PORT` | `8000` | Server port |
| `MCP_DEBUG` | `false` | Enable debug mode |
| `MCP_WEATHER_API_BASE_URL` | `https://api.weather.gov` | Weather API base URL |
| `MCP_LOG_LEVEL` | `INFO` | Logging level |
| `MCP_LOG_FILE` | `mcp_server.log` | Log file path |

---

## API Documentation

When running the server, access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
