"""Unit tests for Discovery parser and Mission Compiler."""

import pytest
from terraseek.discovery.compiler import MissionCompiler
from terraseek.schemas.common import ChangeType


def test_parse_new_buildings_near_river():
    intent = MissionCompiler.parse_query("new buildings near a river")
    assert intent.target_entity == "building"
    assert intent.change_type == ChangeType.BUILDING
    assert intent.change_detected_required is True
    assert len(intent.spatial_constraints) == 1
    assert intent.spatial_constraints[0]["feature"] == "river"
    assert intent.spatial_constraints[0]["distance_meters"] == 500.0


def test_parse_road_development():
    intent = MissionCompiler.parse_query("road development")
    assert intent.target_entity == "road"
    assert intent.change_type == ChangeType.ROAD
    assert intent.change_detected_required is True


def test_parse_vegetation_loss():
    intent = MissionCompiler.parse_query("vegetation loss")
    assert intent.target_entity == "vegetation"
    assert intent.change_type == ChangeType.VEGETATION


def test_parse_water_change():
    intent = MissionCompiler.parse_query("water change")
    assert intent.target_entity == "water"
    assert intent.change_type == ChangeType.WATER


def test_parse_unmatchable_airport():
    intent = MissionCompiler.parse_query("new airport")
    assert intent.target_entity == "airport"
    assert intent.is_known_unmatchable is True


def test_parse_missing_earlier_imagery():
    intent = MissionCompiler.parse_query("new construction where earlier imagery is unavailable")
    assert intent.earlier_imagery_required is False
