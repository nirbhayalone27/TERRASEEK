"""Deterministic database and vector index seeding script for TerraSeek demo."""

import os
import sys
from datetime import date, datetime
from pathlib import Path

# Add src to python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from terraseek.db.session import init_db, get_session_factory
from terraseek.db.models import (
    SiteModel,
    ObservationModel,
    SpatialFeatureModel,
    ChangeEventModel,
    EvidenceRecordModel,
    EvidenceItemModel,
)
from terraseek.models.adapters import get_embedding_provider
from terraseek.retrieval.qdrant_client import get_vector_manager


def seed_demo_data():
    print("Initializing database tables...")
    init_db()
    session_factory = get_session_factory()
    db = session_factory()
    vector_mgr = get_vector_manager()
    embedder = get_embedding_provider()

    print("Checking existing data...")
    existing = db.query(SiteModel).all()
    if existing:
        print(f"Found {len(existing)} existing sites in database. Syncing vector index...")
        for s in existing:
            vec = embedder.embed_text(f"{s.name} {s.description or ''} {' '.join(s.tags or [])}")
            vector_mgr.upsert_observation(
                point_id=s.id,
                vector=vec,
                payload={
                    "site_id": s.id,
                    "name": s.name,
                    "location": s.location_name,
                    "tags": s.tags,
                    "primary_change": (s.meta_info or {}).get("primary_change"),
                },
            )
        print("Vector index populated with existing sites.")
        db.close()
        return

    print("Seeding 5 deterministic demo sites...")

    # Site 01: Riverside Development (Danube Valley)
    site_01 = SiteModel(
        id="site-01",
        name="Site 01 - Riverside Development",
        location_name="Danube Valley, Sector 4",
        latitude=48.2082,
        longitude=16.3738,
        boundary={
            "type": "Polygon",
            "coordinates": [
                [
                    [16.3688, 48.2032],
                    [16.3788, 48.2032],
                    [16.3788, 48.2132],
                    [16.3688, 48.2132],
                    [16.3688, 48.2032],
                ]
            ],
        },
        description="Active commercial and residential construction along the river corridor.",
        tags=["building", "construction", "river", "urban", "new buildings near a river"],
        meta_info={"primary_change": "BUILDING", "region": "Central Europe"},
    )
    db.add(site_01)

    # Site 01 River spatial feature (within 320m)
    river_01 = SpatialFeatureModel(
        id="feat-danube-river",
        site_id="site-01",
        feature_type="river",
        name="Danube River Channel",
        geometry={
            "type": "LineString",
            "coordinates": [
                [16.3650, 48.2050],
                [16.3720, 48.2070],
                [16.3760, 48.2090],
                [16.3820, 48.2120],
            ],
        },
        meta_info={"flow_direction": "SE", "water_class": "river"},
    )
    db.add(river_01)

    # Site 01 Observations (March 2024 to January 2025)
    obs_01_a = ObservationModel(
        id="obs-site01-20240315",
        site_id="site-01",
        acquisition_date=date(2024, 3, 15),
        sensor="Sentinel-2B",
        resolution_meters=10.0,
        cloud_cover=2.1,
        usable=True,
        asset_path="data/demo/rasters/site-01_before.tif",
        thumbnail_url="/api/v1/sites/site-01/thumbnail/before",
        bands=["B02", "B03", "B04", "B08"],
    )
    obs_01_b = ObservationModel(
        id="obs-site01-20250120",
        site_id="site-01",
        acquisition_date=date(2025, 1, 20),
        sensor="Sentinel-2A",
        resolution_meters=10.0,
        cloud_cover=1.4,
        usable=True,
        asset_path="data/demo/rasters/site-01_after.tif",
        thumbnail_url="/api/v1/sites/site-01/thumbnail/after",
        bands=["B02", "B03", "B04", "B08"],
    )
    db.add_all([obs_01_a, obs_01_b])

    # Site 01 Change Event
    chg_01 = ChangeEventModel(
        id="chg-site01-building",
        site_id="site-01",
        change_type="BUILDING",
        earlier_date=date(2024, 3, 15),
        later_date=date(2025, 1, 20),
        earlier_observation_id="obs-site01-20240315",
        later_observation_id="obs-site01-20250120",
        area_sq_meters=4250.0,
        status="SUPPORTED",
        model_name="UNet-ResNet34-ChangeNet",
        model_tier="DEMO",
        geometry={
            "type": "Polygon",
            "coordinates": [
                [
                    [16.3720, 48.2075],
                    [16.3745, 48.2075],
                    [16.3745, 48.2095],
                    [16.3720, 48.2095],
                    [16.3720, 48.2075],
                ]
            ],
        },
        provenance={"confidence_method": "structural_edge_delineation"},
    )
    db.add(chg_01)

    # Site 02: Industrial Expansion (Rhine Corridor)
    site_02 = SiteModel(
        id="site-02",
        name="Site 02 - Industrial Logistics Expansion",
        location_name="Rhine Logistics Corridor",
        latitude=50.9375,
        longitude=6.9603,
        boundary={
            "type": "Polygon",
            "coordinates": [
                [[6.9553, 50.9325], [6.9653, 50.9325], [6.9653, 50.9425], [6.9553, 50.9425], [6.9553, 50.9325]]
            ],
        },
        description="Earthworks and early construction staging near railway interchange.",
        tags=["construction", "industrial", "earthworks", "railway"],
        meta_info={"primary_change": "BUILDING", "region": "Western Europe"},
    )
    db.add(site_02)

    obs_02_a = ObservationModel(
        id="obs-site02-20240410",
        site_id="site-02",
        acquisition_date=date(2024, 4, 10),
        sensor="Sentinel-2A",
        usable=True,
        asset_path="data/demo/rasters/site-02_before.tif",
        thumbnail_url="/api/v1/sites/site-02/thumbnail/before",
    )
    obs_02_b = ObservationModel(
        id="obs-site02-20250212",
        site_id="site-02",
        acquisition_date=date(2025, 2, 12),
        sensor="Sentinel-2B",
        usable=True,
        asset_path="data/demo/rasters/site-02_after.tif",
        thumbnail_url="/api/v1/sites/site-02/thumbnail/after",
    )
    db.add_all([obs_02_a, obs_02_b])

    chg_02 = ChangeEventModel(
        id="chg-site02-construction",
        site_id="site-02",
        change_type="BUILDING",
        earlier_date=date(2024, 4, 10),
        later_date=date(2025, 2, 12),
        area_sq_meters=6100.0,
        status="NEEDS_REVIEW",
        model_name="DemoChangeDetectionAdapter",
        model_tier="DEMO",
    )
    db.add(chg_02)

    # Site 03: Road Development (Bavaria Link)
    site_03 = SiteModel(
        id="site-03",
        name="Site 03 - Highway Bypass Construction",
        location_name="Bavaria North Link",
        latitude=49.4521,
        longitude=11.0767,
        boundary={
            "type": "Polygon",
            "coordinates": [
                [[11.0717, 49.4471], [11.0817, 49.4471], [11.0817, 49.4571], [11.0717, 49.4571], [11.0717, 49.4471]]
            ],
        },
        description="Linear corridor grading and paving of new arterial bypass.",
        tags=["road", "highway", "infrastructure", "transport"],
        meta_info={"primary_change": "ROAD", "region": "Central Europe"},
    )
    db.add(site_03)

    obs_03_a = ObservationModel(
        id="obs-site03-20240502",
        site_id="site-03",
        acquisition_date=date(2024, 5, 2),
        sensor="Sentinel-2A",
        usable=True,
        asset_path="data/demo/rasters/site-03_before.tif",
        thumbnail_url="/api/v1/sites/site-03/thumbnail/before",
    )
    obs_03_b = ObservationModel(
        id="obs-site03-20241215",
        site_id="site-03",
        acquisition_date=date(2024, 12, 15),
        sensor="Sentinel-2B",
        usable=True,
        asset_path="data/demo/rasters/site-03_after.tif",
        thumbnail_url="/api/v1/sites/site-03/thumbnail/after",
    )
    db.add_all([obs_03_a, obs_03_b])

    chg_03 = ChangeEventModel(
        id="chg-site03-road",
        site_id="site-03",
        change_type="ROAD",
        earlier_date=date(2024, 5, 2),
        later_date=date(2024, 12, 15),
        area_sq_meters=8500.0,
        status="SUPPORTED",
        model_name="DemoChangeDetectionAdapter",
        model_tier="DEMO",
    )
    db.add(chg_03)

    # Site 04: Vegetation Loss (Black Forest Basin)
    site_04 = SiteModel(
        id="site-04",
        name="Site 04 - Forest Canopy Loss",
        location_name="Black Forest Basin",
        latitude=48.0501,
        longitude=8.2014,
        boundary={
            "type": "Polygon",
            "coordinates": [
                [[8.1964, 48.0451], [8.2064, 48.0451], [8.2064, 48.0551], [8.1964, 48.0551], [8.1964, 48.0451]]
            ],
        },
        description="Significant drop in canopy density and NDVI following seasonal storm damage and logging.",
        tags=["vegetation", "forest", "canopy", "loss", "deforestation"],
        meta_info={"primary_change": "VEGETATION", "region": "Southwest Germany"},
    )
    db.add(site_04)

    obs_04_a = ObservationModel(
        id="obs-site04-20240218",
        site_id="site-04",
        acquisition_date=date(2024, 2, 18),
        sensor="Sentinel-2A",
        usable=True,
        asset_path="data/demo/rasters/site-04_before.tif",
        thumbnail_url="/api/v1/sites/site-04/thumbnail/before",
    )
    obs_04_b = ObservationModel(
        id="obs-site04-20241120",
        site_id="site-04",
        acquisition_date=date(2024, 11, 20),
        sensor="Sentinel-2B",
        usable=True,
        asset_path="data/demo/rasters/site-04_after.tif",
        thumbnail_url="/api/v1/sites/site-04/thumbnail/after",
    )
    db.add_all([obs_04_a, obs_04_b])

    chg_04 = ChangeEventModel(
        id="chg-site04-vegetation",
        site_id="site-04",
        change_type="VEGETATION",
        earlier_date=date(2024, 2, 18),
        later_date=date(2024, 11, 20),
        area_sq_meters=14200.0,
        status="SUPPORTED",
        model_name="DemoSpectralNDVIDetector",
        model_tier="DEMO",
    )
    db.add(chg_04)

    # Site 05: Water Extent Change (Alps Catchment)
    site_05 = SiteModel(
        id="site-05",
        name="Site 05 - Reservoir Surface Extent Change",
        location_name="Alps Catchment Reservoir",
        latitude=47.2692,
        longitude=11.4041,
        boundary={
            "type": "Polygon",
            "coordinates": [
                [[11.3991, 47.2642], [11.4091, 47.2642], [11.4091, 47.2742], [11.3991, 47.2742], [11.3991, 47.2642]]
            ],
        },
        description="Seasonal reservoir contraction and shoreline exposure analyzed via MNDWI index.",
        tags=["water", "reservoir", "lake", "hydrology"],
        meta_info={"primary_change": "WATER", "region": "Alps"},
    )
    db.add(site_05)

    obs_05_a = ObservationModel(
        id="obs-site05-20240614",
        site_id="site-05",
        acquisition_date=date(2024, 6, 14),
        sensor="Sentinel-2B",
        usable=True,
        asset_path="data/demo/rasters/site-05_before.tif",
        thumbnail_url="/api/v1/sites/site-05/thumbnail/before",
    )
    obs_05_b = ObservationModel(
        id="obs-site05-20250108",
        site_id="site-05",
        acquisition_date=date(2025, 1, 8),
        sensor="Sentinel-2A",
        usable=True,
        asset_path="data/demo/rasters/site-05_after.tif",
        thumbnail_url="/api/v1/sites/site-05/thumbnail/after",
    )
    db.add_all([obs_05_a, obs_05_b])

    chg_05 = ChangeEventModel(
        id="chg-site05-water",
        site_id="site-05",
        change_type="WATER",
        earlier_date=date(2024, 6, 14),
        later_date=date(2025, 1, 8),
        area_sq_meters=19500.0,
        status="SUPPORTED",
        model_name="DemoSpectralMNDWIDetector",
        model_tier="DEMO",
    )
    db.add(chg_05)

    db.commit()
    print("Database seeding completed.")

    # Populate Qdrant vector index
    print("Populating vector index...")
    sites = [site_01, site_02, site_03, site_04, site_05]
    for s in sites:
        vec = embedder.embed_text(f"{s.name} {s.description} {' '.join(s.tags)}")
        vector_mgr.upsert_observation(
            point_id=s.id,
            vector=vec,
            payload={
                "site_id": s.id,
                "name": s.name,
                "location": s.location_name,
                "tags": s.tags,
                "primary_change": s.meta_info.get("primary_change"),
            },
        )
    print("Vector index populated with 5 demo sites.")
    db.close()


if __name__ == "__main__":
    seed_demo_data()
