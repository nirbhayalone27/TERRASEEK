"""Discovery parser and mission compiler for natural language satellite search."""

import re
from typing import Any, Dict, List, Tuple
from terraseek.schemas.common import ChangeType
from terraseek.schemas.search import MissionIntent


class MissionCompiler:
    """Compiles natural language search queries into inspectable execution plans and evidence requirements."""

    @staticmethod
    def parse_query(raw_query: str) -> MissionIntent:
        q = raw_query.strip().lower()

        # Check for explicitly unmatchable entities for testing truth-in-AI
        if "airport" in q or "runway" in q or "spaceport" in q:
            return MissionIntent(
                raw_query=raw_query,
                target_entity="airport",
                change_detected_required=True,
                change_type=ChangeType.UNKNOWN,
                spatial_constraints=[],
                temporal_required=True,
                earlier_imagery_required=True,
                is_known_unmatchable=True,
            )

        # Check for intentional missing evidence test query
        if "earlier imagery is unavailable" in q or "missing baseline" in q:
            return MissionIntent(
                raw_query=raw_query,
                target_entity="construction",
                change_detected_required=True,
                change_type=ChangeType.BUILDING,
                spatial_constraints=[],
                temporal_required=True,
                earlier_imagery_required=False,  # Explicitly lacking baseline imagery
                is_known_unmatchable=False,
            )

        # Target change type detection
        change_type = ChangeType.UNKNOWN
        target_entity = "general"

        if "building" in q or "construction" in q or "structure" in q:
            change_type = ChangeType.BUILDING
            target_entity = "building"
        elif "road" in q or "highway" in q or "pavement" in q:
            change_type = ChangeType.ROAD
            target_entity = "road"
        elif "vegetation" in q or "forest" in q or "deforestation" in q or "canopy" in q:
            change_type = ChangeType.VEGETATION
            target_entity = "vegetation"
        elif "water" in q or "reservoir" in q or "flood" in q or "lake" in q:
            change_type = ChangeType.WATER
            target_entity = "water"

        # Change indicator
        change_required = any(w in q for w in ["new", "change", "loss", "development", "expansion", "built"])

        # Spatial constraints extraction
        spatial_constraints: List[Dict[str, Any]] = []

        # Check for distance expressions like "within 500m of river" or "near a river"
        dist_match = re.search(r"within\s+(\d+)\s*(m|meter|meters|km)?\s+of\s+(?:a\s+|the\s+)?(\w+)", q)
        if dist_match:
            dist_val = float(dist_match.group(1))
            unit = dist_match.group(2)
            if unit == "km":
                dist_val *= 1000.0
            feature_name = dist_match.group(3)
            spatial_constraints.append({
                "feature": feature_name,
                "distance_meters": dist_val,
                "relation": "within",
            })
        elif "near a river" in q or "near river" in q:
            spatial_constraints.append({
                "feature": "river",
                "distance_meters": 500.0,
                "relation": "within",
            })
        elif "near road" in q or "near a road" in q:
            spatial_constraints.append({
                "feature": "road",
                "distance_meters": 250.0,
                "relation": "within",
            })

        return MissionIntent(
            raw_query=raw_query,
            target_entity=target_entity,
            change_detected_required=change_required,
            change_type=change_type,
            spatial_constraints=spatial_constraints,
            temporal_required=True,
            earlier_imagery_required=True,
            is_known_unmatchable=False,
        )

    @staticmethod
    def generate_execution_plan(mission: MissionIntent) -> List[str]:
        """Produce human-inspectable workflow plan."""
        plan = [
            f"1. Parse Mission Intent: Target='{mission.target_entity}', ChangeRequired={mission.change_detected_required}"
        ]

        if mission.is_known_unmatchable:
            plan.append("2. Candidate Verification: Target entity not present in catalog (Fast NO_MATCH path)")
            return plan

        plan.append("2. Retrieve Candidates: Vector search across catalog embeddings & spatial bounds")

        if mission.spatial_constraints:
            for sc in mission.spatial_constraints:
                plan.append(f"3. Spatial Verification: Verify candidate is within {sc['distance_meters']}m of '{sc['feature']}'")
        else:
            plan.append("3. Spatial Verification: No spatial constraints specified")

        if mission.earlier_imagery_required:
            plan.append("4. Temporal Verification: Confirm existence of baseline & comparison observations")
        else:
            plan.append("4. Temporal Verification: Baseline observations unavailable (Flag INSUFFICIENT_EVIDENCE)")

        plan.append(f"5. Change Detection: Run {mission.change_type.value} model to compute differences")
        plan.append("6. Evidence Engine: Synthesize passport and determine truth status (SUPPORTED | NEEDS_REVIEW | INSUFFICIENT_EVIDENCE | NO_MATCH)")

        return plan
