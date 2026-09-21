"""Pydantic schemas for TerraSeek."""

from terraseek.schemas.common import (
    APIErrorDetails,
    APIErrorResponse,
    ChangeType,
    EvidenceStatus,
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    GeoJSONGeometry,
    JobStatus,
    ModelTier,
    ReviewDecisionType,
)
from terraseek.schemas.site import SiteBase, SiteCreate, SiteDetail, SiteRead
from terraseek.schemas.observation import ObservationBase, ObservationCreate, ObservationRead
from terraseek.schemas.change import (
    ChangeAnalyzeRequest,
    ChangeAnalyzeResult,
    ChangeEventBase,
    ChangeEventRead,
    CompareRequest,
    CompareResult,
)
from terraseek.schemas.spatial import (
    SpatialCheckResult,
    SpatialConstraint,
    SpatialVerificationRequest,
    SpatialVerificationResult,
)
from terraseek.schemas.temporal import (
    EarliestObservationRequest,
    EarliestObservationResult,
    TemporalObservation,
    TemporalVerificationRequest,
    TemporalVerificationResult,
)
from terraseek.schemas.evidence import EvidenceItem, EvidencePassport, EvidenceType
from terraseek.schemas.search import (
    MissionIntent,
    SearchRequest,
    SearchResponse,
    SearchResultItem,
    SimilarRetrievalItem,
    SimilarRetrievalRequest,
    SimilarRetrievalResponse,
)
from terraseek.schemas.review import (
    ReviewDecisionCreate,
    ReviewDecisionRead,
    ReviewTaskBase,
    ReviewTaskCreate,
    ReviewTaskRead,
)
from terraseek.schemas.job import JobCreate, JobRead
from terraseek.schemas.report import ReportCreate, ReportRead
from terraseek.schemas.ingestion import IngestionItemCreate, IngestionResult

__all__ = [
    "APIErrorDetails",
    "APIErrorResponse",
    "ChangeType",
    "EvidenceStatus",
    "GeoJSONFeature",
    "GeoJSONFeatureCollection",
    "GeoJSONGeometry",
    "JobStatus",
    "ModelTier",
    "ReviewDecisionType",
    "SiteBase",
    "SiteCreate",
    "SiteDetail",
    "SiteRead",
    "ObservationBase",
    "ObservationCreate",
    "ObservationRead",
    "ChangeAnalyzeRequest",
    "ChangeAnalyzeResult",
    "ChangeEventBase",
    "ChangeEventRead",
    "CompareRequest",
    "CompareResult",
    "SpatialCheckResult",
    "SpatialConstraint",
    "SpatialVerificationRequest",
    "SpatialVerificationResult",
    "EarliestObservationRequest",
    "EarliestObservationResult",
    "TemporalObservation",
    "TemporalVerificationRequest",
    "TemporalVerificationResult",
    "EvidenceItem",
    "EvidencePassport",
    "EvidenceType",
    "MissionIntent",
    "SearchRequest",
    "SearchResponse",
    "SearchResultItem",
    "SimilarRetrievalItem",
    "SimilarRetrievalRequest",
    "SimilarRetrievalResponse",
    "ReviewDecisionCreate",
    "ReviewDecisionRead",
    "ReviewTaskBase",
    "ReviewTaskCreate",
    "ReviewTaskRead",
    "JobCreate",
    "JobRead",
    "ReportCreate",
    "ReportRead",
    "IngestionItemCreate",
    "IngestionResult",
]
