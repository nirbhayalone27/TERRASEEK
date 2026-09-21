"""Model adapters: GeoRSCLIP, UNetResNet34, and deterministic Demo implementations."""

import hashlib
import logging
from typing import Any, Dict, List, Optional
import numpy as np

from terraseek.schemas.common import ModelTier
from terraseek.models.interfaces import (
    ChangeDetectionModel,
    EmbeddingModel,
    ModelMetadata,
    SpectralAnalyzer,
)
from terraseek.raster.processor import RasterProcessor

logger = logging.getLogger("terraseek.models")


class DemoEmbeddingModel(EmbeddingModel):
    """Deterministic local embedding adapter for development and offline operation.
    
    Generates deterministic, normalized 512-dimensional vectors from text or image hashes.
    Explicitly labeled as ModelTier.DEMO.
    """

    def __init__(self, dimension: int = 512):
        self.dimension = dimension
        self.metadata = ModelMetadata(
            name="DemoEmbeddingAdapter",
            version="1.0.0-deterministic",
            tier=ModelTier.DEMO,
            weights_id="none-deterministic-hash-projection",
            description="Offline deterministic pseudo-embedding generator. DOES NOT use real neural network weights.",
        )

    def get_metadata(self) -> ModelMetadata:
        return self.metadata

    def _generate_vector(self, seed_string: str) -> List[float]:
        # Deterministically map seed string into a normalized unit vector
        h = hashlib.sha256(seed_string.encode("utf-8")).digest()
        # Seed a pseudo-random generator
        seed_int = int.from_bytes(h[:8], "big")
        rng = np.random.RandomState(seed_int % (2**31 - 1))
        vec = rng.randn(self.dimension).astype(np.float32)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    def embed_text(self, text: str) -> List[float]:
        # Normalize text tokenization
        clean_text = text.lower().strip()
        return self._generate_vector(f"text:{clean_text}")

    def embed_image(self, image_bytes_or_path: Any) -> List[float]:
        if isinstance(image_bytes_or_path, (bytes, bytearray)):
            digest = hashlib.sha256(image_bytes_or_path).hexdigest()
        else:
            digest = hashlib.sha256(str(image_bytes_or_path).encode("utf-8")).hexdigest()
        return self._generate_vector(f"image:{digest}")


class GeoRSCLIPEmbeddingModel(EmbeddingModel):
    """Production GeoRSCLIP model adapter.
    
    Uses remote/local GeoRSCLIP model weights when explicitly loaded.
    Fails explicitly if weights are unavailable.
    """

    def __init__(self, model_weights_path: Optional[str] = None):
        self.weights_path = model_weights_path
        self.loaded = False
        self.metadata = ModelMetadata(
            name="GeoRSCLIP",
            version="v1.0",
            tier=ModelTier.PRODUCTION if model_weights_path else ModelTier.UNAVAILABLE,
            weights_id=model_weights_path or "unloaded",
            description="Vision-Language Foundation Model for Remote Sensing Imagery.",
        )

    def get_metadata(self) -> ModelMetadata:
        return self.metadata

    def embed_text(self, text: str) -> List[float]:
        if not self.loaded:
            raise RuntimeError(
                "GeoRSCLIP model weights are not loaded. Set EMBEDDING_PROVIDER=demo for offline mode or configure real weights."
            )
        # Production model inference placeholder
        return []

    def embed_image(self, image_bytes_or_path: Any) -> List[float]:
        if not self.loaded:
            raise RuntimeError("GeoRSCLIP model weights are not loaded.")
        return []


