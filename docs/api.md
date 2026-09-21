# TerraSeek API Specification

Interactive Swagger documentation is exposed at `http://localhost:8000/docs` and ReDoc at `http://localhost:8000/redoc`.

Base Prefix: `/api/v1`

## Endpoints Summary

### System Health
- `GET /api/v1/health`: Liveness probe.
- `GET /api/v1/ready`: Readiness probe verifying PostgreSQL, Qdrant, and storage readiness.

### Search & Retrieval
- `POST /api/v1/search`: Executes natural language satellite query with full multi-domain evidence reasoning.
  - Body: `{"query": "new buildings near a river", "limit": 10}`
  - Returns: `SearchResponse` including mission intent, execution plan, and certified results.
- `POST /api/v1/retrieval/similar`: Vector similarity search across observations. Supports image file upload or site reference.

### Sites & Imagery
- `GET /api/v1/sites`: List registered sites.
- `GET /api/v1/sites/{site_id}`: Site detail with spatial, temporal, and change evidence summaries.
- `GET /api/v1/sites/{site_id}/observations`: Chronological list of satellite observation passes.
- `GET /api/v1/sites/{site_id}/changes`: Delineated change events and geometries.
- `GET /api/v1/sites/{site_id}/thumbnail/{view}`: Serves before/after visual thumbnail images.

### Change & Temporal Reasoning
- `POST /api/v1/change/analyze`: Automated multi-domain change detection.
- `POST /api/v1/change/compare`: Visual and analytical pair comparison.
- `POST /api/v1/temporal/verify`: Validates observation continuity and maximum gap days.
- `POST /api/v1/temporal/earliest`: Determines earliest supported observation date for an event.

### Evidence & Review
- `GET /api/v1/evidence/{evidence_id}`: Retrieves full Evidence Passport.
- `POST /api/v1/evidence/{evidence_id}/review`: Escalates evidence to human analyst queue.
- `GET /api/v1/review/queue`: List pending review tasks.
- `POST /api/v1/review/{review_id}/decision`: Submit reviewer decision (`APPROVE`, `REJECT`, `NEEDS_MORE_EVIDENCE`).

### Jobs & Reports
- `POST /api/v1/jobs`: Submit asynchronous background job.
- `GET /api/v1/jobs/{job_id}`: Poll background task status and results.
- `POST /api/v1/reports`: Generate official evidence report.
- `GET /api/v1/reports/{report_id}`: Retrieve evidence report.
- `POST /api/v1/ingestion/catalog`: Ingest and index new satellite raster assets.
