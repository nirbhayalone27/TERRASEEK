"""FastAPI route dependencies."""

from typing import Generator
from sqlalchemy.orm import Session
from terraseek.db.session import get_db

__all__ = ["get_db"]
