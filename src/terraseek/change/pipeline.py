"""Change detection and spectral analysis pipeline."""

from datetime import date
from typing import Any, Dict, List, Optional
import numpy as np

from terraseek.schemas.common import ChangeType, EvidenceStatus, ModelTier, GeoJSONFeature, GeoJSONFeatureCollection
from terraseek.schemas.change import ChangeEventRead, CompareResult, ChangeAnalyzeResult
from terraseek.models.adapters import get_change_provider, DefaultSpectralAnalyzer
from terraseek.raster.processor import RasterProcessor


class ChangePipeline:
    def __init__(self):
        self.detector = get_change_provider()
        self.spectral_analyzer = DefaultSpectralAnalyzer()

    def analyze_pair(
        self,
        before_raster: np.ndarray,
        after_raster: np.ndarray,
        change_types: List[ChangeType],
        site_id: str,
        earlier_date: date,
        later_date: date,
        base_geometry: Optional[Dict[str, Any]] = None,
    ) -> ChangeAnalyzeResult:
        """Run change detection across specified change types."""
        changes: List[ChangeEventRead] = []
        features: List[GeoJSONFeature] = []

        for c_type in change_types:
            result = self.detector.predict_change(
                before_raster=before_raster,
                after_raster=after_raster,
                change_type=c_type.value,
            )

            is_change = result.get("change_detected", False)
            status = EvidenceStatus.SUPPORTED if is_change else EvidenceStatus.NO_MATCH

            # Construct change polygon GeoJSON if change detected
            geom = base_geometry or {
                "type": "Polygon",
                "coordinates": [[[0.0, 0.0], [0.01, 0.0], [0.01, 0.01], [0.0, 0.01], [0.0, 0.0]]],
            }

            event_id = f"chg-{site_id}-{c_type.value.lower()}"
            ev = ChangeEventRead(
                id=event_id,
                site_id=site_id,
                change_type=c_type,
                earlier_date=earlier_date,
                later_date=later_date,
                area_sq_meters=round(result.get("changed_pixels", 1200) * 100.0, 1),
                status=status,
                model_name=result.get("model_name", "demo-change-detector"),
                model_tier=ModelTier.DEMO if "demo" in result.get("model_name", "").lower() else ModelTier.PRODUCTION,
                geometry=geom,
                provenance={
                    "mean_difference": result.get("mean_difference", 0.0),
                    "change_ratio": result.get("change_ratio", 0.0),
                },
                created_at=np.datetime64("now").astype("datetime64[ms]").astype(object),
            )
            changes.append(ev)

            if is_change:
                features.append(
                    GeoJSONFeature(
                        id=event_id,
                        geometry=geom,
                        properties={
                            "change_type": c_type.value,
                            "area_sq_meters": ev.area_sq_meters,
                            "earlier_date": earlier_date.isoformat(),
                            "later_date": later_date.isoformat(),
                            "status": status.value,
                        },
                    )
                )

        overall_status = (
            EvidenceStatus.SUPPORTED
            if any(c.status == EvidenceStatus.SUPPORTED for c in changes)
            else EvidenceStatus.NO_MATCH
        )

        return ChangeAnalyzeResult(
            site_id=site_id,
            status=overall_status,
            earlier_date=earlier_date,
            later_date=later_date,
            features=GeoJSONFeatureCollection(features=features),
            changes=changes,
            model_tier=ModelTier.DEMO,
            summary=f"Evaluated {len(change_types)} change types. Detected {len(features)} active change features.",
        )
