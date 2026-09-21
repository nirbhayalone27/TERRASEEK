"""Temporal reasoning engine for satellite observations and continuity checks."""

from datetime import date
from typing import Any, Dict, List, Optional
from terraseek.schemas.common import EvidenceStatus
from terraseek.schemas.temporal import TemporalObservation, TemporalVerificationResult


class TemporalEngine:
    @staticmethod
    def verify_timeline(
        observations: List[TemporalObservation],
        min_required: int = 2,
        max_allowed_gap_days: int = 365,
    ) -> TemporalVerificationResult:
        """Analyze observation timeline for temporal evidence and continuity."""
        usable = [obs for obs in observations if obs.usable]
        usable_sorted = sorted(usable, key=lambda x: x.acquisition_date)

        total_count = len(observations)
        usable_count = len(usable_sorted)

        if usable_count < min_required:
            return TemporalVerificationResult(
                status=EvidenceStatus.INSUFFICIENT_EVIDENCE,
                observations_count=total_count,
                usable_observations_count=usable_count,
                has_before_observation=usable_count >= 1,
                has_after_observation=False,
                earliest_supported_observation=usable_sorted[0].acquisition_date if usable_sorted else None,
                latest_observation=usable_sorted[-1].acquisition_date if usable_sorted else None,
                max_gap_days=None,
                summary=f"Insufficient temporal observations. Found {usable_count} usable, require at least {min_required}.",
            )

        # Calculate max gap between consecutive observations
        max_gap = 0
        for i in range(len(usable_sorted) - 1):
            gap = (usable_sorted[i + 1].acquisition_date - usable_sorted[i].acquisition_date).days
            if gap > max_gap:
                max_gap = gap

        earliest = usable_sorted[0].acquisition_date
        latest = usable_sorted[-1].acquisition_date

        has_gap_warning = max_gap > max_allowed_gap_days
        status = EvidenceStatus.NEEDS_REVIEW if has_gap_warning else EvidenceStatus.SUPPORTED

        summary = (
            f"Temporal evidence verified across {usable_count} usable observations ({earliest.strftime('%B %Y')} to {latest.strftime('%B %Y')})."
        )
        if has_gap_warning:
            summary += f" Notice: observation gap of {max_gap} days detected, human review recommended."

        return TemporalVerificationResult(
            status=status,
            observations_count=total_count,
            usable_observations_count=usable_count,
            has_before_observation=True,
            has_after_observation=True,
            earliest_supported_observation=earliest,
            latest_observation=latest,
            max_gap_days=max_gap,
            summary=summary,
        )

    @staticmethod
    def determine_earliest_supported_observation(
        observations: List[TemporalObservation],
        change_events: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Find the earliest satellite observation where the target feature/change is evidenced."""
        if not change_events:
            return {
                "status": EvidenceStatus.NO_MATCH,
                "earliest_date": None,
                "description": "No change events recorded for this site.",
            }

        usable = [obs for obs in observations if obs.usable]
        if not usable:
            return {
                "status": EvidenceStatus.INSUFFICIENT_EVIDENCE,
                "earliest_date": None,
                "description": "No usable observations found to determine earliest occurrence.",
            }

        # Find earliest change event date
        sorted_changes = sorted(change_events, key=lambda c: c.get("later_date") or date.max)
        earliest_change = sorted_changes[0]
        event_date = earliest_change.get("later_date")

        # Find the earliest observation on or after that date
        matching_obs = [obs for obs in usable if obs.acquisition_date >= event_date]
        if matching_obs:
            target_obs = min(matching_obs, key=lambda o: o.acquisition_date)
            return {
                "status": EvidenceStatus.SUPPORTED,
                "earliest_date": target_obs.acquisition_date,
                "observation_id": target_obs.id,
                "description": f"Earliest supported observation verified on {target_obs.acquisition_date.strftime('%B %d, %Y')}.",
            }

        return {
            "status": EvidenceStatus.NEEDS_REVIEW,
            "earliest_date": event_date,
            "description": f"Event recorded at {event_date} but no matching single observation confirmed.",
        }
