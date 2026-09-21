"""Configuration management for TerraSeek."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    title: str = "TerraSeek API"
    version: str = "0.1.0"
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"])


class DatabaseConfig(BaseModel):
    url: str = "postgresql://terraseek:terraseek@localhost:5432/terraseek"
    sqlite_fallback_url: str = "sqlite:///./data/terraseek_dev.db"
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20


class VectorDBConfig(BaseModel):
    url: str = "http://localhost:6333"
    api_key: Optional[str] = None
    collection_name: str = "satellite_observations"
    embedding_dimension: int = 512
    prefer_in_memory: bool = False


class StorageConfig(BaseModel):
    root: str = "./data/storage"
    provider: str = "filesystem"


class ModelsConfig(BaseModel):
    embedding_provider: str = "demo"  # "demo" | "georsclip"
    change_provider: str = "demo"     # "demo" | "unet_resnet34"
    cache_dir: str = "./data/models"


class WorkersConfig(BaseModel):
    poll_interval_seconds: int = 2
    max_concurrent_jobs: int = 4


class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: str = "json"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    env: str = Field(default="development", alias="TERRASEEK_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    api: APIConfig = Field(default_factory=APIConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    vector_db: VectorDBConfig = Field(default_factory=VectorDBConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    models: ModelsConfig = Field(default_factory=ModelsConfig)
    workers: WorkersConfig = Field(default_factory=WorkersConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


def load_settings(config_path: Optional[str] = None) -> Settings:
    """Load settings from yaml file and environment variables."""
    env = os.getenv("TERRASEEK_ENV", "development")
    
    # Locate config file
    if not config_path:
        base_dir = Path(__file__).resolve().parent.parent.parent
        possible_paths = [
            base_dir / "configs" / f"{env}.yaml",
            Path(f"configs/{env}.yaml"),
        ]
        for p in possible_paths:
            if p.exists():
                config_path = str(p)
                break

    data: Dict[str, Any] = {}
    if config_path and Path(config_path).exists():
        with open(config_path, "r") as f:
            yaml_data = yaml.safe_load(f)
            if isinstance(yaml_data, dict):
                data = yaml_data

    # Allow environment variable overrides
    if os.getenv("DATABASE_URL"):
        data.setdefault("database", {})["url"] = os.getenv("DATABASE_URL")
    if os.getenv("QDRANT_URL"):
        data.setdefault("vector_db", {})["url"] = os.getenv("QDRANT_URL")
    if os.getenv("STORAGE_ROOT"):
        data.setdefault("storage", {})["root"] = os.getenv("STORAGE_ROOT")
    if os.getenv("EMBEDDING_PROVIDER"):
        data.setdefault("models", {})["embedding_provider"] = os.getenv("EMBEDDING_PROVIDER")
    if os.getenv("CHANGE_DETECTION_PROVIDER"):
        data.setdefault("models", {})["change_provider"] = os.getenv("CHANGE_DETECTION_PROVIDER")

    return Settings(**data)


# Global settings singleton
settings = load_settings()
