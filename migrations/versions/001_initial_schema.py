"""Initial TerraSeek schema

Revision ID: 001_initial
Revises: 
Create Date: 2026-09-22 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Sites table
    op.create_table(
        'sites',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, index=True),
        sa.Column('location_name', sa.String(length=255), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('boundary', sa.JSON(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('meta_info', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # Observations table
    op.create_table(
        'observations',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('site_id', sa.String(length=36), sa.ForeignKey('sites.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('acquisition_date', sa.Date(), nullable=False, index=True),
        sa.Column('sensor', sa.String(length=100), nullable=True),
        sa.Column('resolution_meters', sa.Float(), nullable=True),
        sa.Column('cloud_cover', sa.Float(), nullable=True),
        sa.Column('usable', sa.Boolean(), nullable=True),
        sa.Column('asset_path', sa.String(length=500), nullable=True),
        sa.Column('thumbnail_url', sa.String(length=500), nullable=True),
        sa.Column('bands', sa.JSON(), nullable=True),
        sa.Column('meta_info', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # Spatial features table
    op.create_table(
        'spatial_features',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('site_id', sa.String(length=36), sa.ForeignKey('sites.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('feature_type', sa.String(length=100), nullable=False, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('geometry', sa.JSON(), nullable=False),
        sa.Column('meta_info', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # Change events table
    op.create_table(
        'change_events',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('site_id', sa.String(length=36), sa.ForeignKey('sites.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('change_type', sa.String(length=50), nullable=False, index=True),
        sa.Column('earlier_date', sa.Date(), nullable=False),
        sa.Column('later_date', sa.Date(), nullable=False),
        sa.Column('earlier_observation_id', sa.String(length=36), nullable=True),
        sa.Column('later_observation_id', sa.String(length=36), nullable=True),
        sa.Column('area_sq_meters', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('model_name', sa.String(length=100), nullable=True),
        sa.Column('model_tier', sa.String(length=50), nullable=True),
        sa.Column('geometry', sa.JSON(), nullable=True),
        sa.Column('provenance', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # Evidence records table
    op.create_table(
        'evidence_records',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('site_id', sa.String(length=36), sa.ForeignKey('sites.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('query', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('spatial_summary', sa.Text(), nullable=True),
        sa.Column('temporal_summary', sa.Text(), nullable=True),
        sa.Column('change_summary', sa.Text(), nullable=True),
        sa.Column('model_provenance', sa.JSON(), nullable=True),
        sa.Column('limitations', sa.JSON(), nullable=True),
        sa.Column('needs_review_reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # Evidence items table
    op.create_table(
        'evidence_items',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('record_id', sa.String(length=36), sa.ForeignKey('evidence_records.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('evidence_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('source', sa.String(length=255), nullable=False),
        sa.Column('asset_id', sa.String(length=100), nullable=True),
        sa.Column('observation_id', sa.String(length=36), nullable=True),
        sa.Column('method', sa.String(length=100), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('geometry', sa.JSON(), nullable=True),
        sa.Column('meta_info', sa.JSON(), nullable=True),
    )

    # Review tasks table
    op.create_table(
        'review_tasks',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('site_id', sa.String(length=36), sa.ForeignKey('sites.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('evidence_id', sa.String(length=36), nullable=False, index=True),
        sa.Column('query', sa.String(length=500), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('flagged_by', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), default='PENDING'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # Review decisions table
    op.create_table(
        'review_decisions',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('task_id', sa.String(length=36), sa.ForeignKey('review_tasks.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('decision', sa.String(length=50), nullable=False),
        sa.Column('reviewer_notes', sa.Text(), nullable=False),
        sa.Column('reviewer_id', sa.String(length=100), nullable=False),
        sa.Column('decided_at', sa.DateTime(), nullable=True),
    )

    # Jobs table
    op.create_table(
        'jobs',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('job_type', sa.String(length=100), nullable=False, index=True),
        sa.Column('status', sa.String(length=50), default='QUEUED', index=True),
        sa.Column('progress_percentage', sa.Float(), default=0.0),
        sa.Column('payload', sa.JSON(), nullable=True),
        sa.Column('result', sa.JSON(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
    )

    # Reports table
    op.create_table(
        'reports',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('site_id', sa.String(length=36), sa.ForeignKey('sites.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('query', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('report_format', sa.String(length=20), default='json'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('reports')
    op.drop_table('jobs')
    op.drop_table('review_decisions')
    op.drop_table('review_tasks')
    op.drop_table('evidence_items')
    op.drop_table('evidence_records')
    op.drop_table('change_events')
    op.drop_table('spatial_features')
    op.drop_table('observations')
    op.drop_table('sites')
