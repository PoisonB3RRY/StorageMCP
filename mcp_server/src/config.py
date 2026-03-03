import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="MCP_",
    )
    
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    weather_api_base_url: str = "https://api.weather.gov"
    user_agent: str = "WeatherMCP/0.1.0"
    
    log_level: str = "INFO"
    log_file: str = "mcp_server.log"


settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings
