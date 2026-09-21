"""Raster processing with rasterio, numpy, and spectral computations."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.enums import Resampling


class RasterProcessor:
    @staticmethod
    def get_metadata(raster_path: str) -> Dict[str, Any]:
        """Read raster bounds, CRS, shape, transform, and band count."""
        with rasterio.open(raster_path) as src:
            return {
                "crs": str(src.crs),
                "bounds": [src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top],
                "width": src.width,
                "height": src.height,
                "count": src.count,
                "dtypes": [str(d) for d in src.dtypes],
                "nodata": src.nodata,
                "transform": [float(x) for x in src.transform],
            }

    @staticmethod
    def read_window(
        raster_path: str,
        col_off: int,
        row_off: int,
        width: int,
        height: int,
        bands: Optional[List[int]] = None,
    ) -> np.ndarray:
        """Read a sub-window of raster without loading the full file into memory."""
        with rasterio.open(raster_path) as src:
            win = Window(col_off=col_off, row_off=row_off, width=width, height=height)
            if bands:
                return src.read(bands, window=win)
            return src.read(window=win)

    @staticmethod
    def calculate_ndvi(red: np.ndarray, nir: np.ndarray) -> np.ndarray:
        """Normalized Difference Vegetation Index: (NIR - Red) / (NIR + Red)."""
        np.seterr(divide="ignore", invalid="ignore")
        denominator = nir.astype(float) + red.astype(float)
        numerator = nir.astype(float) - red.astype(float)
        ndvi = np.where(denominator == 0, 0.0, numerator / denominator)
        return np.nan_to_num(ndvi, nan=0.0)

    @staticmethod
    def calculate_mndwi(green: np.ndarray, swir: np.ndarray) -> np.ndarray:
        """Modified Normalized Difference Water Index: (Green - SWIR) / (Green + SWIR)."""
        np.seterr(divide="ignore", invalid="ignore")
        denominator = green.astype(float) + swir.astype(float)
        numerator = green.astype(float) - swir.astype(float)
        mndwi = np.where(denominator == 0, 0.0, numerator / denominator)
        return np.nan_to_num(mndwi, nan=0.0)

    @staticmethod
    def normalize_band(band: np.ndarray) -> np.ndarray:
        """Min-max normalize band to 0..255 for RGB visualization."""
        b_min = np.percentile(band, 2)
        b_max = np.percentile(band, 98)
        if b_max > b_min:
            scaled = ((band - b_min) / (b_max - b_min)) * 255.0
            return np.clip(scaled, 0, 255).astype(np.uint8)
        return np.zeros_like(band, dtype=np.uint8)

    @staticmethod
    def create_rgb_thumbnail(
        raster_path: str,
        output_png_path: str,
        red_band: int = 1,
        green_band: int = 2,
        blue_band: int = 3,
        max_size: int = 512,
    ) -> str:
        """Generate a high quality visual RGB PNG thumbnail from multi-band raster."""
        from PIL import Image

        with rasterio.open(raster_path) as src:
            # Resample to max_size thumbnail
            scale = max_size / max(src.width, src.height)
            out_w = max(1, int(src.width * scale))
            out_h = max(1, int(src.height * scale))

            r = src.read(red_band, out_shape=(out_h, out_w), resampling=Resampling.bilinear)
            g = src.read(green_band, out_shape=(out_h, out_w), resampling=Resampling.bilinear)
            b = src.read(blue_band, out_shape=(out_h, out_w), resampling=Resampling.bilinear)

            r_norm = RasterProcessor.normalize_band(r)
            g_norm = RasterProcessor.normalize_band(g)
            b_norm = RasterProcessor.normalize_band(b)

            rgb = np.stack([r_norm, g_norm, b_norm], axis=-1)
            img = Image.fromarray(rgb)
            Path(output_png_path).parent.mkdir(parents=True, exist_ok=True)
            img.save(output_png_path, "PNG")
            return output_png_path
