"""Generate synthetic deterministic GeoTIFF rasters and PNG thumbnails for demo sites."""

from pathlib import Path
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from PIL import Image, ImageDraw


def create_demo_assets():
    base_dir = Path("./data/demo/rasters")
    base_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir = Path("./data/demo/thumbnails")
    thumb_dir.mkdir(parents=True, exist_ok=True)

    sites = [
        ("site-01", 16.3738, 48.2082, "building"),
        ("site-02", 6.9603, 50.9375, "construction"),
        ("site-03", 11.0767, 49.4521, "road"),
        ("site-04", 8.2014, 48.0501, "vegetation"),
        ("site-05", 11.4041, 47.2692, "water"),
    ]

    width, height = 256, 256

    for site_id, lon, lat, change_type in sites:
        bounds = (lon - 0.01, lat - 0.01, lon + 0.01, lat + 0.01)
        transform = from_bounds(*bounds, width, height)

        # Generate "Before" raster (3 bands: Red, Green, Blue)
        # Background terrain
        np.random.seed(int(abs(lon * 1000) % 10000))
        before_r = np.clip(np.random.normal(80, 15, (height, width)), 40, 120).astype(np.uint8)
        before_g = np.clip(np.random.normal(120, 20, (height, width)), 60, 180).astype(np.uint8)
        before_b = np.clip(np.random.normal(70, 10, (height, width)), 30, 110).astype(np.uint8)

        # Before image Pillow drawing for distinct features
        img_b = Image.fromarray(np.stack([before_r, before_g, before_b], axis=-1))
        draw_b = ImageDraw.Draw(img_b)

        # If site 01, draw river across corner
        if site_id == "site-01":
            draw_b.line([(0, 40), (256, 120)], fill=(40, 90, 180), width=18)

        # If site 04 (forest), dense green
        if site_id == "site-04":
            draw_b.rectangle([(20, 20), (236, 236)], fill=(30, 140, 40))

        # If site 05 (water), large reservoir
        if site_id == "site-05":
            draw_b.ellipse([(40, 40), (216, 216)], fill=(20, 80, 190))

        arr_b = np.array(img_b)

        # Generate "After" raster with changes
        img_a = Image.fromarray(arr_b.copy())
        draw_a = ImageDraw.Draw(img_a)

        if site_id == "site-01":
            # New buildings (bright rectangular structures) near river
            draw_a.rectangle([(110, 140), (160, 180)], fill=(230, 230, 235), outline=(100, 100, 110), width=2)
            draw_a.rectangle([(170, 130), (210, 170)], fill=(220, 220, 230), outline=(100, 100, 110), width=2)
            draw_a.line([(110, 160), (210, 160)], fill=(150, 150, 160), width=3)
        elif site_id == "site-02":
            # Construction ground clearing (sandy brown)
            draw_a.rectangle([(90, 90), (180, 180)], fill=(180, 150, 110), outline=(140, 110, 70), width=2)
        elif site_id == "site-03":
            # New road cut through terrain
            draw_a.line([(20, 230), (236, 30)], fill=(60, 60, 65), width=12)
            draw_a.line([(20, 230), (236, 30)], fill=(240, 240, 240), width=1)
        elif site_id == "site-04":
            # Forest clearing / loss
            draw_a.rectangle([(60, 60), (160, 160)], fill=(190, 170, 130))
        elif site_id == "site-05":
            # Water level drop / shoreline exposure
            draw_a.ellipse([(40, 40), (216, 216)], fill=(140, 130, 100))
            draw_a.ellipse([(70, 70), (186, 186)], fill=(20, 80, 190))

        arr_a = np.array(img_a)

        # Write Before GeoTIFF
        before_tif = base_dir / f"{site_id}_before.tif"
        with rasterio.open(
            str(before_tif),
            "w",
            driver="GTiff",
            height=height,
            width=width,
            count=3,
            dtype=rasterio.uint8,
            crs="EPSG:4326",
            transform=transform,
        ) as dst:
            dst.write(arr_b[:, :, 0], 1)
            dst.write(arr_b[:, :, 1], 2)
            dst.write(arr_b[:, :, 2], 3)

        # Write After GeoTIFF
        after_tif = base_dir / f"{site_id}_after.tif"
        with rasterio.open(
            str(after_tif),
            "w",
            driver="GTiff",
            height=height,
            width=width,
            count=3,
            dtype=rasterio.uint8,
            crs="EPSG:4326",
            transform=transform,
        ) as dst:
            dst.write(arr_a[:, :, 0], 1)
            dst.write(arr_a[:, :, 1], 2)
            dst.write(arr_a[:, :, 2], 3)

        # Save PNG thumbnails for web UI
        img_b.save(thumb_dir / f"{site_id}_before.png")
        img_a.save(thumb_dir / f"{site_id}_after.png")

    print(f"Successfully generated demo GeoTIFFs and thumbnails in {base_dir} and {thumb_dir}")


if __name__ == "__main__":
    create_demo_assets()
