import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from config import get_settings
from server import mcp, run_sse_server


def main():
    """Main entry point for the MCP server."""
    settings = get_settings()
    
    print(f"Starting Weather MCP Server on {settings.host}:{settings.port}")
    print(f"Debug mode: {settings.debug}")
    print(f"Transport: SSE")
    print(f"SSE endpoint: http://{settings.host}:{settings.port}/sse")
    
    run_sse_server()


if __name__ == "__main__":
    main()
