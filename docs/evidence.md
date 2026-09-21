# Evidence Passport & Truth Policy Engine

TerraSeek enforces strict evidence-backed conclusions distinguishing four primary truth statuses:

## Truth Statuses

| Status | Meaning | System Action |
|---|---|---|
| **SUPPORTED** | All spatial, temporal, and change criteria are satisfied. | Certified search result displayed with full evidence passport. |
| **NEEDS_REVIEW** | Evidence exists but criteria is borderline or has gaps. | Escalated automatically to human analyst review queue. |
| **INSUFFICIENT_EVIDENCE** | Crucial baseline passes or required evidence components are missing. | Clear explainable report detailing missing imagery. |
| **NO_MATCH** | Target feature absent from catalog or spatial constraint violated. | Zero matches reported. Zero false entities fabricated. |

## Evidence Passport Specification
Each conclusion produces an immutable passport containing:
- `id`: Unique UUID.
- `site_id`: Target site.
- `query`: Analyst search query.
- `status`: Ground-truth determination.
- `items`: Itemized evidence checks (RETRIEVAL, SPATIAL, TEMPORAL, STRUCTURAL, SPECTRAL).
- `model_provenance`: Information on model versions, tier, weights, and parameters.
- `limitations`: Stated operating parameters and GSD constraints.
