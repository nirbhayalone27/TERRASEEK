"""Storage interface and filesystem implementation."""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, Dict, Optional


class StorageProvider(ABC):
    @abstractmethod
    def save(self, path: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        """Save binary data to storage. Returns the stored URI or key."""
        pass

    @abstractmethod
    def open(self, path: str) -> bytes:
        """Read binary data from storage."""
        pass

    @abstractmethod
    def delete(self, path: str) -> bool:
        """Delete file from storage."""
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check if file exists."""
        pass

    @abstractmethod
    def get_metadata(self, path: str) -> Dict[str, any]:
        """Get file size, last modified, etc."""
        pass


class FilesystemStorage(StorageProvider):
    def __init__(self, root_dir: str = "./data/storage"):
        self.root = Path(root_dir).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, path: str) -> Path:
        # Prevent directory traversal attacks
        clean_path = path.lstrip("/")
        target = (self.root / clean_path).resolve()
        if not str(target).startswith(str(self.root)):
            raise ValueError(f"Security: Path traversal attempt detected for path '{path}'")
        return target

    def save(self, path: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        target = self._resolve(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return str(target.relative_to(self.root))

    def open(self, path: str) -> bytes:
        target = self._resolve(path)
        if not target.exists():
            raise FileNotFoundError(f"Storage item not found: {path}")
        return target.read_bytes()

    def delete(self, path: str) -> bool:
        target = self._resolve(path)
        if target.exists():
            target.unlink()
            return True
        return False

    def exists(self, path: str) -> bool:
        return self._resolve(path).exists()

    def get_metadata(self, path: str) -> Dict[str, any]:
        target = self._resolve(path)
        if not target.exists():
            raise FileNotFoundError(f"Storage item not found: {path}")
        stat = target.stat()
        return {
            "size_bytes": stat.st_size,
            "modified_at": stat.st_mtime,
            "is_file": target.is_file(),
        }


def get_storage() -> StorageProvider:
    from terraseek.config import settings
    return FilesystemStorage(root_dir=settings.storage.root)
