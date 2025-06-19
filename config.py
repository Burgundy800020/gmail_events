from pydantic_settings import BaseSettings 
from pydantic import Field, PostgresDsn
from typing import Optional, Literal


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str= Field(..., description="PostgreSQL database URL")
    
    # Gmail settings
    token: str = Field(..., description="Path to Gmail OAuth token file")
    
    # OpenAI settings
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key")
    GPT_MODEL: str = Field("gpt-4.1", description="GPT model to use for event extraction")

    # Application settings
    mode: Literal['normal', 'debug', 'debug_all'] = Field('normal', description="Enable debug mode")
    POLLING_INTERVAL: int = Field(60, description="Interval in seconds between email checks")
    output: Optional[str] = Field(None, description="Path to output file for events")
    ALL_TIME: bool = Field(False, description="Process all emails instead of just new ones")
    
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"
        cli_parse_args = True


# Create global settings instance
settings = Settings()

# Configure logging based on settings
import structlog
import logging

logging.basicConfig(
    level=logging.INFO if settings.mode == 'debug' else logging.ERROR
)

structlog.configure(
    logger_factory=structlog.stdlib.LoggerFactory(),
    processors=[
        structlog.processors.KeyValueRenderer(key_order=['event'])
    ]
) 
