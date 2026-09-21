"""SQLAlchemy ORM models for TerraSeek."""

import uuid
from datetime import datetime, date
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def generate_uuid() -> str:
    return str(uuid.uuid4())


class SiteModel(Base):
    __tablename__ = "sites"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False, index=True)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    boundary = Column(JSON, nullable=True)  # GeoJSON polygon/multipolygon
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)
    meta_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    observations = relationship("ObservationModel", back_populates="site", cascade="all, delete-orphan")
    spatial_features = relationship("SpatialFeatureModel", back_populates="site", cascade="all, delete-orphan")
    change_events = relationship("ChangeEventModel", back_populates="site", cascade="all, delete-orphan")
    evidence_records = relationship("EvidenceRecordModel", back_populates="site", cascade="all, delete-orphan")
    review_tasks = relationship("ReviewTaskModel", back_populates="site", cascade="all, delete-orphan")
    reports = relationship("ReportModel", back_populates="site", cascade="all, delete-orphan")


class ObservationModel(Base):
    __tablename__ = "observations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    site_id = Column(String(36), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    acquisition_date = Column(Date, nullable=False, index=True)
    sensor = Column(String(100), default="Sentinel-2")
    resolution_meters = Column(Float, default=10.0)
    cloud_cover = Column(Float, default=0.0)
    usable = Column(Boolean, default=True)
    asset_path = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    bands = Column(JSON, default=list)
    meta_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    site = relationship("SiteModel", back_populates="observations")


class SpatialFeatureModel(Base):
    __tablename__ = "spatial_features"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    site_id = Column(String(36), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    feature_type = Column(String(100), nullable=False, index=True)  # river, road, water_body, building
    name = Column(String(255), nullable=False)
    geometry = Column(JSON, nullable=False)  # GeoJSON representation
    meta_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    site = relationship("SiteModel", back_populates="spatial_features")


class ChangeEventModel(Base):
    __tablename__ = "change_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    site_id = Column(String(36), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    change_type = Column(String(50), nullable=False, index=True)  # BUILDING, ROAD, VEGETATION, WATER
    earlier_date = Column(Date, nullable=False)
    later_date = Column(Date, nullable=False)
    earlier_observation_id = Column(String(36), nullable=True)
    later_observation_id = Column(String(36), nullable=True)
    area_sq_meters = Column(Float, default=0.0)
    status = Column(String(50), default="SUPPORTED")
    model_name = Column(String(100), default="demo-change-detector")
    model_tier = Column(String(50), default="DEMO")
    geometry = Column(JSON, nullable=True)  # GeoJSON of changed polygon
    provenance = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    site = relationship("SiteModel", back_populates="change_events")


class EvidenceRecordModel(Base):
    __tablename__ = "evidence_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    site_id = Column(String(36), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    query = Column(String(500), nullable=False)
    status = Column(String(50), nullable=False)  # SUPPORTED, NEEDS_REVIEW, INSUFFICIENT_EVIDENCE, NO_MATCH
    spatial_summary = Column(Text, default="")
    temporal_summary = Column(Text, default="")
    change_summary = Column(Text, default="")
    model_provenance = Column(JSON, default=dict)
    limitations = Column(JSON, default=list)
    needs_review_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    site = relationship("SiteModel", back_populates="evidence_records")
    items = relationship("EvidenceItemModel", back_populates="record", cascade="all, delete-orphan")


class EvidenceItemModel(Base):
    __tablename__ = "evidence_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    record_id = Column(String(36), ForeignKey("evidence_records.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_type = Column(String(50), nullable=False)  # RETRIEVAL, SPATIAL, TEMPORAL, STRUCTURAL, SPECTRAL
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    source = Column(String(255), nullable=False)
    asset_id = Column(String(100), nullable=True)
    observation_id = Column(String(36), nullable=True)
    method = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    geometry = Column(JSON, nullable=True)
    meta_info = Column(JSON, default=dict)

    record = relationship("EvidenceRecordModel", back_populates="items")


class ReviewTaskModel(Base):
    __tablename__ = "review_tasks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    site_id = Column(String(36), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_id = Column(String(36), nullable=False, index=True)
    query = Column(String(500), nullable=False)
    reason = Column(Text, nullable=False)
    flagged_by = Column(String(100), default="system")
    status = Column(String(50), default="PENDING")  # PENDING, RESOLVED
    created_at = Column(DateTime, default=datetime.utcnow)

    site = relationship("SiteModel", back_populates="review_tasks")
    decisions = relationship("ReviewDecisionModel", back_populates="task", cascade="all, delete-orphan")


class ReviewDecisionModel(Base):
    __tablename__ = "review_decisions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    task_id = Column(String(36), ForeignKey("review_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    decision = Column(String(50), nullable=False)  # APPROVE, REJECT, NEEDS_MORE_EVIDENCE
    reviewer_notes = Column(Text, nullable=False)
    reviewer_id = Column(String(100), nullable=False)
    decided_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("ReviewTaskModel", back_populates="decisions")


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    job_type = Column(String(100), nullable=False, index=True)
    status = Column(String(50), default="QUEUED", index=True)  # QUEUED, RUNNING, SUCCEEDED, FAILED, CANCELLED
    progress_percentage = Column(Float, default=0.0)
    payload = Column(JSON, default=dict)
    result = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)


class ReportModel(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    site_id = Column(String(36), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    query = Column(String(500), nullable=False)
    status = Column(String(50), nullable=False)
    content = Column(JSON, nullable=False)
    report_format = Column(String(20), default="json")
    created_at = Column(DateTime, default=datetime.utcnow)

    site = relationship("SiteModel", back_populates="reports")


class ModelRunModel(Base):
    __tablename__ = "model_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    model_name = Column(String(100), nullable=False, index=True)
    model_tier = Column(String(50), nullable=False)
    model_version = Column(String(50), nullable=False)
    inference_timestamp = Column(DateTime, default=datetime.utcnow)
    input_asset = Column(String(500), nullable=True)
    parameters = Column(JSON, default=dict)
    execution_time_ms = Column(Float, default=0.0)
