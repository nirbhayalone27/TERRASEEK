"""Model interfaces and contracts."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import numpy as np
from terraseek.schemas.common import ModelTier


class ModelMetadata:
    def __init__(
        self,
        name: str,
        version: str,
        tier: ModelTier,
        weights_id: Optional[str] = None,
        description: str = "",
    ):
        self.name = name
        self.version = version
        self.tier = tier
        self.weights_id = weights_id
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.name,
            "model_version": self.version,
            "model_tier": self.tier.value if hasattr(self.tier, "value") else str(self.tier),
            "weights_identifier": self.weights_id,
            "description": self.description,
        }


class EmbeddingModel(ABC):
    @abstractmethod
    def get_metadata(self) -> ModelMetadata:
        pass

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def embed_image(self, image_bytes_or_path: Any) -> List[float]:
        pass


class ChangeDetectionModel(ABC):
    @abstractmethod
    def get_metadata(self) -> ModelMetadata:
        pass

    @abstractmethod
    def predict_change(
        self,
        before_raster: np.ndarray,
        after_raster: np.ndarray,
        change_type: str = "BUILDING",
    ) -> Dict[str, Any]:
        pass


class SpectralAnalyzer(ABC):
    @abstractmethod
    def analyze(self, bands: Dict[str, np.ndarray]) -> Dict[str, Any]:
        pass
