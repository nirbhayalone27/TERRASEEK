"""Quality assessment for ingested rasters and observations."""

from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np
import rasterio
from pydantic import BaseModel, Field


class QualityReport(BaseModel):
    is_usable: bool
    quality_score: float  # 0.0 to 1.0
    cloud_cover_pct: float
    nodata_pct: float
    dimensions_valid: bool
    bands_valid: bool
    temporal_valid: bool
    issues: List[str] = Field(default_factory=list)
    details: Dict[str, Any] = Field(default_factory=dict)


class QualityChecker:
    @staticmethod
    def inspect_raster(
        raster_path: str,
        expected_bands: int = 3,
        acquisition_date: Optional[date] = None,
        max_allowed_cloud_pct: float = 30.0,
        max_allowed_nodata_pct: float = 20.0,
    ) -> QualityReport:
        issues: List[str] = []
        path = Path(raster_path)
        if not path.exists():
            return QualityReport(
                is_usable=False,
                quality_score=0.0,
                cloud_cover_pct=100.0,
                nodata_pct=100.0,
                dimensions_valid=False,
                bands_valid=False,
                temporal_valid=False,
                issues=["File does not exist"],
            )

        with rasterio.open(raster_path) as src:
            width = src.width
            height = src.height
            count = src.count
            nodata_val = src.nodata

            dim_valid = width >= 32 and height >= 32
            if not dim_valid:
                issues.append(f"Image dimensions too small ({width}x{height})")

            bands_valid = count >= expected_bands
            if not bands_valid:
                issues.append(f"Missing bands: found {count}, expected at least {expected_bands}")

            # Sample first band for nodata and cloud approximation
            sample = src.read(1, out_shape=(min(height, 256), min(width, 256)))
            if nodata_val is not None:
                nodata_count = np.count_nonzero(sample == nodata_val)
            else:
                nodata_count = np.count_nonzero(sample == 0)
            
            total_pixels = sample.size
            nodata_pct = float((nodata_count / total_pixels) * 100.0) if total_pixels > 0 else 100.0

            # Estimate high reflectance (bright cloud-like pixels)
            # In normalized 8-bit, values > 245
            bright_count = np.count_nonzero(sample > (240 if sample.dtype == np.uint8 else 9000))
            cloud_pct = float((bright_count / total_pixels) * 100.0) if total_pixels > 0 else 0.0

            if nodata_pct > max_allowed_nodata_pct:
                issues.append(f"High nodata ratio: {nodata_pct:.1f}%")

            if cloud_pct > max_allowed_cloud_pct:
                issues.append(f"High cloud cover detected: {cloud_pct:.1f}%")

            temporal_valid = True
            if acquisition_date is not None:
                # Check realistic satellite date range
                if acquisition_date.year < 1970 or acquisition_date > date.today():
                    temporal_valid = False
                    issues.append(f"Invalid acquisition date: {acquisition_date}")

            score = 1.0 - (nodata_pct / 100.0) * 0.5 - (cloud_pct / 100.0) * 0.5
            score = max(0.0, min(1.0, score))
            usable = dim_valid and bands_valid and temporal_valid and (nodata_pct <= max_allowed_nodata_pct)

            return QualityReport(
                is_usable=usable,
                quality_score=round(score, 2),
                cloud_cover_pct=round(cloud_pct, 1),
                nodata_pct=round(nodata_pct, 1),
                dimensions_valid=dim_valid,
                bands_valid=bands_valid,
                temporal_valid=temporal_valid,
                issues=issues,
                details={"width": width, "height": height, "bands": count},
            )