class DemoChangeDetectionModel(ChangeDetectionModel):
    """Deterministic change detector using numerical differences and spectral thresholds.
    
    Explicitly labeled as ModelTier.DEMO.
    """

    def __init__(self):
        self.metadata = ModelMetadata(
            name="DemoChangeDetectionAdapter",
            version="1.0.0-spectral-diff",
            tier=ModelTier.DEMO,
            weights_id="none-algebraic-diff",
            description="Algorithmic image difference & thresholding adapter for offline change detection.",
        )

    def get_metadata(self) -> ModelMetadata:
        return self.metadata

    def predict_change(
        self,
        before_raster: np.ndarray,
        after_raster: np.ndarray,
        change_type: str = "BUILDING",
    ) -> Dict[str, Any]:
        """Perform normalized difference and compute change metrics."""
        # Ensure compatible shape
        min_h = min(before_raster.shape[-2], after_raster.shape[-2])
        min_w = min(before_raster.shape[-1], after_raster.shape[-1])
        b_slice = before_raster[..., :min_h, :min_w].astype(float)
        a_slice = after_raster[..., :min_h, :min_w].astype(float)

        diff = np.abs(a_slice - b_slice)
        mean_diff = float(np.mean(diff))
        max_diff = float(np.max(diff))
        
        # Binary mask threshold
        threshold = 30.0 if np.max(before_raster) > 1.0 else 0.15
        changed_pixels = int(np.count_nonzero(diff > threshold))
        total_pixels = int(diff.size)
        change_ratio = float(changed_pixels / total_pixels) if total_pixels > 0 else 0.0

        return {
            "model_name": self.metadata.name,
            "model_tier": self.metadata.tier.value,
            "change_type": change_type,
            "mean_difference": round(mean_diff, 4),
            "max_difference": round(max_diff, 4),
            "changed_pixels": changed_pixels,
            "change_ratio": round(change_ratio, 4),
            "change_detected": change_ratio > 0.05,
        }


class UNetResNet34ChangeModel(ChangeDetectionModel):
    """Production Siamese U-Net with ResNet-34 backbone for building/road change detection."""

    def __init__(self, weights_path: Optional[str] = None):
        self.weights_path = weights_path
        self.loaded = False
        self.metadata = ModelMetadata(
            name="UNet-ResNet34-ChangeNet",
            version="2.1.0",
            tier=ModelTier.PRODUCTION if weights_path else ModelTier.UNAVAILABLE,
            weights_id=weights_path or "unloaded",
            description="Siamese U-Net with ResNet-34 backbone for high-resolution optical change detection.",
        )

    def get_metadata(self) -> ModelMetadata:
        return self.metadata

    def predict_change(
        self,
        before_raster: np.ndarray,
        after_raster: np.ndarray,
        change_type: str = "BUILDING",
    ) -> Dict[str, Any]:
        if not self.loaded:
            raise RuntimeError(
                "UNet-ResNet34 model weights are not loaded. Set CHANGE_DETECTION_PROVIDER=demo for offline mode."
            )
        return {}


class DefaultSpectralAnalyzer(SpectralAnalyzer):
    """Analyzes multispectral bands for vegetation (NDVI) and water (MNDWI)."""

    def analyze(self, bands: Dict[str, np.ndarray]) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        if "red" in bands and "nir" in bands:
            ndvi = RasterProcessor.calculate_ndvi(bands["red"], bands["nir"])
            results["mean_ndvi"] = round(float(np.nanmean(ndvi)), 4)
            results["max_ndvi"] = round(float(np.nanmax(ndvi)), 4)
            results["vegetation_dense"] = bool(results["mean_ndvi"] > 0.5)

        if "green" in bands and "swir" in bands:
            mndwi = RasterProcessor.calculate_mndwi(bands["green"], bands["swir"])
            results["mean_mndwi"] = round(float(np.nanmean(mndwi)), 4)
            results["water_detected"] = bool(results["mean_mndwi"] > 0.0)

        return results


def get_embedding_provider() -> EmbeddingModel:
    from terraseek.config import settings
    if settings.models.embedding_provider == "georsclip":
        return GeoRSCLIPEmbeddingModel()
    return DemoEmbeddingModel(dimension=settings.vector_db.embedding_dimension)


def get_change_provider() -> ChangeDetectionModel:
    from terraseek.config import settings
    if settings.models.change_provider == "unet_resnet34":
        return UNetResNet34ChangeModel()
    return DemoChangeDetectionModel()
