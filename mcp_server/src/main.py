import os
import sys
from typing import Optional

import uvicorn
from fastapi import FastAPI

# Add the current directory to sys.path to enable absolute imports
sys.path.insert(0, os.path.dirname(__file__))
from config import get_settings
from server import app

# Add the parent directory to sys.path to import weather module
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    # Configure logging
    import logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(settings.log_file),
        ],
    )
    
    return app


def run_server(host: Optional[str] = None, port: Optional[int] = None):
    """Run the MCP server."""
    settings = get_settings()
    
    # Use provided values or fall back to settings
    server_host = host or settings.host
    server_port = port or settings.port
    
    print(f"Starting Weather MCP Server on {server_host}:{server_port}")
    print(f"Debug mode: {settings.debug}")
    
    uvicorn.run(
        "mcp_server.src.main:app",
        host=server_host,
        port=server_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    run_server()