# StorageMCP

A Python-based Model Context Protocol (MCP) server for file storage operations.

## Features

- File upload and download
- File listing and metadata retrieval
- Directory management
- File search capabilities
- MCP protocol compliance

## MCP Servers

This project includes multiple MCP servers:

### 1. Weather MCP Server

A FastAPI-based MCP server for weather forecasting and alerts.

**Features:**
- Weather forecast for specific locations (latitude/longitude)
- Weather alerts for US states
- RESTful API with automatic documentation
- Async support for efficient request handling
- Environment-based configuration
- Comprehensive logging and monitoring

**Quick Start:**
```bash
# Navigate to the MCP server directory
cd mcp_server

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m mcp_server.src.main

# Access API documentation
open http://localhost:8000/docs
```

**Available Tools:**
- `get_forecast`: Get weather forecast for a location
- `get_alerts`: Get weather alerts for a US state

For detailed information, see [mcp_server/README.md](mcp_server/README.md).