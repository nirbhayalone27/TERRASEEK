"""Spatial reasoning and geometry verification using Shapely and pyproj."""

from typing import Any, Dict, List, Optional, Tuple
import pyproj
from shapely.geometry import Point, Polygon, MultiPolygon, LineString, shape
from shapely.ops import transform

from terraseek.schemas.common import EvidenceStatus
from terraseek.schemas.spatial import SpatialCheckResult, SpatialConstraint, SpatialVerificationResult

# Geodesic transformer for metric distance (WGS84 lat/lon to Web Mercator or Local UTM)
wgs84 = pyproj.CRS("EPSG:4326")
mercator = pyproj.CRS("EPSG:3857")
project_to_meters = pyproj.Transformer.from_crs(wgs84, mercator, always_xy=True).transform


class SpatialEngine:
    @staticmethod
    def parse_geometry(geom_dict: Dict[str, Any]):
        """Safely parse a GeoJSON geometry dictionary into a Shapely shape."""
        try:
            return shape(geom_dict)
        except Exception as e:
            raise ValueError(f"Invalid GeoJSON geometry: {e}")

    @staticmethod
    def calculate_distance_meters(geom1_dict: Dict[str, Any], geom2_dict: Dict[str, Any]) -> float:
        """Calculate geodesic distance between two GeoJSON geometries in meters."""
        s1 = SpatialEngine.parse_geometry(geom1_dict)
        s2 = SpatialEngine.parse_geometry(geom2_dict)

        s1_m = transform(project_to_meters, s1)
        s2_m = transform(project_to_meters, s2)

        return float(s1_m.distance(s2_m))

    @staticmethod
    def verify_within_distance(
        site_geometry: Dict[str, Any],
        target_features: List[Dict[str, Any]],
        max_distance_meters: float,
        target_type: str = "river",
    ) -> SpatialCheckResult:
        """Verify whether a site is within max_distance_meters of any target feature."""
        if not target_features:
            return SpatialCheckResult(
                constraint=SpatialConstraint(feature_type=target_type, relation="within", distance_meters=max_distance_meters),
                satisfied=False,
                measured_distance_meters=None,
                target_feature_name=None,
                description=f"No {target_type} features found in the site region for verification.",
            )

        min_dist = float("inf")
        closest_name = None

        for feat in target_features:
            feat_geom = feat.get("geometry")
            if not feat_geom:
                continue
            dist = SpatialEngine.calculate_distance_meters(site_geometry, feat_geom)
            if dist < min_dist:
                min_dist = dist
                closest_name = feat.get("name", target_type)

        satisfied = min_dist <= max_distance_meters
        desc = (
            f"Within {round(min_dist, 1)}m of {closest_name} (Threshold: <= {max_distance_meters}m)"
            if satisfied
            else f"Nearest {target_type} ({closest_name}) is {round(min_dist, 1)}m away (Exceeds {max_distance_meters}m)"
        )

        return SpatialCheckResult(
            constraint=SpatialConstraint(feature_type=target_type, relation="within", distance_meters=max_distance_meters),
            satisfied=satisfied,
            measured_distance_meters=round(min_dist, 1),
            target_feature_name=closest_name,
            description=desc,
        )

    @staticmethod
    def verify_constraints(
        site_geometry: Dict[str, Any],
        constraints: List[SpatialConstraint],
        available_features: List[Dict[str, Any]],
    ) -> SpatialVerificationResult:
        """Verify all spatial constraints against available spatial features."""
        checks: List[SpatialCheckResult] = []
        all_satisfied = True

        for c in constraints:
            matching_features = [
                f for f in available_features
                if c.feature_type.lower() in f.get("feature_type", "").lower()
                or c.feature_type.lower() in f.get("name", "").lower()
            ]
            check = SpatialEngine.verify_within_distance(
                site_geometry=site_geometry,
                target_features=matching_features,
                max_distance_meters=c.distance_meters,
                target_type=c.feature_type,
            )
            checks.append(check)
            if not check.satisfied:
                all_satisfied = False

        status = EvidenceStatus.SUPPORTED if all_satisfied else EvidenceStatus.NO_MATCH
        summary = (
            f"All {len(checks)} spatial constraint(s) satisfied."
            if all_satisfied
            else f"Spatial constraint failed: {next((c.description for c in checks if not c.satisfied), 'Constraint not met')}"
        )

        return SpatialVerificationResult(
            status=status,
            checks=checks,
            summary=summary,
        )
